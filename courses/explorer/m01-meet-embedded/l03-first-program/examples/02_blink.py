# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux, Advance Innovation Centre (AIC), Burapha University
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
#
# 02_blink.py - ไฟกะพริบเป็นจังหวะ พร้อมตัวนับรอบบนจอ
#
# ย่อและดัดแปลงจาก examples/s03/02_led_blink.py ของหลักสูตร AIoT in Action
# https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer
# (commit a80bbe88, MIT)
#
# ไฟล์นี้สอน: กะพริบหนึ่งรอบคือ สั่งติด รอ สั่งดับ รอ เวลาที่รอคือจังหวะ
# ดูที่จอ   : ป้ายบอก "ติด" หรือ "ดับ" ตรงกับหลอดจริง และเลขนับรอบเดินขึ้นทีละหนึ่ง
#             ใน BENTO Emulator ให้กดปุ่ม HW เพื่อเปิดแผงฮาร์ดแวร์จำลอง แล้วดูหลอดบนแผงนั้น
# กับดัก    : โปรแกรมที่จบแล้วต้องบอกได้ว่าไฟอยู่สถานะไหน จึงปิดท้ายด้วย off() เสมอ

import gpio
import time
import ui

ROUNDS = 6        # กะพริบกี่รอบ
ON_MS = 250       # ติดค้างนานเท่าไร (มิลลิวินาที)
OFF_MS = 250      # ดับค้างนานเท่าไร

COL_TEXT, COL_DIM = 0xE8EAED, 0x9AA3AF
COL_OK, COL_WARN = 0x30A46C, 0xF5A623

# เลือกดวงจากชื่อที่บอร์ดรายงาน ไม่ใช่จากเลขที่จำมา
# ถ้าบอร์ดมีดวงที่ชื่อขึ้นต้นด้วย RGB_ ใช้ดวงนั้น ไม่มีก็ใช้ดวงแรก
LED = 0
for i, name in enumerate(gpio.board_info()["led_names"]):
    if name.startswith("RGB_"):
        LED = i
        break

led = gpio.led(LED)
led.off()                  # เริ่มจากสถานะที่รู้แน่ว่าคืออะไร

ui.screen()
time.sleep_ms(200)

ui.Label("ไฟกะพริบ", x=24, y=8, color=COL_TEXT, value=28)
state = ui.Label("ดับ", x=24, y=64, color=COL_DIM, value=28)
seg = ui.Seg7(text="0", x=200, y=56, w=140, h=56, color=COL_OK)
ui.Label("หลอดที่ใช้: " + led.name(), x=24, y=144, color=COL_DIM, value=20)
ui.poll()

rounds = 0
for k in range(ROUNDS):
    led.on()
    state.text("ติด")
    state.color(COL_WARN)
    ui.poll()
    time.sleep_ms(ON_MS)

    led.off()
    state.text("ดับ")
    state.color(COL_DIM)
    rounds = rounds + 1
    seg.text(str(rounds))      # Seg7 รับข้อความ ไม่ใช่ตัวเลข จึงต้อง str()
    ui.poll()
    time.sleep_ms(OFF_MS)

led.off()
state.text("จบแล้ว ไฟดับ")
ui.poll()

# ----- ตาคุณ แก้แล้วรันใหม่ -----
# ทำนายก่อนรัน: ถ้าตั้ง ON_MS = 50 และ OFF_MS = 950 ไฟจะดูเป็นอย่างไร
# แล้วรันจริงเทียบกับที่ทำนายไว้
