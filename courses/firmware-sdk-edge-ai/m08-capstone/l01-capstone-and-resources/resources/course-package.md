# Course package map — Modules and portals (M08)

**Course 1 · Module 8**

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [Capstone brief](capstone-brief.md) · [TOC](../../../README.md)

---

## Module index

| Module | Lesson | Lab | Cheatsheet / worksheet |
|---|---|---|---|
| M01 | [README](../../../m01-mcu-architecture/l01-architecture-and-sdk-layers/README.md) | [lab](../../../m01-mcu-architecture/l02-lab/README.md) | [sdk-layer](../../../m01-mcu-architecture/l01-architecture-and-sdk-layers/resources/sdk-layer-cheatsheet.md) |
| M02 | [README](../../../m02-toolchain/l01-modustoolbox-and-vscode/README.md) | [lab](../../../m02-toolchain/l02-lab/README.md) | [toolchain](../../../m02-toolchain/l01-modustoolbox-and-vscode/resources/toolchain-cheatsheet.md) |
| M03 | [README](../../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md) | [lab](../../../m03-gpio-peripherals/l02-lab/README.md) | [peripheral-api-map](../../../m03-gpio-peripherals/l01-gpio-and-peripherals/resources/peripheral-api-map.md) |
| M04 | [README](../../../m04-rtos/l01-freertos-programming/README.md) | [lab](../../../m04-rtos/l02-lab/README.md) | [rtos-patterns](../../../m04-rtos/l01-freertos-programming/resources/rtos-patterns.md) |
| M05 | [README](../../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) | [lab](../../../m05-sensor-data/l02-lab/README.md) | [sensor-ai-prep](../../../m05-sensor-data/l01-sensor-data-for-edge-ai/resources/sensor-ai-prep.md) |
| M06 | [README](../../../m06-mqtt/l01-mqtt-and-mqtts/README.md) | [lab](../../../m06-mqtt/l02-lab/README.md) | [mqtt-cloud](../../../m06-mqtt/l01-mqtt-and-mqtts/resources/mqtt-cloud.md) |
| M07 | [README](../../../m07-ble/l01-ble-connectivity/README.md) | [lab](../../../m07-ble/l02-lab/README.md) | [ble-connectivity](../../../m07-ble/l01-ble-connectivity/resources/ble-connectivity.md) |
| M08 | [README](../README.md) | [lab](../../l02-lab/README.md) | [capstone-brief](capstone-brief.md) |

Course overview: [หน้าหลักสูตร](../../../README.md)

---

## Online portals

| Portal | URL | Use |
|---|---|---|
| TESAIoT Developer Hub | https://dev.tesaiot.dev/ | Examples, flowchart, API Reference |
| Bitstream Studio | https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio | Host app / twin / tools |
| TESAIoT_Hackathon | https://github.com/drsanti/TESAIoT_Hackathon | HEX, Flasher, VSIX, web-app, ble-flet |

---

## API index (quick)

| Domain | Start here |
|---|---|
| Architecture | M01 |
| Tooling | M02 |
| GPIO / UART / PWM / ADC / I2C | M03 — `led_controller_*`, `cm55_button_*`, `sensor_adc_*`, `sensor_sht40_*` |
| RTOS | M04 — `xTaskCreate`, `vTaskDelay`, queues, mutex |
| Sensors / AI prep | M05 — `sensor_*_read`, fusion bridge, windows |
| MQTT | M06 — `cm55_trigger_mqtt_*`, JSON encode |
| BLE | M07 — `cm55_trigger_ble_periph_*`, `cm55_ble_request_scan_*` |

Full examples: [dev.tesaiot.dev](https://dev.tesaiot.dev/)

---

## Before you submit Capstone

- [ ] Lab M02–M07 ผ่านเกณฑ์ขั้นต่ำแล้ว  
- [ ] เลือก track MQTT และ/หรือ BLE ตามเกณฑ์ผ่าน  
- [ ] Broker / สแกนเนอร์ BLE พร้อม (ตามที่เลือก)  
- [ ] ไม่ฝังรหัสผ่านในไฟล์สาธารณะ  
- [ ] มี brief + README + หลักฐานสาธิต  

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [TOC](../../../README.md)
