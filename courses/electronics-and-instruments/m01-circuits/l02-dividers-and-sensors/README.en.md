---
id: elec.m01.l02
lang: en
title: {th: วงจรแบ่งแรงดันและเซนเซอร์แบบอนาล็อก, en: Voltage dividers and analog sensors}
summary: {th: เข้าใจลูกบิดบนบอร์ดในฐานะวงจรแบ่งแรงดัน และแปลงค่าที่ ADC อ่านได้เป็นโวลต์, en: Understand the board's knob as a voltage divider and convert ADC counts to volts.}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m01.l01]
objectives:
- {th: คำนวณแรงดันขาออกของวงจรแบ่งแรงดันจากค่าตัวต้านทานสองตัว, en: Compute the output of a voltage divider from two resistor values.}
- {th: แปลงค่าที่ ADC อ่านได้เป็นแรงดันจากความละเอียดและแรงดันอ้างอิง แล้วเทียบกับมัลติมิเตอร์, en: 'Convert ADC counts to volts from resolution and reference, and compare with a multimeter.'}
- {th: อธิบายผลของความต้านทานขาเข้าของ ADC ต่อความแม่นยำของวงจรแบ่งแรงดัน, en: Explain how ADC input impedance affects divider accuracy.}
develops:
- {skill: hw.circuits, to: 2}
- {skill: mcu.adc-dac, to: 2}
- {skill: sys.sensors-actuators, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: alpha
translation: done
source_sha256: 8ebee8fd25f72f442ae577f189a56156d44ca4efb6bbffee66877b5e756da811
---

## Objectives

By the end of this lesson you will:

1. Compute the output voltage of a voltage divider from two resistor values
2. Convert an ADC reading to a voltage from its resolution and reference voltage, and compare it against a multimeter
3. Explain how the input resistance of an ADC (and of a meter) affects a voltage divider's accuracy

## Before you start

- You have completed the [Voltage, current and resistance](../l01-voltage-current-resistance/README.md) lesson, and can use Ohm's law and series circuits
- For the lab: a breadboard, jumper wires, a 10 kΩ resistor, a 12 kΩ resistor, two 1 MΩ resistors, a multimeter, and a board
- The part reading a knob through the ADC uses the Developer Hub's QWA309 example, which runs only on the TESAIoT Dev Kit. If you are using the Eva Kit, see the note in the lab.

## See it work first

If you have a TESAIoT Dev Kit, open the [QWA309 Potentiometer Monitor example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_pot_monitor&q=prac_qwa309_pot_monitor) and flash it to the board.
The screen shows four cards, one per potentiometer (knob), each with a raw count, a voltage, and a percentage. Turn one knob all the way in both directions and notice two things.

- The raw count runs from about 0 to about 4095 — why this particular number?
- The maximum voltage the screen shows is about 1.8 V, not 3.3 V — why?

Per this example's README, all four knobs are wired to pins P15.4 through P15.7 and read with a 12-bit SAR ADC, reference voltage 1.8 V.
By the end of this lesson, you will be able to explain every number on that screen yourself.

## Concepts

### 1. The voltage divider

Two resistors in series across a supply produce a midpoint voltage proportional to the supply voltage — this is called a **voltage divider.**

<figure>
<svg viewBox="0 0 440 222" width="440" role="img" aria-label="A voltage divider feeding an ADC pin, and a potentiometer as an adjustable voltage divider" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<path d="M60 22H80M70 22V30"/><text x="70" y="17" text-anchor="middle" fill="currentColor" stroke="none">V_in</text>
<path d="M70 30V40"/>
<polyline points="70,40 70,50 76,52.5 64,57.5 76,62.5 64,67.5 76,72.5 64,77.5 70,80 70,90"/>
<text x="86" y="70" fill="currentColor" stroke="none">R1 (top)</text>
<path d="M70 90V110M70 100H150"/>
<circle cx="70" cy="100" r="2.5" fill="currentColor"/>
<rect x="150" y="88" width="70" height="24" rx="3"/>
<text x="185" y="105" text-anchor="middle" fill="currentColor" stroke="none">ADC pin</text>
<text x="110" y="94" text-anchor="middle" fill="currentColor" stroke="none">V_out</text>
<polyline points="70,110 70,120 76,122.5 64,127.5 76,132.5 64,137.5 76,142.5 64,147.5 70,150 70,160"/>
<text x="86" y="140" fill="currentColor" stroke="none">R2 (bottom)</text>
<path d="M70 160V168M60 168H80M64 172H76M68 176H72"/>
<text x="20" y="210" fill="currentColor" stroke="none">V_out = V_in × R2 / (R1 + R2)</text>
<path d="M320 22H340M330 22V30"/><text x="330" y="17" text-anchor="middle" fill="currentColor" stroke="none">1.8 V</text>
<path d="M330 30V60"/>
<polyline points="330,60 330,85 336,87.5 324,92.5 336,97.5 324,102.5 336,107.5 324,112.5 330,115 330,140"/>
<path d="M370 100L339 100M345.4 97.3L339 100L345.4 102.7"/>
<path d="M370 100H390"/>
<text x="394" y="104" fill="currentColor" stroke="none">wiper</text>
<path d="M330 140V170"/>
<path d="M330 170V178M320 178H340M324 182H336M328 186H332"/>
<text x="318" y="104" text-anchor="end" fill="currentColor" stroke="none">pot</text>
</svg>
<figcaption>Left: a two-resistor voltage divider. Right: a potentiometer is a voltage divider whose middle pin (the wiper) can slide.</figcaption>
</figure>

The same current flows through R1 and R2 (they are in series): I = V_in / (R1 + R2). So the voltage across R2 is I × R2.

```text
V_out = V_in × R2 / (R1 + R2)
```

**Example:** 3.3 V, R1 = 10 kΩ (top), R2 = 4.7 kΩ (bottom)

```text
V_out = 3.3 × 4.7 / (10 + 4.7) = 3.3 × 0.3197 = 1.055 V
```

**Working backwards:** you want 1.8 V from 3.3 V. The ratio you need is 1.8 / 3.3 = 0.545.
Choose R1 = 10 kΩ, and R2 = 12 kΩ gives exactly 3.3 × 12 / 22 = 1.800 V. We will actually wire this 10 kΩ / 12 kΩ pair in the lab.

**A potentiometer (knob)** is a resistor with a sliding middle pin (the wiper). Its two end pins sit across a supply, so the middle pin is a voltage divider whose ratio you can adjust.
Turn it 30% of its travel, and the middle pin gives about 30% of the voltage across it. The knob's total resistance value has no effect on the ratio, as long as nothing loads it by drawing current (that is section 3's topic).

Many analogue sensors use exactly this principle — a thermistor (resistance changes with temperature), or an LDR (resistance changes with light).
Put it in place of R1 or R2, and the midpoint voltage changes with whatever quantity you want to measure.

### 2. The ADC: from voltage to a number, and back

An **N-bit ADC (analog-to-digital converter)** splits the range from 0 to a reference voltage (V_ref) into 2^N steps, giving a number from 0 to 2^N − 1.

- A 12-bit ADC has 2^12 = 4096 steps, so raw values fall in the range 0 to 4095
- The size of one step (1 LSB) = V_ref / 2^N

**Example:** a 12-bit ADC with V_ref = 1.8 V (the kind used to read a knob on the TESAIoT Dev Kit)

```text
1 LSB = 1.8 V / 4096 = 0.000439 V ≈ 0.44 mV
```

Converting a raw count back to a voltage:

```text
V = raw × V_ref / 2^N
raw 2048 → 2048 × 1.8 / 4096 = 0.900 V   (exactly half of the full range)
raw 3000 → 3000 × 1.8 / 4096 = 1.318 V
```

Some code divides by 4095 instead of 4096. The Pot Monitor example uses `POT_ADC_FULL_SCALE` = 4095 and computes in whole millivolts.
So raw 3000 gives 3000 × 1800 / 4095 = 1318 mV (rounded down). The two approaches differ by less than one LSB, far smaller than the resistor tolerances already present in the circuit.
What matters is knowing which one the code you are using has chosen.

**Percentage does not need a reference voltage.** Percentage = 100 × raw / full-scale is a pure ratio.
Voltage, on the other hand, depends directly on V_ref. If the real V_ref differs from what the code assumes, the calculated voltage is off by that same proportion, while the percentage stays correct.
The TESAIoT Dev Kit's SDK notes this exact caveat in its CM33 example that reads a knob: the function that converts to volts "multiplies by a hard-coded 3.3 V," not a measured real V_ref.
This is exactly why we need to compare against a multimeter at least once.

### 3. When the voltage divider is loaded

The formula in section 1 works when nothing draws current out of V_out — but in real life, something always does: the ADC pin, and the multimeter itself.
Looking from the V_out pin, the voltage divider behaves like a supply V_th with an internal resistance R_th = R1 ∥ R2 (a Thévenin equivalent circuit).

<figure>
<svg viewBox="0 0 340 140" width="340" role="img" aria-label="The Thévenin equivalent of a loaded voltage divider" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<circle cx="30" cy="60" r="14"/>
<text x="30" y="64" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">V_th</text>
<path d="M30 46V30H60M30 74V110"/>
<polyline points="60,30 75,30 77.5,24 82.5,36 87.5,24 92.5,36 97.5,24 102.5,36 105,30 120,30"/>
<text x="90" y="20" text-anchor="middle" fill="currentColor" stroke="none">R_th = R1 ∥ R2</text>
<path d="M120 30H190M190 30V45"/>
<circle cx="190" cy="30" r="2.5" fill="currentColor"/>
<text x="200" y="34" fill="currentColor" stroke="none">V_out</text>
<polyline points="190,45 190,55 196,57.5 184,62.5 196,67.5 184,72.5 196,77.5 184,82.5 190,85 190,95"/>
<text x="206" y="75" fill="currentColor" stroke="none">R_load (ADC, meter)</text>
<path d="M190 95V110M30 110H190"/>
<path d="M110 110V118M100 118H120M104 122H116M108 126H112"/>
</svg>
<figcaption>Looking from the V_out pin, the voltage divider behaves like a supply V_th with internal resistance R1 ∥ R2. Whatever load you connect divides the voltage once again.</figcaption>
</figure>

The load you connect divides the voltage one more time:

```text
V_out = V_th × R_load / (R_load + R_th)
```

**Example:** 3.3 V divided by two 100 kΩ resistors gives 1.65 V unloaded, and R_th = 100 kΩ ∥ 100 kΩ = 50 kΩ.

| Load | V_out | Error from 1.65 V |
|---|---|---|
| 1 MΩ | 1.65 × 1 M / 1.05 M = 1.571 V | −4.8% |
| 10 MΩ (a typical multimeter) | 1.65 × 10 M / 10.05 M = 1.642 V | −0.5% |

A rule of thumb worth remembering: make the load's resistance at least about 100 times R_th, and the error stays below about 1%.

**A SAR ADC has one more thing to consider.** While sampling, the ADC connects a **sampling capacitor** to the pin, and that capacitor must charge through R_th quickly enough before conversion happens.
Suppose the internal capacitor is 5 pF (a value assumed for this calculation — check the chip's datasheet for the real one), with R_th = 50 kΩ.

```text
τ = R × C = 50 kΩ × 5 pF = 250 ns
To settle within half an LSB of 12 bits, you need about ln(2^13) ≈ 9 τ ≈ 2.25 µs
```

If the ADC's sampling time is shorter than this, the reading comes out slightly low, and it shifts depending on the previous reading.
There are three fixes: lower the resistor values (at the cost of wasted current — two 10 kΩ resistors at 3.3 V draw 165 µA continuously), lengthen the sampling time,
or add a small capacitor at the ADC pin as a local charge reserve. For high accuracy, insert a voltage-follower op-amp in between.

## Worked example

**Problem:** a sensor outputs 0 to 5 V, and we want to read it with a 12-bit ADC that accepts 0 to 1.8 V (V_ref = 1.8 V). Design a voltage divider, then convert the reading back to the sensor's voltage.

**Step 1: choose a ratio.** 5 V must come down below 1.8 V, with some margin. Choose a ratio of 1/3, with R1 = 20 kΩ, R2 = 10 kΩ.

```text
V_adc max = 5 × 10 / (20 + 10) = 1.667 V    below 1.8 V, with about 7% headroom
```

**Step 2: check the side effects**

```text
Current the circuit draws from the 5 V sensor = 5 V / 30 kΩ = 0.167 mA
R_th = 20 kΩ ∥ 10 kΩ = 6.67 kΩ   a 10 MΩ load causes only about 6.67 k / 10 M ≈ 0.07% error
Resolution on the sensor's side = 0.44 mV × 3 = 1.32 mV per step
```

If the sensor can supply only very little current, 0.167 mA may be too much — check its datasheet. This is the trade-off between current and accuracy.

**Step 3: convert back.** A reading of raw = 3500.

```text
V_adc    = 3500 × 1.8 / 4096 = 1.538 V
V_sensor = V_adc × (R1 + R2) / R2 = 1.538 × 3 = 4.614 V
```

**Step 4: compare against a meter.** Measure the sensor's output voltage with a multimeter. If it differs from 4.614 V by more than about 1%, suspect these three things in order:
the resistors' real values (measured in Ω mode, powered off), the real V_ref, and the ADC's sampling time.

## Practice

1. A 3.3 V supply, R1 = 4.7 kΩ (top), R2 = 10 kΩ (bottom). What is V_out?
2. You want 1.2 V from 3.3 V, using R2 = 10 kΩ as the bottom resistor. What must R1 be? Using the nearest standard E24 value, what voltage do you actually get?
3. A 12-bit ADC, V_ref = 1.8 V. (a) How many volts is raw 1024? (b) How many volts is the maximum raw value, 4095? Why does it not reach exactly 1.8 V?
4. A 10-bit ADC, V_ref = 3.3 V. How many mV is one LSB, and roughly what raw value would 1.0 V give?
5. A voltage divider of two 1 MΩ resistors from 3.3 V, measured with a meter whose input resistance is 10 MΩ — what would it read? Compare this against the two-100-kΩ example with a 1 MΩ load in section 3, and notice something.
6. A 12-bit ADC reads raw 2867, and the code uses a full scale of 4095. What percentage is that?

## Solution

1. V_out = 3.3 × 10 / 14.7 = 2.245 V ≈ 2.24 V
2. R1 = R2 × (V_in / V_out − 1) = 10 kΩ × (3.3 / 1.2 − 1) = 10 kΩ × 1.75 = 17.5 kΩ. The nearest E24 value is 18 kΩ, giving 3.3 × 10 / 28 = 1.179 V.
3. (a) 1024 × 1.8 / 4096 = 0.450 V  (b) 4095 × 1.8 / 4096 = 1.7996 V. The maximum is one LSB (0.44 mV) below V_ref, because the count starts at 0.
4. 1 LSB = 3.3 V / 1024 = 3.22 mV, and 1.0 V × 1024 / 3.3 = 310.3, so raw is about 310.
5. R_th = 500 kΩ, giving 1.65 × 10 M / 10.5 M = 1.571 V — exactly the same as the section 3 example, because the ratio R_load / R_th is 20 in both cases. The error depends on this ratio, not on the absolute values.
6. 100 × 2867 / 4095 = 70.0%

## Check your understanding

Answer at least 4 of the 5 questions in [quiz.yaml](quiz.yaml) correctly. Questions 4 and 5 test loading effects — if you get them wrong, go back and reread section 3.

## Lab

**Part A: a voltage divider on a breadboard** (any board)

1. With USB unplugged, connect R1 = 10 kΩ from 3V3 to point M, and R2 = 12 kΩ from point M to GND.
2. **Guess:** write down the voltage you expect at point M (1.80 V, if 3V3 is exactly 3.30 V).
3. Plug in USB. Measure the real 3V3 voltage and the voltage at point M. Recalculate using the real 3V3 voltage you measured, and compare.
4. Unplug USB, and change both resistors to 1 MΩ. Guess first what you will measure, then plug in USB and measure point M.
5. **Investigate:** the value you measured in step 4 is probably noticeably below half of 3V3. Use the formula in section 3 to work backwards and find your meter's input resistance.

```text
R_meter = R_th × V_measured / (V_th − V_measured)      where V_th = 3V3 / 2 and R_th = 500 kΩ
Example: measured 1.571 V from a V_th of 1.650 V → R_meter = 500 k × 1.571 / 0.079 ≈ 9.9 MΩ
```

Resistor tolerance (±5%) can shift the result by several more percent, so it is worth measuring the real value of both 1 MΩ resistors first (before wiring them in, and not while holding the leads with your fingers),
then using V_th = 3V3 × R2 / (R1 + R2) and R_th = R1 ∥ R2 from your measured values.
Compare the result against your meter's manual (most are around 10 MΩ in DC voltage mode). If they are close, you have just measured the "measuring instrument" using itself.

**Part B: reading a knob through the ADC** (TESAIoT Dev Kit)

1. Run the [QWA309 Potentiometer Monitor](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_pot_monitor&q=prac_qwa309_pot_monitor) example, and turn one knob to four positions: roughly 1/4, 1/2, 3/4, and all the way.
2. At each position, record the raw value and the mV value the screen shows, then calculate it yourself with raw × 1800 / 4095. Your number must match the screen. If it does not, find what the code does differently from what you assumed.
3. If you can reach the knob's middle pin (for example, from a pin underneath the board), measure the middle pin's voltage relative to GND with a multimeter, and compare it against what the ADC reports. If you cannot reach it, skip this step — never probe a chip's pins on a powered board.
4. If you want to see the value change over time as a graph, try the [QWA309 4-Channel ADC Scope](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_adc_scope&q=prac_qwa309_adc_scope) example, which reads all four knobs every 60 ms and plots them as a line graph.

| Position | raw | mV on screen | mV calculated by hand | Meter (if measured) |
|---|---|---|---|---|
| about 1/4 | | | | |
| about 1/2 | | | | |
| about 3/4 | | | | |
| all the way | | | | |

**If you are using the Eva Kit:** the SDK has a C example for CM33 that reads a knob on the Eva Kit as a 16-bit raw value (0 to 65535), a percentage, and a voltage, computed by multiplying against an assumed 3.3 V.
Compare the voltage the code reports against a multimeter, and explain the difference using the V_ref discussion in section 2.

## Going further

The next lesson, [Basic components](../l03-components/README.md), applies Ohm's law to an LED, looks at what capacitors and diodes actually do,
and chooses a transistor for when a microcontroller pin cannot supply enough current. If you want to go on to read a knob from C code on the TESAIoT Dev Kit, see the lesson
[Analog and ADC in the TESAIoT Firmware Stack course](../../../tesaiot-firmware-stack/m04-qwa309-hardware/l02-analog-and-adc/README.md).

## Reflect

Next time you see a voltage number on some device's screen, what will you ask yourself before trusting that number?

## References

- [AIoT in Action: examples/s05/05_adc_counts_to_volts.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s05/05_adc_counts_to_volts.py)
- [AIoT in Action: examples/s05/03_pot_setpoint_deadband.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s05/03_pot_setpoint_deadband.py)
- [SDK: cm33/io/03_read_potentiometers.c (raw, percent and volts)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/03_read_potentiometers.c)
- [Lessons In Electric Circuits by Tony R. Kuphaldt (open book)](https://www.ibiblio.org/kuphaldt/electricCircuits/)
- [README of QWA309 Potentiometer Monitor (Developer Hub, commit 372d0d8)](https://github.com/tesaiot/developer-hub/blob/372d0d849578a6a49b634d3ecaab8b5958166921/prac_qwa309_pot_monitor/README.md)
- [Voltage divider (Wikipedia)](https://en.wikipedia.org/wiki/Voltage_divider)
