---
id: elec.m04.l01
lang: en
title: {th: จับสัญญาณดิจิทัลครั้งแรก, en: Capturing a first digital signal}
summary: {th: ต่อ logic analyzer เลือกอัตราสุ่มตัวอย่างและ trigger แล้ววัดเวลาของสัญญาณ, en: 'Connect a logic analyzer, choose sample rate and trigger, and time the signal.'}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m03.l02]
objectives:
- {th: ต่อสายกราวด์และสายสัญญาณของ logic analyzer กับบอร์ดได้ถูกต้อง, en: Connect the logic analyzer's ground and signal leads to the board correctly.}
- {th: เลือกอัตราสุ่มตัวอย่างที่เร็วพอสำหรับสัญญาณที่ต้องการวัด และอธิบายผลเมื่อช้าเกินไป, en: Choose a sample rate fast enough for the signal and explain what happens when it is too slow.}
- {th: วัดความกว้างพัลส์และความถี่ของสัญญาณไฟกะพริบจากภาพที่จับได้, en: Measure pulse width and frequency of a blink signal from a capture.}
develops:
- {skill: meas.logic-analyzer, to: 2}
- {skill: sys.dsp, to: 1}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: alpha
translation: done
slides: slides.md
source_sha256: ef6d053edd152c43f76eccf2da203add9d76ea37d8c4856578236100af489a4b
---

## Objectives

By the end of this lesson you will:

1. Connect a logic analyzer's ground and signal leads to a board correctly
2. Choose a sample rate fast enough for the signal you want to measure, and explain what happens when it is too slow
3. Measure a blink signal's pulse width and frequency from a capture

## Before you start

- An inexpensive logic analyzer that works with sigrok (many models use the [fx2lafw](https://sigrok.org/wiki/Fx2lafw) driver), with leads and clips
- [PulseView](https://sigrok.org/wiki/PulseView) installed on your computer — plug the device in and check that the program can see it
- A TESAIoT Dev Kit flashed with the [QWA309 Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) example, which generates a signal for us to measure on the header
- If using the Eva Kit, write a program that blinks a spare pin at a rhythm you know, e.g. 250 ms on, 250 ms off, and measure that pin instead

> **Instrument safety.** Most inexpensive logic analyzers have no ground isolation — their ground is your computer's ground.
> Never connect one to a circuit whose ground is not the same as your computer's, or to a circuit carrying mains power, and always check the device's maximum input voltage spec before use.

## See it work first

Run the header test program and press the **PWM Out** button. The screen states it is driving P13.3 and P13.4 as a phase-inverted pair, for 50 cycles, half-period 20 ms, "approximately 25 Hz."
If you have an LED with a 1 kΩ resistor wired to pin P13.3 (as in the lesson [Basic components](../../m01-circuits/l03-components/README.md)), you will see it blink so fast it almost looks solidly lit, for about two seconds.

Your eyes can only tell you "it blinks fast" — they cannot answer whether it is really 25 Hz, whether every pulse is the same width, or whether all 50 cycles actually happened.
A multimeter cannot answer either, because it averages the value. The instrument that can answer is a logic analyzer.

## Concepts

### 1. How a logic analyzer works, and how to connect it

A logic analyzer reads each channel's voltage at a fixed rhythm, compares it against a threshold, and stores it as 0 or 1 in time order. The program on your computer draws the result as a square waveform.
It has no idea what the real voltage is — only whether it is above or below the threshold (to see the real voltage, you need an oscilloscope, in Module 5).

**Ground first, always.** Voltage is the difference between two points. A logic analyzer's signal channels measure relative to its own GND lead.
If GND is not connected to the board's GND, the instrument has no reference point, and the result will be garbage or a flat line, even if the signal lead is connected correctly.
The right order is: connect GND → connect the signal lead → open the program, and disconnect in reverse.

**Voltage levels must match.** Check the spec to confirm the instrument's input threshold can read a 3.3 V signal (almost every model can). For 1.8 V signals, some models can read them, while others sit close enough to the threshold to be unreliable.

**Choosing which pin to probe.** Probe or clip only header pins or test points, using a clip designed to grip a pin. Never let a bare metal lead tip touch a neighbouring pin.

### 2. Sample rate, and when it is too slow

The **sample rate (f_s)** is how many times per second the device reads. The gap between two samples is T_s = 1 / f_s, which is the **time resolution** you can measure with.
An edge that happens between two samples will only be seen at the next sample, so a measured pulse width can be off by about one T_s.

**How fast is fast enough?** The Nyquist–Shannon sampling theorem says a signal with maximum frequency f must be sampled faster than 2f to be reconstructed.
But timing a digital signal needs more than that. A common rule of thumb is **at least 4 samples across the narrowest pulse**, and 10 or more samples if you want to time it accurately.

| Signal | Narrowest interval | Suitable sample rate |
|---|---|---|
| The header test program's 25 Hz PWM | 20 ms | 10 kHz is already enough (0.1 ms resolution, or 0.25% of the 40 ms period) |
| UART at 115200 baud | 1 bit = 1 / 115200 = 8.68 µs | 1 MHz gives 8.7 samples per bit; 4 MHz is more comfortable |
| I2C at 400 kHz | SCL's high or low half is about 1.25 µs | 4 to 10 MHz |

**If it is too slow**, two symptoms appear.

- **Missing pulses.** A pulse narrower than T_s can fall entirely between two samples, and the device never sees it at all.
- **Aliasing.** A fast signal, sampled too slowly, looks like a slower signal that does not really exist.

<figure>
<svg viewBox="0 0 380 180" width="380" role="img" aria-label="A fast signal sampled too slowly, appearing as a slower signal that is not really there" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<polyline points="20,70 30,70 30,30 40,30 40,70 50,70 50,30 60,30 60,70 70,70 70,30 80,30 80,70 90,70 90,30 100,30 100,70 110,70 110,30 120,30 120,70 130,70 130,30 140,30 140,70 150,70 150,30 160,30 160,70 170,70 170,30 180,30 180,70 190,70 190,30 200,30 200,70 210,70 210,30 220,30 220,70 230,70 230,30 240,30 240,70 250,70 250,30 260,30 260,70 270,70 270,30 280,30 280,70 290,70 290,30 300,30 300,70 310,70 310,30 320,30 320,70 330,70 330,30 340,30 340,70 350,70 350,30 360,30 360,70 360,70"/>
<text x="20" y="20" fill="currentColor" stroke="none">signal on the wire (fast)</text>
<path d="M22 82V90" stroke-width="1"/>
<circle cx="22" cy="70" r="2.5" fill="currentColor"/>
<path d="M44 82V90" stroke-width="1"/>
<circle cx="44" cy="70" r="2.5" fill="currentColor"/>
<path d="M66 82V90" stroke-width="1"/>
<circle cx="66" cy="70" r="2.5" fill="currentColor"/>
<path d="M88 82V90" stroke-width="1"/>
<circle cx="88" cy="70" r="2.5" fill="currentColor"/>
<path d="M110 82V90" stroke-width="1"/>
<circle cx="110" cy="30" r="2.5" fill="currentColor"/>
<path d="M132 82V90" stroke-width="1"/>
<circle cx="132" cy="30" r="2.5" fill="currentColor"/>
<path d="M154 82V90" stroke-width="1"/>
<circle cx="154" cy="30" r="2.5" fill="currentColor"/>
<path d="M176 82V90" stroke-width="1"/>
<circle cx="176" cy="30" r="2.5" fill="currentColor"/>
<path d="M198 82V90" stroke-width="1"/>
<circle cx="198" cy="30" r="2.5" fill="currentColor"/>
<path d="M220 82V90" stroke-width="1"/>
<circle cx="220" cy="70" r="2.5" fill="currentColor"/>
<path d="M242 82V90" stroke-width="1"/>
<circle cx="242" cy="70" r="2.5" fill="currentColor"/>
<path d="M264 82V90" stroke-width="1"/>
<circle cx="264" cy="70" r="2.5" fill="currentColor"/>
<path d="M286 82V90" stroke-width="1"/>
<circle cx="286" cy="70" r="2.5" fill="currentColor"/>
<path d="M308 82V90" stroke-width="1"/>
<circle cx="308" cy="70" r="2.5" fill="currentColor"/>
<path d="M330 82V90" stroke-width="1"/>
<circle cx="330" cy="30" r="2.5" fill="currentColor"/>
<path d="M352 82V90" stroke-width="1"/>
<circle cx="352" cy="30" r="2.5" fill="currentColor"/>
<polyline points="22,150 44,150 44,150 66,150 66,150 88,150 88,150 110,150 110,110 132,110 132,110 154,110 154,110 176,110 176,110 198,110 198,110 220,110 220,150 242,150 242,150 264,150 264,150 286,150 286,150 308,150 308,150 330,150 330,110 352,110 352,110"/>
<text x="20" y="170" fill="currentColor" stroke="none">what a too-slow sample rate shows (a slower, wrong signal)</text>
</svg>
<figcaption>Top: the real signal on the wire, with dots marking each sample. Bottom: the picture the device draws from those dots — its frequency is wrong. This is aliasing.</figcaption>
</figure>

**Example:** a 1 kHz square wave is sampled at 1.1 kHz. Each sample lands 1000 / 1100 = 0.909 cycles further along the wave —
equivalent to slipping backward by 0.091 cycles each time. The result completes one full cycle every 11 samples, giving 1100 / 11 = **100 Hz.** This false frequency equals |1100 − 1000| Hz.
The picture looks clean and convincing — this is exactly why aliasing is dangerous. It never looks like a mistake.

**Memory.** Number of samples = f_s × capture time. Sampling at 1 MHz for 5 s gives 5 million samples per channel.
Setting the rate higher than necessary wastes memory and shortens how long you can capture. A device that streams over USB continuously may not sustain its top rate when many channels are enabled at once.

### 3. Trigger, and timing measurements

A **trigger** is a condition that tells the device "start capturing here" — for example, a rising edge on channel 0. The device waits until the condition is true, then captures samples around that point.
This means you never have to press start in time for the event, and the event lands in the same position every time you capture.

**Measuring time from a capture.** Use the program's time-measurement tool (cursors or markers), placed on the signal's edges.

```text
Pulse width (t_high)  = the falling edge's time − the previous rising edge's time
Period (T)             = the next rising edge's time − the first rising edge's time
Frequency (f)           = 1 / T
Duty cycle              = t_high / T
```

Measuring several periods and dividing by the count is more accurate than measuring a single period, because the roughly one-T_s error at each edge also gets divided by the number of periods.

## Worked example

**Problem:** capture the signal from the header test program's PWM Out button, then measure its frequency, pulse width, and count its cycles.

1. **Know what to expect first.** From the on-screen description, the half-period is 20 ms, so the period is about 40 ms, frequency about 25 Hz, duty about 50%, for 50 cycles, lasting about 2 s total.
   P13.4 should be phase-inverted from P13.3 the whole time.
2. **Connect the leads.** The device's GND to the header's GND, channel 0 to P13.3, channel 1 to P13.4.
3. **Choose a sample rate.** The narrowest interval is 20 ms; at 10 kHz, that gives 200 samples across it — 0.1 ms resolution, more than enough.
4. **Choose a capture time.** At least 3 s, to cover the signal's 2 s, giving 10 kHz × 3 s = 30,000 samples per channel.
5. **Set the trigger** to channel 0's rising edge. Press Run in the program, then press PWM Out on screen.
6. **Measure** (the following numbers are sample data). The first rising edge is at 0 ms; the 11th rising edge is at 401.0 ms.
   Average period = 401.0 / 10 = 40.10 ms. Frequency = 1 / 40.10 ms = 24.94 Hz. The first pulse's width is 20.05 ms; duty = 20.05 / 40.10 = 50.0%.
7. **Interpret.** The period is 0.1 ms (0.25%) longer than 40 ms, because the program generates the signal by writing the pin and delaying in software — every cycle picks up a small extra amount of time from other instructions.
   If your device's 0.1 ms resolution is too coarse to tell this difference apart, raise the sample rate to 100 kHz and measure again.
8. **Count the cycles.** Use a decoder, or count rising edges — you must get exactly 50 edges, and channels 0 and 1 must never both be 1 at the same time, anywhere.

## Practice

1. To capture UART at 115200 baud with at least 8 samples per bit, what sample rate do you need at minimum?
2. Sampling at 1 MHz for 5 s, using 8 channels — how many samples per channel does the device need to store, and how many in total?
3. A 900 Hz square wave is sampled at 1 kHz. What frequency will you see in the result?
4. In a capture, rising edges are at 12.0 ms and 52.1 ms, with a falling edge between them at 32.0 ms. Find the period, frequency, pulse width, and duty cycle.
5. A signal has a pulse 3 µs wide, sampled at 200 kHz. What happens? What should you change it to?
6. If you forget to connect the logic analyzer's GND lead, what would the result probably look like, and why?

## Solution

1. 115200 × 8 = 921,600 samples per second — use 1 MHz (giving 8.7 samples per bit)
2. 1 MHz × 5 s = 5 million samples per channel; across 8 channels, 40 million total
3. |1000 − 900| = 100 Hz
4. Period = 52.1 − 12.0 = 40.1 ms. Frequency = 1 / 40.1 ms = 24.9 Hz. Pulse width = 32.0 − 12.0 = 20.0 ms. Duty = 20.0 / 40.1 = 49.9%.
5. The 5 µs gap between samples is wider than the 3 µs pulse — the pulse might vanish entirely, or show as just a single sample. You need at least 4 samples per pulse, i.e. 4 / 3 µs ≈ 1.33 MHz; choose 2 MHz or higher (10 samples per pulse would use about 4 MHz).
6. The result would be garbage, or a flat, unchanging line, or something that shifts as you move the wire — because the signal channel has no shared reference point with the board, so the voltage the device sees is not the signal's voltage relative to the board's GND.

## Check your understanding

Answer at least 4 of the 5 questions in [quiz.yaml](quiz.yaml) correctly.

## Lab

**Part A: a slow blinking signal (GPIO Out)**

1. Connect the device's GND to the header's GND, then connect channels 0 through 5 to P13.0, P13.3, P13.4, P13.5, P13.6, P13.7 in order (if your device has fewer channels, use just the first two pins).
2. Set the sample rate to 10 kHz, capture time 20 s, and trigger on channel 0's rising edge.
3. Press Run, then press **GPIO Out** on screen. The program drives each pin to 1 in turn, about 0.7 s each, in sequence, then turns everything off — repeated three times.
4. **Guess** before looking at the result: will each pin's pulse width be longer than 700 ms, or shorter, and why? (Hint: look at the example's code for what runs between the two delay calls.)
5. Measure channel 0's pulse width across all three rounds, and the time from channel 0's rising edge to channel 1's rising edge. Record it in the table.

**Part B: a faster signal (PWM Out)**

1. Connect channel 0 to P13.3 and channel 1 to P13.4. Follow the worked example, measure the average period across 10 periods, the frequency, the pulse width, and count the cycles.
2. **Deliberately make it too slow.** Lower the sample rate to the lowest your device allows, and capture again. If your device is still too fast to show an effect on a 25 Hz signal,
   calculate instead at what sample rate the problem would start to show, and what you would see.
3. Try PulseView's **Timing** decoder (if your version has it), which shows the time between edges automatically — compare it against your own manual measurement.

| Measurement | Expected | Measured |
|---|---|---|
| P13.0's pulse width (GPIO Out) | about 0.7 s | |
| Rising edge of P13.0 to rising edge of P13.3 | about 0.7 s | |
| Average period across 10 periods (PWM Out) | about 40 ms | |
| Frequency | about 25 Hz | |
| P13.3's duty cycle | about 50% | |
| Number of cycles | 50 | |
| Any interval where P13.3 and P13.4 are both 1? | none | |

## Going further

The next lesson, [Decoding I2C and UART](../l02-decode-i2c-and-uart/README.md), has the program read a signal's meaning for us — from a device's address on the I2C bus, to the bytes travelling on a UART wire.

## Reflect

In Part A, did you guess correctly whether the pulse would be longer or shorter than 700 ms? What does this tell you about generating timing with software delays?

## References

- [sigrok PulseView](https://sigrok.org/wiki/PulseView)
- [Logic analyzer (Wikipedia)](https://en.wikipedia.org/wiki/Logic_analyzer)
- [AIoT in Action: examples/s03/02_led_blink.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s03/02_led_blink.py)
- [Nyquist–Shannon sampling theorem (Wikipedia)](https://en.wikipedia.org/wiki/Nyquist%E2%80%93Shannon_sampling_theorem)
- [Code of QWA309 Header I/O Test (Developer Hub, commit 372d0d8)](https://github.com/tesaiot/developer-hub/blob/372d0d849578a6a49b634d3ecaab8b5958166921/prac_qwa309_header_hw_test/header_tester_ui.c)
