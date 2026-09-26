---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 6.1 — หกโมเดลกับ edge_ai API: แอปที่โฟกัสโมเดลเดียว"
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

# บทเรียน 6.1 — หกโมเดลกับ edge_ai API: แอปที่โฟกัสโมเดลเดียว
## สร้าง "แอปโฟกัสโมเดลเดียว" ของคุณเอง

**โมดูล 6 — แอป Edge AI**

**เปิด โมดูล 6 (Apps, Pillar 5)**

> คาถาประจำบทเรียน: **"เมนูให้เลือกทุกอย่าง คือเดโม — แอปที่ทำงานจริงมักโฟกัสโมเดลเดียว แล้วเอา verdict ไปทำอะไรสักอย่าง"**

MicroPython บนบอร์ด BENTO (PSoC Edge · Cortex-M55 + Ethos-U55 NPU)

---

# เปิดบทเรียนด้วยของจริงก่อน

เหมือนทุกบทเรียน เราเริ่มแบบ **กลับด้าน** — รันของที่ทำงานได้ก่อน แล้วค่อยแกะ วันนี้เปิดตัวอย่าง [`16_edge_ai_sound_events.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l01-focused-apps/examples/16_edge_ai_sound_events.py) มันคือเมนูรวมสามโมเดลเสียง (ไอ / เสียงเตือน / ไซเรน) ในหน้าเดียว

<div style="text-align:center;margin:10px 0">
<svg width="820" height="150" viewBox="0 0 820 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arOpen" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="40" width="180" height="70" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="104" y="72" font-size="15" font-weight="700" fill="#2e7d32" text-anchor="middle">รันเดโมเสียง</text>
  <text x="104" y="94" font-size="12" fill="#555" text-anchor="middle">ตัวอย่าง 16</text>
  <rect x="234" y="40" width="180" height="70" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="324" y="72" font-size="15" font-weight="700" fill="#1565c0" text-anchor="middle">แกะดูข้างใน</text>
  <text x="324" y="94" font-size="12" fill="#555" text-anchor="middle">find_model + result</text>
  <rect x="454" y="40" width="180" height="70" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="544" y="72" font-size="15" font-weight="700" fill="#e65100" text-anchor="middle">โฟกัสโมเดลเดียว</text>
  <text x="544" y="94" font-size="12" fill="#555" text-anchor="middle">+ นับเมื่อเจอ</text>
  <rect x="674" y="40" width="132" height="70" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="740" y="72" font-size="15" font-weight="700" fill="#6a1b9a" text-anchor="middle">รีทาร์เก็ต</text>
  <text x="740" y="94" font-size="12" fill="#555" text-anchor="middle">cough/alarm/siren</text>
  <line x1="194" y1="75" x2="230" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="414" y1="75" x2="450" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="634" y1="75" x2="670" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
</svg>
</div>

> บทเรียน 1.1–1.3 เราทำ "เมนู 6 โมเดล" ให้เลือกได้ทุกตัว — สนุกดีสำหรับเดโม แต่วันนี้เราจะถอยไปอีกก้าว: เอาโมเดลเดียวมาทำเป็น **แอป** ที่มีหน้าจอเฉพาะตัว แล้วต่อ verdict เข้ากับการกระทำจริง

---

# เป้าหมายของชุดบทเรียนนี้

จบชุดบทเรียนนี้เราจะเปลี่ยนจาก "รันโมเดล" เป็น "สร้างแอป" ครบ 4 เรื่อง แล้วปิดท้ายด้วยแอปที่คุณสร้างเอง:

1. **เมนู กับ แอปโฟกัส ต่างกันตรงไหน** และทำไมงานจริงมักเลือกอย่างหลัง
2. **`find_model()`** — เล็งโมเดลด้วยคีย์เวิร์ด แทนที่จะ hard-code เลข index
3. อ่าน **`scores` ทุกคลาส + `latency_ms`** ให้เป็น ไม่ใช่แค่คลาสที่ชนะ
4. **จาก verdict สู่ action** — นับเมื่อคลาสเป้าหมายข้ามเกณฑ์ `CONF_FLOOR` (ก้าวแรกของ Apps)
5. ลงมือ: เติม [`s15_apps.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l02-focused-app-lab/practice/s15_apps.py) ให้เป็น **แอป Cough** ที่นับจำนวนครั้งที่ไอบนจอ

ปลายทางวันนี้: แอปโฟกัสหน้าตาสะอาด รันโมเดลเดียว โชว์คลาสที่ชนะ + แถบทุกคลาส และตัวนับที่เพิ่มขึ้นจริงเมื่อเจอเสียงเป้าหมาย

> วันนี้เรายังไม่แตะ RGB/เสียง/WiFi (นั่นคือ บทเรียน 6.3–6.6) เราโฟกัสที่ "โครงของแอปต่อโมเดล" กับการกระทำเบาที่สุดหนึ่งอย่าง คือการนับ

---

# ชุดบทเรียนนี้อยู่ตรงไหนของวงจร

เราเดินมาครบสี่ Pillar แรกแล้ว (DAQ → Processing → Analysis → Training) ชุดบทเรียนนี้เข้าสู่ **Pillar 5 · Apps** — ขั้นที่เอาโมเดลไป "ใช้งาน" จริง

<div style="text-align:center;margin:6px 0">
<svg width="920" height="150" viewBox="0 0 920 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arLC" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g text-anchor="middle">
    <rect x="10" y="46" width="160" height="60" rx="12" fill="#eceff1" stroke="#90a4ae" stroke-width="2"/>
    <text x="90" y="72" font-size="13" font-weight="700" fill="#607d8b">1 · DAQ</text>
    <text x="90" y="92" font-size="10" fill="#999">โมดูล 2</text>
    <rect x="196" y="46" width="160" height="60" rx="12" fill="#eceff1" stroke="#90a4ae" stroke-width="2"/>
    <text x="276" y="72" font-size="13" font-weight="700" fill="#607d8b">2 · Processing</text>
    <text x="276" y="92" font-size="10" fill="#999">โมดูล 3</text>
    <rect x="382" y="46" width="160" height="60" rx="12" fill="#eceff1" stroke="#90a4ae" stroke-width="2"/>
    <text x="462" y="72" font-size="13" font-weight="700" fill="#607d8b">3 · Analysis</text>
    <text x="462" y="92" font-size="10" fill="#999">โมดูล 4</text>
    <rect x="568" y="46" width="160" height="60" rx="12" fill="#eceff1" stroke="#90a4ae" stroke-width="2"/>
    <text x="648" y="72" font-size="13" font-weight="700" fill="#607d8b">4 · Training</text>
    <text x="648" y="92" font-size="10" fill="#999">โมดูล 5</text>
    <rect x="754" y="40" width="160" height="72" rx="12" fill="#e0f7fa" stroke="#00838f" stroke-width="3"/>
    <text x="834" y="70" font-size="14" font-weight="700" fill="#00838f">5 · Apps</text>
    <text x="834" y="90" font-size="11" fill="#00838f">ชุดบทเรียนนี้ (6.1–6.2)</text>
  </g>
  <line x1="170" y1="76" x2="194" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <line x1="356" y1="76" x2="380" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <line x1="542" y1="76" x2="566" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <line x1="728" y1="76" x2="752" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <text x="462" y="132" font-size="12" fill="#888" text-anchor="middle">Apps คือปลายทางของทั้งวงจร — เอาทุกอย่างที่สร้างมา มาทำเป็นของที่ใช้ได้จริง</text>
</svg>
</div>

- บทเรียน 1.1–1.3 เราเคยแตะ Apps มาแล้วสั้นๆ (เมนู 6 โมเดล) และ บทเรียน 1.6–1.7 เราแกะ path จาก verdict สู่ action
- ชุดบทเรียนนี้เอาทั้งสองมาต่อยอด: สร้าง **แอปที่โฟกัสและใช้ได้จริง** ไม่ใช่แค่เดโมเมนู
- บทเรียน 6.3–6.4 (ชุดบทเรียนถัดไป) จะต่อ action ให้แรงขึ้น (RGB/เสียง/log + debounce เต็มรูปแบบ) · บทเรียน 6.5–6.6 ต่อ IoT

> เราปิดวงกลับมาที่จุดเริ่ม — แต่รอบนี้คุณเข้าใจทุกขั้นที่อยู่เบื้องหลังโมเดลแล้ว การสร้างแอปจึงไม่ใช่กล่องดำอีกต่อไป

---

# ทบทวนจากบทเรียน 1.6–1.7 — verdict สู่ action

บทเรียน 1.6–1.7 เราแกะแอป Edge AI จนเห็น "เส้นทางของผล" — จากเซนเซอร์ไปจนถึงการกระทำ วันนี้เราต่อจากปลายเส้นนั้น

<div style="text-align:center;margin:6px 0">
<svg width="900" height="140" viewBox="0 0 900 140" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arV" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="16" y="44" width="150" height="54" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="91" y="68" font-size="12" font-weight="700" fill="#1565c0" text-anchor="middle">เซนเซอร์</text>
  <text x="91" y="86" font-size="10" fill="#666" text-anchor="middle">ไมค์ / IMU / เรดาร์</text>
  <rect x="206" y="44" width="150" height="54" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="281" y="68" font-size="12" font-weight="700" fill="#6a1b9a" text-anchor="middle">โมเดล (NPU)</text>
  <text x="281" y="86" font-size="10" fill="#666" text-anchor="middle">อนุมาน</text>
  <rect x="396" y="44" width="160" height="54" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="476" y="66" font-size="12" font-weight="700" fill="#e65100" text-anchor="middle">verdict</text>
  <text x="476" y="84" font-size="10" fill="#666" text-anchor="middle">label · conf · scores</text>
  <rect x="596" y="44" width="150" height="54" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="671" y="66" font-size="12" font-weight="700" fill="#2e7d32" text-anchor="middle">action</text>
  <text x="671" y="84" font-size="10" fill="#666" text-anchor="middle">นับ / เตือน / log</text>
  <line x1="166" y1="71" x2="204" y2="71" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arV)"/>
  <line x1="356" y1="71" x2="394" y2="71" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arV)"/>
  <line x1="556" y1="71" x2="594" y2="71" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arV)"/>
  <rect x="392" y="112" width="360" height="22" rx="6" fill="none" stroke="#2e7d32" stroke-dasharray="5 4"/>
  <text x="572" y="128" font-size="11" fill="#2e7d32" text-anchor="middle">โฟกัสของชุดบทเรียนนี้: จาก verdict → action ที่เบาที่สุด</text>
</svg>
</div>

- โมดูล 1 หยุดที่ช่อง **verdict** เป็นหลัก — เอา `label` + `conf` ขึ้นจอ
- ชุดบทเรียนนี้เราขยับไปช่อง **action** ช่องแรก: "นับ" เมื่อคลาสเป้าหมายมาแบบมั่นใจ
- การนับดูเล็กน้อย แต่มันสอนหลักการเดียวกับ action ที่ใหญ่กว่า: **ตัดสินใจว่าจะเชื่อ verdict เมื่อไร แล้วค่อยลงมือ**

> "นับ" คือ action ที่ปลอดภัยที่สุดสำหรับเรียนรู้ — ไม่มีอะไรพัง แต่คุณจะได้เจอปัญหาจริงของ Apps ทันที: นับเฟ้อเพราะเสียงกระพริบ, false positive จาก conf ต่ำ เดี๋ยวเราแก้ทีละอย่าง

---

# เมนู กับ แอปโฟกัส ต่างกันตรงไหน

ทั้งคู่ใช้ `edge_ai` ตัวเดียวกัน ต่างกันที่ **เจตนาของการออกแบบ** — และงานจริงเกือบทั้งหมดเป็นแบบขวา

<div style="text-align:center;margin:6px 0">
<svg width="860" height="210" viewBox="0 0 860 210" font-family="DejaVu Sans, sans-serif">
  <rect x="12" y="10" width="410" height="190" rx="12" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
  <text x="217" y="36" font-size="15" font-weight="700" fill="#455a64" text-anchor="middle">เมนู (1.1–1.3 · ตัวอย่าง 12/16)</text>
  <text x="217" y="64" font-size="12" fill="#455a64" text-anchor="middle">dropdown เลือกได้ทุกโมเดล</text>
  <text x="217" y="86" font-size="12" fill="#455a64" text-anchor="middle">UI กลางๆ ใช้ได้กับทุกตัว</text>
  <text x="217" y="108" font-size="12" fill="#455a64" text-anchor="middle">ผู้ใช้ต้องรู้ว่าจะเลือกอะไร</text>
  <text x="217" y="134" font-size="12" fill="#2e7d32" text-anchor="middle">ดีสำหรับ: สำรวจ · เดโม · ทดสอบ</text>
  <text x="217" y="160" font-size="12" fill="#c62828" text-anchor="middle">ไม่ดีสำหรับ: สินค้าจริง</text>
  <text x="217" y="182" font-size="11" fill="#888" text-anchor="middle">(เครื่องตรวจเสียงไอ ไม่ควรให้เลือกโมเดลเอง)</text>
  <rect x="438" y="10" width="410" height="190" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="643" y="36" font-size="15" font-weight="700" fill="#2e7d32" text-anchor="middle">แอปโฟกัส (6.1–6.2 · ตัวอย่าง 13/14/15)</text>
  <text x="643" y="64" font-size="12" fill="#2e7d32" text-anchor="middle">เล็งโมเดลเดียวตอนเปิดแอป</text>
  <text x="643" y="86" font-size="12" fill="#2e7d32" text-anchor="middle">UI ออกแบบเฉพาะงานนั้น</text>
  <text x="643" y="108" font-size="12" fill="#2e7d32" text-anchor="middle">ผู้ใช้แค่ "ใช้" ไม่ต้องเลือก</text>
  <text x="643" y="134" font-size="12" fill="#2e7d32" text-anchor="middle">verdict ต่อกับ action ได้เต็มที่</text>
  <text x="643" y="160" font-size="12" fill="#455a64" text-anchor="middle">ดีสำหรับ: สินค้า · งานเฉพาะทาง</text>
  <text x="643" y="182" font-size="11" fill="#888" text-anchor="middle">คือรูปแบบที่เราจะสร้างวันนี้</text>
</svg>
</div>

> คิดง่ายๆ: เมนูคือ "รีโมตรวม" ที่คุมทีวีได้ทุกยี่ห้อ ส่วนแอปโฟกัสคือ "ปุ่มเดียว" บนเครื่องที่ทำงานหนึ่งอย่างให้ดีที่สุด งานวิศวกรรมจริงต้องการอย่างหลังมากกว่า

---

# ตระกูลแอปอ้างอิง — ตัวอย่าง 13 ถึง 16

ก่อนสร้างเอง มาดูของที่มีอยู่ ทั้งสี่ตัวคือ "แอปต่อโมเดล" ที่โครงเกือบเหมือนกันเป๊ะ ต่างแค่โมเดลกับ UI นิดหน่อย

| # | ไฟล์ | โมเดล/เซนเซอร์ | จุดเด่นที่เพิ่มจากเมนู |
|---|---|---|---|
| 13 | [`13_edge_ai_motion.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l06-edge-ai-app-anatomy/examples/13_edge_ai_motion.py) | Motion (IMU) | โฟกัสตัวเดียว + `find_model` + latency |
| 14 | [`14_edge_ai_babycry.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l01-focused-apps/examples/14_edge_ai_babycry.py) | Baby Cry (MIC) | การ์ดผลลัพธ์ + แถบความมั่นใจต่อคลาส |
| 15 | [`15_edge_ai_radar_push.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l01-focused-apps/examples/15_edge_ai_radar_push.py) | Push (RADAR) | โมเดล float32 + คำใบ้ระยะยืน |
| 16 | [`16_edge_ai_sound_events.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l01-focused-apps/examples/16_edge_ai_sound_events.py) | Cough/Alarm/Siren (MIC) | คัดเฉพาะโมเดลไมค์เข้ามาในเมนูย่อย |

- สังเกตว่าทั้งสี่ตัวมีก้อนเดียวกัน: `find_model()` → `select()` → ลูป `result()` → วาด verdict + แถบ → `finally: stop()`
- ตัวอย่าง 13/14/15 คือ **แอปโฟกัสโมเดลเดียว** (แม่แบบของเรา) · ตัวอย่าง 16 เป็นเมนูย่อยของสามโมเดลเสียง
- งานชุดบทเรียนนี้: เอาโครงเดียวกันนี้ **บวก action หนึ่งอย่าง** (การนับ) แล้วทำให้รีทาร์เก็ตง่ายด้วยตัวแปรบนหัวไฟล์

> จำ pattern นี้ไว้ให้ขึ้นใจ เพราะแอป Edge AI 90% ที่คุณจะเขียนต่อจากนี้ ล้วนเป็นโครงนี้ทั้งนั้น เปลี่ยนแค่ "โมเดลอะไร" กับ "ทำอะไรกับผล"

---

# 6 โมเดล — ตัวไหนเอามาทำแอปโฟกัสได้บ้าง

ทะเบียนโมเดลยังเป็น 6 ตัวเดิมจากบทเรียน 1.1–1.3 ชุดบทเรียนนี้เราจะหยิบ **โมเดลเสียง** มาทำแอป เพราะทดสอบง่าย (ส่งเสียงเอง) และเป็นสนามใหญ่ของ Edge AI จริง

| # | ชื่อโมเดล | เซนเซอร์ | คลาส (labels) | เหมาะทำแอป |
|---|---|---|---|---|
| 0 | Motion Detection | IMU | idle, circle, shaking | ตัวอย่าง 13 |
| 1 | Baby Cry Detection | MIC | unlabelled, baby_cry | ตัวอย่าง 14 |
| 2 | Push Detection | RADAR | unlabelled, Push | ตัวอย่าง 15 |
| 3 | **Cough Detection** | MIC | unlabelled, cough | **ชุดบทเรียนนี้ (ค่าตั้งต้น)** |
| 4 | Alarm Detection | MIC | unlabelled, alarm | รีทาร์เก็ต |
| 5 | Siren Detection | MIC | unlabelled, sirens | รีทาร์เก็ต |

- ค่าตั้งต้นของ [`s15_apps.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l02-focused-app-lab/practice/s15_apps.py) เล็งที่ **Cough Detection** — เราสร้างแอป "เครื่องนับเสียงไอ"
- โมเดล Cough/Alarm/Siren มาจาก DEEPCRAFT Ready-Model แต่ละตัวมีสองคลาส: `unlabelled` กับคลาสเป้าหมาย
- การบ้าน: เปลี่ยนสองบรรทัดบนหัวไฟล์ให้เป็น Alarm และ Siren แล้วเซฟเป็นไฟล์แยก

> เราเลือก Cough เป็นตัวตั้งต้นเพราะ "ไอ" เป็นเสียงสั้นชัด นับง่าย เห็นตัวเลขขยับทันที — เหมาะกับการเรียนเรื่อง "ขอบขาขึ้น" กับ debounce ที่จะเจอต่อไป

---

# ทวนคำสั่งหลักของ edge_ai

แอปโฟกัสยืนอยู่บนคำสั่งเดิมจาก บทเรียน 1.1–1.3 แต่ชุดบทเรียนนี้เราตัด `count()`/`models()` ออกจากลูปหลัก เหลือแค่สามตัวที่ทำงานจริงตอนรัน

| คำสั่ง | ชุดบทเรียนนี้ใช้ทำอะไร |
|---|---|
| `edge_ai.models()` | เรียกครั้งเดียวตอนเปิด — ให้ `find_model()` ค้นทะเบียน |
| `edge_ai.select(n)` | เริ่มโมเดลเป้าหมายตัวเดียว (ครั้งเดียว ไม่มีปุ่ม Load) |
| `edge_ai.result()` | ดึง verdict ล่าสุดในลูป — หัวใจของแอป |
| `edge_ai.stop()` | ปิดเครื่องยนต์ตอนออก (`finally`) |
| `edge_ai.CONF_FLOOR` | เส้นแบ่ง 0.50 — ใช้ตัดสินว่าจะ "นับ" ไหม |
| `edge_ai.SENSOR_MIC` | ค่าคงที่ = 2 — เซนเซอร์สำรองให้ `find_model()` |

- ต่างจาก บทเรียน 1.1–1.3 ตรงที่ `select()` เรียก **ครั้งเดียวตอนเปิดแอป** ไม่ต้องรอผู้ใช้กด Load — แอปโฟกัสรู้อยู่แล้วว่าจะรันอะไร
- `CONF_FLOOR` คราวนี้ไม่ใช่แค่เปลี่ยนสี แต่เป็น **เงื่อนไขของ action** จริง (นับหรือไม่นับ)

> น้อยลงแต่คมขึ้น — เมื่อคุณรู้ว่าจะรันโมเดลไหน โค้ดก็สั้นลง เหลือแต่แก่น: อ่านผล แล้วตัดสินใจ

---

# result() เจาะลึก — คราวนี้เราใช้ scores กับ latency

`result()` คืน dict เดิมจาก บทเรียน 1.1–1.3 แต่ชุดบทเรียนนี้เราจะใช้ฟิลด์ให้ครบขึ้น โดยเฉพาะ `scores` (ทุกคลาส) และ `latency_ms`

```python
r = edge_ai.result()
# {'index': 3, 'label': 'cough', 'top': 1, 'conf': 0.88,
#  'scores': [0.12, 0.88], 'latency_ms': 6.4, 'seq': 210, 'running': True}
```

| ฟิลด์ | ชุดบทเรียนนี้ใช้ยังไง |
|---|---|
| `label` + `conf` | คำตอบสั้น + ใช้เทียบ `CONF_FLOOR` เพื่อตัดสินใจนับ |
| `top` | index คลาสที่ชนะ — ระบายแถบตัวชนะเป็นเขียว |
| `scores` | คะแนน **ทุกคลาส** — วาดแถบครบทุกแถว เห็น "ความสูสี" |
| `latency_ms` | เวลาอนุมานจริง — โชว์บนการ์ด เทียบข้ามเซนเซอร์ได้ |
| `seq` | เลขลำดับผล — กันวาดจอซ้ำ (วาดเฉพาะตอน `seq` เปลี่ยน) |

> ใน บทเรียน 1.1–1.3 เราสนใจแค่ `label`/`conf` — ชุดบทเรียนนี้ `scores` กับ `latency_ms` เลื่อนมาเป็นพระเอก เพราะแอปที่ดีต้องบอกผู้ใช้ได้ว่า "มั่นใจแค่ไหน" และ "เร็วแค่ไหน" ไม่ใช่แค่ "คืออะไร"

---

# find_model() — เล็งด้วยคีย์เวิร์ด ไม่ hard-code index

หัวใจที่ทำให้แอปโฟกัส "ทน" คือไม่ผูกกับเลข index ตายตัว เราค้นทะเบียนจากชื่อแทน แบบเดียวกับตัวอย่าง 13–16

```python
def find_model(keywords, sensor):
    ms = edge_ai.models()
    for m in ms:                       # 1) ลองจับชื่อก่อน
        for k in keywords:
            if k.lower() in m['name'].lower():
                return m
    for m in ms:                       # 2) ไม่เจอชื่อ -> ใช้เซนเซอร์ที่ตรงกันตัวแรก
        if m['sensor'] == sensor:
            return m
    return ms[0]                       # 3) กันเหนียว -> ตัวแรกสุด
```

- ส่ง `("cough",)` เข้าไป มันจะคืน dict ของโมเดล Cough ไม่ว่ามันจะอยู่ index เท่าไร
- ถ้าเฟิร์มแวร์สลับลำดับโมเดล หรือเพิ่ม/ลดโมเดล โค้ดนี้ยังหาถูกตัว — ต่างจาก `select(3)` ที่จะพังทันที
- มีสามชั้นถอยหลัง (ชื่อ → เซนเซอร์ → ตัวแรก) เพื่อให้แอป **ไม่ crash** แม้หาไม่เจอเป๊ะ

> นี่คือนิสัยเดียวกับ บทเรียน 1.1–1.3 — "ถามฮาร์ดแวร์ อย่าเดา" แค่คราวนี้เราถามแบบเจาะจง "ขอโมเดลที่ชื่อมีคำว่า cough" แล้วปล่อยให้เฟิร์มแวร์ตอบว่ามันอยู่ตรงไหน

---

# โครงของแอปโฟกัส

จับโครงให้ได้ก่อนดูโค้ดจริง แอปโฟกัสทุกตัวเดินตามห้าจังหวะนี้ — เป็นญาติสนิทของ "โครงร่วม" จาก บทเรียน 1.4–1.5 แต่ `select` ขยับมาอยู่ต้นเรื่อง

<div style="text-align:center;margin:6px 0">
<svg width="900" height="150" viewBox="0 0 900 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arSk" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="12" y="46" width="150" height="56" rx="10" fill="#cfd8dc" stroke="#607d8b" stroke-width="2"/>
  <text x="87" y="70" font-size="12" font-weight="700" fill="#455a64" text-anchor="middle">1 · find_model</text>
  <text x="87" y="90" font-size="10" fill="#666" text-anchor="middle">เล็งตัวเป้าหมาย</text>
  <rect x="186" y="46" width="150" height="56" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="261" y="70" font-size="12" font-weight="700" fill="#1565c0" text-anchor="middle">2 · สร้าง widget</text>
  <text x="261" y="90" font-size="10" fill="#666" text-anchor="middle">การ์ด + แถบคลาส</text>
  <rect x="360" y="46" width="150" height="56" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="435" y="70" font-size="12" font-weight="700" fill="#6a1b9a" text-anchor="middle">3 · select</text>
  <text x="435" y="90" font-size="10" fill="#666" text-anchor="middle">เริ่มครั้งเดียว</text>
  <rect x="534" y="46" width="160" height="56" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="614" y="66" font-size="12" font-weight="700" fill="#e65100" text-anchor="middle">4 · ลูป result</text>
  <text x="614" y="84" font-size="10" fill="#666" text-anchor="middle">verdict + action(นับ)</text>
  <rect x="718" y="46" width="170" height="56" rx="10" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
  <text x="803" y="66" font-size="12" font-weight="700" fill="#455a64" text-anchor="middle">5 · finally stop</text>
  <text x="803" y="84" font-size="10" fill="#666" text-anchor="middle">เก็บกวาด</text>
  <line x1="162" y1="74" x2="184" y2="74" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <line x1="336" y1="74" x2="358" y2="74" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <line x1="510" y1="74" x2="532" y2="74" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <line x1="694" y1="74" x2="716" y2="74" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <path d="M614,102 C614,128 435,128 435,104" fill="none" stroke="#9e9e9e" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arSk)"/>
  <text x="524" y="140" font-size="11" fill="#9e9e9e" text-anchor="middle">วนอ่านผลทุก ~150 ms</text>
</svg>
</div>

> ต่างจากเมนู บทเรียน 1.1–1.3 ตรงที่ **ไม่มีปุ่ม Load** — `select()` อยู่ก่อนลูปเลย เพราะแอปโฟกัส "รู้ตั้งแต่เปิด" ว่าจะรันโมเดลอะไร ผู้ใช้ไม่ต้องเลือก

---

# อ่าน scores ทุกคลาส — แถบต่อคลาส

`scores` คือหัวใจที่ทำให้ผู้ใช้ "เห็นความมั่นใจ" ไม่ใช่แค่คลาสเดียว เราวาดหนึ่งแถบต่อหนึ่งคลาส ตัวที่ชนะระบายเขียว

```python
top = r['top']
for i, (lb, br) in enumerate(rows):
    if i < len(r['scores']):
        br.value(int(r['scores'][i] * 100))   # ความสูงของแถบ = คะแนนคลาสนั้น
        br.color(GREEN if i == top else DIM)   # คลาสที่ชนะ = เขียว, ที่เหลือ = จาง
```

- โมเดล Cough มีสองคลาส `['unlabelled', 'cough']` เราจึงเห็นสองแถบ ขยับสวนทางกัน
- เวลาไอชัดๆ แถบ `cough` จะพุ่งเข้าใกล้ 100% แถบ `unlabelled` จะยุบลง
- เวลาเงียบ/เสียงอื่น แถบสองอันจะ **สูสี** — นี่แหละคือตอนที่ `conf` ต่ำกว่า `CONF_FLOOR`

> แถบทุกคลาสไม่ได้มีไว้สวยงามเฉยๆ มันบอกคุณว่าโมเดล "ลังเล" หรือ "ชัวร์" ด้วยตาเปล่า — ก่อนจะเชื่อคำตอบ ให้ดูว่าตัวชนะทิ้งห่างตัวอื่นแค่ไหน

---

# latency — เวลาอนุมานต่างกันตามเซนเซอร์

`latency_ms` คือเวลาที่ NPU ใช้อนุมานหนึ่งครั้ง แอปที่ดีควรโชว์ให้เห็น เพราะมันบอก "ความสด" ของคำตอบ

```python
lat.text("latency: %.1f ms" % r['latency_ms'])
```

- โมเดลเสียง (Cough/Alarm/Siren) มักใช้เวลาต่างจากโมเดล IMU (Motion) เพราะขนาดอินพุตและสถาปัตยกรรมต่างกัน
- ตัวเลขนี้เล็ก (ไม่กี่ ms) เพราะมี **Ethos-U55** ช่วยคูณเมทริกซ์ — ถ้าให้ CPU ทำเองจะช้ากว่าหลายเท่า
- ในงานจริง latency สำคัญมากกับงานที่ต้องตอบทันที (ตรวจการล้ม เสียงเตือน) — ช้าไปคือพลาดจังหวะ

> ลองสังเกตในแล็บ: สลับระหว่างแอป Cough (ไมค์) กับตัวอย่าง 13 (IMU) แล้วเทียบ `latency_ms` คุณจะเห็นด้วยตาว่า "โมเดลคนละแบบ กินเวลาคนละอย่าง" — นี่คือข้อมูลที่วิศวกรใช้เลือกโมเดล

---

# จาก verdict สู่ action — นับเมื่อข้าม CONF_FLOOR

นี่คือของใหม่จริงๆ ของชุดบทเรียนนี้ เราไม่หยุดที่การโชว์ผล แต่ "ทำอะไรสักอย่าง" เมื่อเจอคลาสเป้าหมายแบบมั่นใจ

```python
is_target = (r['label'] == TARGET_CLASS
             and r['conf'] >= edge_ai.CONF_FLOOR)   # เชื่อก็ต่อเมื่อมั่นใจถึงเกณฑ์
if is_target and not was_target:                    # นับเฉพาะ "ขอบขาขึ้น"
    hits += 1
    hits_lbl.text(str(hits))
was_target = is_target
```

- เงื่อนไขมีสองส่วน: คลาสต้องเป็นเป้าหมาย **และ** `conf` ต้องถึง `CONF_FLOOR` — ถ้าปล่อยเงื่อนไข conf ทิ้ง ตัวนับจะเก็บ false positive เต็มไปหมด
- `CONF_FLOOR` เลื่อนสถานะจาก "ตัวเปลี่ยนสี" (บทเรียน 1.1–1.3) มาเป็น **"ประตูของ action"** จริง
- นี่คือหลักการเดียวกับทุก action ในโลก Edge AI: **ตัดสินใจว่าจะเชื่อ verdict ไหม ก่อนลงมือ**

> action แรกของคุณคือการนับ — เล็กแต่จริง ในบทเรียน 6.3–6.4 เราจะเปลี่ยน `hits += 1` เป็น "จุด RGB / เล่นเสียง / เขียน log" ด้วยโครงตัดสินใจอันเดียวกันนี้

---

# คณิตเบื้องหลัง (1) — argmax เลือกคลาสที่ชนะ

โมเดลไม่ได้คืนแค่ "คลาสเดียว" แต่คืน `scores` เป็นคะแนนของทุกคลาส เราต้องเลือก "ตัวที่ชนะ" ออกมาหนึ่งตัว วิธีคิดคือหาตำแหน่งที่คะแนนสูงสุด:

$$\hat{y} \;=\; \arg\max_{i}\; s_i$$

โดยที่ $s = (s_0, s_1, \dots, s_{K-1})$ คือเวกเตอร์คะแนนของ $K$ คลาส และ $\hat{y}$ คือ index ของคลาสที่ชนะ (ในโค้ดคือ `r['top']`)

- $s_i$ — คะแนน (คล้ายความน่าจะเป็น) ของคลาสที่ $i$ รวมกันทุกคลาสได้ประมาณ 1
- $\arg\max$ — แปลว่า "เอา **index** ที่ทำให้ค่ามากที่สุด" ไม่ใช่ตัวเลขค่ามากที่สุด
- $\hat{y}$ — คลาสที่โมเดลเชียร์ที่สุด เราจึงระบายแถบของคลาสนี้เป็นสีเขียว

ตัวอย่างโมเดล Cough ที่มีสองคลาส `['unlabelled', 'cough']`: ได้ $s = (0.12,\ 0.88)$ → $\hat{y}=1$ → คลาส `cough` ชนะ, และ conf ของผลนี้คือ $0.88$

> argmax บอกแค่ "ใครชนะ" มันไม่เคยบอกว่า "ชนะขาดหรือชนะเฉียด" — เพราะแม้คะแนน $0.51$ ต่อ $0.49$ ก็ยังมีผู้ชนะ นั่นคือเหตุผลที่เราต้องดู conf ต่ออีกชั้นในสไลด์ถัดไป ก่อนจะเชื่อผล

---

# คณิตเบื้องหลัง (2) — CONF_FLOOR ประตูของ action

เพราะ argmax เลือกผู้ชนะเสมอ แม้ตอนคะแนนสูสี เราจึงตั้ง "เส้นแบ่งความมั่นใจ" ไว้อีกชั้น ก่อนจะยอมนับ ความมั่นใจของผลก็คือคะแนนของตัวที่ชนะ:

$$\text{conf} \;=\; s_{\hat{y}} \;=\; \max_i\, s_i$$

$$\text{count} \;\Longleftarrow\; \big(\,\text{label} = \text{TARGET}\,\big)\ \wedge\ \big(\,\text{conf} \ge \tau\,\big), \qquad \tau = 0.50$$

- $\text{conf}$ — คะแนนของคลาสที่ชนะ (ตัวสูงสุด) ใช้เป็นค่าความมั่นใจ
- $\tau$ (อ่านว่า "เทา") — เกณฑ์ขั้นต่ำ คือ `edge_ai.CONF_FLOOR` = $0.50$ ในชุดบทเรียนนี้
- $\wedge$ — เครื่องหมาย "และ" ทั้งสองเงื่อนไขต้องจริง **พร้อมกัน** จึงจะนับ

ทำไมมันสำคัญกับชุดบทเรียนนี้: ถ้าไม่มี $\tau$ ทุกครั้งที่ `cough` แค่ชนะแบบ $0.51$ ต่อ $0.49$ ก็จะถูกนับ ตัวนับจะเฟ้อไปด้วย false positive การใส่ $\tau$ คือการเขียนกฎว่า "เชื่อก็ต่อเมื่อมั่นใจถึงเกณฑ์" ซึ่งเป็นหัวใจของการเปลี่ยน verdict ให้เป็น action

> เลข $0.50$ ไม่ใช่ของศักดิ์สิทธิ์ — ตั้งสูง ($\tau=0.7$) ได้ความชัวร์แต่พลาดเสียงเบาๆ ตั้งต่ำ ($\tau=0.3$) จับได้ไวแต่ false positive เยอะ การเลือก $\tau$ คือการชั่งน้ำหนักสองอย่างนี้ให้เข้ากับงาน

---

# ขอบขาขึ้น — ทำไมต้อง "not was_target"

ถ้านับทุกผลที่เข้าคลาสเป้าหมาย จะได้ตัวเลขเฟ้อมหาศาล เพราะไอหนึ่งครั้งกินเวลาหลายผลอนุมาน เราจึงนับเฉพาะ **จังหวะที่เพิ่งเข้า**

<div style="text-align:center;margin:6px 0">
<svg width="880" height="150" viewBox="0 0 880 150" font-family="DejaVu Sans, sans-serif">
  <text x="20" y="30" font-size="12" fill="#455a64">conf ของคลาส cough ตามเวลา (เส้นประ = CONF_FLOOR)</text>
  <line x1="40" y1="100" x2="840" y2="100" stroke="#b0bec5" stroke-width="1.5"/>
  <line x1="40" y1="66" x2="840" y2="66" stroke="#ef6c00" stroke-width="1.5" stroke-dasharray="6 4"/>
  <text x="846" y="70" font-size="10" fill="#ef6c00" text-anchor="end"></text>
  <path d="M40,98 L150,96 L200,50 L280,48 L330,95 L470,97 L520,44 L600,46 L650,96 L840,98"
        fill="none" stroke="#6a1b9a" stroke-width="2.4"/>
  <circle cx="185" cy="60" r="6" fill="#2e7d32"/>
  <text x="185" y="42" font-size="11" fill="#2e7d32" text-anchor="middle">นับ +1</text>
  <circle cx="505" cy="58" r="6" fill="#2e7d32"/>
  <text x="505" y="40" font-size="11" fill="#2e7d32" text-anchor="middle">นับ +1</text>
  <text x="240" y="118" font-size="10" fill="#999" text-anchor="middle">ค้างเหนือเกณฑ์ = ไม่นับซ้ำ</text>
  <text x="560" y="118" font-size="10" fill="#999" text-anchor="middle">ค้างเหนือเกณฑ์ = ไม่นับซ้ำ</text>
</svg>
</div>

- `was_target` จำสถานะรอบก่อน เรานับเฉพาะตอน "รอบนี้เข้าเป้า แต่รอบก่อนยังไม่เข้า" (ขอบขาขึ้น false → true)
- ตราบใดที่เสียงยังดังค้างเหนือเกณฑ์ จะไม่นับซ้ำ ต้องตกลงต่ำกว่าเกณฑ์ก่อน แล้วขึ้นใหม่ถึงนับอีกครั้ง
- ในฉบับเต็ม (`examples/`) เราเสริม **debounce เบาๆ** อีกชั้น: ต้องเจอติดกันสองผลถึงนับ กันเสียงกระพริบชั่วขณะ

> เทคนิค "ขอบขาขึ้น" นี้เหมือนกับการอ่านปุ่มกดในคอร์สอื่นเป๊ะ — เรานับ "การกด" หนึ่งครั้ง ไม่ใช่นับทุกมิลลิวินาทีที่นิ้วยังกดค้างอยู่

---

# ข้อควรรู้ — Ready-Model แบบ eval มีขีดจำกัด

โมเดล Cough/Alarm/Siren เป็น DEEPCRAFT **Ready-Model** แบบ eval มีเงื่อนไขที่ต้องรู้ก่อนทดสอบ ไม่งั้นจะงงว่าทำไมผลหยุดนิ่ง

- Ready-Model แบบ eval **จำกัดจำนวนครั้งการอนุมาน** (inference count) ต่อการบูตหนึ่งครั้ง
- ถ้ารันนานๆ แล้วผลค้างนิ่ง (ตัวเลข `seq` ไม่ขยับ) นั่นแปลว่าถึงขีดจำกัดแล้ว — **รีบูตบอร์ด** จะรีเซ็ต
- นี่ไม่ใช่บั๊กในโค้ดเรา เป็นลักษณะของโมเดล eval ซึ่งเป็นของ Imagimob AB (บริษัทในเครือ Infineon) ใช้ได้เพื่อประเมินผลเท่านั้น ห้ามใช้เชิงพาณิชย์หรือแจกจ่ายต่อ

<div style="text-align:center;margin:8px 0">
<div style="display:inline-block;background:#fff3e0;border:2px solid #ef6c00;border-radius:14px;padding:8px 18px;color:#e65100;font-size:.92em">
ผลหยุดนิ่ง + seq ไม่ขยับ = ถึงขีด eval แล้ว → รีบูตบอร์ด ไม่ใช่แก้โค้ด
</div>
</div>

> จุดนี้สำคัญเชิงวิศวกรรม: โมเดลที่ "ให้ลองฟรี" มักมีเงื่อนไขซ่อนอยู่ พอเราฝึกโมเดลเองได้ (โมดูล 5 (Training) ที่เพิ่งผ่านมา) เราก็หลุดจากข้อจำกัดนี้ — นี่คือเหตุผลหนึ่งที่คอร์สพาไปถึงการเทรนเอง
