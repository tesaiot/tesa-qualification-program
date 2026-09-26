---
id: edgeai-dev.m01.l03
lang: th
title: {th: 'ลงมือทำ: เมนูโมเดลตัวแรกของเรา', en: 'Hands-on: your first model menu'}
summary: {th: 'ไล่โค้ดไฟล์ s01_first_inference.py ตามโครงสี่จังหวะของโปรแกรม MicroPython แล้วเติมสี่ช่องด้วยคำสั่ง select, result, verdict.text และ stop จนเมนู Edge AI ทำงานครบวงจรและปิดตัวเองอย่างเรียบร้อย', en: 'Walk through s01_first_inference.py along the four-beat MicroPython program skeleton, then fill its four blanks with select, result, verdict.text and stop until the edge AI menu works end to end and shuts down cleanly.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 20, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m01.l02]
objectives:
  - {th: 'ชี้ได้ว่าส่วนใดของ s01_first_inference.py อยู่ในจังหวะ import, สร้างครั้งเดียว, ลูป และ ui.poll และอธิบายว่าทำไมต้องสร้าง widget นอกลูป', en: 'Point out which parts of s01_first_inference.py belong to the import, create-once, loop and ui.poll beats, and explain why widgets are created outside the loop.'}
  - {th: เติมสี่ช่องใน practice/s01_first_inference.py จนกด Load แล้วเห็นคลาสที่ชนะและแถบความมั่นใจทุกคลาสเปลี่ยนตามท่าทางหรือเสียง และกด Stop แล้วโมเดลหยุดจริง, en: 'Fill the four blanks in practice/s01_first_inference.py until Load shows the winning class and every class''s confidence bar changing with motion or sound, and Stop really stops the model.'}
  - {th: 'อธิบายว่าการเช็ก r[''seq''] ก่อนวาดจอ และบล็อก finally ที่เรียก edge_ai.stop() ป้องกันปัญหาอะไร', en: 'Explain what checking r[''seq''] before redrawing and the finally block that calls edge_ai.stop() protect against.'}
  - {th: หาท่าหรือเสียงที่ทำให้ conf ต่ำกว่า 50% แล้วอธิบายได้ว่าทำไมคะแนนถึงกระจาย, en: Find a motion or sound that keeps conf below 50% and explain why the scores spread out.}
develops: [{skill: lang.micropython, to: 2}, {skill: ai.edge, to: 2}, {skill: gui.embedded, to: 1}]
assesses: [{skill: lang.micropython, level: 2, evidence: practice/s01_first_inference.py}, {skill: ai.edge, level: 2, evidence: practice/s01_first_inference.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 1.3 — ลงมือทำ: เมนูโมเดลตัวแรกของเรา

> โมดูล 1 — เริ่มต้น: รันของจริงแล้วแกะดูข้างใน · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

ไล่โค้ดไฟล์ s01_first_inference.py ตามโครงสี่จังหวะของโปรแกรม MicroPython แล้วเติมสี่ช่องด้วยคำสั่ง select, result, verdict.text และ stop จนเมนู Edge AI ทำงานครบวงจรและปิดตัวเองอย่างเรียบร้อย

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. ชี้ได้ว่าส่วนใดของ s01_first_inference.py อยู่ในจังหวะ import, สร้างครั้งเดียว, ลูป และ ui.poll และอธิบายว่าทำไมต้องสร้าง widget นอกลูป
2. เติมสี่ช่องใน practice/s01_first_inference.py จนกด Load แล้วเห็นคลาสที่ชนะและแถบความมั่นใจทุกคลาสเปลี่ยนตามท่าทางหรือเสียง และกด Stop แล้วโมเดลหยุดจริง
3. อธิบายว่าการเช็ก r['seq'] ก่อนวาดจอ และบล็อก finally ที่เรียก edge_ai.stop() ป้องกันปัญหาอะไร
4. หาท่าหรือเสียงที่ทำให้ conf ต่ำกว่า 50% แล้วอธิบายได้ว่าทำไมคะแนนถึงกระจาย

## ก่อนเริ่ม

ผ่านบทเรียน 1.2 มาแล้ว และรู้ว่าสี่คำสั่ง models, select, result, stop ทำอะไร
เปิดไฟล์ฝึกใน BENTO IDE เตรียมบันทึกการเรียนไว้จดว่าแต่ละโมเดลต้องทำท่าหรือเสียงแบบไหนถึงจะชนะ

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/)
- **เรียนมาก่อน:** [บทเรียน 1.2 — โมดูล edge_ai: ถามทะเบียนโมเดล เลือก แล้วอ่านคำตอบ](../l02-edge-ai-module/README.md)

## แนวคิด

โปรแกรม MicroPython บน BENTO เกือบทุกตัวเดิน **สี่จังหวะ**: import → สร้าง widget ครั้งเดียว → ลูปที่อ่านค่าแล้วอัปเดตจอ →
`ui.poll` รับปุ่มและการแตะจอ แล้ววนกลับ การสร้าง widget นอกลูปแล้วในลูปแค่เปลี่ยนค่าทำให้จอไม่กระพริบและไม่กินหน่วยความจำ
ไฟล์ `s01_first_inference.py` อ่านได้เป็นประโยคเดียว: ถามว่ามีโมเดลอะไร → เลือกหนึ่งตัว → วนอ่านผล → เอาคลาสที่ชนะขึ้นจอ → หยุดตอนออก

ช่องเติมทั้งสี่คือสี่คำสั่งหลักพอดี: ปุ่ม Load เรียก `edge_ai.select(sel)` ภายใน `try` และขึ้น RUNNING **หลัง** select สำเร็จเท่านั้น
ในลูปอ่าน `r = edge_ai.result()` แล้ววาดเฉพาะเมื่อ `r['seq']` เปลี่ยน ด้วย `verdict.text(r['label'] or '-')` และแถบของทุกคลาสจาก `r['scores']`
(คลาสที่ `i == top` ระบายเขียว) ปุ่ม Stop เรียก `edge_ai.stop()` ส่วนบล็อก `finally` ที่ให้ไว้แล้วหยุดเครื่องยนต์ทุกครั้งที่ออก
ไม่ว่าจะออกด้วยปุ่ม back หรือ error นี่คือนิสัยงานฝังตัว: ทิ้งเครื่องไว้ในสถานะที่รู้แน่เสมอ

ความสำเร็จของบทเรียนนี้ไม่ใช่แค่ "เห็นตัวหนังสือขยับ" แต่ต้องบอกได้ว่า `conf` 92% หมายความว่าอะไร และทำไมบางท่าโมเดลถึงยังไม่ชัวร์
ท่าที่ก้ำกึ่งระหว่างสองคลาส หรือเสียงที่คล้ายหลายคลาส ทำให้คะแนนกระจาย ไม่มีคลาสไหนชนะขาด

## ตัวอย่างสมบูรณ์

ใช้บันไดช่วยเหลือตามลำดับ: คำใบ้ `# เติม:` ในไฟล์ฝึก → ตารางช่องเติมในสไลด์ → เฉลย → ฉบับเต็ม
`s01_first_inference_full.py` เป็นฉบับขัดเรียบร้อยที่เพิ่ม latency และใช้ `CONF_FLOOR` แยกสี "มั่นใจ" กับ "ยังไม่ชัวร์"
เปิดดูหลังเติมไฟล์ฝึกผ่านแล้ว แล้วลองหาว่ามันต่างจากไฟล์ของคุณตรงไหน

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/s01_first_inference_full.py](examples/s01_first_inference_full.py) | เมนู Edge AI 6 โมเดล (ฉบับเต็ม) |

## ฝึกเติม

ในไฟล์มี `pass` สี่จุดตรงคอมเมนต์ `# เติม:` เติมตามลำดับนี้ แล้วรันทดสอบทุกครั้งที่เติมเสร็จหนึ่งจุด
1) ปุ่ม Load → `edge_ai.select(sel)` 2) ในลูป → `r = edge_ai.result()` 3) มีผลใหม่ → `verdict.text(r['label'] or '-')`
4) ปุ่ม Stop → `edge_ai.stop()` ถ้าลืมจุดที่ 1 จะขึ้น RUNNING แต่ไม่มีผล ถ้าลืมจุดที่ 3 แถบขยับแต่ตัวอักษรใหญ่ไม่เปลี่ยน
ถ้ายังไม่ขึ้น ให้กลับไปเช็กการเยื้องบรรทัดกับชื่อคำสั่งก่อน

| ไฟล์ฝึก | เรื่อง |
|---|---|
| [practice/s01_first_inference.py](practice/s01_first_inference.py) | รันโมเดล Edge AI ตัวแรกของเรา (ฉบับฝึกเติมโค้ด) |

## เฉลย

เปิดเฉลยหลังจากลองเองแล้วอย่างน้อยหนึ่งรอบ และอ่าน [วิธีใช้เฉลย](../../README.md#วิธีใช้เฉลย) ก่อน

| เฉลย | คู่กับ |
|---|---|
| [solution/s01_first_inference.py](solution/s01_first_inference.py) | [practice/s01_first_inference.py](practice/s01_first_inference.py) |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. เรียงสี่จังหวะของโปรแกรม MicroPython บน BENTO *(เรียงลำดับ · เป้าหมายข้อ 1)*
   - ก) ลูป: อ่านผลแล้วอัปเดตจอ
   - ข) import: edge_ai, ui, lcd, time
   - ค) ui.poll: รับปุ่มและการแตะจอ
   - ง) สร้างครั้งเดียว: อ่าน models() และสร้าง widget

   <details><summary>เฉลย</summary>

   **ข → ง → ก → ค** — import → สร้างครั้งเดียว → ลูป → ui.poll แล้ววนกลับ widget สร้างนอกลูป ในลูปแค่เปลี่ยนค่า จอจึงไม่กระพริบ

   </details>

2. เติมไฟล์ฝึกแล้ว กด Load สถานะขึ้น RUNNING แต่ไม่มีผลอนุมานเลย ลืมเติมจุดใดมากที่สุด *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) จุดที่ 1: edge_ai.select(sel) ในปุ่ม Load
   - ข) จุดที่ 3: verdict.text(...)
   - ค) จุดที่ 4: edge_ai.stop()
   - ง) บรรทัด import lcd

   <details><summary>เฉลย</summary>

   **ก** — ถ้าไม่เรียก select() โมเดลไม่ถูกสั่งให้รันเลย แต่โค้ดยังขึ้นข้อความ RUNNING ตามบรรทัดถัดไป ตารางช่องเติมในสไลด์บอกอาการนี้ไว้ตรง ๆ

   </details>

3. แถบความมั่นใจขยับทุกคลาส แต่ตัวอักษรใหญ่ของคลาสที่ชนะไม่เปลี่ยนเลย ช่องใดยังไม่ได้เติม *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) r = edge_ai.result()
   - ข) verdict.text(r['label'] or '-')
   - ค) edge_ai.stop()
   - ง) edge_ai.select(sel)

   <details><summary>เฉลย</summary>

   **ข** — แถบมาจาก r['scores'] ที่ให้ไว้แล้ว แสดงว่า result() ทำงาน ส่วนตัวอักษรใหญ่ต้องเติม verdict.text เอง

   </details>

4. ข้อใดบอกเหตุผลของการเช็ก r['seq'] และบล็อก finally ได้ถูกต้อง (เลือกทุกข้อที่ถูก) *(เลือกได้หลายข้อ · เป้าหมายข้อ 3)*
   - ก) เช็ก seq เพื่อวาดจอเฉพาะเมื่อมีผลใหม่ ไม่วาดซ้ำทุกรอบ
   - ข) finally ทำให้ออกยังไงก็เรียก edge_ai.stop() เครื่องยนต์ไม่รันค้าง
   - ค) seq คือความมั่นใจของโมเดลเป็นเปอร์เซ็นต์
   - ง) finally ทำให้โปรแกรมไม่มีวันเกิด error

   <details><summary>เฉลย</summary>

   **ก, ข** — seq เพิ่มขึ้นทุกครั้งที่มีผลใหม่ จึงบอกได้ว่าควรวาดไหม ส่วน finally ไม่ได้กัน error แต่รับประกันว่าตอนออกจะหยุดเครื่องยนต์เสมอ

   </details>

5. ถ้าทำท่าที่ก้ำกึ่งระหว่าง circle กับ shaking สิ่งที่มักเห็นบนจอคืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) คลาสใดคลาสหนึ่งชนะขาดที่ 100%
   - ข) คะแนนกระจายระหว่างสองคลาส conf ของผู้ชนะต่ำ อาจต่ำกว่า 50%
   - ค) โมเดลหยุดทำงาน
   - ง) latency_ms กลายเป็นศูนย์

   <details><summary>เฉลย</summary>

   **ข** — เมื่อข้อมูลคล้ายหลายคลาส softmax จะแบ่งคะแนนไปหลายคลาส ผู้ชนะจึงชนะแบบเฉียด นี่คือเหตุผลที่ต้องมี CONF_FLOOR

   </details>

## แล็บ

**MVP ของชุดบทเรียน 1.1–1.3:** รันเมนู `edge_ai` แล้วอ่านผลสดออก ทั้งคลาสที่ชนะ (`label`) และความมั่นใจ (`conf`) เปลี่ยนตามท่าทางหรือเสียงจริง

- [ ] เติมไฟล์ฝึกครบสี่ช่อง รันได้บน Emulator หรือบอร์ด
- [ ] สลับอย่างน้อยสามโมเดล แล้วจดลงบันทึกการเรียนว่าแต่ละตัวต้องทำอะไรถึงจะได้คลาสที่ชนะ
- [ ] หาท่าหรือเสียงที่ทำให้ conf ต่ำกว่า 50% และอธิบายว่าทำไม
- [ ] อธิบายได้ว่าโค้ดเรียก models, select, result และ stop ตรงไหน ทำอะไร

## ไปต่อ

ชุดบทเรียนถัดไป (บทเรียน 1.4–1.5) เราจะแกะแอปเซนเซอร์ทีละส่วน จับโครงสี่จังหวะให้ขาด แล้ว remix เป็นของเราเอง

บทเรียนถัดไป: [บทเรียน 1.4 — แกะแอปเซนเซอร์: โครงร่วมสี่จังหวะของทุกโปรแกรม](../l04-sensor-app-anatomy/README.md)

## สะท้อนคิด

- ถ้าลบการเช็ก `seq` ออก จอจะทำงานต่างไปอย่างไร และใครเป็นคนจ่ายราคานั้น
- โมเดลตัวไหนที่คุณทำให้ชนะได้ยากที่สุด คุณคิดว่าเป็นเพราะโมเดลหรือเพราะวิธีที่เราป้อนข้อมูล
