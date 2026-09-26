---
id: fw-sdk.m08.l01
lang: th
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
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M08/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M08 — Capstone Project and Course Resources

**Course 1 · Module 8**  
**Suggested time:** ยืดหยุ่น — แนะนำ 2–4 ชั่วโมง + ทำ Capstone ต่อเองได้  
**Format:** รวมทักษะ M01–M07 เป็นมินิโปรเจกต์ + ใช้แผนที่เอกสาร / พอร์ทัลออนไลน์

[Lab](../l02-lab/README.md) · [Capstone brief](resources/capstone-brief.md) · [Course package map](resources/course-package.md) · [← Table of Contents](../../README.md) · [← M07](../../m07-ble/l01-ble-connectivity/README.md)

> **หมายเหตุ: โค้ดในบทนี้เขียนสำหรับเฟิร์มแวร์ชุดใด** (ตรวจสอบเมื่อ 26 ก.ย. 2026)
>
> โค้ด C ในบทนี้เรียก API ของเฟิร์มแวร์ **TESAIoT Bitstream** ที่ต้นฉบับเรียกว่า “TESA Firmware SDK” ซึ่งเผยแพร่เป็นไฟล์ HEX สำเร็จรูป (`tesaiot-bitstream-<version>.hex`) คู่กับ Bitstream Studio ในแพ็กแล็บ [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/tree/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/hex) **ซอร์สโค้ดของเฟิร์มแวร์ชุดนี้ยังไม่เปิดเผยต่อสาธารณะ** ฟังก์ชันอย่าง `cm55_*`, `sensor_*`, `led_controller_*`, `cm33_mqtt_*`, `cm55_ble_*` จึงยังไม่มี header ให้เปิดดูหรือนำไป build เอง ให้อ่าน snippet เป็นแนวคิดและลำดับการเรียกใช้ ส่วนการเรียก FreeRTOS และ Infineon PDL (เช่น `xTaskCreate`, `vTaskDelay`, `Cy_GPIO_*`) เป็น API สาธารณะตามปกติ
>
> Capstone ใช้ API จากโมดูล 3–7 ทั้งหมด ดูตัวเทียบที่ตรวจแล้วใน SDK เปิดได้ในหมายเหตุของแต่ละบทเรียน และในตารางสรุปที่[หน้าหลักสูตร](../../README.md)

> **โฮสต์ `ble-flet` ยังไม่เผยแพร่** — [README ของ TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/blob/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/README.md) (commit `f5f09a6`) ระบุว่า `python-app/`, `ble-react/` และ `ble-flet/` เป็นของผู้ดูแลและไม่อยู่ใน repo สาธารณะ ให้ใช้เส้นทางสำรองที่บทเรียนเสนอไว้แล้ว คือ GATT explorer ทั่วไป เช่น nRF Connect, LightBlue หรือ AIROC™ Bluetooth® Connect

---

## เป้าหมาย (Learning Outcomes)

เมื่อเรียนจบ คุณควรทำได้ดังนี้:

1. ใช้ **ชุดแบบฝึก M01–M07** เป็นฐาน แล้วรวมเป็นระบบที่สาธิตได้  
2. ส่งมอบงานตาม **เกณฑ์ผ่าน** ของ Capstone (build/flash, RTOS, sensor, MQTT หรือ BLE)  
3. ใช้ **แผนที่เอกสาร / API** ของหลักสูตรเพื่อหาฟังก์ชันและตัวอย่างต่อเอง  
4. ส่งมอบ **โปรเจกต์ Capstone** พร้อม README ที่ผู้อื่นทำซ้ำได้  
5. ใช้แหล่งเรียนรู้ **ออนไลน์** (Developer Hub, Marketplace, Hackathon) ประกอบการสาธิต  

> แบบฝึกของแต่ละโมดูลเป็นส่วนหนึ่งของชุดฝึกทั้งหลักสูตร — M08 คือชั้น **รวมและส่งมอบ**

### Read alongside this chapter

| เอกสาร | ใช้เมื่อ |
|---|---|
| [Table of Contents](../../README.md) | ดัชนีทั้งคอร์ส |
| [Course package map](resources/course-package.md) | แผนที่โมดูล + พอร์ทัลออนไลน์ + ดัชนี API |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | ตัวอย่างโค้ด + API Reference |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | Host / Digital Twin / broker tools |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | HEX, Flasher, VSIX, `web-app/`, `ble-flet/` |
| [M05](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) · [M06](../../m06-mqtt/l01-mqtt-and-mqtts/README.md) · [M07](../../m07-ble/l01-ble-connectivity/README.md) | Sensor + MQTT + BLE สำหรับ Capstone |

---

## 1. Full Hands-on Lab Index (Course 1)

| Module | Lab | สิ่งที่ได้เมื่อผ่าน |
|---|---|---|
| [M01](../../m01-mcu-architecture/l02-lab/README.md) | แผนที่โดเมน ↔ ชั้น SDK | เลือกโดเมน/ชั้นได้ก่อนเขียนโค้ด |
| [M02](../../m02-toolchain/l02-lab/README.md) | Create / Build / Flash / Debug | โปรเจกต์รันบนบอร์ด |
| [M03](../../m03-gpio-peripherals/l02-lab/README.md) | GPIO + UART + peripheral | Driver API จริงบนฮาร์ดแวร์ |
| [M04](../../m04-rtos/l02-lab/README.md) | Multi-task + queue / mutex | FreeRTOS พื้นฐาน |
| [M05](../../m05-sensor-data/l02-lab/README.md) | Sensor + filter + window | ข้อมูลพร้อม AI / twin |
| [M06](../../m06-mqtt/l02-lab/README.md) | Wi‑Fi + MQTT pub/sub | เชื่อม cloud / broker |
| [M07](../../m07-ble/l02-lab/README.md) | BLE peripheral / scan + host | เชื่อม local / phone / desktop |
| **[M08](../l02-lab/README.md)** | **Capstone mini-project** | ระบบรวมที่สาธิตและทำซ้ำได้ |

> **Key phrase**  
> Capstone คือการ *เลือกและเชื่อม* ชิ้นส่วนที่มีแล้ว — ไม่ใช่เขียนทุกอย่างใหม่จากศูนย์

---

## 2. Capstone Plan and Pass Criteria

ใช้ส่วนนี้วางแผนงานและตรวจก่อนส่ง

### 2.1 Suggested pacing (for you)

| ช่วง | โฟกัส |
|---|---|
| ก่อนเริ่ม Capstone | ตรวจว่า lab หลัก M02–M07 ผ่านเกณฑ์ขั้นต่ำแล้ว |
| ชม. 1 | เขียนสถาปัตยกรรม task + เลือกเซ็นเซอร์ / connectivity |
| ชม. 2–3 | รวมโค้ดบนบอร์ด + ทดสอบ MQTT และ/หรือ BLE |
| ชม. 4 / ทำต่อเอง | README, หลักฐานสาธิต, เก็บงาน |

### 2.2 Your setup checklist

- [ ] บอร์ด + สาย USB + Wi‑Fi ที่ใช้ได้  
- [ ] Broker ที่กำหนด (LAN / Studio / สาธารณะตามนโยบาย) — ถ้าใช้ MQTT  
- [ ] โทรศัพท์หรือ PC ที่สแกน BLE ได้ — ถ้าใช้ BLE  
- [ ] [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) หรือ VSIX จาก [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)  
- [ ] HEX / Flasher จาก Hackathon เมื่อเลือกใช้แพ็กสำเร็จรูป  
- [ ] **อย่า** commit รหัสผ่าน Wi‑Fi / broker ในไฟล์ที่ส่งสาธารณะ  

### 2.3 Minimum pass criteria

| เกณฑ์ | ต้องมี |
|---|---|
| Build + flash ได้ตาม README ของคุณ | ใช่ |
| ≥ 2 FreeRTOS tasks | ใช่ |
| Sensor path + LED/UART indication | ใช่ |
| **Connectivity** — MQTT **หรือ** BLE (อย่างน้อยหนึ่งเส้น) พร้อมรับคำสั่งหรือยืนยันลิงก์ | ใช่ |
| ไม่ฝัง secret ในไฟล์ส่งสาธารณะ | ใช่ |

งานต่อยอด (ไม่บังคับ): ใช้ทั้ง MQTT และ BLE, threshold alert, mutex บนบัสร่วม, คิว/topic พร้อมต่อ Digital Twin, คุณภาพสาธิต

รายละเอียดเต็มใน [แล็บ](../l02-lab/README.md) และ [capstone-brief.md](resources/capstone-brief.md)

---

## 3. Developer Guide and API Reference Map

### 3.1 Where to look first

| ความต้องการ | ไปที่ |
|---|---|
| เรียกดูตัวอย่างออนไลน์ | [TESAIoT Developer Hub](https://dev.tesaiot.dev/) — Example Explorer + API Reference |
| ชื่อฟังก์ชัน peripheral | [M03 cheatsheet](../../m03-gpio-peripherals/l01-gpio-and-peripherals/resources/peripheral-api-map.md) |
| FreeRTOS patterns | [M04 cheatsheet](../../m04-rtos/l01-freertos-programming/resources/rtos-patterns.md) |
| Sensors / windows / fusion | [M05 cheatsheet](../../m05-sensor-data/l01-sensor-data-for-edge-ai/resources/sensor-ai-prep.md) |
| MQTT / Wi‑Fi triggers | [M06 cheatsheet](../../m06-mqtt/l01-mqtt-and-mqtts/resources/mqtt-cloud.md) |
| BLE peripheral / scan | [M07 cheatsheet](../../m07-ble/l01-ble-connectivity/resources/ble-connectivity.md) |
| สถาปัตยกรรมชิป / ชั้น SDK | [M01](../../m01-mcu-architecture/l01-architecture-and-sdk-layers/README.md) |
| Toolchain | [M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md) |

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

ตัวอย่างหน่วงใน task (จาก M04/M05):

```c
TickType_t last = xTaskGetTickCount();
for (;;) {
    /* read → filter → maybe publish */
    vTaskDelayUntil(&last, pdMS_TO_TICKS(200));
}
```

ตัวอย่างสั่ง MQTT หลัง Wi‑Fi พร้อม (จาก M06):

```c
(void)cm55_trigger_mqtt_connect();
/* wait until cm55_get_mqtt_status reports CONNECTED */
```

ตัวอย่างอ่านสถานะ BLE peripheral (จาก M07):

```c
ipc_ble_periph_status_t ble;
if (cm55_ble_periph_status_get_sync(&ble, 5000U)) {
    /* stack_ready / connection_id / tx_notify_enabled */
}
```

แผ่นรวม: [course-package.md](resources/course-package.md)

---

## 4. Project Examples and Source Patterns

| แหล่งตัวอย่าง | บทบาทใน M08 |
|---|---|
| โปรเจกต์ที่ผู้เรียนสร้างใน M02–M07 | ฐานโค้ด Capstone |
| [Developer Hub](https://dev.tesaiot.dev/) | ดึงตัวอย่าง GPIO / Sensors / System / Integrations |
| [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) | HEX สำเร็จรูป, `web-app/`, `ble-flet/` สำหรับหลักฐาน live |
| Infineon CE (เสริม) | เทียบแนวทางผู้ผลิต — ไม่แทน TESA Driver API |

### 4.1 Recommended Capstone theme

**Environmental / Activity monitor (ขนาดเล็ก)**

ต้องมีอย่างน้อย:

1. **Sensor path** — อ่านเป็นคาบ + filter หรือ window (M05)  
2. **Local indication** — LED และ/หรือ UART (M03)  
3. **RTOS** — ≥ 2 tasks + คิวหรือ mutex เมื่อจำเป็น (M04)  
4. **Connectivity** — อย่างน้อยหนึ่งเส้น:  
   - **MQTT** publish + subscribe คำสั่ง (M06), **หรือ**  
   - **BLE** peripheral ที่โฮสต์เชื่อมได้ + ยืนยันลิงก์/คำสั่ง (M07)  

ทางเลือกเสริม:

- ใช้ทั้ง MQTT และ BLE  
- Event/alert เมื่อเกินเกณฑ์  
- โครงสร้าง `to_twin` (คิวหรือ topic แยก) สำหรับต่อ Digital Twin  
- สาธิตบน Bitstream Studio, Hackathon dashboard หรือ `ble-flet/`  

---

## 5. Course Resources Map

| ชิ้น | ที่อยู่ |
|---|---|
| Table of Contents | [หน้าหลักสูตร](../../README.md) |
| Lessons M01–M08 | `mNN-<slug>/l01-<slug>/README.md` |
| Labs | `mNN-<slug>/l02-lab/README.md` |
| Cheatsheets / worksheets | `mNN-<slug>/l01-<slug>/resources/*` |
| แผนที่รวม | [course-package.md](resources/course-package.md) |

### External portals

| Portal | URL |
|---|---|
| Code examples / API | https://dev.tesaiot.dev/ |
| VS Code host / twin | https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio |
| Lab pack HEX/VSIX/web/BLE | https://github.com/drsanti/TESAIoT_Hackathon |

---

## 6. Course 1 Wrap-Up and Next Path

หลังจบ Course 1 คุณควรอธิบายได้ว่า:

1. TESA Firmware SDK วางชั้น HAL/Driver/Utility/Application อย่างไร  
2. ModusToolbox™ + VS Code ใช้สร้าง ไล่บั๊ก และ flash อย่างไร  
3. GPIO / peripherals, FreeRTOS, sensor prep, MQTT และ BLE ต่อกันเป็นผลิตภัณฑ์ Edge อย่างไร  
4. โฮสต์ (Bitstream Studio / Hackathon BLE) และแพ็กแล็บช่วยทดสอบอย่างไร  

**เส้นทางต่อไป (นอก Course 1):** หลักสูตร Digital Twin / Product Design — ใช้สตรีมและโครงสร้างที่เตรียมใน Capstone เป็นอินพุต

### Next Steps

1. ทำ Capstone: [Lab](../l02-lab/README.md)  
2. กรอก [capstone-brief.md](resources/capstone-brief.md)  
3. เก็บแผนที่เอกสาร: [course-package.md](resources/course-package.md)  
4. กลับไปทบทวนโมดูลที่ยังไม่แน่นผ่าน [TOC](../../README.md)  

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

## เช็กความเข้าใจ

คำถามสั้นสามข้อใน [quiz.yaml](quiz.yaml) ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อน แล้วค่อยเทียบกับเฉลยและคำอธิบายในไฟล์

## แล็บ

ลงมือต่อที่ [แล็บ Capstone: มินิโปรเจกต์](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Capstone brief](resources/capstone-brief.md) · [Course package map](resources/course-package.md) · [← Table of Contents](../../README.md)

## ตัวอย่างบน TESAIoT Developer Hub

ลองของจริงบน TESAIoT Dev Kit: เปิดตัวอย่างบน Developer Hub เพื่ออ่านโค้ด ดาวน์โหลด หรือ flash เฟิร์มแวร์สำเร็จรูป

- [EP07 — SensorHub Final](https://dev.tesaiot.dev/?example=developer-hub--int_ep07_sensorhub_final&q=int_ep07_sensorhub_final) — โปรเจกต์ปิดคอร์ส: แดชบอร์ดรวมเซนเซอร์ทั้ง 4 ตัว (DPS368, SHT4x, BMI270, BMM350) + ไมโครโฟน PDM สเตอริโอ บนจอเดียว
- [EP07 — Final WiFi Manager](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep07_final_wifi_manager&q=hmi_ep07_final_wifi_manager) — รวม scan + profile + connect + auto-retry + ping watchdog เป็น WiFi manager สมบูรณ์ พร้อม state machine บนหน้าจอและ auto-connect จาก profile
