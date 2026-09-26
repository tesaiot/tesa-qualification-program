---
id: aiot-mpy.m01.l02
lang: en
title: {th: 'ข้อความแรกขึ้นจอ: โมดูล lcd กับ ui', en: 'First lines on screen: the lcd and ui modules'}
summary: {th: ส่งข้อความแรกขึ้นจอบอร์ดด้วยโมดูล lcd ui และ time แล้วเรียนกติกาที่ทำให้ข้อความหายเงียบ ๆ ก่อนจะประกอบทั้งหมดเป็นจอสถานะหนึ่งใบ, en: 'Put your first text on the board with the lcd, ui and time modules, learn the rules that make text vanish without an error, then combine them into one status screen.'}
level: L2
time_min: {concept: 10, practise: 40, lab: 20, check: 5}
hardware: {emulator: true, boards: [eva-kit, devkit]}
prerequisites: [aiot-mpy.m01.l01]
objectives:
  - {th: 'ส่งข้อความหนึ่งบรรทัดออกสามปลายทาง (print, lcd.print, ui.Label) แล้วหาเจอครบทั้งสามที่ โดยเรียก ui.poll() หลังสร้างหรือแก้ widget ทุกครั้ง', en: 'Send one line of text to three destinations (print, lcd.print, ui.Label) and find all three, calling ui.poll() after every widget you create or change.'}
  - {th: ทำนายได้ว่าข้อความภาษาไทยหนึ่งก้อนจะพอดีกับ lcd.print() หนึ่งครั้ง (127 ไบต์) หรือไม่ โดยนับด้วย len(text.encode()) แล้วแบ่งข้อความที่ยาวเกินก่อนส่ง, en: 'Predict whether a Thai string fits one lcd.print() call (127 bytes) by counting len(text.encode()), and split longer text before sending it.'}
  - {th: อธิบายและใช้โครงของ 08_status_screen.py ได้ คือสร้าง widget ครั้งเดียวนอกลูปแล้วเขียนทับด้วย .text() หรือ .value() และพิมพ์ลงลิ้นชัก Console เฉพาะตอนระดับเปลี่ยน, en: 'Explain and reuse the structure of 08_status_screen.py - create widgets once outside the loop, overwrite them with .text() or .value(), and log to the Console drawer only when the level changes.'}
  - {th: เติม level_name() ใน 09_your_level_rule.py จนหกแถวใน CASES เป็นสีเขียวครบ รวมค่าที่อยู่ตรงเส้น 49 50 79 และ 80, en: 'Complete level_name() in 09_your_level_rule.py until all six CASES rows turn green, including the boundary values 49, 50, 79 and 80.'}
develops: [{skill: gui.embedded, to: 2}, {skill: lang.micropython, to: 2}, {skill: mcu.timers, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {repo: 'https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer', path: session-01.html (slides 8–22), ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079}
source_sha256: 5db9b4b7a75e10119ec66732cafbe6a6d2cb7d95677fbde42b5922f1524c313d
---

# Lesson 1.2 — First lines on screen: the lcd and ui modules

> Module 1 — Existing UI-based Application · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Put your first text on the board's screen with the lcd, ui and time modules, and learn the rules that make text vanish silently, before combining it all into one status screen.

## Objectives

By the end of this lesson you will be able to:

1. Send one line of text to three destinations (print, lcd.print, ui.Label) and find it in all three places, calling ui.poll() every time you create or change a widget
2. Predict whether a chunk of Thai text fits in one lcd.print() call (127 bytes) by counting with len(text.encode()), and split text that is too long before sending it
3. Explain and reuse the structure of 08_status_screen.py: create widgets once outside the loop, overwrite them with .text() or .value(), and print to the Console drawer only when the level changes
4. Complete level_name() in 09_your_level_rule.py until all six rows in CASES are green, including the values right on the lines 49, 50, 79 and 80

## Before you start

Keep your learning log from lesson 1.1 open. On the board's screen, touch the **BENTO Playground** card and leave it open every time before you send code,
then open BENTO IDE on the computer and let it find the board. One board per team is enough, but take turns at the keyboard in every part.

- **Equipment:** an Eva Kit or TESAIoT Dev Kit board with the BENTO MicroPython firmware installed, or the BENTO Emulator in [BENTO IDE](https://ide.tesaiot.dev/)
- **Before this:** [Lesson 1.1 — Board tour: play with the real thing first](../l01-board-tour/README.md)

## See it work first

Send `01_first_line.py` to the board, then **look at the board's screen, not the computer's**. One label appears on the Playground page straight away,
but where did the other lines go? Try to find them before reading on: one line is in the BENTO IDE console on the computer,
and the other two are waiting in the Console drawer, which opens with the green icon button in the bottom-right corner of the Playground page
(a small red dot on the corner of the button means there are messages waiting). A silent screen usually means we are looking in the wrong place, not that the code is broken.

## Concepts

The firmware already does about 70% of the heavy work for us: reading the sensors, drawing every menu, handling IPC between the two cores and running MicroPython.
Our job is the remaining 30%: deciding what data to show, how to show it, and where to send it next.
In this lesson our 30% is still very small, just printing to the screen, but the mechanism behind it is the same in every lesson from here on.

One line of text can go to three places, each different: `print()` goes to the console on the computer · `lcd.print()` goes to the Console drawer on the board ·
`ui.Label` goes straight onto the screen. The one rule to remember: after you create or change `ui.*`, tap `ui.poll()` once,
or the screen will freeze for about two seconds. And `value=` on a `ui.Label` is the font size, not a number to display.
Our drawing area is 792 x 398 pixels; about 100x58 in the bottom-right corner belongs to the Console button, so never place a widget over it.

The screen counts **bytes**, not characters. `lcd.print()` can send 127 bytes per call, and a `ui` label carries 126 bytes both when it is created and when you call `.text()`.
One Thai character takes 3 bytes, so you get about 42 characters. The part that goes over is cut off without any error, and the `\n` at the end of the line disappears too.
The colours in the drawer are the same kind of thing: the five `span` classes (muted info ok warn error) are five levels of importance, not colours to pick as you like,
and a misspelt class name simply comes out in the normal colour, with no error to catch.

A value that changes all the time can be shown in two ways. The drawer way is `lcd.clear()` and then redrawing the whole page (more often than about 5 times a second, the eye sees the screen flicker).
The widget way is to create the widget once outside the loop and overwrite it with `.text()` or `.value()`, which is much cheaper because only the new value crosses between the cores.
Do not create a `ui.Label` with empty text, because the screen fills in the word `Label` by itself. As for time, `sleep_ms()` means sleep for
*at least* this long. The work before the sleep takes its own time, so the loop runs slower than you asked and the delay accumulates. Always measure with `ticks_diff()`, never by subtracting directly.

`08_status_screen.py` has not a single new command. What is new is how the pieces are joined together: the screen answers "how are things now",
the drawer answers "what has happened so far", and it prints to the drawer only when the level changes. This is the file most worth re-reading in the set.

## Worked example

The slides suggest opening the files in this order: `01_first_line.py` → `02_markup_tags.py` → `03_byte_limit.py` → `08_status_screen.py`
→ `09_your_level_rule.py`. Every file ends with a **ตาคุณ** (your turn) block for you to edit and run again. In `03` and `07`, **predict before you run**
and write the number you predicted in your learning log before you press send. Open the remaining files when you meet the matching symptom: text cut off at the end of a line,
open `06_safe_print.py` · a report so long you cannot tell whether it passed, open `04_console_drawer.py` · values flowing down until the screen is full,
open `05_clear_and_refresh.py` · a loop that runs slower than you told it to and drifts more the longer it runs, open `07_ticks_and_beat.py`

| File | What this file teaches |
|---|---|
| [examples/01_first_line.py](examples/01_first_line.py) | The first line on the board's screen |
| [examples/02_markup_tags.py](examples/02_markup_tags.py) | Making the lines that need reading urgently stand out from the others |
| [examples/03_byte_limit.py](examples/03_byte_limit.py) | Text longer than 127 bytes is cut off silently |
| [examples/04_console_drawer.py](examples/04_console_drawer.py) | The Console drawer, and a summary card you can read without opening the drawer |
| [examples/05_clear_and_refresh.py](examples/05_clear_and_refresh.py) | Updating in the same place, as opposed to printing line after line downwards |
| [examples/06_safe_print.py](examples/06_safe_print.py) | A print helper that is never cut off silently |
| [examples/07_ticks_and_beat.py](examples/07_ticks_and_beat.py) | A loop that sleeps the same amount every round does not keep time |
| [examples/08_status_screen.py](examples/08_status_screen.py) | One status screen, with three modules sharing the work |
| [examples/09_your_level_rule.py](examples/09_your_level_rule.py) | This file runs, but still gets every answer wrong; your job is to make it right |

**Screens from the BENTO Emulator** for this lesson's examples (click a file name to open the code)

<div class="tok-screens">
<figure><img src="img/screens/01_first_line.webp" alt="examples/01_first_line.py running in the BENTO Emulator: The first line on the board&#x27;s screen" width="800" height="480" loading="lazy"><figcaption><a href="examples/01_first_line.py"><code>01_first_line.py</code></a> The first line on the board&#x27;s screen</figcaption></figure>
<figure><img src="img/screens/02_markup_tags.webp" alt="examples/02_markup_tags.py running in the BENTO Emulator: Making the lines that need reading urgently stand out from the others" width="800" height="480" loading="lazy"><figcaption><a href="examples/02_markup_tags.py"><code>02_markup_tags.py</code></a> Making the lines that need reading urgently stand out from the others</figcaption></figure>
<figure><img src="img/screens/03_byte_limit.webp" alt="examples/03_byte_limit.py running in the BENTO Emulator: Text longer than 127 bytes is cut off silently" width="800" height="480" loading="lazy"><figcaption><a href="examples/03_byte_limit.py"><code>03_byte_limit.py</code></a> Text longer than 127 bytes is cut off silently</figcaption></figure>
<figure><img src="img/screens/04_console_drawer.webp" alt="examples/04_console_drawer.py running in the BENTO Emulator: The Console drawer, and a summary card you can read without opening the drawer" width="800" height="480" loading="lazy"><figcaption><a href="examples/04_console_drawer.py"><code>04_console_drawer.py</code></a> The Console drawer, and a summary card you can read without opening the drawer</figcaption></figure>
<figure><img src="img/screens/05_clear_and_refresh.webp" alt="examples/05_clear_and_refresh.py running in the BENTO Emulator: Updating in the same place, as opposed to printing line after line downwards" width="800" height="480" loading="lazy"><figcaption><a href="examples/05_clear_and_refresh.py"><code>05_clear_and_refresh.py</code></a> Updating in the same place, as opposed to printing line after line downwards</figcaption></figure>
<figure><img src="img/screens/06_safe_print.webp" alt="examples/06_safe_print.py running in the BENTO Emulator: A print helper that is never cut off silently" width="800" height="480" loading="lazy"><figcaption><a href="examples/06_safe_print.py"><code>06_safe_print.py</code></a> A print helper that is never cut off silently</figcaption></figure>
<figure><img src="img/screens/07_ticks_and_beat.webp" alt="examples/07_ticks_and_beat.py running in the BENTO Emulator: A loop that sleeps the same amount every round does not keep time" width="800" height="480" loading="lazy"><figcaption><a href="examples/07_ticks_and_beat.py"><code>07_ticks_and_beat.py</code></a> A loop that sleeps the same amount every round does not keep time</figcaption></figure>
<figure><img src="img/screens/08_status_screen.webp" alt="examples/08_status_screen.py running in the BENTO Emulator: One status screen, with three modules sharing the work" width="800" height="480" loading="lazy"><figcaption><a href="examples/08_status_screen.py"><code>08_status_screen.py</code></a> One status screen, with three modules sharing the work</figcaption></figure>
<figure><img src="img/screens/09_your_level_rule.webp" alt="examples/09_your_level_rule.py running in the BENTO Emulator: This file runs, but still gets every answer wrong; your job is to make it right" width="800" height="480" loading="lazy"><figcaption><a href="examples/09_your_level_rule.py"><code>09_your_level_rule.py</code></a> This file runs, but still gets every answer wrong; your job is to make it right</figcaption></figure>
</div>

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automatic marking.

1. You create a ui.Label on the Playground page and the screen freezes for about two seconds before the label appears. What is the most likely cause? *(choose one · objective 1)*
   - A) ui.poll() has not been called after creating the widget
   - B) value= is set wrongly, because value= is the number the label displays
   - C) The label must use lcd.print() instead to appear immediately
   - D) The board is not connected to WiFi yet

   <details><summary>Solution</summary>

   **A** — After you create or change ui.*, you must tap ui.poll() once. If you do not, the label still comes, but about two seconds late. value= on a ui.Label is the font size.

   </details>

2. Which statements give the destination of the text correctly? Choose every correct answer. *(choose all that apply · objective 1)*
   - A) print() appears in the BENTO IDE console on the computer, not on the board's screen
   - B) lcd.print() waits in the Console drawer; you must touch the green icon button in the bottom-right corner to see it
   - C) ui.Label appears on the Playground page without pressing anything
   - D) All three commands appear in the same place and differ only in text colour

   <details><summary>Solution</summary>

   **A, B, C** — One line can go to three different places: print() is on the computer, lcd.print() is in the Console drawer and ui.Label is on the screen. So a silent screen usually means we are looking in the wrong place.

   </details>

3. You call lcd.print() once with a Thai text 50 characters long. What happens? *(choose one · objective 2)*
   - A) The text is cut at 127 bytes without any error, and the \n at the end of the line disappears too
   - B) You get an error saying the text is too long
   - C) The screen wraps onto new lines by itself until every character is shown
   - D) It is shown in full, because 50 characters is still below 127

   <details><summary>Solution</summary>

   **A** — One Thai character takes 3 bytes, so 50 characters are 150 bytes, over the ceiling of 127 bytes per call. The excess is cut off silently. Count with len(text.encode()), not len(text).

   </details>

4. How should you write a status screen whose value changes every 200 ms? *(choose one · objective 3)*
   - A) Create the widgets once outside the loop, overwrite them with .text() or .value(), and print to the drawer only when the level changes
   - B) Create a new ui.Label in the loop every round, so you always get the latest value
   - C) lcd.clear() and redraw the whole page every 200 ms
   - D) lcd.print() every round, so the history is as complete as possible

   <details><summary>Solution</summary>

   **A** — A widget created in the loop is a new widget every round, clearing the screen more often than about 5 times a second flickers, and a drawer written every round holds nothing but repeated lines that nobody can read. That is why 08_status_screen.py separates the screen's job from the drawer's job.

   </details>

5. In level_name() you write if v >= 50 return "เริ่มสูง" (getting high) before if v >= 80 return "ต้องรีบดู" (check now). What result does the value 92 give? *(choose one · objective 4)*
   - A) "เริ่มสูง", without any error
   - B) "ต้องรีบดู", because 92 is greater than 80
   - C) SyntaxError, because the conditions overlap
   - D) "ปกติ" (normal)

   <details><summary>Solution</summary>

   **A** — 92 passes the 50 condition first, so it falls into the middle band and never reaches the top one, with no error to catch. Order the ifs from the strictest condition downwards.

   </details>

## Lab

**The ตาคุณ (your turn) blocks you must do.** Record the result of every item in your learning log.

- [ ] `01`: add your team name to all three destinations, then note everywhere you have to look to see all of them
- [ ] `02`: find the line in `REPORT` that has the wrong level and fix it, then add one more line of team news and choose its level
- [ ] `03`: put the members' Thai names into `ITEMS`; first predict how many bytes each is and whether it will be green or red, then run and compare
- [ ] `08`: move `lcd.print()` out of the `if` so it fires every round, then answer which kind of history is more useful in practice
- [ ] `09`: complete `level_name()` until all six rows are green, then add a row to `CASES` that you think your own rule is likely to fail

## Going further

Lesson 1.3 opens the other modules in the box (`gpio` `sensors` `dsp` `mic` `machine`) and has each team complete the practice file
`s01_hello_lcd.py` until the team name appears on screen. The remaining rules of `ui` are in lessons 2.4–2.6, and the simulated values in `08`
are replaced with values from real sensors from lessons 2.7–2.9 onwards.

Next lesson: [Lesson 1.3 — Inside the box: two cores, AIoT and your team's screen](../l03-inside-the-box/README.md)

## Reflect

- What kind of line in your work should make someone walking past get up from their chair, and which class should it carry?
- Which piece of knowledge in this lesson relies on people's discipline every single time, and how could you move it into a function?
- History written every round versus history written only on a change: which one can answer "at which second did the value reach the check-now level"?
