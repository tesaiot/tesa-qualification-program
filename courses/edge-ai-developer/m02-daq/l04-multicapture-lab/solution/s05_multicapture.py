# s05_multicapture.py - เก็บ 2 เซนเซอร์พร้อมกันบนเส้นเวลาเดียว (เฉลย)
# วิธีรัน: 1) เปิดใน BENTO IDE แล้วเสียบบอร์ด BENTO AI Kit (ชุดบทเรียนนี้ต้องใช้บอร์ดจริง
#             เพราะ Emulator มีแค่เสียงสังเคราะห์ ไม่ใช่เสียงจริง)
#          2) กด "Program to Device"
#          3) เลือก label กดปุ่มเพื่อบันทึกหนึ่งชุด ทำท่า + ส่งเสียงพร้อมกัน ~4 วินาที
#          4) กด "< ออก" แล้วเปิด /multicapture.csv ดูว่าทุกแถวมี IMU + db บน t_ms เดียวกัน
#
# เฉลยนี้ไม่ได้มีไว้ลอกวาง — สิ่งที่นับคือการที่คุณอธิบายได้ว่า "เส้นเวลาร่วม"
# คืออะไร ทำไมสองเซนเซอร์ต้องแชร์ t_ms เดียวกัน อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์ใหม่ด้วยมือ
# หัวใจของชุดบทเรียนนี้มีแค่สี่ก้าวในลูป: ประทับเวลา -> อ่าน IMU -> อ่าน MIC -> เขียนหนึ่งแถว

import ui
ui.screen()
import lcd
from machine import PDM_PCM
import sensors
import array, math, time

RATE_MS = 20                 # 50 Hz — หนึ่งแถวต่อ 20 มิลลิวินาที (ตรงอัตราโมเดล Motion บนบอร์ด)
BURST = 200                  # จำนวนแถวต่อการกดหนึ่งครั้ง (~4 วินาที) พอให้เห็นท่าครบจังหวะ
CHUNK = 512                  # จำนวน sample เสียงต่อหนึ่งเฟรม — เล็กพอให้ loop ตามอัตรา IMU ทัน
PATH = "/multicapture.csv"
LABELS = ("idle", "circle", "shaking")

CYAN  = 0x71C7EC
GREEN = 0x50D890
CARD  = 0x2A1712
RED   = 0xE85B5B

lcd.clear()
lcd.console('<h2> Multi-Sensor Capture - IMU + MIC บนเส้นเวลาเดียว</h2>')

# สร้าง widget ครั้งเดียวก่อนลูป — ถ้าสร้างซ้ำทุกวนรอบจะกินหน่วยความจำและจอกระพริบ
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

# เปิดไมโครโฟน PDM หนึ่งครั้งก่อนลูป แล้วคืน hardware ใน finally เสมอ (นิสัย embedded)
pdm = PDM_PCM(0, sck="P8_5", data="P8_6", sample_rate=16000)
buf = array.array("h", (0 for _ in range(CHUNK)))

# เขียนหัวตารางถ้าไฟล์ยังไม่มี — คอลัมน์แรกคือ t_ms คือ "เส้นเวลาร่วม" ที่มัดทุกเซนเซอร์ไว้
try:
    open(PATH, "r").close()
except OSError:
    with open(PATH, "w") as f:
        f.write("t_ms,label,ax,ay,az,gx,gy,gz,db\n")

total = 0


def dbfs(chunk):
    """แปลงหนึ่งเฟรมเสียงเป็นระดับ dBFS — หา RMS ของบล็อกแล้วเทียบกับ full-scale (32768)"""
    acc = 0
    for s in chunk:
        acc += s * s
    rms = math.sqrt(acc / len(chunk))
    return 20 * math.log10(rms / 32768) if rms > 0 else -96.0


def record(label):
    """บันทึก BURST แถวของ label นี้ แต่ละแถวมัด IMU + ระดับเสียงไว้บน t_ms เดียวกัน"""
    global total
    status.text("กำลังบันทึก '%s' ..." % label)
    status.color(RED)
    t0 = time.ticks_ms()                     # จุดศูนย์ของเส้นเวลาชุดนี้ — ทุกแถวนับจากตรงนี้
    with open(PATH, "a") as f:
        for _ in range(BURST):
            # ก้าวที่ 1: ประทับเวลาของแถวนี้เทียบ t0 — นี่คือ "เส้นเวลาร่วม" ที่ทำให้ค่า
            # IMU กับค่าเสียงในแถวเดียวกัน "หมายถึงเวลาเดียวกัน" ticks_diff กัน wrap-around ให้
            t_ms = time.ticks_diff(time.ticks_ms(), t0)

            # ก้าวที่ 2: อ่านเซนเซอร์ตัวที่หนึ่ง — IMU 6 แกน (accel 3 + gyro 3) พร้อมกันทีเดียว
            ax, ay, az, gx, gy, gz = sensors.bmi270.motion()

            # ก้าวที่ 3: อ่านเซนเซอร์ตัวที่สอง — ดึงเสียงหนึ่งเฟรมเข้า buf แล้วย่อเป็น dBFS
            # อ่านสองเซนเซอร์ติดกันในรอบเดียว จึงถือว่าเป็น "ช่วงเวลาเดียวกัน" ของแถวนี้
            pdm.readinto(buf)
            db = dbfs(buf)

            # ก้าวที่ 4: เขียนหนึ่งแถวที่รวมทั้งสองเซนเซอร์ไว้ด้วย t_ms ร่วม — นี่คือ dataset base
            f.write("%d,%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.1f\n"
                    % (t_ms, label, ax, ay, az, gx, gy, gz, db))

            level.value(max(0, int(db + 60)))    # โชว์ระดับเสียงสดๆ ระหว่างอัด
            time.sleep_ms(RATE_MS)               # คุมจังหวะให้ใกล้ 50 Hz
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
    pdm.deinit()                             # ออกจากงานยังไง ทิ้งไมโครโฟนไว้ให้เรียบร้อยแบบนั้น
    lcd.console("<span class=ok> จบ: %d แถวใน %s</span>" % (total, PATH))
    status.text("จบ - dataset อยู่ที่ %s" % PATH)

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
