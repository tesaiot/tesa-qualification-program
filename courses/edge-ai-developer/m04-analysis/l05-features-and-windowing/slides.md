---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 4.5 — feature และหน้าต่าง: สิ่งที่โมเดลเห็นจริง"
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

# บทเรียน 4.5 — feature และหน้าต่าง: สิ่งที่โมเดลเห็นจริง
## สิ่งที่โมเดล "เห็น" จริง ๆ

**โมดูล 4 — วิเคราะห์สัญญาณ**

**โมดูล 4 (Analysis, Pillar 3) — ชุดบทเรียนที่สาม**

> คาถาประจำบทเรียน: **"โมเดลไม่เคยเห็นสัญญาณดิบ มันเห็นแต่ feature vector ที่เราบีบมาให้ — วันนี้เราจะเป็นคนบีบเอง"**

MicroPython บนบอร์ด BENTO (PSoC Edge · Cortex-M55 + Ethos-U55 NPU)

---

# เปิดบทเรียนด้วยของจริงก่อน

เหมือนทุกบทเรียน เราเริ่มแบบ **กลับด้าน** — รันของที่ทำงานได้จริงก่อน แล้วค่อยแกะว่ามันบีบสัญญาณเป็นอะไร

<div style="text-align:center;margin:10px 0">
<svg width="820" height="150" viewBox="0 0 820 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arOpen" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="40" width="180" height="70" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="104" y="72" font-size="15" font-weight="700" fill="#2e7d32" text-anchor="middle">รันตัวอย่างก่อน</text>
  <text x="104" y="94" font-size="12" fill="#555" text-anchor="middle">s10_windowing</text>
  <rect x="234" y="40" width="180" height="70" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="324" y="72" font-size="15" font-weight="700" fill="#1565c0" text-anchor="middle">แกะดูข้างใน</text>
  <text x="324" y="94" font-size="12" fill="#555" text-anchor="middle">window + feature</text>
  <rect x="454" y="40" width="180" height="70" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="544" y="72" font-size="15" font-weight="700" fill="#e65100" text-anchor="middle">เติม/แก้เอง</text>
  <text x="544" y="94" font-size="12" fill="#555" text-anchor="middle">5 จุดหลัก</text>
  <rect x="674" y="40" width="132" height="70" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="740" y="72" font-size="15" font-weight="700" fill="#6a1b9a" text-anchor="middle">ต่อยอด</text>
  <text x="740" y="94" font-size="12" fill="#555" text-anchor="middle">สู่ Training</text>
  <line x1="194" y1="75" x2="230" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="414" y1="75" x2="450" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="634" y1="75" x2="670" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
</svg>
</div>

เปิด [`s10_windowing.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l05-features-and-windowing/examples/s10_windowing.py) แล้ว **Run** ก่อนเลย — วางบอร์ดนิ่ง สลับกับเขย่าเบา ๆ แล้วดูแท่ง `mean/std/band0..3` ขยับ นั่นแหละคือ feature vector ที่กำลังไหลเข้าโมเดล

> ชุดบทเรียนนี้ไม่ต้องเข้าใจสูตรทุกตัวตั้งแต่แรก ขอแค่เห็นว่า "สัญญาณดิบก้อนหนึ่งกลายเป็นตัวเลขไม่กี่ตัว" แล้วเริ่มสงสัยว่าตัวเลขพวกนี้มาจากไหน เท่านั้นพอ

---

# เราอยู่ตรงไหนของวงจร

วันนี้เป็นชุดบทเรียนที่สามของ **Analysis (Pillar 3)** — ขั้นที่ 3 ของวงจรชีวิตข้อมูล เป็นจุดที่สัญญาณกลายเป็น "สิ่งที่โมเดลกินได้"

<div style="text-align:center;margin:6px 0">
<svg width="920" height="150" viewBox="0 0 920 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arLC" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g text-anchor="middle">
    <rect x="10" y="46" width="160" height="64" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="90" y="74" font-size="14" font-weight="700" fill="#1565c0">1 · DAQ</text>
    <text x="90" y="94" font-size="11" fill="#888">โมดูล 2</text>
    <rect x="196" y="46" width="160" height="64" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="276" y="74" font-size="14" font-weight="700" fill="#2e7d32">2 · Processing</text>
    <text x="276" y="94" font-size="11" fill="#888">โมดูล 3</text>
    <rect x="382" y="40" width="160" height="76" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="3"/>
    <text x="462" y="72" font-size="14" font-weight="700" fill="#e65100">3 · Analysis</text>
    <text x="462" y="92" font-size="11" fill="#555">4.1–4.2·4.3–4.4·4.5–4.6 (นี่)</text>
    <text x="462" y="108" font-size="10" fill="#888">feature front-end</text>
    <rect x="568" y="46" width="160" height="64" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
    <text x="648" y="74" font-size="14" font-weight="700" fill="#6a1b9a">4 · Training</text>
    <text x="648" y="94" font-size="11" fill="#888">โมดูล 5</text>
    <rect x="754" y="46" width="160" height="64" rx="12" fill="#e0f7fa" stroke="#00838f" stroke-width="2"/>
    <text x="834" y="74" font-size="14" font-weight="700" fill="#00838f">5 · Apps</text>
    <text x="834" y="94" font-size="11" fill="#888">โมดูล 6</text>
  </g>
  <line x1="170" y1="78" x2="194" y2="78" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <line x1="356" y1="78" x2="380" y2="78" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <line x1="542" y1="78" x2="566" y2="78" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <line x1="728" y1="78" x2="752" y2="78" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <text x="462" y="140" font-size="12" fill="#888" text-anchor="middle">Analysis คือประตูสุดท้ายก่อนสัญญาณจะกลายเป็นข้อมูลที่โมเดลกินได้</text>
</svg>
</div>

> บทเรียน 4.1–4.2 เราขัดสัญญาณให้สะอาด (filter) · บทเรียน 4.3–4.4 เราแปลงไปโดเมนความถี่ (FFT) · วันนี้ บทเรียน 4.5–4.6 เราเอาสองอันนั้นมาบีบเป็น **feature vector** ที่โมเดลใช้จริง

---

# เป้าหมายของชุดบทเรียนนี้

จบชุดบทเรียนนี้เราจะเดินครบ 4 เรื่อง แล้วปิดท้ายด้วยการทำ feature front-end ด้วยมือเอง:

1. **ทำไมโมเดลไม่กิน sample ดิบ** ทีละจุด แต่กิน "หน้าต่าง" (window) ของสัญญาณ
2. **Windowing + hop** — ตัดสัญญาณเป็นหน้าต่างซ้อนกัน ทำไมต้องซ้อน (overlap)
3. **Feature vector** — บีบหน้าต่างเป็นตัวเลขไม่กี่ตัว (mean, std, พลังงานต่อย่าน) และญาติของมันคือ **mel/log-mel spectrogram** ที่โมเดลเสียงใช้
4. ลงมือ: สร้าง feature vector จากสัญญาณ IMU ด้วยตัวเอง แล้วดูมันขยับสดบนจอ

ปลายทางของวันนี้: จากสัญญาณ IMU ดิบ 50 จุด สร้าง feature vector 6 ตัวที่ **เปลี่ยนตามการเคลื่อนไหวจริง** ขึ้นจอ

> วันนี้เราไม่ฝึกโมเดลนะ เราสร้าง "สิ่งที่โมเดลจะเห็น" ต่างหาก — พอถึงบทเรียน Training (บทเรียน 5.1–5.2) คุณจะเก็บ feature vector พวกนี้เป็น dataset จริง

---

# ปัญหา: โมเดลไม่กิน sample ดิบทีละจุด

ลองนึกถึงเสียง "ไอ" หนึ่งครั้ง หรือท่า "เขย่า" หนึ่งที — มันไม่ใช่ค่า ณ จุดเดียว มันคือ **รูปร่างของสัญญาณช่วงเวลาหนึ่ง**

- ถ้าป้อน accel ทีละจุดให้โมเดล มันเห็นแค่ตัวเลขเดียว บอกอะไรไม่ได้ว่ากำลัง "เขย่า" หรือ "นิ่ง"
- ความหมายอยู่ใน **แพตเทิร์นตามเวลา** — ต้องดูสัญญาณเป็นก้อน ไม่ใช่ทีละจุด
- เราจึงรวบสัญญาณเป็น "หน้าต่าง" (window) เช่น 50 จุด (= 1 วินาทีที่ 50 Hz) แล้วค่อยตัดสินใจจากทั้งก้อน

<div style="text-align:center;margin:8px 0">
<svg width="820" height="120" viewBox="0 0 820 120" font-family="DejaVu Sans, sans-serif">
  <text x="20" y="30" font-size="13" fill="#555">สัญญาณดิบ (ทีละจุด) — มองไม่ออกว่าเกิดอะไร:</text>
  <polyline points="20,80 40,60 60,88 80,52 100,92 120,58 140,84 160,50 180,90 200,62 220,86 240,54 260,88 280,60 300,82" fill="none" stroke="#90a4ae" stroke-width="2"/>
  <rect x="360" y="44" width="280" height="56" rx="8" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="500" y="68" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">มองเป็น "ก้อน" (window)</text>
  <text x="500" y="88" font-size="11" fill="#666" text-anchor="middle">ถึงจะเห็นว่านี่คือ "เขย่า"</text>
  <line x1="300" y1="72" x2="356" y2="72" stroke="#607d8b" stroke-width="2.4"/>
</svg>
</div>

> นี่คือหลักเดียวกับหูคน: เราแยก "เสียงไอ" กับ "เสียงพูด" ไม่ได้จากคลื่นเสียง 1/1000 วินาที ต้องฟังทั้งช่วงถึงจะรู้ โมเดลก็เหมือนกัน

---

# ภาพเคลื่อนไหว — หน้าต่างเลื่อน (sliding window)

![ภาพเคลื่อนไหว: kernel ของ Conv1D ไถลไปตามสัญญาณทีละตำแหน่ง แล้วคูณรวมเป็นผลลัพธ์ y[t] w:760](../../assets/img/anim_conv1d.svg)

หน้าต่างเลื่อนทีละก้าว (stride) บีบ sample หลายจุดให้เป็น feature หนึ่งชุดที่โมเดลกินได้

---

# Windowing คืออะไร

**Windowing** คือการตัดสัญญาณที่ไหลมาเรื่อย ๆ ให้เป็นก้อนความยาวคงที่ (`WIN` จุด) ทีละก้อน แล้วประมวลผลทีละหน้าต่าง

<div style="text-align:center;margin:6px 0">
<svg width="880" height="180" viewBox="0 0 880 180" font-family="DejaVu Sans, sans-serif">
  <text x="20" y="24" font-size="12" fill="#555">สตรีมสัญญาณต่อเนื่อง →</text>
  <line x1="20" y1="60" x2="860" y2="60" stroke="#cfd8dc" stroke-width="2"/>
  <g font-size="10" fill="#90a4ae" text-anchor="middle">
    <circle cx="40" cy="60" r="3" fill="#90a4ae"/><circle cx="80" cy="60" r="3" fill="#90a4ae"/>
    <circle cx="120" cy="60" r="3" fill="#90a4ae"/><circle cx="160" cy="60" r="3" fill="#90a4ae"/>
    <circle cx="200" cy="60" r="3" fill="#90a4ae"/><circle cx="240" cy="60" r="3" fill="#90a4ae"/>
    <circle cx="280" cy="60" r="3" fill="#90a4ae"/><circle cx="320" cy="60" r="3" fill="#90a4ae"/>
  </g>
  <rect x="28" y="44" width="200" height="32" rx="6" fill="rgba(46,125,50,.15)" stroke="#2e7d32" stroke-width="2"/>
  <text x="128" y="66" font-size="11" fill="#2e7d32" text-anchor="middle">window 1 (WIN=50)</text>
  <rect x="128" y="86" width="200" height="32" rx="6" fill="rgba(21,101,192,.15)" stroke="#1565c0" stroke-width="2"/>
  <text x="228" y="108" font-size="11" fill="#1565c0" text-anchor="middle">window 2</text>
  <rect x="228" y="128" width="200" height="32" rx="6" fill="rgba(239,108,0,.15)" stroke="#ef6c00" stroke-width="2"/>
  <text x="328" y="150" font-size="11" fill="#e65100" text-anchor="middle">window 3</text>
  <line x1="128" y1="40" x2="128" y2="164" stroke="#b0bec5" stroke-width="1" stroke-dasharray="4 3"/>
  <line x1="228" y1="40" x2="228" y2="164" stroke="#b0bec5" stroke-width="1" stroke-dasharray="4 3"/>
  <text x="600" y="60" font-size="12" fill="#555">แต่ละหน้าต่างเลื่อนไปทีละ HOP=25 จุด</text>
  <text x="600" y="82" font-size="12" fill="#555">(ครึ่งหนึ่งของ WIN → ซ้อนกัน 50%)</text>
  <text x="600" y="110" font-size="11" fill="#888">ทุกหน้าต่าง → คำนวณ feature หนึ่งชุด</text>
</svg>
</div>

- `WIN = 50` — ยาวหนึ่งหน้าต่าง (1 วินาทีที่ 50 Hz)
- `HOP = 25` — เลื่อนหน้าต่างทีละ 25 จุด (ครึ่งหนึ่งของ WIN)
- ผลคือหน้าต่างซ้อนกัน 50% — เราจะได้ feature vector ชุดใหม่ทุก ๆ 25 จุด

> ค่าพวกนี้ไม่ได้ตั้งมั่ว โมเดลถูกฝึกมาด้วยขนาดหน้าต่างเท่าไร ตอนใช้งานจริงก็ต้อง feed หน้าต่างขนาดเดียวกัน ไม่งั้น "สิ่งที่โมเดลเห็น" จะไม่ตรงกับตอนฝึก

---

# ทำไมต้องซ้อน (overlap / hop)

ถ้าตัดหน้าต่างชนกันพอดี (hop = win) เหตุการณ์สั้น ๆ อาจตกร่องระหว่างหน้าต่างพอดีจนพลาด — การซ้อนช่วยไม่ให้พลาด

<div style="text-align:center;margin:6px 0">
<svg width="860" height="170" viewBox="0 0 860 170" font-family="DejaVu Sans, sans-serif">
  <!-- no overlap -->
  <text x="20" y="24" font-size="13" font-weight="700" fill="#c62828">ไม่ซ้อน (hop = win)</text>
  <rect x="20" y="34" width="150" height="28" rx="5" fill="rgba(46,125,50,.12)" stroke="#2e7d32"/>
  <rect x="172" y="34" width="150" height="28" rx="5" fill="rgba(21,101,192,.12)" stroke="#1565c0"/>
  <path d="M160,48 l8,-4 l0,8 z" fill="#c62828"/>
  <text x="168" y="80" font-size="11" fill="#c62828">เหตุการณ์สั้นตกร่องระหว่างหน้าต่าง → พลาด</text>
  <!-- overlap -->
  <text x="20" y="120" font-size="13" font-weight="700" fill="#2e7d32">ซ้อน 50% (hop = win/2)</text>
  <rect x="20" y="130" width="150" height="24" rx="5" fill="rgba(46,125,50,.12)" stroke="#2e7d32"/>
  <rect x="95" y="130" width="150" height="24" rx="5" fill="rgba(21,101,192,.12)" stroke="#1565c0"/>
  <rect x="170" y="130" width="150" height="24" rx="5" fill="rgba(239,108,0,.12)" stroke="#ef6c00"/>
  <text x="360" y="146" font-size="11" fill="#2e7d32">ทุกจุดถูกครอบด้วยหน้าต่างอย่างน้อยหนึ่งอัน → ไม่พลาด</text>
</svg>
</div>

- **ตอบไวขึ้น** — ได้ผลใหม่ทุก HOP จุด ไม่ต้องรอครบทั้งหน้าต่างใหม่
- **ไม่พลาดเหตุการณ์สั้น** — เสียงไอครั้งเดียว/ท่าปัดเร็ว ไม่หลุดร่องระหว่างหน้าต่าง
- แต่ซ้อนมาก = คำนวณบ่อยขึ้น = กินแรงขึ้น เป็นข้อแลกเปลี่ยนที่วิศวกรต้องเลือก

> hop เล็ก = ตอบไว แต่เปลือง · hop ใหญ่ = ประหยัด แต่ตอบช้าและอาจพลาด — เราเลือก 50% เป็นค่ากลางที่โมเดลเสียง/IMU ส่วนใหญ่ใช้

---

# Feature vector — บีบหน้าต่างเป็นตัวเลขไม่กี่ตัว

หน้าต่างหนึ่งมี 50 จุด แต่เราไม่ได้ป้อน 50 จุดนั้นตรง ๆ เข้าโมเดล เราบีบมันเป็น **feature vector** สั้น ๆ ที่สรุป "ลักษณะเด่น" ของหน้าต่างไว้

<div style="text-align:center;margin:6px 0">
<svg width="860" height="150" viewBox="0 0 860 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arFV" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="40" width="230" height="80" rx="10" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
  <text x="135" y="66" font-size="13" font-weight="700" fill="#455a64" text-anchor="middle">หน้าต่าง 50 จุด</text>
  <polyline points="40,100 55,84 70,108 85,78 100,110 115,86 130,104 145,80 160,108 175,88 190,102 205,82 220,106 235,90" fill="none" stroke="#90a4ae" stroke-width="1.6"/>
  <rect x="330" y="40" width="230" height="80" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="445" y="60" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">บีบ (feature extraction)</text>
  <text x="445" y="82" font-size="11" fill="#666" text-anchor="middle">mean · std</text>
  <text x="445" y="100" font-size="11" fill="#666" text-anchor="middle">พลังงาน 4 ย่าน</text>
  <rect x="640" y="40" width="200" height="80" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="740" y="66" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">feature vector</text>
  <text x="740" y="88" font-size="11" fill="#555" text-anchor="middle">[m, s, b0, b1, b2, b3]</text>
  <text x="740" y="106" font-size="10" fill="#888" text-anchor="middle">6 ตัว = สิ่งที่โมเดลเห็น</text>
  <line x1="250" y1="80" x2="326" y2="80" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arFV)"/>
  <line x1="560" y1="80" x2="636" y2="80" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arFV)"/>
</svg>
</div>

- 50 จุด → 6 ตัวเลข: **บีบข้อมูล** ให้เล็กลงมาก แต่เก็บลักษณะสำคัญไว้
- โมเดลเรียนรู้จาก 6 ตัวนี้ — ยิ่ง feature ดี โมเดลยิ่งเล็กและแม่นได้ (นี่คือหัวใจของ Edge AI)

> "โมเดลดีแค่ไหน ขึ้นกับ feature ที่ป้อนมันมากพอ ๆ กับตัวโมเดลเอง" — วิศวกร Edge AI ใช้เวลากับ feature front-end นี้เยอะกว่าที่คนคิด

---

# feature ที่เราคำนวณวันนี้

ตัวอย่างวันนี้บีบหนึ่งหน้าต่าง (แกน Z ของ accel) เป็น 6 ตัว สองกลุ่ม:

| feature | สูตร (ในโค้ด) | บอกอะไร |
|---|---|---|
| `mean` | `sum(win)/n` | ระดับ DC / ทิศแรงโน้มถ่วงของแกนนี้ |
| `std` | `sqrt(Σ(x-mean)²/n)` | **ความแรงของการสั่น** — นิ่ง=ต่ำ เขย่า=สูง |
| `band0..3` | variance ของแต่ละช่วงเวลา | การสั่นกระจุกอยู่ต้น/กลาง/ท้ายหน้าต่าง |

- `mean` กับ `std` เป็น feature **เชิงสถิติ** ของทั้งหน้าต่าง — เบา คำนวณเร็ว แต่ทรงพลัง
- `band0..3` แบ่งหน้าต่างเป็น 4 ช่วงเวลาแล้ววัด variance แต่ละช่วง — จับ "รูปร่างตามเวลา" ได้หยาบ ๆ

> `std` ตัวเดียวแยก "นิ่ง/ขยับ" ได้เกือบหมดแล้ว — ในฉบับเต็มเราเอา `std` มาตัดสิน "นิ่ง/ขยับ" ตรง ๆ เป็นตัวอย่างของ "การจำแนกคลาสเวอร์ชันมือทำ"

---

# std คือหัวใจ — ทำไม variance ถึงเล่าเรื่องได้

`std` (ส่วนเบี่ยงเบนมาตรฐาน) วัดว่าสัญญาณ "แกว่ง" ห่างจากค่าเฉลี่ยแค่ไหน — มันคือรากของ variance ที่เราเจอมาตั้งแต่โมดูล 3 (Processing)

$$\mathrm{std} = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^2}$$

- บอร์ดวางนิ่ง: ทุกจุดใกล้ค่าเฉลี่ย → `std` เล็ก
- เขย่าบอร์ด: จุดกระจายห่างค่าเฉลี่ย → `std` ใหญ่
- นี่คือเหตุผลที่ feature เชิงสถิติง่าย ๆ แยกท่าทางได้ดีอย่างน่าประหลาดใจ

<div style="text-align:center;margin:6px 0">
<svg width="780" height="110" viewBox="0 0 780 110" font-family="DejaVu Sans, sans-serif">
  <text x="20" y="24" font-size="12" fill="#2e7d32" font-weight="700">นิ่ง → std ต่ำ</text>
  <line x1="20" y1="60" x2="360" y2="60" stroke="#cfd8dc"/>
  <polyline points="20,60 50,58 80,62 110,59 140,61 170,58 200,62 230,60 260,59 290,61 320,60 350,60" fill="none" stroke="#2e7d32" stroke-width="2"/>
  <text x="420" y="24" font-size="12" fill="#c62828" font-weight="700">เขย่า → std สูง</text>
  <line x1="420" y1="60" x2="760" y2="60" stroke="#cfd8dc"/>
  <polyline points="420,60 450,30 480,86 510,34 540,84 570,32 600,88 630,36 660,82 690,30 720,86 750,60" fill="none" stroke="#c62828" stroke-width="2"/>
</svg>
</div>

> จำ variance จากบทเรียน Processing (บทเรียน 3.1–3.2) ได้ไหม — วันนี้เราเอามันกลับมาใช้เป็น feature โดยตรง แนวคิดเก่าไม่เคยหายไป มันแค่เปลี่ยนบทบาท

---

# band energy — ญาติหยาบ ๆ ของ spectrogram

`band0..3` แบ่งหน้าต่างเป็น 4 ช่วง**เวลา** แล้ววัดพลังงาน (variance) แต่ละช่วง — จับได้ว่าการสั่นแรงตอนไหนของหน้าต่าง

- ถ้าการปัดมือเกิดตอนต้นหน้าต่าง → `band0` แรง, `band3` เบา
- ถ้าเป็นการสั่นสม่ำเสมอ → ทุก band ใกล้กัน
- นี่คือ "รูปร่างตามเวลา" แบบหยาบ — โมเดลใช้แยกท่าที่มี pattern เวลาต่างกันได้

> ในโลกจริงของ **เสียง** เราไม่แบ่งตามเวลาอย่างเดียว เราแบ่งตาม **ความถี่** (เอา FFT จาก บทเรียน 4.3–4.4 มาจัดเป็นย่าน) — นั่นแหละคือ mel spectrogram ที่หน้าถัดไปจะเล่า

---

# สิ่งที่โมเดลเสียงเห็นจริง — mel / log-mel spectrogram

โมเดลเสียงบนบอร์ด (Baby Cry, Cough, Alarm, Siren) ไม่ได้กินคลื่นเสียงดิบ มันกิน **spectrogram** — ภาพความถี่ต่อเวลา

<div style="text-align:center;margin:6px 0">
<svg width="900" height="170" viewBox="0 0 900 170" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arMel" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="50" width="150" height="70" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="89" y="80" font-size="12" font-weight="700" fill="#1565c0" text-anchor="middle">เสียงดิบ</text>
  <text x="89" y="100" font-size="10" fill="#888" text-anchor="middle">PDM / PCM</text>
  <rect x="200" y="50" width="150" height="70" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="275" y="74" font-size="12" font-weight="700" fill="#2e7d32" text-anchor="middle">ตัดหน้าต่าง</text>
  <text x="275" y="94" font-size="10" fill="#888" text-anchor="middle">win + hop</text>
  <text x="275" y="110" font-size="10" fill="#888" text-anchor="middle">(เหมือนวันนี้)</text>
  <rect x="386" y="50" width="150" height="70" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="461" y="74" font-size="12" font-weight="700" fill="#e65100" text-anchor="middle">FFT ต่อหน้าต่าง</text>
  <text x="461" y="94" font-size="10" fill="#888" text-anchor="middle">พลังงานต่อความถี่</text>
  <text x="461" y="110" font-size="10" fill="#888" text-anchor="middle">(4.3–4.4)</text>
  <rect x="572" y="50" width="150" height="70" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="647" y="74" font-size="12" font-weight="700" fill="#6a1b9a" text-anchor="middle">จัดเป็น mel band</text>
  <text x="647" y="94" font-size="10" fill="#888" text-anchor="middle">รวมเป็นไม่กี่ย่าน</text>
  <text x="647" y="110" font-size="10" fill="#888" text-anchor="middle">+ log</text>
  <rect x="758" y="50" width="130" height="70" rx="10" fill="#e0f7fa" stroke="#00838f" stroke-width="2"/>
  <text x="823" y="80" font-size="12" font-weight="700" fill="#00838f" text-anchor="middle">spectrogram</text>
  <text x="823" y="100" font-size="10" fill="#888" text-anchor="middle">= input โมเดล</text>
  <line x1="164" y1="85" x2="196" y2="85" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arMel)"/>
  <line x1="350" y1="85" x2="382" y2="85" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arMel)"/>
  <line x1="536" y1="85" x2="568" y2="85" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arMel)"/>
  <line x1="722" y1="85" x2="754" y2="85" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arMel)"/>
  <text x="450" y="150" font-size="11" fill="#888" text-anchor="middle">โครงเดียวกับที่เราทำวันนี้ ต่างแค่ "ย่าน" เป็นความถี่ (mel) แทนเวลา และมี log</text>
</svg>
</div>

- **mel band** = จัดกลุ่มความถี่ให้ตรงกับที่หูคนได้ยิน (ความถี่ต่ำละเอียด ความถี่สูงหยาบ)
- **log** = บีบช่วง dynamic range ให้เสียงเบา/ดังอยู่ในสเกลใกล้กัน
- แต่แกนหลักเหมือนกันเป๊ะ: **window → transform → รวมเป็นย่าน → นั่นคือ input ของโมเดล**

> วันนี้เราทำเวอร์ชัน IMU ที่เห็นด้วยตาง่ายกว่า แต่พอเข้าใจ "window → feature" แล้ว spectrogram ของเสียงก็คือเรื่องเดียวกัน แค่ย่านเป็นความถี่

---

# คณิตของหน้าต่าง — Hann window

ก่อนเอาหน้าต่างไปทำ FFT เราไม่ตัดขอบตรง ๆ แต่ค่อย ๆ **ลดขอบให้เรียบ** ด้วยตัวคูณรูประฆังที่ชื่อ Hann window:

$$w[n] = 0.5 - 0.5\cos\!\left(\frac{2\pi n}{N-1}\right)$$

อ่านสัญลักษณ์ทีละตัวแบบง่าย ๆ:

- $n$ — ลำดับจุดในหน้าต่าง เริ่มที่ $0$ ไปจนถึง $N-1$
- $N$ — จำนวนจุดทั้งหน้าต่าง (เช่น `WIN = 50`)
- $w[n]$ — ตัวคูณของจุดที่ $n$ มีค่าอยู่ระหว่าง $0$ (ที่ขอบสองข้าง) ถึง $1$ (ตรงกลาง)

ค่าที่ได้: ขอบซ้าย $w[0]=0$ · กลางหน้าต่าง $w \approx 1$ · ขอบขวา $w[N-1]=0$ — เหมือนกดเสียงให้เบาลงตอนต้นและปลาย

<div style="text-align:center;margin:8px 0">
<svg width="720" height="140" viewBox="0 0 720 140" font-family="DejaVu Sans, sans-serif">
  <line x1="40" y1="110" x2="700" y2="110" stroke="#cfd8dc" stroke-width="1.5"/>
  <line x1="40" y1="20" x2="40" y2="110" stroke="#cfd8dc" stroke-width="1.5"/>
  <text x="30" y="26" font-size="11" fill="#888" text-anchor="end">1</text>
  <text x="30" y="112" font-size="11" fill="#888" text-anchor="end">0</text>
  <text x="40" y="128" font-size="11" fill="#888" text-anchor="middle">n=0</text>
  <text x="700" y="128" font-size="11" fill="#888" text-anchor="middle">n=N-1</text>
  <path d="M40,110 C 200,110 240,22 370,22 C 500,22 540,110 700,110" fill="none" stroke="#6a1b9a" stroke-width="3"/>
  <text x="370" y="16" font-size="12" fill="#6a1b9a" text-anchor="middle" font-weight="700">w[n] — รูประฆัง Hann</text>
</svg>
</div>

> **ทำไมสำคัญกับชุดบทเรียนนี้:** ตอนตัดหน้าต่างแข็ง ๆ ขอบที่ขาดกระทันหันจะสร้างความถี่ปลอมใน FFT (เรียก spectral leakage) พอคูณ Hann ให้ขอบค่อย ๆ จางลง สเปกตรัมสะอาดขึ้น — mel spectrogram ของเสียงทุกตัวบนบอร์ดใช้ trick นี้ก่อนทำ FFT เสมอ

---

# คณิตของ spectrogram — log-mel

รวมทุกอย่างในหน้าที่แล้วเป็นสูตรเดียว คือสิ่งที่โมเดลเสียง "เห็น" จริง ๆ:

$$\text{logmel} = \log\Big(\,\mathrm{Mel}\big(\,\lvert\,\mathrm{FFT}(x \cdot w)\,\rvert\,\big)\Big)$$

ไล่จากในสุดออกมานอกสุด — อ่านเหมือนสายพาน:

- $x \cdot w$ — สัญญาณหนึ่งหน้าต่าง $x$ คูณ Hann window $w$ (ลดขอบให้เรียบก่อน)
- $\mathrm{FFT}(\cdot)$ — แปลงไปโดเมนความถี่ (ของ บทเรียน 4.3–4.4) ได้พลังงานต่อความถี่
- $\lvert\cdot\rvert$ — เอาขนาด (magnitude) ทิ้งเฟส เหลือแค่ "แต่ละความถี่แรงแค่ไหน"
- $\mathrm{Mel}(\cdot)$ — รวมความถี่เป็นไม่กี่ย่านตามสเกลการได้ยินของหู (ต่ำละเอียด สูงหยาบ)
- $\log(\cdot)$ — บีบช่วง dynamic range ให้เสียงเบากับดังอยู่สเกลใกล้กัน

<div style="text-align:center;margin:6px 0">
<svg width="860" height="86" viewBox="0 0 860 86" font-family="DejaVu Sans, sans-serif">
  <defs><marker id="arLM" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="9" refX="9" refY="4" orient="auto"><path d="M0,0 L9,4 L0,8 Z" fill="#607d8b"/></marker></defs>
  <g text-anchor="middle" font-size="12" font-weight="700">
    <rect x="8" y="26" width="120" height="40" rx="8" fill="#e3f2fd" stroke="#1565c0"/><text x="68" y="51" fill="#1565c0">x · w</text>
    <rect x="176" y="26" width="120" height="40" rx="8" fill="#e8f5e9" stroke="#2e7d32"/><text x="236" y="51" fill="#2e7d32">FFT</text>
    <rect x="344" y="26" width="120" height="40" rx="8" fill="#fff3e0" stroke="#ef6c00"/><text x="404" y="51" fill="#e65100">| · |</text>
    <rect x="512" y="26" width="120" height="40" rx="8" fill="#f3e5f5" stroke="#6a1b9a"/><text x="572" y="51" fill="#6a1b9a">Mel</text>
    <rect x="680" y="26" width="120" height="40" rx="8" fill="#e0f7fa" stroke="#00838f"/><text x="740" y="51" fill="#00838f">log</text>
  </g>
  <line x1="128" y1="46" x2="174" y2="46" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arLM)"/>
  <line x1="296" y1="46" x2="342" y2="46" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arLM)"/>
  <line x1="464" y1="46" x2="510" y2="46" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arLM)"/>
  <line x1="632" y1="46" x2="678" y2="46" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arLM)"/>
</svg>
</div>

> **ทำไมสำคัญกับชุดบทเรียนนี้:** `band0..3` ที่เราทำวันนี้คือรุ่นย่อของสูตรนี้ — เราแบ่งเป็นย่าน**เวลา**และวัด variance ส่วนเสียงแบ่งเป็นย่าน**ความถี่** (Mel) แล้วใส่ log แค่นั้น โครง `window → transform → รวมย่าน` อันเดียวกันเป๊ะ

---

# สิ่งที่โมเดลเห็น = feature vector ไม่ใช่สัญญาณดิบ

จับใจความสำคัญที่สุดของชุดบทเรียนนี้ให้แน่น:

<div style="text-align:center;margin:14px 0">
<div style="display:inline-block;background:#fff3e0;border:2px solid #ef6c00;border-radius:16px;padding:12px 24px;color:#e65100;font-weight:700;font-size:1.05em">
โมเดลไม่เคยเห็นสัญญาณดิบ · มันเห็นแต่ feature vector ที่ front-end บีบมาให้
</div>
</div>

- ตอน **ฝึก** (Training): dataset ก็คือชุดของ feature vector แบบนี้ พร้อม label
- ตอน **ใช้งาน** (Apps): front-end บนบอร์ดบีบสัญญาณสดเป็น feature vector ชุดเดียวกัน แล้วป้อนโมเดล
- ถ้า front-end ตอนฝึกกับตอนใช้ **ไม่ตรงกัน** โมเดลจะเพี้ยนทันที — นี่คือบั๊กคลาสสิกของ Edge AI

> เพราะฉะนั้นการเข้าใจ feature front-end จึงสำคัญพอ ๆ กับตัวโมเดล — ชุดบทเรียนนี้คือรากฐานที่ทำให้โมดูล 5 (Training) ไม่ใช่กล่องดำ

---

# รู้จักคำสั่งที่ใช้ในไฟล์วันนี้

ไฟล์ตัวอย่างใช้ของที่เราคุ้นแล้ว บวก `math` เข้ามาช่วยคำนวณ:

| คำสั่ง | ทำอะไร |
|---|---|
| `sensors.bmi270.motion()` | คืน `(ax,ay,az,gx,gy,gz)` — เราใช้ `az` เป็นสัญญาณ |
| `math.sqrt(x)` | รากที่สอง (สำหรับ `std`) |
| `ui.Bar(...)` / `.value(v)` | แท่งแสดงค่า feature แต่ละตัว |
| `ui.Label(...)` / `.text(s)` | ป้ายชื่อ feature + ตัวนับหน้าต่าง |
| `lcd.console(...)` | พิมพ์ feature vector เป็นข้อความ (ดูค่าจริง) |
| `time.sleep_ms(20)` | เว้นจังหวะให้ได้อัตราสุ่ม 50 Hz |

- ไม่มีคำสั่งใหม่แปลก ๆ — ชุดบทเรียนนี้ความยากอยู่ที่ **แนวคิด** (window/feature) ไม่ใช่ API
- ทุกอย่างเป็น pure Python บน CM33 ไม่ต้องพึ่ง NPU เลย

> `sensors.bmi270.motion()` คืน 6 ค่า เราแตกเป็น `ax,ay,az,gx,gy,gz` แล้วหยิบแค่ `az` มาทำสัญญาณตัวอย่าง — แกนอื่นทำแบบเดียวกันได้หมด
