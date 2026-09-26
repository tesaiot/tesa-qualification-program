---
id: edgeai-dev.m05.l06
lang: en
title: {th: 'รันโมเดลบนเว็บ: LiteRT.js, int8 I/O และ parity', en: 'Running the model on the web: LiteRT.js, int8 I/O and parity'}
summary: {th: 'พาโมเดลตัวเดิมไปรันในเบราว์เซอร์ เลือก runtime อย่างมีเหตุผล (LiteRT.js, ONNX Runtime Web, tfjs-tflite, WebNN) เข้าใจกับดัก int8 I/O ที่ทำให้ต้องมีไฟล์ web อีกใบ front-end ที่อยู่นอกกราฟ คณิตของ quantize กับ dequantize และนิยาม parity ที่วัดด้วย max-abs-diff กับเกณฑ์ TOL', en: 'Take the same model into the browser. Choose a runtime with reasons (LiteRT.js, ONNX Runtime Web, tfjs-tflite, WebNN), understand the int8 I/O trap that calls for a second web file, the front-end that lives outside the graph, the maths of quantize and dequantize, and parity defined by max-abs-diff against a TOL.'}
level: L3
time_min: {concept: 50, practise: 10, check: 10}
hardware: {emulator: true, boards: [none]}
prerequisites: [edgeai-dev.m05.l05]
objectives:
  - {th: เปรียบเทียบ runtime บนเบราว์เซอร์สี่ตัวและให้เหตุผลการเลือกได้ รวมถึงอธิบายว่าทำไม BENTO Emulator จึงแปลงโมเดลเป็น ONNX แล้วรันด้วย ONNX Runtime Web, en: 'Compare four browser runtimes and justify a choice, including why the BENTO Emulator converts the model to ONNX and runs it with ONNX Runtime Web.'}
  - {th: อธิบายว่าทำไมโมเดล int8 เต็มของ MCU อาจต้องมีไฟล์ web อีกใบ และ convert_web.py สร้างไฟล์ weight-only int8 ที่ I/O เป็น float จากน้ำหนัก Keras ชุดเดียวกันอย่างไร, en: 'Explain why the MCU''s full-integer int8 model may need a second web file, and how convert_web.py builds a weight-only int8 file with float I/O from the same Keras weights.'}
  - {th: 'คำนวณ quantize q = clip(round(x/s + z), −128, 127) และ dequantize x̂ = (q − z)·s จากค่า scale และ zero-point ที่กำหนด', en: 'Compute quantize q = clip(round(x/s + z), −128, 127) and dequantize x̂ = (q − z)·s from a given scale and zero-point.'}
  - {th: ตัดสิน parity ด้วย d = max|s_pc − s_web| ≤ TOL และคลาสที่ชนะตรงกัน พร้อมอธิบายว่าทำไม d ไม่จำเป็นต้องเป็นศูนย์ และทำไม front-end คือจุดที่พังบ่อยที่สุด, en: 'Judge parity by d = max|s_pc − s_web| ≤ TOL with the same winning class, and explain why d need not be zero and why the front-end is where parity breaks most often.'}
develops: [{skill: ai.model-deploy, to: 3}, {skill: hw.math, to: 2}, {skill: ai.edge, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: 543aa3fb4feafccf25c8d1cfae577bc197d7f59a5d789a4faa02d1d7dba30bec
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 5.6 — Running the model on the web: LiteRT.js, int8 I/O and parity

> Module 5 — Training and deploying to several targets · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Take the same model into the browser. Choose a runtime with reasons (LiteRT.js, ONNX Runtime Web, tfjs-tflite, WebNN), understand the int8 I/O trap that calls for a second web file, the front-end that lives outside the graph, the maths of quantize and dequantize, and parity defined by max-abs-diff against a TOL.

## Objectives

By the end of this lesson, you will:

1. Compare four browser runtimes and justify a choice, including why the BENTO Emulator converts the model to ONNX and runs it with ONNX Runtime Web.
2. Explain why the MCU's full-integer int8 model may need a second web file, and how convert_web.py builds a weight-only int8 file with float I/O from the same Keras weights.
3. Compute quantize q = clip(round(x/s + z), −128, 127) and dequantize x̂ = (q − z)·s from a given scale and zero-point.
4. Judge parity by d = max|s_pc − s_web| ≤ TOL with the same winning class, and explain why d need not be zero, and why the front-end is where parity breaks most often.

## Before you start

You've been through lessons 5.3–5.5, and have `model_int8.tflite` and `model_int8.tflite.norm.npz`. If you'll make a web file, run `train.py --save-keras` to get `model.keras`. Open the BENTO Emulator, select the Motion model, and flip the REAL switch on to watch alongside.

- **Hardware:** your computer, no board needed (or use the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) alongside it) — a PC and a browser. The BENTO Emulator is used to watch an example hand-gesture model actually running in the browser.
- **Prior lesson:** [lesson 5.5 — Hands-on: complete the training script and run it in Docker](../l05-train-lab/README.md)

## See it work first

In the BENTO Emulator's Edge AI panel, select the Motion model and flip the REAL switch on (the label changes from MOCK to REAL). The three-class confidence bars will move with the simulated IMU. This is a hand-gesture model trained with the same pipeline as ours, running in a browser tab with no server. Ask yourself: how does it know the model's mean/std and scale?

## Concepts

A browser model needs no installation — send a link, and a verdict is right there to try before flashing anything, and data never leaves the user's machine. The author surveyed the runtimes as follows: **LiteRT.js** (`@litertjs/core`) loads a `.tflite` file — the same format as the MCU — via WASM or WebGPU, with `loadLiteRt()`, `loadAndCompile()` and `run()`, making it the primary choice. `@tensorflow/tfjs-tflite` is no longer developed. **ONNX Runtime Web** is fully mature and handles int8 well, but needs an extra step converting TFLite to ONNX. WebNN isn't yet production-ready. The BENTO Emulator chose ONNX Runtime Web's path: convert `model_int8.tflite` with `tf2onnx` once (int8 in/out), then build the front-end itself in JS.

The MCU's model is **full-integer int8** (int8 in/out), as the Ethos-U55 requires. The author found that LiteRT.js accepts I/O as float32/int32, so this file might fail to load. `convert_web.py` fixes this by converting the **same Keras model** into `model_web.tflite`, dynamic-range style (`Optimize.DEFAULT` with no representative dataset) — weights are int8, but I/O is float, roughly four times smaller than pure float, and built from the exact same weights as the MCU's. What makes a file "browser-clean" is having no NPU custom ops; a file that's already been through Vela is therefore kept for the MCU only.

The graph only ever sees an already-prepared feature — **the front-end lives outside the graph.** Ours is normalizing with mean/std from `.norm.npz` (audio models carry a much heavier front-end: FFT, Mel, log). An int8 file needs its input quantized, $q = \mathrm{clip}(\mathrm{round}(x/s + z), -128, 127)$, and its output dequantized, $\hat{x} = (q - z)\cdot s$, always reading $s, z$ from the model itself. **Parity** is a measurement, not an assumption: the browser uses XNNPACK's kernels, while the board uses CMSIS-NN, and the two aren't bit-exact with each other. We judge it with $d = \max_k |s^{pc}_k - s^{web}_k| \le \mathrm{TOL}$ (for example, 0.02), with the winning class also required to match. If it fails, nine times out of ten the problem is in the front-end, especially normalization.

## Worked example

This lesson's slides also reference files in another lesson and under `shared/`:

- [shared/training](../../shared/training)
- [shared/training/convert_web.py](../../shared/training/convert_web.py) — Prepare the trained model for the browser (BENTO Edge AI Emulator / any web page).
- [shared/training/eval_pc.py](../../shared/training/eval_pc.py) — Run the exported int8 .tflite on the PC and report accuracy + confusion.
- [shared/training/model_int8.tflite](../../shared/training/model_int8.tflite)
- [shared/training/train.py](../../shared/training/train.py) — Train a tiny IMU gesture classifier and export it as int8 TFLite.

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. What's LiteRT.js's main advantage over ONNX Runtime Web in this course? *(single choice · objective 1)*
   - a) Always faster on every machine
   - b) Loads the .tflite file, the same format as the MCU, directly, with no cross-format conversion
   - c) Only supports int8
   - d) Needs no front-end

   <details><summary>Solution</summary>

   **b** — this removes a conversion step that could introduce distortion. ONNX Runtime Web must convert TFLite to ONNX first, which is the path the BENTO Emulator chose to run an int8 in/out file.

   </details>

2. convert_web.py sets Optimize.DEFAULT without attaching a representative dataset. What kind of file does it produce? *(single choice · objective 2)*
   - a) Full-integer int8 (int8 in/out)
   - b) Dynamic-range: int8 weights, but float activations and I/O
   - c) Pure float16
   - d) A file that's already been through Vela

   <details><summary>Solution</summary>

   **b** — with no samples to calibrate against, the converter can only compress the weights. The file shrinks about four times, while I/O stays float, which the browser can accept.

   </details>

3. An input has scale s = 0.05 and zero-point z = −10. What does x = 1.2 quantize to? *(single choice · objective 3)*
   - a) 14
   - b) 24
   - c) 34
   - d) −10

   <details><summary>Solution</summary>

   **a** — round(1.2 / 0.05 + (−10)) = round(24 − 10) = 14, and dequantizing gets back (14 + 10) × 0.05 = 1.2.

   </details>

4. s_pc = [0.10, 0.85, 0.05] and s_web = [0.07, 0.88, 0.05], with TOL = 0.02. What's the result? *(single choice · objective 4)*
   - a) Passes, because the winning class matches
   - b) Fails, because d = 0.03 exceeds TOL, even though the winning class matches
   - c) Passes, because d = 0.00
   - d) Fails, because the winning class differs

   <details><summary>Solution</summary>

   **b** — both conditions must pass. d = max(0.03, 0.03, 0.00) = 0.03 > 0.02, so it fails. Check the front-end first.

   </details>

5. The browser predicts a different class from the PC on nearly every window. What should you check first? *(single choice · objective 4)*
   - a) The XNNPACK versus CMSIS-NN kernels
   - b) Normalization — whether both sides use the same mean/std set from .norm.npz
   - c) Internet speed
   - d) The number of epochs

   <details><summary>Solution</summary>

   **b** — different kernels cause small, consistent score differences. But if classes are wrong across the board, the front-end — especially normalize — is usually the cause.

   </details>

## Lab

- [ ] Write a comparison table of the four runtimes in your learning log, with your reasoning for which one you'd choose for your own demo web page.
- [ ] If you have Docker installed, run `train.py --save-keras`, then `convert_web.py`, and compare the sizes of `model_int8.tflite` and `model_web.tflite`.
- [ ] Compute the quantize and dequantize of x = 0.8 with s = 0.04, z = −5, and see how far the value that comes back differs from the original.

## Going further

In lesson 5.7, we'll fill in `s13_web.py` to complete all four steps: build PC-side ground truth, measure parity, and hear the Cortex-A story.

Next lesson: [lesson 5.7 — Hands-on: matching the web's verdict to the PC's, and the Cortex-A story](../l07-web-parity-lab/README.md)

## Reflect

- If you had to send a demo to a customer with no board, which runtime would you choose, and which files would you need to send?
- Why isn't "the winning class matches" alone enough evidence of parity?
