---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 4.1 — เฟิร์มแวร์หลาย task ด้วย FreeRTOS"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT) · CC BY-NC 4.0"
---
<style>
section { font-size: 24px; padding: 40px 52px; justify-content: flex-start; }
section h1 { font-size: 1.45em; line-height: 1.12; margin: 0 0 .22em; }
section h2 { font-size: 1.12em; margin: .15em 0; }
section h3 { font-size: 1.0em; margin: .12em 0; }
section p, section li { margin: .16em 0; line-height: 1.32; }
section img { max-width: 100%; height: auto; }
section svg { max-height: 250px; }
section table { font-size: .78em; }
section pre { font-size: .70em; line-height: 1.32; background:#0d1117; color:#e6edf3; border:1px solid #30363d; border-radius:8px; padding:12px 16px; box-shadow:0 2px 8px rgba(0,0,0,.25); }
section pre code { white-space: pre-wrap; background:transparent; color:inherit; } section pre .hljs-comment{color:#8b949e;font-style:italic} section pre .hljs-keyword,section pre .hljs-built_in,section pre .hljs-literal{color:#ff7b72} section pre .hljs-string{color:#a5d6ff} section pre .hljs-number{color:#79c0ff} section pre .hljs-title,section pre .hljs-title.function_,section pre .hljs-section{color:#d2a8ff} section pre .hljs-meta{color:#ffa657} section pre .hljs-attr,section pre .hljs-attribute,section pre .hljs-name{color:#7ee787}
section blockquote { margin: .25em 0; font-size: .92em; }
/* two images on a line (parity / 2x2 grids) stay side-by-side and small */
section p > img + img { margin-left: 10px; }
/* scroll-within-slide: dense slides scroll instead of clipping */
section { overflow-y: auto; overflow-x: hidden; }
section::-webkit-scrollbar { width: 11px; }
section::-webkit-scrollbar-thumb { background:#4a90d9; border-radius:6px; }
section::-webkit-scrollbar-track { background:rgba(0,0,0,.06); }
/* image drop-shadow + cover-slide readability (auto) */
section img{filter:drop-shadow(0 3px 12px rgba(0,0,0,.5))}
section.cover *{color:#fff !important}
section.cover h1,section.cover h2,section.cover h3,section.cover p,section.cover li,section.cover strong,section.cover em,section.cover blockquote,section.cover div{text-shadow:0 2px 9px rgba(0,0,0,.92),0 0 3px rgba(0,0,0,.8)}
section.cover div[style*="background:#"],section.cover div[style*="background: #"]{background:rgba(10,14,20,.66) !important;border-color:rgba(120,200,255,.45) !important;max-width:62%}
section.cover blockquote{border-left:4px solid rgba(120,200,255,.6) !important;background:rgba(13,17,23,.55) !important;border-radius:6px;padding:.3em .6em}
section.cover h1,section.cover h2,section.cover h3,section.cover p,section.cover blockquote{max-width:60%}
section.cover div:not(:has(img)){max-width:62%}
section.cover img{filter:none}
</style>

<!-- _class: cover -->

# บทเรียน 4.1 — เฟิร์มแวร์หลาย task ด้วย FreeRTOS

## สร้าง task ที่มีคาบเวลา เลือก priority ส่งข้อมูลด้วย queue ป้องกันบัสด้วย mutex ส่งสัญญาณด้วย semaphore/event group และเคารพกฎของ ISR

**หลักสูตร TESA Firmware SDK สำหรับ Edge AI — โมดูล 4 · บทเรียน 1**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. สร้าง task แบบมีคาบเวลาด้วย `vTaskDelay` / `vTaskDelayUntil` แทน busy-wait และกำหนด priority ตามแนวทางของบทเรียน
2. เลือกกลไก FreeRTOS (queue, mutex, binary semaphore, event group) ให้ตรงกับโจทย์ส่งข้อมูล ล็อกทรัพยากร หรือส่งสัญญาณสถานะ
3. ระบุสิ่งที่ห้ามทำใน ISR / tick hook และใช้ฟังก์ชัน `*FromISR` แทนได้ถูกต้อง

---

## ก่อนเริ่ม

- ผ่าน [บทเรียน 3.2 — แล็บ M03](../../m03-gpio-peripherals/l02-lab/README.md) มาแล้ว
- ใช้บอร์ดจริง: TESAIoT Dev Kit หรือ Eva Kit (KIT_PSE84_EVAL)
- บทเรียนเชิงปฏิบัติ — สร้างและประสาน **FreeRTOS tasks** ร่วมกับ TESA Firmware SDK

> **หมายเหตุสำคัญ (ตรวจสอบเมื่อ 26 ก.ย. 2026):** โค้ด C ในบทนี้เรียก API ของเฟิร์มแวร์ TESAIoT Bitstream ที่ยังไม่เปิดซอร์ส ฟังก์ชันอย่าง `cm55_initialize`, `cm55_start_scheduler`, `led_controller_toggle`, `cm55_button_on_pressed`, `cm55_i2c_manager_i2c_lock` จึงยังไม่มี header ให้เปิดดูหรือ build เอง — อ่านเป็นแนวคิดและลำดับการเรียกใช้ ส่วน FreeRTOS เอง (`xTaskCreate`, `vTaskDelay`, …) เป็น API สาธารณะตามปกติ

---

## ดูของจริงก่อน — ทำไมต้องมี RTOS

ใน โมดูล 3 โค้ดมักอยู่ในลูปเดียว: อ่านปุ่ม → UART → ADC เมื่อระบบโต (เซ็นเซอร์หลายตัว, connectivity, UI, Edge AI) ลูปเดียวทำให้งานช้าไปบล็อกงานที่ต้องตอบสนองเร็ว และยากต่อการแยกหน้าที่และทดสอบ

**RTOS** ในแพลตฟอร์มหลักสูตรนี้คือ **FreeRTOS** — สร้างหลาย Task ที่สลับกันทำงานตามลำดับความสำคัญ

| แนวคิด | ความหมายสั้น |
|---|---|
| Task | ฟังก์ชันที่รันอิสระ มี stack ของตัวเอง |
| Scheduler | เลือก task ที่จะได้ CPU |
| Priority | ตัวเลขสูงกว่า = สำคัญกว่า (ใน FreeRTOS) |
| Blocking | task รอคิว/หน่วง → ปล่อย CPU ให้ task อื่น |

> **Key phrase**: แยกงานตาม *ความรับผิดชอบและจังหวะเวลา* — ไม่ใช่แยกไฟล์ C อย่างเดียว

---

## แนวคิด — เฟิร์มแวร์เริ่ม FreeRTOS อย่างไร

แอปมาตรฐานบน CM55 **ไม่เรียก** `vTaskStartScheduler()` จาก `main` โดยตรง แต่ใช้ wrapper ของ SDK:

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
| `cm55_initialize(...)` | bring-up + สร้าง task เริ่มต้น (ยังไม่รัน scheduler) |
| `cm55_start_scheduler()` | เริ่ม scheduler — โดยปกติไม่กลับมาที่ `main` |

---

## ตัวอย่างสมบูรณ์ — สร้าง task แบบมีคาบเวลา (LED heartbeat)

```c
#include "FreeRTOS.h"
#include "task.h"
#include "led_controller.h"

#define BLINK_PERIOD_MS  (500U)

static void blink_task(void *arg)
{
    (void)arg;
    for (;;) {
        led_controller_toggle(LED_RED);
        vTaskDelay(pdMS_TO_TICKS(BLINK_PERIOD_MS));
    }
}
```

`xTaskCreate(blink_task, "LAB_BLINK", 256, NULL, tskIDLE_PRIORITY + 1U, &handle)` — จาก [README.md](README.md) หัวข้อ 3.1

---

## แนวคิด — priority ตามแนวทางของหลักสูตร

| แนวทาง | ตัวอย่างในแล็บ |
|---|---|
| งาน background / กระพริบ | `tskIDLE_PRIORITY + 1` |
| งานตอบสนองปุ่ม / UI เบา | สูงกว่า blink เล็กน้อย |
| งานวิกฤต (IPC / watchdog path ในผลิตภัณฑ์) | สูงกว่า — **อย่ายกทุกอย่างขึ้นสูงสุด** |

ในผลิตภัณฑ์จริง priority สูงเกินไปของงานหนักอาจ starve งานสำคัญอื่น — ในแล็บให้เปลี่ยนทีละน้อยแล้วสังเกตอาการ

---

## ตัวอย่างสมบูรณ์ — Queue ส่งข้อมูลระหว่าง task

คิวของ FreeRTOS **คัดลอกข้อมูลตามขนาด item** ไม่ใช่ส่ง pointer อัตโนมัติ — แนวทางในหลักสูตร: อย่า `printf` จาก ISR ให้ **enqueue** แล้วให้ task ดึงไปพิมพ์

```c
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
```

จาก ISR: `xQueueSendFromISR(s_log_q, &item, &xHigherPriorityTaskWoken); portYIELD_FROM_ISR(...)` — [README.md](README.md) หัวข้อ 4

---

## ตัวอย่างสมบูรณ์ — Mutex ป้องกันบัสร่วม

จาก โมดูล 3: บัส I²C ร่วมต้องล็อก

```c
static SemaphoreHandle_t s_bus_mtx;

void lab_bus_lock_init(void) { s_bus_mtx = xSemaphoreCreateMutex(); }
void lab_bus_lock(void)      { (void)xSemaphoreTake(s_bus_mtx, portMAX_DELAY); }
void lab_bus_unlock(void)    { (void)xSemaphoreGive(s_bus_mtx); }
```

เรียกผ่าน wrapper ของหลักสูตรเมื่อมี: `cm55_i2c_manager_i2c_lock()` ... `cm55_i2c_manager_i2c_unlock()`

> ใน SDK จริง การล็อก I²C บางจุดใช้ **poll + `vTaskDelay(1)`** แทน `portMAX_DELAY` เพื่อเลี่ยงสถานการณ์ scheduler ยังไม่พร้อม

---

## แนวคิด — Binary Semaphore กับ Event Group

**Binary semaphore** — ใช้เมื่อต้องการ "มีสัญญาณแล้ว" ไม่ใช่ส่ง payload ใหญ่ (ถ้าต้องส่งข้อมูล ให้ใช้ queue)

```c
(void)xSemaphoreTake(s_evt, pdMS_TO_TICKS(1000));   /* task รอ */
(void)xSemaphoreGive(s_evt);                        /* อีก task หรือ ISR ส่งสัญญาณ */
```

**Event group** — ธงสถานะที่รอได้หลายบิต เช่น "I²C พร้อมแล้ว" ก่อนให้เซ็นเซอร์เริ่มทำงาน

```c
(void)xEventGroupSetBits(s_ready, READY_BIT);
EventBits_t bits = xEventGroupWaitBits(s_ready, READY_BIT, pdFALSE, pdFALSE, ticks);
```

---

## แนวคิด — กฎของ ISR และ tick hook

| หัวข้อ | แนวปฏิบัติในหลักสูตร |
|---|---|
| Period ของ task | ใช้ `vTaskDelay` / `vTaskDelayUntil` ตามแบบที่โปรเจกต์ใช้ |
| งานยาวใน priority สูง | แยกเป็น task ต่ำกว่า หรือหั่นงานเป็นชิ้นสั้น ๆ |
| ISR | สั้น ๆ · ไม่ `printf` · ไม่ I²C · ไม่ mutex แบบ blocking |
| Tick hook | ห้ามเรียก driver ที่ต้องล็อกหรือ I/O ช้า |
| Heap / queue depth | `depth × sizeof(item)` กิน RAM — คิวใหญ่เกินอาจได้ `NULL` |

> **ห้ามใน ISR / tick hook**: `xSemaphoreTake` (blocking), `vTaskDelay`, I²C, `printf` — ใช้ `*FromISR` แล้วให้ task ทำงานหนักแทน

---

## ตัวอย่างสมบูรณ์ — โจทย์รวมหลาย task

โจทย์: กระพริบ LED คาบเวลาคงที่ + กดปุ่มแล้วส่งข้อความเข้าคิว log + task อื่นพิมพ์ UART

```text
blink_task          → led_controller_toggle + vTaskDelay
button callback     → xQueueSend(log_q, "btn\r\n")
log_drain_task      → xQueueReceive + printf
```

ต่อยอดแล็บโมดูล 3 ส่วน D: ADC อ่านใน task ช้า + PWM ปรับในอีก task หรือส่งค่าผ่านคิว

---

## ฝึกเติม/แล็บ

[แล็บ: เฟิร์มแวร์หลาย task ด้วย FreeRTOS](../l02-lab/README.md)

- สร้าง task ที่มีคาบเวลาอย่างน้อยสอง task ที่รันพร้อมกัน
- ส่งข้อมูลระหว่าง task ด้วย queue อย่างน้อยหนึ่งเส้นทาง
- ล็อกทรัพยากรร่วม (เช่นบัส I²C) ด้วย mutex เมื่อมีมากกว่าหนึ่ง task ใช้งาน
- เคารพกฎ ISR / tick hook ตลอดทั้งแล็บ

---

## เช็กความเข้าใจ

1. ตามหลักการ priority ของบทเรียน งาน background เช่นกระพริบ LED ควรใช้ priority ระดับใด
2. ต้องการส่ง "ข้อมูล" จาก task ปุ่มไปยัง task ที่พิมพ์ UART ควรใช้กลไกใด (queue / mutex / event group)
3. ข้อใดห้ามทำใน ISR หรือ tick hook ตามบทเรียน (เลือกได้หลายข้อ): `portYIELD_FROM_ISR` · `vTaskDelay` · `printf` · `xQueueSendFromISR` · อ่านเซ็นเซอร์ผ่าน I²C

---

## ไปต่อ

- หลักสูตรใช้ **FreeRTOS** — เริ่มผ่าน `cm55_initialize` / `cm55_start_scheduler`
- **Task + delay** เป็นรากฐาน; แยกจังหวะงานด้วยหลาย task
- **Queue** ส่งข้อมูล · **Mutex** ล็อกทรัพยากร · **Binary semaphore / Event group** ส่งสัญญาณสถานะ
- เคารพกฎ ISR และ priority เพื่อไม่ให้ระบบ "ค้างเงียบ" หรือ starve — ต่อไป **โมดูล 5** จะใช้หลาย task กับ pipeline เซ็นเซอร์ / Edge AI

[บทเรียนโมดูล 5 →](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md)

---

## แหล่งที่มา

"บทเรียน 4.1 — เฟิร์มแวร์หลาย task ด้วย FreeRTOS" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C1 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
