---
id: biz.m01.l01
lang: en
title:
  th: Edge AI และ IoT ทำอะไรได้ และทำอะไรไม่ได้
  en: What edge AI and IoT can and cannot do
summary:
  th: แยกโจทย์ธุรกิจที่ IoT และ Edge AI ช่วยได้จริง ออกจากโจทย์ที่ไม่ควรใช้ ผ่านกรณีตัวอย่างจากโรงงาน ฟาร์ม สุขภาพ และค้าปลีก
  en: Separate business problems that IoT and edge AI really help with from those they should not be used for, through factory, farm, health and retail cases.
level: L1
time_min: {concept: 15, practise: 10, check: 5}
hardware: {emulator: false, boards: [none]}
prerequisites: []
objectives:
  - th: จำแนกโจทย์จากกรณีตัวอย่างสี่อุตสาหกรรมได้ว่าเหมาะกับ IoT อย่างเดียว IoT ร่วมกับ Edge AI หรือไม่ควรใช้ทั้งคู่ ถูกอย่างน้อย 3 ใน 4 กรณี
    en: Classify cases from four industries as IoT only, IoT with edge AI, or neither, with at least 3 of 4 correct.
  - th: อธิบายข้อจำกัดหลักของ Edge AI ได้อย่างน้อย 3 ข้อ
    en: Explain at least three key limits of edge AI.
  - th: เขียนโจทย์ธุรกิจของตัวเองในรูป "วัดอะไร ตัดสินใจอะไร แล้วใครทำอะไรต่อ" ได้หนึ่งประโยค
    en: Write your own business problem as one sentence of "what is measured, what is decided, and who acts on it".
develops:
  - {skill: biz.product-decision, to: 1}
  - {skill: iot.fundamentals, to: 1}
  - {skill: ai.edge, to: 1}
context: {audience: entrepreneur, lang: none, code: none}
status: alpha
translation: done
slides: slides.md
source_sha256: 9eef893a7546df4e6c06997d62a1c887ad318184cbd53e081cc38a73f32a0b82
---

## Objectives

1. Classify which problems suit IoT alone, IoT together with edge AI, or neither
2. Explain at least three key limits of edge AI
3. Write your own business problem as a single sentence a technical team can act on

This course needs no code and no board.

## Before you start

Think of one problem in your business that you would "want to know about before it's too late", for example a machine about to fail, stock in a fridge about to spoil,
or customers waiting too long in a queue. Write it down in one line; we will come back to it at the end of the lesson.

## See it work first

This table shows four example cases. Read it and try to guess which rows really "need AI".

| Industry | Problem | What is measured | What is decided | Does it need AI? |
|---|---|---|---|---|
| Factory | A pump motor fails suddenly, stopping the production line | The motor's own vibration | "The vibration pattern differs from normal" — notify a technician before it fails | Usually yes, because "abnormal" is not a single number |
| Farm | Vegetables in a greenhouse wilt from heat and dryness | Temperature, air humidity, soil moisture | "Humidity below the threshold" — trigger misting or watering | Usually no, a simple rule is enough |
| Health | An elderly person lives alone, falls, and nobody knows | Movement in the room, sensed by radar, no camera | "A fall has just happened and the person has not gotten up" — notify a relative | Usually yes, because a fall and sitting down quickly look similar |
| Retail | Stock in a fridge spoils because the door was not shut tight all night | Temperature inside the fridge | "Warmer than the threshold for more than 15 minutes" — text the manager | No, a simple rule is enough |

Two of the four rows need no AI at all. This is the first lesson of this course: **most problems need good measurement and clear rules before they need AI**.

## Concepts

### 1. Two terms that often get mixed up

- **IoT (Internet of Things)** is devices with sensors that measure things on their own and send the data over a network, so we know what is happening without anyone standing there watching.
- **Edge AI** is running an already-trained AI model **on the device itself**, close to the sensor, instead of sending all the raw data up to the cloud for a computer somewhere else to think about it.

New chips built for this job are getting smaller and more capable. For example, the TESAIoT Dev Kit board used in TESA's courses uses the Infineon PSoC™ Edge E84 chip,
which pairs an Arm® Cortex®-M55 processor with the Ethos™-U55 AI accelerator (NPU), and has a motion sensor, a 60 GHz radar, a microphone
and environmental sensors on the board, per the [SDK README](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/README.md).
We are not citing this example to sell you this particular board, but to show that "AI on a small device" already exists for real.

### 2. Three steps before you talk about AI

Ask in this order. Wherever you can answer, stop there.

1. **Can it be measured?** Is there any signal this problem gives off that a sensor can pick up? If there is no signal, no technology can help.
2. **Is a simple rule enough?** If it can be decided with "the value is over a threshold" or "over the threshold for longer than X minutes", IoT with a rule is enough — cheaper, and easier to explain.
3. **Does it need to recognise a pattern?** If "abnormal" is not a single number but a pattern in a signal — such as sound, vibration or posture — that is where edge AI earns its cost.

### 3. What edge AI cannot do, or does not do well

- **It is never 100% correct.** Every model has both false alarms and missed real events. You must design who is responsible when it is wrong, and what each kind of mistake costs.
- **No data, no model.** A model learns from examples; it needs real data from the actual site, both from normal times and from abnormal ones. Collecting that data is often the longest part of the project.
- **It is not install-and-done.** Conditions change, machines change, seasons change. A model that is accurate today may be less accurate next year. You need a plan to maintain and update it.
- **It does not replace fixing the process.** If an alert fires and nobody knows what to do next, no amount of accuracy helps.

### 4. A good problem statement has three parts

A sentence a technical team can act on must answer all three parts: **what is measured**, **what is decided**, and **who acts on it next**. For example

> Measure the temperature in every fridge. If it stays over the threshold for more than 15 minutes, text the shift manager to check the door within 30 minutes.

This sentence does not mention AI at all, and that is not a shortcoming.

## Practice

Go back to the problem you wrote down at the start of the lesson. Rewrite it with all three parts, then walk the three steps and say which step your problem stops at.

| Part | Your problem |
|---|---|
| What is measured | |
| What is decided | |
| Who acts on it next | |
| Stops at step (1 can it be measured / 2 is a rule enough / 3 needs to recognise a pattern) | |

## Check your understanding

Answer the questions in [quiz.yaml](quiz.yaml). A score of 80% or more passes.

## Going further

If you would like to see with your own eyes how a small device "measures then decides", try the [Explorer](../../../explorer/README.md) course's lesson on reading a sensor.
It takes about half an hour in a browser, with no board needed.

## Reflect

If your system raises a false alarm once a week, will staff still trust it? And if it misses a real event once a month, how bad is the damage?
The answers to these two questions tell you how much accuracy you actually need.
