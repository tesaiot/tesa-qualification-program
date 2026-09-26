# TESA Firmware SDK สำหรับ Edge AI

หลักสูตรเชิงปฏิบัติการเฟิร์มแวร์ภาษา C บน PSOC™ Edge E84 ตั้งแต่สถาปัตยกรรมชิปและชั้น SDK เครื่องมือ ModusToolbox™ + VS Code อุปกรณ์ต่อพ่วง FreeRTOS การเตรียมข้อมูลเซ็นเซอร์สำหรับ Edge AI ไปจนถึง MQTT, BLE และ Capstone

> เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA) · นำเข้าจาก [drsanti/TESAIoT-Courses — C1](https://github.com/drsanti/TESAIoT-Courses/tree/287c21814ba8c75f693136616dcd270349a15966/C1) (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

| | |
|---|---|
| ระดับ | L3 · ทำได้เอง |
| สถานะ | alpha (เนื้อหานำเข้าแล้ว กำลังทบทวน) |
| เวลาโดยประมาณ | ~26 ชั่วโมง (รวมเวลาของโมดูลตามต้นฉบับ) |
| ฮาร์ดแวร์ | TESAIoT PSoC Edge DevKit หรือ KIT_PSE84_EVAL (โมดูล 1 ไม่ต้องใช้บอร์ด) |
| เหมาะกับ | นักพัฒนา · นักศึกษา · ผู้สอน |
| ภาษา | ไทย คำศัพท์เทคนิคเป็นภาษาอังกฤษ หัวข้อในบทเรียนเป็นภาษาอังกฤษตามต้นฉบับ · ฉบับภาษาอังกฤษของบทเรียนยังรอแปล |

## หลักสูตรนี้สำหรับใคร

นักพัฒนาและนักศึกษาที่อ่านเขียนภาษา C ได้แล้ว และอยากพัฒนาอุปกรณ์ Edge AI บน PSOC™ Edge E84 ให้ครบตั้งแต่ชิปถึงคลาวด์ รวมถึงผู้สอนที่ต้องการชุดแล็บพร้อมใช้

## ก่อนเรียน

- เขียนภาษา C ระดับพื้นฐานได้ (ฟังก์ชัน pointer struct และ callback ปรากฏในโค้ดตัวอย่างทุกบท)
- ใช้คอมพิวเตอร์ติดตั้งโปรแกรมและใช้เทอร์มินัลเบื้องต้นได้

## สิ่งที่ต้องมี

- **บอร์ด**: TESAIoT PSoC Edge DevKit หรือ Infineon [KIT_PSE84_EVAL](https://www.infineon.com/evaluation-board/KIT-pse84-eval) พร้อมสาย USB (โมดูล 1 ยังไม่ต้องใช้บอร์ด)
- **ModusToolbox™ 3.6 ขึ้นไป** ตามบทเรียนโมดูล 2 พร้อม Arm GNU Toolchain ที่มากับชุดติดตั้ง ถ้าจะ build จากซอร์สเปิดของ [tesaiot-pse84-devkit-sdk](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/README.md) ให้ใช้ 3.6 เท่านั้นตามที่ README ของ SDK ระบุ
- **Visual Studio Code** กับส่วนขยายของ ModusToolbox™
- **เฟิร์มแวร์ HEX** `tesaiot-bitstream-<version>.hex` และ **TESAIoT Flasher** จาก [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/tree/f5f09a6e89a42a800dd39bae362c1c3f2328cc72) (ณ commit `f5f09a6` รายการ `latest` ใน firmware manifest คือ 0.2.1)
- **Bitstream Studio** ([VS Marketplace](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) เวอร์ชัน 0.2.2 เมื่อ 26 ก.ย. 2026) หรือ VSIX ที่คู่กับ HEX
- เครื่องมือโฮสต์: serial terminal, MQTTX หรือ `mosquitto_sub`, และ GATT explorer (nRF Connect / LightBlue / AIROC™ Bluetooth® Connect)
- เครือข่าย Wi-Fi และ broker MQTT ของคุณเอง (broker ใน Bitstream Studio หรือ broker สาธารณะสำหรับทดสอบ) — อย่า commit รหัสผ่านลง Git

รุ่นและเวอร์ชันทั้งหมดบันทึกไว้ในช่อง `toolchain` ของ [course.yaml](course.yaml)

## หมายเหตุสำคัญเรื่องเฟิร์มแวร์และโค้ดตัวอย่าง

โค้ด C ในโมดูล 3–8 เขียนสำหรับเฟิร์มแวร์ **TESAIoT Bitstream** (ต้นฉบับเรียกว่า “TESA Firmware SDK”) ซึ่งเผยแพร่เป็นไฟล์ HEX สำเร็จรูปคู่กับ Bitstream Studio ใน [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/tree/f5f09a6e89a42a800dd39bae362c1c3f2328cc72) **ซอร์สโค้ดและ header ของเฟิร์มแวร์ชุดนี้ยังไม่เปิดเผยต่อสาธารณะ** จากการตรวจสอบเมื่อ 26 ก.ย. 2026 ไม่พบชื่อฟังก์ชันอย่าง `cm55_trigger_mqtt_connect`, `cm55_get_mqtt_status` หรือ `cm55_ble_periph_*` ทั้งใน SDK สาธารณะ ใน repo TESAIoT_Hackathon (มีแต่ไฟล์ HEX, VSIX, ตัวติดตั้ง และ web-app) และในการค้นของ [TESAIoT Developer Hub](https://dev.tesaiot.dev/) จึงให้อ่าน snippet เป็นแนวคิดและลำดับการเรียกใช้ แล้วลงมือจริงด้วยไฟล์ HEX ตามแล็บ

SDK โอเพนซอร์สที่ใช้ได้วันนี้คือ [tesaiot-pse84-devkit-sdk](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) (Apache-2.0) ซึ่งเป็น**คนละโค้ดเบส**และตั้งชื่อ API ต่างกัน ตารางนี้จับคู่เฉพาะส่วนที่ตรวจแล้วว่าทำงานเรื่องเดียวกัน:

| กลุ่ม API ในบทเรียน | ซอร์ส | ตัวเทียบที่ตรวจแล้วใน SDK เปิด (commit `ef72c1b`) |
|---|---|---|
| `led_controller_*`, `cm55_button_*` (โมดูล 3–4) | ยังไม่เปิด | [`io/04_gpio_led_button.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c) ใช้ PDL `Cy_GPIO_*` |
| `cm55_adc_*` (โมดูล 3) | ยังไม่เปิด | [`io/03_read_potentiometers.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/03_read_potentiometers.c) · [`cm55 io/02_pots_and_capsense.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/io/02_pots_and_capsense.c) |
| `sensor_sht40_*`, `sensor_bmi270_*`, `sensor_dps368_*`, `sensor_bmm350_*`, `cm55_i2c_manager_i2c_lock` (โมดูล 3–5) | ยังไม่เปิด | [`sensors/`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/tree/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors) 01–05 (`sht40_*`, `bmi270_*`, `bmm350_*`, `dps368_*`, `sensor_i2c_lock`) |
| `cm55_initialize`, `cm55_start_scheduler` (โมดูล 4) | ยังไม่เปิด | [`proj_cm55/main.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/main.c#L225-L238) เรียก `vTaskStartScheduler()` เองจาก `main` |
| `bitstream_led_pwm_*`, `cm55_uart_send` (โมดูล 3) | ยังไม่เปิด | ยังไม่พบ |
| `cm55_imu_fusion_bridge_*`, `bitstream_bs_cfg_*` (โมดูล 5) | ยังไม่เปิด | ยังไม่พบ |
| `cm55_trigger_connect`, `cm55_get_wifi_status`, `example_wifi_*` (โมดูล 6) | ยังไม่เปิด | [`connectivity/10_wifi_join.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/10_wifi_join.c) (`app_wifi_*`, `cy_wcm_*`) · [`cm55 connectivity/01_wifi_join_and_remember.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/connectivity/01_wifi_join_and_remember.c) (`wifi_manager_*`) |
| `cm55_trigger_mqtt_*`, `cm55_get_mqtt_status`, `cm33_mqtt_*`, `bs_mqtt_telem_encode_json_*` (โมดูล 6) | ยังไม่เปิด | [`modules/tesaiot_mqtt/`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/tree/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_mqtt) (`tesaiot_mqtt_connect`, `_publish`, `_is_connected`, `_disconnect`) |
| `cm55_ble_periph_*`, `cm55_trigger_ble_periph_*` (โมดูล 7) | ยังไม่เปิด | [`ble/01_nus_bring_up_and_talk.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/ble/01_nus_bring_up_and_talk.c) (`ble_nus_*`) ซึ่ง SDK ระบุเองว่ายัง link บน template ที่ส่งมอบไม่ได้ |
| `cm55_ble_request_scan_*` (โมดูล 7) | ยังไม่เปิด | ยังไม่พบ (`ble_nus` เป็นบทบาท peripheral อย่างเดียว) |
| FreeRTOS (`xTaskCreate`, `xQueue*`, `xSemaphore*`, event groups) และ Infineon PDL (`Cy_GPIO_*`, `Cy_SCB_SPI_*`) | สาธารณะ | ใช้ได้ตามเอกสารของ FreeRTOS และ Infineon |
| โฮสต์ `ble-flet` (โมดูล 7–8) | ไม่เผยแพร่ | [README ของ TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/blob/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/README.md) ระบุว่าเป็นของผู้ดูแล ใช้ GATT explorer ทั่วไปแทน |

## ผลลัพธ์การเรียนรู้

เมื่อจบหลักสูตร คุณจะ:

1. จับคู่งาน Edge AI กับโดเมนฮาร์ดแวร์ของ PSOC™ Edge E84 และกับชั้นซอฟต์แวร์ HAL/BSP · Driver API · Utility · Application ได้
2. สร้าง build flash และ debug โปรเจกต์เฟิร์มแวร์ด้วย ModusToolbox™ และ VS Code บนบอร์ดจริง
3. ควบคุม GPIO, UART, I²C, PWM และ ADC ผ่าน Driver API และแบ่งงานเป็นหลาย task ด้วย FreeRTOS (queue, mutex, event group)
4. อ่านเซ็นเซอร์ด้วยคาบเวลาคงที่ กรอง normalize และจัดหน้าต่างข้อมูลเพื่อเตรียมเข้า Edge AI
5. เชื่อมอุปกรณ์กับ broker ด้วย MQTT/MQTTs และกับโฮสต์ใกล้ตัวด้วย BLE พร้อมเก็บหลักฐานการทำงาน
6. ส่งมอบมินิโปรเจกต์ที่รวม sensor, RTOS และ connectivity พร้อม README ที่ผู้อื่นทำซ้ำได้

## โมดูล

| # | โมดูล | บทเรียน | แล็บ | เวลาตามต้นฉบับ |
|---|---|---|---|---|
| 1 | [สถาปัตยกรรม MCU และโครงสร้าง Firmware SDK](m01-mcu-architecture/README.md) | [สถาปัตยกรรม MCU หลายโดเมนและชั้นของ Firmware SDK](m01-mcu-architecture/l01-architecture-and-sdk-layers/README.md) | [แล็บ](m01-mcu-architecture/l02-lab/README.md) | ประมาณ 2.5–3 ชั่วโมง (บทเรียน) + แล็บ 30–45 นาที |
| 2 | [ModusToolbox™ และ VS Code สำหรับพัฒนาเฟิร์มแวร์](m02-toolchain/README.md) | [ModusToolbox™ และ VS Code: สร้าง build flash debug](m02-toolchain/l01-modustoolbox-and-vscode/README.md) | [แล็บ](m02-toolchain/l02-lab/README.md) | ประมาณ 2.5–3 ชั่วโมง (บทเรียน) + แล็บ 90–120 นาที |
| 3 | [GPIO และอุปกรณ์ต่อพ่วงพื้นฐาน](m03-gpio-peripherals/README.md) | [GPIO และอุปกรณ์ต่อพ่วงผ่าน Driver API](m03-gpio-peripherals/l01-gpio-and-peripherals/README.md) | [แล็บ](m03-gpio-peripherals/l02-lab/README.md) | ประมาณ 3 ชั่วโมง (บทเรียน) + แล็บ 2.5–3 ชั่วโมง |
| 4 | [การเขียนเฟิร์มแวร์แบบ RTOS](m04-rtos/README.md) | [เฟิร์มแวร์หลาย task ด้วย FreeRTOS](m04-rtos/l01-freertos-programming/README.md) | [แล็บ](m04-rtos/l02-lab/README.md) | ประมาณ 3.5–4 ชั่วโมง (บทเรียน) + แล็บ 2.5–3.5 ชั่วโมง |
| 5 | [ข้อมูลเซ็นเซอร์และการเตรียมข้อมูลสำหรับ Edge AI](m05-sensor-data/README.md) | [สตรีมเซ็นเซอร์ที่พร้อมสำหรับ Edge AI](m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) | [แล็บ](m05-sensor-data/l02-lab/README.md) | ประมาณ 3.5–4 ชั่วโมง (บทเรียน) + แล็บ 2.5–3.5 ชั่วโมง |
| 6 | [MQTT และ MQTTs สำหรับสื่อสารกับคลาวด์](m06-mqtt/README.md) | [MQTT และ MQTTs บนอุปกรณ์ Edge](m06-mqtt/l01-mqtt-and-mqtts/README.md) | [แล็บ](m06-mqtt/l02-lab/README.md) | ประมาณ 3.5–4 ชั่วโมง (บทเรียน) + แล็บ 2.5–3.5 ชั่วโมง |
| 7 | [การเชื่อมต่อ Bluetooth Low Energy (BLE)](m07-ble/README.md) | [BLE สำหรับผลิตภัณฑ์ Edge](m07-ble/l01-ble-connectivity/README.md) | [แล็บ](m07-ble/l02-lab/README.md) | ประมาณ 3–3.5 ชั่วโมง (บทเรียน) + แล็บ ~2–2.5 ชั่วโมง |
| 8 | [Capstone และแหล่งเรียนรู้ของหลักสูตร](m08-capstone/README.md) | [วางแผน Capstone และใช้แผนที่เอกสาร](m08-capstone/l01-capstone-and-resources/README.md) | [แล็บ](m08-capstone/l02-lab/README.md) | ยืดหยุ่น — บทเรียน 2–4 ชั่วโมง + ทำ Capstone ต่อเองได้ |

## วิธีเรียน

1. อ่านบทเรียนที่ 1 ของแต่ละโมดูล แล้วทำแล็บ (บทเรียนที่ 2) ของโมดูลนั้น
2. ใช้ชีตในโฟลเดอร์ `resources/` เป็นแผ่นสรุปตอนลงมือบนบอร์ด
3. เปิดตาราง **Read alongside this chapter** ในแต่ละบทเพื่อไปยังเอกสารออนไลน์ที่เกี่ยวข้อง
4. ตอบ `quiz.yaml` ท้ายบทเรียนเพื่อเช็กความเข้าใจก่อนเข้าแล็บ

ต้นฉบับเขียนขึ้นเพื่อการอบรมแบบมีผู้สอน ถ้อยคำในบทเรียนปรับให้เรียนด้วยตัวเองได้แล้ว แต่ค่าที่ขึ้นกับเครื่องของคุณ (Wi-Fi, broker, พอร์ต COM, เวอร์ชัน HEX) ยังต้องตั้งเอง ให้เริ่มจากค่าที่บทเรียนให้ไว้ (เช่น baud 921600 หรือ broker ใน Bitstream Studio) แล้วดูเอกสารของเครื่องมือประกอบ ในเนื้อหาจะเห็นคำว่า **Course 1 / Course 2 / Course 3** และรหัส **M01–M08** ตามต้นฉบับ: Course 1 คือหลักสูตร TESA Firmware SDK สำหรับ Edge AI, Course 2 คือหลักสูตร Digital Twin และ Course 3 คือหลักสูตรการออกแบบผลิตภัณฑ์ ส่วน M0N คือโมดูลที่ N

## ลำดับที่แนะนำระหว่างสามหลักสูตร

ต้นฉบับแนะนำให้เรียนตามลำดับนี้:

```text
หลักสูตร 1  TESA Firmware SDK สำหรับ Edge AI        เฟิร์มแวร์บนบอร์ด
    │
    ▼
หลักสูตร 2  พัฒนาเฟิร์มแวร์ร่วมกับ Digital Twin        เฟิร์มแวร์ ↔ Digital Twin ↔ คลาวด์
    │
    ▼
หลักสูตร 3  การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม        ออกแบบผลิตภัณฑ์ → Twin → ต้นแบบจริง
```

ถ้าต้องการแค่งานออกแบบใน Blender เริ่มโมดูล 1–3 ของหลักสูตร 3 ก่อนได้ ส่วนแล็บที่ใช้ Twin จะง่ายขึ้นมากหลังเรียนหลักสูตร 2

- หลักสูตร 1: [TESA Firmware SDK สำหรับ Edge AI](../firmware-sdk-edge-ai/README.md)
- หลักสูตร 2: [พัฒนาเฟิร์มแวร์ร่วมกับ TESA Digital Twin บน VS Code](../digital-twin/README.md)
- หลักสูตร 3: [การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)](../product-design/README.md)

## ที่มาและสัญญาอนุญาต

เนื้อหาหลักสูตรนี้นำเข้าจาก [drsanti/TESAIoT-Courses](https://github.com/drsanti/TESAIoT-Courses) โฟลเดอร์ `C1/` ที่ commit [`287c218`](https://github.com/drsanti/TESAIoT-Courses/tree/287c21814ba8c75f693136616dcd270349a15966/C1) งานต้นฉบับได้รับทุนจากสมาคมสมองกลฝังตัวไทย (TESA) ซึ่งเป็นผู้ถือสิทธิ์ และเผยแพร่ที่นี่ภายใต้ [CC BY-NC 4.0](../../LICENSES/CC-BY-NC-4.0.txt) TESA Open Knowledge คงข้อความสอนของผู้เขียนไว้ตามเดิม สิ่งที่เพิ่มคือโครงสร้างโมดูล/บทเรียน front matter คำถามเช็กความเข้าใจ หมายเหตุเรื่องเฟิร์มแวร์และเครื่องมือ การแก้ลิงก์ให้ตรงโครงสร้างใหม่ และการปรับถ้อยคำที่ผูกกับการอบรมในห้องเรียน (เช่น รอบอบรม คะแนน) ให้เหมาะกับการเรียนแบบเปิด เครื่องมือและเอกสารของบุคคลที่สาม (Infineon, Blender, ระบบนิเวศ MQTT ฯลฯ) อยู่ภายใต้สัญญาอนุญาตของเจ้าของแต่ละราย

## อ้างอิง TESA

ถ้าคุณนำเนื้อหาหลักสูตรนี้ไปใช้ต่อ ไม่ว่าจะเป็นสไลด์ เอกสารประกอบการสอน มคอ.3 เอกสารแจก หรือ repo โค้ด โปรดอ้างอิงด้วยข้อความนี้:

> "TESA Firmware SDK สำหรับ Edge AI" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0

ถ้าคุณดัดแปลงเนื้อหา ให้เติม «(ดัดแปลง)» ต่อท้ายข้อความข้างบน และคงเครดิตผู้เขียนต้นฉบับไว้ด้วย:

> เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
>
> เครื่องมือ Bitstream Studio (VS Code) และ Ternion ที่หลักสูตรนี้ใช้ เป็นผลงานของ ผศ.ดร.สันติ นุราช (KMUTT)

การอ้างอิงไม่ได้หมายความว่า TESA หรือ Infineon รับรองหลักสูตรหรืองานของคุณ ดูรูปแบบและตัวอย่างการอ้างอิงเพิ่มเติม (สไลด์ มคอ.3 เอกสารแจก repo โค้ด) ได้ที่ [ATTRIBUTION.md](../../ATTRIBUTION.md)
