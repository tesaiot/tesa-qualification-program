# 13 - Edge AI: Motion (IMU) ด้วย API ใหม่ edge_ai — เห็นคะแนนทุกคลาส + latency
#
# ฝาแฝดของตัวอย่าง 11 แต่ใช้โมดูล edge_ai (registry): ได้ scores ครบทุกคลาส
# และเวลาอนุมาน (latency_ms) ไม่ใช่แค่คลาสที่ชนะ
#
# ลองทำท่า: ถือบอร์ดวาดวงกลมในอากาศ / เขย่าบอร์ด / วางนิ่ง
import edge_ai
import ui
ui.screen()
import lcd
import time

PURPLE = 0xBB86FC
GREEN  = 0x50D890
DIM    = 0x6A3A31
CYAN   = 0x71C7EC
SEC    = 0xCFC6BF

lcd.clear()
lcd.console('<h2> Edge AI - Motion (edge_ai API)</h2>')


def find_model(keyword, sensor):
    """หาโมเดลตามชื่อ (เช่น 'Motion') ถ้าไม่เจอใช้เซนเซอร์ตรงกันตัวแรก"""
    ms = edge_ai.models()
    for m in ms:
        if keyword.lower() in m['name'].lower():
            return m
    for m in ms:
        if m['sensor'] == sensor:
            return m
    return ms[0]


model = find_model('Motion', edge_ai.SENSOR_IMU)
labels = model['labels']
lcd.console(' โมเดล: %s  คลาส: %s' % (model['name'], ", ".join(labels)))

# ---- สร้าง widget ครั้งเดียว ----
ui.Label("Edge AI - Motion", x=20, y=10, color=PURPLE)
verdict = ui.Seg7("---", x=40, y=55, color=GREEN)
lat = ui.Label("latency: -- ms", x=40, y=150, color=CYAN)
hint = ui.Label("วาดวงกลม / เขย่า / วางนิ่ง", x=40, y=185, color=SEC)

rows = []
for i in range(len(labels)):
    y = 60 + i * 40
    lb = ui.Label(labels[i], x=430, y=y, color=SEC)
    br = ui.Bar(x=430, y=y + 18, w=320, h=12, min=0, max=100, value=0, color=DIM)
    rows.append((lb, br))

back = ui.Button("< ออก", x=570, y=352, w=120, h=36)
back_id = back.id()

edge_ai.select(model['index'])
lcd.console('<span class=ok> เริ่มอนุมาน…</span>')

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
            # ช่อง debug: พิมพ์ผลผ่าน print() ก็ได้
            print(r['label'], "%.0f%%" % (r['conf'] * 100), "%.1fms" % r['latency_ms'])

        time.sleep_ms(180)
except KeyboardInterrupt:
    pass
finally:
    edge_ai.stop()
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
