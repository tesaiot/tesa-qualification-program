# s10_windowing.py - โมเดล "เห็น" อะไร: windowing + feature vector
#
# โมเดลไม่ได้กิน sample ทีละจุด มันกิน "หน้าต่าง" (window) ของสัญญาณ แล้วบีบเป็น
# feature vector สั้น ๆ โปรแกรมนี้แสดงกระบวนการนั้นให้เห็นด้วยตา:
#   สตรีม IMU -> ตัดเป็นหน้าต่างซ้อนกัน (win=50, hop=25) -> คำนวณ feature ต่อหน้าต่าง
#   (mean, std, พลังงาน 4 ย่านความถี่) -> แสดง feature vector ล่าสุด
#
# นี่คือสะพานสู่โมดูล 5 (Training): dataset ที่เรา train ก็คือชุดของ feature vector แบบนี้
# และ front-end บนบอร์ด (FFT/mel) ก็ทำงานแบบเดียวกันนี้ก่อนส่งเข้าโมเดล

import ui, lcd, sensors, time, math

WIN = 50               # ขนาดหน้าต่าง (1 วินาทีที่ 50 Hz) - เท่าที่โมเดลใช้
HOP = 25               # เลื่อนทีละ 25 (ซ้อน 50%)
BANDS = 4              # แบ่งพลังงานเป็น 4 ย่านความถี่


def features(win):
    # feature vector จากหนึ่งหน้าต่าง (แกน Z ของ accel)
    n = len(win)
    mean = sum(win) / n
    std = math.sqrt(sum((x - mean) ** 2 for x in win) / n)
    # พลังงานอย่างง่ายต่อย่าน (แบ่งหน้าต่างเป็น BANDS ช่วง วัด variance แต่ละช่วง)
    band_e = []
    seg = n // BANDS
    for b in range(BANDS):
        s = win[b * seg:(b + 1) * seg]
        m = sum(s) / len(s)
        band_e.append(sum((x - m) ** 2 for x in s) / len(s))
    return [mean, std] + band_e


# สร้าง widget ครั้งเดียว
ui.screen()
ui.Label("Windowing - โมเดลเห็นอะไร", x=20, y=10, color=0x71C7EC)
info = ui.Label("สตรีม -> หน้าต่าง -> feature vector", x=20, y=44)
labels = []
names = ["mean", "std", "band0", "band1", "band2", "band3"]
bars = []
for i, nm in enumerate(names):
    labels.append(ui.Label(nm, x=20, y=90 + i * 36))
    bars.append(ui.Bar(x=160, y=92 + i * 36, w=560, h=22, color=0x50D890))
win_lbl = ui.Label("windows: 0", x=20, y=320, color=0xBB86FC)
back = ui.Button("< ออก", x=570, y=316, w=120, h=44, color=0x2A1712)

buf = []
nwin = 0

try:
    while True:
        # เก็บทีละ HOP จุดใหม่ ต่อท้าย buffer
        for _ in range(HOP):
            _, _, az, _, _, _ = sensors.bmi270.motion()
            buf.append(az)
            time.sleep_ms(20)
        # เมื่อ buffer ยาวพอหนึ่งหน้าต่าง -> คำนวณ feature แล้วเลื่อน
        if len(buf) >= WIN:
            fv = features(buf[-WIN:])
            nwin += 1
            win_lbl.text("windows: %d" % nwin)
            # แสดง feature vector (normalize คร่าว ๆ ให้เห็นแท่ง)
            for i, v in enumerate(fv):
                scaled = min(100, int(abs(v) * (2 if i < 2 else 0.02)))
                bars[i].value(scaled)
            lcd.console("fv = [" + ", ".join("%.2f" % v for v in fv) + "]")
            buf = buf[-WIN:]        # เก็บหน้าต่างเดิมไว้ให้ซ้อน
        for ev in ui.poll():
            if ev.get("handle") == back.id():
                raise KeyboardInterrupt
except KeyboardInterrupt:
    pass
finally:
    info.text("จบ - feature vector นี้แหละที่ป้อนเข้าโมเดล")

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
