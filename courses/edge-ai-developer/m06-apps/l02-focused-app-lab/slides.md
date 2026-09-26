---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 6.2 — ลงมือทำ: แอปโฟกัสของเราเอง"
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

# บทเรียน 6.2 — ลงมือทำ: แอปโฟกัสของเราเอง

## Apps I: 6 โมเดล กับ edge_ai API · สร้าง "แอปโฟกัสโมเดลเดียว" ของคุณเอง

**โมดูล 6 — แอป Edge AI**

> ต่อจากบทเรียน 6.1 — หกโมเดลกับ edge_ai API: แอปที่โฟกัสโมเดลเดียว

---

# ลงมือ (1) — รันบน BENTO Emulator

ไม่มีบอร์ดก็เริ่มได้ ซ้อมโครงแอปบน Emulator ได้เลย (โมเดลเสียงบน Emulator เป็นค่าจำลอง ลูกบิด POTEN ดันคลาสเหตุการณ์ขึ้นได้แต่ยังไม่ชนะ `unlabelled` ตัวนับจึงยังไม่ขยับ):

1. เปิด **ide.tesaiot.dev** (BENTO Emulator) ในเบราว์เซอร์
2. เปิด [`16_edge_ai_sound_events.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l01-focused-apps/examples/16_edge_ai_sound_events.py) กด **Run** ดูเมนูเสียงสามโมเดลก่อน (ของจริงที่จะแกะ)
3. จากนั้นเปิด [`s15_apps.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l02-focused-app-lab/practice/s15_apps.py) — นี่คือแอปโฟกัส Cough ที่เราจะเติม
4. เติมสี่ช่องให้ครบ กด **Run** หมุนลูกบิด POTEN แล้วดูแถบสองคลาสขยับ ถ้าอยากเห็นตัวนับทำงานบน Emulator ให้เล็งโมเดล Motion ชั่วคราว (`TARGET_KEYWORDS = ("motion",)`, `TARGET_CLASS = "shaking"`) แล้วกดปุ่ม Shake
5. ตัวนับกับเสียงไอจริงต้องลองบนบอร์ด ลองเสียงอื่นที่ไม่ใช่ไอ ดูว่าตัวนับ **ไม่ขยับ** (เพราะ conf ไม่ถึงเกณฑ์ หรือคลาสไม่ตรง)

> Emulator ใช้เซนเซอร์เสียง **จำลอง** แต่ API เหมือนบอร์ดจริงทุกบรรทัด — ซ้อมโครงแอปที่บ้านได้ แล้วมายืนยันด้วยไมค์จริงบนบอร์ด

---

# หน้าจอ BENTO Edge AI Emulator

![หน้า Edge AI บน BENTO Emulator: dropdown เลือกโมเดล Motion Detection ปุ่ม Load และ Stop คลาสที่ชนะ idle เวลาอนุมาน และแถบความมั่นใจของ idle circle shaking w:680](../../assets/img/edge_ai_page.png)

จอ emulator ที่รันได้จริงในเบราว์เซอร์ — เปิด **ide.tesaiot.dev** แล้วกด Run ได้เลย ไม่ต้องมีบอร์ด API ทุกบรรทัดเหมือนบอร์ดจริง จึงซ้อมแอปโฟกัสที่บ้านก่อน แล้วมายืนยันด้วยไมค์จริงบนบอร์ด

---

# ลงมือ (2) — รันบนบอร์ด BENTO จริง

บนบอร์ดจริงใช้ไมค์จริงบนบอร์ด เสียงจริง NPU จริง:

1. เสียบบอร์ดเข้าคอมด้วยสาย USB
2. เปิด [`s15_apps.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l02-focused-app-lab/practice/s15_apps.py) ใน **BENTO IDE** กด **Program to Device**
3. บนจอขึ้นแอปโฟกัส Cough: การ์ด verdict + การ์ดตัวนับ + แถบสองคลาส
4. **ไอใกล้ไมค์** (หรือเปิดคลิปเสียงไอ) หลายครั้ง ดูคลาส `cough` ชนะ + ตัวนับเพิ่ม
5. ถ้าผลค้างนิ่ง (seq ไม่ขยับ) ให้ **รีบูตบอร์ด** — ถึงขีด eval ของ Ready-Model แล้ว

> จุดที่ควรสังเกต: ตัวนับจะเพิ่ม **หนึ่งต่อการไอหนึ่งครั้ง** ไม่ใช่พรวดหลายที เพราะโค้ดนับเฉพาะขอบขาขึ้น ถ้าเห็นมันพรวด แปลว่าเงื่อนไข `not was_target` หายไป

---

# โครงของไฟล์ s15_apps.py

ทั้งไฟล์อ่านเป็นประโยคเดียว: **"เล็งโมเดล cough → สร้างการ์ด → เริ่มรัน → วนอ่านผล เอาคลาสขึ้นจอ นับเมื่อเจอ → ออกก็หยุด"**

<div style="text-align:center;margin:6px 0">
<svg width="920" height="215" viewBox="0 0 920 215" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arS1" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g font-size="13" text-anchor="middle">
    <rect x="14" y="24" width="180" height="54" rx="10" fill="#cfd8dc" stroke="#607d8b" stroke-width="2"/>
    <text x="104" y="47" font-weight="700" fill="#455a64">เล็งโมเดล</text>
    <text x="104" y="66" font-size="11" fill="#999">find_model :53</text>
    <rect x="234" y="24" width="180" height="54" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="324" y="47" font-weight="700" fill="#1565c0">สร้างการ์ด</text>
    <text x="324" y="66" font-size="11" fill="#999">Panel+Seg7+Bar :62</text>
    <rect x="454" y="24" width="180" height="54" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
    <text x="544" y="47" font-weight="700" fill="#6a1b9a">เริ่มรัน</text>
    <text x="544" y="66" font-size="11" fill="#999">select :88 (เติม)</text>
    <rect x="674" y="24" width="230" height="54" rx="10" fill="#eceff1" stroke="#607d8b" stroke-width="2"/>
    <text x="789" y="47" font-weight="700" fill="#455a64">ออก → finally stop</text>
    <text x="789" y="66" font-size="11" fill="#999">:125</text>
    <rect x="234" y="140" width="200" height="58" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="334" y="164" font-weight="700" fill="#e65100">อ่านผล + verdict</text>
    <text x="334" y="183" font-size="11" fill="#999">result/verdict :96 (เติม)</text>
    <rect x="474" y="140" width="200" height="58" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="574" y="160" font-weight="700" fill="#2e7d32">นับเมื่อเจอ</text>
    <text x="574" y="178" font-size="11" fill="#999">is_target :112 (เติม)</text>
    <text x="574" y="192" font-size="10" fill="#999">+ CONF_FLOOR</text>
  </g>
  <line x1="194" y1="51" x2="232" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS1)"/>
  <line x1="414" y1="51" x2="452" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS1)"/>
  <line x1="634" y1="51" x2="672" y2="51" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS1)"/>
  <path d="M544,78 C544,118 334,110 334,138" fill="none" stroke="#2e7d32" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#arS1)"/>
  <text x="470" y="112" font-size="12" fill="#2e7d32">วนอ่านผลทุก 150 ms</text>
  <line x1="434" y1="169" x2="472" y2="169" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arS1)"/>
  <text x="470" y="210" font-size="11" fill="#888" text-anchor="middle">แถวล่าง = สิ่งที่เกิดในลูปทุกครั้งที่มีผลใหม่</text>
</svg>
</div>

> เลขบรรทัด (`:88`, `:96`, `:112`) ชี้จุดที่คุณต้องเติมในไฟล์ฝึก — สามจุดหลัก แต่มีสี่ช่อง `# เติม:` (result กับ verdict อยู่ใกล้กัน)

---

# ไล่โค้ด (1) — เล็งโมเดลด้วยตัวแปรบนหัวไฟล์

ส่วนบนสุดของไฟล์คือ "แผงตั้งค่า" ที่ทำให้รีทาร์เก็ตง่าย เปลี่ยนที่นี่ที่เดียวก็ได้แอปโมเดลอื่น:

```python
TARGET_KEYWORDS = ("cough",)   # คีย์เวิร์ดหาชื่อโมเดล
TARGET_CLASS    = "cough"       # ชื่อคลาสที่ถือว่า "ตรวจเจอ"
TARGET_SENSOR   = edge_ai.SENSOR_MIC

model = find_model(TARGET_KEYWORDS, TARGET_SENSOR)
labels = model['labels']       # เช่น ['unlabelled', 'cough']
```

- `TARGET_KEYWORDS` บอก `find_model()` ว่าจะหาโมเดลชื่ออะไร · `TARGET_CLASS` บอกว่าคลาสไหนคือ "เจอ"
- แยกสองค่านี้ออกจากกันเพราะ **ชื่อโมเดล กับ ชื่อคลาส ไม่เหมือนกัน** เช่น โมเดลชื่อ "Siren Detection" แต่คลาสคือ `sirens`
- บรรทัดพวกนี้ให้ไว้แล้วในไฟล์ฝึก — งานของคุณคือสี่ช่องด้านล่าง

> ออกแบบให้ "จุดที่ต้องแก้ตอนรีทาร์เก็ต" รวมอยู่บนหัวไฟล์ทั้งหมด เป็นนิสัยที่ดีมาก คนอ่านโค้ดต่อจะรู้ทันทีว่าปรับอะไรได้ตรงไหน โดยไม่ต้องไล่ทั้งไฟล์

---

# ไล่โค้ด (2) — ช่องเติมที่ 1: เริ่มรัน

**ช่องเติมที่ 1**: ก่อนเข้าลูป สั่งให้โมเดลเป้าหมายเริ่มรัน (ครั้งเดียว ไม่มีปุ่ม Load):

```python
try:
    # เติม: เริ่มรันโมเดลเป้าหมายตัวเดียว ด้วย edge_ai.select(model['index'])
    pass
    lcd.console('<span class=ok> เริ่มฟัง %s…</span>' % model['name'])

    while True:
        ...
```

- แทน `pass` ด้วย `edge_ai.select(model['index'])` — ใช้ `model['index']` ที่ `find_model()` หามาให้
- ต่างจาก บทเรียน 1.1–1.3: ที่นี่ `select()` อยู่ **ก่อนลูป** ไม่ใช่ในปุ่ม เพราะแอปโฟกัสรู้อยู่แล้วว่าจะรันอะไร
- ทั้งก้อนอยู่ใน `try` เพราะ `select()` โยน `OSError` ได้ ถ้า M55 ไม่ยืนยันการสลับ

> ถ้าลืมเติมช่องนี้: แอปเปิดได้ การ์ดขึ้นครบ แต่ `result()` จะคืน `None` ตลอด เพราะไม่มีโมเดลไหนถูกสั่งให้รันเลย — ตัวนับจะไม่มีวันขยับ

---

# ไล่โค้ด (3) — ช่องเติมที่ 2+3: อ่านผล + คลาสที่ชนะ

**ช่องเติมที่ 2 และ 3**: หัวใจของลูป อ่านผลแล้วเอาคลาสที่ชนะขึ้นจอ:

```python
# เติม: อ่านผลอนุมานล่าสุดมาเก็บใน r  ->  r = edge_ai.result()
r = None
pass
if r and r['seq'] != last_seq:
    last_seq = r['seq']
    # เติม: แสดงคลาสที่ชนะบนจอ ด้วย verdict.text(r['label'] or '-')
    pass
    conf.text("conf: %.0f %%" % (r['conf'] * 100))
    lat.text("latency: %.1f ms" % r['latency_ms'])
```

- ช่อง 2: แทน `pass` ด้วย `r = edge_ai.result()` (ลบ `r = None` ทิ้ง หรือปล่อยไว้ก็ได้ เพราะจะถูกทับ)
- ช่อง 3: แทน `pass` ด้วย `verdict.text(r['label'] or '-')`
- เช็ก `seq` ก่อนเสมอ วาดจอเฉพาะตอนมีผลใหม่ — เหมือน บทเรียน 1.1–1.3 เป๊ะ

> โครงส่วนนี้เหมือน บทเรียน 1.1–1.3 มาก จงใจให้เหมือน เพราะเราต้องการให้คุณ **จำ pattern อ่านผลให้ขึ้นใจ** ก่อนจะต่อ action ที่เป็นของใหม่จริงในช่องถัดไป

---

# ไล่โค้ด (4) — ช่องเติมที่ 4: เงื่อนไขตรวจเจอ

**ช่องเติมที่ 4**: ของใหม่ของชุดบทเรียนนี้ ต่อ verdict เข้ากับ action (การนับ):

```python
# เติม: แทน False ด้วยเงื่อนไขตรวจเจอจริง
#       r['label'] == TARGET_CLASS and r['conf'] >= edge_ai.CONF_FLOOR
is_target = False
if is_target and not was_target:
    hits += 1
    hits_lbl.text(str(hits))
    lcd.console('<span class=ok> เจอ %s ครั้งที่ %d</span>' % (TARGET_CLASS, hits))
was_target = is_target
```

- แทน `False` ด้วย `r['label'] == TARGET_CLASS and r['conf'] >= edge_ai.CONF_FLOOR`
- สองเงื่อนไขต้องเป็นจริง**พร้อมกัน**: คลาสตรงเป้า และมั่นใจถึงเกณฑ์
- `not was_target` คือกุญแจของ "ขอบขาขึ้น" — นับหนึ่งต่อการเจอหนึ่งครั้ง

> ลองผิดดูก็ได้เพื่อเรียนรู้: ถ้าเติมแค่ `r['label'] == TARGET_CLASS` (ตัด conf ทิ้ง) แล้วส่งเสียงมั่วๆ คุณจะเห็นตัวนับเด้งทั้งที่ไม่ได้ไอ — นั่นคือ false positive ที่ `CONF_FLOOR` มีไว้กัน

---

# ลงมือทำ — เติมช่องว่างทั้ง 4 จุด

เปิด [`s15_apps.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l02-focused-app-lab/practice/s15_apps.py) มี `# เติม:` วางไว้ **4 จุด** (สามจุดหลักของ edge_ai + หนึ่ง action):

| # | จุด | เติมด้วย | ถ้าลืม |
|---|---|---|---|
| 1 | ก่อนลูป | `edge_ai.select(model['index'])` | แอปเปิดได้ แต่ result เป็น None ตลอด |
| 2 | ในลูป | `r = edge_ai.result()` | จอไม่ขึ้นคลาสเลย |
| 3 | มีผลใหม่ | `verdict.text(r['label'] or '-')` | แถบขยับ แต่ตัวใหญ่ไม่เปลี่ยน |
| 4 | ตรวจเจอ | `r['label']==TARGET_CLASS and r['conf']>=edge_ai.CONF_FLOOR` | ตัวนับไม่ขยับ (หรือเด้งมั่ว) |

ขั้นตอน:

1. ไล่หา `# เติม:` ทีละจุด แทน `pass`/`False` ตามคำใบ้
2. กด **Run** (Emulator) หรือ **Program to Device** (บอร์ด)
3. ทำเสียงไอหลายครั้ง ดูคลาส `cough` ชนะ + ตัวนับเพิ่ม ถ้าตัวนับเด้งมั่ว กลับไปเช็กเงื่อนไข conf ในช่อง 4

> สามช่องแรกคือ pattern เดิมจาก บทเรียน 1.1–1.3 (select/result/verdict) — ช่องที่ 4 คือก้าวใหม่จริงของคุณ: การเปลี่ยน "ผล" ให้กลายเป็น "การกระทำ"

---

# รีทาร์เก็ตเป็น cough / alarm / siren

MVP วันนี้ต้องมีแอป **อย่างน้อยสองตัว** ข่าวดีคือรีทาร์เก็ตใช้เวลาไม่ถึงนาที เปลี่ยนแค่สองบรรทัดบนหัวไฟล์แล้วเซฟเป็นไฟล์ใหม่:

```python
# s15_alarm_app.py — แค่เปลี่ยนสองบรรทัดนี้
TARGET_KEYWORDS = ("alarm",)
TARGET_CLASS    = "alarm"

# s15_siren_app.py — โมเดลชื่อ Siren แต่คลาสสะกด sirens (มี s)
TARGET_KEYWORDS = ("siren",)
TARGET_CLASS    = "sirens"
```

- โครงทั้งไฟล์ **ไม่ต้องแตะ** — `find_model()` หาโมเดลใหม่ให้เอง, แถบคลาสปรับตาม `labels` ที่ได้มา
- ระวังจุดเดียว: `TARGET_CLASS` ต้องสะกดตรงกับ label จริง (Siren → `sirens` มี s) เช็กด้วย `edge_ai.models()` ใน REPL ก่อน
- เซฟเป็น `s15_cough_app.py` / `s15_alarm_app.py` / `s15_siren_app.py` — นี่คือ "แอปต่อโมเดล" ที่หลักสูตรตั้งเป้าไว้

> นี่คือผลตอบแทนของการออกแบบให้ตัวแปรอยู่บนหัวไฟล์: โมเดลหนึ่งแม่แบบ กลายเป็นสามแอปได้ในไม่กี่นาที — คุณเพิ่งสร้าง "ตระกูลแอป" ของตัวเอง

---

# แหล่งเรียนรู้เพิ่มเติม

อยากเข้าใจ argmax / softmax / edge AI ให้ลึกขึ้น ลองดูจากช่องที่อธิบายเห็นภาพ:

**วิดีโอ (ภาษาอังกฤษ อธิบายเข้าใจง่าย)**
- Softmax และ argmax คลาสไหนชนะ — ช่อง StatQuest with Josh Starmer: https://www.youtube.com/@statquest
- What is Edge AI / TinyML บนอุปกรณ์เล็ก — ช่อง Edge Impulse: https://www.youtube.com/@EdgeImpulse
- Neural networks เข้าใจแบบเห็นภาพ — ช่อง 3Blue1Brown: https://www.youtube.com/@3blue1brown

**ภาพ / เอกสารอ้างอิง**
- ฟังก์ชัน Softmax (ที่มาของคะแนนต่อคลาส) — https://en.wikipedia.org/wiki/Softmax_function (ที่มา: Wikipedia, CC BY-SA)
- Arm Ethos-U55 NPU ตัวเร่งการอนุมานบนบอร์ด — https://www.arm.com/products/silicon-ip-cpu/ethos/ethos-u55 (ที่มา: Arm Ltd. official docs)

> วิดีโอ/ภาพภายนอกเป็นของเจ้าของต้นฉบับ ใช้เพื่อการศึกษา อ้างอิงลิงก์ต้นทาง

---

# ชัยชนะที่เห็นได้ + MVP ของชุดบทเรียนนี้

<div style="text-align:center;margin:14px 0">
<div style="display:inline-block;background:#e8f5e9;border:2px solid #2e7d32;border-radius:22px;padding:10px 22px;color:#2e7d32;font-weight:700;font-size:1.05em">
ชัยชนะที่เห็นได้ของชุดบทเรียนนี้ · แอปโฟกัสที่คุณสร้างเอง รันโมเดลเดียว แล้ว "นับ" ขึ้นจริงเมื่อเจอเสียงเป้าหมาย
</div>
</div>

**MVP ของบทเรียน 6.1–6.2 (เกณฑ์ผ่านของชุดบทเรียน):** คุณสร้าง **แอปโฟกัสต่อโมเดล** ที่ UI สะอาด — เล็งโมเดลด้วย `find_model()`, โชว์ verdict + แถบทุกคลาส + latency, และมี action หนึ่งอย่าง (ตัวนับ) ที่ทำงานจริงเมื่อคลาสเป้าหมายข้าม `CONF_FLOOR`

- ทำบน **Emulator** หรือ **บอร์ดจริง** ก็ได้ (โค้ดชุดเดียวกัน)
- รีทาร์เก็ตได้อย่างน้อย **สองโมเดล** (เช่น Cough + Alarm) โดยแก้แค่ตัวแปรบนหัวไฟล์
- อธิบายได้ว่าทำไมต้องเช็ก `CONF_FLOOR` ก่อนนับ และทำไมต้องนับเฉพาะ "ขอบขาขึ้น"

> "แอปที่สร้างเอง" ไม่ใช่แค่ "รันแล้วมีตัวเลข" — คุณต้องบอกได้ว่า action ของคุณเชื่อ verdict ตอนไหน และกันนับเฟ้ออย่างไร นั่นคือหัวใจของ Apps

---

# บันไดช่วยเหลือ — ใบ้ → เริ่มจากโครง → เฉลย → ฉบับเต็ม

ถ้าติด ให้ไต่บันไดนี้ทีละขั้น อย่าเพิ่งกระโดดไปดูเฉลย เพราะของจะเข้าหัวตอนที่คุณพยายามเองก่อน:

- **ใบ้** — คำใบ้อยู่ในคอมเมนต์ `# เติม:` ทั้ง 4 จุดในไฟล์ฝึก + ตารางช่องเติมหน้าที่แล้ว
- **เริ่มจากโครง** — [`s15_apps.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l02-focused-app-lab/practice/s15_apps.py) มีโครงครบทั้งไฟล์ เหลือแค่ 4 จุดให้เติม
- **เฉลย** — [`s15_apps.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l02-focused-app-lab/solution/s15_apps.py) เติมครบพร้อมคอมเมนต์อธิบายทุกช่อง (อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์เอง)
- **ฉบับเต็ม** — [`s15_apps_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l02-focused-app-lab/examples/s15_apps_full.py) ฉบับขัดเรียบร้อย เพิ่มสีตาม `CONF_FLOOR`, debounce เบาๆ (นับเมื่อเจอติดกันสองผล), เวลา "เจอครั้งล่าสุด" และปุ่ม Reset

> ลองเขียนเองให้สุดก่อนนะ ถ้าติดจริงๆ ค่อยเปิดเฉลยดูทีละช่อง แล้วกลับมาพิมพ์เอง — เดี๋ยวเราค่อย ๆ แกะไปด้วยกัน

---

# เชื่อมโยงรากฐาน — วันนี้เราแตะอะไรไปบ้าง

การสร้างแอปโฟกัสตัวแรกดึงทุกอย่างจากชุดบทเรียนก่อนหน้ามารวมกัน แล้วเพิ่ม "การกระทำ" เข้าไป:

**ฝั่ง Edge AI / Apps**
- **แอปต่อโมเดล** — เล็งโมเดลเดียวด้วย `find_model()` แทนเมนู (ต่อจาก บทเรียน 1.1–1.3 และ 1.6–1.7)
- **verdict → action** — เปลี่ยน `label`/`conf` ให้เป็นการกระทำ (การนับ) — เปิด โมดูล 6 (Apps)
- **CONF_FLOOR = ประตูของ action** — ตัดสินใจว่าจะเชื่อผลไหม ก่อนลงมือ
- **ขอบขาขึ้น + debounce** — นับหนึ่งต่อเหตุการณ์ ไม่ใช่ต่อผลอนุมาน

**ฝั่ง MicroPython / โครงโปรแกรม**
- **โครงแอปโฟกัส** — find_model → สร้างครั้งเดียว → select → ลูป → `finally: stop`
- **ตัวแปรตั้งค่าบนหัวไฟล์** — รีทาร์เก็ตทั้งแอปด้วยการแก้จุดเดียว
- **เก็บกวาดตอนจบ** — `finally: edge_ai.stop()` คืนเครื่องสู่สถานะที่รู้แน่ (เหมือนทุกบทเรียน)

> ทั้งหมดนี้ยังยืนบนคำสั่งเดิมแค่ไม่กี่ตัว — สิ่งที่เพิ่มคือ "วิธีคิด" เรื่องการเปลี่ยนผลเป็นการกระทำ ซึ่งจะขยายต่อในสองชุดบทเรียนถัดไป

---

# ใช้จริงที่ไหน — แอป Edge AI ต่อโมเดลในโลกจริง

แอปโฟกัสที่เราสร้างวันนี้ ไม่ใช่ของสมมติ ทุกตัวมีสินค้าจริงที่ทำงานด้วยโครงเดียวกัน: โฟกัสโมเดลเดียว + นับ/เตือนเมื่อเจอ

<div style="text-align:center;margin:6px 0">
<svg width="880" height="210" viewBox="0 0 880 210" font-family="DejaVu Sans, sans-serif">
  <rect x="12" y="10" width="420" height="92" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="28" y="34" font-size="13" font-weight="700" fill="#2e7d32">Cough — เครื่องนับ/คัดกรองสุขภาพ</text>
  <text x="28" y="56" font-size="11" fill="#555">นับความถี่การไอในห้องผู้ป่วย · เฝ้าอาการกลางคืน</text>
  <text x="28" y="76" font-size="11" fill="#555">เสียงไม่ออกจากเครื่อง → ความเป็นส่วนตัว</text>
  <text x="28" y="94" font-size="11" fill="#888">คือแอป s15_cough_app วันนี้ + ตัวนับ</text>
  <rect x="448" y="10" width="420" height="92" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="464" y="34" font-size="13" font-weight="700" fill="#e65100">Alarm — เฝ้าเสียงเตือนในโรงงาน</text>
  <text x="464" y="56" font-size="11" fill="#555">ได้ยินเสียงเตือนเครื่องจักร → log/แจ้งเวร</text>
  <text x="464" y="76" font-size="11" fill="#555">ทำงานในที่เสียงดัง ไม่ต้องพึ่งคน</text>
  <text x="464" y="94" font-size="11" fill="#888">คือแอป s15_alarm_app (รีทาร์เก็ต)</text>
  <rect x="12" y="112" width="420" height="90" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="28" y="136" font-size="13" font-weight="700" fill="#1565c0">Siren — รถฉุกเฉิน/เมืองอัจฉริยะ</text>
  <text x="28" y="158" font-size="11" fill="#555">ได้ยินไซเรน → หรี่เพลง/เตือนคนขับหูตึง</text>
  <text x="28" y="178" font-size="11" fill="#555">รันบนอุปกรณ์ ตอบทันที ไม่พึ่งเน็ต</text>
  <text x="28" y="196" font-size="11" fill="#888">คือแอป s15_siren_app (รีทาร์เก็ต)</text>
  <rect x="448" y="112" width="420" height="90" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="464" y="136" font-size="13" font-weight="700" fill="#6a1b9a">ร่วมกัน — verdict + เกณฑ์ + action</text>
  <text x="464" y="158" font-size="11" fill="#555">ทุกแอปใช้ conf ตัดสินว่าจะเชื่อไหม</text>
  <text x="464" y="178" font-size="11" fill="#555">แล้วทำ action (นับ · log · เตือน)</text>
  <text x="464" y="196" font-size="11" fill="#888">6.3–6.4 ต่อ action แรงขึ้น · 6.5–6.6 ต่อ IoT</text>
</svg>
</div>

> โมเดลเดียวกัน เปลี่ยนคีย์เวิร์ดกลายเป็นสินค้าคนละตัว — นี่คือพลังของ "แอปต่อโมเดล" ที่ออกแบบมาดี แม่แบบหนึ่งอัน ต่อยอดได้ทั้งตระกูล

---

# งานทำเอง + สรุปบทเรียน

**งานทำเอง (ท้ายบทเรียน):**

1. เติม [`s15_apps.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m06-apps/l02-focused-app-lab/practice/s15_apps.py) ให้ครบทั้ง 4 ช่อง รันได้จริง — แอป Cough นับได้ (Emulator หรือบอร์ด)
2. รีทาร์เก็ตเป็น **อย่างน้อยหนึ่งโมเดลอื่น** (Alarm หรือ Siren) เซฟเป็นไฟล์ใหม่ แล้วยืนยันว่าตัวนับทำงาน
3. ทดลอง: ตัด `and r['conf'] >= CONF_FLOOR` ออกชั่วคราว ส่งเสียงมั่วๆ แล้วจดว่าตัวนับเด้งต่างจากเดิมยังไง (แล้วใส่กลับ)

ใบ้ข้อ 3 — เมื่อไม่มีเกณฑ์ conf ทุกครั้งที่คลาสเป้าหมาย "แค่ชนะ" (แม้คะแนนสูสี) ก็จะถูกนับ คุณจะเห็น false positive พุ่งขึ้นทันที นั่นคือเหตุผลที่แอปจริงต้องมีเส้นแบ่ง

**วันนี้เราได้:** แยกเมนูออกจากแอปโฟกัส · เล็งโมเดลด้วย `find_model()` · อ่าน `scores`/`latency_ms` ให้ครบ · ต่อ verdict เข้ากับ action แรก (การนับ) ด้วยเกณฑ์ `CONF_FLOOR` และขอบขาขึ้น · รีทาร์เก็ตเป็นตระกูลแอป cough/alarm/siren

> ชุดบทเรียนถัดไป (บทเรียน 6.3–6.4) เราจะทำให้ action **แรงขึ้น**: จาก "นับ" เป็นจุด RGB / เล่นเสียง / เขียน log พร้อม debounce เต็มรูปแบบและการจัดการ false positive อย่างจริงจัง — เจอกันครับ
