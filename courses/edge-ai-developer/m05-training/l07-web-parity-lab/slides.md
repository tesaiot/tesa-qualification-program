---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 5.7 — ลงมือทำ: verdict บนเว็บให้ตรงกับ PC และเรื่องราว Cortex-A"
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

# บทเรียน 5.7 — ลงมือทำ: verdict บนเว็บให้ตรงกับ PC และเรื่องราว Cortex-A

## Training III · รันโมเดลบน Web และเรื่องราว Cortex-A

**โมดูล 5 — ฝึกโมเดลและนำไปใช้หลายเป้าหมาย**

> ต่อจากบทเรียน 5.6 — รันโมเดลบนเว็บ: LiteRT.js, int8 I/O และ parity

---

# โครงของ web_verdict — สี่ขั้นเดียวกันทุกภาษา

ทั้งฝั่ง PC (`web_verdict` ใน Python) และฝั่งเบราว์เซอร์ (`webVerdict` ใน JS) เดินสี่จังหวะเดียวกัน:

<div style="text-align:center;margin:6px 0">
<svg width="900" height="140" viewBox="0 0 900 140" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arWV" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="44" width="200" height="60" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="114" y="70" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">1 · normalize</text>
  <text x="114" y="90" font-size="11" fill="#666" text-anchor="middle">mean/std เดียวกัน</text>
  <rect x="238" y="44" width="200" height="60" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="338" y="70" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">2 · quantize</text>
  <text x="338" y="90" font-size="11" fill="#666" text-anchor="middle">float→int8 (ถ้า int8 I/O)</text>
  <rect x="462" y="44" width="200" height="60" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="562" y="70" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">3 · invoke</text>
  <text x="562" y="90" font-size="11" fill="#666" text-anchor="middle">กราฟทำงานเอง</text>
  <rect x="686" y="44" width="200" height="60" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="786" y="70" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">4 · dequantize</text>
  <text x="786" y="90" font-size="11" fill="#666" text-anchor="middle">→ verdict {label,conf}</text>
  <line x1="214" y1="74" x2="236" y2="74" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arWV)"/>
  <line x1="438" y1="74" x2="460" y2="74" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arWV)"/>
  <line x1="662" y1="74" x2="684" y2="74" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arWV)"/>
  <text x="450" y="30" font-size="11" fill="#888" text-anchor="middle">ขั้น 1, 2, 4 คือของเรา · ขั้น 3 กราฟทำเอง — parity อยู่ที่ 1, 2, 4</text>
</svg>
</div>

- ขั้น 1, 2, 4 เป็น **โค้ดของเรา** (front-end + post) — ต้องเหมือนกันข้ามภาษา
- ขั้น 3 กราฟทำเอง เกือบเหมือนกันข้ามเป้าหมาย (ต่างแค่ kernel: XNNPACK vs CMSIS-NN)
- ในไฟล์ฝึก [`s13_web.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l07-web-parity-lab/practice/s13_web.py) สี่ขั้นนี้แหละคือ 5 ช่องที่คุณต้องเติม

> จำโครงสี่ขั้นนี้ไว้ เดี๋ยวไล่โค้ดทีละช่อง แล้วคุณจะเห็นว่า Python กับ JS เป็นเรื่องเดียวกันคนละภาษา

---

# ไล่โค้ด (1) — normalization (เติม 1)

**ช่องเติมที่ 1**: ทำ front-end ให้เหมือนตอนเทรน — จุดที่ parity พังบ่อยสุด:

```python
def web_verdict(model_path, window, z):
    # เติม 1: ใช้ mean/std ชุดเดียวกับตอนเทรน
    x = (window - z["mean"]) / z["std"]
    ...
```

- `z` คือไฟล์ `model_int8.tflite.norm.npz` ที่ [`train.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/train.py) เซฟไว้ มี `mean` กับ `std` อย่างละ 6 ค่า (ต่อแกน IMU)
- ถ้าลืมขั้นนี้ (ปล่อย `x = window`) โมเดลเห็นข้อมูลดิบคนละสเกล — verdict จะมั่วทันที
- ฝั่ง JS ก็ต้องทำสูตรเดียวกัน: `(v - mean[i%6]) / std[i%6]`

> ลองเล่นให้เห็นภัย: comment บรรทัดนี้ทิ้งแล้วรัน จะเห็น conf เพี้ยนจนคลาสที่ชนะเปลี่ยน — นั่นคือพลังของ front-end

---

# ไล่โค้ด (2) — quantize float → int8 (เติม 2)

**ช่องเติมที่ 2**: โมเดล MCU เป็น int8 in/out เราจึงต้องแปลง feature เป็น int8 ก่อนป้อน:

```python
    in_scale, in_zero = inp["quantization"]      # อ่านค่ามาจากตัวโมเดล ไม่ใช่เดา
    # เติม 2: quantize ด้วย scale/zero ของ input tensor
    q = np.clip(np.round(x / in_scale + in_zero), -128, 127).astype(np.int8)
```

- `scale/zero` มาจาก `inp["quantization"]` — ค่าที่ converter คำนวณไว้ตอน quantize อ่านจากโมเดลตรงๆ
- `np.clip(..., -128, 127)` กันค่าล้นช่วง int8 · `np.round` ปัดให้เป็นจำนวนเต็ม
- ไฟล์ web (float I/O) **ข้ามขั้นนี้** เพราะกราฟรับ float ตรงๆ — นี่คือความต่างเดียวของเส้นทาง web

> quantize คือการ "ย่อ" float ให้ลงช่วง 256 ระดับของ int8 — สูตรนี้ต้องเป๊ะ ไม่งั้น parity พังตั้งแต่ input

---

# ไล่โค้ด (3) — ป้อนแล้วอนุมาน (เติม 3)

**ช่องเติมที่ 3**: ขั้นที่กราฟทำงานเอง — ป้อน tensor แล้วสั่ง invoke:

```python
    # เติม 3: ป้อน q เข้าโมเดลแล้วสั่งอนุมาน
    it.set_tensor(inp["index"], q)
    it.invoke()
    o = it.get_tensor(out["index"])[0].astype(np.float32)
```

- `set_tensor` วางข้อมูลเข้าช่อง input · `invoke()` รันกราฟ · `get_tensor` ดึงผลออกจากช่อง output
- นี่คือสามบรรทัดที่เทียบตรงกับ `model.run([x])` บรรทัดเดียวของ LiteRT.js — คนละสไตล์ API งานเดียวกัน
- บน Cortex-A โค้ดสามบรรทัดนี้ **เหมือนกันเป๊ะ** เพราะ `ai-edge-litert` ลงบน RPi/Jetson ได้ตรงๆ

> ขั้นนี้แทบไม่มีอะไรให้ parity พลาด เพราะเป็นตัวกราฟทำงาน — ความต่างเล็กน้อยที่เหลือมาจาก kernel (XNNPACK vs CMSIS-NN) ซึ่งเรายอมรับผ่าน TOL

---

# ไล่โค้ด (4) — dequantize + verdict (เติม 4, 5)

**ช่องเติมที่ 4 และ 5**: แปลง output int8 กลับเป็น float แล้วสรุป verdict:

```python
    # เติม 4: dequantize output กลับเป็นความน่าจะเป็น (โมเดลมี softmax head)
    o = (o - out_zero) * out_scale
    top = int(o.argmax())
    # เติม 5: conf = คะแนนของคลาสที่ชนะ (ตัวเลขที่ใช้วัด parity)
    conf = float(o[top])
    return {"label": dt.CLASSES[top], "top": top, "conf": conf, "scores": o.tolist()}
```

- dequantize: `(int8 - zero) * scale` เอาจำนวนเต็มกลับเป็นทศนิยม — output softmax จึงรวมได้ ~1.0
- `argmax` = คลาสที่ชนะ · `conf` = คะแนนของคลาสนั้น — คู่นี้แหละที่เอาไปเทียบกับเบราว์เซอร์
- `scores` ทั้งชุดคืนออกไปด้วย เพราะ parity วัดจาก `max|scores_pc - scores_web|` ทุกคลาส

> เทียบกันชัดๆ: ฝั่ง PC ได้ `{label, conf, scores}` — ฝั่งเบราว์เซอร์ต้องได้ dict หน้าตาเดียวกัน ตัวเลขตรงในเกณฑ์ TOL = ผ่าน MVP ของบทเรียน 5.6–5.7

---

# ฝั่ง JS — LiteRT.js ทำสี่ขั้นเดียวกัน

โค้ดฝั่งเบราว์เซอร์อยู่ในไฟล์ฝึกเป็นค่าคงที่ `JS_LITERT` (พิมพ์ออกมาด้วย `--show-js`) เทียบทีละขั้นกับ Python:

```javascript
function webVerdict(window, mean, std) {
  const x = window.map((v, i) => (v - mean[i % 6]) / std[i % 6]);  // (1) normalize เหมือน PC
  const out = model.run([x]);                                      // (2)(3) float I/O + invoke
  const scores = out[0];                                           // (4) softmax อยู่ในกราฟ
  let top = 0;
  for (let i = 1; i < scores.length; i++) if (scores[i] > scores[top]) top = i;
  return {top, conf: scores[top], scores};
}
```

- ขั้น (1) normalize **สูตรเดียวกับ Python** เป๊ะ — นี่คือหัวใจของ parity
- ขั้น (2) เบราว์เซอร์ใช้ไฟล์ float I/O จึงไม่ต้อง quantize เอง — ข้าม `set_tensor int8` ไป
- ผลลัพธ์ `{top, conf, scores}` หน้าตาเดียวกับ dict ฝั่ง PC ตั้งใจให้เทียบกันได้ทันที

> อ่านสองไฟล์คู่กัน (Python กับ JS) แล้วจะเห็นชัดว่า deploy ข้ามเป้าหมายคือ "เขียนท่าเดียวกันหลายภาษา" ไม่ใช่เวทมนตร์

---

# ลงมือทำ — เติมช่องว่างทั้ง 5 จุด

เปิด [`s13_web.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l07-web-parity-lab/practice/s13_web.py) ในฟังก์ชัน `web_verdict()` มีช่องให้เติม **5 จุด** ตามโครงสี่ขั้น:

| # | ขั้น | เติมด้วย | ถ้าลืม |
|---|---|---|---|
| 1 | normalize | `x = (window - z["mean"]) / z["std"]` | verdict มั่ว (คนละสเกล) |
| 2 | quantize | `q = np.clip(np.round(x/in_scale+in_zero),-128,127).astype(np.int8)` | input เพี้ยน |
| 3 | invoke | `it.set_tensor(inp["index"], q)` + `it.invoke()` | ได้ scores เป็นศูนย์ |
| 4 | dequantize | `o = (o - out_zero) * out_scale` | conf ไม่ใช่ความน่าจะเป็น |
| 5 | verdict | `conf = float(o[top])` | conf ค้างที่ 0.0 |

ขั้นตอน:

1. ไล่หา `# เติม:` ทีละจุด แทน placeholder ด้วยคำสั่งจริงตามคำใบ้
2. รันจาก [`shared/training/`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training): `python s13_web.py` — ดู verdict ฝั่ง PC ที่พิมพ์ออกมา
3. เอา window ตัวเดียวกันไปรันในเบราว์เซอร์ (LiteRT.js) แล้วเทียบ label/conf ให้ตรงในเกณฑ์ TOL

> ห้าช่องนี้คือโครงสี่ขั้นของทุกการ deploy — เติมครบเมื่อไร คุณมี ground truth ฝั่ง PC ไว้วัด parity กับเบราว์เซอร์

---

# เรื่องราว Cortex-A — ไฟล์เดิม ไม่ต้องแก้

Web เป็นเป้าหมายที่ "ยุ่ง" ที่สุด (ต้องแปลงไฟล์ + reproduce front-end ใน JS) แต่ **Cortex-A ง่ายที่สุด**:

```bash
# บน Raspberry Pi / Jetson / mini-PC (Linux):
pip install ai-edge-litert
python eval_pc.py --model model_int8.tflite --data data/gestures.csv
```

- [`eval_pc.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/eval_pc.py) **ตัวเดิมเป๊ะ** รันบน Cortex-A ได้โดยไม่แก้แม้แต่บรรทัดเดียว — `ai-edge-litert` ลงบน ARM Linux ได้
- ใช้ **ไฟล์ `.tflite` เดิม** ไม่ต้องแปลง (int8 หรือ float ก็รันได้ ไม่มีข้อจำกัด I/O แบบเบราว์เซอร์)
- นี่คือความหมายจริงของ "train once, run everywhere" ที่จับต้องได้: PC กับ Cortex-A ใช้สคริปต์เดียวกัน

> Cortex-A คือ "PC ตัวเล็ก" ที่รัน Linux เต็ม — ต่างจาก MCU ตรงที่มี OS + Python จริง จึงเอาสคริปต์ PC ไปวางรันได้เลย

---

# สเปกตรัม Cortex-A — เร่งความเร็วด้วย delegate

Cortex-A ไม่ได้มีแค่ CPU หลายรุ่นมี GPU/NPU ในตัว เร่งการอนุมานผ่าน **delegate** ของ LiteRT:

| บอร์ด | ตัวเร่ง | delegate |
|---|---|---|
| Raspberry Pi 5 | CPU (Cortex-A76) | XNNPACK (มากับ runtime) |
| Jetson (Orin/Nano) | GPU (CUDA) | GPU delegate |
| บอร์ด NNAPI เดิม | NPU | LiteRT GPU delegate (NNAPI เลิกใช้ A15) |
| บอร์ด Arm ML | Arm NN | Arm NN = TFLite delegate |

- **delegate** = ปลั๊กอินที่ย้ายบางส่วนของกราฟไปรันบน GPU/NPU แทน CPU — ไฟล์โมเดลเดิม โค้ดเปลี่ยนนิดเดียว
- `tflite-runtime` เดิมถูกเปลี่ยนชื่อเป็น **`ai-edge-litert`** (แค่สลับชื่อ import) — ของใหม่ที่ยัง maintain
- ต่างจาก MCU: Cortex-A รับ **int8 หรือ float** ก็ได้ ไม่บังคับ int8 เหมือน Ethos-U55

> จุดตัดสินใจ: ถ้าต้องเร็ว+กินไฟต่ำมากให้ MCU · ถ้าต้องแรง+ยืดหยุ่น+มี OS ให้ Cortex-A · ถ้าต้องแชร์ทันทีไม่ติดตั้งให้ Web

---

# เลือกเป้าหมายยังไง — การตัดสินใจเชิงวิศวกรรม

คำถามที่คอร์สนี้ฝึกให้ตอบ: **"โมเดลตัวนี้ควรรันที่ไหน?"** — แต่ละที่แลกอะไรกับอะไร

<div style="text-align:center;margin:6px 0">
<svg width="900" height="200" viewBox="0 0 900 200" font-family="DejaVu Sans, sans-serif">
  <line x1="40" y1="150" x2="860" y2="150" stroke="#b0bec5" stroke-width="3"/>
  <text x="46" y="182" font-size="12" fill="#607d8b">เล็ก · กินไฟต่ำ · ต้องแปลงมาก</text>
  <text x="854" y="182" font-size="12" fill="#607d8b" text-anchor="end">แรง · ยืดหยุ่น · deploy ง่าย</text>
  <circle cx="150" cy="150" r="11" fill="#1565c0"/>
  <rect x="80" y="42" width="150" height="90" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="155" y="64" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">MCU + NPU</text>
  <text x="155" y="84" font-size="10" fill="#555" text-anchor="middle">ต้อง Vela + int8</text>
  <text x="155" y="100" font-size="10" fill="#888" text-anchor="middle">เร็ว/ประหยัดสุด</text>
  <text x="155" y="116" font-size="10" fill="#888" text-anchor="middle">แปลงยากสุด (5.8–5.9)</text>
  <circle cx="390" cy="150" r="11" fill="#2e7d32"/>
  <rect x="320" y="42" width="150" height="90" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="395" y="64" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">Web</text>
  <text x="395" y="84" font-size="10" fill="#555" text-anchor="middle">float I/O + JS front-end</text>
  <text x="395" y="100" font-size="10" fill="#888" text-anchor="middle">แชร์ลิงก์ทันที</text>
  <text x="395" y="116" font-size="10" fill="#888" text-anchor="middle">reproduce front-end</text>
  <circle cx="630" cy="150" r="11" fill="#ef6c00"/>
  <rect x="560" y="42" width="150" height="90" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="635" y="64" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">Cortex-A</text>
  <text x="635" y="84" font-size="10" fill="#555" text-anchor="middle">ไฟล์เดิม ไม่แก้</text>
  <text x="635" y="100" font-size="10" fill="#888" text-anchor="middle">มี OS + delegate</text>
  <text x="635" y="116" font-size="10" fill="#888" text-anchor="middle">deploy ง่ายสุด</text>
  <circle cx="800" cy="150" r="11" fill="#6a1b9a"/>
  <rect x="730" y="42" width="150" height="90" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="805" y="64" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">PC / Docker</text>
  <text x="805" y="84" font-size="10" fill="#555" text-anchor="middle">ground truth</text>
  <text x="805" y="100" font-size="10" fill="#888" text-anchor="middle">โต๊ะฝึก + วัด parity</text>
  <text x="805" y="116" font-size="10" fill="#888" text-anchor="middle">eval_pc.py</text>
</svg>
</div>

> ไม่มีเป้าหมายไหน "ดีที่สุด" มีแค่ "เหมาะกับงานนี้ที่สุด" — วิศวกรที่เก่งคือคนที่ตอบคำถามนี้ได้ พร้อมเหตุผล

---

# ลงมือ (1) — สร้าง ground truth ฝั่ง PC

ก่อนเทียบกับเบราว์เซอร์ เราต้องมี "คำตอบที่ถือว่าถูก" ก่อน — นั่นคือ verdict ฝั่ง PC:

1. เปิดเทอร์มินัลใน [`shared/training/`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training) (ที่มี [`dataset_tools.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/dataset_tools.py) + [`model_int8.tflite`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/model_int8.tflite))
2. เติม [`s13_web.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l07-web-parity-lab/practice/s13_web.py) ให้ครบ 5 ช่อง
3. รัน `python s13_web.py` — จะเห็น verdict: `label`, `conf`, และ `scores` ครบทุกคลาส
4. จดค่า `scores` ไว้ — นี่คือ ground truth ที่เบราว์เซอร์ต้องตามให้ทัน

```text
verdict ฝั่ง PC (ground truth ที่เบราว์เซอร์ต้องได้ตรงกัน):
  label = circle   conf = 0.9xxx  (คลาสจริง = circle)
  scores = ['0.0xxx', '0.9xxx', '0.0xxx']
```

> ถ้ายังไม่มี `data/gestures.csv` สคริปต์จะสร้างชุดสังเคราะห์ให้ก่อน (เหมือน `dataset_tools.py --synthesize`) — pipeline เดินได้ก่อนมีข้อมูลจริง

---

# ลงมือ (2) — รันในเบราว์เซอร์แล้วเทียบ

ตอนนี้เอา window เดียวกันไปรันฝั่งเบราว์เซอร์ (หน้าเว็บของคุณที่โหลด LiteRT.js — BENTO Emulator โหลดไฟล์ของเราเองไม่ได้) แล้ววัด parity:

1. เตรียมไฟล์ web: `python convert_web.py --keras model.keras --out model_web.tflite` (ต้องมี `model.keras` จาก `train.py --save-keras` ก่อน ส่วน `[[`s13_web_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l07-web-parity-lab/examples/s13_web_full.py)](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l07-web-parity-lab/examples/s13_web_full.py) --export-web` ทำขั้นเดียวกันนี้)
2. โหลด `model_web.tflite` ใน LiteRT.js แล้วรัน `webVerdict(window, mean, std)` กับ window ตัวเดิม
3. เทียบ `scores` สองฝั่ง คำนวณ `max|score_pc - score_web|`
4. ผ่านเมื่อ **คลาสที่ชนะตรงกัน** และ **ความต่างสูงสุด ≤ TOL (0.02)**

[`s13_web_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l07-web-parity-lab/examples/s13_web_full.py) ทำขั้นเดียวกันบน PC ในสคริปต์เดียว (รันทั้งไฟล์ int8 และไฟล์ web ด้วย interpreter บน PC บนชุดทดสอบ แล้วสรุป PASS/FAIL) ใช้เป็นด่านแรกก่อนเปิดเบราว์เซอร์จริง

> ถ้ายังไม่มีหน้าเว็บของตัวเอง เริ่มจาก [`s13_web_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l07-web-parity-lab/examples/s13_web_full.py) เทียบไฟล์ int8 กับไฟล์ web บน PC ก่อน แล้วค่อยยืนยันในเบราว์เซอร์ด้วยโค้ดจาก `--show-js`

---

# หน้าตาจริงของสิ่งที่เรารัน — BENTO Edge AI Emulator

นี่ไม่ใช่ภาพประกอบ แต่เป็นเบราว์เซอร์ที่กำลังอนุมานจริง (BENTO Emulator รันโมเดลท่ามือผ่าน ONNX Runtime Web):

![หน้า BENTO Playground บน Emulator ที่รันโมเดล Motion จริงผ่าน ONNX Runtime Web: คลาส idle 43% แถบความมั่นใจสามคลาส และเวลาอนุมาน 0.30 ms w:680](../../assets/img/edge_ai_real.png)

จอ emulator ที่รันได้จริง — BENTO Edge AI Emulator (MicroPython-WASM + ONNX Runtime Web ในแท็บเดียว)

- โมเดลท่ามือที่ฝึกด้วย pipeline เดียวกับเรา แปลงจาก [`model_int8.tflite`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/model_int8.tflite) เป็น ONNX ครั้งเดียว แล้วให้ verdict สดๆ บนหน้าเว็บ
- ไม่มีเซิร์ฟเวอร์ ไม่มีบอร์ด ข้อมูลไม่ออกจากเครื่อง — นี่คือ "Edge" ที่ขอบอยู่ที่แท็บของผู้ใช้
- เบื้องหลังจอทำสี่ขั้นเดียวกับ [`eval_pc.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/eval_pc.py): normalize → quantize → run → dequantize โดยป้อน window จาก IMU จำลอง

> เปิดของจริงก่อน แล้วค่อยแกะว่าทำไมมันถึงทำงาน — สี่ขั้นในโค้ด 5 ช่องของเราคือสี่ขั้นเดียวกับที่ทำงานอยู่หลังจอนี้

---

# parity ไม่ผ่าน — ไล่แก้ตรงไหนก่อน

ถ้า `max-abs-diff` เกิน TOL หรือคลาสที่ชนะไม่ตรง อย่าเพิ่งโทษตัวโมเดล ไล่ตามลำดับนี้ (เรียงจากที่ผิดบ่อยสุด):

| อาการ | สงสัยตรงไหนก่อน | เช็กอะไร |
|---|---|---|
| verdict คนละคลาสเลย | **normalize (ช่อง 1)** | ทั้งสองฝั่งใช้ `mean/std` ชุดเดียวกันจาก `.norm.npz` ไหม |
| conf เพี้ยนเป็นระบบ | **quantize (ช่อง 2)** | อ่าน `scale/zero` จากโมเดลจริง ไม่ใช่ค่าเดา |
| scores เป็นศูนย์หมด | **invoke (ช่อง 3)** | ลืม `set_tensor`/`invoke` หรือ input shape ผิด |
| ต่างกันนิดเดียวสม่ำเสมอ | **kernel (ยอมรับได้)** | XNNPACK vs CMSIS-NN — ถ้า ≤ TOL ถือว่าผ่าน |
| โหลดไฟล์ไม่ขึ้นในเบราว์เซอร์ | **ไฟล์ผิด** | ใช้ `model_web.tflite` (float I/O) ไม่ใช่ไฟล์ int8 เต็ม |

- **กฎแรก**: เทียบ `scores` ทีละคลาส ไม่ใช่ดูแค่ label — ตัวเลขบอกว่าเพี้ยนที่ขั้นไหน
- **กฎสอง**: แก้ front-end ก่อนเสมอ (ช่อง 1, 2) เพราะโมเดลไฟล์เดียวกัน กราฟไม่น่าผิด

> วิธีดีบักที่เร็วที่สุด: feed **input ชุดเดียวกันเป๊ะ** ทั้งสองฝั่ง แล้วไล่เทียบ output ทีละขั้น (หลัง normalize, หลัง quantize, หลัง invoke) — จุดที่เริ่มต่างคือจุดที่ front-end ไม่ตรง

---

# แหล่งเรียนรู้เพิ่มเติม

อยากต่อยอดเรื่องรันโมเดลในเบราว์เซอร์และ deploy บน edge ลองดูของดีเหล่านี้ (ลิงก์ต้นทาง เปิดดูได้ตามสะดวก):

**วิดีโอ (ช่องที่น่าเชื่อถือ)**

- WebAssembly คืออะไร ทำงานยังไง — ช่อง Computerphile: https://www.youtube.com/@Computerphile
- LiteRT / TensorFlow Lite รันบนเว็บและ edge — ช่อง TensorFlow: https://www.youtube.com/@TensorFlow
- Neural Networks พื้นฐานที่ทำให้ inference เข้าใจง่าย — ช่อง 3Blue1Brown: https://www.youtube.com/@3blue1brown

**ภาพ / เอกสารอ้างอิง**

- โลโก้และหน้าอธิบาย WebAssembly — https://commons.wikimedia.org/wiki/File:WebAssembly_Logo.svg (ที่มา: Wikimedia Commons, public domain)
- เอกสาร LiteRT อย่างเป็นทางการ (on-device / เบราว์เซอร์) — https://ai.google.dev/edge/litert (ที่มา: Google AI for Developers, docs)
- ONNX Runtime Web tutorial — https://onnxruntime.ai/docs/tutorials/web/ (ที่มา: ONNX Runtime docs, MIT License)

> วิดีโอ/ภาพภายนอกเป็นของเจ้าของต้นฉบับ ใช้เพื่อการศึกษา อ้างอิงลิงก์ต้นทาง — ลิงก์เหล่านี้ไว้ขุดต่อเอง

---

# ชัยชนะที่เห็นได้ + MVP ของชุดบทเรียนนี้

<div style="text-align:center;margin:14px 0">
<div style="display:inline-block;background:#e8f5e9;border:2px solid #2e7d32;border-radius:22px;padding:10px 22px;color:#2e7d32;font-weight:700;font-size:1.05em">
ชัยชนะที่เห็นได้ของชุดบทเรียนนี้ · โมเดล .tflite ที่เราเทรนเอง รันในเบราว์เซอร์แล้วให้ verdict สดๆ (การอนุมานจริง ไม่ใช่ mock)
</div>
</div>

**MVP ของบทเรียน 5.6–5.7 (เกณฑ์ผ่านของชุดบทเรียน):** โมเดล `.tflite` ที่เทรนใน บทเรียน 5.3–5.5 ให้ verdict ในเบราว์เซอร์ **ตรงกับฝั่ง PC ภายในเกณฑ์** (`max|score_pc - score_web| ≤ TOL`, คลาสที่ชนะตรงกัน)

- ทำบนหน้าเว็บที่โหลด LiteRT.js (โค้ดจาก `--show-js`) เทียบกับ [`s13_web.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l07-web-parity-lab/practice/s13_web.py) ฝั่ง PC ถ้ายังไม่มีหน้าเว็บ ใช้ [`s13_web_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l07-web-parity-lab/examples/s13_web_full.py) เทียบไฟล์ int8 กับไฟล์ web บน PC เป็นด่านแรก
- อธิบายได้ว่าทำไม parity อาจไม่เป๊ะทุกบิต (XNNPACK vs CMSIS-NN) และทำไม front-end ต้องเหมือนกัน

> "ตรงกัน" ไม่ใช่แค่ "คลาสเดียวกัน" — คุณต้องวัดตัวเลขและบอกได้ว่าความต่างอยู่ในเกณฑ์ที่ยอมรับหรือไม่ เพราะอะไร

---

# บันไดช่วยเหลือ — ใบ้ → เริ่มจากโครง → เฉลย → ฉบับเต็ม

ถ้าติด ให้ไต่บันไดนี้ทีละขั้น อย่าเพิ่งกระโดดไปดูเฉลย เพราะของจะเข้าหัวตอนที่คุณพยายามเองก่อน:

- **ใบ้** — คำใบ้อยู่ในคอมเมนต์ `# เติม:` ทั้ง 5 จุดในไฟล์ฝึก + ตารางช่องเติมหน้าที่แล้ว บอกว่าแต่ละช่องเติมอะไร
- **เริ่มจากโครง** — [`s13_web.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l07-web-parity-lab/practice/s13_web.py) มีโครงครบทั้งไฟล์ (โหลดข้อมูล/interpreter/JS snippet) เหลือแค่ 5 บรรทัดให้เติม
- **เฉลย** — [`s13_web.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l07-web-parity-lab/solution/s13_web.py) เติมครบพร้อมคอมเมนต์อธิบายทุกขั้น (อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์เอง)
- **ฉบับเต็ม** — [`s13_web_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l07-web-parity-lab/examples/s13_web_full.py) แล็บ parity ครบวง: export ไฟล์ web + รันทั้ง int8/web ทั้งชุดทดสอบ + สรุป PASS/FAIL ตามเกณฑ์ MVP ของบทเรียน 5.6–5.7

> ลองเขียนเองให้สุดก่อนนะ ถ้าติดจริงๆ ค่อยเปิดเฉลยดูทีละช่อง แล้วกลับมาพิมพ์เอง — เดี๋ยวเราค่อย ๆ แกะไปด้วยกัน

---

# เชื่อมโยงรากฐาน — วันนี้เราแตะอะไรไปบ้าง

การ deploy โมเดลข้ามเป้าหมายซ่อนแนวคิดหลายชั้นที่จะใช้ต่อในบทเรียน 5.8–5.9 และ โมดูล 6 (Apps):

**ฝั่ง deploy / ระบบ**
- **หนึ่งไฟล์ หลายเป้าหมาย** — `.tflite` เดียวไป Web/Cortex-A ได้ MCU ต้อง Vela เพิ่ม (บทเรียน 5.8–5.9)
- **int8 I/O constraint** — เบราว์เซอร์บังคับ float I/O → ต้องมี web variant ([`convert_web.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/convert_web.py))
- **front-end นอกกราฟ** — normalize/DSP ไม่อยู่ในโมเดล ต้อง reproduce ให้ตรงทุกเป้าหมาย
- **parity เป็นการวัด** — XNNPACK ≠ CMSIS-NN bit-exact ใช้ `max-abs-diff` + TOL ตัดสิน

**ฝั่งเครื่องมือ / runtime**
- **LiteRT.js** — โหลด `.tflite` ในเบราว์เซอร์ (เลือกเหนือ tfjs-tflite/ORT-Web)
- **ai-edge-litert** — `tflite-runtime` โฉมใหม่ รันบน PC และ Cortex-A ด้วยสคริปต์เดียว
- **delegate** — เร่งบน GPU/NPU ของ Cortex-A โดยไม่แก้ไฟล์โมเดล

> ทั้งหมดนี้ทำให้โมเดลของคุณจาก บทเรียน 5.3–5.5 ไม่ได้ติดอยู่บนบอร์ดตัวเดียว — มันพร้อมไปอยู่ทุกที่ที่งานต้องการ

---

# ใช้จริงที่ไหน — browser ML ในโลกจริง

การรันโมเดลในเบราว์เซอร์ไม่ใช่ของแปลกใหม่ มีสินค้า/เครื่องมือจริงทำแบบเดียวกัน:

<div style="text-align:center;margin:6px 0">
<svg width="880" height="200" viewBox="0 0 880 200" font-family="DejaVu Sans, sans-serif">
  <rect x="12" y="10" width="420" height="86" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="28" y="34" font-size="13" font-weight="700" fill="#1565c0">Edge Impulse — browser pre-flight</text>
  <text x="28" y="56" font-size="11" fill="#555">ลองโมเดลในเบราว์เซอร์ก่อน flash ลงบอร์ด</text>
  <text x="28" y="76" font-size="11" fill="#888">"เบราว์เซอร์เป็นด่านตรวจ" — แนวเดียวกับ parity ของเรา</text>
  <rect x="448" y="10" width="420" height="86" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="464" y="34" font-size="13" font-weight="700" fill="#2e7d32">Google Teachable Machine</text>
  <text x="464" y="56" font-size="11" fill="#555">เทรน+อนุมานในเบราว์เซอร์ (tfjs)</text>
  <text x="464" y="76" font-size="11" fill="#888">แต่ตายตัว ไม่มี sensor/DSP/embedded</text>
  <rect x="12" y="108" width="420" height="82" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="28" y="132" font-size="13" font-weight="700" fill="#e65100">BENTO Edge AI Emulator</text>
  <text x="28" y="154" font-size="11" fill="#555">MicroPython-WASM + ONNX Runtime Web อนุมานจริง</text>
  <text x="28" y="174" font-size="11" fill="#888">คู่ที่ผู้เขียนยังไม่พบในเครื่องมืออื่น</text>
  <rect x="448" y="108" width="420" height="82" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="464" y="132" font-size="13" font-weight="700" fill="#6a1b9a">ร่วมกัน — ไฟล์เดียว หลายที่</text>
  <text x="464" y="154" font-size="11" fill="#555">โมเดลของคุณรันได้ MCU/Web/Cortex-A</text>
  <text x="464" y="174" font-size="11" fill="#888">พิสูจน์ parity = มั่นใจก่อน ship</text>
</svg>
</div>

> จุดต่างของเรา: **MicroPython-first + หลายเป้าหมาย + emulator ที่อนุมานจริง + ครบทั้ง pipeline** — เท่าที่ผู้เขียนสำรวจ ยังไม่พบคอร์สหรือเครื่องมือที่รวมสี่อย่างนี้ไว้ด้วยกัน

---

# งานทำเอง + สรุปบทเรียน

**งานทำเอง (ท้ายบทเรียน):**

1. เติม [`s13_web.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l07-web-parity-lab/practice/s13_web.py) ให้ครบทั้ง 5 ช่อง รันได้จริงจาก [`shared/training/`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training) แล้วอ่าน verdict ฝั่ง PC ออก
2. รัน window อย่างน้อย **1 ตัว** ในเบราว์เซอร์ (หน้าเว็บที่โหลด LiteRT.js) หรือถ้ายังไม่มี ใช้ [`s13_web_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l07-web-parity-lab/examples/s13_web_full.py) เทียบ `scores` กับฝั่ง PC แล้วจดค่า `max-abs-diff`
3. อธิบายว่า **ทำไม** ค่าอาจไม่เป็นศูนย์เป๊ะ และทำไมยัง "ผ่าน" ได้ถ้าอยู่ในเกณฑ์ TOL

ใบ้ข้อ 3 — ลองปิด normalization (ช่อง 1) ฝั่งใดฝั่งหนึ่งดู แล้วเทียบว่า `max-abs-diff` พุ่งขึ้นแค่ไหน จะเห็นว่า front-end สำคัญกว่าที่คิด

**วันนี้เราได้:** เข้าใจว่าโมเดลไฟล์เดียวไป Web/Cortex-A ได้ยังไง · ทำไมเบราว์เซอร์ต้องไฟล์ float I/O · reproduce front-end + วัด parity ด้วย `max-abs-diff`/TOL · เห็นว่า Cortex-A ใช้สคริปต์เดิม

> ชุดบทเรียนถัดไป (บทเรียน 5.8–5.9) เราจะพาโมเดลตัวเดียวกันนี้ไป **MCU ผ่าน Vela** แล้วเทียบทั้งสามเป้าหมาย (MCU/Web/Cortex-A) ด้าน latency/accuracy/power — ปิดวง "train once, run everywhere" ให้ครบ เจอกันครับ
