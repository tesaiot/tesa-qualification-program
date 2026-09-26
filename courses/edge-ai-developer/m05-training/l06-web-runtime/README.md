---
id: edgeai-dev.m05.l06
lang: th
title: {th: 'รันโมเดลบนเว็บ: LiteRT.js, int8 I/O และ parity', en: 'Running the model on the web: LiteRT.js, int8 I/O and parity'}
summary: {th: 'พาโมเดลตัวเดิมไปรันในเบราว์เซอร์ เลือก runtime อย่างมีเหตุผล (LiteRT.js, ONNX Runtime Web, tfjs-tflite, WebNN) เข้าใจกับดัก int8 I/O ที่ทำให้ต้องมีไฟล์ web อีกใบ front-end ที่อยู่นอกกราฟ คณิตของ quantize กับ dequantize และนิยาม parity ที่วัดด้วย max-abs-diff กับเกณฑ์ TOL', en: 'Take the same model into the browser. Choose a runtime with reasons (LiteRT.js, ONNX Runtime Web, tfjs-tflite, WebNN), understand the int8 I/O trap that calls for a second web file, the front-end that lives outside the graph, the maths of quantize and dequantize, and parity defined by max-abs-diff against a TOL.'}
level: L3
time_min: {concept: 50, practise: 10, check: 10}
hardware: {emulator: true, boards: [none]}
prerequisites: [edgeai-dev.m05.l05]
objectives:
  - {th: เปรียบเทียบ runtime บนเบราว์เซอร์สี่ตัวและให้เหตุผลการเลือกได้ รวมถึงอธิบายว่าทำไม BENTO Emulator จึงแปลงโมเดลเป็น ONNX แล้วรันด้วย ONNX Runtime Web, en: 'Compare four browser runtimes and justify a choice, including why the BENTO Emulator converts the model to ONNX and runs it with ONNX Runtime Web.'}
  - {th: อธิบายว่าทำไมโมเดล int8 เต็มของ MCU อาจต้องมีไฟล์ web อีกใบ และ convert_web.py สร้างไฟล์ weight-only int8 ที่ I/O เป็น float จากน้ำหนัก Keras ชุดเดียวกันอย่างไร, en: 'Explain why the MCU''s full-integer int8 model may need a second web file, and how convert_web.py builds a weight-only int8 file with float I/O from the same Keras weights.'}
  - {th: 'คำนวณ quantize q = clip(round(x/s + z), −128, 127) และ dequantize x̂ = (q − z)·s จากค่า scale และ zero-point ที่กำหนด', en: 'Compute quantize q = clip(round(x/s + z), −128, 127) and dequantize x̂ = (q − z)·s from a given scale and zero-point.'}
  - {th: ตัดสิน parity ด้วย d = max|s_pc − s_web| ≤ TOL และคลาสที่ชนะตรงกัน พร้อมอธิบายว่าทำไม d ไม่จำเป็นต้องเป็นศูนย์ และทำไม front-end คือจุดที่พังบ่อยที่สุด, en: 'Judge parity by d = max|s_pc − s_web| ≤ TOL with the same winning class, and explain why d need not be zero and why the front-end is where parity breaks most often.'}
develops: [{skill: ai.model-deploy, to: 3}, {skill: hw.math, to: 2}, {skill: ai.edge, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 5.6 — รันโมเดลบนเว็บ: LiteRT.js, int8 I/O และ parity

> โมดูล 5 — ฝึกโมเดลและนำไปใช้หลายเป้าหมาย · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

พาโมเดลตัวเดิมไปรันในเบราว์เซอร์ เลือก runtime อย่างมีเหตุผล (LiteRT.js, ONNX Runtime Web, tfjs-tflite, WebNN) เข้าใจกับดัก int8 I/O ที่ทำให้ต้องมีไฟล์ web อีกใบ front-end ที่อยู่นอกกราฟ คณิตของ quantize กับ dequantize และนิยาม parity ที่วัดด้วย max-abs-diff กับเกณฑ์ TOL

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เปรียบเทียบ runtime บนเบราว์เซอร์สี่ตัวและให้เหตุผลการเลือกได้ รวมถึงอธิบายว่าทำไม BENTO Emulator จึงแปลงโมเดลเป็น ONNX แล้วรันด้วย ONNX Runtime Web
2. อธิบายว่าทำไมโมเดล int8 เต็มของ MCU อาจต้องมีไฟล์ web อีกใบ และ convert_web.py สร้างไฟล์ weight-only int8 ที่ I/O เป็น float จากน้ำหนัก Keras ชุดเดียวกันอย่างไร
3. คำนวณ quantize q = clip(round(x/s + z), −128, 127) และ dequantize x̂ = (q − z)·s จากค่า scale และ zero-point ที่กำหนด
4. ตัดสิน parity ด้วย d = max|s_pc − s_web| ≤ TOL และคลาสที่ชนะตรงกัน พร้อมอธิบายว่าทำไม d ไม่จำเป็นต้องเป็นศูนย์ และทำไม front-end คือจุดที่พังบ่อยที่สุด

## ก่อนเริ่ม

ผ่านชุดบทเรียน 5.3–5.5 มาแล้ว มี `model_int8.tflite` กับ `model_int8.tflite.norm.npz` และถ้าจะทำไฟล์ web ให้รัน `train.py --save-keras` เพื่อได้ `model.keras`
เปิด BENTO Emulator เลือกโมเดล Motion แล้วเปิดสวิตช์ REAL ไว้ดูประกอบ

- **อุปกรณ์:** คอมพิวเตอร์ของคุณ ไม่ต้องใช้บอร์ด (หรือใช้ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) ประกอบ) — ใช้ PC และเบราว์เซอร์ BENTO Emulator ใช้ดูตัวอย่างโมเดลท่ามือที่รันจริงในเบราว์เซอร์
- **เรียนมาก่อน:** [บทเรียน 5.5 — ลงมือทำ: เติมสคริปต์ฝึกแล้วรันใน Docker](../l05-train-lab/README.md)

## ดูของจริงก่อน

ในแผง Edge AI ของ BENTO Emulator เลือกโมเดล Motion แล้วเปิดสวิตช์ REAL (ป้ายเปลี่ยนจาก MOCK เป็น REAL) แถบความมั่นใจสามคลาสจะขยับตาม IMU จำลอง
นี่คือโมเดลท่ามือที่ฝึกด้วย pipeline เดียวกับเรา รันในแท็บเบราว์เซอร์โดยไม่มีเซิร์ฟเวอร์ ถามตัวเองว่ามันรู้ mean/std กับ scale ของโมเดลได้อย่างไร

## แนวคิด

โมเดลในเบราว์เซอร์ไม่ต้องติดตั้งอะไร ส่งลิงก์ก็เห็น verdict ลองก่อน flash ได้ และข้อมูลไม่ออกจากเครื่องผู้ใช้ ผู้เขียนสำรวจ runtime ไว้ดังนี้:
**LiteRT.js** (`@litertjs/core`) โหลด `.tflite` ฟอร์แมตเดียวกับ MCU ผ่าน WASM หรือ WebGPU ด้วย `loadLiteRt()`, `loadAndCompile()` และ `run()` จึงเป็นตัวเลือกหลัก
`@tensorflow/tfjs-tflite` ไม่มีการพัฒนาต่อแล้ว **ONNX Runtime Web** โตเต็มที่และรองรับ int8 ดี แต่ต้องแปลง TFLite เป็น ONNX เพิ่มหนึ่งขั้น และ WebNN ยังไม่พร้อมใช้งานจริง
BENTO Emulator เลือกทางของ ONNX Runtime Web: แปลง `model_int8.tflite` ด้วย `tf2onnx` ครั้งเดียว (int8 in/out) แล้วทำ front-end เองใน JS

โมเดลของ MCU เป็น **full-integer int8** (int8 in/out) ตามที่ Ethos-U55 ต้องการ ผู้เขียนพบว่า LiteRT.js รับ I/O เป็น float32/int32 ไฟล์นี้จึงอาจโหลดไม่ได้
`convert_web.py` แก้ด้วยการแปลง **Keras ตัวเดิม** เป็น `model_web.tflite` แบบ dynamic-range (`Optimize.DEFAULT` โดยไม่มี representative dataset)
น้ำหนักเป็น int8 แต่ I/O เป็น float เล็กกว่า float ล้วนราวสี่เท่าและมาจากน้ำหนักชุดเดียวกับ MCU สิ่งที่ทำให้ไฟล์ "browser-clean" คือไม่มี custom op ของ NPU
ไฟล์ที่ผ่าน Vela แล้วจึงเก็บไว้ให้ MCU เท่านั้น

กราฟเห็นแค่ feature ที่เตรียมเสร็จแล้ว **front-end อยู่นอกกราฟ** ของเราคือ normalize ด้วย mean/std จาก `.norm.npz` (โมเดลเสียงหนักกว่านั้นมาก คือ FFT, Mel, log)
ไฟล์ int8 ต้อง quantize ขาเข้า $q = \mathrm{clip}(\mathrm{round}(x/s + z), -128, 127)$ และ dequantize ขาออก $\hat{x} = (q - z)\cdot s$ โดยอ่าน $s, z$ จากโมเดลเสมอ
**parity** คือการวัด ไม่ใช่ข้อสมมติ: เบราว์เซอร์ใช้ kernel ของ XNNPACK ส่วนบอร์ดใช้ CMSIS-NN ที่ไม่ bit-exact ต่อกัน เราจึงตัดสินด้วย
$d = \max_k |s^{pc}_k - s^{web}_k| \le \mathrm{TOL}$ (เช่น 0.02) และคลาสที่ชนะต้องตรงกัน ถ้าไม่ผ่าน เก้าในสิบครั้งปัญหาอยู่ที่ front-end โดยเฉพาะ normalization

## ตัวอย่างสมบูรณ์

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นหรือใน `shared/` ด้วย:

- [shared/training](../../shared/training)
- [shared/training/convert_web.py](../../shared/training/convert_web.py) — Prepare the trained model for the browser (BENTO Edge AI Emulator / any web page).
- [shared/training/eval_pc.py](../../shared/training/eval_pc.py) — Run the exported int8 .tflite on the PC and report accuracy + confusion.
- [shared/training/model_int8.tflite](../../shared/training/model_int8.tflite)
- [shared/training/train.py](../../shared/training/train.py) — Train a tiny IMU gesture classifier and export it as int8 TFLite.

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. ข้อได้เปรียบหลักของ LiteRT.js เหนือ ONNX Runtime Web ในคอร์สนี้คืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) เร็วกว่าเสมอทุกเครื่อง
   - ข) โหลด .tflite ฟอร์แมตเดียวกับ MCU ได้ตรง ๆ ไม่ต้องแปลงข้ามฟอร์แมต
   - ค) รองรับเฉพาะ int8
   - ง) ไม่ต้องทำ front-end

   <details><summary>เฉลย</summary>

   **ข** — ลดขั้นแปลงที่อาจทำให้เพี้ยน ส่วน ONNX Runtime Web ต้องแปลง TFLite เป็น ONNX ก่อน ซึ่งเป็นทางที่ BENTO Emulator เลือกเพื่อรันไฟล์ int8 in/out

   </details>

2. convert_web.py ตั้ง Optimize.DEFAULT โดยไม่ผูก representative dataset ได้ไฟล์แบบใด *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) full-integer int8 (int8 in/out)
   - ข) dynamic-range: น้ำหนัก int8 แต่ activation และ I/O เป็น float
   - ค) float16 ล้วน
   - ง) ไฟล์ที่ผ่าน Vela แล้ว

   <details><summary>เฉลย</summary>

   **ข** — ไม่มีตัวอย่างไว้ calibrate converter จึงบีบได้แค่น้ำหนัก ไฟล์เล็กลงราวสี่เท่าและ I/O ยังเป็น float ที่เบราว์เซอร์รับได้

   </details>

3. input มี scale s = 0.05 และ zero-point z = −10 ค่า x = 1.2 ถูก quantize เป็นเท่าไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) 14
   - ข) 24
   - ค) 34
   - ง) −10

   <details><summary>เฉลย</summary>

   **ก** — round(1.2 / 0.05 + (−10)) = round(24 − 10) = 14 และ dequantize กลับได้ (14 + 10) × 0.05 = 1.2

   </details>

4. s_pc = [0.10, 0.85, 0.05] และ s_web = [0.07, 0.88, 0.05] ด้วย TOL = 0.02 ผลเป็นอย่างไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) ผ่าน เพราะคลาสที่ชนะตรงกัน
   - ข) ไม่ผ่าน เพราะ d = 0.03 เกิน TOL แม้คลาสที่ชนะจะตรงกัน
   - ค) ผ่าน เพราะ d = 0.00
   - ง) ไม่ผ่าน เพราะคลาสที่ชนะต่างกัน

   <details><summary>เฉลย</summary>

   **ข** — ต้องผ่านทั้งสองเงื่อนไข d = max(0.03, 0.03, 0.00) = 0.03 > 0.02 จึงไม่ผ่าน ให้ไล่ตรวจ front-end ก่อน

   </details>

5. เบราว์เซอร์ทายคนละคลาสกับ PC เกือบทุก window ควรตรวจอะไรก่อน *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) kernel XNNPACK กับ CMSIS-NN
   - ข) normalization ว่าทั้งสองฝั่งใช้ mean/std ชุดเดียวกันจาก .norm.npz หรือไม่
   - ค) ความเร็วอินเทอร์เน็ต
   - ง) จำนวน epoch

   <details><summary>เฉลย</summary>

   **ข** — kernel ต่างกันทำให้คะแนนต่างเล็กน้อยสม่ำเสมอ แต่ถ้าคลาสเพี้ยนทั้งกระดาน front-end โดยเฉพาะ normalize มักเป็นต้นเหตุ

   </details>

## แล็บ

- [ ] เขียนตารางเปรียบเทียบ runtime สี่ตัวในบันทึกการเรียน พร้อมเหตุผลว่าคุณจะเลือกตัวใดสำหรับหน้าเว็บเดโมของคุณ
- [ ] ถ้าติดตั้ง Docker ไว้ รัน `train.py --save-keras` แล้ว `convert_web.py` เทียบขนาด `model_int8.tflite` กับ `model_web.tflite`
- [ ] คำนวณ quantize และ dequantize ของ x = 0.8 ด้วย s = 0.04, z = −5 แล้วดูว่าค่าที่ได้กลับมาคลาดจากเดิมเท่าไร

## ไปต่อ

บทเรียน 5.7 เราจะเติม `s13_web.py` ให้ครบสี่ขั้น สร้าง ground truth ฝั่ง PC วัด parity และฟังเรื่องราวของ Cortex-A

บทเรียนถัดไป: [บทเรียน 5.7 — ลงมือทำ: verdict บนเว็บให้ตรงกับ PC และเรื่องราว Cortex-A](../l07-web-parity-lab/README.md)

## สะท้อนคิด

- ถ้าต้องส่งเดโมให้ลูกค้าที่ไม่มีบอร์ด คุณจะเลือก runtime ใด และต้องส่งไฟล์อะไรไปบ้าง
- ทำไม "คลาสที่ชนะตรงกัน" อย่างเดียวจึงยังไม่พอเป็นหลักฐานของ parity
