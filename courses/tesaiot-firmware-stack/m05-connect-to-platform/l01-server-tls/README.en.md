---
id: fw-stack.m05.l01
lang: en
title:
  th: "ส่งข้อมูลขึ้น TESAIoT Platform ด้วย Server-TLS"
  en: "Telemetry to the TESAIoT Platform with Server-TLS"
summary:
  th: "ส่งข้อมูลขึ้น TESAIoT Platform ด้วย Server-TLS"
  en: "Telemetry to the TESAIoT Platform with Server-TLS"
level: L3
time_min: {concept: 15, lab: 45, check: 5}
hardware: {emulator: false, boards: [none]}
prerequisites: [fw-stack.m02.l07]
objectives:
  - th: "ส่ง telemetry ขึ้นแพลตฟอร์มผ่าน HTTPS หรือ MQTTS แบบ Server-TLS ด้วยตัวอย่างภาษา C"
    en: "Send telemetry to the platform over HTTPS or MQTTS with Server-TLS using the C example"
  - th: "อธิบายว่า CA certificate ทำหน้าที่อะไรในการยืนยันตัวตนของเซิร์ฟเวอร์"
    en: "Explain what the CA certificate does when verifying the server"
develops:
  - {skill: sec.tls, to: 2}
  - {skill: proto.mqtt, to: 2}
  - {skill: iot.cloud-platform, to: 2}
context: {platform: host-pc, lang: c}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "examples/embedded-devices/entry/device-servertls"
  ref: d2ed42c4a31232f553b6b8cef9ee7373db348c21
source_sha256: 699293e41735b922a575f590b575ddfc1438a1a7397681cbe1c5c285effda471
---

# Telemetry to the TESAIoT Platform with Server-TLS

## Objectives

1. Send telemetry to the platform over HTTPS or MQTTS with Server-TLS using the C example
2. Explain what the CA certificate does when verifying the server

## Concepts

A device that sends data to the platform must be able to prove it is talking to the real server, and the platform must know the device is genuine. This lesson uses Developer Hub reference examples that connect to the real TESAIoT Platform.

## Worked example

This example is written in C and runs on a computer first (GCC/Clang with OpenSSL, mbedTLS or wolfSSL, or libcurl) so the protocol is easy to see, before you carry the same ideas over to the board.

- [Example README](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/entry/device-servertls/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/entry/device-servertls) · commit `d2ed42c`
- You need device credentials from the TESAIoT Platform, following the steps in the README. Never commit real credentials to a public repository.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- Whose identity does Server-TLS verify, and whose does it not verify?
- If the device's clock is wrong, why might TLS fail?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--device-servertls&q=device-servertls)
- The example lives in tesaiot/developer-hub (Apache-2.0) and is referenced by link
