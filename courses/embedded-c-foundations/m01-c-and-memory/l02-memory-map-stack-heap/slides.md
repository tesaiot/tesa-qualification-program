---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.2 — แผนที่หน่วยความจำ stack และ heap"
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

# บทเรียน 1.2 — แผนที่หน่วยความจำ stack และ heap

## รู้ว่าข้อมูลแต่ละก้อนอยู่ที่ใด และป้องกัน stack ล้นกับการจองหน่วยความจำในที่ที่ไม่ควร

**โมดูล 1 — ภาษา C สำหรับไมโครคอนโทรลเลอร์และหน่วยความจำ**

หลักสูตร **พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge** · ต่อจากบทเรียน 1.1

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. จำแนกตัวแปรในโปรแกรมตัวอย่างได้ว่าอยู่ใน stack, heap หรือหน่วยความจำแบบ static
2. อ่านค่าพื้นที่ stack ที่เหลือของ task จากตัวนับที่ SDK ให้มา และตัดสินได้ว่าใกล้ล้นหรือไม่
3. อธิบายว่าทำไมไม่ควรจองหน่วยความจำแบบ dynamic ใน ISR หรือในลูปเวลาจริง

ใช้เวลาประมาณ 70 นาที (แนวคิด 15 · ฝึก 25 · แล็บ 25 · เช็ก 5)

---

## ก่อนเริ่ม

ทวนจากบทเรียน 1.1 สองข้อ

1. `uint8_t` บวกเกิน 255 แล้วเกิดอะไรขึ้น และทำไมตัวอย่างของ SDK จึงขยายเป็น 64 บิตก่อนคูณ
2. ตัวแปรแบบไหนที่ต้องเป็น `volatile` และ `volatile` ช่วยเรื่อง `count++` ที่ถูก interrupt แทรกได้หรือไม่

---

## ดูของจริงก่อน

เปิด [examples/02_where_it_lives.c](examples/02_where_it_lives.c) **ทายก่อนรัน**: ที่อยู่ของ `local_buf` (ตัวแปร local ใน `main`) กับ `g_zeroed` (ตัวแปร global) ตัวไหนมีค่ามากกว่า

```sh
gcc -std=c11 -Wall -Wextra -o where_it_lives examples/02_where_it_lives.c
./where_it_lives
```

ตัวเลขบนเครื่องคุณจะไม่ตรงกับเพื่อน แต่ที่อยู่จะแบ่งเป็นกลุ่มชัดเจน — ค่าคงที่กับตัวแปร global อยู่ใกล้กัน ก้อนที่ `malloc` ได้อยู่อีกย่าน ตัวแปร local อยู่ไกลออกไปอีกย่าน และ `depth 1, 2, 3` แสดงว่ายิ่งเรียกฟังก์ชันลึก ที่อยู่ของ stack frame ยิ่ง **ลดลง**

บนไมโครคอนโทรลเลอร์ไม่มีระบบปฏิบัติการสุ่มตำแหน่งให้ — **linker script เป็นคนวางทุกกลุ่ม** และเราอ่านมันได้

---

## แนวคิด (1) — แผนที่หน่วยความจำ

| ส่วน (section) | เก็บอะไร | อยู่ที่ไหนบน PSOC™ Edge E84 |
|---|---|---|
| `.text` `.rodata` | โค้ด ค่าคงที่ `const` | flash ภายนอก QSPI (CPU รันโค้ดจากตรงนั้นได้เลย — XIP) |
| `.data` | static ที่มีค่าเริ่มต้น เช่น `int g = 42;` | ค่าเริ่มต้นอยู่ flash คัดลอกมา RAM ตอนบูต |
| `.bss` | static ที่ไม่ได้ให้ค่า หรือให้ 0 | RAM ล้างเป็นศูนย์ตอนบูต ไม่กินที่ flash |
| heap | ก้อนที่ได้จาก `malloc()` | RAM ส่วนที่เหลือหลัง `.bss` |
| stack | ตัวแปร local ที่อยู่คืนค่า | บนสุดของ RAM ก้อนนั้น โตลงหาที่อยู่ต่ำ |

อ่านได้จริงจาก [pse84_ns_cm33.ld](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/COMPONENT_CM33/TOOLCHAIN_GCC_ARM/pse84_ns_cm33.ld#L346-L361) — `.data` วางเป็น `> m33_data AT > m33_nvm_sel`, stack เริ่มที่ `__StackTop` ขนาดเริ่มต้น `0x1000` ไบต์

---

## แนวคิด (1) ต่อ — ทุกไบต์ของ .bss กินไบต์ของ heap

คอมเมนต์ในตัว linker script (บรรทัด 265) บันทึกจากบอร์ดจริงไว้ว่า **"every byte of .bss costs a byte of heap one for one"**

เมื่อเพิ่มหน้าจอใหม่เข้าไป heap เหลือน้อยจน mTLS ล้มด้วย

```text
WARN: Malloc failed arena=121812 used=121308 free=504 largest_free=0
```

คอมเมนต์สรุปว่า "Eleven rounds of code review could not see that; the board said it in ten minutes."

> ตัวแปร static ไม่ฟรี มันกินที่จากคนอื่นเสมอ

---

## แนวคิด (2) — stack ต่อ task และ high-water mark

ใน FreeRTOS **แต่ละ task มี stack ของตัวเอง** เป็นจำนวน word (4 ไบต์บน CPU 32 บิต) เช่น `xTaskCreate(bento_heartbeat_task, "HB", 256, NULL, 1, NULL)`

วิธีวัด: ตอนสร้าง task FreeRTOS ระบายไบต์ `0xA5` ทั่ว stack แล้ว `uxTaskGetStackHighWaterMark()` นับว่ายังเหลือ `0xA5` ที่ไม่เคยถูกเขียนทับกี่ word — ค่านี้คือ **ค่าต่ำสุดตลอดอายุของ task ลดได้อย่างเดียว**

SDK เปิดตัวนับแบบเดียวกัน เช่น `ai_engine_stack_free_words()` ซึ่งตัวอย่าง [07_engine_health.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/07_engine_health.c#L51-L62) บอกว่าเป็น "ALL-TIME MINIMUM. It only ever falls."

**หลักตัดสินของหลักสูตรนี้** (ไม่ใช่ตัวเลขจาก SDK หรือ FreeRTOS): เหลือน้อยกว่า 32 word = **วิกฤต** · เหลือน้อยกว่า 1/4 = **ต่ำ**

---

## แนวคิด (2) ต่อ — ทำไม hook อัตโนมัติไม่พอ

`configCHECK_FOR_STACK_OVERFLOW` ถูกตั้งเป็น 2 ในทั้งสองคอร์ hook จะพิมพ์ `FATAL: Stack overflow in task '...'`

แต่คอมเมนต์ใน linker script เตือนว่ามัน **"only samples at a context switch"** (บรรทัด 307) — stack ที่ล้นไปทับข้อมูลข้าง ๆ ระหว่างสองครั้งที่ตรวจ อาจสร้างความเสียหายก่อน hook จะทันทำงาน

วิธีที่ใช้ได้จริง: วัด high-water mark ตอนระบบทำงานหนักที่สุด แล้วเผื่อที่ว่างไว้ ไม่ใช่พึ่งตัวตรวจอัตโนมัติอย่างเดียว

---

## แนวคิด (3) — ทำไมไม่จองใน ISR หรือลูปเวลาจริง

SDK ตั้ง `configHEAP_ALLOCATION_SCHEME` เป็น heap_3 ซึ่ง `pvPortMalloc()` เรียก `malloc()` ของ newlib ตรง ๆ โดยหยุด scheduler ไว้ระหว่างนั้น

1. **ไม่ปลอดภัยในบริบท ISR** — ISR เรียกได้เฉพาะฟังก์ชันที่ลงท้าย `FromISR` และ `xTaskResumeAll()` ไม่ใช่หนึ่งในนั้น
2. **เวลาไม่แน่นอน** — `malloc()` ต้องค้นหาช่องว่าง เวลาที่ใช้ขึ้นกับสภาพ heap ตอนนั้น
3. **fragmentation** — heap อาจเหลือรวมมากแต่ไม่มีช่องต่อเนื่องใหญ่พอ hook จึงพิมพ์ทั้ง `free` และ `largest_free`
4. **จัดการความล้มเหลวไม่ได้** — ใน ISR ไม่มีที่ให้รอหรือลองใหม่

ทางออก: จองทุกอย่างตอนเริ่มระบบ หรือใช้บัฟเฟอร์ static — littlefs build ด้วย `LFS2_NO_MALLOC` ให้โค้ดที่ต้องใช้ heap **คอมไพล์ไม่ผ่าน** แทนที่จะแอบจองเงียบ ๆ

---

## ตัวอย่างสมบูรณ์ — สามท่าใน 02_where_it_lives.c

```c
int g_initialised = 42;   // static: .data
int g_zeroed;              // static: .bss

int main(void) {
    static uint32_t s_calls;      // static ในฟังก์ชัน: .bss ไม่ใช่ stack
    uint8_t local_buf[64] = {0};  // local: stack frame ของ main
    uint8_t *block = malloc(64);  // ตัวชี้อยู่ stack, ก้อน 64 ไบต์อยู่ heap
    ...
    free(block);   // ทุก malloc ต้องมี free หนึ่งครั้ง
    block = NULL;
}
```

**ท่าที่ 1** พิมพ์ที่อยู่ 8 วัตถุให้ตรวจว่าจับกลุ่มตามป้าย · **ท่าที่ 2** พิมพ์ขนาดแต่ละก้อน · **ท่าที่ 3** เรียกฟังก์ชันซ้อน 3 ชั้น ให้เห็นว่า stack โตลง

---

## ฝึกเติม

เปิด [practice/02_stack_watermark.c](practice/02_stack_watermark.c) จำลองวิธีที่ FreeRTOS วัด stack ด้วยอาร์เรย์หนึ่งก้อน มีช่องให้เติม 3 จุด

1. `stack_paint()` ระบายทุกไบต์ด้วย `0xA5`
2. `high_water_bytes()` นับไบต์ `0xA5` ที่ต่อเนื่องจากปลายที่ stack ยังไปไม่ถึง
3. `percent_used()` คิดเปอร์เซ็นต์แบบเดียวกับ 07_engine_health ต้องไม่หารด้วยศูนย์

```sh
gcc -std=c11 -Wall -Wextra -o watermark practice/02_stack_watermark.c && ./watermark
```

สังเกต test ที่เรียก `simulate_use()` แบบตื้นลงหลังจากเคยลึก — ค่าที่คาดไว้ไม่เปลี่ยน เพราะ high-water mark คือค่าต่ำสุดตลอดอายุ · ลองเองก่อนอย่างน้อย 15 นาที แล้วค่อยเปิด [solution/02_stack_watermark.c](solution/02_stack_watermark.c)

---

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) ครอบคลุมเป้าหมายทั้งสามข้อ (ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน)

1. `static uint8_t buf[512]; uint8_t tmp[16]; uint8_t *p = malloc(32);` — ข้อใดจำแนกถูก
2. จาก linker script ของ CM33 ข้อใดถูก (เลือกได้หลายข้อ)
3. task inference ได้ stack 2048 words, `stack_free_words` เป็น 96 — ข้อสรุปใดดีที่สุด
4. ทำไมการตั้ง `configCHECK_FOR_STACK_OVERFLOW = 2` อย่างเดียวจึงไม่พอ
5. ข้อใดเป็นเหตุผลที่ไม่ควรเรียก `malloc()` ใน ISR หรือลูปที่ต้องตรงเวลา (เลือกได้หลายข้อ)

---

## แล็บ

**งาน:** อ่านตัวนับ stack ของ task จริงสองตัวบนบอร์ด แล้วตัดสินว่าปลอดภัยหรือไม่

1. build แม่แบบของ SDK เปิดตัวอย่าง (`make build -j ENABLE_PAGE_EXAMPLES=1` แล้ว `make program`) ถอดสาย USB ให้สุดและเสียบใหม่
2. บนจอแตะ **SDK Examples** เลือก `cm55/display/00_display_bringup` กด **Run this example** จดค่า `stack %lu words` และ `stack never used: %lu words`
3. เลือก `cm55/edge_ai/07_engine_health` แล้วรัน จดบรรทัด `inference task stack: ... words granted, ... still free at its worst (...% used)`
4. คำนวณเปอร์เซ็นต์ที่ใช้ของ GFX task เอง แล้วตัดสินทั้งสอง task ด้วยหลักของแบบฝึก (วิกฤต ต่ำ หรือปลอดภัย)
5. เปิด [10_littlefs_basics.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/storage/10_littlefs_basics.c) จำแนกตัวแปร 5 ตัว เช่น `s_buf`, `k_known_paths` ว่าอยู่ stack, heap หรือ static

**หลักฐานที่เก็บไว้ใน portfolio:** ภาพหน้าจอทั้งสองตัวอย่าง ตารางค่าที่จด การคำนวณ คำตัดสิน และตารางจำแนกตัวแปร 5 ตัว

---

## ไปต่อ

- อ่าน linker script ของ CM33 ช่วง `.cy_csr_buffers` ([บรรทัด 261-324](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/COMPONENT_CM33/TOOLCHAIN_GCC_ARM/pse84_ns_cm33.ld#L261-L324)) — ทีมย้ายบัฟเฟอร์ static 8 KB ออกจาก `.bss` แล้วใส่ `ASSERT` ให้ build ล้มถ้าหลุดกลับมา ลองอธิบายว่าทำไม "ให้ build ล้ม" ดีกว่าการเขียนเตือนไว้ในเอกสาร
- เอกสาร [FreeRTOS memory management](https://www.freertos.org/Documentation/00-Overview) เทียบ heap_1 ถึง heap_5

บทถัดไป: [บทเรียน 1.3 — struct, pointer และบัฟเฟอร์วงแหวน](../l03-structs-pointers-buffers/README.md)

---

## แหล่งที่มาและเครดิต

"พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

โค้ดของหลักสูตรนี้ (`examples/`, `practice/`, `solution/`) Apache-2.0 · โค้ดของ SDK ไม่ได้คัดลอกเป็นไฟล์
บทเรียนยกมาเป็นช่วงสั้น ๆ พร้อมลิงก์ไปยังไฟล์ที่ commit `ef72c1b` (Apache-2.0, tesaiot-pse84-devkit-sdk)
