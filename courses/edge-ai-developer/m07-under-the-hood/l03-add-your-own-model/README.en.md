---
id: edgeai-dev.m07.l03
lang: en
title: {th: 'เพิ่มโมเดลของเราเอง: สามการแก้ สัญญาสี่ฟังก์ชัน และ Vela', en: 'Adding your own model: three edits, a four-function contract and Vela'}
summary: {th: 'เรียนวิธีเพิ่มโมเดลของเราเองให้บอร์ดรู้จัก ทะเบียนแบบ shape-driven ทำให้ใช้แค่สามการแก้ในซอร์สเฟิร์มแวร์ตัวเต็ม คือ Makefile, ROW กับ s_models[] และไฟล์โมเดล รู้จักสัญญาสี่ฟังก์ชัน AIM_ กับ IMAI_ feed ของเซนเซอร์เดิม งบหน่วยความจำ flash กับ arena และทางเทียบเท่าใน SDK สาธารณะ', en: 'Learn how to make the board know a model of your own. A shape-driven registry means only three edits in the full firmware source (the Makefile, a ROW in s_models[], and the model file). Meet the four-function contract, AIM_ versus IMAI_, reusing an existing sensor''s feed, the flash-versus-arena memory budget, and the equivalent routes in the public SDK.'}
level: L3
time_min: {concept: 55, practise: 5, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m07.l02]
objectives:
  - {th: 'อธิบายได้ว่าทำไมทะเบียนแบบ shape-driven จึงใช้แค่สามการแก้โดยไม่แตะ MicroPython หรือ IPC และบอกทางเทียบเท่าใน SDK สาธารณะ (ai_engine_register(), การใส่โมเดลแทนช่องเดิม หรือโมเดล IMU แบบ staged)', en: 'Explain why a shape-driven registry needs only three edits and no change to MicroPython or IPC, and name the equivalents in the public SDK (ai_engine_register(), filling an existing slot, or a staged IMU model).'}
  - {th: 'เขียน descriptor ของโมเดล (name, sensor, class_labels ที่ index 0 เป็นคลาสปฏิเสธ, period_ms, ตัวชี้สี่ฟังก์ชัน) และบอกสัญญาสี่ฟังก์ชันพร้อมรหัสคืนค่าได้', en: 'Write a model descriptor (name, sensor, class_labels with index 0 as the negative class, period_ms, four function pointers) and state the four-function contract with its return codes.'}
  - {th: แยกหน่วยความจำของโมเดลเป็น flash (weights + code) กับ RAM (tensor arena + บัฟเฟอร์) และอธิบายว่า arena ไม่พอทำให้ select() ล้มอย่างไร, en: 'Split a model''s memory into flash (weights plus code) and RAM (tensor arena plus buffers), and explain how an arena that is too small makes select() fail.'}
  - {th: อธิบายว่าทำไมโมเดลที่ใช้เซนเซอร์เดิมจึงยืม feed ที่มีอยู่ได้ และทำไม feature parity จึงเป็นความล้มเหลวเงียบอันดับหนึ่ง, en: 'Explain why a model on an existing sensor can borrow the existing feed, and why feature parity is the number-one silent failure.'}
develops: [{skill: build.vendor-sdk, to: 2}, {skill: lang.c, to: 2}, {skill: ai.model-deploy, to: 3}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: 741bcec525cd72dc70868e8246f7eb4a6ee581537e36085162b1a2b98650ec6d
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 7.3 — Adding your own model: three edits, a four-function contract, and Vela

> Module 7 — Under the hood and extending the firmware · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Learn how to make the board know a model of your own. A shape-driven registry means only three edits are needed in the full firmware source — the Makefile, a ROW in s_models[], and the model file. Meet the four-function contract, AIM_ versus IMAI_, reusing an existing sensor's feed, the flash-versus-arena memory budget, and the equivalent routes in the public SDK.

## Objectives

By the end of this lesson, you will:

1. Explain why a shape-driven registry needs only three edits, with no change to MicroPython or the IPC, and name the equivalents in the public SDK (ai_engine_register(), filling an existing slot, or a staged IMU model).
2. Write a model descriptor (name, sensor, class_labels with index 0 as the negative class, period_ms, four function pointers), and state the four-function contract with its return codes.
3. Split a model's memory into flash (weights + code) and RAM (tensor arena + buffers), and explain how an arena that's too small makes select() fail.
4. Explain why a model on an existing sensor can borrow the existing feed, and why feature parity is the number-one silent failure.

## Before you start

You've been through lessons 7.1–7.2, and understand the `s_models[]` registry, `ai_model_desc_t`, and the IPC model link. Keep the SDK's [Filling a model slot guide](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/main/bento-firmware-template-mtb-mpy/proj_cm55/modules/ai_models/README.md) open alongside your screen.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — this is a concept lesson. Actually adding a model requires building the firmware with ModusToolbox; the full source containing ai_engine.c isn't yet public. The public SDK provides a prebuilt engine and headers to use instead.
- **Prior lesson:** [lesson 7.2 — Hands-on: tracing the stack from MicroPython](../l02-trace-the-stack-lab/README.md)

## See it work first

Throughout the course, `edge_ai.models()` has answered with six models on the board. Today, ask the reverse question: how would a seventh model come to show up in that table? The full firmware source already has a `FALL_ROW` written as an example, waiting — it just needs to be switched on.

## Concepts

Neither MicroPython (`edge_ai`) nor the IPC model link knows any model's name at all. `count()` counts the size of `s_models[]`, `model(n)` copies the fields of row n, and `select(n)` has the task call that row's function pointers. The registry is therefore **shape-driven** — data drives behaviour. In the full source, adding a model takes **three edits**: (1) add the name to `AI_MODELS` in the Makefile, which derives `-DEDGE_AI_MODEL_<name>` for you (watch out for extra spaces) (2) write a ROW wrapped in `#if defined(...)`, then append it to `s_models[]` (the array's order is the menu's order), and (3) place the model file in `proj_cm55/modules/ai_models/`. In the public SDK, `ai_engine` comes as a prebuilt library, so a new row is added via `ai_engine_register(&desc)` from your own code at run time, or by filling an existing slot — and the current firmware version can also load a staged IMU model per `ai_model_staged.h`.

Every model must supply **four functions**: `<PREFIX>_init(void)`, `<PREFIX>_enqueue(const float *in)`, `<PREFIX>_dequeue(float *out)`, and `<PREFIX>_finalize(void)`, returning `0` on success, `-1` (NODATA) while the window isn't yet full, and `-2` on error. A model built from DEEPCRAFT Studio uses the prefix `AIM_<NAME>_`, while a Ready-Model `.a` exports `IMAI_*`, with the same names on every one — so it needs `objcopy` to rename it to `IMAI_<NAME>_*` before it can coexist with others. The descriptor's `class_labels` must have the negative class (idle, unlabelled, normal) at index 0, since the screen uses the highest score among class 1 and up as the confidence.

Memory splits into $M_{flash} = W_{weights} + C_{code}$ and $M_{RAM} = A_{arena} + B_{io}$, where the arena must be large enough for the largest number of tensors alive at once. If the arena isn't big enough, `init()` returns a negative value, and `select()` raises `OSError`. Large weights in a `combo` image can hit the flash ceiling and need moving to the `.ml_weights` section. A model on an existing sensor can borrow the existing feed right away (Fall uses the IMU, so it borrows `feed_imu`); a new sensor needs its own feed written to convert raw values into the same units used during training. A self-trained model can be wrapped two ways: DEEPCRAFT's converter, which generates C with a front end, or wrapping TFLite-Micro yourself with `AddEthosU()` and writing a matching front end. The real trap is feature parity: a `.tflite` graph has no FFT or mel filterbank inside it — if the front end is even slightly off, scores drift silently wrong.

## Worked example

This lesson's slides also reference a file in another lesson or in `shared/`:

- [shared/training/quantize_vela.sh](../../shared/training/quantize_vela.sh) — Compile an int8 .tflite for the Ethos-U55 NPU on the PSoC Edge board.

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. Why doesn't adding a model in the full source require editing MicroPython's edge_ai module? *(single choice · objective 1)*
   - a) Because MicroPython already stores every model's name
   - b) Because the registry is shape-driven — MicroPython asks count() and model(n) from s_models[] every time
   - c) Because IPC sends the model file itself
   - d) Because you'd edit the emulator instead

   <details><summary>Solution</summary>

   **b** — no model's name is ever hard-coded on the Python side. Add a row at the far end, and the whole chain sees it on its own.

   </details>

2. If you're using the public SDK, where ai_engine comes as a prebuilt library, how would you add a model that has no existing slot? *(single choice · objective 1)*
   - a) Edit ai_engine.c inside the archive
   - b) Call ai_engine_register(&desc) from your own code at run time
   - c) Add the name to edge_ai.py
   - d) It can't be done at all

   <details><summary>Solution</summary>

   **b** — Route 0 in the SDK guide lets the engine add a row from your descriptor, with no need to rebuild the archive.

   </details>

3. AIM_FALL_dequeue returns −1 after only a few enqueue calls. What does that mean? *(single choice · objective 2)*
   - a) The model is broken
   - b) NODATA — the window isn't full yet, keep enqueuing
   - c) The winning class is −1
   - d) The arena isn't big enough

   <details><summary>Solution</summary>

   **b** — a streaming model needs a full window of L calls before dequeue can return 0 with scores.

   </details>

4. You add a model, and it shows up in models(), but select() raises OSError every time. What's the most likely cause? *(single choice · objective 3)*
   - a) The model name is too long
   - b) init() returns a negative value, for example because the tensor arena is smaller than the graph needs
   - c) You forgot to add labels
   - d) WiFi isn't connected

   <details><summary>Solution</summary>

   **b** — select confirms by observation. If the model's init fails, the engine never switches, so Q_ACTIVE never equals the requested value.

   </details>

5. Why did the author choose Fall Detection as the first model to add? *(single choice · objective 4)*
   - a) Because it's the most accurate
   - b) Because it uses the IMU, so it can borrow the existing feed_imu, and its front end is the lightest, with no FFT to get wrong
   - c) Because it doesn't need to go through Vela
   - d) Because it's float32

   <details><summary>Solution</summary>

   **b** — choose the path that's already proven first. An audio model needs its FFT and mel filterbank to match training exactly, which is the most common silent failure point.

   </details>

## Lab

- [ ] Write out Fall Detection's ROW by hand in your learning log, pointing out which field ends up in `edge_ai.models()`.
- [ ] Open the SDK's Filling a model slot guide, and summarise the difference between Route 0 (`ai_engine_register`) and Route 1 (filling an existing slot) in two lines.
- [ ] Estimate the memory budget of a model with 40,000 bytes of weights and a 20 KB arena — which parts consume flash, and which consume RAM.

## Going further

In lesson 7.4, we'll use `s19_extend_model.py` to build a ROW from a spec, check the registry with `count()` and `models()`, then run the model we added.

Next lesson: [lesson 7.4 — Hands-on: making a new model show up in edge_ai.models()](../l04-extend-model-lab/README.md)

## Reflect

- If you had to add a self-trained audio model, which front-end steps would need to match training exactly?
- What are the trade-offs between adding a model at build time versus at run time, for a product that updates over OTA?
