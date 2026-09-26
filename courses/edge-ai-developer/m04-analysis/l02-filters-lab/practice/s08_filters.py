# s08_filters.py - ทำสัญญาณให้สะอาดด้วยฟิลเตอร์ DSP (ฉบับฝึกเติมโค้ด)
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) เติมช่องว่าง (pass) ทั้ง 5 จุดตามคำใบ้ในคอมเมนต์ให้ครบ
#          3) กด "Program to Device" แล้วเขย่า/ขยับบอร์ดเบา ๆ ให้เกิดสัญญาณรบกวน
#          4) ดูสองกราฟ: บน = Raw (ดิบ มีหนาม) · ล่าง = Filtered (ผ่านฟิลเตอร์ เรียบขึ้น)
#             แล้วสลับฟิลเตอร์ใน dropdown ดูว่าเส้นล่างเรียบต่างกันยังไง
#
# สัญญาณดิบจากเซนเซอร์ "มีหนาม" เสมอ งานของ Analysis คือดึงของจริงออกจากสัญญาณรบกวน
# โมดูล dsp มีฟิลเตอร์สำเร็จให้แล้ว (EMA/Median/Kalman1D) ทุกตัวใช้ท่าเดียวกัน:
# สร้างหนึ่งครั้ง -> ป้อนตัวอย่างด้วย .update(x) ทีละค่า -> ได้ค่าที่กรองแล้วออกมา
# งานของเราชุดบทเรียนนี้คือเติม 5 จุดที่ประกอบร่างไปป์ไลน์นี้ให้ครบ

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

# พารามิเตอร์เริ่มต้นของแต่ละฟิลเตอร์ — คือ "นิสัย" ของมัน
EMA_ALPHA   = 0.15          # ยิ่งเล็กยิ่งเรียบ แต่ตอบสนองช้าลง
MED_WINDOW  = 5             # median 5 ค่า — หนามโดด ๆ (outlier/multipath) โดนโหวตตกไป
KAL_Q       = 0.02          # q ต่ำ = เชื่อว่าสัญญาณจริงนิ่ง -> เรียบมาก
KAL_R       = 0.6           # r สูง = ไม่ค่อยเชื่อการวัด (มองว่าเซนเซอร์ noisy)


def make_filter(name):
    """สร้างอ็อบเจกต์ฟิลเตอร์หนึ่งตัวตามชื่อ — ทุกตัวมี .update(x)/.value()/.reset() เหมือนกัน

    ระวัง: พารามิเตอร์ทุกตัวเป็น keyword (alpha=/window=/q=/r=) ส่งเป็น positional ไม่ได้
    """
    if name == "Median":
        # เติม: สร้าง median filter หน้าต่าง MED_WINDOW ค่า -> return dsp.Median(window=MED_WINDOW)
        pass
    if name == "Kalman1D":
        # เติม: สร้าง kalman -> return dsp.Kalman1D(q=KAL_Q, r=KAL_R)
        pass
    # EMA เป็นค่าเริ่มต้น (ให้ไว้แล้ว) — ใช้ดูรูปแบบการส่ง keyword argument
    return dsp.EMA(alpha=EMA_ALPHA)


lcd.clear()
lcd.console('<h2> Analysis I - ทำสัญญาณให้สะอาดด้วยฟิลเตอร์ DSP</h2>')

# สร้าง widget ครั้งเดียวก่อนเข้าลูป (สร้างซ้ำในลูปจะกินหน่วยความจำและจอกระพริบ)
ui.Label("DSP Filters", x=20, y=8, color=PURPLE)
src_dd = ui.Dropdown(text="\n".join(SOURCE_NAMES), x=20, y=42, w=200)
flt_dd = ui.Dropdown(text="\n".join(FILTER_NAMES), x=232, y=42, w=160)
status = ui.Label("IMU · EMA", x=410, y=50, color=CYAN)

ui.Label("Raw (มีสัญญาณรบกวน)", x=20, y=86, color=ORANGE)
raw_chart = ui.Chart(x=20, y=104, w=750, h=96, min=0, max=250)
ui.Label("Filtered (สะอาดขึ้น)", x=20, y=206, color=GREEN)
filt_chart = ui.Chart(x=20, y=224, w=750, h=96, min=0, max=250)

nr_lab = ui.Label("noise down -- %", x=20, y=326, color=CYAN)
nr_bar = ui.Bar(x=180, y=330, w=280, h=12, min=0, max=100, value=0, color=DIM)

back = ui.Button("< ออก", x=650, y=352, w=120, h=36)
back_id = back.id()
src_id = src_dd.id()
flt_id = flt_dd.id()

source = 0                          # 0 = IMU accel, 1 = Radar range
filt_name = FILTER_NAMES[0]
filt = make_filter(filt_name)       # ฟิลเตอร์ที่กำลังใช้อยู่ (เริ่มที่ EMA)

last_raw = 0.0
prev_x = 0.0
prev_y = 0.0
raw_jit = 0.0
filt_jit = 0.0
nsamp = 0


def clamp(v):
    """คุมค่าให้อยู่ในช่วงกราฟ 0..250 (กันเส้นทะลุขอบ)"""
    return 0 if v < 0 else (250 if v > 250 else int(v))


def read_raw():
    """อ่านสัญญาณดิบหนึ่งค่าจากแหล่งที่เลือก แล้วปรับสเกลให้พอดีกับกราฟ 0..250"""
    global last_raw
    if source == 0:
        ax, ay, az = sensors.bmi270.acceleration()
        # เติม: หา "ขนาด" ของเวกเตอร์ความเร่งสามแกน -> mag = (ax*ax + ay*ay + az*az) ** 0.5
        mag = 0.0
        pass
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
    global raw_jit, filt_jit, nsamp
    raw_jit = 0.0
    filt_jit = 0.0
    nsamp = 0


show = "%s · %s"

try:
    while True:
        for ev in ui.poll():
            h = ev.get('handle')
            t = ev.get('type')
            if h == back_id:
                raise KeyboardInterrupt
            elif h == src_id and t == 'value_changed':
                source = ev.get('value')
                filt.reset()
                reset_stats()
                status.text(show % (SOURCE_NAMES[source].split()[0], filt_name))
                if source == 1:
                    lcd.console(' Radar range: ระยะจริงบนบอร์ด (Emulator ใช้ลูกบิดจำลอง)')
            elif h == flt_id and t == 'value_changed':
                filt_name = FILTER_NAMES[ev.get('value')]
                filt = make_filter(filt_name)
                reset_stats()
                status.text(show % (SOURCE_NAMES[source].split()[0], filt_name))
                lcd.console(' สลับฟิลเตอร์เป็น %s' % filt_name)

        x = read_raw()                  # สัญญาณดิบหนึ่งค่า (มีสัญญาณรบกวนปนอยู่)
        # เติม: ป้อนตัวอย่างเข้าฟิลเตอร์ทีละค่า มันคืนค่าที่กรองแล้ว -> y = filt.update(x)
        y = x
        pass

        # เติม: วาดสองเส้นเทียบกัน -> raw_chart.value(clamp(x))  แล้ว  filt_chart.value(clamp(y))
        pass

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

        time.sleep_ms(60)
except KeyboardInterrupt:
    pass
finally:
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
