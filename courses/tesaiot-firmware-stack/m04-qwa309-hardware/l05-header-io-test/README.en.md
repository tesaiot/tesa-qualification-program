---
id: fw-stack.m04.l05
lang: en
title:
  th: "ทดสอบ I/O บน header: I2C UART SPI GPIO PWM ADC"
  en: "Header I/O test: I2C, UART, SPI, GPIO, PWM, ADC"
summary:
  th: "ทดสอบ I/O บน header: I2C UART SPI GPIO PWM ADC"
  en: "Header I/O test: I2C, UART, SPI, GPIO, PWM, ADC"
level: L3
time_min: {concept: 10, practise: 25, lab: 30, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m01.l01]
objectives:
  - th: "ทดสอบขา I/O บน header ครบทุกชนิดด้วยโปรแกรม diagnostic และอ่านผลจากคอนโซลบนจอ"
    en: "Exercise every I/O type on the header with the diagnostic program and read the on-screen console"
  - th: "ยืนยันสัญญาณอย่างน้อยหนึ่งชนิดด้วย logic analyzer หรือออสซิลโลสโคป"
    en: "Confirm at least one signal with a logic analyzer or oscilloscope"
develops:
  - {skill: proto.uart, to: 2}
  - {skill: proto.spi, to: 1}
  - {skill: proto.i2c, to: 2}
  - {skill: mcu.pwm, to: 1}
  - {skill: meas.logic-analyzer, to: 1}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "prac_qwa309_header_hw_test"
  ref: e5c772252e7d20f715463e0d27df9ece4e569c38
source_sha256: e687d74f7246da9c5239e6d2afdb1f895f9ca0cfa56371f34feca654100eec86
---

# Header I/O test: I2C, UART, SPI, GPIO, PWM, ADC

## Objectives

1. Exercise every I/O type on the header with the diagnostic program and read the on-screen console
2. Confirm at least one signal with a logic analyzer or oscilloscope

## Concepts

### What the QWA309 base board gives you to practise with

The QWA309 base board of the TESAIoT Dev Kit gives you real hardware to practise with: push buttons, four potentiometers, a CAN transceiver and a header for external devices. This lesson uses Developer Hub exercises written specifically for this board. This lesson turns the QWA309's header into a diagnostic tool that exercises every I/O type the header supports in a single program — I2C, UART, SPI, GPIO, PWM and ADC/PWM3 — where most tests need a wired-up ESP32-S3 companion board running simulator firmware as the test partner.

### What the diagnostic tool tests, and through which pins

The screen has a separate test button per bus: **Scan** searches for devices on the display/touch I2C bus (`DISPLAY_I2C_CONTROLLER_HW`); **I2C ESP32** talks to the ESP32 simulator at address `0x30`; **UART Echo** goes through SCB9 (`P15.1` = TX, `P15.0` = RX at 115200 8N1); **SPI ESP32** goes through bit-banged SPI on `P9.0`–`P9.3` (CS/MISO/MOSI/SCK); **GPIO In/Out** goes through six pins (`P13.0`, `P13.3`–`P13.7`); **PWM Out** drives the complementary PWM5 pair (`P13.3`/`P13.4`); and **ADC In**/**PWM3 Out** use the ADC/PWM3 net pin pair (`P15.2`/`P15.3`). Each button runs its test non-blockingly via `lv_timer_create()`, then prints the result into an on-screen console built with `lv_textarea_create()`, timestamped. Pressing any button temporarily disables the others until that test finishes.

### Confirming a reply with a small protocol: magic byte + counter + checksum

The tests that need to talk to the ESP32 (I2C, UART, SPI) all use the same packet shape: a fixed first magic byte (request `ESP32_SIM_REQ_MAGIC = 0xA5`, response `ESP32_SIM_RSP_MAGIC = 0x5A`), followed by a command byte, a counter that increments on every send, and finally a checksum from `xor_checksum()`, which XORs every preceding byte together. The receiving side checks the magic, the counter and the checksum — all three — before declaring PASS; failing that, it retries up to a set count (for example `UART_TEST_RETRIES`). This three-layer check confirms that the ESP32 test partner actually received "this" request (not a stale answer left over from before) and that the data was not corrupted in transit — but it only confirms the one path being tested; it says nothing about whether any other pin on the header works.

### Scanning I2C only across the range the standard reserves for ordinary use

`run_i2c_scan()` steps through addresses from `I2C_SCAN_MIN_ADDR = 0x08` to `I2C_SCAN_MAX_ADDR = 0x77`, not the full 7-bit range 0x00–0x7F, because 0x00–0x07 and 0x78–0x7F are reserved by the I2C standard for special purposes — for example the general call address, which multiple devices may answer at once, and the 10-bit addressing scheme. Probing a reserved address can trigger unintended behaviour; ordinary I2C devices never use addresses in that range. The function prints the results as a 16-column-by-8-row hex table, the same layout common I2C scanner tools use.

### Bit-banged SPI: the CPU toggles the pins itself, one bit at a time, instead of hardware

`spi_transfer_frame()` never touches the chip's SPI peripheral at all — it drives `P9.3` (SCK), `P9.2` (MOSI), `P9.1` (MISO) and `P9.0` (CS) with plain `Cy_GPIO_Write()`/`Cy_GPIO_Read()` calls. It lowers CS, then loops bit by bit from the MSB: write MOSI, delay with `Cy_SysLib_DelayUs(5U)`, raise SCK, delay another 5 µs, read MISO and store the bit, lower SCK — mode 0 (clock idles LOW, sampled on the rising edge). The upside is that any pin can be used, which suits a test tool; the downside is that it is far slower than hardware (the CPU is busy the whole transfer) and the clock timing can jitter if an interrupt intervenes — unlike hardware SPI (SCB), which shifts bits with dedicated circuitry and a steadier clock. The difference is clearly visible on a logic analyzer.

### PWM the board can send but cannot verify itself: reports "SENT", not "PASS"

`run_pwm_output_test()` generates a complementary PWM5 pair (`P13.3` = PWM5+, `P13.4` = PWM5−) by toggling `Cy_GPIO_Write()` directly in a loop, again with no PWM peripheral involved. At `PWM_TEST_HALF_PERIOD_MS = 20` ms per half-cycle (a full period of 40 ms, roughly 25 Hz), it repeats for `PWM_TEST_CYCLES = 50` cycles. Because the board can command the output pins but has no way to verify the signal actually reached the far end, the result is reported as "SENT" (sent), never "PASS" (confirmed passing) — that confirmation has to come from the ESP32 side or an external measurement tool. One thing worth watching for specifically is a both-high fault (both pins HIGH at once), which is dangerous for a circuit driven by a complementary signal pair.

### Trusting the measuring instrument before the software result, when they disagree

If the program reports PASS (having checked the magic/counter/checksum fully) but a connected logic analyzer sees no signal at all, check the measurement setup before concluding the software result is wrong: the pin and ground actually connected, the instrument's threshold level, sample rate and trigger settings. Then measure again on a signal whose outcome is already known for certain (for instance, the pin currently under test) before comparing against the program's result — only after that should the code or the hardware itself be suspected. The underlying principle: validate the instrument first, before trusting the number it reports.

## Worked example

The QWA309 exercise set on the Developer Hub (pinned to commit `e5c7722`) runs only on the TESAIoT Dev Kit, because it uses hardware on the base board.

- **QWA309 — Header I/O Test** — a diagnostic that exercises every Arduino header I/O (I2C 3V3, UART SCB9, bit-banged SPI, GPIO P13, PWM, an ADC net, 4000T EZI2C) with a console UI
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_header_hw_test/README.md) · [code](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_header_hw_test) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test)

The excerpts below are copied from the actual files at the same commit (Apache-2.0, tesaiot/developer-hub).

[`header_tester_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_header_hw_test/header_tester_ui.c) — the checksum that confirms data was not corrupted in transit:

```c
static uint8_t xor_checksum(const uint8_t *data, uint32_t size)
{
    uint8_t checksum = 0U;

    for (uint32_t i = 0U; i < size; i++)
    {
        checksum ^= data[i];
    }

    return checksum;
}
```

[`header_tester_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_header_hw_test/header_tester_ui.c) — scans I2C only across the range the standard reserves for ordinary devices:

```c
for (uint8_t row = 0U; row < 8U; row++)
{
    for (uint8_t col = 0U; col < 16U; col++)
    {
        uint8_t address = (uint8_t)(row * 16U + col);

        if ((address < I2C_SCAN_MIN_ADDR) || (address > I2C_SCAN_MAX_ADDR))
        {
            continue;   /* reserved range, not a normal device address */
        }

        bool device_found = probe_i2c_address(address, NULL);
        /* ... record into found_addresses[], print into row_text ... */
    }
}
```

[`header_tester_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_header_hw_test/header_tester_ui.c) — bit-banged SPI: the CPU toggles the pins itself, one bit at a time, mode 0:

```c
for (int8_t bit = 7; bit >= 0; bit--)
{
    uint32_t tx_bit = ((tx[byte_index] >> (uint8_t)bit) & 0x01U);

    Cy_GPIO_Write(HEADER_SPI_MOSI_PORT, HEADER_SPI_MOSI_PIN, tx_bit);
    Cy_SysLib_DelayUs(5U);
    Cy_GPIO_Write(HEADER_SPI_CLK_PORT, HEADER_SPI_CLK_PIN, 1U);
    Cy_SysLib_DelayUs(5U);

    if (Cy_GPIO_Read(HEADER_SPI_MISO_PORT, HEADER_SPI_MISO_PIN) != 0U)
    {
        rx_byte |= (uint8_t)(1U << (uint8_t)bit);
    }

    Cy_GPIO_Write(HEADER_SPI_CLK_PORT, HEADER_SPI_CLK_PIN, 0U);
    Cy_SysLib_DelayUs(5U);
}
```

[`header_tester_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_header_hw_test/header_tester_ui.c) — complementary PWM5 driven directly with GPIO; the result reports "SENT", not "PASS":

```c
for (uint32_t cycle = 0U; cycle < PWM_TEST_CYCLES; cycle++)
{
    Cy_GPIO_Write(P13_3_PORT, P13_3_PIN, 1U);
    Cy_GPIO_Write(P13_4_PORT, P13_4_PIN, 0U);
    Cy_SysLib_Delay(PWM_TEST_HALF_PERIOD_MS);

    Cy_GPIO_Write(P13_3_PORT, P13_3_PIN, 0U);
    Cy_GPIO_Write(P13_4_PORT, P13_4_PIN, 1U);
    Cy_SysLib_Delay(PWM_TEST_HALF_PERIOD_MS);
}
/* Result: SENT - not PASS; the board cannot verify the far end. */
```

## Common mistakes

- **Assuming a PASS on one path means every other header pin works too** — the magic/counter/checksum protocol only confirms the one path actually tested; every other pin needs its own separate test.
- **Scanning I2C across the full 0x00–0x7F range** — 0x00–0x07 and 0x78–0x7F are reserved by the standard; probing them can trigger special behaviour, such as the general call address that multiple devices answer at once.
- **Assuming bit-banged SPI behaves identically to hardware SPI in every way** — bit-banging is flexible about which pins to use but slower, and its clock can jitter under interrupts, unlike SCB hardware SPI's steadier clock.
- **Seeing PWM Out's "SENT" result and concluding it passed** — the board can drive the output pins but cannot verify the signal reaches the far end itself; that confirmation needs an external measurement tool or the ESP32 side.
- **Trusting the measuring instrument the instant it disagrees with the software result** — check the instrument's own setup first (cable, ground, threshold, sample rate, trigger) by measuring a signal whose outcome is already known, before comparing.

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- How does bit-banged SPI differ from hardware SPI?
- If the program reports UART passed but the logic analyzer sees no signal, which do you trust?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [All TESAIoT Dev Kit exercises](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38) · commit `e5c7722`
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
