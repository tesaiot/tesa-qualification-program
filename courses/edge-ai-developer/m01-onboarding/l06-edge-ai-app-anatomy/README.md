---
id: edgeai-dev.m01.l06
lang: th
title: {th: 'แกะแอป Edge AI: ทะเบียนโมเดล verdict และ action', en: 'Taking an edge AI app apart: the registry, the verdict and the action'}
summary: {th: แกะแอป Edge AI ที่โฟกัสโมเดลเดียวเป็นสามจังหวะ select → result → action เลือกโมเดลจากชื่อแทนเลข เข้าใจที่มาของ conf จาก softmax และ argmax แล้วเพิ่ม action ที่ยิงครั้งเดียวเมื่อเจอคลาสเป้าหมายที่มั่นใจพอ, en: 'Take a single-model edge AI app apart into select → result → action, pick the model by name instead of number, see where conf comes from (softmax and argmax), and add an action that fires once when a confident target class appears.'}
level: L3
time_min: {concept: 40, practise: 15, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m01.l05]
objectives:
  - {th: เขียน find_model() ที่ค้นโมเดลจากคำในชื่อผ่าน edge_ai.models() แล้วส่ง index ของ dict ที่ได้ไปให้ select() และอธิบายว่าทำไมทนกว่าการ select ด้วยเลขตายตัว, en: 'Write find_model() to look a model up by a word in its name via edge_ai.models(), pass the returned dict''s index to select(), and explain why this is sturdier than selecting a fixed number.'}
  - {th: คำนวณ softmax ของคะแนนดิบชุดเล็ก ๆ และบอกได้ว่า label มาจาก argmax ส่วน conf มาจาก max ของ scores ชุดเดียวกัน, en: Compute the softmax of a small set of raw scores and state that label comes from the argmax and conf from the max of the same scores.}
  - {th: เขียนเงื่อนไข action ที่ต้องผ่านทั้ง label ตรงเป้าหมายและ conf ≥ CONF_FLOOR พร้อมธง fired ที่ทำให้ action ยิงครั้งเดียวต่อการเจอ (edge-trigger), en: 'Write an action condition that needs both the target label and conf ≥ CONF_FLOOR, with a fired flag so the action fires once per detection (edge-triggered).'}
  - {th: เปรียบเทียบการ poll ด้วย result() กับ on_result(cb) ได้ว่าใครเป็นผู้ขับ ต้องเช็ก seq หรือไม่ และเหมาะกับงานแบบไหน, en: 'Compare polling with result() against on_result(cb) by who drives, whether seq must be checked, and what each suits.'}
develops: [{skill: ai.edge, to: 2}, {skill: lang.micropython, to: 2}, {skill: prog.state-machines, to: 1}, {skill: hw.math, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 1.6 — แกะแอป Edge AI: ทะเบียนโมเดล verdict และ action

> โมดูล 1 — เริ่มต้น: รันของจริงแล้วแกะดูข้างใน · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

แกะแอป Edge AI ที่โฟกัสโมเดลเดียวเป็นสามจังหวะ select → result → action เลือกโมเดลจากชื่อแทนเลข เข้าใจที่มาของ conf จาก softmax และ argmax แล้วเพิ่ม action ที่ยิงครั้งเดียวเมื่อเจอคลาสเป้าหมายที่มั่นใจพอ

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เขียน find_model() ที่ค้นโมเดลจากคำในชื่อผ่าน edge_ai.models() แล้วส่ง index ของ dict ที่ได้ไปให้ select() และอธิบายว่าทำไมทนกว่าการ select ด้วยเลขตายตัว
2. คำนวณ softmax ของคะแนนดิบชุดเล็ก ๆ และบอกได้ว่า label มาจาก argmax ส่วน conf มาจาก max ของ scores ชุดเดียวกัน
3. เขียนเงื่อนไข action ที่ต้องผ่านทั้ง label ตรงเป้าหมายและ conf ≥ CONF_FLOOR พร้อมธง fired ที่ทำให้ action ยิงครั้งเดียวต่อการเจอ (edge-trigger)
4. เปรียบเทียบการ poll ด้วย result() กับ on_result(cb) ได้ว่าใครเป็นผู้ขับ ต้องเช็ก seq หรือไม่ และเหมาะกับงานแบบไหน

## ก่อนเริ่ม

ผ่านชุดบทเรียน 1.1–1.5 มาแล้ว จำสี่คำสั่ง models, select, result, stop และโครงสี่จังหวะได้
เปิด `13_edge_ai_motion.py` ไว้ใน BENTO IDE และถ้ามี ให้เปิด `12_edge_ai_menu.py` เทียบด้วย

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — บน Emulator ไม่มี Push Detection และคะแนนของโมเดลเป็นค่าจำลอง
- **เรียนมาก่อน:** [บทเรียน 1.5 — ลงมือทำ: remix เป็น Tilt Monitor ของเรา](../l05-sensor-remix-lab/README.md)

## ดูของจริงก่อน

รัน `13_edge_ai_motion.py` ก่อนแตะโค้ด แล้วเขย่าบอร์ด วาดวงกลม หรือวางนิ่ง คลาสที่ชนะ แถบคะแนน และ latency เปลี่ยนสด
แอปนี้คือฝาแฝดโมเดลเดียวของเมนู `12_edge_ai_menu.py` ลองรันเทียบกันแล้วสังเกตว่า "โมเดลเดียว" ต่างจาก "เมนู" ตรงไหน

## แนวคิด

แอป Edge AI ที่โฟกัสโมเดลเดียวอ่านเป็น **สามจังหวะ**: (1) **select** เลือกโมเดลจากทะเบียน (2) **result** อ่านคำตัดสินแล้ววาดจอ
(3) **action** สั่งการเมื่อคำตัดสินเข้าเงื่อนไข ชุดบทเรียน 1.1–1.3 หยุดที่จังหวะ 2 บทเรียนนี้เติมจังหวะ 3 ซึ่งทำให้ Edge AI "ใช้งานได้จริง"
งานจริงส่วนใหญ่ไม่ให้ผู้ใช้เลือกโมเดลเอง นาฬิกาตรวจการล้มรันโมเดลเดียวตลอดแล้วลงมือเมื่อเจอ

ทะเบียนจาก `edge_ai.models()` เป็นแหล่งความจริงของแอป แทนที่จะ `select(0)` ด้วยเลขที่อาจสลับได้เมื่อเฟิร์มแวร์เปลี่ยน เราเขียน
`find_model(keyword)` ค้นจากชื่อแล้วคืน dict ทั้งก้อน ได้ทั้ง `index` ไปสั่ง select และ `labels` ไว้ตั้งคลาสเป้าหมาย เปลี่ยน keyword
คำเดียวก็ remix เป็นแอปของโมเดลอื่น

`scores` มาจาก **softmax** ที่บีบคะแนนดิบ (logits) $z_i$ ให้เป็นความน่าจะเป็นที่รวมกันได้ 1:
$\text{softmax}(z)_i = e^{z_i} / \sum_j e^{z_j}$ จากนั้น `label` คือ **argmax** (ตำแหน่งของคะแนนสูงสุด) และ `conf` คือ **max**
(ค่าคะแนนสูงสุด) เช่น scores = [0.03, 0.05, 0.92] ได้ label = shaking และ conf = 0.92 เส้น `CONF_FLOOR` จึงมีความหมายเพราะคะแนนถูก normalize แล้ว

action ต้องยิงเมื่อ **ใช่คลาสเป้าหมาย และ มั่นใจพอ** (`r['conf'] >= edge_ai.CONF_FLOOR`) และยิง **ครั้งเดียวต่อการเจอ** ด้วยธง `fired`
(edge-triggered) ไม่ใช่ยิงทุกเฟรมตลอดที่ยังเจอ (level-triggered) แยก "การตัดสินใจ" (เงื่อนไข `hit`) ออกจาก "การลงมือ" (`fire_action()`
ที่บี๊บด้วย `ui.tone` และขึ้นแบนเนอร์) จะ remix action ได้โดยไม่แตะ logic ตรวจจับ อีกทางหนึ่งคือ `edge_ai.on_result(cb)`
ที่ให้เฟิร์มแวร์เรียกฟังก์ชันของเราเมื่อมีคำตัดสิน (ทันทีที่คลาสเปลี่ยน และทวนคลาสเดิมราววินาทีละครั้ง) จึงไม่ต้องเช็ก `seq` เอง
แต่บน BENTO Emulator callback จะทำงานก็ต่อเมื่อโปรแกรมเรียก `edge_ai.result()` หรือ `edge_ai.active()`

## ตัวอย่างสมบูรณ์

`11_edge_ai_motion.py` ทำงานเดียวกับ `13` แต่ใช้โมดูลรุ่นเก่า (deepcraft) ได้แค่คลาสที่ชนะ ส่วน `13` ใช้ `edge_ai` จึงได้คะแนนทุกคลาสและ latency
เปิดสองไฟล์เทียบกันเพื่อเห็นว่าทะเบียนโมเดลให้อะไรเพิ่ม

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/11_edge_ai_motion.py](examples/11_edge_ai_motion.py) | Edge AI: โมเดล AI จำแนกการเคลื่อนไหว (รันบนบอร์ด ไม่ต้องต่อเน็ต) |
| [examples/13_edge_ai_motion.py](examples/13_edge_ai_motion.py) | Edge AI: Motion (IMU) ด้วย API ใหม่ edge_ai — เห็นคะแนนทุกคลาส + latency |

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นหรือใน `shared/` ด้วย:

- [m01-onboarding/l02-edge-ai-module/examples/12_edge_ai_menu.py](../l02-edge-ai-module/examples/12_edge_ai_menu.py) — Edge AI Menu: เลือกและรันโมเดล AI ได้ทุกตัวในเฟิร์มแวร์เดียว (ไม่ต้องต่อเน็ต)
- [m01-onboarding/l03-first-inference-lab/solution/s01_first_inference.py](../l03-first-inference-lab/solution/s01_first_inference.py) — รันโมเดล Edge AI ตัวแรกของเรา
- [m01-onboarding/l07-verdict-action-lab/examples/s03_anatomy_edgeai_full.py](../l07-verdict-action-lab/examples/s03_anatomy_edgeai_full.py) — เฝ้าจับคลาสด้วย on_result แล้วสั่งการ (ฉบับเต็ม)
- [m01-onboarding/l07-verdict-action-lab/practice/s03_anatomy_edgeai.py](../l07-verdict-action-lab/practice/s03_anatomy_edgeai.py) — แกะแอป Edge AI แล้ว remix: สลับโมเดล + สั่งการเมื่อเจอคลาส (ฉบับฝึกเติมโค้ด)

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. ทำไม find_model("Motion") ถึงดีกว่า edge_ai.select(0) ในแอปที่จะใช้กับหลายบอร์ด *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) เพราะ select() รับเลขไม่ได้
   - ข) เพราะลำดับโมเดลอาจต่างกันตามเฟิร์มแวร์หรือบอร์ด การค้นจากชื่อจึงได้โมเดลที่ต้องการเสมอ และได้ labels มาใช้ต่อด้วย
   - ค) เพราะ find_model() รันเร็วกว่าบน NPU
   - ง) เพราะชื่อโมเดลไม่เคยเปลี่ยน แต่ index เปลี่ยนทุกครั้งที่บูต

   <details><summary>เฉลย</summary>

   **ข** — บน Dev Kit Cough อยู่ที่ 3 แต่บน Emulator อยู่ที่ 2 เพราะไม่มี Push การถามทะเบียนด้วยชื่อทำให้โค้ดทนต่อความต่างนี้

   </details>

2. คะแนนดิบ z = [0, 0, 0] ของสามคลาส ผ่าน softmax แล้วได้อะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) [0, 0, 0]
   - ข) [1, 1, 1]
   - ค) [0.33, 0.33, 0.33] โดยประมาณ conf จึงต่ำกว่า CONF_FLOOR
   - ง) [1, 0, 0]

   <details><summary>เฉลย</summary>

   **ค** — e⁰ = 1 ทุกคลาส หารด้วยผลรวม 3 ได้ราว 0.33 เท่ากันหมด argmax ยังเลือกผู้ชนะได้หนึ่งตัว แต่ conf 0.33 ต่ำกว่า 0.50 จึงไม่ควรเชื่อ

   </details>

3. scores = [0.10, 0.70, 0.20] ของ labels ['idle', 'circle', 'shaking'] ค่า top, label และ conf คืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) top = 1, label = circle, conf = 0.70
   - ข) top = 0.70, label = circle, conf = 1
   - ค) top = 2, label = shaking, conf = 0.20
   - ง) top = 1, label = idle, conf = 0.10

   <details><summary>เฉลย</summary>

   **ก** — argmax ให้ตำแหน่ง 1 (top) ซึ่งตรงกับชื่อ circle ส่วน max ให้ค่า 0.70 คือ conf

   </details>

4. เขย่าบอร์ดค้างสามวินาที โมเดลตอบ shaking ทุกเฟรม ถ้าไม่มีธง fired จะเกิดอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) action ยิงครั้งเดียวเหมือนเดิม
   - ข) action ยิงทุกเฟรมที่ยังเจอ บี๊บรัวจนน่ารำคาญ (level-triggered)
   - ค) action ไม่ยิงเลย
   - ง) โมเดลหยุดทำงาน

   <details><summary>เฉลย</summary>

   **ข** — ธง fired ทำให้ยิงตอนขอบขาขึ้นครั้งเดียว แล้วรีเซ็ตเมื่อออกจากคลาสเป้าหมาย นี่คือ edge-trigger แบบเดียวกับการกดปุ่มหนึ่งครั้งได้ event หนึ่งครั้ง

   </details>

5. ข้อใดถูกต้องเกี่ยวกับ on_result(cb) เทียบกับการ poll ด้วย result() (เลือกทุกข้อที่ถูก) *(เลือกได้หลายข้อ · เป้าหมายข้อ 4)*
   - ก) เฟิร์มแวร์เป็นผู้เรียก cb ให้ เราจึงไม่ต้องเช็ก seq เอง
   - ข) cb ถูกเรียกทันทีที่คลาสเปลี่ยน และอาจถูกเรียกซ้ำด้วยคลาสเดิมราววินาทีละครั้ง จึงยังต้องมีธง fired
   - ค) การ poll เห็นทุกจังหวะในลูปเดียว เหมาะกับตอนเริ่มเรียน
   - ง) on_result ทำให้ไม่ต้องเรียก edge_ai.stop() ตอนจบ

   <details><summary>เฉลย</summary>

   **ก, ข, ค** — ทั้งสองวิธีถูกต้อง ต่างกันที่ใครถาม ตอนจบยังต้องถอน callback ด้วย on_result(None) แล้ว stop() เสมอ

   </details>

## แล็บ

- [ ] รัน `13_edge_ai_motion.py` แล้วจดลงบันทึกการเรียนว่าแต่ละท่าให้คลาสอะไรและ conf ประมาณเท่าไร
- [ ] ใน REPL ลองเขียน `find_model("Cough")` แล้วพิมพ์ `index` กับ `labels` ที่ได้ เทียบกับบอร์ดหรือ Emulator ของคุณ
- [ ] คิดเลข softmax ของ z = [2.0, 3.1, 1.2] ด้วยเครื่องคิดเลขแล้วบอกว่าคลาสไหนชนะด้วย conf เท่าไร

## ไปต่อ

บทเรียน 1.7 เราจะเติมไฟล์ `s03_anatomy_edgeai.py` จนแอปบี๊บและขึ้นแบนเนอร์เองเมื่อเจอคลาสเป้าหมาย แล้ว remix ให้เป็นของเรา

บทเรียนถัดไป: [บทเรียน 1.7 — ลงมือทำ: จาก verdict สู่ action บนบอร์ด](../l07-verdict-action-lab/README.md)

## สะท้อนคิด

- ในบ้านหรือที่ทำงานของคุณ มีงานไหนที่ "รู้ว่าเจออะไร" ยังไม่พอ ต้อง "ลงมือทำต่อ" ด้วย และ action นั้นควรยิงครั้งเดียวหรือยิงซ้ำได้
- ถ้า action ของคุณคือโทรแจ้งเหตุฉุกเฉิน คุณจะตั้ง CONF_FLOOR สูงหรือต่ำ เพราะอะไร
