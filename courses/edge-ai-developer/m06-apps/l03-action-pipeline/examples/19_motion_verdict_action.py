# 19_motion_verdict_action.py - ท่าทางสั่งงาน และราคาของแต่ละคำตัดสิน
#
#
# Why : นาฬิกาที่ปลุกให้จอสว่างเมื่อยกข้อมือ กล่องพัสดุที่บันทึกว่าถูกเขย่าระหว่างขนส่ง
#       และเครื่องมือช่างที่ตื่นเมื่อถูกหยิบขึ้น ทั้งหมดคือการเอาป้ายผลจากโมเดลไป
#       สั่งการจริง ไม่ใช่แค่พิมพ์ออกจอ และของที่สั่งงานผิดเพราะเชื่อคำตัดสินที่
#       ความมั่นใจต่ำ จะกลายเป็นของที่ผู้ใช้ไม่กล้าใช้
# What: คำตัดสินแต่ละใบมีสามอย่างเสมอ ป้าย ความมั่นใจ และเวลาที่ใช้คิด วิศวกร
#       ต้องดูทั้งสามอย่าง เพราะโมเดลที่แม่นแต่ช้าเกินไป ใช้คุมงานจริงไม่ได้
#       และโมเดลที่เร็วแต่มั่นใจต่ำ ก็ไม่ควรได้รับอนุญาตให้สั่งไฟหรือมอเตอร์
#
# ดูที่จอ: ชื่อคลาสตัวใหญ่ด้านล่าง ตัวเลขเขียวคือความมั่นใจเป็นเปอร์เซ็นต์
#          กราฟคือความมั่นใจตามเวลาเทียบกับเกณฑ์ แถบขวาคือเวลาคิดเทียบกับตัวช้าสุด
#          ดูสามอย่างพร้อมกัน อย่าดูแค่ป้าย
# กับดัก : ป้ายของแต่ละโมเดลไม่เหมือนกัน อย่า hardcode ตัวเลขดัชนีคลาส ให้เทียบ
#          จากข้อความในป้ายแทน โมเดลเปลี่ยนแล้วโค้ดจะยังอ่านรู้เรื่อง

import edge_ai
import gpio
import lcd
import time
import ui

MODEL = 0          # 0 = Motion Detection (idle / circle / shaking)
CONF = 0.70

ui.screen()
ui.Label("ท่าทางสั่งงาน", x=12, y=6, value=24)
ch = ui.Chart(x=12, y=40, w=470, h=200, min=0, max=100)
s_conf = 0
s_thr = ch.add_series(0xFF5555)

ui.Label("ฟ้า = ความมั่นใจ %", x=496, y=44, value=16, color=0x00BFFF)
ui.Label("แดง = เกณฑ์สั่งงาน %d%%" % int(CONF * 100), x=496, y=68, value=16,
         color=0xFF5555)
ui.Label("ความมั่นใจ (%)", x=496, y=100, value=16)
seg = ui.Seg7(x=496, y=122, w=180, h=44)
lbl_lat = ui.Label("เวลาคิด -- ms", x=496, y=178, value=16)
bar = ui.Bar(x=496, y=200, w=180, h=16, min=0, max=100)
ui.Label("แถบ = เทียบกับที่ช้าที่สุด", x=496, y=222, value=14)

ui.Panel(x=12, y=252, w=470, h=80)
st = ui.Label("รอคำตัดสินแรก", x=24, y=262, value=28)
sub = ui.Label("ยังไม่มีคำสั่งใด ๆ", x=24, y=300, value=18)
ui.poll()

lcd.clear()
lcd.console("<h2>ท่าทางสั่งงาน</h2>")

desc = edge_ai.model(MODEL)
lcd.print("โมเดล:", desc["name"])
lcd.print("ป้ายทั้งหมด:", ", ".join(desc["labels"]))

edge_ai.select(MODEL)
edge_ai.start()

last_seq = -1
last_label = ""
slowest = 0.0
acted = 0

for _ in range(1500):
    r = edge_ai.result()
    if r is not None and r["seq"] != last_seq:
        last_seq = r["seq"]
        label = (r["label"] or "").lower()
        pct = int(r["conf"] * 100)

        if r["latency_ms"] > slowest:
            slowest = r["latency_ms"]

        ch.set_next(s_conf, pct)
        ch.set_next(s_thr, int(CONF * 100))
        seg.text(str(pct))
        st.text(label if label else "(ไม่มีป้าย)")
        st.color(0x55DD55 if r["conf"] >= CONF else 0xFFC83D)
        lbl_lat.text("เวลาคิด %.2f ms" % r["latency_ms"])
        bar.value(int(r["latency_ms"] / slowest * 100.0))

        # สั่งงานเฉพาะตอนป้ายเปลี่ยนและมั่นใจพอ ไม่ใช่ทุกคำตัดสิน
        if label != last_label and r["conf"] >= CONF:
            last_label = label
            acted += 1
            for i in range(gpio.num_leds()):
                gpio.led(i).off()

            if "shak" in label:
                gpio.led(0).on()
                ui.tone(84, ui.WAVE_SQUARE, 110, 120)
            elif "circle" in label:
                gpio.led(2).on()
                ui.tone(72, ui.WAVE_TRIANGLE, 95, 150)
            else:
                gpio.led(1).on()

            sub.text("สั่งงานครั้งที่ %d เมื่อป้ายเปลี่ยน" % acted)
            lcd.print(label, pct, "% |", round(r["latency_ms"], 1), "ms")

    ui.poll()
    time.sleep_ms(60)

edge_ai.stop()
for i in range(gpio.num_leds()):
    gpio.led(i).off()
sub.text("ช้าที่สุดที่เจอ %.2f ms | สั่งงาน %d ครั้ง" % (slowest, acted))
ui.poll()
lcd.print("ช้าที่สุด", round(slowest, 2), "ms | สั่งงาน", acted, "ครั้ง")
print("เวลาคิดที่ช้าที่สุดที่เจอ:", round(slowest, 1), "ms")

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux, Advance Innovation Centre (AIC), Burapha University
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
