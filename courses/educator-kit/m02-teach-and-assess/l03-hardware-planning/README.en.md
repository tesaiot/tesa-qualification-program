---
id: edu.m02.l03
lang: en
title:
  th: วางแผนฮาร์ดแวร์
  en: Planning the hardware
summary:
  th: วางแผนบอร์ดหนึ่งตัวต่อผู้เรียนสามถึงสี่คนร่วมกับอีมูเลเตอร์ การหมุนเวียนบทบาทในกลุ่ม remote flash การยืมคืน และรายการตรวจก่อนแล็บ
  en: Plan one board per three to four learners alongside the emulator, rotate roles in each group, use remote flash, run a lending scheme, and check readiness before labs.
level: L3
time_min: {concept: 15, practise: 25, check: 5}
hardware: {emulator: true, boards: [none, eva-kit, devkit]}
prerequisites: [edu.m02.l02]
objectives:
  - th: คำนวณจำนวนบอร์ด สายต่อ และเครื่องคอมพิวเตอร์ที่ต้องใช้สำหรับรายวิชาของตัวเอง โดยใช้อัตราบอร์ดหนึ่งตัวต่อผู้เรียนสามถึงสี่คนและมีสำรอง
    en: Compute the boards, cables and computers your course needs at one board per three to four learners, with spares.
  - th: ออกแบบการหมุนเวียนบทบาทในกลุ่ม ให้ทุกคนได้ลงมือบนบอร์ดและทุกคนทำงานในอีมูเลเตอร์ระหว่างรอ
    en: Design a role rotation so every learner gets board time and everyone works in the emulator while waiting.
  - th: เลือกได้ว่าเมื่อใดควรใช้ remote flash และอธิบายขั้นตอนการใช้ตามที่หน้าบริการแสดง
    en: Decide when to use remote flash and describe the steps as the service page shows them.
develops:
  - {skill: edu.facilitation, to: 3}
  - {skill: sys.simulation, to: 2}
assesses:
  - {skill: edu.facilitation, level: 3, evidence: resources/hardware-checklist.md}
context: {audience: educator, platform: psoc-edge-e84, ide: bento-ide, emulator: bento-emulator}
status: alpha
translation: done
slides: slides.md
source_sha256: 3620ef8de0e60b0c200cb2dfa533134a363a81d857957e31da31b025f40800cf
---

## Objectives

1. Compute the hardware you need
2. Design a role rotation within groups
3. Decide when to use remote flash

## Before you start

- From the previous lesson, what kind of graded work must be done on a board in front of the assessor?
- From the teaching-methods lesson, which activities can be done in the emulator, and which need a real board?

## See it work first

Open [BENTO IDE](https://ide.tesaiot.dev/), press the **BENTO Emulator** button, then press **HW**. You will see a simulated hardware panel with LEDs, buttons, a knob and a tilt pad.
Every learner can use this at the same time with no board at all. This is why your course does not need one board per learner.

## Concepts

### 1. One board per three to four learners; everyone has an emulator

The recommended ratio is one board per three to four learners, and **everyone** uses the emulator on their own machine.
Work that can be done in the emulator (understanding the API, filling in practice, designing the screen) does not need to wait its turn for a board; the board is reserved for work that genuinely needs it.
This number is a guideline, not a rule. More boards are always better; with fewer, move more work into the emulator and use remote flash.

### 2. Rotate roles so nobody just watches

A group with a single board often ends up with the strongest person typing the whole lab. Prevent this with roles that rotate every 15 minutes.

| Role | What they do |
|---|---|
| Driver | Types and runs on the board |
| Navigator | Reads the brief, calls out the next step, checks against the objectives |
| Tester | Runs the same code in the emulator and compares the result with the board |
| Recorder | Collects evidence, images, logs and predictions into the group's portfolio |

### 3. Remote flash

For firmware that must be flashed as a `.hex` file, the [TESAIoT Remote Flash](https://flash.tesaiot.dev/) service lets a browser send a file to be flashed onto a board connected to a different machine.
As the service page shows it, the steps are: create a pairing code on the web page, enter the code in the TESAIoT Programmer app on the machine the board is connected to,
then choose the `.hex` file and start flashing. This is useful when

- All the boards are connected to machines in the lab, and learners submit work from their own machines
- Learners are studying remotely, and the institution has boards connected and ready

Before using it with a whole class, try pairing and flashing yourself once first.

### 4. What the emulator does not tell you

The emulator answers well whether a program runs to completion and what the screen looks like, but WiFi is simulated, sensor values are simulated,
and some hardware limits, such as the time a board is not yet ready to answer about sensors right after power-on, never show up in a browser.
Instructors should run the lab's example on a real board first every time, and tell learners in advance where the results differ.

## Worked example

A course has 30 learners, with a 3-hour lab each week.

- **Move 1: number of boards** 30 ÷ 4 = 7.5, rounded up to 8 groups, plus 2 spares, totalling 10 boards, and 12 USB data cables
- **Move 2: machines** Learners use their own laptops for the emulator; the lab room has 8 machines connected to boards
- **Move 3: timing** The first half of the lab, everyone works in the emulator; the second half rotates roles every 15 minutes on the board
- **Move 4: network** Test before the term starts that the lab network needs no web login and does not block the ports the MQTT lesson uses

## Practice

Copy [resources/hardware-checklist.md](resources/hardware-checklist.md) and fill it in fully for your own course, together with a role-rotation table for one lab.

## Check your understanding

Answer the questions in [quiz.yaml](quiz.yaml). A score of 80% or more passes.

## Going further

The next lesson is the final module, on trainer training and the path to becoming a TQP Certified Trainer.

## Reflect

If half your boards broke on lab day, what would your backup plan be, and which learning outcomes would learners still fully achieve?
