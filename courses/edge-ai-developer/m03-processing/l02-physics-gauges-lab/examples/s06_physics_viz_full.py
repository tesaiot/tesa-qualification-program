# s06_physics_viz_full.py - Physics Lab: raw -> derived -> viz (ฉบับเต็ม)
# วิธีรัน: เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator (ide.tesaiot.dev)
#          กด "Program to Device" แล้วเลือกปริมาณใน dropdown
#
# ฉบับนี้คือเวอร์ชันที่ขัดจนเรียบร้อยของ s06_physics_viz.py — โครงและ 4 สูตรแปลง
# เหมือนไฟล์ฝึกทุกบรรทัด แต่เพิ่มสิ่งที่ทำให้ "อ่านค่าได้แม่นขึ้น": จำค่าสูงสุด/ต่ำสุด
# (hi/lo hold), ป้ายบอกสถานะ STEADY/ACTIVE ตามระดับ และปุ่ม Reset ล้างสถิติ
# ทั้งหมดยังยืนอยู่บนแก่นเดียวกัน: อ่านค่าดิบ -> คำนวณเป็นปริมาณจริง -> ส่งขึ้นจอ

import ui
ui.screen()
import lcd
import sensors
import dsp
import math
import time

WHITE  = 0xFFFFFF
GREEN  = 0x50D890   # ค่าหลัก + สถานะ ACTIVE
CYAN   = 0x71C7EC   # สูตร/หน่วย
AMBER  = 0xFFAA44   # แถบ + สถานะ STEADY
DIM    = 0x888888   # ข้อความรอง
CARD   = 0x1E1E28

# 4 ปริมาณ: (ชื่อ dropdown, สูตรย่อ, หน่วย, ระดับที่ถือว่า "ACTIVE" บนสเกล 0..100)
VIEWS = (
    ("Tilt (IMU)",      "dsp.tilt(ax,ay,az) -> deg", "deg",  30),
    ("Energy (IMU)",    "|accel| - 1g",             "g",    25),
    ("Altitude (baro)", "dsp.altitude(p, p0)",      "m",    60),
    ("Sound dBFS (MIC)","20*log10(rms/32768)",      "dBFS", 45),
)

lcd.clear()
lcd.console('<h2> Physics Lab - raw -&gt; derived -&gt; viz (ฉบับเต็ม)</h2>')

ui.Label("Physics Lab", x=20, y=8, color=WHITE)
dd = ui.Dropdown(text="\n".join(v[0] for v in VIEWS), x=20, y=42, w=250)
btn_reset = ui.Button("Reset", x=285, y=42, w=90, h=36)
state = ui.Label("STEADY", x=490, y=50, color=AMBER)

ui.Panel(x=20, y=92, w=360, h=210, color=CARD)
seg = ui.Seg7("--", x=44, y=120, color=GREEN)       # ค่าที่คำนวณได้ (headline)
unit = ui.Label("", x=44, y=206, color=CYAN)        # สูตร/หน่วยของปริมาณที่เลือก
hilo = ui.Label("hi/lo: -- / --", x=44, y=230, color=DIM)
bar = ui.Bar(x=44, y=258, w=312, h=16, min=0, max=100, value=0, color=AMBER)

ui.Label("ประวัติย้อนหลัง (normalized 0..100)", x=420, y=66, color=DIM)
chart = ui.Chart(x=420, y=90, w=352, h=210, min=0, max=100)

back = ui.Button("< ออก", x=570, y=352, w=120, h=36)
back_id = back.id()
dd_id = dd.id()
reset_id = btn_reset.id()

# ไมโครโฟน PDM มีเฉพาะบนบอร์ดจริง (Emulator ยังไม่จำลอง)
try:
    from machine import PDM_PCM
    import array
    pdm = PDM_PCM(0, sck="P8_5", data="P8_6", sample_rate=16000)
    mbuf = array.array("h", (0 for _ in range(1024)))
    has_mic = True
except Exception:
    has_mic = False
    lcd.console('<span class=warn> ไม่มีไมค์ PDM (Emulator) - view "Sound" ใช้บนบอร์ด</span>')

try:
    p0, _ = sensors.dps368.pressure_temperature()
except Exception:
    p0 = 1013.25

sel = 0
hi = -1e9
lo = 1e9


def clamp100(x):
    """บีบค่าให้อยู่ในช่วง 0..100 เพื่อป้อนแถบ Bar และ Chart"""
    if x < 0:
        return 0
    if x > 100:
        return 100
    return int(x)


def reset_stats():
    """ล้างสถิติ hi/lo (ใช้ตอนสลับปริมาณ หรือกดปุ่ม Reset)"""
    global hi, lo
    hi = -1e9
    lo = 1e9
    hilo.text("hi/lo: -- / --")
    seg.text("--")


unit.text(VIEWS[sel][1])
lcd.console(' เลือกปริมาณใน dropdown แล้วขยับ/ยกบอร์ด/ส่งเสียงเพื่อดูค่าเปลี่ยน')

try:
    while True:
        val = None      # ค่าจริง (มีหน่วย) สำหรับ hi/lo
        head = "--"
        norm = 0

        if sel == 0:                                   # Tilt: มุมเอียงจากแรงโน้มถ่วง
            ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
            roll, pitch = dsp.tilt(ax, ay, az)
            val = pitch if abs(pitch) >= abs(roll) else roll
            head = "%d" % int(val)
            norm = clamp100(abs(val) / 90.0 * 100)

        elif sel == 1:                                 # Energy: ขนาดเวกเตอร์ความเร่ง - 1g
            ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
            mag = math.sqrt(ax * ax + ay * ay + az * az) / 9.81   # motion() ให้ m/s² หาร 9.81 เป็น g
            val = abs(mag - 1.0)
            head = "%.2f" % val
            norm = clamp100(val / 2.0 * 100)

        elif sel == 2:                                 # Altitude: ฟิสิกส์ความดันบรรยากาศ
            p, t = sensors.dps368.pressure_temperature()
            val = dsp.altitude(p, p0)
            head = "%.1f" % val
            norm = clamp100((val + 5.0) / 10.0 * 100)

        else:                                          # Sound dBFS: ระดับเสียงสเกล log
            if has_mic:
                pdm.readinto(mbuf)
                acc = 0
                for s in mbuf:
                    acc += s * s
                rms = math.sqrt(acc / len(mbuf))
                val = 20 * math.log10(rms / 32768.0) if rms > 0 else -96.0
                head = "%d" % int(val)
                norm = clamp100(val + 60.0)
            else:
                head = "board"
                norm = 0

        # viz: ค่าเดียวไปสามที่ + ป้ายสถานะ + สถิติ hi/lo
        seg.text(head)
        bar.value(norm)
        active = norm >= VIEWS[sel][3]
        bar.color(GREEN if active else AMBER)
        chart.value(norm)
        state.text("ACTIVE" if active else "STEADY")
        state.color(GREEN if active else AMBER)

        if val is not None:
            if val > hi:
                hi = val
            if val < lo:
                lo = val
            hilo.text("hi/lo: %s / %s" % (
                ("%.1f" % hi if abs(hi) < 1e8 else "--"),
                ("%.1f" % lo if abs(lo) < 1e8 else "--")))

        for ev in ui.poll():
            h = ev.get('handle')
            t = ev.get('type')
            if h == back_id:
                raise KeyboardInterrupt
            elif h == reset_id:
                reset_stats()
                lcd.console(' ล้างสถิติ hi/lo')
            elif h == dd_id and t == 'value_changed':
                sel = ev.get('value')
                unit.text(VIEWS[sel][1])
                reset_stats()
                lcd.console(' ปริมาณ: %s  [%s]' % (VIEWS[sel][0], VIEWS[sel][2]))

        time.sleep_ms(120)
except KeyboardInterrupt:
    pass
finally:
    if has_mic:
        pdm.deinit()
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
