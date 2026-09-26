# s04_daq_logger.py - เก็บข้อมูล sensor ลงไฟล์ CSV (Data Acquisition)
#
# นี่คือก้าวแรกของการทำ Edge AI จริง: ก่อนจะ train โมเดลได้ เราต้องมี "ข้อมูล"
# ก่อน โปรแกรมนี้อ่าน IMU ที่อัตราคงที่ แล้วเขียนลงไฟล์ CSV บนบอร์ด — ไฟล์นี้
# จะกลายเป็น dataset ที่เราเอาไป train ในโมดูล 5 (Training)
#
# รูปแบบไฟล์ (หนึ่งบรรทัดต่อหนึ่ง sample):
#   label,ax,ay,az,gx,gy,gz
# เราเลือก label ก่อนบันทึกแต่ละท่า (idle / circle / shaking) ให้ตรงกับโมเดล
# Motion บนบอร์ด เพื่อจะเปรียบเทียบกับของที่มีให้ได้
#
# วิธีเล่น: แตะปุ่ม label ที่ต้องการ แล้วทำท่านั้นค้างไว้ ~4 วินาที ระบบจะบันทึก
# ให้อัตโนมัติ ทำครบทุก label แล้วกด "< ออก" ไฟล์อยู่ที่ /gestures.csv

import ui, lcd, sensors, time

RATE_MS = 20            # 50 Hz — ตรงกับอัตราที่โมเดลบนบอร์ดกิน
BURST = 200            # จำนวน sample ต่อการกดหนึ่งครั้ง (~4 วินาที)
PATH = "/gestures.csv"
LABELS = ("idle", "circle", "shaking")

# สร้าง widget ครั้งเดียวก่อนลูป (แบบเดียวกับทุกตัวอย่างในคอร์ส)
ui.screen()
title = ui.Label("DAQ Logger - เก็บ dataset", x=20, y=10, color=0x71C7EC)
status = ui.Label("เลือก label แล้วทำท่าค้างไว้", x=20, y=44)
count_lbl = ui.Label("บันทึกแล้ว: 0 samples", x=20, y=76)
btns = []
for i, name in enumerate(LABELS):
    btns.append(ui.Button(name, x=20 + i * 130, y=120, w=120, h=54, color=0x50D890))
back = ui.Button("< ออก", x=20, y=320, w=120, h=48, color=0x2A1712)

# เขียนหัวตารางถ้าไฟล์ยังไม่มี
try:
    open(PATH, "r").close()
except OSError:
    with open(PATH, "w") as f:
        f.write("label,ax,ay,az,gx,gy,gz\n")

total = 0


def record(label):
    # บันทึก BURST samples ของ label นี้ลงไฟล์ ที่อัตรา RATE_MS
    global total
    status.text("กำลังบันทึก '%s' ..." % label)
    with open(PATH, "a") as f:
        for _ in range(BURST):
            ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
            f.write("%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n" % (label, ax, ay, az, gx, gy, gz))
            time.sleep_ms(RATE_MS)
    total += BURST
    count_lbl.text("บันทึกแล้ว: %d samples" % total)
    status.text("เสร็จ '%s' - เลือกท่าต่อไป" % label)
    lcd.console("logged %d samples of '%s' -> %s" % (BURST, label, PATH))


try:
    while True:
        for ev in ui.poll():
            h = ev.get("handle")
            if h == back.id():
                raise KeyboardInterrupt
            for i, b in enumerate(btns):
                if h == b.id():
                    record(LABELS[i])
        time.sleep_ms(30)
except KeyboardInterrupt:
    pass
finally:
    lcd.console("DAQ done: %d samples total in %s" % (total, PATH))
    status.text("จบ - dataset อยู่ที่ %s" % PATH)

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
