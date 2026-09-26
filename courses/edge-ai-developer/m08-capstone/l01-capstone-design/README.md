---
id: edgeai-dev.m08.l01
lang: th
title: {th: 'ออกแบบ capstone: Guardian สามเสาในไฟล์เดียว', en: 'Designing the capstone: Guardian, three pillars in one file'}
summary: {th: ออกแบบ capstone ที่ต่างจากเดโมหนึ่งชิ้น Guardian ร้อยสามเสาของวงจรข้อมูลไว้ในลูปเดียว ได้แก่ DAQ (ความเร่งดิบเป็นบริบท) Processing (EMA กรองความมั่นใจ) และ Apps (verdict ผ่านชั้นตัดสินใจแล้วสั่งการ) พร้อมคณิตของขนาดเวกเตอร์ EMA และเงื่อนไขยิงสามด่าน และการเลือกค่าออกแบบอย่างมีเหตุผล, en: 'Design a capstone that is more than one more demo. The Guardian threads three pillars of the data lifecycle through one loop - DAQ (raw acceleration as context), Processing (EMA-filtered confidence) and Apps (a verdict through a decision layer to an action) - with the maths of vector magnitude, EMA and the three-gate firing rule, and reasoned choices of design values.'}
level: L3
time_min: {concept: 45, practise: 15, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m07.l04]
objectives:
  - {th: 'แยก capstone หรือผลิตภัณฑ์ออกจากเดโม และชี้ได้ว่า Guardian ข้ามสามเสาใด (DAQ, Processing, Apps) และต่อยอดด้วยเสา Training หรือ Analysis ได้อย่างไร', en: 'Tell a capstone or product from a demo, and show which three pillars the Guardian crosses (DAQ, Processing, Apps) and how Training or Analysis could extend it.'}
  - {th: คำนวณขนาดเวกเตอร์ความเร่งและ EMA ของความมั่นใจหนึ่งก้าว และอธิบายว่าทำไมต้องสร้างตัวกรองนอกลูปและล้างเมื่อกด Load, en: 'Compute the acceleration vector magnitude and one EMA step of the confidence, and explain why the filter is created outside the loop and reset on Load.'}
  - {th: เขียนเงื่อนไขยิง (top = alert_idx) ∧ (s_n ≥ CONF_FLOOR) ∧ (streak ≥ HITS_NEEDED) พร้อม edge-trigger และบอกว่าพีคหลอกแบบใดถูกด่านใดกันไว้, en: 'Write the firing rule (top = alert_idx) ∧ (s_n ≥ CONF_FLOOR) ∧ (streak ≥ HITS_NEEDED) with an edge trigger, and say which gate stops which kind of fake peak.'}
  - {th: 'เลือกค่า CONF_FLOOR, HITS_NEEDED, EMA_ALPHA และจังหวะลูปให้ผลิตภัณฑ์ที่กำหนด พร้อมเหตุผลเรื่องการพลาดของจริงเทียบกับการเตือนผิด ความไว ความนิ่ง และพลังงาน', en: 'Choose CONF_FLOOR, HITS_NEEDED, EMA_ALPHA and the loop period for a given product, with reasons about misses versus false alarms, responsiveness, stability and energy.'}
develops: [{skill: ai.edge, to: 3}, {skill: biz.product-decision, to: 2}, {skill: sys.dsp, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 8.1 — ออกแบบ capstone: Guardian สามเสาในไฟล์เดียว

> โมดูล 8 — Capstone: แอป Edge AI ของเราเอง · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

ออกแบบ capstone ที่ต่างจากเดโมหนึ่งชิ้น Guardian ร้อยสามเสาของวงจรข้อมูลไว้ในลูปเดียว ได้แก่ DAQ (ความเร่งดิบเป็นบริบท) Processing (EMA กรองความมั่นใจ) และ Apps (verdict ผ่านชั้นตัดสินใจแล้วสั่งการ) พร้อมคณิตของขนาดเวกเตอร์ EMA และเงื่อนไขยิงสามด่าน และการเลือกค่าออกแบบอย่างมีเหตุผล

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. แยก capstone หรือผลิตภัณฑ์ออกจากเดโม และชี้ได้ว่า Guardian ข้ามสามเสาใด (DAQ, Processing, Apps) และต่อยอดด้วยเสา Training หรือ Analysis ได้อย่างไร
2. คำนวณขนาดเวกเตอร์ความเร่งและ EMA ของความมั่นใจหนึ่งก้าว และอธิบายว่าทำไมต้องสร้างตัวกรองนอกลูปและล้างเมื่อกด Load
3. เขียนเงื่อนไขยิง (top = alert_idx) ∧ (s_n ≥ CONF_FLOOR) ∧ (streak ≥ HITS_NEEDED) พร้อม edge-trigger และบอกว่าพีคหลอกแบบใดถูกด่านใดกันไว้
4. เลือกค่า CONF_FLOOR, HITS_NEEDED, EMA_ALPHA และจังหวะลูปให้ผลิตภัณฑ์ที่กำหนด พร้อมเหตุผลเรื่องการพลาดของจริงเทียบกับการเตือนผิด ความไว ความนิ่ง และพลังงาน

## ก่อนเริ่ม

ผ่านโมดูล 1 ถึง 7 มาแล้ว มี logger ฟิลเตอร์ โมเดลที่ฝึกเอง และท่อสั่งการในมือ
เปิด `s20_capstone_full.py` (อยู่ในบทเรียน 8.2) ไว้ใน BENTO IDE

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — Guardian ใช้ IMU กับ edge_ai ซึ่ง Emulator รองรับ (โมเดล Motion กับปุ่ม Shake) เหตุการณ์จริงอย่างเสียงหรือเรดาร์ต้องใช้บอร์ด
- **เรียนมาก่อน:** [บทเรียน 7.4 — ลงมือทำ: ให้โมเดลใหม่โผล่ใน edge_ai.models()](../../m07-under-the-hood/l04-extend-model-lab/README.md)

## ดูของจริงก่อน

รัน `s20_capstone_full.py` เลือก Motion กด Load แล้วเขย่าค้างจนแบนเนอร์ `! ALERT !` เด้งพร้อมเสียงและตัวนับ จากนั้นเขย่าแวบเดียว
สังเกตว่ามันไม่เตือน ถามตัวเองว่า Guardian ใช้ของจากโมดูลใดบ้างถึงทำแบบนี้ได้

## แนวคิด

**เดโม** ตอบว่า "ทำได้ไหม" ในสภาพอุดมคติ ส่วน **capstone** ตอบว่า "ใช้ได้จริงไหม" ต้องรับมือ noise, false positive และการเก็บกวาด แล้วอธิบายการออกแบบได้
ข้อกำหนดคือต้องข้ามอย่างน้อยสามเสาของวงจรข้อมูล Guardian ร้อยสามเสาในลูป `while` เดียว: **DAQ** อ่าน `ax, ay, az = sensors.bmi270.acceleration()`
แล้วหา $mag = \sqrt{a_x^2 + a_y^2 + a_z^2}$ (วางนิ่งราว 9.8 m/s², เขย่าพุ่งขึ้น) เป็นบริบท **Processing** กรองความมั่นใจด้วย
$s_n = \alpha c_n + (1-\alpha) s_{n-1}$ ผ่าน `conf_ema = dsp.EMA(alpha=EMA_ALPHA)` ที่สร้างนอกลูปเพราะต้องจำอดีต และ `reset()` เมื่อกด Load เพื่อเริ่มเฝ้ารอบใหม่
**Apps** ใช้แกนเดิม `models` / `select` / `result` / `stop` กับ `CONF_FLOOR` แล้วเพิ่มชั้นตัดสินใจ ต่อยอดได้ด้วยโมเดลที่ฝึกเอง (Training) หรือ feature จาก FFT (Analysis)

ชั้นตัดสินใจมีสามด่านซ้อนกัน: คลาสถูกตัว (`top == alert_idx` โดยกติกาออกแบบให้คลาสสุดท้ายคือเหตุการณ์ เช่น shaking) มั่นใจพอจากค่าที่กรองแล้ว
(`conf_s >= CONF_FLOOR`) และติดกันพอ (`streak >= HITS_NEEDED`) คือ
$\text{fire} \iff (top = alert\_idx) \wedge (s_n \ge \text{CONF\_FLOOR}) \wedge (streak \ge \text{HITS\_NEEDED})$ แล้วใช้ธง `fired` ยิงครั้งเดียวต่อเหตุการณ์
พลาดด่านไหน `streak` กลับเป็นศูนย์ false positive ส่วนใหญ่ผ่านได้แค่หนึ่งหรือสองด่าน การบังคับให้ผ่านครบสามคือเหตุผลที่พีคแวบเดียวไม่ทำให้เตือน

ทุกค่าออกแบบมีราคาสองด้าน `CONF_FLOOR` สูงพลาดของจริง ต่ำเตือนผิด `HITS_NEEDED` สูงตอบช้า ต่ำโดนพีคหลอก `EMA_ALPHA` สูงไวแต่แกว่ง ต่ำนิ่งแต่หน่วง
และ `time.sleep_ms` ของลูปแลกพลังงานกับความไว ไม่มีค่าที่ถูกที่สุด มีแต่ค่าที่เหมาะกับต้นทุนของการพลาดในงานนั้น เช่นตรวจการล้มของผู้สูงอายุยอมเตือนผิดดีกว่าพลาด
ส่วนป้ายโฆษณากวักมือยอมพลาดดีกว่ากวนคนเดินผ่าน capstone เริ่มที่ **Design** (เฝ้าอะไร action อะไร เกณฑ์เท่าไรเพราะอะไร) แล้วค่อย **Build** และ **Ship**

## ตัวอย่างสมบูรณ์

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นหรือใน `shared/` ด้วย:

- [m08-capstone/l02-capstone-build-lab/examples/s20_capstone_full.py](../l02-capstone-build-lab/examples/s20_capstone_full.py) — Capstone: Edge AI Guardian (ฉบับเต็ม)
- [m08-capstone/l02-capstone-build-lab/practice/s20_capstone.py](../l02-capstone-build-lab/practice/s20_capstone.py) — Capstone: Edge AI Guardian (ฉบับฝึกเติมโค้ด)

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. Guardian แตะเสาใดโดยตรงบ้าง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) DAQ, Processing และ Apps
   - ข) Training เท่านั้น
   - ค) Analysis กับ Training
   - ง) Apps เท่านั้น

   <details><summary>เฉลย</summary>

   **ก** — อ่านความเร่งดิบ (DAQ) กรองความมั่นใจด้วย EMA (Processing) และ verdict สู่ action (Apps) ส่วน Training กับ Analysis เป็นทางต่อยอด

   </details>

2. EMA_ALPHA = 0.4 ค่าที่กรองไว้เดิม 0.30 และ conf ดิบใหม่ 0.90 ได้ค่าใหม่เท่าไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) 0.90
   - ข) 0.60
   - ค) 0.54
   - ง) 0.36

   <details><summary>เฉลย</summary>

   **ค** — 0.4 × 0.90 + 0.6 × 0.30 = 0.36 + 0.18 = 0.54 ผ่านเกณฑ์ 0.50 แล้ว แต่ยังต้องผ่านด่าน streak ด้วย

   </details>

3. ถ้าสร้าง dsp.EMA ใหม่ทุกรอบในลูป จะเกิดอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) กรองได้ดีขึ้น
   - ข) ตัวกรองเสียความจำทุกเฟรม ค่าออกเท่ากับค่าดิบ จึงไม่ได้กรองอะไรเลย
   - ค) โปรแกรมหยุด
   - ง) ค่ากลายเป็นศูนย์

   <details><summary>เฉลย</summary>

   **ข** — EMA ครั้งแรกคืนค่าที่ป้อนเข้าไป ถ้าสร้างใหม่ทุกรอบก็เหมือนไม่มีตัวกรอง จึงต้องสร้างครั้งเดียวก่อนลูป

   </details>

4. top = alert_idx, conf_s = 0.62 และ streak = 2 ขณะ HITS_NEEDED = 3 Guardian ยิงหรือไม่ *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) ยิง เพราะคลาสถูกและมั่นใจพอ
   - ข) ยังไม่ยิง เพราะด่าน streak ยังไม่ครบ
   - ค) ยิงสองครั้ง
   - ง) ไม่ยิงเพราะ conf ต่ำ

   <details><summary>เฉลย</summary>

   **ข** — ต้องผ่านครบทั้งสามด่านพร้อมกัน ถ้าผลถัดไปยังถูกคลาสและมั่นใจพอ streak จะครบ 3 แล้วยิงครั้งเดียว

   </details>

5. Guardian ตรวจการล้มของผู้สูงอายุ ควรปรับค่าไปทางใด *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) CONF_FLOOR สูงและ HITS_NEEDED มาก เพื่อไม่ให้เตือนผิดเลย
   - ข) ยอมเตือนผิดได้บ้างเพื่อไม่พลาดของจริง เช่น CONF_FLOOR ต่ำลงและ HITS_NEEDED น้อยลง
   - ค) ไม่ต้องมีชั้นตัดสินใจ
   - ง) EMA_ALPHA = 0

   <details><summary>เฉลย</summary>

   **ข** — ต้นทุนของการพลาดการล้มสูงกว่าการเตือนผิดมาก การจูนจึงต้องเอนไปทางไว แล้วเขียนเหตุผลนี้ไว้ในการออกแบบ

   </details>

## แล็บ

- [ ] เขียนแผนผังสามเสาของ Guardian ในบันทึกการเรียน พร้อมชื่อคำสั่งหลักของแต่ละเสา
- [ ] ใช้ 15 นาทีออกแบบ Guardian ของคุณ: เฝ้าโมเดลใด เหตุการณ์คืออะไร action คืออะไร และต้นทุนของการพลาดกับการเตือนผิดต่างกันแค่ไหน
- [ ] เลือกค่าเริ่มต้นของ `CONF_FLOOR`, `HITS_NEEDED`, `EMA_ALPHA` พร้อมเหตุผลหนึ่งบรรทัดต่อค่า

## ไปต่อ

บทเรียน 8.2 เราจะเติมห้าบรรทัดสันหลังของ `s20_capstone.py` แล้วสร้าง จูน และเดโม Guardian ของเราเอง

บทเรียนถัดไป: [บทเรียน 8.2 — ลงมือทำ: สร้างและส่งมอบแอป Edge AI](../l02-capstone-build-lab/README.md)

## สะท้อนคิด

- งานรอบตัวคุณงานไหนที่การพลาดของจริงแพงกว่าการเตือนผิด และงานไหนกลับกัน
- ถ้าได้เพิ่มเสาที่สี่ให้ Guardian คุณจะเลือก Training หรือ Analysis และได้อะไรเพิ่ม
