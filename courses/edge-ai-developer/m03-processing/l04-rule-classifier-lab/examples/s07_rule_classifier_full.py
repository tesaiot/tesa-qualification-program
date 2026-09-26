# s07_rule_classifier_full.py - จำแนกสภาพอากาศด้วยกฎ (ฉบับเต็ม)
# วิธีรัน: เปิดใน BENTO IDE (บอร์ดจริง AI Kit) หรือ BENTO Emulator (ide.tesaiot.dev)
#          กด "Program to Device" (หรือ Run) แล้วหายใจรดเซนเซอร์ / กำบอร์ด / เป่าลมเย็น
#
# ฉบับนี้คือเวอร์ชันขัดเรียบร้อยของ s07_rule_classifier.py — โครงกฎเดียวกับที่คุณเติม
# ในไฟล์ฝึก แต่เพิ่มสามอย่างที่ทำให้ classifier แบบกฎ "น่าเชื่อถือ + อธิบายได้" มากขึ้น:
#   1) rule trace — บอกว่า "ขั้นไหนของบันได" ที่ยิงคลาสนี้ออกมา (จุดแข็งของกฎมือ: อธิบายได้)
#   2) เทียบกับ dsp.comfort_zone (กฎสำเร็จรูปใน firmware) พร้อมไฟบอกว่าตรง/ต่างกัน
#   3) ฮิสเทอรีซิส (hysteresis) กันคลาสกระพริบตอนค่าวัดสั่นคร่อมเส้นแบ่งพอดี
# ทั้งหมดยังยืนบนแนวคิดเดียว: derived metric (dew point / heat index) -> บันไดกฎ -> คลาส

import ui
ui.screen()
import lcd
import sensors
import dsp
import time

# ธีมสีต่อคลาส
GREEN  = 0x50D890   # comfortable
AMBER  = 0xE0A03A   # hot
RED    = 0xE85B5B   # danger
CYAN   = 0x71C7EC   # humid
BLUE   = 0x5B8DEF   # cold
YELLOW = 0xE7D14B   # dry
CARD   = 0x223344
SEC    = 0xCFC6BF
WHITE  = 0xFFFFFF
OK     = 0x50D890
WARN   = 0xE0A03A

COLORS = {"comfortable": GREEN, "hot": AMBER, "danger": RED,
          "humid": CYAN, "cold": BLUE, "dry": YELLOW}

# เส้นแบ่งของบันไดกฎ รวบไว้ที่เดียว ปรับค่าที่นี่แล้วทั้งกฎขยับตาม (magic number ห้ามฝังในโค้ด)
HI_DANGER = 41.0    # heat index >= นี่ = อันตราย
HI_HOT    = 32.0    # heat index >= นี่ = ร้อน
RH_HUMID  = 70.0    # ความชื้น >= นี่ = ชื้น
T_COLD    = 20.0    # อุณหภูมิ < นี่ = หนาว
RH_DRY    = 30.0    # ความชื้น < นี่ = แห้ง
MARGIN    = 0.6     # แถบฮิสเทอรีซิส: ต้องข้ามเส้นเกินระยะนี้ถึงจะยอมเปลี่ยนคลาส

lcd.clear()
lcd.console('<h2> Rule-based Weather Classifier (full)</h2>')


def classify(t, h, hi):
    """บันไดกฎ — คืน (คลาส, เหตุผล) เพื่อให้ 'อธิบายได้' ว่าขั้นไหนที่ยิงคลาสนี้ออกมา
    ตรวจจากบนลงล่าง ขั้นแรกที่จริงชนะทันที ('ลำดับ' คือหัวใจของบันไดกฎ)
    """
    if hi >= HI_DANGER:
        return "danger", "feels-like %.0f >= %.0f" % (hi, HI_DANGER)
    if hi >= HI_HOT:
        return "hot", "feels-like %.0f >= %.0f" % (hi, HI_HOT)
    if h >= RH_HUMID:
        return "humid", "RH %.0f >= %.0f" % (h, RH_HUMID)
    if t < T_COLD:
        return "cold", "temp %.0f < %.0f" % (t, T_COLD)
    if h < RH_DRY:
        return "dry", "RH %.0f < %.0f" % (h, RH_DRY)
    return "comfortable", "in all comfort bounds"


# seed การ์ดด้วยค่าจริงหนึ่งครั้ง (สร้าง widget ครั้งเดียวก่อนลูป)
p, t = sensors.dps368.pressure_temperature()
h = sensors.sht40.humidity()

ui.Label("TESAIoT Rule Classifier (pre-ML)", x=250, y=8, color=WHITE)

ui.Panel(x=40, y=45, w=230, h=160, color=CARD)
ui.Label("Sensor readings", x=70, y=58, color=SEC)
lab_t = ui.Label("temp: --.- C", x=70, y=92, color=CYAN)
lab_h = ui.Label("hum : --.- %", x=70, y=122, color=CYAN)
lab_p = ui.Label("pres: ---- hPa", x=70, y=152, color=CYAN)
arc_h = ui.Arc(x=180, y=95, min=0, max=100, value=int(h))

ui.Panel(x=285, y=45, w=230, h=160, color=CARD)
ui.Label("Derived metrics", x=315, y=58, color=SEC)
lab_dew = ui.Label("dew point: --.- C", x=315, y=92, color=SEC)
lab_hi = ui.Label("feels-like: --.- C", x=315, y=122, color=SEC)
lab_delta = ui.Label("feels vs temp: --", x=315, y=152, color=SEC)

ui.Panel(x=530, y=45, w=230, h=160, color=CARD)
ui.Label("Verdict (our rule)", x=560, y=58, color=SEC)
verdict = ui.Seg7("---", x=555, y=88, color=GREEN)
lab_why = ui.Label("why: --", x=545, y=150, color=SEC)
lab_builtin = ui.Label("builtin: --  [--]", x=545, y=176, color=SEC)

hint = ui.Label("หายใจรด/กำบอร์ด แล้วดูคลาส+เหตุผลเปลี่ยน", x=60, y=260, color=SEC)

back = ui.Button("< ออก", x=560, y=350, w=130, h=38)
back_id = back.id()

zone = "comfortable"        # คลาสปัจจุบัน (ใช้กับฮิสเทอรีซิส)
n = 0
try:
    while True:
        p, t = sensors.dps368.pressure_temperature()
        h = sensors.sht40.humidity()

        dp = dsp.dew_point(t, h)
        hi = dsp.heat_index(t, h)

        lab_t.text("temp: %.1f C" % t)
        lab_h.text("hum : %.1f %%" % h)
        lab_p.text("pres: %.0f hPa" % p)
        arc_h.value(int(max(0, min(100, h))))
        lab_dew.text("dew point: %.1f C" % dp)
        lab_hi.text("feels-like: %.1f C" % hi)
        lab_delta.text("feels vs temp: %+.1f C" % (hi - t))

        # ตัดสินด้วยกฎ + ฮิสเทอรีซิส: เปลี่ยนคลาสเฉพาะเมื่อเข้าเงื่อนไขใหม่ "ชัดพอ"
        new_zone, reason = classify(t, h, hi)
        if new_zone != zone:
            # เผื่อ margin: ถ้า heat index แค่ไต่คร่อมเส้นนิดเดียว อย่าเพิ่งสลับ (กันกระพริบ)
            _, reason2 = classify(t, h, hi - MARGIN if hi >= HI_HOT else hi + MARGIN)
            if reason2 == reason or new_zone in ("danger", "cold", "humid", "dry"):
                zone = new_zone
        verdict.text(zone)
        verdict.color(COLORS.get(zone, WHITE))
        lab_why.text("why: %s" % reason)

        # เทียบกับกฎสำเร็จรูปใน firmware — ไฟเขียว=ตรงกัน, เหลือง=ต่างกัน (คนละชุดเส้นแบ่ง)
        builtin = dsp.comfort_zone(t, h)
        agree = (builtin == zone)
        lab_builtin.text("builtin: %s  [%s]" % (builtin, "=" if agree else "x"))
        lab_builtin.color(OK if agree else WARN)

        n += 1
        if n % 5 == 0:
            lcd.console(' T=%.1fC RH=%.0f%% feels=%.1fC -> %s (%s)'
                        % (t, h, hi, zone, reason))

        for ev in ui.poll():
            if ev.get('handle') == back_id:
                raise KeyboardInterrupt
        time.sleep_ms(700)
except KeyboardInterrupt:
    pass
finally:
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
