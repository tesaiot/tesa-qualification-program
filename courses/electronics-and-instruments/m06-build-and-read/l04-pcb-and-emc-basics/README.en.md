---
id: elec.m06.l04
lang: en
title: {th: พื้นฐาน PCB และ EMC, en: PCB and EMC basics}
summary: {th: เข้าใจหลักการวางชิ้นส่วน กราวด์ และเส้นทางสัญญาณที่ลดปัญหาสัญญาณรบกวนและการแผ่คลื่น, en: 'Understand placement, grounding and routing principles that reduce noise and emissions.'}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m06.l03]
objectives:
- {th: อธิบายหน้าที่ของระนาบกราวด์และตัวเก็บประจุ decoupling ที่วางชิดขาไฟของชิป, en: Explain the ground plane and decoupling capacitors placed close to chip power pins.}
- {th: ระบุปัจจัยที่ทำให้บอร์ดแผ่คลื่นรบกวนหรือไวต่อสัญญาณรบกวนได้อย่างน้อยสามข้อ, en: Name at least three factors that make a board emit or pick up interference.}
- {th: อธิบายว่าทำไมผลิตภัณฑ์ที่มีวิทยุหรือไฟฟ้าต้องผ่านการทดสอบมาตรฐานก่อนวางขาย, en: Explain why products with radios or electronics must pass standards testing before sale.}
develops:
- {skill: hwdev.pcb-emc, to: 2}
- {skill: test.standards, to: 1}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: alpha
translation: done
source_sha256: 3216173fd19ade1ed0b10f8baddaaa4d714139be69054dd4cb675839f3c8482b
---

## Objectives

By the end of this lesson you will:

1. Explain the job of a ground plane and of decoupling capacitors placed close to a chip's power pins
2. Name at least three factors that make a board emit interference or be sensitive to it
3. Explain why a product containing a radio or electronics must pass standards testing before it can be sold

## Before you start

- You already understand decoupling (lesson [Basic components](../../m01-circuits/l03-components/README.md)), a probe's ground loop (lesson [Oscilloscope basics](../../m05-oscilloscope/l01-scope-basics/README.md)), and can read a schematic (the previous lesson)
- For the lab: a board, a magnifying glass or a phone camera, an oscilloscope with a probe
- This lesson is only a foundation. Real PCB design and EMC testing are specialist subjects that go far deeper. Our goal is to be able to read a board and ask the right questions.

## See it work first

Look closely at both sides of a board with a magnifying glass, or take close-up photos. Find these things:

- Many small capacitors sitting right next to the main chip
- Many small holes (vias), arranged in rows or spread across the board, especially around the edges and around any radio section
- Metal covers over components (shield cans), and an area with no copper around an antenna
- Small components right next to the USB connector (usually ESD protection parts or a ferrite bead)

Why does a designer add these things, when the schematic would still function without many of them? The answer is that a schematic tells you "what connects to what," but not "which way the current actually flows" —
and on a real board, the path current takes is everything.

## Concepts

### 1. Current must return: ground planes and decoupling

Every bit of current leaving a chip's pin along a trace must always flow all the way back to the chip through ground, completing a loop. At high frequency, the return current chooses the path with **the least inductance**,
which is the path directly underneath the signal trace, because that makes the loop's area as small as possible.

<figure>
<svg viewBox="0 0 400 155" width="400" role="img" aria-label="Return current flowing beneath a signal trace on a continuous ground plane, compared to a plane with a slot" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<rect x="20" y="20" width="160" height="110" rx="3" stroke-dasharray="4 3"/>
<text x="100" y="145" text-anchor="middle" fill="currentColor" stroke="none">solid ground plane</text>
<path d="M40 60H160" stroke-width="3"/>
<text x="40" y="52" fill="currentColor" stroke="none">signal</text>
<path d="M40 70H160" stroke-width="1.5" stroke-dasharray="4 3"/>
<text x="40" y="88" font-size="11" fill="currentColor" stroke="none">return current</text>
<rect x="220" y="20" width="160" height="110" rx="3" stroke-dasharray="4 3"/>
<text x="300" y="145" text-anchor="middle" fill="currentColor" stroke="none">plane with a slot</text>
<path d="M296 20V100M304 20V100" stroke-width="1"/>
<path d="M240 60H360" stroke-width="3"/>
<text x="240" y="52" fill="currentColor" stroke="none">signal</text>
<path d="M240 70H290V112H310V70H360" stroke-dasharray="4 3"/>
<text x="300" y="124" text-anchor="middle" font-size="10" fill="currentColor" stroke="none">detour = big loop</text>
</svg>
<figcaption>Left: a continuous ground plane — the return current runs directly beneath the signal trace, keeping the loop small. Right: a slot in the plane forces the current to detour, enlarging the loop, which emits and picks up more interference.</figcaption>
</figure>

A **ground plane** is a full copper layer inside the board (a four-layer board is often stacked as signal / ground / power / signal).
It lets return current run beneath every signal trace, keeping loops small and ground's own resistance and inductance low.
If the plane has a slot or is cut beneath a signal trace, the current must detour, and the loop grows immediately (right-hand picture). An easy rule to remember: **never route a fast signal trace across a gap in the ground plane.**

**Decoupling must sit close.** A real capacitor is not just capacitance — its package and the traces connecting it also carry inductance (ESL).

```text
A 100 nF capacitor with 1 nH of total inductance resonates at f0 = 1 / (2π √(1 nH × 100 nF)) ≈ 15.9 MHz
At 100 MHz: the ideal capacitor part has an impedance of 1 / (2π × 100 MHz × 100 nF) ≈ 0.016 Ω
            but the inductive part has 2π × 100 MHz × 1 nH ≈ 0.63 Ω — almost 40 times larger
```

Above its resonant frequency, a capacitor starts behaving like an inductor, so at high frequency **placement and loop length matter more than the capacitance value.**
An extra 5 mm of trace adds about 5 nH of inductance (a rough rule of about 1 nH per millimetre). If the current changes by 25 mA within 1 ns, the ripple voltage grows by 5 nH × 25 mA / 1 ns = 0.125 V.

<figure>
<svg viewBox="0 0 450 140" width="450" role="img" aria-label="A decoupling capacitor placed close to a chip's power pin, compared to placed far away" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<rect x="50" y="40" width="60" height="60" rx="3"/>
<text x="80" y="75" text-anchor="middle" fill="currentColor" stroke="none">IC</text>
<path d="M110 55H120"/>
<text x="114" y="50" font-size="10" fill="currentColor" stroke="none">VDD</text>
<path d="M110 85H120"/>
<text x="114" y="100" font-size="10" fill="currentColor" stroke="none">GND</text>
<path d="M120 55H160V64M152 64H168M152 70H168M160 70V85H120"/>
<text x="100" y="130" text-anchor="middle" fill="currentColor" stroke="none">close: small loop</text>
<rect x="260" y="40" width="60" height="60" rx="3"/>
<text x="290" y="75" text-anchor="middle" fill="currentColor" stroke="none">IC</text>
<path d="M320 55H330"/>
<text x="324" y="50" font-size="10" fill="currentColor" stroke="none">VDD</text>
<path d="M320 85H330"/>
<text x="324" y="100" font-size="10" fill="currentColor" stroke="none">GND</text>
<path d="M330 55H420V64M412 64H428M412 70H428M420 70V85H330"/>
<text x="310" y="130" text-anchor="middle" fill="currentColor" stroke="none">far: big loop</text>
</svg>
<figcaption>A decoupling capacitor must sit close to a chip's power pin — the smaller the loop between the power pin, the capacitor, and ground, the less inductance it carries.</figcaption>
</figure>

This is why a designer places a small capacitor right next to every power pin, drills the shortest possible vias down to the ground and power planes, and often combines several values together to cover multiple frequency ranges.

### 2. What makes a board emit or pick up interference

**EMC (electromagnetic compatibility)** is a device's ability to work in an electromagnetic environment without disturbing other devices beyond a limit (emission), and without malfunctioning when disturbed within a specified level (immunity).

| Factor | Why | Common fix |
|---|---|---|
| **A large loop area** | A loop is an antenna. For a small loop, the radiated field scales with current, loop area, and the square of frequency — and a large loop also picks up interference well | A continuous ground plane; keep the signal trace close to its return path |
| **A fast signal edge** | An edge rising within t_r spreads energy out to about 0.35 / t_r — for example, a 1 ns edge reaches about 350 MHz, even if the signal itself is only 1 MHz | Reduce output drive strength; add a small series resistor; use the slowest edge the application can tolerate |
| **A clock signal and its harmonics** | A 25 MHz square wave has odd harmonics at 75, 125, 175 MHz … | Keep the clock trace short, buried between planes; use a spread-spectrum clock if the chip supports one |
| **A cable acting as an antenna** | A cable about a quarter-wavelength long radiates and picks up well; a 1 m cable matches λ / 4 at 75 MHz | A ferrite bead or filter at the connector; a shielded cable grounded at the right point |
| **An unprotected connector** | Static electricity and interference enter through a connector first | A TVS diode, an RC filter, right at the connector |
| **A high-impedance point or a floating pin** | Easily picks up the ambient electric field (we already saw this in the floating-pin lesson) | A pull-up or pull-down; a filter at an ADC pin |
| **Insufficient or distant decoupling** | Supply ripple becomes interference for every chip sharing that rail | A capacitor close to the pin, several values, short vias |

### 3. Why testing is required before sale

Radio spectrum is a resource everyone shares. A single device emitting beyond its limit can disturb aviation radio, medical equipment, or a whole building's communication network.
And a device that cannot withstand static or ambient fields might malfunction at a dangerous moment. Countries therefore require products to pass testing before they can be sold.

- **EMC emissions**, such as the CISPR family of standards (CISPR 32 for multimedia and information technology equipment)
- **EMC immunity**, such as CISPR 35 and the IEC 61000-4-x test series (IEC 61000-4-2 is the electrostatic discharge test)
- **Radio.** Using radio spectrum must follow each country's own rules, such as ETSI EN 300 328 for the 2.4 GHz band in Europe, and FCC Part 15 in the United States.
  In Thailand, radio communication equipment falls under the NBTC (National Broadcasting and Telecommunications Commission)
- **Electrical safety**, such as IEC 62368-1 for audio, video and information technology equipment. In Thailand, some product categories must also meet mandatory TISI (Thai Industrial Standards Institute) standards

The exact list of standards a product must pass depends on the product category and the country of sale — always check with the relevant authority or an accredited test lab.
A commonly misunderstood point: **using a pre-certified radio module does not automatically certify the whole product.** The main board, wiring, power supply, and enclosure can all change the emission result on their own.
Experienced teams therefore run their own **pre-compliance** testing, with a near-field probe and a spectrum analyzer, starting from the earliest prototypes, because fixing a problem during design is far cheaper than fixing it after failing a formal test.

## Worked example

**Problem:** a team sends a prototype temperature sensor that reports over WiFi for testing. Emissions exceed the limit around 75 MHz and 125 MHz. Reviewing the design, they find:

1. A two-layer board, with the external memory's 25 MHz clock trace 6 cm long, routed across a slot cut into the ground plane to make room for a power trace
2. The main chip's decoupling capacitor sits about 15 mm from the power pin, connected by a thin trace
3. A 1 m USB cable connects directly to the connector, with no filter

**Analysis**

- 75 and 125 MHz are the 3rd and 5th harmonics of the 25 MHz clock, so the clock trace is the likely source
- The clock trace crosses the ground plane's slot, forcing the return current to detour — a large loop (the loop-area factor)
- A 1 m USB cable has λ / 4 landing exactly at 75 MHz, so any interference leaking onto the cable radiates well (the cable-antenna factor)
- Decoupling 15 mm away adds about 15 nH of inductance (the 1 nH-per-millimetre rule); above a few MHz, the capacitor barely helps anymore

**Fixes, in order of value for effort**

1. Re-route the clock trace to be short and never cross the slot, or close the slot and move to a four-layer board with a full ground plane
2. Add a 22 to 33 Ω series resistor right at the clock's source pin, or reduce drive strength, to slow the edge down
3. Move the decoupling capacitor right next to the power pin, using short vias down to the plane
4. Add a ferrite bead or a filter for USB, right at the connector

Then run pre-compliance with a near-field probe, comparing before and after the fix, before sending it for another round of formal testing.

## Practice

1. A 10 nF capacitor has 0.8 nH of total inductance. At what frequency does it resonate? Above that frequency, how does it behave?
2. A signal edge rises in 2 ns. To about what frequency does its energy spread?
3. A 0.5 m cable has λ / 4 landing at what frequency (using the speed of light, 3 × 10⁸ m/s)?
4. A 16 MHz clock is a square wave. At what frequencies do the three strongest harmonics fall?
5. Name three factors that make a board sensitive to interference (immunity), with a fix for each.
6. A company uses a pre-certified WiFi module and concludes the product needs no further EMC testing. How would you respond?

## Solution

1. f0 = 1 / (2π √(0.8 nH × 10 nF)) ≈ 56.3 MHz. Above this, its impedance is dominated by inductance — it behaves like an inductor, filtering less and less as frequency rises.
2. 0.35 / 2 ns = 175 MHz.
3. λ = 4 × 0.5 m = 2 m, so f = 3 × 10⁸ / 2 = 150 MHz.
4. A square wave (50% duty) carries only odd harmonics. The strongest is the fundamental, 16 MHz, followed by 48 MHz and 80 MHz.
5. For example: a floating pin or a high-impedance point (add a pull-up or pull-down); a long, unfiltered sensor cable (add an RC filter or a ferrite bead at the connector);
   an unprotected connector (add a TVS diode right at the connector); a large loop (a continuous ground plane); insufficient decoupling (a capacitor close to the pin).
6. A module's certification covers the module itself, under the conditions it was tested in. The main board, wiring, power supply, and enclosure can all emit and pick up interference on their own — the whole product still needs to pass EMC and safety testing per the requirements of whichever market it will be sold in.
   Radio requirements for the finished product must also be checked with that country's own authority.

## Check your understanding

Answer at least 4 of the 5 questions in [quiz.yaml](quiz.yaml) correctly.

## Lab

**Part A: read a board by eye.** Using a magnifying glass or close-up photos of your board (and its schematic, if available), fill in the table.

| What to find | Where / how many | What it does |
|---|---|---|
| Decoupling capacitors around the main chip | | |
| Vias arranged in a row (stitching vias) | | |
| A metal shield can | | |
| An antenna area with no copper | | |
| Protection parts or filters near the USB connector | | |
| Ferrite beads (marked FB on the schematic) | | |

**Part B: a loop is an antenna** (oscilloscope, no need to connect to the board)

1. Set the probe to 10×. Clip the probe's ground lead onto its own tip, forming the ground lead into a loop. **Do not touch the board.**
2. Set 20 mV/div, AC coupling, timebase about 1 µs/div, trigger mode Auto.
3. Hold the loop above a powered, running board (about 1 cm away), and slowly sweep it across the board — close to the main chip, close to the voltage regulator, and along the USB cable. Note where the signal is strongest.
4. Repeat with the loop squeezed smaller (coil the ground lead into a tighter loop), and compare the signal size at the same spot.
5. Conclude how loop size affects the picked-up signal, and connect this to why a ground spring gave a cleaner picture in the oscilloscope lesson.

**Part C (if time allows): noise on the supply rail.** Measure the 3V3 rail with AC coupling and a short ground lead, as in the lesson [Oscilloscope basics](../../m05-oscilloscope/l01-scope-basics/README.md),
while the board is lightly loaded, then compare against while the screen is updating or wireless is active. Record the peak-to-peak ripple voltage in both conditions.

## Going further

You have completed all six modules of this course. These skills carry straight over into courses that work with a real board, such as
[TESAIoT Firmware Stack](../../../tesaiot-firmware-stack/README.md), which writes C firmware for the TESAIoT Dev Kit.
Every time a program says "sent" or "read successfully," you now have the tools to prove for yourself whether that is really true.

## Reflect

If you were designing your own first product, which point from this lesson would you check first, right from component placement, and why?

## References

- [Printed circuit board (Wikipedia)](https://en.wikipedia.org/wiki/Printed_circuit_board)
- [Electromagnetic compatibility (Wikipedia)](https://en.wikipedia.org/wiki/Electromagnetic_compatibility)
- [Decoupling capacitor (Wikipedia)](https://en.wikipedia.org/wiki/Decoupling_capacitor)
