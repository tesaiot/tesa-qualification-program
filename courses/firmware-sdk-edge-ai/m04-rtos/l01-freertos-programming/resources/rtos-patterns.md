# Cheatsheet — FreeRTOS Patterns (M04)

**Course 1 · Module 4**

ใช้ควบคู่บทเรียนและแล็บ — snippet จาก TESA Firmware SDK + FreeRTOS API

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [← Table of Contents](../../../README.md)

---

## Boot path

```c
(void)cm55_initialize(system_ready_callback, NULL);
(void)cm55_start_scheduler(); /* does not return */
```

อย่าเรียก `vTaskStartScheduler()` ซ้ำถ้าใช้ `cm55_start_scheduler()` แล้ว

---

## Task + delay

```c
xTaskCreate(fn, "NAME", stack_words, NULL, tskIDLE_PRIORITY + 1U, &handle);
vTaskDelay(pdMS_TO_TICKS(500));
```

| Do | Don't |
|---|---|
| ลูป `for (;;)` ใน task คาบ | busy-wait นานโดยไม่ delay |
| ตรวจ `pdPASS` ตอน create | ละเลย heap หมด |

Docs: [xTaskCreate](https://www.freertos.org/a00125.html) · [vTaskDelay](https://www.freertos.org/a00127.html)

---

## Queue

```c
q = xQueueCreate(8, sizeof(item_t));
xQueueSend(q, &item, 0);
xQueueReceive(q, &item, portMAX_DELAY);
/* ISR: */ xQueueSendFromISR(q, &item, &woken); portYIELD_FROM_ISR(woken);
```

RAM ≈ `depth × sizeof(item)` (+ overhead)

Docs: [xQueueCreate](https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/01-xQueueCreate)

---

## Mutex / binary semaphore

```c
mtx = xSemaphoreCreateMutex();
xSemaphoreTake(mtx, portMAX_DELAY);
xSemaphoreGive(mtx);

sem = xSemaphoreCreateBinary();
xSemaphoreTake(sem, pdMS_TO_TICKS(1000));
xSemaphoreGive(sem); /* or GiveFromISR */
```

I²C ในหลักสูตร:

```c
cm55_i2c_manager_i2c_lock();
/* ... */
cm55_i2c_manager_i2c_unlock();
```

Docs: [Mutexes](https://www.freertos.org/Real-time-embedded-RTOS-mutexes.html)

---

## Event group

```c
eg = xEventGroupCreate();
xEventGroupSetBits(eg, BIT0);
xEventGroupWaitBits(eg, BIT0, pdFALSE, pdFALSE, ticks);
```

Docs: [Event Groups](https://www.freertos.org/FreeRTOS-Event-Groups.html)

---

## ISR rules

| Allowed (สั้น ๆ) | Forbidden |
|---|---|
| `xQueueSendFromISR` | `printf` / I²C / `vTaskDelay` |
| `xSemaphoreGiveFromISR` | `xSemaphoreTake` แบบ block |
| `portYIELD_FROM_ISR` | งานยาวใน ISR |

---

## Lab API log

| งาน | API ที่ใช้จริง |
|---|---|
| Create blink tasks | |
| Delay | |
| Queue send/receive | |
| Mutex / I²C lock | |
| Event group / binary sem | |

---

## Portals

| แหล่ง | ลิงก์ |
|---|---|
| Examples | [TESAIoT Developer Hub](https://dev.tesaiot.dev/) |
| Host | [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) |
| Lab pack | [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) |

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [← Table of Contents](../../../README.md)
