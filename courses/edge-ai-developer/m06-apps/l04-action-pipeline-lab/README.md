---
id: edgeai-dev.m06.l04
lang: th
title: {th: 'ลงมือทำ: action pipeline ที่กัน false positive', en: 'Hands-on: an action pipeline that resists false positives'}
summary: {th: เติมสี่ด่านของท่อใน s16_action_pipeline.py คือ อ่านผล กรอง debounce+cooldown และยิง action จนไฟบนจอไล่ฟ้า เหลือง แดง พร้อมเสียงและ log เมื่อคลาสเป้าหมายค้างนานพอ แล้วจูน NEED_HITS กับ COOLDOWN_MS และพิสูจน์ว่าท่อปฏิเสธสัญญาณปลอมได้จริง, en: 'Fill the four pipeline stages in s16_action_pipeline.py (read, filter, debounce plus cooldown, fire) until the on-screen light goes cyan, amber, red with a sound and a log line when the target class lasts long enough, then tune NEED_HITS and COOLDOWN_MS and prove the pipeline really rejects fake signals.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m06.l03]
objectives:
  - {th: เติมสี่จุดใน practice/s16_action_pipeline.py จนการเจอคลาสเป้าหมายต่อเนื่องครบ NEED_HITS ยิงไฟแดง เสียง และ log หนึ่งบรรทัด ส่วนสัญญาณเฟรมเดียวไม่ยิง, en: 'Fill the four points in practice/s16_action_pipeline.py so that the target class held for NEED_HITS frames fires the red light, a sound and one log line, while a one-frame signal does not.'}
  - {th: 'จูน NEED_HITS อย่างน้อยสามค่า (เช่น 1, 3, 6) บันทึกจำนวน false positive และ false negative ของแต่ละค่า แล้วเลือกค่าให้งานที่กำหนดพร้อมเหตุผล', en: 'Tune NEED_HITS to at least three values (for example 1, 3, 6), record the false positives and false negatives of each, and pick a value for a given job with reasons.'}
  - {th: ชี้ได้ว่าสัญญาณปลอมที่คุณสร้างถูกด่านใดกันไว้ และอธิบายว่าถ้าลืม last_fire = now จะเกิดอะไร, en: 'Point to the stage that blocked the fake signal you made, and explain what happens if last_fire = now is forgotten.'}
develops: [{skill: ai.edge, to: 3}, {skill: prog.state-machines, to: 2}, {skill: lang.micropython, to: 2}]
assesses: [{skill: ai.edge, level: 3, evidence: practice/s16_action_pipeline.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 6.4 — ลงมือทำ: action pipeline ที่กัน false positive

> โมดูล 6 — แอป Edge AI · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เติมสี่ด่านของท่อใน s16_action_pipeline.py คือ อ่านผล กรอง debounce+cooldown และยิง action จนไฟบนจอไล่ฟ้า เหลือง แดง พร้อมเสียงและ log เมื่อคลาสเป้าหมายค้างนานพอ แล้วจูน NEED_HITS กับ COOLDOWN_MS และพิสูจน์ว่าท่อปฏิเสธสัญญาณปลอมได้จริง

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เติมสี่จุดใน practice/s16_action_pipeline.py จนการเจอคลาสเป้าหมายต่อเนื่องครบ NEED_HITS ยิงไฟแดง เสียง และ log หนึ่งบรรทัด ส่วนสัญญาณเฟรมเดียวไม่ยิง
2. จูน NEED_HITS อย่างน้อยสามค่า (เช่น 1, 3, 6) บันทึกจำนวน false positive และ false negative ของแต่ละค่า แล้วเลือกค่าให้งานที่กำหนดพร้อมเหตุผล
3. ชี้ได้ว่าสัญญาณปลอมที่คุณสร้างถูกด่านใดกันไว้ และอธิบายว่าถ้าลืม last_fire = now จะเกิดอะไร

## ก่อนเริ่ม

ผ่านบทเรียน 6.3 มาแล้ว เข้าใจท่อสี่ด่าน EMA และการยิงตอนขอบขึ้น
เตรียมบันทึกการเรียนไว้จดตารางจูน NEED_HITS

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — บน Emulator ตั้ง MODEL_KEYWORD = "Motion" กับ TARGET_CLASS = "shaking" แล้วกดปุ่ม Shake ค้างเพื่อซ้อมท่อ ส่วนเสียงไอจริงต้องใช้บอร์ด
- **เรียนมาก่อน:** [บทเรียน 6.3 — ท่อสั่งการ: CONF_FLOOR, debounce, cooldown และ on_result](../l03-action-pipeline/README.md)

## แนวคิด

ทั้งไฟล์อ่านเป็นประโยคเดียว: เลือกโมเดล → วนอ่านผล → เฟรมนี้เจอเป้าหมายไหม → ครบ debounce และ cooldown ไหม → ยิง action
ไฟล์ฝึกเตรียม widget การ์ดไฟ `fire_action()` และ `set_light()` ไว้แล้ว เหลือสี่จุดตามการไหล: (1) `r = edge_ai.result()` ถ้าว่าง จอไม่ขึ้นคลาสและท่อไม่เดิน
(2) `hit = (r['label'] == TARGET_CLASS and r['conf'] >= edge_ai.CONF_FLOOR)` ถ้าว่าง streak ไม่ขยับ (3) `should_fire = ready and cooled`
โดย `ready = streak >= NEED_HITS` และ `cooled` มาจาก `ticks_diff` ที่เตรียมไว้ และ (4) `fire_action(r['conf']); last_fire = now; streak = 0`
คือสั่งการ ตั้งนาฬิกาเว้นช่วงใหม่ และล้างตัวนับ ลืม `last_fire = now` แล้ว cooldown ไม่เริ่มใหม่ ท่อจะยิงรัวเมื่อเหตุการณ์ค้าง

หัวใจเชิงวิศวกรรมคือการจูน ไม่มีค่าที่ถูกตายตัว `NEED_HITS` สูงเตือนผิดน้อยแต่พลาดเหตุการณ์สั้น `CONF_FLOOR` สูงเชื่อเฉพาะที่มั่นใจมาก
`COOLDOWN_MS` ยาวไม่รบกวนซ้ำแต่เหตุการณ์จริงสองครั้งติดกันจะเห็นครั้งเดียว วัดผลด้วยการนับ false positive (ยิงทั้งที่ไม่มีเหตุ)
เทียบกับ false negative (มีเหตุแต่ไม่ยิง) แล้วถามว่างานนี้พลาดแบบไหนแพงกว่า ความสำเร็จไม่ใช่แค่ไฟติด แต่ต้องแสดงว่าท่อ **ปฏิเสธ** สัญญาณปลอมได้

## ตัวอย่างสมบูรณ์

`s16_action_pipeline_full.py` เพิ่ม `dsp.EMA` smoothing ที่ `EMA_ALPHA = 0.35` ไฟสี่สถานะ `on_result` ที่ log เฉพาะตอนคลาสเปลี่ยน
และตัวนับ `blocked` ที่นับครั้งที่ cooldown กันการยิงซ้ำไว้ ลองไอหรือเขย่าค้างยาวแล้วดู `blocked` เพิ่ม

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/s16_action_pipeline_full.py](examples/s16_action_pipeline_full.py) | action pipeline ครบวง: กรอง + smooth + debounce + action (ฉบับเต็ม) |

## ฝึกเติม

คอมเมนต์ `# เติม:` อยู่ที่บรรทัด 120 (อ่านผล), 134 (กรอง), 152 (debounce + cooldown) และ 157 (ยิง action)
ถ้าไอแวบเดียวแล้วยิง แปลว่าด่าน 2 หรือ 3 ยังไม่ทำงาน ถ้าเขย่าค้างแล้วยิงรัว ตรวจ `last_fire = now` ในจุดที่ 157

| ไฟล์ฝึก | เรื่อง |
|---|---|
| [practice/s16_action_pipeline.py](practice/s16_action_pipeline.py) | จาก verdict สู่ action จริง: RGB + เสียง + log (ฉบับฝึกเติมโค้ด) |

## เฉลย

เปิดเฉลยหลังจากลองเองแล้วอย่างน้อยหนึ่งรอบ และอ่าน [วิธีใช้เฉลย](../../README.md#วิธีใช้เฉลย) ก่อน

| เฉลย | คู่กับ |
|---|---|
| [solution/s16_action_pipeline.py](solution/s16_action_pipeline.py) | [practice/s16_action_pipeline.py](practice/s16_action_pipeline.py) |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. ไฟค้างสีฟ้าตลอดแม้เขย่าค้างนาน streak ไม่ขยับเลย จุดใดยังว่าง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) จุดที่ 2 hit ยังเป็น False
   - ข) จุดที่ 4
   - ค) จุดที่ 3
   - ง) ไม่มีจุดใดผิด

   <details><summary>เฉลย</summary>

   **ก** — streak เพิ่มเมื่อ hit เป็นจริงเท่านั้น ถ้า hit ยังเป็นค่าเริ่มต้น False ท่อจะรีเซ็ตทุกเฟรม

   </details>

2. ไฟขึ้นเหลือง 1/3 และ 2/3 ตามการเขย่า แต่ไม่เคยแดง ไม่มีเสียงหรือ log จุดใดยังว่าง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) จุดที่ 1
   - ข) จุดที่ 2
   - ค) จุดที่ 3 หรือ 4 (should_fire ยังเป็น False หรือยังไม่เรียก fire_action)
   - ง) COOLDOWN_MS เป็นศูนย์

   <details><summary>เฉลย</summary>

   **ค** — streak ขยับแปลว่าด่าน 1 และ 2 ทำงาน ปลายท่อที่ไม่ยิงอยู่ที่เงื่อนไข should_fire หรือการเรียก fire_action

   </details>

3. NEED_HITS = 1 ผลการทดสอบน่าจะเป็นแบบใด *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) ไม่เคยยิง
   - ข) ไวที่สุดแต่ false positive มากที่สุด เพราะเฟรมเดียวที่ผ่านด่านกรองก็ยิง
   - ค) พลาดเหตุการณ์จริงบ่อยที่สุด
   - ง) เหมือน NEED_HITS = 6

   <details><summary>เฉลย</summary>

   **ข** — debounce ที่ 1 เฟรมเท่ากับไม่มี debounce ส่วนค่าสูงอย่าง 6 จะพลาดเหตุการณ์สั้นของจริงบ่อยขึ้น

   </details>

4. ลืม last_fire = now ในจุดที่ 4 แล้วเขย่าค้างยาว จะเกิดอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) ยิงครั้งเดียวตามปกติ
   - ข) cooldown ไม่เริ่มนับใหม่ ท่อยิงซ้ำทุกครั้งที่ streak ครบ
   - ค) ไม่ยิงเลย
   - ง) โปรแกรม error

   <details><summary>เฉลย</summary>

   **ข** — cooled ยังเป็นจริงตลอดเพราะ last_fire ไม่ขยับ ด่าน cooldown จึงไม่มีผล

   </details>

## แล็บ

**MVP ของชุดบทเรียน 6.3–6.4:** action pipeline แบบ debounce ที่คลาสเป้าหมายต่อเนื่องจุดชนวน action จริง ส่วนสัญญาณกระพริบสั้น ๆ ถูกกันไว้

- [ ] เติมไฟล์ฝึกครบสี่จุด ซ้อมบน Emulator ด้วย Motion กับปุ่ม Shake แล้วลองกับเสียงไอจริงบนบอร์ด
- [ ] จูน `NEED_HITS` = 1, 3, 6 ทำการทดสอบเดียวกันสิบครั้งต่อค่า แล้วจดตาราง false positive กับ false negative ลงบันทึกการเรียน
- [ ] สร้างสัญญาณที่ควรถูกกัน (กด Shake แวบเดียวหรือไอครั้งเดียว) ยืนยันว่าไม่ยิง และบอกว่าด่านใดกันไว้
- [ ] เลือกค่าให้สองงาน (เตือนไฟไหม้ กับ เตือนขโมย) พร้อมเหตุผล

## ไปต่อ

ชุดบทเรียนถัดไป (บทเรียน 6.5–6.6) เราจะรวม verdict กับเซนเซอร์ดิบ (sensor fusion) แล้วส่งเหตุการณ์ออกเน็ตด้วย WiFi และ MQTT

บทเรียนถัดไป: [บทเรียน 6.5 — sensor fusion: verdict ของโมเดลกับเซนเซอร์ดิบ](../l05-sensor-fusion/README.md)

## สะท้อนคิด

- ค่าที่คุณเลือกสำหรับเตือนขโมยกับเตือนไฟไหม้ต่างกันอย่างไร และคุณจะอธิบายให้ลูกค้าฟังอย่างไร
- ถ้า log ของคุณมีแต่ ALERT แต่ไม่มีบันทึกการกันยิง คุณจะรู้ได้อย่างไรว่าเกราะทำงานอยู่
