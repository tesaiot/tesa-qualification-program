---
id: edu.m03.l01
lang: en
title:
  th: อบรมผู้สอนและเส้นทางสู่ TQP Certified Trainer
  en: Train-the-trainer and the path to TQP Certified Trainer
summary:
  th: เตรียมตัวเข้าเวิร์กช็อป train-the-trainer สองวัน วางแผนการสาธิตการสอน และรู้เงื่อนไขของใบรับรอง TQP Certified Trainer ตามกติกาของ TESA
  en: Prepare for the two-day train-the-trainer workshop, plan a teaching demonstration, and know the conditions of the TQP Certified Trainer credential under TESA's rules.
level: L3
time_min: {concept: 20, practise: 30, check: 5}
hardware: {emulator: true, boards: [none, eva-kit, devkit]}
prerequisites: [edu.m02.l03]
objectives:
  - th: ระบุเงื่อนไขของ TQP Certified Trainer ได้ครบสามข้อ และบอกอายุของใบรับรองได้
    en: State all three conditions of TQP Certified Trainer and the credential's validity period.
  - th: วางแผนการสาธิตการสอนหนึ่งบทเรียนยาว 20 นาที ที่ครอบคลุมทวนบทก่อน ดูของจริงก่อน ตัวอย่างที่มีป้ายขั้นตอน และเช็กความเข้าใจ
    en: Plan a 20-minute teaching demonstration of one lesson covering retrieval, see-it-work, a subgoal-labelled example and a check.
  - th: อธิบายกติกาความเป็นกลางที่ผู้สอนต้องปฏิบัติเกี่ยวกับการสอบ TQP ได้
    en: Explain the impartiality rules a trainer must follow regarding TQP exams.
develops:
  - {skill: edu.facilitation, to: 3}
  - {skill: edu.lesson-design, to: 3}
  - {skill: edu.assessment, to: 2}
context: {audience: educator, credential: TQP Certified Trainer}
status: alpha
translation: done
slides: slides.md
source_sha256: 66626de0dbc7061589997bf2735dd20651985157eab13b1b62659c799ebcef59
---

## Objectives

1. Know the conditions of TQP Certified Trainer
2. Plan a 20-minute teaching demonstration
3. Understand the impartiality rules around exams

## Before you start

- From the previous lesson, what are the four roles in a group with a single board?
- In the lesson you will teach, at what minute do learners see something working?

## See it work first

Open [tqp/certification.md](../../../../tqp/certification.md) and look at the **Trainer** row in the credential tier table, and the "Impartiality" section.
These two parts are the whole set of rules this lesson explains. If anything in this lesson conflicts with that file, the file wins.

## Concepts

### 1. What TQP Certified Trainer is

Per [tqp/certification.md](../../../../tqp/certification.md), TQP Certified Trainer certifies that the holder **can teach courses aligned with TQP**.
It is issued jointly under TESA × Infineon, is valid for **2 years**, and has three conditions.

1. **Hold an L4 certificate in the subject taught.** A trainer must be able to perform at a level higher than what learners are required to reach.
2. **Complete the trainer course**, meaning this educator kit, together with the train-the-trainer workshop.
3. **Demonstrate teaching in front of a panel.**

Every tier of the TQP credential is not yet open for applications until announced in tqp/certification.md, per the rollout plan; the trainer course is in Phase 2.
In the meantime, you can prepare by completing this kit fully, and by teaching for real using the model you chose in the first module.

### 2. The two-day train-the-trainer workshop (outline)

| Block | Day 1 | Day 2 |
|---|---|---|
| Morning | Review the educator kit: adoption models, the crosswalk table, TESA attribution | Practise assessment: single-point rubrics, graded work that holds up against public solutions |
| Afternoon | Hands-on with the board and emulator, in the role of a learner, cycling through every role in a group | Practise a teaching demonstration with fellow trainers, get feedback, then demonstrate for real |
| End of day | Reflect on where your learners are likely to get stuck | Plan the first term, and the trainer community's channels for exchange |

This outline is the educator kit's plan; the actual details of each cohort will be announced by TESA.

### 3. What a good teaching demonstration looks like

The 20-minute demonstration is not a short lecture. It shows that you can run a learning experience by the principles in the second module.

- Open with a retrieval question from the previous lesson (no more than 2 minutes)
- Let learners see something working, and have them predict before running it
- Teach the concept in short segments of no more than 6 minutes
- Walk through an example labelled Move 1, 2, 3
- Close with a check for understanding tied to the objectives, and say what you would do next if a learner got a particular question wrong

### 4. Impartiality

Training and certification must stay separate, under the rules in tqp/certification.md.

- **A trainer does not examine someone they taught within 2 years**
- **Candidates are not required to take a TESA course to sit the exam**; equivalent alternative paths are accepted
- Trainers do not receive TQP exam content, and should not promise learners that studying with them guarantees a pass
- Your course does not become a "TESA-certified course" just because you hold a Trainer credential; see the lesson on TESA attribution

## Worked example

A 20-minute demonstration plan for the lesson [Read a sensor and watch the value change](../../../explorer/m02-sense-and-connect/l01-read-a-sensor/README.md)

- **Move 1 (0–2 min)** Ask a retrieval question: "why does it need `str()` before passing to Seg7?"
- **Move 2 (2–6 min)** Open the emulator, have learners predict what will move on screen when the knob is turned, then run it
- **Move 3 (6–11 min)** Explain `sensors.snapshot()` and "ask before you take"
- **Move 4 (11–16 min)** Walk through Moves 1–5 of the example, and explain where a real board differs from the emulator
- **Move 5 (16–20 min)** Two check-for-understanding questions, and say what you would look at next if a learner got the `OSError` question wrong

## Practice

Write a 20-minute demonstration plan for the lesson you will actually teach, in the five-move form above, then rehearse it with a colleague once and ask for two pieces of feedback.

## Check your understanding

Answer the questions in [quiz.yaml](quiz.yaml). A score of 80% or more passes, and completes this educator kit.

## Going further

- Go back to [catalog/tracks.yaml](../../../../catalog/tracks.yaml) and look at the educator pathway and the course you will teach
- Share your teaching plan with the community through this repository's [GitHub Issues](https://github.com/tesaiot/tesa-qualification-program/issues);
  do not forget to credit TESA for anything adapted from the repository

## Reflect

If your learners sit the TQP exam a year from now, what have you taught that they will actually use in the practical exam room, and what should you stop teaching because it does not help?
