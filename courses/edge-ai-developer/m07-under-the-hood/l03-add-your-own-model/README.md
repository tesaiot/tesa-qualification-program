---
id: edgeai-dev.m07.l03
lang: th
title: {th: 'เพิ่มโมเดลของเราเอง: สามการแก้ สัญญาสี่ฟังก์ชัน และ Vela', en: 'Adding your own model: three edits, a four-function contract and Vela'}
summary: {th: 'เรียนวิธีเพิ่มโมเดลของเราเองให้บอร์ดรู้จัก ทะเบียนแบบ shape-driven ทำให้ใช้แค่สามการแก้ในซอร์สเฟิร์มแวร์ตัวเต็ม คือ Makefile, ROW กับ s_models[] และไฟล์โมเดล รู้จักสัญญาสี่ฟังก์ชัน AIM_ กับ IMAI_ feed ของเซนเซอร์เดิม งบหน่วยความจำ flash กับ arena และทางเทียบเท่าใน SDK สาธารณะ', en: 'Learn how to make the board know a model of your own. A shape-driven registry means only three edits in the full firmware source (the Makefile, a ROW in s_models[], and the model file). Meet the four-function contract, AIM_ versus IMAI_, reusing an existing sensor''s feed, the flash-versus-arena memory budget, and the equivalent routes in the public SDK.'}
level: L3
time_min: {concept: 55, practise: 5, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m07.l02]
objectives:
  - {th: 'อธิบายได้ว่าทำไมทะเบียนแบบ shape-driven จึงใช้แค่สามการแก้โดยไม่แตะ MicroPython หรือ IPC และบอกทางเทียบเท่าใน SDK สาธารณะ (ai_engine_register(), การใส่โมเดลแทนช่องเดิม หรือโมเดล IMU แบบ staged)', en: 'Explain why a shape-driven registry needs only three edits and no change to MicroPython or IPC, and name the equivalents in the public SDK (ai_engine_register(), filling an existing slot, or a staged IMU model).'}
  - {th: 'เขียน descriptor ของโมเดล (name, sensor, class_labels ที่ index 0 เป็นคลาสปฏิเสธ, period_ms, ตัวชี้สี่ฟังก์ชัน) และบอกสัญญาสี่ฟังก์ชันพร้อมรหัสคืนค่าได้', en: 'Write a model descriptor (name, sensor, class_labels with index 0 as the negative class, period_ms, four function pointers) and state the four-function contract with its return codes.'}
  - {th: แยกหน่วยความจำของโมเดลเป็น flash (weights + code) กับ RAM (tensor arena + บัฟเฟอร์) และอธิบายว่า arena ไม่พอทำให้ select() ล้มอย่างไร, en: 'Split a model''s memory into flash (weights plus code) and RAM (tensor arena plus buffers), and explain how an arena that is too small makes select() fail.'}
  - {th: อธิบายว่าทำไมโมเดลที่ใช้เซนเซอร์เดิมจึงยืม feed ที่มีอยู่ได้ และทำไม feature parity จึงเป็นความล้มเหลวเงียบอันดับหนึ่ง, en: 'Explain why a model on an existing sensor can borrow the existing feed, and why feature parity is the number-one silent failure.'}
develops: [{skill: build.vendor-sdk, to: 2}, {skill: lang.c, to: 2}, {skill: ai.model-deploy, to: 3}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 7.3 — เพิ่มโมเดลของเราเอง: สามการแก้ สัญญาสี่ฟังก์ชัน และ Vela

> โมดูล 7 — ใต้ฝากระโปรงและการต่อเติม · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เรียนวิธีเพิ่มโมเดลของเราเองให้บอร์ดรู้จัก ทะเบียนแบบ shape-driven ทำให้ใช้แค่สามการแก้ในซอร์สเฟิร์มแวร์ตัวเต็ม คือ Makefile, ROW กับ s_models[] และไฟล์โมเดล รู้จักสัญญาสี่ฟังก์ชัน AIM_ กับ IMAI_ feed ของเซนเซอร์เดิม งบหน่วยความจำ flash กับ arena และทางเทียบเท่าใน SDK สาธารณะ

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. อธิบายได้ว่าทำไมทะเบียนแบบ shape-driven จึงใช้แค่สามการแก้โดยไม่แตะ MicroPython หรือ IPC และบอกทางเทียบเท่าใน SDK สาธารณะ (ai_engine_register(), การใส่โมเดลแทนช่องเดิม หรือโมเดล IMU แบบ staged)
2. เขียน descriptor ของโมเดล (name, sensor, class_labels ที่ index 0 เป็นคลาสปฏิเสธ, period_ms, ตัวชี้สี่ฟังก์ชัน) และบอกสัญญาสี่ฟังก์ชันพร้อมรหัสคืนค่าได้
3. แยกหน่วยความจำของโมเดลเป็น flash (weights + code) กับ RAM (tensor arena + บัฟเฟอร์) และอธิบายว่า arena ไม่พอทำให้ select() ล้มอย่างไร
4. อธิบายว่าทำไมโมเดลที่ใช้เซนเซอร์เดิมจึงยืม feed ที่มีอยู่ได้ และทำไม feature parity จึงเป็นความล้มเหลวเงียบอันดับหนึ่ง

## ก่อนเริ่ม

ผ่านชุดบทเรียน 7.1–7.2 มาแล้ว เข้าใจทะเบียน `s_models[]`, `ai_model_desc_t` และ IPC model link
เปิด [คู่มือ Filling a model slot](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/main/bento-firmware-template-mtb-mpy/proj_cm55/modules/ai_models/README.md) ของ SDK ไว้คู่จอ

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — เป็นบทเรียนแนวคิด การเพิ่มโมเดลจริงต้อง build เฟิร์มแวร์ด้วย ModusToolbox ซอร์สตัวเต็มที่มี ai_engine.c ยังไม่เปิดเผย SDK สาธารณะมี engine แบบ prebuilt กับ header ให้ใช้แทน
- **เรียนมาก่อน:** [บทเรียน 7.2 — ลงมือทำ: ส่องสแตกจาก MicroPython](../l02-trace-the-stack-lab/README.md)

## ดูของจริงก่อน

ทั้งคอร์ส `edge_ai.models()` ตอบหกโมเดลบนบอร์ด วันนี้ถามกลับว่าโมเดลตัวที่เจ็ดจะโผล่ในตารางนั้นได้อย่างไร
ซอร์สเฟิร์มแวร์ตัวเต็มมี `FALL_ROW` เขียนรอไว้เป็นตัวอย่างแล้ว ขาดแค่การปลุกให้ทำงาน

## แนวคิด

MicroPython (`edge_ai`) กับ IPC model link ไม่รู้จักชื่อโมเดลใดเลย `count()` นับจากขนาดของ `s_models[]` `model(n)` คัดลอกฟิลด์จากแถวที่ n
และ `select(n)` ให้ task เรียกตัวชี้ของแถวนั้น ทะเบียนจึงเป็น **shape-driven** ข้อมูลขับพฤติกรรม ในซอร์สตัวเต็มการเพิ่มโมเดลใช้ **สามการแก้**:
(1) เติมชื่อใน `AI_MODELS` ของ Makefile ซึ่ง derive `-DEDGE_AI_MODEL_<name>` ให้เอง (ระวังเว้นวรรคเกิน) (2) เขียน ROW ครอบด้วย `#if defined(...)` แล้วต่อเข้า
`s_models[]` (ลำดับใน array คือลำดับในเมนู) และ (3) วางไฟล์โมเดลใน `proj_cm55/modules/ai_models/` ใน SDK สาธารณะ `ai_engine` มาเป็นไลบรารี prebuilt
แถวใหม่จึงเพิ่มด้วย `ai_engine_register(&desc)` จากโค้ดของเราตอนรัน หรือใส่โมเดลแทนช่องเดิม และเฟิร์มแวร์รุ่นปัจจุบันยังโหลดโมเดล IMU แบบ staged ได้ตาม `ai_model_staged.h`

ทุกโมเดลต้องให้ **สี่ฟังก์ชัน** `<PREFIX>_init(void)`, `<PREFIX>_enqueue(const float *in)`, `<PREFIX>_dequeue(float *out)` และ `<PREFIX>_finalize(void)`
คืน `0` เมื่อสำเร็จ `-1` (NODATA) ระหว่างที่หน้าต่างยังไม่เต็ม และ `-2` เมื่อผิดพลาด โมเดลที่สร้างจาก DEEPCRAFT Studio ใช้คำนำหน้า `AIM_<NAME>_`
ส่วน Ready-Model แบบ `.a` ส่งออก `IMAI_*` ชื่อซ้ำกันทุกตัว จึงต้อง `objcopy` เปลี่ยนเป็น `IMAI_<NAME>_*` ก่อนอยู่ร่วมกัน descriptor มี `class_labels`
ที่ index 0 ต้องเป็นคลาสปฏิเสธ (idle, unlabelled, normal) เพราะหน้าจอใช้คะแนนสูงสุดของคลาส 1 ขึ้นไปเป็นความมั่นใจ

หน่วยความจำแยกเป็น $M_{flash} = W_{weights} + C_{code}$ กับ $M_{RAM} = A_{arena} + B_{io}$ โดย arena ต้องใหญ่พอสำหรับ tensor ที่มีชีวิตพร้อมกันมากที่สุด
ถ้า arena ไม่พอ `init()` คืนค่าติดลบ แล้ว `select()` โยน `OSError` weights ก้อนใหญ่ในภาพ `combo` อาจชนกำแพงแฟลช ต้องย้ายไป section `.ml_weights`
โมเดลที่ใช้เซนเซอร์เดิมยืม feed เดิมได้ทันที (Fall ใช้ IMU จึงยืม `feed_imu`) เซนเซอร์ใหม่ต้องเขียน feed เองเพื่อแปลงค่าดิบให้เป็นหน่วยเดียวกับตอนฝึก
ห่อโมเดลที่ฝึกเองได้สองทาง: ตัวแปลงของ DEEPCRAFT ที่สร้าง C พร้อม front-end หรือห่อ TFLite-Micro เองด้วย `AddEthosU()` แล้วเขียน front-end ให้ตรง
กับดักตัวจริงคือ feature parity: กราฟ `.tflite` ไม่มี FFT หรือ mel อยู่ข้างใน ถ้า front-end คลาดนิดเดียวคะแนนจะเพี้ยนเงียบ ๆ

## ตัวอย่างสมบูรณ์

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นหรือใน `shared/` ด้วย:

- [shared/training/quantize_vela.sh](../../shared/training/quantize_vela.sh) — Compile an int8 .tflite for the Ethos-U55 NPU on the PSoC Edge board.

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. ทำไมการเพิ่มโมเดลในซอร์สตัวเต็มจึงไม่ต้องแก้โมดูล edge_ai ของ MicroPython *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) เพราะ MicroPython เก็บชื่อโมเดลไว้ทุกตัวอยู่แล้ว
   - ข) เพราะทะเบียนเป็น shape-driven MicroPython ถาม count() และ model(n) จาก s_models[] ทุกครั้ง
   - ค) เพราะ IPC ส่งไฟล์โมเดลให้เอง
   - ง) เพราะต้องแก้ Emulator แทน

   <details><summary>เฉลย</summary>

   **ข** — ไม่มีชื่อโมเดลใดถูก hard-code ฝั่ง Python เพิ่มแถวที่ปลายทาง ทั้งสายเห็นเอง

   </details>

2. ถ้าใช้ SDK สาธารณะที่ ai_engine มาเป็นไลบรารี prebuilt จะเพิ่มโมเดลที่ไม่มีช่องอยู่แล้วได้อย่างไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) แก้ ai_engine.c ใน archive
   - ข) เรียก ai_engine_register(&desc) จากโค้ดของเราตอนรัน
   - ค) เพิ่มชื่อใน edge_ai.py
   - ง) ทำไม่ได้เลย

   <details><summary>เฉลย</summary>

   **ข** — Route 0 ของคู่มือ SDK ให้ engine เพิ่มแถวจาก descriptor ของเรา โดยไม่ต้อง rebuild archive

   </details>

3. AIM_FALL_dequeue คืน −1 หลัง enqueue ได้ไม่กี่ครั้ง แปลว่าอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) โมเดลพัง
   - ข) NODATA หน้าต่างยังไม่เต็ม ต้อง enqueue ต่อ
   - ค) คลาสที่ชนะคือ −1
   - ง) arena ไม่พอ

   <details><summary>เฉลย</summary>

   **ข** — โมเดลแบบ streaming ต้องได้ข้อมูลครบหน้าต่าง L ครั้งก่อน dequeue จึงคืน 0 พร้อมคะแนน

   </details>

4. เพิ่มโมเดลแล้วโผล่ใน models() แต่ select() โยน OSError ทุกครั้ง สาเหตุที่เป็นไปได้มากคืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) ชื่อโมเดลยาวเกินไป
   - ข) init() คืนค่าติดลบ เช่น tensor arena เล็กเกินกว่าที่กราฟต้องใช้
   - ค) ลืมใส่ labels
   - ง) Wi-Fi ไม่ติด

   <details><summary>เฉลย</summary>

   **ข** — select ยืนยันด้วยการสังเกต ถ้าโมเดล init ไม่ผ่าน engine ไม่สลับ Q_ACTIVE จึงไม่เคยเท่ากับที่ขอ

   </details>

5. ทำไมผู้เขียนเลือก Fall Detection เป็นโมเดลตัวแรกที่เพิ่ม *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) เพราะแม่นที่สุด
   - ข) เพราะใช้ IMU จึงยืม feed_imu เดิมได้ และ front-end เบาที่สุด ไม่มี FFT ให้พลาด
   - ค) เพราะไม่ต้องผ่าน Vela
   - ง) เพราะเป็น float32

   <details><summary>เฉลย</summary>

   **ข** — เลือกเส้นทางที่พิสูจน์แล้วก่อน โมเดลเสียงต้องทำ FFT และ mel ให้ตรงกับตอนฝึกซึ่งเป็นจุดพังเงียบที่พบบ่อยที่สุด

   </details>

## แล็บ

- [ ] เขียน ROW ของ Fall Detection ด้วยมือในบันทึกการเรียน พร้อมชี้ว่าฟิลด์ใดไปโผล่ใน `edge_ai.models()`
- [ ] เปิดคู่มือ Filling a model slot ของ SDK แล้วสรุปความต่างของ Route 0 (`ai_engine_register`) กับ Route 1 (ใส่แทนช่องเดิม) เป็นสองบรรทัด
- [ ] ประเมินงบหน่วยความจำของโมเดลที่ weights 40,000 ไบต์และ arena 20 KB ว่ากิน flash กับ RAM ส่วนใดบ้าง

## ไปต่อ

บทเรียน 7.4 เราจะใช้ `s19_extend_model.py` สร้าง ROW จากสเปก ตรวจทะเบียนด้วย `count()` กับ `models()` แล้วรันโมเดลที่เพิ่มเข้าไป

บทเรียนถัดไป: [บทเรียน 7.4 — ลงมือทำ: ให้โมเดลใหม่โผล่ใน edge_ai.models()](../l04-extend-model-lab/README.md)

## สะท้อนคิด

- ถ้าต้องเพิ่มโมเดลเสียงที่ฝึกเอง front-end ใดบ้างที่ต้องทำให้ตรงกับตอนฝึก
- ข้อดีข้อเสียของการเพิ่มโมเดลตอน build กับตอนรันต่างกันอย่างไรสำหรับสินค้าที่อัปเดตผ่าน OTA
