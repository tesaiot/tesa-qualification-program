# s06_physics_viz.py - Physics Lab: raw -> derived -> viz
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) กด "Program to Device" (หรือ Run บน Emulator)
#          3) เลือกปริมาณใน dropdown แล้วขยับ/ยกบอร์ด/ส่งเสียง
#          4) ดูค่าที่คำนวณได้ขึ้นจอ พร้อมแถบและกราฟย้อนหลัง
#
# เฉลยนี้ไม่ได้มีไว้ลอกวาง สิ่งที่นับคือการอธิบายด้วยคำพูดของคุณเอง
# อ่านให้เข้าใจว่า "สูตร" แต่ละบรรทัดแปลงตัวเลขดิบเป็นปริมาณอะไร ปิดไฟล์ แล้วพิมพ์เอง
# แก่นของชุดบทเรียนนี้คือ 4 สูตรแปลง: tilt (มุม) · energy (พลังงาน) · altitude (ความสูง) · dBFS (เสียง)
# ทุกสูตรเดินตามจังหวะเดียวกัน: อ่านค่าดิบ -> คำนวณเป็นปริมาณจริง -> ส่งขึ้นจอให้เห็น

import ui
ui.screen()
import lcd
import sensors
import dsp
import math
import time

# ธีมสีให้คุ้นตากับหน้าจอจริงบนบอร์ด
WHITE  = 0xFFFFFF
GREEN  = 0x50D890   # ค่าหลัก (headline)
CYAN   = 0x71C7EC   # สูตร/หน่วย
AMBER  = 0xFFAA44   # แถบ/ค่าที่กำลังขยับ
DIM    = 0x888888   # ข้อความรอง
CARD   = 0x1E1E28

# 4 ปริมาณที่เราจะคำนวณ (ชื่อโชว์ใน dropdown, สูตรย่อ, หน่วย)
VIEWS = (
    ("Tilt (IMU)",      "dsp.tilt(ax,ay,az) -> deg", "deg"),
    ("Energy (IMU)",    "|accel| - 1g",             "g"),
    ("Altitude (baro)", "dsp.altitude(p, p0)",      "m"),
    ("Sound dBFS (MIC)","20*log10(rms/32768)",      "dBFS"),
)

lcd.clear()
lcd.console('<h2> Physics Lab - raw -&gt; derived -&gt; viz</h2>')

# สร้าง widget ครั้งเดียวก่อนเข้าลูป — ถ้าสร้างซ้ำทุกวนรอบจะกินหน่วยความจำและจอกระพริบ
ui.Label("Physics Lab", x=20, y=8, color=WHITE)
dd = ui.Dropdown(text="\n".join(v[0] for v in VIEWS), x=20, y=42, w=280)

ui.Panel(x=20, y=92, w=360, h=210, color=CARD)
seg = ui.Seg7("--", x=44, y=120, color=GREEN)       # ค่าที่คำนวณได้ (headline)
unit = ui.Label("", x=44, y=210, color=CYAN)        # สูตร/หน่วยของปริมาณที่เลือก
bar = ui.Bar(x=44, y=250, w=312, h=16, min=0, max=100, value=0, color=AMBER)

ui.Label("ประวัติย้อนหลัง (normalized 0..100)", x=420, y=66, color=DIM)
chart = ui.Chart(x=420, y=90, w=352, h=210, min=0, max=100)

back = ui.Button("< ออก", x=570, y=352, w=120, h=36)
back_id = back.id()
dd_id = dd.id()

# ไมโครโฟน PDM มีเฉพาะบนบอร์ดจริง (Emulator ยังไม่จำลอง) — ตรวจก่อน ถ้าไม่มีก็ข้าม
# view "Sound" ให้ทำบนบอร์ด ส่วน 3 view แรกรันได้ทั้งบอร์ดและ Emulator
try:
    from machine import PDM_PCM
    import array
    pdm = PDM_PCM(0, sck="P8_5", data="P8_6", sample_rate=16000)
    mbuf = array.array("h", (0 for _ in range(1024)))
    has_mic = True
except Exception:
    has_mic = False
    lcd.console('<span class=warn> ไม่มีไมค์ PDM (Emulator) - view "Sound" ใช้บนบอร์ด</span>')

# ความดันอ้างอิงตอนเริ่ม ใช้เป็นจุด 0 เมตรของ altitude — ยิ่งสูงขึ้น ความดันยิ่งลดลง
# เราจึงวัด "ความสูงเทียบกับตอนเริ่ม" ได้ แม้ไม่รู้ความสูงสัมบูรณ์เหนือน้ำทะเล
try:
    p0, _ = sensors.dps368.pressure_temperature()
except Exception:
    p0 = 1013.25

sel = 0
unit.text(VIEWS[sel][1])
lcd.console(' เลือกปริมาณใน dropdown แล้วขยับ/ยกบอร์ด/ส่งเสียงเพื่อดูค่าเปลี่ยน')


def clamp100(x):
    """บีบค่าให้อยู่ในช่วง 0..100 เพื่อป้อนแถบ Bar และ Chart (ทั้งสองรับ 0..100)"""
    if x < 0:
        return 0
    if x > 100:
        return 100
    return int(x)


try:
    while True:
        head = "--"
        norm = 0

        if sel == 0:                                   # Tilt: มุมเอียงจากแรงโน้มถ่วง
            # accelerometer วัดเวกเตอร์แรงโน้มถ่วง dsp.tilt เอา atan2 ของแกนมาถอด
            # ออกเป็นมุม roll/pitch (องศา) ให้ — คำนวณฝั่ง C เร็วและแม่น
            ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
            roll, pitch = dsp.tilt(ax, ay, az)
            dom = pitch if abs(pitch) >= abs(roll) else roll  # โชว์แกนที่เอียงมากสุด
            head = "%d" % int(dom)
            norm = clamp100(abs(dom) / 90.0 * 100)     # 0..90 องศา -> 0..100

        elif sel == 1:                                 # Energy: ขนาดเวกเตอร์ความเร่ง
            # ตอนวางนิ่ง ขนาดเวกเตอร์ความเร่ง ~ 1g (แรงโน้มถ่วง) เราลบ 1g ออก
            # เหลือ "พลังงานส่วนเกิน" ที่เกิดจากการขยับจริง — ยิ่งเขย่าแรง ยิ่งสูง
            ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
            mag = math.sqrt(ax * ax + ay * ay + az * az) / 9.81   # motion() ให้ m/s² หาร 9.81 เป็น g
            energy = abs(mag - 1.0)
            head = "%.2f" % energy
            norm = clamp100(energy / 2.0 * 100)        # 0..2g -> 0..100

        elif sel == 2:                                 # Altitude: ฟิสิกส์ความดันบรรยากาศ
            # ความดันลดลงตามความสูงแบบ log dsp.altitude ใส่สูตรบรรยากาศมาตรฐานให้
            # ป้อน p0 (ความดันตอนเริ่ม) เป็นจุดอ้างอิง จะได้ความสูงเทียบกับตอนเริ่ม
            p, t = sensors.dps368.pressure_temperature()
            alt = dsp.altitude(p, p0)
            head = "%.1f" % alt
            norm = clamp100((alt + 5.0) / 10.0 * 100)  # โชว์ช่วง -5..+5 เมตรรอบจุดเริ่ม

        else:                                          # Sound dBFS: ระดับเสียงสเกล log
            if has_mic:
                # RMS = ค่ากลางกำลังสองของสัญญาณเสียง (ความ "ดัง" เชิงพลังงาน)
                pdm.readinto(mbuf)
                acc = 0
                for s in mbuf:
                    acc += s * s
                rms = math.sqrt(acc / len(mbuf))
                # dBFS = เทียบ RMS กับค่าเต็มสเกล (32768) แล้วแปลงเป็น decibel
                # หูคนรับรู้เสียงแบบ log สเกลนี้จึงตรงกับความรู้สึก "ดัง/เบา" จริง
                db = -96.0
                if rms > 0:
                    db = 20 * math.log10(rms / 32768.0)
                head = "%d" % int(db)
                norm = clamp100(db + 60.0)             # -60..0 dBFS -> 0..60
            else:
                head = "board"                         # ไม่มีไมค์บน Emulator
                norm = 0

        # raw -> derived เสร็จแล้ว ที่เหลือคือ viz: ส่งค่าเดียวกันไปสามที่
        seg.text(head)                                 # ตัวเลขใหญ่ (ค่าจริง + หน่วย)
        bar.value(norm)                                # แถบระดับ (normalized)
        bar.color(GREEN if norm >= 50 else AMBER)      # เขียวเมื่อค่าสูง ช่วยอ่านเร็ว
        chart.value(norm)                              # กราฟย้อนหลัง เห็นแนวโน้ม

        for ev in ui.poll():
            h = ev.get('handle')
            t = ev.get('type')
            if h == back_id:
                raise KeyboardInterrupt
            elif h == dd_id and t == 'value_changed':
                # เปลี่ยนปริมาณที่ดู — อัปเดตป้ายสูตร/หน่วย แล้วล้างค่าเก่า
                sel = ev.get('value')
                unit.text(VIEWS[sel][1])
                seg.text("--")
                lcd.console(' ปริมาณ: %s  [%s]' % (VIEWS[sel][0], VIEWS[sel][2]))

        time.sleep_ms(120)                             # ~8 Hz พอตาเห็นลื่น ไม่กิน CPU เปล่า
except KeyboardInterrupt:
    pass
finally:
    if has_mic:
        pdm.deinit()                                   # ออกจากงานยังไง คืนฮาร์ดแวร์ให้เรียบร้อยแบบนั้น
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
