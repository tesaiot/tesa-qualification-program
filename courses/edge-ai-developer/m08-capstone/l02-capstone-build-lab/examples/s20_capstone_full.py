# s20_capstone_full.py - Capstone: Edge AI Guardian (ฉบับเต็ม)
# วิธีรัน: เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator (ide.tesaiot.dev)
#          กด "Program to Device" (หรือ Run) เลือกโมเดลใน dropdown แล้วกด Load
#
# ฉบับนี้คือเวอร์ชันที่ขัดจนเรียบร้อยของ s20_capstone.py — โครงสามเสาเดียวกับไฟล์ฝึก
# (DAQ อ่านเซนเซอร์ดิบ / Processing กรอง+หน่วง / Apps verdict->action) แต่ยกระดับให้
# ใกล้ "ผลิตภัณฑ์ที่ส่งมอบได้" มากขึ้น:
#   1) เลือกโมเดลได้สดจาก dropdown (ทั้งทะเบียนจากเฟิร์มแวร์) ไม่ต้องแก้ค่าคงที่ในโค้ด
#   2) โชว์ latency ของ NPU + ความมั่นใจที่กรองแล้ว + บริบทการเคลื่อนไหวจากเสา DAQ
#   3) debounce ด้วย streak + edge-trigger กันเตือนซ้ำ + นับจำนวนครั้งที่สั่งการ
# ทั้งหมดยังยืนอยู่บนคำสั่งหลักเดิม: models / select / result / stop + dsp/sensors

import edge_ai
import ui
ui.screen()
import lcd
import sensors
import dsp
import time

# ---- ปุ่มออกแบบของ capstone: ตัวเลขพวกนี้คือ "การตัดสินใจเชิงวิศวกรรม" ในรูปตัวเลข ----
HITS_NEEDED = 3            # เจอคลาสเป้าหมายติดกันกี่ครั้งถึงจะสั่งการ (debounce)
EMA_ALPHA   = 0.4          # ความหนักของการกรองความมั่นใจ (มาก=ตอบไว, น้อย=นิ่งกว่า)
ACTION_NOTE = 72           # โน้ต MIDI ของเสียงยืนยันตอนสั่งการ (60=โดกลาง, 72=โดสูง)

# ธีมสีเดียวกับหน้า Edge AI จริงบนบอร์ด
PURPLE = 0xBB86FC   # ชื่อ/หัวข้อ AI
GREEN  = 0x50D890   # คลาสที่ชนะ (มั่นใจ) + ACTION ยิงแล้ว
AMBER  = 0xE0A03A   # ยังไม่ถึงเกณฑ์ความมั่นใจ (not sure)
DIM    = 0x6A3A31   # คลาสที่ไม่ชนะ
CYAN   = 0x71C7EC   # ความมั่นใจ / latency / บริบทเซนเซอร์
RED    = 0xE85B5B   # STOPPED / error / รอจับ
CARD   = 0x2A1712   # พื้นการ์ดผลลัพธ์
SEC    = 0xCFC6BF   # ข้อความรอง

SENSOR = ("IMU", "RADAR", "MIC")

lcd.clear()
lcd.console('<h2> Edge AI Guardian - งานจบคอร์ส (ฉบับเต็ม)</h2>')
lcd.console(' links: %s' % str(edge_ai.links()))

# ทะเบียนโมเดลจาก CM55 — ค่าจริงจากเฟิร์มแวร์ ไม่ใช่ค่าที่เราสมมติ
models = edge_ai.models()
names = [m['name'] for m in models]
lcd.console(' พบ %d โมเดล: %s' % (len(models), ", ".join(names)))
lcd.console(' เกณฑ์ความมั่นใจ (CONF_FLOOR) = %.0f %% · debounce = %d ครั้ง'
            % (edge_ai.CONF_FLOOR * 100, HITS_NEEDED))

# เสา Processing: ตัวกรองความมั่นใจ สร้างครั้งเดียว ใช้ซ้ำทุกโมเดล (reset ตอน Load)
conf_ema = dsp.EMA(alpha=EMA_ALPHA)

# ---- สร้าง widget ครั้งเดียวก่อนลูป ----
ui.Label("Edge AI Guardian", x=20, y=8, color=PURPLE)
dd = ui.Dropdown(text="\n".join(names), x=200, y=6, w=230)
btn_load = ui.Button("Load", x=442, y=6, w=80, h=34)
btn_stop = ui.Button("Stop", x=528, y=6, w=80, h=34)
status = ui.Label("STOPPED", x=624, y=14, color=RED)

ui.Panel(x=20, y=52, w=340, h=196, color=CARD)
verdict = ui.Seg7("---", x=40, y=74, color=GREEN)
conf = ui.Label("conf: -- %", x=40, y=160, color=CYAN)
lat = ui.Label("latency: -- ms", x=40, y=184, color=CYAN)
ctx = ui.Label("motion: -- ", x=40, y=208, color=CYAN)         # บริบทจากเสา DAQ
banner = ui.Label("เลือกโมเดล แล้วกด Load", x=40, y=228, color=RED)
hits_lab = ui.Label("alert: 0 ครั้ง", x=380, y=352, color=SEC)

# แถวคะแนนต่อคลาส (สูงสุด 8) สร้างไว้ก่อน แล้วโชว์เฉพาะคลาสของโมเดลที่เลือก
rows = []
for i in range(8):
    y = 60 + i * 34
    lb = ui.Label("", x=420, y=y, color=SEC)
    br = ui.Bar(x=420, y=y + 16, w=320, h=11, min=0, max=100, value=0, color=DIM)
    lb.hide()
    br.hide()
    rows.append((lb, br))

back = ui.Button("< ออก", x=570, y=352, w=120, h=36)
back_id = back.id()
dd_id = dd.id()
load_id = btn_load.id()
stop_id = btn_stop.id()

# สถานะรวมของ Guardian
sel = 0
running = False
last_seq = -1
streak = 0
fired = False
alert_count = 0
alert_idx = 0
alert_name = ""


def show_rows(mi):
    """โชว์แถบคลาสของโมเดลที่เลือก + คำนวณ 'คลาสเป้าหมาย' (คลาสสุดท้าย = เหตุการณ์ที่สนใจ)"""
    global alert_idx, alert_name
    labels = models[mi]['labels']
    alert_idx = len(labels) - 1
    alert_name = labels[alert_idx]
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
    """คืนการ์ดผลลัพธ์สู่สถานะว่าง (ใช้ตอนสลับโมเดล/หยุด)"""
    verdict.text('---')
    verdict.color(GREEN)
    conf.text("conf: -- %")
    lat.text("latency: -- ms")


def fire_alert(label, conf_val, lat_ms):
    """verdict -> action ปลายทางของทั้งสามเสา: บี๊บ + แบนเนอร์ + นับครั้ง + คอนโซล
    ในผลิตภัณฑ์จริง action ตรงนี้คือ เปิดไฟ / ส่ง MQTT / บันทึกเหตุการณ์ — สลับได้ทันที"""
    global alert_count
    alert_count += 1
    banner.text("! ALERT: %s !" % label)
    banner.color(GREEN)
    hits_lab.text("alert: %d ครั้ง" % alert_count)
    if hasattr(ui, "tone"):
        ui.tone(ACTION_NOTE, ui.WAVE_SINE, 120, 150)
    lcd.console('<span class=ok> ACTION #%d: %s (conf %.0f%%, %.1f ms)</span>'
                % (alert_count, label, conf_val * 100, lat_ms))


def reset_watch():
    """เริ่มเฝ้ารอบใหม่: ล้างตัวกรอง + debounce + edge-trigger ให้สะอาด"""
    global last_seq, streak, fired
    last_seq = -1
    streak = 0
    fired = False
    conf_ema.reset()


show_rows(sel)
lcd.console(' เลือกโมเดลใน dropdown แล้วกด Load เพื่อเริ่มเฝ้า')

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
                banner.text("รอ Load %s ..." % models[sel]['name'])
                banner.color(RED)
                lcd.console(' เลือก: %s (%s) — เป้าหมาย "%s"'
                            % (models[sel]['name'], SENSOR[models[sel]['sensor']], alert_name))
            elif h == load_id:
                try:
                    edge_ai.select(sel)
                    running = True
                    reset_watch()
                    status.text("RUNNING")
                    status.color(GREEN)
                    banner.text("รอจับ %s ..." % alert_name)
                    banner.color(RED)
                    lcd.console('<span class=ok> เริ่มเฝ้า %s</span>' % models[sel]['name'])
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
                banner.text("หยุดเฝ้าแล้ว")
                banner.color(RED)
                lcd.console(' หยุดเฝ้า')

        if running:
            # เสา DAQ: อ่านความเร่งดิบมาเป็นบริบท — ผู้ใช้เห็นว่าอุปกรณ์นิ่งหรือถูกจับอยู่
            ax, ay, az = sensors.bmi270.acceleration()
            mag = (ax * ax + ay * ay + az * az) ** 0.5
            ctx.text("motion: %.1f" % mag)

            # เสา Apps: อ่าน verdict ล่าสุด แล้วทำงานเฉพาะตอนมีผลใหม่ (seq เปลี่ยน)
            r = edge_ai.result()
            if r and r['seq'] != last_seq:
                last_seq = r['seq']

                # เสา Processing: กรอง conf ให้นิ่งก่อนเทียบเกณฑ์ ลดการแกว่งจากพีคชั่วขณะ
                conf_s = conf_ema.update(r['conf'])
                sure = conf_s >= edge_ai.CONF_FLOOR

                verdict.text(r['label'] or '-')
                verdict.color(GREEN if sure else AMBER)
                conf.text("conf: %.0f %%%s"
                          % (conf_s * 100, "" if sure else "  (not sure)"))
                lat.text("latency: %.1f ms" % r['latency_ms'])
                top = r['top']
                for i, (lb, br) in enumerate(rows):
                    if i < len(r['scores']):
                        br.value(int(r['scores'][i] * 100))
                        br.color(GREEN if i == top else DIM)

                # verdict -> decision -> action: ต้องเป็นคลาสเป้าหมาย + มั่นใจ + ติดกันครบเกณฑ์
                hit = (top == alert_idx) and sure
                if hit:
                    streak += 1
                else:
                    streak = 0
                    fired = False
                    banner.text("รอจับ %s ..." % alert_name)
                    banner.color(RED)

                if streak >= HITS_NEEDED and not fired:
                    fire_alert(r['label'], conf_s, r['latency_ms'])
                    fired = True

        time.sleep_ms(150)
except KeyboardInterrupt:
    pass
finally:
    edge_ai.stop()
    lcd.console('<span class=ok> จบการทำงาน — สั่งการทั้งหมด %d ครั้ง</span>' % alert_count)

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
