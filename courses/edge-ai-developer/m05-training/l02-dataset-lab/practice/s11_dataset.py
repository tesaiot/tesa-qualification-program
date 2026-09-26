# s11_dataset.py - เก็บ dataset IMU ที่ "สมดุลและพร้อม train" ลง CSV (ฉบับฝึกเติมโค้ด)
# วิธีรัน: 1) เปิดใน BENTO IDE แล้วเสียบบอร์ดจริง (ชุดบทเรียนนี้ต้องอ่าน IMU จริง)
#          2) เติมช่องว่าง (pass) ทั้ง 4 จุดตามคำใบ้ในคอมเมนต์ให้ครบ
#          3) กด "Program to Device" แล้วแตะปุ่ม label ทำท่านั้นค้าง ~4 วินาที
#          4) เก็บให้ครบทั้ง 3 คลาสจนแถบสมดุลเต็ม แล้วกด "< ออก" ไฟล์อยู่ที่ /gestures.csv
#
# บทเรียน 2.1–2.2 เราเขียน logger ที่เก็บ IMU ลง CSV ได้ ชุดบทเรียนนี้เรายกระดับเป็น "dataset
# engineering": เก็บพร้อมเฝ้า class balance ตลอด แล้วส่ง CSV ต่อให้ dataset_tools.py
# แบ่ง train/val/test บน PC งานของเราชุดบทเรียนนี้คือเติม 4 คำสั่ง: อ่าน -> เขียน -> นับ -> นำทาง

import ui
ui.screen()
import lcd
import sensors
import time

RATE_MS = 20            # 50 Hz - ตรงกับอัตราที่โมเดล Motion บนบอร์ดกิน
BURST = 200            # จำนวน sample ต่อการกดหนึ่งครั้ง (~4 วินาที)
TARGET = 1000          # เป้าหมาย sample ต่อคลาส (เก็บให้ทุกคลาสถึงเป้า = สมดุล)
PATH = "/gestures.csv"
CLASSES = ("idle", "circle", "shaking")   # 3 คลาสเดียวกับโมเดล Motion + dataset_tools.py

# ธีมสีเดียวกับหน้าอื่นในคอร์ส (จะได้คุ้นตากับของจริง)
CYAN   = 0x71C7EC   # หัวข้อ / ข้อความรอง
GREEN  = 0x50D890   # ปุ่ม label + สถานะดี
AMBER  = 0xE0A03A   # คลาสที่ยังน้อย
DIM    = 0x6A3A31   # พื้นแถบ
CARD   = 0x2A1712   # พื้นการ์ด

lcd.clear()
lcd.console('<h2> Dataset Engineering - เก็บให้สมดุล</h2>')
lcd.console(' เป้าหมาย: เก็บ %d sample/คลาส ให้ครบทั้ง %s' % (TARGET, ", ".join(CLASSES)))

# สร้าง widget ครั้งเดียวก่อนลูป (สร้างซ้ำในลูปจะกินหน่วยความจำและจอกระพริบ)
ui.Label("Dataset - เก็บ IMU ให้สมดุล", x=20, y=10, color=CYAN)
status = ui.Label("แตะปุ่ม label แล้วทำท่านั้นค้างไว้", x=20, y=42, color=CYAN)

# ปุ่ม label + แถบสมดุลต่อคลาส (สร้างครบทุกคลาสไว้ก่อน แล้วแค่อัปเดตค่า)
btns = {}
bars = {}
labs = {}
for i, name in enumerate(CLASSES):
    y = 84 + i * 56
    btns[name] = ui.Button(name, x=20, y=y, w=150, h=44, color=GREEN)
    labs[name] = ui.Label("%s: 0" % name, x=190, y=y + 4, color=CYAN)
    bars[name] = ui.Bar(x=190, y=y + 26, w=560, h=12, min=0, max=TARGET, value=0, color=DIM)

hint = ui.Label("เริ่มเก็บได้เลย", x=20, y=270, color=AMBER)
back = ui.Button("< ออก", x=650, y=352, w=120, h=36, color=CARD)

# เขียนหัวตารางถ้าไฟล์ยังไม่มี (ให้ไว้แล้ว)
try:
    open(PATH, "r").close()
except OSError:
    with open(PATH, "w") as f:
        f.write("label,ax,ay,az,gx,gy,gz\n")

# ตัวนับจำนวน sample สะสมต่อคลาส - หัวใจของ class balance
counts = {c: 0 for c in CLASSES}


def refresh_balance():
    """อัปเดตแถบสมดุล + บอกว่าคลาสไหนยังน้อย เพื่อให้เก็บได้สมดุล"""
    for c in CLASSES:
        bars[c].value(min(counts[c], TARGET))
        labs[c].text("%s: %d" % (c, counts[c]))
    # เติม: หาคลาสที่เก็บได้ "น้อยที่สุด" ตอนนี้ เพื่อบอกผู้ใช้ให้ไปเก็บเพิ่ม
    #   -> fewest = min(counts, key=counts.get)
    fewest = CLASSES[0]
    pass
    if counts[fewest] < TARGET:
        hint.text("เก็บ '%s' เพิ่ม (น้อยสุดตอนนี้)" % fewest)
        hint.color(AMBER)
    else:
        hint.text("ครบทุกคลาสถึงเป้า - dataset พร้อม split!")
        hint.color(GREEN)


def record(label):
    """เก็บ BURST samples ของ label นี้ลงไฟล์ ที่อัตรา RATE_MS แล้วนับเข้าตัวนับสมดุล"""
    status.text("กำลังเก็บ '%s' ..." % label)
    with open(PATH, "a") as f:
        for _ in range(BURST):
            # เติม: อ่าน IMU 6 แกนในบรรทัดเดียว
            #   -> ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
            ax = ay = az = gx = gy = gz = 0.0
            pass
            # เติม: เขียนหนึ่งบรรทัด "label,ax,ay,az,gx,gy,gz" ลงไฟล์
            #   -> f.write("%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n"
            #              % (label, ax, ay, az, gx, gy, gz))
            pass
            time.sleep_ms(RATE_MS)
    # เติม: บวกจำนวน sample ของคลาสนี้เข้าตัวนับ (class balance)
    #   -> counts[label] += BURST
    pass
    refresh_balance()
    status.text("เสร็จ '%s' - เลือกท่าต่อไปให้สมดุล" % label)
    lcd.console(" logged %d samples of '%s' -> %s" % (BURST, label, PATH))


refresh_balance()

try:
    while True:
        for ev in ui.poll():
            h = ev.get("handle")
            if h == back.id():
                raise KeyboardInterrupt
            for name in CLASSES:
                if h == btns[name].id():
                    record(name)
        time.sleep_ms(30)
except KeyboardInterrupt:
    pass
finally:
    total = sum(counts.values())
    lcd.console(" dataset done: %d samples total in %s" % (total, PATH))
    lcd.console(" per-class: %s" % ", ".join("%s=%d" % (c, counts[c]) for c in CLASSES))
    status.text("จบ - dataset อยู่ที่ %s (split ต่อบน PC)" % PATH)

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
