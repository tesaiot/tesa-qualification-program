---
id: edgeai-dev.m01.l04
lang: en
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
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
source_sha256: 10a6156e5fde0ac4cf2ef98b297be7b4416f1b0f4c8faa2c61b8fe8d177b56ec
---

# Lesson 1.4 — Taking a sensor app apart: the four-beat skeleton of every program

> Module 1 — Getting started: run the real thing, then take it apart · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Take three working sensor apps apart until the shared four-beat skeleton shows — import → create widgets once → a read-compute-draw loop → ui.poll with a back button — and meet sensors.bmi270.motion, sensors.radar and dsp.tilt.

## Objectives

By the end of this lesson, you will:

1. Place each line of 01_imu_6axis.py, 02_imu_tilt_fusion.py and 04_radar_presence.py in one of the four beats, and state how the three apps differ in the read, compute and draw slots.
2. Explain why widgets are created before the loop and the screen is redrawn only when a value changes, naming at least two harms of doing the opposite.
3. Read sensors.bmi270.motion() and sensors.radar(), state the accel (m/s²) and gyro (dps) units, compute the acceleration magnitude |a|, and turn accel into roll and pitch with dsp.tilt.

## Before you start

You've been through lessons 1.1–1.3. This lesson builds on the program skeleton you glimpsed in lesson 1.3. Keep `01_imu_6axis.py` and `04_radar_presence.py` open in BENTO IDE.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — real radar exists on the TESAIoT Dev Kit; on the emulator, the radar's presence value is simulated with the Shake button.
- **Prior lesson:** [lesson 1.3 — Hands-on: your first model menu](../l03-first-inference-lab/README.md)

## See it work first

Always run the real thing before taking it apart: run `01_imu_6axis.py` and move or shake the board — the six-axis numbers and the |a| bar follow along. Then run `04_radar_presence.py`, and compare sitting still in front of the board with stepping out of range: the label switches from CLEAR to PRESENCE.

## Concepts

The three apps — `01` (six-axis numbers), `02` (a tilt-angle gauge), and `04` (a present-or-not label) — use different sensors and different screens, but all follow the **same four beats**: (1) import the modules and call `ui.screen()` right away; (2) create every widget before the loop, keeping a variable for any one whose value will change; (3) a loop that reads → computes → draws, then pauses with `time.sleep_ms(100)`; (4) a non-blocking `ui.poll()` that, on finding the back button's handle, does `raise KeyboardInterrupt` to exit and clean up in an `except`. Beats 1–2 run once; beats 3–4 repeat until you exit. Once you can see this skeleton, reading new code gets much faster, because you know exactly where to look for each thing.

The rule most often broken is: **what "is" gets created before the loop; what "changes" happens inside the loop.** If a widget is created inside the loop, the screen flickers, and widgets pile up until memory runs out. Another habit, from `04`, is to **only redraw when a value changes**, by keeping the last-drawn value to compare against (`last`, `was`, `last_seq`), which keeps the screen steady and doesn't unnecessarily saturate the cross-core communication channel. A deadzone helps further, so tiny jitters in the angle near zero don't make the needle twitch.

`sensors.bmi270.motion()` returns `(ax, ay, az, gx, gy, gz)` in one call, so every axis comes from the same instant. Accel is in m/s² (lying flat, `az` ≈ 9.8); gyro is in degrees per second. The vector magnitude $|a| = \sqrt{a_x^2 + a_y^2 + a_z^2}$ collapses three axes into one number — around 9.8 at rest, spiking when shaken. `sensors.radar()` returns a dict with `presence` and `energy`. And `dsp.tilt(ax, ay, az)` computes `(roll, pitch)` in degrees for you, in C, because heavy maths should be handed off to C, leaving MicroPython to handle logic and the screen.

## Worked example

Follow PRIMM: **Predict** what each app shows before running it → **Run** it → **Investigate** with the three-app comparison table in the slides. `02_imu_tilt_fusion.py` is the tilt-angle gauge app that uses `dsp.tilt`, and is the template for the Tilt Monitor in lesson 1.5.

| File | What this file teaches |
|---|---|
| [examples/01_imu_6axis.py](examples/01_imu_6axis.py) | IMU BMI270: a six-axis dashboard on screen |
| [examples/04_radar_presence.py](examples/04_radar_presence.py) | Radar: a large status label that changes colour when someone is detected (event-driven) |
| [examples/02_imu_tilt_fusion.py](examples/02_imu_tilt_fusion.py) | Tilt angle: a pair of arc gauges (pitch / roll) plus Seg7 digits |

This lesson's slides also reference a file in another lesson:

- [m01-onboarding/l05-sensor-remix-lab/practice/s02_anatomy_sensor.py](../l05-sensor-remix-lab/practice/s02_anatomy_sensor.py) — taking apart a sensor app's structure, then remixing it yourself (the fill-in-the-code version)

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. Which part of apps 01, 02 and 04 is identical, line for line, enough to copy across apps directly? *(single choice · objective 1)*
   - a) The sensor-reading slot
   - b) The computation slot
   - c) The ui.poll loop with the back button that raises KeyboardInterrupt
   - d) The kind of widget created

   <details><summary>Solution</summary>

   **c** — the three-app comparison table shows they only differ in "what's read, what's computed, what it's drawn with". The poll loop and the back button are exactly identical.

   </details>

2. If you accidentally create a new ui.Seg7 every round inside the loop, what happens? (select every correct answer) *(multiple choice · objective 2)*
   - a) The screen flickers, because it's redrawn on top of itself every frame
   - b) Old widgets pile up until memory runs out and it hangs
   - c) The loop gets faster, since there's no variable to keep
   - d) The sensor's values become more accurate

   <details><summary>Solution</summary>

   **a, b** — create a widget once before the loop, then just change its value inside the loop, such as seg.text("42"), which keeps the screen steady and memory usage constant.

   </details>

3. In 04_radar_presence.py, what does the line `if now != was` do? *(single choice · objective 2)*
   - a) Stops the loop when no one is present
   - b) Only redraws the screen when the status changes; leaves it untouched when the value is the same
   - c) Restarts the radar every round
   - d) Waits until someone walks in

   <details><summary>Solution</summary>

   **b** — this is event-driven drawing: it keeps the latest status in `was`, and only redraws when the new value differs from it.

   </details>

4. With the board lying flat and still on a table, which values from sensors.bmi270.motion() make the most sense? *(single choice · objective 3)*
   - a) ax ≈ 9.8, ay ≈ 0, az ≈ 0
   - b) ax ≈ 0, ay ≈ 0, az ≈ 9.8, and all three gyro axes near 0
   - c) Every axis is 0, because the board isn't moving
   - d) az ≈ 1.0, because the unit is g

   <details><summary>Solution</summary>

   **b** — accel is in m/s² and also measures gravity, so the axis perpendicular to the ground reads around 9.8. Gyro measures rotation, which is near 0 when still.

   </details>

5. If ax = 0, ay = 6, az = 8 m/s², what is |a|? *(single choice · objective 3)*
   - a) 14
   - b) 10
   - c) 7
   - d) 100

   <details><summary>Solution</summary>

   **b** — |a| = √(0² + 6² + 8²) = √100 = 10 m/s², a 3D Pythagorean calculation. A value close to 9.8 means the board is barely accelerating — it's mostly gravity split across two axes.

   </details>

## Lab

- [ ] Run `01` and `04` (if you have a board), and note what changes on screen as you move or approach it.
- [ ] Write a four-beat table for all three apps in your learning log — which slots are identical line for line, and which differ.
- [ ] Lay the board flat and read |a| until it's close to 9.8, then tilt it and observe how gravity spreads across ax and ay.

## Going further

In lesson 1.5, we'll remix these three apps into our own Tilt Monitor by filling in four blanks in a practice file.

Next lesson: [lesson 1.5 — Hands-on: our own Tilt Monitor remix](../l05-sensor-remix-lab/README.md)

## Reflect

- If you had to change app `01` to read radar instead of the IMU, which beats would you need to change, and which wouldn't need touching at all?
- Why does reading all six axes in one call matter for computing the angle?
