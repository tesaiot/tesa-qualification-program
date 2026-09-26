# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
#
# เฉลยในแม่แบบ: คอมเมนต์ในเฉลยอธิบายว่า "ทำไม" ไม่ใช่แค่ "ทำอะไร"
import time

COUNT_FROM = 3
DELAY_S = 1

# stop เป็น 0 เพราะ range หยุดก่อนถึงค่า stop เสมอ ตัวสุดท้ายที่พิมพ์จึงเป็น 1
# step เป็น -1 เพราะเรานับลง ถ้าลืมใส่ step จะไม่มีรอบไหนทำงานเลย เพราะ 3 มากกว่า 0 ตั้งแต่ต้น
for n in range(COUNT_FROM, 0, -1):
    print(n)
    time.sleep(DELAY_S)

print("go")
