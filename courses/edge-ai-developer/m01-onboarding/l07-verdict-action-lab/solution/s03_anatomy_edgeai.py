# s03_anatomy_edgeai.py - แกะแอป Edge AI แล้ว remix: สลับโมเดล + สั่งการเมื่อเจอคลาส
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) กด "Program to Device"
#          3) ทำท่า/ส่งเสียงตามโมเดล พอคลาสเป้าหมายชนะเกินเกณฑ์ แอปจะสั่งการเอง
#
# เฉลยนี้ไม่ได้มีไว้ลอกวาง สิ่งที่นับคือการอธิบายด้วยคำพูดของคุณเอง
# อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์ใหม่ด้วยมือ ตอนพิมพ์เองสมองจะจับ pattern ได้ว่า
# แอป Edge AI ตัวเดียวคือ 3 จังหวะ: select (เลือกโมเดล) -> result (อ่าน verdict)
# -> action (สั่งการเมื่อ verdict เข้าเงื่อนไข) จังหวะที่สามคือของใหม่ของชุดบทเรียนนี้

import edge_ai
import ui
ui.screen()
import lcd
import time

# ---- remix ตรงนี้ได้เลย: สลับโมเดล + เลือกคลาสที่อยาก "จับแล้วสั่งการ" ----
# นี่คือสองบรรทัดที่ทำให้แอปเดียวกลายเป็นได้หลายแอป — เปลี่ยนสองค่านี้ทั้งพฤติกรรม
MODEL_KEYWORD = "Motion"     # ลองเปลี่ยนเป็น "Baby Cry" / "Cough" / "Siren" / "Push"
TARGET_CLASS  = "shaking"    # คลาสของโมเดลนั้นที่อยากดักจับ (ดูจาก labels ในคอนโซล)

# ธีมสีเดียวกับหน้า Edge AI จริงบนบอร์ด (จะได้คุ้นตากับของจริง)
PURPLE = 0xBB86FC   # ชื่อ/หัวข้อ AI
GREEN  = 0x50D890   # คลาสที่ชนะ + ACTION ยิงแล้ว
DIM    = 0x6A3A31   # คลาสที่ไม่ชนะ
CYAN   = 0x71C7EC   # ความมั่นใจ / latency
RED    = 0xE85B5B   # error / รอจับ
CARD   = 0x2A1712   # พื้นการ์ดผลลัพธ์
SEC    = 0xCFC6BF   # ข้อความรอง

SENSOR = ("IMU", "RADAR", "MIC")

lcd.clear()
lcd.console('<h2> Edge AI - เฝ้าจับคลาส แล้วสั่งการ (remix)</h2>')


def find_model(keyword):
    """หาโมเดลจากชื่อในทะเบียนของเฟิร์มแวร์ — ถ้าไม่เจอใช้ตัวแรกกันแอปพัง
    เราถาม models() แทนการ hard-code index เพราะถ้าเฟิร์มแวร์สลับลำดับโมเดล
    โค้ดจะยังหาโมเดลถูกตัวจากชื่อได้เอง (นิสัย 'ถามฮาร์ดแวร์ก่อน' จากบทเรียน 1.1–1.3)"""
    ms = edge_ai.models()
    for m in ms:
        if keyword.lower() in m['name'].lower():
            return m
    return ms[0]


model = find_model(MODEL_KEYWORD)
labels = model['labels']
lcd.console(' โมเดล: %s (%s)  คลาส: %s'
            % (model['name'], SENSOR[model['sensor']], ", ".join(labels)))
lcd.console(' จะสั่งการเมื่อเจอคลาส "%s" มั่นใจเกิน %.0f%%'
            % (TARGET_CLASS, edge_ai.CONF_FLOOR * 100))

# ---- สร้าง widget ครั้งเดียวก่อนเข้าลูป — สร้างซ้ำทุกวนรอบจะกินหน่วยความจำและจอกระพริบ ----
ui.Label("Edge AI - watcher", x=20, y=8, color=PURPLE)
ui.Panel(x=20, y=48, w=320, h=150, color=CARD)
verdict = ui.Seg7("---", x=40, y=74, color=GREEN)
conf = ui.Label("conf: -- %", x=40, y=162, color=CYAN)
banner = ui.Label("รอจับ %s ..." % TARGET_CLASS, x=40, y=214, color=RED)

# แถวคะแนนต่อคลาส สร้างครบตามจำนวนคลาสของโมเดลนี้ตั้งแต่แรก แล้วในลูปแค่เปลี่ยนค่า
rows = []
for i in range(len(labels)):
    y = 60 + i * 40
    lb = ui.Label(labels[i], x=400, y=y, color=SEC)
    br = ui.Bar(x=400, y=y + 18, w=340, h=12, min=0, max=100, value=0, color=DIM)
    rows.append((lb, br))

back = ui.Button("< ออก", x=570, y=352, w=120, h=36)
back_id = back.id()


def fire_action(conf_val):
    """ACTION เมื่อจับคลาสเป้าหมายได้ — บี๊บ + แบนเนอร์ + คอนโซล
    นี่คือหัวใจของชุดบทเรียนนี้: verdict (โมเดลบอกว่าเจออะไร) กลายเป็น action จริงบนบอร์ด
    ในงานจริง action ตรงนี้อาจเป็น เปิดไฟ / ส่งแจ้งเตือน / บันทึกเหตุการณ์"""
    banner.text("! เจอ %s !" % TARGET_CLASS)
    banner.color(GREEN)
    if hasattr(ui, "tone"):
        ui.tone(72, ui.WAVE_SINE, 120, 150)   # โน้ต MIDI 72 = โดสูง (เสียงยืนยัน)
    lcd.console('<span class=ok> ACTION: เจอ %s (conf %.0f%%)</span>'
                % (TARGET_CLASS, conf_val * 100))


# ---- สั่งให้ CM55 เริ่มรันโมเดลที่เลือก (confirm by observation เหมือนบทเรียน 1.1–1.3) ----
try:
    # หัวใจข้อแรก: บอก CM55 ให้สลับมารันโมเดลที่เลือกจากชื่อ — ห่อ try เพราะข้ามคอร์พลาดได้
    edge_ai.select(model['index'])
    lcd.console('<span class=ok> เริ่มอนุมาน…</span>')
except OSError as e:
    lcd.console('<span class=error> โหลดไม่สำเร็จ: %s</span>' % e)

last_seq = -1
fired = False           # กันยิง action ซ้ำ: ยิงครั้งเดียวต่อการเจอหนึ่งครั้ง (edge-trigger)
try:
    while True:
        for ev in ui.poll():
            if ev.get('handle') == back_id:
                raise KeyboardInterrupt

        # หัวใจข้อสอง: อ่านผลอนุมานล่าสุด result() คืน dict หรือ None ถ้ายังไม่มีผล
        r = edge_ai.result()
        if r and r['seq'] != last_seq:      # วาดจอเฉพาะตอนมีผลใหม่ (seq เปลี่ยน)
            last_seq = r['seq']
            # หัวใจข้อสาม: เอาคลาสที่ชนะขึ้นจอ ถ้า label ว่างก็โชว์ '?'
            verdict.text(r['label'] or '-')
            conf.text("conf: %.0f %%" % (r['conf'] * 100))
            top = r['top']
            for i, (lb, br) in enumerate(rows):
                if i < len(r['scores']):
                    br.value(int(r['scores'][i] * 100))
                    br.color(GREEN if i == top else DIM)

            # หัวใจข้อสี่ (ของใหม่ชุดบทเรียนนี้): verdict เข้าเงื่อนไขไหม -> ถ้าใช่ค่อยสั่งการ
            # เงื่อนไข = คลาสที่ชนะตรงเป้าหมาย และมั่นใจไม่ต่ำกว่า CONF_FLOOR
            hit = (r['label'] == TARGET_CLASS
                   and r['conf'] >= edge_ai.CONF_FLOOR)
            if hit and not fired:
                # ยิง action ครั้งเดียวตอน "เพิ่งเจอ" ไม่ยิงรัวทุกเฟรมที่ยังเจออยู่
                fire_action(r['conf'])
                fired = True
            elif not hit:
                # ออกจากคลาสเป้าหมายแล้ว รีเซ็ต fired ให้พร้อมยิงรอบใหม่
                fired = False
                banner.text("รอจับ %s ..." % TARGET_CLASS)
                banner.color(RED)

        time.sleep_ms(180)      # เว้นจังหวะ ไม่รัดจอจนกิน CPU เปล่า
except KeyboardInterrupt:
    pass
finally:
    edge_ai.stop()      # ออกจากงานยังไง ทิ้งเครื่องไว้ให้เรียบร้อยแบบนั้น
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
