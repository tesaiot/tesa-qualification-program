# s15_apps.py - แอป Edge AI แบบ "โฟกัสโมเดลเดียว" (เฉลย)
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) กด "Program to Device"
#          3) ส่งเสียงตามโมเดลเป้าหมาย (ค่าตั้งต้น = Cough) ให้ครบหลายครั้ง
#          4) ดูคลาสที่ชนะ + แถบทุกคลาส และตัวนับ "ตรวจเจอ" ค่อยๆ เพิ่มขึ้น
#
# เฉลยนี้ไม่ได้มีไว้ลอกวาง สิ่งที่นับคือการอธิบายด้วยคำพูดของคุณเอง
# อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์ใหม่ด้วยมือ — ทั้งไฟล์ยืนอยู่บนสามคำสั่งหลักของ
# edge_ai (select / result / stop) บวกกับ "การกระทำ" ง่ายๆ หนึ่งอย่าง: การนับ
#
# ของใหม่ชุดบทเรียนนี้เทียบกับ บทเรียน 1.1–1.3 คือ "โฟกัส": เราไม่ทำเมนูให้เลือกทุกโมเดล แต่เล็ง
# โมเดลเดียวด้วย find_model() แล้วเอา verdict มา "ทำอะไรต่อ" — จุดเริ่มของ Apps

import edge_ai
import ui
ui.screen()
import lcd
import time

# ----- ตั้งเป้าหมายของแอปนี้ (เปลี่ยนสองบรรทัดนี้เพื่อรีทาร์เก็ตเป็นแอปโมเดลอื่น) -----
# อยากได้ s15_alarm_app.py:  TARGET_KEYWORDS=("alarm",)  TARGET_CLASS="alarm"
# อยากได้ s15_siren_app.py:  TARGET_KEYWORDS=("siren",)  TARGET_CLASS="sirens"
TARGET_KEYWORDS = ("cough",)
TARGET_CLASS    = "cough"
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
    """เล็งโมเดลตามคีย์เวิร์ดในชื่อ ถ้าไม่เจอค่อยหลบไปใช้เซนเซอร์ที่ตรงกันตัวแรก
    ถามทะเบียนจากเฟิร์มแวร์จริงทุกครั้ง จะได้ไม่ต้อง hard-code index ที่อาจเลื่อน"""
    ms = edge_ai.models()
    for m in ms:
        for k in keywords:
            if k.lower() in m['name'].lower():
                return m
    for m in ms:
        if m['sensor'] == sensor:
            return m
    return ms[0]


# เล็งโมเดลเป้าหมายตัวเดียว — หัวใจของ "แอปโฟกัส" คือไม่ให้ผู้ใช้เลือกทั้งเมนู
model = find_model(TARGET_KEYWORDS, TARGET_SENSOR)
labels = model['labels']
lcd.console(' โมเดลเป้าหมาย: %s  คลาส: %s' % (model['name'], ", ".join(labels)))
lcd.console(' นับเมื่อเจอคลาส "%s" ที่ conf >= %.0f %%'
            % (TARGET_CLASS, edge_ai.CONF_FLOOR * 100))

# ---- สร้าง widget ครั้งเดียวก่อนเข้าลูป (สร้างซ้ำในลูปจะกินหน่วยความจำ จอกระพริบ) ----
ui.Label(model['name'], x=20, y=10, color=PURPLE)

ui.Panel(x=20, y=52, w=340, h=150, color=CARD)
verdict = ui.Seg7("---", x=40, y=78, color=GREEN)
conf = ui.Label("conf: -- %", x=40, y=164, color=CYAN)

ui.Panel(x=20, y=214, w=340, h=96, color=CARD)
ui.Label('ตรวจเจอ "%s"' % TARGET_CLASS, x=40, y=224, color=SEC)
hits_lbl = ui.Seg7("0", x=40, y=248, color=GREEN)
lat = ui.Label("latency: -- ms", x=40, y=320, color=CYAN)

# แถบคะแนนต่อคลาส — โมเดลเสียงส่วนใหญ่มีสองคลาส เราวาดครบตามจำนวนคลาสจริง
rows = []
for i in range(len(labels)):
    y = 60 + i * 40
    lb = ui.Label(labels[i], x=430, y=y, color=SEC)
    br = ui.Bar(x=430, y=y + 18, w=320, h=12, min=0, max=100, value=0, color=DIM)
    rows.append((lb, br))

back = ui.Button("< ออก", x=570, y=352, w=120, h=36)
back_id = back.id()

hits = 0            # จำนวนครั้งที่ตรวจเจอคลาสเป้าหมาย
last_seq = -1       # อัปเดตจอเฉพาะตอนมีผลใหม่ (seq เปลี่ยน) ไม่รัดจอทุกรอบ
was_target = False  # กันนับซ้ำ: นับเฉพาะจังหวะ "เพิ่งเข้า" คลาสเป้าหมาย (ขอบขาขึ้น)

try:
    # หัวใจข้อแรก: สั่ง CM55 ให้รันโมเดลเป้าหมายตัวเดียว select() ส่งคำสั่งแล้วรอ
    # ยืนยันว่าเปลี่ยนจริง (confirm by observation) ถ้าไม่สำเร็จจะโยน OSError
    edge_ai.select(model['index'])
    lcd.console('<span class=ok> เริ่มฟัง %s…</span>' % model['name'])

    while True:
        for ev in ui.poll():
            if ev.get('handle') == back_id:
                raise KeyboardInterrupt

        # หัวใจข้อสอง: ดึงผลอนุมานล่าสุด result() คืน dict หรือ None ถ้ายังไม่มีผล
        r = edge_ai.result()
        if r and r['seq'] != last_seq:
            last_seq = r['seq']
            # หัวใจข้อสาม: เอาคลาสที่ชนะขึ้นจอ ถ้า label ว่างก็โชว์ '?'
            verdict.text(r['label'] or '-')
            conf.text("conf: %.0f %%" % (r['conf'] * 100))
            lat.text("latency: %.1f ms" % r['latency_ms'])
            top = r['top']
            # ไล่ระบายแถบคะแนน "ทุกคลาส" คลาสที่ชนะเป็นเขียว ที่เหลือสีจาง
            for i, (lb, br) in enumerate(rows):
                if i < len(r['scores']):
                    br.value(int(r['scores'][i] * 100))
                    br.color(GREEN if i == top else DIM)

            # ---- จาก verdict สู่ action: นับเมื่อ "เพิ่งเข้า" คลาสเป้าหมายแบบมั่นใจ ----
            # เชื่อคำตอบก็ต่อเมื่อ conf ถึงเกณฑ์ CONF_FLOOR เท่านั้น ต่ำกว่านั้นถือว่า
            # โมเดลยังไม่ชัวร์ ไม่ควรนับ เพราะจะเก็บ false positive มาเต็มไปหมด
            is_target = (r['label'] == TARGET_CLASS
                         and r['conf'] >= edge_ai.CONF_FLOOR)
            # นับเฉพาะ "ขอบขาขึ้น": เจอคลาสเป้าหมายครั้งใหม่ ไม่ใช่ค้างเจอต่อเนื่อง
            if is_target and not was_target:
                hits += 1
                hits_lbl.text(str(hits))
                lcd.console('<span class=ok> เจอ %s ครั้งที่ %d</span>'
                            % (TARGET_CLASS, hits))
            was_target = is_target

        time.sleep_ms(150)      # เว้นจังหวะ ไม่รัดจอจนกิน CPU เปล่า
except KeyboardInterrupt:
    pass
finally:
    edge_ai.stop()      # คู่กับ select เสมอ — ออกยังไงก็หยุดเครื่องยนต์ให้ว่าง
    lcd.console('<span class=ok> จบการทำงาน — ตรวจเจอทั้งหมด %d ครั้ง</span>' % hits)

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
