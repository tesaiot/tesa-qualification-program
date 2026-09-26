# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux, Advance Innovation Centre (AIC), Burapha University
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
#
# solution/tilt_alarm.py - เฉลยของ practice/tilt_alarm.py
#
# โครงดัดแปลงจาก examples/s01/12_every_sense_at_once.py และ examples/s03/02_led_blink.py
# ของหลักสูตร AIoT in Action (MIT)

import gpio
import sensors
import time
import ui

LIMIT = 8.0
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
        # เติม 1: ขอค่าทั้งก้อนครั้งเดียวต่อรอบ บนบอร์ดจริงบรรทัดนี้โยน OSError ได้
        # ตอนเพิ่งเปิดเครื่อง จึงอยู่ใน try (อีมูเลเตอร์ไม่โยน แต่เราเขียนเผื่อบอร์ดเสมอ)
        s = sensors.snapshot()
    except OSError:
        time.sleep_ms(TICK_MS)
        continue

    # เติม 2: คีย์มีเท่าที่บอร์ดมีให้ ถามด้วย in ก่อนอ่าน ไม่งั้นได้ KeyError
    if "bmi270" in s:
        az = s["bmi270"]["az"]
        az_lbl.text("az  " + str(round(az, 2)))
        if az < LIMIT:
            # เติม 3: ไฟกับป้ายต้องเล่าเรื่องเดียวกันเสมอ
            led.on()
            state.text("เอียง")
            state.color(COL_WARN)
        else:
            # เติม 4: ฝั่งตรงข้ามต้องสั่งดับให้ชัด ไม่ปล่อยไฟค้างจากรอบก่อน
            led.off()
            state.text("วางราบ")
            state.color(COL_OK)

    ui.poll()
    time.sleep_ms(TICK_MS)

led.off()
state.text("จบแล้ว ไฟดับ")
ui.poll()
