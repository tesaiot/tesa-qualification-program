---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 3.2 — แล็บ: GPIO และอุปกรณ์ต่อพ่วงบนฮาร์ดแวร์จริง"
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

# บทเรียน 3.2 — แล็บ: GPIO และอุปกรณ์ต่อพ่วงบนฮาร์ดแวร์จริง

## ลงมือทีละบล็อก: LED + ปุ่ม, UART log, แล้วเลือก PWM / ADC / I²C อย่างน้อยหนึ่งอย่าง ก่อนรวมเป็นมินิวงจร

**หลักสูตร TESA Firmware SDK สำหรับ Edge AI — โมดูล 3 · แล็บ**

---

## เป้าหมาย

เมื่อทำครบ คุณจะ

1. ทำให้ปุ่มสลับ LED บนบอร์ดจริงได้ (Lab A)
2. ส่ง log ทาง UART ที่อ่านได้บน terminal (Lab B)
3. ทำอุปกรณ์ต่อพ่วงเพิ่มอย่างน้อยหนึ่งชนิดจาก PWM, ADC หรือ I²C และจดชื่อฟังก์ชันจริงที่เรียก (Lab C)

---

## ก่อนเริ่ม

- [ ] ผ่านเกณฑ์ โมดูล 2
- [ ] โปรเจกต์ตัวอย่างที่ลิงก์ TESA Firmware SDK แล้ว
- [ ] สาย USB + serial terminal
- [ ] รู้คิตในมือ (AI vs Eval — มีผลต่อปุ่มที่สองและ POT)

> **หมายเหตุ:** snippet ในแล็บนี้ใช้ API ของเฟิร์มแวร์ TESAIoT Bitstream ซึ่งยังไม่เปิดซอร์ส ดูรายละเอียดและตัวอย่างเทียบใน SDK สาธารณะได้ที่หมายเหตุต้นบทเรียน [บทเรียน 3.1](../l01-gpio-and-peripherals/README.md)

---

## ดูของจริงก่อน — เกณฑ์ผ่านของแต่ละบล็อก

| บล็อก | เกณฑ์ผ่าน |
|---|---|
| Lab A (GPIO, required) | กดปุ่มแล้ว LED เปลี่ยนสถานะอย่างเสถียร |
| Lab B (UART, required) | เห็นข้อความตรงกับเหตุการณ์ปุ่ม |
| Lab C (เลือก ≥ 1, required) | ตามชนิดที่เลือก — ดูสไลด์ถัดไป |
| Lab D (มินิรวม, แนะนำ) | รวมผลจาก A+B กับ C เข้าด้วยกัน |

---

## ฝึกเติม/แล็บ (1) — Lab A: GPIO LED + Button

1. เรียก `led_controller_init` (ถ้าโปรเจกต์ยังไม่ init) และทดลอง `led_controller_set` / `led_controller_toggle`
2. เรียก `cm55_button_init` แล้วผูก `cm55_button_on_pressed(BUTTON_ID_0, …)` ให้สลับ LED
3. Flash แล้วสาธิตบนบอร์ด

```c
/* แนวทางสั้น — ดูรายละเอียดใน บทเรียน 3.1 หัวข้อ 2 */
(void)led_controller_init();
(void)cm55_button_init();
(void)cm55_button_on_pressed(BUTTON_ID_0, on_btn_pressed);
```

---

## ฝึกเติม/แล็บ (2) — Lab B: UART log

1. ในตัวจัดการปุ่ม (หรือ loop) พิมพ์ข้อความ เช่น `btn toggled`
2. เปิด terminal บนพอร์ต KitProg3 ตาม baud ของโปรเจกต์
3. ยืนยันว่าข้อความตรงกับเหตุการณ์ปุ่ม

```c
printf("btn toggled\r\n");
/* หรือ */ LOG_INFO("LAB", "btn toggled");
```

---

## ฝึกเติม/แล็บ (3) — Lab C: เลือกอย่างน้อยหนึ่งอย่าง

**C1 PWM**
```c
(void)bitstream_led_pwm_init();
(void)bitstream_led_pwm_set_brightness(0, 20);
(void)bitstream_led_pwm_set_brightness(0, 80);
```

**C2 ADC (Eval kit with POT)**
```c
(void)cm55_adc_init();
int16_t mv = cm55_adc_read_pot_mv();
printf("POT mV=%d\r\n", (int)mv);
```

**C3 I²C sensor** — `sensor_sht40_startup()` / `sensor_sht40_read(&s)` (หรือเซ็นเซอร์อื่นบนบอร์ดของคุณ เช่น `sensor_bmi270_*`)

---

## ฝึกเติม/แล็บ (4) — Lab D: Mini Integration (แนะนำ)

รวม A+B กับผลจาก C เช่น ADC → PWM duty หรือปุ่ม → สลับโหมด + UART log

หน่วงใน task:

```c
vTaskDelay(pdMS_TO_TICKS(50));
```

**Optional:** เปิด [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) ถ้าเฟิร์มแวร์ส่ง telemetry

**Short report (5–10 บรรทัด):** ชื่อ BSP/บอร์ด · ตารางงาน → ชื่อ API จริง (จาก API map) · ผล Lab A/B/C

---

## เช็กความเข้าใจ — ตรวจอาการก่อนขอความช่วยเหลือ

ถ้าติดปัญหา ให้ตอบตัวเองก่อนว่าน่าจะตรงแถวไหน:

1. LED ไม่ติด — อะไรที่ควรตรวจก่อน (id, active level, การ init)
2. ปุ่มไม่มี event — อะไรที่มักลืมทำ
3. UART เงียบ — อะไรที่มักเป็นสาเหตุ
4. I²C fail — อะไรที่มักลืมทำเมื่อเขียนไดรเวอร์ระดับต่ำเอง
5. ADC อ่านได้ 0 ตลอด — สาเหตุที่เป็นไปได้คืออะไร

---

## ไปต่อ

ก่อนส่งงาน ตรวจกับตัวเองว่า:

- [ ] Lab A ผ่าน
- [ ] Lab B ผ่าน
- [ ] Lab C ≥ 1 ข้อผ่าน
- [ ] กรอก [peripheral-api-map.md](../l01-gpio-and-peripherals/resources/peripheral-api-map.md)
- [ ] (แนะนำ) Lab D

พร้อมแล้ว ไปต่อ **โมดูล 4 — การเขียนเฟิร์มแวร์แบบ RTOS**

[บทเรียนโมดูล 4 →](../../m04-rtos/l01-freertos-programming/README.md)

---

## แหล่งที่มา

"บทเรียน 3.2 — แล็บ: GPIO และอุปกรณ์ต่อพ่วงบนฮาร์ดแวร์จริง" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C1 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
