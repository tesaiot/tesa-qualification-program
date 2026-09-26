---
id: explore.m02.l03
lang: en
title:
  th: ไปต่อทางไหนดี และแบ่งปันอย่างไรให้ถูก
  en: Where to go next, and how to share it right
summary:
  th: เลือกเส้นทางเรียนต่อจากห้าเส้นทางของ TESA Open Knowledge เก็บผลงานลง portfolio และอ้างอิง TESA ให้ถูกเมื่อแบ่งปันหรือดัดแปลงเนื้อหา
  en: Pick a next pathway from the five TESA Open Knowledge pathways, collect your work in a portfolio, and credit TESA correctly when sharing or adapting.
level: L1
time_min: {concept: 10, practise: 10, check: 5}
hardware: {emulator: true, boards: [none]}
prerequisites: [explore.m02.l02]
objectives:
  - th: เลือกเส้นทางเรียนต่อที่ตรงกับเป้าหมายของตัวเองจากห้าเส้นทาง พร้อมให้เหตุผลอย่างน้อย 1 ข้อ
    en: Choose a next pathway that matches your goal from the five pathways and give at least one reason.
  - th: เขียนข้อความอ้างอิง TESA ที่ถูกต้องสำหรับเนื้อหาที่นำไปแบ่งปัน และเติมคำว่า (ดัดแปลง) เมื่อแก้ไขเนื้อหา
    en: Write a correct TESA attribution for shared material, adding "(adapted)" when the material was changed.
  - th: รวบรวมหลักฐานงานจาก Explorer อย่างน้อย 3 ชิ้น (ภาพหน้าจอ ไฟล์โค้ด หรือแผนภาพ) เป็น portfolio
    en: Collect at least three pieces of evidence from Explorer (screenshots, code files or diagrams) into a portfolio.
develops:
  - {skill: soft.self-driven, to: 1}
  - {skill: soft.communication, to: 1}
context: {platform: none, lang: none, audience: public}
status: alpha
translation: done
slides: slides.md
source_sha256: d821b8ad1658dd3d2a4ac4365ad002547ce22ba1534bcfe51de2a2b5ddf00418
---

## Objectives

1. Choose a next pathway that matches your goal, with a reason
2. Credit TESA correctly when sharing or adapting content
3. Collect your Explorer work into a portfolio

## Before you start

- From the previous lesson, why is a public broker on port 1883 unsuitable for real data?
- Of the six lessons so far, which one did you enjoy the most and want to keep going with?

## See it work first

Open the folder or album where you have been keeping screenshots from the previous lessons, and count how many there are.
These are evidence of what you can now do, not just what you have "read about".

## Concepts

### 1. Five pathways: choose by goal, not by difficulty

TESA Open Knowledge organises its courses into five pathways. Full details are in [catalog/tracks.yaml](../../../../catalog/tracks.yaml).

| If you want to... | Pathway | Next step |
|---|---|---|
| Go a little further for fun, or to understand your kids | Explorer | The first module of the AIoT in Action course |
| Make product or investment decisions without writing code | Entrepreneur | The [Edge AI and IoT for Business Decisions](../../../edge-ai-iot-for-business/README.md) course |
| Learn systematically for a project or a job application | Student | AIoT in Action, then continue into C-language firmware |
| Level up skills for the job you already have | Developer | Take the placement quiz, then skip to the right level |
| Teach it at an educational institution | Educator | The [Educator Kit](../../../educator-kit/README.md) course |

No pathway is better than another. Choose by asking "what do I want to be able to do three months from now?"

### 2. Learning alone often does not finish; find a study buddy

Research on open online courses finds that only a small fraction of people who sign up ever finish. What actually helps is structure:
learning in a cohort with other people, having deadlines, and having someone to answer questions. If TESA has a cohort or a camp running, try joining it,
or invite a couple of friends to learn along with you; that helps a lot too.

### 3. You can share it, but you must always credit TESA

Content in TESA Open Knowledge is published under the **CC BY-NC 4.0** licence, which means you may share it, teach with it and adapt it for non-commercial purposes (commercial use needs TESA's permission first),
under one important condition: **you must credit the source** in the wording TESA specifies. The attribution text for this course is

> "Explorer: Meet Embedded Systems" from TESA Open Knowledge by the Thai Embedded Systems Association (TESA), https://github.com/tesaiot/tesa-qualification-program, licensed under CC BY-NC 4.0

Three rules worth remembering

- **If you change the content**, add the word **(adapted)** after the attribution text, and if you can, say briefly what changed, so readers know it is not the original.
- **The example code** in this course is adapted from the AIoT in Action course under the MIT licence; always keep the copyright line at the top of the file.
- **Never claim TESA endorses** your work or course. Crediting the source does not mean TESA endorses or sponsors it.

Details and worked examples of attribution for slides, handouts and posts are in [ATTRIBUTION.md](../../../../ATTRIBUTION.md) at the root of the knowledge base.

### 4. A portfolio is evidence

A portfolio does not need to be fancy. A single folder with screenshots, the code files you edited, and a diagram you drew yourself with a short caption is enough.
If you use GitHub, a public repository works too, but **always check first that no WiFi password or any other password is in the files**.

TESA plans to issue a completion record (TQP T0 Open Knowledge Completion) for people who pass the end-of-lesson checks, counting only lessons with `stable` status,
which this course (status alpha) has not reached yet. See the latest rules and status at [tqp/certification.md](../../../../tqp/certification.md).
T0 confirms completion; it is not a certification of competency.

## Practice

1. Write one sentence: "Three months from now, I want to..." and pick one pathway from the table.
2. Suppose you are going to turn the lesson "First program: draw on the screen and light an LED" into a post to teach a friend, changing the example to blink in Morse code.
   Write the attribution text you would put at the end of the post, correctly (hint: since you changed it, it needs the word "adapted").

## Check your understanding

Answer the questions in [quiz.yaml](quiz.yaml). A score of 80% or more passes, and counts as finishing the Explorer course.

## Lab

Assemble your Explorer portfolio with at least three pieces.

- [ ] The "sense, decide, act" table from the first lesson
- [ ] A screenshot of the blinking-light program, or the tilt warning light
- [ ] The MQTT message-path diagram from the previous lesson

## Going further

Open the course page of the pathway you chose and look at its first lesson. If you chose the student or developer pathway,
you have already written MicroPython for this board, so the early lessons of the next course will feel familiar.

## Reflect

Before starting Explorer, what did you think an embedded system was? How has your answer changed now?
