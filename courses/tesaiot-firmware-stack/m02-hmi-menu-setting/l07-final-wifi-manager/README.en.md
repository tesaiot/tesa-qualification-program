---
id: fw-stack.m02.l07
lang: en
title:
  th: "Wi-Fi Manager สมบูรณ์: เชื่อมต่อ ลองใหม่ และต่ออัตโนมัติ"
  en: "Complete Wi-Fi manager: connect, retry and auto-connect"
summary:
  th: "รวม scan + profile + connect + auto-retry + ping watchdog เป็น WiFi manager สมบูรณ์ พร้อม state machine บนหน้าจอและ auto-connect จาก profile ที่เก็บไว้"
  en: "Complete Wi-Fi manager: connect, retry and auto-connect"
level: L3
time_min: {concept: 15, practise: 25, lab: 20, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m02.l06]
objectives:
  - th: "รวม scan, profile และ connect เป็น Wi-Fi manager ที่ต่ออัตโนมัติจากโปรไฟล์ที่บันทึกไว้"
    en: "Combine scan, profile and connect into a Wi-Fi manager that auto-connects from the stored profile"
  - th: "ออกแบบ state machine ของการเชื่อมต่อ (ต่อ หลุด ลองใหม่) และแสดงสถานะบนจอ"
    en: "Design a connection state machine (connect, drop, retry) and show its state on screen"
  - th: "ใช้ ping ไปยัง gateway ตรวจว่าเครือข่ายตอบจริง และอธิบายว่าในตัวอย่างนี้ผลของ ping ไม่ได้สั่งให้ต่อใหม่"
    en: "Ping the gateway to check that the network really answers, and explain that in this example the ping result does not trigger a reconnect"
develops:
  - {skill: prog.state-machines, to: 3}
  - {skill: proto.wifi, to: 3}
  - {skill: proto.tcp-ip, to: 1}
  - {skill: rtos.basics, to: 2}
assesses:
  - {skill: prog.state-machines, level: 2, evidence: "วิดีโอหรือ log ที่บอร์ดต่อ Wi-Fi อัตโนมัติหลังรีเซ็ต และกลับมาเองหลังปิด AP"}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "hmi_ep07_final_wifi_manager"
  ref: 9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465
source_sha256: 09f83839b902382bb25b4e21474b78ece2ab83ca8ad25931cd1d4c20975977c5
---

# Complete Wi-Fi manager: connect, retry and auto-connect

## Objectives

1. Combine scan, profile and connect into a Wi-Fi manager that auto-connects from the stored profile
2. Design a connection state machine (connect, drop, retry) and show its state on screen
3. Ping the gateway to check that the network really answers, and explain that in this example the ping result does not trigger a reconnect

## Concepts

Combining scan + profile + connect + auto-retry + a ping watchdog into a complete Wi-Fi manager, with a state machine on screen and auto-connect from the stored profile

## Worked example

This episode's code lives on the Developer Hub (pinned to commit `9a8e3ed`). Read the full **Why / What / How** first in the [episode's README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/README.md), then work through the code in this order:

- [`main_example.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/main_example.c)
- [`nav/menu_nav_logic.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/nav/menu_nav_logic.c)
- [`nav/menu_nav_logic.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/nav/menu_nav_logic.h)
- [`nav/ui_menu_layout.h`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/nav/ui_menu_layout.h)
- [`nav/ui_menu_navigation.c`](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/nav/ui_menu_navigation.c)
- and 15 more files in the [episode's folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager)

### Build and flash

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

Or open [this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep07_final_wifi_manager&q=hmi_ep07_final_wifi_manager) and flash the ready-made firmware.

## See it work first

![Screen of EP07 — Final WiFi Manager on the TESAIoT Dev Kit](https://raw.githubusercontent.com/tesaiot/developer-hub/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/hmi_ep07_final_wifi_manager.png)

Before reading the code, guess what objects this screen has, and what changes when the user taps it or when a sensor value changes.

## Try a change

1. **Guess** before you change anything: pick one value the example's README explains in the How section, and write down what you expect to change on the screen or in the log.
2. **Change and run**: build + flash, then compare against your guess. If it does not match, find which part you misunderstood.
3. **Extend**: add one thing the example does not yet have, and keep a photo or video in your portfolio.

## Check your understanding

- Why is "connected to the AP" not enough on its own to say the internet works?
- Which states does the connection state machine need?
- What goes wrong if retries happen too often?

The answers are in the example's README and in the code. If you cannot answer one, go back and read the Why / What / How section again.

## References

- [Episode README](https://github.com/tesaiot/developer-hub/blob/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager/README.md) · [code folder](https://github.com/tesaiot/developer-hub/tree/9a8e3ed1d813bfd67fabf6b7ac15c6ff9750b465/hmi_ep07_final_wifi_manager) · commit `9a8e3ed`
- [Open this example on the Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep07_final_wifi_manager&q=hmi_ep07_final_wifi_manager)
- The code belongs to the Developer Hub and is referenced by link, not copied into this repository
