---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 3.1 — GPIO และอุปกรณ์ต่อพ่วงผ่าน Driver API"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT) · CC BY 4.0"
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

# บทเรียน 3.1 — GPIO และอุปกรณ์ต่อพ่วงผ่าน Driver API

## ควบคุม LED ปุ่ม UART I²C PWM และ ADC ผ่านชั้น Driver และรู้ว่า SPI กับ timer อยู่ตรงไหนในสแต็ก

**หลักสูตร TESA Firmware SDK สำหรับ Edge AI — โมดูล 3 · บทเรียน 1**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. เลือกฟังก์ชันระดับ wrapper หรือ PDL ที่เหมาะกับงาน GPIO (LED, ปุ่ม) จากตาราง naming map ได้ถูกต้อง
2. เรียงลำดับการใช้ Driver API มาตรฐาน (init → enable → transfer → ตรวจค่าคืน → deinit) ได้ถูกต้อง
3. อธิบายเหตุผลที่ต้องล็อกบัส I²C ก่อน และปลดล็อกหลังการอ่านเขียนระดับต่ำ เมื่อหลาย task ใช้บัสร่วมกัน

---

## ก่อนเริ่ม

- ผ่าน [บทเรียน 2.2 — แล็บ M02](../../m02-toolchain/l02-lab/README.md) มาแล้ว: มีโปรเจกต์ที่ build/flash ได้
- **ต้องใช้บอร์ดจริง**: TESAIoT Dev Kit หรือ Eva Kit (KIT_PSE84_EVAL)
- บทเรียนเชิงปฏิบัติ — เรียก **Driver API** ของ TESA Firmware SDK บนโปรเจกต์จากโมดูล 2

> **หมายเหตุสำคัญ (ตรวจสอบเมื่อ 26 ก.ย. 2026):** โค้ด C ในบทนี้เรียก API ของเฟิร์มแวร์ **TESAIoT Bitstream** ที่แจกเป็นไฟล์ HEX สำเร็จรูป — **ซอร์สโค้ดของเฟิร์มแวร์ชุดนี้ยังไม่เปิดเผยต่อสาธารณะ** ฟังก์ชันอย่าง `led_controller_*`, `cm55_button_*`, `cm55_uart_send`, `sensor_sht40_*`, `cm55_i2c_manager_i2c_lock`, `bitstream_led_pwm_*`, `cm55_adc_*` จึงยังไม่มี header ให้เปิดดูหรือ build เอง — อ่าน snippet เป็นแนวคิดและลำดับการเรียกใช้ ส่วน FreeRTOS และ Infineon PDL (`xTaskCreate`, `vTaskDelay`, `Cy_GPIO_*`) เป็น API สาธารณะตามปกติ

---

## ดูของจริงก่อน — จาก Application ลงไปถึง Driver

```text
Application  →  TESA Driver API (led_controller_*, cm55_*, sensor_*)
                    →  MTB HAL / Infineon PDL  →  Hardware pins / blocks
```

| หลักการในหลักสูตร | ทำไมสำคัญ |
|---|---|
| เรียก wrapper ของ SDK ก่อน | โค้ดแล็บตรงกับผลิตภัณฑ์ / โปรเจกต์ตัวอย่าง |
| Init ให้ครบก่อน read/write | บัสและพินพร้อม |
| ตรวจค่าคืน / timeout | แยกบั๊กซอฟต์แวร์กับฮาร์ดแวร์ |
| ใช้ mutex รอบบัสร่วม (I²C) | หลาย task แชร์บัสเดียวกันได้อย่างปลอดภัย |

> **Key phrase**: Application ตัดสินใจ — Driver คุยกับฮาร์ดแวร์ — อย่ากระโดดไปแตะ register ในแบบฝึกมาตรฐาน

---

## แนวคิด — GPIO พื้นฐาน

**GPIO** คือขาที่ตั้งเป็นอินพุตหรือเอาต์พุตดิจิทัลได้

| โหมด | ใช้ทำอะไร | ใน SDK หลักสูตร |
|---|---|---|
| Output | ขับ LED | `led_controller_*` หรือ `Cy_GPIO_Write` / `Cy_GPIO_Inv` |
| Input / event | อ่านปุ่ม | `cm55_button_*` |
| Interrupt | ขอบขา → callback | ภายใน `cm55_button` (GPIO IRQ + task) |

แนวคิดที่ต้องรู้: **active-high/low**, **pull-up/down**, **debounce** (ในปุ่มของ SDK มักจัดการในโมดูลปุ่ม)

**อย่าใช้ `cyhal_gpio_*` เป็นเส้นทางหลักของหลักสูตรนี้** — สแต็ก TESA ใช้ wrapper + PDL / MTB HAL

---

## ตัวอย่างสมบูรณ์ — LED output (wrapper ของ SDK)

```c
#include "led_controller.h"

void lab_led_demo(void)
{
    (void)led_controller_init();          /* optional; BSP มัก init พินไว้แล้ว */
    led_controller_set(LED_RED, true);
    led_controller_toggle(LED_GREEN);
    led_controller_off_all();
}
```

`led_id_t`: `LED_RED`, `LED_GREEN`, `LED_BLUE` — จาก [README.md](README.md) หัวข้อ 2.1 (ฟังก์ชันของเฟิร์มแวร์ที่ยังไม่เปิดซอร์ส)

---

## ตัวอย่างสมบูรณ์ — ปุ่มและ event callback

```c
#include "sensor_button.h"   /* public API: cm55_button_* */

static void on_btn_pressed(cm55_button_t handle, const button_event_t *evt)
{
    (void)handle;
    led_controller_toggle(LED_BLUE);
    printf("button %lu pressed (count=%lu)\r\n",
           (unsigned long)evt->button_id,
           (unsigned long)evt->press_count);
}

void lab_button_setup(void)
{
    (void)cm55_button_init();
    (void)cm55_button_on_pressed(BUTTON_ID_0, on_btn_pressed);
}
```

จาก [README.md](README.md) หัวข้อ 2.3 — บนคิตบางรุ่นมีปุ่มเดียว (`BUTTON_ID_0`); Eval อาจมี `BUTTON_ID_1` ตาม BSP

---

## ตัวอย่างสมบูรณ์ — I²C เซ็นเซอร์ และการล็อกบัส

```c
#include "sensor_sht40.h"

void lab_i2c_sht40(void)
{
    if (sensor_sht40_startup() != CY_RSLT_SUCCESS) {
        printf("SHT40 startup failed\r\n");
        return;
    }
    sht40_sample_t sample;
    if (sensor_sht40_read(&sample)) {
        printf("T=%.2f C  RH=%.2f %%\r\n",
               (double)sample.temperature, (double)sample.humidity);
    }
}
```

ล็อกบัสเมื่อเขียนไดรเวอร์ระดับต่ำเองบนบัสร่วม: `cm55_i2c_manager_i2c_lock()` ... `cm55_i2c_manager_i2c_unlock()` — จาก [README.md](README.md) หัวข้อ 3.3

---

## แนวคิด — เพริเฟอรัลที่เหลือ: Timer, UART, PWM, ADC, SPI

| เพริเฟอรัล | API หลักในหลักสูตร | หมายเหตุ |
|---|---|---|
| Timer / delay | `vTaskDelay(pdMS_TO_TICKS(...))` (FreeRTOS) | รายละเอียด multi-task ใน โมดูล 4 |
| UART / log | `printf` / `LOG_INFO` / `cm55_uart_send` | terminal มักเป็นพอร์ต KitProg3 |
| PWM (ความสว่าง LED) | `bitstream_led_pwm_set_brightness(led_id, percent)` | LED เปิด/ปิดดิจิทัลยังใช้ `led_controller_*` ได้ |
| ADC (potentiometer, Eval) | `cm55_adc_read_pot_mv` / `cm55_adc_read_pot_counts` | บนคิตไม่มี POT อาจเป็น no-op / คืน 0 |
| SPI | แนวคิด + ตัวอย่าง Developer Hub / Infineon | path หลักปัจจุบันในไลบรารีอยู่ที่โมดูล radar (`Cy_SCB_SPI_*`) |

แนวคิดที่ต้องรู้ของ SPI: **CS, CPOL/CPHA, MOSI/MISO/SCK**

---

## แนวคิด — ใช้ Driver API อย่างเป็นระบบ (ลำดับมาตรฐาน)

1. **Init / configure** (`*_init`, `*_startup`)
2. **Enable / start** (ถ้าแยก)
3. **Transfer** (read/write/set)
4. **ตรวจค่าคืน**
5. **Deinit** เมื่อเลิกใช้ (แอปจริง)

แผ่นจดชื่อ API: [peripheral-api-map.md](resources/peripheral-api-map.md)

---

## ตัวอย่างสมบูรณ์ — โจทย์รวม: ปุ่มสลับ LED + UART

```c
static void on_pressed(cm55_button_t h, const button_event_t *evt)
{
    (void)h;
    (void)evt;
    led_controller_toggle(LED_GREEN);
    printf("btn toggled\r\n");
}

void app_lab_ab(void)
{
    (void)led_controller_init();
    (void)cm55_button_init();
    (void)cm55_button_on_pressed(BUTTON_ID_0, on_pressed);
}
```

จาก [README.md](README.md) หัวข้อ 5 Scenario A — Scenario B (ADC ขับ PWM) และ C (I²C → UART) อยู่ในไฟล์เดียวกัน

---

## ฝึกเติม/แล็บ

[แล็บ: GPIO และอุปกรณ์ต่อพ่วงบนฮาร์ดแวร์จริง](../l02-lab/README.md)

- แยกฝึกทีละบล็อก (LED, ปุ่ม, UART, I²C, PWM, ADC) บนบอร์ดจริง
- รวมเป็นวงจรเล็ก ๆ ตามโจทย์ scenario
- จดชื่อฟังก์ชันจริงที่เรียกใช้ในโปรเจกต์ของคุณ (เวอร์ชัน SDK อาจต่างกัน)
- ตรวจ alias LED/ปุ่มจาก BSP ของคิตในมือก่อนเริ่ม

---

## เช็กความเข้าใจ

1. ในสแต็กของบทเรียนนี้ ข้อใดถูกระบุว่า "อย่าใช้เป็นเส้นทางหลัก" ของหลักสูตร
2. เรียงลำดับการใช้ Driver API มาตรฐานจากรายการนี้: ตรวจค่าคืน · Init/configure · Deinit เมื่อเลิกใช้ · Transfer (read/write/set) · Enable/start
3. ทำไมต้องล็อกบัส I²C รอบการอ่านเขียนระดับต่ำ

---

## ไปต่อ

- เรียก **TESA Driver API** (`led_controller_*`, `cm55_*`, `sensor_*`) เป็นหลัก
- Timer ในแล็บพื้นฐาน = `vTaskDelay` (FreeRTOS) — โมดูล 4 ขยายเป็น multi-task
- UART = `printf` / `LOG_*` / `cm55_uart_send` · I²C/ADC/PWM มี wrapper พร้อมใช้ · SPI เป็นแนวคิด + ตัวอย่าง Hub/Infineon
- พร้อมแล้วสำหรับ **โมดูล 4 — การเขียนเฟิร์มแวร์แบบ RTOS**

[บทเรียนโมดูล 4 →](../../m04-rtos/l01-freertos-programming/README.md)

---

## แหล่งที่มา

"บทเรียน 3.1 — GPIO และอุปกรณ์ต่อพ่วงผ่าน Driver API" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C1 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
