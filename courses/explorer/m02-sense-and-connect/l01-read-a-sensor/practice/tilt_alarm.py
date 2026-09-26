# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux, Advance Innovation Centre (AIC), Burapha University
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
#
# practice/tilt_alarm.py - ฝึกเติม: ไฟเตือนเมื่อบอร์ดเอียง
#
# โครงดัดแปลงจาก examples/s01/12_every_sense_at_once.py และ examples/s03/02_led_blink.py
# ของหลักสูตร AIoT in Action (MIT)
#
# โจทย์   : ถามเซนเซอร์ทุก 200 ms นาน 20 วินาที
#           ถ้า az ต่ำกว่า LIMIT (บอร์ดเอียง) ให้หลอดติดและป้ายเขียนว่า "เอียง"
#           ถ้าไม่ต่ำกว่า ให้หลอดดับและป้ายเขียนว่า "วางราบ"
# มีช่องให้เติม 4 จุด มากกว่าบทที่แล้ว เพราะคุณเคยเห็นทุกคำสั่งที่ต้องใช้มาแล้ว
# ลองเองก่อนอย่างน้อย 15 นาที แล้วค่อยเปิด solution/tilt_alarm.py เทียบ

import gpio
import sensors
import time
import ui

LIMIT = 8.0        # az ต่ำกว่านี้ถือว่าเอียง (วางราบราว 9.8)
RUN_MS = 20000
TICK_MS = 200

COL_TEXT, COL_OK, COL_WARN = 0xE8EAED, 0x30A46C, 0xF5A623

led = gpio.led(0)
led.off()

ui.screen()
time.sleep_ms(200)
ui.Label("ไฟเตือนเมื่อเอียง", x=24, y=8, color=COL_TEXT, value=28)
state = ui.Label("รอค่าแรก", x=24, y=64, color=COL_TEXT, value=28)
az_lbl = ui.Label("az  รอค่า", x=24, y=120, color=COL_TEXT, value=24)
ui.poll()

t0 = time.ticks_ms()
while time.ticks_diff(time.ticks_ms(), t0) < RUN_MS:
    try:
        # เติม 1: ขอค่าเซนเซอร์ทั้งก้อนมาเก็บในตัวแปร s
        pass
    except OSError:
        time.sleep_ms(TICK_MS)
        continue

    # เติม 2: เปลี่ยน False ให้เป็นเงื่อนไข "มีคีย์ bmi270 อยู่ใน s"
    if False:
        az = s["bmi270"]["az"]
        az_lbl.text("az  " + str(round(az, 2)))
        if az < LIMIT:
            # เติม 3: สั่งหลอดติด แล้วเขียน "เอียง" ลงป้าย state พร้อมเปลี่ยนเป็น COL_WARN
            pass
        else:
            # เติม 4: สั่งหลอดดับ แล้วเขียน "วางราบ" ลงป้าย state พร้อมเปลี่ยนเป็น COL_OK
            pass

    ui.poll()
    time.sleep_ms(TICK_MS)

led.off()
state.text("จบแล้ว ไฟดับ")
ui.poll()
