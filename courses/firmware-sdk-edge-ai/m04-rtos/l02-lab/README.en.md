---
id: fw-sdk.m04.l02
lang: en
title:
  th: 'แล็บ: เฟิร์มแวร์หลาย task ด้วย FreeRTOS'
  en: 'Lab: Multi-Task Firmware with FreeRTOS'
summary:
  th: สร้างสอง task คาบต่างกัน ส่งเหตุการณ์ปุ่มผ่าน queue ป้องกันบัสร่วมด้วย mutex แล้วเขียนโน้ตเรื่อง timing
  en: Build two tasks at different periods, send button events through a queue, guard a shared bus with a mutex and write timing notes.
level: L3
time_min:
  lab: 210
hardware:
  emulator: false
  boards:
  - devkit
  - eva-kit
prerequisites:
- fw-sdk.m04.l01
objectives:
- th: รันสอง task ที่กระพริบ LED ด้วยคาบเวลา 500 ms และ 200 ms โดยไม่ busy-wait
  en: Run two tasks that blink LEDs at 500 ms and 200 ms without busy-waiting.
- th: ส่งเหตุการณ์ปุ่มผ่าน queue ไปยัง task ที่พิมพ์ UART
  en: Send button events through a queue to a task that prints to UART.
- th: ป้องกันทรัพยากรที่ใช้ร่วมด้วย mutex หรือ API ล็อกบัสของโปรเจกต์
  en: Protect a shared resource with a mutex or the project's bus-lock API.
develops:
- skill: rtos.freertos
  to: 2
- skill: rtos.basics
  to: 2
assesses:
- skill: rtos.freertos
  level: 2
  evidence: README.md#submit-checklist
context:
  platform: psoc-edge-e84
  lang: c
  ide: modustoolbox-vscode
  firmware: tesaiot-bitstream (HEX; source not public yet)
status: alpha
translation: done
source_sha256: 126a6a87ddbedd2f7ca91026a42679f06c2b8ad75b44d59f262a75a43d92e3b9
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M04/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M04 — Multi-Task Firmware with FreeRTOS

**Course 1 · Module 4**
**Type:** Hands-on lab (create tasks, then add queue / mutex)
**Suggested time:** 2.5–3.5 hours

Read first: [Lesson](../l01-freertos-programming/README.md) · [Cheatsheet](../l01-freertos-programming/resources/rtos-patterns.md) · [← Table of Contents](../../README.md) · [← M03](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md) · [M05 →](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md)

> **Note:** the snippets in this lab use the API of the TESAIoT Bitstream firmware, which is not yet open source. See detail and equivalent examples in the public SDK in the note at the top of the lesson [Multi-task Firmware with FreeRTOS](../l01-freertos-programming/README.md)

### Useful references during the lab

| Document | Use when |
|---|---|
| [Lesson snippets](../l01-freertos-programming/README.md) | `xTaskCreate`, queue, mutex, event group |
| [M03 Driver APIs](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md) | LED / button / UART / I²C |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | System / Real-Time examples |
| [FreeRTOS xTaskCreate](https://www.freertos.org/a00125.html) | Checking the parameters |

---

## Lab Goals

Once complete, you will:

- Have created at least **two tasks** running at different periods
- Use **`vTaskDelay(pdMS_TO_TICKS(...))`** instead of busy-waiting
- Send an event through at least one **queue** path
- Use a **mutex** (or `cm55_i2c_manager_i2c_lock`) when sharing a resource
- (Recommended) use an **event group** or a binary semaphore as a ready flag

---

## Prerequisites

- [ ] Have passed Lab M03 (at least GPIO + UART)
- [ ] An example project that can call `cm55_initialize` / `cm55_start_scheduler`
- [ ] Know the point at which the project allows `xTaskCreate` (after init / in a callback)

> Don't call `vTaskStartScheduler()` yourself again if the project already uses `cm55_start_scheduler()`

---

## Lab A — Two blink rates (required)

1. Create a task `LAB_BLINK_SLOW` that blinks an LED at a **500 ms** period
2. Create a task `LAB_BLINK_FAST` that blinks another LED (or switches colour) at a **200 ms** period
3. Use slightly different priorities (such as idle+1 and idle+2) and observe the behaviour

```c
led_controller_toggle(LED_RED);
vTaskDelay(pdMS_TO_TICKS(500));
```

**Pass when:** you see two distinct rhythms on the board, with no long `while` busy-delay inside a single task

---

## Lab B — Button → Queue → UART task (required)

1. Create a short-message queue (`xQueueCreate`)
2. Create a task that pulls from the queue and calls `printf` / `LOG_INFO`
3. In `cm55_button_on_pressed` (or wherever the button event fires), `xQueueSend` a message, such as `btn\r\n`

**Pass when:** pressing the button shows a message on serial, while the blink task from Lab A keeps running

---

## Lab C — Shared resource lock (required)

Choose at least one:

### C1 Your own mutex

- Create with `xSemaphoreCreateMutex`
- Have two tasks share printing, or share a status variable, under Take/Give

### C2 The SDK's I²C lock

- Read a sensor in one task
- Wrap it with `cm55_i2c_manager_i2c_lock` / `unlock` (or the lock API your project has)

**Pass when:** you can explain why locking is needed, and demonstrate there is no random bus contention breaking things

---

## Lab D — Ready flag (recommended)

1. Create with `xEventGroupCreate`
2. Have a setup task set the "READY" bit once init is done
3. Have another task call `xEventGroupWaitBits` before starting its work

Or use a binary semaphore as a "now ready" signal instead.

**Pass when:** the waiting task does not start its work before the ready signal

---

## Lab E — Timing notes (short write-up)

Answer briefly (5–8 lines):

1. What would you risk by putting `printf` inside an ISR?
2. What would happen to the system if the heaviest task's priority stayed at maximum all the time?
3. How does a queue's `depth × sizeof(item)` affect RAM?

---

## Troubleshooting

| Symptom | Approach |
|---|---|
| `xTaskCreate` returns something other than `pdPASS` | The heap is exhausted · the stack is too large · called before the system is ready |
| The task doesn't run | `cm55_start_scheduler` not called yet · a priority/name clash · the task's loop ended and wasn't recreated |
| A HardFault when pressing the button | A blocking API is inside an ISR · check for `FromISR` |
| UART output is garbled / hangs | Missing a mutex / recursive lock around printf |
| Random I²C NACKs | Missing a bus lock when several tasks use it |

---

## Submit checklist

- [ ] Lab A passed
- [ ] Lab B passed
- [ ] Lab C passed
- [ ] (Recommended) Lab D
- [ ] Lab E fully answered
- [ ] The API table in [rtos-patterns.md](../l01-freertos-programming/resources/rtos-patterns.md) filled in

[Lesson](../l01-freertos-programming/README.md) · [Cheatsheet](../l01-freertos-programming/resources/rtos-patterns.md) · [Table of Contents](../../README.md) · [M05 →](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md)
