---
id: fw-sdk.m06.l01
lang: th
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
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M06/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M06 — MQTT and MQTTs for Cloud Communication

**Course 1 · Module 6**  
**Suggested time:** ประมาณ 3.5–4 ชั่วโมง (แนวคิด + Wi‑Fi + MQTT บนบอร์ด / โฮสต์)  
**Format:** บทเรียนเชิงปฏิบัติ — เชื่อมอุปกรณ์กับ broker, publish telemetry, subscribe คำสั่ง

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/mqtt-cloud.md) · [← Table of Contents](../../README.md) · [← M05](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) · [M07 BLE →](../../m07-ble/l01-ble-connectivity/README.md)

> **หมายเหตุ: โค้ดในบทนี้เขียนสำหรับเฟิร์มแวร์ชุดใด** (ตรวจสอบเมื่อ 26 ก.ย. 2026)
>
> โค้ด C ในบทนี้เรียก API ของเฟิร์มแวร์ **TESAIoT Bitstream** ที่ต้นฉบับเรียกว่า “TESA Firmware SDK” ซึ่งเผยแพร่เป็นไฟล์ HEX สำเร็จรูป (`tesaiot-bitstream-<version>.hex`) คู่กับ Bitstream Studio ในแพ็กแล็บ [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/tree/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/hex) **ซอร์สโค้ดของเฟิร์มแวร์ชุดนี้ยังไม่เปิดเผยต่อสาธารณะ** ฟังก์ชันอย่าง `cm55_trigger_connect`, `cm55_get_wifi_status`, `cm55_trigger_mqtt_connect`, `cm55_get_mqtt_status`, `cm55_trigger_mqtt_policy_set`, `cm33_mqtt_nvm_*`, `cm33_mqtt_stack_publish`, `bs_mqtt_telem_encode_json_*` จึงยังไม่มี header ให้เปิดดูหรือนำไป build เอง ให้อ่าน snippet เป็นแนวคิดและลำดับการเรียกใช้ ส่วนการเรียก FreeRTOS และ Infineon PDL (เช่น `xTaskCreate`, `vTaskDelay`, `Cy_GPIO_*`) เป็น API สาธารณะตามปกติ
>
> ถ้าต้องการโค้ดที่อ่านและ build ได้จากซอร์สเปิด ให้ดู [tesaiot-pse84-devkit-sdk](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) (Apache-2.0) ซึ่งเป็น**คนละโค้ดเบสและตั้งชื่อ API ต่างกัน** ตัวอย่างที่ตรวจแล้วว่าทำงานเรื่องเดียวกับบทนี้ (commit `ef72c1b`):
>
> - [`proj_cm33_ns/examples/connectivity/10_wifi_join.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/10_wifi_join.c) — join Wi-Fi บน CM33_NS (`app_wifi_init`, `app_wifi_connect_direct`, `app_wifi_get_ipv4`, `cy_wcm_*`)
> - [`proj_cm55/examples/connectivity/01_wifi_join_and_remember.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/connectivity/01_wifi_join_and_remember.c) — join Wi-Fi จาก CM55 ผ่าน IPC ไป CM33_NS (`wifi_manager_*`) — แนวคิดเดียวกับ “CM55 สั่ง CM33 เป็นเจ้าของวิทยุ” ในบทนี้
> - [`bento_libs/claw/common/modules/tesaiot_mqtt/`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/tree/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_mqtt) — client MQTT แบบ TLS บน CM33_NS มี `tesaiot_mqtt_connect` / `tesaiot_mqtt_publish` / `tesaiot_mqtt_is_connected` / `tesaiot_mqtt_disconnect` (อ่าน README ของโมดูลก่อนใช้)
>
> ยังไม่พบตัวเทียบใน SDK สาธารณะ: การเข้ารหัส JSON telemetry แบบ `bs_mqtt_telem_encode_json_*` และตาราง topic ใน NVM (`cm33_mqtt_nvm_*`)

---

## เป้าหมาย (Learning Outcomes)

เมื่อเรียนจบ คุณควรทำได้ดังนี้:

1. อธิบายหลักการ **MQTT** และความต่างจาก **MQTTs** (MQTT over TLS)  
2. อธิบาย **Broker, Client, Topic, QoS, Retained Message**  
3. ตั้งค่าและสั่งเชื่อมต่อ MQTT ผ่าน **TESA Firmware SDK** (เส้นทาง CM55 → IPC → CM33)  
4. ชี้ broker ได้ทั้งของสาธารณะ / LAN / คลาวด์ทั่วไป (ฟิลด์คอนฟิกชุดเดียวกัน)  
5. **Publish** telemetry / event จากอุปกรณ์  
6. **Subscribe** เพื่อรับคำสั่งกลับมาควบคุมอุปกรณ์  
7. ออกแบบ **payload** ที่เหมาะสม (JSON เป็นเส้นทางหลักใน SDK ปัจจุบัน)  
8. อธิบายแนวทางความปลอดภัย: TLS, root CA, username/password  
9. ทำแบบฝึกบนบอร์ดจริงและตรวจด้วยเครื่องมือโฮสต์  

> **Snippet ในบทนี้** อ้างชื่อฟังก์ชันจาก TESA Firmware SDK — ใช้ร่วมกับโปรเจกต์ตัวอย่างหรือตัวอย่างบน Developer Hub  
> ดูตัวอย่างโฮสต์เพิ่ม: **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** · [Hackathon `web-app/` MQTT labs](https://github.com/drsanti/TESAIoT_Hackathon) · [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)

### Read alongside this chapter

| เอกสาร | ใช้เมื่อ |
|---|---|
| [MQTT Essentials (HiveMQ)](https://www.hivemq.com/mqtt-essentials/) | แนวคิด broker / topic / QoS / retain |
| [MQTT version 5.0 / 3.1.1 OASIS overview](https://mqtt.org/) | สเปกโปรโตคอล |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | `ex09`–`ex15` MQTT ในเบราว์เซอร์ + broker ใน Studio |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | Start broker / telemetry / MQTT panel |
| [M05 — Sensor / AI prep](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) | แหล่งค่าที่จะ publish |
| [M04 — RTOS](../../m04-rtos/l01-freertos-programming/README.md) | task ที่เรียก trigger / รอสถานะ |

---

## 1. MQTT in One Page

**MQTT** เป็นโปรโตคอล publish/subscribe บน TCP เหมาะกับ IoT ที่แบนด์วิดท์และพลังงานจำกัด

| คำ | ความหมาย |
|---|---|
| **Broker** | ตัวกลางรับ/ส่งข้อความตาม topic |
| **Client** | อุปกรณ์หรือแอปที่เชื่อม broker |
| **Topic** | ชื่อช่องข้อความแบบลำดับชั้น (เช่น `bitstream/<id>/sensors`) |
| **Publish** | ส่งข้อความเข้า topic |
| **Subscribe** | ลงทะเบียนรับข้อความจาก topic |
| **QoS** | ระดับการรับประกันการส่ง (0 / 1 / 2 ในสเปก) |
| **Retain** | broker เก็บข้อความล่าสุดของ topic ให้ subscriber ใหม่ |

### MQTT vs MQTTs

| | MQTT (plain) | MQTTs |
|---|---|---|
| ชั้นขนส่ง | TCP | TCP + **TLS** |
| พอร์ตที่พบบ่อย | **1883** | **8883** |
| ใน SDK นี้ | `tls = 0` | `tls = 1` (+ root CA) |

> **Key phrase**  
> MQTTs ไม่ใช่โปรโตคอลคนละตัว — คือ MQTT ที่ห่อด้วย TLS

อ่านเสริม: [HiveMQ MQTT Essentials](https://www.hivemq.com/mqtt-essentials/)

---

## 2. Where MQTT Lives in TESA Firmware

| บทบาท | คอร์ | API ที่ผู้เรียนเรียกบ่อย |
|---|---|---|
| Wi‑Fi STA | **CM33** | ผ่าน IPC จาก CM55: `cm55_trigger_connect` … |
| MQTT client + TLS | **CM33** | `mqtt_manager_*` / `cm33_mqtt_stack_*` (เจ้าของจริง) |
| สั่งเชื่อม / อ่านสถานะจากแอป | **CM55** | `cm55_trigger_mqtt_*`, `cm55_get_mqtt_status` |
| เข้ารหัส JSON telemetry | **CM55** | `bs_mqtt_telem_encode_json_*` |

```text
[Sensors / App on CM55]
        │  cm55_trigger_mqtt_*  / JSON encode
        ▼
   IPC to CM33
        │
        ▼
[Wi‑Fi + cy_mqtt_* stack on CM33] ──TCP/TLS──► Broker
```

**MQTT จะไม่ขึ้นเองถ้า Wi‑Fi ยังไม่ CONNECTED** — ต้อง join AP ก่อนทุกครั้ง

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

หรือผ่านตัวอย่าง Wi‑Fi ของโปรเจกต์ตัวอย่าง:

```c
#include "example_wifi.h"

example_wifi_ipc_register();
example_wifi_ui_connect("YOUR_SSID", "YOUR_WIFI_PASSWORD");
```

> ใช้ค่า SSID/รหัสผ่านของเครือข่ายที่คุณใช้ — **อย่า commit ความลับลง Git**

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

| `mqtt.state` (แนวทาง) | ความหมาย |
|---|---|
| 0 | DISCONNECTED |
| 1 | CONNECTING |
| 2 | CONNECTED |
| 3 | ERROR |

### Policy bits (factory often enables all three)

| Bit | ความหมายโดยสรุป |
|---|---|
| `AUTO_CONNECT` | พยายามเชื่อมเมื่อเงื่อนไขพร้อม |
| `TELEMETRY_PUBLISH` | อนุญาต publish ค่าเซ็นเซอร์ขึ้น broker |
| `MQTT_ENABLED` | เปิดโมดูล MQTT |

---

## 5. Broker Configuration (Any Cloud / LAN)

SDK ใช้คอนฟิกชุดเดียวชี้ไปยัง broker ใดก็ได้ — **ไม่มี hostname “TESA cloud” แยกต่างหากในเฟิร์มแวร์**  
ค่าโรงงานสาธิตที่พบบ่อย: host สาธารณะพอร์ต plain **1883** (เช่น HiveMQ public) — ให้ยึดค่าที่คุณตั้งไว้

```c
#include "cm33_mqtt_nvm.h"

cm33_mqtt_config_v3_t cfg;
(void)cm33_mqtt_nvm_get_config(&cfg);

(void)strncpy(cfg.broker_host, "YOUR_BROKER_HOST", sizeof(cfg.broker_host) - 1U);
cfg.port = 1883U;   /* หรือ 8883 เมื่อใช้ TLS */
cfg.tls  = 0U;      /* 1 = MQTTs */
cfg.client_id_mode = CM33_MQTT_CLIENT_ID_MODE_AUTO_MAC;
(void)strncpy(cfg.username, "YOUR_USER", sizeof(cfg.username) - 1U);
(void)strncpy(cfg.password, "YOUR_PASSWORD", sizeof(cfg.password) - 1U);
cfg.keepalive_seconds = 60U;
cfg.root_ca_len = 0U; /* เมื่อ tls=1 และ len=0 อาจใช้ embedded root CA (เช่น ISRG Root X1) */

(void)cm33_mqtt_nvm_set_config(&cfg);
```

| สถานการณ์แล็บ | แนวตั้งค่า |
|---|---|
| Demo สาธารณะ | host สาธารณะ, `1883`, `tls=0` |
| Broker ใน LAN / เครื่องในแล็บ | IP หรือ hostname ในเครือข่าย, `1883` |
| MQTTs | `tls=1`, พอร์ต `8883`, CA พร้อม |
| Auth | กรอก username/password เมื่อ broker บังคับ |

บนโฮสต์อาจตั้งค่าผ่าน **Bitstream Studio** / BS2 MQTT commands แทนการแก้ NVM ตรง ๆ — ตามคู่มือของเครื่องมือ

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

| Suffix ที่พบบ่อย | ใช้ทำอะไร |
|---|---|
| `sensors` | telemetry จากอุปกรณ์ |
| `actuators` | คำสั่งเข้าอุปกรณ์ (subscribe) |
| `status` | สถานะ / LWT ตามคอนฟิก |

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

### 6.3 QoS and retain — สเปก vs พฤติกรรม telemetry ใน SDK

| แนวคิดในสเปก MQTT | ในเส้นทาง telemetry ของ SDK ปัจจุบัน |
|---|---|
| QoS 0/1/2 | Publish telemetry ใช้ **QoS 0** เป็นหลัก |
| Retain | Telemetry publish มัก **retain = false** |
| QoS ใน topic table | มีผลกับ subscribe / คอนฟิกบางจุด |

อธิบาย QoS/retain ให้ครบในทฤษฎี — แล้วฝึกตามพฤติกรรมจริงของเฟิร์มแวร์ตัวอย่าง

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

เส้นทาง telemetry หลักใน SDK คือ **JSON ข้อความ**  
**ยังไม่มี** เส้นทาง CBOR สำเร็จรูปใน MQTT path ปัจจุบัน — ถ้าต้องการ binary ให้เป็นขั้นออกแบบเพิ่มนอกแล็บมาตรฐาน

```c
#include "bitstream_mqtt_telemetry_json.h"

char json[512];
uint16_t len = 0U;
int16_t values[2] = {2500, 5500}; /* ตัวอย่างค่าสเกลจากเซ็นเซอร์ */

(void)bs_mqtt_telem_encode_json_readable(
    /* sensor_id */ 2U, /* mask */ 0x03U, /* counter */ 1U, /* t_ms */ 1000U,
    values, 2U, "bitstream-AABBCCDDEEFF",
    json, sizeof(json), &len);
```

ทางเลือก: `bs_mqtt_telem_encode_json_scalar(...)` สำหรับรูปแบบ `values: [...]`

### ส่งต่อจากเซ็นเซอร์ (สถาปัตยกรรม)

```text
sensor EVT (M05) → encode JSON on CM55 → relay to CM33 → publish to broker
```

เปิด `TELEMETRY_PUBLISH` ใน policy เพื่อให้เส้นทางนี้ทำงานตามที่ตั้งค่าไว้

### ตรวจบนโฮสต์

| เครื่องมือ | ใช้เมื่อ |
|---|---|
| MQTTX / mosquitto_sub | subscribe topic ของบอร์ด |
| Hackathon `ex09`–`ex15` | แล็บ MQTT ในเบราว์เซอร์ ([repo](https://github.com/drsanti/TESAIoT_Hackathon)) |
| Bitstream Studio broker | เมื่อต้องการใช้ broker ในเครื่อง |

---

## 8. Security: TLS, Certificates, Authentication

| ชั้น | ในหลักสูตรนี้ |
|---|---|
| **TLS (MQTTs)** | `cfg.tls = 1`, พอร์ต **8883** |
| **Server trust** | PEM ใน NVM หรือ embedded root CA เมื่อ `root_ca_len = 0` |
| **Client auth** | username / password ในคอนฟิก (ถ้า broker ต้องการ) |
| **Mutual TLS (client cert)** | **ยังไม่มี** ฟิลด์ client cert/key ในคอนฟิก v3 มาตรฐาน |
| **Transport บนอากาศ** | Wi‑Fi ของตัวเอง + อย่าฝังรหัสผ่านใน repo |

```c
#include "cm33_mqtt_embedded_ca.h"

const char *ca = cm33_mqtt_embedded_root_ca();
size_t ca_len = cm33_mqtt_embedded_root_ca_size();
```

แนวปฏิบัติ: ใช้ broker ที่เชื่อถือได้, หมุนรหัสผ่านในแล็บ, แยกเครือข่ายแล็บออกจากเครือข่ายใช้งานจริง

---

## 9. Cloud Providers: TESA vs Others

| คำถามผู้เรียน | คำตอบสั้น |
|---|---|
| ต้องมี “TESA cloud API” พิเศษไหม? | คอนฟิก broker ชุดเดียวชี้ไปที่โฮสต์ใดก็ได้ |
| ใช้ AWS IoT / Azure / HiveMQ Cloud ได้ไหม? | ได้ในหลักการ ถ้า endpoint,พอร์ต, TLS และ auth ตรงกับที่คอนฟิกรองรับ |
| แล็บมาตรฐานใช้อะไร? | มักเป็น public/LAN broker ก่อน แล้วค่อย cloud จริง |

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

ชั้นล่างสุดเป็น Infineon `cy_mqtt_*` — ผู้เรียนทั่วไปใช้ **`cm55_trigger_mqtt_*`** ก็เพียงพอสำหรับแล็บ

ใต้ฝา: BS2 UART ยังมีชุดคำสั่ง MQTT (`MQTT_CONNECT` ฯลฯ) สำหรับโฮสต์ — ใช้เมื่อทำงานผ่านแผง Bitstream Studio

---

## 11. Module Summary

1. MQTT = pub/sub; **MQTTs = MQTT + TLS**  
2. **Wi‑Fi ก่อน MQTT** เสมอ  
3. สั่งจาก CM55 ด้วย `cm55_trigger_mqtt_*`; เซสชันจริงอยู่ CM33  
4. Topic แบบ `bitstream/<MAC>/…` + policy bits  
5. Payload หลัก = **JSON**; telemetry publish เป็น QoS0 ในพาธปัจจุบัน  
6. ความปลอดภัย = TLS + CA + (optional) user/pass  
7. ต่อไป **M07 BLE** แล้ว **M08 Capstone** รวมแล็บและเอกสารหลักสูตร  

### Next Steps

1. ทำแบบฝึก: [Lab](../l02-lab/README.md)  
2. เก็บแผ่นสรุป: [Cheatsheet](resources/mqtt-cloud.md)  
3. เมื่อพร้อม ไปต่อ **M07 — Bluetooth Low Energy (BLE)** ([บทเรียน M07](../../m07-ble/l01-ble-connectivity/README.md)) แล้วจบด้วย **M08 Capstone**

---

## References and Further Reading

### Course portals

1. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**  
2. **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)**  
3. **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** — MQTT web examples `ex09`–`ex15`  

### MQTT concepts

4. [MQTT.org](https://mqtt.org/)  
5. [HiveMQ MQTT Essentials](https://www.hivemq.com/mqtt-essentials/)  
6. [HiveMQ — Public Broker](https://www.hivemq.com/public-mqtt-broker/) (ใช้สำหรับทดสอบเท่านั้น)

### Prior modules

7. [M05 — Sensor Data and Edge AI Preparation](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md)  
8. [M04 — RTOS Programming](../../m04-rtos/l01-freertos-programming/README.md)  

---

## เช็กความเข้าใจ

คำถามสั้นสามข้อใน [quiz.yaml](quiz.yaml) ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อน แล้วค่อยเทียบกับเฉลยและคำอธิบายในไฟล์

## แล็บ

ลงมือต่อที่ [แล็บ: Wi-Fi, MQTT connect, publish และ subscribe](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/mqtt-cloud.md) · [← Table of Contents](../../README.md) · [← M05](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) · [M07 BLE →](../../m07-ble/l01-ble-connectivity/README.md)

## ตัวอย่างบน TESAIoT Developer Hub

ลองของจริงบน TESAIoT Dev Kit: เปิดตัวอย่างบน Developer Hub เพื่ออ่านโค้ด ดาวน์โหลด หรือ flash เฟิร์มแวร์สำเร็จรูป

- [TESA IoT Device → Platform (Server-TLS) — HTTPS or MQTTS via Mongoose](https://dev.tesaiot.dev/?example=developer-hub--device-servertls&q=device-servertls) — Unified, beginner-friendly C example that can send telemetry over either:
- [TESA IoT Device → Platform (mTLS) — HTTPS or MQTTS via Mongoose](https://dev.tesaiot.dev/?example=developer-hub--device-mtls&q=device-mtls) — Unified, intermediate-level C example that can send telemetry over either:
