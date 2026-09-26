---
id: aiot-mpy.m03.l02
lang: th
title: {th: gyro ฟิลเตอร์ complementary และโค้ดเครื่องวัดระดับ, en: 'Gyro, the complementary filter and the level code'}
summary: {th: เห็นว่า gyro กับ accelerometer เสียคนละแบบ (drift กับการกระตุก) ฟิลเตอร์ complementary และ dsp.EMA เข้ามาช่วยตรงไหน แล้วแกะโค้ดเครื่องวัดระดับทีละท่า ตั้งแต่อุ่นเครื่องเซนเซอร์จนถึงปุ่มตั้งศูนย์, en: 'See how the gyro and the accelerometer fail in different ways (drift versus jitter), where a complementary filter and dsp.EMA help, then read the digital-level code pose by pose from sensor warm-up to the zero button.'}
level: L2
time_min: {concept: 30, practise: 20, check: 5}
hardware: {emulator: true, boards: [eva-kit, devkit]}
prerequisites: [aiot-mpy.m03.l01]
objectives:
  - {th: คำนวณมุมที่ไหลจาก bias ของ gyro ได้ (เช่น 0.05 deg/s นาน 60 วินาที ได้ 3°) และอธิบายว่าฟิลเตอร์ complementary ฟัง gyro ในช่วงสั้นและฟัง accelerometer ในช่วงยาวอย่างไร, en: Compute the angle drift caused by a gyro bias (e.g. 0.05 deg/s for 60 s gives 3°) and explain how a complementary filter trusts the gyro short-term and the accelerometer long-term.}
  - {th: 'คำนวณ time constant จากค่าในลูปได้ทั้งของ dsp.EMA (τ ≈ Ts/α: 0.2 s กับ α 0.2 ได้ราว 1 s) และของ complementary (τ = aΔt/(1−a): a 0.98 ได้ 9.8 s) และบอกได้ว่า alpha สูงในสองสูตรนี้ให้ผลตรงข้ามกัน', en: 'Compute time constants from loop values for dsp.EMA (τ ≈ Ts/α: 0.2 s with α 0.2 gives about 1 s) and for the complementary filter (τ = aΔt/(1−a): a 0.98 gives 9.8 s), and state that a high alpha does opposite things in the two formulas.'}
  - {th: 'อธิบายเหตุผลของท่าในโค้ดเครื่องวัดระดับได้: ไม่เรียก sensors.init() แต่อุ่นเครื่องใน try/except, ตั้ง ui.Bar เป็น min=-90 max=90, กรองก่อนแล้วค่อยหักค่าศูนย์ และเรียก ui.poll() ทุกรอบ', en: 'Explain the reasons behind the digital-level code: no sensors.init() but a warm-up inside try/except, ui.Bar set to min=-90 max=90, filter before subtracting the zero, and ui.poll() on every loop.'}
  - {th: 'รัน 05_madgwick_and_pedometer.py แล้วชี้ได้ว่าต้องแปลงหน่วยอะไรก่อนป้อน dsp.Madgwick และ dsp.Pedometer (gyro เป็น rad/s, ความเร่งเป็น g, fs เท่าอัตราของลูปจริง)', en: 'Run 05_madgwick_and_pedometer.py and point out which units must be converted before feeding dsp.Madgwick and dsp.Pedometer (gyro in rad/s, acceleration in g, fs equal to the real loop rate).'}
develops: [{skill: sys.dsp, to: 2}, {skill: sys.sensors-actuators, to: 2}, {skill: gui.hmi, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {repo: 'https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer', path: session-06.html (slides 13–32), ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079}
---

# บทเรียน 3.2 — gyro ฟิลเตอร์ complementary และโค้ดเครื่องวัดระดับ

> โมดูล 3 — แสดงผลเซนเซอร์บน HMI · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เห็นว่า gyro กับ accelerometer เสียคนละแบบ (drift กับการกระตุก) ฟิลเตอร์ complementary และ dsp.EMA เข้ามาช่วยตรงไหน แล้วแกะโค้ดเครื่องวัดระดับทีละท่า ตั้งแต่อุ่นเครื่องเซนเซอร์จนถึงปุ่มตั้งศูนย์

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. คำนวณมุมที่ไหลจาก bias ของ gyro ได้ (เช่น 0.05 deg/s นาน 60 วินาที ได้ 3°) และอธิบายว่าฟิลเตอร์ complementary ฟัง gyro ในช่วงสั้นและฟัง accelerometer ในช่วงยาวอย่างไร
2. คำนวณ time constant จากค่าในลูปได้ทั้งของ dsp.EMA (τ ≈ Ts/α: 0.2 s กับ α 0.2 ได้ราว 1 s) และของ complementary (τ = aΔt/(1−a): a 0.98 ได้ 9.8 s) และบอกได้ว่า alpha สูงในสองสูตรนี้ให้ผลตรงข้ามกัน
3. อธิบายเหตุผลของท่าในโค้ดเครื่องวัดระดับได้: ไม่เรียก sensors.init() แต่อุ่นเครื่องใน try/except, ตั้ง ui.Bar เป็น min=-90 max=90, กรองก่อนแล้วค่อยหักค่าศูนย์ และเรียก ui.poll() ทุกรอบ
4. รัน 05_madgwick_and_pedometer.py แล้วชี้ได้ว่าต้องแปลงหน่วยอะไรก่อนป้อน dsp.Madgwick และ dsp.Pedometer (gyro เป็น rad/s, ความเร่งเป็น g, fs เท่าอัตราของลูปจริง)

## ก่อนเริ่ม

ต่อจากบทเรียน 3.1: ต้องจำได้ว่า `dsp.tilt()` คืน `(roll, pitch)` และหกแกนมาจาก `motion()` ครั้งเดียว
ทบทวน `dsp.EMA` จากบทเรียน 2.7–2.9 (ค่าใหม่มีน้ำหนัก α ที่เหลือคือความจำของค่าเก่า) เพราะวันนี้มันกลับมาเป็นตัวกรองของเครื่องวัดระดับ
เปิดไฟล์ฝึก `s06_digital_level.py` ของบทเรียน 3.3 ไว้ข้าง ๆ สไลด์ "แกะโค้ดจริง" ไล่ตามไฟล์นั้นทีละท่า

- **อุปกรณ์:** บอร์ด Eva Kit หรือ TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/)
- **เรียนมาก่อน:** [บทเรียน 3.1 — accelerometer กับมุมเอียง: roll และ pitch](../l01-accelerometer-tilt/README.md)

## แนวคิด

**gyro รู้แค่ว่าตอนนี้กำลังหมุนเร็วแค่ไหน ไม่รู้ว่าอยู่ที่กี่องศา** โครงสร้างในชิปถูกขับให้สั่นในแนวหนึ่งตลอดเวลา
พอชิปหมุน แรง Coriolis ผลักมวลที่กำลังสั่นให้เบนไปในแนวตั้งฉาก วงจรวัดการเบนนั้นแล้วแปลงเป็น deg/s
จะได้มุมต้องบวกสะสม ω·Δt เอง และตรงนี้คือที่มาของปัญหา

สองเซนเซอร์เสียคนละแบบ **accelerometer ถูกในระยะยาวแต่กระตุกในระยะสั้น** เพราะมันวัดแรงทั้งหมด แยกไม่ได้ว่าอันไหนคือแรงโน้มถ่วง
อันไหนคือมือที่เขย่า พัดลม หรือการเคาะโต๊ะ **gyro นิ่งและไวในระยะสั้นแต่ไหลในระยะยาว** บน Eva Kit วางนิ่งแล้ว `gz` ยังอ่านได้ 0.03–0.05 deg/s
ถ้า bias เป็น 0.05 deg/s มุมที่บวกสะสมจะผิด 3° หลัง 60 วินาที และ 30° หลัง 600 วินาที ปรากฏการณ์นี้ชื่อ **drift**

ฟิลเตอร์ complementary เอาจุดแข็งของทั้งคู่มาต่อกัน: θ = a(θ + ωΔt) + (1−a)θ_accel ครึ่งแรกเป็น high-pass ต่อ gyro
ครึ่งหลังเป็น low-pass ต่อ accelerometer และสองครึ่งรวมกันได้หนึ่งพอดี เส้นแบ่งคือ τ = aΔt/(1−a) ซึ่งที่ a = 0.98, Δt = 0.2 s ได้ 9.8 s
แต่ชุดบทเรียนนี้ใช้ **ครึ่งเดียว** คือ `dsp.tilt()` (accelerometer ล้วน) ต่อด้วย `dsp.EMA(alpha=0.2)` ได้ τ ≈ Ts/α = 1.0 s
ได้เส้นนิ่งที่ไม่มี drift เลยเพราะไม่ได้อินทิเกรตอะไร แลกกับ lag ราวหนึ่งวินาที และอย่าเชื่อชื่อพารามิเตอร์: alpha สูงใน `dsp.EMA`
แปลว่าเชื่อค่าใหม่มาก (ไวขึ้น สั่นขึ้น) ส่วน a สูงใน complementary แปลว่าเชื่อค่าเดิมกับ gyro มาก (นิ่งขึ้น)

ตระกูล IMU มีสิบสี่ชื่อ: `sensors.bmi270` ห้าชื่อ (`temperature()` กับ `chip_id()` ขึ้น `OSError` บน Eva Kit แต่ใช้ได้บน Dev Kit),
`sensors.bmm350` ห้าชื่อที่ใช้ได้ทั้งสองบอร์ด และฝั่ง `dsp` อีกสี่ชื่อ ถ้าอยากได้ fusion เต็มรูปและ yaw มี `dsp.Madgwick(beta=, fs=)`
ซึ่งต้องป้อน gyro เป็น **เรเดียนต่อวินาที** (`math.radians(gx)`) และ `fs` ต้องเท่าอัตราของลูปจริง (ลูป 200 ms คือ `fs=5.0` ไม่ใช่ค่าตั้งต้น 100)
ส่วน `dsp.Pedometer` มีค่าตั้งต้น `threshold=1.5` เป็นหน่วย **g** ทั้งสองคลาสไม่มี `.value()` เข็มทิศมี `bmm350.heading()` ที่ใช้ atan2(x, y)
กับ `dsp.compass()` ที่ใช้ atan2(y, x) จึงคืนคนละมุม และ `dsp.compass()` ทิ้ง `mz` จึงยังไม่ชดเชยการเอียง
ตัวเลขขนาดสนามที่บอร์ดอ่านได้ (ราว 1532) ยังไม่มีข้อสรุปว่าตัวคงที่หรือป้ายหน่วย µT ผิด อย่าจดเป็นข้อเท็จจริง

**ปุ่มตั้งศูนย์** มีเพราะวางราบแล้วแทบไม่มีทางได้ 0.0 เป๊ะ (โต๊ะไม่ราบจริง ชิปติดไม่ตรงเป๊ะ และมี zero-g offset จากโรงงาน)
เราจำมุมตอนกดไว้แล้วลบออกทุกรอบ เช่นกดตอน 1.8° แล้วต่อจากนั้น 4.3° จะแสดงเป็น 2.5° โค้ดเครื่องวัดระดับเรียงเป็นหกท่า:

1. **อุ่นเครื่อง** ไม่มี `sensors.init()` ทั้งสองบอร์ด (Eva ปฏิเสธด้วย `OSError` · Dev Kit ไม่จำเป็น) อ่าน `motion()` ทิ้งหนึ่งครั้งใน `try/except` เพราะรอบแรกหลังรีเซ็ตบน Eva รอได้ถึง 16 วินาที
2. **หน้าจอ** `ui.Bar(..., min=-90, max=90)` เพราะช่วงปริยาย 0–100 จะปัด −30 เป็น 0 จนแถบนิ่ง · `ui.Scale` แนวนอนคือไม้บรรทัด ไม่รับ `.value()` · `ui.Spinbox` ต้องมีปุ่มเพิ่ม/ลดข้าง ๆ เพราะนิ้วแตะแล้วแค่เลือกหลัก
3. **อ่านและแปลง** `motion()` แล้ว `dsp.tilt()` ห่อด้วย `try/except OSError` เพราะการอ่านพลาดเป็นเรื่องปกติ
4. **กรองแล้วหักศูนย์** `roll_f = ema_roll.update(roll)` ก่อน แล้วค่อย `roll_f - roll_zero`
5. **รับเหตุการณ์** `ui.poll()` ทุกรอบ เพราะเงียบราวสองวินาที widget จะถูกซ่อนทั้งหน้า แล้วเทียบ `ev['handle']` กับ `.id()` ที่เก็บไว้ ตอนกดตั้งศูนย์เก็บ `roll_f` ที่กรองแล้ว ไม่ใช่ค่าดิบ
6. **แสดงผล** `int(clamp90(...))` ก่อนส่งให้แถบ แถบกับไฟขยับทุกรอบ (5 ครั้งต่อวินาที) ส่วน Seg7 เขียนใหม่ไม่เกินวินาทีละครั้ง

## ตัวอย่างสมบูรณ์

สองไฟล์นี้อยู่นอกเกณฑ์ผ่านของชุดบทเรียน แต่เป็นที่เดียวที่ได้ลองของตระกูล IMU ที่เหลือ

- `05_madgwick_and_pedometer.py` **ทำนายก่อนรัน**: มีตัวนับก้าวสองตัว ตัวหนึ่งป้อนเป็น g อีกตัวใช้ค่าตั้งต้นแล้วป้อน m/s² ตรง ๆ ตัวไหนจะนับขึ้นเองทั้งที่บอร์ดวางนิ่ง ·
  **รัน** แล้ววางบอร์ดนิ่ง ดูตัวสีส้ม · **สำรวจ** เทียบคอลัมน์ Madgwick กับ `dsp.tilt()` ตอนวางนิ่งและตอนสะบัด และสังเกตว่า yaw มีแค่ฝั่ง Madgwick ·
  **ดัดแปลง** ลบสามบรรทัด `math.radians()` ชั่วคราว แล้วดูว่ามุมหมุนติ้วแค่ไหน (ไฟล์นี้ลูปทุก 100 ms จึงตั้ง `fs=10.0`)
- `04_compass_and_magnetometer.py` เทียบ `heading()` กับ `dsp.compass()` ซึ่งไม่เท่ากัน และนั่นถูกแล้ว กดปุ่มล้างค่าแล้วหมุนบอร์ดช้า ๆ ครบรอบ
  เพื่อดูสถานะการสอบเทียบ แล้วลองเอียงบอร์ดดูว่าทิศจาก `dsp.compass()` เพี้ยนทันที

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/04_compass_and_magnetometer.py](examples/04_compass_and_magnetometer.py) | เข็มทิศบนบอร์ด และตัวเลขหนึ่งตัวที่ยังไม่มีใครตอบได้ |
| [examples/05_madgwick_and_pedometer.py](examples/05_madgwick_and_pedometer.py) | สองคลาส IMU ที่เหลือใน dsp และหน่วยที่ดักไว้ทั้งคู่ |

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นด้วย:

- [m03-sensor-hmi/l03-digital-level-lab/practice/s06_digital_level.py](../l03-digital-level-lab/practice/s06_digital_level.py) — เครื่องวัดระดับดิจิทัลสองแกน (ฉบับฝึกเติมโค้ด)
- [shared/lvgl_ports/sec3_sensor_viz/eva/ex10_scale_pitch.py](../../shared/lvgl_ports/sec3_sensor_viz/eva/ex10_scale_pitch.py)

**ภาพจอจาก BENTO Emulator** ของตัวอย่างในบทนี้ (คลิกชื่อไฟล์เพื่อเปิดโค้ด)

<div class="tok-screens">
<figure><img src="img/screens/04_compass_and_magnetometer.webp" alt="จอของ examples/04_compass_and_magnetometer.py ขณะรันใน BENTO Emulator: เข็มทิศบนบอร์ด และตัวเลขหนึ่งตัวที่ยังไม่มีใครตอบได้" width="800" height="480" loading="lazy"><figcaption><a href="examples/04_compass_and_magnetometer.py"><code>04_compass_and_magnetometer.py</code></a> เข็มทิศบนบอร์ด และตัวเลขหนึ่งตัวที่ยังไม่มีใครตอบได้</figcaption></figure>
<figure><img src="img/screens/05_madgwick_and_pedometer.webp" alt="จอของ examples/05_madgwick_and_pedometer.py ขณะรันใน BENTO Emulator: สองคลาส IMU ที่เหลือใน dsp และหน่วยที่ดักไว้ทั้งคู่" width="800" height="480" loading="lazy"><figcaption><a href="examples/05_madgwick_and_pedometer.py"><code>05_madgwick_and_pedometer.py</code></a> สองคลาส IMU ที่เหลือใน dsp และหน่วยที่ดักไว้ทั้งคู่</figcaption></figure>
</div>

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. วางบอร์ดนิ่ง gyro อ่าน gz ได้ 0.05 deg/s (bias) ถ้าบวกสะสม ω·Δt เป็นมุมไปเรื่อย ๆ ผ่านไป 10 นาที มุมจะผิดไปราวเท่าไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) 30°
   - ข) 3°
   - ค) 0.05°
   - ง) 0° เพราะบอร์ดไม่ได้หมุน

   <details><summary>เฉลย</summary>

   **ก** — 0.05 deg/s × 600 s = 30° ความผิดพลาดจิ๋วถูกบวกสะสมทุกรอบโดยไม่มีอะไรดึงกลับ นี่คือ drift และเป็นเหตุผลที่ต้องให้ accelerometer คอยดึงกลับในระยะยาว

   </details>

2. ลูปหมุนทุก 200 ms และใช้ dsp.EMA(alpha=0.2) ค่าที่กรองแล้วจะตามการเอียงช้ากว่าค่าดิบราวเท่าไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) ราว 1 วินาที
   - ข) ราว 0.04 วินาที
   - ค) ราว 9.8 วินาที
   - ง) ไม่มี lag เพราะ EMA ไม่ได้อินทิเกรตอะไร

   <details><summary>เฉลย</summary>

   **ก** — τ ≈ Ts/α = 0.2/0.2 = 1.0 วินาที ส่วน 9.8 วินาทีคือเส้นแบ่งของ complementary ที่ a = 0.98 การไม่อินทิเกรตทำให้ไม่มี drift แต่ยังมี lag

   </details>

3. เพื่อนบอกว่า "ตั้ง alpha=0.98 แล้วเส้นจะนิ่งขึ้นเสมอ" ข้อใดถูก *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) จริงเฉพาะ complementary ที่ a สูงแปลว่าเชื่อค่าเดิมกับ gyro มาก ส่วน dsp.EMA ที่ alpha 0.98 แปลว่าเชื่อค่าใหม่มาก จึงไวและสั่นขึ้น
   - ข) จริงทั้งสองสูตร เพราะชื่อพารามิเตอร์เหมือนกัน
   - ค) ไม่จริงทั้งสองสูตร alpha สูงทำให้สั่นขึ้นเสมอ
   - ง) alpha ไม่มีผลกับความนิ่ง มีผลแค่กับ drift

   <details><summary>เฉลย</summary>

   **ก** — ใน dsp.EMA ค่าใหม่มีน้ำหนัก α ส่วนใน complementary ค่าเดิมบวก gyro มีน้ำหนัก a ตัวเลขเดียวกันจึงให้ผลตรงข้ามกันสุดขั้ว ให้เปิดดูสมการ อย่าเชื่อชื่อพารามิเตอร์

   </details>

4. ข้อใดคือเหตุผลที่ถูกต้องของโค้ดเครื่องวัดระดับ เลือกทุกข้อที่ถูก *(เลือกได้หลายข้อ · เป้าหมายข้อ 3)*
   - ก) ต้องตั้ง ui.Bar เป็น min=-90, max=90 ไม่งั้นช่วงปริยาย 0–100 จะปัด −30 องศาเป็น 0 แล้วแถบนิ่งสนิททั้งที่โค้ดคำนวณถูก
   - ข) ตอนกดตั้งศูนย์ต้องเก็บ roll_f ที่กรองแล้ว ไม่ใช่ roll ดิบที่อาจกำลังสั่นอยู่พอดี
   - ค) ต้องเรียก sensors.init() ก่อน motion() บน Eva Kit ไม่งั้นอ่านค่าไม่ได้
   - ง) เรียก ui.poll() เฉพาะรอบที่มีคนกดปุ่มก็พอ

   <details><summary>เฉลย</summary>

   **ก, ข** — บน Eva Kit sensors.init() ถูกปฏิเสธด้วย OSError และบน Dev Kit ก็ไม่จำเป็น ส่วน ui.poll() ต้องเรียกทุกรอบ เพราะฝั่ง CM55 ใช้มันเป็นสัญญาณว่าโปรแกรมยังมีชีวิต เงียบราวสองวินาที widget จะถูกซ่อนทั้งหน้า

   </details>

5. จาก 05_madgwick_and_pedometer.py ข้อใดคือกับดักเรื่องหน่วยที่ต้องจัดการเอง เลือกทุกข้อที่ถูก *(เลือกได้หลายข้อ · เป้าหมายข้อ 4)*
   - ก) Madgwick.update() ต้องการ gyro เป็นเรเดียนต่อวินาที แต่ motion() คืนองศาต่อวินาที จึงต้อง math.radians() เอง
   - ข) Pedometer ค่าตั้งต้น threshold=1.5 เป็นหน่วย g ถ้าป้อน m/s² มันจะนับก้าวขึ้นเรื่อย ๆ ทั้งที่บอร์ดวางนิ่ง
   - ค) fs ของ Madgwick ต้องเท่าอัตราของลูปจริง ลูป 200 ms คือ fs=5.0
   - ง) Madgwick กับ Pedometer มี .value() ให้อ่านผลเหมือนตัวกรองหกตัวในบทเรียน 2.7–2.9

   <details><summary>เฉลย</summary>

   **ก, ข, ค** — ลืมแปลง gyro เท่ากับป้อนใหญ่เกินจริงราว 57 เท่า มุมหมุนติ้วโดยไม่มี error และ 9.81 m/s² ข้ามเกณฑ์ 1.5 ตั้งแต่ยังไม่ขยับ ทั้งสองคลาสไม่มี .value() ต้องเก็บค่าที่ .update() คืนมาเอง

   </details>

## ไปต่อ

บทเรียน 3.3 คือแล็บ: เติมช่องว่างหกจุดใน `s06_digital_level.py` ตามหกท่าที่เพิ่งแกะ แล้วตรวจกับ MVP checkpoint
ตอนทดสอบให้วางบอร์ดราบ กดตั้งศูนย์ แล้วเอียงช้า ๆ อย่าถือบอร์ดลอยกลางอากาศแล้วโบก เพราะความเร่งจากการเหวี่ยงจะปนกับแรงโน้มถ่วง

บทเรียนถัดไป: [บทเรียน 3.3 — ลงมือทำ: เครื่องวัดระดับดิจิทัล](../l03-digital-level-lab/README.md)

## สะท้อนคิด

- เครื่องชั่งในครัวมีปุ่มแบบเดียวกับปุ่มตั้งศูนย์ ของรอบตัวคุณมีอะไรอีกที่ให้ผู้ใช้กำหนดจุดอ้างอิงเอง
- ถ้าต้องเปลี่ยนคาบลูปจาก 200 ms เป็น 50 ms คุณต้องกลับไปคิดตัวเลขไหนใหม่อีกบ้าง
