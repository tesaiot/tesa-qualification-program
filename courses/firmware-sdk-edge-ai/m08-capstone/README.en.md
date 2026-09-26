
# Module 8 — Capstone and Course Resources

*Capstone Project and Course Resources* · [TESA Firmware SDK for Edge AI](../README.md) course

## Objectives

Combine the skills from Modules 1–7 into a demonstrable mini-project, and deliver it with a README that others can reproduce.

## Lessons

| # | Lesson | Content |
|---|---|---|
| 1 | [Planning the Capstone and using the course map](l01-capstone-and-resources/README.md) | The Capstone's pass criteria, a map of the course's sheets and APIs, a reference architecture, and three demo scenarios |
| 2 | [Capstone lab: a mini-project](l02-lab/README.md) | Building a mini-project on real hardware that combines sensors, RTOS, and MQTT or BLE, demonstrating three scenarios, and delivering a reproducible README |

Approximate time per the original: flexible — 2–4 hours of lessons + continuing the Capstone on your own.

Accompanying sheets and templates (in the `resources/` folder of lesson 1):

- [capstone-brief.md](l01-capstone-and-resources/resources/capstone-brief.md)
- [course-package.md](l01-capstone-and-resources/resources/course-package.md)

> The C code in this module uses the API of the TESAIoT Bitstream firmware, which is not yet open source. Read the note at the top of the [lesson](l01-capstone-and-resources/README.md) before you start.

## Checkpoint

Before moving to the next module, check that you can do the following:

- [ ] Build + flash works, following your own README
- [ ] At least two FreeRTOS tasks are genuinely running
- [ ] A sensor path + status shown on an LED/UART
- [ ] MQTT or BLE works, either receiving a command or confirming the link
- [ ] All three scenarios are demonstrated, with no secrets in public files

[← Module 7](../m07-ble/README.md) · [Course page](../README.md)
