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
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "prac_qwa309_header_hw_test"
  ref: e5c772252e7d20f715463e0d27df9ece4e569c38
source_sha256: 9f4cacef5151038df6918e25e29468cb8097a5c913a24c731645824afb5f10d4
---

# Header I/O test: I2C, UART, SPI, GPIO, PWM, ADC

## Objectives

1. Exercise every I/O type on the header with the diagnostic program and read the on-screen console
2. Confirm at least one signal with a logic analyzer or oscilloscope

## Concepts

The QWA309 base board of the TESAIoT Dev Kit gives you real hardware to practise with: push buttons, four potentiometers, a CAN transceiver and a header for external devices. This lesson uses Developer Hub exercises written specifically for this board.

## Worked example

The QWA309 exercise set on the Developer Hub (pinned to commit `e5c7722`) runs only on the TESAIoT Dev Kit, because it uses hardware on the base board.

- **QWA309 — Header I/O Test** — a diagnostic that exercises every Arduino header I/O (I2C 3V3, UART SCB9, bit-banged SPI, GPIO P13, PWM, an ADC net, 4000T EZI2C) with a console UI
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_header_hw_test/README.md) · [code](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_header_hw_test) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test)

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
