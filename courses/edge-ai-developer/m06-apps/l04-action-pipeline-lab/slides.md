---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 6.4 — ลงมือทำ: action pipeline ที่กัน false positive"
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

# บทเรียน 6.4 — ลงมือทำ: action pipeline ที่กัน false positive

## Apps II: ท่อสั่งการ (action pipeline) · จาก verdict สู่ action จริง — RGB · เสียง · log

**โมดูล 6 — แอป Edge AI**

> ต่อจากบทเรียน 6.3 — ท่อสั่งการ: CONF_FLOOR, debounce, cooldown และ on_result

---

# โครงร่วมของโปรแกรม — ตัวเดิมที่เจอทุกบทเรียน

ก่อนดูไฟล์จริง จำโครง 4 จังหวะจากบทเรียน 1.1–1.3 ไว้ — ชุดบทเรียนนี้ยังเดินตามเป๊ะ ของใหม่แค่ไปแทรกอยู่ใน "ลูป"

<div style="text-align:center;margin:6px 0">
<svg width="880" height="150" viewBox="0 0 880 150" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arSk" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="40" width="190" height="56" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="115" y="64" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">1 · import</text>
  <text x="115" y="84" font-size="11" fill="#666" text-anchor="middle">edge_ai · ui · dsp · time</text>
  <rect x="238" y="40" width="210" height="56" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="343" y="64" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">2 · สร้างครั้งเดียว</text>
  <text x="343" y="84" font-size="11" fill="#666" text-anchor="middle">widget + ไฟ RGB + EMA</text>
  <rect x="476" y="40" width="200" height="56" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="576" y="64" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">3 · ลูป (ของใหม่นี่)</text>
  <text x="576" y="84" font-size="11" fill="#666" text-anchor="middle">อ่านผล → ท่อ → action</text>
  <rect x="704" y="40" width="156" height="56" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="782" y="64" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">4 · ui.poll</text>
  <text x="782" y="84" font-size="11" fill="#666" text-anchor="middle">รับปุ่ม back</text>
  <line x1="210" y1="68" x2="236" y2="68" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <line x1="448" y1="68" x2="474" y2="68" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <line x1="676" y1="68" x2="702" y2="68" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <path d="M782,96 C782,120 576,120 576,98" fill="none" stroke="#9e9e9e" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arSk)"/>
  <text x="670" y="124" font-size="11" fill="#9e9e9e" text-anchor="middle">วนกลับ</text>
</svg>
</div>

> "สร้างครั้งเดียว" ยังสำคัญเท่าเดิม: `ui.Panel` ของไฟ RGB และ `dsp.EMA` สร้างนอกลูป ในลูปแค่ `light.color()` และ `smoother.update()` — สร้างซ้ำทุกรอบจอกระพริบและ EMA จะรีเซ็ตตลอด

---

# โครงของไฟล์ s16_action_pipeline.py

ทั้งไฟล์อ่านเป็นประโยคเดียว: **"เลือกโมเดล → วนอ่านผล → เฟรมนี้เจอเป้าหมายไหม → ครบ debounce+cooldown ไหม → ยิง action"**

<div style="text-align:center;margin:6px 0">
<svg width="940" height="210" viewBox="0 0 940 210" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arS16" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g font-size="13" text-anchor="middle">
    <rect x="14" y="24" width="160" height="52" rx="10" fill="#cfd8dc" stroke="#607d8b" stroke-width="2"/>
    <text x="94" y="46" font-weight="700" fill="#455a64">เลือกโมเดล</text>
    <text x="94" y="64" font-size="10" fill="#999">select() :108</text>
    <rect x="206" y="24" width="160" height="52" rx="10" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
    <text x="286" y="46" font-weight="700" fill="#455a64">อ่านผล</text>
    <text x="286" y="64" font-size="10" fill="#999">result() :ช่อง 1</text>
    <polygon points="452,50 502,24 552,50 502,76" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="502" y="46" font-weight="700" fill="#1565c0" font-size="11">hit?</text>
    <text x="502" y="62" font-size="9" fill="#888">ช่อง 2</text>
    <rect x="620" y="24" width="160" height="52" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="700" y="42" font-weight="700" fill="#2e7d32">streak+1</text>
    <text x="700" y="60" font-size="10" fill="#999">ready = streak≥NEED</text>
    <!-- row B -->
    <polygon points="452,150 512,124 572,150 512,176" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="512" y="146" font-weight="700" fill="#e65100" font-size="11">ready</text>
    <text x="512" y="162" font-size="9" fill="#888">&amp; cooled? :ช่อง 3</text>
    <rect x="640" y="124" width="180" height="52" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
    <text x="730" y="146" font-weight="700" fill="#6a1b9a">fire_action</text>
    <text x="730" y="164" font-size="10" fill="#999">RGB+เสียง+log :ช่อง 4</text>
  </g>
  <line x1="174" y1="50" x2="204" y2="50" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS16)"/>
  <line x1="366" y1="50" x2="450" y2="50" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS16)"/>
  <line x1="552" y1="50" x2="618" y2="50" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS16)"/>
  <text x="585" y="42" font-size="10" fill="#2e7d32">yes</text>
  <path d="M700,76 C700,100 512,100 512,122" fill="none" stroke="#2e7d32" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arS16)"/>
  <line x1="572" y1="150" x2="638" y2="150" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS16)"/>
  <text x="605" y="142" font-size="10" fill="#6a1b9a">yes</text>
  <path d="M452,50 C420,90 380,150 300,150" fill="none" stroke="#c62828" stroke-width="1.8" stroke-dasharray="5 4"/>
  <text x="330" y="120" font-size="10" fill="#c62828">no → streak=0 (ไฟฟ้า)</text>
  <text x="470" y="202" font-size="11" fill="#888" text-anchor="middle">ช่อง 1–4 ในไฟล์ฝึก = ด่านของท่อ เรียงตามการไหลนี้</text>
</svg>
</div>

> ตัวเลข `:108` และ `ช่อง 1–4` ชี้จุดที่ต้องเติมในไฟล์ฝึก จำโครงนี้ไว้ เดี๋ยวไล่ดูทีละช่อง

---

# ไล่โค้ด (1) — อ่านผลอนุมาน

**ช่องเติมที่ 1**: ในลูป ดึงผลล่าสุดมาก่อน เหมือนบทเรียน 1.1–1.3 เป๊ะ — นี่คือปากทางของท่อ

```python
if running:  # (ในไฟล์คือหลังรับปุ่ม)
    # เติม: อ่านผลอนุมานล่าสุดมาเก็บใน r  ->  r = edge_ai.result()
    r = None
    pass
    if r and r['seq'] != last_seq:      # ทำงานเฉพาะตอนมีผลใหม่ (seq เปลี่ยน)
        last_seq = r['seq']
        verdict.text(r['label'] or '-')
        conf.text("conf: %.0f %%" % (r['conf'] * 100))
```

- แทน `pass` ด้วย `r = edge_ai.result()` — คืน dict (`label`/`conf`/`scores`/`seq`/...) หรือ `None`
- เช็ก `seq` ก่อนเสมอ วาดจอ + เดินท่อเฉพาะตอนมีผลใหม่ ไม่รัดจอทุกรอบ
- ถ้าลืมเติม: `r` เป็น `None` ตลอด → จอไม่ขึ้นคลาส ท่อไม่เดิน action ไม่ยิง

> เหมือนบทเรียน 1.1–1.3 ทุกอย่าง ต่างกันแค่คราวนี้ผลที่อ่านได้กำลังจะถูกส่งเข้าท่อไปตัดสินใจต่อ ไม่ได้จบที่ขึ้นจอ

---

# ไล่โค้ด (2) — ด่านกรอง (false-positive gate)

**ช่องเติมที่ 2**: ด่านแรกของท่อ — เฟรมนี้นับเป็น "การเจอเป้าหมายจริง" ไหม

```python
# เติม: hit = (r['label'] == TARGET_CLASS and r['conf'] >= edge_ai.CONF_FLOOR)
hit = False
pass

if hit:
    streak += 1
    if streak < NEED_HITS:
        set_light(AMBER, "%d/%d" % (streak, NEED_HITS))
else:
    streak = 0
    set_light(CYAN, "watching")
```

- แทน `hit = False; pass` ด้วยเงื่อนไขสองข้อ **and** กัน: คลาสตรงเป้าหมาย **และ** มั่นใจถึงเกณฑ์
- `hit` เป็น boolean ของเฟรมเดียว — ยังไม่ยิง แค่ตัดสินว่าเฟรมนี้เข้าข่ายไหม
- ถ้าลืมกรอง `conf`: verdict ที่โมเดลเดาแบบไม่มั่นใจก็จะถูกนับด้วย → หลอกง่ายขึ้นมาก

> สังเกตว่า `streak` เพิ่มเมื่อ `hit` และรีเซ็ตเป็น 0 ทันทีที่ไม่ `hit` — บรรทัดเล็กๆ นี้แหละที่ล้างยอดแหลมเดี่ยวทิ้ง

---

# ไล่โค้ด (3) — เงื่อนไข debounce + cooldown

**ช่องเติมที่ 3**: ด่านตัดสินว่า "ยิงได้หรือยัง" — ต้องผ่านทั้ง debounce และ cooldown

```python
now = time.ticks_ms()
cooled = time.ticks_diff(now, last_fire) >= COOLDOWN_MS   # พ้นช่วงเว้นแล้วไหม
ready = streak >= NEED_HITS                               # จับครบต่อเนื่องหรือยัง
# เติม: should_fire = ready and cooled
should_fire = False
pass
if should_fire:
    ...
```

- แทน `should_fire = False; pass` ด้วย `should_fire = ready and cooled`
- `ready` มาจาก debounce (ด่าน 2 นับ streak) · `cooled` มาจาก cooldown (ด่าน 3 นับเวลา) — **ต้องจริงทั้งคู่**
- `ready` กับ `cooled` เตรียมไว้ให้แล้ว หน้าที่ของช่องนี้คือ "and" มันเข้าด้วยกัน

> ถ้าเอา `cooled` ออก เหลือแค่ `ready`: พอคลาสเป้าหมายค้างยาว จะยิงรัวทุกครั้งที่ streak ครบ — cooldown คือตัวเว้นจังหวะ

---

# ไล่โค้ด (4) — ยิง action

**ช่องเติมที่ 4**: ปลายท่อ — เมื่อผ่านครบทุกด่าน สั่งการจริงแล้วรีเซ็ตให้พร้อมรอบใหม่

```python
if should_fire:
    # เติม: fire_action(r['conf']); last_fire = now; streak = 0
    pass
```

- แทน `pass` ด้วยสามคำสั่ง: `fire_action(r['conf'])` (ยิง RGB+เสียง+log) · `last_fire = now` (เริ่มนับ cooldown ใหม่) · `streak = 0` (ล้าง streak รอบใหม่)
- `fire_action()` เตรียมไว้ให้แล้ว ข้างในทำ 3 ช่องทางครบ — ช่องนี้แค่ "เรียกใช้ + เก็บกวาดสถานะ"
- ถ้าลืม `last_fire = now`: cooldown ไม่ถูกรีเซ็ต จะยิงรัวทันทีในเฟรมถัดไป

> สามบรรทัดนี้คือ "จบหนึ่งเหตุการณ์": สั่งการ · ตั้งนาฬิกาเว้นช่วง · เคลียร์ตัวนับ พร้อมเริ่มเฝ้ารอบใหม่

---

# ลงมือทำ — เติมช่องว่างทั้ง 4 จุด

เปิด [`s16_action_pipeline.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l04-action-pipeline-lab/practice/s16_action_pipeline.py) มี `pass` วางไว้ **4 จุด** = 4 ด่านของท่อเรียงตามการไหล

| # | ด่านของท่อ | เติมด้วย | ถ้าลืม |
|---|---|---|---|
| 1 | อ่านผล | `r = edge_ai.result()` | จอไม่ขึ้นคลาส ท่อไม่เดิน |
| 2 | กรอง | `hit = (r['label'] == TARGET_CLASS and r['conf'] >= edge_ai.CONF_FLOOR)` | streak ไม่ขยับ ไม่มีวันยิง |
| 3 | debounce+cooldown | `should_fire = ready and cooled` | `should_fire` False ตลอด ไม่ยิง |
| 4 | action | `fire_action(r['conf']); last_fire = now; streak = 0` | ผ่านด่านแต่ไม่สั่งการ (หรือยิงรัว) |

ขั้นตอน:

1. ไล่หา `# เติม:` ทีละจุด แทน `pass` ตามคำใบ้
2. กด **Run** (Emulator) หรือ **Program to Device** (บอร์ด) เลือก Cough (หรือ Motion เพื่อทดสอบง่าย)
3. ทำเสียง/ท่าให้ค้าง — ดูไฟไล่ ฟ้า → เหลือง → แดง + เสียง + log ถ้าไอแวบเดียวแล้วยิง แปลว่า debounce ยังไม่ทำงาน กลับไปเช็กช่อง 2–3

> สี่ช่องนี้คือ 4 ด่านของท่อเป๊ะ — เติมครบเมื่อไร คุณจะมี action pipeline ที่กัน false positive ได้จริง

---

# หน้าตาจริงตอนรัน — บน BENTO Edge AI Emulator

ก่อนลงมือ ดูหน้าเมนู Edge AI บน Emulator ที่คุ้นกันตั้งแต่โมดูล 1: dropdown · ปุ่ม Load/Stop · การ์ดผล · แถบคะแนนต่อคลาส

![หน้า Edge AI บน BENTO Emulator: dropdown เลือกโมเดล Motion Detection ปุ่ม Load และ Stop คลาสที่ชนะ idle เวลาอนุมาน และแถบความมั่นใจของ idle circle shaking w:680](../../assets/img/edge_ai_page.png)

จอ emulator ที่รันได้จริงบนเบราว์เซอร์ (BENTO Edge AI Emulator) — ไฟล์ของบทเรียนนี้ใช้การ์ดผลกับแถบแบบเดียวกัน แล้วเพิ่มการ์ดไฟ RGB กับ log เข้ามา

> สังเกตแถบคะแนนแต่ละคลาส — พอเราเติมท่อครบ 4 ด่านแล้วรัน การ์ดไฟในหน้าของเราจะไล่สีฟ้า → เหลือง → แดง ให้เห็นกับตา

---

# ลงมือ (1) — รันบน BENTO Emulator

ไม่มีบอร์ดก็เริ่มได้ทันที:

1. เปิด **ide.tesaiot.dev** (BENTO Emulator) ในเบราว์เซอร์
2. เปิดไฟล์ [`s16_action_pipeline.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l04-action-pipeline-lab/practice/s16_action_pipeline.py)
3. กด **Run** — จะเห็นการ์ดผล + ไฟ RGB + แถบคะแนนแต่ละคลาส
4. ตั้งต้นโมเดลเป็น **Motion** (`MODEL_KEYWORD="Motion"`, `TARGET_CLASS="shaking"`) เพราะเขย่าจำลองง่ายกว่าไอ — แล้วเขย่าค้างดูไฟไล่สี
5. ลองปรับ `NEED_HITS` เป็น 1 แล้ว 5 สังเกตว่ายิงง่าย/ยากต่างกันแค่ไหน

> Motion/shaking เหมาะกับการซ้อมที่บ้านเพราะควบคุมได้ด้วยมือ พอเข้าใจท่อแล้วค่อยสลับไป Cough ตอนอยู่กับบอร์ดจริง + ไมค์

---

# ลงมือ (2) — รันบนบอร์ด BENTO จริง

บนบอร์ดจริงใช้ไมค์จริง เสียงจริง:

1. เสียบบอร์ด เปิดไฟล์ใน **BENTO IDE** กด **Program to Device**
2. ใช้ค่าตั้งต้น **Cough** (`TARGET_CLASS="cough"`) — ไอใส่ไมค์ให้ต่อเนื่องหน่อย
3. สังเกตว่าไอ **แค้กเดียวสั้นๆ** มักไม่ยิง แต่ไอเป็นชุด 2–3 ครั้งติดจะดันไฟเป็นแดง
4. ดู log ในคอนโซล: `ALERT #n ... conf ...%` พร้อมจำนวนครั้ง
5. ในฉบับเต็ม ลองไอค้างยาวๆ ดูตัวเลข `blocked` เพิ่มขึ้น — นั่นคือ cooldown กำลังกันยิงซ้ำ

> โมเดลเสียงแบบ Ready-Model (Cough/Alarm/Siren) มีขีดจำกัดจำนวนครั้งการอนุมานต่อการบูต ถ้าผลนิ่งให้รีบูตบอร์ด — ไม่ใช่โค้ดเราพัง

---

# จูน pipeline — sensitivity แลกกับ false positive

หัวใจเชิงวิศวกรรมของชุดบทเรียนนี้ ไม่มีค่าที่ "ถูก" ตายตัว ทุกค่าคือการแลกเปลี่ยน คุณต้องเลือกให้เหมาะกับงาน

<div style="text-align:center;margin:6px 0">
<svg width="880" height="150" viewBox="0 0 880 150" font-family="DejaVu Sans, sans-serif">
  <line x1="60" y1="80" x2="820" y2="80" stroke="#b0bec5" stroke-width="3"/>
  <text x="60" y="112" font-size="12" fill="#c62828">ไว (ยิงง่าย)</text>
  <text x="820" y="112" font-size="12" fill="#1565c0" text-anchor="end">เข้ม (ยิงยาก)</text>
  <circle cx="180" cy="80" r="9" fill="#c62828"/>
  <text x="180" y="58" font-size="11" fill="#c62828" text-anchor="middle">NEED_HITS=1</text>
  <text x="180" y="132" font-size="10" fill="#888" text-anchor="middle">false positive เยอะ</text>
  <circle cx="440" cy="80" r="9" fill="#2e7d32"/>
  <text x="440" y="58" font-size="11" fill="#2e7d32" text-anchor="middle">NEED_HITS=3</text>
  <text x="440" y="132" font-size="10" fill="#888" text-anchor="middle">จุดกลางที่ใช้ได้</text>
  <circle cx="700" cy="80" r="9" fill="#1565c0"/>
  <text x="700" y="58" font-size="11" fill="#1565c0" text-anchor="middle">NEED_HITS=6</text>
  <text x="700" y="132" font-size="10" fill="#888" text-anchor="middle">พลาดของจริงบ่อย</text>
</svg>
</div>

- **NEED_HITS สูง** = เตือนผิดน้อย แต่พลาดเหตุการณ์สั้นๆ ของจริง (เช่น ไอครั้งเดียว)
- **CONF_FLOOR สูง** = เชื่อเฉพาะที่มั่นใจมาก แต่เหตุการณ์คลุมเครือจะหลุด
- **COOLDOWN_MS ยาว** = ไม่รบกวนซ้ำ แต่ถ้าเกิดเหตุจริงสองครั้งติดในช่วงเว้น จะเห็นแค่ครั้งเดียว
- เครื่องมือวัดว่าจูนดีไหม: นับ **false positive** (ยิงทั้งที่ไม่มีเหตุ) เทียบ **false negative** (มีเหตุแต่ไม่ยิง)

> คำถามวิศวกรจริง: "งานนี้พลาดแบบไหนแพงกว่ากัน?" เตือนไฟไหม้พลาดของจริงไม่ได้เลย (ต้องไว) · เตือนขโมยพร่ำเพรื่อคนจะเลิกสนใจ (ต้องเข้ม) — ค่าพวกนี้คือการตัดสินใจเชิงออกแบบ

---

# แหล่งเรียนรู้เพิ่มเติม

อยากเข้าใจ debounce · false positive · hysteresis ให้ลึกขึ้น ลองตามลิงก์เหล่านี้ (เปิดดูได้ตามสะดวก):

**วิดีโอ (ลิงก์ — ของเจ้าของช่องแต่ละคน)**

- Switch bounce & debouncing อธิบายจากหน้าสัมผัสจริง — ช่อง EEVblog: https://www.youtube.com/@EEVblog
- Exponential Moving Average เข้าใจง่ายทีละสเต็ป — ช่อง StatQuest with Josh Starmer: https://www.youtube.com/@statquest
- Precision, recall & false positive คืออะไร — ช่อง 3Blue1Brown (Bayes/สถิติ): https://www.youtube.com/@3blue1brown

**ภาพ / เอกสารอ้างอิง**

- Schmitt trigger (แนวคิด hysteresis กันสัญญาณสั่นข้ามเส้น): https://en.wikipedia.org/wiki/Schmitt_trigger  (ที่มา: Wikipedia, CC BY-SA)
- Switch bounce waveform (ภาพสัญญาณเด้งของหน้าสัมผัส): https://commons.wikimedia.org/wiki/File:Bouncy_Switch.png  (ที่มา: Wikimedia Commons, public domain / CC)
- Confusion matrix (false positive / false negative): https://en.wikipedia.org/wiki/Confusion_matrix  (ที่มา: Wikipedia, CC BY-SA)

> วิดีโอ/ภาพภายนอกเป็นของเจ้าของต้นฉบับ ใช้เพื่อการศึกษา อ้างอิงลิงก์ต้นทาง — เราไม่ได้ฝังหรือทำซ้ำ เพียงชี้ทางไปอ่านต่อ

---

# ชัยชนะที่เห็นได้ + MVP ของชุดบทเรียนนี้

<div style="text-align:center;margin:14px 0">
<div style="display:inline-block;background:#e8f5e9;border:2px solid #2e7d32;border-radius:22px;padding:10px 22px;color:#2e7d32;font-weight:700;font-size:1.05em">
ชัยชนะที่เห็นได้ของชุดบทเรียนนี้ · verdict ของโมเดลจุดชนวน action จริง (ไฟแดง + เสียง + log) — และ "ไอแวบเดียว" ยิงไม่ได้
</div>
</div>

**MVP ของบทเรียน 6.3–6.4 (เกณฑ์ผ่านของชุดบทเรียน):** คุณต่อ **action pipeline แบบ debounce** ได้ — คลาสเป้าหมาย (เช่น cough) ที่จับได้ต่อเนื่องจุดชนวน action จริง ส่วนสัญญาณกระพริบสั้นๆ ถูกกันไว้ ไม่ยิง

- ทำบน **Emulator** หรือ **บอร์ดจริง** ก็ได้ (โค้ดชุดเดียวกัน)
- อธิบายได้ว่าท่อ 4 ด่านแต่ละด่านกันอะไร และจูน `NEED_HITS`/`COOLDOWN_MS` แล้วพฤติกรรมเปลี่ยนยังไง

> "ยิง action ได้" ไม่ใช่แค่ "ไฟติด" — คุณต้องแสดงให้เห็นว่า pipeline **ปฏิเสธ** สัญญาณปลอมได้ด้วย นั่นคือส่วนที่ยากและมีค่าจริง

---

# บันไดช่วยเหลือ — ใบ้ → เริ่มจากโครง → เฉลย → ฉบับเต็ม

ถ้าติด ให้ไต่บันไดนี้ทีละขั้น อย่าเพิ่งกระโดดไปดูเฉลย เพราะของจะเข้าหัวตอนที่คุณพยายามเองก่อน:

- **ใบ้** — คำใบ้อยู่ในคอมเมนต์ `# เติม:` ทั้ง 4 จุดในไฟล์ฝึก + ตารางด่านของท่อหน้าที่แล้ว บอกว่าแต่ละช่องเติมอะไร
- **เริ่มจากโครง** — [`s16_action_pipeline.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l04-action-pipeline-lab/practice/s16_action_pipeline.py) มีโครงครบทั้งไฟล์ (widget/ไฟ RGB/fire_action เตรียมไว้แล้ว) เหลือแค่ 4 บรรทัดของท่อ
- **เฉลย** — [`s16_action_pipeline.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l04-action-pipeline-lab/solution/s16_action_pipeline.py) เติมครบพร้อมคอมเมนต์อธิบายทุกด่าน (อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์เอง)
- **ฉบับเต็ม** — [`s16_action_pipeline_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l04-action-pipeline-lab/examples/s16_action_pipeline_full.py) เพิ่ม `dsp.EMA` smoothing · ไฟ RGB 4 สถานะ · `on_result` log การเปลี่ยนคลาส · ตัวนับ `blocked`

> ลองเขียนเองให้สุดก่อนนะ ถ้าติดจริงๆ ค่อยเปิดเฉลยดูทีละด่าน แล้วกลับมาพิมพ์เอง — เดี๋ยวเราค่อย ๆ แกะไปด้วยกัน

---

# เชื่อมโยงรากฐาน — วันนี้เราแตะอะไรไปบ้าง

action pipeline ตัวเดียวซ่อนแนวคิดที่ใช้ต่อได้ทั้งงาน Edge AI จริง:

**ฝั่ง Edge AI / ระบบ**
- **verdict → action** — ผลของโมเดลไม่ได้จบที่จอ มันจุดชนวนการกระทำในโลกจริง
- **false-positive handling** — เกราะ 3 ชั้น (conf floor · debounce · cooldown) คือหัวใจที่แยก demo ออกจากของใช้งาน
- **event vs poll** — `on_result` (callback) กับ `result()` (poll) เหมาะกับงานคนละแบบ เลือกให้ถูก
- **smoothing** — `dsp.EMA` จาก โมดูล 3 (Processing) กลับมาใช้กด verdict ที่กระตุก

**ฝั่ง MicroPython / โครงโปรแกรม**
- **โครงร่วมเดิม** — import → สร้างครั้งเดียว → ลูป → `ui.poll` (ของใหม่แทรกในลูป)
- **แยก fire_action() ออกมา** — ตรรกะ "จะทำอะไรตอนยิง" แก้ที่เดียว ไม่ปนกับ debounce
- **`time.ticks_ms`/`ticks_diff`** — วัดเวลาอย่างถูกต้อง รับมือ overflow
- **เก็บกวาดตอนจบ** — `finally: on_result(None); stop()` คืนเครื่องสู่สถานะที่รู้แน่

> ทั้งหมดนี้คือ "หลังบ้าน" ที่ทำให้แอป Edge AI น่าเชื่อถือพอจะปล่อยให้คนใช้จริง — ชุดบทเรียนถัดไป (บทเรียน 6.5–6.6) เราจะต่อปลายท่อออกเน็ต

---

# ใช้จริงที่ไหน — action pipeline ในโลกจริง

ทุกอุปกรณ์ Edge AI ที่ขายได้ มี pipeline แบบนี้ซ่อนอยู่หลังบ้าน หลักการเดียวกับที่เราต่อวันนี้เป๊ะ:

<div style="text-align:center;margin:6px 0">
<svg width="880" height="220" viewBox="0 0 880 220" font-family="DejaVu Sans, sans-serif">
  <rect x="12" y="10" width="420" height="96" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="28" y="34" font-size="13" font-weight="700" fill="#1565c0">เครื่องตรวจการล้ม (IMU)</text>
  <text x="28" y="56" font-size="11" fill="#555">verdict "fall" ต้องค้างจริง ไม่ใช่แค่วางโทรศัพท์แรงๆ</text>
  <text x="28" y="76" font-size="11" fill="#555">debounce กันแจ้งเตือนปลอม → ญาติไม่ตกใจฟรี</text>
  <text x="28" y="96" font-size="11" fill="#888">action: โทรฉุกเฉิน (ยิงพลาดไม่ได้ทั้งสองทาง)</text>
  <rect x="448" y="10" width="420" height="96" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="464" y="34" font-size="13" font-weight="700" fill="#2e7d32">ตรวจเสียงไอ/เสียงเตือน (MIC)</text>
  <text x="464" y="56" font-size="11" fill="#555">ไอครั้งเดียวไม่นับ ต้องเป็นชุด → debounce + cooldown</text>
  <text x="464" y="76" font-size="11" fill="#555">log ทุกครั้งพร้อมเวลา → หมอดูแนวโน้มย้อนหลังได้</text>
  <text x="464" y="96" font-size="11" fill="#888">action: บันทึก + แจ้งเตือน (คือ Cough วันนี้)</text>
  <rect x="12" y="118" width="420" height="92" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="28" y="142" font-size="13" font-weight="700" fill="#e65100">สวิตช์ไฟตามการมีคน (RADAR)</text>
  <text x="28" y="164" font-size="11" fill="#555">คนเดินผ่านแวบเดียวไม่เปิดไฟ → ต้องอยู่จริง</text>
  <text x="28" y="184" font-size="11" fill="#555">cooldown กันไฟกระพริบตอนคนขยับไปมา</text>
  <text x="28" y="202" font-size="11" fill="#888">action: เปิดรีเลย์ไฟ</text>
  <rect x="448" y="118" width="420" height="92" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="464" y="142" font-size="13" font-weight="700" fill="#6a1b9a">ร่วมกัน — ชั้นตัดสินใจ</text>
  <text x="464" y="164" font-size="11" fill="#555">ทุกงานมี verdict → กรอง → debounce → cooldown → action</text>
  <text x="464" y="184" font-size="11" fill="#555">ต่างกันแค่ปลายท่อ (เสียง/รีเลย์/เน็ต) และค่าจูน</text>
  <text x="464" y="202" font-size="11" fill="#888">6.5–6.6 ต่อปลายท่อออก WiFi/MQTT</text>
</svg>
</div>

> ท่อ 4 ด่านที่เราต่อวันนี้ ไม่ใช่ของสมมติ — มันคือชั้นที่ทำให้ Edge AI ในตลาด "เชื่อถือได้" เราแค่ต่อมันด้วยมือตัวเองในไม่กี่บรรทัด

---

# งานทำเอง + สรุปบทเรียน

**งานทำเอง (ท้ายบทเรียน):**

1. เติม [`s16_action_pipeline.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l04-action-pipeline-lab/practice/s16_action_pipeline.py) ให้ครบทั้ง 4 ช่อง รันได้จริง (Emulator หรือบอร์ด)
2. จูน `NEED_HITS` อย่างน้อย **3 ค่า** (เช่น 1, 3, 6) จดว่าแต่ละค่ายิงง่าย/ยากต่างกันแค่ไหน และเกิด false positive กี่ครั้ง
3. หาสัญญาณที่ **ควรถูกกัน** (เช่น ไอแวบเดียว / ขยับผ่านเร็วๆ) แล้วยืนยันว่า pipeline กันมันได้จริง อธิบายว่าด่านไหนกัน

ใบ้ข้อ 3 — สัญญาณสั้นๆ ที่หลุด CONF_FLOOR ได้ จะถูกด่าน debounce (streak) จับไว้ เพราะมันไม่ค้างต่อเนื่อง ลองดูตัวเลข streak ตอนนั้นว่าขึ้นถึงเท่าไรแล้วรีเซ็ต

**วันนี้เราได้:** เข้าใจ verdict → action · เห็นปัญหา false positive จริง · ต่อเกราะ 3 ชั้น (conf floor · debounce · cooldown) + smoothing · แยก event (`on_result`) กับ poll · สั่งการ 3 ช่อง (RGB · เสียง · log)

> ชุดบทเรียนถัดไป (บทเรียน 6.5–6.6) เราจะ **รวม verdict กับเซนเซอร์ดิบ** (sensor fusion) แล้วส่ง action ออกเน็ตด้วย WiFi/MQTT — ปลายท่อของวันนี้จะยื่นไปถึงคลาวด์ เจอกันครับ
