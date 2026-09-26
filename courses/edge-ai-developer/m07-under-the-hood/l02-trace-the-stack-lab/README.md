---
id: edgeai-dev.m07.l02
lang: th
title: {th: 'ลงมือทำ: ส่องสแตกจาก MicroPython', en: 'Hands-on: tracing the stack from MicroPython'}
summary: {th: 'เติมคำสั่งฝั่งอ่านห้าตัวของ edge_ai ใน s18_under_the_hood.py คือ links, model, active, result และ latency แล้วกด Trace ให้ log ไล่สแตกสามชั้น transport, control และ result พร้อมจับคู่แต่ละบรรทัดกับฟังก์ชันหรือฟิลด์ใน header ของ SDK และเทียบ latency ของโมเดล int8 บน NPU กับโมเดล float32 บน CPU', en: 'Fill the five read-side calls of edge_ai in s18_under_the_hood.py (links, model, active, result and latency), press Trace to log the three stack layers (transport, control, result), match each line to a function or field in the SDK headers, and compare the latency of an int8 model on the NPU with a float32 model on the CPU.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m07.l01]
objectives:
  - {th: 'เติมห้าจุดใน practice/s18_under_the_hood.py จนกด Trace แล้วได้ log ครบสี่ส่วน transport, registry, control และ result โดยค่า active() ตรงกับโมเดลที่เลือก', en: 'Fill the five points in practice/s18_under_the_hood.py until Trace logs all four parts (transport, registry, control, result) with active() matching the selected model.'}
  - {th: จับคู่ log อย่างน้อยสามบรรทัดกับฟังก์ชันหรือฟิลด์ใน ai_engine.h หรือ ipc_model_link_defs.h ของ SDK, en: Match at least three log lines to a function or field in the SDK's ai_engine.h or ipc_model_link_defs.h.}
  - {th: บนบอร์ด เทียบ latency() ของโมเดล int8 กับโมเดล float32 และอธิบายความต่างด้วยเส้นทาง NPU กับ CPU, en: 'On the board, compare latency() of an int8 model with a float32 model and explain the difference by the NPU and CPU paths.'}
develops: [{skill: rtos.multicore-ipc, to: 2}, {skill: hw.architecture, to: 3}, {skill: lang.micropython, to: 2}]
assesses: [{skill: rtos.multicore-ipc, level: 2, evidence: practice/s18_under_the_hood.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 7.2 — ลงมือทำ: ส่องสแตกจาก MicroPython

> โมดูล 7 — ใต้ฝากระโปรงและการต่อเติม · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เติมคำสั่งฝั่งอ่านห้าตัวของ edge_ai ใน s18_under_the_hood.py คือ links, model, active, result และ latency แล้วกด Trace ให้ log ไล่สแตกสามชั้น transport, control และ result พร้อมจับคู่แต่ละบรรทัดกับฟังก์ชันหรือฟิลด์ใน header ของ SDK และเทียบ latency ของโมเดล int8 บน NPU กับโมเดล float32 บน CPU

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เติมห้าจุดใน practice/s18_under_the_hood.py จนกด Trace แล้วได้ log ครบสี่ส่วน transport, registry, control และ result โดยค่า active() ตรงกับโมเดลที่เลือก
2. จับคู่ log อย่างน้อยสามบรรทัดกับฟังก์ชันหรือฟิลด์ใน ai_engine.h หรือ ipc_model_link_defs.h ของ SDK
3. บนบอร์ด เทียบ latency() ของโมเดล int8 กับโมเดล float32 และอธิบายความต่างด้วยเส้นทาง NPU กับ CPU

## ก่อนเริ่ม

ผ่านบทเรียน 7.1 มาแล้ว รู้จักสามคอร์ ทะเบียนโมเดล IPC สอง plane และ ai_result_t
เปิด `ai_engine.h` กับ `ipc_model_link_defs.h` ของ SDK ไว้คู่จอเหมือนบทเรียนก่อน

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — บน Emulator ซ้อมเรียก API ฝั่งอ่านได้ (ได้ ('ipc',) และทะเบียนห้าโมเดล) แต่ latency กับผลโมเดลเป็นค่าจำลอง การเทียบ int8 กับ float32 ต้องทำบนบอร์ด
- **เรียนมาก่อน:** [บทเรียน 7.1 — สแตก Edge AI: tri-core, ai_engine, IPC model link และ TFLite-Micro](../l01-edge-ai-stack/README.md)

## แนวคิด

ไฟล์นี้ไม่ได้อนุมานอะไรใหม่ มันเป็น **เครื่องมือส่องสแตก** ที่เรียก API ฝั่งอ่านแล้ว log ทีละชั้น ห้าจุดที่เติมคือ (1) `links = edge_ai.links()`
คืน `('ipc',)` บอกว่าคุยกับ CM55 ผ่าน IPC model link (2) `desc = edge_ai.model(mi)` ดึง descriptor ตัวเดียว (name, sensor, labels) ผ่าน `Q_MODEL`
(3) `cur = edge_ai.active()` หลัง `select(sel)` ที่ให้ไว้แล้ว ถ้าปกติ `cur` ต้องเท่ากับ `sel` นี่คือการยืนยันด้วยการสังเกตที่เห็นกับตา
(4) `r = edge_ai.result()` ผ่าน `Q_RESULT` และ (5) `ms = edge_ai.latency()` คือเวลาอนุมานล่าสุดจาก `inference_us` ทั้งห้าเป็นการอ่านแบบ pull ทั้งหมด

เมื่อ Trace ทำงาน log จะไล่จาก transport → registry → control → result ให้จับคู่แต่ละบรรทัดกับ header ของ SDK เช่น `active()` กับ `ai_engine_active()`
และ `MODEL_LINK_Q_ACTIVE`, `select(n)` กับ `MODEL_LINK_CMD_SELECT_BASE + n`, key ของ `result()` กับฟิลด์ของ `ai_result_t` ซอร์ส C ฝั่งเฟิร์มแวร์ที่ log เอ่ยถึง
(`ai_engine.c`, `deepcraft_task.c`) ยังไม่เปิดเผย header จึงเป็นหลักฐานสาธารณะที่ตรวจได้ บนบอร์ด ลอง Trace โมเดล int8 (เช่น Motion) แล้วสลับไปโมเดล float32
(ผู้เขียนระบุว่า Push และ Siren) เทียบ `latency()` จะเห็นว่าเส้นทาง NPU กับ CPU ต่างกันจริง อย่าสลับโมเดลรัว ๆ เว้นเป็นวินาทีเพื่อไม่ให้ control plane ค้าง

## ตัวอย่างสมบูรณ์

`s18_under_the_hood_full.py` เพิ่มแผนที่สแตกบนจอ ตารางจับคู่ key ของ `result()` กับฟิลด์ใน `ai_result_t` callback `on_result`
(เรียกเมื่อคลาสเปลี่ยนและทวนราววินาทีละครั้ง) และการเทียบ latency ระหว่าง int8 กับ float32

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/s18_under_the_hood_full.py](examples/s18_under_the_hood_full.py) | เครื่องส่องสแตก Edge AI ฉบับเต็ม (สำหรับ Researcher) |

## ฝึกเติม

คอมเมนต์ `# เติม` อยู่ที่บรรทัด 38 (`links`), 75 (`model`), 109 (`active`), 134 (`result`) และ 142 (`latency`)
ถ้า log ชั้น transport ว่าง จุดที่ 38 ยังว่าง ถ้า active() ขึ้น −1 ตลอดทั้งที่เลือกโมเดลแล้ว ตรวจจุดที่ 109

| ไฟล์ฝึก | เรื่อง |
|---|---|
| [practice/s18_under_the_hood.py](practice/s18_under_the_hood.py) | แกะสแตก Edge AI จากปลาย MicroPython ลงไปถึง NPU (ฉบับฝึกเติมโค้ด) |

## เฉลย

เปิดเฉลยหลังจากลองเองแล้วอย่างน้อยหนึ่งรอบ และอ่าน [วิธีใช้เฉลย](../../README.md#วิธีใช้เฉลย) ก่อน

| เฉลย | คู่กับ |
|---|---|
| [solution/s18_under_the_hood.py](solution/s18_under_the_hood.py) | [practice/s18_under_the_hood.py](practice/s18_under_the_hood.py) |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. บน Emulator และบนบอร์ด edge_ai.links() ควรคืนอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) ('ipc',)
   - ข) ('wifi',)
   - ค) None
   - ง) จำนวนโมเดล

   <details><summary>เฉลย</summary>

   **ก** — MicroPython คุยกับ ai_engine ผ่าน IPC model link ทางเดียว Emulator คืนค่าเดียวกันเพื่อให้โค้ดย้ายไปบอร์ดได้ แม้ในเบราว์เซอร์จะไม่มี IPC จริง

   </details>

2. หลัง select(sel) สำเร็จ ค่า cur = edge_ai.active() ควรเป็นอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) −1
   - ข) sel เพราะ select รอจนเห็น Q_ACTIVE เท่ากับค่าที่ขอแล้ว
   - ค) sel + 1
   - ง) จำนวนโมเดล

   <details><summary>เฉลย</summary>

   **ข** — select คืนก็ต่อเมื่อยืนยันด้วยการสังเกตแล้ว ถ้าไม่ยืนยันมันโยน OSError แทน

   </details>

3. log "select(n)" ควรจับคู่กับสิ่งใดใน ipc_model_link_defs.h *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) MODEL_LINK_Q_RESULT
   - ข) MODEL_LINK_CMD_SELECT_BASE (0x90) บวก n บน control plane
   - ค) MODEL_LINK_STREAM_MIC_PCM
   - ง) BENTO_MODEL_LINK_VERSION

   <details><summary>เฉลย</summary>

   **ข** — SELECT ใส่เลขโมเดลไว้ในไบต์คำสั่งบน OP_CTRL แล้วยืนยันด้วย Q_ACTIVE บน query plane

   </details>

4. บนบอร์ด latency ของ Motion (int8) ต่ำกว่า Push (float32) มาก เพราะอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) Motion มีคลาสน้อยกว่า
   - ข) โมเดล int8 ที่ผ่าน Vela รันบน Ethos-U55 ส่วน float32 รันบน CPU ด้วย float kernel
   - ค) เรดาร์ช้ากว่า IMU เสมอ
   - ง) เพราะ IPC ของเรดาร์ช้ากว่า

   <details><summary>เฉลย</summary>

   **ข** — latency วัดเฉพาะช่วงอนุมาน ความต่างหลักจึงมาจากว่ากราฟรันบน NPU หรือบน CPU

   </details>

## แล็บ

**MVP ของชุดบทเรียน 7.1–7.2:** อธิบายสแตกได้ แล้วชี้ฟังก์ชันหรือฟิลด์ต้นทางของสามชั้น (transport, control, result) ได้อย่างน้อยชั้นละหนึ่งจุด

- [ ] เติมไฟล์ฝึกครบห้าจุด กด Trace บน Emulator หรือบอร์ดจน log ขึ้นครบ
- [ ] จับคู่ log อย่างน้อยสามบรรทัดกับฟังก์ชันหรือฟิลด์ใน `ai_engine.h` หรือ `ipc_model_link_defs.h` แล้วจดลงบันทึกการเรียน
- [ ] บนบอร์ด Trace โมเดล int8 หนึ่งตัวกับ float32 หนึ่งตัว จด `latency()` ทั้งสองและอธิบายความต่าง
- [ ] อธิบายด้วยคำพูดของคุณว่าทำไม `active()` อาจยังไม่ใช่โมเดลที่เพิ่งขอถ้าอ่านจากที่อื่นระหว่างสลับ

## ไปต่อ

ชุดบทเรียนถัดไป (บทเรียน 7.3–7.4) เราจะใช้แผนที่นี้เพิ่มโมเดลของเราเองให้โผล่ใน `edge_ai.models()`

บทเรียนถัดไป: [บทเรียน 7.3 — เพิ่มโมเดลของเราเอง: สามการแก้ สัญญาสี่ฟังก์ชัน และ Vela](../l03-add-your-own-model/README.md)

## สะท้อนคิด

- log บรรทัดไหนที่คุณยังชี้ต้นทางไม่ได้ และข้อมูลใดที่ขาดไปจากส่วนที่เปิดเผย
- ถ้าบอร์ดค้างหลังสลับโมเดลรัว ๆ คุณจะเล่าอาการนี้ให้ทีมเฟิร์มแวร์ฟังอย่างไรให้เขาหาต้นเหตุได้
