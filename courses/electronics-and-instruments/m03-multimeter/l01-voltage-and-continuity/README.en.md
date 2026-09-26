---
id: elec.m03.l01
lang: en
title: {th: วัดแรงดันและความต่อเนื่อง, en: Measuring voltage and continuity}
summary: {th: เลือกโหมดและย่านวัด วัดแรงดันขนานกับจุดที่ต้องการ และตรวจสายขาดหรือลัดวงจรด้วยโหมดความต่อเนื่อง, en: 'Pick mode and range, measure voltage in parallel, and find breaks or shorts with continuity mode.'}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m02.l02]
objectives:
- {th: วัดแรงดันที่จุดทดสอบบนบอร์ดโดยเลือกโหมดและย่านวัดถูกต้อง, en: Measure voltage at board test points with the right mode and range.}
- {th: ตรวจความต่อเนื่องของสายและหาจุดลัดวงจรบนวงจรที่ปิดไฟแล้ว, en: Check continuity and find shorts on an unpowered circuit.}
develops:
- {skill: meas.multimeter, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: alpha
translation: done
source_sha256: 773a0505d3ee9180737a94eaa362e48b4730985706f78c6874bbbb07e555b696
---

## Objectives

By the end of this lesson you will:

1. Measure voltage at a board's test points, choosing the right mode and range, and state how accurate the reading is
2. Check continuity in wires and find a short circuit on an unpowered circuit

## Before you start

- A digital multimeter with its manual (if you cannot find a paper copy, find the PDF for that model — we will need to read its accuracy specification)
- A board, a USB cable, a breadboard still holding the circuit from the lesson [Voltage, current and resistance](../../m01-circuits/l01-voltage-current-resistance/README.md), several jumper wires
- If you have them, hook or clip test leads help keep a hand free and reduce slipping

> **Safety.** This course **never measures mains power**, under any circumstance. Mains voltage (230 V) requires a meter and leads with the correct safety rating, and specific training.
> A good multimeter and its leads print a measurement category rating, such as CAT II 600 V or CAT III 1000 V, per the IEC 61010 standard. A higher CAT number tolerates larger transient surges from the electrical system.
> Even though our work is at 3.3 V, choosing a rated instrument from the start is a good habit, because the same meter may one day be picked up for more dangerous work.

## See it work first

Pick up the multimeter and look at it before plugging in any leads.

- How many jack sockets does it have? Which is labelled COM, which is labelled VΩ (or V, Ω, diode), which is labelled mA or µA, and is there a separate 10A or A jack? Is a fuse rating printed near those jacks?
- What symbols are on the rotary dial? Find V⎓ (DC voltage), V~ (AC voltage), Ω, a speaker or sound-wave symbol (continuity), and a diode symbol.
- Is this a manual-range meter (with numbers like 200m, 2, 20, 200 around the dial), or an auto-ranging one (with the word AUTO on the display)?

Write your answers down — we will use them when choosing a range in the next section.

## Concepts

### 1. Mode, jacks, range, and accuracy

| What you measure | Dial | Red lead | Black lead | How to connect |
|---|---|---|---|---|
| DC voltage | V⎓ | VΩ | COM | In parallel (across the points you measure) |
| Resistance, continuity, diode | Ω, speaker, diode | VΩ | COM | Across the component, **powered off** |
| Current | mA or A | mA or 10A | COM | In series (next lesson) |

**Choosing a range.** On a manual-range meter, pick the **smallest range that is still larger than the value you expect** — for example, measure 3.3 V on the 20 V range.
If you pick the 2 V range instead, the display shows OL (overload) because the real value exceeds that range. Nothing is damaged — just step up a range. If you have no idea what to expect, start from the largest range and step down.

**Resolution is not accuracy.** A 3½-digit meter (2000 counts) on the 20 V range displays down to 0.01 V, but the manual states its real accuracy something like
"±(0.5% + 2 digits)," meaning the error can be 0.5% of the reading, plus another 2 units of the last displayed digit.

**Example:** a reading of 3.29 V on the 20 V range

```text
Error = ±(0.5% × 3.29 V + 2 × 0.01 V) = ±(0.016 + 0.020) V = ±0.036 V
The real value lies roughly between 3.25 V and 3.33 V
```

If a classmate measures 3.30 V with a different meter, neither of you is wrong — both values fall within the instruments' error bands. Do not waste time chasing a difference smaller than your tools' own accuracy.

### 2. Measuring voltage: in parallel, referenced to ground

<figure>
<svg viewBox="0 0 380 190" width="380" role="img" aria-label="A multimeter measuring voltage in parallel across a resistor" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<path d="M70 22H90M80 22V30"/><text x="80" y="17" text-anchor="middle" fill="currentColor" stroke="none">3V3</text>
<path d="M80 30V40"/>
<polyline points="80,40 80,50 86,52.5 74,57.5 86,62.5 74,67.5 86,72.5 74,77.5 80,80 80,90"/>
<text x="64" y="70" text-anchor="end" fill="currentColor" stroke="none">R1</text>
<path d="M80 90V100"/>
<circle cx="80" cy="100" r="2.5" fill="currentColor"/>
<polyline points="80,100 80,110 86,112.5 74,117.5 86,122.5 74,127.5 86,132.5 74,137.5 80,140 80,150"/>
<text x="64" y="130" text-anchor="end" fill="currentColor" stroke="none">R2</text>
<path d="M80 150V160"/>
<circle cx="80" cy="160" r="2.5" fill="currentColor"/>
<path d="M80 160V168M70 168H90M74 172H86M78 176H82"/>
<path d="M80 100H160V112M80 160H160V148"/>
<circle cx="160" cy="130" r="18"/>
<text x="160" y="135" text-anchor="middle" font-weight="bold" fill="currentColor" stroke="none">V</text>
<text x="186" y="112" fill="currentColor" stroke="none">red → VΩ jack</text>
<text x="186" y="152" fill="currentColor" stroke="none">black → COM</text>
<text x="186" y="132" fill="currentColor" stroke="none">meter across R2 (parallel)</text>
</svg>
<figcaption>Measure voltage by connecting in parallel (across) the points you care about, with no need to break the circuit. Black lead at COM touches ground; red lead at the VΩ jack touches the point being measured.</figcaption>
</figure>

Voltage is the difference between two points, so measuring it never requires breaking a circuit — just touch two leads across the points of interest.
For most work on a board, leave the black lead at GND and touch various points with the red lead. The number you get is that point's "voltage relative to ground."
If the leads are swapped, a digital meter simply shows a negative value — not dangerous for DC.

A multimeter in voltage mode has very high input resistance (usually around 10 MΩ), so it barely disturbs the circuit, except in very high-resistance circuits — which we already saw in the [voltage dividers](../../m01-circuits/l02-dividers-and-sensors/README.md) lab.

**What should the supply voltage be?** Every voltage regulator model has its own tolerance — check that specific part's datasheet.
If you do not know the exact part, use ±5% as a rough rule: a 3.3 V rail should sit between 3.14 and 3.47 V, and a 1.8 V rail between 1.71 and 1.89 V.
Outside this range is considered abnormal — find the cause before doing anything else.

**Probing technique.** Probe only header pins, labelled test points (marked TP), or the leads of large components.
**Never probe the closely spaced pins of a chip on a powered board** — the slightest slip of the probe tip can short two adjacent pins, and the board can be destroyed in a fraction of a second.

### 3. Continuity and resistance: powered off only

Ω mode and continuity mode work by sending a small current from the meter itself through whatever you are measuring, and reading the resulting voltage.
If the circuit has its own power source active, the reading will be wrong, and the meter can be damaged. **Always remove power, and let capacitors discharge, before measuring.**

**Continuity mode** beeps when resistance is below a threshold (usually around ten to a few tens of ohms, depending on the model — check the manual). It quickly answers "are these two points connected?"

- Is a jumper wire broken inside? Measure end to end — it must beep.
- Is a breadboard's power rail broken in the middle? Measure from the left end to the right end.
- Is the supply rail shorted to ground? Measure between the 3V3 rail and the GND rail — **it must not beep.**

**In-circuit resistance.** When you measure a component still wired into a circuit, the meter sees every path connected across those two points.
Measuring a 10 kΩ resistor that has another 10 kΩ in parallel with it will read 5 kΩ — that does not mean the resistor is faulty. If you need its real value, lift one lead out of the circuit.

**A real board is neither 0 nor infinite.** Measuring between the 3V3 rail and GND on a powered-off board usually gives several hundred ohms to a few kilohms, and the value may slowly climb,
because many decoupling capacitors are being charged by the meter's own current. What signals a true "short" is a value close to 0 Ω that does not move.
The best method is to compare against a known-working board of the same model.

**Diode mode** shows the voltage drop across a conducting diode (a silicon diode is about 0.5 to 0.7 V). It can find an LED's polarity — some LEDs will glow faintly when the red lead is on the anode.

## Worked example

**Scenario:** the breadboard circuit from the first lesson (R1 = 1 kΩ, R2 = 2.2 kΩ in parallel with R3 = 4.7 kΩ) is wired up, but the voltage at point A reads 0 V instead of the expected 1.98 V. Find the cause, step by step.

1. **Start at the supply.** Plug in power, and measure the breadboard's 3V3 rail against its GND rail: 3.29 V. The supply is fine; the problem is in the circuit.
2. **Measure point by point along the current path.** R1's pin on the 3V3-rail side reads 3.29 V; R1's other pin reads 0 V. This means either all the voltage is dropping across R1, or R1 is broken, or point A is being pulled to ground.
3. **Remove power, then switch to continuity mode.** Measure between point A and the GND rail: the meter beeps immediately, with a value near 0 Ω. Point A is shorted to ground.
4. **Find the culprit.** Trace the jumper wires connected to point A's column, and find that one wire has slipped into the column right next to the GND rail.
5. **Fix it, then check before applying power.** Measure the resistance between the breadboard's 3V3 rail and GND rail (still disconnected from the board): about 2.50 kΩ, matching R1 + (R2 ∥ R3) = 1 + 1.50 kΩ.
6. **Apply power, and measure again.** Point A now reads 1.97 V, within the tolerance of the resistors and the instrument.

Notice the sequence: measure voltage while powered to find "where it's wrong," then power off and use continuity or Ω to find "why it's wrong" — and always check total resistance before applying power again.

## Practice

1. A manual-range meter has ranges of 200 mV, 2 V, 20 V, 200 V. To measure 1.8 V, which range should you use, and what resolution do you get?
2. A meter rated at ±(0.5% + 3 digits) reads 1.802 V on the 2 V range (resolution 0.001 V). What range does the real value fall in?
3. Measuring the 3V3 pin on the 2 V range, the display shows OL. What does this mean, and what should you do next?
4. Measuring a 4.7 kΩ resistor that has another 4.7 kΩ in parallel with it, in circuit, what will you read?
5. Measuring resistance between a powered-off board's 3V3 rail and GND gives 0.3 Ω, and the value does not move. What should you do next?
6. Measuring a 3.3 V rail gives −3.30 V. What caused this, and is it dangerous?
7. In the worked-example circuit, with the 3V3 wire disconnected from the board, measuring resistance across R2 (from point A to GND) without lifting any leads — what would you read, and why?

## Solution

1. The 2 V range, because it is the smallest range still larger than 1.8 V. Resolution is 0.001 V (1 mV).
2. ±(0.5% × 1.802 + 3 × 0.001) = ±(0.009 + 0.003) = ±0.012 V. The real value lies between 1.790 and 1.814 V.
3. The real value exceeds the chosen range. Switch to the 20 V range — nothing is damaged.
4. 4.7 kΩ ∥ 4.7 kΩ = 2.35 kΩ. To get the single resistor's own value, lift one of its leads out of the circuit.
5. A value near 0 Ω that does not move is a short circuit. **Never apply power.** Compare against a working board, and look for the short — a solder bridge, a metal fragment, or a capacitor that has failed shorted.
6. The red and black leads are swapped. For DC, this is not dangerous — the meter simply shows a minus sign.
7. About 1.50 kΩ, because the meter now sees R2 in parallel with R3 (R1 is not on the path, since its other end is floating once the 3V3 wire is disconnected).

## Check your understanding

Answer at least 4 of the 5 questions in [quiz.yaml](quiz.yaml) correctly.

## Lab

**Part A: measure the board's supply rails** (powered on)

1. Plug in USB. Set the meter to V⎓ (use the 20 V range if manual). Black lead at the header's GND.
2. Measure the header's 3V3 pin. Record the value and the range used, then compute the error band from your meter's manual spec.
3. If the header has a 5V pin (power from USB), measure it too, and compare against the acceptable range for USB power stated in the board's documentation or the USB standard.
4. Open the board's schematic. If there is a test point or a safely accessible 1V8 pin (not a chip's own pin), measure it too. If there is no such point, skip it and note why.
5. Fill in the table, and decide whether each rail is within its normal range.

| Rail | Range used | Reading | ± per meter spec | Acceptable range | Normal? |
|---|---|---|---|---|---|
| 3V3 | | | | 3.14 to 3.47 V (±5%) | |
| 5V (if present) | | | | per documentation | |
| 1V8 (if a test point exists) | | | | 1.71 to 1.89 V (±5%) | |

**Part B: continuity and finding a short** (powered off)

1. Unplug USB, and disconnect every wire between the breadboard and the board.
2. Check continuity on every jumper wire you use often. Discard any that do not beep, or beep inconsistently while wiggled.
3. Check whether the breadboard's power rails run the full length, or break in the middle (some long breadboards do).
4. Wire the R1, R2, R3 circuit from the first lesson back up, and measure resistance between the breadboard's 3V3 rail and GND rail, comparing against 2.50 kΩ.
5. **The short-hunting game.** Have a classmate secretly plug a short jumper wire between any two columns in the circuit, without telling you. Use Ω mode and continuity mode to find it.
   Record which points you measured, in what order, and how many measurements it took. Try to minimise this by splitting the circuit in half each time.

## Going further

The next lesson, [Measuring current safely](../l02-current-safely/README.md), covers the mode that destroys multimeters most often.
We will look at why, and how to make sure it never happens to your meter.

## Reflect

In the short-hunting game, which method found the fault fastest? Does that way of thinking also apply to hunting bugs in a program?

## References

- [Multimeter (Wikipedia)](https://en.wikipedia.org/wiki/Multimeter)
- [Lessons In Electric Circuits by Tony R. Kuphaldt (open book)](https://www.ibiblio.org/kuphaldt/electricCircuits/)
