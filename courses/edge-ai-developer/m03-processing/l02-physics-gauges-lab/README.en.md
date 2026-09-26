---
id: edgeai-dev.m03.l02
lang: en
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
source_sha256: ee57849e2d6a6f6d9360e88bf036f70b019a7a215fb70b385f6f67e3180fab6f
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 3.2 — Hands-on: four physics gauges on screen

> Module 3 — Processing with maths and physics · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Fill the four conversion formulas in s06_physics_viz.py (tilt, energy, altitude, dBFS), then pick a quantity from the dropdown, move, lift or make noise, until the Seg7, bar and chart move with the values we computed ourselves.

## Objectives

By the end of this lesson, you will:

1. Fill the four formulas in practice/s06_physics_viz.py until at least three quantities (Tilt, Energy, Altitude) show values that follow real motion on the emulator or the board.
2. Test the energy formula so it reads about 0 at rest and above 1 when shaken hard, and explain why it must divide by 9.81 and subtract 1 g.
3. Explain the role of the placeholders in the practice file, capturing p0 before the loop, and releasing the microphone with pdm.deinit() in finally.

## Before you start

You've been through lesson 3.1, and understand the four formulas and the reasoning behind dividing by 9.81. Fill in one formula at a time and test one quantity at a time — this catches bugs more easily than filling everything in at once.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — Tilt, Energy and Altitude work fully on the emulator; Sound on the emulator is synthetic. Real sound needs a board whose PDM microphone works (see the TESAIoT Dev Kit's limitation in lesson 2.3).
- **Prior lesson:** [lesson 3.1 — From raw numbers to physical quantities: tilt angle, energy, altitude and dBFS](../l01-physics-quantities/README.md)

## Concepts

The whole file reads as one sentence: choose a quantity → read the raw value → compute it into a real quantity → send it to Seg7, Bar and Chart → loop every 120 ms. The top of the file creates widgets once, tries opening the mic inside a `try` to set `has_mic`, and captures `p0` before the loop — all of this is already given. Our job is the four formulas in the middle (the derived beat). The practice file leaves placeholders such as `roll, pitch = 0.0, 0.0` or `db = -96.0` so it runs (showing 0) even before you fill anything in — the values only move once you fill in the real formula, the same technique as `r = None` in lesson 1.3.

The four formulas are: (1) `roll, pitch = dsp.tilt(ax, ay, az)` (2) `mag = math.sqrt(ax*ax + ay*ay + az*az) / 9.81`, then `energy = abs(mag - 1.0)` (3) `alt = dsp.altitude(p, p0)` and (4) `db = 20 * math.log10(rms / 32768.0)` inside `if rms > 0:`, because log10(0) can't be computed. Watch the order `dsp.tilt` returns (roll before pitch), and remember `motion()` gives units of m/s² — if you forget to divide by 9.81, energy stays stuck around 8.8 even at rest. Pressure is sensitive to wind and air conditioning, so the altitude value naturally jitters a little — we'll filter it steady in module 4.

Once everything's filled in, the `Chart` keeps a history for you. Try shaking rhythmically and watch the waveform — you'll see "the shape of the motion" much more clearly than a plain still number. Success isn't just the numbers moving — you should be able to say what energy 0.8 actually means, and why tilt can use atan2 without ever needing to know accel's unit.

## Worked example

`s06_physics_viz_full.py` adds remembering the highest and lowest values (hi/lo hold), a STEADY/ACTIVE label, and a Reset button. Run it before starting the lesson to see where you're headed, then come back and read it again once your practice file passes.

| File | What this file teaches |
|---|---|
| [examples/s06_physics_viz_full.py](examples/s06_physics_viz_full.py) | Physics Lab: raw -> derived -> viz (full version) |

## Practice

The 4 `# TODO:` comments are at lines 94, 103, 112 and 125 (Tilt, Energy, Altitude, dBFS). Replace the placeholders with the formulas the hints describe, then press Run (emulator) or Program to Device (board). If a gauge stays stuck at 0, check that you filled in the formula line and didn't leave a placeholder overwriting it afterward.

| Practice file | Topic |
|---|---|
| [practice/s06_physics_viz.py](practice/s06_physics_viz.py) | Physics Lab: raw -> derived -> viz (the fill-in-the-code version) |

## Solution

Open the solution after trying on your own at least once, and read [how to use the solutions](../../README.en.md#how-to-use-the-solutions) first.

| Solution | Pairs with |
|---|---|
| [solution/s06_physics_viz.py](solution/s06_physics_viz.py) | [practice/s06_physics_viz.py](practice/s06_physics_viz.py) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. You filled in the Tilt formula, but the angle gauge stays stuck at 0 every time. What's the likely cause? *(single choice · objective 1)*
   - a) You haven't replaced pass yet, or a placeholder line roll, pitch = 0.0, 0.0 still remains after the formula
   - b) dsp.tilt only works on a board
   - c) You must divide by 9.81 before calling dsp.tilt
   - d) Chart can't accept values above 100

   <details><summary>Solution</summary>

   **a** — the placeholder exists to let the file run before you fill anything in. If it's still overwriting the value after your formula, the gauge stays at 0 forever. dsp.tilt, on the other hand, needs no unit conversion first.

   </details>

2. With the board lying still, Energy reads 8.81 constantly. How should the formula be fixed? *(single choice · objective 2)*
   - a) Change abs to max
   - b) Divide the vector's magnitude by 9.81 to get units of g, before subtracting 1.0
   - c) Remove the subtraction of 1.0 from the formula
   - d) Use gx, gy, gz instead of ax, ay, az

   <details><summary>Solution</summary>

   **b** — motion() gives m/s², so at rest the magnitude is about 9.81. Dividing by 9.81 gives about 1 g, and subtracting 1 leaves about 0.

   </details>

3. energy (in g) is converted into a bar with clamp100(energy / 2.0 * 100). If energy = 0.5, where does the bar sit? *(single choice · objective 2)*
   - a) 5
   - b) 25
   - c) 50
   - d) 100

   <details><summary>Solution</summary>

   **b** — 0.5 / 2.0 × 100 = 25. The range 0..2g is mapped onto a 0..100 bar; anything above 2g gets clamped to 100.

   </details>

4. Which of these are true about the parts already given in the practice file? (select every correct answer) *(multiple choice · objective 3)*
   - a) p0 is captured once before the loop, because it's a reference point that doesn't change
   - b) pdm.deinit() sits in finally, so the microphone is always released no matter how you exit
   - c) The placeholders let the file run and show 0 before anything's filled in
   - d) Widgets are recreated inside the loop every 120 ms

   <details><summary>Solution</summary>

   **a, b, c** — widgets are created once before the loop, per the shared skeleton, with only their values changing inside it. The other three are correct set-up before the loop and correct cleanup.

   </details>

## Lab

**The MVP for lessons 3.1–3.2:** a raw signal → a computed quantity → shown on screen, the full loop working for at least one quantity.

- [ ] All four formulas in the practice file are filled in, and it runs on the emulator or the board.
- [ ] Test at least three quantities (Tilt → Energy → Altitude), and note in your learning log what you had to do to see each value clearly change.
- [ ] Find Energy's reference value at rest, then temporarily remove `- 1.0` and see what the value at rest becomes, and explain why.
- [ ] Be able to explain what quantity and unit each formula you filled in converts the raw number into.

## Going further

In the next pair of lessons (3.3–3.4), we'll take the quantities we've computed and judge them with rules — such as "comfortable" or "hot" from temperature and humidity.

Next lesson: [lesson 3.3 — Derived values and rule-based classification: dew point, heat index and a rule ladder](../l03-rules-before-ml/README.md)

## Reflect

- Which quantity does the Chart tell a better story with than a plain Seg7 number, and why?
- If you had to use the energy value to decide "someone picked up the board," what threshold would you set, and how would you test that threshold?
