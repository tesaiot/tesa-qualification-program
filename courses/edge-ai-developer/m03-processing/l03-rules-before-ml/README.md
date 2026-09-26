---
id: edgeai-dev.m03.l03
lang: th
title: {th: 'ค่าอนุพัทธ์และการจำแนกด้วยกฎ: dew point, heat index และบันไดกฎ', en: 'Derived metrics and rule-based classification: dew point, heat index and the rule ladder'}
summary: {th: เขียน classifier ตัวแรกของหลักสูตรโดยยังไม่ใช้ ML แปลงอุณหภูมิกับความชื้นเป็นค่าอนุพัทธ์ dew point และ heat index แล้วตัดสินเป็นคลาสด้วยเส้นแบ่งและบันไดกฎที่ลำดับชั้นถูกต้อง, en: 'Build the course''s first classifier without ML - turn temperature and humidity into the derived metrics dew point and heat index, then decide a class with thresholds and a correctly ordered rule ladder.'}
level: L3
time_min: {concept: 40, practise: 10, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m03.l02]
objectives:
  - {th: อธิบายได้ว่า classifier คือกล่องที่รับตัวเลขแล้วคืนคลาส และเปรียบเทียบการหาเส้นแบ่งด้วยกฎมือกับด้วย ML ได้อย่างน้อยสองมิติ (ข้อมูลฝึก ความอธิบายได้ หรือความซับซ้อนของ pattern), en: 'Explain a classifier as a box that takes numbers and returns a class, and compare hand-set rules with ML on at least two dimensions (training data, explainability or pattern complexity).'}
  - {th: เรียก dsp.dew_point และ dsp.heat_index แล้วอธิบายได้ว่าทำไมค่าอนุพัทธ์ช่วยให้กฎตัดสินได้ดีกว่าค่าดิบ เช่น 32°C ที่ความชื้น 40% กับ 80% ให้ heat index ต่างกันราว 12 องศา, en: Call dsp.dew_point and dsp.heat_index and explain why derived metrics help rules decide better than raw values (for example 32°C at 40% and 80% humidity differ by about 12 degrees of heat index).}
  - {th: เรียงบันไดกฎหลายชั้นให้เงื่อนไขที่เฉพาะหรือรุนแรงกว่าอยู่บน และหา dead branch ในบันไดที่เรียงผิดได้, en: 'Order a multi-step rule ladder with the more specific or severe conditions on top, and spot the dead branch in a wrongly ordered ladder.'}
develops: [{skill: ai.edge, to: 1}, {skill: sys.dsp, to: 2}, {skill: prog.algo-ds, to: 2}, {skill: sys.sensors-actuators, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 3.3 — ค่าอนุพัทธ์และการจำแนกด้วยกฎ: dew point, heat index และบันไดกฎ

> โมดูล 3 — ประมวลผลด้วยคณิตศาสตร์และฟิสิกส์ · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เขียน classifier ตัวแรกของหลักสูตรโดยยังไม่ใช้ ML แปลงอุณหภูมิกับความชื้นเป็นค่าอนุพัทธ์ dew point และ heat index แล้วตัดสินเป็นคลาสด้วยเส้นแบ่งและบันไดกฎที่ลำดับชั้นถูกต้อง

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. อธิบายได้ว่า classifier คือกล่องที่รับตัวเลขแล้วคืนคลาส และเปรียบเทียบการหาเส้นแบ่งด้วยกฎมือกับด้วย ML ได้อย่างน้อยสองมิติ (ข้อมูลฝึก ความอธิบายได้ หรือความซับซ้อนของ pattern)
2. เรียก dsp.dew_point และ dsp.heat_index แล้วอธิบายได้ว่าทำไมค่าอนุพัทธ์ช่วยให้กฎตัดสินได้ดีกว่าค่าดิบ เช่น 32°C ที่ความชื้น 40% กับ 80% ให้ heat index ต่างกันราว 12 องศา
3. เรียงบันไดกฎหลายชั้นให้เงื่อนไขที่เฉพาะหรือรุนแรงกว่าอยู่บน และหา dead branch ในบันไดที่เรียงผิดได้

## ก่อนเริ่ม

ผ่านชุดบทเรียน 3.1–3.2 มาแล้ว เข้าใจรูปแบบ raw → derived → viz
เปิด REPL ไว้ลอง `dsp.dew_point`, `dsp.heat_index` และ `dsp.comfort_zone` ด้วยค่าที่คุณเลือกเอง

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — ใช้ DPS368 กับ SHT40 ที่มีบน TESAIoT Dev Kit (Eva Kit ไม่มี) ส่วน Emulator จำลองค่าอุณหภูมิและความชื้นให้
- **เรียนมาก่อน:** [บทเรียน 3.2 — ลงมือทำ: เกจฟิสิกส์สี่ตัวบนจอ](../l02-physics-gauges-lab/README.md)

## ดูของจริงก่อน

รันกฎสำเร็จรูป `dsp.comfort_zone(t, rh)` ที่เฟิร์มแวร์มีให้ก่อน มันตอบ `comfortable`, `hot`, `humid` ฯลฯ ได้เลย
แล้วค่อยถามว่า "มันรู้ได้ยังไงว่าตอนนี้ร้อน" ซึ่งคำตอบคือ `if` ไม่กี่บรรทัดในภาษา C ไม่มี AI สักนิด

## แนวคิด

**Classifier** คือฟังก์ชันที่รับตัวเลขแล้วคืน "คลาส" หนึ่งป้ายจากชุดที่กำหนด โมเดล Motion ในโมดูล 1 ก็เป็น classifier เพียงแต่ข้างในเป็น
neural network ส่วนวันนี้ข้างในคือ **กฎที่เราตั้งเอง** รูปเข้าออกเหมือนกัน ต่างที่วิธีหาเส้นแบ่ง: กฎมือไม่ต้องมีข้อมูลฝึก รันได้ทันที
และอธิบายได้ทุกคำตัดสิน แต่จะบานเมื่อเงื่อนไขเยอะและไม่เก่งกับ pattern ซับซ้อน ส่วน ML เรียนเส้นแบ่งจากข้อมูลและจับ pattern
หลายมิติได้ แต่ต้องมีข้อมูล ต้องฝึก และอธิบาย "ทำไม" ได้ยากกว่า ในงานจริงหลายอย่างกฎ threshold ง่าย ๆ ชนะ ML

ค่าดิบบางทีตัดสินยาก 32°C ตอนแห้งกับตอนชื้นจัดรู้สึกต่างกันมาก **ค่าอนุพัทธ์** (derived metric) รวมหลายค่าดิบเป็นตัวเดียวที่ตัดสินง่ายขึ้น
ซึ่งในโลก ML เรียกว่า feature engineering `dsp.dew_point(t, rh)` ใช้สูตร Magnus–Tetens คืนจุดน้ำค้าง (dew point ยิ่งเข้าใกล้อุณหภูมิ
อากาศยิ่งอิ่มตัว) `dsp.heat_index(t, rh)` ใช้ Rothfusz regression คืน "อุณหภูมิที่รู้สึก" เช่น 32°C ที่ 40% ได้ราว 32°C แต่ที่ 80% ได้ราว 44°C
ทั้งสองคำนวณบน CM33 ไม่ใช้ NPU และ `dsp.comfort_zone` คือ classifier สำเร็จรูปที่ตัดสินจากค่าดิบ `t` กับ `rh` ด้วยบันได `if`

หน่วยย่อยที่สุดของกฎคือ **เส้นแบ่งเดียว** ที่แบ่งโลกเป็นสองคลาส ตำแหน่งของเส้น (เช่น heat index 32) คือ hyperparameter ของกฎที่เราเลือกเอง
จากความรู้หรือมาตรฐาน พอต้องการหลายคลาสเราเรียง `if` เป็น **บันไดกฎ** ไล่จากบนลงล่าง ขั้นแรกที่เป็นจริงชนะแล้ว return จบทันที
กฎเหล็กคือ **เงื่อนไขที่เฉพาะหรือรุนแรงกว่าต้องอยู่บน** ถ้าวาง `hi >= 32` ไว้เหนือ `hi >= 41` ค่า 43 จะได้ `hot` และชั้น `danger`
ไม่มีวันถูกเรียก เป็น dead branch ที่ compiler ไม่เตือน ต้องจับด้วยการทดสอบ

## ตัวอย่างสมบูรณ์

`08_environment_dashboard.py` เป็นแดชบอร์ดสามการ์ด (อุณหภูมิ ความชื้น ความดัน) ที่อ่านเซนเซอร์ชุดเดียวกับบทเรียนนี้
รันดูค่าดิบก่อน แล้วลองคิดว่าถ้าจะให้การ์ดบอก "สบายหรือไม่" ต้องเพิ่มค่าอนุพัทธ์ตัวไหน

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/08_environment_dashboard.py](examples/08_environment_dashboard.py) | Environment Dashboard: 3 การ์ด (อุณหภูมิ / ความชื้น / ความดัน) |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. ข้อใดเป็นจุดแข็งของกฎมือเมื่อเทียบกับ ML (เลือกทุกข้อที่ถูก) *(เลือกได้หลายข้อ · เป้าหมายข้อ 1)*
   - ก) ไม่ต้องมีข้อมูลฝึก รันได้ทันที
   - ข) อธิบายได้ว่าคำตัดสินมาจากเงื่อนไขใด
   - ค) จับ pattern ซับซ้อนหลายสิบมิติได้ดี
   - ง) ปรับเส้นแบ่งตามข้อมูลใหม่ได้เอง

   <details><summary>เฉลย</summary>

   **ก, ข** — สองข้อหลังเป็นจุดแข็งของ ML ที่เรียนเส้นแบ่งจากข้อมูล ส่วนกฎมือเบา อธิบายได้ และไม่ต้องมีข้อมูลฝึก

   </details>

2. ทำไมบันไดกฎของบทเรียนนี้ตัดสิน hot และ danger จาก heat index แทนอุณหภูมิดิบ *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) เพราะ heat index อ่านได้เร็วกว่า
   - ข) เพราะอุณหภูมิเท่ากันแต่ความชื้นต่างกันทำให้ร่างกายรู้สึกต่างกันมาก heat index รวมผลนั้นไว้แล้ว
   - ค) เพราะเซนเซอร์อุณหภูมิไม่แม่น
   - ง) เพราะ heat index เป็นจำนวนเต็มเสมอ

   <details><summary>เฉลย</summary>

   **ข** — 32°C ที่ความชื้น 80% รู้สึกเหมือนราว 44°C ถ้าตัดสินจากอุณหภูมิดิบจะพลาดภาวะร้อนอบอ้าวที่อันตรายจริง

   </details>

3. dew point เข้าใกล้อุณหภูมิอากาศมาก หมายความว่าอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) อากาศแห้งมาก
   - ข) อากาศใกล้อิ่มตัว ชื้นมาก ไอน้ำใกล้จะกลั่นเป็นหยดน้ำ
   - ค) เซนเซอร์เสีย
   - ง) อุณหภูมิกำลังลดลงเร็ว

   <details><summary>เฉลย</summary>

   **ข** — เมื่อ RH เข้าใกล้ 100% ค่า ln(RH/100) เข้าใกล้ 0 ทำให้ dew point เข้าใกล้อุณหภูมิจริง ระยะห่าง t − Td จึงเป็นสัญญาณความชื้นที่ดี

   </details>

4. บันไดเขียนว่า if hi >= 32: return "hot" ไว้ก่อน if hi >= 41: return "danger" อินพุต hi = 43 จะได้อะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) danger
   - ข) hot และชั้น danger กลายเป็น dead branch ที่ไม่มีวันถูกเรียก
   - ค) error เพราะเงื่อนไขซ้อนกัน
   - ง) comfortable

   <details><summary>เฉลย</summary>

   **ข** — บันได return ขั้นแรกที่จริง 43 ≥ 32 จึงตอบ hot ก่อนถึงชั้น danger เงื่อนไขที่รุนแรงกว่าต้องอยู่บนเสมอ

   </details>

## แล็บ

- [ ] ใน REPL เรียก `dsp.heat_index(32, 40)` และ `dsp.heat_index(32, 80)` จดผลลงบันทึกการเรียน
- [ ] เรียก `dsp.comfort_zone` ด้วยค่าสามชุดที่ได้คลาสต่างกัน แล้วเขียนว่าค่าชุดไหนตกชั้นไหนของบันได
- [ ] เขียนบันไดกฎ 6 ชั้นลงกระดาษ แล้วสลับสองชั้นบนเพื่อหาอินพุตที่ทำให้เกิด dead branch

## ไปต่อ

บทเรียน 3.4 เราจะเขียน `classify()` ของตัวเองในไฟล์ `s07_rule_classifier.py` แล้วเทียบกับกฎสำเร็จรูปของเฟิร์มแวร์

บทเรียนถัดไป: [บทเรียน 3.4 — ลงมือทำ: ตัวจำแนกความสบายด้วยกฎ](../l04-rule-classifier-lab/README.md)

## สะท้อนคิด

- มีงานไหนที่คุณคิดว่าควรใช้กฎมากกว่า ML เพราะต้องอธิบายคำตัดสินได้หรือมีเกณฑ์กฎหมายกำหนดไว้แล้ว
- ถ้าเซนเซอร์ของคุณมี 50 ค่า การเขียนบันไดกฎจะยากขึ้นตรงไหน
