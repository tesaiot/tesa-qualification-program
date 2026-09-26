# 18_switch_cost.py - สลับโมเดลระหว่างที่โปรแกรมกำลังรัน
#
# Why : บอร์ดรันได้ทีละหนึ่งโมเดล งานจริงมักอยากได้มากกว่าหนึ่ง เช่นฟังเสียงไอ
#       ไปพร้อมกับดูการเคลื่อนไหว ทางออกที่ทุกคนคิดถึงคือสลับไปมาเร็ว ๆ
#       แต่การสลับมีราคาเป็นเวลาโหลด ที่ไม่มีใครเห็นจนกว่าจะจับเวลามันจริง ๆ
# What: เรียก select() ตัวใหม่คือการสลับ ไม่ต้อง stop() ก่อน โปรแกรมนี้จับเวลา
#       ทุกครั้งที่สลับ แล้วเอาราคานั้นขึ้นจอ ให้เห็นว่าสลับถี่แค่ไหนถึงจะไม่คุ้ม
#
# ดูที่จอ: ชื่อโมเดลที่กำลังรันตัวใหญ่ เวลาโหลดของรอบนี้เป็นตัวเลขและเป็นแถบ
#          แถบหน้าต่างฟังที่เดินจนเต็มก่อนสลับ และเวลาโหลดสะสมที่จ่ายไปทั้งหมด
# กับดัก : การสลับไม่ฟรี โปรแกรมที่สลับโมเดลทุกวินาที จะใช้เวลาเกือบทั้งหมด
#          ไปกับการโหลด แล้วเหลือเวลาฟังจริงน้อยกว่าที่คิดมาก

import edge_ai
import lcd
import time
import ui

WANT = ["motion", "cough"]    # สลับระหว่างสองตัวนี้
LISTEN_MS = 6000              # ฟังผลของแต่ละตัวนานแค่ไหนก่อนสลับ
LOAD_MAX = 2000               # เพดานของแถบเวลาโหลด เป็น ms

COL_TEXT, COL_DIM = 0xFFFFFF, 0xA0B4CC
COL_OK, COL_WARN, COL_INFO, COL_BAD = 0x00E676, 0xFFA726, 0x40C4FF, 0xFF5252

# แปลงคำค้นเป็นดัชนีจริงก่อนเข้าลูป จะได้ไม่ต้องค้นซ้ำทุกรอบ
plan = []
for key in WANT:
    for m in edge_ai.models():
        if key in m["name"].lower():
            plan.append((m["index"], m["name"]))

ui.screen()
time.sleep_ms(200)

ui.Label("สลับโมเดลไปมา และราคาของมัน", x=20, y=12, color=COL_TEXT, value=24)

ui.Label("กำลังรัน", x=40, y=64, color=COL_DIM, value=16)
now_lbl = ui.Label("ยังไม่ได้เริ่ม", x=40, y=88, color=COL_INFO, value=28)

ui.Label("เวลาโหลดรอบนี้", x=40, y=136, color=COL_DIM, value=16)
load_bar = ui.Bar(x=190, y=138, w=330, h=20, min=0, max=LOAD_MAX, value=0)
load_lbl = ui.Label("0 ms", x=540, y=134, color=COL_TEXT, value=20)

ui.Label("หน้าต่างฟัง", x=40, y=168, color=COL_DIM, value=16)
listen_bar = ui.Bar(x=190, y=170, w=330, h=20, min=0, max=100, value=0)
listen_lbl = ui.Label("0 / " + str(LISTEN_MS // 1000) + " s", x=540, y=166,
                      color=COL_TEXT, value=20)

ui.Label("ผลเด่นของรอบล่าสุด", x=20, y=216, color=COL_DIM, value=16)
best_lbl = ui.Label("ยังไม่มีอะไรเหนือเส้น", x=20, y=240, color=COL_DIM,
                    value=24)

ui.Label("จ่ายค่าสลับสะสม", x=20, y=286, color=COL_DIM, value=16)
total_seg = ui.Seg7(text="0", x=20, y=308, w=120, h=40, color=COL_WARN)
ui.Label("ms - เวลานี้ไม่ได้ใช้ฟังอะไรเลย", x=155, y=316, color=COL_DIM,
         value=20)

lcd.clear()
lcd.console("<h2>สลับโมเดลไปมา</h2>")

load_total = 0

for idx, name in plan:
    lcd.console("<span class=muted>---</span>")
    lcd.print("<span class=info>สลับไป", name, "</span>")

    now_lbl.text("กำลังโหลด " + name)
    now_lbl.color(COL_WARN)
    ui.poll()

    # จับเวลารอบ select() เพื่อให้เห็นด้วยตัวเลขว่าการสลับมีราคา
    t_start = time.ticks_ms()
    edge_ai.select(idx)
    load_ms = time.ticks_diff(time.ticks_ms(), t_start)

    load_total = load_total + load_ms
    load_bar.value(load_ms)
    load_lbl.text(str(load_ms) + " ms")
    total_seg.text(str(load_total))
    lcd.print("<span class=muted>โหลดเสร็จใน", load_ms, "ms</span>")

    # ยืนยันว่าได้ตัวที่ขอจริง ไม่ใช่เชื่อว่า select() สำเร็จเพราะไม่มี error
    if edge_ai.active() != idx:
        now_lbl.text("ได้ไม่ตรงที่ขอ: " + name)
        now_lbl.color(COL_BAD)
        lcd.print("<span class=error>ได้ไม่ตรงที่ขอ</span>")
        ui.poll()
        continue

    now_lbl.text(name)
    now_lbl.color(COL_OK)
    best_lbl.text("กำลังฟัง...")
    best_lbl.color(COL_DIM)
    listen_bar.value(0)

    last_seq = -1
    best = ""
    t0 = time.ticks_ms()

    while True:
        spent = time.ticks_diff(time.ticks_ms(), t0)
        if spent >= LISTEN_MS:
            break

        r = edge_ai.result()

        # เก็บเฉพาะผลที่ทั้งใหม่และเหนือเส้น เพื่อรายงานผลเด่นของรอบนี้ตัวเดียว
        # ถ้ารายงานทุกผล จอจะเต็มไปด้วย idle จนหาของสำคัญไม่เจอ
        if r is not None and r["seq"] != last_seq:
            last_seq = r["seq"]
            if r["conf"] >= edge_ai.CONF_FLOOR and r["top"] > 0:
                # str() ครอบไว้เพราะ label เป็น None ได้ ถ้าถามชื่อคลาสไม่สำเร็จ
                best = str(r["label"]) + "  " + str(int(r["conf"] * 100)) + "%"
                best_lbl.text(best)
                best_lbl.color(COL_OK)

        # แถบเดินตามเวลาที่ผ่านไป คนดูจึงรู้ว่ายังเหลืออีกนาน ไม่ใช่เดาว่าค้าง
        listen_bar.value(int(spent * 100 / LISTEN_MS))
        listen_lbl.text(str(spent // 1000) + " / " +
                        str(LISTEN_MS // 1000) + " s")

        ui.poll()
        time.sleep_ms(100)

    listen_bar.value(100)
    listen_lbl.text(str(LISTEN_MS // 1000) + " / " +
                    str(LISTEN_MS // 1000) + " s")

    if best == "":
        best_lbl.text("ไม่มีอะไรเหนือเส้นเลยในรอบของ " + name)
        best_lbl.color(COL_DIM)
        lcd.print("<span class=muted>ไม่มีอะไรเหนือเส้นเลย</span>")
    else:
        lcd.print("<span class=ok>เด่นสุด:", best, "</span>")

now_lbl.text("กำลังหยุดโมเดล")
now_lbl.color(COL_WARN)
ui.poll()
lcd.print("<span class=muted>กำลังหยุดโมเดล</span>")
edge_ai.stop()

now_lbl.text("จบรอบทดลอง")
now_lbl.color(COL_DIM)
lcd.print("<span class=ok>จบรอบทดลอง</span>")
ui.poll()

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux, Advance Innovation Centre (AIC), Burapha University
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
