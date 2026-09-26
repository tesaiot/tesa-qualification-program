#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
#
# examples/prove_red.sh — พิสูจน์ว่า test ล้มเป็น ด้วยการจงใจใส่บั๊กทีละจุด (mutation) แล้วดูว่า test จับได้ไหม
#
#     bash prove_red.sh <ไฟล์ test> <โฟลเดอร์ src ของ Unity>
#     bash prove_red.sh ../solution/test_level_alarm.c unity/src
#
# ทุก mutant สร้างในโฟลเดอร์ชั่วคราวแล้วลบทิ้ง ไม่แตะ level_alarm.c ตัวจริง
# "killed" = test ล้มกับโค้ดที่มีบั๊ก (ดี)  "SURVIVED" = test ผ่านทั้งที่โค้ดผิด (test ยังไม่พอ)
# "SKIPPED" และ "BROKEN" = mutant นั้นไม่ได้พิสูจน์อะไร จึงนับเป็นความล้มเหลวด้วย ไม่ใช่ผ่าน

set -u
if [ $# -ne 2 ]; then
    echo "usage: bash prove_red.sh <test file> <unity src dir>" >&2
    exit 2
fi
HERE="$(cd "$(dirname "$0")" && pwd)"
TEST="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
UNITY="$(cd "$2" && pwd)"
CC="${CC:-cc}"
survived=0
unproven=0

# ชื่อ | ข้อความเดิมใน level_alarm.c | ข้อความที่แทน
mutants=(
  "threshold >= becomes >|(mv >= a->on_mv)|(mv > a->on_mv)"
  "hysteresis ignored|(mv < a->off_mv)|(mv < a->on_mv)"
  "no reset on a gap|a->count = 0u; // ต้องติดกัน|/* reset removed */ // ต้องติดกัน"
  "read failure reported as normal|        a->state = ALARM_FAULT;|        a->state = ALARM_NORMAL;"
)

run_suite() {   # $1 = source of level_alarm.c ; คืนค่า exit ของ test
    local dir="$1"
    "$CC" -std=c11 -Wall -Wextra -I"$HERE" -I"$UNITY" -o "$dir/t" "$TEST" "$dir/level_alarm.c" "$UNITY/unity.c" \
        >/dev/null 2>&1 || return 99
    "$dir/t" >/dev/null 2>&1
}

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

cp "$HERE/level_alarm.c" "$tmp/level_alarm.c"
if ! run_suite "$tmp"; then
    echo "the suite does not pass on the real code; fix that first"
    exit 1
fi
echo "baseline: all tests pass on the real code"

for m in "${mutants[@]}"; do
    IFS='|' read -r name from to <<< "$m"
    cp "$HERE/level_alarm.c" "$tmp/level_alarm.c"
    if ! grep -qF -- "$from" "$tmp/level_alarm.c"; then
        echo "SKIPPED  $name (pattern not found; the source changed)"
        unproven=$((unproven + 1))
        continue
    fi
    python3 - "$tmp/level_alarm.c" "$from" "$to" <<'PY'
import sys
p, a, b = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(p, encoding="utf-8").read()
open(p, "w", encoding="utf-8").write(s.replace(a, b, 1))
PY
    run_suite "$tmp"
    rc=$?
    if [ "$rc" -eq 0 ]; then
        echo "SURVIVED $name"
        survived=$((survived + 1))
    elif [ "$rc" -eq 99 ]; then
        echo "BROKEN   $name (mutant did not compile)"
        unproven=$((unproven + 1))
    else
        echo "killed   $name"
    fi
done
echo "survived: $survived  unproven: $unproven"
[ "$survived" -eq 0 ] && [ "$unproven" -eq 0 ]
