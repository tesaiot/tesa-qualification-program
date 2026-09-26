# s02_anatomy_sensor_full.py - Tilt Monitor remix (ฉบับเต็ม)
# วิธีรัน: เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator (ide.tesaiot.dev)
#          กด "Program to Device" แล้วเอียงบอร์ดช้าๆ ทั้งสองแกน
#
# ฉบับนี้คือเวอร์ชันที่ขัดจนเรียบร้อยของ s02_anatomy_sensor.py — โครงร่วมสี่จังหวะเดิม
# (import -> สร้างครั้งเดียว -> ลูป -> ui.poll) แต่ remix เพิ่มให้ "อ่านสถานะบอร์ดได้ครบ":
#   - เกจ Arc คู่ pitch/roll เหมือน 02
#   - แถบ |a| (ขนาดแรงโน้มถ่วง) เหมือน 01 ไว้ดูว่าบอร์ดกำลังนิ่งหรือถูกเขย่า
#   - ป้ายสถานะ LEVEL/TILTED เปลี่ยนสีแบบ event-driven เหมือน 04
#   - จำ "มุมเอียงมากสุดที่เคยเจอ" (peak) แล้วมีปุ่ม Reset ล้างค่า
# ทั้งหมดยังยืนอยู่บนโครงร่วมเดิม เพิ่มแค่รายละเอียดที่ทำให้อ่านง่ายขึ้น

# ----- จังหวะ 1: import -----
import ui
ui.screen()
import lcd
import sensors
import dsp
import time

# ธีมสี รวมไว้ที่เดียวเพื่อ remix ง่าย
CYAN  = 0x44CCFF   # แกน pitch
AMBER = 0xFFAA44   # แกน roll
GREEN = 0x50D890   # LEVEL + มุมเด่น
RED   = 0xE85B5B   # TILTED
GREY  = 0x888888   # ข้อความรอง
DIM   = 0x6A6A6A

DEAD = 2.0         # องศา - deadzone กันเข็มสั่นตอนวางราบ
TILT_LIMIT = 20    # องศา - เกินนี้ = "เอียง"

lcd.clear()
lcd.console('<h2> Tilt Monitor - remix (ฉบับเต็ม)</h2>')
lcd.console(' chip id: 0x%02X  |  วางบอร์ดราบตอนเริ่ม แล้วค่อยเอียง' % sensors.bmi270.chip_id())

# ----- จังหวะ 2: สร้าง widget ครั้งเดียวก่อนลูป -----
ui.Label("Pitch", x=150, y=18, color=CYAN)
arc_p = ui.Arc(x=80, y=48, min=-90, max=90, value=0)
ui.Label("Roll", x=520, y=18, color=AMBER)
arc_r = ui.Arc(x=450, y=48, min=-90, max=90, value=0)

seg = ui.Seg7("0", x=305, y=96, color=GREEN)               # มุมเด่นปัจจุบัน (องศา)
ui.Label("องศาที่เอียงมากสุดตอนนี้", x=300, y=158, color=GREY)
peak_lbl = ui.Label("peak: 0 deg", x=305, y=182, color=CYAN)  # มุมมากสุดที่เคยเจอ

ui.Label("|a| (m/s2 x10) - วางนิ่ง ~98", x=60, y=214, color=GREY)
mag_bar = ui.Bar(x=60, y=240, w=650, min=0, max=300, value=98)

panel = ui.Panel(x=250, y=278, w=290, h=56, color=0x115511)
state = ui.Label("LEVEL", x=350, y=296, color=0xFFFFFF)

btn_reset = ui.Button("Reset peak", x=60, y=350, w=150, h=38)
back = ui.Button("< ออก", x=560, y=350, w=130, h=38)
reset_id = btn_reset.id()
back_id = back.id()

# ----- จังหวะ 3: ลูป -----
last = (999, 999)
was_tilted = None
peak = 0
n = 0
try:
    while True:
        # อ่านครบ 6 แกนใต้ bus lock เดียว = snapshot เวลาตรงกัน (ใช้ accel ทำ tilt + magnitude)
        ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
        roll, pitch = dsp.tilt(ax, ay, az)

        # แถบ |a| อัปเดตทุกรอบ ดูได้ว่าบอร์ดนิ่ง (~98) หรือถูกเขย่า (พุ่งสูง)
        mag = (ax * ax + ay * ay + az * az) ** 0.5
        mag_bar.value(int(mag * 10))

        p = 0 if abs(pitch) < DEAD else int(pitch)
        r = 0 if abs(roll) < DEAD else int(roll)
        if (p, r) != last:                     # วาดเข็ม/ตัวเลขเฉพาะตอนมุมเปลี่ยนจริง
            arc_p.value(p)
            arc_r.value(r)
            ang = p if abs(p) >= abs(r) else r
            seg.text("%d" % ang)
            last = (p, r)

            if abs(ang) > peak:                # จำมุมมากสุดที่เคยเอียง
                peak = abs(ang)
                peak_lbl.text("peak: %d deg" % peak)

            tilted = abs(ang) >= TILT_LIMIT
            if tilted != was_tilted:           # เปลี่ยนสีป้ายเฉพาะตอนข้ามเกณฑ์ (event-driven)
                if tilted:
                    panel.color(0x881111)
                    state.text("TILTED")
                    seg.color(RED)
                    lcd.console('<span class=warn> เอียง %d องศา</span>' % abs(ang))
                else:
                    panel.color(0x115511)
                    state.text("LEVEL")
                    seg.color(GREEN)
                    lcd.console('<span class=ok> กลับมาราบแล้ว</span>')
                was_tilted = tilted

        n += 1
        if n % 30 == 0:                        # log เว้นระยะ ไม่ถี่จนรก console
            lcd.console(' pitch=%+d  roll=%+d  |a|=%.2f' % (p, r, mag))

        # ----- จังหวะ 4: ui.poll รับปุ่ม -----
        for ev in ui.poll():
            h = ev.get('handle')
            if h == back_id:
                raise KeyboardInterrupt
            elif h == reset_id:                # ปุ่ม Reset: ล้างค่า peak กลับเป็น 0
                peak = 0
                peak_lbl.text("peak: 0 deg")
                lcd.console(' ล้างค่า peak แล้ว')
        time.sleep_ms(80)
except KeyboardInterrupt:
    lcd.console('<span class=ok> จบการทำงาน</span>')
    print("stopped after", n, "samples, peak", peak, "deg")

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
