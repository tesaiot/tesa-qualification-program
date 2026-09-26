---
id: edgeai-dev.m03.l02
lang: th
title: {th: 'ลงมือทำ: เกจฟิสิกส์สี่ตัวบนจอ', en: 'Hands-on: four physics gauges on screen'}
summary: {th: 'เติมสี่สูตรแปลงใน s06_physics_viz.py (tilt, energy, altitude, dBFS) แล้วเลือกปริมาณใน dropdown ขยับ ยก หรือส่งเสียง จนเกจ Seg7 แถบ และกราฟขยับตามค่าที่เราคำนวณเอง', en: 'Fill the four conversion formulas in s06_physics_viz.py (tilt, energy, altitude, dBFS), then pick a quantity from the dropdown and move, lift or make noise until the Seg7, bar and chart follow the values you computed.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m03.l01]
objectives:
  - {th: 'เติมสี่สูตรใน practice/s06_physics_viz.py จนอย่างน้อยสามปริมาณ (Tilt, Energy, Altitude) แสดงค่าที่เปลี่ยนตามการเคลื่อนไหวจริงบน Emulator หรือบอร์ด', en: 'Fill the four formulas in practice/s06_physics_viz.py until at least three quantities (Tilt, Energy, Altitude) show values that follow real motion on the emulator or the board.'}
  - {th: ทดสอบสูตร energy ให้ได้ราว 0 ตอนวางนิ่งและเกิน 1 ตอนเขย่าแรง แล้วอธิบายได้ว่าทำไมต้องหาร 9.81 และลบ 1g, en: 'Test the energy formula to read about 0 at rest and above 1 when shaken hard, and explain why it divides by 9.81 and subtracts 1 g.'}
  - {th: อธิบายหน้าที่ของ placeholder ในไฟล์ฝึก การจับ p0 ก่อนลูป และการคืนไมโครโฟนด้วย pdm.deinit() ใน finally, en: 'Explain the role of the placeholders in the practice file, capturing p0 before the loop, and releasing the microphone with pdm.deinit() in finally.'}
develops: [{skill: sys.dsp, to: 2}, {skill: lang.micropython, to: 2}, {skill: gui.hmi, to: 2}]
assesses: [{skill: sys.dsp, level: 2, evidence: practice/s06_physics_viz.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 3.2 — ลงมือทำ: เกจฟิสิกส์สี่ตัวบนจอ

> โมดูล 3 — ประมวลผลด้วยคณิตศาสตร์และฟิสิกส์ · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เติมสี่สูตรแปลงใน s06_physics_viz.py (tilt, energy, altitude, dBFS) แล้วเลือกปริมาณใน dropdown ขยับ ยก หรือส่งเสียง จนเกจ Seg7 แถบ และกราฟขยับตามค่าที่เราคำนวณเอง

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เติมสี่สูตรใน practice/s06_physics_viz.py จนอย่างน้อยสามปริมาณ (Tilt, Energy, Altitude) แสดงค่าที่เปลี่ยนตามการเคลื่อนไหวจริงบน Emulator หรือบอร์ด
2. ทดสอบสูตร energy ให้ได้ราว 0 ตอนวางนิ่งและเกิน 1 ตอนเขย่าแรง แล้วอธิบายได้ว่าทำไมต้องหาร 9.81 และลบ 1g
3. อธิบายหน้าที่ของ placeholder ในไฟล์ฝึก การจับ p0 ก่อนลูป และการคืนไมโครโฟนด้วย pdm.deinit() ใน finally

## ก่อนเริ่ม

ผ่านบทเรียน 3.1 มาแล้ว เข้าใจสี่สูตรและเหตุผลของการหาร 9.81
เติมทีละสูตรแล้วทดสอบทีละปริมาณ จะจับบั๊กได้ง่ายกว่าเติมรวดเดียว

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — Tilt, Energy และ Altitude ครบบน Emulator ส่วน Sound บน Emulator เป็นเสียงสังเคราะห์ เสียงจริงต้องใช้บอร์ดที่ไมโครโฟน PDM ใช้ได้ (ดูข้อจำกัดของ TESAIoT Dev Kit ในบทเรียน 2.3)
- **เรียนมาก่อน:** [บทเรียน 3.1 — จากตัวเลขดิบสู่ปริมาณทางฟิสิกส์: มุมเอียง พลังงาน ความสูง และ dBFS](../l01-physics-quantities/README.md)

## แนวคิด

ทั้งไฟล์อ่านเป็นประโยคเดียว: เลือกปริมาณ → อ่านค่าดิบ → คำนวณเป็นปริมาณจริง → ส่งขึ้น Seg7, Bar และ Chart → วนทุก 120 ms
ส่วนบนสร้าง widget ครั้งเดียว ลองเปิดไมค์ใน `try` เพื่อตั้ง `has_mic` และจับ `p0` ก่อนลูป ทั้งหมดนี้ให้ไว้แล้ว งานของเราคือสูตรตรงกลาง
(จังหวะ derived) สี่จุด ไฟล์ฝึกวาง placeholder อย่าง `roll, pitch = 0.0, 0.0` หรือ `db = -96.0` ไว้ให้รันได้ตั้งแต่ยังไม่เติม
(โชว์ 0) พอเติมจริงค่าถึงจะขยับ เทคนิคเดียวกับ `r = None` ในบทเรียน 1.3

สี่สูตรคือ (1) `roll, pitch = dsp.tilt(ax, ay, az)` (2) `mag = math.sqrt(ax*ax + ay*ay + az*az) / 9.81` แล้ว `energy = abs(mag - 1.0)`
(3) `alt = dsp.altitude(p, p0)` และ (4) `db = 20 * math.log10(rms / 32768.0)` ภายใน `if rms > 0:` เพราะ log10(0) คำนวณไม่ได้
ระวังลำดับที่ `dsp.tilt` คืน (roll ก่อน pitch) และจำว่า `motion()` ให้หน่วย m/s² ถ้าลืมหาร 9.81 พลังงานจะค้างราว 8.8 แม้วางนิ่ง
ความดันไวต่อลมและแอร์ ค่าความสูงจึงแกว่งเล็กน้อยเป็นปกติ ซึ่งเราจะกรองให้นิ่งในโมดูล 4

เมื่อเติมครบ กราฟ `Chart` เก็บประวัติย้อนหลังให้ ลองเขย่าเป็นจังหวะแล้วดูรูปคลื่น จะเห็น "รูปร่างของการเคลื่อนไหว" ชัดกว่าตัวเลขนิ่ง ๆ
ความสำเร็จไม่ใช่แค่ตัวเลขขยับ แต่ต้องบอกได้ว่า energy 0.8 หมายความว่าอะไร และทำไม tilt ใช้ atan2 ได้โดยไม่ต้องรู้หน่วยของ accel

## ตัวอย่างสมบูรณ์

`s06_physics_viz_full.py` เพิ่มการจำค่าสูงสุดต่ำสุด (hi/lo hold) ป้าย STEADY/ACTIVE และปุ่ม Reset
รันก่อนเริ่มบทเรียนเพื่อดูปลายทาง แล้วกลับมาอ่านอีกครั้งหลังเติมไฟล์ฝึกผ่าน

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/s06_physics_viz_full.py](examples/s06_physics_viz_full.py) | Physics Lab: raw -> derived -> viz (ฉบับเต็ม) |

## ฝึกเติม

คอมเมนต์ `# เติม:` สี่จุดอยู่ที่บรรทัด 94, 103, 112 และ 125 (Tilt, Energy, Altitude, dBFS)
แทน placeholder ด้วยสูตรตามคำใบ้ แล้วกด Run (Emulator) หรือ Program to Device (บอร์ด)
ถ้าเกจค้างที่ 0 ให้ตรวจว่าเติมบรรทัดสูตรแล้วและไม่ได้เขียนทับด้วย placeholder อีกครั้ง

| ไฟล์ฝึก | เรื่อง |
|---|---|
| [practice/s06_physics_viz.py](practice/s06_physics_viz.py) | Physics Lab: raw -> derived -> viz (ฉบับฝึกเติมโค้ด) |

## เฉลย

เปิดเฉลยหลังจากลองเองแล้วอย่างน้อยหนึ่งรอบ และอ่าน [วิธีใช้เฉลย](../../README.md#วิธีใช้เฉลย) ก่อน

| เฉลย | คู่กับ |
|---|---|
| [solution/s06_physics_viz.py](solution/s06_physics_viz.py) | [practice/s06_physics_viz.py](practice/s06_physics_viz.py) |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. เติมสูตร Tilt แล้วแต่เกจมุมยังค้างที่ 0 ทุกครั้ง สาเหตุที่น่าจะเป็นคืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) ยังไม่ได้แทน pass หรือยังเหลือบรรทัด placeholder roll, pitch = 0.0, 0.0 อยู่หลังสูตร
   - ข) dsp.tilt ใช้ได้เฉพาะบนบอร์ด
   - ค) ต้องหาร 9.81 ก่อนเรียก dsp.tilt
   - ง) Chart รับค่าเกิน 100 ไม่ได้

   <details><summary>เฉลย</summary>

   **ก** — placeholder มีไว้ให้ไฟล์รันได้ตอนยังไม่เติม ถ้ามันยังทับค่าหลังสูตรอยู่ เกจจะโชว์ 0 ตลอด ส่วน dsp.tilt ไม่ต้องแปลงหน่วยก่อน

   </details>

2. วางบอร์ดนิ่งแล้ว Energy โชว์ 8.81 ตลอด ต้องแก้สูตรอย่างไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) เปลี่ยน abs เป็น max
   - ข) หารขนาดเวกเตอร์ด้วย 9.81 ให้เป็นหน่วย g ก่อนลบ 1.0
   - ค) ลบ 1.0 ออกจากสูตร
   - ง) ใช้ gx gy gz แทน ax ay az

   <details><summary>เฉลย</summary>

   **ข** — motion() ให้ m/s² ขนาดตอนนิ่งจึงราว 9.81 หาร 9.81 แล้วได้ราว 1g ลบ 1 จึงเหลือราว 0

   </details>

3. energy (หน่วย g) ถูกแปลงเป็นแถบด้วย clamp100(energy / 2.0 * 100) ถ้า energy = 0.5 แถบจะอยู่ที่เท่าไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) 5
   - ข) 25
   - ค) 50
   - ง) 100

   <details><summary>เฉลย</summary>

   **ข** — 0.5 / 2.0 × 100 = 25 ช่วง 0..2g ถูก map ลงแถบ 0..100 ส่วนค่าเกิน 2g จะถูก clamp ไว้ที่ 100

   </details>

4. ข้อใดถูกต้องเกี่ยวกับส่วนที่ให้ไว้แล้วในไฟล์ฝึก (เลือกทุกข้อที่ถูก) *(เลือกได้หลายข้อ · เป้าหมายข้อ 3)*
   - ก) p0 จับครั้งเดียวก่อนลูปเพราะเป็นจุดอ้างอิงที่ไม่เปลี่ยน
   - ข) pdm.deinit() อยู่ใน finally เพื่อคืนไมโครโฟนเสมอไม่ว่าจะออกด้วยวิธีใด
   - ค) placeholder ทำให้ไฟล์รันได้และโชว์ 0 ตั้งแต่ยังไม่เติม
   - ง) widget ถูกสร้างใหม่ในลูปทุก 120 ms

   <details><summary>เฉลย</summary>

   **ก, ข, ค** — widget สร้างครั้งเดียวก่อนลูปตามโครงร่วม ในลูปแค่เปลี่ยนค่า ส่วนอีกสามข้อคือการเตรียมของก่อนลูปและการเก็บกวาดที่ถูกต้อง

   </details>

## แล็บ

**MVP ของชุดบทเรียน 3.1–3.2:** สัญญาณดิบ → ปริมาณที่คำนวณได้ → แสดงเห็นบนจอ ครบวงอย่างน้อยหนึ่งปริมาณ

- [ ] เติมไฟล์ฝึกครบสี่สูตร รันได้บน Emulator หรือบอร์ด
- [ ] ทดสอบอย่างน้อยสามปริมาณ (Tilt → Energy → Altitude) จดลงบันทึกการเรียนว่าต้องทำอะไรถึงจะเห็นค่าเปลี่ยนชัด
- [ ] หาค่าอ้างอิงตอนนิ่งของ Energy แล้วลองลบ `- 1.0` ออกชั่วคราว ดูว่าค่าตอนนิ่งกลายเป็นเท่าไรและอธิบายว่าทำไม
- [ ] อธิบายได้ว่าสูตรที่เติมแปลงตัวเลขดิบเป็นปริมาณอะไร หน่วยอะไร

## ไปต่อ

ชุดบทเรียนถัดไป (บทเรียน 3.3–3.4) เราจะเอาปริมาณที่แปลงได้ไปตัดสินด้วยกฎ เช่น "สบาย" หรือ "ร้อน" จากอุณหภูมิกับความชื้น

บทเรียนถัดไป: [บทเรียน 3.3 — ค่าอนุพัทธ์และการจำแนกด้วยกฎ: dew point, heat index และบันไดกฎ](../l03-rules-before-ml/README.md)

## สะท้อนคิด

- ปริมาณไหนที่ Chart เล่าเรื่องได้ดีกว่าตัวเลข Seg7 และเพราะอะไร
- ถ้าต้องใช้ค่า energy ไปตัดสินว่า "มีคนหยิบบอร์ด" คุณจะตั้งเกณฑ์ที่เท่าไร และจะทดสอบเกณฑ์นั้นอย่างไร
