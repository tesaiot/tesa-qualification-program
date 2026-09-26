---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 1.3 — ลงมือทำ: เมนูโมเดลตัวแรกของเรา"
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

# บทเรียน 1.3 — ลงมือทำ: เมนูโมเดลตัวแรกของเรา

## Edge AI และวงจรชีวิตของข้อมูล · รันโมเดลตัวแรกของเรา

**โมดูล 1 — เริ่มต้น: รันของจริงแล้วแกะดูข้างใน**

> ต่อจากบทเรียน 1.2 — โมดูล edge_ai: ถามทะเบียนโมเดล เลือก แล้วอ่านคำตอบ

---

# โครงร่วมของทุกโปรแกรม MicroPython

ก่อนดูโค้ดจริง จับ "โครง" ให้ได้ก่อน โปรแกรม MicroPython บน BENTO เกือบทุกตัวเดินตามสี่จังหวะนี้ (เราจะเจอซ้ำทั้งคอร์ส):

<div style="text-align:center;margin:6px 0">
<svg width="880" height="130" viewBox="0 0 880 130" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arSk" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="20" y="40" width="190" height="56" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="115" y="64" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">1 · import</text>
  <text x="115" y="84" font-size="11" fill="#666" text-anchor="middle">edge_ai · ui · lcd · time</text>
  <rect x="238" y="40" width="200" height="56" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="338" y="64" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">2 · สร้างครั้งเดียว</text>
  <text x="338" y="84" font-size="11" fill="#666" text-anchor="middle">อ่าน models() + widget</text>
  <rect x="466" y="40" width="190" height="56" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="561" y="64" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">3 · ลูป</text>
  <text x="561" y="84" font-size="11" fill="#666" text-anchor="middle">อ่านผล + อัปเดตจอ</text>
  <rect x="684" y="40" width="176" height="56" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="772" y="64" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">4 · ui.poll</text>
  <text x="772" y="84" font-size="11" fill="#666" text-anchor="middle">รับปุ่ม/แตะจอ</text>
  <line x1="210" y1="68" x2="236" y2="68" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <line x1="438" y1="68" x2="464" y2="68" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <line x1="656" y1="68" x2="682" y2="68" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arSk)"/>
  <path d="M772,96 C772,116 561,116 561,98" fill="none" stroke="#9e9e9e" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arSk)"/>
  <text x="666" y="120" font-size="11" fill="#9e9e9e" text-anchor="middle">วนกลับ</text>
</svg>
</div>

> **"สร้างครั้งเดียว"** สำคัญมาก: สร้าง widget นอกลูป ในลูปแค่เปลี่ยนค่า/ข้อความ ถ้าสร้างซ้ำทุกรอบ จอจะกระพริบและกินหน่วยความจำ บทเรียน 1.4–1.5 เราจะแกะโครงนี้ให้ละเอียด

---

# โครงของไฟล์ s01_first_inference.py

ทั้งไฟล์อ่านเป็นประโยคเดียว: **"ถามว่ามีโมเดลอะไร → เลือกหนึ่งตัว → วนอ่านผล → เอาคลาสที่ชนะขึ้นจอ → หยุดตอนออก"**

<div style="text-align:center;margin:6px 0">
<svg width="920" height="220" viewBox="0 0 920 220" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arS1" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g font-size="14" text-anchor="middle">
    <rect x="14" y="24" width="170" height="54" rx="10" fill="#cfd8dc" stroke="#607d8b" stroke-width="2"/>
    <text x="99" y="47" font-weight="700" fill="#455a64">อ่านทะเบียน</text>
    <text x="99" y="66" font-size="11" fill="#999">models() :33</text>
    <rect x="224" y="24" width="170" height="54" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="309" y="47" font-weight="700" fill="#1565c0">สร้าง widget</text>
    <text x="309" y="66" font-size="11" fill="#999">dropdown+การ์ด :39</text>
    <rect x="434" y="24" width="170" height="54" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="519" y="47" font-weight="700" fill="#e65100">กด Load</text>
    <text x="519" y="66" font-size="11" fill="#999">select(sel) :103</text>
    <polygon points="689,51 739,23 789,51 739,79" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
    <text x="739" y="47" font-weight="700" fill="#6a1b9a" font-size="12">running?</text>
    <rect x="820" y="24" width="90" height="54" rx="10" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
    <text x="865" y="55" font-size="12" fill="#455a64">ออก→stop</text>
    <!-- row B -->
    <rect x="224" y="140" width="180" height="58" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="314" y="164" font-weight="700" fill="#e65100">อ่านผล</text>
    <text x="314" y="183" font-size="11" fill="#999">result() :124</text>
    <rect x="434" y="140" width="180" height="58" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="524" y="160" font-weight="700" fill="#2e7d32">คลาสที่ชนะ</text>
    <text x="524" y="178" font-size="11" fill="#999">verdict.text :128</text>
    <text x="524" y="192" font-size="10" fill="#999">+ แถบ scores</text>
  </g>
  <line x1="184" y1="51" x2="222" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS1)"/>
  <line x1="394" y1="51" x2="432" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS1)"/>
  <line x1="604" y1="51" x2="687" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS1)"/>
  <line x1="789" y1="51" x2="818" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS1)"/>
  <text x="806" y="43" font-size="11" fill="#607d8b">no</text>
  <path d="M739,79 C739,120 314,110 314,138" fill="none" stroke="#2e7d32" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arS1)"/>
  <text x="520" y="112" font-size="12" fill="#2e7d32">yes → วนอ่านผลทุก 180 ms</text>
  <line x1="404" y1="169" x2="432" y2="169" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS1)"/>
  <text x="470" y="214" font-size="11" fill="#888" text-anchor="middle">แถวล่าง = สิ่งที่เกิดในลูปเมื่อโมเดลกำลังรัน</text>
</svg>
</div>

> ตัวเลขบรรทัด (`:103`, `:124`, `:128`) ชี้ไปที่จุดที่คุณต้องเติมโค้ดในไฟล์ฝึก จำโครงนี้ไว้ เดี๋ยวไล่ดูทีละส่วน

---

# ไล่โค้ด (1) — อ่านทะเบียนโมเดล

ส่วนแรกของไฟล์ ถามเฟิร์มแวร์ว่ามีโมเดลอะไร แล้วเอาชื่อไปทำ dropdown:

```python
import edge_ai
import ui
ui.screen()
import lcd, time

models = edge_ai.models()               # ถามเฟิร์มแวร์ (ให้ไว้แล้ว)
names = [m['name'] for m in models]     # ดึงเฉพาะชื่อไปทำ dropdown
lcd.console(' พบ %d โมเดล: %s' % (len(models), ", ".join(names)))

dd = ui.Dropdown(text="\n".join(names), x=20, y=42, w=250)
btn_load = ui.Button("Load", x=285, y=42, w=88, h=36)
```

- `models()` ให้ list ของ dict — เราวนดึง `m['name']` มาต่อเป็นบรรทัดใน dropdown
- บรรทัดนี้ให้ไว้แล้วในไฟล์ฝึก เพราะทั้งไฟล์ต้องพึ่ง `models` แต่คุณควรอ่านให้เข้าใจว่ามันได้อะไรมา

> ลองใน REPL ก่อนก็ได้: `import edge_ai; edge_ai.models()` แล้วดูว่าตอบอะไรกลับมา — นี่คือวิธี "ถามฮาร์ดแวร์" ที่เร็วที่สุด

---

# ไล่โค้ด (2) — กด Load แล้ว select()

**ช่องเติมที่ 1**: เมื่อผู้ใช้กดปุ่ม Load เราต้องสั่งให้โมเดลที่เลือกเริ่มรัน:

```python
elif h == load_id:
    try:
        # เติม: สั่งให้ CM55 รันโมเดลที่เลือก ด้วย edge_ai.select(sel)
        pass
        running = True
        status.text("RUNNING")
        status.color(GREEN)
    except OSError as e:
        status.text("ERROR")            # ข้ามคอร์พลาดได้ ต้องเผื่อไว้
        status.color(RED)
```

- แทน `pass` ด้วย `edge_ai.select(sel)` — `sel` คือ index ที่เลือกใน dropdown
- ต้องอยู่ใน `try` เพราะ `select()` โยน `OSError` ได้ถ้า M55 ไม่ยืนยันการสลับ
- ถ้าลืมเติม: กด Load แล้วสถานะขึ้น RUNNING แต่ไม่มีผลอนุมานจริง (เพราะไม่ได้สั่งโมเดลเลย)

> นี่คือเหตุผลที่เราขึ้น "RUNNING" **หลัง** `select()` สำเร็จเท่านั้น — ถ้า error จะกระโดดไป except ไม่โกหกผู้ใช้ว่ากำลังรัน

---

# ไล่โค้ด (3) — อ่านผล + แถบความมั่นใจ

**ช่องเติมที่ 2 และ 3**: หัวใจของ MVP วันนี้ อ่านผลแล้วเอาคลาสที่ชนะขึ้นจอ:

```python
if running:
    # เติม: อ่านผลอนุมานล่าสุดมาเก็บใน r  ->  r = edge_ai.result()
    r = None
    pass
    if r and r['seq'] != last_seq:      # มีผลใหม่จริงไหม (seq เปลี่ยน)
        last_seq = r['seq']
        # เติม: แสดงคลาสที่ชนะ ด้วย verdict.text(r['label'] or '-')
        pass
        conf.text("conf: %.0f %%" % (r['conf'] * 100))
        top = r['top']
        for i, (lb, br) in enumerate(rows):
            if i < len(r['scores']):
                br.value(int(r['scores'][i] * 100))     # แถบต่อคลาส
                br.color(GREEN if i == top else DIM)     # คลาสที่ชนะสีเขียว
```

- ช่องที่ 2: แทน `pass` ด้วย `r = edge_ai.result()` (ลบ `r = None` ทิ้ง หรือปล่อยไว้ก็ได้ เพราะจะถูกทับ)
- ช่องที่ 3: แทน `pass` ด้วย `verdict.text(r['label'] or '-')`
- เช็ก `seq` ก่อนเสมอ จะได้วาดจอเฉพาะตอนมีผลใหม่ ไม่รัดจอทุกรอบ

> `r['scores']` คือคะแนน **ทุกคลาส** เราวนเอาไปทำแถบ ส่วนคลาสที่ `i == top` (ชนะ) ระบายเขียว — ผู้ใช้เห็นทั้งคำตอบและ "ความสูสี" ของคลาสอื่น

---

# ไล่โค้ด (4) — หยุดให้เรียบร้อย

**ช่องเติมที่ 4**: ปุ่ม Stop และการเก็บกวาดตอนออก:

```python
elif h == stop_id:
    # เติม: สั่งหยุดโมเดลด้วย edge_ai.stop()
    pass
    running = False
    status.text("STOPPED")
    status.color(RED)
...
finally:
    edge_ai.stop()      # ให้ไว้แล้ว: ออกยังไงก็หยุดเครื่องยนต์เสมอ
```

- แทน `pass` ด้วย `edge_ai.stop()` — คู่กับ `select()` เมื่อ Load
- บล็อก `finally` ให้ไว้แล้ว: ไม่ว่าจะออกด้วยปุ่ม back หรือ error โมเดลจะถูกหยุดเสมอ

> นิสัย embedded: **ออกจากงานยังไง ทิ้งเครื่องไว้ให้เรียบร้อยแบบนั้น** อย่าปล่อยเครื่องยนต์รันค้างหลังโปรแกรมจบ นี่คือหลักเดียวกับที่คอร์สเกมสอน "คืนฮาร์ดแวร์สู่สถานะที่รู้แน่"

---

# ลงมือทำ — เติมช่องว่างทั้ง 4 จุด

เปิด [`s01_first_inference.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l03-first-inference-lab/practice/s01_first_inference.py) ในไฟล์มี `pass` วางไว้ **4 จุด** ตรงที่ต้องเติมคำสั่งจริงของ `edge_ai`:

| # | จุด | เติมด้วย | ถ้าลืม |
|---|---|---|---|
| 1 | ปุ่ม Load | `edge_ai.select(sel)` | RUNNING แต่ไม่มีผล |
| 2 | ในลูป | `r = edge_ai.result()` | จอไม่ขึ้นคลาสเลย |
| 3 | มีผลใหม่ | `verdict.text(r['label'] or '-')` | แถบขยับ แต่ตัวเลขใหญ่ไม่เปลี่ยน |
| 4 | ปุ่ม Stop | `edge_ai.stop()` | กด Stop แล้วโมเดลยังรันอยู่ |

ขั้นตอน:

1. ไล่หา `# เติม:` ทีละจุด แล้วแทน `pass` ด้วยคำสั่งตามคำใบ้
2. กด **Run** (Emulator) หรือ **Program to Device** (บอร์ด)
3. เลือกโมเดล กด Load ทำท่า/ส่งเสียง ดูคลาสที่ชนะ ถ้ายังไม่ขึ้น กลับมาเช็ก indent กับชื่อคำสั่ง

> สี่ช่องนี้คือสี่คำสั่งหลักของ `edge_ai` เป๊ะ — เติมครบเมื่อไร คุณรันเมนู 6 โมเดลได้ครบวงจร

---

# แหล่งเรียนรู้เพิ่มเติม

อยากต่อยอดที่บ้าน ลองตามลิงก์เหล่านี้ คัดมาจากช่อง/แหล่งที่เชื่อถือได้

**วิดีโอ (เปิดในเบราว์เซอร์ ไม่ได้ฝังในสไลด์):**

- เข้าใจ neural network แบบเห็นภาพทีละชั้น — ช่อง 3Blue1Brown: https://www.youtube.com/@3blue1brown
- Neural networks อธิบายทีละขั้นแบบเข้าใจง่าย — ช่อง StatQuest: https://www.youtube.com/@statquest
- On-device machine learning ด้วย LiteRT / TensorFlow Lite — ช่อง TensorFlow: https://www.youtube.com/@TensorFlow

**ภาพ / เอกสารอ้างอิง:**

- บทความ Edge computing (ภาพรวม + แผนภาพ) — https://en.wikipedia.org/wiki/Edge_computing (ที่มา: Wikipedia, CC BY-SA 4.0)
- เอกสารทางการ on-device inference — https://ai.google.dev/edge/litert (ที่มา: Google AI Edge, official docs)
- คลังภาพ edge computing (สาธารณะ/ครีเอทีฟคอมมอนส์) — https://commons.wikimedia.org/wiki/Category:Edge_computing (ที่มา: Wikimedia Commons, CC/public-domain)

> วิดีโอ/ภาพภายนอกเป็นของเจ้าของต้นฉบับ ใช้เพื่อการศึกษา อ้างอิงลิงก์ต้นทาง

---

# ชัยชนะที่เห็นได้ + MVP ของชุดบทเรียนนี้

<div style="text-align:center;margin:14px 0">
<div style="display:inline-block;background:#e8f5e9;border:2px solid #2e7d32;border-radius:22px;padding:10px 22px;color:#2e7d32;font-weight:700;font-size:1.05em">
ชัยชนะที่เห็นได้ของชุดบทเรียนนี้ · เมนู 6 โมเดลรู้จำท่าทาง/เสียงของคุณบนจอ พร้อมคลาสที่ชนะและความมั่นใจ
</div>
</div>

**MVP ของบทเรียน 1.1–1.3 (เกณฑ์ผ่านของชุดบทเรียน):** คุณรันเมนู `edge_ai` ได้ แล้ว **อ่านผลสด** ออก — คลาสที่ชนะ (`label`) + ความมั่นใจ (`conf`) เปลี่ยนตามท่าทาง/เสียงจริง

- ทำบน **Emulator** หรือ **บอร์ดจริง** ก็ได้ (โค้ดชุดเดียวกัน)
- อธิบายได้ว่าโค้ดเรียก `models` / `select` / `result` / `stop` ตรงไหน ทำอะไร

> "อ่านผลออก" ไม่ใช่แค่ "เห็นตัวหนังสือขยับ" — คุณต้องบอกได้ว่า `conf` 92% หมายความว่าอะไร และทำไมบางท่าโมเดลถึง "ยังไม่ชัวร์"

---

# บันไดช่วยเหลือ — ใบ้ → เริ่มจากโครง → เฉลย → ฉบับเต็ม

ถ้าติด ให้ไต่บันไดนี้ทีละขั้น อย่าเพิ่งกระโดดไปดูเฉลย เพราะของจะเข้าหัวตอนที่คุณพยายามเองก่อน:

- **ใบ้** — คำใบ้อยู่ในคอมเมนต์ `# เติม:` ทั้ง 4 จุดในไฟล์ฝึก + ตารางหน้าที่แล้ว บอกว่าแต่ละช่องเติมอะไร
- **เริ่มจากโครง** — [`s01_first_inference.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l03-first-inference-lab/practice/s01_first_inference.py) มีโครงครบทั้งไฟล์แล้ว เหลือแค่ 4 บรรทัดให้เติม
- **เฉลย** — [`s01_first_inference.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l03-first-inference-lab/solution/s01_first_inference.py) เติมครบพร้อมคอมเมนต์อธิบายทุกช่อง (อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์เอง)
- **ฉบับเต็ม** — [`s01_first_inference_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l03-first-inference-lab/examples/s01_first_inference_full.py) ฉบับขัดเรียบร้อย เพิ่ม latency + เกณฑ์ CONF_FLOOR แยก "มั่นใจ/ยังไม่ชัวร์" ด้วยสี

> ลองเขียนเองให้สุดก่อนนะ ถ้าติดจริงๆ ค่อยเปิดเฉลยดูทีละช่อง แล้วกลับมาพิมพ์เอง — เดี๋ยวเราค่อย ๆ แกะไปด้วยกัน

---

# เชื่อมโยงรากฐาน — วันนี้เราแตะอะไรไปบ้าง

การรันโมเดลตัวแรกซ่อนแนวคิด Edge AI หลายชั้นที่จะใช้ไปตลอดคอร์ส:

**ฝั่ง Edge AI / ระบบ**
- **Inference on device** — โมเดลอนุมานบน NPU ตรงหน้า ไม่ผ่านคลาวด์
- **Model registry** — เฟิร์มแวร์เก็บทะเบียนโมเดลไว้ เราถามด้วย `models()` ไม่ hard-code
- **Verdict = ความน่าจะเป็น** — `conf` + `scores` + `CONF_FLOOR` บอกว่าโมเดล "มั่นใจแค่ไหน" ไม่ใช่คำตอบเด็ดขาด
- **Cross-core pull** — โค้ด Python (M33) ดึงผลจากคอร์ AI (M55) แบบปลอดภัย

**ฝั่ง MicroPython / โครงโปรแกรม**
- **โครงร่วม** — import → สร้างครั้งเดียว → ลูป → `ui.poll` (จะแกะละเอียดใน บทเรียน 1.4–1.5)
- **สร้าง widget ครั้งเดียว** — ประหยัดหน่วยความจำ จอไม่กระพริบ
- **เก็บกวาดตอนจบ** — `finally: edge_ai.stop()` คืนเครื่องสู่สถานะที่รู้แน่

> ทั้งหมดนี้ยืนบนคำสั่งแค่ 4 ตัว — พลังของ MicroPython-first คือคุณได้ผลจริงตั้งแต่ชุดบทเรียนแรก โดยยังไม่ต้องแตะ C หรือ toolchain

---

# ใช้จริงที่ไหน — Edge AI inference ในโลกจริง

สี่โมเดลที่เราลองวันนี้ ไม่มีตัวไหนเป็นของสมมติ ทุกตัวมีสินค้าจริงในโลกที่ทำงานด้วยหลักการเดียวกัน:

<div style="text-align:center;margin:6px 0">
<svg width="880" height="220" viewBox="0 0 880 220" font-family="DejaVu Sans, sans-serif">
  <rect x="12" y="10" width="420" height="96" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="28" y="34" font-size="13" font-weight="700" fill="#1565c0">Motion (IMU) — นาฬิกา/แท็ก</text>
  <text x="28" y="56" font-size="11" fill="#555">ตรวจการล้ม · นับก้าว · รู้ท่าทางการออกกำลัง</text>
  <text x="28" y="76" font-size="11" fill="#555">ต้องตอบทันที + ทำงานตลอด → รันบนอุปกรณ์</text>
  <text x="28" y="96" font-size="11" fill="#888">โมเดลเดียวกับ "shaking/circle/idle" วันนี้</text>
  <rect x="448" y="10" width="420" height="96" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="464" y="34" font-size="13" font-weight="700" fill="#2e7d32">เสียง (MIC) — บ้าน/โรงงาน</text>
  <text x="464" y="56" font-size="11" fill="#555">ตรวจเสียงเด็กร้อง · เสียงไอ · เสียงเตือน/ไซเรน</text>
  <text x="464" y="76" font-size="11" fill="#555">เสียงไม่ต้องออกจากเครื่อง → ความเป็นส่วนตัว</text>
  <text x="464" y="96" font-size="11" fill="#888">โมเดล Baby Cry/Cough/Alarm/Siren วันนี้</text>
  <rect x="12" y="118" width="420" height="92" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="28" y="142" font-size="13" font-weight="700" fill="#e65100">เรดาร์ (RADAR) — สวิตช์/ป้าย</text>
  <text x="28" y="164" font-size="11" fill="#555">ตรวจการมี-ไม่มีคน · ท่าทางกวักมือ (ไม่ใช้กล้อง)</text>
  <text x="28" y="184" font-size="11" fill="#555">ทำงานในที่มืด/ผ่านวัสดุได้ → เปิดไฟอัตโนมัติ</text>
  <text x="28" y="202" font-size="11" fill="#888">โมเดล Push Detection วันนี้</text>
  <rect x="448" y="118" width="420" height="92" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="464" y="142" font-size="13" font-weight="700" fill="#6a1b9a">ร่วมกัน — ความมั่นใจ + action</text>
  <text x="464" y="164" font-size="11" fill="#555">ทุกงานใช้ conf/scores ตัดสินว่าจะเชื่อไหม</text>
  <text x="464" y="184" font-size="11" fill="#555">แล้วสั่งการต่อ (แจ้งเตือน · เปิดไฟ · บันทึก)</text>
  <text x="464" y="202" font-size="11" fill="#888">คือ โมดูล 6 (Apps, โมดูล 6) ของเรา</text>
</svg>
</div>

> เห็นไหมว่า 6 โมเดลที่เล่นวันนี้ ไม่ได้เล่นเปล่า — มันคือแก่นของสินค้า Edge AI จริงที่ขายอยู่ในตลาด เราแค่กำลังเริ่มจากปลายทางเพื่อจะย้อนไปสร้างเองได้

---

# งานทำเอง + สรุปบทเรียน

**งานทำเอง (ท้ายบทเรียน):**

1. เติม [`s01_first_inference.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l03-first-inference-lab/practice/s01_first_inference.py) ให้ครบทั้ง 4 ช่อง รันได้จริง (Emulator หรือบอร์ด)
2. ลองสลับอย่างน้อย **3 โมเดล** (เช่น Motion → Baby Cry → Push) แล้วจดว่าแต่ละตัวต้องทำอะไรถึงจะได้คลาสที่ชนะ
3. หาท่า/เสียงที่ทำให้โมเดล **"ยังไม่ชัวร์"** (conf ต่ำกว่า 50%) แล้วอธิบายว่าทำไม

ใบ้ข้อ 3 — ท่าที่ก้ำกึ่งระหว่างสองคลาส หรือเสียงที่คล้ายหลายคลาส จะทำให้คะแนนกระจาย ไม่มีคลาสไหนชนะขาด

**วันนี้เราได้:** เข้าใจว่า Edge AI คืออะไร · เห็นวงจร 5 ขั้นและสเปกตรัมหลายเป้าหมาย · รันเมนู 6 โมเดลด้วย `models`/`select`/`result`/`stop` · อ่านคลาสที่ชนะ + ความมั่นใจสดๆ

> ชุดบทเรียนถัดไป (บทเรียน 1.4–1.5) เราจะ **แกะแอปเซนเซอร์** ทีละส่วน — จับโครงร่วม "import → สร้างครั้งเดียว → ลูป → ui.poll" ให้ขาด แล้วลอง remix เอง เจอกันครับ
