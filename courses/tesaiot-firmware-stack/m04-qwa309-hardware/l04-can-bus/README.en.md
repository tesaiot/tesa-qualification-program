---
id: fw-stack.m04.l04
lang: en
title:
  th: "CAN bus 500 kbps: ส่ง heartbeat และอ่านเฟรม"
  en: "CAN bus at 500 kbps: heartbeat out, frames in"
summary:
  th: "CAN bus 500 kbps: ส่ง heartbeat และอ่านเฟรม"
  en: "CAN bus at 500 kbps: heartbeat out, frames in"
level: L3
time_min: {concept: 10, practise: 25, lab: 30, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m01.l01]
objectives:
  - th: "ส่งเฟรม heartbeat 1 Hz ผ่าน CANFD0 แบบ Classic CAN 2.0A ที่ 500 kbps"
    en: "Send a 1 Hz heartbeat on CANFD0 as Classic CAN 2.0A at 500 kbps"
  - th: "อ่านเฟรมที่เข้ามา แสดงเฟรมล่าสุด (ID และข้อมูล) และตัวนับเฟรมที่รับและส่ง"
    en: "Receive frames and show the latest frame (ID and data) with the receive and transmit counters"
develops:
  - {skill: proto.can, to: 2}
  - {skill: gui.hmi, to: 2}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "prac_qwa309_can_monitor"
  ref: e5c772252e7d20f715463e0d27df9ece4e569c38
source_sha256: 084c71b4c22c04460b2020b91ee5738aea7a0f92a38d0ecfe1b3d2fb03ab862e
---

# CAN bus at 500 kbps: heartbeat out, frames in

## Objectives

1. Send a 1 Hz heartbeat on CANFD0 as Classic CAN 2.0A at 500 kbps
2. Receive frames and show the latest frame (ID and data) with the receive and transmit counters

## Concepts

The QWA309 base board of the TESAIoT Dev Kit gives you real hardware to practise with: push buttons, four potentiometers, a CAN transceiver and a header for external devices. This lesson uses Developer Hub exercises written specifically for this board.

## Worked example

The QWA309 exercise set on the Developer Hub (pinned to commit `e5c7722`) runs only on the TESAIoT Dev Kit, because it uses hardware on the base board.

- **QWA309 — CAN Bus Monitor** — CANFD0 running Classic CAN 2.0A at 500 kbps (P16.2 RX / P16.3 TX, SN65HVD230) on CM55 in polled mode — a 1 Hz TX heartbeat plus an RX frame table on LVGL
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_can_monitor/README.md) · [code](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_can_monitor) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_can_monitor&q=prac_qwa309_can_monitor)

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- Why must a CAN bus have termination at the ends of the cable?
- What does a CAN frame's ID tell you, beyond just naming the message?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [All TESAIoT Dev Kit exercises](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38) · commit `e5c7722`
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
