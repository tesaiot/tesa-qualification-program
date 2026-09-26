---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 4.2 — ลงมือทำ: ฟิลเตอร์ทำสัญญาณให้สะอาดสด ๆ"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · ดัดแปลงจาก Edge AI Developer (รศ.วิรุฬห์ ศรีบริรักษ์, BUU) · CC BY 4.0"
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

# บทเรียน 4.2 — ลงมือทำ: ฟิลเตอร์ทำสัญญาณให้สะอาดสด ๆ

## Analysis I: ฟิลเตอร์ DSP · ทำสัญญาณให้สะอาดสด ๆ ตรงหน้า

**โมดูล 4 — วิเคราะห์สัญญาณ**

> ต่อจากบทเรียน 4.1 — ฟิลเตอร์ DSP: EMA, Median, Kalman และ radar range profile

---

# โครงร่วมของโปรแกรม — คุ้นแล้วใช่ไหม

โครงเดิมทุกบทเรียน: **import → สร้างครั้งเดียว → ลูป → `ui.poll`** วันนี้ "สร้างครั้งเดียว" มีของใหม่คือ **อ็อบเจกต์ฟิลเตอร์**

<div style="text-align:center;margin:6px 0">
<svg width="880" height="130" viewBox="0 0 880 130" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arSk" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="40" width="190" height="56" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="115" y="64" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">1 · import</text>
  <text x="115" y="84" font-size="11" fill="#666" text-anchor="middle">ui · lcd · sensors · dsp</text>
  <rect x="238" y="40" width="200" height="56" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="338" y="64" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">2 · สร้างครั้งเดียว</text>
  <text x="338" y="84" font-size="11" fill="#666" text-anchor="middle">widget + ฟิลเตอร์ dsp</text>
  <rect x="466" y="40" width="190" height="56" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="561" y="64" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">3 · ลูป</text>
  <text x="561" y="84" font-size="11" fill="#666" text-anchor="middle">read → update → วาด</text>
  <rect x="684" y="40" width="176" height="56" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="772" y="64" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">4 · ui.poll</text>
  <text x="772" y="84" font-size="11" fill="#666" text-anchor="middle">สลับฟิลเตอร์/แหล่ง</text>
  <line x1="210" y1="68" x2="236" y2="68" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <line x1="438" y1="68" x2="464" y2="68" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <line x1="656" y1="68" x2="682" y2="68" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <path d="M772,96 C772,116 561,116 561,98" fill="none" stroke="#9e9e9e" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arSk)"/>
  <text x="666" y="120" font-size="11" fill="#9e9e9e" text-anchor="middle">วนกลับ</text>
</svg>
</div>

> ย้ำอีกครั้ง: ฟิลเตอร์ต้องสร้างใน "ขั้นที่ 2" นอกลูป เพราะมันเก็บความจำ ถ้าเผลอสร้างในลูป = รีเซ็ตความจำทุกรอบ เส้นล่างจะไม่มีวันเรียบ

---

# โครงของไฟล์ s08_filters.py

ทั้งไฟล์อ่านเป็นประโยคเดียว: **"อ่านค่าดิบ → ป้อนเข้าฟิลเตอร์ → วาดดิบเทียบกรอง → วัดว่าลด noise ได้กี่ %"**

<div style="text-align:center;margin:6px 0">
<svg width="900" height="180" viewBox="0 0 900 180" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arS8" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g font-size="13" text-anchor="middle">
    <rect x="14" y="30" width="180" height="54" rx="10" fill="#cfd8dc" stroke="#607d8b" stroke-width="2"/>
    <text x="104" y="52" font-weight="700" fill="#455a64">make_filter()</text>
    <text x="104" y="70" font-size="11" fill="#999">สร้างฟิลเตอร์ :46</text>
    <rect x="234" y="30" width="180" height="54" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="324" y="52" font-weight="700" fill="#1565c0">read_raw()</text>
    <text x="324" y="70" font-size="11" fill="#999">accel magnitude :99</text>
    <rect x="454" y="30" width="180" height="54" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="544" y="52" font-weight="700" fill="#e65100">filt.update(x)</text>
    <text x="544" y="70" font-size="11" fill="#999">กรองหนึ่งค่า</text>
    <rect x="674" y="30" width="200" height="54" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="774" y="52" font-weight="700" fill="#2e7d32">วาดสองกราฟ</text>
    <text x="774" y="70" font-size="11" fill="#999">raw_chart / filt_chart</text>
  </g>
  <line x1="194" y1="57" x2="232" y2="57" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS8)"/>
  <line x1="414" y1="57" x2="452" y2="57" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS8)"/>
  <line x1="634" y1="57" x2="672" y2="57" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS8)"/>
  <path d="M774,84 C774,130 324,130 324,86" fill="none" stroke="#2e7d32" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arS8)"/>
  <text x="540" y="126" font-size="12" fill="#2e7d32" text-anchor="middle">วนอ่าน+กรองทุก 60 ms · แถบ noise down % วัด jitter ดิบเทียบกรอง</text>
</svg>
</div>

> ตัวเลขบรรทัด (`:46`, `:99`) ชี้จุดที่คุณต้องเติมโค้ดในไฟล์ฝึก จำโครงนี้ไว้ เดี๋ยวไล่ทีละส่วน

---

# make_filter() — สร้างฟิลเตอร์จากชื่อ

**ช่องเติมที่ 1 และ 2**: ฟังก์ชันนี้แปลงชื่อฟิลเตอร์เป็นอ็อบเจกต์จริง สังเกต keyword argument ให้ดี:

```python
def make_filter(name):
    if name == "Median":
        # เติม: return dsp.Median(window=MED_WINDOW)
        pass
    if name == "Kalman1D":
        # เติม: return dsp.Kalman1D(q=KAL_Q, r=KAL_R)
        pass
    return dsp.EMA(alpha=EMA_ALPHA)   # ให้ไว้แล้ว (ค่าเริ่มต้น)
```

- ช่อง 1: แทน `pass` ด้วย `return dsp.Median(window=MED_WINDOW)`
- ช่อง 2: แทน `pass` ด้วย `return dsp.Kalman1D(q=KAL_Q, r=KAL_R)`
- EMA ให้ไว้แล้วเป็นตัวอย่างรูปแบบ — ถ้าลืมเติมช่อง 1/2 แอปยังรันได้ (ใช้ EMA เสมอ) แต่เลือก Median/Kalman แล้วจอจะค้าง/พัง

> ทำไมต้องเป็น `window=` `q=` `r=` ไม่ใช่ `dsp.Median(5)` เฉย ๆ? เพราะฝั่ง C ประกาศพารามิเตอร์เป็น keyword-only ส่ง positional จะโยน `TypeError` ทันที — อ่านข้อความ error แล้วแก้เป็น keyword

---

# ไล่โค้ด (1) — อ่านค่าดิบ + accel magnitude

**ช่องเติมที่ 3**: อ่านความเร่งสามแกนแล้วยุบเป็น "ขนาด" ค่าเดียวเพื่อเอาไปกรอง:

```python
def read_raw():
    global last_raw
    if source == 0:                     # IMU
        ax, ay, az = sensors.bmi270.acceleration()
        # เติม: mag = (ax*ax + ay*ay + az*az) ** 0.5
        mag = 0.0
        pass
        last_raw = mag * 10.0           # x10 ให้เห็นชัดบนกราฟ
    ...
    return last_raw
```

- แทนบล็อกด้วย `mag = (ax*ax + ay*ay + az*az) ** 0.5` — นี่คือความยาวเวกเตอร์ (Pythagoras 3 มิติ)
- อยู่นิ่ง magnitude ≈ 9.8 (แรงโน้มถ่วง 1g) พอขยับจะพุ่งขึ้น → หนามเพียบ เหมาะเป็นของเล่นฟิลเตอร์
- ถ้าลืมเติม: `mag` ค้างที่ 0 → ทั้งสองกราฟแบนราบ ไม่มีอะไรให้กรอง

> ทำไมยุบสามแกนเป็นค่าเดียว? เพราะฟิลเตอร์ในชุดบทเรียนนี้เป็น **1 มิติ** (`Kalman1D` — เลข 1 บอกอยู่) เราจึงต้องแปลงเวกเตอร์เป็นสเกลาร์ก่อน (การ fuse หลายแกนจริง ๆ คือ `dsp.Madgwick` เก็บไว้บทเรียนเรื่อง IMU เชิงลึก)

---

# ไล่โค้ด (2) — filt.update(x) หัวใจของชุดบทเรียน

**ช่องเติมที่ 4**: บรรทัดเดียวที่เป็นหัวใจทั้งชุดบทเรียน ป้อนค่าดิบเข้าฟิลเตอร์ รับค่าที่กรองแล้วออกมา:

```python
x = read_raw()          # ค่าดิบ (มีหนาม)
# เติม: y = filt.update(x)
y = x
pass
```

- แทนด้วย `y = filt.update(x)` — `filt` คืออ็อบเจกต์ที่ `make_filter()` สร้างไว้
- ถ้าลืมเติม (`y = x`): เส้นล่างจะเท่าเส้นบนเป๊ะ — ไม่มีการกรองเลย (บททดสอบง่าย ๆ ว่าเติมถูกไหม: สองกราฟต้องต่างกัน)
- `filt` เปลี่ยนได้ตอน runtime เมื่อผู้ใช้เลือก dropdown — แต่โค้ดบรรทัดนี้ไม่ต้องรู้ว่าเป็นตัวไหน เพราะ API เหมือนกันหมด

> พลังของ API ร่วม: บรรทัด `filt.update(x)` เขียนครั้งเดียว ใช้ได้กับทั้ง EMA/Median/Kalman โดยไม่ต้อง if แยก — นี่คือเหตุผลที่ทุกฟิลเตอร์ออกแบบให้หน้าตาเหมือนกัน

---

# ไล่โค้ด (3) — วาดสองกราฟ + วัด noise

**ช่องเติมที่ 5**: เอาค่าดิบกับค่ากรองขึ้นสองกราฟ ให้ตาเทียบกันได้:

```python
# เติม: raw_chart.value(clamp(x))  แล้ว  filt_chart.value(clamp(y))
pass

raw_jit  += abs(x - prev_x)      # การกระตุกของเส้นดิบ
filt_jit += abs(y - prev_y)      # การกระตุกของเส้นกรอง
...
red = (1.0 - filt_jit / raw_jit) * 100.0    # ลด jitter ได้กี่ %
```

- แทน `pass` ด้วยสองบรรทัด: `raw_chart.value(clamp(x))` และ `filt_chart.value(clamp(y))`
- `clamp()` คุมค่าให้อยู่ในช่วงกราฟ 0..250 (กันเส้นทะลุขอบ)
- เมตริก `noise down %` วัดจาก **การกระตุกระหว่างเฟรม** (ผลรวม `|x - x_prev|`) — ไม่ต้องมีสัญญาณจริงให้เทียบ ใช้กับเซนเซอร์จริงได้เลย

> เราวัด "ความเรียบ" ด้วย jitter เพราะกับเซนเซอร์จริงเราไม่มี "เฉลย" ว่าค่าจริงคือเท่าไร — วิธีนี้ตรงไปตรงมา: ฟิลเตอร์ดี = การกระตุกลดลง

---

# ลงมือ (1) — รันบน BENTO Emulator

ไม่มีบอร์ดก็เริ่มได้ (IMU จำลองมีให้ครบ):

1. เปิด **ide.tesaiot.dev** ในเบราว์เซอร์ เปิดไฟล์ [`s08_filters.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l02-filters-lab/practice/s08_filters.py)
2. เติมช่องว่างทั้ง 5 จุดตามคำใบ้ `# เติม:`
3. กด **Run** จะเห็นสองกราฟ + dropdown เลือกฟิลเตอร์/แหล่ง
4. ลากปุ่ม Shake ที่ Emulator จำลอง หรือขยับ → เส้นบนเต้น เส้นล่างเรียบกว่า
5. สลับฟิลเตอร์ EMA → Median → Kalman1D ดูว่าเส้นล่างเปลี่ยนนิสัยยังไง

> แหล่ง **Radar range** บน Emulator เป็นระยะจำลองที่หมุนด้วยลูกบิด ไม่มี multipath จริง — ใช้ IMU accel เป็นหลักตอนซ้อม แล้วค่อยลอง radar จริงบนบอร์ด

---

# หน้าตาบนจอ — BENTO Edge AI Emulator

นี่คือของจริงที่รันได้ในเบราว์เซอร์ ไม่ต้องมีบอร์ดก็เห็นสัญญาณ IMU ขยับตามมือ:

<div style="text-align:center;margin:6px 0">

![จอ BENTO Emulator ขณะรันแดชบอร์ด IMU: ค่า gx gy gz จากตัวจำลองและแถบขนาดความเร่ง w:680](../../assets/img/imu_dashboard.png)

</div>

จอ emulator ที่รันได้จริง — IMU dashboard บน BENTO Edge AI Emulator (ide.tesaiot.dev) ค่าดิบขยับตามที่เราลากปุ่ม Shake

- เปิดจากเบราว์เซอร์ล้วน ๆ ไม่ต้องต่อสาย ไม่ต้องลง toolchain — เหมาะกับซ้อมก่อนลงบอร์ดจริง
- ค่า accel สามแกนที่เห็นตรงนี้ คือ `x` ตัวเดียวกับที่เราจะป้อนเข้า `filt.update(x)` ในแอป [`s08_filters.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l02-filters-lab/practice/s08_filters.py)

> เห็นเลขเต้น ๆ ตรงนี้ไหม นั่นแหละหนามที่เราจะกรอง — จอนี้คือสนามซ้อมก่อนจะไปเจอสัญญาณจริงบนบอร์ดจริง

---

# ลงมือ (2) — รันบนบอร์ด BENTO จริง

บนบอร์ดจริงได้ครบทั้ง IMU และ **radar range profile** ของจริง:

1. เสียบบอร์ด เปิด [`s08_filters.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l02-filters-lab/practice/s08_filters.py) ใน **BENTO IDE** กด **Program to Device**
2. โหมด IMU: ขยับ/เขย่าบอร์ด ดูสองกราฟเทียบ + noise down %
3. สลับ dropdown แหล่งเป็น **Radar range** แล้วเดินเข้า-ออกหน้าบอร์ด 0.5–5 เมตร
4. เลือกฟิลเตอร์ **Median** ในโหมด radar → สังเกตว่าระยะที่กระโดด (multipath) นิ่งขึ้นชัดเจน
5. เทียบ EMA กับ Median ในโหมด radar — Median กัน spike ได้ดีกว่า เห็นด้วยตา

> จุดที่ควรสังเกต: ในโหมด radar ลอง EMA ก่อน จะเห็น spike ถูกเกลี่ยเป็นโหนกนุ่ม ๆ แต่ยังอยู่ — พอสลับเป็น Median โหนกหายไปเลย นี่คือความต่างของ "เกลี่ย" กับ "โหวตตัด"

---

# ลงมือทำ — เติมช่องว่างทั้ง 5 จุด

เปิด [`s08_filters.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l02-filters-lab/practice/s08_filters.py) มี `pass`/placeholder วางไว้ **5 จุด** ตรงที่ต้องเติมของจริง:

| # | จุด | เติมด้วย | ถ้าลืม |
|---|---|---|---|
| 1 | make_filter (Median) | `return dsp.Median(window=MED_WINDOW)` | เลือก Median แล้วพัง |
| 2 | make_filter (Kalman) | `return dsp.Kalman1D(q=KAL_Q, r=KAL_R)` | เลือก Kalman แล้วพัง |
| 3 | read_raw | `mag = (ax*ax+ay*ay+az*az) ** 0.5` | สองกราฟแบนราบ |
| 4 | ในลูป | `y = filt.update(x)` | เส้นล่าง = เส้นบน (ไม่กรอง) |
| 5 | ในลูป | `raw_chart.value(clamp(x))` + `filt_chart.value(clamp(y))` | จอไม่ขึ้นกราฟ |

ขั้นตอน:

1. ไล่หา `# เติม:` ทีละจุด แทน `pass`/placeholder ด้วยคำสั่งตามคำใบ้
2. กด **Run** (Emulator) หรือ **Program to Device** (บอร์ด)
3. ขยับบอร์ด ดูสองกราฟต่างกัน สลับฟิลเตอร์ครบสามตัว ถ้าไม่ต่างกลับไปเช็กช่อง 4

> ห้าช่องนี้ประกอบเป็นไปป์ไลน์ Analysis ที่สมบูรณ์: สร้างฟิลเตอร์ → อ่านค่า → กรอง → เห็นผล เติมครบเมื่อไร คุณทำสัญญาณจริงให้สะอาดได้ด้วยมือตัวเอง

---

# แหล่งเรียนรู้เพิ่มเติม

ถ้าอยากเข้าใจฟิลเตอร์ให้ลึกกว่านี้ สามช่องนี้อธิบายด้วยภาพเคลื่อนไหวเข้าใจง่ายมาก:

**วิดีโอ (อธิบายเชิงสัญชาตญาณ)**
- Kalman filter อธิบายแบบเห็นภาพ — ช่อง Michel van Biezen: https://www.youtube.com/@MichelvanBiezen
- แนวคิด moving average / smoothing เชิงคณิต — ช่อง 3Blue1Brown: https://www.youtube.com/@3blue1brown
- Signal / filtering เชิงวิศวกรรม — ช่อง Computerphile: https://www.youtube.com/@Computerphile

**ภาพ/เอกสารอ้างอิง (เปิดอ่านต่อได้)**
- Moving average (บทความ + กราฟตัวอย่าง): https://en.wikipedia.org/wiki/Moving_average
  (ที่มา: Wikipedia, CC BY-SA)
- Kalman filter (ภาพรวม + สมการ predict/update): https://en.wikipedia.org/wiki/Kalman_filter
  (ที่มา: Wikipedia, CC BY-SA)
- Exponential smoothing (พื้นฐานของ EMA): https://en.wikipedia.org/wiki/Exponential_smoothing
  (ที่มา: Wikipedia, CC BY-SA)

> วิดีโอ/ภาพภายนอกเป็นของเจ้าของต้นฉบับ ใช้เพื่อการศึกษา อ้างอิงลิงก์ต้นทาง — เปิดดูเป็นการบ้านเสริม ไม่บังคับ แต่ช่วยให้ภาพสูตรที่เราแกะกันวันนี้ชัดขึ้นอีกมาก

---

# ชัยชนะที่เห็นได้ + MVP ของชุดบทเรียนนี้

<div style="text-align:center;margin:14px 0">
<div style="display:inline-block;background:#e8f5e9;border:2px solid #2e7d32;border-radius:22px;padding:10px 22px;color:#2e7d32;font-weight:700;font-size:1.05em">
ชัยชนะที่เห็นได้ของชุดบทเรียนนี้ · สัญญาณจริงที่มีหนาม ถูกกรองให้เรียบสด ๆ บนจอ — เส้นล่างสะอาดกว่าเส้นบนเห็นชัด
</div>
</div>

**MVP ของบทเรียน 4.1–4.2 (เกณฑ์ผ่านของชุดบทเรียน):** คุณเปิดแอป [`s08_filters.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l02-filters-lab/practice/s08_filters.py) แล้วทำให้ฟิลเตอร์ **ปรับสัญญาณเซนเซอร์ที่มี noise ให้ดีขึ้นอย่างเห็นได้** — เส้น Filtered เรียบกว่าเส้น Raw ชัดเจน พร้อมตัวเลข `noise down %` ยืนยัน

- ทำบน **Emulator** (IMU) หรือ **บอร์ดจริง** (IMU หรือ radar range) ก็ได้
- อธิบายได้ว่าเลือกฟิลเตอร์ตัวไหน เพราะอะไร และข้อแลกเปลี่ยน "เรียบ ↔ ตอบสนอง" คืออะไร

> "กรองดีขึ้น" ไม่ใช่แค่ "เส้นดูสวย" — คุณต้องบอกได้ว่าทำไม Median ชนะ EMA ตอนเจอ spike และทำไม α เล็กลงถึงเรียบขึ้นแต่ตามช้าลง

---

# บันไดช่วยเหลือ — ใบ้ → เริ่มจากโครง → เฉลย → ฉบับเต็ม

ถ้าติด ให้ไต่บันไดนี้ทีละขั้น อย่าเพิ่งกระโดดไปดูเฉลย เพราะของจะเข้าหัวตอนที่คุณพยายามเองก่อน:

- **ใบ้** — คำใบ้อยู่ในคอมเมนต์ `# เติม:` ทั้ง 5 จุดในไฟล์ฝึก + ตารางหน้าที่แล้ว บอกว่าแต่ละช่องเติมอะไร
- **เริ่มจากโครง** — [`s08_filters.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l02-filters-lab/practice/s08_filters.py) มีโครงครบทั้งไฟล์แล้ว เหลือ 5 จุดให้เติม (make_filter 2 จุด + ในลูป 3 จุด)
- **เฉลย** — [`s08_filters.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l02-filters-lab/solution/s08_filters.py) เติมครบพร้อมคอมเมนต์อธิบายทุกช่อง (อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์เอง)
- **ฉบับเต็ม** — [`s08_filters_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l02-filters-lab/examples/s08_filters_full.py) เพิ่ม slider จูนพารามิเตอร์สด (α/window/r), แถบ noise down เปลี่ยนสีตามเกณฑ์, ปุ่ม Freeze จับภาพหนามนิ่ง ๆ

> ลองเขียนเองให้สุดก่อนนะ ถ้าติดจริง ๆ ค่อยเปิดเฉลยดูทีละช่อง แล้วกลับมาพิมพ์เอง — เดี๋ยวเราค่อย ๆ แกะไปด้วยกัน

---

# เชื่อมโยงรากฐาน — วันนี้เราแตะอะไรไปบ้าง

การกรองสัญญาณตัวแรกซ่อนแนวคิด Analysis หลายชั้นที่จะใช้ต่อไปตลอดเสา 3–5:

**ฝั่ง Analysis / สัญญาณ**
- **Noise ≠ signal** — สัญญาณดิบมีหนามเสมอ ต้องแยกของจริงออกจากสัญญาณรบกวนก่อนตัดสินใจ
- **Temporal filter** — ฟิลเตอร์จำอดีต ป้อนสด `.update(x)` ทีละค่า (streaming) เหมาะกับ MCU ที่ RAM น้อย
- **ข้อแลกเปลี่ยน เรียบ ↔ ตอบสนอง** — หัวใจของการจูนฟิลเตอร์ทุกตัว (α, window, q/r)
- **เลือกให้ตรงกับ noise** — EMA (หนามเล็ก) / Median (spike) / Kalman (ผสม)

**ฝั่ง MicroPython / โครงโปรแกรม**
- **สร้างครั้งเดียว** — ฟิลเตอร์เก็บ state ในตัว ห้ามสร้างในลูป (จะรีเซ็ตความจำ)
- **API ร่วม** — `.update/.value/.reset` เหมือนกันทุกตัว → สลับฟิลเตอร์โดยไม่แก้ลูป
- **try/except กับฮาร์ดแวร์ที่อาจไม่พร้อม** — `radar_range()` โยน `OSError` เมื่อ radar DSP ไม่ทำงาน เราจึงห่อไว้ (ซ้ำบทเรียน 1.1–1.3)

> ทั้งหมดนี้คือประตูสู่ บทเรียน 4.3–4.4 (FFT — มองสัญญาณในโดเมนความถี่) และ บทเรียน 4.5–4.6 (feature ที่โมเดลกินจริง) — กรองให้สะอาดก่อน แล้วค่อยสกัด feature เสมอ

---

# ใช้จริงที่ไหน — filtering ในโลกจริง

ฟิลเตอร์สามตัวที่เล่นวันนี้ไม่ใช่ของสมมติ ทุกตัวอยู่ในสินค้าจริงที่คุณใช้ทุกวัน:

<div style="text-align:center;margin:6px 0">
<svg width="880" height="210" viewBox="0 0 880 210" font-family="DejaVu Sans, sans-serif">
  <rect x="12" y="10" width="420" height="92" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="28" y="34" font-size="13" font-weight="700" fill="#1565c0">EMA — เกจ/นาฬิกา/เทอร์โมสตัท</text>
  <text x="28" y="56" font-size="11" fill="#555">เลขก้าว · อุณหภูมิห้อง · ความสว่างจอออโต้</text>
  <text x="28" y="76" font-size="11" fill="#555">ต้องนิ่งไม่กระพริบ ยอมช้าได้นิด → EMA ราคาถูก</text>
  <text x="28" y="94" font-size="11" fill="#888">ฟิลเตอร์ที่ฝังในเฟิร์มแวร์อุปกรณ์นับล้านตัว</text>
  <rect x="448" y="10" width="420" height="92" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="464" y="34" font-size="13" font-weight="700" fill="#2e7d32">Median — เรดาร์/GPS/ระยะ</text>
  <text x="464" y="56" font-size="11" fill="#555">ระยะเรดาร์รถยนต์ · พิกัด GPS · เซนเซอร์จอด</text>
  <text x="464" y="76" font-size="11" fill="#555">ค่ากระโดดเป็นครั้งคราว (multipath) → Median ตัดทิ้ง</text>
  <text x="464" y="94" font-size="11" fill="#888">โมเดล Push Detection ก็ยืนบนระยะที่กรองแล้ว</text>
  <rect x="12" y="112" width="420" height="88" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="28" y="136" font-size="13" font-weight="700" fill="#6a1b9a">Kalman — โดรน/รถ/AR</text>
  <text x="28" y="158" font-size="11" fill="#555">ทรงตัวโดรน · นำทางรถ · ติดตามหัวใน VR/AR</text>
  <text x="28" y="178" font-size="11" fill="#555">ผสม IMU + เซนเซอร์อื่นแบบเรียลไทม์ → Kalman</text>
  <rect x="448" y="112" width="420" height="88" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="464" y="136" font-size="13" font-weight="700" fill="#e65100">ร่วมกัน — สะอาดก่อนเข้าโมเดล</text>
  <text x="464" y="158" font-size="11" fill="#555">Edge AI ทุกงานกรอง noise ก่อนป้อนโมเดลเสมอ</text>
  <text x="464" y="178" font-size="11" fill="#555">สัญญาณสะอาด = โมเดลเล็กลง + แม่นขึ้น</text>
</svg>
</div>

> เห็นไหมว่าฟิลเตอร์ไม่ใช่ของเล่นในห้องเรียน — มันคือชั้นแรกที่ทำให้สัญญาณ "อ่านออก" ทั้งสำหรับคนและสำหรับโมเดล เราแค่กำลังเริ่มจับเครื่องมือชุดนี้

---

# งานทำเอง + สรุปบทเรียน

**งานทำเอง (ท้ายบทเรียน):**

1. เติม [`s08_filters.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l02-filters-lab/practice/s08_filters.py) ให้ครบทั้ง 5 ช่อง รันได้จริง (Emulator หรือบอร์ด) — เส้น Filtered เรียบกว่า Raw
2. ทดลองสลับครบ **สามฟิลเตอร์** (EMA → Median → Kalman1D) จดค่า `noise down %` ของแต่ละตัวกับสัญญาณเดียวกัน
3. หาสถานการณ์ที่ **Median ชนะ EMA ชัดเจน** (ใบ้: สร้าง spike — เคาะบอร์ดแรง ๆ ครั้งเดียว หรือใช้ radar multipath) แล้วอธิบายว่าทำไม

ใบ้ข้อ 3 — spike คือค่าโดดสุดขั้วครั้งเดียว EMA จะเกลี่ยมันเป็นโหนกที่ยังเห็น ส่วน Median จะโหวตมันตกไปเลย

**วันนี้เราได้:** เข้าใจว่า noise คืออะไรและมาจากไหน · รู้จักฟิลเตอร์สามตระกูล (`EMA`/`Median`/`Kalman1D`) + API ร่วม · เห็น radar range profile ของจริง · ทำสัญญาณจริงให้สะอาดสด ๆ พร้อมวัดผลเป็น %

> ชุดบทเรียนถัดไป (บทเรียน 4.3–4.4) เราจะมองสัญญาณเดียวกันนี้ใน **โดเมนความถี่** ด้วย FFT — จากการดูว่า "ค่าขึ้นลงยังไงตามเวลา" ไปสู่ "มีความถี่อะไรซ่อนอยู่บ้าง" เจอกันครับ
