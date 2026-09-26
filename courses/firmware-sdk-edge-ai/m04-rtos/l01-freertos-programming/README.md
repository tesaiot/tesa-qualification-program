---
id: fw-sdk.m04.l01
lang: th
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
slides: slides.md
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M04/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M04 — RTOS Firmware Programming

**Course 1 · Module 4**  
**Suggested time:** ประมาณ 3.5–4 ชั่วโมง (อ่าน + lab หลาย task บนบอร์ด)  
**Format:** บทเรียนเชิงปฏิบัติ — สร้างและประสาน **FreeRTOS tasks** ร่วมกับ TESA Firmware SDK

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/rtos-patterns.md) · [← Table of Contents](../../README.md) · [← M03](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md) · [M05 →](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md)

> **หมายเหตุ: โค้ดในบทนี้เขียนสำหรับเฟิร์มแวร์ชุดใด** (ตรวจสอบเมื่อ 26 ก.ย. 2026)
>
> โค้ด C ในบทนี้เรียก API ของเฟิร์มแวร์ **TESAIoT Bitstream** ที่ต้นฉบับเรียกว่า “TESA Firmware SDK” ซึ่งเผยแพร่เป็นไฟล์ HEX สำเร็จรูป (`tesaiot-bitstream-<version>.hex`) คู่กับ Bitstream Studio ในแพ็กแล็บ [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/tree/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/hex) **ซอร์สโค้ดของเฟิร์มแวร์ชุดนี้ยังไม่เปิดเผยต่อสาธารณะ** ฟังก์ชันอย่าง `cm55_initialize`, `cm55_start_scheduler`, `led_controller_toggle`, `cm55_button_on_pressed`, `cm55_i2c_manager_i2c_lock` จึงยังไม่มี header ให้เปิดดูหรือนำไป build เอง ให้อ่าน snippet เป็นแนวคิดและลำดับการเรียกใช้ ส่วนการเรียก FreeRTOS และ Infineon PDL (เช่น `xTaskCreate`, `vTaskDelay`, `Cy_GPIO_*`) เป็น API สาธารณะตามปกติ
>
> ถ้าต้องการโค้ดที่อ่านและ build ได้จากซอร์สเปิด ให้ดู [tesaiot-pse84-devkit-sdk](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) (Apache-2.0) ซึ่งเป็น**คนละโค้ดเบสและตั้งชื่อ API ต่างกัน** ตัวอย่างที่ตรวจแล้วว่าทำงานเรื่องเดียวกับบทนี้ (commit `ef72c1b`):
>
> - [`proj_cm55/main.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/main.c#L225-L238) และ [`proj_cm33_ns/main.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/main.c#L309-L391) — สร้าง task ด้วย `xTaskCreate` แล้วเรียก `vTaskStartScheduler()` จาก `main` โดยตรง (ไม่มี wrapper `cm55_start_scheduler`)
> - [`proj_cm33_ns/examples/sensors/05_auto_push_task.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/05_auto_push_task.c) — task FreeRTOS ที่อ่านเซ็นเซอร์เป็นคาบภายใต้ mutex และปรับอัตราได้
> - [`proj_cm33_ns/examples/sensors/02_read_imu.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/02_read_imu.c) — ล็อกบัสหนึ่งครั้งต่อหนึ่งตัวอย่าง (`sensor_i2c_lock` / `sensor_i2c_unlock`)

---

## เป้าหมาย (Learning Outcomes)

เมื่อเรียนจบ คุณควรทำได้ดังนี้:

1. อธิบายบทบาทของ **RTOS** และการแบ่งงานเป็น **Task**  
2. ออกแบบ Task พร้อม **stack**, **priority** และเข้าใจ scheduler เบื้องต้น  
3. ใช้ **Queue, Mutex, Binary Semaphore, Event Group** เพื่อสื่อสารและป้องกัน race condition  
4. คำนึงถึง **timing** และข้อห้ามใน ISR / tick hook  
5. สร้างระบบหลาย task ที่ทำงานร่วมกับ Driver API จาก [M03](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md)  
6. ทำแบบฝึกปฏิบัติ multi-task บนบอร์ดจริง  

> **เกี่ยวกับ snippet ในบทนี้**  
> ตัวอย่างภาษา C ดึงจาก **TESA Firmware SDK** (FreeRTOS บน CM55) แล้วนำเสนอเป็น snippet เท่านั้น  
> ดูตัวอย่างเพิ่มบน **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** (Domain: **System** / **Embedded** / **Real-Time**)

### Read alongside this chapter

| เอกสาร | ใช้เมื่อ |
|---|---|
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | ตัวอย่าง multi-task / system ของหลักสูตร |
| [FreeRTOS — xTaskCreate](https://www.freertos.org/a00125.html) | สร้าง task |
| [FreeRTOS — vTaskDelay](https://www.freertos.org/a00127.html) | หน่วงแบบให้ CPU ว่าง |
| [FreeRTOS — xQueueCreate](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/01-xQueueCreate) | คิวส่งข้อมูลระหว่าง task |
| [FreeRTOS — Queues overview](https://www.freertos.org/Embedded-RTOS-Queues.html) | แนวคิด copy-by-value |
| [FreeRTOS — Mutex / Semaphore](https://www.freertos.org/Real-time-embedded-RTOS-mutexes.html) | ล็อกทรัพยากรร่วม |
| [FreeRTOS — Event Groups](https://www.freertos.org/FreeRTOS-Event-Groups.html) | ธงสถานะระหว่าง task |
| [M03 — GPIO and Peripherals](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md) | `led_controller_*`, `cm55_button_*`, I²C lock |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | HEX / Flasher เมื่อใช้แพ็กแล็บ |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | ดู telemetry หลังมีหลาย task ส่งข้อมูล (เสริม) |

---

## 1. Why RTOS for Edge Products

ใน M03 โค้ดมักอยู่ในลูปเดียว: อ่านปุ่ม → UART → ADC  
เมื่อระบบโต (เซ็นเซอร์หลายตัว, connectivity, UI, Edge AI) ลูปเดียวทำให้:

- งานช้าไปบล็อกงานที่ต้องตอบสนองเร็ว  
- ยากต่อการแยกหน้าที่และทดสอบ  

**RTOS (Real-Time Operating System)** ในแพลตฟอร์มหลักสูตรนี้คือ **FreeRTOS** — สร้างหลาย Task ที่สลับกันทำงานตามลำดับความสำคัญ

| แนวคิด | ความหมายสั้น |
|---|---|
| **Task** | ฟังก์ชันที่รันอิสระ มี stack ของตัวเอง |
| **Scheduler** | เลือก task ที่จะได้ CPU |
| **Priority** | ตัวเลขสูงกว่า = สำคัญกว่า (ใน FreeRTOS) |
| **Blocking** | task รอคิว/หน่วง → ปล่อย CPU ให้ task อื่น |

> **Key phrase**  
> แยกงานตาม *ความรับผิดชอบและจังหวะเวลา* — ไม่ใช่แยกไฟล์ C อย่างเดียว

---

## 2. How the Firmware Starts FreeRTOS

แอปมาตรฐานบน CM55 **ไม่เรียก** `vTaskStartScheduler()` จาก `main` โดยตรง แต่ใช้:

```c
#include "cm55_init.h"

int main(void)
{
    (void)cm55_initialize(system_ready_callback, NULL);
    (void)cm55_start_scheduler(); /* wraps vTaskStartScheduler(); does not return */
}
```

| ขั้นตอน | ความหมาย |
|---|---|
| `cm55_initialize(...)` | bring-up + สร้าง task เริ่มต้นบน main stack (ยังไม่รัน scheduler) |
| callback / โค้ดหลัง init | ลงทะเบียน hook, สร้าง task เพิ่มได้ตามแบบโปรเจกต์ |
| `cm55_start_scheduler()` | เริ่ม scheduler — โดยปกติไม่กลับมาที่ `main` |

ในแล็บ: สร้าง task ของคุณในจุดที่โปรเจกต์กำหนด (หลัง init / ใน callback) แล้วให้ scheduler ทำงาน

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
        /* create failed — ตรวจ heap / stack / priority */
    }
}
```

| พารามิเตอร์ `xTaskCreate` | ความหมาย |
|---|---|
| ฟังก์ชัน task | ต้องลูปตลอด หรือลบตัวเองเมื่อจบงาน one-shot |
| ชื่อ | สตริงสั้น ๆ สำหรับ debug |
| stack (words) | เล็กเกินไป → overflow; ใหญ่เกินไป → กิน RAM |
| priority | สูงกว่า = แย่ง CPU ได้ก่อนเมื่อพร้อมรัน |
| handle | เก็บไว้ถ้าจะลบ/แจ้ง task ทีหลัง |

อ่านเพิ่ม: [xTaskCreate](https://www.freertos.org/a00125.html) · [vTaskDelay](https://www.freertos.org/a00127.html)

### 3.2 Two tasks, two rates

```c
/* Task A: 250 ms — “fast heartbeat” */
vTaskDelay(pdMS_TO_TICKS(250));

/* Task B: 500 ms — LED blink */
vTaskDelay(pdMS_TO_TICKS(500));
```

สังเกตว่าทั้งคู่รัน “พร้อมกันในมุมมองระบบ” โดยไม่ busy-wait ในลูปเดียว

### 3.3 Priority rules of thumb (course)

| แนวทาง | ตัวอย่างในแล็บ |
|---|---|
| งาน background / กระพริบ | `tskIDLE_PRIORITY + 1` |
| งานตอบสนองปุ่ม / UI เบา | สูงกว่า blink เล็กน้อย |
| งานวิกฤต (IPC / watchdog path ในผลิตภัณฑ์) | สูงกว่า — **อย่ายกทุกอย่างขึ้นสูงสุด** |

ในผลิตภัณฑ์จริง priority สูงเกินไปของงานหนักอาจ starve งานสำคัญอื่น — ในแล็บให้เปลี่ยนทีละน้อยแล้วสังเกตอาการ

---

## 4. Queues — Pass Data Between Tasks

คิวของ FreeRTOS **คัดลอกข้อมูลตามขนาด item** ไม่ใช่ส่ง pointer โดยอัตโนมัติ  
อ่านภาพรวม: [Queues](https://www.freertos.org/Embedded-RTOS-Queues.html) · [xQueueCreate](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/01-xQueueCreate)

### 4.1 Producer / consumer (UART log drain pattern)

แนวทางใน SDK: อย่า `printf` จาก ISR — **enqueue** แล้วให้ task ดึงไปพิมพ์

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
    /* คัดลอกแบบจำกัดความยาว — ตัวอย่างแล็บ */
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

ปุ่มใน SDK (`cm55_button_*`) ใช้แนว ISR/bridge + queue ในพาธ IRQ — แล็บอาจใช้ callback ของปุ่มใน task context ก่อน แล้วค่อยฝึก `FromISR` เมื่อพร้อม

---

## 5. Mutex and Semaphores — Protect Shared Resources

### 5.1 Mutex around a shared bus (I²C)

จาก [M03](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md): บัส I²C ร่วมต้องล็อก

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

ใน SDK จริง การล็อก I²C บางจุดใช้รูปแบบ **poll + `vTaskDelay(1)`** แทน `portMAX_DELAY` เพื่อเลี่ยงสถานการณ์ scheduler ยังไม่พร้อม — ในแล็บพื้นฐาน `Take(... portMAX_DELAY)` ใช้ได้เมื่อรู้ว่า scheduler รันแล้ว

เรียกผ่าน wrapper ของหลักสูตรเมื่อมี:

```c
cm55_i2c_manager_i2c_lock();
/* sensor / HAL transfer */
cm55_i2c_manager_i2c_unlock();
```

UART ของผลิตภัณฑ์ใช้ **recursive mutex** สำหรับ serialize `printf` — รู้ไว้ว่า mutex ธรรมดา vs recursive คนละกรณี

อ่านเพิ่ม: [Mutexes](https://www.freertos.org/Real-time-embedded-RTOS-mutexes.html)

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

ใช้เมื่อต้องการ “มีสัญญาณแล้ว” ไม่ใช่ส่ง payload ใหญ่ — ถ้าต้องส่งข้อมูล ให้ใช้ **queue**

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

ใน SDK ใช้แนวนี้กับธง “I²C พร้อมแล้ว” ก่อนให้เซ็นเซอร์เริ่มทำงาน  
อ่านเพิ่ม: [Event Groups](https://www.freertos.org/FreeRTOS-Event-Groups.html)

---

## 7. Timing Constraints and Real-Time Behavior

| หัวข้อ | แนวปฏิบัติในหลักสูตร |
|---|---|
| Period ของ task | ใช้ `vTaskDelay` / `vTaskDelayUntil` ตามแบบที่โปรเจกต์ใช้ |
| งานยาวใน priority สูง | แยกเป็น task ต่ำกว่า หรือหั่นงานเป็นชิ้นสั้น ๆ |
| ISR | สั้น ๆ · ไม่ `printf` · ไม่ I²C · ไม่ mutex แบบ blocking |
| Tick hook | ห้ามเรียก driver ที่ต้องล็อกหรือ I/O ช้า |
| Heap / queue depth | `depth × sizeof(item)` กิน RAM — สร้างคิวใหญ่เกินอาจได้ `NULL` |

> **ห้ามใน ISR / tick hook**  
> `xSemaphoreTake` (blocking), `vTaskDelay`, I²C, `printf`  
> ใช้ `*FromISR` แล้วให้ task ทำงานหนักแทน

---

## 8. Worked Multi-Task Scenario

โจทย์: กระพริบ LED คาบคงที่ + กดปุ่มแล้วส่งข้อความเข้าคิว log + task อื่นพิมพ์ UART

```text
blink_task          → led_controller_toggle + vTaskDelay
button callback     → xQueueSend(log_q, "btn\r\n")
log_drain_task      → xQueueReceive + printf
```

ต่อยอด M03 Lab D: ADC อ่านใน task ช้า + PWM ปรับใน task เดียวกันหรือส่งค่าผ่านคิว

---

## 9. Module Summary

1. หลักสูตรใช้ **FreeRTOS** — เริ่มผ่าน `cm55_initialize` / `cm55_start_scheduler`  
2. **Task + delay** เป็นรากฐาน; แยกจังหวะงานด้วยหลาย task  
3. **Queue** ส่งข้อมูล; **Mutex** ล็อกทรัพยากร; **Binary semaphore / Event group** ส่งสัญญาณสถานะ  
4. เคารพกฎ ISR และ priority เพื่อไม่ให้ระบบ “ค้างเงียบ” หรือ starve  
5. ต่อไป **M05** จะใช้หลาย task กับ pipeline เซ็นเซอร์ / Edge AI  

### Next Steps

1. ทำแบบฝึก: [Lab](../l02-lab/README.md)  
2. เก็บแผ่นสรุป: [Cheatsheet](resources/rtos-patterns.md)  
3. เมื่อพร้อม ไปต่อ **M05 — Sensor Data and Edge AI Preparation** ([บทเรียน M05](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md))

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

## เช็กความเข้าใจ

คำถามสั้นสามข้อใน [quiz.yaml](quiz.yaml) ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อน แล้วค่อยเทียบกับเฉลยและคำอธิบายในไฟล์

## แล็บ

ลงมือต่อที่ [แล็บ: เฟิร์มแวร์หลาย task ด้วย FreeRTOS](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/rtos-patterns.md) · [← Table of Contents](../../README.md) · [← M03](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md) · [M05 →](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md)

## ตัวอย่างบน TESAIoT Developer Hub

ลองของจริงบน TESAIoT Dev Kit: เปิดตัวอย่างบน Developer Hub เพื่ออ่านโค้ด ดาวน์โหลด หรือ flash เฟิร์มแวร์สำเร็จรูป

- [EP07 — Final WiFi Manager](https://dev.tesaiot.dev/?example=developer-hub--hmi_ep07_final_wifi_manager&q=hmi_ep07_final_wifi_manager) — รวม scan + profile + connect + auto-retry + ping watchdog เป็น WiFi manager สมบูรณ์ พร้อม state machine บนหน้าจอและ auto-connect จาก profile
- [EP07 — SensorHub Final](https://dev.tesaiot.dev/?example=developer-hub--int_ep07_sensorhub_final&q=int_ep07_sensorhub_final) — โปรเจกต์ปิดคอร์ส: แดชบอร์ดรวมเซนเซอร์ทั้ง 4 ตัว (DPS368, SHT4x, BMI270, BMM350) + ไมโครโฟน PDM สเตอริโอ บนจอเดียว
