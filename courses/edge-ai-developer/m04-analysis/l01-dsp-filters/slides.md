---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 4.1 — ฟิลเตอร์ DSP: EMA, Median, Kalman และ radar range profile"
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

# บทเรียน 4.1 — ฟิลเตอร์ DSP: EMA, Median, Kalman และ radar range profile
## ทำสัญญาณให้สะอาดสด ๆ ตรงหน้า

**โมดูล 4 — วิเคราะห์สัญญาณ**

**เปิดกล่อง Analysis (เสาที่ 3 ของวงจรข้อมูล)**

> คาถาประจำบทเรียน: **"สัญญาณดิบมีหนามเสมอ — ฟิลเตอร์คือมือที่ปัดหนามทิ้ง เหลือแต่ของจริงให้โมเดลเห็น"**

`dsp.EMA` · `dsp.Median` · `dsp.Kalman1D` บนบอร์ด BENTO (PSoC Edge · Cortex-M55 + Ethos-U55 NPU)

---

# เปิดบทเรียนด้วยของจริงก่อน

เหมือนทุกบทเรียน เราเริ่มแบบ **กลับด้าน** — รันของที่ทำงานได้ก่อน แล้วค่อยแกะว่ามันสะอาดขึ้นได้ยังไง

<div style="text-align:center;margin:10px 0">
<svg width="820" height="150" viewBox="0 0 820 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arOpen" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="40" width="180" height="70" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="104" y="72" font-size="15" font-weight="700" fill="#2e7d32" text-anchor="middle">รันของจริงก่อน</text>
  <text x="104" y="94" font-size="12" fill="#555" text-anchor="middle">Raw vs Filtered</text>
  <rect x="234" y="40" width="180" height="70" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="324" y="72" font-size="15" font-weight="700" fill="#1565c0" text-anchor="middle">แกะดูข้างใน</text>
  <text x="324" y="94" font-size="12" fill="#555" text-anchor="middle">ฟิลเตอร์ทำงานยังไง</text>
  <rect x="454" y="40" width="180" height="70" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="544" y="72" font-size="15" font-weight="700" fill="#e65100" text-anchor="middle">เติม/จูนเอง</text>
  <text x="544" y="94" font-size="12" fill="#555" text-anchor="middle">EMA/Median/Kalman</text>
  <rect x="674" y="40" width="132" height="70" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="740" y="72" font-size="15" font-weight="700" fill="#6a1b9a" text-anchor="middle">อยากสร้างต่อ</text>
  <text x="740" y="94" font-size="12" fill="#555" text-anchor="middle">FFT · feature (4.3–4.6)</text>
  <line x1="194" y1="75" x2="230" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="414" y1="75" x2="450" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="634" y1="75" x2="670" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
</svg>
</div>

วิธี **PRIMM** (Predict–Run–Investigate–Modify–Make) อันเดิม: ครั้งนี้เราจะเปิดแอปที่โชว์เส้นดิบเทียบเส้นที่กรองแล้วสองกราฟซ้อนกัน แล้วมือคุณเขย่าบอร์ด ตาคุณเห็นเส้นล่างเรียบกว่าเส้นบนทันที

> ยังไม่ต้องเข้าใจสมการฟิลเตอร์ทุกตัวในนาทีแรก ขอแค่เห็นว่า "เส้นบนกระตุก เส้นล่างนิ่ง" แล้วเริ่มสงสัยว่ามันทำได้ยังไง เท่านั้นพอ

---

# เป้าหมายของชุดบทเรียนนี้

จบชุดบทเรียนนี้เราจะเดินครบ แล้วปิดท้ายด้วยการทำสัญญาณจริงให้สะอาดสด ๆ:

1. **ทำไมสัญญาณดิบต้องกรอง** — สัญญาณรบกวน (noise) มาจากไหน และมันหลอกโมเดลยังไง
2. **ฟิลเตอร์สามตระกูล** ที่ใช้บ่อยสุดใน Edge AI: `dsp.EMA` (ถัวเฉลี่ยถ่วงน้ำหนัก) · `dsp.Median` (ตัดหนามโดด) · `dsp.Kalman1D` (ชั่งน้ำหนัก predict/measure)
3. **API ร่วม** ของทุกฟิลเตอร์: `.update(x)` / `.value()` / `.reset()` — สร้างครั้งเดียว ป้อนทีละค่า
4. **radar range profile** — ตัวอย่างของจริงที่ฝั่ง C ทำ HPF→FFT→dB→peak ให้แล้ว เหลือ median กันหนามฝั่งเรา
5. ลงมือ: เปิดแอป [`s08_filters.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l02-filters-lab/practice/s08_filters.py) เขย่าบอร์ด ดูเส้นดิบเทียบเส้นกรอง + เปอร์เซ็นต์ลดสัญญาณรบกวน

ปลายทางของวันนี้: เลือกฟิลเตอร์ใน dropdown ขยับบอร์ด แล้วเห็นเส้นล่างสะอาดกว่าเส้นบนอย่างชัดเจน พร้อมตัวเลข "noise down %"

> วันนี้เราเน้น "กรองเป็น + อธิบายข้อแลกเปลี่ยนได้" ส่วน FFT กับ feature extraction เก็บไว้เป็น บทเรียน 4.3–4.6 ต่อจากนี้

---

# ชุดบทเรียนนี้อยู่ตรงไหนของวงจร

เราเข้าเสาที่ 3 แล้ว — **Analysis** ต่อจาก Processing (โมดูล 3) ที่เราแปลงสัญญาณดิบเป็นปริมาณที่มีความหมาย (tilt, พลังงาน, dBFS)

<div style="text-align:center;margin:6px 0">
<svg width="920" height="150" viewBox="0 0 920 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arLC" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g text-anchor="middle">
    <rect x="10" y="46" width="160" height="60" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="90" y="72" font-size="13" font-weight="700" fill="#1565c0">1 · DAQ</text>
    <text x="90" y="92" font-size="10" fill="#888">โมดูล 2</text>
    <rect x="196" y="46" width="160" height="60" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="276" y="72" font-size="13" font-weight="700" fill="#2e7d32">2 · Processing</text>
    <text x="276" y="92" font-size="10" fill="#888">โมดูล 3 (มาแล้ว)</text>
    <rect x="382" y="42" width="160" height="68" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="3"/>
    <text x="462" y="70" font-size="13" font-weight="700" fill="#e65100">3 · Analysis</text>
    <text x="462" y="90" font-size="10" fill="#888">4.1–4.2 (วันนี้) · 4.3–4.4 · 4.5–4.6</text>
    <rect x="568" y="46" width="160" height="60" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
    <text x="648" y="72" font-size="13" font-weight="700" fill="#6a1b9a">4 · Training</text>
    <text x="648" y="92" font-size="10" fill="#888">โมดูล 5</text>
    <rect x="754" y="46" width="160" height="60" rx="12" fill="#e0f7fa" stroke="#00838f" stroke-width="2"/>
    <text x="834" y="72" font-size="13" font-weight="700" fill="#00838f">5 · Apps</text>
    <text x="834" y="92" font-size="10" fill="#888">โมดูล 6</text>
  </g>
  <line x1="170" y1="76" x2="194" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <line x1="356" y1="76" x2="380" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <line x1="542" y1="76" x2="566" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <line x1="728" y1="76" x2="752" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <text x="462" y="132" font-size="12" fill="#888" text-anchor="middle">Analysis = ทำสัญญาณให้ "อ่านง่าย" ก่อนส่งให้โมเดล — เริ่มที่การกรองสัญญาณรบกวน</text>
</svg>
</div>

> Processing แปลง "หน่วย" (accel → tilt), Analysis จัดการ "รูปร่างของสัญญาณตามเวลา/ความถี่" ฟิลเตอร์วันนี้คือก้าวแรก ก่อนจะไป FFT (บทเรียน 4.3–4.4) และ feature ที่โมเดลกินจริง (บทเรียน 4.5–4.6)

---

# ทบทวนเร็ว — จาก บทเรียน 3.1–3.2 มาถึงตรงนี้

บทเรียน 3.1–3.2 เราเอาสัญญาณดิบมาแปลงเป็นปริมาณที่มีความหมาย เช่น `dsp.tilt(ax,ay,az)` คืน `(roll,pitch)` แล้วโชว์เป็นเกจ

- แต่ตอนโชว์เกจจริง คุณคงเห็นว่ามัน **สั่น** ตลอด ทั้งที่วางบอร์ดนิ่ง ๆ — นั่นแหละสัญญาณรบกวน
- บทเรียน 3.1–3.2 ตอบคำถาม "ค่านี้แปลว่าอะไร" (ฟิสิกส์) · บทเรียน 4.1–4.2 ตอบ "ค่านี้เชื่อได้แค่ไหน และจะทำให้นิ่งได้ยังไง" (สัญญาณ)
- เครื่องมือเดียวกัน คือโมดูล `dsp` — บทเรียน 3.1–3.2 ใช้ฟังก์ชันฟิสิกส์ (`tilt/altitude`) วันนี้เราใช้คลาสฟิลเตอร์ (`EMA/Median/Kalman1D`)

> ถ้าบทเรียน 3.1–3.2 คุณเคยรำคาญว่า "ทำไมเกจกระพริบจัง" — ชุดบทเรียนนี้แหละคือคำตอบ เราจะจับความกระพริบนั้นมากดให้นิ่ง

---

# ปัญหา: สัญญาณดิบมีหนามเสมอ

ไม่มีเซนเซอร์ตัวไหนในโลกให้ค่าเรียบ ๆ ทุกอย่างมี **หนาม** (noise) ปนมาด้วย บางทีก็หนามเล็ก ๆ กระจาย บางทีก็ค่าโดดสุดขั้ว (outlier)

<div style="text-align:center;margin:6px 0">
<svg width="880" height="220" viewBox="0 0 880 220" font-family="DejaVu Sans, sans-serif">
  <rect x="12" y="10" width="850" height="200" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1"/>
  <line x1="40" y1="110" x2="850" y2="110" stroke="#30363d" stroke-width="1" stroke-dasharray="4 4"/>
  <text x="46" y="28" font-size="12" fill="#8b949e">สัญญาณจริง (ของที่เราอยากได้) = เส้นประ · สัญญาณดิบ = เส้นส้มมีหนาม</text>
  <path d="M40,110 C160,60 260,60 380,110 C500,160 600,160 720,110 C780,85 820,85 850,95" fill="none" stroke="#4488ff" stroke-width="2" stroke-dasharray="6 5"/>
  <path d="M40,112 L70,86 L88,124 L110,70 L130,120 L155,64 L172,118 L200,58 L215,72 L240,50 L262,74 L285,96 L305,150 L330,120 L352,168 L378,132 L400,158 L425,120 L448,176 L470,140 L495,160 L520,132 L545,176 L568,146 L592,158 L618,120 L640,142 L665,104 L690,140 L712,100 L735,118 L760,92 L785,110 L810,84 L835,100" fill="none" stroke="#ff9800" stroke-width="1.6"/>
  <text x="46" y="200" font-size="12" fill="#8b949e">ถ้าเอาสัญญาณดิบไปตัดสินใจตรง ๆ (threshold/โมเดล) หนามพวกนี้จะทำให้ "เจอผี" — เดี๋ยวข้าม เดี๋ยวไม่ข้าม</text>
</svg>
</div>

- หนามเล็กกระจาย มาจากความร้อน วงจร ADC การสั่นสะเทือน — เรียกว่า noise
- ค่าโดดสุดขั้ว (spike) มาจากการสะท้อนหลายทาง (multipath ของเรดาร์) หรือชนสัญญาณชั่วขณะ — เรียกว่า outlier
- ฟิลเตอร์ต่างชนิดเก่งกันคนละแบบ: บางตัวเก่งหนามเล็ก บางตัวเก่ง spike (เดี๋ยวเราจะเจอ)

> นี่คือเหตุผลที่ Analysis มาก่อน Training เสมอ — ถ้าป้อนสัญญาณสกปรกให้โมเดล มันจะเรียน "หนาม" ไปด้วย แล้วพังตอนใช้จริง

---

# รันของจริงก่อน — เห็นแอปทำงานเลย

เปิด [`s08_filters_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l02-filters-lab/examples/s08_filters_full.py) (หรือ [`s08_filters.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l02-filters-lab/practice/s08_filters.py) ที่เติมครบแล้ว) จะเห็นสองกราฟซ้อนกัน:

- **กราฟบน (Raw)** — สัญญาณดิบจาก IMU (ขนาดความเร่งสามแกน) มีหนามชัดตอนขยับ
- **กราฟล่าง (Filtered)** — ค่าเดียวกันที่ผ่านฟิลเตอร์ เรียบขึ้นเห็น ๆ
- **แถบ noise down %** — บอกว่าฟิลเตอร์ลด "การกระตุกระหว่างเฟรม" ได้กี่เปอร์เซ็นต์

ลองเลย: เขย่าบอร์ดเบา ๆ → เส้นบนเต้นแรง เส้นล่างตามช้ากว่าและเรียบกว่า แล้วสลับฟิลเตอร์ใน dropdown ดูว่าเส้นล่างเปลี่ยนนิสัยยังไง

> อย่าเพิ่งอ่านโค้ด รันก่อน เล่นก่อน ให้ตาเห็นความต่างของสามฟิลเตอร์ด้วยมือตัวเอง แล้วค่อยกลับมาถามว่า "มันต่างกันเพราะอะไร"

---

# สัญญาณรบกวนมาจากไหน

ก่อนจะกรอง เราต้องรู้ว่ากำลังสู้กับอะไร noise มีหลายหน้า และแต่ละหน้าเรียกฟิลเตอร์คนละตัว

| ชนิด | หน้าตา | มาจาก | ใครจัดการเก่ง |
|---|---|---|---|
| **white noise** | หนามเล็กกระจายรอบค่าจริง | ความร้อน · วงจร · ADC | EMA / SMA (ถัวเฉลี่ย) |
| **spike / outlier** | ค่าโดดสุดขั้วเป็นครั้งคราว | multipath · ชนสัญญาณ · บิตพลิก | Median (โหวตค่ากลาง) |
| **drift** | ค่าค่อย ๆ เลื่อนช้า ๆ | อุณหภูมิ · แบตหมด | HPF (ตัดของช้า) |
| **สั่นเร็วปนช้า** | จริงบ้างรบกวนบ้าง | ทุกอย่างรวมกัน | Kalman (ชั่งน้ำหนัก) |

- ไม่มีฟิลเตอร์ "ตัวเทพ" ที่ชนะทุกแบบ — เลือกให้ตรงกับหน้าของ noise ที่เจอ
- วันนี้เราโฟกัส 3 ตัว: EMA (หนามเล็ก) · Median (spike) · Kalman1D (ผสม)

> การถามว่า "สัญญาณของฉันสกปรกแบบไหน" คือทักษะวิศวกรที่แท้จริง — ก่อนหยิบเครื่องมือ ให้มองศัตรูก่อน

---

# แนวคิดหลัก — ฟิลเตอร์คือความจำ

หัวใจของฟิลเตอร์ตามเวลา (temporal filter): มันไม่ได้มองแค่ค่าปัจจุบันค่าเดียว แต่ **จำอดีต** แล้วเอามาถ่วงกับค่าใหม่

<div style="text-align:center;margin:6px 0">
<svg width="860" height="150" viewBox="0 0 860 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arF" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="50" width="150" height="52" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="95" y="72" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">ค่าใหม่ x</text>
  <text x="95" y="90" font-size="10" fill="#888" text-anchor="middle">(มีหนาม)</text>
  <rect x="340" y="34" width="200" height="84" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="440" y="62" font-size="14" font-weight="700" fill="#1565c0" text-anchor="middle">ฟิลเตอร์</text>
  <text x="440" y="84" font-size="11" fill="#555" text-anchor="middle">จำอดีต + ถ่วงกับค่าใหม่</text>
  <text x="440" y="102" font-size="10" fill="#888" text-anchor="middle">state ภายใน (.value())</text>
  <rect x="700" y="50" width="150" height="52" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="775" y="72" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">ค่าที่กรองแล้ว y</text>
  <text x="775" y="90" font-size="10" fill="#888" text-anchor="middle">(เรียบขึ้น)</text>
  <line x1="170" y1="76" x2="336" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arF)"/>
  <line x1="540" y1="76" x2="696" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arF)"/>
  <path d="M440,118 C440,140 440,140 440,126" fill="none" stroke="#9e9e9e" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#arF)"/>
  <text x="440" y="140" font-size="10" fill="#9e9e9e" text-anchor="middle">ป้อนทีละค่าในลูป: y = filt.update(x)</text>
</svg>
</div>

- ทุกฟิลเตอร์ในโมดูล `dsp` ทำงานแบบ **streaming**: ป้อนทีละค่าด้วย `.update(x)` มันเก็บ state ไว้ในตัวแล้วคืนค่าที่กรองแล้ว
- ต่างจากการโหลดทั้งอาร์เรย์มากรอง — บนไมโครคอนโทรลเลอร์เราไม่มี RAM เก็บทั้งสัญญาณ จึงกรองสด ทีละตัวอย่าง

> "ความเรียบ" มาจากการที่ฟิลเตอร์ไม่ยอมกระโดดตามค่าใหม่ทันที มันถ่วงด้วยอดีต — ยิ่งถ่วงหนัก ยิ่งเรียบ แต่ก็ยิ่งตอบสนองช้า นี่คือข้อแลกเปลี่ยนหลักของทั้งชุดบทเรียน

---

# โมดูล dsp — ฟิลเตอร์สำเร็จให้แล้ว

โมดูล `dsp` (ฝั่ง C บน CM33) มีคลาสฟิลเตอร์พร้อมใช้หลายตัว ทุกตัวหน้าตา API เหมือนกันเป๊ะ วันนี้เราโฟกัสสามตัว:

| คลาส | สร้างด้วย | เก่งเรื่อง | ความจำ |
|---|---|---|---|
| `dsp.EMA` | `EMA(alpha=0.15)` | หนามเล็กกระจาย | ค่าเดียว (ถูกสุด) |
| `dsp.SMA` | `SMA(window=10)` | หนามเล็ก + ค่าเฉลี่ยตรง | buffer N ค่า |
| `dsp.Median` | `Median(window=5)` | spike / outlier โดด ๆ | buffer N ค่า |
| `dsp.LPF` | `LPF(cutoff=5, fs=100)` | ตัดของเร็ว (ความถี่สูง) | ค่าเดียว |
| `dsp.HPF` | `HPF(cutoff=0.5, fs=100)` | ตัด drift (ความถี่ต่ำ) | ค่าเดียว |
| `dsp.Kalman1D` | `Kalman1D(q=0.02, r=0.6)` | ผสม จริง+รบกวน | ค่าเดียว + ความมั่นใจ |

- **สำคัญ**: พารามิเตอร์ทุกตัวเป็น **keyword argument** (`alpha=`, `window=`, `q=`, `r=`) ส่งแบบ positional เช่น `dsp.EMA(0.15)` จะโยน `TypeError` ทันที
- วันนี้เราเล่นสามตัวหลัก: `EMA` / `Median` / `Kalman1D` (อีกสามตัวเป็นการบ้านต่อยอด)

> ฝั่ง C เขียนฟิลเตอร์ให้เสร็จ เรากลายเป็นคนเลือกและจูน — นี่คือ 70% ที่ได้ฟรี เราลงมือกับ 30% ที่เหลือคือ "เลือกให้ถูก + ตั้งค่าให้พอดี"

---

# API ร่วมของทุกฟิลเตอร์ — สามเมท็อด

จำสามเมท็อดนี้ตัวเดียว ใช้ได้กับฟิลเตอร์ทุกตัวในโมดูล `dsp`:

```python
import dsp
f = dsp.EMA(alpha=0.15)      # 1) สร้างครั้งเดียว (นอกลูป!)
while True:
    x = read_sensor()        # ค่าดิบหนึ่งตัว
    y = f.update(x)          # 2) ป้อนเข้า -> คืนค่าที่กรองแล้ว
    last = f.value()        #    ดูค่าล่าสุดโดยไม่ป้อนใหม่
    f.reset()               # 3) ล้าง state (เช่นตอนสลับแหล่งสัญญาณ)
```

- `.update(x)` — หัวใจ: ป้อนตัวอย่างใหม่หนึ่งค่า คืนค่าที่กรองแล้ว (เรียกทุกวนรอบ)
- `.value()` — คืนค่าล่าสุดที่กรองไว้ ไม่เปลี่ยน state (เอาไว้อ่านซ้ำ)
- `.reset()` — ล้างความจำกลับเป็นศูนย์ (เริ่มนับใหม่)

> **สร้างครั้งเดียวนอกลูป** สำคัญมาก เพราะ state (ความจำ) อยู่ในอ็อบเจกต์ ถ้าสร้างใหม่ทุกวนรอบ = ลบความจำทุกครั้ง ฟิลเตอร์จะไม่มีวันเรียบ (นี่คือบั๊กยอดฮิต)

---

# EMA — ถัวเฉลี่ยแบบถ่วงน้ำหนักอดีต

**EMA (Exponential Moving Average)** ฟิลเตอร์ที่ถูกและใช้บ่อยสุด สูตรมีแค่บรรทัดเดียว:

$$y_t = \alpha\, x_t + (1-\alpha)\, y_{t-1}$$

- ค่าใหม่ $x_t$ มีน้ำหนัก $\alpha$ · ค่าที่กรองไว้เดิม $y_{t-1}$ มีน้ำหนัก $1-\alpha$
- $\alpha$ เล็ก (เช่น 0.05) = เชื่ออดีตมาก → **เรียบมาก แต่ตอบสนองช้า** (ลากตามช้า)
- $\alpha$ ใหญ่ (เช่น 0.5) = เชื่อค่าใหม่มาก → **ไวมาก แต่เรียบน้อย** (หนามยังโผล่)

<div style="text-align:center;margin:6px 0">
<svg width="820" height="120" viewBox="0 0 820 120" font-family="DejaVu Sans, sans-serif">
  <text x="60" y="24" font-size="12" fill="#666">α = 0.5 (ไว)</text>
  <path d="M20,70 L60,44 L80,80 L110,40 L135,78 L165,42 L190,74 L230,44 L260,64" fill="none" stroke="#ef6c00" stroke-width="1.8"/>
  <text x="330" y="24" font-size="12" fill="#666">α = 0.15 (สมดุล)</text>
  <path d="M300,70 C340,58 360,58 400,60 C440,62 460,60 500,58 C520,57 530,58 540,58" fill="none" stroke="#1565c0" stroke-width="2.2"/>
  <text x="610" y="24" font-size="12" fill="#666">α = 0.05 (เรียบ/ช้า)</text>
  <path d="M580,72 C640,70 700,66 800,60" fill="none" stroke="#2e7d32" stroke-width="2.4"/>
  <text x="410" y="108" font-size="11" fill="#888" text-anchor="middle">α เล็กลง → เส้นเรียบขึ้น แต่ตามของจริงช้าลง (ข้อแลกเปลี่ยน)</text>
</svg>
</div>

> คำถามวิศวกร: "ฉันยอมช้าแค่ไหนเพื่อแลกความเรียบ?" — งานตรวจการล้มต้องไว เลือก α ใหญ่หน่อย · งานวัดอุณหภูมิห้องยอมช้าได้ เลือก α เล็ก ในไฟล์เราตั้ง `EMA_ALPHA = 0.15` เป็นจุดตั้งต้นที่สมดุล

---

# Median — โหวตเอาค่ากลาง ตัดหนามโดด

**Median filter** เก่งคนละเรื่องกับ EMA มันไม่ถัวเฉลี่ย แต่ **เรียงค่าล่าสุด N ตัวแล้วเอาค่ากลาง** — ค่าโดดสุดขั้วจึงไม่มีสิทธิ์ชนะ

<div style="text-align:center;margin:6px 0">
<svg width="840" height="150" viewBox="0 0 840 150" font-family="DejaVu Sans, sans-serif">
  <text x="20" y="26" font-size="13" font-weight="700" fill="#455a64">หน้าต่าง 5 ค่าล่าสุด (มี spike ปน):</text>
  <g font-size="13" text-anchor="middle">
    <rect x="30" y="40" width="54" height="34" rx="6" fill="#e3f2fd" stroke="#1565c0"/><text x="57" y="62" fill="#1565c0">98</text>
    <rect x="94" y="40" width="54" height="34" rx="6" fill="#e3f2fd" stroke="#1565c0"/><text x="121" y="62" fill="#1565c0">101</text>
    <rect x="158" y="40" width="54" height="34" rx="6" fill="#ffebee" stroke="#c62828"/><text x="185" y="62" fill="#c62828">240</text>
    <rect x="222" y="40" width="54" height="34" rx="6" fill="#e3f2fd" stroke="#1565c0"/><text x="249" y="62" fill="#1565c0">99</text>
    <rect x="286" y="40" width="54" height="34" rx="6" fill="#e3f2fd" stroke="#1565c0"/><text x="313" y="62" fill="#1565c0">100</text>
  </g>
  <text x="420" y="60" font-size="20" fill="#607d8b">→ เรียง →</text>
  <g font-size="13" text-anchor="middle">
    <rect x="520" y="40" width="54" height="34" rx="6" fill="#e8f5e9" stroke="#2e7d32"/><text x="547" y="62" fill="#2e7d32">98</text>
    <rect x="584" y="40" width="54" height="34" rx="6" fill="#e8f5e9" stroke="#2e7d32"/><text x="611" y="62" fill="#2e7d32">99</text>
    <rect x="648" y="40" width="54" height="34" rx="6" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2.5"/><text x="675" y="62" fill="#2e7d32" font-weight="700">100</text>
    <rect x="712" y="40" width="54" height="34" rx="6" fill="#e8f5e9" stroke="#2e7d32"/><text x="739" y="62" fill="#2e7d32">101</text>
    <rect x="776" y="40" width="54" height="34" rx="6" fill="#ffebee" stroke="#c62828"/><text x="803" y="62" fill="#c62828">240</text>
  </g>
  <text x="675" y="98" font-size="12" fill="#2e7d32" text-anchor="middle">ค่ากลาง = 100 (spike 240 ถูกดันไปขอบ ไม่โดนเลือก)</text>
  <text x="420" y="130" font-size="11" fill="#888" text-anchor="middle">ถ้าใช้ mean จะได้ (98+101+240+99+100)/5 = 127.6 — โดน spike ลากเสียหมด</text>
</svg>
</div>

- สร้างด้วย `dsp.Median(window=5)` — เฟิร์มแวร์บังคับ window เป็นเลขคี่ (3..15) เพื่อให้มีค่ากลางชัด
- ข้อดี: spike เดียวโดดแค่ไหนก็ไม่กระเทือนผล · ข้อเสีย: กินความจำ N ค่า และตอบสนองขอบคมช้ากว่านิด

> นี่คือฟิลเตอร์ที่ตัวอย่างเรดาร์ ([`05_radar_distance.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l01-dsp-filters/examples/05_radar_distance.py)) ใช้จริง เพราะระยะจากเรดาร์ชอบกระโดดเพราะ multipath — median กันได้ตรงจุด เดี๋ยวเราจะเห็นมันในหน้า radar range profile

---

# Kalman1D — ชั่งน้ำหนักระหว่าง "ที่คาด" กับ "ที่วัด"

**Kalman filter** ฉลาดกว่าเพื่อน มันเก็บทั้งค่าประมาณ $x$ และ **ความไม่มั่นใจ** $p$ แล้วทุกก้าวจะชั่งน้ำหนักว่าจะเชื่อการวัดใหม่แค่ไหน

<div style="text-align:center;margin:4px 0">
<svg width="820" height="120" viewBox="0 0 820 120" font-family="DejaVu Sans, sans-serif">
  <rect x="20" y="34" width="180" height="52" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="110" y="56" font-size="12" font-weight="700" fill="#1565c0" text-anchor="middle">predict</text>
  <text x="110" y="76" font-size="11" fill="#555" text-anchor="middle">p += q (ยิ่งไม่แน่ใจขึ้น)</text>
  <rect x="320" y="34" width="200" height="52" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="420" y="54" font-size="12" font-weight="700" fill="#e65100" text-anchor="middle">gain k = p / (p + r)</text>
  <text x="420" y="74" font-size="11" fill="#555" text-anchor="middle">เชื่อการวัดแค่ไหน</text>
  <rect x="640" y="34" width="160" height="52" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="720" y="54" font-size="12" font-weight="700" fill="#2e7d32" text-anchor="middle">update</text>
  <text x="720" y="74" font-size="11" fill="#555" text-anchor="middle">x += k(z - x)</text>
  <line x1="200" y1="60" x2="316" y2="60" stroke="#607d8b" stroke-width="2"/>
  <line x1="520" y1="60" x2="636" y2="60" stroke="#607d8b" stroke-width="2"/>
</svg>
</div>

- `dsp.Kalman1D(q=0.02, r=0.6)` — สองปุ่มปรับ:
  - `q` (process noise) ต่ำ = เชื่อว่าสัญญาณจริง "นิ่ง" → เรียบมาก · สูง = ยอมให้ค่าจริงขยับเร็ว
  - `r` (measurement noise) สูง = "ไม่ค่อยเชื่อเซนเซอร์" (มองว่า noisy) → กรองหนัก · ต่ำ = เชื่อการวัด
- ต่างจาก EMA ตรงที่ Kalman ปรับความหนักของการกรองเองตามความมั่นใจ ไม่ได้ใช้ค่าคงที่ตัวเดียว

> เริ่มจูนง่าย ๆ: ล็อก `q` ไว้เล็ก ๆ แล้วเล่นกับ `r` อย่างเดียว — `r` สูงขึ้น = เรียบขึ้นแต่ตามช้าลง (คุ้น ๆ ไหม มันคือข้อแลกเปลี่ยนเดิม แค่คนละหน้าตา)

---

# ภาพเคลื่อนไหว — EMA ทำสัญญาณ noisy ให้เรียบ

![ภาพเคลื่อนไหว: เส้นสัญญาณดิบที่มีสัญญาณรบกวนเทียบกับเส้น EMA ที่เรียบกว่า พร้อมสูตร y[t] = α·x[t] + (1−α)·y[t−1] w:760](img/anim_ema_filter.svg)

เส้นเขียว (เรียบ) ค่อย ๆ วาดทับเส้นแดง (ดิบ) — เห็นแนวโน้มจริงโดยไม่ถูกหนามหลอก

---

# คณิตของ EMA — อ่านทีละตัวอักษร

สูตร EMA มีบรรทัดเดียว ท่องได้เลย แล้วเราจะแกะทีละสัญลักษณ์ว่ามันแปลว่าอะไร:

$$y[n] = \alpha\, x[n] + (1-\alpha)\, y[n-1]$$

- $y[n]$ — ค่าที่กรองแล้ว **รอบนี้** (ค่าที่เราจะเอาไปวาด/ใช้ตัดสินใจ)
- $x[n]$ — ค่าดิบจากเซนเซอร์ **รอบนี้** (ยังมีหนาม)
- $y[n-1]$ — ค่าที่กรองแล้ว **รอบก่อน** = ความจำของฟิลเตอร์ (state ที่เก็บในอ็อบเจกต์)
- $\alpha$ — น้ำหนักที่เราให้กับ "ของใหม่" ($0 < \alpha \le 1$) ส่วน $1-\alpha$ คือน้ำหนักที่ให้กับ "ของเก่า"

อ่านเป็นประโยคเดียว: **ค่าใหม่หนึ่งส่วน $\alpha$ ผสมกับความทรงจำเดิมอีก $1-\alpha$ ส่วน**

<div style="text-align:center;margin:6px 0">
<svg width="760" height="92" viewBox="0 0 760 92" font-family="DejaVu Sans, sans-serif">
  <rect x="20" y="26" width="330" height="44" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="185" y="46" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">ของใหม่ x[n] · น้ำหนัก α</text>
  <text x="185" y="63" font-size="10" fill="#888" text-anchor="middle">α ใหญ่ = ไว · α เล็ก = เรียบ</text>
  <rect x="410" y="26" width="330" height="44" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="575" y="46" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">ความจำเดิม y[n-1] · น้ำหนัก (1-α)</text>
  <text x="575" y="63" font-size="10" fill="#888" text-anchor="middle">ยิ่งถ่วงหนัก ยิ่งลากตามช้า</text>
  <text x="380" y="54" font-size="20" fill="#607d8b" text-anchor="middle">+</text>
</svg>
</div>

> ทำไมสำคัญกับชุดบทเรียนนี้: ค่า `EMA_ALPHA = 0.15` ในไฟล์คือการเลือกว่า "เชื่อของใหม่ 15% เชื่อความจำเดิม 85%" นั่นแหละคือปุ่มเดียวที่ตัดสินว่าเส้นล่างจะเรียบแค่ไหน ตามช้าแค่ไหน — เข้าใจสูตรนี้ตัวเดียว จูน EMA เป็นทันที

---

# คณิตของ Kalman — gain คือ "จะเชื่อการวัดแค่ไหน"

หัวใจของ Kalman1D คือค่าเดียวชื่อ **Kalman gain** $K$ ที่คำนวณใหม่ทุกก้าว:

$$K = \frac{P}{P + R} \qquad\quad x \leftarrow x + K\,(z - x)$$

- $P$ — ความ **ไม่มั่นใจ** ในค่าประมาณของเราตอนนี้ (มาจากปุ่ม $q$: ยิ่ง $q$ สูง $P$ ยิ่งโต)
- $R$ — ความ **ไม่น่าเชื่อถือของเซนเซอร์** (ปุ่ม $r$: เซนเซอร์ยิ่ง noisy เราตั้ง $R$ ยิ่งสูง)
- $z$ — ค่าที่ **วัดได้จริง** รอบนี้ · $x$ — ค่าประมาณที่เราเชื่อ
- $K$ — อยู่ระหว่าง $0$ ถึง $1$ เสมอ: ใกล้ $1$ = เชื่อการวัดเต็มที่ · ใกล้ $0$ = เชื่อค่าประมาณเดิม แทบไม่ขยับ

ลองแทนค่าให้เห็นภาพ:

- ถ้า $R$ ใหญ่กว่า $P$ มาก (เซนเซอร์ห่วย) → $K$ เล็ก → $x$ ขยับนิดเดียว = **กรองหนัก เรียบมาก**
- ถ้า $P$ ใหญ่กว่า $R$ มาก (เราไม่มั่นใจตัวเอง) → $K$ ใกล้ $1$ → $x$ กระโดดตามการวัด = **ไวมาก**

> ทำไมสำคัญกับชุดบทเรียนนี้: EMA ใช้ $\alpha$ **คงที่** ทั้งชีวิต แต่ Kalman คำนวณ $K$ ใหม่ทุกก้าวตามความมั่นใจ — นี่คือเหตุผลที่มันฉลาดกว่า แต่ก็มีสองปุ่ม (`q`, `r`) ให้จูน ไม่ใช่ปุ่มเดียวเหมือน EMA เทียบสองสูตรนี้ข้าง ๆ กัน คุณจะเห็นว่า Kalman ก็คือ EMA ที่ปรับ $\alpha$ ของตัวเองได้

---

# เทียบสามฟิลเตอร์ — เลือกตัวไหนดี

ไม่มีตัวชนะขาด เลือกให้ตรงกับหน้าของ noise และงบประมาณ (CPU/RAM) ที่มี

| | EMA | Median | Kalman1D |
|---|---|---|---|
| เก่งเรื่อง | หนามเล็กกระจาย | spike / outlier | ผสม จริง+รบกวน |
| ราคา (CPU/RAM) | ถูกสุด (ค่าเดียว) | กลาง (buffer N) | กลาง (คณิตนิดหน่อย) |
| ปุ่มปรับ | `alpha` | `window` | `q`, `r` |
| จุดอ่อน | spike ยังเล็ดลอด | ตอบขอบคมช้า | ต้องจูน 2 ค่า |
| เหมาะกับ | เกจอุณหภูมิ/แสง | ระยะเรดาร์/GPS | IMU fusion ละเอียด |

- เจอ **spike** → Median ก่อนเลย (EMA จะเกลี่ย spike ให้เนียนแต่ยังเห็นโหนก)
- เจอ **หนามเล็ก** เน้นถูก → EMA
- อยากเรียบ + ตามทัน + ยอมจูน → Kalman1D

> ในงานจริงเรามัก **ต่อฟิลเตอร์กัน** เช่น Median กัน spike ก่อน แล้ว EMA เกลี่ยให้เนียนต่อ — วันนี้เราลองทีละตัวก่อน ให้เข้าใจนิสัยของแต่ละตัวชัด ๆ

---

# radar range profile — ของจริงที่ฝั่ง C ทำให้แล้ว

ตัวอย่างอ้างอิงของชุดบทเรียนนี้คือ [`05_radar_distance.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l01-dsp-filters/examples/05_radar_distance.py) — ไม้วัดระยะด้วยเรดาร์ 60 GHz ที่โชว์ว่าการกรองสำคัญแค่ไหนกับสัญญาณจริง

<div style="text-align:center;margin:6px 0">
<svg width="900" height="130" viewBox="0 0 900 130" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arR" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g text-anchor="middle" font-size="12">
    <rect x="10" y="44" width="120" height="48" rx="9" fill="#eceff1" stroke="#607d8b" stroke-width="2"/><text x="70" y="66" font-weight="700" fill="#455a64">raw ADC</text><text x="70" y="82" font-size="10" fill="#888">antenna</text>
    <rect x="160" y="44" width="120" height="48" rx="9" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/><text x="220" y="66" font-weight="700" fill="#1565c0">HPF</text><text x="220" y="82" font-size="10" fill="#888">ตัด DC/drift</text>
    <rect x="310" y="44" width="120" height="48" rx="9" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/><text x="370" y="66" font-weight="700" fill="#6a1b9a">FFT</text><text x="370" y="82" font-size="10" fill="#888">→ ระยะ (4.3–4.4)</text>
    <rect x="460" y="44" width="120" height="48" rx="9" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/><text x="520" y="66" font-weight="700" fill="#e65100">dB + peak</text><text x="520" y="82" font-size="10" fill="#888">หา bin แรง</text>
    <rect x="610" y="44" width="140" height="48" rx="9" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/><text x="680" y="66" font-weight="700" fill="#2e7d32">Median (เรา)</text><text x="680" y="82" font-size="10" fill="#888">กัน multipath</text>
    <rect x="778" y="44" width="112" height="48" rx="9" fill="#e0f7fa" stroke="#00838f" stroke-width="2"/><text x="834" y="66" font-weight="700" fill="#00838f">ระยะบนจอ</text>
  </g>
  <line x1="130" y1="68" x2="158" y2="68" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arR)"/>
  <line x1="280" y1="68" x2="308" y2="68" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arR)"/>
  <line x1="430" y1="68" x2="458" y2="68" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arR)"/>
  <line x1="580" y1="68" x2="608" y2="68" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arR)"/>
  <line x1="750" y1="68" x2="776" y2="68" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arR)"/>
</svg>
</div>

- `sensors.radar_range()` คืน dict: `{'distance_m','peak_db','resolution_m','target','seq'}` — ฝั่ง C ทำ HPF→FFT→dB→peak ให้หมดแล้ว
- ความละเอียด ~0.33 m/bin (ดูจาก `resolution_m`) — บอกโซนได้ แต่ระยะชอบ **กระโดด** เพราะการสะท้อนหลายทาง (multipath)
- ฟิลเตอร์ที่เหมาะคือ **Median** เพราะการกระโดดคือ spike แท้ ๆ — ในแอปเราจึงเลือก Median ได้เมื่อสลับแหล่งเป็น Radar

> `sensors.radar_range()` ให้ระยะจริงบน **บอร์ดจริง** เท่านั้น (บน Emulator เป็นระยะจำลองที่หมุนด้วยลูกบิด) และบนบอร์ดจะโยน `OSError` ถ้า radar DSP ยังไม่ทำงาน — โค้ดเราจึงห่อ `try/except OSError` ไว้ คงเส้นนิ่งแทนที่จะพัง (บทเรียนเดียวกับ `select()` ใน บทเรียน 1.1–1.3)
