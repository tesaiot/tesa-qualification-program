# s01_first_inference.py - รันโมเดล Edge AI ตัวแรกของเรา (ฉบับฝึกเติมโค้ด)
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) เติมช่องว่าง (pass) ทั้ง 4 จุดตามคำใบ้ในคอมเมนต์ให้ครบ
#          3) กด "Program to Device" แล้วลองเลือกโมเดลใน dropdown กด Load
#          4) ทำท่า/ส่งเสียงตามโมเดล แล้วดูคลาสที่ชนะ + แถบความมั่นใจบนจอ
#
# บอร์ดมีโมเดล DEEPCRAFT หลายตัวคอมไพล์รวมไว้ในเฟิร์มแวร์เดียว รันบน CM55 (NPU
# Ethos-U55) โมดูล edge_ai อ่าน "ทะเบียนโมเดล" จาก CM55 มาให้เรา แล้วสลับโมเดล
# ได้สดๆ ด้วยคำสั่งไม่กี่บรรทัด งานของเราชุดบทเรียนนี้คือเติม 4 คำสั่งหลักของ edge_ai

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

# อ่านทะเบียนโมเดลจาก CM55 (เป็นการ pull ผ่าน IPC — ปลอดภัย ไม่ค้าง)
# บรรทัดนี้ให้ไว้แล้ว เพราะทั้งไฟล์ต้องใช้ models ต่อ ลองอ่านว่าได้อะไรกลับมา
models = edge_ai.models()
names = [m['name'] for m in models]
lcd.console(' พบ %d โมเดลในเฟิร์มแวร์: %s' % (len(models), ", ".join(names)))

# สร้าง widget ครั้งเดียวก่อนเข้าลูป (สร้างซ้ำในลูปจะกินหน่วยความจำและจอกระพริบ)
ui.Label("Edge AI", x=20, y=8, color=PURPLE)
dd = ui.Dropdown(text="\n".join(names), x=20, y=42, w=250)
btn_load = ui.Button("Load", x=285, y=42, w=88, h=36)
btn_stop = ui.Button("Stop", x=381, y=42, w=88, h=36)
status = ui.Label("STOPPED", x=490, y=50, color=RED)

ui.Panel(x=20, y=92, w=300, h=150, color=CARD)
verdict = ui.Seg7("---", x=40, y=118, color=GREEN)
conf = ui.Label("conf: -- %", x=40, y=206, color=CYAN)

# แถวคะแนนต่อคลาส (โมเดลหนึ่งมีได้ถึง 8 คลาส) สร้างไว้ก่อนแล้วค่อยโชว์/ซ่อน
rows = []
for i in range(8):
    y = 96 + i * 30
    lb = ui.Label("", x=360, y=y, color=SEC)
    br = ui.Bar(x=360, y=y + 16, w=400, h=10, min=0, max=100, value=0, color=DIM)
    lb.hide()
    br.hide()
    rows.append((lb, br))

back = ui.Button("< ออก", x=650, y=352, w=120, h=36)
back_id = back.id()
dd_id = dd.id()
load_id = btn_load.id()
stop_id = btn_stop.id()


def show_rows(mi):
    """โชว์แถบคลาสของโมเดลที่เลือก (สร้างไว้แล้ว แค่เปลี่ยนข้อความ + โชว์/ซ่อน)"""
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
last_seq = -1
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
                sel = ev.get('value')
                verdict.text('---')
                conf.text("conf: -- %")
                show_rows(sel)
                lcd.console(' เลือก: %s (%s)'
                            % (models[sel]['name'], SENSOR[models[sel]['sensor']]))
            elif h == load_id:
                try:
                    # เติม: สั่งให้ CM55 รันโมเดลที่เลือก ด้วย edge_ai.select(sel)
                    pass
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
                # เติม: สั่งหยุดโมเดลด้วย edge_ai.stop()
                pass
                running = False
                status.text("STOPPED")
                status.color(RED)
                lcd.console(' หยุดโมเดล')

        if running:
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

        time.sleep_ms(180)
except KeyboardInterrupt:
    pass
finally:
    edge_ai.stop()      # ปิดเครื่องยนต์ให้เรียบร้อยเสมอ ไม่ปล่อยค้างรัน
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
