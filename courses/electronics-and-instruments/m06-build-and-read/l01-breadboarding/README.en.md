---
id: elec.m06.l01
lang: en
title: {th: ต่อวงจรบนเบรดบอร์ด, en: Breadboarding}
summary: {th: รู้ว่ารูบนเบรดบอร์ดเชื่อมกันอย่างไร และต่อวงจรตามแผนผังให้ตรวจง่าย, en: Know how breadboard holes connect and build circuits from a schematic that are easy to check.}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m05.l02]
objectives:
- {th: ระบุแถวและรางไฟที่เชื่อมกันบนเบรดบอร์ดได้ถูกต้อง, en: Identify which rows and rails are connected on a breadboard.}
- {th: ต่อวงจรตามแผนผังโดยใช้สีสายตามแบบแผน และตรวจด้วยมัลติมิเตอร์ก่อนจ่ายไฟ, en: Build from a schematic with conventional wire colours and check with a multimeter before powering.}
develops:
- {skill: hwdev.breadboard, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: alpha
translation: done
source_sha256: 35735feec8cdb340e00ba17abca0c48b534065aaf85242ad1e88af45afe6462e
---

## Objectives

By the end of this lesson you will:

1. Correctly identify which rows and power rails are connected on a breadboard
2. Build from a schematic using conventional wire colours, and check it with a multimeter before applying power

## Before you start

- You can already use a multimeter's continuity mode and diode mode (lesson [Measuring voltage and continuity](../../m03-multimeter/l01-voltage-and-continuity/README.md))
- For the lab: a breadboard, several coloured jumper wires (red, black, and at least two other colours), three red LEDs, four 1 kΩ resistors, one 10 kΩ resistor, one push button,
  and a TESAIoT Dev Kit flashed with the [QWA309 Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) example
- If using the Eva Kit, wire the same circuit to spare pins on the board, and write a short program yourself that blinks the LEDs and reads the button

## See it work first

Turn the breadboard over and look at the back. If you can peel off the adhesive backing without damaging it (or look at a manufacturer's diagram), you will see metal strips arranged under the holes —
many short strips in the middle, and a couple of long strips along the top and bottom edges.

Before reading on, guess which pairs of holes connect to each other, then prove it with your multimeter's continuity mode (plug two short jumper wires into the holes you want to test, then touch the meter's leads to the ends of those wires).
If you guess a pair wrong, that is good news — it means you have just avoided that mistake before wiring a real circuit.

## Concepts

### 1. Inside a breadboard

<figure>
<svg viewBox="0 0 420 250" width="420" role="img" aria-label="A breadboard's internal wiring: power rails running lengthwise, and rows of five holes" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<text x="20" y="22" font-weight="bold" fill="currentColor" stroke="none">+</text>
<text x="20" y="38" font-weight="bold" fill="currentColor" stroke="none">−</text>
<path d="M60 18H252" stroke-width="3"/>
<path d="M60 34H252" stroke-width="3" stroke-dasharray="4 3"/>
<text x="40" y="60" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">a</text>
<circle cx="68" cy="56" r="2"/>
<circle cx="84" cy="56" r="2"/>
<circle cx="100" cy="56" r="2"/>
<circle cx="116" cy="56" r="2"/>
<circle cx="132" cy="56" r="2"/>
<circle cx="148" cy="56" r="2"/>
<circle cx="164" cy="56" r="2"/>
<circle cx="180" cy="56" r="2"/>
<circle cx="196" cy="56" r="2"/>
<circle cx="212" cy="56" r="2"/>
<circle cx="228" cy="56" r="2"/>
<circle cx="244" cy="56" r="2"/>
<text x="40" y="76" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">b</text>
<circle cx="68" cy="72" r="2"/>
<circle cx="84" cy="72" r="2"/>
<circle cx="100" cy="72" r="2"/>
<circle cx="116" cy="72" r="2"/>
<circle cx="132" cy="72" r="2"/>
<circle cx="148" cy="72" r="2"/>
<circle cx="164" cy="72" r="2"/>
<circle cx="180" cy="72" r="2"/>
<circle cx="196" cy="72" r="2"/>
<circle cx="212" cy="72" r="2"/>
<circle cx="228" cy="72" r="2"/>
<circle cx="244" cy="72" r="2"/>
<text x="40" y="92" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">c</text>
<circle cx="68" cy="88" r="2"/>
<circle cx="84" cy="88" r="2"/>
<circle cx="100" cy="88" r="2"/>
<circle cx="116" cy="88" r="2"/>
<circle cx="132" cy="88" r="2"/>
<circle cx="148" cy="88" r="2"/>
<circle cx="164" cy="88" r="2"/>
<circle cx="180" cy="88" r="2"/>
<circle cx="196" cy="88" r="2"/>
<circle cx="212" cy="88" r="2"/>
<circle cx="228" cy="88" r="2"/>
<circle cx="244" cy="88" r="2"/>
<text x="40" y="108" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">d</text>
<circle cx="68" cy="104" r="2"/>
<circle cx="84" cy="104" r="2"/>
<circle cx="100" cy="104" r="2"/>
<circle cx="116" cy="104" r="2"/>
<circle cx="132" cy="104" r="2"/>
<circle cx="148" cy="104" r="2"/>
<circle cx="164" cy="104" r="2"/>
<circle cx="180" cy="104" r="2"/>
<circle cx="196" cy="104" r="2"/>
<circle cx="212" cy="104" r="2"/>
<circle cx="228" cy="104" r="2"/>
<circle cx="244" cy="104" r="2"/>
<text x="40" y="124" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">e</text>
<circle cx="68" cy="120" r="2"/>
<circle cx="84" cy="120" r="2"/>
<circle cx="100" cy="120" r="2"/>
<circle cx="116" cy="120" r="2"/>
<circle cx="132" cy="120" r="2"/>
<circle cx="148" cy="120" r="2"/>
<circle cx="164" cy="120" r="2"/>
<circle cx="180" cy="120" r="2"/>
<circle cx="196" cy="120" r="2"/>
<circle cx="212" cy="120" r="2"/>
<circle cx="228" cy="120" r="2"/>
<circle cx="244" cy="120" r="2"/>
<path d="M68 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M84 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M100 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M116 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M132 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M148 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M164 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M180 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M196 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M212 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M228 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M244 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<text x="40" y="164" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">f</text>
<circle cx="68" cy="160" r="2"/>
<circle cx="84" cy="160" r="2"/>
<circle cx="100" cy="160" r="2"/>
<circle cx="116" cy="160" r="2"/>
<circle cx="132" cy="160" r="2"/>
<circle cx="148" cy="160" r="2"/>
<circle cx="164" cy="160" r="2"/>
<circle cx="180" cy="160" r="2"/>
<circle cx="196" cy="160" r="2"/>
<circle cx="212" cy="160" r="2"/>
<circle cx="228" cy="160" r="2"/>
<circle cx="244" cy="160" r="2"/>
<text x="40" y="180" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">g</text>
<circle cx="68" cy="176" r="2"/>
<circle cx="84" cy="176" r="2"/>
<circle cx="100" cy="176" r="2"/>
<circle cx="116" cy="176" r="2"/>
<circle cx="132" cy="176" r="2"/>
<circle cx="148" cy="176" r="2"/>
<circle cx="164" cy="176" r="2"/>
<circle cx="180" cy="176" r="2"/>
<circle cx="196" cy="176" r="2"/>
<circle cx="212" cy="176" r="2"/>
<circle cx="228" cy="176" r="2"/>
<circle cx="244" cy="176" r="2"/>
<text x="40" y="196" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">h</text>
<circle cx="68" cy="192" r="2"/>
<circle cx="84" cy="192" r="2"/>
<circle cx="100" cy="192" r="2"/>
<circle cx="116" cy="192" r="2"/>
<circle cx="132" cy="192" r="2"/>
<circle cx="148" cy="192" r="2"/>
<circle cx="164" cy="192" r="2"/>
<circle cx="180" cy="192" r="2"/>
<circle cx="196" cy="192" r="2"/>
<circle cx="212" cy="192" r="2"/>
<circle cx="228" cy="192" r="2"/>
<circle cx="244" cy="192" r="2"/>
<text x="40" y="212" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">i</text>
<circle cx="68" cy="208" r="2"/>
<circle cx="84" cy="208" r="2"/>
<circle cx="100" cy="208" r="2"/>
<circle cx="116" cy="208" r="2"/>
<circle cx="132" cy="208" r="2"/>
<circle cx="148" cy="208" r="2"/>
<circle cx="164" cy="208" r="2"/>
<circle cx="180" cy="208" r="2"/>
<circle cx="196" cy="208" r="2"/>
<circle cx="212" cy="208" r="2"/>
<circle cx="228" cy="208" r="2"/>
<circle cx="244" cy="208" r="2"/>
<text x="40" y="228" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">j</text>
<circle cx="68" cy="224" r="2"/>
<circle cx="84" cy="224" r="2"/>
<circle cx="100" cy="224" r="2"/>
<circle cx="116" cy="224" r="2"/>
<circle cx="132" cy="224" r="2"/>
<circle cx="148" cy="224" r="2"/>
<circle cx="164" cy="224" r="2"/>
<circle cx="180" cy="224" r="2"/>
<circle cx="196" cy="224" r="2"/>
<circle cx="212" cy="224" r="2"/>
<circle cx="228" cy="224" r="2"/>
<circle cx="244" cy="224" r="2"/>
<path d="M68 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M84 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M100 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M116 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M132 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M148 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M164 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M180 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M196 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M212 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M228 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M244 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M60 140H252" stroke-dasharray="4 3"/>
<text x="260" y="144" fill="currentColor" stroke="none">centre channel</text>
<text x="68" y="48" text-anchor="middle" font-size="10" fill="currentColor" stroke="none">1</text>
<text x="116" y="48" text-anchor="middle" font-size="10" fill="currentColor" stroke="none">4</text>
<text x="164" y="48" text-anchor="middle" font-size="10" fill="currentColor" stroke="none">7</text>
<text x="212" y="48" text-anchor="middle" font-size="10" fill="currentColor" stroke="none">10</text>
<text x="260" y="26" fill="currentColor" stroke="none">power rails (long)</text>
<text x="260" y="84" fill="currentColor" stroke="none">5 holes in a column</text>
<text x="260" y="100" fill="currentColor" stroke="none">= one node</text>
</svg>
<figcaption>The faint thick lines are the metal strips under the holes: the five holes a through e in the same column connect to one point; f through j connect to another. The centre channel keeps the two sides apart. The power rails at the top connect lengthwise (some models break in the middle).</figcaption>
</figure>

- **Groups of five holes.** In the middle of the breadboard, five holes in the same column (a through e) connect to a single point (one node); f through j form another point.
  Different breadboard brands label these "rows" or "columns" differently — remember the rule "five holes in line, not crossing the centre channel," rather than a name.
- **The centre channel** keeps the two sides apart, sized to fit a dual in-line (DIP) chip, so each of its pins lands on a different point.
- **Power rails.** The long strips along the edges, usually marked with a red (+) line and a blue (−) line, used to distribute power and ground.
  **On some long breadboards, the power rails break in the middle** — always check with continuity mode before using any board for the first time.
- The hole spacing is 2.54 mm (0.1 inch), matching a typical header pin.

**The classic mistake** is plugging a resistor's two leads into the same group of five holes — the resistor is shorted out, and the circuit behaves as if it were not there at all.
An LED wired this way will not light either, because there is no voltage across it.

### 2. Wire colour and layout

Wire colour has no electrical effect, but it matters a great deal for checking. The common convention:

| Colour | Used for |
|---|---|
| Red | The positive supply rail (if there are several voltages, use a different colour for each, e.g. red = 5 V, orange = 3.3 V, and label them) |
| Black (or blue) | Ground |
| Other colours | Signals, colour-coded by function, e.g. yellow = a pin driving an LED, green = a pin reading a button |

**Layout habits that make checking easy:**

- Wire the schematic one net at a time. Once a net is wired, mark it off on your printed schematic.
- Keep wires short and flat against the breadboard, never arching over components; trim component leads to a matching length.
- Place components following the schematic's orientation (power at the top, ground at the bottom, signal flowing left to right) — this lets whoever checks it compare quickly against the drawing.
- If a chip is present, add a 100 nF capacitor across the rails right next to each chip's power pin (the reason is in the lesson [Basic components](../../m01-circuits/l03-components/README.md)).

**A breadboard's limits.** The metal strips running parallel to each other have a few pF of capacitance between them, and the contacts have their own resistance and inductance.
The result is that a breadboard does not suit fast signals in the multi-MHz range, high-resistance points, or high current.

```text
5 pF of stray capacitance with a 100 kΩ signal source
f_c = 1 / (2π × R × C) = 1 / (2π × 100 kΩ × 5 pF) ≈ 318 kHz
```

Signals faster than about this get filtered into rounded edges. At 1 MΩ, this frequency drops to about 32 kHz.
Contacts that have seen a lot of use grow loose, a common cause of a circuit that "sometimes works, sometimes doesn't," which is hard to diagnose.

### 3. Check before applying power

Check in this order every time, **while the breadboard is still disconnected from the board or any supply.**

1. **Check by eye.** Go net by net against the schematic. LEDs and capacitors are polarised. No component's two leads should accidentally sit in the same group.
2. **The power rails and ground must never connect.** Continuity between the + rail and the − rail must **not beep.**
3. **Resistance between the rails must make sense.** Calculate in advance what resistance the circuit should show between the rails, then measure and compare.
4. **Test each LED in diode mode.** Touch the red lead to the anode and the black lead to the cathode — you should read roughly V_f, and some LEDs will glow faintly.
5. **Apply power in order:** GND first, then the supply, then signal wires. If your supply can limit current, set the limit low first (e.g. 50 mA), so a mistake burns nothing.

## Worked example

**Problem:** wire three LEDs to pins P13.3, P13.4, P13.5, and an active-low button to pin P13.0, on a TESAIoT Dev Kit,
then test with the header test program's GPIO Out and GPIO In buttons.

**Schematic (written as a net list)**

| Net | Connects to |
|---|---|
| GND | The header's GND pin, the − rail, LED1 through LED3's cathodes, one side of the button |
| 3V3 | The header's 3V3 pin, the + rail, one end of R_pu 10 kΩ |
| LED1 | P13.3 → 1 kΩ → LED1's anode (likewise LED2 at P13.4, LED3 at P13.5) |
| BTN_N | R_pu's other end, the button's other side, and 1 kΩ to P13.0 |

**Wire list**

| From | To | Colour |
|---|---|---|
| The header's GND | The − rail | Black |
| The header's 3V3 | The + rail | Red |
| P13.3, P13.4, P13.5 | Each LED's 1 kΩ resistor | Yellow |
| P13.0 | The 1 kΩ resistor connected to BTN_N | Green |

**Calculate before wiring**

```text
Each LED's current while the pin is 1 (V_f ≈ 1.8 to 2.0 V): (3.3 − 2.0) / 1 kΩ ≈ 1.3 mA to (3.3 − 1.8) / 1 kΩ = 1.5 mA
Resistance between the + rail and the − rail, disconnected from the board:
  Button released → no current path → reads OL (open circuit)
  Button pressed   → through R_pu to ground → reads 10 kΩ
```

**Check:** the + and − rails do not beep, read OL, and read 10 kΩ when the button is pressed. Every LED passes diode mode. Then connect to the board, in order: GND, 3V3, signal wires.

**Test:** press GPIO Out — the three LEDs should light in sequence, one pin at a time, about 0.7 s each. Press GPIO In, then press the button — bit 0 of the mask must change with the button.
The 1 kΩ resistor between BTN_N and P13.0 protects the pin: while GPIO Out drives P13.0 as an output, if someone presses the button, the current will never exceed 3.3 mA.

## Practice

1. On the breadboard in the figure, are holes a12 and e12 connected? What about e12 and f12? What about a12 and a13?
2. A resistor is plugged in with one lead at b15 and the other at d15. What happens?
3. With 5 pF of stray capacitance and a 10 kΩ signal source, at what frequency does filtering start?
4. A breadboard carries both 5 V and 3.3 V. How should you arrange wire colours and labels?
5. Before applying power, you measure 0.4 Ω between the + rail and the − rail. What should you do next?
6. In the worked example, if you forget to add R_pu 10 kΩ, what will the resistance between the rails read while the button is pressed, and will the button still work in GPIO In mode?

## Solution

1. a12 and e12 are connected (the same group of five holes). e12 and f12 are not connected (separated by the centre channel). a12 and a13 are not connected (different groups).
2. Both leads land in the same group, so the resistor is shorted out — it has no effect on the circuit.
3. f_c = 1 / (2π × 10 kΩ × 5 pF) ≈ 3.18 MHz.
4. Use a different colour for each voltage, e.g. red = 5 V, orange = 3.3 V; keep them on separate rails, and label the rails too — never make someone else guess.
5. Never apply power. A value close to 0 Ω is a short circuit. Find the wire or component lead connecting the + and − rails, removing components one at a time and measuring again.
6. It reads OL both pressed and released, because there is no path from the + rail to ground. The button can still pull the pin down to 0 while pressed, but while released the pin floats (GPIO In sets it as no-pull), so the reading is unreliable.

## Check your understanding

Answer at least 4 of the 5 questions in [quiz.yaml](quiz.yaml) correctly.

## Lab

1. **Survey your own breadboard.** Use continuity mode to check whether the power rails run the full length or break in the middle, and spot-check a couple of groups of five holes. Record the results.
2. **Draw the schematic** of the worked example on paper using proper symbols (see the symbols in the lesson [Reading a schematic](../l03-reading-schematics/README.md) if you are not familiar yet). Print it or photograph it, and keep it beside you.
3. **Wire one net at a time**, following the wire list. Mark off each net on the schematic as soon as it is wired.
4. **Check before applying power.** Complete all five steps in Concepts section 3. Record the resistance between the rails, both released and pressed.
5. **Apply power.** Connect GND, then 3V3, then the signal wires. Measure the + rail's voltage against the − rail with a multimeter.
6. **Test its behaviour.** Does GPIO Out light the LEDs in the right order? Does GPIO In's bit 0 follow the button?
7. **Have a classmate check it.** Hand them the breadboard and the schematic without explaining anything, and time how many minutes it takes them to confirm every net is wired correctly.
   This time is your work's tidiness score.

| Check | Result |
|---|---|
| Does the power rail break in the middle? | |
| + rail vs. − rail (button released) | should be OL |
| + rail vs. − rail (button pressed) | should be about 10 kΩ |
| Every LED passes diode mode | |
| + rail voltage after applying power | |
| GPIO Out lights in the right order | |
| GPIO In's bit 0 follows the button | |
| Time your classmate took to check it | |

## Going further

A breadboard suits experimentation, but a circuit that must survive real use needs soldering. The next lesson, [Soldering safely](../l02-soldering-safely/README.md),
practises soldering one row of a connector well enough to pass a visual check and a multimeter check.

## Reflect

The last time a circuit on your breadboard did not work, what was the cause? If you had used this lesson's pre-power checklist, how much sooner would you have found it?

## References

- [Breadboard (Wikipedia)](https://en.wikipedia.org/wiki/Breadboard)
