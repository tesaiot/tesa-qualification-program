---
id: edu.m01.l01
lang: en
title:
  th: สี่รูปแบบการนำหลักสูตรไปใช้
  en: Four ways to adopt the courses
summary:
  th: เลือกรูปแบบการนำ TESA Open Knowledge ไปใช้ในสถาบันของคุณ ระหว่างวิชาเลือกเต็ม แทรกโมดูลในวิชาเดิม ห้องเรียนกลับด้าน และสอนร่วมกับ TESA พร้อมแผนเวลาสำหรับช่วงสอน 1.5 และ 3 ชั่วโมง
  en: Choose how to adopt TESA Open Knowledge in your institution (full elective, drop-in modules, flipped, co-taught with TESA), with timing plans for 1.5-hour and 3-hour slots.
level: L3
time_min: {concept: 20, practise: 25, check: 5}
hardware: {emulator: false, boards: [none]}
prerequisites: []
objectives:
  - th: เปรียบเทียบสี่รูปแบบการนำไปใช้ในด้านเวลา ทรัพยากร และความเสี่ยง แล้วเลือกรูปแบบที่เหมาะกับบริบทของตัวเองพร้อมเหตุผลอย่างน้อย 2 ข้อ
    en: Compare the four adoption models on time, resources and risk, and choose one for your context with at least two reasons.
  - th: จัดบทเรียนหนึ่งบทลงในแผนเวลาของช่วงสอน 1.5 หรือ 3 ชั่วโมง โดยทุกช่วงกิจกรรมยาวไม่เกิน 10 นาที ยกเว้นแล็บ
    en: Fit one lesson into a 1.5-hour or 3-hour slot plan in which every activity segment except the lab is at most 10 minutes.
  - th: ระบุความเสี่ยงของการให้ผู้เรียนเรียนเองล้วนโดยไม่มีโครงสร้าง และมาตรการลดความเสี่ยงอย่างน้อย 2 ข้อ
    en: Identify the risk of pure self-paced study without structure and at least two mitigations.
develops:
  - {skill: edu.lesson-design, to: 2}
  - {skill: edu.facilitation, to: 2}
context: {audience: educator, lang: none}
status: alpha
translation: done
source_sha256: 4570c173c54b941b71c76ffb1848a90fa0169707e31c8941476e964b25087ec8
---

## Objectives

1. Choose an adoption model that fits your context, with reasons
2. Fit a lesson into a 1.5-hour or 3-hour teaching slot
3. Design structure that helps learners finish

## Before you start

- Does your course already have a topic on microcontrollers, IoT or edge AI? If so, in which week?
- How many development boards does your institution have, and how many learners per class?

## See it work first

Open the course pages of [AIoT in Action](../../../aiot-micropython/README.md) and [Explorer](../../../explorer/README.md) and look at two things.
First, each lesson states its time in minutes, broken into segments (`time_min`). Second, every lesson has objectives, a check for understanding, and some lessons have a practice file with a solution.
What you get from TESA Open Knowledge is pieces that fit together, not a finished course you must teach as one solid block.

## Concepts

### 1. Four models

| Model | What it looks like | Fits when | What to prepare |
|---|---|---|---|
| **Full elective** | One course is used as the spine of an entire subject | You can open a new subject, and have enough boards for labs | A full-course learning-outcome crosswalk, complete assessment, a hardware plan |
| **Drop-in modules** | Take one or two modules to replace an existing topic in a microcontroller or IoT course | You cannot restructure a large course, but want to modernise the content | Check which topic the module replaces, and whether it fits the same number of hours |
| **Flipped classroom** | Learners read the lesson and complete the check for understanding before class; class time goes to hands-on lab work on the board | Lab hours are scarce, boards are limited | Set a deadline for the check for understanding before the lab slot, and track who has not done it |
| **Co-taught with TESA** | Your institution's instructor teaches together with a TESA speaker or the TESA network, for example in a camp or before a competition | Starting from scratch, instructors are not yet familiar with the board | Contact TESA in advance, agree on roles and assessment |

No model is the best. Most institutions start with "drop-in modules" for one term, gather data on how well it works, and then expand to a full elective.

### 2. The unit of planning is the lesson, not the course

Each lesson takes 20–75 minutes and states its time broken into concept, practice, lab and check segments, so you can fit lessons into a teaching slot like stacking blocks.
The rule is **each activity segment is at most 6–10 minutes**, except the lab, alternating the type of activity, because learner attention drops quickly during long stretches of listening.
Template timing plans for 1.5-hour and 3-hour slots are at [resources/slot-plans.md](resources/slot-plans.md).

### 3. Pure self-paced study usually does not finish

Data from MOOCs run by MIT and Harvard on edX in 2017–18 reported that only about three percent of people who registered finished
([Reich & Ruipérez-Valiente 2019, *Science*](https://doi.org/10.1126/science.aav7958)),
and large-scale experiments found that light nudges, such as reminder messages or planning prompts, help very little once scaled up
([Kizilcec et al. 2020, *PNAS*](https://doi.org/10.1073/pnas.1921417117)).

What helps is **structure**: a cohort moving together, deadlines, an instructor to answer questions, and evidence of completion.
If you have learners use TESA Open Knowledge outside class, set a deadline per lesson, and measure completion per lesson, not per course.

## Worked example

An instructor teaches a 15-week microcontroller course, 3 hours a week, and wants to add IoT without expanding the course.

- **Move 1: choose a model** Drop-in modules — use the IoT module from AIoT in Action to replace the existing three weeks of serial-communication topics.
- **Move 2: compare the time** Add up the `time_min` of the lessons in that module and compare with the 9 hours available; anything over that becomes pre-class flipped work.
- **Move 3: build structure** The end-of-lesson check for understanding must be submitted before the lab hour; the lab is done in groups on the board; evidence goes into a portfolio.
- **Move 4: write the documentation** Add rows to the learning-outcome crosswalk table (next lesson), and put the TESA attribution in the course specification document (lesson 3 of this module).

## Practice

Choose one of your own courses and fill in the table.

| Question | Your answer |
|---|---|
| The model you chose, and two reasons | |
| The course or module you will use | |
| Hours available, compared with the total `time_min` | |
| Structure that helps learners finish (deadlines, cohort, who answers questions) | |

Then choose one lesson and lay it out in the template at [resources/slot-plans.md](resources/slot-plans.md).

## Check your understanding

Answer the questions in [quiz.yaml](quiz.yaml). A score of 80% or more passes.

## Going further

The models this educator kit draws on include [Arm Education Kits](https://www.arm.com/resources/education/education-kits)
and the [Microsoft IoT for Beginners teacher guide](https://github.com/microsoft/IoT-For-Beginners/blob/main/for-teachers.md), which also describes flipped use.

## Reflect

If you were starting next term, would your biggest constraint be time, boards, or instructor familiarity, and does the model you chose fix that constraint or work around it?
