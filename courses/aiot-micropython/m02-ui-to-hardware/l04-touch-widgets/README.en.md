---
id: aiot-mpy.m02.l04
lang: en
title: {th: จอสัมผัสและ widget ตัวแรก, en: The touch screen and your first widgets}
summary: {th: เข้าใจว่านิ้วที่แตะกระจกเดินทางไปถึงโค้ด Python ผ่านคิวเหตุการณ์ของอีกคอร์ได้อย่างไร แล้วสร้าง widget ตัวแรกให้ถูกตำแหน่ง ถูกขนาดตัวอักษร และจำเบอร์ประจำตัวของมันไว้แยกว่าใครถูกแตะ, en: 'Understand how a finger on the glass reaches your Python code through the other core''s event queue, then build your first widgets at the right place and font size and keep their id numbers so you can tell which one was tapped.'}
level: L2
time_min: {concept: 25, lab: 20, check: 5}
hardware: {emulator: true, boards: [eva-kit, devkit]}
prerequisites: [aiot-mpy.m02.l03]
objectives:
  - {th: อธิบายเส้นทางสี่ทอดจากนิ้วแตะกระจกถึงโค้ด Python (ตัวตรวจจับสัมผัส → CM55 ที่รู้ว่าโดน widget ไหน → คิวเหตุการณ์ → ui.poll() บน CM33) และบอกได้ว่าต่างจากการ polling ปุ่มจริงอย่างไร รวมทั้งเกิดอะไรขึ้นถ้าโค้ดไม่เรียก ui.poll() เลย, en: 'Explain the four-hop path from a finger on the glass to Python (touch detector, CM55 finding the widget, the event queue, ui.poll() on CM33), how it differs from polling a real button, and what happens if the code never calls ui.poll().'}
  - {th: 'สร้าง ui.Label, ui.Button และ ui.Switch หลัง ui.screen() ด้วย x, y, w, h และ color ที่กำหนดเอง บอกได้ว่าเมื่อไรจึงปล่อยให้จอจัดวางเอง (x=-1) และอ่าน value= ของ Label/Button/Dropdown/Textarea ว่าเป็นขนาดฟอนต์ที่รับแค่ 14/16/20/24/28 ไม่ใช่ค่าที่วัดได้', en: 'Create ui.Label, ui.Button and ui.Switch after ui.screen() with your own x, y, w, h and color, say when to let the screen lay things out (x=-1), and read value= on Label/Button/Dropdown/Textarea as a font size limited to 14/16/20/24/28, not a measured value.'}
  - {th: เก็บ .id() ของปุ่มหลายตัวไว้ใน list แล้วแปลงเหตุการณ์ที่บอกมาแค่เบอร์ handle กับชนิด 'clicked' กลับเป็นแถวของปุ่มด้วย .index() ตามห้าขั้นของการสร้าง widget ได้ถูกต้อง, en: 'Keep the .id() of several buttons in a list and turn an event carrying a handle number and type ''clicked'' back into the button''s row with .index(), following the five steps of building a widget.'}
develops: [{skill: gui.embedded, to: 1}, {skill: gui.hmi, to: 1}, {skill: rtos.multicore-ipc, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {repo: 'https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer', path: session-04.html (slides 1–14), ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079}
source_sha256: 4be1c5b6ca7ee1f70860b52db7ba21320206fa5f63b4bc0501d641c1fc7de6ce
---

# Lesson 2.4 — The touch screen and your first widgets

> Module 2 — From Screen to Hardware · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Understand how a finger on the glass reaches your Python code through the other core's event queue, then build your first widgets at the right place and font size, and keep their id numbers so you can tell which one was tapped.

## Objectives

By the end of this lesson you will be able to:

1. Explain the four-hop path from a finger on the glass to Python (touch detector, CM55 finding the widget, the event queue, ui.poll() on CM33), how it differs from polling a real button, and what happens if the code never calls ui.poll()
2. Create ui.Label, ui.Button and ui.Switch after ui.screen() with your own x, y, w, h and color, say when to let the screen lay things out (x=-1), and read value= on Label/Button/Dropdown/Textarea as a font size limited to 14/16/20/24/28, not a measured value
3. Keep the .id() of several buttons in a list and turn an event carrying a handle number and type 'clicked' back into the button's row with .index(), following the five steps of building a widget

## Before you start

Lessons 2.4–2.6 build on the loop from lessons 2.1–2.3 (read → decide → command → wait → loop again); the only change is that the input now comes from a finger on the glass.
Teams who have not yet tried `07_button_to_broker.py` from lesson 2.3 lose nothing — the main content does not depend on it.
Have your learning log ready to note the font sizes you try and the `.id()` numbers you get from the hands-on part at the end of the lesson.

- **Equipment:** an Eva Kit or TESAIoT Dev Kit board with the BENTO MicroPython firmware installed, or the BENTO Emulator in [BENTO IDE](https://ide.tesaiot.dev/)
- **Before this:** [Lesson 2.3 — Hands-on: running lights, a button, and the broker](../l03-led-button-lab/README.md)

## See it work first

On the Eva Kit, open the **Controls** menu you played with back in lesson 1.1, and touch a coloured circle again. Watch for the three things this set of lessons must build for itself:
the button knowing it was touched · the real LED changing state · the text on screen changing to match. Teams with a Dev Kit have no such card,
which is all the more reason to build it yourselves — look instead at the finished picture of the solution in the slides. Behind this ordinary-looking page is an event-handling circuit we are about to write ourselves.

## Concepts

The spell for this set of lessons is: **the screen is not the real thing, the screen reports the real thing, and the two must always agree**.
The reason you need a button on screen when a real button can already command a light is that once a machine ships, someone else uses it and only ever sees the screen.
The board gives Python only one real button to touch, but one machine has more than one command, and a panel that disagrees with the real thing deceives the person operating the machine.
Even so, a real button still has one advantage the screen does not: a finger can find it by feel without looking.

**A button on screen is not a button on the board.** A real button wires straight into a chip pin, which we can "read" ourselves whenever we like. A button on screen is an image the CM55 draws.
The touch screen does not measure pressure at all; it measures **the closeness of a conductor** (a finger increases capacitance at that spot), and the detector lives entirely on the CM55 side
while Python runs on CM33 — a different core. So the CM55 logs the event into a queue and waits for us to "collect what was left for us" with `ui.poll()`.
If we never ask, the queue does not lose the event, but nothing happens either.

**The five steps of a widget** (the same order as LVGL in C): 1 create it, `ui.Button("Red")` · 2 place it at `x, y, w, h`
(or `.pos(x, y)`) · 3 its look: `text`, `color` · 4 remember its handle, `btn.id()` · 5 filter events, `ev['type'] == 'clicked'`.
Steps 1–3 are what you see; steps 4–5 are what responds. Step 4 differs most from C, because C hands a callback for the system to call,
while we keep our own id number to check ourselves in the loop. Always start a new page with `ui.screen()` to clear out the old one. `x, y` is the top-left corner in pixels;
leave out `w, h` and the screen fits the widget to the text. Colours are `0xRRGGBB`, and `x=-1` (the default) lets the screen lay widgets out in the order you created them —
good for quick experiments, but a real control panel must set its own positions, because "where the button is" is part of the design.

**A trap every group falls into:** on Label, Button, Dropdown and Textarea, `value=` is a **font size**, accepting only 14 / 16 / 20 / 24 / 28.
`ui.Label("Temperature", value=24)` therefore means text 24 pixels tall, not 24 degrees. `min`, `max` and `value` that mean their literal name
apply only to Slider, Arc and Bar. To change a Label's text, always use `.text("new text")`.

**A handle is an id card.** What you get back when creating a widget is a handle bound to the real widget on the CM55. An event from `ui.poll()`
does not say "the red button was pressed" — it only gives a number, for example `{'handle': 4, 'type': 'clicked'}`, with no name, no colour, no text.
With several buttons, the cleanest approach is `on_ids = [b.id() for b in btn_on]`, then `on_ids.index(ev['handle'])` gives back the row number.
If you did not keep `.id()`, there is no way at all to tell which one sent the event when it arrives.

## Worked example

The slides for this lesson also refer to files that live in other lessons:

- [m02-ui-to-hardware/l03-led-button-lab/examples/07_button_to_broker.py](../l03-led-button-lab/examples/07_button_to_broker.py) — a button and a light on our desk end up on the broker, for a web page to read
- [m02-ui-to-hardware/l03-led-button-lab/solution/s03_led_button.py](../l03-led-button-lab/solution/s03_led_button.py) — an LED chase over every LED plus a debounced button counter
- [shared/web/mqtt_dashboard.html](../../shared/web/mqtt_dashboard.html) — a class-wide dashboard

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automatic marking.

1. A team creates three buttons and writes a loop that only sleeps, with no ui.poll() at all. The user taps the red button three times. What happens? *(choose one · objective 1)*
   - A) The red LED lights on its own, because the CM55 already knows this button is named red
   - B) The events are logged in the queue on the CM55 side and wait there, but the Python code does nothing at all, because nobody asked
   - C) The program stops with an error, because the queue is full
   - D) CM33 reads the finger position directly from the screen itself, so ui.poll() is not needed

   <details><summary>Solution</summary>

   **B** — The touch detector lives entirely on the CM55 side, while Python runs on CM33. The CM55 logs the event into a queue and waits for us to ask with ui.poll(). If we never ask, the event is not lost, but nothing happens either.

   </details>

2. Which statement correctly explains how the board's touch screen knows a finger has touched it? *(choose one · objective 1)*
   - A) It measures pressure — the harder you press, the more clearly it registers
   - B) There is a tiny mechanical switch under the glass at every point
   - C) It measures the closeness of a conductor — a person's finger approaching the glass increases the capacitance at that spot
   - D) Python code on CM33 polls the screen's pin one point at a time

   <details><summary>Solution</summary>

   **C** — The touch screen does not measure pressure at all; it measures the closeness of a conductor. A person's finger is a conductor, so it changes the capacitance at that point with no mechanical switch needed. This same principle comes back in lessons 2.7–2.9 when reading CapSense.

   </details>

3. What does the line `ui.Label("Temperature", value=24)` mean? *(choose one · objective 2)*
   - A) Display a temperature value of 24 degrees on the label
   - B) The text on the label is 24 pixels tall
   - C) Place the label 24 pixels from the left edge
   - D) The label updates every 24 ms

   <details><summary>Solution</summary>

   **B** — On Label, Button, Dropdown and Textarea, value= is the font size and only accepts 14, 16, 20, 24, 28. A value that means its literal name applies only to Slider, Arc and Bar. To change the text, use .text() instead.

   </details>

4. Which statements about placing widgets on screen are correct? Choose every correct one. *(choose all that apply · objective 2)*
   - A) x=-1 (the default) lets the screen lay widgets out in the order they were created; good for quick experiments, but you cannot control the position
   - B) A real control panel should set its own x, y, because a button's position is part of the design
   - C) If w, h are left out, the screen fits the widget to the text automatically
   - D) x, y are measured from the bottom-right corner of the screen
   - E) You must create a new widget every time you want to change the text on a Label

   <details><summary>Solution</summary>

   **A, B, C** — x, y is the top-left corner in pixels, and text is changed with .text() on the same widget, with no need to recreate it. x=-1 lets the screen lay things out on its own, which does not suit a control panel that must design its layout.

   </details>

5. Suppose `on_ids = [3, 4, 5]` holds the ids for the red, green and blue buttons in that order, and ui.poll() returns `{'handle': 4, 'type': 'clicked'}`. What does `on_ids.index(ev['handle'])` give? *(choose one · objective 3)*
   - A) 4, the button's id number
   - B) 1, the row of the green button
   - C) "green", because the event tells you the button's name
   - D) 2, the row of the blue button

   <details><summary>Solution</summary>

   **B** — The event only gives a number, with no name and no colour. .index() finds where the number 4 sits in the list, which is position 1 (counting from 0) — the row of the green button. Without keeping .id(), there would be no way to tell which one sent the event.

   </details>

## Lab

**Hands-on** (about 20 minutes). Write it in BENTO IDE and send it to a board or the Emulator with BENTO Playground kept open.
There is no event loop yet — lesson 2.5 will make the buttons respond. A widget you create stays on screen until someone calls `ui.screen()` again,
but end your script with `ui.poll()` once, because the CM55 hides the whole set of widgets until the first `ui.poll()` arrives.
If you never call it, the screen stays blank for about 2 seconds before things appear (rule 1 of the `ui` module, in lesson 2.5).

- [ ] Start with `ui.screen()`, followed by `time.sleep_ms(200)`, then create the three lines from the slides (`title`, `btn`, `sw`); check that each one sits exactly at the x, y you commanded
- [ ] Remove `x=` and `y=` from the button, then run it again; note where the button ends up when the screen is left to lay it out on its own
- [ ] Create five Labels with `value=` 14, 16, 20, 24 and 28, and pick the size that reads clearly from standing distance. Try one value outside these five once, and note what happens
- [ ] Change the text of one Label with `.text()` instead of creating a new one
- [ ] Create three buttons — red, green, blue — keep their `.id()` in a list, and `lcd.print` them out. Record the numbers in your learning log, and notice they are pure numbers, with no name or colour

## Going further

Lesson 2.5 puts these stored id numbers to real use: write an event loop that calls `ui.poll()` every round, tell events apart by `handle`, and command `gpio.led()`
so the real LED lights up exactly when the screen reports it.

Next lesson: [Lesson 2.5 — The event loop: touch the screen, light the real LED](../l05-event-loop/README.md)

## Reflect

- What does a car gain and lose by moving every button onto one touch screen? If it were a control panel on factory machinery, which real buttons would you keep?
- If an event only gives a number, and one day you insert a new button into the middle of the list, which part of the code needs the most care?
