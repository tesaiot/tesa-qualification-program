# 03 - DPS368: จอแสดงความดัน + กราฟย้อนหลัง + สถิติสูง/ต่ำ
# firmware แก้อาการอุณหภูมิเพี้ยนหลังบูตแล้ว (correctTemperature จาก Infineon)
# เคล็ด: Chart รับ int - เก็บ hPa x10 เพื่อคงทศนิยม 1 ตำแหน่ง
import ui
ui.screen()
import lcd
import sensors
import time

lcd.clear()
lcd.console('<h2> Barometric Station</h2>')

ui.Label("DPS368 Pressure (hPa)", x=280, y=10, color=0xFFFFFF)
seg = ui.Seg7("----.-", x=270, y=45, color=0xFF4444)
lab_t   = ui.Label("temp: --.- C",   x=60, y=130, color=0x44CCFF)
lab_alt = ui.Label("alt~: ---.- m",  x=300, y=130, color=0xFFAA44)
lab_rec = ui.Label("hi/lo: -- / --", x=520, y=130, color=0xAAAAAA)

p0, _ = sensors.dps368.pressure_temperature()
band = int(p0 * 10)
chart = ui.Chart(x=50, y=170, w=700, h=160, min=band - 30, max=band + 30)

back = ui.Button("< ออก", x=560, y=350, w=130, h=38)
back_id = back.id()
ui.Label("ลองยกบอร์ดขึ้น-ลง 1 เมตร แล้วดูกราฟ", x=60, y=360, color=0x888888)

hi = lo = p0
n = 0
try:
    while True:
        p, t = sensors.dps368.pressure_temperature()
        hi = max(hi, p); lo = min(lo, p)
        seg.text("%.1f" % p)
        lab_t.text("temp: %.2f C" % t)
        lab_alt.text("alt~: %.1f m" % sensors.dps368.altitude())
        lab_rec.text("hi/lo: %.1f / %.1f" % (hi, lo))
        chart.value(int(p * 10))
        n += 1
        if n % 15 == 0:
            lcd.console(' P=%.2f hPa  T=%.2f C' % (p, t))
        for ev in ui.poll():
            if ev.get('handle') == back_id:
                raise KeyboardInterrupt
        time.sleep_ms(500)                     # 2 Hz พอ - ความดันเปลี่ยนช้า
except KeyboardInterrupt:
    lcd.console('<span class=ok> จบ: hi %.1f / lo %.1f hPa</span>' % (hi, lo))

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
