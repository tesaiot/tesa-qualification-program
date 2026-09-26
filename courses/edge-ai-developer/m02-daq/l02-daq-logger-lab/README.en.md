---
id: edgeai-dev.m02.l02
lang: en
title: {th: 'ลงมือทำ: DAQ logger เก็บ dataset ลง CSV', en: 'Hands-on: a DAQ logger that writes a CSV dataset'}
summary: {th: เขียน DAQ logger ตามสี่จังหวะ schema → sample → record → rate จนเก็บ dataset ที่ติด label ลง /gestures.csv บนบอร์ด แล้วตรวจไฟล์ วัดอัตราจริง และเข้าใจกับดักเงียบที่ทำให้ dataset เสีย, en: 'Write a DAQ logger in four beats (schema, sample, record, rate) until it stores a labelled dataset in /gestures.csv on the board, then check the file, measure the real rate and learn the silent traps that spoil a dataset.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m02.l01]
objectives:
  - {th: 'เติมสี่ช่องใน practice/s04_daq_logger.py จนกดปุ่ม label หนึ่งครั้งแล้วได้ 200 บรรทัดใหม่ในไฟล์ ที่ขึ้นต้นด้วยหัวตาราง label,ax,ay,az,gx,gy,gz และค่าไม่เป็นศูนย์หมด', en: 'Fill the four blanks in practice/s04_daq_logger.py so each label press adds 200 new lines to a file headed label,ax,ay,az,gx,gy,gz with values that are not all zero.'}
  - {th: เก็บครบสาม label อย่างน้อยคนละสอง burst แล้วเปิดไฟล์ใน REPL ยืนยันว่าจำนวนบรรทัดเท่ากับ 1 + (จำนวน burst × 200) และแต่ละ label สมดุล, en: 'Record all three labels at least twice each, then open the file in the REPL and confirm the line count equals 1 + (bursts × 200) and the labels are balanced.'}
  - {th: 'อธิบายได้ว่าทำไมอัตราจริงต่ำกว่า 50 Hz ที่ตั้งไว้ และระบุกับดักเงียบสี่ข้อ (โหมด "w", label ผิด, คอลัมน์สลับ, ลืม \n) ได้', en: 'Explain why the real rate is below the 50 Hz set, and name the four silent traps ("w" mode, wrong label, swapped columns, missing \n).'}
develops: [{skill: ai.data-collection, to: 2}, {skill: lang.micropython, to: 2}, {skill: sys.memory-fs, to: 2}]
assesses: [{skill: ai.data-collection, level: 2, evidence: practice/s04_daq_logger.py}, {skill: sys.memory-fs, level: 2, evidence: practice/s04_daq_logger.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: 3017ec57d0ce0755c40630faca989a86ae5e9c21b684e81864aa8ef4075d07a3
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 2.2 — Hands-on: a DAQ logger that writes a CSV dataset

> Module 2 — Collecting sensor data (DAQ) · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Write a DAQ logger following the four beats — schema → sample → record → rate — until it saves a labelled dataset to /gestures.csv on the board, then check the file, measure the real rate, and learn the silent traps that spoil a dataset.

## Objectives

By the end of this lesson, you will:

1. Fill the four blanks in practice/s04_daq_logger.py so that pressing a label button once adds 200 new lines to a file headed with label,ax,ay,az,gx,gy,gz, with values that aren't all zero.
2. Record all three labels, at least two bursts each, then open the file in the REPL and confirm the line count equals 1 + (number of bursts × 200), and that the labels are balanced.
3. Explain why the real rate is below the 50 Hz that was set, and name the four silent traps ("w" mode, a wrong label, swapped columns, a missing \n).

## Before you start

You've been through lesson 2.1, and remember the schema and the reasoning behind 50 Hz. Keep your learning log ready to note the number of bursts per label, and the line count you actually get.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — the emulator fully simulates the IMU, good for practising collection, but data meant for training a real model should come from the board.
- **Prior lesson:** [lesson 2.1 — Sampling to match the model: rate, Nyquist, windows and the CSV schema](../l01-sampling-and-schema/README.md)

## Concepts

The logger follows the same four-beat skeleton, but its loop has **DAQ's own four beats**: **schema** (write the header once if the file doesn't exist yet, using try/except to check first) → **sample** (`sensors.bmi270.motion()`, all six axes in one call) → **record** (`f.write` one line, columns in schema order, ending with `\n`) → **rate** (`time.sleep_ms(RATE_MS)`), looping `BURST` times per press. Every DAQ system in the world follows these same four beats — they differ only in detail. Opening with `with open(PATH, "a")` for each burst closes and flushes the file every time, so unplugging mid-way doesn't lose a burst that already finished writing.

`time.sleep_ms(20)` doesn't give exactly 50 Hz, because each round also spends time reading the sensor and writing the file, so the real rate is a little lower (around 40–45 Hz). What's acceptable is being consistently lower; what's bad is a rate that drifts. The lesson here: **don't trust the value you set — measure what you actually get**, which the full version shows with `time.ticks_diff`.

Record labels that match the Motion model's classes (`idle`, `circle`, `shaking`), keep them balanced, and **check before trusting**, every time: count lines, check the header, check the values. Four traps produce no error at all: opening with `"w"` and overwriting old data, pressing the wrong label button, writing columns out of order, and forgetting `\n`. This skeleton is a template — change only the sample and schema lines, and you can collect a different sensor, such as `sensors.dps368.pressure_temperature()` or `sensors.sht40.temperature_humidity()`, at a much slower rate. This `/gestures.csv` file is the raw material for module 5 (Training).

## Worked example

`s04_daq_logger.py` in the examples folder is the reference version this lesson builds around. `s04_daq_logger_full.py` adds a counter split by label (see class balance live), measures the real rate in Hz, and has a Clear button to wipe the file and start over. Open it for comparison once your practice file is done.

| File | What this file teaches |
|---|---|
| [examples/s04_daq_logger.py](examples/s04_daq_logger.py) | Recording sensor data to a CSV file (Data Acquisition) |
| [examples/s04_daq_logger_full.py](examples/s04_daq_logger_full.py) | Recording a dataset to CSV (full version) |

## Practice

The file has 4 blanks (lines 55, 69, 73 and 76), matching DAQ's four beats exactly: 1) schema: `f.write("label,ax,ay,az,gx,gy,gz\n")` 2) sample: `ax, ay, az, gx, gy, gz = sensors.bmi270.motion()` 3) record: `f.write("%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n" % (label, ax, ay, az, gx, gy, gz))` 4) rate: `time.sleep_ms(RATE_MS)`. If every line is 0.0, blank 2 is still empty. If the file never grows at all, blank 3 is still empty.

| Practice file | Topic |
|---|---|
| [practice/s04_daq_logger.py](practice/s04_daq_logger.py) | Recording sensor data to a CSV file (Data Acquisition) (the fill-in-the-code version) |

## Solution

Open the solution after trying on your own at least once, and read [how to use the solutions](../../README.en.md#how-to-use-the-solutions) first.

| Solution | Pairs with |
|---|---|
| [solution/s04_daq_logger.py](solution/s04_daq_logger.py) | [practice/s04_daq_logger.py](practice/s04_daq_logger.py) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. Put DAQ's four beats in order, as they appear in the logger file *(ordering · objective 1)*
   - a) record: write one line to the file
   - b) schema: write the header once
   - c) rate: time.sleep_ms(RATE_MS)
   - d) sample: sensors.bmi270.motion()

   <details><summary>Solution</summary>

   **b → d → a → c** — schema happens once at the start, then sample → record → rate loop for BURST rounds per press.

   </details>

2. You open the file and every line is 0.0000 except the label column. Which blank is still empty? *(single choice · objective 1)*
   - a) Blank 1, schema
   - b) Blank 2, the sample that reads motion()
   - c) Blank 3, record
   - d) Blank 4, rate

   <details><summary>Solution</summary>

   **b** — the placeholder line ax = ay = ... = 0.0 lets the program run without error, but if the sensor is never actually read, every value stays zero, making the dataset useless.

   </details>

3. You record idle 2 bursts, circle 2 bursts, and shaking 3 bursts. How many lines (including the header) should a correct file have? *(single choice · objective 2)*
   - a) 1400
   - b) 1401
   - c) 1407
   - d) 601

   <details><summary>Solution</summary>

   **b** — 7 bursts × 200 = 1400 data lines, plus 1 header line, giving 1401. And shaking has one more burst than the other classes — worth recording more of the others to balance it.

   </details>

4. You set RATE_MS = 20, but the measured rate is really about 43 Hz. Why? *(single choice · objective 3)*
   - a) The sensor is broken
   - b) Each round also spends time reading the sensor and writing the file, on top of the 20 ms sleep, so one real round takes longer than 20 ms
   - c) time.sleep_ms rounds to whole seconds
   - d) Flash can only be written 43 times per second

   <details><summary>Solution</summary>

   **b** — this is a real fact of embedded work. As long as it's consistently lower, it's still usable. What matters is measuring the real value instead of trusting the one you set.

   </details>

5. Which of these are silent traps where the program runs fine but the dataset is wrong? (select every correct answer) *(multiple choice · objective 3)*
   - a) Writing gx before ax, not matching the schema
   - b) Forgetting \n at the end of a line, so every sample runs together into one line
   - c) Misspelling sensors, causing a NameError
   - d) Opening the file with "w" inside the recording loop

   <details><summary>Solution</summary>

   **a, b, d** — a NameError shows an error right away, so it isn't a silent trap. The other three run fine but produce wrong data — always open the file and check.

   </details>

## Lab

**The MVP for lessons 2.1–2.2:** a logger that genuinely saves N labelled samples to CSV, letting you choose the label, sampling at a steady rate, writing to a file on the board, and verifiable for the correct number of lines.

- [ ] All four blanks in the practice file are filled in, and a dataset can be recorded on the emulator or the board.
- [ ] Record all three labels, at least two bursts each, then count lines in the REPL and get 1 + (bursts × 200).
- [ ] Change `RATE_MS` to 40 (25 Hz), record another set, and note in your learning log how the time per burst and the waveform differ.
- [ ] Be able to explain where in the code the four beats — schema, sample, record, rate — happen, and why 50 Hz.

## Going further

In the next pair of lessons (2.3–2.4), we'll record audio and the IMU together on one shared timeline, enriching the dataset.

Next lesson: [lesson 2.3 — Audio and several sensors on one timeline: PDM at 16 kHz, timestamps and jitter](../l03-audio-and-timeline/README.md)

## Reflect

- Is your dataset balanced yet? If not, how would you collect more without mixing up labels?
- If you wanted to record air pressure instead of the IMU, how many lines would you need to change, and what would you set RATE_MS to?
