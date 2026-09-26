---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 1.6 — แกะแอป Edge AI: ทะเบียนโมเดล verdict และ action"
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

# บทเรียน 1.6 — แกะแอป Edge AI: ทะเบียนโมเดล verdict และ action
## จาก verdict สู่ action

**โมดูล 1 — เริ่มต้น: รันของจริงแล้วแกะดูข้างใน**

**Onboarding — กลับด้าน (แกะแอป Edge AI)**

> คาถาประจำบทเรียน: **"โมเดลบอกว่า 'เจออะไร' เป็นแค่ครึ่งเดียว — Edge AI ที่ใช้งานได้จริงต้อง 'ลงมือทำอะไรต่อ' เมื่อคำตอบเข้าเงื่อนไข"**

MicroPython บนบอร์ด BENTO (PSoC Edge · Cortex-M55 + Ethos-U55 NPU)

---

# เปิดบทเรียนด้วยของจริงก่อน

ยังใช้แนว **กลับด้าน** เหมือนสองชุดบทเรียนแรก — ชุดบทเรียนนี้เราจะรันแอป Edge AI ที่ทำงานได้จริงก่อน แล้วค่อยแกะกายวิภาคของมัน แล้ว remix เป็นของเราเอง

<div style="text-align:center;margin:10px 0">
<svg width="820" height="150" viewBox="0 0 820 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arOpen3" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="40" width="180" height="70" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="104" y="72" font-size="15" font-weight="700" fill="#2e7d32" text-anchor="middle">รันแอปจริงก่อน</text>
  <text x="104" y="94" font-size="12" fill="#555" text-anchor="middle">เมนู 12 / Motion 13</text>
  <rect x="234" y="40" width="180" height="70" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="324" y="72" font-size="15" font-weight="700" fill="#1565c0" text-anchor="middle">แกะกายวิภาค</text>
  <text x="324" y="94" font-size="12" fill="#555" text-anchor="middle">select→result→action</text>
  <rect x="454" y="40" width="180" height="70" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="544" y="72" font-size="15" font-weight="700" fill="#e65100" text-anchor="middle">remix เอง</text>
  <text x="544" y="94" font-size="12" fill="#555" text-anchor="middle">สลับโมเดล + action</text>
  <rect x="674" y="40" width="132" height="70" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="740" y="72" font-size="15" font-weight="700" fill="#6a1b9a" text-anchor="middle">อยากสร้างต่อ</text>
  <text x="740" y="94" font-size="12" fill="#555" text-anchor="middle">โมดูล 6 (Apps)</text>
  <line x1="194" y1="75" x2="230" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen3)"/>
  <line x1="414" y1="75" x2="450" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen3)"/>
  <line x1="634" y1="75" x2="670" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen3)"/>
</svg>
</div>

นี่คือขั้น **Investigate → Modify** ของ PRIMM: เราเห็นแอปทำงานแล้ว (Run) ชุดบทเรียนนี้จะเปิดฝาดูข้างใน (Investigate) แล้วดัดแปลง (Modify) ให้เป็นแอปของเรา

> บทเรียน 1.1–1.3 เราเห็นเมนูรู้จำท่าทาง บทเรียน 1.4–1.5 เราแกะแอปเซนเซอร์ — ชุดบทเรียนนี้รวมสองอย่าง: แกะ "แอป Edge AI" ให้ขาด แล้วต่อยอดจาก "อ่านผล" ไปสู่ "สั่งการ"

---

# เป้าหมายของชุดบทเรียนนี้

จบชุดบทเรียนนี้เราจะเดินครบ 4 เรื่อง แล้วปิดท้ายด้วยการ remix แอป Edge AI ของเราเอง:

1. **กายวิภาคของแอป Edge AI ตัวเดียว** — 3 จังหวะ: `select` → `result` → **action**
2. **ทะเบียนโมเดล (registry)** — เลือกโมเดลจากชื่อด้วย `find_model()` ไม่ hard-code index
3. **เส้นทาง verdict → screen** — คำตอบของโมเดลกลายเป็นภาพบนจอได้ยังไง
4. **verdict → action** — เพิ่ม "การกระทำจริง" เมื่อคำตอบเข้าเงื่อนไข + รู้จัก `on_result()`
5. ลงมือ: remix [`s03_anatomy_edgeai.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l07-verdict-action-lab/practice/s03_anatomy_edgeai.py) — สลับโมเดล + สั่งการเมื่อเจอคลาสเป้าหมาย

ปลายทางของวันนี้: แอปเฝ้าจับ "โมเดลเดียว 1 คลาส" ที่พอเจอคลาสเป้าหมายเกินเกณฑ์ **บี๊บ + ขึ้นแบนเนอร์** เอง

> วันนี้เราไม่ได้แค่ "อ่านผล" (บทเรียน 1.1–1.3) แต่ทำให้ผลนั้น **สั่งการอะไรบางอย่างได้** — นี่คือประตูสู่ โมดูล 6 (Apps)

---

# ชุดบทเรียนนี้อยู่ตรงไหนของคอร์ส

บทเรียน 1.6–1.7 เป็นบทเรียน **ปิดกล่อง Onboarding** — สองชุดบทเรียนก่อนกลับด้าน "แอปเซนเซอร์" และตอนนี้เรากลับด้าน "แอป Edge AI"

<div style="text-align:center;margin:8px 0">
<svg width="820" height="120" viewBox="0 0 820 120" font-family="DejaVu Sans, sans-serif">
  <line x1="60" y1="60" x2="760" y2="60" stroke="#cfd8dc" stroke-width="3"/>
  <circle cx="150" cy="60" r="9" fill="#2e7d32"/>
  <text x="150" y="40" font-size="12" font-weight="700" fill="#2e7d32" text-anchor="middle">บทเรียน 1.1–1.3</text>
  <text x="150" y="86" font-size="11" fill="#777" text-anchor="middle">รันเมนู 6 โมเดล</text>
  <circle cx="360" cy="60" r="9" fill="#1565c0"/>
  <text x="360" y="40" font-size="12" font-weight="700" fill="#1565c0" text-anchor="middle">บทเรียน 1.4–1.5</text>
  <text x="360" y="86" font-size="11" fill="#777" text-anchor="middle">แกะแอปเซนเซอร์</text>
  <circle cx="570" cy="60" r="11" fill="#ef6c00"/>
  <text x="570" y="38" font-size="12" font-weight="700" fill="#e65100" text-anchor="middle">บทเรียน 1.6–1.7 (วันนี้)</text>
  <text x="570" y="86" font-size="11" fill="#777" text-anchor="middle">แกะแอป Edge AI + action</text>
  <circle cx="720" cy="60" r="9" fill="#6a1b9a"/>
  <text x="720" y="40" font-size="12" font-weight="700" fill="#6a1b9a" text-anchor="middle">บทเรียน 2.1–2.2+</text>
  <text x="720" y="86" font-size="11" fill="#777" text-anchor="middle">Pillar 1: DAQ</text>
</svg>
</div>

- **บทเรียน 1.1–1.3** ให้เราเห็นปลายทาง (เมนูรู้จำท่าทาง) และรู้จัก 4 คำสั่ง `models`/`select`/`result`/`stop`
- **บทเรียน 1.6–1.7** ต่อยอด: จากอ่านผลเฉยๆ ไปสู่ "อ่านผลแล้วลงมือ" — และจากเมนูหลายโมเดล ไปสู่แอปโฟกัสโมเดลเดียว
- จบชุดบทเรียนนี้ Onboarding ครบ แล้วบทเรียน 2.1–2.2 เราเริ่มลงลึกเก็บข้อมูลเซนเซอร์ของเราเอง (DAQ)

> "กลับด้าน" ยังทำงานเหมือนเดิม: เห็นของสำเร็จก่อน แล้วย้อนเข้าใจ — พอถึง โมดูล 6 (Apps) คุณจะกลับมามองแอปวันนี้แล้วต่อยอดเป็นระบบจริงได้

---

# ทบทวนเร็ว — 4 คำสั่งจากบทเรียน 1.1–1.3

ก่อนแกะแอป เรียก 4 คำสั่งของ `edge_ai` ที่เจอในบทเรียน 1.1–1.3 กลับมาในหัวก่อน ชุดบทเรียนนี้เราจะต่อยอดจากตรงนี้พอดี:

| คำสั่ง | ทำอะไร |
|---|---|
| `edge_ai.models()` | คืน list ของ dict — ทะเบียนโมเดลทั้งหมด `{index, name, sensor, labels}` |
| `edge_ai.select(n)` | สั่งให้ CM55 รันโมเดลหมายเลข `n` (ส่งคำสั่งแล้วรอยืนยัน) |
| `edge_ai.result()` | ผลอนุมานล่าสุดเป็น dict หรือ `None` — มี `label`/`conf`/`scores`/`seq`/`latency_ms` |
| `edge_ai.stop()` | หยุดเครื่องยนต์ให้ว่าง (idle) |
| `edge_ai.CONF_FLOOR` | ค่าคงที่ `0.50` — ต่ำกว่านี้ถือว่า "ยังไม่ชัวร์" |

ชุดบทเรียนนี้เพิ่มอีกสองแนวคิดบนฐานนี้: **เลือกโมเดลจากชื่อ** (แทน index) และ **`on_result()`** (แทนการ poll เอง)

> ถ้ายังไม่แม่น เปิด [`s01_first_inference.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l03-first-inference-lab/solution/s01_first_inference.py) อ่านทวนก่อน — ชุดบทเรียนนี้ยืนบนคำสั่งเดิมเป๊ะ แค่ประกอบมันเป็น "แอปที่ลงมือทำ" ได้

---

# จากเมนู 6 โมเดล สู่ "แอปตัวเดียว"

บทเรียน 1.1–1.3 ใช้ [`12_edge_ai_menu.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l02-edge-ai-module/examples/12_edge_ai_menu.py) — เมนูสลับได้ทั้ง 6 โมเดล เหมาะกับ "สำรวจว่ามีอะไรบ้าง" แต่แอปใช้งานจริงมักโฟกัส **โมเดลเดียว** แล้วทำงานให้ดีที่สุด

<div style="text-align:center;margin:6px 0">
<svg width="860" height="170" viewBox="0 0 860 170" font-family="DejaVu Sans, sans-serif">
  <rect x="14" y="20" width="400" height="130" rx="12" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
  <text x="214" y="46" font-size="14" font-weight="700" fill="#455a64" text-anchor="middle">12 · เมนู 6 โมเดล (บทเรียน 1.1–1.3)</text>
  <text x="214" y="72" font-size="12" fill="#555" text-anchor="middle">dropdown สลับได้ทุกตัว</text>
  <text x="214" y="94" font-size="12" fill="#555" text-anchor="middle">"มีโมเดลอะไรให้เล่นบ้าง?"</text>
  <text x="214" y="120" font-size="11" fill="#888" text-anchor="middle">เหมาะกับสำรวจ / เดโม</text>
  <rect x="446" y="20" width="400" height="130" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="646" y="46" font-size="14" font-weight="700" fill="#e65100" text-anchor="middle">13 → s03 · แอปโมเดลเดียว (ชุดบทเรียนนี้)</text>
  <text x="646" y="72" font-size="12" fill="#555" text-anchor="middle">โฟกัสโมเดลเดียว + ลงมือ</text>
  <text x="646" y="94" font-size="12" fill="#555" text-anchor="middle">"เจอ shaking แล้วทำอะไรต่อ?"</text>
  <text x="646" y="120" font-size="11" fill="#888" text-anchor="middle">เหมาะกับสินค้า / งานจริง</text>
</svg>
</div>

- [`13_edge_ai_motion.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l06-edge-ai-app-anatomy/examples/13_edge_ai_motion.py) คือฝาแฝดโมเดลเดียวของ 12 — เลือก Motion ด้วย `find_model()` แล้ววนอ่านผล
- แอปชุดบทเรียนนี้ ([`s03_anatomy_edgeai.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l07-verdict-action-lab/practice/s03_anatomy_edgeai.py)) ต่อยอดจาก 13: เพิ่ม "**สั่งการ**เมื่อเจอคลาสเป้าหมาย" เข้าไป

> โลกจริงส่วนใหญ่ไม่ได้ให้ผู้ใช้เลือกโมเดลเอง — นาฬิกาตรวจการล้ม รันโมเดลเดียวตลอด แล้วลงมือเมื่อเจอ นี่คือรูปแบบที่เรากำลังแกะ

---

# รันของจริงก่อน — เห็นแอปทำงานเลย

ก่อนแกะโค้ด รันสองแอปอ้างอิงให้เห็นของจริงในมือก่อน (ทำได้ทั้ง Emulator และบอร์ด):

1. เปิด **ide.tesaiot.dev** หรือ BENTO IDE เสียบบอร์ด
2. รัน [`13_edge_ai_motion.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l06-edge-ai-app-anatomy/examples/13_edge_ai_motion.py) — โมเดล Motion โมเดลเดียว
3. **เขย่าบอร์ด / วาดวงกลม / วางนิ่ง** ดูคลาสที่ชนะ (`shaking`/`circle`/`idle`) + แถบคะแนน + latency เปลี่ยนสด
4. สังเกต: มัน **รู้จำท่าของคุณได้แล้ว** ตั้งแต่ยังไม่แตะโค้ด — นั่นแหละคือของที่เราจะแกะ
5. ลอง [`12_edge_ai_menu.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l02-edge-ai-module/examples/12_edge_ai_menu.py) เทียบด้วย เห็นว่า "โมเดลเดียว" กับ "เมนู" ต่างกันตรงไหน

> ความรู้สึก "มันทำงานได้แล้ว ฉันอยากรู้ว่าทำไม" คือเชื้อเพลิงของชุดบทเรียนนี้ — จับความสงสัยนั้นไว้ แล้วเราจะเปิดฝาดูข้างในกันทีละส่วน

---

# จอ Emulator ที่รันได้จริง

ไม่มีบอร์ดในมือก็เริ่มได้ — นี่คือหน้า Edge AI บน BENTO Emulator ที่รันในเบราว์เซอร์ล้วนๆ ทุกคนได้ลองมือพร้อมกัน:

![หน้า Edge AI บน BENTO Emulator: dropdown เลือกโมเดล Motion Detection ปุ่ม Load และ Stop คลาสที่ชนะ idle เวลาอนุมาน และแถบความมั่นใจของ idle circle shaking w:680](../../assets/img/edge_ai_page.png)

จอ emulator ที่รันได้จริง — หน้า Edge AI ของ BENTO (เลือกโมเดล ดู verdict + แถบคะแนน + conf สดๆ)

- ทุกจังหวะที่เราจะแกะในชุดบทเรียนนี้ เห็นได้บนหน้านี้เลย: เลือกโมเดล (`select`) → คลาสที่ชนะตัวใหญ่กลางจอ (`result`) → แถบ `scores` ทุกคลาส + conf % ด้านข้าง
- ตรงที่ยังว่างในภาพคือช่องที่เราจะเติมวันนี้ — จังหวะ **action** เมื่อ verdict เข้าเงื่อนไข

> Emulator กับบอร์ดจริงใช้โค้ดชุดเดียวกันเป๊ะ — เขียนบน Emulator ให้เข้าใจก่อน แล้วยกไฟล์เดิมไปลงบอร์ดได้ทันที ไม่ต้องแก้อะไร

---

# กายวิภาคของแอป Edge AI ตัวเดียว

แอป Edge AI ที่โฟกัสโมเดลเดียว อ่านเป็น **3 จังหวะ** เสมอ — จำโครงนี้ไว้ แล้วทุกแอปในคอร์สจะเข้าใจง่ายขึ้น:

<div style="text-align:center;margin:6px 0">
<svg width="900" height="180" viewBox="0 0 900 180" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arAnat" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g text-anchor="middle">
    <rect x="30" y="50" width="240" height="90" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="150" y="82" font-size="16" font-weight="700" fill="#1565c0">1 · select</text>
    <text x="150" y="106" font-size="12" fill="#555">เลือกโมเดลจากทะเบียน</text>
    <text x="150" y="124" font-size="11" fill="#888">find_model → select()</text>
    <rect x="330" y="50" width="240" height="90" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="450" y="82" font-size="16" font-weight="700" fill="#e65100">2 · result</text>
    <text x="450" y="106" font-size="12" fill="#555">อ่าน verdict + วาดจอ</text>
    <text x="450" y="124" font-size="11" fill="#888">result() → verdict.text</text>
    <rect x="630" y="50" width="240" height="90" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="750" y="82" font-size="16" font-weight="700" fill="#2e7d32">3 · action</text>
    <text x="750" y="106" font-size="12" fill="#555">สั่งการเมื่อเข้าเงื่อนไข</text>
    <text x="750" y="124" font-size="11" fill="#888">fire_action() ← ของใหม่</text>
  </g>
  <line x1="270" y1="95" x2="328" y2="95" stroke="#607d8b" stroke-width="2.6" marker-end="url(#arAnat)"/>
  <line x1="570" y1="95" x2="628" y2="95" stroke="#607d8b" stroke-width="2.6" marker-end="url(#arAnat)"/>
  <text x="450" y="28" font-size="13" font-weight="700" fill="#455a64" text-anchor="middle">เลือก ──▶ อ่าน ──▶ ลงมือ</text>
  <text x="450" y="166" font-size="11" fill="#888" text-anchor="middle">บทเรียน 1.1–1.3 หยุดที่จังหวะ 2 · ชุดบทเรียนนี้เติมจังหวะ 3 เข้าไป</text>
</svg>
</div>

> จังหวะ 1–2 คือของเดิมจากบทเรียน 1.1–1.3 (เลือกโมเดล อ่านผลขึ้นจอ) จังหวะ 3 — **action** — คือหัวใจใหม่ที่ทำให้ Edge AI "ใช้งานได้จริง" ไม่ใช่แค่โชว์ตัวเลข

---

# ทะเบียนโมเดล (registry) — หน้าตาข้างใน

`edge_ai.models()` คืน **ทะเบียน** ที่เฟิร์มแวร์ถืออยู่ แต่ละแถวคือโมเดลหนึ่งตัว การแกะแอปเริ่มที่เข้าใจโครงสร้างนี้:

<div style="text-align:center;margin:6px 0">
<svg width="900" height="200" viewBox="0 0 900 200" font-family="DejaVu Sans, sans-serif">
  <rect x="20" y="14" width="860" height="172" rx="12" fill="#f7f9fb" stroke="#607d8b" stroke-width="2"/>
  <text x="40" y="40" font-size="14" font-weight="700" fill="#455a64">edge_ai.models()  →  list ของ dict</text>
  <g font-size="12">
    <rect x="40" y="54" width="820" height="30" rx="6" fill="#e3f2fd" stroke="#1565c0"/>
    <text x="52" y="74" fill="#1565c0" font-weight="700">index 0</text>
    <text x="150" y="74" fill="#333">name: "Motion Detection"</text>
    <text x="420" y="74" fill="#333">sensor: 0 (IMU)</text>
    <text x="600" y="74" fill="#333">labels: [idle, circle, shaking]</text>
    <rect x="40" y="90" width="820" height="30" rx="6" fill="#e8f5e9" stroke="#2e7d32"/>
    <text x="52" y="110" fill="#2e7d32" font-weight="700">index 1</text>
    <text x="150" y="110" fill="#333">name: "Baby Cry Detection"</text>
    <text x="420" y="110" fill="#333">sensor: 2 (MIC)</text>
    <text x="600" y="110" fill="#333">labels: [unlabelled, baby_cry]</text>
    <rect x="40" y="126" width="820" height="30" rx="6" fill="#fff3e0" stroke="#ef6c00"/>
    <text x="52" y="146" fill="#e65100" font-weight="700">index 2</text>
    <text x="150" y="146" fill="#333">name: "Push Detection"</text>
    <text x="420" y="146" fill="#333">sensor: 1 (RADAR)</text>
    <text x="600" y="146" fill="#333">labels: [unlabelled, Push]</text>
  </g>
  <text x="450" y="176" font-size="11" fill="#888" text-anchor="middle">... รวม 6 แถวบน Dev Kit · index ใช้ตอน select() · labels คือคลาสที่ result() จะตอบ</text>
</svg>
</div>

- แต่ละ dict มี 4 คีย์: `index` (ใช้ `select`), `name` (โชว์/ค้นหา), `sensor` (0=IMU,1=RADAR,2=MIC), `labels` (คลาสที่ตอบได้)
- `labels` สำคัญมากชุดบทเรียนนี้ — คลาสเป้าหมายที่เราจะดักจับต้องเป็นชื่อจากลิสต์นี้เป๊ะ

> ทะเบียนคือ "แหล่งความจริง" ของแอป — เราไม่เดาว่าโมเดลไหนคลาสอะไร เราอ่านจากที่นี่ ถ้าเฟิร์มแวร์เพิ่มโมเดล แอปเห็นเองทันที

---

# select() — เลือกจากชื่อ ไม่ใช่ index

บทเรียน 1.1–1.3 เราส่ง index ตรงๆ (`select(0)`) แต่ index อาจสลับได้ถ้าเฟิร์มแวร์เปลี่ยน แอปที่ทนทานกว่าคือ **ค้นหาโมเดลจากชื่อ** แล้วค่อยเอา index ไป select:

```python
def find_model(keyword):
    ms = edge_ai.models()
    for m in ms:
        if keyword.lower() in m['name'].lower():
            return m           # เจอชื่อที่ตรง คืน dict ทั้งก้อน
    return ms[0]               # ไม่เจอ ใช้ตัวแรกกันแอปพัง

model = find_model("Motion")   # remix: เปลี่ยน keyword = เปลี่ยนแอป
edge_ai.select(model['index']) # เอา index จาก dict ไปสั่งจริง
```

- `find_model()` ยืมมาจาก [`13_edge_ai_motion.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l06-edge-ai-app-anatomy/examples/13_edge_ai_motion.py) — คืน dict ทั้งก้อน เราจึงได้ทั้ง `index` และ `labels` มาใช้ต่อ
- เปลี่ยนแค่ `keyword` เดียว แอปก็ remix เป็นโมเดลอื่นได้ — นี่คือจุด remix แรกของชุดบทเรียน

> นิสัยเดิมจากบทเรียน 1.1–1.3 ยังอยู่: **ถามฮาร์ดแวร์ก่อน อย่าเดา** แต่รอบนี้เราถามด้วย "ชื่อ" ที่มนุษย์อ่านออก แทนตัวเลข index ที่จำยาก

---

# result() — verdict dict (ทบทวน)

`result()` คืน dict ก้อนเดิมจากบทเรียน 1.1–1.3 ชุดบทเรียนนี้เราจะใช้ 2 คีย์เป็นหลักในการตัดสิน "จะสั่งการไหม": `label` กับ `conf`

```python
r = edge_ai.result()
# r = {'label': 'shaking',     # คลาสที่ชนะ (ข้อความ)  ← ใช้เทียบเป้าหมาย
#      'top': 2,               # index ของคลาสที่ชนะ
#      'conf': 0.92,           # ความมั่นใจ 0..1        ← ใช้เทียบ CONF_FLOOR
#      'scores': [.03,.05,.92],# คะแนนทุกคลาส → ทำแถบ
#      'latency_ms': 4.1,
#      'seq': 137, 'running': True}
```

- `label` = "เจออะไร" · `conf` = "มั่นใจแค่ไหน" — สองตัวนี้รวมกันคือเงื่อนไขของ action
- `seq` เพิ่มทุกครั้งที่มีผลใหม่ — ยังใช้กันวาดจอซ้ำเหมือนบทเรียน 1.1–1.3
- `result()` เป็น **pull** ถามเมื่อไรก็ได้ในลูป คืนผลล่าสุด ไม่บล็อกรอ

> บทเรียน 1.1–1.3 เราเอา `label` ขึ้นจอเฉยๆ ชุดบทเรียนนี้เราจะ **เอา `label` + `conf` ไปตัดสินใจ** ว่าจะลงมือทำหรือไม่ — ความต่างอยู่ตรงนี้

---

# เบื้องหลัง conf — softmax เปลี่ยนคะแนนดิบเป็นความน่าจะเป็น

`scores` กับ `conf` ที่ `result()` คืนมาไม่ได้โผล่มาลอยๆ — มันมาจากสูตรชื่อ **softmax** โมเดลปล่อย "คะแนนดิบ" (logits) $z_i$ ของแต่ละคลาสออกมาก่อน แล้ว softmax บีบให้เป็นความน่าจะเป็นที่รวมกันได้ 1:

$$\text{softmax}(z)_i = \frac{e^{z_i}}{\displaystyle\sum_{j=1}^{K} e^{z_j}}$$

อ่านทีละตัวแบบไม่ต้องกลัวสูตร:

- $z_i$ = คะแนนดิบของคลาสที่ $i$ (logit) ที่โมเดลปล่อยออกมา ค่าติดลบก็ได้
- $K$ = จำนวนคลาสทั้งหมด (เช่น Motion มี 3 คลาส: idle, circle, shaking)
- $e^{z_i}$ = ยกกำลัง exponential ทำให้ค่าบวกเสมอ และดันคะแนนที่สูงให้เด่นขึ้น
- ตัวส่วน $\sum_j e^{z_j}$ = ผลรวมของทุกคลาส ใช้ "หาร normalize" ให้ทุกคลาสรวมกันได้พอดี 1

ผลลัพธ์ $\text{softmax}(z)_i$ คือ **ความน่าจะเป็นของคลาส $i$** — นี่แหละคือค่าที่ไปโผล่ในทุกช่องของ `r['scores']` (แต่ละแถบที่เห็นบนจอ)

> ทำไมไม่ใช้คะแนนดิบตรงๆ? เพราะเราอยากได้เลข 0..1 ที่ตีความเป็น "มั่นใจกี่เปอร์เซ็นต์" ได้จริง — และเส้น `CONF_FLOOR = 0.50` จะมีความหมายก็ต่อเมื่อคะแนนถูก normalize แล้วเท่านั้น

---

# argmax หาป้าย · max หา conf — ที่มาของ label กับ conf

จาก `scores` ที่ softmax ให้มา เฟิร์มแวร์คำนวณสองค่าที่เราเอาไปตัดสินใจ ด้วยตัวดำเนินการคู่กัน:

$$\hat{y} = \arg\max_i \text{softmax}(z)_i \qquad\qquad \text{conf} = \max_i \text{softmax}(z)_i$$

- $\arg\max$ = **ตำแหน่ง** (index) ของคลาสที่คะแนนสูงสุด → กลายเป็น `r['top']` แล้วแปลงเป็นชื่อ `r['label']`
- $\max$ = **ค่า** คะแนนสูงสุดเอง (ไม่ใช่ตำแหน่ง) → กลายเป็น `r['conf']` ความมั่นใจ 0..1

ลองแทนตัวเลขจริงของโมเดล Motion 3 คลาส:

$$\text{scores} = [\,0.03,\ 0.05,\ 0.92\,] \;\Longrightarrow\; \hat{y}=2\ (\text{shaking}),\quad \text{conf}=0.92$$

- คลาส index 2 คะแนนสูงสุด → `label = "shaking"`, `top = 2`
- ค่าสูงสุด 0.92 → `conf = 0.92` = มั่นใจ 92%
- $0.92 \geq \text{CONF\_FLOOR}\ (0.50)$ → เงื่อนไข `hit` เป็น `True` → **สั่งการ**

> นี่คือสะพานเชื่อมสูตรกับโค้ดของเราตรงๆ: `r['label']` มาจาก argmax, `r['conf']` มาจาก max ของ scores ก้อนเดียวกัน — สองบรรทัดเงื่อนไข `hit` ในชุดบทเรียนนี้ (`label == TARGET` และ `conf >= CONF_FLOOR`) ก็คือ argmax คู่กับ max นั่นเอง

---

# เส้นทาง verdict → screen

ก่อนต่อ action มาปิดเส้นทางเดิมให้ขาดก่อน: verdict หนึ่งก้อนกลายเป็นภาพบนจอได้ยังไง นี่คือ "จังหวะ 2" แบบละเอียด

<div style="text-align:center;margin:6px 0">
<svg width="900" height="190" viewBox="0 0 900 190" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arV2S" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="60" width="180" height="70" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="110" y="88" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">result()</text>
  <text x="110" y="110" font-size="11" fill="#666" text-anchor="middle">dict หรือ None</text>
  <rect x="250" y="60" width="180" height="70" rx="10" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
  <text x="340" y="84" font-size="12" font-weight="700" fill="#455a64" text-anchor="middle">seq เปลี่ยน?</text>
  <text x="340" y="106" font-size="11" fill="#666" text-anchor="middle">มีผลใหม่จริงไหม</text>
  <rect x="480" y="24" width="180" height="60" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="570" y="50" font-size="12" font-weight="700" fill="#2e7d32" text-anchor="middle">verdict.text</text>
  <text x="570" y="70" font-size="11" fill="#666" text-anchor="middle">คลาสที่ชนะ (Seg7)</text>
  <rect x="480" y="104" width="180" height="60" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="570" y="130" font-size="12" font-weight="700" fill="#1565c0" text-anchor="middle">แถบ scores</text>
  <text x="570" y="150" font-size="11" fill="#666" text-anchor="middle">br.value ทุกคลาส</text>
  <rect x="710" y="60" width="170" height="70" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="795" y="88" font-size="12" font-weight="700" fill="#e65100" text-anchor="middle">conf %</text>
  <text x="795" y="110" font-size="11" fill="#666" text-anchor="middle">ความมั่นใจ</text>
  <line x1="200" y1="95" x2="248" y2="95" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arV2S)"/>
  <line x1="430" y1="80" x2="478" y2="60" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arV2S)"/>
  <line x1="430" y1="110" x2="478" y2="128" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arV2S)"/>
  <line x1="660" y1="70" x2="708" y2="88" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arV2S)"/>
</svg>
</div>

- เช็ก `seq` ก่อน → วาดเฉพาะตอนมีผลใหม่ (ไม่รัดจอ) · แล้วกระจายไป `verdict.text` + แถบ `scores` + `conf`
- `scores` คือคะแนน **ทุกคลาส** เอาไปทำแถบ คลาสที่ `i == top` ระบายเขียว ผู้ใช้เห็นทั้งคำตอบและความสูสี

> นี่คือ "จังหวะ 2" ที่คุณเติมมาแล้วในบทเรียน 1.1–1.3 — ชุดบทเรียนนี้เราต่อ "จังหวะ 3" (action) จากจุดเดียวกันนี้ หลังวาดจอเสร็จ

---

# ของใหม่ชุดบทเรียนนี้ — verdict → ACTION

จนถึงบทเรียน 1.1–1.3 เราหยุดที่ "เอาคำตอบขึ้นจอ" แต่แอป Edge AI จริงต้อง **ลงมือทำอะไรต่อ** เมื่อคำตอบเข้าเงื่อนไข นี่คือก้าวจาก inference ไปสู่ application

<div style="text-align:center;margin:8px 0">
<svg width="820" height="130" viewBox="0 0 820 130" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arV2A" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="40" width="200" height="56" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="120" y="64" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">verdict</text>
  <text x="120" y="84" font-size="11" fill="#666" text-anchor="middle">"shaking" 92%</text>
  <polygon points="300,68 360,40 420,68 360,96" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
  <text x="360" y="64" font-size="11" font-weight="700" fill="#455a64" text-anchor="middle">เข้าเงื่อนไข?</text>
  <text x="360" y="80" font-size="10" fill="#666" text-anchor="middle">label + conf</text>
  <rect x="500" y="40" width="200" height="56" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="600" y="64" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">ACTION</text>
  <text x="600" y="84" font-size="11" fill="#666" text-anchor="middle">บี๊บ · แบนเนอร์ · แจ้งเตือน</text>
  <line x1="220" y1="68" x2="298" y2="68" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arV2A)"/>
  <line x1="420" y1="68" x2="498" y2="68" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arV2A)"/>
  <text x="460" y="60" font-size="11" fill="#2e7d32" text-anchor="middle">yes</text>
</svg>
</div>

- ในบทเรียนนี้ action = **บี๊บ + แบนเนอร์บนจอ** (ทำได้ทั้ง Emulator และบอร์ด)
- ในงานจริง action เดียวกันนี้อาจเป็น: เปิดไฟ · ส่ง MQTT แจ้งเตือน · บันทึกเหตุการณ์ลงไฟล์ · สั่งมอเตอร์

> "โมเดลรู้ว่าเจออะไร" เป็นแค่ครึ่งทาง — คุณค่าจริงเกิดตอน **การกระทำ** ที่ตามมา นี่คือสิ่งที่ โมดูล 6 (Apps) ทั้งบล็อกจะขยายให้ลึก

---

# เงื่อนไขของ action — label + conf

action ไม่ควรยิงทุกครั้งที่โมเดลตอบ — ต้องยิงเฉพาะเมื่อ **ใช่คลาสที่เราสนใจ** และ **มั่นใจพอ** สองเงื่อนไขนี้คู่กันเสมอ:

```python
hit = (r['label'] == TARGET_CLASS            # 1) ใช่คลาสเป้าหมายไหม
       and r['conf'] >= edge_ai.CONF_FLOOR)  # 2) มั่นใจถึงเกณฑ์ไหม (>= 0.50)

if hit and not fired:
    fire_action(r['conf'])                   # ลงมือ
    fired = True
```

- เช็ก `label` อย่างเดียวไม่พอ — ถ้าโมเดลตอบ "shaking" แต่ `conf` แค่ 30% แปลว่ามัน "เดา" เราไม่ควรลงมือ
- `CONF_FLOOR = 0.50` คือเส้นที่เฟิร์มแวร์แนะนำ (จากบทเรียน 1.1–1.3) — เป็นตัวกัน false positive

> นี่คือบทเรียน Edge AI สำคัญ: **action ต้องตั้งอยู่บนความมั่นใจ ไม่ใช่แค่ป้ายคลาส** เส้น `CONF_FLOOR` คือปุ่มที่คุณจะปรับจริงจังในชุดบทเรียน Apps (บทเรียน 6.3–6.4)

---

# edge-trigger — ยิงครั้งเดียวต่อการเจอ

ปัญหา: ถ้าคุณเขย่าค้าง 3 วินาที โมเดลตอบ "shaking" ทุกเฟรม — ถ้ายิง action ทุกเฟรม เสียงจะบี๊บรัวจนน่ารำคาญ ทางแก้คือ **จำว่ายิงไปแล้ว**

```python
if hit and not fired:      # เพิ่งเข้าคลาสเป้าหมาย → ยิงครั้งเดียว
    fire_action(r['conf'])
    fired = True
elif not hit:              # ออกจากคลาสเป้าหมายแล้ว → รีเซ็ต
    fired = False
```

- `fired` เป็นธง: ตั้ง `True` ตอนยิง เคลียร์ `False` ตอนออกจากคลาส — action จึงยิง "ตอนขอบขาขึ้น" ครั้งเดียว
- นี่เรียกว่า **edge-triggered** (ยิงตอนเปลี่ยนสถานะ) ตรงข้ามกับ **level-triggered** (ยิงตลอดที่ยังเจอ)

> pattern เดียวกับปุ่มกดในงาน embedded: เรากด **หนึ่งครั้ง** ได้ event หนึ่งครั้ง ไม่ใช่ event รัวตราบที่ยังกดค้าง — action ที่ดีต้องคุมจังหวะการยิงเสมอ

---

# fire_action() — action จริงบนบอร์ด

`fire_action()` คือที่ที่ verdict กลายเป็นการกระทำจริง ในบทเรียนนี้เราให้มันบี๊บ + ขึ้นแบนเนอร์ + จดคอนโซล:

```python
def fire_action(conf_val):
    banner.text("! เจอ %s !" % TARGET_CLASS)
    banner.color(GREEN)
    if hasattr(ui, "tone"):
        ui.tone(72, ui.WAVE_SINE, 120, 150)   # โน้ต MIDI 72, sine, ดัง 120, 150 ms
    lcd.console('<span class=ok> ACTION: เจอ %s (conf %.0f%%)</span>'
                % (TARGET_CLASS, conf_val * 100))
```

- `ui.tone(note, wave, vol, ms)` เล่นเสียงผ่าน SFX mixer ฝั่ง CM55 — `note` เป็น MIDI (60 = โดกลาง)
- ห่อด้วย `hasattr(ui, "tone")` เผื่อพื้นผิวที่ไม่มีลำโพง — แอปไม่พังถ้าเล่นเสียงไม่ได้
- แยก `fire_action()` เป็นฟังก์ชัน = remix ง่าย: อยากเปลี่ยน action แก้ที่เดียว

> เก็บ "การตัดสินใจ" (เงื่อนไข hit) แยกจาก "การลงมือ" (fire_action) — โครงนี้ทำให้เปลี่ยน action โดยไม่แตะ logic ตรวจจับได้ นี่คือนิสัยออกแบบที่ดี

---

# on_result() — วิธี event-driven

การ poll เอง (`result()` ในลูป + เช็ก `seq`) ใช้ได้ดี แต่ `edge_ai` มีทางที่สะอาดกว่า: ให้เฟิร์มแวร์ **เรียกฟังก์ชันของเราให้** เมื่อมีคำตัดสิน (ทันทีที่คลาสเปลี่ยน และทวนคลาสเดิมราววินาทีละครั้ง)

<div style="text-align:center;margin:6px 0">
<svg width="900" height="180" viewBox="0 0 900 180" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arCb" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="16" width="410" height="150" rx="12" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
  <text x="225" y="40" font-size="13" font-weight="700" fill="#455a64" text-anchor="middle">poll เอง (บทเรียน 1.1–1.3 + ฝึก)</text>
  <text x="225" y="66" font-size="11" fill="#555" text-anchor="middle">while: r = result()</text>
  <text x="225" y="86" font-size="11" fill="#555" text-anchor="middle">ถ้า seq เปลี่ยน → วาด/สั่งการ</text>
  <text x="225" y="112" font-size="11" fill="#888" text-anchor="middle">เราถามเอง เช็ก seq เอง</text>
  <text x="225" y="132" font-size="11" fill="#888" text-anchor="middle">คุมจังหวะได้ตรงไปตรงมา</text>
  <rect x="470" y="16" width="410" height="150" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="675" y="40" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">on_result(cb) (ฉบับเต็ม)</text>
  <text x="675" y="66" font-size="11" fill="#555" text-anchor="middle">on_result(on_change)</text>
  <text x="675" y="86" font-size="11" fill="#555" text-anchor="middle">เฟิร์มแวร์เรียก cb ให้เมื่อมีคำตัดสิน</text>
  <text x="675" y="112" font-size="11" fill="#888" text-anchor="middle">ไม่ต้องเช็ก seq เอง</text>
  <text x="675" y="132" font-size="11" fill="#888" text-anchor="middle">ลูปเหลือแค่รับปุ่ม</text>
</svg>
</div>

```python
def on_change(r):          # เฟิร์มแวร์เรียกให้เมื่อมีคำตัดสิน (scheduler context — ปลอดภัยกับ UI)
    verdict.text(r['label'] or '-')
    if r['label'] == TARGET_CLASS and r['conf'] >= edge_ai.CONF_FLOOR:
        fire_action(r['conf'])
edge_ai.on_result(on_change)   # ลงทะเบียนครั้งเดียว
```

> `on_result` ยิง cb ให้เราทันทีที่คลาสเปลี่ยน (และทวนคลาสเดิมราววินาทีละครั้ง) เราจึงไม่ต้องเช็ก `seq` เอง แต่ยังต้องมีธง `fired` กันยิง action ซ้ำ — [`s03_anatomy_edgeai_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l07-verdict-action-lab/examples/s03_anatomy_edgeai_full.py) ใช้วิธีนี้ ทำให้ลูปหลักเหลือแค่รับปุ่ม back

---

# poll กับ on_result — เลือกยังไง

สองวิธีให้ผลเดียวกัน ต่างที่ "ใครถาม" — เข้าใจข้อแลกเปลี่ยนแล้วเลือกใช้ให้เหมาะกับงาน:

| ประเด็น | poll เอง (`result()`) | `on_result(cb)` |
|---|---|---|
| ใครขับ | โค้ดเราถามเองในลูป | เฟิร์มแวร์เรียก cb ให้ |
| เช็ก `seq` | ต้องเช็กเอง | ไม่ต้อง (ยิงตอนคลาสเปลี่ยน และทวนคลาสเดิมราววินาทีละครั้ง) |
| คุมจังหวะ | ตรงไปตรงมา เห็นทั้งลูป | logic กระจายไปอยู่ใน cb |
| เหมาะกับ | เริ่มเรียน · อยากเห็นทุกจังหวะ | แอปที่ action ต้องไวและสะอาด |

- ในไฟล์ฝึก (`practice/`) เราใช้ **poll** เพราะเห็นทั้ง 3 จังหวะในลูปเดียว เข้าใจง่าย
- บน BENTO Emulator callback ของ `on_result` จะทำงานก็ต่อเมื่อโปรแกรมเรียก `edge_ai.result()` หรือ `edge_ai.active()` ถ้าลูปมีแค่ `ui.poll()` บน Emulator จะไม่เห็นผลเลย (บนบอร์ดไม่มีข้อจำกัดนี้)
- ในฉบับเต็ม (`examples/`) เราใช้ **on_result** เพราะแอปโตขึ้น — ย้าย logic ไปที่ cb ทำให้ลูปสะอาด

> ทั้งคู่ถูกต้อง ไม่มีผิด — เริ่มจาก poll ให้เข้าใจกลไกก่อน แล้วค่อยยกไป on_result เมื่อแอปต้องการความสะอาด (ลองเป็นโจทย์ต่อยอดดูได้)
