# 12 - Edge AI Menu: เลือกและรันโมเดล AI ได้ทุกตัวในเฟิร์มแวร์เดียว (ไม่ต้องต่อเน็ต)
#
# บอร์ดมีโมเดล DEEPCRAFT หลายตัวคอมไพล์รวมไว้ (Motion / Baby Cry / Radar / Cough /
# Alarm / Siren) รันบน CM55 (Ethos-U55 NPU) โมดูล edge_ai อ่าน "ทะเบียนโมเดล"
# จาก CM55 แบบ pull (ปลอดภัย ไม่ค้าง) แล้วสลับโมเดลได้สดๆ ด้วย edge_ai.select(n)
#
# หน้านี้จำลอง layout ของหน้า Edge AI จริงในเฟิร์มแวร์ (page_edge_ai.c) เป๊ะที่สุด
# เท่าที่ ui module ทำได้: control row (dropdown + ปุ่ม Load/Stop สถานะเดียว + LED
# + chip), การ์ด verdict กว้างเต็มจอด้านบน, แถบความมั่นใจต่อคลาสเต็มความกว้าง,
# บรรทัด latency + engine badge — ใช้สีจากธีมเดียวกัน (tesaiot_ui_theme.h)
import edge_ai
import ui
ui.screen()
import lcd
import time

# ---- สีจากธีมจริง tesaiot_ui_theme.h ----
PURPLE  = 0xBB86FC   # AI indicator / หัวข้อ
GREEN   = 0x50D890   # active / winner / RUNNING
ORANGE  = 0xF2B84B   # LOADING
RED     = 0xE85B5B   # STOPPED / error
CYAN    = 0x71C7EC   # latency / info
CARD    = 0x2A1712   # BG_CARD (warm glass)
PRIMARY = 0xF5F2EE   # TEXT_PRIMARY (warm white)
SEC     = 0xCFC6BF   # TEXT_SECONDARY
DIM     = 0x9A918A   # TEXT_DISABLED / แถบที่ไม่ชนะ
BAR_OFF = 0x4A2520   # BG_SURFACE (แถบพื้น)

SENSOR = ("IMU", "RADAR", "MIC")

lcd.clear()
lcd.console('<h2> Edge AI - เมนูโมเดล</h2>')
lcd.console(' links: %s' % str(edge_ai.links()))

models = edge_ai.models()
names = [m['name'] for m in models]
short = [n.split(" Detect")[0] for n in names]   # ตัด " Detect..." (เฟิร์มแวร์ตัดชื่อที่ 15 ตัว)
lcd.console(' พบ %d โมเดล: %s' % (len(models), ", ".join(names)))

# ================= สร้าง widget ครั้งเดียว (เลียนหน้า Edge AI จริง) =================
ui.Label("Edge AI", x=20, y=44, color=PURPLE)
ui.Label("Ethos-U55 NPU", x=632, y=46, color=GREEN)          # engine badge (บนขวา)

# ---- control row: dropdown ใหญ่ | ปุ่มสถานะเดียวใหญ่ | LED + chip ----
dd = ui.Dropdown(text="\n".join(short), x=20, y=72, w=340, h=52)   # ชื่อสั้น กล่องพอดี
btn = ui.Button("Load", x=462, y=72, w=160, h=52, color=GREEN)
led = ui.Panel(x=638, y=88, w=20, h=20, color=RED)
chip = ui.Label("STOPPED", x=666, y=90, color=DIM)

# ---- การ์ด verdict (เด่นสุด, กว้างเต็มจอ) ----
ui.Panel(x=16, y=138, w=760, h=72, color=CARD)
desc = ui.Label("Select a model, then Load", x=300, y=144, color=SEC)
verdict = ui.Seg7("--", x=350, y=164, color=PRIMARY)   # Seg7 = ฟอนต์ใหญ่ (เหมือน H1)

# ---- แถบความมั่นใจต่อคลาส (เต็มความกว้าง) — สร้าง 5 แถว โชว์เฉพาะของโมเดล ----
ROW_Y0, ROW_DY = 220, 30
rows = []
for i in range(5):
    y = ROW_Y0 + i * ROW_DY
    lb = ui.Label("", x=24, y=y, color=SEC)
    br = ui.Bar(x=170, y=y + 2, w=470, h=18, min=0, max=100, value=0, color=BAR_OFF)
    pc = ui.Label("", x=650, y=y, color=DIM)
    lb.hide(); br.hide(); pc.hide()
    rows.append((lb, br, pc))

# ---- บรรทัด stats ----
lat = ui.Label("inference: -- ms", x=24, y=376, color=CYAN)

back = ui.Button("< ออก", x=560, y=350, w=120, h=38)   # ขวาสุด 680 พ้นปุ่ม console (702)
back_id = back.id()
dd_id = dd.id()
btn_id = btn.id()


def show_rows(mi):
    labels = models[mi]['labels']
    for i, (lb, br, pc) in enumerate(rows):
        if i < len(labels):
            lb.text(labels[i]); lb.color(SEC)
            br.value(0); br.color(BAR_OFF)
            pc.text("0%")
            lb.show(); br.show(); pc.show()
        else:
            lb.hide(); br.hide(); pc.hide()


def refresh_btn():
    """ปุ่มสถานะเดียว: Stop(แดง) ถ้าโมเดลที่เลือก = ตัวที่รันอยู่, ไม่งั้น Load(เขียว)."""
    if active >= 0 and sel == active:
        btn.text("Stop"); btn.color(RED)
    else:
        btn.text("Load"); btn.color(GREEN)


sel = 0            # โมเดลที่เลือกใน dropdown
active = -1        # โมเดลที่กำลังรัน (-1 = ไม่มี)
last_seq = -1
show_rows(sel)
refresh_btn()
lcd.console(' เลือกโมเดลใน dropdown แล้วกด Load')

try:
    while True:
        for ev in ui.poll():
            h = ev.get('handle')
            t = ev.get('type')
            if h == back_id:
                raise KeyboardInterrupt
            elif h == dd_id and t == 'value_changed':
                sel = ev.get('value')
                verdict.text("--"); desc.text("Select a model, then Load")
                lat.text("inference: -- ms")
                show_rows(sel)
                refresh_btn()
                lcd.console(' เลือก: %s (%s)'
                            % (models[sel]['name'], SENSOR[models[sel]['sensor']]))
            elif h == btn_id:
                if active >= 0 and sel == active:            # Stop
                    edge_ai.stop()
                    active = -1
                    led.color(RED); chip.text("STOPPED"); chip.color(DIM)
                    verdict.text("--"); desc.text("Select a model, then Load")
                    lcd.console(' หยุดโมเดล')
                else:                                        # Load / Switch
                    # confirm budget ฝั่ง C = 500ms; cold-load โมเดลแรกอาจนานกว่านั้น
                    # → retry ไม่กี่ครั้ง (โมเดลกำลังโหลดจริง แค่ยัง confirm ไม่ทัน)
                    led.color(ORANGE); chip.text("LOADING"); chip.color(ORANGE)
                    ok = False
                    for _try in range(3):
                        try:
                            edge_ai.select(models[sel]['index'])
                            ok = True; break
                        except OSError:
                            time.sleep_ms(300)
                    if ok:
                        active = sel; last_seq = -1
                        led.color(GREEN); chip.text("RUNNING"); chip.color(GREEN)
                        desc.text(short[sel])   # ชื่อสั้น ไม่ตัด
                        lcd.console('<span class=ok> รัน %s</span>' % models[sel]['name'])
                    else:
                        active = -1
                        led.color(RED); chip.text("FAILED"); chip.color(RED)
                        lcd.console('<span class=error> โหลดไม่สำเร็จ (confirm timeout)</span>')
                refresh_btn()

        # อัปเดตเฉพาะตอนมีผลอนุมานใหม่ (seq เปลี่ยน)
        if active >= 0:
            r = edge_ai.result()
            if r and r['seq'] != last_seq:
                last_seq = r['seq']
                verdict.text(r['label'] or '-')
                lat.text("inference: %.1f ms" % r['latency_ms'])
                top = r['top']
                for i, (lb, br, pc) in enumerate(rows):
                    if i < len(r['scores']):
                        pctv = int(r['scores'][i] * 100)
                        br.value(pctv); br.color(GREEN if i == top else BAR_OFF)
                        pc.text("%d%%" % pctv); pc.color(PRIMARY if i == top else DIM)
                        lb.color(PRIMARY if i == top else SEC)

        time.sleep_ms(180)
except KeyboardInterrupt:
    pass
finally:
    edge_ai.stop()
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
