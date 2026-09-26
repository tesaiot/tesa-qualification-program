
# Module 3 — GPIO and Basic Peripherals

*GPIO and Basic Peripherals* · [TESA Firmware SDK for Edge AI](../README.md) course

## Objectives

Talk to hardware through the Driver layer: LEDs, buttons, UART, I²C, PWM and ADC, on the project you can build/flash from Module 2, then combine them into a small circuit.

## Lessons

| # | Lesson | Content |
|---|---|---|
| 1 | [GPIO and peripherals through the Driver API](l01-gpio-and-peripherals/README.md) | Controlling LEDs, buttons, UART, I²C, PWM and ADC through the Driver layer, and knowing where SPI and timers sit in the stack |
| 2 | [Lab: GPIO and peripherals on real hardware](l02-lab/README.md) | Hands-on block by block: LED + button, UART logging, then choosing at least one of PWM / ADC / I²C, before combining them into a mini circuit |

Approximate time per the original: about 3 hours (lessons) + a 2.5–3 hour lab.

Accompanying sheets and templates (in the `resources/` folder of lesson 1):

- [peripheral-api-map.md](l01-gpio-and-peripherals/resources/peripheral-api-map.md)

> The C code in this module uses the API of the TESAIoT Bitstream firmware, which is not yet open source. Read the note at the top of the [lesson](l01-gpio-and-peripherals/README.md) before you start.

## Checkpoint

Before moving to the next module, check that you can do the following:

- [ ] A button toggles an LED on the real board
- [ ] There is a log over UART you can read on a terminal
- [ ] At least one of PWM, ADC or I²C works, with the real function names you called noted in the sheet

[← Module 2](../m02-toolchain/README.md) · [Course page](../README.md) · [Module 4 →](../m04-rtos/README.md)
