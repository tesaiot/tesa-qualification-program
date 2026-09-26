---
id: edgeai-dev.m03.l01
lang: en
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
translation: done
source_sha256: c17e5bba84124245fe539e1d40a41f27a20ec09558536ceba5c5d58388de4b22
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 3.1 — From raw numbers to physical quantities: tilt angle, energy, altitude and dBFS

> Module 3 — Processing with maths and physics · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Enter the Processing stage with the raw → derived → viz pattern. Turn raw numbers into four quantities people understand — tilt angle with atan2, motion energy, altitude from pressure, and sound level in dBFS — and choose the right widget for each.

## Objectives

By the end of this lesson, you will:

1. Explain the raw → derived → viz pattern, and say which quantities use a ready-made dsp function (tilt, altitude) and which need your own formula (energy, dBFS).
2. Compute roll and pitch from three-axis acceleration with atan2, and explain why the accelerometer's unit cancels out in the ratio formula.
3. Compute motion energy from motion(), which is in m/s² (divide by 9.81 to get g, then subtract 1 g), and relative altitude with dsp.altitude(p, p0).
4. Choose a widget (Seg7, Bar, Chart, Arc) to match each quantity, and explain why dBFS uses a log scale.

## Before you start

You've been through module 2, can read raw sensor values, and remember the four-beat skeleton from lesson 1.4. Open `s06_physics_viz_full.py` (in lesson 3.2) and try it before taking it apart.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — Tilt, Energy and Altitude work on the emulator; real sound level needs the board's microphone.
- **Prior lesson:** [lesson 2.4 — Hands-on: IMU and sound in one file](../../m02-daq/l04-multicapture-lab/README.md)

## See it work first

Run `s06_physics_viz_full.py` first. Pick a quantity in the dropdown, then tilt, shake, or raise and lower the board — the computed number genuinely changes. This lesson's question is: "how does a number from a sensor turn into a quantity that actually means something?"

## Concepts

A raw number like `(0.20, -6.97, 6.87, 1.1, -0.4, 0.3)` from `sensors.bmi270.motion()` doesn't tell a person anything yet. The **Processing** stage turns it into a meaningful quantity through three beats: **raw → derived → viz** (read raw → compute → display). This lesson's four quantities all share the same skeleton, differing only in the formula in the middle. `dsp` computes on the C side, so it's fast — two quantities have ready-made functions, and we write the formula for the other two ourselves.

**Tilt angle:** the accelerometer measures gravity's vector, which always points toward the ground. When the board tilts, this force spreads across three axes, and we recover the angle with $\text{roll} = \operatorname{atan2}(a_y, a_z)$ and $\text{pitch} = \operatorname{atan2}(-a_x, \sqrt{a_y^2 + a_z^2})$ — the exact same formula `dsp.tilt(ax, ay, az)` uses, returning **(roll, pitch)** in degrees (roll first). The formula is a ratio of axes, so the unit cancels out, and atan2 knows the quadrant, giving a full-range angle with no division-by-zero problem.

**Motion energy:** `motion()` returns acceleration in m/s² (at rest ≈ 9.81). Dividing the vector's magnitude by 9.81 gives units of g: $|a| = \sqrt{a_x^2 + a_y^2 + a_z^2} / 9.81$. At rest, this is about 1 g, so we subtract 1: `energy = abs(mag - 1.0)`, making "still = 0", leaving only the part caused by movement. **Altitude:** air pressure drops with height. `dsp.altitude(p, p0)` uses the barometric formula against a reference pressure `p0`, captured once before the loop, giving a relative altitude — raising the board 1 metre raises the value by about +1.0 (if p0 isn't given, it's compared against 1013.25 hPa). **Sound level:** $\text{rms} = \sqrt{\frac{1}{N}\sum s_i^2}$, then $\text{dBFS} = 20\log_{10}(\text{rms}/32768)$ — using 20 because RMS is an amplitude, and a log scale because human ears perceive loudness logarithmically. The decibel scale squeezes the wide range from −96 to 0 into something easy to read.

The viz step is choosing the picture that matches the data: `Seg7` for a prominent number, `Bar` for a level against a 0..100 range, `Chart` for a trend over time, and `Arc` for an angle. Every quantity is normalized into the 0..100 range with `clamp100` before feeding Bar and Chart.

## Worked example

This lesson's examples are physics apps using the same raw → derived → viz skeleton: `03_baro_pressure_altitude.py` shows pressure with a trend graph (storing hPa × 10, since Chart accepts integers), while `09_radar_theremin.py` converts a hand's distance from the radar into a musical note with `ui.tone`. Try **predicting** before running each one: what quantity does it turn the raw value into?

| File | What this file teaches |
|---|---|
| [examples/03_baro_pressure_altitude.py](examples/03_baro_pressure_altitude.py) | DPS368: a pressure display + trend graph + high/low stats |
| [examples/09_radar_theremin.py](examples/09_radar_theremin.py) | Radar Theremin: hand distance = a musical note (J8 speaker) + a pitch gauge on screen |

This lesson's slides also reference files in another lesson and under `shared/`:

- [m03-processing/l02-physics-gauges-lab/examples/s06_physics_viz_full.py](../l02-physics-gauges-lab/examples/s06_physics_viz_full.py) — Physics Lab: raw -> derived -> viz (full version)
- [m03-processing/l02-physics-gauges-lab/practice/s06_physics_viz.py](../l02-physics-gauges-lab/practice/s06_physics_viz.py) — Physics Lab: raw -> derived -> viz (the fill-in-the-code version)
- [shared/interactive/math_lab.html](../../shared/interactive/math_lab.html)

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. Which quantities in this lesson have a ready-made function in dsp? (select every correct answer) *(multiple choice · objective 1)*
   - a) Tilt angle (dsp.tilt)
   - b) Altitude (dsp.altitude)
   - c) Motion energy
   - d) Sound level (dBFS)

   <details><summary>Solution</summary>

   **a, b** — tilt and altitude exist in the dsp module; energy and dBFS we write ourselves with math.sqrt and math.log10.

   </details>

2. ax = 0, ay = 6.9, az = 6.9 m/s². What is roll = atan2(ay, az)? *(single choice · objective 2)*
   - a) 0 degrees
   - b) 45 degrees
   - c) 90 degrees
   - d) Can't be computed without converting to g first

   <details><summary>Solution</summary>

   **b** — atan2(6.9, 6.9) = 45°. The formula is a ratio, so units cancel out — m/s² or g both give the same angle.

   </details>

3. The board lies still, so motion() gives |a| ≈ 9.81 m/s². If you write energy = abs(mag - 1.0) without dividing by 9.81, what do you get? *(single choice · objective 3)*
   - a) About 0, as intended
   - b) About 8.8 — the bar stays full even while still
   - c) About −1
   - d) An error, because math.sqrt can't accept a negative value

   <details><summary>Solution</summary>

   **b** — you must divide by 9.81 to get units of g first. At rest, mag ≈ 1, and subtracting 1 leaves about 0.

   </details>

4. Why capture pressure p0 once before the loop, and pass it into dsp.altitude(p, p0)? *(single choice · objective 3)*
   - a) Because dsp.altitude always needs two values
   - b) To get a relative altitude against the starting point, which clearly shows the board being lifted, independent of that day's weather
   - c) To warm up the sensor
   - d) To convert hPa to kPa

   <details><summary>Solution</summary>

   **b** — p0 is an optional argument. Without it, altitude is compared against 1013.25 hPa, giving height above sea level that depends on the weather. Supplying your own p0 puts zero at the moment the program starts.

   </details>

5. Why does sound level use the dBFS (log) scale instead of the RMS value directly? *(single choice · objective 4)*
   - a) Because log computes faster
   - b) Because ears perceive loudness logarithmically, and sound's range is very wide — log keeps quiet sounds from being squeezed unreadable
   - c) Because RMS can be negative
   - d) Because Bar only accepts negative values

   <details><summary>Solution</summary>

   **b** — the decibel scale compresses a wide range, roughly −96 to 0 dBFS, into something easy to read, the same way the Richter scale or pH does.

   </details>

## Lab

- [ ] Compute the roll angle of (ax, ay, az) = (0, −6.97, 6.87) m/s² by hand or with a calculator, and compare it against `dsp.tilt` in the REPL.
- [ ] With the board lying still, compute energy both dividing by 9.81 and without, and note in your learning log how they differ.
- [ ] If you have a board, raise and lower it by one metre and watch how much `dsp.altitude(p, p0)` changes.

## Going further

In lesson 3.2, we'll fill in four formulas in the `s06_physics_viz.py` file and watch all four gauges move with real motion.

Next lesson: [lesson 3.2 — Hands-on: four physics gauges on screen](../l02-physics-gauges-lab/README.md)

## Reflect

- What devices around you convert raw numbers into quantities the same way this lesson does — a step counter, or a phone that knows which floor it's on?
- If you had to show air pressure to an everyday person, which widget would you choose, and why?
