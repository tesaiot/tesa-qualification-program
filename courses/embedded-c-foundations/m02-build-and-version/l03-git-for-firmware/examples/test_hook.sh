#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
#
# examples/test_hook.sh — ทดสอบ pre-commit hook ใน repository ชั่วคราวที่สร้างแล้วลบทิ้งทุกกรณี
#
#     bash test_hook.sh ../practice/pre-commit.sh
#     bash test_hook.sh ../solution/pre-commit.sh
#
# ทุกกรณีสร้าง repository ใหม่ใน mktemp -d ไม่แตะ repository ของคุณ
# ค่าที่ดูเหมือนรหัสผ่านในไฟล์นี้เป็นข้อมูลทดสอบที่ตั้งใจให้ถูกปฏิเสธ ไม่ใช่รหัสของระบบใด

set -u
if [ $# -ne 1 ] || [ ! -f "$1" ]; then
    echo "usage: bash test_hook.sh <path to pre-commit.sh>" >&2
    exit 2
fi
HOOK="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
passed=0
failed=0

# case <ชื่อกรณี> <accept|reject> <path> <เนื้อหาไฟล์>
case_run() {
    local name="$1" expect="$2" path="$3" body="$4"
    local dir
    dir="$(mktemp -d)"
    (
        cd "$dir" || exit 99
        git init -q .
        git config user.email "test@example.invalid"
        git config user.name "hook test"
        cp "$HOOK" .git/hooks/pre-commit
        chmod +x .git/hooks/pre-commit
        mkdir -p "$(dirname "$path")"
        printf '%s\n' "$body" > "$path"
        git add -- "$path"
        git commit -q -m "test: $name" >/dev/null 2>&1
    )
    local rc=$?
    rm -rf "$dir"
    local got="reject"
    [ "$rc" -eq 0 ] && got="accept"
    if [ "$got" = "$expect" ]; then
        echo "PASS $name ($got)"
        passed=$((passed + 1))
    else
        echo "FAIL $name: expected $expect, got $got"
        failed=$((failed + 1))
    fi
}

hdr="-----BEGIN"   # ต่อสตริงตอนรัน ไฟล์นี้จึงไม่มีบรรทัดหัวของกุญแจจริงอยู่ในตัว
case_run "ordinary source"          accept "src/main.c"                  'int main(void) { return 0; }'
case_run "placeholder password"     accept "config/wifi_example.h"       '#define WIFI_PASSWORD "<your-password>"'
case_run "empty token"              accept "config/cloud_example.h"      'static const char API_TOKEN[] = "";'
case_run "build output"             reject "build/app_combined.hex"      ':00000001FF'
case_run "fetched dependency"       reject "mtb_shared/freertos/x.c"     'int x;'
case_run "object file"              reject "src/main.o"                  'not really an object'
case_run "real-looking password"    reject "config/wifi.h"               '#define WIFI_PASSWORD "hunter2"'
case_run "real-looking token array" reject "config/cloud.h"              'static const char API_TOKEN[] = "tok-0000";'
case_run "private key file"         reject "certs/device.key"            "$hdr EC PRIVATE KEY-----"

echo "$passed passed, $failed failed"
[ "$failed" -eq 0 ]
