---
id: elec.m01.l03
lang: en
title: {th: 'ชิ้นส่วนพื้นฐาน: ตัวต้านทาน ตัวเก็บประจุ ไดโอด และทรานซิสเตอร์', en: 'Basic components: resistors, capacitors, diodes and transistors'}
summary: {th: รู้จักหน้าที่ของชิ้นส่วนพื้นฐาน และใช้ทรานซิสเตอร์เป็นสวิตช์ขับโหลดที่ขาไมโครคอนโทรลเลอร์ขับเองไม่ได้, en: 'Know what the basic components do, and use a transistor as a switch for loads a pin cannot drive.'}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m01.l02]
objectives:
- {th: คำนวณตัวต้านทานจำกัดกระแสของหลอด LED จากแรงดันแหล่งจ่าย แรงดันตกคร่อม LED และกระแสที่ต้องการ, en: 'Compute an LED current-limiting resistor from supply voltage, LED forward voltage and target current.'}
- {th: อธิบายหน้าที่ของตัวเก็บประจุ decoupling และไดโอดกันไฟย้อนในวงจรขับโหลดแบบขดลวด, en: Explain decoupling capacitors and flyback diodes on inductive loads.}
- {th: เลือกใช้ทรานซิสเตอร์หรือ MOSFET เป็นสวิตช์เมื่อโหลดต้องการกระแสเกินขาของไมโครคอนโทรลเลอร์, en: Choose a transistor or MOSFET switch when a load needs more current than a pin supplies.}
develops:
- {skill: hw.electronics, to: 2}
- {skill: hwdev.design-basics, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: alpha
translation: done
source_sha256: 8ce499ef3610cff38be0ef8c309608bb3748bbab820a69de196094ee4b70fe76
---

## Objectives

By the end of this lesson you will:

1. Compute an LED's current-limiting resistor from the supply voltage, the LED's forward voltage, and the target current
2. Explain what decoupling capacitors and flyback diodes do in a circuit driving an inductive load
3. Choose a transistor or MOSFET as a switch when a load needs more current than a microcontroller pin can supply

## Before you start

- You can already use Ohm's law, series circuits and voltage dividers (the previous two lessons)
- For the lab: a leaded red LED, a 470 Ω resistor and a 1 kΩ resistor, a 100 kΩ resistor, a 100 µF electrolytic capacitor (rated at least 6.3 V), a stopwatch (a phone works), a multimeter, and a board
- A magnifying glass or a phone camera for looking closely at the board

> **Safety.** Electrolytic capacitors are polarised — the longer lead is positive, and the side with a coloured stripe is negative. Connecting one backwards can make it heat up, bulge, or explode.
> This lesson only uses 3.3 V, but build the habit of checking polarity every time, starting now.

## See it work first

Look closely at the board with a magnifying glass or a phone camera. Take a photo and zoom in.

- Around every chip there are several small brown or grey rectangular parts, sitting right next to the chip's pins — most are capacitors
- Next to every LED there is usually one small resistor

Ask yourself two questions: why does every chip need its own capacitor sitting right next to its pins, and why must an LED always come paired with a resistor?
This lesson answers both.

## Concepts

### 1. The LED and its current-limiting resistor

An LED is a kind of diode. When conducting, it has a fairly constant **forward voltage (V_f)**, depending on its colour and part number.
A red LED is usually around 1.8 to 2.2 V; blue, bright green and white are usually around 2.8 to 3.3 V. Always check the real value in the specific part's datasheet.

The problem is that once the voltage exceeds V_f by even a little, the LED's current shoots up very fast. So a resistor is needed to absorb the remaining voltage and set the current.

<figure>
<svg viewBox="0 0 360 170" width="360" role="img" aria-label="An LED in series with a current-limiting resistor" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<path d="M50 22H70M60 22V30"/><text x="60" y="17" text-anchor="middle" fill="currentColor" stroke="none">3.3 V or GPIO</text>
<path d="M60 30V40"/>
<polyline points="60,40 60,50 66,52.5 54,57.5 66,62.5 54,67.5 66,72.5 54,77.5 60,80 60,90"/>
<text x="76" y="70" fill="currentColor" stroke="none">R</text>
<path d="M60 90V105.0M52 105.0H68L60 117.0Z M52 117.0H68M60 117.0V134"/><path d="M71 106.0l7 -6m-4 0h4v4M71 113.0l7 -6m-4 0h4v4"/>
<text x="92" y="120" fill="currentColor" stroke="none">LED (V_f)</text>
<path d="M60 134V142M50 142H70M54 146H66M58 150H62"/>
<text x="180" y="60" fill="currentColor" stroke="none">R = (V_s − V_f) / I</text>
<text x="180" y="84" fill="currentColor" stroke="none">3.3 V, V_f 2.0 V, 5 mA</text>
<text x="180" y="104" fill="currentColor" stroke="none">R = 1.3 V / 5 mA = 260 Ω</text>
<text x="180" y="124" fill="currentColor" stroke="none">use 270 Ω → 4.81 mA</text>
</svg>
<figcaption>The resistor absorbs whatever voltage is left over from the LED's V_f, and this is what sets the current.</figcaption>
</figure>

```text
R = (V_s − V_f) / I
```

**Example:** a 3.3 V supply, a red LED with V_f = 2.0 V, needing 5 mA

```text
R = (3.3 − 2.0) V / 5 mA = 1.3 V / 5 mA = 260 Ω
The nearest standard value at or above this is 270 Ω → I = 1.3 V / 270 Ω = 4.81 mA
Power in the resistor = 1.3 V × 4.81 mA = 6.26 mW
```

Always round up to the next standard value — the current comes out a little below target, which is the safer direction.

**The trap with a blue LED at 3.3 V.** With V_f = 3.0 V, only 0.3 V is left for the resistor. Choosing 150 Ω gives 2 mA in theory.
But each LED's real V_f varies by ±0.2 V, so the real current swings anywhere from 0.1 V / 150 Ω = 0.67 mA to 0.5 V / 150 Ω = 3.33 mA — a five-fold range.
When headroom is small, brightness becomes uncontrollable. The fix is to feed the LED from a higher supply and use a transistor as a switch (section 3).

**Microcontroller pins have limits too.** Each pin can source or sink no more than the value stated in the chip's datasheet, and the whole port together has a further combined limit.
Before wiring an LED straight to a pin, always check the GPIO DC specifications table in the PSoC Edge E84's datasheet (or whichever chip you are using) first.

### 2. Capacitors and diodes: the helpers that get forgotten

A **capacitor (C)** stores charge, Q = C × V. When it charges through a resistor, the voltage rises exponentially with a **time constant τ = R × C.**

<figure>
<svg viewBox="0 0 380 190" width="380" role="img" aria-label="A graph of a capacitor's voltage as it charges through a resistor" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<path d="M40 150H350M40 150V20"/>
<polyline points="40,150 45,140.4 50,131.6 55,123.5 60,116 65,109.1 70,102.8 75,97 80,91.6 85,86.7 90,82.2 95,78 100,74.1 105,70.6 110,67.4 115,64.4 120,61.6 125,59.1 130,56.8 135,54.6 140,52.7 145,50.9 150,49.2 155,47.7 160,46.2 165,44.9 170,43.7 175,42.6 180,41.6 185,40.7 190,39.9 195,39.1 200,38.3 205,37.7 210,37.1 215,36.5 220,36 225,35.5 230,35.1 235,34.7 240,34.3 245,33.9 250,33.6 255,33.3 260,33.1 265,32.8 270,32.6 275,32.4 280,32.2 285,32 290,31.9 295,31.7 300,31.6 305,31.4 310,31.3 315,31.2 320,31.1 325,31 330,31 335,30.9 340,30.8"/>
<path d="M40 30H340" stroke-dasharray="4 3"/>
<path d="M40 74.1H100.0V150" stroke-dasharray="4 3"/>
<text x="36" y="34" text-anchor="end" fill="currentColor" stroke="none">V_s</text>
<text x="36" y="78.14553294057308" text-anchor="end" fill="currentColor" stroke="none">63%</text>
<text x="100.0" y="166" text-anchor="middle" fill="currentColor" stroke="none">1τ</text>
<text x="160.0" y="166" text-anchor="middle" fill="currentColor" stroke="none">2τ</text>
<text x="220.0" y="166" text-anchor="middle" fill="currentColor" stroke="none">3τ</text>
<text x="280.0" y="166" text-anchor="middle" fill="currentColor" stroke="none">4τ</text>
<text x="340.0" y="166" text-anchor="middle" fill="currentColor" stroke="none">5τ</text>
<text x="300" y="14" text-anchor="middle" fill="currentColor" stroke="none">99.3% at 5τ</text>
<text x="190.0" y="184" text-anchor="middle" fill="currentColor" stroke="none">t</text>
</svg>
<figcaption>A capacitor charging through a resistor: at 1τ = RC it reaches 63.2% of the supply voltage; at 5τ it reaches about 99.3%.</figcaption>
</figure>

**Example:** R = 10 kΩ, C = 100 nF, a 3.3 V supply

```text
τ = 10 kΩ × 100 nF = 1 ms
At t = 1τ (1 ms), voltage = 3.3 × (1 − e^−1) = 3.3 × 0.632 = 2.09 V
At t = 5τ (5 ms), it reaches about 99.3% — treated as fully charged in practice
```

**Decoupling.** When logic inside a chip switches state, it draws a short current spike. A long trace running from the voltage regulator has inductance, and cannot supply current that fast.
Suppose a chip suddenly draws an extra 50 mA within 2 ns, through a trace with 10 nH of inductance (a reasonable assumed value).

```text
V = L × di/dt = 10 nH × (50 mA / 2 ns) = 0.25 V   a momentary dip of almost 8% of 3.3 V
```

If a 100 nF capacitor sits right next to the power pin, a 50 mA spike lasting 10 ns draws 50 mA × 10 ns = 0.5 nC of charge from that capacitor.

```text
ΔV = Q / C = 0.5 nC / 100 nF = 5 mV
```

Only a 5 mV dip. This is exactly why every chip has its own decoupling capacitor, which must sit **as close to the power pin as possible** — because the trace between the capacitor and the pin has inductance too.
A typical board has a small one (e.g. 100 nF) right next to every power pin, plus a few larger ones (e.g. 10 µF) for slower changes. We will come back to this in the lesson [PCB and EMC basics](../../m06-build-and-read/l04-pcb-and-emc-basics/README.md).

A **diode** lets current flow one way only. A silicon diode drops about 0.6 to 0.7 V; a Schottky diode drops about 0.2 to 0.4 V.

A **flyback diode** matters for inductive loads such as a relay or motor coil, which will not let its current change instantly. When a switch cuts the current, the coil generates its own high voltage, following V = L × di/dt.
Suppose a 100 mH coil carrying 50 mA is cut off within 1 µs.

```text
V = 100 mH × (50 mA / 1 µs) = 5,000 V   (in theory; in reality the voltage spikes until the transistor breaks down or a spark jumps first)
```

A diode connected across the coil (cathode toward the positive supply side) gives the current somewhere to keep circulating, so the voltage at the switching point is limited to about the supply voltage plus 0.7 V.
The current then decays with a time constant of L / R. If the coil's own resistance is 100 Ω, that gives τ = 100 mH / 100 Ω = 1 ms.

### 3. Transistors and MOSFETs as switches

When a load needs more current or voltage than a microcontroller pin can give, have the pin "command" a switch instead, and let the switch connect the load to its own supply.
The most common approach is a low-side switch, connected between the load and GND.

<figure>
<svg viewBox="0 0 360 245" width="360" role="img" aria-label="A low-side MOSFET driving a relay coil, with a flyback diode" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<path d="M150 22H170M160 22V30"/><text x="160" y="17" text-anchor="middle" fill="currentColor" stroke="none">5 V</text>
<path d="M160 30V40M160 40H110M160 40H210"/>
<circle cx="160" cy="40" r="2.5" fill="currentColor"/>
<path d="M110 40V52M210 40V52"/>
<path d="M110 52V60.0a4 4 0 0 1 0 8a4 4 0 0 1 0 8a4 4 0 0 1 0 8a4 4 0 0 1 0 8V100"/>
<text x="96" y="80" text-anchor="end" fill="currentColor" stroke="none">relay coil</text>
<path d="M210 100V82.0M202 82.0H218L210 70.0Z M202 70.0H218M210 70.0V52"/>
<text x="226" y="80" fill="currentColor" stroke="none">flyback diode</text>
<path d="M110 100V112H210V100"/>
<circle cx="160" cy="112" r="2.5" fill="currentColor"/>
<path d="M160 112V130"/>
<path d="M160 130V140H150M150 136V164M144 138V162M150 160H160V170"/>
<path d="M150 150H160V160M151 150l5 -3M151 150l5 3"/>
<text x="170" y="152" fill="currentColor" stroke="none">N-MOSFET (logic level)</text>
<path d="M144 150H120"/>
<polyline points="70,150 80,150 82.5,144 87.5,156 92.5,144 97.5,156 102.5,144 107.5,156 110,150 120,150"/>
<text x="95" y="140" text-anchor="middle" fill="currentColor" stroke="none">100 Ω</text>
<path d="M70 150H40"/>
<circle cx="37" cy="150" r="3"/>
<text x="37" y="138" text-anchor="middle" fill="currentColor" stroke="none">GPIO</text>
<path d="M120 150V165"/>
<circle cx="120" cy="150" r="2.5" fill="currentColor"/>
<polyline points="120,165 120,170 126,172.5 114,177.5 126,182.5 114,187.5 126,192.5 114,197.5 120,200 120,205"/>
<text x="104" y="190" text-anchor="end" fill="currentColor" stroke="none">100 kΩ</text>
<path d="M120 205V215H160M160 170V215"/>
<circle cx="160" cy="215" r="2.5" fill="currentColor"/>
<path d="M160 215V223M150 223H170M154 227H166M158 231H162"/>
</svg>
<figcaption>A GPIO pin commands a low-side MOSFET that connects the relay coil to ground. A diode across the coil gives the current somewhere to keep flowing when it switches off. A 100 kΩ resistor pulls the gate down to ground while the chip has not yet started up.</figcaption>
</figure>

**An NPN transistor (BJT)** is controlled by base current. As a switch, we deliberately oversupply base current to drive it into saturation, usually assuming a "forced β" of around 10 to 20.
A 5 V relay coil drawing 70 mA, with a forced β of 20, needs a base current of 70 / 20 = 3.5 mA. The base resistor = (3.3 − 0.7) V / 3.5 mA = 743 Ω; use 750 Ω.
This works fine if the pin can easily supply 3.5 mA, but a 500 mA load would need tens of mA of base current, far more than a pin can provide.

**An N-channel MOSFET** is controlled by gate voltage (V_GS), draws almost no current while held on (only a brief pulse to charge the gate), and suits high-current loads.
The thing to watch is **V_GS(th)** in the datasheet: this is the voltage where the MOSFET "just starts" conducting, not where it is fully on.
Check that **R_DS(on)** is specified at a V_GS equal to or below what your pin can provide (e.g. 2.5 V for a 3.3 V pin). This kind of MOSFET is called logic-level.

**Example:** a 12 V LED strip drawing 500 mA, with a MOSFET whose R_DS(on) = 0.05 Ω at V_GS = 2.5 V

```text
Voltage across the MOSFET = 0.5 A × 0.05 Ω = 25 mV
Power in the MOSFET = (0.5 A)² × 0.05 Ω = 12.5 mW   no heatsink needed
```

An NPN with the same load, at a forced β of 10, would need 50 mA of base current — far beyond a microcontroller pin.

| Load | Choice |
|---|---|
| Current within what the pin supplies, voltage within the pin's own — e.g. a small LED | Direct from the pin, through a resistor |
| Current up to around 100 mA — e.g. a buzzer, a small relay | An NPN with a base resistor, or a small MOSFET |
| High current or a voltage higher than the board's — e.g. a 12 V LED strip, a motor | A low-side, logic-level N-channel MOSFET |
| The load is a coil (relay, motor, solenoid) | Any of the above, **plus** a flyback diode |

## Worked example

**Problem:** drive a 5 V relay (coil drawing 70 mA, coil resistance about 5 V / 70 mA = 71 Ω) from the board's 3.3 V GPIO pin.

1. **Can the pin drive it directly?** No — both the voltage (needs 5 V) and the current (70 mA) exceed what a GPIO pin should supply.
2. **Choose a switch.** A logic-level, low-side N-channel MOSFET. Choose a part specifying R_DS(on) at V_GS = 2.5 V or lower; assume 0.1 Ω.
   Voltage drop = 70 mA × 0.1 Ω = 7 mV, and power = (70 mA)² × 0.1 Ω = 0.49 mW.
3. **A 100 Ω gate resistor** limits the momentary charging surge to no more than 3.3 V / 100 Ω = 33 mA.
   If the gate capacitance is 500 pF (an assumed value — check C_iss in the datasheet), the time constant is 100 Ω × 500 pF = 50 ns, fast enough for a relay many times over.
4. **A 100 kΩ gate pull-down resistor.** While the chip is resetting or has not yet configured the pin, it may float. This resistor keeps the MOSFET reliably off, drawing only 3.3 V / 100 kΩ = 33 µA while active.
5. **A flyback diode**, such as a 1N4148, across the coil, cathode toward the 5 V side and anode toward the MOSFET's drain side. A small signal diode like this is fine for a small relay whose coil current is only a few tens of mA.
6. **Decoupling for the 5 V rail:** add 100 nF right next to the relay, plus one more 10 µF, because the relay draws a current pulse every time it switches.

Notice we have used every idea from this lesson: Ohm's law (coil current, gate current), time constants (gate, coil), decoupling, and diodes.

## Practice

1. A 5 V supply, a red LED with V_f = 2.0 V, needing 10 mA. Find R, the standard E12 value to use, the real current, and the power in the resistor.
2. A 3.3 V supply, a white LED with V_f = 2.9 V, needing 2 mA. Find R. If the real LED has V_f = 3.1 V, what current results?
3. R = 47 kΩ, C = 1 µF, a 3.3 V supply. Find τ, the time considered "fully charged" (5τ), and the voltage at t = τ.
4. A chip draws a 200 mA spike lasting 5 ns from a decoupling capacitor. What is the voltage dip if the capacitor is (a) 100 nF, (b) 10 nF?
5. A 12 V LED strip drawing 1 A is commanded from a 3.3 V GPIO pin. Which kind of switch should you choose? If R_DS(on) = 0.03 Ω, what is the power in the switch? Does it need a flyback diode?
6. A 5 V relay with a 400 Ω coil is driven by an NPN with a forced β of 20. Find the coil current, the base current, and a standard E12 base resistor.

## Solution

1. R = 3.0 V / 10 mA = 300 Ω. Use 330 Ω (the nearest E12 value above it). Current = 3.0 / 330 = 9.09 mA. Power = 3.0 V × 9.09 mA = 27.3 mW.
2. R = 0.4 V / 2 mA = 200 Ω. If V_f = 3.1 V, the current becomes 0.2 V / 200 Ω = 1.0 mA — half of the design value. This is exactly the headroom problem.
3. τ = 47 kΩ × 1 µF = 47 ms. Fully charged at 5τ = 235 ms. Voltage at t = τ is 3.3 × 0.632 = 2.09 V.
4. Charge = 200 mA × 5 ns = 1 nC. (a) 1 nC / 100 nF = 10 mV  (b) 1 nC / 10 nF = 100 mV. A capacitor ten times smaller gives a voltage dip ten times larger.
5. A low-side, logic-level N-channel MOSFET. Power = (1 A)² × 0.03 Ω = 30 mW. An LED strip is a resistive load, not an inductive one, so it does not need a flyback diode.
6. Coil current = 5 V / 400 Ω = 12.5 mA. Base current = 12.5 / 20 = 0.625 mA. Base resistor = (3.3 − 0.7) / 0.625 mA = 4.16 kΩ.
   The nearest E12 value below that is 3.9 kΩ (giving a base current of 0.67 mA, which guarantees saturation), and a flyback diode is still needed across the coil.

## Check your understanding

Answer at least 4 of the 5 questions in [quiz.yaml](quiz.yaml) correctly, then try explaining to a friend, without looking at this page, what happens when a relay switches off if you remove the flyback diode from its circuit.

## Lab

**Part A: an LED and a resistor**

1. With USB unplugged, wire 3V3 → 470 Ω → a red LED (the longer lead is the anode, connect it to the resistor side) → GND.
2. **Guess:** if V_f ≈ 2.0 V, the current should be (3.3 − 2.0) / 470 = 2.77 mA.
3. Plug in USB, and measure the voltage across the resistor (V_R) and the voltage across the LED (V_f) with a multimeter. Check that V_R + V_f ≈ your measured 3V3 voltage.
4. Compute the real current I = V_R / R (using the resistor value you measured while powered off), and compare against your guess.
5. Change to 1 kΩ, and repeat. Notice the brightness, and record how much V_f changes as the current drops (usually a small drop, not perfectly constant as the formula assumes).

| R | V_R | V_f | I = V_R / R | Brightness (by eye) |
|---|---|---|---|---|
| 470 Ω | | | | |
| 1 kΩ | | | | |

**Part B: a time constant you can watch with your own eyes**

1. With USB unplugged, wire 3V3 → 100 kΩ → the positive lead of a 100 µF capacitor, negative lead to GND. Check polarity before applying power.
2. Fully discharge the capacitor first, by touching a 1 kΩ resistor across its two leads for a few seconds.
3. **Guess:** τ = 100 kΩ × 100 µF = 10 s. At 10 s, you should read about 63% of the final voltage.
4. Place the meter leads across the capacitor first, then plug in USB and start the stopwatch at the same moment. Record the voltage every 5 s up to 60 s.
5. Find the time at which the voltage reaches 63% of its final value — that is your measured τ.

**Interpreting the results:** the meter's 10 MΩ input resistance sits in parallel with the capacitor, so the final voltage becomes 3.3 × 10 M / 10.1 M ≈ 3.27 V, and τ drops to about 9.9 s. This effect from the meter is small.
What matters more is the electrolytic capacitor's own tolerance, usually ±20%, so a measured τ anywhere from about 8 to 12 s is entirely normal.
If you measure well outside that range, check the resistor's value and the capacitor's polarity.

## Going further

The next module moves into [Logic levels and basic gates](../../m02-digital-logic/l01-logic-levels-and-gates/README.md). We will look at which voltages a chip counts as 0 or 1,
and why a board that has both a 1.8 V system and a 3.3 V system needs care when connecting external devices.

## Reflect

Which component in this lesson had you overlooked before, when you saw it on a board — and how will you look at it differently now?

## References

- [Lessons In Electric Circuits by Tony R. Kuphaldt (open book)](https://www.ibiblio.org/kuphaldt/electricCircuits/)
- [AIoT in Action: examples/s03/03_led_brightness.py](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s03/03_led_brightness.py)
- [RC time constant (Wikipedia)](https://en.wikipedia.org/wiki/RC_time_constant)
- [Decoupling capacitor (Wikipedia)](https://en.wikipedia.org/wiki/Decoupling_capacitor)
- [Flyback diode (Wikipedia)](https://en.wikipedia.org/wiki/Flyback_diode)
