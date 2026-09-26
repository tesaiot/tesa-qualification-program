---
id: fw-sdk.m03.l01
lang: en
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
translation: done
slides: slides.md
source_sha256: 6559d7022aef47f806734d500dcbb5394f18425b27668965d3c7546d87b21aa6
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M03/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M03 — GPIO and Basic Peripherals

**Course 1 · Module 3**
**Suggested time:** about 3 hours (reading + lab on the board)
**Format:** a hands-on lesson — calls the **Driver API** of the TESA Firmware SDK on the project you can build/flash from [M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md)

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/peripheral-api-map.md) · [← Table of Contents](../../README.md) · [← M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md) · [M04 →](../../m04-rtos/l01-freertos-programming/README.md)

> **Note: which firmware the code in this lesson is written for** (checked on 2026-09-26)
>
> The C code in this lesson calls the API of the **TESAIoT Bitstream** firmware, called "TESA Firmware SDK" in the original, which is published as a ready-made HEX file (`tesaiot-bitstream-<version>.hex`) alongside Bitstream Studio in the [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/tree/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/hex) lab pack. **The source code of this firmware is not yet public.** Functions such as `led_controller_*`, `cm55_button_*`, `cm55_uart_send`, `sensor_sht40_*`, `cm55_i2c_manager_i2c_lock`, `bitstream_led_pwm_*` and `cm55_adc_*` therefore have no header you can open or build yourself. Read the snippets as concepts and a calling order. The calls to FreeRTOS and the Infineon PDL (such as `xTaskCreate`, `vTaskDelay`, `Cy_GPIO_*`) are ordinary public APIs.
>
> If you want code you can read and build from open source, see [tesaiot-pse84-devkit-sdk](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) (Apache-2.0), which is a **different codebase with different API names**. Examples already checked to do the same job as this lesson (commit `ef72c1b`):
>
> - [`proj_cm33_ns/examples/io/04_gpio_led_button.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c) — an LED and a button with the PDL's `Cy_GPIO_*`, on the pins `CYBSP_USER_LED1` / `CYBSP_USER_BTN1` (matches section 2.2)
> - [`proj_cm33_ns/examples/io/03_read_potentiometers.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/03_read_potentiometers.c) — reading a potentiometer through the SAR ADC (`potentiometer_read_raw` / `_percent` / `_voltage`)
> - [`proj_cm55/examples/io/02_pots_and_capsense.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/io/02_pots_and_capsense.c) — reading knobs VR1–VR4 on the CM55 (`cm55_pot_read_all`)
> - [`proj_cm33_ns/examples/sensors/04_read_environment.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/04_read_environment.c) — reading the SHT40 / DPS368 over I²C, locking the bus with `sensor_i2c_lock` / `sensor_i2c_unlock`
> - [`proj_cm33_ns/examples/sensors/01_i2c_bus_scan.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/01_i2c_bus_scan.c) — scanning the I²C bus under the same mutex
>
> No equivalent found yet in the public SDK: dimming LEDs via PWM (`bitstream_led_pwm_*`) and `cm55_uart_send`

---

## Objectives (Learning Outcomes)

By the end of this lesson you should be able to:

1. Explain **GPIO** fundamentals and try it on the board with the course's API (`led_controller_*`, `cm55_button_*`, or `Cy_GPIO_*`)
2. Explain the role of the main peripherals: **Timer, UART, I²C, SPI, PWM, ADC**
3. Use the TESA Firmware SDK's **Driver API** to control peripherals systematically
4. Do exercises block by block, then combine them into a small circuit, noting the real function names called

This module takes you from "a project that runs" in M02 to **talking to hardware through the Driver layer**, per the map in [M01](../../m01-mcu-architecture/l01-architecture-and-sdk-layers/README.md)

> **About the snippets in this lesson**
> The C examples below are drawn from the **TESA Firmware SDK** (a wrapper on the CM55 + FreeRTOS)
> In the lab, call these function names per the project you have locked your version to — see more examples on the **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** (Domain: **GPIO** / **Sensors** / **Embedded**)

### Naming map (course-facing)

| Task in the lab | Recommended API to call | Layer underneath (just know it exists) |
|---|---|---|
| LED on/off / toggle | `led_controller_set` / `led_controller_toggle` | `Cy_GPIO_*` + a BSP pin |
| A button + event | `cm55_button_init` / `cm55_button_on_pressed` | GPIO IRQ + a FreeRTOS task |
| Logging a message | `printf` / `LOG_INFO` after bring-up | `init_retarget_io` · `cm55_uart_*` |
| An I²C sensor | `sensor_sht40_*` (or another sensor in the SDK) | `cm55_i2c_manager_*` · `mtb_hal_i2c_*` |
| Reading a POT (Eval) | `cm55_adc_read_pot_mv` | Autonomous Analog SAR |
| Dimming an LED via PWM | `bitstream_led_pwm_set_brightness` | `Cy_TCPWM_PWM_*` |
| Delaying inside a task | `vTaskDelay(pdMS_TO_TICKS(...))` | FreeRTOS (detail in M04) |
| General SPI in a lab | Concept + an Infineon / Hub example | In the current SDK, the main SPI path is on the radar module (`Cy_SCB_SPI_*`) |

Do not use `cyhal_gpio_*` as this course's main path — the TESA stack uses **a wrapper + PDL / MTB HAL**.

### Read alongside this chapter

| Document | Use when |
|---|---|
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | The course's main code examples + API Reference |
| [AN241775 — HAL on PSOC™ Edge (PDF)](https://www.infineon.com/assets/row/public/documents/30/42/infineon-an241775-getting-started-with-hal-psoc-edge-applicationnotes-en.pdf) | PDL / HAL / the Device Configurator |
| [AN235935 — Getting started on ModusToolbox™ (PDF)](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf) | build / program / a UART terminal |
| [mtb-example-psoc-edge-hello-world](https://github.com/Infineon/mtb-example-psoc-edge-hello-world) | LED + UART (extra Infineon example) |
| [mtb-example-psoc-edge-gpio-interrupt](https://github.com/Infineon/mtb-example-psoc-edge-gpio-interrupt) | GPIO interrupts (extra Infineon example) |
| [mtb-example-psoc-edge-spi-dma](https://github.com/Infineon/mtb-example-psoc-edge-spi-dma) | An SPI code example, when you want a separate SPI lab |
| [retarget-io](https://github.com/Infineon/retarget-io) | The `printf` → UART concept |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | HEX / Flasher / web-app |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | Host telemetry (extra) |

---

## 1. From Application Down to Driver API

```text
Application  →  TESA Driver API (led_controller_*, cm55_*, sensor_*)
                    →  MTB HAL / Infineon PDL  →  Hardware pins / blocks
```

| Course principle | Why it matters |
|---|---|
| Call the SDK's wrapper first | Lab code matches the product / example projects |
| Fully init before reading/writing | The bus and pins are ready |
| Check return values / timeouts | Tells apart a software bug from a hardware one |
| Use a mutex around a shared bus (I²C) | Lets several tasks safely share the same bus |

> **Key phrase**
> The Application decides — the Driver talks to hardware — don't jump ahead to touching registers in standard exercises.

---

## 2. GPIO Fundamentals

**GPIO** is a pin that can be set as a digital input or output.

| Mode | What it's for | In the course's SDK |
|---|---|---|
| Output | Driving an LED | `led_controller_*`, or `Cy_GPIO_Write` / `Cy_GPIO_Inv` |
| Input / event | Reading a button | `cm55_button_*` |
| Interrupt | A pin edge → a callback | Inside `cm55_button` (GPIO IRQ + a task) |

Concepts to know: **active-high/low**, **pull-up/down**, **debounce** (usually handled inside the SDK's button module).

### 2.1 LED output (TESA wrapper)

```c
#include "led_controller.h"

void lab_led_demo(void)
{
    (void)led_controller_init();          /* optional; the BSP usually already inits the pin */
    led_controller_set(LED_RED, true);
    led_controller_toggle(LED_GREEN);
    led_controller_off_all();
}
```

`led_id_t`: `LED_RED`, `LED_GREEN`, `LED_BLUE`

### 2.2 Raw GPIO (when you need to touch a pin directly)

```c
#include "cybsp.h"
#include "cy_gpio.h"

/* Example: toggle USER LED1 with the PDL */
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

Some kits have a single button (`BUTTON_ID_0`); the Eval kit may have `BUTTON_ID_1` depending on the BSP.

---

## 3. Core Peripherals

### 3.1 Timer / delay (lab mindset)

For a lab with several tasks / periodic timing, use **FreeRTOS** (detail in M04):

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

Low-level TCPWM (`Cy_TCPWM_Counter_*` / `mtb_hal_timer_*`) exists in the stack, but a basic lab doesn't need to call it directly.

### 3.2 UART / logging

After the app's bring-up (`cm55_initialize` in a standard project), retarget IO is usually already set up — use:

```c
#include <stdio.h>
#include "app_log.h"

void lab_uart_log(void)
{
    printf("hello from CM55\r\n");
    LOG_INFO("LAB", "btn toggled");
}
```

Send a raw buffer when needed:

```c
#include "cm55_uart.h"

const char msg[] = "raw uart\r\n";
cm55_uart_send((const uint8_t *)msg, sizeof(msg) - 1U);
```

The terminal is usually the **KitProg3** port — the baud rate follows the project/manual (Infineon examples are usually 115200 8N1).

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

When writing your own low-level driver on a shared bus, lock it:

```c
cm55_i2c_manager_i2c_lock();
/* mtb_hal_i2c_controller_write / read ... */
cm55_i2c_manager_i2c_unlock();
```

Other sensors in the SDK follow the same pattern: `sensor_bmi270_*`, `sensor_dps368_*`, `sensor_bmm350_*` (detail in M05)

### 3.4 SPI

In the current product, the clearest SPI path in the library sits on the radar module (`Cy_SCB_SPI_Init` / `Cy_SCB_SPI_Enable` / `Cy_SCB_SPI_Transfer`).
For a general SPI lab: use the examples on the [Developer Hub](https://dev.tesaiot.dev/), or [mtb-example-psoc-edge-spi-dma](https://github.com/Infineon/mtb-example-psoc-edge-spi-dma)

Concepts you need to know: **CS, CPOL/CPHA, MOSI/MISO/SCK**

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

Digital on/off for an LED can still use `led_controller_*` — use PWM when you need continuous brightness.

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

> On a kit with no POT (such as some AI kit configurations), the function may be a no-op / return 0 — follow the kit you actually have.

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

The standard sequence:

1. **Init / configure** (`*_init`, `*_startup`)
2. **Enable / start** (if separate)
3. **Transfer** (read/write/set)
4. **Check the return value**
5. **Deinit** once done (in a real app)

An API name sheet: [peripheral-api-map.md](resources/peripheral-api-map.md)

### 4.1 Finding more examples

| Source | How to use it |
|---|---|
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | Domain GPIO / Sensors / Embedded |
| The example project you're using | The header of the same module as the snippets in this lesson |
| Infineon CE | Compare against a vendor approach (extra) |

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
        /* map 0..1800 mV → 0..100% (adjust to the kit's real Vref) */
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

Use `sensor_sht40_read` + `printf` per §3.3 — later, arrange data windows in M05 / watch it on [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) once the firmware sends telemetry

---

## 6. Board Reality Checks

- Check the LED / button aliases from the BSP of the kit in hand
- Most boards' I²C already has pull-ups — lock the bus when several tasks use it
- The ADC POT works on the Eval kit, as the SDK supports it
- The HEX / Flasher pack: **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)**

> The main lab is measured by the LED / UART / values you can read
> Extra host: [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)

---

## 7. Module Summary

1. Call the **TESA Driver API** (`led_controller_*`, `cm55_*`, `sensor_*`) as the main path
2. The timer in a basic lab = **`vTaskDelay`** (FreeRTOS) — M04 expands into multi-tasking
3. UART = `printf` / `LOG_*` / `cm55_uart_send`
4. I²C / ADC / PWM have ready-made wrappers in the SDK
5. SPI is a concept + Hub/Infineon examples

### Next Steps

1. Do the exercise: [Lab](../l02-lab/README.md)
2. Note the real API names: [Cheatsheet](resources/peripheral-api-map.md)
3. When ready, continue to **M04 — RTOS Programming** ([M04 lesson](../../m04-rtos/l01-freertos-programming/README.md))

---

## References and Further Reading

### Course portals

1. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**
2. **[Bitstream Studio (Marketplace)](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)**
3. **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)**

### Infineon (extra)

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

## Check your understanding

Three short questions in [quiz.yaml](quiz.yaml), one per objective of this lesson. Try answering them yourself first, then compare with the answer key and explanations in the file.

## Lab

Continue hands-on at [Lab: GPIO and peripherals on real hardware](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/peripheral-api-map.md) · [← Table of Contents](../../README.md) · [← M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md) · [M04 →](../../m04-rtos/l01-freertos-programming/README.md)

## Examples on the TESAIoT Developer Hub

Try the real thing on the TESAIoT Dev Kit: open examples on the Developer Hub to read the code, download it, or flash ready-made firmware.

- [QWA309 — Push Button Monitor](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_button_monitor&q=prac_qwa309_button_monitor) — reads buttons SW9 (P17.5) and SW10 (P17.7) as active-low pull-up, showing pressed/released state + a press count on LVGL
- [QWA309 — Potentiometer Monitor](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_pot_monitor&q=prac_qwa309_pot_monitor) — reads 4 potentiometers (P15.4–P15.7) through the AUTANALOG SAR ADC, 12-bit (Vref 1.8V), shown as a bar + voltage + percentage in real time — a first practice exercise
- [QWA309 — 4-Channel ADC Scope](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_adc_scope&q=prac_qwa309_adc_scope) — plots the 4 pot values (P15.4-7, SAR 12-bit) as a scrolling line on an LVGL chart, 0-100% — an analog oscilloscope
