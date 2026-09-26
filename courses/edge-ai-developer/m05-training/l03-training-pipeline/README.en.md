---
id: edgeai-dev.m05.l03
lang: en
title: {th: 'ฝึกโมเดลใน Docker: หนึ่งชิ้นงาน สี่เป้าหมาย', en: 'Training in Docker: one artifact, four targets'}
summary: {th: เลิกยืมโมเดลสำเร็จรูปแล้วฝึกของเราเอง เริ่มจากเหตุผลที่ต้องฝึกใน Docker ภาพรวม "หนึ่งชิ้นงาน สี่เป้าหมาย" ของ model_int8.tflite แล้วรัน train.py กับ eval_pc.py ของจริง (หรือบน Colab) ก่อนเข้าใจ อ่าน log ให้ออกว่าแต่ละบรรทัดบอกอะไร, en: 'Stop borrowing ready-made models and train your own. Start with why training runs in Docker and the "one artifact, four targets" picture of model_int8.tflite, then run the real train.py and eval_pc.py (or Colab) before understanding them, and learn to read every line of the log.'}
level: L3
time_min: {concept: 30, practise: 25, check: 10}
hardware: {emulator: false, boards: [none]}
prerequisites: [edgeai-dev.m05.l02]
objectives:
  - {th: 'บอกเหตุผลที่ฝึกใน Docker ได้อย่างน้อยสองข้อ และอธิบายหน้าที่ของ -v "$PWD":/work กับ --rm ในคำสั่ง docker run', en: 'Give at least two reasons to train inside Docker, and explain what -v "$PWD":/work and --rm do in the docker run command.'}
  - {th: 'วาดแผนผังหนึ่งชิ้นงานสี่เป้าหมาย (MCU, PC, Web, Cortex-A) ของ model_int8.tflite และบอกได้ว่าทำไมมีแค่ MCU ที่ต้องผ่าน Vela', en: 'Draw the one-artifact, four-target map of model_int8.tflite (MCU, PC, web, Cortex-A) and say why only the MCU needs Vela.'}
  - {th: รัน train.py และ eval_pc.py (ใน Docker หรือบน Colab) แล้วจดจำนวนหน้าต่างแต่ละกอง ความแม่น float32 และ int8 ขนาดไฟล์ และไฟล์ที่ต้องเดินทางคู่กับโมเดล, en: 'Run train.py and eval_pc.py (in Docker or on Colab) and record the window count of each set, the float32 and int8 accuracy, the file size and the file that must travel with the model.'}
develops: [{skill: build.docker, to: 2}, {skill: ai.model-training, to: 2}, {skill: ai.model-deploy, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: 8e53d4fcb64c5fd6e0a15821b84f37a5a0bb9b725bc02064edcfa867d9bfb73e
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 5.3 — Training in Docker: one artifact, four targets

> Module 5 — Training and deploying to several targets · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Stop borrowing ready-made models and train our own. Start with why training runs in Docker, the "one artifact, four targets" picture of model_int8.tflite, then run the real train.py and eval_pc.py (or on Colab) before understanding them, and learn to read what every line of the log tells you.

## Objectives

By the end of this lesson, you will:

1. Give at least two reasons to train inside Docker, and explain what -v "$PWD":/work and --rm do in the docker run command.
2. Draw the one-artifact, four-target map of model_int8.tflite (MCU, PC, web, Cortex-A), and say why only the MCU needs Vela.
3. Run train.py and eval_pc.py (in Docker or on Colab), and record the window count of each set, the float32 and int8 accuracy, the file size, and the file that must travel alongside the model.

## Before you start

You've been through lessons 5.1–5.2, and have `data/gestures.csv` from the board, or can create a synthetic set with `python dataset_tools.py --synthesize --out data/gestures.csv`. Have Docker installed (the first run downloads several hundred MB of TensorFlow), or a Google Colab notebook ready.

- **Hardware:** your computer, no board needed — a PC with Docker installed, or a Google account for Colab.
- **Prior lesson:** [lesson 5.2 — Hands-on: capture a balanced dataset on the board, split it on the PC](../l02-dataset-lab/README.md)

## See it work first

In the [`shared/training`](../../shared/training/) folder, run `docker build -t edgeai-train .` once, then `docker run --rm -v "$PWD":/work edgeai-train python train.py --data data/gestures.csv --out model_int8.tflite`. Watch accuracy climb every epoch until a `model_int8.tflite` file, roughly 11 KB, appears in the folder on your own machine — before knowing what's happening inside.

## Concepts

Training needs TensorFlow plus a dozen other libraries, and every machine's versions mismatch just enough to produce "it runs on my machine." **Docker** fixes this with a single image: the `Dockerfile` starts from `python:3.11-slim`, installs `tensorflow`, `ai-edge-litert`, `numpy`, `scikit-learn`, and installs `ethos-u-vela` as a separate layer. Everyone gets the same versions on macOS, Windows and Linux, without cluttering their machine — and it can be deleted. `-v "$PWD":/work` places the current folder inside the container, so code, data and results all live in the same place. `--rm` deletes the container when it's done. If you don't have Docker yet, use the [`train_edge_ai.ipynb`](../../shared/training/notebooks/train_edge_ai.ipynb) notebook on Google Colab instead (the notebook synthesizes its own data in units of g, so it's good for practising the pipeline, but a model meant for the board must be trained from the board's own CSV).

The whole module revolves around one file, `model_int8.tflite`, following **train once, run everywhere**: the PC runs it with `eval_pc.py` via `ai-edge-litert`; Cortex-A (Raspberry Pi, Jetson) runs the same file with the same kind of script; the browser uses the version `convert_web.py` prepares; and the MCU needs an extra compile step with `quantize_vela.sh` (Vela), because the Ethos-U55 needs a graph converted into NPU ops. The resulting `_vela.tflite` file therefore only works on the MCU.

`train.py`'s log, with the synthetic set, tells you line by line: `train/val/test windows: 101 21 21` is the window count for the three sets; every epoch has `accuracy` paired with `val_accuracy`, which should climb together; then `float32 test accuracy` on the set the model has never seen; the size of the file written (the course's reference file is 11,504 bytes); and `model_int8.tflite.norm.npz`, which stores the mean/std. This file must always travel with the model. `eval_pc.py` runs the real int8 file and prints `int8 test accuracy` along with a confusion matrix — this is the ground truth before taking it anywhere else. The synthetic set separates classes easily, so the numbers look great; real data having some confusion is normal.

## Worked example

This lesson's slides also reference files in another lesson and under `shared/`:

- [m05-training/l05-train-lab/practice/s12_train.py](../l05-train-lab/practice/s12_train.py) — training our own model with TensorFlow, then testing it on the PC (the fill-in-the-code version)
- [shared/training](../../shared/training)
- [shared/training/dataset_tools.py](../../shared/training/dataset_tools.py) — Dataset tools for the IMU gesture classifier (Pillar 4 / Training).
- [shared/training/eval_pc.py](../../shared/training/eval_pc.py) — Run the exported int8 .tflite on the PC and report accuracy + confusion.
- [shared/training/model_int8.tflite](../../shared/training/model_int8.tflite)
- [shared/training/notebooks/train_edge_ai.ipynb](../../shared/training/notebooks/train_edge_ai.ipynb)
- [shared/training/train.py](../../shared/training/train.py) — Train a tiny IMU gesture classifier and export it as int8 TFLite.

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. In docker run --rm -v "$PWD":/work edgeai-train python train.py, what does -v "$PWD":/work do? *(single choice · objective 1)*
   - a) Deletes the container when it's done
   - b) Places the current folder on your machine at /work inside the container, so code, data and results all share the same place
   - c) Names the image
   - d) Installs TensorFlow on your machine

   <details><summary>Solution</summary>

   **b** — the bind mount means the model_int8.tflite file written inside /work appears on your machine right away. --rm deletes the container, and -t during build names the image.

   </details>

2. Which target needs to compile model_int8.tflite an extra step before use? *(single choice · objective 2)*
   - a) A PC, via ai-edge-litert
   - b) Cortex-A, such as a Raspberry Pi
   - c) An MCU using the Ethos-U55, which needs Vela
   - d) No target needs anything extra

   <details><summary>Solution</summary>

   **c** — Vela converts the parts the NPU can run into Ethos-U ops. The resulting file therefore only runs on the MCU; PC and Cortex-A use the same int8 file directly.

   </details>

3. The log says float32 test accuracy 0.980, but eval_pc.py says int8 test accuracy 0.600. What should you suspect first? *(single choice · objective 3)*
   - a) The data is unbalanced
   - b) Something's wrong with the int8 compression (calibration, or a mismatched normalize)
   - c) Docker is too slow
   - d) Nothing's wrong — int8 should always be much less accurate

   <details><summary>Solution</summary>

   **b** — the same model should get int8 accuracy close to float32. If it drops sharply, check the representative dataset and the `.norm.npz` file used to normalize at test time.

   </details>

4. Which file must travel alongside model_int8.tflite to every target? *(single choice · objective 3)*
   - a) The Dockerfile
   - b) model_int8.tflite.norm.npz, which holds the training set's mean/std
   - c) The whole gestures.csv file
   - d) train.py

   <details><summary>Solution</summary>

   **b** — whoever uses the model must normalize data with the same mean/std used during training, or the model won't error out — it'll just quietly predict wrong.

   </details>

## Lab

- [ ] Build the image, then run `train.py` and `eval_pc.py` (or run the Colab notebook to the end), and note every number the log explains into your learning log.
- [ ] Draw a map from `model_int8.tflite` to the four targets, writing the name of the script for each path.
- [ ] Delete `model_int8.tflite.norm.npz`, then run `eval_pc.py` again. Note what happens, and why.

## Going further

In lesson 5.4, we'll open `train.py` and take apart its four beats — build, fit, convert, eval — along with the maths behind each one.

Next lesson: [lesson 5.4 — Inside training: Keras, Conv1D, gradient descent, int8 and the confusion matrix](../l04-inside-training/README.md)

## Reflect

- What other work have you run into "it runs on my machine" problems with? Could Docker have helped?
- If you had to send a model to a web team and a firmware team at the same time, which files would you send to whom?
