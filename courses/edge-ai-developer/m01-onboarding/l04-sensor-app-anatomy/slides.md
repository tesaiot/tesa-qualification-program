---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 1.4 — แกะแอปเซนเซอร์: โครงร่วมสี่จังหวะของทุกโปรแกรม"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · ดัดแปลงจาก Edge AI Developer (รศ.วิรุฬห์ ศรีบริรักษ์, BUU) · CC BY-NC 4.0"
---
<style>
section { font-size: 24px; padding: 40px 52px; justify-content: flex-start; }
section h1 { font-size: 1.45em; line-height: 1.12; margin: 0 0 .22em; }
section h2 { font-size: 1.12em; margin: .15em 0; }
section h3 { font-size: 1.0em; margin: .12em 0; }
section p, section li { margin: .16em 0; line-height: 1.32; }
section img { max-width: 100%; height: auto; }
section svg { max-height: 250px; }
section table { font-size: .78em; }
section pre { font-size: .70em; line-height: 1.32; background:#0d1117; color:#e6edf3; border:1px solid #30363d; border-radius:8px; padding:12px 16px; box-shadow:0 2px 8px rgba(0,0,0,.25); }
section pre code { white-space: pre-wrap; background:transparent; color:inherit; } section pre .hljs-comment{color:#8b949e;font-style:italic} section pre .hljs-keyword,section pre .hljs-built_in,section pre .hljs-literal{color:#ff7b72} section pre .hljs-string{color:#a5d6ff} section pre .hljs-number{color:#79c0ff} section pre .hljs-title,section pre .hljs-title.function_,section pre .hljs-section{color:#d2a8ff} section pre .hljs-meta{color:#ffa657} section pre .hljs-attr,section pre .hljs-attribute,section pre .hljs-name{color:#7ee787}
section blockquote { margin: .25em 0; font-size: .92em; }
/* two images on a line (parity / 2x2 grids) stay side-by-side and small */
section p > img + img { margin-left: 10px; }
/* scroll-within-slide: dense slides scroll instead of clipping */
section { overflow-y: auto; overflow-x: hidden; }
section::-webkit-scrollbar { width: 11px; }
section::-webkit-scrollbar-thumb { background:#4a90d9; border-radius:6px; }
section::-webkit-scrollbar-track { background:rgba(0,0,0,.06); }
/* image drop-shadow + cover-slide readability (auto) */
section img{filter:drop-shadow(0 3px 12px rgba(0,0,0,.5))}
section.cover *{color:#fff !important}
section.cover h1,section.cover h2,section.cover h3,section.cover p,section.cover li,section.cover strong,section.cover em,section.cover blockquote,section.cover div{text-shadow:0 2px 9px rgba(0,0,0,.92),0 0 3px rgba(0,0,0,.8)}
section.cover div[style*="background:#"],section.cover div[style*="background: #"]{background:rgba(10,14,20,.66) !important;border-color:rgba(120,200,255,.45) !important;max-width:62%}
section.cover blockquote{border-left:4px solid rgba(120,200,255,.6) !important;background:rgba(13,17,23,.55) !important;border-radius:6px;padding:.3em .6em}
section.cover h1,section.cover h2,section.cover h3,section.cover p,section.cover blockquote{max-width:60%}
section.cover div:not(:has(img)){max-width:62%}
section.cover img{filter:none}
</style>

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

# บทเรียน 1.4 — แกะแอปเซนเซอร์: โครงร่วมสี่จังหวะของทุกโปรแกรม
## โครงร่วมของทุกโปรแกรม แล้ว remix เป็นของเรา

**โมดูล 1 — เริ่มต้น: รันของจริงแล้วแกะดูข้างใน**

**โมดูล 1 — Onboarding · กลับด้าน (ต่อจากบทเรียน 1.1–1.3)**

> คาถาประจำบทเรียน: **"อ่านโค้ดที่ทำงานได้ให้ออกก่อน แล้วจะแก้มันให้เป็นของเราได้ — โปรแกรมเกือบทุกตัวเดินตามโครงเดียวกัน"**

MicroPython บนบอร์ด BENTO · `sensors.*` · `dsp.tilt` · `ui.poll`

---

# เปิดบทเรียนด้วยการอ่านของจริงก่อน

ชุดบทเรียนก่อนหน้าเรา **รัน** โมเดลสำเร็จรูปได้แล้ว วันนี้เราขยับอีกขั้นของ **กลับด้าน** — เอาแอปที่ทำงานได้จริงมา **แกะ** ให้เห็นโครง แล้ว **แก้** ให้เป็นของเราเอง

<div style="text-align:center;margin:10px 0">
<svg width="820" height="150" viewBox="0 0 820 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arOpen" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="40" width="180" height="70" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="104" y="72" font-size="15" font-weight="700" fill="#2e7d32" text-anchor="middle">Run รันของจริง</text>
  <text x="104" y="94" font-size="12" fill="#555" text-anchor="middle">01 / 02 / 04</text>
  <rect x="234" y="40" width="180" height="70" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="324" y="72" font-size="15" font-weight="700" fill="#1565c0" text-anchor="middle">Investigate แกะ</text>
  <text x="324" y="94" font-size="12" fill="#555" text-anchor="middle">โครงร่วม 4 จังหวะ</text>
  <rect x="454" y="40" width="180" height="70" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="544" y="72" font-size="15" font-weight="700" fill="#e65100" text-anchor="middle">Modify remix</text>
  <text x="544" y="94" font-size="12" fill="#555" text-anchor="middle">สลับเซนเซอร์/จอ</text>
  <rect x="674" y="40" width="132" height="70" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="740" y="72" font-size="15" font-weight="700" fill="#6a1b9a" text-anchor="middle">Make ต่อยอด</text>
  <text x="740" y="94" font-size="12" fill="#555" text-anchor="middle">ชุดบทเรียนถัดไป</text>
  <line x1="194" y1="75" x2="230" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="414" y1="75" x2="450" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="634" y1="75" x2="670" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
</svg>
</div>

บทเรียน 1.1–1.3 เราอยู่ที่ **Run** วันนี้เราลงลึกสอง P กลาง — **Investigate** (แกะโครง) กับ **Modify** (remix) ของ **PRIMM** วิธีนี้ทำให้คุณ "เป็นเจ้าของโค้ด" ได้โดยไม่ต้องเขียนจากศูนย์ ซึ่งยากเกินไปสำหรับตอนนี้

> อ่านโค้ดคนอื่นให้ออกคือทักษะวิศวกรที่จริงกว่าเขียนใหม่จากว่าง — ในงานจริงเราแก้ของที่มีอยู่มากกว่าสร้างใหม่เสมอ

---

# เป้าหมายของชุดบทเรียนนี้

จบชุดบทเรียนนี้เราจะทำครบ 4 เรื่อง แล้วปิดท้ายด้วย remix ที่รันได้จริง:

1. **อ่านแอปเซนเซอร์ที่ทำงานได้** (`01` IMU, `02` tilt, `04` radar) แล้วเห็นว่ามันต่างกันแต่โครงเหมือนกัน
2. **โครงร่วม 4 จังหวะ** — import → สร้าง widget ครั้งเดียว → ลูป → `ui.poll` (+ ปุ่ม back) โครงที่เจอซ้ำทั้งคอร์ส
3. **รู้จัก `sensors.*`** — อ่านค่าจริงจากบอร์ด และ **`dsp.tilt`** — ยกงานคณิตให้ฝั่ง C ทำ
4. **remix เอง** — สลับเซนเซอร์ / เปลี่ยนการแสดงผล / ลองพังแล้วซ่อม (break-and-fix)

ปลายทางของวันนี้: [`s02_anatomy_sensor.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l05-sensor-remix-lab/practice/s02_anatomy_sensor.py) — remix ที่ผสมทั้งสามตัวอย่าง เอียงบอร์ดแล้วเข็มขยับ มุมเด่นขึ้นจอ ป้ายเปลี่ยนสีเมื่อเอียงเกินเกณฑ์

> วันนี้ยังไม่เขียนของใหม่จากศูนย์ เราฝึก "อ่านออก + แก้เป็น" ก่อน — พอจับโครงร่วมได้ ชุดบทเรียนถัด ๆ ไปการสร้างเองจะง่ายขึ้นมาก

---

# ทบทวนบทเรียน 1.1–1.3 สั้นๆ — เราอยู่ตรงไหน

ชุดบทเรียนก่อนหน้าเราเปิดคอร์สด้วยการรันเมนู 6 โมเดล อ่านคลาสที่ชนะ + ความมั่นใจได้ — นั่นคือขั้น **Apps** (ปลายวงจร)

- เราเห็นแล้วว่า MicroPython บน BENTO สั่งงานได้ด้วยโค้ดไม่กี่บรรทัด
- ตอนท้ายบทเรียน 1.1–1.3 เราแอบเห็น **"โครงร่วม"** ผ่านๆ: import → สร้างครั้งเดียว → ลูป → `ui.poll`
- ชุดบทเรียนนี้เราจะ **แกะโครงนั้นให้ขาด** โดยใช้แอปเซนเซอร์ที่เรียบง่ายกว่าโมเดล AI เป็นตัวอย่าง

<div style="text-align:center;margin:8px 0">
<svg width="760" height="96" viewBox="0 0 760 96" font-family="DejaVu Sans, sans-serif">
  <line x1="40" y1="48" x2="720" y2="48" stroke="#cfd8dc" stroke-width="3"/>
  <circle cx="150" cy="48" r="9" fill="#607d8b"/>
  <text x="150" y="30" font-size="12" font-weight="700" fill="#607d8b" text-anchor="middle">บทเรียน 1.1–1.3</text>
  <text x="150" y="74" font-size="11" fill="#777" text-anchor="middle">รันโมเดลสำเร็จ</text>
  <circle cx="380" cy="48" r="10" fill="#00838f"/>
  <text x="380" y="30" font-size="12" font-weight="700" fill="#00838f" text-anchor="middle">บทเรียน 1.4–1.5 (วันนี้)</text>
  <text x="380" y="74" font-size="11" fill="#777" text-anchor="middle">แกะโครง + remix แอปเซนเซอร์</text>
  <circle cx="610" cy="48" r="9" fill="#6a1b9a"/>
  <text x="610" y="30" font-size="12" font-weight="700" fill="#6a1b9a" text-anchor="middle">บทเรียน 1.6–1.7+</text>
  <text x="610" y="74" font-size="11" fill="#777" text-anchor="middle">แกะแอป Edge AI แล้วสร้างเอง</text>
</svg>
</div>

> เราเลือกแกะ "แอปเซนเซอร์" ก่อนแอป AI เพราะมันมีแค่ อ่านค่า → คำนวณ → วาดจอ ไม่มีเรื่องโมเดล/IPC ข้ามคอร์มาบัง ทำให้เห็นโครงเปล่าๆ ชัดที่สุด

---

# รันของจริงก่อน (1) — IMU 6 แกน

เปิด [`01_imu_6axis.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l04-sensor-app-anatomy/examples/01_imu_6axis.py) รันดูก่อน แล้วขยับ/เขย่าบอร์ด ตัวเลข 6 แกนวิ่งตามทันที:

```python
import ui
ui.screen()
import lcd, sensors, time

ui.Label("BMI270 - Accelerometer + Gyroscope", x=210, y=10, color=0xFFFFFF)
la = [ui.Label("AX: --", x=60,  y=60 + i * 40, color=0x44CCFF) for i in range(3)]
mag_bar = ui.Bar(x=60, y=225, w=650, min=0, max=300, value=98)
back = ui.Button("< ออก", x=640, y=350, w=130, h=38); back_id = back.id()

while True:
    ax, ay, az, gx, gy, gz = sensors.bmi270.motion()   # อ่าน 6 แกนพร้อมกัน
    mag = (ax*ax + ay*ay + az*az) ** 0.5
    mag_bar.value(int(mag * 10))                        # วางนิ่ง ~98
    for ev in ui.poll():
        if ev.get('handle') == back_id:
            raise KeyboardInterrupt
    time.sleep_ms(100)
```

> ก่อนจะแกะ ให้รันมันก่อนเสมอ — เห็นของทำงานแล้วสมองจะอยากรู้ "มันทำงานยังไง" นี่คือหัวใจของ กลับด้าน

---

# รันของจริงก่อน (2) — เรดาร์ตรวจการมีคน

เปิด [`04_radar_presence.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l04-sensor-app-anatomy/examples/04_radar_presence.py) แล้วนั่งนิ่งหน้าบอร์ด vs ออกนอกระยะ ป้ายเปลี่ยนจาก CLEAR เป็น PRESENCE:

```python
panel = ui.Panel(x=100, y=50, w=590, h=220, color=0x115511)
state = ui.Label("CLEAR", x=330, y=140, color=0xFFFFFF)
back = ui.Button("< ออก", x=640, y=350, w=130, h=38); back_id = back.id()

was = None
while True:
    r = sensors.radar()
    now = bool(r["presence"])
    if now != was:                       # วาดใหม่ "เฉพาะตอนสถานะเปลี่ยน"
        panel.color(0x881111 if now else 0x115511)
        state.text("PRESENCE" if now else "CLEAR")
        was = now
    for ev in ui.poll():
        if ev.get('handle') == back_id:
            raise KeyboardInterrupt
    time.sleep_ms(300)
```

> สังเกตว่าโค้ดคนละเซนเซอร์ (`radar()` ไม่ใช่ `bmi270.motion()`) คนละหน้าตาจอ แต่วางตัวเหมือนกันเป๊ะ — นี่แหละคือ "โครงร่วม" ที่เราจะแกะกัน

---

# สามแอปต่างกัน แต่โครงเดียวกัน

`01` โชว์ตัวเลข 6 แกน · `02` โชว์เกจมุมเอียง · `04` โชว์ป้ายมีคน/ไม่มีคน — เซนเซอร์คนละตัว จอคนละแบบ แต่ถ้ามองข้ามรายละเอียด ทั้งสามเดินตาม **สี่จังหวะ** เดียวกัน

<div style="text-align:center;margin:6px 0">
<svg width="900" height="230" viewBox="0 0 900 230" font-family="DejaVu Sans, sans-serif">
  <g font-size="12" text-anchor="middle">
    <text x="150" y="20" font-weight="700" fill="#1565c0">01 IMU</text>
    <text x="450" y="20" font-weight="700" fill="#2e7d32">02 Tilt</text>
    <text x="750" y="20" font-weight="700" fill="#ef6c00">04 Radar</text>
  </g>
  <g font-size="11" text-anchor="start" fill="#455a64">
    <rect x="20" y="34" width="860" height="42" rx="8" fill="#eceff1" stroke="#607d8b"/>
    <text x="34" y="52" font-weight="700">1 · import</text>
    <text x="150" y="52" text-anchor="middle">ui/sensors/time</text>
    <text x="450" y="52" text-anchor="middle">+ dsp</text>
    <text x="750" y="52" text-anchor="middle">ui/sensors/time</text>
    <text x="34" y="68" fill="#888" font-size="10">เหมือนกันเกือบหมด ต่างแค่ import dsp เพิ่มใน 02</text>
    <rect x="20" y="82" width="860" height="42" rx="8" fill="#e3f2fd" stroke="#1565c0"/>
    <text x="34" y="100" font-weight="700">2 · สร้างครั้งเดียว</text>
    <text x="150" y="100" text-anchor="middle">Label x6 + Bar</text>
    <text x="450" y="100" text-anchor="middle">Arc x2 + Seg7</text>
    <text x="750" y="100" text-anchor="middle">Panel + Label</text>
    <text x="34" y="116" fill="#888" font-size="10">widget ต่างชนิด แต่ "สร้างก่อนลูป" เหมือนกัน</text>
    <rect x="20" y="130" width="860" height="42" rx="8" fill="#fff3e0" stroke="#ef6c00"/>
    <text x="34" y="148" font-weight="700">3 · ลูป: อ่าน→คำนวณ→วาด</text>
    <text x="150" y="148" text-anchor="middle">motion()</text>
    <text x="450" y="148" text-anchor="middle">motion()+tilt()</text>
    <text x="750" y="148" text-anchor="middle">radar()</text>
    <text x="34" y="164" fill="#888" font-size="10">อ่านเซนเซอร์คนละตัว แต่รูปแบบ "อ่านแล้ววาด" เหมือนกัน</text>
    <rect x="20" y="178" width="860" height="42" rx="8" fill="#f3e5f5" stroke="#6a1b9a"/>
    <text x="34" y="196" font-weight="700">4 · ui.poll + back</text>
    <text x="150" y="196" text-anchor="middle">poll → back_id</text>
    <text x="450" y="196" text-anchor="middle">poll → back_id</text>
    <text x="750" y="196" text-anchor="middle">poll → back_id</text>
    <text x="34" y="212" fill="#888" font-size="10">ทั้งสามจบด้วยลูปรับปุ่ม + ปุ่ม back ที่ raise KeyboardInterrupt เหมือนกันทุกบรรทัด</text>
  </g>
</svg>
</div>

> พอเห็นโครงร่วม การอ่านโค้ดใหม่ๆ จะเร็วขึ้นมาก เพราะคุณรู้ว่า "จะหาอะไรตรงไหน" — ที่เหลือคือรายละเอียดของแต่ละแอป

---

# โครงร่วม 4 จังหวะ — ภาพรวม

จำภาพนี้ให้ขึ้นใจ โปรแกรม MicroPython บน BENTO เกือบทุกตัวเดินตามนี้ (เราเห็นผ่านๆ มาแล้วในบทเรียน 1.1–1.3 วันนี้แกะเต็ม):

<div style="text-align:center;margin:6px 0">
<svg width="880" height="150" viewBox="0 0 880 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arSk" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="40" width="190" height="60" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="115" y="64" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">1 · import</text>
  <text x="115" y="84" font-size="11" fill="#666" text-anchor="middle">ui · sensors · dsp · time</text>
  <rect x="238" y="40" width="200" height="60" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="338" y="64" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">2 · สร้างครั้งเดียว</text>
  <text x="338" y="84" font-size="11" fill="#666" text-anchor="middle">widget + ปุ่ม back</text>
  <rect x="466" y="40" width="190" height="60" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="561" y="64" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">3 · ลูป</text>
  <text x="561" y="84" font-size="11" fill="#666" text-anchor="middle">อ่าน → คำนวณ → วาด</text>
  <rect x="684" y="40" width="176" height="60" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="772" y="64" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">4 · ui.poll</text>
  <text x="772" y="84" font-size="11" fill="#666" text-anchor="middle">รับปุ่ม/แตะจอ</text>
  <line x1="210" y1="70" x2="236" y2="70" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <line x1="438" y1="70" x2="464" y2="70" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <line x1="656" y1="70" x2="682" y2="70" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <path d="M772,100 C772,128 561,128 561,102" fill="none" stroke="#9e9e9e" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arSk)"/>
  <text x="666" y="132" font-size="11" fill="#9e9e9e" text-anchor="middle">วนกลับ</text>
</svg>
</div>

- **จังหวะ 1–2 ทำครั้งเดียว** (ตอนเริ่ม) · **จังหวะ 3–4 วนซ้ำ** ตลอดจนกดออก
- ทุกอย่างในลูปมีแค่สองหน้าที่: **แก้ค่าของ widget** (จังหวะ 3) กับ **ฟังปุ่ม** (จังหวะ 4)

> เราจะไล่ทีละจังหวะในสไลด์ถัดไป จำไว้ว่าจังหวะ 1–2 คือ "ตั้งเวที" ทำหนเดียว ส่วน 3–4 คือ "การแสดง" ที่วนไม่หยุด

---

# จังหวะ 1 — import: หยิบเครื่องมือมาวางบนโต๊ะ

บรรทัดแรกๆ ของทุกไฟล์คือการบอกว่าเราจะใช้โมดูลอะไรบ้าง แต่ละตัวเปิดประตูสู่คนละความสามารถ:

```python
import ui
ui.screen()          # เคลียร์จอ + เตรียม canvas 792x398 (เรียกครั้งเดียว ทันทีหลัง import ui)
import lcd           # console ข้อความด้านล่างจอ (lcd.console / lcd.clear)
import sensors       # อ่านเซนเซอร์จริงบนบอร์ด (bmi270 / radar / ...)
import dsp           # ยกงานคณิต/ฟิสิกส์ให้ฝั่ง C (tilt / altitude / ...)
import time          # จังหวะเวลา (time.sleep_ms)
```

- `ui.screen()` เรียก **ทันทีหลัง `import ui`** เสมอ เพื่อเคลียร์จอและจองพื้นที่วาด — ถ้าลืม widget อาจไปวางทับหน้าเก่า
- `01/04` ไม่ได้ `import dsp` เพราะไม่ต้องคำนวณมุม ส่วน `02` และ remix ของเราต้องใช้ จึง import เพิ่ม

> import คือการประกาศ "ฉันจะใช้อะไรบ้าง" — อ่าน import ให้จบก่อน แล้วคุณจะเดาได้เลยว่าแอปนี้แตะเซนเซอร์ตัวไหน วาดจอด้วยอะไร

---

# จังหวะ 2 — สร้าง widget ครั้งเดียว

ก่อนเข้าลูป เราสร้าง widget ทุกตัวที่จะใช้ให้ครบ แล้วเก็บ "ตัวอ้างอิง" ไว้ในตัวแปร เพื่อจะไปแก้ค่าทีหลัง:

```python
ui.Label("Pitch", x=170, y=24, color=CYAN)          # ป้ายนิ่งๆ ไม่ต้องเก็บตัวแปร
arc_p = ui.Arc(x=100, y=54, min=-90, max=90, value=0)  # เก็บ arc_p ไว้แก้ค่าในลูป
seg   = ui.Seg7("0", x=330, y=104, color=GREEN)        # เก็บ seg ไว้เปลี่ยนตัวเลข
back  = ui.Button("< ออก", x=640, y=350, w=130, h=38)
back_id = back.id()                                    # จำ id ปุ่มไว้เทียบตอน poll
```

- widget ที่ต้อง **แก้ค่าในลูป** ต้องเก็บตัวแปรไว้ (`arc_p`, `seg`) · ป้ายที่วางแล้วนิ่งไม่ต้องเก็บ
- `back.id()` คืนเลขประจำปุ่ม เราเก็บเป็น `back_id` ไว้เทียบกับอีเวนต์ที่ `ui.poll()` ส่งกลับมา

> คิดภาพ widget เป็นป้ายที่ตอกติดผนังไว้แล้ว ในลูปเราแค่เดินไปเปลี่ยนตัวเลขบนป้าย — เราไม่รื้อป้ายเก่าแล้วตอกใหม่ทุกวินาที

---

# ทำไม "สร้างครั้งเดียว" ถึงสำคัญมาก

นี่เป็นกฎที่พลาดบ่อยและเจ็บจริง ถ้าเผลอสร้าง widget **ในลูป** จะเกิดสองปัญหาพร้อมกัน:

<div style="text-align:center;margin:6px 0">
<svg width="860" height="170" viewBox="0 0 860 170" font-family="DejaVu Sans, sans-serif">
  <rect x="20" y="16" width="400" height="140" rx="12" fill="#ffebee" stroke="#c62828" stroke-width="2"/>
  <text x="220" y="42" font-size="14" font-weight="700" fill="#c62828" text-anchor="middle">สร้างในลูป (ผิด)</text>
  <text x="40" y="70" font-size="12" fill="#555">while True:</text>
  <text x="60" y="90" font-size="12" fill="#c62828">seg = ui.Seg7(...)   # สร้างใหม่ทุกรอบ</text>
  <text x="40" y="118" font-size="12" fill="#555">- จอกระพริบ (วาดทับซ้ำๆ)</text>
  <text x="40" y="138" font-size="12" fill="#555">- widget กองสะสม → หน่วยความจำหมด → ค้าง</text>
  <rect x="440" y="16" width="400" height="140" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="640" y="42" font-size="14" font-weight="700" fill="#2e7d32" text-anchor="middle">สร้างก่อนลูป (ถูก)</text>
  <text x="460" y="70" font-size="12" fill="#555">seg = ui.Seg7(...)   # สร้างครั้งเดียว</text>
  <text x="460" y="90" font-size="12" fill="#555">while True:</text>
  <text x="480" y="110" font-size="12" fill="#2e7d32">seg.text("42")     # แค่แก้ค่า</text>
  <text x="460" y="138" font-size="12" fill="#555">- จอนิ่ง · หน่วยความจำคงที่ · ลื่น</text>
</svg>
</div>

- **จอกระพริบ** — สร้าง widget ใหม่ทับของเดิมทุกเฟรม ตาจะเห็นการกระพริบตลอด
- **หน่วยความจำรั่ว** — widget เก่าไม่ถูกลบ กองสะสมจนเต็ม แล้วโปรแกรมค้าง (บทเรียน 1.1–1.3 เราเตือนเรื่องนี้ไว้แล้ว)

> กฎง่ายๆ: **สิ่งที่ "เป็น" อยู่ สร้างก่อนลูป · สิ่งที่ "เปลี่ยน" ทำในลูป** — จำประโยคนี้ไว้ จะไม่พลาดเรื่อง widget อีกเลย

---

# จังหวะ 3 — ลูป: อ่าน → คำนวณ → วาด

หัวใจของทุกแอปอยู่ในลูป และในลูปมีจังหวะย่อยสามท่อนเสมอ **อ่านเซนเซอร์ → คำนวณ → วาดจอ**:

```python
while True:
    ax, ay, az, gx, gy, gz = sensors.bmi270.motion()   # (ก) อ่าน: ดึงค่าจากเซนเซอร์
    roll, pitch = dsp.tilt(ax, ay, az)                 # (ข) คำนวณ: แปลงเป็นมุม
    p = 0 if abs(pitch) < DEAD else int(pitch)         #     จัดค่าให้พร้อมโชว์
    if (p, r) != last:                                 # (ค) วาดเฉพาะตอนค่าเปลี่ยน
        arc_p.value(p)
        seg.text("%d" % ang)
        last = (p, r)
    ...
    time.sleep_ms(100)                                 # เว้นจังหวะ ไม่รัดจอจนกิน CPU
```

- **(ก) อ่าน** — คำสั่งเดียวได้ค่ามา · **(ข) คำนวณ** — แปลงค่าดิบเป็นสิ่งที่คนอ่านรู้เรื่อง · **(ค) วาด** — เอาขึ้นจอ
- `time.sleep_ms(100)` = ลูปวิ่ง ~10 ครั้ง/วินาที เร็วพอให้ลื่น แต่ไม่รัดจน CPU/IPC ทำงานหนักเปล่า

> เห็นโครง "อ่าน–คำนวณ–วาด" นี้ไหม? ทั้ง `01/02/04` และ remix ของเราใช้อันเดียวกันหมด ต่างแค่ "อ่านอะไร คำนวณอะไร วาดด้วย widget อะไร"

---

# จังหวะ 4 — ui.poll: ฟังปุ่มและการแตะจอ

จอ BENTO เป็นทัชสกรีน ทุกการกดปุ่ม/แตะจอจะถูกเก็บเป็น "อีเวนต์" เราดึงมาอ่านด้วย `ui.poll()` หนึ่งครั้งต่อรอบลูป:

<div style="text-align:center;margin:6px 0">
<svg width="880" height="170" viewBox="0 0 880 170" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arPo" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="50" width="150" height="64" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="95" y="78" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">แตะจอ/กดปุ่ม</text>
  <text x="95" y="98" font-size="11" fill="#666" text-anchor="middle">ผู้ใช้ทำ</text>
  <rect x="230" y="50" width="180" height="64" rx="10" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
  <text x="320" y="72" font-size="13" font-weight="700" fill="#455a64" text-anchor="middle">คิว (queue)</text>
  <text x="320" y="92" font-size="11" fill="#666" text-anchor="middle">อีเวนต์รอถูกอ่าน</text>
  <rect x="470" y="50" width="180" height="64" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="560" y="72" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">ui.poll()</text>
  <text x="560" y="92" font-size="11" fill="#666" text-anchor="middle">คืน list ของอีเวนต์</text>
  <rect x="710" y="50" width="150" height="64" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="785" y="72" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">เทียบ handle</text>
  <text x="785" y="92" font-size="11" fill="#666" text-anchor="middle">== back_id ?</text>
  <line x1="170" y1="82" x2="228" y2="82" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arPo)"/>
  <line x1="410" y1="82" x2="468" y2="82" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arPo)"/>
  <line x1="650" y1="82" x2="708" y2="82" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arPo)"/>
  <text x="440" y="140" font-size="11" fill="#888" text-anchor="middle">poll ครั้งเดียวต่อรอบลูป — ดึงอีเวนต์ที่คั่งค้างออกมาให้หมด แล้วค่อยวนต่อ</text>
</svg>
</div>

```python
for ev in ui.poll():                    # ดึงอีเวนต์ที่ค้างในคิวออกมาทีละตัว
    if ev.get('handle') == back_id:     # ใช่ปุ่ม back ที่เราจำ id ไว้ไหม
        raise KeyboardInterrupt
```

> `ui.poll()` เป็นแบบ **non-blocking** — ถ้าไม่มีใครกด มันคืน list ว่างแล้วลูปวิ่งต่อ ไม่ค้างรอ นี่คือเหตุผลที่จอยังอัปเดตค่าเซนเซอร์ได้ลื่นๆ พร้อมกับฟังปุ่มไปด้วย

---

# ปุ่ม back — ทางออกที่สุภาพของทุกแอป

ทุกแอปในคอร์สมีปุ่ม back ที่ทำงานเหมือนกัน และมันผูกกับวิธี "ออกจากลูปอย่างเรียบร้อย":

```python
try:
    while True:
        ...
        for ev in ui.poll():
            if ev.get('handle') == back_id:
                raise KeyboardInterrupt      # กด back = โยนสัญญาณออกจากลูป
        time.sleep_ms(100)
except KeyboardInterrupt:
    lcd.console('<span class=ok> จบการทำงาน</span>')   # เก็บกวาดตอนจบ
```

- กดปุ่ม back → `raise KeyboardInterrupt` → กระโดดออกจาก `while` ไปที่ `except` ทันที
- ที่ `except` (หรือ `finally`) เราทำการ **เก็บกวาด** — พิมพ์ข้อความจบ หรือหยุดเครื่องยนต์ (แบบที่บทเรียน 1.1–1.3 เรียก `edge_ai.stop()`)

> `raise` กลางลูปดูแรง แต่จริงๆ คือวิธี "ออกจากงานอย่างมีระเบียบ" — เราไม่ปล่อยให้โปรแกรมจบดื้อๆ แต่ให้มันวิ่งผ่าน `except` เพื่อเก็บของให้เรียบร้อยก่อน

---

# เทียบสามแอปด้วยโครงเดียว

พอมีโครงในหัวแล้ว ลองวางสามแอปลงตารางเดียว จะเห็นว่าต่างกันแค่ช่อง "อ่านอะไร / คำนวณอะไร / วาดด้วยอะไร":

| จังหวะ | `01` IMU 6-axis | `02` Tilt | `04` Radar |
|---|---|---|---|
| **1 import** | ui·sensors·time | + `dsp` | ui·sensors·time |
| **2 สร้างครั้งเดียว** | Label ×6 + Bar | Arc ×2 + Seg7 | Panel + Label |
| **3 อ่าน** | `bmi270.motion()` | `bmi270.motion()` | `sensors.radar()` |
| **3 คำนวณ** | `|a|` = √(ax²+ay²+az²) | `dsp.tilt(ax,ay,az)` | `bool(r["presence"])` |
| **3 วาด** | `label.text` + `bar.value` | `arc.value` + `seg.text` | `panel.color` + `state.text` |
| **4 poll + back** | เหมือนกันทุกบรรทัด | เหมือนกันทุกบรรทัด | เหมือนกันทุกบรรทัด |

- แถวล่างสุด (poll + back) **เหมือนกันเป๊ะ** ทั้งสามไฟล์ — นี่คือส่วนที่ copy ข้ามแอปได้เลย
- remix ของเราวันนี้ = หยิบช่อง "อ่าน" จาก `01`, ช่อง "คำนวณ" จาก `02`, ลูกเล่น "วาดเฉพาะตอนเปลี่ยน" จาก `04`

> ตารางนี้คือแผนที่ remix ของคุณ — อยากเปลี่ยนแอปให้อ่านเซนเซอร์อื่น ก็แค่สลับช่อง "อ่าน" กับ "คำนวณ" ส่วนโครงที่เหลือไม่ต้องแตะ

---

# รู้จักโมดูล sensors

`sensors` คือหน้าต่างเดียวที่เราอ่านค่าจริงจากฮาร์ดแวร์บนบอร์ด แต่ละเซนเซอร์มีฟังก์ชันของตัวเอง ชุดบทเรียนนี้เราใช้สองตัว:

| คำสั่ง | คืนค่า |
|---|---|
| `sensors.bmi270.motion()` | `(ax, ay, az, gx, gy, gz)` — accel 3 + gyro 3 อ่านพร้อมกัน |
| `sensors.bmi270.acceleration()` | `(ax, ay, az)` — เฉพาะ accel |
| `sensors.bmi270.chip_id()` | int — เลขรุ่นชิป (ใช้เช็กว่าต่อเซนเซอร์ติด) |
| `sensors.radar()` | `{'presence', 'energy'}` — มีคนไหม + พลังงานสะท้อน |
| `sensors.dps368.pressure_temperature()` | `(hPa, °C)` — ความดัน/อุณหภูมิ (ชุดบทเรียนหลัง ๆ) |
| `sensors.sht40.temperature_humidity()` | `(°C, %RH)` — อุณหภูมิ/ความชื้น (ชุดบทเรียนหลัง ๆ) |

- ชุดบทเรียนนี้โฟกัส **`bmi270.motion()`** (IMU) กับ **`radar()`** — สองตัวที่เราเพิ่งเห็นใน `01` และ `04`
- ตัว baro/humidity เก็บไว้เจอกันจริงใน โมดูล 2 (DAQ) ตอนนี้แค่รู้ว่ามี

> `motion()` อ่าน 6 แกน **ในครั้งเดียวใต้ bus lock เดียว** = ได้ค่าที่เวลาตรงกันทุกแกน ถ้าอ่านทีละแกนแยกกัน ค่าจะคนละเสี้ยววินาที เอามาคำนวณมุมจะเพี้ยน

---

# sensors.bmi270.motion() — อ่าน IMU 6 แกน

IMU (Inertial Measurement Unit) BMI270 วัดสองอย่าง: **ความเร่ง** (accelerometer) กับ **การหมุน** (gyroscope) อย่างละ 3 แกน:

```python
ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
# ax, ay, az = ความเร่ง 3 แกน หน่วย m/s2 (วางนิ่งแกนที่ตั้งฉากพื้นจะได้ ~9.8 จากแรงโน้มถ่วง)
# gx, gy, gz = ความเร็วเชิงมุม 3 แกน หน่วย dps (องศา/วินาที) — บอกว่าบอร์ดกำลังหมุนเร็วแค่ไหน
```

- **accelerometer** จับแรงโน้มถ่วง → เอามาหา "บอร์ดเอียงกี่องศา" ได้ (นี่คือที่มาของ `dsp.tilt`)
- **gyroscope** จับการหมุน → เอามาจับ "กำลังหมุน/เขย่า" ได้
- วางบอร์ดนิ่งราบ: `az ≈ 9.8`, ที่เหลือ ≈ 0 · เอียงบอร์ด: แรงโน้มถ่วงกระจายไป ax/ay ด้วย

> ชุดบทเรียนนี้ remix ของเราใช้แค่ 3 แกน accel (ax, ay, az) เพื่อคำนวณมุมเอียง ส่วน gyro เราอ่านมาเก็บไว้เฉยๆ เผื่อคุณอยากต่อยอด (เช่น จับการหมุนเร็ว)

---

# คณิตเบื้องหลัง — ขนาดของเวกเตอร์ความเร่ง

ใน `01` มีบรรทัด `mag = (ax*ax + ay*ay + az*az) ** 0.5` นั่นคือการหา **ขนาด (magnitude)** ของเวกเตอร์ความเร่ง 3 แกน รวมเป็นตัวเลขเดียว:

$$ |a| \;=\; \sqrt{a_x^{2} + a_y^{2} + a_z^{2}} $$

อ่านทีละสัญลักษณ์แบบง่ายๆ:

- $a_x, a_y, a_z$ — ความเร่งของแต่ละแกน หน่วย **m/s²** (ค่าที่ `bmi270.motion()` คืนมา 3 ตัวแรก)
- ยกกำลังสองทุกแกน ($a_x^2$ …) เพื่อให้ค่าลบกลายเป็นบวก (ทิศทางไม่สำคัญ เราสนแค่ "แรงรวมเท่าไร")
- บวกกันแล้ว **ถอดรากที่สอง** $\sqrt{\;}$ — ได้ความยาวของลูกศรความเร่งในปริภูมิ 3 มิติ (ทฤษฎีบทพีทาโกรัสในสามมิติ)

<div style="text-align:center;margin:8px 0">
<svg width="560" height="180" viewBox="0 0 560 180" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arMag" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#c62828"/></marker>
    <marker id="arAx" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="8" refX="8" refY="3.5" orient="auto"><path d="M0,0 L8,3.5 L0,7 Z" fill="#607d8b"/></marker>
  </defs>
  <line x1="60" y1="140" x2="240" y2="140" stroke="#607d8b" stroke-width="2" marker-end="url(#arAx)"/>
  <text x="250" y="145" font-size="12" fill="#607d8b">aₓ</text>
  <line x1="60" y1="140" x2="60" y2="30" stroke="#607d8b" stroke-width="2" marker-end="url(#arAx)"/>
  <text x="42" y="26" font-size="12" fill="#607d8b">a_z</text>
  <line x1="60" y1="140" x2="150" y2="90" stroke="#607d8b" stroke-width="2" marker-end="url(#arAx)"/>
  <text x="150" y="82" font-size="12" fill="#607d8b">a_y</text>
  <line x1="60" y1="140" x2="235" y2="55" stroke="#c62828" stroke-width="3" marker-end="url(#arMag)"/>
  <text x="250" y="52" font-size="14" font-weight="700" fill="#c62828">|a|</text>
  <text x="330" y="90" font-size="13" fill="#455a64">วางนิ่งราบ → |a| ≈ 9.8 m/s²</text>
  <text x="330" y="112" font-size="13" fill="#455a64">(แรงโน้มถ่วงล้วน)</text>
  <text x="330" y="140" font-size="13" fill="#455a64">เขย่าแรง → |a| พุ่งสูงกว่า 9.8</text>
</svg>
</div>

**ทำไมมันสำคัญกับชุดบทเรียนนี้:** `01` เอา `|a|` ไปป้อน `mag_bar` — วางบอร์ดนิ่งแท่งจะอยู่ราว 9.8 (จาก $\sqrt{0^2+0^2+9.8^2}$) พอเขย่าเลขจะพุ่งขึ้น นี่คือวิธี "ยุบ 3 แกนเป็นค่าเดียว" ที่ดูการเคลื่อนไหวรวมได้ในแท่งเดียว โดยไม่ต้องจ้องทั้งสามตัวเลขพร้อมกัน

> สังเกตว่าโค้ดเขียน `** 0.5` แทน `sqrt` — ยกกำลัง 0.5 คือรากที่สองพอดี (ทั้งคู่ให้ผลเท่ากัน) เป็นเหตุผลว่าทำไมคณิตนิดเดียวถึงแปลงเป็นโค้ดบรรทัดเดียวได้เลย

---

# sensors.radar() — ตรวจการมีคนโดยไม่ใช้กล้อง

เรดาร์ 60 GHz ยิงคลื่นออกไปแล้ววัดคลื่นสะท้อน ตรวจได้ว่ามีสิ่งเคลื่อนไหวอยู่หน้าบอร์ดไหม โดย **ไม่ต้องใช้กล้อง**:

```python
r = sensors.radar()
# r = {'presence': 1, 'energy': 1234.0}
now = bool(r["presence"])       # True = พบการเคลื่อนไหว
e   = r["energy"]               # พลังงานสะท้อน (มากขึ้นเมื่อวัตถุใกล้/ใหญ่)
```

- `'presence'` — เฟิร์มแวร์ตัดสินให้แล้วว่า "มีคน/ไม่มี" (1 หรือ 0) เราเอาไป `bool()` ต่อได้เลย
- `'energy'` — ค่าดิบของพลังงานสะท้อน ใช้ดูแนวโน้ม (ใกล้เข้ามา energy สูงขึ้น)
- `radar()` คุยข้ามคอร์ไป CM55 เหมือน `edge_ai` — ถ้า timeout จะโยน `OSError` (ในงานจริงควรห่อ try)

> เรดาร์เด่นตรงที่ทำงานในที่มืด ผ่านวัสดุบางอย่างได้ และไม่บันทึกภาพ = เป็นส่วนตัวกว่ากล้อง เหมาะกับสวิตช์ไฟอัตโนมัติ ป้ายอัจฉริยะ ที่ไม่อยากให้มีกล้องจ้อง

---

# dsp.tilt() — ยกงานคณิตให้ฝั่ง C ทำ

จาก accel 3 แกนดิบ เราอยากได้ "บอร์ดเอียงกี่องศา" การคำนวณนี้ใช้ตรีโกณ (`atan2`) ซึ่งถ้าเขียนใน MicroPython จะช้า `dsp` จึงยกไปคำนวณฝั่ง **C** ให้:

```python
import dsp
roll, pitch = dsp.tilt(ax, ay, az)    # คืน (roll, pitch) หน่วยองศา
# roll  = เอียงซ้าย-ขวา (หมุนรอบแกนหน้า-หลัง)
# pitch = เอียงหน้า-หลัง (ก้ม-เงย)
```

- `dsp.tilt` รับ accel 3 แกน คืนมุมสองค่าเป็น **องศา** พร้อมใช้ ไม่ต้องแปลงเรเดียนเอง
- เขียนเองก็ได้ (`math.atan2`) แต่ `dsp` เร็วกว่าเพราะรันบน C — บทเรียน Processing (บทเรียน 3.1–3.2+) เราจะแกะข้างในว่ามันทำอะไร
- โมดูล `dsp` ยังมี `dsp.altitude(p)`, `dsp.compass(mx,my,mz)`, `dsp.dew_point(t,rh)` ฯลฯ ไว้ใช้ชุดบทเรียนหลัง ๆ

> นี่คือแนวคิดสำคัญ: **งานคณิตหนักๆ ยกให้ C ทำ** MicroPython เก่งเรื่องเรียบเรียง logic + คุมจอ ส่วนเลขเยอะๆ ให้ฝั่ง C ที่เร็วกว่าจัดการ เราแค่เรียกใช้ผลลัพธ์

---

# วาดจอเฉพาะตอนค่าเปลี่ยน (event-driven)

บทเรียนสำคัญจาก `04`: **อย่าวาดจอทุกเฟรม วาดเฉพาะตอนค่าเปลี่ยนจริง** ทำให้จอนิ่ง สายตาไม่ล้า และ IPC ไม่รก

```python
last = (999, 999)                       # ค่าที่วาดครั้งก่อน (ตั้งเป็นค่าที่เป็นไปไม่ได้)
while True:
    ...
    if (p, r) != last:                  # เปลี่ยนจากครั้งก่อนไหม
        arc_p.value(p); arc_r.value(r)  # เปลี่ยน → วาดใหม่
        last = (p, r)                   # จำค่าล่าสุดไว้เทียบรอบหน้า
    # ไม่เปลี่ยน → ข้าม ไม่แตะจอเลย
```

- เก็บ "ค่าที่วาดล่าสุด" ไว้ในตัวแปร (`last`, `was`, `last_seq`) แล้วเทียบก่อนวาด
- ในบทเรียน 1.1–1.3 เราเจอลายเดียวกันในชื่อ `last_seq` — เช็ก `seq` ก่อนวาดผลอนุมานใหม่
- deadzone (`DEAD = 2.0`) ช่วยอีกชั้น: มุมสั่นเล็กๆ ใกล้ 0 ปัดเป็น 0 เข็มจะได้ไม่กระตุก

> "วาดเฉพาะตอนเปลี่ยน" เป็นนิสัยที่ดีของงาน embedded — จอที่กระพริบตลอดไม่ใช่แค่กวนตา แต่เปลืองพลังและทำให้ช่องสื่อสารข้ามคอร์ (IPC) แน่นโดยไม่จำเป็น

---

# PRIMM — วิธีคิดของชุดบทเรียนนี้

เราทำตามลำดับ **PRIMM** ที่เกริ่นในบทเรียน 1.1–1.3 แต่ชุดบทเรียนนี้เน้นสอง P กลาง (Investigate + Modify) เป็นพิเศษ:

<div style="text-align:center;margin:6px 0">
<svg width="900" height="140" viewBox="0 0 900 140" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arPr" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="44" width="150" height="56" rx="10" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
  <text x="89" y="68" font-size="13" font-weight="700" fill="#455a64" text-anchor="middle">Predict</text>
  <text x="89" y="88" font-size="10" fill="#888" text-anchor="middle">เดาว่าโค้ดทำอะไร</text>
  <rect x="184" y="44" width="150" height="56" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="259" y="68" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">Run</text>
  <text x="259" y="88" font-size="10" fill="#888" text-anchor="middle">รันดูว่าจริงไหม</text>
  <rect x="354" y="40" width="160" height="64" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="3"/>
  <text x="434" y="66" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">Investigate</text>
  <text x="434" y="88" font-size="10" fill="#1565c0" text-anchor="middle">แกะโครง 4 จังหวะ</text>
  <rect x="534" y="40" width="160" height="64" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="3"/>
  <text x="614" y="66" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">Modify</text>
  <text x="614" y="88" font-size="10" fill="#e65100" text-anchor="middle">remix ของเรา</text>
  <rect x="714" y="44" width="150" height="56" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="789" y="68" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">Make</text>
  <text x="789" y="88" font-size="10" fill="#888" text-anchor="middle">สร้างเอง (ชุดบทเรียนหลัง)</text>
  <line x1="164" y1="72" x2="182" y2="72" stroke="#607d8b" stroke-width="2" marker-end="url(#arPr)"/>
  <line x1="334" y1="72" x2="352" y2="72" stroke="#607d8b" stroke-width="2" marker-end="url(#arPr)"/>
  <line x1="514" y1="72" x2="532" y2="72" stroke="#607d8b" stroke-width="2" marker-end="url(#arPr)"/>
  <line x1="694" y1="72" x2="712" y2="72" stroke="#607d8b" stroke-width="2" marker-end="url(#arPr)"/>
</svg>
</div>

- **Investigate** — แกะโครง 4 จังหวะที่เพิ่งไล่ไป · ถามตัวเองว่า "บรรทัดนี้อยู่จังหวะไหน ทำหน้าที่อะไร"
- **Modify** — แก้ทีละนิดแล้วดูผล นี่ปลอดภัยและเรียนรู้เร็วกว่าเขียนใหม่ทั้งไฟล์
- **Make** (เขียนของใหม่จากศูนย์) เก็บไว้ โมดูล 2 (DAQ) เป็นต้นไป ตอนที่โครงติดมือแล้ว

> อ่านโค้ดแล้วรันดู แล้วค่อยแก้ทีละบรรทัด — สามก้าวนี้คือวิธีที่วิศวกรจริงเรียนของใหม่ ไม่ใช่นั่งท่องไวยากรณ์ให้ครบก่อนแตะโค้ด
