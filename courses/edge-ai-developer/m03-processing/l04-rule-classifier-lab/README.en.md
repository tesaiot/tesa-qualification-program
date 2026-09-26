---
id: edgeai-dev.m03.l04
lang: en
title: {th: 'ลงมือทำ: ตัวจำแนกความสบายด้วยกฎ', en: 'Hands-on: a rule-based comfort classifier'}
summary: {th: เติม s07_rule_classifier.py ให้คำนวณ dew point กับ heat index เขียนบันไดกฎหกชั้นใน classify() และระบายสีคำตัดสินบนจอ แล้วเทียบกับ dsp.comfort_zone พร้อมเห็นจุดแข็งเรื่องอธิบายได้และข้อจำกัดที่ปูทางไปสู่ ML, en: 'Complete s07_rule_classifier.py so it computes dew point and heat index, write a six-step ladder in classify(), colour the verdict on screen, and compare it with dsp.comfort_zone while seeing the explainability strength and the limits that lead to ML.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m03.l03]
objectives:
  - {th: เติมสี่ช่องใน practice/s07_rule_classifier.py จนการ์ดคำตัดสินเปลี่ยนคำและสีตามอุณหภูมิกับความชื้นจริง และทำให้เกิดคลาสต่างกันอย่างน้อยสามคลาส, en: 'Fill the four blanks in practice/s07_rule_classifier.py until the verdict card changes word and colour with real temperature and humidity, producing at least three different classes.'}
  - {th: ปรับเส้นแบ่งหนึ่งเส้นแล้วอธิบายได้ว่าคำตัดสินที่ค่าใกล้เส้นเปลี่ยนไปอย่างไร และทำไมคำตัดสินของเราอาจไม่ตรงกับ dsp.comfort_zone โดยไม่แปลว่าผิด, en: 'Adjust one threshold and explain how verdicts near that line change, and why your verdict may disagree with dsp.comfort_zone without being wrong.'}
  - {th: อธิบายจุดแข็งด้านความอธิบายได้ของกฎ (rule trace) และข้อจำกัดสามข้อของกฎมือที่เป็นแรงจูงใจของ ML, en: Explain the explainability strength of rules (the rule trace) and three limits of hand-written rules that motivate ML.}
develops: [{skill: prog.algo-ds, to: 2}, {skill: lang.micropython, to: 2}, {skill: gui.hmi, to: 2}, {skill: ai.edge, to: 1}]
assesses: [{skill: prog.algo-ds, level: 2, evidence: practice/s07_rule_classifier.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: 4ebe3236eae98856114e470c6206481fcb7282a5cda47be187662bbfdaf7c0c2
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 3.4 — Hands-on: a rule-based comfort classifier

> Module 3 — Processing with maths and physics · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Complete s07_rule_classifier.py so it computes dew point and heat index, write a six-step ladder in classify(), colour the verdict on screen, and compare it with dsp.comfort_zone, while seeing the explainability strength and the limits that lead to ML.

## Objectives

By the end of this lesson, you will:

1. Fill the four blanks in practice/s07_rule_classifier.py until the verdict card changes word and colour with real temperature and humidity, producing at least three different classes.
2. Adjust one threshold and explain how verdicts near that line change, and why your verdict may disagree with dsp.comfort_zone without being wrong.
3. Explain the explainability strength of rules (the rule trace), and three limits of hand-written rules that motivate ML.

## Before you start

You've been through lesson 3.3, and know a rule ladder must be ordered from severe to broad. If you're using a board, prepare a way to change the air around the sensors: breathe on it, cup the board in your hand, or bring it near an air conditioner.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — needs the SHT40 and DPS368 (present on the TESAIoT Dev Kit, absent on the Eva Kit); the emulator simulates the values and computes dsp with the real formulas.
- **Prior lesson:** [lesson 3.3 — Derived metrics and rule-based classification: dew point, heat index and the rule ladder](../l03-rules-before-ml/README.md)

## Concepts

The loop has four steps: **read raw values → convert to derived → decide with rules → draw the class.** Reading raw values is already given (`p, t = sensors.dps368.pressure_temperature()` and `h = sensors.sht40.humidity()`, which returns a single %RH value). The four blanks are: (1) `dp = dsp.dew_point(t, h)` (2) `hi = dsp.heat_index(t, h)` (3) the rule ladder in `classify()`, checking `danger` (hi ≥ 41) → `hot` (hi ≥ 32) → `humid` (h ≥ 70) → `cold` (t < 20) → `dry` (h < 30) → `comfortable`, and (4) `verdict.text(zone)` with `verdict.color(COLORS.get(zone, WHITE))`. The starting values `dp = 0.0` and `hi = t` keep the program from crashing before everything's filled in. If you forget blank 3, `classify()` returns `None`, and the card stays empty and white.

The bottom section, already given, shows `dsp.comfort_zone(t, h)` for comparison. The verdicts may disagree, because the two rules define "comfortable" differently (ours uses heat index; the firmware's uses raw temperature, with different threshold numbers). Neither set is completely "right" — a rule depends on the definition chosen, a limitation ML will later help with using real data.

The strongest thing about a rule ladder is that every decision can be traced back to which step fired. The full version has `classify()` return the reason too, such as `why: feels-like 43 >= 41` — this is the explainability that safety and medical work require. But hand-set rules run into three walls: rules balloon out of control once there are many features, thresholds a human sets may not be the best ones for real data, and rules never adapt to new data on their own. The feeling that "if there were any more conditions than this, writing `if`s just wouldn't work anymore" is the real motivation behind ML, in module 5.

## Worked example

`s07_rule_classifier_full.py` adds a rule trace (`why`), a flag for whether it matches `dsp.comfort_zone`, and hysteresis to stop the class flickering when a reading jitters right across a threshold. Open it once your practice file is done.

| File | What this file teaches |
|---|---|
| [examples/s07_rule_classifier_full.py](examples/s07_rule_classifier_full.py) | Classifying weather with rules (full version) |

## Practice

The `# TODO:` comments are at lines 43 (the rule ladder in `classify()`), 91 (dew point), 94 (heat index), and 106–107 (showing it on screen with colour). Fill in one blank at a time and run it. If the class never changes, check your indentation and the ladder's step order.

| Practice file | Topic |
|---|---|
| [practice/s07_rule_classifier.py](practice/s07_rule_classifier.py) | Classifying weather with "rules" we write ourselves (the fill-in-the-code version) |

## Solution

Open the solution after trying on your own at least once, and read [how to use the solutions](../../README.en.md#how-to-use-the-solutions) first.

| Solution | Pairs with |
|---|---|
| [solution/s07_rule_classifier.py](solution/s07_rule_classifier.py) | [practice/s07_rule_classifier.py](practice/s07_rule_classifier.py) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. Put the four steps of s07_rule_classifier.py's loop in order *(ordering · objective 1)*
   - a) Decide with rules: zone = classify(t, h, hi)
   - b) Read raw values: dps368 and sht40
   - c) Draw the class: verdict.text and verdict.color
   - d) Convert to derived: dew_point and heat_index

   <details><summary>Solution</summary>

   **b → d → a → c** — read → convert → decide → draw is a mini pipeline for the whole classifier. Blanks 1–2 are the convert step, 3 is the decide step, 4 is the draw step.

   </details>

2. You run it and the verdict card stays empty and white forever. What's the most likely cause? *(single choice · objective 1)*
   - a) The ladder in classify() hasn't been filled in yet, so the function returns None, and COLORS.get(None, WHITE) gives white
   - b) The SHT40 isn't connected
   - c) The heat index is too high
   - d) The emulator doesn't support ui.Seg7

   <details><summary>Solution</summary>

   **a** — a class not found in COLORS falls back to white. This symptom tells you the ladder isn't working yet.

   </details>

3. classify()'s verdict is comfortable, but dsp.comfort_zone answers acceptable. What should you conclude? *(single choice · objective 2)*
   - a) classify() must be wrong
   - b) dsp.comfort_zone must be wrong
   - c) The two rules define comfort differently (different values and thresholds) — disagreeing doesn't mean either is wrong
   - d) The sensors are reading inconsistent values

   <details><summary>Solution</summary>

   **c** — ours decides from heat index; the firmware's decides from raw temperature with its own ranges. A rule depends on the definition chosen.

   </details>

4. Which of these are limits of hand-set rules that motivate moving to ML? (select every correct answer) *(multiple choice · objective 3)*
   - a) Rules balloon out of control to write when there are dozens of features
   - b) A threshold a human sets may not be the best one for real data
   - c) Rules don't adapt to new data on their own
   - d) Rules can't explain their own decision

   <details><summary>Solution</summary>

   **a, b, c** — explainability is a strength of rules, not a limitation. A rule trace can always say which step fired the decision.

   </details>

## Lab

**The MVP for lessons 3.3–3.4:** write your own `classify()` with a rule ladder, and have the board or emulator show a class that genuinely changes as temperature or humidity changes, using at least one derived value in the decision.

- [ ] All four blanks in the practice file are filled in, and it runs on the emulator or the board.
- [ ] Produce at least three classes (for example, breathing on it → `humid`, cupping the board → `hot`, normal → `comfortable`), and note the method in your learning log.
- [ ] Adjust one threshold (for example, `hi >= 32` to `>= 30`), find a value that sits right across it, and explain how the verdict changes.
- [ ] Point out which condition the `hot` class comes from, and why it uses `hi` instead of `t`.

## Going further

In the next module (Analysis), we start with signal filters — EMA, Median and Kalman — that smooth out jittery signals visibly to the eye.

Next lesson: [lesson 4.1 — DSP filters: EMA, Median, Kalman and the radar range profile](../../m04-analysis/l01-dsp-filters/README.md)

## Reflect

- If your verdict disagrees with `dsp.comfort_zone`, how would you decide which one to trust?
- What problem does hysteresis solve, and why is it more necessary with a real sensor than with a simulated value?
