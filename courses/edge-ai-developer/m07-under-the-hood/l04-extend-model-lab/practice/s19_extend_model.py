# s19_extend_model.py - เพิ่มโมเดลของเราเองเข้า Edge AI (ฉบับฝึกเติมโค้ด)
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) เติมช่องว่าง (pass / ...) ทั้ง 5 จุดตามคำใบ้ในคอมเมนต์ให้ครบ
#          3) กด "Program to Device" (หรือ Run) — สคริปต์จะทำสองอย่าง:
#             ก) พิมพ์ "3 การแก้" (Makefile + C ROW + ไฟล์โมเดล) ที่ต้องเอาไปวางในเฟิร์มแวร์
#             ข) ถามเฟิร์มแวร์ผ่าน edge_ai ว่าโมเดลของเรา "โผล่ในทะเบียนแล้วหรือยัง"
#
# ชุดบทเรียนนี้เราเป็น "นักวิจัย/นักต่อเติม" — ไม่ได้แค่เรียกโมเดลสำเร็จ แต่ลงไปเพิ่มโมเดล
# ตัวใหม่ให้เฟิร์มแวร์รู้จัก การเพิ่มโมเดลใช้ "3 การแก้" เท่านั้น (ดู ai_models/README.md ของ SDK):
#   Edit 1  proj_cm55/Makefile          -> เติมชื่อโมเดลใน AI_MODELS
#   Edit 2  ai_engine.c                 -> เพิ่ม <NAME>_ROW แล้วต่อเข้า s_models[]
#   Edit 3  วางไฟล์โมเดลลงในโฟลเดอร์      -> model_<name>.c/.h (AIM_*) หรือ .a (IMAI_*)
# แล้ว build+flash ใหม่ โมเดลจะโผล่ใน edge_ai.models() เอง โดยไม่ต้องแตะ MicroPython/IPC
# เพราะทั้ง model-link เป็นแบบ "shape-driven" (ทะเบียนบอกรูปร่าง เดี๋ยวสายที่เหลือปรับตาม)

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

lcd.clear()
lcd.console('<h2> Edge AI - เพิ่มโมเดลของเราเอง</h2>')

# ----- สเปกของโมเดลที่เราจะเพิ่ม (งานของคุณข้อ 1) -----
# นี่คือ "ใจความ" ของ C ROW ที่เราจะไปเขียนใน ai_engine.c เขียนที่ Python ก่อน
# ให้เห็นภาพ แล้วค่อยแปลงเป็น ROW ในเฟิร์มแวร์ เราเลือกโมเดลที่ "ใช้เซนเซอร์เดิม"
# จะได้ไม่ต้องเขียน feed ใหม่ — Fall Detection ใช้ IMU (feed_imu เดิม) เหมือน Motion
NAME_UI = "Fall Detection"     # ชื่อที่จะโชว์ใน edge_ai.models() -> field .name
PREFIX  = "FALL"               # คำนำหน้าฟังก์ชันโมเดล -> AIM_FALL_init/enqueue/...
SPEC = {
    "name":   NAME_UI,
    # เติม: ใส่เซนเซอร์ + คลาสของโมเดลนี้
    #   sensor ให้ใช้ค่าคงที่จากเฟิร์มแวร์ (0=IMU, 1=RADAR, 2=MIC) -> edge_ai.SENSOR_IMU
    #   labels เป็น list ของชื่อคลาส (Fall = ล้ม/ไม่ล้ม)
    "sensor": None,            # เติม: edge_ai.SENSOR_IMU
    "labels": [],             # เติม: ["normal", "fall"]
    "period_ms": 200,
}


def make_row(spec, prefix):
    """แปลงสเปกเป็นข้อความ C ROW แบบเดียวกับที่อยู่ใน ai_engine.c จริง
    (นี่คือ 'โครง' ของ Edit 2 — เราสร้างเป็น string ให้เห็นก่อนไปวางในเฟิร์มแวร์)"""
    labels_c = ", ".join('"%s"' % c for c in spec["labels"])
    # ----- ผูกฟังก์ชันโมเดลเข้ากับ ROW (งานของคุณข้อ 2) -----
    # โมเดลทุกตัวต้องมี "สัญญา 4 ฟังก์ชัน": init / enqueue / dequeue / finalize
    # โมเดลที่ gen จาก DEEPCRAFT ใช้คำนำหน้า AIM_<PREFIX>_  (เช่น AIM_FALL_init)
    # เติม: เติมชื่อฟังก์ชัน dequeue ให้ครบตามแบบ init/enqueue (ใช้ prefix ตัวใหญ่)
    init_fn = "AIM_%s_init" % prefix
    enq_fn = "AIM_%s_enqueue" % prefix
    deq_fn = None             # เติม: "AIM_%s_dequeue" % prefix
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


# ชื่อ C ของค่าคงที่เซนเซอร์ (เอาไว้พิมพ์ลง ROW ให้อ่านออกเหมือนในซอร์สจริง)
SENSOR_C = ("AI_SENSOR_IMU", "AI_SENSOR_RADAR", "AI_SENSOR_MIC")


def print_three_edits(spec, prefix):
    """พิมพ์ '3 การแก้' ที่ต้องเอาไปวางในเฟิร์มแวร์ (ai_models/README.md ของ SDK)"""
    lo = prefix.lower()
    lcd.console('<b> Edit 1 — proj_cm55/Makefile</b>')
    lcd.console('  AI_MODELS := motion audio radar cough alarm siren %s' % lo)
    lcd.console('<b> Edit 2 — ai_engine.c (ROW + ต่อเข้า s_models[])</b>')
    lcd.console('<pre>%s</pre>' % make_row(spec, prefix))
    lcd.console('  ...แล้วเติม %s_ROW ต่อท้าย s_models[] ด้วย' % prefix)
    lcd.console('<b> Edit 3 — วางไฟล์โมเดล</b>')
    lcd.console('  model_%s.c + model_%s.h (export AIM_%s_*)' % (lo, lo, prefix))
    lcd.console('  แล้ว: rm -rf proj_cm55/build; make program EDGE_AI_MODEL=combo')


# หัวข้อบนจอ
ui.Label("Edge AI · Add-a-model", x=20, y=8, color=PURPLE)
ui.Panel(x=20, y=42, w=470, h=196, color=CARD)
found_lbl = ui.Seg7("---", x=40, y=64, color=RED)
detail = ui.Label("", x=40, y=150, color=SEC)
conf = ui.Label("conf: -- %", x=40, y=182, color=CYAN)

# แถวรายชื่อโมเดลในทะเบียน (โมเดลของเราจะถูกไฮไลต์เขียว)
rows = []
for i in range(10):
    y = 42 + i * 30
    lb = ui.Label("", x=520, y=y, color=SEC)
    lb.hide()
    rows.append(lb)

btn_check = ui.Button("Re-check", x=20, y=248, w=140, h=36)
btn_run = ui.Button("Run mine", x=170, y=248, w=140, h=36)
back = ui.Button("< ออก", x=650, y=352, w=120, h=36)
check_id = btn_check.id()
run_id = btn_run.id()
back_id = back.id()


def scan_registry():
    """ถามเฟิร์มแวร์ว่ามีโมเดลอะไรบ้าง แล้วหาว่าโมเดลของเราโผล่หรือยัง
    คืน (index_ของเรา_หรือ_-1, จำนวนโมเดลทั้งหมด)"""
    # ----- อ่านทะเบียนสด (งานของคุณข้อ 3) -----
    # edge_ai.count() คืนจำนวนโมเดลที่คอมไพล์รวมในเฟิร์มแวร์ตอนนี้
    # เติม: อ่านจำนวนโมเดลปัจจุบันมาเก็บใน n  ->  n = edge_ai.count()
    n = 0
    pass
    models = edge_ai.models()
    mine = -1
    for i, m in enumerate(models):
        hit = (m['name'] == SPEC['name'])
        # ----- หา index ของโมเดลเรา (งานของคุณข้อ 4) -----
        # ถ้าชื่อในทะเบียนตรงกับ SPEC['name'] ให้จำ index ตัวนั้นไว้ใน mine
        # เติม: ถ้า hit เป็นจริง ให้ mine = i
        pass
        if i < len(rows):
            rows[i].text('%2d  %-16s %s'
                         % (m['index'], m['name'], SENSOR[m['sensor']]))
            rows[i].color(GREEN if hit else DIM)
            rows[i].show()
    for j in range(len(models), len(rows)):
        rows[j].hide()
    return mine, n


def run_mine(idx):
    """เลือกโมเดลของเราแล้วอ่าน verdict สดๆ — พิสูจน์ว่ามัน 'รันได้จริง' (MVP ของบทเรียน 7.3–7.4)"""
    try:
        # ----- สั่งรันโมเดลของเรา + อ่านผล (งานของคุณข้อ 5) -----
        # edge_ai.select(idx) สั่ง CM55 สลับมารันโมเดล index นี้ (รอยืนยัน, โยน OSError ได้)
        # edge_ai.result() คืน dict ผลอนุมานล่าสุด (label/conf/scores/seq) หรือ None
        # เติม: สั่ง select(idx) แล้วอ่านผลมาเก็บใน r
        r = None
        pass
        detail.text("running %s — ทำท่าตามคลาส" % SPEC['name'])
        detail.color(GREEN)
        return r
    except OSError as e:
        detail.text("select ล้มเหลว: %s" % e)
        detail.color(RED)
        return None


# ครั้งแรก: พิมพ์ 3 การแก้ + สแกนทะเบียน
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
    lcd.console('<span class=error> ยังไม่พบ %s (มี %d โมเดล) — ต้อง build ใหม่</span>'
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
                mine, total = scan_registry()
                if mine >= 0:
                    found_lbl.text(SPEC['name'])
                    found_lbl.color(GREEN)
                    detail.text("เจอแล้ว index=%d (จาก %d)" % (mine, total))
                    detail.color(GREEN)
                else:
                    found_lbl.text("NOT YET")
                    found_lbl.color(RED)
            elif h == run_id:
                if mine >= 0:
                    run_mine(mine)
                    running = True
                    last_seq = -1

        if running:
            r = edge_ai.result()
            if r and r['seq'] != last_seq:
                last_seq = r['seq']
                found_lbl.text(r['label'] or '-')
                conf.text("conf: %.0f %%" % (r['conf'] * 100))

        time.sleep_ms(180)
except KeyboardInterrupt:
    pass
finally:
    edge_ai.stop()      # ออกยังไงก็คืนเครื่องยนต์สู่ idle เสมอ
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
