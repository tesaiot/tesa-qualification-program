# s07_rule_classifier.py - จำแนกสภาพอากาศด้วย "กฎ" ที่เราเขียนเอง (เฉลย)
# วิธีรัน: เปิดใน BENTO IDE (บอร์ดจริง AI Kit) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          กด "Program to Device" แล้วหายใจรดเซนเซอร์ / กำบอร์ด / เป่าลม ดูคลาสเปลี่ยน
#
# เฉลยนี้ไม่ได้มีไว้ลอกวาง สิ่งที่นับคือการอธิบายกฎด้วยคำพูดของคุณเอง
# อ่านให้เข้าใจว่า "บันไดกฎ" (threshold ladder) ทำงานยังไง ปิดไฟล์ แล้วพิมพ์ใหม่ด้วยมือ
#
# แก่นของชุดบทเรียนนี้: classifier ตัวแรกของคอร์ส ที่ยัง "ไม่ใช่ ML" — เราตั้งเส้นแบ่งทุกเส้นเอง
# ข้อดีของกฎมือคือ "อธิบายได้ทุกคำตัดสิน" (ขั้นไหนของบันไดที่ยิงคลาสนี้ออกมา) ข้อเสียคือ
# พอเงื่อนไขซับซ้อนขึ้น กฎจะบานและปรับยาก — นั่นคือเหตุผลที่ โมดูล 5 (Training) มี ML เข้ามาช่วย
# สังเกตด้วยว่า heat index (ค่าอนุพัทธ์) จับ "ความรู้สึกร้อน" ตอนชื้นได้ ที่อุณหภูมิดิบเปล่าๆ ไม่เห็น

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
    """จำแนกสภาพอากาศด้วย 'บันไดกฎ' — เราเป็นคนตั้งเส้นแบ่งเองทุกเส้น
    รับ: t=อุณหภูมิ(C), h=ความชื้น(%RH), hi=heat index 'รู้สึกเหมือน'(C)
    คืน: ชื่อคลาสเป็น str หนึ่งตัวใน COLORS

    บันไดกฎ = ตรวจเงื่อนไขทีละขั้นจากบนลงล่าง ขั้นแรกที่จริงชนะทันที (return แล้วจบ)
    เพราะงั้น "ลำดับ" คือหัวใจ: อันตรายสุดต้องอยู่บนสุด ไม่งั้นจะโดนคลาสอื่นแย่งไปก่อน
    """
    if hi >= 41:                    # heat index สูงมาก = เสี่ยงฮีตสโตรก
        return "danger"
    if hi >= 32:                    # รู้สึกร้อน (ใช้ค่า 'รู้สึกเหมือน' ไม่ใช่ t ดิบ)
        return "hot"
    if h >= 70:                     # ชื้นเกินไป อึดอัด
        return "humid"
    if t < 20:                      # หนาว
        return "cold"
    if h < 30:                      # อากาศแห้ง
        return "dry"
    return "comfortable"            # ผ่านทุกด่าน = สบายดี


# อ่านค่าครั้งแรกเพื่อ seed การ์ด (สร้าง widget ครั้งเดียวก่อนเข้าลูป จอจะได้ไม่กระพริบ)
p, t = sensors.dps368.pressure_temperature()
h = sensors.sht40.humidity()

ui.Label("TESAIoT Rule Classifier (pre-ML)", x=250, y=8, color=WHITE)

# การ์ดซ้าย: ค่าดิบที่วัดได้ (raw) — วัตถุดิบตั้งต้น
ui.Panel(x=40, y=45, w=230, h=150, color=CARD)
ui.Label("Sensor readings", x=70, y=58, color=SEC)
lab_t = ui.Label("temp: --.- C", x=70, y=92, color=CYAN)
lab_h = ui.Label("hum : --.- %", x=70, y=122, color=CYAN)
lab_p = ui.Label("pres: ---- hPa", x=70, y=152, color=CYAN)

# การ์ดกลาง: ค่าอนุพัทธ์ (derived) ที่ dsp คำนวณให้จากค่าดิบ
ui.Panel(x=285, y=45, w=230, h=150, color=CARD)
ui.Label("Derived metrics", x=315, y=58, color=SEC)
lab_dew = ui.Label("dew point: --.- C", x=315, y=92, color=SEC)
lab_hi = ui.Label("feels-like: --.- C", x=315, y=122, color=SEC)

# การ์ดขวา: คำตัดสินจากกฎของเรา + คำตัดสินจากกฎสำเร็จรูปของ dsp (ไว้เทียบ)
ui.Panel(x=530, y=45, w=230, h=150, color=CARD)
ui.Label("Verdict (our rule)", x=560, y=58, color=SEC)
verdict = ui.Seg7("---", x=555, y=90, color=GREEN)
lab_builtin = ui.Label("dsp.comfort_zone: --", x=545, y=160, color=SEC)

hint = ui.Label("หายใจรดเซนเซอร์ / กำบอร์ด แล้วดูคลาสเปลี่ยน", x=60, y=250, color=SEC)

back = ui.Button("< ออก", x=560, y=350, w=130, h=38)
back_id = back.id()

n = 0
try:
    while True:
        # 1) อ่านค่าดิบ: อุณหภูมิ+ความดันจาก DPS368, ความชื้นจาก SHT40 (AI Kit มีทั้งคู่)
        p, t = sensors.dps368.pressure_temperature()
        h = sensors.sht40.humidity()

        # 2) แปลงเป็นค่าอนุพัทธ์ — สองสูตรฟิสิกส์นี้ dsp คำนวณให้ เราแค่เรียกใช้
        dp = dsp.dew_point(t, h)        # จุดน้ำค้าง: ชื้นแค่ไหนถึงจะกลั่นเป็นหยดน้ำ
        hi = dsp.heat_index(t, h)       # ดัชนีความร้อน: ร้อน+ชื้น -> "รู้สึกเหมือน" กี่องศา

        lab_t.text("temp: %.1f C" % t)
        lab_h.text("hum : %.1f %%" % h)
        lab_p.text("pres: %.0f hPa" % p)
        lab_dew.text("dew point: %.1f C" % dp)
        lab_hi.text("feels-like: %.1f C" % hi)

        # 3) ตัดสินใจด้วยกฎของเรา แล้วเอาคลาสไประบายสีตามแผนที่ COLORS
        zone = classify(t, h, hi)
        verdict.text(zone)
        verdict.color(COLORS.get(zone, WHITE))

        # 4) เทียบกับกฎสำเร็จรูปใน firmware (dsp.comfort_zone ก็เป็นบันไดกฎเหมือนกัน แต่เขียนด้วย C)
        #    ค่าอาจไม่ตรงกัน 100% เพราะเราตั้งเส้นแบ่งคนละชุด — จดประเด็นนี้ลงบันทึกการเรียนของคุณ
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
