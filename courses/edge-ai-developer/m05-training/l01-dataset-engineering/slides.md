---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 5.1 — วิศวกรรมชุดข้อมูล: สมดุลคลาส หน้าต่าง และการแบ่ง train/val/test"
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

# บทเรียน 5.1 — วิศวกรรมชุดข้อมูล: สมดุลคลาส หน้าต่าง และการแบ่ง train/val/test
## เก็บ · ติดป้าย · แบ่ง

**โมดูล 5 — ฝึกโมเดลและนำไปใช้หลายเป้าหมาย**

**เปิด โมดูล 5 — Training (โต๊ะฝึกโมเดล)**

> คาถาประจำบทเรียน: **"โมเดลจะแม่นแค่ไหน ตัดสินกันตั้งแต่ก่อนเขียนโค้ด train บรรทัดแรก — ที่ dataset ที่สมดุลและแบ่งถูก"**

MicroPython บนบอร์ด BENTO เก็บข้อมูล → CSV → แบ่ง train/val/test บน PC

---

# เปิดบทเรียนด้วยของจริงก่อน

ยังใช้แนว **กลับด้าน** เหมือนเดิม — แต่รอบนี้เราจะรัน "ท่อ (pipeline) เตรียมข้อมูล" ที่ทำงานได้จริงก่อนด้วยข้อมูลปลอม แล้วค่อยแกะว่าอะไรทำให้ dataset "ดีพอจะ train" จริง

<div style="text-align:center;margin:10px 0">
<svg width="820" height="150" viewBox="0 0 820 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arOpen11" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="40" width="180" height="70" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="104" y="72" font-size="15" font-weight="700" fill="#2e7d32" text-anchor="middle">รันท่อจริงก่อน</text>
  <text x="104" y="94" font-size="12" fill="#555" text-anchor="middle">synthesize + split</text>
  <rect x="234" y="40" width="180" height="70" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="324" y="72" font-size="15" font-weight="700" fill="#1565c0" text-anchor="middle">แกะว่าดีเพราะอะไร</text>
  <text x="324" y="94" font-size="12" fill="#555" text-anchor="middle">balance · split · leak</text>
  <rect x="454" y="40" width="180" height="70" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="544" y="72" font-size="15" font-weight="700" fill="#e65100" text-anchor="middle">เก็บของจริงเอง</text>
  <text x="544" y="94" font-size="12" fill="#555" text-anchor="middle">MPY → CSV บนบอร์ด</text>
  <rect x="674" y="40" width="132" height="70" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="740" y="72" font-size="15" font-weight="700" fill="#6a1b9a" text-anchor="middle">อยากสร้างต่อ</text>
  <text x="740" y="94" font-size="12" fill="#555" text-anchor="middle">5.3–5.5 train.py</text>
  <line x1="194" y1="75" x2="230" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen11)"/>
  <line x1="414" y1="75" x2="450" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen11)"/>
  <line x1="634" y1="75" x2="670" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen11)"/>
</svg>
</div>

นี่คือขั้น **Investigate → Modify** ของ PRIMM: เห็นท่อทั้งเส้นทำงานด้วยข้อมูล synthesize ก่อน (Run) แล้วเปิดฝาดูว่าอะไรทำให้ dataset ใช้ได้ (Investigate) จากนั้นเปลี่ยนข้อมูลปลอมเป็นข้อมูลจริงที่เราเก็บเอง (Modify)

> ชุดบทเรียนก่อน ๆ เราเรียก "โมเดลที่ฝึกมาแล้ว" มาใช้ ชุดบทเรียนนี้เราเริ่มทำสิ่งที่วิศวกรทำก่อนการ train เสมอ — เตรียมข้อมูล ซึ่งเป็นงานที่กินเวลาจริงมากที่สุดในสาย ML

---

# เป้าหมายของชุดบทเรียนนี้

จบชุดบทเรียนนี้เราจะเดินครบ 4 เรื่อง แล้วปิดท้ายด้วย dataset ที่พร้อม train จริง:

1. **dataset คืออะไร** — CSV ของ sample ที่ติดป้าย (label) แล้ว และเส้นทาง capture → label → window → split
2. **class balance** — ทำไมจำนวน sample ของแต่ละคลาสควรใกล้เคียงกัน และเก็บให้สมดุลยังไง
3. **train / val / test split** — ทำไมต้องแบ่ง 3 กอง แบ่งแบบ stratified และกฎ "ห้ามให้ข้อมูลรั่ว (no leakage)"
4. **MPY → CSV** — เก็บข้อมูล IMU ที่ติดป้ายลงไฟล์บนบอร์ดด้วย `sensors.bmi270.motion()`
5. ลงมือ: เติม [`s11_dataset.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l02-dataset-lab/practice/s11_dataset.py) เก็บ dataset ที่ **สมดุล** แล้วส่งต่อให้ [`dataset_tools.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/dataset_tools.py) แบ่งบน PC

ปลายทางของวันนี้: ไฟล์ `gestures.csv` ที่มี 3 คลาสสมดุล พร้อมแบ่ง train/val/test — dataset ที่ "train ได้จริง"

> ชุดบทเรียนถัดไป (บทเรียน 5.3–5.5) เราจะเอา dataset นี้ไป train เป็นโมเดลจริงใน Docker — วันนี้คือการปูฐานให้โมเดลนั้นแม่น

---

# ชุดบทเรียนนี้อยู่ตรงไหนของคอร์ส

บทเรียน 5.1–5.2 เป็นบทเรียน **เปิด โมดูล 5 (Training)** — เราหยุด "ใช้" โมเดลสำเร็จ แล้วเริ่ม "สร้าง" โมเดลของเราเอง โดยเริ่มจากสิ่งที่มาก่อนการ train เสมอ

<div style="text-align:center;margin:8px 0">
<svg width="820" height="120" viewBox="0 0 820 120" font-family="DejaVu Sans, sans-serif">
  <line x1="60" y1="60" x2="760" y2="60" stroke="#cfd8dc" stroke-width="3"/>
  <circle cx="150" cy="60" r="9" fill="#1565c0"/>
  <text x="150" y="40" font-size="12" font-weight="700" fill="#1565c0" text-anchor="middle">โมดูล 2 · DAQ</text>
  <text x="150" y="86" font-size="11" fill="#777" text-anchor="middle">เก็บ sensor ลง CSV</text>
  <circle cx="360" cy="60" r="9" fill="#ef6c00"/>
  <text x="360" y="40" font-size="12" font-weight="700" fill="#e65100" text-anchor="middle">4.5–4.6 · Analysis</text>
  <text x="360" y="86" font-size="11" fill="#777" text-anchor="middle">windowing / feature</text>
  <circle cx="570" cy="60" r="11" fill="#6a1b9a"/>
  <text x="570" y="38" font-size="12" font-weight="700" fill="#6a1b9a" text-anchor="middle">5.1–5.2 (วันนี้)</text>
  <text x="570" y="86" font-size="11" fill="#777" text-anchor="middle">dataset engineering</text>
  <circle cx="720" cy="60" r="9" fill="#00838f"/>
  <text x="720" y="40" font-size="12" font-weight="700" fill="#00838f" text-anchor="middle">5.3–5.5+</text>
  <text x="720" y="86" font-size="11" fill="#777" text-anchor="middle">train → deploy</text>
</svg>
</div>

- **โมดูล 2** สอนวิธี "เก็บข้อมูล sensor ลง CSV" ([`s04_daq_logger.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m02-daq/l02-daq-logger-lab/practice/s04_daq_logger.py)) — เราจะต่อยอดจากตรงนั้น
- **บทเรียน 4.5–4.6** สอนว่าโมเดลเห็น "หน้าต่าง (window)" ไม่ใช่ sample เดี่ยว — แนวคิดนั้นกลับมาใช้ตอนแบ่งข้อมูล
- **บทเรียน 5.1–5.2 วันนี้** รวมสามอย่าง: เก็บให้สมดุล + ติดป้ายถูก + แบ่งเป็น train/val/test — แล้ว บทเรียน 5.3–5.5 จึงเอาไป train

> "กลับด้าน" ยังทำงาน: เห็นท่อสำเร็จก่อน (synthetic) แล้วย้อนเข้าใจ — พอถึง บทเรียน 5.3–5.9 คุณจะ train โมเดลตัวเองบน dataset ที่เก็บวันนี้

---

# ทบทวนเร็ว — จาก บทเรียน 2.1–2.2 DAQ logger

บทเรียน 2.1–2.2 เราเขียน [`s04_daq_logger.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m02-daq/l02-daq-logger-lab/practice/s04_daq_logger.py) ที่อ่าน IMU แล้วเขียนลง CSV — ชุดบทเรียนนี้ยืนบนโครงเดิมนั้นเป๊ะ แค่ยกระดับจาก "เก็บข้อมูล" เป็น "เก็บ dataset ที่ดีพอจะ train"

```python
# หัวใจของ s04 — อ่าน sample แล้วเขียนลงไฟล์ (เราจะต่อยอดจากตรงนี้)
with open(PATH, "a") as f:
    for _ in range(BURST):
        ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
        f.write("%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n"
                % (label, ax, ay, az, gx, gy, gz))
        time.sleep_ms(RATE_MS)     # 20 ms = 50 Hz
```

- บทเรียน 2.1–2.2 ตอบคำถาม "เก็บข้อมูลลงไฟล์ยังไง" — ชุดบทเรียนนี้ตอบ "เก็บยังไงให้ **สมดุล + แบ่งได้ + ไม่รั่ว**"
- ความต่าง: บทเรียน 2.1–2.2 เก็บดะ · บทเรียน 5.1–5.2 เก็บโดยเฝ้าดู **class balance** ตลอด แล้วส่งต่อให้ split บน PC

> ถ้ายังไม่แม่นเรื่องเขียน CSV บนบอร์ด เปิด [`s04_daq_logger.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m02-daq/l02-daq-logger-lab/examples/s04_daq_logger.py) อ่านทวนก่อน — ชุดบทเรียนนี้เพิ่มแค่ "สมองของการเตรียมข้อมูล" ทับลงไป

---

# dataset คืออะไร

**dataset** ในงานของเราคือไฟล์ CSV ธรรมดา หนึ่งบรรทัดต่อหนึ่ง sample โดยมี **ป้าย (label)** บอกว่าตอนเก็บ sample นั้นเรากำลังทำท่าอะไร:

<div style="text-align:center;margin:6px 0">
<svg width="880" height="180" viewBox="0 0 880 180" font-family="DejaVu Sans, sans-serif">
  <rect x="20" y="14" width="840" height="152" rx="12" fill="#f7f9fb" stroke="#607d8b" stroke-width="2"/>
  <text x="40" y="40" font-size="14" font-weight="700" fill="#455a64">gestures.csv  —  หนึ่งบรรทัด = หนึ่ง sample ที่ติดป้ายแล้ว</text>
  <g font-size="12" font-family="monospace">
    <rect x="40" y="52" width="800" height="26" rx="5" fill="#eceff1" stroke="#607d8b"/>
    <text x="52" y="70" fill="#455a64" font-weight="700">label,ax,ay,az,gx,gy,gz</text>
    <text x="560" y="70" font-size="11" fill="#888" font-family="DejaVu Sans">← หัวตาราง (header)</text>
    <rect x="40" y="82" width="800" height="24" rx="5" fill="#e3f2fd" stroke="#1565c0"/>
    <text x="52" y="99" fill="#1565c0">idle,0.006,-0.007,9.842,0.05,-0.27,0.18</text>
    <rect x="40" y="110" width="800" height="24" rx="5" fill="#e8f5e9" stroke="#2e7d32"/>
    <text x="52" y="127" fill="#2e7d32">circle,2.01,1.98,9.91,40.2,39.7,0.4</text>
  </g>
  <text x="450" y="156" font-size="11" fill="#888" text-anchor="middle">ป้ายคือ "คำตอบที่ถูก" ที่เราสอนโมเดล · 6 ช่องหลังคือค่าจาก IMU (accel 3 + gyro 3)</text>
</svg>
</div>

- 6 คอลัมน์หลัง (`ax,ay,az,gx,gy,gz`) คือค่าจาก `sensors.bmi270.motion()` — เหมือนที่โมเดล Motion บนบอร์ดกินเป๊ะ
- คอลัมน์ `label` คือ "เฉลย" ที่มนุษย์ติดให้ ตอน train โมเดลจะเรียนความสัมพันธ์ "ค่า 6 ช่องนี้ → ป้ายนี้"

> เราจงใจใช้ 3 คลาสเดียวกับโมเดล Motion บนบอร์ด (`idle / circle / shaking`) เพื่อจะเทียบโมเดลที่เรา train เอง กับของสำเร็จได้ในชุดบทเรียนหลัง

---

# ท่อเตรียมข้อมูล — 4 ขั้นก่อนถึง train

dataset ดิบยัง train ไม่ได้ทันที ต้องผ่าน 4 ขั้น กว่าจะกลายเป็นสิ่งที่โมเดลเรียนได้ — ชุดบทเรียนนี้เราทำครบทั้งเส้น:

<div style="text-align:center;margin:6px 0">
<svg width="920" height="190" viewBox="0 0 920 190" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arPipe" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g text-anchor="middle">
    <rect x="10" y="56" width="170" height="76" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="95" y="84" font-size="14" font-weight="700" fill="#1565c0">1 · capture</text>
    <text x="95" y="104" font-size="11" fill="#555">อ่าน IMU 50 Hz</text>
    <text x="95" y="120" font-size="10" fill="#888">บนบอร์ด (MPY)</text>
    <rect x="196" y="56" width="170" height="76" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="281" y="84" font-size="14" font-weight="700" fill="#2e7d32">2 · label</text>
    <text x="281" y="104" font-size="11" fill="#555">ติดป้ายแต่ละท่า</text>
    <text x="281" y="120" font-size="10" fill="#888">idle/circle/shaking</text>
    <rect x="382" y="56" width="170" height="76" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="467" y="84" font-size="14" font-weight="700" fill="#e65100">3 · window</text>
    <text x="467" y="104" font-size="11" fill="#555">ตัดเป็นหน้าต่าง</text>
    <text x="467" y="120" font-size="10" fill="#888">50 sample/หน้าต่าง</text>
    <rect x="568" y="56" width="170" height="76" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
    <text x="653" y="84" font-size="14" font-weight="700" fill="#6a1b9a">4 · split</text>
    <text x="653" y="104" font-size="11" fill="#555">แบ่ง train/val/test</text>
    <text x="653" y="120" font-size="10" fill="#888">บน PC</text>
    <rect x="754" y="56" width="156" height="76" rx="12" fill="#e0f7fa" stroke="#00838f" stroke-width="2"/>
    <text x="832" y="84" font-size="14" font-weight="700" fill="#00838f">train</text>
    <text x="832" y="104" font-size="11" fill="#555">5.3–5.5 (Docker)</text>
    <text x="832" y="120" font-size="10" fill="#888">→ .tflite</text>
  </g>
  <line x1="180" y1="94" x2="194" y2="94" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arPipe)"/>
  <line x1="366" y1="94" x2="380" y2="94" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arPipe)"/>
  <line x1="552" y1="94" x2="566" y2="94" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arPipe)"/>
  <line x1="738" y1="94" x2="752" y2="94" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arPipe)"/>
  <text x="235" y="30" font-size="12" font-weight="700" fill="#455a64" text-anchor="middle">บนบอร์ด (s11_dataset.py)</text>
  <text x="700" y="30" font-size="12" font-weight="700" fill="#455a64" text-anchor="middle">บน PC (dataset_tools.py)</text>
  <text x="460" y="170" font-size="11" fill="#888" text-anchor="middle">ชุดบทเรียนนี้ทำครบขั้น 1–4 · ขั้น train เก็บไว้ 5.3–5.5</text>
</svg>
</div>

> ขั้น 1–2 (capture + label) เกิดบนบอร์ดด้วย MicroPython · ขั้น 3–4 (window + split) เกิดบน PC ด้วย [`dataset_tools.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/dataset_tools.py) — ชุดบทเรียนนี้เราแตะทั้งสองฝั่ง

---

# รันของจริงก่อน — สร้าง dataset ปลอมแล้วส่อง

ก่อนเก็บข้อมูลจริง (ที่ใช้เวลานาน) เรารันท่อทั้งเส้นด้วย **ข้อมูล synthesize** ก่อน เพื่อพิสูจน์ว่าโค้ดทำงาน แล้วเห็นว่า dataset ที่ดี "หน้าตาเป็นยังไง":

```bash
# 1) สร้าง dataset ปลอม (idle=นิ่ง, circle=หมุน, shaking=สั่นแรง)
python dataset_tools.py --synthesize --out data/gestures.csv

# 2) ส่องว่าได้อะไร — จำนวน sample, จำนวนหน้าต่าง, จำนวนต่อคลาส
python dataset_tools.py --out data/gestures.csv
# samples (3600, 6) windows (143, 50, 6) class counts [48 48 47]
```

- `class counts [48 48 47]` = จำนวนหน้าต่างของแต่ละคลาส **ใกล้เคียงกัน** → นี่คือ dataset ที่ **สมดุล**
- `windows (143, 50, 6)` = 143 หน้าต่าง แต่ละหน้าต่างมี 50 sample × 6 ช่อง — นี่คือรูปร่างที่โมเดลกิน

> เราให้ `synthesize` ไว้ตั้งแต่แรก เพื่อให้ท่อ "รันได้" ก่อนมีข้อมูลจริง — เป็นเชื้อเพลิงของการกลับด้าน: เห็นของสำเร็จก่อน แล้วค่อยเอาข้อมูลจริงมาแทน

---

# class balance — ทำไมความสมดุลถึงสำคัญ

ถ้าคลาสหนึ่งมี sample เยอะกว่าเพื่อนมาก โมเดลจะ "ขี้เกียจ" — มันเดาคลาสที่เจอบ่อยไว้ก่อนก็ถูกบ่อยแล้ว โดยไม่ต้องเรียนรู้จริง

<div style="text-align:center;margin:6px 0">
<svg width="880" height="200" viewBox="0 0 880 200" font-family="DejaVu Sans, sans-serif">
  <rect x="12" y="14" width="420" height="176" rx="12" fill="#fdecea" stroke="#c62828" stroke-width="2"/>
  <text x="222" y="38" font-size="14" font-weight="700" fill="#c62828" text-anchor="middle">ไม่สมดุล (แย่)</text>
  <rect x="40" y="120" width="70" height="50" fill="#1565c0"/><text x="75" y="186" font-size="11" fill="#555" text-anchor="middle">idle</text>
  <rect x="140" y="60" width="70" height="110" fill="#2e7d32"/><text x="175" y="186" font-size="11" fill="#555" text-anchor="middle">circle</text>
  <rect x="240" y="140" width="70" height="30" fill="#ef6c00"/><text x="275" y="186" font-size="11" fill="#555" text-anchor="middle">shaking</text>
  <text x="350" y="90" font-size="11" fill="#c62828" text-anchor="middle">โมเดลเดา</text>
  <text x="350" y="106" font-size="11" fill="#c62828" text-anchor="middle">"circle" ไว้ก่อน</text>
  <rect x="448" y="14" width="420" height="176" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="658" y="38" font-size="14" font-weight="700" fill="#2e7d32" text-anchor="middle">สมดุล (ดี)</text>
  <rect x="500" y="80" width="70" height="90" fill="#1565c0"/><text x="535" y="186" font-size="11" fill="#555" text-anchor="middle">idle</text>
  <rect x="600" y="76" width="70" height="94" fill="#2e7d32"/><text x="635" y="186" font-size="11" fill="#555" text-anchor="middle">circle</text>
  <rect x="700" y="82" width="70" height="88" fill="#ef6c00"/><text x="735" y="186" font-size="11" fill="#555" text-anchor="middle">shaking</text>
  <text x="800" y="120" font-size="11" fill="#2e7d32" text-anchor="middle">ต้องเรียน</text>
  <text x="800" y="136" font-size="11" fill="#2e7d32" text-anchor="middle">จริงทุกคลาส</text>
</svg>
</div>

- ตัวอย่างสุดโต่ง: ถ้า 95% ของข้อมูลเป็น `idle` โมเดลที่ตอบ "idle" ตลอดจะแม่น 95% บนกระดาษ แต่ใช้งานจริงไม่ได้เลย
- ทางแก้ที่ตรงที่สุด: **เก็บให้แต่ละคลาสมีจำนวนใกล้เคียงกัน** ตั้งแต่ตอนเก็บข้อมูล — นี่คือสิ่งที่ [`s11_dataset.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l02-dataset-lab/practice/s11_dataset.py) เฝ้าดูให้

> ชุดบทเรียนนี้เราจึงไม่เก็บข้อมูลแบบ "ดะ" แต่เก็บพร้อม **แถบสมดุลต่อคลาส** บนจอ ถ้าคลาสไหนน้อย โปรแกรมจะบอกให้เก็บเพิ่ม — เก็บอย่างมีสติ ไม่ใช่เก็บเยอะ

---

# windowing — โมเดลเห็น "หน้าต่าง" ไม่ใช่ sample เดี่ยว

sample เดียว (ค่า IMU ณ วินาทีหนึ่ง) บอกท่าไม่ได้ — `shaking` กับ `idle` ที่จังหวะหนึ่งอาจมีค่าเท่ากันบังเอิญ โมเดลต้องเห็น **ช่วงเวลา** ถึงจะแยกออก (นี่คือแนวคิดจาก บทเรียน 4.5–4.6 ที่กลับมาใช้)

<div style="text-align:center;margin:6px 0">
<svg width="900" height="170" viewBox="0 0 900 170" font-family="DejaVu Sans, sans-serif">
  <text x="40" y="28" font-size="12" fill="#455a64" font-weight="700">สาย sample ต่อเนื่อง (50 Hz)</text>
  <line x1="40" y1="60" x2="860" y2="60" stroke="#cfd8dc" stroke-width="2"/>
  <g>
    <rect x="60" y="44" width="240" height="34" rx="6" fill="rgba(21,101,192,.18)" stroke="#1565c0" stroke-width="2"/>
    <text x="180" y="100" font-size="11" fill="#1565c0" text-anchor="middle">หน้าต่าง 1 (WIN=50)</text>
    <rect x="180" y="90" width="240" height="34" rx="6" fill="rgba(46,125,50,.18)" stroke="#2e7d32" stroke-width="2"/>
    <text x="300" y="146" font-size="11" fill="#2e7d32" text-anchor="middle">หน้าต่าง 2 (เลื่อน HOP=25)</text>
    <rect x="300" y="44" width="240" height="34" rx="6" fill="rgba(239,108,0,.18)" stroke="#ef6c00" stroke-width="2"/>
    <text x="420" y="36" font-size="11" fill="#e65100" text-anchor="middle">หน้าต่าง 3</text>
  </g>
  <text x="450" y="168" font-size="11" fill="#888" text-anchor="middle">แต่ละหน้าต่าง = 50 sample × 6 ช่อง · เลื่อนทีละ 25 (ซ้อน 50%) · ป้ายของหน้าต่าง = ป้ายส่วนใหญ่ในนั้น</text>
</svg>
</div>

- `WIN = 50` (1 วินาทีที่ 50 Hz) คือ "ความยาวหนึ่งท่า" ที่โมเดลตัดสิน · `HOP = 25` คือเลื่อนหน้าต่างทีละครึ่ง (ได้ข้อมูลมากขึ้นจากสายเดียว)
- `make_windows()` ใน [`dataset_tools.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/dataset_tools.py) ทำขั้นนี้ให้ — และมันคือ **การจัดหน้าต่างแบบเดียวกับที่ feed บนบอร์ดทำ** ตอนอนุมานจริง

> ทำไมต้องเหมือนกันเป๊ะ? เพราะโมเดลที่ฝึกด้วยหน้าต่าง 50 sample จะทำงานถูกก็ต่อเมื่อตอนใช้จริงมันก็เห็นหน้าต่าง 50 sample เช่นกัน — "train เห็นแบบไหน ใช้จริงต้องเห็นแบบนั้น"

---

# train / val / test — ทำไมต้องแบ่ง 3 กอง

เราไม่เอาข้อมูลทั้งหมดไป train แล้ววัดความแม่นบนข้อมูลเดิม เพราะนั่นเหมือนให้ผู้เรียนดูเฉลยก่อนสอบ — ต้องกันข้อมูลไว้ "สอบจริง" ต่างหาก

<div style="text-align:center;margin:6px 0">
<svg width="900" height="170" viewBox="0 0 900 170" font-family="DejaVu Sans, sans-serif">
  <rect x="40" y="40" width="820" height="50" rx="8" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
  <rect x="40" y="40" width="574" height="50" rx="8" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="327" y="70" font-size="14" font-weight="700" fill="#1565c0" text-anchor="middle">train (70%) — โมเดลเรียนจากกองนี้</text>
  <rect x="614" y="40" width="123" height="50" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="675" y="64" font-size="12" font-weight="700" fill="#e65100" text-anchor="middle">val</text>
  <text x="675" y="80" font-size="10" fill="#888" text-anchor="middle">15%</text>
  <rect x="737" y="40" width="123" height="50" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="798" y="64" font-size="12" font-weight="700" fill="#6a1b9a" text-anchor="middle">test</text>
  <text x="798" y="80" font-size="10" fill="#888" text-anchor="middle">15%</text>
  <text x="327" y="120" font-size="11" fill="#555" text-anchor="middle">ใช้ปรับโมเดล</text>
  <text x="675" y="120" font-size="11" fill="#555" text-anchor="middle">จูนระหว่าง train</text>
  <text x="798" y="120" font-size="11" fill="#555" text-anchor="middle">สอบครั้งเดียว</text>
  <text x="450" y="150" font-size="11" fill="#888" text-anchor="middle">test = แตะครั้งเดียวตอนจบ · ถ้าแอบดู test ระหว่างจูน ตัวเลขจะโกหก</text>
</svg>
</div>

- **train** — โมเดลเรียนจากกองนี้ · **val** — ใช้เช็กระหว่างฝึกว่าเริ่ม overfit หรือยัง (จูนได้) · **test** — สอบจริง แตะครั้งเดียวตอนจบ
- `split()` ใน [`dataset_tools.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/dataset_tools.py) ทำให้ครบ 3 กอง ด้วยสัดส่วน `val=0.15, test=0.15` (ที่เหลือ 70% เป็น train)

> ทำไมต้องมี val แยกจาก test? เพราะเราจูนโมเดลโดยดู val ซ้ำๆ — val จึง "ปนเปื้อน" การตัดสินใจของเราไปแล้ว test ที่ไม่เคยแตะเลยเท่านั้นถึงบอกความแม่นจริงได้

---

# stratified split — สัดส่วนคลาสเท่ากันทุกกอง

ถ้าแบ่งแบบสุ่มดื้อๆ อาจซวยได้ว่า test ดันไม่มี `shaking` เลย — วัดความแม่นของ `shaking` ไม่ได้ ทางแก้คือแบ่งแบบ **stratified**: แยกทีละคลาสแล้วค่อยหั่น

```python
# หัวใจของ split() — แยก index ของแต่ละคลาสก่อน แล้วหั่น 70/15/15 ในแต่ละคลาส
idx = {c: rng.permutation(np.where(y == c)[0]) for c in np.unique(y)}
for c, ii in idx.items():
    n = len(ii)
    nte, nva = int(n * test), int(n * val)
    te += list(ii[:nte])            # 15% แรกของคลาสนี้ → test
    va += list(ii[nte:nte + nva])   # 15% ถัดไป → val
    tr += list(ii[nte + nva:])      # ที่เหลือ → train
```

- ผลคือทั้ง 3 กองมีสัดส่วน `idle : circle : shaking` เท่ากัน — ไม่มีคลาสไหนหายจากกองใด
- `rng.permutation` สลับก่อนหั่น เพื่อไม่ให้ลำดับการเก็บข้อมูล (เช่น เก็บ idle ทั้งหมดก่อน) มาทำให้กองเอนเอียง

> "stratified" แปลว่า "แบ่งเป็นชั้นตามคลาส" — เป็นค่าเริ่มต้นที่ควรใช้เสมอในงาน classification ที่คลาสมีความสำคัญเท่ากัน

---

# คณิตเบื้องหลัง — สมดุลคลาส กับสัดส่วน 70/15/15

สามแนวคิดที่เพิ่งดูไป เขียนเป็นสูตรสั้นๆ ได้ ช่วยให้เห็นว่า "สมดุล" กับ "แบ่ง" วัดกันด้วยตัวเลขจริง

**สัดส่วนของแต่ละคลาส (class balance)**

$$p_c \;=\; \frac{n_c}{N}, \qquad \text{สมดุลเมื่อ}\quad p_c \;\approx\; \frac{1}{K}$$

- $n_c$ = จำนวน sample (หรือหน้าต่าง) ของคลาส $c$ · $N=\sum_c n_c$ = จำนวนทั้งหมด
- $K$ = จำนวนคลาส — ชุดบทเรียนนี้ $K=3$ (`idle` / `circle` / `shaking`)
- $p_c$ = สัดส่วนของคลาส $c$ · สมดุลคือทุกคลาสได้ราว $1/3 \approx 0.33$ เท่าๆ กัน

**แบ่งเป็น 3 กอง (train / val / test)**

$$N_{\text{test}}=\lfloor 0.15\,N\rfloor,\quad N_{\text{val}}=\lfloor 0.15\,N\rfloor,\quad N_{\text{train}}=N-N_{\text{test}}-N_{\text{val}}\;\approx 0.70\,N$$

- $\lfloor\,\cdot\,\rfloor$ = ปัดลงเป็นจำนวนเต็ม (แบ่ง sample เป็นเศษไม่ได้) · $N_{\text{train}}$ รับเศษที่เหลือ เลยรวมกันได้ครบ $N$ พอดี
- **ทำไมสำคัญ:** ถ้า $p_c$ เบ้ไปคลาสเดียว โมเดลเดาคลาสนั้นก็ "แม่น" บนกระดาษโดยไม่ได้เรียนอะไร — ตรงกับสไลด์ class balance ที่เราเพิ่งดู

> อยากได้ $N_{\text{train}}:N_{\text{val}}:N_{\text{test}} = 70:15:15$ ก็คูณ $N$ ด้วย 0.15 แล้วปัดลงให้ test และ val ที่เหลือเป็น train — นี่คือสิ่งที่ `split()` ทำให้ในบรรทัด `int(n*test)`, `int(n*val)`

---

# คณิตเบื้องหลัง — stratified: แบ่งทีละคลาสให้สัดส่วนคงเดิม

การแบ่งแบบ stratified ไม่ได้หั่นทั้งกองรวด แต่หั่น **ทีละคลาส** ด้วยสัดส่วนเดียวกัน แล้วเอามารวม

$$n_{c,\text{test}}=\lfloor 0.15\,n_c\rfloor,\quad n_{c,\text{val}}=\lfloor 0.15\,n_c\rfloor,\quad n_{c,\text{train}}=n_c-n_{c,\text{test}}-n_{c,\text{val}}$$

- $n_{c,\text{train}}$ = จำนวนของคลาส $c$ ที่ตกไปกอง train (val/test อ่านทำนองเดียวกัน)
- ทำแบบนี้กับ **ทุกคลาส** $c$ แล้วต่อกัน — คือความหมายของโค้ด `for c in np.unique(y)` ในฟังก์ชัน `split()`

**สิ่งที่รับประกัน (invariant):** สัดส่วนของทุกคลาสในทุกกองเท่ากับสัดส่วนเดิม $p_c$

$$\frac{n_{c,\text{train}}}{N_{\text{train}}}\;\approx\;\frac{n_{c,\text{val}}}{N_{\text{val}}}\;\approx\;\frac{n_{c,\text{test}}}{N_{\text{test}}}\;\approx\;p_c$$

- **ทำไมสำคัญ:** สูตรนี้บอกว่า **ไม่มีกองไหนขาดคลาส** — ถ้าเก็บ `shaking` มา $n_{\text{shaking}}=20$ หน้าต่าง test ก็ยังได้ราว $\lfloor 0.15\times 20\rfloor=3$ หน้าต่าง ไม่หลุดเป็น 0 เหมือนสุ่มดื้อๆ
- ตรงกับ `np.bincount` ที่เราสั่งพิมพ์ตอนตรวจ dataset — ตัวเลขทั้ง 3 กองจะสะท้อน $p_c$ เดียวกัน

> นี่คือเหตุผลที่ "stratified" เป็นค่าเริ่มต้นที่ควรใช้เสมอ — คณิตข้างบนพิสูจน์ว่ามันกันเหตุ "test ไม่มี shaking" ได้ตั้งแต่ก่อน train

---

# no leakage — กฎเหล็กของการเตรียมข้อมูล

ข้อผิดพลาดที่ทำให้ตัวเลขความแม่น "สวยหลอกๆ" คือ **ข้อมูลรั่ว (leakage)** — ปล่อยให้สถิติของ val/test แอบเข้าไปมีอิทธิพลตอน train จุดที่พลาดบ่อยสุดคือตอน normalize

```python
# ถูก: คิด mean/std จาก TRAIN เท่านั้น แล้วเอาไปใช้กับ val/test
def normalize(X_train, *others):
    mean = X_train.reshape(-1, X_train.shape[-1]).mean(0)
    std  = X_train.reshape(-1, X_train.shape[-1]).std(0) + 1e-6
    norm = lambda A: (A - mean) / std
    return (norm(X_train), *[norm(o) for o in others]), (mean, std)
```

- ถ้าคิด `mean/std` จากข้อมูล **ทั้งหมด** (รวม test) = test รั่วเข้า train แล้ว ความแม่นที่วัดได้จะดีเกินจริง
- กฎ: **fit บน train · apply ทุกกอง** — สถิติของ test ต้องไม่มีวันถูกโมเดลเห็นก่อนสอบ

> leakage เป็นบั๊กที่ไม่ crash — โปรแกรมรันผ่าน ตัวเลขออกมาสวย แต่พอ deploy จริงกลับพัง นี่คือเหตุผลที่วิศวกร ML ระวังเรื่องนี้เป็นพิเศษ

---

# dataset_tools.py — เครื่องมือฝั่ง PC

ฝั่ง PC เรามีไฟล์เดียว [`dataset_tools.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/dataset_tools.py) (ให้ไว้แล้ว) ที่รวม 5 ฟังก์ชันของการเตรียมข้อมูล — ชุดบทเรียนนี้เราเรียกใช้มัน ไม่ต้องเขียนเอง แต่ต้องอ่านให้เข้าใจ:

| ฟังก์ชัน | ทำอะไร |
|---|---|
| `load_csv(path)` | อ่าน CSV ของบอร์ด → `(samples[N,6], labels[N])` |
| `make_windows(s, l)` | ตัดสายเป็นหน้าต่างซ้อนกัน → `(X[W,50,6], y[W])` |
| `normalize(X_train, ...)` | มาตรฐานต่อช่อง (fit บน train เท่านั้น) |
| `split(X, y)` | แบ่ง train/val/test แบบ stratified |
| `synthesize(path)` | สร้างข้อมูลปลอมให้ท่อรันได้ก่อนมีข้อมูลจริง |

- ค่าคงที่สำคัญอยู่หัวไฟล์: `CLASSES = ["idle","circle","shaking"]`, `WIN = 50`, `HOP = 25` — ตรงกับที่บอร์ดเก็บ
- ทั้ง 5 ฟังก์ชันคือ "สมองการเตรียมข้อมูล" ที่ชุดบทเรียนนี้สอน — โค้ดฝั่งบอร์ดแค่ป้อน CSV ที่ถูกฟอร์แมตให้มัน

> เราให้ [`dataset_tools.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/dataset_tools.py) มาแล้ว เพราะโฟกัสของ **คุณ** ชุดบทเรียนนี้คือ "เก็บ CSV ให้ดี" (ฝั่งบอร์ด) ส่วนการ split เป็นตรรกะ PC ที่อ่านเข้าใจแล้วเรียกใช้ได้
