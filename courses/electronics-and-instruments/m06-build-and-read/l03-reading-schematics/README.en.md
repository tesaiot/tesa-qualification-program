---
id: elec.m06.l03
lang: en
title: {th: อ่านแผนผังวงจร, en: Reading schematics}
summary: {th: อ่านสัญลักษณ์ ชื่อสัญญาณ และบล็อกของแผนผังวงจร แล้วตามสัญญาณจากขาชิปไปถึงชิ้นส่วน, en: 'Read symbols, net names and blocks, and trace a signal from a chip pin to a component.'}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m06.l02]
objectives:
- {th: ระบุสัญลักษณ์ของชิ้นส่วนพื้นฐานและชื่อสัญญาณบนแผนผังวงจรได้, en: Identify basic component symbols and net names on a schematic.}
- {th: ตามสัญญาณหนึ่งเส้นจากขาของไมโครคอนโทรลเลอร์ไปถึงหลอด LED หรือปุ่มบนแผนผังของบอร์ดได้, en: Trace one signal from a microcontroller pin to an LED or button on a board schematic.}
develops:
- {skill: hwdev.design-basics, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: alpha
translation: done
slides: slides.md
source_sha256: bc191441536e489416492b1afd21194157fbde331e322db7af066e0888476af3
---

## Objectives

By the end of this lesson you will:

1. Identify basic component symbols and net names on a schematic
2. Trace one signal from a microcontroller pin to an LED or a button on a board's schematic

## Before you start

- The schematic for the board you are using. A chip vendor's dev kit usually has a schematic downloadable from that kit's product page. If you cannot find one, ask your instructor or the board's maintainer.
  Without a real schematic at all, every concept and practice exercise here can still be done with this page's example schematic; the lab can only be done in part.
- A TESAIoT Dev Kit that can run [QWA309 Potentiometer Monitor](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_pot_monitor&q=prac_qwa309_pot_monitor) and [QWA309 Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test)
- A multimeter, and a logic analyzer

## See it work first

Two public documents about the TESAIoT Dev Kit disagree about the very same knobs.

- The Potentiometer Monitor example's README and its code label them **VR1 = P15.5** and **VR2 = P15.4**
- The SDK's README for the QWA309 base board's overlay states, in its board-notes section, "PCBA silkscreen swaps VR1↔VR2; schematic is authoritative (VR1=P15.4)"
  and another note that the SPI's CS pin is P9.0, while the "9.2" silkscreen label is wrong, because P9.2 is MOSI

Who is right? This is not answered by choosing whichever document looks more trustworthy — it is answered by reading the schematic and measuring.
The key observation is that both documents **agree on the chip's pin names** (P15.4 through P15.7), and disagree only on **the names people assigned** (VR1, VR2).
By the end of this lesson, you will be able to settle a question like this yourself, on your own board.

## Concepts

### 1. Symbols, reference designators, and values

<figure>
<svg viewBox="0 0 400 160" width="400" role="img" aria-label="Basic schematic symbols" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<polyline points="10,30 20,30 22.5,24 27.5,36 32.5,24 37.5,36 42.5,24 47.5,36 50,30 60,30"/>
<text x="35" y="60" text-anchor="middle" fill="currentColor" stroke="none">R (US)</text>
<path d="M80 30H90"/><rect x="90" y="24" width="30" height="12" rx="3"/><path d="M120 30H130"/>
<text x="105" y="60" text-anchor="middle" fill="currentColor" stroke="none">R (IEC)</text>
<path d="M150 30H166M166 20V40M172 20V40M172 30H188"/>
<text x="169" y="60" text-anchor="middle" fill="currentColor" stroke="none">C</text>
<path d="M205 30H221M221 20V40M227 20V40M227 30H243"/><text x="214" y="18" font-size="11" fill="currentColor" stroke="none">+</text>
<text x="224" y="60" text-anchor="middle" fill="currentColor" stroke="none">C polar</text>
<path d="M262 30H274M274 22V38L286 30Z M286 22V38M286 30H298"/>
<text x="280" y="60" text-anchor="middle" fill="currentColor" stroke="none">diode</text>
<path d="M318 30H330M330 22V38L342 30Z M342 22V38M342 30H354M334 18l6 -8m-4 0h4v4M341 18l6 -8m-4 0h4v4"/>
<text x="336" y="60" text-anchor="middle" fill="currentColor" stroke="none">LED</text>
<path d="M20 110H34M34 98V122M34 105L50 94M34 115L50 126M44 124l6 2l-2 -6"/>
<text x="36" y="144" text-anchor="middle" fill="currentColor" stroke="none">NPN</text>
<path d="M85 110H97M97 98V122M103 98V106M103 107V113M103 114V122M103 102H115V92M103 118H115V128M103 110H115V118M106 110l4 -3m-4 3l4 3"/>
<text x="102" y="144" text-anchor="middle" fill="currentColor" stroke="none">N-MOSFET</text>
<path d="M160 106V114M150 114H170M154 118H166M158 122H162"/>
<text x="160" y="144" text-anchor="middle" fill="currentColor" stroke="none">GND</text>
<path d="M205 106H225M215 106V114"/><text x="215" y="101" text-anchor="middle" fill="currentColor" stroke="none">3V3</text>
<path d="M215 114V122"/>
<text x="215" y="144" text-anchor="middle" fill="currentColor" stroke="none">power net</text>
<path d="M255 110H268"/><circle cx="270" cy="110" r="2.5"/><circle cx="296" cy="110" r="2.5"/><path d="M298 110H311M272 108L295 98"/>
<text x="283" y="144" text-anchor="middle" fill="currentColor" stroke="none">SW</text>
<path d="M330 110H345"/><path d="M345 102H385L392 110L385 118H345Z"/>
<text x="366" y="114" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">SCL</text>
<text x="362" y="144" text-anchor="middle" fill="currentColor" stroke="none">net label</text>
</svg>
<figcaption>Common symbols: a resistor (the American style is a zig-zag, the IEC style is a box), a capacitor, a polarised capacitor, a diode, an LED, an NPN transistor, an N-channel MOSFET, ground, a power net's name, a switch, and a net label.</figcaption>
</figure>

There are two common resistor styles: zig-zag (popular in America and Japan) and box (the IEC standard, popular in Europe). Both mean the same thing.

**Reference designators.** A letter states the type, and a number states its sequence, used consistently across the schematic, the board's silkscreen, and the bill of materials (BOM).

| Letter | Type | Letter | Type |
|---|---|---|---|
| R | Resistor | U | Chip (IC) |
| C | Capacitor | J, P, CN | Connector |
| L | Inductor | SW | Switch, button |
| D | Diode, LED | TP | Test point |
| Q | Transistor, MOSFET | Y, X | Crystal |
| FB | Ferrite bead | F | Fuse |

**Writing values without a decimal point.** Schematics often use a letter in place of the point, because a tiny dot is easy to lose when printed or copied.

```text
4k7 = 4.7 kΩ    2R2 = 2.2 Ω    1M0 = 1.0 MΩ    100n = 100 nF    4p7 = 4.7 pF    1u0 = 1.0 µF
```

Codes printed on a chip resistor: the first two digits are the number, and the last digit is how many zeros follow. "103" = 10 × 10³ = 10 kΩ; "472" = 4.7 kΩ.
The four-digit style uses the first three digits as the number: "4701" = 470 × 10¹ = 4.7 kΩ. Leaded ceramic capacitors use the same scheme in pF: "104" = 10 × 10⁴ pF = 100 nF.

### 2. Wires, net names, and multiple sheets

A **net** is a group of points that are all electrically connected. A schematic can show what shares a net in several ways.

- **Wires drawn connected.** Two wires meeting in a T shape with a **junction dot** are connected. Two wires crossing in an X shape **with no dot** are not connected.
- **Net labels.** Two points carrying the same label are the same net, even with no wire drawn between them at all — used to avoid drawing wires across the whole page.
- **Power and ground symbols.** Every "3V3" symbol anywhere on the schematic is the same net; likewise for every ground symbol.
- **Multiple sheets.** A real board's schematic usually spans several sheets. The first sheet is often a block diagram; net labels or off-sheet connectors carry a signal to another sheet.
  A hierarchical schematic uses sub-blocks that have their own input and output pins.

**Meaningful signal names.** A good name tells you immediately what the signal is, which voltage domain it belongs to, and at what level it operates.
The TESAIoT Dev Kit's header test program prints signal names in this style on screen, for example:

```text
P13.3_GPIO_PWM5+_3V3     chip pin P13.3 | used as GPIO or PWM5's positive terminal | 3.3 V domain
P15.2_ADC_2_PWM3+_3V3    pin P15.2 | used as ADC channel 2 or PWM3's positive terminal | 3.3 V domain
```

**Active-low signals** usually carry one of several markers, such as an overbar over the name, starting with n or /, or ending in _N or #.
For example, RESET_N, /CS, nWP, BTN_N all mean "active when 0."

### 3. Tracing a signal from a chip pin to a component, and when the documentation disagrees with the board

<figure>
<svg viewBox="0 0 400 275" width="400" role="img" aria-label="An example schematic using net labels to connect two sheets" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<rect x="20" y="30" width="90" height="130" rx="3"/>
<text x="65" y="50" text-anchor="middle" font-weight="bold" fill="currentColor" stroke="none">MCU</text>
<text x="106" y="84" text-anchor="end" font-size="11" fill="currentColor" stroke="none">IO1</text>
<text x="106" y="134" text-anchor="end" font-size="11" fill="currentColor" stroke="none">IO2</text>
<path d="M110 80H140"/>
<polyline points="140,80 150,80 152.5,74 157.5,86 162.5,74 167.5,86 172.5,74 177.5,86 180,80 190,80"/>
<text x="165" y="68" text-anchor="middle" fill="currentColor" stroke="none">R12 1k</text>
<path d="M190 80H220"/>
<path d="M220 72H250L262 80L250 88H220Z"/>
<text x="240" y="84" text-anchor="middle" font-size="10" fill="currentColor" stroke="none">LED1</text>
<text x="310" y="84" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">→ sheet 2</text>
<path d="M110 130H220"/>
<path d="M220 122H270L278 130L270 138H220Z"/>
<text x="247" y="134" text-anchor="middle" font-size="10" fill="currentColor" stroke="none">BTN_N</text>
<text x="320" y="134" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">→ sheet 2</text>
<path d="M20 190H380" stroke-dasharray="4 3"/>
<text x="20" y="208" font-size="11" fill="currentColor" stroke="none">sheet 2</text>
<path d="M30 230H60L68 238L60 246H30Z"/>
<text x="48" y="242" text-anchor="middle" font-size="10" fill="currentColor" stroke="none">LED1</text>
<path d="M68 238H100M100 230V246L112 238Z M112 230V246M112 238H140"/>
<path d="M100 226l6 -8m-4 0h4v4M107 226l6 -8m-4 0h4v4"/>
<text x="106" y="262" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">D5</text>
<path d="M140 238V246M130 246H150M134 250H146M138 254H142"/>
<path d="M180 230H230L238 238L230 246H180Z"/>
<text x="208" y="242" text-anchor="middle" font-size="10" fill="currentColor" stroke="none">BTN_N</text>
<path d="M238 238H280"/>
<circle cx="280" cy="238" r="2.5" fill="currentColor"/>
<path d="M280 238V226"/>
<polyline points="280,196 280,196 286,198.5 274,203.5 286,208.5 274,213.5 286,218.5 274,223.5 280,226 280,226"/>
<path d="M270 190H290M280 190V198"/><text x="280" y="185" text-anchor="middle" fill="currentColor" stroke="none">3V3</text>
<text x="292" y="214" font-size="11" fill="currentColor" stroke="none">R40 10k</text>
<path d="M280 238H310"/><circle cx="312" cy="238" r="2.5"/><circle cx="338" cy="238" r="2.5"/><path d="M314 236L336 226M340 238H360V246"/>
<path d="M360 246V254M350 254H370M354 258H366M358 262H362"/>
<text x="325" y="262" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">SW3</text>
</svg>
<figcaption>An example schematic (drawn for practice, not a real board's schematic): on sheet 1, the MCU's pins IO1 and IO2 go out to labels LED1 and BTN_N. Sheet 2 has the same labels — points sharing a name are the same wire, even with no line drawn between them.</figcaption>
</figure>

**Steps for tracing a signal**

1. Find the microcontroller's symbol (often split into several parts by port), then find the pin you care about
2. Follow the wire until you reach a component or a label. If you find a label, search for the same name on every sheet (a PDF reader can search text)
3. For every component you pass, record its reference designator, value, and orientation (e.g. which way an LED's anode points)
4. Keep going until you reach the end, usually a power rail or ground, then summarise it as a sentence, e.g. "pin IO1 drives LED1 active-high through 1 kΩ"
5. Open the datasheet of any unfamiliar component alongside this. A component's pins on a schematic are arranged for the drafter's convenience, not to match their real position on the package.

**When the silkscreen does not match the schematic.** The schematic is the document used to create the board, so it is usually more trustworthy than a label printed on the board itself.
But a schematic is also written by a person, has revisions, and can be wrong. The final answer must come from measurement:
power off, and use continuity mode from a header pin to the component; or power on, run a program that you know drives a specific pin, and watch with a logic analyzer where the signal actually shows up.

The TESAIoT Dev Kit's SDK warns of another case of overlapping names, in the `cm33/io/04_gpio_led_button.c` example:
the code's name `CYBSP_USER_BTN1` points to `CYBSP_SW1`, but the board's silkscreen reads SW2. Neither is wrong — they are names in different systems. What ties every name together is **the chip's pin.**

## Worked example

**Problem:** using the example schematic in section 3, determine how LED1 and button SW3 work, and how the program must set up the pins.

**LED1**

1. Sheet 1: pin IO1 → R12 (1 kΩ) → label LED1
2. Sheet 2: label LED1 → D5 (LED, anode toward the label, cathode toward ground) → GND
3. Conclusion: IO1 = 1 → current flows from IO1 through R12 and D5 to ground; the LED lights — this is **active-high**
4. Current: with V_f = 2.0 V, (3.3 − 2.0) V / 1 kΩ = 1.3 mA
5. Program: set IO1 as a push-pull output (on PSoC, `CY_GPIO_DM_STRONG`), starting at 0 so the LED does not flash on at power-up

**SW3**

1. Sheet 1: pin IO2 → label BTN_N directly, with no resistor in between
2. Sheet 2: label BTN_N → a point where R40 (10 kΩ) goes up to 3V3, and SW3 goes down to ground
3. Conclusion: released, R40 pulls it up to 1; pressed, SW3 connects it to ground, giving 0 — this is **active-low**, matching the name's _N suffix
4. Current while pressed: 3.3 V / 10 kΩ = 0.33 mA
5. Program: an external pull-up already exists, so setting IO2 as a no-pull input is enough (also enabling the internal pull-up would not be wrong, just unnecessary), and write `pressed = !read(IO2)`

## Practice

1. Translate these values: 4k7, 2R2, 100n, 1u0, and the chip resistor codes "103" and "4701," and the ceramic capacitor code "104"
2. Name the component type from its reference designator: U3, Q2, TP5, FB1, J4, Y1
3. Break down the parts of the signal name `P15.2_ADC_2_PWM3+_3V3`, and say whether a 5 V signal can connect to this pin
4. On a schematic, a horizontal and a vertical line cross in an X, with no junction dot. Are these two wires connected? What if it were a T shape with a dot?
5. Which of these signal names are active-low: RESET_N, /CS, nWP, EN, SCL
6. A board's silkscreen labels the SPI's CS pin as "9.2," but the SDK says CS is P9.0 and P9.2 is MOSI. Design an experiment that confirms which pin is really CS, without opening the schematic.

## Solution

1. 4.7 kΩ, 2.2 Ω, 100 nF, 1.0 µF, 10 kΩ, 4.7 kΩ, and 100 nF
2. U3 is a chip, Q2 is a transistor or MOSFET, TP5 is a test point, FB1 is a ferrite bead, J4 is a connector, Y1 is a crystal
3. Chip pin P15.2 | used as ADC channel 2 or PWM3's positive terminal | 3.3 V domain. A 5 V signal cannot connect, because it exceeds the pin's voltage domain (see the lesson [Logic levels](../../m02-digital-logic/l01-logic-levels-and-gates/README.md))
4. An X with no dot is not connected; a T with a dot is connected (a good schematic drafter avoids a dotted X-shaped junction, because a tiny dot can be lost when printed)
5. RESET_N, /CS, and nWP
6. One example: connect two logic analyzer channels to the header pin labelled "9.2" and to the suspected neighbouring pin, run the header test program, and press the SPI ESP32 button.
   Per the example's code, the CS pin (P9.0) starts at 1 and drops to 0 for the whole transfer, while MOSI (P9.2) changes with every data bit on every clock. Whichever pin shows the CS-shaped waveform is the real CS.

## Check your understanding

Answer at least 4 of the 5 questions in [quiz.yaml](quiz.yaml) correctly.

## Lab

**Part A: trace a signal on a real schematic** (if you have your board's schematic)

1. Find the first block-diagram sheet. Record how many sheets the schematic has, and what each one covers.
2. Trace one user LED's signal from the chip pin to ground or the supply rail. Record the reference designator and value of every component along the way, and conclude whether it is active-high or active-low.
   Then compare against the SDK, which states that the board's LED lights when the pin is 1 (`CYBSP_LED_STATE_ON = 1`).
3. Trace one user button's signal. Is there an external pull-up resistor? If not, the program must enable the chip's internal pull-up, matching the SDK setting the button to `CY_GPIO_DM_PULLUP`.
4. Find the microcontroller's decoupling capacitors. Count how many there are and what values they use — keep this for the next lesson.

**Part B: which pin is VR1 on your board** (TESAIoT Dev Kit)

1. Run the Potentiometer Monitor example. Turn the knob the silkscreen labels VR1 all the way in one direction, and see which card on screen moves, and which pin it shows.
2. Repeat for every knob, fill in the table, then conclude how the silkscreen, the example's code, and the SDK's description agree (or disagree) on your board.
3. Write a short, one-paragraph proposal: if you were the documentation's maintainer, how would you resolve this confusion? (Hint: refer to things primarily by the chip's own pin name.)

| Silkscreen label | Pin the on-screen card shows | Name the example's code uses | Per the schematic (if available) |
|---|---|---|---|
| VR1 | | | |
| VR2 | | | |
| VR3 | | | |
| VR4 | | | |

**Part C: read a signal name on the header.** Run the header test program, press ADC In or PWM Out, and record the full signal name printed on screen. Break it down as in Practice question 3.

## Going further

The course's last lesson, [PCB and EMC basics](../l04-pcb-and-emc-basics/README.md), takes us from schematic to real board — how a capacitor's placement and a trace's shape affect noise.

## Reflect

In Part B, which document did you trust before measuring, and did that trust change afterwards? How does this habit apply to other documentation you read every day?

## References

- [Circuit diagram (Wikipedia)](https://en.wikipedia.org/wiki/Circuit_diagram)
- [Lessons In Electric Circuits by Tony R. Kuphaldt (open book)](https://www.ibiblio.org/kuphaldt/electricCircuits/)
- [SDK: the QWA309 base board's overlay README (pins and board notes)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-mpy/bento_libs/claw/kit-tesaiot-pse84-ai/README.md)
- [README of QWA309 Potentiometer Monitor (Developer Hub, commit 372d0d8)](https://github.com/tesaiot/developer-hub/blob/372d0d849578a6a49b634d3ecaab8b5958166921/prac_qwa309_pot_monitor/README.md)
- [SDK: cm33/io/04_gpio_led_button.c (define names versus board silkscreen)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c)
