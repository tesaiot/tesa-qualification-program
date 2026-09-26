# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux, Advance Innovation Centre (AIC), Burapha University
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
#
# 01_hello_screen.py - ข้อความเดียว ไปได้สามที่
#
# ย่อและดัดแปลงจาก examples/s01/01_first_line.py ของหลักสูตร AIoT in Action
# https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer
# (commit a80bbe88, MIT)
#
# ไฟล์นี้สอน: ป้ายบนจอ (ui.Label) ลิ้นชัก Console (lcd.print) และคอนโซลฝั่งคอม (print)
#             เป็นสามที่ คนละที่กัน
# ดูที่จอ   : หัวเรื่องหนึ่งบรรทัด กับป้ายสีฟ้าที่เปลี่ยนข้อความหลังผ่านไปหนึ่งวินาที
# กับดัก    : สร้างป้ายแล้วลืม ui.poll() ป้ายจะขึ้นช้าไปราวสองวินาที
#             นานพอให้เราเข้าใจผิดว่าโค้ดพัง

import lcd
import time
import ui

COL_TEXT = 0xE8EAED      # ข้อความหลัก
COL_ACCENT = 0x4A9EFF    # ค่าที่กำลังเปลี่ยน

ui.screen()
time.sleep_ms(200)

# ท่าที่ 1 - ป้ายบนจอ เห็นได้ทันทีโดยไม่ต้องกดอะไร
ui.Label("สวัสดี ระบบสมองกลฝังตัว", x=24, y=8, color=COL_TEXT, value=28)
say = ui.Label("กำลังเขียนลงลิ้นชัก...", x=24, y=64, color=COL_ACCENT, value=24)
ui.poll()

# ท่าที่ 2 - ลิ้นชัก Console ล้างก่อน จะได้รู้ว่าบรรทัดไหนมาจากรอบนี้
lcd.clear()
lcd.print("สวัสดี บอร์ด PSoC Edge")
lcd.print("หนึ่งบวกหนึ่งได้", 1 + 1)     # ส่งตัวเลขได้เลย ไม่ต้องแปลงก่อน

# ท่าที่ 3 - print() ขึ้นที่คอนโซลฝั่งคอม ไม่ได้ขึ้นบนจอบอร์ด
print("บรรทัดนี้อยู่บนคอม")

time.sleep_ms(1000)

# แก้ข้อความบนป้ายเดิม ไม่ใช่วางป้ายใหม่ทับ
say.text("เขียนแล้ว เปิดลิ้นชัก Console ดูได้")
ui.poll()

# ----- ตาคุณ แก้แล้วรันใหม่ -----
# ใส่ชื่อของคุณลงไปทั้งสามที่ คือป้ายบนจอ ลิ้นชัก และ print()
# แล้วตอบว่าต้องมองตรงไหนบ้าง ถึงจะเห็นชื่อครบทั้งสามครั้ง
