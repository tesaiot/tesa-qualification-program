---
id: edgeai-dev.m06.l01
lang: th
title: {th: 'หกโมเดลกับ edge_ai API: แอปที่โฟกัสโมเดลเดียว', en: 'Six models and the edge_ai API: an app focused on one model'}
summary: {th: เปิดโมดูลแอป จากเมนูที่ให้เลือกทุกโมเดลไปสู่แอปที่โฟกัสโมเดลเดียว เล็งโมเดลด้วย find_model() แทนเลข index อ่าน scores ทุกคลาสกับ latency_ms ให้เป็น และต่อ verdict เข้ากับ action แรกคือการนับเมื่อคลาสเป้าหมายมั่นใจถึง CONF_FLOOR เฉพาะจังหวะขอบขาขึ้น, en: 'Open the apps module - from a menu that offers every model to an app focused on one. Target the model with find_model() instead of an index, read every class score and latency_ms, and wire the verdict to a first action - counting when the target class reaches CONF_FLOOR, on the rising edge only.'}
level: L3
time_min: {concept: 45, practise: 15, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m05.l09]
objectives:
  - {th: เปรียบเทียบแอปเมนูกับแอปโฟกัสโมเดลเดียว และบอกได้ว่างานแบบใดควรใช้แบบใด, en: 'Compare a menu app with a single-model focused app, and say which kind of job suits each.'}
  - {th: อธิบาย find_model() ที่ถอยสามชั้น (ชื่อ → เซนเซอร์ → ตัวแรก) และเหตุผลที่ไม่ควร hard-code เลข index ของโมเดล, en: Explain find_model() with its three fallbacks (name → sensor → first) and why a model index should never be hard-coded.}
  - {th: 'อ่าน dict ของ edge_ai.result() ได้ครบ ทั้ง top ที่มาจาก argmax, conf ที่เป็นคะแนนสูงสุด, scores ทุกคลาส, latency_ms และ seq ที่ใช้วาดจอเฉพาะผลใหม่', en: 'Read an edge_ai.result() dict fully - top from argmax, conf as the highest score, every class score, latency_ms, and seq for redrawing only on new results.'}
  - {th: เขียนเงื่อนไขนับ label == TARGET_CLASS และ conf ≥ CONF_FLOOR (0.50) ที่นับเฉพาะขอบขาขึ้น และอธิบายขีดจำกัดของโมเดล Ready-Model แบบประเมินผล, en: 'Write the counting condition label == TARGET_CLASS and conf ≥ CONF_FLOOR (0.50) that counts on the rising edge only, and explain the limits of the evaluation Ready Models.'}
develops: [{skill: ai.edge, to: 3}, {skill: lang.micropython, to: 2}, {skill: gui.hmi, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 6.1 — หกโมเดลกับ edge_ai API: แอปที่โฟกัสโมเดลเดียว

> โมดูล 6 — แอป Edge AI · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เปิดโมดูลแอป จากเมนูที่ให้เลือกทุกโมเดลไปสู่แอปที่โฟกัสโมเดลเดียว เล็งโมเดลด้วย find_model() แทนเลข index อ่าน scores ทุกคลาสกับ latency_ms ให้เป็น และต่อ verdict เข้ากับ action แรกคือการนับเมื่อคลาสเป้าหมายมั่นใจถึง CONF_FLOOR เฉพาะจังหวะขอบขาขึ้น

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เปรียบเทียบแอปเมนูกับแอปโฟกัสโมเดลเดียว และบอกได้ว่างานแบบใดควรใช้แบบใด
2. อธิบาย find_model() ที่ถอยสามชั้น (ชื่อ → เซนเซอร์ → ตัวแรก) และเหตุผลที่ไม่ควร hard-code เลข index ของโมเดล
3. อ่าน dict ของ edge_ai.result() ได้ครบ ทั้ง top ที่มาจาก argmax, conf ที่เป็นคะแนนสูงสุด, scores ทุกคลาส, latency_ms และ seq ที่ใช้วาดจอเฉพาะผลใหม่
4. เขียนเงื่อนไขนับ label == TARGET_CLASS และ conf ≥ CONF_FLOOR (0.50) ที่นับเฉพาะขอบขาขึ้น และอธิบายขีดจำกัดของโมเดล Ready-Model แบบประเมินผล

## ก่อนเริ่ม

ผ่านโมดูล 1 มาแล้ว เคยใช้ `edge_ai.models()`, `select()`, `result()` และ `stop()` และจำโครง verdict สู่ action จากบทเรียน 1.6 ได้
เปิดตัวอย่าง `16_edge_ai_sound_events.py` ไว้ใน BENTO IDE

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — บน Emulator คะแนนของโมเดลเป็นค่าจำลอง โมเดลเสียงขยับตามลูกบิด POTEN แต่คลาสเหตุการณ์ยังไม่ชนะ unlabelled และไม่มีโมเดล Push เสียงจริงกับเรดาร์ต้องใช้บอร์ด
- **เรียนมาก่อน:** [บทเรียน 5.9 — ลงมือทำ: เทียบสามเป้าหมาย MCU, Web และ PC](../../m05-training/l09-three-targets-lab/README.md)

## ดูของจริงก่อน

รัน `16_edge_ai_sound_events.py` บนบอร์ดแล้วสลับ Cough, Alarm และ Siren ใน dropdown เดียว ดูแถบสองคลาสขยับเมื่อมีเสียง
ถามตัวเองว่า ถ้าเครื่องนี้ต้องนับเสียงไอในห้องผู้ป่วยทั้งคืน ผู้ใช้ควรต้องเลือกโมเดลเองหรือไม่

## แนวคิด

เมนูเลือกโมเดลเหมาะกับการสำรวจและเดโม แต่สินค้าจริงแทบทั้งหมดเป็น **แอปโฟกัส**: เล็งโมเดลเดียวตอนเปิดแอป UI ออกแบบเฉพาะงาน และต่อ verdict เข้ากับ action
ตัวอย่าง 13 ถึง 16 มีก้อนเดียวกัน คือ `find_model()` → `select()` → ลูป `result()` → วาด verdict กับแถบ → `finally: stop()` บนบอร์ดมีหกโมเดล
(Motion, Baby Cry, Push, Cough, Alarm, Siren) ส่วน Emulator มีห้า ลำดับจึงไม่เท่ากัน `find_model()` หาจากคีย์เวิร์ดในชื่อก่อน ไม่เจอค่อยใช้โมเดลแรกที่ตรง
`sensor` (เช่น `edge_ai.SENSOR_MIC = 2`) และสุดท้ายใช้ตัวแรกกันแอปล่ม `select(3)` ตายตัวจะพังทันทีที่ทะเบียนเปลี่ยน

dict ของ `result()` ให้มากกว่าคลาสที่ชนะ: `top` คือ $\hat{y} = \arg\max_i s_i$ `conf` คือ $s_{\hat{y}}$ `scores` ใช้วาดแถบทุกคลาสให้เห็นว่าโมเดลลังเลหรือชัวร์
`latency_ms` บอกเวลาอนุมานบน NPU ซึ่งต่างกันตามโมเดล และ `seq` ใช้วาดจอเฉพาะเมื่อมีผลใหม่ argmax เลือกผู้ชนะเสมอแม้ 0.51 ต่อ 0.49
เราจึงตั้งประตูของ action: นับเมื่อ `r['label'] == TARGET_CLASS and r['conf'] >= edge_ai.CONF_FLOOR` (0.50) และนับเฉพาะ **ขอบขาขึ้น** (`is_target and not was_target`)
เพราะไอหนึ่งครั้งกินหลายผลอนุมาน ตั้งเกณฑ์สูงได้ความชัวร์แต่พลาดเสียงเบา ตั้งต่ำจับไวแต่ false positive มาก

Cough, Alarm และ Siren เป็น DEEPCRAFT Ready-Model ของ Imagimob AB (บริษัทในเครือ Infineon) แบบประเมินผล ใช้ได้เพื่อการทดลองเท่านั้น
และจำกัดจำนวนครั้งอนุมาน ถ้าผลค้างนิ่งและ `seq` ไม่ขยับ นั่นคือเพดานของโมเดล ไม่ใช่โค้ดพัง ผู้เขียนแนะนำให้รีบูตบอร์ด
เมื่อฝึกโมเดลเองได้แบบโมดูล 5 ข้อจำกัดนี้ก็หายไป

## ตัวอย่างสมบูรณ์

`14_edge_ai_babycry.py` การ์ดผลลัพธ์กับแถบความมั่นใจของโมเดลไมค์ `15_edge_ai_radar_push.py` โมเดลเรดาร์ Push (ยืนห่างราว 60 ซม. ต้องใช้บอร์ดที่มีเรดาร์)
`16_edge_ai_sound_events.py` เมนูย่อยสามโมเดลเสียง `17_latency_min_max_avg.py` เก็บ latency 20 รอบแล้วสรุปต่ำสุด สูงสุด เฉลี่ย
และ `18_switch_cost.py` จับเวลาการสลับโมเดลด้วย `select()` ให้เห็นว่าการสลับถี่ ๆ มีราคา (สองไฟล์หลังย้ายมาจากคอร์ส AIoT ของผู้เขียน)

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/14_edge_ai_babycry.py](examples/14_edge_ai_babycry.py) | Edge AI: Baby Cry (ไมโครโฟน) — ตรวจเสียงเด็กร้องบนบอร์ด (ไม่ต้องต่อเน็ต) |
| [examples/15_edge_ai_radar_push.py](examples/15_edge_ai_radar_push.py) | Edge AI: Radar Push (เรดาร์ 60 GHz) — จำแนกท่าทางมือด้วยเรดาร์บนบอร์ด |
| [examples/16_edge_ai_sound_events.py](examples/16_edge_ai_sound_events.py) | Edge AI: Sound Events (Cough / Alarm / Siren) — 3 โมเดลไมค์ ใน dropdown เดียว |
| [examples/17_latency_min_max_avg.py](examples/17_latency_min_max_avg.py) | วัดว่าโมเดลใช้เวลาคิดนานแค่ไหน |
| [examples/18_switch_cost.py](examples/18_switch_cost.py) | สลับโมเดลระหว่างที่โปรแกรมกำลังรัน |

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นหรือใน `shared/` ด้วย:

- [m01-onboarding/l06-edge-ai-app-anatomy/examples/13_edge_ai_motion.py](../../m01-onboarding/l06-edge-ai-app-anatomy/examples/13_edge_ai_motion.py) — Edge AI: Motion (IMU) ด้วย API ใหม่ edge_ai — เห็นคะแนนทุกคลาส + latency
- [m06-apps/l02-focused-app-lab/practice/s15_apps.py](../l02-focused-app-lab/practice/s15_apps.py) — แอป Edge AI แบบ "โฟกัสโมเดลเดียว" (ฉบับฝึกเติมโค้ด)

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. เครื่องนับเสียงไอข้างเตียงผู้ป่วยควรเป็นแอปแบบใด *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) เมนูที่ให้ผู้ใช้เลือกโมเดลเองทุกครั้ง
   - ข) แอปโฟกัสที่เล็งโมเดล Cough ตั้งแต่เปิด และต่อ verdict กับการนับ
   - ค) แอปที่สลับทุกโมเดลทุกวินาที
   - ง) ไม่ต้องมีแอป ใช้ REPL

   <details><summary>เฉลย</summary>

   **ข** — ผู้ใช้ปลายทางไม่ควรต้องรู้ว่ามีโมเดลอะไร เมนูเหมาะกับการสำรวจและเดโม แอปโฟกัสเหมาะกับงานจริง

   </details>

2. ทำไม find_model(("cough",), edge_ai.SENSOR_MIC) จึงดีกว่า edge_ai.select(3) *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) เร็วกว่า
   - ข) หาโมเดลจากชื่อ จึงยังถูกตัวแม้ลำดับทะเบียนเปลี่ยน เช่น Emulator ที่ไม่มี Push ทำให้ Cough อยู่ index 2
   - ค) ใช้หน่วยความจำน้อยกว่า
   - ง) select(3) ใช้ไม่ได้บนบอร์ด

   <details><summary>เฉลย</summary>

   **ข** — บนบอร์ด Cough อยู่ index 3 แต่บน Emulator อยู่ index 2 การถามทะเบียนด้วยชื่อทำให้โค้ดชุดเดียวใช้ได้ทั้งสองที่

   </details>

3. r['scores'] = [0.12, 0.88] ของโมเดล ['unlabelled', 'cough'] ค่า r['top'] และ r['conf'] คืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) top = 0, conf = 0.12
   - ข) top = 1, conf = 0.88
   - ค) top = 0.88, conf = 1
   - ง) top = 1, conf = 0.12

   <details><summary>เฉลย</summary>

   **ข** — top คือ index ของคะแนนสูงสุด (argmax) conf คือค่าคะแนนนั้นเอง คลาสที่ชนะจึงเป็น cough ด้วยความมั่นใจ 0.88

   </details>

4. ไอหนึ่งครั้งยาวสามผลอนุมาน ได้ conf ของ cough เป็น 0.8, 0.9, 0.85 แล้วตกลง ตัวนับแบบขอบขาขึ้นเพิ่มกี่ครั้ง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) 0
   - ข) 1
   - ค) 3
   - ง) 2

   <details><summary>เฉลย</summary>

   **ข** — นับเฉพาะตอนเปลี่ยนจากไม่เข้าเป้าเป็นเข้าเป้า ตราบใดที่ยังค้างเหนือเกณฑ์จะไม่นับซ้ำ ไอหนึ่งครั้งจึงได้ 1

   </details>

5. แอป Cough ทำงานดีมาสักพัก แล้วผลค้างนิ่งและ seq ไม่ขยับ สาเหตุที่น่าจะเป็นที่สุดคืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) โค้ดมี memory leak
   - ข) โมเดล Ready-Model แบบประเมินผลถึงเพดานจำนวนครั้งอนุมาน
   - ค) CONF_FLOOR ตั้งผิด
   - ง) ไมค์เสีย

   <details><summary>เฉลย</summary>

   **ข** — โมเดลประเมินผลจำกัดจำนวนครั้งอนุมาน นี่คือลักษณะของใบอนุญาต ไม่ใช่บั๊กในโค้ด โมเดลที่ฝึกเองไม่มีข้อจำกัดนี้

   </details>

## แล็บ

- [ ] รัน `17_latency_min_max_avg.py` กับ `TARGET = "motion"` แล้วเปลี่ยนเป็น `"cough"` จดต่ำสุด สูงสุด และเฉลี่ยของทั้งสองลงบันทึกการเรียน
- [ ] เขียน `find_model()` ด้วยมือในบันทึกการเรียน แล้วอธิบายว่าบน Emulator ที่ไม่มี Push ทำไม `select(3)` จึงได้โมเดลคนละตัวกับบนบอร์ด
- [ ] วาดกราฟ conf ของคลาส cough ตามเวลาแบบคร่าว ๆ แล้วทำเครื่องหมายจุดที่ต้องนับตามกฎขอบขาขึ้น

## ไปต่อ

บทเรียน 6.2 เราจะเติม `s15_apps.py` ให้เป็นแอปนับเสียงไอ แล้วรีทาร์เก็ตเป็น Alarm หรือ Siren ด้วยการแก้แค่สองบรรทัดบนหัวไฟล์

บทเรียนถัดไป: [บทเรียน 6.2 — ลงมือทำ: แอปโฟกัสของเราเอง](../l02-focused-app-lab/README.md)

## สะท้อนคิด

- อุปกรณ์รอบตัวคุณชิ้นไหนเป็นแอปโฟกัสโมเดลเดียว และมันทำ action อะไรกับ verdict
- ถ้าต้องเลือก CONF_FLOOR ให้เครื่องเตือนไซเรนในรถ คุณจะตั้งสูงหรือต่ำ เพราะอะไร
