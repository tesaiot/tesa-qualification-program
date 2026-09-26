---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 1.7 — ลงมือทำ: จาก verdict สู่ action บนบอร์ด"
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

# บทเรียน 1.7 — ลงมือทำ: จาก verdict สู่ action บนบอร์ด

## แกะแอป Edge AI · จาก verdict สู่ action

**โมดูล 1 — เริ่มต้น: รันของจริงแล้วแกะดูข้างใน**

> ต่อจากบทเรียน 1.6 — แกะแอป Edge AI: ทะเบียนโมเดล verdict และ action

---

# ไล่หนึ่งรอบเต็ม — sensor → model → UI → action

รวมทุกจังหวะเป็นภาพเดียว: จากเซนเซอร์บนบอร์ด จนถึงเสียงบี๊บที่คุณได้ยิน — นี่คือวงจรที่แอปชุดบทเรียนนี้เดินทุก ~180 ms

<div style="text-align:center;margin:6px 0">
<svg width="920" height="180" viewBox="0 0 920 180" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arCyc" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g text-anchor="middle">
    <rect x="10" y="56" width="150" height="66" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="85" y="84" font-size="12" font-weight="700" fill="#1565c0">เซนเซอร์</text>
    <text x="85" y="104" font-size="10" fill="#888">IMU/RADAR/MIC</text>
    <rect x="192" y="56" width="150" height="66" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
    <text x="267" y="80" font-size="12" font-weight="700" fill="#6a1b9a">โมเดล (M55)</text>
    <text x="267" y="100" font-size="10" fill="#888">NPU อนุมาน</text>
    <rect x="374" y="56" width="150" height="66" rx="10" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
    <text x="449" y="80" font-size="12" font-weight="700" fill="#455a64">result()</text>
    <text x="449" y="100" font-size="10" fill="#888">verdict dict</text>
    <rect x="556" y="56" width="150" height="66" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="631" y="80" font-size="12" font-weight="700" fill="#e65100">จอ + เงื่อนไข</text>
    <text x="631" y="100" font-size="10" fill="#888">label + conf</text>
    <rect x="738" y="56" width="170" height="66" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="823" y="80" font-size="12" font-weight="700" fill="#2e7d32">action</text>
    <text x="823" y="100" font-size="10" fill="#888">บี๊บ + แบนเนอร์</text>
  </g>
  <line x1="160" y1="89" x2="190" y2="89" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arCyc)"/>
  <line x1="342" y1="89" x2="372" y2="89" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arCyc)"/>
  <line x1="524" y1="89" x2="554" y2="89" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arCyc)"/>
  <line x1="706" y1="89" x2="736" y2="89" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arCyc)"/>
  <text x="267" y="40" font-size="10" fill="#999" text-anchor="middle">CM55 + NPU</text>
  <text x="620" y="40" font-size="10" fill="#999" text-anchor="middle">โค้ด Python บน CM33</text>
  <path d="M823,122 C823,156 85,156 85,124" fill="none" stroke="#9e9e9e" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arCyc)"/>
  <text x="460" y="152" font-size="11" fill="#9e9e9e" text-anchor="middle">วนรอบใหม่ทุก ~180 ms</text>
</svg>
</div>

> ครึ่งซ้าย (เซนเซอร์ → โมเดล) เกิดบน CM55 อัตโนมัติ เราไม่แตะ · ครึ่งขวา (result → จอ → action) คือโค้ด Python ของเราบน CM33 — ชุดบทเรียนนี้เราคุมครึ่งขวาทั้งหมด

---

# โครงของไฟล์ s03_anatomy_edgeai.py

ทั้งไฟล์อ่านเป็นประโยคเดียว: **"หาโมเดลจากชื่อ → สั่งรัน → วนอ่านผลขึ้นจอ → พอเจอคลาสเป้าหมายมั่นใจพอ ก็สั่งการ → หยุดตอนออก"**

<div style="text-align:center;margin:6px 0">
<svg width="920" height="210" viewBox="0 0 920 210" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arS3" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g font-size="14" text-anchor="middle">
    <rect x="14" y="24" width="180" height="54" rx="10" fill="#cfd8dc" stroke="#607d8b" stroke-width="2"/>
    <text x="104" y="47" font-weight="700" fill="#455a64">find_model</text>
    <text x="104" y="66" font-size="11" fill="#999">:37 (ให้ไว้แล้ว)</text>
    <rect x="234" y="24" width="180" height="54" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="324" y="47" font-weight="700" fill="#1565c0">select</text>
    <text x="324" y="66" font-size="11" fill="#999">ช่อง 1</text>
    <rect x="454" y="24" width="180" height="54" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="544" y="47" font-weight="700" fill="#e65100">อ่านผล + จอ</text>
    <text x="544" y="66" font-size="11" fill="#999">ช่อง 2+3</text>
    <polygon points="704,51 754,23 804,51 754,79" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
    <text x="754" y="47" font-weight="700" fill="#6a1b9a" font-size="12">hit?</text>
    <rect x="834" y="24" width="76" height="54" rx="10" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
    <text x="872" y="55" font-size="11" fill="#455a64">ออก→stop</text>
    <rect x="454" y="140" width="200" height="58" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="554" y="164" font-weight="700" fill="#2e7d32">fire_action</text>
    <text x="554" y="182" font-size="11" fill="#999">ช่อง 4 · ยิงครั้งเดียว</text>
  </g>
  <line x1="194" y1="51" x2="232" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS3)"/>
  <line x1="414" y1="51" x2="452" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS3)"/>
  <line x1="634" y1="51" x2="702" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS3)"/>
  <line x1="804" y1="51" x2="832" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS3)"/>
  <text x="820" y="43" font-size="11" fill="#607d8b">no</text>
  <path d="M754,79 C754,120 554,110 554,138" fill="none" stroke="#2e7d32" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arS3)"/>
  <text x="700" y="112" font-size="12" fill="#2e7d32">yes → สั่งการ</text>
  <text x="470" y="206" font-size="11" fill="#888" text-anchor="middle">แถวล่าง = จังหวะ 3 (action) ที่ต่อจากการวาดจอ</text>
</svg>
</div>

> ตัวเลขช่อง (1–4) ชี้จุดที่คุณต้องเติมในไฟล์ฝึก — เหมือนบทเรียน 1.1–1.3 แต่ช่องที่ 4 เปลี่ยนจาก `stop()` มาเป็น **`fire_action()`** ซึ่งคือหัวใจใหม่ของชุดบทเรียนนี้

---

# ไล่โค้ด (1) — find_model + select

**ช่องเติมที่ 1**: หาโมเดลจากชื่อ (ให้ไว้แล้ว) แล้วสั่งให้ CM55 เริ่มรัน:

```python
model = find_model(MODEL_KEYWORD)   # ให้ไว้แล้ว: คืน dict ทั้งก้อน
labels = model['labels']

try:
    # เติม: สั่งให้ CM55 รันโมเดลนี้ ด้วย edge_ai.select(model['index'])
    pass
    lcd.console('<span class=ok> เริ่มอนุมาน…</span>')
except OSError as e:
    lcd.console('<span class=error> โหลดไม่สำเร็จ: %s</span>' % e)
```

- แทน `pass` ด้วย `edge_ai.select(model['index'])` — เอา index จาก dict ไปสั่ง
- ต้องอยู่ใน `try` เพราะ `select()` โยน `OSError` ได้ (ข้ามคอร์อาจพลาด — เหมือนบทเรียน 1.1–1.3)
- ถ้าลืมเติม: จอค้างที่ `---` ตลอด เพราะไม่มีโมเดลรัน `result()` คืน `None`

> `MODEL_KEYWORD` อยู่บนหัวไฟล์ — remix ได้ทันที เปลี่ยนเป็น `"Cough"` แอปก็กลายเป็นตัวจับเสียงไอ โดยไม่แตะ logic ข้างล่างเลย

---

# ไล่โค้ด (2) — อ่านผล + verdict.text

**ช่องเติมที่ 2 และ 3**: จังหวะ 2 เดิมจากบทเรียน 1.1–1.3 อ่าน verdict แล้วเอาคลาสที่ชนะขึ้นจอ:

```python
# เติม: อ่านผลอนุมานล่าสุดมาเก็บใน r  ->  r = edge_ai.result()
r = None
pass
if r and r['seq'] != last_seq:          # มีผลใหม่จริงไหม (seq เปลี่ยน)
    last_seq = r['seq']
    # เติม: แสดงคลาสที่ชนะ ด้วย verdict.text(r['label'] or '-')
    pass
    conf.text("conf: %.0f %%" % (r['conf'] * 100))
    top = r['top']
    for i, (lb, br) in enumerate(rows):
        if i < len(r['scores']):
            br.value(int(r['scores'][i] * 100))
            br.color(GREEN if i == top else DIM)
```

- ช่อง 2: `r = edge_ai.result()` · ช่อง 3: `verdict.text(r['label'] or '-')`
- เช็ก `seq` ก่อนเสมอ — วาดจอเฉพาะตอนมีผลใหม่ (เหตุผลเดียวกับบทเรียน 1.1–1.3)

> สองช่องนี้เป็น "ของเดิม" ที่คุณทำเป็นแล้วจากบทเรียน 1.1–1.3 — วางไว้ให้ทวน จังหวะที่ 3 ต่างหากคือของใหม่จริงๆ ที่ต้องโฟกัส

---

# ไล่โค้ด (3) — เงื่อนไข hit + fire_action

**ช่องเติมที่ 4**: จังหวะ 3 (ของใหม่) — พอวาดจอเสร็จ เช็กว่าเข้าเงื่อนไขไหม ถ้าใช่ก็สั่งการ:

```python
    hit = (r['label'] == TARGET_CLASS
           and r['conf'] >= edge_ai.CONF_FLOOR)   # label ตรง + มั่นใจพอ
    if hit and not fired:
        # เติม: สั่งการเมื่อจับ TARGET ได้ครั้งแรก -> fire_action(r['conf'])
        pass
        fired = True
    elif not hit:
        fired = False                              # ออกจากคลาสแล้ว รีเซ็ต
        banner.text("รอจับ %s ..." % TARGET_CLASS)
        banner.color(RED)
```

- แทน `pass` ด้วย `fire_action(r['conf'])` — ส่ง `conf` เข้าไปให้ action โชว์
- `and not fired` = ยิงครั้งเดียวต่อการเจอ (edge-trigger) ไม่บี๊บรัว
- ถ้าลืมเติม: จอโชว์คลาสถูก แต่ไม่มีเสียง ไม่มีแบนเนอร์ — แอปยัง "ไม่ลงมือ"

> นี่คือบรรทัดที่ทำให้แอปชุดบทเรียนนี้ต่างจากบทเรียน 1.1–1.3 — verdict กลายเป็น action ตรงจุดนี้เป๊ะ เติมเสร็จเมื่อไร แอปของคุณ "ทำงาน" ไม่ใช่แค่ "รายงาน"

---

# ไล่โค้ด (4) — หยุดให้เรียบร้อย

ปุ่ม back และการเก็บกวาดตอนออก (ให้ไว้แล้ว — เหมือนบทเรียน 1.1–1.3):

```python
finally:
    edge_ai.stop()      # ให้ไว้แล้ว: ออกยังไงก็หยุดเครื่องยนต์เสมอ
    lcd.console('<span class=ok> จบการทำงาน</span>')
```

- บล็อก `finally` ให้ไว้แล้ว: ไม่ว่าจะออกด้วยปุ่ม back หรือ error โมเดลจะถูกหยุดเสมอ
- ในฉบับเต็มที่ใช้ `on_result` ต้องถอน callback ด้วย: `edge_ai.on_result(None)` ก่อน `stop()`

> นิสัย embedded เดิม: **ออกจากงานยังไง ทิ้งเครื่องไว้ให้เรียบร้อยแบบนั้น** — หยุดโมเดล ถอน callback ที่ต่อไว้ ไม่ปล่อยอะไรค้างหลังโปรแกรมจบ

---

# remix (1) — สลับโมเดล + เปลี่ยนคลาสเป้าหมาย

หัวใจของ MVP วันนี้คือ **remix** — และจุด remix แรกอยู่บนหัวไฟล์แค่สองบรรทัด:

```python
MODEL_KEYWORD = "Motion"     # → "Baby Cry" / "Cough" / "Siren" / "Push"
TARGET_CLASS  = "shaking"    # → คลาสของโมเดลใหม่ (ดูจาก labels ในคอนโซล)
```

- เปลี่ยน `MODEL_KEYWORD` = สลับทั้งโมเดลและเซนเซอร์ (IMU → MIC → RADAR) โดยไม่แตะ logic
- เปลี่ยน `TARGET_CLASS` = เปลี่ยนว่า "จับอะไรแล้วสั่งการ" — ต้องเป็นชื่อจาก `labels` ของโมเดลนั้นเป๊ะ
- ตัวอย่าง remix เสียงไอ: `MODEL_KEYWORD = "Cough"`, `TARGET_CLASS = "cough"`

> อยากรู้ว่าโมเดลใหม่มีคลาสอะไร? รันแล้วดูบรรทัด `โมเดล: ... คลาส: ...` ในคอนโซล หรือถาม REPL: `edge_ai.models()` — ถามฮาร์ดแวร์ก่อนเสมอ

---

# remix (2) — เปลี่ยน action

จุด remix ที่สองคือ **การกระทำ** — แก้แค่ใน `fire_action()` ที่เดียว logic ตรวจจับไม่ต้องแตะ:

- **เปลี่ยนเสียง** — `ui.tone(60, ...)` (โดกลาง) แทน 72 หรือใช้ `ui.sfx(ui.SFX_UI_SELECT)` เล่นเสียงสำเร็จรูป
- **action สองระดับ** — ถ้า `conf` สูงมากบี๊บสองครั้ง ถ้าพอผ่านเกณฑ์บี๊บครั้งเดียว
- **นับเหตุการณ์** — เก็บตัวนับว่ายิง action ไปกี่ครั้ง แล้วโชว์บนจอ (ฉบับเต็มทำแบบนี้)
- **แจ้งเตือนจริง** — (ต่อยอด โมดูล 6 (Apps)) ส่ง MQTT / เขียนไฟล์ log เมื่อเจอ

> เพราะเราแยก "ตัดสินใจ" ออกจาก "ลงมือ" การ remix action จึงปลอดภัย — คุณเปลี่ยนสิ่งที่แอป **ทำ** ได้ โดยไม่กระทบสิ่งที่แอป **ตรวจจับ**

---

# ลงมือทำ — เติมช่องว่างทั้ง 4 จุด

เปิด [`s03_anatomy_edgeai.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l07-verdict-action-lab/practice/s03_anatomy_edgeai.py) ในไฟล์มี `pass` วางไว้ **4 จุด** ตรงที่ต้องเติมคำสั่งจริง:

| # | จุด | เติมด้วย | ถ้าลืม |
|---|---|---|---|
| 1 | หลัง find_model | `edge_ai.select(model['index'])` | จอค้าง `---` ไม่มีผล |
| 2 | ในลูป | `r = edge_ai.result()` | จอไม่ขึ้นคลาสเลย |
| 3 | มีผลใหม่ | `verdict.text(r['label'] or '-')` | แถบขยับ แต่ตัวใหญ่ไม่เปลี่ยน |
| 4 | เข้าเงื่อนไข hit | `fire_action(r['conf'])` | เจอคลาสถูก แต่ไม่บี๊บ ไม่มีแบนเนอร์ |

ขั้นตอน:

1. ตั้ง `MODEL_KEYWORD` + `TARGET_CLASS` ที่อยากลอง (เริ่มจาก Motion/shaking ก็ได้)
2. ไล่หา `# เติม:` ทีละจุด แล้วแทน `pass` ด้วยคำสั่งตามคำใบ้
3. กด **Run** (Emulator) หรือ **Program to Device** (บอร์ด) ทำท่า/ส่งเสียงจนแบนเนอร์ขึ้น + ได้ยินบี๊บ

> ช่อง 1–3 คือของเดิมจากบทเรียน 1.1–1.3 (แค่ทวน) ช่อง 4 คือของใหม่ — เติมครบเมื่อไร คุณได้แอป Edge AI ที่ "ลงมือทำ" ตัวแรกของตัวเอง

---

# แหล่งเรียนรู้เพิ่มเติม — softmax และความมั่นใจ

อยากเข้าใจ softmax/argmax ให้ลึกกว่าในบทเรียน ลองดูสื่อคุณภาพเหล่านี้ (ลิงก์ไปต้นทาง ไม่ได้ฝังวิดีโอไว้ในสไลด์):

**วิดีโอ**

- Softmax และ ArgMax อธิบายทีละขั้น — StatQuest with Josh Starmer: https://www.youtube.com/@statquest
- Neural networks (ชุดวิชวลไลซ์คลาสสิกที่พา softmax เข้าใจภาพรวม) — 3Blue1Brown: https://www.3blue1brown.com/topics/neural-networks
- But what is a neural network? — 3Blue1Brown: https://www.youtube.com/@3blue1brown

**เอกสาร / ภาพอ้างอิง**

- Softmax function (นิยาม + สูตร + ภาพประกอบ) — Wikipedia: https://en.wikipedia.org/wiki/Softmax_function  (ที่มา: Wikipedia, CC BY-SA)
- Arg max (นิยาม argmax) — Wikipedia: https://en.wikipedia.org/wiki/Arg_max  (ที่มา: Wikipedia, CC BY-SA)
- tf.nn.softmax (สูตรเดียวกับที่โมเดลใช้จริงตอน inference) — TensorFlow docs: https://www.tensorflow.org/api_docs/python/tf/nn/softmax

> วิดีโอ/ภาพภายนอกเป็นของเจ้าของต้นฉบับ ใช้เพื่อการศึกษา อ้างอิงลิงก์ต้นทาง

---

# ชัยชนะที่เห็นได้ + MVP ของชุดบทเรียนนี้

<div style="text-align:center;margin:14px 0">
<div style="display:inline-block;background:#e8f5e9;border:2px solid #2e7d32;border-radius:22px;padding:10px 22px;color:#2e7d32;font-weight:700;font-size:1.05em">
ชัยชนะที่เห็นได้ของชุดบทเรียนนี้ · remix แอป Edge AI ให้จับคลาสเป้าหมายได้เอง แล้ว "บี๊บ + ขึ้นแบนเนอร์" สั่งการจริง
</div>
</div>

**MVP ของบทเรียน 1.6–1.7 (เกณฑ์ผ่านของชุดบทเรียน):** คุณ remix [`s03_anatomy_edgeai.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l07-verdict-action-lab/practice/s03_anatomy_edgeai.py) ได้จริง — **สลับโมเดล** (เปลี่ยน `MODEL_KEYWORD`/`TARGET_CLASS`) + **สั่งการเมื่อเจอ verdict** ที่เข้าเงื่อนไข

- ทำบน **Emulator** หรือ **บอร์ดจริง** ก็ได้ (โค้ดชุดเดียวกัน)
- อธิบายได้ว่าทำไม action เช็กทั้ง `label` **และ** `conf >= CONF_FLOOR` และทำไมต้องมี `fired`

> "สั่งการได้" ไม่ใช่แค่ "เห็นแบนเนอร์" — คุณต้องบอกได้ว่าแอปนี้ต่างจากบทเรียน 1.1–1.3 ตรงไหน (จังหวะ action) และ remix ของคุณเปลี่ยนอะไรไปจากต้นฉบับ

---

# บันไดช่วยเหลือ — ใบ้ → เริ่มจากโครง → เฉลย → ฉบับเต็ม

ถ้าติด ให้ไต่บันไดนี้ทีละขั้น อย่าเพิ่งกระโดดไปดูเฉลย เพราะของจะเข้าหัวตอนที่คุณพยายามเองก่อน:

- **ใบ้** — คำใบ้อยู่ในคอมเมนต์ `# เติม:` ทั้ง 4 จุดในไฟล์ฝึก + ตารางหน้าที่แล้ว บอกว่าแต่ละช่องเติมอะไร
- **เริ่มจากโครง** — [`s03_anatomy_edgeai.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l07-verdict-action-lab/practice/s03_anatomy_edgeai.py) มีโครงครบทั้งไฟล์แล้ว เหลือแค่ 4 บรรทัดให้เติม
- **เฉลย** — [`s03_anatomy_edgeai.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l07-verdict-action-lab/solution/s03_anatomy_edgeai.py) เติมครบพร้อมคอมเมนต์อธิบายทุกช่อง (อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์เอง)
- **ฉบับเต็ม** — [`s03_anatomy_edgeai_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l07-verdict-action-lab/examples/s03_anatomy_edgeai_full.py) ยกไปใช้ `on_result` + แยกสี CONF_FLOOR + นับจำนวน action + latency

> ลองเขียนเองให้สุดก่อนนะ ถ้าติดจริงๆ ค่อยเปิดเฉลยดูทีละช่อง แล้วกลับมาพิมพ์เอง — เดี๋ยวเราค่อย ๆ แกะไปด้วยกัน

---

# เชื่อมโยงรากฐาน — วันนี้เราแตะอะไรไปบ้าง

การ remix แอป Edge AI ตัวเดียวซ่อนแนวคิดที่จะใช้ไปตลอด โมดูล 6 (Apps):

**ฝั่ง Edge AI / ระบบ**
- **Model registry** — เลือกโมเดลจากชื่อด้วย `find_model()` ไม่ hard-code index (ทนต่อการเปลี่ยนเฟิร์มแวร์)
- **Verdict → decision** — action ตั้งอยู่บน `label` + `conf >= CONF_FLOOR` ไม่ใช่ป้ายคลาสเดียวๆ
- **Verdict → action** — จาก inference สู่ application: การกระทำจริงเมื่อเข้าเงื่อนไข
- **Event-driven** — `on_result(cb)` เฟิร์มแวร์เรียก cb ให้ตอนคลาสเปลี่ยน (แทน poll เอง)

**ฝั่ง MicroPython / โครงโปรแกรม**
- **แยกตัดสินใจจากลงมือ** — เงื่อนไข `hit` แยกจาก `fire_action()` remix ง่าย
- **edge-trigger** — ธง `fired` ยิง action ครั้งเดียวต่อการเจอ ไม่รัว
- **เก็บกวาดตอนจบ** — `finally: stop()` (+ `on_result(None)` ในฉบับเต็ม)

> ทั้งหมดยังยืนบนคำสั่งเดิมของ `edge_ai` — ชุดบทเรียนนี้ไม่ได้เพิ่มของยาก แต่สอน "ประกอบ" คำสั่งเดิมให้กลายเป็นแอปที่ลงมือทำได้

---

# ใช้จริงที่ไหน — verdict → action ในโลกจริง

pattern "จับคลาสเป้าหมาย แล้วสั่งการ" ที่เราทำวันนี้ คือแก่นของสินค้า Edge AI จริงทุกตัว:

<div style="text-align:center;margin:6px 0">
<svg width="880" height="220" viewBox="0 0 880 220" font-family="DejaVu Sans, sans-serif">
  <rect x="12" y="10" width="420" height="96" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="28" y="34" font-size="13" font-weight="700" fill="#1565c0">Motion (IMU) — นาฬิกาตรวจการล้ม</text>
  <text x="28" y="56" font-size="11" fill="#555">verdict: "fall" เกินเกณฑ์ → action: โทรฉุกเฉิน</text>
  <text x="28" y="76" font-size="11" fill="#555">ต้องยิงครั้งเดียว ไม่โทรรัวทุกเฟรม</text>
  <text x="28" y="96" font-size="11" fill="#888">= edge-trigger + CONF_FLOOR ของเราวันนี้</text>
  <rect x="448" y="10" width="420" height="96" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="464" y="34" font-size="13" font-weight="700" fill="#2e7d32">เสียง (MIC) — เครื่องเฝ้าเด็ก</text>
  <text x="464" y="56" font-size="11" fill="#555">verdict: "baby_cry" → action: แจ้งมือถือพ่อแม่</text>
  <text x="464" y="76" font-size="11" fill="#555">เสียงไม่ออกจากเครื่อง → ความเป็นส่วนตัว</text>
  <text x="464" y="96" font-size="11" fill="#888">= remix "Baby Cry" ของเราวันนี้</text>
  <rect x="12" y="118" width="420" height="92" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="28" y="142" font-size="13" font-weight="700" fill="#e65100">เรดาร์ (RADAR) — สวิตช์ไร้สัมผัส</text>
  <text x="28" y="164" font-size="11" fill="#555">verdict: "Push" → action: เปิดไฟ/ประตู</text>
  <text x="28" y="184" font-size="11" fill="#555">ทำงานในที่มืด ไม่ใช้กล้อง</text>
  <text x="28" y="202" font-size="11" fill="#888">= remix "Push" ของเราวันนี้</text>
  <rect x="448" y="118" width="420" height="92" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="464" y="142" font-size="13" font-weight="700" fill="#6a1b9a">ร่วมกัน — verdict + action</text>
  <text x="464" y="164" font-size="11" fill="#555">ทุกสินค้า = จับคลาส + ตัดสินด้วย conf + ลงมือ</text>
  <text x="464" y="184" font-size="11" fill="#555">ต่างกันแค่ "action" ปลายทาง</text>
  <text x="464" y="202" font-size="11" fill="#888">คือ โมดูล 6 (Apps, โมดูล 6) ของเรา</text>
</svg>
</div>

> สังเกตว่าทุกสินค้าใช้ pattern เดียวกับแอปชุดบทเรียนนี้เป๊ะ — ต่างกันแค่ action ปลายทาง เราแค่กำลังเริ่มจากปลายทางเพื่อย้อนไปสร้างเองได้

---

# งานทำเอง + สรุปบทเรียน

**งานทำเอง (ท้ายบทเรียน):**

1. เติม [`s03_anatomy_edgeai.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l07-verdict-action-lab/practice/s03_anatomy_edgeai.py) ให้ครบทั้ง 4 ช่อง รันได้จริง (Emulator หรือบอร์ด)
2. **remix**: เปลี่ยน `MODEL_KEYWORD` + `TARGET_CLASS` เป็นโมเดลอื่น (เช่น Motion → Cough) ยืนยัน action ยิงตามคลาสใหม่
3. หาท่า/เสียงที่ทำให้คลาสเป้าหมาย "ชนะแต่ conf ต่ำกว่า CONF_FLOOR" แล้วอธิบายว่าทำไม action ถึงไม่ยิง

ใบ้ข้อ 3 — เงื่อนไข `hit` เช็กทั้ง `label` **และ** `conf` ถ้าคลาสถูกแต่มั่นใจไม่ถึงเกณฑ์ `hit` เป็น `False` action จึงไม่ยิง (นี่คือตัวกัน false positive)

**วันนี้เราได้:** แกะกายวิภาคแอป Edge AI เป็น 3 จังหวะ (`select`→`result`→`action`) · เลือกโมเดลจากชื่อ · เพิ่ม action บน verdict ด้วยเงื่อนไข label+conf · รู้จัก `on_result` · remix เป็นแอปของตัวเอง

> ชุดบทเรียนถัดไป (บทเรียน 2.1–2.2) เราปิดกล่อง Onboarding แล้วเปิด **Pillar 1 — DAQ**: เริ่มเก็บข้อมูลเซนเซอร์ของเราเองลงไฟล์ CSV เพื่อเป็นวัตถุดิบฝึกโมเดลในบล็อกถัดๆ ไป เจอกันครับ
