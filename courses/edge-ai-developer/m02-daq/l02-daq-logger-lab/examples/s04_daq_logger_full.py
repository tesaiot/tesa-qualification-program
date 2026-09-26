# s04_daq_logger_full.py - เก็บ dataset ลง CSV (ฉบับเต็ม)
# วิธีรัน: เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator (ide.tesaiot.dev)
#          กด "Program to Device" แล้วแตะปุ่ม label ทำท่านั้นค้างไว้จนแถบเต็ม
#
# ฉบับนี้คือเวอร์ชันที่ขัดจนเรียบร้อยของ s04_daq_logger.py - โครงสี่จังหวะเดียวกัน
# (schema -> sample -> record -> rate) แต่เพิ่มรายละเอียดที่ทำให้ "เก็บ dataset ได้ดีขึ้น":
#   - นับ sample แยกต่อ label เพื่อดู class balance (แต่ละท่าเก็บพอๆ กันไหม)
#   - วัด "อัตราสุ่มจริง" ด้วย time.ticks - จะเห็นว่า sleep_ms ไม่ได้เป๊ะ 50 Hz
#   - แถบ progress ระหว่างบันทึก + ปุ่ม Clear ล้างไฟล์เริ่มใหม่
# ทั้งหมดยังยืนบนเซนเซอร์จริงและไฟล์ CSV ธรรมดาบรรทัดต่อบรรทัด

import ui
ui.screen()
import lcd
import sensors
import time
import os

RATE_MS = 20                      # 50 Hz - ตรงกับอัตราที่โมเดล Motion บนบอร์ดกิน
BURST   = 200                     # sample ต่อการกดหนึ่งครั้ง (~4 วินาที ที่ 50 Hz)
PATH    = "/gestures.csv"
HEADER  = "label,ax,ay,az,gx,gy,gz\n"
LABELS  = ("idle", "circle", "shaking")

CYAN  = 0x71C7EC
GREEN = 0x50D890
AMBER = 0xE0A03A
DARK  = 0x2A1712
SEC   = 0xCFC6BF

lcd.clear()
lcd.console('<h2> DAQ Logger - เก็บ dataset (ฉบับเต็ม)</h2>')


def ensure_header():
    """เขียนหัวตาราง (schema) ถ้าไฟล์ยังไม่มี - เรียกได้ซ้ำอย่างปลอดภัย"""
    try:
        open(PATH, "r").close()
    except OSError:
        with open(PATH, "w") as f:
            f.write(HEADER)


ensure_header()

# ---- สร้าง widget ครั้งเดียวก่อนลูป ----
ui.Label("DAQ Logger", x=20, y=10, color=CYAN)
status    = ui.Label("เลือก label แล้วทำท่าค้างไว้", x=20, y=44, color=SEC)
count_lbl = ui.Label("รวม: 0 samples", x=20, y=76, color=GREEN)
rate_lbl  = ui.Label("อัตราจริง: -- Hz", x=300, y=76, color=CYAN)

btns = []
per_lbl = []          # ป้ายนับ sample แยกต่อ label (ดู class balance)
for i, name in enumerate(LABELS):
    x = 20 + i * 170
    btns.append(ui.Button(name, x=x, y=120, w=160, h=54, color=GREEN))
    per_lbl.append(ui.Label("%s: 0" % name, x=x, y=182, color=SEC))

prog = ui.Bar(x=20, y=224, w=510, h=16, min=0, max=BURST, value=0, color=AMBER)
btn_clear = ui.Button("Clear file", x=20, y=320, w=150, h=48, color=DARK)
back      = ui.Button("< ออก", x=190, y=320, w=150, h=48, color=DARK)
back_id   = back.id()
clear_id  = btn_clear.id()

counts = {name: 0 for name in LABELS}
total  = 0


def record(label):
    """บันทึก BURST samples ของ label นี้ พร้อมวัดอัตราสุ่มจริงและอัปเดต progress"""
    global total
    status.text("กำลังบันทึก '%s' ..." % label)
    t0 = time.ticks_ms()
    with open(PATH, "a") as f:
        for k in range(BURST):
            ax, ay, az, gx, gy, gz = sensors.bmi270.motion()   # sample: 6 แกน snapshot เดียว
            f.write("%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n"        # record: หนึ่งบรรทัดต่อ sample
                    % (label, ax, ay, az, gx, gy, gz))
            time.sleep_ms(RATE_MS)                              # rate: คุมจังหวะให้คงที่
            if k % 10 == 0:
                prog.value(k)
    prog.value(BURST)
    # อัตราสุ่มจริง = จำนวน sample หารด้วยเวลาที่ใช้จริง (มักต่ำกว่า 50 Hz เล็กน้อย
    # เพราะ sleep_ms + เวลาอ่านเซนเซอร์ + เวลาเขียนไฟล์ รวมกันแล้วเกิน 20 ms/รอบ)
    dt_ms = time.ticks_diff(time.ticks_ms(), t0)
    hz = (BURST * 1000.0) / dt_ms if dt_ms > 0 else 0.0
    counts[label] += BURST
    total += BURST
    count_lbl.text("รวม: %d samples" % total)
    rate_lbl.text("อัตราจริง: %.1f Hz" % hz)
    for i, name in enumerate(LABELS):
        per_lbl[i].text("%s: %d" % (name, counts[name]))
    status.text("เสร็จ '%s' (%.1f Hz) - เลือกท่าต่อไป" % (label, hz))
    lcd.console(" logged %d '%s' @ %.1f Hz -> %s" % (BURST, label, hz, PATH))
    prog.value(0)


def clear_file():
    """ล้างไฟล์เริ่มเก็บใหม่ - ใช้ตอนเก็บผิด label หรืออยากเริ่มรอบใหม่"""
    global total
    try:
        os.remove(PATH)
    except OSError:
        pass
    ensure_header()
    total = 0
    for name in LABELS:
        counts[name] = 0
    for i, name in enumerate(LABELS):
        per_lbl[i].text("%s: 0" % name)
    count_lbl.text("รวม: 0 samples")
    rate_lbl.text("อัตราจริง: -- Hz")
    status.text("ล้างไฟล์แล้ว - เริ่มเก็บใหม่ได้")
    lcd.console("<span class=ok> cleared %s</span>" % PATH)


try:
    while True:
        for ev in ui.poll():
            h = ev.get("handle")
            if h == back_id:
                raise KeyboardInterrupt
            elif h == clear_id:
                clear_file()
            else:
                for i, b in enumerate(btns):
                    if h == b.id():
                        record(LABELS[i])
        time.sleep_ms(30)
except KeyboardInterrupt:
    pass
finally:
    lcd.console("<span class=ok> DAQ done: %d samples total in %s</span>" % (total, PATH))
    status.text("จบ - dataset อยู่ที่ %s (%d samples)" % (PATH, total))

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
