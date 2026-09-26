---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 5.6 — รันโมเดลบนเว็บ: LiteRT.js, int8 I/O และ parity"
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

# บทเรียน 5.6 — รันโมเดลบนเว็บ: LiteRT.js, int8 I/O และ parity
## รันโมเดลบน Web และเรื่องราว Cortex-A

**โมดูล 5 — ฝึกโมเดลและนำไปใช้หลายเป้าหมาย**

**โมดูล 5 · Training (Pillar 4) — เป้าหมายเดียว หลายที่รัน**

> คาถาประจำบทเรียน: **"โมเดล .tflite ไฟล์เดียวที่เราเทรน รันได้ทั้งในเบราว์เซอร์และบน Linux SBC — แต่ 'รันได้' กับ 'ตอบตรงกัน' เป็นคนละเรื่อง"**

จาก [`model_int8.tflite`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/model_int8.tflite) ตัวเดิม → LiteRT.js ในเบราว์เซอร์ + `ai-edge-litert` บน Cortex-A

---

# เปิดบทเรียนด้วยของจริงก่อน

เหมือนทุกบทเรียน เราเริ่มแบบ **กลับด้าน** — เปิดของที่ทำงานได้จริงก่อน แล้วค่อยแกะว่าทำไมมันถึงทำงาน

<div style="text-align:center;margin:10px 0">
<svg width="820" height="150" viewBox="0 0 820 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arOpen" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="40" width="180" height="70" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="104" y="72" font-size="15" font-weight="700" fill="#2e7d32" text-anchor="middle">รันในเบราว์เซอร์</text>
  <text x="104" y="94" font-size="12" fill="#555" text-anchor="middle">verdict เด้งบนหน้าเว็บ</text>
  <rect x="234" y="40" width="180" height="70" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="324" y="72" font-size="15" font-weight="700" fill="#1565c0" text-anchor="middle">แกะดูข้างใน</text>
  <text x="324" y="94" font-size="12" fill="#555" text-anchor="middle">LiteRT.js + front-end</text>
  <rect x="454" y="40" width="180" height="70" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="544" y="72" font-size="15" font-weight="700" fill="#e65100" text-anchor="middle">พิสูจน์ parity</text>
  <text x="544" y="94" font-size="12" fill="#555" text-anchor="middle">Web = PC ไหม</text>
  <rect x="674" y="40" width="132" height="70" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="740" y="72" font-size="15" font-weight="700" fill="#6a1b9a" text-anchor="middle">ต่อไป Cortex-A</text>
  <text x="740" y="94" font-size="12" fill="#555" text-anchor="middle">ไฟล์เดิมบน Linux</text>
  <line x1="194" y1="75" x2="230" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="414" y1="75" x2="450" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="634" y1="75" x2="670" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
</svg>
</div>

ในบทเรียน 5.3–5.5 เราเทรนโมเดล IMU (idle / circle / shaking) จนได้ [`model_int8.tflite`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/model_int8.tflite) แล้วรันบน PC ผ่าน [`eval_pc.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/eval_pc.py) วันนี้เอาไฟล์นั้นไปเปิดในเบราว์เซอร์ — เห็น verdict เด้งจากในหน้าเว็บโดยไม่ต้องลงอะไรเลย นั่นคือความอัศจรรย์ที่เราจะแกะ

> ชุดบทเรียนนี้เป้าหมายไม่ใช่แค่ "รันได้ในเว็บ" แต่คือ **พิสูจน์ให้ได้ว่าเบราว์เซอร์ตอบเหมือน PC** ภายในเกณฑ์ที่ยอมรับ — นี่คือ MVP ของบทเรียน 5.6–5.7

---

# เป้าหมายของชุดบทเรียนนี้

จบชุดบทเรียนนี้เราจะเดินครบเรื่องการ deploy โมเดลข้ามเป้าหมาย แล้วปิดท้ายด้วยการพิสูจน์ parity:

1. **runtime บนเบราว์เซอร์** — ทำไมเลือก LiteRT.js (ไม่ใช่ tfjs-tflite ที่ตายแล้ว หรือ ONNX-Runtime-Web)
2. **กับดัก int8 I/O** — ทำไมโมเดล MCU อาจต้องมี "ไฟล์ web" อีกใบ และ [`convert_web.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/convert_web.py) สร้างมันยังไง
3. **front-end นอกกราฟ** — สิ่งที่โมเดลไม่เห็น (normalize/DSP) ต้องทำซ้ำใน JS ให้ตรงเป๊ะ
4. **parity เป็นแล็บ** — วัด max-abs-diff ระหว่าง PC กับ Web ไม่ใช่เชื่อว่าตรงเอง
5. **เรื่องราว Cortex-A** — ไฟล์เดียวกันรันบน RPi/Jetson ด้วย `ai-edge-litert` ไม่ต้องแก้อะไร

ปลายทางวันนี้: window เดียวกันให้ verdict ตรงกันทั้งฝั่ง PC และเบราว์เซอร์ (LiteRT.js) ภายในเกณฑ์ TOL

> วันนี้เราไม่ได้เทรนโมเดลใหม่ เราเอาโมเดลจาก บทเรียน 5.3–5.5 มา **ส่งต่อให้หลายเป้าหมาย** — งานของวิศวกร deploy คือทำให้ทุกที่ได้คำตอบเดียวกัน

---

# ย้อนดูว่าเรามาถึงไหนใน Pillar 4

โมดูล 5 (Training) เดินเป็นสี่ชุดบทเรียน วันนี้คือชุดบทเรียนที่สาม — ขั้น "กระจายไปหลายเป้าหมาย"

<div style="text-align:center;margin:6px 0">
<svg width="900" height="150" viewBox="0 0 900 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arP4" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="16" y="46" width="196" height="66" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="114" y="72" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">5.1–5.2 · Dataset</text>
  <text x="114" y="94" font-size="11" fill="#555" text-anchor="middle">เก็บ+จัดข้อมูลบนบอร์ด</text>
  <rect x="234" y="46" width="196" height="66" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="332" y="72" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">5.3–5.5 · Train + PC</text>
  <text x="332" y="94" font-size="11" fill="#555" text-anchor="middle">TensorFlow → .tflite</text>
  <rect x="452" y="42" width="196" height="74" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="3"/>
  <text x="550" y="70" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">5.6–5.7 · Web + Cortex-A</text>
  <text x="550" y="92" font-size="11" fill="#555" text-anchor="middle">วันนี้ · LiteRT.js + parity</text>
  <rect x="670" y="46" width="196" height="66" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="768" y="72" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">5.8–5.9 · MCU/Vela</text>
  <text x="768" y="94" font-size="11" fill="#555" text-anchor="middle">int8 → Ethos-U55</text>
  <line x1="212" y1="79" x2="232" y2="79" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arP4)"/>
  <line x1="430" y1="79" x2="450" y2="79" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arP4)"/>
  <line x1="648" y1="79" x2="668" y2="79" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arP4)"/>
  <text x="452" y="30" font-size="12" fill="#888" text-anchor="middle">"ไฟล์เดียว หลายเป้าหมาย" — วันนี้คือ Web กับ Linux SBC</text>
</svg>
</div>

- บทเรียน 5.1–5.2 ให้ข้อมูล · บทเรียน 5.3–5.5 ให้ [`model_int8.tflite`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/model_int8.tflite) + `.norm.npz` และ `model.keras` เมื่อรัน `train.py --save-keras` — วันนี้เราใช้ของสามอย่างนี้ต่อ
- บทเรียน 5.8–5.9 (ชุดบทเรียนถัดไป) จะพาไป MCU ผ่าน Vela ซึ่งเป็นเป้าหมายเดียวที่ต้องคอมไพล์เพิ่ม ที่เหลือใช้ไฟล์เดิม

> ถ้าบทเรียนไหนหลุด กลับไปดู [`shared/training/`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training) ได้ ทั้ง [`train.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/train.py) [`eval_pc.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/eval_pc.py) [`convert_web.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/convert_web.py) อยู่ที่นั่น เป็นชุดเดียวต่อกัน

---

# train once, run everywhere — ซูมเข้าที่ Web กับ Cortex-A

บทเรียน 1.1–1.3 เราเห็นสเปกตรัมเป้าหมายผ่านๆ วันนี้เจาะสองช่องกลาง โดยยึด [`model_int8.tflite`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/model_int8.tflite) เป็นแหล่งความจริงเดียว

| เป้าหมาย | ทำอะไรกับไฟล์ | runtime | int8 บังคับ? |
|---|---|---|---|
| **MCU + Ethos-U55** | `vela` compile เพิ่ม (บทเรียน 5.8–5.9) | TFLite-Micro | ใช่ (NPU) |
| **Web (เบราว์เซอร์)** | อาจต้องแปลงเป็น float I/O | LiteRT.js | ไม่ (§1) |
| **Cortex-A (Linux)** | ใช้ไฟล์เดิม ไม่แก้ | `ai-edge-litert` | ไม่ |
| **PC / Docker** | ใช้ไฟล์เดิม | TF / LiteRT | ไม่ |

- มีแค่ **MCU** ที่ต้องคอมไพล์เพิ่ม (Vela) เพราะ NPU อ่าน custom op ของมันเอง
- **Web** เป็นที่เดียวที่อาจต้อง "แปลงครั้งที่สอง" ของโมเดลตัวเดิม (ไม่ใช่แค่ compile) — เดี๋ยวเราจะเห็นว่าทำไม
- **Cortex-A** เอาไฟล์เดิมไปวางแล้วรัน [`eval_pc.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/eval_pc.py) ได้เลย — สคริปต์ไม่ต้องแก้แม้แต่บรรทัดเดียว

> ตารางนี้คือ "หนึ่งไฟล์ สี่เป้าหมาย" ฉบับย่อ — วันนี้เราลงมือกับสองช่องกลาง

---

# ทำไมต้องรันบน Web

การเอาโมเดลไปไว้ในเบราว์เซอร์ไม่ใช่แค่ของเล่น มันแก้ปัญหาจริงของการส่งมอบงาน AI:

- **ไม่ต้องติดตั้งอะไร** — ส่งลิงก์ให้ลูกค้าหรือผู้สอน เปิดปุ๊บเห็น verdict ปั๊บ ไม่ต้องมีบอร์ด ไม่ต้อง flash
- **pre-flight ก่อน flash** — ลองโมเดลในเว็บก่อนเสียเวลา compile ลงบอร์ด (Edge Impulse ก็ทำแบบนี้)
- **เดโม + สอน** — BENTO Emulator รันโมเดลท่ามือจริงในเบราว์เซอร์ (ผ่าน ONNX Runtime Web) ผู้เรียนเปิดเล่นต่อที่บ้านได้
- **ความเป็นส่วนตัวยังอยู่** — โมเดลรันในเครื่องผู้ใช้ ข้อมูล (เสียง/ท่าทาง) ไม่ต้องขึ้นเซิร์ฟเวอร์

<div style="text-align:center;margin:8px 0">
<svg width="760" height="120" viewBox="0 0 760 120" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arWeb" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="36" width="180" height="52" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="110" y="60" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">.tflite</text>
  <text x="110" y="78" font-size="11" fill="#666" text-anchor="middle">ไฟล์จาก 5.3–5.5</text>
  <rect x="290" y="36" width="180" height="52" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="380" y="60" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">เบราว์เซอร์</text>
  <text x="380" y="78" font-size="11" fill="#666" text-anchor="middle">LiteRT.js · WebGPU</text>
  <rect x="560" y="36" width="180" height="52" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="650" y="60" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">verdict</text>
  <text x="650" y="78" font-size="11" fill="#666" text-anchor="middle">ไม่มีเซิร์ฟเวอร์</text>
  <line x1="200" y1="62" x2="286" y2="62" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arWeb)"/>
  <line x1="470" y1="62" x2="556" y2="62" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arWeb)"/>
</svg>
</div>

> Edge AI ในเบราว์เซอร์คือ "Edge" อีกแบบ — ขอบของเครือข่ายอยู่ที่แท็บของผู้ใช้ ข้อมูลไม่ออกไปไหน เหมือนที่รันบนชิป

---

# runtime บนเบราว์เซอร์ — เลือก LiteRT.js

ในเบราว์เซอร์มีหลายทางเลือกรัน ML แต่ไม่ใช่ทุกอันจะเหมาะ ผู้เขียนสำรวจแล้วสรุปไว้ดังนี้:

| ทางเลือก | สถานะ | ตัดสิน |
|---|---|---|
| **LiteRT.js** (Google, 2026) | โหลด `.tflite` ตรงๆ ผ่าน WASM/WebGPU | **เลือกอันนี้** |
| `@tensorflow/tfjs-tflite` | alpha ตั้งแต่ 2023 ไม่มี commit แล้ว | ตายแล้ว อย่าใช้ |
| **ONNX-Runtime-Web** | โตเต็มที่ int8 ดี | ต้องแปลง TFLite→ONNX (เพิ่ม hop) → fallback |
| **WebNN** | origin-trial Chrome/Edge (~2027) | ยังไม่พร้อม production |

- **LiteRT.js** ใช้ `.tflite` **ฟอร์แมตเดียวกับบนบอร์ด** — ไม่ต้องแปลงข้ามฟอร์แมต ลดโอกาสเพี้ยน
- **ORT-Web** เก็บเป็นทางสำรอง: ถ้าต้อง ONNX อยู่แล้ว หรืออยากได้ int8 WASM ที่ปรับจูนมานาน แต่ต้องแปลงเพิ่มหนึ่งขั้น
- **BENTO Edge AI Emulator** ใช้ทางสำรองนี้: แปลง [`model_int8.tflite`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/model_int8.tflite) เป็น ONNX ครั้งเดียวด้วย `tf2onnx` (int8 in/out) แล้วรันด้วย ONNX Runtime Web (WASM) จึงไม่ต้องมีไฟล์ float I/O แต่มีขั้นแปลงฟอร์แมตเพิ่มหนึ่งขั้น

> การเลือก runtime คือการตัดสินใจเชิงวิศวกรรม ไม่ใช่แค่ "อันไหนดัง" — LiteRT.js ชนะเพราะ **ฟอร์แมตเดียวกับ MCU** ทำให้ parity ง่ายขึ้นมาก

---

# LiteRT.js ทำงานยังไง

โหลดโมเดลในเบราว์เซอร์ด้วยสามบรรทัด แล้วเรียก `run()` เหมือน interpreter บน PC:

```javascript
import {loadLiteRt, loadAndCompile} from '@litertjs/core';
await loadLiteRt('.../wasm/');               // โหลด WASM runtime ครั้งเดียว
const model = await loadAndCompile(
    'model_web.tflite', {accelerator: 'webgpu'});   // WebGPU ถ้ามี, ไม่งั้น WASM
const out = model.run([x]);                  // x = feature ที่เตรียมไว้แล้ว
```

- `loadLiteRt()` โหลด WASM (XNNPACK) ครั้งเดียว · `loadAndCompile()` คอมไพล์กราฟ · `run()` อนุมาน
- `accelerator:'webgpu'` ใช้ GPU ของเครื่องผ่านเบราว์เซอร์ ถ้าไม่รองรับก็ถอยไป WASM CPU อัตโนมัติ
- สังเกตว่า `run()` รับ `x` ที่ **เตรียม feature เสร็จแล้ว** — กราฟไม่ได้ทำ front-end ให้ (จุดสำคัญของชุดบทเรียนนี้)

> เทียบกับ PC: `loadAndCompile` ≈ `Interpreter(model_path=...)` + `allocate_tensors()`, และ `model.run` ≈ `set_tensor` + `invoke` + `get_tensor` — คนละภาษา แต่ท่าเดียวกัน

---

# กับดัก int8 I/O — ทำไม Web อาจต้องไฟล์ที่สอง

โมเดลที่เราเทรนให้ MCU เป็น **full-integer int8**: input int8, output int8 (เพราะ Ethos-U55 บังคับ) แต่...

<div style="text-align:center;margin:6px 0">
<svg width="880" height="150" viewBox="0 0 880 150" font-family="DejaVu Sans, sans-serif">
  <rect x="20" y="30" width="400" height="96" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="220" y="54" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">model_int8.tflite (MCU)</text>
  <text x="220" y="78" font-size="12" fill="#555" text-anchor="middle">int8 in → กราฟ → int8 out</text>
  <text x="220" y="100" font-size="11" fill="#888" text-anchor="middle">Ethos-U55 บังคับ full-integer</text>
  <rect x="460" y="30" width="400" height="96" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="660" y="54" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">model_web.tflite (เบราว์เซอร์)</text>
  <text x="660" y="78" font-size="12" fill="#555" text-anchor="middle">float32 in → กราฟ → float32 out</text>
  <text x="660" y="100" font-size="11" fill="#888" text-anchor="middle">LiteRT.js บังคับ I/O = float32/int32</text>
</svg>
</div>

- **LiteRT.js จำกัด I/O tensor เป็น float32/int32** ไฟล์ int8 เต็ม (int8 in/out) อาจโหลดไม่ได้ในเบราว์เซอร์
- ทางแก้: ทำ **weight-only / dynamic-range int8** (น้ำหนัก int8 แต่ I/O เป็น float) หรือ float32 ล้วน
- ไฟล์ web เล็กกว่า float ~4 เท่า (เพราะน้ำหนักยัง int8) แต่ผ่านข้อจำกัด I/O ของเบราว์เซอร์

> นี่คือที่เดียวในทั้งคอร์สที่ต้อง **แปลงโมเดลครั้งที่สอง** ไม่ใช่แค่ compile — และต้องลองจริงว่าไฟล์ไหนโหลดได้ในเบราว์เซอร์

---

# convert_web.py — สร้างไฟล์ web จากน้ำหนักชุดเดียว

ตัวช่วยที่เตรียมไว้ให้แล้วใน [`convert_web.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/convert_web.py) แปลง `model.keras` เดิม → ไฟล์ web:

```python
model = tf.keras.models.load_model("model.keras")   # Keras ตัวเดียวกับที่เทรน
conv = tf.lite.TFLiteConverter.from_keras_model(model)
conv.optimizations = [tf.lite.Optimize.DEFAULT]      # dynamic-range: int8 weights, float I/O
tflite = conv.convert()
open("model_web.tflite", "wb").write(tflite)
```

- แปลงจาก **Keras ตัวเดิม** ไม่ใช่จากไฟล์ int8 — จึงพิสูจน์ได้ว่ามาจากน้ำหนักชุดเดียวกับโมเดล MCU
- `Optimize.DEFAULT` โดยไม่ให้ representative dataset = dynamic-range (น้ำหนัก int8, activation/IO float)
- ไฟล์ที่ได้ **browser-clean**: ไม่มี ethos-u custom op รันได้ทั้งในเบราว์เซอร์และบน Cortex-A

> `model.keras` ได้จาก `train.py --save-keras` แล้วรันผ่าน Docker เดียวกับ บทเรียน 5.3–5.5: `docker run ... python convert_web.py --keras model.keras --out model_web.tflite` — ไม่ต้องลง TensorFlow บนเครื่องตัวเอง

---

# ของจริงที่ต้องพูดตรงๆ — โมเดล DEEPCRAFT ที่ shipped

มีเรื่องหนึ่งที่ต้องซื่อสัตย์: โมเดล 6 ตัวที่ติดมากับเฟิร์มแวร์ **ไม่ได้โหลดในเบราว์เซอร์ได้ทุกตัว**

- โมเดล int8 ของ NPU (Motion, Baby Cry) ถูก **Vela-compile มาแล้ว** มี `ethos-u` custom op → เบราว์เซอร์/interpreter ทั่วไปโหลดไม่ได้
- โมเดล **radar เป็น float32** ไม่มี custom op → โหลดในเบราว์เซอร์ได้ (เป็นหลักฐานว่า DEEPCRAFT `.tflite` ทำ browser-clean ได้)
- **โมเดลที่ผู้เรียนเทรนเอง** (export จาก TF แบบ CPU-only ตามชุดบทเรียนนี้) → browser-portable โดยปริยาย

<div style="text-align:center;margin:6px 0">
<svg width="820" height="96" viewBox="0 0 820 96" font-family="DejaVu Sans, sans-serif">
  <rect x="14" y="20" width="392" height="60" rx="10" fill="#ffebee" stroke="#c62828" stroke-width="2"/>
  <text x="210" y="44" font-size="12" font-weight="700" fill="#c62828" text-anchor="middle">Vela int8 (Motion/BabyCry)</text>
  <text x="210" y="64" font-size="11" fill="#666" text-anchor="middle">มี ethos-u custom op → เบราว์เซอร์โหลดไม่ได้</text>
  <rect x="418" y="20" width="392" height="60" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="614" y="44" font-size="12" font-weight="700" fill="#2e7d32" text-anchor="middle">โมเดลของคุณ / radar float32</text>
  <text x="614" y="64" font-size="11" fill="#666" text-anchor="middle">ops มาตรฐาน → รันในเบราว์เซอร์ได้</text>
</svg>
</div>

> บทเรียน: สิ่งที่ทำให้ "browser-portable" คือ **ไม่มี custom op เฉพาะ NPU** — โมเดลที่คุณ export เองในชุดบทเรียนนี้ปลอดภัยอยู่แล้ว ส่วนไฟล์ Vela เก็บไว้ให้ MCU

---

# สิ่งที่กราฟไม่เห็น — front-end อยู่นอกกราฟ

หัวใจที่คนพลาดบ่อยที่สุด: โมเดล `.tflite` เห็นแค่ **feature vector ที่แปลงเสร็จแล้ว** ส่วนขั้นแปลงสัญญาณอยู่ **นอกกราฟ**

<div style="text-align:center;margin:6px 0">
<svg width="900" height="150" viewBox="0 0 900 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arFE" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="46" width="300" height="72" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="164" y="74" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">front-end (นอกกราฟ)</text>
  <text x="164" y="96" font-size="11" fill="#666" text-anchor="middle">normalize · window · (เสียง: FFT/Mel/log)</text>
  <rect x="360" y="46" width="240" height="72" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="480" y="74" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">กราฟ .tflite</text>
  <text x="480" y="96" font-size="11" fill="#666" text-anchor="middle">เห็นแค่ feature ที่แปลงเสร็จ</text>
  <rect x="646" y="46" width="240" height="72" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="766" y="74" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">scores</text>
  <text x="766" y="96" font-size="11" fill="#666" text-anchor="middle">ความน่าจะเป็นต่อคลาส</text>
  <line x1="314" y1="82" x2="358" y2="82" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arFE)"/>
  <line x1="600" y1="82" x2="644" y2="82" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arFE)"/>
  <text x="164" y="30" font-size="11" fill="#ef6c00" text-anchor="middle">คุณต้องทำซ้ำขั้นนี้ใน JS/Python ให้ตรง</text>
</svg>
</div>

- โมเดล IMU ของเรา front-end คือ **normalize ด้วย mean/std** (จาก `.norm.npz`) + จัด window
- โมเดลเสียง front-end หนักกว่ามาก: FFT → Mel → log (เป็น C ที่เรียก CMSIS-DSP ตอนอยู่บนบอร์ด)
- ถ้าจะรันในเบราว์เซอร์/PC ต้อง **สร้าง front-end ขึ้นมาใหม่** ให้ผลออกมาเหมือนกันเป๊ะ

> นี่คือบทเรียน "โมเดลเห็นอะไรจริงๆ" (บทเรียน 4.1–4.2) กลับมาทวงคืน — ถ้า front-end คนละแบบ ต่อให้กราฟเดียวกัน verdict ก็เพี้ยน

---

# parity คือแล็บ ไม่ใช่ข้อสมมติ

คำเตือนสำคัญ: เบราว์เซอร์กับบอร์ด **ไม่การันตีว่าได้เลขเป๊ะทุกบิต**

- เบราว์เซอร์ใช้ **XNNPACK** · บอร์ดใช้ **CMSIS-NN** · CMSIS-NN bit-exact กับ TFLite *reference* kernel ไม่ใช่กับ XNNPACK
- แปลว่าคะแนนอาจต่างกันนิดหน่อยแม้เป็นโมเดลไฟล์เดียวกัน — เรื่องปกติ ไม่ใช่บั๊ก
- วิธีที่ถูก: **วัด** ความต่าง (`max|score_pc - score_web|`) แล้วตั้งเกณฑ์ยอมรับ `TOL` เช่น 0.02

```python
diff = float(np.max(np.abs(s_int8 - s_web)))
ok = diff <= TOL and s_int8.argmax() == s_web.argmax()
```

> "ตอบตรงกัน" ในงาน embedded ไม่ได้แปลว่าเท่ากันเป๊ะ แต่แปลว่า **คลาสที่ชนะตรงกัน + คะแนนต่างในเกณฑ์** — เราจึงต้องวัด ไม่ใช่หวังเอา

---

# คณิตเบื้องหลัง int8 — quantize / dequantize

สองสูตรนี้คือหัวใจของ **เติม 2** กับ **เติม 4** ที่เราเพิ่งไล่โค้ด เขียนเป็นคณิตให้เห็นชัดว่าทำอะไร:

**ตอนป้อนเข้ากราฟ (quantize float → int8):**

$$q = \mathrm{clip}\!\left(\operatorname{round}\!\left(\frac{x}{s} + z\right),\,-128,\,127\right)$$

**ตอนอ่านผลออกมา (dequantize int8 → float):**

$$\hat{x} = (q - z)\cdot s$$

อ่านทีละตัวแบบภาษาคน:

- $x$ — ค่า feature แบบ float หลัง normalize (ผลของ **เติม 1**)
- $s$ — *scale* คือ "float กี่หน่วยต่อ int8 หนึ่งขั้น" อ่านมาจากโมเดล `inp["quantization"]` โดยตรง
- $z$ — *zero-point* คือค่า int8 ที่แทน $0.0$ พอดี ก็อ่านจากโมเดลเช่นกัน
- $q$ — ค่า int8 ที่ป้อนเข้ากราฟจริง · $\hat{x}$ — ค่า float ที่ได้กลับมาหลัง dequantize
- ช่วง int8 มี $2^{8}=256$ ระดับ ($-128 \ldots 127$) จึงต้อง $\mathrm{clip}$ กันค่าล้น

> ทำไมสำคัญกับชุดบทเรียนนี้: $s$ กับ $z$ ต้อง **อ่านจากโมเดล ไม่ใช่เดา** — ใส่ผิดแม้นิดเดียว input ก็เพี้ยนตั้งแต่ยังไม่ถึงกราฟ และไฟล์ web (float I/O) ไม่ต้องทำสองสูตรนี้เลย นั่นคือความต่างเดียวของเส้นทางเบราว์เซอร์

---

# คณิตของ parity — วัดความต่าง ไม่ใช่หวังให้เท่า

เกณฑ์ผ่าน MVP ของบทเรียน 5.6–5.7 ทั้งอันเขียนเป็นสมการได้สั้นๆ แค่สองบรรทัด:

$$d \;=\; \max_{k}\,\bigl|\,s^{\text{pc}}_{k} - s^{\text{web}}_{k}\,\bigr|$$

$$\textbf{PASS} \iff d \le \mathrm{TOL} \;\;\wedge\;\; \operatorname*{arg\,max}_{k}\, s^{\text{pc}}_{k} = \operatorname*{arg\,max}_{k}\, s^{\text{web}}_{k}$$

- $s^{\text{pc}}_{k},\, s^{\text{web}}_{k}$ — คะแนน softmax ของคลาส $k$ ฝั่ง PC และฝั่งเบราว์เซอร์
- $d$ — ความต่างสูงสุดข้ามทุกคลาส (ก็คือ `max-abs-diff` ในโค้ด)
- $\mathrm{TOL}$ — เกณฑ์ยอมรับ เช่น $0.02$ · $\operatorname{arg\,max}$ — ดัชนีคลาสที่ชนะ

คะแนนเป็น softmax head ในกราฟ จึงรวมได้ราว $1.0$ เสมอ:

$$\sigma(o)_k = \frac{e^{\,o_k}}{\sum_j e^{\,o_j}}, \qquad \sum_k \sigma(o)_k = 1$$

> ทำไมสำคัญกับชุดบทเรียนนี้: XNNPACK (เบราว์เซอร์) กับ CMSIS-NN (บอร์ด) ไม่ bit-exact ต่อกัน $d$ จึงไม่จำเป็นต้องเป็น $0$ — สมการบรรทัดที่สองคือ MVP ของบทเรียน 5.6–5.7 ทั้งอัน "คลาสตรง + ต่างในเกณฑ์" เขียนเป็นคณิต

---

# front-end คือจุดที่ parity พังบ่อยที่สุด

ถ้า parity ไม่ผ่าน 9 ใน 10 ครั้งปัญหาอยู่ที่ **front-end** ไม่ใช่ตัวโมเดล และตัวที่พังบ่อยสุดคือ **normalization**

```python
# ตอนเทรน (train.py) เราเซฟ mean/std ที่ fit จาก train set ไว้:
np.savez(out + ".norm.npz", mean=mean, std=std)

# ตอน deploy ทุกเป้าหมายต้อง normalize ด้วยชุดเดียวกันนี้:
x = (window - z["mean"]) / z["std"]      # PC / Cortex-A
// x = window.map((v,i) => (v - mean[i%6]) / std[i%6])   // เบราว์เซอร์
```

- ถ้าฝั่งหนึ่งลืม normalize หรือใช้ mean/std คนละชุด โมเดลจะเห็นข้อมูลคนละสเกล → verdict เพี้ยนทันที
- เราจึงเซฟ `mean/std` เป็นไฟล์ติดไปกับโมเดลเสมอ (silent-failure point ที่คลาสสิกมาก)
- quantize (float→int8) ก็ต้องใช้ `scale/zero` ที่ **อ่านจากโมเดล** ไม่ใช่เดา

> จำประโยคนี้ไว้: **"โมเดลเดียวกัน ข้อมูลคนละสเกล = คนละโมเดล"** — parity เริ่มพังตั้งแต่ยังไม่ถึงกราฟ
