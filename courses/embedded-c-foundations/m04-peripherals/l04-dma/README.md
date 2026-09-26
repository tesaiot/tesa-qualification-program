---
id: c-found.m04.l04
lang: th
title: {th: DMA, en: DMA}
summary: {th: ย้ายข้อมูลโดยไม่ใช้ CPU และรู้ข้อควรระวังเรื่องบัฟเฟอร์ที่ DMA กับ CPU ใช้ร่วมกัน, en: Move data without the CPU and know the pitfalls of buffers shared by DMA and the CPU.}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m04.l03]
objectives:
- {th: อธิบายว่า DMA ช่วยลดภาระ CPU ในการย้ายข้อมูลอย่างไร และเมื่อใดไม่คุ้ม, en: Explain how DMA offloads data movement from the CPU and when it is not worth it.}
- {th: ระบุความเสี่ยงของบัฟเฟอร์ที่ DMA กับ CPU ใช้ร่วมกัน เช่น cache และการอ่านก่อนการย้ายเสร็จ, en: 'Identify the risks of buffers shared by DMA and the CPU, such as caches and reading before the transfer completes.'}
develops:
- {skill: mcu.dma, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: pending
---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. อธิบายว่า DMA ช่วยลดภาระ CPU ในการย้ายข้อมูลอย่างไร และเมื่อใดไม่คุ้ม
2. ระบุความเสี่ยงของบัฟเฟอร์ที่ DMA กับ CPU ใช้ร่วมกัน เช่น cache และการอ่านก่อนการย้ายเสร็จ

ใช้เวลาประมาณ 70 นาที (แนวคิด 15 · ฝึก 25 · แล็บ 25 · เช็ก 5) แล็บของบทนี้เป็นการอ่านโค้ดและค่าตั้งจริงของ SDK
เพราะตัวอย่างในแคตตาล็อกของ SDK ที่ commit นี้ยังไม่มีตัวอย่าง DMA โดยตรง

## ก่อนเริ่ม

ทวนจากบทก่อนหน้าสองข้อ

1. บัฟเฟอร์วงแหวนในบทเรียน 1.3 ต้องเขียนข้อมูลก่อนแล้วจึงเลื่อน `head` ทำไมลำดับนี้สำคัญเมื่อผู้เขียนเป็นอีกบริบทหนึ่ง
2. ISR ที่ดีในบทเรียน 4.1 ทำงานอะไรบ้าง และส่งอะไรต่อให้ task

## ดูของจริงก่อน

เปิด [examples/10_dma_cache_sim.c](examples/10_dma_cache_sim.c) แบบจำลองนี้มีหน่วยความจำจริงที่ "DMA" เขียน และ cache ที่ CPU อ่านผ่าน
เหมือน Cortex-M55 ที่มี data cache **ทายก่อนรัน** ว่าบรรทัด `frame 2, stale cache:` จะพิมพ์ค่าอะไร

```sh
gcc -std=c11 -Wall -Wextra -o dma_cache_sim examples/10_dma_cache_sim.c
./dma_cache_sim
```

DMA เขียน `BB` ครบแล้ว แต่ CPU ยังเห็น `AA` เพราะอ่านจากสำเนาใน cache จนกว่าจะ invalidate และบรรทัด `frame 3, read too early:`
แสดงบั๊กอีกแบบ CPU อ่านตอน DMA เขียนไปครึ่งเดียว ได้ `CC` ครึ่งหนึ่งกับ `BB` อีกครึ่ง บั๊กทั้งสองแบบไม่ทำให้โปรแกรมล้ม มันแค่ให้ข้อมูลผิดอย่างเงียบ ๆ

## แนวคิด

### 1. DMA ทำงานแทน CPU ได้อย่างไร และเมื่อไรไม่คุ้ม

**DMA (Direct Memory Access)** คือฮาร์ดแวร์ที่ย้ายข้อมูลระหว่างรีจิสเตอร์ของอุปกรณ์กับหน่วยความจำ หรือระหว่างหน่วยความจำด้วยกัน โดยไม่ต้องให้ CPU
คัดลอกทีละไบต์ CPU ตั้ง **descriptor** ครั้งเดียว (ต้นทาง ปลายทาง ขนาดของแต่ละชิ้น จำนวนชิ้น และสัญญาณที่สั่งให้ย้าย) แล้วไปทำอย่างอื่น
DMA ย้ายเองทุกครั้งที่อุปกรณ์ส่งสัญญาณ trigger และแจ้งด้วย interrupt เมื่อครบ เอกสารของ PDL สรุปไว้ว่า
"The DMA channel can be used in any project to transfer data without CPU intervention basing on a hardware trigger signal from another component."
([cy_dma.h @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_dma.h))

PDL สำหรับชิปนี้มีไดรเวอร์ DMA สองชนิด คือ DataWire (`Cy_DMA_*` ใน `cy_dma.h`) และ AXI DMAC (`Cy_AXIDMAC_*` ใน `cy_axidmac.h`)
ลำดับการตั้งตามเอกสาร: `Cy_DMA_Descriptor_Init()` แล้ว `Cy_DMA_Channel_Init()` แล้ว `Cy_DMA_Enable()` กับ `Cy_DMA_Channel_Enable()`
และเอกสารเตือนว่า "Even if a DMA channel is enabled, it is not operational until the DMA block is enabled"

ตัวอย่างการตัดสินใจเรื่อง DMA ที่มีใน SDK เอง

| งาน | ทางที่ SDK ใช้ | เหตุผล |
|---|---|---|
| รับภาพจากกล้องทีละบรรทัด | DMA ย้ายค่าจากพอร์ต GPIO ลงบัฟเฟอร์บรรทัด แล้ว AXI DMAC ย้ายบรรทัดไปรวมเป็นภาพ (ไดรเวอร์กล้อง) | ข้อมูลมาเร็วกว่าที่ CPU จะรับทีละไบต์ด้วย interrupt ได้ |
| อ่านเขียน FIFO ของเรดาร์ผ่าน SPI | `Cy_SCB_SPI_Transfer()` แบบ interrupt | ปริมาณพอที่ ISR ของ SPI จัดการได้ |
| ทดสอบ SPI 8 ไบต์บน header | bit-bang ด้วย `Cy_GPIO_Write()` (ตัวอย่าง Header I/O Test บน Developer Hub) | งานสั้นมาก ครั้งคราว การตั้ง DMA ไม่คุ้ม |

DMA **ไม่คุ้ม** เมื่อข้อมูลน้อยจนเวลาตั้ง descriptor มากกว่าเวลาคัดลอกเอง เมื่อข้อมูลต้องถูกประมวลผลทีละไบต์ระหว่างทางอยู่แล้ว
เมื่อช่อง DMA มีน้อยและอุปกรณ์อื่นต้องการมากกว่า และเมื่อค่าใช้จ่ายของการดูแล cache (หัวข้อถัดไป) กับความซับซ้อนของโค้ดมากกว่าเวลา CPU ที่ประหยัดได้

### 2. ความเสี่ยงที่หนึ่ง: อ่านก่อน DMA เขียนเสร็จ

DMA กับ CPU ทำงานพร้อมกันจริง บัฟเฟอร์ที่ DMA กำลังเขียนอยู่ห้ามให้ CPU อ่าน วิธีมาตรฐานคือ **ping-pong** มีสองก้อน DMA เขียนก้อนหนึ่ง
ขณะ CPU ประมวลผลอีกก้อน และสลับกันเมื่อ DMA แจ้งว่าเสร็จ ไดรเวอร์กล้องใน SDK ทำแบบนี้ ISR ของสัญญาณ HREF ตั้งปลายทางของ DMA เป็น
`line_buffer[row_buffer_flag]` แล้วสลับ `row_buffer_flag` ส่วน ISR ของ VSYNC สลับ frame buffer แล้วตั้ง `*_frame_ready = true` ให้ฝั่งที่ใช้ภาพรู้ว่าพร้อม
([mtb_dvp_camera_ov7675.c บรรทัด 627-670](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/camera-dvp-ov7675/mtb_dvp_camera_ov7675.c#L627-L670))
ถ้า CPU ช้ากว่า DMA ต้องมีนโยบายชัดว่าจะทิ้งข้อมูลก้อนไหน และ **นับ** ทุกครั้งที่ทิ้ง (overrun) แบบที่แบบฝึกของบทนี้ทำ

### 3. ความเสี่ยงที่สอง: cache

Cortex-M55 มี data cache CPU อ่านเขียนผ่านสำเนาใน cache ส่วน DMA อ่านเขียนหน่วยความจำจริงโดยไม่ผ่าน cache ความจริงสองชุดนี้ต้องทำให้ตรงกันเอง

- **CPU เขียน แล้ว DMA อ่าน** (เช่น descriptor หรือข้อมูลที่จะส่งออก) ต้อง **clean** คือเขียนสำเนาใน cache ลงหน่วยความจำก่อนสั่ง DMA
- **DMA เขียน แล้ว CPU อ่าน** ต้อง **invalidate** คือทิ้งสำเนาเก่าใน cache ก่อนอ่าน ไม่อย่างนั้นได้ค่าเก่าแบบในตัวอย่าง
- หรือ **วางบัฟเฟอร์ไว้ในหน่วยความจำที่ไม่ผ่าน cache** แล้วไม่ต้องทำทั้งสองอย่าง

ไดรเวอร์กล้องใน SDK ใช้ครบทั้งสามแบบ และเขียนเหตุผลไว้ทุกจุด

```c
Cy_DMA_Descriptor_SetDstAddress(&CYBSP_DMA_DVP_CAM_CONTROLLER_Descriptor_0,
                                (uint8_t*)line_buffer[row_buffer_flag]);
#if defined (__DCACHE_PRESENT) && (__DCACHE_PRESENT != 0)
/* line_buffer is in .cy_sharedmem (non-cacheable) — no invalidate needed.
 * DMA descriptor is in cached .cy_socmem_data — clean IS needed. */
SCB_CleanDCache_by_Addr((uint32_t*)&CYBSP_DMA_DVP_CAM_CONTROLLER_Descriptor_0,
                        sizeof(CYBSP_DMA_DVP_CAM_CONTROLLER_Descriptor_0));
#endif
Cy_DMA_Channel_Enable(CYBSP_DMA_DVP_CAM_CONTROLLER_HW,
                      CYBSP_DMA_DVP_CAM_CONTROLLER_CHANNEL);

row_buffer_flag = !row_buffer_flag;
```

ที่มา: [mtb_dvp_camera_ov7675.c บรรทัด 637-648](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/camera-dvp-ov7675/mtb_dvp_camera_ov7675.c#L637-L648)
(Apache-2.0, Copyright 2025 Infineon Technologies AG ดัดแปลงโดยทีม TESA ใน tesaiot-pse84-devkit-sdk)

ห้าจุดที่ควรสังเกต: บัฟเฟอร์บรรทัดถูกวางด้วย `__attribute__((section(".cy_sharedmem")))` ซึ่งคอมเมนต์บอกว่าไม่ผ่าน cache จึงไม่ต้อง invalidate,
descriptor อยู่ในหน่วยความจำที่ผ่าน cache จึงต้อง `SCB_CleanDCache_by_Addr()` (ฟังก์ชันของ CMSIS-Core ที่ PDL ใช้) ทุกครั้งที่ CPU แก้มัน ก่อนเปิด channel,
การ clean ถูกครอบด้วย `#if defined (__DCACHE_PRESENT)` โค้ดเดียวกันจึงถูกทั้งคอร์ที่มีและไม่มี data cache,
เอกสาร `cy_dma.h` ของ PDL เขียนหลักเดียวกันไว้สำหรับชิปที่มีคอร์ CM7 ("D cache needs to be cleaned before DMA transfer and should be invalidated after DMA transfer")
และ cache ทำงานเป็น line (เอกสาร PDL ระบุ 32 ไบต์สำหรับ CM7) บัฟเฟอร์ของ DMA จึงควรตรงขอบและยาวเต็ม line เพื่อไม่ให้การ clean หรือ invalidate ไปโดนตัวแปรข้าง ๆ

## ตัวอย่างสมบูรณ์

[examples/10_dma_cache_sim.c](examples/10_dma_cache_sim.c) ทำงานเป็นสามท่า

- **ท่าที่ 1** DMA เติมบัฟเฟอร์ครบ CPU อ่านครั้งแรก cache ว่างอยู่จึงได้ของจริง
- **ท่าที่ 2** DMA เติมรอบสอง CPU อ่านโดยไม่ invalidate ได้สำเนาเก่า แล้ว invalidate แล้วอ่านใหม่ได้ของจริง
- **ท่าที่ 3** invalidate ถูกแล้ว แต่อ่านเร็วเกินไป ได้ข้อมูลครึ่งเก่าครึ่งใหม่ จนกว่าจะรอให้ DMA เสร็จ

ลองแก้แล้วทายก่อนรัน

1. ลบ `cache_invalidate(&b);` บรรทัดแรกในท่าที่ 3 ออก บรรทัด `read too early` จะเห็นอะไร และบั๊กสองแบบซ้อนกันทำให้วินิจฉัยยากขึ้นอย่างไร
2. ทำให้ `cpu_read()` ไม่ผ่าน cache เลย (เหมือนวางบัฟเฟอร์ไว้ในหน่วยความจำที่ไม่ผ่าน cache) บั๊กแบบไหนหายไป แบบไหนยังอยู่
3. เพิ่มฟังก์ชัน `cpu_write()` กับ `cache_clean()` แล้วจำลองกรณี CPU เตรียมข้อมูลให้ DMA ส่งออกโดยลืม clean

## ฝึกเติม

เปิด [practice/10_ping_pong.c](practice/10_ping_pong.c) มีช่องให้เติม 6 จุด มากที่สุดในโมดูลนี้ เพราะนี่คือบทปิดท้ายของโมดูล
ตัวจัดการ ping-pong ต้องไม่ให้ DMA ทับก้อนของ CPU นับ overrun เมื่อ CPU ช้า และ invalidate ก่อนคืนก้อนให้ CPU อ่าน

```sh
gcc -std=c11 -Wall -Wextra -o ping_pong practice/10_ping_pong.c && ./ping_pong
```

test ตั้งใจให้ CPU อ่านก้อนแรกไว้หนึ่งครั้งก่อนเริ่ม cache จึงมีสำเนาเก่าค้างอยู่ ถ้าคุณลืม invalidate test ข้อที่อ่านค่า `0x11` จะล้ม

## เฉลย

ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/10_ping_pong.c](solution/10_ping_pong.c)
เราทดลองลบบรรทัด invalidate ออกจากเฉลย แล้วรัน test ได้ `FAIL ... expected 17 got 0` คือ test จับบั๊ก cache ได้จริง
คอมเมนต์ในเฉลยบอกทางเลือกบนบอร์ดจริงสองทาง invalidate ด้วยฟังก์ชันของ CMSIS-Core ตามขนาดบัฟเฟอร์ หรือวางบัฟเฟอร์ในหน่วยความจำที่ไม่ผ่าน cache แบบไดรเวอร์กล้อง

## เช็กความเข้าใจ

ตอบคำถาม 4 ข้อใน [quiz.yaml](quiz.yaml) (บนเว็บไซต์อยู่ท้ายหน้านี้) ครอบคลุมเป้าหมายทั้งสองข้อ ตอบถูกตั้งแต่ 3 ข้อขึ้นไปถือว่าจบบทเรียน

## แล็บ

**งาน:** อ่านค่าตั้ง DMA จริงใน BSP ของ SDK และไดรเวอร์กล้อง แล้วตอบด้วยหลักฐานว่าข้อมูลไหลอย่างไร

1. เปิด [cycfg_dmas.c ของ BSP](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_dmas.c)
   (หรือเปิด `design.modus` ของแม่แบบด้วย Device Configurator ของ ModusToolbox) แล้วจดค่าของ descriptor `CYBSP_DMA_DVP_CAM_CONTROLLER_Descriptor_0_config`:
   `dataSize` `descriptorType` `xCount` `yCount` `triggerInType` `interruptType`
2. คำนวณว่า descriptor หนึ่งตัวย้ายกี่ชิ้น และกี่ไบต์ต่อหนึ่งรอบ แล้วอธิบายว่า `CY_DMA_1ELEMENT` ใน `triggerInType` แปลว่า trigger หนึ่งครั้งย้ายเท่าไร
   (ความหมายของค่า enum เหล่านี้อยู่ใน [`cy_dma.h`](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_dma.h))
3. ใน [cycfg_dmas.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_dmas.h)
   หาว่า channel ของกล้องใช้ DMA block ไหน channel เท่าไร และ IRQ ชื่ออะไร BSP ยังตั้ง channel ไหนไว้อีกบ้าง
4. ในไดรเวอร์กล้อง หาทุกบรรทัดที่เรียก `SCB_CleanDCache_by_Addr()` แล้วเขียนตารางว่าแต่ละครั้ง clean อะไร และทำไมบัฟเฟอร์ข้อมูลไม่ต้อง invalidate
5. ตอบคำถามออกแบบ: ถ้าย้าย `line_buffer` ไปไว้ใน RAM ปกติที่ผ่าน cache ต้องเพิ่มอะไรในโค้ด ที่จุดไหน และจะรู้ได้อย่างไรว่าลืม (อาการที่จะเห็นบนภาพ)

**หลักฐานที่เก็บไว้ใน portfolio:** ตารางค่าตั้งของ descriptor พร้อมการคำนวณ ตาราง clean ทุกจุด และคำตอบข้อ 5
(หลักสูตรนี้ไม่ได้ขอให้รันไดรเวอร์กล้องบนบอร์ด และไม่ได้ยืนยันว่าแม่แบบที่ build ตามค่าเริ่มต้นคอมไพล์ไดรเวอร์นี้เข้าไปด้วย บทนี้ใช้มันเป็นโค้ดสำหรับอ่าน)

## ไปต่อ

- อ่านหัวไฟล์ของ [`cy_axidmac.h`](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_axidmac.h) แล้วเทียบกับ DataWire DMA ว่าต่างกันอย่างไร และไดรเวอร์กล้องใช้แต่ละตัวทำอะไร
- โจทย์ท้าทาย: ขยายแบบฝึกเป็นสามก้อน (triple buffering) แล้วดูว่าจำนวน overrun ในสถานการณ์เดียวกันลดลงไหม แลกกับหน่วยความจำเท่าไร
- เชื่อมกับบทถัดไป: UART, I2C และ SPI ในโมดูล 5 ต่างก็ใช้ DMA ได้เมื่อข้อมูลมาก ลองหาว่า BSP ตั้ง `CYBSP_DMA_TX_SPI_CONTROLLER` ไว้ให้ SPI ตัวไหน

บทถัดไปเข้าสู่โมดูล 5: [บทเรียน 5.1 UART](../../m05-serial-buses/l01-uart/README.md)

## สะท้อนคิด

- บั๊กของ cache ไม่เกิดบนคอมพิวเตอร์ที่คุณ test เกิดแค่บนชิปที่มี data cache คุณจะเขียน test หรือ checklist แบบไหนให้จับได้ก่อนถึงมือผู้ใช้
- งานไหนในโปรเจกต์ของคุณที่ CPU กำลังคัดลอกข้อมูลทีละไบต์ และถ้าย้ายไปให้ DMA จะได้เวลา CPU กลับมาเท่าไร

## แหล่งอ้างอิง

- [Infineon mtb-pdl-cat1 (Peripheral Driver Library) @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/tree/release-v3.24.0)
- [SDK: ไดรเวอร์กล้อง mtb_dvp_camera_ov7675.c (DMA, AXI DMAC, clean cache และ ping-pong)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/camera-dvp-ov7675/mtb_dvp_camera_ov7675.c)
- [SDK: cycfg_dmas.c ของ BSP (ค่าตั้ง descriptor และ channel)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_dmas.c)
- [Direct memory access (Wikipedia)](https://en.wikipedia.org/wiki/Direct_memory_access)
