# s16_action_pipeline.py - จาก verdict สู่ action จริง: RGB + เสียง + log (เฉลย)
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) กด "Program to Device" แล้วส่งเสียง/ทำท่าตามโมเดล (ตั้งต้นคือ Cough)
#          3) พอโมเดลจับคลาสเป้าหมายได้นานพอ ไฟ RGB เป็นแดง + เสียงเตือน + log ในคอนโซล
#
# เฉลยนี้ไม่ได้มีไว้ลอกวาง สิ่งที่นับคือการอธิบายด้วยคำพูดของคุณเอง
# อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์ใหม่ด้วยมือ ตอนพิมพ์เองสมองจะจับ pattern ได้ว่า
# "action pipeline" คือท่อ 4 ข้อต่อกัน: อ่านผล -> กรองความมั่นใจ -> debounce -> สั่งการ
# หัวใจของชุดบทเรียนนี้คือสองข้อกลาง (กรอง + debounce) เพราะมันคือเกราะกัน false positive:
# โมเดลตอบเป็นความน่าจะเป็น มันกระพริบผิดได้ ถ้าเรายิง action ทุกเฟรมก็จะเตือนพร่ำเพรื่อ

import edge_ai
import ui
ui.screen()
import lcd
import time

# ---- ปุ่มปรับพฤติกรรม pipeline (remix ตรงนี้เพื่อคุม false positive) ----
# ลองปรับ NEED_HITS ให้สูงขึ้น จะยิงยากขึ้นแต่พลาดของจริงมากขึ้น; ต่ำลงจะไวขึ้นแต่หลอกง่ายขึ้น
# นี่คือ trade-off จริงของงาน Edge AI: sensitivity แลกกับ false positive
MODEL_KEYWORD = "Cough"      # โมเดลที่จะเฝ้า ("Baby Cry"/"Siren"/"Alarm"/"Motion" ก็ได้)
TARGET_CLASS  = "cough"      # คลาสที่อยากดักจับ (ดู labels ในคอนโซลตอนรัน)
NEED_HITS     = 3            # ต้องจับคลาสเป้าหมายติดกันกี่เฟรมถึงจะยอมยิง (กันกระพริบ)
COOLDOWN_MS   = 3000         # หลังยิงแล้ว เว้นกี่ ms ก่อนยิงซ้ำได้ (refractory period)

# ธีมสีเดียวกับหน้า Edge AI จริงบนบอร์ด (จะได้คุ้นตากับของจริง)
PURPLE = 0xBB86FC   # ชื่อ/หัวข้อ AI
GREEN  = 0x50D890   # คลาสที่ชนะ
DIM    = 0x6A3A31   # คลาสที่ไม่ชนะ
CYAN   = 0x71C7EC   # ความมั่นใจ / เฝ้าดูอยู่
AMBER  = 0xE0A03A   # เจอเป้าหมายแล้ว แต่ยังยืนยันไม่ครบ
RED    = 0xE85B5B   # ALERT / error
CARD   = 0x2A1712   # พื้นการ์ดผลลัพธ์
SEC    = 0xCFC6BF   # ข้อความรอง
LIGHT_OFF = 0x444444  # ไฟ RGB ตอนยังไม่เจออะไร

SENSOR = ("IMU", "RADAR", "MIC")

lcd.clear()
lcd.console('<h2> Edge AI - Action Pipeline</h2>')


def find_model(keyword):
    """หาโมเดลจากชื่อในทะเบียนของเฟิร์มแวร์ — ไม่เจอใช้ตัวแรกกันแอปพัง
    ถาม models() แทน hard-code index เพราะถ้าเฟิร์มแวร์สลับลำดับ โค้ดยังหาถูกตัวจากชื่อ"""
    ms = edge_ai.models()
    for m in ms:
        if keyword.lower() in m['name'].lower():
            return m
    return ms[0]


model = find_model(MODEL_KEYWORD)
labels = model['labels']
lcd.console(' โมเดล: %s (%s)  คลาส: %s'
            % (model['name'], SENSOR[model['sensor']], ", ".join(labels)))
lcd.console(' ยิง action เมื่อเจอ "%s" ติดกัน %d เฟรม + มั่นใจเกิน %.0f%%'
            % (TARGET_CLASS, NEED_HITS, edge_ai.CONF_FLOOR * 100))

# ---- สร้าง widget ครั้งเดียวก่อนลูป — สร้างซ้ำทุกวนรอบจะกินหน่วยความจำและจอกระพริบ ----
ui.Label("Edge AI - Action Pipeline", x=20, y=8, color=PURPLE)
ui.Panel(x=20, y=48, w=330, h=180, color=CARD)
verdict = ui.Seg7("---", x=40, y=72, color=GREEN)
conf = ui.Label("conf: -- %", x=40, y=160, color=CYAN)
streak_lab = ui.Label("streak: 0/%d" % NEED_HITS, x=40, y=186, color=SEC)

# "ไฟ RGB" บนจอ = การ์ดสีที่เปลี่ยนตามสถานะ pipeline — นี่คือ action ช่องภาพ
# เทา=ว่าง  ฟ้า=กำลังเฝ้า  เหลือง=เจอเป้าหมายแต่ยังไม่ครบ  แดง=ยิงแล้ว
light = ui.Panel(x=380, y=48, w=120, h=120, color=LIGHT_OFF)
light_lab = ui.Label("IDLE", x=400, y=178, color=SEC)
hits_lab = ui.Label("alerts: 0", x=560, y=8, color=SEC)

# แถวคะแนนต่อคลาส สร้างครบตามจำนวนคลาสของโมเดลนี้ตั้งแต่แรก แล้วในลูปแค่เปลี่ยนค่า
rows = []
for i in range(len(labels)):
    y = 60 + i * 40
    lb = ui.Label(labels[i], x=540, y=y, color=SEC)
    br = ui.Bar(x=540, y=y + 18, w=210, h=12, min=0, max=100, value=0, color=DIM)
    rows.append((lb, br))

back = ui.Button("< ออก", x=570, y=352, w=120, h=36)
back_id = back.id()

# สถานะของ pipeline (ตัวแปรที่ทั้งลูปและ fire_action ใช้ร่วมกัน)
streak = 0            # จับคลาสเป้าหมายติดกันมากี่เฟรมแล้ว (ตัวนับ debounce)
alerts = 0            # ยิง action ไปแล้วกี่ครั้ง (ไว้ทำ log)
last_fire = time.ticks_ms()  # เวลาที่ยิงครั้งล่าสุด (ฐานของ cooldown)


def set_light(color, text):
    """action ช่องที่ 1 — ไฟ RGB บนจอ: เปลี่ยนสี + ป้ายสถานะตามขั้นของ pipeline"""
    light.color(color)
    light_lab.text(text)


def fire_action(conf_val):
    """verdict -> action จริง 3 ช่องพร้อมกัน: ไฟแดง + เสียงเตือน + บันทึก log
    ในงานจริง ตรงนี้อาจเป็น เปิดรีเลย์ / ส่งแจ้งเตือน MQTT / เขียนไฟล์เหตุการณ์
    (บทเรียน 6.5–6.6 เราจะต่อ action นี้ออกเน็ตด้วย WiFi/MQTT)"""
    global alerts
    alerts += 1
    set_light(RED, "ALERT")                    # ช่องภาพ
    hits_lab.text("alerts: %d" % alerts)
    if hasattr(ui, "tone"):
        ui.tone(76, ui.WAVE_SINE, 140, 160)    # ช่องเสียง: โน้ต MIDI 76 = มีสูง
    lcd.console('<span class=error> ALERT #%d: %s (conf %.0f%%)</span>'   # ช่อง log
                % (alerts, TARGET_CLASS, conf_val * 100))


# ---- สั่งให้ CM55 เริ่มรันโมเดลที่เลือก (confirm by observation เหมือนบทเรียน 1.1–1.3) ----
try:
    edge_ai.select(model['index'])
    lcd.console('<span class=ok> เริ่มอนุมาน…</span>')
except OSError as e:
    lcd.console('<span class=error> โหลดไม่สำเร็จ: %s</span>' % e)

last_seq = -1
try:
    while True:
        for ev in ui.poll():
            if ev.get('handle') == back_id:
                raise KeyboardInterrupt

        # ท่อข้อ 1 — อ่านผลอนุมานล่าสุด result() คืน dict หรือ None ถ้ายังไม่มีผล
        r = edge_ai.result()
        if r and r['seq'] != last_seq:      # ทำงานเฉพาะตอนมีผลใหม่ (seq เปลี่ยน)
            last_seq = r['seq']
            verdict.text(r['label'] or '-')
            conf.text("conf: %.0f %%" % (r['conf'] * 100))
            top = r['top']
            for i, (lb, br) in enumerate(rows):
                if i < len(r['scores']):
                    br.value(int(r['scores'][i] * 100))
                    br.color(GREEN if i == top else DIM)

            # ท่อข้อ 2 — ด่านกรอง false positive: เฟรมนี้ "นับเป็นการเจอเป้าหมาย" ไหม
            # นับก็ต่อเมื่อคลาสที่ชนะตรงเป้าหมาย และมั่นใจไม่ต่ำกว่าเกณฑ์ CONF_FLOOR
            # (ถ้าไม่กรอง conf โมเดลเดาแบบไม่มั่นใจก็จะถูกนับด้วย = หลอกง่าย)
            hit = (r['label'] == TARGET_CLASS and r['conf'] >= edge_ai.CONF_FLOOR)

            if hit:
                streak += 1                 # เจอต่อเนื่อง เพิ่ม streak
                if streak < NEED_HITS:
                    set_light(AMBER, "%d/%d" % (streak, NEED_HITS))
            else:
                streak = 0                  # หลุดคลาสเป้าหมาย รีเซ็ต streak ทันที
                set_light(CYAN, "watching")
            streak_lab.text("streak: %d/%d" % (streak, NEED_HITS))

            now = time.ticks_ms()
            cooled = time.ticks_diff(now, last_fire) >= COOLDOWN_MS  # พ้น cooldown แล้วไหม
            ready = streak >= NEED_HITS                              # จับครบจำนวนเฟรมหรือยัง
            # ท่อข้อ 3 — debounce: ยิงได้ก็ต่อเมื่อจับครบต่อเนื่อง "และ" พ้นช่วงเว้นแล้ว
            # streak คือ debounce เชิงเวลา (กันกระพริบ) · cooldown กันยิงรัวถี่ๆ ตอนเจอค้าง
            should_fire = ready and cooled
            if should_fire:
                # ท่อข้อ 4 — ยิง action จริง แล้วรีเซ็ตให้พร้อมรอบใหม่
                fire_action(r['conf'])
                last_fire = now
                streak = 0

        time.sleep_ms(150)      # เว้นจังหวะ ไม่รัดจอจนกิน CPU เปล่า
except KeyboardInterrupt:
    pass
finally:
    edge_ai.stop()      # ออกจากงานยังไง ทิ้งเครื่องไว้ให้เรียบร้อยแบบนั้น
    lcd.console('<span class=ok> จบการทำงาน — ยิง action ทั้งหมด %d ครั้ง</span>' % alerts)

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
