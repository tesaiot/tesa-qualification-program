---
id: edgeai-dev.m04.l05
lang: en
title: {th: 'feature และหน้าต่าง: สิ่งที่โมเดลเห็นจริง', en: 'Features and windowing: what the model actually sees'}
summary: {th: เข้าใจสิ่งที่โมเดลเห็นจริง โมเดลไม่กิน sample ดิบทีละจุดแต่กินหน้าต่างที่ถูกบีบเป็น feature vector เรียนเรื่องหน้าต่างเลื่อนกับ hop ทำไมต้องซ้อน ฟีเจอร์เชิงสถิติ mean std และพลังงานต่อย่าน และโยงไปสู่ log-mel spectrogram ของโมเดลเสียง, en: 'Learn what the model actually sees - not raw samples one by one but windows squeezed into a feature vector; sliding windows and hop, why they overlap, statistical features (mean, std, band energy), and the link to the log-mel spectrogram used by audio models.'}
level: L3
time_min: {concept: 45, practise: 10, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m04.l04]
objectives:
  - {th: 'อธิบายได้ว่าทำไมโมเดลต้องดูหน้าต่างของสัญญาณแทน sample เดี่ยว และคำนวณจำนวนหน้าต่างต่อวินาทีจาก WIN, HOP และอัตราสุ่ม', en: 'Explain why a model must look at a window of signal rather than single samples, and compute windows per second from WIN, HOP and the sample rate.'}
  - {th: บอกข้อแลกเปลี่ยนของการซ้อนหน้าต่าง (hop เล็กกับใหญ่) และเหตุผลที่หน้าต่างซ้อนกันไม่พลาดเหตุการณ์สั้น, en: State the trade-off of window overlap (small versus large hop) and why overlapping windows do not miss short events.}
  - {th: คำนวณ mean และ std ของหน้าต่างเล็ก ๆ ด้วยมือ และอธิบายว่า std แยกนิ่งกับขยับได้อย่างไร ส่วน mean บอกท่าทางคงที่, en: 'Compute the mean and std of a small window by hand, and explain how std separates still from moving while mean tells the steady posture.'}
  - {th: อธิบายสายพาน log-mel = log(Mel(|FFT(x·w)|)) และเหตุผลที่ front-end ตอนฝึกกับตอนใช้งานต้องตรงกัน, en: Explain the log-mel pipeline log(Mel(|FFT(x·w)|)) and why the front-end must match between training and deployment.}
develops: [{skill: sys.dsp, to: 3}, {skill: ai.data-collection, to: 2}, {skill: hw.math, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: a05418b12186784594b5f427f5a9614c0b0bd54e85c6adb683c6042cef678634
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 4.5 — Features and windowing: what the model actually sees

> Module 4 — Signal analysis · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Understand what a model actually sees. A model doesn't eat raw samples one point at a time — it eats windows squeezed into a feature vector. Learn about sliding windows and hop, why they must overlap, statistical features (mean, std, per-band energy), and the link to the log-mel spectrogram used by audio models.

## Objectives

By the end of this lesson, you will:

1. Explain why a model must look at a window of signal instead of a single sample, and compute windows per second from WIN, HOP and the sample rate.
2. State the trade-off of window overlap (small versus large hop), and why overlapping windows don't miss short events.
3. Compute the mean and std of a small window by hand, and explain how std separates still from moving, while mean shows a steady posture.
4. Explain the log-mel pipeline log(Mel(|FFT(x·w)|)), and why the front-end must match between training and deployment.

## Before you start

You've been through lessons 4.3–4.4, and understand the FFT, the Hann window, and the magnitude. Open the `s10_windowing.py` example in BENTO IDE.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/)
- **Prior lesson:** [lesson 4.4 — Hands-on: a live spectrum from the IMU](../l04-fft-spectrum-lab/README.md)

## See it work first

Run `s10_windowing.py` right away. Alternate lying the board still and shaking it gently, and watch the mean, std and band0..3 bars move. That's the feature vector flowing into the model — one chunk of raw signal becoming just a handful of numbers.

## Concepts

A single cough or a single shake isn't a value at one point — it's **the shape of a signal over a stretch of time**. A model therefore eats a **window** — for example, `WIN = 50` points, or one second at 50 Hz. The window slides forward by `HOP = 25` points at a time, so it overlaps 50%, giving a new feature set every 25 points (twice a second). Overlapping makes the response quicker and stops short events falling into the gap between windows, at the cost of computing more often. The window size isn't set arbitrarily — whatever size the model was trained with, deployment must feed it the exact same size.

A 50-point window is squeezed into a **feature vector** of six values: `[mean, std, band0, band1, band2, band3]`. `mean` shows the DC level, or the direction of gravity on that axis (a steady posture). `std` = $\sqrt{\frac{1}{n}\sum (x_i - \bar{x})^2}$ shows how strong the shaking is — low at rest, high when shaken. `band0..3` splits the window into four segments **in time**, then measures the variance of each segment, catching whether the shaking is clustered near the start, middle, or end of the window. A model is only as small and accurate as its features are good.

The board's audio models use the same skeleton, but split into bands by **frequency** instead: slice a window → multiply by Hann → FFT → take the magnitude → combine into mel bands, matching how the ear hears (fine resolution at low frequency, coarse at high) → log to compress the dynamic range. It can be written as one formula: $\text{logmel} = \log(\mathrm{Mel}(|\mathrm{FFT}(x \cdot w)|))$. The most important takeaway is: **a model never sees the raw signal.** It only ever sees the feature vector a front-end squeezes for it. During training, the dataset is a set of feature vectors with labels; in deployment, the board squeezes a live signal the exact same way. If the two front-ends don't match, the model breaks instantly — a classic edge AI bug.

## Worked example

`s10_windowing.py` is the reference version, using `WIN = 50` and `HOP = 25`. **Predict** before running it: which bar will rise the most when shaken? Then try rotating the board slowly and compare — you'll see mean change while std stays low.

| File | What this file teaches |
|---|---|
| [examples/s10_windowing.py](examples/s10_windowing.py) | What a model "sees": windowing + a feature vector |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. WIN = 50, HOP = 25, at a sample rate of 50 Hz. How many new feature vectors per second? *(single choice · objective 1)*
   - a) 1
   - b) 2
   - c) 25
   - d) 50

   <details><summary>Solution</summary>

   **b** — a new set comes every HOP = 25 points. At 50 points per second, that's 2 sets per second, each covering 1 second and overlapping 50%.

   </details>

2. You set HOP = WIN (no overlap). What's the main risk? *(single choice · objective 2)*
   - a) Memory fills up
   - b) A short event straddling the boundary between two windows might get split in half and missed by the model, and results come more slowly
   - c) std becomes negative
   - d) The sampling rate changes

   <details><summary>Solution</summary>

   **b** — overlap covers every point with more than one window, and produces results more often. No overlap saves effort but responds more slowly and misses more easily.

   </details>

3. A window [7.8, 11.8, 7.8, 11.8] — what are its mean and std? *(single choice · objective 3)*
   - a) mean 9.8, std 0
   - b) mean 9.8, std 2.0
   - c) mean 4.0, std 9.8
   - d) mean 11.8, std 4.0

   <details><summary>Solution</summary>

   **b** — the average is 9.8; every point is 2.0 away from the average, so std is 2.0. Compare with a still window [9.8, 9.8, 9.8, 9.8], where std = 0 even though the mean is the same.

   </details>

4. You rotate the board slowly from flat to upright. Which feature changes the most? *(single choice · objective 3)*
   - a) mean, because gravity's direction on the Z axis changes; std stays low since there's no shaking
   - b) std, because the board is moving
   - c) band3 only
   - d) No feature changes

   <details><summary>Solution</summary>

   **a** — mean shows steady posture, std shows shaking. A slow rotation changes az's average level but barely makes the value oscillate.

   </details>

5. Put the pipeline that builds a log-mel spectrogram from one audio window in order *(ordering · objective 4)*
   - a) FFT
   - b) Multiply by the Hann window (x · w)
   - c) log
   - d) Take the magnitude |·|
   - e) Combine into Mel bands

   <details><summary>Solution</summary>

   **b → a → d → e → c** — x·w → FFT → |·| → Mel → log. If training and on-board deployment don't do these steps identically, the model's results go wrong.

   </details>

## Lab

- [ ] Compute the number of windows per second when WIN = 50, HOP = 25 at 50 Hz, and when HOP = 50.
- [ ] Compute the mean and std of the windows [9.8, 9.8, 9.8, 9.8] and [7.8, 11.8, 7.8, 11.8] by hand, and note them in your learning log.
- [ ] Write out the log-mel pipeline step by step in your own words, saying which step you've already done in lesson 4.4.

## Going further

In lesson 4.6, we'll fill in the `s10_windowing.py` file to collect a buffer, squeeze features, and slide the window ourselves.

Next lesson: [lesson 4.6 — Hands-on: a feature vector from a sliding window](../l06-windowing-lab/README.md)

## Reflect

- If you had to tell "walking" apart from "running," which of these six features do you think would help most, and what's still missing?
- Why is it dangerous to change the window size after a model has already been trained?
