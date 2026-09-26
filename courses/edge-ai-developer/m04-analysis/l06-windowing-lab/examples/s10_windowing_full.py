# s10_windowing_full.py - feature front-end แบบเห็นภาพ: windowing + feature vector (ฉบับเต็ม)
# วิธีรัน: เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator (ide.tesaiot.dev)
#          กด "Program to Device" แล้ววางบอร์ดนิ่ง สลับกับเขย่า/หมุนเบา ๆ
#
# ฉบับนี้คือเวอร์ชันที่ขัดจนเรียบร้อยของ s10_windowing.py - โครงเดียวกับที่คุณเติมใน
# ไฟล์ฝึก แต่เพิ่มรายละเอียดที่ทำให้ "อ่านสิ่งที่โมเดลเห็นได้ชัดขึ้น": เน้นย่านพลังงาน
# ที่แรงสุด, ตัดสินหยาบ ๆ ว่า "นิ่ง/ขยับ" จาก std (สะพานสู่การจำแนกคลาส), และโชว์อัตรา
# หน้าต่างต่อวินาที ทั้งหมดยังยืนบนแนวคิดเดียว: สัญญาณดิบ -> หน้าต่าง -> feature vector

import ui
ui.screen()
import lcd
import sensors
import time
import math

# ธีมสีเดียวกับหน้า Analysis จริงบนบอร์ด
CYAN   = 0x71C7EC   # หัวข้อ / อัตรา
GREEN  = 0x50D890   # แท่งทั่วไป + "ขยับ"
AMBER  = 0xE0A03A   # ย่านพลังงานที่แรงสุดในหน้าต่างนี้
DIM    = 0x6A3A31   # แท่งจาง
PURPLE = 0xBB86FC   # ตัวนับหน้าต่าง
RED    = 0xE85B5B   # "นิ่ง"
CARD   = 0x2A1712   # พื้นปุ่ม back
SEC    = 0xCFC6BF   # ข้อความรอง

WIN      = 50       # ขนาดหน้าต่าง (1 วินาทีที่ 50 Hz) - เท่าที่โมเดลใช้จริง
HOP      = 25       # เลื่อนหน้าต่างทีละ 25 จุด (ซ้อนกัน 50%)
BANDS    = 4        # แบ่งพลังงานเป็น 4 ย่านตามเวลา
DT_MS    = 20       # คาบสุ่ม 20 ms = 50 Hz
STD_MOVE = 0.06     # เส้นแบ่งหยาบ ๆ: std เกินนี้ถือว่า "ขยับ" (m/s²) - จูนได้ตามบอร์ด

# สเกลของแต่ละ feature (คูณก่อนวาดแท่ง) ให้ทุกตัวพอเห็นในช่วง 0..100
SCALE = (2.0, 900.0, 0.03, 0.03, 0.03, 0.03)   # mean, std, band0..band3
NAMES = ["mean", "std", "band0", "band1", "band2", "band3"]


def features(win):
    """บีบหนึ่งหน้าต่าง (แกน Z ของ accel) ให้เป็น feature vector [mean, std, band0..band3]
    หน้าต่าง WIN จุดกลายเป็นตัวเลข 6 ตัว - โมเดลเห็น 6 ตัวนี้ ไม่เคยเห็นจุดดิบเลย"""
    n = len(win)
    mean = sum(win) / n                                        # ระดับ DC ของหน้าต่าง
    std = math.sqrt(sum((x - mean) ** 2 for x in win) / n)      # ความแรงของการสั่น
    band_e = []
    seg = n // BANDS
    for b in range(BANDS):
        s = win[b * seg:(b + 1) * seg]
        m = sum(s) / len(s)
        band_e.append(sum((x - m) ** 2 for x in s) / len(s))    # variance ต่อย่านเวลา
    return [mean, std] + band_e


# ---- สร้าง widget ครั้งเดียวก่อนเข้าลูป ----
ui.Label("Windowing - โมเดลเห็นอะไร", x=20, y=10, color=CYAN)
info = ui.Label("สตรีม -> หน้าต่าง -> feature vector", x=20, y=44, color=SEC)
verdict = ui.Label("--", x=470, y=10, color=SEC)             # นิ่ง / ขยับ (จาก std)
rate_lbl = ui.Label("rate: -- win/s", x=470, y=44, color=CYAN)

bars = []
for i, nm in enumerate(NAMES):
    ui.Label(nm, x=20, y=90 + i * 36, color=SEC)
    bars.append(ui.Bar(x=160, y=92 + i * 36, w=560, h=22, min=0, max=100, value=0, color=GREEN))
win_lbl = ui.Label("windows: 0", x=20, y=320, color=PURPLE)
back = ui.Button("< ออก", x=570, y=316, w=120, h=44, color=CARD)
back_id = back.id()

lcd.clear()
lcd.console('<h2> Windowing - feature front-end (ฉบับเต็ม)</h2>')
lcd.console(' WIN=%d, HOP=%d, BANDS=%d, STD_MOVE=%.3f' % (WIN, HOP, BANDS, STD_MOVE))

buf = []
nwin = 0
t_last = time.ticks_ms()

try:
    while True:
        # เก็บ HOP จุดใหม่ ต่อท้าย buffer (สตรีมเข้ามาเรื่อย ๆ ทีละก้อน)
        for _ in range(HOP):
            ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
            buf.append(az)
            time.sleep_ms(DT_MS)

        if len(buf) >= WIN:
            fv = features(buf[-WIN:])
            nwin += 1
            win_lbl.text("windows: %d" % nwin)

            # อัตราหน้าต่างต่อวินาที (หนึ่งหน้าต่างใหม่ต่อ HOP*DT_MS มิลลิวินาที)
            now = time.ticks_ms()
            dt = time.ticks_diff(now, t_last)
            t_last = now
            if dt > 0:
                rate_lbl.text("rate: %.1f win/s" % (1000.0 / dt))

            # เน้นย่านพลังงานที่แรงสุด (index 2..5) ให้เห็นว่าการสั่นกระจุกตรงไหนของหน้าต่าง
            band_vals = fv[2:]
            top_band = 2 + band_vals.index(max(band_vals))
            for i, v in enumerate(fv):
                scaled = min(100, int(abs(v) * SCALE[i]))
                bars[i].value(scaled)
                bars[i].color(AMBER if i == top_band else (GREEN if i < 2 else DIM))

            # ตัดสินหยาบ ๆ ว่า นิ่ง/ขยับ จาก std - นี่คือ "จำแนกคลาส" เวอร์ชันมือทำ
            moving = fv[1] >= STD_MOVE
            verdict.text("ขยับ" if moving else "นิ่ง")
            verdict.color(GREEN if moving else RED)

            lcd.console(" fv = [" + ", ".join("%.3f" % v for v in fv) + "]  ->  "
                        + ("moving" if moving else "still"))
            buf = buf[-WIN:]                 # เก็บหน้าต่างเดิมไว้ให้ถัดไปซ้อน 50%

        for ev in ui.poll():
            if ev.get("handle") == back_id:
                raise KeyboardInterrupt
except KeyboardInterrupt:
    pass
finally:
    info.text("จบ - feature vector นี้แหละที่ป้อนเข้าโมเดล")
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
