# 15 - Edge AI: Radar Push (เรดาร์ 60 GHz) — จำแนกท่าทางมือด้วยเรดาร์บนบอร์ด
#
# โมเดลเรดาร์เป็นแบบ float32 อ่านเฟรมจาก XENSIV BGT60TR13C จำแนกท่า push/gesture
# ยืนห่างบอร์ดประมาณ 60 ซม. แล้วดันมือเข้าหาเรดาร์
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
SEC    = 0xCFC6BF

lcd.clear()
lcd.console('<h2> Edge AI - Radar Push</h2>')


def find_model(keywords, sensor):
    ms = edge_ai.models()
    for m in ms:
        for k in keywords:
            if k.lower() in m['name'].lower():
                return m
    for m in ms:
        if m['sensor'] == sensor:
            return m
    return ms[0]


model = find_model(('Radar', 'Push', 'Gesture'), edge_ai.SENSOR_RADAR)
labels = model['labels']
lcd.console(' โมเดล: %s  คลาส: %s' % (model['name'], ", ".join(labels)))

ui.Label("Edge AI - Radar Push", x=20, y=10, color=PURPLE)
ui.Panel(x=20, y=55, w=340, h=150, color=CARD)
verdict = ui.Seg7("---", x=40, y=80, color=GREEN)
lat = ui.Label("latency: -- ms", x=40, y=165, color=CYAN)
hint = ui.Label("ยืนห่าง ~60 ซม. แล้วดันมือเข้าหาเรดาร์", x=20, y=225, color=SEC)

rows = []
for i in range(len(labels)):
    y = 62 + i * 40
    lb = ui.Label(labels[i], x=430, y=y, color=SEC)
    br = ui.Bar(x=430, y=y + 18, w=320, h=12, min=0, max=100, value=0, color=DIM)
    rows.append((lb, br))

back = ui.Button("< ออก", x=570, y=352, w=120, h=36)
back_id = back.id()

edge_ai.select(model['index'])
lcd.console('<span class=ok> เริ่มอ่านเรดาร์…</span>')

last_seq = -1
try:
    while True:
        for ev in ui.poll():
            if ev.get('handle') == back_id:
                raise KeyboardInterrupt

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
