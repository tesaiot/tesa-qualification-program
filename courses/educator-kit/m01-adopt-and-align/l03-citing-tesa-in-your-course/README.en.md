---
id: edu.m01.l03
lang: en
title:
  th: อ้างอิง TESA ในรายวิชาของคุณ
  en: Citing TESA in your university course
summary:
  th: ใส่ข้อความอ้างอิง TESA ให้ครบทุกจุดที่ใช้สื่อ ทั้งเอกสารรายละเอียดรายวิชา สไลด์ เอกสารแจก และหน้า LMS รู้ว่าเมื่อไรต้องเติม (ดัดแปลง) และห้ามอ้างว่ารายวิชาได้รับการรับรองจาก TESA
  en: Put the TESA attribution everywhere the material is used (course specification, slides, handouts, LMS pages), know when to add "(adapted)", and never claim TESA certifies the course.
level: L3
time_min: {concept: 15, practise: 20, check: 5}
hardware: {emulator: false, boards: [none]}
prerequisites: [edu.m01.l02]
objectives:
  - th: เขียนข้อความอ้างอิง TESA ลงเอกสารรายละเอียดรายวิชา (มคอ.3 หรือแบบฟอร์มที่สถาบันใช้) ได้ครบทั้งชื่องาน ผู้สร้าง แหล่งที่มา และสัญญาอนุญาต
    en: Write the TESA attribution into the course specification with title, author, source and licence all present.
  - th: ใส่บรรทัดเครดิตสั้นในสไลด์ทุกหน้าที่นำมาใช้ และข้อความเต็มในเอกสารแจกและหน้า LMS ได้ถูกรูปแบบ
    en: Put the short credit line on every reused slide, and the full attribution on handouts and LMS pages, in the right form.
  - th: ตัดสินได้ว่าเมื่อใดต้องเติม (ดัดแปลง) และเขียนสิ่งที่เปลี่ยนได้สั้น ๆ
    en: Decide when "(adapted)" is required and describe the change briefly.
  - th: แยกการอ้างอิงที่มาออกจากการอ้างการรับรอง และระบุได้ว่าข้อความใดห้ามใช้ในเอกสารรายวิชา
    en: Tell attribution apart from a claim of certification, and identify wording that must not appear in course documents.
develops:
  - {skill: edu.lesson-design, to: 3}
  - {skill: soft.communication, to: 2}
assesses:
  - {skill: edu.lesson-design, level: 3, evidence: resources/syllabus-attribution.md}
context: {audience: educator, licence: CC-BY-NC-4.0}
status: alpha
translation: done
slides: slides.md
source_sha256: d289addb28e2779de5d6c12b850b96220218c2c8316a7276082c5ff5cbb59b33
---

## Objectives

1. Put the full TESA attribution into the course specification
2. Put credit on slides, handouts and LMS pages in the right form
3. Know when "(adapted)" is required
4. Never write anything that suggests TESA certifies the course

## Before you start

- From the previous lesson, which lessons does your crosswalk table use, and which courses are they from?
- In your course right now, where is material borrowed from elsewhere credited?

## See it work first

Open the file [ATTRIBUTION.md](../../../../ATTRIBUTION.md) at the root of the knowledge base and look at "The required wording" and "Worked examples".
Then open the bottom of any course page, for example [Explorer](../../../explorer/README.md); you will see a "Attribution" section with the course name already filled in.
Every course in the repository has this section; you can copy it directly.

## Concepts

### 1. Why attribution is required

Content in TESA Open Knowledge is published under the **CC BY-NC 4.0** licence, which allows non-commercial use only, and TESA gives educational institutions an additional permission.
Your institution may therefore teach with it, adapt it, and use it in its regular courses that charge tuition ([ATTRIBUTION.md](../../../../ATTRIBUTION.md)); other commercial use, such as paid training for outside participants, needs TESA's permission first.
The condition every time is that you credit the source in the manner the owner specifies, and TESA specifies one form of wording, used everywhere.

> "«title»" from TESA Open Knowledge by the Thai Embedded Systems Association (TESA), https://github.com/tesaiot/tesa-qualification-program, licensed under CC BY-NC 4.0

Attribution is also a matter of academic integrity. When learners see their instructor crediting sources correctly, they learn to do the same
(this is why the crosswalk table in the previous lesson placed this under the Ethics domain).

### 2. Where it must appear

| Where | What to put |
|---|---|
| **Course specification** (มคอ.3 or the form your institution uses instead) | The full wording, one entry per course or lesson used, with a note that the course is not certified by TESA or Infineon |
| **Every slide reused or adapted** | The short credit line in the footer, and the full wording on the title or last slide |
| **Handouts and worksheets** | The short credit line on every page, and the full wording with the full URL on the first or last page |
| **LMS pages** | The full wording at the end of the lesson page or on the course's first page |

The short credit line is

```
TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0
```

Ready-to-paste wording for every case is at [resources/syllabus-attribution.md](resources/syllabus-attribution.md).

### 3. When "(adapted)" is required

If you **cut, add, translate, or restructure**, add **(adapted)** after the attribution text, and if you can, say briefly what changed, for example
"(adapted: removed the lab, and changed the example to the course's own board)".
Changing the slide template to your faculty's own, without touching the content, also counts as adapting the format; including it is the safer choice.

If the course you use has its own upstream source (stated at the bottom of the course page), you must also keep that upstream credit, for example a course adapted from AIC's AIoT in Action.

### 4. Attribution is not the same as certification

CC BY-NC 4.0 does not allow implying that the owner certifies or endorses the user's work, and the names TESA, TQP and "Certified by TESA and Infineon" are marks
not covered by the CC licence ([TRADEMARKS.md](../../../../TRADEMARKS.md)). So

- **You may write** "This course uses open material from TESA Open Knowledge", together with the attribution text.
- **You may not write** "TESA-certified course", "TQP exam preparation course", or use the TESA or TQP logo on course documents,
  **unless** that course has been mapped against the TESA Qualification Program through TESA and given written permission.

TQP certification belongs to the individual who passes the exam, not to the course. See the rules at [tqp/certification.md](../../../../tqp/certification.md).

## Worked example

An instructor uses Explorer's first module in the first two weeks of a microcontroller course, converts the slides to the faculty's own template, and drops lesson 3.

- **Move 1: the course document** Place the "adapted" wording from resources under teaching materials:
  `"Explorer: Meet Embedded Systems" from TESA Open Knowledge by the Thai Embedded Systems Association (TESA), https://github.com/tesaiot/tesa-qualification-program, licensed under CC BY-NC 4.0 (adapted: used the first module only, dropped lesson 3, and converted to the faculty's slide template)`
  followed by the upstream AIoT in Action credit from the bottom of the Explorer course page, because the example code comes from there.
- **Move 2: slides** Keep the original footer, add the course code in front of it on the same line, and put the full wording on the last slide.
- **Move 3: LMS** Place the full wording at the end of the page for those two weeks.
- **Move 4: check the wording** Search the whole document set to confirm it contains no phrase like "certified by TESA" or "TQP exam preparation".

## Practice

1. Open [resources/syllabus-attribution.md](resources/syllabus-attribution.md) and fill in the attribution text for your own course in all four places.
2. Write an "(adapted: ...)" note that matches what you actually changed, in no more than one line.

## Check your understanding

Answer the questions in [quiz.yaml](quiz.yaml). A score of 80% or more passes.

## Going further

If your institution would like to map a course against TQP, contact TESA through the channel listed in [ATTRIBUTION.md](../../../../ATTRIBUTION.md),
and do not write any wording about certification until you have received written permission.

## Reflect

If your learners publish their coursework in a public portfolio, how will you teach them to credit both TESA and yourself?
