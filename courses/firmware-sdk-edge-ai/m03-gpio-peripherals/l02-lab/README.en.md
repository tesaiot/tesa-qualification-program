---
id: fw-sdk.m03.l02
lang: en
title:
  th: 'แล็บ: GPIO และอุปกรณ์ต่อพ่วงบนฮาร์ดแวร์จริง'
  en: 'Lab: GPIO and Peripherals on Real Hardware'
summary:
  th: 'ลงมือทีละบล็อก: LED + ปุ่ม, UART log, แล้วเลือก PWM / ADC / I²C อย่างน้อยหนึ่งอย่าง ก่อนรวมเป็นมินิวงจร'
  en: 'Work block by block: LED + button, UART log, then at least one of PWM / ADC / I²C before a short integration.'
level: L3
time_min:
  lab: 180
hardware:
  emulator: false
  boards:
  - devkit
  - eva-kit
prerequisites:
- fw-sdk.m03.l01
objectives:
- th: ทำให้ปุ่มสลับ LED บนบอร์ดจริงได้ (Lab A)
  en: Make a button toggle an LED on the real board (Lab A).
- th: ส่ง log ทาง UART ที่อ่านได้บน terminal (Lab B)
  en: Produce a readable UART log on a terminal (Lab B).
- th: ทำอุปกรณ์ต่อพ่วงเพิ่มอย่างน้อยหนึ่งชนิดจาก PWM, ADC หรือ I²C และจดชื่อฟังก์ชันจริงที่เรียก (Lab C)
  en: Get at least one more peripheral working (PWM, ADC or I²C) and record the real function names used (Lab C).
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
assesses:
- skill: mcu.gpio
  level: 2
  evidence: README.md#lab-a--gpio-led--button-required
- skill: proto.uart
  level: 2
  evidence: README.md#lab-b--uart-log-required
context:
  platform: psoc-edge-e84
  lang: c
  ide: modustoolbox-vscode
  firmware: tesaiot-bitstream (HEX; source not public yet)
status: alpha
translation: done
slides: slides.md
source_sha256: 318f3e807478ffa7370bb8e505ba0339a6ebf80e36e7d80ee5204cc42a609bb9
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M03/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M03 — GPIO and Peripherals on Real Hardware

**Course 1 · Module 3**
**Type:** Hands-on lab (block-by-block, then short integration)
**Suggested time:** 2.5–3 hours

Read first: [Lesson](../l01-gpio-and-peripherals/README.md) · [API map](../l01-gpio-and-peripherals/resources/peripheral-api-map.md) · [← Table of Contents](../../README.md) · [← M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md) · [M04 →](../../m04-rtos/l01-freertos-programming/README.md)

> **Note:** the snippets in this lab use the API of the TESAIoT Bitstream firmware, which is not yet open source. See detail and equivalent examples in the public SDK in the note at the top of the lesson [GPIO and Peripherals through a Driver API](../l01-gpio-and-peripherals/README.md)

### Useful references during the lab

| Document | Use when |
|---|---|
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | GPIO / Sensors / Embedded examples |
| Snippets in the [Lesson](../l01-gpio-and-peripherals/README.md) | The TESA Firmware SDK's real function names |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | HEX / Flasher, if using the ready-made pack |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | Watching telemetry (extra) |

---

## Lab Goals

- Control an LED with `led_controller_*` (or `Cy_GPIO_*`)
- Receive button events with `cm55_button_*`
- Send a UART log (`printf` / `LOG_INFO` / `cm55_uart_send`)
- Get at least one of: **PWM** (`bitstream_led_pwm_*`) · **ADC** (`cm55_adc_*`) · **I²C** (`sensor_sht40_*`, or another sensor on your board) working
- Fill in the real API names in [peripheral-api-map.md](../l01-gpio-and-peripherals/resources/peripheral-api-map.md)

---

## Prerequisites

- [ ] Have met the M02 bar
- [ ] An example project already linked to the TESA Firmware SDK
- [ ] A USB cable + a serial terminal
- [ ] Know the kit in hand (AI vs Eval — affects the second button and the POT)

---

## Lab A — GPIO: LED + Button (required)

1. Call `led_controller_init` (if the project hasn't already) and try `led_controller_set` / `led_controller_toggle`
2. Call `cm55_button_init`, then bind `cm55_button_on_pressed(BUTTON_ID_0, …)` to toggle the LED
3. Flash it and demonstrate it on the board

**Pass when:** pressing the button reliably changes the LED's state

```c
/* A short approach — see detail in Lesson §2 */
(void)led_controller_init();
(void)cm55_button_init();
(void)cm55_button_on_pressed(BUTTON_ID_0, on_btn_pressed);
```

---

## Lab B — UART log (required)

1. In the button callback (or a loop), print a message, such as `btn toggled`
2. Open a terminal on the KitProg3 port at the project's baud rate
3. Confirm the message matches the button event

```c
printf("btn toggled\r\n");
/* or */ LOG_INFO("LAB", "btn toggled");
```

**Pass when:** you see the message matching the button event

---

## Lab C — Choose at least one (required)

### C1 PWM

```c
(void)bitstream_led_pwm_init();
(void)bitstream_led_pwm_set_brightness(0, 20);
(void)bitstream_led_pwm_set_brightness(0, 80);
```

**Pass when:** you can clearly see at least 2 different brightness levels

### C2 ADC (Eval kit with POT)

```c
(void)cm55_adc_init();
int16_t mv = cm55_adc_read_pot_mv();
printf("POT mV=%d\r\n", (int)mv);
```

**Pass when:** the value changes when you turn the POT, and can be printed over UART

### C3 I²C sensor

```c
(void)sensor_sht40_startup();
sht40_sample_t s;
if (sensor_sht40_read(&s)) {
    printf("T=%.2f RH=%.2f\r\n", (double)s.temperature, (double)s.humidity);
}
```

(or another sensor on your board — `sensor_bmi270_*`, etc.)

**Pass when:** you can read a value and print it over UART

---

## Lab D — Mini integration (recommended)

Combine A+B with the result from C, for example ADC → PWM duty, or a button → switching a mode + a UART log

Delay inside a task:

```c
vTaskDelay(pdMS_TO_TICKS(50));
```

**Optional:** open [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) if the firmware sends telemetry

---

## Short report (5–10 lines)

1. The BSP / board name
2. A table of tasks → the real API name (from the API map)
3. The results of Lab A/B/C

---

## Troubleshooting

| Symptom | How to fix it |
|---|---|
| The LED doesn't light | The wrong `led_id_t` · the active level · the BSP not yet initialised |
| The button gives no event | Haven't called `cm55_button_init` / bound the callback · used the wrong `BUTTON_ID_*` |
| UART is silent | The COM port / baud rate · retarget not ready yet · `cm55_uart_out_*` still locked |
| I²C fails | The sensor isn't ready · forgot to lock the bus when writing a low-level driver · the wrong address |
| ADC always reads 0 | The kit has no POT · haven't called `cm55_adc_init` |
| PWM doesn't change | Haven't called `bitstream_led_pwm_init` · `led_id` out of range |

---

## Submit checklist

- [ ] Lab A passed
- [ ] Lab B passed
- [ ] Lab C: ≥ 1 item passed
- [ ] [peripheral-api-map.md](../l01-gpio-and-peripherals/resources/peripheral-api-map.md) filled in
- [ ] (Recommended) Lab D

[Lesson](../l01-gpio-and-peripherals/README.md) · [API map](../l01-gpio-and-peripherals/resources/peripheral-api-map.md) · [Table of Contents](../../README.md) · [M04 →](../../m04-rtos/l01-freertos-programming/README.md)
