---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 4.1 — GPIO และ interrupt"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0"
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
<!-- _backgroundColor: #0d1117 -->

# บทเรียน 4.1 — GPIO และ interrupt

## ขับหลอดไฟ อ่านปุ่ม และรับเหตุการณ์ด้วย interrupt ตามกติกาของบริบท ISR

**โมดูล 4 — Timer, Interrupt, Watchdog, DMA และสัญญาณนาฬิกา**

หลักสูตร **พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ตั้งค่าขา GPIO ด้วยคำสั่ง PDL ให้เป็นขาออกและขาเข้าที่มี drive mode ถูกต้อง
2. เขียน ISR ที่สั้น ไม่บล็อก และส่งงานต่อให้ task แทนการทำงานหนักใน ISR
3. กันเด้งปุ่มโดยไม่ใช้การรอแบบบล็อก

ใช้เวลาประมาณ 70 นาที

---

## ก่อนเริ่ม

ทวนจากโมดูลก่อนหน้าสองข้อ

1. ถ้า ISR กับ task ใช้ตัวแปรร่วมกัน ต้องประกาศอย่างไร และ `volatile` อย่างเดียวพอไหม
2. ตอนที่ CM33 หยุดที่ breakpoint ในลูปอ่านปุ่ม การกดปุ่มหายไปได้อย่างไร

---

## ดูของจริงก่อน

เปิด [examples/07_debounce_trace.c](examples/07_debounce_trace.c) — ป้อนค่าที่ "อ่านจากขา" ทุก 10 ms จากตารางที่จำลองการกดหนึ่งครั้งที่หน้าสัมผัสเด้งทั้งตอนกดและตอนปล่อย **ทายก่อนรัน**: นับแบบค่าดิบจะได้กี่ครั้ง และแบบกันเด้งได้กี่ครั้ง

```sh
gcc -std=c11 -Wall -Wextra -o debounce_trace examples/07_debounce_trace.c
./debounce_trace
```

ค่าดิบนับได้ 6 ครั้ง ส่วนแบบกันเด้งได้ 1 ครั้ง พร้อมเวลาของ PRESS/RELEASE ที่ช้ากว่าการแตะครั้งแรกราว 30 ms — สังเกตว่าไม่มี `delay` เลยสักบรรทัด ตัวกันเด้งทั้งตัวคือฟังก์ชันที่ถูกเรียกหนึ่งครั้งต่อการอ่าน แล้วคืนทันที

---

## แนวคิด (1) — drive mode คือทั้งหมดของงาน GPIO

ขาหนึ่งขาต้องตั้งสามอย่าง: ขาเป็นของใคร (HSIOM), ขับไฟแบบไหน (drive mode), ค่าเริ่มต้น — `Cy_GPIO_Pin_FastInit(port, pin, driveMode, outVal, hsiom)` รวมไว้ในคำสั่งเดียว SDK ตั้งหัวข้อว่า **"DRIVE MODES ARE THE WHOLE JOB"**

| ใช้ขาเป็น | drive mode | ข้อควรรู้ |
|---|---|---|
| ขาออกขับ LED | `CY_GPIO_DM_STRONG` | `outVal` เป็นค่าดับ ขาจะไม่กะพริบตอนเริ่ม |
| ขาเข้าของปุ่มลงกราวด์ | `CY_GPIO_DM_PULLUP` | `outVal` ต้องเป็น 1 เพราะเปิด pull-up ถ้าส่ง 0 ปุ่มจะดูเหมือนถูกกดตลอด |
| ขาเข้าที่มีตัวต้านทานภายนอก | `CY_GPIO_DM_HIGHZ` | ไม่มี pull ภายใน |
| ขาเข้าสัญญาณ active-high | `CY_GPIO_DM_PULLDOWN` | driver ของเรดาร์ใช้แบบนี้ |

> ใช้ค่าขั้วจาก BSP (`CYBSP_BTN_PRESSED`, `CYBSP_LED_STATE_ON`) แทนการเขียนเลขเอง — "Print the silkscreen name to a user."

---

## ตัวอย่างสมบูรณ์ — drive mode จริงจาก SDK

```c
static void leds_init(void)
{
    for (unsigned i = 0U; i < LED_COUNT; i++) {
        Cy_GPIO_Pin_FastInit(s_leds[i].port, s_leds[i].pin,
                             CY_GPIO_DM_STRONG,
                             CYBSP_LED_STATE_OFF,   /* dark from the first cycle */
                             HSIOM_SEL_GPIO);
    }
}

static void button_init(void)
{
    /* outVal = CYBSP_BTN_OFF (1) is what energises the pull-up. */
    Cy_GPIO_Pin_FastInit(CYBSP_USER_BTN1_PORT, CYBSP_USER_BTN1_NUM,
                         CY_GPIO_DM_PULLUP, CYBSP_BTN_OFF, HSIOM_SEL_GPIO);
}
```

ที่มา: [04_gpio_led_button.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c#L126-L141) (Apache-2.0, tesaiot-pse84-devkit-sdk)

---

## แนวคิด (2) — ISR ที่ดี: สั้น ไม่รอ ไม่พิมพ์ แล้วส่งงานต่อ

ISR ขัดจังหวะทุกอย่างที่มีความสำคัญต่ำกว่า — กติกาของ SDK: **"Never `printf` from an IPC callback (ISR context)"** และฟังก์ชัน `_from_isr` คือฟังก์ชันที่ **"takes no mutex, allocates nothing, and prints nothing"**

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

มันทำสองอย่าง: บันทึกว่าเกิดเหตุการณ์ (ตัวนับ `volatile` ที่หยุดที่ค่าสูงสุด ไม่วนกลับ) และล้าง interrupt flag — ถ้าไม่ล้าง ISR จะถูกเรียกซ้ำไม่รู้จบ งานหนักทั้งหมดอยู่ใน task

---

## แนวคิด (2) ต่อ — ปลุก task และลำดับการเปิด interrupt

เมื่อต้องปลุก task ทันที ใช้ API ของ FreeRTOS ที่ลงท้าย `FromISR` แล้วเรียก `portYIELD_FROM_ISR()` — ตัวอย่าง SDK ใช้ `xSemaphoreGiveFromISR()` และ `xQueueSendFromISR()` พร้อมกำกับ "No printf here — this is ISR context"

ISR ที่เรียก API แบบ `FromISR` ต้องมีลำดับความสำคัญไม่สูงกว่า `configMAX_SYSCALL_INTERRUPT_PRIORITY`

| ขั้น | คำสั่ง |
|---|---|
| ล้างของค้าง ตั้งขา | `Cy_GPIO_ClearInterrupt()` แล้ว `Cy_GPIO_Pin_FastInit(..., CY_GPIO_DM_PULLDOWN, ...)` |
| เลือกขอบ เปิด mask ของขา | `Cy_GPIO_SetInterruptEdge(..., CY_GPIO_INTR_RISING)`, `Cy_GPIO_SetInterruptMask(..., 1u)` |
| ผูก ISR กับแหล่ง interrupt | `Cy_SysInt_Init(&cfg, isr)` |
| เปิดที่ NVIC | `NVIC_ClearPendingIRQ()` แล้ว `NVIC_EnableIRQ()` |

---

## แนวคิด (3) — กันเด้งแบบไม่บล็อก: นับ "เวลา" ไม่ใช่ "ครั้งที่อ่านติดกัน"

หน้าสัมผัสของปุ่มเด้งอยู่หลายมิลลิวินาทีหลังกดและหลังปล่อย การกันเด้งคือเชื่อค่าใหม่ก็ต่อเมื่อมัน **นิ่งนานพอ** — SDK อ่านทุก 10 ms และเชื่อเมื่อได้ค่าเดิมสามครั้งติดกัน (รวม 30 ms) และเตือนว่า

> **"Debounce in TIME, not by reading the pin twice in a row: two reads 200 ns apart are two samples of the same bounce."**

"ไม่บล็อก" แปลว่าตัวกันเด้งไม่รอเอง — มันเก็บสถานะไว้ใน struct แล้วถูกเรียกหนึ่งครั้งต่อการอ่าน ผู้เรียกเป็นคนกำหนดจังหวะ (task ที่ `vTaskDelay` หรือ timer ของ LVGL) ถ้าใช้ interrupt ของขาช่วย ISR ควรแค่ **"ปลุก" task ที่ทำการกันเด้ง** เพราะการเด้งหนึ่งครั้งก่อ interrupt ได้หลายสิบครั้ง

---

## ตัวอย่างสมบูรณ์ — สามท่าใน 07_debounce_trace.c

**ท่าที่ 1** ตาราง `raw[]` คือค่าที่อ่านได้ทุก 10 ms มีการเด้งตอนกด ตอนปล่อย และสัญญาณรบกวนหนึ่งการอ่าน
**ท่าที่ 2** `debounce_step()` รับค่าหนึ่งค่า ปรับสถานะใน struct แล้วคืนเหตุการณ์ ไม่มีการรอข้างใน
**ท่าที่ 3** นับขอบขาขึ้นของค่าดิบเทียบกับจำนวน PRESS ที่กันเด้งแล้ว บนข้อมูลชุดเดียวกัน

ลองแก้แล้วทายก่อนรัน: เปลี่ยน `DEBOUNCE_POLLS` เป็น 1 นับได้กี่ครั้ง และต่างจากไม่มีการกันเด้งอย่างไร — เปลี่ยนเป็น 10 เวลาของ PRESS เลื่อนไปเท่าไร ผู้ใช้จะรู้สึกอย่างไรกับปุ่มที่ตอบช้าขนาดนั้น

---

## ฝึกเติม

เปิด [practice/07_debounce.c](practice/07_debounce.c) — มีช่องให้เติม 3 จุดใน `debounce_step()` และ test สี่กรณี: กดสะอาด, กดแบบเด้ง, สัญญาณรบกวนสั้น, กดค้างหนึ่งแสนรอบ

```sh
gcc -std=c11 -Wall -Wextra -o debounce practice/07_debounce.c && ./debounce
```

ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/07_debounce.c](solution/07_debounce.c) — จุดที่มักพลาด: ไม่หยุดนับ `agree` ที่ `DEBOUNCE_POLLS` ถ้าเป็นชนิดเล็ก (`uint8_t`) และกดค้างนาน ตัวนับจะวนกลับ — test กดค้างหนึ่งแสนรอบมีไว้จับข้อนี้

---

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) ครอบคลุมเป้าหมายทั้งสามข้อ (ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน)

1. ปุ่มต่อจากขาลงกราวด์ ไม่มีตัวต้านทานภายนอก การเรียกใดตั้งขานี้ได้ถูกต้อง
2. ทำไมตัวอย่าง GPIO ของ SDK ให้ `outVal` ของ LED เป็น `CYBSP_LED_STATE_OFF` และใช้ชื่อนี้แทนเลข 0
3. ข้อใดควรอยู่ใน ISR ของขา GPIO (เลือกได้หลายข้อ)
4. เรียงขั้นการเปิด interrupt ของขา GPIO ตามแบบของ driver เรดาร์ใน SDK
5. อ่านปุ่มทุก 10 ms และเชื่อเมื่อค่าตรงกัน 3 ครั้งติด ถ้าปุ่มเด้ง 5 ms หลังกด การกดจะถูกรายงานหลังจากแตะครั้งแรกนานราวเท่าไร

---

## แล็บ

**งาน:** วัดคุณภาพการกันเด้งบนบอร์ดจริง แล้วออกแบบการรับปุ่มด้วย interrupt ที่ส่งงานต่อให้ task

1. build ด้วย `SDK_EXAMPLE_CM33=cm33/io/04_gpio_led_button` flash ถอดสายเสียบใหม่
2. ในห้าวินาทีที่ตัวอย่างเฝ้าปุ่ม กด SW2 สามแบบ: ช้า ๆ ห้าครั้ง, เร็วที่สุดเท่าที่ทำได้, แตะเบา ๆ จดจำนวนที่นับได้เทียบกับที่กดจริง
3. (ถ้ามีบอร์ดฐาน QWA309) flash ตัวอย่าง Button Monitor จาก Developer Hub ที่อ่านทุก 25 ms ทำการทดลองแบบเดียวกัน เทียบผล
4. ออกแบบบนกระดาษการรับ SW2 ด้วย interrupt ขอบขาลง: ระบุคำสั่ง PDL ทุกขั้น เขียน ISR ที่ล้าง flag แล้วปลุก task ด้วย `xSemaphoreGiveFromISR()` อธิบายว่าทำไมไม่นับการกดใน ISR ตรง ๆ

**หลักฐานที่เก็บไว้ใน portfolio:** ตารางผลการกดทั้งสามแบบ log จาก serial console และแบบร่าง ISR กับ task พร้อมคำอธิบาย

---

## ไปต่อ

- เปิด [`cy_gpio.h` @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_gpio.h) หาค่า `CY_GPIO_INTR_RISING/FALLING/BOTH` แล้วคิดว่าตัวกันเด้งที่ใช้ interrupt ควรฟังขอบไหน
- เอกสาร [FreeRTOS](https://www.freertos.org/Documentation/00-Overview) หัวข้อ task notifications — ทางเลือกที่เบากว่า semaphore ในการปลุก task หนึ่งตัว

บทถัดไป: [บทเรียน 4.2 — Timer และสัญญาณนาฬิกา](../l02-timers-and-clocks/README.md)

---

## แหล่งที่มาและเครดิต

"พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

โค้ดของหลักสูตรนี้ (`examples/`, `practice/`, `solution/`) Apache-2.0 · โค้ดของ SDK ไม่ได้คัดลอกเป็นไฟล์
บทเรียนยกมาเป็นช่วงสั้น ๆ พร้อมลิงก์ไปยังไฟล์ที่ commit `ef72c1b` (Apache-2.0, tesaiot-pse84-devkit-sdk)
