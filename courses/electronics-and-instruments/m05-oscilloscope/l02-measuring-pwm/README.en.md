---
id: elec.m05.l02
lang: en
title: {th: วัด PWM, en: Measuring PWM}
summary: {th: 'วัด period, ความถี่ และ duty cycle ของสัญญาณ PWM ที่หรี่หลอด LED และเทียบกับค่าที่โปรแกรมสั่ง', en: 'Measure period, frequency and duty cycle of the PWM dimming an LED and compare with the commanded value.'}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m05.l01]
objectives:
- {th: วัด period ความถี่ และ duty cycle ของ PWM จากรูปคลื่นได้, en: 'Measure PWM period, frequency and duty cycle from the waveform.'}
- {th: เทียบ duty cycle ที่วัดได้กับค่าที่โปรแกรมสั่ง และอธิบายเมื่อไม่ตรงกัน, en: Compare measured duty cycle with the commanded value and explain any mismatch.}
develops:
- {skill: meas.oscilloscope, to: 2}
- {skill: mcu.pwm, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: alpha
translation: done
source_sha256: 804067af189537d5837c79968066710a0c679daf16809fd7f8d9e8c68fc1e86b
---

## Objectives

By the end of this lesson you will:

1. Measure PWM's period, frequency, and duty cycle from a waveform
2. Compare a measured duty cycle against the commanded value, and explain any mismatch

## Before you start

- You can already set up an oscilloscope for a stable trace (lesson [Oscilloscope basics](../l01-scope-basics/README.md)), and time a signal with a logic analyzer (lesson [Capturing a first digital signal](../../m04-logic-analyzer/l01-capture-a-signal/README.md))
- A TESAIoT Dev Kit flashed with the [QWA309 Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) example, a two-channel oscilloscope (or logic analyzer), and a multimeter
- The lab's optional section uses the AIoT in Action course's MicroPython firmware, which has a `led.brightness()` command. If you do not have it, skip that section.

## See it work first

The AIoT in Action course has an example, [03_led_brightness.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s03/03_led_brightness.py),
that dims an LED with `led.brightness(pct)` and reads it back with `led.duty()`. In that example, there is a test that commands `on()` followed by `toggle()`.
The LED has gone dark, but `duty()` still answers the same number. The comment in the code sums it up: "duty() = what was commanded, not what is measured."

This is exactly this lesson's question: does the number the program reports match the signal actually coming out of the pin? We answer with measuring instruments, not by trusting the number on screen.

## Concepts

### 1. PWM's three numbers

**PWM (pulse-width modulation)** is a square wave with a fixed period, whose proportion of time spent at 1 can be adjusted.

<figure>
<svg viewBox="0 0 380 200" width="380" role="img" aria-label="PWM signals at the same frequency, with duty cycles of 25, 50 and 75 percent" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<polyline points="40,46 60,46 60,20 85,20 85,46 160,46 160,20 185,20 185,46 260,46 260,20 285,20 285,46 370,46"/>
<text x="30" y="46" text-anchor="end" fill="currentColor" stroke="none">25%</text>
<polyline points="40,96 60,96 60,70 110,70 110,96 160,96 160,70 210,70 210,96 260,96 260,70 310,70 310,96 370,96"/>
<text x="30" y="96" text-anchor="end" fill="currentColor" stroke="none">50%</text>
<polyline points="40,146 60,146 60,120 135,120 135,146 160,146 160,120 235,120 235,146 260,146 260,120 335,120 335,146 370,146"/>
<text x="30" y="146" text-anchor="end" fill="currentColor" stroke="none">75%</text>
<path d="M60 172V180M160 172V180M60 176H160"/>
<text x="110" y="192" text-anchor="middle" fill="currentColor" stroke="none">period T</text>
<text x="260" y="192" text-anchor="middle" fill="currentColor" stroke="none">duty D = t_high / T</text>
</svg>
<figcaption>These three PWM rows share the same period, differing only in the proportion of each period spent at 1 (the duty cycle).</figcaption>
</figure>

```text
Period       T = time from one rising edge to the next
Frequency    f = 1 / T
Duty cycle   D = t_high / T
Average voltage   V_avg = D × V_high     (when a load or filter circuit averages the signal)
```

**Example:** T = 2 ms, t_high = 0.5 ms, on a 3.3 V pin

```text
f = 1 / 2 ms = 500 Hz     D = 0.5 / 2 = 25%     V_avg = 0.25 × 3.3 V = 0.825 V
```

An LED driven by PWM fast enough appears to the eye as an average brightness (generally, above about 100 Hz most people no longer see flicker, though a phone camera may still show banding).
A multimeter in DC voltage mode also reads the average, as long as the period is much shorter than the meter's own averaging time. At a low frequency like 25 Hz, the number will bounce around instead.

### 2. Hardware PWM versus software PWM

**PWM from a hardware timer.** A counter counts up on a clock of frequency f_clk, restarting after reaching N; the pin is 1 while the count is still below a compare value.

```text
f_PWM = f_clk / N        D = compare / N        Duty resolution = 1 / N
```

**Example:** f_clk = 1 MHz, N = 1000 gives 1 kHz PWM with duty adjustable in steps of 0.1%.
Wanting 20 kHz from a 100 MHz clock gives N = 5000, with 0.02% resolution.
The register detail (whether you load N or N − 1) varies by hardware — on the PSoC, this block is called TCPWM; check the PDL documentation alongside it.
The TESAIoT Dev Kit's SDK notes that the RGB LED's dimming path wires its pin to a TCPWM0 signal, while the AIoT in Action course notes that an LED with no hardware PWM path
gets only a short pulse of about 12 ms, then goes dark, without holding its brightness.

**PWM from software.** The program writes the pin to 1, delays, writes it to 0, delays, and loops. The header test program's PWM Out button works this way
(writing P13.3 = 1, P13.4 = 0, delaying 20 ms, then swapping, for 50 cycles, per the example's code).
The advantage is that any pin works; the disadvantage is that the time taken by other instructions and interrupts leaks into the rhythm, so the period comes out slightly longer than set and can jitter,
and the CPU must not do anything else in the meantime.

**A complementary pair.** Driving a motor with an H-bridge uses two signals that are phase-inverted from each other, and these two signals **must never both be 1 at the same time.**
Otherwise the top and bottom transistors would both conduct at once, shorting the supply (shoot-through). Real systems leave a brief **dead time** where both lines are 0 before switching.

<figure>
<svg viewBox="0 0 400 150" width="400" role="img" aria-label="A complementary signal pair on pins P13.3 and P13.4" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<polyline points="70,50 90,50 90,20 140,20 140,50 190,50 190,20 240,20 240,50 290,50 290,20 340,20 340,50 380,50"/>
<text x="60" y="40" text-anchor="end" fill="currentColor" stroke="none">P13.3</text>
<polyline points="70,110 140,110 140,80 190,80 190,110 240,110 240,80 290,80 290,110 340,110 340,80 380,80"/>
<text x="60" y="100" text-anchor="end" fill="currentColor" stroke="none">P13.4</text>
<path d="M90 118V126M190 118V126M90 122H190"/>
<text x="140" y="140" text-anchor="middle" fill="currentColor" stroke="none">≈ 40 ms (2 × 20 ms)</text>
</svg>
<figcaption>The complementary pair from the header tester's PWM Out button: when one pin is 1, the other is 0, and they must never both be 1 at once (a both-high fault).</figcaption>
</figure>

### 3. Why a measured value can differ from the commanded one

| Cause | Symptom | Example |
|---|---|---|
| Counter resolution | Duty gets rounded to a step | N = 100, commanding 33.3% actually gives 33% |
| An off-by-one count | The period or duty is always off by one step | Loading N instead of N − 1 into the register |
| Software PWM | The period comes out longer than set, and jitters | Set 40 ms, measure 40.1 ms |
| Reversed polarity | The measured duty is 100% minus the commanded value | An active-low LED commanded 20% lights for 80% of the time |
| A number in the program that is not a measurement | The program reports the last commanded value | `duty()` still answers 100 after `toggle()` has turned the LED off |
| The pin is not connected to the hardware's PWM | You get a short pulse then nothing, or no signal at all | An LED with no PWM path |
| Measurement method | The pulse width comes out wrong when the edge is slow | Measuring at the 10% level instead of the 50% level of the voltage |

**How to measure accurately:**

- Measure pulse width at the **50% level** of the voltage (most instruments' automatic measurement uses this level)
- Measure several periods and average, or use the instrument's statistics (mean, min, max) — the min and max tell you how much jitter there is
- Time resolution must be finer than the duty resolution you want to check — to see a 0.1% step of a 1 kHz PWM (1 µs), you need to measure time more finely than 1 µs

## Worked example

**Problem:** measure the PWM from the PWM Out button, and compare it against what the code commands (half-period 20 ms, 50 cycles, P13.3 and P13.4 phase-inverted). The numbers below are sample data.

1. **The commanded value:** t_high = 20 ms, T = 40 ms, f = 25 Hz, D = 50%.
2. **Connect.** Channel 1 at P13.3, channel 2 at P13.4, both probe grounds at GND. Set 10 ms/div, 1 V/div, trigger on channel 1's rising edge at 1.65 V, mode Normal.
3. **Measure channel 1** (averaged over 10 periods): T = 40.10 ms, t_high = 20.05 ms.

```text
f = 1 / 40.10 ms = 24.94 Hz
D = 20.05 / 40.10 = 50.0%
The period is 0.10 ms (0.25%) longer than commanded
```

4. **Explain.** The duty matches the commanded value, but the period is a little longer, spread evenly across both halves — the signature of software PWM, where the time taken by the pin-write instructions and the loop leaks into every half-period.
5. **Check the complementary pair.** Zoom in on an edge where the two channels swap, and check whether there is any interval where both lines read 1. In the example's code, one pin is written to 1 just one instruction before the other is written to 0.
   If your instrument is fine enough, you may see an extremely brief overlap at one edge, every cycle. This is exactly why a real system must design dead time in hardware, not rely on instruction ordering.
6. **Count cycles.** Channel 1 must show exactly 50 pulses.

## Practice

1. A PWM has a 2 ms period and a 0.5 ms pulse width. Find its frequency, duty, and average voltage on a 3.3 V pin.
2. A 20 kHz PWM with 30% duty. Find its period and pulse width.
3. A timer uses a 10 MHz clock, and you want 10 kHz PWM. How many counts per period do you need? What compare value gives 33% duty, and how fine can duty be adjusted?
4. An LED is wired active-low (it lights when the pin is 0). The program commands 20% duty on the pin. For what percentage of the time is the LED lit?
5. A software PWM is set for a 40.0 ms period, but measures at 40.4 ms. What is the percent error, and what is the real frequency?
6. A timer has N = 100, and the program commands 12.34%. What duty will the hardware likely actually give?
7. A 3.3 V pin drives 40% duty PWM. What should a DC-voltage-mode multimeter read, roughly, if the frequency is high enough?

## Solution

1. f = 500 Hz, D = 25%, V_avg = 0.825 V
2. T = 1 / 20 kHz = 50 µs. Pulse width = 0.30 × 50 µs = 15 µs.
3. N = 10 MHz / 10 kHz = 1000. Compare value = 330. Resolution = 1 / 1000 = 0.1%.
4. The LED lights when the pin is 0, which is 100% − 20% = 80% of the time.
5. (40.4 − 40.0) / 40.0 = 1%. Frequency = 1 / 40.4 ms = 24.75 Hz.
6. 12 steps out of 100 is 12% (if the code truncates), off from the commanded value by 0.34 percentage points.
7. 0.40 × 3.3 V = 1.32 V.

## Check your understanding

Answer at least 4 of the 5 questions in [quiz.yaml](quiz.yaml) correctly.

## Lab

**Part A: PWM Out on P13.3 and P13.4.** Follow the worked example with your own real data, using an oscilloscope (or a logic analyzer at 100 kHz if you have no scope).

**Part B: PWM3 Out on P15.2 and P15.3.** Press the **PWM3 Out** button — the program drives the same kind of complementary pair on pins shared with the ADC. Measure the same way, and compare against Part A.

| | Commanded | P13.3 | P13.4 | P15.2 | P15.3 |
|---|---|---|---|---|---|
| Average period | 40 ms | | | | |
| Frequency | 25 Hz | | | | |
| t_high | 20 ms | | | | |
| Duty | 50% | | | | |
| Jitter (max T − min T) | 0 | | | | |
| Ever both 1 with its partner? | never | | | | |

**Part C: a multimeter and PWM.** Measure P13.3 in DC voltage mode while PWM Out is running. Record the number you see, and explain why it bounces around near 1.65 V instead of holding steady.

**Optional: LED PWM** (if you have the MicroPython firmware and a safely accessible test point)

1. Open the board's schematic. Find whether the RGB LED's pin, or a resistor connected to it, has a point you can safely probe. If not, stop here — never probe a chip's own pin.
2. If there is one, command `led.brightness(10)`, then `led.brightness(50)`, then `led.brightness(90)`, one at a time, and measure frequency and duty at that point.
3. Read `led.duty()` after each one, and compare it against what you measured. Remember to account for polarity (does the LED light when the pin is 1 or 0?) before drawing a conclusion.

## Going further

The next module begins with [Building a circuit on a breadboard](../../m06-build-and-read/l01-breadboarding/README.md), where we build a larger circuit correctly the first time,
checking it with every instrument we now know how to use, before ever applying power.

## Reflect

Which number in your own program reports "what was commanded" that you have previously read as "what actually happened" — and which instrument would you use to prove it?

## References

- [AIoT in Action: examples/s03/03_led_brightness.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s03/03_led_brightness.py)
- [Oscilloscope (Wikipedia)](https://en.wikipedia.org/wiki/Oscilloscope)
- [Pulse-width modulation (Wikipedia)](https://en.wikipedia.org/wiki/Pulse-width_modulation)
- [SDK: cm33/io/04_gpio_led_button.c (the RGB LED's pin and its TCPWM path)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c)
- [Code of QWA309 Header I/O Test (Developer Hub, commit 372d0d8)](https://github.com/tesaiot/developer-hub/blob/372d0d849578a6a49b634d3ecaab8b5958166921/prac_qwa309_header_hw_test/header_tester_ui.c)
