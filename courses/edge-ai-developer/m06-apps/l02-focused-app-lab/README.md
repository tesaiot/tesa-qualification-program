---
id: edgeai-dev.m06.l02
lang: th
title: {th: 'ลงมือทำ: แอปโฟกัสของเราเอง', en: 'Hands-on: your own focused app'}
summary: {th: เติมสี่จุดใน s15_apps.py ให้เป็นแอปโฟกัสที่นับเสียงไอ ได้แก่ select โมเดลเป้าหมายก่อนลูป อ่าน result โชว์คลาสที่ชนะ และเงื่อนไขตรวจเจอที่ผ่าน CONF_FLOOR แล้วรีทาร์เก็ตเป็น Alarm หรือ Siren ด้วยการแก้แค่สองบรรทัดบนหัวไฟล์ จนได้ตระกูลแอปต่อโมเดลของเราเอง, en: 'Fill four points in s15_apps.py to make a focused cough-counting app - select the target model before the loop, read the result, show the winning class, and a detection condition gated by CONF_FLOOR - then retarget it to Alarm or Siren by editing just two lines at the top, giving you your own family of per-model apps.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m06.l01]
objectives:
  - {th: เติมสี่จุดใน practice/s15_apps.py จนแอปขึ้นคลาสที่ชนะ แถบทุกคลาส latency และตัวนับที่เพิ่มหนึ่งครั้งต่อเหตุการณ์เป้าหมายหนึ่งครั้ง, en: 'Fill the four points in practice/s15_apps.py until the app shows the winning class, a bar per class, the latency, and a counter that rises once per target event.'}
  - {th: รีทาร์เก็ตแอปเป็นโมเดลอื่นอย่างน้อยหนึ่งตัวโดยแก้แค่ TARGET_KEYWORDS กับ TARGET_CLASS และตรวจชื่อคลาสจาก edge_ai.models() ก่อน (เช่น Siren ใช้คลาส sirens), en: 'Retarget the app to at least one other model by editing only TARGET_KEYWORDS and TARGET_CLASS, checking the class name in edge_ai.models() first (Siren''s class is sirens).'}
  - {th: ทดลองตัดเงื่อนไข conf ≥ CONF_FLOOR ออกชั่วคราว แล้วอธิบายจากผลที่เห็นว่าทำไมตัวนับจึงเก็บ false positive, en: Temporarily remove the conf ≥ CONF_FLOOR condition and use what you see to explain why the counter then collects false positives.}
develops: [{skill: ai.edge, to: 3}, {skill: lang.micropython, to: 2}, {skill: gui.hmi, to: 2}]
assesses: [{skill: ai.edge, level: 2, evidence: practice/s15_apps.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 6.2 — ลงมือทำ: แอปโฟกัสของเราเอง

> โมดูล 6 — แอป Edge AI · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เติมสี่จุดใน s15_apps.py ให้เป็นแอปโฟกัสที่นับเสียงไอ ได้แก่ select โมเดลเป้าหมายก่อนลูป อ่าน result โชว์คลาสที่ชนะ และเงื่อนไขตรวจเจอที่ผ่าน CONF_FLOOR แล้วรีทาร์เก็ตเป็น Alarm หรือ Siren ด้วยการแก้แค่สองบรรทัดบนหัวไฟล์ จนได้ตระกูลแอปต่อโมเดลของเราเอง

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เติมสี่จุดใน practice/s15_apps.py จนแอปขึ้นคลาสที่ชนะ แถบทุกคลาส latency และตัวนับที่เพิ่มหนึ่งครั้งต่อเหตุการณ์เป้าหมายหนึ่งครั้ง
2. รีทาร์เก็ตแอปเป็นโมเดลอื่นอย่างน้อยหนึ่งตัวโดยแก้แค่ TARGET_KEYWORDS กับ TARGET_CLASS และตรวจชื่อคลาสจาก edge_ai.models() ก่อน (เช่น Siren ใช้คลาส sirens)
3. ทดลองตัดเงื่อนไข conf ≥ CONF_FLOOR ออกชั่วคราว แล้วอธิบายจากผลที่เห็นว่าทำไมตัวนับจึงเก็บ false positive

## ก่อนเริ่ม

ผ่านบทเรียน 6.1 มาแล้ว เข้าใจ find_model, CONF_FLOOR และการนับขอบขาขึ้น
เตรียมคลิปเสียงไอ เสียงเตือน หรือไซเรนไว้เปิดใกล้บอร์ด

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — บน Emulator โมเดลเสียงเป็นค่าจำลองที่คลาสเหตุการณ์ยังไม่ชนะ unlabelled ตัวนับจึงไม่ขยับ ทดสอบตรรกะการนับบน Emulator ได้ด้วยโมเดล Motion กับปุ่ม Shake ส่วนการนับเสียงไอจริงต้องใช้บอร์ด
- **เรียนมาก่อน:** [บทเรียน 6.1 — หกโมเดลกับ edge_ai API: แอปที่โฟกัสโมเดลเดียว](../l01-focused-apps/README.md)

## แนวคิด

ทั้งไฟล์อ่านเป็นประโยคเดียว: เล็งโมเดล cough → สร้างการ์ด → เริ่มรัน → วนอ่านผล เอาคลาสขึ้นจอ นับเมื่อเจอ → ออกก็หยุด
แผงตั้งค่าบนหัวไฟล์คือ `TARGET_KEYWORDS = ("cough",)`, `TARGET_CLASS = "cough"` และ `TARGET_SENSOR = edge_ai.SENSOR_MIC` แยกชื่อโมเดลกับชื่อคลาสออกจากกัน
เพราะไม่เหมือนกันเสมอ สี่จุดที่เติมคือ (1) `edge_ai.select(model['index'])` ก่อนลูปใน `try` เพราะ `select()` โยน `OSError` ได้ถ้าการสลับไม่ได้รับการยืนยัน
(2) `r = edge_ai.result()` (3) `verdict.text(r['label'] or '-')` เมื่อ `seq` เปลี่ยน และ
(4) `is_target = r['label'] == TARGET_CLASS and r['conf'] >= edge_ai.CONF_FLOOR` ซึ่งเป็นของใหม่จริงของบทเรียนนี้

ตัวนับเพิ่มเมื่อ `is_target and not was_target` คือหนึ่งต่อการไอหนึ่งครั้ง ถ้าเห็นเลขพรวดหลายทีต่อเสียงเดียว แปลว่าเงื่อนไขขอบขาขึ้นหายไป
ถ้าผลค้างนิ่งและ `seq` ไม่ขยับ นั่นคือเพดานของ Ready-Model แบบประเมินผล ไม่ใช่โค้ดพัง รีทาร์เก็ตใช้เวลาไม่ถึงนาที: `("alarm",)` กับ `"alarm"`
หรือ `("siren",)` กับ `"sirens"` (มี s) แล้วเซฟเป็นไฟล์ใหม่ โครงทั้งไฟล์ไม่ต้องแตะ เพราะ `find_model()` หาโมเดลให้ และแถบปรับตาม `labels` ที่ได้มา
ความสำเร็จคือบอกได้ว่า action ของคุณเชื่อ verdict เมื่อไร และกันนับเฟ้ออย่างไร

## ตัวอย่างสมบูรณ์

`s15_apps_full.py` เพิ่มสีตาม `CONF_FLOOR` debounce เบา ๆ (นับเมื่อเจอติดกันสองผล) ป้ายเวลาที่เจอครั้งล่าสุด และปุ่ม Reset ล้างตัวนับ

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/s15_apps_full.py](examples/s15_apps_full.py) | แอป Edge AI แบบ "โฟกัสโมเดลเดียว" (ฉบับเต็ม) |

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นหรือใน `shared/` ด้วย:

- [m06-apps/l01-focused-apps/examples/16_edge_ai_sound_events.py](../l01-focused-apps/examples/16_edge_ai_sound_events.py) — Edge AI: Sound Events (Cough / Alarm / Siren) — 3 โมเดลไมค์ ใน dropdown เดียว

## ฝึกเติม

คอมเมนต์ `# เติม:` อยู่ที่บรรทัด 87 (`select`), 96 (`result`), 101 (`verdict.text`) และ 112 (`is_target`)
ถ้าการ์ดขึ้นครบแต่ไม่มีผลเลย ตรวจจุดที่ 87 ก่อน ถ้าแถบขยับแต่ตัวใหญ่ไม่เปลี่ยน ตรวจจุดที่ 101

| ไฟล์ฝึก | เรื่อง |
|---|---|
| [practice/s15_apps.py](practice/s15_apps.py) | แอป Edge AI แบบ "โฟกัสโมเดลเดียว" (ฉบับฝึกเติมโค้ด) |

## เฉลย

เปิดเฉลยหลังจากลองเองแล้วอย่างน้อยหนึ่งรอบ และอ่าน [วิธีใช้เฉลย](../../README.md#วิธีใช้เฉลย) ก่อน

| เฉลย | คู่กับ |
|---|---|
| [solution/s15_apps.py](solution/s15_apps.py) | [practice/s15_apps.py](practice/s15_apps.py) |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. แอปขึ้นการ์ดครบแต่ไม่มีผลใด ๆ เลยและตัวนับไม่ขยับ จุดใดยังว่างมากที่สุด *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) จุดที่ 1 edge_ai.select(model['index'])
   - ข) จุดที่ 3 verdict.text(...)
   - ค) จุดที่ 4 is_target
   - ง) ไม่มีจุดใดผิด

   <details><summary>เฉลย</summary>

   **ก** — ถ้าไม่ select โมเดลเป้าหมาย ก็ไม่มีโมเดลรัน จึงไม่มีผลให้ result() คืน

   </details>

2. ไอหนึ่งครั้งแต่ตัวนับเพิ่มสามถึงสี่ครั้ง ส่วนใดของเงื่อนไขหายไป *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) r["conf"] >= edge_ai.CONF_FLOOR
   - ข) not was_target (การนับเฉพาะขอบขาขึ้น)
   - ค) r["label"] == TARGET_CLASS
   - ง) edge_ai.stop()

   <details><summary>เฉลย</summary>

   **ข** — ไอหนึ่งครั้งกินหลายผลอนุมาน ถ้าไม่จำสถานะรอบก่อน ทุกผลที่เข้าเป้าจะถูกนับหมด

   </details>

3. รีทาร์เก็ตเป็นไซเรนด้วย TARGET_KEYWORDS = ("siren",) และ TARGET_CLASS = "siren" แล้วตัวนับไม่เคยขยับ เพราะอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) โมเดล Siren ไม่มีบนบอร์ด
   - ข) ชื่อคลาสจริงคือ sirens (มี s) เงื่อนไข label == TARGET_CLASS จึงไม่เคยจริง
   - ค) CONF_FLOOR สูงเกินไป
   - ง) find_model หาไม่เจอ

   <details><summary>เฉลย</summary>

   **ข** — ชื่อโมเดลกับชื่อคลาสไม่เหมือนกันเสมอ ให้ตรวจ labels จาก edge_ai.models() ใน REPL ก่อนรีทาร์เก็ต

   </details>

4. ตัดเงื่อนไข conf ออกแล้ว ตัวนับเพิ่มแม้ไม่มีใครไอ เพราะอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) ไมค์เสีย
   - ข) argmax ให้ผู้ชนะเสมอ แม้ cough ชนะแบบเฉียด 0.51 ต่อ 0.49 ก็ถูกนับ กลายเป็น false positive
   - ค) seq ไม่เปลี่ยน
   - ง) โมเดลเปลี่ยนเป็น Motion

   <details><summary>เฉลย</summary>

   **ข** — CONF_FLOOR คือประตูที่บอกว่าเชื่อผลก็ต่อเมื่อมั่นใจถึงเกณฑ์ ถ้าไม่มีประตู ทุกครั้งที่ชนะเฉียดก็กลายเป็นการกระทำ

   </details>

## แล็บ

**MVP ของชุดบทเรียน 6.1–6.2:** แอปโฟกัสต่อโมเดลที่ UI สะอาด เล็งโมเดลด้วย `find_model()` โชว์ verdict แถบทุกคลาสและ latency และมีตัวนับที่ทำงานจริงเมื่อคลาสเป้าหมายข้าม `CONF_FLOOR` รีทาร์เก็ตได้อย่างน้อยสองโมเดล

- [ ] เติมไฟล์ฝึกครบสี่จุด ซ้อมบน Emulator แล้วนับเสียงไอจริงบนบอร์ด
- [ ] รีทาร์เก็ตเป็น Alarm หรือ Siren เซฟเป็นไฟล์ใหม่ แล้วยืนยันว่าตัวนับทำงาน
- [ ] ตัด `and r['conf'] >= edge_ai.CONF_FLOOR` ออกชั่วคราว ส่งเสียงอื่น ๆ แล้วจดลงบันทึกการเรียนว่าตัวนับต่างจากเดิมอย่างไร แล้วใส่กลับ
- [ ] อธิบายได้ว่าทำไมต้องเช็ก `CONF_FLOOR` ก่อนนับ และทำไมต้องนับเฉพาะขอบขาขึ้น

## ไปต่อ

ชุดบทเรียนถัดไป (บทเรียน 6.3–6.4) เราจะเปลี่ยนการนับเป็น action ที่แรงขึ้น เช่นไฟ RGB เสียง และ log พร้อม debounce และ cooldown เต็มรูปแบบ

บทเรียนถัดไป: [บทเรียน 6.3 — ท่อสั่งการ: CONF_FLOOR, debounce, cooldown และ on_result](../l03-action-pipeline/README.md)

## สะท้อนคิด

- ถ้าแอปนับเสียงไอนับเกินจริงในห้องที่มีคนคุยกัน คุณจะปรับอะไรก่อน ระหว่าง CONF_FLOOR กับ debounce
- การแยก TARGET_KEYWORDS ออกจาก TARGET_CLASS ช่วยคนที่ต้องดูแลโค้ดต่อจากคุณอย่างไร
