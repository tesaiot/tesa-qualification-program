---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 4.4 — DMA"
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

# บทเรียน 4.4 — DMA

## ย้ายข้อมูลโดยไม่ใช้ CPU และรู้ข้อควรระวังเรื่องบัฟเฟอร์ที่ DMA กับ CPU ใช้ร่วมกัน

**โมดูล 4 — Timer, Interrupt, Watchdog, DMA และสัญญาณนาฬิกา**

หลักสูตร **พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge** · ต่อจากบทเรียน 4.3

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. อธิบายว่า DMA ช่วยลดภาระ CPU ในการย้ายข้อมูลอย่างไร และเมื่อใดไม่คุ้ม
2. ระบุความเสี่ยงของบัฟเฟอร์ที่ DMA กับ CPU ใช้ร่วมกัน เช่น cache และการอ่านก่อนการย้ายเสร็จ

ใช้เวลาประมาณ 70 นาที — แล็บของบทนี้เป็นการอ่านโค้ดและค่าตั้งจริงของ SDK เพราะแคตตาล็อกที่ commit นี้ยังไม่มีตัวอย่าง DMA โดยตรง

---

## ก่อนเริ่ม

ทวนจากบทก่อนหน้าสองข้อ

1. บัฟเฟอร์วงแหวนในบทเรียน 1.3 ต้องเขียนข้อมูลก่อนแล้วจึงเลื่อน `head` ทำไมลำดับนี้สำคัญเมื่อผู้เขียนเป็นอีกบริบทหนึ่ง
2. ISR ที่ดีในบทเรียน 4.1 ทำงานอะไรบ้าง และส่งอะไรต่อให้ task

---

## ดูของจริงก่อน

เปิด [examples/10_dma_cache_sim.c](examples/10_dma_cache_sim.c) — จำลองหน่วยความจำจริงที่ "DMA" เขียน และ cache ที่ CPU อ่านผ่าน เหมือน Cortex-M55 ที่มี data cache **ทายก่อนรัน**: บรรทัด `frame 2, stale cache:` จะพิมพ์ค่าอะไร

```sh
gcc -std=c11 -Wall -Wextra -o dma_cache_sim examples/10_dma_cache_sim.c
./dma_cache_sim
```

DMA เขียน `BB` ครบแล้ว แต่ CPU ยังเห็น `AA` เพราะอ่านจากสำเนาใน cache จนกว่าจะ invalidate และบรรทัด `frame 3, read too early:` แสดงบั๊กอีกแบบ — CPU อ่านตอน DMA เขียนไปครึ่งเดียว ได้ `CC` ครึ่งหนึ่งกับ `BB` อีกครึ่ง บั๊กทั้งสองแบบไม่ทำให้โปรแกรมล้ม มันแค่ให้ข้อมูลผิดอย่างเงียบ ๆ

---

## แนวคิด (1) — DMA ทำงานแทน CPU ได้อย่างไร

**DMA** คือฮาร์ดแวร์ที่ย้ายข้อมูลระหว่างรีจิสเตอร์ของอุปกรณ์กับหน่วยความจำ โดยไม่ต้องให้ CPU คัดลอกทีละไบต์ CPU ตั้ง **descriptor** ครั้งเดียว (ต้นทาง ปลายทาง ขนาดของแต่ละชิ้น จำนวนชิ้น) แล้วไปทำอย่างอื่น DMA ย้ายเองทุกครั้งที่อุปกรณ์ส่งสัญญาณ trigger และแจ้งด้วย interrupt เมื่อครบ

| งาน | ทางที่ SDK ใช้ | เหตุผล |
|---|---|---|
| รับภาพจากกล้องทีละบรรทัด | DMA + AXI DMAC | ข้อมูลมาเร็วกว่าที่ CPU จะรับทีละไบต์ได้ |
| อ่านเขียน FIFO เรดาร์ผ่าน SPI | `Cy_SCB_SPI_Transfer()` แบบ interrupt | ปริมาณพอที่ ISR จัดการได้ |
| ทดสอบ SPI 8 ไบต์บน header | bit-bang ด้วย `Cy_GPIO_Write()` | งานสั้นมาก การตั้ง DMA ไม่คุ้ม |

> DMA **ไม่คุ้ม** เมื่อข้อมูลน้อยจนเวลาตั้ง descriptor มากกว่าเวลาคัดลอกเอง เมื่อต้องประมวลผลทีละไบต์ระหว่างทางอยู่แล้ว หรือเมื่อช่อง DMA มีน้อย

---

## แนวคิด (2) — ความเสี่ยงที่หนึ่ง: อ่านก่อน DMA เขียนเสร็จ

DMA กับ CPU ทำงานพร้อมกันจริง บัฟเฟอร์ที่ DMA กำลังเขียนอยู่ห้ามให้ CPU อ่าน วิธีมาตรฐานคือ **ping-pong** — มีสองก้อน DMA เขียนก้อนหนึ่งขณะ CPU ประมวลผลอีกก้อน แล้วสลับกันเมื่อ DMA แจ้งว่าเสร็จ

ไดรเวอร์กล้องใน SDK: ISR ของสัญญาณ HREF ตั้งปลายทาง DMA เป็น `line_buffer[row_buffer_flag]` แล้วสลับ `row_buffer_flag` ส่วน ISR ของ VSYNC สลับ frame buffer แล้วตั้ง `*_frame_ready = true`

> ถ้า CPU ช้ากว่า DMA ต้องมีนโยบายชัดว่าจะทิ้งข้อมูลก้อนไหน และ **นับ** ทุกครั้งที่ทิ้ง (overrun)

---

## แนวคิด (3) — ความเสี่ยงที่สอง: cache

Cortex-M55 มี data cache — CPU อ่านเขียนผ่านสำเนาใน cache ส่วน DMA อ่านเขียนหน่วยความจำจริงโดยไม่ผ่าน cache ความจริงสองชุดนี้ต้องทำให้ตรงกันเอง

- **CPU เขียน แล้ว DMA อ่าน** ต้อง **clean** — เขียนสำเนาใน cache ลงหน่วยความจำก่อนสั่ง DMA
- **DMA เขียน แล้ว CPU อ่าน** ต้อง **invalidate** — ทิ้งสำเนาเก่าใน cache ก่อนอ่าน ไม่งั้นได้ค่าเก่า
- หรือ **วางบัฟเฟอร์ไว้ในหน่วยความจำที่ไม่ผ่าน cache** แล้วไม่ต้องทำทั้งสองอย่าง

---

## ตัวอย่างสมบูรณ์ — clean/invalidate จริงในไดรเวอร์กล้อง

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
```

ที่มา: [mtb_dvp_camera_ov7675.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/camera-dvp-ov7675/mtb_dvp_camera_ov7675.c#L637-L648) — บัฟเฟอร์บรรทัดอยู่ใน `.cy_sharedmem` (ไม่ผ่าน cache) แต่ descriptor ผ่าน cache จึงต้อง clean ทุกครั้งที่ CPU แก้มัน ก่อนเปิด channel

---

## ตัวอย่างสมบูรณ์ — สามท่าใน 10_dma_cache_sim.c

**ท่าที่ 1** DMA เติมบัฟเฟอร์ครบ CPU อ่านครั้งแรก cache ว่างอยู่จึงได้ของจริง
**ท่าที่ 2** DMA เติมรอบสอง CPU อ่านโดยไม่ invalidate ได้สำเนาเก่า แล้ว invalidate แล้วอ่านใหม่ได้ของจริง
**ท่าที่ 3** invalidate ถูกแล้ว แต่อ่านเร็วเกินไป ได้ข้อมูลครึ่งเก่าครึ่งใหม่ จนกว่าจะรอให้ DMA เสร็จ

ลองแก้แล้วทายก่อนรัน: ลบ `cache_invalidate(&b);` บรรทัดแรกในท่าที่ 3 ออก บรรทัด `read too early` จะเห็นอะไร และบั๊กสองแบบซ้อนกันทำให้วินิจฉัยยากขึ้นอย่างไร

---

## ฝึกเติม

เปิด [practice/10_ping_pong.c](practice/10_ping_pong.c) — มีช่องให้เติม 6 จุด มากที่สุดในโมดูลนี้ (บทปิดท้ายของโมดูล) ตัวจัดการ ping-pong ต้องไม่ให้ DMA ทับก้อนของ CPU นับ overrun เมื่อ CPU ช้า และ invalidate ก่อนคืนก้อนให้ CPU อ่าน

```sh
gcc -std=c11 -Wall -Wextra -o ping_pong practice/10_ping_pong.c && ./ping_pong
```

test ตั้งใจให้ CPU อ่านก้อนแรกไว้หนึ่งครั้งก่อนเริ่ม cache จึงมีสำเนาเก่าค้างอยู่ ถ้าลืม invalidate test ข้อที่อ่านค่า `0x11` จะล้ม

ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/10_ping_pong.c](solution/10_ping_pong.c)

---

## เช็กความเข้าใจ

ตอบคำถาม 4 ข้อใน [quiz.yaml](quiz.yaml) ครอบคลุมเป้าหมายทั้งสองข้อ (ตอบถูกตั้งแต่ 3 ข้อขึ้นไปถือว่าจบบทเรียน)

1. ข้อใดอธิบายการทำงานของ DMA ได้ถูกต้องที่สุด
2. กรณีใดที่ DMA มักไม่คุ้ม (เลือกได้หลายข้อ)
3. บน CM55 ที่มี data cache DMA เพิ่งเขียนบัฟเฟอร์ใน RAM ปกติที่ผ่าน cache เสร็จ CPU ต้องทำอะไรก่อนอ่าน
4. ไดรเวอร์กล้องใน SDK ป้องกันความเสี่ยงของบัฟเฟอร์ร่วมอย่างไร (เลือกได้หลายข้อ)

---

## แล็บ

**งาน:** อ่านค่าตั้ง DMA จริงใน BSP ของ SDK และไดรเวอร์กล้อง แล้วตอบด้วยหลักฐานว่าข้อมูลไหลอย่างไร

1. เปิด [cycfg_dmas.c ของ BSP](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_dmas.c) จดค่าของ descriptor: `dataSize` `xCount` `yCount` `triggerInType`
2. คำนวณว่า descriptor หนึ่งตัวย้ายกี่ชิ้น และกี่ไบต์ต่อหนึ่งรอบ อธิบายว่า `CY_DMA_1ELEMENT` แปลว่า trigger หนึ่งครั้งย้ายเท่าไร
3. ใน `cycfg_dmas.h` หาว่า channel ของกล้องใช้ DMA block ไหน channel เท่าไร IRQ ชื่ออะไร
4. ในไดรเวอร์กล้อง หาทุกบรรทัดที่เรียก `SCB_CleanDCache_by_Addr()` เขียนตารางว่าแต่ละครั้ง clean อะไร และทำไมบัฟเฟอร์ข้อมูลไม่ต้อง invalidate
5. ตอบคำถามออกแบบ: ถ้าย้าย `line_buffer` ไปไว้ใน RAM ปกติที่ผ่าน cache ต้องเพิ่มอะไรในโค้ด และจะรู้ได้อย่างไรว่าลืม

**หลักฐานที่เก็บไว้ใน portfolio:** ตารางค่าตั้งของ descriptor พร้อมการคำนวณ ตาราง clean ทุกจุด และคำตอบข้อ 5

---

## ไปต่อ

- อ่านหัวไฟล์ของ [`cy_axidmac.h`](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_axidmac.h) แล้วเทียบกับ DataWire DMA ว่าต่างกันอย่างไร
- โจทย์ท้าทาย: ขยายแบบฝึกเป็นสามก้อน (triple buffering) แล้วดูว่าจำนวน overrun ลดลงไหม แลกกับหน่วยความจำเท่าไร

บทถัดไปเข้าสู่โมดูล 5: [บทเรียน 5.1 — UART](../../m05-serial-buses/l01-uart/README.md)

---

## แหล่งที่มาและเครดิต

"พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

โค้ดของหลักสูตรนี้ (`examples/`, `practice/`, `solution/`) Apache-2.0 · โค้ดของ SDK ไม่ได้คัดลอกเป็นไฟล์
บทเรียนยกมาเป็นช่วงสั้น ๆ พร้อมลิงก์ไปยังไฟล์ที่ commit `ef72c1b` (Apache-2.0, Copyright 2025 Infineon Technologies AG ดัดแปลงโดยทีม TESA, tesaiot-pse84-devkit-sdk)
