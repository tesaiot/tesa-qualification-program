---
id: edgeai-dev.m01.l07
lang: th
title: {th: 'ลงมือทำ: จาก verdict สู่ action บนบอร์ด', en: 'Hands-on: from verdict to action on the board'}
summary: {th: เติมสี่ช่องในไฟล์ s03_anatomy_edgeai.py จนแอปเฝ้าโมเดลเดียวบี๊บและขึ้นแบนเนอร์เองเมื่อเจอคลาสเป้าหมายที่มั่นใจพอ แล้ว remix ให้สลับโมเดล เปลี่ยนคลาสเป้าหมาย และเปลี่ยน action โดยไม่แตะ logic ตรวจจับ, en: 'Fill the four blanks in s03_anatomy_edgeai.py until the single-model watcher beeps and shows a banner on its own when a confident target class appears, then remix the model, the target class and the action without touching the detection logic.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m01.l06]
objectives:
  - {th: 'เติม practice/s03_anatomy_edgeai.py ครบสี่ช่อง (select, result, verdict.text, fire_action) จนทำท่าหรือส่งเสียงตรงคลาสเป้าหมายแล้วได้ยินบี๊บหนึ่งครั้งและเห็นแบนเนอร์ และเมื่อออกจากคลาสนั้นแบนเนอร์กลับเป็น "รอจับ ..."', en: 'Fill the four blanks of practice/s03_anatomy_edgeai.py (select, result, verdict.text, fire_action) so that performing the target class gives one beep and a banner, and leaving it turns the banner back to "waiting".'}
  - {th: remix แอปด้วยการเปลี่ยน MODEL_KEYWORD และ TARGET_CLASS เป็นโมเดลอื่นที่ใช้เซนเซอร์ต่างกัน โดยตั้งคลาสเป้าหมายจาก labels ที่อ่านได้จริง แล้วยืนยันว่า action ยิงตามคลาสใหม่, en: 'Remix the app by changing MODEL_KEYWORD and TARGET_CLASS to another model with a different sensor, setting the target from the labels actually reported, and confirm the action fires on the new class.'}
  - {th: หากรณีที่คลาสเป้าหมายชนะแต่ conf ต่ำกว่า CONF_FLOOR แล้วอธิบายได้ว่าทำไม action จึงไม่ยิง และธง fired ป้องกันอะไร, en: 'Find a case where the target class wins but conf is below CONF_FLOOR, and explain why the action does not fire and what the fired flag prevents.'}
develops: [{skill: ai.edge, to: 2}, {skill: lang.micropython, to: 2}, {skill: prog.state-machines, to: 2}]
assesses: [{skill: ai.edge, level: 2, evidence: practice/s03_anatomy_edgeai.py}, {skill: prog.state-machines, level: 2, evidence: practice/s03_anatomy_edgeai.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 1.7 — ลงมือทำ: จาก verdict สู่ action บนบอร์ด

> โมดูล 1 — เริ่มต้น: รันของจริงแล้วแกะดูข้างใน · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เติมสี่ช่องในไฟล์ s03_anatomy_edgeai.py จนแอปเฝ้าโมเดลเดียวบี๊บและขึ้นแบนเนอร์เองเมื่อเจอคลาสเป้าหมายที่มั่นใจพอ แล้ว remix ให้สลับโมเดล เปลี่ยนคลาสเป้าหมาย และเปลี่ยน action โดยไม่แตะ logic ตรวจจับ

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เติม practice/s03_anatomy_edgeai.py ครบสี่ช่อง (select, result, verdict.text, fire_action) จนทำท่าหรือส่งเสียงตรงคลาสเป้าหมายแล้วได้ยินบี๊บหนึ่งครั้งและเห็นแบนเนอร์ และเมื่อออกจากคลาสนั้นแบนเนอร์กลับเป็น "รอจับ ..."
2. remix แอปด้วยการเปลี่ยน MODEL_KEYWORD และ TARGET_CLASS เป็นโมเดลอื่นที่ใช้เซนเซอร์ต่างกัน โดยตั้งคลาสเป้าหมายจาก labels ที่อ่านได้จริง แล้วยืนยันว่า action ยิงตามคลาสใหม่
3. หากรณีที่คลาสเป้าหมายชนะแต่ conf ต่ำกว่า CONF_FLOOR แล้วอธิบายได้ว่าทำไม action จึงไม่ยิง และธง fired ป้องกันอะไร

## ก่อนเริ่ม

ผ่านบทเรียน 1.6 มาแล้ว เข้าใจเงื่อนไข hit (label ตรงเป้าหมายและ conf ≥ CONF_FLOOR) กับธง fired
ถ้าจำสี่คำสั่งจากบทเรียน 1.3 ไม่แม่น เปิดเฉลย `s01_first_inference.py` ทวนก่อน เพราะช่อง 1–3 เป็นของเดิม

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — ฉบับเต็มใช้ on_result ซึ่งบน Emulator จะเรียก callback ก็ต่อเมื่อโปรแกรมเรียก edge_ai.result() หรือ edge_ai.active() จึงควรลองฉบับเต็มบนบอร์ด
- **เรียนมาก่อน:** [บทเรียน 1.6 — แกะแอป Edge AI: ทะเบียนโมเดล verdict และ action](../l06-edge-ai-app-anatomy/README.md)

## แนวคิด

ทั้งไฟล์อ่านเป็นประโยคเดียว: หาโมเดลจากชื่อ → สั่งรัน → วนอ่านผลขึ้นจอทุกราว 180 ms → พอเจอคลาสเป้าหมายที่มั่นใจพอก็สั่งการ → หยุดตอนออก
ช่อง 1–3 ทวนของเดิมจากบทเรียน 1.3 (`select(model['index'])` ภายใน `try`, `r = edge_ai.result()`, `verdict.text(...)`)
ช่อง 4 คือของใหม่ `fire_action(r['conf'])` ที่อยู่ในเงื่อนไข `if hit and not fired:` ครึ่งซ้ายของวงจร (เซนเซอร์ → โมเดล) เกิดบน CM55
อัตโนมัติ ครึ่งขวา (result → จอ → action) คือโค้ด Python ของเราบน CM33 ทั้งหมด

จุด remix มีสองชั้น ชั้นแรกอยู่บนหัวไฟล์สองบรรทัด: `MODEL_KEYWORD` สลับทั้งโมเดลและเซนเซอร์ (IMU → MIC → RADAR) ส่วน
`TARGET_CLASS` ต้องสะกดตรงกับชื่อใน `labels` ของโมเดลนั้นเป๊ะ (ดูได้จากบรรทัดในคอนโซลหรือ `edge_ai.models()`) เช่น
`"Cough"` คู่กับ `"cough"` ชั้นที่สองคือ `fire_action()` ที่แก้ได้ที่เดียว เปลี่ยนโน้ตของ `ui.tone`, ใช้ `ui.sfx(ui.SFX_UI_SELECT)`,
บี๊บสองระดับตามความมั่นใจ หรือนับจำนวนครั้ง โดยไม่กระทบสิ่งที่แอปตรวจจับ

ตอนจบ บล็อก `finally` หยุดเครื่องยนต์เสมอ ถ้าใช้ `on_result` (อย่างในฉบับเต็ม) ต้องถอน callback ด้วย `edge_ai.on_result(None)` ก่อน `stop()`
ความสำเร็จของบทเรียนไม่ใช่แค่เห็นแบนเนอร์ แต่ต้องบอกได้ว่าแอปนี้ต่างจากบทเรียน 1.3 ตรงไหน และ remix ของคุณเปลี่ยนอะไร

## ตัวอย่างสมบูรณ์

`s03_anatomy_edgeai_full.py` ยกไปใช้ `on_result` แยกสีด้วย `CONF_FLOOR` นับจำนวน action และโชว์ latency
ลองอ่านหลังไฟล์ฝึกทำงานแล้ว สังเกตว่าลูปหลักเหลือแค่รับปุ่ม เพราะงานอ่านผลย้ายไปอยู่ใน callback

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/s03_anatomy_edgeai_full.py](examples/s03_anatomy_edgeai_full.py) | เฝ้าจับคลาสด้วย on_result แล้วสั่งการ (ฉบับเต็ม) |

## ฝึกเติม

เติมตามลำดับ 1) `edge_ai.select(model['index'])` หลัง `find_model` 2) `r = edge_ai.result()` 3) `verdict.text(r['label'] or '-')`
4) `fire_action(r['conf'])` ในเงื่อนไข hit ตั้ง `MODEL_KEYWORD`/`TARGET_CLASS` ที่อยากลองก่อน (เริ่มที่ Motion กับ shaking ก็ได้)
ถ้าจอค้างที่ `---` แปลว่าช่อง 1 ยังว่าง ถ้าคลาสขึ้นถูกแต่ไม่มีเสียงและแบนเนอร์ แปลว่าช่อง 4 ยังว่าง

| ไฟล์ฝึก | เรื่อง |
|---|---|
| [practice/s03_anatomy_edgeai.py](practice/s03_anatomy_edgeai.py) | แกะแอป Edge AI แล้ว remix: สลับโมเดล + สั่งการเมื่อเจอคลาส (ฉบับฝึกเติมโค้ด) |

## เฉลย

เปิดเฉลยหลังจากลองเองแล้วอย่างน้อยหนึ่งรอบ และอ่าน [วิธีใช้เฉลย](../../README.md#วิธีใช้เฉลย) ก่อน

| เฉลย | คู่กับ |
|---|---|
| [solution/s03_anatomy_edgeai.py](solution/s03_anatomy_edgeai.py) | [practice/s03_anatomy_edgeai.py](practice/s03_anatomy_edgeai.py) |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. เติมไฟล์ครบแล้ว หน้าจอขึ้นคลาส shaking ถูกต้อง แต่ไม่มีเสียงบี๊บและไม่มีแบนเนอร์เลย ช่องใดยังว่าง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) ช่อง 1 edge_ai.select(model['index'])
   - ข) ช่อง 2 r = edge_ai.result()
   - ค) ช่อง 4 fire_action(r['conf'])
   - ง) ไม่มีช่องไหนว่าง เป็นเพราะ Emulator ไม่มีลำโพง

   <details><summary>เฉลย</summary>

   **ค** — คลาสขึ้นจอแปลว่าช่อง 1–3 ทำงานแล้ว ช่อง 4 คือจุดที่ verdict กลายเป็น action ถ้าว่าง แอปจะ "รายงาน" แต่ไม่ "ลงมือ"

   </details>

2. อยากเปลี่ยนแอปเป็นตัวจับเสียงไอ ต้องตั้งสองบรรทัดบนหัวไฟล์อย่างไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) MODEL_KEYWORD = "Cough", TARGET_CLASS = "cough"
   - ข) MODEL_KEYWORD = "cough", TARGET_CLASS = "Cough Detection"
   - ค) MODEL_KEYWORD = "Motion", TARGET_CLASS = "cough"
   - ง) MODEL_KEYWORD = 3, TARGET_CLASS = 1

   <details><summary>เฉลย</summary>

   **ก** — find_model ค้นคำในชื่อโดยไม่สนตัวพิมพ์ แต่ TARGET_CLASS ต้องตรงกับ labels ของโมเดลเป๊ะ ซึ่งของ Cough Detection คือ unlabelled กับ cough

   </details>

3. ผลคือ {'label': 'shaking', 'conf': 0.42} และ TARGET_CLASS = 'shaking' action จะเป็นอย่างไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) ยิงทันทีเพราะคลาสตรง
   - ข) ไม่ยิง เพราะ hit ต้องการ conf ≥ CONF_FLOOR (0.50) ด้วย และ fired ถูกรีเซ็ตเป็น False
   - ค) ยิงสองครั้ง
   - ง) โปรแกรมโยน OSError

   <details><summary>เฉลย</summary>

   **ข** — hit เป็น False เพราะ conf ยังไม่ถึงเกณฑ์ โค้ดจึงเข้า elif not hit ซึ่งรีเซ็ต fired และขึ้นแบนเนอร์ "รอจับ" นี่คือตัวกัน false positive

   </details>

4. เรียงเหตุการณ์เมื่อผู้ใช้เขย่าบอร์ดสองรอบ (เขย่า หยุด เขย่า) โดยเป้าหมายคือ shaking *(เรียงลำดับ · เป้าหมายข้อ 3)*
   - ก) hit เป็น False จึงรีเซ็ต fired = False
   - ข) hit เป็น True และ fired เป็น False จึงยิง action แล้วตั้ง fired = True
   - ค) hit เป็น True อีกครั้ง fired เป็น False จึงยิง action รอบที่สอง
   - ง) hit ยังเป็น True แต่ fired เป็น True จึงไม่ยิงซ้ำ

   <details><summary>เฉลย</summary>

   **ข → ง → ก → ค** — edge-trigger ยิงตอนเพิ่งเข้าคลาส ไม่ยิงซ้ำระหว่างที่ยังเขย่าค้าง รีเซ็ตเมื่อออกจากคลาส แล้วพร้อมยิงใหม่เมื่อเข้าคลาสอีกครั้ง

   </details>

## แล็บ

**MVP ของชุดบทเรียน 1.6–1.7:** remix `s03_anatomy_edgeai.py` ได้จริง คือสลับโมเดล (เปลี่ยน `MODEL_KEYWORD` และ `TARGET_CLASS`) และสั่งการเมื่อเจอคำตัดสินที่เข้าเงื่อนไข

- [ ] เติมไฟล์ฝึกครบสี่ช่อง ทำท่าหรือเสียงจนได้ยินบี๊บหนึ่งครั้งและเห็นแบนเนอร์
- [ ] remix เป็นโมเดลอื่นอย่างน้อยหนึ่งตัว (เช่น Motion → Cough) แล้วยืนยันว่า action ยิงตามคลาสใหม่
- [ ] หาท่าหรือเสียงที่คลาสเป้าหมายชนะแต่ conf ต่ำกว่า CONF_FLOOR แล้วจดลงบันทึกการเรียนว่าทำไม action ไม่ยิง
- [ ] อธิบายได้ว่าทำไมต้องเช็กทั้ง label และ conf และทำไมต้องมีธง fired

## ไปต่อ

โมดูลถัดไปเราเปิดเสาที่ 1 (DAQ) เริ่มเก็บข้อมูลเซนเซอร์ของเราเองลงไฟล์ CSV เพื่อเป็นวัตถุดิบฝึกโมเดลในโมดูล 5

บทเรียนถัดไป: [บทเรียน 2.1 — สุ่มสัญญาณให้ตรงกับโมเดล: อัตราสุ่ม Nyquist หน้าต่าง และ schema ของ CSV](../../m02-daq/l01-sampling-and-schema/README.md)

## สะท้อนคิด

- action ที่คุณเลือกใน remix ควรยิงครั้งเดียวต่อการเจอ หรือควรยิงซ้ำเป็นระยะ ถ้ายิงซ้ำ คุณจะออกแบบธงหรือตัวจับเวลาอย่างไร
- ถ้าต้องเอาแอปนี้ไปใช้กับโมเดลที่คลาสเป้าหมายไม่ได้อยู่ลำดับเดียวกัน โค้ดของคุณต้องแก้ตรงไหนบ้าง
