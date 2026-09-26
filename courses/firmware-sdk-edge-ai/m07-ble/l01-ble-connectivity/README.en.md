---
id: fw-sdk.m07.l01
lang: en
title:
  th: BLE สำหรับผลิตภัณฑ์ Edge
  en: BLE for Edge Products
summary:
  th: บทบาทของ BLE เทียบกับ MQTT คำศัพท์ GAP/GATT การแบ่งงาน CM33/CM55 การอ่านสถานะ สั่ง advertising และเส้นทาง scan
  en: The role of BLE versus MQTT, GAP/GATT vocabulary, the CM33/CM55 split, reading status, controlling advertising and the scan path.
level: L3
time_min:
  concept: 40
  practise: 20
  check: 10
hardware:
  emulator: false
  boards:
  - devkit
  - eva-kit
prerequisites:
- fw-sdk.m06.l02
objectives:
- th: เปรียบเทียบบทบาทของ BLE (local) กับ MQTT (cloud / broker) สำหรับผลิตภัณฑ์ Edge ได้อย่างน้อยสามด้าน
  en: Compare BLE (local) with MQTT (cloud / broker) for an Edge product on at least three points.
- th: อธิบายคำ GAP, GATT, Peripheral, Central, Advertising และ Notification ด้วยตัวอย่างจากบอร์ดและโฮสต์
  en: Explain GAP, GATT, Peripheral, Central, Advertising and Notification with examples from the board and host.
- th: 'อธิบายการแบ่งงานระหว่างคอร์: CM33 เป็นเจ้าของ BLE stack ส่วน CM55 สั่งงานผ่าน IPC'
  en: 'Explain the core split: CM33 owns the BLE stack and CM55 drives it over IPC.'
develops:
- skill: proto.bluetooth
  to: 2
- skill: rtos.multicore-ipc
  to: 1
context:
  platform: psoc-edge-e84
  lang: c
  ide: modustoolbox-vscode
  firmware: tesaiot-bitstream (HEX; source not public yet)
status: alpha
translation: done
slides: slides.md
source_sha256: 2fa6ca0e5b52859496628d07321898838de84ac20cfcca1f05a48b1a5a0bd721
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M07/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M07 — Bluetooth Low Energy (BLE) Connectivity

**Course 1 · Module 7**
**Suggested time:** about 3–3.5 hours (concepts + peripheral status/ADV + a host demo)
**Format:** a hands-on lesson — comparing with MQTT (M06), connecting a local host over BLE

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/ble-connectivity.md) · [← Table of Contents](../../README.md) · [← M06](../../m06-mqtt/l01-mqtt-and-mqtts/README.md) · [M08 →](../../m08-capstone/l01-capstone-and-resources/README.md)

> **Note: which firmware the code in this lesson is written for** (checked on 2026-09-26)
>
> The C code in this lesson calls the API of the **TESAIoT Bitstream** firmware, called "TESA Firmware SDK" in the original, which is published as a ready-made HEX file (`tesaiot-bitstream-<version>.hex`) alongside Bitstream Studio in the [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/tree/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/hex) lab pack. **The source code of this firmware is not yet public.** Functions such as `cm55_ble_periph_status_get_sync`, `cm55_ble_periph_adv_ctrl_sync`, `cm55_trigger_ble_periph_*`, `cm55_ble_request_scan_*` and `cm55_ble_ipc_set_event_handler` therefore have no header you can open or build yourself. Read the snippets as concepts and a calling order. The calls to FreeRTOS and the Infineon PDL (such as `xTaskCreate`, `vTaskDelay`, `Cy_GPIO_*`) are ordinary public APIs.
>
> If you want code you can read and build from open source, see [tesaiot-pse84-devkit-sdk](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) (Apache-2.0), which is a **different codebase with different API names**. An example already checked to do the same job as this lesson (commit `ef72c1b`):
>
> - [`proj_cm33_ns/examples/ble/01_nus_bring_up_and_talk.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/ble/01_nus_bring_up_and_talk.c) — a BLE peripheral using the Nordic UART Service: advertise, read the link status, and send data (`ble_nus_init`, `ble_nus_get_state`, `ble_nus_rearm_advertising`, `ble_nus_send`) — this file itself notes that it still runs on a template that cannot be delivered, because `libbento_secure.a` is not yet in `LDLIBS`
>
> No equivalent found yet in the public SDK: the scan / observer path (`cm55_ble_request_scan_*`) — `ble_nus` in the SDK is a peripheral-only role

> **The `ble-flet` host is not yet published** — the [TESAIoT_Hackathon README](https://github.com/drsanti/TESAIoT_Hackathon/blob/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/README.md) (commit `f5f09a6`) states that `python-app/`, `ble-react/` and `ble-flet/` belong to the maintainers and are not in the public repo. Use the backup path the lesson already suggests: a general GATT explorer such as nRF Connect, LightBlue, or AIROC™ Bluetooth® Connect

---

## Objectives (Learning Outcomes)

By the end of this lesson you should be able to:

1. Explain the role of **BLE** in an edge product (local / phone / desktop) compared with **MQTT** (cloud / broker)
2. Explain the key terms: **GAP, GATT, Peripheral, Central, Advertising, Connection, Notification**
3. Point out that in the TESA Firmware SDK, **the CM33 owns the BLE stack** and **the CM55 drives it over IPC**
4. Read the peripheral's status with `cm55_ble_periph_status_get_sync` / `cm55_get_ble_periph_status`
5. Control **advertising** with `cm55_ble_periph_adv_ctrl_sync` (stop / start / restart)
6. Explain the **scan** path (the CM55 requests a scan → the CM33 reports the result) for observer mode
7. Use a lab host: **[TESAIoT_Hackathon `ble-flet/`](https://github.com/drsanti/TESAIoT_Hackathon)**, or a general GATT scanning app
8. Do the exercise on the real board and keep evidence of the link

> **The snippets in this lesson** reference function names from the TESA Firmware SDK — use them together with an example project, or an example on the Developer Hub.
> More hosts: **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** · [Hackathon BLE](https://github.com/drsanti/TESAIoT_Hackathon) · [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)

### Read alongside this chapter

| Document | Use when |
|---|---|
| [Bluetooth LE overview (Bluetooth SIG)](https://www.bluetooth.com/learn-about-bluetooth/tech-overview/) | The GAP / GATT concepts |
| [Infineon Find Me CE (PSoC Edge)](https://github.com/Infineon/mtb-example-psoc-edge-btstack-findme) | A vendor example (peripheral + mobile app) |
| **[TESAIoT_Hackathon — ble-flet](https://github.com/drsanti/TESAIoT_Hackathon)** | A desktop BLE dashboard (scan → connect → stream) |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | The main host, usually using USB/UART; compare against the BLE lab |
| [M06 — MQTT](../../m06-mqtt/l01-mqtt-and-mqtts/README.md) | A comparison point for cloud connectivity |
| [M04 — RTOS](../../m04-rtos/l01-freertos-programming/README.md) | A task that waits on status / calls IPC |

---

## 1. BLE in One Page

**Bluetooth Low Energy (BLE)** is a short-range, low-power radio, suited to a phone, tablet, or desktop near the board — no Wi‑Fi or broker needed.

| Term | Meaning |
|---|---|
| **Peripheral** | The device that *advertises* and waits for a host to connect (the TESA board is usually this role) |
| **Central** | The host that *scans* and connects (phone / PC / `ble-flet`) |
| **GAP** | The discovery-and-connection layer (the ADV name, address, connection) |
| **GATT** | The service/characteristic layer (Service / Characteristic / Notify / Write) |
| **Advertising** | Announcing yourself over the air before any connection exists |
| **Notification** | The peripheral sends data to the Central without waiting to be polled every time |

### BLE vs MQTT (after M06)

| | BLE | MQTT |
|---|---|---|
| Range | Close (a room / a desk) | Over a network / the cloud |
| Middle bridge | No broker required | Requires a **broker** |
| Power / setup | No need to join Wi‑Fi | Needs Wi‑Fi (+ TLS if MQTTs) |
| Lab host | `ble-flet`, nRF Connect, the AIROC app | MQTTX, the Studio broker, the web-app |
| In the Capstone (M08) | The local path | The cloud path |

> **Key phrase**
> MQTT carries data up onto a network — BLE carries data into a nearby phone/PC.

Further reading: [Bluetooth LE tech overview](https://www.bluetooth.com/learn-about-bluetooth/tech-overview/)

---

## 2. Where BLE Lives in TESA Firmware

On the Evaluation Kit, the radio is usually an **AIROC™ Wi‑Fi & Bluetooth® combo** — the BLE stack runs on the **CM33**; the sensor app on the **CM55** drives it through IPC.

| Role | Core | API learners call often |
|---|---|---|
| The BLE stack + a GATT peripheral | **CM33** | `ble_periph_*` (the real owner) |
| Status / commanding ADV from the app | **CM55** | `cm55_trigger_ble_periph_*`, `cm55_ble_periph_*_sync` |
| Scanning (observer) | **CM33** runs the scan · **CM55** requests it and receives events | `cm55_ble_request_scan_*`, `cm55_ble_ipc_set_event_handler` |
| BS2 over BLE (a lab host) | The CM33 bridge + a host GATT client | The host: the Hackathon `ble-flet` |

```text
[Phone / PC central] ──GATT──► [BLE peripheral on CM33]
                                    ▲
                                    │ IPC
                                    │
                              [App on CM55]
                         cm55_trigger_ble_periph_*
                         cm55_ble_request_scan_*
```

> **Honest note**
> Wi‑Fi (M06) and BLE share the same radio on many kits — don't expect maximum throughput on both at once without testing coexistence in a real room.

---

## 3. Peripheral Status (Diagnostic First)

Before "connecting to a phone", confirm the BLE profile on the firmware is working.

The status structure (a summary of its important fields):

```c
typedef struct {
  uint8_t profile_ble_active;
  uint8_t manager_inited;
  uint8_t stack_ready;
  uint8_t tx_notify_enabled;
  uint32_t last_error;
  uint16_t connection_id; /* 0 = no link */
} ipc_ble_periph_status_t;
```

### Reading the status synchronously (recommended in the lab)

```c
#include "cm55_ipc_app.h"
#include "ipc_ble_periph_types.h"

ipc_ble_periph_status_t st;

if (cm55_ble_periph_status_get_sync(&st, 5000U)) {
    /* check stack_ready, connection_id, tx_notify_enabled */
} else {
    /* timeout / IPC did not respond — check the firmware has the BLE profile on */
}
```

Or fire the request without waiting, and read the snapshot later:

```c
(void)cm55_trigger_ble_periph_status_get();
/* … wait for the event / a short delay … */
(void)cm55_get_ble_periph_status(&st);
```

| Field | Approximate meaning |
|---|---|
| `profile_ble_active` | This build's BLE profile is turned on |
| `manager_inited` / `stack_ready` | The stack is ready |
| `tx_notify_enabled` | The Central has turned on notify (the link is genuinely in use) |
| `connection_id` | A GATT connection exists when this is not 0 |
| `last_error` | The most recent error code (0 = normal) |

---

## 4. Advertising Control

Advertising makes the device visible to a Central — the name in TESA labs usually starts with **`TESAIoT-`**

```c
uint8_t result = 0xFF;

/* action: 0 = stop, 1 = start, 2 = restart */
if (cm55_ble_periph_adv_ctrl_sync(1U, &result, 5000U)) {
    /* result 0 = ok, per the bridge */
}
```

| `action` | Meaning |
|---|---|
| `0` | Stop advertising |
| `1` | Start advertising |
| `2` | Restart advertising (worker-safe) |

> **Key phrase from the firmware**
> While a connection exists, stopping ADV does not cut the link — and starting ADV may not be necessary since it's already connected.

If the host doesn't see the device after being on for a long time: check the **ADV timeout** / reboot the board (the Hackathon `ble-flet` README describes this symptom).

---

## 5. Scan Path (Optional Observer Lab)

When the role is **scanning for other devices** (not just being a peripheral):

```c
#include "cm55_ipc_app.h"

static void on_ble_ipc(const ipc_msg_t *msg, void *user)
{
    (void)user;
    /* classify the event by IPC_EVT_BLE_*'s cmd */
}

void ble_scan_lab_start(void)
{
    cm55_ble_ipc_set_event_handler(on_ble_ipc, NULL);
    cm55_ble_request_scan_all();          /* or scan_name / scan_addr */
    /* stop with a scan-stop command per the SDK example once time's up */
}
```

Common helpers:

| API | Use when |
|---|---|
| `cm55_ble_request_scan_all` | A full scan, no filtering |
| `cm55_ble_request_scan_name` | Filtering by a partial name |
| `cm55_ble_request_scan_addr` | Filtering by a 6-byte address |
| `cm55_ble_ipc_set_event_handler` | Receiving scan results/status in a task |

Examples in this firmware are usually named around **`example_ble`** (toggling scan on/off periodically) — see them on the Developer Hub / the firmware's example project.

---

## 6. Host Tools for the Lab

### 6.1 Recommended: Hackathon `ble-flet`

The [`TESAIoT_Hackathon`](https://github.com/drsanti/TESAIoT_Hackathon) pack has a desktop app built with **Python + Flet + bleak**:

1. Flash a HEX with the **BLE module profile** turned on
2. Run `ble-flet` per the repo's README
3. The app will hunt for a name starting with **`TESAIoT-*`** → connect → stream

Suited to a lab that needs **live evidence**, without relying on Web Bluetooth in a browser.

### 6.2 Generic GATT explorers

- nRF Connect / LightBlue / AIROC™ Bluetooth® Connect (per the Infineon Find Me example)
- Use these to confirm the device advertises and connects, even before decoding BS2

### 6.3 Bitstream Studio

[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) is the course's main host for USB/UART and MQTT — in M07 it is used as a *comparison point* for when to choose local BLE instead of a cable or a broker.

### GATT identity (a BS2 BLE lab)

The lab host references the BS2 family's service/characteristic (a UUID fixed in `ble-flet`), and an ADV name starting with `TESAIoT-` — **don't hardcode the UUID in your deliverable documents unless you need to**; instead, state which version of the Hackathon pack you used.

---

## 7. Security and Lab Hygiene

| Topic | Practice |
|---|---|
| Pairing / bonding | The lab usually uses a short link — don't assume it's production-grade secure pairing |
| Data over the air | BLE doesn't go through a broker, but is still within the radio range of the lab room |
| Secrets | There is no Wi‑Fi password in this path — but other credentials still must not be embedded in public files |
| A single Central | Don't open nRF Connect and `ble-flet` at the same time on one machine, both pointed at the same board |

---

## 8. Design Patterns for Capstone (Preview M08)

Choose at least one connectivity path in the Capstone:

```text
Sensor task ──► window/filter ──► LED/UART
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
   MQTT publish (M06)      BLE notify / host (M07)
   MQTT subscribe cmd      BLE write / command
```

M08's minimum bar: **MQTT or BLE** — using both is a bonus.

---

## 9. Common Pitfalls

| Symptom | Common cause |
|---|---|
| The scan finds nothing | The BLE profile is off · not advertising yet · the ADV timed out · too far away / interference |
| Status sync times out | The CM33 isn't ready yet · IPC hasn't come up · the build has no BLE |
| It connects, then drops | Another Central grabbed it · the board rebooted · a firmware policy timeout |
| Wi‑Fi + BLE together behave oddly | Combo radio coexistence — test them separately before combining |
| Confused with MQTT | A different transport layer entirely — don't go looking for a broker in a BLE lab |

---

## Next Steps

1. Do the lab: [Lab](../l02-lab/README.md)
2. Keep the summary sheet: [ble-connectivity.md](resources/ble-connectivity.md)
3. When ready, continue to **M08 — Capstone** ([M08 lesson](../../m08-capstone/l01-capstone-and-resources/README.md))

---

## References and Further Reading

1. [Bluetooth LE overview](https://www.bluetooth.com/learn-about-bluetooth/tech-overview/)
2. [Infineon mtb-example-psoc-edge-btstack-findme](https://github.com/Infineon/mtb-example-psoc-edge-btstack-findme)
3. [Infineon BLE + Wi‑Fi IoT gateway CE](https://github.com/Infineon/mtb-example-psoc-edge-btstack-wifi-iot-gateway)
4. **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** (`ble-flet/`)
5. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**
6. **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)**
7. [M06 MQTT](../../m06-mqtt/l01-mqtt-and-mqtts/README.md) · [M08 Capstone](../../m08-capstone/l01-capstone-and-resources/README.md)
8. [PSOC™ Edge E84](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84)

---

## Check your understanding

Three short questions in [quiz.yaml](quiz.yaml), one per objective of this lesson. Try answering them yourself first, then compare with the answer key and explanations in the file.

## Lab

Continue hands-on at [Lab: BLE connectivity](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/ble-connectivity.md) · [← Table of Contents](../../README.md) · [← M06](../../m06-mqtt/l01-mqtt-and-mqtts/README.md) · [M08 →](../../m08-capstone/l01-capstone-and-resources/README.md)
