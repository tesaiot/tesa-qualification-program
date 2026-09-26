---
id: edgeai-dev.m05.l08
lang: th
title: {th: 'quantize และ Vela: เอาโมเดลของเราขึ้น Ethos-U55', en: 'Quantize and Vela: putting our model on the Ethos-U55'}
summary: {th: 'เป้าหมายสุดท้ายและยากที่สุดของ "train once, run everywhere" คือ MCU กับ Ethos-U55 เข้าใจว่าทำไม NPU ต้องมีขั้นคอมไพล์ Vela เพิ่ม ไฟล์ .tflite สามหน้าตาไปเป้าหมายใด สัญญาสี่ฟังก์ชัน AIM_* ที่ทำให้ edge_ai เรียกโมเดลได้ สองทางในการห่อโมเดล และเหตุผลที่ NPU เร็วและประหยัดกว่า', en: 'The last and hardest target of "train once, run everywhere" is the MCU with its Ethos-U55. Learn why the NPU needs an extra Vela compile, which of three .tflite packages goes where, the four-function AIM_* contract that lets edge_ai call a model, the two ways to wrap a model, and why the NPU is faster and cheaper per inference.'}
level: L3
time_min: {concept: 50, practise: 10, check: 10}
hardware: {emulator: false, boards: [none]}
prerequisites: [edgeai-dev.m05.l07]
objectives:
  - {th: 'อธิบายได้ว่าทำไมมีแค่ MCU ที่ต้องคอมไพล์ด้วย Vela และจับคู่ไฟล์ model_int8, model_int8_vela และ model_web กับเป้าหมายที่ถูกต้อง', en: 'Explain why only the MCU needs a Vela compile, and match model_int8, model_int8_vela and model_web to the right targets.'}
  - {th: รัน quantize_vela.sh ใน Docker image เดิมจนได้ output/model_int8_vela.tflite และอธิบายตัวเลือก --accelerator-config ethos-u55-128 กับ --optimise Performance, en: 'Run quantize_vela.sh in the same Docker image to get output/model_int8_vela.tflite, and explain --accelerator-config ethos-u55-128 and --optimise Performance.'}
  - {th: 'อธิบายสัญญา AIM_* สี่ฟังก์ชัน (init, enqueue, dequeue, finalize) กับรหัสคืนค่า และบอกได้ว่ากับดักหลักของการห่อโมเดลคือ feature parity ไม่ใช่ตัวกราฟ', en: 'Describe the four-function AIM_* contract (init, enqueue, dequeue, finalize) and its return codes, and name feature parity, not the graph, as the main trap when wrapping a model.'}
  - {th: อธิบายว่าทำไม NPU จึงเร็วกว่าและใช้พลังงานต่อการอนุมานน้อยกว่า CPU และอ่านตารางเทียบโดยดู worst-case latency กับความผิดพลาดรายคลาสได้, en: 'Explain why the NPU is faster and uses less energy per inference than the CPU, and read a comparison table looking at worst-case latency and per-class errors.'}
develops: [{skill: ai.model-deploy, to: 3}, {skill: hw.architecture, to: 2}, {skill: build.vendor-sdk, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 5.8 — quantize และ Vela: เอาโมเดลของเราขึ้น Ethos-U55

> โมดูล 5 — ฝึกโมเดลและนำไปใช้หลายเป้าหมาย · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เป้าหมายสุดท้ายและยากที่สุดของ "train once, run everywhere" คือ MCU กับ Ethos-U55 เข้าใจว่าทำไม NPU ต้องมีขั้นคอมไพล์ Vela เพิ่ม ไฟล์ .tflite สามหน้าตาไปเป้าหมายใด สัญญาสี่ฟังก์ชัน AIM_* ที่ทำให้ edge_ai เรียกโมเดลได้ สองทางในการห่อโมเดล และเหตุผลที่ NPU เร็วและประหยัดกว่า

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. อธิบายได้ว่าทำไมมีแค่ MCU ที่ต้องคอมไพล์ด้วย Vela และจับคู่ไฟล์ model_int8, model_int8_vela และ model_web กับเป้าหมายที่ถูกต้อง
2. รัน quantize_vela.sh ใน Docker image เดิมจนได้ output/model_int8_vela.tflite และอธิบายตัวเลือก --accelerator-config ethos-u55-128 กับ --optimise Performance
3. อธิบายสัญญา AIM_* สี่ฟังก์ชัน (init, enqueue, dequeue, finalize) กับรหัสคืนค่า และบอกได้ว่ากับดักหลักของการห่อโมเดลคือ feature parity ไม่ใช่ตัวกราฟ
4. อธิบายว่าทำไม NPU จึงเร็วกว่าและใช้พลังงานต่อการอนุมานน้อยกว่า CPU และอ่านตารางเทียบโดยดู worst-case latency กับความผิดพลาดรายคลาสได้

## ก่อนเริ่ม

ผ่านชุดบทเรียน 5.3–5.7 มาแล้ว มี `model_int8.tflite` ที่ผ่าน `eval_pc.py` และเข้าใจ quantize กับ dequantize
เปิด [`quantize_vela.sh`](../../shared/training/quantize_vela.sh) ไว้อ่านคู่กับสไลด์

- **อุปกรณ์:** คอมพิวเตอร์ของคุณ ไม่ต้องใช้บอร์ด — ใช้ PC กับ Docker image เดิม ส่วนที่ต้องใช้บอร์ดอยู่ในบทเรียน 5.9
- **เรียนมาก่อน:** [บทเรียน 5.7 — ลงมือทำ: verdict บนเว็บให้ตรงกับ PC และเรื่องราว Cortex-A](../l07-web-parity-lab/README.md)

## ดูของจริงก่อน

ใน Docker image เดิม สั่ง `./quantize_vela.sh model_int8.tflite` แล้วดูไฟล์ใหม่ใน `output/` ไฟล์ `_vela.tflite` นี้เบราว์เซอร์กับ PC เปิดไม่ได้แล้ว
ถามตัวเองว่า Vela เปลี่ยนอะไรในไฟล์ และทำไมเปลี่ยนแล้ว accuracy ไม่ควรเปลี่ยน

## แนวคิด

Web, Cortex-A และ PC ล้วนรันกราฟ TFLite ทั่วไปบน CPU หรือ GPU ได้ตรง ๆ แต่ **NPU ไม่ใช่ CPU** มันคือวงจรคูณเมทริกซ์ int8 เฉพาะทาง
**Vela** (`ethos-u-vela` ของ Arm) จึงรับ `.tflite` แบบ full-integer int8 แล้วแทน subgraph ที่ NPU ทำได้ด้วย custom op ตัวเดียวชื่อ `ethos-u`
ส่วนที่ NPU ทำไม่ได้ปล่อยให้ Cortex-M55 ทำ `quantize_vela.sh` ห่อคำสั่ง `vela --accelerator-config ethos-u55-128 --optimise Performance`
(U55 ที่ 128 MAC ต่อรอบ เน้นความเร็ว) ได้ `output/model_int8_vela.tflite` ที่ใช้ได้กับ MCU เท่านั้น ถึงตรงนี้มี **หนึ่งน้ำหนัก สามบรรจุภัณฑ์**:
`model_int8.tflite` (PC, Cortex-A และต้นทางของ Vela) `_vela.tflite` (MCU) และ `model_web.tflite` (เบราว์เซอร์) เอาไฟล์ผิดที่จะโหลดไม่ขึ้นทันที

Vela ไม่แก้คณิตของโมเดล $q = \mathrm{round}(x/s) + z$ และ $x = (q - z)\cdot s$ ยังใช้ $s, z$ ที่ PTQ ฝังไว้ในทุก tensor accuracy บน NPU จึงควรเท่ากับ int8 บน PC
(ต่างได้แค่ระดับการปัดเศษของ kernel) ถ้าบนบอร์ดเพี้ยนมาก ให้สงสัย front-end ก่อน ไฟล์ Vela ยังไม่ใช่โมเดลที่บอร์ดรู้จัก ต้อง **ห่อ** ด้วยสัญญาสี่ฟังก์ชัน
`<SLOT>_init`, `<SLOT>_enqueue(const float *in)`, `<SLOT>_dequeue(float *out)` และ `<SLOT>_finalize` ซึ่งคือ IPWIN streaming ABI ของ Imagimob
ที่ DEEPCRAFT Studio สร้างให้ `dequeue` คืน −1 (NODATA) ระหว่างที่หน้าต่างยังไม่เต็มเป็นเรื่องปกติ ห่อได้สองทาง: ตัวแปลงของ DEEPCRAFT ที่สร้าง C
พร้อม front-end ให้ หรือห่อ TFLite-Micro เองแล้วเขียน front-end ให้ตรงกับตอนฝึก กับดักอันดับหนึ่งคือ feature ที่ไม่ตรงกัน ไม่ใช่ตัวกราฟ
ซอร์สเฟิร์มแวร์ BENTO ที่คอร์สใช้ยังไม่เปิด ใน [SDK สาธารณะ](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) ตัว engine มาเป็นไลบรารี prebuilt
โมเดลใหม่จึงเข้าทะเบียนด้วย `ai_engine_register()` หรือใส่แทนช่องเดิม ตาม
[คู่มือ Filling a model slot](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/main/bento-firmware-template-mtb-mpy/proj_cm55/modules/ai_models/README.md)

NPU ไม่ได้ฉลาดกว่า CPU มันทำงานเดียวคือคูณเมทริกซ์ int8 ด้วยวงจร MAC ขนาน 128 ตัวต่อรอบ งานเดียวกันจึงเสร็จในรอบน้อยกว่ามาก
เสร็จเร็วคือปลุกวงจรสั้นแล้วกลับไปหลับ พลังงานต่อการอนุมานจึงต่ำตามไปด้วย ตอนอ่านตารางเทียบ ระวังสามเรื่อง: accuracy รวมอาจซ่อนคลาสที่พลาด
(ดู confusion matrix) latency เฉลี่ยซ่อน worst-case และ Web ต่างเล็กน้อยได้เพราะ activation เป็น float

## ตัวอย่างสมบูรณ์

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นหรือใน `shared/` ด้วย:

- [shared/interactive/math_lab.html](../../shared/interactive/math_lab.html)
- [shared/training/eval_pc.py](../../shared/training/eval_pc.py) — Run the exported int8 .tflite on the PC and report accuracy + confusion.
- [shared/training/model_int8.tflite](../../shared/training/model_int8.tflite)
- [shared/training/quantize_vela.sh](../../shared/training/quantize_vela.sh) — Compile an int8 .tflite for the Ethos-U55 NPU on the PSoC Edge board.

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. ไฟล์ใดควรส่งไปหน้าเว็บ *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) model_int8_vela.tflite
   - ข) model_web.tflite ที่ I/O เป็น float และไม่มี custom op ของ NPU
   - ค) model.keras
   - ง) ไฟล์ใดก็ได้

   <details><summary>เฉลย</summary>

   **ข** — ไฟล์ Vela มี op ethos-u ที่รันได้เฉพาะบน NPU ส่วน model_web.tflite ทำมาเพื่อเบราว์เซอร์ และ model_int8.tflite ใช้กับ PC และ Cortex-A

   </details>

2. หลังรัน ./quantize_vela.sh model_int8.tflite ไฟล์ของ MCU อยู่ที่ใด *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) ./model_int8.tflite ทับไฟล์เดิม
   - ข) ./output/model_int8_vela.tflite
   - ค) ./vela/model.bin
   - ง) ในบอร์ดโดยตรง

   <details><summary>เฉลย</summary>

   **ข** — Vela เขียนผลลงโฟลเดอร์ output ต่อท้ายชื่อด้วย _vela ไฟล์ int8 เดิมยังอยู่ไว้ใช้กับ PC และ Cortex-A

   </details>

3. AIM_GESTURE_dequeue คืน −1 ในช่วงแรกหลัง start หมายความว่าอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) โมเดลพัง ต้อง flash ใหม่
   - ข) NODATA: หน้าต่างยังเก็บข้อมูลไม่เต็ม เป็นเรื่องปกติ
   - ค) NPU ร้อนเกินไป
   - ง) คลาสที่ชนะคือ −1

   <details><summary>เฉลย</summary>

   **ข** — ตาม IPWIN ABI ค่า −1 คือยังไม่มีผล enqueue ต่อไปจนหน้าต่างเต็ม dequeue จึงคืน 0 พร้อมคะแนน

   </details>

4. int8 บน PC แม่น 0.95 แต่บนบอร์ดทายผิดเกือบหมด ควรสงสัยอะไรก่อน *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) Vela คำนวณผิด
   - ข) front-end บนบอร์ด (normalize, quantize หรือ feature) ไม่ตรงกับตอนฝึก
   - ค) NPU ช้าเกินไป
   - ง) ต้องฝึกใหม่ด้วย epoch มากขึ้น

   <details><summary>เฉลย</summary>

   **ข** — Vela ไม่แก้คณิต ความต่างใหญ่ขนาดนี้มักมาจากข้อมูลที่ป้อนเข้าโมเดลบนบอร์ดคนละสเกลหรือคนละ feature กับตอนฝึก

   </details>

5. ทำไม Ethos-U55 ใช้พลังงานต่อการอนุมานน้อยกว่า Cortex-M55 ทำเอง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) เพราะใช้ float32
   - ข) เพราะคูณเมทริกซ์ int8 ได้ขนาน 128 MAC ต่อรอบ งานเสร็จในรอบน้อยกว่า แล้วบอร์ดกลับไปหลับได้เร็ว
   - ค) เพราะข้ามการ normalize
   - ง) เพราะไม่ต้องใช้ไฟ

   <details><summary>เฉลย</summary>

   **ข** — ความเร็วกับพลังงานมาจากเหตุผลเดียวกัน วงจรเฉพาะทางทำงานเดียวได้ขนาน ใช้รอบสัญญาณนาฬิกาน้อยกว่ามาก

   </details>

## แล็บ

- [ ] รัน `./quantize_vela.sh model_int8.tflite` ใน Docker image เดิม จดขนาดไฟล์ `_vela.tflite` เทียบกับ `model_int8.tflite` ลงบันทึกการเรียน
- [ ] อ่านรายงานที่ Vela พิมพ์ออกมา แล้วหาว่ามี op ใดที่ตกไปรันบน CPU หรือไม่
- [ ] วาดแผนผัง "หนึ่งน้ำหนัก สามบรรจุภัณฑ์" พร้อมเขียนว่าแต่ละไฟล์มาจากสคริปต์ใดและไปเป้าหมายใด

## ไปต่อ

บทเรียน 5.9 เราจะเติม `s14_tflite_board.py` ให้ bench int8 บน PC รัน Vela แล้วเติมตารางเทียบสามเป้าหมาย รวมถึงอ่าน latency จริงจากบอร์ด

บทเรียนถัดไป: [บทเรียน 5.9 — ลงมือทำ: เทียบสามเป้าหมาย MCU, Web และ PC](../l09-three-targets-lab/README.md)

## สะท้อนคิด

- ถ้าโมเดลของคุณมี op ที่ Ethos-U55 ทำไม่ได้หลายตัว ผลต่อ latency จะเป็นอย่างไร และคุณจะแก้ที่ไหน
- งานแบบไหนที่คุณยอมจ่ายขั้นคอมไพล์เพิ่มเพื่อให้แบตเตอรี่อยู่ได้นานขึ้น
