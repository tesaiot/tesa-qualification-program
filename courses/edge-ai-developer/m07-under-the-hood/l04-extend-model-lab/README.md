---
id: edgeai-dev.m07.l04
lang: th
title: {th: 'ลงมือทำ: ให้โมเดลใหม่โผล่ใน edge_ai.models()', en: 'Hands-on: make a new model appear in edge_ai.models()'}
summary: {th: เติมห้าจุดใน s19_extend_model.py ที่ข้ามสองฝั่ง ครึ่งบนสร้าง C ROW จากสเปกในภาษา Python ครึ่งล่างถามทะเบียนด้วย count() และ models() แล้วเลือกรันโมเดลของเรา จากนั้นเพิ่มโมเดลเข้าเฟิร์มแวร์จริง ยืนยันด้วยจำนวนโมเดลก่อนและหลัง และเดิน checklist ก่อนเชื่อผลบนฮาร์ดแวร์, en: 'Fill five points in s19_extend_model.py, which spans two worlds - the top half builds a C ROW from a Python spec, the bottom half queries the registry with count() and models() and runs your model. Then add the model to real firmware, prove it with the model count before and after, and walk the checklist before trusting the hardware.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m07.l03]
objectives:
  - {th: เติมห้าจุดใน practice/s19_extend_model.py จนพิมพ์ ROW ที่มีสี่ชื่อฟังก์ชันและคลาสครบ และหา index ของโมเดลในทะเบียนจากชื่อได้ (บน Emulator จะยังไม่เจอ Fall ซึ่งถูกต้อง), en: 'Fill the five points in practice/s19_extend_model.py until it prints a ROW with all four function names and the classes, and finds the model''s registry index by name (on the emulator Fall is not found yet, which is correct).'}
  - {th: เพิ่มโมเดลเข้าเฟิร์มแวร์ (สามการแก้ในซอร์สตัวเต็ม หรือ ai_engine_register() ใน SDK สาธารณะ) แล้วแสดง edge_ai.count() ก่อนและหลัง ชื่อใหม่ใน models() และ verdict จริงเมื่อ select, en: 'Add a model to the firmware (three edits in the full source, or ai_engine_register() in the public SDK), then show edge_ai.count() before and after, the new name in models(), and a real verdict when selected.'}
  - {th: 'เดิน checklist ก่อนเชื่อผล (ตรวจสัญลักษณ์ด้วย nm, section .ml_weights, clean build, hard power-cycle) และอธิบายเหตุผลของแต่ละข้อ', en: 'Walk the pre-trust checklist (symbols checked with nm, the .ml_weights section, a clean build, a hard power cycle) and explain the reason for each item.'}
develops: [{skill: build.vendor-sdk, to: 2}, {skill: ai.model-deploy, to: 3}, {skill: lang.micropython, to: 2}]
assesses: [{skill: build.vendor-sdk, level: 2, evidence: practice/s19_extend_model.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 7.4 — ลงมือทำ: ให้โมเดลใหม่โผล่ใน edge_ai.models()

> โมดูล 7 — ใต้ฝากระโปรงและการต่อเติม · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เติมห้าจุดใน s19_extend_model.py ที่ข้ามสองฝั่ง ครึ่งบนสร้าง C ROW จากสเปกในภาษา Python ครึ่งล่างถามทะเบียนด้วย count() และ models() แล้วเลือกรันโมเดลของเรา จากนั้นเพิ่มโมเดลเข้าเฟิร์มแวร์จริง ยืนยันด้วยจำนวนโมเดลก่อนและหลัง และเดิน checklist ก่อนเชื่อผลบนฮาร์ดแวร์

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เติมห้าจุดใน practice/s19_extend_model.py จนพิมพ์ ROW ที่มีสี่ชื่อฟังก์ชันและคลาสครบ และหา index ของโมเดลในทะเบียนจากชื่อได้ (บน Emulator จะยังไม่เจอ Fall ซึ่งถูกต้อง)
2. เพิ่มโมเดลเข้าเฟิร์มแวร์ (สามการแก้ในซอร์สตัวเต็ม หรือ ai_engine_register() ใน SDK สาธารณะ) แล้วแสดง edge_ai.count() ก่อนและหลัง ชื่อใหม่ใน models() และ verdict จริงเมื่อ select
3. เดิน checklist ก่อนเชื่อผล (ตรวจสัญลักษณ์ด้วย nm, section .ml_weights, clean build, hard power-cycle) และอธิบายเหตุผลของแต่ละข้อ

## ก่อนเริ่ม

ผ่านบทเรียน 7.3 มาแล้ว รู้จักสามการแก้ สัญญาสี่ฟังก์ชัน และทางเทียบเท่าใน SDK
ถ้าจะทำส่วนเฟิร์มแวร์ ติดตั้ง ModusToolbox และ clone [SDK สาธารณะ](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) ไว้ พร้อมโมเดลที่ห่อตามสัญญาสี่ฟังก์ชันแล้ว

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — ครึ่งบนของไฟล์ (สเปกกับ ROW) ซ้อมบน Emulator ได้ การเพิ่มโมเดลต้อง build เฟิร์มแวร์ด้วย ModusToolbox แล้วลงบอร์ด ซอร์สตัวเต็มยังไม่เปิดเผย จึงใช้ SDK สาธารณะกับ ai_engine_register() แทนการแก้ ai_engine.c
- **เรียนมาก่อน:** [บทเรียน 7.3 — เพิ่มโมเดลของเราเอง: สามการแก้ สัญญาสี่ฟังก์ชัน และ Vela](../l03-add-your-own-model/README.md)

## แนวคิด

ไฟล์นี้ข้ามฝั่ง: เขียนสเปก → พิมพ์ C ROW ที่ต้องวาง → ถามทะเบียนว่าโผล่ยัง → เลือกรันแล้วอ่าน verdict ห้าจุดที่เติมคือ
(1) `"sensor": edge_ai.SENSOR_IMU` กับ `"labels": ["normal", "fall"]` ใน `SPEC` (2) `deq_fn = "AIM_%s_dequeue" % prefix` ใน `make_row()`
ที่ประกอบข้อความ `#if defined(EDGE_AI_MODEL_fall)` / `#define FALL_ROW {...}` / `#endif` ให้ก๊อปไปวาง ลืมจุดนี้ ROW จะมี `.dequeue = None` ซึ่งคอมไพล์ไม่ผ่าน
(3) `n = edge_ai.count()` (4) `mine = i` เมื่อชื่อตรง ซึ่งหา index จากชื่อ ไม่ hard-code ตัวเลข และ (5) `edge_ai.select(idx)` ตามด้วย `r = edge_ai.result()`
ห่อด้วย `try/except OSError` เพราะโมเดลใหม่อาจ init ไม่ผ่าน

บน Emulator ใช้ซ้อมครึ่งบนได้ ทะเบียนมีห้าโมเดลและยังไม่มี Fall ซึ่งถูกต้อง เพราะเบราว์เซอร์ build C ไม่ได้ ครึ่งล่างทดลองกับโมเดลที่มีอยู่ เช่น Motion
บนบอร์ด ในซอร์สตัวเต็มทำสามการแก้ แล้ว `rm -rf proj_cm55/build; make program EDGE_AI_MODEL=combo` ถ้าใช้ SDK สาธารณะ ให้เรียก `ai_engine_register(&desc)`
จากโค้ดของเราตอนบูต แล้ว build ด้วย ModusToolbox จากนั้นกด Re-check: `count()` ต้องเพิ่มขึ้น (บนบอร์ดหกเป็นเจ็ด) ชื่อใหม่ขึ้นสีเขียว แล้ว Run mine
ขยับบอร์ดจนคลาสสลับ `normal` กับ `fall` ก่อนเชื่อผลให้เดิน checklist: ทดสอบ `.tflite` ใน Python ก่อนห่อ ตรวจด้วย `nm` ว่าสัญลักษณ์ไม่ชนกัน
weights ก้อนใหญ่อยู่ใน `.ml_weights` front-end ตรงกับตอนฝึก clean build และ **hard power-cycle** หนึ่งการเปลี่ยนต่อหนึ่งการ flash

## ตัวอย่างสมบูรณ์

`s19_extend_model_full.py` รองรับทั้ง `STYLE = "AIM"` (โมเดลจาก DEEPCRAFT Studio) และ `"IMAI"` (Ready-Model แบบ `.a`) ตรวจว่าสัญญาสี่ฟังก์ชันครบ
เทียบ `count()` ก่อนและหลัง และแยกสี verdict ตาม `CONF_FLOOR` พร้อม latency

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/s19_extend_model_full.py](examples/s19_extend_model_full.py) | เพิ่มโมเดลของเราเองเข้า Edge AI (ฉบับเต็ม) |

## ฝึกเติม

คอมเมนต์ `# เติม` อยู่ที่บรรทัด 44 (`SPEC` sensor และ labels), 60 (`deq_fn`), 129 (`count`), 138 (`mine = i`) และ 156 (`select` กับ `result`)
ถ้า ROW ที่พิมพ์มี `None` อยู่ จุดที่ 60 ยังว่าง ถ้า diff ของจำนวนโมเดลเป็นศูนย์เสมอ ตรวจจุดที่ 129

| ไฟล์ฝึก | เรื่อง |
|---|---|
| [practice/s19_extend_model.py](practice/s19_extend_model.py) | เพิ่มโมเดลของเราเองเข้า Edge AI (ฉบับฝึกเติมโค้ด) |

## เฉลย

เปิดเฉลยหลังจากลองเองแล้วอย่างน้อยหนึ่งรอบ และอ่าน [วิธีใช้เฉลย](../../README.md#วิธีใช้เฉลย) ก่อน

| เฉลย | คู่กับ |
|---|---|
| [solution/s19_extend_model.py](solution/s19_extend_model.py) | [practice/s19_extend_model.py](practice/s19_extend_model.py) |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. ROW ที่พิมพ์ออกมามี .dequeue = None จุดใดยังว่าง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) จุดที่ 1 SPEC
   - ข) จุดที่ 2 deq_fn ใน make_row()
   - ค) จุดที่ 3 count()
   - ง) จุดที่ 5 select

   <details><summary>เฉลย</summary>

   **ข** — make_row ประกอบชื่อฟังก์ชันทั้งสี่จาก prefix ถ้า deq_fn ยังเป็น None ข้อความ ROW จะคอมไพล์ไม่ผ่าน

   </details>

2. รันบน Emulator แล้ว scan_registry() ไม่เจอ Fall Detection หมายความว่าอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) โค้ดผิด
   - ข) ถูกต้องแล้ว Emulator มีห้าโมเดลที่คอมไพล์มาแล้ว และ build C ในเบราว์เซอร์ไม่ได้
   - ค) ต้องรีเฟรชเบราว์เซอร์
   - ง) ต้องเพิ่มชื่อใน edge_ai.py

   <details><summary>เฉลย</summary>

   **ข** — การเพิ่มโมเดลต้องมี toolchain และ flash ลงบอร์ด นี่คือเส้นแบ่งระหว่างงานเฟิร์มแวร์กับงานระดับแอป

   </details>

3. หลักฐานข้อใดยืนยันว่าเพิ่มโมเดลสำเร็จจริง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) build ผ่านโดยไม่มี error
   - ข) count() เพิ่มขึ้น ชื่อใหม่อยู่ใน models() และ select แล้ว verdict สลับตามการขยับจริง
   - ค) ไฟล์โมเดลอยู่ในโฟลเดอร์ถูกที่
   - ง) ROW พิมพ์ออกมาครบ

   <details><summary>เฉลย</summary>

   **ข** — build ผ่านหรือไฟล์อยู่ถูกที่ยังไม่ได้แปลว่าทั้งสี่ฟังก์ชันต่อสายถูก ต้องเห็นทั้งทะเบียนและ verdict บนบอร์ด

   </details>

4. ทำไม checklist จึงให้ hard power-cycle ก่อนเชื่อผลบนฮาร์ดแวร์ *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) เพื่อล้างไฟล์ใน flash
   - ข) หลัง flash เซนเซอร์และ NPU บางตัวต้อง init ใหม่จากไฟจริง ไม่งั้นค่าที่อ่านอาจค้างจากรอบก่อน
   - ค) เพื่อให้ Wi-Fi ต่อใหม่
   - ง) ไม่จำเป็น

   <details><summary>เฉลย</summary>

   **ข** — หนึ่งการเปลี่ยนต่อหนึ่งการ flash แล้ว power-cycle ก่อนเชื่อ ช่วยให้แน่ใจว่าผลที่เห็นมาจากการเปลี่ยนครั้งนี้จริง

   </details>

## แล็บ

**MVP ของชุดบทเรียน 7.3–7.4:** โมเดลใหม่ที่เพิ่มเอง `edge_ai.count()` เพิ่มขึ้น ชื่อโผล่ใน `edge_ai.models()` และเลือกรันแล้วได้ verdict จริงบนบอร์ด

- [ ] เติมไฟล์ฝึกครบห้าจุด รันบน Emulator แล้วตรวจ ROW ที่พิมพ์ออกมาทีละฟิลด์
- [ ] บนบอร์ด จด `edge_ai.count()` ก่อนเพิ่มโมเดล
- [ ] เพิ่มโมเดล (สามการแก้ในซอร์สตัวเต็ม หรือ `ai_engine_register()` ใน SDK) build แล้ว hard power-cycle จด `count()` หลังเพิ่ม และ verdict เมื่อ Run mine
- [ ] เขียน checklist ที่คุณเดินจริงลงบันทึกการเรียน พร้อมหลักฐานของแต่ละข้อ (เช่นผลของ `nm`)

## ไปต่อ

โมดูลถัดไป (Capstone) เราจะรวมทุกอย่างตั้งแต่ DAQ ถึงแอปเป็นแอป Edge AI ของเราเองในไฟล์เดียว

บทเรียนถัดไป: [บทเรียน 8.1 — ออกแบบ capstone: Guardian สามเสาในไฟล์เดียว](../../m08-capstone/l01-capstone-design/README.md)

## สะท้อนคิด

- ถ้า count() เพิ่มแล้วแต่ verdict ไม่เคยเปลี่ยนเลย คุณจะไล่หาสาเหตุจากชั้นไหนก่อน
- ในสินค้าจริง คุณจะเลือกเพิ่มโมเดลตอน build หรือโหลดตอนรัน และเพราะอะไร
