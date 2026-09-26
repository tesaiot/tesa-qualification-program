---
id: fw-sdk.m07.l02
lang: en
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
source_sha256: aee186a6f4548f2669a6843ec708ae48ea5100ba82140dbad967601b42fab2c0
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

> **Note:** the snippets in this lab use the API of the TESAIoT Bitstream firmware, which is not yet open source. See detail and equivalent examples in the public SDK in the note at the top of the lesson [BLE for Edge Products](../l01-ble-connectivity/README.md)

> **The `ble-flet` host is not yet published** — the [TESAIoT_Hackathon README](https://github.com/drsanti/TESAIoT_Hackathon/blob/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/README.md) (commit `f5f09a6`) states that `python-app/`, `ble-react/` and `ble-flet/` belong to the maintainers and are not in the public repo. Use the backup path the lesson already suggests: a general GATT explorer such as nRF Connect, LightBlue, or AIROC™ Bluetooth® Connect

### Useful references during the lab

| Document | Use when |
|---|---|
| [Hackathon ble-flet](https://github.com/drsanti/TESAIoT_Hackathon) | A desktop central + stream |
| [Infineon Find Me CE](https://github.com/Infineon/mtb-example-psoc-edge-btstack-findme) | A mobile-app workflow (vendor) |
| [M06 lab](../../m06-mqtt/l02-lab/README.md) | Comparing against the cloud path |
| [M04 lab](../../m04-rtos/l02-lab/README.md) | Task + delay |

---

## Lab Goals

- Read the **BLE peripheral status** from the CM55
- Control **ADV start/stop/restart** and confirm the host sees the name `TESAIoT-*` (or whatever name you set)
- Connect at least one host (`ble-flet`, or a GATT explorer)
- (Optional) run a brief **scan** and record the result from an IPC event

---

## Prerequisites

- [ ] A board + HEX/firmware with the **BLE profile turned on**
- [ ] A PC or phone with Bluetooth on
- [ ] (Recommended) clone [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) and have `ble-flet` ready
- [ ] Close any other Central that might steal the link (nRF Connect still open, etc.)

---

## Part A — Peripheral status

1. Flash the example firmware (or your own build with BLE)
2. From a task on the CM55, call:

```c
ipc_ble_periph_status_t st;
bool ok = cm55_ble_periph_status_get_sync(&st, 5000U);
```

3. Record the values: `profile_ble_active`, `stack_ready`, `connection_id`, `last_error`

**Pass when:** the sync succeeds, and `stack_ready` (or the build's equivalent) shows the stack is ready

---

## Part B — Advertising + host discover

1. Start ADV:

```c
uint8_t result = 0xFF;
(void)cm55_ble_periph_adv_ctrl_sync(1U, &result, 5000U);
```

2. On the host:
   - **Main path:** run `ble-flet` → let it hunt for `TESAIoT-*`
   - **Backup path:** open nRF Connect / a scanning app → find the device's set name

3. Once connected, read the status again — expect `connection_id != 0` and/or `tx_notify_enabled`, depending on the host's state

**Pass when:** the host sees and connects to the device at least once, with evidence (a screenshot)

---

## Part C — Link behaviour (short soak)

1. Stream or read a value briefly on the host (~30–60 seconds)
2. Press disconnect on the host, then start/restart ADV if needed
3. Successfully reconnect

**Pass when:** you can reconnect without reflashing (except for the ADV-timeout case the Hackathon documentation notes — then reboot per the guide)

---

## Part D — Optional scan observer

1. Register `cm55_ble_ipc_set_event_handler`
2. Call `cm55_ble_request_scan_all()` (or `scan_name`) briefly
3. Record at least 1 advertisement entry (addr / rssi / name) from the log

**Pass when (optional):** there is a readable scan-result log

---

## Deliverables checklist

- [ ] A status table before/after connecting
- [ ] A screenshot of the host seeing `TESAIoT-*` (or whatever name you set)
- [ ] A short note: how does BLE differ from MQTT in your project?
- [ ] (If you did Part D) a sample scan log

---

## Troubleshooting

| Symptom | Approach |
|---|---|
| Status times out | Check the HEX has BLE on · wait longer after boot · check the IPC |
| No scan results | Start ADV · get closer · close other Centrals · reboot the board |
| Connects then drops immediately | Don't open two Central apps at the same time |
| `ble-flet` finds nothing after 60s | An ADV timeout — reboot, or a HEX with auto-restart fixed (see the Hackathon README) |
| Confused with the Wi‑Fi lab | M07 needs no broker; the focus is the BLE radio |

[Lesson](../l01-ble-connectivity/README.md) · [Cheatsheet](../l01-ble-connectivity/resources/ble-connectivity.md) · [Table of Contents](../../README.md) · [M08 →](../../m08-capstone/l01-capstone-and-resources/README.md)
