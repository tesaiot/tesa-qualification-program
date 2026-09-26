---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 7.4 — ลงมือทำ: ให้โมเดลใหม่โผล่ใน edge_ai.models()"
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

# บทเรียน 7.4 — ลงมือทำ: ให้โมเดลใหม่โผล่ใน edge_ai.models()

## ต่อเติม Edge AI · เพิ่มโมเดลของเราเองเข้าเฟิร์มแวร์

**โมดูล 7 — ใต้ฝากระโปรงและการต่อเติม**

> ต่อจากบทเรียน 7.3 — เพิ่มโมเดลของเราเอง: สามการแก้ สัญญาสี่ฟังก์ชัน และ Vela

---

# รู้จักไฟล์ s19_extend_model.py

ไฟล์ฝึกวันนี้ไม่ใช่เกม แต่เป็น **เครื่องมือ "สร้าง 3 การแก้ + ยืนยันผล"** — อ่านเป็นประโยคเดียว: "เขียนสเปกโมเดล → พิมพ์ C ROW ที่ต้องวาง → ถามทะเบียนว่าโผล่ยัง → เลือกรันแล้วอ่าน verdict"

<div style="text-align:center;margin:6px 0">
<svg width="920" height="200" viewBox="0 0 920 200" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arF9" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <g font-size="13" text-anchor="middle">
    <rect x="14" y="70" width="180" height="60" rx="10" fill="#cfd8dc" stroke="#607d8b" stroke-width="2"/>
    <text x="104" y="96" font-weight="700" fill="#455a64">SPEC ของโมเดล</text>
    <text x="104" y="116" font-size="11" fill="#999">name/sensor/labels :44</text>
    <rect x="224" y="70" width="180" height="60" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
    <text x="314" y="96" font-weight="700" fill="#e65100">make_row()</text>
    <text x="314" y="116" font-size="11" fill="#999">ประกอบ C ROW :60</text>
    <rect x="434" y="70" width="180" height="60" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
    <text x="524" y="96" font-weight="700" fill="#1565c0">scan_registry()</text>
    <text x="524" y="116" font-size="11" fill="#999">count()+models() :129</text>
    <rect x="644" y="70" width="180" height="60" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
    <text x="734" y="96" font-weight="700" fill="#2e7d32">run_mine()</text>
    <text x="734" y="116" font-size="11" fill="#999">select+result :156</text>
  </g>
  <line x1="194" y1="100" x2="222" y2="100" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arF9)"/>
  <line x1="404" y1="100" x2="432" y2="100" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arF9)"/>
  <line x1="614" y1="100" x2="642" y2="100" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arF9)"/>
  <text x="460" y="30" font-size="12" font-weight="700" fill="#455a64" text-anchor="middle">สเปก (Python)  ──▶  C ROW ที่วางในเฟิร์มแวร์  ──▶  ยืนยันบนบอร์ดจริง</text>
  <text x="460" y="176" font-size="11" fill="#888" text-anchor="middle">ตัวเลขบรรทัด (:44 :60 :129 :156) = จุดที่ต้องเติมในไฟล์ฝึก</text>
</svg>
</div>

> ไฟล์นี้ "ข้ามฝั่ง": ครึ่งบนเป็นตัวช่วยสร้างโค้ด C (สิ่งที่คุณจะไปวางในเฟิร์มแวร์) ครึ่งล่างเป็นตัวตรวจ MicroPython (ถามบอร์ดว่าโมเดลโผล่จริงไหม) — สองครึ่งคือทั้งงานของสาย Researcher

---

# ไล่โค้ด (1) — SPEC ของโมเดล

**ช่องเติมที่ 1**: เขียน "ใจความ" ของโมเดลก่อน — นี่คือ field เดียวกับที่จะไปอยู่ใน C ROW:

```python
NAME_UI = "Fall Detection"
PREFIX  = "FALL"
SPEC = {
    "name":   NAME_UI,
    # เติม: ใส่เซนเซอร์ + คลาสของโมเดลนี้
    "sensor": None,            # เติม: edge_ai.SENSOR_IMU
    "labels": [],             # เติม: ["normal", "fall"]
    "period_ms": 200,
}
```

- `sensor` ใช้ค่าคงที่จากเฟิร์มแวร์: `edge_ai.SENSOR_IMU` (=0) / `SENSOR_RADAR` (=1) / `SENSOR_MIC` (=2)
- Fall ใช้ IMU → เลือก `SENSOR_IMU` แปลว่ายืม `feed_imu` เดิม ไม่ต้องเขียน feed ใหม่
- `labels` = คลาสที่โมเดลตอบได้ ตรงกับ `.class_labels` ใน ROW

> เขียนสเปกที่ Python ก่อนมีข้อดี: เห็นภาพชัด แก้ง่าย แล้วค่อยให้ `make_row()` แปลเป็น C ให้ — ลดโอกาสพิมพ์ ROW ผิดมือ

---

# ไล่โค้ด (2) — make_row() ประกอบ C ROW

**ช่องเติมที่ 2**: ผูก "สัญญา 4 ฟังก์ชัน" เข้ากับ ROW ด้วยคำนำหน้า `AIM_<PREFIX>_`:

```python
def make_row(spec, prefix):
    ...
    init_fn = "AIM_%s_init" % prefix        # AIM_FALL_init
    enq_fn = "AIM_%s_enqueue" % prefix      # AIM_FALL_enqueue
    # เติม: เติมชื่อ dequeue ให้ครบตามแบบ init/enqueue
    deq_fn = None             # เติม: "AIM_%s_dequeue" % prefix
    fin_fn = "AIM_%s_finalize" % prefix     # AIM_FALL_finalize
    return ( ... )            # ประกอบเป็นข้อความ #if / #define FALL_ROW / #endif
```

- ครบสี่ชื่อเมื่อไร `make_row()` จะพ่นข้อความ ROW ที่ก็อปไปวางใน `ai_engine.c` ได้เลย
- ถ้าลืมเติม `deq_fn` → ROW จะมี `.dequeue = None` → C คอมไพล์ไม่ผ่าน (function pointer เป็น NULL)
- ถ้าโมเดลเป็น ready `.a` เปลี่ยน `AIM` เป็น `IMAI` (ฉบับเต็มมีตัวเลือก `STYLE` ให้สลับ)

> สังเกตว่า `make_row()` แค่ประกอบ "สตริง" — มันไม่ได้คอมไพล์ C ให้ หน้าที่มันคือ **ลดข้อผิดพลาดตอนพิมพ์ ROW ด้วยมือ** ให้เราได้ ROW ที่ field ตรงกับสเปกเป๊ะ

---

# ไล่โค้ด (3) — scan_registry(): อ่านทะเบียนสด

**ช่องเติมที่ 3**: ถามเฟิร์มแวร์ว่าตอนนี้มีกี่โมเดล — เลขนี้จะเพิ่มขึ้นหลังเราเพิ่มโมเดลสำเร็จ:

```python
def scan_registry():
    # เติม: อ่านจำนวนโมเดลปัจจุบันมาเก็บใน n
    n = 0
    pass                      # เติม: n = edge_ai.count()
    models = edge_ai.models()
    mine = -1
    for i, m in enumerate(models):
        hit = (m['name'] == SPEC['name'])
        ...
```

- `edge_ai.count()` คืนจำนวนโมเดลที่คอมไพล์รวมใน image ตอนนี้ (`sizeof(s_models)/...`)
- ก่อนเพิ่ม Fall = 6 · หลัง build ใหม่สำเร็จ = 7 — diff นี้คือหลักฐานว่า Edit 1+2 ติดจริง
- ยังเป็นการ **ถามฮาร์ดแวร์ก่อน อย่าเดา** เหมือนที่ทำมาตั้งแต่ บทเรียน 1.1–1.3

> `edge_ai.count()` เป็น pull ผ่าน IPC เหมือน `models()` — เรียกเมื่อไรก็ได้ มันไปนับ `s_models[]` บน CM55 มาให้สดๆ

---

# ไล่โค้ด (4) — หา index ของโมเดลเราในทะเบียน

**ช่องเติมที่ 4**: วนทะเบียนหาว่าชื่อโมเดลเราอยู่ index ไหน (ต้องรู้ index ก่อนถึงจะ `select()` ได้):

```python
    for i, m in enumerate(models):
        hit = (m['name'] == SPEC['name'])
        # เติม: ถ้า hit เป็นจริง ให้ mine = i
        pass
        if i < len(rows):
            rows[i].text('%2d  %-16s %s'
                         % (m['index'], m['name'], SENSOR[m['sensor']]))
            rows[i].color(GREEN if hit else DIM)   # ของเราเขียว ที่เหลือจาง
            rows[i].show()
    return mine, n
```

- เทียบ `m['name']` กับ `SPEC['name']` — ตรงเมื่อไร จำ `i` ไว้ใน `mine`
- แถวที่ `hit` ระบายเขียว = "โมเดลของเราโผล่แล้ว" (ชัยชนะที่เห็นได้)
- ถ้าวนจบแล้ว `mine` ยังเป็น `-1` = ยังไม่เจอ → ต้องกลับไปเช็ก 3 การแก้ + build ใหม่

> เราหา index จากชื่อ ไม่ hard-code ตัวเลข เพราะพอเพิ่มโมเดล ลำดับ index อาจเลื่อน — หาโดยชื่อปลอดภัยกว่าเสมอ (บทเรียนเดียวกับ `models()` ใน บทเรียน 1.1–1.3)

---

# ไล่โค้ด (5) — select + result: รันของเราจริง

**ช่องเติมที่ 5**: หัวใจของ MVP วันนี้ — สั่งรันโมเดลที่เราเพิ่ง เพิ่มเข้าไป แล้วอ่าน verdict:

```python
def run_mine(idx):
    try:
        # เติม: สั่ง select(idx) แล้วอ่านผลมาเก็บใน r
        r = None
        pass                  # เติม: edge_ai.select(idx); r = edge_ai.result()
        detail.text("running %s — ทำท่าตามคลาส" % SPEC['name'])
        detail.color(GREEN)
        return r
    except OSError as e:      # ข้ามคอร์พลาดได้ ต้องเผื่อไว้
        detail.text("select ล้มเหลว: %s" % e)
        detail.color(RED)
        return None
```

- `edge_ai.select(idx)` สั่ง CM55 สลับมารันโมเดลของเรา (confirm by observation — โยน `OSError` ได้)
- `edge_ai.result()` คืน verdict `{label, conf, scores, seq, latency_ms}` — เหมือนที่ใช้มาตั้งแต่ บทเรียน 1.1–1.3
- เมื่อ `Fall Detection` รันแล้วขยับบอร์ดจริง คลาสจะสลับ `normal` / `fall` = โมเดลของเราทำงาน

> ห่อ `select()` ด้วย `try/except OSError` เสมอ — โมเดลใหม่ที่เพิ่งเพิ่มมีโอกาส init ไม่ผ่าน (เช่น arena ไม่พอ) เราอยากเห็น error ชัดๆ ไม่ใช่โปรแกรมตายเงียบ

---

# ลงมือทำ — เติมช่องว่างทั้ง 5 จุด

เปิด [`s19_extend_model.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m07-under-the-hood/l04-extend-model-lab/practice/s19_extend_model.py) มี `# เติม:` วางไว้ **5 จุด** ครอบทั้งฝั่ง C (สร้าง ROW) และฝั่ง MicroPython (ยืนยัน):

| # | จุด | เติมด้วย | ถ้าลืม |
|---|---|---|---|
| 1 | `SPEC['sensor']` | `edge_ai.SENSOR_IMU` | make_row พังตอนอ่าน sensor |
| 1 | `SPEC['labels']` | `["normal", "fall"]` | ROW ไม่มีคลาส |
| 2 | `deq_fn` | `"AIM_%s_dequeue" % prefix` | ROW มี `.dequeue = None` |
| 3 | `n` | `edge_ai.count()` | diff จำนวนโมเดลเป็น 0 เสมอ |
| 4 | `mine` | `mine = i` (เมื่อ hit) | หาโมเดลไม่เจอ กด Run ไม่ได้ |
| 5 | `run_mine` | `select(idx)` + `result()` | กด Run แล้วไม่มี verdict |

ขั้นตอน:

1. ไล่หา `# เติม:` ทีละจุด เติมตามคำใบ้
2. กด **Run** — อ่าน "3 การแก้" ที่พิมพ์ออกมา เอาไปวางในเฟิร์มแวร์ (Makefile + ROW + ไฟล์)
3. `rm -rf proj_cm55/build; make program EDGE_AI_MODEL=combo` แล้วกลับมากด **Re-check** → **Run mine**

> ห้าช่องนี้เดินครบวงจรของสาย Researcher: ออกแบบสเปก → ประกอบ C ROW → build → ยืนยันว่าโผล่ → รันจริง

---

# ลงมือ (1) — บนบอร์ด BENTO จริง

การเพิ่มโมเดลต้อง build เฟิร์มแวร์ใหม่ ดังนั้นขั้นนี้ทำบน **บอร์ดจริง** (Emulator รัน MicroPython แต่ไม่ build C):

1. เติม 5 ช่องในไฟล์ฝึก แล้ว Run บนบอร์ด — อ่าน "3 การแก้" ที่คอนโซลพิมพ์
2. ทำ Edit 1 (Makefile), Edit 2 (ปลดล็อก `FALL_ROW` + ต่อเข้า `s_models[]`), Edit 3 (วาง `model_fall.c/.h`)
3. `rm -rf proj_cm55/build; make program EDGE_AI_MODEL=combo` (clean build ทุกครั้ง)
4. รันไฟล์ฝึกอีกครั้ง กด **Re-check** — `Fall Detection` ควรโผล่เขียว index=6 (count 6→7)
5. กด **Run mine** แล้วขยับ/ปล่อยบอร์ดให้เหมือนล้ม ดู verdict สลับ `normal` / `fall`

> ลบ `build/` ก่อน build ทุกครั้ง (cache ของ Ninja กับ timestamp ของไฟล์ที่ sync มาทำให้ link ของเก่าได้) และ **hard power-cycle** ก่อนเชื่อผลอนุมานบนฮาร์ดแวร์

---

# ลงมือ (2) — บน BENTO Emulator (ขอบเขต)

Emulator รัน MicroPython ได้ แต่ **build C ไม่ได้** ในเบราว์เซอร์ — ใช้ซ้อม "ครึ่งบน" ของไฟล์:

1. เปิด **ide.tesaiot.dev** วางไฟล์ [`s19_extend_model.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m07-under-the-hood/l04-extend-model-lab/practice/s19_extend_model.py) กด **Run**
2. ดู "3 การแก้" ที่พิมพ์ออกมา — ซ้อมอ่าน/แก้สเปก `SPEC` แล้วดู `make_row()` เปลี่ยน ROW ตาม
3. `scan_registry()` จะโชว์ 5 โมเดลของ Emulator (ไม่มี Push) — `Fall Detection` ยัง **ไม่โผล่** (เพราะ build ไม่ได้) = ถูกต้อง เป็นบทเรียน

- ใช้ Emulator ฝึก "ออกแบบสเปก + อ่าน ROW ที่ได้" ให้คล่อง ก่อนลงมือ build บนบอร์ดจริง
- ครึ่งล่าง (`select`/`result`) ทดสอบกับโมเดลที่มีอยู่แล้วบน Emulator ได้ (ลองเลือก Motion แทน)

> ขอบเขตนี้เองก็เป็นบทเรียน: "เพิ่มโมเดล C" เป็นงานที่ต้องมี toolchain — ต่างจากงาน app-layer ที่เขียน `.py` แล้วรันได้เลยทุกพื้นผิว นี่คือเส้นแบ่งระหว่าง firmware กับ application

---

# หน้าตา Emulator ที่เราจะซ้อมกัน

ก่อนไปลงมือ นี่คือหน้าเมนู Edge AI ของ Emulator ที่อ่านทะเบียนโมเดลชุดเดียวกับที่ [`s19_extend_model.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m07-under-the-hood/l04-extend-model-lab/practice/s19_extend_model.py) ถาม

![หน้า Edge AI บน BENTO Emulator: dropdown เลือกโมเดล Motion Detection ปุ่ม Load และ Stop คลาสที่ชนะ idle เวลาอนุมาน และแถบความมั่นใจของ idle circle shaking w:680](../../assets/img/edge_ai_page.png)

จอ emulator ที่รันได้จริง — BENTO Edge AI Emulator บนเบราว์เซอร์ ใช้ซ้อม "ครึ่งบน" (ออกแบบสเปก + อ่าน ROW) ก่อนไป build จริงบนบอร์ด

> สังเกตว่าตัว Emulator มี 5 โมเดล ยังไม่มี `Fall Detection` — ถูกต้องแล้ว เพราะเบราว์เซอร์ build C ไม่ได้ ตัวที่ 7 จะโผล่ก็ต่อเมื่อเราทำครบ 3 การแก้แล้ว flash ลงบอร์ดจริง

---

# แหล่งเรียนรู้เพิ่มเติม

อยากเข้าใจ "เพิ่มโมเดล TFLite เข้าเฟิร์มแวร์ / deploy โมเดลลง MCU" ให้ลึกกว่านี้ ลองตามลิงก์เหล่านี้ (เปิดดูได้ตามสะดวก):

**วิดีโอ**

- Neural Networks — how they learn — ช่อง 3Blue1Brown: https://www.youtube.com/@3blue1brown
- Neural Networks Clearly Explained — ช่อง StatQuest with Josh Starmer: https://www.youtube.com/@statquest
- How to run TensorFlow Lite on microcontrollers — TensorFlow (official): https://www.youtube.com/@TensorFlow

**เอกสาร / ภาพอ้างอิง**

- TensorFlow Lite for Microcontrollers — คู่มือทางการ (deploy โมเดลลง MCU): https://www.tensorflow.org/lite/microcontrollers
- Arm Ethos-U55 NPU + Vela compiler — เอกสารทางการ Arm: https://developer.arm.com/Processors/Ethos-U55
- ภาพ Quantization (int8 mapping) — บทความ Quantization: https://en.wikipedia.org/wiki/Quantization_(signal_processing) (ที่มา: Wikimedia Commons, CC BY-SA)

> วิดีโอ/ภาพภายนอกเป็นของเจ้าของต้นฉบับ ใช้เพื่อการศึกษา อ้างอิงลิงก์ต้นทาง

---

# ชัยชนะที่เห็นได้ + MVP ของชุดบทเรียนนี้

<div style="text-align:center;margin:14px 0">
<div style="display:inline-block;background:#e8f5e9;border:2px solid #2e7d32;border-radius:22px;padding:10px 22px;color:#2e7d32;font-weight:700;font-size:1.05em">
ชัยชนะที่เห็นได้ของชุดบทเรียนนี้ · โมเดลตัวใหม่ที่คุณเพิ่มเอง โผล่ใน edge_ai.models() แล้วรันได้จริงบนบอร์ด
</div>
</div>

**MVP ของบทเรียน 7.3–7.4 (เกณฑ์ผ่านของชุดบทเรียน):** คุณเพิ่มโมเดลของตัวเองครบ **3 การแก้** แล้ว **`edge_ai.count()` เพิ่มขึ้น** + ชื่อโมเดลใหม่โผล่ใน `edge_ai.models()` และ **เลือกรันแล้วได้ verdict จริง** บนบอร์ด

- ทำบน **บอร์ดจริง** (ต้อง build C — Emulator ทำครึ่งบนได้)
- อธิบายได้ว่า 3 การแก้แต่ละอันทำอะไร และทำไม MicroPython/IPC ไม่ต้องแตะ

> "โผล่ในทะเบียน" ไม่ใช่แค่ตัวเลข count เพิ่ม — คุณต้อง `select()` มันแล้วเห็น verdict สลับตามการขยับบอร์ดจริง นั่นคือหลักฐานว่าทั้ง 4 ฟังก์ชันของโมเดลต่อสายถูก

---

# บันไดช่วยเหลือ — ใบ้ → เริ่มจากโครง → เฉลย → ฉบับเต็ม

ถ้าติด ให้ไต่บันไดนี้ทีละขั้น อย่าเพิ่งกระโดดไปดูเฉลย เพราะของจะเข้าหัวตอนที่คุณพยายามเองก่อน:

- **ใบ้** — คำใบ้อยู่ในคอมเมนต์ `# เติม:` ทั้ง 5 จุด + ตารางช่องเติม + หัวข้อ Filling a model slot ใน `ai_models/README.md` ของ SDK
- **เริ่มจากโครง** — [`s19_extend_model.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m07-under-the-hood/l04-extend-model-lab/practice/s19_extend_model.py) มีโครงครบทั้งไฟล์ เหลือเติม 5 จุด + ทำ 3 การแก้ในเฟิร์มแวร์
- **เฉลย** — [`s19_extend_model.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m07-under-the-hood/l04-extend-model-lab/solution/s19_extend_model.py) เติมครบพร้อมคอมเมนต์อธิบายทุกช่อง (อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์เอง)
- **ฉบับเต็ม** — [`s19_extend_model_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m07-under-the-hood/l04-extend-model-lab/examples/s19_extend_model_full.py) ฉบับขัดเรียบ: รองรับ AIM_/IMAI_, ตรวจสัญญา 4 ฟังก์ชัน, diff count ก่อน/หลัง, แยกสี CONF_FLOOR + latency

> ลองเขียนเองให้สุดก่อนนะ ถ้าติดเรื่อง build C จริงๆ ค่อยเปิดเฉลยดู `make_row()` ทีละบรรทัด แล้วกลับมาลงมือเอง เดี๋ยวเราค่อย ๆ แกะไปด้วยกัน

---

# เชื่อมโยงรากฐาน — วันนี้เราแตะอะไรไปบ้าง

การเพิ่มโมเดลตัวแรกซ่อนแนวคิดวิศวกรรม Edge AI หลายชั้นที่รวบยอดทั้งคอร์ส:

**ฝั่ง Edge AI / เฟิร์มแวร์**
- **Shape-driven registry** — ข้อมูล (`s_models[]`) ขับพฤติกรรม ไม่ใช่ชื่อ hard-code → เพิ่มของใหม่ = เพิ่มแถว
- **Model contract** — สัญญา 4 ฟังก์ชัน (`init/enqueue/dequeue/finalize`) = interface ที่ทุกโมเดลต้องทำตาม
- **feed = แปลงหน่วย** — เลือกเซนเซอร์เดิม เลี่ยงงาน feed ใหม่ · เซนเซอร์ใหม่ต้องเขียน feed เอง
- **Vela + int8** — MCU ต้องคอมไพล์เพิ่มลง NPU · feature parity คือกับดักเงียบตัวจริง

**ฝั่งกระบวนการ / เครื่องมือ**
- **3 การแก้** — Makefile · ROW+s_models[] · ไฟล์โมเดล แล้ว clean build
- **ยืนยันด้วยการวัด** — `count()` diff + `models()` + verdict จริง ไม่เชื่อจนกว่าจะเห็น
- **firmware vs app** — เพิ่มโมเดล C ต้องมี toolchain ต่างจาก app-layer ที่ `.py` รันได้ทุกพื้นผิว

> ทั้งหมดนี้คือก้าวจาก "ผู้ใช้ Edge AI" เป็น "ผู้ต่อเติม Edge AI" — คุณเปิดฝากระโปรงเครื่องยนต์ได้แล้ว และรู้ว่าจะเสียบของใหม่เข้าไปตรงไหนอย่างปลอดภัย

---

# ใช้จริงที่ไหน — การต่อเติม Edge AI ในโลกจริง

ทักษะ "เพิ่มโมเดลเข้าเฟิร์มแวร์" ไม่ใช่แบบฝึกหัด — มันคืองานจริงของทีมผลิตภัณฑ์ Edge AI:

<div style="text-align:center;margin:6px 0">
<svg width="880" height="210" viewBox="0 0 880 210" font-family="DejaVu Sans, sans-serif">
  <rect x="12" y="10" width="420" height="92" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="28" y="34" font-size="13" font-weight="700" fill="#1565c0">เพิ่มความสามารถให้สินค้าเดิม</text>
  <text x="28" y="56" font-size="11" fill="#555">นาฬิกาเพิ่ม "ตรวจการล้ม" ในเฟิร์มแวร์รุ่นถัดไป</text>
  <text x="28" y="76" font-size="11" fill="#555">โมเดลใหม่ผ่าน OTA · ฮาร์ดแวร์เดิม</text>
  <text x="28" y="94" font-size="11" fill="#888">= 3 การแก้ + build ที่เราทำวันนี้</text>
  <rect x="448" y="10" width="420" height="92" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="464" y="34" font-size="13" font-weight="700" fill="#2e7d32">โมเดลเฉพาะทางของลูกค้า</text>
  <text x="464" y="56" font-size="11" fill="#555">โรงงานอยากตรวจ "เสียงเครื่องจักรผิดปกติ" ของตัวเอง</text>
  <text x="464" y="76" font-size="11" fill="#555">เทรนเอง (โมดูล 5 (Training)) → wrap → เพิ่มเข้าทะเบียน</text>
  <text x="464" y="94" font-size="11" fill="#888">= Path A/B + สัญญา 4 ฟังก์ชัน</text>
  <rect x="12" y="112" width="420" height="88" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="28" y="136" font-size="13" font-weight="700" fill="#e65100">แพลตฟอร์มหลายโมเดล</text>
  <text x="28" y="158" font-size="11" fill="#555">image เดียวบรรจุหลายโมเดล สลับตอนรัน (combo)</text>
  <text x="28" y="178" font-size="11" fill="#555">จัดการหน่วยความจำ/สัญลักษณ์ไม่ให้ชนกัน</text>
  <text x="28" y="196" font-size="11" fill="#888">= objcopy prefix + .ml_weights ที่เราเห็นวันนี้</text>
  <rect x="448" y="112" width="420" height="88" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="464" y="136" font-size="13" font-weight="700" fill="#6a1b9a">งานวิจัย — engine ตัวใหม่</text>
  <text x="464" y="158" font-size="11" fill="#555">อยากลอง runtime อื่น → เพิ่ม MicroPython module ใหม่</text>
  <text x="464" y="178" font-size="11" fill="#555">reuse bento_link IPC · pull/confirm pattern</text>
  <text x="464" y="196" font-size="11" fill="#888">(สาย Researcher แท้)</text>
</svg>
</div>

> เห็นไหมว่า "เพิ่มโมเดลตัวที่ 7" วันนี้ คือทักษะเดียวกับที่ทีมจริงใช้ปล่อยฟีเจอร์ AI ใหม่ผ่าน OTA — เราแค่ทำมันครบวงจรบนโต๊ะเรียน

---

# Checklist ก่อนเชื่อผลบนฮาร์ดแวร์

checklist ปิดงานจากเอกสารภายในของเฟิร์มแวร์ — ไล่ให้ครบก่อนบอกว่า "โมเดลเพิ่มสำเร็จ":

- ☐ โมเดลรันได้เดี่ยวๆ ก่อน (ทดสอบ `.tflite` ใน Python ก่อน wrap)
- ☐ สัญลักษณ์ `AIM_<NAME>_*` / `IMAI_<NAME>_*` ไม่ชนกับใคร (`nm` เช็ก — ระวัง `mtb_init` global)
- ☐ ROW ต่อเข้า `s_models[]` แล้ว, `<name>` อยู่ใน `AI_MODELS`, วางไฟล์แล้ว
- ☐ weights ก้อนใหญ่ → ใส่ section `.ml_weights` (กันล้น flash wall)
- ☐ front-end ตรงกับตอน train (สำคัญมากสำหรับเสียง/เรดาร์)
- ☐ `rm -rf proj_cm55/build; make program EDGE_AI_MODEL=combo`
- ☐ REPL: `edge_ai.count()` เพิ่มขึ้น, ชื่อใหม่ใน `edge_ai.models()`, ได้ verdict จริง
- ☐ **hard power-cycle** ก่อนเชื่อผลอนุมานบนฮาร์ดแวร์

> ข้อสุดท้ายคือกฎทองของการดีบักบนบอร์ด: หลัง flash เซนเซอร์/โมเดลบางตัวต้อง power-cycle ก่อน ไม่งั้นค่าที่วัดได้อาจหลอกเรา — "ONE change per flash, power-cycle before trusting"

---

# งานทำเอง + สรุปบทเรียน

**งานทำเอง (ท้ายบทเรียน):**

1. เติม [`s19_extend_model.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m07-under-the-hood/l04-extend-model-lab/practice/s19_extend_model.py) ให้ครบทั้ง 5 ช่อง + ทำ 3 การแก้ในเฟิร์มแวร์ จนโมเดลใหม่โผล่ใน `edge_ai.models()` (บอร์ดจริง)
2. บันทึกค่า `edge_ai.count()` **ก่อน/หลัง** เพิ่มโมเดล แล้วอธิบายว่าทำไมเลขเปลี่ยนโดยไม่ต้องแตะ MicroPython
3. เปลี่ยน `SPEC` ให้เป็นโมเดลของทีมเอง (เลือกเซนเซอร์ที่มี feed อยู่แล้ว) แล้วเล่าว่า 3 การแก้ของทีมต่างจาก Fall ตรงไหน

ใบ้ข้อ 3 — ถ้าเลือกเซนเซอร์ MIC (เช่น keyword) จะยืม `feed_audio` ได้ แต่ต้องระวัง front-end (FFT/mel) ให้ตรงกับตอน train — นี่คือกับดัก feature parity ที่เตือนไว้

**วันนี้เราได้:** เข้าใจว่าการเพิ่มโมเดล = 3 การแก้ · รู้จักสัญญา 4 ฟังก์ชัน + AIM_/IMAI_ · เข้าใจ feed กับ Vela · เพิ่ม Fall Detection เข้าทะเบียนแล้วรันได้จริง

> ชุดบทเรียนถัดไป (บทเรียน 8.1–8.2 · Capstone) เราจะรวบทุกอย่างตั้งแต่ DAQ ถึง Apps มาสร้าง **ผลิตภัณฑ์ Edge AI ของทีมเอง** — เอาทักษะ "ต่อเติมเครื่องยนต์" วันนี้ไปใช้ได้เต็มที่ เจอกันครับ
