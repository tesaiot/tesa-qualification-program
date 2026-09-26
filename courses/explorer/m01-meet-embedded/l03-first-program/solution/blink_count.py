# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux, Advance Innovation Centre (AIC), Burapha University
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
#
# solution/blink_count.py - เฉลยของ practice/blink_count.py
#
# โครงดัดแปลงจาก examples/s03/02_led_blink.py ของหลักสูตร AIoT in Action (MIT)
#
# เปิดไฟล์นี้หลังจากลองเองแล้วอย่างน้อย 15 นาที
# ถ้าของคุณต่างจากเฉลยแต่หลอดกะพริบครบและเลขบนจอตรง ก็ถือว่าถูก

import gpio
import time
import ui

TIMES = 5
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
    # on() สั่งค่าตรง ๆ อ่านบรรทัดเดียวก็รู้ว่าไฟจะติด
    led.on()
    time.sleep_ms(ON_MS)

    led.off()
    # นับตอนดับ เพราะกะพริบหนึ่งครั้งคือ "ติดแล้วดับ" ครบหนึ่งวง
    count = count + 1
    # Seg7 รับข้อความ ส่งตัวเลขตรง ๆ ไม่ได้ จึงต้องแปลงด้วย str()
    seg.text(str(count))
    ui.poll()
    time.sleep_ms(OFF_MS)

# ปิดท้ายด้วย off() อีกครั้ง โปรแกรมที่จบแล้วต้องบอกได้แน่ว่าไฟดับ
led.off()
print("กะพริบไป", count, "ครั้ง")
