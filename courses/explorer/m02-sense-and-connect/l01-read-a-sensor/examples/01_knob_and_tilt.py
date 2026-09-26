# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux, Advance Innovation Centre (AIC), Burapha University
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
#
# 01_knob_and_tilt.py - หมุนลูกบิด เอียงบอร์ด แล้วดูตัวเลขบนจอขยับตาม
#
# ย่อและดัดแปลงจาก examples/s01/12_every_sense_at_once.py ของหลักสูตร AIoT in Action
# https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer
# (commit a80bbe88, MIT)
#
# ไฟล์นี้สอน: sensors.snapshot() คืน dict ก้อนเดียวที่มีค่าเซนเซอร์หลายตัวจากเวลาเดียวกัน
#             "pot" คือลูกบิดหมุน (percent 0-100) "bmi270" คือเซนเซอร์ความเคลื่อนไหว
#             az คือความเร่งแกน z หน่วย m/s^2 วางราบราว 9.8 เอียงแล้วค่าลดลง
# ดูที่จอ   : วงแหวนกวาดตามลูกบิด ตัวเลข az เปลี่ยนเมื่อเอียง และตัวนับรอบเดินขึ้น
#             ใน BENTO Emulator ให้กดปุ่ม HW แล้วหมุนลูกบิด POTEN หรือลากแผ่นเอียงบนแผงจำลอง
# กับดัก    : หลังเปิดเครื่องใหม่ ๆ บอร์ดอาจยังไม่พร้อมตอบเรื่องเซนเซอร์อยู่ครู่หนึ่ง
#             snapshot() จะโยน OSError ออกมา ไม่ได้แปลว่าโค้ดผิด จึงต้องดักไว้
#             และคีย์ในก้อนมีเท่าที่บอร์ดมีให้ ต้องถามด้วย in ก่อนอ่านเสมอ

import sensors
import time
import ui

RUN_MS = 20000     # เฝ้าดูนานเท่าไร
TICK_MS = 200      # ถามซ้ำทุกกี่มิลลิวินาที

COL_TEXT, COL_DIM = 0xE8EAED, 0x9AA3AF
COL_OK, COL_WARN = 0x30A46C, 0xF5A623

ui.screen()
time.sleep_ms(200)

ui.Label("ลูกบิดกับการเอียง", x=24, y=8, color=COL_TEXT, value=28)

# Arc ไม่รับ color= ตอนสร้าง ต้องเรียก .color() หลังสร้าง
arc = ui.Arc(x=24, y=64, w=120, h=120, min=0, max=100, value=0)
arc.color(COL_OK)
pot_lbl = ui.Label("pot  รอค่า", x=24, y=200, color=COL_TEXT, value=24)
az_lbl = ui.Label("az  รอค่า", x=300, y=100, color=COL_TEXT, value=24)
state = ui.Label("กำลังขอค่าชุดแรก", x=24, y=260, color=COL_DIM, value=20)
ui.poll()

t0 = time.ticks_ms()
rounds = 0

while time.ticks_diff(time.ticks_ms(), t0) < RUN_MS:
    rounds = rounds + 1
    try:
        s = sensors.snapshot()
    except OSError:
        state.text("บอร์ดยังไม่พร้อม รอบที่ " + str(rounds))
        ui.poll()
        time.sleep_ms(TICK_MS)
        continue

    if "pot" in s:
        # percent เป็นทศนิยม แต่ Arc รับจำนวนเต็ม จึงแปลงด้วย int()
        pct = int(s["pot"]["percent"])
        arc.value(pct)
        pot_lbl.text("pot  " + str(pct) + " %")

    if "bmi270" in s:
        az = s["bmi270"]["az"]
        az_lbl.text("az  " + str(round(az, 2)))
        # วางราบ az ราว 9.8 เอียงมากขึ้นค่าลดลง
        az_lbl.color(COL_OK if az > 8.0 else COL_WARN)

    state.text("อ่านไปแล้ว " + str(rounds) + " รอบ")
    ui.poll()
    time.sleep_ms(TICK_MS)

state.text("จบแล้ว ค่าสุดท้ายค้างไว้ให้อ่าน")
ui.poll()

# ----- ตาคุณ แก้แล้วรันใหม่ -----
# ทำนายก่อนรัน: ถ้าคว่ำบอร์ดลง ค่า az จะเป็นบวกหรือลบ
# แล้วลองจริง (หรือลากแผ่นเอียงในอีมูเลเตอร์จนสุด) เทียบกับที่ทำนาย
