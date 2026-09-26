---
id: edgeai-dev.m05.l07
lang: th
title: {th: 'ลงมือทำ: verdict บนเว็บให้ตรงกับ PC และเรื่องราว Cortex-A', en: 'Hands-on: a web verdict that matches the PC, and the Cortex-A story'}
summary: {th: 'เติมห้าจุดใน s13_web.py ให้ทำสี่ขั้นเดียวกับที่เบราว์เซอร์ทำ คือ normalize, quantize, invoke และ dequantize จนได้ verdict ฝั่ง PC เป็น ground truth แล้ววัด parity กับไฟล์ web ด้วย max-abs-diff ปิดด้วยเรื่องราว Cortex-A ที่รัน eval_pc.py ตัวเดิมได้เลย และการเลือกเป้าหมายอย่างมีเหตุผล', en: 'Fill five points in s13_web.py so it performs the same four steps as the browser (normalize, quantize, invoke, dequantize) and gives a PC verdict as ground truth, then measure parity against the web file with max-abs-diff. Close with the Cortex-A story, where the same eval_pc.py simply runs, and choosing a target with reasons.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [none]}
prerequisites: [edgeai-dev.m05.l06]
objectives:
  - {th: เติมห้าจุดใน practice/s13_web.py จนพิมพ์ verdict ฝั่ง PC ที่ conf เท่ากับคะแนนสูงสุดใน scores และ scores รวมกันได้ราว 1, en: Fill the five points in practice/s13_web.py until it prints a PC verdict whose conf equals the highest score and whose scores sum to about 1.}
  - {th: วัด parity อย่างน้อยหนึ่ง window (ด้วย s13_web_full.py บน PC หรือหน้าเว็บที่โหลด LiteRT.js) จดค่า max-abs-diff กับคลาสที่ชนะ แล้วตัดสินผ่านหรือไม่ผ่านตาม TOL = 0.02, en: 'Measure parity for at least one window (with s13_web_full.py on the PC or a web page running LiteRT.js), record max-abs-diff and the winning class, and judge pass or fail against TOL = 0.02.'}
  - {th: 'เลือกเป้าหมาย (MCU, Web, Cortex-A หรือ PC) ให้โจทย์ที่กำหนดพร้อมข้อแลกเปลี่ยนอย่างน้อยสองข้อ และอธิบายว่าทำไม eval_pc.py รันบน Cortex-A ได้โดยไม่แก้', en: 'Choose a target (MCU, web, Cortex-A or PC) for a given scenario with at least two trade-offs, and explain why eval_pc.py runs on Cortex-A unchanged.'}
develops: [{skill: ai.model-deploy, to: 3}, {skill: lang.python, to: 2}, {skill: ai.edge, to: 2}]
assesses: [{skill: ai.model-deploy, level: 2, evidence: practice/s13_web.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 5.7 — ลงมือทำ: verdict บนเว็บให้ตรงกับ PC และเรื่องราว Cortex-A

> โมดูล 5 — ฝึกโมเดลและนำไปใช้หลายเป้าหมาย · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เติมห้าจุดใน s13_web.py ให้ทำสี่ขั้นเดียวกับที่เบราว์เซอร์ทำ คือ normalize, quantize, invoke และ dequantize จนได้ verdict ฝั่ง PC เป็น ground truth แล้ววัด parity กับไฟล์ web ด้วย max-abs-diff ปิดด้วยเรื่องราว Cortex-A ที่รัน eval_pc.py ตัวเดิมได้เลย และการเลือกเป้าหมายอย่างมีเหตุผล

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เติมห้าจุดใน practice/s13_web.py จนพิมพ์ verdict ฝั่ง PC ที่ conf เท่ากับคะแนนสูงสุดใน scores และ scores รวมกันได้ราว 1
2. วัด parity อย่างน้อยหนึ่ง window (ด้วย s13_web_full.py บน PC หรือหน้าเว็บที่โหลด LiteRT.js) จดค่า max-abs-diff กับคลาสที่ชนะ แล้วตัดสินผ่านหรือไม่ผ่านตาม TOL = 0.02
3. เลือกเป้าหมาย (MCU, Web, Cortex-A หรือ PC) ให้โจทย์ที่กำหนดพร้อมข้อแลกเปลี่ยนอย่างน้อยสองข้อ และอธิบายว่าทำไม eval_pc.py รันบน Cortex-A ได้โดยไม่แก้

## ก่อนเริ่ม

ผ่านบทเรียน 5.6 มาแล้ว เข้าใจ quantize, dequantize และนิยาม parity
คัดลอก `practice/s13_web.py` ไปวางใน [`shared/training`](../../shared/training/) ที่มี `dataset_tools.py`, `model_int8.tflite` และ `.norm.npz`

- **อุปกรณ์:** คอมพิวเตอร์ของคุณ ไม่ต้องใช้บอร์ด (หรือใช้ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) ประกอบ) — ใช้ PC (Python กับ ai-edge-litert หรือ Docker image เดิม) การเทียบในเบราว์เซอร์ต้องทำหน้าเว็บของคุณเองที่โหลด LiteRT.js เพราะ BENTO Emulator โหลดไฟล์ของเราเองไม่ได้
- **เรียนมาก่อน:** [บทเรียน 5.6 — รันโมเดลบนเว็บ: LiteRT.js, int8 I/O และ parity](../l06-web-runtime/README.md)

## แนวคิด

`web_verdict()` เดินสี่ขั้นเดียวกับที่หน้าเว็บต้องทำ ห้าจุดที่เติมคือ (1) `x = (window - z["mean"]) / z["std"]` normalize ด้วยชุดเดียวกับตอนฝึก
(2) `q = np.clip(np.round(x / in_scale + in_zero), -128, 127).astype(np.int8)` โดยอ่าน scale/zero จาก `inp["quantization"]`
(3) `it.set_tensor(inp["index"], q)` แล้ว `it.invoke()` (4) `o = (o - out_zero) * out_scale` ให้ softmax กลับเป็นความน่าจะเป็น และ
(5) `conf = float(o[top])` ผลคืน dict `{label, top, conf, scores}` หน้าตาเดียวกับที่ฝั่ง JS (`webVerdict`) คืน ฝั่ง JS ใช้ไฟล์ web ที่ I/O เป็น float
จึงข้ามขั้น quantize และ dequantize ส่วนขั้น normalize ต้องเป็นสูตรเดียวกันทุกตัวอักษร

ground truth ฝั่ง PC คือ `python s13_web.py` จากนั้นวัด parity: `s13_web_full.py --export-web` สร้าง `model_web.tflite` จาก `model.keras`
แล้ว `python s13_web_full.py` รันไฟล์ int8 กับไฟล์ web บนชุดทดสอบ 12 window พิมพ์ max-abs-diff และคลาสที่ชนะ นี่คือด่านแรกบน PC
ขั้นถัดไปคือหน้าเว็บของคุณที่โหลด LiteRT.js ด้วยโค้ดจาก `--show-js` ถ้าไม่ผ่าน ไล่ตามลำดับ: normalize → quantize → invoke ก่อนโทษ kernel
วิธีดีบักที่เร็วที่สุดคือป้อน input ชุดเดียวกันเป๊ะแล้วเทียบผลทีละขั้น จุดที่เริ่มต่างคือจุดที่ front-end ไม่ตรง

**Cortex-A** ง่ายที่สุด: `pip install ai-edge-litert` บน Raspberry Pi หรือ Jetson แล้วรัน `eval_pc.py` กับไฟล์ `.tflite` เดิมได้เลย เพราะมี Linux และ Python จริง
ไม่มีข้อจำกัด int8 แบบ NPU และเร่งต่อได้ด้วย delegate (XNNPACK บน CPU, GPU delegate บน Jetson) การเลือกเป้าหมายคือการแลก:
MCU เล็กและประหยัดไฟที่สุดแต่แปลงยากสุด Web แชร์ได้ทันทีแต่ต้องทำ front-end ใน JS Cortex-A แรงและยืดหยุ่น PC คือโต๊ะฝึกและ ground truth

## ตัวอย่างสมบูรณ์

`s13_web_full.py` คือแล็บ parity ครบวงบน PC: `--export-web` สร้างไฟล์ web จาก `model.keras` (ได้จาก `train.py --save-keras`), รันเฉย ๆ
เทียบไฟล์ int8 กับไฟล์ web 12 window แล้วสรุปผ่านหรือไม่ผ่าน และ `--show-js` พิมพ์โค้ด LiteRT.js ไปวางในหน้าเว็บ
ข้อควรรู้: ตัวเลือก `--index` ของไฟล์ฝึกยังไม่ได้ถูกใช้ สคริปต์หยิบ window ทดสอบตัวแรกเสมอ

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/s13_web_full.py](examples/s13_web_full.py) | แล็บ parity ครบวง: PC vs Web จากโมเดล .tflite ไฟล์เดียว (ฉบับเต็ม) |

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นหรือใน `shared/` ด้วย:

- [shared/training](../../shared/training)
- [shared/training/convert_web.py](../../shared/training/convert_web.py) — Prepare the trained model for the browser (BENTO Edge AI Emulator / any web page).
- [shared/training/dataset_tools.py](../../shared/training/dataset_tools.py) — Dataset tools for the IMU gesture classifier (Pillar 4 / Training).
- [shared/training/eval_pc.py](../../shared/training/eval_pc.py) — Run the exported int8 .tflite on the PC and report accuracy + confusion.
- [shared/training/model_int8.tflite](../../shared/training/model_int8.tflite)
- [shared/training/train.py](../../shared/training/train.py) — Train a tiny IMU gesture classifier and export it as int8 TFLite.

## ฝึกเติม

คอมเมนต์ `# เติม` อยู่ที่บรรทัด 38 (normalize), 50 (quantize), 55 (invoke), 60 (dequantize) และ 65 (conf)
ถ้า conf เป็น 0.0000 จุดที่ 65 ยังว่าง ถ้า scores เป็นเลขจำนวนเต็มอย่าง −128 หรือ 127 จุดที่ 60 ยังว่าง

| ไฟล์ฝึก | เรื่อง |
|---|---|
| [practice/s13_web.py](practice/s13_web.py) | เอาโมเดลของเราลง Web แล้วทวนผลให้ตรงกับ PC (ฉบับฝึกเติมโค้ด) |

## เฉลย

เปิดเฉลยหลังจากลองเองแล้วอย่างน้อยหนึ่งรอบ และอ่าน [วิธีใช้เฉลย](../../README.md#วิธีใช้เฉลย) ก่อน

| เฉลย | คู่กับ |
|---|---|
| [solution/s13_web.py](solution/s13_web.py) | [practice/s13_web.py](practice/s13_web.py) |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. รันแล้ว scores ดูถูกต้องแต่ conf = 0.0000 ทุกครั้ง จุดใดยังว่าง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) เติม 1 normalize
   - ข) เติม 3 invoke
   - ค) เติม 4 dequantize
   - ง) เติม 5 conf = float(o[top])

   <details><summary>เฉลย</summary>

   **ง** — placeholder conf = 0.0 ค้างอยู่ ต้องดึงคะแนนของคลาสที่ชนะออกมาด้วย float(o[top])

   </details>

2. scores ออกมาเป็น ['-128.0000', '127.0000', '-128.0000'] จุดใดยังว่าง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) เติม 2 quantize
   - ข) เติม 4 dequantize ค่ายังเป็น int8 ดิบ ไม่ใช่ความน่าจะเป็น
   - ค) เติม 1 normalize
   - ง) ไม่มีจุดใดผิด

   <details><summary>เฉลย</summary>

   **ข** — ต้องแปลงกลับด้วย (o − out_zero) × out_scale ค่าจึงอยู่ในช่วง 0..1 และรวมกันได้ราว 1

   </details>

3. s13_web_full.py รายงานคลาสที่ชนะตรงกัน 12/12 window และ max-abs-diff สูงสุด 0.0117 ที่ TOL 0.02 สรุปอย่างไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) ผ่านบน PC แล้ว ขั้นต่อไปคือยืนยันในเบราว์เซอร์จริง
   - ข) ไม่ผ่าน เพราะ diff ไม่เป็นศูนย์
   - ค) ผ่าน และไม่ต้องทดสอบที่ไหนอีก
   - ง) ไม่ผ่าน เพราะต้องได้ 100%

   <details><summary>เฉลย</summary>

   **ก** — ครบทั้งสองเงื่อนไข แต่ s13_web_full.py รันไฟล์ web ด้วย interpreter บน PC จึงเป็นด่านแรก เบราว์เซอร์จริงอาจใช้ kernel ต่างกันจึงควรยืนยันซ้ำ

   </details>

4. ต้องส่งเดโมให้ลูกค้าเปิดดูทันทีโดยไม่ติดตั้งอะไรและไม่มีบอร์ด ควรเลือกเป้าหมายใด *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) MCU + Ethos-U55
   - ข) Web ในเบราว์เซอร์
   - ค) Cortex-A
   - ง) PC ใน Docker

   <details><summary>เฉลย</summary>

   **ข** — เว็บแชร์ด้วยลิงก์ได้ทันทีและข้อมูลอยู่ในเครื่องผู้ใช้ แลกกับการต้องทำ front-end ใน JS และวัด parity เอง

   </details>

5. ทำไม eval_pc.py จึงรันบน Raspberry Pi ได้โดยไม่แก้แม้แต่บรรทัดเดียว *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) เพราะ Raspberry Pi มี Ethos-U55
   - ข) เพราะ Cortex-A มี Linux กับ Python จริง ติดตั้ง ai-edge-litert ได้ และใช้ไฟล์ .tflite เดิมโดยไม่บังคับ int8
   - ค) เพราะ eval_pc.py ถูกคอมไพล์เป็นภาษา C
   - ง) เพราะใช้ Vela

   <details><summary>เฉลย</summary>

   **ข** — Cortex-A คือ PC ตัวเล็กที่มีระบบปฏิบัติการเต็ม สคริปต์และไฟล์โมเดลชุดเดียวกับบน PC จึงย้ายไปได้ทันที

   </details>

## แล็บ

**MVP ของชุดบทเรียน 5.6–5.7:** verdict ของไฟล์ web ตรงกับฝั่ง PC ภายในเกณฑ์ (max|score_pc − score_web| ≤ TOL และคลาสที่ชนะตรงกัน) พร้อมอธิบายได้ว่าทำไมไม่จำเป็นต้องเท่ากันทุกบิต

- [ ] เติมไฟล์ฝึกครบห้าจุด รัน `python s13_web.py` แล้วจด label, conf และ scores ลงบันทึกการเรียน
- [ ] รัน `s13_web_full.py --export-web` แล้ว `s13_web_full.py` จด max-abs-diff สูงสุดและจำนวน window ที่คลาสตรงกัน
- [ ] ปิด normalize ฝั่งใดฝั่งหนึ่งชั่วคราว แล้วดูว่า max-abs-diff พุ่งขึ้นแค่ไหน
- [ ] ถ้าทำได้ ยืนยันอย่างน้อยหนึ่ง window ในหน้าเว็บที่โหลด LiteRT.js ด้วยโค้ดจาก `--show-js`

## ไปต่อ

ชุดบทเรียนถัดไป (บทเรียน 5.8–5.9) เราจะพาโมเดลเดียวกันไป MCU ผ่าน Vela แล้วเทียบสามเป้าหมายด้าน latency, accuracy และพลังงาน

บทเรียนถัดไป: [บทเรียน 5.8 — quantize และ Vela: เอาโมเดลของเราขึ้น Ethos-U55](../l08-quantize-and-vela/README.md)

## สะท้อนคิด

- ถ้าคุณต้องทำเดโมเสียงแทน IMU front-end ฝั่ง JS จะยากขึ้นตรงไหน
- ในงานของคุณ TOL เท่าไรจึงยอมรับได้ และใครควรเป็นคนตัดสินเกณฑ์นั้น
