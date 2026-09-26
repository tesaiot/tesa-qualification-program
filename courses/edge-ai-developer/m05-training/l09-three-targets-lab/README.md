---
id: edgeai-dev.m05.l09
lang: th
title: {th: 'ลงมือทำ: เทียบสามเป้าหมาย MCU, Web และ PC', en: 'Hands-on: comparing three targets, MCU, web and PC'}
summary: {th: 'เติมห้าจุดใน s14_tflite_board.py ให้ bench โมเดล int8 บน PC เป็น ground truth ทั้ง accuracy และ latency เรียก Vela ผ่าน quantize_vela.sh แล้วพิมพ์ตารางเทียบ MCU, Web และ PC จากนั้นข้ามจาก Python ไป MicroPython อ่าน latency จริงจากบอร์ดมาเติมช่อง MCU และตัดสินใจว่าโมเดลควรอยู่ที่ไหน', en: 'Fill five points in s14_tflite_board.py to bench the int8 model on the PC as ground truth for accuracy and latency, call Vela through quantize_vela.sh and print the MCU, web and PC comparison table; then cross from Python to MicroPython, read a real latency from the board to fill the MCU row, and decide where the model should live.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [edgeai-dev.m05.l08]
objectives:
  - {th: เติมห้าจุดใน practice/s14_tflite_board.py จนพิมพ์ accuracy ของ int8 และ latency ต่อ window ที่ไม่เป็นศูนย์บน PC รัน Vela เมื่อมี และพิมพ์ตารางสามเป้าหมาย, en: 'Fill the five points in practice/s14_tflite_board.py until it prints the int8 accuracy and a non-zero per-window latency on the PC, runs Vela when available and prints the three-target table.'}
  - {th: อ่าน latency_ms จากบอร์ดด้วย edge_ai แล้วเติมช่อง MCU ด้วย --mcu-ms โดยระบุชัดว่าเป็นโมเดลของเราหรือโมเดล Motion ที่ใช้เป็นจุดอ้างอิง, en: 'Read latency_ms from the board with edge_ai and fill the MCU row with --mcu-ms, stating clearly whether it is your model or the built-in Motion model used as a reference.'}
  - {th: อธิบายจากตารางที่เติมแล้วว่าทำไม accuracy ควรตรงกันแต่ latency ต่างกัน และเลือกเป้าหมายให้โจทย์ที่กำหนดพร้อมเหตุผล, en: 'Use the completed table to explain why accuracy should agree while latency differs, and choose a target for a given scenario with reasons.'}
develops: [{skill: ai.model-deploy, to: 3}, {skill: lang.python, to: 2}, {skill: lang.micropython, to: 2}]
assesses: [{skill: ai.model-deploy, level: 2, evidence: practice/s14_tflite_board.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 5.9 — ลงมือทำ: เทียบสามเป้าหมาย MCU, Web และ PC

> โมดูล 5 — ฝึกโมเดลและนำไปใช้หลายเป้าหมาย · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เติมห้าจุดใน s14_tflite_board.py ให้ bench โมเดล int8 บน PC เป็น ground truth ทั้ง accuracy และ latency เรียก Vela ผ่าน quantize_vela.sh แล้วพิมพ์ตารางเทียบ MCU, Web และ PC จากนั้นข้ามจาก Python ไป MicroPython อ่าน latency จริงจากบอร์ดมาเติมช่อง MCU และตัดสินใจว่าโมเดลควรอยู่ที่ไหน

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เติมห้าจุดใน practice/s14_tflite_board.py จนพิมพ์ accuracy ของ int8 และ latency ต่อ window ที่ไม่เป็นศูนย์บน PC รัน Vela เมื่อมี และพิมพ์ตารางสามเป้าหมาย
2. อ่าน latency_ms จากบอร์ดด้วย edge_ai แล้วเติมช่อง MCU ด้วย --mcu-ms โดยระบุชัดว่าเป็นโมเดลของเราหรือโมเดล Motion ที่ใช้เป็นจุดอ้างอิง
3. อธิบายจากตารางที่เติมแล้วว่าทำไม accuracy ควรตรงกันแต่ latency ต่างกัน และเลือกเป้าหมายให้โจทย์ที่กำหนดพร้อมเหตุผล

## ก่อนเริ่ม

ผ่านบทเรียน 5.8 มาแล้ว เข้าใจว่า Vela ทำอะไรและไฟล์ใดไปเป้าหมายใด
คัดลอก `practice/s14_tflite_board.py` ไปวางใน [`shared/training`](../../shared/training/) ที่มี `dataset_tools.py`, `model_int8.tflite`, `.norm.npz` และ `quantize_vela.sh`

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว (บทเรียนนี้ต้องใช้บอร์ดจริง) — bench และ Vela ทำบน PC ได้ ตัวเลข latency ของ MCU ต้องมาจากบอร์ดจริง เพราะ Emulator ไม่มี NPU
- **เรียนมาก่อน:** [บทเรียน 5.8 — quantize และ Vela: เอาโมเดลของเราขึ้น Ethos-U55](../l08-quantize-and-vela/README.md)

## แนวคิด

ทั้งไฟล์อ่านเป็นประโยคเดียว: bench int8 บน PC เป็น ground truth → รัน Vela ได้ไฟล์ MCU → วางตัวเลขเทียบสามเป้าหมาย → ชี้ทางไปอ่าน latency จริงบนบอร์ด
ห้าจุดที่เติมอยู่ใน `bench_int8()` สี่จุด คือ (1) normalize ด้วย mean/std (2) quantize ด้วย scale/zero ของ input (3) จับเวลาเฉพาะช่วง
`it.invoke()` ด้วย `time.perf_counter()` แล้วสะสมเป็น ms (4) `correct += int(o.argmax() == y[i])` และอีกหนึ่งจุดใน `run_vela()` คือ
(5) `subprocess.run(["./quantize_vela.sh", int8_path], check=True)` ที่ห่อ try/except ไว้ เครื่องที่ไม่มี vela จะได้ข้อความแล้วข้ามไป ไม่ตายทั้งสคริปต์

เราวัด "เวลาอนุมานล้วน" ไม่รวม normalize หรือ quantize เพื่อให้เทียบกับตัวเลขบนบอร์ดได้ตรงประเด็น บน PC ใช้ `time.perf_counter()` คร่อม `invoke()`
ในเบราว์เซอร์ใช้ `performance.now()` คร่อม `model.run()` ส่วน MCU ต้องมาจากบอร์ดเท่านั้น: เลือกโมเดลด้วย `edge_ai.select(n)` แล้วอ่าน
`edge_ai.result()["latency_ms"]` หรือ `edge_ai.latency()` (ค่าล่าสุดหน่วย ms) เก็บหลายครั้งเพื่อดูทั้งค่าเฉลี่ยและค่าสูงสุด แล้วส่งกลับด้วย
`python s14_tflite_board.py --mcu-ms <ค่า>` ตารางจะเติมช่อง MCU ให้ ช่อง accuracy ของ MCU ใส่ `pc_acc` ไว้ก่อน แล้วยืนยันด้วย verdict จริงบนบอร์ด

การพาโมเดลของเราเองขึ้น NPU เป็นสาย researcher ที่ต้อง build เฟิร์มแวร์: ห่อไฟล์ Vela ด้วยสัญญา `AIM_*` ลงทะเบียนโมเดล build แล้ว hard power-cycle
ก่อนเชื่อผล ใน SDK สาธารณะใช้ `ai_engine_register()` แทนการแก้ `ai_engine.c` ถ้ายังไม่ถึงขั้นนั้น ใช้ latency ของโมเดล Motion ที่มากับบอร์ดเป็นจุดอ้างอิงได้
แต่ต้องเขียนกำกับว่าเป็นคนละโมเดล ความสำเร็จคือบอกได้ว่าทำไม accuracy สามเป้าหมายควรตรงกันแต่ latency ต่างคนละระดับ และงานแบบไหนควรอยู่ที่ใด

## ตัวอย่างสมบูรณ์

`s14_tflite_board_full.py` เพิ่ม bench เส้นทาง Web (ไฟล์ float I/O ที่สร้างด้วย `convert_web.py`) คอลัมน์พลังงานแบบเชิงคุณภาพ (ไม่ได้วัดจริง) ตัวเลือก `--no-vela` และ `--show-mpy` ที่พิมพ์โค้ด MicroPython
สำหรับอ่าน latency บนบอร์ด เปิดเทียบหลังเติมไฟล์ฝึกเสร็จ

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/s14_tflite_board_full.py](examples/s14_tflite_board_full.py) | แล็บเทียบเป้าหมายครบวง: PC vs Web vs MCU จากโมเดลไฟล์เดียว (ฉบับเต็ม) |

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นหรือใน `shared/` ด้วย:

- [shared/training](../../shared/training)
- [shared/training/quantize_vela.sh](../../shared/training/quantize_vela.sh) — Compile an int8 .tflite for the Ethos-U55 NPU on the PSoC Edge board.

## ฝึกเติม

คอมเมนต์ `# เติม` อยู่ที่บรรทัด 47 (normalize), 52 (quantize), 58 (จับเวลา invoke), 68 (นับคลาสถูก) และ 83 (เรียก `quantize_vela.sh`)
ถ้า latency เป็น 0.00 ms ตลอด จุดที่ 58 ยังว่าง ถ้า accuracy แปลก ให้ตรวจจุดที่ 47 และ 52 ก่อน เพราะ front-end คือจุดพังบ่อยที่สุด

| ไฟล์ฝึก | เรื่อง |
|---|---|
| [practice/s14_tflite_board.py](practice/s14_tflite_board.py) | quantize -> Vela -> รันบน NPU แล้วเทียบสามเป้าหมาย (ฉบับฝึกเติมโค้ด) |

## เฉลย

เปิดเฉลยหลังจากลองเองแล้วอย่างน้อยหนึ่งรอบ และอ่าน [วิธีใช้เฉลย](../../README.md#วิธีใช้เฉลย) ก่อน

| เฉลย | คู่กับ |
|---|---|
| [solution/s14_tflite_board.py](solution/s14_tflite_board.py) | [practice/s14_tflite_board.py](practice/s14_tflite_board.py) |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. ตารางแสดง latency ของ PC เป็น 0.00 ms ทุกครั้ง จุดใดยังว่าง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) เติม 1 normalize
   - ข) เติม 3 จับเวลาและเรียก invoke()
   - ค) เติม 4 นับคลาสถูก
   - ง) เติม 5 เรียก Vela

   <details><summary>เฉลย</summary>

   **ข** — placeholder คือ pass จึงไม่มีทั้งการ invoke และการบวก total_ms ผลคือ latency 0 และ accuracy ที่ไม่มีความหมาย

   </details>

2. สคริปต์พิมพ์ "ยังไม่มี vela ในเครื่องนี้" ควรทำอย่างไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) ลบจุดที่ 5 ทิ้ง
   - ข) รันสคริปต์ใน Docker image ของบทเรียน 5.3–5.5 ที่ติดตั้ง ethos-u-vela ไว้
   - ค) ฝึกโมเดลใหม่
   - ง) เปลี่ยนไปใช้ไฟล์ model_web.tflite

   <details><summary>เฉลย</summary>

   **ข** — try/except ทำให้สคริปต์ไม่ตาย แต่จะยังไม่มีไฟล์ _vela จนกว่าจะรันในที่ที่มี vela

   </details>

3. ทำไมเลข latency ของ MCU วัดจาก PC หรือจาก BENTO Emulator ไม่ได้ *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) เพราะ PC กับ Emulator ไม่มี Ethos-U55 เวลาที่วัดได้จึงเป็นของ CPU หรือเบราว์เซอร์ ไม่ใช่ของ NPU
   - ข) เพราะ time.perf_counter() ใช้ไม่ได้
   - ค) เพราะ latency ของ MCU เท่ากับ PC เสมอ
   - ง) เพราะ Vela ต้องรันบนบอร์ด

   <details><summary>เฉลย</summary>

   **ก** — ต้องอ่านจาก edge_ai บนบอร์ดจริงเท่านั้น เลขบน Emulator คือเวลาของ runtime ในเบราว์เซอร์

   </details>

4. แท็กติดสัตว์ใส่แบตที่ต้องอยู่ได้หลายเดือนและจำแนกท่าทางตลอดเวลา ควรรันโมเดลที่ไหน *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) Cortex-A
   - ข) MCU + NPU ด้วยไฟล์ _vela.tflite
   - ค) เบราว์เซอร์
   - ง) PC ใน Docker

   <details><summary>เฉลย</summary>

   **ข** — งานนี้ต้องการพลังงานต่อการอนุมานต่ำที่สุดและไม่มี OS ให้ใช้ ขั้น Vela ที่จ่ายเพิ่มตอน build คุ้มกับแบตที่อยู่นานขึ้นทุกครั้งที่รัน

   </details>

## แล็บ

**MVP ของชุดบทเรียน 5.8–5.9:** ตารางเทียบสามเป้าหมาย (MCU, Web, PC) ด้วยตัวเลขจริง อธิบายได้ว่าทำไม accuracy ตรงกันแต่ latency ต่างกัน และทำไม MCU ต้องผ่าน Vela

- [ ] เติมไฟล์ฝึกครบห้าจุด รันใน Docker image เดิมจนได้ accuracy และ latency ของ int8 บน PC และไฟล์ `_vela.tflite`
- [ ] บนบอร์ด เลือกโมเดลแล้วอ่าน `edge_ai.latency()` อย่างน้อย 20 ครั้ง จดค่าเฉลี่ยและค่าสูงสุด ระบุว่าเป็นโมเดลใด
- [ ] รัน `python s14_tflite_board.py --mcu-ms <ค่าเฉลี่ย>` แล้วเก็บตารางลงบันทึกการเรียน
- [ ] เลือกเป้าหมายให้งานสามแบบ (แท็กใส่แบต, เดโมให้ลูกค้า, เกตเวย์หน้างาน) พร้อมเหตุผลจากตาราง

## ไปต่อ

โมดูลถัดไป (แอป Edge AI) เราจะเอาโมเดลมาทำแอปจริง หนึ่ง verdict หนึ่งงาน เริ่มจากแอปที่โฟกัสโมเดลเดียว

บทเรียนถัดไป: [บทเรียน 6.1 — หกโมเดลกับ edge_ai API: แอปที่โฟกัสโมเดลเดียว](../../m06-apps/l01-focused-apps/README.md)

## สะท้อนคิด

- latency บน PC ของคุณเทียบกับบน NPU ต่างกันกี่เท่า และตัวเลขนี้ยุติธรรมแค่ไหนเมื่อ PC ไม่ได้ถูกจำกัดพลังงาน
- ถ้าต้องเลือกระหว่าง accuracy สูงขึ้น 2% กับ latency ต่ำลงครึ่งหนึ่ง งานของคุณควรเลือกอะไร
