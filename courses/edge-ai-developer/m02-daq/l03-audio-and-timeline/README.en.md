---
id: edgeai-dev.m02.l03
lang: en
title: {th: 'เสียงและหลายเซนเซอร์บนเส้นเวลาเดียว: PDM 16 kHz ประทับเวลา และ jitter', en: 'Audio and several sensors on one timeline: 16 kHz PDM, timestamps and jitter'}
summary: {th: เพิ่มเซนเซอร์ตัวที่สองให้ dataset เข้าใจว่าไมโครโฟน PDM ส่งเสียงเป็น PCM 16 kHz อย่างไร ย่อเฟรมเสียงเป็นค่า dBFS ค่าเดียว แล้วมัดเสียงกับ IMU ไว้บนเส้นเวลาเดียวด้วย ticks_ms และตรวจ jitter ได้, en: 'Add a second sensor to the dataset - learn how the PDM microphone delivers 16 kHz PCM, reduce an audio frame to one dBFS value, and tie sound and IMU to one timeline with ticks_ms while checking for jitter.'}
level: L3
time_min: {concept: 40, practise: 10, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m02.l02]
objectives:
  - {th: อธิบายเส้นทาง PDM → PCM 16-bit → RMS → dBFS และคำนวณ dBFS ของเฟรมจาก RMS ได้ (เช่น RMS = 3277 ได้ราว −20 dBFS), en: Explain the path PDM → 16-bit PCM → RMS → dBFS and compute a frame's dBFS from its RMS (for example RMS = 3277 gives about −20 dBFS).}
  - {th: คำนวณระยะห่างระหว่างตัวอย่างเสียง Ts = 1/fs และความยาวของหนึ่งเฟรม t = N/fs ได้ และบอกว่าเฟรมที่ยาวเกินจังหวะแถวส่งผลกับ jitter อย่างไร, en: 'Compute the sample spacing Ts = 1/fs and one frame''s length t = N/fs, and say how a frame longer than the row period affects jitter.'}
  - {th: 'อธิบายได้ว่าทำไมต้อง "อ่านพร้อมกัน เขียนแถวเดียว ประทับเวลาร่วม" และใช้ time.ticks_diff(time.ticks_ms(), t0) แทนการลบตรง ๆ', en: 'Explain why you "read together, write one row, share one timestamp", and use time.ticks_diff(time.ticks_ms(), t0) instead of plain subtraction.'}
develops: [{skill: ai.data-collection, to: 2}, {skill: sys.dsp, to: 2}, {skill: sys.sensors-actuators, to: 2}, {skill: mcu.timers, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: ae80310df8586e5674358c429a31852b0c0df0e259691be1598ddc1b06631d0a
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 2.3 — Audio and several sensors on one timeline: 16 kHz PDM, timestamps and jitter

> Module 2 — Collecting sensor data (DAQ) · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Add a second sensor to the dataset. Learn how the PDM microphone delivers 16 kHz PCM sound, reduce an audio frame to a single dBFS value, then tie sound and the IMU together onto one timeline with ticks_ms and check for jitter.

## Objectives

By the end of this lesson, you will:

1. Explain the path PDM → 16-bit PCM → RMS → dBFS, and compute a frame's dBFS from its RMS (for example, RMS = 3277 gives about −20 dBFS).
2. Compute the audio sample spacing Ts = 1/fs and one frame's length t = N/fs, and state how a frame longer than the row period affects jitter.
3. Explain why you must "read together, write one row, share one timestamp," and use time.ticks_diff(time.ticks_ms(), t0) instead of plain subtraction.

## Before you start

You've been through lessons 2.1–2.2, have your own `/gestures.csv` file, and understand DAQ's four beats. If you'll use real audio, make sure you have a board whose PDM microphone works (see the hardware line below).

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — real audio must come from the board's PDM microphone. The 06/07 audio examples state they work on the PSoC Edge AI Kit; on the TESAIoT Dev Kit (which has an audio codec), enabling PDM still conflicts with the audio system's clock. The emulator has PDM_PCM that delivers synthetic audio, only good for trying the program's skeleton.
- **Prior lesson:** [lesson 2.2 — Hands-on: a DAQ logger that writes a CSV dataset](../l02-daq-logger-lab/README.md)

## See it work first

Run `06_mic_level_meter.py` and speak or clap into the mic — the VU bar and the dBFS number follow along, sound turning into real numbers before your eyes. Then look at `07_mic_record_wav.py`, which records the whole raw audio block into a `.wav` file. These two are the raw material we'll tie to the IMU.

## Concepts

The board's microphone is **PDM**, sending high-speed 0/1 bits. The `machine.PDM_PCM` hardware converts these into 16-bit **PCM** audio samples at `sample_rate=16000`, which we read into `array.array("h", ...)` with `pdm.readinto(buf)`. The sample spacing is $T_s = 1/f_s = 62.5\ \mu s$, and 16 kHz is enough for speech and environmental sound, whose energy mostly sits below 8 kHz, per the Nyquist rule. We read in chunks of `CHUNK = 512` samples, so one frame lasts $t = N/f_s = 512/16000 = 32$ ms.

Recording every single sample to CSV isn't feasible (16,000 values per second), so we reduce a frame to **a single value**: find the RMS (the wave's average magnitude), then compare it against the 16-bit maximum in decibels, $\text{dBFS} = 20\log_{10}(\text{RMS}/32768)$ — 0 is the loudest, and more negative means quieter. The whole raw audio block can still be saved separately as WAV if needed.

The problem with two sensors is **syncing**: if they're recorded to separate files on separate schedules, there's no way to pair which sound goes with which motion. The fix is to **read together, write one row, share one timestamp**: in a single loop round, read the IMU and the MIC back to back, then write one row where both use the same `t_ms`. `t_ms = time.ticks_diff(time.ticks_ms(), t0)` uses `ticks_diff` because the millisecond counter can wrap around back to zero. The real interval between rows will drift somewhat from 20 ms, since reading audio and writing the file both take time — this is called **jitter**. Because we keep the real `t_ms` on every row, we can check for it after the fact, and reduce jitter by shrinking `CHUNK`, trimming other work in the loop, and not printing to the console too often. The file's schema is `t_ms,label,ax,ay,az,gx,gy,gz,db`, with a label on every row, so the dataset is ready to train the moment it leaves the board.

## Worked example

**Predict** before running `06_mic_level_meter.py`: roughly how different will the dBFS be between silence and a clap? Then run it and compare. `07_mic_record_wav.py` produces a `/rec.wav` file you can pull off with BENTO IDE (file transfer) or `mpremote`, then listen to on your PC.

| File | What this file teaches |
|---|---|
| [examples/06_mic_level_meter.py](examples/06_mic_level_meter.py) | VU Meter: PDM mic -> RMS -> dBFS -> a level bar with peak hold |
| [examples/07_mic_record_wav.py](examples/07_mic_record_wav.py) | Recording audio to a .wav file, with an on-screen countdown |

This lesson's slides also reference files in other lessons:

- [m02-daq/l02-daq-logger-lab/practice/s04_daq_logger.py](../l02-daq-logger-lab/practice/s04_daq_logger.py) — recording sensor data to a CSV file (Data Acquisition) (the fill-in-the-code version)
- [m02-daq/l04-multicapture-lab/practice/s05_multicapture.py](../l04-multicapture-lab/practice/s05_multicapture.py) — recording 2 sensors together on one timeline (the fill-in-the-code version)

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. An audio frame has RMS = 32768, equal to the 16-bit maximum. What's the dBFS? *(single choice · objective 1)*
   - a) 0 dBFS
   - b) −96 dBFS
   - c) +20 dBFS
   - d) 32768 dBFS

   <details><summary>Solution</summary>

   **a** — 20·log10(32768/32768) = 20·log10(1) = 0 dBFS, the loudest possible. Quieter sound gives a negative value; −96 is the value the code uses to represent complete silence.

   </details>

2. Put the audio path in order, from the microphone to the db column in the CSV *(ordering · objective 1)*
   - a) Compute the frame's RMS
   - b) High-speed PDM 0/1 bits
   - c) Convert to dBFS and write it to the row
   - d) 16-bit PCM samples in buf from pdm.readinto()

   <details><summary>Solution</summary>

   **b → d → a → c** — PDM → PCM in a buffer → RMS → dBFS as one value per frame, which is the first step before building a spectrogram in module 4.

   </details>

3. At fs = 16 kHz, how long is a frame of N = 512 samples? *(single choice · objective 2)*
   - a) 3.2 ms
   - b) 32 ms
   - c) 62.5 µs
   - d) 512 ms

   <details><summary>Solution</summary>

   **b** — t = N / fs = 512 / 16000 = 0.032 seconds = 32 ms, longer than the 20 ms row period. Reading audio is therefore the main cause of jitter.

   </details>

4. Which approach guarantees audio and IMU values in a dataset are correctly paired by time? *(single choice · objective 3)*
   - a) Record audio and the IMU to separate files, then pair them afterward by line order
   - b) Read both sensors in the same loop round, then write one row sharing one t_ms
   - c) Use time.time() to record a separate timestamp for each file
   - d) Set RATE_MS to 0

   <details><summary>Solution</summary>

   **b** — one round = one row = one t_ms, so every column in a row refers to the same instant. Pairing by order easily breaks when the rates differ.

   </details>

5. Why use time.ticks_diff(time.ticks_ms(), t0) instead of time.ticks_ms() - t0? *(single choice · objective 3)*
   - a) Because ticks_diff is faster
   - b) Because the millisecond counter can wrap back to zero; ticks_diff computes the interval correctly even when the counter wraps
   - c) Because ticks_ms returns a value in seconds
   - d) Because subtraction isn't possible in MicroPython

   <details><summary>Solution</summary>

   **b** — ticks_ms and ticks_diff are MicroPython's standard pair for safely measuring short intervals, immune to wrap-around.

   </details>

## Lab

- [ ] Run the VU meter and note the dBFS values for silence, speaking, and a clap, in your learning log.
- [ ] Compute t = N/fs for CHUNK = 256 and 1024, and say which one risks pushing rows further than 20 ms apart.
- [ ] Write the schema for a multi-sensor file by hand, and say which call each column comes from.

## Going further

In lesson 2.4, we'll fill in the `s05_multicapture.py` file so it records the IMU and audio onto one timeline in `/multicapture.csv`.

Next lesson: [lesson 2.4 — Hands-on: recording the IMU and audio into one file](../l04-multicapture-lab/README.md)

## Reflect

- What real-world job needs to look at sound and motion together to make the right call?
- If you'd recorded audio and the IMU to separate files, could you still recover their timing alignment afterward? What extra data would you need?
