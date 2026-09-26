# 16 - Edge AI: Sound Events (Cough / Alarm / Siren) — 3 โมเดลไมค์ ใน dropdown เดียว
#
# สามโมเดลเสียงจาก DEEPCRAFT Ready-Model (ไอ / เสียงเตือนโรงงาน / ไซเรน) รันบน
# ไมค์บนบอร์ด เลือกสลับได้สดๆ ด้วย edge_ai.select()
#
# หมายเหตุ: Ready-Model แบบ eval มีขีดจำกัดจำนวนครั้งการอนุมาน (inference count)
# ต่อการบูตหนึ่งครั้ง — ถ้าผลหยุดนิ่ง ให้รีบูตบอร์ด
import edge_ai
import ui
ui.screen()
import lcd
import time

PURPLE = 0xBB86FC
GREEN  = 0x50D890
DIM    = 0x6A3A31
CYAN   = 0x71C7EC
CARD   = 0x2A1712
RED    = 0xE85B5B
SEC    = 0xCFC6BF

lcd.clear()
lcd.console('<h2> Edge AI - Sound Events</h2>')

# เลือกเฉพาะโมเดลกลุ่มเสียงเหตุการณ์ (cough/alarm/siren) จากทะเบียนจริง
WANT = ('cough', 'alarm', 'siren')
events = []
for m in edge_ai.models():
    name = m['name'].lower()
    if any(w in name for w in WANT):
        events.append(m)
if not events:   # เผื่อชื่อไม่ตรง: ใช้โมเดลไมค์ทั้งหมด
    events = [m for m in edge_ai.models() if m['sensor'] == edge_ai.SENSOR_MIC]

names = [m['name'] for m in events]
lcd.console(' โมเดลเสียง: %s' % ", ".join(names))

ui.Label("Edge AI - Sound Events", x=20, y=8, color=PURPLE)
dd = ui.Dropdown(text="\n".join(names), x=20, y=42, w=250)
btn_load = ui.Button("Load", x=285, y=42, w=88, h=36)
btn_stop = ui.Button("Stop", x=381, y=42, w=88, h=36)
status = ui.Label("STOPPED", x=490, y=50, color=RED)

ui.Panel(x=20, y=92, w=300, h=150, color=CARD)
verdict = ui.Seg7("---", x=40, y=118, color=GREEN)
lat = ui.Label("latency: -- ms", x=40, y=206, color=CYAN)

rows = []
for i in range(8):
    y = 96 + i * 34
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
    labels = events[mi]['labels']
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


sel = 0
running = False
last_seq = -1
show_rows(sel)
lcd.console(' เลือกโมเดลเสียงแล้วกด Load')

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
                show_rows(sel)
                lcd.console(' เลือก: %s' % events[sel]['name'])
            elif h == load_id:
                try:
                    edge_ai.select(events[sel]['index'])
                    running = True
                    last_seq = -1
                    status.text("RUNNING")
                    status.color(GREEN)
                    lcd.console('<span class=ok> รัน %s</span>' % events[sel]['name'])
                except OSError as e:
                    status.text("ERROR")
                    status.color(RED)
                    lcd.console('<span class=error> โหลดไม่สำเร็จ: %s</span>' % e)
            elif h == stop_id:
                edge_ai.stop()
                running = False
                status.text("STOPPED")
                status.color(RED)

        if running:
            r = edge_ai.result()
            if r and r['seq'] != last_seq:
                last_seq = r['seq']
                verdict.text(r['label'] or '-')
                lat.text("latency: %.1f ms" % r['latency_ms'])
                top = r['top']
                for i, (lb, br) in enumerate(rows):
                    if i < len(r['scores']):
                        br.value(int(r['scores'][i] * 100))
                        br.color(GREEN if i == top else DIM)

        time.sleep_ms(180)
except KeyboardInterrupt:
    pass
finally:
    edge_ai.stop()
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
