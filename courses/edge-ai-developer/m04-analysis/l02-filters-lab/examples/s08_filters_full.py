# s08_filters_full.py - ทำสัญญาณให้สะอาดด้วยฟิลเตอร์ DSP (ฉบับเต็ม)
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) กด "Program to Device"
#          3) เขย่า/ขยับบอร์ดเบา ๆ ให้เกิดสัญญาณรบกวน แล้วดู Raw เทียบ Filtered
#          4) เลื่อน slider "strength" เพื่อจูนฟิลเตอร์สด ๆ แล้วสังเกตว่าเรียบขึ้น/ตอบช้าลงยังไง
#
# ต่อยอดจาก s08_filters.py: เพิ่ม slider จูนพารามิเตอร์สดตามชนิดฟิลเตอร์ (EMA alpha /
# Median window / Kalman r), แถบ noise-reduction เปลี่ยนสีตามเกณฑ์, และปุ่มหยุด/ไปต่อ (freeze)
# เพื่อจับภาพหนามเทียบเส้นเรียบได้นิ่ง ๆ ทั้งไฟล์ยังยืนบนสามก้าวเดิม: สร้าง -> update() -> วาด

import ui
ui.screen()
import lcd
import sensors
import dsp
import time

PURPLE = 0xBB86FC
GREEN  = 0x50D890
DIM    = 0x6A3A31
CYAN   = 0x71C7EC
RED    = 0xE85B5B
AMBER  = 0xFFC107
ORANGE = 0xFF9800
SEC    = 0xCFC6BF

FILTER_NAMES = ("EMA", "Median", "Kalman1D")
SOURCE_NAMES = ("IMU accel", "Radar range")

# ช่วง slider (1..100) แต่ละฟิลเตอร์ตีความ "strength" ต่างกัน
def build(name, strength):
    """สร้างฟิลเตอร์พร้อมพารามิเตอร์ที่ map มาจาก slider strength (1..100)

    - EMA:      alpha สูง = ตอบไว/เรียบน้อย, alpha ต่ำ = เรียบมาก -> กลับทางกับ strength
    - Median:   window ยิ่งกว้าง ยิ่งตัด outlier เก่ง (3..15, บังคับคี่โดยเฟิร์มแวร์)
    - Kalman1D: r ยิ่งสูง ยิ่งไม่เชื่อการวัด -> เรียบมาก
    """
    s = strength / 100.0                          # 0.01..1.0
    if name == "Median":
        w = 3 + int(s * 12)                       # 3..15
        return dsp.Median(window=w), "window=%d" % (w if (w & 1) else w + 1)
    if name == "Kalman1D":
        r = 0.05 + s * 3.0                        # 0.05..3.05
        return dsp.Kalman1D(q=0.02, r=r), "r=%.2f" % r
    alpha = 0.5 - s * 0.48                         # 0.5..0.02 (strength สูง = เรียบมาก)
    return dsp.EMA(alpha=alpha), "alpha=%.2f" % alpha


lcd.clear()
lcd.console('<h2> Analysis I - ฟิลเตอร์ DSP (ฉบับเต็ม)</h2>')
lcd.console(' Raw มีหนามเสมอ — ฟิลเตอร์ดึงของจริงออกจากสัญญาณรบกวน เลื่อน strength ดูผลสด')

ui.Label("DSP Filters +", x=20, y=8, color=PURPLE)
src_dd = ui.Dropdown(text="\n".join(SOURCE_NAMES), x=20, y=40, w=180)
flt_dd = ui.Dropdown(text="\n".join(FILTER_NAMES), x=212, y=40, w=150)
ui.Label("strength", x=378, y=30, color=SEC)
strength_sl = ui.Slider(x=378, y=50, w=180, min=1, max=100, value=45)
param_lab = ui.Label("alpha=0.28", x=572, y=44, color=CYAN)

ui.Label("Raw (มีสัญญาณรบกวน)", x=20, y=84, color=ORANGE)
raw_chart = ui.Chart(x=20, y=102, w=750, h=92, min=0, max=250)
ui.Label("Filtered (สะอาดขึ้น)", x=20, y=200, color=GREEN)
filt_chart = ui.Chart(x=20, y=218, w=750, h=92, min=0, max=250)

nr_lab = ui.Label("noise down -- %", x=20, y=322, color=CYAN)
nr_bar = ui.Bar(x=180, y=326, w=260, h=12, min=0, max=100, value=0, color=DIM)
freeze_btn = ui.Button("Freeze", x=470, y=316, w=110, h=34)

back = ui.Button("< ออก", x=570, y=350, w=120, h=36)
back_id = back.id()
src_id = src_dd.id()
flt_id = flt_dd.id()
freeze_id = freeze_btn.id()

source = 0
filt_name = FILTER_NAMES[0]
strength = 45
filt, param_str = build(filt_name, strength)
param_lab.text(param_str)

frozen = False
last_raw = 0.0
prev_x = 0.0
prev_y = 0.0
raw_jit = 0.0
filt_jit = 0.0
nsamp = 0


def clamp(v):
    return 0 if v < 0 else (250 if v > 250 else int(v))


def read_raw():
    global last_raw
    if source == 0:
        ax, ay, az = sensors.bmi270.acceleration()
        mag = (ax * ax + ay * ay + az * az) ** 0.5
        last_raw = mag * 10.0
    else:
        try:
            r = sensors.radar_range()
            if r['target']:
                last_raw = r['distance_m'] * 100.0
        except OSError:
            pass
    return last_raw


def rebuild():
    """สร้างฟิลเตอร์ใหม่ตามชื่อ+strength ปัจจุบัน แล้วล้างสถิติ jitter"""
    global filt, param_str, raw_jit, filt_jit, nsamp
    filt, param_str = build(filt_name, strength)
    param_lab.text(param_str)
    raw_jit = 0.0
    filt_jit = 0.0
    nsamp = 0


show = "%s · %s"
status_console = True

try:
    while True:
        for ev in ui.poll():
            h = ev.get('handle')
            t = ev.get('type')
            if h == back_id:
                raise KeyboardInterrupt
            elif h == freeze_id:
                frozen = not frozen
                freeze_btn.text("Run" if frozen else "Freeze")
                lcd.console(' หยุดภาพไว้ดูหนาม' if frozen else ' ไปต่อ')
            elif h == src_id and t == 'value_changed':
                source = ev.get('value')
                rebuild()
                filt.reset()
                if source == 1:
                    lcd.console(' Radar range: ระยะจริงบนบอร์ด (Emulator ใช้ลูกบิดจำลอง)')
            elif h == flt_id and t == 'value_changed':
                filt_name = FILTER_NAMES[ev.get('value')]
                rebuild()
                lcd.console(' สลับฟิลเตอร์เป็น %s (%s)' % (filt_name, param_str))
            elif h == strength_sl.id() and t == 'value_changed':
                strength = strength_sl.value()
                rebuild()

        if not frozen:
            x = read_raw()
            y = filt.update(x)
            raw_chart.value(clamp(x))
            filt_chart.value(clamp(y))

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
                # เขียว = ลดได้เยอะ, เหลือง = พอใช้, จาง = ยังไม่ช่วย
                nr_bar.color(GREEN if red >= 60.0 else (AMBER if red >= 30.0 else DIM))
                nr_lab.text("noise down %d %%" % int(red))

        time.sleep_ms(60)
except KeyboardInterrupt:
    pass
finally:
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
