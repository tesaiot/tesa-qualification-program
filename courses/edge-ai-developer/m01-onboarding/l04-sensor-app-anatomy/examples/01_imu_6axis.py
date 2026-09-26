# 01 - IMU BMI270: dashboard 6 แกนบนจอ
# แนวคิด: สร้าง widget ครั้งเดียวก่อนลูป แล้ว "แก้ค่า" อย่างเดียว (ห้ามสร้างใหม่ทุกเฟรม)
# motion() อ่านครบ 6 แกนใต้ bus lock เดียว = snapshot เวลาตรงกัน
import ui
ui.screen()                       # เคลียร์จอ + canvas 792x398
import lcd
import sensors
import time

lcd.clear()
lcd.console('<h2> IMU 6-Axis Dashboard</h2>')
lcd.console(' chip id: 0x%02X' % sensors.bmi270.chip_id())

# ---- สร้าง UI ครั้งเดียว: หัวเรื่อง / ค่าสด / แถบพลังงาน / ปุ่มออก ----
ui.Label("BMI270 - Accelerometer + Gyroscope", x=210, y=10, color=0xFFFFFF)

la = [ui.Label("AX: --", x=60,  y=60 + i * 40, color=0x44CCFF) for i in range(3)]
lg = [ui.Label("GX: --", x=420, y=60 + i * 40, color=0xFFAA44) for i in range(3)]
ui.Label("accel |a| (m/s2 x10) - วางนิ่ง ~98:", x=60, y=195, color=0xAAAAAA)
mag_bar = ui.Bar(x=60, y=225, w=650, min=0, max=300, value=98)

back = ui.Button("< ออก", x=560, y=350, w=130, h=38)
back_id = back.id()
ui.Label("ขยับ/เขย่าบอร์ดแล้วดูค่า", x=60, y=360, color=0x888888)

A = ("AX", "AY", "AZ"); G = ("GX", "GY", "GZ")
n = 0
try:
    while True:
        ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
        acc = (ax, ay, az); gyr = (gx, gy, gz)
        for i in range(3):
            la[i].text("%s: %+6.2f m/s2" % (A[i], acc[i]))
            lg[i].text("%s: %+7.1f dps" % (G[i], gyr[i]))
        mag = (ax * ax + ay * ay + az * az) ** 0.5
        mag_bar.value(int(mag * 10))           # วางนิ่ง ~9.8 m/s2 = 98

        n += 1
        if n % 20 == 0:                        # log ลง console แบบเว้นระยะ
            lcd.console(' |a| = %.2f m/s2' % mag)

        for ev in ui.poll():                   # poll ครั้งเดียวต่อรอบ
            if ev.get('handle') == back_id:
                raise KeyboardInterrupt
        time.sleep_ms(100)                     # 10 Hz - ลื่นและปลอดภัยต่อ IPC
except KeyboardInterrupt:
    lcd.console('<span class=ok> จบการทำงาน</span>')
    print("stopped after", n, "samples")

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
