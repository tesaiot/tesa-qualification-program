---
id: edgeai-dev.m05.l02
lang: en
title: {th: 'ลงมือทำ: เก็บ dataset ที่สมดุลบนบอร์ดแล้วแบ่งบน PC', en: 'Hands-on: capture a balanced dataset on the board, split it on the PC'}
summary: {th: เติมสี่จุดใน s11_dataset.py ให้อ่าน IMU เขียน CSV นับจำนวนต่อคลาส และนำทางให้เก็บคลาสที่ยังน้อย จนได้ /gestures.csv สามคลาสที่สมดุลจากบอร์ด แล้วคัดลอกมาแบ่ง train/val/test บน PC พร้อมพิสูจน์ด้วย np.bincount ว่าทุกกองครบทุกคลาส, en: 'Fill four points in s11_dataset.py to read the IMU, write the CSV, count per class and steer you to the class that is short, until the board gives a balanced three-class /gestures.csv; then copy it to the PC, split it into train/val/test and prove with np.bincount that every set holds every class.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m05.l01]
objectives:
  - {th: เติมสี่จุดใน practice/s11_dataset.py จนกดปุ่ม label แล้ว /gestures.csv ได้ 200 บรรทัดใหม่ที่ค่าไม่เป็นศูนย์ แถบสมดุลขยับ และคำใบ้ชี้คลาสที่มีน้อยที่สุด, en: 'Fill the four points in practice/s11_dataset.py so each label press adds 200 non-zero lines to /gestures.csv, the balance bars move and the hint names the class with the fewest samples.'}
  - {th: เก็บ dataset จากบอร์ดให้ครบสามคลาสถึงเป้า แล้วบน PC รัน load_csv → make_windows → split → normalize ตามลำดับ และแสดง np.bincount ของทั้งสามกองที่มีครบทุกคลาส, en: 'Capture a dataset on the board with all three classes at target, then on the PC run load_csv → make_windows → split → normalize in that order and show an np.bincount for all three sets with every class present.'}
  - {th: ทดลองเก็บให้ไม่สมดุลโดยตั้งใจ แล้วอธิบายจากตัวเลขได้ว่าทำไม split แบบ stratified พาความไม่สมดุลไปทุกกอง และต้องแก้ตอนเก็บ, en: Capture an unbalanced dataset on purpose and use the numbers to explain why a stratified split carries the imbalance into every set and must be fixed at capture time.}
develops: [{skill: ai.data-collection, to: 3}, {skill: lang.micropython, to: 2}, {skill: lang.python, to: 2}]
assesses: [{skill: ai.data-collection, level: 2, evidence: practice/s11_dataset.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: 09126a3c454f996a6ce97c94a3e7ebed7507cd8b76144c15ec4bc18a1ec4565d
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 5.2 — Hands-on: capture a balanced dataset on the board, split it on the PC

> Module 5 — Training and deploying to several targets · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Fill four points in s11_dataset.py to read the IMU, write the CSV, count per class, and steer you toward the class that's still short, until the board gives a balanced three-class /gestures.csv, then copy it over and split it into train/val/test on the PC, proving with np.bincount that every set holds every class.

## Objectives

By the end of this lesson, you will:

1. Fill the four points in practice/s11_dataset.py so that pressing a label button adds 200 new, non-zero lines to /gestures.csv, the balance bars move, and the hint names the class with the fewest samples.
2. Capture a dataset on the board with all three classes reaching target, then on the PC run load_csv → make_windows → split → normalize in that order, and show an np.bincount for all three sets with every class present.
3. Deliberately capture an unbalanced dataset, and use the numbers to explain why a stratified split carries the imbalance into every set, and why it must be fixed at capture time.

## Before you start

You've been through lesson 5.1, and understand class balance, stratified splitting, and the no-leakage rule. Have a PC with Python 3, numpy, and [`dataset_tools.py`](../../shared/training/dataset_tools.py) ready, and a board if you'll capture real data.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — the emulator simulates the IMU well enough to practise filling in the code and pressing label buttons, but a dataset meant for training a real model must be captured from the board's IMU.
- **Prior lesson:** [lesson 5.1 — Dataset engineering: class balance, windows and the train/val/test split](../l01-dataset-engineering/README.md)

## Concepts

The whole file reads as one sentence: choose a label → read the IMU in a burst → write it to CSV → count per class → say which class is still short → every class at target means the dataset is ready. The skeleton is still the same four beats (import → create once → loop → `ui.poll`). What's new is inside `record()`. The first two points are carried over from the DAQ logger: (1) `ax, ay, az, gx, gy, gz = sensors.bmi270.motion()`, giving accel in m/s² (`az` around 9.81 at rest) and gyro in deg/s (2) `f.write("%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n" % (label, ax, ay, az, gx, gy, gz))`, whose column order must match `CHANNELS`, and whose label must spell exactly like `CLASSES`, since `load_csv()` uses `CLASSES.index(label)` — spelling `Idle` with a capital already errors out.

The last two points are the brains of dataset engineering: (3) `counts[label] += BURST` after finishing a burst, which is what makes the balance bars move, and (4) `fewest = min(counts, key=counts.get)`, which loops over every key and returns the **class name** with the smallest count, letting the program say what to collect next. Record at 20 ms per sample (50 Hz), matching the Motion model — at a different rate, the same motion stretches or shrinks inside a window.

Once you've captured enough, copy `/gestures.csv` off the board (BENTO IDE's file transfer, or `mpremote`) to `data/gestures.csv` on the PC, then call `load_csv` → `make_windows` → `split` → `normalize(Xtr, Xva, Xte)`. **Always split before normalize.** Finish with a report of `np.bincount` for all three sets. If any set is missing a class — for example, test showing `[20 20 0]` — it means `shaking` wasn't captured enough, and you need to go back and capture more on the board.

## Worked example

`s11_dataset_full.py` adds a red warning when the smallest class drops below 70% of the largest (`BALANCE_TOL = 0.30`), shows the min/max balance ratio, estimates the window count using the same formula as `make_windows()`, and has a Clear button. Worth knowing: the counters start at zero every time it runs, even if the existing file already has data in it.

| File | What this file teaches |
|---|---|
| [examples/s11_dataset_full.py](examples/s11_dataset_full.py) | Recording a balanced, train-ready IMU dataset to CSV (full version) |

This lesson's slides also reference files in another lesson and under `shared/`:

- [shared/training/dataset_tools.py](../../shared/training/dataset_tools.py) — Dataset tools for the IMU gesture classifier (Pillar 4 / Training).
- [shared/training/train.py](../../shared/training/train.py) — Train a tiny IMU gesture classifier and export it as int8 TFLite.

## Practice

The `# TODO:` comments are at lines 67 (finding `fewest`), 84 (reading `motion()`), 88 (`f.write`), and 93 (`counts[label] += BURST`). If the CSV is all 0.0, point 84 is still empty. If the bars never move, point 93 is still empty. If the hint always points at `idle`, point 67 is still empty.

| Practice file | Topic |
|---|---|
| [practice/s11_dataset.py](practice/s11_dataset.py) | Recording an IMU dataset that's "balanced and ready to train" to CSV (the fill-in-the-code version) |

## Solution

Open the solution after trying on your own at least once, and read [how to use the solutions](../../README.en.md#how-to-use-the-solutions) first.

| Solution | Pairs with |
|---|---|
| [solution/s11_dataset.py](solution/s11_dataset.py) | [practice/s11_dataset.py](practice/s11_dataset.py) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. You press a label button, and the balance bar never moves, even though the file gains lines. Which point is still empty? *(single choice · objective 1)*
   - a) ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
   - b) f.write(...)
   - c) counts[label] += BURST
   - d) fewest = min(counts, key=counts.get)

   <details><summary>Solution</summary>

   **c** — the bar reads from counts. If BURST is never added to the counter, the file grows but the program has no idea how much was captured — capturing blind.

   </details>

2. counts = {'idle': 600, 'circle': 200, 'shaking': 400}. What does min(counts, key=counts.get) return? *(single choice · objective 1)*
   - a) 200
   - b) 'circle'
   - c) 'idle'
   - d) ('circle', 200)

   <details><summary>Solution</summary>

   **b** — min loops over the dict's keys but compares using counts.get, so it returns the class name with the smallest count, not the number. The hint therefore says to capture more circle.

   </details>

3. Put the PC-side steps in order so there's no data leakage *(ordering · objective 2)*
   - a) split(X, y)
   - b) load_csv("data/gestures.csv")
   - c) normalize(Xtr, Xva, Xte)
   - d) make_windows(s, l)

   <details><summary>Solution</summary>

   **b → d → a → c** — read the file → slice into windows → split into sets → normalize using train's statistics. If normalize ran before split, test's statistics would leak in.

   </details>

4. You capture idle at three times the rate of the other classes, then split stratified. What's the result? *(single choice · objective 3)*
   - a) The split automatically balances every set
   - b) Every set gets idle at roughly three times the other classes too — the imbalance follows into every set
   - c) test ends up with no idle at all
   - d) The program errors out

   <details><summary>Solution</summary>

   **b** — a stratified split preserves each class's original proportion in every set, so it never fixes imbalance. It has to be fixed at capture time.

   </details>

## Lab

**The MVP for lessons 5.1–5.2:** a clean, balanced, split dataset from the board — every set (train/val/test) has all three classes in close-to-equal proportion.

- [ ] All four points in the practice file are filled in. Try it on the emulator first, then capture real data on the board until all three classes reach `TARGET`.
- [ ] Copy `gestures.csv` to the PC, run split, and print `np.bincount` for all three sets into your learning log.
- [ ] Capture another file with `idle` deliberately at three times the other classes, compare the proportions across the three sets, and explain why the imbalance doesn't disappear on its own.
- [ ] Be able to explain why balance matters, why three sets are needed, and why normalize must fit on train only.

## Going further

In the next pair of lessons (5.3–5.5), we'll take this dataset and train it into a real model with TensorFlow in Docker, then export it as an int8 `.tflite`.

Next lesson: [lesson 5.3 — Training a model in Docker: one artifact, four targets](../l03-training-pipeline/README.md)

## Reflect

- How many windows does your dataset hold in total? Do you think that's enough for a small model, and how would you know?
- If you had to add a fourth class, such as `tap`, which files would you need to change, on both the board side and the PC side?
