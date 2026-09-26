---
id: edgeai-dev.m05.l03
lang: th
title: {th: 'ฝึกโมเดลใน Docker: หนึ่งชิ้นงาน สี่เป้าหมาย', en: 'Training in Docker: one artifact, four targets'}
summary: {th: เลิกยืมโมเดลสำเร็จรูปแล้วฝึกของเราเอง เริ่มจากเหตุผลที่ต้องฝึกใน Docker ภาพรวม "หนึ่งชิ้นงาน สี่เป้าหมาย" ของ model_int8.tflite แล้วรัน train.py กับ eval_pc.py ของจริง (หรือบน Colab) ก่อนเข้าใจ อ่าน log ให้ออกว่าแต่ละบรรทัดบอกอะไร, en: 'Stop borrowing ready-made models and train your own. Start with why training runs in Docker and the "one artifact, four targets" picture of model_int8.tflite, then run the real train.py and eval_pc.py (or Colab) before understanding them, and learn to read every line of the log.'}
level: L3
time_min: {concept: 30, practise: 25, check: 10}
hardware: {emulator: false, boards: [none]}
prerequisites: [edgeai-dev.m05.l02]
objectives:
  - {th: 'บอกเหตุผลที่ฝึกใน Docker ได้อย่างน้อยสองข้อ และอธิบายหน้าที่ของ -v "$PWD":/work กับ --rm ในคำสั่ง docker run', en: 'Give at least two reasons to train inside Docker, and explain what -v "$PWD":/work and --rm do in the docker run command.'}
  - {th: 'วาดแผนผังหนึ่งชิ้นงานสี่เป้าหมาย (MCU, PC, Web, Cortex-A) ของ model_int8.tflite และบอกได้ว่าทำไมมีแค่ MCU ที่ต้องผ่าน Vela', en: 'Draw the one-artifact, four-target map of model_int8.tflite (MCU, PC, web, Cortex-A) and say why only the MCU needs Vela.'}
  - {th: รัน train.py และ eval_pc.py (ใน Docker หรือบน Colab) แล้วจดจำนวนหน้าต่างแต่ละกอง ความแม่น float32 และ int8 ขนาดไฟล์ และไฟล์ที่ต้องเดินทางคู่กับโมเดล, en: 'Run train.py and eval_pc.py (in Docker or on Colab) and record the window count of each set, the float32 and int8 accuracy, the file size and the file that must travel with the model.'}
develops: [{skill: build.docker, to: 2}, {skill: ai.model-training, to: 2}, {skill: ai.model-deploy, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 5.3 — ฝึกโมเดลใน Docker: หนึ่งชิ้นงาน สี่เป้าหมาย

> โมดูล 5 — ฝึกโมเดลและนำไปใช้หลายเป้าหมาย · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เลิกยืมโมเดลสำเร็จรูปแล้วฝึกของเราเอง เริ่มจากเหตุผลที่ต้องฝึกใน Docker ภาพรวม "หนึ่งชิ้นงาน สี่เป้าหมาย" ของ model_int8.tflite แล้วรัน train.py กับ eval_pc.py ของจริง (หรือบน Colab) ก่อนเข้าใจ อ่าน log ให้ออกว่าแต่ละบรรทัดบอกอะไร

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. บอกเหตุผลที่ฝึกใน Docker ได้อย่างน้อยสองข้อ และอธิบายหน้าที่ของ -v "$PWD":/work กับ --rm ในคำสั่ง docker run
2. วาดแผนผังหนึ่งชิ้นงานสี่เป้าหมาย (MCU, PC, Web, Cortex-A) ของ model_int8.tflite และบอกได้ว่าทำไมมีแค่ MCU ที่ต้องผ่าน Vela
3. รัน train.py และ eval_pc.py (ใน Docker หรือบน Colab) แล้วจดจำนวนหน้าต่างแต่ละกอง ความแม่น float32 และ int8 ขนาดไฟล์ และไฟล์ที่ต้องเดินทางคู่กับโมเดล

## ก่อนเริ่ม

ผ่านชุดบทเรียน 5.1–5.2 มาแล้ว มี `data/gestures.csv` จากบอร์ด หรือสร้างชุดสังเคราะห์ด้วย `python dataset_tools.py --synthesize --out data/gestures.csv`
ติดตั้ง Docker ไว้ (ครั้งแรกจะดาวน์โหลด TensorFlow หลายร้อย MB) หรือเตรียมเปิด notebook บน Google Colab

- **อุปกรณ์:** คอมพิวเตอร์ของคุณ ไม่ต้องใช้บอร์ด — ใช้ PC ที่ติดตั้ง Docker หรือบัญชี Google สำหรับ Colab
- **เรียนมาก่อน:** [บทเรียน 5.2 — ลงมือทำ: เก็บ dataset ที่สมดุลบนบอร์ดแล้วแบ่งบน PC](../l02-dataset-lab/README.md)

## ดูของจริงก่อน

ในโฟลเดอร์ [`shared/training`](../../shared/training/) สั่ง `docker build -t edgeai-train .` ครั้งเดียว แล้ว
`docker run --rm -v "$PWD":/work edgeai-train python train.py --data data/gestures.csv --out model_int8.tflite`
ดู accuracy ไต่ขึ้นทุก epoch จนได้ไฟล์ `model_int8.tflite` ราว 11 KB โผล่ในโฟลเดอร์บนเครื่องเรา ก่อนรู้ว่าข้างในทำอะไร

## แนวคิด

การฝึกต้องใช้ TensorFlow กับไลบรารีอีกเป็นสิบ แต่ละเครื่องเวอร์ชันไม่ตรงกันจนเกิด "บนเครื่องผมรันได้นะ" **Docker** แก้ด้วยอิมเมจเดียว:
`Dockerfile` เริ่มจาก `python:3.11-slim` ลง `tensorflow`, `ai-edge-litert`, `numpy`, `scikit-learn` และลง `ethos-u-vela` แยกชั้นไว้
ทุกคนจึงได้เวอร์ชันเดียวกันบน macOS, Windows และ Linux ไม่รกเครื่อง ลบทิ้งได้ `-v "$PWD":/work` เอาโฟลเดอร์ปัจจุบันไปวางใน container
โค้ด ข้อมูล และผลลัพธ์จึงอยู่ที่เดียวกัน `--rm` ลบ container ทิ้งเมื่อจบ ถ้ายังไม่มี Docker ใช้ notebook
[`train_edge_ai.ipynb`](../../shared/training/notebooks/train_edge_ai.ipynb) บน Google Colab แทนได้ (notebook สังเคราะห์ข้อมูลเองในหน่วย g
จึงใช้ซ้อม pipeline ได้ แต่โมเดลที่จะใช้กับบอร์ดต้องฝึกจาก CSV ของบอร์ด)

ทั้งโมดูลหมุนรอบไฟล์เดียว `model_int8.tflite` แบบ **train once, run everywhere**: PC รันด้วย `eval_pc.py` ผ่าน `ai-edge-litert`
Cortex-A (Raspberry Pi, Jetson) รันไฟล์เดิมด้วยสคริปต์เดิม เบราว์เซอร์ใช้ฉบับที่ `convert_web.py` เตรียมให้ และ MCU ต้องคอมไพล์เพิ่มด้วย
`quantize_vela.sh` (Vela) เพราะ Ethos-U55 ต้องการกราฟที่แปลงเป็น op ของ NPU ไฟล์ `_vela.tflite` ที่ได้จึงใช้ได้กับ MCU เท่านั้น

log ของ `train.py` กับชุดสังเคราะห์บอกทีละบรรทัด: `train/val/test windows: 101 21 21` คือจำนวนหน้าต่างสามกอง ทุก epoch มี `accuracy`
คู่กับ `val_accuracy` ที่ควรไต่ขึ้นด้วยกัน จากนั้น `float32 test accuracy` บนชุดที่โมเดลไม่เคยเห็น ขนาดไฟล์ที่เขียน (ไฟล์อ้างอิงในคอร์ส 11,504 ไบต์)
และ `model_int8.tflite.norm.npz` ที่เก็บ mean/std ไว้ ไฟล์นี้ต้องเดินทางคู่กับโมเดลเสมอ `eval_pc.py` รันไฟล์ int8 จริงแล้วพิมพ์ `int8 test accuracy`
กับ confusion matrix นี่คือ ground truth ก่อนเอาไปที่อื่น ชุดสังเคราะห์แยกคลาสง่ายจึงได้ตัวเลขสวย ข้อมูลจริงจะมีความสับสนบ้างเป็นเรื่องปกติ

## ตัวอย่างสมบูรณ์

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นหรือใน `shared/` ด้วย:

- [m05-training/l05-train-lab/practice/s12_train.py](../l05-train-lab/practice/s12_train.py) — ฝึกโมเดลของเราเองด้วย TensorFlow แล้วทดสอบบน PC (ฉบับฝึกเติมโค้ด)
- [shared/training](../../shared/training)
- [shared/training/dataset_tools.py](../../shared/training/dataset_tools.py) — Dataset tools for the IMU gesture classifier (Pillar 4 / Training).
- [shared/training/eval_pc.py](../../shared/training/eval_pc.py) — Run the exported int8 .tflite on the PC and report accuracy + confusion.
- [shared/training/model_int8.tflite](../../shared/training/model_int8.tflite)
- [shared/training/notebooks/train_edge_ai.ipynb](../../shared/training/notebooks/train_edge_ai.ipynb)
- [shared/training/train.py](../../shared/training/train.py) — Train a tiny IMU gesture classifier and export it as int8 TFLite.

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. ใน docker run --rm -v "$PWD":/work edgeai-train python train.py ส่วน -v "$PWD":/work ทำอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) ลบ container ทิ้งเมื่อจบ
   - ข) เอาโฟลเดอร์ปัจจุบันบนเครื่องไปวางที่ /work ใน container โค้ด ข้อมูล และผลลัพธ์จึงอยู่ที่เดียวกัน
   - ค) ตั้งชื่ออิมเมจ
   - ง) ติดตั้ง TensorFlow ลงเครื่อง

   <details><summary>เฉลย</summary>

   **ข** — bind mount ทำให้ไฟล์ model_int8.tflite ที่เขียนใน /work โผล่บนเครื่องเราทันที ส่วน --rm คือลบ container และ -t ตอน build คือตั้งชื่อ

   </details>

2. เป้าหมายใดต้องคอมไพล์ model_int8.tflite เพิ่มอีกขั้นก่อนใช้ *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) PC ผ่าน ai-edge-litert
   - ข) Cortex-A เช่น Raspberry Pi
   - ค) MCU ที่ใช้ Ethos-U55 ต้องผ่าน Vela
   - ง) ไม่มีเป้าหมายใดต้องทำเพิ่ม

   <details><summary>เฉลย</summary>

   **ค** — Vela แปลงส่วนที่ NPU รันได้เป็น op ของ Ethos-U ไฟล์ที่ได้จึงรันได้แค่บน MCU ส่วน PC และ Cortex-A ใช้ไฟล์ int8 เดิม

   </details>

3. log บอก float32 test accuracy 0.980 แต่ eval_pc.py บอก int8 test accuracy 0.600 ควรสงสัยอะไรก่อน *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) ข้อมูลไม่สมดุล
   - ข) การบีบเป็น int8 (calibration หรือ normalize ที่ไม่ตรงกัน) มีปัญหา
   - ค) Docker ช้าเกินไป
   - ง) ไม่มีอะไรผิด int8 ควรแม่นน้อยกว่ามากเสมอ

   <details><summary>เฉลย</summary>

   **ข** — โมเดลเดียวกันควรได้ int8 ใกล้ float32 ถ้าตกมากให้ตรวจ representative dataset และไฟล์ .norm.npz ที่ใช้ normalize ตอนทดสอบ

   </details>

4. ไฟล์ใดต้องเดินทางคู่กับ model_int8.tflite ไปทุกเป้าหมาย *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) Dockerfile
   - ข) model_int8.tflite.norm.npz ที่เก็บ mean/std ของชุดฝึก
   - ค) gestures.csv ทั้งไฟล์
   - ง) train.py

   <details><summary>เฉลย</summary>

   **ข** — ฝั่งที่ใช้โมเดลต้อง normalize ข้อมูลด้วย mean/std ชุดเดียวกับตอนฝึก ไม่งั้นโมเดลไม่ error แต่ทายผิดเงียบ ๆ

   </details>

## แล็บ

- [ ] build อิมเมจแล้วรัน `train.py` กับ `eval_pc.py` (หรือรัน notebook บน Colab จนจบ) จดตัวเลขทุกบรรทัดที่อธิบายไว้ลงบันทึกการเรียน
- [ ] วาดแผนผัง `model_int8.tflite` ไปสี่เป้าหมาย พร้อมเขียนชื่อสคริปต์ของแต่ละทาง
- [ ] ลบ `model_int8.tflite.norm.npz` ทิ้งแล้วรัน `eval_pc.py` อีกครั้ง จดว่าเกิดอะไรและเพราะอะไร

## ไปต่อ

บทเรียน 5.4 เราจะเปิด `train.py` แกะสี่จังหวะ build, fit, convert, eval พร้อมคณิตเบื้องหลังแต่ละจังหวะ

บทเรียนถัดไป: [บทเรียน 5.4 — ข้างในการฝึก: Keras, Conv1D, gradient descent, int8 และ confusion matrix](../l04-inside-training/README.md)

## สะท้อนคิด

- งานอื่นที่คุณเคยเจอปัญหา "บนเครื่องผมรันได้" มีอะไรบ้าง Docker ช่วยได้ไหม
- ถ้าต้องส่งโมเดลให้ทีมเว็บกับทีมเฟิร์มแวร์พร้อมกัน คุณจะส่งไฟล์อะไรให้ใครบ้าง
