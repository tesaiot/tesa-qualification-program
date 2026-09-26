# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux, Advance Innovation Centre (AIC), Burapha University
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
#
# practice/blink_count.py - ฝึกเติม: กะพริบให้ครบจำนวนที่ตั้ง แล้วนับรอบบนจอ
#
# โครงดัดแปลงจาก examples/s03/02_led_blink.py ของหลักสูตร AIoT in Action (MIT)
#
# โจทย์   : ทำให้หลอดกะพริบ TIMES ครั้ง แต่ละครั้งติด 300 ms ดับ 300 ms
#           ทุกครั้งที่ดับ ตัวเลขบนจอต้องเพิ่มขึ้นหนึ่ง และจบด้วยหลอดดับ
# มีช่องให้เติม 2 จุด มองหาบรรทัด "# เติม:" แล้วแทน pass ด้วยโค้ดของคุณ
# ลองเองก่อนอย่างน้อย 15 นาที แล้วค่อยเปิด solution/blink_count.py เทียบ

import gpio
import time
import ui

TIMES = 5          # กะพริบกี่ครั้ง ลองเปลี่ยนเป็นเลขอื่นหลังทำเสร็จ
ON_MS = 300
OFF_MS = 300

COL_TEXT, COL_OK = 0xE8EAED, 0x30A46C

led = gpio.led(0)
led.off()

ui.screen()
time.sleep_ms(200)
ui.Label("นับการกะพริบ", x=24, y=8, color=COL_TEXT, value=28)
seg = ui.Seg7(text="0", x=24, y=64, w=140, h=56, color=COL_OK)
ui.poll()

count = 0
for k in range(TIMES):
    # เติม: สั่งหลอดให้ติด (ดูตัวอย่าง examples/02_blink.py)
    pass
    time.sleep_ms(ON_MS)

    led.off()
    # เติม: เพิ่ม count ขึ้นหนึ่ง แล้วเขียนเลขใหม่ลง seg (อย่าลืม str())
    pass
    ui.poll()
    time.sleep_ms(OFF_MS)

led.off()
print("กะพริบไป", count, "ครั้ง")
