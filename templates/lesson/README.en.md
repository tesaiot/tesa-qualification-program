---
id: "<short>.m01.l01"                 # same id as the Thai file
lang: en
title:
  th: "<ชื่อบทเรียน>"
  en: "<Lesson title>"
summary:
  th: "<บทเรียนนี้พาผู้เรียนไปทำอะไรได้>"
  en: "<What this lesson lets the learner do>"
level: L2
time_min: {concept: 10, practise: 20, lab: 20, check: 5}
hardware: {emulator: true, boards: [eva-kit, devkit]}
prerequisites: []
objectives:
  - th: "<เขียนโปรแกรมนับถอยหลังจาก N ถึง 1 ใน BENTO Emulator ได้ถูกต้อง>"
    en: "<Write a program that counts down from N to 1 in the BENTO Emulator>"
  - th: "<อธิบายได้ว่าทำไม range(3, 0, -1) หยุดที่ 1 โดยอ้างค่า stop>"
    en: "<Explain why range(3, 0, -1) stops at 1, referring to the stop value>"
develops:
  - {skill: lang.micropython, to: 2}
assesses:
  - {skill: lang.micropython, level: 2, evidence: practice/01_countdown.py}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: pre-alpha
translation: pending                  # keep equal to the Thai file
slides: slides.md
# source_sha256: <value printed by: python3 tools/i18n_stale.py --hash <lesson folder>/README.md>
---

<!--
Lesson template (English). The Thai README.md is the source; this file repeats its front matter with lang: en.
After translating, record source_sha256 (see the comment above) and set translation: done in BOTH files.
Guide (Thai): templates/AUTHORING.md
-->

## Objectives

By the end of this lesson you will be able to:

1. «Objective 1, matching objectives[0] in the front matter»
2. «Objective 2»

About 55 minutes «the total of time_min».

## Before you start

Two review questions. Answer them in your head before reading on.

1. «Review question 1 from an earlier lesson»
2. «Review question 2»

## See it work first

Open [examples/01_countdown.py](examples/01_countdown.py) in BENTO IDE (https://ide.tesaiot.dev/). **Predict** what the screen
will show, then run it.

## Concept

«At most three chunks of at most 6 minutes or one screen each.»

## Worked example

[examples/01_countdown.py](examples/01_countdown.py) works in three steps:

- **Step 1** set the values we will experiment with
- **Step 2** count down one at a time
- **Step 3** pause between rounds, then say we are done

Change `COUNT_FROM` to 5, predict what you will see, then run it.

## Practice

Open [practice/01_countdown.py](practice/01_countdown.py) and fill in the blanks so the program behaves like the example.

## Solution

Try on your own for at least 15 minutes before opening [solution/01_countdown.py](solution/01_countdown.py). Its comments explain
why each line is the way it is.

## Check your understanding

Answer the questions in [quiz.yaml](quiz.yaml). 80% or more completes the lesson.

## Lab

«Hands-on work on a board or the emulator (Modify → Make). Say exactly what evidence to keep for the portfolio.»

## Going further

«A challenge, a datasheet or application note to read, or a real industry use case.»

## Reflect

- What surprised you in this lesson?
- Where could this code fail in a real product?
