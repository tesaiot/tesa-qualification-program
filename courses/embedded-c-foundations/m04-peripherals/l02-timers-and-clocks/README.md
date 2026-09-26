---
id: c-found.m04.l02
lang: th
title: {th: Timer และสัญญาณนาฬิกา, en: Timers and clocks}
summary: {th: ทำงานเป็นจังหวะด้วย timer ของฮาร์ดแวร์และของ RTOS และเข้าใจว่าสัญญาณนาฬิกากำหนดความแม่นยำอย่างไร, en: Run periodic work with hardware and RTOS timers and understand how clocks set accuracy.}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m04.l01]
objectives:
- {th: คำนวณค่าตั้ง timer จากความถี่สัญญาณนาฬิกาและช่วงเวลาที่ต้องการได้, en: Compute timer settings from the clock frequency and the desired interval.}
- {th: เลือกระหว่าง timer ของฮาร์ดแวร์กับ software timer ของ RTOS ให้เหมาะกับงาน พร้อมเหตุผล, en: 'Choose between a hardware timer and an RTOS software timer for a task, with reasons.'}
- {th: อธิบายผลของการตั้งอัตราการทำงานของ task เบื้องหลังต่อภาระของระบบ, en: Explain how the rate of a background task affects system load.}
develops:
- {skill: mcu.timers, to: 3}
- {skill: mcu.clock, to: 2}
- {skill: rtos.freertos, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: pending
---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. คำนวณค่าตั้ง timer จากความถี่สัญญาณนาฬิกาและช่วงเวลาที่ต้องการได้
2. เลือกระหว่าง timer ของฮาร์ดแวร์กับ software timer ของ RTOS ให้เหมาะกับงาน พร้อมเหตุผล
3. อธิบายผลของการตั้งอัตราการทำงานของ task เบื้องหลังต่อภาระของระบบ

ใช้เวลาประมาณ 70 นาที (แนวคิด 15 · ฝึก 25 · แล็บ 25 · เช็ก 5)

## ก่อนเริ่ม

ทวนจากบทก่อนหน้าสองข้อ

1. ตัวกันเด้งในบทเรียน 4.1 อ่านปุ่มทุก 10 ms ใครเป็นคนกำหนดจังหวะ 10 ms นั้น ตัวกันเด้งเองหรือผู้เรียก
2. `175000 * 65535` ล้น 32 บิต แล้ว `65536 * 1000000` ล่ะ (บทเรียน 1.1)

## ดูของจริงก่อน

เปิด [examples/08_timer_math.c](examples/08_timer_math.c) ตัวเลขทุกตัวในไฟล์นี้อ่านมาจากไฟล์ที่ Device Configurator สร้างไว้ใน BSP ของ SDK
**ทายก่อนรัน** ว่า `GENERAL_PURPOSE_TIMER` ที่ BSP ตั้งไว้จะ overflow ทุกกี่มิลลิวินาที

```sh
gcc -std=c11 -Wall -Wextra -o timer_math examples/08_timer_math.c
./timer_math
```

ได้ 1000 ms พอดี และบรรทัดถัด ๆ มาแสดงว่าสัญญาณนาฬิกา 100 MHz ตัวเดียวกันนี้ ผ่านตัวหารคนละค่า กลายเป็นจังหวะของ PWM, UART 115200,
I2C 400 kHz และ SPI 25 MHz ของเรดาร์ ความถี่ของ UART ไม่ลงตัวพอดี คลาดไป -0.22% ซึ่งเป็นผลของการหารเลขจำนวนเต็ม

## แนวคิด

### 1. จากสัญญาณนาฬิกาถึงเวลา: สองสูตร

บน PSOC™ Edge E84 ในแม่แบบของ SDK อุปกรณ์กลุ่มหนึ่ง (TCPWM0, SCB2 ที่เป็น UART console, SCB3 ที่เป็น SPI ของเรดาร์ และอื่น ๆ) ใช้สัญญาณนาฬิกา CLK_HF10
ซึ่งตั้งไว้ที่ 100 MHz ([cycfg_clocks.c บรรทัด 153-154](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_clocks.c#L153-L154)
และตารางกลุ่มอุปกรณ์ใน [pse84_config.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/pse84_config.h#L6956-L7010))
แต่ละอุปกรณ์มีตัวหารของตัวเอง ตั้งด้วย `Cy_SysClk_PeriPclkSetDivider()` ซึ่งเอกสารของ PDL บอกว่าค่า N "causes integer division of (divider value + 1)"

- ความถี่ที่ timer ได้: **f<sub>cnt</sub> = f<sub>src</sub> / (N + 1)**
- เวลาต่อหนึ่งรอบของ timer ที่นับขึ้นจาก 0 ถึง period: **T = (period + 1) / f<sub>cnt</sub>**

ตัวอย่างจริงใน BSP: `GENERAL_PURPOSE_TIMER` คือ TCPWM0 counter 2 ใช้ตัวหาร 16 บิตค่า 9999 จึงได้ 100 MHz / 10000 = 10 kHz
และตั้ง `period = 9999` เปิด interrupt เมื่อถึง terminal count ([cycfg_peripherals.c บรรทัด 1115-1125](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_peripherals.c#L1115-L1125))
10000 จังหวะที่ 10 kHz คือ 1 วินาที ที่ commit นี้ยังไม่มีโค้ดของแม่แบบเรียกใช้ timer ตัวนี้ มันเป็นของที่ BSP เตรียมไว้ให้ ฟังก์ชันที่ใช้เริ่มมันอยู่ใน
[`cy_tcpwm_counter.h`](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_tcpwm_counter.h) เช่น `Cy_TCPWM_Counter_Init()`
`Cy_TCPWM_Counter_Enable()` และ `Cy_TCPWM_TriggerStart_Single()`

ช่วงเวลาเดียวกันทำได้หลายคู่ของตัวหารกับ period ตัวหารเล็กให้ความละเอียดสูงกว่า (แต่ละจังหวะสั้นกว่า) แต่ period ต้องใหญ่พอ
และความแม่นยำของทุกอย่างในสายนี้ **ไม่ดีไปกว่าต้นทาง** ถ้าต้นทางคลาด 1% ทุก timer คลาด 1% ตาม
ตัวอย่างสุดขั้วคือ watchdog ที่ใช้ oscillator ภายในความแม่นยำต่ำ เอกสารของ PDL ระบุความคลาด ±30% (บทเรียน 4.3)

### 2. timer ของฮาร์ดแวร์ หรือ software timer ของ RTOS

FreeRTOS ในแม่แบบตั้ง `configTICK_RATE_HZ` เป็น 1000 ([FreeRTOSConfig.h ของ CM33 บรรทัด 66](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/FreeRTOSConfig.h#L66))
หนึ่ง tick คือ 1 ms ทุกอย่างที่อิง tick จึงละเอียดได้ไม่เกินหนึ่ง tick

| ต้องการ | ใช้ | เหตุผล |
|---|---|---|
| คลื่น PWM ที่ขา วัดความกว้างพัลส์ (capture) จังหวะระดับไมโครวินาที | timer ของฮาร์ดแวร์ (TCPWM) | ฮาร์ดแวร์นับเองโดยไม่ขึ้นกับภาระของ CPU แต่มีจำนวนจำกัด และงานใน ISR ต้องสั้น |
| งานเป็นระยะระดับมิลลิวินาทีขึ้นไปใน task | `vTaskDelayUntil()` ใน task ของงานนั้น | task มี stack ของตัวเอง รอหรือเรียก API ที่บล็อกได้ |
| เรียกฟังก์ชันสั้น ๆ ครั้งเดียวหรือเป็นระยะโดยไม่อยากสร้าง task | software timer ของ FreeRTOS (`xTimerCreate()`) | callback ทำงานใน timer service task (ตั้ง priority 3 ใน config ของแม่แบบ) ห้ามบล็อก เพราะ timer ทุกตัวแชร์ task เดียวกัน |
| งานเป็นระยะบนหน้าจอของ CM55 | `lv_timer_create()` ของ LVGL | ตัวอย่างของ SDK ฝั่ง CM55 ใช้วิธีนี้ทุกตัว เพราะงานต้องอยู่ใน GFX task และห้ามบล็อก |

เรื่องที่พลาดบ่อยคือ `vTaskDelay()` กับ `vTaskDelayUntil()` เอกสารใน task.h ของ FreeRTOS อธิบายว่า `vTaskDelay()` "specifies a wake time relative
to the time at which the function is called" ส่วน `xTaskDelayUntil()` "specifies the absolute (exact) time at which it wishes to unblock"
([task.h ของ Infineon FreeRTOS release-v10.6.202](https://github.com/Infineon/freertos/blob/release-v10.6.202/Source/include/task.h))
ลูปที่ทำงาน 5 ms แล้ว `vTaskDelay(100 ms)` จึงวนทุก 105 ms ไม่ใช่ 100 ms และเลื่อนไปเรื่อย ๆ แม่แบบเปิด `INCLUDE_vTaskDelayUntil` ไว้แล้วในไฟล์ config

### 3. อัตราของ task เบื้องหลัง คือภาระของทั้งระบบ

task ที่อ่านเซนเซอร์ทุก P มิลลิวินาที และแต่ละรอบใช้เวลา C มิลลิวินาที ครอบครองทั้ง CPU และบัส I2C เป็นสัดส่วนราว C/P
ตัวอย่าง [05_auto_push_task.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/05_auto_push_task.c#L12-L75)
ของ SDK เล่าเรื่องจริงของ task ที่อ่านเซนเซอร์ทุกตัวแล้วส่งไป CM55 (ค่าเริ่มต้นทุก 100 ms)

- **ลูปหน่วงหลังอ่าน ไม่ใช่ระหว่างอ่าน** ตัวอย่างวัดจำนวนรอบจริงเทียบกับที่ควรได้ แล้วเตือนว่าถ้าได้น้อยกว่า "the reads themselves are costing more than the interval"
- **หน้าผาที่ 50 ms** `sensor_auto_set_rate()` รับ 20 ถึง 5000 ms แต่ต่ำกว่า 50 ms ลูป "reads ONLY the accelerometer" เพราะเซนเซอร์ตัวอื่นใช้เวลาบนบัสจนอัดลงงบ 20 ms ไม่ได้
  ตั้ง 20 ms เพื่อให้ทุกอย่างเร็วขึ้น ผลคือเซนเซอร์ห้าจากหกตัวหยุดส่งเงียบ ๆ
- **ผู้อ่านสองรายบนบัสเดียว** "Two readers on one bus at two rates is a bug waiting for a deadline; one publisher and many consumers is not."
  ถ้าค่าอายุ 100 ms ใช้ได้ ให้อ่านจาก cache ด้วย `sensor_auto_get_bmi270()` ซึ่งไม่แตะบัสเลย

อัตรายังผูกกับความถูกต้องด้วย โมเดล IMU ของ Edge AI ถูกฝึกด้วยข้อมูล 50 Hz ตัวอย่าง 08_deepcraft_link เตือนว่าถ้าปล่อยให้ข้อมูลมาทุก 100 ms
"every verdict is computed over five times the intended span of time and is confidently wrong" อัตราที่ผิดไม่ได้แค่เปลืองพลังงาน มันทำให้ผลผิด

## ตัวอย่างสมบูรณ์

[examples/08_timer_math.c](examples/08_timer_math.c) ทำงานเป็นสามท่า

- **ท่าที่ 1** `divided_hz()` ใช้สูตรตัวหาร N + 1 ของ PDL
- **ท่าที่ 2** คำนวณรอบของ `GENERAL_PURPOSE_TIMER` และ `PWM_LED_CTRL` จากค่าใน BSP (สำหรับ PWM เราสมมติว่านับ 0..period แบบเดียวกับ counter ให้ตรวจกับคู่มือของชิป)
- **ท่าที่ 3** คำนวณ baud ของ UART ความถี่ SCL ของ I2C และ SCLK ของ SPI จากสัญญาณนาฬิกาเดียวกัน

ลองแก้แล้วทายก่อนรัน

1. ถ้าต้องการให้ `GENERAL_PURPOSE_TIMER` เกิดทุก 250 ms โดยไม่เปลี่ยนตัวหาร period ต้องเป็นเท่าไร
2. ถ้าเปลี่ยนตัวหารของ UART จาก 86 เป็น 85 baud จริงและความคลาดเคลื่อนเป็นเท่าไร ตัวไหนใกล้ 115200 กว่า
3. ทำไมโปรแกรมนี้ใช้ `double` ได้ แต่ฟังก์ชันแบบเดียวกันในเฟิร์มแวร์ของ SDK มักเขียนด้วยเลขจำนวนเต็ม (คำใบ้: `printf` ของ CM33 ในแม่แบบไม่มี float)

## ฝึกเติม

เปิด [practice/08_timer_math.c](practice/08_timer_math.c) มีช่องให้เติม 4 จุด เขียนด้วยเลขจำนวนเต็มล้วนแบบเฟิร์มแวร์

1. `divided_hz()` ตามสูตรตัวหาร
2. `overflow_us()` ต้องใช้ตัวกลาง 64 บิต
3. `pick_timer()` หาตัวหารที่เล็กที่สุดที่ได้ช่วงเวลาพอดีเป๊ะด้วย period 16 บิต และบอกตรง ๆ เมื่อทำไม่ได้
4. `baud_error_ppm()` ความคลาดเคลื่อนเป็นส่วนในล้าน

```sh
gcc -std=c11 -Wall -Wextra -o timer_math practice/08_timer_math.c && ./timer_math
```

สังเกตว่า test ของ 1 วินาทีคาดหวังตัวหาร 1599 กับ period 62499 ไม่ใช่ 9999 กับ 9999 แบบใน BSP ทั้งสองคู่ได้ 1 วินาทีพอดี
แต่กติกาของแบบฝึกคือเลือกตัวหารที่เล็กที่สุด ข้อกำหนดที่เขียนชัดทำให้คำตอบมีคำตอบเดียว

## เฉลย

ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/08_timer_math.c](solution/08_timer_math.c)
จุดที่ควรเทียบคือทุกที่ที่คูณก่อนหารใช้ `uint64_t` หรือ `int64_t` และ `pick_timer()` ไม่แตะค่าที่ผู้เรียกส่งมาเมื่อหาคำตอบไม่ได้
ซึ่งเป็นหลักเดียวกับผลลัพธ์ที่บอกความจริงในบทเรียน 3.2

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) (บนเว็บไซต์อยู่ท้ายหน้านี้) ครอบคลุมเป้าหมายทั้งสามข้อ ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน

## แล็บ

**งาน:** วัดอัตราจริงของ task เบื้องหลังบนบอร์ด แล้วอธิบายส่วนต่างระหว่างอัตราที่ตั้งกับอัตราที่ได้

1. build ด้วย `make build -j ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/sensors/05_auto_push_task` แล้ว flash ถอดสายเสียบใหม่
2. จาก serial console จดค่า `rate` เริ่มต้น mask ของเซนเซอร์ และบรรทัด `measured ... cycles in 1000 ms (expected about ...)` ทั้งตอนอัตราเดิมและตอนที่ตัวอย่างปรับเป็น 25 ms
3. คำนวณจาก "expected" กับ "measured" ว่าแต่ละรอบใช้เวลาจริงกี่มิลลิวินาที แล้วประมาณเวลาที่การอ่านเซนเซอร์กินต่อรอบ (C) จากสูตร รอบจริง = C + ค่าหน่วง
4. ตอบว่าตอนอัตรา 25 ms เซนเซอร์ตัวไหนยังถูกอ่าน และทำไมจำนวนรอบที่วัดได้จึงใกล้หรือห่างจากที่คาด
5. ตรวจว่าตัวอย่างคืนค่าทุกอย่างกลับเหมือนเดิม (บรรทัด `--- restored ---`) ถ้าไม่ครบ ตัวอย่างจะรายงาน `RESTORE INCOMPLETE` ให้บันทึกไว้

**หลักฐานที่เก็บไว้ใน portfolio:** log ของตัวอย่างทั้งหมด ตารางการคำนวณในข้อ 3 และคำอธิบายข้อ 4

## ไปต่อ

- เอกสาร [FreeRTOS](https://www.freertos.org/Documentation/00-Overview) หัวข้อ software timers อธิบาย timer command queue และเหตุผลที่ callback ห้ามบล็อก
- โจทย์ท้าทาย: เขียน task ที่ทำงานทุก 20 ms ด้วย `vTaskDelayUntil()` แล้ววัดด้วย `xTaskGetTickCount()` ว่าคลาดไปเท่าไรใน 1000 รอบ เทียบกับ `vTaskDelay()`
- เปิดหัวไฟล์ของ [cy_tcpwm_counter.h](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_tcpwm_counter.h) อ่านโหมดการนับ (up, down, up/down) และอธิบายว่าสูตร period + 1 ต้องเปลี่ยนไหมในโหมดอื่น

บทถัดไป: [บทเรียน 4.3 Watchdog](../l03-watchdog/README.md)

## สะท้อนคิด

- งานเป็นระยะในโปรเจกต์ของคุณงานไหนที่ใช้ `vTaskDelay()` ทั้งที่ควรเป็น `vTaskDelayUntil()` และคุณจะรู้ได้อย่างไรว่ามันเลื่อน
- ถ้าผู้ใช้ขอให้ "อ่านเซนเซอร์เร็วขึ้นสองเท่า" คุณจะถามอะไรกลับก่อนแก้ค่า

## แหล่งอ้างอิง

- [SDK: cm33/sensors/05_auto_push_task.c (อัตราของ task เบื้องหลังและขีดจำกัด 50 ms)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/05_auto_push_task.c)
- [SDK: cycfg_peripheral_clocks.c ของ BSP (ตัวหารของแต่ละอุปกรณ์)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_peripheral_clocks.c)
- [SDK: cycfg_peripherals.c ของ BSP (ค่าตั้งของ TCPWM และ SCB)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_peripherals.c)
- [Infineon mtb-pdl-cat1 (Peripheral Driver Library) @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/tree/release-v3.24.0)
- [FreeRTOS documentation](https://www.freertos.org/Documentation/00-Overview)
