---
id: edu.m02.l01
lang: en
title:
  th: วิธีสอนที่ได้ผลกับการเขียนโปรแกรมระบบฝังตัว
  en: Teaching methods that work for embedded programming
summary:
  th: ใช้ PRIMM ตัวอย่างที่มีป้ายขั้นตอน ไฟล์ฝึกที่ตัวช่วยค่อย ๆ ลดลง แบบฝึก Parsons การทดสอบย้อนหลังแบบเว้นระยะ และการแบ่งงานระหว่างอีมูเลเตอร์กับบอร์ดจริง พร้อมงานวิจัยที่รองรับ
  en: Use PRIMM, subgoal-labelled examples, fading practice files, Parsons problems, spaced retrieval and a clear emulator-versus-board split, with the research behind each.
level: L3
time_min: {concept: 25, practise: 25, check: 5}
hardware: {emulator: true, boards: [none, eva-kit, devkit]}
prerequisites: [edu.m01.l03]
objectives:
  - th: จัดลำดับกิจกรรมของตัวอย่างหนึ่งไฟล์ตาม PRIMM (Predict, Run, Investigate, Modify, Make) ได้ครบห้าขั้น
    en: Sequence the activities around one example file through all five PRIMM stages.
  - th: ออกแบบไฟล์ฝึกสามไฟล์ในโมดูลเดียวให้ตัวช่วยลดลงตามลำดับ (ตัวอย่างเต็ม ราว 2 ช่องว่าง ราว 6 ช่องว่าง) และแปลงหนึ่งไฟล์เป็นแบบฝึก Parsons
    en: Design three practice files in one module with fading support (full example, about 2 blanks, about 6 blanks) and turn one into a Parsons problem.
  - th: แบ่งกิจกรรมของบทเรียนได้ว่าส่วนใดใช้อีมูเลเตอร์ และส่วนใดต้องใช้บอร์ดจริง พร้อมเหตุผล
    en: Split a lesson's activities between the emulator and a real board, with reasons.
  - th: อธิบายงานวิจัยอย่างน้อย 3 ชิ้นที่รองรับวิธีสอนในบทนี้ได้ถูกต้อง
    en: Correctly explain at least three studies behind the methods in this lesson.
develops:
  - {skill: edu.lesson-design, to: 3}
  - {skill: edu.facilitation, to: 3}
context: {audience: educator, platform: psoc-edge-e84, emulator: bento-emulator}
status: alpha
translation: done
slides: slides.md
source_sha256: f9c4579cf1ff54388808e4673718d03aa77a1378adde7eb92ef67015819f8686
---

## Objectives

1. Sequence the activities around one example file through PRIMM
2. Design practice files with fading support, and turn one into a Parsons problem
3. Split work between the emulator and a real board
4. Explain the research behind these methods

## Before you start

- From the previous lesson, what kind of attribution text must go on every slide?
- In your course, at what minute of the first hour do learners see their first piece of working code?

## See it work first

Open Explorer's lessons [First program](../../../explorer/m01-meet-embedded/l03-first-program/README.md) and [Read a sensor](../../../explorer/m02-sense-and-connect/l01-read-a-sensor/README.md) and notice three things.

- The "See it work first" section always says **predict before you run**
- The "Worked example" section is labelled **Move 1, 2, 3**
- The first lesson's practice file has 2 blanks; the next lesson's has 4

None of these three happened by accident. Each one has research behind it.

## Concepts

### 1. PRIMM: Predict, Run, Investigate, Modify, Make

**PRIMM** (Predict, Run, Investigate, Modify, Make) sequences activity around example code into five stages: learners predict the result before running,
run it to compare, investigate what each part does, modify the existing code, and then make something new. Research by Sentance, Waite and Kallia reports results
from using PRIMM in schools, where the group taught with PRIMM outperformed the control group ([Sentance, Waite & Kallia 2019](https://doi.org/10.1080/08993408.2019.1608781)).
This fits the "start from something that works, then take it apart" principle that courses in TESA Open Knowledge use.

### 2. Subgoal-labelled examples

Examples labelled with subgoals, such as "Move 1: pick a light" and "Move 2: start from a known state", help beginners learn programming problem-solving better
([Morrison, Margulieux & Guzdial 2015](https://doi.org/10.1145/2787622.2787733)). Every worked example in the repository therefore always carries Move labels.

### 3. Scaffolding must fade

Start with a full example, then leave more and more blank until the learner writes the whole file themselves in the final task (backward fading)
([Renkl & Atkinson 2003](https://doi.org/10.1207/S15326985EP3801_3); [Renkl, Atkinson & Große 2004](https://doi.org/10.1023/B:TRUC.0000021815.74806.f6)).
Another reason is **expertise reversal**: too much support becomes a burden once the learner has gotten better
([Kalyuga, Ayres, Chandler & Sweller 2003](https://doi.org/10.1207/S15326985EP3801_4)).
The practice used in this repository: within one module, practice files go from a full example → about 2 blanks → about 6 blanks → a blank file in the capstone task.

### 4. Parsons problems

A **Parsons** problem gives learners lines of code to arrange in the right order. Research reports learning outcomes close to writing or fixing the code oneself,
but in less time ([Ericson, Margulieux & Rick 2017](https://doi.org/10.1145/3141880.3141895)). This fits learners who do not yet have a board,
and C-language lessons that have no emulator. In `quiz.yaml`, `type: order` builds a Parsons problem directly.

### 5. Spaced retrieval practice

Practice testing and distributed practice are the two techniques with the highest utility scores in a review of ten learning techniques
([Dunlosky et al. 2013](https://doi.org/10.1177/1529100612453266)). This is why every lesson has 3–5 check-for-understanding questions,
and the "Before you start" section always asks a question that reviews the previous lesson.

### 6. The emulator for concepts, a real board for debugging and measurement

A review of virtual and remote labs against hands-on labs found that most studies report equal or better outcomes
([Brinson 2015](https://doi.org/10.1016/j.compedu.2015.07.003)). But some skills, such as debugging hardware, using measurement instruments,
and dealing with real timing, must happen on a board. The split used in this repository is

| Use the emulator | Use a real board |
|---|---|
| Understanding concepts and the API | Debugging when the board's result differs from the emulator |
| Filling in practice files and iterating quickly | Measuring real values with instruments |
| Designing the screen | Real networking, power, and timing |
| Learners who do not yet have a board turn | End-of-module labs and the capstone |

### 7. Learn in a cohort; do not leave it purely self-paced

As seen in the first lesson of this kit, pure self-paced study has a low completion rate. Mastery learning genuinely helps overall achievement
([Kulik, Kulik & Bangert-Drowns 1990](https://doi.org/10.3102/00346543060002265)), but the same work also notes that fully self-paced programmes tend to have lower completion rates.
So use a per-lesson passing bar (80%) together with cohort learning that has deadlines.

## Worked example

Use Explorer's example [`02_blink.py`](../../../explorer/m01-meet-embedded/l03-first-program/examples/02_blink.py), sequenced through PRIMM.

- **Move 1: Predict (3 minutes)** Have learners read only the values `ROUNDS`, `ON_MS`, `OFF_MS` and write a prediction
- **Move 2: Run (3 minutes)** Run it in the emulator, compare with the prediction
- **Move 3: Investigate (8 minutes)** Ask "what would happen if the last `led.off()` were removed?", "why does it need `str()`?"
- **Move 4: Modify (8 minutes)** Change the rhythm to a short-on, long-off pattern
- **Move 5: Make (15 minutes)** Write a Morse-code blink of their own, on a board if one is available

## Practice

Choose one module in your own course and plan three practice files.

| File | Support | How many blanks | Has a Parsons version? |
|---|---|---|---|
| Lesson 1 | Full example, change one value | 0–1 | |
| Lesson 2 | | About 2 | |
| Lesson 3 | | About 6 | |

Then write one Parsons problem in `quiz.yaml` form (`type: order`) from the lesson 2 file.

## Check your understanding

Answer the questions in [quiz.yaml](quiz.yaml). A score of 80% or more passes.

## Going further

Further reading for instructors: [Carpentries Instructor Training](https://carpentries.github.io/instructor-training/) has a section on live coding and on giving feedback, which works well for lab classes.

## Reflect

Which method in this lesson were you already using without a name for it, and which one could you try as early as next week?
