---
id: edgeai-dev.m05.l07
lang: en
title: {th: 'ลงมือทำ: verdict บนเว็บให้ตรงกับ PC และเรื่องราว Cortex-A', en: 'Hands-on: a web verdict that matches the PC, and the Cortex-A story'}
summary: {th: 'เติมห้าจุดใน s13_web.py ให้ทำสี่ขั้นเดียวกับที่เบราว์เซอร์ทำ คือ normalize, quantize, invoke และ dequantize จนได้ verdict ฝั่ง PC เป็น ground truth แล้ววัด parity กับไฟล์ web ด้วย max-abs-diff ปิดด้วยเรื่องราว Cortex-A ที่รัน eval_pc.py ตัวเดิมได้เลย และการเลือกเป้าหมายอย่างมีเหตุผล', en: 'Fill five points in s13_web.py so it performs the same four steps as the browser (normalize, quantize, invoke, dequantize) and gives a PC verdict as ground truth, then measure parity against the web file with max-abs-diff. Close with the Cortex-A story, where the same eval_pc.py simply runs, and choosing a target with reasons.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [none]}
prerequisites: [edgeai-dev.m05.l06]
objectives:
  - {th: เติมห้าจุดใน practice/s13_web.py จนพิมพ์ verdict ฝั่ง PC ที่ conf เท่ากับคะแนนสูงสุดใน scores และ scores รวมกันได้ราว 1, en: Fill the five points in practice/s13_web.py until it prints a PC verdict whose conf equals the highest score and whose scores sum to about 1.}
  - {th: วัด parity อย่างน้อยหนึ่ง window (ด้วย s13_web_full.py บน PC หรือหน้าเว็บที่โหลด LiteRT.js) จดค่า max-abs-diff กับคลาสที่ชนะ แล้วตัดสินผ่านหรือไม่ผ่านตาม TOL = 0.02, en: 'Measure parity for at least one window (with s13_web_full.py on the PC or a web page running LiteRT.js), record max-abs-diff and the winning class, and judge pass or fail against TOL = 0.02.'}
  - {th: 'เลือกเป้าหมาย (MCU, Web, Cortex-A หรือ PC) ให้โจทย์ที่กำหนดพร้อมข้อแลกเปลี่ยนอย่างน้อยสองข้อ และอธิบายว่าทำไม eval_pc.py รันบน Cortex-A ได้โดยไม่แก้', en: 'Choose a target (MCU, web, Cortex-A or PC) for a given scenario with at least two trade-offs, and explain why eval_pc.py runs on Cortex-A unchanged.'}
develops: [{skill: ai.model-deploy, to: 3}, {skill: lang.python, to: 2}, {skill: ai.edge, to: 2}]
assesses: [{skill: ai.model-deploy, level: 2, evidence: practice/s13_web.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: c02edcecea26d56c537de4f1d6ffaef1bb53f84849c6546a93f9517add16ec40
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 5.7 — Hands-on: a web verdict that matches the PC, and the Cortex-A story

> Module 5 — Training and deploying to several targets · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Fill five points in s13_web.py so it performs the same four steps as the browser — normalize, quantize, invoke, dequantize — giving a PC verdict as ground truth, then measure parity against the web file with max-abs-diff. Close with the Cortex-A story, where the same eval_pc.py just runs, and choosing a target with reasons.

## Objectives

By the end of this lesson, you will:

1. Fill the five points in practice/s13_web.py until it prints a PC verdict whose conf equals the highest score in scores, and whose scores sum to about 1.
2. Measure parity for at least one window (with s13_web_full.py on the PC, or a web page running LiteRT.js), record the max-abs-diff and the winning class, and judge pass or fail against TOL = 0.02.
3. Choose a target (MCU, web, Cortex-A or PC) for a given scenario, with at least two trade-offs, and explain why eval_pc.py runs on Cortex-A unchanged.

## Before you start

You've been through lesson 5.6, and understand quantize, dequantize, and the definition of parity. Copy `practice/s13_web.py` into [`shared/training`](../../shared/training/), which has `dataset_tools.py`, `model_int8.tflite` and `.norm.npz`.

- **Hardware:** your computer, no board needed (or use the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) alongside it) — a PC (Python with ai-edge-litert, or the same Docker image). Comparing in a browser needs your own web page loading LiteRT.js, since the BENTO Emulator can't load our own file.
- **Prior lesson:** [lesson 5.6 — Running the model on the web: LiteRT.js, int8 I/O and parity](../l06-web-runtime/README.md)

## Concepts

`web_verdict()` walks the same four steps a web page must do. The five points we fill in are: (1) `x = (window - z["mean"]) / z["std"]`, normalizing with the exact same set used during training (2) `q = np.clip(np.round(x / in_scale + in_zero), -128, 127).astype(np.int8)`, reading scale/zero from `inp["quantization"]` (3) `it.set_tensor(inp["index"], q)`, then `it.invoke()` (4) `o = (o - out_zero) * out_scale`, turning softmax back into probabilities, and (5) `conf = float(o[top])`. The result returns a dict `{label, top, conf, scores}`, in exactly the same shape as what the JS side (`webVerdict`) returns. The JS side uses the web file, whose I/O is float, so it skips the quantize and dequantize steps — but the normalize step must be the exact same formula, letter for letter.

The PC-side ground truth is `python s13_web.py`. Then measure parity: `s13_web_full.py --export-web` builds `model_web.tflite` from `model.keras`, then `python s13_web_full.py` runs the int8 file against the web file over a 12-window test set, printing the max-abs-diff and the winning class — this is the first checkpoint, on the PC. The next step is your own web page loading LiteRT.js, using the code from `--show-js`. If it fails, check in order: normalize → quantize → invoke, before blaming the kernel. The fastest way to debug is feeding the exact same input to both sides and comparing the result step by step — wherever they first diverge is where the front-end doesn't match.

**Cortex-A** is the easiest: `pip install ai-edge-litert` on a Raspberry Pi or Jetson, then run `eval_pc.py` with the same `.tflite` file directly, because it has real Linux and Python — none of the NPU's int8 restrictions, and it can be accelerated further with a delegate (XNNPACK on CPU, a GPU delegate on Jetson). Choosing a target is a trade-off: the MCU is the smallest and most power-efficient but hardest to convert for; the web shares instantly but needs a front-end built in JS; Cortex-A is powerful and flexible; the PC is the training bench and the ground truth.

## Worked example

`s13_web_full.py` is a full parity lab on the PC: `--export-web` builds a web file from `model.keras` (produced by `train.py --save-keras`); running it plainly compares the int8 file against the web file over 12 windows and reports pass or fail; and `--show-js` prints LiteRT.js code to paste into a web page. Worth knowing: the training file's `--index` option isn't used yet — the script always picks the first test window.

| File | What this file teaches |
|---|---|
| [examples/s13_web_full.py](examples/s13_web_full.py) | A full parity lab: PC vs. web, from one single .tflite model (full version) |

This lesson's slides also reference files in another lesson and under `shared/`:

- [shared/training](../../shared/training)
- [shared/training/convert_web.py](../../shared/training/convert_web.py) — Prepare the trained model for the browser (BENTO Edge AI Emulator / any web page).
- [shared/training/dataset_tools.py](../../shared/training/dataset_tools.py) — Dataset tools for the IMU gesture classifier (Pillar 4 / Training).
- [shared/training/eval_pc.py](../../shared/training/eval_pc.py) — Run the exported int8 .tflite on the PC and report accuracy + confusion.
- [shared/training/model_int8.tflite](../../shared/training/model_int8.tflite)
- [shared/training/train.py](../../shared/training/train.py) — Train a tiny IMU gesture classifier and export it as int8 TFLite.

## Practice

The `# TODO` comments are at lines 38 (normalize), 50 (quantize), 55 (invoke), 60 (dequantize), and 65 (conf). If conf is 0.0000, point 65 is still empty. If scores come out as whole numbers like −128 or 127, point 60 is still empty.

| Practice file | Topic |
|---|---|
| [practice/s13_web.py](practice/s13_web.py) | Taking our model to the web, then verifying results match the PC (the fill-in-the-code version) |

## Solution

Open the solution after trying on your own at least once, and read [how to use the solutions](../../README.en.md#how-to-use-the-solutions) first.

| Solution | Pairs with |
|---|---|
| [solution/s13_web.py](solution/s13_web.py) | [practice/s13_web.py](practice/s13_web.py) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. You run it, and scores look correct, but conf = 0.0000 every time. Which point is still empty? *(single choice · objective 1)*
   - a) Point 1, normalize
   - b) Point 3, invoke
   - c) Point 4, dequantize
   - d) Point 5, conf = float(o[top])

   <details><summary>Solution</summary>

   **d** — the placeholder conf = 0.0 is still there. It needs the winning class's score pulled out with float(o[top]).

   </details>

2. scores come out as ['-128.0000', '127.0000', '-128.0000']. Which point is still empty? *(single choice · objective 1)*
   - a) Point 2, quantize
   - b) Point 4, dequantize — the value is still raw int8, not a probability
   - c) Point 1, normalize
   - d) Nothing is wrong

   <details><summary>Solution</summary>

   **b** — it must be converted back with (o − out_zero) × out_scale, so the value falls in the 0..1 range and sums to about 1.

   </details>

3. s13_web_full.py reports the winning class matching on 12/12 windows, with a max max-abs-diff of 0.0117 at TOL 0.02. What's the conclusion? *(single choice · objective 2)*
   - a) It passes on the PC — the next step is confirming in a real browser
   - b) It fails, because the diff isn't zero
   - c) It passes, and no further testing is needed anywhere
   - d) It fails, because it must reach 100%

   <details><summary>Solution</summary>

   **a** — both conditions pass, but s13_web_full.py runs the web file with an interpreter on the PC, so this is only the first checkpoint. A real browser might use a different kernel, so it's worth confirming again.

   </details>

4. You need to send a demo a customer can open immediately, with nothing to install and no board. Which target should you choose? *(single choice · objective 3)*
   - a) MCU + Ethos-U55
   - b) Web, in a browser
   - c) Cortex-A
   - d) PC in Docker

   <details><summary>Solution</summary>

   **b** — the web shares instantly with a link, and data stays on the user's machine, in exchange for having to build the front-end in JS and measure parity yourself.

   </details>

5. Why does eval_pc.py run on a Raspberry Pi without changing even a single line? *(single choice · objective 3)*
   - a) Because a Raspberry Pi has an Ethos-U55
   - b) Because Cortex-A has real Linux and Python, can install ai-edge-litert, and uses the same .tflite file with no forced int8
   - c) Because eval_pc.py is compiled into C
   - d) Because it uses Vela

   <details><summary>Solution</summary>

   **b** — Cortex-A is a small PC with a full operating system, so the same script and model file used on a PC can move over immediately.

   </details>

## Lab

**The MVP for lessons 5.6–5.7:** the web file's verdict matches the PC side within tolerance (max|score_pc − score_web| ≤ TOL, and the winning class matches), and you can explain why they don't need to match bit for bit.

- [ ] All five points in the practice file are filled in. Run `python s13_web.py` and note the label, conf and scores in your learning log.
- [ ] Run `s13_web_full.py --export-web`, then `s13_web_full.py`, and note the highest max-abs-diff and how many windows' classes matched.
- [ ] Temporarily disable normalize on one side, and see how far max-abs-diff spikes.
- [ ] If you can, confirm at least one window in a web page loading LiteRT.js, using the code from `--show-js`.

## Going further

In the next pair of lessons (5.8–5.9), we'll take the same model onto the MCU through Vela, then compare three targets on latency, accuracy and power.

Next lesson: [lesson 5.8 — Quantizing and Vela: getting our model onto the Ethos-U55](../l08-quantize-and-vela/README.md)

## Reflect

- If you had to build an audio demo instead of an IMU one, where would the JS-side front-end get harder?
- In your own work, what TOL would be acceptable, and who should be the one to decide that threshold?
