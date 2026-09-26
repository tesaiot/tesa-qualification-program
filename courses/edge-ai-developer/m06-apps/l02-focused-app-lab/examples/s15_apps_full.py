# s15_apps_full.py - แอป Edge AI แบบ "โฟกัสโมเดลเดียว" (ฉบับเต็ม)
# วิธีรัน: เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator (ide.tesaiot.dev)
#          กด "Program to Device" แล้วส่งเสียงตามโมเดลเป้าหมาย (ค่าตั้งต้น = Cough)
#
# ฉบับนี้คือเวอร์ชันขัดเรียบร้อยของ s15_apps.py — โครงเดียวกับที่คุณเติมในไฟล์ฝึก
# แต่เพิ่มรายละเอียดที่ทำให้แอปโฟกัส "ใช้งานได้จริง": แยกสี "มั่นใจ/ยังไม่ชัวร์"
# ด้วยเกณฑ์ CONF_FLOOR, นับด้วย debounce เบาๆ (ต้องเจอติดกันสองผลถึงจะนับ),
# จำเวลาที่เจอครั้งล่าสุด, และมีปุ่ม Reset ล้างตัวนับ ทั้งหมดยังยืนอยู่บนคำสั่ง
# หลักของ edge_ai เท่าเดิม
#
# รีทาร์เก็ตเป็นแอปโมเดลอื่นได้ทันที เปลี่ยนสามบรรทัด TARGET_* ด้านล่าง แล้วเซฟ
# เป็นไฟล์ใหม่ เช่น s15_alarm_app.py / s15_siren_app.py — โครงเดิมใช้ต่อได้หมด

import edge_ai
import ui
ui.screen()
import lcd
import time

# ----- ตั้งเป้าหมายของแอปนี้ -----
# Cough : TARGET_KEYWORDS=("cough",)  TARGET_CLASS="cough"
# Alarm : TARGET_KEYWORDS=("alarm",)  TARGET_CLASS="alarm"
# Siren : TARGET_KEYWORDS=("siren",)  TARGET_CLASS="sirens"
TARGET_KEYWORDS = ("cough",)
TARGET_CLASS    = "cough"
TARGET_SENSOR   = edge_ai.SENSOR_MIC

# ธีมสีเดียวกับหน้า Edge AI จริงบนบอร์ด
PURPLE = 0xBB86FC   # ชื่อ/หัวข้อ AI
GREEN  = 0x50D890   # ชนะแบบมั่นใจ + ตรวจเจอ
AMBER  = 0xE0A03A   # ยังไม่ถึงเกณฑ์ความมั่นใจ (not sure)
DIM    = 0x6A3A31   # คลาสที่ไม่ชนะ
CYAN   = 0x71C7EC   # ความมั่นใจ / latency
RED    = 0xE85B5B   # error
CARD   = 0x2A1712   # พื้นการ์ด
SEC    = 0xCFC6BF   # ข้อความรอง

SENSOR = ("IMU", "RADAR", "MIC")

lcd.clear()
lcd.console('<h2> Edge AI - แอปโฟกัสโมเดลเดียว (ฉบับเต็ม)</h2>')


def find_model(keywords, sensor):
    """เล็งโมเดลตามคีย์เวิร์ดในชื่อ ถ้าไม่เจอค่อยหลบไปใช้เซนเซอร์ที่ตรงกันตัวแรก"""
    ms = edge_ai.models()
    for m in ms:
        for k in keywords:
            if k.lower() in m['name'].lower():
                return m
    for m in ms:
        if m['sensor'] == sensor:
            return m
    return ms[0]


model = find_model(TARGET_KEYWORDS, TARGET_SENSOR)
labels = model['labels']
lcd.console(' โมเดลเป้าหมาย: %s (%s)  คลาส: %s'
            % (model['name'], SENSOR[model['sensor']], ", ".join(labels)))
lcd.console(' เกณฑ์ความมั่นใจ (CONF_FLOOR) = %.0f %%' % (edge_ai.CONF_FLOOR * 100))

# ---- สร้าง widget ครั้งเดียวก่อนลูป ----
ui.Label(model['name'], x=20, y=10, color=PURPLE)

ui.Panel(x=20, y=52, w=340, h=150, color=CARD)
verdict = ui.Seg7("---", x=40, y=78, color=GREEN)
conf = ui.Label("conf: -- %", x=40, y=164, color=CYAN)

ui.Panel(x=20, y=214, w=340, h=96, color=CARD)
ui.Label('ตรวจเจอ "%s"' % TARGET_CLASS, x=40, y=224, color=SEC)
hits_lbl = ui.Seg7("0", x=40, y=248, color=GREEN)
last_lbl = ui.Label("ล่าสุด: -- s ก่อน", x=180, y=232, color=SEC)
lat = ui.Label("latency: -- ms", x=40, y=320, color=CYAN)

btn_reset = ui.Button("Reset", x=250, y=316, w=100, h=34)
reset_id = btn_reset.id()

# แถบคะแนนต่อคลาส
rows = []
for i in range(len(labels)):
    y = 60 + i * 40
    lb = ui.Label(labels[i], x=430, y=y, color=SEC)
    br = ui.Bar(x=430, y=y + 18, w=320, h=12, min=0, max=100, value=0, color=DIM)
    rows.append((lb, br))

back = ui.Button("< ออก", x=570, y=352, w=120, h=36)
back_id = back.id()

hits = 0
last_seq = -1
sure_run = 0            # จำนวนผลติดกันที่เข้าคลาสเป้าหมายแบบมั่นใจ (ใช้ทำ debounce)
counted = False         # นับไปแล้วสำหรับ "เหตุการณ์" นี้หรือยัง
last_hit_ms = None      # เวลาที่เจอครั้งล่าสุด (ticks_ms)


def do_reset():
    global hits, sure_run, counted, last_hit_ms
    hits = 0
    sure_run = 0
    counted = False
    last_hit_ms = None
    hits_lbl.text("0")
    last_lbl.text("ล่าสุด: -- s ก่อน")
    lcd.console(' ล้างตัวนับแล้ว')


try:
    edge_ai.select(model['index'])
    lcd.console('<span class=ok> เริ่มฟัง %s…</span>' % model['name'])

    while True:
        for ev in ui.poll():
            h = ev.get('handle')
            if h == back_id:
                raise KeyboardInterrupt
            elif h == reset_id:
                do_reset()

        r = edge_ai.result()
        if r and r['seq'] != last_seq:
            last_seq = r['seq']
            sure = r['conf'] >= edge_ai.CONF_FLOOR
            # แยกสีคลาสที่ชนะ: เขียว = มั่นใจ, เหลือง = ยังไม่ชัวร์
            verdict.text(r['label'] or '-')
            verdict.color(GREEN if sure else AMBER)
            conf.text("conf: %.0f %%%s"
                      % (r['conf'] * 100, "" if sure else "  (not sure)"))
            lat.text("latency: %.1f ms" % r['latency_ms'])
            top = r['top']
            for i, (lb, br) in enumerate(rows):
                if i < len(r['scores']):
                    br.value(int(r['scores'][i] * 100))
                    br.color(GREEN if i == top else DIM)

            # ---- debounce เบาๆ: ต้องเจอคลาสเป้าหมายแบบมั่นใจ "ติดกันสองผล" ถึงนับ ----
            # เสียงจริงมักกระพริบข้ามเกณฑ์ในเสี้ยววินาที การนับทันทีจะได้ตัวเลขเฟ้อ
            # ตรงนี้คือ preview ของ โมดูล 6 (Apps) บทเรียน 6.3–6.4 (debounce/false-positive)
            is_target = (r['label'] == TARGET_CLASS and sure)
            sure_run = sure_run + 1 if is_target else 0
            if sure_run >= 2 and not counted:
                hits += 1
                counted = True
                last_hit_ms = time.ticks_ms()
                hits_lbl.text(str(hits))
                lcd.console('<span class=ok> เจอ %s ครั้งที่ %d</span>'
                            % (TARGET_CLASS, hits))
            if sure_run == 0:
                counted = False   # เหตุการณ์จบแล้ว พร้อมนับครั้งใหม่

        # อัปเดต "ล่าสุดกี่วินาทีก่อน" แม้ไม่มีผลใหม่ จะได้เห็นเวลาเดินจริง
        if last_hit_ms is not None:
            ago = time.ticks_diff(time.ticks_ms(), last_hit_ms) // 1000
            last_lbl.text("ล่าสุด: %d s ก่อน" % ago)

        time.sleep_ms(120)
except KeyboardInterrupt:
    pass
finally:
    edge_ai.stop()
    lcd.console('<span class=ok> จบการทำงาน — ตรวจเจอทั้งหมด %d ครั้ง</span>' % hits)

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
