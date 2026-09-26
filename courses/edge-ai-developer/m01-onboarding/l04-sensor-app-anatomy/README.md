---
id: edgeai-dev.m01.l04
lang: th
title: {th: 'แกะแอปเซนเซอร์: โครงร่วมสี่จังหวะของทุกโปรแกรม', en: 'Taking a sensor app apart: the four-beat skeleton of every program'}
summary: {th: 'แกะแอปเซนเซอร์สามตัวที่ทำงานได้จริงจนเห็นโครงร่วมสี่จังหวะ import → สร้าง widget ครั้งเดียว → ลูปอ่าน คำนวณ วาด → ui.poll กับปุ่ม back แล้วรู้จัก sensors.bmi270.motion, sensors.radar และ dsp.tilt', en: 'Take three working sensor apps apart until the shared four-beat skeleton shows (import, create widgets once, a read-compute-draw loop, ui.poll with a back button), and meet sensors.bmi270.motion, sensors.radar and dsp.tilt.'}
level: L3
time_min: {concept: 35, practise: 20, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m01.l03]
objectives:
  - {th: 'ระบุได้ว่าแต่ละบรรทัดของ 01_imu_6axis.py, 02_imu_tilt_fusion.py และ 04_radar_presence.py อยู่ในจังหวะใดของโครงร่วมสี่จังหวะ และบอกความต่างของทั้งสามแอปในช่อง "อ่าน คำนวณ วาด"', en: 'Place each line of 01_imu_6axis.py, 02_imu_tilt_fusion.py and 04_radar_presence.py in one of the four beats, and state how the three apps differ in the read, compute and draw slots.'}
  - {th: อธิบายได้ว่าทำไมต้องสร้าง widget ก่อนลูป และวาดจอเฉพาะเมื่อค่าเปลี่ยน โดยบอกผลเสียที่เกิดถ้าทำตรงข้ามได้อย่างน้อยสองข้อ, en: 'Explain why widgets are created before the loop and the screen is redrawn only when a value changes, naming at least two harms of doing the opposite.'}
  - {th: อ่านค่าจาก sensors.bmi270.motion() และ sensors.radar() บอกหน่วยของ accel (m/s²) กับ gyro (dps) คำนวณขนาดเวกเตอร์ความเร่ง |a| และใช้ dsp.tilt แปลงเป็นมุม roll กับ pitch ได้, en: 'Read sensors.bmi270.motion() and sensors.radar(), state the accel (m/s²) and gyro (dps) units, compute the acceleration magnitude |a|, and turn accel into roll and pitch with dsp.tilt.'}
develops: [{skill: lang.micropython, to: 2}, {skill: sys.sensors-actuators, to: 2}, {skill: gui.embedded, to: 2}, {skill: hw.math, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 1.4 — แกะแอปเซนเซอร์: โครงร่วมสี่จังหวะของทุกโปรแกรม

> โมดูล 1 — เริ่มต้น: รันของจริงแล้วแกะดูข้างใน · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

แกะแอปเซนเซอร์สามตัวที่ทำงานได้จริงจนเห็นโครงร่วมสี่จังหวะ import → สร้าง widget ครั้งเดียว → ลูปอ่าน คำนวณ วาด → ui.poll กับปุ่ม back แล้วรู้จัก sensors.bmi270.motion, sensors.radar และ dsp.tilt

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. ระบุได้ว่าแต่ละบรรทัดของ 01_imu_6axis.py, 02_imu_tilt_fusion.py และ 04_radar_presence.py อยู่ในจังหวะใดของโครงร่วมสี่จังหวะ และบอกความต่างของทั้งสามแอปในช่อง "อ่าน คำนวณ วาด"
2. อธิบายได้ว่าทำไมต้องสร้าง widget ก่อนลูป และวาดจอเฉพาะเมื่อค่าเปลี่ยน โดยบอกผลเสียที่เกิดถ้าทำตรงข้ามได้อย่างน้อยสองข้อ
3. อ่านค่าจาก sensors.bmi270.motion() และ sensors.radar() บอกหน่วยของ accel (m/s²) กับ gyro (dps) คำนวณขนาดเวกเตอร์ความเร่ง |a| และใช้ dsp.tilt แปลงเป็นมุม roll กับ pitch ได้

## ก่อนเริ่ม

ผ่านชุดบทเรียน 1.1–1.3 มาแล้ว บทเรียนนี้ต่อยอดโครงโปรแกรมที่เห็นผ่าน ๆ ในบทเรียน 1.3
เปิดตัวอย่าง `01_imu_6axis.py` และ `04_radar_presence.py` ไว้ใน BENTO IDE

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — เรดาร์ของจริงมีบน TESAIoT Dev Kit ส่วนบน Emulator ค่า presence ของเรดาร์จำลองด้วยปุ่ม Shake
- **เรียนมาก่อน:** [บทเรียน 1.3 — ลงมือทำ: เมนูโมเดลตัวแรกของเรา](../l03-first-inference-lab/README.md)

## ดูของจริงก่อน

รันของจริงก่อนแกะเสมอ: รัน `01_imu_6axis.py` แล้วขยับหรือเขย่าบอร์ด ตัวเลขหกแกนและแถบ |a| วิ่งตาม
จากนั้นรัน `04_radar_presence.py` แล้วนั่งนิ่งหน้าบอร์ดเทียบกับออกนอกระยะ ป้ายจะเปลี่ยนจาก CLEAR เป็น PRESENCE

## แนวคิด

สามแอป `01` (ตัวเลขหกแกน) `02` (เกจมุมเอียง) และ `04` (ป้ายมีคนหรือไม่มีคน) ใช้เซนเซอร์และจอคนละแบบ แต่เดินตาม **สี่จังหวะเดียวกัน**:
(1) import โมดูลแล้วเรียก `ui.screen()` ทันที (2) สร้าง widget ทุกตัวก่อนลูปแล้วเก็บตัวแปรของตัวที่ต้องแก้ค่า
(3) ลูปที่ อ่าน → คำนวณ → วาด แล้วพัก `time.sleep_ms(100)` (4) `ui.poll()` ที่ไม่บล็อก ถ้าเจอ handle ของปุ่ม back ก็
`raise KeyboardInterrupt` เพื่อออกไปเก็บกวาดใน `except` จังหวะ 1–2 ทำครั้งเดียว จังหวะ 3–4 วนซ้ำจนกดออก
พอเห็นโครงนี้ การอ่านโค้ดใหม่จะเร็วขึ้นมาก เพราะรู้ว่าจะหาอะไรตรงไหน

กฎที่พลาดบ่อยคือ **สิ่งที่ "เป็น" สร้างก่อนลูป สิ่งที่ "เปลี่ยน" ทำในลูป** ถ้าสร้าง widget ในลูป จอจะกระพริบและ widget กองสะสม
จนหน่วยความจำหมด อีกนิสัยหนึ่งจาก `04` คือ **วาดเฉพาะตอนค่าเปลี่ยน** โดยเก็บค่าที่วาดล่าสุดไว้เทียบ (`last`, `was`, `last_seq`)
จอจึงนิ่ง และช่องสื่อสารข้ามคอร์ไม่แน่นโดยไม่จำเป็น deadzone ช่วยอีกชั้นให้มุมที่สั่นเล็ก ๆ ใกล้ศูนย์ไม่ทำให้เข็มกระตุก

`sensors.bmi270.motion()` คืน `(ax, ay, az, gx, gy, gz)` ในครั้งเดียว ค่าจึงเป็นช่วงเวลาเดียวกันทุกแกน accel มีหน่วย m/s²
(วางราบ `az` ≈ 9.8) gyro มีหน่วยองศาต่อวินาที ขนาดเวกเตอร์ $|a| = \sqrt{a_x^2 + a_y^2 + a_z^2}$ ยุบสามแกนเป็นค่าเดียว
วางนิ่งได้ราว 9.8 เขย่าแล้วพุ่งขึ้น `sensors.radar()` คืน dict ที่มี `presence` กับ `energy` ส่วน `dsp.tilt(ax, ay, az)`
คำนวณ `(roll, pitch)` เป็นองศาในภาษา C ให้ เพราะงานคณิตหนัก ๆ ควรยกให้ C ทำ แล้ว MicroPython คุมตรรกะกับจอ

## ตัวอย่างสมบูรณ์

ทำตาม PRIMM: ทาย (Predict) ว่าแต่ละแอปแสดงอะไรก่อนรัน → รัน (Run) → แกะ (Investigate) ด้วยตารางเทียบสามแอปในสไลด์
`02_imu_tilt_fusion.py` คือแอปเกจมุมเอียงที่ใช้ `dsp.tilt` เป็นต้นแบบของ Tilt Monitor ในบทเรียน 1.5

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/01_imu_6axis.py](examples/01_imu_6axis.py) | IMU BMI270: dashboard 6 แกนบนจอ |
| [examples/04_radar_presence.py](examples/04_radar_presence.py) | Radar: ป้ายสถานะใหญ่เปลี่ยนสีเมื่อพบคน (event-driven) |
| [examples/02_imu_tilt_fusion.py](examples/02_imu_tilt_fusion.py) | มุมเอียง: เกจ Arc คู่ (pitch / roll) + ตัวเลข Seg7 |

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นหรือใน `shared/` ด้วย:

- [m01-onboarding/l05-sensor-remix-lab/practice/s02_anatomy_sensor.py](../l05-sensor-remix-lab/practice/s02_anatomy_sensor.py) — แกะโครงแอปเซนเซอร์แล้ว remix เอง (ฉบับฝึกเติมโค้ด)

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. ส่วนใดของสามแอป 01 02 และ 04 ที่เหมือนกันทุกบรรทัดจน copy ข้ามแอปได้เลย *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) ช่องอ่านเซนเซอร์
   - ข) ช่องคำนวณ
   - ค) ลูป ui.poll กับปุ่ม back ที่ raise KeyboardInterrupt
   - ง) ชนิดของ widget ที่สร้าง

   <details><summary>เฉลย</summary>

   **ค** — ตารางเทียบสามแอปแสดงว่าต่างกันแค่ "อ่านอะไร คำนวณอะไร วาดด้วยอะไร" ส่วน poll กับปุ่ม back เหมือนกันเป๊ะ

   </details>

2. ถ้าเผลอสร้าง ui.Seg7 ใหม่ทุกรอบในลูป จะเกิดอะไร (เลือกทุกข้อที่ถูก) *(เลือกได้หลายข้อ · เป้าหมายข้อ 2)*
   - ก) จอกระพริบเพราะวาดทับซ้ำทุกเฟรม
   - ข) widget เก่ากองสะสมจนหน่วยความจำหมดแล้วค้าง
   - ค) ลูปเร็วขึ้นเพราะไม่ต้องเก็บตัวแปร
   - ง) ค่าจากเซนเซอร์แม่นขึ้น

   <details><summary>เฉลย</summary>

   **ก, ข** — สร้าง widget ครั้งเดียวก่อนลูป แล้วในลูปแค่แก้ค่า เช่น seg.text("42") จอจึงนิ่งและหน่วยความจำคงที่

   </details>

3. ใน 04_radar_presence.py บรรทัด if now != was ทำหน้าที่อะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) หยุดลูปเมื่อไม่มีคน
   - ข) วาดจอเฉพาะตอนสถานะเปลี่ยน ไม่แตะจอเมื่อค่าเดิม
   - ค) เปิดเรดาร์ใหม่ทุกรอบ
   - ง) รอจนกว่าจะมีคนเข้ามา

   <details><summary>เฉลย</summary>

   **ข** — นี่คือการวาดแบบ event-driven เก็บสถานะล่าสุดไว้ใน was แล้ววาดใหม่เฉพาะตอนที่ต่างไปจากเดิม

   </details>

4. วางบอร์ดนิ่งราบบนโต๊ะ ค่าจาก sensors.bmi270.motion() ข้อใดสมเหตุสมผลที่สุด *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) ax ≈ 9.8, ay ≈ 0, az ≈ 0
   - ข) ax ≈ 0, ay ≈ 0, az ≈ 9.8 และ gyro ทั้งสามแกนใกล้ 0
   - ค) ทุกแกนเป็น 0 เพราะบอร์ดไม่ขยับ
   - ง) az ≈ 1.0 เพราะหน่วยเป็น g

   <details><summary>เฉลย</summary>

   **ข** — accel มีหน่วย m/s² และวัดแรงโน้มถ่วงด้วย แกนที่ตั้งฉากพื้นจึงได้ราว 9.8 ส่วน gyro วัดการหมุน วางนิ่งจึงใกล้ 0

   </details>

5. ถ้า ax = 0, ay = 6, az = 8 m/s² ค่า |a| เท่าไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) 14
   - ข) 10
   - ค) 7
   - ง) 100

   <details><summary>เฉลย</summary>

   **ข** — |a| = √(0² + 6² + 8²) = √100 = 10 m/s² เป็นพีทาโกรัสในสามมิติ ค่าใกล้ 9.8 แปลว่าบอร์ดแทบไม่ได้เร่ง มีแค่แรงโน้มถ่วงที่ถูกเอียงไปสองแกน

   </details>

## แล็บ

- [ ] รัน `01` และ `04` (ถ้ามีบอร์ด) แล้วจดว่าอะไรบนจอเปลี่ยนเมื่อคุณขยับหรือเคลื่อนเข้าใกล้
- [ ] เขียนตารางสี่จังหวะของทั้งสามแอปลงบันทึกการเรียน ช่องไหนเหมือนกันทุกบรรทัด ช่องไหนต่างกัน
- [ ] วางบอร์ดราบแล้วอ่าน |a| ให้ได้ใกล้ 9.8 จากนั้นเอียงแล้วสังเกตว่าแรงโน้มถ่วงกระจายไปที่ ax และ ay อย่างไร

## ไปต่อ

บทเรียน 1.5 เราจะ remix สามแอปนี้เป็น Tilt Monitor ของเราเองด้วยการเติมสี่ช่องในไฟล์ฝึก

บทเรียนถัดไป: [บทเรียน 1.5 — ลงมือทำ: remix เป็น Tilt Monitor ของเรา](../l05-sensor-remix-lab/README.md)

## สะท้อนคิด

- ถ้าต้องเปลี่ยนแอป `01` ให้อ่านเรดาร์แทน IMU คุณต้องแก้จังหวะไหนบ้าง และจังหวะไหนไม่ต้องแตะเลย
- ทำไมการอ่านหกแกนในครั้งเดียวถึงสำคัญกับการคำนวณมุม
