# 17_latency_min_max_avg.py - วัดว่าโมเดลใช้เวลาคิดนานแค่ไหน
#
# ไฟล์นี้สอน: การอ่านตัวเลขครั้งเดียวไม่ใช่การวัด ต้องเห็นทั้งช่วง ต่ำสุด สูงสุด เฉลี่ย
# ดูที่จอ   : กราฟเส้นเดียวที่ไหลไปทางซ้าย แถบความคืบหน้าที่เต็มขึ้นเรื่อย ๆ
#             และตัวเลขใหญ่ที่กลายเป็นค่าเฉลี่ยตอนเก็บครบ
# กับดัก    : latency_ms ไม่ใช่ "ความเร็วที่คนรู้สึก" โมเดลเสียงต้องฟังครบ 500 ms
#             ก่อนถึงจะเริ่มคิด เวลาที่คนรอจริงจึงยาวกว่าตัวเลขนี้มาก

import edge_ai
import lcd
import time
import ui

TARGET = "motion"    # เปลี่ยนเป็น "cough" หรือ "siren" แล้วรันใหม่เพื่อเทียบ
SAMPLES = 20         # เก็บกี่รอบก่อนสรุป
CHART_MAX = 100      # แกนตั้งเป็นสัดส่วน 0-100 ของรอบที่ช้าที่สุดที่เจอ
TIMEOUT_MS = 30000   # เพดานเวลา เผื่อโมเดลไม่ยอมออกผลครบ SAMPLES รอบ

COL_TEXT, COL_DIM = 0xFFFFFF, 0xA0B4CC
COL_CARD = 0x142240
COL_OK, COL_WARN, COL_INFO = 0x00E676, 0xFFA726, 0x40C4FF

idx = -1
model_name = ""
for m in edge_ai.models():
    if TARGET in m["name"].lower():
        idx = m["index"]
        model_name = m["name"]

if idx < 0:
    raise ValueError("ไม่พบโมเดลชื่อ " + TARGET + " บนบอร์ดนี้")

ui.screen()
time.sleep_ms(200)

ui.Label("วัดเวลาคิดของ " + model_name, x=20, y=12, color=COL_TEXT, value=24)

# Chart เก็บได้ 50 จุดต่อเส้น จุดที่ 51 ดันจุดแรกออก กราฟจึงเลื่อนซ้ายเอง
# ช่วงแกนตั้งกำหนดตอนสร้างแล้วเปลี่ยนทีหลังไม่ได้ และเวลาคิดของแต่ละบอร์ดต่างกัน
# หลายเท่า จึงส่งค่าเป็นสัดส่วนของรอบที่ช้าที่สุด แทนที่จะตรึงแกนเป็น ms ตายตัว
chart = ui.Chart(x=20, y=52, w=650, h=170, min=0, max=CHART_MAX, color=COL_CARD)
series = chart.add_series(COL_INFO)
ui.Label("แกนตั้ง 100 = รอบที่ช้าที่สุด", x=20, y=228, color=COL_DIM, value=16)
ui.Label("กราฟเก็บ 50 จุดล่าสุด", x=340, y=228, color=COL_DIM, value=16)

ui.Label("เก็บได้แล้ว", x=20, y=256, color=COL_DIM, value=16)
bar = ui.Bar(x=130, y=258, w=250, h=20, min=0, max=SAMPLES, value=0)
count_lbl = ui.Label("0 / " + str(SAMPLES), x=396, y=254, color=COL_TEXT,
                     value=20)

seg = ui.Seg7(text="0", x=500, y=246, w=140, h=54, color=COL_OK)
ui.Label("ms", x=612, y=254, color=COL_DIM, value=16)

summary = ui.Label("กำลังโหลดโมเดล รอได้ถึง 15 วินาที", x=20, y=312,
                   color=COL_WARN, value=20)

lcd.clear()
lcd.console("<h2>วัดเวลาคิดของโมเดล</h2>")
lcd.print("วัด:", model_name)
ui.poll()

edge_ai.select(idx)
summary.text("กำลังเก็บค่า อย่าเพิ่งวางบอร์ดลง")
summary.color(COL_DIM)

# เก็บสรุปไว้ในตัวแปรไม่กี่ตัว ไม่เก็บทั้ง list เพราะ heap บนบอร์ดมีจำกัด
lo = 99999.0
hi = 0.0
total = 0.0
got = 0
last_seq = -1

# ลูปที่รอเงื่อนไขอย่างเดียวโดยไม่มีเพดานเวลา คือลูปที่ค้างได้ตลอดกาล
deadline = time.ticks_add(time.ticks_ms(), TIMEOUT_MS)

while got < SAMPLES and time.ticks_diff(deadline, time.ticks_ms()) > 0:
    r = edge_ai.result()

    if r is not None and r["seq"] != last_seq:
        last_seq = r["seq"]
        ms = r["latency_ms"]

        if ms < lo:
            lo = ms
        if ms > hi:
            hi = ms
        total = total + ms
        got = got + 1

        # ส่งเป็นสัดส่วนของค่าที่ช้าที่สุดเท่าที่เจอมา ถ้าส่ง int(ms) ตรง ๆ
        # บอร์ดที่คิดเร็วกว่า 1 ms จะได้กราฟแบนติดพื้นทั้งเส้น
        if hi > 0:
            chart.set_next(series, int(ms * 100 / hi))
        bar.value(got)
        count_lbl.text(str(got) + " / " + str(SAMPLES))

        # ใช้ "%.2f" ไม่ใช่ round() เพราะ round คืน float ที่พิมพ์ออกมา
        # เป็นทศนิยมสิบหกหลักได้ ส่วน "%.2f" ได้สองตำแหน่งเสมอ
        seg.text("%.2f" % ms)
        lcd.print("รอบ", got, "=", "%.2f" % ms, "ms")

    ui.poll()
    time.sleep_ms(50)

edge_ai.stop()

if got == 0:
    # ไม่ได้ผลเลยก็ต้องบอก ห้ามหารด้วยศูนย์แล้วปล่อยให้โปรแกรมพัง
    seg.text("--")
    seg.color(0xFF5252)
    summary.text("ไม่ได้ผลสักรอบ - โมเดลไม่ตัดสินใน 30 วินาที")
    lcd.print("<span class=error>ไม่ได้ผลเลยสักรอบ</span>")
else:
    avg = "%.2f" % (total / got)
    seg.text(avg)
    seg.color(COL_OK)

    # ช่วงกว้างบอกว่าเวลาคิดไม่คงที่ ซึ่งสำคัญกว่าค่าเฉลี่ยในงานที่ต้องตอบทัน
    summary.text("ต่ำสุด " + ("%.2f" % lo) + " - สูงสุด " + ("%.2f" % hi) +
                 " - เฉลี่ย " + avg + " ms - ช่วงกว้าง " +
                 ("%.2f" % (hi - lo)) + " ms")
    summary.color(COL_OK)
    lcd.print("ต่ำสุด", "%.2f" % lo, "ms | สูงสุด", "%.2f" % hi, "ms")
    lcd.print("<span class=ok>เฉลี่ย", avg, "ms</span>")
    lcd.print("<span class=muted>ช่วงกว้าง", "%.2f" % (hi - lo), "ms</span>")

ui.poll()

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux, Advance Innovation Centre (AIC), Burapha University
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
