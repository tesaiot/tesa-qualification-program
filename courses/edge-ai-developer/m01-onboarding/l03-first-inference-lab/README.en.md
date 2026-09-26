---
id: edgeai-dev.m01.l03
lang: en
title: {th: 'ลงมือทำ: เมนูโมเดลตัวแรกของเรา', en: 'Hands-on: your first model menu'}
summary: {th: 'ไล่โค้ดไฟล์ s01_first_inference.py ตามโครงสี่จังหวะของโปรแกรม MicroPython แล้วเติมสี่ช่องด้วยคำสั่ง select, result, verdict.text และ stop จนเมนู Edge AI ทำงานครบวงจรและปิดตัวเองอย่างเรียบร้อย', en: 'Walk through s01_first_inference.py along the four-beat MicroPython program skeleton, then fill its four blanks with select, result, verdict.text and stop until the edge AI menu works end to end and shuts down cleanly.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 20, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m01.l02]
objectives:
  - {th: 'ชี้ได้ว่าส่วนใดของ s01_first_inference.py อยู่ในจังหวะ import, สร้างครั้งเดียว, ลูป และ ui.poll และอธิบายว่าทำไมต้องสร้าง widget นอกลูป', en: 'Point out which parts of s01_first_inference.py belong to the import, create-once, loop and ui.poll beats, and explain why widgets are created outside the loop.'}
  - {th: เติมสี่ช่องใน practice/s01_first_inference.py จนกด Load แล้วเห็นคลาสที่ชนะและแถบความมั่นใจทุกคลาสเปลี่ยนตามท่าทางหรือเสียง และกด Stop แล้วโมเดลหยุดจริง, en: 'Fill the four blanks in practice/s01_first_inference.py until Load shows the winning class and every class''s confidence bar changing with motion or sound, and Stop really stops the model.'}
  - {th: 'อธิบายว่าการเช็ก r[''seq''] ก่อนวาดจอ และบล็อก finally ที่เรียก edge_ai.stop() ป้องกันปัญหาอะไร', en: 'Explain what checking r[''seq''] before redrawing and the finally block that calls edge_ai.stop() protect against.'}
  - {th: หาท่าหรือเสียงที่ทำให้ conf ต่ำกว่า 50% แล้วอธิบายได้ว่าทำไมคะแนนถึงกระจาย, en: Find a motion or sound that keeps conf below 50% and explain why the scores spread out.}
develops: [{skill: lang.micropython, to: 2}, {skill: ai.edge, to: 2}, {skill: gui.embedded, to: 1}]
assesses: [{skill: lang.micropython, level: 2, evidence: practice/s01_first_inference.py}, {skill: ai.edge, level: 2, evidence: practice/s01_first_inference.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
source_sha256: 5ff2bf8dfa86ed3b3541d58f465320ba96b2d34f7ac0cc38048349127f1c387e
---

# Lesson 1.3 — Hands-on: your first model menu

> Module 1 — Getting started: run the real thing, then take it apart · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Walk through the s01_first_inference.py file along the four-beat MicroPython program skeleton, then fill its four blanks with the select, result, verdict.text and stop calls until the edge AI menu works end to end and shuts down cleanly.

## Objectives

By the end of this lesson, you will:

1. Point out which parts of s01_first_inference.py belong to the import, create-once, loop and ui.poll beats, and explain why widgets are created outside the loop.
2. Fill the four blanks in practice/s01_first_inference.py until Load shows the winning class and every class's confidence bar changing with motion or sound, and Stop really stops the model.
3. Explain what checking r['seq'] before redrawing and the finally block that calls edge_ai.stop() protect against.
4. Find a motion or sound that keeps conf below 50% and explain why the scores spread out.

## Before you start

You've been through lesson 1.2, and know what the four calls models, select, result, stop do. Open the practice file in BENTO IDE, and keep your notes ready to record what motion or sound each model needs to win.

- **Hardware:** a TESAIoT Dev Kit board already flashed with BENTO's MicroPython firmware, or the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/)
- **Prior lesson:** [lesson 1.2 — The edge_ai module: list the models, select one, read its answer](../l02-edge-ai-module/README.md)

## Concepts

Nearly every MicroPython program on BENTO follows **four beats**: import → create widgets once → a loop that reads values and updates the screen → `ui.poll`, which handles buttons and touches, then loops back. Creating widgets outside the loop, and only changing their values inside it, keeps the screen from flickering and saves memory. The `s01_first_inference.py` file reads as a single sentence: ask what models exist → select one → loop reading results → put the winning class on screen → stop on exit.

The four blanks are exactly the four core calls: the Load button calls `edge_ai.select(sel)` inside a `try`, and only shows RUNNING **after** select succeeds. Inside the loop, it reads `r = edge_ai.result()` and only redraws when `r['seq']` changes, using `verdict.text(r['label'] or '-')` and a bar for every class from `r['scores']` (the class where `i == top` is coloured green). The Stop button calls `edge_ai.stop()`, and the `finally` block, already given, stops the engine every time you exit — whether that's the back button or an error. This is an embedded systems habit: always leave the machine in a state you know for certain.

Success in this lesson isn't just "the text moves" — you should be able to say what `conf` 92% actually means, and why the model isn't sure yet for some motions. A motion halfway between two classes, or a sound that resembles several classes, spreads the score out, with no class winning by much.

## Worked example

Use the help ladder in order: the `# TODO:` hints in the practice file → the fill-in table in the slides → the solution → the full version. `s01_first_inference_full.py` is a polished version that adds latency and uses `CONF_FLOOR` to colour "confident" apart from "not sure yet". Open it once you've passed the practice file, and find what's different from your own file.

| File | What this file teaches |
|---|---|
| [examples/s01_first_inference_full.py](examples/s01_first_inference_full.py) | A 6-model edge AI menu (full version) |

## Practice

The file has 4 blanks, each marked with a `# TODO:` comment. Fill them in this order, and test after each one: 1) the Load button → `edge_ai.select(sel)` 2) inside the loop → `r = edge_ai.result()` 3) on a new result → `verdict.text(r['label'] or '-')` 4) the Stop button → `edge_ai.stop()`. If you forget blank 1, it will show RUNNING with no results at all. If you forget blank 3, the bars move but the large winning-class text never changes. If nothing shows up, check your indentation and call names first.

| Practice file | Topic |
|---|---|
| [practice/s01_first_inference.py](practice/s01_first_inference.py) | Running our first edge AI model (the fill-in-the-code version) |

## Solution

Open the solution after trying on your own at least once, and read [how to use the solutions](../../README.en.md#how-to-use-the-solutions) first.

| Solution | Pairs with |
|---|---|
| [solution/s01_first_inference.py](solution/s01_first_inference.py) | [practice/s01_first_inference.py](practice/s01_first_inference.py) |

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automated checking.

1. Put the four beats of a MicroPython program on BENTO in order *(ordering · objective 1)*
   - a) Loop: read results then update the screen
   - b) import: edge_ai, ui, lcd, time
   - c) ui.poll: handle buttons and touches
   - d) create-once: read models() and create widgets

   <details><summary>Solution</summary>

   **b → d → a → c** — import → create-once → loop → ui.poll, then loop back. Widgets are created outside the loop, and only their values change inside it, so the screen doesn't flicker.

   </details>

2. You filled in the practice file. Pressing Load shows RUNNING, but there's never any inference result at all. Which blank was most likely left unfilled? *(single choice · objective 2)*
   - a) Blank 1: edge_ai.select(sel) in the Load button
   - b) Blank 3: verdict.text(...)
   - c) Blank 4: edge_ai.stop()
   - d) The import lcd line

   <details><summary>Solution</summary>

   **a** — if select() is never called, the model is never actually told to run, yet the code still shows RUNNING on the following line. The fill-in table in the slides notes this symptom directly.

   </details>

3. The confidence bars move for every class, but the large winning-class text never changes. Which blank is still unfilled? *(single choice · objective 2)*
   - a) r = edge_ai.result()
   - b) verdict.text(r['label'] or '-')
   - c) edge_ai.stop()
   - d) edge_ai.select(sel)

   <details><summary>Solution</summary>

   **b** — the bars come from r['scores'], which is already given, proving result() is working. The large text still needs verdict.text filled in yourself.

   </details>

4. Which of these correctly explain the reasoning behind checking r['seq'] and the finally block? (select every correct answer) *(multiple choice · objective 3)*
   - a) Checking seq means only redrawing when there's a new result, instead of redrawing every round
   - b) finally means edge_ai.stop() is called no matter how you exit, so the engine never keeps running unattended
   - c) seq is the model's confidence, as a percentage
   - d) finally means the program can never have an error

   <details><summary>Solution</summary>

   **a, b** — seq increases every time there's a new result, telling you whether to redraw. finally doesn't prevent errors — it guarantees that the engine is always stopped on the way out.

   </details>

5. If you make a motion halfway between circle and shaking, what do you typically see on screen? *(single choice · objective 4)*
   - a) One class wins outright at 100%
   - b) The score is split between the two classes; the winner's conf is low, possibly below 50%
   - c) The model stops working
   - d) latency_ms becomes zero

   <details><summary>Solution</summary>

   **b** — when the data resembles several classes, softmax splits the score across them, so the winner only wins narrowly. This is exactly why CONF_FLOOR exists.

   </details>

## Lab

**The MVP for lessons 1.1–1.3:** run the `edge_ai` menu and read live results — both the winning class (`label`) and the confidence (`conf`) change with real motion or sound.

- [ ] All four blanks in the practice file are filled in, and it runs on the emulator or the board.
- [ ] Switch between at least three models, and note in your learning log what each one needs to win.
- [ ] Find a motion or sound that keeps conf below 50%, and explain why.
- [ ] Be able to explain where in the code models, select, result and stop are called, and what each one does.

## Going further

In the next pair of lessons (1.4–1.5), we'll take the sensor app apart piece by piece, nail down the four-beat structure completely, and remix it into something of our own.

Next lesson: [lesson 1.4 — Taking apart the sensor app: the shared four-beat structure of every program](../l04-sensor-app-anatomy/README.md)

## Reflect

- If you removed the `seq` check, how would the screen's behaviour change, and who pays the price for that?
- Which model was hardest for you to make win, and do you think that's because of the model, or because of how we fed it data?
