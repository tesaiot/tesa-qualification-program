---
id: fw-stack.m05.l02
lang: en
title:
  th: "ยืนยันตัวตนทั้งสองฝั่งด้วย mTLS"
  en: "Mutual authentication with mTLS"
summary:
  th: "ยืนยันตัวตนทั้งสองฝั่งด้วย mTLS"
  en: "Mutual authentication with mTLS"
level: L3
time_min: {concept: 15, lab: 45, check: 5}
hardware: {emulator: false, boards: [none]}
prerequisites: [fw-stack.m02.l07]
objectives:
  - th: "ส่ง telemetry ด้วย mTLS โดยใช้ client certificate และ private key ของอุปกรณ์"
    en: "Send telemetry with mTLS using the device client certificate and private key"
  - th: "เปรียบเทียบ Server-TLS กับ mTLS ในด้านความปลอดภัยและการดูแลกุญแจ"
    en: "Compare Server-TLS and mTLS for security and key handling"
develops:
  - {skill: sec.tls, to: 3}
  - {skill: sec.crypto, to: 2}
  - {skill: iot.cloud-platform, to: 2}
context: {platform: host-pc, lang: c}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "examples/embedded-devices/intermediate/device-mtls"
  ref: d2ed42c4a31232f553b6b8cef9ee7373db348c21
source_sha256: bc795213d40f1630f0487df11390e01b80a8dd090b6fd2cc14f342986d940cd2
---

# Mutual authentication with mTLS

## Objectives

1. Send telemetry with mTLS using the device client certificate and private key
2. Compare Server-TLS and mTLS for security and key handling

## Concepts

A device that sends data to the platform must be able to prove it is talking to the real server, and the platform must know the device is genuine. This lesson uses Developer Hub reference examples that connect to the real TESAIoT Platform.

## Worked example

This example is written in C and runs on a computer first (GCC/Clang with OpenSSL, mbedTLS or wolfSSL, or libcurl) so the protocol is easy to see, before you carry the same ideas over to the board.

- [Example README](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/intermediate/device-mtls/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/intermediate/device-mtls) · commit `d2ed42c`
- You need device credentials from the TESAIoT Platform, following the steps in the README. Never commit real credentials to a public repository.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- What does mTLS add on top of Server-TLS?
- If a device's private key leaks, what is the impact?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--device-mtls&q=device-mtls)
- The example lives in tesaiot/developer-hub (Apache-2.0) and is referenced by link
