# s04_daq_logger.py - เก็บข้อมูล sensor ลงไฟล์ CSV (Data Acquisition) (ฉบับฝึกเติมโค้ด)
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) เติมช่องว่าง (pass) ทั้ง 4 จุดตามคำใบ้ในคอมเมนต์ให้ครบ
#          3) กด "Program to Device" แล้วแตะปุ่ม label ที่ต้องการ ทำท่านั้นค้างไว้
#          4) กด "< ออก" แล้วเปิดไฟล์ /gestures.csv ดูว่ามีข้อมูลกี่บรรทัด
#
# นี่คือก้าวแรกของ Edge AI จริง: ก่อนจะ train โมเดลได้ เราต้องมี "ข้อมูล" ก่อน
# โปรแกรมนี้อ่าน IMU ที่อัตราคงที่ (sampling rate) แล้วเขียนลงไฟล์ CSV บนบอร์ด
# ไฟล์นี้จะกลายเป็น dataset ที่เราเอาไป train ในบทเรียน Training (โมดูล 5)
#
# หัวใจของ DAQ ยืนบน 4 เรื่อง ที่คุณจะได้เติมเองในไฟล์นี้:
#   1) schema  - รูปแบบหนึ่งบรรทัดต่อหนึ่ง sample:  label,ax,ay,az,gx,gy,gz
#   2) sample  - อ่านค่าเซนเซอร์หนึ่ง snapshot ด้วย sensors.bmi270.motion()
#   3) record  - เขียน sample นั้นต่อท้ายไฟล์เป็นหนึ่งบรรทัด
#   4) rate    - เว้นจังหวะให้คงที่ (RATE_MS) เพื่อให้อัตราสุ่มตรงกับที่โมเดลกิน

import ui
ui.screen()                       # เคลียร์จอ + เตรียม canvas 792x398
import lcd
import sensors
import time

RATE_MS = 20                      # 50 Hz - ตรงกับอัตราที่โมเดล Motion บนบอร์ดกิน
BURST   = 200                     # จำนวน sample ต่อการกดหนึ่งครั้ง (~4 วินาที)
PATH    = "/gestures.csv"
LABELS  = ("idle", "circle", "shaking")   # ให้ตรงกับคลาสของโมเดล Motion

# ธีมสีให้คุ้นตากับหน้าจออื่นในคอร์ส
CYAN  = 0x71C7EC
GREEN = 0x50D890
DARK  = 0x2A1712
SEC   = 0xCFC6BF

lcd.clear()
lcd.console('<h2> DAQ Logger - เก็บ dataset ลง CSV</h2>')

# ---- สร้าง widget ครั้งเดียวก่อนลูป (สร้างซ้ำในลูปจะกินหน่วยความจำ + จอกระพริบ) ----
ui.Label("DAQ Logger", x=20, y=10, color=CYAN)
status    = ui.Label("เลือก label แล้วทำท่าค้างไว้", x=20, y=44, color=SEC)
count_lbl = ui.Label("บันทึกแล้ว: 0 samples", x=20, y=76, color=GREEN)
btns = []
for i, name in enumerate(LABELS):
    btns.append(ui.Button(name, x=20 + i * 130, y=120, w=120, h=54, color=GREEN))
back = ui.Button("< ออก", x=20, y=320, w=120, h=48, color=DARK)
back_id = back.id()

# เขียน "หัวตาราง" ครั้งเดียวถ้าไฟล์ยังไม่มี - บรรทัดแรกของ CSV คือ schema
# บอกว่าแต่ละคอลัมน์คืออะไร เครื่องมือ train จะอ่านหัวนี้เพื่อรู้จักคอลัมน์
try:
    open(PATH, "r").close()       # ไฟล์มีอยู่แล้ว -> ไม่ต้องเขียนหัวซ้ำ
except OSError:
    with open(PATH, "w") as f:
        # เติม: เขียนหัวตาราง (schema) ด้วย
        #       f.write("label,ax,ay,az,gx,gy,gz\n")
        pass

total = 0


def record(label):
    """บันทึก BURST samples ของ label นี้ต่อท้ายไฟล์ ที่อัตรา RATE_MS คงที่"""
    global total
    status.text("กำลังบันทึก '%s' ..." % label)
    with open(PATH, "a") as f:            # "a" = append ต่อท้าย ไม่ลบของเก่า
        for _ in range(BURST):
            # เติม: อ่าน IMU หนึ่ง snapshot ครบ 6 แกนใต้ bus lock เดียว
            #       ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
            ax = ay = az = gx = gy = gz = 0.0
            pass
            # เติม: เขียน sample นี้เป็นหนึ่งบรรทัด (ต้องเรียงคอลัมน์ให้ตรง schema)
            #       f.write("%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n"
            #               % (label, ax, ay, az, gx, gy, gz))
            pass
            # เติม: เว้นจังหวะให้คงที่ เพื่อคุมอัตราสุ่มให้ ~50 Hz
            #       time.sleep_ms(RATE_MS)
            pass
    total += BURST
    count_lbl.text("บันทึกแล้ว: %d samples" % total)
    status.text("เสร็จ '%s' - เลือกท่าต่อไป" % label)
    lcd.console(" logged %d samples of '%s' -> %s" % (BURST, label, PATH))


try:
    while True:
        for ev in ui.poll():
            h = ev.get("handle")
            if h == back_id:
                raise KeyboardInterrupt
            for i, b in enumerate(btns):
                if h == b.id():
                    record(LABELS[i])
        time.sleep_ms(30)
except KeyboardInterrupt:
    pass
finally:
    lcd.console("<span class=ok> DAQ done: %d samples total in %s</span>" % (total, PATH))
    status.text("จบ - dataset อยู่ที่ %s" % PATH)

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
