---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 2.3 — เสียงและหลายเซนเซอร์บนเส้นเวลาเดียว: PDM 16 kHz ประทับเวลา และ jitter"
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

# บทเรียน 2.3 — เสียงและหลายเซนเซอร์บนเส้นเวลาเดียว: PDM 16 kHz ประทับเวลา และ jitter
## มัดสองสัญญาณให้เป็น dataset เดียว

**โมดูล 2 — เก็บข้อมูลจากเซนเซอร์ (DAQ)**

**โมดูล 2 · Pillar 1 — DAQ (ต่อจากบทเรียน 2.1–2.2)**

> คาถาประจำบทเรียน: **"ก่อนจะฝึกโมเดลหลายเซนเซอร์ได้ ต้องเก็บสัญญาณทุกตัวให้อยู่บนเวลาเดียวกันก่อน"**

MicroPython บนบอร์ด BENTO (PSoC Edge · ไมโครโฟน PDM + IMU BMI270)

---

# เปิดบทเรียนด้วยของจริงก่อน

เหมือนทุกบทเรียน เราเริ่มแบบ **กลับด้าน** — รันของที่ทำงานได้ก่อน แล้วค่อยแกะ วันนี้ของจริงคือ "โต๊ะเก็บ dataset" ที่อัดเสียงและการเคลื่อนไหวพร้อมกัน

<div style="text-align:center;margin:10px 0">
<svg width="820" height="150" viewBox="0 0 820 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arOpen" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="40" width="180" height="70" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="104" y="72" font-size="15" font-weight="700" fill="#2e7d32" text-anchor="middle">รันตัวเก็บก่อน</text>
  <text x="104" y="94" font-size="12" fill="#555" text-anchor="middle">VU + อัด WAV</text>
  <rect x="234" y="40" width="180" height="70" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="324" y="72" font-size="15" font-weight="700" fill="#1565c0" text-anchor="middle">แกะดูข้างใน</text>
  <text x="324" y="94" font-size="12" fill="#555" text-anchor="middle">PDM · เส้นเวลา</text>
  <rect x="454" y="40" width="180" height="70" rx="12" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="544" y="72" font-size="15" font-weight="700" fill="#e65100" text-anchor="middle">เติม/แก้เอง</text>
  <text x="544" y="94" font-size="12" fill="#555" text-anchor="middle">4 ก้าวในลูป</text>
  <rect x="674" y="40" width="132" height="70" rx="12" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="740" y="72" font-size="15" font-weight="700" fill="#6a1b9a" text-anchor="middle">ได้ dataset</text>
  <text x="740" y="94" font-size="12" fill="#555" text-anchor="middle">ฐานของ Training</text>
  <line x1="194" y1="75" x2="230" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="414" y1="75" x2="450" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
  <line x1="634" y1="75" x2="670" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arOpen)"/>
</svg>
</div>

เราจะรัน VU meter กับตัวอัด WAV ที่มีให้แล้ว (ตัวอย่าง 06/07) เพื่อ "เห็นเสียงกลายเป็นตัวเลข" ก่อน แล้วค่อยเอาสองความสามารถนี้ — อ่านเสียง + อ่าน IMU — มามัดรวมบนเส้นเวลาเดียว

> ชุดบทเรียนนี้ยังไม่ต้อง train อะไร ขอแค่ได้ไฟล์ dataset ที่ทุกแถวมี "ทั้งเสียงและการเคลื่อนไหวของช่วงเวลาเดียวกัน" ก็ถือว่าถึงเป้าแล้ว

---

# เป้าหมายของชุดบทเรียนนี้

จบชุดบทเรียนนี้เราจะเดินครบ 4 เรื่อง แล้วปิดท้ายด้วยการเก็บ dataset จริง:

1. **ไมโครโฟน PDM** อ่านเสียงยังไง — จาก bitstream เป็น PCM เป็นระดับ dBFS
2. **เส้นเวลาร่วม (shared timeline)** — ทำไมสองเซนเซอร์ต้องแชร์ `t_ms` เดียวกัน
3. **การอ่านหลายเซนเซอร์ในลูปเดียว** — IMU + MIC ต่อแถว บนอัตราที่คุมได้
4. **รูปแบบ dataset** ที่เอาไป train ต่อได้ (CSV ต่อแถว + เสียงดิบเป็น WAV)
5. ลงมือ: เติม [`s05_multicapture.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m02-daq/l04-multicapture-lab/practice/s05_multicapture.py) ให้เก็บ **≥2 เซนเซอร์บนเวลาเดียว** ลงไฟล์

ปลายทางของวันนี้: กดปุ่ม label ทำท่า + ส่งเสียงพร้อมกัน แล้วได้ไฟล์ `/multicapture.csv` ที่ทุกแถวมี IMU และระดับเสียงบน `t_ms` เดียวกัน

> วันนี้เราเน้น "เก็บให้ตรงเวลา" ส่วนการแปลงสัญญาณเป็น feature (FFT / spectrogram) เก็บไว้เป็นเป้าหมายของ โมดูล 4 (Analysis)

---

# ย้อนชุดบทเรียนก่อนหน้า — DAQ I เราเก็บ IMU ได้แล้ว

บทเรียน 2.1–2.2 เราสร้าง [`s04_daq_logger.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m02-daq/l02-daq-logger-lab/practice/s04_daq_logger.py) เก็บ IMU 6 แกนลง CSV ทีละ label ได้แล้ว นั่นคือ **เซนเซอร์เดียว บนเส้นเวลาเดียว** — วันนี้เราต่อยอดเป็น **สองเซนเซอร์**

<div style="text-align:center;margin:8px 0">
<svg width="820" height="150" viewBox="0 0 820 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arDaq" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="30" y="44" width="300" height="72" rx="12" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="180" y="72" font-size="14" font-weight="700" fill="#1565c0" text-anchor="middle">บทเรียน 2.1–2.2 — DAQ I</text>
  <text x="180" y="94" font-size="12" fill="#555" text-anchor="middle">IMU -> CSV (label,ax..gz)</text>
  <text x="180" y="110" font-size="11" fill="#888" text-anchor="middle">เซนเซอร์เดียว</text>
  <rect x="490" y="44" width="300" height="72" rx="12" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="640" y="72" font-size="14" font-weight="700" fill="#2e7d32" text-anchor="middle">บทเรียน 2.3–2.4 — DAQ II (วันนี้)</text>
  <text x="640" y="94" font-size="12" fill="#555" text-anchor="middle">IMU + MIC -> CSV (+t_ms,db)</text>
  <text x="640" y="110" font-size="11" fill="#888" text-anchor="middle">สองเซนเซอร์ เวลาเดียว</text>
  <line x1="330" y1="80" x2="488" y2="80" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arDaq)"/>
  <text x="409" y="72" font-size="11" fill="#607d8b" text-anchor="middle">เพิ่มเสียง</text>
  <text x="409" y="98" font-size="11" fill="#607d8b" text-anchor="middle">+ เส้นเวลา</text>
</svg>
</div>

- โครงเดิมยังอยู่: ปุ่ม label · ฟังก์ชัน `record()` · เขียน CSV ทีละแถว · `finally` เก็บกวาด
- ของใหม่ที่เพิ่มเข้ามามีแค่สาม: เปิดไมโครโฟน, อ่านเสียงหนึ่งเฟรมต่อแถว, ประทับ `t_ms` ให้ทุกแถว

> ถ้าบทเรียน 2.1–2.2 เข้าหัวแล้ว ชุดบทเรียนนี้คือการ "บวกอีกหนึ่งเซนเซอร์" — เห็นชัดว่า pattern การเก็บข้อมูลขยายได้เรื่อยๆ ไม่ใช่เขียนใหม่ทั้งหมด

---

# ทำไมต้องเก็บมากกว่าหนึ่งสัญญาณ

โมเดล Edge AI ที่ทรงพลังหลายตัวไม่ได้ดูสัญญาณเดียว มันดู **หลายสัญญาณพร้อมกัน** แล้วตัดสินใจจากภาพรวม — แต่จะทำแบบนั้นได้ dataset ต้องเก็บมาให้ตรงเวลากันตั้งแต่แรก

- **เสียง + การเคลื่อนไหว** — เช่น แยก "ไอจริง" จาก "เคาะโต๊ะ" ต้องดูทั้งเสียงและว่าตัวคนขยับไหม
- **หลายเซนเซอร์ยืนยันกัน** — เรดาร์เห็นคนเข้ามา + เสียงเปลี่ยน = มั่นใจกว่าใช้ตัวเดียว
- **บริบท** — ระดับเสียงพื้นหลังช่วยให้โมเดลรู้ว่าตอนนี้เงียบหรือมีเสียงรบกวน

> หัวใจของชุดบทเรียน: ถ้าเก็บเสียงกับ IMU มา "คนละไฟล์ คนละเวลา" เราจะจับคู่มันทีหลังไม่ได้เลย — ต้องมัดด้วยเส้นเวลาเดียวตั้งแต่ตอนเก็บ

---

# เสียงคือสนามใหญ่ของ Edge AI

จำเมนู 6 โมเดลชุดบทเรียนแรกได้ไหม — **4 ใน 6** ใช้ไมโครโฟน (Baby Cry / Cough / Alarm / Siren) งานเสียงจึงเป็นสนามใหญ่ และการเก็บเสียงเป็นทักษะ DAQ ที่ขาดไม่ได้

<div style="text-align:center;margin:8px 0">
<svg width="760" height="140" viewBox="0 0 760 140" font-family="DejaVu Sans, sans-serif">
  <rect x="20" y="30" width="230" height="82" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="135" y="56" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">เสียง (MIC)</text>
  <text x="135" y="78" font-size="11" fill="#555" text-anchor="middle">Baby Cry · Cough</text>
  <text x="135" y="96" font-size="11" fill="#555" text-anchor="middle">Alarm · Siren</text>
  <rect x="270" y="30" width="220" height="82" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="380" y="56" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">การเคลื่อนไหว (IMU)</text>
  <text x="380" y="78" font-size="11" fill="#555" text-anchor="middle">Motion:</text>
  <text x="380" y="96" font-size="11" fill="#555" text-anchor="middle">idle/circle/shaking</text>
  <rect x="510" y="30" width="230" height="82" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="625" y="56" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">เรดาร์ (RADAR)</text>
  <text x="625" y="78" font-size="11" fill="#555" text-anchor="middle">Push Detection</text>
  <text x="625" y="96" font-size="11" fill="#555" text-anchor="middle">มี-ไม่มีคน</text>
</svg>
</div>

- เก็บเสียงดิบได้ = เปิดประตูสู่ dataset ของทุกโมเดลเสียง (โมดูล 5 (Training) เราจะฝึกเอง)
- ชุดบทเรียนนี้เราจับคู่เสียงกับ IMU เพื่อฝึกทักษะ "sync หลายเซนเซอร์" ซึ่งใช้ได้กับทุกคู่เซนเซอร์

> เก็บเสียงบนอุปกรณ์แล้ววิเคราะห์ในเครื่อง = ความเป็นส่วนตัว เสียงไม่ต้องออกไปคลาวด์ — นี่คือจุดขายของ Edge AI ที่เราเห็นตั้งแต่บทเรียน 1.1–1.3

---

# ไมโครโฟน PDM ทำงานยังไง

ไมโครโฟนบนบอร์ดเป็นแบบ **PDM** (Pulse-Density Modulation) มันส่งบิต 0/1 ความเร็วสูงมา ฮาร์ดแวร์แปลงเป็นตัวอย่างเสียง **PCM** (ตัวเลข 16-bit) ให้เราอ่านเป็น array ได้

<div style="text-align:center;margin:8px 0">
<svg width="820" height="140" viewBox="0 0 820 140" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arPdm" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="42" width="160" height="60" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="100" y="66" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">ไมค์ PDM</text>
  <text x="100" y="86" font-size="11" fill="#666" text-anchor="middle">บิต 0/1 เร็วมาก</text>
  <rect x="250" y="42" width="200" height="60" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="350" y="66" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">ฮาร์ดแวร์ PDM_PCM</text>
  <text x="350" y="86" font-size="11" fill="#666" text-anchor="middle">แปลงเป็น PCM 16-bit</text>
  <rect x="520" y="42" width="200" height="60" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="620" y="66" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">buf (array 'h')</text>
  <text x="620" y="86" font-size="11" fill="#666" text-anchor="middle">ตัวอย่างเสียง 16000/s</text>
  <line x1="180" y1="72" x2="246" y2="72" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arPdm)"/>
  <line x1="450" y1="72" x2="516" y2="72" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arPdm)"/>
  <text x="770" y="76" font-size="11" fill="#999">readinto()</text>
</svg>
</div>

```python
from machine import PDM_PCM
pdm = PDM_PCM(0, sck="P8_5", data="P8_6", sample_rate=16000)
buf = array.array("h", (0 for _ in range(512)))   # 'h' = 16-bit signed
pdm.readinto(buf)                                  # เติม buf ด้วยตัวอย่างเสียงชุดใหม่
```

> `sample_rate=16000` คือ 16000 ตัวอย่างต่อวินาที ซึ่งเป็นอัตรามาตรฐานของงานเสียงพูด/เสียงสิ่งแวดล้อม — เพียงพอสำหรับโมเดลเสียงส่วนใหญ่ในคอร์ส

---

# อ่านเสียงหนึ่งเฟรม — จากคลื่นเป็นตัวเลขเดียว

`buf` เต็มไปด้วยตัวเลขหลายร้อยตัว เราย่อมันเป็น **ค่าเดียวต่อเฟรม** ที่บอก "ตอนนี้ดังแค่ไหน" — วิธีมาตรฐานคือหา RMS แล้วแปลงเป็น **dBFS**

```python
def dbfs(chunk):
    acc = 0
    for s in chunk:
        acc += s * s               # กำลังสองของแต่ละตัวอย่าง
    rms = math.sqrt(acc / len(chunk))
    return 20 * math.log10(rms / 32768) if rms > 0 else -96.0
```

- **RMS** (root-mean-square) = ขนาดเฉลี่ยของคลื่นในเฟรมนั้น สะท้อน "พลังงานเสียง"
- **dBFS** = เทียบ RMS กับค่าสูงสุดที่ 16-bit ทำได้ (32768) แล้วเป็นเดซิเบล 0 = ดังสุด, ยิ่งลบยิ่งเบา
- ค่าเดียวนี้แหละที่เราจะเก็บลง CSV เป็นคอลัมน์ `db` ต่อแถว

> ทำไมไม่เก็บทุกตัวอย่างลง CSV? เพราะ 16000 ค่า/วินาที จะใหญ่มหาศาล — ในชุดบทเรียนนี้เราเก็บ **สรุประดับเสียง** ต่อแถวไว้ใน CSV ส่วนเสียงดิบเก็บแยกเป็น WAV (ในฉบับเต็ม)

---

# คณิตของการสุ่มเสียง — 16 kHz หมายความว่าอะไร

ไมค์ PDM ถูกแปลงเป็น PCM ที่ **อัตราสุ่ม (sample rate)** — `sample_rate=16000` แปลว่าเก็บ 16,000 ตัวอย่างต่อวินาที ระยะห่างระหว่างสองตัวอย่างจึงคงที่:

$$T_s = \frac{1}{f_s} = \frac{1}{16{,}000\ \text{Hz}} = 62.5\ \mu s$$

- $f_s$ = อัตราสุ่ม (samples per second) — ที่นี่คือ 16,000
- $T_s$ = ระยะเวลาระหว่างสองตัวอย่างที่ติดกัน ยิ่ง $f_s$ สูง ตัวอย่างยิ่งถี่ เสียงยิ่งละเอียด
- **mono** = ช่องสัญญาณเดียว หนึ่งตัวอย่าง = หนึ่งตัวเลข (ไม่ใช่คู่ซ้าย/ขวาแบบสเตอริโอ) จึงตรงกับ `array.array("h", ...)` ที่เก็บเลข 16-bit เรียงกันตรงๆ

> ทำไมเลือก 16 kHz? เสียงพูดและเสียงสิ่งแวดล้อมส่วนใหญ่มีพลังงานต่ำกว่า 8 kHz ตามกฎ Nyquist อัตราสุ่มต้อง $\geq$ สองเท่าของความถี่สูงสุดที่อยากเก็บ 16 kHz จึงพอดีกับงานเสียงในคอร์ส และประหยัดหน่วยความจำกว่า 44.1 kHz ของเพลง

---

# หนึ่งเฟรมเสียงกินเวลาเท่าไร — N ตัวอย่าง

เราไม่ได้อ่านทีละตัวอย่าง แต่อ่านทีละก้อน `buf` ขนาด $N =$ `CHUNK` ตัวอย่าง ก้อนหนึ่งจึงครอบคลุมช่วงเวลา:

$$t_{win} = \frac{N}{f_s}$$

ลองแทนค่า `CHUNK = 512` (จากโค้ด `range(512)`):

$$t_{win} = \frac{512}{16{,}000} = 0.032\ \text{s} = 32\ \text{ms}$$

- $N$ = จำนวนตัวอย่างในหนึ่งเฟรม (ขนาด buffer) — คือ `CHUNK` ที่ส่งเข้า `array.array`
- $t_{win}$ = "หน้าต่างเวลา" ที่ค่า `db` หนึ่งค่าเป็นตัวแทน — `db` แถวนี้คือพลังงานเสียงเฉลี่ยของ 32 ms ช่วงนี้
- ยิ่ง `CHUNK` ใหญ่ เฟรมยิ่งยาว `readinto()` ยิ่งรอนานขึ้น จึงเพิ่ม jitter ในลูป ~20 ms ของเรา

> นี่คือเหตุผลเบื้องหลังคำใบ้ "ลด `CHUNK` เพื่อลด jitter": ถ้า $t_{win}$ ยาวใกล้หรือเกินจังหวะแถว (`RATE_MS = 20`) เฟรมเสียงจะกลืนเวลาจนแถวห่างเกินเป้า — และเพราะเราเก็บ `t_ms` จริงไว้ทุกแถว เราจึง "เห็น" อาการนี้ย้อนหลังได้

---

# ของเจ๋งก่อน (1) — VU meter ที่มีให้แล้ว

ก่อนเขียนเอง รันตัวอย่าง [`06_mic_level_meter.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m02-daq/l03-audio-and-timeline/examples/06_mic_level_meter.py) ให้เห็นเสียงกลายเป็นแถบระดับสดๆ — นี่คือครึ่งแรกของสิ่งที่เราจะเอาไปมัดรวม

```python
pdm.readinto(buf)
rms = math.sqrt(sum(s*s for s in buf) / len(buf))
db = 20 * math.log10(rms / 32768) if rms > 0 else -96.0
bar.value(max(0, int(db + 60)))         # แกน 0..60 = -60..0 dBFS
seg.text("%d" % int(db))
```

- ลองพูด / ปรบมือ ใส่ไมค์ แล้วดูแถบขยับ + ตัวเลข dBFS วิ่ง — เสียงเป็นตัวเลขจริงๆ แล้ว
- โครงเดียวกับที่เราจะใช้: `readinto` -> `dbfs` -> เอาค่าไปใช้ต่อ

> "รันของที่ทำงานได้ก่อน" — พอเห็นแถบ VU ขยับตามเสียงตัวเอง คุณจะเข้าใจ `dbfs()` โดยไม่ต้องท่องสูตร แล้วค่อยเอาไปประกอบเป็นตัวเก็บ dataset

---

# ของเจ๋งก่อน (2) — อัดเสียงเป็น WAV

ตัวอย่าง [`07_mic_record_wav.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m02-daq/l03-audio-and-timeline/examples/07_mic_record_wav.py) เก็บ **เสียงดิบทั้งก้อน** ลงไฟล์ `.wav` — นี่คืออีกครึ่งที่ฉบับเต็มของเราจะใช้เก็บคลื่นเสียงคู่กับ CSV

```python
with open("/rec.wav", "wb") as f:
    f.write(wav_header(total, RATE))     # หัวไฟล์ WAV
    while written < total:
        pdm.readinto(buf)
        f.write(buf)                     # ต่อท้ายเสียงดิบทีละก้อน
        written += CHUNK
```

- WAV = หัวไฟล์สั้นๆ บอกอัตรา/ช่องสัญญาณ แล้วตามด้วยตัวอย่างเสียงดิบตรงๆ
- ดึงไฟล์ออกจากบอร์ดด้วย BENTO IDE (file transfer) หรือ `mpremote` เอาไปฟัง/วิเคราะห์บน PC ได้

> สองตัวอย่างนี้คือ "วัตถุดิบ" ของชุดบทเรียน: ตัวหนึ่งย่อเสียงเป็นตัวเลข (VU) อีกตัวเก็บเสียงดิบ (WAV) เราจะหยิบทั้งคู่มาต่อกับ IMU บนเส้นเวลาเดียว

---

# ปัญหาการ sync — สองสัญญาณคนละจังหวะ

ถ้าเก็บเสียงกับ IMU แยกกัน แต่ละตัวมีจังหวะของมันเอง เวลาเอามารวม เราจะไม่รู้ว่า "ค่าเสียงตัวนี้เกิดพร้อมกับการขยับตัวไหน" — ข้อมูลจับคู่ไม่ได้

<div style="text-align:center;margin:6px 0">
<svg width="860" height="170" viewBox="0 0 860 170" font-family="DejaVu Sans, sans-serif">
  <text x="20" y="40" font-size="13" font-weight="700" fill="#c62828">ไม่ sync — เก็บแยกไฟล์</text>
  <line x1="150" y1="60" x2="820" y2="60" stroke="#b0bec5" stroke-width="2"/>
  <text x="20" y="64" font-size="11" fill="#1565c0">IMU</text>
  <circle cx="200" cy="60" r="5" fill="#1565c0"/><circle cx="300" cy="60" r="5" fill="#1565c0"/><circle cx="400" cy="60" r="5" fill="#1565c0"/><circle cx="520" cy="60" r="5" fill="#1565c0"/><circle cx="640" cy="60" r="5" fill="#1565c0"/>
  <line x1="150" y1="96" x2="820" y2="96" stroke="#b0bec5" stroke-width="2"/>
  <text x="20" y="100" font-size="11" fill="#6a1b9a">MIC</text>
  <circle cx="240" cy="96" r="5" fill="#6a1b9a"/><circle cx="360" cy="96" r="5" fill="#6a1b9a"/><circle cx="470" cy="96" r="5" fill="#6a1b9a"/><circle cx="600" cy="96" r="5" fill="#6a1b9a"/>
  <text x="430" y="140" font-size="12" fill="#c62828" text-anchor="middle">จุดไม่ตรงกัน -> จับคู่ "เสียงนี้คู่กับท่านี้" ไม่ได้</text>
</svg>
</div>

- ทางแก้ที่ **ผิด**: เก็บสองไฟล์แยกแล้วหวังว่าจะจับคู่ตอนหลังด้วยลำดับ — พลาดง่ายมากเมื่ออัตราต่างกัน
- ทางแก้ที่ **ถูก**: อ่านทั้งสองเซนเซอร์ใน **ลูปเดียว รอบเดียว** แล้วเขียนลง **แถวเดียว** พร้อมเวลาประทับร่วม

> นี่เป็นปัญหาคลาสสิกของงาน DAQ: ไม่ใช่แค่ "เก็บให้ได้" แต่ "เก็บให้ตรงเวลา" ต่างหากที่ทำให้ dataset ใช้งานได้จริง

---

# ทางออก — เส้นเวลาเดียว (shared timeline)

วิธีของเราเรียบง่ายและได้ผล: ในหนึ่งรอบของลูป อ่าน IMU และ MIC **ติดกัน** แล้วเขียนหนึ่งแถวที่ทั้งคู่แชร์ค่าเวลา `t_ms` เดียวกัน

<div style="text-align:center;margin:6px 0">
<svg width="860" height="170" viewBox="0 0 860 170" font-family="DejaVu Sans, sans-serif">
  <text x="20" y="34" font-size="13" font-weight="700" fill="#2e7d32">sync — หนึ่งรอบ = หนึ่งแถว = หนึ่ง t_ms</text>
  <line x1="150" y1="70" x2="820" y2="70" stroke="#b0bec5" stroke-width="2"/>
  <g>
    <line x1="230" y1="52" x2="230" y2="120" stroke="#cfd8dc" stroke-width="1"/>
    <line x1="380" y1="52" x2="380" y2="120" stroke="#cfd8dc" stroke-width="1"/>
    <line x1="530" y1="52" x2="530" y2="120" stroke="#cfd8dc" stroke-width="1"/>
    <line x1="680" y1="52" x2="680" y2="120" stroke="#cfd8dc" stroke-width="1"/>
  </g>
  <circle cx="230" cy="62" r="5" fill="#1565c0"/><circle cx="230" cy="78" r="5" fill="#6a1b9a"/>
  <circle cx="380" cy="62" r="5" fill="#1565c0"/><circle cx="380" cy="78" r="5" fill="#6a1b9a"/>
  <circle cx="530" cy="62" r="5" fill="#1565c0"/><circle cx="530" cy="78" r="5" fill="#6a1b9a"/>
  <circle cx="680" cy="62" r="5" fill="#1565c0"/><circle cx="680" cy="78" r="5" fill="#6a1b9a"/>
  <text x="230" y="138" font-size="10" fill="#555" text-anchor="middle">t=0</text>
  <text x="380" y="138" font-size="10" fill="#555" text-anchor="middle">t=20</text>
  <text x="530" y="138" font-size="10" fill="#555" text-anchor="middle">t=40</text>
  <text x="680" y="138" font-size="10" fill="#555" text-anchor="middle">t=60</text>
  <text x="70" y="66" font-size="11" fill="#1565c0">IMU</text>
  <text x="70" y="82" font-size="11" fill="#6a1b9a">MIC</text>
  <text x="430" y="160" font-size="11" fill="#2e7d32" text-anchor="middle">แต่ละหลัก = อ่านสองเซนเซอร์แล้วเขียนแถวเดียว บน t_ms ร่วม</text>
</svg>
</div>

- ผล: ทุกแถวใน CSV บอกได้แน่ว่า "ค่าเสียง `db` กับค่า IMU นี้เกิดในช่วงเวลาเดียวกัน (`t_ms`)"
- ทีหลังเราจะจับคู่/ตัดหน้าต่าง/ลากกราฟตามเวลาได้ทันที เพราะทุกอย่างอ้างเส้นเวลาเดียว

> นี่คือแก่นของชุดบทเรียน ถ้าจำได้เรื่องเดียว ให้จำว่า **"อ่านพร้อมกัน เขียนแถวเดียว ประทับเวลาร่วม"**

---

# ประทับเวลา — ticks_ms / ticks_diff

MicroPython ให้นาฬิกามิลลิวินาทีมา เราจับเวลาเริ่มไว้ที่ `t0` แล้วทุกแถวเก็บ "ผ่านไปกี่ ms จาก `t0`"

```python
t0 = time.ticks_ms()                        # จุดศูนย์ของชุดนี้
# ... ในลูป:
t_ms = time.ticks_diff(time.ticks_ms(), t0) # เวลาผ่านไปเทียบ t0
```

- ใช้ `time.ticks_diff(a, b)` แทนการลบตรงๆ (`a - b`) เพราะตัวนับ ms มี **wrap-around** (วนกลับ 0) `ticks_diff` จัดการให้ถูก
- `t_ms` เริ่มที่ ~0 ในแถวแรก แล้วเพิ่มขึ้นเรื่อยๆ — เป็นแกนเวลาของทั้งชุด
- ทุกเซนเซอร์ในรอบเดียวกันใช้ `t_ms` ค่าเดียวกัน จึงถือว่า "เวลาเดียวกัน"

> อย่าใช้ `time.time()` หรือเลขรอบมานับเวลา — `ticks_ms/ticks_diff` คือคู่มาตรฐานของ MicroPython สำหรับวัดช่วงเวลาสั้นๆ อย่างแม่นและปลอดภัยจาก wrap

---

# อัตราสุ่มกับความคลาดเคลื่อน (jitter)

เราตั้งใจให้แต่ละแถวห่างกัน `RATE_MS = 20` (50 Hz) ด้วย `time.sleep_ms(20)` แต่ในความจริงงานอ่านเสียง/เขียนไฟล์ก็กินเวลา ทำให้ช่วงจริงเพี้ยนได้เล็กน้อย — ค่านี้เรียก **jitter**

<div style="text-align:center;margin:6px 0">
<svg width="820" height="120" viewBox="0 0 820 120" font-family="DejaVu Sans, sans-serif">
  <line x1="40" y1="60" x2="780" y2="60" stroke="#b0bec5" stroke-width="2"/>
  <circle cx="120" cy="60" r="5" fill="#2e7d32"/><circle cx="260" cy="60" r="5" fill="#2e7d32"/>
  <circle cx="392" cy="60" r="5" fill="#ef6c00"/><circle cx="560" cy="60" r="5" fill="#2e7d32"/>
  <text x="190" y="46" font-size="10" fill="#2e7d32" text-anchor="middle">~20 ms</text>
  <text x="326" y="46" font-size="10" fill="#2e7d32" text-anchor="middle">~20 ms</text>
  <text x="476" y="46" font-size="10" fill="#ef6c00" text-anchor="middle">28 ms (ช้าไป)</text>
  <text x="410" y="96" font-size="11" fill="#607d8b" text-anchor="middle">jitter = ช่วงจริงเบี่ยงจากเป้า — เก็บ t_ms ไว้ เราจึงตรวจได้ว่าเพี้ยนแค่ไหน</text>
</svg>
</div>

- เพราะเราเก็บ `t_ms` จริงไว้ทุกแถว เราจึง **ตรวจสอบย้อนหลังได้** ว่าช่วงจริงใกล้ 20 ms แค่ไหน
- ฉบับเต็มวัด `dt` เฉลี่ยจริงและ `jitter` (ช่องว่างที่ใหญ่สุด) แล้วโชว์บนจอ — ถ้า jitter สูงมาก แปลว่า dataset ช่วงนั้นเชื่อถือไม่ได้
- วิธีลด jitter: ลด `CHUNK` เสียง, ลดงานในลูป, อย่าพิมพ์ console ถี่

> บทเรียน DAQ: การเก็บ "เวลาจริง" ไว้ ไม่ใช่แค่สมมติว่าตรง 20 ms เป๊ะ ทำให้เราตรวจคุณภาพ dataset ได้ — วิศวกรที่ดีไม่เชื่อ ตรวจเสมอ

---

# รูปแบบไฟล์ dataset — CSV schema

ไฟล์ที่เราจะได้หน้าตาแบบนี้ หนึ่งบรรทัดต่อหนึ่งแถวเวลา ทุกคอลัมน์ของแถวเดียวกันอ้าง `t_ms` เดียวกัน

```text
t_ms,label,ax,ay,az,gx,gy,gz,db
0,shaking,0.02,-0.98,0.11,1.4,-0.7,0.3,-41.2
20,shaking,0.31,-0.88,0.25,8.9,-3.1,1.2,-38.5
40,shaking,-0.12,-1.02,0.07,-5.2,2.4,-0.9,-37.9
```

| คอลัมน์ | มาจาก | ความหมาย |
|---|---|---|
| `t_ms` | `ticks_diff` | เส้นเวลาร่วม (ms จากต้นชุด) |
| `label` | ปุ่มที่กด | ท่า/คลาสของชุดนี้ (idle/circle/shaking) |
| `ax..gz` | `bmi270.motion()` | เซนเซอร์ 1 — accel 3 แกน + gyro 3 แกน |
| `db` | `dbfs(buf)` | เซนเซอร์ 2 — ระดับเสียงของเฟรมนั้น |

> สังเกตว่า `label` อยู่ในทุกแถว — เราเก็บไปพร้อมข้อมูลเลย จะได้ไม่ต้องมานั่งใส่ label ทีหลัง นี่คือ dataset ที่ "พร้อม train" ตั้งแต่ออกจากบอร์ด
