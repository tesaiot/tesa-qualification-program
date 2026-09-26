# TESAIoT Firmware Stack: C Firmware on the TESAIoT Dev Kit

The core TESA Qualification Program course for developers. You write C firmware for the **TESAIoT Dev Kit**
(the PSoC Edge AI Kit SoM on the QWA309 base board) with ModusToolbox and TESA's **master template**.
Every lesson is tied to a real example on the [TESAIoT Developer Hub](https://dev.tesaiot.dev/)
([github.com/tesaiot/developer-hub](https://github.com/tesaiot/developer-hub)), pinned to an exact commit.

| | |
|---|---|
| Level | L3 Independent |
| Time | about 25 hours |
| Board | TESAIoT Dev Kit (lesson 5.3 uses the Eva Kit, as its example's BSP does) |
| Tools | ModusToolbox 3.6 or later, git, a USB-C cable for KitProg3 |
| You should know | C at level L2 (variables, functions, basic pointers and structs) |

## Outcomes

1. Build and flash C firmware to the TESAIoT Dev Kit with ModusToolbox and the master template on your own.
2. Build a touch-screen HMI with LVGL, from a label to a Wi-Fi manager with a state machine and NVM profiles.
3. Read every on-board sensor and the PDM microphone and combine them into a smooth dashboard.
4. Use GPIO, ADC, I2C, CAN, UART, SPI and PWM on the QWA309 base board and confirm signals with an instrument.
5. Send data to the TESAIoT Platform with Server-TLS and mTLS, and explain the role of OPTIGA™ Trust M.

## Modules

| Module | Lessons | Examples from |
|---|---|---|
| [1 · Getting started with the TESAIoT Dev Kit](m01-getting-started/README.md) | 1 | master template (`tesaiot_dev_kit_master`) |
| [2 · HMI Menu & Setting with LVGL](m02-hmi-menu-setting/README.md) | 7 | Episodes series 1 (`hmi_ep01`–`hmi_ep07`) |
| [3 · Sensors and audio on the TESAIoT Dev Kit](m03-interactive-sensors/README.md) | 7 | Episodes series 2 (`int_ep01`–`int_ep07`) |
| [4 · Hardware on the QWA309 base board](m04-qwa309-hardware/README.md) | 5 | practice codes `prac_qwa309_*` |
| [5 · Connecting to the TESAIoT Platform securely](m05-connect-to-platform/README.md) | 4 | `embedded-devices` and `security` examples |

The lesson pages are in Thai for now; the code and every example README they link to are on GitHub.

## Where the code lives

All code stays in the Developer Hub and is linked at pinned commits, never copied, so there is one source.
The episodes, the practice codes and the examples on `main` are Apache-2.0; the master template and the OPTIGA
client are under Infineon/Cypress EULAs.

## How to cite TESA

> "TESAIoT Firmware Stack: C Firmware on the TESAIoT Dev Kit" from TESA Open Knowledge by the Thai Embedded Systems
> Association (TESA), https://github.com/tesaiot/tesa-qualification-program, licensed under CC BY-NC 4.0

Add "(adapted)" when you change it. The example code is the TESAIoT Firmware Stack by the Thai Embedded Systems
Association (TESA) in [tesaiot/developer-hub](https://github.com/tesaiot/developer-hub). See [ATTRIBUTION.md](../../ATTRIBUTION.md).
