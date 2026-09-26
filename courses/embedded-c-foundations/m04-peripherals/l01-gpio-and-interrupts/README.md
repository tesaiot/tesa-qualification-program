---
id: c-found.m04.l01
lang: th
title: {th: GPIO และ interrupt, en: GPIO and interrupts}
summary: {th: ขับหลอดไฟ อ่านปุ่ม และรับเหตุการณ์ด้วย interrupt ตามกติกาของบริบท ISR, en: 'Drive LEDs, read buttons and handle events with interrupts under ISR rules.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m03.l02]
objectives:
- {th: ตั้งค่าขา GPIO ด้วยคำสั่ง PDL ให้เป็นขาออกและขาเข้าที่มี drive mode ถูกต้อง, en: Configure GPIO pins with PDL calls as outputs and inputs with the correct drive mode.}
- {th: เขียน ISR ที่สั้น ไม่บล็อก และส่งงานต่อให้ task แทนการทำงานหนักใน ISR, en: 'Write a short, non-blocking ISR that hands work to a task instead of doing it inside.'}
- {th: กันเด้งปุ่มโดยไม่ใช้การรอแบบบล็อก, en: Debounce a button without blocking waits.}
develops:
- {skill: mcu.gpio, to: 3}
- {skill: mcu.interrupts, to: 3}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
slides: slides.md
---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ตั้งค่าขา GPIO ด้วยคำสั่ง PDL ให้เป็นขาออกและขาเข้าที่มี drive mode ถูกต้อง
2. เขียน ISR ที่สั้น ไม่บล็อก และส่งงานต่อให้ task แทนการทำงานหนักใน ISR
3. กันเด้งปุ่มโดยไม่ใช้การรอแบบบล็อก

ใช้เวลาประมาณ 70 นาที (แนวคิด 15 · ฝึก 25 · แล็บ 25 · เช็ก 5)

## ก่อนเริ่ม

ทวนจากโมดูลก่อนหน้าสองข้อ

1. ถ้า ISR กับ task ใช้ตัวแปรร่วมกัน ต้องประกาศอย่างไร และ `volatile` อย่างเดียวพอไหม (บทเรียน 1.1 และ 1.3)
2. ตอนที่ CM33 หยุดที่ breakpoint ในลูปอ่านปุ่ม การกดปุ่มหายไปได้อย่างไร (บทเรียน 3.1)

## ดูของจริงก่อน

เปิด [examples/07_debounce_trace.c](examples/07_debounce_trace.c) ไฟล์นี้ป้อนค่าที่ "อ่านจากขา" ทุก 10 ms จากตาราง ซึ่งจำลองการกดปุ่มหนึ่งครั้ง
ที่หน้าสัมผัสเด้งทั้งตอนกดและตอนปล่อย และมีสัญญาณรบกวนอีกหนึ่งการอ่าน **ทายก่อนรัน** ว่านับแบบค่าดิบจะได้กี่ครั้ง และแบบกันเด้งได้กี่ครั้ง

```sh
gcc -std=c11 -Wall -Wextra -o debounce_trace examples/07_debounce_trace.c
./debounce_trace
```

ค่าดิบนับได้ 6 ครั้ง ส่วนแบบกันเด้งได้ 1 ครั้ง พร้อมเวลาของ PRESS และ RELEASE ที่ช้ากว่าการแตะครั้งแรกราว 30 ms
และสังเกตว่าในโค้ดไม่มี `delay` เลยสักบรรทัด ตัวกันเด้งทั้งตัวคือฟังก์ชันที่ถูกเรียกหนึ่งครั้งต่อการอ่าน แล้วคืนทันที

## แนวคิด

### 1. drive mode คือทั้งหมดของงาน GPIO

ขาหนึ่งขาของ PSOC™ Edge ต้องตั้งสามอย่าง: ขาเป็นของใคร (HSIOM) ขับไฟแบบไหน (drive mode) และค่าเริ่มต้น PDL รวมไว้ในคำสั่งเดียว
`Cy_GPIO_Pin_FastInit(port, pin, driveMode, outVal, hsiom)` ตัวอย่าง [04_gpio_led_button.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c#L46-L60)
ของ SDK มีหัวข้อว่า "DRIVE MODES ARE THE WHOLE JOB"

```c
static void leds_init(void)
{
    for (unsigned i = 0U; i < LED_COUNT; i++) {
        Cy_GPIO_Pin_FastInit(s_leds[i].port, s_leds[i].pin,
                             CY_GPIO_DM_STRONG,
                             CYBSP_LED_STATE_OFF,   /* dark from the first cycle */
                             HSIOM_SEL_GPIO);       /* take the pin back from TCPWM */
    }
}

static void button_init(void)
{
    /* outVal = CYBSP_BTN_OFF (1) is what energises the pull-up. */
    Cy_GPIO_Pin_FastInit(CYBSP_USER_BTN1_PORT, CYBSP_USER_BTN1_NUM,
                         CY_GPIO_DM_PULLUP, CYBSP_BTN_OFF, HSIOM_SEL_GPIO);
}
```

ที่มา: [04_gpio_led_button.c บรรทัด 126-141](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c#L126-L141)
(Apache-2.0, tesaiot-pse84-devkit-sdk)

| ใช้ขาเป็น | drive mode จาก `cy_gpio.h` | ข้อควรรู้ |
|---|---|---|
| ขาออกขับ LED | `CY_GPIO_DM_STRONG` (push-pull) | ให้ `outVal` เป็นค่าดับ ขาจะไม่กะพริบตอนเริ่ม |
| ขาเข้าของปุ่มที่ต่อลงกราวด์ | `CY_GPIO_DM_PULLUP` | `outVal` ต้องเป็น 1 เพราะค่านี้คือสิ่งที่ "เปิด" pull-up ถ้าส่ง 0 ปุ่มจะดูเหมือนถูกกดตลอด |
| ขาเข้าที่มีตัวต้านทานภายนอก | `CY_GPIO_DM_HIGHZ` | ไม่มี pull ภายใน |
| ขาเข้าของสัญญาณ active-high เช่น data-ready | `CY_GPIO_DM_PULLDOWN` | driver ของเรดาร์ใน SDK ใช้แบบนี้ |
| ขาออกที่ไม่ต้องอ่านกลับ | `CY_GPIO_DM_STRONG_IN_OFF` | ปิด input buffer |

บน BSP ของบอร์ดนี้ ปุ่มผู้ใช้ `CYBSP_USER_BTN1` คือ P7.0 ตั้งไว้เป็น `CY_GPIO_DM_PULLUP` ค่าเริ่มต้น 1 และ LED1 กับ LED2 อยู่ที่ P10.7 และ P10.5
แบบ `CY_GPIO_DM_STRONG` ([cycfg_pins.h บรรทัด 274-303 สำหรับปุ่ม](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_pins.h#L274-L303)
และ [บรรทัด 466-500 สำหรับ LED](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_pins.h#L466-L500))
ชื่อ define ของปุ่มคือ BTN1 แต่บนแผ่นวงจรพิมพ์ว่า SW2 คอมเมนต์ของ SDK บอกว่า "Print the silkscreen name to a user."
และให้ใช้ค่าขั้วจาก BSP (`CYBSP_BTN_PRESSED` = 0, `CYBSP_LED_STATE_ON` = 1) แทนการเขียนเลขเอง

### 2. ISR ที่ดี: สั้น ไม่รอ ไม่พิมพ์ แล้วส่งงานต่อ

ISR ขัดจังหวะทุกอย่างที่มีความสำคัญต่ำกว่า ระหว่างที่มันทำงาน interrupt อื่นที่ต่ำกว่าต้องรอ และ task ทุกตัวหยุด
กติกาของ SDK จึงชัดเจน: "Never `printf` from an IPC callback (ISR context)" (README แคตตาล็อก) และตัวอย่าง TACP อธิบายว่า
ฟังก์ชันที่ได้ชื่อ `_from_isr` คือฟังก์ชันที่ "takes no mutex, allocates nothing, and prints nothing"
ISR ที่สั้นที่สุดใน SDK คือตัวรับสัญญาณ data-ready ของเรดาร์

```c
/** Radar data-ready interrupt handler */
static void radar_data_ready_isr(void)
{
    if (radar_drdy_events < 0xFFFFFFFFu) {
        radar_drdy_events++;
    }
    Cy_GPIO_ClearInterrupt(CYBSP_RADAR_INT_PORT, CYBSP_RADAR_INT_NUM);
    NVIC_ClearPendingIRQ(radar_irq_cfg.intrSrc);
}
```

ที่มา: [radar_task.c บรรทัด 109-117](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/radar_task.c#L109-L117)
(Apache-2.0, tesaiot-pse84-devkit-sdk) มันทำสองอย่าง: บันทึกว่าเกิดเหตุการณ์ (ตัวนับ `volatile` ที่หยุดที่ค่าสูงสุด ไม่วนกลับ)
และล้าง interrupt flag ของขา ถ้าไม่ล้าง ISR จะถูกเรียกซ้ำไม่รู้จบ งานหนักทั้งหมดอยู่ใน task ของเรดาร์

เมื่อต้องปลุก task ทันที ใช้ API ของ FreeRTOS ที่ลงท้ายด้วย `FromISR` แล้วเรียก `portYIELD_FROM_ISR()` ให้สลับไปหา task ที่ถูกปลุกได้เลยเมื่อ ISR จบ
ตัวอย่างใน SDK: [ipc_tesaiot_handler.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_config/ipc_tesaiot_handler.c#L360-L363)
ใช้ `xSemaphoreGiveFromISR()` ส่วน [sensor_auto_task.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/mpy/sensor_auto_task.c#L274-L299)
คัดลอกคำขอเข้าคิวด้วย `xQueueSendFromISR()` และเขียนกำกับว่า "No printf here — this is ISR context"
อีกกติกาหนึ่งของ FreeRTOS: ISR ที่เรียก API แบบ `FromISR` ต้องมีลำดับความสำคัญไม่สูงกว่าค่า `configMAX_SYSCALL_INTERRUPT_PRIORITY`
ซึ่งไฟล์ [FreeRTOSConfig.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/FreeRTOSConfig.h#L126-L138)
ของ CM33 อธิบายว่า "sets the highest interrupt priority from which interrupt safe FreeRTOS API functions can be called"

การตั้ง interrupt ของขา GPIO มีสองชั้น ชั้นขา (PDL) กับชั้น NVIC ของ CPU driver ของเรดาร์ใน SDK ทำตามลำดับนี้

| ขั้น | คำสั่ง (จาก `bento_bgt60trxx_platform.c` และ `radar_task.c`) |
|---|---|
| ล้างของค้าง ตั้งขา | `Cy_GPIO_ClearInterrupt()` แล้ว `Cy_GPIO_Pin_FastInit(..., CY_GPIO_DM_PULLDOWN, ...)` |
| เลือกขอบ เปิด mask ของขา | `Cy_GPIO_SetInterruptEdge(..., CY_GPIO_INTR_RISING)` และ `Cy_GPIO_SetInterruptMask(..., 1u)` |
| ผูก ISR กับแหล่ง interrupt | `Cy_SysInt_Init(&cfg, isr)` โดย `cfg.intrSrc` คือหมายเลข IRQ และ `cfg.intrPriority` คือลำดับความสำคัญ |
| เปิดที่ NVIC | `NVIC_ClearPendingIRQ()` แล้ว `NVIC_EnableIRQ()` |

### 3. กันเด้งแบบไม่บล็อก: นับ "เวลา" ไม่ใช่นับ "ครั้งที่อ่านติดกันเร็ว ๆ"

หน้าสัมผัสของปุ่มเด้งอยู่หลายมิลลิวินาทีหลังกดและหลังปล่อย การกันเด้งคือเชื่อค่าใหม่ก็ต่อเมื่อมัน **นิ่งนานพอ**
ตัวอย่างของ SDK อ่านทุก 10 ms และเชื่อเมื่อได้ค่าเดิมสามครั้งติดกัน รวม 30 ms และเตือนว่า "Debounce in TIME, not by reading the pin twice in a row:
two reads 200 ns apart are two samples of the same bounce." ([04_gpio_led_button.c บรรทัด 116-124](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c#L116-L124))

"ไม่บล็อก" แปลว่าตัวกันเด้งไม่รอเอง มันเก็บสถานะไว้ใน struct แล้วถูกเรียกหนึ่งครั้งต่อการอ่าน ผู้เรียกเป็นคนกำหนดจังหวะ
จะเป็น task ที่ `vTaskDelay(pdMS_TO_TICKS(10))` ระหว่างรอบ (แบบตัวอย่างของ SDK) หรือ timer ของ LVGL (แบบตัวอย่าง Button Monitor บน Developer Hub
ที่อ่านทุก 25 ms และเชื่อเมื่อตรงกันสอง tick) ก็ได้ ถ้าใช้ interrupt ของขาช่วย ISR ควรแค่ "ปลุก" task ที่ทำการกันเด้ง
เพราะการเด้งหนึ่งครั้งก่อ interrupt ได้หลายสิบครั้ง การนับใน ISR ตรง ๆ จะได้ตัวเลขเดียวกับการนับค่าดิบ

## ตัวอย่างสมบูรณ์

[examples/07_debounce_trace.c](examples/07_debounce_trace.c) ทำงานเป็นสามท่า

- **ท่าที่ 1** ตาราง `raw[]` คือค่าที่อ่านได้ทุก 10 ms มีทั้งการเด้งตอนกด ตอนปล่อย และสัญญาณรบกวนหนึ่งการอ่าน
- **ท่าที่ 2** `debounce_step()` รับค่าหนึ่งค่า ปรับสถานะใน struct แล้วคืนเหตุการณ์ ไม่มีการรอข้างใน
- **ท่าที่ 3** นับขอบขาขึ้นของค่าดิบเทียบกับจำนวน PRESS ที่กันเด้งแล้ว บนข้อมูลชุดเดียวกัน

ลองแก้แล้วทายก่อนรัน

1. เปลี่ยน `DEBOUNCE_POLLS` เป็น 1 นับได้กี่ครั้ง และแบบนี้ต่างจากไม่มีการกันเด้งอย่างไร
2. เปลี่ยนเป็น 10 เวลาของ PRESS เลื่อนไปเท่าไร ผู้ใช้จะรู้สึกอย่างไรกับปุ่มที่ตอบช้าขนาดนั้น
3. ต่อสัญญาณรบกวนในแถวสุดท้ายให้ยาวขึ้นเป็นสามการอ่านติดกัน ผลเปลี่ยนไหม แล้วคุณจะเลือกค่า `DEBOUNCE_POLLS` อย่างไร

## ฝึกเติม

เปิด [practice/07_debounce.c](practice/07_debounce.c) มีช่องให้เติม 3 จุดใน `debounce_step()` และ test สี่กรณี
กดสะอาด กดแบบเด้ง สัญญาณรบกวนสั้น และกดค้างหนึ่งแสนรอบ

```sh
gcc -std=c11 -Wall -Wextra -o debounce practice/07_debounce.c && ./debounce
```

## เฉลย

ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/07_debounce.c](solution/07_debounce.c)
จุดที่มักพลาดคือไม่หยุดนับ `agree` ที่ `DEBOUNCE_POLLS` ถ้า `agree` เป็นชนิดที่เล็ก (เช่น `uint8_t`) และกดค้างนาน ตัวนับจะวนกลับ
test กดค้างหนึ่งแสนรอบมีไว้จับข้อนี้ อีกจุดคือ test สัญญาณรบกวนผ่านตั้งแต่ก่อนเติม (โค้ดเปล่าคืน `EV_NONE` เสมอ)
test นั้นจึงมีความหมายก็ต่อเมื่อ test กรณีกดจริงผ่านด้วย

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) (บนเว็บไซต์อยู่ท้ายหน้านี้) ครอบคลุมเป้าหมายทั้งสามข้อ ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน

## แล็บ

**งาน:** วัดคุณภาพการกันเด้งบนบอร์ดจริง แล้วออกแบบการรับปุ่มด้วย interrupt ที่ส่งงานต่อให้ task

1. build ด้วย `make build -j ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/io/04_gpio_led_button` แล้ว flash ถอดสายเสียบใหม่
   (ขั้นตอนเต็มใน [บทเรียน 2.1](../../m02-build-and-version/l01-toolchain-first-build/README.md))
2. ในห้าวินาทีที่ตัวอย่างเฝ้าปุ่ม กด SW2 สามแบบ แบบละรอบ: ช้า ๆ ห้าครั้ง, เร็วที่สุดเท่าที่ทำได้, และแตะเบา ๆ จดจำนวนที่นับได้เทียบกับที่กดจริง
3. (ถ้ามีบอร์ดฐาน QWA309 ที่ใช้ปุ่มได้) flash ตัวอย่าง Button Monitor จาก Developer Hub (ลิงก์ท้ายหน้า) ซึ่งอ่านปุ่มที่ P17.5 และ P17.7
   ด้วย timer ทุก 25 ms แล้วทำการทดลองแบบเดียวกัน เทียบผลกับข้อ 2
4. ออกแบบบนกระดาษ (หรือเขียนโค้ดถ้าคุณพร้อม) การรับ SW2 ด้วย interrupt ขอบขาลง: ระบุคำสั่ง PDL ทุกขั้นตามตารางในแนวคิดข้อ 2
   โดยใช้ `CYBSP_USER_BTN1_PORT` `CYBSP_USER_BTN1_NUM` และ `CYBSP_USER_BTN1_IRQ` ของ BSP เขียน ISR ที่ล้าง flag แล้วปลุก task ด้วย `xSemaphoreGiveFromISR()`
   และให้ task เป็นคนเรียก `debounce_step()` อธิบายว่าทำไมไม่นับการกดใน ISR ตรง ๆ
   (ถ้าลองบนบอร์ด ให้บันทึกว่าคุณใช้ interrupt priority เท่าไร และผลที่ได้ หลักสูตรนี้ยังไม่ได้ทดสอบโค้ดชิ้นนี้บนบอร์ด)

**หลักฐานที่เก็บไว้ใน portfolio:** ตารางผลการกดทั้งสามแบบ (และของ Button Monitor ถ้าทำ) log จาก serial console และแบบร่าง ISR กับ task พร้อมคำอธิบาย

## ไปต่อ

- เปิด [`cy_gpio.h` @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_gpio.h) หาค่า `CY_GPIO_INTR_RISING`
  `CY_GPIO_INTR_FALLING` `CY_GPIO_INTR_BOTH` แล้วคิดว่าตัวกันเด้งที่ใช้ interrupt ควรฟังขอบไหน
- เอกสาร [FreeRTOS](https://www.freertos.org/Documentation/00-Overview) หัวข้อ task notifications เป็นทางเลือกที่เบากว่า semaphore สำหรับปลุก task หนึ่งตัว
  ใน SDK มีตัวอย่างการใช้ `xTaskNotifyFromISR()` อยู่ใน PAL ของ OPTIGA (`pal_i2c.c`)

บทถัดไป: [บทเรียน 4.2 Timer และสัญญาณนาฬิกา](../l02-timers-and-clocks/README.md)

## สะท้อนคิด

- ปุ่มแบบไหนในชีวิตประจำวันที่คุณเคยเจอว่า "กดครั้งเดียวทำงานสองครั้ง" และตอนนี้คุณเดาได้ไหมว่าผู้ออกแบบพลาดตรงไหน
- ถ้า ISR ต้องทำงานที่ใช้เวลาหนึ่งมิลลิวินาที คุณจะแบ่งงานนั้นระหว่าง ISR กับ task อย่างไร

## แหล่งอ้างอิง

- [SDK: cm33/io/04_gpio_led_button.c (drive mode และการกันเด้งแบบไม่บล็อก)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c)
- [SDK: ตัวอย่างฝั่ง CM33 (ข้อควรทราบเรื่องบริบท ISR)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/README.md)
- [SDK: tesaiot-radar/radar_task.c (ISR ของ data-ready และการตั้ง interrupt)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/radar_task.c)
- [SDK: cycfg_pins.h ของ BSP (ขาของปุ่มและ LED)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_pins.h)
- [Infineon mtb-pdl-cat1 (Peripheral Driver Library) @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/tree/release-v3.24.0)
- [Interrupt (Wikipedia)](https://en.wikipedia.org/wiki/Interrupt)

## ตัวอย่างบน TESAIoT Developer Hub

ลองของจริงบน TESAIoT Dev Kit: เปิดตัวอย่างบน Developer Hub เพื่ออ่านโค้ด ดาวน์โหลด หรือ flash เฟิร์มแวร์สำเร็จรูป

- [QWA309 — Push Button Monitor](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_button_monitor&q=prac_qwa309_button_monitor) — อ่านปุ่มสองปุ่มที่ P17.5 และ P17.7 แบบ active-low pull-up ด้วย timer ทุก 25 ms แสดงสถานะกด ปล่อย จำนวนครั้ง และเวลาที่กดค้างบน LVGL (ชื่อปุ่มบนแผ่นวงจรในเอกสารแต่ละแหล่งไม่ตรงกัน ให้ยึดหมายเลขขา)
- [QWA309 — Hardware Button Menu](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_hw_button_menu&q=prac_qwa309_hw_button_menu) — นำทางเมนู LVGL ด้วยปุ่มกายภาพ SW6=Move SW5=Select (ไม่ใช้ touch) — headless/kiosk UX pattern
