---
id: aiot-mpy.m01.l01
lang: en
title: {th: 'ทัวร์บอร์ด: เล่นของจริงก่อน', en: 'Board tour: play with the real thing first'}
summary: {th: เล่นเมนูที่มากับบอร์ดให้ครบก่อนเขียนโค้ดบรรทัดแรก แล้วจับคู่ให้ได้ว่าแต่ละเมนูอ่านเซนเซอร์ตัวไหน และหน้าไหนคือที่ที่โค้ดของเราจะไปปรากฏ, en: 'Play with the menus that ship on the board before writing any code, match each menu to the sensors it reads, and find the page where your own code will appear.'}
level: L2
time_min: {concept: 15, lab: 30, check: 5}
hardware: {emulator: true, boards: [eva-kit, devkit]}
prerequisites: []
objectives:
  - {th: 'ระบุเซนเซอร์ที่เมนู Home (แผง Sensor Live), Sensor Dashboard และ Smart Watch ใช้ ได้ถูกต้องอย่างน้อยสามเมนู จากการเอียง หมุน แตะ และหมุนลูกบิดบนบอร์ดจริงหรือ Emulator', en: 'Identify the sensors behind the Home (Sensor Live panel), Sensor Dashboard and Smart Watch menus for at least three menus, by tilting, turning, touching and turning the knob on the board or the Emulator.'}
  - {th: 'บอกได้ว่าเมนู Controls, Audio Player และ TESAIoT Connectivity มีเฉพาะบน Eva Kit และเลือกทางแทนบน Dev Kit ได้', en: 'State that Controls, Audio Player and TESAIoT Connectivity exist only on the Eva Kit, and choose the Dev Kit alternative.'}
  - {th: อธิบายว่าทำไมต้องเปิดหน้า BENTO Playground ค้างไว้ก่อนส่งโค้ดจาก BENTO IDE, en: Explain why the BENTO Playground page must be open before you send code from BENTO IDE.}
develops: [{skill: sys.sensors-actuators, to: 1}, {skill: iot.fundamentals, to: 1}, {skill: gui.embedded, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {repo: 'https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer', path: session-01.html (slides 1–7), ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079}
source_sha256: dbc85f565928b2cb3a6b96e25987cfda75c8f8c1e324d0b4e0a85c094954cc88
---

# Lesson 1.1 — Board tour: play with the real thing first

> Module 1 — Existing UI-based Application · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Play with the menus that ship on the board before you write your first line of code, then match each menu to the sensor it reads, and find the page where your own code will appear.

## Objectives

By the end of this lesson you will be able to:

1. Identify the sensors used by the Home menu (the Sensor Live panel), Sensor Dashboard and Smart Watch correctly for at least three menus, by tilting, turning and touching the board and turning the knob on the real board or the Emulator
2. State that the Controls, Audio Player and TESAIoT Connectivity menus exist only on the Eva Kit, and choose the alternative on the Dev Kit
3. Explain why the BENTO Playground page must be left open before you send code from BENTO IDE

## Before you start

There is no code to write in this lesson. Get a notebook or a file ready as your own **learning log**
(the slides tell you from time to time what to record). If you have no board, open the BENTO Emulator in BENTO IDE and you can follow almost every step.

- **Equipment:** an Eva Kit or TESAIoT Dev Kit board with the BENTO MicroPython firmware installed, or the BENTO Emulator in [BENTO IDE](https://ide.tesaiot.dev/)

## See it work first

Switch the board on and stay on the Home page for now; do not open any menu yet. Tilt the board, turn it, touch the touch pads
and turn the knob, then watch the Sensor Live panel in the top-right corner of the screen. These values are already moving even though there is not a single line of our code yet,
because the firmware reads the sensors all the time.

## Concepts

The board in this course has every part a real AIoT system needs: a motion sensor (IMU), a compass,
touch buttons (CapSense), a knob, a touch screen, a microphone and a WiFi radio. The menus that ship on the board are the "destination"
that we will gradually build ourselves throughout the course. So playing first is not a waste of time: it is seeing the target before you set off.

The tour has three rounds. Round one is the Home page and the Sensor Live panel. Round two is the three menus you must play through fully
(Controls, Sensor Dashboard, Smart Watch). Round three is the menus you need to know exist (Audio Player,
Wi-Fi Setting, BENTO Playground, TESAIoT Connectivity). While you play, ask yourself every time
which sensor the value on the screen comes from.

The two boards use the same code, but their Home pages are not the same: the Dev Kit has no Controls, Audio Player
or TESAIoT Connectivity card. Teams with a Dev Kit will instead see a real light switched on by their own code in lesson 1.3.

The most important page for us is **BENTO Playground**. The result of code sent from BENTO IDE appears on this page.
If it is not left open before you send the code, it will look as if you sent it and nothing happened.

## Worked example

The slides for this lesson also refer to files that live in other lessons:

- [m01-ui-application/l03-inside-the-box/examples/11_lights_and_a_button.py](../l03-inside-the-box/examples/11_lights_and_a_button.py) — real lights and a real button, controlled from one line of Python
- [m01-ui-application/l03-inside-the-box/examples/15_one_number_many_faces.py](../l03-inside-the-box/examples/15_one_number_many_faces.py) — a single number, and ten ways the screen can tell it

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automatic marking.

1. On the Home page you turn the board around on the spot without tilting it. Which row of the Sensor Live panel should change most clearly? *(choose one · objective 1)*
   - A) Comp (compass)
   - B) Touch
   - C) Pot
   - D) No row changes, because no code has been written yet

   <details><summary>Solution</summary>

   **A** — Turning on the spot changes the direction the board faces, so the compass (Comp) changes. These values are already moving without any code of ours, because the firmware reads the sensors all the time.

   </details>

2. Which menus use data from the motion sensor (IMU)? Choose every correct answer. *(choose all that apply · objective 1)*
   - A) Sensor Dashboard (the chart that ripples when you shake the board)
   - B) Smart Watch (the step counter)
   - C) The IMU row of the Sensor Live panel on the Home page
   - D) Wi-Fi Setting

   <details><summary>Solution</summary>

   **A, B, C** — The Sensor Dashboard chart, the Smart Watch step counter and the IMU row of Sensor Live all come from the same acceleration sensor. Wi-Fi Setting uses the radio, not a sensor.

   </details>

3. Your team has a TESAIoT Dev Kit and cannot find the Controls card on the Home page. Which statement is correct? *(choose one · objective 2)*
   - A) The board is broken and needs new firmware
   - B) The Dev Kit has no such card; watch a real light switched on by the example code in lesson 1.3 instead
   - C) You must connect to WiFi before the card appears
   - D) You must insert an SD card first

   <details><summary>Solution</summary>

   **B** — Controls, Audio Player and TESAIoT Connectivity exist only on the Eva Kit. The two boards use the same code, so Dev Kit teams see a real light switched on by their own code instead.

   </details>

4. You press Program to Device in BENTO IDE and the board's screen shows nothing at all. What should you check first? *(choose one · objective 3)*
   - A) Whether the BENTO Playground page is left open on the board
   - B) Switch to the C language
   - C) Reset the board to factory settings
   - D) Connect the board to WiFi

   <details><summary>Solution</summary>

   **A** — The result of code sent from the IDE appears on the BENTO Playground page. If the board is sitting on another page, it will look as if you sent the code and nothing happened.

   </details>

## Lab

**The three-round tour** (about 30 minutes). Do it on the real board or the Emulator and write it down in your learning log.

- [ ] Round 1: on the Home page, tilt, turn, touch, slide a finger along the slider and turn the knob, then note which rows of Sensor Live change
- [ ] Round 2: Controls (Eva Kit): touch the circles and watch the real LEDs · Sensor Dashboard: shake the board and watch the chart · Smart Watch: swipe to change pages
- [ ] Round 3: open Audio Player, Wi-Fi Setting, BENTO Playground and TESAIoT Connectivity (if present) to learn where they are
- [ ] Make a three-column table in your learning log: menu · sensor used · what you see on the screen, with at least five rows

## Going further

Next lesson: [Lesson 1.2 — First lines on screen: the lcd and ui modules](../l02-first-lines-on-screen/README.md)

## Reflect

- Which menu do you think you could use in your own work right away, and what would you still need to add?
- The dashboards of older cars had a real knob for everything. When everything moved onto a single screen, what was lost?
