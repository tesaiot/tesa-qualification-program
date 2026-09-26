---
id: c-found.m04.l03
lang: th
title: {th: Watchdog, en: The watchdog}
summary: {th: ใช้ watchdog ให้ระบบฟื้นตัวเองเมื่อค้าง โดยป้อนในจุดที่พิสูจน์ว่าระบบยังทำงานจริง, en: 'Use a watchdog so the system recovers when it hangs, feeding it only where progress is proven.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m04.l02]
objectives:
- {th: อธิบายหน้าที่ของ watchdog และผลเมื่อไม่ได้รับการป้อนภายในเวลาที่กำหนด, en: Explain what a watchdog does and what happens when it is not fed in time.}
- {th: ระบุจุดที่ถูกต้องในการป้อน watchdog ในโปรแกรมที่มีหลาย task และอธิบายว่าทำไมการป้อนใน ISR ของ timer เป็นกับดัก, en: Identify the correct feeding point in a multi-task program and explain why feeding from a timer ISR is a trap.}
- {th: ออกแบบการบันทึกสาเหตุการรีเซ็ตเพื่อให้รู้ว่า watchdog ทำงานเมื่อใด, en: Design reset-cause logging so you know when the watchdog fired.}
develops:
- {skill: mcu.watchdog, to: 3}
- {skill: rtos.basics, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
slides: slides.md
---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. อธิบายหน้าที่ของ watchdog และผลเมื่อไม่ได้รับการป้อนภายในเวลาที่กำหนด
2. ระบุจุดที่ถูกต้องในการป้อน watchdog ในโปรแกรมที่มีหลาย task และอธิบายว่าทำไมการป้อนใน ISR ของ timer เป็นกับดัก
3. ออกแบบการบันทึกสาเหตุการรีเซ็ตเพื่อให้รู้ว่า watchdog ทำงานเมื่อใด

ใช้เวลาประมาณ 70 นาที (แนวคิด 15 · ฝึก 25 · แล็บ 25 · เช็ก 5)

## ก่อนเริ่ม

ทวนจากบทก่อนหน้าสองข้อ

1. ตัวเฝ้าการค้างของเรดาร์ใน SDK รายงาน 0 ครั้งทั้งที่ task ค้าง เพราะมันอยู่ตรงไหน (บทเรียน 3.2)
2. ISR ของ timer ยังทำงานได้ไหม ถ้า task ทุกตัวติดอยู่ในลูปไม่รู้จบ (บทเรียน 4.1 และ 4.2)

## ดูของจริงก่อน

เปิด [examples/09_watchdog_sim.c](examples/09_watchdog_sim.c) ระบบจำลองมีสาม task และ watchdog ที่รีเซ็ตเมื่อไม่ถูกป้อนเกิน 10 tick
ที่ tick 40 task `sensor` ค้าง แล้วลองสองกลยุทธ์: A ป้อนใน ISR ของ timer ทุก tick, B ให้ผู้ดูแลป้อนเฉพาะเมื่อทุก task รายงานความคืบหน้าครบ
**ทายก่อนรัน** ว่ากลยุทธ์ A จะรีเซ็ตที่ tick ไหน

```sh
gcc -std=c11 -Wall -Wextra -o watchdog_sim examples/09_watchdog_sim.c
./watchdog_sim
```

กลยุทธ์ A **ไม่รีเซ็ตเลย** ทั้งที่ task ค้างไปแล้ว 60 tick เพราะ ISR ของ timer ไม่รู้และไม่สนว่า task เป็นอย่างไร
กลยุทธ์ B รีเซ็ตภายในเวลาที่ตั้ง และบอกได้ด้วยว่า task ไหนคือตัวที่หายไป watchdog ที่ป้อนผิดที่ดีกว่าไม่มีเลยนิดเดียว

## แนวคิด

### 1. watchdog คืออะไร และทำงานอย่างไรบน PSOC™ Edge

watchdog คือตัวนับที่เดินด้วยสัญญาณนาฬิกาของตัวเอง แยกจาก CPU ซอฟต์แวร์ต้อง "ป้อน" (ล้าง) มันเป็นระยะ ถ้าไม่ป้อนจนถึงค่าที่ตั้ง มันรีเซ็ตทั้งชิป
แนวคิดคือถ้าซอฟต์แวร์ยังป้อนได้ แปลว่ายังทำงาน ถ้าป้อนไม่ได้ แปลว่าค้าง และการเริ่มใหม่ดีกว่าค้างไปเรื่อย ๆ

PDL มีไดรเวอร์ WDT ใน [`cy_wdt.h`](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_wdt.h) BSP ของบอร์ดนี้ประกาศ
`CY_IP_MXS22SRSS` ([cy_device_headers_ns.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/cy_device_headers_ns.h#L733-L736))
ซึ่งทำให้ใช้ชุดฟังก์ชันแบบ match value ของ PDL ได้ ลำดับการตั้งตามเอกสารของไดรเวอร์คือ

| ขั้น | ฟังก์ชัน |
|---|---|
| ปลดล็อกและปิดก่อนแก้ | `Cy_WDT_Unlock()` แล้ว `Cy_WDT_Disable()` |
| เลือกสัญญาณนาฬิกา (สำหรับ MXS22SRSS คือ PILO หรือ clk_bak) | `Cy_WDT_SetClkSource()` |
| ตั้งเวลา | `Cy_WDT_SetMatch()` และถ้าต้องการสั้นลง `Cy_WDT_SetIgnoreBits()` |
| เปิด แล้วล็อกกันแก้โดยไม่ตั้งใจ | `Cy_WDT_Enable()` แล้ว `Cy_WDT_Lock()` |
| ป้อน | `Cy_WDT_ClearWatchdog()` ซึ่งเอกสารเขียนว่า "Clears ("feeds") the watchdog, to prevent a XRES device reset" |

ข้อเตือนจากเอกสารของ PDL ที่ต้องรู้ก่อนเปิดใช้: เวลาของ watchdog ต้องยาวกว่าเวลาบูตของชิป ("a WDT reset can be generated faster than a device start-up")
การเปลี่ยนค่ามีผลช้าไปสองสามจังหวะของสัญญาณนาฬิกาความถี่ต่ำ และ oscillator ความแม่นยำต่ำต้องเผื่อ margin ให้มาก (เอกสารยกตัวอย่าง ILO ของชิปรุ่นอื่นที่คลาดได้ ±30%)
ความแม่นยำของ PILO หรือ clk_bak บนชิปนี้ให้ดูใน datasheet ของชิป และระหว่างดีบัก การหยุด CPU ที่ breakpoint อาจทำให้ watchdog รีเซ็ตกลางทาง (บทเรียน 3.1)

**สถานะในแม่แบบของ SDK:** เราค้นซอร์สของแม่แบบ mtb-only ที่ commit นี้แล้ว ไม่พบการเปิด hardware watchdog (`Cy_WDT_Enable` หรือ `Cy_WDT_ClearWatchdog`)
มีเพียง `Cy_WDT_Unlock()` ในโค้ดตั้งสัญญาณนาฬิกาที่ BSP สร้าง ([cycfg_clocks.c บรรทัด 584](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_clocks.c#L584))
ส่วนที่ SDK ใช้จริงคือ watchdog แบบซอฟต์แวร์ของ task ตัวหนึ่ง ซึ่งเป็นหัวข้อถัดไป

### 2. ป้อนที่ไหน: ที่ที่พิสูจน์ว่าระบบคืบหน้า

watchdog ตรวจได้เฉพาะสิ่งที่ "คนป้อน" รู้ ถ้าป้อนจาก ISR ของ timer มันพิสูจน์ได้แค่ว่า interrupt ของ timer ยังทำงาน ซึ่งมักจริงแม้ task ทุกตัวตาย
ถ้าให้แต่ละ task ป้อนเอง task ตัวไหนก็ได้ที่ยังรอดจะป้อนแทนตัวที่ตายไปแล้ว รูปแบบที่ใช้ได้คือ **check-in กับผู้ดูแลหนึ่งคน**

1. task ที่สำคัญแต่ละตัวตั้งบิตของตัวเองเมื่อ **ทำงานคืบหน้าจริง** (อ่านเซนเซอร์ได้ ส่งข้อความได้) ไม่ใช่แค่ตื่นขึ้นมา
2. ผู้ดูแลเป็น task ที่ความสำคัญต่ำ ตรวจเป็นระยะ ป้อนเฉพาะเมื่อบิตครบ แล้วล้างบิตทั้งหมด
3. เวลาของ watchdog ยาวกว่ารอบที่ช้าที่สุดของ task ทุกตัว บวก margin

ผู้ดูแลที่ความสำคัญต่ำยังจับอีกอาการได้ฟรี: task ความสำคัญสูงที่วนไม่ปล่อย CPU ผู้ดูแลจะไม่ได้รัน watchdog จึงรีเซ็ต

SDK มีตัวอย่าง watchdog แบบซอฟต์แวร์ของจริง [08_deepcraft_link.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/08_deepcraft_link.c#L37-L45)
อธิบายว่า task ของ model link เคย "asleep inside its own queue receive with a command outstanding" หลังสลับโมเดลไปเป็นร้อยครั้ง
`deepcraft_task_watchdog()` ต้องถูกเรียกราว 1 Hz "from a context that never blocks" และมันตรวจพบงานค้างแล้วปลุก task ให้ทำต่อ
คอมเมนต์เดียวกันยอมรับตรง ๆ ว่า "The watchdog does not fix the underlying fault" watchdog คือการฟื้นตัว ไม่ใช่การแก้บั๊ก ต้องบันทึกทุกครั้งที่มันทำงาน

### 3. บันทึกสาเหตุการรีเซ็ต: รู้ให้ได้ว่า watchdog ทำงานเมื่อไร

watchdog ที่รีเซ็ตเงียบ ๆ ทำให้ระบบดูเหมือน "บางทีก็บูตใหม่เอง" สิ่งที่ต้องมีคือบันทึกที่รอดข้ามการรีเซ็ต

- **อ่านสาเหตุ** `Cy_SysLib_GetResetReason()` คืนชุดบิต เช่น `CY_SYSLIB_RESET_HWWDT` (0x0001) `CY_SYSLIB_RESET_SOFT` (0x0010)
  `CY_SYSLIB_RESET_SWWDT0`..`3` ของ multi-counter watchdog (ดูตารางใน [`cy_syslib.h`](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_syslib.h))
  ทดสอบด้วย `&` เพราะอาจมีหลายบิตพร้อมกัน BSP ของ SDK เองใช้ฟังก์ชันนี้ตอนตั้งสัญญาณนาฬิกา และเขียนกำกับว่าค่า 0 หมายถึง "POR, XRES, or BOD"
  ([cycfg_clocks.c บรรทัด 571-575](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_clocks.c#L571-L575))
  หลังบันทึกแล้วเรียก `Cy_SysLib_ClearResetReason()` ไม่อย่างนั้นบูตครั้งต่อไปจะเห็นสาเหตุเดิม
- **เก็บร่องรอยไว้ใน RAM ที่ไม่ถูกล้างตอนบูต** linker script ของ SDK มี section `.noinit` ที่ startup ไม่แตะ
  ([pse84_ns_cm33.ld บรรทัด 339-343](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/COMPONENT_CM33/TOOLCHAIN_GCC_ARM/pse84_ns_cm33.ld#L339-L343))
  ผู้ดูแลเขียน "task ไหนยังไม่ check in" ลงไปทุกรอบ หลังรีเซ็ตจึงรู้ว่าใครค้าง หลังเปิดไฟครั้งแรกค่าใน RAM เป็นขยะ ต้องมี magic number ไว้แยก
  CM55 ของแม่แบบใช้หลักเดียวกัน มันเขียน fault marker ไว้ที่ที่อยู่คงที่ใน SRAM พร้อมคอมเมนต์ว่า "survives until power cycle"
- **ส่งออก** พิมพ์ตอนบูต นับจำนวน และถ้ามีการเชื่อมต่อ ส่งขึ้นระบบที่เก็บ log ได้

## ตัวอย่างสมบูรณ์

[examples/09_watchdog_sim.c](examples/09_watchdog_sim.c) ทำงานเป็นสามท่า

- **ท่าที่ 1** แต่ละ task ทำงานหนึ่งรอบแล้ว check in ด้วยการตั้งบิต (task `sensor` ค้างตั้งแต่ tick 40)
- **ท่าที่ 2** กลยุทธ์ A ป้อนทุก tick ไม่ดูอะไร กลยุทธ์ B ป้อนเมื่อบิตครบแล้วล้างบิต
- **ท่าที่ 3** watchdog จำลองนับต่อ ถ้าเกินเวลาพิมพ์ว่ารีเซ็ต พร้อมชื่อ task ที่ขาด check in

ลองแก้แล้วทายก่อนรัน

1. ในกลยุทธ์ B ลบบรรทัด `checkin = 0u;` ออก แล้วรัน watchdog ยังจับการค้างได้ไหม เพราะอะไร
2. เปลี่ยน `WDT_TIMEOUT_TICKS` เป็น 1 กลยุทธ์ B ทำอะไร นั่นบอกอะไรเรื่องการเลือกเวลาของ watchdog
3. ทำให้ task `ui` ทำงานคืบหน้าแค่ทุก 5 tick (check in ทุก 5 tick) แล้วหาค่า `WDT_TIMEOUT_TICKS` ที่เล็กที่สุดที่ไม่รีเซ็ตผิด

## ฝึกเติม

เปิด [practice/09_watchdog.c](practice/09_watchdog.c) มีช่องให้เติม 5 จุด ผู้ดูแลแบบ check-in และบันทึกการบูตที่รอดข้ามการรีเซ็ต

1. `wd_checkin()` ตั้งบิตของ task
2. `supervisor_poll()` ไม่ป้อนถ้ายังขาด task
3. `supervisor_poll()` ล้างบิตหลังป้อน
4. `boot_record_update()` แยกขยะใน RAM ออกด้วย magic
5. `boot_record_update()` นับการรีเซ็ตจาก watchdog และเก็บชื่อ task ที่ขาด

```sh
gcc -std=c11 -Wall -Wextra -o watchdog practice/09_watchdog.c && ./watchdog
```

## เฉลย

ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/09_watchdog.c](solution/09_watchdog.c)
สองจุดที่ควรเทียบ: เฉลยทดสอบสาเหตุการรีเซ็ตด้วย `&` ไม่ใช่ `==` และคอมเมนต์เตือนว่า `|=` ใน `wd_checkin()` ที่หลาย task เรียกพร้อมกันบนบอร์ดจริง
ต้องมี critical section หรือใช้ event group ของ FreeRTOS แทน ซึ่งเป็นความรู้จากบทเรียน 1.3 ที่กลับมาในที่ที่ไม่คาดคิด

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) (บนเว็บไซต์อยู่ท้ายหน้านี้) ครอบคลุมเป้าหมายทั้งสามข้อ ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน

## แล็บ

**งาน:** อ่านสาเหตุการรีเซ็ตของบอร์ดจริงในสถานการณ์ต่าง ๆ แล้วออกแบบการป้อน watchdog ให้แม่แบบ

1. ในโปรเจกต์ของคุณ (บน branch ใหม่ ตามบทเรียน 2.3) เพิ่มสามบรรทัดนี้ใน `proj_cm33_ns/main.c` ทันทีหลัง `init_retarget_io();`
   (เอกสาร B1 ของ SDK บอกว่าจากจุดนี้ UART พร้อมแล้ว)
   ```c
   uint32_t reset_reason = Cy_SysLib_GetResetReason();
   printf("[RST] reason=0x%08lx%s\r\n", (unsigned long)reset_reason,
          (reset_reason & CY_SYSLIB_RESET_HWWDT) ? " HWWDT" : "");
   ```
   build แล้ว flash
2. บันทึกค่าที่พิมพ์ในสี่สถานการณ์: ถอดสายเสียบใหม่, กดปุ่มรีเซ็ตบนบอร์ด (ถ้ามี), หลัง `make program`, และถอดเสียบอีกครั้งหลังจากนั้น
   ค่าไหนเป็น 0 ค่าไหนมีบิต และบิตค้างข้ามการรีเซ็ตหรือไม่ (โค้ดนี้ยังไม่ล้างสาเหตุ นั่นเป็นส่วนหนึ่งของสิ่งที่คุณสังเกต)
3. เทียบค่าที่ได้กับตารางใน `cy_syslib.h` ข้อไหนตรงกับที่คาด ข้อไหนไม่ตรง เขียนสิ่งที่เห็นจริงแยกจากสิ่งที่อนุมาน
4. ออกแบบ (บนกระดาษ) การเปิด hardware watchdog ให้แม่แบบ: ระบุ task ที่ต้อง check in อย่างน้อยสามตัวจาก task ที่แม่แบบสร้าง
   (ดู `main()` ใน proj_cm33_ns/main.c) รอบที่ช้าที่สุดของแต่ละตัว เวลาของ watchdog ที่เลือกพร้อม margin และจุดที่วางผู้ดูแล
   (หลักสูตรนี้ยังไม่ได้ทดสอบการเปิด hardware watchdog บนแม่แบบนี้ ถ้าคุณลองจริง ให้ทำบน branch แยก และบันทึกผลทั้งหมด รวมผลต่อการดีบัก)

**หลักฐานที่เก็บไว้ใน portfolio:** diff ของการแก้ main.c ตารางค่าสาเหตุการรีเซ็ตทั้งสี่สถานการณ์พร้อมคำอธิบาย และแบบร่างการออกแบบ watchdog ข้อ 4

## ไปต่อ

- อ่านหัวข้อ Functional Description, Clearing WDT และ Reset Detection ในหัวไฟล์ของ [`cy_wdt.h`](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_wdt.h)
  แล้วคำนวณว่าถ้าใช้ match value แบบในเอกสาร ต้องป้อนบ่อยแค่ไหน
- เปรียบเทียบ watchdog แบบ window (ห้ามป้อนเร็วเกินไปด้วย) กับแบบธรรมดา ใน [Watchdog timer (Wikipedia)](https://en.wikipedia.org/wiki/Watchdog_timer) แบบ window จับบั๊กอะไรได้เพิ่ม

บทถัดไป: [บทเรียน 4.4 DMA](../l04-dma/README.md)

## สะท้อนคิด

- ระบบที่คุณเคยใช้ ระบบไหนที่ "บูตใหม่เองเป็นบางครั้ง" ตอนนี้คุณจะถามผู้พัฒนาว่าอะไร
- ถ้า watchdog ช่วยให้ผลิตภัณฑ์ดูเหมือนไม่เคยค้าง ทีมจะรู้ได้อย่างไรว่ามีบั๊กที่ต้องแก้

## แหล่งอ้างอิง

- [SDK: cm55/edge_ai/08_deepcraft_link.c (deepcraft_task_watchdog)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/08_deepcraft_link.c)
- [SDK: cycfg_clocks.c ของ BSP (การใช้ Cy_SysLib_GetResetReason และ Cy_WDT_Unlock)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_clocks.c)
- [Infineon mtb-pdl-cat1 (Peripheral Driver Library) @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/tree/release-v3.24.0)
- [Watchdog timer (Wikipedia)](https://en.wikipedia.org/wiki/Watchdog_timer)
