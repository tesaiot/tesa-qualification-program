---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.1 — ภาษา C บนไมโครคอนโทรลเลอร์"
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

# บทเรียน 1.1 — ภาษา C บนไมโครคอนโทรลเลอร์

## ใช้ชนิดข้อมูลขนาดแน่นอน ตัวดำเนินการระดับบิต และ volatile กับรีจิสเตอร์ของอุปกรณ์

**โมดูล 1 — ภาษา C สำหรับไมโครคอนโทรลเลอร์และหน่วยความจำ**

หลักสูตร **พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge** · อ้างอิง TESAIoT PSE84 Dev Kit SDK

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. เลือกชนิดข้อมูลขนาดแน่นอนจาก `stdint.h` ให้เหมาะกับค่าที่เก็บ และอธิบายผลของ overflow ได้
2. เขียนการตั้ง ล้าง และสลับบิตด้วยตัวดำเนินการระดับบิตแบบ read-modify-write ได้ถูกต้อง
3. อธิบายว่าเมื่อใดต้องใช้ `volatile` กับตัวแปรที่ใช้ร่วมกับฮาร์ดแวร์หรือ interrupt

ใช้เวลาประมาณ 70 นาที (แนวคิด 15 · ฝึก 25 · แล็บ 25 · เช็ก 5) — ครึ่งแรกทำบนคอมพิวเตอร์ได้เลย ส่วนแล็บใช้บอร์ด TESAIoT Dev Kit

---

## ก่อนเริ่ม

บทเรียนนี้ต่อจากคนที่เขียน Python หรือ MicroPython ได้แล้ว ลองตอบในใจสองข้อ

1. ใน MicroPython `x = 250 + 10` ได้ 260 เสมอ ในภาษา C บนไมโครคอนโทรลเลอร์จะได้ 260 เสมอไหม ขึ้นกับอะไร
2. เวลาสั่ง `gpio.led(0).on()` แล้วไฟติด ในชิปต้องมีอะไรสักอย่างเปลี่ยนค่า คุณคิดว่าคืออะไร และอยู่ที่ไหน

**สิ่งที่ต้องมี:** คอมไพเลอร์ C บนคอมพิวเตอร์ (gcc หรือ clang) สำหรับครึ่งแรก และสำหรับแล็บคือบอร์ด TESAIoT Dev Kit กับ ModusToolbox™ 3.6

---

## ดูของจริงก่อน

ทายก่อนรัน: [examples/01_types_and_bits.c](examples/01_types_and_bits.c) บรรทัด `count after +10` จะพิมพ์เลขอะไร

```sh
gcc -std=c11 -Wall -Wextra -o types_and_bits examples/01_types_and_bits.c
./types_and_bits
```

ถ้าคุณทายว่า 260 คุณไม่ได้ผิดคนเดียว — โปรแกรมพิมพ์ `count after +10 = 4` เพราะ `uint8_t` เก็บได้แค่ 0 ถึง 255 ค่าที่เกินจึงวนกลับ

ไบต์ `0x30` กับ `0xF8` กลายเป็น -2000 และผลคูณ 32 บิตไม่เท่ากับผลคูณ 64 บิต — บทเรียนนี้คือคำอธิบายของทั้งสามบรรทัดนั้น

---

## แนวคิด (1) — ชนิดข้อมูลขนาดแน่นอนและ overflow

ภาษา C ไม่สัญญาว่า `int` กว้างกี่บิต แต่รีจิสเตอร์ ไบต์บนบัส และแพ็กเก็ตของโปรโตคอลถูกนิยามเป็นจำนวนบิตแน่นอน งานเฟิร์มแวร์จึงใช้ชนิดจาก `<stdint.h>`

| ค่าที่จะเก็บ | ชนิดที่เหมาะ |
|---|---|
| ไบต์บนบัส I2C หรือ UART | `uint8_t` |
| ค่าดิบเซนเซอร์ที่ติดลบได้ | `int16_t` |
| ตัวนับรอบ เวลาเป็น ms | `uint32_t` |
| ผลคูณกลางทางที่อาจเกิน 32 บิต | `uint64_t` |

**overflow** ของ unsigned นิยามไว้ว่าวนกลับแบบ modulo 2ᴺ เช่น `uint8_t` 250+10 = 4 ส่วน overflow ของ signed เป็น *undefined behaviour* — อย่าเขียนโค้ดที่พึ่งมัน

---

## แนวคิด (1) ต่อ — ตัวอย่างจาก SDK จริง

SDK ใช้ความรู้นี้จริงในหลายจุด:

- [`06_raw_register_access.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/06_raw_register_access.c#L243-L252)
  แปลงค่าจาก SHT40 ด้วยตัวแปรกลาง 64 บิต คอมเมนต์บอกเหตุผลว่า "175000 * 65535 does not fit in 32 bits"
- [`05_auto_push_task.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/05_auto_push_task.c#L110-L115)
  หาจำนวนรอบด้วย `sensor_auto_get_push_count() - before` ถูกต้องแม้ตัวนับจะวนกลับ เพราะการลบของ unsigned ก็เป็น modulo เหมือนกัน

(Apache-2.0, tesaiot-pse84-devkit-sdk @ `ef72c1b`)

---

## แนวคิด (2) — ตัวดำเนินการระดับบิตและ read-modify-write

รีจิสเตอร์หนึ่งตัวมักรวมหลายหน้าที่ไว้คนละบิต ถ้าเขียนทับทั้งตัว บิตของหน้าที่อื่นจะหายไปด้วย วิธีปลอดภัยคือ **read-modify-write**

| ทำอะไร | เขียนแบบนี้ |
|---|---|
| ตั้งบิต (set) | `reg \|= mask;` |
| ล้างบิต (clear) | `reg &= ~mask;` |
| สลับบิต (toggle) | `reg ^= mask;` |
| เขียนฟิลด์หลายบิต | ล้างฟิลด์ก่อน แล้ว OR ค่าที่เลื่อนและตัดด้วย mask |

บนชิปจริงเรามักไม่แตะรีจิสเตอร์เอง แต่เรียกฟังก์ชันของ **PDL (Peripheral Driver Library)** เช่น `Cy_GPIO_Set()` `Cy_GPIO_Clr()` — ใช้ชื่อ `CYBSP_LED_STATE_ON` แทนเลข 1 เพราะบอร์ดรุ่นถัดไปอาจกลับขั้ว

---

## แนวคิด (3) — volatile คือสัญญากับคอมไพเลอร์ ไม่ใช่กุญแจ

คอมไพเลอร์ที่เปิด optimisation มีสิทธิ์จำค่าตัวแปรไว้ในรีจิสเตอร์ของ CPU และตัดการอ่าน/เขียนที่ดูเหมือนไร้ผลทิ้ง `volatile` บอกว่า **ทุกการอ่านและเขียนต้องเกิดขึ้นจริงตามลำดับในโค้ด** ใช้เมื่อ

- **รีจิสเตอร์ของอุปกรณ์** ที่ฮาร์ดแวร์เปลี่ยนค่าเอง
- **ตัวแปรที่ ISR เขียนแล้ว task อ่าน** เช่น `radar_drdy_events`
- **ตัวแปรที่อีกคอร์หรือ DMA เขียน** เช่นธงที่ task หนึ่งตั้งแล้วอีก task อ่าน
- **ลูปหน่วงเวลาแบบนับเลขเปล่า** `for (volatile uint32_t d = 0; d < 300000; d++) {}`

volatile **ไม่ได้** ให้ความเป็น atomic — `count++` บน volatile ยังเป็นสามจังหวะ (เรื่องนี้อยู่ในบทเรียน 1.3 และโมดูล 4)

---

## ตัวอย่างสมบูรณ์ — ท่าที่ 1 ขนาดชนิดและ overflow

[examples/01_types_and_bits.c](examples/01_types_and_bits.c)

```c
uint8_t count = 250u;
count = (uint8_t)(count + 10u);           // วนกลับ (modulo 256)
printf("count after +10 = %u\n", (unsigned)count);

const uint8_t lsb = 0x30u, msb = 0xF8u;   // 0xF830 = -2000
const int16_t raw = (int16_t)((uint16_t)lsb | ((uint16_t)msb << 8));

const uint32_t t_raw = 65535u;
const uint32_t wrong = 175000u * t_raw;             // คูณใน 32 บิต วนกลับ
const uint64_t right = (uint64_t)175000u * t_raw;   // ขยายเป็น 64 บิตก่อนคูณ
```

---

## ตัวอย่างสมบูรณ์ — ท่าที่ 2/3 read-modify-write

```c
// ท่าที่ 2: set / clear / toggle
fake_ctrl |= CTRL_ENABLE_MSK;          // set
fake_ctrl &= ~(uint32_t)0x4u;          // clear bit 2
fake_ctrl ^= (1u << 8);                // toggle bit 8

// ท่าที่ 3: เขียนฟิลด์ MODE 3 บิต อ่านครั้งเดียว เขียนครั้งเดียว
uint32_t v = fake_ctrl;                        // read
v &= ~CTRL_MODE_MSK;                           // modify: ล้างฟิลด์
v |= (mode << CTRL_MODE_POS) & CTRL_MODE_MSK;  // modify: ใส่ค่าใหม่
fake_ctrl = v;                                 // write
```

อ่านต่อจากของจริงใน SDK: [`06_raw_register_access.c`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/06_raw_register_access.c#L176-L196) อ่านรีจิสเตอร์ `PWR_CTRL` ของ BMI270 เขียนค่าเดิมกลับ แล้วอ่านซ้ำเพื่อยืนยัน โดยถือ lock ของบัสตลอดทั้งขั้น

---

## ฝึกเติม

เปิด [practice/01_bitops.c](practice/01_bitops.c) — มีช่องให้เติม 2 จุดที่มีคำว่า `TODO` คือ `bits_set()` กับ `bits_clear()`

```sh
gcc -std=c11 -Wall -Wextra -o bitops practice/01_bitops.c && ./bitops
```

คอมไพล์และรัน**ก่อน**เติม คุณควรเห็น test ล้มหลายข้อ — นั่นคือหลักฐานว่า test ตรวจอะไรบางอย่างจริง

เติมจนบรรทัดสุดท้ายพิมพ์ `PASS: 0 failure(s)` — ลองเองก่อนอย่างน้อย 15 นาที แล้วค่อยเปิด [solution/01_bitops.c](solution/01_bitops.c)

---

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) ครอบคลุมเป้าหมายทั้งสามข้อ (ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน)

1. `uint8_t level = 200;` แล้ว `level = (uint8_t)(level + 100);` ค่าของ `level` คือเท่าไร
2. จับคู่ข้อมูลกับชนิดข้อมูล ข้อใดเหมาะสม (เลือกได้หลายข้อ)
3. บรรทัดใดล้างบิตที่ 3 ของ `reg` โดยไม่เปลี่ยนบิตอื่น
4. เรียงบรรทัดให้เป็นการเขียนฟิลด์ MODE แบบ read-modify-write ที่อ่านครั้งเดียวและเขียนครั้งเดียว
5. ตัวแปรใดควรประกาศเป็น `volatile` (เลือกได้หลายข้อ)

---

## แล็บ

**งาน:** รันตัวอย่าง GPIO และ register ของ SDK บนบอร์ด แล้วอธิบายผลที่เห็นด้วยความรู้ของบทนี้

```sh
cd bento-firmware-template-mtb-only
make build -j ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/io/04_gpio_led_button
make program
```

1. ถอดสาย USB ออกให้สุดแล้วเสียบใหม่หลัง flash ทุกครั้ง เปิด serial console ที่ 115200 8N1 ไว้ก่อน
2. อ่าน log ของ `[io/04]` แล้วกดปุ่ม SW2 สองสามครั้งใน 5 วินาที ดูจำนวนการกดที่กันเด้งแล้ว
3. build ใหม่ด้วย `SDK_EXAMPLE_CM33=cm33/sensors/06_raw_register_access` ดู chip id (ควรเป็น `0x24`) ค่าดิบ XYZ และบรรทัด `PWR_CTRL ... (verified, board unchanged)`
4. บันทึกว่าเมื่อวางบอร์ดราบ ค่าดิบแกนใดใหญ่ที่สุดและเป็นบวกหรือลบ

**หลักฐานที่เก็บไว้ใน portfolio:** log จาก serial console ของทั้งสองตัวอย่าง และคำตอบข้อ 4

---

## ไปต่อ

- เปิด [`cy_gpio.h` ของ mtb-pdl-cat1 @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_gpio.h) หา `Cy_GPIO_Pin_FastInit()` และ `CY_GPIO_DM_PULLUP` อ่านว่าพารามิเตอร์ `outVal` มีผลต่อโหมด pull-up อย่างไร
- โจทย์ท้าทาย: เขียนฟังก์ชัน `field_read(reg, msk, pos)` คู่กับ `field_write()` ในแบบฝึก แล้วเพิ่ม test ของมันเอง

บทถัดไป: [บทเรียน 1.2 — แผนที่หน่วยความจำ stack และ heap](../l02-memory-map-stack-heap/README.md) ถามต่อว่าตัวแปรแต่ละตัวในบทนี้อยู่ที่ไหนในหน่วยความจำ

---

## แหล่งที่มาและเครดิต

"พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

โค้ดของหลักสูตรนี้ (`examples/`, `practice/`, `solution/`) Apache-2.0 · โค้ดของ SDK ไม่ได้คัดลอกเป็นไฟล์
บทเรียนยกมาเป็นช่วงสั้น ๆ พร้อมลิงก์ไปยังไฟล์ที่ commit `ef72c1b` (Apache-2.0, tesaiot-pse84-devkit-sdk)
