---
id: edgeai-dev.m05.l01
lang: en
title: {th: 'วิศวกรรมชุดข้อมูล: สมดุลคลาส หน้าต่าง และการแบ่ง train/val/test', en: 'Dataset engineering: class balance, windows and the train/val/test split'}
summary: {th: 'เริ่มสร้างโมเดลของเราเองจากสิ่งที่มาก่อนการฝึกเสมอ คือ dataset รู้จักท่อเตรียมข้อมูลสี่ขั้น capture, label, window, split เหตุผลของ class balance การแบ่ง train/val/test แบบ stratified และกฎเหล็กห้ามข้อมูลรั่ว (no leakage) โดยรันท่อทั้งเส้นด้วยข้อมูลสังเคราะห์ก่อน', en: 'Start building your own model from what always comes before training - the dataset. Learn the four-step preparation pipeline (capture, label, window, split), why class balance matters, the stratified train/val/test split and the no-leakage rule, running the whole pipeline on synthetic data first.'}
level: L3
time_min: {concept: 45, practise: 10, check: 10}
hardware: {emulator: false, boards: [none]}
prerequisites: [edgeai-dev.m04.l06]
objectives:
  - {th: เรียงท่อเตรียมข้อมูลสี่ขั้น capture → label → window → split ได้ และบอกได้ว่าขั้นใดทำบนบอร์ด ขั้นใดทำบน PC, en: Order the four-step preparation pipeline (capture → label → window → split) and say which steps run on the board and which on the PC.}
  - {th: คำนวณสัดส่วนคลาส p_c = n_c / N และอธิบายด้วยตัวอย่างได้ว่าทำไม dataset ที่ไม่สมดุลให้ความแม่นบนกระดาษที่หลอกตา, en: Compute the class share p_c = n_c / N and use an example to explain why an unbalanced dataset gives a misleading accuracy on paper.}
  - {th: 'คำนวณจำนวนหน้าต่างของแต่ละคลาสในกอง train, val และ test แบบ stratified ด้วย ⌊0.15·n_c⌋ และบอกหน้าที่ของแต่ละกอง', en: 'Compute the per-class window counts of a stratified train, val and test split with ⌊0.15·n_c⌋, and state the job of each set.'}
  - {th: ระบุได้ว่า normalize แบบใดทำให้ข้อมูลรั่ว และแก้ด้วยกฎ fit บน train แล้ว apply ทุกกอง, en: 'Identify which normalisation leaks data and fix it with the rule "fit on train, apply to every set".'}
develops: [{skill: ai.data-collection, to: 3}, {skill: ai.model-training, to: 1}, {skill: hw.math, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: b2dcb0c47ab41a8a9dfef50150b503c8fb23690ef8a615387713a3850c52654d
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 5.1 — Dataset engineering: class balance, windows and the train/val/test split

> Module 5 — Training and deploying to several targets · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Start building our own model from what always comes before training — the dataset. Learn the four-step preparation pipeline (capture, label, window, split), why class balance matters, the stratified train/val/test split, and the iron no-leakage rule, running the whole pipeline on synthetic data first.

## Objectives

By the end of this lesson, you will:

1. Order the four-step preparation pipeline, capture → label → window → split, and say which steps run on the board and which run on the PC.
2. Compute the class share p_c = n_c / N, and use an example to explain why an unbalanced dataset gives a misleading accuracy on paper.
3. Compute the per-class window counts of a stratified train, val and test split with ⌊0.15·n_c⌋, and state the job of each set.
4. Identify which kind of normalisation leaks data, and fix it with the rule "fit on train, apply to every set".

## Before you start

You've been through module 4, understand the sliding window WIN and HOP from lesson 4.5, and have already recorded a CSV with the DAQ logger in lesson 2.2. Have a PC with Python 3 and numpy ready, and download [`dataset_tools.py`](../../shared/training/dataset_tools.py).

- **Hardware:** your computer — no board needed. Use a PC with Python 3 and numpy; the board or emulator is used in lesson 5.2.
- **Prior lesson:** [lesson 4.6 — Hands-on: a feature vector from a sliding window](../../m04-analysis/l06-windowing-lab/README.md)

## See it work first

Run the whole pipeline before understanding it: `python dataset_tools.py --synthesize --out data/gestures.csv`, then `python dataset_tools.py --out data/gestures.csv`. You'll get `samples (3600, 6) windows (143, 50, 6) class counts [48 48 47]`. Ask yourself: what do the last three numbers tell you?

## Concepts

Our **dataset** is a plain CSV — one line per sample, starting with a **label**, followed by six values, `ax,ay,az,gx,gy,gz`, from `sensors.bmi270.motion()`. The label is the answer a human attached. We use the same three classes as the board's Motion model (`idle`, `circle`, `shaking`), so we can later compare our own model against the ready-made one. A raw CSV still can't be trained on — it must pass through four steps: **capture** and **label** on the board with MicroPython, then **window** and **split** on the PC with `dataset_tools.py`, which has five functions: `load_csv`, `make_windows`, `normalize`, `split` and `synthesize`. Synthetic data lets the pipeline run before we have real data.

**Class balance:** if 95% of the data is `idle`, a model that always answers `idle` is 95% accurate on paper, but useless in practice. We measure it with $p_c = n_c/N$, and it's balanced when $p_c \approx 1/K$ (about 0.33 for three classes). The most direct fix is to collect it balanced in the first place. **Windowing** uses `WIN = 50` (one second at 50 Hz) and `HOP = 25`. A window's label is whichever label dominates inside it, and it must be sliced exactly the way the board feeds the model in deployment.

**Train / val / test:** train teaches the model, val checks and tunes during training, test is a one-time exam at the end. `split()` divides it **stratified** — splitting class by class, shuffling order with `rng.permutation`, then cutting $n_{c,test} = \lfloor 0.15\,n_c \rfloor$, $n_{c,val} = \lfloor 0.15\,n_c \rfloor$, with the rest as train. Every set therefore has all classes in the same proportion. The 143-window synthetic data splits into train `[34 34 33]`, val `[7 7 7]`, test `[7 7 7]`. Last is **no leakage:** `normalize()` computes mean/std from train only, then applies it to every set. If computed from all the data combined, test leaks into train, and the accuracy numbers will look too good, with no error to warn you.

## Worked example

This lesson's slides also reference files in other lessons and under `shared/`:

- [m02-daq/l02-daq-logger-lab/examples/s04_daq_logger.py](../../m02-daq/l02-daq-logger-lab/examples/s04_daq_logger.py) — recording sensor data to a CSV file (Data Acquisition)
- [m02-daq/l02-daq-logger-lab/practice/s04_daq_logger.py](../../m02-daq/l02-daq-logger-lab/practice/s04_daq_logger.py) — recording sensor data to a CSV file (Data Acquisition) (the fill-in-the-code version)
- [m05-training/l02-dataset-lab/practice/s11_dataset.py](../l02-dataset-lab/practice/s11_dataset.py) — recording an IMU dataset that's "balanced and ready to train" to CSV (the fill-in-the-code version)
- [shared/training/dataset_tools.py](../../shared/training/dataset_tools.py) — Dataset tools for the IMU gesture classifier (Pillar 4 / Training).

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. Put the pipeline for preparing sensor data, from raw to ready-to-train, in order *(ordering · objective 1)*
   - a) window: slice into 50-sample windows (on the PC)
   - b) capture: read the IMU at 50 Hz (on the board)
   - c) split: divide into train/val/test (on the PC)
   - d) label: attach the motion's name (on the board)

   <details><summary>Solution</summary>

   **b → d → a → c** — capture and label happen on the board while collecting; window and split happen on the PC with dataset_tools.py, then get passed on to training.

   </details>

2. A dataset has idle 950 windows, circle 30, and shaking 20. What accuracy does a model that always answers idle get? *(single choice · objective 2)*
   - a) 33%
   - b) 50%
   - c) 95%, despite learning nothing at all
   - d) 100%

   <details><summary>Solution</summary>

   **c** — p_idle = 950/1000 = 0.95. The accuracy on paper is high but misleading. Balanced data should give each class about 1/3.

   </details>

3. The shaking class has 40 windows, split stratified (val = test = 0.15). How many windows go to train, val and test? *(single choice · objective 3)*
   - a) 28, 6, 6
   - b) 30, 5, 5
   - c) 26, 7, 7
   - d) 40, 0, 0

   <details><summary>Solution</summary>

   **a** — ⌊0.15 × 40⌋ = 6 go to test and 6 to val; the remaining 40 − 12 = 28 become train. Train always absorbs the remainder.

   </details>

4. Why must val be kept separate from test? *(single choice · objective 3)*
   - a) So train has less data
   - b) We look at val repeatedly while tuning, so val ends up mixed into our decisions. Only test, never touched, tells the real accuracy
   - c) val and test only differ in name
   - d) Because test must be bigger than train

   <details><summary>Solution</summary>

   **b** — val is used during training, so it starts leaning toward our tuning choices. Test is kept for a one-time exam at the end. If you peek at test while tuning, the numbers lie.

   </details>

5. Which code causes data leakage? *(single choice · objective 4)*
   - a) Split first, then normalize(Xtr, Xva, Xte), computing mean/std from Xtr
   - b) Normalize the whole X block with the mean/std of all the data, then split
   - c) Using rng.permutation before slicing each class
   - d) Setting a fixed seed for the split

   <details><summary>Solution</summary>

   **b** — mean/std computed including test lets test's statistics leak into the data used for training. You must fit on train, then apply to every set.

   </details>

## Lab

- [ ] Run `dataset_tools.py` with `--synthesize`, then reading the file, and note the number of samples, windows and class counts in your learning log.
- [ ] In Python, call `split()` on the resulting windows, then print `np.bincount` for all three sets, and check it matches your hand calculation.
- [ ] Write two lines explaining where the leak would occur if `normalize()` were called before `split()`.

## Going further

In lesson 5.2, we'll fill in `s11_dataset.py` to record a real dataset on the board while watching a balance bar, then split it on the PC.

Next lesson: [lesson 5.2 — Hands-on: recording a balanced dataset on the board, then splitting it on the PC](../l02-dataset-lab/README.md)

## Reflect

- If you collected walking gestures from several people, why should train/test be split by "person" instead of by sample?
- For a class that's rare in real work, such as the sound of failing machinery, how would you collect it to keep things balanced?
