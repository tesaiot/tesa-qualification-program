---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 4.6 — ลงมือทำ: feature vector จากหน้าต่างเลื่อน"
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

# บทเรียน 4.6 — ลงมือทำ: feature vector จากหน้าต่างเลื่อน

## Analysis III: feature extraction & windowing · สิ่งที่โมเดล "เห็น" จริง ๆ

**โมดูล 4 — วิเคราะห์สัญญาณ**

> ต่อจากบทเรียน 4.5 — feature และหน้าต่าง: สิ่งที่โมเดลเห็นจริง

---

# โครงร่วมของทุกโปรแกรม MicroPython

โครงเดิมที่เราจับมาตั้งแต่ บทเรียน 1.4–1.5 — ชุดบทเรียนนี้ก็เดินตามสี่จังหวะนี้ แค่เนื้อในเป็น "windowing + feature"

<div style="text-align:center;margin:6px 0">
<svg width="880" height="130" viewBox="0 0 880 130" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arSk" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="40" width="190" height="56" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="115" y="64" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">1 · import</text>
  <text x="115" y="84" font-size="11" fill="#666" text-anchor="middle">ui · sensors · math · time</text>
  <rect x="238" y="40" width="200" height="56" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="338" y="64" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">2 · สร้างครั้งเดียว</text>
  <text x="338" y="84" font-size="11" fill="#666" text-anchor="middle">แท่ง 6 ตัว + buffer</text>
  <rect x="466" y="40" width="190" height="56" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="561" y="64" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">3 · ลูป</text>
  <text x="561" y="84" font-size="11" fill="#666" text-anchor="middle">เก็บ → หน้าต่าง → feature</text>
  <rect x="684" y="40" width="176" height="56" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="772" y="64" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">4 · ui.poll</text>
  <text x="772" y="84" font-size="11" fill="#666" text-anchor="middle">รับปุ่มออก</text>
  <line x1="210" y1="68" x2="236" y2="68" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <line x1="438" y1="68" x2="464" y2="68" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <line x1="656" y1="68" x2="682" y2="68" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <path d="M772,96 C772,116 561,116 561,98" fill="none" stroke="#9e9e9e" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arSk)"/>
  <text x="666" y="120" font-size="11" fill="#9e9e9e" text-anchor="middle">วนกลับ</text>
</svg>
</div>

> "สร้างครั้งเดียว" ยังจริงเสมอ — แท่ง 6 อันสร้างนอกลูป ในลูปแค่เรียก `.value()` เปลี่ยนความสูง ถ้าสร้างแท่งใหม่ทุกหน้าต่าง จอจะกระพริบและกินหน่วยความจำ

---

# โครงของไฟล์ s10_windowing.py

ทั้งไฟล์อ่านเป็นประโยคเดียว: **"เก็บสัญญาณเข้า buffer → พอครบหน้าต่างก็บีบเป็น feature → โชว์เป็นแท่ง → เลื่อนหน้าต่าง → วนต่อ"**

<div style="text-align:center;margin:6px 0">
<svg width="920" height="200" viewBox="0 0 920 200" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arS10" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g font-size="14" text-anchor="middle">
    <rect x="14" y="30" width="180" height="56" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="104" y="54" font-weight="700" fill="#1565c0">เก็บ HOP จุด</text>
    <text x="104" y="73" font-size="11" fill="#999">buf.append(az)</text>
    <rect x="234" y="30" width="180" height="56" rx="10" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
    <text x="324" y="50" font-weight="700" fill="#455a64" font-size="12">ครบหน้าต่าง?</text>
    <text x="324" y="70" font-size="11" fill="#999">len(buf) >= WIN</text>
    <rect x="454" y="30" width="180" height="56" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="544" y="54" font-weight="700" fill="#e65100">บีบ feature</text>
    <text x="544" y="73" font-size="11" fill="#999">features(buf[-WIN:])</text>
    <rect x="674" y="30" width="180" height="56" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="764" y="54" font-weight="700" fill="#2e7d32">โชว์แท่ง</text>
    <text x="764" y="73" font-size="11" fill="#999">bars[i].value(...)</text>
    <rect x="454" y="130" width="180" height="56" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
    <text x="544" y="154" font-weight="700" fill="#6a1b9a">เลื่อนหน้าต่าง</text>
    <text x="544" y="173" font-size="11" fill="#999">buf = buf[-WIN:]</text>
  </g>
  <line x1="194" y1="58" x2="232" y2="58" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS10)"/>
  <line x1="414" y1="58" x2="452" y2="58" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS10)"/>
  <line x1="634" y1="58" x2="672" y2="58" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS10)"/>
  <path d="M764,86 C764,120 544,110 544,128" fill="none" stroke="#2e7d32" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arS10)"/>
  <path d="M454,158 C300,158 220,120 210,88" fill="none" stroke="#9e9e9e" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arS10)"/>
  <text x="330" y="150" font-size="11" fill="#9e9e9e" text-anchor="middle">วนกลับไปเก็บ HOP จุดถัดไป</text>
</svg>
</div>

> ตัวเลขในโค้ด (`buf.append`, `features(...)`, `buf = buf[-WIN:]`) คือ 5 จุดที่คุณต้องเติมในไฟล์ฝึก — จำโครงนี้ไว้ เดี๋ยวไล่ทีละส่วน

---

# ไล่โค้ด (1) — เก็บ sample เข้า buffer

**ช่องเติมที่ 1**: ในลูปเราอ่าน IMU ทีละจุด แล้วต่อท้าย buffer:

```python
for _ in range(HOP):                       # เก็บทีละ HOP จุด
    ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
    # เติม: เก็บ accel แกน Z (az) ต่อท้าย buffer  ->  buf.append(az)
    pass
    time.sleep_ms(DT_MS)                    # 20 ms = 50 Hz
```

- แทน `pass` ด้วย `buf.append(az)` — สัญญาณ (แกน Z) ไหลเข้ามาสะสมใน `buf`
- `sensors.bmi270.motion()` คืน 6 ค่า เราหยิบแค่ `az` มาทำสัญญาณตัวอย่าง
- ถ้าลืมเติม: `buf` ว่างตลอด หน้าต่างไม่มีวันครบ แท่งไม่ขยับเลย

> `time.sleep_ms(20)` คือสิ่งที่ทำให้อัตราสุ่มเป็น 50 Hz พอดี — อัตราสุ่มต้องตรงกับที่โมเดลคาดหวัง ไม่งั้นความหมายของ "หน้าต่าง 1 วินาที" จะเพี้ยน

---

# ไล่โค้ด (2) — mean และ std

**ช่องเติมที่ 2 และ 3**: หัวใจของ feature vector อยู่ในฟังก์ชัน `features()`:

```python
def features(win):
    n = len(win)
    # เติม: ค่าเฉลี่ยของหน้าต่าง  ->  mean = sum(win) / n
    mean = 0.0
    # เติม: ส่วนเบี่ยงเบนมาตรฐาน
    #       ->  std = math.sqrt(sum((x - mean) ** 2 for x in win) / n)
    std = 0.0
```

- ช่องที่ 2: แทนด้วย `mean = sum(win) / n` — ค่าเฉลี่ยของทั้งหน้าต่าง
- ช่องที่ 3: แทนด้วย `std = math.sqrt(sum((x - mean) ** 2 for x in win) / n)` — ต้องคำนวณ `mean` ก่อนเสมอ เพราะ `std` ใช้ `mean`
- ถ้าลืมเติม: แท่ง `mean`/`std` ค้างที่ศูนย์ ทั้งที่บอร์ดขยับ

> สังเกตลำดับ: `std` พึ่ง `mean` — ถ้าสลับบรรทัด `std` จะใช้ `mean = 0.0` ผิดทันที นี่คือกับดักที่ต้องระวัง

---

# ไล่โค้ด (3) — band energy

**ช่องเติมที่ 4**: แบ่งหน้าต่างเป็น 4 ช่วงเวลา แล้ววัดพลังงาน (variance) แต่ละช่วง:

```python
band_e = []
seg = n // BANDS
for b in range(BANDS):
    s = win[b * seg:(b + 1) * seg]         # หนึ่งช่วงเวลา
    m = sum(s) / len(s)
    # เติม: พลังงาน (variance) ของย่านนี้ ต่อท้าย band_e
    #       ->  band_e.append(sum((x - m) ** 2 for x in s) / len(s))
    pass
return [mean, std] + band_e
```

- แทน `pass` ด้วย `band_e.append(sum((x - m) ** 2 for x in s) / len(s))`
- แต่ละรอบวัด variance ของช่วงเวลาหนึ่ง แล้วสะสมเข้า `band_e`
- ถ้าลืมเติม: `band_e` ว่าง feature vector เหลือแค่ 2 ตัว (mean, std) แท่ง band0..3 ไม่ขยับ

> นี่คือ feature "รูปร่างตามเวลา" — ถ้าเปลี่ยนจากแบ่ง**เวลา**เป็นแบ่ง**ความถี่** (เอา FFT จาก บทเรียน 4.3–4.4 มาจัดย่าน) ก็จะกลายเป็น spectrogram ของเสียงทันที

---

# ไล่โค้ด (4) — เลื่อนหน้าต่าง (ให้ซ้อน)

**ช่องเติมที่ 5**: หลังคำนวณ feature เสร็จ ต้องเลื่อนหน้าต่างให้ซ้อนกับอันต่อไป:

```python
if len(buf) >= WIN:
    fv = features(buf[-WIN:])              # บีบ WIN จุดท้ายเป็น feature
    ...
    for i, v in enumerate(fv):
        bars[i].value(min(100, int(abs(v) * (2 if i < 2 else 0.02))))
    # เติม: เก็บเฉพาะ WIN จุดท้ายไว้ให้หน้าต่างถัดไปซ้อน 50%  ->  buf = buf[-WIN:]
    pass
```

- แทน `pass` ด้วย `buf = buf[-WIN:]` — ตัด buffer ให้เหลือแค่ WIN จุดท้าย
- รอบหน้าเราจะเติมอีก HOP จุด แล้วหน้าต่างใหม่จะซ้อนกับอันเดิม 50%
- ถ้าลืมเติม: `buf` โตขึ้นเรื่อย ๆ ไม่มีที่สิ้นสุด → กินหน่วยความจำจนหมด (memory leak)

> `buf[-WIN:]` เป็นสำนวน Python ที่หมายถึง "เอาแค่ WIN ตัวท้าย" — เข้าใจมันแล้วคุณคุมหน้าต่างเลื่อนได้ทั้งหมด

---

# ไล่โค้ด (5) — แสดง feature เป็นแท่ง

ส่วนแสดงผล เอา feature vector มาสเกลให้พอเห็นแล้วตั้งค่าแท่ง (ให้ไว้แล้วในไฟล์ฝึก):

```python
for i, v in enumerate(fv):
    scaled = min(100, int(abs(v) * (2 if i < 2 else 0.02)))
    bars[i].value(scaled)
lcd.console(" fv = [" + ", ".join("%.2f" % v for v in fv) + "]")
```

- `mean`/`std` ค่าน้อย (index < 2) คูณ 2 พอเห็น · `band` ค่าใหญ่ คูณ 0.02 กันล้นแท่ง
- `abs(v)` เพราะ `mean` ติดลบได้ แต่แท่งเริ่มที่ 0
- `lcd.console(...)` พิมพ์ค่าจริงเป็นข้อความ — ดูตัวเลขเป๊ะ ๆ ควบคู่กับแท่ง

> การสเกลนี้เป็นแค่ "ให้เห็นด้วยตา" — ตอนป้อนโมเดลจริง เราจะ **normalize** อย่างเป็นระบบ (โมดูล 5 (Training)) ไม่ใช่คูณค่าคงที่แบบนี้ แต่หลักการ "ทำให้ทุก feature อยู่สเกลใกล้กัน" เหมือนกัน

---

# ลงมือ (1) — รันบน BENTO Emulator

ไม่มีบอร์ดก็เริ่มได้เลย:

1. เปิด **ide.tesaiot.dev** (BENTO Emulator) ในเบราว์เซอร์
2. เปิดไฟล์ [`s10_windowing.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l06-windowing-lab/practice/s10_windowing.py)
3. กด **Run** — จะเห็นแท่ง feature 6 ตัว (mean/std/band0..3) + ตัวนับ windows
4. ใช้ตัวจำลอง IMU: สลับ "วางนิ่ง" กับ "เขย่า" ดูแท่ง `std` และ band ขยับตาม
5. สังเกต `windows:` เพิ่มขึ้นทุกครั้งที่บีบ feature ชุดใหม่ (ทุก HOP จุด)

> Emulator ใช้ IMU **จำลอง** แต่ pipeline window→feature เหมือนบอร์ดจริงทุกบรรทัด — ซ้อมที่บ้านได้เต็มที่

---

# หน้าตาจริงบน Emulator

รันแล้วจอจะขึ้นแท่ง feature ทั้ง 6 ตัว ขยับตามสัญญาณ IMU จำลองแบบเรียลไทม์

รันบน BENTO Edge AI Emulator ในเบราว์เซอร์ได้ ไม่ต้องมีบอร์ดก็เห็น feature vector ขยับสด

- แท่งซ้ายสองอันคือ `mean` / `std` (สถิติทั้งหน้าต่าง) · สี่อันถัดไปคือ `band0..3` (พลังงานต่อช่วงเวลา)
- ลองสลับ "วางนิ่ง" กับ "เขย่า" ในตัวจำลอง แล้วดู `std` พุ่งขึ้นชัด ๆ

> จอนี้คือ MVP ของชุดบทเรียนนี้ตอนรันบน emulator — 6 แท่งเดียวกันจะขึ้นเหมือนกันเมื่อ Program to Device ลงบอร์ดจริง

---

# ลงมือ (2) — รันบนบอร์ด BENTO จริง

บนบอร์ดจริงใช้ IMU จริง:

1. เสียบบอร์ดเข้าคอมด้วยสาย USB
2. เปิด [`s10_windowing.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l06-windowing-lab/practice/s10_windowing.py) ใน **BENTO IDE** กด **Program to Device**
3. **วางบอร์ดนิ่งบนโต๊ะ** — ดู `std` ต่ำ แท่งแทบไม่ขยับ
4. **เขย่าบอร์ดเบา ๆ** — `std` พุ่งขึ้น band ที่ตรงกับจังหวะสั่นสว่างขึ้น
5. ลอง **หมุน/เอียง** ช้า ๆ — `mean` เปลี่ยน (ทิศแรงโน้มถ่วงต่อแกน Z เปลี่ยน) แต่ `std` ยังต่ำ

> จุดที่ควรสังเกต: `mean` กับ `std` เล่าคนละเรื่อง — `mean` = ท่าทางคงที่ (เอียงแค่ไหน), `std` = การเคลื่อนไหว (สั่นแค่ไหน) นี่คือเหตุผลที่เราต้องมีหลาย feature

---

# ลงมือทำ — เติมช่องว่างทั้ง 5 จุด

เปิด [`s10_windowing.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l06-windowing-lab/practice/s10_windowing.py) มี `# เติม:` วางไว้ **5 จุด**:

| # | จุด | เติมด้วย | ถ้าลืม |
|---|---|---|---|
| 1 | ในลูปเก็บ sample | `buf.append(az)` | หน้าต่างไม่ครบ แท่งไม่ขยับ |
| 2 | ใน `features()` | `mean = sum(win) / n` | แท่ง mean/std ค้างที่ 0 |
| 3 | ใน `features()` | `std = math.sqrt(sum((x-mean)**2 for x in win)/n)` | แท่ง std ค้างที่ 0 |
| 4 | ใน loop band | `band_e.append(sum((x-m)**2 for x in s)/len(s))` | band0..3 ไม่ขยับ |
| 5 | หลังบีบ feature | `buf = buf[-WIN:]` | buffer โตไม่หยุด (memory leak) |

ขั้นตอน:

1. ไล่หา `# เติม:` ทีละจุด แทน `pass`/`0.0` ด้วยคำสั่งตามคำใบ้
2. กด **Run** (Emulator) หรือ **Program to Device** (บอร์ด)
3. วางนิ่งสลับเขย่า ดูแท่งขยับ ถ้าไม่ขยับ กลับมาเช็ก indent + ลำดับ mean→std

> ห้าช่องนี้คือทั้ง pipeline ของ feature front-end — เติมครบเมื่อไร คุณสร้าง "สิ่งที่โมเดลเห็น" ได้ด้วยมือเอง

---

# แหล่งเรียนรู้เพิ่มเติม

อยากเข้าใจ spectrogram / mel filterbank / feature extraction ให้ลึกขึ้น ลองดูของดีเหล่านี้:

**วิดีโอ (ภาพสวย เข้าใจง่าย)**

- Fourier Transform เชิงภาพ (รากของ FFT/spectrogram) — ช่อง 3Blue1Brown: https://www.youtube.com/@3blue1brown
- Spectrogram & audio feature extraction ด้วย Python — ช่อง Sentdex: https://www.youtube.com/@sentdex
- Simple audio recognition (mel spectrogram เป็น input โมเดล) — TensorFlow docs: https://www.tensorflow.org/tutorials/audio/simple_audio

**ภาพ / บทความอ้างอิง**

- Spectrogram — บทความ + ภาพตัวอย่าง: https://en.wikipedia.org/wiki/Spectrogram  (ที่มา: Wikimedia Commons / Wikipedia, CC BY-SA)
- Mel scale & mel filterbank: https://en.wikipedia.org/wiki/Mel_scale  (ที่มา: Wikipedia, CC BY-SA)
- Hann / window function: https://en.wikipedia.org/wiki/Window_function  (ที่มา: Wikipedia, CC BY-SA)

> วิดีโอ/ภาพภายนอกเป็นของเจ้าของต้นฉบับ ใช้เพื่อการศึกษา อ้างอิงลิงก์ต้นทาง

---

# ชัยชนะที่เห็นได้ + MVP ของชุดบทเรียนนี้

<div style="text-align:center;margin:14px 0">
<div style="display:inline-block;background:#e8f5e9;border:2px solid #2e7d32;border-radius:22px;padding:10px 22px;color:#2e7d32;font-weight:700;font-size:1.05em">
ชัยชนะที่เห็นได้ของชุดบทเรียนนี้ · feature vector 6 ตัวที่บีบจากสัญญาณ IMU ดิบ เปลี่ยนตามการเคลื่อนไหวจริงบนจอ
</div>
</div>

**MVP ของบทเรียน 4.5–4.6 (เกณฑ์ผ่านของชุดบทเรียน):** คุณสร้าง **feature vector จากสัญญาณดิบด้วยมือเอง** — ตัดหน้าต่าง (window+hop) แล้วบีบเป็น `mean/std/band` ที่เปลี่ยนตามการเคลื่อนไหว

- ทำบน **Emulator** หรือ **บอร์ดจริง** ก็ได้ (โค้ดชุดเดียวกัน)
- อธิบายได้ว่า window/hop คืออะไร ทำไมต้องซ้อน และ `std` บอกอะไร

> "สร้าง feature ได้" ไม่ใช่แค่ "เห็นแท่งขยับ" — คุณต้องบอกได้ว่าทำไมวางนิ่งแล้ว `std` ต่ำ และ feature vector นี้จะกลายเป็น dataset ของโมดูล 5 (Training) ยังไง

---

# บันไดช่วยเหลือ — ใบ้ → เริ่มจากโครง → เฉลย → ฉบับเต็ม

ถ้าติด ให้ไต่บันไดนี้ทีละขั้น อย่าเพิ่งกระโดดไปดูเฉลย เพราะของจะเข้าหัวตอนที่คุณพยายามเองก่อน:

- **ใบ้** — คำใบ้อยู่ในคอมเมนต์ `# เติม:` ทั้ง 5 จุดในไฟล์ฝึก + ตารางหน้าที่แล้ว บอกว่าแต่ละช่องเติมอะไร
- **เริ่มจากโครง** — [`s10_windowing.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l06-windowing-lab/practice/s10_windowing.py) มีโครงครบทั้งไฟล์แล้ว เหลือแค่ 5 บรรทัดให้เติม
- **เฉลย** — [`s10_windowing.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l06-windowing-lab/solution/s10_windowing.py) เติมครบพร้อมคอมเมนต์อธิบายทุกช่อง (อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์เอง)
- **ฉบับเต็ม** — [`s10_windowing_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l06-windowing-lab/examples/s10_windowing_full.py) ฉบับขัดเรียบร้อย เพิ่มการเน้นย่านที่แรงสุด + ตัดสิน "นิ่ง/ขยับ" จาก `std` + อัตราหน้าต่างต่อวินาที

> ลองเขียนเองให้สุดก่อนนะ ถ้าติดจริง ๆ ค่อยเปิดเฉลยดูทีละช่อง แล้วกลับมาพิมพ์เอง — เดี๋ยวเราค่อย ๆ แกะไปด้วยกัน

---

# เชื่อมโยงรากฐาน — วันนี้เราแตะอะไรไปบ้าง

การสร้าง feature front-end ด้วยมือ ซ่อนแนวคิด Analysis หลายชั้นที่จะใช้ต่อในโมดูล 5 (Training):

**ฝั่ง DSP / Analysis**
- **Windowing + hop** — ตัดสัญญาณต่อเนื่องเป็นหน้าต่างซ้อนกัน (หัวใจของทุก front-end)
- **Feature vector** — บีบ 50 จุด → 6 ตัวเลข เก็บลักษณะเด่นไว้
- **std = variance** — เอาแนวคิดจาก บทเรียน 3.1–3.2 มาใช้เป็น feature โดยตรง
- **band energy → spectrogram** — แบ่งย่าน (เวลา/ความถี่) คือแกนของ mel spectrogram

**ฝั่ง MicroPython / โครงโปรแกรม**
- **buffer + slicing** — `buf.append` / `buf[-WIN:]` คุมหน้าต่างเลื่อน
- **สร้าง widget ครั้งเดียว** — แท่ง 6 อันสร้างนอกลูป ในลูปแค่ `.value()`
- **pure Python บน CM33** — feature front-end ไม่ต้องพึ่ง NPU

> ทั้งหมดนี้คือ "สิ่งที่โมเดลเห็น" — ชุดบทเรียนถัดไป (บทเรียน 5.1–5.2) เราจะเก็บ feature vector พวกนี้พร้อม label กลายเป็น dataset จริงที่เอาไปฝึกโมเดลได้

---

# ใช้จริงที่ไหน — feature front-end ในโลกจริง

pipeline window→feature ที่เราทำวันนี้ ไม่ใช่ของสมมติ ทุกโมเดล Edge AI จริงมี front-end แบบนี้ก่อนถึงตัวโมเดลเสมอ:

<div style="text-align:center;margin:6px 0">
<svg width="880" height="210" viewBox="0 0 880 210" font-family="DejaVu Sans, sans-serif">
  <rect x="12" y="10" width="420" height="92" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="28" y="34" font-size="13" font-weight="700" fill="#1565c0">เสียง (MIC) — mel spectrogram</text>
  <text x="28" y="56" font-size="11" fill="#555">Baby Cry · Cough · Alarm · Siren ทุกตัวกิน spectrogram</text>
  <text x="28" y="76" font-size="11" fill="#555">window → FFT → mel band → log = input โมเดล</text>
  <text x="28" y="94" font-size="11" fill="#888">โครงเดียวกับ band energy วันนี้ แค่ย่านเป็นความถี่</text>
  <rect x="448" y="10" width="420" height="92" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="464" y="34" font-size="13" font-weight="700" fill="#2e7d32">ท่าทาง (IMU) — สถิติต่อหน้าต่าง</text>
  <text x="464" y="56" font-size="11" fill="#555">นับก้าว · ตรวจล้ม · รู้ท่าออกกำลัง</text>
  <text x="464" y="76" font-size="11" fill="#555">mean/std/energy ต่อหน้าต่าง = feature</text>
  <text x="464" y="94" font-size="11" fill="#888">คือ Motion Detection ที่เราเล่นบทเรียน 1.1–1.3</text>
  <rect x="12" y="114" width="420" height="86" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="28" y="138" font-size="13" font-weight="700" fill="#e65100">เรดาร์ (RADAR) — range/doppler</text>
  <text x="28" y="160" font-size="11" fill="#555">ตรวจการมี-ไม่มีคน · ท่ากวักมือ</text>
  <text x="28" y="180" font-size="11" fill="#555">แต่ละเฟรมเรดาร์บีบเป็น feature ก่อนเข้าโมเดล</text>
  <rect x="448" y="114" width="420" height="86" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="464" y="138" font-size="13" font-weight="700" fill="#6a1b9a">ร่วมกัน — front-end ต้องตรงกันเสมอ</text>
  <text x="464" y="160" font-size="11" fill="#555">ตอนฝึกกับตอนใช้ ต้องบีบ feature แบบเดียวกันเป๊ะ</text>
  <text x="464" y="180" font-size="11" fill="#555">ไม่งั้นโมเดลเพี้ยน — บั๊กคลาสสิกของ Edge AI</text>
</svg>
</div>

> 6 โมเดลที่เล่นตั้งแต่บทเรียน 1.1–1.3 ทุกตัวมี feature front-end แบบนี้ซ่อนอยู่ วันนี้เราแค่เปิดฝากล่องมาทำเอง

---

# สะพานสู่ Training — dataset คือชุดของ feature vector

feature vector ที่เราสร้างวันนี้ ไม่ได้จบแค่โชว์บนจอ — มันคือ **หน่วยข้อมูลของ dataset** ในโมดูล 5 (Training)

<div style="text-align:center;margin:8px 0">
<svg width="820" height="110" viewBox="0 0 820 110" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arBr" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="34" width="200" height="52" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="114" y="58" font-size="12" font-weight="700" fill="#e65100" text-anchor="middle">4.5–4.6 (นี่)</text>
  <text x="114" y="76" font-size="11" fill="#666" text-anchor="middle">feature vector หนึ่งชุด</text>
  <rect x="300" y="34" width="220" height="52" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="410" y="58" font-size="12" font-weight="700" fill="#2e7d32" text-anchor="middle">5.1–5.2 — เก็บหลายชุด + label</text>
  <text x="410" y="76" font-size="11" fill="#666" text-anchor="middle">dataset (CSV)</text>
  <rect x="606" y="34" width="200" height="52" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="706" y="58" font-size="12" font-weight="700" fill="#6a1b9a" text-anchor="middle">5.3–5.5 — ฝึกโมเดล</text>
  <text x="706" y="76" font-size="11" fill="#666" text-anchor="middle">TensorFlow (Docker)</text>
  <line x1="214" y1="60" x2="298" y2="60" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arBr)"/>
  <line x1="520" y1="60" x2="604" y2="60" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arBr)"/>
</svg>
</div>

- ในบทเรียน 5.1–5.2 เราจะทำแบบวันนี้ แต่ **ติด label** (เช่น "นิ่ง"/"เขย่า") แล้วเก็บลง CSV
- CSV นั้นคือ dataset ที่ บทเรียน 5.3–5.5 เอาไปฝึกโมเดลใน TensorFlow
- เข้าใจ feature front-end วันนี้ = เข้าใจว่า dataset มาจากไหน ไม่ใช่กล่องดำ

> นี่คือเหตุผลที่คอร์สนี้จัด Analysis ไว้ **ก่อน** Training — คุณต้องรู้ว่า "โมเดลเห็นอะไร" ก่อนจะฝึกมันได้อย่างเข้าใจ

---

# งานทำเอง + สรุปบทเรียน

**งานทำเอง (ท้ายบทเรียน):**

1. เติม [`s10_windowing.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l06-windowing-lab/practice/s10_windowing.py) ให้ครบทั้ง 5 ช่อง รันได้จริง (Emulator หรือบอร์ด)
2. วางนิ่งกับเขย่า แล้วจดค่า `std` ทั้งสองกรณี — ต่างกันกี่เท่า? อธิบายว่าทำไม
3. ลองเปลี่ยน `HOP` เป็น `WIN` (ไม่ซ้อน) แล้วสังเกตว่าอัตราหน้าต่าง (`windows:`) เปลี่ยนยังไง และเสี่ยงพลาดอะไร

ใบ้ข้อ 3 — `HOP` เล็กลง = ได้ feature ถี่ขึ้น (ตอบไว แต่เปลืองแรง) · `HOP` ใหญ่ = ห่างขึ้น (ประหยัด แต่อาจพลาดเหตุการณ์สั้น)

**วันนี้เราได้:** เข้าใจว่าโมเดลกิน feature vector ไม่ใช่สัญญาณดิบ · ทำ windowing + hop เอง · บีบหน้าต่างเป็น mean/std/band energy · เห็นว่ามันคือญาติของ mel spectrogram และคือ dataset ของชุดบทเรียนหน้า

> ชุดบทเรียนถัดไป (บทเรียน 5.1–5.2 — Training I) เราจะเอา feature front-end นี้ไปเก็บเป็น **dataset จริง** พร้อม label แล้วเตรียมข้อมูลให้พร้อมฝึกโมเดล เจอกันครับ
