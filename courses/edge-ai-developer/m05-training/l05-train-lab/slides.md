---
marp: true
theme: default
paginate: true
math: katex
lang: th
title: "บทเรียน 5.5 — ลงมือทำ: เติมสคริปต์ฝึกแล้วรันใน Docker"
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

# บทเรียน 5.5 — ลงมือทำ: เติมสคริปต์ฝึกแล้วรันใน Docker

## Training II · ฝึกโมเดลใน TensorFlow (Docker) แล้วทดสอบบน PC

**โมดูล 5 — ฝึกโมเดลและนำไปใช้หลายเป้าหมาย**

> ต่อจากบทเรียน 5.4 — ข้างในการฝึก: Keras, Conv1D, gradient descent, int8 และ confusion matrix

---

# โครงของไฟล์ s12_train.py — 4 ช่องที่ต้องเติม

ไฟล์ฝึก [`s12_train.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l05-train-lab/practice/s12_train.py) มีโครงครบทั้งไฟล์แล้ว เหลือ **4 จุด** ให้เติม ตรงกับสี่จังหวะพอดี:

<div style="text-align:center;margin:6px 0">
<svg width="900" height="180" viewBox="0 0 900 180" font-family="DejaVu Sans, sans-serif">
  <defs>
    <marker id="arF" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="10" refX="10" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#607d8b"/></marker>
  </defs>
  <rect x="14" y="40" width="200" height="70" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="114" y="66" font-size="13" font-weight="700" fill="#1565c0" text-anchor="middle">ช่อง 1 · fit</text>
  <text x="114" y="86" font-size="11" fill="#666" text-anchor="middle">model.fit(...)</text>
  <text x="114" y="102" font-size="10" fill="#999" text-anchor="middle">ในฟังก์ชัน main</text>
  <rect x="240" y="40" width="200" height="70" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="340" y="66" font-size="13" font-weight="700" fill="#2e7d32" text-anchor="middle">ช่อง 2 · repr set</text>
  <text x="340" y="86" font-size="11" fill="#666" text-anchor="middle">representative_dataset</text>
  <text x="340" y="102" font-size="10" fill="#999" text-anchor="middle">ใน to_int8_tflite</text>
  <rect x="466" y="40" width="200" height="70" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="566" y="66" font-size="13" font-weight="700" fill="#e65100" text-anchor="middle">ช่อง 3 · int8 I/O</text>
  <text x="566" y="86" font-size="11" fill="#666" text-anchor="middle">inference_input_type</text>
  <text x="566" y="102" font-size="10" fill="#999" text-anchor="middle">ใน to_int8_tflite</text>
  <rect x="692" y="40" width="196" height="70" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="790" y="66" font-size="13" font-weight="700" fill="#6a1b9a" text-anchor="middle">ช่อง 4 · accuracy</text>
  <text x="790" y="86" font-size="11" fill="#666" text-anchor="middle">(preds == yte).mean()</text>
  <text x="790" y="102" font-size="10" fill="#999" text-anchor="middle">ใน eval_int8</text>
  <line x1="214" y1="75" x2="238" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arF)"/>
  <line x1="440" y1="75" x2="464" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arF)"/>
  <line x1="666" y1="75" x2="690" y2="75" stroke="#607d8b" stroke-width="2.4" marker-end="url(#arF)"/>
  <text x="450" y="150" font-size="12" fill="#888" text-anchor="middle">ส่วนที่เหลือ (dataset_tools, build_model, quantize/dequantize) ให้ไว้แล้ว — อ่านให้เข้าใจ</text>
</svg>
</div>

> ทุกช่องมีคำใบ้ `# เติม:` พร้อมคำตอบเต็มในคอมเมนต์ ลองพิมพ์เองก่อน ถ้าติดค่อยเปิดเฉลย

---

# ไล่โค้ด (1) — ช่องเติม fit

**ช่องเติมที่ 1** อยู่ในฟังก์ชัน `main()` หลัง `compile` — จังหวะที่โมเดลเรียนรู้จริง:

```python
model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy", metrics=["accuracy"])

# ----- เติมช่องที่ 1 -----
# เติม: ฝึกโมเดลด้วยชุดฝึก และตรวจกับชุด val ทุก epoch
#       -> model.fit(Xtr, ytr, validation_data=(Xva, yva),
#                    epochs=a.epochs, batch_size=32, verbose=2)
pass

_, acc = model.evaluate(Xte, yte, verbose=0)   # วัด float32 บนชุดทดสอบ
```

- แทน `pass` ด้วย `model.fit(...)` ตามคำใบ้ — นี่คือบรรทัดที่ใช้เวลานานที่สุด (ฝึก 25 รอบ)
- ถ้าลืมเติม: โมเดลจะไม่เคยเรียนรู้ `evaluate` จะได้ accuracy ราวๆ 33% (เดามั่วใน 3 คลาส)
- `verbose=2` = พิมพ์หนึ่งบรรทัดต่อ epoch จะได้เห็น accuracy/val_accuracy ไต่ขึ้น

> สังเกตว่า `evaluate` (บรรทัดถัดมา) จะโชว์ความแม่นจริงก็ต่อเมื่อ `fit` ทำงานก่อน — ลืมช่องนี้ ตัวเลขทั้งหมดหลังจากนี้จะมั่ว

---

# ไล่โค้ด (2+3) — ช่องเติม int8

**ช่องเติมที่ 2 และ 3** อยู่ในฟังก์ชัน `to_int8_tflite()` — สองจังหวะที่แยก "โมเดล PC" ออกจาก "โมเดลลงชิป":

```python
conv = tf.lite.TFLiteConverter.from_keras_model(model)
conv.optimizations = [tf.lite.Optimize.DEFAULT]

# ----- เติมช่องที่ 2 -----
# เติม: -> conv.representative_dataset = representative
pass

conv.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]

# ----- เติมช่องที่ 3 -----
# เติม: -> conv.inference_input_type = tf.int8
#          conv.inference_output_type = tf.int8
pass
```

- ช่อง 2: แทน `pass` ด้วย `conv.representative_dataset = representative` (calibration — เห็นสไลด์ก่อนหน้า)
- ช่อง 3: แทน `pass` ด้วยสองบรรทัด บังคับ input/output เป็น int8
- ถ้าลืมช่อง 2: `conv.convert()` หยุดด้วย `ValueError` เพราะ full-integer ต้องมี representative dataset · ถ้าลืมช่อง 3: ขาเข้า/ขาออกของไฟล์ยังเป็น float32 ไม่ใช่สัญญา int8 ที่ต้องการ และ `eval_int8()` ที่ป้อน int8 จะรันไม่ผ่าน

> สองช่องนี้สั้นมาก แต่คือ **หัวใจของทั้ง Pillar 4** — ทำให้โมเดล 11 KB วิ่งบน NPU ได้จริง อ่านคอมเมนต์ในไฟล์ให้ครบก่อนเติม

---

# ไล่โค้ด (4) — ช่องเติม accuracy

**ช่องเติมที่ 4** อยู่ในฟังก์ชัน `eval_int8()` หลังลูปรันโมเดลครบทุกหน้าต่าง:

```python
    preds.append(int(o.argmax()))
preds = np.asarray(preds)

# ----- เติมช่องที่ 4 -----
# เติม: คำนวณความแม่นบนชุดทดสอบ (สัดส่วนที่ทายถูก)
#       -> acc = (preds == yte).mean()
acc = 0.0
pass
print("int8 test accuracy: %.3f" % acc)
```

- แทน `pass` ด้วย `acc = (preds == yte).mean()` — เทียบคำทายกับเฉลย นับสัดส่วนที่ตรง
- `preds == yte` ได้ array ของ True/False, `.mean()` ของ True/False = สัดส่วน True = ความแม่น
- ถ้าลืมเติม: `acc` ค้างที่ 0.0 รายงานจะบอก accuracy = 0 ทั้งที่โมเดลอาจทายถูกหมด

> นี่คือช่องเดียวกับที่ [`eval_pc.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/eval_pc.py) ทำ — คุณกำลังเขียนตัววัดผลด้วยมือ เข้าใจว่า "accuracy 1.000" มาจากไหนจริงๆ

---

# ลงมือทำ — เติม 4 ช่อง แล้วรันใน Docker

เปิด [`s12_train.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l05-train-lab/practice/s12_train.py) วางไว้ในโฟลเดอร์ [`shared/training/`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training) (ข้างๆ [`dataset_tools.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/dataset_tools.py)) แล้วเติมทีละช่อง:

| # | ฟังก์ชัน | เติมด้วย | ถ้าลืม |
|---|---|---|---|
| 1 | `main` | `model.fit(Xtr, ytr, validation_data=(Xva, yva), epochs=a.epochs, batch_size=32, verbose=2)` | accuracy ~33% (เดามั่ว) |
| 2 | `to_int8_tflite` | `conv.representative_dataset = representative` | `convert()` หยุดด้วย ValueError |
| 3 | `to_int8_tflite` | `conv.inference_input_type = tf.int8` (+output) | I/O ยังเป็น float32 — `eval_int8` ป้อน int8 ไม่ผ่าน |
| 4 | `eval_int8` | `acc = (preds == yte).mean()` | รายงาน accuracy = 0 |

ขั้นตอน:

1. เติมทั้ง 4 ช่อง ตามคำใบ้ `# เติม:` (ลบ `pass` แทนด้วยคำสั่งจริง)
2. `docker build -t edgeai-train .` (ครั้งเดียว) แล้ว `docker run --rm -v "$PWD":/work edgeai-train python s12_train.py`
3. ดูจนได้ `float32 test accuracy` → `int8 test accuracy` → confusion matrix + ไฟล์ [`model_int8.tflite`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/model_int8.tflite) โผล่มา

> สี่ช่องนี้คือสี่จังหวะของการฝึกเป๊ะ — เติมครบเมื่อไร คุณมีโมเดลของตัวเองพร้อมกระจายไปสี่เป้าหมายในชุดบทเรียนถัด ๆ ไป

---

# ปลายทางของไฟล์นี้ — รันได้จริงบน Emulator

[`model_int8.tflite`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/model_int8.tflite) ที่เราเพิ่งฝึกไม่ได้จบแค่ในไฟล์ **BENTO Edge AI Emulator** มีโมเดลท่ามือที่ฝึกด้วย pipeline เดียวกันนี้ติดมาแล้ว (แปลง `.tflite` เป็น ONNX ครั้งเดียว) เปิดสวิตช์ REAL ของโมเดล Motion ก็เห็นมันทายท่ามือ live บนหน้าจอเบราว์เซอร์ ชุดบทเรียนถัดไป (บทเรียน 5.6–5.7) เราจะดูว่าไฟล์ของเราเองไปถึงเบราว์เซอร์ได้อย่างไร

<div style="text-align:center;margin:8px 0">

![หน้า BENTO Playground บน Emulator ที่รันโมเดล Motion จริงผ่าน ONNX Runtime Web: คลาส idle 43% แถบความมั่นใจสามคลาส และเวลาอนุมาน 0.30 ms w:680](../../assets/img/edge_ai_real.png)

</div>

จอ emulator ที่รันได้จริง — โมเดลท่ามือ int8 ที่ฝึกด้วย pipeline เดียวกับวันนี้ ทำงานในเบราว์เซอร์ผ่าน ONNX Runtime Web

- บรรทัดบน = คลาสที่ชนะพร้อมความมั่นใจ, แถบสามแถบ = ความมั่นใจของแต่ละคลาส (จาก softmax), บรรทัดล่าง = เวลาอนุมานและ backend ที่ใช้
- นี่คือ "the one artifact → many targets" ที่จับต้องได้: ไฟล์ `.tflite` เดียวเป็นต้นทางของทั้งเบราว์เซอร์และบอร์ด
- วันนี้เราแค่สร้างไฟล์ + ทดสอบบน PC ให้แน่ใจก่อน ชุดบทเรียนถัดไปค่อยเอาขึ้นจอ emulator

> เห็นภาพปลายทางแล้วจะฝึกสนุกขึ้น — ถ้า front-end (normalize + quantize) ตรงกัน ไฟล์ที่ผ่าน [`eval_pc.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/eval_pc.py) จะตัดสินแบบเดียวกันในเบราว์เซอร์ นี่คือ parity ที่ชุดบทเรียนถัดไปจะพิสูจน์

---

# แหล่งเรียนรู้เพิ่มเติม

ถ้าอยากเข้าใจคณิตหลังฉากให้ลึกขึ้น สามคลิปนี้อธิบายด้วยภาพเคลื่อนไหวที่เข้าใจง่ายมาก:

**วิดีโอ**
- Neural network เรียนรู้ยังไง (gradient descent เชิงภาพ) — 3Blue1Brown: https://www.3blue1brown.com/lessons/gradient-descent
- Cross-entropy / softmax สำหรับงาน classification — StatQuest with Josh Starmer: https://www.youtube.com/@statquest
- convolution คืออะไร (สัญชาตญาณของการเลื่อน-คูณ-บวก) — 3Blue1Brown: https://www.3blue1brown.com/lessons/convolutions

**เอกสาร/ภาพอ้างอิง**
- Post-training quantization ฉบับทางการ — TensorFlow Lite docs: https://www.tensorflow.org/lite/performance/post_training_quantization
- ภาพ gradient descent ไต่ลงเนิน loss — https://commons.wikimedia.org/wiki/File:Gradient_descent.svg (ที่มา: Wikimedia Commons, CC BY-SA)
- บทความ convolution (นิยาม + แอนิเมชัน) — https://en.wikipedia.org/wiki/Convolution (ที่มา: Wikipedia, CC BY-SA)

> วิดีโอ/ภาพภายนอกเป็นของเจ้าของต้นฉบับ ใช้เพื่อการศึกษา อ้างอิงลิงก์ต้นทาง

---

# ชัยชนะที่เห็นได้ + MVP ของชุดบทเรียนนี้

<div style="text-align:center;margin:14px 0">
<div style="display:inline-block;background:#e8f5e9;border:2px solid #2e7d32;border-radius:22px;padding:10px 22px;color:#2e7d32;font-weight:700;font-size:1.05em">
ชัยชนะที่เห็นได้ของชุดบทเรียนนี้ · โมเดลที่คุณฝึกเอง ทายท่ามือของชุดทดสอบถูก พร้อมไฟล์ model_int8.tflite ในมือ
</div>
</div>

**MVP ของบทเรียน 5.3–5.5 (เกณฑ์ผ่านของชุดบทเรียน):** คุณฝึกโมเดล Keras ใน Docker ได้สำเร็จ แล้วได้ **รายงานความแม่น** ออกมา — `float32 accuracy`, `int8 accuracy`, และ confusion matrix บนชุดทดสอบที่โมเดลไม่เคยเห็น

- ได้ไฟล์ [`model_int8.tflite`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/model_int8.tflite) (int8 full-integer) + `model_int8.tflite.norm.npz` (mean/std)
- อธิบายได้ว่าโค้ดเรียก `fit` / `representative_dataset` / `inference_input_type` / accuracy ตรงไหน ทำอะไร

> "ฝึกได้" ไม่ใช่แค่ "เห็นตัวเลขวิ่ง" — คุณต้องบอกได้ว่าทำไม int8 accuracy ควรใกล้ float32 และ representative dataset มีไว้ทำอะไร

---

# บันไดช่วยเหลือ — ใบ้ → เริ่มจากโครง → เฉลย → ฉบับเต็ม

ถ้าติด ให้ไต่บันไดนี้ทีละขั้น อย่าเพิ่งกระโดดไปดูเฉลย เพราะของจะเข้าหัวตอนที่คุณพยายามเองก่อน:

- **ใบ้** — คำใบ้อยู่ในคอมเมนต์ `# เติม:` ทั้ง 4 จุดในไฟล์ฝึก + ตารางหน้าที่แล้ว บอกว่าแต่ละช่องเติมอะไร
- **เริ่มจากโครง** — [`s12_train.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l05-train-lab/practice/s12_train.py) มีโครงครบทั้งไฟล์แล้ว เหลือแค่ 4 จุดให้เติม (dataset/model/quantize ให้ไว้แล้ว)
- **เฉลย** — [`s12_train.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l05-train-lab/solution/s12_train.py) เติมครบพร้อมคอมเมนต์อธิบายทุกช่อง (อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์เอง)
- **ฉบับเต็ม** — [`s12_train_full.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l05-train-lab/examples/s12_train_full.py) ฉบับขัดเรียบร้อย เพิ่ม `synthesize` fallback + `model.summary()` + เกต MVP (เทียบ float32 vs int8 แล้วบอก PASS/NOT YET)

> ลองเขียนเองให้สุดก่อนนะ ถ้าติดจริงๆ ค่อยเปิดเฉลยดูทีละช่อง แล้วกลับมาพิมพ์เอง — เดี๋ยวเราค่อย ๆ แกะไปด้วยกัน

---

# เชื่อมโยงรากฐาน — วันนี้เราแตะอะไรไปบ้าง

การฝึกโมเดลตัวแรกซ่อนแนวคิด Edge AI หลายชั้นที่จะใช้ไปตลอด โมดูล 5 (Training) และ Apps:

**ฝั่ง Machine Learning / Training**
- **โครงโมเดลเล็ก** — Conv1D + pooling + dense ที่เล็กพอลง NPU (op ที่ Ethos-U55 เร่งได้)
- **train / val / test** — ฝึกด้วย train, จับ overfit ด้วย val, วัดผลจริงด้วย test (ชุดที่ไม่เคยเห็น)
- **int8 quantization + calibration** — บีบโมเดลด้วย representative dataset ให้ลงชิปได้โดยไม่เสียความแม่นมาก
- **confusion matrix** — อ่านว่าโมเดลสับสนคู่ไหน ไม่ใช่แค่ตัวเลข accuracy เดียว

**ฝั่ง วิศวกรรม / เครื่องมือ**
- **Docker** — สภาพแวดล้อมทำซ้ำได้ รันเหมือนกันทุก OS
- **the one artifact** — `.tflite` หนึ่งไฟล์ ที่ บทเรียน 5.6–5.9 จะกระจายไปสี่เป้าหมาย
- **normalization เป็นส่วนหนึ่งของโมเดล** — เซฟ mean/std ไว้ ไม่งั้นเกิดจุดพังเงียบ

> ทั้งหมดนี้ยืนบนสี่จังหวะ `build → fit → convert → eval` — พลังของ "train once, run everywhere" คือคุณสร้างชิ้นงานเดียวในชุดบทเรียนนี้ แล้วเอาไปได้ทั้งบอร์ด เบราว์เซอร์ และ Cortex-A

---

# ใช้จริงที่ไหน — training pipeline ในโลกจริง

โฟลว์ที่เราทำวันนี้ (เก็บข้อมูล → ฝึกใน container → บีบ int8 → ทดสอบ) ไม่ใช่ของเล่น มันคือ **workflow มาตรฐานของทีม Edge AI จริง**

<div style="text-align:center;margin:6px 0">
<svg width="880" height="200" viewBox="0 0 880 200" font-family="DejaVu Sans, sans-serif">
  <rect x="12" y="10" width="420" height="86" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="28" y="34" font-size="13" font-weight="700" fill="#1565c0">Reproducible training (Docker/CI)</text>
  <text x="28" y="56" font-size="11" fill="#555">ทีมฝึกโมเดลในกล่องเดียวกัน ผลตรงกันเป๊ะ</text>
  <text x="28" y="76" font-size="11" fill="#555">รันบน CI ได้ ฝึกใหม่อัตโนมัติเมื่อข้อมูลเพิ่ม</text>
  <text x="28" y="92" font-size="11" fill="#888">เหมือน MLOps pipeline จริงในบริษัท</text>
  <rect x="448" y="10" width="420" height="86" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="464" y="34" font-size="13" font-weight="700" fill="#2e7d32">int8 quantization (ทุกงาน on-device)</text>
  <text x="464" y="56" font-size="11" fill="#555">คำสั่งเสียง · กล้อง AI · wearable ตรวจการล้ม</text>
  <text x="464" y="76" font-size="11" fill="#555">ทุกตัวบีบ int8 เพื่อลง MCU/NPU เหมือนเรา</text>
  <text x="464" y="92" font-size="11" fill="#888">representative dataset = ขั้นบังคับในงานจริง</text>
  <rect x="12" y="106" width="420" height="84" rx="10" fill="#fff3e0" stroke="#ef6c00" stroke-width="2"/>
  <text x="28" y="130" font-size="13" font-weight="700" fill="#e65100">held-out test = ป้องกันหลอกตัวเอง</text>
  <text x="28" y="152" font-size="11" fill="#555">วัดผลบนชุดที่โมเดลไม่เคยเห็น ค่าที่เชื่อได้</text>
  <text x="28" y="172" font-size="11" fill="#555">confusion matrix บอกว่าเก็บข้อมูลเพิ่มตรงไหน</text>
  <rect x="448" y="106" width="420" height="84" rx="10" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="464" y="130" font-size="13" font-weight="700" fill="#6a1b9a">the one artifact → many targets</text>
  <text x="464" y="152" font-size="11" fill="#555">.tflite เดียว ไป MCU/Web/Cortex-A</text>
  <text x="464" y="172" font-size="11" fill="#555">คือ 5.6–5.9 ของเรา (Web แล้วบอร์ด)</text>
</svg>
</div>

> โมเดลที่คุณฝึกวันนี้แก้โจทย์เดียวกับโมเดล Motion ที่ติดมากับบอร์ดตั้งแต่ บทเรียน 1.1–1.3 — ต่างกันแค่ตัวนี้ **คุณฝึกเอง** เข้าใจทุกจังหวะ นี่คือความหมายของการ "ถอยกลับไปสร้างต้นทางเอง"

---

# งานทำเอง + สรุปบทเรียน

**งานทำเอง (ท้ายบทเรียน):**

1. เติม [`s12_train.py`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/m05-training/l05-train-lab/practice/s12_train.py) ให้ครบทั้ง 4 ช่อง รันใน Docker จนได้ [`model_int8.tflite`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/model_int8.tflite) + รายงานความแม่น
2. ลองลด `--epochs` เหลือ 3 แล้วรันใหม่ เทียบ accuracy กับตอน 25 epoch — จดว่าต่างกันแค่ไหน เพราะอะไร
3. ลองให้ `representative()` ป้อนหน้าต่างศูนย์ล้วน (`np.zeros_like(X_repr[i:i + 1])`) แทนหน้าต่างจริง แล้วรันใหม่ ดูว่า int8 accuracy เปลี่ยนไหม อธิบายว่าทำไม

ใบ้ข้อ 3 — converter วัดช่วงค่า activation จากตัวอย่างที่ป้อน ถ้าตัวอย่างไม่เหมือนข้อมูลจริง สเกล int8 จะไม่พอดี ความแม่นบน int8 มักตกจาก float32 ให้เห็น (ส่วนการลบบรรทัดช่อง 2 ทิ้งไปเลย `convert()` จะหยุดด้วย ValueError)

**วันนี้เราได้:** เข้าใจว่าทำไมฝึกใน Docker · เดินครบสี่จังหวะ `build → fit → convert → eval` · รู้ว่า int8 + representative dataset สำคัญยังไง · ฝึกโมเดลของตัวเองแล้วอ่าน accuracy + confusion matrix เป็น

> ชุดบทเรียนถัดไป (บทเรียน 5.6–5.7) เราจะเอาไฟล์ [`model_int8.tflite`](https://github.com/tesaiot/tesa-qualification-program/blob/main/courses/edge-ai-developer/shared/training/model_int8.tflite) เดียวกันนี้ไป **รันในเบราว์เซอร์** (BENTO Edge AI Emulator) แล้วเล่าเรื่องการเอาไปรันบน Cortex-A (Raspberry Pi/Jetson) — ไฟล์เดิม ไม่แก้ เจอกันครับ
