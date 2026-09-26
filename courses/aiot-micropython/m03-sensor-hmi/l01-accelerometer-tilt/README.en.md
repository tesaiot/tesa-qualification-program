---
id: aiot-mpy.m03.l01
lang: en
title: {th: 'accelerometer กับมุมเอียง: roll และ pitch', en: 'The accelerometer and tilt: roll and pitch'}
summary: {th: เข้าใจว่า accelerometer วัดแรงที่ดันมวลจิ๋วในชิปไว้ ไม่ได้วัดมุม แล้วใช้เงาของแรงโน้มถ่วงบนแกนของบอร์ดกับ atan2 เปลี่ยนความเร่งสามแกนเป็น roll และ pitch โดยจำลำดับที่ dsp.tilt() คืนค่าได้แม่น, en: 'Understand that an accelerometer measures the force holding a tiny proof mass, not an angle, then turn three acceleration axes into roll and pitch through gravity''s projection and atan2, remembering the order dsp.tilt() returns them in.'}
level: L2
time_min: {concept: 25, lab: 15, check: 5}
hardware: {emulator: true, boards: [eva-kit, devkit]}
prerequisites: [aiot-mpy.m02.l09]
objectives:
  - {th: อธิบายได้ว่าทำไมบอร์ดที่วางนิ่งบนโต๊ะอ่าน az ได้ราว +9.81 m/s² แต่ตอนตกอิสระอ่านได้ราว 0 ทั้งสามแกน โดยใช้แนวคิด proper acceleration และมวลพิสูจน์บนสปริงในชิป, en: 'Explain why a board lying still reads az of about +9.81 m/s² yet reads about 0 on all three axes in free fall, using proper acceleration and the spring-mounted proof mass inside the chip.'}
  - {th: 'คำนวณ roll จาก ay และ az ด้วย atan2 ได้ถูกภายใน 1 องศา (เช่น ay 4.90, az 8.49 ได้ 30°) ตรวจค่าดิบด้วยขนาด √(ax²+ay²+az²) ≈ 9.81 m/s² ก่อนเชื่อ และบอกได้ว่าทำไม yaw หาจาก accelerometer ไม่ได้', en: 'Compute roll from ay and az with atan2 to within 1 degree (e.g. ay 4.90, az 8.49 gives 30°), sanity-check the raw values with the magnitude √(ax²+ay²+az²) ≈ 9.81 m/s² first, and state why yaw cannot come from the accelerometer.'}
  - {th: 'เขียน `ax, ay, az, gx, gy, gz = sensors.bmi270.motion()` ตามด้วย `roll, pitch = dsp.tilt(ax, ay, az)` ในลำดับที่ถูก และอธิบายว่าทำไมต้องได้หกแกนจากการอ่านครั้งเดียว', en: 'Write `ax, ay, az, gx, gy, gz = sensors.bmi270.motion()` followed by `roll, pitch = dsp.tilt(ax, ay, az)` in the right order, and explain why the six axes must come from a single read.'}
develops: [{skill: sys.sensors-actuators, to: 2}, {skill: hw.math, to: 2}, {skill: hw.electronics, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {repo: 'https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer', path: session-06.html (slides 1–12), ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079}
source_sha256: 23e0bec195f6975efd47ccd452428d63adfdf762ec80a6a990993a31ed951f9e
---

# Lesson 3.1 — The accelerometer and tilt: roll and pitch

> Module 3 — Sensor Visualization on HMI · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Understand that an accelerometer measures the force holding a tiny proof mass in the chip, not an angle, then turn three acceleration axes into roll and pitch through gravity's projection onto the board's axes and atan2, remembering the order dsp.tilt() returns its values in.

## Objectives

By the end of this lesson you will be able to:

1. Explain why a board lying still reads az of about +9.81 m/s² yet reads about 0 on all three axes in free fall, using proper acceleration and the spring-mounted proof mass inside the chip
2. Compute roll from ay and az with atan2 to within 1 degree (e.g. ay 4.90, az 8.49 gives 30°), sanity-check the raw values with the magnitude √(ax²+ay²+az²) ≈ 9.81 m/s² first, and state why yaw cannot come from the accelerometer
3. Write `ax, ay, az, gx, gy, gz = sensors.bmi270.motion()` followed by `roll, pitch = dsp.tilt(ax, ay, az)` in the right order, and explain why the six axes must come from a single read

## Before you start

Review lessons 2.7–2.9: there we turned one raw value from `pot.read()` into a percentage and voltage, then put it on screen with Bar + Scale + Seg7.
Lessons 3.1–3.3 use the same screen layout — only the data source changes, to three raw values from the IMU, with a formula sitting in the middle.
This lesson has no code file of its own yet. Have a calculator with atan2 ready, and your learning log to record which edge of your team's board makes the value change.

- **Equipment:** an Eva Kit or TESAIoT Dev Kit board with the BENTO MicroPython firmware installed, or the BENTO Emulator in [BENTO IDE](https://ide.tesaiot.dev/)
- **Before this:** [Lesson 2.9 — Hands-on: the potentiometer gauge and touch slider](../../m02-ui-to-hardware/l09-pot-capsense-lab/README.md)

## See it work first

Open the Sensor Dashboard menu on the board, and try three things before diving into the content: lying flat, one line (AZ) stays high and never reaches zero;
lift one edge, that line drops and another line (AY) climbs to take its place; shake it then set it down, and the gyro spikes then settles at once.
The line that stays up is **gravity**, and it is the key to the digital level we build in lesson 3.3.

## Concepts

**A sensor never tells you an angle — we work it out ourselves from raw numbers.** No chip measures "degrees" directly. An IMU measures acceleration and angular velocity,
and if we compute in the wrong order or the wrong unit, the program does not crash — it just answers wrong, quietly, which is the most expensive kind of bug.

An accelerometer does not measure how fast the board is speeding up. It measures **the force the housing uses to hold a tiny mass inside it from falling freely**
(proper acceleration). The table pushes the board up, the board pushes the mass up, so it reads +1 g pointing up; during free fall, all three axes read about 0.
Inside the BMI270 is a proof mass on a silicon spring, with comb fingers interleaved with fingers fixed to the housing — each pair is a capacitor.
Whenever the mass shifts, the capacitance on the two sides differs; a circuit measures that difference and feeds it to an ADC inside the chip, which comes out as a number over I2C.

Gravity always points down with a magnitude of 9.81 m/s². As the board tilts, its "shadow" moves from az onto ay, but the combined magnitude stays constant
(0° gives az 9.81, ay 0 · 30° gives az 8.50, ay 4.91 · 90° gives az 0, ay 9.81). Before trusting any value, check that √(ax²+ay²+az²) comes out to about 9.81,
then convert the shadow to degrees: roll = atan2(ay, az) and pitch = atan2(−ax, √(ay²+az²)), multiplied by 180/π.
We use `atan2`, not `atan`, because it takes the numerator and denominator separately, so it can tell all four quadrants apart and never blows up when the denominator is zero at a right angle.
Yaw (spinning the board flat on the table) never changes the shadow on any axis at all, so the accelerometer cannot see it — you need a magnetometer (lessons 3.7–3.9) or the gyro.

All of this is two lines of code, with two traps:

- `dsp.tilt(ax, ay, az)` returns `(roll, pitch)` — **roll always comes first**. If you accidentally write `pitch, roll = ...`, the order many textbooks use,
  the program does not error; the screen shows numbers in full, but tilting left-right makes the PITCH bar move while the ROLL bar sits still
- `sensors.bmi270.motion()` gives all six axes from **the same single read** (ax, ay, az in m/s²; gx, gy, gz in deg/s).
  On the Eva Kit it picks up one snapshot held by the display core; on the Dev Kit, CM33 reserves the I2C bus, reads six axes, then releases it.
  If you call `acceleration()` and then `gyroscope()`, the value could belong to a different set between the two calls, and if the board is moving, the two would come from different moments in its motion

The axis convention must always be confirmed against the real board. The slides use the Eva Kit lifting its left edge as the example (ay 4.90, az 8.49 gives 30.0°),
but on the TESAIoT Dev Kit, **nobody has measured yet** which edge of the QWA309 base makes roll increase — the same IMU chip, mounted on a differently built board.
Dev Kit teams must lift each edge and record it themselves — never borrow the Eva Kit's "left edge" wording.

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automatic marking.

1. A board lies still on the table, not moving anywhere, yet az reads about +9.81 m/s². Why? *(choose one · objective 1)*
   - A) The sensor measures the force the housing uses to hold the proof mass from falling freely; the table pushes the board up, so it reads +1 g pointing up
   - B) It is a factory offset; zeroing it would leave 0
   - C) It is electrical noise that must be filtered out with dsp.EMA
   - D) The board is genuinely accelerating slightly upward from the table vibrating

   <details><summary>Solution</summary>

   **A** — An accelerometer measures proper acceleration, the force that holds a small mass inside from falling freely. If the board were released into free fall, all three axes would read about 0, because nothing is holding that mass any more.

   </details>

2. On the Eva Kit, lifting the left edge reads ay 4.90 and az 8.49 m/s². What should roll be? *(choose one · objective 2)*
   - A) 30.0°
   - B) 60.0°
   - C) 0.524°
   - D) 45.0°

   <details><summary>Solution</summary>

   **A** — roll = atan2(ay, az) = atan2(4.90, 8.49) = 0.524 rad, multiplied by 180/π gives 30.0°. The 0.524 choice is the radian value left unconverted to degrees.

   </details>

3. Which statements about finding tilt from an accelerometer are correct? Choose every correct one. *(choose all that apply · objective 2)*
   - A) Lying still, √(ax²+ay²+az²) should give about 9.81 m/s² no matter how the board is tilted, so it can be used as a sensor health check
   - B) atan2 is used because it can tell all four quadrants apart and never blows up when the denominator is zero at a right angle
   - C) Spinning the board flat on the table changes ay, so yaw can be found from the accelerometer
   - D) dsp.tilt() returns three angles: roll, pitch and yaw

   <details><summary>Solution</summary>

   **A, B** — Gravity's shadow moves between axes but the combined magnitude stays constant, and atan2 takes the numerator and denominator separately. Spinning flat on the table changes the shadow on no axis at all, which is why dsp.tilt() gives only two axes — a limit of physics, not of the firmware.

   </details>

4. If you write `pitch, roll = dsp.tilt(ax, ay, az)` and run the level, what happens? *(choose one · objective 3)*
   - A) It raises TypeError immediately, because the order is wrong
   - B) No error at all; the numbers appear in full, but tilting left-right makes the PITCH bar move while the ROLL bar sits still
   - C) It works correctly, because Python matches by variable name automatically
   - D) Both angle values become 0

   <details><summary>Solution</summary>

   **B** — dsp.tilt() returns (roll, pitch), with roll always first. Swapping the unpacking order does not crash the program — it just gives a wrong answer quietly, which is the most expensive kind of bug, because nobody knows it is sitting there.

   </details>

5. Why does this set of lessons' code read `sensors.bmi270.motion()` once, instead of calling `acceleration()` followed by `gyroscope()`? *(choose one · objective 3)*
   - A) motion() gives all six axes from the same single read; reading them separately while the board moves risks accel and gyro coming from different moments of its motion
   - B) acceleration() does not work on the Eva Kit
   - C) motion() already returns degrees, so dsp.tilt() is unnecessary
   - D) acceleration() returns units of g, while motion() returns m/s²

   <details><summary>Solution</summary>

   **A** — On the Eva Kit, motion() picks up one single snapshot; on the Dev Kit, CM33 reserves the bus, reads six axes, then releases it. Data you plan to combine must come from the same moment. acceleration() also works on both boards and returns m/s² the same way.

   </details>

## Lab

**Find your team's board's axes, and compute an angle by hand** (about 15 minutes). Record every item in your learning log.

- [ ] In Sensor Dashboard, lift each edge in turn (left, right, top, bottom) and record which line drops and which climbs
- [ ] Sum up which edge moves the ay and az pair (used by roll) and which edge moves ax (used by pitch). Dev Kit teams, write clearly which edge of the QWA309 base this is
- [ ] Sanity-check with the Eva Kit numbers from the slides: ax 0.02, ay −0.05, az 9.79 must give a magnitude of about 9.79 m/s²
- [ ] Compute atan2(4.90, 8.49) in radians, then convert to degrees — you should get about 0.524 rad and 30.0°
- [ ] Compute roll from the pair ay 8.50, az 4.91 in the gravity-shadow table, and check that it gives about 60°
- [ ] Write the two lines `motion()` and `dsp.tilt()` in your learning log, and underline the `(roll, pitch)` order

## Going further

Lesson 3.2 continues with the gyro: how it fails in a different way from the accelerometer, where a filter helps, then it takes apart the level code move by move.
If you want to understand "it is the thing sitting still that is really being accelerated", the slides recommend a Veritasium clip, starting at 2:30.

Next lesson: [Lesson 3.2 — Gyro, the complementary filter and the level code](../l02-gyro-fusion/README.md)

## Reflect

- Gravity is what many jobs call noise. Why does it become the signal in this lesson?
- If you accidentally wrote `pitch, roll = dsp.tilt(...)`, how would you notice, given that the program raises no error?
- Does your own work need yaw? If it does, which sensor would you get it from?
