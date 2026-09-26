---
id: c-found.m05.l01
lang: en
title: {th: UART, en: UART}
summary: {th: เข้าใจเฟรมของ UART และกติกาเจ้าของพอร์ตเดียว แล้วยืนยันด้วย logic analyzer, en: 'Understand UART framing and the single-owner rule, and verify it with a logic analyzer.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m04.l04]
objectives:
- {th: 'ถอดรหัสเฟรม UART หนึ่งเฟรมจากภาพสัญญาณได้ครบ start bit, data, parity และ stop bit', en: 'Decode one UART frame from a trace: start bit, data, parity and stop bit.'}
- {th: อธิบายว่าทำไม UART หนึ่งพอร์ตควรมีเจ้าของเพียงงานเดียว และส่งต่อข้อมูลผ่านบัฟเฟอร์, en: Explain why one UART port should have a single owner task that hands data on through a buffer.}
- {th: ตั้งค่า logic analyzer ให้ถอดรหัส UART ที่ baud rate ที่กำหนดได้, en: Set up a logic analyzer to decode UART at a given baud rate.}
develops:
- {skill: proto.uart, to: 3}
- {skill: meas.logic-analyzer, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
source_sha256: 0ab20248dff4fe8e66aa7204d3faf16c9f68cf8dfa6d56e411eb2c5837038594
---

## Objectives

By the end of this lesson, you will be able to

1. Decode one UART frame from a trace, in full: the start bit, data, parity and stop bit.
2. Explain why one UART port should have exactly one owner task, handing data on through a buffer.
3. Set up a logic analyzer to decode UART at a given baud rate.

Takes about 70 minutes (concepts 15 · practice 25 · lab 25 · check 5). The lab needs a logic analyzer that can accept 3.3 V signals, and [PulseView](https://sigrok.org/wiki/PulseView) or a manufacturer's program that can decode UART.

## Before you start

Two review questions from earlier lessons.

1. This board's debug UART uses a 100 MHz clock, a divider of 86, and 10x oversampling — what is the real baud rate, and how far off is it from 115200, as a percentage (lesson 4.2)?
2. In the ring buffer from lesson 1.3, what does the writer change, and what does the reader change?

## See it work first

Open [examples/11_uart_frame.c](examples/11_uart_frame.c). This program draws the waveform of one byte on a UART wire. **Predict before you run it:** for the byte `0xA5`, is the first bit after the start bit a 1 or a 0?

```sh
gcc -std=c11 -Wall -Wextra -o uart_frame examples/11_uart_frame.c
./uart_frame
```

The first bit is 1, because UART sends the **least significant bit (LSB) first**. `0xA5` is `1010 0101`, so on the wire it appears in the order 1 0 1 0 0 1 0 1, reading left to right. At 115200 baud, one bit lasts 8.68 microseconds, and one 8N1 frame is ten bits long. This same byte is the first one you'll capture from the board's pins in the lab.

## Concepts

### 1. One UART frame

UART has no clock wire. Both sides agree on a speed (the baud rate) beforehand, and use the start bit's edge as the timing reference point.

```
 idle  start  D0  D1  D2  D3  D4  D5  D6  D7  [parity]  stop  idle
 ‾‾‾‾‾\_____/‾‾‾ ... 8 bits of data, LSB first ...  [P]      ‾‾‾‾  ‾‾‾‾
```

| Part | Level | Purpose |
|---|---|---|
| idle | 1 | An idle wire is held high |
| start | 0 | A falling edge tells the receiver a frame is starting; the receiver counts time from this edge |
| data | follows the data | 5 to 9 bits, most commonly 8, LSB first |
| parity (if present) | follows the rule | even or odd, making the total count of 1s even or odd; catches only an odd number of flipped bits |
| stop | 1 | 1 or 2 bits; if the receiver sees a 0 here, that's a framing error, usually meaning the baud rates don't match |

The debug UART's settings in the SDK's BSP match 8N1 in every respect: `dataWidth = 8UL`, `parity = CY_SCB_UART_PARITY_NONE`, `stopBits = CY_SCB_UART_STOP_BITS_1`, `enableMsbFirst = false`, and `oversample = 10` ([cycfg_peripherals.c lines 584-608](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_peripherals.c#L584-L608)). Oversampling is how many clock beats fall within one bit; the receiver uses it to find the middle of the bit, the point furthest from either edge, which gives it some tolerance for baud rate mismatch. The template opens this port in `init_retarget_io()` with `Cy_SCB_UART_Init()` and `Cy_SCB_UART_Enable()`, then wires it to `printf` through retarget-io ([retarget_io_init.c lines 59-93](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/driver/retarget_io_init.c#L59-L93)).

### 2. One port, one owner

UART is a single stream of bytes. If two tasks read the same port, the bytes get split between them, and neither one gets a complete message. The SDK's [08_tacp_host_protocol.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/08_tacp_host_protocol.c#L17-L30) example (mtb-mpy variant) has a section titled "ONE OWNER. EXACTLY ONE.", explaining that "a split stream is not a protocol — a magic byte lands in one task and the command byte in the other, and both see garbage." Any other task that wants the data receives it from the owner instead, through a buffer — in that file, a ring buffer read with `tacp_ring_buf_read()`, which returns -1 when empty (lesson 1.3).

The transmit side has an owner too. Retarget-io's `printf` holds a mutex while printing, so the SDK's example runner sets its own task to priority 1, with the reasoning that this mutex has "no priority inheritance" — the lowest-priority task "can only ever be the waiter, never the holder that blocks somebody more important" ([sdk_examples_cm33.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sdk_examples_cm33.c)) — and `printf` from an ISR is strictly forbidden. In this template, CM33_NS owns the board's one console; CM55 has no console at all (lesson 2.1).

### 3. Reading a UART wire with a logic analyzer

A logic analyzer samples the wire's level as 0 or 1 many times per bit, and decoding software does the same thing a UART receiver does: find the start edge, then read the middle of each bit. Every setting must match the sender.

| Setting | For the UART on this board's header |
|---|---|
| Pin to probe | The header's TX, which is P15.1 (SCB9); always connect the analyzer's ground to the board's ground too |
| Voltage level | 3.3 V — check your analyzer can accept this |
| Sample rate | Several times the baud rate, e.g. 1 MHz or higher for 115200; higher gives sharper edges |
| Decoder | UART, baud 115200, 8 data bits, no parity, 1 stop bit, LSB first, not inverted |
| Trigger | A falling edge on TX, to capture the first frame |

This pin and format come from the SDK documentation's "Peripherals at a glance" table ("QWA309 header UART | P15.0 RX / P15.1 TX | SCB9, 115200 8N1"). If the decoder shows a framing error on every frame, suspect the baud rate first. If it shows bytes that look bit-reversed, suspect the bit order or signal polarity.

## Worked example

[examples/11_uart_frame.c](examples/11_uart_frame.c) runs in three parts.

- **Part 1**: `uart_encode()` produces the levels for the start bit, LSB-first data, parity, and stop.
- **Part 2**: `draw()` draws a text waveform labelled S, D0 through D7, P, T, with the timing of each bit and the whole frame.
- **Part 3**: draws `0xA5` in 8N1 and 8E1, and `0x11` (the second byte the Header I/O Test example sends), then calculates throughput.

Try changing things and predicting the result before you run it.

1. Change the baud to 9600. How long does a frame become, and if you need to send 200 bytes per second of logging, is 9600 enough?
2. Add `PARITY_ODD`. What does the parity bit for `0xA5` become?
3. Draw `0xB4` and compare it with the waveform you'll capture in the lab.

## Practice

Open [practice/11_uart_decode.c](practice/11_uart_decode.c), a decoder that works the same way a logic analyzer does. There are 3 gaps to fill in — this is module 5's first lesson, so there are fewer than usual.

1. Read the data bits at the middle of each bit, LSB first.
2. Check parity, both even and odd.
3. Check the stop bit, and return a framing error when it's wrong.

```sh
gcc -std=c11 -Wall -Wextra -o uart_decode practice/11_uart_decode.c && ./uart_decode
```

There's a test case for `0xFF`, which is real data, not "no data," and a case with the stop bit set to 0, simulating a baud mismatch.

## Solution

Try it yourself for at least 15 minutes first, then open [solution/11_uart_decode.c](solution/11_uart_decode.c). The comments in the solution point out a limitation of parity that's often forgotten: it only catches an odd number of flipped bits. If two bits flip at once, parity still checks out. Data that matters therefore needs a checksum or CRC at the message level too — the Header I/O Test example ends every packet with an XOR checksum, and the SDK's TACP uses CRC-16.

## Check your understanding

Answer the 5 questions in [quiz.yaml](quiz.yaml) (shown at the bottom of this page on the website), covering all three objectives. Getting 4 or more right counts as finishing the lesson.

## Lab

**Task:** capture a real UART frame from the board's pins with a logic analyzer, decode it by eye first, then confirm with a decoder.

1. Open the [QWA309 — Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) example on the Developer Hub, and flash the example's prebuilt firmware onto the board. (This example uses the Developer Hub's master template, not the SDK's template — an overview is in [TESAIoT Firmware Stack, lesson 1.1](../../../tesaiot-firmware-stack/m01-getting-started/l01-toolchain-and-master-template/README.md).)
2. Connect the logic analyzer: one channel to P15.1 (the header UART's TX) and ground. Check the pin location from the board's silkscreen or documentation. Set it up following the table in concept 3.
3. Start capturing, then press **UART Echo** on the screen. The screen will print a line `TX: A5 11 00 B4` (the third number increases every time you press it). With no paired test board connected, the screen shows FAIL because nothing answers — but the packet is still sent out the TX pin every time it retries. (The example calls `Cy_SCB_UART_PutArrayBlocking()` before waiting for a reply, and retries up to four times.)
4. **Decode it by eye first.** Zoom into the first byte's waveform, identify the start bit, all eight data bits, and the stop bit, then convert to hex. You should get `A5`. Measure the width of one bit with the program's cursors, and compare it against 8.68 microseconds.
5. Turn on the decoder and compare it against what you decoded by eye, and against the `TX:` line on the screen.
6. Try setting the decoder wrong, one setting at a time: baud 57600, parity even, bit order MSB first. Note what the decoder shows in each case.

**Evidence to keep in your portfolio:** a picture of the waveform with bits labelled by hand, a picture of the decoder's result matching the `TX:` line on the screen, the bit width you measured, and a table of symptoms for each of the three wrong settings.

## Going further

- The SDK's `08_tacp_host_protocol.c` example explains that `tacp_init()` clears the hardware's RX FIFO, which is correct at system start-up but wrong if called later. Read the "WHAT tacp_init() COSTS" section and explain why.
- [Universal asynchronous receiver-transmitter (Wikipedia)](https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter), the framing and break condition sections.
- Challenge: extend the exercise's decoder to read several frames back to back from one long signal, and decode the whole `A5 11 00 B4` packet, including checking the XOR checksum.

Next lesson: [lesson 5.2, I2C](../l02-i2c/README.md)

## Reflect

- If all you saw on a wire were framing errors, what three things would you check first, and in what order?
- Which job in your system wants to "secretly listen in" on someone else's UART, and how would you design it to receive data from the owner instead?

## References

- [SDK: cm33/connectivity/08_tacp_host_protocol.c (UART has a single owner)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/08_tacp_host_protocol.c)
- [SDK: the BSP's cycfg_peripherals.c (the debug UART's settings)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_peripherals.c)
- [Peripherals at a glance (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__peripherals__quickref.html)
- [sigrok PulseView](https://sigrok.org/wiki/PulseView)
- [Universal asynchronous receiver-transmitter (Wikipedia)](https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter)

## Examples on the TESAIoT Developer Hub

Try the real thing on the TESAIoT Dev Kit: open an example on the Developer Hub to read the code, download it, or flash a prebuilt firmware image.

- [QWA309 — Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) — diagnostic: tests all Arduino header I/O (I2C 3V3, UART SCB9, bit-banged SPI, GPIO P13, PWM, an ADC net, and 4000T EZI2C), with a console UI.
