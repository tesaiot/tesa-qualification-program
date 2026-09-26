---
id: edgeai-dev.m07.l04
lang: en
title: {th: 'ลงมือทำ: ให้โมเดลใหม่โผล่ใน edge_ai.models()', en: 'Hands-on: make a new model appear in edge_ai.models()'}
summary: {th: เติมห้าจุดใน s19_extend_model.py ที่ข้ามสองฝั่ง ครึ่งบนสร้าง C ROW จากสเปกในภาษา Python ครึ่งล่างถามทะเบียนด้วย count() และ models() แล้วเลือกรันโมเดลของเรา จากนั้นเพิ่มโมเดลเข้าเฟิร์มแวร์จริง ยืนยันด้วยจำนวนโมเดลก่อนและหลัง และเดิน checklist ก่อนเชื่อผลบนฮาร์ดแวร์, en: 'Fill five points in s19_extend_model.py, which spans two worlds - the top half builds a C ROW from a Python spec, the bottom half queries the registry with count() and models() and runs your model. Then add the model to real firmware, prove it with the model count before and after, and walk the checklist before trusting the hardware.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m07.l03]
objectives:
  - {th: เติมห้าจุดใน practice/s19_extend_model.py จนพิมพ์ ROW ที่มีสี่ชื่อฟังก์ชันและคลาสครบ และหา index ของโมเดลในทะเบียนจากชื่อได้ (บน Emulator จะยังไม่เจอ Fall ซึ่งถูกต้อง), en: 'Fill the five points in practice/s19_extend_model.py until it prints a ROW with all four function names and the classes, and finds the model''s registry index by name (on the emulator Fall is not found yet, which is correct).'}
  - {th: เพิ่มโมเดลเข้าเฟิร์มแวร์ (สามการแก้ในซอร์สตัวเต็ม หรือ ai_engine_register() ใน SDK สาธารณะ) แล้วแสดง edge_ai.count() ก่อนและหลัง ชื่อใหม่ใน models() และ verdict จริงเมื่อ select, en: 'Add a model to the firmware (three edits in the full source, or ai_engine_register() in the public SDK), then show edge_ai.count() before and after, the new name in models(), and a real verdict when selected.'}
  - {th: 'เดิน checklist ก่อนเชื่อผล (ตรวจสัญลักษณ์ด้วย nm, section .ml_weights, clean build, hard power-cycle) และอธิบายเหตุผลของแต่ละข้อ', en: 'Walk the pre-trust checklist (symbols checked with nm, the .ml_weights section, a clean build, a hard power cycle) and explain the reason for each item.'}
develops: [{skill: build.vendor-sdk, to: 2}, {skill: ai.model-deploy, to: 3}, {skill: lang.micropython, to: 2}]
assesses: [{skill: build.vendor-sdk, level: 2, evidence: practice/s19_extend_model.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: 08e244ee37b3b2c985e8544b7b523d72d9afa65fbe5428fcc67ec5ddcffe8707
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 7.4 — Hands-on: make a new model appear in edge_ai.models()

> Module 7 — Under the hood and extending the firmware · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Fill five points in s19_extend_model.py, which spans two worlds: the top half builds a C ROW from a spec in Python, the bottom half queries the registry with count() and models() and then selects and runs our model. Then add the model to real firmware, prove it with the model count before and after, and walk a checklist before trusting the result on hardware.

## Objectives

By the end of this lesson, you will:

1. Fill the five points in practice/s19_extend_model.py until it prints a ROW with all four function names and the classes complete, and find the model's registry index by name (on the emulator, Fall isn't found yet, which is correct).
2. Add a model to the firmware (three edits in the full source, or ai_engine_register() in the public SDK), then show edge_ai.count() before and after, the new name in models(), and a real verdict on select.
3. Walk the pre-trust checklist (symbols checked with nm, the .ml_weights section, a clean build, a hard power cycle), and explain the reason for each item.

## Before you start

You've been through lesson 7.3, and know the three edits, the four-function contract, and the equivalent routes in the SDK. If you'll be doing the firmware part, install ModusToolbox and clone the [public SDK](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk), with a model already wrapped to the four-function contract.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — the top half of the file (the spec and the ROW) can be practised on the emulator. Actually adding a model requires building the firmware with ModusToolbox, then flashing the board. The full source isn't yet public, so use the public SDK with ai_engine_register() instead of editing ai_engine.c.
- **Prior lesson:** [lesson 7.3 — Adding your own model: three edits, a four-function contract, and Vela](../l03-add-your-own-model/README.md)

## Concepts

This file crosses worlds: write a spec → print the C ROW you need to place → ask the registry whether it's shown up → select and run it, then read the verdict. The five points to fill in are: (1) `"sensor": edge_ai.SENSOR_IMU` and `"labels": ["normal", "fall"]` in `SPEC` (2) `deq_fn = "AIM_%s_dequeue" % prefix` in `make_row()`, which assembles the text `#if defined(EDGE_AI_MODEL_fall)` / `#define FALL_ROW {...}` / `#endif` for you to copy and place — forget this point, and the ROW has `.dequeue = None`, which won't compile (3) `n = edge_ai.count()` (4) `mine = i` when the name matches, finding the index by name rather than hard-coding a number, and (5) `edge_ai.select(idx)`, followed by `r = edge_ai.result()`, wrapped in `try/except OSError`, since a new model may fail to init.

On the emulator, you can practise the top half — the registry has five models and doesn't yet have Fall, which is correct, since the browser can't build C. The bottom half can be tried with an existing model, such as Motion. On the board, in the full source, make the three edits, then `rm -rf proj_cm55/build; make program EDGE_AI_MODEL=combo`. If using the public SDK, call `ai_engine_register(&desc)` from your own code at boot, then build with ModusToolbox. After that, press Re-check: `count()` must increase (on the board, six becomes seven), the new name turns green, then Run mine — move the board until the class switches between `normal` and `fall`. Before trusting the result, walk the checklist: test the `.tflite` in Python before wrapping it; check with `nm` that symbols don't collide; large weights sit in `.ml_weights`; the front end matches training; a clean build; and a **hard power cycle** — one change per flash.

## Worked example

`s19_extend_model_full.py` supports both `STYLE = "AIM"` (a model from DEEPCRAFT Studio) and `"IMAI"` (a Ready-Model `.a`), checks that the four-function contract is complete, compares `count()` before and after, and colours the verdict by `CONF_FLOOR`, with latency.

| File | What this file teaches |
|---|---|
| [examples/s19_extend_model_full.py](examples/s19_extend_model_full.py) | Adding your own model into Edge AI (full version) |

## Practice

The `# TODO` comments are at lines 44 (`SPEC` sensor and labels), 60 (`deq_fn`), 129 (`count`), 138 (`mine = i`), and 156 (`select` and `result`). If the printed ROW has a `None` in it, point 60 is still empty. If the model-count diff is always zero, check point 129.

| Practice file | Topic |
|---|---|
| [practice/s19_extend_model.py](practice/s19_extend_model.py) | Adding your own model into Edge AI (the fill-in-the-code version) |

## Solution

Open the solution after trying on your own at least once, and read [how to use the solutions](../../README.en.md#how-to-use-the-solutions) first.

| Solution | Pairs with |
|---|---|
| [solution/s19_extend_model.py](solution/s19_extend_model.py) | [practice/s19_extend_model.py](practice/s19_extend_model.py) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. The printed ROW has .dequeue = None. Which point is still empty? *(single choice · objective 1)*
   - a) Point 1, SPEC
   - b) Point 2, deq_fn in make_row()
   - c) Point 3, count()
   - d) Point 5, select

   <details><summary>Solution</summary>

   **b** — make_row assembles all four function names from the prefix. If deq_fn is still None, the ROW text won't compile.

   </details>

2. Running on the emulator, scan_registry() doesn't find Fall Detection. What does that mean? *(single choice · objective 1)*
   - a) The code is wrong
   - b) That's correct — the emulator has five models already compiled in, and the browser can't build C
   - c) The browser needs a refresh
   - d) The name needs adding to edge_ai.py

   <details><summary>Solution</summary>

   **b** — adding a model requires a toolchain and flashing the board. This is exactly the boundary between firmware work and app-level work.

   </details>

3. Which piece of evidence confirms a model was genuinely added successfully? *(single choice · objective 2)*
   - a) The build passes with no errors
   - b) count() has increased, the new name is in models(), and after select, the verdict genuinely switches with real motion
   - c) The model file is in the right folder
   - d) The ROW prints out completely

   <details><summary>Solution</summary>

   **b** — a passing build, or a file in the right place, doesn't yet prove all four functions are correctly wired. You need to see both the registry and the verdict on the board.

   </details>

4. Why does the checklist call for a hard power cycle before trusting the result on hardware? *(single choice · objective 3)*
   - a) To clear files from flash
   - b) After flashing, some sensors and the NPU need to be reinitialised from real power, otherwise a reading might still be stuck from before
   - c) So WiFi reconnects
   - d) It isn't necessary

   <details><summary>Solution</summary>

   **b** — one change per flash, then a power cycle before trusting it, makes sure the result you see genuinely comes from this change.

   </details>

## Lab

**The MVP for lessons 7.3–7.4:** a newly added model raises `edge_ai.count()`, its name shows up in `edge_ai.models()`, and selecting and running it gets a real verdict on the board.

- [ ] All five points in the practice file are filled in. Run it on the emulator and check the printed ROW field by field.
- [ ] On the board, note `edge_ai.count()` before adding the model.
- [ ] Add the model (three edits in the full source, or `ai_engine_register()` in the SDK), build it, hard power-cycle, note `count()` after adding it, and the verdict when running Run mine.
- [ ] Write out the checklist you actually walked in your learning log, with evidence for each item (for example, `nm`'s output).

## Going further

In the next module (Capstone), we'll combine everything from DAQ through to apps into our own Edge AI app, in a single file.

Next lesson: [lesson 8.1 — Designing the capstone: Guardian's three pillars in one file](../../m08-capstone/l01-capstone-design/README.md)

## Reflect

- If count() increased but the verdict never changed at all, which layer would you investigate first?
- In a real product, would you add a model at build time or load it at run time, and why?
