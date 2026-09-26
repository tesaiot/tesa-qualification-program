---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 3.1 — จากตัวเลขดิบสู่ปริมาณทางฟิสิกส์: มุมเอียง พลังงาน ความสูง และ dBFS"
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

# บทเรียน 3.1 — จากตัวเลขดิบสู่ปริมาณทางฟิสิกส์: มุมเอียง พลังงาน ความสูง และ dBFS
## คณิต & ฟิสิกส์: แปลงตัวเลขดิบให้พูดภาษาคน

**โมดูล 3 — ประมวลผลด้วยคณิตศาสตร์และฟิสิกส์**

**โมดูล 3 (Processing, Pillar 2) · ขั้นที่ 2 ของวงจรชีวิตข้อมูล**

> คาถาประจำบทเรียน: **"เซนเซอร์ให้ตัวเลขดิบ เราให้ความหมาย — มุมเอียง พลังงาน ความสูง ระดับเสียง ล้วนเป็นสูตรไม่กี่บรรทัด"**

MicroPython บนบอร์ด BENTO (PSoC Edge · Cortex-M55 + Ethos-U55 NPU)

---

# เปิดบทเรียนด้วยของจริงก่อน

เหมือนทุกบทเรียน เราเริ่มแบบ **กลับด้าน** — รันของที่ทำงานได้ก่อน แล้วค่อยแกะว่ามันคำนวณอะไรอยู่ข้างใน

<div style="text-align:center;margin:10px 0">
<svg width="820" height="150" viewBox="0 0 820 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arOpen" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="40" width="180" height="70" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="104" y="72" font-size="15" font-weight="700" fill="#2e7d32" text-anchor="middle">รัน Physics Lab</text>
  <text x="104" y="94" font-size="12" fill="#555" text-anchor="middle">4 ปริมาณสดๆ</text>
  <rect x="234" y="40" width="180" height="70" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="324" y="72" font-size="15" font-weight="700" fill="#1565c0" text-anchor="middle">แกะดูสูตร</text>
  <text x="324" y="94" font-size="12" fill="#555" text-anchor="middle">raw -&gt; derived</text>
  <rect x="454" y="40" width="180" height="70" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="544" y="72" font-size="15" font-weight="700" fill="#e65100" text-anchor="middle">เติมสูตรเอง</text>
  <text x="544" y="94" font-size="12" fill="#555" text-anchor="middle">4 บรรทัดคณิต</text>
  <rect x="674" y="40" width="132" height="70" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="740" y="72" font-size="15" font-weight="700" fill="#6a1b9a" text-anchor="middle">remix ต่อ</text>
  <text x="740" y="94" font-size="12" fill="#555" text-anchor="middle">เกจของคุณ</text>
  <line x1="194" y1="75" x2="230" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="414" y1="75" x2="450" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="634" y1="75" x2="670" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
</svg>
</div>

เปิด [`s06_physics_viz_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m03-processing/l02-physics-gauges-lab/examples/s06_physics_viz_full.py) รันก่อน เลือกปริมาณใน dropdown แล้วเอียงบอร์ด/เขย่า/ยกขึ้น-ลง — จอโชว์ตัวเลขที่คำนวณเปลี่ยนตามจริง นั่นแหละของที่เราจะแกะแล้วสร้างเองในชุดบทเรียนนี้

> ชุดบทเรียนนี้ไม่ต้องท่องสูตรฟิสิกส์มาก่อน ขอแค่ได้เห็นว่า "ตัวเลขจากเซนเซอร์ กลายเป็นมุม/ความสูง/ระดับเสียงได้ยังไง" แล้วเริ่มอยากรู้ว่าสูตรนั้นหน้าตาเป็นแบบไหน

---

# เป้าหมายของชุดบทเรียนนี้

จบชุดบทเรียนนี้เราจะเดินครบ แล้วปิดท้ายด้วยเกจฟิสิกส์ที่คำนวณเอง:

1. **ทำไมต้อง Processing** — ตัวเลขดิบจากเซนเซอร์ยัง "ไม่พูดภาษาคน" เราต้องแปลงก่อน
2. **รูปแบบหัวใจ** ของทั้งขั้นนี้: `raw → derived → viz` (อ่านดิบ → คำนวณ → แสดงผล)
3. **สี่ปริมาณฟิสิกส์**: มุมเอียง (`dsp.tilt`) · พลังงาน (energy) · ความสูง (`dsp.altitude`) · ระดับเสียง (dBFS)
4. **เลือก widget ให้เข้ากับข้อมูล** — Arc / Bar / Seg7 / Chart อย่างไหนเหมาะกับอะไร
5. ลงมือ: เติม **4 สูตรแปลง** ใน [`s06_physics_viz.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m03-processing/l02-physics-gauges-lab/practice/s06_physics_viz.py) แล้วดูเกจขยับตามการเคลื่อนไหวจริง

ปลายทางของวันนี้: เลือกปริมาณใน dropdown แล้วขยับบอร์ด — ค่าที่ **เราคำนวณเอง** โชว์เป็นตัวเลข + แถบ + กราฟ

> วันนี้เน้น "อ่านดิบเป็น + แปลงเป็น + แสดงเป็น" ส่วนการกรองสัญญาณรบกวนและ FFT เก็บไว้ โมดูล 4 (Analysis)

---

# ชุดบทเรียนนี้อยู่ตรงไหนของวงจร

จำวงจรชีวิตข้อมูล 5 ขั้นจากบทเรียน 1.1–1.3 ได้ไหม — ชุดบทเรียนนี้เราเดินถึง **ขั้นที่ 2: Processing**

<div style="text-align:center;margin:6px 0">
<svg width="920" height="170" viewBox="0 0 920 170" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arLC" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g text-anchor="middle">
    <rect x="10" y="50" width="160" height="64" rx="12" fill="#eceff1" stroke="#90a4ae" stroke-width="2"/>
    <text x="90" y="78" font-size="13" font-weight="700" fill="#607d8b">1 · DAQ</text>
    <text x="90" y="98" font-size="10" fill="#888">อ่านค่าดิบ (2.1–2.2)</text>
    <rect x="196" y="44" width="160" height="76" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="3"/>
    <text x="276" y="72" font-size="14" font-weight="700" fill="#2e7d32">2 · Processing</text>
    <text x="276" y="92" font-size="11" fill="#555">คณิต+ฟิสิกส์</text>
    <text x="276" y="107" font-size="10" fill="#2e7d32">ชุดบทเรียนนี้ (วันนี้)</text>
    <rect x="382" y="50" width="160" height="64" rx="12" fill="#eceff1" stroke="#90a4ae" stroke-width="2"/>
    <text x="462" y="78" font-size="13" font-weight="700" fill="#607d8b">3 · Analysis</text>
    <text x="462" y="98" font-size="10" fill="#888">DSP · FFT (4.1–4.2+)</text>
    <rect x="568" y="50" width="160" height="64" rx="12" fill="#eceff1" stroke="#90a4ae" stroke-width="2"/>
    <text x="648" y="78" font-size="13" font-weight="700" fill="#607d8b">4 · Training</text>
    <text x="648" y="98" font-size="10" fill="#888">ฝึกโมเดล</text>
    <rect x="754" y="50" width="160" height="64" rx="12" fill="#eceff1" stroke="#90a4ae" stroke-width="2"/>
    <text x="834" y="78" font-size="13" font-weight="700" fill="#607d8b">5 · Apps</text>
    <text x="834" y="98" font-size="10" fill="#888">อนุมาน + action</text>
  </g>
  <line x1="170" y1="82" x2="194" y2="82" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <line x1="356" y1="82" x2="380" y2="82" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <line x1="542" y1="82" x2="566" y2="82" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <line x1="728" y1="82" x2="752" y2="82" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <text x="462" y="150" font-size="12" fill="#888" text-anchor="middle">DAQ เก็บค่ามาให้ (ชุดบทเรียนก่อนหน้า) → Processing แปลงให้มีความหมาย (ชุดบทเรียนนี้) → Analysis ขุดลึกต่อ (ชุดบทเรียนถัด ๆ ไป)</text>
</svg>
</div>

> Processing คือสะพานระหว่าง "ตัวเลขที่เซนเซอร์เห็น" กับ "ปริมาณที่คนเข้าใจ" — ถ้าข้ามขั้นนี้ โมเดลกับหน้าจอจะได้แต่ตัวเลขดิบที่ไม่มีความหมาย

---

# ตัวเลขดิบยังไม่พูดภาษาคน

ลองดูของจริง `sensors.bmi270.motion()` คืนอะไรมา:

```python
ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
# เช่น: (0.20, -6.97, 6.87, 1.1, -0.4, 0.3)
```

- ตัวเลขชุดนี้อ่านแล้วบอกอะไรไม่ได้เลย — บอร์ดเอียงกี่องศา? นิ่งหรือขยับ?
- แต่ถ้าเอา `ax, ay, az` ไปเข้าสูตรตรีโกณ จะได้ **มุมเอียง** ที่คนเข้าใจทันที
- นี่คืองานของขั้น Processing: เอาตัวเลขดิบมา **บีบให้เป็นปริมาณที่มีความหมาย**

<div style="text-align:center;margin:8px 0">
<svg width="760" height="120" viewBox="0 0 760 120" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arRD" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="36" width="250" height="52" rx="10" fill="#eceff1" stroke="#90a4ae" stroke-width="2"/>
  <text x="145" y="58" font-size="12" fill="#607d8b" text-anchor="middle">ค่าดิบ: (0.20, -6.97, 6.87)</text>
  <text x="145" y="76" font-size="10" fill="#999" text-anchor="middle">อ่านแล้วไม่รู้เรื่อง</text>
  <rect x="490" y="36" width="250" height="52" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="615" y="58" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">roll ≈ −45 องศา</text>
  <text x="615" y="76" font-size="10" fill="#666" text-anchor="middle">คนเข้าใจทันที</text>
  <line x1="270" y1="62" x2="486" y2="62" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arRD)"/>
  <text x="378" y="52" font-size="12" fill="#ef6c00" text-anchor="middle">dsp.tilt</text>
</svg>
</div>

> คำถามของชุดบทเรียนนี้: **"ตัวเลขจากเซนเซอร์นี้ แปลงเป็นปริมาณที่มีความหมายได้ยังไง?"** — คำตอบคือคณิตกับฟิสิกส์ไม่กี่บรรทัด

---

# รูปแบบหัวใจ — raw → derived → viz

ทุกปริมาณที่เราทำวันนี้เดินตามสามจังหวะเดียวกันเป๊ะ จำโครงนี้ให้ขึ้นใจ เพราะมันคือ **MVP ของชุดบทเรียน (MVP ของบทเรียน 3.1–3.2)**

<div style="text-align:center;margin:6px 0">
<svg width="880" height="150" viewBox="0 0 880 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arM6" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="46" width="240" height="64" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="140" y="74" font-size="15" font-weight="700" fill="#1565c0" text-anchor="middle">1 · raw</text>
  <text x="140" y="96" font-size="11" fill="#666" text-anchor="middle">อ่านค่าดิบจากเซนเซอร์</text>
  <rect x="320" y="46" width="240" height="64" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="440" y="74" font-size="15" font-weight="700" fill="#e65100" text-anchor="middle">2 · derived</text>
  <text x="440" y="96" font-size="11" fill="#666" text-anchor="middle">คำนวณเป็นปริมาณจริง</text>
  <rect x="620" y="46" width="240" height="64" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="740" y="74" font-size="15" font-weight="700" fill="#2e7d32" text-anchor="middle">3 · viz</text>
  <text x="740" y="96" font-size="11" fill="#666" text-anchor="middle">แสดงบนจอ (เกจ/แถบ/กราฟ)</text>
  <line x1="260" y1="78" x2="316" y2="78" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arM6)"/>
  <line x1="560" y1="78" x2="616" y2="78" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arM6)"/>
  <text x="440" y="134" font-size="12" fill="#888" text-anchor="middle">สูตรที่คุณเติมคือจังหวะกลาง (derived) — สองข้างเราเตรียมไว้ให้แล้ว</text>
</svg>
</div>

**MVP ของบทเรียน 3.1–3.2:** สัญญาณดิบ → ปริมาณที่คำนวณได้ → แสดงเห็นบนจอ ครบวง สำหรับอย่างน้อยหนึ่งปริมาณ

> ที่เราให้ dropdown สลับ 4 ปริมาณ ก็เพราะทั้งสี่ใช้โครงเดียวกัน ต่างกันแค่ "สูตรตรงกลาง" — เห็นโครงร่วมแล้วจะเติมได้ทั้งสี่โดยไม่งง

---

# สี่ปริมาณของวันนี้

แต่ละปริมาณมาจากเซนเซอร์ต่างกัน แต่เข้าโครง `raw → derived → viz` เหมือนกันหมด

| ปริมาณ | เซนเซอร์ (raw) | สูตรแปลง (derived) | หน่วย | รันที่ไหน |
|---|---|---|---|---|
| **Tilt** มุมเอียง | IMU `bmi270.motion()` | `dsp.tilt(ax,ay,az)` | องศา | Emulator + บอร์ด |
| **Energy** พลังงาน | IMU `bmi270.motion()` | `abs(accel) - 1g` | g | Emulator + บอร์ด |
| **Altitude** ความสูง | baro `dps368` | `dsp.altitude(p, p0)` | เมตร | Emulator + บอร์ด |
| **Sound** ระดับเสียง | MIC (PDM) | `20·log10(rms/32768)` | dBFS | บอร์ดเท่านั้น |

- สามปริมาณแรกใช้ **IMU/baro** ซึ่ง Emulator จำลองให้ — ซ้อมที่บ้านได้เลย
- ปริมาณเสียง (dBFS) ต้องใช้ไมค์ PDM จริง จึงทำ **บนบอร์ด** เท่านั้น (โค้ดเราเช็กให้ ถ้าไม่มีไมค์ก็ข้าม)

> สังเกตว่า 2 ใน 4 มาจาก IMU ตัวเดียว — เซนเซอร์เดียวแปลงได้หลายปริมาณ ขึ้นอยู่กับ "สูตรที่เราเลือกใช้"

---

# ปูจากชุดบทเรียนก่อนหน้า — เรามีอะไรอยู่ในมือแล้ว

ชุดบทเรียนนี้ไม่ได้เริ่มจากศูนย์ เรายืนบนสองชุดบทเรียนก่อนหน้า:

- **จากบทเรียน 1.4–1.5 (แกะแอปเซนเซอร์)** — โครงร่วม `import → สร้างครั้งเดียว → ลูป → ui.poll` ที่เราจะเจอซ้ำในไฟล์วันนี้ทุกบรรทัด
- **จากบทเรียน 2.1–2.2 (DAQ)** — วิธีอ่านค่าดิบจากเซนเซอร์ (`sensors.bmi270.motion()`, `sensors.dps368...`) วันนี้เราต่อยอดด้วยการ **แปลง** ค่าที่อ่านมา
- **ของใหม่ของวันนี้** — โมดูล `dsp` และ "สูตรฟิสิกส์" ที่ทำให้ค่าดิบมีความหมาย

<div style="text-align:center;margin:8px 0">
<svg width="760" height="96" viewBox="0 0 760 96" font-family="DejaVu Sans, sans-serif">
  <line x1="60" y1="48" x2="700" y2="48" stroke="#cfd8dc" stroke-width="3"/>
  <circle cx="140" cy="48" r="9" fill="#1565c0"/>
  <text x="140" y="30" font-size="12" font-weight="700" fill="#1565c0" text-anchor="middle">บทเรียน 1.4–1.5</text>
  <text x="140" y="72" font-size="11" fill="#777" text-anchor="middle">โครงร่วม</text>
  <circle cx="360" cy="48" r="9" fill="#2e7d32"/>
  <text x="360" y="30" font-size="12" font-weight="700" fill="#2e7d32" text-anchor="middle">บทเรียน 2.1–2.2</text>
  <text x="360" y="72" font-size="11" fill="#777" text-anchor="middle">อ่านค่าดิบ (DAQ)</text>
  <circle cx="600" cy="48" r="10" fill="#ef6c00"/>
  <text x="600" y="30" font-size="12" font-weight="700" fill="#e65100" text-anchor="middle">บทเรียน 3.1–3.2 (วันนี้)</text>
  <text x="600" y="72" font-size="11" fill="#777" text-anchor="middle">แปลงให้มีความหมาย</text>
</svg>
</div>

> ถ้าลืมโครงร่วมของบทเรียน 1.4–1.5 กลับไปเปิด `s02` ทวนสัก 5 นาทีก่อน เพราะไฟล์วันนี้เดินตามโครงนั้นเป๊ะ ต่างกันแค่ในลูปเราคำนวณฟิสิกส์แทนการอ่านโมเดล

---

# รู้จักโมดูล dsp

`dsp` (Digital Signal Processing) คือกล่องเครื่องมือคณิตของ BENTO คำนวณฝั่ง C จึงเร็ว วันนี้เราแตะสองฟังก์ชันสำเร็จรูป + เขียนสูตรเองสองอัน

| กลุ่ม | ตัวอย่าง | ชุดบทเรียนนี้ใช้ |
|---|---|---|
| ฟิวชัน IMU (มุม) | `dsp.tilt(ax,ay,az)` → `(roll,pitch)` | ใช้ (Tilt) |
| ความดัน → ความสูง | `dsp.altitude(p[, p0])` → เมตร | ใช้ (Altitude) |
| ตัวกรองสัญญาณ | `dsp.EMA / Median / Kalman1D` | บทเรียน 4.1–4.2 |
| สภาพอากาศ | `dsp.dew_point / heat_index` | บทเรียน 3.3–3.4 |

- **Tilt** กับ **Altitude** มีฟังก์ชันสำเร็จใน `dsp` — เราแค่เรียกใช้ (แต่จะเข้าใจว่ามันคำนวณอะไร)
- **Energy** กับ **dBFS** ไม่มีฟังก์ชันสำเร็จ — เราเขียนสูตรเองด้วย `math.sqrt` / `math.log10` (นี่คือ "คณิตที่คุณเขียน")

> `dsp` คำนวณฝั่ง C ก็จริง แต่เราจะไม่เรียกแบบกล่องดำ — ทุกฟังก์ชันที่ใช้ เราจะเปิดดูว่ามันแปลงตัวเลขด้วยฟิสิกส์อะไร จะได้ remix เองเป็นในชุดบทเรียนถัด ๆ ไป

---

# Tilt (1) — ฟิสิกส์ของมุมเอียง

Accelerometer ไม่ได้วัด "มุม" ตรงๆ มันวัด **เวกเตอร์แรงโน้มถ่วง** ที่ชี้ลงพื้นเสมอ พอบอร์ดเอียง เวกเตอร์นี้จะกระจายลงสามแกนต่างกัน — เราถอดมุมกลับออกมาด้วยตรีโกณ

<div style="text-align:center;margin:6px 0">
<svg width="720" height="200" viewBox="0 0 720 200" font-family="DejaVu Sans, sans-serif">
  <rect x="60" y="60" width="180" height="110" rx="8" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" transform="rotate(-18 150 115)"/>
  <text x="150" y="45" font-size="12" fill="#1565c0" text-anchor="middle">บอร์ดเอียง</text>
  <line x1="150" y1="115" x2="150" y2="185" stroke="#c62828" stroke-width="3"/>
  <path d="M145,178 L150,188 L155,178 Z" fill="#c62828"/>
  <text x="176" y="180" font-size="12" fill="#c62828">g (แรงโน้มถ่วง)</text>
  <text x="150" y="200" font-size="10" fill="#888" text-anchor="middle">ชี้ลงพื้นเสมอ</text>
  <g transform="translate(420,40)">
    <text x="0" y="0" font-size="13" font-weight="700" fill="#333">ถอดมุมด้วย atan2:</text>
    <text x="0" y="34" font-size="14" fill="#1565c0">pitch = atan2(−ax, √(ay²+az²))</text>
    <text x="0" y="64" font-size="14" fill="#ef6c00">roll  = atan2(ay, az)</text>
    <text x="0" y="104" font-size="12" fill="#666">dsp.tilt ทำสูตรนี้ให้เรา</text>
    <text x="0" y="124" font-size="12" fill="#666">คืน (roll, pitch) เป็นองศา</text>
    <text x="0" y="150" font-size="11" fill="#999">อัตราส่วนของแกนจึงหักล้างหน่วย —</text>
    <text x="0" y="166" font-size="11" fill="#999">ไม่ต้องรู้ว่า accel หน่วยอะไร ก็ได้มุม</text>
  </g>
</svg>
</div>

> เพราะ tilt ใช้ **อัตราส่วน** ของแกน (atan2) หน่วยของ accelerometer จึงหักล้างกัน — นี่คือเหตุผลที่ตัวอย่าง 02 เอา `motion()` ยัดเข้า `dsp.tilt` ได้เลยโดยไม่ต้องแปลงหน่วยก่อน

---

# คณิตเบื้องหลัง Tilt — atan2 ทีละสัญลักษณ์

สูตรเต็มของมุมเอียง เขียนเป็นคณิตได้สองบรรทัด (ผลลัพธ์เป็นเรเดียน คูณ $\frac{180}{\pi}$ ให้เป็นองศา):

$$\text{roll} = \operatorname{atan2}(a_y,\ a_z)$$

$$\text{pitch} = \operatorname{atan2}\!\left(-a_x,\ \sqrt{a_y^{2}+a_z^{2}}\right)$$

อ่านทีละตัว:

- $a_x,\ a_y,\ a_z$ — ความเร่งสามแกนจาก `bmi270.motion()` (หน่วย m/s²)
- $\operatorname{atan2}(y,\ x)$ — อาร์กแทนเจนต์แบบ "รู้ควอดรันต์" คืนมุมเต็มช่วง $-180^\circ$ ถึง $+180^\circ$ (ต่างจาก $\operatorname{atan}$ ที่ได้แค่ครึ่งเดียว)
- $\sqrt{a_y^{2}+a_z^{2}}$ — ขนาดของแรงโน้มถ่วงที่เหลือในระนาบ $y$–$z$ หลังหักแกน $x$ ออก

**ทำไมสำคัญกับชุดบทเรียนนี้:** เพราะสูตรเป็น **อัตราส่วน** ของแกน (เช่น $a_y/a_z$) หน่วยจึงหักล้างกันหมด นี่คือเหตุผลที่ป้อน `motion()` เข้า `dsp.tilt` ได้ตรงๆ โดยไม่ต้องแปลงหน่วยก่อน และ $\operatorname{atan2}$ ยังกันปัญหาหารด้วยศูนย์ตอน $a_z = 0$ (บอร์ดตั้งฉากพอดี) ที่ $\operatorname{atan}$ ธรรมดาทำไม่ได้


▸ **ลองเล่นสด (GeoGebra):** [เปิด Interactive Math Lab](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/interactive/math_lab.html) — ลากเวกเตอร์แรงโน้มถ่วง ดู atan2 คำนวณมุมเอียงสด (applet 5)

---

# Tilt (2) — dsp.tilt แล้วส่งขึ้นเกจ

จาก raw ของ IMU สามค่า เรียก `dsp.tilt` ครั้งเดียวได้มุมสองแกน แล้วเลือกแกนที่เอียงมากสุดมาโชว์:

```python
ax, ay, az, gx, gy, gz = sensors.bmi270.motion()   # raw
roll, pitch = dsp.tilt(ax, ay, az)                 # derived — สูตรที่คุณเติม
dom = pitch if abs(pitch) >= abs(roll) else roll   # แกนที่เอียงมากสุด
seg.text("%d" % int(dom))                          # viz: ตัวเลข
norm = clamp100(abs(dom) / 90.0 * 100)             # 0..90 องศา -> 0..100
bar.value(norm)                                     # viz: แถบ
```

- `dsp.tilt` คืน `(roll, pitch)` — ระวังลำดับ! roll มาก่อน pitch
- `clamp100` บีบค่าเป็น 0..100 เพราะ `Bar`/`Chart` รับช่วงนี้ (เราตั้ง `min=0, max=100`)
- มุม 0..90 map เป็น 0..100 บนแถบ — ตรงไปตรงมา

> `dsp.tilt(ax,ay,az) -> (roll, pitch)` ตรวจจากเอกสาร API แล้ว ลำดับคือ roll ก่อน ถ้าสลับ เกจสองแกนจะสลับกัน — ลองสังเกตตอนรัน

---

# Energy (1) — ขนาดของการเคลื่อนไหว

ถ้าอยากรู้ว่าบอร์ด "ขยับแรงแค่ไหน" (ไม่สนทิศ) เราวัด **ขนาดของเวกเตอร์ความเร่ง** ตอนวางนิ่ง ขนาดนี้ ~ 1g (แรงโน้มถ่วงล้วน) พอเขย่า ขนาดจะเบนออกจาก 1g

<div style="text-align:center;margin:6px 0">
<svg width="760" height="180" viewBox="0 0 760 180" font-family="DejaVu Sans, sans-serif">
  <text x="150" y="30" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">วางนิ่ง</text>
  <line x1="150" y1="150" x2="150" y2="70" stroke="#2e7d32" stroke-width="4"/>
  <path d="M144,78 L150,66 L156,78 Z" fill="#2e7d32"/>
  <text x="150" y="168" font-size="11" fill="#666" text-anchor="middle">|accel| ≈ 1.0g → energy ≈ 0</text>
  <text x="560" y="30" font-size="13" font-weight="700" fill="#ef6c00" text-anchor="middle">เขย่า</text>
  <line x1="560" y1="150" x2="620" y2="60" stroke="#ef6c00" stroke-width="4"/>
  <path d="M611,64 L622,56 L620,70 Z" fill="#ef6c00"/>
  <text x="560" y="168" font-size="11" fill="#666" text-anchor="middle">|accel| = 1.8g → energy = 0.8</text>
  <g transform="translate(310,60)">
    <text x="0" y="0" font-size="14" fill="#333">mag = √(ax² + ay² + az²) / 9.81</text>
    <text x="0" y="30" font-size="14" fill="#ef6c00">energy = |mag − 1.0|</text>
    <text x="0" y="58" font-size="11" fill="#999">ลบ 1g เพื่อเอาฐานแรงโน้มถ่วงออก</text>
    <text x="0" y="74" font-size="11" fill="#999">เหลือเฉพาะ "พลังงานส่วนเกิน" จากการขยับ</text>
  </g>
</svg>
</div>

> นี่ไม่มีฟังก์ชันสำเร็จใน `dsp` — เราเขียนสูตรเองด้วย `math.sqrt` ขนาดเวกเตอร์คือรากที่สองของผลรวมกำลังสอง (พีทาโกรัสสามมิติ) หาร 9.81 ให้เป็นหน่วย g แล้วลบ 1g ออกเพื่อให้ "นิ่ง = 0"

---

# Energy (2) — เขียนสูตรเอง

```python
ax, ay, az, gx, gy, gz = sensors.bmi270.motion()   # raw
mag = math.sqrt(ax*ax + ay*ay + az*az) / 9.81      # ขนาดเวกเตอร์ (m/s² -> g)
energy = abs(mag - 1.0)                             # derived — ลบฐาน 1g
seg.text("%.2f" % energy)                          # viz
norm = clamp100(energy / 2.0 * 100)                # 0..2g -> 0..100
```

- `ax*ax` เร็วกว่า `ax**2` เล็กน้อยบน MicroPython และอ่านง่ายพอกัน
- `motion()` คืนความเร่งหน่วย m/s² (วางนิ่ง ≈ 9.81) เราหาร 9.81 ให้เป็นหน่วย g (วางนิ่ง = 1g) แล้วลบ `1.0` — ถ้าไม่ลบ ตอนนิ่งค่าจะค้างที่ 1 ไม่ใช่ 0
- `abs(...)` กัน energy ติดลบตอน mag < 1g (เช่นตกอิสระชั่วขณะ)

> ทำไมต้อง "ลบ 1g"? เพราะเราสนใจ **การเปลี่ยนแปลง** ไม่ใช่แรงโน้มถ่วงคงที่ นี่คือไอเดียเดียวกับ high-pass filter ที่จะเจอเต็มๆ ในบทเรียน 4.1–4.2

---

# Altitude (1) — ฟิสิกส์ของความดันอากาศ

ยิ่งสูง อากาศยิ่งเบาบาง **ความดันจึงลดลงตามความสูง** ความสัมพันธ์นี้เป็นสูตรมาตรฐาน (barometric formula) `dsp.altitude` ใส่สูตรนี้มาให้แล้ว

<div style="text-align:center;margin:6px 0">
<svg width="760" height="190" viewBox="0 0 760 190" font-family="DejaVu Sans, sans-serif">
  <line x1="80" y1="160" x2="80" y2="20" stroke="#90a4ae" stroke-width="2"/>
  <line x1="80" y1="160" x2="380" y2="160" stroke="#90a4ae" stroke-width="2"/>
  <text x="60" y="24" font-size="11" fill="#666" text-anchor="end">สูง</text>
  <text x="380" y="178" font-size="11" fill="#666" text-anchor="middle">ความดัน (hPa) →</text>
  <path d="M110,150 C180,120 280,60 360,35" fill="none" stroke="#ef6c00" stroke-width="3"/>
  <text x="250" y="80" font-size="11" fill="#ef6c00">ความดันลดเมื่อขึ้นสูง</text>
  <g transform="translate(430,40)">
    <text x="0" y="0" font-size="13" font-weight="700" fill="#333">alt = dsp.altitude(p, p0)</text>
    <text x="0" y="30" font-size="12" fill="#666">p  = ความดันตอนนี้</text>
    <text x="0" y="50" font-size="12" fill="#666">p0 = ความดันตอนเริ่ม (จุด 0 ม.)</text>
    <text x="0" y="82" font-size="11" fill="#999">เราวัด "ความสูงเทียบกับตอนเริ่ม"</text>
    <text x="0" y="98" font-size="11" fill="#999">ยกบอร์ดขึ้น 1 ม. → alt ≈ +1.0</text>
    <text x="0" y="126" font-size="11" fill="#888">p0 จับครั้งเดียวก่อนลูป</text>
  </g>
</svg>
</div>

> ทำไมต้องมี `p0`? ถ้าไม่มีจุดอ้างอิง เราจะได้แต่ "ความสูงเหนือน้ำทะเล" ซึ่งขึ้นกับสภาพอากาศวันนั้น การจับ `p0` ตอนเริ่มทำให้ได้ **ความสูงสัมพัทธ์** ที่แม่นและเห็นผลชัดเวลายกบอร์ด

---

# Altitude (2) — dsp.altitude(p, p0)

```python
# ก่อนลูป: จับความดันอ้างอิงครั้งเดียว
p0, _ = sensors.dps368.pressure_temperature()

# ในลูป:
p, t = sensors.dps368.pressure_temperature()       # raw
alt = dsp.altitude(p, p0)                           # derived — สูตรที่คุณเติม
seg.text("%.1f" % alt)                             # viz (เมตร)
norm = clamp100((alt + 5.0) / 10.0 * 100)          # โชว์ช่วง -5..+5 ม.
```

- `dps368.pressure_temperature()` คืน `(hPa, °C)` — เราใช้แค่ความดัน ส่วนอุณหภูมิทิ้ง (`_`)
- ความดันเปลี่ยนช้า อ่าน 2–8 Hz ก็พอ (ในไฟล์เราหน่วง 120 ms)
- ช่วง ±5 เมตรถูก map ลง 0..100 เพื่อให้เห็นการยกบอร์ดชัดๆ

> `dsp.altitude(p[, p0])` — `p0` เป็น argument ที่ไม่บังคับ ถ้าไม่ใส่จะใช้ความดันมาตรฐานระดับน้ำทะเล (1013.25) เราเลือกใส่ `p0` เอง เพื่อให้จุด 0 อยู่ที่ "ตอนเริ่มโปรแกรม"

---

# Sound dBFS (1) — จากคลื่นเสียงเป็นตัวเลขเดียว

ไมค์คืนคลื่นเสียงเป็นตัวอย่างหลายพันจุดต่อวินาที เราย่อมันเป็น "ระดับความดัง" ตัวเลขเดียวสองก้าว: **RMS** (พลังงานเฉลี่ย) แล้วแปลงเป็น **dBFS** (สเกล log)

<div style="text-align:center;margin:6px 0">
<svg width="820" height="150" viewBox="0 0 820 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arDB" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="44" width="210" height="70" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="119" y="70" font-size="12" font-weight="700" fill="#1565c0" text-anchor="middle">คลื่นเสียง (buf)</text>
  <path d="M28,98 q10,-20 20,0 t20,0 t20,0 t20,0 t20,0 t20,0 t20,0 t20,0" fill="none" stroke="#1565c0" stroke-width="1.6"/>
  <rect x="300" y="44" width="210" height="70" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="405" y="70" font-size="12" font-weight="700" fill="#e65100" text-anchor="middle">RMS</text>
  <text x="405" y="94" font-size="11" fill="#666" text-anchor="middle">√(ค่ากลางกำลังสอง)</text>
  <rect x="586" y="44" width="220" height="70" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="696" y="70" font-size="12" font-weight="700" fill="#2e7d32" text-anchor="middle">dBFS</text>
  <text x="696" y="94" font-size="11" fill="#666" text-anchor="middle">20·log10(rms/32768)</text>
  <line x1="224" y1="79" x2="296" y2="79" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arDB)"/>
  <line x1="510" y1="79" x2="582" y2="79" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arDB)"/>
  <text x="405" y="134" font-size="11" fill="#888" text-anchor="middle">คลื่นหลายพันจุด → พลังงานเฉลี่ย → ระดับความดังตัวเลขเดียว</text>
</svg>
</div>

> `32768` คือค่าเต็มสเกลของตัวอย่างเสียง 16-bit (2¹⁵) เราเทียบ RMS กับค่าเต็มสเกล จึงได้ "dBFS" = decibel เทียบ Full Scale ค่าจะเป็น 0 เมื่อดังสุด และติดลบเมื่อเบาลง

---

# คณิตเบื้องหลัง dBFS — RMS แล้ว log

ย่อคลื่นเสียง $N$ จุดให้เหลือตัวเลขเดียว ด้วยสองก้าว:

$$\text{rms} = \sqrt{\frac{1}{N}\sum_{i=1}^{N} s_i^{2}}$$

$$\text{dBFS} = 20\,\log_{10}\!\left(\frac{\text{rms}}{32768}\right)$$

อ่านทีละตัว:

- $s_i$ — ตัวอย่างเสียงจุดที่ $i$ (16-bit มีค่า $-32768$ ถึง $32767$)
- $N$ — จำนวนจุดใน buffer (`len(mbuf)`)
- $\text{rms}$ — root-mean-square คือ "พลังงานเฉลี่ย" ของคลื่น (ยกกำลังสองก่อนเฉลี่ย ค่าบวก-ลบจึงไม่หักกันเอง)
- $32768 = 2^{15}$ — ค่าเต็มสเกลของ 16-bit จึงได้ decibel ที่ **เทียบ Full Scale**

**ทำไมสำคัญกับชุดบทเรียนนี้:** สัมประสิทธิ์เป็น $20$ ไม่ใช่ $10$ เพราะ RMS เป็น **แอมพลิจูด** ไม่ใช่กำลัง ($20 = 2\times 10$ มาจาก $s^2$ ในนิยามกำลัง) ค่าจึงออกมาเป็น $0$ dBFS เมื่อดังเต็มสเกลและติดลบเมื่อเบาลง ตรงกับที่หูคนรับรู้เสียงแบบ log พอดี

---

# Sound dBFS (2) — โค้ด + เงื่อนไขบอร์ด

```python
if has_mic:                                # PDM มีเฉพาะบนบอร์ด
    pdm.readinto(mbuf)                     # raw: อ่านคลื่นเข้า buffer
    acc = 0
    for s in mbuf:
        acc += s * s                       # ผลรวมกำลังสอง
    rms = math.sqrt(acc / len(mbuf))       # ค่ากลางกำลังสอง
    db = 20 * math.log10(rms / 32768.0)    # derived — สูตรที่คุณเติม
    seg.text("%d" % int(db))              # viz
```

- ไมค์ PDM เป็น **ฮาร์ดแวร์จริง** โค้ดจึงเช็ก `has_mic` ก่อน (บน Emulator จะได้เสียงสังเคราะห์ ไม่ใช่เสียงจริง)
- ต้องเช็ก `rms > 0` ก่อน `log10` เพราะ `log10(0)` ไม่มีค่า (เงียบสนิท = ให้ค่าพื้น -96 dBFS)
- ปิดท้ายด้วย `pdm.deinit()` ใน `finally` — คืนฮาร์ดแวร์ไมค์เสมอ

> ปริมาณนี้ต้องใช้ **เสียงจริงบนบอร์ด** — บนบอร์ดให้ลองปรบมือ/พูดใส่ไมค์ดู ส่วน Emulator เล่นสามปริมาณแรก (Tilt/Energy/Altitude) ได้เต็มที่

---

# ทำไมต้องเป็นสเกล log (decibel)

ทำไม dBFS ใช้ `log10` ไม่ใช่ค่าดิบตรงๆ? เพราะ **หูคนรับรู้เสียงแบบ log** ไม่ใช่แบบเชิงเส้น

- เสียงดังขึ้น "สองเท่า" ในความรู้สึก จริงๆ คือพลังงานเพิ่มขึ้นราว 10 เท่า
- ถ้าโชว์ค่าดิบ (linear) เสียงเบาๆ จะเบียดกันอยู่ล่างสุดจนแยกไม่ออก เสียงดังจะพุ่งชนเพดาน
- สเกล decibel บีบช่วงกว้างมหาศาลให้อ่านง่าย: ตั้งแต่ ~-96 (เงียบ) ถึง 0 (ดังเต็มสเกล)

<div style="text-align:center;margin:6px 0">
<svg width="720" height="120" viewBox="0 0 720 120" font-family="DejaVu Sans, sans-serif">
  <text x="20" y="40" font-size="12" fill="#c62828">linear:</text>
  <rect x="90" y="28" width="600" height="18" fill="#ffebee" stroke="#c62828"/>
  <rect x="640" y="28" width="50" height="18" fill="#c62828"/>
  <text x="360" y="60" font-size="10" fill="#999" text-anchor="middle">เสียงเบาเบียดกันซ้ายสุด อ่านไม่ออก</text>
  <text x="20" y="92" font-size="12" fill="#2e7d32">log (dB):</text>
  <rect x="90" y="80" width="600" height="18" fill="#e8f5e9" stroke="#2e7d32"/>
  <line x1="230" y1="80" x2="230" y2="98" stroke="#2e7d32"/>
  <line x1="370" y1="80" x2="370" y2="98" stroke="#2e7d32"/>
  <line x1="510" y1="80" x2="510" y2="98" stroke="#2e7d32"/>
  <text x="360" y="114" font-size="10" fill="#999" text-anchor="middle">กระจายทั้งช่วง เห็นความต่างของเสียงเบาชัด</text>
</svg>
</div>

> log สเกลไม่ได้มีแค่ในเสียง — ความสว่าง แผ่นดินไหว (Richter) ค่า pH ล้วนใช้ log เพราะธรรมชาติหลายอย่างครอบคลุมช่วงกว้างมาก การ "บีบด้วย log" ทำให้ตัวเลขอ่านออก

---

# เลือก widget ให้เข้ากับข้อมูล

ปริมาณต่างชนิดเหมาะกับการแสดงผลต่างแบบ นี่คือทักษะของขั้น viz — เลือกให้ผู้ใช้ "อ่านออกในพริบตา"

| widget | เหมาะกับ | ใช้กับปริมาณ |
|---|---|---|
| `ui.Seg7` | ตัวเลขเด่นตัวเดียว (headline) | ทุกปริมาณ (ค่าจริง) |
| `ui.Bar` | ระดับเทียบกับช่วง (0..100) | ทุกปริมาณ (normalized) |
| `ui.Chart` | แนวโน้มย้อนหลัง | ทุกปริมาณ (ประวัติ) |
| `ui.Arc` | มุม/เข็มหมุน | เหมาะ Tilt เป็นพิเศษ |

- ไฟล์วันนี้ใช้ **Seg7 + Bar + Chart** ร่วมกันทั้งสี่ปริมาณ ให้เห็นทั้ง "ค่าตอนนี้" และ "แนวโน้ม"
- `Bar` และ `Chart` รับช่วง `min..max` เราตั้ง `0..100` แล้ว normalize ทุกปริมาณเข้าช่วงนี้ด้วย `clamp100`
- ตัวอย่าง 02 เลือก `Arc` คู่กับ tilt เพราะเข็มหมุนสื่อ "มุม" ได้ตรงกว่าแถบ — ลองปรับใช้ในงานทำเองได้

> viz ไม่ใช่แค่ "โชว์ตัวเลข" แต่คือการเลือกภาพที่ตรงกับปริมาณ ระดับเสียงเป็นแถบ มุมเป็นเข็ม แนวโน้มเป็นกราฟ — เลือกผิด ผู้ใช้ก็อ่านยากขึ้นทันที
