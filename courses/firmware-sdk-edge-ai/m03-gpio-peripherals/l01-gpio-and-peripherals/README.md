---
id: fw-sdk.m03.l01
lang: th
title:
  th: GPIO และอุปกรณ์ต่อพ่วงผ่าน Driver API
  en: GPIO and Peripherals through a Driver API
summary:
  th: ควบคุม LED ปุ่ม UART I²C PWM และ ADC ผ่านชั้น Driver และรู้ว่า SPI กับ timer อยู่ตรงไหนในสแต็ก
  en: Drive LEDs, buttons, UART, I²C, PWM and ADC through the driver layer and see where SPI and timers sit in the stack.
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
- fw-sdk.m02.l02
objectives:
- th: เลือกฟังก์ชันระดับ wrapper หรือ PDL ที่เหมาะกับงาน GPIO (LED, ปุ่ม) จากตาราง naming map ได้ถูกต้อง
  en: Pick the right wrapper-level or PDL call for a GPIO task (LED, button) from the naming map.
- th: เรียงลำดับการใช้ Driver API มาตรฐาน (init → enable → transfer → ตรวจค่าคืน → deinit) ได้ถูกต้อง
  en: Put the standard driver-API sequence (init, enable, transfer, check return, deinit) in the right order.
- th: อธิบายเหตุผลที่ต้องล็อกบัส I²C ก่อน และปลดล็อกหลังการอ่านเขียนระดับต่ำ เมื่อหลาย task ใช้บัสร่วมกัน
  en: Explain why a shared I²C bus must be locked before, and unlocked after, low-level reads and writes when several tasks use it.
develops:
- skill: mcu.gpio
  to: 2
- skill: proto.uart
  to: 2
- skill: proto.i2c
  to: 2
- skill: mcu.pwm
  to: 1
- skill: mcu.adc-dac
  to: 1
- skill: proto.spi
  to: 1
- skill: mcu.interrupts
  to: 1
context:
  platform: psoc-edge-e84
  lang: c
  ide: modustoolbox-vscode
  firmware: tesaiot-bitstream (HEX; source not public yet)
status: alpha
translation: pending
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M03/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M03 — GPIO and Basic Peripherals

**Course 1 · Module 3**  
**Suggested time:** ประมาณ 3 ชั่วโมง (อ่าน + lab บนบอร์ด)  
**Format:** บทเรียนเชิงปฏิบัติ — เรียก **Driver API** ของ TESA Firmware SDK บนโปรเจกต์ที่ build/flash ได้จาก [M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md)

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/peripheral-api-map.md) · [← Table of Contents](../../README.md) · [← M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md) · [M04 →](../../m04-rtos/l01-freertos-programming/README.md)

> **หมายเหตุ: โค้ดในบทนี้เขียนสำหรับเฟิร์มแวร์ชุดใด** (ตรวจสอบเมื่อ 26 ก.ย. 2026)
>
> โค้ด C ในบทนี้เรียก API ของเฟิร์มแวร์ **TESAIoT Bitstream** ที่ต้นฉบับเรียกว่า “TESA Firmware SDK” ซึ่งเผยแพร่เป็นไฟล์ HEX สำเร็จรูป (`tesaiot-bitstream-<version>.hex`) คู่กับ Bitstream Studio ในแพ็กแล็บ [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/tree/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/hex) **ซอร์สโค้ดของเฟิร์มแวร์ชุดนี้ยังไม่เปิดเผยต่อสาธารณะ** ฟังก์ชันอย่าง `led_controller_*`, `cm55_button_*`, `cm55_uart_send`, `sensor_sht40_*`, `cm55_i2c_manager_i2c_lock`, `bitstream_led_pwm_*`, `cm55_adc_*` จึงยังไม่มี header ให้เปิดดูหรือนำไป build เอง ให้อ่าน snippet เป็นแนวคิดและลำดับการเรียกใช้ ส่วนการเรียก FreeRTOS และ Infineon PDL (เช่น `xTaskCreate`, `vTaskDelay`, `Cy_GPIO_*`) เป็น API สาธารณะตามปกติ
>
> ถ้าต้องการโค้ดที่อ่านและ build ได้จากซอร์สเปิด ให้ดู [tesaiot-pse84-devkit-sdk](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) (Apache-2.0) ซึ่งเป็น**คนละโค้ดเบสและตั้งชื่อ API ต่างกัน** ตัวอย่างที่ตรวจแล้วว่าทำงานเรื่องเดียวกับบทนี้ (commit `ef72c1b`):
>
> - [`proj_cm33_ns/examples/io/04_gpio_led_button.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c) — LED และปุ่มด้วย PDL `Cy_GPIO_*` บนพิน `CYBSP_USER_LED1` / `CYBSP_USER_BTN1` (ตรงกับหัวข้อ 2.2)
> - [`proj_cm33_ns/examples/io/03_read_potentiometers.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/03_read_potentiometers.c) — อ่าน potentiometer ผ่าน SAR ADC (`potentiometer_read_raw` / `_percent` / `_voltage`)
> - [`proj_cm55/examples/io/02_pots_and_capsense.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/io/02_pots_and_capsense.c) — อ่าน knob VR1–VR4 บน CM55 (`cm55_pot_read_all`)
> - [`proj_cm33_ns/examples/sensors/04_read_environment.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/04_read_environment.c) — อ่าน SHT40 / DPS368 ทาง I²C พร้อมล็อกบัสด้วย `sensor_i2c_lock` / `sensor_i2c_unlock`
> - [`proj_cm33_ns/examples/sensors/01_i2c_bus_scan.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/01_i2c_bus_scan.c) — สแกนบัส I²C ภายใต้ mutex ตัวเดียวกัน
>
> ยังไม่พบตัวเทียบใน SDK สาธารณะ: PWM หรี่ไฟ (`bitstream_led_pwm_*`) และ `cm55_uart_send`

---

## เป้าหมาย (Learning Outcomes)

เมื่อเรียนจบ คุณควรทำได้ดังนี้:

1. อธิบายพื้นฐาน **GPIO** และทดลองบนบอร์ดด้วย API ของหลักสูตร (`led_controller_*`, `cm55_button_*`, หรือ `Cy_GPIO_*`)  
2. อธิบายบทบาทของ peripheral หลัก: **Timer, UART, I²C, SPI, PWM, ADC**  
3. ใช้ **Driver API** ของ TESA Firmware SDK เพื่อควบคุมอุปกรณ์ต่อพ่วงอย่างเป็นระบบ  
4. ทำแบบฝึกแยกบล็อกแล้วรวมเป็นวงจรเล็ก ๆ พร้อมจดชื่อฟังก์ชันจริงที่เรียกใช้  

โมดูลนี้พาคุณจาก “โปรเจกต์รันได้” ใน M02 ไปสู่การ **คุยกับฮาร์ดแวร์ผ่านชั้น Driver** ตามแผนที่ใน [M01](../../m01-mcu-architecture/l01-architecture-and-sdk-layers/README.md)

> **เกี่ยวกับ snippet ในบทนี้**  
> ตัวอย่างภาษา C ด้านล่างดึงจาก **TESA Firmware SDK** (wrapper บน CM55 + FreeRTOS)  
> ในแล็บให้เรียกชื่อฟังก์ชันเหล่านี้ตามโปรเจกต์ที่คุณล็อกเวอร์ชันไว้ — ดูตัวอย่างเพิ่มบน **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** (Domain: **GPIO** / **Sensors** / **Embedded**)

### Naming map (course-facing)

| งานในแล็บ | API ที่แนะนำให้เรียก | ชั้นด้านล่าง (รู้ไว้พอ) |
|---|---|---|
| LED on/off / toggle | `led_controller_set` / `led_controller_toggle` | `Cy_GPIO_*` + BSP pin |
| ปุ่ม + event | `cm55_button_init` / `cm55_button_on_pressed` | GPIO IRQ + FreeRTOS task |
| Log ข้อความ | `printf` / `LOG_INFO` หลัง bring-up | `init_retarget_io` · `cm55_uart_*` |
| เซ็นเซอร์ I²C | `sensor_sht40_*` (หรือเซ็นเซอร์อื่นใน SDK) | `cm55_i2c_manager_*` · `mtb_hal_i2c_*` |
| อ่าน POT (Eval) | `cm55_adc_read_pot_mv` | Autonomous Analog SAR |
| หรี่ไฟ PWM | `bitstream_led_pwm_set_brightness` | `Cy_TCPWM_PWM_*` |
| หน่วงเวลาใน task | `vTaskDelay(pdMS_TO_TICKS(...))` | FreeRTOS (ลงลึกใน M04) |
| SPI ทั่วไปใน lab | แนวคิด + ตัวอย่าง Infineon / Hub | ใน SDK ปัจจุบัน path SPI หลักอยู่ที่ radar (`Cy_SCB_SPI_*`) |

อย่าใช้ `cyhal_gpio_*` เป็นเส้นทางหลักของหลักสูตรนี้ — สแต็ก TESA ใช้ **wrapper + PDL / MTB HAL**

### Read alongside this chapter

| เอกสาร | ใช้เมื่อ |
|---|---|
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | ตัวอย่างโค้ดหลักสูตร + API Reference |
| [AN241775 — HAL on PSOC™ Edge (PDF)](https://www.infineon.com/assets/row/public/documents/30/42/infineon-an241775-getting-started-with-hal-psoc-edge-applicationnotes-en.pdf) | PDL / HAL / Device Configurator |
| [AN235935 — Getting started on ModusToolbox™ (PDF)](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf) | build / program / UART terminal |
| [mtb-example-psoc-edge-hello-world](https://github.com/Infineon/mtb-example-psoc-edge-hello-world) | LED + UART (Infineon เสริม) |
| [mtb-example-psoc-edge-gpio-interrupt](https://github.com/Infineon/mtb-example-psoc-edge-gpio-interrupt) | GPIO interrupt (Infineon เสริม) |
| [mtb-example-psoc-edge-spi-dma](https://github.com/Infineon/mtb-example-psoc-edge-spi-dma) | SPI CE เมื่อต้องการแล็บ SPI แยก |
| [retarget-io](https://github.com/Infineon/retarget-io) | แนวคิด `printf` → UART |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | HEX / Flasher / web-app |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | telemetry บนโฮสต์ (เสริม) |

---

## 1. From Application Down to Driver API

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

> **Key phrase**  
> Application ตัดสินใจ — Driver คุยกับฮาร์ดแวร์ — อย่ากระโดดไปแตะ register ในแบบฝึกมาตรฐาน

---

## 2. GPIO Fundamentals

**GPIO** คือขาที่ตั้งเป็นอินพุตหรือเอาต์พุตดิจิทัลได้

| โหมด | ใช้ทำอะไร | ใน SDK หลักสูตร |
|---|---|---|
| Output | ขับ LED | `led_controller_*` หรือ `Cy_GPIO_Write` / `Cy_GPIO_Inv` |
| Input / event | อ่านปุ่ม | `cm55_button_*` |
| Interrupt | ขอบขา → callback | ภายใน `cm55_button` (GPIO IRQ + task) |

แนวคิด: **active-high/low**, **pull-up/down**, **debounce** (ในปุ่มของ SDK มักจัดการในโมดูลปุ่ม)

### 2.1 LED output (TESA wrapper)

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

`led_id_t`: `LED_RED`, `LED_GREEN`, `LED_BLUE`

### 2.2 Raw GPIO (เมื่อต้องการแตะพินตรง)

```c
#include "cybsp.h"
#include "cy_gpio.h"

/* ตัวอย่าง: สลับ USER LED1 ด้วย PDL */
Cy_GPIO_Inv(CYBSP_USER_LED1_PORT, CYBSP_USER_LED1_PIN);
Cy_GPIO_Write(CYBSP_USER_LED1_PORT, CYBSP_USER_LED1_PIN, 1U);
```

### 2.3 Button events

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

บนคิตบางรุ่นมีปุ่มเดียว (`BUTTON_ID_0`); Eval อาจมี `BUTTON_ID_1` ตาม BSP

---

## 3. Core Peripherals

### 3.1 Timer / delay (lab mindset)

สำหรับแล็บหลาย task / คาบเวลา ให้ใช้ **FreeRTOS** (ลงรายละเอียดใน M04):

```c
#include "FreeRTOS.h"
#include "task.h"

void blink_task(void *arg)
{
    (void)arg;
    for (;;) {
        led_controller_toggle(LED_RED);
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}
```

TCPWM ระดับต่ำ (`Cy_TCPWM_Counter_*` / `mtb_hal_timer_*`) มีในสแต็ก แต่แล็บพื้นฐานไม่จำเป็นต้องเรียกตรง

### 3.2 UART / logging

หลัง bring-up ของแอป (`cm55_initialize` ในโปรเจกต์มาตรฐาน) มักมี retarget IO แล้ว — ใช้:

```c
#include <stdio.h>
#include "app_log.h"

void lab_uart_log(void)
{
    printf("hello from CM55\r\n");
    LOG_INFO("LAB", "btn toggled");
}
```

ส่งบัฟเฟอร์ดิบเมื่อต้องการ:

```c
#include "cm55_uart.h"

const char msg[] = "raw uart\r\n";
cm55_uart_send((const uint8_t *)msg, sizeof(msg) - 1U);
```

Terminal มักเป็นพอร์ต **KitProg3** — baud ตามโปรเจกต์/คู่มือ (ตัวอย่าง Infineon มัก 115200 8N1)

### 3.3 I²C (sensor path)

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
               (double)sample.temperature,
               (double)sample.humidity);
    }
}
```

เมื่อเขียนไดรเวอร์ระดับต่ำเองบนบัสร่วม ให้ล็อก:

```c
cm55_i2c_manager_i2c_lock();
/* mtb_hal_i2c_controller_write / read ... */
cm55_i2c_manager_i2c_unlock();
```

เซ็นเซอร์อื่นใน SDK ตามแนวเดียวกัน: `sensor_bmi270_*`, `sensor_dps368_*`, `sensor_bmm350_*` (รายละเอียดใน M05)

### 3.4 SPI

ในผลิตภัณฑ์ปัจจุบัน path SPI ที่เห็นชัดในไลบรารีอยู่ที่โมดูล radar (`Cy_SCB_SPI_Init` / `Cy_SCB_SPI_Enable` / `Cy_SCB_SPI_Transfer`)  
สำหรับแล็บ SPI ทั่วไป: ใช้ตัวอย่างบน [Developer Hub](https://dev.tesaiot.dev/) หรือ [mtb-example-psoc-edge-spi-dma](https://github.com/Infineon/mtb-example-psoc-edge-spi-dma)

แนวคิดที่ต้องรู้: **CS, CPOL/CPHA, MOSI/MISO/SCK**

### 3.5 PWM (LED brightness)

```c
#include "bitstream_led_pwm.h"

void lab_pwm_brightness(void)
{
    if (bitstream_led_pwm_init() != 0) {
        return;
    }
    (void)bitstream_led_pwm_set_brightness(0 /* led_id */, 20);  /* ~20% */
    (void)bitstream_led_pwm_set_brightness(0, 80);               /* ~80% */
}
```

LED เปิด/ปิดแบบดิจิทัลยังใช้ `led_controller_*` ได้ — PWM ใช้เมื่อต้องการความสว่างต่อเนื่อง

### 3.6 ADC (potentiometer on Eval kit)

```c
#include "sensor_adc.h"

void lab_adc_pot(void)
{
    if (!cm55_adc_init()) {
        printf("ADC init failed or POT N/A on this kit\r\n");
        return;
    }

    int32_t counts = cm55_adc_read_pot_counts();
    int16_t mv = cm55_adc_read_pot_mv();
    printf("POT counts=%ld  mV=%d\r\n", (long)counts, (int)mv);
}
```

> บนคิตที่ไม่มี POT (เช่น AI kit บางคอนฟิก) ฟังก์ชันอาจเป็น no-op / คืน 0 — ให้ยึดคิตที่ใช้

### 3.7 Peripheral map

```text
Application
   ├── led_controller_* / Cy_GPIO_*     → LED
   ├── cm55_button_*                    → button events
   ├── printf / LOG_* / cm55_uart_*     → UART log
   ├── sensor_* + cm55_i2c_manager_*    → I²C sensors
   ├── bitstream_led_pwm_*              → PWM brightness
   ├── cm55_adc_*                       → POT (Eval)
   └── vTaskDelay / xTaskCreate         → timing & tasks (M04)
```

---

## 4. How to Use Driver API in Practice

ลำดับมาตรฐาน:

1. **Init / configure** (`*_init`, `*_startup`)  
2. **Enable / start** (ถ้าแยก)  
3. **Transfer** (read/write/set)  
4. **ตรวจค่าคืน**  
5. **Deinit** เมื่อเลิกใช้ (แอปจริง)

แผ่นจดชื่อ API: [peripheral-api-map.md](resources/peripheral-api-map.md)

### 4.1 Finding more examples

| แหล่ง | วิธีใช้ |
|---|---|
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | Domain GPIO / Sensors / Embedded |
| โปรเจกต์ตัวอย่างที่คุณใช้ | header ของโมดูลเดียวกันกับ snippet ในบทนี้ |
| Infineon CE | เปรียบเทียบแนวทางผู้ผลิต (เสริม) |

---

## 5. Worked Integration Scenarios

### Scenario A — Button toggles LED + UART

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

### Scenario B — ADC drives PWM brightness

```c
void app_lab_adc_pwm(void)
{
    (void)cm55_adc_init();
    (void)bitstream_led_pwm_init();

    for (;;) {
        int16_t mv = cm55_adc_read_pot_mv();
        /* map 0..1800 mV → 0..100% (ปรับตาม Vref จริงของคิต) */
        uint8_t duty = (uint8_t)((mv * 100) / 1800);
        if (duty > 100U) {
            duty = 100U;
        }
        (void)bitstream_led_pwm_set_brightness(0, duty);
        vTaskDelay(pdMS_TO_TICKS(50));
    }
}
```

### Scenario C — I²C sample to UART (preview of M05)

ใช้ `sensor_sht40_read` + `printf` ตาม §3.3 — ต่อไปจัดหน้าต่างข้อมูลใน M05 / ดูบน [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) เมื่อเฟิร์มแวร์ส่ง telemetry

---

## 6. Board Reality Checks

- ตรวจ alias LED / ปุ่มจาก BSP ของคิตในมือ  
- I²C บนบอร์ดส่วนใหญ่มี pull-up แล้ว — ล็อกบัสเมื่อหลาย task  
- ADC POT ใช้ได้บน Eval ตามที่ SDK รองรับ  
- แพ็ก HEX / Flasher: **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)**  

> Lab หลักวัดผลที่ LED / UART / ค่าที่อ่านได้  
> Host เสริม: [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)

---

## 7. Module Summary

1. เรียก **TESA Driver API** (`led_controller_*`, `cm55_*`, `sensor_*`) เป็นหลัก  
2. Timer ในแล็บพื้นฐาน = **`vTaskDelay`** (FreeRTOS) — M04 ขยาย multi-task  
3. UART = `printf` / `LOG_*` / `cm55_uart_send`  
4. I²C / ADC / PWM มี wrapper พร้อมใช้ใน SDK  
5. SPI เป็นแนวคิด + ตัวอย่าง Hub/Infineon  

### Next Steps

1. ทำแบบฝึก: [Lab](../l02-lab/README.md)  
2. จดชื่อ API จริง: [Cheatsheet](resources/peripheral-api-map.md)  
3. เมื่อพร้อม ไปต่อ **M04 — RTOS Programming** ([บทเรียน M04](../../m04-rtos/l01-freertos-programming/README.md))

---

## References and Further Reading

### Course portals

1. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**  
2. **[Bitstream Studio (Marketplace)](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)**  
3. **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)**  

### Infineon (เสริม)

4. [AN241775 (PDF)](https://www.infineon.com/assets/row/public/documents/30/42/infineon-an241775-getting-started-with-hal-psoc-edge-applicationnotes-en.pdf)  
5. [AN235935 (PDF)](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf)  
6. [mtb-example-psoc-edge-hello-world](https://github.com/Infineon/mtb-example-psoc-edge-hello-world)  
7. [mtb-example-psoc-edge-gpio-interrupt](https://github.com/Infineon/mtb-example-psoc-edge-gpio-interrupt)  
8. [mtb-example-psoc-edge-spi-dma](https://github.com/Infineon/mtb-example-psoc-edge-spi-dma)  
9. [retarget-io](https://github.com/Infineon/retarget-io)  
10. [KIT_PSE84_EVAL](https://www.infineon.com/evaluation-board/KIT-pse84-eval)  

### FreeRTOS (preview for M04)

11. [FreeRTOS task control](https://www.freertos.org/a00127.html) — `vTaskDelay`  
12. [FreeRTOS xTaskCreate](https://www.freertos.org/a00125.html)  

---

## เช็กความเข้าใจ

คำถามสั้นสามข้อใน [quiz.yaml](quiz.yaml) ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อน แล้วค่อยเทียบกับเฉลยและคำอธิบายในไฟล์

## แล็บ

ลงมือต่อที่ [แล็บ: GPIO และอุปกรณ์ต่อพ่วงบนฮาร์ดแวร์จริง](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/peripheral-api-map.md) · [← Table of Contents](../../README.md) · [← M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md) · [M04 →](../../m04-rtos/l01-freertos-programming/README.md)
