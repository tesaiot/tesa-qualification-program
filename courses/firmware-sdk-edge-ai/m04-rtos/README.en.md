
# Module 4 — RTOS Firmware Programming

*RTOS Firmware Programming* · [TESA Firmware SDK for Edge AI](../README.md) course

## Objectives

Split work by responsibility and timing with FreeRTOS: tasks, priority, queues, mutexes, semaphores and event groups, along with the rules of an ISR.

## Lessons

| # | Lesson | Content |
|---|---|---|
| 1 | [Multi-task firmware with FreeRTOS](l01-freertos-programming/README.md) | Creating a periodic task, choosing a priority, passing data with a queue, protecting a bus with a mutex, signalling with a semaphore/event group, and respecting the rules of an ISR |
| 2 | [Lab: multi-task firmware with FreeRTOS](l02-lab/README.md) | Creating two tasks with different periods, passing a button event through a queue, protecting a shared bus with a mutex, then writing notes about timing |

Approximate time per the original: about 3.5–4 hours (lessons) + a 2.5–3.5 hour lab.

Accompanying sheets and templates (in the `resources/` folder of lesson 1):

- [rtos-patterns.md](l01-freertos-programming/resources/rtos-patterns.md)

> The C code in this module uses the API of the TESAIoT Bitstream firmware, which is not yet open source. Read the note at the top of the [lesson](l01-freertos-programming/README.md) before you start.

## Checkpoint

Before moving to the next module, check that you can do the following:

- [ ] Two tasks blink an LED at different periods with no busy-waiting
- [ ] A button event travels through a queue to a task that prints over UART
- [ ] A shared resource is protected with a mutex or a bus-locking API
- [ ] Lab E's timing questions are all answered

[← Module 3](../m03-gpio-peripherals/README.md) · [Course page](../README.md) · [Module 5 →](../m05-sensor-data/README.md)
