---
id: fw-sdk.m03.l02
lang: th
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

> **หมายเหตุ:** snippet ในแล็บนี้ใช้ API ของเฟิร์มแวร์ TESAIoT Bitstream ซึ่งยังไม่เปิดซอร์ส ดูรายละเอียดและตัวอย่างเทียบใน SDK สาธารณะได้ที่หมายเหตุต้นบทเรียน [GPIO และอุปกรณ์ต่อพ่วงผ่าน Driver API](../l01-gpio-and-peripherals/README.md)

### Useful references during the lab

| เอกสาร | ใช้เมื่อ |
|---|---|
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | ตัวอย่าง GPIO / Sensors / Embedded |
| Snippet ใน [Lesson](../l01-gpio-and-peripherals/README.md) | ชื่อฟังก์ชันจริงของ TESA Firmware SDK |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | HEX / Flasher หากใช้แพ็กสำเร็จรูป |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | ดู telemetry (เสริม) |

---

## Lab Goals

- ควบคุม LED ด้วย `led_controller_*` (หรือ `Cy_GPIO_*`)  
- รับเหตุการณ์ปุ่มด้วย `cm55_button_*`  
- ส่ง log ทาง UART (`printf` / `LOG_INFO` / `cm55_uart_send`)  
- ทำอย่างน้อยหนึ่งอย่างจาก: **PWM** (`bitstream_led_pwm_*`) · **ADC** (`cm55_adc_*`) · **I²C** (`sensor_sht40_*` หรือเซ็นเซอร์อื่นที่มีบนบอร์ดของคุณ)  
- กรอกชื่อ API จริงใน [peripheral-api-map.md](../l01-gpio-and-peripherals/resources/peripheral-api-map.md)  

---

## Prerequisites

- [ ] ผ่านเกณฑ์ M02  
- [ ] โปรเจกต์ตัวอย่างที่ลิงก์ TESA Firmware SDK แล้ว  
- [ ] สาย USB + serial terminal  
- [ ] รู้คิตในมือ (AI vs Eval — มีผลต่อปุ่มที่สองและ POT)

---

## Lab A — GPIO: LED + Button (required)

1. เรียก `led_controller_init` (ถ้าโปรเจกต์ยังไม่ init) และทดลอง `led_controller_set` / `led_controller_toggle`  
2. เรียก `cm55_button_init` แล้วผูก `cm55_button_on_pressed(BUTTON_ID_0, …)` ให้สลับ LED  
3. Flash แล้วสาธิตบนบอร์ด  

**Pass when:** กดปุ่มแล้ว LED เปลี่ยนสถานะอย่างเสถียร

```c
/* แนวทางสั้น — ดูรายละเอียดใน Lesson §2 */
(void)led_controller_init();
(void)cm55_button_init();
(void)cm55_button_on_pressed(BUTTON_ID_0, on_btn_pressed);
```

---

## Lab B — UART log (required)

1. ใน callback ปุ่ม (หรือ loop) พิมพ์ข้อความ เช่น `btn toggled`  
2. เปิด terminal บนพอร์ต KitProg3 ตาม baud ของโปรเจกต์  
3. ยืนยันว่าข้อความตรงกับเหตุการณ์ปุ่ม  

```c
printf("btn toggled\r\n");
/* หรือ */ LOG_INFO("LAB", "btn toggled");
```

**Pass when:** เห็นข้อความตรงกับเหตุการณ์ปุ่ม

---

## Lab C — Choose at least one (required)

### C1 PWM

```c
(void)bitstream_led_pwm_init();
(void)bitstream_led_pwm_set_brightness(0, 20);
(void)bitstream_led_pwm_set_brightness(0, 80);
```

**Pass when:** เห็นความสว่างต่างกันชัดเจนอย่างน้อย 2 ระดับ

### C2 ADC (Eval kit with POT)

```c
(void)cm55_adc_init();
int16_t mv = cm55_adc_read_pot_mv();
printf("POT mV=%d\r\n", (int)mv);
```

**Pass when:** ค่าเปลี่ยนเมื่อหมุน POT และพิมพ์ทาง UART ได้

### C3 I²C sensor

```c
(void)sensor_sht40_startup();
sht40_sample_t s;
if (sensor_sht40_read(&s)) {
    printf("T=%.2f RH=%.2f\r\n", (double)s.temperature, (double)s.humidity);
}
```

(หรือเซ็นเซอร์อื่นที่มีบนบอร์ดของคุณ — `sensor_bmi270_*` ฯลฯ)

**Pass when:** อ่านค่าได้และพิมพ์ทาง UART

---

## Lab D — Mini integration (recommended)

รวม A+B กับผลจาก C เช่น ADC → PWM duty หรือปุ่ม → สลับโหมด + UART log  

หน่วงใน task:

```c
vTaskDelay(pdMS_TO_TICKS(50));
```

**Optional:** เปิด [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) ถ้าเฟิร์มแวร์ส่ง telemetry

---

## Short report (5–10 lines)

1. ชื่อ BSP / บอร์ด  
2. ตารางงาน → ชื่อ API จริง (จาก API map)  
3. ผล Lab A/B/C  

---

## Troubleshooting

| อาการ | แนวทางแก้ |
|---|---|
| LED ไม่ติด | `led_id_t` ผิด · active level · ยังไม่ init BSP |
| ปุ่มไม่มี event | ยังไม่ `cm55_button_init` / ผูก callback · ใช้ผิด `BUTTON_ID_*` |
| UART เงียบ | พอร์ต COM / baud · retarget ยังไม่พร้อม · ล็อก `cm55_uart_out_*` ค้าง |
| I²C fail | เซ็นเซอร์ไม่พร้อม · ลืม lock บัสเมื่อเขียนไดรเวอร์ต่ำ · ที่อยู่ผิด |
| ADC = 0 ตลอด | คิตไม่มี POT · ยังไม่ `cm55_adc_init` |
| PWM ไม่เปลี่ยน | ยังไม่ `bitstream_led_pwm_init` · `led_id` ผิดช่วง |

---

## Submit checklist

- [ ] Lab A ผ่าน  
- [ ] Lab B ผ่าน  
- [ ] Lab C ≥ 1 ข้อผ่าน  
- [ ] กรอก [peripheral-api-map.md](../l01-gpio-and-peripherals/resources/peripheral-api-map.md)  
- [ ] (แนะนำ) Lab D  

[Lesson](../l01-gpio-and-peripherals/README.md) · [API map](../l01-gpio-and-peripherals/resources/peripheral-api-map.md) · [Table of Contents](../../README.md) · [M04 →](../../m04-rtos/l01-freertos-programming/README.md)
