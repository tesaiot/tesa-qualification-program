# Firmware Development with the VS Code-based TESA Digital Twin

A hands-on course on developing, checking and testing Edge AI firmware with a VS Code-based Digital Twin (Bitstream Studio): simulate the device, sensors, behaviour, data pipeline and cloud link so development depends less on real hardware.

> Original content by drsanti (https://github.com/drsanti), supported by the Thai Embedded Systems Association (TESA). Imported from [drsanti/TESAIoT-Courses — C2](https://github.com/drsanti/TESAIoT-Courses/tree/287c21814ba8c75f693136616dcd270349a15966/C2) (commit `287c218`) under CC BY 4.0.

| | |
|---|---|
| Level | L3 · Independent |
| Status | alpha (imported, under review) |
| Estimated time | ~18 hours (sum of the source's module estimates) |
| Audience | developer, student, educator |
| Language | Lessons are in Thai with English technical terms and English section headings; English lesson translations are pending. |

## Before you start

Course 1, or equivalent C / MCU / MQTT basics (recommended by the source, not required).

## What you need

- Visual Studio Code 1.75+ (Bitstream Studio declares engine `^1.75.0`; the lab-pack README suggests 1.85+) or Cursor.
- Bitstream Studio (VS Marketplace 0.2.2 as of 2026-09-26) or a VSIX from TESAIoT_Hackathon `vsix/` that matches the HEX.
- Bitstream Simulator for board-free mode: the source calls it a separate extension, but as of 2026-09-26 it is on neither the VS Marketplace nor TESAIoT_Hackathon `vsix/`. If you cannot get it, use the Bitstream (real board) path where a lab offers the choice.
- Board: TESAIoT PSoC Edge DevKit with a `tesaiot-bitstream-<version>.hex` from TESAIoT_Hackathon for the Bitstream path (UART at 921600 baud).
- Example web apps `ex01`–`ex17` in TESAIoT_Hackathon `web-app/`.
- Blender 4.5 for the Twin 3D part of module 3.
- The `.vsix` files and installers in TESAIoT_Hackathon are stored with Git LFS: install `git-lfs` before cloning, or download single files from the GitHub web page.

All tool versions are recorded in the `toolchain` field of [course.yaml](course.yaml).

## Learning outcomes

1. Explain a Digital Twin architecture and decide when a Twin/Simulator is enough and when the real board must confirm.
2. Install and use Bitstream Studio in VS Code and open a Simulator or Bitstream (UART) session reproducibly.
3. Build a Virtual Device with sensors, behaviours and a repeatable event script.
4. Prove firmware-to-Twin I/O, measure latency and isolate faults layer by layer.
5. Design a telemetry pipeline and MQTT pub/sub, then run controlled fault-injection experiments.
6. Test the system end to end with at least three test cases and hand over a reproducible README.

## Modules

| # | Module | Lesson | Lab |
|---|---|---|---|
| 1 | [Digital Twin Architecture](m01-twin-architecture/README.md) | [Virtual Devices, Digital Twins and Real Firmware](m01-twin-architecture/l01-twin-architecture/README.md) | [Lab: Twin Architecture Map](m01-twin-architecture/l02-lab/README.md) |
| 2 | [VS Code for Twin Development](m02-vscode-twin/README.md) | [Setting up the Twin Host in VS Code with Bitstream Studio](m02-vscode-twin/l01-vscode-for-twin/README.md) | [Lab: Install VS Code Twin and First Session](m02-vscode-twin/l02-lab/README.md) |
| 3 | [Virtual Device Modeling (+ Blender for Twin 3D)](m03-virtual-device/README.md) | [Virtual Devices, Behaviours, Event Scripts and 3D Models for the Twin](m03-virtual-device/l01-virtual-device-modeling/README.md) | [Lab: Build a Virtual Device and Event Script](m03-virtual-device/l02-lab/README.md) |
| 4 | [Firmware–Twin Co-simulation](m04-cosimulation/README.md) | [Co-simulation: Prove I/O, Measure Latency, Isolate Faults](m04-cosimulation/l01-firmware-twin-cosim/README.md) | [Lab: Co-simulation End-to-End I/O](m04-cosimulation/l02-lab/README.md) |
| 5 | [Telemetry and Cloud Simulation](m05-telemetry-cloud/README.md) | [Telemetry Pipelines, MQTT on the Twin and Fault Injection](m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md) | [Lab: Telemetry Pipeline and MQTT on Twin](m05-telemetry-cloud/l02-lab/README.md) |
| 6 | [System Integration and Testing](m06-integration/README.md) | [End-to-end Testing on the Digital Twin](m06-integration/l01-system-integration-testing/README.md) | [Lab: E2E Mini-Project on Digital Twin](m06-integration/l02-lab/README.md) |

## How to learn

Take the modules in order 1 → 6, lesson then lab. Use the worksheets and checklists in `resources/` while setting up the Twin and collecting evidence. The host is Bitstream Studio. The course focuses on Firmware ↔ Twin ↔ Cloud and links back to Course 1 instead of re-teaching GPIO or RTOS.

The source was written for instructor-led training; the wording has been adapted for self-study, but machine-specific values (Wi-Fi, broker, COM port, HEX version) are yours to set. Start from the defaults the lessons give (for example 921600 baud or the broker inside Bitstream Studio) and the tool documentation. The text keeps the source names **Course 1 / 2 / 3** (Course 1 = TESA Firmware SDK for Edge AI, Course 2 = Digital Twin, Course 3 = Product Industrial Design) and **M01–M08** for modules.

## Suggested order across the three courses

The source suggests Course 1 → Course 2 → Course 3: firmware on the board, then firmware ↔ Digital Twin ↔ cloud, then product design → Twin → physical prototype. If you only need Blender design work, modules 1–3 of Course 3 can come first; its Twin labs are much easier after Course 2.

- Course 1: [TESA Firmware SDK for Edge AI](../firmware-sdk-edge-ai/README.en.md)
- Course 2: [Firmware Development with the VS Code-based TESA Digital Twin](../digital-twin/README.en.md)
- Course 3: [Product Industrial Design (Blender & Twin)](../product-design/README.en.md)

## Source and licence

Imported from [drsanti/TESAIoT-Courses](https://github.com/drsanti/TESAIoT-Courses) folder `C2/` at commit [`287c218`](https://github.com/drsanti/TESAIoT-Courses/tree/287c21814ba8c75f693136616dcd270349a15966/C2). TESA funded the original work and holds the rights; it is published here under [CC BY 4.0](../../LICENSES/CC-BY-4.0.txt). TESA Open Knowledge kept the author's teaching text; it added the module/lesson structure, front matter, quizzes, firmware and tool notes, fixed links for the new layout, and reworded classroom-delivery phrases (training round, grading) for open learning. Third-party tools and documents keep their own licences.

## How to cite TESA

If you reuse this course in slides, teaching material, a course specification, handouts or a code repository, credit it with:

> "Firmware Development with the VS Code-based TESA Digital Twin" from TESA Open Knowledge by the Thai Embedded Systems Association (TESA), https://github.com/tesaiot/tesa-qualification-program, licensed under CC BY 4.0

If you change the material, add "(adapted)" and keep the original author credit:

> Original content by drsanti (https://github.com/drsanti), supported by the Thai Embedded Systems Association (TESA)

Citing TESA does not mean that TESA or Infineon endorses your course or work. More formats and examples (slides, course specifications, handouts, code repositories) are in [ATTRIBUTION.md](../../ATTRIBUTION.md).
