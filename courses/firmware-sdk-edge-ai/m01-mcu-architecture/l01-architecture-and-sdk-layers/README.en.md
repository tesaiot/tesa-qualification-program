---
id: fw-sdk.m01.l01
lang: en
title:
  th: สถาปัตยกรรม MCU หลายโดเมนและชั้นของ Firmware SDK
  en: Multi-domain MCU Architecture and Firmware SDK Layers
summary:
  th: อ่านแผนที่ PSOC™ Edge E84 แบบหลายโดเมน และชั้นซอฟต์แวร์ HAL/BSP · Driver API · Utility · Application ก่อนเขียนโค้ดจริง
  en: Read the multi-domain map of PSOC™ Edge E84 and the HAL/BSP, Driver API, Utility and Application layers before writing real code.
level: L3
time_min:
  concept: 50
  practise: 15
  check: 10
hardware:
  emulator: false
  boards:
  - none
prerequisites: []
objectives:
- th: จับคู่งานผลิตภัณฑ์ 4 แบบ (UI, always-on sensing, inference หนัก, publish MQTT) กับโดเมน Cortex-M55 / Cortex-M33 + NNLite / Ethos-U55 ได้ถูกต้อง พร้อมเหตุผลข้อละหนึ่งประโยค
  en: Match four product workloads (UI, always-on sensing, heavy inference, MQTT publish) to the Cortex-M55, Cortex-M33 + NNLite or Ethos-U55 domain, with a one-sentence reason each.
- th: จำแนกทุกขั้นตอนของโจทย์ตัวอย่างว่าอยู่ชั้น HAL/BSP, Driver API, Utility หรือ Application
  en: Classify every step of a worked scenario as HAL/BSP, Driver API, Utility or Application.
- th: อธิบายความต่างระหว่าง SDK กับ IDE (ModusToolbox™ / VS Code) โดยยกตัวอย่างสิ่งที่อยู่ในแต่ละฝั่งได้อย่างน้อยฝั่งละหนึ่งอย่าง
  en: Explain how the SDK differs from the IDE (ModusToolbox™ / VS Code), giving at least one example of what belongs to each.
develops:
- skill: hw.architecture
  to: 2
- skill: build.vendor-sdk
  to: 1
- skill: ai.edge
  to: 1
context:
  platform: psoc-edge-e84
  lang: c
  ide: modustoolbox-vscode
  firmware: tesaiot-bitstream (HEX; source not public yet)
status: alpha
translation: done
source_sha256: 7f14d413f8069a64f39ac80ff6153d5b7cee181b817a50e342b5745bbede9380
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M01/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M01 — MCU Architecture and Firmware SDK Structure

**Course 1 · Module 1**
**Suggested time:** about 2.5–3 hours (careful reading + exercises)
**Format:** a conceptual lesson — no board flashing yet (hands-on work with tools starts in [M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md))

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/sdk-layer-cheatsheet.md) · [← Table of Contents](../../README.md) · [M02 →](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md)

> **Note: which firmware the code in this lesson is written for** (checked on 2026-09-26)
>
> The C code in this lesson calls the API of the **TESAIoT Bitstream** firmware, called "TESA Firmware SDK" in the original, which is published as a ready-made HEX file (`tesaiot-bitstream-<version>.hex`) alongside Bitstream Studio in the [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/tree/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/hex) lab pack. **The source code of this firmware is not yet public.** Functions such as `led_controller_*`, `cm55_button_*`, `sensor_*` and `cm55_adc_*` therefore have no header you can open or build yourself. Read the snippets as concepts and a calling order. The calls to FreeRTOS and the Infineon PDL (such as `xTaskCreate`, `vTaskDelay`, `Cy_GPIO_*`) are ordinary public APIs.
>
> If you want code you can read and build from open source, see [tesaiot-pse84-devkit-sdk](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) (Apache-2.0), which is a **different codebase with different API names**. An example already checked to do the same job as this lesson (commit `ef72c1b`):
>
> - The [SDK's README](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/README.md) and the [`bento-firmware-template-mtb-only/`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/tree/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/) folder — a fully open firmware structure (`bsps/` · `bento_libs/` · `proj_cm33_ns/` · `proj_cm55/`) to compare against the HAL/BSP · Driver · Utility · Application layer map in this lesson

---

## Objectives (Learning Outcomes)

By the end of this lesson you should be able to:

1. Explain why **Edge AI** work needs a multi-domain microcontroller
2. Explain the system structure of **[PSOC™ Edge E84](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84)** at a firmware developer's level: the high-performance domain (Cortex-M55 + Ethos-U55) and the low-power domain (Cortex-M33 + NNLite), plus an overview of memory, HMI and security
3. Explain the main components of the **TESA Firmware SDK** in the way this course frames it: **HAL / BSP**, **Driver API** and **Utility Modules**, and connect them to the **[ModusToolbox™](https://www.infineon.com/modustoolbox)** software stack (PDL, HAL, BSP, middleware)
4. Match "the work to be done" to "the hardware domain / software layer that should be called" before writing code in the next lesson

This module is the **mental map** for the whole of Course 1. Once you understand the chip's architecture and its software layers, installing the tools ([M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md)) and calling the Driver API ([M03](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md)) will have a clear frame.

> **A note on spec numbers**
> The clock, memory and feature numbers below are drawn from Infineon's manuals for the PSOC™ Edge E8x / E84 family, such as the [Product Brief (PDF)](https://www.infineon.com/assets/row/public/documents/30/45/infineon-psoc-edge-e84-productbrief-en.pdf) and the [E84 product page](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84).
> The specific chip (SKU) on your board may differ slightly — treat the documentation for the actual board/chip you have as authoritative, and use the numbers in this lesson as a **framework for understanding**, not a substitute for the full datasheet.

### Read alongside this chapter

| Document | Use when |
|---|---|
| [PSOC™ Edge E84 product page](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84) | An overview of features and processing domains |
| [PSOC™ Edge E84 documentation hub](https://documentation.infineon.com/psocedge/docs/eyv1750399809563) | Reading more of the Edge family's documentation |
| [PSOC™ Edge E84 Product Brief (PDF)](https://www.infineon.com/assets/row/public/documents/30/45/infineon-psoc-edge-e84-productbrief-en.pdf) | A spec summary: M55/M33, NPU, memory, HMI, security |
| [PSOC™ Edge family overview](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm) | Comparing the whole Edge family |
| [KIT_PSE84_EVAL](https://www.infineon.com/evaluation-board/KIT-pse84-eval) | The evaluation kit used for learning/prototyping |
| [AN241775 — Getting started with HAL on PSOC™ Edge (PDF)](https://www.infineon.com/assets/row/public/documents/30/42/infineon-an241775-getting-started-with-hal-psoc-edge-applicationnotes-en.pdf) | The PDL / HAL / BSP / middleware stack |
| [AN235935 — Getting started with PSOC™ Edge on ModusToolbox™ (PDF)](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf) | Leading into the tools in M02 |
| [mtb-dsl-pse8xxgp (Device Support Library)](https://github.com/Infineon/mtb-dsl-pse8xxgp) | The PDL/HAL source of the PSE8xx family |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | The course's code example / flowchart / API reference library (the main reference) |
| **[Bitstream Studio (Marketplace)](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | A host app in VS Code — telemetry, Sensor Studio, digital twin linked to the firmware |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | The lab pack: HEX, VSIX, Flasher, web-app demos for hands-on practice |

---

## 1. From Traditional MCUs to Edge AI

### 1.1 What Traditional MCUs Do Well

Microcontrollers (MCUs) have long been used to control devices, for example

- Reading switches / simple sensors
- Driving LEDs, motors, relays
- Communicating over UART / I²C / SPI
- Running predictable control loops

This work usually sits on a single core, with limited memory, and needs no on-chip Machine Learning model acceleration.

### 1.2 What Changes with Edge AI

Modern smart products usually need more than "read a value and send it to the cloud":

| Requirement | Example in a product |
|---|---|
| Processing near the data source | Knowing there is a voice command / a gesture, without constantly streaming raw audio |
| Fast response (low latency) | A UI or a safety interlock that must respond within milliseconds |
| Disciplined power use | Listening all night on a battery |
| Privacy | Some raw data never needs to leave the device |
| Tolerating a dropped connection | The main function still works even while the cloud is temporarily unavailable |

This idea is called **Edge AI** — running artificial intelligence or machine learning close to the data source.

### 1.3 Why a Single Core Is Often Not Enough

If you force everything onto one CPU, you frequently run into conflicts such as

- Heavy inference is needed → needs a high clock → uses a lot of power
- Always-on sensing is needed → must wake often → clashes with the power budget
- UI/graphics + sensors + networking are all needed at once → they compete for CPU time

So MCUs of the Edge AI era are designed as **multi-domain** — separating high-performance work from low-power work, and separating the Neural Network accelerator from the general-purpose core.

This course does not just teach "write C to make the board do things"; it teaches you to see the **chip architecture + SDK software layers** as one system.

---

## 2. Course Platform: PSOC™ Edge E84

The **TESA Firmware SDK** in this course supports development on the **[Infineon PSOC™ Edge](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm)** family, using **[PSOC™ Edge E84](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84)** as the main case study.

Read the architecture summary from the [Product Brief (PDF)](https://www.infineon.com/assets/row/public/documents/30/45/infineon-psoc-edge-e84-productbrief-en.pdf) and the [family documentation on Infineon documentation](https://documentation.infineon.com/psocedge/docs/eyv1750399809563)

### 2.1 Why This Family Fits Edge AI Learning

Per Infineon's product documentation, the E84 family is positioned as an MCU combining:

- High performance for apps and advanced ML — [Arm® Cortex®-M55](https://developer.arm.com/Processors/Cortex-M55) + [Ethos™-U55](https://developer.arm.com/Processors/Ethos-U55)
- A low-power domain for always-on work — [Arm® Cortex®-M33](https://developer.arm.com/Processors/Cortex-M33) + Infineon NNLite
- HMI interfaces (graphics / audio) at the chip level
- Industry-grade security (such as Edge Protect / a PSA level, depending on the chip's support)
- The **[ModusToolbox™](https://www.infineon.com/modustoolbox)** tool ecosystem and ML solutions such as **[DEEPCRAFT™](https://www.infineon.com/design-resources/embedded-software/deepcraft-edge-ai-solutions)**

This matters for the course: you will practise both classic firmware I/O control and preparing the path to Edge AI / connectivity work in later lessons, without changing platform partway through.

Reference evaluation kit: **[KIT_PSE84_EVAL](https://www.infineon.com/evaluation-board/KIT-pse84-eval)** (use whichever board you have)

### 2.2 What to Focus on in M01 (and What to Skip for Now)

| Focus in M01 | Not yet needed in M01 |
|---|---|
| What domains exist, and what kind of work fits each | Memorising the whole chip's register map |
| Which layer software talks to hardware through | Setting up the Device Configurator on every screen |
| The relationship between the SDK and the IDE | Flashing Hello World (that's in M02) |
| An overview of memory / security / HMI | Writing an ML model entirely by yourself |

> **Remember this sentence**
> In M01 you do not need to memorise the whole datasheet.
> You need to be able to answer "which domain should this work sit in?" and "which software layer should this code sit in?"

---

## 3. PSOC™ Edge Multi-Domain Architecture

Infineon describes PSOC™ Edge as a **multi-domain** architecture, balancing high performance with fine-grained power optimization — see the summary in the [E84 product page](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84) and the [Product Brief (PDF)](https://www.infineon.com/assets/row/public/documents/30/45/infineon-psoc-edge-e84-productbrief-en.pdf)

Overall, there are at least two main domains a firmware learner should know:

### 3.1 High-Performance Domain

| Component | Role in brief | Read more |
|---|---|---|
| **Arm® Cortex®-M55** | The main application core, up to about **400 MHz**, with a Helium™ DSP and an FPU | [Cortex-M55](https://developer.arm.com/Processors/Cortex-M55) · [Helium](https://developer.arm.com/Architectures/Helium) |
| **Arm® Ethos™-U55 NPU** | A Neural Network accelerator for advanced ML work, up to about **400 MHz** (documentation states roughly 128 MAC/cycle) | [Ethos-U55](https://developer.arm.com/Processors/Ethos-U55) |

Suited to work such as:

- Core product logic / control loops
- Signal preprocessing (DSP)
- Inference that needs high performance
- Coordinating graphics / connectivity in active mode

### 3.2 Low-Power Domain

| Component | Role in brief | Read more |
|---|---|---|
| **Arm® Cortex®-M33** | A low-power core, up to about **200 MHz** | [Cortex-M33](https://developer.arm.com/Processors/Cortex-M33) |
| **Infineon NNLite** | A low-power Neural Network accelerator for Always-On AI/ML | [E84 product overview](https://documentation.infineon.com/psocedge/docs/eyv1750399809563) |

Suited to work such as:

- Always-on sensing / wake word / acoustic activity detection
- Work that must run continuously while saving power
- Watching for a condition, then "waking" the high-performance domain when needed

### 3.3 Simple Data-Flow View

```text
Sensor / microphone / button
        │
        ├──────────────► Low-Power Domain
        │                Cortex-M33 + NNLite
        │                (always-on / wake / low-power ML)
        │                      │
        │                      │ wakes / sends an event
        │                      ▼
        └──────────────► High-Performance Domain
                         Cortex-M55 (+ Helium DSP)
                                │
                                ├──────────────► Ethos-U55 NPU (advanced inference)
                                │
                                ├──────────────► HMI (graphics / audio) as needed
                                │
                                └──────────────► Connectivity (e.g. Wi-Fi / MQTT in later lessons)
```

> **Key phrase**
> Don't just memorise the core names — be able to answer *which domain should this work sit in, and why*.

### 3.4 Task-to-Domain Mapping (Design Time)

| Type of work | Domain that usually fits | Short reason |
|---|---|---|
| UI / menu / driving an LED from app state | High-Performance (M55) | It's core product logic |
| Listening quietly all night | Low-Power (M33 ± NNLite) | The power budget matters more than throughput |
| An advanced gesture / vision model on-device | Ethos-U55 (+ an app on M55 coordinating it) | Needs ML acceleration |
| Building JSON and publishing MQTT | An app on the main core (usually M55) | It's a protocol/policy matter, not the NPU's job |
| Light filtering before feeding a model | M55 (DSP/Helium) or a utility in the app | Preprocessing is not the same as inference |

### 3.5 Common Misconceptions

| Misconception | Reality |
|---|---|
| Having an NPU means you don't need to write I/O-controlling firmware | The NPU accelerates inference — reading sensors and driving actuators is still the app's + driver's job |
| Everything should run on the Cortex-M55 | Always-on work should be considered for the low-power domain |
| Edge AI = always sending raw data to the cloud | The opposite — it aims to process at the edge first |
| NNLite and Ethos-U55 are interchangeable for every task | They serve different purposes: always-on power saving vs. high-performance ML |
| You must pick the correct domain from the very first line of Hello World | M01 teaches the map — real task assignment becomes clearer in M04–M05 |

### 3.6 Think Before the Lab

Choose the most suitable domain for each task:

1. Blink an LED per the menu state on screen
2. Listen for a wake word, low-power, all night
3. Run a gesture-recognition model on the device
4. Build JSON and publish it to a broker

Approach: (1) M55 · (2) M33 / NNLite · (3) Ethos-U55 (+ M55 coordinating) · (4) an app on the main core
Details are in the [lab](../l02-lab/README.md)

---

## 4. SoC Memory and On-Chip Connectivity (Developer Overview)

A firmware learner does not need to memorise every address range, but should know that "memory has several layers", and each layer affects latency / power / model size.

### 4.1 Memory Overview from E8x Family Documents

The family's product documentation gives roughly this picture (depending on the sub-variant — check the [Product Brief](https://www.infineon.com/assets/row/public/documents/30/45/infineon-psoc-edge-e84-productbrief-en.pdf)):

| Resource | Role from a developer's view |
|---|---|
| **System SRAM** (up to several MB combined; E84 documentation often mentions about **6 MB** across domains) | Storage for code/data/graphics or ML buffers in active mode |
| **SRAM in the Low-Power domain** (documentation states about 1 MB in some architecture summaries) | Supports always-on work without needing all resources powered on |
| **TCM / cache of the Cortex-M55** | Reduces wait-states for critical code and data |
| **RRAM** (documentation states about 512 KB in several variants) | Low-power non-volatile memory for storing data/part of the firmware, depending on the system design |
| **Boot ROM** | The chip's boot code |
| **External memory via SMIF / Octal / QSPI** (on the evaluation kit) | Expanding code/models/assets when on-chip SRAM isn't enough |

### 4.2 Why Memory Matters for Edge AI

- ML models and sensor buffers compete for SRAM
- HMI graphics consume memory and bus bandwidth
- Choosing to keep model weights in RRAM / external flash affects boot time and power

In this course, you will feel this directly when arranging buffers in M05, and when connecting UI/telemetry in later lessons — M01 is only laying out the map.

### 4.3 Peripherals and Interfaces Common in Edge / IoT Work

The family's documentation lists a wide range of peripherals, which this course will practise one group at a time:

| Group | Example | Emphasised in |
|---|---|---|
| GPIO / Timer / PWM / ADC | Buttons, lights, motors, reading analogue values | [M03](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md) |
| UART / I²C / SPI / I3C | Debug console, sensors, high-speed buses | [M03](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md), M05 |
| USB / SD / Ethernet / CAN (depending on the variant) | System connectivity | Extra, based on interest |
| Audio (PDM/I2S/TDM), graphics (2.5D GPU, MIPI-DSI/DBI) | HMI | Overview in M01; hands-on depends on the kit |
| An external radio on the kit (e.g. Wi-Fi/Bluetooth on the Evaluation Kit) | Cloud / local radio | [M06 MQTT](../../m06-mqtt/l01-mqtt-and-mqtts/README.md) · [M07 BLE](../../m07-ble/l01-ble-connectivity/README.md) |

---

## 5. HMI, Audio, Graphics, and Security (Overview)

### 5.1 Human–Machine Interface (HMI)

PSOC™ Edge E84 is positioned to support more complex HMI than a typical MCU, for example (summarised from the [Product Brief](https://www.infineon.com/assets/row/public/documents/30/45/infineon-psoc-edge-e84-productbrief-en.pdf)):

- High-resolution graphics at the level the documentation states (for example, a display path up to about 1024×768)
- A 2.5D GPU and display interfaces (MIPI-DSI / DBI, depending on the variant)
- Multi-channel microphone interfaces and features such as Acoustic Activity Detection / wake-word in a low-power context

Read deeper when ready (not required in M01): the list of application notes at [PSOC™ Edge application notes](https://documentation.infineon.com/psocedge/docs/umo1761464512847), such as AN239191 (graphics) and AN237939 (high-performance graphics / low power)

For a firmware course: understand that **HMI is not always outside the chip** — some of it is a block inside the SoC that the app must manage resources and power for, in line with the processing domains.

### 5.2 Security at the Architecture Level

Infineon's documentation states high-level security directions, such as

- A Secure Enclave / lockstep in the low-power domain (depending on the variant)
- Secure Boot and key storage
- Infineon Edge Protect guidance / a PSA level, depending on the SKU
- Encryption libraries and services in the ecosystem (including Trusted Firmware-M guidance in some documents)

A starting point for research: [AN237849 — Getting started with PSOC™ Edge security](https://documentation.infineon.com/psocedge/docs/umo1761464512847) (see the application notes list) and the security summary in the Product Brief

In this course:

| Lesson | What to expect |
|---|---|
| **M01** | Know that security is part of the chip's architecture, not an extra add-on |
| **M06** | Goes into the practical detail of MQTT over TLS, certificates and authentication |

---

## 6. Evaluation Kits

Infineon has at least two common approaches to starting with the E84:

| Kit | Purpose in brief | Link |
|---|---|---|
| **KIT_PSE84_EVAL** (PSOC™ Edge E84 Evaluation Kit) | A general evaluation platform with broad interface access, suited to rapid prototyping | [KIT_PSE84_EVAL](https://www.infineon.com/evaluation-board/KIT-pse84-eval) · [Kit guide](https://documentation.infineon.com/psocedge/docs/lne1762692969598) |
| **KIT_PSEA84** (PSOC™ Edge E84 AI Kit) | A lower-cost approach for edge AI work, as offered by Infineon | See the [E84 product page](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84) |

### 6.1 Typical Evaluation Kit Features (Overview)

From the kit's product page (details depend on the hardware revision you hold):

- A PSOC™ Edge E84 chip
- An on-board programmer/debugger (such as KitProg)
- External memory (QSPI / Octal flash / RAM, depending on the kit)
- A microphone / speaker / display / camera (on HMI-focused kits)
- A wireless module, such as AIROC™ Wi-Fi & Bluetooth® on some kits
- An expansion header (Arduino / mikroBUS / others, depending on the kit)

### 6.2 Product Directions That Match This Course

- Smart home — audio / gesture / thermostat
- Wearables — low-power always-on sensing
- Small robots — context awareness within a limited scope
- Locks / security — device-level authentication
- Industrial HMI — a local display and input

---

## 7. Software Ecosystem: From ModusToolbox™ to TESA Firmware SDK

Before entering "HAL / Driver API / Utility" as this course frames it, you should see the actual Infineon stack that the SDK and example projects stand on.
Read alongside [AN241775 (HAL on PSOC™ Edge)](https://www.infineon.com/assets/row/public/documents/30/42/infineon-an241775-getting-started-with-hal-psoc-edge-applicationnotes-en.pdf) and [mtb-dsl-pse8xxgp](https://github.com/Infineon/mtb-dsl-pse8xxgp)

### 7.1 Software Layers in ModusToolbox™ (from Infineon Docs)

Documents such as AN241775 and the [ModusToolbox™](https://www.infineon.com/modustoolbox) manual lay out roughly this picture:

```text
Applications / Code Examples / Reference Designs
        │
        ▼
Middleware libraries
(Graphics, ML, Wi-Fi/Bluetooth, CAPSENSE, Voice, Security, …)
        │
        ▼
Board Support Packages (BSP)
        │
        ▼
Device Support Library
  ├── Peripheral Driver Library (PDL)
  ├── Hardware Abstraction Layer (HAL)
  ├── Device Utilities
  └── Device Information
        │
        ▼
Hardware (PSOC™ Edge)
```

In brief:

| Piece | What it does |
|---|---|
| **BSP** | Board-specific code and configuration — board init, pin mapping, libraries the board needs |
| **PDL** | Low-level peripheral APIs + the chip's headers/startup code — close to the hardware |
| **HAL** | A portable layer wrapping the PDL; on newer PSOC™ Edge parts, Infineon emphasises HAL supporting middleware, with peripheral setup made clearer through the **Device Configurator + PDL** |
| **Middleware** | Ready-made stacks (RTOS abstraction, connectivity, ML, graphics, etc.) |
| **Application** | Your own product code |

> For PSOC™ Edge: the order the documentation often recommends is
> **set up/init peripherals with the PDL (and the configurator) → bind HAL objects when middleware needs them → middleware/the app then uses it**

### 7.2 Where TESA Firmware SDK Fits

The **TESA Firmware SDK** in this course is the body of knowledge and API this course gives learners to develop TESAIoT / Edge AI products systematically on the platform above.

In the lesson's terms, we group it into three axes learners must understand clearly before writing code:

| Course term | What it usually maps to in the real stack | What the learner does |
|---|---|---|
| **HAL / BSP** | The BSP + bring-up / board abstraction (+ the platform's HAL context) | Choose the board, call init per the project guide |
| **Driver API** | The peripheral-control entry point this course standardises on (sitting on the SDK's PDL/HAL/driver, depending on the version used) | Read/write GPIO, UART, I2C, SPI, PWM, ADC |
| **Utility Modules** | Reusable helper modules used across example projects/products | Buffers, light filters, logging helpers |

And a fourth layer you always write yourself:

| Layer | Meaning |
|---|---|
| **Application** | Product policy, tasks, decisions, and calls down into the layers below |

### 7.3 SDK Is Not the IDE

| Term | What it is | Read more |
|---|---|---|
| **ModusToolbox™ / VS Code** | The development tool (creating a project, managing libraries, writing code, building, debugging) | [M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md) · [ModusToolbox™](https://www.infineon.com/modustoolbox) |
| **TESA Firmware SDK** | The software/API set and approach your code calls into in this course | Section 8 of this lesson |
| **Device Support Library** | Infineon's chip-support package (PDL/HAL/utilities) | [mtb-dsl-pse8xxgp](https://github.com/Infineon/mtb-dsl-pse8xxgp) |
| **DEEPCRAFT™** | An ML model workflow for Edge (overview in M01; detail in the Sensor/AI lesson) | [DEEPCRAFT™](https://www.infineon.com/design-resources/embedded-software/deepcraft-edge-ai-solutions) |
| **Digital Twin** | A simulated / 3D view on the host (the full Digital Twin course is a separate course) — the host tool used alongside the firmware is **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | [Marketplace](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) |

Remember it firmly: **installing the IDE ≠ understanding the SDK**.

---

## 8. Core SDK Building Blocks: HAL/BSP, Driver API, Utility

### 8.1 Bottom-Up Software Layers (Course Teaching Model)

```text
+--------------------------------------------------+
| Application / Product Logic                      |
| (product policy, tasks, decisions)                |
+--------------------------------------------------+
| Utility Modules                                  |
| (buffer, helper, logging, reusable helper work)    |
+--------------------------------------------------+
| Driver API                                       |
| (GPIO, UART, I2C, SPI, PWM, ADC, …)              |
+--------------------------------------------------+
| HAL / BSP                                        |
| (board bring-up, clocks, pin mux, board abstraction)|
+--------------------------------------------------+
| Hardware                                         |
| (PSOC™ Edge E84 + devices on the evaluation kit)   |
+--------------------------------------------------+
```

### 8.2 BSP / HAL — Prepare the Stage

The **Board Support Package (BSP)** lets a project know which board it's running on, what each pin is connected to, and which libraries it needs to pull in.

The **Hardware Abstraction Layer (HAL)** in the Infineon ecosystem lets the layers above speak a more portable language than touching registers directly.
On newer PSOC™ Edge parts, the documentation emphasises that setting up and initialising most peripherals is done through the **configurator + PDL**, while HAL is used purposefully alongside middleware.

In this course, you will usually:

1. Create/open a project from the kit's BSP
2. Call init per the project's own example, or examples on the **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**
3. Not start from "writing registers bit by bit" in standard exercises

### 8.3 Driver API — Talk to Hardware

The **Driver API** is the main entry point for controlling peripherals, in this course's approach.

Example work:

- GPIO — LEDs / buttons / control signals
- UART — logging and text protocols
- I²C / SPI — sensors and external memory
- PWM / ADC — driving signals and reading analogue values
- Timer — timing

The course's rule: **call the SDK's Driver API for the version you are using**; don't skip ahead to writing registers directly, unless a lesson explicitly says to.

The real function names depend on the version locked into your project — M01 focuses on the layer's role, while calling detail with real snippets is practised in **[M03](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md)** (such as `led_controller_*`, `cm55_button_*`, `sensor_*`, `cm55_adc_*`) and RTOS in M04 (`xTaskCreate`, `vTaskDelay`, …)

### 8.4 Utility Modules — Helpers

**Utility Modules** do not replace drivers; they help with repeated work, such as

- A light ring buffer / queue at the app level
- Basic filtering / smoothing
- Logging helpers
- Data-formatting functions shared across several modules

A simple rule: **Utility organises things — the Driver talks to hardware — the Application decides**.

### 8.5 Application — Product Policy

The application layer is where you write things such as

- Blink a light when a sensor value crosses a threshold
- Change mode once an inference result comes back
- When to publish to the cloud (detail in M06)
- When to wake the high-performance domain after an event from the low-power domain

### 8.6 Quick Decision Table

| Question you ask yourself | The layer likely involved |
|---|---|
| Is the board ready to run yet? Are the clock and pins set up? | HAL / BSP |
| Which peripheral do I need to talk to? | Driver API |
| Is there reusable helper work needed in several places? | Utility |
| What is the product's policy? Who decides? | Application |
| Do I need a ready-made stack (e.g. RTOS abstraction, Wi-Fi)? | Middleware (through the tools/libraries from M02 onward) |

A one-page summary: [sdk-layer-cheatsheet.md](resources/sdk-layer-cheatsheet.md)

### 8.7 Worked Scenarios

#### Scenario A — Temperature Threshold

The task: read temperature over I²C every 1 second; if it exceeds a threshold, turn on an LED and print a message over UART.

| Step | Layer |
|---|---|
| Initialise the board and the I²C / LED / UART pins | HAL / BSP |
| Read I²C, write GPIO, send over UART | Driver API |
| Keep the last N samples / a moving average | Utility |
| Compare against the threshold, change the product's state | Application |

#### Scenario B — Always-On Then Heavy Inference

The task: wait to catch Acoustic Activity on the low-power domain; once an event occurs, wake the high-performance domain to run a model on the Ethos-U55, then update the UI.

| Step | Domain / layer |
|---|---|
| Listen for / detect audio activity | Low-Power Domain (M33 ± NNLite) |
| Wake up and send an event | Application policy + an inter-domain path, per the system design |
| Preprocessing / windowing the data | Utility + an app on M55 |
| Heavy inference | Ethos-U55 |
| Update the screen / LED / send a summary to the cloud | Application (+ connectivity in M06) |

---

## 9. Development Tools and ML Workflow (Preview)

### 9.1 Tools You Will Use in M02

| Tool | Role | Read more |
|---|---|---|
| **ModusToolbox™** | Creating projects, managing BSPs/libraries, the configurator | [ModusToolbox™](https://www.infineon.com/modustoolbox) · [M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md) |
| **Visual Studio Code** | Writing code, building and debugging (with whichever extensions/workflow you choose) | [VS Code](https://code.visualstudio.com/) · [VS Code for ModusToolbox™](https://documentation.infineon.com/modustoolbox/docs/visual-studio-code-for-modustoolbox-user-guide) |
| **KitProg / SWD debugger** | Flashing and debugging on real hardware | [AN235935 (PDF)](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf) |
| **Library Manager / Project Creator** | Choosing and updating libraries in a project | [Tools package user guide (PDF)](https://www.infineon.com/assets/row/public/documents/30/68/infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf) |

Useful starting documentation from Infineon (optional further reading):

- [AN235935 — Getting started with PSOC™ Edge on ModusToolbox™ (PDF)](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf)
- [AN241775 — Getting started with HAL on PSOC™ Edge (PDF)](https://www.infineon.com/assets/row/public/documents/30/42/infineon-an241775-getting-started-with-hal-psoc-edge-applicationnotes-en.pdf)
- [PSOC™ Edge quick start guide](https://documentation.infineon.com/modustoolbox/docs/psoc-edge-quick-start-guide)

### 9.2 DEEPCRAFT™ (Overview)

**[DEEPCRAFT™](https://www.infineon.com/design-resources/embedded-software/deepcraft-edge-ai-solutions)** is Infineon's solution/studio for the Edge AI model workflow, from data preparation through to deploying the model on a device.

In this course:

- M01: know that there is an ML path on the platform, and it is a different layer from the GPIO driver
- M05: focuses on preparing sensor data / buffers / data windows ready for inference

> Successfully flashing Hello World is the goal of **[M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md)**, not M01

---

## 10. Module Summary

1. **Edge AI** pushes an MCU to support performance, power, HMI and security all at once — not just a faster CPU
2. **[PSOC™ Edge E84](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84)** is a multi-domain example: High-Performance (M55 + Ethos-U55) and Low-Power (M33 + NNLite)
3. SoC memory has several layers, affecting models, graphics, and always-on work
4. Infineon's real stack has BSP / PDL / HAL / middleware — this course explains it through **HAL/BSP + Driver API + Utility + Application**
5. **SDK ≠ IDE** — the tool sits in a different layer from the library your code calls
6. M01 does not flash a board — you are now ready to install the tools in [M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md)

### Next Steps

1. Do the hands-on exercise: [Lab](../l02-lab/README.md)
2. Keep the summary sheet handy: [Cheatsheet](resources/sdk-layer-cheatsheet.md)
3. When ready, continue to **M02 — ModusToolbox and VS Code for Firmware Development** ([M02 lesson](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md))
4. After M02, continue to **M03 — GPIO and Basic Peripherals** ([M03 lesson](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md))

---

## References and Further Reading

Use these as a starting point for research — always check the latest version on the Infineon / Arm website.

### Platform and architecture

1. [PSOC™ Edge E84 — Infineon product page](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84)
2. [PSOC™ Edge E84 documentation hub](https://documentation.infineon.com/psocedge/docs/eyv1750399809563)
3. [PSOC™ Edge E84 Microcontrollers Product Brief (PDF)](https://www.infineon.com/assets/row/public/documents/30/45/infineon-psoc-edge-e84-productbrief-en.pdf)
4. [PSOC™ Edge family overview](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm)
5. [KIT_PSE84_EVAL — Evaluation Kit](https://www.infineon.com/evaluation-board/KIT-pse84-eval)

### CPU / NPU (Arm developer)

6. [Arm Cortex-M55](https://developer.arm.com/Processors/Cortex-M55)
7. [Arm Helium technology](https://developer.arm.com/Architectures/Helium)
8. [Arm Ethos-U55](https://developer.arm.com/Processors/Ethos-U55)
9. [Arm Cortex-M33](https://developer.arm.com/Processors/Cortex-M33)

### Software stack and tools

10. [ModusToolbox™ software](https://www.infineon.com/modustoolbox)
11. [AN235935 — Getting started with PSOC™ Edge on ModusToolbox™ (PDF)](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf)
12. [AN241775 — Getting started with HAL on PSOC™ Edge (PDF)](https://www.infineon.com/assets/row/public/documents/30/42/infineon-an241775-getting-started-with-hal-psoc-edge-applicationnotes-en.pdf)
13. [Infineon mtb-dsl-pse8xxgp (Device Support Library)](https://github.com/Infineon/mtb-dsl-pse8xxgp)
14. [PSOC™ Edge quick start guide](https://documentation.infineon.com/modustoolbox/docs/psoc-edge-quick-start-guide)
15. [DEEPCRAFT™ AI Suite](https://www.infineon.com/design-resources/embedded-software/deepcraft-edge-ai-solutions)
16. [Visual Studio Code](https://code.visualstudio.com/) — used in practice in [M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md)
17. [PSOC™ Edge application notes index](https://documentation.infineon.com/psocedge/docs/umo1761464512847) — a list of application notes on graphics, security, power and connectivity
18. [KIT_PSE84_EVAL kit guide](https://documentation.infineon.com/psocedge/docs/lne1762692969598)
19. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** — a library of code examples, flowcharts, and API references for PSoC Edge E84 (the course's main reference)
20. **[Bitstream Studio — Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** — a VS Code extension (Sensor Telemetry, Sensor Studio, digital twin) for a host that connects to TESAIoT / PSoC Edge firmware
21. **[TESAIoT_Hackathon (GitHub)](https://github.com/drsanti/TESAIoT_Hackathon)** — the hands-on pack: `hex/` (firmware), `vsix/` (Bitstream Studio), `flasher/` (TESAIoT Flasher), `web-app/` (telemetry demos)

---

## Check your understanding

Three short questions in [quiz.yaml](quiz.yaml), one per objective of this lesson. Try answering them yourself first, then compare with the answer key and explanations in the file.

## Lab

Continue hands-on at [Lab: matching MCU domains to SDK layers](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/sdk-layer-cheatsheet.md) · [← Table of Contents](../../README.md) · [M02 →](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md)

## Examples on the TESAIoT Developer Hub

Try the real thing on the TESAIoT Dev Kit: open examples on the Developer Hub to read the code, download it, or flash ready-made firmware.

- Related lesson: [TESAIoT Firmware Stack 1.1 · Tools, boards, and the master template](../../../tesaiot-firmware-stack/m01-getting-started/l01-toolchain-and-master-template/README.md)
