# s18_under_the_hood_full.py - เครื่องส่องสแตก Edge AI ฉบับเต็ม (สำหรับ Researcher)
# วิธีรัน: เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev กด Program
#
# ฉบับเต็มนี้ต่อยอดจากไฟล์ฝึก 5 ช่อง (links / model / active / result / latency) แล้วเพิ่ม
# ของที่ช่วยให้ "แกะสแตกเห็นทั้งเส้น" ได้จริง:
#   - แผนที่สแตกสามชั้น (transport -> control -> result) พิมพ์เป็น log ตอนเปิด
#   - จับคู่ทุก key ของ result() กับฟิลด์ใน ai_result_t (ดูฟิลด์ใน ai_engine.h ของ SDK)
#   - แถบ scores ทุกคลาส + แยกสี "มั่นใจ/ยังไม่ชัวร์" ด้วย edge_ai.CONF_FLOOR
#   - on_result(cb) — ให้เฟิร์มแวร์เรียกกลับเมื่อคลาส "เปลี่ยน" และทวนคลาสเดิมราววินาทีละครั้ง
#   - latency สูงสุด (worst case) ที่ NPU เคยใช้ เทียบกับ latency ล่าสุด
#
# เป้าหมายของชุดบทเรียน: อธิบายสแตกได้ แล้วชี้ฟังก์ชันหรือฟิลด์ต้นทางของแต่ละชั้นใน header ของ SDK เป็น (MVP ของบทเรียน 7.1–7.2)

import edge_ai
import ui
ui.screen()
import lcd
import time

PURPLE = 0xBB86FC
GREEN  = 0x50D890
AMBER  = 0xF5C542   # ยังไม่ชัวร์ (conf < CONF_FLOOR)
DIM    = 0x6A3A31
CYAN   = 0x71C7EC
RED    = 0xE85B5B
CARD   = 0x2A1712
SEC    = 0xCFC6BF

SENSOR = ("IMU", "RADAR", "MIC")   # ตรงกับ ai_sensor_t: 0=IMU 1=RADAR 2=MIC

# แผนที่สแตก: แต่ละคำสั่งฝั่ง "อ่าน" ไปโผล่ที่ query sub-plane ไหน แล้วสุดทางที่ไฟล์ไหน
STACK_MAP = (
    ("links()",   "OP_QUERY", "IPC model link -> deepcraft_task.c"),
    ("count()",   "Q_COUNT",  "ai_engine_model_count() @ai_engine.c"),
    ("model(n)",  "Q_MODEL",  "ai_engine_model(i) -> ai_model_desc_t"),
    ("active()",  "Q_ACTIVE", "s_current @ai_engine.c (ไม่ใช่ s_active)"),
    ("result()",  "Q_RESULT", "ai_result_t s_res (publish lock-free)"),
    ("latency()", "Q_RESULT", "s_res.inference_us / 1000"),
)

lcd.clear()
lcd.console('<h2> Edge AI - เครื่องส่องสแตกใต้ฝากระโปรง</h2>')

# ---- ชั้นที่ 0: transport ----
links = edge_ai.links()
lcd.console(' [0 transport] links() = %s' % (links,))

# ---- ชั้นที่ 1: registry ----
n = edge_ai.count()
models = edge_ai.models()
names = [m['name'] for m in models]
lcd.console(' [1 registry] count()=%d models() <- s_models[] @ai_engine.c' % n)

# พิมพ์แผนที่สแตกครั้งเดียวตอนเปิด — ไว้เทียบกับ log สดตอน Trace
lcd.console(' --- แผนที่สแตก (API ฝั่งอ่าน -> query -> ปลายทาง C) ---')
for call, q, dst in STACK_MAP:
    lcd.console('   %-10s %-9s %s' % (call, q, dst))

ui.Label("Edge AI stack tracer", x=20, y=8, color=PURPLE)
dd = ui.Dropdown(text="\n".join(names), x=20, y=42, w=250)
btn_trace = ui.Button("Trace", x=285, y=42, w=88, h=36)
btn_stop = ui.Button("Stop", x=381, y=42, w=88, h=36)
status = ui.Label("IDLE", x=490, y=50, color=RED)

ui.Panel(x=20, y=92, w=320, h=150, color=CARD)
verdict = ui.Seg7("---", x=40, y=118, color=GREEN)
active_lb = ui.Label("active(): -1", x=40, y=196, color=SEC)
conf = ui.Label("conf: -- %", x=40, y=216, color=CYAN)
lat = ui.Label("lat: -- / max -- ms", x=160, y=216, color=CYAN)

# แถวคะแนนต่อคลาส (โมเดลหนึ่งมีได้ถึง 8 คลาส) สร้างไว้ก่อนแล้วค่อยโชว์/ซ่อน
rows = []
for i in range(8):
    y = 96 + i * 30
    lb = ui.Label("", x=360, y=y, color=SEC)
    br = ui.Bar(x=360, y=y + 16, w=400, h=10, min=0, max=100, value=0, color=DIM)
    lb.hide()
    br.hide()
    rows.append((lb, br))

back = ui.Button("< ออก", x=570, y=352, w=120, h=36)
back_id = back.id()
dd_id = dd.id()
trace_id = btn_trace.id()
stop_id = btn_stop.id()

lat_max = 0.0


def show_rows(mi):
    """โชว์แถบคลาสของโมเดลที่เลือก (widget สร้างไว้แล้ว แค่เปลี่ยนข้อความ + โชว์/ซ่อน)"""
    labels = models[mi]['labels']
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


def show_descriptor(mi):
    """ดึง descriptor ของโมเดลหนึ่งตัวมาเจาะ แล้ว log ว่าฟิลด์มาจากไหน"""
    desc = edge_ai.model(mi)
    lcd.console(' [1 registry] model(%d): name=%s sensor=%s labels=%s'
                % (mi, desc['name'], SENSOR[desc['sensor']], desc['labels']))


def on_change(r):
    """เฟิร์มแวร์เรียก callback นี้เมื่อ "คลาสเปลี่ยน" (และทวนคลาสเดิมราววินาทีละครั้ง) — รันในบริบท scheduler
    ปลอดภัยกับ print/lcd นี่คือแบบ event-driven ต่างจากการ pull เองในลูป"""
    lcd.console(' [cb] on_result: %s (%.0f%%) seq=%d'
                % (r['label'] or '-', r['conf'] * 100, r['seq']))


sel = 0
running = False
last_seq = -1
show_rows(sel)
show_descriptor(sel)
edge_ai.on_result(on_change)     # ลงทะเบียน callback ครั้งเดียว (ยกเลิกด้วย on_result(None))
lcd.console(' เลือกโมเดลแล้วกด Trace เพื่อไล่สแตก transport -> control -> result')

try:
    while True:
        for ev in ui.poll():
            h = ev.get('handle')
            t = ev.get('type')
            if h == back_id:
                raise KeyboardInterrupt
            elif h == dd_id and t == 'value_changed':
                sel = ev.get('value')
                verdict.text('---')
                conf.text("conf: -- %")
                show_rows(sel)
                show_descriptor(sel)
            elif h == trace_id:
                try:
                    edge_ai.select(sel)
                    lcd.console(' [2 control] select(%d) -> SELECT(0x%02X)'
                                ' confirmed by observation' % (sel, 0x90 + sel))
                    cur = edge_ai.active()
                    active_lb.text("active(): %d" % cur)
                    lcd.console(' [2 control] active() = %d <- s_current @ai_engine.c'
                                % cur)
                    running = True
                    last_seq = -1
                    lat_max = 0.0
                    status.text("RUNNING")
                    status.color(GREEN)
                except OSError as e:
                    status.text("ERROR")
                    status.color(RED)
                    lcd.console('<span class=error> select ไม่ยืนยัน: %s</span>' % e)
            elif h == stop_id:
                edge_ai.stop()
                running = False
                status.text("STOPPED")
                status.color(RED)
                active_lb.text("active(): -1")
                lcd.console(' [2 control] stop() -> DC_CMD_STOP · engine idle')

        if running:
            r = edge_ai.result()
            if r and r['seq'] != last_seq:
                last_seq = r['seq']
                sure = r['conf'] >= edge_ai.CONF_FLOOR    # เกิน 0.50 ถึงจะเชื่อ
                verdict.text(r['label'] or '-')
                verdict.color(GREEN if sure else AMBER)
                conf.text("conf: %.0f %%" % (r['conf'] * 100))
                ms = edge_ai.latency()
                if ms > lat_max:
                    lat_max = ms
                lat.text("lat: %.2f / max %.2f ms" % (ms, lat_max))
                top = r['top']
                for i, (lb, br) in enumerate(rows):
                    if i < len(r['scores']):
                        br.value(int(r['scores'][i] * 100))
                        br.color(GREEN if i == top else DIM)

        time.sleep_ms(150)
except KeyboardInterrupt:
    pass
finally:
    edge_ai.on_result(None)     # ถอน callback ก่อนออก
    edge_ai.stop()              # คืนเครื่องยนต์สู่ idle เสมอ
    lcd.console('<span class=ok> จบการแกะสแตก</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
