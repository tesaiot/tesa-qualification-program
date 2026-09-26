# s16_action_pipeline.py - จาก verdict สู่ action จริง: RGB + เสียง + log (ฉบับฝึกเติมโค้ด)
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) เติมช่องว่าง (pass) ทั้ง 4 จุดตามคำใบ้ในคอมเมนต์ให้ครบ
#          3) กด "Program to Device" แล้วส่งเสียง/ทำท่าตามโมเดล (ตั้งต้นคือ Cough)
#          4) พอโมเดลจับคลาสเป้าหมายได้ "นานพอ" ไฟ RGB บนจอจะเป็นสีแดง + มีเสียงเตือน
#             + คอนโซลบันทึกเหตุการณ์ นั่นคือ action pipeline ที่เราต่อขึ้นเอง
#
# บทเรียน 1.1–1.3 เราแค่ "อ่านผล" ชุดบทเรียนนี้เราเอาผล (verdict) ไป "สั่งการ" (action) จริง แต่โมเดล
# ไม่ได้มั่นใจ 100% เสมอ ถ้ายิง action ทุกครั้งที่คลาสกระพริบมาแวบเดียว จะเตือนพร่ำเพรื่อ
# (false positive) งานของชุดบทเรียนนี้คือต่อ "ท่อ" 4 ข้อ: อ่านผล -> กรองความมั่นใจ ->
# debounce (ต้องจับได้ต่อเนื่องหลายเฟรม + เว้นช่วง) -> ค่อยสั่งการ

import edge_ai
import ui
ui.screen()
import lcd
import time

# ---- ปุ่มปรับพฤติกรรม pipeline (remix ตรงนี้เพื่อคุม false positive) ----
MODEL_KEYWORD = "Cough"      # โมเดลที่จะเฝ้า ("Baby Cry"/"Siren"/"Alarm"/"Motion" ก็ได้)
TARGET_CLASS  = "cough"      # คลาสที่อยากดักจับ (ดู labels ในคอนโซลตอนรัน)
NEED_HITS     = 3            # ต้องจับคลาสเป้าหมายติดกันกี่เฟรมถึงจะยอมยิง (กันกระพริบ)
COOLDOWN_MS   = 3000         # หลังยิงแล้ว เว้นกี่ ms ก่อนยิงซ้ำได้ (refractory)

# ธีมสีเดียวกับหน้า Edge AI จริงบนบอร์ด
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
lcd.console(' ยิง action เมื่อเจอ "%s" ติดกัน %d เฟรม + มั่นใจเกิน %.0f%%'
            % (TARGET_CLASS, NEED_HITS, edge_ai.CONF_FLOOR * 100))

# ---- สร้าง widget ครั้งเดียวก่อนลูป ----
ui.Label("Edge AI - Action Pipeline", x=20, y=8, color=PURPLE)
ui.Panel(x=20, y=48, w=330, h=180, color=CARD)
verdict = ui.Seg7("---", x=40, y=72, color=GREEN)
conf = ui.Label("conf: -- %", x=40, y=160, color=CYAN)
streak_lab = ui.Label("streak: 0/%d" % NEED_HITS, x=40, y=186, color=SEC)

# "ไฟ RGB" บนจอ = การ์ดสีที่เปลี่ยนตามสถานะ pipeline (เทา=ว่าง ฟ้า=เฝ้า เหลือง=ใกล้ แดง=ยิง)
light = ui.Panel(x=380, y=48, w=120, h=120, color=LIGHT_OFF)
light_lab = ui.Label("IDLE", x=400, y=178, color=SEC)
hits_lab = ui.Label("alerts: 0", x=560, y=8, color=SEC)

# แถวคะแนนต่อคลาส สร้างครบตามจำนวนคลาสของโมเดลนี้
rows = []
for i in range(len(labels)):
    y = 60 + i * 40
    lb = ui.Label(labels[i], x=540, y=y, color=SEC)
    br = ui.Bar(x=540, y=y + 18, w=210, h=12, min=0, max=100, value=0, color=DIM)
    rows.append((lb, br))

back = ui.Button("< ออก", x=650, y=352, w=120, h=36)
back_id = back.id()

# สถานะของ pipeline (ตัวแปรที่ callback/ลูปใช้ร่วมกัน)
streak = 0            # จับคลาสเป้าหมายติดกันมากี่เฟรมแล้ว
alerts = 0            # ยิง action ไปแล้วกี่ครั้ง
last_fire = time.ticks_ms()  # เวลาที่ยิงครั้งล่าสุด (ใช้ทำ cooldown)


def set_light(color, text):
    """เปลี่ยนสีไฟ RGB บนจอ + ป้ายกำกับสถานะ (นี่คือ 'action' ช่องแรก)"""
    light.color(color)
    light_lab.text(text)


def fire_action(conf_val):
    """verdict -> action จริง: ไฟแดง + เสียงเตือน + บันทึก log + นับจำนวนครั้ง
    ในงานจริง ตรงนี้อาจเป็น เปิดรีเลย์ / ส่งแจ้งเตือน MQTT / เขียนไฟล์เหตุการณ์"""
    global alerts
    alerts += 1
    set_light(RED, "ALERT")
    hits_lab.text("alerts: %d" % alerts)
    if hasattr(ui, "tone"):
        ui.tone(76, ui.WAVE_SINE, 140, 160)   # โน้ต MIDI 76 = มีสูง (เสียงเตือน)
    lcd.console('<span class=error> ALERT #%d: %s (conf %.0f%%)</span>'
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

        # เติม: อ่านผลอนุมานล่าสุดมาเก็บใน r  ->  r = edge_ai.result()
        r = None
        pass
        if r and r['seq'] != last_seq:      # ทำงานเฉพาะตอนมีผลใหม่ (seq เปลี่ยน)
            last_seq = r['seq']
            verdict.text(r['label'] or '-')
            conf.text("conf: %.0f %%" % (r['conf'] * 100))
            top = r['top']
            for i, (lb, br) in enumerate(rows):
                if i < len(r['scores']):
                    br.value(int(r['scores'][i] * 100))
                    br.color(GREEN if i == top else DIM)

            # ---- ท่อของ action pipeline: กรอง -> debounce -> สั่งการ ----
            # เติม: ด่านกรอง false positive — นับว่า "เจอเป้าหมายจริง" ก็ต่อเมื่อ
            #       คลาสที่ชนะ == TARGET_CLASS และมั่นใจไม่ต่ำกว่า CONF_FLOOR
            #       hit = (r['label'] == TARGET_CLASS and r['conf'] >= edge_ai.CONF_FLOOR)
            hit = False
            pass

            if hit:
                streak += 1                 # เจอต่อเนื่อง เพิ่ม streak
                if streak < NEED_HITS:
                    set_light(AMBER, "%d/%d" % (streak, NEED_HITS))
            else:
                streak = 0                  # หลุดคลาสเป้าหมาย รีเซ็ต streak
                set_light(CYAN, "watching")
            streak_lab.text("streak: %d/%d" % (streak, NEED_HITS))

            now = time.ticks_ms()
            cooled = time.ticks_diff(now, last_fire) >= COOLDOWN_MS  # พ้น cooldown แล้วไหม
            ready = streak >= NEED_HITS                              # จับครบจำนวนเฟรมหรือยัง
            # เติม: เงื่อนไข debounce — ยิงได้ก็ต่อเมื่อจับครบต่อเนื่อง (ready) "และ"
            #       พ้นช่วงเว้นแล้ว (cooled)  ->  should_fire = ready and cooled
            should_fire = False
            pass
            if should_fire:
                # เติม: ยิง action จริง + บันทึกเวลาไว้ทำ cooldown + รีเซ็ต streak
                #       fire_action(r['conf']); last_fire = now; streak = 0
                pass

        time.sleep_ms(150)      # เว้นจังหวะ ไม่รัดจอจนกิน CPU เปล่า
except KeyboardInterrupt:
    pass
finally:
    edge_ai.stop()      # ออกจากงานยังไง ทิ้งเครื่องไว้ให้เรียบร้อยแบบนั้น
    lcd.console('<span class=ok> จบการทำงาน — ยิง action ทั้งหมด %d ครั้ง</span>' % alerts)

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
