---
id: edgeai-dev.m05.l05
lang: en
title: {th: 'ลงมือทำ: เติมสคริปต์ฝึกแล้วรันใน Docker', en: 'Hands-on: complete the training script and run it in Docker'}
summary: {th: 'เติมสี่ช่องใน s12_train.py ตรงสี่จังหวะของการฝึก คือ fit, representative dataset, int8 I/O และ accuracy แล้วรันใน Docker จนได้ model_int8.tflite กับรายงานความแม่น float32, int8 และ confusion matrix ของโมเดลที่เราฝึกเองทั้งตัว พร้อมทดลองลดจำนวน epoch และเปลี่ยนชุด calibrate', en: 'Fill the four points of s12_train.py that match the four beats of training (fit, representative dataset, int8 I/O and accuracy), run it in Docker until you get model_int8.tflite and a float32, int8 and confusion-matrix report for a model you trained yourself, then experiment with fewer epochs and a different calibration set.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: false, boards: [none]}
prerequisites: [edgeai-dev.m05.l04]
objectives:
  - {th: 'เติมสี่ช่องใน practice/s12_train.py จนรันใน Docker ได้ float32 test accuracy, int8 test accuracy, confusion matrix และไฟล์ model_int8.tflite กับ .norm.npz', en: 'Fill the four points in practice/s12_train.py so that a Docker run prints float32 test accuracy, int8 test accuracy and a confusion matrix and writes model_int8.tflite and its .norm.npz.'}
  - {th: รันเทียบ 3 epoch กับ 25 epoch แล้วจดความแม่นทั้งสองแบบ พร้อมอธิบายความต่างด้วยคำว่า underfit, en: 'Compare 3 and 25 epochs, record both accuracies and explain the difference in terms of underfitting.'}
  - {th: 'ระบุได้จากอาการว่าช่องใดยังว่าง (ความแม่นราว 0.33, ValueError ตอน convert, eval ป้อน int8 ไม่ผ่าน หรือ accuracy 0.000)', en: 'Tell from the symptom which point is still empty (accuracy near 0.33, a ValueError at convert, eval failing to feed int8, or accuracy 0.000).'}
develops: [{skill: ai.model-training, to: 3}, {skill: build.docker, to: 2}, {skill: lang.python, to: 2}]
assesses: [{skill: ai.model-training, level: 2, evidence: practice/s12_train.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: f321eb52684483b5606448b852ba97492de7f1bbf8dd426aa99f58f2de7f0a09
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 5.5 — Hands-on: complete the training script and run it in Docker

> Module 5 — Training and deploying to several targets · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Fill four points in s12_train.py matching training's four beats — fit, the representative dataset, int8 I/O and accuracy — then run it in Docker until you get model_int8.tflite and a float32, int8 and confusion-matrix report for a model you trained entirely yourself, and experiment with fewer epochs and a different calibration set.

## Objectives

By the end of this lesson, you will:

1. Fill the four points in practice/s12_train.py so a Docker run prints float32 test accuracy, int8 test accuracy and a confusion matrix, and writes model_int8.tflite and its .norm.npz.
2. Run once at 3 epochs and once at 25, record both accuracies, and explain the difference using the word underfitting.
3. Tell from the symptom which point is still empty (accuracy near 0.33, a ValueError at convert, eval failing to feed int8, or accuracy 0.000).

## Before you start

You've been through lesson 5.4, and understand the four beats: build, fit, convert, eval. Copy `practice/s12_train.py` into [`shared/training`](../../shared/training/), next to `dataset_tools.py`, and have `data/gestures.csv` ready.

- **Hardware:** your computer, no board needed — a PC with Docker installed. Without Docker, copy the blanks you fill in into a Colab notebook to try instead.
- **Prior lesson:** [lesson 5.4 — Inside training: Keras, Conv1D, gradient descent, int8 and the confusion matrix](../l04-inside-training/README.md)

## Concepts

The training file already gives you dataset_tools, `build_model`, and the quantize/dequantize sections in full. Four points remain, matching the four beats: (1) in `main()`, after `compile`, fill in `model.fit(Xtr, ytr, validation_data=(Xva, yva), epochs=a.epochs, batch_size=32, verbose=2)`. Forget this, and the model never learns — accuracy sits around 0.33 (guessing among three classes). (2) In `to_int8_tflite()`, fill in `conv.representative_dataset = representative`. Forget it, and `convert()` stops with a `ValueError`. (3) Fill in `conv.inference_input_type = tf.int8` and `conv.inference_output_type = tf.int8`. Forget it, and the input and output stay float32 (the scale in `quantization` is 0), so `eval_int8()`, which feeds int8, fails to run. (4) In `eval_int8()`, fill in `acc = (preds == yte).mean()`. Forget it, and it reports 0.000 even though the confusion matrix's diagonal might be entirely correct.

Run it with `docker run --rm -v "$PWD":/work edgeai-train python s12_train.py`, and you'll get `float32 test accuracy` → `int8 test accuracy` → a confusion matrix, and the files `model_int8.tflite` and `model_int8.tflite.norm.npz`. Success isn't just watching numbers run — you should be able to say why int8 should be close to float32, and what the representative dataset is for. This file is the artifact the next pair of lessons will carry into a browser and onto the board.

## Worked example

`s12_train_full.py` synthesizes its own data if `data/gestures.csv` doesn't exist yet, prints `model.summary()` and `count_params()`, warns when int8's accuracy drops more than `INT8_DROP_WARN = 0.05` below float32, and has an MVP gate that passes when int8 accuracy ≥ `MVP_MIN_ACC = 0.80` (returning exit code 0 or 1, usable in CI). It sits in `shared/training`, alongside the practice file.

| File | What this file teaches |
|---|---|
| [examples/s12_train_full.py](examples/s12_train_full.py) | Train + test a hand-gesture model, end to end (full version) |

This lesson's slides also reference files in another lesson and under `shared/`:

- [shared/training](../../shared/training)
- [shared/training/dataset_tools.py](../../shared/training/dataset_tools.py) — Dataset tools for the IMU gesture classifier (Pillar 4 / Training).
- [shared/training/eval_pc.py](../../shared/training/eval_pc.py) — Run the exported int8 .tflite on the PC and report accuracy + confusion.
- [shared/training/model_int8.tflite](../../shared/training/model_int8.tflite)

## Practice

The `# TODO:` comments are at lines 131 (point 1, `model.fit`), 53 (point 2, `representative_dataset`), 60 (point 3, int8 I/O), and 97 (point 4, `acc`). Fill them in one at a time and run it — the symptom of whichever point is still empty tells you which one's left.

| Practice file | Topic |
|---|---|
| [practice/s12_train.py](practice/s12_train.py) | Training our own model with TensorFlow, then testing it on the PC (the fill-in-the-code version) |

## Solution

Open the solution after trying on your own at least once, and read [how to use the solutions](../../README.en.md#how-to-use-the-solutions) first.

| Solution | Pairs with |
|---|---|
| [solution/s12_train.py](solution/s12_train.py) | [practice/s12_train.py](practice/s12_train.py) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. Every run gives float32 test accuracy: 0.333. Which point is still empty? *(single choice · objective 1)*
   - a) Point 1, model.fit
   - b) Point 2, representative_dataset
   - c) Point 3, int8 I/O
   - d) Point 4, acc

   <details><summary>Solution</summary>

   **a** — without fitting, the weights stay random, so the model guesses right about one time in three among three classes, and evaluate measures about 0.33.

   </details>

2. convert() stops with ValueError: For full integer quantization, a representative_dataset must be specified. Which point needs fixing? *(single choice · objective 3)*
   - a) Point 1
   - b) Point 2, fill in conv.representative_dataset = representative
   - c) Point 3
   - d) Point 4

   <details><summary>Solution</summary>

   **b** — the message says directly that full-integer compression needs samples to calibrate the value range against.

   </details>

3. The report says int8 test accuracy: 0.000, but the confusion matrix's diagonal is fully populated with correct numbers. Which point is still empty? *(single choice · objective 3)*
   - a) Point 1
   - b) Point 2
   - c) Point 3
   - d) Point 4, acc is still its starting value, 0.0

   <details><summary>Solution</summary>

   **d** — the confusion matrix is computed from the real preds, but the accuracy number comes from acc, still 0.0. It needs acc = (preds == yte).mean() filled in.

   </details>

4. Training for 3 epochs gives both accuracy and val_accuracy clearly lower than at 25 epochs. How would you explain this? *(single choice · objective 2)*
   - a) Overfitting
   - b) Underfitting, because training was too short — the loss hasn't finished descending yet
   - c) int8 dropped the accuracy
   - d) Data leakage

   <details><summary>Solution</summary>

   **b** — both train and val being low together is the symptom of underfitting. Giving the model more time to descend the loss's slope improves it.

   </details>

## Lab

**The MVP for lessons 5.3–5.5:** successfully train a Keras model in Docker, getting a report of float32 accuracy, int8 accuracy and a confusion matrix on a test set the model has never seen, along with the `model_int8.tflite` and `.norm.npz` files.

- [ ] All four points in the practice file are filled in, and running it in Docker produces the report and both files.
- [ ] Run with `--epochs 3` compared to 25 epochs, note both accuracies in your learning log, and explain the difference.
- [ ] Have `representative()` feed all-zero windows (`np.zeros_like(X_repr[i:i + 1])`) instead of real ones, and compare int8 accuracy against the original.
- [ ] Be able to explain where `fit`, `representative_dataset`, `inference_input_type` and accuracy sit, and what each does.

## Going further

In the next pair of lessons (5.6–5.7), we'll take this file and run it in a browser, prove its verdict matches the PC's, and tell the Cortex-A story.

Next lesson: [lesson 5.6 — Running a model on the web: LiteRT.js, int8 I/O and parity](../l06-web-runtime/README.md)

## Reflect

- How far apart are your int8 and float32 accuracies, and how much would you trust that number when the test set only has about twenty windows?
- If real data gives much lower accuracy than synthetic data, where would you start fixing it?
