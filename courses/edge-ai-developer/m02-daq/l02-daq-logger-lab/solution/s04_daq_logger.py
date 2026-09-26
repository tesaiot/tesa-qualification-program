# s04_daq_logger.py - เก็บข้อมูล sensor ลงไฟล์ CSV (Data Acquisition)
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) กด "Program to Device"
#          3) แตะปุ่ม label (idle / circle / shaking) แล้วทำท่านั้นค้างไว้ ~4 วินาที
#          4) ทำครบทุก label แล้วกด "< ออก" ไฟล์ dataset อยู่ที่ /gestures.csv
#
# เฉลยนี้ไม่ได้มีไว้ลอกวาง สิ่งที่นับคือการอธิบายด้วยคำพูดของคุณเอง
# อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์ใหม่ด้วยมือ ตอนพิมพ์เองนั่นแหละสมองจะจำ pattern
# ของ DAQ ได้: ทั้งไฟล์ยืนอยู่บนสี่จังหวะ schema -> sample -> record -> rate
#
# ทำไมชุดบทเรียนนี้ถึงสำคัญ: โมเดล Edge AI ทุกตัวเกิดจาก "ข้อมูล" ที่มีคนเก็บมาก่อน
# วันนี้เราเป็นคนเก็บเอง แล้วจะเห็นว่า dataset ไม่ใช่ของวิเศษ มันคือไฟล์ CSV
# ธรรมดาที่เราเขียนทีละบรรทัด ด้วยเซนเซอร์จริงบนบอร์ดจริง

import ui
ui.screen()                       # เคลียร์จอ + เตรียม canvas 792x398
import lcd
import sensors
import time

RATE_MS = 20                      # 50 Hz - ตรงกับอัตราที่โมเดล Motion บนบอร์ดกิน
BURST   = 200                     # จำนวน sample ต่อการกดหนึ่งครั้ง (~4 วินาที ที่ 50 Hz)
PATH    = "/gestures.csv"
LABELS  = ("idle", "circle", "shaking")   # ให้ตรงกับคลาสของโมเดล Motion เป๊ะ

# ธีมสีให้คุ้นตากับหน้าจออื่นในคอร์ส
CYAN  = 0x71C7EC
GREEN = 0x50D890
DARK  = 0x2A1712
SEC   = 0xCFC6BF

lcd.clear()
lcd.console('<h2> DAQ Logger - เก็บ dataset ลง CSV</h2>')

# ---- สร้าง widget ครั้งเดียวก่อนลูป ----
# สร้างครั้งเดียวแล้วในลูปแค่ "แก้ค่า" เป็นนิสัยที่เราใช้ทั้งคอร์ส ประหยัดแรมและจอไม่กระพริบ
ui.Label("DAQ Logger", x=20, y=10, color=CYAN)
status    = ui.Label("เลือก label แล้วทำท่าค้างไว้", x=20, y=44, color=SEC)
count_lbl = ui.Label("บันทึกแล้ว: 0 samples", x=20, y=76, color=GREEN)
btns = []
for i, name in enumerate(LABELS):
    btns.append(ui.Button(name, x=20 + i * 130, y=120, w=120, h=54, color=GREEN))
back = ui.Button("< ออก", x=20, y=320, w=120, h=48, color=DARK)
back_id = back.id()

# บรรทัดแรกของ CSV คือ "หัวตาราง" (schema) - บอกว่าแต่ละคอลัมน์คืออะไร เขียนครั้งเดียว
# พอเท่านั้น ถ้าไฟล์มีอยู่แล้วเราจะ append ต่อ ไม่เขียนหัวซ้ำ (ไม่งั้น dataset จะเสีย)
try:
    open(PATH, "r").close()       # เปิดอ่านได้ = ไฟล์มีอยู่แล้ว ข้ามการเขียนหัว
except OSError:
    with open(PATH, "w") as f:    # ยังไม่มีไฟล์ -> สร้างใหม่พร้อมหัวตาราง
        f.write("label,ax,ay,az,gx,gy,gz\n")

total = 0


def record(label):
    """บันทึก BURST samples ของ label นี้ต่อท้ายไฟล์ ที่อัตรา RATE_MS คงที่"""
    global total
    status.text("กำลังบันทึก '%s' ..." % label)
    # เปิดไฟล์แบบ "a" (append) ครั้งเดียวต่อ burst แล้วเขียนรวดเดียว - เร็วกว่าเปิด/ปิดทุก sample
    with open(PATH, "a") as f:
        for _ in range(BURST):
            # sample: อ่าน IMU ครบ 6 แกนใน snapshot เดียว (motion() อ่านใต้ bus lock เดียว
            # เวลาของทุกแกนจึงตรงกัน - สำคัญมากตอนเอาไป train)
            ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
            # record: เขียนหนึ่ง sample = หนึ่งบรรทัด เรียงคอลัมน์ให้ตรง schema เป๊ะ
            # %.4f = เก็บทศนิยม 4 ตำแหน่ง พอสำหรับ IMU และไม่ทำให้ไฟล์ใหญ่เกิน
            f.write("%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n"
                    % (label, ax, ay, az, gx, gy, gz))
            # rate: เว้นจังหวะให้คงที่ คุมอัตราสุ่มให้ ~50 Hz - ต้องตรงกับที่โมเดลกิน
            time.sleep_ms(RATE_MS)
    total += BURST
    count_lbl.text("บันทึกแล้ว: %d samples" % total)
    status.text("เสร็จ '%s' - เลือกท่าต่อไป" % label)
    lcd.console(" logged %d samples of '%s' -> %s" % (BURST, label, PATH))


try:
    while True:
        for ev in ui.poll():          # poll ครั้งเดียวต่อรอบ รับการแตะปุ่ม
            h = ev.get("handle")
            if h == back_id:
                raise KeyboardInterrupt
            for i, b in enumerate(btns):
                if h == b.id():
                    record(LABELS[i])
        time.sleep_ms(30)             # ระหว่างรอการกด ไม่รัด CPU เปล่า
except KeyboardInterrupt:
    pass
finally:
    # ออกจากงานยังไง ทิ้งไว้ให้เรียบร้อยแบบนั้น - สรุปยอดที่เก็บได้ให้ผู้ใช้เห็น
    lcd.console("<span class=ok> DAQ done: %d samples total in %s</span>" % (total, PATH))
    status.text("จบ - dataset อยู่ที่ %s" % PATH)

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
