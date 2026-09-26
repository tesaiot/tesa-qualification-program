---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 5.3 — ฝึกโมเดลใน Docker: หนึ่งชิ้นงาน สี่เป้าหมาย"
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

# บทเรียน 5.3 — ฝึกโมเดลใน Docker: หนึ่งชิ้นงาน สี่เป้าหมาย
## ฝึกโมเดลใน TensorFlow (Docker) แล้วทดสอบบน PC

**โมดูล 5 — ฝึกโมเดลและนำไปใช้หลายเป้าหมาย**

**โมดูล 5 · Pillar 4 — Training (train once, run everywhere)**

> คาถาประจำบทเรียน: **"เลิกยืมโมเดลสำเร็จรูป — ชุดบทเรียนนี้เราฝึกโมเดลของเราเอง จากข้อมูลของเราเอง แล้วบีบให้เล็กพอจะลงชิป"**

TensorFlow ใน Docker (รันเหมือนกันทุก OS) · ปลายทางคือไฟล์ [`model_int8.tflite`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/model_int8.tflite) หนึ่งไฟล์

---

# เปิดบทเรียนด้วยของจริงก่อน

เหมือนทุกบทเรียน เราเริ่มแบบ **กลับด้าน** — รันการฝึกที่ทำงานได้จริงก่อน เห็นตัวเลข accuracy ขึ้นจริง แล้วค่อยแกะว่าแต่ละบรรทัดทำอะไร

<div style="text-align:center;margin:10px 0">
<svg width="820" height="150" viewBox="0 0 820 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arOpen" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="40" width="180" height="70" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="104" y="72" font-size="15" font-weight="700" fill="#2e7d32" text-anchor="middle">รันการฝึกก่อน</text>
  <text x="104" y="94" font-size="12" fill="#555" text-anchor="middle">docker run train</text>
  <rect x="234" y="40" width="180" height="70" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="324" y="72" font-size="15" font-weight="700" fill="#1565c0" text-anchor="middle">แกะดูข้างใน</text>
  <text x="324" y="94" font-size="12" fill="#555" text-anchor="middle">4 จังหวะของการฝึก</text>
  <rect x="454" y="40" width="180" height="70" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="544" y="72" font-size="15" font-weight="700" fill="#e65100" text-anchor="middle">เติม/แก้เอง</text>
  <text x="544" y="94" font-size="12" fill="#555" text-anchor="middle">4 ช่องหลัก</text>
  <rect x="674" y="40" width="132" height="70" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="740" y="72" font-size="15" font-weight="700" fill="#6a1b9a" text-anchor="middle">โมเดลของเรา</text>
  <text x="740" y="94" font-size="12" fill="#555" text-anchor="middle">.tflite หนึ่งไฟล์</text>
  <line x1="194" y1="75" x2="230" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="414" y1="75" x2="450" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="634" y1="75" x2="670" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
</svg>
</div>

เราใช้แนว **PRIMM** เหมือนเดิม (Predict–Run–Investigate–Modify–Make) แต่รอบนี้ "ของที่ทำงานได้" ไม่ใช่แอปบนจอ — มันคือ **สคริปต์ฝึกโมเดล** ที่พ่นตัวเลข accuracy กับ confusion matrix ออกมา

> ชุดบทเรียนนี้ไม่ต้องเข้าใจ TensorFlow ทุกบรรทัด ขอแค่ได้เห็นโมเดลของคุณเรียนรู้จากข้อมูลจริง แล้วทายท่ามือชุดทดสอบถูก เท่านั้นพอ

---

# เป้าหมายของชุดบทเรียนนี้

จบชุดบทเรียนนี้เราจะเดินครบ 4 เรื่อง แล้วปิดท้ายด้วยโมเดลที่ฝึกเองและทดสอบผ่าน:

1. **ทำไมต้องฝึกใน Docker** — สภาพแวดล้อมที่ทำซ้ำได้ รันเหมือนกันบน macOS / Windows / Linux
2. **สี่จังหวะของการฝึก** — สร้างโมเดล (build) → ฝึก (fit) → บีบ int8 (convert) → ทดสอบบน PC (eval)
3. **ทำไมต้อง int8** และ **representative dataset** คืออะไร — หัวใจที่ทำให้โมเดลลงชิปได้
4. **อ่านผลเป็น** — float32 vs int8 accuracy, confusion matrix, จุดที่โมเดลสับสน
5. ลงมือ: เติม 4 ช่องใน [`s12_train.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l05-train-lab/practice/s12_train.py) แล้วรันใน Docker จนได้ [`model_int8.tflite`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/model_int8.tflite) + รายงานความแม่น

ปลายทางของวันนี้: โมเดลที่ **คุณฝึกเอง** ทายท่ามือของชุดทดสอบ (ที่โมเดลไม่เคยเห็น) ได้แม่น พร้อมไฟล์ `.tflite` ที่ชุดบทเรียนถัดไปจะเอาไปลงเบราว์เซอร์และบอร์ด

> วันนี้เราเน้น "ฝึกได้ + อ่านผลเป็น + บีบ int8 เป็น" ส่วนการเอาไปรันบนบอร์ดจริง (Vela/NPU) เก็บไว้ บทเรียน 5.8–5.9

---

# ชุดบทเรียนนี้อยู่ตรงไหนของวงจร

จำวงจรชีวิตข้อมูล 5 ขั้นจากบทเรียน 1.1–1.3 ได้ไหม — วันนี้เรามาถึง **ขั้นที่ 4 (Training)** แล้ว หลังเก็บข้อมูลเอง (DAQ) และแปลงสัญญาณเป็น (Analysis)

<div style="text-align:center;margin:6px 0">
<svg width="920" height="150" viewBox="0 0 920 150" font-family="DejaVu Sans, sans-serif">
  <g text-anchor="middle">
    <rect x="10" y="46" width="150" height="60" rx="10" fill="#eceff1" stroke="#90a4ae" stroke-width="2"/>
    <text x="85" y="72" font-size="13" font-weight="700" fill="#607d8b">1 · DAQ</text>
    <text x="85" y="92" font-size="10" fill="#888">เก็บข้อมูล (โมดูล 2)</text>
    <rect x="176" y="46" width="150" height="60" rx="10" fill="#eceff1" stroke="#90a4ae" stroke-width="2"/>
    <text x="251" y="72" font-size="13" font-weight="700" fill="#607d8b">2 · Processing</text>
    <text x="251" y="92" font-size="10" fill="#888">คณิต+ฟิสิกส์ (โมดูล 3)</text>
    <rect x="342" y="46" width="150" height="60" rx="10" fill="#eceff1" stroke="#90a4ae" stroke-width="2"/>
    <text x="417" y="72" font-size="13" font-weight="700" fill="#607d8b">3 · Analysis</text>
    <text x="417" y="92" font-size="10" fill="#888">DSP+feature (โมดูล 4)</text>
    <rect x="508" y="40" width="150" height="72" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="3"/>
    <text x="583" y="68" font-size="14" font-weight="700" fill="#6a1b9a">4 · Training</text>
    <text x="583" y="88" font-size="11" fill="#6a1b9a">เราอยู่นี่</text>
    <text x="583" y="104" font-size="10" fill="#888">โมดูล 5</text>
    <rect x="674" y="46" width="150" height="60" rx="10" fill="#eceff1" stroke="#90a4ae" stroke-width="2"/>
    <text x="749" y="72" font-size="13" font-weight="700" fill="#607d8b">5 · Apps</text>
    <text x="749" y="92" font-size="10" fill="#888">อนุมาน+action (โมดูล 6)</text>
  </g>
  <text x="417" y="136" font-size="12" fill="#888" text-anchor="middle">ตอนเริ่มคอร์ส เราเริ่มจากขั้น 5 (รันของสำเร็จ) วันนี้เราถอยกลับมาสร้างโมเดลเองที่ขั้น 4</text>
</svg>
</div>

- **บทเรียน 5.1–5.2 (ชุดบทเรียนก่อนหน้า)** — เราเก็บ dataset ท่ามือบนบอร์ด แล้วแบ่ง train/val/test ได้ `gestures.csv`
- **บทเรียน 5.3–5.5 (วันนี้)** — เอา `gestures.csv` ไปฝึกโมเดลใน TensorFlow แล้วบีบเป็น [`model_int8.tflite`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/model_int8.tflite)
- **บทเรียน 5.6–5.9 (ถัดไป)** — เอาไฟล์เดิมไปรันบนเบราว์เซอร์ (บทเรียน 5.6–5.7) และบนบอร์ด NPU (บทเรียน 5.8–5.9)

> โจทย์ของเราคือท่ามือ 3 คลาส `idle / circle / shaking` — **ตัวเดียวกับโมเดล Motion ที่ติดมากับบอร์ด** ตั้งแต่ บทเรียน 1.1–1.3 พอฝึกเองเสร็จ เราจะเทียบโมเดลของเรากับของโรงงานได้เลย

---

# ย้อนความ — บทเรียน 5.1–5.2 ให้อะไรเรามาบ้าง

ชุดบทเรียนนี้ไม่ได้เริ่มจากศูนย์ ของสำคัญที่ บทเรียน 5.1–5.2 ส่งต่อมาคือ **ข้อมูลที่พร้อมฝึก** และ **เครื่องมือจัดการข้อมูล**

<div style="text-align:center;margin:6px 0">
<svg width="880" height="150" viewBox="0 0 880 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arS11" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="44" width="200" height="64" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="120" y="70" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">บอร์ด BENTO</text>
  <text x="120" y="90" font-size="11" fill="#666" text-anchor="middle">เขย่า/วาดวง/วางนิ่ง</text>
  <rect x="290" y="44" width="220" height="64" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="400" y="66" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">data/gestures.csv</text>
  <text x="400" y="86" font-size="11" fill="#666" text-anchor="middle">label,ax,ay,az,gx,gy,gz</text>
  <text x="400" y="100" font-size="10" fill="#888" text-anchor="middle">หนึ่งแถวต่อหนึ่งตัวอย่าง ~50 Hz</text>
  <rect x="580" y="44" width="280" height="64" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="720" y="66" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">dataset_tools.py</text>
  <text x="720" y="86" font-size="11" fill="#666" text-anchor="middle">load_csv · make_windows</text>
  <text x="720" y="100" font-size="11" fill="#666" text-anchor="middle">normalize · split</text>
  <line x1="220" y1="76" x2="286" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS11)"/>
  <line x1="510" y1="76" x2="576" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS11)"/>
</svg>
</div>

- [`dataset_tools.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/dataset_tools.py) ทำงานหนักเรื่องข้อมูลให้เราแล้ว: อ่าน CSV → ตัดหน้าต่าง (window) → normalize → แบ่งชุด
- ในโค้ดชุดบทเรียนนี้ เราจึง `import dataset_tools as dt` แล้วเรียกใช้ — เหมือนที่ บทเรียน 1.1–1.3 เราได้ `edge_ai.models()` มาฟรีๆ
- งานใหม่ของ **บทเรียน 5.3–5.5** คือทุกอย่างที่เกิด **หลัง** ได้ข้อมูล: สร้างโมเดล ฝึก บีบ ทดสอบ

> ถ้ายังไม่มี `gestures.csv` จริง ก็รันได้ — `dataset_tools.synthesize()` สร้างชุดสังเคราะห์ให้ pipeline เดินได้ก่อน แล้วค่อยเอาข้อมูลจริงมาแทน (ฉบับเต็มทำ fallback นี้ให้อัตโนมัติ)

---

# ทำไมต้องฝึกใน Docker

การฝึกโมเดลต้องใช้ TensorFlow + ไลบรารีเป็นสิบ แต่ละเครื่องเวอร์ชันไม่ตรงกัน นี่คือฝันร้ายคลาสสิก "บนเครื่องผมรันได้นะ" — **Docker แก้ปัญหานี้**

<div style="text-align:center;margin:6px 0">
<svg width="880" height="180" viewBox="0 0 880 180" font-family="DejaVu Sans, sans-serif">
  <rect x="12" y="10" width="410" height="160" rx="12" fill="#ffebee" stroke="#c62828" stroke-width="2"/>
  <text x="217" y="36" font-size="14" font-weight="700" fill="#c62828" text-anchor="middle">ลง TensorFlow เองบนเครื่อง</text>
  <text x="217" y="64" font-size="12" fill="#555" text-anchor="middle">macOS ไม่มี GPU wheel · เวอร์ชันชนกัน</text>
  <text x="217" y="86" font-size="12" fill="#555" text-anchor="middle">โปรแกรม vendor GUI ไม่รันบน mac</text>
  <text x="217" y="108" font-size="12" fill="#555" text-anchor="middle">เพื่อนได้ผลไม่เท่าเรา ตามหา bug ทั้งวัน</text>
  <text x="217" y="140" font-size="12" fill="#c62828" text-anchor="middle">"บนเครื่องผมรันได้นะ"</text>
  <rect x="458" y="10" width="410" height="160" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="663" y="36" font-size="14" font-weight="700" fill="#2e7d32" text-anchor="middle">ฝึกใน Docker</text>
  <text x="663" y="64" font-size="12" fill="#555" text-anchor="middle">อิมเมจเดียว = เวอร์ชันเป๊ะเหมือนกันทุกคน</text>
  <text x="663" y="86" font-size="12" fill="#555" text-anchor="middle">รันเหมือนกันบน macOS / Windows / Linux</text>
  <text x="663" y="108" font-size="12" fill="#555" text-anchor="middle">ไม่รกเครื่อง ลบทิ้งได้ในบรรทัดเดียว</text>
  <text x="663" y="140" font-size="12" fill="#2e7d32" text-anchor="middle">"build ครั้งเดียว รันซ้ำได้ตลอด"</text>
</svg>
</div>

- `Dockerfile` ของเราเริ่มจาก `python:3.11-slim` แล้ว `pip install tensorflow ai-edge-litert numpy scikit-learn`
- เราเลือก package `tensorflow` (ไม่ใช่ `tensorflow-cpu`) เพราะมี wheel สำหรับ linux/arm64 → รันบน Docker ของ Apple Silicon ได้
- โค้ดของเราถูก bind-mount เข้าไปตอนรัน (`-v "$PWD":/work`) แก้ไฟล์บนเครื่อง เห็นผลใน container ทันที ไม่ต้อง rebuild

> Docker คือ "สภาพแวดล้อมสำเร็จรูปในกล่อง" — เหมือนเฟิร์มแวร์บนบอร์ดที่ทุกคนได้เหมือนกัน แต่คราวนี้เป็นโต๊ะฝึกโมเดลบน PC ที่ทุกคนได้เหมือนกัน

---

# ภาพรวม pipeline — หนึ่งชิ้นงาน สี่เป้าหมาย

ทั้ง Pillar 4 หมุนรอบไฟล์เดียว: [`model_int8.tflite`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/model_int8.tflite) เราสร้างมันในชุดบทเรียนนี้ แล้ว บทเรียน 5.6–5.9 เอาไปกระจายสี่ทาง

<div style="text-align:center;margin:6px 0">
<svg width="900" height="220" viewBox="0 0 900 220" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arPL" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="330" y="10" width="240" height="46" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="450" y="30" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">train.py (Keras ใน Docker)</text>
  <text x="450" y="46" font-size="10" fill="#888" text-anchor="middle">ชุดบทเรียนนี้เราทำจังหวะนี้</text>
  <rect x="330" y="78" width="240" height="46" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="3"/>
  <text x="450" y="99" font-size="14" font-weight="700" fill="#6a1b9a" text-anchor="middle">model_int8.tflite</text>
  <text x="450" y="115" font-size="10" fill="#888" text-anchor="middle">"train once" — หนึ่งชิ้นงาน</text>
  <line x1="450" y1="56" x2="450" y2="76" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arPL)"/>
  <!-- four targets -->
  <rect x="20" y="160" width="190" height="50" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="115" y="180" font-size="12" font-weight="700" fill="#1565c0" text-anchor="middle">MCU + Ethos-U55</text>
  <text x="115" y="198" font-size="10" fill="#888" text-anchor="middle">quantize_vela.sh · 5.8–5.9</text>
  <rect x="230" y="160" width="190" height="50" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="3"/>
  <text x="325" y="180" font-size="12" font-weight="700" fill="#2e7d32" text-anchor="middle">PC / Docker</text>
  <text x="325" y="198" font-size="10" fill="#888" text-anchor="middle">eval_pc.py · ชุดบทเรียนนี้</text>
  <rect x="440" y="160" width="200" height="50" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="540" y="180" font-size="12" font-weight="700" fill="#e65100" text-anchor="middle">Web / เบราว์เซอร์</text>
  <text x="540" y="198" font-size="10" fill="#888" text-anchor="middle">convert_web.py · 5.6–5.7</text>
  <rect x="660" y="160" width="210" height="50" rx="10" fill="#e0f7fa" stroke="#00838f" stroke-width="2"/>
  <text x="765" y="180" font-size="12" font-weight="700" fill="#00838f" text-anchor="middle">Cortex-A (Linux)</text>
  <text x="765" y="198" font-size="10" fill="#888" text-anchor="middle">ไฟล์เดิม · eval_pc.py</text>
  <line x1="420" y1="124" x2="130" y2="158" stroke="#607d8b" stroke-width="2" marker-end="url(#arPL)"/>
  <line x1="440" y1="124" x2="335" y2="158" stroke="#607d8b" stroke-width="2" marker-end="url(#arPL)"/>
  <line x1="460" y1="124" x2="540" y2="158" stroke="#607d8b" stroke-width="2" marker-end="url(#arPL)"/>
  <line x1="480" y1="124" x2="760" y2="158" stroke="#607d8b" stroke-width="2" marker-end="url(#arPL)"/>
</svg>
</div>

> มีแค่ MCU ที่ต้องคอมไพล์เพิ่ม (Vela) เพราะต้องแปลงให้ NPU อ่านออก · PC / Web / Cortex-A ใช้ไฟล์ `.tflite` เดียวกันเป๊ะ — นี่คือ "train once, run everywhere" ที่จับต้องได้ วันนี้เราสร้างชิ้นงานนั้นและทดสอบมันบน PC

---

# ทางเลือก — ฝึกบน Google Colab (ฟรี ไม่ต้องมี Docker)

ถ้าเครื่องยังไม่มี Docker หรืออยากได้ GPU ฟรี ใช้ **Colab notebook** ที่ให้มาได้เลย — pipeline เดียวกันเป๊ะ (synthesize → Conv1D → int8 → eval → ดาวน์โหลด [`model_int8.tflite`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/model_int8.tflite)):

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/notebooks/train_edge_ai.ipynb)

- ไฟล์: [`train_edge_ai.ipynb`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/notebooks/train_edge_ai.ipynb) (รันครบทุกเซลล์ = ได้ไฟล์ int8 พร้อม deploy)
- เปิดได้ 2 ทาง: กดแบดจ์ **หรือ** Colab → File → Upload notebook แล้วเลือกไฟล์นี้
- ผลลัพธ์เหมือนรันใน Docker — เอา [`model_int8.tflite`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/model_int8.tflite) ไปเข้าบทเรียน 5.6–5.7 (Web) / บทเรียน 5.8–5.9 (บอร์ด) ต่อได้ทันที

> Docker = reproducible แบบมืออาชีพ · Colab = เริ่มได้ทันทีในเบราว์เซอร์ — เลือกได้ตามสะดวก ผลได้ไฟล์เดียวกัน

---

# รันของจริงก่อน (1) — build อิมเมจ

ยังไม่ต้องเข้าใจโค้ด รันให้เห็นก่อน เปิด terminal ในโฟลเดอร์ [`shared/training/`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training) แล้ว build อิมเมจครั้งเดียว:

```bash
cd courses/edge-ai-developer/shared/training   # ในโฟลเดอร์ที่ clone repo นี้มา
docker build -t edgeai-train .
```

- คำสั่งนี้อ่าน `Dockerfile` แล้วประกอบ "กล่องสำเร็จรูป" ที่มี TensorFlow + ai-edge-litert พร้อมใช้
- ทำครั้งเดียวพอ ครั้งต่อไป Docker ใช้ cache รันได้ทันที (ยกเว้นแก้ `Dockerfile` เอง)
- `-t edgeai-train` = ตั้งชื่อกล่องว่า `edgeai-train` จะได้เรียกใช้ง่ายๆ

> ครั้งแรกจะโหลดนาน (ดึง TensorFlow ~หลายร้อย MB) รอสักครู่ พอขึ้น `naming to ... edgeai-train` ก็พร้อม ครั้งต่อไปเร็วมาก

---

# รันของจริงก่อน (2) — ฝึกโมเดล

ทีนี้สั่งฝึกจริง ใช้ `eval` เวอร์ชันสำเร็จ ([`train.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/train.py)) ก่อน เพื่อดูว่าปลายทางหน้าตาเป็นยังไง:

```bash
docker run --rm -v "$PWD":/work edgeai-train \
    python train.py --data data/gestures.csv --out model_int8.tflite
```

จะเห็น log ไหลออกมาแบบนี้ (ตัวเลขจริงจากรันที่เราทดสอบไว้แล้ว):

```
train/val/test windows: 101 21 21
Epoch 1/25 ... loss: 1.05 - accuracy: 0.44 - val_accuracy: 0.68
...
Epoch 25/25 ... accuracy: 1.00 - val_accuracy: 1.00
float32 test accuracy: 1.000
wrote model_int8.tflite (11504 bytes)
```

- `-v "$PWD":/work` = เอาโฟลเดอร์ปัจจุบันไปวางที่ `/work` ใน container โค้ด+ข้อมูล+ผลลัพธ์อยู่ที่เดียวกัน
- `--rm` = ลบ container ทิ้งเมื่อจบ ไม่รกเครื่อง
- ตอนจบได้ไฟล์ [`model_int8.tflite`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/model_int8.tflite) (~11 KB) โผล่มาในโฟลเดอร์จริงบนเครื่องเรา

> สังเกต `val_accuracy` ไต่ตาม `accuracy` ขึ้นไปด้วยกัน — นั่นแปลว่าโมเดล "เข้าใจ" ไม่ใช่แค่ "จำข้อสอบ" (ถ้า val ไม่ตาม train แปลว่า overfit)

---

# รันของจริงก่อน (3) — ทดสอบบน PC

มีโมเดลแล้ว ทดสอบไฟล์ int8 บน PC ด้วย [`eval_pc.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/eval_pc.py) — นี่คือ ground truth ก่อนเอาลงบอร์ด:

```bash
docker run --rm -v "$PWD":/work edgeai-train \
    python eval_pc.py --model model_int8.tflite --data data/gestures.csv
```

```
int8 test accuracy: 1.000

confusion (rows=true, cols=pred): ['idle', 'circle', 'shaking']
  idle     [7 0 0]
  circle   [0 7 0]
  shaking  [0 0 7]
```

- `int8 test accuracy` ควรใกล้ `float32 test accuracy` — ถ้าตกฮวบ แปลว่า quantization มีปัญหา
- **confusion matrix**: แถว = คลาสจริง คอลัมน์ = คลาสที่โมเดลทาย เลขบนแนวทแยง = ทายถูก นอกแนวทแยง = สับสน
- ตารางนี้สวยเพราะเป็นข้อมูลสังเคราะห์ (แยกคลาสง่าย) — ข้อมูลจริงจากบอร์ดจะเห็นความสับสนบ้าง

> เราเพิ่งเห็น "ปลายทาง" แล้ว: โมเดลของเราทายชุดทดสอบถูกหมด ทีนี้ย้อนกลับไปแกะว่า [`train.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/train.py) ทำอะไรทีละจังหวะ
