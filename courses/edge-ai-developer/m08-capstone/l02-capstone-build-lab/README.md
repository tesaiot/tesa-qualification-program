---
id: edgeai-dev.m08.l02
lang: th
title: {th: 'ลงมือทำ: สร้างและส่งมอบแอป Edge AI', en: 'Hands-on: build and ship an edge AI app'}
summary: {th: 'เติมห้าบรรทัดสันหลังของ s20_capstone.py คือ select, อ่านความเร่งดิบ, result, กรองความมั่นใจด้วย EMA และ fire_alert แล้วออกแบบ จูน และเดโม Guardian ของเราเอง พิสูจน์ด้วยหลักฐานว่าเหตุการณ์จริงทำให้เตือนครั้งเดียว ส่วนเคสหลอกไม่ทำให้เตือน และเล่าเหตุผลของค่าออกแบบที่เลือก', en: 'Fill the five backbone lines of s20_capstone.py (select, raw acceleration, result, EMA-filtered confidence and fire_alert), then design, tune and demo your own Guardian - proving with evidence that a real event alerts once while decoys do not, and explaining the design values you chose.'}
level: L3
time_min: {concept: 15, practise: 45, lab: 90, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m08.l01]
objectives:
  - {th: เติมห้าจุดใน practice/s20_capstone.py จน Guardian แสดงบริบท motion กับ verdict ที่กรองแล้ว และเตือน (เสียง แบนเนอร์ ตัวนับ) ครั้งเดียวเมื่อคลาสเป้าหมายต่อเนื่องครบ HITS_NEEDED ผล, en: 'Fill the five points in practice/s20_capstone.py until the Guardian shows the motion context and a filtered verdict, and alerts once (sound, banner, counter) when the target class lasts HITS_NEEDED results.'}
  - {th: 'ออกแบบ Guardian ของคุณ (โมเดล action และค่า CONF_FLOOR, HITS_NEEDED, EMA_ALPHA) และบันทึกเหตุผลพร้อมหลักฐานที่วัดได้ คือจำนวนการเตือนจากเหตุการณ์จริงกับจากเคสหลอกอย่างละอย่างน้อยห้าครั้ง', en: 'Design your Guardian (model, action, CONF_FLOOR, HITS_NEEDED, EMA_ALPHA) and record the reasons with measured evidence - the alerts from real events and from decoys, at least five trials each.'}
  - {th: เดโมสองนาทีที่แสดงการเตือนจริง เคสหลอกที่ไม่เตือน และการแลกเปลี่ยนที่เลือก พร้อมเสนอทิศต่อยอดหนึ่งทิศ, en: 'Give a two-minute demo showing a real alert, a decoy that does not alert and the trade-off you chose, and propose one extension direction.'}
develops: [{skill: ai.edge, to: 3}, {skill: biz.product-decision, to: 2}, {skill: soft.communication, to: 2}]
assesses: [{skill: ai.edge, level: 3, evidence: practice/s20_capstone.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 8.2 — ลงมือทำ: สร้างและส่งมอบแอป Edge AI

> โมดูล 8 — Capstone: แอป Edge AI ของเราเอง · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เติมห้าบรรทัดสันหลังของ s20_capstone.py คือ select, อ่านความเร่งดิบ, result, กรองความมั่นใจด้วย EMA และ fire_alert แล้วออกแบบ จูน และเดโม Guardian ของเราเอง พิสูจน์ด้วยหลักฐานว่าเหตุการณ์จริงทำให้เตือนครั้งเดียว ส่วนเคสหลอกไม่ทำให้เตือน และเล่าเหตุผลของค่าออกแบบที่เลือก

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เติมห้าจุดใน practice/s20_capstone.py จน Guardian แสดงบริบท motion กับ verdict ที่กรองแล้ว และเตือน (เสียง แบนเนอร์ ตัวนับ) ครั้งเดียวเมื่อคลาสเป้าหมายต่อเนื่องครบ HITS_NEEDED ผล
2. ออกแบบ Guardian ของคุณ (โมเดล action และค่า CONF_FLOOR, HITS_NEEDED, EMA_ALPHA) และบันทึกเหตุผลพร้อมหลักฐานที่วัดได้ คือจำนวนการเตือนจากเหตุการณ์จริงกับจากเคสหลอกอย่างละอย่างน้อยห้าครั้ง
3. เดโมสองนาทีที่แสดงการเตือนจริง เคสหลอกที่ไม่เตือน และการแลกเปลี่ยนที่เลือก พร้อมเสนอทิศต่อยอดหนึ่งทิศ

## ก่อนเริ่ม

ผ่านบทเรียน 8.1 มาแล้ว มีแบบร่าง Guardian ของคุณและค่าเริ่มต้นพร้อมเหตุผล
เตรียมเคสหลอกไว้ล่วงหน้า เช่นเขย่าแวบเดียวหรือเสียงก้ำกึ่ง เพื่อพิสูจน์ว่าชั้นตัดสินใจทำงาน

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — ทำ capstone ครบบน Emulator ได้ด้วยโมเดล Motion กับปุ่ม Shake ถ้าจะเฝ้าเสียงหรือเรดาร์ต้องใช้บอร์ด
- **เรียนมาก่อน:** [บทเรียน 8.1 — ออกแบบ capstone: Guardian สามเสาในไฟล์เดียว](../l01-capstone-design/README.md)

## แนวคิด

ทั้งไฟล์อ่านเป็นประโยคเดียว: เลือกโมเดล → อ่านบริบทและ verdict → กรองให้นิ่ง → เจอครบเกณฑ์ค่อยสั่งการ → ออกก็เก็บกวาด ปุ่มออกแบบอยู่บนหัวไฟล์
(`MODEL_KEYWORD`, `HITS_NEEDED = 3`, `EMA_ALPHA = 0.4`, `ACTION_NOTE = 72`) ห้าจุดที่เติมคือ (1) `edge_ai.select(model['index'])` เมื่อกด Load ใน `try`
แล้วขึ้น RUNNING หลัง select สำเร็จเท่านั้น (2) `ax, ay, az = sensors.bmi270.acceleration()` ลืมแล้ว motion ค้าง 0.0 (3) `r = edge_ai.result()` ลืมแล้วการ์ดไม่ขยับ
(4) `conf_s = conf_ema.update(r['conf'])` ลืมแล้วสีสถานะกระพริบตามพีค และ (5) `fire_alert(r['label'], conf_s)` เมื่อ `streak >= HITS_NEEDED and not fired`
ลืมแล้วครบเกณฑ์แต่ Guardian เงียบ

เติมครบยังไม่ใช่ capstone ขั้นที่ห้าที่เฉลยไม่ได้ให้คือการออกแบบของคุณ: เลือกโมเดลและ action ตั้งค่าออกแบบ แล้ววัดผลจริง ทำเหตุการณ์จริงกับเคสหลอกอย่างละหลายครั้ง
นับว่าเตือนกี่ครั้ง จากนั้นจูนและบันทึกว่าค่าเปลี่ยนผลอย่างไร เพื่อให้คำอธิบายการออกแบบยืนบนตัวเลข ไม่ใช่ความรู้สึก ส่งมอบด้วยเดโมสั้น ๆ ที่เห็นทั้งการเตือนจริงและการไม่เตือน
ทิศต่อยอดมีสี่ทาง: เสียบโมเดลที่ฝึกเองจากโมดูล 5, เพิ่ม feature จาก FFT ของโมดูล 4, fusion กับเซนเซอร์ดิบหรือเรดาร์ของบทเรียน 6.5 และส่งเหตุการณ์ขึ้น MQTT แบบบทเรียน 6.6

## ตัวอย่างสมบูรณ์

`s20_capstone_full.py` คือ Guardian ฉบับขัดเรียบร้อย เลือกโมเดลสดจาก dropdown แสดง latency ล้างตัวกรองเมื่อเริ่มเฝ้ารอบใหม่ และนับจำนวนการเตือน

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/s20_capstone_full.py](examples/s20_capstone_full.py) | Capstone: Edge AI Guardian (ฉบับเต็ม) |

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นหรือใน `shared/` ด้วย:

- [shared/training/eval_pc.py](../../shared/training/eval_pc.py) — Run the exported int8 .tflite on the PC and report accuracy + confusion.

## ฝึกเติม

คอมเมนต์ `# เติม:` อยู่ที่บรรทัด 127 (`select`), 152 (ความเร่งดิบ), 159 (`result`), 166 (`conf_ema.update`) และ 194 (`fire_alert`)
ถ้าขึ้น RUNNING แต่การ์ดไม่ขยับ ตรวจจุดที่ 127 และ 159 ถ้าสีสถานะกระพริบทุกเฟรม ตรวจจุดที่ 166

| ไฟล์ฝึก | เรื่อง |
|---|---|
| [practice/s20_capstone.py](practice/s20_capstone.py) | Capstone: Edge AI Guardian (ฉบับฝึกเติมโค้ด) |

## เฉลย

เปิดเฉลยหลังจากลองเองแล้วอย่างน้อยหนึ่งรอบ และอ่าน [วิธีใช้เฉลย](../../README.md#วิธีใช้เฉลย) ก่อน

| เฉลย | คู่กับ |
|---|---|
| [solution/s20_capstone.py](solution/s20_capstone.py) | [practice/s20_capstone.py](practice/s20_capstone.py) |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. Guardian ขึ้น RUNNING แต่การ์ดผลไม่ขยับเลยและ motion ขยับตามการเขย่า จุดใดยังว่าง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) จุดที่ 2 อ่านความเร่ง
   - ข) จุดที่ 3 r = edge_ai.result() (หรือจุดที่ 1 select)
   - ค) จุดที่ 4 EMA
   - ง) จุดที่ 5 fire_alert

   <details><summary>เฉลย</summary>

   **ข** — motion ขยับแปลว่าเสา DAQ ทำงาน การ์ดผลต้องการทั้งโมเดลที่ถูก select และการอ่าน result ในลูป

   </details>

2. เขย่าค้างครบเกณฑ์แล้วแบนเนอร์ขึ้นรอจับตลอด ไม่มีเสียงหรือตัวนับเพิ่ม จุดใดยังว่าง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) จุดที่ 5 fire_alert(r["label"], conf_s)
   - ข) จุดที่ 2
   - ค) จุดที่ 1
   - ง) ไม่มีจุดใดผิด

   <details><summary>เฉลย</summary>

   **ก** — ด่านทั้งสามผ่านแล้วแต่ไม่มีการเรียกการกระทำ fire_alert คือปลายท่อที่ทำเสียง แบนเนอร์ และนับครั้ง

   </details>

3. หลักฐานแบบใดดีที่สุดสำหรับอธิบายว่าเลือก HITS_NEEDED = 4 เพราะอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) "รู้สึกว่ากำลังดี"
   - ข) ตารางผลทดลอง: ที่ 4 เหตุการณ์จริงเตือนครบ 5/5 และเคสหลอกเตือน 0/5 ส่วนที่ 2 เคสหลอกเตือน 3/5
   - ค) ค่าเดียวกับเพื่อน
   - ง) ค่าที่มากที่สุดที่ใส่ได้

   <details><summary>เฉลย</summary>

   **ข** — การตัดสินใจเชิงวิศวกรรมต้องยืนบนการวัด จำนวนการเตือนจากเหตุการณ์จริงเทียบกับเคสหลอกคือหลักฐานของการแลกเปลี่ยน

   </details>

4. เดโม capstone ที่ดีควรแสดงอะไรนอกจากการเตือนที่ทำงาน *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) โค้ดทั้งไฟล์บนจอ
   - ข) เคสหลอกที่ Guardian ไม่เตือน และเหตุผลของการแลกเปลี่ยนที่เลือก
   - ค) จำนวนบรรทัดของโค้ด
   - ง) ไม่ต้องมีอะไรเพิ่ม

   <details><summary>เฉลย</summary>

   **ข** — ส่วนที่ยากและมีค่าคือการปฏิเสธสัญญาณปลอม และการอธิบายว่าทำไมตั้งค่าแบบนี้ นั่นคือความต่างระหว่างผลิตภัณฑ์กับเดโม

   </details>

## แล็บ

**MVP ของชุดบทเรียน 8.1–8.2:** ส่งมอบ Guardian ที่ทำงานครบอย่างน้อยสามเสา (DAQ, Processing, Apps) เฝ้าเหตุการณ์เป้าหมาย ผ่านชั้นตัดสินใจ (conf ที่กรองแล้วกับ debounce) แล้ว action ยิงจริง พร้อมอธิบายการออกแบบได้

- [ ] เติมไฟล์ฝึกครบห้าจุด รันบน Emulator หรือบอร์ดจนเห็นการเตือนจริง
- [ ] ออกแบบ Guardian ของคุณ ตั้งค่าออกแบบ แล้วทดสอบเหตุการณ์จริงกับเคสหลอกอย่างละอย่างน้อยห้าครั้ง จดผลลงบันทึกการเรียน
- [ ] ลองค่าออกแบบอย่างน้อยสองชุด เลือกชุดที่ใช้พร้อมเหตุผลจากตัวเลข
- [ ] อัดหรือเดโมสองนาที: การเตือนจริง เคสหลอกที่ไม่เตือน และการแลกเปลี่ยนที่เลือก ปิดท้ายด้วยคำถามวิจัยหรือทิศต่อยอดหนึ่งข้อ

## ไปต่อ

จบคอร์สแล้ว ต่อยอดได้ตามสี่ทิศในบทเรียนนี้ หรือกลับไปที่โมดูล 5 ฝึกโมเดลของคุณเองแล้วเสียบเข้า Guardian

นี่คือบทเรียนสุดท้ายของหลักสูตร กลับไปที่ [หน้าหลักสูตร](../../README.md) เพื่อดูทางไปต่อ

## สะท้อนคิด

- ค่าออกแบบที่คุณเลือกเปลี่ยนไปจากค่าเริ่มต้นเท่าไร และตัวเลขใดทำให้คุณเปลี่ยนใจ
- ถ้าต้องส่ง Guardian นี้ให้ลูกค้าใช้จริง อะไรคือสิ่งที่ยังขาดมากที่สุด
