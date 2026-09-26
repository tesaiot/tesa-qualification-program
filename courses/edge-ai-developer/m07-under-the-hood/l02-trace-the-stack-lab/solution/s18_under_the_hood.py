# s18_under_the_hood.py - แกะสแตก Edge AI จากปลาย MicroPython ลงไปถึง NPU
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) กด "Program to Device"
#          3) เลือกโมเดลใน dropdown กด Trace แล้วอ่าน log แกะสแตกทีละชั้น
#          4) เทียบทุกบรรทัด log กับ ai_engine.h และ ipc_model_link_defs.h ใน SDK ว่าแต่ละค่ามาจากฟังก์ชันหรือฟิลด์ไหน
#
# เฉลยนี้ไม่ได้มีไว้ลอกวาง สิ่งที่นับคือการที่คุณ "ชี้ไฟล์:บรรทัด" ได้เอง
# อ่านให้เข้าใจ ปิดไฟล์ แล้วไล่สแตกด้วยปากตัวเอง: MicroPython (CM33_NS) เรียก edge_ai
# -> ข้าม IPC model link -> ai_engine (CM55) เลือกโมเดล -> feed เซนเซอร์ -> Ethos-U55 NPU
# -> publish ผลลง ai_result_t s_res -> เรา pull กลับมาเป็น dict ทั้งหมดยืนบนคำสั่งฝั่ง
# "อ่าน" แค่ห้าตัว: links / model / active / result / latency — ชุดบทเรียนนี้คือส่องไม่ใช่สร้าง

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
# ทุกคำสั่ง edge_ai วิ่งผ่าน "ช่องทาง" หนึ่งไปหา CM55 links() บอกว่าตอนนี้ต่ออยู่กับ
# backend อะไร ปกติได้ ('ipc',) นั่นคือ IPC model link ที่ปลายทาง CM55 อยู่ใน
# deepcraft_task.c — จำไว้ว่านี่คือ "สะพาน" เดียวที่ Python คุยกับ ai_engine ได้
links = edge_ai.links()
lcd.console(' [0 transport] links() = %s  -> IPC model link (deepcraft_task.c)'
            % (links,))

# ---- ชั้นที่ 1: registry (ทะเบียนโมเดลบน CM55) ----
# count()/models() เป็นการ pull ทะเบียน s_models[] จาก ai_engine.c ผ่าน query plane
# (Q_COUNT / Q_MODEL) ทะเบียนนี้ไม่ได้ hard-code ฝั่ง Python — มันถูกประกอบตอน build
# จาก ROW macros ที่ Makefile เลือกเข้ามา เพราะงั้นถ้าเฟิร์มแวร์เพิ่มโมเดล เราเห็นทันที
n = edge_ai.count()
models = edge_ai.models()
names = [m['name'] for m in models]
lcd.console(' [1 registry] count()=%d  models() <- s_models[] @ai_engine.c' % n)

# สร้าง widget ครั้งเดียวก่อนเข้าลูป — ถ้าสร้างซ้ำทุกวนรอบจะกินหน่วยความจำและจอกระพริบ
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

back = ui.Button("< ออก", x=570, y=352, w=120, h=36)
back_id = back.id()
dd_id = dd.id()
trace_id = btn_trace.id()
stop_id = btn_stop.id()


def show_descriptor(mi):
    """ดึง descriptor ของโมเดลหนึ่งตัว แล้ว log ให้เห็นว่าฟิลด์มาจากไหน"""
    # model(mi) ดึง descriptor ทีละตัว — ฝั่ง C คือ ai_engine_model(i) คืน
    # ai_model_desc_t (name/sensor/class_labels...) แล้วส่งกลับผ่าน Q_MODEL
    # เทียบกับ models() ที่ได้มาทั้งก้อน model(mi) เหมาะเวลาอยากดูตัวเดียวเจาะๆ
    desc = edge_ai.model(mi)
    lcd.console(' [1 registry] model(%d): name=%s sensor=%s labels=%s'
                % (mi, desc['name'], SENSOR[desc['sensor']], desc['labels']))


sel = 0            # โมเดลที่เลือกใน dropdown (เริ่มที่ index 0 = Motion Detection)
running = False
last_seq = -1      # กันวาดจอซ้ำ: log เฉพาะตอนมี verdict ใหม่ (seq เปลี่ยน)
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
                # เปลี่ยนโมเดลใน dropdown — ล้างผลเก่า แล้วส่อง descriptor ของตัวใหม่
                sel = ev.get('value')
                verdict.text('---')
                conf.text("conf: -- %")
                show_descriptor(sel)
            elif h == trace_id:
                try:
                    # ---- ชั้นที่ 2: control plane (สั่งข้ามคอร์) ----
                    # select() ส่ง SELECT(0x90+n) ผ่าน control plane แล้ว "รอยืนยัน"
                    # ด้วยการ poll Q_ACTIVE จนอ่านค่ากลับมาเท่ากับ n (สูงสุด 25×20 ms)
                    # นี่คือหลัก "confirmed by observation" ไม่เชื่อว่าสั่งแล้วสำเร็จ
                    edge_ai.select(sel)
                    lcd.console(' [2 control] select(%d) -> SELECT(0x%02X)'
                                ' confirmed by observation' % (sel, 0x90 + sel))
                    # active() อ่าน s_current (โมเดลที่ task "สลับไปแล้วจริง") ไม่ใช่ s_active
                    # (โมเดลที่แค่ "ขอ") — เอกสารเตือนว่า s_active นำ s_current อยู่หนึ่ง tick
                    cur = edge_ai.active()
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
            # result() pull verdict ล่าสุด ฝั่ง C คือ ai_result_t s_res ที่ publish()
            # เขียนแบบ lock-free (single-writer) เรายอมรับ "หนึ่งเฟรมเก่า" แลกกับความเร็ว
            r = edge_ai.result()
            if r and r['seq'] != last_seq:
                # seq เพิ่มทุกครั้งที่มี verdict ใหม่ — log เฉพาะตอนเปลี่ยนจริง
                last_seq = r['seq']
                verdict.text(r['label'] or '-')
                conf.text("conf: %.0f %%" % (r['conf'] * 100))
                # latency() อ่านเวลาอนุมานครั้งล่าสุด (ฝั่ง C คือ inference_us / 1000)
                # นี่คือเวลาที่ Ethos-U55 ใช้จริง มักไม่กี่มิลลิวินาที
                ms = edge_ai.latency()
                lat.text("latency: %.2f ms" % ms)
                lcd.console(' [3 result] seq=%d label=%s conf=%.2f  <- s_res.seq/scores'
                            % (r['seq'], r['label'], r['conf']))

        time.sleep_ms(180)      # เว้นจังหวะ ไม่รัดจอจนกิน CPU เปล่า
except KeyboardInterrupt:
    pass
finally:
    edge_ai.stop()      # ออกจากงานยังไง ทิ้งเครื่องไว้ให้เรียบร้อยแบบนั้น
    lcd.console('<span class=ok> จบการแกะสแตก</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
