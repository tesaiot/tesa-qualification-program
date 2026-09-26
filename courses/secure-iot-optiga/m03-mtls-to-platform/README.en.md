# Module 3 · mTLS to the TESAIoT Platform

**Module goal:** connect the device to the platform with mTLS, using an identity anchored in the secure element.

Status **alpha** (content complete, awaiting pilot teaching and feedback) · about 140 minutes

**Module agreement:** the main lab runs on a computer with `openssl` and `mosquitto-clients`. The on-board lab needs a device already registered with the TESAIoT Platform, and credentials from the bundle must never be pushed to any repository.

| Lesson | Topic | Time |
|---|---|---|
| [sec-iot.m03.l01](l01-tls-and-mtls/README.md) | TLS and mTLS | 70 minutes |
| [sec-iot.m03.l02](l02-mqtts-to-tesaiot/README.md) | MQTTs to the TESAIoT Platform | 70 minutes |

## Module checkpoint

- [ ] an mTLS handshake diagram that marks which step uses the key inside the chip
- [ ] the device sends data over MQTTs to the TESAIoT Platform, and you can explain the connection log
