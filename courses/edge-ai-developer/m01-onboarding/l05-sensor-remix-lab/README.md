---
id: edgeai-dev.m01.l05
lang: th
title: {th: 'ลงมือทำ: remix เป็น Tilt Monitor ของเรา', en: 'Hands-on: remix it into your own Tilt Monitor'}
summary: {th: remix สามแอปเซนเซอร์เป็น Tilt Monitor ของเราเอง ด้วยการเติมสี่ช่องที่เป็นหัวใจของโครงร่วม แล้วลองสลับเซนเซอร์ เปลี่ยนการแสดงผล และจงใจทำให้พังแล้วซ่อม จนอธิบายได้ทุกบรรทัดว่าอยู่จังหวะไหน, en: 'Remix the three sensor apps into your own Tilt Monitor by filling the four blanks at the heart of the skeleton, then swap the sensor, change the display and break-and-fix until you can place every line in its beat.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m01.l04]
objectives:
  - {th: 'เติมสี่ช่องใน practice/s02_anatomy_sensor.py (motion, dsp.tilt, seg.text, raise KeyboardInterrupt) จนเอียงบอร์ดแล้วเกจสองแกนขยับ มุมเด่นขึ้น Seg7 ป้ายเปลี่ยนเป็น TILTED เมื่อเอียงถึง 20 องศา และกดปุ่มออกแล้วโปรแกรมจบ', en: 'Fill the four blanks in practice/s02_anatomy_sensor.py (motion, dsp.tilt, seg.text, raise KeyboardInterrupt) until tilting moves both gauges, the dominant angle shows on the Seg7, the panel turns TILTED at 20 degrees, and the back button ends the program.'}
  - {th: วินิจฉัยอาการเข็มไม่ขยับ มุมเป็นศูนย์ตลอด ตัวเลขใหญ่ไม่เปลี่ยน และกดออกแล้วไม่ออก ว่าเกิดจากช่องใดที่ยังไม่ได้เติม, en: 'Diagnose a still needle, an angle stuck at zero, a big number that never changes and a back button that does nothing, each to the blank that is still empty.'}
  - {th: ทำ remix ที่ต่างจากต้นฉบับอย่างน้อยหนึ่งอย่าง (สลับเป็น sensors.radar() หรือเปลี่ยนการแสดงผล) แล้วชี้ได้ว่าบรรทัดใดอยู่จังหวะใดและแต่ละคำสั่ง sensors.* กับ dsp.tilt ทำอะไร, en: Make at least one remix that differs from the originals (switch to sensors.radar() or change the display) and point out which line belongs to which beat and what each sensors.* and dsp.tilt call does.}
develops: [{skill: lang.micropython, to: 2}, {skill: sys.sensors-actuators, to: 2}, {skill: gui.embedded, to: 2}, {skill: soft.problem-solving, to: 2}]
assesses: [{skill: lang.micropython, level: 2, evidence: practice/s02_anatomy_sensor.py}, {skill: sys.sensors-actuators, level: 2, evidence: practice/s02_anatomy_sensor.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 1.5 — ลงมือทำ: remix เป็น Tilt Monitor ของเรา

> โมดูล 1 — เริ่มต้น: รันของจริงแล้วแกะดูข้างใน · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

remix สามแอปเซนเซอร์เป็น Tilt Monitor ของเราเอง ด้วยการเติมสี่ช่องที่เป็นหัวใจของโครงร่วม แล้วลองสลับเซนเซอร์ เปลี่ยนการแสดงผล และจงใจทำให้พังแล้วซ่อม จนอธิบายได้ทุกบรรทัดว่าอยู่จังหวะไหน

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เติมสี่ช่องใน practice/s02_anatomy_sensor.py (motion, dsp.tilt, seg.text, raise KeyboardInterrupt) จนเอียงบอร์ดแล้วเกจสองแกนขยับ มุมเด่นขึ้น Seg7 ป้ายเปลี่ยนเป็น TILTED เมื่อเอียงถึง 20 องศา และกดปุ่มออกแล้วโปรแกรมจบ
2. วินิจฉัยอาการเข็มไม่ขยับ มุมเป็นศูนย์ตลอด ตัวเลขใหญ่ไม่เปลี่ยน และกดออกแล้วไม่ออก ว่าเกิดจากช่องใดที่ยังไม่ได้เติม
3. ทำ remix ที่ต่างจากต้นฉบับอย่างน้อยหนึ่งอย่าง (สลับเป็น sensors.radar() หรือเปลี่ยนการแสดงผล) แล้วชี้ได้ว่าบรรทัดใดอยู่จังหวะใดและแต่ละคำสั่ง sensors.* กับ dsp.tilt ทำอะไร

## ก่อนเริ่ม

ผ่านบทเรียน 1.4 มาแล้ว จำตารางเทียบสามแอปได้ว่าช่อง "อ่าน คำนวณ วาด" ของแต่ละแอปคืออะไร
เปิดไฟล์ฝึกใน BENTO IDE และเตรียมบันทึกการเรียนไว้จดสิ่งที่แก้ใน remix พร้อมเหตุผล

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/)
- **เรียนมาก่อน:** [บทเรียน 1.4 — แกะแอปเซนเซอร์: โครงร่วมสี่จังหวะของทุกโปรแกรม](../l04-sensor-app-anatomy/README.md)

## แนวคิด

โจทย์ของเราคือ **Tilt Monitor**: หยิบช่อง "อ่าน" จาก `01` (`bmi270.motion()`) ช่อง "คำนวณ" จาก `02` (`dsp.tilt`) และลูกเล่น
"วาดเฉพาะตอนเปลี่ยน" จาก `04` มาผสมเป็นแอปใหม่ เกจ Arc คู่โชว์ pitch กับ roll, Seg7 โชว์มุมที่เอียงมากสุด และป้าย LEVEL/TILTED
เปลี่ยนสีเมื่อเอียงเกิน `TILT_LIMIT` = 20 องศา ค่าคงที่ `DEAD` กับ `TILT_LIMIT` บนหัวไฟล์คือปุ่มปรับพฤติกรรมที่ remix ได้ง่ายที่สุด

ไฟล์ฝึกให้จังหวะ 1–2 (import และสร้าง widget) มาครบแล้ว ช่องว่างสี่จุดอยู่ในจังหวะ 3–4 พอดี: อ่าน IMU, แปลงเป็นมุม, เอามุมเด่นขึ้น Seg7
และ `raise KeyboardInterrupt` เมื่อกดปุ่มออก สังเกตการวาดแบบ event-driven ที่ซ้อนสองชั้น ชั้นนอกเช็กว่ามุมเปลี่ยน ชั้นในเช็กว่าสถานะ
เอียงกับราบเปลี่ยน ทั้งคู่เพื่อไม่แตะจอเกินจำเป็น

remix คือหัวใจของขั้น Modify ใน PRIMM: **สลับเซนเซอร์** (อ่าน `sensors.radar()` แล้วโชว์ presence หรือ energy แทนมุม โครงไม่ต้องแตะ)
**เปลี่ยนการแสดงผล** (Seg7 เป็น Bar, เปลี่ยน `TILT_LIMIT` เป็น 10) และ **พังแล้วซ่อม** (ย้าย `ui.Arc(...)` เข้าไปในลูป ดูจอกระพริบ
แล้วย้ายกลับ) remix ที่รันได้แต่เจ้าของอธิบายไม่ได้ยังไม่ถือว่าผ่าน เพราะเป้าหมายคือ "อ่านออก" ไม่ใช่แค่ "ลอกให้รัน"

## ตัวอย่างสมบูรณ์

`s02_anatomy_sensor_full.py` คือฉบับขัดเรียบร้อยที่เพิ่มแถบ |a| จำมุมสูงสุดที่เคยเจอ (peak) และปุ่ม Reset
เปิดดูหลังจากไฟล์ฝึกของคุณทำงานแล้ว เพื่อเทียบว่าเขาต่อยอดโครงเดียวกันอย่างไร

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/s02_anatomy_sensor_full.py](examples/s02_anatomy_sensor_full.py) | Tilt Monitor remix (ฉบับเต็ม) |

## ฝึกเติม

ไฟล์มี `pass` สี่จุด (บรรทัด 62, 67, 76 และ 96) ตรงคอมเมนต์ `# เติม:`
1) `ax, ay, az, gx, gy, gz = sensors.bmi270.motion()` 2) `roll, pitch = dsp.tilt(ax, ay, az)`
3) `seg.text("%d" % ang)` 4) `raise KeyboardInterrupt` เอียงบอร์ดช้า ๆ แล้วดูว่าเข็ม ตัวเลข และป้ายตอบสนองครบหรือยัง

| ไฟล์ฝึก | เรื่อง |
|---|---|
| [practice/s02_anatomy_sensor.py](practice/s02_anatomy_sensor.py) | แกะโครงแอปเซนเซอร์แล้ว remix เอง (ฉบับฝึกเติมโค้ด) |

## เฉลย

เปิดเฉลยหลังจากลองเองแล้วอย่างน้อยหนึ่งรอบ และอ่าน [วิธีใช้เฉลย](../../README.md#วิธีใช้เฉลย) ก่อน

| เฉลย | คู่กับ |
|---|---|
| [solution/s02_anatomy_sensor.py](solution/s02_anatomy_sensor.py) | [practice/s02_anatomy_sensor.py](practice/s02_anatomy_sensor.py) |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. ช่องเติมที่ 2 ของ Tilt Monitor คือคำสั่งใด *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
   - ข) roll, pitch = dsp.tilt(ax, ay, az)
   - ค) seg.text("%d" % ang)
   - ง) raise KeyboardInterrupt

   <details><summary>เฉลย</summary>

   **ข** — ช่อง 1 อ่าน ช่อง 2 คำนวณมุมด้วย dsp.tilt ช่อง 3 วาดมุมเด่น และช่อง 4 ออกจากลูปเมื่อกดปุ่ม back ตรงกับโครงอ่าน คำนวณ วาด ฟังปุ่ม

   </details>

2. รันแล้วเข็มไม่ขยับเลยและมุมเป็น 0 ตลอดแม้เอียงบอร์ด สาเหตุที่น่าจะเป็นที่สุดคืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) ยังไม่ได้เติมช่อง 1 ax ay az จึงค้างเป็น 0 ทำให้ dsp.tilt ได้มุม 0 เสมอ
   - ข) ลืมเติม raise KeyboardInterrupt
   - ค) TILT_LIMIT ตั้งไว้สูงเกินไป
   - ง) จอเสีย

   <details><summary>เฉลย</summary>

   **ก** — บรรทัดสำรอง ax = ay = az = ... = 0 ทำให้โปรแกรมรันได้แต่ค่าเป็นศูนย์ เป็นเบาะแสตอน debug ว่าช่องอ่านเซนเซอร์ยังว่าง

   </details>

3. กดปุ่ม "< ออก" แล้วโปรแกรมยังวนต่อไม่จบ ช่องใดยังว่าง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) ช่อง 1
   - ข) ช่อง 2
   - ค) ช่อง 3
   - ง) ช่อง 4 raise KeyboardInterrupt ใน ui.poll

   <details><summary>เฉลย</summary>

   **ง** — ถ้าไม่ raise ในลูป ui.poll โปรแกรมจะเห็นอีเวนต์ของปุ่มแต่ไม่ทำอะไร จึงวนต่อไปเรื่อย ๆ

   </details>

4. อยากให้แอปเดิมแสดงว่ามีคนอยู่หน้าบอร์ดแทนมุมเอียง ต้องแก้ส่วนใดเป็นหลัก *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) เขียนโครงใหม่ทั้งไฟล์
   - ข) เปลี่ยนช่องอ่านเป็น sensors.radar() และช่องคำนวณเป็น bool(r["presence"]) ส่วน poll และปุ่ม back คงเดิม
   - ค) เปลี่ยนแค่ TILT_LIMIT
   - ง) ลบ ui.poll ทิ้ง

   <details><summary>เฉลย</summary>

   **ข** — ตารางเทียบสามแอปคือแผนที่ remix สลับช่องอ่านกับคำนวณก็ได้แอปใหม่ โครงที่เหลือไม่ต้องแตะ

   </details>

## แล็บ

**MVP ของชุดบทเรียน 1.4–1.5:** remix ที่ต่างจากต้นฉบับจริง และอธิบายแต่ละส่วนได้ว่าอยู่จังหวะไหน

- [ ] ไฟล์ฝึกเติมครบสี่ช่อง รันบน Emulator หรือบอร์ดแล้วเข็ม มุมเด่น และป้ายสถานะทำงาน
- [ ] ทำ remix อย่างน้อยหนึ่งอย่างที่ต่างจาก `01/02/04` แล้วจดลงบันทึกการเรียนว่าแก้อะไร เพราะอะไร
- [ ] ลองพังแล้วซ่อม: ย้ายการสร้าง widget เข้าลูป สังเกตอาการ แล้วย้ายกลับ
- [ ] ชี้ได้ว่าบรรทัดไหนในไฟล์ของคุณอยู่จังหวะ import สร้างครั้งเดียว ลูป หรือ poll

## ไปต่อ

ชุดบทเรียนถัดไป (บทเรียน 1.6–1.7) เราจะแกะแอป Edge AI แบบเดียวกัน แล้ว remix ให้สลับโมเดลและสั่งการเมื่อเจอคลาสที่ต้องการ

บทเรียนถัดไป: [บทเรียน 1.6 — แกะแอป Edge AI: ทะเบียนโมเดล verdict และ action](../l06-edge-ai-app-anatomy/README.md)

## สะท้อนคิด

- remix ของคุณแก้แค่ช่องไหนของโครงสี่จังหวะ ช่องที่ไม่ต้องแตะบอกอะไรเกี่ยวกับการออกแบบโปรแกรมนี้
- ตอนย้าย widget เข้าลูป คุณเห็นอาการอะไร และถ้าปล่อยไว้นาน ๆ คิดว่าจะเกิดอะไรต่อ
