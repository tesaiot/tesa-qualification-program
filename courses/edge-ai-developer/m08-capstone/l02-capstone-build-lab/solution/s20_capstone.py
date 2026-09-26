# s20_capstone.py - Capstone: Edge AI Guardian (เฉลย)
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) กด "Program to Device" (หรือ Run บน Emulator) แล้วกด Load
#          3) ทำท่า/ส่งเสียงตามโมเดล พอคลาสเป้าหมายชนะติดกันครบเกณฑ์ Guardian จะสั่งการเอง
#
# เฉลยนี้ไม่ได้มีไว้ลอกวาง หัวใจของ capstone อยู่ที่การออกแบบ + อธิบายเหตุผลเชิงวิศวกรรม
# ด้วยคำพูดของทีมเอง อ่านให้เข้าใจ ปิดไฟล์ แล้วประกอบใหม่ด้วยมือ ตอนพิมพ์เองนั่นแหละ
# สมองจะจับได้ว่า "ผลิตภัณฑ์ Edge AI หนึ่งชิ้น" คือการร้อยสามเสาเข้าด้วยกัน:
#   - เสา DAQ        อ่านเซนเซอร์ดิบ (sensors.bmi270) มาเป็นบริบทข้างๆ verdict
#   - เสา Processing กรองความมั่นใจให้นิ่งด้วย dsp.EMA + หน่วง (debounce) กันเตือนพร่ำ
#   - เสา Apps       edge_ai select/result -> ตัดสินใจ -> สั่งการ (เสียง+แบนเนอร์+นับครั้ง)
# ทั้งไฟล์ยังยืนอยู่บนคำสั่งหลักเดิม: models / select / result / stop + เพื่อนจาก dsp/sensors

import edge_ai
import ui
ui.screen()
import lcd
import sensors
import dsp
import time

# ---- ปุ่มออกแบบของ capstone: เปลี่ยนสี่ค่านี้ = เปลี่ยนพฤติกรรมทั้งผลิตภัณฑ์ ----
# นี่คือหัวใจของ "design->build->ship": ทีมตัดสินใจก่อนว่าจะเฝ้าอะไร ตอบไวแค่ไหน
# และยอมพลาด/ยอมเตือนเกินแค่ไหน แล้วค่าพวกนี้คือการตัดสินใจนั้นในรูปตัวเลข
MODEL_KEYWORD = "Motion"     # โมเดลที่ Guardian เฝ้า ("Baby Cry"/"Cough"/"Siren"/"Push"...)
HITS_NEEDED   = 3            # ต้องเจอคลาสเป้าหมายติดกันกี่ครั้งถึงจะสั่งการ (debounce)
EMA_ALPHA     = 0.4          # ความหนักของการกรองความมั่นใจ (มาก=ตอบไว, น้อย=นิ่งกว่า)
ACTION_NOTE   = 72           # โน้ต MIDI ของเสียงยืนยันตอนสั่งการ (60=โดกลาง, 72=โดสูง)

# ธีมสีเดียวกับหน้า Edge AI จริงบนบอร์ด (จะได้คุ้นตากับของจริง)
PURPLE = 0xBB86FC   # ชื่อ/หัวข้อ AI
GREEN  = 0x50D890   # คลาสที่ชนะ + ACTION ยิงแล้ว
AMBER  = 0xE0A03A   # ยังไม่ถึงเกณฑ์ความมั่นใจ (not sure)
DIM    = 0x6A3A31   # คลาสที่ไม่ชนะ
CYAN   = 0x71C7EC   # ความมั่นใจ / บริบทเซนเซอร์
RED    = 0xE85B5B   # error / รอจับ
CARD   = 0x2A1712   # พื้นการ์ดผลลัพธ์
SEC    = 0xCFC6BF   # ข้อความรอง

SENSOR = ("IMU", "RADAR", "MIC")

lcd.clear()
lcd.console('<h2> Edge AI Guardian - งานจบคอร์ส (เฉลย)</h2>')


def find_model(keyword):
    """หาโมเดลจากชื่อในทะเบียนของเฟิร์มแวร์ — ไม่เจอก็ใช้ตัวแรกกันแอปพัง
    ถามฮาร์ดแวร์ก่อน (models()) แทน hard-code index เพราะถ้าเฟิร์มแวร์สลับลำดับ
    โค้ดจะยังหาโมเดลถูกตัวจากชื่อได้เอง (นิสัยเดียวกับที่ปูมาตั้งแต่บทเรียน 1.1–1.3)"""
    ms = edge_ai.models()
    for m in ms:
        if keyword.lower() in m['name'].lower():
            return m
    return ms[0]


model = find_model(MODEL_KEYWORD)
labels = model['labels']
# กติกาออกแบบของ Guardian: "คลาสสุดท้าย" ของโมเดล = เหตุการณ์ที่เราสนใจ (เช่น shaking,
# baby_cry, Push, cough) ส่วนคลาสแรกมักเป็น idle/silence/unlabelled — ถ้าโมเดลของคุณ
# วางคลาสไว้คนละที่ ก็แค่แก้ alert_idx ให้ตรง นี่คือจุดออกแบบที่ควรจดเหตุผลลงบันทึกการเรียน
alert_idx = len(labels) - 1
alert_name = labels[alert_idx]
lcd.console(' โมเดล: %s (%s)  คลาส: %s'
            % (model['name'], SENSOR[model['sensor']], ", ".join(labels)))
lcd.console(' Guardian จะเฝ้า "%s" มั่นใจเกิน %.0f%% ติดกัน %d ครั้ง'
            % (alert_name, edge_ai.CONF_FLOOR * 100, HITS_NEEDED))

# เสา Processing: ตัวกรองความมั่นใจ สร้างครั้งเดียวก่อนลูป (มี .update(x)/.value()/.reset())
# EMA ถัวเฉลี่ยแบบถ่วงน้ำหนักอดีต ทำให้ conf ไม่กระโดดไปมาจนตัดสินใจพลาด
conf_ema = dsp.EMA(alpha=EMA_ALPHA)

# ---- สร้าง widget ครั้งเดียวก่อนเข้าลูป — สร้างซ้ำทุกวนรอบจะกินหน่วยความจำและจอกระพริบ ----
ui.Label("Edge AI Guardian", x=20, y=8, color=PURPLE)
btn_load = ui.Button("Load", x=250, y=6, w=88, h=34)
btn_stop = ui.Button("Stop", x=344, y=6, w=88, h=34)
status = ui.Label("STOPPED", x=448, y=14, color=RED)
hits_lab = ui.Label("alert: 0 ครั้ง", x=560, y=14, color=SEC)

ui.Panel(x=20, y=52, w=340, h=190, color=CARD)
verdict = ui.Seg7("---", x=40, y=76, color=GREEN)
conf = ui.Label("conf: -- %", x=40, y=162, color=CYAN)
ctx = ui.Label("motion: -- ", x=40, y=188, color=CYAN)     # บริบทจากเสา DAQ
banner = ui.Label("รอจับ %s ..." % alert_name, x=40, y=214, color=RED)

# แถวคะแนนต่อคลาส สร้างครบตามจำนวนคลาสของโมเดลนี้ตั้งแต่แรก แล้วในลูปแค่เปลี่ยนค่า
rows = []
for i in range(len(labels)):
    y = 60 + i * 40
    lb = ui.Label(labels[i], x=420, y=y, color=SEC)
    br = ui.Bar(x=420, y=y + 18, w=320, h=12, min=0, max=100, value=0, color=DIM)
    rows.append((lb, br))

back = ui.Button("< ออก", x=570, y=352, w=120, h=36)
back_id = back.id()
load_id = btn_load.id()
stop_id = btn_stop.id()

# สถานะที่ลูปกับตัวนับใช้ร่วมกัน
running = False
last_seq = -1
streak = 0          # เจอคลาสเป้าหมายติดกันมาแล้วกี่ครั้ง (ตัวหน่วง/debounce)
fired = False       # ยิง action ไปแล้วในรอบเหตุการณ์นี้หรือยัง (edge-trigger)
alert_count = 0


def fire_alert(label, conf_val):
    """verdict -> action: บี๊บ + แบนเนอร์ + นับจำนวนครั้ง + คอนโซล
    นี่คือปลายทางของทั้งสามเสา ในผลิตภัณฑ์จริง action ตรงนี้อาจเป็น เปิดไฟ / ส่ง MQTT /
    บันทึกเหตุการณ์ลงไฟล์ — ตอนนี้เราแทนด้วยเสียง+ข้อความเพื่อให้ 'เห็นผล' ได้ทันที"""
    global alert_count
    alert_count += 1
    banner.text("! ALERT: %s !" % label)
    banner.color(GREEN)
    hits_lab.text("alert: %d ครั้ง" % alert_count)
    if hasattr(ui, "tone"):
        ui.tone(ACTION_NOTE, ui.WAVE_SINE, 120, 150)
    lcd.console('<span class=ok> ACTION #%d: %s (conf %.0f%%)</span>'
                % (alert_count, label, conf_val * 100))


lcd.console(' กด Load แล้วทำท่า/ส่งเสียงให้ตรงคลาสเป้าหมาย')

try:
    while True:
        for ev in ui.poll():
            h = ev.get('handle')
            if h == back_id:
                raise KeyboardInterrupt
            elif h == load_id:
                try:
                    # เสา Apps (start): บอก CM55 ให้สลับมารันโมเดลที่เลือก — ห่อ try เพราะ
                    # ข้ามคอร์พลาดได้ ขึ้น RUNNING เฉพาะตอน select สำเร็จ ไม่โกหกผู้ใช้
                    edge_ai.select(model['index'])
                    running = True
                    last_seq = -1
                    streak = 0
                    fired = False
                    status.text("RUNNING")
                    status.color(GREEN)
                    conf_ema.reset()        # เริ่มเฝ้ารอบใหม่ ล้างประวัติตัวกรองให้สะอาด
                    lcd.console('<span class=ok> เริ่มเฝ้า %s</span>' % model['name'])
                except OSError as e:
                    status.text("ERROR")
                    status.color(RED)
                    lcd.console('<span class=error> โหลดไม่สำเร็จ: %s</span>' % e)
            elif h == stop_id:
                edge_ai.stop()
                running = False
                status.text("STOPPED")
                status.color(RED)
                banner.text("รอจับ %s ..." % alert_name)
                banner.color(RED)
                lcd.console(' หยุดเฝ้า')

        if running:
            # เสา DAQ: อ่านความเร่งดิบ 3 แกนมาเป็นบริบทข้างๆ verdict ผู้ใช้จะได้เห็นว่า
            # ตอนนี้อุปกรณ์ถูกจับ/สั่นอยู่ไหม (เผื่อ noise การจับรบกวนโมเดลเสียง)
            ax, ay, az = sensors.bmi270.acceleration()
            mag = (ax * ax + ay * ay + az * az) ** 0.5      # ขนาดเวกเตอร์ความเร่ง
            ctx.text("motion: %.1f" % mag)

            # เสา Apps (read): อ่านผลอนุมานล่าสุด result() คืน dict หรือ None ถ้ายังไม่มีผล
            r = edge_ai.result()
            if r and r['seq'] != last_seq:      # วาด/ตัดสินใจเฉพาะตอนมีผลใหม่ (seq เปลี่ยน)
                last_seq = r['seq']

                # เสา Processing: กรองความมั่นใจให้นิ่งด้วย EMA ก่อนเอาไปเทียบเกณฑ์ ลด
                # การตัดสินใจแกว่งจากพีคชั่วขณะ (.update คืนค่าที่กรองแล้วออกมาเลย)
                conf_s = conf_ema.update(r['conf'])

                sure = conf_s >= edge_ai.CONF_FLOOR
                verdict.text(r['label'] or '-')
                verdict.color(GREEN if sure else AMBER)
                conf.text("conf: %.0f %%%s"
                          % (conf_s * 100, "" if sure else "  (not sure)"))
                top = r['top']
                for i, (lb, br) in enumerate(rows):
                    if i < len(r['scores']):
                        br.value(int(r['scores'][i] * 100))
                        br.color(GREEN if i == top else DIM)

                # verdict -> decision: คลาสที่ชนะเป็นเป้าหมาย และมั่นใจ(กรองแล้ว)ถึงเกณฑ์ไหม
                hit = (top == alert_idx) and sure
                if hit:
                    streak += 1     # เจออีกครั้งติดกัน สะสม streak ขึ้น
                else:
                    streak = 0      # หลุดคลาสเป้าหมาย รีเซ็ตทั้ง streak และ fired
                    fired = False
                    banner.text("รอจับ %s ..." % alert_name)
                    banner.color(RED)

                # decision -> action: เจอติดกันครบเกณฑ์ HITS_NEEDED และยังไม่เคยยิงรอบนี้
                # เดี๋ยว "ติดกันครบ" คือ debounce ที่กันเตือนจากพีคหลอกเพียงเฟรมเดียว
                if streak >= HITS_NEEDED and not fired:
                    fire_alert(r['label'], conf_s)
                    fired = True    # ยิงครั้งเดียวต่อเหตุการณ์ ไม่รัวทุกเฟรมที่ยังเจออยู่

        time.sleep_ms(150)      # เว้นจังหวะ ไม่รัดจอจนกิน CPU เปล่า
except KeyboardInterrupt:
    pass
finally:
    edge_ai.stop()      # ออกจากงานยังไง ทิ้งเครื่องไว้ให้เรียบร้อยแบบนั้น
    lcd.console('<span class=ok> จบการทำงาน — สั่งการทั้งหมด %d ครั้ง</span>' % alert_count)

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
