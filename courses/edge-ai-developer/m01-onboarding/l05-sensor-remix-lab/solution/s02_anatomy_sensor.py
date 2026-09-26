# s02_anatomy_sensor.py - แกะโครงแอปเซนเซอร์แล้ว remix เอง (เฉลย)
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) กด "Program to Device"
#          3) เอียงบอร์ดช้าๆ ทั้งสองแกน ดูเข็ม Arc คู่ + มุมเด่น Seg7 + ป้าย LEVEL/TILTED
#
# เฉลยนี้ไม่ได้มีไว้ลอกวาง สิ่งที่นับคือการอธิบายด้วยคำพูดของคุณเอง
# อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์ใหม่ด้วยมือ — พอพิมพ์เองจะจับ "โครงร่วม" ได้ติดมือ
# ทั้งไฟล์ก็แค่สี่จังหวะเดิมที่เจอซ้ำทั้งคอร์ส:
#   import  ->  สร้าง widget ครั้งเดียว  ->  ลูป(อ่าน+ประมวลผล+วาดจอ)  ->  ui.poll
# และมันคือการ remix ของสามตัวอย่าง: โครงอ่าน IMU จาก 01, dsp.tilt จาก 02,
# และลูกเล่น "เปลี่ยนจอเฉพาะตอนสถานะเปลี่ยน" (event-driven) จาก 04

# ----- จังหวะ 1: import -----
import ui
ui.screen()                       # เคลียร์จอ + เตรียม canvas 792x398
import lcd
import sensors
import dsp
import time

# ธีมสี เก็บรวมไว้ที่เดียวเพื่อให้ remix ง่าย อยากเปลี่ยนหน้าตาก็แก้ตรงนี้จุดเดียว
CYAN  = 0x44CCFF   # แกน pitch
AMBER = 0xFFAA44   # แกน roll
GREEN = 0x50D890   # LEVEL (วางราบ) + มุมเด่น
RED   = 0xE85B5B   # TILTED (เอียงเกินเกณฑ์)
GREY  = 0x888888   # ข้อความรอง

DEAD = 2.0         # องศา - deadzone กันเข็มสั่นตอนวางบอร์ดราบนิ่งๆ
TILT_LIMIT = 20    # องศา - เกินนี้ถือว่า "เอียง" ปรับตัวเลขนี้แล้วสังเกตว่าป้ายไวขึ้น/ช้าลง

lcd.clear()
lcd.console('<h2> Tilt Monitor - remix ของเรา</h2>')
lcd.console(' chip id: 0x%02X' % sensors.bmi270.chip_id())

# ----- จังหวะ 2: สร้าง widget ครั้งเดียวก่อนเข้าลูป -----
# หัวใจของโครงร่วม: widget ทุกตัวเกิด "ก่อน" ลูป ในลูปเราแค่เปลี่ยนค่ากับข้อความของมัน
# ลองคิดว่า widget คือป้ายที่ตอกติดผนังไว้แล้ว เราแค่เดินไปเปลี่ยนตัวเลขบนป้าย ไม่ตอกใหม่
ui.Label("Pitch", x=170, y=24, color=CYAN)
arc_p = ui.Arc(x=100, y=54, min=-90, max=90, value=0)
ui.Label("Roll", x=560, y=24, color=AMBER)
arc_r = ui.Arc(x=490, y=54, min=-90, max=90, value=0)

seg = ui.Seg7("0", x=330, y=104, color=GREEN)          # มุมเด่น (องศา)
ui.Label("องศาที่เอียงมากสุด", x=330, y=168, color=GREY)

panel = ui.Panel(x=250, y=205, w=290, h=64, color=0x115511)
state = ui.Label("LEVEL", x=350, y=228, color=0xFFFFFF)

back = ui.Button("< ออก", x=560, y=350, w=130, h=38)
back_id = back.id()
ui.Label("เอียงบอร์ดช้าๆ ทั้งสองแกน", x=60, y=360, color=GREY)

# ----- จังหวะ 3: ลูป -----
last = (999, 999)        # ค่าที่วาดครั้งก่อน ใช้เทียบเพื่อวาดจอเฉพาะตอนค่าเปลี่ยนจริง
was_tilted = None        # สถานะก่อนหน้า (None = ยังไม่เคยรู้) สำหรับสลับสีป้ายแบบ event-driven
try:
    while True:
        # อ่านครบ 6 แกนในครั้งเดียวใต้ bus lock เดียว = ได้ snapshot ที่เวลาตรงกันทุกแกน
        # (ชุดบทเรียนนี้เราใช้แค่ ax, ay, az แต่ motion() ให้ gyro มาด้วย เผื่อ remix ต่อ)
        ax, ay, az, gx, gy, gz = sensors.bmi270.motion()

        # ยกงานคณิตให้ฝั่ง C ทำ: dsp.tilt แปลง accel 3 แกนเป็นมุมเอียง คืน (roll, pitch) องศา
        roll, pitch = dsp.tilt(ax, ay, az)

        p = 0 if abs(pitch) < DEAD else int(pitch)   # ในเขต deadzone ปัดเป็น 0 เข็มจะได้นิ่ง
        r = 0 if abs(roll) < DEAD else int(roll)
        if (p, r) != last:                     # วาดจอเฉพาะตอนมุมเปลี่ยนจริง ไม่รัดจอทุกเฟรม
            arc_p.value(p)
            arc_r.value(r)
            ang = p if abs(p) >= abs(r) else r  # เลือกแกนที่เอียงมากสุดมาโชว์เป็นตัวเลขเด่น
            seg.text("%d" % ang)
            last = (p, r)

            # event-driven ยกมาจาก 04: เปลี่ยนสี/ข้อความป้าย "เฉพาะตอนข้ามเกณฑ์" ไม่ใช่ทุกเฟรม
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

        # ----- จังหวะ 4: ui.poll รับปุ่ม เรียกครั้งเดียวต่อรอบลูป -----
        for ev in ui.poll():
            if ev.get('handle') == back_id:
                raise KeyboardInterrupt        # กดปุ่ม back = โยนออกไปให้ except เก็บกวาด
        time.sleep_ms(100)                     # 10 Hz - ลื่นตาและปลอดภัยต่อ IPC
except KeyboardInterrupt:
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
