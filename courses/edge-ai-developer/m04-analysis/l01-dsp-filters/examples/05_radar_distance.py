# 05 - Radar Range: ไม้วัดระยะบนจอ (Bar + Seg7 + กราฟ)
# ฝั่ง C ทำ HPF -> FFT -> dB -> หา peak ให้แล้ว - Python แค่แสดงผล
# ความละเอียด ~0.33 m/bin: บอกโซนได้แม่น แต่ไม่ใช่เวอร์เนีย
import ui
ui.screen()
import lcd
import sensors
import time

MAX_CM = 500                                   # สนใจถึง 5 เมตร
NEAR_CM = 100                                  # ต่ำกว่านี้ = โซนใกล้ (แดง)

lcd.clear()
lcd.console('<h2> Radar Range Finder</h2>')
sensors.radar_config(0)                        # จำฉากนิ่งใหม่ (อย่ายืนหน้าบอร์ด!)
time.sleep_ms(500)
sensors.radar_config(4.0)                      # 4 dB เหนือ baseline (ค่าที่สอบเทียบแล้ว
                                               # — คนยืนนิ่งสะท้อน ~+3dB จากการหายใจ)

# median filter 5 ค่า — กัน multipath โดดข้ามเฟรม (บทเรียน filtering ของจริง)
hist = []
def smooth(cm):
    hist.append(cm)
    if len(hist) > 5:
        hist.pop(0)
    return sorted(hist)[len(hist) // 2]

ui.Label("BGT60TR13C - Distance", x=290, y=10, color=0xFFFFFF)
seg = ui.Seg7("---", x=300, y=45, color=0x00FF88)
ui.Label("cm", x=470, y=70, color=0x888888)
bar = ui.Bar(x=50, y=140, w=690, min=0, max=MAX_CM, value=0)
chart = ui.Chart(x=50, y=185, w=700, h=150, min=0, max=MAX_CM)
lab = ui.Label("รอเป้า...", x=50, y=120, color=0xAAAAAA)

back = ui.Button("< ออก", x=560, y=350, w=130, h=38)
back_id = back.id()
ui.Label("เดินเข้า-ออกหน้าบอร์ด 0.5 - 5 เมตร", x=60, y=360, color=0x888888)

zone_near = None
try:
    while True:
        r = sensors.radar_range()
        if r["target"]:
            cm = int(r["distance_m"] * 100)
            seg.text("%d" % cm)
            bar.value(min(cm, MAX_CM))
            chart.value(min(cm, MAX_CM))
            lab.text("peak %.1f dB  (+/- %d cm)" % (r["peak_db"],
                                                    int(r["resolution_m"] * 100)))
            near = cm < NEAR_CM
            if near != zone_near:              # เปลี่ยนโซนค่อยเปลี่ยนสี
                bar.color(0xFF4444 if near else 0x44CC44)
                zone_near = near
        else:
            seg.text("---")
            lab.text("ไม่พบเป้าเหนือ threshold")
        for ev in ui.poll():
            if ev.get('handle') == back_id:
                raise KeyboardInterrupt
        time.sleep_ms(250)
except KeyboardInterrupt:
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
