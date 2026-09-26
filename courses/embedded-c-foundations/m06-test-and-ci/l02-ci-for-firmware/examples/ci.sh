#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
#
# examples/ci.sh — การตรวจสี่ขั้นที่ CI รัน และคุณรันเองในเครื่องได้ด้วยคำสั่งเดียวกันทุกตัวอักษร
#
#     bash ci.sh tests    unit test ด้วย Unity แล้วพิสูจน์ว่า test ล้มเป็น (บทเรียน 6.1)
#     bash ci.sh format   รูปแบบโค้ดตรงกับ .clang-format ไหม
#     bash ci.sh static   วิเคราะห์แบบสถิตด้วย cppcheck
#     bash ci.sh cross    คอมไพล์ตรรกะด้วย arm-none-eabi-gcc สำหรับ Cortex-M33 และ Cortex-M55
#     bash ci.sh all      ทั้งสี่ขั้น แล้วสรุป
#
# ตัวแปรที่เปลี่ยนได้ (ค่าเริ่มต้นคือโครงของ repo ที่บทเรียน 6.2 แนะนำ)
#     SRC_DIR       โฟลเดอร์ของตรรกะและ test        ค่าเริ่มต้น host-tests
#     TEST          ไฟล์ test เทียบกับ SRC_DIR        ค่าเริ่มต้น test_level_alarm.c
#     UNITY_DIR     src ของ Unity                    ค่าเริ่มต้น $SRC_DIR/unity/src
#     CLANG_FORMAT  CPPCHECK  ARM_CC  ARM_SIZE       ใช้เมื่อเครื่องมืออยู่นอก PATH
#
# ทุกขั้นจบด้วยหนึ่งในสามผล: PASS, FAIL หรือ NOT CHECKED (เครื่องมือไม่มี หรือไม่มีไฟล์ให้ตรวจ)
# NOT CHECKED ไม่ใช่ PASS จึงคืนค่าที่ไม่ใช่ 0 เหมือนกัน

set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
SRC_DIR="${SRC_DIR:-host-tests}"
TEST="${TEST:-test_level_alarm.c}"
UNITY_DIR="${UNITY_DIR:-$SRC_DIR/unity/src}"
CLANG_FORMAT="${CLANG_FORMAT:-clang-format}"
CPPCHECK="${CPPCHECK:-cppcheck}"
ARM_CC="${ARM_CC:-arm-none-eabi-gcc}"
ARM_SIZE="${ARM_SIZE:-arm-none-eabi-size}"

# แฟล็กของ Cortex-M33 ตาม Makefile ของไลบรารีใน SDK ("MUST match project: softfp")
CM33_FLAGS=(-mcpu=cortex-m33 -mthumb -mfloat-abi=softfp -mfpu=fpv5-sp-d16)
CM55_FLAGS=(-mcpu=cortex-m55 -mthumb)
WARN_FLAGS=(-std=c11 -Wall -Wextra -Werror -O2 -ffunction-sections -fdata-sections)

not_checked() { echo "NOT CHECKED: $*"; exit 3; }
need() { command -v "$1" >/dev/null 2>&1 || not_checked "$1 is not installed (or set the variable that points to it)"; }

# ไฟล์ตรรกะ = ไฟล์ .c และ .h ระดับบนสุดของ SRC_DIR ที่ไม่ใช่ test
logic_sources() { find "$SRC_DIR" -maxdepth 1 -name '*.c' ! -name 'test_*' | sort; }
logic_headers() { find "$SRC_DIR" -maxdepth 1 -name '*.h' | sort; }
format_files() { logic_sources; logic_headers; if [ -f "$SRC_DIR/$TEST" ]; then echo "$SRC_DIR/$TEST"; fi; }

# อ่านรายการไฟล์ลงอาร์เรย์ files ทีละบรรทัด (bash 3.2 ของ macOS ไม่มี mapfile)
collect() {
    files=()
    while IFS= read -r f; do
        if [ -n "$f" ]; then files+=("$f"); fi
    done < <("$@")
}

stage_tests() {
    [ -f "$UNITY_DIR/unity.c" ] || not_checked "Unity not found at $UNITY_DIR (clone v2.7.0 first)"
    [ -f "$SRC_DIR/$TEST" ] || not_checked "test file $SRC_DIR/$TEST not found"
    make -C "$SRC_DIR" test TEST="$TEST" UNITY_DIR="$(cd "$UNITY_DIR" && pwd)"
    # test ที่ผ่านยังไม่พอ ต้องเห็นว่ามันล้มเมื่อโค้ดผิดด้วย
    bash "$SRC_DIR/prove_red.sh" "$SRC_DIR/$TEST" "$UNITY_DIR"
}

stage_format() {
    need "$CLANG_FORMAT"
    "$CLANG_FORMAT" --version
    collect format_files
    [ "${#files[@]}" -gt 0 ] || not_checked "no source files under $SRC_DIR"
    # ไม่มี --Werror แล้ว --dry-run จะพิมพ์คำเตือนแต่คืน 0 ขั้นนี้จะเขียวตลอด
    "$CLANG_FORMAT" --style="file:$HERE/.clang-format" --dry-run --Werror "${files[@]}"
    echo "format: ${#files[@]} files match .clang-format"
}

stage_static() {
    need "$CPPCHECK"
    "$CPPCHECK" --version
    collect logic_sources
    [ "${#files[@]}" -gt 0 ] || not_checked "no logic sources under $SRC_DIR"
    # ไม่มี --error-exitcode แล้ว cppcheck รายงาน error แต่คืน 0 ขั้นนี้จะเขียวตลอด
    "$CPPCHECK" --std=c11 --enable=warning,performance,portability --error-exitcode=1 \
        --inline-suppr --quiet -I "$SRC_DIR" "${files[@]}"
    echo "static: cppcheck found nothing in ${#files[@]} file(s)"
}

stage_cross() {
    need "$ARM_CC"
    "$ARM_CC" --version | head -n 1
    collect logic_sources
    [ "${#files[@]}" -gt 0 ] || not_checked "no logic sources under $SRC_DIR"
    local out
    out="$(mktemp -d)"
    trap 'rm -rf "$out"' RETURN
    for f in "${files[@]}"; do
        local name
        name="$(basename "$f" .c)"
        "$ARM_CC" "${CM33_FLAGS[@]}" "${WARN_FLAGS[@]}" -I "$SRC_DIR" -c "$f" -o "$out/$name.cm33.o"
        "$ARM_CC" "${CM55_FLAGS[@]}" "${WARN_FLAGS[@]}" -I "$SRC_DIR" -c "$f" -o "$out/$name.cm55.o"
    done
    if command -v "$ARM_SIZE" >/dev/null 2>&1; then
        "$ARM_SIZE" "$out"/*.o
    fi
    echo "cross: ${#files[@]} file(s) compile for Cortex-M33 and Cortex-M55 with -Werror"
}

run_stage() {   # รันหนึ่งขั้นใน subshell เพื่อให้ exit ของขั้นนั้นไม่หยุด "all"
    # อย่าเขียน ( stage ) || rc=$? เพราะ bash ปิด set -e ทั้งหมดใน subshell ที่อยู่หน้า ||
    # คำสั่งที่ล้มกลางขั้นจะถูกข้าม แล้วขั้นนั้นจบด้วย 0 กลายเป็น PASS ปลอม
    local rc
    set +e
    (
        set -e
        "stage_$1"
    )
    rc=$?
    set -e
    case "$rc" in
        0) echo "== $1: PASS" ;;
        3) echo "== $1: NOT CHECKED" ;;
        *) echo "== $1: FAIL (exit $rc)" ;;
    esac
    return "$rc"
}

case "${1:-}" in
    tests | format | static | cross)
        run_stage "$1"
        ;;
    all)
        bad=0
        for s in tests format static cross; do
            run_stage "$s" || bad=$((bad + 1))
        done
        echo "== all: $bad stage(s) did not pass"
        [ "$bad" -eq 0 ]
        ;;
    *)
        echo "usage: bash ci.sh tests|format|static|cross|all" >&2
        exit 2
        ;;
esac
