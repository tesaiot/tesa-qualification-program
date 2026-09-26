---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 8.2 — ลงมือทำ: สร้างและส่งมอบแอป Edge AI"
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

# บทเรียน 8.2 — ลงมือทำ: สร้างและส่งมอบแอป Edge AI

## Capstone · ออกแบบ → สร้าง → ส่งมอบ แอป Edge AI ครบสามเสา

**โมดูล 8 — Capstone: แอป Edge AI ของเราเอง**

> ต่อจากบทเรียน 8.1 — ออกแบบ capstone: Guardian สามเสาในไฟล์เดียว

---

# โครงของไฟล์ s20_capstone.py

ทั้งไฟล์อ่านเป็นประโยคเดียว: **"เลือกโมเดล → อ่านบริบท + verdict → กรองให้นิ่ง → เจอครบเกณฑ์ค่อยสั่งการ → ออกก็เก็บกวาด"**

<div style="text-align:center;margin:6px 0">
<svg width="920" height="220" viewBox="0 0 920 220" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arS20" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g font-size="14" text-anchor="middle">
    <rect x="14" y="24" width="176" height="54" rx="10" fill="#cfd8dc" stroke="#607d8b" stroke-width="2"/>
    <text x="102" y="47" font-weight="700" fill="#455a64">find_model</text>
    <text x="102" y="66" font-size="11" fill="#999">models() + alert_idx</text>
    <rect x="230" y="24" width="176" height="54" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="318" y="47" font-weight="700" fill="#e65100">กด Load</text>
    <text x="318" y="66" font-size="11" fill="#999">select() :เติม 1</text>
    <rect x="446" y="24" width="176" height="54" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="534" y="47" font-weight="700" fill="#1565c0">DAQ + result</text>
    <text x="534" y="66" font-size="11" fill="#999">:เติม 2, 3</text>
    <rect x="662" y="24" width="176" height="54" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="750" y="47" font-weight="700" fill="#2e7d32">กรอง + ตัดสินใจ</text>
    <text x="750" y="66" font-size="11" fill="#999">EMA :เติม 4</text>
    <rect x="446" y="140" width="200" height="58" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
    <text x="546" y="164" font-weight="700" fill="#6a1b9a">สั่งการ</text>
    <text x="546" y="182" font-size="11" fill="#999">fire_alert() :เติม 5</text>
    <rect x="680" y="140" width="158" height="58" rx="10" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
    <text x="759" y="164" font-weight="700" fill="#455a64" font-size="13">ออก → stop()</text>
    <text x="759" y="182" font-size="11" fill="#999">finally (ให้แล้ว)</text>
  </g>
  <line x1="190" y1="51" x2="228" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS20)"/>
  <line x1="406" y1="51" x2="444" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS20)"/>
  <line x1="622" y1="51" x2="660" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS20)"/>
  <path d="M750,78 C750,110 546,112 546,138" fill="none" stroke="#2e7d32" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arS20)"/>
  <text x="640" y="112" font-size="12" fill="#2e7d32">streak ครบ → ยิง</text>
  <line x1="646" y1="169" x2="678" y2="169" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS20)"/>
  <text x="470" y="214" font-size="11" fill="#888" text-anchor="middle">แถวล่าง = สิ่งที่เกิดในลูปเมื่อ Guardian กำลังเฝ้า</text>
</svg>
</div>

> ป้าย `:เติม 1..5` ชี้จุดที่คุณต้องเติมในไฟล์ฝึก ทั้งห้าคือ "กระดูกสันหลัง" ของสามเสา — เติมครบเมื่อไร Guardian ทำงานครบวง

---

# ไล่โค้ด (1) — ปุ่มออกแบบ + หาโมเดล

ส่วนหัวไฟล์คือ "ปุ่มออกแบบ" ที่ทีมปรับได้ แล้ว `find_model` หาโมเดลจากชื่อ (ถามฮาร์ดแวร์ ไม่ hard-code index):

```python
MODEL_KEYWORD = "Motion"   # โมเดลที่เฝ้า
HITS_NEEDED   = 3          # debounce: เจอติดกันกี่ครั้งถึงสั่งการ
EMA_ALPHA     = 0.4        # ความหนักของตัวกรอง conf

model = find_model(MODEL_KEYWORD)
labels = model['labels']
alert_idx = len(labels) - 1        # คลาสสุดท้าย = เหตุการณ์ที่สนใจ
conf_ema = dsp.EMA(alpha=EMA_ALPHA)  # สร้างตัวกรองครั้งเดียว
```

- `alert_idx = len(labels) - 1` — กติกาออกแบบ: คลาสสุดท้ายคือ "เหตุการณ์" (shaking/baby_cry/Push/cough)
- ถ้าโมเดลของคุณวางคลาสไว้คนละที่ ก็แก้บรรทัดนี้บรรทัดเดียว — นี่คือจุดออกแบบที่ควรจดเหตุผลลงบันทึกการเรียน

> `conf_ema` สร้าง **นอกลูป** เพราะมันต้องจำอดีต — สร้างซ้ำในลูปจะล้างความจำทุกเฟรม กรองไม่ได้ผล (บทเรียน "สร้างครั้งเดียว" จากบทเรียน 1.1–1.3)

---

# ไล่โค้ด (2) — เติม 1: กด Load แล้ว select()

**ช่องเติมที่ 1 (เสา Apps · start):** เมื่อกด Load สั่งให้โมเดลเริ่มรัน:

```python
elif h == load_id:
    try:
        # เติม: edge_ai.select(model['index'])
        pass
        running = True
        streak = 0
        fired = False
        status.text("RUNNING"); status.color(GREEN)
        conf_ema.reset()        # เริ่มเฝ้ารอบใหม่ ล้างตัวกรอง
    except OSError as e:
        status.text("ERROR")    # ข้ามคอร์พลาดได้ ต้องเผื่อ
```

- แทน `pass` ด้วย `edge_ai.select(model['index'])` — ต้องอยู่ใน `try` เพราะ `select()` โยน `OSError` ได้
- สังเกต `conf_ema.reset()` ตอน Load — เริ่มเฝ้ารอบใหม่ต้องล้างความจำตัวกรองให้สะอาด

> ขึ้น RUNNING **หลัง** `select()` สำเร็จเท่านั้น เหมือนบทเรียน 1.1–1.3 — ถ้า error กระโดดไป except ไม่โกหกผู้ใช้ว่ากำลังเฝ้า

---

# ไล่โค้ด (3) — เติม 2: อ่านเซนเซอร์ดิบ (DAQ)

**ช่องเติมที่ 2 (เสา DAQ):** อ่านความเร่งดิบมาเป็นบริบท ทุกวนรอบที่กำลังเฝ้า:

```python
if running:
    # เติม: ax, ay, az = sensors.bmi270.acceleration()
    ax, ay, az = 0.0, 0.0, 0.0
    pass
    mag = (ax*ax + ay*ay + az*az) ** 0.5
    ctx.text("motion: %.1f" % mag)
```

- แทน `pass` ด้วย `ax, ay, az = sensors.bmi270.acceleration()` (ลบบรรทัด `0.0` ทิ้งหรือปล่อยไว้ก็ได้ เพราะถูกทับ)
- `mag` คือขนาดเวกเตอร์ความเร่ง — อยู่นิ่ง ~9.8, ถูกจับ/เขย่าพุ่งขึ้น
- ถ้าลืมเติม: `motion` ค้างที่ 0.0 ตลอด (เพราะไม่ได้อ่านของจริง) — เสา DAQ ไม่ทำงาน

> นี่คือเสาแรกสุดของวงจร (DAQ) ที่ยังมีบทบาทในผลิตภัณฑ์ปลายทาง — ทีมที่อยากต่อยอดการออกแบบ เอา `mag` ไปทำ fusion gate ต่อได้ (โจทย์ต่อยอด)

---

# ไล่โค้ด (4) — เติม 3: อ่าน verdict (Apps)

**ช่องเติมที่ 3 (เสา Apps · read):** อ่านผลอนุมานล่าสุด แล้วทำงานเฉพาะตอนมีผลใหม่:

```python
    # เติม: r = edge_ai.result()
    r = None
    pass
    if r and r['seq'] != last_seq:   # มีผลใหม่จริงไหม
        last_seq = r['seq']
        ...
```

- แทน `pass` ด้วย `r = edge_ai.result()` — คืน dict หรือ `None` ถ้ายังไม่มีผล
- เช็ก `r and r['seq'] != last_seq` ก่อนเสมอ — วาด/ตัดสินใจเฉพาะตอนมีผลใหม่ (บทเรียน `seq` จากบทเรียน 1.1–1.3)
- ถ้าลืมเติม: `r` เป็น `None` ตลอด → การ์ดผลลัพธ์ไม่ขยับเลย

> `result()` เป็นการ **pull** ผลจาก M55 — เรียกในลูปเมื่อไรก็ได้ ไม่บล็อกรอ คืนผลล่าสุดที่คอร์ AI คิดไว้

---

# ไล่โค้ด (5) — เติม 4: กรอง conf (Processing)

**ช่องเติมที่ 4 (เสา Processing):** กรองความมั่นใจให้นิ่งก่อนเอาไปเทียบเกณฑ์:

```python
        # เติม: conf_s = conf_ema.update(r['conf'])
        conf_s = r['conf']
        pass
        sure = conf_s >= edge_ai.CONF_FLOOR
        verdict.text(r['label'] or '-')
        verdict.color(GREEN if sure else AMBER)
```

- แทน `pass` ด้วย `conf_s = conf_ema.update(r['conf'])` — `.update()` คืนค่าที่กรองแล้วออกมาเลย
- แล้วเทียบ `conf_s` (ไม่ใช่ `r['conf']` ดิบ) กับ `CONF_FLOOR` — ต่ำกว่าเกณฑ์เป็นเหลือง (not sure)
- ถ้าลืมเติม: ใช้ conf ดิบ → verdict สี/สถานะกระพริบตามพีคทุกเฟรม

> จุดนี้คือที่ที่เสา Processing "แทรก" ระหว่าง verdict กับ decision — โมเดลพูด conf ดิบ เรากรองก่อน แล้วค่อยเชื่อ

---

# ไล่โค้ด (6) — เติม 5: สั่งการเมื่อครบเกณฑ์

**ช่องเติมที่ 5 (เสา Apps · action):** decision ผ่านสามด่านครบ → ยิง action:

```python
        hit = (top == alert_idx) and sure
        if hit:
            streak += 1
        else:
            streak = 0; fired = False
            banner.text("รอจับ %s ..." % alert_name)

        if streak >= HITS_NEEDED and not fired:
            # เติม: fire_alert(r['label'], conf_s)
            pass
            fired = True
```

- แทน `pass` ด้วย `fire_alert(r['label'], conf_s)` — บี๊บ + แบนเนอร์ + นับครั้ง
- `fired = True` หลังยิง — edge-trigger กันยิงรัวทุกเฟรมที่ยังเจออยู่
- ถ้าลืมเติม: ครบเกณฑ์แล้วแต่ Guardian เงียบ ไม่สั่งการ

> ห้าช่องนี้คือกระดูกสันหลังของสามเสา: select (Apps) → sensors (DAQ) → result (Apps) → EMA (Processing) → fire_alert (Apps) เติมครบ = ผลิตภัณฑ์ทำงานครบวง

---

# ลงมือทำ — เติมช่องว่างทั้ง 5 จุด

เปิด [`s20_capstone.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m08-capstone/l02-capstone-build-lab/practice/s20_capstone.py) ไล่หา `# เติม:` ทั้ง **5 จุด** แล้วแทน `pass` ด้วยคำสั่งจริง:

| # | เสา | จุด | เติมด้วย | ถ้าลืม |
|---|---|---|---|---|
| 1 | Apps | ปุ่ม Load | `edge_ai.select(model['index'])` | RUNNING แต่ไม่มีผล |
| 2 | DAQ | ในลูป | `ax, ay, az = sensors.bmi270.acceleration()` | motion ค้าง 0.0 |
| 3 | Apps | ในลูป | `r = edge_ai.result()` | การ์ดไม่ขยับ |
| 4 | Processing | มีผลใหม่ | `conf_s = conf_ema.update(r['conf'])` | สี/สถานะกระพริบ |
| 5 | Apps | ครบเกณฑ์ | `fire_alert(r['label'], conf_s)` | ครบแล้วแต่เงียบ |

ขั้นตอน:

1. เติมทีละจุดตามคำใบ้ `# เติม:`
2. กด **Run** (Emulator) หรือ **Program to Device** (บอร์ด)
3. เลือกโมเดล กด Load ทำเหตุการณ์เป้าหมายติดกัน ดูแบนเนอร์ ALERT เด้ง

> เติมครบทั้งห้าแล้วยังไม่พอสำหรับ capstone — ขั้นต่อไปคือ **ออกแบบ** ของทีม: เฝ้าอะไร, action อะไร, ตั้งเกณฑ์เท่าไร เพราะอะไร

---

# ลงมือ (1) — รันบน BENTO Emulator

ไม่มีบอร์ดก็ทำ capstone ได้เต็มรูปแบบ (Guardian ใช้ IMU + edge_ai ที่ Emulator รองรับครบ):

1. เปิด **ide.tesaiot.dev** (BENTO Emulator) ในเบราว์เซอร์
2. เปิด [`s20_capstone.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m08-capstone/l02-capstone-build-lab/practice/s20_capstone.py) เติม 5 ช่อง
3. กด **Run** → เลือก Motion กด **Load**
4. ใช้ปุ่ม Shake / ลากเอียง ที่ Emulator จำลอง ทำ "shaking" ติดกันหลายครั้ง
5. ดูแบนเนอร์ `! ALERT: shaking !` + ตัวนับเพิ่ม แล้วลองทำพีคแวบเดียว — Guardian ไม่เตือน

> Emulator ใช้เซนเซอร์จำลอง แต่ API เหมือนบอร์ดจริงทุกบรรทัด — ซ้อมออกแบบที่บ้านได้เต็มที่ แล้วมายืนยันกับของจริงบนบอร์ด

---

# จอ Emulator ที่รันได้จริง

โค้ด capstone ชุดเดียวรันได้ทั้งบนเบราว์เซอร์ (Emulator) และบน MCU จริง (Cortex-M55) โดย API เหมือนกันทุกบรรทัด ส่วน Cortex-A ใช้ไฟล์โมเดลเดียวกันแต่รันด้วยสคริปต์ Python อย่าง [`eval_pc.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/eval_pc.py) ไม่ใช่โค้ด MicroPython นี้:

![หน้า Edge AI บน BENTO Emulator: dropdown เลือกโมเดล Motion Detection ปุ่ม Load และ Stop คลาสที่ชนะ idle เวลาอนุมาน และแถบความมั่นใจของ idle circle shaking w:680](../../assets/img/edge_ai_page.png)

จอ emulator ที่รันได้จริง — หน้าเมนู Edge AI ของ BENTO Emulator (dropdown, Load/Stop, แถบคะแนน) ซึ่ง [`s20_capstone.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m08-capstone/l02-capstone-build-lab/practice/s20_capstone.py) ใช้องค์ประกอบแบบเดียวกัน แล้วเพิ่มแบนเนอร์ ALERT กับตัวนับ

<div style="text-align:center;margin:6px 0">
<svg width="820" height="126" viewBox="0 0 820 126" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arSpec" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="298" y="6" width="224" height="42" rx="9" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
  <text x="410" y="26" font-size="13" font-weight="700" fill="#455a64" text-anchor="middle">s20_capstone.py — โค้ดชุดเดียว</text>
  <text x="410" y="42" font-size="11" fill="#888" text-anchor="middle">edge_ai · dsp · sensors · ui</text>
  <rect x="40" y="80" width="210" height="40" rx="9" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="145" y="98" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">MCU · Cortex-M55</text>
  <text x="145" y="114" font-size="10" fill="#888" text-anchor="middle">บอร์ด BENTO + NPU</text>
  <rect x="305" y="80" width="210" height="40" rx="9" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="410" y="98" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">Cortex-A · Linux</text>
  <text x="410" y="114" font-size="10" fill="#888" text-anchor="middle">โมเดลเดียวกัน · สคริปต์ Python</text>
  <rect x="570" y="80" width="210" height="40" rx="9" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="675" y="98" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">Web · Emulator</text>
  <text x="675" y="114" font-size="10" fill="#888" text-anchor="middle">เบราว์เซอร์ (ในภาพ)</text>
  <line x1="360" y1="48" x2="180" y2="78" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arSpec)"/>
  <line x1="410" y1="48" x2="410" y2="78" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arSpec)"/>
  <line x1="460" y1="48" x2="640" y2="78" stroke="#607d8b" stroke-width="2.2" marker-end="url(#arSpec)"/>
</svg>
</div>

> สเปกตรัม MCU → Cortex-A → Web คือธีมของทั้งคอร์ส: เราฝึกโมเดลครั้งเดียว รันได้ทุกเป้าหมาย ส่วนแอป MicroPython นี้รันได้บน Emulator กับบอร์ด ภาพนี้คือฝั่ง Web — ซ้อมที่บ้านให้ชิน แล้วเอา [`s20_capstone.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m08-capstone/l02-capstone-build-lab/practice/s20_capstone.py) ไฟล์เดิมไปลงบอร์ดจริงได้เลย

---

# ลงมือ (2) — รันบนบอร์ด BENTO จริง

บนบอร์ดจริงพิสูจน์กับของจริง เซนเซอร์จริง NPU จริง:

1. เสียบบอร์ด เปิด [`s20_capstone.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m08-capstone/l02-capstone-build-lab/practice/s20_capstone.py) ใน **BENTO IDE** กด **Program to Device**
2. เลือกโมเดลที่ทีมออกแบบจะเฝ้า กด **Load**
3. ทำเหตุการณ์เป้าหมายจริง (เขย่าบอร์ด / ส่งเสียงไอ / ยื่นมือเข้าเรดาร์) ติดกันจนครบเกณฑ์
4. ยืนยันว่า Guardian สั่งการ (เสียง + แบนเนอร์) และดู `latency` จริงของ NPU (ฉบับเต็ม)
5. จูน `HITS_NEEDED` / `EMA_ALPHA` แล้วสังเกตว่า "ไวขึ้น/เตือนมั่วขึ้น" อย่างไร

> จูนค่าออกแบบบนของจริงคือหัวใจ capstone — จดค่าที่คุณเลือกและ **เหตุผล** ลงบันทึกการเรียน นั่นคือหลักฐานการตัดสินใจเชิงวิศวกรรม

---

# ทิศทางวิจัย + โปรดักชัน — ต่อจากที่นี่ไปไหนได้

Guardian คือฐาน ทีมที่อยากไปไกลกว่า MVP มีสี่ทิศให้ต่อ (แต่ละทิศคือทั้งบล็อกของคอร์ส):

- **เสียบโมเดลที่ฝึกเอง (Training)** — เอา `.tflite` จากบทเรียน 5.3–5.9 มาแทนโมเดลสำเร็จรูป → Guardian เฝ้า "คลาสของคุณเอง"
- **feature จาก Analysis** — เพิ่ม FFT/spectrogram (บทเรียน 4.3–4.6) เป็นด่านกรองก่อน action (เช่น เตือนเฉพาะเสียงในช่วงความถี่หนึ่ง)
- **sensor fusion จริง** — รวม `mag` (DAQ) กับ verdict: เตือนเฉพาะตอนอุปกรณ์นิ่ง / มีคนอยู่ (เรดาร์) → ลด false positive
- **ส่งขึ้นคลาวด์ (IoT)** — `action` = publish MQTT (บทเรียน 6.5–6.6) แทนเสียง → เหตุการณ์ Edge วิ่งไปแดชบอร์ด

> ทิศทางวิจัย: on-device learning, personalization ต่อผู้ใช้, การประเมิน false-positive rate จริงในสนาม — capstone ที่ดีจะ "ตั้งคำถามวิจัยหนึ่งข้อ" ไว้ท้ายรายงาน

---

# แหล่งเรียนรู้เพิ่มเติม

อยากต่อยอด capstone หรือหาไอเดียโปรเจกต์ tinyML เพิ่ม เริ่มจากแหล่งเหล่านี้ได้เลย:

**วิดีโอ (ช่องการศึกษาที่น่าเชื่อถือ)**

- Neural networks ทำงานยังไง — ช่อง 3Blue1Brown: https://www.youtube.com/@3blue1brown
- โมเดล ML อธิบายทีละขั้นแบบเข้าใจง่าย — ช่อง StatQuest with Josh Starmer: https://www.youtube.com/@statquest
- TensorFlow Lite for Microcontrollers (รันโมเดลบน MCU) — TensorFlow official docs: https://www.tensorflow.org/lite/microcontrollers

**ภาพ/เอกสารอ้างอิง (เปิดอ่านฟรี)**

- Exponential smoothing — Wikipedia: https://en.wikipedia.org/wiki/Exponential_smoothing (ที่มา: Wikipedia, CC BY-SA 4.0) — คือรากของสูตร EMA ในเสา Processing
- Edge computing — Wikipedia: https://en.wikipedia.org/wiki/Edge_computing (ที่มา: Wikipedia, CC BY-SA 4.0) — ภาพรวมว่าทำไม Edge AI ถึงประมวลผลบนอุปกรณ์

> วิดีโอ/ภาพภายนอกเป็นของเจ้าของต้นฉบับ ใช้เพื่อการศึกษา อ้างอิงลิงก์ต้นทาง — เปิดดูจากลิงก์โดยตรง ไม่ได้ฝังไว้ในสไลด์

---

# ชัยชนะที่เห็นได้ + MVP ของชุดบทเรียนนี้

<div style="text-align:center;margin:14px 0">
<div style="display:inline-block;background:#e8f5e9;border:2px solid #2e7d32;border-radius:22px;padding:10px 22px;color:#2e7d32;font-weight:700;font-size:1.05em">
ชัยชนะที่เห็นได้ · ผลิตภัณฑ์ Edge AI ของทีม เฝ้าเหตุการณ์จริงแล้วสั่งการเอง โดยไม่เตือนมั่ว — เดโมได้
</div>
</div>

**MVP ของบทเรียน 8.1–8.2 (เกณฑ์ผ่านของชุดบทเรียน):** คุณส่งมอบ Guardian ที่ทำงาน **ครบ ≥3 เสา** (DAQ + Processing + Apps) — เลือกโมเดล เฝ้าเหตุการณ์เป้าหมาย ผ่านชั้นตัดสินใจ (conf กรอง + debounce) แล้ว action ยิงจริง พร้อม **อธิบายการออกแบบ** ได้

- ทำบน **Emulator** หรือ **บอร์ดจริง** ก็ได้ (โค้ดชุดเดียวกัน)
- อธิบายได้ว่าแต่ละเสาอยู่บรรทัดไหน ทำอะไร และทำไมตั้งค่า `CONF_FLOOR`/`HITS_NEEDED`/`EMA_ALPHA` เท่านั้น

> "ส่งมอบได้" ไม่ใช่แค่ "รันผ่าน" — ต้องเดโมให้คนอื่นดู เล่าเหตุผลการออกแบบ และชี้ได้ว่าจะต่อยอดทิศไหน

---

# บันไดช่วยเหลือ — ใบ้ → เริ่มจากโครง → เฉลย → ฉบับเต็ม

ถ้าติด ไต่บันไดนี้ทีละขั้น อย่าเพิ่งกระโดดไปดูเฉลย ของจะเข้าหัวตอนที่คุณพยายามเองก่อน:

- **ใบ้** — คำใบ้อยู่ในคอมเมนต์ `# เติม:` ทั้ง 5 จุดในไฟล์ฝึก + ตารางเสา/จุด/คำสั่งหน้าที่แล้ว
- **เริ่มจากโครง** — [`s20_capstone.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m08-capstone/l02-capstone-build-lab/practice/s20_capstone.py) มีโครงครบทั้งไฟล์ เหลือ 5 บรรทัดกระดูกสันหลังให้เติม
- **เฉลย** — [`s20_capstone.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m08-capstone/l02-capstone-build-lab/solution/s20_capstone.py) เติมครบพร้อมคอมเมนต์อธิบายทุกเสา (อ่านให้เข้าใจ ปิดไฟล์ แล้วประกอบเอง)
- **ฉบับเต็ม** — [`s20_capstone_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m08-capstone/l02-capstone-build-lab/examples/s20_capstone_full.py) ฉบับขัดเรียบร้อย: เลือกโมเดลสดจาก dropdown + latency + reset ตัวกรอง + นับ alert

> capstone มีขั้นที่ห้าที่เฉลยไม่ได้ให้: **การออกแบบของทีม** — เฉลยให้แค่โครง Guardian ส่วน "เฝ้าอะไร action อะไร" เป็นของคุณ

---

# เชื่อมโยงรากฐาน — ชุดบทเรียนนี้รวบอะไรจากทั้งคอร์ส

capstone ไม่ได้สอนของใหม่ มันเรียก "ของเก่าที่เข้าใจแล้ว" กลับมาพร้อมกัน:

**ฝั่งเสาข้อมูล**
- **DAQ (โมดูล 2)** — `sensors.bmi270.acceleration()` อ่านบริบทดิบ
- **Processing/Analysis (บทเรียน 3.1–4.6)** — `dsp.EMA` กรองความมั่นใจให้ตัดสินใจนิ่ง
- **Apps (โมดูล 6)** — `edge_ai` verdict → debounce → action

**ฝั่งวิศวกรรม/โครงโปรแกรม**
- **โครงร่วม** — import → สร้างครั้งเดียว → ลูป → `ui.poll` (จากบทเรียน 1.4–1.5)
- **confirm by observation + `try/except OSError`** — จากบทเรียน 1.1–1.3
- **debounce + edge-trigger** — จากชุดบทเรียน Apps (บทเรียน 6.3–6.4)
- **เก็บกวาดตอนจบ** — `finally: edge_ai.stop()` คืนเครื่องสู่สถานะที่รู้แน่

> พลังของ capstone: คุณเห็นว่าทุกบทเรียนไม่ได้แยกกัน มันคือชิ้นส่วนของผลิตภัณฑ์เดียว — และตอนนี้คุณต่อมันเป็นแล้ว

---

# ใช้จริงที่ไหน — Guardian ในโลกจริง

โครง "เฝ้า → กรอง → สั่งการ" ที่สร้างวันนี้ คือแก่นของสินค้า Edge AI จริงหลายหมวด:

<div style="text-align:center;margin:6px 0">
<svg width="880" height="220" viewBox="0 0 880 220" font-family="DejaVu Sans, sans-serif">
  <rect x="12" y="10" width="420" height="96" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="28" y="34" font-size="13" font-weight="700" fill="#1565c0">ดูแลผู้สูงอายุ (IMU+เสียง)</text>
  <text x="28" y="56" font-size="11" fill="#555">ตรวจการล้ม/เรียกช่วย · เฝ้าเสียงไอ กลางคืน</text>
  <text x="28" y="76" font-size="11" fill="#555">ยอม false + ดีกว่า miss → เกณฑ์ตั้งไว</text>
  <text x="28" y="96" font-size="11" fill="#888">= Guardian ที่จูน CONF_FLOOR ต่ำ</text>
  <rect x="448" y="10" width="420" height="96" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="464" y="34" font-size="13" font-weight="700" fill="#2e7d32">โรงงาน/เครื่องจักร (เสียง+IMU)</text>
  <text x="464" y="56" font-size="11" fill="#555">ฟังเสียงผิดปกติ · สั่นเกินเกณฑ์ → แจ้งซ่อม</text>
  <text x="464" y="76" font-size="11" fill="#555">ต้องกัน false + เพราะหยุดสายพานแพง</text>
  <text x="464" y="96" font-size="11" fill="#888">= Guardian ที่ debounce สูง</text>
  <rect x="12" y="118" width="420" height="92" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="28" y="142" font-size="13" font-weight="700" fill="#e65100">บ้าน/ค้าปลีก (เรดาร์+เสียง)</text>
  <text x="28" y="164" font-size="11" fill="#555">เปิดไฟเมื่อมีคน · ตรวจเสียงเด็กร้อง</text>
  <text x="28" y="184" font-size="11" fill="#555">ข้อมูลไม่ออกจากเครื่อง → ความเป็นส่วนตัว</text>
  <text x="28" y="202" font-size="11" fill="#888">= Guardian + sensor fusion</text>
  <rect x="448" y="118" width="420" height="92" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="464" y="142" font-size="13" font-weight="700" fill="#6a1b9a">ร่วมกัน — เฝ้า + ตัดสินใจ + สั่งการ</text>
  <text x="464" y="164" font-size="11" fill="#555">ทุกงานใช้ conf + debounce ตัดสินว่าจะเชื่อไหม</text>
  <text x="464" y="184" font-size="11" fill="#555">แล้ว action ต่อ (แจ้งเตือน/เปิดไฟ/ส่งคลาวด์)</text>
  <text x="464" y="202" font-size="11" fill="#888">คือโครง Guardian ที่คุณสร้างวันนี้</text>
</svg>
</div>

> โครงเดียวกันหมด ต่างแค่ "จูนเกณฑ์ให้เข้ากับต้นทุนของการพลาด" — capstone ฝึกให้คุณคิดเรื่องนี้เป็น ไม่ใช่แค่เขียนโค้ดให้รันได้

---

# งานทำเอง + ปิดคอร์ส

**งานทำเอง (ท้ายบทเรียนและท้ายหลักสูตร):**

1. เติม [`s20_capstone.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m08-capstone/l02-capstone-build-lab/practice/s20_capstone.py) ให้ครบทั้ง 5 ช่อง รันได้จริง (Emulator หรือบอร์ด)
2. **ออกแบบ Guardian ของทีม** — เลือกโมเดลที่เฝ้า + action + ตั้ง `CONF_FLOOR`/`HITS_NEEDED`/`EMA_ALPHA` แล้ว **เขียนเหตุผล** ลงบันทึกการเรียน
3. เดโม 2 นาที: โชว์ ALERT ยิงจริง + โชว์ว่าพีคหลอกไม่ทำให้เตือน + เล่าการแลกเปลี่ยนที่เลือก

ใบ้ข้อ 3 — เตรียม "เคสหลอก" ไว้ล่วงหน้า (ท่า/เสียงก้ำกึ่ง) เพื่อพิสูจน์ว่า debounce ทำงาน นั่นคือหลักฐานว่า Guardian เป็นผลิตภัณฑ์ ไม่ใช่เดโม

**ทั้งคอร์สเราได้:** เดินครบ 5 เสาของวงจรชีวิตข้อมูล · ฝึกโมเดลเอง · รันข้ามเป้าหมาย (MCU/Web/PC) · และวันนี้ **ร้อยทุกอย่างเป็นผลิตภัณฑ์เดียวที่ส่งมอบได้**

> ขอบคุณที่เดินมาจนจบคอร์สครับ จากบทเรียนแรกที่เมนู 6 โมเดลเป็นกล่องดำ วันนี้คุณเปิดกล่องได้ทุกชั้นและประกอบกล่องของตัวเองเป็นแล้ว — เอา Guardian ตัวนี้ไปต่อยอดเป็นของจริงได้เลย
