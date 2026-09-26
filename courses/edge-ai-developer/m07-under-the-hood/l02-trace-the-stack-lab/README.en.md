---
id: edgeai-dev.m07.l02
lang: en
title: {th: 'ลงมือทำ: ส่องสแตกจาก MicroPython', en: 'Hands-on: tracing the stack from MicroPython'}
summary: {th: 'เติมคำสั่งฝั่งอ่านห้าตัวของ edge_ai ใน s18_under_the_hood.py คือ links, model, active, result และ latency แล้วกด Trace ให้ log ไล่สแตกสามชั้น transport, control และ result พร้อมจับคู่แต่ละบรรทัดกับฟังก์ชันหรือฟิลด์ใน header ของ SDK และเทียบ latency ของโมเดล int8 บน NPU กับโมเดล float32 บน CPU', en: 'Fill the five read-side calls of edge_ai in s18_under_the_hood.py (links, model, active, result and latency), press Trace to log the three stack layers (transport, control, result), match each line to a function or field in the SDK headers, and compare the latency of an int8 model on the NPU with a float32 model on the CPU.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m07.l01]
objectives:
  - {th: 'เติมห้าจุดใน practice/s18_under_the_hood.py จนกด Trace แล้วได้ log ครบสี่ส่วน transport, registry, control และ result โดยค่า active() ตรงกับโมเดลที่เลือก', en: 'Fill the five points in practice/s18_under_the_hood.py until Trace logs all four parts (transport, registry, control, result) with active() matching the selected model.'}
  - {th: จับคู่ log อย่างน้อยสามบรรทัดกับฟังก์ชันหรือฟิลด์ใน ai_engine.h หรือ ipc_model_link_defs.h ของ SDK, en: Match at least three log lines to a function or field in the SDK's ai_engine.h or ipc_model_link_defs.h.}
  - {th: บนบอร์ด เทียบ latency() ของโมเดล int8 กับโมเดล float32 และอธิบายความต่างด้วยเส้นทาง NPU กับ CPU, en: 'On the board, compare latency() of an int8 model with a float32 model and explain the difference by the NPU and CPU paths.'}
develops: [{skill: rtos.multicore-ipc, to: 2}, {skill: hw.architecture, to: 3}, {skill: lang.micropython, to: 2}]
assesses: [{skill: rtos.multicore-ipc, level: 2, evidence: practice/s18_under_the_hood.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: 45f5a0a719208ab9ab589c47972df33b66676b887adc71287a225f9177aa7287
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 7.2 — Hands-on: tracing the stack from MicroPython

> Module 7 — Under the hood and extending the firmware · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Fill in five read-side calls of edge_ai in s18_under_the_hood.py — links, model, active, result, and latency — then press Trace to log the three stack layers (transport, control, and result), match each line to a function or field in the SDK's headers, and compare the latency of an int8 model on the NPU with a float32 model on the CPU.

## Objectives

By the end of this lesson, you will:

1. Fill the five points in practice/s18_under_the_hood.py until Trace logs all four parts (transport, registry, control, result), with active() matching the selected model.
2. Match at least three log lines to a function or field in the SDK's ai_engine.h or ipc_model_link_defs.h.
3. On the board, compare latency() of an int8 model with a float32 model, and explain the difference via the NPU and CPU paths.

## Before you start

You've been through lesson 7.1, and know the three cores, the model registry, the IPC's two planes, and ai_result_t. Keep the SDK's `ai_engine.h` and `ipc_model_link_defs.h` open alongside your screen, as in the prior lesson.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — on the emulator, you can practise calling the read-side API (getting `('ipc',)` and a five-model registry), but latency and model results are simulated values. Comparing int8 with float32 needs the board.
- **Prior lesson:** [lesson 7.1 — The Edge AI stack: tri-core, ai_engine, the IPC model link, and TFLite-Micro](../l01-edge-ai-stack/README.md)

## Concepts

This file doesn't run any new inference. It's a **stack-tracing tool** that calls the read-side API and logs it, one layer at a time. The five points to fill in are: (1) `links = edge_ai.links()`, returning `('ipc',)`, showing it talks to the CM55 over the IPC model link (2) `desc = edge_ai.model(mi)`, fetching a single descriptor (name, sensor, labels) via `Q_MODEL` (3) `cur = edge_ai.active()`, after the already-provided `select(sel)` — normally `cur` should equal `sel`, since this is confirmation by observation, seen with your own eyes (4) `r = edge_ai.result()` via `Q_RESULT`, and (5) `ms = edge_ai.latency()`, the latest inference time from `inference_us`. All five are pull-style reads.

When Trace runs, the log proceeds transport → registry → control → result. Match each line to the SDK's headers — for example, `active()` to `ai_engine_active()` and `MODEL_LINK_Q_ACTIVE`; `select(n)` to `MODEL_LINK_CMD_SELECT_BASE + n`; and the keys of `result()` to the fields of `ai_result_t`. The C source on the firmware side that the log mentions (`ai_engine.c`, `deepcraft_task.c`) isn't yet public — the headers are the public, checkable evidence. On the board, try tracing an int8 model (for example, Motion), then switch to a float32 model (the author notes Push and Siren), and compare `latency()` — you'll see the NPU and CPU paths genuinely differ. Don't switch models rapidly; leave a second between switches so the control plane doesn't jam.

## Worked example

`s18_under_the_hood_full.py` adds an on-screen stack map, a table matching the keys of `result()` to the fields in `ai_result_t`, an `on_result` callback (called on a class change, and repeating roughly once a second), and a latency comparison between int8 and float32.

| File | What this file teaches |
|---|---|
| [examples/s18_under_the_hood_full.py](examples/s18_under_the_hood_full.py) | A full Edge AI stack-tracing tool (for a Researcher) |

## Practice

The `# TODO` comments are at lines 38 (`links`), 75 (`model`), 109 (`active`), 134 (`result`), and 142 (`latency`). If the transport layer of the log is empty, point 38 is still empty. If active() always shows −1 even after selecting a model, check point 109.

| Practice file | Topic |
|---|---|
| [practice/s18_under_the_hood.py](practice/s18_under_the_hood.py) | Taking apart the Edge AI stack from the MicroPython end down to the NPU (the fill-in-the-code version) |

## Solution

Open the solution after trying on your own at least once, and read [how to use the solutions](../../README.en.md#how-to-use-the-solutions) first.

| Solution | Pairs with |
|---|---|
| [solution/s18_under_the_hood.py](solution/s18_under_the_hood.py) | [practice/s18_under_the_hood.py](practice/s18_under_the_hood.py) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. On the emulator and on the board, what should edge_ai.links() return? *(single choice · objective 1)*
   - a) ('ipc',)
   - b) ('wifi',)
   - c) None
   - d) The number of models

   <details><summary>Solution</summary>

   **a** — MicroPython talks to ai_engine over the IPC model link, one path only. The emulator returns the same value so the code can move to the board unchanged, even though there's no real IPC in the browser.

   </details>

2. After select(sel) succeeds, what should cur = edge_ai.active() be? *(single choice · objective 1)*
   - a) −1
   - b) sel, because select waits to see Q_ACTIVE equal the requested value
   - c) sel + 1
   - d) The number of models

   <details><summary>Solution</summary>

   **b** — select returns only once it's confirmed by observation. If it never confirms, it raises OSError instead.

   </details>

3. What does the log "select(n)" match to in ipc_model_link_defs.h? *(single choice · objective 2)*
   - a) MODEL_LINK_Q_RESULT
   - b) MODEL_LINK_CMD_SELECT_BASE (0x90) plus n, on the control plane
   - c) MODEL_LINK_STREAM_MIC_PCM
   - d) BENTO_MODEL_LINK_VERSION

   <details><summary>Solution</summary>

   **b** — SELECT packs the model number into the command byte on OP_CTRL, then confirms via Q_ACTIVE on the query plane.

   </details>

4. On the board, Motion's (int8) latency is far lower than Push's (float32). Why? *(single choice · objective 3)*
   - a) Motion has fewer classes
   - b) A Vela-compiled int8 model runs on the Ethos-U55, while float32 runs on the CPU with a float kernel
   - c) Radar is always slower than the IMU
   - d) The radar's IPC is slower

   <details><summary>Solution</summary>

   **b** — latency only measures the inference span. The main difference comes from whether the graph runs on the NPU or the CPU.

   </details>

## Lab

**The MVP for lessons 7.1–7.2:** being able to explain the stack, and point to the source function or field for at least one point in each of the three layers (transport, control, result).

- [ ] All five points in the practice file are filled in. Press Trace on the emulator or the board until the log shows completely.
- [ ] Match at least three log lines to a function or field in `ai_engine.h` or `ipc_model_link_defs.h`, and note them in your learning log.
- [ ] On the board, trace one int8 model and one float32 model, note both `latency()` values, and explain the difference.
- [ ] Explain in your own words why `active()` might not yet be the model most recently requested, if read from elsewhere during a switch.

## Going further

In the next pair of lessons (7.3–7.4), we'll use this map to add our own model so it shows up in `edge_ai.models()`.

Next lesson: [lesson 7.3 — Adding your own model: three edits, the four-function contract, and Vela](../l03-add-your-own-model/README.md)

## Reflect

- Which log line could you still not point to a source for, and what information is missing from what's public?
- If the board hung after switching models rapidly, how would you describe this symptom to the firmware team so they could find the root cause?
