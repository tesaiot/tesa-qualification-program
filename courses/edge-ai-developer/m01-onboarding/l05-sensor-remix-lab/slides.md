---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 1.5 — ลงมือทำ: remix เป็น Tilt Monitor ของเรา"
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

# บทเรียน 1.5 — ลงมือทำ: remix เป็น Tilt Monitor ของเรา

## แกะแอปเซนเซอร์ทีละส่วน · โครงร่วมของทุกโปรแกรม แล้ว remix เป็นของเรา

**โมดูล 1 — เริ่มต้น: รันของจริงแล้วแกะดูข้างใน**

> ต่อจากบทเรียน 1.4 — แกะแอปเซนเซอร์: โครงร่วมสี่จังหวะของทุกโปรแกรม

---

# โจทย์ remix ของเรา — Tilt Monitor

วันนี้เราจะ remix สามตัวอย่างเป็นแอปเดียว: **Tilt Monitor** — เอียงบอร์ดแล้วเห็นมุมสองแกน + ป้ายเตือนเมื่อเอียงเกินเกณฑ์

<div style="text-align:center;margin:8px 0">
<svg width="820" height="150" viewBox="0 0 820 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arRx" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="30" width="200" height="44" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="114" y="50" font-size="12" font-weight="700" fill="#1565c0" text-anchor="middle">อ่าน จาก 01</text>
  <text x="114" y="66" font-size="10" fill="#666" text-anchor="middle">bmi270.motion()</text>
  <rect x="14" y="90" width="200" height="44" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="114" y="110" font-size="12" font-weight="700" fill="#2e7d32" text-anchor="middle">คำนวณ จาก 02</text>
  <text x="114" y="126" font-size="10" fill="#666" text-anchor="middle">dsp.tilt()</text>
  <rect x="304" y="60" width="220" height="44" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="414" y="80" font-size="12" font-weight="700" fill="#e65100" text-anchor="middle">วาด เฉพาะตอนเปลี่ยน จาก 04</text>
  <text x="414" y="96" font-size="10" fill="#666" text-anchor="middle">Arc + Seg7 + Panel เปลี่ยนสี</text>
  <rect x="610" y="60" width="196" height="44" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="708" y="80" font-size="12" font-weight="700" fill="#6a1b9a" text-anchor="middle">s02_anatomy_sensor.py</text>
  <text x="708" y="96" font-size="10" fill="#666" text-anchor="middle">remix ของเรา</text>
  <line x1="214" y1="52" x2="302" y2="74" stroke="#607d8b" stroke-width="2" marker-end="url(#arRx)"/>
  <line x1="214" y1="112" x2="302" y2="92" stroke="#607d8b" stroke-width="2" marker-end="url(#arRx)"/>
  <line x1="524" y1="82" x2="608" y2="82" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arRx)"/>
</svg>
</div>

- เกจ **Arc คู่** (pitch/roll) + **Seg7** โชว์มุมเด่น (ยกจาก `02`)
- **ป้ายสถานะ** LEVEL/TILTED เปลี่ยนสีเมื่อเอียงเกิน `TILT_LIMIT` (ลูกเล่น event-driven จาก `04`)

> นี่คือ remix ที่ "ต่างจากต้นฉบับจริงๆ" — ไม่ใช่แค่ copy `02` มา แต่เอาสามแอปมาผสมเป็นของใหม่ที่ทำงานได้ นี่แหละคือ MVP ของชุดบทเรียนนี้

---

# โครงของไฟล์ s02_anatomy_sensor.py

ทั้งไฟล์อ่านเป็นประโยคเดียว: **"อ่าน IMU → แปลงเป็นมุม → โชว์เข็มกับมุมเด่น → เตือนเมื่อเอียงเกิน → ฟังปุ่ม back"**

<div style="text-align:center;margin:6px 0">
<svg width="920" height="200" viewBox="0 0 920 200" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arS2" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g font-size="13" text-anchor="middle">
    <rect x="14" y="30" width="165" height="54" rx="10" fill="#cfd8dc" stroke="#607d8b" stroke-width="2"/>
    <text x="96" y="53" font-weight="700" fill="#455a64">อ่าน IMU</text>
    <text x="96" y="72" font-size="11" fill="#999">motion() :62</text>
    <rect x="219" y="30" width="165" height="54" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="301" y="53" font-weight="700" fill="#2e7d32">คำนวณมุม</text>
    <text x="301" y="72" font-size="11" fill="#999">dsp.tilt :67</text>
    <rect x="424" y="30" width="165" height="54" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="506" y="53" font-weight="700" fill="#e65100">โชว์มุมเด่น</text>
    <text x="506" y="72" font-size="11" fill="#999">seg.text :76</text>
    <rect x="629" y="30" width="165" height="54" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="711" y="49" font-weight="700" fill="#1565c0">เตือนเมื่อเอียง</text>
    <text x="711" y="68" font-size="11" fill="#999">panel.color</text>
    <text x="711" y="80" font-size="10" fill="#999">(event-driven)</text>
    <rect x="380" y="128" width="180" height="54" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
    <text x="470" y="151" font-weight="700" fill="#6a1b9a">ui.poll + back</text>
    <text x="470" y="170" font-size="11" fill="#999">:96 → KeyboardInterrupt</text>
  </g>
  <line x1="179" y1="57" x2="217" y2="57" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS2)"/>
  <line x1="384" y1="57" x2="422" y2="57" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS2)"/>
  <line x1="589" y1="57" x2="627" y2="57" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS2)"/>
  <path d="M711,84 C711,120 560,120 505,126" fill="none" stroke="#9e9e9e" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arS2)"/>
  <path d="M380,155 C200,155 96,120 96,86" fill="none" stroke="#2e7d32" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arS2)"/>
  <text x="250" y="120" font-size="11" fill="#2e7d32">วนกลับทุก 100 ms</text>
</svg>
</div>

> ตัวเลขบรรทัด (`:62`, `:67`, `:76`, `:96`) ชี้จุดที่ต้องเติมโค้ดในไฟล์ฝึก — จำโครงนี้ไว้ เดี๋ยวไล่ทีละช่อง

---

# ไล่โค้ด (1) — import + สร้าง widget ครั้งเดียว

ส่วนหัวของไฟล์ (จังหวะ 1–2) ให้ไว้ครบแล้ว อ่านให้เข้าใจว่าสร้างอะไรไว้บ้าง:

```python
import ui
ui.screen()
import lcd, sensors, dsp, time

DEAD = 2.0          # deadzone กันเข็มสั่น
TILT_LIMIT = 20     # เกินนี้ = "เอียง"

arc_p = ui.Arc(x=100, y=54, min=-90, max=90, value=0)   # เกจ pitch
arc_r = ui.Arc(x=490, y=54, min=-90, max=90, value=0)   # เกจ roll
seg   = ui.Seg7("0", x=330, y=104, color=GREEN)          # มุมเด่น
panel = ui.Panel(x=250, y=205, w=290, h=64, color=0x115511)
state = ui.Label("LEVEL", x=350, y=228, color=0xFFFFFF)
back  = ui.Button("< ออก", x=640, y=350, w=130, h=38); back_id = back.id()
```

- widget ที่ต้องแก้ค่าในลูปถูกเก็บตัวแปรไว้: `arc_p`, `arc_r`, `seg`, `panel`, `state`
- `DEAD` กับ `TILT_LIMIT` เป็นค่าคงที่ที่ควบคุมพฤติกรรม — remix ง่ายๆ คือลองเปลี่ยนสองค่านี้

> อ่านหัวไฟล์ให้ครบก่อนเข้าลูป จะได้รู้ว่ามี widget อะไรให้เล่นบ้าง ค่าคงที่ตัวไหนคุมอะไร — เหมือนดูรายชื่อเครื่องมือก่อนลงมือ

---

# ไล่โค้ด (2) — อ่านเซนเซอร์ + คำนวณมุม

**ช่องเติมที่ 1 และ 2**: ต้นลูป อ่าน IMU แล้วแปลงเป็นมุม (จังหวะ 3 ท่อน อ่าน + คำนวณ):

```python
while True:
    # เติม: อ่านค่า 6 แกนจาก IMU  ->  ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
    ax = ay = az = gx = gy = gz = 0
    pass

    # เติม: แปลงเป็นมุมเอียง  ->  roll, pitch = dsp.tilt(ax, ay, az)
    roll, pitch = 0.0, 0.0
    pass
```

- ช่อง 1: แทน `pass` ด้วย `ax, ay, az, gx, gy, gz = sensors.bmi270.motion()` (ลบบรรทัด `ax = ay = ...` ทิ้งได้)
- ช่อง 2: แทน `pass` ด้วย `roll, pitch = dsp.tilt(ax, ay, az)`
- ถ้าลืมเติมช่อง 1: `ax,ay,az` ค้างเป็น 0 → `dsp.tilt` ได้มุม 0 เสมอ เข็มไม่ขยับ (นี่คือเบาะแสตอน debug)

> สังเกตว่า remix ใช้ `motion()` เหมือน `01` เป๊ะ แต่เอาผลไปป้อน `dsp.tilt` เหมือน `02` — คุณกำลัง "ผสม" สองแอปด้วยมือตัวเอง

---

# ไล่โค้ด (3) — โชว์มุมเด่น + เตือนเมื่อเอียง

**ช่องเติมที่ 3**: วาดมุมเด่นขึ้น Seg7 (จังหวะ 3 ท่อน วาด) ส่วน event-driven ให้ไว้แล้วเป็นตัวอย่าง:

```python
if (p, r) != last:                     # วาดเฉพาะตอนมุมเปลี่ยน (บทเรียนจาก 04)
    arc_p.value(p); arc_r.value(r)
    ang = p if abs(p) >= abs(r) else r  # แกนที่เอียงมากสุด
    # เติม: โชว์มุมเด่นบน Seg7  ->  seg.text("%d" % ang)
    pass
    last = (p, r)
    tilted = abs(ang) >= TILT_LIMIT     # ให้ไว้แล้ว: เปลี่ยนสีเฉพาะตอนข้ามเกณฑ์
    if tilted != was_tilted:
        panel.color(0x881111 if tilted else 0x115511)
        state.text("TILTED" if tilted else "LEVEL")
        was_tilted = tilted
```

- ช่อง 3: แทน `pass` ด้วย `seg.text("%d" % ang)` — เอามุมเด่นขึ้นจอตัวใหญ่
- ส่วน `tilted != was_tilted` ให้ไว้แล้ว เป็นตัวอย่างลาย event-driven ที่ยกจาก `04` (อ่านให้เข้าใจ)

> เห็นการซ้อนสองชั้นของ "วาดเฉพาะตอนเปลี่ยน" ไหม — ชั้นนอกเช็กมุมเปลี่ยน ชั้นในเช็กสถานะ (เอียง/ราบ) เปลี่ยน ทั้งคู่เพื่อไม่แตะจอเกินจำเป็น

---

# ไล่โค้ด (4) — ui.poll + ปุ่ม back

**ช่องเติมที่ 4**: ท้ายลูป ฟังปุ่ม back (จังหวะ 4) แล้วออกอย่างเรียบร้อย:

```python
    for ev in ui.poll():
        if ev.get('handle') == back_id:
            # เติม: ออกจากลูปตอนกดปุ่ม back  ->  raise KeyboardInterrupt
            pass
    time.sleep_ms(100)
except KeyboardInterrupt:
    lcd.console('<span class=ok> จบการทำงาน</span>')   # ให้ไว้แล้ว: เก็บกวาดตอนจบ
```

- ช่อง 4: แทน `pass` ด้วย `raise KeyboardInterrupt` — โยนสัญญาณออกจากลูปไปที่ `except`
- ถ้าลืมเติม: กดปุ่ม back แล้วโปรแกรมไม่ออก ค้างวนอยู่ในลูปต่อไป (ทดสอบดูได้)

> โครงนี้เหมือน `01/02/04` ทุกบรรทัด — พอเติมครบ คุณจะเห็นว่า "ส่วนรับปุ่ม" ของทุกแอปในคอร์สหน้าตาเดียวกันเป๊ะ copy ข้ามไฟล์ได้เลย

---

# หน้าตาบนจอ — รันได้จริงทั้งบน Emulator และบอร์ด

ก่อนลงมือ ดูปลายทางกันก่อนว่าเติมครบแล้วจอจะออกมาหน้าตาแบบไหน — เข็มมุมสองแกน ตัวเลขมุมเด่นตัวใหญ่ และป้ายสถานะที่เปลี่ยนสีเมื่อเอียงเกินเกณฑ์:

<div style="text-align:center;margin:2px 0;color:#555;font-size:.9em">รันบน BENTO Emulator ได้ด้วยโค้ดชุดเดียวกันกับที่ Program to Device ลงบอร์ด</div>

> ไม่ต้องมีบอร์ดอยู่ในมือก็ฝึกได้ — กด Run บน Emulator เห็นผลทันทีในเบราว์เซอร์ พอมั่นใจแล้วค่อยกด Program to Device โค้ดไม่ต้องแก้แม้แต่บรรทัดเดียว

---

# ลงมือทำ — เติมช่องว่างทั้ง 4 จุด

เปิด [`s02_anatomy_sensor.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l05-sensor-remix-lab/practice/s02_anatomy_sensor.py) ในไฟล์มี `pass` วางไว้ **4 จุด** ตรงหัวใจของโครงร่วม:

| # | จุด (จังหวะ) | เติมด้วย | ถ้าลืม |
|---|---|---|---|
| 1 | ต้นลูป (อ่าน) | `ax, ay, az, gx, gy, gz = sensors.bmi270.motion()` | เข็มไม่ขยับเลย |
| 2 | ต้นลูป (คำนวณ) | `roll, pitch = dsp.tilt(ax, ay, az)` | มุมเป็น 0 ตลอด |
| 3 | มีค่าใหม่ (วาด) | `seg.text("%d" % ang)` | เข็มขยับ แต่ตัวเลขใหญ่ไม่เปลี่ยน |
| 4 | ปุ่ม back (poll) | `raise KeyboardInterrupt` | กด back แล้วไม่ออก |

ขั้นตอน:

1. ไล่หา `# เติม:` ทีละจุด แล้วแทน `pass` ด้วยคำสั่งตามคำใบ้
2. กด **Run** (Emulator) หรือ **Program to Device** (บอร์ด)
3. เอียงบอร์ดช้าๆ ดูเข็มขยับ + มุมเด่นขึ้น Seg7 + ป้ายเปลี่ยนสีเมื่อเอียงเกิน 20 องศา

> สี่ช่องนี้คือหัวใจของโครงร่วม 4 จังหวะเป๊ะ — เติมครบเมื่อไร คุณ remix สามแอปเป็นของตัวเองสำเร็จ

---

# remix ต่อ — swap sensor / change display / break-and-fix

เติมครบแล้วยังไม่จบ ลอง **แก้ของ** ดูสามแนว นี่คือหัวใจของ Modify ใน PRIMM:

- **สลับเซนเซอร์ (swap sensor)** — เปลี่ยนช่อง "อ่าน" จาก `bmi270.motion()` เป็น `sensors.radar()` แล้วโชว์ presence/energy แทนมุม (โครง 4 จังหวะไม่ต้องแตะ)
- **เปลี่ยนการแสดงผล (change display)** — ลองเปลี่ยน `Seg7` เป็น `Bar` หรือเพิ่มแถบ energy · เปลี่ยนสี · เปลี่ยน `TILT_LIMIT` เป็น 10 แล้วดูว่าป้ายไวขึ้นไหม
- **ลองพังแล้วซ่อม (break-and-fix)** — จงใจย้าย `arc_p = ui.Arc(...)` เข้าไป **ในลูป** แล้วดูจอกระพริบ/ค้าง จากนั้นย้ายกลับออกมา — เข้าใจกฎ "สร้างครั้งเดียว" ด้วยตาตัวเอง

> break-and-fix เป็นวิธีเรียนที่ทรงพลัง: จงใจทำให้พังในที่ที่ควบคุมได้ แล้วซ่อม คุณจะจำบทเรียนนั้นแม่นกว่าอ่านเฉยๆ สิบเท่า — แต่จำค่าที่แก้ไว้ เพื่อย้อนกลับได้เสมอ

---

# แหล่งเรียนรู้เพิ่มเติม — เจาะลึกเรื่อง accelerometer / IMU

อยากเข้าใจว่าชิป IMU วัดความเร่งได้อย่างไร และทำไมแรงโน้มถ่วงถึงกลายเป็นมุมเอียงได้ ลองดูสามคลิปนี้:

**วิดีโอ**

- How does an accelerometer work? (MEMS ข้างในชิป) — ช่อง Real Engineering: https://www.youtube.com/@RealEngineering
- Accelerometer & Gyroscope (IMU) explained — ช่อง Sentdex: https://www.youtube.com/@sentdex
- Vectors and dot products (ทำความเข้าใจ magnitude/เวกเตอร์) — ช่อง 3Blue1Brown: https://www.youtube.com/@3blue1brown

**ภาพ / อ้างอิงเปิด**

- แผนภาพหลักการ MEMS accelerometer — (ที่มา: Wikimedia Commons — en.wikipedia.org/wiki/Accelerometer, CC BY-SA)
- บทความพื้นฐาน Inertial Measurement Unit — (ที่มา: en.wikipedia.org/wiki/Inertial_measurement_unit, Wikipedia CC BY-SA)

> วิดีโอ/ภาพภายนอกเป็นของเจ้าของต้นฉบับ ใช้เพื่อการศึกษา อ้างอิงลิงก์ต้นทาง — เราเปิดดูผ่านลิงก์ ไม่ได้ฝังหรือดาวน์โหลดมาเผยแพร่ซ้ำ

---

# ชัยชนะที่เห็นได้ + MVP ของชุดบทเรียนนี้

<div style="text-align:center;margin:14px 0">
<div style="display:inline-block;background:#e8f5e9;border:2px solid #2e7d32;border-radius:22px;padding:10px 22px;color:#2e7d32;font-weight:700;font-size:1.05em">
ชัยชนะที่เห็นได้ของชุดบทเรียนนี้ · remix สามแอปเป็น Tilt Monitor ที่ทำงานได้ เอียงบอร์ดแล้วเข็มขยับ มุมขึ้นจอ ป้ายเปลี่ยนสี
</div>
</div>

**MVP ของบทเรียน 1.4–1.5 (เกณฑ์ผ่านของชุดบทเรียน):** คุณทำ remix ที่ **ต่างจากต้นฉบับจริง** แล้ว **อธิบายแต่ละส่วนได้** — ชี้ได้ว่าบรรทัดไหนอยู่จังหวะไหน (import / สร้างครั้งเดียว / ลูป / poll) และแต่ละคำสั่ง `sensors.*` / `dsp.tilt` ทำอะไร

- ทำบน **Emulator** หรือ **บอร์ดจริง** ก็ได้ (โค้ดชุดเดียวกัน)
- remix ต้องมีอย่างน้อยหนึ่งอย่างที่ต่างจาก `01/02/04`: สลับเซนเซอร์ หรือเปลี่ยนการแสดงผลอย่างมีเหตุผล

> "อธิบายแต่ละส่วนได้" คือหัวใจ — remix ที่รันได้แต่เจ้าของอธิบายไม่ได้ ยังไม่ผ่าน เพราะเป้าหมายของชุดบทเรียนนี้คือ "อ่านออก" ไม่ใช่แค่ "ลอกให้รัน"

---

# บันไดช่วยเหลือ — ใบ้ → เริ่มจากโครง → เฉลย → ฉบับเต็ม

ถ้าติด ให้ไต่บันไดนี้ทีละขั้น อย่าเพิ่งกระโดดไปดูเฉลย เพราะของจะเข้าหัวตอนที่คุณพยายามเองก่อน:

- **ใบ้** — คำใบ้อยู่ในคอมเมนต์ `# เติม:` ทั้ง 4 จุดในไฟล์ฝึก + ตารางหน้าที่แล้ว บอกว่าแต่ละช่องเติมอะไร
- **เริ่มจากโครง** — [`s02_anatomy_sensor.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l05-sensor-remix-lab/practice/s02_anatomy_sensor.py) มีโครง 4 จังหวะครบทั้งไฟล์แล้ว เหลือแค่ 4 บรรทัดให้เติม
- **เฉลย** — [`s02_anatomy_sensor.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l05-sensor-remix-lab/solution/s02_anatomy_sensor.py) เติมครบพร้อมคอมเมนต์อธิบายทุกช่อง (อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์เอง)
- **ฉบับเต็ม** — [`s02_anatomy_sensor_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l05-sensor-remix-lab/examples/s02_anatomy_sensor_full.py) ฉบับขัดเรียบร้อย เพิ่มแถบ `|a|`, จำมุม peak, ปุ่ม Reset

> ลองเขียนเองให้สุดก่อนนะ ถ้าติดจริงๆ ค่อยเปิดเฉลยดูทีละช่อง แล้วกลับมาพิมพ์เอง — เดี๋ยวเราค่อย ๆ แกะไปด้วยกัน

---

# เชื่อมโยงรากฐาน — วันนี้เราแตะอะไรไปบ้าง

การ remix แอปเซนเซอร์ทำให้เราจับแนวคิดที่จะใช้ไปตลอดคอร์สได้ครบชุด:

**ฝั่งโครงโปรแกรม (ใช้ทุกบทเรียนต่อจากนี้)**
- **โครงร่วม 4 จังหวะ** — import → สร้างครั้งเดียว → ลูป → `ui.poll` เจอซ้ำในทุกแอป
- **สร้าง widget ครั้งเดียว** — สิ่งที่ "เป็น" สร้างก่อนลูป สิ่งที่ "เปลี่ยน" ทำในลูป
- **วาดเฉพาะตอนเปลี่ยน (event-driven)** — เก็บค่าล่าสุดไว้เทียบ จอนิ่ง IPC ไม่รก
- **ปุ่ม back + เก็บกวาด** — `raise KeyboardInterrupt` → `except` ออกอย่างมีระเบียบ

**ฝั่งเซนเซอร์ / สัญญาณ**
- **`sensors.*`** — อ่านค่าจริงจากฮาร์ดแวร์ (`bmi270.motion()`, `radar()`)
- **`dsp.tilt`** — ยกงานคณิตหนักให้ฝั่ง C เราแค่เรียกใช้ผล (จะแกะข้างในใน โมดูล 3 (Processing))

> ทั้งหมดนี้จะกลายเป็น "มือ" ที่ติดตัว — ชุดบทเรียน DAQ (บทเรียน 2.1–2.2) เราจะเอาโครงเดียวกันนี้ไปเขียน logger เก็บข้อมูลลงไฟล์ โดยไม่ต้องเริ่มจากศูนย์

---

# ใช้จริงที่ไหน — แอปเซนเซอร์ในโลกจริง

สามตัวอย่างที่เรา remix วันนี้ไม่ใช่ของเล่น ทุกตัวมีสินค้าจริงในตลาดที่ทำงานด้วยโครงเดียวกัน:

<div style="text-align:center;margin:6px 0">
<svg width="880" height="220" viewBox="0 0 880 220" font-family="DejaVu Sans, sans-serif">
  <rect x="12" y="10" width="420" height="96" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="28" y="34" font-size="13" font-weight="700" fill="#1565c0">Tilt (IMU) — เครื่องมือ/ยานพาหนะ</text>
  <text x="28" y="56" font-size="11" fill="#555">ระดับน้ำดิจิทัล · เตือนรถพ่วงเอียง · โดรนรู้ท่าตัวเอง</text>
  <text x="28" y="76" font-size="11" fill="#555">อ่าน accel → dsp.tilt → เตือนเมื่อเกินเกณฑ์</text>
  <text x="28" y="96" font-size="11" fill="#888">คือ Tilt Monitor ที่เรา remix วันนี้เป๊ะ</text>
  <rect x="448" y="10" width="420" height="96" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="464" y="34" font-size="13" font-weight="700" fill="#2e7d32">Motion (IMU) — สุขภาพ/ฟิตเนส</text>
  <text x="464" y="56" font-size="11" fill="#555">นับก้าว · ตรวจการล้ม · รู้ท่าออกกำลัง</text>
  <text x="464" y="76" font-size="11" fill="#555">โครงเดียวกัน ต่างแค่ "คำนวณอะไรจาก 6 แกน"</text>
  <text x="464" y="96" font-size="11" fill="#888">ต่อยอดจาก 01 ที่เราอ่านวันนี้</text>
  <rect x="12" y="118" width="420" height="92" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="28" y="142" font-size="13" font-weight="700" fill="#e65100">Radar — อาคาร/ป้าย</text>
  <text x="28" y="164" font-size="11" fill="#555">เปิดไฟอัตโนมัติ · ป้ายโฆษณารู้ว่ามีคนดู</text>
  <text x="28" y="184" font-size="11" fill="#555">ไม่ใช้กล้อง = เป็นส่วนตัว · ทำงานในที่มืด</text>
  <text x="28" y="202" font-size="11" fill="#888">คือ 04 ที่เรารันวันนี้</text>
  <rect x="448" y="118" width="420" height="92" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="464" y="142" font-size="13" font-weight="700" fill="#6a1b9a">ร่วมกัน — โครงเดียว เปลี่ยนได้ทุกงาน</text>
  <text x="464" y="164" font-size="11" fill="#555">อ่าน → คำนวณ → วาด → ฟังปุ่ม เหมือนกันหมด</text>
  <text x="464" y="184" font-size="11" fill="#555">สลับเซนเซอร์/การคำนวณ = ได้สินค้าใหม่</text>
  <text x="464" y="202" font-size="11" fill="#888">นี่คือพลังของการจับ "โครงร่วม" ให้ขาด</text>
</svg>
</div>

> เห็นไหมว่าพอจับโครงร่วมได้ คุณไม่ได้เรียนแค่ "แอปเดียว" แต่ได้แม่แบบที่ปรับเป็นสินค้าจริงได้สารพัด — แค่เปลี่ยนช่อง "อ่าน" กับ "คำนวณ"

---

# งานทำเอง + สรุปบทเรียน

**งานทำเอง (ท้ายบทเรียน):**

1. เติม [`s02_anatomy_sensor.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l05-sensor-remix-lab/practice/s02_anatomy_sensor.py) ให้ครบทั้ง 4 ช่อง รันได้จริง (Emulator หรือบอร์ด)
2. ทำ remix ที่ **ต่างจากต้นฉบับ** อย่างน้อยหนึ่งอย่าง: สลับเซนเซอร์ (`radar()`) หรือเปลี่ยนการแสดงผล แล้วจดว่าแก้อะไร เพราะอะไร
3. ชี้ให้ได้ว่าในไฟล์ remix ของคุณ บรรทัดไหนอยู่ **จังหวะไหน** (import / สร้างครั้งเดียว / ลูป / poll)

ใบ้ข้อ 2 — remix ที่ง่ายและเห็นผลชัด: เปลี่ยน `TILT_LIMIT` เป็น 10 (ป้ายไวขึ้น) หรือสลับ `bmi270.motion()` เป็น `sensors.radar()` แล้วโชว์ presence แทนมุม

**วันนี้เราได้:** อ่านแอปเซนเซอร์ที่ทำงานได้ให้ออก · จับโครงร่วม 4 จังหวะ · รู้จัก `sensors.*` + `dsp.tilt` · remix สามแอปเป็น Tilt Monitor ของตัวเอง

> ชุดบทเรียนถัดไป (บทเรียน 1.6–1.7) เราจะเอา "การแกะโครง" แบบเดียวกันนี้ไปใช้กับ **แอป Edge AI** — แกะเมนูโมเดลจากบทเรียน 1.1–1.3 ให้ขาด แล้ว remix ให้สลับโมเดล + สั่งการเมื่อเจอคลาสที่ต้องการ เจอกันครับ
