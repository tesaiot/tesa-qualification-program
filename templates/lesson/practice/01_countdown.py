# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
#
# แบบฝึกในแม่แบบ: ชื่อไฟล์เดียวกับ solution/01_countdown.py เพื่อให้จับคู่กันได้
# บทแรกของโมดูลเว้นว่างน้อย บทหลัง ๆ เว้นมากขึ้น จนบทสุดท้ายเป็นไฟล์เกือบเปล่า
#
# โจทย์: นับถอยหลังจาก COUNT_FROM ถึง 1 ทีละหนึ่ง พักตัวละ DELAY_S วินาที แล้วพิมพ์ "go"
import time

COUNT_FROM = 3
DELAY_S = 1

# ----- เติมส่วนนี้เอง (งานของคุณ) -----
# ใบ้: range(start, stop, step) หยุดก่อนถึง stop และ step ติดลบได้
for n in range(____, ____, ____):
    print(n)
    time.sleep(DELAY_S)
# ----- จบส่วนของคุณ -----

print("go")
