---
id: edgeai-dev.m05.l05
lang: th
title: {th: 'ลงมือทำ: เติมสคริปต์ฝึกแล้วรันใน Docker', en: 'Hands-on: complete the training script and run it in Docker'}
summary: {th: 'เติมสี่ช่องใน s12_train.py ตรงสี่จังหวะของการฝึก คือ fit, representative dataset, int8 I/O และ accuracy แล้วรันใน Docker จนได้ model_int8.tflite กับรายงานความแม่น float32, int8 และ confusion matrix ของโมเดลที่เราฝึกเองทั้งตัว พร้อมทดลองลดจำนวน epoch และเปลี่ยนชุด calibrate', en: 'Fill the four points of s12_train.py that match the four beats of training (fit, representative dataset, int8 I/O and accuracy), run it in Docker until you get model_int8.tflite and a float32, int8 and confusion-matrix report for a model you trained yourself, then experiment with fewer epochs and a different calibration set.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: false, boards: [none]}
prerequisites: [edgeai-dev.m05.l04]
objectives:
  - {th: 'เติมสี่ช่องใน practice/s12_train.py จนรันใน Docker ได้ float32 test accuracy, int8 test accuracy, confusion matrix และไฟล์ model_int8.tflite กับ .norm.npz', en: 'Fill the four points in practice/s12_train.py so that a Docker run prints float32 test accuracy, int8 test accuracy and a confusion matrix and writes model_int8.tflite and its .norm.npz.'}
  - {th: รันเทียบ 3 epoch กับ 25 epoch แล้วจดความแม่นทั้งสองแบบ พร้อมอธิบายความต่างด้วยคำว่า underfit, en: 'Compare 3 and 25 epochs, record both accuracies and explain the difference in terms of underfitting.'}
  - {th: 'ระบุได้จากอาการว่าช่องใดยังว่าง (ความแม่นราว 0.33, ValueError ตอน convert, eval ป้อน int8 ไม่ผ่าน หรือ accuracy 0.000)', en: 'Tell from the symptom which point is still empty (accuracy near 0.33, a ValueError at convert, eval failing to feed int8, or accuracy 0.000).'}
develops: [{skill: ai.model-training, to: 3}, {skill: build.docker, to: 2}, {skill: lang.python, to: 2}]
assesses: [{skill: ai.model-training, level: 2, evidence: practice/s12_train.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 5.5 — ลงมือทำ: เติมสคริปต์ฝึกแล้วรันใน Docker

> โมดูล 5 — ฝึกโมเดลและนำไปใช้หลายเป้าหมาย · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เติมสี่ช่องใน s12_train.py ตรงสี่จังหวะของการฝึก คือ fit, representative dataset, int8 I/O และ accuracy แล้วรันใน Docker จนได้ model_int8.tflite กับรายงานความแม่น float32, int8 และ confusion matrix ของโมเดลที่เราฝึกเองทั้งตัว พร้อมทดลองลดจำนวน epoch และเปลี่ยนชุด calibrate

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เติมสี่ช่องใน practice/s12_train.py จนรันใน Docker ได้ float32 test accuracy, int8 test accuracy, confusion matrix และไฟล์ model_int8.tflite กับ .norm.npz
2. รันเทียบ 3 epoch กับ 25 epoch แล้วจดความแม่นทั้งสองแบบ พร้อมอธิบายความต่างด้วยคำว่า underfit
3. ระบุได้จากอาการว่าช่องใดยังว่าง (ความแม่นราว 0.33, ValueError ตอน convert, eval ป้อน int8 ไม่ผ่าน หรือ accuracy 0.000)

## ก่อนเริ่ม

ผ่านบทเรียน 5.4 มาแล้ว เข้าใจสี่จังหวะ build, fit, convert, eval
คัดลอก `practice/s12_train.py` ไปวางใน [`shared/training`](../../shared/training/) ข้าง `dataset_tools.py` และมี `data/gestures.csv` พร้อม

- **อุปกรณ์:** คอมพิวเตอร์ของคุณ ไม่ต้องใช้บอร์ด — ใช้ PC ที่ติดตั้ง Docker ถ้าไม่มี Docker ให้คัดลอกช่องที่เติมไปทดลองใน notebook บน Colab
- **เรียนมาก่อน:** [บทเรียน 5.4 — ข้างในการฝึก: Keras, Conv1D, gradient descent, int8 และ confusion matrix](../l04-inside-training/README.md)

## แนวคิด

ไฟล์ฝึกให้ dataset_tools, `build_model` และส่วน quantize/dequantize ไว้ครบ เหลือสี่ช่องที่ตรงสี่จังหวะ:
(1) ใน `main()` หลัง `compile` เติม `model.fit(Xtr, ytr, validation_data=(Xva, yva), epochs=a.epochs, batch_size=32, verbose=2)` ลืมช่องนี้
โมเดลไม่เคยเรียน ความแม่นจะอยู่แถว 0.33 (เดาในสามคลาส) (2) ใน `to_int8_tflite()` เติม `conv.representative_dataset = representative`
ลืมแล้ว `convert()` หยุดด้วย `ValueError` (3) เติม `conv.inference_input_type = tf.int8` และ `conv.inference_output_type = tf.int8`
ลืมแล้วขาเข้าขาออกยังเป็น float32 (สเกลใน `quantization` เป็น 0) และ `eval_int8()` ที่ป้อน int8 จะรันไม่ผ่าน
(4) ใน `eval_int8()` เติม `acc = (preds == yte).mean()` ลืมแล้วรายงาน 0.000 ทั้งที่ confusion matrix อาจถูกทั้งแนวทแยง

รันด้วย `docker run --rm -v "$PWD":/work edgeai-train python s12_train.py` จะได้ `float32 test accuracy` → `int8 test accuracy` → confusion matrix
และไฟล์ `model_int8.tflite` กับ `model_int8.tflite.norm.npz` ความสำเร็จไม่ใช่แค่เห็นตัวเลขวิ่ง แต่ต้องบอกได้ว่าทำไม int8 ควรใกล้ float32
และ representative dataset มีไว้ทำอะไร ไฟล์ที่ได้คือชิ้นงานที่ชุดบทเรียนถัดไปจะพาไปเบราว์เซอร์และบอร์ด

## ตัวอย่างสมบูรณ์

`s12_train_full.py` สร้างชุดสังเคราะห์ให้เองถ้ายังไม่มี `data/gestures.csv` พิมพ์ `model.summary()` กับ `count_params()` เตือนเมื่อ int8 แม่นตกจาก float32
เกิน `INT8_DROP_WARN = 0.05` และมีเกต MVP ที่ผ่านเมื่อ int8 accuracy ≥ `MVP_MIN_ACC = 0.80` (คืน exit code 0 หรือ 1 ใช้ใน CI ได้)
วางไว้ใน `shared/training` เช่นเดียวกับไฟล์ฝึก

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/s12_train_full.py](examples/s12_train_full.py) | ฝึก + ทดสอบโมเดลท่ามือ แบบครบวงจร (ฉบับเต็ม) |

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นหรือใน `shared/` ด้วย:

- [shared/training](../../shared/training)
- [shared/training/dataset_tools.py](../../shared/training/dataset_tools.py) — Dataset tools for the IMU gesture classifier (Pillar 4 / Training).
- [shared/training/eval_pc.py](../../shared/training/eval_pc.py) — Run the exported int8 .tflite on the PC and report accuracy + confusion.
- [shared/training/model_int8.tflite](../../shared/training/model_int8.tflite)

## ฝึกเติม

คอมเมนต์ `# เติม:` อยู่ที่บรรทัด 131 (ช่อง 1 `model.fit`), 53 (ช่อง 2 `representative_dataset`), 60 (ช่อง 3 int8 I/O) และ 97 (ช่อง 4 `acc`)
เติมทีละช่องแล้วรัน อาการของช่องที่ยังว่างบอกได้เองว่าเหลือช่องไหน

| ไฟล์ฝึก | เรื่อง |
|---|---|
| [practice/s12_train.py](practice/s12_train.py) | ฝึกโมเดลของเราเองด้วย TensorFlow แล้วทดสอบบน PC (ฉบับฝึกเติมโค้ด) |

## เฉลย

เปิดเฉลยหลังจากลองเองแล้วอย่างน้อยหนึ่งรอบ และอ่าน [วิธีใช้เฉลย](../../README.md#วิธีใช้เฉลย) ก่อน

| เฉลย | คู่กับ |
|---|---|
| [solution/s12_train.py](solution/s12_train.py) | [practice/s12_train.py](practice/s12_train.py) |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. รันแล้วได้ float32 test accuracy: 0.333 ทุกครั้ง ช่องใดยังว่าง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) ช่อง 1 model.fit
   - ข) ช่อง 2 representative_dataset
   - ค) ช่อง 3 int8 I/O
   - ง) ช่อง 4 acc

   <details><summary>เฉลย</summary>

   **ก** — ถ้าไม่ fit น้ำหนักยังเป็นค่าสุ่ม โมเดลเดาในสามคลาสได้ราวหนึ่งในสาม evaluate จึงวัดได้ราว 0.33

   </details>

2. convert() หยุดด้วย ValueError: For full integer quantization, a representative_dataset must be specified. ต้องแก้ช่องใด *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) ช่อง 1
   - ข) ช่อง 2 เติม conv.representative_dataset = representative
   - ค) ช่อง 3
   - ง) ช่อง 4

   <details><summary>เฉลย</summary>

   **ข** — ข้อความบอกตรง ๆ ว่าการบีบแบบ full-integer ต้องมีตัวอย่างไว้ calibrate ช่วงค่า

   </details>

3. รายงานบอก int8 test accuracy: 0.000 แต่ confusion matrix มีตัวเลขเต็มแนวทแยง ช่องใดยังว่าง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) ช่อง 1
   - ข) ช่อง 2
   - ค) ช่อง 3
   - ง) ช่อง 4 acc ยังเป็นค่าเริ่มต้น 0.0

   <details><summary>เฉลย</summary>

   **ง** — confusion matrix คำนวณจาก preds จริง แต่ตัวเลขความแม่นมาจาก acc ที่ยังเป็น 0.0 ต้องเติม acc = (preds == yte).mean()

   </details>

4. ฝึก 3 epoch ได้ทั้ง accuracy และ val_accuracy ต่ำกว่าตอน 25 epoch ชัดเจน อธิบายอย่างไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) overfit
   - ข) underfit เพราะฝึกสั้นเกินไป loss ยังลงไม่สุด
   - ค) int8 ทำให้แม่นตก
   - ง) ข้อมูลรั่ว

   <details><summary>เฉลย</summary>

   **ข** — ทั้ง train และ val ต่ำด้วยกันคืออาการ underfit ให้เวลาโมเดลไถลลงเนิน loss มากขึ้นก็ดีขึ้น

   </details>

## แล็บ

**MVP ของชุดบทเรียน 5.3–5.5:** ฝึกโมเดล Keras ใน Docker สำเร็จ ได้รายงาน float32 accuracy, int8 accuracy และ confusion matrix บนชุดทดสอบที่โมเดลไม่เคยเห็น พร้อมไฟล์ `model_int8.tflite` และ `.norm.npz`

- [ ] เติมไฟล์ฝึกครบสี่ช่อง รันใน Docker จนได้รายงานและไฟล์ทั้งสอง
- [ ] รันด้วย `--epochs 3` เทียบกับ 25 epoch จดความแม่นทั้งสองแบบลงบันทึกการเรียน และอธิบายความต่าง
- [ ] ให้ `representative()` ป้อนหน้าต่างศูนย์ล้วน (`np.zeros_like(X_repr[i:i + 1])`) แทนหน้าต่างจริง แล้วเทียบ int8 accuracy กับเดิม
- [ ] อธิบายได้ว่า `fit`, `representative_dataset`, `inference_input_type` และ accuracy อยู่ตรงไหน ทำอะไร

## ไปต่อ

ชุดบทเรียนถัดไป (บทเรียน 5.6–5.7) เราจะพาไฟล์นี้ไปรันในเบราว์เซอร์ พิสูจน์ว่าคำตัดสินตรงกับ PC และเล่าเรื่องการรันบน Cortex-A

บทเรียนถัดไป: [บทเรียน 5.6 — รันโมเดลบนเว็บ: LiteRT.js, int8 I/O และ parity](../l06-web-runtime/README.md)

## สะท้อนคิด

- int8 accuracy ของคุณต่างจาก float32 เท่าไร และคุณเชื่อตัวเลขนั้นแค่ไหนเมื่อชุดทดสอบมีแค่ราวยี่สิบหน้าต่าง
- ถ้าข้อมูลจริงให้ความแม่นต่ำกว่าข้อมูลสังเคราะห์มาก คุณจะเริ่มแก้จากตรงไหน
