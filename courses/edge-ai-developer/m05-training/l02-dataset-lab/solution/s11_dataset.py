# s11_dataset.py - เก็บ dataset IMU ที่สมดุลและพร้อม train ลง CSV บนบอร์ด
# วิธีรัน: 1) เปิดใน BENTO IDE แล้วเสียบบอร์ดจริง (ต้องอ่าน IMU จริง)
#          2) กด "Program to Device"
#          3) แตะปุ่ม label ทำท่านั้นค้าง ~4 วินาที เก็บให้ครบทั้ง 3 คลาสจนแถบเต็ม
#          4) กด "< ออก" แล้วคัดลอก /gestures.csv ไป split บน PC ด้วย dataset_tools.py
#
# เฉลยนี้ไม่ได้มีไว้ลอกวาง สิ่งที่นับคือการอธิบายด้วยคำพูดของคุณเอง
# อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์ใหม่ด้วยมือ ตอนพิมพ์เองนั่นแหละสมองจะจำได้ว่า
# "dataset engineering" ต่างจากการเก็บ log ตรงไหน คำตอบคือ 2 บรรทัดสุดท้าย: การ
# นับต่อคลาส (counts) แล้วนำทางให้เก็บคลาสที่ยังน้อย - เก็บอย่างมีสติ ไม่ใช่เก็บดะ

import ui
ui.screen()
import lcd
import sensors
import time

RATE_MS = 20            # 50 Hz - ต้องตรงกับอัตราที่โมเดล Motion บนบอร์ดกิน ไม่งั้นท่า
                        # เดียวกันจะ "ยืด/หด" ในหน้าต่าง แล้วโมเดลจะสับสนตอนใช้จริง
BURST = 200            # เก็บทีละชุด 200 sample (~4 วินาที) ต่อการกดหนึ่งครั้ง
TARGET = 1000          # เป้าหมายต่อคลาส - เก็บให้ทุกคลาสถึงเป้าเท่ากัน = สมดุล
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

# สร้าง widget ครั้งเดียวก่อนลูป - ถ้าสร้างซ้ำทุกวนรอบจะกินหน่วยความจำและจอกระพริบ
ui.Label("Dataset - เก็บ IMU ให้สมดุล", x=20, y=10, color=CYAN)
status = ui.Label("แตะปุ่ม label แล้วทำท่านั้นค้างไว้", x=20, y=42, color=CYAN)

# ปุ่ม label หนึ่งปุ่มต่อคลาส + แถบสมดุลต่อคลาส สร้างครบไว้ก่อน แล้วในลูปแค่อัปเดตค่า
# แถบสมดุลนี่แหละคือหัวใจที่ทำให้เรา "เห็น" ว่าเก็บคลาสไหนไปเท่าไร ไม่ต้องเดา
btns = {}
bars = {}
labs = {}
for i, name in enumerate(CLASSES):
    y = 84 + i * 56
    btns[name] = ui.Button(name, x=20, y=y, w=150, h=44, color=GREEN)
    labs[name] = ui.Label("%s: 0" % name, x=190, y=y + 4, color=CYAN)
    bars[name] = ui.Bar(x=190, y=y + 26, w=560, h=12, min=0, max=TARGET, value=0, color=DIM)

hint = ui.Label("เริ่มเก็บได้เลย", x=20, y=270, color=AMBER)
back = ui.Button("< ออก", x=570, y=352, w=120, h=36, color=CARD)

# เขียนหัวตารางถ้าไฟล์ยังไม่มี - ลำดับคอลัมน์ต้องตรงกับ CHANNELS ใน dataset_tools.py
try:
    open(PATH, "r").close()
except OSError:
    with open(PATH, "w") as f:
        f.write("label,ax,ay,az,gx,gy,gz\n")

# ตัวนับจำนวน sample สะสมต่อคลาส - นี่คือสิ่งที่แยก "logger" (บทเรียน 2.1–2.2) ออกจาก
# "dataset engineering" (บทเรียน 5.1–5.2): เราไม่เก็บเฉยๆ แต่เฝ้าดูจำนวนต่อคลาสตลอด
counts = {c: 0 for c in CLASSES}


def refresh_balance():
    """อัปเดตแถบสมดุลทุกคลาส แล้วบอกว่าคลาสไหนยังน้อย เพื่อให้เก็บได้สมดุลกัน"""
    for c in CLASSES:
        bars[c].value(min(counts[c], TARGET))
        labs[c].text("%s: %d" % (c, counts[c]))
    # หัวใจข้อสี่: หาคลาสที่มี sample น้อยที่สุดตอนนี้ min(counts, key=counts.get)
    # วนคีย์ทั้งหมด เทียบด้วยค่า (counts.get) แล้วคืน "ชื่อคลาส" ที่ค่าน้อยสุด
    fewest = min(counts, key=counts.get)
    if counts[fewest] < TARGET:
        hint.text("เก็บ '%s' เพิ่ม (น้อยสุดตอนนี้)" % fewest)
        hint.color(AMBER)
    else:
        # ทุกคลาสถึงเป้าแล้ว = สมดุล พร้อมเอาไป split เป็น train/val/test บน PC
        hint.text("ครบทุกคลาสถึงเป้า - dataset พร้อม split!")
        hint.color(GREEN)


def record(label):
    """เก็บ BURST samples ของ label นี้ลงไฟล์ที่อัตรา RATE_MS แล้วนับเข้าตัวนับสมดุล"""
    status.text("กำลังเก็บ '%s' ..." % label)
    with open(PATH, "a") as f:
        for _ in range(BURST):
            # หัวใจข้อหนึ่ง: อ่าน IMU 6 แกนพร้อมกันในทูเพิลเดียว = 6 คอลัมน์ของ CSV เป๊ะ
            # accel 3 แกน (m/s^2, az~9.81 ตอนนิ่ง) + gyro 3 แกน (deg/s, ~0 ตอนไม่หมุน)
            ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
            # หัวใจข้อสอง: เขียนหนึ่งบรรทัด ป้าย (label) มาก่อนเสมอ ตามด้วย 6 ค่า
            # dataset_tools.py ใช้ CLASSES.index(label) แปลงป้ายเป็นตัวเลข ป้ายต้องสะกดตรง
            f.write("%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n" % (label, ax, ay, az, gx, gy, gz))
            time.sleep_ms(RATE_MS)          # เว้นจังหวะให้ครบ 50 Hz พอดี
    # หัวใจข้อสาม: บวกจำนวนที่เพิ่งเก็บเข้าตัวนับของคลาสนี้ แถบสมดุลจะขยับตามทันที
    counts[label] += BURST
    refresh_balance()
    status.text("เสร็จ '%s' - เลือกท่าต่อไปให้สมดุล" % label)
    lcd.console("<span class=ok> logged %d samples of '%s' -> %s</span>" % (BURST, label, PATH))


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
    # สรุปให้เห็นสัดส่วนตอนจบ - ถ้าตัวเลขต่อคลาสห่างกันมาก ควรกลับมาเก็บเพิ่มก่อน train
    total = sum(counts.values())
    lcd.console("<span class=ok> dataset done: %d samples total in %s</span>" % (total, PATH))
    lcd.console(" per-class: %s" % ", ".join("%s=%d" % (c, counts[c]) for c in CLASSES))
    status.text("จบ - dataset อยู่ที่ %s (split ต่อบน PC ด้วย dataset_tools.py)" % PATH)

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
