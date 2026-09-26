# s19_extend_model.py - เพิ่มโมเดลของเราเองเข้า Edge AI
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) กด "Program to Device" (หรือ Run)
#          3) อ่าน "3 การแก้" ที่สคริปต์พิมพ์ออกมา เอาไปวางในเฟิร์มแวร์ แล้ว build+flash
#          4) กลับมากด Re-check — โมเดลของเราจะโผล่เขียวในทะเบียน แล้วกด Run mine
#
# เฉลยนี้ไม่ได้มีไว้ลอกวาง สิ่งที่นับคือการอธิบายด้วยคำพูดของคุณเอง อ่านให้เข้าใจ
# ว่า "การเพิ่มโมเดล" คือแค่ 3 การแก้ (Makefile / ROW / ไฟล์โมเดล) แล้วทั้งระบบปรับตามเอง
# เพราะ model-link เป็น shape-driven — ทะเบียนบอกรูปร่าง MicroPython กับ IPC ไม่ต้องแตะเลย
# ทั้งไฟล์นี้ยืนบนความจริงข้อเดียว: โมเดลที่ดีคือโมเดลที่ "โผล่ใน edge_ai.models() แล้วรันได้"

import edge_ai
import ui
ui.screen()
import lcd
import time

# ธีมสีเดียวกับหน้า Edge AI จริง (จะได้คุ้นตากับของจริง)
PURPLE = 0xBB86FC   # หัวข้อ AI
GREEN  = 0x50D890   # โมเดลของเรา "เจอแล้ว" / คลาสที่ชนะ
DIM    = 0x6A3A31   # โมเดลอื่นในทะเบียน
CYAN   = 0x71C7EC   # ความมั่นใจ / ค่าตัวเลข
RED    = 0xE85B5B   # "ยังไม่เจอ" / error
CARD   = 0x2A1712   # พื้นการ์ด
SEC    = 0xCFC6BF   # ข้อความรอง

SENSOR = ("IMU", "RADAR", "MIC")
# ชื่อ C ของค่าคงที่เซนเซอร์ — พิมพ์ลง ROW ให้อ่านออกเหมือนซอร์สจริงใน ai_engine.c
SENSOR_C = ("AI_SENSOR_IMU", "AI_SENSOR_RADAR", "AI_SENSOR_MIC")

lcd.clear()
lcd.console('<h2> Edge AI - เพิ่มโมเดลของเราเอง</h2>')

# สเปกของโมเดลที่เราจะเพิ่ม — เขียนที่ Python ก่อนให้เห็นภาพ แล้วค่อยแปลงเป็น C ROW
# เคล็ดสำคัญ: เลือกโมเดลที่ "ใช้เซนเซอร์เดิม" จะได้ไม่ต้องเขียน feed ใหม่ Fall Detection
# ใช้ IMU เหมือน Motion จึงยืม feed_imu เดิมได้เลย
NAME_UI = "Fall Detection"     # ชื่อที่จะโชว์ใน edge_ai.models() -> field .name
PREFIX  = "FALL"               # คำนำหน้าฟังก์ชันโมเดล -> AIM_FALL_init/enqueue/...
SPEC = {
    "name":   NAME_UI,
    "sensor": edge_ai.SENSOR_IMU,       # 0=IMU — ยืม feed_imu เดิม ไม่ต้องเขียน feed ใหม่
    "labels": ["normal", "fall"],       # 2 คลาส: ปกติ / ล้ม
    "period_ms": 200,
}


def make_row(spec, prefix):
    """แปลงสเปกเป็นข้อความ C ROW แบบเดียวกับที่อยู่ใน ai_engine.c จริง — นี่คือ 'โครง'
    ของ Edit 2 ที่เราจะเอาไปวาง แต่ละโมเดลต้องผูก 'สัญญา 4 ฟังก์ชัน' ให้ครบ:
        init (เตรียมโมเดล) / enqueue (ป้อน 1 ตัวอย่าง) / dequeue (ดึง verdict) / finalize
    โมเดลที่ gen จาก DEEPCRAFT ใช้คำนำหน้า AIM_<PREFIX>_ ส่วน ready-model .a ใช้ IMAI_<PREFIX>_
    ทั้งคู่มีลายเซ็นเดียวกันเป๊ะ จึงเสียบเข้า ROW ได้เหมือนกัน"""
    labels_c = ", ".join('"%s"' % c for c in spec["labels"])
    init_fn = "AIM_%s_init" % prefix
    enq_fn = "AIM_%s_enqueue" % prefix
    deq_fn = "AIM_%s_dequeue" % prefix
    fin_fn = "AIM_%s_finalize" % prefix
    return (
        '#if defined(EDGE_AI_MODEL_%s)\n'
        '#  include "model_%s.h"\n'
        '#  define %s_ROW { .name = "%s", \\\n'
        '        .description = "add-a-model demo", \\\n'
        '        .sensor = %s, .class_count = %d, \\\n'
        '        .class_labels = { %s }, \\\n'
        '        .flash_bytes = 40000u, .period_ms = %du, \\\n'
        '        .init = %s, .enqueue = %s, \\\n'
        '        .dequeue = %s, .finalize = %s },\n'
        '#else\n'
        '#  define %s_ROW\n'
        '#endif'
        % (prefix.lower(), prefix.lower(), prefix, spec["name"],
           SENSOR_C[spec["sensor"]], len(spec["labels"]), labels_c,
           spec["period_ms"], init_fn, enq_fn, deq_fn, fin_fn, prefix)
    )


def print_three_edits(spec, prefix):
    """พิมพ์ '3 การแก้' ที่ต้องเอาไปวางในเฟิร์มแวร์ (ai_models/README.md ของ SDK) — ครบเท่านี้จริงๆ
    ไม่ต้องแตะ MicroPython หรือ IPC เลย เพราะ registry เป็นคนบอกรูปร่างให้ทั้งสาย"""
    lo = prefix.lower()
    lcd.console('<b> Edit 1 — proj_cm55/Makefile</b>')
    lcd.console('  AI_MODELS := motion audio radar cough alarm siren %s' % lo)
    lcd.console('<b> Edit 2 — ai_engine.c (ROW + ต่อเข้า s_models[])</b>')
    lcd.console('<pre>%s</pre>' % make_row(spec, prefix))
    lcd.console('  ...แล้วเติม %s_ROW ต่อท้าย s_models[] ด้วย' % prefix)
    lcd.console('<b> Edit 3 — วางไฟล์โมเดล</b>')
    lcd.console('  model_%s.c + model_%s.h (export AIM_%s_*)' % (lo, lo, prefix))
    lcd.console('  แล้ว: rm -rf proj_cm55/build; make program EDGE_AI_MODEL=combo')


# หัวข้อ + การ์ดสถานะบนจอ (สร้างครั้งเดียว)
ui.Label("Edge AI · Add-a-model", x=20, y=8, color=PURPLE)
ui.Panel(x=20, y=42, w=470, h=196, color=CARD)
found_lbl = ui.Seg7("---", x=40, y=64, color=RED)
detail = ui.Label("", x=40, y=150, color=SEC)
conf = ui.Label("conf: -- %", x=40, y=182, color=CYAN)

# แถวรายชื่อโมเดลในทะเบียน (โมเดลของเราจะถูกไฮไลต์เขียว) — สร้างไว้ก่อน แค่โชว์/ซ่อน
rows = []
for i in range(10):
    y = 42 + i * 30
    lb = ui.Label("", x=520, y=y, color=SEC)
    lb.hide()
    rows.append(lb)

btn_check = ui.Button("Re-check", x=20, y=248, w=140, h=36)
btn_run = ui.Button("Run mine", x=170, y=248, w=140, h=36)
back = ui.Button("< ออก", x=570, y=352, w=120, h=36)
check_id = btn_check.id()
run_id = btn_run.id()
back_id = back.id()


def scan_registry():
    """ถามเฟิร์มแวร์ว่ามีโมเดลอะไรบ้าง แล้วหาว่าโมเดลของเราโผล่หรือยัง
    คืน (index_ของเรา_หรือ_-1, จำนวนโมเดลทั้งหมด) — ถามฮาร์ดแวร์ก่อนเสมอ อย่าเดา"""
    n = edge_ai.count()             # จำนวนโมเดลที่คอมไพล์รวมในเฟิร์มแวร์ตอนนี้
    models = edge_ai.models()       # ทะเบียนจริง — ค่าจาก CM55 ไม่ใช่ค่าที่เรา hard-code
    mine = -1
    for i, m in enumerate(models):
        hit = (m['name'] == SPEC['name'])
        if hit:
            mine = i                # เจอชื่อโมเดลของเราในทะเบียน — จำ index ไว้ไปสั่ง select
        if i < len(rows):
            rows[i].text('%2d  %-16s %s'
                         % (m['index'], m['name'], SENSOR[m['sensor']]))
            rows[i].color(GREEN if hit else DIM)   # ของเราเขียว ที่เหลือจาง
            rows[i].show()
    for j in range(len(models), len(rows)):
        rows[j].hide()
    return mine, n


def run_mine(idx):
    """เลือกโมเดลของเราแล้วอ่าน verdict สดๆ — พิสูจน์ว่า 'รันได้จริง' คือหัวใจ MVP ของบทเรียน 7.3–7.4"""
    try:
        edge_ai.select(idx)         # สั่ง CM55 สลับมารันโมเดลนี้ (confirm by observation)
        r = edge_ai.result()        # ผลอนุมานล่าสุด (อาจเป็น None ในรอบแรกๆ ก่อนหน้าต่างเต็ม)
        detail.text("running %s — ทำท่าตามคลาส" % SPEC['name'])
        detail.color(GREEN)
        return r
    except OSError as e:
        # ข้ามคอร์พลาดได้ ต้องเผื่อไว้เสมอ ไม่งั้นโปรแกรมตายทั้งตัว
        detail.text("select ล้มเหลว: %s" % e)
        detail.color(RED)
        return None


# ครั้งแรก: พิมพ์ 3 การแก้ให้ก็อปไปวาง + สแกนทะเบียนว่ามีโมเดลเราหรือยัง
print_three_edits(SPEC, PREFIX)
mine, total = scan_registry()
if mine >= 0:
    found_lbl.text(SPEC['name'])
    found_lbl.color(GREEN)
    detail.text("เจอในทะเบียน! index=%d (จาก %d โมเดล)" % (mine, total))
    detail.color(GREEN)
    lcd.console('<span class=ok> เจอ %s ใน edge_ai.models() index=%d</span>'
                % (SPEC['name'], mine))
else:
    found_lbl.text("NOT YET")
    found_lbl.color(RED)
    detail.text("ยังไม่เจอ — ทำ 3 การแก้แล้ว build+flash ใหม่ ค่อยกด Re-check")
    detail.color(RED)
    lcd.console('<span class=error> ยังไม่พบ %s (มี %d โมเดล) — build ใหม่ก่อน</span>'
                % (SPEC['name'], total))

running = False
last_seq = -1
try:
    while True:
        for ev in ui.poll():
            h = ev.get('handle')
            if h == back_id:
                raise KeyboardInterrupt
            elif h == check_id:
                # กดหลัง build+flash ใหม่ — ถ้า 3 การแก้ถูก โมเดลจะโผล่เขียวเดี๋ยวนั้น
                mine, total = scan_registry()
                if mine >= 0:
                    found_lbl.text(SPEC['name'])
                    found_lbl.color(GREEN)
                    detail.text("เจอแล้ว index=%d (จาก %d)" % (mine, total))
                    detail.color(GREEN)
                    lcd.console('<span class=ok> Re-check: เจอแล้ว index=%d</span>' % mine)
                else:
                    found_lbl.text("NOT YET")
                    found_lbl.color(RED)
                    detail.text("ยังไม่เจอ — เช็ก AI_MODELS + ROW + ต่อเข้า s_models[]")
                    detail.color(RED)
            elif h == run_id:
                if mine >= 0:
                    run_mine(mine)
                    running = True
                    last_seq = -1
                else:
                    detail.text("ยังไม่มีโมเดลให้รัน — build ให้โผล่ก่อน")
                    detail.color(RED)

        if running:
            r = edge_ai.result()
            if r and r['seq'] != last_seq:      # วาดเฉพาะตอนมี verdict ใหม่
                last_seq = r['seq']
                found_lbl.text(r['label'] or '-')
                conf.text("conf: %.0f %%" % (r['conf'] * 100))

        time.sleep_ms(180)
except KeyboardInterrupt:
    pass
finally:
    edge_ai.stop()      # ออกจากงานยังไง ทิ้งเครื่องไว้ให้เรียบร้อยแบบนั้น
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
