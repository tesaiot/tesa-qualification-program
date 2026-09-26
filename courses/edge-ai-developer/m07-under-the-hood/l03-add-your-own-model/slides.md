---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 7.3 — เพิ่มโมเดลของเราเอง: สามการแก้ สัญญาสี่ฟังก์ชัน และ Vela"
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

# บทเรียน 7.3 — เพิ่มโมเดลของเราเอง: สามการแก้ สัญญาสี่ฟังก์ชัน และ Vela
## เพิ่มโมเดลของเราเองเข้าเฟิร์มแวร์

**โมดูล 7 — ใต้ฝากระโปรงและการต่อเติม**

**โมดูล 7–8 · Researcher — ลงไปแก้เครื่องยนต์เอง**

> คาถาประจำบทเรียน: **"การเพิ่มโมเดลใหม่ให้บอร์ดรู้จัก ใช้แค่ 3 การแก้ — Makefile หนึ่งบรรทัด, C ROW หนึ่งก้อน, ไฟล์โมเดลหนึ่งไฟล์ แล้วมันจะโผล่ใน edge_ai.models() เอง"**

MicroPython + C บนบอร์ด BENTO (PSoC Edge · Cortex-M55 + Ethos-U55 NPU)

---

# เปิดบทเรียนด้วยของจริงก่อน

ทั้งคอร์สเราเรียก `edge_ai.models()` แล้วได้ตาราง 6 โมเดลกลับมา วันนี้เรากลับด้านอีกครั้ง — ไม่ถามว่า "มีโมเดลอะไร" แต่ถามว่า **"ทำยังไงโมเดลถึงโผล่ในตารางนั้น"** แล้วลงมือเพิ่มตัวที่ 7 ด้วยมือเราเอง

<div style="text-align:center;margin:10px 0">
<svg width="820" height="150" viewBox="0 0 820 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arOpen" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="40" width="180" height="70" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="104" y="72" font-size="15" font-weight="700" fill="#2e7d32" text-anchor="middle">โมเดลที่มีอยู่</text>
  <text x="104" y="94" font-size="12" fill="#555" text-anchor="middle">6 ตัวในทะเบียน</text>
  <rect x="234" y="40" width="180" height="70" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="324" y="72" font-size="15" font-weight="700" fill="#1565c0" text-anchor="middle">แกะทะเบียน</text>
  <text x="324" y="94" font-size="12" fill="#555" text-anchor="middle">ROW เข้ามายังไง</text>
  <rect x="454" y="40" width="180" height="70" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="544" y="72" font-size="15" font-weight="700" fill="#e65100" text-anchor="middle">เพิ่มของเรา</text>
  <text x="544" y="94" font-size="12" fill="#555" text-anchor="middle">3 การแก้</text>
  <rect x="674" y="40" width="132" height="70" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="740" y="72" font-size="15" font-weight="700" fill="#6a1b9a" text-anchor="middle">โผล่ในเมนู</text>
  <text x="740" y="94" font-size="12" fill="#555" text-anchor="middle">models() +1</text>
  <line x1="194" y1="75" x2="230" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="414" y1="75" x2="450" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="634" y1="75" x2="670" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
</svg>
</div>

น่าสนใจตรงที่เฟิร์มแวร์จริง **มีสล็อตของโมเดลตัวที่ 7 รออยู่แล้ว** — `FALL_ROW`, `GESTURE_ROW`, `KEYWORD_ROW` ถูกเขียนไว้เป็นคอมเมนต์ในซอร์ส เป็นตัวอย่างที่พร้อมปลุกให้ทำงาน เราจะเริ่มจากตรงนั้น

> ชุดบทเรียนนี้เป็นสาย Researcher — เราไม่ได้แค่เรียก API แล้ว วันนี้เราเปิดฝากระโปรง เพิ่มโมเดลเข้าเครื่องยนต์เอง แล้วยืนยันว่ามันโผล่จริง

---

# เป้าหมายของชุดบทเรียนนี้

จบชุดบทเรียนนี้เราจะเดินครบ แล้วปิดท้ายด้วยโมเดลของเราเองรันบนบอร์ด:

1. **"3 การแก้"** ที่ทำให้โมเดลใหม่โผล่ในทะเบียน (Makefile · C ROW · ไฟล์โมเดล)
2. **สัญญา 4 ฟังก์ชัน** ที่ทุกโมเดลต้องมี — `init` / `enqueue` / `dequeue` / `finalize`
3. **AIM_ vs IMAI_** — สองทางได้โมเดลมา (gen จาก DEEPCRAFT vs ready-model `.a`)
4. **feed** คืออะไร ทำไมโมเดลที่ใช้เซนเซอร์เดิม **ไม่ต้องเขียน feed ใหม่**
5. **Vela** — ทำไม MCU ต้องคอมไพล์เพิ่มก่อนโมเดลรันบน NPU ได้
6. ลงมือ: เพิ่ม **Fall Detection** ครบ 3 การแก้ แล้วยืนยันด้วย `edge_ai.count()` / `models()`

ปลายทางของวันนี้: โมเดลตัวที่ 7 (`Fall Detection`) โผล่ใน `edge_ai.models()` เลือกรันแล้วอ่าน verdict ได้จริง

> วันนี้เราแตะ **C จริง** เป็นครั้งแรกของคอร์ส แต่ไม่ต้องเขียนโมเดลเอง — เราแค่ "ต่อสาย" โมเดลที่มีอยู่เข้าทะเบียน แล้วให้ MicroPython มองเห็น

---

# ย้อนดู: โมเดลโผล่ใน models() ได้ยังไง (จาก บทเรียน 7.1–7.2)

ชุดบทเรียนก่อนหน้า (บทเรียน 7.1–7.2) เราไล่ stack จากปลายถึงต้น วันนี้เราสนใจแค่ท่อนบน: **จาก `edge_ai.models()` ลงไปถึง `s_models[]`**

<div style="text-align:center;margin:6px 0">
<svg width="900" height="200" viewBox="0 0 900 200" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arST" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="30" width="200" height="56" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="120" y="54" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">edge_ai.models()</text>
  <text x="120" y="74" font-size="11" fill="#666" text-anchor="middle">MicroPython · CM33</text>
  <rect x="20" y="114" width="200" height="56" rx="10" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
  <text x="120" y="138" font-size="13" font-weight="700" fill="#455a64" text-anchor="middle">IPC model-link</text>
  <text x="120" y="158" font-size="11" fill="#666" text-anchor="middle">Q_COUNT / Q_MODEL</text>
  <rect x="360" y="72" width="220" height="56" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="470" y="96" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">ai_engine (CM55)</text>
  <text x="470" y="116" font-size="11" fill="#666" text-anchor="middle">อ่านจาก s_models[]</text>
  <rect x="660" y="72" width="220" height="56" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="770" y="92" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">s_models[]</text>
  <text x="770" y="110" font-size="11" fill="#666" text-anchor="middle">ทะเบียน ROW ต่อกัน</text>
  <text x="770" y="124" font-size="10" fill="#999" text-anchor="middle">เราเติมที่นี่วันนี้</text>
  <line x1="120" y1="86" x2="120" y2="112" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arST)"/>
  <line x1="220" y1="140" x2="358" y2="108" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arST)"/>
  <line x1="580" y1="100" x2="658" y2="100" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arST)"/>
  <text x="450" y="176" font-size="12" fill="#888" text-anchor="middle">ทั้งสายอ่านจาก s_models[] — เพิ่ม ROW ที่ปลายทาง ทั้งสายเห็นเอง</text>
</svg>
</div>

> จุดสำคัญ: MicroPython **ไม่ได้ hard-code** ชื่อโมเดลไว้เลย มันถามลงไปที่ `s_models[]` ทุกครั้ง เพราะงั้นเราแก้ที่ `s_models[]` ที่เดียว ทั้งสาย (IPC + Python + จอ) ปรับตามเอง

---

# หัวใจของชุดบทเรียน — เพิ่มโมเดล = "3 การแก้" เท่านั้น

เอกสารภายในของเฟิร์มแวร์สรุปการเพิ่มโมเดลไว้สั้นมาก มีแค่สามที่ที่ต้องแตะ (ต้องมีซอร์สเฟิร์มแวร์ตัวเต็มซึ่งยังไม่เปิดเผย ใน [SDK สาธารณะ](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) `ai_engine` มาเป็นไลบรารี prebuilt จึงเพิ่มแถวใหม่ด้วย `ai_engine_register()` ตอนรัน ใส่โมเดลแทนช่องเดิม หรือโหลดโมเดล IMU แบบ staged ตาม `ai_model_staged.h` แทน Edit 2):

<div style="text-align:center;margin:6px 0">
<svg width="920" height="200" viewBox="0 0 920 200" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="ar3E" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="50" width="270" height="100" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="155" y="80" font-size="15" font-weight="700" fill="#1565c0" text-anchor="middle">Edit 1 · Makefile</text>
  <text x="155" y="104" font-size="12" fill="#555" text-anchor="middle">เติมชื่อใน AI_MODELS</text>
  <text x="155" y="124" font-size="11" fill="#888" text-anchor="middle">หนึ่งคำ</text>
  <rect x="325" y="50" width="270" height="100" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="460" y="80" font-size="15" font-weight="700" fill="#e65100" text-anchor="middle">Edit 2 · ai_engine.c</text>
  <text x="460" y="104" font-size="12" fill="#555" text-anchor="middle">เพิ่ม ROW + ต่อ s_models[]</text>
  <text x="460" y="124" font-size="11" fill="#888" text-anchor="middle">หนึ่งก้อน C</text>
  <rect x="630" y="50" width="270" height="100" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="765" y="80" font-size="15" font-weight="700" fill="#6a1b9a" text-anchor="middle">Edit 3 · ไฟล์โมเดล</text>
  <text x="765" y="104" font-size="12" fill="#555" text-anchor="middle">model_x.c/.h หรือ .a</text>
  <text x="765" y="124" font-size="11" fill="#888" text-anchor="middle">วางลงโฟลเดอร์</text>
  <line x1="290" y1="100" x2="323" y2="100" stroke="#607d8b" stroke-width="2.4" marker-end="url(#ar3E)"/>
  <line x1="595" y1="100" x2="628" y2="100" stroke="#607d8b" stroke-width="2.4" marker-end="url(#ar3E)"/>
  <text x="460" y="180" font-size="12" fill="#888" text-anchor="middle">แล้ว build+flash — ไม่ต้องแตะ MicroPython หรือ IPC เลย</text>
</svg>
</div>

> สังเกตว่า **ไม่มี "Edit 4: แก้ MicroPython"** — นั่นคือความงามของ shape-driven registry ที่เราจะอธิบายหน้าถัดไป

---

# ทำไมแค่ 3 การแก้ถึงพอ — shape-driven

โค้ด MicroPython (`modedgeai.c`) กับ IPC model-link **ไม่รู้จักชื่อโมเดลใดๆ เลย** มันแค่ส่งต่อ "รูปร่าง" ที่ `s_models[]` บอก:

- ถาม `count()` → ตอบ `sizeof(s_models)/sizeof(...)` — เพิ่ม ROW หนึ่งตัว เลขนี้ขึ้นเอง
- ถาม `model(n)` → คัดลอก `s_models[n].name / sensor / class_labels` ส่งกลับ — ไม่มีชื่อไหน hard-code
- `select(n)` → บอก `ai_task` ให้เรียก `s_models[n].init/enqueue/dequeue` — ผูกด้วย pointer ไม่ใช่ชื่อ

```c
// registry เป็นแค่ array ของ descriptor — เพิ่มสมาชิกก็พอ
static const ai_model_desc_t s_models[] = {
    MOTION_ROW AUDIO_ROW RADAR_ROW COUGH_ROW ALARM_ROW SIREN_ROW
    FALL_ROW          // <- เติมของเราตรงนี้ ทั้งสายเห็นเอง
};
#define MODEL_COUNT ((uint32_t)(sizeof(s_models)/sizeof(s_models[0])))
```

> นี่คือบทเรียนออกแบบซอฟต์แวร์ที่ใช้ได้ทุกที่: **ให้ข้อมูล (data) ขับพฤติกรรม อย่าให้ชื่อ (name) ขับ** พอทะเบียนเป็น data ล้วน การเพิ่มของใหม่ก็แค่เพิ่มแถวข้อมูล ไม่ต้องไล่แก้โค้ดหลายที่

---

# Edit 1 — Makefile: เติมชื่อใน AI_MODELS

การแก้แรกง่ายสุด บอก build system ว่า image นี้จะบรรจุโมเดลอะไรบ้าง:

```makefile
# proj_cm55/Makefile
ifeq ($(EDGE_AI_MODEL),combo)
AI_MODELS := motion audio radar cough alarm siren fall
endif                                            # ^ เติม fall
```

- Makefile จะ **auto-derive** ให้เองจากคำว่า `fall`:
  - นิยาม `-DEDGE_AI_MODEL_fall` (ตัวที่ `#if defined(...)` ในซอร์สเช็ก)
  - ดึง ML component + ตั้ง `CY_ML_MODEL_MEM`
  - (ถ้าเป็น `.a`) สร้าง `LDLIBS` guard ให้
- `combo` = image ที่บรรจุหลายโมเดลแล้วสลับตอนรันได้ (ที่เราใช้ทั้งคอร์ส)

> ข้อควรระวังจากบันทึกจริงของโปรเจกต์: flag ใน `.mk` ต้องเป็นคำเปล่าๆ เว้นวรรคหลังคำเกินมาจะทำ `ifeq` พัง — พิมพ์ `fall` ให้สะอาด อย่ามี trailing space

---

# Edit 2 — ai_engine.c: กายวิภาคของ ROW

ROW คือ "บัตรประจำตัวโมเดล" หนึ่งใบ ห่อด้วย `#if defined` เพื่อให้ image ที่ไม่บรรจุโมเดลนี้ ROW หายไปเฉยๆ (ขยายเป็นค่าว่าง):

```c
#if defined(EDGE_AI_MODEL_fall)
#  include "model_fall.h"
#  define FALL_ROW { .name = "Fall Detection",              \
        .description = "Detects a fall from the IMU",       \
        .sensor = AI_SENSOR_IMU, .class_count = 2,          \
        .class_labels = { "normal", "fall" },               \
        .flash_bytes = 40000u, .period_ms = 200u,           \
        .init = AIM_FALL_init, .enqueue = AIM_FALL_enqueue, \
        .dequeue = AIM_FALL_dequeue, .finalize = AIM_FALL_finalize },
#else
#  define FALL_ROW                       // image ไม่มี fall -> ROW เป็นค่าว่าง
#endif
```

- `.name` / `.class_labels` = สิ่งที่ `edge_ai.models()` ส่งกลับไปโชว์บนจอ
- `.sensor` เลือกว่าใช้ feed ตัวไหน · `.period_ms` = จังหวะป้อนข้อมูล
- สี่ pointer ล่างคือ **สัญญา 4 ฟังก์ชัน** (หน้าถัดไป)

> ก้อนนี้เป็นของจริงจาก `ai_engine.c` — `FALL_ROW` เขียนไว้ให้แล้วในซอร์ส เพียงแต่ `EDGE_AI_MODEL_fall` ยังไม่ถูกนิยาม (จนกว่าเราจะทำ Edit 1)

---

# Edit 2 (ต่อ) — ต่อ ROW เข้า s_models[]

เขียน ROW ไว้อย่างเดียวยังไม่พอ ต้อง "เสียบ" มันเข้าทะเบียนด้วย มิฉะนั้นมันลอยอยู่เฉยๆ:

```c
static const ai_model_desc_t s_models[] = {
    MOTION_ROW
    AUDIO_ROW
    RADAR_ROW
    COUGH_ROW
    ALARM_ROW
    SIREN_ROW
    FALL_ROW        // <- เติมบรรทัดนี้ (ลำดับที่นี่ = ลำดับในเมนู)
};
```

- ไม่ต้องมีลูกน้ำเพราะแต่ละ `_ROW` จบด้วย `},` ในตัวมาโครเองแล้ว
- ลำดับใน array นี้ = ลำดับที่โผล่ในเมนู/dropdown ตรงๆ
- ถ้า image นี้ไม่บรรจุ `fall` → `FALL_ROW` ขยายเป็นว่าง → ทะเบียนสั้นลงเองอย่างปลอดภัย

> จำ pattern สองจังหวะนี้: **ประกาศ ROW** (define) แล้ว **เสียบเข้า array** (ต่อท้าย) เหมือน UI page ในคอร์สเกมที่ต้อง register แล้วต้องใส่การ์ด — ลืมข้อใดข้อหนึ่งแล้ว "มีแต่ไม่โผล่" หรือ "โผล่แต่พัง"

---

# Edit 3 — วางไฟล์โมเดล (source vs ready-model)

การแก้ที่สามคือเอา "ตัวโมเดล" มาวางในโฟลเดอร์ `proj_cm55/modules/ai_models/` มีสองแบบ:

<div style="text-align:center;margin:6px 0">
<svg width="900" height="180" viewBox="0 0 900 180" font-family="DejaVu Sans, sans-serif">
  <rect x="20" y="20" width="410" height="140" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="225" y="48" font-size="15" font-weight="700" fill="#2e7d32" text-anchor="middle">source-generated (AIM_)</text>
  <text x="225" y="76" font-size="12" fill="#555" text-anchor="middle">model_fall.c + model_fall.h</text>
  <text x="225" y="98" font-size="12" fill="#555" text-anchor="middle">export AIM_FALL_init / enqueue / ...</text>
  <text x="225" y="122" font-size="11" fill="#888" text-anchor="middle">มาจาก DEEPCRAFT converter</text>
  <text x="225" y="142" font-size="11" fill="#888" text-anchor="middle">มี DSP front-end ในตัว · แก้/อ่านได้</text>
  <rect x="470" y="20" width="410" height="140" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="675" y="48" font-size="15" font-weight="700" fill="#6a1b9a" text-anchor="middle">ready-model .a (IMAI_)</text>
  <text x="675" y="76" font-size="12" fill="#555" text-anchor="middle">fall_lib_eval.a (binary อย่างเดียว)</text>
  <text x="675" y="98" font-size="12" fill="#555" text-anchor="middle">export IMAI_FALL_init / enqueue / ...</text>
  <text x="675" y="122" font-size="11" fill="#888" text-anchor="middle">objcopy เปลี่ยนชื่อกันชน (prefix)</text>
  <text x="675" y="142" font-size="11" fill="#888" text-anchor="middle">Infineon ส่งมาแบบ eval · ไม่มีซอร์ส</text>
</svg>
</div>

- ทั้งสองแบบเสียบเข้า ROW ได้เหมือนกัน เพราะ **ลายเซ็นฟังก์ชันเหมือนกันเป๊ะ** ต่างแค่คำนำหน้า
- Cough / Alarm / Siren ในเฟิร์มแวร์จริง = ready-model `.a` ทั้งสาม (แต่ละตัว objcopy prefix ให้ไม่ชนกัน)

> ปัญหาใหญ่ของ ready-model คือ **สัญลักษณ์ชนกัน** (`.a` หลายตัว export `IMAI_init` เหมือนกัน) วิธีแก้คือ objcopy เปลี่ยนชื่อเป็น `IMAI_COUGH_*` / `IMAI_ALARM_*` ให้ nm เห็นแยกกันสนิท

---

# สัญญา 4 ฟังก์ชัน — หัวใจที่ทุกโมเดลต้องมี

ไม่ว่าโมเดลมาจากทางไหน มันต้องให้ครบสี่ฟังก์ชันนี้ (ลายเซ็นตรงเป๊ะ) ROW ถึงจะเสียบได้:

```c
int  <PREFIX>_init(void);                // 0 = ok, <0 = fail (เตรียมโมเดล/arena)
int  <PREFIX>_enqueue(const float *in);  // ป้อน 1 sample/หน้าต่าง เข้าโมเดล
int  <PREFIX>_dequeue(float *out);       // 0 = มี verdict (เติม out[]), <0 = ยังไม่มี/จบ
void <PREFIX>_finalize(void);            // (ไม่ถูกเรียกตอน runtime — มีไว้ครบสัญญา)
```

- `ai_task` บน CM55 วนเรียก `enqueue` (ป้อนข้อมูลจากเซนเซอร์) แล้ว `dequeue` (ถามว่ามีคำตอบยัง)
- return codes: `SUCCESS(0)` / `NODATA(-1)` / `ERROR(-2)` / `STREAMEND(-3)`
- `<PREFIX>` = `AIM_FALL` (source) หรือ `IMAI_FALL` (ready `.a`) — เลือกให้ตรงกับไฟล์ที่วาง

> นี่คือ "interface" แบบเดียวกับที่ ROW ผูกด้วย function pointer — ตราบใดที่โมเดลทำตามสัญญานี้ `ai_engine` ไม่สนใจว่าข้างในเป็น TFLite-Micro, DEEPCRAFT หรืออะไร มันเรียกผ่าน 4 ช่องนี้เท่านั้น

---

# คณิตเบื้องหลัง (1) — โมเดลหนึ่งตัวกินหน่วยความจำเท่าไร

โมเดลไม่ได้อยู่ที่เดียว มันแยกร่างลงสองหน่วยความจำ — **weights อยู่ใน flash, arena อยู่ใน RAM** เขียนเป็นสูตรง่ายๆ ได้แบบนี้:

$$ M_{\text{flash}} = W_{\text{weights}} + C_{\text{code}}, \qquad M_{\text{RAM}} = A_{\text{arena}} + B_{\text{io}} $$

อ่านทีละตัว (ภาษาคน):

- $M_{\text{flash}}$ = ที่ที่โมเดลกินใน flash · $W_{\text{weights}}$ = ก้อนพารามิเตอร์ int8 ของโมเดล (ตัวนี้แหละคือ `.flash_bytes = 40000u` ที่เราประกาศใน `FALL_ROW`) · $C_{\text{code}}$ = โค้ด kernel ที่รันโมเดล
- $M_{\text{RAM}}$ = ที่ที่โมเดลกินใน RAM ตอนรัน · $A_{\text{arena}}$ = **tensor arena** ที่ TFLite-Micro ใช้พัก activation ระหว่างชั้น · $B_{\text{io}}$ = บัฟเฟอร์ input/output (หน้าต่าง feed)

arena ต้องใหญ่แค่ไหน? ใหญ่พอสำหรับ "จังหวะที่ tensor มีชีวิตพร้อมกันเยอะสุด" ในกราฟ:

$$ A_{\text{arena}} \;\ge\; \max_{t}\ \sum_{\tau\,\in\,\mathrm{live}(t)} \mathrm{size}(\tau) $$

> ทำไมเรื่องนี้สำคัญ **วันนี้**: ถ้าเราประเมิน `.flash_bytes` ต่ำไป weights ก้อนใหญ่จะทะลุ flash wall (`0x60900000`) — นี่คือเหตุผลที่กฎ checklist บอกให้ย้าย weights ก้อนโตไป section `.ml_weights` · และถ้า arena ไม่พอ `init()` จะคืนค่า `<0` ทำให้ `select()` โยน `OSError` (จำได้ไหมว่าเราห่อ `try/except` ไว้ทำไม)

---

# คณิตเบื้องหลัง (2) — สัญญา 4 ฟังก์ชันในภาษาคณิต

หน้าที่แล้วเราเห็นสี่ฟังก์ชันเป็นโค้ด ทีนี้มองมันเป็นคณิตสั้นๆ — โมเดลหนึ่งตัวคือ **ทูเพิลของฟังก์ชันสี่ตัว**:

$$ \mathcal{M} \;\equiv\; \langle\, \texttt{init},\ \texttt{enqueue},\ \texttt{dequeue},\ \texttt{finalize} \,\rangle $$

มันเป็นแบบ **streaming** — ป้อนทีละ sample สะสมจนเต็มหน้าต่างยาว $L$ ก่อน ถึงจะมี verdict โผล่:

$$ \underbrace{\texttt{enqueue}(x_1),\ \dots,\ \texttt{enqueue}(x_L)}_{L\ \text{ครั้ง}} \;\Longrightarrow\; \texttt{dequeue}(y) = 0 $$

พอ `dequeue` คืน `0` ตัว $y$ คือคะแนนของแต่ละคลาส เราเลือกคลาสที่คะแนนสูงสุดเป็นคำตอบ:

$$ \hat{c} \;=\; \arg\max_{c}\, p_c, \qquad \sum_{c} p_c = 1 $$

อ่านทีละตัว: $L$ = ความยาวหน้าต่าง (ผูกกับ `period_ms` × sample rate) · $p_c$ = ความมั่นใจของคลาส $c$ (รวมกันได้ 1) · $\hat{c}$ = คลาสที่ชนะ คือ `label` ที่ `edge_ai.result()` คืนกลับมา

> ทำไมเรื่องนี้สำคัญ **วันนี้**: สี่ฟังก์ชันนี้คือ "หน้าตา" ที่ ROW ผูกด้วย function pointer — โมเดลของเราจะต่อสายเข้าทะเบียนได้ก็ต่อเมื่อมันครบทั้งสี่และลายเซ็นตรงเป๊ะ · และ $\hat{c}$ นี่แหละคือเลขที่ฉบับเต็มเอาไปเทียบกับ `CONF_FLOOR` ก่อนจะเชื่อว่า "ล้มจริง" ไม่ใช่สัญญาณรบกวน

---

# feed — ทำไม Fall ไม่ต้องเขียน feed ใหม่

`enqueue` ต้องการ "ข้อมูลในหน่วยที่โมเดลฝึกมา" ตัวที่แปลงข้อมูลดิบจากเซนเซอร์ให้อยู่ในหน่วยนั้นเรียกว่า **feed** ในเฟิร์มแวร์มี feed อยู่แล้ว 3 ตัว ตามเซนเซอร์:

<div style="text-align:center;margin:6px 0">
<svg width="900" height="170" viewBox="0 0 900 170" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arFd" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="30" width="180" height="50" rx="9" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="110" y="52" font-size="12" font-weight="700" fill="#1565c0" text-anchor="middle">feed_imu</text>
  <text x="110" y="70" font-size="10" fill="#666" text-anchor="middle">Motion · Fall</text>
  <rect x="20" y="94" width="180" height="50" rx="9" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="110" y="116" font-size="12" font-weight="700" fill="#e65100" text-anchor="middle">feed_radar</text>
  <text x="110" y="134" font-size="10" fill="#666" text-anchor="middle">Push · Gesture</text>
  <rect x="20" y="158" width="180" height="0" rx="9"/>
  <rect x="240" y="62" width="180" height="50" rx="9" fill="#e0f7fa" stroke="#00838f" stroke-width="2"/>
  <text x="330" y="84" font-size="12" font-weight="700" fill="#00838f" text-anchor="middle">feed_audio</text>
  <text x="330" y="102" font-size="10" fill="#666" text-anchor="middle">Baby Cry · Cough · Alarm · Siren</text>
  <rect x="520" y="55" width="180" height="64" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="610" y="82" font-size="12" font-weight="700" fill="#6a1b9a" text-anchor="middle">enqueue()</text>
  <text x="610" y="102" font-size="10" fill="#666" text-anchor="middle">ของโมเดล</text>
  <line x1="200" y1="55" x2="330" y2="62" stroke="#607d8b" stroke-width="2" marker-end="url(#arFd)"/>
  <line x1="420" y1="87" x2="518" y2="87" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arFd)"/>
  <text x="800" y="90" font-size="11" fill="#2e7d32" text-anchor="middle">Fall ใช้ IMU</text>
  <text x="800" y="108" font-size="11" fill="#2e7d32" text-anchor="middle">= ยืม feed_imu</text>
</svg>
</div>

- `.sensor = AI_SENSOR_IMU` บอกให้ `ai_task` ใช้ `feed_imu` ที่มีอยู่แล้ว — **เราไม่ต้องเขียนบรรทัด feed เลย**
- นี่คือเหตุผลที่เราเลือก Fall เป็นตัวอย่างแรก: มันใช้ IMU เหมือน Motion ทุกอย่างต่อสายให้อัตโนมัติ

> เอกสารระบุชัด: `FALL` ยืม feed ของ IMU, `GESTURE` ยืม radar, `KEYWORD` ยืม mic — โมเดลที่ใช้เซนเซอร์เดิม **ไม่ต้องมี feed ใหม่** เลือกเซนเซอร์ให้ตรงกับที่มีอยู่ งานจะเบาที่สุด

---

# ถ้าเซนเซอร์ใหม่จริงๆ — ต้องเขียน feed เอง

ถ้าโมเดลของคุณใช้เซนเซอร์ที่ยังไม่มี feed (ไม่ใช่ IMU/radar/mic) จะมีงานเพิ่มสองที่:

```c
// 1) เขียน feed ใหม่ ลอกโครงจาก feed_imu / feed_radar
static void feed_<sensor>(const ai_model_desc_t *m) {
    // ดึง sample ใหม่สุดจากเซนเซอร์
    // แปลงเป็นหน่วยที่โมเดลฝึกมา (สำคัญ! ต้องตรงกับตอน train)
    // m->enqueue(sample);
}

// 2) เพิ่ม case ใน ai_task dispatch
switch (m->sensor) {
    case AI_SENSOR_IMU:   feed_imu(m);   break;
    case AI_SENSOR_RADAR: feed_radar(m); break;
    case AI_SENSOR_<S>:   feed_<sensor>(m); break;   // <- เพิ่มตรงนี้
}
```

- งานหลักของ feed คือ **แปลงหน่วย** — ดึงค่าดิบแล้วทำให้เหมือนที่โมเดลเห็นตอนฝึก
- ชุดบทเรียนนี้เราเลี่ยงงานนี้โดยเลือกโมเดลที่ใช้เซนเซอร์เดิม แต่ต้องรู้ว่ามันอยู่ตรงไหนเผื่อวันหน้า

> การเลือก "เซนเซอร์เดิม" ไม่ใช่การขี้เกียจ — เป็นการตัดสินใจเชิงวิศวกรรมที่ฉลาด: เริ่มจากเส้นทางที่พิสูจน์แล้วว่าเดินได้ ค่อยขยายทีหลัง (ตรงกับกฎ "reuse proven path, don't guess")

---

# เลือกตัวอย่าง — Fall Detection (มีในเฟิร์มแวร์จริง)

ทำไมเราเลือก Fall เป็นโมเดลตัวที่ 7 ที่จะเพิ่ม? เพราะมันเป็น **worked example ที่เขียนรออยู่แล้ว** ในซอร์ส:

| ประเด็น | Fall Detection |
|---|---|
| เซนเซอร์ | IMU → ยืม `feed_imu` (ไม่ต้องเขียน feed) |
| คลาส | `normal`, `fall` (2 คลาส) |
| ROW | `FALL_ROW` เขียนไว้แล้วใน `ai_engine.c` (เป็นคอมเมนต์รอ) |
| งานเรา | ทำ Edit 1 (Makefile) + ปลดล็อก Edit 2 + วางไฟล์โมเดล |
| ยืนยัน | `edge_ai.count()` เพิ่มขึ้น, `Fall Detection` โผล่ใน `models()` |

- ถ้ายังไม่มีไฟล์ `model_fall.c/.h` จริง คุณสามารถ **retrain ใน DEEPCRAFT Studio** แล้ว export หรือห่อโมเดล IMU ที่ฝึกเองในโมดูล 5 ตามสัญญา 4 ฟังก์ชัน
- โครงงาน "ต่อสาย" ทั้งหมดเหมือนกันหมด ไม่ว่าโมเดลจริงข้างในจะเป็นอะไร

> เริ่มจากตัวที่เฟิร์มแวร์ "เกือบพร้อม" อยู่แล้ว ทำให้เราโฟกัสที่ **กลไกการเพิ่ม** ไม่ใช่ไปติดเรื่องเทรนโมเดล ซึ่งเราทำไปแล้วใน โมดูล 5 (Training)

---

# Vela — ทำไม MCU ต้องคอมไพล์เพิ่ม

จำสเปกตรัมเป้าหมายจาก บทเรียน 1.1–1.3 ได้ไหม? Web/Cortex-A ใช้ `.tflite` เดิมได้เลย แต่ **MCU ตัวเดียวที่ต้องคอมไพล์เพิ่ม** ก่อนรันบน NPU:

<div style="text-align:center;margin:6px 0">
<svg width="880" height="150" viewBox="0 0 880 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arVe" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="48" width="190" height="56" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="115" y="72" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">model_int8.tflite</text>
  <text x="115" y="92" font-size="11" fill="#666" text-anchor="middle">จาก Training (5.8–5.9)</text>
  <rect x="330" y="48" width="190" height="56" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="425" y="72" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">vela</text>
  <text x="425" y="92" font-size="11" fill="#666" text-anchor="middle">คอมไพล์ให้ Ethos-U55</text>
  <rect x="640" y="48" width="210" height="56" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="745" y="72" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">_vela.tflite</text>
  <text x="745" y="92" font-size="11" fill="#666" text-anchor="middle">NPU อ่านออก · ฝังใน .a/.c</text>
  <line x1="210" y1="76" x2="328" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arVe)"/>
  <line x1="520" y1="76" x2="638" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arVe)"/>
  <text x="425" y="128" font-size="11" fill="#888" text-anchor="middle">Vela แปลง op ให้เป็นคำสั่งที่ Ethos-U55 รันได้ — ที่เหลือ CPU ทำ (fallback)</text>
</svg>
</div>

- Vela คือ compiler ของ Arm ที่แปลงกราฟ `.tflite` int8 → คำสั่งเฉพาะของ Ethos-U55 NPU
- เราทำขั้นนี้ไปแล้วใน บทเรียน 5.8–5.9 ([`quantize_vela.sh`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/quantize_vela.sh)) — ผลลัพธ์ `_vela.tflite` คือสิ่งที่ฝังในไฟล์โมเดล (Edit 3)
- Path B (hand-wrap) ต้องใส่ **Ethos-U custom op** ใน op resolver (`AddEthosU()`) โมเดลถึงเรียก NPU ได้

> int8 คือ "ตัวหารร่วม" ที่ MCU บังคับ — Vela รับเฉพาะ int8 นี่คือเหตุผลที่ โมดูล 5 (Training) เน้น quantization ไม่ใช่แค่ความแม่น แต่เพื่อให้ผ่าน Vela ลง NPU ได้

---

# โมเดลที่คุณฝึกเอง — สองเส้นทางสู่ AIM_/IMAI_

ถ้าเป็น `.tflite` ที่คุณเทรนเองใน โมดูล 5 (Training) จะทำให้บอร์ดรันได้ยังไง? มีสองทาง:

<div style="text-align:center;margin:6px 0">
<svg width="900" height="180" viewBox="0 0 900 180" font-family="DejaVu Sans, sans-serif">
  <rect x="20" y="20" width="410" height="145" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="225" y="46" font-size="14" font-weight="700" fill="#2e7d32" text-anchor="middle">Path A · DEEPCRAFT converter</text>
  <text x="225" y="72" font-size="11" fill="#555" text-anchor="middle">ป้อน .tflite/.keras เข้า converter</text>
  <text x="225" y="92" font-size="11" fill="#555" text-anchor="middle">มันสร้าง model_x.c/.h (AIM_*) ให้</text>
  <text x="225" y="112" font-size="11" fill="#555" text-anchor="middle">รวม DSP front-end (FFT/mel) ให้ด้วย</text>
  <text x="225" y="140" font-size="11" fill="#2e7d32" text-anchor="middle">แนะนำ · เรียบง่ายสุด</text>
  <rect x="470" y="20" width="410" height="145" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="675" y="46" font-size="14" font-weight="700" fill="#6a1b9a" text-anchor="middle">Path B · hand-wrap TFLite-Micro</text>
  <text x="675" y="72" font-size="11" fill="#555" text-anchor="middle">xxd -i ฝัง _vela.tflite เป็น bytes</text>
  <text x="675" y="92" font-size="11" fill="#555" text-anchor="middle">ตั้ง MicroInterpreter + AddEthosU()</text>
  <text x="675" y="112" font-size="11" fill="#555" text-anchor="middle">เขียน front-end เอง (graph ไม่ทำ FFT)</text>
  <text x="675" y="140" font-size="11" fill="#6a1b9a" text-anchor="middle">คุมได้เต็ม · งานสาย Researcher</text>
</svg>
</div>

> Path A เหมาะกับคอร์สทั่วไป Path B คือสิ่งที่สาย extension/research สอน — คุมทุกอย่างเองแลกกับงานที่มากขึ้น ชุดบทเรียนนี้เราเข้าใจทั้งสอง แล้วเลือก Path ที่เหมาะกับโมเดลของเรา

---

# กับดักตัวจริง — feature parity ไม่ใช่ตัว graph

จุดที่ทำให้โมเดลที่ฝึกดีๆ "ใบ้สนิท" บนบอร์ด มักไม่ใช่กราฟผิด แต่เป็น **front-end ไม่ตรงกับตอนเทรน**:

- โมเดลเสียง/เรดาร์ คาดหวัง feature vector เฉพาะ — เช่น Baby Cry = FFT 512 จุด Hann window → mel 20 band → clip → log ต่อหน้าต่าง 60 เฟรม
- ตัว `.tflite` **ไม่มี** ขั้น FFT/mel อยู่ในกราฟ — feed/enqueue ของคุณต้องทำเอง ให้ตรงเป๊ะกับตอนฝึก
- window/hop/mel/normalization ผิดนิดเดียว = คะแนนเพี้ยนเงียบๆ ไม่มี error ให้จับ

```c
// ใน enqueue: ต้องรัน front-end เดียวกับตอน train ก่อนป้อนเข้า tensor
int AIM_FALL_enqueue(const float *in) {
    // IMU 6 แกน -> normalize เหมือนตอน train -> เขียนลง input tensor
    // (Fall ใช้ IMU ตรงๆ ไม่มี FFT — ง่ายกว่าเสียง/เรดาร์มาก)
}
```

> นี่คือ "the #1 silent failure" ที่เอกสารเตือน — เลือก Fall (IMU) เป็นตัวแรกเพราะ front-end ของมันเบาสุด ไม่มี FFT ให้พลาด พอคล่องแล้วค่อยขยับไปงานเสียง
