---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 5.2 — ลงมือทำ: เก็บ dataset ที่สมดุลบนบอร์ดแล้วแบ่งบน PC"
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

# บทเรียน 5.2 — ลงมือทำ: เก็บ dataset ที่สมดุลบนบอร์ดแล้วแบ่งบน PC

## Training I: วิศวกรรมชุดข้อมูล · เก็บ · ติดป้าย · แบ่ง

**โมดูล 5 — ฝึกโมเดลและนำไปใช้หลายเป้าหมาย**

> ต่อจากบทเรียน 5.1 — วิศวกรรมชุดข้อมูล: สมดุลคลาส หน้าต่าง และการแบ่ง train/val/test

---

# MPY → CSV — เก็บ dataset บนบอร์ด

นี่คือพื้นผิวของคุณชุดบทเรียนนี้: [`s11_dataset.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l02-dataset-lab/practice/s11_dataset.py) รันบนบอร์ด อ่าน IMU แล้วเขียน CSV ที่ `/gestures.csv` — ต่างจาก บทเรียน 2.1–2.2 ตรงที่มัน **เฝ้าดู class balance** ให้ระหว่างเก็บ

<div style="text-align:center;margin:6px 0">
<svg width="900" height="170" viewBox="0 0 900 170" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arMpy" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="50" width="180" height="70" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="110" y="80" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">BMI270 (IMU)</text>
  <text x="110" y="100" font-size="11" fill="#666" text-anchor="middle">bmi270.motion()</text>
  <rect x="250" y="50" width="200" height="70" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="350" y="74" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">ติดป้าย + นับสมดุล</text>
  <text x="350" y="94" font-size="11" fill="#666" text-anchor="middle">counts[label] += ...</text>
  <text x="350" y="110" font-size="10" fill="#888" text-anchor="middle">แถบต่อคลาสบนจอ</text>
  <rect x="500" y="50" width="180" height="70" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="590" y="80" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">เขียน CSV</text>
  <text x="590" y="100" font-size="11" fill="#666" text-anchor="middle">/gestures.csv</text>
  <rect x="730" y="50" width="150" height="70" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="805" y="80" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">→ PC</text>
  <text x="805" y="100" font-size="11" fill="#666" text-anchor="middle">split ที่นั่น</text>
  <line x1="200" y1="85" x2="248" y2="85" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arMpy)"/>
  <line x1="450" y1="85" x2="498" y2="85" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arMpy)"/>
  <line x1="680" y1="85" x2="728" y2="85" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arMpy)"/>
  <text x="450" y="150" font-size="11" fill="#888" text-anchor="middle">เก็บบนบอร์ด → คัดลอกไฟล์ออกมา → split บน PC ด้วย dataset_tools.py</text>
</svg>
</div>

> [`s11_dataset.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l02-dataset-lab/practice/s11_dataset.py) เป็นสคริปต์ MicroPython (ไม่ใช่เกม) — เหมาะกับโมดูล 5 (Training) ที่งานคือ "เก็บข้อมูลให้ดี" ยังคงมีฉบับฝึก/เฉลย/เต็ม เหมือนชุดบทเรียนอื่น แค่ตัวชิ้นงานเป็นสคริปต์เก็บข้อมูล

---

# รู้จัก sensors.bmi270.motion()

หัวใจของการเก็บคือคำสั่งเดียว: อ่าน IMU 6 แกนพร้อมกันในทูเพิลเดียว — accelerometer 3 แกน + gyroscope 3 แกน

```python
import sensors
ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
# ax,ay,az = ความเร่ง (m/s^2) — az ~ 9.81 ตอนวางนิ่ง (แรงโน้มถ่วง)
# gx,gy,gz = ความเร็วเชิงมุม (deg/s) — ~0 ตอนไม่หมุน
```

- `motion()` คืน 6 ค่าในครั้งเดียว = 6 คอลัมน์ของ CSV เป๊ะ (ไม่ต้องเรียก accel/gyro แยก)
- อ่านที่ `20 ms` ต่อครั้ง = `50 Hz` ตรงกับอัตราที่โมเดล Motion บนบอร์ดกิน — สำคัญเพื่อให้ dataset เข้ากับโมเดลได้

> ลองใน REPL ก่อน: `import sensors; sensors.bmi270.motion()` แล้ววางบอร์ดนิ่งๆ ดูว่า `az` ใกล้ 9.81 ไหม — นี่คือการ "ถามฮาร์ดแวร์" เพื่อเช็กว่า sensor พร้อมก่อนเก็บจริง

---

# โครงร่วมของโปรแกรมเก็บข้อมูล

[`s11_dataset.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l02-dataset-lab/practice/s11_dataset.py) เดินตามโครงร่วมเดียวกับทุกโปรแกรม MicroPython ในคอร์ส (import → สร้างครั้งเดียว → ลูป → `ui.poll`) — คุ้นแล้วจากชุดบทเรียนก่อน ๆ

<div style="text-align:center;margin:6px 0">
<svg width="880" height="130" viewBox="0 0 880 130" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arSk11" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="40" width="190" height="56" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="115" y="64" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">1 · import</text>
  <text x="115" y="84" font-size="11" fill="#666" text-anchor="middle">ui · lcd · sensors · time</text>
  <rect x="238" y="40" width="200" height="56" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="338" y="64" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">2 · สร้างครั้งเดียว</text>
  <text x="338" y="84" font-size="11" fill="#666" text-anchor="middle">ปุ่ม label + แถบสมดุล</text>
  <rect x="466" y="40" width="190" height="56" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="561" y="64" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">3 · record</text>
  <text x="561" y="84" font-size="11" fill="#666" text-anchor="middle">อ่าน+เขียน+นับ</text>
  <rect x="684" y="40" width="176" height="56" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="772" y="64" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">4 · ui.poll</text>
  <text x="772" y="84" font-size="11" fill="#666" text-anchor="middle">รับปุ่ม label</text>
  <line x1="210" y1="68" x2="236" y2="68" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk11)"/>
  <line x1="438" y1="68" x2="464" y2="68" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk11)"/>
  <line x1="656" y1="68" x2="682" y2="68" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk11)"/>
  <path d="M772,96 C772,116 561,116 561,98" fill="none" stroke="#9e9e9e" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arSk11)"/>
  <text x="666" y="120" font-size="11" fill="#9e9e9e" text-anchor="middle">วนกลับ</text>
</svg>
</div>

> โครงเดิมเป๊ะ — สิ่งใหม่ชุดบทเรียนนี้อยู่ใน `record()` (จังหวะ 3): เพิ่ม "นับสมดุล" ทับการอ่าน-เขียนแบบ บทเรียน 2.1–2.2 นี่คือจุดที่คุณจะเติมโค้ด

---

# โครงของไฟล์ s11_dataset.py

ทั้งไฟล์อ่านเป็นประโยคเดียว: **"เลือกป้าย → อ่าน IMU เป็นชุด → เขียนลง CSV → นับจำนวนต่อคลาส → บอกว่าคลาสไหนยังน้อย → พอครบทุกคลาสถึงเป้า = dataset พร้อม"**

<div style="text-align:center;margin:6px 0">
<svg width="920" height="210" viewBox="0 0 920 210" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arS11" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g font-size="14" text-anchor="middle">
    <rect x="14" y="24" width="180" height="54" rx="10" fill="#cfd8dc" stroke="#607d8b" stroke-width="2"/>
    <text x="104" y="47" font-weight="700" fill="#455a64">แตะปุ่ม label</text>
    <text x="104" y="66" font-size="11" fill="#999">idle/circle/shaking</text>
    <rect x="234" y="24" width="180" height="54" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="324" y="47" font-weight="700" fill="#1565c0">อ่าน IMU</text>
    <text x="324" y="66" font-size="11" fill="#999">ช่อง 1 · motion()</text>
    <rect x="454" y="24" width="180" height="54" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="544" y="47" font-weight="700" fill="#e65100">เขียน CSV</text>
    <text x="544" y="66" font-size="11" fill="#999">ช่อง 2 · f.write</text>
    <rect x="674" y="24" width="180" height="54" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="764" y="47" font-weight="700" fill="#2e7d32">นับสมดุล</text>
    <text x="764" y="66" font-size="11" fill="#999">ช่อง 3 · counts</text>
    <rect x="454" y="140" width="200" height="58" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
    <text x="554" y="164" font-weight="700" fill="#6a1b9a">นำทางให้สมดุล</text>
    <text x="554" y="182" font-size="11" fill="#999">ช่อง 4 · คลาสน้อยสุด</text>
  </g>
  <line x1="194" y1="51" x2="232" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS11)"/>
  <line x1="414" y1="51" x2="452" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS11)"/>
  <line x1="634" y1="51" x2="672" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS11)"/>
  <path d="M764,78 C764,120 554,110 554,138" fill="none" stroke="#6a1b9a" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arS11)"/>
  <text x="700" y="112" font-size="12" fill="#6a1b9a">แล้วบอกผู้ใช้</text>
  <text x="470" y="206" font-size="11" fill="#888" text-anchor="middle">ช่อง 1–4 = 4 จุดที่คุณเติมในไฟล์ฝึก · หัวใจชุดบทเรียนนี้คือช่อง 3–4 (การเฝ้าสมดุล)</text>
</svg>
</div>

> ตัวเลขช่อง (1–4) ชี้จุดที่ต้องเติม — ช่อง 1–2 คือ "อ่าน+เขียน" ที่ยกมาจาก บทเรียน 2.1–2.2 · ช่อง 3–4 คือ **สมองใหม่ของชุดบทเรียนนี้**: การเฝ้า class balance

---

# ไล่โค้ด (1) — อ่าน IMU หนึ่ง sample

**ช่องเติมที่ 1**: ในลูปเก็บ อ่านค่า IMU 6 แกนมาเก็บในตัวแปร 6 ตัว:

```python
def record(label):
    with open(PATH, "a") as f:
        for _ in range(BURST):          # BURST=200 sample ต่อการกดหนึ่งครั้ง
            # เติม: อ่าน IMU 6 แกน -> ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
            ax = ay = az = gx = gy = gz = 0.0
            pass
            f.write(...)                 # (ช่อง 2)
            time.sleep_ms(RATE_MS)       # 20 ms = 50 Hz
```

- แทน `pass` ด้วย `ax, ay, az, gx, gy, gz = sensors.bmi270.motion()` — อ่าน 6 ค่าในบรรทัดเดียว
- ถ้าลืมเติม: ทุกบรรทัดใน CSV จะเป็น `0.0` หมด (ค่าเริ่มต้น) — dataset ไม่มีข้อมูลจริง train ไม่ได้

> อ่านที่ `50 Hz` (ทุก 20 ms) เพราะโมเดลบนบอร์ดกินอัตรานี้ — ถ้าเก็บที่อัตราอื่น ท่าเดียวกันจะ "ยืด/หด" ในหน้าต่าง โมเดลจะสับสน

---

# ไล่โค้ด (2) — เขียนหนึ่งบรรทัด CSV

**ช่องเติมที่ 2**: เขียน sample ที่อ่านได้เป็นหนึ่งบรรทัด โดยขึ้นต้นด้วยป้าย:

```python
            # เติม: เขียนบรรทัด "label,ax,ay,az,gx,gy,gz" ลงไฟล์
            #   f.write("%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n"
            #           % (label, ax, ay, az, gx, gy, gz))
            pass
```

- ลำดับคอลัมน์ต้องเป็น `label,ax,ay,az,gx,gy,gz` เป๊ะ — ตรงกับ `CHANNELS` ใน [`dataset_tools.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/dataset_tools.py) ไม่งั้น `load_csv()` อ่านผิดช่อง
- `%.4f` = ทศนิยม 4 ตำแหน่ง พอสำหรับ IMU และไม่ทำให้ไฟล์ใหญ่เกิน

> ป้าย (`label`) มาก่อนเสมอ — [`dataset_tools.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/dataset_tools.py) ใช้ `CLASSES.index(row["label"])` แปลงชื่อคลาสเป็นตัวเลข ถ้าสะกดป้ายผิด (เช่น `Idle` ตัวใหญ่) มันจะหาไม่เจอแล้ว error

---

# ไล่โค้ด (3) — นับสมดุลต่อคลาส

**ช่องเติมที่ 3**: หลังเขียนครบชุด บวกจำนวนที่เก็บเข้าตัวนับของคลาสนั้น — นี่คือหัวใจ "dataset engineering" ที่ต่างจาก บทเรียน 2.1–2.2:

```python
    # (จบลูปเขียนไฟล์แล้ว)
    # เติม: บวกจำนวน sample ของคลาสนี้ -> counts[label] += BURST
    pass
    refresh_balance()      # อัปเดตแถบสมดุลบนจอ (ให้ไว้แล้ว)
```

- `counts` เป็น dict `{"idle":0, "circle":0, "shaking":0}` เก็บจำนวนสะสมต่อคลาส
- แทน `pass` ด้วย `counts[label] += BURST` — ทุกครั้งที่เก็บครบชุด ตัวนับของคลาสนั้นเพิ่ม
- ถ้าลืมเติม: แถบสมดุลไม่ขยับ คุณจะไม่รู้เลยว่าเก็บคลาสไหนไปเท่าไร — เก็บแบบตาบอด

> การนับต่อคลาสคือสิ่งที่ทำให้เราเก็บ "อย่างมีสติ" — เห็นตัวเลขจริงว่าคลาสไหนน้อย แล้วเก็บเพิ่มให้สมดุล ไม่ใช่เดา

---

# ไล่โค้ด (4) — นำทางให้สมดุล

**ช่องเติมที่ 4**: หาคลาสที่เก็บได้ **น้อยที่สุด** ตอนนี้ แล้วบอกผู้ใช้ให้ไปเก็บคลาสนั้นเพิ่ม:

```python
def refresh_balance():
    for c in CLASSES:                      # อัปเดตแถบต่อคลาส (ให้ไว้แล้ว)
        bars[c].value(min(counts[c], TARGET))
    # เติม: หาคลาสที่มี sample น้อยสุด -> fewest = min(counts, key=counts.get)
    fewest = CLASSES[0]
    pass
    if counts[fewest] < TARGET:
        hint.text("เก็บ '%s' เพิ่ม (น้อยสุดตอนนี้)" % fewest)
    else:
        hint.text("ครบทุกคลาสถึงเป้า — dataset พร้อม split!")
```

- แทน `pass` ด้วย `fewest = min(counts, key=counts.get)` — คืน **ชื่อคลาส** ที่ค่าน้อยสุดใน dict
- `min(counts, key=counts.get)` วนคีย์ทั้งหมด เทียบด้วยค่า (`counts.get`) แล้วคืนคีย์ที่ค่าน้อยสุด
- ถ้าลืมเติม: คำแนะนำจะชี้ `idle` ตลอด (ค่าเริ่มต้น) — นำทางผิด เก็บไม่สมดุล

> นี่คือความต่างที่จับต้องได้ระหว่าง "logger" (บทเรียน 2.1–2.2) กับ "dataset engineering" (บทเรียน 5.1–5.2) — โปรแกรมช่วยคุณ **ตัดสินใจว่าจะเก็บอะไรต่อ** เพื่อให้ผลลัพธ์สมดุล

---

# หน้าตาจอตอนเก็บข้อมูล — ลองใน Emulator ก่อน

ก่อนลงบอร์ดจริง เปิด **BENTO Edge AI Emulator** ดูหน้าตาโปรแกรมเก็บข้อมูลได้ก่อน — เห็นค่า IMU 6 แกนสดๆ และปุ่ม label ทำงานเหมือนบนบอร์ด

<div style="text-align:center;margin:6px 0">

![จอ BENTO Emulator ขณะรันแดชบอร์ด IMU: ค่า gx gy gz จากตัวจำลองและแถบขนาดความเร่ง w:680](../../assets/img/imu_dashboard.png)

</div>

จอ BENTO Emulator ขณะรันแดชบอร์ด IMU (ตัวอย่าง 01) — ค่าที่เห็นมาจากตัวจำลอง IMU ตัวเดียวกับที่ [`s11_dataset.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l02-dataset-lab/practice/s11_dataset.py) อ่าน พอรันโปรแกรมเก็บข้อมูล จอจะมีปุ่ม label และแถบสมดุลต่อคลาสแทน

- ขยับบอร์ด (หรือลาก emulator) แล้วดูค่าเปลี่ยน = ยืนยันว่า `sensors.bmi270.motion()` ทำงานก่อนเก็บจริง
- จอนี้ช่วยซ้อม "อ่าน → เขียน → นับ" ได้โดยไม่ต้องมีบอร์ด แต่เก็บ dataset จริงต้องใช้บอร์ด เพราะต้องอ่าน IMU ของจริง

> ใช้ emulator เพื่อทำความคุ้นเคยกับหน้าจอและปุ่ม label ก่อน แล้วค่อยไปเก็บของจริงบนบอร์ด — ประหยัดเวลาลองผิดลองถูก

---

# ลงมือทำ — เติมช่องว่างทั้ง 4 จุด

เปิด [`s11_dataset.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l02-dataset-lab/practice/s11_dataset.py) ในไฟล์มี `pass` วางไว้ **4 จุด** ตรงที่ต้องเติมคำสั่งจริง:

| # | จุด | เติมด้วย | ถ้าลืม |
|---|---|---|---|
| 1 | ในลูป record | `ax, ay, az, gx, gy, gz = sensors.bmi270.motion()` | CSV เป็น 0.0 หมด |
| 2 | หลังอ่าน | `f.write("%s,%.4f,...\n" % (label, ax, ...))` | ไฟล์ว่าง / บรรทัดหาย |
| 3 | จบชุด | `counts[label] += BURST` | แถบสมดุลไม่ขยับ |
| 4 | refresh | `fewest = min(counts, key=counts.get)` | คำแนะนำชี้ผิดคลาส |

ขั้นตอน:

1. ไล่หา `# เติม:` ทีละจุด แล้วแทน `pass` ด้วยคำสั่งตามคำใบ้
2. กด **Program to Device** (บอร์ด) — ชุดบทเรียนนี้ต้องใช้ **บอร์ดจริง** เพราะต้องอ่าน IMU จริง
3. แตะปุ่มแต่ละ label ทำท่านั้นค้าง ~4 วินาที ดูแถบสมดุลขึ้นทีละคลาส เก็บให้ครบทั้ง 3 ถึงเป้า

> สี่ช่องนี้คือ "อ่าน → เขียน → นับ → นำทาง" ครบวงของการเก็บ dataset ที่สมดุล เติมครบเมื่อไร คุณได้ไฟล์ที่ train ได้จริง

---

# จาก CSV บนบอร์ด สู่ split บน PC

พอเก็บครบแล้ว คัดลอก `/gestures.csv` ออกจากบอร์ดมาที่ PC แล้วให้ [`dataset_tools.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/dataset_tools.py) ทำ 2 ขั้นสุดท้าย (window + split):

```python
import dataset_tools as dt
s, l = dt.load_csv("data/gestures.csv")      # อ่าน CSV ของบอร์ด
X, y = dt.make_windows(s, l)                  # ตัดเป็นหน้าต่าง 50 sample
(Xtr,ytr),(Xva,yva),(Xte,yte) = dt.split(X, y)  # แบ่ง train/val/test
(Xtr,Xva,Xte),(mean,std) = dt.normalize(Xtr, Xva, Xte)  # fit บน train เท่านั้น
print("train", Xtr.shape, "val", Xva.shape, "test", Xte.shape)
```

- ลำดับสำคัญ: **split ก่อน แล้วค่อย normalize** — ถ้า normalize ก่อน split จะเกิด leakage (test รั่ว)
- ผลลัพธ์คือ 3 กองที่พร้อมป้อน [`train.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/train.py) ในบทเรียน 5.3–5.5 — dataset ที่ "จบงานเตรียม" แล้ว

> สังเกตว่าโค้ด PC สั้นมาก เพราะงานหนัก (เก็บให้สมดุล ติดป้ายถูก) ทำเสร็จตั้งแต่ฝั่งบอร์ดแล้ว — dataset ที่ดีทำให้ขั้นต่อไปง่ายลงทั้งหมด

---

# ตรวจ dataset — balance + split report

ก่อนบอกว่า "พร้อม train" ตรวจสองอย่างให้ผ่านก่อน คือ **สมดุล** และ **แบ่งครบทุกคลาส**:

```python
import numpy as np
print("windows/class :", np.bincount(y))                 # ควรใกล้เคียงกันทุกคลาส
for name, yy in [("train",ytr),("val",yva),("test",yte)]:
    print(name, "class counts", np.bincount(yy, minlength=3))
# train class counts [70 71 69]   ← ทุกกองมีครบ 3 คลาส สัดส่วนใกล้กัน
# val   class counts [15 15 14]
# test  class counts [15 15 14]
```

- ถ้ากองไหน **ขาดคลาส** (เช่น `test` เป็น `[20 20 0]`) แปลว่าเก็บ `shaking` น้อยเกิน — กลับไปเก็บเพิ่มบนบอร์ด
- ถ้าทุกกองมีครบ 3 คลาสและสัดส่วนใกล้กัน = ผ่าน นี่คือ **MVP ของบทเรียน 5.1–5.2**

> การตรวจนี้คือ "การสอบผ่าน" ของชุดบทเรียน — ตัวเลขต้องบอกเองว่า dataset สมดุลและแบ่งถูก ไม่ใช่แค่ "มีไฟล์"

---

# แหล่งเรียนรู้เพิ่มเติม

อยากเข้าใจ dataset / train-test split ให้ลึกขึ้น ลองดูจากแหล่งที่อธิบายดีเหล่านี้ (ลิงก์ไปต้นทาง ไม่ได้ฝังวิดีโอในสไลด์)

**วิดีโอ (ช่องการศึกษาที่น่าเชื่อถือ)**

- Machine Learning Fundamentals: Cross Validation — ช่อง StatQuest with Josh Starmer: https://www.youtube.com/@statquest
- Neural Networks (ชุด intuition ว่าโมเดลเรียนจากข้อมูลยังไง) — ช่อง 3Blue1Brown: https://www.youtube.com/@3blue1brown
- Data, bias และ training set — ช่อง Computerphile: https://www.youtube.com/@Computerphile

**บทความ / เอกสารอ้างอิง (ภาพ + คำอธิบาย)**

- Training, validation, and test data sets — บทความ Wikipedia: https://en.wikipedia.org/wiki/Training,_validation,_and_test_data_sets (ที่มา: Wikipedia, CC BY-SA)
- Stratified sampling — บทความ Wikipedia: https://en.wikipedia.org/wiki/Stratified_sampling (ที่มา: Wikipedia, CC BY-SA)
- `train_test_split` — เอกสารทางการ scikit-learn: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html (ที่มา: scikit-learn docs, BSD-3-Clause)

> วิดีโอ/ภาพภายนอกเป็นของเจ้าของต้นฉบับ ใช้เพื่อการศึกษา อ้างอิงลิงก์ต้นทาง

---

# ชัยชนะที่เห็นได้ + MVP ของชุดบทเรียนนี้

<div style="text-align:center;margin:14px 0">
<div style="display:inline-block;background:#e8f5e9;border:2px solid #2e7d32;border-radius:22px;padding:10px 22px;color:#2e7d32;font-weight:700;font-size:1.05em">
ชัยชนะที่เห็นได้ของชุดบทเรียนนี้ · ไฟล์ gestures.csv 3 คลาสสมดุล แบ่ง train/val/test ครบ — dataset ที่ "train ได้จริง"
</div>
</div>

**MVP ของบทเรียน 5.1–5.2 (เกณฑ์ผ่านของชุดบทเรียน):** คุณเก็บ dataset จากบอร์ดที่ **สะอาด · สมดุล · แบ่งแล้ว** — ทุกกอง (train/val/test) มีครบ 3 คลาส สัดส่วนใกล้เคียงกัน

- เก็บบน **บอร์ดจริง** (ต้องอ่าน IMU จริง) แล้ว split บน **PC** ด้วย [`dataset_tools.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/dataset_tools.py)
- อธิบายได้ว่าทำไมต้อง balance · ทำไมต้อง 3 กอง · ทำไม normalize ต้อง fit บน train เท่านั้น

> "dataset พร้อม" ไม่ใช่แค่ "มีไฟล์ CSV" — คุณต้องชี้ตัวเลข `np.bincount` ให้เห็นว่าสมดุลจริง และเล่ากฎ no-leakage ได้

---

# บันไดช่วยเหลือ — ใบ้ → เริ่มจากโครง → เฉลย → ฉบับเต็ม

ถ้าติด ให้ไต่บันไดนี้ทีละขั้น อย่าเพิ่งกระโดดไปดูเฉลย เพราะของจะเข้าหัวตอนที่คุณพยายามเองก่อน:

- **ใบ้** — คำใบ้อยู่ในคอมเมนต์ `# เติม:` ทั้ง 4 จุดในไฟล์ฝึก + ตารางหน้าที่แล้ว บอกว่าแต่ละช่องเติมอะไร
- **เริ่มจากโครง** — [`s11_dataset.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l02-dataset-lab/practice/s11_dataset.py) มีโครงครบทั้งไฟล์ (UI + ลูป + refresh_balance) เหลือแค่ 4 บรรทัดให้เติม
- **เฉลย** — [`s11_dataset.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l02-dataset-lab/solution/s11_dataset.py) เติมครบพร้อมคอมเมนต์อธิบายทุกช่อง (อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์เอง)
- **ฉบับเต็ม** — [`s11_dataset_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l02-dataset-lab/examples/s11_dataset_full.py) ฉบับขัดเรียบร้อย: เพิ่มการเตือนคลาสไม่สมดุล + สรุปสัดส่วนตอนออก + ปุ่มล้างไฟล์

> ลองเขียนเองให้สุดก่อนนะ ถ้าติดจริงๆ ค่อยเปิดเฉลยดูทีละช่อง แล้วกลับมาพิมพ์เอง — เดี๋ยวเราค่อย ๆ แกะไปด้วยกัน

---

# เชื่อมโยงรากฐาน — วันนี้เราแตะอะไรไปบ้าง

การเก็บ dataset หนึ่งชุดซ่อนแนวคิดของสาย ML ที่จะใช้ไปตลอดคอร์ส:

**ฝั่ง dataset engineering**
- **class balance** — จำนวนต่อคลาสต้องใกล้กัน ไม่งั้นโมเดล "ขี้เกียจเดา"
- **train/val/test split** — กัน test ไว้สอบจริง แตะครั้งเดียว
- **stratified** — ทุกกองมีครบทุกคลาส สัดส่วนเท่ากัน
- **no leakage** — fit สถิติบน train เท่านั้น สถิติ test ห้ามรั่วเข้า train

**ฝั่ง MicroPython / โครงโปรแกรม**
- **MPY → CSV** — `sensors.bmi270.motion()` + `f.write()` เก็บข้อมูลลงไฟล์บนบอร์ด
- **โครงร่วม** — import → สร้างครั้งเดียว → ลูป → `ui.poll` (เหมือนทุกบทเรียน)
- **เก็บอย่างมีสติ** — เฝ้า `counts` ต่อคลาสระหว่างเก็บ ไม่ใช่เก็บดะ

> ทั้งหมดนี้ยืนบนไฟล์ CSV ธรรมดา — พลังของการเข้าใจ dataset คือ ตอน train แม่นหรือพัง คุณจะรู้ว่าย้อนไปแก้ที่ข้อมูล ไม่ใช่ไล่จูนโมเดลอย่างเดียว

---

# ใช้จริงที่ไหน — dataset engineering ในโลกจริง

ทุกทีมที่ทำ Edge AI จริงใช้เวลากับการเตรียมข้อมูลมากกว่าการ train โมเดลเสียอีก — งานที่เราทำวันนี้คือหัวใจของสายอาชีพ ML:

<div style="text-align:center;margin:6px 0">
<svg width="880" height="210" viewBox="0 0 880 210" font-family="DejaVu Sans, sans-serif">
  <rect x="12" y="10" width="420" height="92" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="28" y="34" font-size="13" font-weight="700" fill="#1565c0">สายการผลิต — เก็บ dataset เสียง/สั่น</text>
  <text x="28" y="56" font-size="11" fill="#555">ตรวจเครื่องจักรผิดปกติ ต้องเก็บทั้ง "ปกติ/เสีย"</text>
  <text x="28" y="76" font-size="11" fill="#555">ให้สมดุล — เสียงเสียหายากกว่า ต้องตั้งใจเก็บ</text>
  <text x="28" y="94" font-size="11" fill="#888">คือปัญหา class balance เดียวกับวันนี้</text>
  <rect x="448" y="10" width="420" height="92" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="464" y="34" font-size="13" font-weight="700" fill="#2e7d32">อุปกรณ์สวมใส่ — ท่าทาง/สุขภาพ</text>
  <text x="464" y="56" font-size="11" fill="#555">เก็บท่าเดิน/วิ่ง/ล้ม จากผู้ใช้หลายคน</text>
  <text x="464" y="76" font-size="11" fill="#555">split ตาม "คน" ไม่ใช่ตาม sample กัน leakage</text>
  <text x="464" y="94" font-size="11" fill="#888">คือกฎ no-leakage เดียวกับวันนี้</text>
  <rect x="12" y="114" width="420" height="86" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="28" y="138" font-size="13" font-weight="700" fill="#e65100">คำพูด/สั่งงานเสียง — label ยาก</text>
  <text x="28" y="160" font-size="11" fill="#555">ต้องมีคนฟังแล้วติดป้ายทุกคลิป (งานหนัก)</text>
  <text x="28" y="180" font-size="11" fill="#555">ป้ายผิดแม้ไม่กี่ % ก็ทำโมเดลแย่ลงชัดเจน</text>
  <rect x="448" y="114" width="420" height="86" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="464" y="138" font-size="13" font-weight="700" fill="#6a1b9a">ร่วมกัน — "garbage in, garbage out"</text>
  <text x="464" y="160" font-size="11" fill="#555">โมเดลแม่นได้แค่ที่ข้อมูลดี — ไม่มีทางลัด</text>
  <text x="464" y="180" font-size="11" fill="#555">เตรียมข้อมูลดี = ครึ่งหนึ่งของงานเสร็จแล้ว</text>
</svg>
</div>

> ที่เราเฝ้าแถบสมดุลกับกันข้อมูลรั่ววันนี้ ไม่ใช่พิธีกรรมในห้องเรียน — มันคือสิ่งที่ทีม ML มืออาชีพทำจริงทุกวัน เพราะ "ข้อมูลขยะเข้า ก็ได้โมเดลขยะออก"

---

# งานทำเอง + สรุปบทเรียน

**งานทำเอง (ท้ายบทเรียน):**

1. เติม [`s11_dataset.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l02-dataset-lab/practice/s11_dataset.py) ให้ครบทั้ง 4 ช่อง เก็บ dataset จริงบนบอร์ด — ทั้ง 3 คลาสถึงเป้า
2. คัดลอก `gestures.csv` มา PC แล้วรัน split ด้วย [`dataset_tools.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/dataset_tools.py) พิมพ์ `np.bincount` ของทั้ง 3 กอง
3. ทดลอง **เก็บให้ไม่สมดุล** ตั้งใจ (เช่น `idle` เยอะกว่าเพื่อน 3 เท่า) แล้วอธิบายว่าสัดส่วนใน train/val/test เปลี่ยนยังไง

ใบ้ข้อ 3 — เพราะ split เป็น stratified สัดส่วนที่ไม่สมดุลจะ **ติดไปทั้ง 3 กอง** เท่าๆ กัน ไม่ได้หายไปเอง ปัญหาต้องแก้ที่ "ตอนเก็บ" ไม่ใช่ตอน split

**วันนี้เราได้:** เข้าใจว่า dataset ที่ดีคืออะไร · เก็บ IMU ที่ติดป้ายลง CSV บนบอร์ด · เฝ้า class balance ระหว่างเก็บ · แบ่ง train/val/test แบบ stratified โดยไม่ให้ข้อมูลรั่ว

> ชุดบทเรียนถัดไป (บทเรียน 5.3–5.5) เราจะเอา dataset นี้ไป **train เป็นโมเดลจริง** ใน Docker ด้วย TensorFlow แล้วส่งออกเป็น `.tflite` — โมเดลตัวแรกที่เป็นของเราเองทั้งตัว เจอกันครับ
