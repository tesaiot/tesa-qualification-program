# Explorer: Meet Embedded Systems

Level **L1 Aware** · status **alpha** · 6 lessons of 20–30 minutes · about 3 hours in total · **no board required**

A short course for anyone curious about the small computers hidden inside rice cookers, washing machines and wrist watches.
You start by spotting them around you, then write your first lines of MicroPython in the **BENTO Emulator**, which runs in a
web browser: text on a screen, a blinking LED, a sensor reading, and a value that shows up on a web page. If you already have an
Eva Kit or a TESAIoT Dev Kit, the same code runs on the board.

The lessons are written in Thai; English lesson pages are pending (`translation: pending`).

## Who it is for

- Members of the public, parents and school students with no programming background
- Entrepreneurs who want to see the real thing once before making a product decision
- Educators looking for an opening unit on embedded systems

You need a computer or tablet with Chrome or Edge, and an internet connection. The lessons are not designed for phone screens.

## Outcomes

1. Give everyday examples of embedded systems and separate their sensing, deciding and acting parts.
2. Run a MicroPython program in the BENTO Emulator or on a board that shows text on screen and controls an LED.
3. Read a sensor and display its changing value, handling the case where no reading is available yet.
4. Explain how MQTT works and send one value to a web page by following a guided example.
5. Choose a next pathway that fits their goal, and credit TESA correctly when sharing or adapting the material.

## Modules and lessons

**Module 1 — Meet embedded systems and write a first program** ([m01-meet-embedded](m01-meet-embedded/README.md))

| Lesson | Topic | Time |
|---|---|---|
| explore.m01.l01 | Embedded systems all around you | 25 min |
| explore.m01.l02 | Meet the board and the emulator | 25 min |
| explore.m01.l03 | First program: draw on the screen and light an LED | 28 min |

**Module 2 — Sense, connect, and choose what next** ([m02-sense-and-connect](m02-sense-and-connect/README.md))

| Lesson | Topic | Time |
|---|---|---|
| explore.m02.l01 | Read a sensor and watch the value change | 28 min |
| explore.m02.l02 | Connected things: MQTT and a dashboard | 30 min |
| explore.m02.l03 | Where to go next, and how to share it right | 25 min |

## How to learn

Every lesson follows the same shape: see it work first, then read the concept. Every example runs as is; practice files have
blanks that grow in number from lesson to lesson; each lesson ends with a short check in `quiz.yaml` (80% or more to pass).

**Try it without a board.** Every lesson works in the BENTO Emulator inside [BENTO IDE](https://ide.tesaiot.dev/). Use the
emulator to learn concepts and a real board to prove and measure.

## Source of the code

Every code file in this course is a shortened adaptation of an example from AIoT in Action. It uses the BENTO MicroPython API
exactly as the original does, and each file names the original it came from.

> Adapted from AIoT in Action — Embedded Systems for AIoT Developer, © 2026 Assoc. Prof. Wiroon Sriborrirux, Advance Innovation
> Centre (AIC), Burapha University · BENTO & TESAIoT (CC BY 4.0 / MIT)
> https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer (commit a80bbe88)

## Licence

- Content (Markdown and quizzes): CC BY 4.0
- Example code, practice files and solutions: MIT (keep the original copyright lines at the top of each file)

## How to cite TESA

When you use, share or adapt this course, credit it as follows:

> "Explorer: Meet Embedded Systems" from TESA Open Knowledge by the Thai Embedded Systems Association (TESA), https://github.com/tesaiot/tesa-qualification-program, licensed under CC BY 4.0

Add "(adapted)" at the end of the credit, with a short note of what you changed, when you change the material, and keep the AIoT in Action credit above when you reuse the code.
Crediting TESA does not mean TESA endorses your work. Details and examples are in [ATTRIBUTION.md](../../ATTRIBUTION.md).
