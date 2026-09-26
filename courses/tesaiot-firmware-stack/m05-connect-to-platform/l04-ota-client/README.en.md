---
id: fw-stack.m05.l04
lang: en
title:
  th: "อัปเดตเฟิร์มแวร์ทางไกลด้วย OTA client"
  en: "Remote firmware update with the OTA client"
summary:
  th: "อัปเดตเฟิร์มแวร์ทางไกลด้วย OTA client"
  en: "Remote firmware update with the OTA client"
level: L3
time_min: {concept: 15, lab: 45, check: 5}
hardware: {emulator: false, boards: [none]}
prerequisites: [fw-stack.m02.l07]
objectives:
  - th: "อธิบายขั้นตอน OTA: ถามงาน อ่าน job document ดาวน์โหลด ตรวจ integrity และรายงานผล"
    en: "Explain the OTA steps: poll, read the job document, download, verify integrity and report"
  - th: "อ่านโค้ด OTA client และระบุว่าขั้นตอนใด (รายงานสถานะ ดาวน์โหลด ตรวจ integrity) ยังเป็น TODO ในตัวอย่างอ้างอิง"
    en: "Read the OTA client code and name which steps (status report, download, integrity check) are still TODO in the reference example"
develops:
  - {skill: iot.ota, to: 2}
  - {skill: mcu.bootloader, to: 1}
  - {skill: sec.fundamentals, to: 1}
context: {platform: host-pc, lang: c}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "examples/embedded-devices/advanced/c_ota_client"
  ref: d2ed42c4a31232f553b6b8cef9ee7373db348c21
source_sha256: 9fb549a6823b7e707a66d3ddb92d710baf71a89bfbe74ac21d110e924568acf1
---

# Remote firmware update with the OTA client

## Objectives

1. Explain the OTA steps: poll, read the job document, download, verify integrity and report
2. Read the OTA client code and name which steps (status report, download, integrity check) are still TODO in the reference example

## Concepts

A device that sends data to the platform must be able to prove it is talking to the real server, and the platform must know the device is genuine. This lesson uses Developer Hub reference examples that connect to the real TESAIoT Platform.

## Worked example

This example is written in C and runs on a computer first (GCC/Clang with OpenSSL, mbedTLS or wolfSSL, or libcurl) so the protocol is easy to see, before you carry the same ideas over to the board.

- [Example README](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/advanced/c_ota_client/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/advanced/c_ota_client) · commit `d2ed42c`
- You need device credentials from the TESAIoT Platform, following the steps in the README. Never commit real credentials to a public repository.

> **Warning:** without `--ca-cert`, the `ota_client.c` example at this commit disables server certificate verification, and the example command in the example's README does not include this flag either. Always include `--ca-cert`. A real device must never disable certificate verification.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- Why must you verify a firmware image's integrity before installing it?
- If power is lost during an update, what should a well-designed system do?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--c_ota_client&q=c_ota_client)
- The example lives in tesaiot/developer-hub (Apache-2.0) and is referenced by link
