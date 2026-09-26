# s15_apps.py - แอป Edge AI แบบ "โฟกัสโมเดลเดียว" (ฉบับฝึกเติมโค้ด)
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) เติมช่องว่าง (pass / False) ทั้ง 4 จุดตามคำใบ้ในคอมเมนต์ให้ครบ
#          3) กด "Program to Device" แล้วส่งเสียงตามโมเดลเป้าหมาย (ค่าตั้งต้น = Cough)
#          4) ดูคลาสที่ชนะ + แถบทุกคลาส และตัวนับ "จำนวนครั้งที่ตรวจเจอ" เพิ่มขึ้น
#
# บทเรียน 1.1–1.3 เราทำ "เมนู 6 โมเดล" ให้เลือกได้ทั้งหมด — ชุดบทเรียนนี้เราถอยไปอีกก้าว
# แล้วสร้าง "แอปต่อโมเดล" ตัวเดียวจบ: เล็งโมเดลเป้าหมายด้วยคีย์เวิร์ด (find_model)
# รันตัวเดียว แล้วต่อ verdict เข้ากับ "การกระทำ" ง่ายๆ คือนับครั้งที่คลาสเป้าหมาย
# ข้ามเกณฑ์ความมั่นใจ นี่คือก้าวแรกสู่ โมดูล 6 (Apps) — จาก "อ่านผล" สู่ "ทำอะไรกับผล"
#
# อยากได้แอปของโมเดลอื่น (alarm / siren / motion)? เปลี่ยนแค่สองบรรทัด TARGET_*
# ข้างล่าง แล้วเซฟเป็นไฟล์ใหม่ (เช่น s15_alarm_app.py) — โครงเดิมทั้งหมดใช้ต่อได้เลย

import edge_ai
import ui
ui.screen()
import lcd
import time

# ----- ตั้งเป้าหมายของแอปนี้ (เปลี่ยนสองบรรทัดนี้เพื่อรีทาร์เก็ตเป็นแอปโมเดลอื่น) -----
TARGET_KEYWORDS = ("cough",)   # คีย์เวิร์ดหาชื่อโมเดล เช่น ("alarm",) / ("siren",)
TARGET_CLASS    = "cough"       # ชื่อคลาสที่ถือว่า "ตรวจเจอ" เช่น "alarm" / "sirens"
TARGET_SENSOR   = edge_ai.SENSOR_MIC   # เซนเซอร์สำรอง ถ้าหาโมเดลจากชื่อไม่เจอ

# ธีมสีเดียวกับหน้า Edge AI จริงบนบอร์ด (จะได้คุ้นตากับของจริง)
PURPLE = 0xBB86FC   # ชื่อ/หัวข้อ AI
GREEN  = 0x50D890   # คลาสที่ชนะ + ตรวจเจอ
DIM    = 0x6A3A31   # คลาสที่ไม่ชนะ
CYAN   = 0x71C7EC   # ความมั่นใจ / latency
RED    = 0xE85B5B   # error
CARD   = 0x2A1712   # พื้นการ์ด
SEC    = 0xCFC6BF   # ข้อความรอง

lcd.clear()
lcd.console('<h2> Edge AI - แอปโฟกัสโมเดลเดียว</h2>')


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


# ถามทะเบียนจากเฟิร์มแวร์ แล้วเล็งโมเดลเป้าหมายตัวเดียว (ไม่ทำ dropdown ทั้งเมนู)
model = find_model(TARGET_KEYWORDS, TARGET_SENSOR)
labels = model['labels']
lcd.console(' โมเดลเป้าหมาย: %s  คลาส: %s' % (model['name'], ", ".join(labels)))
lcd.console(' นับเมื่อเจอคลาส "%s" ที่ conf >= %.0f %%'
            % (TARGET_CLASS, edge_ai.CONF_FLOOR * 100))

# ---- สร้าง widget ครั้งเดียวก่อนเข้าลูป ----
ui.Label(model['name'], x=20, y=10, color=PURPLE)

ui.Panel(x=20, y=52, w=340, h=150, color=CARD)
verdict = ui.Seg7("---", x=40, y=78, color=GREEN)
conf = ui.Label("conf: -- %", x=40, y=164, color=CYAN)

ui.Panel(x=20, y=214, w=340, h=96, color=CARD)
ui.Label('ตรวจเจอ "%s"' % TARGET_CLASS, x=40, y=224, color=SEC)
hits_lbl = ui.Seg7("0", x=40, y=248, color=GREEN)
lat = ui.Label("latency: -- ms", x=40, y=320, color=CYAN)

# แถบคะแนนต่อคลาส — สร้างครบตามจำนวนคลาสของโมเดลนี้
rows = []
for i in range(len(labels)):
    y = 60 + i * 40
    lb = ui.Label(labels[i], x=430, y=y, color=SEC)
    br = ui.Bar(x=430, y=y + 18, w=320, h=12, min=0, max=100, value=0, color=DIM)
    rows.append((lb, br))

back = ui.Button("< ออก", x=650, y=352, w=120, h=36)
back_id = back.id()

hits = 0            # จำนวนครั้งที่ตรวจเจอคลาสเป้าหมาย
last_seq = -1       # กันวาดจอซ้ำ: อัปเดตเฉพาะตอนมีผลใหม่ (seq เปลี่ยน)
was_target = False  # กันนับซ้ำ: นับเฉพาะ "ขอบขาขึ้น" ตอนเพิ่งเข้าคลาสเป้าหมาย

try:
    # เติม: เริ่มรันโมเดลเป้าหมายตัวเดียว ด้วย edge_ai.select(model['index'])
    pass
    lcd.console('<span class=ok> เริ่มฟัง %s…</span>' % model['name'])

    while True:
        for ev in ui.poll():
            if ev.get('handle') == back_id:
                raise KeyboardInterrupt

        # เติม: อ่านผลอนุมานล่าสุดมาเก็บใน r  ->  r = edge_ai.result()
        r = None
        pass
        if r and r['seq'] != last_seq:
            last_seq = r['seq']
            # เติม: แสดงคลาสที่ชนะบนจอ ด้วย verdict.text(r['label'] or '-')
            pass
            conf.text("conf: %.0f %%" % (r['conf'] * 100))
            lat.text("latency: %.1f ms" % r['latency_ms'])
            top = r['top']
            for i, (lb, br) in enumerate(rows):
                if i < len(r['scores']):
                    br.value(int(r['scores'][i] * 100))
                    br.color(GREEN if i == top else DIM)

            # ---- จาก verdict สู่ action: นับเมื่อ "เพิ่งเข้า" คลาสเป้าหมายแบบมั่นใจ ----
            # เติม: แทน False ด้วยเงื่อนไขตรวจเจอจริง
            #       r['label'] == TARGET_CLASS and r['conf'] >= edge_ai.CONF_FLOOR
            is_target = False
            if is_target and not was_target:
                hits += 1
                hits_lbl.text(str(hits))
                lcd.console('<span class=ok> เจอ %s ครั้งที่ %d</span>'
                            % (TARGET_CLASS, hits))
            was_target = is_target

        time.sleep_ms(150)
except KeyboardInterrupt:
    pass
finally:
    edge_ai.stop()      # ออกจากงานยังไง ทิ้งเครื่องยนต์ให้ว่างแบบนั้นเสมอ
    lcd.console('<span class=ok> จบการทำงาน — ตรวจเจอทั้งหมด %d ครั้ง</span>' % hits)

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
