---
id: fw-sdk.m07.l01
lang: th
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
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M07/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M07 — Bluetooth Low Energy (BLE) Connectivity

**Course 1 · Module 7**  
**Suggested time:** ประมาณ 3–3.5 ชั่วโมง (แนวคิด + peripheral status/ADV + host demo)  
**Format:** บทเรียนเชิงปฏิบัติ — เปรียบเทียบกับ MQTT (M06), เชื่อมโฮสต์ท้องถิ่นผ่าน BLE

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/ble-connectivity.md) · [← Table of Contents](../../README.md) · [← M06](../../m06-mqtt/l01-mqtt-and-mqtts/README.md) · [M08 →](../../m08-capstone/l01-capstone-and-resources/README.md)

> **หมายเหตุ: โค้ดในบทนี้เขียนสำหรับเฟิร์มแวร์ชุดใด** (ตรวจสอบเมื่อ 26 ก.ย. 2026)
>
> โค้ด C ในบทนี้เรียก API ของเฟิร์มแวร์ **TESAIoT Bitstream** ที่ต้นฉบับเรียกว่า “TESA Firmware SDK” ซึ่งเผยแพร่เป็นไฟล์ HEX สำเร็จรูป (`tesaiot-bitstream-<version>.hex`) คู่กับ Bitstream Studio ในแพ็กแล็บ [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/tree/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/hex) **ซอร์สโค้ดของเฟิร์มแวร์ชุดนี้ยังไม่เปิดเผยต่อสาธารณะ** ฟังก์ชันอย่าง `cm55_ble_periph_status_get_sync`, `cm55_ble_periph_adv_ctrl_sync`, `cm55_trigger_ble_periph_*`, `cm55_ble_request_scan_*`, `cm55_ble_ipc_set_event_handler` จึงยังไม่มี header ให้เปิดดูหรือนำไป build เอง ให้อ่าน snippet เป็นแนวคิดและลำดับการเรียกใช้ ส่วนการเรียก FreeRTOS และ Infineon PDL (เช่น `xTaskCreate`, `vTaskDelay`, `Cy_GPIO_*`) เป็น API สาธารณะตามปกติ
>
> ถ้าต้องการโค้ดที่อ่านและ build ได้จากซอร์สเปิด ให้ดู [tesaiot-pse84-devkit-sdk](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) (Apache-2.0) ซึ่งเป็น**คนละโค้ดเบสและตั้งชื่อ API ต่างกัน** ตัวอย่างที่ตรวจแล้วว่าทำงานเรื่องเดียวกับบทนี้ (commit `ef72c1b`):
>
> - [`proj_cm33_ns/examples/ble/01_nus_bring_up_and_talk.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/ble/01_nus_bring_up_and_talk.c) — BLE peripheral แบบ Nordic UART Service: advertise อ่านสถานะลิงก์ และส่งข้อมูล (`ble_nus_init`, `ble_nus_get_state`, `ble_nus_rearm_advertising`, `ble_nus_send`) — ไฟล์นี้ระบุเองว่ายังรันบน template ที่ส่งมอบไม่ได้ เพราะ `libbento_secure.a` ยังไม่อยู่ใน `LDLIBS`
>
> ยังไม่พบตัวเทียบใน SDK สาธารณะ: เส้นทาง scan / observer (`cm55_ble_request_scan_*`) — `ble_nus` ใน SDK เป็นบทบาท peripheral อย่างเดียว

> **โฮสต์ `ble-flet` ยังไม่เผยแพร่** — [README ของ TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/blob/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/README.md) (commit `f5f09a6`) ระบุว่า `python-app/`, `ble-react/` และ `ble-flet/` เป็นของผู้ดูแลและไม่อยู่ใน repo สาธารณะ ให้ใช้เส้นทางสำรองที่บทเรียนเสนอไว้แล้ว คือ GATT explorer ทั่วไป เช่น nRF Connect, LightBlue หรือ AIROC™ Bluetooth® Connect

---

## เป้าหมาย (Learning Outcomes)

เมื่อเรียนจบ คุณควรทำได้ดังนี้:

1. อธิบายบทบาท **BLE** ในผลิตภัณฑ์ Edge (local / phone / desktop) เทียบกับ **MQTT** (cloud / broker)  
2. อธิบายคำสำคัญ: **GAP, GATT, Peripheral, Central, Advertising, Connection, Notification**  
3. ชี้ได้ว่าใน TESA Firmware SDK **CM33 เป็นเจ้าของ BLE stack** และ **CM55 สั่งผ่าน IPC**  
4. อ่านสถานะ peripheral ด้วย `cm55_ble_periph_status_get_sync` / `cm55_get_ble_periph_status`  
5. สั่ง **advertising** ด้วย `cm55_ble_periph_adv_ctrl_sync` (stop / start / restart)  
6. อธิบายเส้นทาง **scan** (CM55 ขอสแกน → CM33 รายงานผล) สำหรับโหมด observer  
7. ใช้โฮสต์แล็บ: **[TESAIoT_Hackathon `ble-flet/`](https://github.com/drsanti/TESAIoT_Hackathon)** หรือแอปสแกน GATT ทั่วไป  
8. ทำแบบฝึกบนบอร์ดจริงและเก็บหลักฐานลิงก์  

> **Snippet ในบทนี้** อ้างชื่อฟังก์ชันจาก TESA Firmware SDK — ใช้ร่วมกับโปรเจกต์ตัวอย่างหรือตัวอย่างบน Developer Hub  
> ดูโฮสต์เพิ่ม: **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** · [Hackathon BLE](https://github.com/drsanti/TESAIoT_Hackathon) · [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)

### Read alongside this chapter

| เอกสาร | ใช้เมื่อ |
|---|---|
| [Bluetooth LE overview (Bluetooth SIG)](https://www.bluetooth.com/learn-about-bluetooth/tech-overview/) | แนวคิด GAP / GATT |
| [Infineon Find Me CE (PSoC Edge)](https://github.com/Infineon/mtb-example-psoc-edge-btstack-findme) | ตัวอย่างผู้ผลิต (peripheral + mobile app) |
| **[TESAIoT_Hackathon — ble-flet](https://github.com/drsanti/TESAIoT_Hackathon)** | Desktop BLE dashboard (scan → connect → stream) |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | Host หลักมักใช้ USB/UART; เทียบกับ BLE lab |
| [M06 — MQTT](../../m06-mqtt/l01-mqtt-and-mqtts/README.md) | คู่เปรียบเทียบ cloud connectivity |
| [M04 — RTOS](../../m04-rtos/l01-freertos-programming/README.md) | task ที่รอสถานะ / เรียก IPC |

---

## 1. BLE in One Page

**Bluetooth Low Energy (BLE)** เป็นวิทยุระยะสั้นพลังงานต่ำ เหมาะกับโทรศัพท์ แท็บเล็ต และเดสก์ท็อปที่อยู่ใกล้บอร์ด — ไม่ต้องมี Wi‑Fi หรือ broker

| คำ | ความหมาย |
|---|---|
| **Peripheral** | อุปกรณ์ที่ *โฆษณา (advertise)* และรอให้โฮสต์เชื่อม (บอร์ด TESA มักเป็นบทบาทนี้) |
| **Central** | โฮสต์ที่ *สแกน* แล้วเชื่อม (phone / PC / `ble-flet`) |
| **GAP** | ชั้นค้นพบและเชื่อมต่อ (ชื่อ ADV, ที่อยู่, connection) |
| **GATT** | ชั้นบริการ/คุณลักษณะ (Service / Characteristic / Notify / Write) |
| **Advertising** | การประกาศตัวบนอากาศก่อนมี connection |
| **Notification** | Peripheral ส่งข้อมูลไป Central โดยไม่ต้องรอ poll ทุกครั้ง |

### BLE vs MQTT (หลัง M06)

| | BLE | MQTT |
|---|---|---|
| ระยะ | ใกล้ (ห้อง / โต๊ะ) | ผ่านเครือข่าย / คลาวด์ |
| สะพานกลาง | ไม่บังคับ broker | ต้องมี **broker** |
| พลังงาน / setup | ไม่ต้อง join Wi‑Fi | ต้อง Wi‑Fi (+ TLS ถ้า MQTTs) |
| โฮสต์แล็บ | `ble-flet`, nRF Connect, AIROC app | MQTTX, Studio broker, web-app |
| ใน Capstone (M08) | เส้นทาง local | เส้นทาง cloud |

> **Key phrase**  
> MQTT พาข้อมูลขึ้นเครือข่าย — BLE พาข้อมูลเข้ามือถือ/พีซีที่อยู่ใกล้

อ่านเสริม: [Bluetooth LE tech overview](https://www.bluetooth.com/learn-about-bluetooth/tech-overview/)

---

## 2. Where BLE Lives in TESA Firmware

บน Evaluation Kit วิทยุมักเป็น **AIROC™ Wi‑Fi & Bluetooth® combo** — สแต็ก BLE รันบน **CM33**; แอปเซ็นเซอร์บน **CM55** สั่งผ่าน IPC

| บทบาท | คอร์ | API ที่ผู้เรียนเรียกบ่อย |
|---|---|---|
| BLE stack + GATT peripheral | **CM33** | `ble_periph_*` (เจ้าของจริง) |
| สถานะ / สั่ง ADV จากแอป | **CM55** | `cm55_trigger_ble_periph_*`, `cm55_ble_periph_*_sync` |
| สแกน (observer) | **CM33** รันสแกน · **CM55** ขอและรับ event | `cm55_ble_request_scan_*`, `cm55_ble_ipc_set_event_handler` |
| BS2 over BLE (โฮสต์แล็บ) | CM33 bridge + host GATT client | โฮสต์: Hackathon `ble-flet` |

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
> Wi‑Fi (M06) และ BLE ใช้วิทยุชุดเดียวกันบนหลายคิต — อย่าคาดหวัง throughput สูงสุดทั้งสองพร้อมกันโดยไม่ทดสอบ coexistence ในห้องจริง

---

## 3. Peripheral Status (Diagnostic First)

ก่อน “เชื่อมกับมือถือ” ให้ยืนยันว่าโปรไฟล์ BLE บนเฟิร์มแวร์ทำงาน

โครงสร้างสถานะ (สรุปฟิลด์ที่สำคัญ):

```c
typedef struct {
  uint8_t profile_ble_active;
  uint8_t manager_inited;
  uint8_t stack_ready;
  uint8_t tx_notify_enabled;
  uint32_t last_error;
  uint16_t connection_id; /* 0 = ไม่มีลิงก์ */
} ipc_ble_periph_status_t;
```

### อ่านสถานะแบบ sync (แนะนำในแล็บ)

```c
#include "cm55_ipc_app.h"
#include "ipc_ble_periph_types.h"

ipc_ble_periph_status_t st;

if (cm55_ble_periph_status_get_sync(&st, 5000U)) {
    /* ตรวจ stack_ready, connection_id, tx_notify_enabled */
} else {
    /* timeout / IPC ไม่ตอบ — ตรวจว่า firmware เปิด BLE profile */
}
```

หรือยิงคำขอแบบไม่รอ แล้วอ่าน snapshot ทีหลัง:

```c
(void)cm55_trigger_ble_periph_status_get();
/* … รอ event / delay สั้น ๆ … */
(void)cm55_get_ble_periph_status(&st);
```

| ฟิลด์ | ความหมายโดยประมาณ |
|---|---|
| `profile_ble_active` | โปรไฟล์ BLE ของบิลด์เปิดอยู่ |
| `manager_inited` / `stack_ready` | สแต็กพร้อม |
| `tx_notify_enabled` | Central เปิด notify แล้ว (ลิงก์ใช้งานจริง) |
| `connection_id` | มี GATT connection เมื่อไม่ใช่ 0 |
| `last_error` | รหัสผิดพลาดล่าสุด (0 = ปกติ) |

---

## 4. Advertising Control

Advertising ทำให้ Central มองเห็นอุปกรณ์ — ชื่อในแล็บ TESA มักขึ้นต้นด้วย **`TESAIoT-`**

```c
uint8_t result = 0xFF;

/* action: 0 = stop, 1 = start, 2 = restart */
if (cm55_ble_periph_adv_ctrl_sync(1U, &result, 5000U)) {
    /* result 0 = ok ตาม bridge */
}
```

| `action` | ความหมาย |
|---|---|
| `0` | Stop advertising |
| `1` | Start advertising |
| `2` | Restart advertising (worker-safe) |

> **Key phrase จาก firmware**  
> ขณะมี connection อยู่ การ stop ADV จะไม่ตัดลิงก์ — และ start ADV อาจไม่จำเป็นเพราะเชื่อมอยู่แล้ว

ถ้าโฮสต์ไม่เห็นอุปกรณ์หลังบูตนาน: ตรวจ **ADV timeout** / reboot บอร์ด (Hackathon `ble-flet` README อธิบายอาการนี้)

---

## 5. Scan Path (Optional Observer Lab)

เมื่อบทบาทเป็น **สแกนหาอุปกรณ์อื่น** (ไม่ใช่แค่เป็น peripheral):

```c
#include "cm55_ipc_app.h"

static void on_ble_ipc(const ipc_msg_t *msg, void *user)
{
    (void)user;
    /* แยกประเภท event ตาม cmd ของ IPC_EVT_BLE_* */
}

void ble_scan_lab_start(void)
{
    cm55_ble_ipc_set_event_handler(on_ble_ipc, NULL);
    cm55_ble_request_scan_all();          /* หรือ scan_name / scan_addr */
    /* หยุดด้วยคำสั่ง scan stop ตามตัวอย่าง SDK เมื่อครบเวลา */
}
```

ตัวช่วยที่พบบ่อย:

| API | ใช้เมื่อ |
|---|---|
| `cm55_ble_request_scan_all` | สแกนเต็ม ไม่กรอง |
| `cm55_ble_request_scan_name` | กรองตามชื่อย่อย |
| `cm55_ble_request_scan_addr` | กรองตามที่อยู่ 6 ไบต์ |
| `cm55_ble_ipc_set_event_handler` | รับผลสแกน/สถานะใน task |

ตัวอย่างในเฟิร์มแวร์ชุดนี้มักชื่อแนว **`example_ble`** (สลับสแกนเปิด/ปิดเป็นคาบ) — เปิดดูใน Developer Hub / โปรเจกต์ตัวอย่างของเฟิร์มแวร์

---

## 6. Host Tools for the Lab

### 6.1 Recommended: Hackathon `ble-flet`

แพ็ก [`TESAIoT_Hackathon`](https://github.com/drsanti/TESAIoT_Hackathon) มีแอปเดสก์ท็อป **Python + Flet + bleak**:

1. Flash HEX ที่เปิด **BLE module profile**  
2. รัน `ble-flet` ตาม README ใน repo  
3. แอปจะ hunt ชื่อ **`TESAIoT-*`** → connect → สตรีม  

เหมาะกับแล็บที่ต้องการ **หลักฐาน live** โดยไม่พึ่ง Web Bluetooth ในเบราว์เซอร์

### 6.2 Generic GATT explorers

- nRF Connect / LightBlue / AIROC™ Bluetooth® Connect (ตามตัวอย่าง Infineon Find Me)  
- ใช้ยืนยันว่าอุปกรณ์ advertise และเชื่อมได้ แม้ยังไม่ decode BS2

### 6.3 Bitstream Studio

[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) เป็นโฮสต์หลักของหลักสูตรสำหรับ USB/UART และ MQTT — ใน M07 ใช้เป็น *คู่เทียบ* ว่าเมื่อไรเลือก BLE local แทนสายหรือ broker

### GATT identity (แล็บ BS2 BLE)

โฮสต์แล็บอ้างอิง service/characteristic ตระกูล BS2 (UUID คงที่ใน `ble-flet`) และชื่อ ADV ขึ้นต้น `TESAIoT-` — **อย่า hardcode UUID ในเอกสารผลงานถ้าไม่จำเป็น**; ระบุว่าใช้แพ็ก Hackathon เวอร์ชันใด

---

## 7. Security and Lab Hygiene

| หัวข้อ | แนวปฏิบัติ |
|---|---|
| Pairing / bonding | แล็บมักใช้ลิงก์สั้น ๆ — อย่าสมมติว่าเป็น production secure pairing |
| ข้อมูลบนอากาศ | BLE ไม่ผ่าน broker แต่ยังอยู่ในช่วงวิทยุของห้องที่ทำแล็บ |
| Secret | ไม่มีรหัส Wi‑Fi ใน path นี้ — แต่ยังห้ามฝัง credential อื่นในไฟล์สาธารณะ |
| Central เดียว | อย่าเปิด nRF Connect และ `ble-flet` พร้อมกันบนเครื่องเดียวไปที่บอร์ดเดียวกัน |

---

## 8. Design Patterns for Capstone (Preview M08)

เลือกอย่างน้อยหนึ่งเส้นทาง connectivity ใน Capstone:

```text
Sensor task ──► window/filter ──► LED/UART
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
   MQTT publish (M06)      BLE notify / host (M07)
   MQTT subscribe cmd      BLE write / command
```

เกณฑ์ขั้นต่ำของ M08: **MQTT หรือ BLE** — ใช้ทั้งสองได้เป็นโบนัส

---

## 9. Common Pitfalls

| อาการ | สาเหตุที่พบบ่อย |
|---|---|
| สแกนไม่เจอ | BLE profile ปิด · ยังไม่ ADV · ADV timeout · อยู่ไกล/มีคลื่นรบกวน |
| Status sync timeout | CM33 ยังไม่พร้อม · IPC ไม่ขึ้น · บิลด์ไม่มี BLE |
| Connect แล้วหลุด | Central อีกตัวแย่ง · reboot บอร์ด · timeout นโยบายเฟิร์มแวร์ |
| Wi‑Fi + BLE พร้อมกันแปลก ๆ | Combo radio coexistence — ทดสอบแยกก่อนรวม |
| สับสนกับ MQTT | คนละชั้นขนส่ง — อย่าหา broker ในแล็บ BLE |

---

## Next Steps

1. ทำแล็บ: [แล็บ](../l02-lab/README.md)  
2. เก็บแผ่นสูตร: [ble-connectivity.md](resources/ble-connectivity.md)  
3. เมื่อพร้อม ไปต่อ **M08 — Capstone** ([บทเรียน M08](../../m08-capstone/l01-capstone-and-resources/README.md))

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

## เช็กความเข้าใจ

คำถามสั้นสามข้อใน [quiz.yaml](quiz.yaml) ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อน แล้วค่อยเทียบกับเฉลยและคำอธิบายในไฟล์

## แล็บ

ลงมือต่อที่ [แล็บ: การเชื่อมต่อ BLE](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/ble-connectivity.md) · [← Table of Contents](../../README.md) · [← M06](../../m06-mqtt/l01-mqtt-and-mqtts/README.md) · [M08 →](../../m08-capstone/l01-capstone-and-resources/README.md)
