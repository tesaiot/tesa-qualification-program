---
id: edu.m01.l02
lang: en
title:
  th: ตารางเทียบผลลัพธ์การเรียนรู้ (Curriculum Crosswalk)
  en: The curriculum crosswalk
summary:
  th: เทียบบทเรียนแต่ละบทกับผลลัพธ์การเรียนรู้ของรายวิชา ด้าน K/S/E/C ตามมาตรฐานคุณวุฒิ 2565 การประเมิน ชั่วโมง หน่วยสมรรถนะ TPQI และคุณลักษณะบัณฑิต Washington Accord สำหรับ TABEE
  en: Map each lesson to a course learning outcome, the 2565 (2022) Thai qualification-standard domains K/S/E/C, assessment, hours, TPQI units and Washington Accord attributes for TABEE.
level: L3
time_min: {concept: 20, practise: 30, check: 5}
hardware: {emulator: false, boards: [none]}
prerequisites: [edu.m01.l01]
objectives:
  - th: เขียนผลลัพธ์การเรียนรู้ระดับรายวิชา (CLO) ในรูปกริยาวัดผลได้ + เงื่อนไข + เกณฑ์ ได้อย่างน้อย 3 ข้อ และระบุระดับ Bloom ของแต่ละข้อ
    en: Write at least three course learning outcomes as measurable verb + condition + criterion, naming each one's Bloom level.
  - th: จัดผลลัพธ์แต่ละข้อลงด้าน ความรู้ ทักษะ จริยธรรม หรือลักษณะบุคคล ตามประกาศมาตรฐานคุณวุฒิระดับอุดมศึกษา พ.ศ. 2565 ได้ถูกต้อง
    en: Assign each outcome to the Knowledge, Skills, Ethics or Character domain of the 2022 higher-education qualification standard.
  - th: เติมตารางเทียบรายบทเรียนอย่างน้อย 3 แถว ให้ครบทุกคอลัมน์ รวมหน่วย TPQI และ WA ในแถวที่เกี่ยวข้อง
    en: Complete at least three crosswalk rows in every column, including TPQI units and WA attributes where they apply.
develops:
  - {skill: edu.lesson-design, to: 3}
  - {skill: edu.assessment, to: 2}
assesses:
  - {skill: edu.lesson-design, level: 3, evidence: resources/crosswalk-template.md}
context: {audience: educator, frameworks: [TQF-2565, TPQI, IEA-GAPC-2021]}
status: alpha
translation: done
slides: slides.md
source_sha256: a5560a6a71d88d2e7cd388decd7ffd7e69aedebc30244af8af1b28ab7de68f8e
---

## Objectives

1. Write measurable CLOs, with a Bloom level
2. Assign CLOs to the K/S/E/C domains of the 2565 (2022) qualification standard
3. Complete a lesson crosswalk table in every column

## Before you start

- From the previous lesson, which adoption model did you choose, and which lessons will you use?
- What verbs does your course's current learning outcomes use: "understand", "know", or measurable verbs?

## See it work first

Open the lesson page [First program: draw on the screen and light an LED](../../../explorer/m01-meet-embedded/l03-first-program/README.md) and look at the file's front matter.
You will see `objectives` written as measurable verbs, `develops` naming a skill id and level, `time_min` stating the time, and `quiz.yaml` with questions tied to every objective.
Almost all of this can move straight into your crosswalk table. Your job is to connect it to your course documents and the standard frameworks.

## Concepts

### 1. Write the outcomes first, then design the assessment and activities

The **constructive alignment** principle keeps outcomes, assessment and learning activities all pointing the same way
([Biggs 1996](https://doi.org/10.1007/BF00138871)), using **revised Bloom's taxonomy** to choose measurable verbs
([Krathwohl 2002](https://doi.org/10.1207/s15430421tip4104_2)).

| Not measurable | Measurable (verb + condition + criterion) | Bloom |
|---|---|---|
| Understand GPIO | Blink an LED for a given number of cycles with `gpio.led().on()/off()` on a board or emulator, always ending in the off state | Apply |
| Know about MQTT | Explain the roles of broker, topic, publish and subscribe with a diagram, with all four terms correct | Understand |
| Know about security | Compare the risk of a public broker on port 1883 with MQTTs, and choose the option that fits given data, with a reason | Analyse / Evaluate |

### 2. Four domains under the 2022 qualification standard

The Notification of the Higher Education Standard Committee on the Details of Learning Outcomes under the Higher Education Qualification Standard B.E. 2565
(Royal Gazette, Volume 139, Special Issue 212 Ngor, dated 9 September 2022, in force from 27 September 2022)
requires learning outcomes to cover at least four domains: **Knowledge, Skills, Ethics and Character**
([the notice from the Office of the Permanent Secretary, Ministry of Higher Education, Science, Research and Innovation](https://www.ops.go.th/en/role/edu-standard/item/6940-2022-07-22-02-54-49)).

Most embedded-systems lessons mainly reinforce the K and S domains, while E and C come from activities such as
crediting sources correctly (see the next lesson), never putting a password in published work, teamwork in labs, and a portfolio that is honest about what was actually done.

### 3. Two external frameworks people often ask about

- **TPQI** The professional qualification "Embedded Systems Developer, Level 4" has two competency units: ICT-CSOS-107B (embedded systems hardware development)
  and ICT-FYNH-108B (embedded systems software development) ([TPQI-Net](https://tpqi-net.tpqi.go.th/qualifications/standard/book?id=81&cer_level_id=2865)).
  Include these units only in lessons that genuinely relate to them; L1–L2 lessons usually do not yet meet the bar of a competency unit but form its foundation.
- **TABEE** The Council of Engineers' accreditation of engineering programmes uses the graduate-attribute criteria of the Washington Accord
  (the Council of Engineers Thailand is a provisional signatory of the Washington Accord, per the [IEA list](https://www.internationalengineeringalliance.org/accords/washington-accord#list-of-signatories)), set out in the IEA Graduate Attributes and Professional Competencies, 2021 edition
  ([IEA GAPC 2021](https://www.internationalengineeringalliance.org/assets/Uploads/IEA-Graduate-Attributes-and-Professional-Competencies-2021.1-Sept-2021.pdf)),
  with 11 items, WA1–WA11, listed at the end of the template.

TESA's skill map uses levels L1–L5, whose numbers match the professional qualification levels. See [tqp/levels.md](../../../../tqp/levels.md) for details.

## Worked example

Three example rows (using lessons that genuinely exist in the repository)

| Lesson | CLO + Bloom verb | K/S/E/C | Assessment | Hours | TPQI unit | WA | skill id |
|---|---|---|---|---|---|---|---|
| `explore.m01.l03` | CLO1 Blink an LED for a given number of cycles, ending in the off state (Apply) | S | `quiz.yaml` + practice file `practice/blink_count.py` | 0.15 / 0.25 / 0.1 | Foundation of ICT-FYNH-108B | WA5 | `mcu.gpio` |
| `explore.m02.l02` | CLO2 Explain the roles of broker, topic, publish, subscribe with a diagram (Understand) | K | A diagram in the portfolio + `quiz.yaml` | 0.2 / 0.2 / 0.1 | | WA1 | `proto.mqtt`, `iot.fundamentals` |
| `explore.m02.l03` | CLO3 Correctly credit the source of adapted material under its licence (Apply) | E | The attribution text in submitted work | 0.15 / 0.15 / 0.1 | | WA7 | `soft.communication` |

- **Move 1** Copy `objectives` and `develops` from the lesson page
- **Move 2** Write the course CLO that lesson serves; several lessons may map to one CLO
- **Move 3** Choose the most prominent K/S/E/C domain; you do not need to fill in every domain on every row
- **Move 4** Add TPQI units and WA attributes only where you can genuinely justify the connection; if it takes a long explanation, it probably does not belong

## Practice

Copy [resources/crosswalk-template.md](resources/crosswalk-template.md) and fill in at least three rows for your own course,
using the lessons you chose in the previous lesson.

## Check your understanding

Answer the questions in [quiz.yaml](quiz.yaml). A score of 80% or more passes.

## Going further

If your institution is preparing for a TABEE review, this table can serve as supporting evidence, but whether the evidence is sufficient is the reviewer's judgement to make,
and the course-specification document format each institution uses may differ; check with your institution's academic affairs office.

## Reflect

Which CLO in your course has no lesson or assessment behind it at all yet? What should fill that gap?
