---
id: explore.m01.l01
lang: en
title:
  th: ระบบสมองกลฝังตัวซ่อนอยู่รอบตัวเรา
  en: Embedded systems all around you
summary:
  th: มองหาคอมพิวเตอร์ตัวเล็กที่ซ่อนอยู่ในของใช้ประจำวัน แล้วแยกให้ออกว่าส่วนไหนรับรู้ ส่วนไหนตัดสินใจ และส่วนไหนลงมือทำ
  en: Find the small computers hidden in everyday objects and tell apart the parts that sense, decide and act.
level: L1
time_min: {concept: 12, practise: 8, check: 5}
hardware: {emulator: true, boards: [none]}
prerequisites: []
objectives:
  - th: ระบุส่วนรับรู้ ส่วนตัดสินใจ และส่วนสั่งงาน ของอุปกรณ์ในบ้านได้อย่างน้อย 3 ชิ้น
    en: Identify the sensing, deciding and acting parts of at least three household devices.
  - th: อธิบายด้วยคำพูดของตัวเองว่าไมโครคอนโทรลเลอร์ต่างจากคอมพิวเตอร์ทั่วไปอย่างไร อย่างน้อย 2 ประเด็น
    en: Explain in your own words at least two ways a microcontroller differs from a general-purpose computer.
  - th: จำแนกได้ว่าอุปกรณ์ใดมีระบบสมองกลฝังตัว จากรายการที่กำหนดให้ ถูกอย่างน้อย 4 ใน 5 ข้อ
    en: Classify which listed devices contain an embedded system, with at least 4 of 5 correct.
develops:
  - {skill: hw.architecture, to: 1}
  - {skill: sys.sensors-actuators, to: 1}
context: {platform: none, lang: none, audience: public}
status: alpha
translation: done
slides: slides.md
source_sha256: 9b4e1c7f0a931e613eef625de180737c714ee4ccc9afccf973c9daffd42d02a5
---

## Objectives

By the end of this lesson you will be able to

1. Identify the sensing, deciding and acting parts of at least three household devices
2. Explain at least two ways a microcontroller differs from a general-purpose computer
3. Classify which devices contain an embedded system

This lesson needs no board and nothing to install. All you need are your eyes and one sheet of paper.

## Before you start

Try answering these two questions in your head first. Don't worry about getting them wrong.

- How many things in your home "know" what time it is right now?
- How does a rice cooker know that the rice is cooked?

The answers to these two questions are what this whole lesson is about.

## See it work first

Walk around your home or office for a couple of minutes and note down the things that have buttons, lights, a screen, or can sound an alarm, for example
a washing machine, a microwave, an air-conditioner remote, a wrist watch, a lift, traffic lights, a newer refrigerator, a blood-pressure monitor.

Almost everything on this list has a small computer hidden inside it. This computer has no keyboard and no mouse,
and most people never know it is there. That is an **embedded system**.

## Concepts

### 1. Sense, decide, act

Almost every embedded system works by repeating the same three steps over and over.

| Step | In English | Example in a digital rice cooker (the kind with a display and mode buttons) |
|---|---|---|
| Sense | sense (through a **sensor**) | The temperature sensor at the bottom of the pot |
| Decide | decide (with a **microcontroller**) | "It is hotter than a certain point, so the water is gone and the rice is cooked" |
| Act | act (through an **actuator**) | Cut power to the heating element, switch to keep-warm mode, turn on the status light |

A traditional rice cooker with a single lever also knows when the rice is cooked, but it uses a heat-operated cut-off (a thermostat) and has no computer inside.
So two things that do the same job may be an embedded system in one case and not in the other.

Try these three columns on a washing machine. The water-level sensor is the sensing part, the wash programme is the deciding part,
and the motor and the water valves are the acting parts. Once you have seen it this way, you will see it in everything.

### 2. A microcontroller is not a shrunken computer

A desktop computer is designed to do everything: browse the web, write documents, play games. A **microcontroller** is designed to do one job,
do it well, do it on time and use little power. There are at least three clear differences.

- **A dedicated job** One program runs from power-on to power-off. Nobody comes along and installs more apps.
- **On time** An airbag must inflate within a set time; even slightly late is useless. Work like this is called **real-time** work.
- **Low power and small** Many run for a year on a single battery, and the whole system sits on one chip (the processor, memory and the pins to connect devices are all on the same chip).

### 3. So what is not one?

Things that make no decision at all, such as an ordinary light switch that only connects or breaks a circuit, or a torch that lights up when you press it, do not count as embedded systems,
even though electricity runs through them. If there is no part that "thinks", it is not one.

## Practice

Take a sheet of paper and draw a table with the columns below, then fill in at least three rows from the things you noted in "See it work first".

| Device | What it senses (sensor) | What it decides | What it drives (actuator) |
|---|---|---|---|
| Example: air conditioner | Room temperature | "The room is still warmer than the setting" | Compressor, fan |
| | | | |
| | | | |
| | | | |

If you cannot fill in a cell, ask "how does it know?" and "what does it do next?". These two questions usually lead you to the answer.

## Check your understanding

Answer the questions in [quiz.yaml](quiz.yaml). A score of 80% or more passes this lesson.

## Going further

Think about this: if the temperature sensor in a rice cooker failed and reported "cold" all the time, what would happen?
Questions like this are what embedded engineers think about every day. A good system must notice when its own sensor is lying.

In the next lesson, [Meet the board and the emulator](../l02-board-and-emulator/README.md), we will see a real microcontroller
and try controlling it through a web browser, with no board needed.

## Reflect

Which device in your home surprised you most by having a computer inside? And if you could redesign it, what else would you want it to sense?
