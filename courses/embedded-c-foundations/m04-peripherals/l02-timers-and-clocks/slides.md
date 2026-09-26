---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 4.2 — Timer และสัญญาณนาฬิกา"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY 4.0"
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

# บทเรียน 4.2 — Timer และสัญญาณนาฬิกา

## ทำงานเป็นจังหวะด้วย timer ของฮาร์ดแวร์และของ RTOS และเข้าใจว่าสัญญาณนาฬิกากำหนดความแม่นยำอย่างไร

**โมดูล 4 — Timer, Interrupt, Watchdog, DMA และสัญญาณนาฬิกา**

หลักสูตร **พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge** · ต่อจากบทเรียน 4.1

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. คำนวณค่าตั้ง timer จากความถี่สัญญาณนาฬิกาและช่วงเวลาที่ต้องการได้
2. เลือกระหว่าง timer ของฮาร์ดแวร์กับ software timer ของ RTOS ให้เหมาะกับงาน พร้อมเหตุผล
3. อธิบายผลของการตั้งอัตราการทำงานของ task เบื้องหลังต่อภาระของระบบ

ใช้เวลาประมาณ 70 นาที

---

## ก่อนเริ่ม

ทวนจากบทก่อนหน้าสองข้อ

1. ตัวกันเด้งในบทเรียน 4.1 อ่านปุ่มทุก 10 ms ใครเป็นคนกำหนดจังหวะ 10 ms นั้น ตัวกันเด้งเองหรือผู้เรียก
2. `175000 * 65535` ล้น 32 บิต แล้ว `65536 * 1000000` ล่ะ

---

## ดูของจริงก่อน

เปิด [examples/08_timer_math.c](examples/08_timer_math.c) ตัวเลขทุกตัวอ่านมาจากไฟล์ที่ Device Configurator สร้างไว้ใน BSP **ทายก่อนรัน**: `GENERAL_PURPOSE_TIMER` ที่ BSP ตั้งไว้จะ overflow ทุกกี่มิลลิวินาที

```sh
gcc -std=c11 -Wall -Wextra -o timer_math examples/08_timer_math.c
./timer_math
```

ได้ 1000 ms พอดี และบรรทัดถัดมาแสดงว่าสัญญาณนาฬิกา 100 MHz ตัวเดียวกัน ผ่านตัวหารคนละค่า กลายเป็นจังหวะของ PWM, UART 115200, I2C 400 kHz และ SPI 25 MHz — ความถี่ของ UART ไม่ลงตัวพอดี คลาดไป -0.22% ซึ่งเป็นผลของการหารเลขจำนวนเต็ม

---

## แนวคิด (1) — จากสัญญาณนาฬิกาถึงเวลา: สองสูตร

อุปกรณ์กลุ่มหนึ่ง (TCPWM0, UART console, SPI เรดาร์) ใช้สัญญาณนาฬิกา CLK_HF10 ตั้งไว้ที่ 100 MHz แต่ละอุปกรณ์มีตัวหารของตัวเอง — ค่า N **"causes integer division of (divider value + 1)"**

- ความถี่ที่ timer ได้: **f_cnt = f_src / (N + 1)**
- เวลาต่อหนึ่งรอบของ timer ที่นับขึ้นจาก 0 ถึง period: **T = (period + 1) / f_cnt**

ตัวอย่างจริงใน BSP: `GENERAL_PURPOSE_TIMER` (TCPWM0 counter 2) ใช้ตัวหาร 9999 → 100 MHz / 10000 = 10 kHz ตั้ง `period = 9999` → 10000 จังหวะที่ 10 kHz คือ 1 วินาที

> ช่วงเวลาเดียวกันทำได้หลายคู่ของตัวหารกับ period และความแม่นยำของทุกอย่างในสายนี้**ไม่ดีไปกว่าต้นทาง** — watchdog ที่ใช้ oscillator ภายในความแม่นยำต่ำ คลาดได้ถึง ±30%

---

## แนวคิด (2) — timer ของฮาร์ดแวร์ หรือ software timer ของ RTOS

FreeRTOS ตั้ง `configTICK_RATE_HZ` เป็น 1000 (หนึ่ง tick = 1 ms) — ทุกอย่างที่อิง tick จึงละเอียดได้ไม่เกินหนึ่ง tick

| ต้องการ | ใช้ | เหตุผล |
|---|---|---|
| PWM, จังหวะระดับไมโครวินาที | hardware timer (TCPWM) | ฮาร์ดแวร์นับเองไม่ขึ้นกับภาระ CPU แต่มีจำนวนจำกัด |
| งานเป็นระยะ ms ขึ้นไปใน task | `vTaskDelayUntil()` | task มี stack ของตัวเอง รอ/บล็อกได้ |
| เรียกสั้น ๆ เป็นระยะ ไม่อยากสร้าง task | `xTimerCreate()` | callback ทำงานใน timer service task ห้ามบล็อก (แชร์ task เดียวกันทุกตัว) |
| งานเป็นระยะบนจอ CM55 | `lv_timer_create()` | ต้องอยู่ใน GFX task และห้ามบล็อก |

---

## แนวคิด (2) ต่อ — vTaskDelay vs vTaskDelayUntil

`vTaskDelay()` **"specifies a wake time relative to the time at which the function is called"** ส่วน `xTaskDelayUntil()` **"specifies the absolute (exact) time at which it wishes to unblock"**

ลูปที่ทำงาน 5 ms แล้ว `vTaskDelay(100 ms)` จึงวนทุก **105 ms ไม่ใช่ 100 ms** และเลื่อนไปเรื่อย ๆ — แม่แบบเปิด `INCLUDE_vTaskDelayUntil` ไว้แล้วในไฟล์ config

---

## แนวคิด (3) — อัตราของ task เบื้องหลัง คือภาระของทั้งระบบ

task ที่อ่านเซนเซอร์ทุก P ms และแต่ละรอบใช้เวลา C ms ครอบครองทั้ง CPU และบัส I2C เป็นสัดส่วนราว C/P

- **ลูปหน่วงหลังอ่าน ไม่ใช่ระหว่างอ่าน** — ถ้าได้รอบน้อยกว่าที่คาด "the reads themselves are costing more than the interval"
- **หน้าผาที่ 50 ms** — `sensor_auto_set_rate()` รับ 20-5000 ms แต่ต่ำกว่า 50 ms ลูป "reads ONLY the accelerometer" ตั้ง 20 ms เพื่อให้เร็วขึ้น ผลคือเซนเซอร์ 5 จาก 6 ตัวหยุดส่งเงียบ ๆ
- **ผู้อ่านสองรายบนบัสเดียว** — "Two readers on one bus at two rates is a bug waiting for a deadline; one publisher and many consumers is not."

> อัตรายังผูกกับความถูกต้อง: โมเดล IMU ฝึกด้วยข้อมูล 50 Hz ถ้าปล่อยข้อมูลมาทุก 100 ms **"every verdict is computed over five times the intended span of time and is confidently wrong"**

---

## ตัวอย่างสมบูรณ์ — สามท่าใน 08_timer_math.c

```c
// ท่าที่ 1: สูตรตัวหาร N + 1 ของ PDL
double divided_hz(double f_src, uint32_t divider_n) {
    return f_src / (double)(divider_n + 1);
}

// ท่าที่ 2: GENERAL_PURPOSE_TIMER — divider=9999, period=9999
double f_cnt = divided_hz(100e6, 9999);          // 10 kHz
double period_ms = 1000.0 * (9999 + 1) / f_cnt;  // 1000 ms

// ท่าที่ 3: baud ของ UART จากสัญญาณนาฬิกาเดียวกัน (divider=86, oversample=10)
double baud = divided_hz(100e6, 86) / 10.0;
```

ลองแก้แล้วทายก่อนรัน: ถ้าต้องการให้ `GENERAL_PURPOSE_TIMER` เกิดทุก 250 ms โดยไม่เปลี่ยนตัวหาร period ต้องเป็นเท่าไร

---

## ฝึกเติม

เปิด [practice/08_timer_math.c](practice/08_timer_math.c) — มีช่องให้เติม 4 จุด เขียนด้วยเลขจำนวนเต็มล้วนแบบเฟิร์มแวร์

1. `divided_hz()` ตามสูตรตัวหาร
2. `overflow_us()` ต้องใช้ตัวกลาง 64 บิต
3. `pick_timer()` หาตัวหารที่เล็กที่สุดที่ได้ช่วงเวลาพอดีเป๊ะด้วย period 16 บิต และบอกตรง ๆ เมื่อทำไม่ได้
4. `baud_error_ppm()` ความคลาดเคลื่อนเป็นส่วนในล้าน

```sh
gcc -std=c11 -Wall -Wextra -o timer_math practice/08_timer_math.c && ./timer_math
```

test ของ 1 วินาทีคาดหวังตัวหาร 1599 กับ period 62499 (ไม่ใช่ 9999/9999 แบบใน BSP) — ทั้งสองคู่ได้ 1 วินาทีพอดี แต่กติกาของแบบฝึกคือเลือกตัวหารที่เล็กที่สุด ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/08_timer_math.c](solution/08_timer_math.c)

---

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) ครอบคลุมเป้าหมายทั้งสามข้อ (ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน)

1. สัญญาณนาฬิกาต้นทาง 100 MHz ผ่านตัวหาร 4999 เข้า timer ที่นับขึ้นจาก 0 ถึง period ต้องการ 10 ms period ต้องเป็นเท่าไร
2. UART ใช้ 100 MHz ตัวหารค่า 86 และ oversample 10 ได้ baud เท่าไรโดยประมาณ และคลาดจาก 115200 เท่าไร
3. งานใดเหมาะกับ timer ของฮาร์ดแวร์ (TCPWM) มากกว่า software timer ของ RTOS (เลือกได้หลายข้อ)
4. task หนึ่งทำงาน 8 ms แล้วเรียก `vTaskDelay(pdMS_TO_TICKS(50))` ทุกรอบ รอบจริงยาวเท่าไร และควรใช้อะไรแทนถ้าต้องการรอบละ 50 ms พอดี
5. ผู้ใช้ตั้ง `sensor_auto_set_rate(20)` เพื่อให้ค่าเซนเซอร์ทุกตัวเร็วขึ้น จากตัวอย่าง 05_auto_push_task จะเกิดอะไร

---

## แล็บ

**งาน:** วัดอัตราจริงของ task เบื้องหลังบนบอร์ด แล้วอธิบายส่วนต่างระหว่างอัตราที่ตั้งกับอัตราที่ได้

1. build ด้วย `SDK_EXAMPLE_CM33=cm33/sensors/05_auto_push_task` flash ถอดสายเสียบใหม่
2. จาก serial console จดค่า `rate` เริ่มต้น mask ของเซนเซอร์ และบรรทัด `measured ... cycles in 1000 ms` ทั้งตอนอัตราเดิมและตอนปรับเป็น 25 ms
3. คำนวณจาก "expected" กับ "measured" ว่าแต่ละรอบใช้เวลาจริงกี่มิลลิวินาที แล้วประมาณเวลาที่การอ่านเซนเซอร์กินต่อรอบ (C)
4. ตอบว่าตอนอัตรา 25 ms เซนเซอร์ตัวไหนยังถูกอ่าน และทำไมจำนวนรอบที่วัดได้จึงใกล้หรือห่างจากที่คาด
5. ตรวจว่าตัวอย่างคืนค่าทุกอย่างกลับเหมือนเดิม (`--- restored ---`) ถ้าไม่ครบ จะรายงาน `RESTORE INCOMPLETE`

**หลักฐานที่เก็บไว้ใน portfolio:** log ของตัวอย่างทั้งหมด ตารางการคำนวณข้อ 3 และคำอธิบายข้อ 4

---

## ไปต่อ

- เอกสาร [FreeRTOS](https://www.freertos.org/Documentation/00-Overview) หัวข้อ software timers — timer command queue และเหตุผลที่ callback ห้ามบล็อก
- โจทย์ท้าทาย: เขียน task ที่ทำงานทุก 20 ms ด้วย `vTaskDelayUntil()` แล้ววัดด้วย `xTaskGetTickCount()` ว่าคลาดไปเท่าไรใน 1000 รอบ เทียบกับ `vTaskDelay()`

บทถัดไป: [บทเรียน 4.3 — Watchdog](../l03-watchdog/README.md)

---

## แหล่งที่มาและเครดิต

"พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

โค้ดของหลักสูตรนี้ (`examples/`, `practice/`, `solution/`) Apache-2.0 · โค้ดของ SDK ไม่ได้คัดลอกเป็นไฟล์
บทเรียนยกมาเป็นช่วงสั้น ๆ พร้อมลิงก์ไปยังไฟล์ที่ commit `ef72c1b` (Apache-2.0, tesaiot-pse84-devkit-sdk)
