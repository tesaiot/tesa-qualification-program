---
id: edgeai-dev.m03.l01
lang: th
title: {th: 'จากตัวเลขดิบสู่ปริมาณทางฟิสิกส์: มุมเอียง พลังงาน ความสูง และ dBFS', en: 'From raw numbers to physical quantities: tilt, energy, altitude and dBFS'}
summary: {th: เข้าสู่ขั้น Processing ด้วยรูปแบบ raw → derived → viz แปลงตัวเลขดิบเป็นสี่ปริมาณที่คนเข้าใจ คือมุมเอียงด้วย atan2 พลังงานการเคลื่อนไหว ความสูงจากความดัน และระดับเสียงแบบ dBFS แล้วเลือก widget ให้เหมาะกับแต่ละปริมาณ, en: 'Enter the Processing stage with the raw → derived → viz pattern - turn raw numbers into four quantities people understand (tilt with atan2, motion energy, altitude from pressure, sound level in dBFS) and pick the right widget for each.'}
level: L3
time_min: {concept: 45, practise: 10, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m02.l04]
objectives:
  - {th: 'อธิบายรูปแบบ raw → derived → viz และบอกได้ว่าปริมาณใดใช้ฟังก์ชันสำเร็จของ dsp (tilt, altitude) และปริมาณใดต้องเขียนสูตรเอง (energy, dBFS)', en: 'Explain the raw → derived → viz pattern and say which quantities use a ready dsp function (tilt, altitude) and which need your own formula (energy, dBFS).'}
  - {th: คำนวณมุม roll และ pitch จากความเร่งสามแกนด้วย atan2 ได้ และอธิบายว่าทำไมหน่วยของ accelerometer หักล้างกันในสูตรอัตราส่วน, en: 'Compute roll and pitch from three-axis acceleration with atan2, and explain why the accelerometer''s unit cancels in the ratio formula.'}
  - {th: 'คำนวณพลังงานการเคลื่อนไหวจาก motion() ที่ให้หน่วย m/s² (หาร 9.81 เป็น g แล้วลบ 1g) และความสูงสัมพัทธ์ด้วย dsp.altitude(p, p0) ได้', en: 'Compute motion energy from motion() in m/s² (divide by 9.81 to get g, then subtract 1 g) and relative altitude with dsp.altitude(p, p0).'}
  - {th: 'เลือก widget (Seg7, Bar, Chart, Arc) ให้เข้ากับปริมาณ และอธิบายว่าทำไม dBFS ใช้สเกล log', en: 'Choose a widget (Seg7, Bar, Chart, Arc) to match each quantity, and explain why dBFS uses a log scale.'}
develops: [{skill: sys.dsp, to: 2}, {skill: hw.math, to: 2}, {skill: sys.sensors-actuators, to: 2}, {skill: gui.hmi, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 3.1 — จากตัวเลขดิบสู่ปริมาณทางฟิสิกส์: มุมเอียง พลังงาน ความสูง และ dBFS

> โมดูล 3 — ประมวลผลด้วยคณิตศาสตร์และฟิสิกส์ · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เข้าสู่ขั้น Processing ด้วยรูปแบบ raw → derived → viz แปลงตัวเลขดิบเป็นสี่ปริมาณที่คนเข้าใจ คือมุมเอียงด้วย atan2 พลังงานการเคลื่อนไหว ความสูงจากความดัน และระดับเสียงแบบ dBFS แล้วเลือก widget ให้เหมาะกับแต่ละปริมาณ

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. อธิบายรูปแบบ raw → derived → viz และบอกได้ว่าปริมาณใดใช้ฟังก์ชันสำเร็จของ dsp (tilt, altitude) และปริมาณใดต้องเขียนสูตรเอง (energy, dBFS)
2. คำนวณมุม roll และ pitch จากความเร่งสามแกนด้วย atan2 ได้ และอธิบายว่าทำไมหน่วยของ accelerometer หักล้างกันในสูตรอัตราส่วน
3. คำนวณพลังงานการเคลื่อนไหวจาก motion() ที่ให้หน่วย m/s² (หาร 9.81 เป็น g แล้วลบ 1g) และความสูงสัมพัทธ์ด้วย dsp.altitude(p, p0) ได้
4. เลือก widget (Seg7, Bar, Chart, Arc) ให้เข้ากับปริมาณ และอธิบายว่าทำไม dBFS ใช้สเกล log

## ก่อนเริ่ม

ผ่านโมดูล 2 มาแล้ว อ่านค่าดิบจากเซนเซอร์เป็น และจำโครงสี่จังหวะจากบทเรียน 1.4 ได้
เปิด `s06_physics_viz_full.py` (อยู่ในบทเรียน 3.2) ไว้ลองเล่นก่อนแกะ

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — Tilt, Energy และ Altitude ใช้ได้บน Emulator ส่วนระดับเสียงจริงต้องใช้ไมโครโฟนบนบอร์ด
- **เรียนมาก่อน:** [บทเรียน 2.4 — ลงมือทำ: เก็บ IMU กับเสียงลงไฟล์เดียว](../../m02-daq/l04-multicapture-lab/README.md)

## ดูของจริงก่อน

รัน `s06_physics_viz_full.py` ก่อน เลือกปริมาณใน dropdown แล้วเอียงบอร์ด เขย่า หรือยกขึ้นลง ตัวเลขที่คำนวณเปลี่ยนตามจริง
คำถามของบทเรียนนี้คือ "ตัวเลขจากเซนเซอร์นี้ แปลงเป็นปริมาณที่มีความหมายได้ยังไง"

## แนวคิด

ตัวเลขดิบอย่าง `(0.20, -6.97, 6.87, 1.1, -0.4, 0.3)` จาก `sensors.bmi270.motion()` ยังไม่บอกอะไรคน ขั้น **Processing** แปลงมันเป็นปริมาณ
ที่มีความหมายด้วยสามจังหวะ **raw → derived → viz** (อ่านดิบ → คำนวณ → แสดงผล) สี่ปริมาณของบทเรียนนี้ใช้โครงเดียวกัน ต่างแค่สูตรตรงกลาง
`dsp` คำนวณฝั่ง C จึงเร็ว สองปริมาณมีฟังก์ชันสำเร็จ อีกสองเราเขียนสูตรเอง

**มุมเอียง:** accelerometer วัดเวกเตอร์แรงโน้มถ่วงที่ชี้ลงพื้นเสมอ พอบอร์ดเอียง แรงนี้กระจายไปสามแกน เราถอดมุมกลับด้วย
$\text{roll} = \operatorname{atan2}(a_y, a_z)$ และ $\text{pitch} = \operatorname{atan2}(-a_x, \sqrt{a_y^2 + a_z^2})$ ซึ่งเป็นสูตรเดียวกับที่
`dsp.tilt(ax, ay, az)` ใช้ คืน **(roll, pitch)** เป็นองศา (roll มาก่อน) สูตรเป็นอัตราส่วนของแกน หน่วยจึงหักล้างกัน และ atan2 รู้ควอดรันต์
ได้มุมเต็มช่วงโดยไม่ติดปัญหาหารศูนย์

**พลังงานการเคลื่อนไหว:** `motion()` คืนความเร่งหน่วย m/s² (วางนิ่ง ≈ 9.81) ขนาดเวกเตอร์หาร 9.81 จะได้หน่วย g
$|a| = \sqrt{a_x^2 + a_y^2 + a_z^2} / 9.81$ วางนิ่งได้ราว 1g จึงลบ 1 ออก `energy = abs(mag - 1.0)` ให้ "นิ่ง = 0" เหลือเฉพาะส่วนที่เกิดจากการขยับ
**ความสูง:** ความดันอากาศลดลงเมื่อสูงขึ้น `dsp.altitude(p, p0)` ใช้สูตร barometric เทียบกับความดันอ้างอิง `p0` ที่จับครั้งเดียวก่อนลูป
จึงได้ความสูงสัมพัทธ์ ยกบอร์ด 1 เมตรค่าขึ้นราว +1.0 (ถ้าไม่ใส่ p0 จะเทียบกับ 1013.25 hPa)
**ระดับเสียง:** $\text{rms} = \sqrt{\frac{1}{N}\sum s_i^2}$ แล้ว $\text{dBFS} = 20\log_{10}(\text{rms}/32768)$ ใช้ 20 เพราะ RMS เป็นแอมพลิจูด
และใช้สเกล log เพราะหูคนรับรู้ความดังแบบ log สเกล decibel จึงบีบช่วงกว้างจาก −96 ถึง 0 ให้อ่านง่าย

ขั้น viz คือเลือกภาพให้ตรงกับข้อมูล: `Seg7` สำหรับตัวเลขเด่น `Bar` สำหรับระดับเทียบช่วง 0..100 `Chart` สำหรับแนวโน้มย้อนหลัง
และ `Arc` สำหรับมุม ทุกปริมาณถูก normalize เข้าช่วง 0..100 ด้วย `clamp100` ก่อนป้อน Bar กับ Chart

## ตัวอย่างสมบูรณ์

ตัวอย่างในบทเรียนนี้คือแอปฟิสิกส์ที่ใช้โครง raw → derived → viz แบบเดียวกัน: `03_baro_pressure_altitude.py` โชว์ความดันพร้อมกราฟย้อนหลัง
(เก็บ hPa × 10 เพราะ Chart รับจำนวนเต็ม) ส่วน `09_radar_theremin.py` แปลงระยะมือจากเรดาร์เป็นโน้ตดนตรีด้วย `ui.tone`
ลองทาย (Predict) ก่อนรันว่าแต่ละแอปแปลง raw เป็นปริมาณอะไร

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/03_baro_pressure_altitude.py](examples/03_baro_pressure_altitude.py) | DPS368: จอแสดงความดัน + กราฟย้อนหลัง + สถิติสูง/ต่ำ |
| [examples/09_radar_theremin.py](examples/09_radar_theremin.py) | Radar Theremin: ระยะมือ = โน้ตดนตรี (ลำโพง J8) + เกจ pitch บนจอ |

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นหรือใน `shared/` ด้วย:

- [m03-processing/l02-physics-gauges-lab/examples/s06_physics_viz_full.py](../l02-physics-gauges-lab/examples/s06_physics_viz_full.py) — Physics Lab: raw -> derived -> viz (ฉบับเต็ม)
- [m03-processing/l02-physics-gauges-lab/practice/s06_physics_viz.py](../l02-physics-gauges-lab/practice/s06_physics_viz.py) — Physics Lab: raw -> derived -> viz (ฉบับฝึกเติมโค้ด)
- [shared/interactive/math_lab.html](../../shared/interactive/math_lab.html)

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. ปริมาณใดในบทเรียนนี้ที่มีฟังก์ชันสำเร็จใน dsp (เลือกทุกข้อที่ถูก) *(เลือกได้หลายข้อ · เป้าหมายข้อ 1)*
   - ก) มุมเอียง (dsp.tilt)
   - ข) ความสูง (dsp.altitude)
   - ค) พลังงานการเคลื่อนไหว
   - ง) ระดับเสียง dBFS

   <details><summary>เฉลย</summary>

   **ก, ข** — tilt กับ altitude มีในโมดูล dsp ส่วน energy กับ dBFS เราเขียนสูตรเองด้วย math.sqrt และ math.log10

   </details>

2. ax = 0, ay = 6.9, az = 6.9 m/s² มุม roll = atan2(ay, az) เป็นเท่าไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) 0 องศา
   - ข) 45 องศา
   - ค) 90 องศา
   - ง) คำนวณไม่ได้เพราะไม่ได้แปลงหน่วยเป็น g ก่อน

   <details><summary>เฉลย</summary>

   **ข** — atan2(6.9, 6.9) = 45° สูตรเป็นอัตราส่วน หน่วยจึงหักล้างกัน ใช้ m/s² หรือ g ก็ได้มุมเท่ากัน

   </details>

3. วางบอร์ดนิ่ง motion() ให้ |a| ≈ 9.81 m/s² ถ้าเขียน energy = abs(mag - 1.0) โดยไม่หาร 9.81 จะได้อะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) ราว 0 ตามที่ต้องการ
   - ข) ราว 8.8 แถบจะเต็มตลอดแม้วางนิ่ง
   - ค) ราว −1
   - ง) error เพราะ math.sqrt รับค่าลบไม่ได้

   <details><summary>เฉลย</summary>

   **ข** — ต้องหาร 9.81 ให้เป็นหน่วย g ก่อน ตอนนิ่ง mag ≈ 1 แล้วลบ 1 จึงเหลือราว 0

   </details>

4. ทำไมจับความดัน p0 ครั้งเดียวก่อนลูปแล้วส่งเข้า dsp.altitude(p, p0) *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) เพราะ dsp.altitude ต้องมีสองค่าเสมอ
   - ข) เพื่อให้ได้ความสูงสัมพัทธ์เทียบกับจุดเริ่ม ซึ่งเห็นการยกบอร์ดชัดและไม่ขึ้นกับสภาพอากาศวันนั้น
   - ค) เพื่อให้เซนเซอร์อุ่นเครื่อง
   - ง) เพื่อแปลง hPa เป็น kPa

   <details><summary>เฉลย</summary>

   **ข** — p0 เป็นอาร์กิวเมนต์ไม่บังคับ ถ้าไม่ใส่จะเทียบกับ 1013.25 hPa ได้ความสูงเหนือน้ำทะเลที่ขึ้นกับอากาศ การใส่ p0 เองทำให้จุด 0 อยู่ที่ตอนเริ่มโปรแกรม

   </details>

5. ทำไมระดับเสียงใช้สเกล dBFS (log) แทนค่า RMS ตรง ๆ *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) เพราะ log คำนวณเร็วกว่า
   - ข) เพราะหูรับรู้ความดังแบบ log และช่วงของเสียงกว้างมาก log ทำให้เสียงเบาไม่เบียดกันจนอ่านไม่ออก
   - ค) เพราะ RMS ติดลบได้
   - ง) เพราะ Bar รับเฉพาะค่าติดลบ

   <details><summary>เฉลย</summary>

   **ข** — สเกล decibel บีบช่วงกว้างตั้งแต่ราว −96 ถึง 0 dBFS ให้อ่านง่าย แบบเดียวกับริกเตอร์หรือ pH

   </details>

## แล็บ

- [ ] คำนวณมุม roll ของ (ax, ay, az) = (0, −6.97, 6.87) m/s² ด้วยมือหรือเครื่องคิดเลข แล้วเทียบกับ `dsp.tilt` ใน REPL
- [ ] วางบอร์ดนิ่งแล้วคำนวณ energy ทั้งแบบหาร 9.81 และไม่หาร จดลงบันทึกการเรียนว่าต่างกันอย่างไร
- [ ] ถ้ามีบอร์ด ยกบอร์ดขึ้นลงหนึ่งเมตรแล้วดู `dsp.altitude(p, p0)` เปลี่ยนเท่าไร

## ไปต่อ

บทเรียน 3.2 เราจะเติมสี่สูตรในไฟล์ `s06_physics_viz.py` แล้วดูเกจทั้งสี่ขยับตามการเคลื่อนไหวจริง

บทเรียนถัดไป: [บทเรียน 3.2 — ลงมือทำ: เกจฟิสิกส์สี่ตัวบนจอ](../l02-physics-gauges-lab/README.md)

## สะท้อนคิด

- มีอุปกรณ์ใดรอบตัวที่แปลงตัวเลขดิบเป็นปริมาณแบบเดียวกับบทเรียนนี้ เช่น นาฬิกานับก้าวหรือมือถือที่รู้ว่าอยู่ชั้นไหน
- ถ้าต้องแสดงความดันอากาศให้คนทั่วไปดู คุณจะเลือก widget ใด เพราะอะไร
