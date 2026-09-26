# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux, Advance Innovation Centre (AIC), Burapha University
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
#
# 01_board_knows_itself.py - ถามบอร์ดว่าตัวเองคือใคร มีไฟกี่ดวง ปุ่มกี่ปุ่ม
#
# ย่อและดัดแปลงจาก examples/s01/10_board_knows_itself.py ของหลักสูตร AIoT in Action
# https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer
# (commit a80bbe88, MIT)
#
# ไฟล์นี้สอน: บอร์ดตอบเองได้ว่ามีอะไร ไม่ต้องเปิดคู่มือหา
#             gpio.board_info() คืน dict ก้อนเดียวที่มีชื่อบอร์ด จำนวนไฟ และจำนวนปุ่ม
# ดูที่จอ   : ชื่อบอร์ดตัวสีฟ้า กับบรรทัดบอกจำนวนไฟและปุ่ม
#             รายชื่อไฟทีละดวงอยู่ในลิ้นชัก Console (ปุ่มสีเขียวมุมขวาล่างของจอ)
# กับดัก    : บนบอร์ดจริง ให้แตะการ์ด BENTO Playground เปิดค้างไว้ก่อนรัน
#             ถ้ายืนอยู่หน้าอื่น จออาจดูเงียบทั้งที่โค้ดรันจบแล้ว

import gpio
import lcd
import time
import ui

COL_TEXT = 0xE8EAED      # ข้อความหลัก
COL_ACCENT = 0x4A9EFF    # ค่าที่บอร์ดตอบมา

# ถามครั้งเดียว เก็บไว้ในตัวแปร แล้วอ่านจากตัวแปรตลอดทั้งไฟล์
info = gpio.board_info()

# ล้างจอ แล้วรอให้คอร์ที่ดูแลจอล้างเสร็จก่อนวางของใหม่
ui.screen()
time.sleep_ms(200)

ui.Label("บอร์ดตอบเองว่าเป็นใคร", x=24, y=8, color=COL_TEXT, value=28)
ui.Label(info["name"], x=24, y=64, color=COL_ACCENT, value=24)
ui.Label("ไฟ " + str(info["leds"]) + " ดวง  ปุ่ม " + str(info["buttons"]) + " ปุ่ม",
         x=24, y=112, color=COL_TEXT, value=24)

# สร้างป้ายเสร็จแล้วเคาะ ui.poll() หนึ่งครั้ง ป้ายจะขึ้นจอทันที
ui.poll()

# รายละเอียดทีละดวงยาวเกินจอ จึงส่งลงลิ้นชัก Console แทน
lcd.clear()
lcd.print("ชื่อบอร์ด:", info["name"])
for i, name in enumerate(info["led_names"]):
    lcd.print("gpio.led(" + str(i) + ") =", name)

# print() ธรรมดาไม่ได้ขึ้นบนจอบอร์ด มันขึ้นที่คอนโซลฝั่งคอมพิวเตอร์
print("board_info() =", info)

# ----- ตาคุณ แก้แล้วรันใหม่ -----
# เพิ่มลูปอีกหนึ่งลูป พิมพ์รายชื่อปุ่มจาก info["btn_names"] ลงลิ้นชัก
# แบบเดียวกับที่พิมพ์รายชื่อไฟ แล้วตอบว่าบอร์ดของคุณมีปุ่มชื่ออะไร
