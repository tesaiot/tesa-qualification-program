
# Module 6 — MQTT and MQTTs for Cloud Communication

*MQTT and MQTTs for Cloud Communication* · [TESA Firmware SDK for Edge AI](../README.md) course

## Objectives

Connect the device to a broker: always join Wi-Fi first, then connect MQTT, publish telemetry, subscribe to receive commands, and understand the difference between MQTT and MQTTs.

## Lessons

| # | Lesson | Content |
|---|---|---|
| 1 | [MQTT and MQTTs on an edge device](l01-mqtt-and-mqtts/README.md) | The publish/subscribe principle, the firmware's connection path (Wi-Fi → MQTT), configuring the broker, topics, JSON payloads, and security with TLS |
| 2 | [Lab: Wi-Fi, MQTT connect, publish and subscribe](l02-lab/README.md) | Joining Wi-Fi, connecting MQTT, publishing a message or telemetry, then subscribing to receive a command back, recording the config without exposing secrets |

Approximate time per the original: about 3.5–4 hours (lessons) + a 2.5–3.5 hour lab.

Accompanying sheets and templates (in the `resources/` folder of lesson 1):

- [mqtt-cloud.md](l01-mqtt-and-mqtts/resources/mqtt-cloud.md)

> The C code in this module uses the API of the TESAIoT Bitstream firmware, which is not yet open source. Read the note at the top of the [lesson](l01-mqtt-and-mqtts/README.md) before you start.

## Checkpoint

Before moving to the next module, check that you can do the following:

- [ ] Wi-Fi reaches the CONNECTED state, and MQTT connects to the chosen broker
- [ ] After publishing, the message appears on the host's subscriber
- [ ] A command from the host reaches the device
- [ ] The short report contains no real passwords or certificates

[← Module 5](../m05-sensor-data/README.md) · [Course page](../README.md) · [Module 7 →](../m07-ble/README.md)
