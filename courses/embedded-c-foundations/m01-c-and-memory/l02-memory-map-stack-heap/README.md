---
id: c-found.m01.l02
lang: th
title: {th: แผนที่หน่วยความจำ stack และ heap, en: 'Memory map, stack and heap'}
summary: {th: รู้ว่าข้อมูลแต่ละก้อนอยู่ที่ใด และป้องกัน stack ล้นกับการจองหน่วยความจำในที่ที่ไม่ควร, en: Know where each piece of data lives and prevent stack overflow and allocation in the wrong place.}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m01.l01]
objectives:
- {th: 'จำแนกตัวแปรในโปรแกรมตัวอย่างได้ว่าอยู่ใน stack, heap หรือหน่วยความจำแบบ static', en: 'Classify the variables of an example program as stack, heap or static.'}
- {th: อ่านค่าพื้นที่ stack ที่เหลือของ task จากตัวนับที่ SDK ให้มา และตัดสินได้ว่าใกล้ล้นหรือไม่, en: Read a task's remaining stack from the counters the SDK exposes and judge whether it is near overflow.}
- {th: อธิบายว่าทำไมไม่ควรจองหน่วยความจำแบบ dynamic ใน ISR หรือในลูปเวลาจริง, en: Explain why dynamic allocation does not belong in an ISR or a real-time loop.}
develops:
- {skill: prog.memory, to: 3}
- {skill: lang.c, to: 3}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: pending
---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. จำแนกตัวแปรในโปรแกรมตัวอย่างได้ว่าอยู่ใน stack, heap หรือหน่วยความจำแบบ static
2. อ่านค่าพื้นที่ stack ที่เหลือของ task จากตัวนับที่ SDK ให้มา และตัดสินได้ว่าใกล้ล้นหรือไม่
3. อธิบายว่าทำไมไม่ควรจองหน่วยความจำแบบ dynamic ใน ISR หรือในลูปเวลาจริง

ใช้เวลาประมาณ 70 นาที (แนวคิด 15 · ฝึก 25 · แล็บ 25 · เช็ก 5)

## ก่อนเริ่ม

ทวนจากบทเรียน 1.1 สองข้อ

1. `uint8_t` บวกเกิน 255 แล้วเกิดอะไรขึ้น และทำไมตัวอย่างของ SDK จึงขยายเป็น 64 บิตก่อนคูณ
2. ตัวแปรแบบไหนที่ต้องเป็น `volatile` และ `volatile` ช่วยเรื่อง `count++` ที่ถูก interrupt แทรกได้หรือไม่

## ดูของจริงก่อน

เปิด [examples/02_where_it_lives.c](examples/02_where_it_lives.c) **ทายก่อนรัน** ว่าที่อยู่ของ `local_buf` (ตัวแปร local ใน `main`)
กับ `g_zeroed` (ตัวแปร global) ตัวไหนมีค่ามากกว่า แล้วรัน

```sh
gcc -std=c11 -Wall -Wextra -o where_it_lives examples/02_where_it_lives.c
./where_it_lives
```

ตัวเลขบนเครื่องของคุณจะไม่ตรงกับของเพื่อน แต่จะเห็นที่อยู่แบ่งเป็นกลุ่มชัดเจน ค่าคงที่กับตัวแปร global อยู่ใกล้กัน
ก้อนที่ `malloc` ได้มาอยู่อีกย่านหนึ่ง ตัวแปร local อยู่ไกลออกไปอีกย่าน และบรรทัด `depth 1, 2, 3` แสดงว่า
ยิ่งเรียกฟังก์ชันลึก ที่อยู่ของ stack frame ยิ่ง **ลดลง** บนไมโครคอนโทรลเลอร์กลุ่มเหล่านี้มีอยู่เหมือนกัน
ต่างกันตรงที่ไม่มีระบบปฏิบัติการสุ่มให้ **linker script เป็นคนวางทุกกลุ่ม** และเราอ่านมันได้

## แนวคิด

### 1. แผนที่หน่วยความจำ: ใครวางอะไรไว้ตรงไหน

| ส่วน (section) | เก็บอะไร | อยู่ที่ไหนบน PSOC™ Edge E84 ในแม่แบบของ SDK |
|---|---|---|
| `.text` `.rodata` | โค้ด ค่าคงที่ `const` ข้อความ | flash ภายนอกแบบ QSPI ซึ่ง CPU รันโค้ดจากตรงนั้นได้เลย (XIP) |
| `.data` | ตัวแปร static ที่มีค่าเริ่มต้น เช่น `int g = 42;` | ค่าเริ่มต้นเก็บใน flash แล้วคัดลอกมาไว้ RAM ตอนบูต |
| `.bss` | ตัวแปร static ที่ไม่ได้ให้ค่า หรือให้ค่า 0 | RAM ถูกล้างเป็นศูนย์ตอนบูต ไม่กินที่ใน flash |
| heap | ก้อนที่ได้จาก `malloc()` | RAM ส่วนที่เหลือหลัง `.bss` |
| stack | ตัวแปร local ที่อยู่ของการกลับจากฟังก์ชัน | บนสุดของ RAM ก้อนนั้น โตลงหาที่อยู่ต่ำ |

ทั้งหมดนี้อ่านได้จาก linker script ของ CM33 non-secure ใน SDK
([pse84_ns_cm33.ld](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/COMPONENT_CM33/TOOLCHAIN_GCC_ARM/pse84_ns_cm33.ld#L346-L361))
เช่น `.data` ถูกวางว่า `> m33_data AT > m33_nvm_sel` แปลว่ารันใน RAM แต่เก็บต้นฉบับไว้ใน flash และตาราง copy
ที่บรรทัด 190 เขียนกำกับไว้ว่า "From load address in ext flash" ส่วน heap เป็นส่วนที่ขยายจนเต็ม คือจากท้าย `.bss` ถึงก่อน stack
และ stack เริ่มที่ `__StackTop = ORIGIN(m33_data) + LENGTH(m33_data)` ขนาดเริ่มต้น `0x1000` ไบต์ (บรรทัด 47)

ผลที่ตามมาซึ่งคอมเมนต์ใน linker script เดียวกันบันทึกไว้จากบอร์ดจริงคือ **ทุกไบต์ที่ `.bss` โตขึ้น คือไบต์ที่ heap หายไป**
("every byte of .bss costs a byte of heap one for one", บรรทัด 265) เมื่อเพิ่มหน้าจอใหม่เข้าไป heap เหลือน้อยจน mTLS ล้มด้วย
`WARN: Malloc failed arena=121812 used=121308 free=504 largest_free=0` และคอมเมนต์สรุปว่า "Eleven rounds of code review could not see that;
the board said it in ten minutes." ตัวแปร static ไม่ฟรี มันกินที่จากคนอื่นเสมอ

### 2. stack ต่อ task และ high-water mark

ในระบบที่ใช้ FreeRTOS **แต่ละ task มี stack ของตัวเอง** ขนาดกำหนดตอนสร้าง task เป็นจำนวน word (4 ไบต์บน CPU 32 บิต)
เช่น task heartbeat ของแม่แบบ mtb-only สร้างด้วย `xTaskCreate(bento_heartbeat_task, "HB", 256, NULL, 1, NULL)`
([proj_cm33_ns/main.c บรรทัด 309](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/main.c#L309))
ส่วน stack ขนาด `0x1000` ใน linker script เป็นของ `main()` ก่อน scheduler เริ่ม และของ interrupt handler หลังจากนั้น

จะรู้ว่า task ใช้ stack ไปลึกแค่ไหน FreeRTOS ใช้วิธีระบายสี: ตอนสร้าง task มันเขียนไบต์ `0xA5` ทั่ว stack
(`tskSTACK_FILL_BYTE` ใน tasks.c) แล้ว `uxTaskGetStackHighWaterMark()` นับว่ายังเหลือ `0xA5` ที่ไม่เคยถูกเขียนทับกี่ word
ค่านี้คือ **ค่าต่ำสุดตลอดอายุของ task** ลดได้อย่างเดียว ยิ่งน้อยยิ่งใกล้ล้น SDK เปิดตัวนับแบบเดียวกันให้อ่านได้หลายจุด เช่น
`ai_engine_stack_words()` กับ `ai_engine_stack_free_words()` ของ task inference ซึ่งตัวอย่าง
[07_engine_health.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/07_engine_health.c#L51-L62)
อธิบายว่าค่าหลังเป็น "ALL-TIME MINIMUM. It only ever falls." และการอ่านต้องสแกน stack จึงควรอ่านราว 1 ครั้งต่อวินาที ไม่ใช่ในลูปวาดจอ

อย่าพึ่งแค่ตัวตรวจอัตโนมัติ `configCHECK_FOR_STACK_OVERFLOW` ถูกตั้งเป็น 2 ในทั้งสองคอร์ และ hook ของ CM33 จะพิมพ์
`FATAL: Stack overflow in task '...'` แต่คอมเมนต์ใน linker script เตือนว่ามัน "only samples at a context switch"
(บรรทัด 307) stack ที่ล้นไปทับข้อมูลข้าง ๆ ระหว่างสองครั้งที่ตรวจ จึงอาจสร้างความเสียหายก่อน hook จะทันทำงาน
วิธีที่ใช้ได้จริงคือวัด high-water mark ตอนระบบทำงานหนักที่สุด แล้วเผื่อที่ว่างไว้

หลักตัดสินที่หลักสูตรนี้ใช้ในแบบฝึก (เป็นหลักของเรา ไม่ใช่ตัวเลขจาก SDK หรือ FreeRTOS): เหลือน้อยกว่า 32 word ถือว่า **วิกฤต**
เหลือน้อยกว่าหนึ่งในสี่ของทั้งหมดถือว่า **ต่ำ** ควรขยาย stack หรือย้ายบัฟเฟอร์ใหญ่ออกจาก stack

### 3. heap: ทำไมไม่จองใน ISR หรือในลูปเวลาจริง

แม่แบบของ SDK ตั้ง `configHEAP_ALLOCATION_SCHEME` เป็น heap_3
([FreeRTOSConfig.h ของ CM33 บรรทัด 189](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/FreeRTOSConfig.h#L189))
ซึ่ง `pvPortMalloc()` ของ FreeRTOS เรียก `malloc()` ของ newlib ตรง ๆ โดยหยุด scheduler ไว้ระหว่างนั้น (`vTaskSuspendAll()` แล้ว `xTaskResumeAll()`)
การจองหน่วยความจำแบบ dynamic ไม่เหมาะกับ ISR และลูปเวลาจริงด้วยเหตุผลสี่ข้อ

1. **ไม่ปลอดภัยในบริบท ISR** FreeRTOS อนุญาตให้ ISR เรียกเฉพาะฟังก์ชันที่ลงท้ายด้วย `FromISR` และ `xTaskResumeAll()` ไม่ใช่หนึ่งในนั้น
2. **เวลาไม่แน่นอน** `malloc()` ต้องค้นหาช่องว่าง เวลาที่ใช้ขึ้นกับสภาพ heap ในตอนนั้น ลูปที่ต้องตรงเวลาจึงเดาเวลาของตัวเองไม่ได้
3. **fragmentation** จองและคืนก้อนขนาดต่างกันไปนาน ๆ heap อาจเหลือรวมหลายร้อยไบต์แต่ไม่มีช่องต่อเนื่องใหญ่พอ
   hook `vApplicationMallocFailedHook()` ของ CM33 จึงพิมพ์ทั้ง `free` และ `largest_free` เพราะ "Malloc failed" เฉย ๆ
   ไม่บอกว่า heap หมดหรือแค่แตกเป็นชิ้น ([main.c บรรทัด 411-425](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/main.c#L411-L425))
4. **จัดการความล้มเหลวไม่ได้** ใน ISR ไม่มีที่ให้รอ ไม่มีที่ให้ลองใหม่ และไม่ควรพิมพ์อะไรเลย

ทางออกคือจองทุกอย่างตอนเริ่มระบบหรือใช้บัฟเฟอร์ static SDK ทำแบบนี้ให้ดูในหลายที่ เช่น littlefs ใน variant mtb-only
ถูก build ด้วย `LFS2_NO_MALLOC` "because every buffer is supplied statically; a code path that would need the heap fails to compile
instead of quietly allocating" ([variants/mtb-only.mk บรรทัด 35-39](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/variants/mtb-only.mk#L35-L39))
และตัวอย่าง `10_littlefs_basics.c` ประกาศบัฟเฟอร์ 512 ไบต์เป็น `static char s_buf[512];` พร้อมเหตุผลว่า
"the runner task's stack is not the place for it"

## ตัวอย่างสมบูรณ์

[examples/02_where_it_lives.c](examples/02_where_it_lives.c) ทำงานเป็นสามท่า

- **ท่าที่ 1** พิมพ์ที่อยู่ของวัตถุแปดอย่าง พร้อมป้ายว่าอยู่ส่วนไหน ให้คุณตรวจด้วยตาว่าที่อยู่จับกลุ่มตามป้ายจริง
- **ท่าที่ 2** พิมพ์ขนาดของแต่ละก้อน ว่ากินที่จาก stack, heap หรือข้อมูลอ่านอย่างเดียว
- **ท่าที่ 3** เรียกฟังก์ชันซ้อนสามชั้น แต่ละชั้นพิมพ์ที่อยู่ของตัวแปร local ของตัวเอง ให้เห็นว่า stack โตลง

ลองแก้แล้วทายก่อนรัน

1. ย้าย `uint8_t local_buf[64]` ออกไปไว้นอก `main` ป้ายที่ถูกต้องของมันเปลี่ยนเป็นอะไร
2. ใส่ `static` หน้า `uint8_t local_buf[64]` (ยังอยู่ใน `main`) ที่อยู่ของมันย้ายไปกลุ่มไหน
3. เปลี่ยนเงื่อนไข `level < 3` เป็น `level < 100000` แล้วรัน โปรแกรมเป็นอย่างไร และบนไมโครคอนโทรลเลอร์ที่ไม่มีระบบปฏิบัติการคอยจับ จะเกิดอะไรแทน

## ฝึกเติม

เปิด [practice/02_stack_watermark.c](practice/02_stack_watermark.c) ไฟล์นี้จำลองวิธีที่ FreeRTOS วัด stack ด้วยอาร์เรย์หนึ่งก้อน
มีช่องให้เติม 3 จุด

1. `stack_paint()` ระบายทุกไบต์ด้วย `0xA5`
2. `high_water_bytes()` นับไบต์ `0xA5` ที่ต่อเนื่องจากปลายที่ stack ยังไปไม่ถึง
3. `percent_used()` คิดเปอร์เซ็นต์แบบเดียวกับตัวอย่าง 07_engine_health และต้องไม่หารด้วยศูนย์

```sh
gcc -std=c11 -Wall -Wextra -o watermark practice/02_stack_watermark.c && ./watermark
```

สังเกต test ที่เรียก `simulate_use()` แบบตื้นลงหลังจากเคยลึก ค่าที่คาดไว้ไม่เปลี่ยน เพราะ high-water mark คือค่าต่ำสุดตลอดอายุ

## เฉลย

ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/02_stack_watermark.c](solution/02_stack_watermark.c)
จุดที่ควรเทียบคือ `percent_used()` ในเฉลยตรวจทั้ง `total == 0` และ `free > total` ก่อนลบ
เพราะการลบ unsigned ที่ติดลบจะวนกลับเป็นเลขมหาศาล (ความรู้จากบทเรียน 1.1)

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) (บนเว็บไซต์อยู่ท้ายหน้านี้) ครอบคลุมเป้าหมายทั้งสามข้อ ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน

## แล็บ

**งาน:** อ่านตัวนับ stack ของ task จริงสองตัวบนบอร์ด แล้วตัดสินว่าปลอดภัยหรือไม่

1. build แม่แบบของ SDK โดยเปิดตัวอย่าง (ขั้นตอนเต็มอยู่ใน [บทเรียน 2.1](../../m02-build-and-version/l01-toolchain-first-build/README.md))
   ```sh
   make build -j ENABLE_PAGE_EXAMPLES=1
   make program
   ```
   แล้วถอดสาย USB ให้สุดและเสียบใหม่
2. บนจอ แตะการ์ด **SDK Examples** เลือก `cm55/display/00_display_bringup` แล้วกด **Run this example**
   จดสองค่า คือ `stack %lu words` ของ GFX task และ `stack never used: %lu words (all-time low)`
3. เลือก `cm55/edge_ai/07_engine_health` แล้วรัน จดบรรทัด `inference task stack: ... words granted, ... still free at its worst (...% used)`
   ตัวอย่างนี้อ่านสองค่านี้ก่อนตรวจว่ามีโมเดลทำงานอยู่ไหม จึงได้ค่า stack แม้จะไม่มีโมเดลทำงาน
   (ถ้าได้ข้อความว่า task ไม่เคยถูกสร้าง ให้จดไว้ นั่นคือผลการวัดเหมือนกัน)
4. คำนวณเปอร์เซ็นต์ที่ใช้ของ GFX task เอง แล้วตัดสินทั้งสอง task ด้วยหลักของแบบฝึก (วิกฤต ต่ำ หรือปลอดภัย)
5. เปิด [10_littlefs_basics.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/storage/10_littlefs_basics.c)
   เลือกตัวแปรห้าตัว เช่น `s_buf`, `k_known_paths`, `s_allow_write`, `present`, `n` แล้วจำแนกว่าแต่ละตัวอยู่ใน stack, heap หรือ static พร้อมเหตุผลหนึ่งประโยค

**หลักฐานที่เก็บไว้ใน portfolio:** ภาพถ่ายหน้าจอผลของทั้งสองตัวอย่าง ตารางค่าที่จด การคำนวณ คำตัดสิน และตารางจำแนกตัวแปรห้าตัว

## ไปต่อ

- อ่าน linker script ของ CM33 ช่วง `.cy_csr_buffers` ([บรรทัด 261-324](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/COMPONENT_CM33/TOOLCHAIN_GCC_ARM/pse84_ns_cm33.ld#L261-L324))
  ทีมย้ายบัฟเฟอร์ static ขนาด 8 KB และ stack ของ task หนึ่งออกจาก `.bss` ไปไว้ใน RAM อีกก้อน เพื่อคืนที่ให้ heap
  แล้วใส่ `ASSERT` ให้ build ล้มถ้าวันหนึ่งบัฟเฟอร์เหล่านั้นหลุดกลับมา ลองอธิบายว่าทำไมการ "ให้ build ล้ม" ดีกว่าการเขียนเตือนไว้ในเอกสาร
- เอกสาร [FreeRTOS](https://www.freertos.org/Documentation/00-Overview) หัวข้อ memory management: เทียบ heap_1 ถึง heap_5 และสังเกตว่า
  เมื่อใช้ heap_3 ค่า `configTOTAL_HEAP_SIZE` ในไฟล์ config ไม่ได้กำหนดขนาด heap จริง

บทถัดไป: [บทเรียน 1.3 struct, pointer และบัฟเฟอร์วงแหวน](../l03-structs-pointers-buffers/README.md)

## สะท้อนคิด

- ในโปรแกรมที่คุณเคยเขียน มีบัฟเฟอร์ใหญ่ตัวไหนที่เป็นตัวแปร local และถ้าย้ายโปรแกรมนั้นมาไว้ใน task ที่มี stack 256 word จะเกิดอะไร
- ถ้าโปรแกรมทำงานได้ปกติมาหนึ่งชั่วโมง แล้วเริ่ม `Malloc failed` ทั้งที่ไม่มีการรั่ว คุณจะเก็บหลักฐานอะไรเพื่อแยกว่า heap หมดหรือแตกเป็นชิ้น

## แหล่งอ้างอิง

- [SDK: cm55/edge_ai/07_engine_health.c (ai_engine_stack_words และ ai_engine_stack_free_words)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/07_engine_health.c)
- [SDK: cm33/storage/10_littlefs_basics.c (บัฟเฟอร์และสัญญาของ API หน่วยเก็บ)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/storage/10_littlefs_basics.c)
- [SDK: cm55/display/00_display_bringup.c (high-water mark ของ GFX task)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/display/00_display_bringup.c)
- [SDK: linker script ของ CM33 non-secure (pse84_ns_cm33.ld)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/COMPONENT_CM33/TOOLCHAIN_GCC_ARM/pse84_ns_cm33.ld)
- [Appendix X — Traps and anti-patterns (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__tut__x__traps__antipatterns.html)
- [FreeRTOS documentation](https://www.freertos.org/Documentation/00-Overview)
- [Infineon FreeRTOS @ release-v10.6.202 (รุ่นที่แม่แบบของ SDK ดึงมา): task.h](https://github.com/Infineon/freertos/blob/release-v10.6.202/Source/include/task.h)
