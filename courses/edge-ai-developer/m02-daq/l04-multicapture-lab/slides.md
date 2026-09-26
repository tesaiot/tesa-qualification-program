---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 2.4 — ลงมือทำ: เก็บ IMU กับเสียงลงไฟล์เดียว"
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

# บทเรียน 2.4 — ลงมือทำ: เก็บ IMU กับเสียงลงไฟล์เดียว

## DAQ II: เก็บเสียง + หลายเซนเซอร์บนเส้นเวลาเดียว · มัดสองสัญญาณให้เป็น dataset เดียว

**โมดูล 2 — เก็บข้อมูลจากเซนเซอร์ (DAQ)**

> ต่อจากบทเรียน 2.3 — เสียงและหลายเซนเซอร์บนเส้นเวลาเดียว: PDM 16 kHz ประทับเวลา และ jitter

---

# โครงของ multi-sensor capture — 4 ก้าวในลูป

หัวใจทั้งหมดอยู่ใน `record()` ตรงลูป `for _ in range(BURST)` แต่ละรอบเดินสี่ก้าวนี้เป๊ะ:

<div style="text-align:center;margin:6px 0">
<svg width="900" height="140" viewBox="0 0 900 140" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="ar4b" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="16" y="44" width="196" height="56" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="114" y="68" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">1 · ประทับเวลา</text>
  <text x="114" y="88" font-size="11" fill="#666" text-anchor="middle">t_ms = ticks_diff</text>
  <rect x="238" y="44" width="196" height="56" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="336" y="68" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">2 · อ่าน IMU</text>
  <text x="336" y="88" font-size="11" fill="#666" text-anchor="middle">bmi270.motion()</text>
  <rect x="460" y="44" width="196" height="56" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="558" y="68" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">3 · อ่าน MIC</text>
  <text x="558" y="88" font-size="11" fill="#666" text-anchor="middle">readinto + dbfs</text>
  <rect x="682" y="44" width="202" height="56" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="783" y="68" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">4 · เขียนแถว</text>
  <text x="783" y="88" font-size="11" fill="#666" text-anchor="middle">f.write(... t_ms ...)</text>
  <line x1="212" y1="72" x2="236" y2="72" stroke="#607d8b" stroke-width="2.4" marker-end="url(#ar4b)"/>
  <line x1="434" y1="72" x2="458" y2="72" stroke="#607d8b" stroke-width="2.4" marker-end="url(#ar4b)"/>
  <line x1="656" y1="72" x2="680" y2="72" stroke="#607d8b" stroke-width="2.4" marker-end="url(#ar4b)"/>
</svg>
</div>

- สี่ก้าวนี้คือสี่ช่องที่คุณต้องเติมในไฟล์ฝึก — เรียงตามนี้เป๊ะ
- ทั้งสี่ก้าวเกิดใน **รอบเดียว** จึงถือว่าอ่าน "เวลาเดียวกัน" ก่อน `sleep_ms(20)` ไปรอบถัดไป

> จำโครงสี่ก้าวนี้ไว้ แล้วโค้ดทั้งไฟล์จะอ่านเป็นประโยคเดียว: "ประทับเวลา อ่านสองเซนเซอร์ เขียนหนึ่งแถว วนใหม่"

---

# โครงของไฟล์ s05_multicapture.py

ทั้งไฟล์อ่านเป็นประโยคเดียว: **"เปิดไมค์ → กดปุ่ม label → วนเก็บ BURST แถว (แต่ละแถวมัด IMU+MIC บน t_ms) → ออกแล้วคืนไมค์"**

<div style="text-align:center;margin:6px 0">
<svg width="920" height="210" viewBox="0 0 920 210" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arS5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g font-size="14" text-anchor="middle">
    <rect x="14" y="24" width="180" height="54" rx="10" fill="#cfd8dc" stroke="#607d8b" stroke-width="2"/>
    <text x="104" y="47" font-weight="700" fill="#455a64">เปิดไมค์+ไฟล์</text>
    <text x="104" y="66" font-size="11" fill="#999">PDM_PCM :48</text>
    <rect x="226" y="24" width="180" height="54" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="316" y="47" font-weight="700" fill="#1565c0">สร้าง widget</text>
    <text x="316" y="66" font-size="11" fill="#999">ปุ่ม label :43</text>
    <rect x="438" y="24" width="180" height="54" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="528" y="47" font-weight="700" fill="#e65100">กดปุ่ม label</text>
    <text x="528" y="66" font-size="11" fill="#999">record() :70</text>
    <polygon points="700,51 750,23 800,51 750,79" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
    <text x="750" y="55" font-weight="700" fill="#6a1b9a" font-size="12">ออก?</text>
    <rect x="830" y="24" width="80" height="54" rx="10" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
    <text x="870" y="48" font-size="11" fill="#455a64">deinit</text>
    <text x="870" y="64" font-size="10" fill="#999">:finally</text>
    <rect x="226" y="132" width="196" height="58" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="324" y="152" font-weight="700" fill="#2e7d32">t_ms + IMU</text>
    <text x="324" y="170" font-size="11" fill="#999">เติม 1,2 :78,83</text>
    <text x="324" y="184" font-size="10" fill="#999">ประทับเวลา + motion()</text>
    <rect x="450" y="132" width="196" height="58" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="548" y="152" font-weight="700" fill="#e65100">MIC + เขียนแถว</text>
    <text x="548" y="170" font-size="11" fill="#999">เติม 3,4 :88,92</text>
    <text x="548" y="184" font-size="10" fill="#999">readinto + f.write</text>
  </g>
  <line x1="194" y1="51" x2="224" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS5)"/>
  <line x1="406" y1="51" x2="436" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS5)"/>
  <line x1="618" y1="51" x2="698" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS5)"/>
  <line x1="800" y1="51" x2="828" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS5)"/>
  <text x="816" y="43" font-size="11" fill="#607d8b">yes</text>
  <path d="M700,79 C640,120 340,110 324,130" fill="none" stroke="#2e7d32" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arS5)"/>
  <text x="520" y="112" font-size="12" fill="#2e7d32">no → วนเก็บ BURST แถว</text>
  <line x1="422" y1="161" x2="448" y2="161" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS5)"/>
  <text x="470" y="206" font-size="11" fill="#888" text-anchor="middle">แถวล่าง = สิ่งที่เกิดในลูป record() แต่ละรอบ</text>
</svg>
</div>

> ตัวเลขบรรทัด (`:78`, `:83`, `:88`, `:92`) ชี้ไปที่สี่ `# เติม:` ในไฟล์ฝึก จำโครงนี้ไว้ เดี๋ยวไล่ดูทีละส่วน

---

# ไล่โค้ด (1) — เปิด PDM + เตรียมไฟล์

ส่วนบนของไฟล์ (ให้ไว้แล้ว) เปิดไมโครโฟนหนึ่งครั้ง เตรียม buffer และเขียนหัวตาราง CSV ถ้ายังไม่มีไฟล์:

```python
pdm = PDM_PCM(0, sck="P8_5", data="P8_6", sample_rate=16000)
buf = array.array("h", (0 for _ in range(CHUNK)))

try:
    open(PATH, "r").close()             # มีไฟล์แล้วไหม
except OSError:
    with open(PATH, "w") as f:
        f.write("t_ms,label,ax,ay,az,gx,gy,gz,db\n")   # ยังไม่มี -> เขียนหัวตาราง
```

- เปิด PDM **นอกลูป** ครั้งเดียว เหมือนสร้าง widget ครั้งเดียว — เปิด/ปิดซ้ำๆ ทั้งกินเวลาและเสี่ยงชน
- หัวตาราง `t_ms,label,...` คือ schema ของ dataset — เขียนครั้งเดียวตอนไฟล์ยังว่าง

> `try: open(...,"r")` เป็นวิธีเช็ก "ไฟล์มีอยู่ไหม" แบบ MicroPython ถ้าไม่มีจะโยน `OSError` แล้วเราค่อยเขียนหัวตารางใหม่ — เก็บข้อมูลต่อท้ายได้โดยไม่ทับของเก่า

---

# ไล่โค้ด (2) — ประทับเวลา t_ms

**ช่องเติมที่ 1**: ก้าวแรกในลูป จับเวลาของแถวนี้เทียบจุดเริ่ม `t0`:

```python
t0 = time.ticks_ms()                    # (ให้ไว้แล้ว) จุดศูนย์ของชุดนี้
with open(PATH, "a") as f:
    for _ in range(BURST):
        # เติม 1: t_ms = time.ticks_diff(time.ticks_ms(), t0)
        t_ms = 0
        pass
```

- แทน `t_ms = 0` / `pass` ด้วย `t_ms = time.ticks_diff(time.ticks_ms(), t0)`
- นี่คือค่าเวลาที่ทั้ง IMU และ MIC ของแถวนี้จะใช้ร่วมกัน — หัวใจของคำว่า "sync"
- ถ้าลืมเติม: ทุกแถวจะมี `t_ms = 0` เหมือนกันหมด เส้นเวลาหาย จับคู่ตามเวลาไม่ได้

> `t0` ถูกตั้งใหม่ทุกครั้งที่กดปุ่ม label ดังนั้นแต่ละชุด (burst) เริ่มนับเวลาที่ ~0 ของตัวเอง — สะดวกเวลาเอาไปตัดหน้าต่างในโมดูล 4 (Analysis)

---

# ไล่โค้ด (3) — อ่าน IMU + MIC พร้อมกัน

**ช่องเติมที่ 2 และ 3**: อ่านสองเซนเซอร์ติดกันในรอบเดียว นี่คือจุดที่ทำให้ทั้งคู่ "เวลาเดียวกัน":

```python
# เติม 2: อ่านเซนเซอร์ตัวที่หนึ่ง (IMU 6 แกน)
ax = ay = az = gx = gy = gz = 0.0
pass                                    # -> ax, ay, az, gx, gy, gz = sensors.bmi270.motion()

# เติม 3: อ่านเซนเซอร์ตัวที่สอง (เสียงหนึ่งเฟรม)
pass                                    # -> pdm.readinto(buf)
db = dbfs(buf)                          # (ให้ไว้แล้ว) ย่อเฟรมเป็นระดับ dBFS
```

- ช่องที่ 2: แทน `pass` ด้วย `ax, ay, az, gx, gy, gz = sensors.bmi270.motion()` (ลบบรรทัด `= 0.0` ทิ้งได้)
- ช่องที่ 3: แทน `pass` ด้วย `pdm.readinto(buf)` — เติม buffer ด้วยเสียงชุดล่าสุด แล้ว `dbfs()` ย่อเป็นค่าเดียว
- อ่านสองอันติดกัน ห่างกันไม่กี่ไมโครวินาที จึงถือว่าเป็น "ช่วงเวลาเดียวกัน" ของแถวนี้ได้

> ลำดับสำคัญ: อ่านทั้งคู่ **ก่อน** เขียนแถว ถ้าเผลออ่าน MIC ในรอบนี้แต่เขียน IMU ของรอบก่อน ข้อมูลจะเหลื่อมเวลากันทันที

---

# ไล่โค้ด (4) — เขียนแถวที่มัดสองเซนเซอร์

**ช่องเติมที่ 4**: รวมทุกอย่างเป็นหนึ่งบรรทัด CSV ที่ทั้ง IMU และ MIC อ้าง `t_ms` เดียวกัน:

```python
# เติม 4: เขียนหนึ่งแถว
pass
# -> f.write("%d,%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.1f\n"
#            % (t_ms, label, ax, ay, az, gx, gy, gz, db))

level.value(max(0, int(db + 60)))       # (ให้ไว้แล้ว) โชว์ระดับเสียงสดๆ
time.sleep_ms(RATE_MS)                  # (ให้ไว้แล้ว) คุมจังหวะ ~50 Hz
```

- แทน `pass` ด้วย `f.write(...)` ตามรูปแบบในคำใบ้ — ลำดับคอลัมน์ต้องตรง schema หัวตาราง
- `%d` สำหรับ `t_ms` (จำนวนเต็ม ms), `%.4f` สำหรับค่า IMU, `%.1f` สำหรับ `db`
- ถ้าลืมเติม: ลูปวิ่งครบ แต่ไฟล์ว่างเปล่า (จำนวนแถวขึ้นบนจอ แต่ CSV ไม่มีข้อมูล)

> `sleep_ms(RATE_MS)` คือสิ่งที่ทำให้แถวห่างกัน ~20 ms อย่าเอาออก ไม่งั้นลูปจะรัวจนอัตราสูงเกินและ jitter พุ่ง

---

# ไล่โค้ด (5) — เก็บกวาด: คืนไมโครโฟน

ปุ่ม Stop ไม่มีในตัวนี้ (เก็บทีละชุดจบในตัว) แต่ต้อง **คืนฮาร์ดแวร์ตอนออก** เสมอ:

```python
finally:
    pdm.deinit()                        # คืนไมโครโฟนให้ระบบเสมอ
    lcd.console("<span class=ok> จบ: %d แถวใน %s</span>" % (total, PATH))
```

- `pdm.deinit()` อยู่ใน `finally` — ไม่ว่าจะออกด้วยปุ่ม back หรือ error ไมโครโฟนจะถูกปิดเสมอ
- ถ้าไม่ปิด: รันโปรแกรมเสียงตัวถัดไปอาจเปิด PDM ซ้ำไม่ได้ (ฮาร์ดแวร์ยังถูกจอง)

> นิสัย embedded เดิมจากบทเรียน 1.1–1.3: **ออกจากงานยังไง ทิ้งเครื่องไว้ให้เรียบร้อยแบบนั้น** — ชุดบทเรียนนี้ "เครื่อง" คือไมโครโฟน PDM

---

# ลงมือทำ — เติมช่องว่างทั้ง 4 จุด

เปิด [`s05_multicapture.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m02-daq/l04-multicapture-lab/practice/s05_multicapture.py) ในไฟล์มี `# เติม:` วางไว้ **4 จุด** ตรงสี่ก้าวของลูปเก็บข้อมูล:

| # | ก้าว | เติมด้วย | ถ้าลืม |
|---|---|---|---|
| 1 | ประทับเวลา | `t_ms = time.ticks_diff(time.ticks_ms(), t0)` | ทุกแถว t_ms = 0 |
| 2 | อ่าน IMU | `ax, ay, az, gx, gy, gz = sensors.bmi270.motion()` | คอลัมน์ IMU เป็น 0 |
| 3 | อ่าน MIC | `pdm.readinto(buf)` | คอลัมน์ db นิ่ง ไม่ตามเสียง |
| 4 | เขียนแถว | `f.write("%d,%s,%.4f,...,%.1f\n" % (...))` | ไฟล์ว่าง แถวไม่ถูกเขียน |

ขั้นตอน:

1. ไล่หา `# เติม:` ทีละจุด แล้วแทน `pass` ด้วยคำสั่งตามคำใบ้
2. กด **Program to Device** (ชุดบทเรียนนี้ต้องบอร์ดจริง — ดูสไลด์ถัดไปว่าทำไม)
3. เลือก label ทำท่า + ส่งเสียงพร้อมกัน ดูจำนวนแถวขึ้น แล้วเปิด CSV ตรวจ

> สี่ช่องนี้คือสี่ก้าวของ DAQ หลายเซนเซอร์เป๊ะ — เติมครบเมื่อไร คุณได้ dataset ที่ทุกแถวมัดเสียงกับการเคลื่อนไหวบนเวลาเดียว

---

# ลงมือ — เสียงจริงต้องใช้บอร์ดจริง

ต่างจากชุดบทเรียนก่อน ๆ เสียงจริงต้องมาจาก **บอร์ด BENTO จริง** (Emulator มี `PDM_PCM` จำลองที่ส่งเสียงสังเคราะห์ ให้ลองโครงโปรแกรมได้ แต่ไม่ใช่เสียงจริง):

1. เสียบบอร์ด BENTO AI Kit เข้าคอมด้วยสาย USB
2. เปิด [`s05_multicapture.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m02-daq/l04-multicapture-lab/practice/s05_multicapture.py) ใน **BENTO IDE** กด **Program to Device**
3. บนจอขึ้นปุ่ม label 3 ปุ่ม + แถบระดับเสียง
4. กด **shaking** แล้ว **เขย่าบอร์ดพร้อมส่งเสียง** ~4 วินาที ดูแถบเสียงขยับ + จำนวนแถวเพิ่ม
5. ทำครบ idle / circle / shaking แล้วกด **< ออก** ไฟล์อยู่ที่ `/multicapture.csv`

> ส่วน IMU กับการเขียน CSV คุณซ้อมแนวคิดได้บน Emulator (จากบทเรียน 2.1–2.2) แต่การอ่านเสียงจริงต้องมาที่บอร์ด — และโปรแกรมเสียงที่รันผ่านบน Emulator ยังไม่ใช่หลักฐานว่าจะรันผ่านบนบอร์ด

---

# หน้าจอที่จะเห็นบนบอร์ด (ภาพจำลอง)

ภาพด้านล่างเป็น **ภาพวาดจำลองหน้าจอ** ให้เห็นล่วงหน้าว่า เมื่อ Program to Device สำเร็จ จอจะมีปุ่ม label สามปุ่ม แถบระดับเสียงสด และตัวนับแถว

<div style="text-align:center;margin:8px 0">
<svg width="720" height="320" viewBox="0 0 720 320" font-family="DejaVu Sans, sans-serif">
  <rect x="10" y="10" width="700" height="300" rx="16" fill="#0d1117" stroke="#30363d" stroke-width="3"/>
  <rect x="26" y="26" width="668" height="40" rx="8" fill="#161b22"/>
  <text x="42" y="52" font-size="16" font-weight="700" fill="#7ee787">s05_multicapture</text>
  <text x="678" y="52" font-size="14" fill="#8b949e" text-anchor="end">BENTO AI Kit</text>
  <rect x="40" y="86" width="180" height="60" rx="10" fill="#1565c0"/>
  <text x="130" y="123" font-size="18" font-weight="700" fill="#fff" text-anchor="middle">idle</text>
  <rect x="270" y="86" width="180" height="60" rx="10" fill="#2e7d32"/>
  <text x="360" y="123" font-size="18" font-weight="700" fill="#fff" text-anchor="middle">circle</text>
  <rect x="500" y="86" width="180" height="60" rx="10" fill="#ef6c00"/>
  <text x="590" y="123" font-size="18" font-weight="700" fill="#fff" text-anchor="middle">shaking</text>
  <text x="40" y="185" font-size="14" fill="#8b949e">ระดับเสียง (dBFS)</text>
  <rect x="40" y="196" width="540" height="30" rx="6" fill="#21262d" stroke="#30363d" stroke-width="1.5"/>
  <rect x="42" y="198" width="352" height="26" rx="5" fill="#4a90d9"/>
  <text x="620" y="219" font-size="22" font-weight="700" fill="#79c0ff" text-anchor="middle">-38</text>
  <text x="40" y="262" font-size="15" fill="#e6edf3">label: <tspan fill="#ffa657" font-weight="700">shaking</tspan>    rows: <tspan fill="#7ee787" font-weight="700">128</tspan></text>
  <rect x="26" y="276" width="668" height="26" rx="6" fill="#161b22"/>
  <text x="42" y="294" font-size="13" fill="#8b949e">console: เก็บ 128 แถว -&gt; /multicapture.csv</text>
</svg>
</div>

- แตะปุ่ม label (idle / circle / shaking) = ตั้ง `t0` ใหม่แล้วเริ่มเก็บ BURST แถวของชุดนั้น
- แถบ VU ยาว-สั้นตาม `db` แบบ realtime ตามบรรทัด `level.value(max(0, int(db + 60)))`
- บรรทัดล่างคือ console บอกจำนวนแถวสะสมและ path ไฟล์ `/multicapture.csv`

> ภาพนี้วาดมือเพื่อให้นึกหน้าจอออกก่อนถึงบอร์ดจริง ตัวเลข (-38 dBFS, 128 แถว) เป็นตัวอย่าง ของจริงจะวิ่งตามเสียงและท่าที่คุณทำ

---

# ทำไมเสียงจริงต้องใช้บอร์ด

Emulator จำลอง IMU / env / dsp / ui ได้ครบ ส่วน **ไมโครโฟน PDM จำลองด้วยเสียงสังเคราะห์** ไม่ใช่เสียงจริง และบน TESAIoT Dev Kit (ที่มี audio codec) การเปิด PDM ยังชนกับ clock ของระบบเสียง CM55

<div style="text-align:center;margin:6px 0">
<svg width="820" height="130" viewBox="0 0 820 130" font-family="DejaVu Sans, sans-serif">
  <rect x="20" y="30" width="240" height="72" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="140" y="56" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">Emulator</text>
  <text x="140" y="78" font-size="11" fill="#555" text-anchor="middle">IMU/env/dsp/ui ได้</text>
  <text x="140" y="94" font-size="11" fill="#c62828" text-anchor="middle">PDM เสียงสังเคราะห์</text>
  <rect x="290" y="30" width="240" height="72" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="410" y="56" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">BENTO AI Kit</text>
  <text x="410" y="78" font-size="11" fill="#2e7d32" text-anchor="middle">PDM ใช้ได้เต็ม</text>
  <text x="410" y="94" font-size="11" fill="#555" text-anchor="middle">ชุดบทเรียนนี้ใช้ตัวนี้</text>
  <rect x="560" y="30" width="240" height="72" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="680" y="56" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">Dev Kit (codec)</text>
  <text x="680" y="78" font-size="11" fill="#c62828" text-anchor="middle">PDM ชน clock เสียง</text>
  <text x="680" y="94" font-size="11" fill="#555" text-anchor="middle">รอ firmware guard</text>
</svg>
</div>

- นี่คือความจริงของงานฮาร์ดแวร์: ความสามารถบางอย่างผูกกับตัวชิป ตัวจำลองยังตามไม่ครบ
- หลักสูตรจึงจัดชุดบทเรียนนี้ให้เก็บเสียงจริงบนบอร์ดเท่านั้น ชัดเจน ไม่กลบเกลื่อน

> ความซื่อตรงเรื่องนี้สำคัญ: เราบอกตรงๆ ว่าอะไรรันที่ไหนได้ ไม่หลอกว่า Emulator ทำได้ทุกอย่าง — คุณจะได้วางแผนบทเรียนถูก

---

# ตรวจ dataset — เปิด CSV ดูของจริง

เก็บเสร็จแล้วอย่าเพิ่งเชื่อ ตรวจก่อน ดึงไฟล์ออกด้วย BENTO IDE (file transfer) หรือ `mpremote` แล้วเปิดดู:

```python
# ตรวจเร็วๆ ใน REPL บนบอร์ด: นับแถว + ดูหัว
n = 0
with open("/multicapture.csv") as f:
    head = f.readline()          # t_ms,label,ax,...,db
    for line in f:
        n += 1
print("rows:", n, "| header:", head.strip())
```

- เช็กสาม: (1) จำนวนแถว ~ `BURST × จำนวนครั้งที่กด`, (2) `t_ms` เพิ่มขึ้นเรื่อยๆ ต่อชุด, (3) `db` เปลี่ยนตามเสียงจริง
- ถ้า `db` นิ่งเป็น -96 ตลอด แปลว่าช่อง 3 (`readinto`) ยังไม่ได้เติม หรือไมค์ไม่ได้เสียง
- ถ้า `t_ms` เป็น 0 หมด แปลว่าช่อง 1 ยังไม่ได้เติม

> การ "เปิดไฟล์ดูจริง" คือทักษะ DAQ ที่ประเมินค่าไม่ได้ — dataset ที่ดูดีบนจอแต่ไฟล์เพี้ยน จะทำให้โมเดลที่ train ออกมาพังเงียบๆ ตรวจตั้งแต่ต้นทางเสมอ

---

# แหล่งเรียนรู้เพิ่มเติม

อยากเข้าใจ PDM / PCM และการเก็บ dataset ให้ลึกขึ้น ลองตามลิงก์เหล่านี้ได้ตามสะดวก (เปิดในเบราว์เซอร์):

**วิดีโอ (ภาษาอังกฤษ อธิบายเห็นภาพ)**
- Digital audio — การสุ่มเสียงเป็นตัวเลขทำงานยังไง — ช่อง Computerphile: https://www.youtube.com/@Computerphile
- A/D และ D/A sampling อธิบายด้วยของจริงบน oscilloscope — Xiph.org Digital Show & Tell: https://xiph.org/video/vid2.shtml
- The Fourier Transform เข้าใจแบบเห็นภาพ (ปูทางสู่ spectrogram ในบทเรียน 4.5–4.6) — ช่อง 3Blue1Brown: https://www.youtube.com/@3blue1brown

**ภาพ / บทความอ้างอิง (เปิดเสรี)**
- Pulse-density modulation (PDM) — https://en.wikipedia.org/wiki/Pulse-density_modulation (ที่มา: Wikipedia, CC BY-SA)
- Pulse-code modulation (PCM) พร้อมไดอะแกรมการสุ่ม — https://en.wikipedia.org/wiki/Pulse-code_modulation (ที่มา: Wikipedia / Wikimedia Commons, CC BY-SA)
- Nyquist–Shannon sampling theorem (ทำไม 16 kHz ถึงพอ) — https://en.wikipedia.org/wiki/Nyquist–Shannon_sampling_theorem (ที่มา: Wikipedia, CC BY-SA)

> วิดีโอ/ภาพภายนอกเป็นของเจ้าของต้นฉบับ ใช้เพื่อการศึกษา อ้างอิงลิงก์ต้นทาง เราลิงก์ไปหา ไม่ได้ฝังหรือทำซ้ำในสไลด์

---

# ชัยชนะที่เห็นได้ + MVP ของชุดบทเรียนนี้

<div style="text-align:center;margin:14px 0">
<div style="display:inline-block;background:#e8f5e9;border:2px solid #2e7d32;border-radius:22px;padding:10px 22px;color:#2e7d32;font-weight:700;font-size:1.05em">
ชัยชนะที่เห็นได้ของชุดบทเรียนนี้ · ไฟล์ dataset ที่ทุกแถวมัดทั้งเสียงและการเคลื่อนไหวไว้บนเวลาเดียวกัน
</div>
</div>

**MVP ของบทเรียน 2.3–2.4 (เกณฑ์ผ่านของชุดบทเรียน):** คุณเก็บ dataset ที่ log **≥2 เซนเซอร์บนเส้นเวลาเดียว** ได้จริง — ไฟล์ `/multicapture.csv` มีคอลัมน์ `t_ms` + IMU + `db` และค่าจริงเปลี่ยนตามท่า/เสียง

- ทำบน **บอร์ดจริง** (เสียงจริงต้องมาจากไมโครโฟนบนบอร์ด)
- อธิบายได้ว่าโค้ดประทับ `t_ms` ตรงไหน อ่านสองเซนเซอร์ตรงไหน และทำไมต้องอยู่ในรอบเดียว

> "เก็บได้" ไม่พอ ต้อง "เก็บตรงเวลา" — คุณต้องชี้ได้ว่าแถวไหนคือช่วงที่คุณเขย่า+ส่งเสียง และ `db` กับ IMU ในแถวนั้นสอดคล้องกัน

---

# บันไดช่วยเหลือ — ใบ้ → เริ่มจากโครง → เฉลย → ฉบับเต็ม

ถ้าติด ให้ไต่บันไดนี้ทีละขั้น อย่าเพิ่งกระโดดไปดูเฉลย เพราะของจะเข้าหัวตอนที่คุณพยายามเองก่อน:

- **ใบ้** — คำใบ้อยู่ในคอมเมนต์ `# เติม:` ทั้ง 4 จุดในไฟล์ฝึก + ตารางสี่ก้าวหน้าที่แล้ว บอกว่าแต่ละช่องเติมอะไร
- **เริ่มจากโครง** — [`s05_multicapture.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m02-daq/l04-multicapture-lab/practice/s05_multicapture.py) มีโครงครบทั้งไฟล์แล้ว (UI + เปิด PDM + `finally`) เหลือแค่ 4 บรรทัดในลูปให้เติม
- **เฉลย** — [`s05_multicapture.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m02-daq/l04-multicapture-lab/solution/s05_multicapture.py) เติมครบพร้อมคอมเมนต์อธิบายทุกก้าว (อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์เอง)
- **ฉบับเต็ม** — [`s05_multicapture_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m02-daq/l04-multicapture-lab/examples/s05_multicapture_full.py) เพิ่มเก็บ WAV เสียงดิบคู่ CSV + วัด `dt`/jitter จริง + สรุป peak dBFS ต่อ label ลง manifest

> ลองเขียนเองให้สุดก่อนนะ ถ้าติดจริงๆ ค่อยเปิดเฉลยดูทีละช่อง แล้วกลับมาพิมพ์เอง — เดี๋ยวเราค่อย ๆ แกะไปด้วยกัน

---

# เชื่อมโยงรากฐาน — วันนี้เราแตะอะไรไปบ้าง

การเก็บ dataset หลายเซนเซอร์ซ่อนแนวคิด DAQ หลายชั้นที่จะใช้ไปตลอดคอร์ส:

**ฝั่ง DAQ / dataset**
- **Shared timeline** — สองเซนเซอร์อ้าง `t_ms` เดียว จึงจับคู่/ตัดหน้าต่างตามเวลาได้
- **Audio front-end** — PDM → PCM → RMS → dBFS คือก้าวแรกก่อนทำ spectrogram (บทเรียน 4.5–4.6)
- **Sampling rate + jitter** — ตั้งอัตราด้วย `sleep_ms` แล้วตรวจด้วย `t_ms` จริง
- **Label ในไฟล์** — เก็บ label พร้อมข้อมูล = dataset พร้อม train

**ฝั่ง MicroPython / โครงโปรแกรม**
- **เปิดฮาร์ดแวร์ครั้งเดียว** — `PDM_PCM(...)` นอกลูป เหมือนสร้าง widget ครั้งเดียว
- **`ticks_ms` / `ticks_diff`** — คู่มาตรฐานวัดเวลาสั้นๆ กัน wrap-around
- **เก็บกวาดตอนจบ** — `finally: pdm.deinit()` คืนไมโครโฟนสู่สถานะที่รู้แน่

> ทั้งหมดต่อยอดจากบทเรียน 2.1–2.2 ตรงๆ — DAQ ไม่ใช่เรื่องเขียนใหม่ทุกครั้ง แต่คือ pattern ที่ขยายทีละเซนเซอร์

---

# ใช้จริงที่ไหน — multi-sensor dataset ในโลกจริง

การมัดหลายเซนเซอร์บนเวลาเดียว ไม่ใช่แบบฝึกหัด มันคือวิธีที่ dataset ระดับสินค้าถูกเก็บจริง:

<div style="text-align:center;margin:6px 0">
<svg width="880" height="200" viewBox="0 0 880 200" font-family="DejaVu Sans, sans-serif">
  <rect x="12" y="10" width="420" height="86" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="28" y="34" font-size="13" font-weight="700" fill="#1565c0">สุขภาพ — นาฬิกา/แพตช์</text>
  <text x="28" y="56" font-size="11" fill="#555">IMU + เสียง + ชีพจร บนเวลาเดียว</text>
  <text x="28" y="76" font-size="11" fill="#555">แยก "ไอ" จาก "ขยับตัว" ต้องดูหลายสัญญาณ</text>
  <rect x="448" y="10" width="420" height="86" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="464" y="34" font-size="13" font-weight="700" fill="#2e7d32">โรงงาน — ตรวจเครื่องจักร</text>
  <text x="464" y="56" font-size="11" fill="#555">สั่นสะเทือน (IMU) + เสียง (MIC) พร้อมกัน</text>
  <text x="464" y="76" font-size="11" fill="#555">จับความผิดปกติที่สัญญาณเดียวมองไม่เห็น</text>
  <rect x="12" y="104" width="420" height="86" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="28" y="128" font-size="13" font-weight="700" fill="#e65100">บ้าน — ตรวจเหตุการณ์</text>
  <text x="28" y="150" font-size="11" fill="#555">เรดาร์ (มีคน) + เสียง (เหตุการณ์) ยืนยันกัน</text>
  <text x="28" y="170" font-size="11" fill="#555">ลด false alarm เพราะสองสัญญาณต้องตรงกัน</text>
  <rect x="448" y="104" width="420" height="86" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="464" y="128" font-size="13" font-weight="700" fill="#6a1b9a">ร่วมกัน — เส้นเวลาคือกาว</text>
  <text x="464" y="150" font-size="11" fill="#555">ทุกงานเริ่มจาก dataset ที่ทุกสัญญาณตรงเวลา</text>
  <text x="464" y="170" font-size="11" fill="#888">คือทักษะที่คุณเพิ่งทำวันนี้</text>
</svg>
</div>

> ไฟล์ `/multicapture.csv` ที่คุณเพิ่งเก็บ ใช้หลักการเดียวกับ dataset ของสินค้าจริงเหล่านี้เป๊ะ — เราแค่ทำในสเกลเล็ก เพื่อจะย้อนไป train โมเดลเองในโมดูล 5 (Training)

---

# งานทำเอง + สรุปบทเรียน

**งานทำเอง (ท้ายบทเรียน):**

1. เติม [`s05_multicapture.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m02-daq/l04-multicapture-lab/practice/s05_multicapture.py) ให้ครบทั้ง 4 ช่อง รันบนบอร์ดจนได้ `/multicapture.csv`
2. เก็บครบ **3 label** (idle / circle / shaking) แต่ละ label ทำท่า + ส่งเสียงต่างกัน แล้วเปิด CSV ยืนยันว่า `db` และ IMU เปลี่ยนตามจริง
3. ตรวจเส้นเวลา: `t_ms` ในแต่ละชุดเพิ่มขึ้นเรื่อยๆ และห่างกันใกล้ 20 ms ไหม — จดว่าเจอ jitter ตรงไหน

ใบ้ข้อ 3 — ถ้าช่วงเวลาเพี้ยนมาก ลองลด `CHUNK` เสียง หรือลดงานในลูป แล้วเทียบ `t_ms` ใหม่

**วันนี้เราได้:** อ่านไมโครโฟน PDM เป็น dBFS · เข้าใจเส้นเวลาร่วม · อ่าน IMU+MIC ในลูปเดียว · เก็บ dataset หลายเซนเซอร์ที่ทุกแถวตรงเวลา (`t_ms` + IMU + `db`)

> ชุดบทเรียนถัดไป (บทเรียน 3.1–3.2) เราเข้าสู่ Pillar 2 (Processing) — เอาสัญญาณดิบที่เก็บมา แปลงเป็นปริมาณเชิงฟิสิกส์ (tilt / altitude / พลังงาน) แล้วโชว์เป็นเกจสดบนจอ เจอกันครับ
