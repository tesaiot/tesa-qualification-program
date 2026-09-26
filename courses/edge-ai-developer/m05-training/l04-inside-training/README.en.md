---
id: edgeai-dev.m05.l04
lang: en
title: {th: 'ข้างในการฝึก: Keras, Conv1D, gradient descent, int8 และ confusion matrix', en: 'Inside training: Keras, Conv1D, gradient descent, int8 and the confusion matrix'}
summary: {th: 'เปิด train.py แกะสี่จังหวะ build, fit, convert และ eval พร้อมคณิตเบื้องหลัง ได้แก่สมการ Conv1D, softmax, cross-entropy, gradient descent และการบีบ int8 ด้วย scale กับ zero-point รู้ว่าทำไม representative dataset จำเป็น ทำไม normalization เป็นส่วนหนึ่งของโมเดล และอ่าน learning curve กับ confusion matrix ให้เป็น', en: 'Open train.py and take apart its four beats (build, fit, convert, eval) with the maths behind them - the Conv1D equation, softmax, cross-entropy, gradient descent and int8 quantization with scale and zero-point. Learn why the representative dataset is required, why normalization is part of the model, and how to read learning curves and a confusion matrix.'}
level: L3
time_min: {concept: 50, practise: 10, check: 10}
hardware: {emulator: false, boards: [none]}
prerequisites: [edgeai-dev.m05.l03]
objectives:
  - {th: 'คำนวณค่าออกของ Conv1D หนึ่งตำแหน่งด้วยมือจาก y[t] = Σ w[k]·x[t+k] + b และนับจำนวนพารามิเตอร์ของชั้น Conv1D กับ Dense ได้', en: 'Compute one Conv1D output by hand with y[t] = Σ w[k]·x[t+k] + b, and count the parameters of a Conv1D and a Dense layer.'}
  - {th: คำนวณ softmax ของคะแนนสามคลาส และแปลความ learning curve ว่าเป็นแบบดี overfit หรือ underfit, en: 'Compute the softmax of three class scores, and interpret a learning curve as healthy, overfitting or underfitting.'}
  - {th: อธิบายการบีบ int8 แบบ full-integer ด้วย real ≈ scale × (q − zero_point) และบอกหน้าที่ของ representative_dataset กับ inference_input_type, en: 'Explain full-integer int8 quantization with real ≈ scale × (q − zero_point), and state the job of representative_dataset and inference_input_type.'}
  - {th: อ่าน confusion matrix แล้วคำนวณความแม่นและระบุคู่คลาสที่โมเดลสับสนได้, en: 'Read a confusion matrix, compute the accuracy and name the pair of classes the model confuses.'}
develops: [{skill: ai.model-training, to: 3}, {skill: hw.math, to: 3}, {skill: ai.model-deploy, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: 0a960c6f1f1be71bf117f96875c73d5970fb1b63acbe0a1dc94692ff69fb5b66
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 5.4 — Inside training: Keras, Conv1D, gradient descent, int8 and the confusion matrix

> Module 5 — Training and deploying to several targets · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Open train.py and take apart its four beats — build, fit, convert and eval — with the maths behind them: the Conv1D equation, softmax, cross-entropy, gradient descent, and int8 compression with scale and zero-point. Know why the representative dataset is needed, why normalization is part of the model, and learn to read a learning curve and a confusion matrix.

## Objectives

By the end of this lesson, you will:

1. Compute one Conv1D output by hand with y[t] = Σ w[k]·x[t+k] + b, and count the parameters of a Conv1D layer and a Dense layer.
2. Compute the softmax of three class scores, and interpret a learning curve as healthy, overfitting or underfitting.
3. Explain full-integer int8 quantization with real ≈ scale × (q − zero_point), and state the job of representative_dataset and inference_input_type.
4. Read a confusion matrix, compute the accuracy, and name the pair of classes the model confuses.

## Before you start

You've been through lesson 5.3, and have already run `train.py` and seen its log. Open [`train.py`](../../shared/training/train.py) alongside the slides, and if you have time, download [`math_lab.html`](../../shared/interactive/math_lab.html) and open it in a browser (needs internet to load GeoGebra).

- **Hardware:** your computer, no board needed — read the code alongside the slides on a PC. If you have time, download math_lab.html and open it in a browser to play with the graphs.
- **Prior lesson:** [lesson 5.3 — Training in Docker: one artifact, four targets](../l03-training-pipeline/README.md)

## Concepts

`train.py` reads as four beats: **build → fit → convert → eval.** The build beat lays out a 1-D CNN with `tf.keras.Sequential`: input `(50, 6)` → `Conv1D(16, 5)` → `MaxPooling1D(2)` → `Conv1D(32, 3)` → `GlobalAveragePooling1D` → `Dense(32)` → `Dense(3, softmax)`. Every layer is an op the Ethos-U55 can accelerate, totalling about 3,200 parameters (the first Conv1D: 5·6·16 + 16 = 496). Conv1D is $y[t] = \sum_{k=0}^{K-1} w[k]\,x[t+k] + b$ — one filter sliding along time, producing a high output when that stretch resembles the filter's shape. For example, kernel `[.2 .5 .3]` on `.1 .4 .8` gives `.46` (b = 0).

The fit beat loops through three equations every batch: **softmax**, $\hat{y}_i = e^{z_i}/\sum_j e^{z_j}$, turns raw scores into probabilities that add up to 1; **cross-entropy**, $L = -\sum_i y_i \log \hat{y}_i$, measures how far a prediction is from the answer; and **gradient descent**, $\theta \leftarrow \theta - \eta\,\nabla_\theta L$, moves the weights downhill on the loss (`adam` is an optimizer in this family). `epochs=25`, `batch_size=32` and `validation_data` let us read the learning curve: `accuracy` and `val_accuracy` rising together is healthy; train high but val low or falling is overfitting; both stuck low is underfitting.

The convert beat compresses float32 into **int8** with $real \approx scale \times (q - zero\_point)$, roughly four times smaller and accelerable by the NPU. The converter must **calibrate** the activation value range from a `representative_dataset` (200 real windows from the training set). If `TFLITE_BUILTINS_INT8` is set but this set is never attached, `convert()` stops with a `ValueError`. `inference_input_type = tf.int8` and `inference_output_type = tf.int8` make the input and output pure int8. The normalize step's mean/std are saved to `.norm.npz`, because normalization is part of the model — whoever uses it must use the same values. The eval beat quantizes the input with the file's scale/zero-point, runs it, then dequantizes the output before `argmax`. The summary is a **confusion matrix**: rows are the true class, columns are the predicted class, the diagonal is correct predictions, and off-diagonal cells tell you which pair needs more data.

## Worked example

This lesson's slides also reference files in another lesson and under `shared/`:

- [m05-training/l05-train-lab/practice/s12_train.py](../l05-train-lab/practice/s12_train.py) — training our own model with TensorFlow, then testing it on the PC (the fill-in-the-code version)
- [shared/interactive/math_lab.html](../../shared/interactive/math_lab.html)
- [shared/training/train.py](../../shared/training/train.py) — Train a tiny IMU gesture classifier and export it as int8 TFLite.

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. kernel w = [.2, .5, .3] and b = 0, over the signal .4 .8 .6. What's the output? *(single choice · objective 1)*
   - a) 0.46
   - b) 0.52
   - c) 0.66
   - d) 1.80

   <details><summary>Solution</summary>

   **c** — .2×.4 + .5×.8 + .3×.6 = .08 + .40 + .18 = .66. Multiply, then add, position by position.

   </details>

2. Raw scores z = [2.0, 3.1, 1.2] for idle, circle, shaking. After softmax, what's circle's probability, roughly? *(single choice · objective 2)*
   - a) 0.31
   - b) 0.49
   - c) 0.67
   - d) 1.00

   <details><summary>Solution</summary>

   **c** — e^3.1 ≈ 22.2, divided by e^2.0 + e^3.1 + e^1.2 ≈ 7.39 + 22.2 + 3.32 ≈ 32.9, giving about 0.67. idle is about 0.22, and shaking about 0.10.

   </details>

3. Training finishes with accuracy = 0.99, but val_accuracy = 0.60 and keeps dropping near the end. What does that mean? *(single choice · objective 2)*
   - a) The model is excellent
   - b) Overfitting — the model has memorized the training set but doesn't generalize
   - c) Underfitting — the model is too small
   - d) The representative dataset is wrong

   <details><summary>Solution</summary>

   **b** — high train but val not following means it's memorizing the exam. Fix it with more data, stopping earlier, or a smaller model. Underfitting is both staying stuck low instead.

   </details>

4. You set supported_ops = [TFLITE_BUILTINS_INT8] but forget to attach representative_dataset, then call convert(). What happens? *(single choice · objective 3)*
   - a) You get a file with the same accuracy
   - b) The converter stops with a ValueError, because full-integer needs samples to calibrate against
   - c) You get a float32 file
   - d) The file shrinks eight times smaller

   <details><summary>Solution</summary>

   **b** — with no samples, the converter can't choose the activation's scale and zero-point, so TensorFlow refuses right away. If given samples that don't resemble reality, the file comes out but accuracy suffers.

   </details>

5. Confusion matrix: idle [10 0 0], circle [0 8 2], shaking [0 1 9]. What's the accuracy, and which pair is most confused? *(single choice · objective 4)*
   - a) 0.90 accuracy, and the model most often mistakes circle for shaking
   - b) 0.90 accuracy, and the model mistakes idle most often
   - c) 0.27 accuracy, and no pair is confused
   - d) 1.00 accuracy

   <details><summary>Solution</summary>

   **a** — the diagonal, 10 + 8 + 9 = 27 out of 30, is 0.90. circle's row has 2 windows predicted as shaking — worth collecting more of these two motions.

   </details>

## Lab

- [ ] Compute three more Conv1D outputs for kernel `[.2 .5 .3]` over `.1 .4 .8 .6 .2 .3`, and compare against an animation.
- [ ] Count the parameters of every layer in the model by hand, and compare against `model.count_params()`, which the full version prints out.
- [ ] Compute the softmax of `[2.0, 3.1, 1.2]` and the loss when the answer is circle, and note it in your learning log.

## Going further

In lesson 5.5, we'll fill four blanks in `s12_train.py` to complete all four beats, then run it in Docker until we have our own model.

Next lesson: [lesson 5.5 — Hands-on: fill in a training script and run it in Docker](../l05-train-lab/README.md)

## Reflect

- If a confusion matrix on real data often confuses circle with shaking, would you fix the data or the model first, and why?
- Why is normalizing with the wrong mean/std set a bug that's harder to find than a program error?
