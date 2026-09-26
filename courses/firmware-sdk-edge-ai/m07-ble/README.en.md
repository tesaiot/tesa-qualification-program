
# Module 7 — Bluetooth Low Energy (BLE) Connectivity

*Bluetooth Low Energy (BLE) Connectivity* · [TESA Firmware SDK for Edge AI](../README.md) course

## Objectives

Connect the board to a nearby phone or PC over BLE: read the peripheral's status, control advertising, and confirm the connection with a host, while understanding how BLE differs from MQTT.

## Lessons

| # | Lesson | Content |
|---|---|---|
| 1 | [BLE for edge products](l01-ble-connectivity/README.md) | BLE's role compared with MQTT, GAP/GATT terminology, the CM33/CM55 split of work, reading status, controlling advertising, and the scan path |
| 2 | [Lab: BLE connectivity](l02-lab/README.md) | Reading the peripheral's status, controlling advertising so a host can discover and connect, briefly testing the link, and (optional) trying a scan |

Approximate time per the original: about 3–3.5 hours (lessons) + a ~2–2.5 hour lab.

Accompanying sheets and templates (in the `resources/` folder of lesson 1):

- [ble-connectivity.md](l01-ble-connectivity/resources/ble-connectivity.md)

> The C code in this module uses the API of the TESAIoT Bitstream firmware, which is not yet open source. Read the note at the top of the [lesson](l01-ble-connectivity/README.md) before you start.

## Checkpoint

Before moving to the next module, check that you can do the following:

- [ ] A table of the peripheral's status before and after a host connects
- [ ] A screenshot of the host seeing and connecting to the device
- [ ] A short note on how BLE differs from MQTT in your project

[← Module 6](../m06-mqtt/README.md) · [Course page](../README.md) · [Module 8 →](../m08-capstone/README.md)
