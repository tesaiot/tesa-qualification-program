# 02 - มุมเอียง: เกจ Arc คู่ (pitch / roll) + ตัวเลข Seg7
# dsp.tilt คำนวณฝั่ง C - คืน (roll, pitch) เป็นองศา
import ui
ui.screen()
import lcd
import sensors
import dsp
import time

lcd.clear()
lcd.console('<h2> Tilt Gauges</h2>')

ui.Label("Pitch", x=170, y=30, color=0x44CCFF)
arc_p = ui.Arc(x=100, y=60, min=-90, max=90, value=0)
ui.Label("Roll", x=560, y=30, color=0xFFAA44)
arc_r = ui.Arc(x=490, y=60, min=-90, max=90, value=0)

seg = ui.Seg7("0", x=330, y=110, color=0x00FF88)   # มุมเด่น (องศา)
ui.Label("องศาที่เอียงมากสุด", x=330, y=175, color=0x888888)

back = ui.Button("< ออก", x=560, y=350, w=130, h=38)
back_id = back.id()
ui.Label("เอียงบอร์ดช้าๆ ทั้งสองแกน", x=60, y=360, color=0x888888)

DEAD = 2.0        # องศา - deadzone กันเข็มสั่นตอนวางราบ
last = (999, 999)
try:
    while True:
        ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
        roll, pitch = dsp.tilt(ax, ay, az)
        p = 0 if abs(pitch) < DEAD else int(pitch)
        r = 0 if abs(roll) < DEAD else int(roll)
        if (p, r) != last:                     # อัปเดตเฉพาะตอนค่าเปลี่ยนจริง
            arc_p.value(p)
            arc_r.value(r)
            seg.text("%d" % (p if abs(p) >= abs(r) else r))
            last = (p, r)
        for ev in ui.poll():
            if ev.get('handle') == back_id:
                raise KeyboardInterrupt
        time.sleep_ms(100)
except KeyboardInterrupt:
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
