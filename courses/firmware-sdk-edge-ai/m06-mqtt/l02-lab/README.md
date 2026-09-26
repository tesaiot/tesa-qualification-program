---
id: fw-sdk.m06.l02
lang: th
title:
  th: 'แล็บ: Wi-Fi, MQTT connect, publish และ subscribe'
  en: 'Lab: Wi-Fi, MQTT Connect, Publish, and Subscribe'
summary:
  th: join Wi-Fi เชื่อม MQTT publish ข้อความหรือ telemetry แล้ว subscribe รับคำสั่งกลับ พร้อมบันทึกคอนฟิกโดยไม่เปิดเผยความลับ
  en: Join Wi-Fi, connect MQTT, publish a message or telemetry, subscribe to commands and record the configuration without exposing secrets.
level: L3
time_min:
  lab: 210
hardware:
  emulator: false
  boards:
  - devkit
  - eva-kit
prerequisites:
- fw-sdk.m06.l01
objectives:
- th: เชื่อม Wi-Fi จนสถานะ CONNECTED แล้วเชื่อม MQTT กับ broker ที่เลือก
  en: Join Wi-Fi until CONNECTED, then connect MQTT to the chosen broker.
- th: publish ข้อความหรือ telemetry แล้วเห็นบน subscriber ของโฮสต์
  en: Publish a message or telemetry and see it on a host subscriber.
- th: รับคำสั่งกลับที่อุปกรณ์ผ่าน subscribe และบันทึกคอนฟิกที่ใช้โดยไม่มีความลับในรายงาน
  en: Receive a command on the device via subscribe and record the configuration with no secrets in the report.
develops:
- skill: proto.mqtt
  to: 2
- skill: proto.wifi
  to: 2
- skill: sec.tls
  to: 1
assesses:
- skill: proto.mqtt
  level: 2
  evidence: README.md#submit-checklist
context:
  platform: psoc-edge-e84
  lang: c
  ide: modustoolbox-vscode
  firmware: tesaiot-bitstream (HEX; source not public yet)
status: alpha
translation: done
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M06/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M06 — Wi‑Fi, MQTT Connect, Publish, and Subscribe

**Course 1 · Module 6**  
**Type:** Hands-on lab (network + broker + device)  
**Suggested time:** 2.5–3.5 hours  

Read first: [Lesson](../l01-mqtt-and-mqtts/README.md) · [Cheatsheet](../l01-mqtt-and-mqtts/resources/mqtt-cloud.md) · [← Table of Contents](../../README.md) · [← M05](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) · [M07 BLE →](../../m07-ble/l01-ble-connectivity/README.md)

> **หมายเหตุ:** snippet ในแล็บนี้ใช้ API ของเฟิร์มแวร์ TESAIoT Bitstream ซึ่งยังไม่เปิดซอร์ส ดูรายละเอียดและตัวอย่างเทียบใน SDK สาธารณะได้ที่หมายเหตุต้นบทเรียน [MQTT และ MQTTs บนอุปกรณ์ Edge](../l01-mqtt-and-mqtts/README.md)

### Useful references during the lab

| เอกสาร | ใช้เมื่อ |
|---|---|
| [Lesson](../l01-mqtt-and-mqtts/README.md) | `cm55_trigger_mqtt_*`, CONFIG, topics |
| [Hackathon MQTT pages](https://github.com/drsanti/TESAIoT_Hackathon) | `web-app/ex09`–`ex15` |
| [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) | Start broker / MQTT tools |
| [HiveMQ MQTT Essentials](https://www.hivemq.com/mqtt-essentials/) | ทบทวน QoS / retain |

---

## Lab Goals

- Join Wi‑Fi จนสถานะ **CONNECTED**  
- **Connect MQTT** ไปยัง broker ที่เลือกใช้  
- **Publish** ข้อความหรือ telemetry อย่างน้อยหนึ่งครั้ง  
- **Subscribe** (จากโฮสต์หรืออุปกรณ์) แล้วเห็นข้อความ  
- อธิบายความต่าง MQTT vs MQTTs และบันทึกค่าคอนฟิกที่ใช้  
- (แนะนำ) ดู JSON telemetry จากเซ็นเซอร์ (ต่อจาก M05)  

---

## Prerequisites

- [ ] ผ่าน M05 อย่างน้อยอ่านเซ็นเซอร์ได้ (สำหรับ telemetry)  
- [ ] SSID / รหัส Wi‑Fi ของห้อง (ไม่บันทึกลง Git)  
- [ ] Broker host/port ที่เลือกใช้  
- [ ] เครื่องมือ subscribe บน PC (MQTTX, mosquitto_sub, หรือ Hackathon web-app)  

> **อย่า** publish รหัสผ่านหรือใบรับรองจริงลงรายงานสาธารณะ

---

## Lab A — Wi‑Fi link (required)

1. เรียก `cm55_trigger_connect` หรือ `example_wifi_ui_connect` ตามโปรเจกต์  
2. อ่าน `cm55_get_wifi_status` จน `IPC_WIFI_LINK_CONNECTED`  
3. บันทึก SSID (ไม่ต้องบันทึกรหัสผ่าน)  

**Pass when:** ลิงก์ Wi‑Fi พร้อมก่อนแตะ MQTT

---

## Lab B — MQTT connect + status (required)

1. ตั้ง policy ให้ MQTT ใช้งานได้ (เช่น factory default)  
2. `cm55_trigger_mqtt_connect`  
3. อ่าน `cm55_get_mqtt_status` จน `state == CONNECTED (2)`  
4. จด `broker_host`, `port`, `tls`, `effective_client_id`  

```c
(void)cm55_trigger_mqtt_connect();
/* poll cm55_get_mqtt_status until connected or timeout */
```

**Pass when:** สถานะ CONNECTED และมี client id ให้จด

---

## Lab C — Publish and observe (required)

เลือกอย่างน้อยหนึ่งทาง:

### C1 Telemetry path

- เปิดเซ็นเซอร์ + policy `TELEMETRY_PUBLISH`  
- Subscribe บนโฮสต์ที่ topic `bitstream/<MAC12>/sensors` (หรือ topic ที่คุณตั้งไว้)  
- ยืนยันว่ามี JSON เข้ามา  

### C2 Explicit publish

- ใช้เส้นทางใดเส้นทางหนึ่ง (`cm33_mqtt_stack_publish` หรือแผง Studio) ส่ง `{"hello":1}`  
- เห็นข้อความบน subscriber  

**Pass when:** เห็น payload บนเครื่องมือโฮสต์อย่างน้อยหนึ่งครั้ง

---

## Lab D — Subscribe / command path (required)

1. Subscribe ฝั่งอุปกรณ์ที่ topic actuators (หรือใช้คอนฟิก topic table ที่มีอยู่)  
2. จากโฮสต์ publish คำสั่งทดสอบไปยัง topic นั้น  
3. บันทึกว่าอุปกรณ์ได้รับอย่างไร (log / LED / เหตุการณ์ตามที่เฟิร์มแวร์รองรับ)  

**Pass when:** มีหลักฐานว่าข้อความจาก cloud/โฮสต์ถึงอุปกรณ์ (หรือถึง log ของสแต็ก)

---

## Lab E — Choose one (recommended)

### E1 MQTT vs MQTTs table

กรอกตารางเปรียบเทียบจากการทดลองหรือจากเอกสารของชุดที่ใช้: พอร์ต, `tls`, CA  

### E2 Hackathon web MQTT

รัน `ex09`–`ex14` ตาม [Hackathon README](https://github.com/drsanti/TESAIoT_Hackathon) (broker ใน Studio ถ้าจำเป็น)  

### E3 Payload design

ออกแบบ JSON สำหรับ event จาก M05 (เกณฑ์อุณหภูมิ/ฟีเจอร์) แล้วลอง publish หนึ่งครั้ง  

**Pass when:** ส่งตาราง/สกรีนช็อต/ไฟล์ออกแบบสั้น ๆ

---

## Short report (10–15 lines)

1. Wi‑Fi SSID (ไม่มีรหัสผ่าน)  
2. Broker host:port และ tls 0/1  
3. Client id / MAC topic ที่ใช้  
4. หลักฐาน publish + subscribe  
5. ข้อจำกัดที่สังเกต (เช่น QoS ของ telemetry, ต้องมี Wi‑Fi ก่อน)  

---

## Troubleshooting

| อาการ | แนวทาง |
|---|---|
| MQTT error / ไม่เชื่อม | Wi‑Fi ยังไม่ขึ้น · `MQTT_ENABLED` ปิด · host/port ผิด |
| เชื่อมได้แต่ไม่มี telemetry | เซ็นเซอร์ไม่ publish · ปิด `TELEMETRY_PUBLISH` · topic ผิด |
| TLS fail | พอร์ตไม่ใช่ 8883 · CA ไม่ตรง broker · นาฬิกาอุปกรณ์เพี้ยน (ถ้ามีผลตรวจใบรับรอง) |
| Subscribe ไม่เห็นของ | คนละ MAC / คนละ prefix topic · คนละ broker |
| Auth fail | username/password ว่างหรือผิด |

---

## Submit checklist

- [ ] Lab A–D ผ่าน  
- [ ] Lab E อย่างน้อย 1 ข้อ  
- [ ] กรอก [mqtt-cloud.md](../l01-mqtt-and-mqtts/resources/mqtt-cloud.md)  
- [ ] รายงานสั้นไม่มีความลับ  

[Lesson](../l01-mqtt-and-mqtts/README.md) · [Cheatsheet](../l01-mqtt-and-mqtts/resources/mqtt-cloud.md) · [Table of Contents](../../README.md) · [M07 BLE →](../../m07-ble/l01-ble-connectivity/README.md)
