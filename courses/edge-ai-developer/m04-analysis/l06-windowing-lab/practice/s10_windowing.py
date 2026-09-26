# s10_windowing.py - โมเดล "เห็น" อะไร: windowing + feature vector (ฉบับฝึกเติมโค้ด)
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) เติมช่องว่าง (# เติม:) ทั้ง 5 จุดตามคำใบ้ในคอมเมนต์ให้ครบ
#          3) กด "Program to Device" (หรือ Run) แล้ววางบอร์ดนิ่ง สลับกับเขย่าเบา ๆ
#          4) ดู feature vector (mean/std/พลังงาน 4 ย่าน) ขยับตามการเคลื่อนไหวจริง
#
# แนวคิดของชุดบทเรียนนี้: โมเดลไม่ได้กิน sample ดิบทีละจุด มันกิน "หน้าต่าง" (window) ของ
# สัญญาณก้อนหนึ่ง แล้วบีบเป็น feature vector สั้น ๆ ก่อนป้อนเข้าโมเดล โปรแกรมนี้ทำ
# front-end อันนั้นให้เห็นด้วยตา: สตรีม IMU -> ตัดเป็นหน้าต่างซ้อนกัน -> คำนวณ feature
# -> โชว์เป็นแท่ง งานของเราชุดบทเรียนนี้อยู่ที่ 5 จุด: เก็บ sample / mean / std / band energy /
# เลื่อนหน้าต่าง สี่ห้าบรรทัดนี้คือหัวใจของ "สิ่งที่โมเดลเห็น"

import ui
ui.screen()
import lcd
import sensors
import time
import math

# ธีมสี (ให้คุ้นตากับหน้า Analysis จริงบนบอร์ด)
CYAN   = 0x71C7EC   # หัวข้อ
GREEN  = 0x50D890   # แท่ง feature
PURPLE = 0xBB86FC   # ตัวนับหน้าต่าง
CARD   = 0x2A1712   # พื้นปุ่ม back
SEC    = 0xCFC6BF   # ข้อความรอง

WIN   = 50          # ขนาดหน้าต่าง (1 วินาทีที่ 50 Hz) - เท่าที่โมเดลใช้จริง
HOP   = 25          # เลื่อนหน้าต่างทีละ 25 จุด (สองหน้าต่างซ้อนกัน 50%)
BANDS = 4           # แบ่งพลังงานเป็น 4 ย่านตามเวลา
DT_MS = 20          # คาบสุ่ม 20 ms = 50 Hz


def features(win):
    """บีบหนึ่งหน้าต่าง (แกน Z ของ accel) ให้เป็น feature vector สั้น ๆ
    คืน [mean, std, band0..band3] - นี่คือสิ่งที่โมเดลเห็น ไม่ใช่สัญญาณดิบ"""
    n = len(win)
    # เติม: ค่าเฉลี่ยของหน้าต่าง  ->  mean = sum(win) / n
    mean = 0.0
    # เติม: ส่วนเบี่ยงเบนมาตรฐาน (บอกความแรงของการสั่น)
    #       ->  std = math.sqrt(sum((x - mean) ** 2 for x in win) / n)
    std = 0.0
    # พลังงานอย่างง่ายต่อย่าน: แบ่งหน้าต่างเป็น BANDS ช่วงเท่า ๆ กัน วัด variance แต่ละช่วง
    band_e = []
    seg = n // BANDS
    for b in range(BANDS):
        s = win[b * seg:(b + 1) * seg]
        m = sum(s) / len(s)
        # เติม: พลังงาน (variance) ของย่านนี้ ต่อท้าย band_e
        #       ->  band_e.append(sum((x - m) ** 2 for x in s) / len(s))
        pass
    return [mean, std] + band_e


# ---- สร้าง widget ครั้งเดียวก่อนเข้าลูป (อย่าสร้างซ้ำในลูป จอจะกระพริบ) ----
ui.Label("Windowing - โมเดลเห็นอะไร", x=20, y=10, color=CYAN)
info = ui.Label("สตรีม -> หน้าต่าง -> feature vector", x=20, y=44, color=SEC)
names = ["mean", "std", "band0", "band1", "band2", "band3"]
bars = []
for i, nm in enumerate(names):
    ui.Label(nm, x=20, y=90 + i * 36, color=SEC)
    bars.append(ui.Bar(x=160, y=92 + i * 36, w=560, h=22, min=0, max=100, value=0, color=GREEN))
win_lbl = ui.Label("windows: 0", x=20, y=320, color=PURPLE)
back = ui.Button("< ออก", x=640, y=316, w=120, h=44, color=CARD)
back_id = back.id()

lcd.clear()
lcd.console('<h2> Windowing - feature front-end</h2>')
lcd.console(' WIN=%d, HOP=%d, BANDS=%d (IMU 50 Hz)' % (WIN, HOP, BANDS))

buf = []
nwin = 0

try:
    while True:
        # เก็บ HOP จุดใหม่ ต่อท้าย buffer (สัญญาณสตรีมเข้ามาเรื่อย ๆ)
        for _ in range(HOP):
            ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
            # เติม: เก็บ accel แกน Z (az) ต่อท้าย buffer  ->  buf.append(az)
            pass
            time.sleep_ms(DT_MS)
        # เมื่อ buffer ยาวพอหนึ่งหน้าต่าง -> คำนวณ feature แล้วเลื่อนหน้าต่าง
        if len(buf) >= WIN:
            fv = features(buf[-WIN:])
            nwin += 1
            win_lbl.text("windows: %d" % nwin)
            # โชว์ feature vector เป็นแท่ง (สเกลคร่าว ๆ ให้เห็นการเปลี่ยน)
            for i, v in enumerate(fv):
                scaled = min(100, int(abs(v) * (2 if i < 2 else 0.02)))
                bars[i].value(scaled)
            lcd.console(" fv = [" + ", ".join("%.2f" % v for v in fv) + "]")
            # เติม: เก็บเฉพาะ WIN จุดท้ายไว้ให้หน้าต่างถัดไปซ้อน 50%  ->  buf = buf[-WIN:]
            pass
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
