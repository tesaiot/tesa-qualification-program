---
id: elec.m01.l01
lang: en
title: {th: แรงดัน กระแส และความต้านทาน, en: 'Voltage, current and resistance'}
summary: {th: ใช้กฎของโอห์มและกฎกำลังไฟฟ้าคำนวณวงจรพื้นฐาน, en: Use Ohm's law and the power law to work out basic circuits.}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: []
objectives:
- {th: คำนวณแรงดัน กระแส หรือความต้านทานที่ไม่ทราบค่าในวงจรอนุกรมและขนานด้วยกฎของโอห์ม, en: 'Compute an unknown voltage, current or resistance in series and parallel circuits with Ohm''s law.'}
- {th: คำนวณกำลังไฟฟ้าที่ตัวต้านทานรับ และเลือกพิกัดกำลังที่เหมาะสม, en: Compute the power a resistor dissipates and choose a suitable power rating.}
develops:
- {skill: hw.circuits, to: 2}
- {skill: hw.math, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: alpha
translation: done
source_sha256: f95239ef9738d06840421975199bf86ef2fcff2ed0fb8dfe3080ba57e443625d
---

## Objectives

By the end of this lesson you will:

1. Compute an unknown voltage, current or resistance in series and parallel circuits with Ohm's law
2. Compute the power a resistor dissipates, and choose a suitable power rating

## Before you start

- A calculator, paper and a pencil. The concepts and practice do not need a board.
- For the lab: a TESAIoT Dev Kit or Eva Kit board with a USB cable, a breadboard, jumper wires, one each of 1 kΩ, 2.2 kΩ and 4.7 kΩ resistors (standard 1/4 W), and a digital multimeter
- Never used a multimeter before? That is fine — this lab uses only voltage mode and resistance mode. Full detail is in Module 3.

> **Safety.** Everything in this lesson uses only the board's 3.3 V supply. Never let a jumper wire connect the 3V3 pin straight to GND (a short circuit),
> and always unplug the USB cable before moving wires on the breadboard.

## See it work first

Pick up the board and look at it. Find the USB connector (where power comes in), then find the pins labelled **3V3** (or 3.3V) and **GND** on the header.
If the silkscreen labels are too small to read, open the board's pinout diagram instead.

GND is the whole board's reference point. Every time we say "this pin is 3.3 V," we always mean "3.3 V above GND" —
the same way a building's height is measured from the ground, not from sea level.

Now guess, before reading on: if you connected one 1 kΩ resistor between 3V3 and GND, how much current would flow, and would the resistor get hot?
Write your answer down, then compare it against what we calculate in the next section.

## Concepts

### 1. Ohm's law: three quantities, one equation

- **Voltage (V)**, in volts (V), is the push that makes charge move. It is always measured between two points.
- **Current (I)**, in amperes (A), is the amount of charge flowing past one point per second.
- **Resistance (R)**, in ohms (Ω), is whatever opposes the current.

All three are tied together by **Ohm's law:**

```text
V = I × R        I = V / R        R = V / I
```

On a microcontroller board, current is usually in milliamps (mA) and resistance is usually in kilohms (kΩ).
Using the pair **mA and kΩ** gives you volts out directly, with no zeros to count.

**Example:** a 1 kΩ resistor across 3.3 V

```text
I = V / R = 3.3 V / 1 kΩ = 3.3 mA
```

Change it to 10 kΩ and the current drops by a factor of ten, to 0.33 mA, or 330 µA.

What about a wire with only 0.1 Ω of resistance? The same law says the current wants to flow at 3.3 / 0.1 = 33 A.
This is exactly why shorting the 3V3 pin to GND is dangerous: the board's voltage regulator gets extremely hot or shuts itself off, and thin traces on the board can burn.

### 2. Series and parallel

<figure>
<svg viewBox="0 0 340 200" width="340" role="img" aria-label="A series circuit and a parallel circuit from a 3.3 V supply" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<path d="M60 22H80M70 22V30"/><text x="70" y="17" text-anchor="middle" fill="currentColor" stroke="none">3.3 V</text>
<path d="M70 30V40"/>
<polyline points="70,40 70,50 76,52.5 64,57.5 76,62.5 64,67.5 76,72.5 64,77.5 70,80 70,90"/>
<text x="86" y="70" fill="currentColor" stroke="none">R1 1 kΩ</text>
<polyline points="70,90 70,100 76,102.5 64,107.5 76,112.5 64,117.5 76,122.5 64,127.5 70,130 70,140"/>
<text x="86" y="120" fill="currentColor" stroke="none">R2 2.2 kΩ</text>
<path d="M70 140V150"/>
<path d="M70 150V158M60 158H80M64 162H76M68 166H72"/>
<path d="M50 50L50 80M47.3 73.6L50 80L52.7 73.6"/>
<text x="44" y="70" text-anchor="end" fill="currentColor" stroke="none">I</text>
<text x="75" y="190" text-anchor="middle" fill="currentColor" stroke="none">series: R = R1 + R2</text>
<path d="M240 22H260M250 22V30"/><text x="250" y="17" text-anchor="middle" fill="currentColor" stroke="none">3.3 V</text>
<path d="M250 30V50M210 50H290M210 50V70M290 50V70"/>
<circle cx="250" cy="50" r="2.5" fill="currentColor"/>
<polyline points="210,70 210,80 216,82.5 204,87.5 216,92.5 204,97.5 216,102.5 204,107.5 210,110 210,120"/>
<text x="194" y="100" text-anchor="end" fill="currentColor" stroke="none">R1</text>
<polyline points="290,70 290,80 296,82.5 284,87.5 296,92.5 284,97.5 296,102.5 284,107.5 290,110 290,120"/>
<text x="306" y="100" fill="currentColor" stroke="none">R2</text>
<path d="M210 120V140M290 120V140M210 140H290M250 140V150"/>
<circle cx="250" cy="140" r="2.5" fill="currentColor"/>
<path d="M250 150V158M240 158H260M244 162H256M248 166H252"/>
<text x="250" y="190" text-anchor="middle" fill="currentColor" stroke="none">parallel: 1/R = 1/R1 + 1/R2</text>
</svg>
<figcaption>Left: series — the same current flows through every part, and the voltage divides. Right: parallel — every part sees the same voltage, and the current splits between them.</figcaption>
</figure>

**Series:** parts connected one after another in a single path.

- The current is the same through every part
- Total resistance R = R1 + R2 + …
- Each part's voltage adds up to the supply voltage (Kirchhoff's voltage law, KVL)

**Example:** 1 kΩ in series with 2.2 kΩ from 3.3 V

```text
R total = 1 kΩ + 2.2 kΩ = 3.2 kΩ
I       = 3.3 V / 3.2 kΩ = 1.03 mA
V_R1    = 1.03 mA × 1 kΩ   = 1.03 V
V_R2    = 1.03 mA × 2.2 kΩ = 2.27 V      check: 1.03 + 2.27 = 3.30 V
```

**Parallel:** parts connected across the same two points.

- Every part sees the same voltage
- Currents split apart, then add back together (Kirchhoff's current law, KCL)
- 1/R = 1/R1 + 1/R2 + … ; for exactly two, the shortcut is R = (R1 × R2) / (R1 + R2)
- The total resistance is always smaller than the smallest part — use this to sanity-check an answer quickly

**Example:** 1 kΩ in parallel with 2.2 kΩ at 3.3 V

```text
R total = (1 × 2.2) / (1 + 2.2) kΩ = 0.6875 kΩ = 687.5 Ω
I1 = 3.3 V / 1 kΩ   = 3.3 mA
I2 = 3.3 V / 2.2 kΩ = 1.5 mA
I total = 4.8 mA                 check: 3.3 V / 687.5 Ω = 4.8 mA
```

### 3. Power and power rating

A resistor turns electrical energy into heat. The rate it heats up is **power (P)**, in watts (W).

```text
P = V × I = I² × R = V² / R
```

Pick the formula that matches what you know: know the voltage across it and the resistance, use V² / R; know the current and the resistance, use I² × R.

Every resistor has a **power rating.** The leaded type used on most breadboards is typically 1/4 W.
The small SMD resistors on a board usually have a lower rating — always check the manufacturer's datasheet.
A common rule of thumb is to **choose a rating at least twice the power you calculated**, because a resistor running at its full rating gets very hot, and its rating drops further as the surrounding air gets hotter.

**Example 1:** the question from "See it work first" — 1 kΩ across 3.3 V

```text
P = V² / R = (3.3 V)² / 1000 Ω = 0.01089 W ≈ 10.9 mW
```

Far below 1/4 W (250 mW). The resistor barely warms up at all.

**Example 2:** 100 Ω across 5 V

```text
P = (5 V)² / 100 Ω = 0.25 W
```

Exactly at the 1/4 W rating. It works, but it will be too hot to touch, and its life will be short. Following the two-times rule, you would need 0.5 W, so pick a 1/2 W part.

## Worked example

This is the actual circuit we will build in the lab. Work through the calculation with us, line by line.

<figure>
<svg viewBox="0 0 300 215" width="300" role="img" aria-label="A mixed circuit: R1 in series with R2 in parallel with R3, from a 3.3 V supply" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<path d="M70 22H90M80 22V30"/><text x="80" y="17" text-anchor="middle" fill="currentColor" stroke="none">3.3 V (3V3)</text>
<path d="M80 30V40"/>
<polyline points="80,40 80,50 86,52.5 74,57.5 86,62.5 74,67.5 86,72.5 74,77.5 80,80 80,90"/>
<text x="96" y="70" fill="currentColor" stroke="none">R1 1 kΩ</text>
<path d="M80 90V100M40 100H200M80 100V100"/>
<circle cx="80" cy="100" r="2.5" fill="currentColor"/>
<text x="208" y="104" fill="currentColor" stroke="none">A (V_A)</text>
<path d="M40 100V115M160 100V115"/>
<polyline points="40,115 40,125 46,127.5 34,132.5 46,137.5 34,142.5 46,147.5 34,152.5 40,155 40,165"/>
<text x="56" y="145" fill="currentColor" stroke="none">R2 2.2 kΩ</text>
<polyline points="160,115 160,125 166,127.5 154,132.5 166,137.5 154,142.5 166,147.5 154,152.5 160,155 160,165"/>
<text x="176" y="145" fill="currentColor" stroke="none">R3 4.7 kΩ</text>
<path d="M40 165V180M160 165V180M40 180H160M100 180V188"/>
<circle cx="100" cy="180" r="2.5" fill="currentColor"/>
<path d="M100 188V196M90 196H110M94 200H106M98 204H102"/>
<circle cx="200" cy="100" r="3"/>
</svg>
<figcaption>A mixed circuit: R1 in series with the R2-parallel-R3 group. Point A is where we will calculate and measure the voltage relative to GND.</figcaption>
</figure>

**Problem:** a 3.3 V supply feeds R1 = 1 kΩ to point A; from point A, R2 = 2.2 kΩ is in parallel with R3 = 4.7 kΩ down to GND.
Find the voltage at point A, the current in every branch, and the power in every part.

**Step 1: collapse the parallel part first**

```text
R2 ∥ R3 = (2.2 × 4.7) / (2.2 + 4.7) kΩ = 10.34 / 6.9 kΩ = 1.499 kΩ ≈ 1.50 kΩ
```

**Step 2: now the circuit is just two parts in series**

```text
R total = 1 kΩ + 1.499 kΩ = 2.499 kΩ ≈ 2.50 kΩ
I       = 3.3 V / 2.499 kΩ = 1.32 mA          (the current through R1)
V_R1    = 1.32 mA × 1 kΩ = 1.32 V
V_A     = 3.3 V − 1.32 V = 1.98 V
```

**Step 3: split the current across the two branches using the voltage at A**

```text
I2 = 1.98 V / 2.2 kΩ = 0.90 mA
I3 = 1.98 V / 4.7 kΩ = 0.42 mA
KCL check: 0.90 + 0.42 = 1.32 mA  matches the current through R1
```

**Step 4: power**

| Part | Formula used | Power |
|---|---|---|
| R1 | I² × R = (1.32 mA)² × 1 kΩ | 1.74 mW |
| R2 | V² / R = (1.98 V)² / 2.2 kΩ | 1.78 mW |
| R3 | V² / R = (1.98 V)² / 4.7 kΩ | 0.83 mW |
| Total | check with V × I = 3.3 V × 1.32 mA | 4.36 mW |

The sum of the three parts (1.74 + 1.78 + 0.83 = 4.35 mW, differing from 4.36 due to rounding) equals the power the supply delivers.
Every part is dozens of times below 1/4 W, so ordinary leaded resistors are comfortably fine here.

Notice the habit used throughout this example: once you finish calculating, **always check with a second law** (KVL, KCL, or total power).
If the two numbers do not agree, some step is wrong.

## Practice

Try these yourself first, then scroll down to check the solutions.

1. A 4.7 kΩ resistor sits across 3.3 V. What is the current, in mA and in µA?
2. An indicator LED circuit needs 2 mA from 3.3 V. What must the circuit's total resistance be?
3. The total resistance of (a) two 10 kΩ resistors in parallel, (b) three 3.3 kΩ resistors in series
4. A 100 Ω resistor sits across 5 V. What power does it dissipate, and what power rating should you choose?
5. You measure 1.2 V across a 330 Ω resistor. What current flows through it?
6. A 3.3 V supply feeds 2.2 kΩ in series with a group of two 1 kΩ resistors in parallel. Find the total current, the voltage across the parallel group, and the current in each 1 kΩ resistor.

## Solution

1. I = 3.3 V / 4.7 kΩ = 0.702 mA = 702 µA
2. R = V / I = 3.3 V / 2 mA = 1.65 kΩ
3. (a) 10 × 10 / (10 + 10) = 5 kΩ  (b) 3 × 3.3 kΩ = 9.9 kΩ
4. P = 5² / 100 = 0.25 W. A 1/4 W part would run exactly at its rating; following the two-times rule, choose 1/2 W.
5. I = 1.2 V / 330 Ω = 3.64 mA. This is the safest way to measure current indirectly — we will use it again in Module 3.
6. 1 kΩ ∥ 1 kΩ = 500 Ω. Total resistance = 2.2 kΩ + 0.5 kΩ = 2.7 kΩ. Total current = 3.3 V / 2.7 kΩ = 1.22 mA.
   Voltage across the parallel group = 1.22 mA × 0.5 kΩ = 0.611 V. Current in each part = 0.611 V / 1 kΩ = 0.611 mA (the two together give 1.22 mA, matching the total current).

## Check your understanding

Answer at least 4 of the 5 questions in [quiz.yaml](quiz.yaml) correctly. For any you get wrong, go back and read the relevant section, then try the calculation again.

## Lab

**Lab goal:** build the circuit from the worked example, measure the real voltages, and explain why they do not match the calculation exactly.

1. **Measure the resistors before wiring anything.** Set the multimeter to Ω mode and measure all three resistors one at a time, disconnected from anything else. Record their real values.
   Do not hold both leads with your fingers — your body's resistance would end up in parallel with the reading.
2. **Wire the circuit as shown**, on the breadboard, with the board's USB cable still unplugged. Five holes in the same breadboard column are connected together (details in the lesson [Building a circuit on a breadboard](../../m06-build-and-read/l01-breadboarding/README.md)).
   Connect the GND wire from the board first, then the 3V3 wire.
3. **Guess** before applying power: write the values you expect to measure into the "calculated" column of the table.
4. **Plug in USB, then measure the voltages.** Set the meter to DC voltage mode (V⎓); black lead in the COM jack touching GND, red lead in the VΩ jack touching the point being measured.
   Measure the real 3V3 voltage first, then the voltage at point A, then the voltage across R1 (red lead at 3V3, black lead at point A).
5. **Compute the currents from the measured voltages.** I1 = V_R1 / R1 (using the resistance you measured in step 1), I2 = V_A / R2, and I3 = V_A / R3, then check that I1 ≈ I2 + I3.
6. **Unplug USB** before taking the circuit apart.

| Item | Calculated (nominal values) | Recalculated (measured values) | Measured |
|---|---|---|---|
| 3V3 voltage | 3.30 V | use your measured value | |
| V_A | 1.98 V | | |
| V_R1 | 1.32 V | | |
| I1 = V_R1 / R1 | 1.32 mA | | |
| I2 + I3 | 1.32 mA | | |

**Interpreting the results:** gold-band resistors carry a ±5% tolerance, and the real 3V3 rail may not be exactly 3.30 V.
If your measured values differ from the "recalculated" column by no more than about 1–2%, that counts as a match. If the difference is larger, find the cause before moving on.
Common causes are plugging into the wrong row, mixing up which resistor is which, or a broken jumper wire.

## Going further

The next lesson, [Voltage dividers and analogue sensors](../l02-dividers-and-sensors/README.md), picks up right where point A leaves off — it is itself a kind of voltage divider.
We will use the same principle to explain a knob on the board, and to convert the number the ADC reads back into volts.

## Reflect

When you guessed in "See it work first," did you think the 1 kΩ resistor would get hot? How did the real answer change how you think about "3.3 V power" now?

## References

- [Lessons In Electric Circuits by Tony R. Kuphaldt (open book)](https://www.ibiblio.org/kuphaldt/electricCircuits/)
- [OpenStax University Physics Volume 2 (the DC circuits chapter)](https://openstax.org/details/books/university-physics-volume-2)
- [Ohm's law (Wikipedia)](https://en.wikipedia.org/wiki/Ohm%27s_law)
