# TESA Firmware SDK for Edge AI

A hands-on C firmware course on PSOC™ Edge E84: chip architecture and SDK layers, ModusToolbox™ + VS Code, peripherals, FreeRTOS, sensor data preparation for Edge AI, MQTT, BLE and a capstone.

> Original content by Asst. Prof. Dr. Santi Nuratch, Department of Control Systems and Instrumentation Engineering, Faculty of Engineering, King Mongkut's University of Technology Thonburi (KMUTT) (https://github.com/drsanti), supported by the Thai Embedded Systems Association (TESA). Imported from [drsanti/TESAIoT-Courses — C1](https://github.com/drsanti/TESAIoT-Courses/tree/287c21814ba8c75f693136616dcd270349a15966/C1) (commit `287c218`) under CC BY 4.0.

| | |
|---|---|
| Level | L3 · Independent |
| Status | alpha (imported, under review) |
| Estimated time | ~26 hours (sum of the source's module estimates) |
| Audience | developer, student, educator |
| Language | Lessons are in Thai with English technical terms and English section headings; English lesson translations are pending. |

## Before you start

Basic C (functions, pointers, structs and callbacks appear in every lesson) and comfort installing tools and using a terminal.

## What you need

- Board: TESAIoT PSoC Edge DevKit or Infineon KIT_PSE84_EVAL with a USB cable (module 1 needs no board).
- ModusToolbox™ 3.6+ per module 2 with its bundled Arm GNU Toolchain; to build the open-source tesaiot-pse84-devkit-sdk use exactly 3.6, as its README requires.
- Visual Studio Code with the ModusToolbox™ extensions.
- Firmware HEX `tesaiot-bitstream-<version>.hex` and TESAIoT Flasher from [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/tree/f5f09a6e89a42a800dd39bae362c1c3f2328cc72) (manifest `latest` = 0.2.1 at commit `f5f09a6`).
- Bitstream Studio (VS Marketplace 0.2.2 as of 2026-09-26) or the VSIX paired with the HEX.
- Host tools: a serial terminal, MQTTX or `mosquitto_sub`, and a GATT explorer (nRF Connect / LightBlue / AIROC™ Bluetooth® Connect).
- Your own Wi-Fi and MQTT broker (the one in Bitstream Studio or a public test broker). Never commit passwords.

All tool versions are recorded in the `toolchain` field of [course.yaml](course.yaml).

## Important: which firmware the code targets

The C code in modules 3–8 is written for the **TESAIoT Bitstream** firmware (the source calls it "TESA Firmware SDK"), distributed as prebuilt HEX files with Bitstream Studio in [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/tree/f5f09a6e89a42a800dd39bae362c1c3f2328cc72). **Its source code and headers are not public yet.** As of 2026-09-26, names such as `cm55_trigger_mqtt_connect`, `cm55_get_mqtt_status` and `cm55_ble_periph_*` appear neither in the public SDK, nor in the TESAIoT_Hackathon repository (HEX, VSIX, installers and web apps only), nor in the TESAIoT Developer Hub search. Read those snippets for the concepts and call order, and do the labs with the HEX.

The open-source SDK available today is [tesaiot-pse84-devkit-sdk](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) (Apache-2.0). It is a **different code base** with different API names; each C1 lesson lists the examples in it that were checked to cover the same topic (commit `ef72c1b`). No public equivalent was found for the PWM brightness wrapper, `cm55_uart_send`, IMU fusion, the Bitstream SENSOR_CFG, the JSON telemetry encoder or the BLE scan path. The `ble-flet` host app used in modules 7–8 is not published either; use a generic GATT explorer.

## Learning outcomes

1. Map Edge AI workloads to PSOC™ Edge E84 hardware domains and to the HAL/BSP, Driver API, Utility and Application layers.
2. Create, build, flash and debug a firmware project with ModusToolbox™ and VS Code on a real board.
3. Drive GPIO, UART, I²C, PWM and ADC through a driver API and split work into FreeRTOS tasks (queue, mutex, event group).
4. Sample sensors at a fixed period, filter, normalise and window the data to prepare it for Edge AI.
5. Connect a device to a broker over MQTT/MQTTs and to a nearby host over BLE, with evidence that it works.
6. Deliver a mini project that combines sensing, RTOS and connectivity, with a README others can reproduce.

## Modules

| # | Module | Lesson | Lab |
|---|---|---|---|
| 1 | [MCU Architecture and Firmware SDK Structure](m01-mcu-architecture/README.md) | [Multi-domain MCU Architecture and Firmware SDK Layers](m01-mcu-architecture/l01-architecture-and-sdk-layers/README.md) | [Lab: Map MCU Domains to SDK Layers](m01-mcu-architecture/l02-lab/README.md) |
| 2 | [ModusToolbox™ and VS Code for Firmware Development](m02-toolchain/README.md) | [ModusToolbox™ and VS Code: Create, Build, Flash, Debug](m02-toolchain/l01-modustoolbox-and-vscode/README.md) | [Lab: Create, Build, Flash, and Debug a Firmware Project](m02-toolchain/l02-lab/README.md) |
| 3 | [GPIO and Basic Peripherals](m03-gpio-peripherals/README.md) | [GPIO and Peripherals through a Driver API](m03-gpio-peripherals/l01-gpio-and-peripherals/README.md) | [Lab: GPIO and Peripherals on Real Hardware](m03-gpio-peripherals/l02-lab/README.md) |
| 4 | [RTOS Firmware Programming](m04-rtos/README.md) | [Multi-task Firmware with FreeRTOS](m04-rtos/l01-freertos-programming/README.md) | [Lab: Multi-Task Firmware with FreeRTOS](m04-rtos/l02-lab/README.md) |
| 5 | [Sensor Data and Edge AI Preparation](m05-sensor-data/README.md) | [AI-ready Sensor Streams](m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) | [Lab: Sensor Streams and AI-Ready Windows](m05-sensor-data/l02-lab/README.md) |
| 6 | [MQTT and MQTTs for Cloud Communication](m06-mqtt/README.md) | [MQTT and MQTTs on an Edge Device](m06-mqtt/l01-mqtt-and-mqtts/README.md) | [Lab: Wi-Fi, MQTT Connect, Publish, and Subscribe](m06-mqtt/l02-lab/README.md) |
| 7 | [Bluetooth Low Energy (BLE) Connectivity](m07-ble/README.md) | [BLE for Edge Products](m07-ble/l01-ble-connectivity/README.md) | [Lab: BLE Connectivity](m07-ble/l02-lab/README.md) |
| 8 | [Capstone Project and Course Resources](m08-capstone/README.md) | [Plan the Capstone and Use the Resource Map](m08-capstone/l01-capstone-and-resources/README.md) | [Lab: Capstone Mini Project](m08-capstone/l02-lab/README.md) |

## How to learn

Read lesson 1 of each module, then do its lab (lesson 2). Keep the sheets in `resources/` open while you work on the board, follow the **Read alongside this chapter** tables for online documents, and answer `quiz.yaml` before each lab.

The source was written for instructor-led training; the wording has been adapted for self-study, but machine-specific values (Wi-Fi, broker, COM port, HEX version) are yours to set. Start from the defaults the lessons give (for example 921600 baud or the broker inside Bitstream Studio) and the tool documentation. The text keeps the source names **Course 1 / 2 / 3** (Course 1 = TESA Firmware SDK for Edge AI, Course 2 = Digital Twin, Course 3 = Product Industrial Design) and **M01–M08** for modules.

## Suggested order across the three courses

The source suggests Course 1 → Course 2 → Course 3: firmware on the board, then firmware ↔ Digital Twin ↔ cloud, then product design → Twin → physical prototype. If you only need Blender design work, modules 1–3 of Course 3 can come first; its Twin labs are much easier after Course 2.

- Course 1: [TESA Firmware SDK for Edge AI](../firmware-sdk-edge-ai/README.en.md)
- Course 2: [Firmware Development with the VS Code-based TESA Digital Twin](../digital-twin/README.en.md)
- Course 3: [Product Industrial Design (Blender & Twin)](../product-design/README.en.md)

## Source and licence

Imported from [drsanti/TESAIoT-Courses](https://github.com/drsanti/TESAIoT-Courses) folder `C1/` at commit [`287c218`](https://github.com/drsanti/TESAIoT-Courses/tree/287c21814ba8c75f693136616dcd270349a15966/C1). TESA funded the original work and holds the rights; it is published here under [CC BY-NC 4.0](../../LICENSES/CC-BY-NC-4.0.txt). TESA Open Knowledge kept the author's teaching text; it added the module/lesson structure, front matter, quizzes, firmware and tool notes, fixed links for the new layout, and reworded classroom-delivery phrases (training round, grading) for open learning. Third-party tools and documents keep their own licences.

## How to cite TESA

If you reuse this course in slides, teaching material, a course specification, handouts or a code repository, credit it with:

> "TESA Firmware SDK for Edge AI" from TESA Open Knowledge by the Thai Embedded Systems Association (TESA), https://github.com/tesaiot/tesa-qualification-program, licensed under CC BY-NC 4.0

If you change the material, add "(adapted)" and keep the original author credit:

> Original content by Asst. Prof. Dr. Santi Nuratch, Department of Control Systems and Instrumentation Engineering, Faculty of Engineering, King Mongkut's University of Technology Thonburi (KMUTT) (https://github.com/drsanti), supported by the Thai Embedded Systems Association (TESA)
>
> The Bitstream Studio (VS Code) and Ternion tools used in this course are by Asst. Prof. Dr. Santi Nuratch (KMUTT).

Citing TESA does not mean that TESA or Infineon endorses your course or work. More formats and examples (slides, course specifications, handouts, code repositories) are in [ATTRIBUTION.md](../../ATTRIBUTION.md).
