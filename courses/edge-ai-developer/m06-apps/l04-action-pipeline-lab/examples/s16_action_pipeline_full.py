# s16_action_pipeline_full.py - action pipeline ครบวง: กรอง + smooth + debounce + action (ฉบับเต็ม)
# วิธีรัน: เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator (ide.tesaiot.dev)
#          กด "Program to Device" แล้วส่งเสียง/ทำท่าตามโมเดล (ตั้งต้นคือ Cough)
#
# ฉบับนี้คือเวอร์ชันขัดเรียบร้อยของ s16_action_pipeline.py — โครง "verdict -> action"
# เดียวกับที่คุณเติมในไฟล์ฝึก แต่ยกระดับเกราะกัน false positive ขึ้นอีกสองชั้น และ
# แยกช่องทางของ action ให้เห็นชัดว่ามี 3 ช่อง (RGB + เสียง + log):
#   1) smoothing ด้วย dsp.EMA — ปรับคะแนนคลาสเป้าหมายให้เนียน กันสัญญาณกระตุกชั่ววูบ
#   2) debounce สองชั้น — ต้องจับต่อเนื่องครบ NEED_HITS เฟรม "และ" คะแนนที่ smooth แล้ว
#      ต้องยังเกินเกณฑ์ จากนั้นเข้าช่วง cooldown กันยิงรัว
#   3) edge_ai.on_result(cb) — ต่อ callback ไว้ "log เมื่อคลาสเปลี่ยน" คู่ไปกับ
#      ลูปหลักที่ทำหน้าที่ตัดสินใจ action (สองกลไกนี้ทำงานพร้อมกันได้ ต่างคนต่างอ่านสถานะ)
# ทั้งหมดยังยืนบนคำสั่งหลักของ edge_ai: models / select / result / on_result / stop

import edge_ai
import ui
ui.screen()
import dsp
import lcd
import time

# ---- ปุ่มปรับพฤติกรรม pipeline (remix เพื่อจูน sensitivity แลกกับ false positive) ----
MODEL_KEYWORD = "Cough"      # โมเดลที่จะเฝ้า ("Baby Cry"/"Siren"/"Alarm"/"Motion" ก็ได้)
TARGET_CLASS  = "cough"      # คลาสที่อยากดักจับ (ดู labels ในคอนโซลตอนรัน)
NEED_HITS     = 3            # ต้องจับคลาสเป้าหมายติดกันกี่เฟรมถึงจะยอมยิง (debounce)
COOLDOWN_MS   = 3000         # หลังยิงแล้ว เว้นกี่ ms ก่อนยิงซ้ำได้ (refractory period)
EMA_ALPHA     = 0.35         # ความเนียนของ smoothing: ต่ำ=นิ่งช้า, สูง=ไวแต่กระตุก

PURPLE = 0xBB86FC
GREEN  = 0x50D890
DIM    = 0x6A3A31
CYAN   = 0x71C7EC
AMBER  = 0xE0A03A
RED    = 0xE85B5B
CARD   = 0x2A1712
SEC    = 0xCFC6BF
LIGHT_OFF = 0x444444

SENSOR = ("IMU", "RADAR", "MIC")

lcd.clear()
lcd.console('<h2> Edge AI - Action Pipeline (ฉบับเต็ม)</h2>')


def find_model(keyword):
    """หาโมเดลจากชื่อในทะเบียน — ไม่เจอใช้ตัวแรก (ถามฮาร์ดแวร์ ไม่ hard-code index)"""
    ms = edge_ai.models()
    for m in ms:
        if keyword.lower() in m['name'].lower():
            return m
    return ms[0]


model = find_model(MODEL_KEYWORD)
labels = model['labels']
# ตำแหน่งของคลาสเป้าหมายใน scores (เอาไว้ดึงคะแนนคลาสนั้นมา smooth) — ไม่เจอใช้ -1
target_idx = labels.index(TARGET_CLASS) if TARGET_CLASS in labels else -1
lcd.console(' โมเดล: %s (%s)  คลาส: %s'
            % (model['name'], SENSOR[model['sensor']], ", ".join(labels)))
lcd.console(' ยิงเมื่อ "%s" ติด %d เฟรม + smooth(conf) เกิน %.0f%% + พ้น cooldown %d ms'
            % (TARGET_CLASS, NEED_HITS, edge_ai.CONF_FLOOR * 100, COOLDOWN_MS))

# ---- สร้าง widget ครั้งเดียวก่อนลูป ----
ui.Label("Edge AI - Action Pipeline", x=20, y=8, color=PURPLE)
ui.Panel(x=20, y=48, w=330, h=190, color=CARD)
verdict = ui.Seg7("---", x=40, y=72, color=GREEN)
conf = ui.Label("conf: -- %", x=40, y=160, color=CYAN)
smooth_lab = ui.Label("smooth: -- %", x=40, y=184, color=CYAN)
streak_lab = ui.Label("streak: 0/%d" % NEED_HITS, x=40, y=208, color=SEC)

# "ไฟ RGB" บนจอ 4 สถานะ: เทา=ว่าง ฟ้า=เฝ้า เหลือง=เจอแต่ยังไม่ครบ แดง=ยิงแล้ว
light = ui.Panel(x=380, y=48, w=120, h=120, color=LIGHT_OFF)
light_lab = ui.Label("IDLE", x=400, y=178, color=SEC)
hits_lab = ui.Label("alerts: 0", x=560, y=8, color=SEC)
block_lab = ui.Label("blocked: 0", x=560, y=30, color=SEC)  # กี่ครั้งที่ pipeline กันไว้

# แถวคะแนนต่อคลาส
rows = []
for i in range(len(labels)):
    y = 60 + i * 40
    lb = ui.Label(labels[i], x=540, y=y + 40, color=SEC)
    br = ui.Bar(x=540, y=y + 58, w=210, h=12, min=0, max=100, value=0, color=DIM)
    rows.append((lb, br))

back = ui.Button("< ออก", x=570, y=352, w=120, h=36)
back_id = back.id()

# สถานะร่วมของ pipeline
smoother = dsp.EMA(alpha=EMA_ALPHA)   # smoothing คะแนนคลาสเป้าหมาย
state = {'streak': 0, 'alerts': 0, 'blocked': 0, 'last_fire': time.ticks_ms()}


def set_light(color, text):
    """action ช่องภาพ — ไฟ RGB บนจอ"""
    light.color(color)
    light_lab.text(text)


def fire_action(conf_val, smooth_val):
    """verdict -> action จริง 3 ช่อง: ไฟแดง + เสียงเตือน + บันทึก log พร้อม timestamp"""
    state['alerts'] += 1
    set_light(RED, "ALERT")
    hits_lab.text("alerts: %d" % state['alerts'])
    if hasattr(ui, "tone"):
        ui.tone(76, ui.WAVE_SINE, 140, 160)     # เสียงเตือน (โน้ต MIDI 76)
    elif hasattr(ui, "sfx"):
        ui.sfx(ui.SFX_UI_DENY)                  # เผื่อบางบอร์ดไม่มี tone
    t = time.ticks_ms()
    lcd.console('<span class=error> ALERT #%d @%dms: %s (conf %.0f%% · smooth %.0f%%)</span>'
                % (state['alerts'], t, TARGET_CLASS, conf_val * 100, smooth_val * 100))


def on_change(r):
    """edge_ai.on_result callback — เฟิร์มแวร์เรียกให้ตอนคลาสเปลี่ยน และทวนคลาสเดิมราววินาทีละครั้ง
    รันใน scheduler context ปลอดภัยกับ UI/print เราใช้ช่องนี้ทำ 'log การเปลี่ยนคลาส'
    ล้วนๆ ส่วนการตัดสินใจ action อยู่ที่ลูปหลัก (ที่นับ streak ต่อเฟรมได้)"""
    lb = r['label'] if isinstance(r['label'], str) else '?'
    if lb == state.get('cb_label'):     # รอบที่เฟิร์มแวร์ทวนคลาสเดิม: ไม่ต้อง log ซ้ำ
        return
    state['cb_label'] = lb
    lcd.console(' [on_result] คลาสเปลี่ยนเป็น: %s (conf %.0f%%)' % (lb, r['conf'] * 100))


# ---- ต่อ callback log แล้วสั่งเริ่มอนุมาน ----
edge_ai.on_result(on_change)        # ลงทะเบียนก่อน select เพื่อไม่พลาดการเปลี่ยนคลาสแรก
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

        r = edge_ai.result()
        if r and r['seq'] != last_seq:
            last_seq = r['seq']
            verdict.text(r['label'] or '-')
            conf.text("conf: %.0f %%" % (r['conf'] * 100))
            top = r['top']
            for i, (lb, br) in enumerate(rows):
                if i < len(r['scores']):
                    br.value(int(r['scores'][i] * 100))
                    br.color(GREEN if i == top else DIM)

            # ชั้นที่ 1 — smoothing: ป้อนคะแนนคลาสเป้าหมายเข้า EMA ให้เนียน
            raw_target = r['scores'][target_idx] if 0 <= target_idx < len(r['scores']) else 0.0
            sm = smoother.update(raw_target)
            smooth_lab.text("smooth: %.0f %%" % (sm * 100))

            # ชั้นที่ 2 — ด่านกรอง: เฟรมนี้เป็นการเจอเป้าหมายจริงไหม (คลาสตรง + conf เกินเกณฑ์)
            hit = (r['label'] == TARGET_CLASS and r['conf'] >= edge_ai.CONF_FLOOR)
            if hit:
                state['streak'] += 1
                if state['streak'] < NEED_HITS:
                    set_light(AMBER, "%d/%d" % (state['streak'], NEED_HITS))
            else:
                state['streak'] = 0
                set_light(CYAN, "watching")
            streak_lab.text("streak: %d/%d" % (state['streak'], NEED_HITS))

            # ชั้นที่ 3 — debounce + smoothing gate + cooldown
            now = time.ticks_ms()
            cooled = time.ticks_diff(now, state['last_fire']) >= COOLDOWN_MS
            ready = state['streak'] >= NEED_HITS
            smooth_ok = sm >= edge_ai.CONF_FLOOR       # คะแนนที่ smooth แล้วต้องยังหนักแน่น
            if ready and smooth_ok and cooled:
                fire_action(r['conf'], sm)
                state['last_fire'] = now
                state['streak'] = 0
            elif ready and not cooled:
                # จับได้จริงแต่ยังอยู่ในช่วง cooldown — นับว่า pipeline "กันการยิงซ้ำ" ไว้
                state['blocked'] += 1
                block_lab.text("blocked: %d" % state['blocked'])

        time.sleep_ms(150)
except KeyboardInterrupt:
    pass
finally:
    edge_ai.on_result(None)     # ถอน callback ก่อนออก (คู่กับตอนลงทะเบียน)
    edge_ai.stop()
    lcd.console('<span class=ok> จบ — ยิง %d ครั้ง · กันซ้ำ %d ครั้ง</span>'
                % (state['alerts'], state['blocked']))

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
