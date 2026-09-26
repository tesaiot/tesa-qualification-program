# s08_filters.py - ทำสัญญาณให้สะอาดด้วยฟิลเตอร์ DSP (EMA / Median / Kalman1D)
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) กด "Program to Device"
#          3) เขย่า/ขยับบอร์ดเบา ๆ ให้เกิดสัญญาณรบกวน แล้วดูสองกราฟ:
#             บน = Raw (ดิบ มีหนาม) · ล่าง = Filtered (ผ่านฟิลเตอร์ เรียบขึ้น)
#          4) สลับฟิลเตอร์ใน dropdown แล้วดูว่าเส้นล่างเรียบต่างกันยังไง
#
# เฉลยนี้ไม่ได้มีไว้ลอกวาง สิ่งที่นับคือการอธิบายด้วยคำพูดของคุณเอง
# อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์ใหม่ด้วยมือ ทั้งไฟล์ยืนอยู่บนของจริงแค่สามก้าว:
# สร้างฟิลเตอร์ (dsp.EMA/Median/Kalman1D) -> ป้อนตัวอย่างด้วย update() -> วาดผลเทียบดิบ

import ui
ui.screen()
import lcd
import sensors
import dsp
import time

# ธีมสีเดียวกับหน้าอื่น ๆ บนบอร์ด (จะได้คุ้นตากับของจริง)
PURPLE = 0xBB86FC   # หัวข้อ
GREEN  = 0x50D890   # เส้นที่ผ่านฟิลเตอร์แล้ว (สะอาด)
DIM    = 0x6A3A31   # แถบตอนยังไม่ลดสัญญาณรบกวน
CYAN   = 0x71C7EC   # ข้อความรอง / เมตริก
RED    = 0xE85B5B   # error
CARD   = 0x2A1712   # พื้นการ์ด
SEC    = 0xCFC6BF   # ข้อความรอง
ORANGE = 0xFF9800   # เส้นดิบ (มีสัญญาณรบกวน)

FILTER_NAMES = ("EMA", "Median", "Kalman1D")
SOURCE_NAMES = ("IMU accel", "Radar range")     # radar_range(): ระยะจริงบนบอร์ด (Emulator จำลองด้วยลูกบิด)

# พารามิเตอร์เริ่มต้นของแต่ละฟิลเตอร์ — คือ "นิสัย" ของมัน จูนได้ในฉบับเต็ม
EMA_ALPHA   = 0.15          # ยิ่งเล็กยิ่งเรียบ แต่ตอบสนองช้าลง (ถ่วงน้ำหนักอดีตมากขึ้น)
MED_WINDOW  = 5             # median 5 ค่า — หนามโดด ๆ (outlier/multipath) โดนโหวตตกไป
KAL_Q       = 0.02          # q ต่ำ = เชื่อว่าสัญญาณจริงนิ่ง -> เรียบมาก
KAL_R       = 0.6           # r สูง = ไม่ค่อยเชื่อการวัด (มองว่าเซนเซอร์ noisy)


def make_filter(name):
    """สร้างอ็อบเจกต์ฟิลเตอร์หนึ่งตัวตามชื่อ — ทุกตัวมี .update(x)/.value()/.reset() เหมือนกัน

    สังเกตว่าพารามิเตอร์ทุกตัวเป็น keyword (alpha=/window=/q=/r=) ตามสเปกของโมดูล dsp
    ส่งเป็น positional ไม่ได้ — นี่คือจุดที่ผู้เรียนพลาดบ่อย
    """
    if name == "Median":
        # median ตัดหนามได้ดีเพราะ "เรียงแล้วเอาค่ากลาง" ค่าโดดสุดขั้วเลยไม่มีสิทธิ์ชนะ
        return dsp.Median(window=MED_WINDOW)
    if name == "Kalman1D":
        # kalman ชั่งน้ำหนักระหว่าง "ที่คาดไว้" กับ "ที่วัดได้" ทุกก้าว — เรียบและตามทัน
        return dsp.Kalman1D(q=KAL_Q, r=KAL_R)
    # EMA เป็นค่าเริ่มต้น: ถัวเฉลี่ยแบบถ่วงน้ำหนักอดีต ราคาถูกสุด เขียนได้ในบรรทัดเดียว
    return dsp.EMA(alpha=EMA_ALPHA)


lcd.clear()
lcd.console('<h2> Analysis I - ทำสัญญาณให้สะอาดด้วยฟิลเตอร์ DSP</h2>')
lcd.console(' สัญญาณดิบจากเซนเซอร์มีหนามเสมอ งานของ Analysis คือดึงของจริงออกจากสัญญาณรบกวน')

# สร้าง widget ครั้งเดียวก่อนเข้าลูป — สร้างซ้ำทุกวนรอบจะกินหน่วยความจำและจอกระพริบ
ui.Label("DSP Filters", x=20, y=8, color=PURPLE)
src_dd = ui.Dropdown(text="\n".join(SOURCE_NAMES), x=20, y=42, w=200)
flt_dd = ui.Dropdown(text="\n".join(FILTER_NAMES), x=232, y=42, w=160)
status = ui.Label("IMU · EMA", x=410, y=50, color=CYAN)

ui.Label("Raw (มีสัญญาณรบกวน)", x=20, y=86, color=ORANGE)
raw_chart = ui.Chart(x=20, y=104, w=750, h=96, min=0, max=250)
ui.Label("Filtered (สะอาดขึ้น)", x=20, y=206, color=GREEN)
filt_chart = ui.Chart(x=20, y=224, w=750, h=96, min=0, max=250)

# เมตริกวัดว่าฟิลเตอร์ช่วยแค่ไหน — เทียบ "การกระตุก" (jitter) ของเส้นดิบกับเส้นที่กรองแล้ว
nr_lab = ui.Label("noise down -- %", x=20, y=326, color=CYAN)
nr_bar = ui.Bar(x=180, y=330, w=280, h=12, min=0, max=100, value=0, color=DIM)

back = ui.Button("< ออก", x=570, y=352, w=120, h=36)
back_id = back.id()
src_id = src_dd.id()
flt_id = flt_dd.id()

source = 0                          # 0 = IMU accel, 1 = Radar range
filt_name = FILTER_NAMES[0]
filt = make_filter(filt_name)       # ฟิลเตอร์ที่กำลังใช้อยู่ (สร้างครั้งเดียว สลับได้ทีหลัง)

last_raw = 0.0                      # ค่าดิบล่าสุด (เผื่อ radar ไม่เจอเป้า จะได้ไม่กระโดดเป็น 0)
prev_x = 0.0                        # ค่าดิบก่อนหน้า — ใช้วัด jitter
prev_y = 0.0                        # ค่าที่กรองแล้วก่อนหน้า
raw_jit = 0.0                       # ผลรวมการกระตุกของเส้นดิบ
filt_jit = 0.0                      # ผลรวมการกระตุกของเส้นที่กรองแล้ว
nsamp = 0


def clamp(v):
    """คุมค่าให้อยู่ในช่วงกราฟ 0..250 (กันเส้นทะลุขอบ)"""
    return 0 if v < 0 else (250 if v > 250 else int(v))


def read_raw():
    """อ่านสัญญาณดิบหนึ่งค่าจากแหล่งที่เลือก แล้วปรับสเกลให้พอดีกับกราฟ 0..250"""
    global last_raw
    if source == 0:
        ax, ay, az = sensors.bmi270.acceleration()
        # ขนาดของเวกเตอร์ความเร่ง = รากที่สองของผลบวกกำลังสองสามแกน (อยู่นิ่ง ~9.8 m/s^2)
        mag = (ax * ax + ay * ay + az * az) ** 0.5
        last_raw = mag * 10.0       # x10 ให้แกว่งเห็นชัดบนกราฟ (นิ่ง ~98, ขยับพุ่งขึ้น)
    else:
        try:
            r = sensors.radar_range()
            if r['target']:
                last_raw = r['distance_m'] * 100.0     # เป็นเซนติเมตร
        except OSError:
            pass                    # radar DSP ไม่ทำงาน -> คงค่าเดิมไว้ ไม่พังโปรแกรม
    return last_raw


def reset_stats():
    """ล้างสถิติ jitter ทุกครั้งที่สลับแหล่ง/ฟิลเตอร์ จะได้วัดกันใหม่แบบยุติธรรม"""
    global raw_jit, filt_jit, nsamp
    raw_jit = 0.0
    filt_jit = 0.0
    nsamp = 0


show = "%s · %s"
lcd.console(' เลือกแหล่งสัญญาณ + ฟิลเตอร์ แล้วขยับบอร์ดเบา ๆ ดูเส้นล่างเรียบกว่าเส้นบน')

try:
    while True:
        for ev in ui.poll():
            h = ev.get('handle')
            t = ev.get('type')
            if h == back_id:
                raise KeyboardInterrupt
            elif h == src_id and t == 'value_changed':
                # เปลี่ยนแหล่งสัญญาณ — ล้างสถานะฟิลเตอร์ด้วย เพราะสเกลเปลี่ยนไปคนละเรื่อง
                source = ev.get('value')
                filt.reset()
                reset_stats()
                status.text(show % (SOURCE_NAMES[source].split()[0], filt_name))
                if source == 1:
                    lcd.console(' Radar range: ระยะจริงบนบอร์ด (Emulator ใช้ลูกบิดจำลอง)')
            elif h == flt_id and t == 'value_changed':
                # เปลี่ยนฟิลเตอร์ — สร้างตัวใหม่ทั้งอัน (สถานะเก่าใช้ต่อไม่ได้)
                filt_name = FILTER_NAMES[ev.get('value')]
                filt = make_filter(filt_name)
                reset_stats()
                status.text(show % (SOURCE_NAMES[source].split()[0], filt_name))
                lcd.console(' สลับฟิลเตอร์เป็น %s' % filt_name)

        x = read_raw()                  # สัญญาณดิบหนึ่งค่า (มีสัญญาณรบกวนปนอยู่)
        # หัวใจของชุดบทเรียน: ป้อนตัวอย่างเข้าฟิลเตอร์ทีละค่า มันคืนค่าที่กรองแล้วออกมา
        y = filt.update(x)

        # วาดสองเส้นเทียบกัน: บน = ดิบ ล่าง = กรองแล้ว (ต่างกันชัดตอนขยับ)
        raw_chart.value(clamp(x))
        filt_chart.value(clamp(y))

        # วัดว่าฟิลเตอร์ลด "การกระตุกระหว่างเฟรม" ได้กี่เปอร์เซ็นต์ (ไม่ต้องมี ground truth)
        raw_jit += abs(x - prev_x)
        filt_jit += abs(y - prev_y)
        prev_x = x
        prev_y = y
        nsamp += 1
        if nsamp > 8 and raw_jit > 0.0:
            red = (1.0 - filt_jit / raw_jit) * 100.0
            if red < 0.0:
                red = 0.0
            nr_bar.value(int(red))
            nr_bar.color(GREEN if red >= 40.0 else DIM)
            nr_lab.text("noise down %d %%" % int(red))

        time.sleep_ms(60)               # ~16 ตัวอย่าง/วินาที พอเห็นหนามแต่ไม่กิน CPU เปล่า
except KeyboardInterrupt:
    pass
finally:
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
