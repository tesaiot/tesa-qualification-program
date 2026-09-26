# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
#
# ตัวอย่างในแม่แบบ: โปรแกรมสมบูรณ์ที่รันได้ทันที แทนที่ด้วยตัวอย่างของบทเรียนคุณ
# รันได้ใน BENTO Emulator บนบอร์ด หรือใน Python 3 ทั่วไป
#
# ท่าที่ 1: กำหนดค่าที่ผู้เรียนจะลองเปลี่ยน
# ท่าที่ 2: วนนับถอยหลังทีละหนึ่ง
# ท่าที่ 3: พักระหว่างรอบ แล้วบอกว่าจบ
import time

COUNT_FROM = 3   # ลองเปลี่ยนเป็น 5 แล้วทายก่อนรันว่าจะเห็นอะไร
DELAY_S = 1      # เวลาพักระหว่างตัวเลข หน่วยวินาที

for n in range(COUNT_FROM, 0, -1):
    print(n)
    time.sleep(DELAY_S)

print("go")
