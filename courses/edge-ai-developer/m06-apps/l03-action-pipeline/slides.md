---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 6.3 — ท่อสั่งการ: CONF_FLOOR, debounce, cooldown และ on_result"
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

# บทเรียน 6.3 — ท่อสั่งการ: CONF_FLOOR, debounce, cooldown และ on_result
## จาก verdict สู่ action จริง — RGB · เสียง · log

**โมดูล 6 — แอป Edge AI**

**โมดูล 6 · Pillar 5 Apps**

> คาถาประจำบทเรียน: **"โมเดลตอบว่า 'น่าจะใช่' — แต่หน้าที่ของเราคือตัดสินใจว่าจะเชื่อเมื่อไร แล้วค่อยสั่งการ"**

MicroPython บนบอร์ด BENTO (PSoC Edge · Cortex-M55 + Ethos-U55 NPU)

---

# เปิดบทเรียนด้วยของจริงก่อน

เหมือนทุกบทเรียน เราเริ่มแบบ **กลับด้าน** — รันของที่ทำงานได้จริงก่อน แล้วค่อยแกะว่ามันกันการเตือนผิดยังไง

<div style="text-align:center;margin:10px 0">
<svg width="820" height="150" viewBox="0 0 820 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arOpen" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="40" width="180" height="70" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="104" y="72" font-size="15" font-weight="700" fill="#2e7d32" text-anchor="middle">รันท่อสั่งการก่อน</text>
  <text x="104" y="94" font-size="12" fill="#555" text-anchor="middle">ไอ -> ไฟแดง + เสียง</text>
  <rect x="234" y="40" width="180" height="70" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="324" y="72" font-size="15" font-weight="700" fill="#1565c0" text-anchor="middle">แกะดูข้างใน</text>
  <text x="324" y="94" font-size="12" fill="#555" text-anchor="middle">4 ด่านของท่อ</text>
  <rect x="454" y="40" width="180" height="70" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="544" y="72" font-size="15" font-weight="700" fill="#e65100" text-anchor="middle">เติม/จูนเอง</text>
  <text x="544" y="94" font-size="12" fill="#555" text-anchor="middle">NEED_HITS · cooldown</text>
  <rect x="674" y="40" width="132" height="70" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="740" y="72" font-size="15" font-weight="700" fill="#6a1b9a" text-anchor="middle">ต่อยอด</text>
  <text x="740" y="94" font-size="12" fill="#555" text-anchor="middle">6.5–6.6 ออกเน็ต</text>
  <line x1="194" y1="75" x2="230" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="414" y1="75" x2="450" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="634" y1="75" x2="670" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
</svg>
</div>

เปิด [`s16_action_pipeline_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l04-action-pipeline-lab/examples/s16_action_pipeline_full.py) รันเลย เลือกโมเดล Cough แล้วลองไอ — ไฟบนจอจะไล่จาก **ฟ้า (เฝ้าดู)** เป็น **เหลือง (เจอแล้วแต่ยังไม่ชัวร์)** แล้วค่อยเป็น **แดง (ยิงเตือน)** พร้อมเสียงและบรรทัด log

> วันนี้ไม่ต้องเข้าใจทุกบรรทัด ขอแค่สังเกตว่า "ไอครั้งเดียวสั้นๆ" มัน **ไม่ยิงทันที** — ทำไมถึงเป็นแบบนั้น นั่นแหละคือหัวใจของชุดบทเรียนนี้

---

# เป้าหมายของชุดบทเรียนนี้

จบชุดบทเรียนนี้เราจะต่อ "ท่อสั่งการ" (action pipeline) ที่แปลง verdict ของโมเดลให้กลายเป็น action จริง อย่างมีวินัย:

1. **verdict → action** — เอาผลจากโมเดล (`result()`) ไปสั่งการจริง: ไฟ RGB บนจอ · เสียง · log
2. **false positive คืออะไร** และทำไมยิง action ตรงๆ จาก verdict ดิบถึงเตือนพร่ำเพรื่อ
3. **สามเกราะกันเตือนผิด** — เกณฑ์ความมั่นใจ (CONF_FLOOR) · debounce (จับต่อเนื่อง) · cooldown (เว้นช่วง)
4. **smoothing** ด้วย `dsp.EMA` เพื่อกดสัญญาณกระตุกชั่ววูบ
5. **`edge_ai.on_result(cb)`** — รับ verdict แบบ event-driven ต่างจากการ poll ยังไง เลือกอันไหน
6. ลงมือ: เติม [`s16_action_pipeline.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l04-action-pipeline-lab/practice/s16_action_pipeline.py) ให้ครบ 4 ด่านของท่อ แล้วจูนจนกัน false positive ได้

ปลายทางของวันนี้: ทำเสียง/ท่าให้โมเดลจับคลาสเป้าหมายได้ **ต่อเนื่องนานพอ** จอถึงจะยิงไฟแดง + เสียง + log — ไอแวบเดียวไม่นับ

> บทเรียน 6.1–6.2 เราทำแอปต่อโมเดลเดี่ยว ชุดบทเรียนนี้เราต่อ "หลังบ้าน" ของแอปนั้น: ชั้นตัดสินใจที่ทำให้มันเชื่อถือได้พอจะเอาไปใช้จริง

---

# ย้อนดูบทเรียน 1.1–1.3 — เราหยุดไว้ตรง "อ่านผล"

ชุดบทเรียนแรกเราเรียก 4 คำสั่งของ `edge_ai` แล้วเอาคลาสที่ชนะขึ้นจอ จบแค่นั้น — **อ่านผลเป็น** แต่ยัง **ไม่สั่งการ**

<div style="text-align:center;margin:8px 0">
<svg width="860" height="150" viewBox="0 0 860 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arB" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="46" width="200" height="60" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="120" y="70" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">บทเรียน 1.1–1.3</text>
  <text x="120" y="90" font-size="11" fill="#555" text-anchor="middle">result() -> ขึ้นจอ</text>
  <rect x="300" y="46" width="240" height="60" rx="10" fill="#e0f7fa" stroke="#00838f" stroke-width="2"/>
  <text x="420" y="70" font-size="13" font-weight="700" fill="#00838f" text-anchor="middle">บทเรียน 6.3–6.4 (วันนี้)</text>
  <text x="420" y="90" font-size="11" fill="#555" text-anchor="middle">result() -> ตัดสินใจ -> action</text>
  <rect x="620" y="46" width="220" height="60" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="730" y="70" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">บทเรียน 6.5–6.6</text>
  <text x="730" y="90" font-size="11" fill="#555" text-anchor="middle">action -> WiFi/MQTT ออกเน็ต</text>
  <line x1="220" y1="76" x2="298" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arB)"/>
  <line x1="540" y1="76" x2="618" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arB)"/>
  <text x="430" y="132" font-size="12" fill="#888" text-anchor="middle">ของใหม่ชุดบทเรียนนี้ = สองกล่องกลาง "ตัดสินใจ" กับ "action"</text>
</svg>
</div>

- บทเรียน 1.1–1.3: `models` → `select` → `result` → `stop` (อ่านผลออก แต่ผลนั้นไม่ได้ไปทำอะไรต่อ)
- ชุดบทเรียนนี้: ใส่ **ชั้นตัดสินใจ** คั่นระหว่าง "อ่านผล" กับ "สั่งการ" — เพราะ verdict ดิบเชื่อทั้งดุ้นไม่ได้

> ในโลกจริง แอป Edge AI ที่ขายได้ ต่างจาก demo ตรง "ชั้นตัดสินใจ" นี่แหละ demo ยิงทุก verdict ก็ดูเท่ในวิดีโอ แต่ของจริงต้องไม่ปลุกคนทั้งบ้านเพราะแมวเดินผ่าน

---

# ชุดบทเรียนนี้อยู่ตรงไหนของวงจร

เราอยู่ที่ขั้นสุดท้ายของวงจรชีวิตข้อมูล — **Apps (ขั้น 5)** — และเป็นชุดบทเรียนกลางของ โมดูล 6 (Apps I·II·III)

<div style="text-align:center;margin:6px 0">
<svg width="920" height="150" viewBox="0 0 920 150" font-family="DejaVu Sans, sans-serif">
  <g text-anchor="middle">
    <rect x="10" y="40" width="150" height="60" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="85" y="66" font-size="12" font-weight="700" fill="#1565c0">1 · DAQ</text>
    <text x="85" y="86" font-size="10" fill="#888">โมดูล 2</text>
    <rect x="176" y="40" width="150" height="60" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="251" y="66" font-size="12" font-weight="700" fill="#2e7d32">2 · Processing</text>
    <text x="251" y="86" font-size="10" fill="#888">โมดูล 3</text>
    <rect x="342" y="40" width="150" height="60" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="417" y="66" font-size="12" font-weight="700" fill="#e65100">3 · Analysis</text>
    <text x="417" y="86" font-size="10" fill="#888">โมดูล 4</text>
    <rect x="508" y="40" width="150" height="60" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
    <text x="583" y="66" font-size="12" font-weight="700" fill="#6a1b9a">4 · Training</text>
    <text x="583" y="86" font-size="10" fill="#888">โมดูล 5</text>
    <rect x="674" y="34" width="236" height="72" rx="10" fill="#e0f7fa" stroke="#00838f" stroke-width="3"/>
    <text x="792" y="58" font-size="13" font-weight="700" fill="#00838f">5 · Apps  (เราอยู่นี่)</text>
    <text x="792" y="78" font-size="11" fill="#555">6.1–6.2 · 6.3–6.4 · 6.5–6.6</text>
    <text x="792" y="96" font-size="10" fill="#00838f">6.3–6.4 = ท่อสั่งการ + debounce</text>
  </g>
  <line x1="160" y1="70" x2="174" y2="70" stroke="#607d8b" stroke-width="2.2"/>
  <line x1="326" y1="70" x2="340" y2="70" stroke="#607d8b" stroke-width="2.2"/>
  <line x1="492" y1="70" x2="506" y2="70" stroke="#607d8b" stroke-width="2.2"/>
  <line x1="658" y1="70" x2="672" y2="70" stroke="#607d8b" stroke-width="2.2"/>
</svg>
</div>

- **บทเรียน 6.1–6.2 (Apps I)** — แอปต่อโมเดลเดี่ยว: เลือกโมเดล อ่าน scores/latency โชว์สวยๆ
- **บทเรียน 6.3–6.4 (Apps II · วันนี้)** — เอา verdict ไปสั่งการจริง + ชั้นกัน false positive
- **บทเรียน 6.5–6.6 (Apps III)** — รวม verdict กับเซนเซอร์ดิบ (fusion) แล้วส่งออกเน็ตด้วย WiFi/MQTT

> action pipeline ที่เราต่อวันนี้ คือกระดูกสันหลังของทุกแอป Edge AI จริง — บทเรียน 6.5–6.6 แค่ต่อปลายท่อออกไปที่คลาวด์

---

# verdict → action: ท่อ 4 ด่าน

หัวใจของชุดบทเรียนนี้คือมองการสั่งการเป็น **ท่อ (pipeline)** ที่ verdict ต้องผ่านทีละด่านก่อนจะได้ยิง action

<div style="text-align:center;margin:6px 0">
<svg width="940" height="200" viewBox="0 0 940 200" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arP" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g text-anchor="middle">
    <rect x="10" y="60" width="150" height="80" rx="12" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
    <text x="85" y="92" font-size="13" font-weight="700" fill="#455a64">verdict ดิบ</text>
    <text x="85" y="112" font-size="10" fill="#888">result(): label+conf</text>
    <rect x="196" y="60" width="150" height="80" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="271" y="88" font-size="13" font-weight="700" fill="#1565c0">1 · กรอง</text>
    <text x="271" y="108" font-size="10" fill="#555">conf ≥ CONF_FLOOR</text>
    <text x="271" y="124" font-size="10" fill="#888">+ ตรงคลาสเป้าหมาย</text>
    <rect x="382" y="60" width="150" height="80" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="457" y="88" font-size="13" font-weight="700" fill="#2e7d32">2 · debounce</text>
    <text x="457" y="108" font-size="10" fill="#555">จับต่อเนื่อง</text>
    <text x="457" y="124" font-size="10" fill="#888">streak ≥ NEED_HITS</text>
    <rect x="568" y="60" width="150" height="80" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="643" y="88" font-size="13" font-weight="700" fill="#e65100">3 · cooldown</text>
    <text x="643" y="108" font-size="10" fill="#555">พ้นช่วงเว้น</text>
    <text x="643" y="124" font-size="10" fill="#888">กันยิงรัว</text>
    <rect x="754" y="60" width="176" height="80" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
    <text x="842" y="88" font-size="13" font-weight="700" fill="#6a1b9a">4 · action</text>
    <text x="842" y="108" font-size="10" fill="#555">RGB · เสียง · log</text>
    <text x="842" y="124" font-size="10" fill="#888">fire_action()</text>
  </g>
  <line x1="160" y1="100" x2="194" y2="100" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arP)"/>
  <line x1="346" y1="100" x2="380" y2="100" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arP)"/>
  <line x1="532" y1="100" x2="566" y2="100" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arP)"/>
  <line x1="718" y1="100" x2="752" y2="100" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arP)"/>
  <text x="470" y="176" font-size="12" fill="#888" text-anchor="middle">verdict หลุดด่านไหน = ไม่ยิง (ตกด่านคือเรื่องดี — นั่นคือมันกัน false positive ให้เรา)</text>
</svg>
</div>

> อ่านท่อนี้ให้ขึ้นใจ เดี๋ยว 4 ช่องที่เราเติมในไฟล์ฝึก คือด่าน 1→4 นี้เป๊ะ ไล่จากซ้ายไปขวา

---

# ปัญหาที่ต้องแก้ — โมเดลกระพริบ = false positive

ถ้าเรายิง action ทุกครั้งที่ `label == "cough"` โดยไม่กรองอะไรเลย จะเกิดอะไรขึ้น? ลองดูสัญญาณจริง:

<div style="text-align:center;margin:6px 0">
<svg width="900" height="200" viewBox="0 0 900 200" font-family="DejaVu Sans, sans-serif">
  <line x1="40" y1="150" x2="860" y2="150" stroke="#b0bec5" stroke-width="2"/>
  <text x="40" y="176" font-size="11" fill="#888">เวลา →</text>
  <line x1="40" y1="40" x2="40" y2="150" stroke="#b0bec5" stroke-width="1.5"/>
  <text x="20" y="46" font-size="10" fill="#888">conf</text>
  <!-- noisy trace with spurious spikes -->
  <polyline points="40,140 90,138 140,120 190,60 240,135 290,142 340,70 390,138 440,55 470,52 500,50 540,58 590,140 640,138 690,72 740,140 790,138 840,141" fill="none" stroke="#c62828" stroke-width="2.2"/>
  <line x1="40" y1="95" x2="860" y2="95" stroke="#2e7d32" stroke-width="1.6" stroke-dasharray="6 4"/>
  <text x="864" y="99" font-size="11" fill="#2e7d32">CONF_FLOOR</text>
  <!-- spurious spikes markers -->
  <circle cx="190" cy="60" r="5" fill="#ef6c00"/>
  <circle cx="340" cy="70" r="5" fill="#ef6c00"/>
  <circle cx="690" cy="72" r="5" fill="#ef6c00"/>
  <text x="265" y="34" font-size="11" fill="#ef6c00" text-anchor="middle">แหลมเดี่ยวสั้นๆ = เดาผิดชั่ววูบ (false positive)</text>
  <!-- real sustained event -->
  <rect x="440" y="40" width="70" height="110" fill="#2e7d3222"/>
  <text x="475" y="34" font-size="11" fill="#2e7d32" text-anchor="middle">ของจริง = ค้างสูงต่อเนื่อง</text>
</svg>
</div>

- ยอดแหลมเดี่ยวๆ (สีส้ม) คือโมเดล "เดาผิดชั่ววูบ" — คลาสกระพริบขึ้นเหนือเส้นแป๊บเดียวแล้วตกลง
- ของจริง (แถบเขียว) คือคลาสเป้าหมายค้างสูง **ต่อเนื่องหลายเฟรม**
- ถ้ายิงทุก verdict ที่เกินเส้น เราจะเตือน 3 ครั้งจากยอดแหลมปลอม + 1 ครั้งจากของจริง = เตือนผิด 3 ครั้ง

> นี่คือปัญหาเดียวกับปุ่มกดจริงในวงจรดิจิทัลที่เรียกว่า **switch bounce** — หน้าสัมผัสสั่นเป็นสิบครั้งใน 1 การกด วิศวกรแก้ด้วยเทคนิคชื่อ **debounce** เราจะยืมมาใช้กับ verdict ของโมเดลตรงๆ

---

# เกราะชั้นที่ 1 — เกณฑ์ความมั่นใจ (CONF_FLOOR)

ด่านแรกของท่อ กันคำตอบที่โมเดล "เดามากกว่ารู้" ออกไปก่อน ด้วยเส้นความมั่นใจที่เฟิร์มแวร์แนะนำ

```python
hit = (r['label'] == TARGET_CLASS and r['conf'] >= edge_ai.CONF_FLOOR)
#      └ ตรงคลาสที่เราเฝ้าไหม          └ มั่นใจถึงเกณฑ์ไหม (0.50)
```

- `edge_ai.CONF_FLOOR = 0.50` — ต่ำกว่านี้ถือว่า "ยังไม่ชัวร์" อย่าเพิ่งนับเป็นการเจอ
- ด่านนี้ตัดยอดแหลมที่ **เตี้ย** ทิ้งได้ แต่ยอดแหลมที่ **สูงชั่ววูบ** ยังหลุดผ่านมาได้ — จึงต้องมีด่าน 2 ต่อ
- `hit` เป็นแค่ boolean ของ "เฟรมนี้" — ยังไม่ใช่การตัดสินใจยิง แค่บอกว่าเฟรมนี้นับเป็นการเจอ

> เกณฑ์นี้จูนได้ ตั้งสูง (เช่น 0.70) = เตือนผิดน้อยลงแต่พลาดของจริงง่ายขึ้น · ตั้งต่ำ = ไวขึ้นแต่หลอกง่ายขึ้น เราจะได้เล่นกับ trade-off นี้ตอนจูน

---

# เกราะชั้นที่ 2 — debounce (ต้องจับต่อเนื่อง)

ด่านที่ทำให้ "ไอแวบเดียว" ไม่ยิง: นับว่าเจอคลาสเป้าหมาย **ติดกันกี่เฟรม** ต้องครบ `NEED_HITS` ก่อนถึงจะยอม

<div style="text-align:center;margin:6px 0">
<svg width="900" height="150" viewBox="0 0 900 150" font-family="DejaVu Sans, sans-serif">
  <g font-size="12" text-anchor="middle">
    <text x="70" y="24" fill="#455a64" font-weight="700">เฟรม:</text>
    <!-- spurious single hit -->
    <rect x="130" y="40" width="40" height="40" rx="6" fill="#e8f5e9" stroke="#2e7d32"/>
    <text x="150" y="66" fill="#2e7d32">hit</text>
    <rect x="176" y="40" width="40" height="40" rx="6" fill="#fbe9e7" stroke="#c62828"/>
    <text x="196" y="66" fill="#c62828">-</text>
    <text x="196" y="104" fill="#c62828" font-size="10">streak=0 · ไม่ยิง</text>
    <!-- real sustained -->
    <rect x="420" y="40" width="40" height="40" rx="6" fill="#e8f5e9" stroke="#2e7d32"/>
    <text x="440" y="66" fill="#2e7d32">hit</text>
    <rect x="466" y="40" width="40" height="40" rx="6" fill="#e8f5e9" stroke="#2e7d32"/>
    <text x="486" y="66" fill="#2e7d32">hit</text>
    <rect x="512" y="40" width="40" height="40" rx="6" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2.5"/>
    <text x="532" y="66" fill="#1b5e20" font-weight="700">hit</text>
    <text x="486" y="104" fill="#2e7d32" font-size="10">streak=3 ≥ NEED_HITS → ยิง!</text>
  </g>
  <text x="196" y="128" font-size="11" fill="#888" text-anchor="middle">แหลมเดี่ยว: streak รีเซ็ตทันทีที่หลุด</text>
  <text x="486" y="128" font-size="11" fill="#888" text-anchor="middle">ค้างต่อเนื่อง 3 เฟรม: ผ่านด่าน debounce</text>
</svg>
</div>

```python
if hit:
    streak += 1          # เจอต่อเนื่อง เพิ่มตัวนับ
else:
    streak = 0           # หลุดเมื่อไร รีเซ็ตทันที (ยอดแหลมเดี่ยวถูกล้างตรงนี้)
ready = streak >= NEED_HITS
```

> `streak` ทำงานเหมือน "ต้องกดค้าง" ไม่ใช่ "แตะแล้วปล่อย" — สัญญาณรบกวนชั่ววูบผ่านไม่ได้ เพราะมันไม่ค้าง

---

# เกราะชั้นที่ 3 — cooldown (เว้นช่วงกันยิงรัว)

debounce กันยอดแหลมได้ แต่ยังมีอีกปัญหา: ถ้าคลาสเป้าหมายค้างสูง **ยาว** (เช่น ไอเป็นชุด) `streak` จะครบซ้ำๆ ทุกไม่กี่เฟรม → ยิงรัวเป็นสิบครั้ง เราจึงเพิ่ม **ช่วงเว้น (refractory period)**

<div style="text-align:center;margin:6px 0">
<svg width="900" height="150" viewBox="0 0 900 150" font-family="DejaVu Sans, sans-serif">
  <line x1="40" y1="80" x2="860" y2="80" stroke="#b0bec5" stroke-width="2"/>
  <circle cx="120" cy="80" r="9" fill="#c62828"/>
  <text x="120" y="58" font-size="12" font-weight="700" fill="#c62828" text-anchor="middle">ยิง #1</text>
  <rect x="120" y="72" width="260" height="16" fill="#ef6c0033"/>
  <text x="250" y="112" font-size="11" fill="#ef6c00" text-anchor="middle">COOLDOWN_MS (เช่น 3000 ms) — ยิงไม่ได้</text>
  <circle cx="380" cy="80" r="9" fill="#2e7d32"/>
  <text x="380" y="58" font-size="12" font-weight="700" fill="#2e7d32" text-anchor="middle">ยิง #2</text>
  <rect x="380" y="72" width="260" height="16" fill="#ef6c0033"/>
  <text x="510" y="112" font-size="11" fill="#ef6c00" text-anchor="middle">เว้นอีกช่วง</text>
  <circle cx="640" cy="80" r="9" fill="#2e7d32"/>
  <text x="640" y="58" font-size="12" font-weight="700" fill="#2e7d32" text-anchor="middle">ยิง #3</text>
</svg>
</div>

```python
now = time.ticks_ms()
cooled = time.ticks_diff(now, last_fire) >= COOLDOWN_MS
if ready and cooled:            # ครบ debounce "และ" พ้นช่วงเว้น
    fire_action(r['conf'])
    last_fire = now             # เริ่มนับ cooldown ใหม่
    streak = 0
```

> ใช้ `time.ticks_ms()` คู่ `time.ticks_diff()` เสมอ อย่าลบเวลาตรงๆ เพราะตัวนับ ms มีวันวนกลับ (overflow) `ticks_diff` จัดการให้ถูกต้อง

---

# เกราะเสริม — smoothing ด้วย dsp.EMA

ในไฟล์ฉบับเต็ม เราเพิ่มอีกชั้น: ก่อนตัดสินใจ เอาคะแนนคลาสเป้าหมายมา "ปรับให้เนียน" ด้วย EMA (ตัวเดียวกับที่เรียนในบทเรียน 4.1–4.2)

```python
import dsp
smoother = dsp.EMA(alpha=0.35)        # สร้างครั้งเดียวก่อนลูป
...
raw = r['scores'][target_idx]          # คะแนนดิบของคลาสเป้าหมาย
sm  = smoother.update(raw)             # ค่าที่เนียนแล้ว
smooth_ok = sm >= edge_ai.CONF_FLOOR   # ใช้ค่าเนียนเป็นด่านเสริม
```

- EMA ถ่วงน้ำหนักค่าเก่ากับค่าใหม่: `y = alpha*x + (1-alpha)*y_prev` — ยอดแหลมเดี่ยวถูกกดลง
- `alpha` ต่ำ = เนียนมากแต่ตอบช้า · สูง = ไวแต่กระตุก (0.35 คือจุดกลางๆ ที่ใช้ได้ดี)
- debounce กับ smoothing แก้คนละมุม: debounce นับ "จำนวนเฟรม" · smoothing กด "ขนาดของค่า" — ใช้คู่กันยิ่งแน่น

> ไม่จำเป็นต้องมีทั้งสอง ไฟล์ฝึกใช้แค่ debounce ก็กัน false positive ได้แล้ว EMA คือของแถมในฉบับเต็มที่ทำให้เนียนขึ้นอีกขั้น

---

# คณิตของ EMA — สูตรเดียว เข้าใจทั้งชั้น smoothing

หัวใจของ smoothing เขียนเป็นสมการเดียว ค่าที่เนียนแล้วรอบนี้ = ผสมค่าดิบรอบนี้กับค่าที่เนียนแล้วรอบก่อน

$$y_t = \alpha\,x_t + (1-\alpha)\,y_{t-1}$$

อ่านทีละตัว (ภาษาคน):

- $x_t$ — คะแนนดิบของคลาสเป้าหมาย ณ เฟรมนี้ (ค่าที่ได้จาก `r['scores'][target_idx]`)
- $y_t$ — คะแนน **หลังปรับให้เนียน** ที่เราจะเอาไปตัดสินใจ
- $y_{t-1}$ — ค่าเนียนของ **เฟรมก่อนหน้า** (ความทรงจำของตัวกรอง)
- $\alpha$ — น้ำหนักของค่าใหม่ อยู่ระหว่าง $0$ ถึง $1$ (ในโค้ดคือ `alpha=0.35`)

ลองแทนค่าให้เห็นภาพ: ถ้า $\alpha = 0.35$ และตอนนี้ $y_{t-1}=0.20$ แล้วมียอดแหลมเดี่ยว $x_t = 0.90$ พุ่งขึ้นมา

$$y_t = 0.35(0.90) + 0.65(0.20) = 0.315 + 0.130 = 0.445$$

- ยอดแหลม $0.90$ ถูก **กดเหลือ $0.445$** ในเฟรมเดียว — ยังไม่ทะลุ `CONF_FLOOR = 0.50` ด้วยซ้ำ นั่นคือเหตุผลที่ EMA กันแหลมปลอมได้
- ถ้าคะแนนสูงจริง **หลายเฟรมติด** $y_t$ จะไต่ขึ้นเรื่อยๆ จนเกินเส้น — ของจริงที่ค้างนานถึงจะผ่าน

> ทำไม EMA ถึงเบา (เหมาะกับบอร์ด): เก็บสถานะแค่ตัวเดียว ($y_{t-1}$) ไม่ต้องเก็บ buffer ย้อนหลัง — คนละเรื่องกับ moving-average ที่ต้องจำ $N$ ค่า นี่คือเหตุผลที่มันวิ่งได้สบายบน Cortex-M55 ทุกเฟรม

---

# คณิตของ "ยิงตอนขอบขึ้น" — rising edge past threshold

debounce ที่เราต่อ ไม่ได้ยิงตอนคะแนน "สูง" เฉยๆ — มันยิงตอนคะแนน **ข้ามเส้นจากล่างขึ้นบน** (rising edge) แล้วค้างครบจำนวนเฟรม เขียนเป็นสองเงื่อนไข

ให้ $s_t$ = คะแนนที่เนียนแล้ว, $\theta$ = เกณฑ์ (`CONF_FLOOR`), $H$ = `NEED_HITS`

**1) นับความต่อเนื่อง (streak):**

$$c_t = \begin{cases} c_{t-1} + 1, & s_t \ge \theta \quad (\text{hit}) \\ 0, & s_t < \theta \quad (\text{miss}) \end{cases}$$

**2) ยิงเฉพาะ "ขอบขึ้น" ของความพร้อม** — ครบเกณฑ์รอบนี้ แต่รอบก่อนยังไม่ครบ:

$$\text{fire}_t = [\,c_t \ge H\,] \;\wedge\; [\,c_{t-1} < H\,] \;\wedge\; [\,t - t_\text{last} \ge T_\text{cool}\,]$$

อ่านเป็นภาษาคน:

- $[\,c_t \ge H\,]$ — จับคลาสเป้าหมายได้ต่อเนื่องครบแล้ว (ผ่าน debounce)
- $[\,c_{t-1} < H\,]$ — **เพิ่งครบเดี๋ยวนี้** ไม่ใช่ครบมาตั้งนานแล้ว → กันยิงซ้ำทุกเฟรมตอนคะแนนค้างยาว
- $[\,t - t_\text{last} \ge T_\text{cool}\,]$ — พ้นช่วง cooldown จากครั้งก่อน (`COOLDOWN_MS`)

<div style="text-align:center;margin:6px 0">
<svg width="820" height="140" viewBox="0 0 820 140" font-family="DejaVu Sans, sans-serif">
  <line x1="40" y1="100" x2="780" y2="100" stroke="#b0bec5" stroke-width="1.6"/>
  <line x1="40" y1="30" x2="40" y2="100" stroke="#b0bec5" stroke-width="1.6"/>
  <text x="18" y="36" font-size="10" fill="#888">s(t)</text>
  <line x1="40" y1="64" x2="780" y2="64" stroke="#2e7d32" stroke-width="1.5" stroke-dasharray="6 4"/>
  <text x="784" y="68" font-size="10" fill="#2e7d32">θ</text>
  <polyline points="40,96 120,94 200,90 280,60 360,44 440,42 520,50 600,88 680,92 760,95" fill="none" stroke="#1565c0" stroke-width="2.4"/>
  <circle cx="300" cy="53" r="6" fill="#c62828"/>
  <text x="300" y="34" font-size="11" fill="#c62828" text-anchor="middle">ขอบขึ้น = ยิงที่นี่</text>
  <text x="470" y="120" font-size="10" fill="#888" text-anchor="middle">ค้างเหนือเส้นต่อไป = ไม่ยิงซ้ำ (เพราะ c(t-1) ครบแล้ว)</text>
</svg>
</div>

> ทำไมต้อง "ขอบขึ้น" ไม่ใช่ "อยู่เหนือเส้น": ถ้ายิงทุกเฟรมที่ $s_t \ge \theta$ พอคะแนนค้างสูงยาวๆ จะยิงรัวเป็นสิบครั้ง เงื่อนไข $c_{t-1} < H$ ทำให้ยิง **ครั้งเดียวต่อหนึ่งเหตุการณ์** — นี่คือหลักการเดียวกับ edge-triggered interrupt ในโลก embedded

---

# รู้จัก edge_ai.on_result(cb) — รับผลแบบ event-driven

จนถึงตอนนี้เรา **poll** — เรียก `result()` เองทุกรอบลูป แต่ `edge_ai` มีอีกวิธี: ให้เฟิร์มแวร์ **โทรกลับ** หาเราเมื่อมีเหตุการณ์

```python
def on_change(r):                     # เฟิร์มแวร์เรียกเมื่อคลาสเปลี่ยน (และทวนราววินาทีละครั้ง)
    print("คลาสใหม่:", r['label'], "%.0f%%" % (r['conf']*100))

edge_ai.on_result(on_change)          # ลงทะเบียน callback
...
edge_ai.on_result(None)               # ถอนตอนจบ (คู่กับตอนลงทะเบียน)
```

- `cb(dict)` รับ dict verdict แบบเดียวกับ `result()` — รันใน **MicroPython scheduler context** ปลอดภัยกับ `print`/UI
- เฟิร์มแวร์ยิง callback ให้ **ทันทีที่คลาสที่ชนะเปลี่ยน** และทวนคลาสเดิมราววินาทีละครั้ง ไม่ใช่ทุกเฟรม
- เราไม่ต้องเช็ก `seq` เอง ไม่ต้องวนถาม — เหมือน "รอสายเข้า" แทน "โทรถามซ้ำๆ"

> จากซอร์สเฟิร์มแวร์ (ยังไม่เปิดเผย): callback ผูกกับ INTENT event ที่ส่งตอนคลาสเปลี่ยน และส่งซ้ำคลาสเดิมห่างกันอย่างน้อยราว 1 วินาที — ไม่ใช่ทุก result

---

# on_result กับ poll — เลือกอันไหน

สองวิธีนี้ไม่ได้มีอันถูกอันผิด มันเหมาะกับงานคนละแบบ ชุดบทเรียนนี้เราใช้ **ทั้งคู่** ในฉบับเต็ม

| | `result()` (poll) | `on_result(cb)` (event) |
|---|---|---|
| ใครเป็นคนเรียก | เราเรียกเองทุกรอบลูป | เฟิร์มแวร์เรียกให้ตอนคลาสเปลี่ยน (และทวนราววินาทีละครั้ง) |
| ได้ผลบ่อยแค่ไหน | ทุกเฟรม (นับ streak ได้) | ตอนเปลี่ยนคลาส + ทวนราววินาทีละครั้ง |
| เหมาะกับ | **debounce / smoothing** (ต้องนับต่อเฟรม) | **log การเปลี่ยนคลาส** · action ง่ายๆ |
| ต้องเช็ก `seq` เอง | ใช่ | ไม่ต้อง |

- **debounce ต้องใช้ poll** เพราะต้องนับว่าคลาสค้างมากี่เฟรม — event ที่ยิงเฉพาะตอน "เปลี่ยน" นับต่อเนื่องไม่ได้
- **log เหมาะกับ on_result** เพราะเราอยากบันทึกเฉพาะ "ตอนคลาสเปลี่ยน" ไม่ใช่ทุกเฟรม (จำคลาสล่าสุดไว้ แล้วข้ามรอบที่เฟิร์มแวร์ทวนคลาสเดิม)
- ในฉบับเต็ม: ลูปหลัก poll เพื่อ debounce+action · `on_result` แยกไปทำ log การเปลี่ยนคลาส — ต่างคนต่างอ่านสถานะ ไม่ชนกัน

> จำหลักไว้: **งานที่ต้องนับเวลา/จำนวนเฟรม → poll · งานที่แค่ตอบสนองต่อ "เหตุการณ์" → callback** นี่คือ pattern ที่เจอทั่วงาน embedded

---

# ช่องทางของ action — RGB · เสียง · log

พอ verdict ผ่านครบ 4 ด่าน เราจะสั่งการออกไป 3 ช่องทางพร้อมกัน แต่ละช่องสื่อสารกับคนคนละแบบ

<div style="text-align:center;margin:6px 0">
<svg width="900" height="180" viewBox="0 0 900 180" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arA" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="360" y="20" width="180" height="50" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="450" y="42" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">fire_action()</text>
  <text x="450" y="60" font-size="10" fill="#888" text-anchor="middle">ผ่านครบ 4 ด่านแล้ว</text>
  <rect x="60" y="120" width="220" height="50" rx="10" fill="#fbe9e7" stroke="#c62828" stroke-width="2"/>
  <text x="170" y="142" font-size="13" font-weight="700" fill="#c62828" text-anchor="middle">RGB (ภาพ)</text>
  <text x="170" y="160" font-size="10" fill="#888" text-anchor="middle">light.color(RED)</text>
  <rect x="340" y="120" width="220" height="50" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="450" y="142" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">เสียง</text>
  <text x="450" y="160" font-size="10" fill="#888" text-anchor="middle">ui.tone / ui.sfx</text>
  <rect x="620" y="120" width="220" height="50" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="730" y="142" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">log</text>
  <text x="730" y="160" font-size="10" fill="#888" text-anchor="middle">lcd.console + counter</text>
  <line x1="430" y1="70" x2="200" y2="118" stroke="#607d8b" stroke-width="2" marker-end="url(#arA)"/>
  <line x1="450" y1="70" x2="450" y2="118" stroke="#607d8b" stroke-width="2" marker-end="url(#arA)"/>
  <line x1="470" y1="70" x2="700" y2="118" stroke="#607d8b" stroke-width="2" marker-end="url(#arA)"/>
</svg>
</div>

- **RGB** เตือนคนที่มองเห็น (สถานะปัจจุบัน) · **เสียง** เตือนคนที่ไม่ได้มอง · **log** เก็บหลักฐานไว้ตรวจย้อนหลัง
- ในงานจริง action อาจเป็น เปิดรีเลย์ · สั่นมอเตอร์ · ส่ง MQTT — โครงเดียวกัน แค่เปลี่ยนปลายท่อ

> แยกฟังก์ชัน `fire_action()` ออกมาต่างหาก ทำให้ "จะทำอะไรตอนยิง" แก้ที่เดียวจบ ไม่ปนกับตรรกะ debounce

---

# action ช่อง RGB — ไฟสถานะบนจอ

บอร์ดไม่มี LED RGB แยกให้สั่งตรงๆ เราจึงทำ "ไฟ RGB" เป็น **การ์ดสีบนจอ** ที่เปลี่ยนสีตามสถานะของท่อ — เห็นชัดว่าตอนนี้ pipeline อยู่ด่านไหน

```python
light = ui.Panel(x=380, y=48, w=120, h=120, color=LIGHT_OFF)  # สร้างครั้งเดียว
...
light.color(CYAN)     # กำลังเฝ้าดู (ยังไม่เจอเป้าหมาย)
light.color(AMBER)    # เจอแล้วแต่ streak ยังไม่ครบ
light.color(RED)      # ยิง! ผ่านครบทุกด่าน
```

| สี | สถานะ pipeline | หมายความว่า |
|---|---|---|
| เทา (off) | ยังไม่เริ่ม | รอผลแรก |
| ฟ้า (CYAN) | watching | เฝ้าดูอยู่ ไม่เจอคลาสเป้าหมาย |
| เหลือง (AMBER) | streak กำลังนับ | เจอแล้ว แต่ยังไม่ต่อเนื่องพอ |
| แดง (RED) | ALERT | ยิง action แล้ว |

> ไล่สีจากฟ้า→เหลือง→แดง ทำให้ผู้ใช้ "เห็น" ว่าท่อกำลังกันหรือกำลังจะยิง — โปร่งใสกว่าไฟติด/ดับเฉยๆ และช่วยเราดีบักตอนจูนด้วย

---

# action ช่องเสียง — ui.tone / ui.sfx

เสียงเตือนคนที่ไม่ได้จ้องจอ BENTO มีสองทางให้เลือก ทั้งคู่เป็น API จริงบนบอร์ด

```python
if hasattr(ui, "tone"):
    ui.tone(76, ui.WAVE_SINE, 140, 160)   # โน้ต MIDI 76 · รูปคลื่น · ความแรง (velocity) · ยาว 160 ms
elif hasattr(ui, "sfx"):
    ui.sfx(ui.SFX_UI_DENY)                # เอฟเฟกต์สำเร็จรูป
```

- `ui.tone(note, wave, ...)` — โน้ตดนตรีสั้นๆ กำหนดความสูงต่ำได้ (โน้ต MIDI 60 = โดกลาง, 76 = มีสูง)
- `ui.sfx(id)` — เสียงเอฟเฟกต์สำเร็จรูป เช่น `ui.SFX_UI_DENY`, `ui.SFX_UI_SELECT`
- ห่อด้วย `hasattr(ui, "tone")` เสมอ — บางบอร์ด/Emulator อาจไม่มีลำโพง โค้ดจะได้ไม่พังทั้งแอปเพราะเรื่องเสียง

> เลือกเสียงให้ตรงความหมาย: เตือนภัยควรเป็นเสียงสูง-สะดุด ไม่ใช่เสียงนุ่มๆ ที่คนมองข้าม — action ที่ดีต้อง "สื่อสาร" ไม่ใช่แค่ "ดัง"

---

# action ช่อง log — บันทึกไว้ตรวจย้อนหลัง

action ที่มองไม่เห็นตอนเกิด แต่สำคัญที่สุดสำหรับงานจริง: **log** — เพราะเราต้องตอบได้ว่า "มันเตือนกี่ครั้ง ตอนไหน มั่นใจเท่าไร"

```python
alerts += 1                                        # ตัวนับจำนวนครั้ง
lcd.console('<span class=error> ALERT #%d @%dms: %s (conf %.0f%%)</span>'
            % (alerts, time.ticks_ms(), TARGET_CLASS, r['conf'] * 100))
```

- `lcd.console(...)` พิมพ์บรรทัด log พร้อม timestamp + ความมั่นใจ ณ ตอนยิง
- ตัวนับ `alerts` โชว์บนจอ — เห็นภาพรวมว่าเตือนไปกี่ครั้งแล้ว
- ในฉบับเต็มยังนับ `blocked` = จำนวนครั้งที่ pipeline **กันการยิงซ้ำไว้** — ทำให้เห็นว่าเกราะทำงานจริง

> log คือความต่างระหว่าง "ของเล่น" กับ "ของใช้งาน" ถ้าเตือนผิดกลางดึก คุณต้องเปิด log มาดูได้ว่าเกิดจากอะไร บทเรียน 6.5–6.6 เราจะส่ง log นี้ขึ้นคลาวด์
