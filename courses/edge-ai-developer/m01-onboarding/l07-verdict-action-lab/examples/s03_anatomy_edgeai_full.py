# s03_anatomy_edgeai_full.py - เฝ้าจับคลาสด้วย on_result แล้วสั่งการ (ฉบับเต็ม)
# วิธีรัน: เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator (ide.tesaiot.dev)
#          กด "Program to Device" แล้วทำท่า/ส่งเสียงตามโมเดลที่เลือก
#
# ฉบับนี้คือเวอร์ชันที่ขัดจนเรียบร้อยของ s03_anatomy_edgeai.py — โครงเดียวกับที่คุณ
# เติมในไฟล์ฝึก แต่ยกระดับ "verdict -> action" สองเรื่อง:
#   1) ใช้ edge_ai.on_result(cb) แทนการ poll เอง — เฟิร์มแวร์เรียก callback ให้เรา
#      ทันทีที่คลาสเปลี่ยน (และทวนคลาสเดิมราววินาทีละครั้ง) เราจึงไม่ต้องเช็ก seq เองอีก โค้ดในลูปเหลือแค่รับปุ่ม
#   2) แยก "มั่นใจ/ยังไม่ชัวร์" ด้วย CONF_FLOOR + โชว์ latency + นับจำนวนครั้งที่สั่งการ
# ทั้งหมดยังยืนอยู่บนคำสั่งหลักของ edge_ai: models / select / result / on_result / stop

import edge_ai
import ui
ui.screen()
import lcd
import time

# ---- remix ตรงนี้: สลับโมเดล + เลือกคลาสเป้าหมาย + เลือกเสียง action ----
MODEL_KEYWORD = "Motion"     # "Baby Cry" / "Cough" / "Siren" / "Push" ...
TARGET_CLASS  = "shaking"    # คลาสที่อยากจับแล้วสั่งการ
ACTION_NOTE   = 72           # โน้ต MIDI ของเสียงยืนยัน (60=โดกลาง, 72=โดสูง)

# ธีมสีเดียวกับหน้า Edge AI จริงบนบอร์ด
PURPLE = 0xBB86FC   # ชื่อ/หัวข้อ AI
GREEN  = 0x50D890   # คลาสที่ชนะ (มั่นใจ) + ACTION ยิงแล้ว
AMBER  = 0xE0A03A   # ผลที่ยังไม่ถึงเกณฑ์ความมั่นใจ (not sure)
DIM    = 0x6A3A31   # คลาสที่ไม่ชนะ
CYAN   = 0x71C7EC   # ความมั่นใจ / latency
RED    = 0xE85B5B   # error / รอจับ
CARD   = 0x2A1712   # พื้นการ์ดผลลัพธ์
SEC    = 0xCFC6BF   # ข้อความรอง

SENSOR = ("IMU", "RADAR", "MIC")

lcd.clear()
lcd.console('<h2> Edge AI - watcher (on_result, ฉบับเต็ม)</h2>')


def find_model(keyword):
    """หาโมเดลจากชื่อในทะเบียน — ไม่เจอใช้ตัวแรก (ถามฮาร์ดแวร์ ไม่ hard-code index)"""
    ms = edge_ai.models()
    for m in ms:
        if keyword.lower() in m['name'].lower():
            return m
    return ms[0]


model = find_model(MODEL_KEYWORD)
labels = model['labels']
lcd.console(' โมเดล: %s (%s)  คลาส: %s'
            % (model['name'], SENSOR[model['sensor']], ", ".join(labels)))
lcd.console(' เกณฑ์ความมั่นใจ (CONF_FLOOR) = %.0f %%' % (edge_ai.CONF_FLOOR * 100))
lcd.console(' จะสั่งการเมื่อเจอ "%s" เกินเกณฑ์' % TARGET_CLASS)

# ---- สร้าง widget ครั้งเดียวก่อนลูป ----
ui.Label("Edge AI - watcher", x=20, y=8, color=PURPLE)
ui.Panel(x=20, y=48, w=340, h=170, color=CARD)
verdict = ui.Seg7("---", x=40, y=72, color=GREEN)
conf = ui.Label("conf: -- %", x=40, y=158, color=CYAN)
lat = ui.Label("latency: -- ms", x=40, y=182, color=CYAN)
banner = ui.Label("รอจับ %s ..." % TARGET_CLASS, x=40, y=232, color=RED)
hits_lab = ui.Label("จับได้: 0 ครั้ง", x=560, y=8, color=SEC)

# แถวคะแนนต่อคลาส สร้างครบตามจำนวนคลาสของโมเดล
rows = []
for i in range(len(labels)):
    y = 60 + i * 40
    lb = ui.Label(labels[i], x=420, y=y, color=SEC)
    br = ui.Bar(x=420, y=y + 18, w=320, h=12, min=0, max=100, value=0, color=DIM)
    rows.append((lb, br))

back = ui.Button("< ออก", x=570, y=352, w=120, h=36)
back_id = back.id()

# สถานะที่ callback กับลูปใช้ร่วมกัน
state = {'fired': False, 'hits': 0}


def fire_action(conf_val):
    """verdict -> action: บี๊บ + แบนเนอร์ + นับจำนวนครั้ง (ในงานจริงคือเปิดไฟ/แจ้งเตือน)"""
    state['hits'] += 1
    banner.text("! เจอ %s !" % TARGET_CLASS)
    banner.color(GREEN)
    hits_lab.text("จับได้: %d ครั้ง" % state['hits'])
    if hasattr(ui, "tone"):
        ui.tone(ACTION_NOTE, ui.WAVE_SINE, 120, 150)
    lcd.console('<span class=ok> ACTION #%d: เจอ %s (conf %.0f%%)</span>'
                % (state['hits'], TARGET_CLASS, conf_val * 100))


def on_change(r):
    """เฟิร์มแวร์เรียกให้เมื่อมีคำตัดสิน (คลาสเปลี่ยน หรือทวนราววินาทีละครั้ง) — รันใน scheduler context ปลอดภัยกับ UI
    เราจึงวาดจอ + ตัดสินใจ action ได้ตรงนี้เลย ไม่ต้อง poll/เช็ก seq เองในลูป"""
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

    # verdict -> decision -> action (edge-trigger: ยิงครั้งเดียวตอนเพิ่งเข้าคลาสเป้าหมาย)
    hit = (r['label'] == TARGET_CLASS and sure)
    if hit and not state['fired']:
        fire_action(r['conf'])
        state['fired'] = True
    elif not hit:
        state['fired'] = False
        banner.text("รอจับ %s ..." % TARGET_CLASS)
        banner.color(RED)


# ---- ต่อ callback แล้วสั่งเริ่มอนุมาน ----
edge_ai.on_result(on_change)        # ลงทะเบียน callback ก่อน select เพื่อไม่พลาดผลแรก
try:
    edge_ai.select(model['index'])
    lcd.console('<span class=ok> เริ่มอนุมาน…</span>')
except OSError as e:
    lcd.console('<span class=error> โหลดไม่สำเร็จ: %s</span>' % e)

# ลูปหลักเหลือแค่รับปุ่ม — งานอ่านผล/วาดจอ/สั่งการ ย้ายไปอยู่ใน on_change หมดแล้ว
try:
    while True:
        for ev in ui.poll():
            if ev.get('handle') == back_id:
                raise KeyboardInterrupt
        time.sleep_ms(120)
except KeyboardInterrupt:
    pass
finally:
    edge_ai.on_result(None)     # ถอน callback ก่อนออก (คู่กับตอนลงทะเบียน)
    edge_ai.stop()
    lcd.console('<span class=ok> จบการทำงาน — จับได้ทั้งหมด %d ครั้ง</span>'
                % state['hits'])

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
