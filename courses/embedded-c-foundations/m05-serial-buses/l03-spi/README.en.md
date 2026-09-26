---
id: c-found.m05.l03
lang: en
title: {th: SPI, en: SPI}
summary: {th: เข้าใจโหมดของ SPI และสาย chip select แล้วยืนยันสัญญาณด้วย logic analyzer, en: 'Understand SPI modes and chip select, and verify signals with a logic analyzer.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m05.l02]
objectives:
- {th: อธิบายโหมด SPI ทั้งสี่จาก CPOL และ CPHA และเลือกโหมดให้ตรงกับ datasheet ของอุปกรณ์ได้, en: Explain the four SPI modes from CPOL and CPHA and match a device datasheet.}
- {th: 'ถอดรหัสภาพสัญญาณ SPI ได้ครบ SCLK, MOSI, MISO และ CS', en: 'Decode an SPI trace with SCLK, MOSI, MISO and CS.'}
- {th: เปรียบเทียบ SPI กับ I2C ในด้านจำนวนสาย ความเร็ว และการต่ออุปกรณ์หลายตัว, en: 'Compare SPI and I2C on wire count, speed and multi-device wiring.'}
develops:
- {skill: proto.spi, to: 3}
- {skill: meas.logic-analyzer, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
source_sha256: 3d9536d9946a1c5d4e8d98e5897ce352d9967561321587aacadf84a124f2a436
---

## Objectives

By the end of this lesson, you will be able to

1. Explain the four SPI modes in terms of CPOL and CPHA, and choose the mode that matches a device's datasheet.
2. Decode an SPI trace in full: SCLK, MOSI, MISO and CS.
3. Compare SPI and I2C on wire count, speed, and wiring several devices.

Takes about 70 minutes (concepts 15 · practice 25 · lab 25 · check 5). The lab needs a four-channel logic analyzer that can accept 3.3 V.

## Before you start

Two review questions from the previous two lessons.

1. Which bit does UART send first, and which bit does I2C send first (lessons 5.1 and 5.2)?
2. In I2C, how does the master pick which device to talk to? Without an address, what else could be used to pick one?

## See it work first

Open [examples/13_spi_modes.c](examples/13_spi_modes.c). This program draws the byte `0xA5` in all four SPI modes, marking a `^` under the edge where the receiver samples the value. **Predict before you run it:** in mode 3, does the receiver sample on SCLK's rising or falling edge?

```sh
gcc -std=c11 -Wall -Wextra -o spi_modes examples/13_spi_modes.c
./spi_modes
```

Mode 3 samples on the rising edge, just like mode 0, even though SCLK idles at a different level. Modes 1 and 2 sample on the falling edge. The last lines compare two real SPIs on this board — the radar's hardware SPI at 25 MHz against the header's bit-banged SPI at around 67 kHz — hundreds of times slower.

## Concepts

### 1. Four wires, four modes

SPI has four signals: SCLK (the master's clock), MOSI (master out), MISO (slave out), and CS or SS (selects a slave, usually active low). Data travels in both directions at once — every SCLK beat, the master sends one bit and receives one bit. "Reading" from a slave therefore always means sending something out at the same time.

| Mode | CPOL (SCLK's idle level) | CPHA | Receiver samples at | Name in the PDL's settings |
|---|---|---|---|---|
| 0 | 0 (low) | 0 | First edge = rising | `CY_SCB_SPI_CPHA0_CPOL0` |
| 1 | 0 (low) | 1 | Second edge = falling | `CY_SCB_SPI_CPHA1_CPOL0` |
| 2 | 1 (high) | 0 | First edge = falling | `CY_SCB_SPI_CPHA0_CPOL1` |
| 3 | 1 (high) | 1 | Second edge = rising | `CY_SCB_SPI_CPHA1_CPOL1` |

Choosing a mode isn't guesswork — every device's datasheet states it, either by mode name, by CPOL/CPHA values, or with a timing diagram showing which edge the data is sampled at. If the datasheet only gives a diagram, look for two things: which level SCLK idles at (CPOL), and whether data must be stable at the first edge or the second (CPHA). The SPI connected to the radar in the SDK's BSP is set to `subMode = CY_SCB_SPI_MOTOROLA`, `sclkMode = CY_SCB_SPI_CPHA0_CPOL0` (mode 0), `enableMsbFirst = true`, 8-bit data, and CS active low on every pin ([cycfg_peripherals.c lines 645-673](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_peripherals.c#L645-L673)).

### 2. Real SPI on this board: hardware versus bit-banged

**The BGT60TR13C radar's SPI** uses SCB3, with MISO on P21.4, MOSI on P21.5, CLK on P21.6, CS on P21.7, and an IRQ pin on P20.3, at 25 Mbps ([02_radar_presence.c lines 25-29](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/sensors/02_radar_presence.c#L25-L29)). This number matches the arithmetic: a 100 MHz clock, a divider of 0, and `oversample = 4`, exactly as the PDL's documentation says a master needs clk_scb equal to oversample times the data rate. The radar's task configures SPI with `Cy_SCB_SPI_Init()`, binds an ISR with `Cy_SysInt_Init()`, selects the slave with `Cy_SCB_SPI_SetActiveSlaveSelect()`, then calls `Cy_SCB_SPI_Enable()` ([radar_task.c lines 152-173](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/radar_task.c#L152-L173)), and the actual transfers use interrupt-driven `Cy_SCB_SPI_Transfer()`.

The SDK's radar platform file contains a great debugging lesson. Its original driver waited for a transfer to finish with an unbounded `while` loop — if the SPI interrupt was ever missed once, this loop would spin forever. The SDK team measured this on a real board and found the Radar page's values stuck every time, after about eight seconds of running, so they changed it to a bounded wait that cancels the transfer and returns an error instead. "A bounded spin turns an unrecoverable wedge into an error return." ([bento_bgt60trxx_platform.c lines 11-36 and 85-102](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/bento_bgt60trxx_platform.c#L11-L102), Apache-2.0, original Copyright 2022 Infineon Technologies AG, adapted in tesaiot-pse84-devkit-sdk)

**SPI on the header**, in the Developer Hub's Header I/O Test example, is bit-banged mode 0 on P9.3 (SCK), P9.2 (MOSI), P9.1 (MISO), P9.0 (CS). The CPU sets each pin one bit at a time with `Cy_GPIO_Write()`, delaying 5 microseconds between steps — much slower than hardware, but easy to read with a logic analyzer, and enough for an 8-byte test. (The SDK's radar example documentation warns of a header "chip-select trap" between P9.0 and P9.2 — in the lab, go by the pins the example you flashed prints on its screen.)

### 3. SPI versus I2C

| Aspect | SPI | I2C |
|---|---|---|
| Wire count | 3 shared wires (SCLK, MOSI, MISO) + one CS per slave | 2 shared wires (SCL, SDA) for every device |
| Selecting a device | With the CS wire | With a 7-bit address in the data |
| Speed on this board | The radar's SPI: 25 MHz | The sensor bus: 400 kHz |
| Direction | Full-duplex, send and receive at once | Half-duplex |
| Receiver confirms receipt | No (no ACK) | Yes, ACK/NACK per byte |
| Wire characteristics | Push-pull, sharp edges, drives fast | Open-drain with pull-ups, speed limited by wire capacitance |

SPI suits high-volume data from a few devices — a radar, a display, flash memory. I2C suits many low-data-rate sensors, saving chip pins. Because SPI has no ACK, proving a wire is good means reading a value you already know the answer to, such as a chip's ID register — the same approach used with I2C in lesson 5.2.

## Worked example

[examples/13_spi_modes.c](examples/13_spi_modes.c) runs in three parts.

- **Part 1** produces the waveform of one byte, MSB first, following each mode's CPOL and CPHA.
- **Part 2** draws SCLK and MOSI as lines, with the idle level before and after the frame, and a `^` under the sampled edge.
- **Part 3** compares the radar's hardware SPI speed against the header's bit-banged one.

Try changing things and predicting the result before you run it.

1. Change the byte to `0x31`, the second byte the Header I/O Test example sends, and draw it in mode 0.
2. If the master uses mode 0 but the slave uses mode 1, which edge does the slave sample at, and how would the resulting data likely be corrupted?
3. Adjust it to print LSB first, and explain what setting has to match between the master and the decoder for this to work.

## Practice

Open [practice/13_spi_decode.c](practice/13_spi_decode.c), a four-wire SPI decoder like a logic analyzer's. This is module 5's last lesson, so there are the most gaps to fill in: 6.

1. Extract CPOL and CPHA from the mode number.
2. Clear state whenever CS is inactive.
3. Tell the leading edge apart from the trailing edge.
4. Choose which edge to sample, based on CPHA.
5. Shift bits into a byte MSB first, from the value that was stable before the edge.
6. Store the byte once 8 bits are collected, without writing past the storage.

```sh
gcc -std=c11 -Wall -Wextra -o spi_decode practice/13_spi_decode.c && ./spi_decode
```

The tests use the real frame the Header I/O Test example sends the first time SPI is pressed: `A5 31 00 5A 01 02 03`, followed by an XOR checksum `CE`, plus a case with the wrong mode set, where the decoder must get bytes that don't match what was sent.

## Solution

Try it yourself for at least 15 minutes first, then open [solution/13_spi_decode.c](solution/13_spi_decode.c). The key point: the solution reads the value from `s[i - 1]`, the value that was stable before the edge — the same thing a receiver's flip-flop actually captures. If the other side changes the data right at that same edge (a mode mismatch), the receiver gets the previous round's bit. The wrong-mode test case exists to prove this. Notice that this test passes even before you fill anything in, because empty code also produces a mismatched byte. A test that passes against empty code only means something once its paired test (decoding with the correct mode, getting `A5`) also passes.

## Check your understanding

Answer the 5 questions in [quiz.yaml](quiz.yaml) (shown at the bottom of this page on the website), covering all three objectives. Getting 4 or more right counts as finishing the lesson.

## Lab

**Task:** capture a real SPI transaction on the header, decode it by eye and with a decoder, and prove the effect of setting the wrong mode.

1. Flash the [QWA309 — Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) example from the Developer Hub (if you haven't already in lesson 5.1).
2. Connect a four-channel logic analyzer to P9.3 (SCK), P9.2 (MOSI), P9.1 (MISO), P9.0 (CS), and ground. Check the pin names against the `Port:` line the example prints on screen when you press the button.
3. Set the trigger to CS's falling edge, then press the **SPI ESP32** button on screen. The screen prints a `TX req:` line with eight bytes. (With no paired test board, the screen shows FAIL, but the master still sends the frame out every time.)
4. Decode the first byte by eye: which level does SCLK idle at, which edge is MOSI stable at, then read 8 bits MSB first. You should get `A5`.
5. Set the decoder to SPI mode 0, MSB first, CS active low, and compare it against the `TX req:` line. Then change the decoder to mode 1 and see what the byte changes to.
6. Measure the length of one bit and how long CS stays low, and compare with the worked example's estimate of about 15 microseconds per bit. How much do they differ, and why?

**Evidence to keep in your portfolio:** a four-channel waveform picture with the first byte labelled by hand, a picture of the decoder's mode-0 result matching `TX req:`, a picture of the result when set to mode 1, and the timing numbers you measured in step 6.

## Going further

- Read the "Configure Data Rate" section in the header of [`cy_scb_spi.h` @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_scb_spi.h), and calculate the divider and oversample setting needed for 10 MHz SPI from a 100 MHz clock.
- Look at [sigrok protocol decoders](https://sigrok.org/wiki/Protocol_decoders) and see how an SPI decoder can be layered with a device decoder (such as an SPI flash chip).
- Challenge: use this lesson's decoder to read a CSV file you exported from your own PulseView capture.

Next lesson, moving into module 6: [lesson 6.1, unit tests on the host](../../m06-test-and-ci/l01-unit-tests-on-host/README.md)

## Reflect

- If a new device's datasheet only gave a timing diagram, what would you read off it to choose a mode, and how would you prove you chose correctly?
- How many unbounded wait loops are in your own code, and what would happen if the interrupt one of them waits for were ever missed once?

## References

- [Infineon mtb-pdl-cat1 (Peripheral Driver Library) @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/tree/release-v3.24.0)
- [SDK: cm55/sensors/02_radar_presence.c (the radar SPI's pins and speed)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/sensors/02_radar_presence.c)
- [SDK: tesaiot-radar/bento_bgt60trxx_platform.c (a bounded SPI wait)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/bento_bgt60trxx_platform.c)
- [sigrok protocol decoders](https://sigrok.org/wiki/Protocol_decoders)
- [Serial Peripheral Interface (Wikipedia)](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface)

## Examples on the TESAIoT Developer Hub

Try the real thing on the TESAIoT Dev Kit: open an example on the Developer Hub to read the code, download it, or flash a prebuilt firmware image.

- [QWA309 — Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) — diagnostic: tests all Arduino header I/O (I2C 3V3, UART SCB9, bit-banged SPI, GPIO P13, PWM, an ADC net, and 4000T EZI2C), with a console UI.
