---
id: elec.m04.l02
lang: en
title: {th: ถอดรหัส I2C และ UART, en: Decoding I2C and UART}
summary: {th: ใช้ protocol decoder ของ sigrok อ่านธุรกรรม I2C และเฟรม UART จากบอร์ดจริง, en: Use sigrok protocol decoders to read I2C transactions and UART frames from a real board.}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m04.l01]
objectives:
- {th: 'ตั้ง decoder ของ I2C แล้วอ่าน address, read/write และ ACK จากการสแกนบัสได้', en: 'Set up the I2C decoder and read address, read/write and ACK from a bus scan.'}
- {th: ตั้ง decoder ของ UART ที่ baud rate ถูกต้อง และอธิบายอาการเมื่อตั้งผิด, en: Set up the UART decoder at the right baud rate and describe the symptoms of a wrong setting.}
develops:
- {skill: meas.logic-analyzer, to: 2}
- {skill: proto.i2c, to: 2}
- {skill: proto.uart, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: alpha
translation: done
source_sha256: 2745e25e39c78e197d28a158daa7857cd4bf2ef8dad6a063d0f96e411ea54a1f
---

## Objectives

By the end of this lesson you will:

1. Set up the I2C decoder, and read the address, read/write bit and ACK from a bus scan
2. Set up the UART decoder at the correct baud rate, and describe the symptoms of setting it wrong

## Before you start

- You can already connect a logic analyzer, set its sample rate, and use a trigger (lesson [Capturing a first digital signal](../l01-capture-a-signal/README.md))
- A TESAIoT Dev Kit flashed with the [QWA309 Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) example, which has a **Scan** button that scans the I2C bus and a **UART Echo** button that sends a short packet out the header's UART pin
- The board's pinout diagram, to find the SDA and SCL pins of the I2C bus on the header, and pin P15.1 (UART TX)
- If using the Eva Kit, scan the I2C bus and print text over UART with your own program — the decoding steps are exactly the same

## See it work first

Press the **Scan** button on the header test program's screen. It prints a table of addresses 0x08 through 0x77; a cell where a device responds shows a number, and other cells show `--`.
It then reports "Found N device(s)," followed by a list of addresses.

How does the program know a device is at a given address? It asks each address in turn, 112 times in all, and listens for anyone answering "present."
In this lesson, we will eavesdrop on all 112 of those conversations on the real wires, and prove with our own eyes that the table on screen tells the truth.

## Concepts

### 1. I2C on the wire: START, address, R/W, ACK, STOP

I2C uses two wires, **SCL** (the clock, driven by the master) and **SDA** (data). Both are open-drain — a device can only pull the line down.
A **pull-up** resistor is what pulls the line back up, the same principle as the active-low button in the lesson [Pull-ups, pull-downs and buttons](../../m02-digital-logic/l02-pullups-and-buttons/README.md).

<figure>
<svg viewBox="0 0 390 170" width="390" role="img" aria-label="An I2C frame sending address 0x30 as a write, with ACK" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<text x="10" y="47" fill="currentColor" stroke="none">SCL</text>
<text x="10" y="107" fill="currentColor" stroke="none">SDA</text>
<polyline points="20,30 80,30 80,55 90,55 90,30 103,30 103,55 116,55 116,30 129,30 129,55 142,55 142,30 155,30 155,55 168,55 168,30 181,30 181,55 194,55 194,30 207,30 207,55 220,55 220,30 233,30 233,55 246,55 246,30 259,30 259,55 272,55 272,30 285,30 285,55 298,55 298,30 311,30 311,55 330,55 330,30 374,30"/>
<polyline points="20,90 70,90 70,115 84,115 84,115 110,115 110,90 136,90 136,90 162,90 162,115 188,115 188,115 214,115 214,115 240,115 240,115 266,115 266,115 292,115 292,115 336,115 336,115 346,115 346,90 374,90"/>
<text x="96.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<text x="122.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">1</text>
<text x="148.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">1</text>
<text x="174.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<text x="200.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<text x="226.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<text x="252.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<text x="278.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">W</text>
<text x="304.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">A</text>
<text x="70" y="158" text-anchor="middle" font-weight="bold" fill="currentColor" stroke="none">S</text>
<text x="168" y="158" text-anchor="middle" fill="currentColor" stroke="none">address 0x30</text>
<text x="278" y="158" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">R/W</text>
<text x="306" y="158" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">ACK</text>
<text x="346" y="158" text-anchor="middle" font-weight="bold" fill="currentColor" stroke="none">P</text>
</svg>
<figcaption>An I2C frame: START (S) is SDA falling while SCL is high, followed by a 7-bit address (0x30 = 0110000), the R/W bit (0 = write), then the target device pulls SDA down to ACK, ending with STOP (P), SDA rising while SCL is high.</figcaption>
</figure>

- **START (S):** SDA falls while SCL is still high — the signal that "I am about to speak"
- **The 7-bit address:** sent MSB first. Data on SDA must stay steady while SCL is high, and may change only while SCL is low
- **R/W:** the 8th bit; 0 = write, 1 = read
- **ACK / NACK:** on the 9th clock pulse, the master releases SDA. If the addressed device really exists, it pulls SDA down (ACK); if no one does, SDA stays high via the pull-up (NACK)
- **STOP (P):** SDA rises while SCL is high

**The 7-bit address versus the byte on the wire.** The first byte on the wire is the address shifted left by one bit, with the R/W bit appended.
So address 0x30 as a write becomes the byte 0x60, and as a read becomes 0x61. Some datasheets write the address in its 8-bit form (0x60), which confuses people very often.
sigrok's decoder shows it in 7-bit form by default (e.g. "Address write: 30").

**What the bus-scan tool does.** The header test program sends START + address + W, then STOP, for each address in turn — no other data at all.
Whichever address gets an ACK is where a device lives. Per the board's SDK documentation, the I2C bus on the TESAIoT Dev Kit's header has a CapSense chip (PSoC 4000T) that answers at 0x08,
so you should see an ACK at 0x08 at minimum. Compare any other address that answers against the list the screen prints.

**Sizing an I2C pull-up** (formula from TI SLVA689). The resistor must not be so small that a device cannot pull the line down to V_OL, and not so large that the rising edge is slower than the spec allows.

```text
R_p(min) = (V_CC − V_OL(max)) / I_OL = (3.3 − 0.4) V / 3 mA = 967 Ω
R_p(max) = t_r / (0.8473 × C_b)
  Fast-mode 400 kHz (t_r ≤ 300 ns), a 100 pF bus → 300 ns / (0.8473 × 100 pF) = 3.54 kΩ
  Standard-mode 100 kHz (t_r ≤ 1000 ns), a 100 pF bus → 11.8 kΩ
```

So a 400 kHz bus with 100 pF of capacitance can choose anywhere between 967 Ω and 3.54 kΩ — for example, 2.2 kΩ.
The constant 0.8473 comes from ln(0.7 / 0.3), the time an RC curve takes to rise from 0.3 × V_CC to 0.7 × V_CC — exactly I2C's V_IL and V_IH thresholds.

### 2. UART on the wire: no clock, so both sides must agree on speed beforehand

UART sends data on a single wire per direction (one side's TX connects to the other side's RX), with no clock wire at all, so both sides must set the same **baud rate** in advance.
The most common format is **8N1**: 8 data bits, no parity bit, 1 stop bit.

<figure>
<svg viewBox="0 0 400 145" width="400" role="img" aria-label="A UART 8N1 frame carrying the byte 0xA5" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<polyline points="10,40 50,40 50,40 50,80 80,80 80,40 110,40 110,80 140,80 140,40 170,40 170,80 200,80 200,80 230,80 230,40 260,40 260,80 290,80 290,40 320,40 320,40 350,40 380,40"/>
<path d="M50 90V96" stroke-dasharray="4 3"/>
<text x="65.0" y="110" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">start</text>
<text x="65.0" y="30" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<path d="M80 90V96" stroke-dasharray="4 3"/>
<text x="95.0" y="110" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">b0</text>
<text x="95.0" y="30" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">1</text>
<path d="M110 90V96" stroke-dasharray="4 3"/>
<text x="125.0" y="110" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">b1</text>
<text x="125.0" y="30" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<path d="M140 90V96" stroke-dasharray="4 3"/>
<text x="155.0" y="110" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">b2</text>
<text x="155.0" y="30" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">1</text>
<path d="M170 90V96" stroke-dasharray="4 3"/>
<text x="185.0" y="110" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">b3</text>
<text x="185.0" y="30" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<path d="M200 90V96" stroke-dasharray="4 3"/>
<text x="215.0" y="110" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">b4</text>
<text x="215.0" y="30" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<path d="M230 90V96" stroke-dasharray="4 3"/>
<text x="245.0" y="110" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">b5</text>
<text x="245.0" y="30" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">1</text>
<path d="M260 90V96" stroke-dasharray="4 3"/>
<text x="275.0" y="110" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">b6</text>
<text x="275.0" y="30" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<path d="M290 90V96" stroke-dasharray="4 3"/>
<text x="305.0" y="110" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">b7</text>
<text x="305.0" y="30" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">1</text>
<path d="M320 90V96" stroke-dasharray="4 3"/>
<text x="335.0" y="110" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">stop</text>
<text x="335.0" y="30" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">1</text>
<text x="10" y="30" font-size="11" fill="currentColor" stroke="none">idle</text>
<text x="200" y="135" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0xA5 = 1010 0101, sent LSB first · 115200 baud: 8.68 µs per bit</text>
</svg>
<figcaption>A UART 8N1 frame carrying byte 0xA5: the idle line is 1, the start bit is 0, followed by 8 data bits sent least-significant bit (LSB) first, then a stop bit of 1.</figcaption>
</figure>

- The idle line is 1
- **The start bit** is 0 for one bit period — the receiver uses this falling edge to set its timing
- **The 8 data bits** are sent **least-significant bit first (LSB first)** — the opposite of I2C
- **The stop bit** is 1. If the receiver reads 0 here instead, it reports a framing error

**The numbers at 115200 baud:**

```text
1 bit    = 1 / 115200 s = 8.68 µs
1 byte   = 10 bits (start + 8 + stop) = 86.8 µs
Maximum throughput = 115200 / 10 = 11,520 bytes per second
```

**Example:** byte 0xA5 = 1010 0101, sent LSB first. The bits on the wire after the start bit are therefore 1, 0, 1, 0, 0, 1, 0, 1, followed by a stop bit of 1.

**The header test program's UART Echo.** It sends a 4-byte packet out pin P15.1 at 115200 8N1: `A5 11 <counter> <checksum>`.
The counter starts at 0 and increments by one on every press; the checksum is the XOR of the first three bytes, so the first press gives `A5 11 00 B4` (0xA5 XOR 0x11 = 0xB4).
The program also prints the bytes it sent on screen, in a `TX:` line, so we have an answer key to check the decoder against.
If no ESP32-S3 board answers as the example expects, per the constants in the code, the program waits 250 ms for a reply, pauses 10 ms, and resends — up to 4 times in total. Measure the real spacing from the capture yourself.

### 3. Reading a capture to spot mistakes

**A wrong baud setting.** The decoder measures bits at the wrong rhythm, giving garbled bytes and framing errors.

- Setting 9600 against a real 115200 signal: one bit the decoder expects is 104 µs, but the whole 4-byte packet (about 347 µs) only lasts about 3.3 bits at 9600, so the decoder sees a single garbled byte or an error
- Setting 57600 (half speed): each bit the decoder reads spans two real bits, giving wrong byte values, usually with framing errors
- Setting too fast, e.g. 230400: the decoder sees one real bit as two, and the resulting bytes are meaningless

**Finding the baud rate from a capture.** Zoom in on the narrowest pulse (one bit), then compute baud ≈ 1 / that width. An 8.68 µs pulse is 115200; a 104 µs pulse is 9600.
Then choose the nearest standard value — UART tolerates only a small baud error (generally, the combined error of both sides should stay under about 2 to 3%).

**Other symptoms a capture can reveal:**

| What you see | Possible cause |
|---|---|
| I2C: every address gets a NACK | No device present, the device has no power, SDA and SCL are swapped, or the address is wrong |
| I2C: SDA or SCL stuck low the whole time | A device is stuck mid-transaction, or a wire is shorted to ground |
| I2C: the rising edge is a long, slow curve (needs an oscilloscope to see) | The pull-up is too large, or the bus is long enough that capacitance is high |
| UART: nothing on the RX wire even though the other side is sending | TX is wired to TX (TX and RX must be crossed), or a common GND was forgotten |

## Worked example

**Problem:** decode the header test program's I2C bus scan, and confirm the result against the screen.

1. **Connect the leads.** The device's GND to GND, channel 0 to SCL, channel 1 to SDA of the I2C bus on the header (find their positions from the board's pinout diagram).
2. **Sample rate.** Not knowing the bus speed yet, use 8 MHz to start, which covers up to 400 kHz (20 samples per SCL period).
   Capture, then measure SCL's period. If it turns out to be 100 kHz, you can lower the sample rate to capture for longer.
3. **Trigger** on SDA's falling edge (which happens at START). Press Run, then press Scan on screen.
4. **Add a decoder.** In PulseView, add a decoder named I2C, and set SCL = channel 0 and SDA = channel 1.
5. **Read the result.** The decoder track shows the sequence Start → Address write: 08 → ACK or NACK → Stop, repeating for each address in turn.
6. **Check.** Address 0x08 should get an ACK (the CapSense chip); addresses with no device get a NACK. Count every address that got an ACK, and compare against "Found N device(s)" on screen — every address must match.
7. **Look at the raw byte.** Switch the decoder's display to show the address in 8-bit form; address 0x08 as a write must show as 0x10.

If the number of ACKs on the wire does not match the screen, do not blame the instrument yet — first check whether you captured all 112 addresses (was the capture time long enough?), and whether the sample rate was fast enough.

## Practice

1. A device has 7-bit address 0x44. What is the first byte on the wire for a write, and for a read?
2. A decoder shows "Address read: 68" followed by NACK. What does this mean, and what should you check next?
3. UART at 9600 8N1: how long is one bit, one byte, and what is the maximum throughput in bytes per second?
4. Sending byte 0x55 over UART 8N1, what does the wire's shape look like, and why is this byte useful for finding the baud rate?
5. You measure the narrowest pulse on a UART wire at 26 µs. What is the baud rate likely to be?
6. A 3.3 V I2C bus at 100 kHz has 200 pF of total capacitance. Find R_p(min) and R_p(max), then decide whether 4.7 kΩ works.
7. Pressing UART Echo a third time (counter = 0x02), what should all 4 bytes of the packet be?

## Solution

1. Write: 0x44 shifted left one bit = 0x88. Read: 0x89.
2. The master asked to read from address 0x68, and no one answered. Check that the device has power, is really on this same bus (a board may have several buses), and that the address matches the datasheet, including any address-select pins on the device.
3. 1 bit = 1 / 9600 = 104.2 µs. 1 byte = 10 bits = 1.042 ms. Maximum throughput = 960 bytes per second.
4. 0x55 = 0101 0101, sent LSB first gives 1, 0, 1, 0, 1, 0, 1, 0. Combined with the start bit (0) and stop bit (1), the wire alternates between 0 and 1 on every single bit — a square wave where every pulse is exactly one bit wide. Measuring that width gives the baud rate immediately.
5. 1 / 26 µs = 38,462 baud. The nearest standard value is 38400.
6. R_p(min) = (3.3 − 0.4) / 3 mA = 967 Ω. R_p(max) = 1000 ns / (0.8473 × 200 pF) = 5.90 kΩ. 4.7 kΩ falls within this range, so it works.
7. `A5 11 02 B6`, because 0xA5 XOR 0x11 XOR 0x02 = 0xB6.

## Check your understanding

Answer at least 4 of the 5 questions in [quiz.yaml](quiz.yaml) correctly.

## Lab

**Part A: the I2C bus scan.** Follow the worked example, then fill in the table.

| What to check | On the board's screen | From the decoder |
|---|---|---|
| SCL frequency | not shown | |
| Number of addresses asked | 112 (0x08 to 0x77) | |
| Addresses that got an ACK | | |
| Wire byte of the first ACK'd address (8-bit form) | not shown | |

**Part B: UART Echo**

1. Connect channel 0 to P15.1 (TX), and, if you have a spare channel, channel 1 to P15.0 (RX). Set the sample rate to 4 MHz, capture time 2 s, trigger on channel 0's falling edge.
2. Add a decoder named UART. Set baud 115200, 8 data bits, parity none, 1 stop bit, and set the decoder's RX to read channel 0.
   (The names RX and TX in the decoder's settings refer to which wire the decoder reads, not which side of the board they belong to.)
3. Press UART Echo on screen. Compare the bytes the decoder reads against the `TX:` line on screen — every byte must match. Count how many times the packet was sent, and how far apart.
4. Measure the start bit's width, calculate the real baud rate from the capture, and compare it against 115200.
5. **Deliberately get it wrong.** Change the decoder's baud to 57600 and 9600. Record what the decoder shows, and explain it using section 3.
6. Watch channel 1 (RX). If nothing answers, the wire stays idle at 1 the whole time. If you have an ESP32-S3 board as the example's README describes, you should see a 5-byte reply starting with 0x5A.

| Decoder's baud | What you see |
|---|---|
| 115200 | |
| 57600 | |
| 9600 | |

## Going further

A logic analyzer can tell you when a signal is 0 or 1, but not what the real voltage looks like. The next lesson, [Oscilloscope basics](../../m05-oscilloscope/l01-scope-basics/README.md),
will show us signal edges, overshoot, and noise that a logic analyzer cannot see. If you want to go further with I2C on this board, see the lesson
[Driving an RGB matrix over I2C in the TESAIoT Firmware Stack course](../../../tesaiot-firmware-stack/m04-qwa309-hardware/l03-rgb-matrix-i2c/README.md).

## Reflect

Next time a program tells you "sent" or "device not found," how many minutes would it take to prove with a logic analyzer what really happened on the wire — and is that worth more than guessing?

## References

- [sigrok protocol decoders](https://sigrok.org/wiki/Protocol_decoders)
- [Texas Instruments: Understanding the I2C Bus (SLVA704)](https://www.ti.com/lit/an/slva704/slva704.pdf)
- [SDK: cm33/sensors/01_i2c_bus_scan.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/01_i2c_bus_scan.c)
- [Texas Instruments: I2C Bus Pullup Resistor Calculation (SLVA689)](https://www.ti.com/lit/an/slva689/slva689.pdf)
- [SDK: the QWA309 base board's capability map (kit-tesaiot-pse84-ai/README.md)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-mpy/bento_libs/claw/kit-tesaiot-pse84-ai/README.md)
- [Code of QWA309 Header I/O Test (Developer Hub, commit 372d0d8)](https://github.com/tesaiot/developer-hub/blob/372d0d849578a6a49b634d3ecaab8b5958166921/prac_qwa309_header_hw_test/header_tester_ui.c)
