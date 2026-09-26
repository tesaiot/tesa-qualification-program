---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 6.1 — MQTT และ MQTTs บนอุปกรณ์ Edge"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT) · CC BY-NC 4.0"
---
<style>
section { font-size: 24px; padding: 40px 52px; justify-content: flex-start; }
section h1 { font-size: 1.45em; line-height: 1.12; margin: 0 0 .22em; }
section h2 { font-size: 1.12em; margin: .15em 0; }
section h3 { font-size: 1.0em; margin: .12em 0; }
section p, section li { margin: .16em 0; line-height: 1.32; }
section img { max-width: 100%; height: auto; }
section svg { max-height: 250px; }
section table { font-size: .78em; }
section pre { font-size: .70em; line-height: 1.32; background:#0d1117; color:#e6edf3; border:1px solid #30363d; border-radius:8px; padding:12px 16px; box-shadow:0 2px 8px rgba(0,0,0,.25); }
section pre code { white-space: pre-wrap; background:transparent; color:inherit; } section pre .hljs-comment{color:#8b949e;font-style:italic} section pre .hljs-keyword,section pre .hljs-built_in,section pre .hljs-literal{color:#ff7b72} section pre .hljs-string{color:#a5d6ff} section pre .hljs-number{color:#79c0ff} section pre .hljs-title,section pre .hljs-title.function_,section pre .hljs-section{color:#d2a8ff} section pre .hljs-meta{color:#ffa657} section pre .hljs-attr,section pre .hljs-attribute,section pre .hljs-name{color:#7ee787}
section blockquote { margin: .25em 0; font-size: .92em; }
/* two images on a line (parity / 2x2 grids) stay side-by-side and small */
section p > img + img { margin-left: 10px; }
/* scroll-within-slide: dense slides scroll instead of clipping */
section { overflow-y: auto; overflow-x: hidden; }
section::-webkit-scrollbar { width: 11px; }
section::-webkit-scrollbar-thumb { background:#4a90d9; border-radius:6px; }
section::-webkit-scrollbar-track { background:rgba(0,0,0,.06); }
/* image drop-shadow + cover-slide readability (auto) */
section img{filter:drop-shadow(0 3px 12px rgba(0,0,0,.5))}
section.cover *{color:#fff !important}
section.cover h1,section.cover h2,section.cover h3,section.cover p,section.cover li,section.cover strong,section.cover em,section.cover blockquote,section.cover div{text-shadow:0 2px 9px rgba(0,0,0,.92),0 0 3px rgba(0,0,0,.8)}
section.cover div[style*="background:#"],section.cover div[style*="background: #"]{background:rgba(10,14,20,.66) !important;border-color:rgba(120,200,255,.45) !important;max-width:62%}
section.cover blockquote{border-left:4px solid rgba(120,200,255,.6) !important;background:rgba(13,17,23,.55) !important;border-radius:6px;padding:.3em .6em}
section.cover h1,section.cover h2,section.cover h3,section.cover p,section.cover blockquote{max-width:60%}
section.cover div:not(:has(img)){max-width:62%}
section.cover img{filter:none}
</style>

<!-- _class: cover -->

# บทเรียน 6.1 — MQTT และ MQTTs บนอุปกรณ์ Edge

## หลักการ publish/subscribe เส้นทางเชื่อมต่อของเฟิร์มแวร์ (Wi-Fi → MQTT) การตั้งค่า broker topic payload JSON และความปลอดภัยด้วย TLS

**หลักสูตร TESA Firmware SDK สำหรับ Edge AI — โมดูล 6 · บทเรียน 1**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. อธิบาย broker, client, topic, QoS และ retain และบอกความต่างของ MQTT กับ MQTTs (TLS, พอร์ต 1883 / 8883)
2. เรียงเส้นทางเชื่อมต่อของเฟิร์มแวร์ได้ถูกต้อง: join Wi-Fi ให้ CONNECTED ก่อน แล้วจึงสั่งเชื่อม MQTT และอ่านสถานะ
3. ออกแบบ topic และ payload JSON สำหรับ telemetry และคำสั่ง โดยไม่ฝังความลับในโค้ดหรือ repo

---

## ก่อนเริ่ม

- ผ่าน [บทเรียน 5.2 — แล็บ M05](../../m05-sensor-data/l02-lab/README.md) มาแล้ว
- ใช้บอร์ดจริง: TESAIoT Dev Kit หรือ Eva Kit (KIT_PSE84_EVAL) พร้อมเครือข่าย Wi-Fi และ broker ของคุณเอง
- **อย่า commit รหัสผ่าน Wi-Fi หรือ broker ลง Git**

> **หมายเหตุสำคัญ (ตรวจสอบเมื่อ 26 ก.ย. 2026):** โค้ด C ในบทนี้เรียก API ของเฟิร์มแวร์ TESAIoT Bitstream ที่ยังไม่เปิดซอร์ส ฟังก์ชันอย่าง `cm55_trigger_connect`, `cm55_get_wifi_status`, `cm55_trigger_mqtt_connect`, `cm55_get_mqtt_status`, `cm33_mqtt_nvm_*`, `cm33_mqtt_stack_publish`, `bs_mqtt_telem_encode_json_*` จึงยังไม่มี header ให้เปิดดูหรือ build เอง — อ่านเป็นแนวคิดและลำดับการเรียกใช้

---

## ดูของจริงก่อน — MQTT ในหน้าเดียว

**MQTT** เป็นโปรโตคอล publish/subscribe บน TCP เหมาะกับ IoT ที่แบนด์วิดท์และพลังงานจำกัด

| คำ | ความหมาย |
|---|---|
| Broker | ตัวกลางรับ/ส่งข้อความตาม topic |
| Client | อุปกรณ์หรือแอปที่เชื่อม broker |
| Topic | ชื่อช่องข้อความแบบลำดับชั้น (เช่น `bitstream/<id>/sensors`) |
| QoS | ระดับการรับประกันการส่ง (0 / 1 / 2 ในสเปก) |
| Retain | broker เก็บข้อความล่าสุดของ topic ให้ subscriber ใหม่ |

| | MQTT (plain) | MQTTs |
|---|---|---|
| ชั้นขนส่ง | TCP | TCP + **TLS** |
| พอร์ตที่พบบ่อย | **1883** | **8883** |

> **Key phrase**: MQTTs ไม่ใช่โปรโตคอลคนละตัว — คือ MQTT ที่ห่อด้วย TLS

---

## แนวคิด — MQTT อยู่ตรงไหนใน TESA Firmware

| บทบาท | คอร์ | API ที่ผู้เรียนเรียกบ่อย |
|---|---|---|
| Wi‑Fi STA | CM33 | ผ่าน IPC จาก CM55: `cm55_trigger_connect` … |
| MQTT client + TLS | CM33 | `mqtt_manager_*` / `cm33_mqtt_stack_*` (เจ้าของจริง) |
| สั่งเชื่อม / อ่านสถานะจากแอป | CM55 | `cm55_trigger_mqtt_*`, `cm55_get_mqtt_status` |
| เข้ารหัส JSON telemetry | CM55 | `bs_mqtt_telem_encode_json_*` |

```text
[Sensors / App on CM55] → cm55_trigger_mqtt_* / JSON encode → IPC to CM33
                                                                    │
                                    [Wi‑Fi + cy_mqtt_* stack on CM33] ──TCP/TLS──► Broker
```

**MQTT จะไม่ขึ้นเองถ้า Wi‑Fi ยังไม่ CONNECTED** — ต้อง join AP ก่อนทุกครั้ง

---

## ตัวอย่างสมบูรณ์ — Wi‑Fi ก่อน แล้วค่อย MQTT

```c
#include "cm55_ipc_app.h"

(void)cm55_trigger_connect("YOUR_SSID", "YOUR_WIFI_PASSWORD", 0U);

ipc_wifi_status_t st;
if (cm55_get_wifi_status(&st) && st.state == (uint8_t)IPC_WIFI_LINK_CONNECTED) {
    /* ready for MQTT */
}
```

```c
#include "cm55_ipc_app.h"
#include "ipc_mqtt_types.h"

(void)cm55_trigger_mqtt_connect();

ipc_mqtt_status_t mqtt;
if (cm55_get_mqtt_status(&mqtt) && mqtt.state == 2U) { /* CONNECTED */ }
```

จาก [README.md](README.md) หัวข้อ 3–4 — ใช้ SSID/รหัสผ่านของเครือข่ายที่คุณใช้เอง อย่า commit ลง Git

---

## แนวคิด — ตั้งค่า broker (ชี้ไปที่ใดก็ได้)

SDK ใช้คอนฟิกชุดเดียวชี้ไปยัง broker ใดก็ได้ — **ไม่มี hostname "TESA cloud" แยกต่างหากในเฟิร์มแวร์**

| สถานการณ์แล็บ | แนวตั้งค่า |
|---|---|
| Demo สาธารณะ | host สาธารณะ, พอร์ต `1883`, `tls=0` |
| Broker ใน LAN / เครื่องในแล็บ | IP หรือ hostname ในเครือข่าย, `1883` |
| MQTTs | `tls=1`, พอร์ต `8883`, CA พร้อม |
| Auth | กรอก username/password เมื่อ broker บังคับ |

```c
cfg.port = 1883U;   /* หรือ 8883 เมื่อใช้ TLS */
cfg.tls  = 0U;      /* 1 = MQTTs */
cfg.client_id_mode = CM33_MQTT_CLIENT_ID_MODE_AUTO_MAC;
```

---

## ตัวอย่างสมบูรณ์ — Topic และ payload JSON

```c
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

เส้นทาง telemetry หลักใน SDK คือ **JSON ข้อความ** — ยังไม่มีเส้นทาง CBOR สำเร็จรูปในพาธ MQTT ปัจจุบัน

---

## แนวคิด — QoS/retain ในสเปกเทียบกับพฤติกรรมจริง

| แนวคิดในสเปก MQTT | ในเส้นทาง telemetry ของ SDK ปัจจุบัน |
|---|---|
| QoS 0/1/2 | Publish telemetry ใช้ **QoS 0** เป็นหลัก |
| Retain | Telemetry publish มัก **retain = false** |
| QoS ใน topic table | มีผลกับ subscribe / คอนฟิกบางจุด |

```c
if (cm33_mqtt_stack_is_connected()) {
    (void)cm33_mqtt_stack_publish("bitstream/AABBCCDDEEFF/sensors",
                                  "{\"hello\":1}", 11);
}
```

อธิบาย QoS/retain ให้ครบในทฤษฎี — แล้วฝึกตามพฤติกรรมจริงของเฟิร์มแวร์ตัวอย่าง

---

## แนวคิด — ความปลอดภัย: TLS, Certificates, Authentication

| ชั้น | ในหลักสูตรนี้ |
|---|---|
| TLS (MQTTs) | `cfg.tls = 1`, พอร์ต **8883** |
| Server trust | PEM ใน NVM หรือ embedded root CA เมื่อ `root_ca_len = 0` |
| Client auth | username / password ในคอนฟิก (ถ้า broker ต้องการ) |
| Mutual TLS (client cert) | **ยังไม่มี** ฟิลด์ client cert/key ในคอนฟิก v3 มาตรฐาน |

แนวปฏิบัติ: ใช้ broker ที่เชื่อถือได้ หมุนรหัสผ่านในแล็บ แยกเครือข่ายแล็บออกจากเครือข่ายใช้งานจริง

---

## ฝึกเติม/แล็บ

[แล็บ: Wi-Fi, MQTT connect, publish และ subscribe](../l02-lab/README.md)

- Join Wi-Fi จนสถานะ CONNECTED
- ตั้งค่า broker (host/port/tls) แล้วสั่งเชื่อม MQTT และตรวจสถานะ
- Publish telemetry เป็น JSON อย่างน้อยหนึ่งค่า
- Subscribe topic คำสั่งแล้วสาธิตว่าอุปกรณ์ตอบสนองได้

---

## เช็กความเข้าใจ

1. MQTTs ต่างจาก MQTT อย่างไรตามบทเรียน
2. สั่ง MQTT connect แล้วสถานะไม่ขึ้น CONNECTED ทั้งที่คอนฟิก broker ถูก สิ่งแรกที่ควรตรวจคืออะไร
3. เส้นทาง telemetry หลักในเฟิร์มแวร์ของบทเรียนใช้ payload และ QoS แบบใด

---

## ไปต่อ

- MQTT = pub/sub; **MQTTs = MQTT + TLS**
- **Wi‑Fi ก่อน MQTT** เสมอ — สั่งจาก CM55 ด้วย `cm55_trigger_mqtt_*`; เซสชันจริงอยู่ CM33
- Topic แบบ `bitstream/<MAC>/…` + policy bits · Payload หลัก = **JSON**; telemetry publish เป็น QoS0 ในพาธปัจจุบัน
- ความปลอดภัย = TLS + CA + (optional) user/pass — ต่อไป **โมดูล 7 BLE** แล้ว **โมดูล 8 Capstone**

[บทเรียนโมดูล 7 →](../../m07-ble/l01-ble-connectivity/README.md)

---

## แหล่งที่มา

"บทเรียน 6.1 — MQTT และ MQTTs บนอุปกรณ์ Edge" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C1 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
