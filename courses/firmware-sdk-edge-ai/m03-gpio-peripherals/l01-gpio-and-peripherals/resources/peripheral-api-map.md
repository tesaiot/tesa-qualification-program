# Cheatsheet — Peripheral ↔ Driver API Map (M03)

**Course 1 · Module 3**

จดชื่อฟังก์ชันจริงที่ใช้ในโปรเจกต์ตัวอย่าง — snippet อ้างอิงจาก TESA Firmware SDK (ดูตัวอย่างเต็มใน [Lesson](../README.md))

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [← Table of Contents](../../../README.md)

---

## Quick picker (TESA SDK)

| งาน | API ที่แนะนำ |
|---|---|
| LED on/off | `led_controller_set(LED_RED, true)` |
| LED toggle | `led_controller_toggle(LED_GREEN)` |
| LED all off | `led_controller_off_all()` |
| Raw pin toggle | `Cy_GPIO_Inv(CYBSP_USER_LED1_PORT, CYBSP_USER_LED1_PIN)` |
| Button init | `cm55_button_init()` |
| Button pressed CB | `cm55_button_on_pressed(BUTTON_ID_0, cb)` |
| UART text | `printf(...)` / `LOG_INFO("SRC", "...")` |
| UART raw | `cm55_uart_send(buf, len)` |
| I²C SHT40 | `sensor_sht40_startup()` · `sensor_sht40_read(&s)` |
| I²C bus lock | `cm55_i2c_manager_i2c_lock()` / `unlock()` |
| ADC POT | `cm55_adc_init()` · `cm55_adc_read_pot_mv()` |
| PWM brightness | `bitstream_led_pwm_init()` · `bitstream_led_pwm_set_brightness(id, 0..100)` |
| Delay in task | `vTaskDelay(pdMS_TO_TICKS(ms))` |
| Create task | `xTaskCreate(...)` (รายละเอียด M04) |

แหล่งตัวอย่างออนไลน์: **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**

---

## Call order

1. `init` / `startup`  
2. `enable` / `start` (ถ้ามี)  
3. `read` / `write` / `set`  
4. ตรวจ return code  

---

## Template — fill during lab

| งาน | กลุ่ม | ชื่อ API จริงในโปรเจกต์คุณ | Header ที่ `#include` |
|---|---|---|---|
| Init / set LED | GPIO | | `led_controller.h` |
| Button callback | GPIO | | `sensor_button.h` |
| UART print | UART | | `stdio.h` / `app_log.h` |
| PWM duty | PWM | | `bitstream_led_pwm.h` |
| ADC read | ADC | | `sensor_adc.h` |
| I2C sensor read | I2C | | `sensor_sht40.h` (หรืออื่น) |
| Task delay | Timer/RTOS | | `FreeRTOS.h` · `task.h` |

---

## Lab pack / host

| แหล่ง | ลิงก์ |
|---|---|
| HEX / Flasher / demos | [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) |
| Host / Digital Twin | [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) |

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [← Table of Contents](../../../README.md)
