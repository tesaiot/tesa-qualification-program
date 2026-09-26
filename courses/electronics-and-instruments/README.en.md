# Electronics & Test Instruments for Embedded Developers

Level **L2** · status **alpha** · 6 modules, 15 lessons · about 20 hours

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

## Board examples used in the labs

Most labs use the Developer Hub QWA309 examples as signal sources to measure. They run on the TESAIoT Dev Kit only;
every lab also says what to do on an Eva Kit (usually a short program of your own that makes the same signal on a free pin).

| Example | Used in |
|---|---|
| [QWA309 Potentiometer Monitor](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_pot_monitor&q=prac_qwa309_pot_monitor) | Voltage dividers and the ADC; reading schematics |
| [QWA309 4-Channel ADC Scope](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_adc_scope&q=prac_qwa309_adc_scope) | Voltage dividers and the ADC |
| [QWA309 Push Button Monitor](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_button_monitor&q=prac_qwa309_button_monitor) | Pull-ups, pull-downs and buttons |
| [QWA309 Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) | Logic levels, buttons, logic analyzer, I2C and UART decoding, oscilloscope, PWM, breadboarding |

## What you need

- A TESAIoT Dev Kit (or Eva Kit) and a USB cable
- A digital multimeter with a mA jack, and its manual
- A low-cost logic analyzer that works with PulseView
- An oscilloscope with a 10× probe (a lab bench scope or a USB scope)
- A breadboard, jumper wires, a basic resistor kit, LEDs, a push button, a 100 µF capacitor
- A temperature-controlled soldering iron, a practice board, safety glasses, an ESD wrist strap and fume extraction (module 6)

## Status

This course is alpha: every lesson has concepts with worked numeric examples, a complete worked example, exercises with answers, a lab and check-for-understanding questions.
Lesson pages are in Thai; the English lesson pages are pending. All diagrams are this course's own work (CC BY 4.0). Report a wrong number or step as described in [CONTRIBUTING.en.md](../../CONTRIBUTING.en.md).

**Safety.** Every lab uses low voltage from the board or a lab supply only. Never measure mains.
Each lesson has its own safety notes (current measurement, probe grounding, the iron, flux fume, ESD); read them before each lab.

## Main references

- [Lessons In Electric Circuits โดย Tony R. Kuphaldt (หนังสือเปิด)](https://www.ibiblio.org/kuphaldt/electricCircuits/)
- [OpenStax University Physics Volume 2 (บทวงจรไฟฟ้ากระแสตรง)](https://openstax.org/details/books/university-physics-volume-2)
- [sigrok PulseView](https://sigrok.org/wiki/PulseView)
- [sigrok protocol decoders](https://sigrok.org/wiki/Protocol_decoders)
- [AIoT in Action: examples/s05/05_adc_counts_to_volts.py (MIT)](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s05/05_adc_counts_to_volts.py)
- [TESAIoT Dev Kit SDK: QWA309 base-board capability map (Apache-2.0)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-mpy/bento_libs/claw/kit-tesaiot-pse84-ai/README.md)
- [Developer Hub: TESAIoT Dev Kit practice examples (commit 372d0d8)](https://github.com/tesaiot/developer-hub/tree/372d0d849578a6a49b634d3ecaab8b5958166921)

## Licence

- Content and diagrams: CC BY 4.0
- This course has no code files of its own yet; any added later will be Apache-2.0
- MicroPython examples referenced belong to AIoT in Action (MIT); C examples belong to the Developer Hub and the TESAIoT Dev Kit SDK. All are linked, not copied into this repository

## How to cite TESA

When you use, share or adapt this course, credit it as follows:

> "Electronics & Test Instruments for Embedded Developers" from TESA Open Knowledge by the Thai Embedded Systems Association (TESA), https://github.com/tesaiot/tesa-qualification-program, licensed under CC BY 4.0

Add "(adapted)" at the end of the credit, with a short note of what you changed, when you change the material.
Crediting TESA does not mean TESA endorses your work. Details and examples are in [ATTRIBUTION.md](../../ATTRIBUTION.md).
