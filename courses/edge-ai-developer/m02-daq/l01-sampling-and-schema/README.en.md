---
id: edgeai-dev.m02.l01
lang: en
title: {th: 'สุ่มสัญญาณให้ตรงกับโมเดล: อัตราสุ่ม Nyquist หน้าต่าง และ schema ของ CSV', en: 'Sampling to match the model: rate, Nyquist, windows and the CSV schema'}
summary: {th: เริ่มวงจรจากต้นน้ำ เข้าใจว่า DAQ คืออะไร ทำไมอัตราสุ่มต้องคงที่และต้องตรงกับที่โมเดลกิน (50 Hz) ใช้กฎ Nyquist กับสูตรความยาวหน้าต่าง T = N/fs และออกแบบ schema ของไฟล์ CSV ที่เขียนลง flash บนบอร์ด, en: 'Start the cycle upstream - learn what DAQ is, why the sampling rate must be steady and match what the model was trained on (50 Hz), use the Nyquist rule and the window length T = N/fs, and design the CSV schema written to the board''s flash.'}
level: L3
time_min: {concept: 40, practise: 10, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m01.l07]
objectives:
  - {th: 'อธิบายได้ว่าทำไม DAQ เป็นขั้นที่ 1 ของวงจรข้อมูล และยกปัจจัยที่ทำให้ dataset เสีย (garbage in, garbage out) ได้อย่างน้อยสามข้อ', en: 'Explain why DAQ is stage 1 of the data cycle and name at least three things that spoil a dataset (garbage in, garbage out).'}
  - {th: ใช้กฎ Nyquist fs ≥ 2·fmax ตัดสินว่าอัตราสุ่มที่กำหนดพอสำหรับสัญญาณหนึ่งหรือไม่ และคำนวณความยาวของหนึ่ง burst ด้วย T = N/fs, en: 'Use the Nyquist rule fs ≥ 2·fmax to judge whether a sampling rate is enough for a signal, and compute the length of one burst with T = N/fs.'}
  - {th: อธิบายได้ว่าทำไม logger ต้องสุ่มที่ 50 Hz ให้ตรงกับโมเดล Motion บนบอร์ด และจะเกิดอะไรกับรูปคลื่นถ้าเก็บที่อัตราอื่น, en: 'Explain why the logger samples at 50 Hz to match the Motion model on the board, and what happens to the waveform if you record at another rate.'}
  - {th: 'เขียน schema label,ax,ay,az,gx,gy,gz และบรรทัด CSV หนึ่ง sample ได้ถูก และเลือกโหมดเปิดไฟล์ "a" หรือ "w" ได้เหมาะกับสถานการณ์', en: 'Write the schema label,ax,ay,az,gx,gy,gz and a one-sample CSV line correctly, and choose the "a" or "w" file mode for the situation.'}
develops: [{skill: ai.data-collection, to: 2}, {skill: sys.dsp, to: 1}, {skill: sys.memory-fs, to: 1}, {skill: sys.sensors-actuators, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
source_sha256: 2a772f21108fc3ccf9621e9a040f2cb22b029a06a0a0ef2e2ba845889147d757
---

# Lesson 2.1 — Sampling to match the model: rate, Nyquist, windows and the CSV schema

> Module 2 — Collecting sensor data (DAQ) · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Start the cycle upstream: understand what DAQ is, why the sampling rate must be steady and match what the model was trained on (50 Hz), use the Nyquist rule and the window-length formula T = N/fs, and design the CSV schema written to the board's flash.

## Objectives

By the end of this lesson, you will:

1. Explain why DAQ is stage 1 of the data cycle, and name at least three things that spoil a dataset (garbage in, garbage out).
2. Use the Nyquist rule fs ≥ 2·fmax to judge whether a given sampling rate is enough for a signal, and compute the length of one burst with T = N/fs.
3. Explain why the logger samples at 50 Hz to match the Motion model on the board, and what happens to the waveform if you record at another rate.
4. Write the schema label,ax,ay,az,gx,gy,gz and a one-sample CSV line correctly, and choose the "a" or "w" file mode for the situation.

## Before you start

You've been through module 1, and know the four-beat skeleton and `sensors.bmi270.motion()`. Keep BENTO IDE's REPL open, and try calling `sensors.bmi270.motion()` while still, compared with while shaking.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/)
- **Prior lesson:** [lesson 1.7 — Hands-on: from verdict to action on the board](../../m01-onboarding/l07-verdict-action-lab/README.md)

## Concepts

**DAQ (Data Acquisition)** means collecting raw sensor data into a set you can store, search, and use later — the starting raw material for every model. The Motion model we played with in module 1 came into being because someone shook a sensor and collected thousands of samples first. A dataset's quality depends on correct labels, a steady sampling rate, balanced classes, and variety in real-world conditions. Garbage in, garbage out.

**The sampling rate** is how many times per second the sensor is read. 50 Hz means reading every 20 ms, so the file sets `RATE_MS = 20` — not a random number, but exactly the rate the Motion model on the board was trained on. Recording at a different rate stretches or shrinks the waveform, so it no longer looks like what the model has seen. The **Nyquist** rule says you must sample at least twice the highest frequency you want to capture, $f_s \ge 2 f_{max}$ — otherwise a fast signal disguises itself as a fake slow wave (aliasing). One burst's length is $T = N / f_s$ — for example, `BURST = 200` at 50 Hz gives 4 seconds, long enough to complete a full motion, since a motion is a pattern over time — the model has to see many samples in a row to tell circle apart from shaking.

The CSV **schema** is the first line, `label,ax,ay,az,gx,gy,gz` — a contract between whoever collects the data and whoever trains on it. Every following line is one snapshot of the IMU's six axes with the motion's name attached. The file is written to the board's flash (LittleFS) with `open()`/`write()`, the same way as Python on a computer. Mode `"a"` appends; `"w"` overwrites. Only use `"w"` when you're certain the file doesn't exist yet. Before writing code, it's worth querying the sensor in the REPL first, to see what "still" and "shaking" values actually look like, so you can tell whether what lands in the file "makes sense."

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. Which of these spoil a dataset even though the program never throws an error? (select every correct answer) *(multiple choice · objective 1)*
   - a) Pressing the shaking button while the board sits still
   - b) Collecting 1000 idle samples but only 50 shaking samples
   - c) A sampling rate that drifts, sometimes fast, sometimes slow
   - d) Collecting many people doing many motions, for variety

   <details><summary>Solution</summary>

   **a, b, c** — a wrong label, unbalanced classes, and an unsteady rate all quietly teach the model the wrong thing. Variety in real-world conditions, on the other hand, makes a model more robust.

   </details>

2. A hand shake tops out around 10 Hz. What's the minimum sampling rate the Nyquist rule requires? *(single choice · objective 2)*
   - a) 5 Hz
   - b) 10 Hz
   - c) 20 Hz
   - d) 100 Hz

   <details><summary>Solution</summary>

   **c** — fs ≥ 2·fmax = 2 × 10 = 20 Hz. Below this, aliasing occurs. Recording at 50 Hz leaves comfortable headroom.

   </details>

3. Collecting N = 150 samples at fs = 50 Hz, how long is one burst? *(single choice · objective 2)*
   - a) 0.33 seconds
   - b) 3 seconds
   - c) 7.5 seconds
   - d) 200 seconds

   <details><summary>Solution</summary>

   **b** — T = N / fs = 150 / 50 = 3 seconds.

   </details>

4. If you collect a dataset at 25 Hz, then train or compare against a model trained at 50 Hz, what's the problem? *(single choice · objective 3)*
   - a) No problem, since each sample's value is still the same
   - b) The waveform over time is spaced out and stretched differently from what the model has seen, so it may predict wrong
   - c) The file becomes twice as large
   - d) The board can no longer write the file

   <details><summary>Solution</summary>

   **b** — the sampling rate used while collecting data must match the rate used in actual deployment. This is a core rule of edge AI: no matter how good a dataset looks, it's useless if the rate doesn't match.

   </details>

5. A logger is used to record three bursts, but the file ends up with only the last burst. What's the likely cause? *(single choice · objective 4)*
   - a) The file is opened inside the recording loop with mode "w", which overwrites it every time, instead of using "a"
   - b) Forgot to write \n at the end of each line
   - c) Called motion() instead of acceleration()
   - d) Flash is full

   <details><summary>Solution</summary>

   **a** — mode "a" appends without erasing old content. Use "w" only when creating a brand new file with its header row.

   </details>

## Lab

- [ ] In the REPL, call `sensors.bmi270.motion()` while still and while shaking, and note the values in your learning log.
- [ ] Compute T = N/fs for BURST = 200 at 50 Hz, and at 25 Hz.
- [ ] Write the schema and one example line, by hand, from a sample you actually read.

## Going further

In lesson 2.2, we'll write a real logger following the four beats — schema → sample → record → rate — and collect our first dataset file.

Next lesson: [lesson 2.2 — Hands-on: a DAQ logger that saves a dataset to CSV](../l02-daq-logger-lab/README.md)

## Reflect

- If your sensor captures a signal that oscillates as fast as 12 Hz, what sampling rate would you set, and why not set it higher than necessary?
- What effect does one wrongly labelled burst have on a model, among thousands of lines in a dataset?
