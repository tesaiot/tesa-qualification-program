#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
#
# practice/pre-commit.sh — ฝึกเติม: git hook ที่ปฏิเสธ commit ซึ่งมีไฟล์ build หรือข้อมูลลับ
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
# ก่อนเติม test จะล้มสี่กรณี ลองเองก่อนอย่างน้อย 15 นาที แล้วค่อยเปิด solution/pre-commit.sh
#
# hook ไม่ใช่กำแพงสุดท้าย คนข้ามได้ด้วย git commit --no-verify มันคือเข็มขัดนิรภัย ไม่ใช่ห้องนิรภัย

fail=0

# TODO 1: ใส่รายชื่อไฟล์ที่ถูก stage ลงในตัวแปร staged (หนึ่งไฟล์ต่อบรรทัด)
#         คำใบ้: git diff --cached --name-only --diff-filter=ACM
staged=""

# TODO 2: วนดูทุกไฟล์ใน staged ถ้า path ขึ้นต้นด้วย build/ หรือ build-xxx/ หรือ mtb_shared/ หรือลงท้ายด้วย .o
#         ให้พิมพ์ "blocked: <path> is a build output or fetched dependency" แล้วตั้ง fail=1
while IFS= read -r f; do
    [ -z "$f" ] && continue
    : # เติมเงื่อนไขตรงนี้
done <<< "$staged"

# บรรทัดที่เพิ่มใหม่ใน commit นี้ (ให้มาแล้ว) บรรทัดหัวของ diff ที่ขึ้นต้นด้วย +++ ถูกตัดออก
added="$(git diff --cached -U0 --no-color | grep '^+' | grep -v '^+++' || true)"

# TODO 3: ถ้า added มีบรรทัดที่ตรงกับรูปแบบข้างล่าง (ไม่สนตัวพิมพ์เล็กใหญ่) ให้พิมพ์บรรทัดนั้น
#         พร้อมข้อความ "blocked: looks like a real secret" แล้วตั้ง fail=1
#         รูปแบบ (ERE): (PASS(WORD)?|SECRET|TOKEN|API_KEY)[A-Za-z0-9_]*(\[\])?[[:space:]]*=?[[:space:]]*"[^"<]
#         คำใบ้: grep -inE

# TODO 4: ถ้า added มีบรรทัดที่ตรงกับ 'BEGIN ([A-Z]+ )?PRIVATE KEY' ให้พิมพ์ "blocked: private key" แล้วตั้ง fail=1

if [ "$fail" -ne 0 ]; then
    echo "pre-commit: commit refused. Remove the files or lines above, or use a <placeholder>."
fi
exit "$fail"
