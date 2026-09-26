---
id: edgeai-dev.m02.l04
lang: en
title: {th: 'ลงมือทำ: เก็บ IMU กับเสียงลงไฟล์เดียว', en: 'Hands-on: IMU and sound in one file'}
summary: {th: เติมสี่ก้าวในลูปของ s05_multicapture.py คือประทับเวลา อ่าน IMU อ่านเสียง และเขียนแถว จนได้ /multicapture.csv ที่ทุกแถวมัด IMU กับระดับเสียงบน t_ms เดียวกัน แล้วตรวจไฟล์และ jitter ด้วยตัวเอง, en: 'Fill the four loop steps of s05_multicapture.py (timestamp, read IMU, read sound, write the row) until /multicapture.csv ties IMU and sound level to one t_ms on every row, then check the file and the jitter yourself.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m02.l03]
objectives:
  - {th: 'เติมสี่ช่องใน practice/s05_multicapture.py จนการกดปุ่ม label หนึ่งครั้งเพิ่ม 200 แถวลง /multicapture.csv ที่มีคอลัมน์ t_ms, label, ax..gz และ db ครบ', en: 'Fill the four blanks in practice/s05_multicapture.py so one label press adds 200 rows to /multicapture.csv with t_ms, label, ax..gz and db columns.'}
  - {th: ตรวจไฟล์ที่เก็บได้ว่า t_ms เพิ่มขึ้นต่อชุดและห่างกันราว 20 ms ค่า db เปลี่ยนตามเสียงจริง และวินิจฉัยได้ว่าช่องใดยังว่างจากอาการในไฟล์, en: Check the recorded file - t_ms rises within each burst about 20 ms apart and db follows real sound - and diagnose which blank is empty from the symptoms in the file.}
  - {th: อธิบายได้ว่าทำไมต้องเปิด PDM นอกลูปครั้งเดียว และคืนไมโครโฟนด้วย pdm.deinit() ในบล็อก finally, en: Explain why the PDM is opened once outside the loop and released with pdm.deinit() in the finally block.}
develops: [{skill: ai.data-collection, to: 2}, {skill: lang.micropython, to: 2}, {skill: sys.sensors-actuators, to: 2}]
assesses: [{skill: ai.data-collection, level: 2, evidence: practice/s05_multicapture.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: 732b9fe980a669a8cc1e3464b21775e74b55f5904a2c4bc6b5a1953f24006221
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 2.4 — Hands-on: IMU and sound in one file

> Module 2 — Collecting sensor data (DAQ) · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Fill the four loop steps of s05_multicapture.py — timestamp, read IMU, read sound, write the row — until /multicapture.csv ties the IMU and sound level to the same t_ms on every row, then check the file and the jitter yourself.

## Objectives

By the end of this lesson, you will:

1. Fill the four blanks in practice/s05_multicapture.py so one label press adds 200 rows to /multicapture.csv, complete with t_ms, label, ax..gz and db columns.
2. Check a recorded file: t_ms rises within each burst, about 20 ms apart, db follows real sound, and diagnose which blank is empty from the symptoms in the file.
3. Explain why the PDM is opened once outside the loop, and released with pdm.deinit() in the finally block.

## Before you start

You've been through lesson 2.3, and understand dBFS, a shared timeline, and jitter. Have a board that can record audio ready, and keep the REPL open to check the file once you're done recording.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — recording real audio needs a board whose PDM microphone works (the author tested on the PSoC Edge AI Kit; on the TESAIoT Dev Kit, enabling PDM still conflicts with the audio system's clock). The emulator gives synthetic audio, good for practising the program's skeleton, but passing on the emulator is not evidence it will pass on the board.
- **Prior lesson:** [lesson 2.3 — Audio and several sensors on one timeline: 16 kHz PDM, timestamps and jitter](../l03-audio-and-timeline/README.md)

## Concepts

The whole file's heart is in `record()`. Each round of `for _ in range(BURST)` follows exactly four steps: (1) timestamp — `t_ms = time.ticks_diff(time.ticks_ms(), t0)` (2) read the IMU — `ax, ay, az, gx, gy, gz = sensors.bmi270.motion()` (3) read sound — `pdm.readinto(buf)`, then `db = dbfs(buf)`, already given (4) write the row — `f.write("%d,%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.1f\n" % (t_ms, label, ax, ay, az, gx, gy, gz, db))`. All four steps happen in one round, before `time.sleep_ms(RATE_MS)`, so they count as the same instant. Order matters: always read both sensors before writing the row, or the data drifts a round out of alignment.

The top of the file is already given: it opens `PDM_PCM(0, sck="P8_5", data="P8_6", sample_rate=16000)` **once, outside the loop**, just like creating a widget once, because opening and closing it repeatedly both costs time and risks conflicts. It prepares a buffer and writes the header if the file doesn't exist yet. `t0` is reset every time a label button is pressed, so each burst starts counting time from its own zero. On exit, the `finally` block always calls `pdm.deinit()` to release the microphone — otherwise the next audio program might fail to open PDM because the hardware is still reserved.

Once you've recorded, **check before trusting**: the row count should equal `BURST × number of presses`, `t_ms` should rise within each burst, and `db` should follow real sound. If `t_ms` is 0 on every row, step 1 is still empty. If `db` never moves, step 3 is still empty, or the mic isn't picking up sound. If the file is empty, step 4 is still empty.

## Worked example

`s05_multicapture_full.py` records both CSV and a paired raw-audio WAV, measures the real interval per row and the worst-case jitter, then summarizes the row count, peak dBFS and average interval per label into a manifest file. Open it once your practice file is working, to see what a production-grade dataset needs to record on top of this.

| File | What this file teaches |
|---|---|
| [examples/s05_multicapture_full.py](examples/s05_multicapture_full.py) | Multi-Sensor Sync Capture (full version) |

## Practice

The file has 4 `# TODO` spots, at lines 78, 83, 88 and 92, matching the four steps in order. Replace `pass` (and the zero placeholder values) with the calls the hints describe. Then Program to Device, choose a label, perform the motion and make the sound together for about four seconds, watch the row count appear on screen, then open the CSV to check.

| Practice file | Topic |
|---|---|
| [practice/s05_multicapture.py](practice/s05_multicapture.py) | Recording 2 sensors together on one timeline (the fill-in-the-code version) |

## Solution

Open the solution after trying on your own at least once, and read [how to use the solutions](../../README.en.md#how-to-use-the-solutions) first.

| Solution | Pairs with |
|---|---|
| [solution/s05_multicapture.py](solution/s05_multicapture.py) | [practice/s05_multicapture.py](practice/s05_multicapture.py) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. Put the four steps of one round of the record() loop in order *(ordering · objective 1)*
   - a) pdm.readinto(buf), then db = dbfs(buf)
   - b) t_ms = time.ticks_diff(time.ticks_ms(), t0)
   - c) f.write(...) one row
   - d) ax, ay, az, gx, gy, gz = sensors.bmi270.motion()

   <details><summary>Solution</summary>

   **b → d → a → c** — timestamp → read IMU → read sound → write the row, then sleep_ms before the next round. Every value in the row is therefore the same instant.

   </details>

2. You open the CSV and find t_ms is 0 on every row, but the IMU and db values change genuinely. Which blank is still empty? *(single choice · objective 2)*
   - a) Step 1, timestamp
   - b) Step 2, read the IMU
   - c) Step 3, read sound
   - d) Step 4, write the row

   <details><summary>Solution</summary>

   **a** — the placeholder line t_ms = 0 is still there, so the timeline is missing, and rows can't be paired by time. ticks_diff needs to be filled in.

   </details>

3. Every row's db column reads −96.0, even when you clap right next to the board. What's the likely cause? *(single choice · objective 2)*
   - a) pdm.readinto(buf) hasn't been filled in yet, so the buffer is all zeros, or the microphone isn't receiving sound
   - b) RATE_MS is set too high
   - c) Forgot \n at the end of the line
   - d) t0 was never reset

   <details><summary>Solution</summary>

   **a** — dbfs() returns −96.0 when RMS is zero, which happens when the buffer was never filled with real sound.

   </details>

4. Which of these explain why pdm.deinit() must be called in finally? (select every correct answer) *(multiple choice · objective 3)*
   - a) No matter whether you exit via the back button or an error, the microphone is always released
   - b) If it's not released, the next audio program might fail to open PDM because the hardware is still reserved
   - c) deinit() is what causes the CSV file to be saved
   - d) It's the same habit as edge_ai.stop() — always leave the machine in a known state

   <details><summary>Solution</summary>

   **a, b, d** — the CSV file is closed and flushed automatically when leaving the with block; deinit() exists to release the microphone hardware.

   </details>

## Lab

**The MVP for lessons 2.3–2.4:** a dataset logging at least two sensors on one shared timeline. The `/multicapture.csv` file has columns `t_ms` + IMU + `db`, with real values changing with motion and sound.

- [ ] All four blanks in the practice file are filled in; running on the board produces `/multicapture.csv`.
- [ ] Record all three labels, each with a different motion and sound, then confirm in the CSV that `db` and the IMU genuinely change.
- [ ] Check the timeline: are `t_ms` values close to 20 ms apart? Note in your learning log where you found jitter, then try shrinking `CHUNK` and compare.
- [ ] Be able to explain where in the code `t_ms` is stamped, where both sensors are read, and why that must happen in a single round.

## Going further

In the next module (Processing), we'll convert the raw signals we've collected into physical quantities — such as tilt angle, height, and sound level — and show them as live gauges.

Next lesson: [lesson 3.1 — From raw numbers to physical quantities: tilt angle, energy, height and dBFS](../../m03-processing/l01-physics-quantities/README.md)

## Reflect

- When was the worst jitter you measured, and which part of the loop do you think caused it?
- If you had to add a third sensor (such as pressure) into the same file, which parts of the code would you need to change?
