---
id: fw-stack.m05.l03
lang: en
title:
  th: "PSoC Edge E84 กับ OPTIGA™ Trust M: กุญแจที่ไม่ออกจากชิป"
  en: "PSoC Edge E84 with OPTIGA™ Trust M: keys that never leave the chip"
summary:
  th: "PSoC Edge E84 กับ OPTIGA™ Trust M: กุญแจที่ไม่ออกจากชิป"
  en: "PSoC Edge E84 with OPTIGA™ Trust M: keys that never leave the chip"
level: L3
time_min: {concept: 15, lab: 45, check: 5}
hardware: {emulator: false, boards: [eva-kit]}
prerequisites: [fw-stack.m02.l07]
objectives:
  - th: "อธิบาย workflow การ provision อุปกรณ์ที่สร้างและเก็บ private key ใน OPTIGA Trust M"
    en: "Explain the provisioning workflow that creates and keeps the private key inside OPTIGA Trust M"
  - th: "เชื่อมต่อ MQTT over TLS ด้วย certificate ที่เก็บใน OPTIGA ตามตัวอย่าง"
    en: "Connect MQTT over TLS with the certificate stored in OPTIGA, following the example"
develops:
  - {skill: sec.secure-element, to: 2}
  - {skill: sec.tls, to: 3}
  - {skill: sec.fundamentals, to: 2}
context: {platform: psoc-edge-e84, lang: c}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "examples/security/pse84_tesaiot_client"
  ref: d2ed42c4a31232f553b6b8cef9ee7373db348c21
source_sha256: 100c909c3b18ccffc6e897979e3648725fece6c2b76168e0b1cb9dacb0de40fc
---

# PSoC Edge E84 with OPTIGA™ Trust M: keys that never leave the chip

## Objectives

1. Explain the provisioning workflow that creates and keeps the private key inside OPTIGA Trust M
2. Connect MQTT over TLS with the certificate stored in OPTIGA, following the example

## Concepts

A device that sends data to the platform must be able to prove it is talking to the real server, and the platform must know the device is genuine. This lesson uses Developer Hub reference examples that connect to the real TESAIoT Platform.

## Worked example

Runs on the PSoC Edge E84 board with the OPTIGA™ Trust M (this project has the Eva Kit BSP: APP_KIT_PSE84_EVAL_EPC2)

- [Example README](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/security/pse84_tesaiot_client/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/security/pse84_tesaiot_client) · commit `d2ed42c`
- You need device credentials from the TESAIoT Platform, following the steps in the README. Never commit real credentials to a public repository.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- Why is a private key inside a secure element safer than one in flash?
- What does Protected Update do with the certificate?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--pse84_tesaiot_client&q=pse84_tesaiot_client)
- This code is under the Cypress (Infineon) EULA, so it is referenced by link only
