---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 1.2 — โมดูล edge_ai: ถามทะเบียนโมเดล เลือก แล้วอ่านคำตอบ"
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

# บทเรียน 1.2 — โมดูล edge_ai: ถามทะเบียนโมเดล เลือก แล้วอ่านคำตอบ

## Edge AI และวงจรชีวิตของข้อมูล · รันโมเดลตัวแรกของเรา

**โมดูล 1 — เริ่มต้น: รันของจริงแล้วแกะดูข้างใน**

> ต่อจากบทเรียน 1.1 — Edge AI คืออะไร: วงจรชีวิตของข้อมูลห้าขั้นและเป้าหมายที่โมเดลไปรันได้

---

# รู้จักโมดูล edge_ai

โมดูล `edge_ai` คือหน้าต่างเดียวที่เราคุยกับเครื่องยนต์อนุมานบน M55 มีคำสั่งเยอะ แต่ชุดบทเรียนนี้ใช้แค่ **4 ตัวหลัก** ก็รันได้ครบวง

| คำสั่ง | คืนค่า / ทำอะไร |
|---|---|
| `edge_ai.count()` | จำนวนโมเดลที่มี |
| `edge_ai.models()` | list ของ dict หนึ่งตัวต่อโมเดล: `{index, name, sensor, labels}` |
| `edge_ai.select(n)` | สั่งให้รันโมเดลหมายเลข `n` (ส่งคำสั่งแล้วรอยืนยัน) |
| `edge_ai.result()` | ผลอนุมานล่าสุดเป็น dict หรือ `None` ถ้ายังไม่มีผล |
| `edge_ai.stop()` | หยุดเครื่องยนต์ให้ว่าง (idle) |
| `edge_ai.CONF_FLOOR` | ค่าคงที่ 0.50 — ต่ำกว่านี้ถือว่า "ยังไม่ชัวร์" |

> โฟกัสสี่ตัว: **models → select → result → stop** สี่ตัวนี้คือทั้งเรื่องราวของชุดบทเรียนนี้ อ่านทะเบียน เลือกโมเดล อ่านผล แล้วหยุด

---

# edge_ai.models() — ถามเฟิร์มแวร์ว่ามีอะไรบ้าง

แทนที่จะ hard-code ชื่อโมเดลลงไปเอง เราถามเฟิร์มแวร์ตรงๆ มันจะคืน list ของ dict มาให้ แต่ละ dict อธิบายโมเดลหนึ่งตัว:

```python
import edge_ai
models = edge_ai.models()
# models[0] หน้าตาประมาณนี้:
# {'index': 0, 'name': 'Motion Detection',
#  'sensor': 0, 'labels': ['idle', 'circle', 'shaking']}
names = [m['name'] for m in models]
print(len(models), "โมเดล:", names)
```

- `'index'` — เลขประจำโมเดล ใช้ตอนสั่ง `select()`
- `'name'` — ชื่อที่เอาไปโชว์บนจอ / dropdown
- `'sensor'` — เซนเซอร์ที่ใช้ (0=IMU, 1=RADAR, 2=MIC)
- `'labels'` — รายชื่อคลาสที่โมเดลตอบได้

> นิสัยที่ดี: **ถามฮาร์ดแวร์ก่อน อย่าเดา** ถ้าเฟิร์มแวร์เพิ่ม/ลดโมเดล โค้ดที่อ่านจาก `models()` จะปรับตามเองโดยไม่ต้องแก้

---

# edge_ai.select(n) — สั่งแล้วรอยืนยัน

การสั่งเปลี่ยนโมเดลไม่เหมือนอ่านค่า มันเป็น "คำสั่งข้ามคอร์" ไปหา M55 `select()` จึงทำสองจังหวะ:

```python
edge_ai.select(0)     # 1) ส่งคำสั่ง SELECT ไปที่ M55
                      # 2) คอยเช็ก active() ว่าสลับจริงหรือยัง
                      #    ถ้าไม่สลับภายในเวลาที่กำหนด -> โยน OSError
```

- นี่เรียกว่า **confirm by observation** — ไม่เชื่อว่าสั่งแล้วสำเร็จ แต่รอ "เห็น" ว่ามันเปลี่ยนจริง
- เพราะข้ามคอร์มีโอกาสพลาดได้ เราจึงห่อด้วย `try/except OSError` เสมอ เผื่อเครื่องยนต์ไม่ตอบ
- `select(n)` กับ `start(n)` ทำเหมือนกัน ในคอร์สนี้เราใช้ `select()` เป็นหลัก

> อ่านโค้ดในไฟล์ฝึก จะเห็นว่าปุ่ม Load เรียก `select()` อยู่ใน `try` แล้วถ้า error ก็โชว์ "ERROR" สีแดง — นี่คือการรับมือความจริงที่ว่า "ข้ามคอร์อาจพลาด"

---

# edge_ai.result() — อ่านคำตอบของโมเดล

หัวใจของ MVP วันนี้ `result()` คืน dict หนึ่งตัวที่บอกทุกอย่างเกี่ยวกับการอนุมานครั้งล่าสุด (หรือ `None` ถ้ายังไม่มีผล):

```python
r = edge_ai.result()
# r หน้าตาประมาณนี้:
# {'label': 'shaking',        # คลาสที่ชนะ (ข้อความ)
#  'top': 2,                  # index ของคลาสที่ชนะ
#  'conf': 0.92,             # ความมั่นใจของคลาสที่ชนะ (0..1)
#  'scores': [0.03,0.05,0.92],# คะแนนของ "ทุก" คลาส
#  'latency_ms': 4.1,        # ใช้เวลาอนุมานกี่มิลลิวินาที
#  'seq': 137, 'running': True}
```

- `'label'` + `'conf'` = คำตอบสั้นๆ ("shaking 92%") · `'scores'` = คะแนนครบทุกคลาส เอาไปทำแถบได้
- `'seq'` เพิ่มขึ้นทุกครั้งที่มีผลใหม่ — เราใช้มันเช็ก "มีผลใหม่ไหม" จะได้ไม่วาดจอซ้ำๆ

> `result()` เป็นการ **pull** เหมือน `models()` — เราถามเมื่อไรก็ได้ในลูป มันคืนผลล่าสุดที่ M55 คิดไว้ ไม่บล็อกรอ

---

# CONF_FLOOR — เมื่อโมเดล "ยังไม่ชัวร์"

โมเดลไม่ได้มั่นใจ 100% เสมอ บางทีคะแนนสูงสุดก็ยังต่ำ แปลว่ามัน "เดา" มากกว่า "รู้" — เราจึงมีเส้นแบ่ง

```python
if r and r['conf'] >= edge_ai.CONF_FLOOR:   # 0.50
    print("มั่นใจ:", r['label'])
else:
    print("ยังไม่ชัวร์")
```

- `CONF_FLOOR = 0.50` คือเส้นที่เฟิร์มแวร์แนะนำ ต่ำกว่านี้อย่าเพิ่งเชื่อคำตอบ
- ในไฟล์ฉบับเต็ม (`examples/`) เราเอาเส้นนี้มาเปลี่ยนสีคำตอบ: เขียว = มั่นใจ, เหลือง = ยังไม่ชัวร์
- นี่คือบทเรียนสำคัญของ Edge AI: **โมเดลตอบความน่าจะเป็น ไม่ใช่ความจริงเด็ดขาด** เราต้องตัดสินใจว่าจะเชื่อที่ความมั่นใจเท่าไร

> ในงานจริง เส้นนี้สำคัญมาก ตั้งต่ำไปก็เตือนพร่ำเพรื่อ (false positive) ตั้งสูงไปก็พลาดของจริง เราจะเล่นกับมันจริงจังในชุดบทเรียน Apps (บทเรียน 6.3–6.4)

---

# คณิตเบื้องหลัง — จากเซนเซอร์ถึงคลาสที่ชนะ

การอนุมานหนึ่งครั้งคือสายโซ่ของฟังก์ชันสี่ทอด อ่านจากซ้ายไปขวา:

$$ \underbrace{x}_{\text{sensor}} \;\longrightarrow\; \underbrace{f(x)}_{\text{feature}} \;\longrightarrow\; \underbrace{s=[s_0,\dots,s_{K-1}]}_{\text{model}} \;\longrightarrow\; \underbrace{\hat{y},\; c}_{\text{verdict}} $$

คลาสที่ชนะ ($\hat{y}$) และความมั่นใจ ($c$) คำนวณจากเวกเตอร์คะแนน $s$ ตรงๆ:

$$ \hat{y} = \arg\max_{k}\, s_k \qquad\qquad c = \max_{k}\, s_k $$

- $x$ = ข้อมูลดิบจากเซนเซอร์ (IMU / MIC / RADAR) หนึ่งหน้าต่างเวลา
- $f(x)$ = feature ที่ผ่าน DSP แล้ว (สิ่งที่โมเดล "เห็น" จริง — เก็บลงลึกใน โมดูล 4 (Analysis))
- $s_k$ = คะแนนของคลาสที่ $k$ รวมกันได้ 1 คือ $\sum_k s_k = 1$ → ตรงกับ `r['scores']`
- $\hat{y}$ = index ของคลาสที่ชนะ = `r['top']` · $c$ = ความมั่นใจ = `r['conf']`
- $K$ = จำนวนคลาสของโมเดลนั้น (เช่น Motion มี $K=3$: idle, circle, shaking)

> ทำไมสำคัญกับชุดบทเรียนนี้: บรรทัด `r = edge_ai.result()` คืนเวกเตอร์ $s$ ทั้งชุด เราจึงวาดได้ทั้งคลาสที่ชนะ **และ** แถบของคลาสอื่น ส่วน `CONF_FLOOR` ก็คือเกณฑ์ตัดบนค่า $c$ นี่เอง — เชื่อคำตอบก็ต่อเมื่อ $c \ge 0.50$

---

# คณิตเบื้องหลัง — latency วัดเป็นมิลลิวินาที

`result()` คืน `latency_ms` มาด้วย คือเวลาที่ NPU ใช้อนุมานหนึ่งครั้ง ($t_{\text{ms}}$) ตัวเลขนี้บอกว่าโมเดลตอบได้ "ทันเหตุการณ์" แค่ไหน

อัตราสูงสุดที่รันได้ต่อวินาที (throughput) แปลงตรงจาก latency:

$$ \text{fps} = \frac{1000}{t_{\text{ms}}} $$

ถ้างานต้องตอบทันภายในงบเวลา $t_{\text{budget}}$ เงื่อนไขที่ต้องผ่านคือ:

$$ t_{\text{ms}} \;\le\; t_{\text{budget}} $$

- $t_{\text{ms}}$ = `r['latency_ms']` — เช่น $4.1$ ms บนบอร์ด (Ethos-U55 ช่วยคูณเมทริกซ์ให้)
- แทนค่า: $t_{\text{ms}} = 4.1 \Rightarrow \text{fps} = \dfrac{1000}{4.1} \approx 244$ ครั้ง/วินาที — เหลือเฟือสำหรับงานเรียลไทม์
- $t_{\text{budget}}$ = งบเวลาที่งานยอมรับได้ (เช่น ตรวจการล้มอยากได้ $< 100$ ms)

> ทำไมสำคัญกับชุดบทเรียนนี้: latency ต่ำคือ **เหตุผลข้อแรก** ที่เรารันบน edge ไม่ใช่คลาวด์ (ย้อนดูสไลด์ "ทำไมต้องรันบนอุปกรณ์") — ลูปเราอ่านผลทุก ~180 ms แต่ NPU อนุมานเสร็จในไม่กี่ ms จอเลยไม่มีทางตามไม่ทัน

---

# ลงมือ (1) — รันบน BENTO Emulator

ไม่มีบอร์ดก็เริ่มได้เลย เปิดเบราว์เซอร์แล้วทำตามนี้:

1. เปิด **ide.tesaiot.dev** (BENTO Emulator) ในเบราว์เซอร์
2. เปิดไฟล์ [`s01_first_inference.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l03-first-inference-lab/practice/s01_first_inference.py) (หรือวางโค้ด)
3. กด **Run** — จะเห็นหน้าเมนู Edge AI: dropdown รายชื่อโมเดล + การ์ดผลลัพธ์
4. เลือก **Motion Detection** กด **Load** แล้วลากแผ่นเอียง/กดปุ่ม Shake ที่ Emulator จำลองให้
5. ดูคลาสที่ชนะเปลี่ยนเป็น `shaking` / `circle` / `idle` พร้อมแถบความมั่นใจ

> Emulator ใช้เซนเซอร์ **จำลอง** และคะแนนของโมเดลก็คำนวณเลียนแบบจากค่าจำลองนั้น (ไม่ได้รันโมเดลจริง ยกเว้นโหมดที่รันโมเดล Motion จริงผ่าน ONNX Runtime Web) แต่ API เหมือนบอร์ดจริงทุกบรรทัด — เหมาะกับซ้อมที่บ้าน แล้วมายืนยันกับของจริงบนบอร์ด

---

# หน้าตาจริงของ Edge AI บนจอ

นี่คือหน้า Edge AI ที่เราจะรันในชุดบทเรียนนี้ — dropdown เลือกโมเดล, ปุ่ม Load/Stop, คลาสที่ชนะตัวใหญ่ และแถบความมั่นใจของทุกคลาสเรียงลงมา

![หน้า Edge AI บน BENTO Emulator: dropdown เลือกโมเดล Motion Detection ปุ่ม Load และ Stop คลาสที่ชนะ idle เวลาอนุมาน และแถบความมั่นใจของ idle circle shaking w:680](../../assets/img/edge_ai_page.png)

จอ emulator ที่รันได้จริง — **BENTO Edge AI Emulator** (เปิดในเบราว์เซอร์ ไม่ต้องมีบอร์ด)

> ทุกอย่างที่เห็นในภาพนี้มาจากคำสั่งแค่ 4 ตัว: `models()` ป้อน dropdown · `select()` อยู่ที่ปุ่ม Load · `result()` ป้อนคลาสที่ชนะ + แถบคะแนน · `stop()` อยู่ที่ปุ่ม Stop — จำภาพนี้ไว้ เดี๋ยวไล่โค้ดจะเห็นว่าแต่ละส่วนมาจากบรรทัดไหน

---

# ลงมือ (2) — รันบนบอร์ด BENTO จริง

บนบอร์ดจริงเราใช้ของจริง เซนเซอร์จริง NPU จริง:

1. เสียบบอร์ดเข้าคอมด้วยสาย USB
2. เปิดไฟล์ [`s01_first_inference.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m01-onboarding/l03-first-inference-lab/practice/s01_first_inference.py) ใน **BENTO IDE** กด **Program to Device**
3. บนจอบอร์ดจะขึ้นหน้าเมนู Edge AI เหมือน Emulator เป๊ะ
4. เลือก **Motion Detection** กด **Load** แล้ว **เขย่าบอร์ด / วาดวงกลมในอากาศ / วางนิ่ง**
5. ลองสลับไป **Baby Cry / Cough / Siren** แล้วส่งเสียงตาม ดูคลาสที่ชนะเปลี่ยนตามเสียง

> จุดที่ควรสังเกต: `latency_ms` บนบอร์ดจริงคือเวลาที่ NPU ใช้อนุมานจริงๆ มักไม่กี่มิลลิวินาที — เร็วเพราะมี Ethos-U55 ช่วยคูณเมทริกซ์
