---
id: aiot-mpy.m03.l07
lang: en
title: {th: 'ออกแบบ HMI: การ์ด ลำดับสายตา สี และงบ widget', en: 'HMI design: cards, visual order, colour and the widget budget'}
summary: {th: ออกแบบแดชบอร์ดสี่การ์ดบนกระดาษก่อนพิมพ์โค้ด ทั้งการจัดกลุ่ม ลำดับสายตา ความหมายของสี พิกัดบนจอ 792x398 และตารางนับ widget ที่ต้องไม่เกินงบ 32 ที่เราตั้งเอง, en: 'Design a four-card dashboard on paper before typing any code, covering grouping, visual hierarchy, colour meaning, coordinates on the 792x398 screen and a widget count that stays within the self-imposed budget of 32.'}
level: L2
time_min: {concept: 30, lab: 20, check: 5}
hardware: {emulator: true, boards: [eva-kit, devkit]}
prerequisites: [aiot-mpy.m03.l06]
objectives:
  - {th: อธิบายหลัก HMI สามข้อที่แผงควบคุมจริงใช้ (การ์ดหนึ่งใบตอบคำถามหนึ่งข้อ ลำดับสายตาสามชั้น และสีเขียว เหลือง แดงที่ถูกจองไว้ให้สถานะ) แล้วชี้ได้ว่าผังตัวอย่างละเมิดข้อไหน, en: 'Explain the three HMI principles real control panels use (one card answers one question, a three-tier visual hierarchy, and green, amber and red reserved for status), and point out which one a sample layout breaks.'}
  - {th: วาดผังสี่การ์ดบนกระดาษพร้อม x y w h ของ Panel ทุกใบ โดยทุกใบผ่านเงื่อนไข x + w ไม่เกิน 792 และ y + h ไม่เกิน 398 และไม่มีการ์ดใดทับกัน, en: 'Draw a four-card layout on paper with x, y, w and h for every Panel, where every card satisfies x + w <= 792 and y + h <= 398 and no two cards overlap.'}
  - {th: ทำตารางงบ widget รายการ์ดที่รวมแล้วไม่เกิน 32 โดยนับ Panel ทุกใบ และไม่นับ series ของ Chart, en: 'Build a per-card widget budget table that totals no more than 32, counting every Panel and not counting Chart series.'}
  - {th: เขียนคำสั่ง ui.Panel ที่ให้ color= เป็นสีพื้น min= เป็นสีขอบ max= เป็นรัศมีมุม และ value= เป็นความหนาขอบ ได้ถูกต้อง และบอกได้ว่าทำไมต้องสร้าง Panel ก่อน Label ที่วางทับ, en: 'Write a ui.Panel call that uses color= for the background, min= for the border colour, max= for the corner radius and value= for the border width, and explain why the Panel must be created before the Labels on top of it.'}
develops: [{skill: gui.hmi, to: 2}, {skill: gui.embedded, to: 2}, {skill: prog.memory, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {repo: 'https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer', path: session-08.html (slides 1–17), ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079}
source_sha256: ff01283e72aecebcf578a791e56d93186fb8c41ecd8db42887e81dda3eb60324
---

# Lesson 3.7 — HMI design: cards, visual order, colour and the widget budget

> Module 3 — Sensor Visualization on HMI · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Design a four-card dashboard on paper before typing any code, covering grouping, visual hierarchy, colour meaning, coordinates on the 792x398 screen and a widget count that stays within the self-imposed budget of 32.

## Objectives

By the end of this lesson you will be able to:

1. Explain the three HMI principles real control panels use (one card answers one question, a three-tier visual hierarchy, and green, amber and red reserved for status), and point out which one a sample layout breaks
2. Draw a four-card layout on paper with x, y, w and h for every Panel, where every card satisfies x + w <= 792 and y + h <= 398 and no two cards overlap
3. Build a per-card widget budget table that totals no more than 32, counting every Panel and not counting Chart series
4. Write a ui.Panel call that uses color= for the background, min= for the border colour, max= for the corner radius and value= for the border width, and explain why the Panel must be created before the Labels on top of it

## Before you start

This lesson's main work happens on paper. Have paper, a pencil, and your learning log ready. Review the three pieces that will share one screen:
the pot with `ui.Arc` and `ui.Seg7`, and CapSense with `ui.Bar` from lessons 2.7–2.9; `sensors.bmi270.motion()`,
which reads six axes in one call, from lessons 3.1–3.3; and `ui.Chart` with multiple series at a 200 ms cadence from lessons 3.4–3.6.

- **Equipment:** an Eva Kit or TESAIoT Dev Kit board with the BENTO MicroPython firmware installed, or the BENTO Emulator in [BENTO IDE](https://ide.tesaiot.dev/)
- **Before this:** [Lesson 3.6 — Hands-on: a three-axis acceleration chart](../l06-accel-chart-lab/README.md)

## See it work first

Open the firmware's **Sensor Dashboard** menu on the board and let it run. One screen, several cards, several sensors,
updating at the same time, no menu to navigate — you know the whole system's state within two seconds. That is an HMI (Human-Machine Interface).
Notice too that the cards depend on the board: the Eva Kit has cards for BMI270, Controls, a motion chart, a compass, a joystick,
and no knob card, while the Dev Kit adds DPS368, SHT40 and radar cards, because the firmware assembles cards to match the chips the board actually has.

## Concepts

Lessons 3.7–3.9 have almost nothing new to learn — the difficulty is that every piece must work at once on one screen. A real control panel is not
designed to look nice; it is designed so that **a tired, rushed person reads it correctly the first time**. The first principle is grouping: values that come from
the same source or are used to decide the same thing belong inside the same frame. One card answers one question — "how is it moving",
"which way is it facing", "is anyone touching it", "what is the knob set to". If you cannot say what question a card answers,
that card should not exist yet.

The second principle is a three-tier visual hierarchy. The first tier is the main value, which must be readable from two or three metres away
(large, bright on a dark background). The second tier is detail — a chart, a bar — read on approaching. The third tier is the card's name, unit, labels,
read only when actively looking for it. In `ui` we have only two tools for this: `value=` on a Label (font size 14/16/20/24/28) and `color=`.
Put 28 on everything and everything is equally prominent, which means nothing is prominent at all. The third principle is that colour has meaning: green is normal,
amber or yellow is watch, red means act now. Never use red for something normal, or the day something real happens, nobody will notice.
The remaining colours distinguish data sources — for example, the IMU card's border is purple `COL_IMU`, and its heading is purple too. Pick real colour numbers from
our own file's top, never invent one on the spot.

Update speed is also a design decision. A number that changes every 20 ms is too fast for anyone to read — all they see is a flickering blur. On the machine side,
a loop that runs too fast sends work to CM55 faster than it can draw, the queue fills, and frames drop silently — no error, just a screen that "feels laggy".
Remember: a heavy dashboard uses 200 ms; a light page with just a few widgets uses 50 ms minimum.

`ui` has no grid or flex layout like the web. Every widget must state its own coordinates. Our usable area is 792 wide, 398 tall, and every card must pass
**x + w ≤ 792** and **y + h ≤ 398**. Overlapping or going past the edge raises no error — it just draws over itself; a wrong number stays silent until we
see it with our own eyes. A card's frame is `ui.Panel`, which reuses familiar kwarg names but with unlike-anyone-else's meanings: `color` is the background,
`min` is the **border colour**, `max` is the **corner radius**, and `value` is the **border width**, for example
`ui.Panel(x=24, y=100, w=368, h=136, color=BG_CARD, min=COL_IMU, max=12, value=2)` (24 + 368 = 392,
100 + 136 = 236, passing both). Always create the Panel first — whatever is created afterward sits on top; swap the order and the card would hide the text under it.

Finally, the budget. The firmware accepts 64 widgets per screen (`UI_MAX_WIDGETS`, identical on both boards); the 65th does not appear and gives
no warning at all, because Python code lives on CM33 while widgets are drawn by LVGL on CM55, and every widget takes one slot in a fixed-size table
reserved at compile time. Reserving a known size in advance beats flexibility that breaks at runtime. This set of lessons sets its own budget
of 32, to leave room for lessons 4.1–5.3 to build on this same screen later. The table in the slides reserves 23 of 32 (Panel counts every card,
so four cards already cost 4 before showing anything at all; three calls to `add_series()` are still just one Chart). Anyone adding more
must come back and edit this table first.

## Worked example

The slides for this lesson also refer to a file that lives in another lesson:

- [m03-sensor-hmi/l09-dashboard-lab/solution/s08_dashboard.py](../l09-dashboard-lab/solution/s08_dashboard.py) — the 4-card Mini-HMI dashboard, on the Eva Kit / Dev Kit

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automatic marking.

1. A team makes the compass card's border bright red because they like the colour, even though the compass works normally. Which explanation is correct? *(choose one · objective 1)*
   - A) Red is reserved for "act now"; using it for something normal means nobody will notice the day something real goes wrong
   - B) No problem — colour is a matter of team taste
   - C) ui.Panel cannot accept red; the card would not display
   - D) Red makes CM55 draw slower, so a darker colour should be used instead

   <details><summary>Solution</summary>

   **A** — On a real control panel, green, amber and red carry meanings the whole industry reads the same way; red means stop or fix it right now. Used on something normal, that colour loses its meaning exactly when it is needed. The remaining colours should distinguish data sources instead.

   </details>

2. Our usable screen is 792 wide, 398 tall. Which of these cards breaks the coordinate condition? *(choose one · objective 2)*
   - A) ui.Panel(x=408, y=100, w=400, h=136, ...)
   - B) ui.Panel(x=24, y=100, w=368, h=136, ...)
   - C) ui.Panel(x=24, y=252, w=320, h=136, ...)
   - D) ui.Panel(x=360, y=252, w=408, h=136, ...)

   <details><summary>Solution</summary>

   **A** — 408 + 400 = 808, over 792. The others give 392, 344 and 768, and y + h never exceeds 388. A card past the edge raises no error — the screen simply draws over itself or cuts it off, so you must add up the numbers on paper first.

   </details>

3. The IMU card has one Panel, a title Label, a Chart where add_series() adds two more lines for all three axes, and one Label for the three-axis value. How many widgets does this card cost? *(choose one · objective 3)*
   - A) 4
   - B) 6
   - C) 3
   - D) 5

   <details><summary>Solution</summary>

   **A** — A Chart's series are not widgets; calling add_series() any number of times is still one Chart. But Panel counts every card, giving Panel + title + Chart + value Label = 4.

   </details>

4. Which statements about the 64-widget ceiling and this lesson's budget of 32 are correct? Choose every correct one. *(choose all that apply · objective 3)*
   - A) The 65th widget does not appear on screen, and there is no warning message at all
   - B) The ceiling comes from a fixed-size table on the CM55 side, reserved at compile time
   - C) 32 is a budget this set of lessons sets for itself, to leave room for lessons 4.1–5.3 to build on
   - D) The Dev Kit can hold more than the Eva Kit, because it has more sensors
   - E) If the budget is exceeded, the firmware expands the table for you at runtime

   <details><summary>Solution</summary>

   **A, B, C** — UI_MAX_WIDGETS is identical on both boards, because they share the same ipc_ui code. The table is reserved at a fixed size so no memory request is needed while drawing the screen; anything over it just disappears silently. 32 is a discipline we impose on ourselves.

   </details>

5. You need a card with background BG_CARD, border colour COL_IMU, 12 px rounded corners and a 2 px border. Which call is correct? *(choose one · objective 4)*
   - A) ui.Panel(x=24, y=100, w=368, h=136, color=BG_CARD, min=COL_IMU, max=12, value=2)
   - B) ui.Panel(x=24, y=100, w=368, h=136, color=COL_IMU, min=BG_CARD, max=2, value=12)
   - C) ui.Panel(x=24, y=100, w=368, h=136, color=BG_CARD, min=0, max=100, value=COL_IMU)
   - D) ui.Panel(x=24, y=100, w=368, h=136, color=BG_CARD, min=12, max=COL_IMU, value=2)

   <details><summary>Solution</summary>

   **A** — For a Panel, color is the background, min is the border colour, max is the corner radius, value is the border width — the same names as Slider, but not a minimum/maximum. Never guess from the name, and the Panel must be created before the Labels on top of it, or the card will hide the text.

   </details>

## Lab

**Design on paper** before touching the keyboard. Do every item below in your learning log.

- [ ] Write the one question each of the four cards answers (IMU · compass · CapSense · knob)
- [ ] Draw the four-card layout with x, y, w, h for every Panel; check each one that x + w ≤ 792 and y + h ≤ 398, and leave gaps between cards
- [ ] Reserve space in a header row or status strip for the team name, the round count and the loop time
- [ ] Build a per-card widget budget table, then add it up in view — it must not exceed 32 (counting every Panel, not series)
- [ ] Mark each card's visual hierarchy: which is the main value (large font, white) and which is a label (smaller, muted)
- [ ] Pick a colour for each card's sensor, and note that green, amber and red are reserved for status only
- [ ] Write the `ui.Panel` command for the first card by hand, and check each kwarg against the Panel meaning table

## Going further

Lesson 3.8 turns this paper layout into code, reading every sensor in one loop at a 200 ms cadence, and lesson 3.9 proves it by running continuously for ten minutes. Keep your layout and budget table well.

Next lesson: [Lesson 3.8 — Building the dashboard: four cards in one loop](../l08-dashboard-build/README.md)

## Reflect

- Which of your cards answers its question the least clearly, and if you had to cut one, which would it be?
- If you had to add one red warning lamp, when should it light, and what should it look like when everything is normal?
- When deciding which Label to cut to fit the budget, what criteria did you use?
