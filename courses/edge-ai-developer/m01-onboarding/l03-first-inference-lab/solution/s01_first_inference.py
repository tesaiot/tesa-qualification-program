# s01_first_inference.py - รันโมเดล Edge AI ตัวแรกของเรา
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) กด "Program to Device"
#          3) เลือกโมเดลใน dropdown กด Load แล้วทำท่า/ส่งเสียงตามโมเดลนั้น
#          4) ดูคลาสที่ชนะบนจอ + แถบความมั่นใจของแต่ละคลาส
#
# เฉลยนี้ไม่ได้มีไว้ลอกวาง สิ่งที่นับคือการอธิบายด้วยคำพูดของคุณเอง
# อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์ใหม่ด้วยมือ ตอนพิมพ์เองนั่นแหละสมองจะจำ pattern
# ของ edge_ai ได้ ทั้งไฟล์ยืนอยู่บนคำสั่งหลักแค่ 4 ตัว: models / select / result / stop

import edge_ai
import ui
ui.screen()
import lcd
import time

# ธีมสีเดียวกับหน้า Edge AI จริงบนบอร์ด (จะได้คุ้นตากับของจริง)
PURPLE = 0xBB86FC   # ชื่อ/หัวข้อ AI
GREEN  = 0x50D890   # คลาสที่ชนะ + สถานะ RUNNING
DIM    = 0x6A3A31   # คลาสที่ไม่ชนะ
CYAN   = 0x71C7EC   # ความมั่นใจ / latency
RED    = 0xE85B5B   # STOPPED / error
CARD   = 0x2A1712   # พื้นการ์ดผลลัพธ์
SEC    = 0xCFC6BF   # ข้อความรอง

SENSOR = ("IMU", "RADAR", "MIC")

lcd.clear()
lcd.console('<h2> Edge AI - โมเดลตัวแรกของเรา</h2>')

# ถามเฟิร์มแวร์ก่อนว่ามีโมเดลอะไรบ้าง แทนที่จะเดาเอง — edge_ai.models() คืน list
# ของ dict หนึ่งตัวต่อหนึ่งโมเดล แต่ละ dict มี index / name / sensor / labels
# ข้อมูลนี้ดึงมาจาก CM55 (pull ผ่าน IPC) ค่าจริง ไม่ใช่ค่าที่เรา hard-code ไว้เอง
models = edge_ai.models()
names = [m['name'] for m in models]
lcd.console(' พบ %d โมเดลในเฟิร์มแวร์: %s' % (len(models), ", ".join(names)))

# สร้าง widget ครั้งเดียวก่อนเข้าลูป — ถ้าสร้างซ้ำทุกวนรอบจะกินหน่วยความจำและจอกระพริบ
ui.Label("Edge AI", x=20, y=8, color=PURPLE)
dd = ui.Dropdown(text="\n".join(names), x=20, y=42, w=250)
btn_load = ui.Button("Load", x=285, y=42, w=88, h=36)
btn_stop = ui.Button("Stop", x=381, y=42, w=88, h=36)
status = ui.Label("STOPPED", x=490, y=50, color=RED)

ui.Panel(x=20, y=92, w=300, h=150, color=CARD)
verdict = ui.Seg7("---", x=40, y=118, color=GREEN)
conf = ui.Label("conf: -- %", x=40, y=206, color=CYAN)

# โมเดลหนึ่งมีได้ถึง 8 คลาส เราสร้างแถวคะแนนไว้ครบ 8 แถวก่อน แล้วค่อยโชว์เฉพาะ
# จำนวนคลาสของโมเดลที่เลือก — ถูกกว่าการลบ/สร้าง widget ใหม่ทุกครั้งที่สลับโมเดล
rows = []
for i in range(8):
    y = 96 + i * 30
    lb = ui.Label("", x=360, y=y, color=SEC)
    br = ui.Bar(x=360, y=y + 16, w=400, h=10, min=0, max=100, value=0, color=DIM)
    lb.hide()
    br.hide()
    rows.append((lb, br))

back = ui.Button("< ออก", x=570, y=352, w=120, h=36)
back_id = back.id()
dd_id = dd.id()
load_id = btn_load.id()
stop_id = btn_stop.id()


def show_rows(mi):
    """โชว์แถบคลาสของโมเดลที่เลือก (widget สร้างไว้แล้ว แค่เปลี่ยนข้อความ + โชว์/ซ่อน)"""
    labels = models[mi]['labels']
    for i, (lb, br) in enumerate(rows):
        if i < len(labels):
            lb.text(labels[i])
            br.value(0)
            br.color(DIM)
            lb.show()
            br.show()
        else:
            lb.hide()
            br.hide()


sel = 0            # โมเดลที่เลือกใน dropdown (เริ่มที่ index 0 = Motion Detection)
running = False
last_seq = -1      # กันวาดจอซ้ำ: วาดเฉพาะตอนมีผลอนุมานใหม่ (seq เปลี่ยน)
show_rows(sel)
lcd.console(' เลือกโมเดลใน dropdown แล้วกด Load เพื่อเริ่มอนุมาน')

try:
    while True:
        for ev in ui.poll():
            h = ev.get('handle')
            t = ev.get('type')
            if h == back_id:
                raise KeyboardInterrupt
            elif h == dd_id and t == 'value_changed':
                # ผู้ใช้เพิ่งเปลี่ยนโมเดลใน dropdown — ล้างผลเก่า แล้วโชว์คลาสของโมเดลใหม่
                sel = ev.get('value')
                verdict.text('---')
                conf.text("conf: -- %")
                show_rows(sel)
                lcd.console(' เลือก: %s (%s)'
                            % (models[sel]['name'], SENSOR[models[sel]['sensor']]))
            elif h == load_id:
                try:
                    # หัวใจข้อแรก: บอก CM55 ให้สลับมารันโมเดลที่เลือก select() จะส่งคำสั่ง
                    # แล้วรอยืนยันว่าเปลี่ยนจริง (confirm by observation) ถ้าไม่สำเร็จโยน OSError
                    edge_ai.select(sel)
                    running = True
                    last_seq = -1
                    status.text("RUNNING")
                    status.color(GREEN)
                    lcd.console('<span class=ok> รัน %s</span>' % models[sel]['name'])
                except OSError as e:
                    status.text("ERROR")
                    status.color(RED)
                    lcd.console('<span class=error> โหลดไม่สำเร็จ: %s</span>' % e)
            elif h == stop_id:
                # หัวใจข้อสี่: หยุดเครื่องยนต์อนุมานให้ว่าง (idle) — คู่กับ select
                edge_ai.stop()
                running = False
                status.text("STOPPED")
                status.color(RED)
                lcd.console(' หยุดโมเดล')

        if running:
            # หัวใจข้อสอง: อ่านผลอนุมานล่าสุด result() คืน dict หรือ None ถ้ายังไม่มีผล
            # ในนั้นมี label (คลาสที่ชนะ) / conf / scores (คะแนนทุกคลาส) / seq / latency_ms
            r = edge_ai.result()
            if r and r['seq'] != last_seq:
                last_seq = r['seq']
                # หัวใจข้อสาม: เอาคลาสที่ชนะขึ้นจอ ถ้า label ว่างก็โชว์ '?'
                verdict.text(r['label'] or '-')
                conf.text("conf: %.0f %%" % (r['conf'] * 100))
                top = r['top']
                # ไล่ระบายแถบคะแนนทุกคลาส คลาสที่ชนะเป็นสีเขียว ที่เหลือสีจาง
                for i, (lb, br) in enumerate(rows):
                    if i < len(r['scores']):
                        br.value(int(r['scores'][i] * 100))
                        br.color(GREEN if i == top else DIM)

        time.sleep_ms(180)      # เว้นจังหวะ ไม่รัดจอจนกิน CPU เปล่า
except KeyboardInterrupt:
    pass
finally:
    edge_ai.stop()      # ออกจากงานยังไง ทิ้งเครื่องไว้ให้เรียบร้อยแบบนั้น
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
