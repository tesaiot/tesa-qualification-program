# s06_physics_viz.py - Physics Lab: raw -> derived -> viz (ฉบับฝึกเติมโค้ด)
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) เติมช่องว่าง (pass) ทั้ง 4 จุดตามคำใบ้ในคอมเมนต์ให้ครบ
#          3) กด "Program to Device" (หรือ Run บน Emulator)
#          4) เลือกปริมาณใน dropdown แล้วขยับ/ยกบอร์ด/ส่งเสียง ดูค่าที่ "คำนวณเอง"
#             ขึ้นจอ พร้อมแถบและกราฟย้อนหลัง
#
# ชุดบทเรียนนี้อยู่ในขั้น Processing ของวงจรชีวิตข้อมูล เซนเซอร์ให้ "ตัวเลขดิบ" มา แต่ตัวเลข
# ดิบยังไม่พูดภาษาคน เราต้องเอาคณิต+ฟิสิกส์ไปแปลงมันเป็น "ปริมาณที่มีความหมาย":
# มุมเอียง (tilt) · พลังงานการเคลื่อนไหว (energy) · ความสูง (altitude) · ระดับเสียง (dBFS)
# งานของคุณคือเติมสูตรแปลงทั้ง 4 จุด — หัวใจของชุดบทเรียนนี้อยู่ตรงบรรทัดที่คุณเติมนี่แหละ

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

# สร้าง widget ครั้งเดียวก่อนเข้าลูป (สร้างซ้ำในลูปจะกินหน่วยความจำและจอกระพริบ)
ui.Label("Physics Lab", x=20, y=8, color=WHITE)
dd = ui.Dropdown(text="\n".join(v[0] for v in VIEWS), x=20, y=42, w=280)

ui.Panel(x=20, y=92, w=360, h=210, color=CARD)
seg = ui.Seg7("--", x=44, y=120, color=GREEN)       # ค่าที่คำนวณได้ (headline)
unit = ui.Label("", x=44, y=210, color=CYAN)        # สูตร/หน่วยของปริมาณที่เลือก
bar = ui.Bar(x=44, y=250, w=312, h=16, min=0, max=100, value=0, color=AMBER)

ui.Label("ประวัติย้อนหลัง (normalized 0..100)", x=420, y=66, color=DIM)
chart = ui.Chart(x=420, y=90, w=352, h=210, min=0, max=100)

back = ui.Button("< ออก", x=650, y=352, w=120, h=36)
back_id = back.id()
dd_id = dd.id()

# ไมโครโฟน PDM มีเฉพาะบนบอร์ดจริง (Emulator ยังไม่จำลอง) — ตรวจก่อน ถ้าไม่มีก็ข้าม
try:
    from machine import PDM_PCM
    import array
    pdm = PDM_PCM(0, sck="P8_5", data="P8_6", sample_rate=16000)
    mbuf = array.array("h", (0 for _ in range(1024)))
    has_mic = True
except Exception:
    has_mic = False
    lcd.console('<span class=warn> ไม่มีไมค์ PDM (Emulator) - view "Sound" ใช้บนบอร์ด</span>')

# ความดันอ้างอิงตอนเริ่ม ใช้เป็นจุด 0 เมตรของ altitude (สูงขึ้น = ความดันลดลง)
try:
    p0, _ = sensors.dps368.pressure_temperature()
except Exception:
    p0 = 1013.25

sel = 0
unit.text(VIEWS[sel][1])
lcd.console(' เลือกปริมาณใน dropdown แล้วขยับ/ยกบอร์ด/ส่งเสียงเพื่อดูค่าเปลี่ยน')


def clamp100(x):
    """บีบค่าให้อยู่ในช่วง 0..100 เพื่อป้อนแถบ Bar และ Chart"""
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
            ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
            # เติม: มุมเอียงจาก accelerometer -> roll, pitch = dsp.tilt(ax, ay, az)
            roll, pitch = 0.0, 0.0
            pass
            dom = pitch if abs(pitch) >= abs(roll) else roll
            head = "%d" % int(dom)
            norm = clamp100(abs(dom) / 90.0 * 100)

        elif sel == 1:                                 # Energy: ขนาดเวกเตอร์ความเร่ง
            ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
            # เติม: พลังงานการเคลื่อนไหว = ขนาดเวกเตอร์ความเร่ง ลบฐาน 1g
            #       mag = math.sqrt(ax*ax + ay*ay + az*az) / 9.81 ; energy = abs(mag - 1.0)
            energy = 0.0
            pass
            head = "%.2f" % energy
            norm = clamp100(energy / 2.0 * 100)

        elif sel == 2:                                 # Altitude: ฟิสิกส์ความดันบรรยากาศ
            p, t = sensors.dps368.pressure_temperature()
            # เติม: ความสูงจากความดัน เทียบกับความดันอ้างอิง p0 -> alt = dsp.altitude(p, p0)
            alt = 0.0
            pass
            head = "%.1f" % alt
            norm = clamp100((alt + 5.0) / 10.0 * 100)  # โชว์ช่วง -5..+5 เมตรรอบจุดเริ่ม

        else:                                          # Sound dBFS: ระดับเสียงสเกล log
            if has_mic:
                pdm.readinto(mbuf)
                acc = 0
                for s in mbuf:
                    acc += s * s
                rms = math.sqrt(acc / len(mbuf))
                # เติม: แปลง RMS เป็น dBFS (สเกล log) -> db = 20 * math.log10(rms / 32768.0)
                db = -96.0
                if rms > 0:
                    pass
                head = "%d" % int(db)
                norm = clamp100(db + 60.0)             # -60..0 dBFS -> 0..60
            else:
                head = "board"
                norm = 0

        seg.text(head)
        bar.value(norm)
        bar.color(GREEN if norm >= 50 else AMBER)
        chart.value(norm)

        for ev in ui.poll():
            h = ev.get('handle')
            t = ev.get('type')
            if h == back_id:
                raise KeyboardInterrupt
            elif h == dd_id and t == 'value_changed':
                sel = ev.get('value')
                unit.text(VIEWS[sel][1])
                seg.text("--")
                lcd.console(' ปริมาณ: %s  [%s]' % (VIEWS[sel][0], VIEWS[sel][2]))

        time.sleep_ms(120)
except KeyboardInterrupt:
    pass
finally:
    if has_mic:
        pdm.deinit()                                   # คืน hardware ไมค์เสมอ
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
