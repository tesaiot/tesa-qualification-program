# s03_anatomy_edgeai.py - แกะแอป Edge AI แล้ว remix: สลับโมเดล + สั่งการเมื่อเจอคลาส (ฉบับฝึกเติมโค้ด)
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) เติมช่องว่าง (pass) ทั้ง 4 จุดตามคำใบ้ในคอมเมนต์ให้ครบ
#          3) กด "Program to Device" แล้วทำท่า/ส่งเสียงตามโมเดลที่เลือก
#          4) พอคลาสเป้าหมายชนะเกินเกณฑ์ แอปจะ "สั่งการ" เอง (บี๊บ + แบนเนอร์)
#
# ชุดบทเรียนนี้เรากลับด้าน "แอป Edge AI ตัวเดียว" ของ example 13 (Motion) แล้ว remix มัน:
# เปลี่ยนจาก "เมนู 6 โมเดล" (บทเรียน 1.1–1.3) มาเป็นแอปเฝ้าจับ "โมเดลเดียว 1 คลาส" แล้ว
# สั่งการเมื่อเจอ — นี่คือก้าวจาก "อ่านผล" (verdict) ไปสู่ "ลงมือ" (action on a verdict)
# ซึ่งเป็นหัวใจของ โมดูล 6 (Apps) ทั้งบล็อก งานของคุณคือเติม 4 คำสั่งที่ต่อวงจรนี้ให้ครบ

import edge_ai
import ui
ui.screen()
import lcd
import time

# ---- remix ตรงนี้ได้เลย: สลับโมเดล + เลือกคลาสที่อยาก "จับแล้วสั่งการ" ----
MODEL_KEYWORD = "Motion"     # ลองเปลี่ยนเป็น "Baby Cry" / "Cough" / "Siren" / "Push"
TARGET_CLASS  = "shaking"    # คลาสของโมเดลนั้นที่อยากดักจับ (ดูจาก labels ในคอนโซล)

# ธีมสีเดียวกับหน้า Edge AI จริงบนบอร์ด
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
    """หาโมเดลจากชื่อ (เช่น 'Motion') ในทะเบียนของเฟิร์มแวร์ — ถ้าไม่เจอใช้ตัวแรก
    บรรทัดนี้คือหัวใจ 'ถามฮาร์ดแวร์ ไม่เดา' เหมือนบทเรียน 1.1–1.3: models() คืนทะเบียนจริง"""
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

# ---- สร้าง widget ครั้งเดียวก่อนเข้าลูป (สร้างซ้ำในลูปจะกินหน่วยความจำและจอกระพริบ) ----
ui.Label("Edge AI - watcher", x=20, y=8, color=PURPLE)
ui.Panel(x=20, y=48, w=320, h=150, color=CARD)
verdict = ui.Seg7("---", x=40, y=74, color=GREEN)
conf = ui.Label("conf: -- %", x=40, y=162, color=CYAN)
banner = ui.Label("รอจับ %s ..." % TARGET_CLASS, x=40, y=214, color=RED)

# แถวคะแนนต่อคลาส สร้างไว้ก่อนแล้วโชว์ตามจำนวนคลาสของโมเดล
rows = []
for i in range(len(labels)):
    y = 60 + i * 40
    lb = ui.Label(labels[i], x=400, y=y, color=SEC)
    br = ui.Bar(x=400, y=y + 18, w=340, h=12, min=0, max=100, value=0, color=DIM)
    rows.append((lb, br))

back = ui.Button("< ออก", x=650, y=352, w=120, h=36)
back_id = back.id()


def fire_action(conf_val):
    """ACTION เมื่อจับคลาสเป้าหมายได้ — บี๊บ + แบนเนอร์ + คอนโซล
    นี่คือ 'action on a verdict': verdict (คำตอบของโมเดล) -> การกระทำจริงบนบอร์ด"""
    banner.text("! เจอ %s !" % TARGET_CLASS)
    banner.color(GREEN)
    if hasattr(ui, "tone"):
        ui.tone(72, ui.WAVE_SINE, 120, 150)   # โน้ต MIDI 72 = โดสูง (เสียงยืนยัน)
    lcd.console('<span class=ok> ACTION: เจอ %s (conf %.0f%%)</span>'
                % (TARGET_CLASS, conf_val * 100))


# ---- สั่งให้ CM55 เริ่มรันโมเดลที่เลือก ----
try:
    # เติม: สั่งให้ CM55 รันโมเดลนี้ ด้วย edge_ai.select(model['index'])
    pass
    lcd.console('<span class=ok> เริ่มอนุมาน…</span>')
except OSError as e:
    lcd.console('<span class=error> โหลดไม่สำเร็จ: %s</span>' % e)

last_seq = -1
fired = False           # กันยิง action ซ้ำ: ยิงครั้งเดียวต่อการเจอหนึ่งครั้ง
try:
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
            top = r['top']
            for i, (lb, br) in enumerate(rows):
                if i < len(r['scores']):
                    br.value(int(r['scores'][i] * 100))
                    br.color(GREEN if i == top else DIM)

            # ตรวจว่าเจอคลาสเป้าหมายและมั่นใจพอไหม (นี่คือ verdict -> decision)
            hit = (r['label'] == TARGET_CLASS
                   and r['conf'] >= edge_ai.CONF_FLOOR)
            if hit and not fired:
                # เติม: สั่งการเมื่อจับ TARGET ได้ครั้งแรก -> fire_action(r['conf'])
                pass
                fired = True
            elif not hit:
                # ออกจากคลาสเป้าหมายแล้ว รีเซ็ตให้พร้อมยิงรอบใหม่
                fired = False
                banner.text("รอจับ %s ..." % TARGET_CLASS)
                banner.color(RED)

        time.sleep_ms(180)
except KeyboardInterrupt:
    pass
finally:
    edge_ai.stop()      # ปิดเครื่องยนต์ให้เรียบร้อยเสมอ ไม่ปล่อยค้างรัน
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
