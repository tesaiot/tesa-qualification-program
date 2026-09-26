---
id: edgeai-dev.m04.l06
lang: en
title: {th: 'ลงมือทำ: feature vector จากหน้าต่างเลื่อน', en: 'Hands-on: a feature vector from a sliding window'}
summary: {th: เติมห้าจุดใน s10_windowing.py ให้เก็บสัญญาณเข้า buffer คำนวณ mean std และพลังงานต่อย่าน แล้วเลื่อนหน้าต่างให้ซ้อน 50% จนได้ feature vector หกตัวที่ขยับตามการเคลื่อนไหวจริง พร้อมเห็นว่ามันคือหน่วยข้อมูลของ dataset ในโมดูลถัดไป, en: 'Fill five points in s10_windowing.py to buffer the signal, compute mean, std and band energy, and slide the window with 50% overlap, producing a six-value feature vector that follows real motion - the unit of the dataset in the next module.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m04.l05]
objectives:
  - {th: เติมห้าจุดใน practice/s10_windowing.py จนแท่ง feature ทั้งหกขยับ และตัวนับหน้าต่างเพิ่มขึ้นทุก HOP จุด, en: Fill the five points in practice/s10_windowing.py until all six feature bars move and the window counter rises every HOP samples.}
  - {th: วัดและจดค่า std ตอนวางนิ่งเทียบกับตอนเขย่า แล้วอธิบายได้ว่าต่างกันเพราะอะไร, en: 'Measure and record std at rest versus shaking, and explain why they differ.'}
  - {th: 'อธิบายได้ว่าลำดับ mean → std สำคัญอย่างไร และทำไมการลืม buf = buf[-WIN:] ทำให้หน่วยความจำรั่ว', en: 'Explain why the order mean → std matters and why forgetting buf = buf[-WIN:] leaks memory.'}
develops: [{skill: sys.dsp, to: 3}, {skill: lang.micropython, to: 2}, {skill: prog.memory, to: 1}]
assesses: [{skill: sys.dsp, level: 3, evidence: practice/s10_windowing.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: 3c73555aaa4ded5fbc1de9e4066ab4f97bd3c4f511164d997c20fc3df74acff6
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 4.6 — Hands-on: a feature vector from a sliding window

> Module 4 — Signal analysis · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Fill five points in s10_windowing.py to buffer the signal, compute mean, std and per-band energy, then slide the window with 50% overlap, producing a six-value feature vector that follows real motion — while seeing that this is the unit of data for the next module's dataset.

## Objectives

By the end of this lesson, you will:

1. Fill the five points in practice/s10_windowing.py until all six feature bars move and the window counter rises every HOP samples.
2. Measure and record std at rest versus while shaking, and explain why they differ.
3. Explain why the order mean → std matters, and why forgetting buf = buf[-WIN:] leaks memory.

## Before you start

You've been through lesson 4.5, and know WIN, HOP, and the six features. Keep your learning log ready to note the std value at rest and while shaking.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/)
- **Prior lesson:** [lesson 4.5 — Features and windowing: what the model actually sees](../l05-features-and-windowing/README.md)

## Concepts

The whole file reads as one sentence: buffer the signal → once a window's worth is collected, squeeze it into features → show them as bars → slide the window → loop. The five points we fill in are: (1) `buf.append(az)`, inside a loop that reads `sensors.bmi270.motion()` one HOP point at a time, delaying 20 ms (50 Hz) (2) `mean = sum(win) / n` (3) `std = math.sqrt(sum((x - mean) ** 2 for x in win) / n)`, which must always come after mean, since it uses the mean value (4) `band_e.append(sum((x - m) ** 2 for x in s) / len(s))`, inside a loop over four bands, and (5) `buf = buf[-WIN:]`, after squeezing the features, to keep only the last WIN points, so the next window overlaps 50%. If you forget this last point, the buffer grows without bound until memory runs out.

The display is already given — the bars are scaled roughly (`mean` and `std` multiplied by 2, bands by 0.02), just enough to be visible to the eye. `lcd.console` prints the feature vector's real values alongside it. When feeding a real model, we'll normalize systematically in module 5, but the same principle applies: bring every feature into a similar scale. Everything here is plain Python on the CM33 — no NPU needed.

Success in this pair of lessons is being able to say why std is low at rest, and how this feature vector becomes a dataset. In the next module, we'll do the same thing but with a label attached, saved to CSV, to train a model in TensorFlow.

## Worked example

`s10_windowing_full.py` adds highlighting the strongest band, deciding "still" or "moving" from std with a threshold `STD_MOVE` (in m/s², adjustable per board), and measuring the window rate per second — an example of rule-based classification on features we built ourselves.

| File | What this file teaches |
|---|---|
| [examples/s10_windowing_full.py](examples/s10_windowing_full.py) | A visual feature front-end: windowing + a feature vector (full version) |

## Practice

The `# TODO:` comments are at lines 37 (mean), 39 (std), 48 (band energy), 78 (`buf.append`), and 91 (`buf = buf[-WIN:]`). Replace `pass` or the `0.0` value with the calls the hints describe, then alternate holding still and shaking. If the bars never move, check your indentation and the mean → std order.

| Practice file | Topic |
|---|---|
| [practice/s10_windowing.py](practice/s10_windowing.py) | What a model "sees": windowing + a feature vector (the fill-in-the-code version) |

## Solution

Open the solution after trying on your own at least once, and read [how to use the solutions](../../README.en.md#how-to-use-the-solutions) first.

| Solution | Pairs with |
|---|---|
| [solution/s10_windowing.py](solution/s10_windowing.py) | [practice/s10_windowing.py](practice/s10_windowing.py) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. You run it, and every bar stays still, and the window counter never rises at all. Which point is most likely still empty? *(single choice · objective 1)*
   - a) buf.append(az), so the buffer never reaches a full window
   - b) band_e.append(...)
   - c) buf = buf[-WIN:]
   - d) std

   <details><summary>Solution</summary>

   **a** — if values are never stored in the buffer, the condition len(buf) >= WIN can never become true, so features are never squeezed, and windows never counted.

   </details>

2. The board lies still and std is low, but once shaken, std is very high. Why? *(single choice · objective 2)*
   - a) Shaking always raises az's average
   - b) std measures how spread out values are from the average; shaking makes az oscillate widely around the average
   - c) The sensor changes units while shaking
   - d) The window shortens while shaking

   <details><summary>Solution</summary>

   **b** — at rest, every point sits close to the average, so std is small. While shaking, points spread far from the average, so std is large — this is why a simple statistical feature separates postures well.

   </details>

3. If the std line is written before the mean line inside features(), what happens? *(single choice · objective 3)*
   - a) You get the same value
   - b) std is computed against the starting value mean = 0.0, so it's wrong (you get a value close to the signal's level, not its spread)
   - c) The program always throws NameError
   - d) band energy becomes wrong instead

   <details><summary>Solution</summary>

   **b** — std needs an already-computed mean. If mean is still 0.0, the sum of (x − 0)² reflects the signal's magnitude, not its spread around the average.

   </details>

4. You forget to fill in buf = buf[-WIN:]. What's the long-term result? *(single choice · objective 3)*
   - a) Windows don't overlap, but everything else is normal
   - b) The buffer keeps growing without bound until memory runs out
   - c) Every feature becomes zero
   - d) The sampling rate speeds up

   <details><summary>Solution</summary>

   **b** — features() still uses buf[-WIN:], so it looks like it's working normally at first, but the list keeps getting appended to forever — a memory leak that eventually hangs the board.

   </details>

## Lab

**The MVP for lessons 4.5–4.6:** build a feature vector from a raw signal by hand — slice a window (window + hop), then squeeze it into mean, std and band values that change with motion.

- [ ] All five points in the practice file are filled in, and it runs on the emulator or the board.
- [ ] Lie still, then shake, and note the std value for both in your learning log — how many times larger, and why?
- [ ] Change `HOP` to match `WIN`, and observe how the window rate changes, and what you risk missing.
- [ ] Be able to explain what a window and a hop are, why they must overlap, and what std tells you.

## Going further

In the next module (Training), we'll collect data like this with a label attached, into a real dataset — split into train, val, test — and train a model of our own.

Next lesson: [lesson 5.1 — Dataset engineering: class balance, windows and the train/val/test split](../../m05-training/l01-dataset-engineering/README.md)

## Reflect

- Are these six features enough to tell idle, circle and shaking apart? If not, what feature would you add?
- If your bands were split by frequency instead of time, how close would the result be to what audio models use?
