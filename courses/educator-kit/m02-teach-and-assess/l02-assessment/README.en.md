---
id: edu.m02.l02
lang: en
title:
  th: ออกแบบการประเมิน
  en: Designing assessment
summary:
  th: แยกสื่อฝึกที่เปิดสาธารณะออกจากงานที่ใช้ให้คะแนน ผูกทุกการประเมินกับเป้าหมายของบทเรียน ใช้ rubric แบบจุดเดียว และรับมือกับเฉลยสาธารณะและเครื่องมือ AI
  en: Separate public practice material from graded work, tie every assessment to a lesson objective, use single-point rubrics, and deal with public solutions and AI tools.
level: L3
time_min: {concept: 20, practise: 25, check: 5}
hardware: {emulator: false, boards: [none]}
prerequisites: [edu.m02.l01]
objectives:
  - th: จำแนกสื่อในคลังได้ว่าชิ้นใดเป็นสื่อฝึกสาธารณะ ชิ้นใดเหมาะเป็นงานให้คะแนน และชิ้นใดต้องขอจาก TESA ถูกอย่างน้อย 4 ใน 5 รายการ
    en: Classify materials as public practice, suitable for grading, or available from TESA on request, with at least 4 of 5 correct.
  - th: เขียน rubric แบบจุดเดียวสำหรับแล็บหนึ่งแล็บ ให้ทุกเป้าหมายของบทเรียนมีเกณฑ์ผ่านที่สังเกตได้
    en: Write a single-point rubric for one lab in which every lesson objective has an observable pass criterion.
  - th: ออกแบบงานให้คะแนนหนึ่งชิ้นที่ยังวัดความสามารถจริงได้ แม้ผู้เรียนเข้าถึงเฉลยสาธารณะและเครื่องมือ AI
    en: Design one graded task that still measures real ability when learners can reach public solutions and AI tools.
develops:
  - {skill: edu.assessment, to: 3}
  - {skill: edu.lesson-design, to: 2}
assesses:
  - {skill: edu.assessment, level: 3, evidence: resources/lab-rubric-template.md}
context: {audience: educator}
status: alpha
translation: done
slides: slides.md
source_sha256: d2348d9d87008620a706071c1179d2ad3eff3f0dd7c372316585a7cb90228821
---

## Objectives

1. Separate public practice material from graded work
2. Write a single-point rubric tied to every objective
3. Design graded work that still measures real ability in an age of open solutions and AI tools

## Before you start

- From the previous lesson, what are the two techniques with high utility scores in Dunlosky and colleagues' review?
- In your course right now, can learners see the solutions to practice exercises? How do you feel about that?

## See it work first

Open the file [quiz.yaml for the First program lesson](../../../explorer/m01-meet-embedded/l03-first-program/quiz.yaml); every item has an `objective` field pointing back to a lesson objective.
Then open [solution/blink_count.py](../../../explorer/m01-meet-embedded/l03-first-program/solution/blink_count.py), which is open for everyone to see.
This repository deliberately keeps its practice exercises and solutions open, because they are learning material, not an exam.

## Concepts

### 1. Three groups of assessment material

| Group | Example | Who can access it |
|---|---|---|
| **Public practice material** | Checks for understanding (`quiz.yaml`), practice files and solutions, labs, sample rubrics | Everyone, in this repository, used for learning, not for a graded decision |
| **Course graded work** | Multiple lab variants for random assignment, detailed grading criteria, capstone brief with criteria | TESA provides these to instructors on request; not published publicly. Contact contact@tesa.or.th or https://www.tesa.or.th/contact |
| **TQP exam item bank** | Real exam questions, per-candidate parameters, secret test vectors | Nobody outside the certifying body, including instructors. See [tqp/certification.md](../../../../tqp/certification.md) |

Important: **do not use the checks for understanding in this repository as graded exams**, because the answers are already open. Use them as practice and as the per-lesson pass bar (80%); that is enough.

### 2. Every assessment ties to an objective

Following constructive alignment from the crosswalk lesson, every objective must have a matching measurement, and the measurement must measure what the objective actually says.
If an objective uses the verb "blink the LED", the measurement must watch the LED blink, not ask for the definition of GPIO.

### 3. Single-point rubrics

A single-point rubric writes only the pass criterion for each objective, and lets the assessor write evidence of where the work falls short or exceeds it.
It is easy to write, easy to read, and works even when groups do the lab differently. The template is at [resources/lab-rubric-template.md](resources/lab-rubric-template.md).

### 4. When solutions are open and AI tools exist

Fill-in-the-blank practice with a public solution can be copied by anyone, and AI tools can write short code like this in a few seconds. Assessment that still measures real ability tends to have these traits.

- **Done on a board in front of the assessor**, with parameters that differ per group, such as a randomly assigned number of cycles, rhythm, or threshold
- **Explained and fixed on the spot**, asking the learner to change one condition and fix it immediately; someone who understands can do it, someone who copied gets stuck
- **Assessing the process**, the prediction before running, a debugging log, and a record of what was tried and did not work
- **Finding a fault**, giving code with a deliberately planted bug for the learner to find and explain

Policy on AI tools belongs to each institution. Tell learners clearly from the start how much they may use, and require them to disclose when they do.

## Worked example

Graded work for the lesson "Read a sensor and watch the value change" that holds up against a public solution.

- **Move 1** Each group draws a threshold `LIMIT` and an extra condition by lot, for example "the light must blink when tilted, not stay on"
- **Move 2** Done on a board in the classroom within 30 minutes; submit the file and a short clip
- **Move 3** The assessor asks the learner to change the threshold on the spot, and to explain why the code catches `OSError`
- **Move 4** Grade with a single-point rubric that has a row for every lesson objective

## Practice

1. Copy [resources/lab-rubric-template.md](resources/lab-rubric-template.md) and write a rubric for one lab in your own course
2. Design one graded task that uses at least two of the traits from Concept 4

## Check your understanding

Answer the questions in [quiz.yaml](quiz.yaml). A score of 80% or more passes.

## Going further

If you need the graded-work set TESA prepares for a course, contact TESA and state your institution, course, and the TESA course you are using.
TESA will not send TQP exam content to anyone, and per fairness rules, an instructor never examines their own learners in the TQP exam.

## Reflect

Which piece of graded work in your course right now could an AI tool complete entirely for a learner? How would you change it without adding too much marking burden?
