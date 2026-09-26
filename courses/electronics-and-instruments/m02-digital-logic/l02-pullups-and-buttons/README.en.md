---
id: elec.m02.l02
lang: en
title: {th: 'Pull-up, pull-down และปุ่มกด', en: 'Pull-ups, pull-downs and buttons'}
summary: {th: ต่อปุ่มแบบ active-low ด้วย pull-up และเห็นการเด้งของหน้าสัมผัสจริงบน logic analyzer, en: Wire an active-low button with a pull-up and see real contact bounce on a logic analyzer.}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m02.l01]
objectives:
- {th: อธิบายว่าทำไมขาเข้าที่ไม่มี pull-up หรือ pull-down จึงอ่านค่าไม่แน่นอน, en: Explain why an input without a pull-up or pull-down reads unpredictably.}
- {th: ต่อปุ่มแบบ active-low และอธิบายว่าทำไมกดแล้วอ่านได้ 0, en: Wire an active-low button and explain why pressing reads 0.}
- {th: วัดระยะเวลาการเด้งของปุ่มด้วย logic analyzer แล้วเลือกเวลากันเด้งจากข้อมูลที่วัดได้, en: Measure bounce duration with a logic analyzer and choose a debounce time from the data.}
develops:
- {skill: hw.digital, to: 2}
- {skill: mcu.gpio, to: 2}
- {skill: meas.logic-analyzer, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: alpha
translation: done
slides: slides.md
source_sha256: a00816fdb9a0b7f6c065772ddce23356c3816fc030dc7d73c1f8b8403e2f118a
---

## Objectives

By the end of this lesson you will:

1. Explain why an input pin with no pull-up or pull-down reads unpredictably
2. Wire an active-low button, and explain why pressing it reads 0
3. Measure a button's bounce duration with a logic analyzer, and choose a debounce time from the measured data

## Before you start

- You know V_IH and V_IL from the lesson [Logic levels and basic gates](../l01-logic-levels-and-gates/README.md)
- For the lab: a TESAIoT Dev Kit flashed with the [QWA309 Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) example,
  a breadboard, one leaded push button (tactile switch), a 10 kΩ resistor and a 1 kΩ resistor, a multimeter, and an inexpensive logic analyzer that works with [PulseView](https://sigrok.org/wiki/PulseView)
- This is the first lesson to use a logic analyzer. The steps in the lab are enough for this task; details on sampling rate live in the lesson [Capturing your first digital signal](../../m04-logic-analyzer/l01-capture-a-signal/README.md)

## See it work first

Run the header test program and press the **GPIO In** button, with **nothing at all connected to the header.**
The program sets pins P13.0, P13.3, P13.4, P13.5, P13.6, P13.7 as no-pull (high-Z) inputs, reads every 100 ms for 8 s, and prints the mask value every time it changes.

While it runs, try touching those pins with a finger, or holding a jumper wire (connected on one end only) near them, and watch whether the mask changes.
On some boards the value visibly bounces around; on others it sits steady at 0 even with nothing connected. Both tell you the same thing: **a reading from a floating pin cannot be trusted.**
Steady today does not mean steady tomorrow — not when a hand is nearby, or when a neighbouring wire changes state.

## Concepts

### 1. Floating pins: an input nobody tells a value

A CMOS input has extremely high input resistance, with leakage current in the nA to µA range. With nothing connected, an input pin behaves like a tiny capacitor that nobody controls.
Charge from a finger, a signal from a neighbouring wire, or the electric field around you can push its voltage anywhere, including into the unguaranteed range between V_IL and V_IH.
When the voltage sits in the middle, the transistors inside the input circuit can end up partially conducting on both sides at once, drawing more current than normal. So a floating pin is both unpredictable and wasteful of power.

The fix is to always give an input a "default value."

- **Pull-up:** a resistor from the pin to the supply. With nothing driving it, the pin reads 1.
- **Pull-down:** a resistor from the pin to GND. With nothing driving it, the pin reads 0.

This resistor must be "weak" enough that another device (or a button) can easily override it, and "strong" enough that noise cannot.

Most microcontrollers have a pull-up and pull-down built into the chip, enabled from software; its real value must be checked in the datasheet (the tolerance is often wide).
On the PSoC, this uses drive mode `CY_GPIO_DM_PULLUP`, and the SDK's `cm33/io/04_gpio_led_button.c` example warns of one detail worth remembering:
the out-value passed to `Cy_GPIO_Pin_FastInit()` must be 1, because in this mode that value is what actually enables the pull-up. Send 0, and the pin reads 0 permanently, as if the button were held down forever.
The Developer Hub's Button Monitor example calls `Cy_GPIO_Pin_FastInit(..., CY_GPIO_DM_PULLUP, 1UL, HSIOM_SEL_GPIO)`, following exactly this rule.

### 2. An active-low button, and choosing a pull-up value

<figure>
<svg viewBox="0 0 380 206" width="380" role="img" aria-label="An active-low button with a pull-up resistor and a series protection resistor" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<path d="M70 22H90M80 22V30"/><text x="80" y="17" text-anchor="middle" fill="currentColor" stroke="none">3V3</text>
<path d="M80 30V40"/>
<polyline points="80,40 80,50 86,52.5 74,57.5 86,62.5 74,67.5 86,72.5 74,77.5 80,80 80,90"/>
<text x="96" y="62" fill="currentColor" stroke="none">R_pu</text>
<text x="96" y="76" fill="currentColor" stroke="none">10 kΩ</text>
<path d="M80 90V110M80 100H130"/>
<circle cx="80" cy="100" r="2.5" fill="currentColor"/>
<polyline points="130,100 140,100 142.5,94 147.5,106 152.5,94 157.5,106 162.5,94 167.5,106 170,100 180,100"/>
<text x="155" y="90" text-anchor="middle" fill="currentColor" stroke="none">1 kΩ</text>
<path d="M180 100H220"/>
<circle cx="223" cy="100" r="3"/>
<text x="232" y="104" fill="currentColor" stroke="none">input pin (P13.0)</text>
<text x="72" y="104" text-anchor="end" fill="currentColor" stroke="none">BTN_N</text>
<path d="M80 110V124.0"/><circle cx="80" cy="124.0" r="2.5"/><path d="M80 140.0V154"/><circle cx="80" cy="140.0" r="2.5"/><path d="M79 138.0L68 122.0"/>
<text x="96" y="136" fill="currentColor" stroke="none">SW</text>
<path d="M80 154V162M70 162H90M74 166H86M78 170H82"/>
<text x="20" y="196" fill="currentColor" stroke="none">released: pin = 1 (3.3 V)   pressed: pin = 0 (0 V)</text>
</svg>
<figcaption>An active-low button: released, the pull-up holds the pin at 1. Pressed, the switch connects the pin to ground, making it 0. The 1 kΩ series resistor protects the pin in case the program accidentally sets it as an output.</figcaption>
</figure>

- **Released:** the switch is open, no current flows through R_pu, the voltage across R_pu is zero, so the pin equals 3.3 V and reads 1.
- **Pressed:** the switch connects the pin directly to GND, the pin is 0 V and reads 0, and current flows through R_pu at 3.3 V / R_pu.

"Pressed means 0" is why this is called **active-low.** In code we write `pressed = !pin`, or compare against a constant the BSP provides, such as `CYBSP_BTN_PRESSED` (whose value is 0).
Why is this so common? GND is everywhere on a board, so a switch connecting to GND never needs to route the supply rail out to the button — and this same principle is the basis of open-drain buses like I2C in Module 4.

**Choosing R_pu** balances three competing concerns.

| R_pu | Current while pressed (3.3 V / R) | Rising-edge speed (τ = R × 10 pF) | Voltage drop from 1 µA leakage |
|---|---|---|---|
| 1 kΩ | 3.3 mA (wasteful) | 10 ns | 1 mV |
| 10 kΩ | 0.33 mA | 100 ns | 10 mV |
| 100 kΩ | 33 µA | 1 µs | 0.1 V |
| 1 MΩ | 3.3 µA | 10 µs | 1 V (leaving the pin at 2.3 V) |

The 10 pF pin/trace capacitance and the 1 µA leakage current in the table are assumed values, just to show the trend — check the real numbers in the datasheet.
The last row is worth noticing: at 1 MΩ, leakage current leaves the pin at 3.3 − 1.0 = 2.3 V, below the rule-of-thumb V_IH of 2.31 V (0.7 × VDD). The pin might not reliably read as 1 even while the button is released.
For a typical button, a value anywhere from about 4.7 kΩ to 47 kΩ is safe on every front — **10 kΩ is the most commonly used value.**

**The 1 kΩ series resistor at the pin** in the figure is not needed for the button to work — it is insurance. If the program accidentally sets the pin as an output driving 1, and someone presses the button at that moment,
the pin would be shorted directly to GND. This resistor limits that current to no more than 3.3 V / 1 kΩ = 3.3 mA. We will always include it in the lab.

### 3. Contact bounce, and choosing a debounce time

The metal contacts inside a button do not touch just once — they strike and bounce apart several times in a very short window before settling. This is called **contact bounce.**

<figure>
<svg viewBox="0 0 380 185" width="380" role="img" aria-label="A button signal bouncing several times before settling at zero" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<polyline points="20,40 100,40 100,110 108,110 108,40 113,40 113,110 124,110 124,40 128,40 128,110 141,110 141,40 144,40 144,110 150,110 150,40 360,40"/>
<path d="M100 125V135M150 125V135M100 130H150"/>
<text x="125" y="150" text-anchor="middle" fill="currentColor" stroke="none">bounce</text>
<text x="20" y="30" fill="currentColor" stroke="none">pin (released = 1)</text>
<text x="300" y="102" text-anchor="middle" fill="currentColor" stroke="none">pressed = 0</text>
<text x="20" y="175" fill="currentColor" stroke="none">debounce time &gt; worst bounce you measured</text>
</svg>
<figcaption>A logic analyzer capture of a button press: the pin toggles several times in a short window before settling. This window is contact bounce.</figcaption>
</figure>

A microcontroller can read a pin on a microsecond timescale, so it sees a single press as many. Bounce duration varies a great deal by button type, age and how hard it is pressed.
Some are under a millisecond; others are several milliseconds. **So you must measure the actual button you are using, never guess.**

A common software debounce approach is "accept a new value only once it has held steady long enough."
The Developer Hub's Button Monitor example reads the button every 25 ms, and accepts a new value once it reads the same value for two consecutive checks (`BUTTON_DEBOUNCE_TICKS = 2`) — meaning it must hold steady for about 50 ms.

**A data-driven way to choose a debounce time:**

1. Measure bounce several times (at least 10 to 20, both pressing and releasing), and find the **longest** duration
2. Debounce time = the longest duration × a safety multiplier of 2 to 3
3. Check that it is not so long that users feel the button lag — a delay of a few tens of milliseconds generally still feels instant

**Hardware debouncing:** put a capacitor across the button, such as 100 nF with a 10 kΩ pull-up. On press, the capacitor discharges through the button very quickly; on release, it charges through the 10 kΩ with τ = 1 ms.
The voltage reaches 0.7 × VDD at time τ × ln(1 / 0.3) = 1.2 × τ = 1.2 ms. An edge this slow should feed an input with a Schmitt trigger (built-in hysteresis), otherwise it may toggle back and forth while the voltage crosses the middle range.

## Worked example

**Problem:** connect an external button to pin P13.0 on the TESAIoT Dev Kit's header, with an external pull-up, and choose a debounce time.

1. **Circuit:** 3V3 → R_pu 10 kΩ → point BTN_N → button → GND, and BTN_N → 1 kΩ → P13.0, per the figure in section 2.
2. **Current while pressed:** 3.3 V / 10 kΩ = 0.33 mA. Power in R_pu = 3.3 V × 0.33 mA = 1.09 mW.
3. **Levels the pin sees:** released, 3.3 V (minus the pin's leakage current times 11 kΩ, which is negligible); pressed, 0 V. Both are far from V_IH and V_IL.
4. **Bounce data.** Suppose you measured 10 presses with a logic analyzer, getting these bounce durations in ms (sample data — not your button's real values):

```text
0.2  0.4  1.6  0.3  0.9  0.1  2.4  0.5  0.7  1.1
maximum = 2.4 ms  average = 0.82 ms
```

5. **Choose the debounce time:** use the maximum, not the average. 2.4 ms × 3 = 7.2 ms, rounded to 10 ms — still fast enough that the user does not notice.
6. **Check against the code:** if you read every 5 ms and accept once the value holds for two consecutive checks, you get about 10 ms — matching your choice.

## Practice

1. A 4.7 kΩ pull-up at 3.3 V. How much current flows while the button is pressed? What power does the resistor dissipate?
2. An input pin has up to 1 µA of leakage current. Using a pull-up of (a) 47 kΩ, (b) 470 kΩ, what voltage is left at the pin while the button is released? Is it still above V_IH = 2.31 V?
3. A debounce RC of a 10 kΩ pull-up with 1 µF: while releasing the button, how long does the pin take to reach 0.7 × VDD?
4. Measured bounce durations (ms): 0.6, 0.3, 3.1, 0.8, 1.2. What debounce time should you choose, and why not the average?
5. A button wired as pull-down (resistor to GND, button to 3.3 V) — what does pressing it read, and what is this configuration called?
6. A program reads a pin every 100 ms, like the GPIO In button in the header test program. Will it see a 2 ms bounce?

## Solution

1. I = 3.3 V / 4.7 kΩ = 0.702 mA, and P = 3.3 V × 0.702 mA = 2.32 mW
2. (a) 1 µA × 47 kΩ = 0.047 V, leaving 3.25 V — passes comfortably. (b) 1 µA × 470 kΩ = 0.47 V, leaving 2.83 V — still passes, but the margin has shrunk a lot.
3. τ = 10 kΩ × 1 µF = 10 ms. Time to reach 0.7 × VDD = 1.2 × 10 ms = 12 ms.
4. The maximum, 3.1 ms, times a 2-to-3 safety factor gives about 6 to 9 ms — choosing 10 ms works. The average (1.2 ms) would let half of all presses' bounce slip through.
5. Pressed connects the pin to 3.3 V, reading 1 — this is called active-high.
6. No. Reading every 100 ms only catches things long enough to span a read cycle. A 2 ms bounce will mostly fall between two reads — exactly why a much faster-sampling logic analyzer is needed here.

## Check your understanding

Answer at least 4 of the 5 questions in [quiz.yaml](quiz.yaml) correctly, and explain in your own words why "it looked steady during testing" is not proof that a floating pin is fine to use.

## Lab

**Part A: a floating pin versus a pin with a pull-up**

1. With USB unplugged, wire the circuit from the worked example, but **without** R_pu 10 kΩ yet (just the button and the 1 kΩ resistor into P13.0).
2. Plug in USB, press **GPIO In**, then touch the BTN_N wire with a finger. Record how many times bit 0 (P13.0) changes within 8 s.
3. Unplug USB, add R_pu 10 kΩ, and repeat. Bit 0 should now stay steady at 1, even while touching the wire.
4. Press GPIO In again, then alternately hold and slowly release the button. Bit 0 should read 0 while pressed and 1 while released.
5. Measure the voltage at BTN_N with a multimeter, both pressed and released, then compute the current through R_pu while pressed.

**Part B: measuring bounce with a logic analyzer**

1. Connect the logic analyzer's GND to the board's GND first, then connect channel 0 (CH0) to point BTN_N.
2. Open PulseView, select the device, set the sample rate to at least 1 MHz (1 µs resolution), with enough samples for several seconds.
3. Set a trigger on CH0's falling edge, press Run, then press the button once.
4. Zoom in on the first edge, and use the time cursor to measure from the first edge to the last edge before it settles — that is the bounce duration.
5. Repeat at least 10 times while pressing, and 10 times while releasing (rising-edge trigger). Record it in the table, then choose a debounce time using section 3's method.

| Trial | Bounce while pressing (ms) | Bounce while releasing (ms) |
|---|---|---|
| 1 | | |
| 2 | | |
| … | | |
| Maximum | | |

**Part C: compare against the Button Monitor example.** Run the [QWA309 Push Button Monitor](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_button_monitor&q=prac_qwa309_button_monitor) example,
which reads buttons on pins P17.7 and P17.5 as active-low with the chip's internal pull-up (if your board does not have buttons on these pins yet, see the example's README for how to wire them).
Press the button quickly and see whether the count matches how many times you actually pressed.
Is this example's roughly 50 ms debounce time longer than the value you chose in Part B? If it is much longer, what are the trade-offs?

**If using the Eva Kit:** wire the same button circuit to a spare pin on the board, and write a short program that sets that pin as a no-pull input and prints the value when it changes. Part B works exactly the same way.

## Going further

The next module starts with [Measuring voltage and continuity](../../m03-multimeter/l01-voltage-and-continuity/README.md), where we get comfortable and safe with a multimeter.
If you want to see a button used in a C program next, see the lesson [Buttons and menus in the TESAIoT Firmware Stack course](../../../tesaiot-firmware-stack/m04-qwa309-hardware/l01-buttons-and-menu/README.md).

## Reflect

Before this lesson, if a button in your program occasionally over-counted, would you have suspected the code or the hardware first? How would you prove which one is at fault now?

## References

- [AIoT in Action: examples/s03/04_button_active_low.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s03/04_button_active_low.py)
- [AIoT in Action: examples/s03/05_debounce_count.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s03/05_debounce_count.py)
- [SDK: cm33/io/04_gpio_led_button.c (the button's drive mode)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c)
- [sigrok PulseView](https://sigrok.org/wiki/PulseView)
- [README of QWA309 Push Button Monitor (Developer Hub, commit 372d0d8)](https://github.com/tesaiot/developer-hub/blob/372d0d849578a6a49b634d3ecaab8b5958166921/prac_qwa309_button_monitor/README.md)
- [Pull-up resistor (Wikipedia)](https://en.wikipedia.org/wiki/Pull-up_resistor)
- [Switch: contact bounce (Wikipedia)](https://en.wikipedia.org/wiki/Switch#Contact_bounce)
