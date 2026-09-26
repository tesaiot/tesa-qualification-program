# 08 - Environment Dashboard: 3 การ์ด (อุณหภูมิ / ความชื้น / ความดัน)
# แบบแดชบอร์ดเซนเซอร์: Panel เป็นการ์ด + ค่าตัวใหญ่
import ui
ui.screen()
import lcd
import sensors
import dsp
import time

lcd.clear()
lcd.console('<h2> Environment Dashboard</h2>')

ui.Label("TESAIoT Environment Station", x=270, y=8, color=0xFFFFFF)

ui.Panel(x=40,  y=45, w=225, h=200, color=0x223344)
ui.Label("Temp (C)", x=100, y=60, color=0x44CCFF)
seg_t = ui.Seg7("--.-", x=75, y=100, color=0x44CCFF)

ui.Panel(x=285, y=45, w=225, h=200, color=0x334422)
ui.Label("Humidity (%)", x=330, y=60, color=0x44FF88)
arc_h = ui.Arc(x=320, y=85, min=0, max=100, value=0)

ui.Panel(x=530, y=45, w=225, h=200, color=0x443322)
ui.Label("Pressure (hPa)", x=575, y=60, color=0xFFAA44)
seg_p = ui.Seg7("----", x=545, y=100, color=0xFFAA44)

verdict = ui.Label("...", x=60, y=270, color=0xAAAAAA)
lab_dew = ui.Label("dew: --  feels: --", x=60, y=305, color=0x888888)

back = ui.Button("< ออก", x=560, y=350, w=130, h=38)
back_id = back.id()

n = 0
try:
    while True:
        p, t = sensors.dps368.pressure_temperature()
        h = sensors.sht40.humidity()
        seg_t.text("%.1f" % t)
        arc_h.value(int(h))
        seg_p.text("%d" % int(p))
        lab_dew.text("dew: %.1f C   feels: %.1f C"
                     % (dsp.dew_point(t, h), dsp.heat_index(t, h)))
        # เกณฑ์สบาย: 23-32C และ RH 40-70% (ปรับตามห้องที่ใช้งานได้)
        if 23 <= t <= 32 and 40 <= h <= 70:
            verdict.text("สบายดี - อยู่ในโซน comfort")
            verdict.color(0x44FF88)
        else:
            verdict.text("นอกโซน comfort - ปรับอากาศ/ระบายลม")
            verdict.color(0xFFAA44)
        n += 1
        if n % 10 == 0:
            lcd.console(' T=%.1fC RH=%.0f%% P=%.0f hPa' % (t, h, p))
        for ev in ui.poll():
            if ev.get('handle') == back_id:
                raise KeyboardInterrupt
        time.sleep_ms(1000)                     # สภาพแวดล้อมเปลี่ยนช้า - 1 Hz พอ
except KeyboardInterrupt:
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
