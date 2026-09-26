---
id: fw-sdk.m04.l02
lang: th
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
translation: pending
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

> **หมายเหตุ:** snippet ในแล็บนี้ใช้ API ของเฟิร์มแวร์ TESAIoT Bitstream ซึ่งยังไม่เปิดซอร์ส ดูรายละเอียดและตัวอย่างเทียบใน SDK สาธารณะได้ที่หมายเหตุต้นบทเรียน [เฟิร์มแวร์หลาย task ด้วย FreeRTOS](../l01-freertos-programming/README.md)

### Useful references during the lab

| เอกสาร | ใช้เมื่อ |
|---|---|
| [Lesson snippets](../l01-freertos-programming/README.md) | `xTaskCreate`, queue, mutex, event group |
| [M03 Driver APIs](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md) | LED / button / UART / I²C |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | ตัวอย่าง System / Real-Time |
| [FreeRTOS xTaskCreate](https://www.freertos.org/a00125.html) | ตรวจพารามิเตอร์ |

---

## Lab Goals

เมื่อทำครบ คุณจะ:

- สร้างอย่างน้อย **สอง task** ที่รันคาบต่างกัน  
- ใช้ **`vTaskDelay(pdMS_TO_TICKS(...))`** แทน busy-wait  
- ส่งเหตุการณ์ผ่าน **queue** อย่างน้อยหนึ่งเส้นทาง  
- ใช้ **mutex** (หรือ `cm55_i2c_manager_i2c_lock`) เมื่อแชร์ทรัพยากร  
- (แนะนำ) ใช้ **event group** หรือ binary semaphore เป็นธงพร้อม  

---

## Prerequisites

- [ ] ผ่าน Lab M03 (GPIO + UART อย่างน้อย)  
- [ ] โปรเจกต์ตัวอย่างที่เรียก `cm55_initialize` / `cm55_start_scheduler` ได้  
- [ ] รู้จุดที่โปรเจกต์อนุญาตให้ `xTaskCreate` (หลัง init / ใน callback)

> อย่าเรียก `vTaskStartScheduler()` ซ้ำเองถ้าโปรเจกต์ใช้ `cm55_start_scheduler()` แล้ว

---

## Lab A — Two blink rates (required)

1. สร้าง task `LAB_BLINK_SLOW` กระพริบ LED ด้วยคาบ **500 ms**  
2. สร้าง task `LAB_BLINK_FAST` กระพริบ LED อีกดวง (หรือสลับสี) ด้วยคาบ **200 ms**  
3. ใช้ priority คนละค่าเล็กน้อย (เช่น idle+1 และ idle+2) แล้วสังเกตพฤติกรรม  

```c
led_controller_toggle(LED_RED);
vTaskDelay(pdMS_TO_TICKS(500));
```

**Pass when:** เห็นสองจังหวะบนบอร์ดโดยไม่ใช้ `while` busy-delay ยาวใน task เดียว

---

## Lab B — Button → Queue → UART task (required)

1. สร้างคิวข้อความสั้น ๆ (`xQueueCreate`)  
2. สร้าง task ดึงคิวแล้ว `printf` / `LOG_INFO`  
3. ใน `cm55_button_on_pressed` (หรือจุด event ปุ่ม) ให้ `xQueueSend` ข้อความ เช่น `btn\r\n`  

**Pass when:** กดปุ่มแล้วเห็นข้อความบน serial โดย task กระพริบจาก Lab A ยังทำงานต่อ

---

## Lab C — Shared resource lock (required)

เลือกอย่างน้อยหนึ่งข้อ:

### C1 Mutex ของคุณเอง

- สร้าง `xSemaphoreCreateMutex`  
- task สองตัวแชร์การพิมพ์หรือแชร์ตัวแปรสถานะภายใต้ Take/Give  

### C2 I²C lock ของ SDK

- อ่านเซ็นเซอร์ใน task หนึ่ง  
- ห่อด้วย `cm55_i2c_manager_i2c_lock` / `unlock` (หรือ API ล็อกที่โปรเจกต์ของคุณมี)

**Pass when:** อธิบายได้ว่าทำไมต้องล็อก และสาธิตว่าไม่มีการแย่งบัสแบบสุ่มพัง

---

## Lab D — Ready flag (recommended)

1. สร้าง `xEventGroupCreate`  
2. task setup ตั้งบิต “READY” หลัง init เสร็จ  
3. task อื่น `xEventGroupWaitBits` ก่อนเริ่มงาน  

หรือใช้ binary semaphore เป็นสัญญาณ “พร้อมแล้ว” ก็ได้

**Pass when:** task ผู้รอไม่เริ่มงานก่อนสัญญาณพร้อม

---

## Lab E — Timing notes (short write-up)

ตอบสั้น ๆ (5–8 บรรทัด):

1. ถ้าเอา `printf` ใส่ ISR จะเสี่ยงอะไร  
2. ถ้า priority ของ task หนักสูงสุดตลอดเวลา ระบบจะเป็นอย่างไร  
3. `depth × sizeof(item)` ของคิวกระทบ RAM อย่างไร  

---

## Troubleshooting

| อาการ | แนวทาง |
|---|---|
| `xTaskCreate` คืนไม่ใช่ `pdPASS` | heap หมด · stack ใหญ่เกิน · เรียกก่อนระบบพร้อม |
| Task ไม่รัน | ยังไม่ `cm55_start_scheduler` · priority/ชื่อชน · ลูป task จบแล้วไม่ได้สร้างใหม่ |
| HardFault เมื่อกดปุ่ม | มี blocking API ใน ISR · ตรวจ `FromISR` |
| UART ปนกัน / ค้าง | ขาด mutex / recursive lock รอบ printf |
| I²C NACK สุ่ม | ขาด bus lock เมื่อมีหลาย task |

---

## Submit checklist

- [ ] Lab A ผ่าน  
- [ ] Lab B ผ่าน  
- [ ] Lab C ผ่าน  
- [ ] (แนะนำ) Lab D  
- [ ] Lab E ตอบครบ  
- [ ] กรอกตาราง API ใน [rtos-patterns.md](../l01-freertos-programming/resources/rtos-patterns.md)  

[Lesson](../l01-freertos-programming/README.md) · [Cheatsheet](../l01-freertos-programming/resources/rtos-patterns.md) · [Table of Contents](../../README.md) · [M05 →](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md)
