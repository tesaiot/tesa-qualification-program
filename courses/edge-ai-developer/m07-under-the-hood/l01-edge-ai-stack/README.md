---
id: edgeai-dev.m07.l01
lang: th
title: {th: 'สแตก Edge AI: tri-core, ai_engine, IPC model link และ TFLite-Micro', en: 'The edge AI stack: tri-core, ai_engine, the IPC model link and TFLite-Micro'}
summary: {th: 'เปิดฝากระโปรงดูว่าทุกครั้งที่เรียก edge_ai.result() เกิดอะไรขึ้น ไล่สแตกจากสามคอร์ของ PSoC Edge E84, ai_engine และทะเบียนโมเดลบน CM55, IPC model link ที่แยก control plane กับ query plane, การ publish ผลแบบ lock-free ไปจนถึง TFLite-Micro ที่เป็น runtime จริงของทั้งโมเดล int8 และ float32', en: 'Open the hood on what happens every time you call edge_ai.result() - the three cores of the PSoC Edge E84, ai_engine and the model registry on the CM55, the IPC model link with its control and query planes, lock-free result publishing, and TFLite-Micro as the real runtime for both int8 and float32 models.'}
level: L3
time_min: {concept: 55, practise: 5, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m06.l06]
objectives:
  - {th: 'วางชิ้นส่วนของสแตก Edge AI ลงบนสามคอร์ (CM33_S, CM33_NS, CM55) ได้ถูกต้อง และอธิบายเหตุผลที่แบ่งงานแบบนั้น', en: 'Place the parts of the edge AI stack on the three cores (CM33_S, CM33_NS, CM55) correctly and explain why the work is split that way.'}
  - {th: อธิบายความต่างของโมเดลที่ขอ (s_active) กับโมเดลที่สลับแล้วจริง (s_current) และเหตุผลที่ select() ยืนยันด้วยการสังเกต Q_ACTIVE แล้วโยน OSError ได้, en: 'Explain the difference between the requested model (s_active) and the model actually switched in (s_current), and why select() confirms by observing Q_ACTIVE and can raise OSError.'}
  - {th: จับคู่ key ของ dict จาก edge_ai.result() กับฟิลด์ของ ai_result_t ได้ และอธิบายว่าทำไมการ publish จึงเป็นแบบ lock-free, en: 'Map the keys of the edge_ai.result() dict to the fields of ai_result_t, and explain why results are published lock-free.'}
  - {th: อธิบายว่า TFLite-Micro คือ runtime จริง (โมเดล int8 ที่ผ่าน Vela ไป NPU ส่วน float32 รันบน CPU) และโค้ดจาก DEEPCRAFT เป็นเปลือกที่ให้สี่ฟังก์ชัน, en: 'Explain that TFLite-Micro is the real runtime (Vela-compiled int8 models go to the NPU, float32 runs on the CPU) and that DEEPCRAFT code is a wrapper exposing four functions.'}
develops: [{skill: hw.architecture, to: 3}, {skill: rtos.multicore-ipc, to: 2}, {skill: ai.model-deploy, to: 3}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 7.1 — สแตก Edge AI: tri-core, ai_engine, IPC model link และ TFLite-Micro

> โมดูล 7 — ใต้ฝากระโปรงและการต่อเติม · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เปิดฝากระโปรงดูว่าทุกครั้งที่เรียก edge_ai.result() เกิดอะไรขึ้น ไล่สแตกจากสามคอร์ของ PSoC Edge E84, ai_engine และทะเบียนโมเดลบน CM55, IPC model link ที่แยก control plane กับ query plane, การ publish ผลแบบ lock-free ไปจนถึง TFLite-Micro ที่เป็น runtime จริงของทั้งโมเดล int8 และ float32

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. วางชิ้นส่วนของสแตก Edge AI ลงบนสามคอร์ (CM33_S, CM33_NS, CM55) ได้ถูกต้อง และอธิบายเหตุผลที่แบ่งงานแบบนั้น
2. อธิบายความต่างของโมเดลที่ขอ (s_active) กับโมเดลที่สลับแล้วจริง (s_current) และเหตุผลที่ select() ยืนยันด้วยการสังเกต Q_ACTIVE แล้วโยน OSError ได้
3. จับคู่ key ของ dict จาก edge_ai.result() กับฟิลด์ของ ai_result_t ได้ และอธิบายว่าทำไมการ publish จึงเป็นแบบ lock-free
4. อธิบายว่า TFLite-Micro คือ runtime จริง (โมเดล int8 ที่ผ่าน Vela ไป NPU ส่วน float32 รันบน CPU) และโค้ดจาก DEEPCRAFT เป็นเปลือกที่ให้สี่ฟังก์ชัน

## ก่อนเริ่ม

ผ่านโมดูล 1 ถึง 6 มาแล้ว ใช้ `edge_ai` ครบทั้ง `models`, `select`, `result`, `on_result` และ `stop`
เปิด [`ai_engine.h`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/main/bento-firmware-template-mtb-mpy/lib/edge_ai/include/ai_engine.h) กับ [`ipc_model_link_defs.h`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/main/bento-firmware-template-mtb-mpy/bento_libs/claw/common/shared/include/ipc_model_link_defs.h) ของ SDK ไว้คู่จอ

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — เป็นบทเรียนอ่านสแตก Emulator เลียนแบบ API ฝั่งอ่านแต่ไม่มี IPC จริง ซอร์สเฟิร์มแวร์ที่คอร์สต้นฉบับอ้าง (ai_engine.c, deepcraft_task.c) ยังไม่เปิดเผย ส่วนที่เปิดคือ header ใน SDK สาธารณะ
- **เรียนมาก่อน:** [บทเรียน 6.6 — ลงมือทำ: ส่งเหตุการณ์ที่ fuse แล้วขึ้น MQTT](../../m06-apps/l06-fusion-iot-lab/README.md)

## ดูของจริงก่อน

เขียนบรรทัดที่ใช้มาทั้งคอร์ส `r = edge_ai.result()` แล้วถามว่าค่า `r['seq']` กับ `r['latency_ms']` มาจากไหน
คำตอบคือมันวิ่งข้ามสองคอร์: Python บน CM33_NS ถามผ่าน IPC ไปหา `ai_engine` บน CM55 แล้วได้ฟิลด์ใน struct `ai_result_t` กลับมา

## แนวคิด

PSoC Edge E84 มีสามคอร์ **CM33_S** ดูแล boot และความปลอดภัย ไม่มีงาน Edge AI **CM33_NS** รัน FreeRTOS กับ MicroPython ของเรา อ่านเซนเซอร์และมีโมดูล
`edge_ai`, `sensors`, `dsp`, `ui` ส่วน **CM55** คอร์เร็ว รัน LVGL, Ethos-U55 NPU และ **`ai_engine`** ที่มี task วนอนุมานทีละโมเดลจากทะเบียน
แต่ละแถวของทะเบียนคือ `ai_model_desc_t` (name, sensor, class_labels ที่ index 0 เป็นคลาสปฏิเสธ, period_ms และตัวชี้สี่ฟังก์ชัน) ทุกโมเดลอยู่ในหน่วยความจำตลอด
การสลับคือเปลี่ยนว่าใครได้ข้อมูลจาก feed ไม่ใช่ปิดเปิดโมเดล และ feed ของแต่ละเซนเซอร์คือ front-end ฝั่ง C ที่แปลงค่าดิบก่อนเข้ากราฟ

CM33_NS เรียกฟังก์ชันบน CM55 ตรง ๆ ไม่ได้ ทั้งสองคุยผ่าน **IPC model link** ที่มีสอง plane: **control** (`MODEL_LINK_OP_CTRL`) สั่งแบบยิงแล้วไม่รอ
เช่น SELECT(n) = `0x90 + n` และ **query** (`MODEL_LINK_OP_QUERY`) อ่านแบบ pull เช่น `Q_COUNT`, `Q_MODEL`, `Q_RESULT`, `Q_ACTIVE` ตามที่นิยามไว้ใน
`ipc_model_link_defs.h` `ai_engine` เก็บสอง index คือ `s_active` (ที่ขอ อ่านด้วย `ai_engine_requested()`) กับ `s_current` (ที่ init เสร็จแล้วจริง อ่านด้วย
`ai_engine_active()`) `edge_ai.active()` คืนตัวหลัง `edge_ai.select(n)` จึงส่งคำสั่งแล้ว poll `Q_ACTIVE` จนเห็น n (ยืนยันด้วยการสังเกต)
ถ้าไม่เห็นในเวลาจะโยน `OSError` และการสั่ง select รัว ๆ เสี่ยงให้ pipe ค้าง

เมื่อ `dequeue()` ได้คำตอบ `publish()` เขียนลง `ai_result_t` โดยไม่ล็อก (ผู้เขียนเดียว ผู้อ่านยอมรับค่าที่เก่าไปหนึ่งเฟรม) เพื่อไม่หน่วง interrupt ของ NPU
ฟิลด์คือ `model_index`, `class_count`, `top_class`, `running`, `scores[]`, `inference_us`, `inference_us_max`, `inferences` และ `seq` dict ของ `result()`
จึงได้ `top` จาก `top_class`, `latency_ms` จาก `inference_us / 1000` และ `seq` เพิ่มทุกครั้งที่ publish runtime จริงคือ **TFLite-Micro** ที่มี kernel ทั้ง int8 และ float32
โมเดล int8 ที่ผ่าน Vela ไปรันบน Ethos-U55 ส่วนโมเดล float32 รันบน CPU ในภาพเดียวกัน โค้ดที่ DEEPCRAFT สร้างเป็นเพียงเปลือกที่ให้ `init`, `enqueue`, `dequeue`, `finalize`

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. โค้ด MicroPython ของเรากับ Ethos-U55 NPU อยู่คนละคอร์อย่างไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) ทั้งคู่อยู่บน CM55
   - ข) MicroPython อยู่บน CM33_NS ส่วน ai_engine กับ NPU อยู่บน CM55 และคุยกันผ่าน IPC
   - ค) MicroPython อยู่บน CM33_S
   - ง) NPU อยู่บน CM33_NS

   <details><summary>เฉลย</summary>

   **ข** — งานหนักอย่าง NPU โมเดล และจออยู่คอร์เร็ว ส่วน REPL กับเซนเซอร์อยู่คอร์ควบคุม CM33_S ดูแล boot กับความปลอดภัย

   </details>

2. edge_ai.active() คืนค่าใด *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) s_active คือโมเดลที่เพิ่งขอ
   - ข) s_current คือโมเดลที่ init เสร็จและสลับไปแล้วจริง
   - ค) จำนวนโมเดลทั้งหมด
   - ง) ค่า seq ล่าสุด

   <details><summary>เฉลย</summary>

   **ข** — active() ไปทาง Q_ACTIVE ซึ่งคืน ai_engine_active() ส่วนโมเดลที่เพิ่งขอคือ Q_REQUESTED หรือ ai_engine_requested()

   </details>

3. select(n) โยน OSError "select not confirmed" หมายความว่าอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) ชื่อโมเดลผิด
   - ข) ส่งคำสั่งแล้วแต่ poll Q_ACTIVE ไม่เห็นโมเดล n ภายในเวลาที่กำหนด
   - ค) บอร์ดไม่มี NPU
   - ง) IPC ถูกปิดถาวร

   <details><summary>เฉลย</summary>

   **ข** — select ไม่เชื่อว่าสั่งแล้วสำเร็จ มันรอเห็นผลจริง ถ้าไม่เห็นก็รายงานเป็น error ให้เราจัดการด้วย try/except

   </details>

4. r['latency_ms'] มาจากฟิลด์ใดของ ai_result_t *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) seq
   - ข) inference_us หารด้วย 1000
   - ค) inferences
   - ง) top_class

   <details><summary>เฉลย</summary>

   **ข** — engine จับเวลาแต่ละการอนุมานเป็นไมโครวินาที MicroPython แปลงเป็นมิลลิวินาที ส่วน seq เพิ่มทุกครั้งที่ publish

   </details>

5. ในภาพเฟิร์มแวร์เดียวกัน โมเดล float32 รันที่ใด *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) บน Ethos-U55 เหมือน int8
   - ข) บน CPU ด้วย float kernel ของ TFLite-Micro
   - ค) รันไม่ได้
   - ง) บน CM33_S

   <details><summary>เฉลย</summary>

   **ข** — TFLite-Micro พก kernel ทั้งสองชนิด NPU รับเฉพาะ int8 ที่ผ่าน Vela โมเดล float32 จึงใช้ CPU และช้ากว่า

   </details>

## แล็บ

- [ ] วาดภาพสามคอร์ในบันทึกการเรียน แล้วเขียนว่าโค้ดของคุณ `ai_engine` NPU และจออยู่คอร์ไหน
- [ ] เปิด `ai_engine.h` หาฟิลด์ทุกตัวของ `ai_result_t` แล้วเขียนว่าแต่ละ key ของ `result()` มาจากฟิลด์ใด
- [ ] เปิด `ipc_model_link_defs.h` หาค่าของ `MODEL_LINK_CMD_SELECT_BASE` และ `MODEL_LINK_Q_ACTIVE` แล้วอธิบายว่า select ยืนยันตัวเองอย่างไร

## ไปต่อ

บทเรียน 7.2 เราจะเติมคำสั่งฝั่งอ่านห้าตัวใน `s18_under_the_hood.py` แล้วไล่ log สามชั้นของสแตกจากปลาย MicroPython

บทเรียนถัดไป: [บทเรียน 7.2 — ลงมือทำ: ส่องสแตกจาก MicroPython](../l02-trace-the-stack-lab/README.md)

## สะท้อนคิด

- ทำไมการออกแบบให้ select ยืนยันด้วยการสังเกตจึงปลอดภัยกว่าการส่งคำสั่งแล้วรอ ack แบบ push
- ถ้าคุณต้องให้แอปรู้ทันทีว่าผลเก่าไปแล้ว คุณจะใช้ฟิลด์ใดของ ai_result_t
