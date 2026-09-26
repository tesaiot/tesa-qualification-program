#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
#
# solution/pre-commit.sh — เฉลยของ practice/pre-commit.sh
#
# ติดตั้งในโปรเจกต์ของคุณ:  cp pre-commit.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
# ตรวจงาน:                  bash ../examples/test_hook.sh pre-commit.sh
#
# hook นี้ต้องทำสี่อย่าง (มีช่องให้เติม 4 จุด มองหา TODO)
#   1. หารายชื่อไฟล์ที่ถูก stage (เพิ่ม คัดลอก หรือแก้)
#   2. ปฏิเสธไฟล์ในโฟลเดอร์ build/ build-*/ mtb_shared/ และไฟล์ .o
#   3. ปฏิเสธบรรทัดที่เพิ่มใหม่ซึ่งกำหนดค่าจริงให้ชื่อที่ดูเป็นความลับ (PASSWORD, SECRET, TOKEN, API_KEY ...)
#      แต่ยอมค่าตัวแทนที่ขึ้นต้นด้วย < เช่น "<your-password>" และค่าว่าง ""
#   4. ปฏิเสธบรรทัดหัวของไฟล์กุญแจส่วนตัว (BEGIN ... PRIVATE KEY)
#
# hook ไม่ใช่กำแพงสุดท้าย คนข้ามได้ด้วย git commit --no-verify มันคือเข็มขัดนิรภัย ไม่ใช่ห้องนิรภัย

fail=0

# ACM = Added, Copied, Modified ไฟล์ที่ถูกลบไม่ต้องตรวจ ใช้ได้แม้ใน commit แรกที่ยังไม่มี HEAD
staged="$(git diff --cached --name-only --diff-filter=ACM)"

# รูปแบบเดียวกับ .gitignore ของ SDK: build/, build-*/, mtb_shared/, *.o
# .gitignore กันได้แค่ไฟล์ที่ยังไม่เคยถูก track และคนบังคับ add ได้ด้วย git add -f hook จึงตรวจซ้ำอีกชั้น
while IFS= read -r f; do
    [ -z "$f" ] && continue
    case "$f" in
        build/*|build-*/*|*/build/*|mtb_shared/*|*.o)
            echo "blocked: $f is a build output or fetched dependency"
            fail=1
            ;;
    esac
done <<< "$staged"

# บรรทัดที่เพิ่มใหม่ใน commit นี้ (ให้มาแล้ว) บรรทัดหัวของ diff ที่ขึ้นต้นด้วย +++ ถูกตัดออก
added="$(git diff --cached -U0 --no-color | grep '^+' | grep -v '^+++' || true)"

# "[^"<] หมายถึงค่าในเครื่องหมายคำพูดที่ไม่ว่างและไม่ขึ้นต้นด้วย < ค่าตัวแทนแบบ "<your-password>" จึงผ่าน
secret_re='(PASS(WORD)?|SECRET|TOKEN|API_KEY)[A-Za-z0-9_]*(\[\])?[[:space:]]*=?[[:space:]]*"[^"<]'
hits="$(printf '%s\n' "$added" | grep -iE "$secret_re" || true)"
if [ -n "$hits" ]; then
    printf '%s\n' "$hits"
    echo "blocked: looks like a real secret"
    fail=1
fi

# ไม่พิมพ์บรรทัดนั้นออกมา เพราะ log ของ hook ก็อาจถูกคัดลอกไปแปะที่อื่นได้
if printf '%s\n' "$added" | grep -qE 'BEGIN ([A-Z]+ )?PRIVATE KEY'; then
    echo "blocked: private key"
    fail=1
fi

if [ "$fail" -ne 0 ]; then
    echo "pre-commit: commit refused. Remove the files or lines above, or use a <placeholder>."
fi
exit "$fail"
