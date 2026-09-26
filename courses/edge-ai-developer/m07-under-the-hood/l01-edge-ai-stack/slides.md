---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 7.1 — สแตก Edge AI: tri-core, ai_engine, IPC model link และ TFLite-Micro"
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

# บทเรียน 7.1 — สแตก Edge AI: tri-core, ai_engine, IPC model link และ TFLite-Micro
## tri-core · ai_engine · IPC model link · TFLite-Micro

**โมดูล 7 — ใต้ฝากระโปรงและการต่อเติม**

**Researcher — อ่านสแตกจริง (เปิดสาย Researcher)**

> คาถาประจำบทเรียน: **"ทุกครั้งที่เราเรียก edge_ai.result() มันวิ่งข้ามคอร์ผ่าน IPC ไปหา NPU แล้วกลับมาเป็น dict — วันนี้เราจะชี้ได้ว่าแต่ละค่ามาจากไฟล์:บรรทัดไหน"**

MicroPython บนบอร์ด BENTO (PSoC Edge · Cortex-M55 + Ethos-U55 NPU)

---

# เปิดบทเรียนด้วยของจริงก่อน

ตลอด 17 ชุดบทเรียนที่ผ่านมาเราเรียก `edge_ai` มานับครั้งไม่ถ้วน แต่ยังไม่เคยเปิดฝากระโปรงดูว่ามันทำงานยังไง ชุดบทเรียนนี้เราจะ **แกะ** ไม่ใช่ **สร้าง** — เอาของที่เราใช้จนคล่องมากางให้เห็นทั้งเส้น

<div style="text-align:center;margin:10px 0">
<svg width="820" height="150" viewBox="0 0 820 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arOpen" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="40" width="180" height="70" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="104" y="72" font-size="15" font-weight="700" fill="#2e7d32" text-anchor="middle">รันของที่คุ้นก่อน</text>
  <text x="104" y="94" font-size="12" fill="#555" text-anchor="middle">result() ที่ใช้ทุกบทเรียน</text>
  <rect x="234" y="40" width="180" height="70" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="324" y="72" font-size="15" font-weight="700" fill="#1565c0" text-anchor="middle">แกะดูข้างใน</text>
  <text x="324" y="94" font-size="12" fill="#555" text-anchor="middle">สแตก 3 ชั้น</text>
  <rect x="454" y="40" width="180" height="70" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="544" y="72" font-size="15" font-weight="700" fill="#e65100" text-anchor="middle">ชี้ไฟล์:บรรทัด</text>
  <text x="544" y="94" font-size="12" fill="#555" text-anchor="middle">SDK: ai_engine.h</text>
  <rect x="674" y="40" width="132" height="70" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="740" y="72" font-size="15" font-weight="700" fill="#6a1b9a" text-anchor="middle">พร้อมต่อยอด</text>
  <text x="740" y="94" font-size="12" fill="#555" text-anchor="middle">7.3–7.4 เพิ่มโมเดล</text>
  <line x1="194" y1="75" x2="230" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="414" y1="75" x2="450" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="634" y1="75" x2="670" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
</svg>
</div>

ยังใช้แนว **PRIMM** เหมือนทั้งคอร์ส แต่รอบนี้ "Investigate" คือพระเอก — โค้ดที่เราเติมเป็นแค่ **เครื่องมือส่อง** ไม่ใช่แอปใหม่ ของจริงที่ต้องเข้าใจอยู่ในเฟิร์มแวร์ ซอร์สและเอกสารสถาปัตยกรรมภายในยังไม่เปิดเผย ส่วนที่เปิดคือ header ของ engine และของ IPC model link ใน [SDK สาธารณะ](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk)

> ชุดบทเรียนนี้ไม่มีอะไรใหม่ให้ท่องจำ ทุกอย่างเราแตะมาแล้วทั้งคอร์ส แค่คราวนี้เราจะ "เห็นทั้งเครื่อง" ไม่ใช่แค่ปุ่มที่กด

---

# เป้าหมายของชุดบทเรียนนี้

จบชุดบทเรียนนี้เราจะไล่สแตก Edge AI ได้ครบ 3 ชั้น แล้วชี้ต้นทางของทุกค่าที่ `edge_ai` คืนมาได้:

1. **tri-core** — PSoC Edge E84 มีสามคอร์ งาน Edge AI อยู่คอร์ไหน ทำไมต้องแบ่ง
2. **ai_engine** — เครื่องยนต์อนุมานบน CM55 กับทะเบียน `s_models[]` และคู่ index `s_active`/`s_current`
3. **IPC model link** — สะพานข้ามคอร์: control plane (สั่ง) กับ query plane (อ่าน)
4. **TFLite-Micro → NPU** — runtime จริงที่รันทั้ง int8 + float32, DEEPCRAFT เป็นแค่ wrapper
5. ลงมือ: เติม 5 คำสั่งฝั่ง **อ่าน** ของ `edge_ai` (`links` / `model` / `active` / `result` / `latency`) แล้ว trace ทั้งเส้น

ปลายทางของวันนี้: กด Trace แล้วอ่าน log สามชั้น (transport → control → result) พร้อมชี้ฟังก์ชันหรือฟิลด์ต้นทางของแต่ละชั้นใน [`ai_engine.h`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/main/bento-firmware-template-mtb-mpy/lib/edge_ai/include/ai_engine.h) กับ [`ipc_model_link_defs.h`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/main/bento-firmware-template-mtb-mpy/bento_libs/claw/common/shared/include/ipc_model_link_defs.h) ของ SDK สาธารณะ

> ชุดบทเรียนนี้เราวัดกันที่ "อธิบายได้" ไม่ใช่ "รันผ่าน" — โค้ดสั้น แต่ความเข้าใจต้องลึกถึงระดับข้ามคอร์

---

# ชุดบทเรียนนี้อยู่ตรงไหนของหลักสูตร

17 ชุดบทเรียนก่อนหน้าเราเดินครบ 5 เสาหลัก: DAQ → Processing → Analysis → Training → Apps ตอนนี้เรามีของครบมือแล้ว บทเรียน 7.1–7.2 เปิดสาย **Researcher** ด้วยการหันกลับไปมองเครื่องมือที่ใช้มาตลอด

<div style="text-align:center;margin:8px 0">
<svg width="880" height="120" viewBox="0 0 880 120" font-family="DejaVu Sans, sans-serif">
  <line x1="40" y1="60" x2="840" y2="60" stroke="#cfd8dc" stroke-width="3"/>
  <circle cx="130" cy="60" r="9" fill="#00838f"/>
  <text x="130" y="40" font-size="12" font-weight="700" fill="#00838f" text-anchor="middle">1.1–6.6</text>
  <text x="130" y="86" font-size="11" fill="#777" text-anchor="middle">ใช้ edge_ai เป็น</text>
  <circle cx="430" cy="60" r="11" fill="#6a1b9a"/>
  <text x="430" y="40" font-size="12" font-weight="700" fill="#6a1b9a" text-anchor="middle">7.1–7.2 (วันนี้)</text>
  <text x="430" y="86" font-size="11" fill="#777" text-anchor="middle">เข้าใจว่าใต้ edge_ai คืออะไร</text>
  <circle cx="700" cy="60" r="9" fill="#ef6c00"/>
  <text x="700" y="40" font-size="12" font-weight="700" fill="#e65100" text-anchor="middle">7.3–8.2</text>
  <text x="700" y="86" font-size="11" fill="#777" text-anchor="middle">เพิ่มโมเดลเอง + capstone</text>
</svg>
</div>

- **Foundation ของชุดบทเรียนนี้ = ทั้งคอร์ส** — เราจะเข้าใจสแตกได้ก็ต่อเมื่อเคยใช้มันจริงมาก่อน
- ทำไมต้องรู้ระดับนี้: ชุดบทเรียนถัดไป (บทเรียน 7.3–7.4) เราจะ **เพิ่มโมเดลของตัวเอง** ถ้าไม่รู้ว่า `s_models[]` กับ ROW macro อยู่ตรงไหน ก็เพิ่มไม่ถูกที่

> Researcher tier ไม่ใช่ "ยากขึ้น" แต่ "ลึกขึ้น" — เราเลิกเป็นผู้ใช้ API แล้วเริ่มเป็นคนที่แก้/ต่อ API ได้

---

# คำถามหลักของชุดบทเรียน — result() มาจากไหน

ลองนึกถึงบรรทัดที่เราเขียนมาตั้งแต่บทเรียน 1.1–1.3:

```python
r = edge_ai.result()      # r['label'], r['conf'], r['scores'], r['seq'] ...
```

ดูเหมือนเรียกฟังก์ชันธรรมดา แต่จริงๆ บรรทัดนี้ทำงานข้าม **สองคอร์**:

- โค้ด Python รันบน **CM33_NS** แต่โมเดลอนุมานบน **CM55** คนละคอร์กัน เรียกฟังก์ชันตรงๆ ไม่ได้
- `result()` จึงเป็นการ **pull** — ส่งคำถามข้ามคอร์ผ่าน IPC แล้วรอ CM55 เติมคำตอบกลับมา
- ค่าที่ได้มาทุก key (`label`/`conf`/`scores`/`seq`) มีต้นทางเป็นฟิลด์ใน struct ฝั่ง C ชื่อ `ai_result_t s_res`

> วันนี้เราจะเดินย้อนจาก dict ตัวนี้กลับไปให้ถึงต้นทาง: จาก Python → IPC → `ai_engine` → NPU แล้วกลับมา ทั้งวงในหนึ่งภาพ

---

# tri-core — สามสมองของ PSoC Edge E84

ชิปตัวนี้มีสาม Arm core งาน Edge AI กระจายอยู่สองคอร์ แล้วคุยกับ MicroPython บนอีกคอร์:

<div style="text-align:center;margin:6px 0">
<svg width="900" height="220" viewBox="0 0 900 220" font-family="DejaVu Sans, sans-serif">
  <rect x="20" y="14" width="860" height="58" rx="10" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
  <text x="40" y="40" font-size="14" font-weight="700" fill="#455a64">CM33_S (secure)</text>
  <text x="40" y="60" font-size="12" fill="#666">boot · TrustZone · provisioning — ไม่มีงาน Edge AI</text>
  <rect x="20" y="80" width="860" height="62" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="40" y="106" font-size="14" font-weight="700" fill="#1565c0">CM33_NS (non-secure)</text>
  <text x="40" y="126" font-size="12" fill="#555">FreeRTOS + MicroPython + เซนเซอร์ (BMI270/BMM350/DPS368/SHT40) · โมดูล edge_ai, sensors, dsp, ui</text>
  <rect x="20" y="150" width="860" height="62" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="40" y="176" font-size="14" font-weight="700" fill="#6a1b9a">CM55 (high-perf)</text>
  <text x="40" y="196" font-size="12" fill="#555">FreeRTOS + LVGL 9.2 + Ethos-U55 NPU · ai_engine · 6 โมเดล · radar task · deepcraft_task (ปลาย IPC)</text>
</svg>
</div>

- **โค้ด MicroPython ของเรา** + เซนเซอร์ IMU/audio อยู่บน **CM33_NS**
- **NPU + โมเดลหนักๆ + LVGL** อยู่บน **CM55** (คอร์เร็ว) — เรดาร์ก็ต่อ SPI ที่ CM55 เป็นข้อยกเว้น
- สองคอร์นี้แลกคำสั่งกับผลกันผ่าน IPC pipe เดียว (เดี๋ยวเจาะ)

> ทำไมต้องแยก: งานที่กินแรง (NPU, โมเดล, จอ) ไปอยู่คอร์เร็ว ส่วน REPL กับเซนเซอร์อยู่คอร์ควบคุม — แต่ละคอร์ทำสิ่งที่ตัวเองถนัด

---

# ai_engine — เครื่องยนต์อนุมานบน CM55

หัวใจของทั้งสแตกคือไฟล์ `proj_cm55/modules/ai_models/ai_engine.c` มันคุม FreeRTOS task ชื่อ `ai_task` ที่รัน **ทีละหนึ่งโมเดล** เลือกจากทะเบียน `s_models[]`

<div style="text-align:center;margin:6px 0">
<svg width="880" height="170" viewBox="0 0 880 170" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arAE" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="30" y="60" width="150" height="60" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="105" y="86" font-size="12" font-weight="700" fill="#1565c0" text-anchor="middle">s_models[]</text>
  <text x="105" y="105" font-size="11" fill="#666" text-anchor="middle">ทะเบียนโมเดล</text>
  <rect x="230" y="60" width="150" height="60" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="305" y="86" font-size="12" font-weight="700" fill="#e65100" text-anchor="middle">feed_*()</text>
  <text x="305" y="105" font-size="11" fill="#666" text-anchor="middle">เซนเซอร์ → enqueue</text>
  <rect x="430" y="60" width="150" height="60" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="505" y="82" font-size="12" font-weight="700" fill="#6a1b9a" text-anchor="middle">dequeue()</text>
  <text x="505" y="101" font-size="11" fill="#666" text-anchor="middle">NPU อนุมาน</text>
  <text x="505" y="114" font-size="10" fill="#999" text-anchor="middle">Ethos-U55</text>
  <rect x="630" y="60" width="150" height="60" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="705" y="86" font-size="12" font-weight="700" fill="#2e7d32" text-anchor="middle">publish()</text>
  <text x="705" y="105" font-size="11" fill="#666" text-anchor="middle">→ ai_result_t s_res</text>
  <line x1="180" y1="90" x2="228" y2="90" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arAE)"/>
  <line x1="380" y1="90" x2="428" y2="90" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arAE)"/>
  <line x1="580" y1="90" x2="628" y2="90" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arAE)"/>
  <text x="405" y="30" font-size="13" font-weight="700" fill="#455a64" text-anchor="middle">ai_task วนตลอด: อ่านโมเดลที่ขอ → feed → dequeue → publish</text>
  <path d="M705,120 C705,150 305,150 305,122" fill="none" stroke="#9e9e9e" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arAE)"/>
  <text x="505" y="150" font-size="11" fill="#9e9e9e" text-anchor="middle">วนรอบถัดไป</text>
</svg>
</div>

- `ai_engine` คือ **แหล่งความจริงเดียว** ว่า "ตอนนี้รันโมเดลอะไร และมันตอบว่าอะไร"
- **กฎเหล็ก**: ห้าม `finalize()` โมเดลเพื่อสลับ — เคยทำแล้ว TFLite-Micro interpreter หลุดมือ NPU จน IPC ค้างถาวร ทุกโมเดลจึง resident อยู่ตลอด สลับแค่เปลี่ยน index ที่ถูก feed

> จำคำนี้ไว้: "สลับโมเดล = เปลี่ยนว่าใครได้กินข้อมูล ไม่ใช่ปิดเปิดโมเดล" — นี่คือบทเรียนที่แลกมาด้วยการ debug หลายชั่วโมง

---

# s_active กับ s_current — ต่างกันหนึ่ง tick

`ai_engine` เก็บ index **สองตัว** ที่คนมักสับสน แต่ต่างกันสำคัญมาก:

<div style="text-align:center;margin:6px 0">
<svg width="860" height="150" viewBox="0 0 860 150" font-family="DejaVu Sans, sans-serif">
  <rect x="30" y="30" width="360" height="90" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="210" y="56" font-size="14" font-weight="700" fill="#e65100" text-anchor="middle">s_active = โมเดลที่ "ขอ"</text>
  <text x="210" y="80" font-size="12" fill="#555" text-anchor="middle">ตั้งทันทีที่ ai_engine_start()</text>
  <text x="210" y="100" font-size="11" fill="#888" text-anchor="middle">อ่านด้วย ai_engine_requested()</text>
  <rect x="470" y="30" width="360" height="90" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="650" y="56" font-size="14" font-weight="700" fill="#2e7d32" text-anchor="middle">s_current = โมเดลที่ "สลับจริง"</text>
  <text x="650" y="80" font-size="12" fill="#555" text-anchor="middle">task ตามมาช้ากว่าได้ถึง 1 tick</text>
  <text x="650" y="100" font-size="11" fill="#888" text-anchor="middle">อ่านด้วย ai_engine_active()  →  edge_ai.active()</text>
</svg>
</div>

- `edge_ai.active()` คืน **s_current** (โมเดลที่สลับไปแล้วจริง) ไม่ใช่ตัวที่เพิ่งขอ
- ถ้าอ่าน `active()` ทันทีหลังสั่ง select อาจได้ค่าเก่า เพราะ task ยังตามไม่ทัน
- เอกสารเตือน: guard ค่า default ให้ดู `requested()` (`s_active`) ไม่ใช่ `active()` — ไม่งั้นทับ selection ใหม่โดยไม่ตั้งใจ

> นี่คือ "gotcha" อันดับหนึ่งของสแตกนี้ ในสคริปต์ฝึกเราจะเรียก `active()` หลัง `select()` เพื่อ **เห็นกับตา** ว่ามันสลับจริงหรือยัง

---

# model descriptor + ROW macro

แต่ละแถวใน `s_models[]` เป็น struct `ai_model_desc_t` ประกาศด้วย ROW macro ที่มี guard `EDGE_AI_MODEL_<name>` — โมเดลจะคอมไพล์เข้ามาก็ต่อเมื่อ Makefile ขอ:

```c
#define MOTION_ROW { .name = "Motion Detection", \
    .sensor = AI_SENSOR_IMU, .class_count = 3, \
    .class_labels = { "idle", "circle", "shaking" }, \
    .flash_bytes = 28272u, .period_ms = 200u, \
    .init = AIM_MOTION_init, .enqueue = AIM_MOTION_enqueue, \
    .dequeue = AIM_MOTION_dequeue, .finalize = AIM_MOTION_finalize }
```

- ทุกฟิลด์ที่ `edge_ai.models()` คืนมา (`name`/`sensor`/`labels`) มาจาก ROW นี้ตรงๆ
- ทะเบียน (และเมนูใน MicroPython) ถูกประกอบ **ทั้งหมด** จากสิ่งที่ Makefile เลือก — ไม่มี hard-code ฝั่ง Python
- ทุกโมเดลต้องให้ 4 ฟังก์ชันตรง contract: `init` / `enqueue` / `dequeue` / `finalize`

> นี่คือจุดที่ชุดบทเรียนถัดไป (บทเรียน 7.3–7.4) เราจะแตะ — เพิ่มโมเดล = เพิ่ม ROW หนึ่งแถว + define ใน Makefile + ไฟล์โมเดล วันนี้แค่รู้จักหน้าตามันก่อน

---

# feed functions — เซนเซอร์เข้าโมเดลยังไง

`ai_task` ดูว่าโมเดลปัจจุบันใช้เซนเซอร์อะไร แล้วเรียก feed function ให้ตรงชนิด:

| เซนเซอร์ | feed fn | ทำอะไร |
|---|---|---|
| `AI_SENSOR_IMU` | `feed_imu()` | ดึง snapshot BMI270 ผ่าน IPC, remap แกน (`-X,-Y,Z`), แปลง counts → g/dps, `enqueue()` ต่อ sequence ใหม่ |
| `AI_SENSOR_RADAR` | `feed_radar()` | ดูด chirp int16 128 sample จาก ring, cast ADC → float (ไม่ scale), `enqueue()` ต่อ chirp |
| `AI_SENSOR_MIC` | `feed_audio()` | เริ่ม PDM mic, normalize int16 → `[-1,1]`, วน enqueue+dequeue+publish ต่อ sample |

- feed function คือที่อยู่ของ **signal front-end ฝั่ง C** — โมเดลเสียงมี FFT/mel front-end รันก่อนกราฟตรงนี้
- นี่ตอบคำถามคอร์ส "โมเดลเห็นอะไรจริงๆ" — สิ่งที่เข้ากราฟไม่ใช่ raw เซนเซอร์ แต่ผ่าน feed แปลงแล้ว

> ถ้าอยากทำ feature เดียวกันซ้ำนอกบอร์ด (เช่นตอน train) ต้องเลียนแบบ feed function นี้ให้เป๊ะ — นี่คือสะพานเชื่อม โมดูล 4 (Analysis) กับโมดูล 5 (Training) ที่เราเดินมา

---

# publish() — เขียนผลแบบ lock-free

เมื่อ `dequeue()` ได้ verdict `publish()` เขียนลง global `ai_result_t s_res` **โดยไม่ล็อก**:

```c
typedef struct {
    uint8_t  model_index, class_count, top_class, running;
    float    scores[AI_MAX_CLASSES];
    uint32_t inference_us, inference_us_max, inferences, seq;
} ai_result_t;
```

- ออกแบบเป็น **single-writer, tolerated-torn-read** — ปิด interrupt รอบ `publish()` เสี่ยงหน่วง completion IRQ ของ Ethos-U55
- ผู้อ่าน (หน้าจอ 30 Hz + MicroPython ผ่าน IPC) ยอมรับ "หนึ่งเฟรมเก่า" แลกกับความเร็ว
- `seq` เพิ่มทุกครั้งที่ publish — เราใช้มันเช็ก "มีผลใหม่ไหม" (นี่คือ `r['seq']` ที่เราเช็กในลูปทุกบทเรียน)

> ทุก key ใน dict ที่ `result()` คืน map ตรงกับฟิลด์ใน struct นี้ — `scores`→`scores`, `seq`→`seq`, `latency_ms`→`inference_us/1000`, `top`→`top_class`

---

# 6 โมเดลที่ shipped มา — int8 อยู่กับ float32

build แบบ `combo` รวม 6 โมเดลในภาพเดียว สลับได้ตอนรัน:

| โมเดล | เซนเซอร์ | ชนิด | ที่มา |
|---|---|---|---|
| Motion Detection | IMU | int8 | source-gen `model_motion.c` |
| Baby Cry Detection | MIC | int8 | source-gen `model_audio.c` |
| Push Detection | RADAR | float32 | source-gen `model_radar.c` |
| Cough Detection | MIC | int8 | ready-model `cough_lib_eval.a` |
| Alarm Detection | MIC | int8 | ready-model `alarm_lib_eval.a` |
| Siren Detection | MIC | float32 | ready-model `siren_lib_eval.a` |

- **source-generated** — C ที่ DEEPCRAFT ImagiNet compiler สร้าง เปิด API `AIM_<NAME>_*`
- **ready-model .a** — ไลบรารี eval ของ Infineon ทุกตัว export `IMAI_*` ไม่ prefix → ชนกัน ต้อง `objcopy` rename เป็น `IMAI_<MODEL>_*` ให้อยู่ร่วมกันได้

> สังเกตว่า int8 (Motion/Cough) กับ float32 (Push/Siren) อยู่ในภาพเดียวกันได้ — คำถามคือมันรันร่วมกันได้ยังไง? หน้าถัดไปตอบ

---

# TFLite-Micro — runtime จริง (DEEPCRAFT เป็นแค่ wrapper)

จุดที่คนเข้าใจผิดบ่อย: **DEEPCRAFT ไม่ใช่ runtime** มันเป็นแค่เปลือกที่ห่อกราฟ `.tflite` ไว้:

<div style="text-align:center;margin:6px 0">
<svg width="880" height="150" viewBox="0 0 880 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arTF" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="30" y="45" width="200" height="60" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="130" y="70" font-size="12" font-weight="700" fill="#6a1b9a" text-anchor="middle">DEEPCRAFT wrapper</text>
  <text x="130" y="90" font-size="11" fill="#666" text-anchor="middle">AIM_*/IMAI_* 4 ฟังก์ชัน</text>
  <rect x="300" y="45" width="240" height="60" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="420" y="70" font-size="12" font-weight="700" fill="#1565c0" text-anchor="middle">TFLite-Micro (runtime จริง)</text>
  <text x="420" y="90" font-size="11" fill="#666" text-anchor="middle">libtensorflow-microlite.a</text>
  <rect x="610" y="45" width="240" height="60" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="730" y="70" font-size="12" font-weight="700" fill="#2e7d32" text-anchor="middle">kernel: int8 + float32</text>
  <text x="730" y="90" font-size="11" fill="#666" text-anchor="middle">int8 → NPU · float → CPU</text>
  <line x1="230" y1="75" x2="298" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arTF)"/>
  <line x1="540" y1="75" x2="608" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arTF)"/>
  <text x="440" y="28" font-size="12" fill="#455a64" text-anchor="middle">บอร์ดไม่เคย "เห็น" DEEPCRAFT — มันเรียกแค่ 4 ฟังก์ชัน init/enqueue/dequeue/finalize</text>
</svg>
</div>

- prebuilt `libtensorflow-microlite.a` พก kernel **ทั้ง int8 และ float32** มาในตัว
- โมเดลไหนก็ตามที่ให้ 4-ฟังก์ชัน contract เดียวกัน (รวมทั้งที่เราเทรนเองแล้วแปลงเป็น `.tflite`) เสียบเข้าได้
- นี่คือเหตุผลว่าทำไมบทเรียน Training (บทเรียน 5.3–5.5) เราถึง train เองแล้วเอาลงบอร์ดได้ — contract เดียวกัน

> "DEEPCRAFT = wrapper, TFLite-Micro = runtime" — จำประโยคนี้ไว้ เพราะมันปลดล็อกความคิดว่า "เราเทรนโมเดลเองแล้วเสียบแทนได้"

---

# int8 + float32 ในภาพเดียว รันร่วมกันยังไง

คำถามค้างจากเมื่อกี้: ทำไม radar/siren (float32) รันในภาพ int8 `combo` ได้?

- `COMPONENT_ML_INT8x8` / `ML_FLOAT32` แค่ตั้ง typedef ตัวชี้ `MTB_ML_DATA_T` — ไม่ได้ตัดสินว่ารันด้วย kernel ไหน
- เส้นทางรันจริงเป็น **runtime-typed**: copy input เป็น byte ดิบ แล้ว switch ตามขนาด output type
- เพราะ TFLite-Micro พก kernel ครบสองชุด → โมเดล float32 รันบน CPU float kernel ได้ ส่วนโมเดล int8 ใช้ U55 NPU — **ไม่ต้อง build แยก**

<div style="text-align:center;margin:6px 0">
<svg width="820" height="96" viewBox="0 0 820 96" font-family="DejaVu Sans, sans-serif">
  <rect x="30" y="24" width="360" height="52" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="210" y="46" font-size="12" font-weight="700" fill="#1565c0" text-anchor="middle">โมเดล int8 (Motion/Cough/Alarm)</text>
  <text x="210" y="65" font-size="11" fill="#666" text-anchor="middle">→ Ethos-U55 NPU (เร็ว ประหยัดไฟ)</text>
  <rect x="430" y="24" width="360" height="52" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="610" y="46" font-size="12" font-weight="700" fill="#e65100" text-anchor="middle">โมเดล float32 (Push/Siren)</text>
  <text x="610" y="65" font-size="11" fill="#666" text-anchor="middle">→ CPU float kernel (ในภาพเดียวกัน)</text>
</svg>
</div>

> ตอน Trace ในสคริปต์ ลองเทียบ `latency()` ของโมเดล int8 กับ float32 — จะเห็นเลยว่า NPU กับ CPU ต่างกันจริง

---

# .tflite → NPU + กำแพง .ml_weights

โมเดล `.tflite` int8 ไปรันบน NPU ได้ต้องผ่านขั้นคอมไพล์ **Vela** ก่อน แปลงให้ Ethos-U55 อ่านออก แล้ว weights ต้องหาที่อยู่ในแฟลช:

- ปกติ weights ลงที่ `.cy_socmem_data` แต่ในภาพ `combo` weights 6 โมเดล + FFT table จะล้นกำแพง `.fw_identity` ที่ `0x60900000`
- ทางแก้: `CY_ML_MODEL_MEM=.ml_weights` ย้าย weights ไปโหลดที่หาง flash ~2.5 MB เหนือกำแพง แล้ว copy ลง SOCMEM ตอน boot (ให้ NPU DMA เอื้อมถึง)
- เรื่องนี้ mechanical — แตะเฉพาะตอนเพิ่มโมเดลใหญ่ (บทเรียน 7.3–7.4)

> จำ address `0x60900000` ไว้ — มันคือ "กำแพง" ที่เราเคยเจอในบันทึกโปรเจกต์จริง ตอน combo image เกือบล้น นี่ไม่ใช่ทฤษฎี เป็นของจริงบนบอร์ดนี้

---

# IPC model link — สะพานข้ามคอร์

MicroPython บน CM33_NS เรียก `ai_engine` บน CM55 ตรงๆ ไม่ได้ ทั้งคู่แลกข้อความขนาดคงที่ผ่าน IPC pipe เดียว มี **สอง plane**:

<div style="text-align:center;margin:6px 0">
<svg width="880" height="180" viewBox="0 0 880 180" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arIP" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="30" y="50" width="200" height="80" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="130" y="82" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">CM33_NS</text>
  <text x="130" y="104" font-size="11" fill="#666" text-anchor="middle">edge_ai (MicroPython)</text>
  <rect x="650" y="50" width="200" height="80" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="750" y="82" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">CM55</text>
  <text x="750" y="104" font-size="11" fill="#666" text-anchor="middle">deepcraft_task → ai_engine</text>
  <line x1="230" y1="76" x2="648" y2="76" stroke="#ef6c00" stroke-width="2.4" marker-end="url(#arIP)"/>
  <text x="440" y="68" font-size="12" font-weight="700" fill="#ef6c00" text-anchor="middle">control plane: SELECT / START / STOP (fire-and-forget)</text>
  <line x1="648" y1="108" x2="230" y2="108" stroke="#2e7d32" stroke-width="2.4" marker-end="url(#arIP)"/>
  <text x="440" y="126" font-size="12" font-weight="700" fill="#2e7d32" text-anchor="middle">query plane: Q_COUNT / Q_MODEL / Q_RESULT / Q_ACTIVE (pull)</text>
  <text x="440" y="158" font-size="11" fill="#999" text-anchor="middle">callback บน CM55 รันใน ISR: ตอบ query ในที่ · ห้าม send จาก callback (เคยทำ pipe ค้าง)</text>
</svg>
</div>

- **control plane** (`OP_CTRL`) — สั่ง: `SELECT(n)=0x90+n`, `START=0x82`, `STOP=0x83` แบบยิงแล้วไม่รอ
- **query plane** (`OP_QUERY`) — อ่านแบบ pull: CM33 วางตัวชี้ struct แล้ว block รอ CM55 เติม

> ข้อจำกัดที่ต้องรู้: control plane เป็น best-effort ใช้ pipe ร่วม ถ้า flood `select()` รัวๆ pipe ค้างได้ (กู้ด้วย core reset เท่านั้น) — ใน REPL ให้เว้นการสลับโมเดลเป็นวินาที

---

# confirmed by observation — ทำไม select ต้องรอ

การออกแบบที่สำคัญที่สุดของ IPC นี้: **อ่านเป็น pull ที่ตอบรับ · สั่งเป็นการยืนยันด้วยการสังเกต**

```python
edge_ai.select(n)   # 1) ส่ง SELECT(0x90+n) ผ่าน control plane
                    # 2) poll Q_ACTIVE จนอ่านกลับได้ = n (สูงสุด 25 × 20 ms)
                    #    ถ้าไม่สลับในเวลา -> OSError "select not confirmed"
```

- ไม่มี push ที่ไม่ถูกตอบรับ ซึ่งอาจแอบทำ pipe ค้างเงียบๆ
- `select()` ไม่เชื่อว่า "สั่งแล้วสำเร็จ" แต่รอ **เห็น** `active()` เปลี่ยนเป็น `n` จริง
- นี่คือเหตุผลที่เราห่อ `select()` ด้วย `try/except OSError` เสมอ

> ในสคริปต์ฝึก เราจะเรียก `active()` ต่อจาก `select()` ทันที เพื่อ **เห็นกับตา** ว่ากลไก confirm-by-observation นี้ทำงาน — index ที่ได้ต้องตรงกับที่ขอ

---

# edge_ai — API ฝั่ง "อ่าน" ที่ชุดบทเรียนนี้ใช้

ชุดบทเรียนก่อน ๆ เราเน้นฝั่ง "สั่ง" (`select`/`stop`) ชุดบทเรียนนี้เราส่องด้วยฝั่ง "อ่าน" 5 ตัว แต่ละตัว map ไป query sub-plane:

| คำสั่ง | คืนค่า | map ไป |
|---|---|---|
| `edge_ai.links()` | `('ipc',)` — link backend | IPC model link (deepcraft_task.c) |
| `edge_ai.model(n)` | dict descriptor หนึ่งตัว | `Q_MODEL` → `ai_engine_model(i)` |
| `edge_ai.active()` | index ที่รันอยู่ (`-1` ถ้า idle) | `Q_ACTIVE` → `s_current` |
| `edge_ai.result()` | dict verdict ล่าสุด หรือ `None` | `Q_RESULT` → `ai_result_t s_res` |
| `edge_ai.latency()` | เวลาอนุมานล่าสุด (ms) | `s_res.inference_us / 1000` |

- ทั้งห้าตัวเป็น **pull** ทั้งหมด — ถามเมื่อไรก็ได้ ไม่บล็อกรอผลใหม่ (แค่บล็อกรอ CM55 ตอบ query)
- `on_result(cb)` เป็นทางเลือกแบบ event-driven — เฟิร์มแวร์เรียก callback ตอนคลาสเปลี่ยน (เราใช้ในฉบับเต็ม)

> โฟกัสห้าตัว: **links → model → active → result → latency** ห้าตัวนี้คือทั้งเรื่องราวของสคริปต์ส่องสแตกชุดบทเรียนนี้

---

# ทั้งเส้นในภาพเดียว — sensor ถึง dict

รวมทุกอย่างเข้าด้วยกัน นี่คือเส้นทางของ **หนึ่งการอนุมาน** ตั้งแต่เซนเซอร์จนเป็น dict ใน Python:

<div style="text-align:center;margin:6px 0">
<svg width="900" height="230" viewBox="0 0 900 230" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arE2" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="30" y="14" width="220" height="46" rx="9" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="140" y="34" font-size="12" font-weight="700" fill="#1565c0" text-anchor="middle">BMI270 (CM33_NS)</text>
  <text x="140" y="52" font-size="10" fill="#666" text-anchor="middle">I2C read + sequence number</text>
  <rect x="30" y="90" width="220" height="46" rx="9" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="140" y="110" font-size="12" font-weight="700" fill="#e65100" text-anchor="middle">feed_imu() (CM55)</text>
  <text x="140" y="128" font-size="10" fill="#666" text-anchor="middle">remap แกน · counts→g/dps</text>
  <rect x="30" y="166" width="220" height="46" rx="9" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="140" y="186" font-size="12" font-weight="700" fill="#6a1b9a" text-anchor="middle">enqueue → dequeue</text>
  <text x="140" y="204" font-size="10" fill="#666" text-anchor="middle">Ethos-U55 NPU (int8)</text>
  <rect x="340" y="90" width="220" height="46" rx="9" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="450" y="110" font-size="12" font-weight="700" fill="#2e7d32" text-anchor="middle">publish() → s_res</text>
  <text x="450" y="128" font-size="10" fill="#666" text-anchor="middle">lock-free · seq++</text>
  <rect x="640" y="42" width="230" height="46" rx="9" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
  <text x="755" y="62" font-size="12" font-weight="700" fill="#455a64" text-anchor="middle">page_edge_ai (CM55)</text>
  <text x="755" y="80" font-size="10" fill="#666" text-anchor="middle">วาด verdict + bars 30 Hz</text>
  <rect x="640" y="138" width="230" height="60" rx="9" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="755" y="160" font-size="12" font-weight="700" fill="#1565c0" text-anchor="middle">Q_RESULT pull (CM33_NS)</text>
  <text x="755" y="178" font-size="10" fill="#666" text-anchor="middle">edge_ai.result() → dict</text>
  <text x="755" y="192" font-size="10" fill="#999" text-anchor="middle">แอป MicroPython ของเรา</text>
  <line x1="140" y1="60" x2="140" y2="88" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arE2)"/>
  <line x1="140" y1="136" x2="140" y2="164" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arE2)"/>
  <line x1="250" y1="188" x2="450" y2="138" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arE2)"/>
  <line x1="560" y1="104" x2="638" y2="80" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arE2)"/>
  <line x1="560" y1="120" x2="638" y2="160" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arE2)"/>
</svg>
</div>

> ทั้งหมดคือ "sample เซนเซอร์บนคอร์หนึ่ง กลายเป็น Python dict บนอีกคอร์ ผ่านผล lock-free กับ IPC pull" — ที่เหลือในสแตกเป็นแค่รายละเอียดรอบการทำให้เส้นนี้เร็ว สลับได้ ปลอดภัย

---

# แผนภาพ dataflow — 6 ป้ายที่ต้องอ่านออก

สแตกนี้ไม่มีสมการให้ท่อง มันเป็น **เส้นทางข้อมูลหกป้าย** ที่ไหลจากซ้ายไปขวาหนึ่งรอบต่อหนึ่งการอนุมาน อ่านป้ายให้ออก แล้วคุณ trace ได้ทั้งเส้น:

<div style="text-align:center;margin:4px 0">
<svg width="900" height="150" viewBox="0 0 900 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arDF" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <text x="450" y="26" font-size="12" font-weight="700" fill="#455a64" text-anchor="middle">หนึ่งการอนุมาน = ไหลซ้าย → ขวา ครบหนึ่งรอบ</text>
  <rect x="8" y="48" width="128" height="56" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="72" y="72" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">sensor</text>
  <text x="72" y="91" font-size="10" fill="#666" text-anchor="middle">IMU/MIC/RADAR</text>
  <rect x="156" y="48" width="120" height="56" rx="10" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
  <text x="216" y="72" font-size="13" font-weight="700" fill="#455a64" text-anchor="middle">IPC</text>
  <text x="216" y="91" font-size="10" fill="#666" text-anchor="middle">ข้ามคอร์</text>
  <rect x="296" y="48" width="120" height="56" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="356" y="72" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">feed_*()</text>
  <text x="356" y="91" font-size="10" fill="#666" text-anchor="middle">แปลง signal</text>
  <rect x="436" y="48" width="140" height="56" rx="10" fill="#ede7f6" stroke="#5e35b1" stroke-width="2"/>
  <text x="506" y="72" font-size="12" font-weight="700" fill="#5e35b1" text-anchor="middle">enqueue → dequeue</text>
  <text x="506" y="91" font-size="10" fill="#666" text-anchor="middle">คิวเข้า/ออกกราฟ</text>
  <rect x="596" y="48" width="120" height="56" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="656" y="72" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">NPU</text>
  <text x="656" y="91" font-size="10" fill="#666" text-anchor="middle">Ethos-U55</text>
  <rect x="736" y="48" width="128" height="56" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="800" y="72" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">publish()</text>
  <text x="800" y="91" font-size="10" fill="#666" text-anchor="middle">s_res · seq++</text>
  <line x1="136" y1="76" x2="154" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arDF)"/>
  <line x1="276" y1="76" x2="294" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arDF)"/>
  <line x1="416" y1="76" x2="434" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arDF)"/>
  <line x1="576" y1="76" x2="594" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arDF)"/>
  <line x1="716" y1="76" x2="734" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arDF)"/>
</svg>
</div>

อ่านแต่ละป้ายเป็นภาษาคน แล้วโยงว่าทำไมมันสำคัญกับชุดบทเรียนนี้:

| ป้าย | อ่านว่าอะไร | ทำไมสำคัญกับชุดบทเรียนนี้ |
|---|---|---|
| `sensor` | เซนเซอร์ดิบบน CM33_NS (IMU/MIC/RADAR) | ต้นทางของทุกค่า — sample แรกก่อนข้ามคอร์ |
| `IPC` | สะพานข้ามคอร์ CM33_NS ↔ CM55 | ชั้น **transport** ที่ `links()` ชี้ให้เห็น |
| `feed_*()` | แปลง raw → feature ที่กราฟกิน | ตอบคำถาม "โมเดลเห็นอะไรจริง ๆ" |
| `enqueue → dequeue` | ป้อนเข้าคิว แล้วดึงออกให้ NPU | จุดที่ "สลับโมเดล = เปลี่ยนว่าใครได้ feed" |
| `NPU` | Ethos-U55 อนุมาน int8 (float ไป CPU) | ที่มาของ `latency()` int8 vs float32 |
| `publish()` | เขียนผลลง `s_res` แบบ lock-free + `seq++` | ปลายทางของ `result()` ทุก key |

> ไม่มีสูตรให้จำ มีแค่หกป้าย — trace เก่งคือ "เห็นค่าปุ๊บ บอกได้ทันทีว่ามันอยู่ป้ายไหนของเส้นนี้"
