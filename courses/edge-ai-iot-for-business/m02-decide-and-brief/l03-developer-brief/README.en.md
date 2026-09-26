---
id: biz.m02.l03
lang: en
title:
  th: "เขียนโจทย์ให้นักพัฒนา: Decision Canvas หนึ่งหน้า"
  en: "Writing a brief for developers: the one-page decision canvas"
summary:
  th: รวบรวมทุกการตัดสินใจจากห้าบทก่อนเป็น decision canvas หนึ่งหน้าที่ส่งให้ทีมพัฒนาหรือผู้รับจ้างได้ และรู้วิธีแบ่งปันแม่แบบพร้อมอ้างอิง TESA
  en: Gather every decision from the five earlier lessons into a one-page decision canvas for a development team or contractor, and share the template with a TESA credit.
level: L1
time_min: {concept: 8, practise: 17, check: 5}
hardware: {emulator: false, boards: [none]}
prerequisites: [biz.m02.l02]
objectives:
  - th: เติม decision canvas ของโครงการตัวเองให้ครบ 15 ช่อง โดยช่องที่ยังไม่รู้เขียนว่าต้องถามใคร
    en: Complete all 15 fields of the decision canvas for your own project, writing who to ask in fields you cannot answer yet.
  - th: แยกโจทย์ที่ดีออกจากโจทย์ที่คลุมเครือได้ และแก้โจทย์คลุมเครือให้วัดผลได้
    en: Tell a good brief from a vague one and rewrite a vague brief so it can be measured.
  - th: เขียนข้อความอ้างอิง TESA ที่ถูกต้องเมื่อแบ่งปันหรือดัดแปลงแม่แบบ
    en: Write a correct TESA attribution when sharing or adapting the template.
develops:
  - {skill: biz.product-decision, to: 2}
  - {skill: soft.communication, to: 2}
  - {skill: biz.risk-compliance, to: 1}
assesses:
  - {skill: biz.product-decision, level: 2, evidence: resources/decision-canvas.md}
context: {audience: entrepreneur, lang: none, code: none, deliverable: decision canvas}
status: alpha
translation: done
slides: slides.md
source_sha256: bbd92273389fcad6a0b1fd7c6c1e1e4266ee3c9154a28e5a5232765521a6091d
---

## Objectives

1. Complete your own project's decision canvas
2. Rewrite a vague brief so it can be measured
3. Share the template with a correct TESA credit

## Before you start

- From the previous lesson, what things must be settled with a partner before signing?
- If a developer sat in front of you for ten minutes, how would you describe your project to them?

## See it work first

Compare two briefs sent to the same development contractor.

**Brief A** "I want a smart AI system to monitor the shop, easy to use, not expensive, get it done as fast as possible."

**Brief B** "Measure the temperature in 12 fridges across three branches. If it stays over the threshold for more than 15 minutes, text the shift manager.
Allow no more than 2 false alarms per branch per month. Must keep working even if the internet drops. Must not collect images or customer data.
No mobile app needed in the first round. Source code and documentation must be handed over at the end of the job."

Quotes for Brief A can differ by ten times between two contractors, because each interprets "smart" differently.
Brief B can be compared on price and on scope, and at handover you can check whether it was really done.

## Concepts

### 1. A good brief can be checked at handover

Every sentence in a brief should be able to answer "at handover, how will we check that this was done?" Words like smart, easy to use, modern, and as fast as possible cannot be checked.
Turn them into numbers or conditions, such as "no more than 2 false alarms per month" or "the manager can set a new threshold themselves within 1 minute".

### 2. State what you will not do, too

A good scope states both what will be done and what **will not** be done in this round. This prevents scope creep and makes prices comparable.

### 3. A one-page decision canvas

The template is at [resources/decision-canvas.md](resources/decision-canvas.md). It has 15 fields, each drawn from one lesson in this course.

| Fields | From lesson |
|---|---|
| 1–4 The problem, the three-part brief, the pre-AI ladder, metrics | biz.m01.l01 |
| 5–7 Architecture, the site, data | biz.m01.l02 |
| 8–9 Cost and time | biz.m01.l03 |
| 10–11 Risk, rules and standards | biz.m02.l01 |
| 12–13 The chosen option and what must be handed back | biz.m02.l02 |
| 14–15 Scope and the decision-maker | This lesson |

### 4. You can share the template, but you must credit TESA

This template and the whole course are published under CC BY 4.0. You may use it inside your company, hand it to clients, or use it in consulting work, including commercially.
The condition is that you credit the source, like this

> "Edge AI & IoT for Product Decisions" from TESA Open Knowledge by the Thai Embedded Systems Association (TESA), https://github.com/tesaiot/tesa-qualification-program, licensed under CC BY 4.0

If you edit the template, for example adding your company's own field, add **(adapted)** after the attribution text and say briefly what changed.
Crediting the source does not mean TESA endorses your project or service; never write it in a way that implies that.
Details and examples are in [ATTRIBUTION.md](../../../../ATTRIBUTION.md).

## Practice

1. Rewrite **Brief A** above into a brief that can be checked at handover. Use your own shop or a hypothetical one.
2. Copy [resources/decision-canvas.md](resources/decision-canvas.md) and fill in all 15 fields for your own project, using what you built in the five earlier lessons.

## Check your understanding

Answer the questions in [quiz.yaml](quiz.yaml). A score of 80% or more passes, and counts as finishing this course.

## Lab

Take your completed decision canvas to at least one developer or contractor and ask them to point out the three least clear fields.
Fix those fields, and keep both the before and after versions as evidence of your learning.

## Going further

- If your team will build it yourselves, have the team look at the developer pathway in [catalog/tracks.yaml](../../../../catalog/tracks.yaml)
- If you must decide on the enclosure and industrial design, see the product design course in the entrepreneur pathway
- TESA has training courses under the TESA Qualification Program (TQP) and a member network that can help you go further

## Reflect

Now that the canvas is complete, do you still want to use AI in this project? Has your answer changed from the first day of the course, and why?
