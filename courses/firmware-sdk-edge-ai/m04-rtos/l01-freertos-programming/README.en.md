---
id: fw-sdk.m04.l01
lang: en
title:
  th: เฟิร์มแวร์หลาย task ด้วย FreeRTOS
  en: Multi-task Firmware with FreeRTOS
summary:
  th: สร้าง task ที่มีคาบเวลา เลือก priority ส่งข้อมูลด้วย queue ป้องกันบัสด้วย mutex ส่งสัญญาณด้วย semaphore/event group และเคารพกฎของ ISR
  en: Create periodic tasks, choose priorities, pass data with queues, guard a bus with a mutex, signal with semaphores/event groups and respect ISR rules.
level: L3
time_min:
  concept: 45
  practise: 20
  check: 10
hardware:
  emulator: false
  boards:
  - devkit
  - eva-kit
prerequisites:
- fw-sdk.m03.l02
objectives:
- th: สร้าง task แบบมีคาบเวลาด้วย `vTaskDelay` / `vTaskDelayUntil` แทน busy-wait และกำหนด priority ตามแนวทางของบทเรียน
  en: Create periodic tasks with `vTaskDelay` / `vTaskDelayUntil` instead of busy-waiting, and set priorities following the lesson's rules of thumb.
- th: เลือกกลไก FreeRTOS (queue, mutex, binary semaphore, event group) ให้ตรงกับโจทย์ส่งข้อมูล ล็อกทรัพยากร หรือส่งสัญญาณสถานะ
  en: Choose the FreeRTOS mechanism (queue, mutex, binary semaphore, event group) that fits passing data, locking a resource or signalling state.
- th: ระบุสิ่งที่ห้ามทำใน ISR / tick hook และใช้ฟังก์ชัน `*FromISR` แทนได้ถูกต้อง
  en: Identify what must not happen in an ISR / tick hook and use the `*FromISR` calls instead.
develops:
- skill: rtos.basics
  to: 2
- skill: rtos.freertos
  to: 2
- skill: mcu.interrupts
  to: 2
context:
  platform: psoc-edge-e84
  lang: c
  ide: modustoolbox-vscode
  firmware: tesaiot-bitstream (HEX; source not public yet)
status: alpha
translation: done
source_sha256: 75e08ee5710d6d00ca904660d7a5f74ae73bf592e160f2a74121720ccfb04b74
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M04/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M04 — RTOS Firmware Programming

**Course 1 · Module 4**
**Suggested time:** about 3.5–4 hours (reading + a multi-task lab on the board)
**Format:** a hands-on lesson — creating and coordinating **FreeRTOS tasks** alongside the TESA Firmware SDK

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/rtos-patterns.md) · [← Table of Contents](../../README.md) · [← M03](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md) · [M05 →](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md)

> **Note: which firmware the code in this lesson is written for** (checked on 2026-09-26)
>
> The C code in this lesson calls the API of the **TESAIoT Bitstream** firmware, called "TESA Firmware SDK" in the original, which is published as a ready-made HEX file (`tesaiot-bitstream-<version>.hex`) alongside Bitstream Studio in the [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/tree/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/hex) lab pack. **The source code of this firmware is not yet public.** Functions such as `cm55_initialize`, `cm55_start_scheduler`, `led_controller_toggle`, `cm55_button_on_pressed` and `cm55_i2c_manager_i2c_lock` therefore have no header you can open or build yourself. Read the snippets as concepts and a calling order. The calls to FreeRTOS and the Infineon PDL (such as `xTaskCreate`, `vTaskDelay`, `Cy_GPIO_*`) are ordinary public APIs.
>
> If you want code you can read and build from open source, see [tesaiot-pse84-devkit-sdk](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) (Apache-2.0), which is a **different codebase with different API names**. Examples already checked to do the same job as this lesson (commit `ef72c1b`):
>
> - [`proj_cm55/main.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/main.c#L225-L238) and [`proj_cm33_ns/main.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/main.c#L309-L391) — create a task with `xTaskCreate`, then call `vTaskStartScheduler()` directly from `main` (no `cm55_start_scheduler` wrapper)
> - [`proj_cm33_ns/examples/sensors/05_auto_push_task.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/05_auto_push_task.c) — a FreeRTOS task that reads a sensor periodically under a mutex, with an adjustable rate
> - [`proj_cm33_ns/examples/sensors/02_read_imu.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/02_read_imu.c) — locking the bus once per sample (`sensor_i2c_lock` / `sensor_i2c_unlock`)

---

## Objectives (Learning Outcomes)

By the end of this lesson you should be able to:

1. Explain the role of an **RTOS** and splitting work into **Tasks**
2. Design a Task with a **stack**, a **priority**, and a basic understanding of the scheduler
3. Use **Queues, Mutexes, Binary Semaphores, Event Groups** to communicate and prevent race conditions
4. Consider **timing** and the restrictions inside an ISR / tick hook
5. Build a multi-task system working with the Driver API from [M03](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md)
6. Do a multi-task hands-on exercise on the real board

> **About the snippets in this lesson**
> The C examples are drawn from the **TESA Firmware SDK** (FreeRTOS on the CM55) and presented purely as snippets.
> See more examples on the **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** (Domain: **System** / **Embedded** / **Real-Time**)

### Read alongside this chapter

| Document | Use when |
|---|---|
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | The course's multi-task / system examples |
| [FreeRTOS — xTaskCreate](https://www.freertos.org/a00125.html) | Creating a task |
| [FreeRTOS — vTaskDelay](https://www.freertos.org/a00127.html) | Delaying while freeing the CPU |
| [FreeRTOS — xQueueCreate](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/01-xQueueCreate) | A queue for passing data between tasks |
| [FreeRTOS — Queues overview](https://www.freertos.org/Embedded-RTOS-Queues.html) | The copy-by-value concept |
| [FreeRTOS — Mutex / Semaphore](https://www.freertos.org/Real-time-embedded-RTOS-mutexes.html) | Locking a shared resource |
| [FreeRTOS — Event Groups](https://www.freertos.org/FreeRTOS-Event-Groups.html) | Status flags between tasks |
| [M03 — GPIO and Peripherals](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md) | `led_controller_*`, `cm55_button_*`, the I²C lock |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | HEX / Flasher, when using the lab pack |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | Watching telemetry once several tasks send data (extra) |

---

## 1. Why RTOS for Edge Products

In M03, the code usually sat in a single loop: read a button → UART → ADC.
As the system grows (several sensors, connectivity, UI, Edge AI), a single loop causes:

- A slow task blocking work that must respond quickly
- Difficulty separating responsibilities and testing them

The **RTOS (Real-Time Operating System)** used on this course's platform is **FreeRTOS** — creating several Tasks that take turns running by priority.

| Concept | Short meaning |
|---|---|
| **Task** | A function that runs independently, with its own stack |
| **Scheduler** | Chooses which task gets the CPU |
| **Priority** | A higher number = more important (in FreeRTOS) |
| **Blocking** | A task waiting on a queue/delay → gives the CPU to another task |

> **Key phrase**
> Split work by *responsibility and timing* — not just by splitting C files.

---

## 2. How the Firmware Starts FreeRTOS

A standard app on the CM55 does **not call** `vTaskStartScheduler()` from `main` directly; it uses:

```c
#include "cm55_init.h"

int main(void)
{
    (void)cm55_initialize(system_ready_callback, NULL);
    (void)cm55_start_scheduler(); /* wraps vTaskStartScheduler(); does not return */
}
```

| Step | Meaning |
|---|---|
| `cm55_initialize(...)` | Bring-up + creating the starting task(s) on the main stack (the scheduler is not running yet) |
| Callback / code after init | Register hooks, create more tasks, per the project's design |
| `cm55_start_scheduler()` | Starts the scheduler — usually does not return to `main` |

In the lab: create your tasks at the point the project designates (after init / in the callback), then let the scheduler run.

---

## 3. Tasks, Stack, Priority, Delay

### 3.1 Create a periodic task (LED heartbeat pattern)

```c
#include "FreeRTOS.h"
#include "task.h"
#include "led_controller.h"

#define BLINK_STACK_WORDS   (256U)
#define BLINK_PERIOD_MS     (500U)

static void blink_task(void *arg)
{
    (void)arg;
    for (;;) {
        led_controller_toggle(LED_RED);
        vTaskDelay(pdMS_TO_TICKS(BLINK_PERIOD_MS));
    }
}

void lab_start_blink_task(void)
{
    TaskHandle_t handle = NULL;
    if (xTaskCreate(blink_task,
                    "LAB_BLINK",
                    BLINK_STACK_WORDS,
                    NULL,
                    tskIDLE_PRIORITY + 1U,
                    &handle) != pdPASS) {
        /* create failed — check the heap / stack / priority */
    }
}
```

| `xTaskCreate` parameter | Meaning |
|---|---|
| The task function | Must loop forever, or delete itself when a one-shot job is done |
| Name | A short string for debugging |
| Stack (words) | Too small → overflow; too large → wastes RAM |
| Priority | Higher = can preempt others sooner once ready to run |
| Handle | Keep it if you'll delete/notify the task later |

Read more: [xTaskCreate](https://www.freertos.org/a00125.html) · [vTaskDelay](https://www.freertos.org/a00127.html)

### 3.2 Two tasks, two rates

```c
/* Task A: 250 ms — "fast heartbeat" */
vTaskDelay(pdMS_TO_TICKS(250));

/* Task B: 500 ms — LED blink */
vTaskDelay(pdMS_TO_TICKS(500));
```

Notice that both run "simultaneously, from the system's point of view", with no busy-waiting in a single loop.

### 3.3 Priority rules of thumb (course)

| Guideline | Example in the lab |
|---|---|
| Background work / blinking | `tskIDLE_PRIORITY + 1` |
| Button response / light UI work | Slightly higher than blink |
| Critical work (an IPC / watchdog path in a real product) | Higher — **don't raise everything to the maximum** |

In a real product, an overly high priority for heavy work can starve other important work — in the lab, change it in small steps and observe the effect.

---

## 4. Queues — Pass Data Between Tasks

A FreeRTOS queue **copies data by the item's size**; it does not automatically pass a pointer.
Read the overview: [Queues](https://www.freertos.org/Embedded-RTOS-Queues.html) · [xQueueCreate](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/01-xQueueCreate)

### 4.1 Producer / consumer (UART log drain pattern)

The SDK's approach: don't `printf` from an ISR — **enqueue** it and let a task pull it and print it.

```c
#include "queue.h"

typedef struct {
    char line[64];
} log_item_t;

static QueueHandle_t s_log_q;

static void log_drain_task(void *arg)
{
    (void)arg;
    log_item_t item;
    for (;;) {
        if (xQueueReceive(s_log_q, &item, portMAX_DELAY) == pdPASS) {
            printf("%s", item.line);
        }
    }
}

void lab_log_queue_init(void)
{
    s_log_q = xQueueCreate(8, sizeof(log_item_t));
    (void)xTaskCreate(log_drain_task, "LAB_LOG", 512, NULL,
                      tskIDLE_PRIORITY + 2U, NULL);
}

void lab_log_post(const char *msg)
{
    log_item_t item = {0};
    /* copy with a length limit — lab example */
    for (size_t i = 0; i + 1U < sizeof(item.line) && msg[i] != '\0'; ++i) {
        item.line[i] = msg[i];
    }
    (void)xQueueSend(s_log_q, &item, 0);
}
```

### 4.2 From ISR to task

```c
BaseType_t xHigherPriorityTaskWoken = pdFALSE;
(void)xQueueSendFromISR(s_log_q, &item, &xHigherPriorityTaskWoken);
portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
```

The SDK's button (`cm55_button_*`) uses an ISR/bridge + queue approach on the IRQ path — the lab may use the button callback in task context first, and practise `FromISR` once ready.

---

## 5. Mutex and Semaphores — Protect Shared Resources

### 5.1 Mutex around a shared bus (I²C)

From [M03](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md): a shared I²C bus must be locked

```c
#include "semphr.h"

static SemaphoreHandle_t s_bus_mtx;

void lab_bus_lock_init(void)
{
    s_bus_mtx = xSemaphoreCreateMutex();
}

void lab_bus_lock(void)
{
    (void)xSemaphoreTake(s_bus_mtx, portMAX_DELAY);
}

void lab_bus_unlock(void)
{
    (void)xSemaphoreGive(s_bus_mtx);
}
```

In the real SDK, some I²C locking uses a **poll + `vTaskDelay(1)`** pattern instead of `portMAX_DELAY`, to avoid a situation where the scheduler isn't ready yet — in a basic lab, `Take(... portMAX_DELAY)` is fine once you know the scheduler is running.

Call it through the course's wrapper when one exists:

```c
cm55_i2c_manager_i2c_lock();
/* sensor / HAL transfer */
cm55_i2c_manager_i2c_unlock();
```

The product's UART uses a **recursive mutex** to serialise `printf` — know that an ordinary mutex vs a recursive one are different cases.

Read more: [Mutexes](https://www.freertos.org/Real-time-embedded-RTOS-mutexes.html)

### 5.2 Binary semaphore — wait for an event

```c
static SemaphoreHandle_t s_evt;

void lab_evt_init(void)
{
    s_evt = xSemaphoreCreateBinary();
}

/* Task waits */
(void)xSemaphoreTake(s_evt, pdMS_TO_TICKS(1000));

/* Other task or ISR signals */
(void)xSemaphoreGive(s_evt);
/* From ISR: xSemaphoreGiveFromISR(s_evt, &xHigherPriorityTaskWoken); */
```

Use this when you need "a signal has occurred", not to send a large payload — if you must send data, use a **queue**.

---

## 6. Event Groups — Ready Flags

```c
#include "event_groups.h"

#define READY_BIT (1U << 0)

static EventGroupHandle_t s_ready;

void lab_ready_init(void)
{
    s_ready = xEventGroupCreate();
}

void lab_mark_ready(void)
{
    (void)xEventGroupSetBits(s_ready, READY_BIT);
}

BaseType_t lab_wait_ready(TickType_t ticks)
{
    EventBits_t bits = xEventGroupWaitBits(
        s_ready, READY_BIT, pdFALSE, pdFALSE, ticks);
    return ((bits & READY_BIT) != 0) ? pdTRUE : pdFALSE;
}
```

The SDK uses this pattern for an "I²C is ready" flag before a sensor starts working.
Read more: [Event Groups](https://www.freertos.org/FreeRTOS-Event-Groups.html)

---

## 7. Timing Constraints and Real-Time Behavior

| Topic | Practice in this course |
|---|---|
| A task's period | Use `vTaskDelay` / `vTaskDelayUntil`, per the project's convention |
| Long work at high priority | Split it into a lower-priority task, or break it into short pieces |
| ISR | Keep it short · no `printf` · no I²C · no blocking mutex |
| Tick hook | Never call a driver that needs a lock, or slow I/O |
| Heap / queue depth | `depth × sizeof(item)` uses RAM — creating too large a queue may return `NULL` |

> **Never in an ISR / tick hook**
> `xSemaphoreTake` (blocking), `vTaskDelay`, I²C, `printf`
> Use `*FromISR` and let a task do the heavy work instead

---

## 8. Worked Multi-Task Scenario

The task: blink an LED at a fixed period + a button press enqueues a message into a log queue + another task prints over UART

```text
blink_task          → led_controller_toggle + vTaskDelay
button callback     → xQueueSend(log_q, "btn\r\n")
log_drain_task      → xQueueReceive + printf
```

Building on M03 Lab D: read the ADC in a slow task + adjust the PWM in the same task, or send the value through a queue

---

## 9. Module Summary

1. The course uses **FreeRTOS** — started through `cm55_initialize` / `cm55_start_scheduler`
2. **Tasks + delay** are the foundation; separate the timing of work with several tasks
3. **Queues** pass data; **Mutexes** lock resources; **Binary semaphores / Event groups** signal state
4. Respect ISR rules and priority so the system doesn't "quietly hang" or starve
5. Next, **M05** will use several tasks with a sensor / Edge AI pipeline

### Next Steps

1. Do the exercise: [Lab](../l02-lab/README.md)
2. Keep the summary sheet: [Cheatsheet](resources/rtos-patterns.md)
3. When ready, continue to **M05 — Sensor Data and Edge AI Preparation** ([M05 lesson](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md))

---

## References and Further Reading

### Course portals

1. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**
2. **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)**
3. **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)**

### FreeRTOS

4. [xTaskCreate](https://www.freertos.org/a00125.html)
5. [vTaskDelay](https://www.freertos.org/a00127.html)
6. [xQueueCreate](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/01-xQueueCreate)
7. [Queues overview](https://www.freertos.org/Embedded-RTOS-Queues.html)
8. [Mutexes](https://www.freertos.org/Real-time-embedded-RTOS-mutexes.html)
9. [Event Groups](https://www.freertos.org/FreeRTOS-Event-Groups.html)
10. [FreeRTOS Kernel Book (GitHub)](https://github.com/FreeRTOS/FreeRTOS-Kernel-Book)

### Prior modules

11. [M03 — GPIO and Basic Peripherals](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md)
12. [M02 — ModusToolbox and VS Code](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md)

---

## Check your understanding

Three short questions in [quiz.yaml](quiz.yaml), one per objective of this lesson. Try answering them yourself first, then compare with the answer key and explanations in the file.

## Lab

Continue hands-on at [Lab: multi-task firmware with FreeRTOS](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/rtos-patterns.md) · [← Table of Contents](../../README.md) · [← M03](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md) · [M05 →](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md)

## Examples on the TESAIoT Developer Hub

Try the real thing on the TESAIoT Dev Kit: open examples on the Developer Hub to read the code, download it, or flash ready-made firmware.

- [EP07 — Final WiFi Manager](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep07_final_wifi_manager&q=hmi_ep07_final_wifi_manager) — combines scan + profile + connect + auto-retry + a ping watchdog into a complete WiFi manager, with a state machine on screen and auto-connect from a saved profile
- [EP07 — SensorHub Final](https://dev.tesaiot.dev/?example=developer-hub--int_ep07_sensorhub_final&q=int_ep07_sensorhub_final) — a course-closing project: a dashboard combining all 4 sensors (DPS368, SHT4x, BMI270, BMM350) + a stereo PDM microphone on a single screen
