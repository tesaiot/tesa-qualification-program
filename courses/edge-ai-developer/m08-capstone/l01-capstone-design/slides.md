---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 8.1 — ออกแบบ capstone: Guardian สามเสาในไฟล์เดียว"
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

# บทเรียน 8.1 — ออกแบบ capstone: Guardian สามเสาในไฟล์เดียว
## ออกแบบ → สร้าง → ส่งมอบ แอป Edge AI ครบสามเสา

**โมดูล 8 — Capstone: แอป Edge AI ของเราเอง**

**บล็อก Researcher & Capstone — ชุดบทเรียนปิดคอร์ส**

> คาถาประจำบทเรียน: **"งานจบไม่ใช่ 'อีกหนึ่งเดโม' — มันคือการร้อยทุกเสาที่เราเดินมาให้กลายเป็นผลิตภัณฑ์ Edge AI ที่ส่งมอบได้จริง"**

MicroPython บนบอร์ด BENTO (PSoC Edge · Cortex-M55 + Ethos-U55 NPU)

---

# เปิดบทเรียนด้วยของจริงก่อน

ปิดคอร์สแบบเดิมที่เราเปิดคอร์ส — **กลับด้าน** รันของที่ทำงานได้จริงก่อน (Guardian ตัวเต็ม) แล้วค่อยแกะว่าทำไมมันถึงร้อยครบทั้งสามเสา

<div style="text-align:center;margin:10px 0">
<svg width="820" height="150" viewBox="0 0 820 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arOpen" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="40" width="180" height="70" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="104" y="72" font-size="15" font-weight="700" fill="#2e7d32" text-anchor="middle">รัน Guardian ตัวเต็ม</text>
  <text x="104" y="94" font-size="12" fill="#555" text-anchor="middle">examples/</text>
  <rect x="234" y="40" width="180" height="70" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="324" y="72" font-size="15" font-weight="700" fill="#1565c0" text-anchor="middle">แกะสามเสา</text>
  <text x="324" y="94" font-size="12" fill="#555" text-anchor="middle">DAQ·Processing·Apps</text>
  <rect x="454" y="40" width="180" height="70" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="544" y="72" font-size="15" font-weight="700" fill="#e65100" text-anchor="middle">เติม/ออกแบบเอง</text>
  <text x="544" y="94" font-size="12" fill="#555" text-anchor="middle">5 บรรทัดสันหลัง</text>
  <rect x="674" y="40" width="132" height="70" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="740" y="72" font-size="15" font-weight="700" fill="#6a1b9a" text-anchor="middle">ส่งมอบ + เดโม</text>
  <text x="740" y="94" font-size="12" fill="#555" text-anchor="middle">MVP ของบทเรียน 8.1–8.2</text>
  <line x1="194" y1="75" x2="230" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="414" y1="75" x2="450" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="634" y1="75" x2="670" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
</svg>
</div>

วิธีเดิมที่ใช้ทั้งคอร์ส — **PRIMM** (Predict–Run–Investigate–Modify–Make) วันนี้หนักที่ **Make**: คุณจะออกแบบผลิตภัณฑ์ของทีมเอง ไม่ใช่แค่เติมช่องว่างแล้วจบ

> ชุดบทเรียนสุดท้ายไม่ใช่การสอนของใหม่กองโต แต่คือ "พิสูจน์ว่าเราต่อของเป็น" — หยิบชิ้นส่วนจาก 19 ชุดบทเรียนมาประกอบเป็นชิ้นเดียวที่ทำงานได้และเล่าให้คนอื่นเข้าใจ

---

# เป้าหมายของชุดบทเรียนนี้

จบชุดบทเรียนนี้เราจะเดินครบ แล้วปิดท้ายด้วยการส่งมอบผลิตภัณฑ์ Edge AI ของทีม:

1. **Capstone คืออะไร** — ต่างจาก "เดโมชิ้นเดียว" ตรงไหน และทำไมต้องข้าม ≥3 เสา
2. **สามเสาใน Guardian หนึ่งไฟล์** — DAQ (เซนเซอร์ดิบ) · Processing (กรอง+หน่วง) · Apps (verdict→action)
3. **ชั้นตัดสินใจ** — `CONF_FLOOR` + debounce + edge-trigger กัน false positive
4. **การตัดสินใจเชิงวิศวกรรม** — latency vs false positive vs พลังงาน: เลือกอะไร แลกกับอะไร
5. ลงมือ: เติม **5 บรรทัดสันหลัง** ของ [`s20_capstone.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m08-capstone/l02-capstone-build-lab/practice/s20_capstone.py) แล้วออกแบบ Guardian เวอร์ชันของทีม

ปลายทางของวันนี้: กด Load เฝ้าโมเดล ทำเหตุการณ์เป้าหมาย แล้ว Guardian **สั่งการเอง** (เสียง + แบนเนอร์ + นับครั้ง) โดยไม่เตือนพร่ำจากพีคหลอก

> วันนี้เน้น "ประกอบเป็น + อธิบายการออกแบบได้" ไม่ใช่เขียนของใหม่ — ทุกคำสั่งที่ใช้ เราเจอมาหมดแล้วในชุดบทเรียนก่อน ๆ

---

# Capstone คืออะไร — ไม่ใช่ "อีกหนึ่งเดโม"

ตลอดคอร์สเราสร้าง "ชิ้นส่วน" ทีละชิ้น: logger, ฟิลเตอร์, FFT, โมเดลที่ฝึกเอง, action pipeline วันนี้เอามาต่อเป็น **ระบบเดียว**

- **เดโม** ตอบคำถาม "ทำได้ไหม" — โชว์ฟีเจอร์เดียว รันในสภาพอุดมคติ
- **Capstone / ผลิตภัณฑ์** ตอบ "ใช้ได้จริงไหม" — ต้องรับมือ noise, false positive, การเก็บกวาด, และอธิบายได้ว่าทำไมออกแบบแบบนี้
- ข้อบังคับของ capstone: ต้องข้าม **≥3 เสา** ของวงจรชีวิตข้อมูล ไม่ใช่แตะแค่ขั้นเรียกโมเดล

> เส้นแบ่งง่ายๆ: เดโมพังเงียบๆ ได้ ผลิตภัณฑ์พังไม่ได้ — มันต้อง "รู้ตัวว่าไม่ชัวร์" และ "ไม่เตือนมั่ว" นี่คือสิ่งที่ capstone ให้คุณพิสูจน์

---

# มองย้อนทั้งคอร์ส — 5 เสาที่เราเดินมา

Guardian ที่จะสร้างวันนี้ ไม่ได้ใช้ของใหม่เลย มันหยิบจากเสาที่เราปูมาทั้งคอร์ส:

<div style="text-align:center;margin:6px 0">
<svg width="920" height="200" viewBox="0 0 920 200" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arLC" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g text-anchor="middle">
    <rect x="10" y="60" width="160" height="72" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="90" y="86" font-size="14" font-weight="700" fill="#1565c0">1 · DAQ</text>
    <text x="90" y="106" font-size="11" fill="#555">อ่านเซนเซอร์ดิบ</text>
    <text x="90" y="122" font-size="10" fill="#2e7d32">Guardian ใช้</text>
    <rect x="196" y="60" width="160" height="72" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="276" y="86" font-size="14" font-weight="700" fill="#2e7d32">2 · Processing</text>
    <text x="276" y="106" font-size="11" fill="#555">กรอง+derived</text>
    <text x="276" y="122" font-size="10" fill="#2e7d32">Guardian ใช้</text>
    <rect x="382" y="60" width="160" height="72" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="462" y="86" font-size="14" font-weight="700" fill="#e65100">3 · Analysis</text>
    <text x="462" y="106" font-size="11" fill="#555">DSP·FFT·feature</text>
    <text x="462" y="122" font-size="10" fill="#888">ต่อยอดได้</text>
    <rect x="568" y="60" width="160" height="72" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
    <text x="648" y="86" font-size="14" font-weight="700" fill="#6a1b9a">4 · Training</text>
    <text x="648" y="106" font-size="11" fill="#555">ฝึกโมเดลเอง</text>
    <text x="648" y="122" font-size="10" fill="#888">เสียบโมเดลได้</text>
    <rect x="754" y="60" width="160" height="72" rx="12" fill="#e0f7fa" stroke="#00838f" stroke-width="2"/>
    <text x="834" y="86" font-size="14" font-weight="700" fill="#00838f">5 · Apps</text>
    <text x="834" y="106" font-size="11" fill="#555">verdict→action</text>
    <text x="834" y="122" font-size="10" fill="#2e7d32">Guardian ใช้</text>
  </g>
  <line x1="170" y1="96" x2="194" y2="96" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <line x1="356" y1="96" x2="380" y2="96" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <line x1="542" y1="96" x2="566" y2="96" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <line x1="728" y1="96" x2="752" y2="96" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <text x="462" y="24" font-size="13" font-weight="700" fill="#455a64" text-anchor="middle">Capstone = ร้อยหลายเสาเข้าเป็นผลิตภัณฑ์เดียว</text>
  <text x="462" y="176" font-size="12" fill="#888" text-anchor="middle">Guardian แตะ DAQ + Processing + Apps ตรงๆ · Analysis/Training = ทางต่อยอด</text>
</svg>
</div>

> เกณฑ์ MVP ของบทเรียน 8.1–8.2 คือ "ข้าม ≥3 เสา" — Guardian ทำครบพอดี และเปิดช่องให้ทีมที่อยากต่อยอดเสียบโมเดลที่ฝึกเอง (เสา Training) หรือ FFT feature (เสา Analysis) เพิ่ม

---

# ชุดบทเรียนนี้อยู่ตรงไหนของคอร์ส

เราปิดวงพอดี — บทเรียน 1.1–1.3 เริ่มที่ **ขั้น Apps** (รันโมเดลสำเร็จรูป) วันนี้กลับมาที่ Apps อีกครั้ง แต่คราวนี้เราสร้างได้ทั้งวงจร

<div style="text-align:center;margin:8px 0">
<svg width="760" height="96" viewBox="0 0 760 96" font-family="DejaVu Sans, sans-serif">
  <line x1="40" y1="48" x2="720" y2="48" stroke="#cfd8dc" stroke-width="3"/>
  <circle cx="120" cy="48" r="9" fill="#00838f"/>
  <text x="120" y="30" font-size="12" font-weight="700" fill="#00838f" text-anchor="middle">บทเรียน 1.1–1.3</text>
  <text x="120" y="74" font-size="11" fill="#777" text-anchor="middle">รันโมเดลสำเร็จ (ขั้น 5)</text>
  <circle cx="410" cy="48" r="9" fill="#6a1b9a"/>
  <text x="410" y="30" font-size="12" font-weight="700" fill="#6a1b9a" text-anchor="middle">บทเรียน 2.1–7.4</text>
  <text x="410" y="74" font-size="11" fill="#777" text-anchor="middle">สร้างเองครบทั้ง 5 เสา</text>
  <circle cx="620" cy="48" r="9" fill="#2e7d32"/>
  <text x="620" y="30" font-size="12" font-weight="700" fill="#2e7d32" text-anchor="middle">บทเรียน 8.1–8.2 (วันนี้)</text>
  <text x="620" y="74" font-size="11" fill="#777" text-anchor="middle">ร้อยทุกเสาเป็นผลิตภัณฑ์</text>
  <path d="M600,44 C520,20 260,20 138,42" fill="none" stroke="#9e9e9e" stroke-width="2" stroke-dasharray="6 5"/>
  <text x="370" y="18" font-size="11" fill="#9e9e9e" text-anchor="middle">ปิดวง — กลับมาที่ Apps แต่ตอนนี้เข้าใจทั้งกระบวนการ</text>
</svg>
</div>

> ความรู้สึกที่อยากให้คุณมีวันนี้: "เมนู 6 โมเดลในชุดบทเรียนแรกเคยเป็นกล่องดำ ตอนนี้เราเปิดกล่องได้ทุกชั้น และประกอบกล่องของเราเองได้แล้ว"

---

# สาธิต — Guardian ทำอะไรบนจอ

ก่อนแกะโค้ด ดูปลายทางก่อน นี่คือสิ่งที่ [`s20_capstone_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m08-capstone/l02-capstone-build-lab/examples/s20_capstone_full.py) โชว์เมื่อรัน:

- เลือกโมเดลใน dropdown (เช่น Motion) กด **Load** → สถานะ RUNNING
- การ์ดกลางโชว์ **คลาสที่ชนะ** + **conf ที่กรองแล้ว** + **latency** + **motion** (บริบทจากเสา DAQ)
- ทำเหตุการณ์เป้าหมาย (เขย่า/ร้อง/ไอ) ให้ตรงคลาสสุดท้ายของโมเดล **ติดกันหลายครั้ง**
- พอครบเกณฑ์ debounce → แบนเนอร์เด้ง `! ALERT !` + เสียงบี๊บ + ตัวนับ `alert: N ครั้ง` เพิ่มขึ้น
- ทำท่าก้ำกึ่ง/พีคแวบเดียว → Guardian **ไม่เตือน** เพราะยังไม่ครบเกณฑ์

> จุดที่อยากให้จับ: มันไม่ได้ "เจอปุ๊บเตือนปั๊บ" — มันรอให้มั่นใจพอ **แล้วค่อยลงมือ** นี่คือความต่างระหว่างเดโมกับผลิตภัณฑ์

---

# สามเสาใน Guardian หนึ่งไฟล์

หัวใจของ capstone: สามเสาที่เคยอยู่คนละบทเรียน วันนี้ไหลต่อกันในลูปเดียว

<div style="text-align:center;margin:6px 0">
<svg width="900" height="210" viewBox="0 0 900 210" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="ar3P" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="16" y="50" width="250" height="120" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="141" y="78" font-size="15" font-weight="700" fill="#1565c0" text-anchor="middle">เสา DAQ</text>
  <text x="141" y="102" font-size="12" fill="#555" text-anchor="middle">sensors.bmi270</text>
  <text x="141" y="122" font-size="11" fill="#888" text-anchor="middle">.acceleration()</text>
  <text x="141" y="144" font-size="11" fill="#888" text-anchor="middle">= บริบท motion</text>
  <rect x="326" y="50" width="250" height="120" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="451" y="78" font-size="15" font-weight="700" fill="#2e7d32" text-anchor="middle">เสา Processing</text>
  <text x="451" y="102" font-size="12" fill="#555" text-anchor="middle">dsp.EMA(conf)</text>
  <text x="451" y="122" font-size="11" fill="#888" text-anchor="middle">+ debounce streak</text>
  <text x="451" y="144" font-size="11" fill="#888" text-anchor="middle">= ความมั่นใจที่นิ่ง</text>
  <rect x="636" y="50" width="250" height="120" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="761" y="78" font-size="15" font-weight="700" fill="#6a1b9a" text-anchor="middle">เสา Apps</text>
  <text x="761" y="102" font-size="12" fill="#555" text-anchor="middle">edge_ai result()</text>
  <text x="761" y="122" font-size="11" fill="#888" text-anchor="middle">→ decision → action</text>
  <text x="761" y="144" font-size="11" fill="#888" text-anchor="middle">= เสียง+แบนเนอร์</text>
  <line x1="266" y1="110" x2="324" y2="110" stroke="#607d8b" stroke-width="2.4" marker-end="url(#ar3P)"/>
  <line x1="576" y1="110" x2="634" y2="110" stroke="#607d8b" stroke-width="2.4" marker-end="url(#ar3P)"/>
  <text x="450" y="30" font-size="13" font-weight="700" fill="#455a64" text-anchor="middle">verdict + บริบท → กรองให้นิ่ง → สั่งการเมื่อมั่นใจพอ</text>
  <text x="450" y="196" font-size="11" fill="#888" text-anchor="middle">ทั้งสามเสาอยู่ในลูป while เดียว — นี่คือ "ผลิตภัณฑ์" ไม่ใช่ 3 สคริปต์แยกกัน</text>
</svg>
</div>

> สังเกตว่า conf จากโมเดล (Apps) ไม่ได้ถูกใช้ตรงๆ มันวิ่งผ่านเสา Processing ก่อน (กรอง+หน่วง) แล้วค่อยกลายเป็น action — เสาไม่ได้เรียงกันเฉยๆ มัน "ป้อนกันจริง"

---

# เสา Apps — verdict → decision → action

หัวใจเดิมจากบทเรียน 1.1–1.3 และ 1.6–1.7 กลับมาครบ: อ่านทะเบียน เลือกโมเดล อ่านผล หยุด แล้วเพิ่ม "ตัดสินใจ + สั่งการ"

| คำสั่ง | ทำอะไรใน Guardian |
|---|---|
| `edge_ai.models()` | อ่านทะเบียนโมเดล → ทำ dropdown + หา `alert_idx` |
| `edge_ai.select(n)` | กด Load → สั่ง CM55 รันโมเดล (ห่อ `try/except OSError`) |
| `edge_ai.result()` | อ่าน verdict ล่าสุด `{label, top, conf, scores, seq, latency_ms}` |
| `edge_ai.CONF_FLOOR` | เส้นความมั่นใจ 0.50 — ต่ำกว่านี้ "ยังไม่ชัวร์" |
| `edge_ai.stop()` | ปุ่ม Stop + `finally` — คืนเครื่องยนต์สู่ idle |

- ทั้งหมดนี้คุณใช้เป็นตั้งแต่บทเรียน 1.1–1.3 แล้ว — capstone แค่ให้ "เอามาต่อกับเสาอื่น"
- ของใหม่คือชั้น **decision**: `top == alert_idx` และ `conf` ถึงเกณฑ์ ค่อยนับเป็น "เจอ"

> เรายึด 4 คำสั่งเดิม (`models`/`select`/`result`/`stop`) เป็นแกน แล้วห่อชั้นตัดสินใจรอบนอก — โครงนี้คือ pattern ของแอป Edge AI ทุกตัวในโลกจริง

---

# เสา Processing — ทำไมต้องกรอง conf

โมเดลตอบความน่าจะเป็น มันกระโดดขึ้นลงได้ทุกเฟรม ถ้าเอา `conf` ดิบไปตัดสินใจตรงๆ Guardian จะ "เตือนแล้วเงียบ เตือนแล้วเงียบ" น่ารำคาญและไม่น่าเชื่อถือ

```python
conf_ema = dsp.EMA(alpha=EMA_ALPHA)   # สร้างครั้งเดียวก่อนลูป
...
conf_s = conf_ema.update(r['conf'])   # กรองก่อนเทียบเกณฑ์
sure = conf_s >= edge_ai.CONF_FLOOR
```

- **EMA** (Exponential Moving Average) จากบทเรียน Analysis (บทเรียน 4.1–4.2) — ถัวเฉลี่ยถ่วงน้ำหนักอดีต ราคาถูกสุด เขียนบรรทัดเดียว
- `alpha` มาก = ตอบไวแต่ยังแกว่ง · `alpha` น้อย = นิ่งแต่ตอบช้า — นี่คือปุ่มออกแบบที่ทีมต้องเลือก
- กรอง conf แล้วยังไม่พอ — เราซ้อน **debounce** อีกชั้น (ถัดไป)

> นี่คือเหตุผลที่โมดูล 4 (Analysis) มีอยู่จริง ไม่ใช่ทฤษฎีลอยๆ: ฟิลเตอร์ตัวเดียวกับที่ทำสัญญาณเซนเซอร์ให้สะอาด วันนี้เอามาทำ "ความมั่นใจ" ให้สะอาดด้วย

---

# คณิตเบื้องหลังเสา Processing — สูตร EMA

ตัวกรอง `dsp.EMA` ที่เราเติมในช่อง 4 มีสูตรบรรทัดเดียว — ผสมค่าปัจจุบันกับ "ความจำ" ที่กรองไว้แล้ว:

$$s_n = \alpha \, c_n + (1-\alpha)\, s_{n-1}$$

อ่านทีละตัวแบบง่ายๆ:

- $c_n$ — ค่า conf **ดิบ** ที่โมเดลตอบในเฟรมนี้ (คือ `r['conf']`)
- $s_n$ — ค่า conf **ที่กรองแล้ว** ในเฟรมนี้ (คือ `conf_s`) เอาไปเทียบ `CONF_FLOOR`
- $s_{n-1}$ — ค่าที่กรองไว้เมื่อเฟรมก่อน (ตัวกรอง "จำ" ให้เราเอง)
- $\alpha$ — น้ำหนักของค่าปัจจุบัน คือ `EMA_ALPHA` โดย $0 < \alpha \le 1$ ($\alpha$ มาก = เชื่อค่าใหม่มาก, $\alpha$ น้อย = เชื่ออดีตมาก)

**ทำไมสำคัญกับชุดบทเรียนนี้:** conf ดิบกระโดดขึ้นลงทุกเฟรม ถ้าเอาไปตัดสินใจตรงๆ Guardian จะเตือนๆ เงียบๆ น่ารำคาญ สูตรนี้ถ่วงอดีตเข้ามาช่วย ทำให้ conf "นิ่ง" ก่อนผ่านด่านตัดสินใจ และเป็นเหตุผลที่ต้องสร้าง `conf_ema` **นอกลูป** — เพราะมันต้องเก็บ $s_{n-1}$ ข้ามเฟรม ถ้าสร้างใหม่ทุกเฟรมความจำจะถูกล้างทิ้ง

> อยากเห็นผลของ $\alpha$ ให้ชัด ลองตั้ง `EMA_ALPHA = 0.9` เทียบกับ `0.2` แล้วรัน: 0.9 ตอบไวแต่ยังแกว่ง, 0.2 นิ่งมากแต่ตามช้า — ไม่มีค่าที่ "ถูกที่สุด" มีแต่ค่าที่ "เหมาะกับงานของทีม"

---

# เสา DAQ — เซนเซอร์ดิบเป็นบริบท

Guardian ไม่ได้ดูแค่คำตอบของโมเดล มันอ่านเซนเซอร์ดิบคู่ขนานไปด้วย เพื่อให้ผู้ใช้ (และตัวมันเอง) รู้ "สถานการณ์รอบตัว"

```python
ax, ay, az = sensors.bmi270.acceleration()   # เสา DAQ: อ่านดิบ
mag = (ax*ax + ay*ay + az*az) ** 0.5          # ขนาดเวกเตอร์ความเร่ง
ctx.text("motion: %.1f" % mag)                # โชว์เป็นบริบท
```

- อยู่นิ่ง `mag` ~9.8 (แรงโน้มถ่วง) · ถูกจับ/เขย่า `mag` พุ่งขึ้น
- ประโยชน์จริง: โมเดลเสียง (Baby Cry/Cough) อาจโดน **noise การจับเครื่อง** รบกวน — เห็น motion สูงตอนได้ verdict ก็รู้ว่าควรระวัง
- นี่คือประตูสู่ **sensor fusion**: รวม "โมเดลว่าไง" กับ "เซนเซอร์ดิบว่าไง" ก่อนตัดสินใจ (โจทย์ต่อยอด)

> การอ่านเซนเซอร์ดิบคือทักษะจากชุดบทเรียน DAQ (โมดูล 2) — capstone เอามาวางข้าง verdict ให้เห็นว่าเสาแรกสุดของวงจรก็ยังมีบทบาทในผลิตภัณฑ์ปลายทาง

---

# ชั้นตัดสินใจ — กัน false positive ยังไง

ปัญหาใหญ่สุดของ Edge AI ที่ใช้งานจริง ไม่ใช่ "เจอไหม" แต่คือ "เตือนมั่วบ่อยแค่ไหน" Guardian ใช้สามด่านกรองซ้อนกัน:

<div style="text-align:center;margin:6px 0">
<svg width="900" height="150" viewBox="0 0 900 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arDec" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="46" width="196" height="60" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="112" y="72" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">ด่าน 1 · คลาสถูกตัว</text>
  <text x="112" y="92" font-size="11" fill="#666" text-anchor="middle">top == alert_idx</text>
  <rect x="244" y="46" width="196" height="60" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="342" y="72" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">ด่าน 2 · มั่นใจพอ</text>
  <text x="342" y="92" font-size="11" fill="#666" text-anchor="middle">conf_s ≥ CONF_FLOOR</text>
  <rect x="474" y="46" width="196" height="60" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="572" y="72" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">ด่าน 3 · ติดกันพอ</text>
  <text x="572" y="92" font-size="11" fill="#666" text-anchor="middle">streak ≥ HITS_NEEDED</text>
  <rect x="704" y="46" width="182" height="60" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="795" y="72" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">ยิง action ครั้งเดียว</text>
  <text x="795" y="92" font-size="11" fill="#666" text-anchor="middle">edge-trigger (fired)</text>
  <line x1="210" y1="76" x2="242" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arDec)"/>
  <line x1="440" y1="76" x2="472" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arDec)"/>
  <line x1="670" y1="76" x2="702" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arDec)"/>
  <text x="450" y="132" font-size="11" fill="#888" text-anchor="middle">พลาดด่านไหน → streak = 0, fired = False (พร้อมเริ่มนับใหม่)</text>
</svg>
</div>

- **debounce** (`streak`) ตัดพีคหลอกที่โผล่เฟรมเดียวทิ้ง — ต้อง "ยืนยันตัวเอง" หลายครั้งก่อน
- **edge-trigger** (`fired`) ยิงครั้งเดียวตอน "เพิ่งเข้าเหตุการณ์" ไม่รัวทุกเฟรมที่ยังเจออยู่

> สามด่านนี้คือ "วิศวกรรมความน่าเชื่อถือ" — ชุดบทเรียน Apps (บทเรียน 6.3–6.4) ปูเรื่อง debounce มาแล้ว วันนี้เอามาเป็นหัวใจการตัดสินใจของผลิตภัณฑ์

---

# คณิตของเสา DAQ + ด่านตัดสินใจ

**ขนาดเวกเตอร์ความเร่ง** (เติมช่อง 2) — ยุบสามแกนเป็นค่าเดียวที่ไม่ขึ้นกับทิศทางบอร์ด:

$$mag = \sqrt{a_x^2 + a_y^2 + a_z^2}$$

- $a_x, a_y, a_z$ — ความเร่งดิบสามแกนจาก `sensors.bmi270.acceleration()` (หน่วย m/s²)
- อยู่นิ่ง แรงโน้มถ่วงดึงแกนเดียว จึงได้ $mag \approx 9.8$ · ถูกจับ/เขย่า → $mag$ พุ่งสูงขึ้น

**เงื่อนไขยิง action** (สามด่านของช่อง 5) — ต้องเป็นจริง **พร้อมกันทั้งหมด** ถึงนับว่า "เจอ":

$$\text{fire} \iff (top = \text{alert\_idx}) \;\wedge\; (s_n \ge \text{CONF\_FLOOR}) \;\wedge\; (\text{streak} \ge \text{HITS\_NEEDED})$$

- ด่านหนึ่งดูว่าคลาสถูกตัว · ด่านสองดูว่ามั่นใจพอ (ใช้ $s_n$ ที่กรองแล้ว ไม่ใช่ $c_n$ ดิบ) · ด่านสามดูว่า "ติดกันพอ"
- $\wedge$ คือ AND — สัญลักษณ์นี้แหละที่บังคับให้ทั้งสามต้องผ่านพร้อมกัน

**ทำไมสำคัญ:** false positive ส่วนใหญ่ผ่านได้แค่หนึ่งหรือสองด่าน การบังคับ $\wedge$ ครบสามคือเหตุผลที่พีคหลอกแวบเดียวไม่ทำให้ Guardian เตือน

> ร้อยกลับเข้าสามเสา: เสา DAQ ให้ $mag$, เสา Processing ให้ $s_n$, เสา Apps รวมทุกอย่างเป็น $\text{fire}$ — คณิตสามบรรทัดนี้คือสามเสาในการตัดสินใจครั้งเดียว

---

# การตัดสินใจเชิงวิศวกรรม — เลือกอะไร แลกกับอะไร

capstone ที่ดีต้อง "อธิบายการแลกเปลี่ยนได้" ไม่ใช่แค่ "รันได้" ทุกปุ่มออกแบบมีราคาสองด้าน:

| ปุ่มออกแบบ | ตั้งสูง → | ตั้งต่ำ → | แลกอะไร |
|---|---|---|---|
| `CONF_FLOOR` | พลาดของจริง (miss) | เตือนมั่ว (false +) | ความไว vs ความแม่น |
| `HITS_NEEDED` | ตอบช้าลง | เตือนจากพีคหลอก | latency vs false + |
| `EMA_ALPHA` | ตอบไวแต่แกว่ง | นิ่งแต่หน่วง | ตอบสนอง vs เสถียร |
| `time.sleep_ms` | ประหยัดไฟ/พลาดจังหวะ | กิน CPU/ไว | พลังงาน vs ความไว |

- ไม่มีค่า "ถูกที่สุด" — ขึ้นกับงาน: ตรวจการล้มของผู้สูงอายุ ยอม false positive ดีกว่า miss · ป้ายโฆษณากวักมือ ยอม miss ดีกว่ากวนคนเดิน
- งานทีมวันนี้: เลือกค่าพวกนี้ **แล้วเขียนเหตุผล** ว่าทำไม เหมาะกับผลิตภัณฑ์ของคุณ

> นี่คือคำถามวิศวกรที่คอร์สฝึกมาทั้งเทอม — "โมเดลตัวนี้ควรอยู่ที่ไหน / ตั้งเกณฑ์เท่าไร / แลกอะไรกับอะไร" capstone คือที่ที่คุณตอบด้วยผลิตภัณฑ์จริง

---

# design → build → ship

capstone ไม่ได้เริ่มที่โค้ด มันเริ่มที่ **ออกแบบ** แล้วค่อยสร้าง แล้วค่อยส่งมอบ — สามจังหวะเดียวกับงานจริง

<div style="text-align:center;margin:8px 0">
<svg width="880" height="150" viewBox="0 0 880 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arDS" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="42" width="250" height="72" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="145" y="70" font-size="15" font-weight="700" fill="#6a1b9a" text-anchor="middle">1 · Design</text>
  <text x="145" y="92" font-size="11" fill="#666" text-anchor="middle">เฝ้าอะไร · action อะไร · เกณฑ์เท่าไร</text>
  <rect x="315" y="42" width="250" height="72" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="440" y="70" font-size="15" font-weight="700" fill="#1565c0" text-anchor="middle">2 · Build</text>
  <text x="440" y="92" font-size="11" fill="#666" text-anchor="middle">เติม 5 บรรทัด + จูนค่าออกแบบ</text>
  <rect x="610" y="42" width="250" height="72" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="735" y="70" font-size="15" font-weight="700" fill="#2e7d32" text-anchor="middle">3 · Ship</text>
  <text x="735" y="92" font-size="11" fill="#666" text-anchor="middle">เดโม + commit + เล่าเหตุผล</text>
  <line x1="270" y1="78" x2="313" y2="78" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arDS)"/>
  <line x1="565" y1="78" x2="608" y2="78" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arDS)"/>
  <path d="M735,114 C735,140 145,140 145,116" fill="none" stroke="#9e9e9e" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arDS)"/>
  <text x="440" y="140" font-size="11" fill="#9e9e9e" text-anchor="middle">เดโมแล้วเจอปัญหา → กลับไปออกแบบใหม่ (วนได้)</text>
</svg>
</div>

> อย่ากระโดดไป Build เลย — ใช้เวลา 15 นาทีแรกที่ **Design** ในบันทึกการเรียน (เฝ้าอะไร ทำไม, action คืออะไร, ตั้งเกณฑ์เท่าไรเพราะอะไร) แล้ว Build จะเร็วและตรง

---

# รู้จักโมดูลที่ capstone ใช้

Guardian ยืนบนโมดูลที่เราคุ้นมือแล้วทั้งหมด — ไม่มี API ใหม่ให้จำ มีแต่การเอามาต่อกัน

| โมดูล | ใช้ทำอะไรใน Guardian | เสา |
|---|---|---|
| `edge_ai` | `models` / `select` / `result` / `stop` / `CONF_FLOOR` | Apps |
| `dsp` | `dsp.EMA(alpha=...)` กรองความมั่นใจ | Processing |
| `sensors` | `sensors.bmi270.acceleration()` อ่านบริบทดิบ | DAQ |
| `ui` / `lcd` | `Dropdown/Button/Seg7/Bar/Label/Panel` + `ui.tone` + `lcd.console` | Apps |

- ทุกตัวเป็น API จริงที่ใช้มาทั้งคอร์ส บนบอร์ดกับ Emulator เหมือนกัน (BENTO IDE มีคำอธิบายของแต่ละคำสั่งในตัว)
- `ui.tone(note, wave, vol, ms)` เล่นเสียงผ่าน SFX mixer ฝั่ง CM55 — เราใช้ยืนยัน action

> ถ้าอยากทบทวนคำสั่งไหน เปิด REPL ถามฮาร์ดแวร์ตรงๆ ได้เลย เช่น `import edge_ai; edge_ai.models()` — นิสัย "ถามก่อนเดา" จากบทเรียน 1.1–1.3 ยังใช้ได้จนชุดบทเรียนสุดท้าย
