# s18_under_the_hood.py - แกะสแตก Edge AI จากปลาย MicroPython ลงไปถึง NPU (ฉบับฝึกเติมโค้ด)
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) เติมช่องว่าง (pass) ทั้ง 5 จุดตามคำใบ้ในคอมเมนต์ให้ครบ
#          3) กด "Program to Device" แล้วเลือกโมเดล กด Trace
#          4) อ่าน "log แกะสแตก" ที่ไล่ตั้งแต่ transport -> registry -> select -> result
#
# ชุดบทเรียนนี้ต่างจากชุดบทเรียนก่อน ๆ ตรงที่เราไม่ได้จะ "สร้างแอปใหม่" แต่จะ "แกะของเดิม" ให้เห็น
# ทั้งเส้นทาง คุณเรียก edge_ai มาตลอดคอร์สแล้ว ชุดบทเรียนนี้เราจะเปิดฝากระโปรงดูว่า
# ทุกครั้งที่เรียก edge_ai.result() มันวิ่งผ่านอะไรบ้าง: จาก MicroPython บน CM33_NS
# ข้าม IPC "model link" ไปหา ai_engine บน CM55 ที่คุมโมเดลจริงแล้วรัน Ethos-U55 NPU
#
# สคริปต์นี้ไม่ได้อนุมานอะไรใหม่ มันเป็น "เครื่องมือส่องสแตก" — เรียก API ฝั่งอ่าน
# (links / model / active / result / latency) แล้วจับคู่ผลแต่ละอันกับไฟล์:บรรทัด
# ในเฟิร์มแวร์ อ้างอิงจาก ai_engine.h และ ipc_model_link_defs.h ใน SDK สาธารณะ

import edge_ai
import ui
ui.screen()
import lcd
import time

# ธีมสีเดียวกับหน้า Edge AI จริงบนบอร์ด (จะได้คุ้นตากับของจริง)
PURPLE = 0xBB86FC   # ชื่อ/หัวข้อ AI
GREEN  = 0x50D890   # ค่าที่ pull สำเร็จ + สถานะ RUNNING
DIM    = 0x6A3A31   # ค่าที่ยังว่าง
CYAN   = 0x71C7EC   # ตัวเลข/latency
RED    = 0xE85B5B   # STOPPED / error
CARD   = 0x2A1712   # พื้นการ์ด
SEC    = 0xCFC6BF   # ข้อความรอง

SENSOR = ("IMU", "RADAR", "MIC")   # ตรงกับ ai_sensor_t: 0=IMU 1=RADAR 2=MIC

lcd.clear()
lcd.console('<h2> Edge AI - แกะสแตกใต้ฝากระโปรง</h2>')

# ---- ชั้นที่ 0: transport (ช่องทางคุยข้ามคอร์) ----
# ทุกคำสั่ง edge_ai วิ่งผ่าน "ช่องทาง" หนึ่งไปหา CM55 ถามดูว่าตอนนี้ใช้ช่องไหน
# เติม 1: อ่านว่ามี link backend อะไรบ้าง  ->  links = edge_ai.links()
#         (คืน tuple เช่น ('ipc',) — ก็คือ IPC model link ใน deepcraft_task.c)
links = None
pass
lcd.console(' [0 transport] links() = %s  -> IPC model link (deepcraft_task.c)'
            % (links,))

# ---- ชั้นที่ 1: registry (ทะเบียนโมเดลบน CM55) ----
# count()/models() เป็นการ pull ทะเบียน s_models[] จาก ai_engine.c ผ่าน query plane
# (Q_COUNT / Q_MODEL) ค่านี้ถูกกำหนดตอน build ตามที่ Makefile เลือกโมเดลเข้ามา
n = edge_ai.count()
models = edge_ai.models()
names = [m['name'] for m in models]
lcd.console(' [1 registry] count()=%d  models() <- s_models[] @ai_engine.c' % n)

# สร้าง widget ครั้งเดียวก่อนเข้าลูป (สร้างซ้ำในลูปจะกินหน่วยความจำและจอกระพริบ)
ui.Label("Edge AI stack tracer", x=20, y=8, color=PURPLE)
dd = ui.Dropdown(text="\n".join(names), x=20, y=42, w=250)
btn_trace = ui.Button("Trace", x=285, y=42, w=88, h=36)
btn_stop = ui.Button("Stop", x=381, y=42, w=88, h=36)
status = ui.Label("IDLE", x=490, y=50, color=RED)

ui.Panel(x=20, y=92, w=320, h=150, color=CARD)
verdict = ui.Seg7("---", x=40, y=118, color=GREEN)
active_lb = ui.Label("active(): -1", x=40, y=196, color=SEC)
conf = ui.Label("conf: -- %", x=40, y=216, color=CYAN)
lat = ui.Label("latency: -- ms", x=190, y=216, color=CYAN)

back = ui.Button("< ออก", x=650, y=352, w=120, h=36)
back_id = back.id()
dd_id = dd.id()
trace_id = btn_trace.id()
stop_id = btn_stop.id()


def show_descriptor(mi):
    """ดึง descriptor ของโมเดลหนึ่งตัว แล้ว log ให้เห็นว่าฟิลด์มาจากไหน"""
    # เติม 2: pull descriptor ของโมเดล index mi ทีละตัว  ->  desc = edge_ai.model(mi)
    #         (map ไป Q_MODEL -> ai_engine_model(i) คืน ai_model_desc_t บน CM55)
    desc = None
    pass
    lcd.console(' [1 registry] model(%d): name=%s sensor=%s labels=%s'
                % (mi, desc['name'], SENSOR[desc['sensor']], desc['labels']))


sel = 0            # โมเดลที่เลือกใน dropdown (เริ่มที่ index 0 = Motion Detection)
running = False
last_seq = -1
show_descriptor(sel)
lcd.console(' เลือกโมเดลแล้วกด Trace เพื่อไล่สแตก select -> active -> result')

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
                show_descriptor(sel)
            elif h == trace_id:
                try:
                    # ---- ชั้นที่ 2: control plane (สั่งข้ามคอร์) ----
                    # select() ส่ง SELECT(0x90+n) ผ่าน control plane แล้ว "รอยืนยัน"
                    # ด้วยการ poll Q_ACTIVE จนอ่านค่ากลับมาเท่ากับ n (บรรทัดนี้ให้ไว้แล้ว)
                    edge_ai.select(sel)
                    lcd.console(' [2 control] select(%d) -> SELECT(0x%02X)'
                                ' confirmed by observation' % (sel, 0x90 + sel))
                    # เติม 3: อ่านว่า engine "สลับ" ไปโมเดลไหนแล้ว -> cur = edge_ai.active()
                    #         (map ไป Q_ACTIVE -> s_current ใน ai_engine.c ไม่ใช่ s_active)
                    cur = -1
                    pass
                    active_lb.text("active(): %d" % cur)
                    lcd.console(' [2 control] active() = %d  <- s_current @ai_engine.c'
                                % cur)
                    running = True
                    last_seq = -1
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
            # ---- ชั้นที่ 3: result plane (อ่านผลกลับ) ----
            # เติม 4: pull verdict ล่าสุด  ->  r = edge_ai.result()
            #         (map ไป Q_RESULT -> ai_result_t s_res ที่ publish() แบบ lock-free)
            r = None
            pass
            if r and r['seq'] != last_seq:
                last_seq = r['seq']
                verdict.text(r['label'] or '-')
                conf.text("conf: %.0f %%" % (r['conf'] * 100))
                # เติม 5: อ่านเวลาอนุมานครั้งล่าสุด (มิลลิวินาที) -> ms = edge_ai.latency()
                #         (map ไป inference_us ใน ai_result_t — เวลาที่ NPU ใช้จริง)
                ms = 0.0
                pass
                lat.text("latency: %.2f ms" % ms)
                lcd.console(' [3 result] seq=%d label=%s conf=%.2f  <- s_res.seq/scores'
                            % (r['seq'], r['label'], r['conf']))

        time.sleep_ms(180)
except KeyboardInterrupt:
    pass
finally:
    edge_ai.stop()      # ปิดเครื่องยนต์ให้เรียบร้อยเสมอ ไม่ปล่อยค้างรัน
    lcd.console('<span class=ok> จบการแกะสแตก</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
