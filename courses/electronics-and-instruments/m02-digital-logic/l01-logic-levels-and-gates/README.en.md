---
id: elec.m02.l01
lang: en
title: {th: ระดับลอจิกและเกตพื้นฐาน, en: Logic levels and basic gates}
summary: {th: รู้ว่าแรงดันเท่าไรนับเป็น 0 หรือ 1 และทำไมการต่ออุปกรณ์ต่างระดับแรงดันจึงอันตราย, en: 'Know which voltages count as 0 or 1, and why mixing voltage levels is dangerous.'}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m01.l03]
objectives:
- {th: อ่านค่าระดับลอจิกขาเข้าและขาออกจากเอกสารข้อมูลของชิป แล้วบอกได้ว่าสองอุปกรณ์ต่อกันตรงได้หรือไม่, en: Read input and output logic thresholds from datasheets and decide whether two devices can connect directly.}
- {th: 'เขียนตารางความจริงของเกต AND, OR, NOT, XOR และใช้แก้โจทย์เงื่อนไขง่าย ๆ ได้', en: 'Write truth tables for AND, OR, NOT and XOR and use them on simple conditions.'}
develops:
- {skill: hw.digital, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: alpha
translation: done
source_sha256: 5258cd1a1c2e38505b51961f281c99b2d0451885a1339ec0fd8e879e48a658c7
---

## Objectives

By the end of this lesson you will:

1. Read a chip's input and output logic thresholds from its datasheet, and decide whether two devices can connect directly
2. Write truth tables for AND, OR, NOT and XOR gates, and use them to solve simple conditional problems

## Before you start

- You can already calculate a voltage divider (lesson [Voltage dividers](../../m01-circuits/l02-dividers-and-sensors/README.md))
- For the lab: a TESAIoT Dev Kit flashed with the [QWA309 Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) example, a multimeter, a breadboard,
  a 1 kΩ resistor, a 2.2 kΩ resistor, two 4.7 kΩ resistors, three 10 kΩ resistors (or one 10 kΩ potentiometer in place of the resistor set)
- If using the Eva Kit, write your own short program that sets a spare pin as an input and prints what it reads, in place of the header test program

## See it work first

The TESAIoT Dev Kit has at least two "voltage worlds" living on a single board.

- The on-board sensor's I2C bus runs at **1.8 V** (SCB0, pin P8.0 = SCL, P8.1 = SDA, at 400 kHz, per the description in the SDK's `cm33/sensors/01_i2c_bus_scan.c` example).
  The same example notes that MicroPython's `machine.I2C` is a different bus, at **3.3 V**, meant for connecting an external sensor board.
- The header pins run at **3.3 V** — you can see this in the signal names the header test program prints, such as `P13.3_GPIO_PWM5+_3V3`, where the trailing `_3V3` states the voltage domain.

Suppose you have a sensor board that runs at 3.3 V — which bus can it connect to, and what happens if you connect it to the wrong one? This lesson gives you the numbers to answer that.

## Concepts

### 1. Which voltages count as 0 or 1

A digital chip does not just see "power or no power." It compares voltage against four thresholds guaranteed by the datasheet.

| Value | Meaning |
|---|---|
| V_OH(min) | An output driven to 1 will give **at least** this voltage |
| V_OL(max) | An output driven to 0 will give **no more than** this voltage |
| V_IH(min) | An input is guaranteed to read 1 when the voltage is **at or above** this |
| V_IL(max) | An input is guaranteed to read 0 when the voltage is **no more than** this |

Between V_IL and V_IH is an unguaranteed range — an input may read anything there, and may bounce around if there is any noise.

<figure>
<svg viewBox="0 0 360 200" width="360" role="img" aria-label="Logic-level bands for a 3.3 V and a 1.8 V system, using the 0.7 and 0.3 of VDD rule of thumb" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<rect x="20" y="21.5" width="60" height="148.5" rx="3"/>
<path d="M20 66.1H80M20 125.5H80"/>
<text x="50" y="47.775000000000006" text-anchor="middle" font-weight="bold" fill="currentColor" stroke="none">1</text>
<text x="50" y="99.75" text-anchor="middle" fill="currentColor" stroke="none">?</text>
<text x="50" y="151.725" text-anchor="middle" font-weight="bold" fill="currentColor" stroke="none">0</text>
<text x="86" y="70.05000000000001" fill="currentColor" stroke="none">V_IH 2.31 V</text>
<text x="86" y="129.45" fill="currentColor" stroke="none">V_IL 0.99 V</text>
<text x="86" y="25.5" fill="currentColor" stroke="none">3.3 V</text>
<text x="50" y="190" text-anchor="middle" fill="currentColor" stroke="none">3.3 V CMOS</text>
<rect x="200" y="89.0" width="60" height="81.0" rx="3"/>
<path d="M200 113.3H260M200 145.7H260"/>
<text x="230" y="105.15" text-anchor="middle" font-weight="bold" fill="currentColor" stroke="none">1</text>
<text x="230" y="133.5" text-anchor="middle" fill="currentColor" stroke="none">?</text>
<text x="230" y="161.85" text-anchor="middle" font-weight="bold" fill="currentColor" stroke="none">0</text>
<text x="266" y="117.3" fill="currentColor" stroke="none">V_IH 1.26 V</text>
<text x="266" y="149.7" fill="currentColor" stroke="none">V_IL 0.54 V</text>
<text x="266" y="93.0" fill="currentColor" stroke="none">1.8 V</text>
<text x="230" y="190" text-anchor="middle" fill="currentColor" stroke="none">1.8 V CMOS</text>
<path d="M15 170H350"/>
</svg>
<figcaption>Example bands using the rule of thumb V_IH = 0.7 × VDD and V_IL = 0.3 × VDD. The middle range is where an input is not guaranteed to read anything in particular. Always use the real values from the chip's datasheet.</figcaption>
</figure>

Many CMOS chips use thresholds close to 0.7 × VDD and 0.3 × VDD; the figure above uses this rule of thumb.
At 3.3 V, that gives V_IH = 2.31 V, V_IL = 0.99 V. At 1.8 V, it gives V_IH = 1.26 V, V_IL = 0.54 V.
But every chip model differs, and some let you choose the threshold — **the value you actually decide with must always come from the datasheet.**

**Noise margin** tells you how much room there is for noise before a 1 turns into an uncertain value.

```text
NM_H = V_OH(min) − V_IH(min)
NM_L = V_IL(max) − V_OL(max)
```

If either comes out negative, the two devices cannot connect directly.

### 2. Can two devices connect to each other?

Use these example values from two devices' assumed datasheets.

| Value | Device A (1.8 V) | Device B (3.3 V) |
|---|---|---|
| V_OH(min) | 1.35 V | 2.9 V |
| V_OL(max) | 0.45 V | 0.4 V |
| V_IH(min) | 1.26 V | 2.31 V |
| V_IL(max) | 0.54 V | 0.99 V |
| Maximum tolerated input voltage (absolute maximum) | 2.1 V | 3.6 V |

**A driving B:** A's level 1 can be as low as 1.35 V, but B needs at least 2.31 V. NM_H = 1.35 − 2.31 = −0.96 V, which is negative.
They cannot connect directly — B would read A's 1 as an uncertain value (in fact, even A's full 1.8 V is still below B's 2.31 V).

**B driving A:** logically, 2.9 V is above A's V_IH (1.26 V), so it reads comfortably as 1. But 2.9 to 3.3 V **exceeds the maximum voltage A's pin can tolerate (2.1 V).**
Current will flow through A's protection diode into A's own 1.8 V supply rail (back-powering) — the pin can be damaged, or the chip can behave strangely even before it has been powered on itself.
This is the most dangerous trap of all, because "it reads correctly" on day one.

**B to B:** NM_H = 2.9 − 2.31 = 0.59 V and NM_L = 0.99 − 0.4 = 0.59 V. Both positive — this connects directly, fine.

**Fixes when direct connection is not possible:**

- A level-translator chip. Works for fast signals, available in both directional and bidirectional versions.
- An open-drain bus, like I2C, uses a MOSFET-based level shifter or a dedicated chip, with a separate pull-up resistor on each side.
- A slow, one-direction, high-to-low signal can use a voltage divider — for example, 10 kΩ and 12 kΩ, converting 3.3 V to 1.80 V.
  But R_th = 10 kΩ ∥ 12 kΩ = 5.45 kΩ, together with a pin capacitance of about 10 pF, gives τ ≈ 55 ns — the edges slow down. This works for signals up to a few hundred kHz, but not for high-speed SPI.

Back to the opening question: a 3.3 V sensor board should connect to the 3.3 V bus, which needs no level shifting at all. If it must connect to the 1.8 V bus, a level-shifting circuit is required.

### 3. Basic gates and truth tables

Once a signal is clearly 0 or 1, we combine them with logic gates.

| A | B | NOT A | A AND B | A OR B | A XOR B |
|---|---|---|---|---|---|
| 0 | 0 | 1 | 0 | 0 | 0 |
| 0 | 1 | 1 | 0 | 1 | 1 |
| 1 | 0 | 0 | 0 | 1 | 1 |
| 1 | 1 | 0 | 1 | 1 | 0 |

- **AND** is 1 when every input is 1
- **OR** is 1 when at least one input is 1
- **NOT** inverts a value
- **XOR** is 1 when the two inputs **differ** — used for change detection or bit flipping
- NAND and NOR are AND and OR each followed by a NOT

In C, use `&&`, `||`, `!` for conditions and `&`, `|`, `~`, `^` for bits. In MicroPython, use `and`, `or`, `not` and `&`, `|`, `^`.

**A real case on the board:** the header test program has a PWM Out button that drives pins P13.3 and P13.4 as a phase-inverted pair, then tells you to check for "no both-high fault."
This fault condition is `P13.3 AND P13.4` — whenever this is 1, something is wrong. The condition that the pair is working correctly is `P13.3 XOR P13.4`, which must be 1 throughout the time the signal is running.

**An active-low button:** its pin reads 0 when pressed. So "pressed" = `NOT pin`. We will actually wire this in the next lesson.

## Worked example

**Problem:** a cooling fan must run when "temperature is high **and** the cabinet door is closed," **or** when the user commands it manually.
Let T = temperature high, D = door closed, M = manual command. Write the truth table, then turn it into code.

```text
FAN = (T AND D) OR M
```

| T | D | M | T AND D | FAN |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 | 1 |
| 0 | 1 | 0 | 0 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 | 1 |

Check the table: every row with M = 1 must run the fan (four rows), and when M = 0 there is exactly one row that runs it, T = 1 and D = 1 — five rows in total, matching the table.

If the door switch is wired active-low (closed reads as 0), the code must invert it before use.

```c
bool door_closed = !door_pin;                 /* active-low: reads 0 when closed */
bool fan_on = (temp_high && door_closed) || manual;
```

Three inputs give 2³ = 8 combinations. Writing out every row is the simplest way to test this. Before turning it into code, try walking through every row in your head first.

## Practice

1. An output has V_OH(min) = 2.4 V and V_OL(max) = 0.4 V, connected to a TTL input with V_IH(min) = 2.0 V and V_IL(max) = 0.8 V. Find NM_H and NM_L. Can they connect directly?
2. Using the rule of thumb 0.7 × VDD and 0.3 × VDD, find V_IH and V_IL for an input powered at 2.5 V.
3. A 5 V device sends a 5 V signal into a 3.3 V microcontroller pin whose datasheet does not state 5 V tolerance. Can they connect directly? Why or why not?
4. Write the truth table of `NOT (A OR B)` (that is, NOR), and compare it against `(NOT A) AND (NOT B)`. Notice something?
5. A burglar alarm sounds when "the system is armed (ARM) and the door is open (OPEN) and it is not in maintenance mode (MAINT)." Write the expression, and say how many of the eight rows make it sound.
6. A circuit checking a phase-inverted pair A and B needs a signal ERR that is 1 when A and B have the same value. Write ERR using the gates you have learned.

## Solution

1. NM_H = 2.4 − 2.0 = 0.4 V, and NM_L = 0.8 − 0.4 = 0.4 V. Both positive, so they connect directly.
2. V_IH = 0.7 × 2.5 = 1.75 V, and V_IL = 0.3 × 2.5 = 0.75 V.
3. No. 5 V exceeds the maximum most 3.3 V pins tolerate (usually around VDD + 0.3 V). Current would flow through the protection diode into the supply rail. Use a level translator, or a voltage divider if the signal is slow and one-directional.
4. Both expressions give 1, 0, 0, 0 for (A, B) = (0, 0), (0, 1), (1, 0), (1, 1) — identical on every row. This is De Morgan's law.
5. `ALARM = ARM AND OPEN AND (NOT MAINT)`. Exactly one row sounds it: ARM = 1, OPEN = 1, MAINT = 0.
6. `ERR = NOT (A XOR B)` (also called XNOR). It is 1 when A and B are equal, which covers both being 1 together (both-high) and both being 0 together.

## Check your understanding

Answer at least 4 of the 5 questions in [quiz.yaml](quiz.yaml) correctly. Questions 1 through 3 use the values table for devices A and B in section 2.

## Lab

**Part A: measure real output levels with a multimeter**

1. Run the [QWA309 Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) program. Find pins P13.0 and GND on the header from the board's pinout diagram.
2. Set the meter to DC voltage mode, black lead at GND, red lead at P13.0, then press the **GPIO Out** button on screen.
   The program drives each pin in turn (P13.0, P13.3, P13.4, P13.5, P13.6, P13.7), about 0.7 s each, then turns everything off, and repeats this three times.
3. Record the voltage while P13.0 is 1, and while it is 0 — these are the pin's real V_OH and V_OL, unloaded.
4. Use the table in section 2 to decide whether this pin can drive device A (1.8 V) and device B (3.3 V), with your reasoning.

**Part B: find the real switching point of an input**

1. With USB unplugged, wire a voltage divider on the breadboard from 3V3, with its midpoint connected through a 1 kΩ resistor to pin P13.0 (the 1 kΩ resistor protects the pin in case GPIO Out is pressed accidentally while this circuit is connected).
2. Press the **GPIO In** button. The program sets all six pins as high-Z inputs (no pull), reads every 100 ms for 8 s, and prints the mask value every time it changes. Bit 0 is P13.0.
   Other bits may bounce around because those pins are floating — that is next lesson's topic. For now, watch only bit 0.
3. Change the resistor pair (top / bottom) per the table, measure the midpoint voltage with the meter, then press GPIO In and read bit 0.

| Top / bottom | Calculated voltage | Measured voltage | Bit 0 read |
|---|---|---|---|
| 10 kΩ / 2.2 kΩ | 0.60 V | | |
| 10 kΩ / 4.7 kΩ | 1.06 V | | |
| 10 kΩ / 10 kΩ | 1.65 V | | |
| 4.7 kΩ / 10 kΩ | 2.24 V | | |
| 2.2 kΩ / 10 kΩ | 2.70 V | | |

If you have a potentiometer, use it instead of the resistor set, and slowly turn it to find the voltage where bit 0 changes, in both directions (up and down). If these two values differ, the input has hysteresis.

**Interpreting the results:** the datasheet only guarantees that below V_IL reads 0 and above V_IH reads 1. The real switching point on your specific board sits somewhere in between,
and may vary with temperature or between individual chips. **Never design a circuit relying on a switching point measured from a single board** — always design from the V_IL and V_IH values in the datasheet.

## Going further

The next lesson, [Pull-ups, pull-downs and push buttons](../l02-pullups-and-buttons/README.md), looks at why a floating input pin reads garbage,
wires an active-low button, and uses a logic analyzer for the first time to see a button's bounce.

## Reflect

If a friend told you "I connected 3.3 V to a 1.8 V pin and it read fine," how would you explain the risk to them, using the numbers from this lesson?

## References

- [Logic gate (Wikipedia)](https://en.wikipedia.org/wiki/Logic_gate)
- [Lessons In Electric Circuits by Tony R. Kuphaldt (open book)](https://www.ibiblio.org/kuphaldt/electricCircuits/)
- [Logic level (Wikipedia)](https://en.wikipedia.org/wiki/Logic_level)
- [SDK: cm33/sensors/01_i2c_bus_scan.c (the 1.8 V sensor bus and machine.I2C's 3.3 V bus)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/01_i2c_bus_scan.c)
- [README of QWA309 Header I/O Test (Developer Hub, commit 372d0d8)](https://github.com/tesaiot/developer-hub/blob/372d0d849578a6a49b634d3ecaab8b5958166921/prac_qwa309_header_hw_test/README.md)
