---
id: fw-stack.m01.l01
lang: en
title:
  th: "เครื่องมือ บอร์ด และ master template"
  en: "Toolchain, board and the master template"
summary:
  th: "ติดตั้ง ModusToolbox เตรียม master template ของ TESAIoT Firmware Stack แล้ว build และ flash ครั้งแรก"
  en: "Install ModusToolbox, set up the TESAIoT Firmware Stack master template, then build and flash for the first time"
level: L2
time_min: {concept: 15, lab: 45}
hardware: {emulator: false, boards: [devkit]}
prerequisites: []
objectives:
  - th: "ติดตั้ง ModusToolbox และ clone master template แล้ว build ผ่านโดยไม่มี error"
    en: "Install ModusToolbox, clone the master template and build it without errors"
  - th: "วางไฟล์ของ episode ลงใน proj_cm55/apps/ แล้ว flash ลงบอร์ดผ่าน KitProg3 ได้"
    en: "Drop an episode into proj_cm55/apps/ and flash it through KitProg3"
  - th: "อธิบายบทบาทของ proj_cm33_s, proj_cm33_ns และ proj_cm55 ในชิปสองคอร์"
    en: "Explain the roles of proj_cm33_s, proj_cm33_ns and proj_cm55 on the dual-core chip"
develops:
  - {skill: build.vendor-sdk, to: 2}
  - {skill: build.make-cmake, to: 2}
  - {skill: build.compilers, to: 1}
  - {skill: vcs.git, to: 1}
  - {skill: hw.architecture, to: 1}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "README.md"
  ref: 082fd3e76595b62cfdb213499a093c233dbb4b53
source_sha256: afd603a59fb87b261dec0c9ba2cc4b75d8ca1747e09156045656181d3bbc0d05
---

# Toolchain, board and the master template

## Objectives

1. Install ModusToolbox, clone the master template and build it without errors
2. Drop an episode into proj_cm55/apps/ and flash it through KitProg3
3. Explain the roles of proj_cm33_s, proj_cm33_ns and proj_cm55 on the dual-core chip

## What you need

- **TESAIoT Dev Kit** (the PSoC Edge AI Kit SoM on the QWA309 base board) and a USB-C cable for KitProg3
- Infineon **ModusToolbox** 3.6 or later, as the master template README says (the episode series README recommends 3.8)
- **git** and a computer that can build C (Windows, macOS or Linux)

## Concepts

The TESAIoT Firmware Stack splits the work into three projects, one per core of the PSoC Edge E84: `proj_cm33_s` (secure),
`proj_cm33_ns` (non-secure: starts the CM55 core, then enters deep sleep) and `proj_cm55` (FreeRTOS, the LVGL display, the VGLite GPU,
the sensors, Wi-Fi and our application).
The master template gets everything ready from boot onwards. We write only the files in `proj_cm55/apps/` and the function
`example_main(parent)` that the master calls for us.

## Lab: build and flash for the first time

1. Clone the master template from the `tesaiot_dev_kit_master` branch of the Developer Hub

   ```sh
   git clone -b tesaiot_dev_kit_master https://github.com/tesaiot/developer-hub.git tesaiot_dev_kit_master
   cd tesaiot_dev_kit_master
   make getlibs
   ```


2. Build and flash following the steps in the [master template README](https://github.com/tesaiot/developer-hub/blob/082fd3e76595b62cfdb213499a093c233dbb4b53/README.md)

```sh
# In the master template folder (see lesson 1.1)
# 1) Delete the old episode's files in proj_cm55/apps/
# 2) Copy all of this episode's files into proj_cm55/apps/
make build
make program     # flash through KitProg3
```

3. If you are not ready to build it yourself yet, open the example on the [Developer Hub](https://dev.tesaiot.dev/) and flash the ready-made firmware
   from the example page (every episode in modules 2–3 and every QWA309 practice code in module 4 has ready-to-use firmware)

## Check your understanding

- Where must an episode's files go, and which files in that folder must you never delete?
- In the master template, the display work and the Wi-Fi work both live in `proj_cm55`. So what does `proj_cm33_ns` do, and what would you gain and lose by moving the network work to the other core?
- `make build` succeeds but `make program` cannot find the board. What should you check first?

## References

- [Master template README (in Thai)](https://github.com/tesaiot/developer-hub/blob/082fd3e76595b62cfdb213499a093c233dbb4b53/README.md) · commit `082fd3e`
- [TESAIoT Developer Hub](https://dev.tesaiot.dev/) · [tesaiot/developer-hub](https://github.com/tesaiot/developer-hub)
- [TESAIoT Dev Kit SDK](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk)
