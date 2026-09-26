---
id: edgeai-dev.m07.l01
lang: en
title: {th: 'สแตก Edge AI: tri-core, ai_engine, IPC model link และ TFLite-Micro', en: 'The edge AI stack: tri-core, ai_engine, the IPC model link and TFLite-Micro'}
summary: {th: 'เปิดฝากระโปรงดูว่าทุกครั้งที่เรียก edge_ai.result() เกิดอะไรขึ้น ไล่สแตกจากสามคอร์ของ PSoC Edge E84, ai_engine และทะเบียนโมเดลบน CM55, IPC model link ที่แยก control plane กับ query plane, การ publish ผลแบบ lock-free ไปจนถึง TFLite-Micro ที่เป็น runtime จริงของทั้งโมเดล int8 และ float32', en: 'Open the hood on what happens every time you call edge_ai.result() - the three cores of the PSoC Edge E84, ai_engine and the model registry on the CM55, the IPC model link with its control and query planes, lock-free result publishing, and TFLite-Micro as the real runtime for both int8 and float32 models.'}
level: L3
time_min: {concept: 55, practise: 5, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m06.l06]
objectives:
  - {th: 'วางชิ้นส่วนของสแตก Edge AI ลงบนสามคอร์ (CM33_S, CM33_NS, CM55) ได้ถูกต้อง และอธิบายเหตุผลที่แบ่งงานแบบนั้น', en: 'Place the parts of the edge AI stack on the three cores (CM33_S, CM33_NS, CM55) correctly and explain why the work is split that way.'}
  - {th: อธิบายความต่างของโมเดลที่ขอ (s_active) กับโมเดลที่สลับแล้วจริง (s_current) และเหตุผลที่ select() ยืนยันด้วยการสังเกต Q_ACTIVE แล้วโยน OSError ได้, en: 'Explain the difference between the requested model (s_active) and the model actually switched in (s_current), and why select() confirms by observing Q_ACTIVE and can raise OSError.'}
  - {th: จับคู่ key ของ dict จาก edge_ai.result() กับฟิลด์ของ ai_result_t ได้ และอธิบายว่าทำไมการ publish จึงเป็นแบบ lock-free, en: 'Map the keys of the edge_ai.result() dict to the fields of ai_result_t, and explain why results are published lock-free.'}
  - {th: อธิบายว่า TFLite-Micro คือ runtime จริง (โมเดล int8 ที่ผ่าน Vela ไป NPU ส่วน float32 รันบน CPU) และโค้ดจาก DEEPCRAFT เป็นเปลือกที่ให้สี่ฟังก์ชัน, en: 'Explain that TFLite-Micro is the real runtime (Vela-compiled int8 models go to the NPU, float32 runs on the CPU) and that DEEPCRAFT code is a wrapper exposing four functions.'}
develops: [{skill: hw.architecture, to: 3}, {skill: rtos.multicore-ipc, to: 2}, {skill: ai.model-deploy, to: 3}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
source_sha256: 3f8be699f30b5a9dc6d2addd1a8704e9a37c3eab8a7b19be72bdcb6131aa9720
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# Lesson 7.1 — The Edge AI stack: tri-core, ai_engine, the IPC model link, and TFLite-Micro

> Module 7 — Under the hood and extending the firmware · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Open the hood on what happens every time you call edge_ai.result(). Trace the stack across the three cores of the PSoC Edge E84, ai_engine and the model registry on the CM55, the IPC model link with its control and query planes, lock-free result publishing, all the way to TFLite-Micro as the real runtime for both int8 and float32 models.

## Objectives

By the end of this lesson, you will:

1. Correctly place the parts of the Edge AI stack onto the three cores (CM33_S, CM33_NS, CM55), and explain why the work is split that way.
2. Explain the difference between the requested model (s_active) and the model actually switched in (s_current), and why select() confirms by observing Q_ACTIVE and can raise OSError.
3. Map the keys of the edge_ai.result() dict to the fields of ai_result_t, and explain why publishing is lock-free.
4. Explain that TFLite-Micro is the real runtime (Vela-compiled int8 models go to the NPU, while float32 runs on the CPU) and that DEEPCRAFT's code is a wrapper exposing four functions.

## Before you start

You've been through modules 1 through 6, and used every part of `edge_ai` — `models`, `select`, `result`, `on_result`, and `stop`. Keep the SDK's [`ai_engine.h`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/main/bento-firmware-template-mtb-mpy/lib/edge_ai/include/ai_engine.h) and [`ipc_model_link_defs.h`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/main/bento-firmware-template-mtb-mpy/bento_libs/claw/common/shared/include/ipc_model_link_defs.h) open alongside your screen.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — this is a stack-reading lesson. The emulator mimics the read-side API but has no real IPC. The firmware source the original course references (ai_engine.c, deepcraft_task.c) isn't yet public; what's open is the header in the public SDK.
- **Prior lesson:** [lesson 6.6 — Hands-on: send the fused event over MQTT](../../m06-apps/l06-fusion-iot-lab/README.md)

## See it work first

Write out the line you've used throughout the course, `r = edge_ai.result()`, and ask where `r['seq']` and `r['latency_ms']` actually come from. The answer is that it crosses two cores: Python on the CM33_NS asks over IPC to `ai_engine` on the CM55, and gets back fields from the `ai_result_t` struct.

## Concepts

The PSoC Edge E84 has three cores. **CM33_S** handles boot and security, with no Edge AI work. **CM33_NS** runs FreeRTOS and our MicroPython, reading sensors, and hosts the `edge_ai`, `sensors`, `dsp`, and `ui` modules. **CM55** is the fast core, running LVGL, the Ethos-U55 NPU, and **`ai_engine`**, which has a task that loops through inference for each model in the registry. Each registry row is an `ai_model_desc_t` (name, sensor, class_labels where index 0 is the rejection class, period_ms, and pointers to four functions). Every model stays in memory the whole time — switching just changes who receives data from a feed, not turning a model on or off, and each sensor's feed is a C-side front end that converts raw values before they enter the graph.

The CM33_NS can't call functions on the CM55 directly — the two talk through the **IPC model link**, which has two planes: **control** (`MODEL_LINK_OP_CTRL`), a fire-and-forget command, such as SELECT(n) = `0x90 + n`, and **query** (`MODEL_LINK_OP_QUERY`), read by pulling, such as `Q_COUNT`, `Q_MODEL`, `Q_RESULT`, `Q_ACTIVE`, as defined in `ipc_model_link_defs.h`. `ai_engine` keeps two indices: `s_active` (the requested one, read with `ai_engine_requested()`) and `s_current` (the one actually finished initialising, read with `ai_engine_active()`). `edge_ai.active()` returns the latter. `edge_ai.select(n)` therefore sends the command, then polls `Q_ACTIVE` until it sees n (confirming by observation) — if it doesn't see it in time, it raises `OSError`, and calling select repeatedly risks jamming the pipe.

When `dequeue()` gets an answer, `publish()` writes it to `ai_result_t` without a lock (a single writer, and the reader accepts a value that's up to one frame stale), so as not to delay the NPU's interrupts. The fields are `model_index`, `class_count`, `top_class`, `running`, `scores[]`, `inference_us`, `inference_us_max`, `inferences`, and `seq`. The `result()` dict therefore gets `top` from `top_class`, `latency_ms` from `inference_us / 1000`, and `seq` incremented every time it publishes. The real runtime is **TFLite-Micro**, which has kernels for both int8 and float32. Vela-compiled int8 models run on the Ethos-U55, while float32 models run on the CPU, within the same firmware image. The code DEEPCRAFT generates is just a wrapper exposing `init`, `enqueue`, `dequeue`, `finalize`.

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. How are our MicroPython code and the Ethos-U55 NPU split across cores? *(single choice · objective 1)*
   - a) Both are on the CM55
   - b) MicroPython is on the CM33_NS, while ai_engine and the NPU are on the CM55, talking over IPC
   - c) MicroPython is on the CM33_S
   - d) The NPU is on the CM33_NS

   <details><summary>Solution</summary>

   **b** — heavy work such as the NPU, the model, and the screen live on the fast core, while the REPL and sensors live on the control core. CM33_S handles boot and security.

   </details>

2. What does edge_ai.active() return? *(single choice · objective 2)*
   - a) s_active, the model most recently requested
   - b) s_current, the model that has finished initialising and actually switched in
   - c) The total number of models
   - d) The latest seq value

   <details><summary>Solution</summary>

   **b** — active() goes through Q_ACTIVE, which returns ai_engine_active(). The most recently requested model is Q_REQUESTED, or ai_engine_requested().

   </details>

3. select(n) raises OSError, "select not confirmed." What does that mean? *(single choice · objective 2)*
   - a) The model name is wrong
   - b) The command was sent, but polling Q_ACTIVE never saw model n within the allotted time
   - c) The board has no NPU
   - d) IPC has been permanently disabled

   <details><summary>Solution</summary>

   **b** — select doesn't trust that a command succeeded just because it was sent. It waits to see the actual result. If it never sees it, it reports an error for us to handle with try/except.

   </details>

4. Where does r['latency_ms'] come from in ai_result_t? *(single choice · objective 3)*
   - a) seq
   - b) inference_us divided by 1000
   - c) inferences
   - d) top_class

   <details><summary>Solution</summary>

   **b** — the engine times each inference in microseconds, and MicroPython converts it to milliseconds. seq, meanwhile, increases every time it publishes.

   </details>

5. Within the same firmware image, where does a float32 model run? *(single choice · objective 4)*
   - a) On the Ethos-U55, same as int8
   - b) On the CPU, using TFLite-Micro's float kernels
   - c) It can't run at all
   - d) On the CM33_S

   <details><summary>Solution</summary>

   **b** — TFLite-Micro carries kernels for both types. The NPU only accepts Vela-compiled int8, so float32 models use the CPU, and are slower.

   </details>

## Lab

- [ ] Draw the three cores in your learning log, and write down which core your code, `ai_engine`, the NPU, and the screen each live on.
- [ ] Open `ai_engine.h`, find every field of `ai_result_t`, and write down which field each key of `result()` comes from.
- [ ] Open `ipc_model_link_defs.h`, find the values of `MODEL_LINK_CMD_SELECT_BASE` and `MODEL_LINK_Q_ACTIVE`, and explain how select confirms itself.

## Going further

In lesson 7.2, we'll fill in five read-side commands in `s18_under_the_hood.py`, then trace the stack's three log layers from the MicroPython end.

Next lesson: [lesson 7.2 — Hands-on: tracing the stack from MicroPython](../l02-trace-the-stack-lab/README.md)

## Reflect

- Why is designing select to confirm by observation safer than sending a command and waiting for a push-style ack?
- If your app needed to know instantly that a result had gone stale, which field of ai_result_t would you use?
