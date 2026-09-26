---
id: fw-sdk.m07.l02
lang: th
title:
  th: 'แล็บ: การเชื่อมต่อ BLE'
  en: 'Lab: BLE Connectivity'
summary:
  th: อ่านสถานะ peripheral สั่ง advertising ให้โฮสต์ค้นพบและเชื่อมต่อ ทดสอบลิงก์สั้น ๆ และ (ทางเลือก) ลอง scan
  en: Read peripheral status, start advertising so a host can discover and connect, soak the link briefly and optionally try a scan.
level: L3
time_min:
  lab: 150
hardware:
  emulator: false
  boards:
  - devkit
  - eva-kit
prerequisites:
- fw-sdk.m07.l01
objectives:
- th: อ่านสถานะ BLE peripheral ก่อนและหลังโฮสต์เชื่อมต่อ แล้วบันทึกเป็นตาราง
  en: Read BLE peripheral status before and after a host connects and record it in a table.
- th: สั่ง advertising และยืนยันด้วยโฮสต์ (GATT explorer) ว่าเห็นและเชื่อมต่ออุปกรณ์ได้
  en: Start advertising and confirm with a host (GATT explorer) that it can see and connect to the device.
develops:
- skill: proto.bluetooth
  to: 2
assesses:
- skill: proto.bluetooth
  level: 2
  evidence: README.md#deliverables-checklist
context:
  platform: psoc-edge-e84
  lang: c
  ide: modustoolbox-vscode
  firmware: tesaiot-bitstream (HEX; source not public yet)
status: alpha
translation: done
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M07/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M07 — BLE Connectivity

**Course 1 · Module 7**  
**Type:** Hands-on lab (status → advertising → host link; optional scan)  
**Suggested time:** ~2–2.5 hours on hardware  

Read first: [Lesson](../l01-ble-connectivity/README.md) · [Cheatsheet](../l01-ble-connectivity/resources/ble-connectivity.md) · [← Table of Contents](../../README.md) · [← M06](../../m06-mqtt/l01-mqtt-and-mqtts/README.md) · [M08 →](../../m08-capstone/l01-capstone-and-resources/README.md)

> **หมายเหตุ:** snippet ในแล็บนี้ใช้ API ของเฟิร์มแวร์ TESAIoT Bitstream ซึ่งยังไม่เปิดซอร์ส ดูรายละเอียดและตัวอย่างเทียบใน SDK สาธารณะได้ที่หมายเหตุต้นบทเรียน [BLE สำหรับผลิตภัณฑ์ Edge](../l01-ble-connectivity/README.md)

> **โฮสต์ `ble-flet` ยังไม่เผยแพร่** — [README ของ TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/blob/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/README.md) (commit `f5f09a6`) ระบุว่า `python-app/`, `ble-react/` และ `ble-flet/` เป็นของผู้ดูแลและไม่อยู่ใน repo สาธารณะ ให้ใช้เส้นทางสำรองที่บทเรียนเสนอไว้แล้ว คือ GATT explorer ทั่วไป เช่น nRF Connect, LightBlue หรือ AIROC™ Bluetooth® Connect

### Useful references during the lab

| เอกสาร | ใช้เมื่อ |
|---|---|
| [Hackathon ble-flet](https://github.com/drsanti/TESAIoT_Hackathon) | desktop central + stream |
| [Infineon Find Me CE](https://github.com/Infineon/mtb-example-psoc-edge-btstack-findme) | mobile app workflow (ผู้ผลิต) |
| [M06 lab](../../m06-mqtt/l02-lab/README.md) | เปรียบเทียบ cloud path |
| [M04 lab](../../m04-rtos/l02-lab/README.md) | task + delay |

---

## Lab Goals

- อ่าน **BLE peripheral status** จาก CM55  
- สั่ง **ADV start/stop/restart** และยืนยันว่าโฮสต์เห็นชื่อ `TESAIoT-*` (หรือชื่อที่ตั้งไว้)  
- เชื่อมโฮสต์อย่างน้อยหนึ่งตัว (`ble-flet` หรือ GATT explorer)  
- (ทางเลือก) รัน **scan** สั้น ๆ และบันทึกผลจาก IPC event  

---

## Prerequisites

- [ ] บอร์ด + HEX/เฟิร์มแวร์ที่ **เปิด BLE profile**  
- [ ] PC หรือโทรศัพท์เปิด Bluetooth  
- [ ] (แนะนำ) clone [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) และเตรียม `ble-flet`  
- [ ] ปิด Central อื่นที่อาจแย่งลิงก์ (nRF Connect ค้างอยู่ ฯลฯ)  

---

## Part A — Peripheral status

1. Flash เฟิร์มแวร์ตัวอย่าง (หรือ build ของคุณที่มี BLE)  
2. จาก task บน CM55 เรียก:

```c
ipc_ble_periph_status_t st;
bool ok = cm55_ble_periph_status_get_sync(&st, 5000U);
```

3. บันทึกค่า: `profile_ble_active`, `stack_ready`, `connection_id`, `last_error`  

**Pass when:** sync สำเร็จ และ `stack_ready` (หรือเทียบเท่าตามบิลด์) แสดงว่าสแต็กพร้อม

---

## Part B — Advertising + host discover

1. สั่ง start ADV:

```c
uint8_t result = 0xFF;
(void)cm55_ble_periph_adv_ctrl_sync(1U, &result, 5000U);
```

2. บนโฮสต์:  
   - **เส้นทางหลัก:** รัน `ble-flet` → ให้มัน hunt `TESAIoT-*`  
   - **เส้นทางสำรอง:** เปิด nRF Connect / แอปสแกน → หาชื่ออุปกรณ์ที่ตั้งไว้  

3. เมื่อเชื่อมแล้ว อ่าน status อีกครั้ง — คาดหวัง `connection_id != 0` และ/หรือ `tx_notify_enabled` ตามสถานะโฮสต์  

**Pass when:** โฮสต์เห็นและเชื่อมอุปกรณ์ได้ อย่างน้อยหนึ่งครั้ง พร้อมหลักฐาน (สกรีนช็อต)

---

## Part C — Link behaviour (short soak)

1. สตรีมหรืออ่านค่าสั้น ๆ บนโฮสต์ (~30–60 วินาที)  
2. กด disconnect บนโฮสต์ แล้วสั่ง ADV start/restart ถ้าจำเป็น  
3. เชื่อมใหม่ให้สำเร็จ  

**Pass when:** ทำ reconnect ได้โดยไม่ต้อง reflash (ยกเว้นกรณี ADV timeout ที่เอกสาร Hackathon ระบุ — แล้ว reboot ตามคู่มือ)

---

## Part D — Optional scan observer

1. ลงทะเบียน `cm55_ble_ipc_set_event_handler`  
2. เรียก `cm55_ble_request_scan_all()` (หรือ `scan_name`) สั้น ๆ  
3. บันทึกอย่างน้อย 1 รายการ adv (addr / rssi / name) จากล็อก  

**Pass when (optional):** มีล็อกผลสแกนที่อ่านได้

---

## Deliverables checklist

- [ ] ตาราง status ก่อน/หลัง connect  
- [ ] สกรีนช็อตโฮสต์ที่เห็น `TESAIoT-*` (หรือชื่อที่ตั้งไว้)  
- [ ] โน้ตสั้น: BLE ต่างจาก MQTT อย่างไรในโปรเจกต์ของคุณ  
- [ ] (ถ้าทำ Part D) ตัวอย่างล็อกสแกน  

---

## Troubleshooting

| อาการ | แนวทาง |
|---|---|
| Status timeout | ตรวจว่า HEX เปิด BLE · รอหลังบูตนานขึ้น · ตรวจ IPC |
| สแกนไม่เจอ | ADV start · เข้าใกล้ · ปิด Central อื่น · reboot บอร์ด |
| Connect แล้วหลุดทันที | อย่าเปิดสองแอป Central พร้อมกัน |
| `ble-flet` ไม่เจอหลัง 60s | ADV timeout — reboot หรือ HEX ที่แก้ auto-restart (ดู Hackathon README) |
| สับสนกับ Wi‑Fi lab | M07 ไม่ต้องมี broker; โฟกัสวิทยุ BLE |

[Lesson](../l01-ble-connectivity/README.md) · [Cheatsheet](../l01-ble-connectivity/resources/ble-connectivity.md) · [Table of Contents](../../README.md) · [M08 →](../../m08-capstone/l01-capstone-and-resources/README.md)
