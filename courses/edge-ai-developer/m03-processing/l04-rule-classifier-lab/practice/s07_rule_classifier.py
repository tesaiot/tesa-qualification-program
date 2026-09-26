# s07_rule_classifier.py - จำแนกสภาพอากาศด้วย "กฎ" ที่เราเขียนเอง (ฉบับฝึกเติมโค้ด)
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง AI Kit) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) เติมช่องว่าง (pass) ทั้ง 4 จุดตามคำใบ้ในคอมเมนต์ให้ครบ
#          3) กด "Program to Device" (หรือ Run) แล้วดูคำตัดสินบนจอ
#          4) หายใจรดเซนเซอร์ / เอามือกำบอร์ด / เป่าลมเย็น ดูคลาสที่ชนะเปลี่ยนตามค่าจริง
#
# ชุดบทเรียนนี้เราอยู่ที่ขั้น Processing ของวงจรข้อมูล ต่อจากบทเรียน 3.1–3.2 (แปลงสัญญาณดิบเป็นค่าฟิสิกส์)
# วันนี้เราเดินอีกก้าว: เอาค่าที่แปลงแล้วมา "ตัดสินใจ" เป็นคลาส ด้วยกฎที่เราตั้งเส้นแบ่งเอง
# — นี่คือ classifier ตัวแรกของคอร์ส แต่ยังไม่ใช้ ML เลย เราเขียนกฎด้วยมือทั้งหมด
# (พอถึง โมดูล 5 (Training) คุณจะได้เห็นว่า ML "เรียน" เส้นแบ่งพวกนี้เองจากข้อมูลได้ยังไง)

import ui
ui.screen()
import lcd
import sensors
import dsp
import time

# ธีมสีต่อคลาส (คลาสที่ชนะจะเอาสีนี้ไปทาตัวหนังสือคำตัดสิน)
GREEN  = 0x50D890   # comfortable
AMBER  = 0xE0A03A   # hot
RED    = 0xE85B5B   # danger
CYAN   = 0x71C7EC   # humid
BLUE   = 0x5B8DEF   # cold
YELLOW = 0xE7D14B   # dry
CARD   = 0x223344   # พื้นการ์ด
SEC    = 0xCFC6BF   # ข้อความรอง
WHITE  = 0xFFFFFF

# แผนที่คลาส -> สี ใช้ตอนระบายคำตัดสิน
COLORS = {"comfortable": GREEN, "hot": AMBER, "danger": RED,
          "humid": CYAN, "cold": BLUE, "dry": YELLOW}

lcd.clear()
lcd.console('<h2> Rule-based Weather Classifier</h2>')


def classify(t, h, hi):
    """จำแนกสภาพอากาศด้วย 'บันไดกฎ' (threshold ladder) — เราเป็นคนตั้งเส้นแบ่งเอง
    รับ: t=อุณหภูมิ(C), h=ความชื้น(%RH), hi=heat index 'รู้สึกเหมือน'(C)
    คืน: ชื่อคลาสเป็น str หนึ่งตัวใน COLORS
    """
    # เติม: เขียนบันไดเงื่อนไข ไล่จาก "อันตรายสุด" ลงมา แล้ว return ชื่อคลาส (str)
    #       ใบ้ (ตั้งเส้นแบ่งได้ตามใจ ปรับทีหลังได้):
    #         if hi >= 41: return "danger"    # heat index สูงมาก = อันตราย
    #         if hi >= 32: return "hot"        # รู้สึกร้อน
    #         if h  >= 70: return "humid"      # ชื้นเกิน
    #         if t  <  20: return "cold"       # หนาว
    #         if h  <  30: return "dry"        # แห้ง
    #         return "comfortable"             # นอกนั้น = สบาย
    #       ลำดับสำคัญ! เงื่อนไขบนสุดชนะก่อน (บันไดกฎ = ตรวจทีละขั้นจากบนลงล่าง)
    pass


# อ่านค่าครั้งแรกเพื่อ seed การ์ด (สร้าง widget ครั้งเดียวก่อนเข้าลูป)
p, t = sensors.dps368.pressure_temperature()
h = sensors.sht40.humidity()

ui.Label("TESAIoT Rule Classifier (pre-ML)", x=250, y=8, color=WHITE)

# การ์ดซ้าย: ค่าดิบที่วัดได้ (raw)
ui.Panel(x=40, y=45, w=230, h=150, color=CARD)
ui.Label("Sensor readings", x=70, y=58, color=SEC)
lab_t = ui.Label("temp: --.- C", x=70, y=92, color=CYAN)
lab_h = ui.Label("hum : --.- %", x=70, y=122, color=CYAN)
lab_p = ui.Label("pres: ---- hPa", x=70, y=152, color=CYAN)

# การ์ดกลาง: ค่าอนุพัทธ์ (derived) ที่คำนวณจากค่าดิบ
ui.Panel(x=285, y=45, w=230, h=150, color=CARD)
ui.Label("Derived metrics", x=315, y=58, color=SEC)
lab_dew = ui.Label("dew point: --.- C", x=315, y=92, color=SEC)
lab_hi = ui.Label("feels-like: --.- C", x=315, y=122, color=SEC)

# การ์ดขวา: คำตัดสินจากกฎของเรา + คำตัดสินจากกฎสำเร็จรูปของ dsp
ui.Panel(x=530, y=45, w=230, h=150, color=CARD)
ui.Label("Verdict (our rule)", x=560, y=58, color=SEC)
verdict = ui.Seg7("---", x=555, y=90, color=GREEN)
lab_builtin = ui.Label("dsp.comfort_zone: --", x=545, y=160, color=SEC)

hint = ui.Label("หายใจรดเซนเซอร์ / กำบอร์ด แล้วดูคลาสเปลี่ยน", x=60, y=250, color=SEC)

back = ui.Button("< ออก", x=640, y=350, w=130, h=38)
back_id = back.id()

n = 0
try:
    while True:
        p, t = sensors.dps368.pressure_temperature()
        h = sensors.sht40.humidity()

        # เติม: คำนวณจุดน้ำค้าง (dew point) จาก t,h ด้วย dsp.dew_point(t, h) เก็บใน dp
        dp = 0.0
        pass
        # เติม: คำนวณดัชนีความร้อน "รู้สึกเหมือน" ด้วย dsp.heat_index(t, h) เก็บใน hi
        hi = t
        pass

        lab_t.text("temp: %.1f C" % t)
        lab_h.text("hum : %.1f %%" % h)
        lab_p.text("pres: %.0f hPa" % p)
        lab_dew.text("dew point: %.1f C" % dp)
        lab_hi.text("feels-like: %.1f C" % hi)

        # เรียก classifier ของเราเอง แล้วเอาคลาสที่ได้ไประบายสี
        zone = classify(t, h, hi)
        # เติม: เอาคลาสที่ชนะขึ้นจอด้วย verdict.text(zone) แล้วตั้งสีด้วย
        #       verdict.color(COLORS.get(zone, WHITE))
        pass

        # เทียบกับกฎสำเร็จรูปที่ฝังมาใน firmware (เขียนด้วย C เป็นกฎเหมือนกัน)
        lab_builtin.text("dsp.comfort_zone: %s" % dsp.comfort_zone(t, h))

        n += 1
        if n % 5 == 0:
            lcd.console(' T=%.1fC RH=%.0f%% feels=%.1fC -> %s'
                        % (t, h, hi, zone))

        for ev in ui.poll():
            if ev.get('handle') == back_id:
                raise KeyboardInterrupt
        time.sleep_ms(800)                      # สภาพแวดล้อมเปลี่ยนช้า ~1 Hz พอ
except KeyboardInterrupt:
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
