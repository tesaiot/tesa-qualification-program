# s02_anatomy_sensor.py - แกะโครงแอปเซนเซอร์แล้ว remix เอง (ฉบับฝึกเติมโค้ด)
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) เติมช่องว่าง (pass) ทั้ง 4 จุดตามคำใบ้ในคอมเมนต์ให้ครบ
#          3) กด "Program to Device" แล้วเอียงบอร์ดช้าๆ ทั้งสองแกน
#          4) ดูเข็ม Arc สองตัวขยับ มุมเด่นขึ้น Seg7 และป้ายสถานะ LEVEL/TILTED เปลี่ยนสี
#
# ชุดบทเรียนนี้เราไม่เขียนของใหม่จากศูนย์ แต่ "กลับด้าน" — เอาแอปเซนเซอร์ที่ทำงานได้แล้ว
# (01_imu_6axis / 02_imu_tilt_fusion / 04_radar_presence) มาแกะดูโครงร่วมของมัน
# แล้ว remix เป็นของเราเอง โครงร่วมที่โปรแกรม MicroPython เกือบทุกตัวใช้คือสี่จังหวะ:
#   import  ->  สร้าง widget ครั้งเดียว  ->  ลูป (อ่าน+ประมวลผล+วาดจอ)  ->  ui.poll รับปุ่ม
# ไฟล์นี้ผสมสามตัวอย่าง: อ่าน IMU เหมือน 01, แปลงเป็นมุมเอียงด้วย dsp.tilt เหมือน 02,
# แล้วเปลี่ยนสีป้ายสถานะเฉพาะตอนสถานะเปลี่ยน (event-driven) เหมือน 04

# ----- จังหวะ 1: import -----
import ui
ui.screen()                       # เคลียร์จอ + เตรียม canvas 792x398
import lcd
import sensors
import dsp
import time

# ธีมสี (เก็บไว้ที่เดียว จะปรับ remix ให้เป็นสีของเราเองก็แก้ตรงนี้)
CYAN  = 0x44CCFF   # แกน pitch
AMBER = 0xFFAA44   # แกน roll
GREEN = 0x50D890   # LEVEL (วางราบ) + มุมเด่น
RED   = 0xE85B5B   # TILTED (เอียงเกินเกณฑ์)
GREY  = 0x888888   # ข้อความรอง

DEAD = 2.0         # องศา - deadzone กันเข็มสั่นตอนวางราบ
TILT_LIMIT = 20    # องศา - เกินนี้ถือว่า "เอียง" (ลอง remix เปลี่ยนตัวเลขนี้ดู)

lcd.clear()
lcd.console('<h2> Tilt Monitor - remix ของเรา</h2>')
lcd.console(' chip id: 0x%02X' % sensors.bmi270.chip_id())

# ----- จังหวะ 2: สร้าง widget ครั้งเดียวก่อนเข้าลูป -----
# กฎเหล็กของโครงร่วม: สร้าง widget "นอกลูป" ในลูปแค่แก้ค่า/ข้อความ
# ถ้าสร้างใหม่ทุกวนรอบ จอจะกระพริบและกินหน่วยความจำจนค้าง
ui.Label("Pitch", x=170, y=24, color=CYAN)
arc_p = ui.Arc(x=100, y=54, min=-90, max=90, value=0)
ui.Label("Roll", x=560, y=24, color=AMBER)
arc_r = ui.Arc(x=490, y=54, min=-90, max=90, value=0)

seg = ui.Seg7("0", x=330, y=104, color=GREEN)          # มุมเด่น (องศา)
ui.Label("องศาที่เอียงมากสุด", x=330, y=168, color=GREY)

panel = ui.Panel(x=250, y=205, w=290, h=64, color=0x115511)
state = ui.Label("LEVEL", x=350, y=228, color=0xFFFFFF)

back = ui.Button("< ออก", x=640, y=350, w=130, h=38)
back_id = back.id()
ui.Label("เอียงบอร์ดช้าๆ ทั้งสองแกน", x=60, y=360, color=GREY)

# ----- จังหวะ 3: ลูป -----
last = (999, 999)        # กันวาดจอซ้ำ: อัปเดตเฉพาะตอนค่าเปลี่ยนจริง
was_tilted = None        # สถานะก่อนหน้า (None = ยังไม่รู้) สำหรับ event-driven
try:
    while True:
        # เติม: อ่านค่า 6 แกนจาก IMU ใต้ bus lock เดียว (snapshot เวลาตรงกัน)
        #       ->  ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
        ax = ay = az = gx = gy = gz = 0
        pass

        # เติม: แปลง accel 3 แกนเป็นมุมเอียง dsp.tilt คืน (roll, pitch) หน่วยองศา
        #       ->  roll, pitch = dsp.tilt(ax, ay, az)
        roll, pitch = 0.0, 0.0
        pass

        p = 0 if abs(pitch) < DEAD else int(pitch)
        r = 0 if abs(roll) < DEAD else int(roll)
        if (p, r) != last:                     # อัปเดตเข็มเฉพาะตอนค่าเปลี่ยน
            arc_p.value(p)
            arc_r.value(r)
            ang = p if abs(p) >= abs(r) else r  # มุมที่เอียงมากสุด
            # เติม: โชว์มุมเด่นบน Seg7  ->  seg.text("%d" % ang)
            pass
            last = (p, r)

            # event-driven (ยกมาจาก 04): เปลี่ยนสีป้าย "เฉพาะตอนข้ามเกณฑ์"
            tilted = abs(ang) >= TILT_LIMIT
            if tilted != was_tilted:
                if tilted:
                    panel.color(0x881111)
                    state.text("TILTED")
                    seg.color(RED)
                else:
                    panel.color(0x115511)
                    state.text("LEVEL")
                    seg.color(GREEN)
                was_tilted = tilted

        # ----- จังหวะ 4: ui.poll รับปุ่ม (poll ครั้งเดียวต่อรอบ) -----
        for ev in ui.poll():
            if ev.get('handle') == back_id:
                # เติม: ออกจากลูปตอนกดปุ่ม back  ->  raise KeyboardInterrupt
                pass
        time.sleep_ms(100)                     # 10 Hz - ลื่นและปลอดภัยต่อ IPC
except KeyboardInterrupt:
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
