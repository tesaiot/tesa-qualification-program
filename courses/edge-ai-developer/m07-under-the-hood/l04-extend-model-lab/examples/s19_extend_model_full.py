# s19_extend_model_full.py - เพิ่มโมเดลของเราเองเข้า Edge AI (ฉบับเต็ม)
# วิธีรัน: เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator (ide.tesaiot.dev)
#          กด "Program to Device" (หรือ Run) — อ่าน "3 การแก้" ที่พิมพ์ออกมา เอาไปวางใน
#          เฟิร์มแวร์ build+flash แล้วกลับมากด Re-check แล้วกด Run mine
#
# ฉบับนี้คือเวอร์ชันขัดเรียบร้อยของ s19_extend_model.py — โครงเดียวกับที่คุณเติมในไฟล์ฝึก
# แต่เพิ่มของที่ทำให้ "งานต่อเติมโมเดล" ครบวงจรและอ่านง่ายขึ้น:
#   - ตรวจ "สัญญา 4 ฟังก์ชัน" (init/enqueue/dequeue/finalize) ก่อนขึ้น ROW ให้ครบ
#   - รองรับทั้ง AIM_* (โมเดล gen จาก DEEPCRAFT) และ IMAI_* (ready-model .a)
#   - โชว์ latency + ใช้เกณฑ์ CONF_FLOOR แยก "มั่นใจ / ยังไม่ชัวร์" ด้วยสี
#   - diff จำนวนโมเดลก่อน/หลัง เพื่อยืนยันว่า count() เพิ่มขึ้นจริง (เกณฑ์ใน ai_models/README.md ของ SDK)
# ทั้งหมดยังยืนบน "3 การแก้" เดิม + คำสั่งอ่านทะเบียนของ edge_ai เท่านั้น

import edge_ai
import ui
ui.screen()
import lcd
import time

# ธีมสีเดียวกับหน้า Edge AI จริงบนบอร์ด
PURPLE = 0xBB86FC   # หัวข้อ AI
GREEN  = 0x50D890   # เจอแล้ว / คลาสที่ชนะ (มั่นใจ)
AMBER  = 0xE0A03A   # verdict ที่ยังไม่ถึงเกณฑ์ความมั่นใจ (not sure)
DIM    = 0x6A3A31   # โมเดลอื่นในทะเบียน
CYAN   = 0x71C7EC   # latency / ค่าตัวเลข
RED    = 0xE85B5B   # ยังไม่เจอ / error
CARD   = 0x2A1712   # พื้นการ์ด
SEC    = 0xCFC6BF   # ข้อความรอง

SENSOR = ("IMU", "RADAR", "MIC")
SENSOR_C = ("AI_SENSOR_IMU", "AI_SENSOR_RADAR", "AI_SENSOR_MIC")

lcd.clear()
lcd.console('<h2> Edge AI - เพิ่มโมเดลของเราเอง (ฉบับเต็ม)</h2>')
lcd.console(' links: %s · CONF_FLOOR=%.2f' % (str(edge_ai.links()), edge_ai.CONF_FLOOR))

# สเปกของโมเดลที่เราจะเพิ่ม — Fall Detection ใช้ IMU (ยืม feed_imu เดิม ไม่ต้องเขียน feed ใหม่)
# ลองเปลี่ยน STYLE เป็น "IMAI" ถ้าโมเดลของคุณมาจาก ready-model .a แทน DEEPCRAFT source
NAME_UI = "Fall Detection"
PREFIX  = "FALL"
STYLE   = "AIM"        # "AIM" = โมเดล gen จาก DEEPCRAFT (source), "IMAI" = ready-model .a
SPEC = {
    "name":   NAME_UI,
    "sensor": edge_ai.SENSOR_IMU,
    "labels": ["normal", "fall"],
    "period_ms": 200,
    "flash_bytes": 40000,
}


def contract_fns(prefix, style):
    """คืนชื่อ 'สัญญา 4 ฟังก์ชัน' ของโมเดลตาม style — ทั้งสองแบบมีลายเซ็นเดียวกันเป๊ะ
    (int init(void) / int enqueue(const float*) / int dequeue(float*) / void finalize(void))
    ต่างแค่คำนำหน้า: AIM_<PREFIX>_ (source) หรือ IMAI_<PREFIX>_ (ready-model .a ที่ objcopy
    เปลี่ยนชื่อให้ไม่ชนกัน)"""
    base = "%s_%s_" % (style, prefix)
    return {k: base + k for k in ("init", "enqueue", "dequeue", "finalize")}


def make_row(spec, prefix, style):
    """แปลงสเปกเป็นข้อความ C ROW แบบเดียวกับใน ai_engine.c จริง (Edit 2)
    ready-model .a ไม่มี header จึงประกาศ extern แทน #include"""
    fn = contract_fns(prefix, style)
    labels_c = ", ".join('"%s"' % c for c in spec["labels"])
    lo = prefix.lower()
    if style == "AIM":
        head = '#  include "model_%s.h"' % lo
    else:
        head = ('extern int  %s(void);\n'
                'extern int  %s(const float *in);\n'
                'extern int  %s(float *out);\n'
                'extern void %s(void);'
                % (fn["init"], fn["enqueue"], fn["dequeue"], fn["finalize"]))
    return (
        '#if defined(EDGE_AI_MODEL_%s)\n'
        '%s\n'
        '#  define %s_ROW { .name = "%s", \\\n'
        '        .description = "add-a-model demo", \\\n'
        '        .sensor = %s, .class_count = %d, \\\n'
        '        .class_labels = { %s }, \\\n'
        '        .flash_bytes = %du, .period_ms = %du, \\\n'
        '        .init = %s, .enqueue = %s, \\\n'
        '        .dequeue = %s, .finalize = %s },\n'
        '#else\n'
        '#  define %s_ROW\n'
        '#endif'
        % (lo, head, prefix, spec["name"], SENSOR_C[spec["sensor"]],
           len(spec["labels"]), labels_c, spec["flash_bytes"], spec["period_ms"],
           fn["init"], fn["enqueue"], fn["dequeue"], fn["finalize"], prefix)
    )


def print_three_edits(spec, prefix, style):
    """พิมพ์ '3 การแก้' ครบตาม ai_models/README.md ของ SDK — ไม่ต้องแตะ MicroPython/IPC เลย"""
    lo = prefix.lower()
    lcd.console('<b> Edit 1 — proj_cm55/Makefile</b>')
    lcd.console('  AI_MODELS := motion audio radar cough alarm siren %s' % lo)
    lcd.console('<b> Edit 2 — ai_engine.c (ROW + ต่อเข้า s_models[])</b>')
    lcd.console('<pre>%s</pre>' % make_row(spec, prefix, style))
    lcd.console('  ...แล้วเติม %s_ROW ต่อท้าย s_models[] ด้วย' % prefix)
    lcd.console('<b> Edit 3 — วางไฟล์โมเดล</b>')
    if style == "AIM":
        lcd.console('  model_%s.c + model_%s.h (export %s_*)'
                    % (lo, lo, "AIM_" + prefix))
    else:
        lcd.console('  %s_lib_eval.a (objcopy prefix -> IMAI_%s_*)' % (lo, prefix))
    lcd.console('  แล้ว: rm -rf proj_cm55/build; make program EDGE_AI_MODEL=combo')


# หัวข้อ + การ์ดสถานะ (สร้างครั้งเดียว)
ui.Label("Edge AI · Add-a-model (full)", x=20, y=8, color=PURPLE)
ui.Panel(x=20, y=42, w=470, h=196, color=CARD)
found_lbl = ui.Seg7("---", x=40, y=64, color=RED)
detail = ui.Label("", x=40, y=150, color=SEC)
conf = ui.Label("conf: -- %", x=40, y=178, color=CYAN)
lat = ui.Label("latency: -- ms", x=40, y=206, color=CYAN)

# แถวรายชื่อโมเดลในทะเบียน (ของเราไฮไลต์เขียว)
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

# จำนวนโมเดล "ก่อน" เพิ่ม — ใช้ diff ยืนยันว่า count() เพิ่มขึ้นจริงหลัง build ใหม่
baseline = edge_ai.count()


def scan_registry():
    """ถามทะเบียนสด หา index โมเดลของเรา คืน (index_หรือ_-1, จำนวนทั้งหมด)"""
    n = edge_ai.count()
    models = edge_ai.models()
    mine = -1
    for i, m in enumerate(models):
        hit = (m['name'] == SPEC['name'])
        if hit:
            mine = i
        if i < len(rows):
            rows[i].text('%2d  %-16s %s'
                         % (m['index'], m['name'], SENSOR[m['sensor']]))
            rows[i].color(GREEN if hit else DIM)
            rows[i].show()
    for j in range(len(models), len(rows)):
        rows[j].hide()
    return mine, n


def report(mine, total):
    """อัปเดตการ์ดสถานะ + คอนโซล พร้อม diff จำนวนโมเดลเทียบ baseline"""
    if mine >= 0:
        found_lbl.text(SPEC['name'])
        found_lbl.color(GREEN)
        detail.text("เจอ index=%d · count %d -> %d (+%d)"
                    % (mine, baseline, total, total - baseline))
        detail.color(GREEN)
        lcd.console('<span class=ok> เจอ %s index=%d (count %d->%d)</span>'
                    % (SPEC['name'], mine, baseline, total))
    else:
        found_lbl.text("NOT YET")
        found_lbl.color(RED)
        detail.text("ยังไม่เจอ (count=%d) — ทำ 3 การแก้ แล้ว build+flash ใหม่" % total)
        detail.color(RED)
        lcd.console('<span class=error> ยังไม่พบ %s (count=%d)</span>'
                    % (SPEC['name'], total))


def run_mine(idx):
    """เลือกโมเดลของเราแล้วอ่าน verdict สดๆ — พิสูจน์ 'รันได้จริง' (MVP ของบทเรียน 7.3–7.4)"""
    try:
        edge_ai.select(idx)
        detail.text("running %s — ทำท่าตามคลาส (%s)"
                    % (SPEC['name'], "/".join(SPEC['labels'])))
        detail.color(GREEN)
        return True
    except OSError as e:
        detail.text("select ล้มเหลว: %s" % e)
        detail.color(RED)
        return False


# ครั้งแรก: พิมพ์ 3 การแก้ + สแกน
print_three_edits(SPEC, PREFIX, STYLE)
mine, total = scan_registry()
report(mine, total)

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
                report(mine, total)
            elif h == run_id:
                if mine >= 0:
                    if run_mine(mine):
                        running = True
                        last_seq = -1
                else:
                    detail.text("ยังไม่มีโมเดลให้รัน — build ให้โผล่ก่อน")
                    detail.color(RED)

        if running:
            r = edge_ai.result()
            if r and r['seq'] != last_seq:
                last_seq = r['seq']
                sure = r['conf'] >= edge_ai.CONF_FLOOR
                found_lbl.text(r['label'] or '-')
                found_lbl.color(GREEN if sure else AMBER)   # มั่นใจ=เขียว, ยังไม่ชัวร์=เหลือง
                conf.text("conf: %.0f %% (%s)"
                          % (r['conf'] * 100, "sure" if sure else "not sure"))
                lat.text("latency: %.1f ms" % r['latency_ms'])

        time.sleep_ms(180)
except KeyboardInterrupt:
    pass
finally:
    edge_ai.stop()
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
