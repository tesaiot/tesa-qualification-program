---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 4.4 — ลงมือทำ: สเปกตรัมสดจาก IMU"
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

# บทเรียน 4.4 — ลงมือทำ: สเปกตรัมสดจาก IMU

## Analysis II: FFT และโดเมนความถี่ · อ่านสเปกตรัมของสัญญาณจริง

**โมดูล 4 — วิเคราะห์สัญญาณ**

> ต่อจากบทเรียน 4.3 — FFT และโดเมนความถี่: bin, Nyquist, DC, leakage และ Hann window

---

# โครงของโปรแกรม s09 — pipeline 4 ขั้น

ทั้งไฟล์อ่านเป็นประโยคเดียว: **"เก็บ N จุด → ตัด DC → คูณ window → FFT → หา magnitude → หา peak → วาดแท่ง"** สี่ขั้นกลางคือช่องที่เราเติม

<div style="text-align:center;margin:6px 0">
<svg width="920" height="180" viewBox="0 0 920 180" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arPl" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g text-anchor="middle" font-size="12">
    <rect x="10" y="60" width="120" height="56" rx="9" fill="#cfd8dc" stroke="#607d8b" stroke-width="2"/>
    <text x="70" y="84" font-weight="700" fill="#455a64">เก็บ N จุด</text>
    <text x="70" y="102" font-size="10" fill="#888">IMU (ให้มา)</text>
    <rect x="150" y="60" width="120" height="56" rx="9" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="210" y="84" font-weight="700" fill="#e65100">1 · ตัด DC</text>
    <text x="210" y="102" font-size="10" fill="#888">mean</text>
    <rect x="290" y="60" width="120" height="56" rx="9" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="350" y="84" font-weight="700" fill="#e65100">2 · window</text>
    <text x="350" y="102" font-size="10" fill="#888">Hann</text>
    <rect x="430" y="60" width="120" height="56" rx="9" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
    <text x="490" y="84" font-weight="700" fill="#6a1b9a">fft()</text>
    <text x="490" y="102" font-size="10" fill="#888">ให้มา</text>
    <rect x="570" y="60" width="120" height="56" rx="9" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="630" y="84" font-weight="700" fill="#e65100">3 · magnitude</text>
    <text x="630" y="102" font-size="10" fill="#888">mag</text>
    <rect x="710" y="60" width="120" height="56" rx="9" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="770" y="84" font-weight="700" fill="#e65100">4 · peak</text>
    <text x="770" y="102" font-size="10" fill="#888">kmax</text>
    <rect x="840" y="60" width="72" height="56" rx="9" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="876" y="84" font-weight="700" fill="#2e7d32">วาด</text>
    <text x="876" y="102" font-size="10" fill="#888">แท่ง</text>
  </g>
  <line x1="130" y1="88" x2="148" y2="88" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arPl)"/>
  <line x1="270" y1="88" x2="288" y2="88" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arPl)"/>
  <line x1="410" y1="88" x2="428" y2="88" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arPl)"/>
  <line x1="550" y1="88" x2="568" y2="88" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arPl)"/>
  <line x1="690" y1="88" x2="708" y2="88" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arPl)"/>
  <line x1="830" y1="88" x2="838" y2="88" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arPl)"/>
  <text x="460" y="150" font-size="12" fill="#888" text-anchor="middle">กล่องสีส้ม 4 กล่อง = 4 ช่องที่คุณเติม · สีเทา/ม่วง/เขียว = ให้มาแล้ว</text>
</svg>
</div>

> เหมือนบทเรียน 1.1–1.3 ที่ยืนบน 4 คำสั่งของ `edge_ai` — ชุดบทเรียนนี้ยืนบน 4 ขั้นของ pipeline วิเคราะห์ความถี่ เติมครบเมื่อไร สเปกตรัมสดก็ขึ้นจอ

---

# โครงร่วมของทุกโปรแกรม MicroPython

สังเกตว่า s09 เดินตาม "โครงร่วม" เดียวกับทุกชุดบทเรียนที่ผ่านมา — จับโครงนี้ได้ อ่านโปรแกรมไหนบนบอร์ดก็ไม่หลง:

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
  <text x="338" y="84" font-size="11" fill="#666" text-anchor="middle">HALF แท่ง + ป้าย Hz</text>
  <rect x="466" y="40" width="190" height="56" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="561" y="64" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">3 · ลูป</text>
  <text x="561" y="84" font-size="11" fill="#666" text-anchor="middle">เก็บ->FFT->วาดแท่ง</text>
  <rect x="684" y="40" width="176" height="56" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="772" y="64" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">4 · ui.poll</text>
  <text x="772" y="84" font-size="11" fill="#666" text-anchor="middle">รับปุ่ม ออก</text>
  <line x1="210" y1="68" x2="236" y2="68" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <line x1="438" y1="68" x2="464" y2="68" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <line x1="656" y1="68" x2="682" y2="68" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <path d="M772,96 C772,116 561,116 561,98" fill="none" stroke="#9e9e9e" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arSk)"/>
  <text x="666" y="120" font-size="11" fill="#9e9e9e" text-anchor="middle">วนกลับ</text>
</svg>
</div>

- **สร้างครั้งเดียว**: `HALF` แท่งกับป้าย Hz สร้างก่อนลูป ในลูปแค่ `bars[k].value(...)` กับ `bars[k].color(...)` — ถ้าสร้างแท่งใหม่ทุกเฟรม จอกระพริบและกินหน่วยความจำ
- **ลูป**: หนึ่งรอบ = เก็บ N จุด → 4 ขั้น pipeline → วาดแท่ง แล้ววน
- **ออกอย่างเรียบร้อย**: `finally` อัปเดตข้อความปิด ไม่ทิ้งงานค้าง

> โครงเดียวกันนี้ใช้ได้กับทุกแอปบนบอร์ด — พอจับโครงได้ คุณจะอ่านโค้ดชุดบทเรียนอื่นได้เร็วขึ้นมาก เพราะรู้ว่าจะไปหาส่วนไหนตรงไหน

---

# รู้จักฟังก์ชัน fft() — ไม่ใช่กล่องดำ

ไฟล์ฝึกให้ `fft()` มาครบ (radix-2 Cooley-Tukey) เราไม่แก้ แต่มาดูว่ามันเป็นแค่การบวก-คูณเป็นระเบียบ:

```python
def fft(re, im):
    n = len(re)
    # 1) bit-reversal: จัดลำดับ input ให้ butterfly ทำงานในที่ได้
    ...
    # 2) butterflies: รวมผลทีละคู่ ไล่ขนาด 2,4,8,...,N
    length = 2
    while length <= n:
        ang = -2.0 * math.pi / length
        wr, wi = math.cos(ang), math.sin(ang)   # หมุนเวกเตอร์ทีละสเต็ป
        ...
        length <<= 1
    return re, im
```

- `re/im` เป็น list ยาว N คู่กัน (`im` เริ่มเป็น 0 เพราะสัญญาณจริงไม่มีส่วนจินตภาพ)
- แต่ละรอบ `length` ทวีคูณ (2 → 4 → 8 → …) นี่คือ "แบ่งครึ่งซ้ำ ๆ" ที่ทำให้เร็ว `N log N`

> อยากลองใน REPL ก็ได้: ป้อนคลื่นไซน์ที่เรารู้ความถี่เข้าไป แล้วดูว่า peak โผล่ที่ bin ที่คาดไว้ไหม — นี่คือวิธี "ตรวจสอบ FFT ด้วยตัวเอง" ที่ดีที่สุด

---

# ตรวจ FFT ด้วยไซน์ที่เรารู้คำตอบ

ก่อนเชื่อ FFT กับสัญญาณจริง มาลองกับไซน์ที่ **เรารู้ความถี่อยู่แล้ว** ถ้า peak โผล่ที่ bin ที่คำนวณได้ แปลว่า pipeline ถูก

```python
# สร้างไซน์ 6.25 Hz ที่ FS=50, N=32  ->  bin คาดหวัง = f*N/FS = 6.25*32/50 = 4
re = [math.sin(2*math.pi*6.25*i/FS) for i in range(N)]
im = [0.0]*N
fft(re, im)
mag = [math.sqrt(re[k]**2 + im[k]**2) for k in range(N//2)]
print(max(range(N//2), key=lambda k: mag[k]))   # ควรได้ 4
```

- ความถี่ `f` แปลงเป็น bin ด้วย `k = f * N / FS` (ผกผันกับ `f = k * FS / N`)
- ไซน์ 6.25 Hz → bin 4 พอดี (ลงตัวเพราะ 6.25 หารกับ bin width 1.5625 ได้ 4 พอดี)
- ลองเปลี่ยนเป็น 5 Hz → bin คาดหวัง 3.2 (ไม่ลงตัว) จะเห็น peak เกลี่ยระหว่าง bin 3 กับ 4 นี่แหละคือ leakage ที่ Hann ช่วยลด

> เทคนิคนี้เรียก "sanity check ด้วย ground truth" — สร้าง input ที่รู้คำตอบ แล้วดูว่าเครื่องมือตอบตรงไหม เป็นนิสัยที่ดีก่อนเชื่ออะไรก็ตามกับข้อมูลจริง

---

# เซนเซอร์ที่ใช้ — IMU accel แกน Z

ชุดบทเรียนนี้เราป้อน **accel แกน Z ของ BMI270** เข้า FFT เพราะการเขย่าบอร์ดขึ้น-ลงตกที่แกน Z พอดี เห็นผลชัดและปลอดภัย (ไม่ต้องต่ออะไรเพิ่ม)

```python
_, _, az, _, _, _ = sensors.bmi270.motion()   # (ax,ay,az,gx,gy,gz)
buf.append(az)
time.sleep_ms(int(1000 / FS))                  # เว้นให้ได้อัตราสุ่ม FS
```

- `sensors.bmi270.motion()` คืน 6 ค่า (accel 3 + gyro 3) เราหยิบแค่ `az`
- **สำคัญ**: หน่วงเวลาให้สม่ำเสมอทุกจุด (`1000/FS` ms) — FFT อ่านความถี่ถูกต่อเมื่อระยะห่างระหว่างจุดเท่ากันเป๊ะ

> ทำไมไม่ใช้ไมค์เลยตั้งแต่ชุดบทเรียนนี้? เพราะ IMU ช้าและจับต้องได้ — เขย่าเองเห็น peak ขยับตามมือ เข้าใจ FFT ก่อน แล้วค่อยเอาไปใช้กับเสียง (16 kHz) ในบทเรียน 4.5–4.6

---

# ไล่โค้ด (1) — เก็บ N จุด แล้วเตรียมตัด DC

ส่วนต้นของลูป เก็บสัญญาณ N จุด (ให้มาแล้ว) แล้ว **ช่องเติมที่ 1** คือหาค่าเฉลี่ยเพื่อตัด DC:

```python
buf = []
for _ in range(N):
    _, _, az, _, _, _ = sensors.bmi270.motion()
    buf.append(az)
    time.sleep_ms(int(1000 / FS))

# เติม: ตัด DC/แรงโน้มถ่วง -> mean = sum(buf) / N
mean = 0.0
```

- แทน `mean = 0.0` ด้วย `mean = sum(buf) / N`
- ถ้าลืม: `mean` เป็น 0 แปลว่าไม่ตัด DC เลย → bin 0 พุ่งเด่น (แรงโน้มถ่วง) กลบสเปกตรัมจริง

> ลองรันทั้งสองแบบเทียบกันจริง ๆ นะ วางบอร์ดนิ่ง ๆ แล้วดู bin 0 — เห็นความต่างชัดมาก นี่คือบทเรียน "ทำไมต้องตัด DC" ที่จำได้ไม่ลืม

---

# ไล่โค้ด (2) — คูณ Hann window

**ช่องเติมที่ 2**: หลังตัด DC คูณ Hann window ก่อนส่งเข้า FFT:

```python
# เติม: คูณ Hann window ลด spectral leakage
#   w[i] = 0.5 - 0.5*math.cos(2*math.pi*i/(N-1))
re = [(buf[i] - mean) for i in range(N)]      # <- ยังไม่คูณ window
im = [0.0] * N
```

แทนบรรทัด `re = ...` ด้วย:

```python
re = [(buf[i] - mean) * (0.5 - 0.5 * math.cos(2 * math.pi * i / (N - 1)))
      for i in range(N)]
```

- `im` เป็น 0 ทั้งหมด เพราะสัญญาณจริง (accel) ไม่มีส่วนจินตภาพ
- ถ้าลืมคูณ window: peak ยังโผล่ที่เดิม แต่แท่งข้างเคียง "รั่ว" สูงกว่าที่ควร — สเปกตรัมเลอะ

> สังเกตว่าเราทำสองอย่างในบรรทัดเดียว: `(buf[i]-mean)` คือตัด DC, `*(0.5-...)` คือ window — อ่านจากในออกนอก: ตัด DC ก่อน แล้วค่อยคูณผ้าคลุม

---

# ไล่โค้ด (3) — magnitude ครึ่งแรก

หลัง `fft(re, im)` (ให้มาแล้ว) ผลอยู่ใน `re/im` **ช่องเติมที่ 3** คือแปลงเป็นขนาด:

```python
fft(re, im)                    # ให้มาแล้ว: เวลา -> ความถี่

# เติม: magnitude = sqrt(re^2 + im^2) เอาเฉพาะครึ่งแรก HALF bin
mag = [0.0 for k in range(HALF)]
```

แทนด้วย:

```python
mag = [math.sqrt(re[k] * re[k] + im[k] * im[k]) for k in range(HALF)]
```

- วนแค่ `range(HALF)` = `N//2` bin แรก (ความถี่บวก) ครึ่งหลังเป็นภาพสะท้อน ไม่ต้องใช้
- ถ้าลืม: `mag` เป็น 0 ทั้งหมด → แท่งสเปกตรัมแบนราบ ไม่ขยับเลย

> `mag[k]` คือคำตอบสุดท้ายของ "ความถี่ k แรงแค่ไหน" — จากตรงนี้เอาไปวาดแท่ง กับหา peak ได้เลย

---

# ไล่โค้ด (4) — หา peak แล้ววาดแท่ง

**ช่องเติมที่ 4**: หา bin เด่น แล้วส่วนที่เหลือ (วาดแท่ง + แปลง Hz) ให้มาแล้ว:

```python
# เติม: bin ที่พลังงานสูงสุด (ข้าม bin 0 = DC)
kmax = 1                       # <- แก้เป็น max(...)
```

แทนด้วย `kmax = max(range(1, HALF), key=lambda k: mag[k])` แล้วส่วนแสดงผล (ให้มาแล้ว):

```python
top = max(mag[1:])                              # ยอดสูงสุด ใช้ normalize
for k in range(HALF):
    bars[k].value(min(100, int(mag[k] / top * 100)))
    bars[k].color(GREEN if k == kmax else DIM)   # bin เด่น = เขียว
peak_lbl.text("peak: %.1f Hz (bin %d)" % (kmax * FS / N, kmax))
```

- normalize ด้วย `top` ให้แท่งสูงสุดเต็มจอเสมอ ไม่ว่าจะเขย่าแรงหรือเบา
- ถ้าลืมหา `kmax`: มันค้างที่ 1 → แท่งขยับแต่ "ความถี่เด่น" ชี้ผิดตลอด

> ครบ 4 ช่องเมื่อไร กด Run แล้วเขย่า — แท่งสเปกตรัมขยับ และ `peak` เลื่อนตามจังหวะที่คุณเขย่า นี่คือ MVP ของวันนี้

---

# ลงมือทำ — เติมช่องว่างทั้ง 4 จุด

เปิด [`s09_fft_spectrum.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l04-fft-spectrum-lab/practice/s09_fft_spectrum.py) ในไฟล์มีค่าเริ่มต้นวางไว้ **4 จุด** ตรงที่ต้องเติมขั้นของ pipeline:

| # | จุด | เติมด้วย | ถ้าลืม |
|---|---|---|---|
| 1 | ตัด DC | `mean = sum(buf) / N` | bin 0 พุ่งกลบสเปกตรัม |
| 2 | window | `re = [(buf[i]-mean)*(0.5-0.5*cos(...)) ...]` | แท่งข้างเคียงรั่ว สเปกตรัมเลอะ |
| 3 | magnitude | `mag = [sqrt(re[k]**2+im[k]**2) ...]` | แท่งแบนราบ ไม่ขยับ |
| 4 | peak | `kmax = max(range(1,HALF), key=lambda k: mag[k])` | ความถี่เด่นชี้ผิด (ค้างที่ 1) |

ขั้นตอน:

1. ไล่หา `# เติม:` ทีละจุด แล้วแทนค่าเริ่มต้นด้วยคำสั่งตามคำใบ้
2. กด **Run** (Emulator) หรือ **Program to Device** (บอร์ด)
3. เขย่าบอร์ดแกน Z เร็ว-ช้าสลับกัน ดูแท่งขยับ + peak Hz เปลี่ยน ถ้ายังไม่ขยับ กลับมาเช็ก indent กับชื่อตัวแปร

> สี่ช่องนี้คือ pipeline วิเคราะห์ความถี่เป๊ะ — ตัด DC → window → magnitude → peak เติมครบเมื่อไร คุณอ่านสเปกตรัมสดได้เอง

---

# ลงมือ (1) — รันบน BENTO Emulator

ไม่มีบอร์ดก็เริ่มได้ เปิดเบราว์เซอร์แล้วทำตามนี้:

1. เปิด **ide.tesaiot.dev** (BENTO Emulator) ในเบราว์เซอร์
2. เปิดไฟล์ [`s09_fft_spectrum.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l04-fft-spectrum-lab/practice/s09_fft_spectrum.py) (หลังเติมครบ 4 ช่อง)
3. กด **Run** — จะเห็นแท่งสเปกตรัม HALF แท่ง เรียงตามความถี่ + ป้าย peak
4. ใช้ตัวควบคุมการเคลื่อนไหวของ Emulator "เขย่า" แกน Z เร็ว-ช้า
5. ดูแท่งขยับ และ peak Hz เลื่อนตามจังหวะ

> Emulator ใช้เซนเซอร์ **จำลอง** แต่ FFT คำนวณจริงทุกบรรทัด — เหมาะกับซ้อมที่บ้าน แล้วมายืนยันกับของจริงบนบอร์ด

---

# หน้าตา Emulator ที่รันได้จริง

![จอ BENTO Emulator ขณะรันแดชบอร์ด IMU: ค่า gx gy gz จากตัวจำลองและแถบขนาดความเร่ง w:680](../../assets/img/imu_dashboard.png)

จอ emulator ที่รันได้จริง — **BENTO Edge AI Emulator** บนเบราว์เซอร์ ไม่ต้องมีบอร์ดก็เขย่า (จำลอง) แล้วเห็นค่าเซนเซอร์ขยับสด ๆ

- ตัวควบคุมการเคลื่อนไหวทางซ้าย ใช้ "เขย่า" แกน Z ป้อนเข้า pipeline FFT เดียวกับบนบอร์ด
- โค้ดชุดเดียวกับที่ flash ลงบอร์ดจริง — ซ้อมที่บ้าน แล้วมายืนยันของจริงบนบอร์ด

> เห็นค่าขยับบนจอนี้เมื่อไร แปลว่า pipeline อ่านเซนเซอร์ได้ถูก เหลือแค่ต่อ 4 ขั้น FFT ก็ได้สเปกตรัมสด

---

# ลงมือ (2) — รันบนบอร์ด BENTO จริง

บนบอร์ดจริงเราใช้ของจริง IMU จริง การสั่นสะเทือนจริง:

1. เสียบบอร์ดเข้าคอมด้วยสาย USB
2. เปิดไฟล์ [`s09_fft_spectrum.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l04-fft-spectrum-lab/practice/s09_fft_spectrum.py) ใน **BENTO IDE** กด **Program to Device**
3. บนจอจะขึ้นแท่งสเปกตรัม เขย่าบอร์ด **ขึ้น-ลง** เป็นจังหวะ
4. เขย่า **ช้า ๆ** (~2-3 ครั้ง/วินาที) → peak อยู่ Hz ต่ำ; เขย่า **เร็ว** → peak เลื่อนไป Hz สูง
5. ลองวางนิ่ง → แท่งเกือบเรียบ (ไม่มีความถี่เด่น) เพราะไม่มีการสั่น

> จุดที่ควรสังเกต: peak Hz ที่ได้ควรใกล้กับ "จำนวนครั้งที่เขย่าต่อวินาที" — เขย่า 3 ครั้ง/วินาที ควรได้ peak ~3 Hz นี่คือ FFT ที่จับต้องได้จริง

---

# แหล่งเรียนรู้เพิ่มเติม

อยากเห็น Fourier / FFT แบบเห็นภาพชัดขึ้น ลองตามลิงก์เหล่านี้:

**วิดีโอ (ช่องการศึกษาที่น่าเชื่อถือ)**
- Fourier transform เชิงภาพ (แนะนำมาก) — 3Blue1Brown: https://www.youtube.com/@3blue1brown
- The Fast Fourier Transform (FFT) อธิบายเชิงอัลกอริทึม — Computerphile: https://www.youtube.com/@Computerphile
- FFT ใน Python ภาคปฏิบัติ — Sentdex: https://www.youtube.com/@sentdex

**บทความ / ภาพอ้างอิง (สาธารณสมบัติ / CC)**
- Fast Fourier transform — สารานุกรม: https://en.wikipedia.org/wiki/Fast_Fourier_transform (ที่มา: Wikipedia, CC BY-SA)
- ภาพ Fourier transform / time-frequency — Wikimedia Commons: https://commons.wikimedia.org/wiki/Category:Fourier_transform (ที่มา: Wikimedia Commons, public domain / CC)

> วิดีโอ/ภาพภายนอกเป็นของเจ้าของต้นฉบับ ใช้เพื่อการศึกษา อ้างอิงลิงก์ต้นทาง

---

# ชัยชนะที่เห็นได้ + MVP ของชุดบทเรียนนี้

<div style="text-align:center;margin:14px 0">
<div style="display:inline-block;background:#e8f5e9;border:2px solid #2e7d32;border-radius:22px;padding:10px 22px;color:#2e7d32;font-weight:700;font-size:1.05em">
ชัยชนะที่เห็นได้ของชุดบทเรียนนี้ · สเปกตรัม FFT สดจาก IMU — แท่งความถี่ขยับ และ peak Hz เปลี่ยนตามจังหวะที่เขย่า
</div>
</div>

**MVP ของบทเรียน 4.3–4.4 (เกณฑ์ผ่านของชุดบทเรียน):** คุณรัน [`s09_fft_spectrum.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l04-fft-spectrum-lab/practice/s09_fft_spectrum.py) ได้ แล้ว **อ่านสเปกตรัมสด** ออก — แท่งความถี่ + `peak` (Hz) เปลี่ยนตามการเขย่าเร็ว/ช้าจริง

- ทำบน **Emulator** หรือ **บอร์ดจริง** ก็ได้ (โค้ดชุดเดียวกัน)
- อธิบายได้ว่า pipeline เรียก ตัด DC / window / magnitude / peak ตรงไหน ทำอะไร

> "อ่านสเปกตรัมออก" ไม่ใช่แค่ "เห็นแท่งขยับ" — คุณต้องบอกได้ว่า peak ที่ 3 Hz หมายความว่าอะไร และทำไมเขย่าเร็วขึ้น peak ถึงเลื่อนขวา

---

# บันไดช่วยเหลือ — ใบ้ → เริ่มจากโครง → เฉลย → ฉบับเต็ม

ถ้าติด ให้ไต่บันไดนี้ทีละขั้น อย่าเพิ่งกระโดดไปดูเฉลย เพราะของจะเข้าหัวตอนที่คุณพยายามเองก่อน:

- **ใบ้** — คำใบ้อยู่ในคอมเมนต์ `# เติม:` ทั้ง 4 จุดในไฟล์ฝึก + ตารางหน้าที่แล้ว บอกว่าแต่ละช่องเติมอะไร
- **เริ่มจากโครง** — [`s09_fft_spectrum.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l04-fft-spectrum-lab/practice/s09_fft_spectrum.py) มีโครงครบทั้งไฟล์แล้ว (รวมทั้ง `fft()` และการวาดแท่ง) เหลือแค่ 4 ขั้นให้เติม
- **เฉลย** — [`s09_fft_spectrum.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l04-fft-spectrum-lab/solution/s09_fft_spectrum.py) เติมครบพร้อมคอมเมนต์อธิบายทุกขั้น (อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์เอง)
- **ฉบับเต็ม** — [`s09_fft_spectrum_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l04-fft-spectrum-lab/examples/s09_fft_spectrum_full.py) ฉบับขัดเรียบร้อย เพิ่มการเฉลี่ยสเปกตรัม (EMA) ให้นิ่ง, ความถี่เด่นตัวใหญ่ (Seg7), peak-hold และวัดพลังงานรวม (RMS)

> ลองเขียนเองให้สุดก่อนนะ ถ้าติดจริง ๆ ค่อยเปิดเฉลยดูทีละขั้น แล้วกลับมาพิมพ์เอง — เดี๋ยวเราค่อย ๆ แกะไปด้วยกัน

---

# เชื่อมโยงรากฐาน — วันนี้เราแตะอะไรไปบ้าง

การอ่านสเปกตรัมสดซ่อนแนวคิด DSP หลายชั้นที่จะใช้ต่อในชุดบทเรียน feature และ Training:

**ฝั่ง DSP / โดเมนความถี่**
- **Time vs frequency** — สัญญาณเดียวกันสองมุมมอง โมเดลเสียงเลือกมองความถี่
- **FFT** — แยกสัญญาณเป็นไซน์แต่ละความถี่ใน `N log N` (radix-2)
- **DC removal + Hann window** — สองการเตรียมสัญญาณมาตรฐานก่อน FFT
- **bin width / Nyquist** — `FS/N` คุมความละเอียด, `FS/2` คือเพดาน

**ฝั่ง MicroPython / โครงโปรแกรม**
- **โครงร่วม** — import → สร้าง widget ครั้งเดียว → ลูป → `ui.poll` (เหมือนทุกบทเรียน)
- **สร้าง widget ครั้งเดียว** — สร้าง HALF แท่งก่อนลูป ในลูปแค่เปลี่ยน value/สี
- **normalize เพื่อแสดงผล** — หารด้วยยอดสูงสุดให้แท่งเต็มจอเสมอ

> ทั้งหมดนี้คือ front-end ครึ่งแรกของโมเดลเสียง บทเรียน 4.5–4.6 เราจะต่อ mel/log-mel ให้ครบ แล้วคุณจะเห็นว่า "ภาพที่โมเดลกิน" หน้าตาเป็นยังไง

---

# ใช้จริงที่ไหน — FFT ในโลกจริง

สเปกตรัมที่เราทำวันนี้ ไม่ใช่ของเล่น มันคือแกนของงาน Edge AI และงานวิศวกรรมจริงหลายสาย:

<div style="text-align:center;margin:6px 0">
<svg width="880" height="220" viewBox="0 0 880 220" font-family="DejaVu Sans, sans-serif">
  <rect x="12" y="10" width="420" height="96" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="28" y="34" font-size="13" font-weight="700" fill="#1565c0">เสียง (MIC) — ML front-end</text>
  <text x="28" y="56" font-size="11" fill="#555">FFT -> mel-spectrogram คือ input ของโมเดลเสียงเกือบทุกตัว</text>
  <text x="28" y="76" font-size="11" fill="#555">เสียงไอ · เสียงเด็กร้อง · เสียงเตือน (โมเดลบทเรียน 1.1–1.3)</text>
  <text x="28" y="96" font-size="11" fill="#888">บทเรียน 4.5–4.6 เราจะต่อยอดตรงนี้พอดี</text>
  <rect x="448" y="10" width="420" height="96" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="464" y="34" font-size="13" font-weight="700" fill="#2e7d32">การสั่นสะเทือน (IMU) — โรงงาน</text>
  <text x="464" y="56" font-size="11" fill="#555">มอเตอร์/แบริ่งเสีย = ความถี่การสั่นเปลี่ยน</text>
  <text x="464" y="76" font-size="11" fill="#555">FFT จับ "ลายเซ็นความถี่" เตือนก่อนพัง (predictive maintenance)</text>
  <text x="464" y="96" font-size="11" fill="#888">โมเดลเดียวกับที่เราเขย่าบอร์ดวันนี้</text>
  <rect x="12" y="118" width="420" height="92" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="28" y="142" font-size="13" font-weight="700" fill="#e65100">เรดาร์ — ความเร็ว/การหายใจ</text>
  <text x="28" y="164" font-size="11" fill="#555">Doppler shift = ความถี่ที่เปลี่ยน -> FFT วัดความเร็ว/อัตราหายใจ</text>
  <text x="28" y="184" font-size="11" fill="#555">ฝั่ง C ของบอร์ดทำ FFT ให้เรดาร์อยู่แล้ว (บทเรียน 4.1–4.2)</text>
  <text x="28" y="202" font-size="11" fill="#888">radar_range() ที่เราใช้ ก็มี FFT ข้างใน</text>
  <rect x="448" y="118" width="420" height="92" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="464" y="142" font-size="13" font-weight="700" fill="#6a1b9a">ร่วมกัน — feature ที่ "อ่านง่าย"</text>
  <text x="464" y="164" font-size="11" fill="#555">ทุกงานเปลี่ยนคลื่นดิบ -> สเปกตรัม ก่อนป้อนโมเดล</text>
  <text x="464" y="184" font-size="11" fill="#555">feature ดี = โมเดลเล็กลง เร็วขึ้น แม่นขึ้น</text>
  <text x="464" y="202" font-size="11" fill="#888">คือหัวใจของ Pillar 3 (Analysis)</text>
</svg>
</div>

> เห็นไหมว่า FFT ที่เราเขย่าบอร์ดเล่นวันนี้ คือเครื่องมือเดียวกับที่ใช้ตรวจมอเตอร์โรงงาน วัดการหายใจด้วยเรดาร์ และเป็น front-end ของโมเดลเสียงทุกตัว เราแค่เริ่มจากสิ่งที่จับต้องได้ที่สุด

---

# งานทำเอง + สรุปบทเรียน

**งานทำเอง (ท้ายบทเรียน):**

1. เติม [`s09_fft_spectrum.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m04-analysis/l04-fft-spectrum-lab/practice/s09_fft_spectrum.py) ให้ครบทั้ง 4 ขั้น รันได้จริง (Emulator หรือบอร์ด)
2. เขย่าบอร์ดที่ **3 จังหวะ** (ช้า/กลาง/เร็ว) จดว่าแต่ละจังหวะได้ peak กี่ Hz แล้วเทียบกับ "จำนวนครั้ง/วินาที" ที่เขย่า
3. ลองรัน **ไม่ตัด DC** (ปล่อย `mean = 0.0`) กับ **ไม่คูณ window** แล้วอธิบายว่าสเปกตรัมเปลี่ยนไปยังไง เพราะอะไร

ใบ้ข้อ 3 — ไม่ตัด DC จะเห็น bin 0 พุ่ง; ไม่คูณ window จะเห็นแท่งข้างเคียง peak "รั่ว" สูงกว่าที่ควร (spectral leakage)

**วันนี้เราได้:** เข้าใจโดเมนเวลา vs ความถี่ · รู้ว่า FFT ทำอะไรและทำไมไม่ใช่กล่องดำ · เดิน pipeline 4 ขั้น (ตัด DC → window → magnitude → peak) · อ่านสเปกตรัมสด + peak Hz จากการเขย่าจริง

> ชุดบทเรียนถัดไป (บทเรียน 4.5–4.6) เราจะต่อจากสเปกตรัมนี้ไปเป็น **windowing + mel-spectrogram** — "ภาพความถี่ตามเวลา" ที่โมเดลเสียงกินเข้าไปจริง ๆ เจอกันครับ
