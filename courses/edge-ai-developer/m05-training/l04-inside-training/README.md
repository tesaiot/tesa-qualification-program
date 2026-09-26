---
id: edgeai-dev.m05.l04
lang: th
title: {th: 'ข้างในการฝึก: Keras, Conv1D, gradient descent, int8 และ confusion matrix', en: 'Inside training: Keras, Conv1D, gradient descent, int8 and the confusion matrix'}
summary: {th: 'เปิด train.py แกะสี่จังหวะ build, fit, convert และ eval พร้อมคณิตเบื้องหลัง ได้แก่สมการ Conv1D, softmax, cross-entropy, gradient descent และการบีบ int8 ด้วย scale กับ zero-point รู้ว่าทำไม representative dataset จำเป็น ทำไม normalization เป็นส่วนหนึ่งของโมเดล และอ่าน learning curve กับ confusion matrix ให้เป็น', en: 'Open train.py and take apart its four beats (build, fit, convert, eval) with the maths behind them - the Conv1D equation, softmax, cross-entropy, gradient descent and int8 quantization with scale and zero-point. Learn why the representative dataset is required, why normalization is part of the model, and how to read learning curves and a confusion matrix.'}
level: L3
time_min: {concept: 50, practise: 10, check: 10}
hardware: {emulator: false, boards: [none]}
prerequisites: [edgeai-dev.m05.l03]
objectives:
  - {th: 'คำนวณค่าออกของ Conv1D หนึ่งตำแหน่งด้วยมือจาก y[t] = Σ w[k]·x[t+k] + b และนับจำนวนพารามิเตอร์ของชั้น Conv1D กับ Dense ได้', en: 'Compute one Conv1D output by hand with y[t] = Σ w[k]·x[t+k] + b, and count the parameters of a Conv1D and a Dense layer.'}
  - {th: คำนวณ softmax ของคะแนนสามคลาส และแปลความ learning curve ว่าเป็นแบบดี overfit หรือ underfit, en: 'Compute the softmax of three class scores, and interpret a learning curve as healthy, overfitting or underfitting.'}
  - {th: อธิบายการบีบ int8 แบบ full-integer ด้วย real ≈ scale × (q − zero_point) และบอกหน้าที่ของ representative_dataset กับ inference_input_type, en: 'Explain full-integer int8 quantization with real ≈ scale × (q − zero_point), and state the job of representative_dataset and inference_input_type.'}
  - {th: อ่าน confusion matrix แล้วคำนวณความแม่นและระบุคู่คลาสที่โมเดลสับสนได้, en: 'Read a confusion matrix, compute the accuracy and name the pair of classes the model confuses.'}
develops: [{skill: ai.model-training, to: 3}, {skill: hw.math, to: 3}, {skill: ai.model-deploy, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 5.4 — ข้างในการฝึก: Keras, Conv1D, gradient descent, int8 และ confusion matrix

> โมดูล 5 — ฝึกโมเดลและนำไปใช้หลายเป้าหมาย · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เปิด train.py แกะสี่จังหวะ build, fit, convert และ eval พร้อมคณิตเบื้องหลัง ได้แก่สมการ Conv1D, softmax, cross-entropy, gradient descent และการบีบ int8 ด้วย scale กับ zero-point รู้ว่าทำไม representative dataset จำเป็น ทำไม normalization เป็นส่วนหนึ่งของโมเดล และอ่าน learning curve กับ confusion matrix ให้เป็น

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. คำนวณค่าออกของ Conv1D หนึ่งตำแหน่งด้วยมือจาก y[t] = Σ w[k]·x[t+k] + b และนับจำนวนพารามิเตอร์ของชั้น Conv1D กับ Dense ได้
2. คำนวณ softmax ของคะแนนสามคลาส และแปลความ learning curve ว่าเป็นแบบดี overfit หรือ underfit
3. อธิบายการบีบ int8 แบบ full-integer ด้วย real ≈ scale × (q − zero_point) และบอกหน้าที่ของ representative_dataset กับ inference_input_type
4. อ่าน confusion matrix แล้วคำนวณความแม่นและระบุคู่คลาสที่โมเดลสับสนได้

## ก่อนเริ่ม

ผ่านบทเรียน 5.3 มาแล้ว เคยรัน `train.py` และเห็น log ของมัน
เปิด [`train.py`](../../shared/training/train.py) คู่กับสไลด์ และถ้ามีเวลา ดาวน์โหลด [`math_lab.html`](../../shared/interactive/math_lab.html) มาเปิดในเบราว์เซอร์ (ต้องต่อเน็ตเพื่อโหลด GeoGebra)

- **อุปกรณ์:** คอมพิวเตอร์ของคุณ ไม่ต้องใช้บอร์ด — ใช้ PC อ่านโค้ดคู่กับสไลด์ ถ้ามีเวลา ดาวน์โหลด math_lab.html มาเปิดในเบราว์เซอร์เพื่อเลื่อนกราฟเล่น
- **เรียนมาก่อน:** [บทเรียน 5.3 — ฝึกโมเดลใน Docker: หนึ่งชิ้นงาน สี่เป้าหมาย](../l03-training-pipeline/README.md)

## แนวคิด

`train.py` อ่านเป็นสี่จังหวะ **build → fit → convert → eval** จังหวะ build วางโมเดล 1-D CNN ด้วย `tf.keras.Sequential`: input `(50, 6)`
→ `Conv1D(16, 5)` → `MaxPooling1D(2)` → `Conv1D(32, 3)` → `GlobalAveragePooling1D` → `Dense(32)` → `Dense(3, softmax)` ทุกชั้นเป็น op ที่ Ethos-U55 เร่งได้
รวมราว 3,200 พารามิเตอร์ (Conv1D แรก 5·6·16 + 16 = 496) Conv1D คือ $y[t] = \sum_{k=0}^{K-1} w[k]\,x[t+k] + b$ filter หนึ่งอันเลื่อนไปตามเวลา
ค่าออกสูงเมื่อช่วงนั้นหน้าตาเหมือน filter เช่น kernel `[.2 .5 .3]` บน `.1 .4 .8` ได้ `.46` (b = 0)

จังหวะ fit วนสามสมการทุก batch: **softmax** $\hat{y}_i = e^{z_i}/\sum_j e^{z_j}$ เปลี่ยนคะแนนดิบเป็นความน่าจะเป็นที่รวมกันได้ 1
**cross-entropy** $L = -\sum_i y_i \log \hat{y}_i$ วัดว่าทายห่างเฉลยแค่ไหน และ **gradient descent** $\theta \leftarrow \theta - \eta\,\nabla_\theta L$
ขยับน้ำหนักลงเนินของ loss (`adam` คือ optimizer ตระกูลนี้) `epochs=25`, `batch_size=32` และ `validation_data` ให้เราอ่าน learning curve:
`accuracy` กับ `val_accuracy` ขึ้นด้วยกันคือดี train สูงแต่ val ต่ำหรือตกคือ overfit ทั้งคู่ต่ำค้างคือ underfit

จังหวะ convert บีบ float32 เป็น **int8** ด้วย $real \approx scale \times (q - zero\_point)$ เล็กลงราวสี่เท่าและ NPU เร่งได้ converter ต้อง
**calibrate** ช่วงค่าของ activation จาก `representative_dataset` (หน้าต่างจริงจากชุดฝึก 200 อัน) ถ้าตั้ง `TFLITE_BUILTINS_INT8` แต่ไม่ผูกชุดนี้
`convert()` จะหยุดด้วย `ValueError` ส่วน `inference_input_type = tf.int8` และ `inference_output_type = tf.int8` ทำให้ขาเข้าขาออกเป็น int8 ล้วน
mean/std ของการ normalize ถูกเซฟลง `.norm.npz` เพราะ normalization เป็นส่วนหนึ่งของโมเดล ฝั่งที่ใช้ต้องใช้ค่าเดียวกัน จังหวะ eval quantize input
ด้วย scale/zero-point ของไฟล์ รัน แล้ว dequantize ขาออกก่อน `argmax` ผลสรุปเป็น **confusion matrix** แถวคือคลาสจริง คอลัมน์คือคลาสที่ทาย
แนวทแยงคือทายถูก ช่องนอกแนวทแยงบอกว่าต้องเก็บข้อมูลเพิ่มที่คู่ไหน

## ตัวอย่างสมบูรณ์

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นหรือใน `shared/` ด้วย:

- [m05-training/l05-train-lab/practice/s12_train.py](../l05-train-lab/practice/s12_train.py) — ฝึกโมเดลของเราเองด้วย TensorFlow แล้วทดสอบบน PC (ฉบับฝึกเติมโค้ด)
- [shared/interactive/math_lab.html](../../shared/interactive/math_lab.html)
- [shared/training/train.py](../../shared/training/train.py) — Train a tiny IMU gesture classifier and export it as int8 TFLite.

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. kernel w = [.2, .5, .3] และ b = 0 บนสัญญาณ .4 .8 .6 ได้ค่าออกเท่าไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) 0.46
   - ข) 0.52
   - ค) 0.66
   - ง) 1.80

   <details><summary>เฉลย</summary>

   **ค** — .2×.4 + .5×.8 + .3×.6 = .08 + .40 + .18 = .66 คือการคูณแล้วบวกทีละตำแหน่ง

   </details>

2. คะแนนดิบ z = [2.0, 3.1, 1.2] ของ idle, circle, shaking หลัง softmax circle ได้ความน่าจะเป็นราวเท่าไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) 0.31
   - ข) 0.49
   - ค) 0.67
   - ง) 1.00

   <details><summary>เฉลย</summary>

   **ค** — e^3.1 ≈ 22.2 หารด้วย e^2.0 + e^3.1 + e^1.2 ≈ 7.39 + 22.2 + 3.32 ≈ 32.9 ได้ราว 0.67 ส่วน idle ราว 0.22 และ shaking ราว 0.10

   </details>

3. ฝึกจบแล้ว accuracy = 0.99 แต่ val_accuracy = 0.60 และตกลงเรื่อย ๆ ในช่วงท้าย แปลว่าอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) โมเดลดีมาก
   - ข) overfit โมเดลจำชุดฝึกแต่ไม่ generalize
   - ค) underfit โมเดลเล็กเกินไป
   - ง) representative dataset ผิด

   <details><summary>เฉลย</summary>

   **ข** — train สูงแต่ val ไม่ตามคือจำข้อสอบ แก้ด้วยข้อมูลเพิ่ม หยุดเร็วขึ้น หรือโมเดลเล็กลง ส่วน underfit คือทั้งคู่ต่ำค้าง

   </details>

4. ตั้ง supported_ops = [TFLITE_BUILTINS_INT8] แต่ลืมผูก representative_dataset แล้วเรียก convert() จะเกิดอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) ได้ไฟล์ที่แม่นเท่าเดิม
   - ข) converter หยุดด้วย ValueError เพราะ full-integer ต้องมีตัวอย่างไว้ calibrate
   - ค) ได้ไฟล์ float32
   - ง) ไฟล์เล็กลงแปดเท่า

   <details><summary>เฉลย</summary>

   **ข** — ไม่มีตัวอย่าง converter ก็เลือก scale และ zero-point ของ activation ไม่ได้ TensorFlow จึงปฏิเสธตั้งแต่ต้น ถ้ามีแต่เป็นตัวอย่างที่ไม่เหมือนจริง ไฟล์จะออกมาแต่แม่นตก

   </details>

5. confusion matrix: idle [10 0 0], circle [0 8 2], shaking [0 1 9] ความแม่นและคู่ที่สับสนที่สุดคืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) ความแม่น 0.90 และโมเดลทาย circle ผิดเป็น shaking บ่อยที่สุด
   - ข) ความแม่น 0.90 และโมเดลทาย idle ผิดบ่อยที่สุด
   - ค) ความแม่น 0.27 และไม่มีคู่ใดสับสน
   - ง) ความแม่น 1.00

   <details><summary>เฉลย</summary>

   **ก** — แนวทแยง 10 + 8 + 9 = 27 จาก 30 คือ 0.90 แถว circle มี 2 หน้าต่างที่ถูกทายเป็น shaking ควรเก็บสองท่านี้เพิ่ม

   </details>

## แล็บ

- [ ] คำนวณค่าออก Conv1D อีกสามตำแหน่งของ kernel `[.2 .5 .3]` บน `.1 .4 .8 .6 .2 .3` แล้วเทียบกับภาพเคลื่อนไหว
- [ ] นับพารามิเตอร์ของทุกชั้นในโมเดลด้วยมือ แล้วเทียบกับ `model.count_params()` ที่ฉบับเต็มพิมพ์ออกมา
- [ ] คำนวณ softmax ของ `[2.0, 3.1, 1.2]` และ loss เมื่อเฉลยคือ circle แล้วจดลงบันทึกการเรียน

## ไปต่อ

บทเรียน 5.5 เราจะเติมสี่ช่องใน `s12_train.py` ให้ครบทั้งสี่จังหวะ แล้วรันใน Docker จนได้โมเดลของเราเอง

บทเรียนถัดไป: [บทเรียน 5.5 — ลงมือทำ: เติมสคริปต์ฝึกแล้วรันใน Docker](../l05-train-lab/README.md)

## สะท้อนคิด

- ถ้า confusion matrix ของข้อมูลจริงสับสน circle กับ shaking บ่อย คุณจะแก้ที่ข้อมูลหรือที่โมเดลก่อน เพราะอะไร
- ทำไมการ normalize ด้วย mean/std คนละชุดจึงเป็นบั๊กที่หายากกว่าโปรแกรม error
