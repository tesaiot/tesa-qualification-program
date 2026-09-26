---
id: edgeai-dev.m05.l09
lang: en
title: {th: 'ลงมือทำ: เทียบสามเป้าหมาย MCU, Web และ PC', en: 'Hands-on: comparing three targets, MCU, web and PC'}
summary: {th: 'เติมห้าจุดใน s14_tflite_board.py ให้ bench โมเดล int8 บน PC เป็น ground truth ทั้ง accuracy และ latency เรียก Vela ผ่าน quantize_vela.sh แล้วพิมพ์ตารางเทียบ MCU, Web และ PC จากนั้นข้ามจาก Python ไป MicroPython อ่าน latency จริงจากบอร์ดมาเติมช่อง MCU และตัดสินใจว่าโมเดลควรอยู่ที่ไหน', en: 'Fill five points in s14_tflite_board.py to bench the int8 model on the PC as ground truth for accuracy and latency, call Vela through quantize_vela.sh and print the MCU, web and PC comparison table; then cross from Python to MicroPython, read a real latency from the board to fill the MCU row, and decide where the model should live.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [edgeai-dev.m05.l08]
objectives:
  - {th: เติมห้าจุดใน practice/s14_tflite_board.py จนพิมพ์ accuracy ของ int8 และ latency ต่อ window ที่ไม่เป็นศูนย์บน PC รัน Vela เมื่อมี และพิมพ์ตารางสามเป้าหมาย, en: 'Fill the five points in practice/s14_tflite_board.py until it prints the int8 accuracy and a non-zero per-window latency on the PC, runs Vela when available and prints the three-target table.'}
  - {th: อ่าน latency_ms จากบอร์ดด้วย edge_ai แล้วเติมช่อง MCU ด้วย --mcu-ms โดยระบุชัดว่าเป็นโมเดลของเราหรือโมเดล Motion ที่ใช้เป็นจุดอ้างอิง, en: 'Read latency_ms from the board with edge_ai and fill the MCU row with --mcu-ms, stating clearly whether it is your model or the built-in Motion model used as a reference.'}
  - {th: อธิบายจากตารางที่เติมแล้วว่าทำไม accuracy ควรตรงกันแต่ latency ต่างกัน และเลือกเป้าหมายให้โจทย์ที่กำหนดพร้อมเหตุผล, en: 'Use the completed table to explain why accuracy should agree while latency differs, and choose a target for a given scenario with reasons.'}
develops: [{skill: ai.model-deploy, to: 3}, {skill: lang.python, to: 2}, {skill: lang.micropython, to: 2}]
assesses: [{skill: ai.model-deploy, level: 2, evidence: practice/s14_tflite_board.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: fb0272a622a864d98c6533944c22ddc98bebe2ca1491f7884109d7d63cf5bfbd
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 5.9 — Hands-on: comparing three targets, MCU, web and PC

> Module 5 — Training and deploying to several targets · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Fill five points in s14_tflite_board.py to bench the int8 model on the PC as ground truth for both accuracy and latency, call Vela through quantize_vela.sh, and print an MCU, web and PC comparison table. Then cross from Python to MicroPython, read a real latency from the board to fill in the MCU row, and decide where the model should live.

## Objectives

By the end of this lesson, you will:

1. Fill the five points in practice/s14_tflite_board.py until it prints int8's accuracy and a non-zero per-window latency on the PC, runs Vela when available, and prints the three-target table.
2. Read latency_ms from the board with edge_ai, and fill the MCU row using --mcu-ms, stating clearly whether it's your own model or the built-in Motion model used as a reference.
3. Use the completed table to explain why accuracy should agree while latency differs, and choose a target for a given scenario, with reasons.

## Before you start

You've been through lesson 5.8, and understand what Vela does and which file goes to which target. Copy `practice/s14_tflite_board.py` into [`shared/training`](../../shared/training/), which has `dataset_tools.py`, `model_int8.tflite`, `.norm.npz` and `quantize_vela.sh`.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware (this lesson needs a real board) — the bench and Vela can run on the PC, but the MCU's latency number must come from the real board, since the emulator has no NPU.
- **Prior lesson:** [lesson 5.8 — Quantize and Vela: putting our model on the Ethos-U55](../l08-quantize-and-vela/README.md)

## Concepts

The whole file reads as one sentence: bench int8 on the PC as ground truth → run Vela to get the MCU file → lay out numbers comparing three targets → point the way to reading real latency on the board. Four of the five points sit in `bench_int8()`: (1) normalize with mean/std (2) quantize with the input's scale/zero (3) time only the `it.invoke()` span with `time.perf_counter()`, accumulating it in ms (4) `correct += int(o.argmax() == y[i])`. And one more point sits in `run_vela()`: (5) `subprocess.run(["./quantize_vela.sh", int8_path], check=True)`, wrapped in try/except — a machine without vela gets a message and moves on, instead of killing the whole script.

We measure "pure inference time", excluding normalize or quantize, so it can be compared meaningfully against the board's numbers. On the PC, use `time.perf_counter()` around `invoke()`; in a browser, use `performance.now()` around `model.run()`; the MCU must come from the board only — select a model with `edge_ai.select(n)`, then read `edge_ai.result()["latency_ms"]` or `edge_ai.latency()` (the latest value, in ms). Collect several readings to see both the average and the maximum, then send it back with `python s14_tflite_board.py --mcu-ms <value>`. The table will fill in the MCU row for you. The MCU's accuracy cell uses `pc_acc` as a placeholder first, then gets confirmed with a real verdict on the board.

Getting your own model onto the NPU is a researcher's path requiring a firmware build: wrap the Vela file with the `AIM_*` contract, register the model, build, then hard power-cycle before trusting the result. In the public SDK, use `ai_engine_register()` instead of editing `ai_engine.c`. If you haven't reached that step yet, you can use the latency of the board's built-in Motion model as a reference point, but you must clearly note it's a different model. Success is being able to say why accuracy across three targets should agree while latency lands at completely different levels, and which kind of work belongs where.

## Worked example

`s14_tflite_board_full.py` adds benching the web path (the float-I/O file built by `convert_web.py`), a qualitative (not actually measured) power column, a `--no-vela` option, and `--show-mpy`, which prints MicroPython code for reading latency on the board. Open it for comparison once your practice file is done.

| File | What this file teaches |
|---|---|
| [examples/s14_tflite_board_full.py](examples/s14_tflite_board_full.py) | A full target-comparison lab: PC vs web vs MCU, from one single model file (full version) |

This lesson's slides also reference files under `shared/`:

- [shared/training](../../shared/training)
- [shared/training/quantize_vela.sh](../../shared/training/quantize_vela.sh) — Compile an int8 .tflite for the Ethos-U55 NPU on the PSoC Edge board.

## Practice

The `# TODO` comments are at lines 47 (normalize), 52 (quantize), 58 (timing invoke), 68 (counting correct classes), and 83 (calling `quantize_vela.sh`). If latency stays at 0.00 ms forever, point 58 is still empty. If accuracy looks odd, check points 47 and 52 first, since the front-end is where things break most often.

| Practice file | Topic |
|---|---|
| [practice/s14_tflite_board.py](practice/s14_tflite_board.py) | quantize -> Vela -> run on the NPU, then compare three targets (the fill-in-the-code version) |

## Solution

Open the solution after trying on your own at least once, and read [how to use the solutions](../../README.en.md#how-to-use-the-solutions) first.

| Solution | Pairs with |
|---|---|
| [solution/s14_tflite_board.py](solution/s14_tflite_board.py) | [practice/s14_tflite_board.py](practice/s14_tflite_board.py) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. The table shows the PC's latency as 0.00 ms every time. Which point is still empty? *(single choice · objective 1)*
   - a) Point 1, normalize
   - b) Point 3, timing and calling invoke()
   - c) Point 4, counting correct classes
   - d) Point 5, calling Vela

   <details><summary>Solution</summary>

   **b** — the placeholder is pass, so there's neither an invoke call nor accumulation into total_ms. The result is 0 latency and a meaningless accuracy.

   </details>

2. The script prints "vela not found on this machine." What should you do? *(single choice · objective 1)*
   - a) Delete point 5
   - b) Run the script inside the lesson 5.3–5.5 Docker image, which has ethos-u-vela installed
   - c) Retrain the model
   - d) Switch to using model_web.tflite instead

   <details><summary>Solution</summary>

   **b** — try/except keeps the script from dying, but there will be no `_vela` file until it's run somewhere that has vela.

   </details>

3. Why can't the MCU's latency number be measured from the PC or the BENTO Emulator? *(single choice · objective 2)*
   - a) Because the PC and the emulator have no Ethos-U55; whatever time is measured belongs to the CPU or the browser, not the NPU
   - b) Because time.perf_counter() doesn't work
   - c) Because the MCU's latency always equals the PC's
   - d) Because Vela must run on the board

   <details><summary>Solution</summary>

   **a** — it must be read from edge_ai on a real board only. The number on the emulator is the browser runtime's time.

   </details>

4. An animal tracking tag on a battery that must last several months, classifying motion continuously. Where should the model run? *(single choice · objective 3)*
   - a) Cortex-A
   - b) MCU + NPU, with the `_vela.tflite` file
   - c) A browser
   - d) PC in Docker

   <details><summary>Solution</summary>

   **b** — this job needs the lowest possible energy per inference, and has no OS to run on. The extra cost of the Vela step at build time is worth the longer battery life every time it runs.

   </details>

## Lab

**The MVP for lessons 5.8–5.9:** a comparison table of three targets (MCU, web, PC) with real numbers, explaining why accuracy matches but latency differs, and why the MCU needs Vela.

- [ ] All five points in the practice file are filled in. Running it in the same Docker image gives int8's accuracy and latency on the PC, and the `_vela.tflite` file.
- [ ] On the board, select a model and read `edge_ai.latency()` at least 20 times, noting the average and maximum, and state which model it was.
- [ ] Run `python s14_tflite_board.py --mcu-ms <average>` and save the table into your learning log.
- [ ] Choose a target for three scenarios (a battery-powered tag, a customer demo, a gateway on the factory floor), with reasons from the table.

## Going further

In the next module (Edge AI apps), we'll take a model and build a real app around it — one verdict, one job — starting with an app focused on a single model.

Next lesson: [lesson 6.1 — Six models and the edge_ai API: an app focused on a single model](../../m06-apps/l01-focused-apps/README.md)

## Reflect

- How many times faster is your PC's latency than the NPU's, and how fair is that number when the PC isn't power-constrained?
- If you had to choose between 2% higher accuracy and half the latency, which would your work need?
