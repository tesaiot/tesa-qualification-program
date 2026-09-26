---
id: elec.m05.l01
lang: en
title: {th: ออสซิลโลสโคปเบื้องต้น, en: Oscilloscope basics}
summary: {th: 'ตั้ง timebase, volts/div และ trigger และต่อสายกราวด์ของโพรบให้ถูก', en: 'Set timebase, volts/div and trigger, and connect the probe ground properly.'}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m04.l02]
objectives:
- {th: 'ตั้ง timebase, volts/div และ trigger ให้เห็นสัญญาณนิ่งบนจอ', en: 'Set timebase, volts/div and trigger to get a stable trace.'}
- {th: อธิบายว่าทำไมสายกราวด์ของโพรบต้องต่อกับกราวด์ของวงจรและสั้นที่สุด, en: Explain why the probe ground must go to circuit ground and be as short as possible.}
- {th: อธิบายว่าออสซิลโลสโคปให้ข้อมูลอะไรที่ logic analyzer ให้ไม่ได้, en: Explain what an oscilloscope shows that a logic analyzer cannot.}
develops:
- {skill: meas.oscilloscope, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: alpha
translation: done
slides: slides.md
source_sha256: ffac453f04ff5f6223b39cd9d6c447cedd36f045581e7243bd36296622fe33c1
---

## Objectives

By the end of this lesson you will:

1. Set timebase, volts/div and trigger to get a stable trace on screen
2. Explain why the probe's ground lead must connect to the circuit's ground and be as short as possible
3. Explain what an oscilloscope shows that a logic analyzer cannot

## Before you start

- An oscilloscope (a lab bench model, or a USB one — either works), with a 10× probe and the ground spring that came with it, if available
- A TESAIoT Dev Kit flashed with the [QWA309 Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) example — we use the PWM Out button as our signal source
- If using the Eva Kit, use any pin where you generate a square wave with your own program
- Read the first few pages of your instrument's manual, and find its bandwidth (MHz), maximum sample rate, and the location of its probe compensation test terminal

> **Safety.** Most bench oscilloscopes connect the probe's ground clip straight to the power plug's earth pin.
> If you clip the ground lead onto a point that is not the circuit's ground, that point is instantly shorted to earth through the probe's cable. This course only measures low-voltage circuits sharing the same ground as the board.
> Never use an ordinary probe on mains circuits or floating-ground circuits — that work needs a differential probe and specific training.

## See it work first

Connect the probe to pin P13.3, connect ground to GND, then press **PWM Out** without setting anything at all yet (or press Auto Set, if your instrument has one).
The trace will very likely run around, sit as a flat line, or show only a blurry band — even though the real signal is a plain 25 Hz square wave.

An oscilloscope does not "know" what we want to look at. We must tell it three things: how wide a time window to show, which voltage range to show, and when to start drawing. These three things are this lesson's content.

## Concepts

### 1. The screen, channels, and three main controls

<figure>
<svg viewBox="0 0 420 220" width="420" role="img" aria-label="An oscilloscope screen with 10 horizontal and 8 vertical divisions, showing a square wave" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<rect x="20" y="15" width="340" height="176" rx="3"/>
<path d="M54 15V191" stroke-width="0.5" stroke-dasharray="4 3"/>
<path d="M88 15V191" stroke-width="0.5" stroke-dasharray="4 3"/>
<path d="M122 15V191" stroke-width="0.5" stroke-dasharray="4 3"/>
<path d="M156 15V191" stroke-width="0.5" stroke-dasharray="4 3"/>
<path d="M190 15V191" stroke-width="0.5" stroke-dasharray="4 3"/>
<path d="M224 15V191" stroke-width="0.5" stroke-dasharray="4 3"/>
<path d="M258 15V191" stroke-width="0.5" stroke-dasharray="4 3"/>
<path d="M292 15V191" stroke-width="0.5" stroke-dasharray="4 3"/>
<path d="M326 15V191" stroke-width="0.5" stroke-dasharray="4 3"/>
<path d="M20 37H360" stroke-width="0.5" stroke-dasharray="4 3"/>
<path d="M20 59H360" stroke-width="0.5" stroke-dasharray="4 3"/>
<path d="M20 81H360" stroke-width="0.5" stroke-dasharray="4 3"/>
<path d="M20 103H360" stroke-width="0.5" stroke-dasharray="4 3"/>
<path d="M20 125H360" stroke-width="0.5" stroke-dasharray="4 3"/>
<path d="M20 147H360" stroke-width="0.5" stroke-dasharray="4 3"/>
<path d="M20 169H360" stroke-width="0.5" stroke-dasharray="4 3"/>
<polyline points="20,147 54,147 54,74.4 122,74.4 122,147 190,147 190,74.4 258,74.4 258,147 326,147 326,74.4 360,74.4"/>
<text x="366" y="151" fill="currentColor" stroke="none">0 V</text>
<text x="366" y="78.4" fill="currentColor" stroke="none">3.3 V</text>
<text x="20" y="209" fill="currentColor" stroke="none">10 ms/div · 1 V/div · trigger ↑ 1.65 V</text>
<path d="M48 109.0l6 -6l6 6" stroke-width="2"/>
</svg>
<figcaption>Most screens are divided into 10 horizontal divisions (time) and 8 vertical divisions (voltage). This example is set to 10 ms/div, so the whole screen shows 100 ms, and a 40 ms-period wave shows about two and a half cycles.</figcaption>
</figure>

Most screens divide into **10 horizontal divisions** (time) and **8 vertical divisions** (voltage). The word "div" means one such square.

**Timebase (s/div)** is the time per horizontal division. The whole screen shows 10 × s/div.

```text
Wanting to see about two to three cycles of a 40 ms-period signal → need about 100 ms across the whole screen → 10 ms/div
Wanting to see one whole UART byte at 115200 (86.8 µs) → need about 100 µs → 10 µs/div
```

Available settings usually follow a 1-2-5 sequence (1, 2, 5, 10, 20, 50 …) — pick the smallest value that still shows everything you need.

**Volts/div (V/div)** is the voltage per vertical division. Set it so the signal fills roughly half to almost the whole screen.

```text
A 0 to 3.3 V signal at 1 V/div is 3.3 divisions tall; at 0.5 V/div it is 6.6 divisions tall (you must move the 0 V line down near the bottom edge)
```

Set the **probe attenuation** in the channel menu to match the switch on the probe itself (1× or 10×). If they do not match, the numbers on screen will be off by a factor of ten.

**Coupling.** DC coupling shows the full real voltage; AC coupling removes the DC part, leaving only what changes.
To see a small ripple on a 3.3 V rail, use AC coupling at 20 mV/div — with DC coupling at 20 mV/div, the trace would simply run off the screen.

### 2. Trigger: making the trace stand still

An oscilloscope redraws its trace many times per second. If each redraw starts at a different point on the wave, the trace runs. **Trigger** tells every redraw to start at the same point.

- **Source:** which channel decides (the channel carrying the signal)
- **Slope:** rising edge or falling edge
- **Level:** the voltage counted as the starting point — it must fall **within** the signal's swing; the middle of the range is safest, e.g. 1.65 V for 3.3 V logic
- **Mode:**
  - Auto draws a trace always, even without finding a trigger — good for finding a signal for the first time
  - Normal redraws only when it finds a trigger, holding the last trace when the signal stops — good for a signal that comes in bursts, like PWM Out, which only runs for about 2 s
  - Single captures once, then stops — good for a one-time event, such as a single button press's bounce

If the trace runs, check in order: is the source on the right channel, is the level within the signal's range, and does the mode fit the signal's behaviour.

### 3. Probes, ground, and what a logic analyzer cannot see

**A 10× probe** attenuates the signal by ten, in exchange for high input resistance (typically 10 MΩ) and low capacitance (tens of pF), so it disturbs the circuit less than a 1× probe.
Before use, it needs **compensation**: connect the probe to the instrument's test terminal (usually a roughly 1 kHz square wave), then turn the small adjuster on the probe until the top of the wave is exactly flat — neither peaked nor rounded.

**The ground lead must connect to the circuit's ground.** The probe tip measures voltage relative to the ground clip, and a bench instrument's ground clip is connected to earth through the power plug.
A board plugged into a computer that is itself plugged into a three-pin socket usually has its ground connected to earth too. Clipping the ground onto the 3V3 pin is the same as shorting 3V3 straight to ground.

**The ground lead must be short.**

<figure>
<svg viewBox="0 0 400 185" width="400" role="img" aria-label="A long probe ground lead forming a large loop, compared to a short ground spring" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<rect x="30" y="70" width="150" height="60" rx="3"/>
<text x="105" y="110" text-anchor="middle" fill="currentColor" stroke="none">board</text>
<rect x="60" y="14" width="60" height="18" rx="3"/>
<text x="90" y="10" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">probe</text>
<path d="M90 32V70"/>
<circle cx="90" cy="70" r="2.5" fill="currentColor"/>
<path d="M60 24C0 24 0 150 60 130"/>
<circle cx="60" cy="130" r="2.5" fill="currentColor"/>
<text x="64" y="146" font-size="11" fill="currentColor" stroke="none">GND clip</text>
<text x="105" y="175" text-anchor="middle" fill="currentColor" stroke="none">long ground lead = big loop</text>
<rect x="230" y="70" width="150" height="60" rx="3"/>
<text x="305" y="110" text-anchor="middle" fill="currentColor" stroke="none">board</text>
<rect x="260" y="14" width="60" height="18" rx="3"/>
<text x="290" y="10" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">probe</text>
<path d="M290 32V70"/>
<circle cx="290" cy="70" r="2.5" fill="currentColor"/>
<path d="M304 32V66"/>
<circle cx="304" cy="70" r="2.5" fill="currentColor"/>
<text x="310" y="52" font-size="11" fill="currentColor" stroke="none">GND spring</text>
<text x="305" y="175" text-anchor="middle" fill="currentColor" stroke="none">short ground spring = small loop</text>
</svg>
<figcaption>Left: a probe's long ground lead and its tip enclose a large loop, acting as an inductor and an antenna. Right: a short ground spring touching ground right next to the point being measured makes a small loop, so the edge shown matches reality far more closely.</figcaption>
</figure>

A probe's long ground lead and its tip enclose a loop. That loop has inductance (a rough rule is about 1 nH per millimetre of wire), and paired with the probe's own capacitance, it becomes a resonant circuit.

```text
f = 1 / (2π √(L × C))
A 15 cm ground lead ≈ 150 nH, with a 15 pF probe → f = 1 / (2π √(150 nH × 15 pF)) ≈ 106 MHz
A 1 cm ground spring ≈ 10 nH, with a 15 pF probe → f ≈ 411 MHz
```

Any edge fast enough excites this loop into ringing, so we see oscillation around 100 MHz at the edge that **does not exist on the board at all** — it is caused by our own way of measuring.
A ground spring pushes this frequency higher than most instruments' bandwidth, and its small loop also picks up less ambient noise.

**Bandwidth and rise time.** An instrument cannot show an edge faster than its own capability. A rule of thumb is t_r ≈ 0.35 / BW.
A 100 MHz instrument shows an edge no faster than about 3.5 ns. If the real edge is 5 ns, you would see about √(5² + 3.5²) = 6.1 ns.

**An oscilloscope versus a logic analyzer**

| Question | Which instrument answers it |
|---|---|
| What is the real voltage of level 1? Is there overshoot or ringing? | Oscilloscope |
| Is I2C's rising edge slow because the pull-up is too large? Does level 0 reach V_OL? | Oscilloscope |
| How much does the supply rail ripple? Are there spikes when a load switches? | Oscilloscope |
| Analogue signals, such as a knob's voltage or audio | Oscilloscope |
| The event sequence of 8 to 16 pins together, over many seconds | Logic analyzer |
| Decoding a long I2C or UART capture | Logic analyzer (many scopes can too, but usually capture for less time) |

The two instruments do not replace each other. A logic analyzer answers "what happened, and when." An oscilloscope answers "what does the signal actually look like."

## Worked example

**Problem:** set up the instrument to get a stable trace of the PWM Out signal (P13.3, 0 to 3.3 V, about 25 Hz, running about 2 s per press), then measure its voltage and period.

1. **Probe.** Set the switch to 10×, set the channel menu to 10×, and compensate the probe against the test terminal first.
2. **Connect.** Ground clip (or ground spring) at the header's GND, as close to P13.3 as possible; probe tip at P13.3.
3. **Vertical.** DC coupling, 1 V/div, move the 0 V line to the second division from the bottom — the signal will be 3.3 divisions tall.
4. **Horizontal.** The period is 40 ms; wanting about two and a half cycles → 10 ms/div (100 ms across the whole screen).
5. **Trigger.** Source channel 1, rising edge, level 1.65 V, mode Normal, because the signal comes in a burst.
6. **Press PWM Out.** The trace stands still while the signal runs, and holds the last trace once the signal stops.
7. **Measure.** Use the cursors or the automatic measurement function to read the peak voltage (should be close to the 3V3 voltage measured with a multimeter), the period, and the frequency.
8. **Zoom the edge.** Set the trigger to Single, change the timebase to nanosecond scale appropriate for your instrument's bandwidth (e.g. 10 ns/div), press PWM Out again, and look at the shape of the first rising edge.

## Practice

1. You want to see a 1 kHz wave, at least two full cycles, on a 10-division screen. What timebase should you use (from the 1-2-5 series)?
2. A 0 to 5 V signal should be at least half the screen tall (4 divisions) without overflowing the 8-division screen. What volts/div should you use?
3. A probe's switch is set to 10×, but the instrument's channel menu is set to 1×. Measuring a 3.3 V signal, what will it read?
4. An instrument with 50 MHz bandwidth shows a rise time no faster than about how much?
5. A ground loop has 100 nH of inductance, and the probe has 10 pF of capacitance. At about what frequency will you see ringing?
6. Match each question to the right instrument: (a) decoding a 5 s I2C capture (b) does SCL ring after its falling edge? (c) how much does the 3V3 rail ripple? (d) do 12 pins of a parallel bus change in the right order?

## Solution

1. Two cycles is 2 ms; you need exactly 0.2 ms per division (2 ms across the whole screen). For extra margin, use 0.5 ms/div to see 5 cycles.
2. 1 V/div makes the signal 5 divisions tall (0.5 V/div would be 10 divisions, overflowing; 2 V/div would be only 2.5 divisions).
3. The probe attenuates by ten, but the instrument does not multiply it back, so it reads about 0.33 V.
4. 0.35 / 50 MHz = 7 ns.
5. f = 1 / (2π √(100 nH × 10 pF)) ≈ 159 MHz.
6. (a) logic analyzer  (b) oscilloscope  (c) oscilloscope (AC coupling)  (d) logic analyzer

## Check your understanding

Answer at least 4 of the 5 questions in [quiz.yaml](quiz.yaml) correctly.

## Lab

1. **Compensate the probe.** Connect it to the instrument's test terminal, adjust until the top of the wave is exactly flat, and photograph the screen three times (under-compensated, correct, and over-compensated).
2. **A stable trace.** Follow steps 1 through 7 of the worked example, and record the values in the table.
3. **Deliberately make the trace run.** Set the level to 5 V (outside the signal's range), or change the source to a channel with no signal. See what happens in Auto and Normal modes, then set it back.
4. **Long ground versus short ground.** Zoom in on the rising edge in Single mode.
   Measure first with the long ground clip lead that came with the probe, then measure again with a ground spring (or the shortest ground lead you can manage) touching GND right next to the point being measured.
   Record the overshoot size and ringing frequency for both.
5. **Work backwards.** Using the measured ringing frequency and the probe's capacitance from the manual, find the ground loop's inductance, L = 1 / ((2π f)² × C).
   For example, ringing at 80 MHz with a 15 pF probe gives L ≈ 264 nH; compare this against your ground lead's length using the rule of thumb of 1 nH per millimetre.
   If the ringing is too fast for your instrument's bandwidth to show, record that your instrument cannot tell this apart, and explain why.
6. **Supply rail.** Measure the 3V3 pin with AC coupling, 20 mV/div, timebase 1 ms/div. Record the peak-to-peak ripple voltage. Try turning the 20 MHz bandwidth limiter on and off (if your instrument has one), and compare.

| Measurement | Result |
|---|---|
| P13.3's level-1 voltage | |
| Period and frequency | |
| Overshoot with the long ground lead | |
| Overshoot with the short ground | |
| Ringing frequency with the long ground lead, and the calculated L | |
| 3V3's ripple voltage (peak to peak) | |

## Going further

The next lesson, [Measuring PWM](../l02-measuring-pwm/README.md), uses both the oscilloscope and the logic analyzer to measure period and duty cycle,
and compares them against what the program commanded, to see whether they really match.

## Reflect

In lab step 4, which picture would you trust as the signal's true shape on the board, and how would you explain your reasoning to someone who only ever uses a long ground lead?

## References

- [Oscilloscope (Wikipedia)](https://en.wikipedia.org/wiki/Oscilloscope)
- [Lessons In Electric Circuits by Tony R. Kuphaldt (open book)](https://www.ibiblio.org/kuphaldt/electricCircuits/)
