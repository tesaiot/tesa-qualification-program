---
id: fw-sdk.m08.l01
lang: en
title:
  th: วางแผน Capstone และใช้แผนที่เอกสาร
  en: Plan the Capstone and Use the Resource Map
summary:
  th: เกณฑ์ผ่านของ Capstone แผนที่ชีตและ API ของหลักสูตร สถาปัตยกรรมอ้างอิง และสถานการณ์สาธิตสามแบบ
  en: Capstone pass criteria, the course's sheet and API map, a reference architecture and three demo scenarios.
level: L3
time_min:
  concept: 35
  practise: 25
  check: 10
hardware:
  emulator: false
  boards:
  - devkit
  - eva-kit
prerequisites:
- fw-sdk.m07.l02
objectives:
- th: 'วางแผน Capstone ให้ครอบคลุมเกณฑ์ผ่านขั้นต่ำ: build/flash, ≥ 2 FreeRTOS tasks, sensor path + LED/UART และ connectivity อย่างน้อยหนึ่งเส้น'
  en: 'Plan a capstone that meets the minimum criteria: build/flash, at least two FreeRTOS tasks, a sensor path with LED/UART, and at least one connectivity path.'
- th: ใช้แผนที่เอกสารของหลักสูตรหาชีตหรือบทเรียนที่ตอบความต้องการแต่ละข้อ
  en: Use the course resource map to find the sheet or lesson for each need.
- th: ออกแบบสถานการณ์สาธิตสามแบบ (Normal, Stimulus, Command) ที่พิสูจน์ระบบได้
  en: Design three demo scenarios (Normal, Stimulus, Command) that prove the system works.
develops:
- skill: iot.fundamentals
  to: 2
- skill: soft.communication
  to: 2
- skill: soft.organization
  to: 1
context:
  platform: psoc-edge-e84
  lang: c
  ide: modustoolbox-vscode
  firmware: tesaiot-bitstream (HEX; source not public yet)
status: alpha
translation: done
source_sha256: 0925bd9637585a21b408ade9882551d7abd4acf744e87338a750e6fe61cf51e3
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M08/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M08 — Capstone Project and Course Resources

**Course 1 · Module 8**
**Suggested time:** flexible — 2–4 hours recommended + continuing the Capstone on your own
**Format:** combining the skills of M01–M07 into a mini-project + using the resource map / online portals

[Lab](../l02-lab/README.md) · [Capstone brief](resources/capstone-brief.md) · [Course package map](resources/course-package.md) · [← Table of Contents](../../README.md) · [← M07](../../m07-ble/l01-ble-connectivity/README.md)

> **Note: which firmware the code in this lesson is written for** (checked on 2026-09-26)
>
> The C code in this lesson calls the API of the **TESAIoT Bitstream** firmware, called "TESA Firmware SDK" in the original, which is published as a ready-made HEX file (`tesaiot-bitstream-<version>.hex`) alongside Bitstream Studio in the [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/tree/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/hex) lab pack. **The source code of this firmware is not yet public.** Functions such as `cm55_*`, `sensor_*`, `led_controller_*`, `cm33_mqtt_*` and `cm55_ble_*` therefore have no header you can open or build yourself. Read the snippets as concepts and a calling order. The calls to FreeRTOS and the Infineon PDL (such as `xTaskCreate`, `vTaskDelay`, `Cy_GPIO_*`) are ordinary public APIs.
>
> The Capstone uses APIs from all of Modules 3–7. See the checked equivalents in the open SDK in each lesson's note, and in the summary table on the [course page](../../README.md)

> **The `ble-flet` host is not yet published** — the [TESAIoT_Hackathon README](https://github.com/drsanti/TESAIoT_Hackathon/blob/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/README.md) (commit `f5f09a6`) states that `python-app/`, `ble-react/` and `ble-flet/` belong to the maintainers and are not in the public repo. Use the backup path the lesson already suggests: a general GATT explorer such as nRF Connect, LightBlue, or AIROC™ Bluetooth® Connect

---

## Objectives (Learning Outcomes)

By the end of this lesson you should be able to:

1. Use the **M01–M07 exercise set** as the foundation, then combine it into a demonstrable system
2. Deliver work against the Capstone's **pass criteria** (build/flash, RTOS, sensor, MQTT or BLE)
3. Use the course's **resource / API map** to find functions and examples on your own
4. Deliver the **Capstone project** with a README others can reproduce
5. Use **online** learning resources (the Developer Hub, the Marketplace, Hackathon) to support the demonstration

> Each module's exercise is part of the whole course's practice set — M08 is the layer that **combines and delivers**.

### Read alongside this chapter

| Document | Use when |
|---|---|
| [Table of Contents](../../README.md) | The whole course's index |
| [Course package map](resources/course-package.md) | A module map + online portals + an API index |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | Code examples + API Reference |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | Host / Digital Twin / broker tools |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | HEX, Flasher, VSIX, `web-app/`, `ble-flet/` |
| [M05](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) · [M06](../../m06-mqtt/l01-mqtt-and-mqtts/README.md) · [M07](../../m07-ble/l01-ble-connectivity/README.md) | Sensor + MQTT + BLE for the Capstone |

---

## 1. Full Hands-on Lab Index (Course 1)

| Module | Lab | What you get once passed |
|---|---|---|
| [M01](../../m01-mcu-architecture/l02-lab/README.md) | The domain ↔ SDK layer map | Can choose a domain/layer before writing code |
| [M02](../../m02-toolchain/l02-lab/README.md) | Create / Build / Flash / Debug | A project running on the board |
| [M03](../../m03-gpio-peripherals/l02-lab/README.md) | GPIO + UART + peripherals | The real Driver API on hardware |
| [M04](../../m04-rtos/l02-lab/README.md) | Multi-task + queue / mutex | Basic FreeRTOS |
| [M05](../../m05-sensor-data/l02-lab/README.md) | Sensor + filter + window | Data ready for AI / a twin |
| [M06](../../m06-mqtt/l02-lab/README.md) | Wi‑Fi + MQTT pub/sub | Connected to the cloud / a broker |
| [M07](../../m07-ble/l02-lab/README.md) | A BLE peripheral / scan + host | Connected locally / to a phone / desktop |
| **[M08](../l02-lab/README.md)** | **The Capstone mini-project** | A combined system, demonstrable and reproducible |

> **Key phrase**
> The Capstone is about *choosing and connecting* pieces you already have — not writing everything from scratch.

---

## 2. Capstone Plan and Pass Criteria

Use this section to plan your work and check before submitting.

### 2.1 Suggested pacing (for you)

| Block | Focus |
|---|---|
| Before starting the Capstone | Check the main labs M02–M07 already meet their minimum bar |
| Hour 1 | Write the task architecture + choose sensors / connectivity |
| Hours 2–3 | Combine the code on the board + test MQTT and/or BLE |
| Hour 4 / continuing on your own | The README, demo evidence, wrapping up |

### 2.2 Your setup checklist

- [ ] A board + a USB cable + working Wi‑Fi
- [ ] A designated broker (LAN / Studio / public per your policy) — if using MQTT
- [ ] A phone or PC that can scan BLE — if using BLE
- [ ] [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio), or the VSIX from [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)
- [ ] HEX / Flasher from Hackathon, if using the ready-made pack
- [ ] **Do not** commit a Wi‑Fi / broker password in files submitted publicly

### 2.3 Minimum pass criteria

| Criterion | Required |
|---|---|
| Builds + flashes, following your own README | Yes |
| ≥ 2 FreeRTOS tasks | Yes |
| A sensor path + LED/UART indication | Yes |
| **Connectivity** — MQTT **or** BLE (at least one path), with a command received or a link confirmed | Yes |
| No secrets embedded in submitted public files | Yes |

Extension work (optional): using both MQTT and BLE, a threshold alert, a mutex on a shared bus, a queue/topic ready for a Digital Twin, demo quality.

Full detail in the [lab](../l02-lab/README.md) and [capstone-brief.md](resources/capstone-brief.md)

---

## 3. Developer Guide and API Reference Map

### 3.1 Where to look first

| Need | Go to |
|---|---|
| Browse online examples | [TESAIoT Developer Hub](https://dev.tesaiot.dev/) — Example Explorer + API Reference |
| Peripheral function names | [M03 cheatsheet](../../m03-gpio-peripherals/l01-gpio-and-peripherals/resources/peripheral-api-map.md) |
| FreeRTOS patterns | [M04 cheatsheet](../../m04-rtos/l01-freertos-programming/resources/rtos-patterns.md) |
| Sensors / windows / fusion | [M05 cheatsheet](../../m05-sensor-data/l01-sensor-data-for-edge-ai/resources/sensor-ai-prep.md) |
| MQTT / Wi‑Fi triggers | [M06 cheatsheet](../../m06-mqtt/l01-mqtt-and-mqtts/resources/mqtt-cloud.md) |
| A BLE peripheral / scan | [M07 cheatsheet](../../m07-ble/l01-ble-connectivity/resources/ble-connectivity.md) |
| The chip architecture / SDK layers | [M01](../../m01-mcu-architecture/l01-architecture-and-sdk-layers/README.md) |
| The toolchain | [M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md) |

### 3.2 Naming map (recap for Capstone)

```text
led_controller_* / cm55_button_* / sensor_*_*
xTaskCreate / vTaskDelay / xQueue* / xSemaphore*
cm55_trigger_connect / cm55_trigger_mqtt_* / bs_mqtt_telem_encode_json_*
cm55_trigger_ble_periph_* / cm55_ble_request_scan_* / cm55_ble_ipc_set_event_handler
```

### 3.3 Capstone data-flow (reference architecture)

```text
[sensor_*_read task] --samples--> [filter / window]
        │                              │
        │                              ▼
        │                        [decision / event]
        │                         │         │
        ▼                         ▼         ▼
   [UART / LED]         [MQTT publish]  [BLE notify / host]
        ▲                    ▲
        └── [MQTT and/or BLE command path]
```

An example delay inside a task (from M04/M05):

```c
TickType_t last = xTaskGetTickCount();
for (;;) {
    /* read → filter → maybe publish */
    vTaskDelayUntil(&last, pdMS_TO_TICKS(200));
}
```

An example MQTT command once Wi‑Fi is ready (from M06):

```c
(void)cm55_trigger_mqtt_connect();
/* wait until cm55_get_mqtt_status reports CONNECTED */
```

An example reading BLE peripheral status (from M07):

```c
ipc_ble_periph_status_t ble;
if (cm55_ble_periph_status_get_sync(&ble, 5000U)) {
    /* stack_ready / connection_id / tx_notify_enabled */
}
```

The combined sheet: [course-package.md](resources/course-package.md)

---

## 4. Project Examples and Source Patterns

| Example source | Role in M08 |
|---|---|
| The projects you built in M02–M07 | The Capstone's codebase |
| [Developer Hub](https://dev.tesaiot.dev/) | Pull examples for GPIO / Sensors / System / Integrations |
| [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) | Ready-made HEX, `web-app/`, `ble-flet/` for live evidence |
| Infineon CE (extra) | Compare against the vendor's approach — does not replace the TESA Driver API |

### 4.1 Recommended Capstone theme

**A small Environmental / Activity monitor**

Must have at least:

1. **A sensor path** — periodic reads + a filter or window (M05)
2. **Local indication** — an LED and/or UART (M03)
3. **RTOS** — ≥ 2 tasks + a queue or mutex when needed (M04)
4. **Connectivity** — at least one path:
   - **MQTT** publish + subscribe to a command (M06), **or**
   - A **BLE** peripheral a host can connect to + a confirmed link/command (M07)

Extra options:

- Use both MQTT and BLE
- An event/alert when a threshold is exceeded
- A `to_twin` structure (a separate queue or topic) for connecting a Digital Twin
- Demonstrate on Bitstream Studio, the Hackathon dashboard, or `ble-flet/`

---

## 5. Course Resources Map

| Piece | Location |
|---|---|
| Table of Contents | [The course page](../../README.md) |
| Lessons M01–M08 | `mNN-<slug>/l01-<slug>/README.md` |
| Labs | `mNN-<slug>/l02-lab/README.md` |
| Cheatsheets / worksheets | `mNN-<slug>/l01-<slug>/resources/*` |
| The combined map | [course-package.md](resources/course-package.md) |

### External portals

| Portal | URL |
|---|---|
| Code examples / API | https://dev.tesaiot.dev/ |
| VS Code host / twin | https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio |
| Lab pack HEX/VSIX/web/BLE | https://github.com/drsanti/TESAIoT_Hackathon |

---

## 6. Course 1 Wrap-Up and Next Path

After finishing Course 1, you should be able to explain:

1. How the TESA Firmware SDK lays out the HAL/Driver/Utility/Application layers
2. How ModusToolbox™ + VS Code are used to build, debug, and flash
3. How GPIO / peripherals, FreeRTOS, sensor prep, MQTT and BLE connect together into an edge product
4. How the host (Bitstream Studio / Hackathon BLE) and the lab pack help you test

**Next path (outside Course 1):** the Digital Twin / Product Design course — using the stream and structure prepared in the Capstone as input.

### Next Steps

1. Do the Capstone: [Lab](../l02-lab/README.md)
2. Fill in [capstone-brief.md](resources/capstone-brief.md)
3. Keep the resource map: [course-package.md](resources/course-package.md)
4. Go back and review any module that isn't solid yet, through the [TOC](../../README.md)

---

## References and Further Reading

1. [Course 1 TOC](../../README.md)
2. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**
3. **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)**
4. **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)**
5. [M01](../../m01-mcu-architecture/l01-architecture-and-sdk-layers/README.md) · [M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md) · [M03](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md) · [M04](../../m04-rtos/l01-freertos-programming/README.md) · [M05](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) · [M06](../../m06-mqtt/l01-mqtt-and-mqtts/README.md) · [M07](../../m07-ble/l01-ble-connectivity/README.md)
6. [MQTT Essentials](https://www.hivemq.com/mqtt-essentials/) · [Bluetooth LE overview (Bluetooth SIG)](https://www.bluetooth.com/learn-about-bluetooth/tech-overview/)
7. [PSOC™ Edge E84](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84)

---

## Check your understanding

Three short questions in [quiz.yaml](quiz.yaml), one per objective of this lesson. Try answering them yourself first, then compare with the answer key and explanations in the file.

## Lab

Continue hands-on at [Capstone lab: a mini-project](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Capstone brief](resources/capstone-brief.md) · [Course package map](resources/course-package.md) · [← Table of Contents](../../README.md)

## Examples on the TESAIoT Developer Hub

Try the real thing on the TESAIoT Dev Kit: open examples on the Developer Hub to read the code, download it, or flash ready-made firmware.

- [EP07 — SensorHub Final](https://dev.tesaiot.dev/?example=developer-hub--int_ep07_sensorhub_final&q=int_ep07_sensorhub_final) — a course-closing project: a dashboard combining all 4 sensors (DPS368, SHT4x, BMI270, BMM350) + a stereo PDM microphone on a single screen
- [EP07 — Final WiFi Manager](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep07_final_wifi_manager&q=hmi_ep07_final_wifi_manager) — combines scan + profile + connect + auto-retry + a ping watchdog into a complete WiFi manager, with a state machine on screen and auto-connect from a saved profile
