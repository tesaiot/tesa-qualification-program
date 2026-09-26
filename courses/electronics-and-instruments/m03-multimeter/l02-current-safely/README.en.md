---
id: elec.m03.l02
lang: en
title: {th: วัดกระแสอย่างปลอดภัย, en: Measuring current safely}
summary: {th: ต่อมัลติมิเตอร์อนุกรมเพื่อวัดกระแส ย้ายสายวัดให้ถูกช่อง และเข้าใจว่าทำไมการวัดกระแสผิดวิธีทำให้ฟิวส์ขาด, en: 'Insert the meter in series to measure current, move the leads to the right jack, and see why doing it wrong blows fuses.'}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m03.l01]
objectives:
- {th: วัดกระแสของหลอด LED หนึ่งดวงโดยต่อมัลติมิเตอร์อนุกรมและใช้ช่องเสียบที่ถูกต้อง, en: Measure one LED's current with the meter in series using the correct jack.}
- {th: อธิบายว่าทำไมการต่อมัลติมิเตอร์ในโหมดวัดกระแสคร่อมแหล่งจ่ายจึงอันตราย, en: Explain why connecting a meter in current mode across a supply is dangerous.}
- {th: เทียบกระแสที่วัดได้กับค่าที่คำนวณจากกฎของโอห์ม และอธิบายความต่าง, en: Compare measured current with the Ohm's-law calculation and explain the difference.}
develops:
- {skill: meas.multimeter, to: 2}
- {skill: hw.circuits, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: alpha
translation: done
slides: slides.md
source_sha256: 35c905322d643b356bc3f961d71c35633987706acdfe195ac3bc99404137bb68
---

## Objectives

By the end of this lesson you will:

1. Measure one LED's current with the meter in series, using the correct jack
2. Explain why connecting a meter in current mode across a supply is dangerous
3. Compare a measured current against the Ohm's-law calculation, and explain the difference

## Before you start

- You have completed [Measuring voltage and continuity](../l01-voltage-and-continuity/README.md), and can compute an LED's resistor (lesson [Basic components](../../m01-circuits/l03-components/README.md))
- For the lab: a red LED, a 270 Ω resistor (or 330 Ω) and a 1 kΩ resistor, a breadboard, jumper wires, a multimeter with an mA jack, and a board
- Open your meter's manual and find the current-mode specification page. Note the fuse rating for the mA jack and the A jack, and, if listed, the burden voltage

> **Safety.** The single most common way a multimeter gets destroyed is **forgetting to move the red lead back from the mA or A jack**, then using it to measure voltage.
> Make yourself a rule starting today: the moment you finish measuring current, move the red lead back to the VΩ jack immediately, before doing anything else.

## See it work first

Turn the meter over, or open its battery compartment (some models let you see the fuses without much unscrewing). See how many fuses there are, and what values are printed on them.
The mA jack usually has a small fuse rated a few hundred milliamps; the 10A jack usually has a separate, larger fuse — or, on some cheap models, no fuse at all on this jack.

These fuses exist for exactly one situation: someone connecting the meter in current mode the wrong way. Why is this mode more dangerous than the others? The answer is in section 2.

## Concepts

### 1. Measuring current means connecting in series

Current is the amount of charge flowing past one point. To measure it, all of that current must **flow through the meter itself** — meaning you must break the circuit at one point, and let the meter bridge that break.

<figure>
<svg viewBox="0 0 400 230" width="400" role="img" aria-label="The correct series connection for measuring current, versus the forbidden connection across a supply" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<path d="M50 22H70M60 22V30"/><text x="60" y="17" text-anchor="middle" fill="currentColor" stroke="none">3V3</text>
<path d="M60 30V40H120V52"/>
<circle cx="120" cy="70" r="18"/>
<text x="120" y="75" text-anchor="middle" font-weight="bold" fill="currentColor" stroke="none">A</text>
<text x="146" y="60" fill="currentColor" stroke="none">red → mA jack</text>
<text x="146" y="88" fill="currentColor" stroke="none">black → COM</text>
<path d="M120 88V100H60V110"/>
<polyline points="60,110 60,120 66,122.5 54,127.5 66,132.5 54,137.5 66,142.5 54,147.5 60,150 60,160"/>
<text x="44" y="140" text-anchor="end" fill="currentColor" stroke="none">R</text>
<path d="M60 160V173.0M52 173.0H68L60 185.0Z M52 185.0H68M60 185.0V200"/><path d="M71 174.0l7 -6m-4 0h4v4M71 181.0l7 -6m-4 0h4v4"/>
<path d="M60 200V208M50 208H70M54 212H66M58 216H62"/>
<path d="M290 22H310M300 22V30"/><text x="300" y="17" text-anchor="middle" fill="currentColor" stroke="none">3V3</text>
<path d="M300 30V52"/>
<circle cx="300" cy="70" r="18"/>
<text x="300" y="75" text-anchor="middle" font-weight="bold" fill="currentColor" stroke="none">A</text>
<path d="M300 88V140"/>
<path d="M300 140V148M290 148H310M294 152H306M298 156H302"/>
<path d="M270 40L330 100M330 40L270 100" stroke-width="3"/>
<text x="300" y="185" text-anchor="middle" fill="currentColor" stroke="none">never: ammeter across a supply</text>
<text x="300" y="202" text-anchor="middle" fill="currentColor" stroke="none">(≈ short circuit → fuse blows)</text>
</svg>
<figcaption>Left: to measure current, break the circuit and let current flow through the meter (in series). Right: never connect a current-mode meter across a supply — in this mode, the meter is almost a short circuit.</figcaption>
</figure>

The safe procedure:

1. Power off
2. Move the red lead to the mA jack (current within that jack's fuse rating) or the 10A jack (higher current, usable only for a limited time per the manual). Turn the dial to DC current mode.
3. If you do not know the expected current, start with the largest jack and range, then step down
4. Break the circuit at one point, and insert the meter in its place (red lead on the side current flows in from, black lead on the side it flows out to)
5. Power on, and read the value
6. Power off, remove the meter, reconnect the circuit, and **move the red lead back to the VΩ jack**

**A safer alternative: measure the voltage across a known resistor.** If the circuit already has a resistor of known value, measure the voltage across it and use Ohm's law, I = V_R / R.
No need to break the circuit, no need to move leads, and no way to blow a fuse. For example, reading 0.47 V across 100 Ω means 4.7 mA of current.
This is why industrial designs often include a low-value **shunt resistor** built into the circuit from the start, specifically for this purpose.

**An LED's current on a board.** You cannot cut a board's trace just to insert a meter in series. If the schematic gives the resistor value connected to the LED, and its pins are accessible, measure the voltage across it instead.
For a whole board's current draw, use a USB pass-through current meter designed for exactly this job, rather than cutting the USB cable.

### 2. Why current mode is dangerous

In current mode, the inside of the meter is a very low-value resistor (a shunt), designed to let current flow through easily, measuring the small voltage that develops across it.
The mA jack may have a total resistance of just a few ohms; the 10A jack may be as low as about a hundredth of an ohm. **In current mode, the meter is almost just a piece of wire.**

Consider what happens if you touch the current-mode leads across a supply, the way you would to measure voltage (the internal resistances below are assumed values, just to show the scale).

| Situation | Current that wants to flow | Result |
|---|---|---|
| The mA jack (assume 5 Ω) across a 3.3 V rail | 3.3 V / 5 Ω = 0.66 A | Far exceeds a several-hundred-mA fuse — it blows |
| The 10A jack (assume 0.01 Ω) across a 3.7 V lithium battery | Limited only by the battery's own internal resistance — possibly tens of amps | The leads get extremely hot; the battery can be damaged or catch fire |
| The A jack across mains power | Enormous | A severe arc flash — lethal. This is exactly why HRC fuses and CAT ratings exist |

The lesson: **whenever the red lead sits in the mA or A jack, never touch it across anything.** Insert the meter only in place of one wire in the circuit.
Lithium batteries deserve special caution — even at low voltage, they can supply an extremely high short-circuit current.

### 3. The measured value never quite matches the calculation — and you must be able to explain why

**The meter itself changes the circuit.** Its internal shunt causes a small voltage drop across the meter, called the **burden voltage**, so the circuit's current drops slightly once the meter is inserted.

**Example:** the red LED from an earlier lesson (3.3 V, V_f = 2.0 V, R = 270 Ω), calculated at 4.81 mA.
If the meter's mA jack has a total resistance of 10 Ω (an assumed value):

```text
I = 1.3 V / (270 + 10) Ω = 4.64 mA      about 3.6% lower than before
```

This effect grows larger when the circuit's own resistance is small. For example, a 100 Ω circuit at 3.3 V should draw 33 mA, but with a 10 Ω meter inserted, it drops to 3.3 / 110 = 30 mA — a 9% reduction.

**Other sources of difference worth remembering every time:**

- Resistor tolerance of ±5% means a "270 Ω" part could really be anywhere from 256.5 to 283.5 Ω, so the current could genuinely fall anywhere from 4.59 to 5.07 mA
- The real 3V3 rail is not exactly 3.30 V, and an LED's V_f depends on current and temperature, not a fixed 2.0 V
- The meter's own accuracy in current mode, which is often coarser than in voltage mode (check the manual)

The good habit is to **recalculate using the values you actually measured** (R from Ω mode, the 3V3 rail and V_f from voltage mode) before comparing against the meter's current reading.
If, even after that, the difference is larger than burden voltage and instrument accuracy can explain, something is genuinely wrong.

## Worked example

**Problem:** measure the current in the circuit 3V3 → 270 Ω → red LED → GND, two ways, and explain the difference (the numbers below are sample data, not what you must get).

1. **Measure the real values first.** Power off, measure the resistor: 268 Ω. Power on, measure 3V3: 3.29 V, and the LED's V_f: 1.98 V.
2. **Recalculate.** (3.29 − 1.98) V / 268 Ω = 4.89 mA.
3. **Method 1: measure the voltage across the resistor.** Get 1.31 V → 1.31 V / 268 Ω = 4.89 mA, matching the recalculation.
4. **Method 2: insert the meter in series** (power off, move the red lead to the mA jack, insert it in place of the wire between 3V3 and the resistor, power on). Reading: 4.71 mA.
5. **Explain.** This differs from method 1 by about 0.18 mA (3.6%). If the meter has an internal resistance of about 10 Ω, then (3.29 − 1.98) / (268 + 10) = 4.71 mA exactly.
   The entire difference is explained by the meter's burden voltage, not a fault in the circuit.
6. **Close out.** Power off, reconnect the circuit, and move the red lead back to the VΩ jack.

## Practice

1. You want to measure roughly 20 mA, and separately roughly 2 A. Which jack should the red lead use in each case?
2. A meter's mA jack has 5 Ω of internal resistance and a 400 mA fuse. If its leads accidentally touch across a 3.3 V rail, what current flows, and what happens?
3. A 3.3 V circuit with a 1 kΩ resistor — what current should flow? If a meter with 10 Ω internal resistance is inserted in series, what will it read, and what is the percent error?
4. Measuring 0.47 V across a 100 Ω resistor, what current is that?
5. An LED at 3.3 V has V_f = 2.0 V, with a 330 Ω ±5% resistor. What range will the current fall in?
6. After measuring current, you turn the dial to V⎓ but forget to move the red lead, then touch it across 3V3 and GND. What happens?

## Solution

1. 20 mA uses the mA jack; 2 A uses the 10A jack (or A), measuring for no longer than the manual's stated time limit.
2. 3.3 V / 5 Ω = 0.66 A, exceeding the 400 mA fuse — it blows. If the fuse does not blow in time, the supply may be short-circuited hard enough to overheat or be damaged.
3. 3.3 mA nominally; with the meter inserted, 3.3 V / 1010 Ω = 3.27 mA, about a 1% error. A circuit with this much resistance barely notices the meter.
4. 0.47 V / 100 Ω = 4.7 mA.
5. The resistor falls between 313.5 and 346.5 Ω. Current ranges from 1.3 V / 346.5 Ω = 3.75 mA to 1.3 V / 313.5 Ω = 4.15 mA (the nominal value is 3.94 mA).
6. The red lead is still in the mA jack, connected to a low-value shunt, not a voltage-measuring circuit. Turning the dial does not move the current path. The result is a short circuit of the 3V3 rail through the meter, and the fuse will likely blow. Many meters beep a warning when the leads sit in the current jack but the dial is set elsewhere — but never rely on that.

## Check your understanding

Answer at least 4 of the 5 questions in [quiz.yaml](quiz.yaml) correctly. Question 1 asks you to order a procedure — try ordering it in your head before looking at the choices.

## Lab

1. **Prepare.** With USB unplugged, wire 3V3 → 270 Ω (or 330 Ω) → a red LED → GND, leaving one gap between the 3V3 rail and the resistor (do not wire that connection yet).
2. **Measure the real values.** Measure the resistor in Ω mode before wiring it into the circuit.
3. **Guess.** Write down the current you expect, both using the nominal value and using your measured value.
4. **Method 1.** Wire a jumper to close the gap. Plug in USB. Measure 3V3, V_R and V_f. Compute the current from V_R / R.
5. **Method 2.** Unplug USB, remove the jumper that closed the gap, move the red lead to the mA jack, turn the dial to DC current mode. Connect the red lead to the 3V3 rail and the black lead to the resistor's pin. Plug in USB, and read the value.
6. **Close out immediately.** Unplug USB, remove the meter, and **move the red lead back to the VΩ jack** before moving on to the next step.
7. Change to 1 kΩ, and repeat steps 3 through 6.

| R | Calculated current (nominal) | Calculated current (measured values) | Method 1: V_R / R | Method 2: meter in series | Difference (%) |
|---|---|---|---|---|---|
| 270 Ω | 4.81 mA | | | | |
| 1 kΩ | 1.30 mA | | | | |

**Interpreting the results:** the percentage difference between method 1 and method 2 should be larger in the 270 Ω circuit than in the 1 kΩ circuit. If that is what you see, you have just watched burden voltage's effect with your own eyes.
If your meter's manual states its burden voltage (e.g. in mV per mA), try using it to estimate the mA jack's internal resistance, and predict method 2's result in advance.

## Going further

A multimeter answers "what is the average voltage or current?" very well, but it cannot see signals that change quickly. The next module, [Capturing your first digital signal](../../m04-logic-analyzer/l01-capture-a-signal/README.md),
uses a logic analyzer to watch signals changing thousands or millions of times a second.

## Reflect

Between measuring the voltage across a resistor and inserting the meter in series, which would you choose first in real work, and in what situation would you need the other one instead?

## References

- [Multimeter (Wikipedia)](https://en.wikipedia.org/wiki/Multimeter)
- [Lessons In Electric Circuits by Tony R. Kuphaldt (open book)](https://www.ibiblio.org/kuphaldt/electricCircuits/)
