# Electronics & Test Instruments for Embedded Developers

Level **L2** · status **pre-alpha (outline, being written)** · 6 modules, 15 lessons · about 20 hours

This course closes the electronics and test-instrument gap. The Embedded Systems Engineering Roadmap marks these skills as required,
and TPQI's Embedded Systems Developer level 4 qualification has a hardware development unit (ICT-CSOS-107B).
Every lesson ties to something measurable on the Eva Kit or TESAIoT Dev Kit: the knob as a voltage divider, the active-low button,
the PWM-dimmed LED and the sensor I2C bus. The emulator cannot help here; this course needs a board and real instruments.

The lesson pages are Thai-first; English lesson pages are pending (`translation: pending`).

## Who it is for

- Students and developers who can program but have never used test instruments
- Anyone who finished Explorer or AIoT in Action and wants to see what really happens on the board
- You need a board, a multimeter, a low-cost sigrok-compatible logic analyzer and, if possible, a lab oscilloscope

## Outcomes

1. Compute voltage, current, resistance and power in basic circuits and design dividers and current-limiting resistors.
2. Explain logic levels, pull-ups and pull-downs, and wire an active-low button correctly.
3. Measure voltage, continuity and current safely with a multimeter.
4. Capture and decode digital signals with a logic analyzer and measure signals with an oscilloscope.
5. Breadboard, solder safely, read schematics, and explain basic PCB and EMC principles.

## Modules and lessons

**Module 1 — Circuits and electronics fundamentals** ([m01-circuits](m01-circuits/README.md))

| Lesson | Topic | Time |
|---|---|---|
| elec.m01.l01 | Voltage, current and resistance | 65 min |
| elec.m01.l02 | Voltage dividers and analog sensors | 65 min |
| elec.m01.l03 | Basic components: resistors, capacitors, diodes and transistors | 65 min |

**Module 2 — Digital logic** ([m02-digital-logic](m02-digital-logic/README.md))

| Lesson | Topic | Time |
|---|---|---|
| elec.m02.l01 | Logic levels and basic gates | 65 min |
| elec.m02.l02 | Pull-ups, pull-downs and buttons | 65 min |

**Module 3 — The multimeter** ([m03-multimeter](m03-multimeter/README.md))

| Lesson | Topic | Time |
|---|---|---|
| elec.m03.l01 | Measuring voltage and continuity | 65 min |
| elec.m03.l02 | Measuring current safely | 65 min |

**Module 4 — Logic and protocol analyzers** ([m04-logic-analyzer](m04-logic-analyzer/README.md))

| Lesson | Topic | Time |
|---|---|---|
| elec.m04.l01 | Capturing a first digital signal | 65 min |
| elec.m04.l02 | Decoding I2C and UART | 65 min |

**Module 5 — The oscilloscope** ([m05-oscilloscope](m05-oscilloscope/README.md))

| Lesson | Topic | Time |
|---|---|---|
| elec.m05.l01 | Oscilloscope basics | 65 min |
| elec.m05.l02 | Measuring PWM | 65 min |

**Module 6 — Breadboarding, soldering, schematics, PCB and EMC basics** ([m06-build-and-read](m06-build-and-read/README.md))

| Lesson | Topic | Time |
|---|---|---|
| elec.m06.l01 | Breadboarding | 65 min |
| elec.m06.l02 | Soldering safely | 65 min |
| elec.m06.l03 | Reading schematics | 65 min |
| elec.m06.l04 | PCB and EMC basics | 65 min |

## Status

This course is an outline (pre-alpha): every lesson has objectives, skills and verified references, but no content, labs or checks yet.
**Safety.** Every lab uses low voltage from the board or a lab supply only. Never measure mains.

## Main references

- [Lessons In Electric Circuits โดย Tony R. Kuphaldt (หนังสือเปิด)](https://www.ibiblio.org/kuphaldt/electricCircuits/)
- [OpenStax University Physics Volume 2 (บทวงจรไฟฟ้ากระแสตรง)](https://openstax.org/details/books/university-physics-volume-2)
- [sigrok PulseView](https://sigrok.org/wiki/PulseView)
- [sigrok protocol decoders](https://sigrok.org/wiki/Protocol_decoders)
- [AIoT in Action: examples/s05/05_adc_counts_to_volts.py (MIT)](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s05/05_adc_counts_to_volts.py)

## Licence

- Content: CC BY 4.0
- New code added to this course: Apache-2.0
- MicroPython examples referenced belong to AIoT in Action (MIT), linked at a pinned commit

## How to cite TESA

When you use, share or adapt this course, credit it as follows:

> "Electronics & Test Instruments for Embedded Developers" from TESA Open Knowledge by the Thai Embedded Systems Association (TESA), https://github.com/tesaiot/tesa-qualification-program, licensed under CC BY 4.0

Add "(adapted)" at the end of the credit, with a short note of what you changed, when you change the material.
Crediting TESA does not mean TESA endorses your work. Details and examples are in [ATTRIBUTION.md](../../ATTRIBUTION.md).
