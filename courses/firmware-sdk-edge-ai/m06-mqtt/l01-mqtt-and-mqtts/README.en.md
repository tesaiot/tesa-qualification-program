---
id: fw-sdk.m06.l01
lang: en
title:
  th: MQTT และ MQTTs บนอุปกรณ์ Edge
  en: MQTT and MQTTs on an Edge Device
summary:
  th: หลักการ publish/subscribe เส้นทางเชื่อมต่อของเฟิร์มแวร์ (Wi-Fi → MQTT) การตั้งค่า broker topic payload JSON และความปลอดภัยด้วย TLS
  en: Publish/subscribe basics, the firmware connection path (Wi-Fi then MQTT), broker settings, topics, JSON payloads and TLS security.
level: L3
time_min:
  concept: 45
  practise: 20
  check: 10
hardware:
  emulator: false
  boards:
  - devkit
  - eva-kit
prerequisites:
- fw-sdk.m05.l02
objectives:
- th: อธิบาย broker, client, topic, QoS และ retain และบอกความต่างของ MQTT กับ MQTTs (TLS, พอร์ต 1883 / 8883)
  en: Explain broker, client, topic, QoS and retain, and how MQTT differs from MQTTs (TLS, ports 1883 / 8883).
- th: 'เรียงเส้นทางเชื่อมต่อของเฟิร์มแวร์ได้ถูกต้อง: join Wi-Fi ให้ CONNECTED ก่อน แล้วจึงสั่งเชื่อม MQTT และอ่านสถานะ'
  en: 'Order the firmware connection path correctly: join Wi-Fi until CONNECTED, then connect MQTT and read its status.'
- th: ออกแบบ topic และ payload JSON สำหรับ telemetry และคำสั่ง โดยไม่ฝังความลับในโค้ดหรือ repo
  en: Design topics and a JSON payload for telemetry and commands without embedding secrets in code or the repo.
develops:
- skill: proto.mqtt
  to: 2
- skill: sec.tls
  to: 1
- skill: proto.wifi
  to: 1
- skill: iot.cloud-platform
  to: 1
context:
  platform: psoc-edge-e84
  lang: c
  ide: modustoolbox-vscode
  firmware: tesaiot-bitstream (HEX; source not public yet)
status: alpha
translation: done
slides: slides.md
source_sha256: 161867cd46ffbd92274440ad0c461018fb11081cc100b87b4da3de3f7dd651f3
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M06/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M06 — MQTT and MQTTs for Cloud Communication

**Course 1 · Module 6**
**Suggested time:** about 3.5–4 hours (concepts + Wi‑Fi + MQTT on the board / host)
**Format:** a hands-on lesson — connecting the device to a broker, publishing telemetry, subscribing to commands

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/mqtt-cloud.md) · [← Table of Contents](../../README.md) · [← M05](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) · [M07 BLE →](../../m07-ble/l01-ble-connectivity/README.md)

> **Note: which firmware the code in this lesson is written for** (checked on 2026-09-26)
>
> The C code in this lesson calls the API of the **TESAIoT Bitstream** firmware, called "TESA Firmware SDK" in the original, which is published as a ready-made HEX file (`tesaiot-bitstream-<version>.hex`) alongside Bitstream Studio in the [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/tree/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/hex) lab pack. **The source code of this firmware is not yet public.** Functions such as `cm55_trigger_connect`, `cm55_get_wifi_status`, `cm55_trigger_mqtt_connect`, `cm55_get_mqtt_status`, `cm55_trigger_mqtt_policy_set`, `cm33_mqtt_nvm_*`, `cm33_mqtt_stack_publish` and `bs_mqtt_telem_encode_json_*` therefore have no header you can open or build yourself. Read the snippets as concepts and a calling order. The calls to FreeRTOS and the Infineon PDL (such as `xTaskCreate`, `vTaskDelay`, `Cy_GPIO_*`) are ordinary public APIs.
>
> If you want code you can read and build from open source, see [tesaiot-pse84-devkit-sdk](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) (Apache-2.0), which is a **different codebase with different API names**. Examples already checked to do the same job as this lesson (commit `ef72c1b`):
>
> - [`proj_cm33_ns/examples/connectivity/10_wifi_join.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/10_wifi_join.c) — joining Wi-Fi on the CM33_NS (`app_wifi_init`, `app_wifi_connect_direct`, `app_wifi_get_ipv4`, `cy_wcm_*`)
> - [`proj_cm55/examples/connectivity/01_wifi_join_and_remember.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/connectivity/01_wifi_join_and_remember.c) — joining Wi-Fi from the CM55 through IPC to the CM33_NS (`wifi_manager_*`) — the same concept as "the CM55 commands the CM33, which owns the radio" in this lesson
> - [`bento_libs/claw/common/modules/tesaiot_mqtt/`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/tree/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_mqtt) — a TLS MQTT client on the CM33_NS, with `tesaiot_mqtt_connect` / `tesaiot_mqtt_publish` / `tesaiot_mqtt_is_connected` / `tesaiot_mqtt_disconnect` (read the module's README before using it)
>
> No equivalent found yet in the public SDK: encoding JSON telemetry as `bs_mqtt_telem_encode_json_*`, and a topic table in NVM (`cm33_mqtt_nvm_*`)

---

## Objectives (Learning Outcomes)

By the end of this lesson you should be able to:

1. Explain the **MQTT** principle and how it differs from **MQTTs** (MQTT over TLS)
2. Explain **Broker, Client, Topic, QoS, Retained Message**
3. Configure and command an MQTT connection through the **TESA Firmware SDK** (the CM55 → IPC → CM33 path)
4. Point at a broker, whether public / on a LAN / a general cloud (the same set of config fields)
5. **Publish** telemetry / events from the device
6. **Subscribe** to receive commands back to control the device
7. Design a suitable **payload** (JSON is the main path in the current SDK)
8. Explain the security approach: TLS, a root CA, a username/password
9. Do the exercise on the real board and check it with host tools

> **The snippets in this lesson** reference function names from the TESA Firmware SDK — use them together with an example project, or an example on the Developer Hub.
> More host examples: **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** · [Hackathon `web-app/` MQTT labs](https://github.com/drsanti/TESAIoT_Hackathon) · [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)

### Read alongside this chapter

| Document | Use when |
|---|---|
| [MQTT Essentials (HiveMQ)](https://www.hivemq.com/mqtt-essentials/) | The broker / topic / QoS / retain concepts |
| [MQTT version 5.0 / 3.1.1 OASIS overview](https://mqtt.org/) | The protocol spec |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | `ex09`–`ex15` MQTT in the browser + a broker in the Studio |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | Starting the broker / telemetry / the MQTT panel |
| [M05 — Sensor / AI prep](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) | The source of values to publish |
| [M04 — RTOS](../../m04-rtos/l01-freertos-programming/README.md) | A task that calls a trigger / waits on status |

---

## 1. MQTT in One Page

**MQTT** is a publish/subscribe protocol over TCP, suited to IoT with limited bandwidth and power.

| Term | Meaning |
|---|---|
| **Broker** | The middleman that receives/sends messages by topic |
| **Client** | A device or app that connects to the broker |
| **Topic** | A hierarchical channel name (such as `bitstream/<id>/sensors`) |
| **Publish** | Sending a message into a topic |
| **Subscribe** | Registering to receive messages from a topic |
| **QoS** | The delivery guarantee level (0 / 1 / 2 in the spec) |
| **Retain** | The broker keeps a topic's latest message for a new subscriber |

### MQTT vs MQTTs

| | MQTT (plain) | MQTTs |
|---|---|---|
| Transport layer | TCP | TCP + **TLS** |
| Common port | **1883** | **8883** |
| In this SDK | `tls = 0` | `tls = 1` (+ a root CA) |

> **Key phrase**
> MQTTs is not a separate protocol — it is MQTT wrapped in TLS.

Further reading: [HiveMQ MQTT Essentials](https://www.hivemq.com/mqtt-essentials/)

---

## 2. Where MQTT Lives in TESA Firmware

| Role | Core | API learners call often |
|---|---|---|
| Wi‑Fi STA | **CM33** | Through IPC from the CM55: `cm55_trigger_connect` … |
| MQTT client + TLS | **CM33** | `mqtt_manager_*` / `cm33_mqtt_stack_*` (the real owner) |
| Connecting / reading status from the app | **CM55** | `cm55_trigger_mqtt_*`, `cm55_get_mqtt_status` |
| Encoding JSON telemetry | **CM55** | `bs_mqtt_telem_encode_json_*` |

```text
[Sensors / App on CM55]
        │  cm55_trigger_mqtt_*  / JSON encode
        ▼
   IPC to CM33
        │
        ▼
[Wi‑Fi + cy_mqtt_* stack on CM33] ──TCP/TLS──► Broker
```

**MQTT will not come up on its own if Wi‑Fi is not yet CONNECTED** — you must join the AP first, every time.

---

## 3. Wi‑Fi First (Prerequisite)

```c
#include "cm55_ipc_app.h"

(void)cm55_trigger_connect("YOUR_SSID", "YOUR_WIFI_PASSWORD", 0U);

ipc_wifi_status_t st;
if (cm55_get_wifi_status(&st) && st.state == (uint8_t)IPC_WIFI_LINK_CONNECTED) {
    /* ready for MQTT */
}
```

Or through the example project's own Wi‑Fi helper:

```c
#include "example_wifi.h"

example_wifi_ipc_register();
example_wifi_ui_connect("YOUR_SSID", "YOUR_WIFI_PASSWORD");
```

> Use the SSID/password of the network you actually use — **never commit secrets to Git**

---

## 4. Connect, Status, Disconnect (CM55 API)

```c
#include "cm55_ipc_app.h"
#include "ipc_mqtt_types.h"

(void)cm55_trigger_mqtt_policy_set(IPC_MQTT_POLICY_FACTORY_DEFAULT); /* often 0x07 */
(void)cm55_trigger_mqtt_connect();

ipc_mqtt_status_t mqtt;
if (cm55_get_mqtt_status(&mqtt) && mqtt.state == 2U) { /* CONNECTED */
    /* mqtt.broker_host, mqtt.port, mqtt.tls, mqtt.effective_client_id */
}

(void)cm55_trigger_mqtt_disconnect();
```

| `mqtt.state` (approach) | Meaning |
|---|---|
| 0 | DISCONNECTED |
| 1 | CONNECTING |
| 2 | CONNECTED |
| 3 | ERROR |

### Policy bits (the factory default usually enables all three)

| Bit | Meaning in brief |
|---|---|
| `AUTO_CONNECT` | Try to connect once conditions are ready |
| `TELEMETRY_PUBLISH` | Allow publishing sensor values up to the broker |
| `MQTT_ENABLED` | Turns on the MQTT module |

---

## 5. Broker Configuration (Any Cloud / LAN)

The SDK uses one set of config fields to point at any broker — **there is no separate "TESA cloud" hostname baked into the firmware**.
A common factory demo value: a public host on the plain **1883** port (such as the HiveMQ public broker) — follow whatever value you have configured.

```c
#include "cm33_mqtt_nvm.h"

cm33_mqtt_config_v3_t cfg;
(void)cm33_mqtt_nvm_get_config(&cfg);

(void)strncpy(cfg.broker_host, "YOUR_BROKER_HOST", sizeof(cfg.broker_host) - 1U);
cfg.port = 1883U;   /* or 8883 when using TLS */
cfg.tls  = 0U;      /* 1 = MQTTs */
cfg.client_id_mode = CM33_MQTT_CLIENT_ID_MODE_AUTO_MAC;
(void)strncpy(cfg.username, "YOUR_USER", sizeof(cfg.username) - 1U);
(void)strncpy(cfg.password, "YOUR_PASSWORD", sizeof(cfg.password) - 1U);
cfg.keepalive_seconds = 60U;
cfg.root_ca_len = 0U; /* when tls=1 and len=0, an embedded root CA may be used (such as ISRG Root X1) */

(void)cm33_mqtt_nvm_set_config(&cfg);
```

| Lab scenario | Setup approach |
|---|---|
| A public demo | A public host, `1883`, `tls=0` |
| A broker on a LAN / a machine in the lab | The network's IP or hostname, `1883` |
| MQTTs | `tls=1`, port `8883`, a CA ready |
| Auth | Fill in the username/password when the broker requires it |

On the host, you may be able to set this through **Bitstream Studio** / BS2 MQTT commands instead of editing NVM directly — per the tool's guide.

---

## 6. Topics, Publish, Subscribe

### 6.1 MAC-based topic helpers

```c
#include "cm33_mqtt_client_id.h"

char topic[CM33_MQTT_TOPIC_MAX];
(void)cm33_mqtt_format_mac_topic(mac, CM33_MQTT_TOPIC_SUFFIX_SENSORS,
                                 topic, sizeof(topic));
/* → "bitstream/<MAC12>/sensors" */
```

| Common suffix | What it's for |
|---|---|
| `sensors` | Telemetry from the device |
| `actuators` | Commands into the device (subscribe) |
| `status` | Status / LWT, depending on config |

### 6.2 Topic table (publish + subscribe slots)

```c
cm33_mqtt_topic_table_t topics = {0};
topics.publish_count = 1U;
topics.telemetry_publish_slot = 0U;
(void)strncpy(topics.publish[0].topic, topic, sizeof(topics.publish[0].topic) - 1U);
topics.publish[0].qos = 0U;

topics.subscribe_count = 1U;
(void)cm33_mqtt_format_mac_topic(mac, CM33_MQTT_TOPIC_SUFFIX_ACTUATORS,
                                 topics.subscribe[0].topic,
                                 sizeof(topics.subscribe[0].topic));
topics.subscribe[0].qos = 0U;
(void)cm33_mqtt_nvm_set_topic_table(&topics);
```

### 6.3 QoS and retain — the spec vs the SDK's telemetry behaviour

| Concept in the MQTT spec | In the current SDK's telemetry path |
|---|---|
| QoS 0/1/2 | Publishing telemetry mainly uses **QoS 0** |
| Retain | Telemetry publishes are usually **retain = false** |
| QoS in the topic table | Affects subscribe / some config points |

Explain QoS/retain fully in theory — then practise against the example firmware's real behaviour.

### 6.4 Owner-path publish (CM33)

```c
#include "cm33_mqtt_stack.h"

if (cm33_mqtt_stack_is_connected()) {
    (void)cm33_mqtt_stack_publish(
        "bitstream/AABBCCDDEEFF/sensors",
        "{\"hello\":1}", 11);
}
```

---

## 7. Payload Design: JSON (Primary Path)

The main telemetry path in the SDK is a **JSON message**.
There is **no** ready-made CBOR path in the current MQTT path yet — if you need binary, that is extra design work outside the standard lab.

```c
#include "bitstream_mqtt_telemetry_json.h"

char json[512];
uint16_t len = 0U;
int16_t values[2] = {2500, 5500}; /* example scaled values from a sensor */

(void)bs_mqtt_telem_encode_json_readable(
    /* sensor_id */ 2U, /* mask */ 0x03U, /* counter */ 1U, /* t_ms */ 1000U,
    values, 2U, "bitstream-AABBCCDDEEFF",
    json, sizeof(json), &len);
```

Alternative: `bs_mqtt_telem_encode_json_scalar(...)` for a `values: [...]` form

### Forwarding from the sensor (architecture)

```text
sensor EVT (M05) → encode JSON on CM55 → relay to CM33 → publish to broker
```

Turn on `TELEMETRY_PUBLISH` in the policy so this path works per the configuration.

### Checking on the host

| Tool | Use when |
|---|---|
| MQTTX / mosquitto_sub | Subscribing to the board's topic |
| Hackathon `ex09`–`ex15` | Browser-based MQTT labs ([repo](https://github.com/drsanti/TESAIoT_Hackathon)) |
| The Bitstream Studio broker | When you want to use a local broker |

---

## 8. Security: TLS, Certificates, Authentication

| Layer | In this course |
|---|---|
| **TLS (MQTTs)** | `cfg.tls = 1`, port **8883** |
| **Server trust** | A PEM in NVM, or the embedded root CA when `root_ca_len = 0` |
| **Client auth** | A username / password in the config (if the broker requires it) |
| **Mutual TLS (client cert)** | **Not yet** a client cert/key field in the standard v3 config |
| **Over-the-air transport** | Your own Wi‑Fi + never embed a password in the repo |

```c
#include "cm33_mqtt_embedded_ca.h"

const char *ca = cm33_mqtt_embedded_root_ca();
size_t ca_len = cm33_mqtt_embedded_root_ca_size();
```

Practical guidance: use a trusted broker, rotate lab passwords, and keep the lab network separate from a real production network.

---

## 9. Cloud Providers: TESA vs Others

| Learner's question | Short answer |
|---|---|
| Do I need a special "TESA cloud API"? | One set of broker config fields points at any host |
| Can I use AWS IoT / Azure / HiveMQ Cloud? | Yes, in principle, if the endpoint, port, TLS and auth match what the config supports |
| What does the standard lab use? | Usually a public/LAN broker first, then a real cloud later |

---

## 10. Optional: CM33 Owner Stack (Deeper)

```c
#include "cm33_mqtt_manager.h"
#include "cm33_mqtt_stack.h"

(void)mqtt_manager_init();
(void)mqtt_manager_start();
(void)mqtt_manager_request_connect();
/* … */
(void)mqtt_manager_request_disconnect();
```

The lowest layer is Infineon's `cy_mqtt_*` — general learners can get by with just **`cm55_trigger_mqtt_*`** for the lab.

Under the hood: BS2 UART also has an MQTT command set (`MQTT_CONNECT`, etc.) for the host — used when working through the Bitstream Studio panel.

---

## 11. Module Summary

1. MQTT = pub/sub; **MQTTs = MQTT + TLS**
2. **Wi‑Fi always before MQTT**
3. Commanded from the CM55 with `cm55_trigger_mqtt_*`; the real session lives on the CM33
4. A topic like `bitstream/<MAC>/…` + policy bits
5. The main payload = **JSON**; publishing telemetry is QoS0 in the current path
6. Security = TLS + a CA + (optional) a user/pass
7. Next, **M07 BLE**, then **M08 Capstone**, which combines the labs and the course's documentation

### Next Steps

1. Do the exercise: [Lab](../l02-lab/README.md)
2. Keep the summary sheet: [Cheatsheet](resources/mqtt-cloud.md)
3. When ready, continue to **M07 — Bluetooth Low Energy (BLE)** ([M07 lesson](../../m07-ble/l01-ble-connectivity/README.md)), then finish with **M08 Capstone**

---

## References and Further Reading

### Course portals

1. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**
2. **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)**
3. **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** — MQTT web examples `ex09`–`ex15`

### MQTT concepts

4. [MQTT.org](https://mqtt.org/)
5. [HiveMQ MQTT Essentials](https://www.hivemq.com/mqtt-essentials/)
6. [HiveMQ — Public Broker](https://www.hivemq.com/public-mqtt-broker/) (use for testing only)

### Prior modules

7. [M05 — Sensor Data and Edge AI Preparation](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md)
8. [M04 — RTOS Programming](../../m04-rtos/l01-freertos-programming/README.md)

---

## Check your understanding

Three short questions in [quiz.yaml](quiz.yaml), one per objective of this lesson. Try answering them yourself first, then compare with the answer key and explanations in the file.

## Lab

Continue hands-on at [Lab: Wi-Fi, MQTT connect, publish and subscribe](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/mqtt-cloud.md) · [← Table of Contents](../../README.md) · [← M05](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) · [M07 BLE →](../../m07-ble/l01-ble-connectivity/README.md)

## Examples on the TESAIoT Developer Hub

Try the real thing on the TESAIoT Dev Kit: open examples on the Developer Hub to read the code, download it, or flash ready-made firmware.

- [TESA IoT Device → Platform (Server-TLS) — HTTPS or MQTTS via Mongoose](https://dev.tesaiot.dev/?example=developer-hub--device-servertls&q=device-servertls) — Unified, beginner-friendly C example that can send telemetry over either:
- [TESA IoT Device → Platform (mTLS) — HTTPS or MQTTS via Mongoose](https://dev.tesaiot.dev/?example=developer-hub--device-mtls&q=device-mtls) — Unified, intermediate-level C example that can send telemetry over either:
