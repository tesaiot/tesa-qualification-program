# s05_multicapture.py - เก็บ 2 เซนเซอร์พร้อมกันบนเส้นเวลาเดียว (ฉบับฝึกเติมโค้ด)
# วิธีรัน: 1) เปิดใน BENTO IDE แล้วเสียบบอร์ด BENTO AI Kit (ชุดบทเรียนนี้ต้องใช้บอร์ดจริง
#             เพราะ Emulator มีแค่เสียงสังเคราะห์ ไม่ใช่เสียงจริง)
#          2) เติมช่องว่าง (pass / None) ทั้ง 4 จุดตามคำใบ้ในคอมเมนต์ให้ครบ
#          3) กด "Program to Device" แล้วเลือก label กดปุ่มเพื่อเริ่มบันทึกหนึ่งชุด
#          4) ทำท่า + ส่งเสียงพร้อมกัน ~4 วินาที ดูจำนวนแถวขึ้นบนจอ
#          5) กด "< ออก" แล้วเปิดไฟล์ /multicapture.csv ดูว่าแต่ละแถวมีทั้ง IMU และ
#             ระดับเสียง (db) อยู่บน "เวลาเดียวกัน" (คอลัมน์ t_ms)
#
# ชุดบทเรียนก่อนหน้า (บทเรียน 2.1–2.2) เราเก็บ IMU อย่างเดียวลง CSV ชุดบทเรียนนี้เราเพิ่มไมโครโฟนเข้าไปอีกหนึ่งช่อง
# แล้ว "มัดสองสัญญาณให้อยู่บนเส้นเวลาเดียว" — นี่คือฐานของ dataset จริงที่ใช้ train
# โมเดลหลายเซนเซอร์ได้ต่อไป งานของเราคือเติม 4 จุดหลักของ loop เก็บข้อมูล

import ui
ui.screen()
import lcd
from machine import PDM_PCM
import sensors
import array, math, time

RATE_MS = 20                 # 50 Hz — หนึ่งแถวต่อ 20 มิลลิวินาที (ตรงอัตราโมเดล Motion)
BURST = 200                  # จำนวนแถวต่อการกดหนึ่งครั้ง (~4 วินาที)
CHUNK = 512                  # จำนวน sample เสียงต่อหนึ่งเฟรม
PATH = "/multicapture.csv"
LABELS = ("idle", "circle", "shaking")

CYAN  = 0x71C7EC
GREEN = 0x50D890
CARD  = 0x2A1712
RED   = 0xE85B5B

lcd.clear()
lcd.console('<h2> Multi-Sensor Capture - IMU + MIC บนเส้นเวลาเดียว</h2>')

# สร้าง widget ครั้งเดียวก่อนลูป (แบบเดียวกับทุกตัวอย่างในคอร์ส)
ui.Label("DAQ II - Sync Capture", x=20, y=10, color=CYAN)
status = ui.Label("เลือก label แล้วทำท่า + ส่งเสียงพร้อมกัน", x=20, y=44)
count_lbl = ui.Label("บันทึกแล้ว: 0 แถว", x=20, y=76)
ui.Panel(x=20, y=104, w=360, h=64, color=CARD)
level = ui.Bar(x=36, y=126, w=320, h=14, min=0, max=60, value=0, color=GREEN)  # 0..60 = -60..0 dBFS
btns = []
for i, name in enumerate(LABELS):
    btns.append(ui.Button(name, x=20 + i * 130, y=190, w=120, h=54, color=GREEN))
back = ui.Button("< ออก", x=20, y=320, w=120, h=48, color=CARD)
back_id = back.id()

# เปิดไมโครโฟน PDM หนึ่งครั้ง (คืน hardware ใน finally เสมอ)
pdm = PDM_PCM(0, sck="P8_5", data="P8_6", sample_rate=16000)
buf = array.array("h", (0 for _ in range(CHUNK)))

# เขียนหัวตารางถ้าไฟล์ยังไม่มี — สังเกตคอลัมน์แรกคือ t_ms = เส้นเวลาร่วม
try:
    open(PATH, "r").close()
except OSError:
    with open(PATH, "w") as f:
        f.write("t_ms,label,ax,ay,az,gx,gy,gz,db\n")

total = 0


def dbfs(chunk):
    """แปลงหนึ่งเฟรมเสียงเป็นระดับ dBFS (ให้ไว้แล้ว) — RMS แล้วเทียบ full-scale"""
    acc = 0
    for s in chunk:
        acc += s * s
    rms = math.sqrt(acc / len(chunk))
    return 20 * math.log10(rms / 32768) if rms > 0 else -96.0


def record(label):
    """บันทึก BURST แถวของ label นี้ โดยแต่ละแถวมีทั้ง IMU และระดับเสียงบนเวลาเดียวกัน"""
    global total
    status.text("กำลังบันทึก '%s' ..." % label)
    status.color(RED)
    t0 = time.ticks_ms()                     # จุดศูนย์ของเส้นเวลาชุดนี้
    with open(PATH, "a") as f:
        for _ in range(BURST):
            # เติม 1: ประทับเวลาของแถวนี้เทียบ t0 (เส้นเวลาร่วมของทุกเซนเซอร์)
            #         t_ms = time.ticks_diff(time.ticks_ms(), t0)
            t_ms = 0
            pass

            # เติม 2: อ่านเซนเซอร์ตัวที่หนึ่ง (IMU 6 แกน) ให้ครบทั้ง 6 ค่า
            #         ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
            ax = ay = az = gx = gy = gz = 0.0
            pass

            # เติม 3: อ่านเซนเซอร์ตัวที่สอง (เสียง) หนึ่งเฟรมเข้า buf ด้วย pdm.readinto(buf)
            pass
            db = dbfs(buf)

            # เติม 4: เขียนหนึ่งแถวที่มัดสองเซนเซอร์ไว้ด้วย t_ms เดียวกัน
            #   f.write("%d,%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.1f\n"
            #           % (t_ms, label, ax, ay, az, gx, gy, gz, db))
            pass

            level.value(max(0, int(db + 60)))
            time.sleep_ms(RATE_MS)
    total += BURST
    count_lbl.text("บันทึกแล้ว: %d แถว" % total)
    status.text("เสร็จ '%s' - เลือกท่าต่อไป" % label)
    status.color(GREEN)
    lcd.console("logged %d rows of '%s' -> %s" % (BURST, label, PATH))


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
    pdm.deinit()                             # คืนไมโครโฟนให้ระบบเสมอ
    lcd.console("<span class=ok> จบ: %d แถวใน %s</span>" % (total, PATH))
    status.text("จบ - dataset อยู่ที่ %s" % PATH)

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
