---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 2.1 — สุ่มสัญญาณให้ตรงกับโมเดล: อัตราสุ่ม Nyquist หน้าต่าง และ schema ของ CSV"
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

# บทเรียน 2.1 — สุ่มสัญญาณให้ตรงกับโมเดล: อัตราสุ่ม Nyquist หน้าต่าง และ schema ของ CSV
## สุ่มสัญญาณเซนเซอร์แล้วเก็บเป็นไฟล์ของเราเอง

**โมดูล 2 — เก็บข้อมูลจากเซนเซอร์ (DAQ)**

**Pillar 1 — Data Acquisition (เริ่มไล่วงจรจากต้นน้ำ)**

> คาถาประจำบทเรียน: **"โมเดลทุกตัวเกิดจากข้อมูลที่มีคนเก็บมาก่อน — วันนี้เราเป็นคนเก็บเอง แล้วจะเห็นว่า dataset ไม่ใช่ของวิเศษ มันคือไฟล์ CSV ที่เราเขียนทีละบรรทัด"**

MicroPython บนบอร์ด BENTO (PSoC Edge · Cortex-M55 + Ethos-U55 NPU)

---

# เปิดบทเรียนด้วยของจริงก่อน

เหมือนทุกบทเรียน เราเริ่มแบบ **กลับด้าน** — รันของที่ทำงานได้จริงก่อน แล้วค่อยแกะว่ามันทำงานยังไง

<div style="text-align:center;margin:10px 0">
<svg width="820" height="150" viewBox="0 0 820 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arOpen" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="40" width="180" height="70" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="104" y="72" font-size="15" font-weight="700" fill="#2e7d32" text-anchor="middle">รัน logger ก่อน</text>
  <text x="104" y="94" font-size="12" fill="#555" text-anchor="middle">เก็บท่า -> CSV</text>
  <rect x="234" y="40" width="180" height="70" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="324" y="72" font-size="15" font-weight="700" fill="#1565c0" text-anchor="middle">แกะดูข้างใน</text>
  <text x="324" y="94" font-size="12" fill="#555" text-anchor="middle">rate · schema · file</text>
  <rect x="454" y="40" width="180" height="70" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="544" y="72" font-size="15" font-weight="700" fill="#e65100" text-anchor="middle">เติม/แก้เอง</text>
  <text x="544" y="94" font-size="12" fill="#555" text-anchor="middle">4 จังหวะหลัก</text>
  <rect x="674" y="40" width="132" height="70" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="740" y="72" font-size="15" font-weight="700" fill="#6a1b9a" text-anchor="middle">เอาไป train</text>
  <text x="740" y="94" font-size="12" fill="#555" text-anchor="middle">บทเรียน 5.1–5.2+</text>
  <line x1="194" y1="75" x2="230" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="414" y1="75" x2="450" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="634" y1="75" x2="670" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
</svg>
</div>

วันนี้ "ของเจ๋ง" ไม่ใช่โมเดลที่รู้จำท่าทาง แต่เป็น **ไฟล์ CSV ไฟล์แรกของเราเอง** ที่เต็มไปด้วยตัวเลขจากเซนเซอร์จริง เปิดหน้าจอ กดปุ่ม `shaking` เขย่าบอร์ด แล้วดูตัวเลข samples วิ่งขึ้น — นั่นคือ dataset กำลังก่อตัวอยู่ตรงหน้า

> ชุดบทเรียนนี้ยังไม่ต้อง train อะไรทั้งนั้น ขอแค่ได้เห็นว่า "ข้อมูลที่โมเดลกิน" หน้าตาเป็นยังไง และมันมาจากมือเราเองได้ยังไง เท่านั้นพอ

---

# เป้าหมายของชุดบทเรียนนี้

จบชุดบทเรียนนี้เราจะเข้าใจ 4 เรื่องของ **DAQ (Data Acquisition)** แล้วปิดท้ายด้วยไฟล์ dataset จริง:

1. **DAQ คืออะไร** และทำไมข้อมูลต้องมาก่อนโมเดลเสมอ
2. **อัตราสุ่ม (sampling rate)** — Hz คืออะไร ทำไมต้องคงที่ และทำไมต้องตรงกับที่โมเดลกิน
3. **schema ของ CSV** — หนึ่งบรรทัดต่อหนึ่ง sample: `label,ax,ay,az,gx,gy,gz`
4. **เขียนลงไฟล์บนบอร์ด** — dataset อยู่บน flash ของอุปกรณ์เอง

ปลายทางของวันนี้: กดปุ่ม label ทำท่าค้างไว้ ระบบเก็บ 200 samples/ครั้งลง `/gestures.csv` — ครบทุกท่าแล้วได้ dataset พร้อม train

> เรากำลังเดินถอยจากปลายน้ำ (บทเรียน 1.1–1.3 และ 1.6–1.7 รันโมเดลสำเร็จรูป) มาที่ **ต้นน้ำ** — ที่ซึ่งข้อมูลเกิดขึ้นจริง นี่คือ Pillar 1 ของทั้งวงจร

---

# ชุดบทเรียนนี้อยู่ตรงไหนของวงจร

จำวงจร 5 ขั้นจากบทเรียน 1.1–1.3 ได้ไหม — DAQ → Processing → Analysis → Training → Apps เราเริ่มจากขั้น **Apps** (ปลายน้ำ) มาสามชุดบทเรียน วันนี้ถอยกลับมาที่ขั้น **1 · DAQ** (ต้นน้ำ)

<div style="text-align:center;margin:6px 0">
<svg width="920" height="180" viewBox="0 0 920 180" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arLC" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g text-anchor="middle">
    <rect x="10" y="52" width="160" height="76" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="3"/>
    <text x="90" y="80" font-size="14" font-weight="700" fill="#1565c0">1 · DAQ</text>
    <text x="90" y="100" font-size="11" fill="#555">เก็บข้อมูลดิบ</text>
    <text x="90" y="116" font-size="10" fill="#c62828">เราอยู่ตรงนี้</text>
    <rect x="196" y="52" width="160" height="76" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="276" y="80" font-size="14" font-weight="700" fill="#2e7d32">2 · Processing</text>
    <text x="276" y="100" font-size="11" fill="#555">คณิต+ฟิสิกส์</text>
    <rect x="382" y="52" width="160" height="76" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="462" y="80" font-size="14" font-weight="700" fill="#e65100">3 · Analysis</text>
    <text x="462" y="100" font-size="11" fill="#555">DSP · FFT · feature</text>
    <rect x="568" y="52" width="160" height="76" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
    <text x="648" y="80" font-size="14" font-weight="700" fill="#6a1b9a">4 · Training</text>
    <text x="648" y="100" font-size="11" fill="#555">ฝึกโมเดล</text>
    <rect x="754" y="52" width="160" height="76" rx="12" fill="#e0f7fa" stroke="#00838f" stroke-width="2"/>
    <text x="834" y="80" font-size="14" font-weight="700" fill="#00838f">5 · Apps</text>
    <text x="834" y="100" font-size="11" fill="#555">1.1–1.3 · 1.6–1.7 (มาแล้ว)</text>
  </g>
  <line x1="170" y1="90" x2="194" y2="90" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <line x1="356" y1="90" x2="380" y2="90" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <line x1="542" y1="90" x2="566" y2="90" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <line x1="728" y1="90" x2="752" y2="90" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arLC)"/>
  <path d="M834,50 C834,20 90,20 90,48" fill="none" stroke="#9e9e9e" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arLC)"/>
  <text x="462" y="24" font-size="12" fill="#9e9e9e" text-anchor="middle">"กลับด้าน" — เห็นปลายน้ำก่อน (Apps) แล้วถอยมาต้นน้ำ (DAQ)</text>
  <text x="462" y="160" font-size="12" fill="#888" text-anchor="middle">บทเรียน 2.1–2.2–2.3–2.4 = Pillar 1 · จากนี้เราจะไล่ขึ้นทีละขั้นจนฝึกโมเดลของตัวเองได้</text>
</svg>
</div>

> ทำไมถอยมาต้นน้ำตอนนี้? เพราะจะเข้าใจว่าโมเดล "เห็นอะไร" ต้องเริ่มจากการเป็นคนป้อนข้อมูลให้มันเองก่อน — ชุดบทเรียนนี้คือก้าวแรกของการเป็นเจ้าของ dataset

---

# DAQ คืออะไร — ทำไมข้อมูลมาก่อนโมเดล

**DAQ (Data Acquisition)** คือการ **เก็บข้อมูลดิบจากเซนเซอร์** ให้เป็นชุดที่จัดเก็บได้ ค้นได้ เอาไปใช้ต่อได้ — นี่คือวัตถุดิบตั้งต้นของทุกโมเดล

- โมเดล Motion ที่เราเล่นในบทเรียน 1.1–1.3 (idle / circle / shaking) ไม่ได้เกิดมาลอยๆ มีคน **เขย่าเซนเซอร์แล้วเก็บตัวเลขไว้** เป็นพันๆ sample ก่อน แล้วจึงเอาไป train
- ถ้าไม่มีขั้นนี้ ก็ไม่มีอะไรให้โมเดลเรียนรู้ — DAQ จึงเป็น **ขั้นที่ 1** เสมอ ไม่ใช่เรื่องรอง
- วันนี้เราทำสิ่งเดียวกับที่ทีมสร้างโมเดลจริงทำ: เลือกท่า ตั้งชื่อ (label) แล้วอัดข้อมูลลงไฟล์

<div style="text-align:center;margin:8px 0">
<svg width="820" height="120" viewBox="0 0 820 120" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arDAQ" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="38" width="150" height="52" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="95" y="60" font-size="12" font-weight="700" fill="#1565c0" text-anchor="middle">เซนเซอร์จริง</text>
  <text x="95" y="78" font-size="10" fill="#666" text-anchor="middle">IMU 6 แกน</text>
  <rect x="240" y="38" width="150" height="52" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="315" y="60" font-size="12" font-weight="700" fill="#e65100" text-anchor="middle">สุ่มที่อัตราคงที่</text>
  <text x="315" y="78" font-size="10" fill="#666" text-anchor="middle">50 ครั้ง/วินาที</text>
  <rect x="460" y="38" width="150" height="52" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="535" y="60" font-size="12" font-weight="700" fill="#2e7d32" text-anchor="middle">ติด label</text>
  <text x="535" y="78" font-size="10" fill="#666" text-anchor="middle">"shaking"</text>
  <rect x="680" y="38" width="120" height="52" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="740" y="60" font-size="12" font-weight="700" fill="#6a1b9a" text-anchor="middle">CSV บนบอร์ด</text>
  <text x="740" y="78" font-size="10" fill="#666" text-anchor="middle">dataset</text>
  <line x1="170" y1="64" x2="236" y2="64" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arDAQ)"/>
  <line x1="390" y1="64" x2="456" y2="64" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arDAQ)"/>
  <line x1="610" y1="64" x2="676" y2="64" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arDAQ)"/>
</svg>
</div>

> "DAQ" เป็นคำที่วิศวกรใช้จริงในสายวัดคุม/instrumentation มานานก่อนยุค AI — หัวใจเหมือนเดิม: **อ่านสัญญาณให้ถูกจังหวะ แล้วเก็บให้ครบถ้วนตรงเวลา**

---

# Garbage in, garbage out — คุณภาพของ dataset

มีคำพูดในวงการ ML ที่จริงเสมอ: **"ข้อมูลเข้าเป็นขยะ ผลออกก็เป็นขยะ"** โมเดลเก่งแค่ไหนก็แพ้ dataset ที่เก็บมั่ว

- **ติด label ถูก** — ถ้ากดปุ่ม `shaking` แต่ดันวางบอร์ดนิ่ง ข้อมูลนั้นจะสอนโมเดลผิด
- **อัตราคงที่** — ถ้าสุ่มเดี๋ยวเร็วเดี๋ยวช้า รูปคลื่นจะบิด โมเดลจะสับสน
- **เก็บพอๆ กันทุกคลาส (class balance)** — ถ้าเก็บ `idle` 1000 แต่ `shaking` 50 โมเดลจะเอนไปทาย idle
- **สภาพจริงหลากหลาย** — เขย่าแรง/เบา เร็ว/ช้า มือคนละคน ยิ่งหลากหลาย โมเดลยิ่งทน

> ชุดบทเรียนนี้เราจะลงมือเก็บจริง แล้วคุณจะรู้สึกเองว่า "การเก็บข้อมูลดีๆ ก็เป็นงานฝีมือ" — ไม่ใช่แค่กดปุ่มมั่วๆ นี่คือเหตุผลที่ dataset ดีมีค่า

---

# อัตราสุ่ม (sampling rate) คืออะไร

**อัตราสุ่ม** คือ "จำนวนครั้งที่เราอ่านเซนเซอร์ต่อวินาที" หน่วยเป็น **เฮิรตซ์ (Hz)** — 50 Hz แปลว่าอ่าน 50 ครั้งใน 1 วินาที คือทุกๆ 20 มิลลิวินาที

<div style="text-align:center;margin:6px 0">
<svg width="840" height="170" viewBox="0 0 840 170" font-family="DejaVu Sans, sans-serif">
  <!-- continuous wave -->
  <path d="M40,80 Q90,20 140,80 T240,80 T340,80 T440,80 T540,80 T640,80 T740,80" fill="none" stroke="#90caf9" stroke-width="2.5"/>
  <text x="40" y="30" font-size="12" fill="#1565c0">สัญญาณจริง (ต่อเนื่อง)</text>
  <!-- sample dots -->
  <g fill="#c62828">
    <circle cx="40" cy="80" r="4"/><circle cx="90" cy="50" r="4"/><circle cx="140" cy="80" r="4"/><circle cx="190" cy="110" r="4"/>
    <circle cx="240" cy="80" r="4"/><circle cx="290" cy="50" r="4"/><circle cx="340" cy="80" r="4"/><circle cx="390" cy="110" r="4"/>
    <circle cx="440" cy="80" r="4"/><circle cx="490" cy="50" r="4"/><circle cx="540" cy="80" r="4"/><circle cx="590" cy="110" r="4"/>
    <circle cx="640" cy="80" r="4"/><circle cx="690" cy="50" r="4"/><circle cx="740" cy="80" r="4"/>
  </g>
  <g stroke="#c62828" stroke-width="1" stroke-dasharray="3 3">
    <line x1="40" y1="80" x2="40" y2="150"/><line x1="90" y1="50" x2="90" y2="150"/><line x1="140" y1="80" x2="140" y2="150"/>
  </g>
  <text x="65" y="165" font-size="11" fill="#c62828" text-anchor="middle">20 ms</text>
  <path d="M40,150 L90,150" stroke="#c62828" stroke-width="1" marker-end="url(#arDAQ2)"/>
  <defs><marker id="arDAQ2" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#c62828"/></marker></defs>
  <text x="420" y="145" font-size="12" fill="#c62828" text-anchor="middle">แต่ละจุดแดง = หนึ่ง sample ที่เราเก็บ (ทุก 20 ms = 50 Hz)</text>
</svg>
</div>

- เราไม่ได้เก็บ "ทุกช่วงเวลา" แต่เก็บเป็น **จุดๆ ที่ระยะเท่าๆ กัน** — เอาจุดพวกนี้มาเรียงกันก็เห็นเป็นรูปคลื่น
- สุ่มถี่ (Hz สูง) = เก็บรายละเอียดได้มาก แต่ไฟล์ใหญ่และกินแรง · สุ่มห่าง (Hz ต่ำ) = ประหยัด แต่พลาดรายละเอียดเร็วๆ

> กฎง่ายๆ: ถ้าจะจับสัญญาณที่แกว่งเร็วแค่ไหน ต้องสุ่มให้ถี่กว่านั้นอย่างน้อยเท่าตัว (เดี๋ยวเรื่อง FFT ในโมดูล 4 (Analysis) จะเจาะลึกกฎนี้)

---

# ทำไมต้อง 50 Hz — ต้องตรงกับที่โมเดลกิน

ในไฟล์เราตั้ง `RATE_MS = 20` ซึ่งคือ **50 Hz** ไม่ใช่เลขสุ่ม แต่เลือกให้ **ตรงกับอัตราที่โมเดล Motion บนบอร์ดกินจริง**

```python
RATE_MS = 20            # 50 Hz — ตรงกับอัตราที่โมเดล Motion บนบอร์ดกิน
BURST   = 200           # 200 sample = ~4 วินาที ที่ 50 Hz
```

- โมเดลถูก train มาบนข้อมูล 50 Hz ถ้าเราเก็บที่อัตราอื่น (เช่น 10 Hz) รูปคลื่นจะ "ยืด/หด" ไม่เหมือนที่โมเดลเคยเห็น
- นี่คือหลักสำคัญของ Edge AI: **อัตราสุ่มตอนเก็บข้อมูล ต้องเท่ากับตอนใช้งานจริง** ไม่งั้น dataset สวยแค่ไหนก็ใช้ไม่ได้
- `BURST = 200` เลือกให้หนึ่งครั้งที่กดปุ่ม ได้ข้อมูล ~4 วินาที — ยาวพอให้ทำท่าได้เต็มรอบ

> จำเลข 20 ms นี้ไว้ให้ดี — ในบทเรียน 1.1–1.3 เราเคยเห็น `edge_ai` อ่านผลทุก ~180 ms แต่ **การป้อนข้อมูลให้โมเดล** ต้องถี่กว่านั้นมาก เพราะโมเดลต้องเห็นรูปคลื่นละเอียด

---

# คณิตเบื้องหลัง (1) — กฎ Nyquist

ทำไมต้องสุ่ม "เร็วกว่าสองเท่า" ของสัญญาณที่อยากจับ? มีกฎคณิตศาสตร์รองรับ เรียกว่า **กฎการสุ่มของ Nyquist–Shannon**:

$$ f_s \;\ge\; 2\,f_{max} $$

อ่านสัญลักษณ์ทีละตัวแบบง่ายๆ:

- $f_s$ = **อัตราสุ่ม** (sampling rate) หน่วย Hz — จำนวนครั้งที่เราอ่านเซนเซอร์ต่อวินาที (ในไฟล์เราคือ 50)
- $f_{max}$ = **ความถี่สูงสุด** ในสัญญาณที่เราอยากจับได้ หน่วย Hz — เช่น การเขย่ามือเร็วสุดราว 5–10 Hz
- $\ge 2$ = ต้องสุ่มให้ถี่ **อย่างน้อยสองเท่า** ของ $f_{max}$ ไม่งั้นเก็บรูปคลื่นไม่ครบ

<div style="text-align:center;margin:6px 0">
<svg width="820" height="150" viewBox="0 0 820 150" font-family="DejaVu Sans, sans-serif">
  <path d="M40,80 Q110,10 180,80 T320,80 T460,80 T600,80 T740,80" fill="none" stroke="#90caf9" stroke-width="2.5"/>
  <g fill="#c62828">
    <circle cx="40" cy="80" r="5"/><circle cx="110" cy="16" r="5"/><circle cx="180" cy="80" r="5"/><circle cx="250" cy="144" r="5"/>
    <circle cx="320" cy="80" r="5"/><circle cx="390" cy="16" r="5"/><circle cx="460" cy="80" r="5"/><circle cx="530" cy="144" r="5"/>
    <circle cx="600" cy="80" r="5"/><circle cx="670" cy="16" r="5"/><circle cx="740" cy="80" r="5"/>
  </g>
  <text x="410" y="16" font-size="12" fill="#1565c0" text-anchor="middle">คลื่นหนึ่งลูก (หนึ่ง cycle) ต้องมีจุดแดงเก็บอย่างน้อย 2 จุด ถึงจะรู้ว่ามันแกว่ง</text>
</svg>
</div>

> ถ้าสุ่มช้ากว่าเกณฑ์นี้ สัญญาณเร็วจะ "แปลงร่าง" กลายเป็นคลื่นช้าปลอมๆ เรียกว่า **aliasing** — dataset จะโกหกโดยที่เราไม่รู้ตัว นี่คือเหตุผลลึกๆ ที่ชุดบทเรียนนี้ย้ำเรื่องอัตราสุ่มคงที่

---

# คณิตเบื้องหลัง (2) — ความยาวหน้าต่าง (window)

รู้อัตราสุ่มแล้ว คำนวณต่อได้เลยว่า หนึ่ง burst ที่เก็บ $N$ sample กินเวลากี่วินาที:

$$ T \;=\; \frac{N}{f_s} $$

- $T$ = **ความยาวเวลา** ของหนึ่ง burst (หนึ่งหน้าต่าง/window) หน่วยวินาที
- $N$ = **จำนวน sample** ที่เก็บต่อหนึ่งครั้ง — ในไฟล์เราคือ `BURST = 200`
- $f_s$ = อัตราสุ่ม = 50 Hz

แทนค่าจริงของชุดบทเรียนนี้:

$$ T \;=\; \frac{200}{50} \;=\; 4 \ \text{วินาที} $$

นี่คือที่มาของ "~4 วินาที" ที่พูดถึงตอนเลือก `BURST`. ลองสังเกต: ถ้าลด $f_s$ เหลือ 25 Hz แต่ยังเก็บ $N = 200$ เท่าเดิม จะได้ $T = 200/25 = 8$ วินาที — นานขึ้นสองเท่า ตรงกับการบ้านข้อ 3 พอดี

> ทำไมต้องรู้ $T$? เพราะตอน train โมเดลกินข้อมูล **ทีละหน้าต่าง** ($T$ วินาที) เราต้องมั่นใจว่าหน้าต่างยาวพอครอบท่าเต็มรอบ — สูตรสั้นๆ นี้บอกได้ทันทีโดยไม่ต้องเดา

---

# BURST — เก็บกี่ sample ต่อการกดหนึ่งครั้ง

เราตั้ง `BURST = 200` หนึ่งครั้งที่กดปุ่ม จะเก็บ 200 sample ต่อเนื่อง ทำไมต้อง 200 ไม่ใช่ 5 หรือ 5000?

- ที่ 50 Hz, 200 sample = **~4 วินาที** — ยาวพอให้ทำท่าเต็มรอบ (เขย่าไปมาหลายครั้ง, วาดวงกลมจบวง)
- ท่าทางเป็น **รูปแบบตามเวลา** ไม่ใช่ค่าจุดเดียว — โมเดลต้องเห็นหลาย sample เรียงกันถึงจะแยก `circle` ออกจาก `shaking` ได้
- น้อยไป (เช่น 5 sample) = ไม่เห็นรูปคลื่นครบ · มากเกินจำเป็น = ไฟล์บวมและเสียเวลาเก็บ

<div style="text-align:center;margin:6px 0">
<svg width="820" height="110" viewBox="0 0 820 110" font-family="DejaVu Sans, sans-serif">
  <text x="20" y="30" font-size="12" fill="#555">หนึ่ง burst = 200 sample เรียงตามเวลา (~4 วินาที):</text>
  <rect x="20" y="42" width="780" height="34" rx="6" fill="#e8f5e9" stroke="#2e7d32"/>
  <path d="M30,59 Q60,44 90,59 T150,59 T210,59 T270,59 T330,59 T390,59 T450,59 T510,59 T570,59 T630,59 T690,59 T750,59 T790,59" fill="none" stroke="#2e7d32" stroke-width="2"/>
  <text x="410" y="98" font-size="11" fill="#888" text-anchor="middle">โมเดลดู "รูปคลื่นทั้งช่วง" ไม่ใช่ค่าเดียว - จึงต้องเก็บเป็นชุดต่อเนื่อง</text>
</svg>
</div>

> เดี๋ยวในบทเรียน Analysis (บทเรียน 4.5–4.6) เราจะเจอคำว่า **window** (หน้าต่าง) — โมเดลจริงกินข้อมูลทีละหน้าต่าง เช่น 1-2 วินาที `BURST` วันนี้คือการเก็บให้ยาวพอครอบหลายหน้าต่าง

---

# schema ของ CSV — หนึ่งบรรทัดต่อหนึ่ง sample

**CSV** (Comma-Separated Values) คือไฟล์ข้อความธรรมดา แต่ละบรรทัดคือหนึ่งแถว แต่ละค่าคั่นด้วยจุลภาค บรรทัดแรกคือ **หัวตาราง (schema)** บอกว่าคอลัมน์ไหนคืออะไร

<div style="text-align:center;margin:6px 0">
<svg width="820" height="180" viewBox="0 0 820 180" font-family="monospace">
  <rect x="20" y="16" width="780" height="30" fill="#e3f2fd" stroke="#1565c0"/>
  <text x="30" y="36" font-size="14" font-weight="700" fill="#1565c0">label,ax,ay,az,gx,gy,gz</text>
  <text x="640" y="36" font-size="11" font-family="DejaVu Sans" fill="#1565c0">&lt;- schema (บรรทัดแรก)</text>
  <rect x="20" y="46" width="780" height="26" fill="#f7f7f7" stroke="#ccc"/>
  <text x="30" y="64" font-size="13" fill="#333">shaking,0.9123,-0.0421,9.7810,12.44,-3.10,0.88</text>
  <rect x="20" y="72" width="780" height="26" fill="#fff" stroke="#ccc"/>
  <text x="30" y="90" font-size="13" fill="#333">shaking,1.2044,0.3310,9.6620,18.20,-1.55,2.01</text>
  <rect x="20" y="98" width="780" height="26" fill="#f7f7f7" stroke="#ccc"/>
  <text x="30" y="116" font-size="13" fill="#333">shaking,-0.4410,0.1120,9.9032,-5.62,4.71,-1.20</text>
  <rect x="20" y="124" width="780" height="26" fill="#fff" stroke="#ccc"/>
  <text x="30" y="142" font-size="13" fill="#999">...  (อีก 197 บรรทัดต่อการกดหนึ่งครั้ง)</text>
  <text x="30" y="168" font-size="12" font-family="DejaVu Sans" fill="#2e7d32">แต่ละบรรทัด = หนึ่ง snapshot ของ IMU 6 แกน + ชื่อท่า</text>
</svg>
</div>

- คอลัมน์ `label` = ชื่อท่า (เราเลือกก่อนกด) · `ax..az` = ความเร่ง 3 แกน · `gx..gz` = ไจโร 3 แกน
- ทำไม CSV? เพราะ **เปิดได้ทุกที่** — Excel, Python (pandas), เครื่องมือ train ทั้งหมดอ่าน CSV ได้ทันที
- ทำไมมี label ในทุกบรรทัด? เพราะตอน train เราต้องรู้ว่าแต่ละ sample เป็นท่าอะไร (supervised learning)

> schema คือ "สัญญา" ระหว่างคนเก็บข้อมูลกับคนเทรน — ถ้าเรียงคอลัมน์สลับ หรือหัวไม่ตรง เครื่อง train จะอ่านผิดทันที ต้องเป๊ะ

---

# เขียนลงไฟล์บนบอร์ด — dataset อยู่บน flash เอง

จุดที่น่าทึ่ง: เราเขียนไฟล์ CSV ลง **หน่วยความจำ flash บนบอร์ดเอง** ด้วย `open()` / `write()` แบบเดียวกับ Python บนคอมเป๊ะ

```python
with open("/gestures.csv", "a") as f:      # "a" = append ต่อท้าย
    f.write("shaking,0.91,-0.04,9.78,12.4,-3.1,0.9\n")
```

- `"/gestures.csv"` — path เริ่มด้วย `/` คือ root ของ filesystem บนบอร์ด (LittleFS)
- โหมด `"a"` (append) = **เขียนต่อท้าย ไม่ลบของเก่า** — สำคัญมาก ถ้าใช้ `"w"` ทุกครั้งจะทับ dataset หายหมด
- `with open(...) as f:` — เปิดแล้วปิดให้อัตโนมัติ ข้อมูลถูก flush ลง flash เรียบร้อยตอนออกจาก `with`

> ข้อมูลอยู่บนอุปกรณ์ ไม่ได้ขึ้นคลาวด์ — สอดคล้องกับหัวใจ Edge AI ตั้งแต่ชุดบทเรียนแรก: **ข้อมูลเกิดที่ไหน ประมวลผล/เก็บที่นั่น** เดี๋ยวโมดูล 5 (Training) เราค่อยดึงไฟล์นี้ออกไป train บนคอม

---

# sensors.bmi270.motion() — อ่าน 6 แกนใน snapshot เดียว

หัวใจของการ sample คือคำสั่งเดียว มันคืน 6 ค่าพร้อมกัน: ความเร่ง 3 แกน + ไจโร 3 แกน

```python
import sensors
ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
#   |__ accelerometer (m/s^2) __|  |__ gyroscope (dps) __|
```

- `ax, ay, az` — ความเร่งแนวแกน X/Y/Z หน่วย m/s² (วางนิ่งแกนที่ตั้งฉากพื้นจะอ่านได้ ~9.8 จากแรงโน้มถ่วง)
- `gx, gy, gz` — ความเร็วเชิงมุม (การหมุน) หน่วยองศา/วินาที
- ทำไมใช้ `motion()` ไม่ใช่ `acceleration()` + `gyroscope()` แยก? เพราะ `motion()` อ่านทั้ง 6 แกน **ใต้ bus lock เดียว** = ทุกแกนเป็นเวลาเดียวกันเป๊ะ (snapshot ตรงเวลา)

> เวลาตรงกันของทุกแกนสำคัญมากตอน train — ถ้า ax กับ gx มาจากคนละจังหวะเวลา รูปคลื่นจะเพี้ยน `motion()` แก้ปัญหานี้ให้เราแล้ว

---

# ถามเซนเซอร์ก่อนเขียนโค้ด — ลองใน REPL

นิสัยที่ดีจากบทเรียน 1.1–1.3: **ถามฮาร์ดแวร์ก่อน อย่าเดา** ก่อนเขียน logger ลองเรียก `motion()` ใน REPL ดูว่าได้อะไรกลับมาจริง

```python
>>> import sensors
>>> sensors.bmi270.motion()
(0.0412, -0.0231, 9.7810, 0.44, -0.12, 0.08)   # วางนิ่งบนโต๊ะ
>>> sensors.bmi270.motion()
(1.9044, 0.8830, 8.2210, 45.20, -18.5, 12.3)   # ขณะเขย่า
```

- วางนิ่ง: แกนที่ตั้งฉากพื้นอ่านได้ ~9.8 (แรงโน้มถ่วง) ไจโรใกล้ 0 (ไม่หมุน)
- เขย่า: ทุกค่าแกว่งแรง โดยเฉพาะไจโร (`gx,gy,gz`) พุ่งขึ้นเพราะมีการหมุน
- เห็นด้วยตาก่อนว่าค่าจริงหน้าตาแบบนี้ พอเอาไปเขียนลงไฟล์ เราจะรู้ทันทีว่าข้อมูล "สมเหตุผล" ไหม

> ลองสองสามครั้งใน REPL ก่อนรัน logger — จะได้ feel ว่าค่านิ่งกับค่าเขย่าต่างกันแค่ไหน นี่คือ "การทำความรู้จักข้อมูล" ที่วิศวกรทำก่อนเก็บจริงเสมอ
