# s01_first_inference_full.py - เมนู Edge AI 6 โมเดล (ฉบับเต็ม)
# วิธีรัน: เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator (ide.tesaiot.dev)
#          กด "Program to Device" แล้วเลือกโมเดลใน dropdown กด Load
#
# ฉบับนี้คือเวอร์ชันที่ขัดจนเรียบร้อยของ s01_first_inference.py — โครงเดียวกับ
# ที่คุณเติมในไฟล์ฝึก แต่เพิ่มรายละเอียดที่ทำให้ "อ่านผลได้แม่นขึ้น": โชว์เวลา
# อนุมาน (latency), ใช้เกณฑ์ความมั่นใจ CONF_FLOOR แยก "มั่นใจ" ออกจาก "ยังไม่ชัวร์"
# และเน้นคลาสที่ชนะให้เห็นง่าย ทั้งหมดยังยืนอยู่บนคำสั่งหลัก 4 ตัวของ edge_ai

import edge_ai
import ui
ui.screen()
import lcd
import time

# ธีมสีเดียวกับหน้า Edge AI จริงบนบอร์ด
PURPLE = 0xBB86FC   # ชื่อ/หัวข้อ AI
GREEN  = 0x50D890   # คลาสที่ชนะ (มั่นใจ) + สถานะ RUNNING
AMBER  = 0xE0A03A   # ผลที่ยังไม่ถึงเกณฑ์ความมั่นใจ (not sure)
DIM    = 0x6A3A31   # คลาสที่ไม่ชนะ
CYAN   = 0x71C7EC   # latency
RED    = 0xE85B5B   # STOPPED / error
CARD   = 0x2A1712   # พื้นการ์ดผลลัพธ์
SEC    = 0xCFC6BF   # ข้อความรอง

SENSOR = ("IMU", "RADAR", "MIC")

lcd.clear()
lcd.console('<h2> Edge AI - เมนูโมเดล (ฉบับเต็ม)</h2>')
lcd.console(' links: %s' % str(edge_ai.links()))

# ทะเบียนโมเดลจาก CM55 — ค่าจริงจากเฟิร์มแวร์ ไม่ใช่ค่าที่เราสมมติ
models = edge_ai.models()
names = [m['name'] for m in models]
lcd.console(' พบ %d โมเดล: %s' % (len(models), ", ".join(names)))
lcd.console(' เกณฑ์ความมั่นใจ (CONF_FLOOR) = %.0f %%' % (edge_ai.CONF_FLOOR * 100))

# ---- สร้าง widget ครั้งเดียวก่อนลูป ----
ui.Label("Edge AI", x=20, y=8, color=PURPLE)
dd = ui.Dropdown(text="\n".join(names), x=20, y=42, w=250)
btn_load = ui.Button("Load", x=285, y=42, w=88, h=36)
btn_stop = ui.Button("Stop", x=381, y=42, w=88, h=36)
status = ui.Label("STOPPED", x=490, y=50, color=RED)

ui.Panel(x=20, y=92, w=300, h=150, color=CARD)
verdict = ui.Seg7("---", x=40, y=118, color=GREEN)
conf = ui.Label("conf: -- %", x=40, y=196, color=CYAN)
lat = ui.Label("latency: -- ms", x=40, y=220, color=CYAN)

# แถวคะแนนต่อคลาส (สูงสุด 8) สร้างไว้ก่อน แล้วโชว์เฉพาะคลาสของโมเดลที่เลือก
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
    """โชว์แถบคลาสของโมเดลที่เลือก (สร้างไว้แล้ว แค่โชว์/ซ่อน)"""
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


def clear_verdict():
    """คืนการ์ดผลลัพธ์กลับสู่สถานะว่าง (ใช้ตอนสลับโมเดล/หยุด)"""
    verdict.text('---')
    verdict.color(GREEN)
    conf.text("conf: -- %")
    lat.text("latency: -- ms")


sel = 0            # โมเดลที่เลือกใน dropdown (เริ่มที่ index 0 = Motion Detection)
running = False
last_seq = -1
show_rows(sel)
lcd.console(' เลือกโมเดลใน dropdown แล้วกด Load')

try:
    while True:
        for ev in ui.poll():
            h = ev.get('handle')
            t = ev.get('type')
            if h == back_id:
                raise KeyboardInterrupt
            elif h == dd_id and t == 'value_changed':
                sel = ev.get('value')
                clear_verdict()
                show_rows(sel)
                lcd.console(' เลือก: %s (%s)'
                            % (models[sel]['name'], SENSOR[models[sel]['sensor']]))
            elif h == load_id:
                try:
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
                edge_ai.stop()
                running = False
                status.text("STOPPED")
                status.color(RED)
                clear_verdict()
                lcd.console(' หยุดโมเดล')

        # อัปเดตเฉพาะตอนมีผลอนุมานใหม่ (seq เปลี่ยน) — ไม่วาดจอทุกเฟรม
        if running:
            r = edge_ai.result()
            if r and r['seq'] != last_seq:
                last_seq = r['seq']
                # แยก "มั่นใจ" ออกจาก "ยังไม่ชัวร์": ต่ำกว่า CONF_FLOOR ให้เป็นสีเหลือง
                sure = r['conf'] >= edge_ai.CONF_FLOOR
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

        time.sleep_ms(150)
except KeyboardInterrupt:
    pass
finally:
    edge_ai.stop()
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
