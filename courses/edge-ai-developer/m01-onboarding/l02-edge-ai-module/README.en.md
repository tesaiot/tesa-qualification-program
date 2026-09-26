---
id: edgeai-dev.m01.l02
lang: en
title: {th: 'โมดูล edge_ai: ถามทะเบียนโมเดล เลือก แล้วอ่านคำตอบ', en: 'The edge_ai module: list the models, select one, read its answer'}
summary: {th: 'ใช้สี่คำสั่งหลักของโมดูล edge_ai คือ models, select, result และ stop อ่านคำตอบของโมเดลเป็น dict แปลความ conf กับ CONF_FLOOR และ latency ให้ถูก แล้วรันเมนูหกโมเดลครั้งแรกบน Emulator หรือบอร์ด', en: 'Use the four core edge_ai calls (models, select, result, stop), read the model''s answer as a dict, interpret conf, CONF_FLOOR and latency correctly, and run the six-model menu for the first time on the emulator or the board.'}
level: L3
time_min: {concept: 30, practise: 20, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m01.l01]
objectives:
  - {th: 'เรียก edge_ai.models() แล้วอ่านคีย์ index, name, sensor และ labels ของแต่ละโมเดลได้ถูก และอธิบายว่าทำไมควรถามทะเบียนจากเฟิร์มแวร์แทนการ hard-code ชื่อหรือเลขโมเดล', en: 'Call edge_ai.models() and read each model''s index, name, sensor and labels keys correctly, and explain why you ask the firmware''s registry instead of hard-coding names or numbers.'}
  - {th: อธิบายว่า edge_ai.select(n) ยืนยันการสลับโมเดลด้วยการสังเกต (confirm by observation) และห่อการเรียกด้วย try/except OSError ได้, en: 'Explain that edge_ai.select(n) confirms the switch by observation, and wrap the call in try/except OSError.'}
  - {th: 'อ่าน dict จาก edge_ai.result() แล้วบอกได้ว่า label, top, conf, scores, latency_ms และ seq หมายถึงอะไร ตัดสินได้ว่าผลใดเชื่อได้ตาม CONF_FLOOR (0.50) และแปลง latency เป็นจำนวนครั้งต่อวินาทีได้', en: 'Read the dict from edge_ai.result(), say what label, top, conf, scores, latency_ms and seq mean, decide which results to trust against CONF_FLOOR (0.50), and convert latency to runs per second.'}
  - {th: รันเมนู Edge AI บน BENTO Emulator หรือบอร์ด เลือกโมเดล กด Load แล้วเห็นคลาสที่ชนะเปลี่ยนตามท่าทางหรือเสียง, en: 'Run the edge AI menu on the BENTO Emulator or the board, choose a model, press Load and see the winning class change with motion or sound.'}
develops: [{skill: ai.edge, to: 2}, {skill: lang.micropython, to: 2}, {skill: rtos.multicore-ipc, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
source_sha256: 77eb73ee690591a58c3e861bcf54c690f257cffb7940891ac3122a2206cde0d6
---

# Lesson 1.2 — The edge_ai module: list the models, select one, read its answer

> Module 1 — Getting started: run the real thing, then take it apart · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Use the four core edge_ai calls — models, select, result and stop — read the model's answer as a dict, interpret conf, CONF_FLOOR and latency correctly, and run the six-model menu for the first time on the emulator or the board.

## Objectives

By the end of this lesson, you will:

1. Call edge_ai.models() and read each model's index, name, sensor and labels keys correctly, and explain why you ask the firmware's registry instead of hard-coding names or numbers.
2. Explain that edge_ai.select(n) confirms the switch by observation, and wrap the call in try/except OSError.
3. Read the dict from edge_ai.result(), say what label, top, conf, scores, latency_ms and seq mean, decide which results to trust against CONF_FLOOR (0.50), and convert latency to runs per second.
4. Run the edge AI menu on the BENTO Emulator or the board, choose a model, press Load and see the winning class change with motion or sound.

## Before you start

Review from lesson 1.1 that MicroPython code lives on the Cortex-M33, while models live on the Cortex-M55 with the NPU. Keep [BENTO IDE](https://ide.tesaiot.dev/) open, and have a USB cable ready if you have a board — the whole lesson also works on the BENTO Emulator if you don't.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/) — on the emulator, model scores are simulated from a simulated sensor, and there are five models (no Push Detection).
- **Prior lesson:** [lesson 1.1 — What edge AI is: the five-stage data lifecycle and where a model can run](../l01-edge-ai-lifecycle/README.md)

## Concepts

The `edge_ai` module is the one window we have into the inference engine on the M55. This lesson uses just four calls — **models → select → result → stop** — which is the whole story of running a model: read the registry, select a model, read its answer, then stop.

`edge_ai.models()` returns a list of one dict per model, with the keys `index` (used when selecting), `name` (shown on screen), `sensor` (0 = IMU, 1 = RADAR, 2 = MIC), and `labels` (the classes the model can answer). The good habit is: **ask the hardware first — never guess.** If the firmware gains or loses models, code that reads from `models()` adapts on its own, which matters a lot, since the board and the emulator don't have the same number of models.

`edge_ai.select(n)` is a cross-core call. It sends the command, then keeps checking whether the engine has actually switched (confirm by observation). If it isn't confirmed within a set time, it throws `OSError`, so we always wrap it in `try/except OSError`. `start(n)` behaves the same way as `select(n)`.

`edge_ai.result()` returns the latest result as a dict, or `None` if there's no result yet: `label` is the winning class, `top` is that class's index, `conf` is confidence from 0 to 1, `scores` are the scores for every class, adding up to 1, `latency_ms` is how long the NPU took, and `seq` increases every time there's a new result. In mathematical terms, the winning class is $\arg\max_k s_k$, and the confidence is $\max_k s_k$. The value `CONF_FLOOR` = 0.50 is the threshold the firmware recommends — below this, the model isn't considered sure yet, because a model answers with a probability, not an absolute truth. Latency can also be converted to runs per second with $\text{fps} = 1000 / t_{\text{ms}}$ — for example, 4.1 ms ≈ 244 runs per second.

## Worked example

Open `12_edge_ai_menu.py` and see first how the real Edge AI page uses these four calls. **Predict** before you run it: what happens if you select Motion and shake the board? Then run it and compare.
The file we'll fill in ourselves is in lesson 1.3.

| File | What this file teaches |
|---|---|
| [examples/12_edge_ai_menu.py](examples/12_edge_ai_menu.py) | Edge AI Menu: select and run any AI model in one firmware image (no network needed) |

This lesson's slides also reference a file in another lesson, and one under `shared/`:

- [m01-onboarding/l03-first-inference-lab/practice/s01_first_inference.py](../l03-first-inference-lab/practice/s01_first_inference.py) — running our first edge AI model (the fill-in-the-code version)

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. Why does the code in this course read model names from edge_ai.models() instead of hard-coding a name or model number? *(single choice · objective 1)*
   - a) Because models() is faster than writing a list yourself
   - b) Because different boards' firmware has different numbers of models — reading from the registry lets the code adapt automatically, with no changes needed
   - c) Because select() only accepts a model name
   - d) Because the emulator has no models at all

   <details><summary>Solution</summary>

   **b** — the habit of "ask the hardware first, never guess" means the same code works on both a six-model board and a five-model emulator. A different order doesn't break anything either.

   </details>

2. If edge_ai.select(n) sends the command but the engine doesn't switch within the set time, what happens? *(single choice · objective 2)*
   - a) select() quietly returns None and the program continues
   - b) select() throws OSError, so we must wrap it in try/except OSError
   - c) The board reboots itself
   - d) The previous model is removed from the registry

   <details><summary>Solution</summary>

   **b** — select() confirms by observing that the active model genuinely changed. If it doesn't see that, it throws OSError, so the program never lies about what's running.

   </details>

3. The result is {'label': 'circle', 'conf': 0.41, ...} and CONF_FLOOR = 0.50. What should you do with this answer? *(single choice · objective 3)*
   - a) Trust it right away, since circle won
   - b) Treat it as not sure yet, since conf is below CONF_FLOOR — don't act on this answer yet
   - c) Call select() again every time conf is low
   - d) Multiply conf by 2 to pass the threshold

   <details><summary>Solution</summary>

   **b** — argmax always picks a winner, even when scores are close. CONF_FLOOR is the cutoff on the conf value: only trust the answer when conf ≥ 0.50.

   </details>

4. latency_ms = 5 means the model can run at most roughly how many times per second? *(single choice · objective 3)*
   - a) 5 times
   - b) 50 times
   - c) 200 times
   - d) 5000 times

   <details><summary>Solution</summary>

   **c** — fps = 1000 / t_ms = 1000 / 5 = 200 runs per second, which is plenty compared to a loop that reads results roughly every 180 ms.

   </details>

5. On the BENTO Emulator, you select Motion Detection, press Load, then drag to tilt the board or press Shake. What should you see? *(single choice · objective 4)*
   - a) The winning class switches between idle / circle / shaking, along with a confidence bar for every class
   - b) The model list disappears from the dropdown
   - c) The screen shows Push every time
   - d) Nothing changes until you connect WiFi

   <details><summary>Solution</summary>

   **a** — Motion has three classes: idle, circle, shaking. On the emulator, scores are simulated from a simulated sensor, so they change with the tilting or shaking we simulate, with no network needed at all.

   </details>

## Lab

- [ ] In the REPL or in a file, type `edge_ai.models()` and note down how many models your board or emulator has, their names, and which sensor each uses.
- [ ] Run the menu on the emulator (or the board), select Motion Detection, press Load, and watch the winning class change to idle / circle / shaking.
- [ ] If you have a board, try switching to at least one microphone model, and make a sound to change the class.

## Going further

In lesson 1.3, we'll walk through the `s01_first_inference.py` file and fill in four gaps ourselves until the menu works end to end.

Next lesson: [lesson 1.3 — Hands-on: our first model menu](../l03-first-inference-lab/README.md)

## Reflect

- If CONF_FLOOR is set too low or too high, what kind of mistake would your app make?
- Why does select() have to "wait and see" that the switch genuinely happened, instead of trusting that the command succeeded?
