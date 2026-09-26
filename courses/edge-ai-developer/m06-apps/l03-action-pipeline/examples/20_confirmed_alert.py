# 20_confirmed_alert.py - ให้โมเดลเป็นแหล่งค่า แล้วยืนยันก่อนเตือน
#
# Why : โมเดลตอบทุกร้อยมิลลิวินาที และมันสะดุดคำว่า shaking ได้ตอนที่ใครสักคน
#       เดินผ่านโต๊ะ ถ้าเอาคำตอบดิบไปยิงเตือนตรง ๆ ทีมจะได้ข้อความสามสิบใบในหนึ่งนาที
#       แล้วจะปิดการแจ้งเตือนทิ้ง ซึ่งแปลว่าใบที่จริงก็จะไม่มีใครเห็น
# What: รวมสามชิ้นที่แอปเตือนจริงต้องมีเข้าด้วยกัน แหล่งค่าคือคำตัดสิน
#       ของโมเดล การยืนยัน N รอบก่อนเชื่อ และช่วงเว้นก่อนเตือนซ้ำ
#       โมเดลตัวที่ 0 คือ Motion Detection มีสามคลาส idle / circle / shaking
#
# ดูที่จอ: ป้ายซ้ายคือคลาสที่โมเดลเพิ่งตอบ Seg7 ถัดมาคือความมั่นใจเป็นเปอร์เซ็นต์
#          ป้ายขวาคือสถานะที่ยืนยันแล้ว ซึ่งเปลี่ยนช้ากว่าป้ายซ้ายเสมอ
#          แถบล่างของการ์ดคือ streak ที่กำลังสะสมเทียบกับ CONFIRM_N
#          กราฟล่างคือความมั่นใจตามเวลา มีเส้นส้มคือ CONF_MIN ตัดขวางไว้
#          เขย่าบอร์ดค้างไว้ จะเห็นเส้นไต่ข้ามเส้นส้ม แล้ว streak จึงเริ่มเดิน
# กับดัก : result() คืน None ได้ตอนที่ยังไม่เคยมีคำตัดสินออกมา และเมื่อมีแล้ว
#          มันคืนใบเดิมซ้ำได้ด้วย ต้องดูคีย์ seq จึงจะรู้ว่าเป็นใบใหม่จริง

import edge_ai
import lcd
import time
import ui

MODEL_INDEX = 0          # 0 = Motion Detection
ALERT_CLASS = "shaking"  # คลาสที่ถือว่าเป็นเรื่อง
CONF_MIN = 0.70          # ต่ำกว่านี้ถือว่าโมเดลยังไม่มั่นใจพอ ไม่นับ
CONFIRM_N = 4
ALERT_GAP_MS = 8000
LOOP_MS = 200

COL_TEXT, COL_DIM = 0xFFFFFF, 0xA0B4CC
COL_CARD = 0x142240
COL_OK, COL_WARN, COL_BAD, COL_INFO = 0x00E676, 0xFFA726, 0xFF5252, 0x40C4FF

STATE_COLOR = {"OK": COL_OK, "ALERT": COL_BAD}

lcd.clear()
lcd.console("<h2>เฉพาะสถานะที่ยืนยันแล้ว</h2>")

# ถามชื่อคลาสจากตัวโมเดลเอง อย่าเดาจากความจำ
desc = edge_ai.model(MODEL_INDEX)
labels = desc["labels"]
lcd.print("<span class=muted>โมเดล {} - {}</span>".format(
    desc["name"], ", ".join(labels)))
# บอกกฎของลิ้นชักไว้ตั้งแต่ต้น ลิ้นชักที่ว่างจึงแปลว่า "ยังไม่มีอะไรยืนยันได้"
# ไม่ใช่ "โปรแกรมไม่ทำงาน" - ค่าที่วิ่งอยู่ตลอดเวลาไปอยู่บนหน้า Playground แทน
# สั้นไว้ก่อน lcd.print ตัดทิ้งที่ 127 ไบต์ และไทยกินตัวละ 3 ไบต์
lcd.print("<span class=muted>บันทึกเฉพาะตอนสถานะยืนยันเปลี่ยน</span>")

# พื้นที่วาดจริง 792x398 - เลี่ยงมุมขวาล่าง x>690 y>340 ที่ปุ่ม Console ทับอยู่
ui.screen()
time.sleep_ms(200)

ui.Label(desc["name"], x=20, y=10, color=COL_TEXT, value=24)

ui.Label("โมเดลตอบว่า", x=38, y=54, color=COL_DIM, value=16)
l_class = ui.Label("-", x=38, y=76, color=COL_DIM, value=28)

ui.Label("มั่นใจ %", x=250, y=54, color=COL_DIM, value=16)
seg_conf = ui.Seg7("0", x=250, y=78, w=90, h=40, color=COL_INFO)

ui.Label("ยืนยันแล้ว", x=380, y=54, color=COL_DIM, value=16)
l_state = ui.Label("OK", x=380, y=76, color=COL_OK, value=28)

ui.Label("เตือนไปแล้ว", x=530, y=54, color=COL_DIM, value=16)
seg_alert = ui.Seg7("0", x=530, y=78, w=90, h=40, color=COL_OK)

ui.Label("ยืนยันติดกัน / {} รอบ".format(CONFIRM_N), x=38, y=138,
         color=COL_DIM, value=14)
bar_streak = ui.Bar(x=230, y=140, w=420, h=18, min=0, max=CONFIRM_N, value=0,
                    color=COL_DIM)

# กราฟความมั่นใจ 0-100 พร้อมเส้น CONF_MIN วางทับไว้
# เส้นเกณฑ์ไม่ใช่ข้อมูลจากโมเดล มันคือการตัดสินใจของทีมที่เอามาวางทับข้อมูล
ch = ui.Chart(x=20, y=184, w=650, h=138, color=COL_CARD, min=0, max=100)
s_conf = ch.add_series(COL_INFO)
s_min = ch.add_series(COL_WARN)

# โจทย์ยืนพื้นเป็นป้ายของตัวเอง เพราะ l_foot เปลี่ยนตามสถานะทุกรอบ
# และแยกเป็นสองใบ เพราะ ui.Label ตัดที่ 95 ไบต์ ไทยหนึ่งตัวกิน 3 ไบต์
ui.Label("เขย่าบอร์ดค้างไว้", x=20, y=334, color=COL_DIM, value=16)
ui.Label("แล้วดูแท่งยืนยันไต่ขึ้น", x=200, y=334, color=COL_DIM, value=16)
l_foot = ui.Label("", x=20, y=358, color=COL_DIM, value=16)
ui.poll()

edge_ai.select(MODEL_INDEX)
edge_ai.start()

state, pending, streak = "OK", "OK", 0
last_alert, alerts, last_seq = None, 0, -1

while True:
    r = edge_ai.result()

    # ข้ามรอบเมื่อยังไม่มีคำตัดสิน หรือเมื่อได้ใบเดิมซ้ำ
    # ถ้านับ streak จากใบเดิมซ้ำ ๆ เกณฑ์ CONFIRM_N จะถึงเร็วกว่าที่ตั้งใจไว้มาก
    if r is None or r["seq"] == last_seq:
        ui.poll()
        time.sleep_ms(LOOP_MS)
        continue
    last_seq = r["seq"]
    conf = r["conf"]
    name = labels[r["top"]] if r["top"] < len(labels) else "?"

    # สองเงื่อนไขต้องจริงพร้อมกัน: คลาสตรง และมั่นใจพอ
    # ความมั่นใจต่ำ ๆ ที่บังเอิญตรงคลาส คือคำตอบที่โมเดลเดาเอา ไม่ควรนับ
    level = "ALERT" if (name == ALERT_CLASS and conf >= CONF_MIN) else "OK"

    if level == pending:
        streak += 1
    else:
        pending = level
        streak = 1

    # จอรายงานทุกใบที่โมเดลตอบ เพราะคนหน้างานต้องเห็นว่ามันกำลังคิดอะไรอยู่
    l_class.text(name)
    l_class.color(COL_BAD if name == ALERT_CLASS else COL_TEXT)
    seg_conf.text("{:.0f}".format(conf * 100))
    seg_conf.color(COL_OK if conf >= CONF_MIN else COL_WARN)
    bar_streak.color(COL_BAD if pending == "ALERT" else COL_DIM)
    bar_streak.value(streak if streak < CONFIRM_N else CONFIRM_N)
    ch.set_next(s_conf, int(conf * 100))
    ch.set_next(s_min, int(CONF_MIN * 100))

    if streak >= CONFIRM_N and pending != state:
        state, now = pending, time.ticks_ms()
        l_state.text(state)
        l_state.color(STATE_COLOR[state])
        if state != "ALERT":
            l_foot.text("กลับสู่ปกติแล้ว")
            l_foot.color(COL_OK)
            lcd.print("<span class=ok>กลับสู่ปกติ</span>")
        elif last_alert is None or time.ticks_diff(now, last_alert) >= ALERT_GAP_MS:
            alerts += 1
            last_alert = now
            seg_alert.text(str(alerts))
            seg_alert.color(COL_BAD)
            l_foot.text("ส่งใบเตือนแล้ว")
            l_foot.color(COL_BAD)
            lcd.print("<span class=error>เตือนครั้งที่ {} - {}</span>".format(alerts, name))
        else:
            # กลั้นไว้ ไม่ใช่ทิ้ง - จอยังบอกว่าเข้าเขตเตือน คนหน้างานจึงไม่ถูกหลอก
            l_foot.text("เข้าเขตเตือนแต่ยังไม่พ้นช่วงเว้น ยังไม่ส่ง")
            l_foot.color(COL_WARN)
            lcd.print("<span class=warn>เข้าเขตเตือนแต่ยังไม่พ้นช่วงเว้น</span>")

    ui.poll()
    time.sleep_ms(LOOP_MS)

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux, Advance Innovation Centre (AIC), Burapha University
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
