---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 4.3 — Watchdog"
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

# บทเรียน 4.3 — Watchdog

## ใช้ watchdog ให้ระบบฟื้นตัวเองเมื่อค้าง โดยป้อนในจุดที่พิสูจน์ว่าระบบยังทำงานจริง

**โมดูล 4 — Timer, Interrupt, Watchdog, DMA และสัญญาณนาฬิกา**

หลักสูตร **พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge** · ต่อจากบทเรียน 4.2

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. อธิบายหน้าที่ของ watchdog และผลเมื่อไม่ได้รับการป้อนภายในเวลาที่กำหนด
2. ระบุจุดที่ถูกต้องในการป้อน watchdog ในโปรแกรมที่มีหลาย task และอธิบายว่าทำไมการป้อนใน ISR ของ timer เป็นกับดัก
3. ออกแบบการบันทึกสาเหตุการรีเซ็ตเพื่อให้รู้ว่า watchdog ทำงานเมื่อใด

ใช้เวลาประมาณ 70 นาที

---

## ก่อนเริ่ม

ทวนจากบทก่อนหน้าสองข้อ

1. ตัวเฝ้าการค้างของเรดาร์ใน SDK รายงาน 0 ครั้งทั้งที่ task ค้าง เพราะมันอยู่ตรงไหน
2. ISR ของ timer ยังทำงานได้ไหม ถ้า task ทุกตัวติดอยู่ในลูปไม่รู้จบ

---

## ดูของจริงก่อน

เปิด [examples/09_watchdog_sim.c](examples/09_watchdog_sim.c) — สาม task และ watchdog ที่รีเซ็ตเมื่อไม่ถูกป้อนเกิน 10 tick ที่ tick 40 task `sensor` ค้าง แล้วลองสองกลยุทธ์: A ป้อนใน ISR ของ timer ทุก tick, B ให้ผู้ดูแลป้อนเฉพาะเมื่อทุก task รายงานความคืบหน้าครบ **ทายก่อนรัน**: กลยุทธ์ A จะรีเซ็ตที่ tick ไหน

```sh
gcc -std=c11 -Wall -Wextra -o watchdog_sim examples/09_watchdog_sim.c
./watchdog_sim
```

กลยุทธ์ A **ไม่รีเซ็ตเลย** ทั้งที่ task ค้างไปแล้ว 60 tick เพราะ ISR ของ timer ไม่รู้และไม่สนว่า task เป็นอย่างไร กลยุทธ์ B รีเซ็ตภายในเวลาที่ตั้ง และบอกได้ด้วยว่า task ไหนคือตัวที่หายไป — watchdog ที่ป้อนผิดที่ดีกว่าไม่มีเลยนิดเดียว

---

## แนวคิด (1) — watchdog คืออะไร และทำงานอย่างไรบน PSOC™ Edge

watchdog คือตัวนับที่เดินด้วยสัญญาณนาฬิกาของตัวเอง แยกจาก CPU ซอฟต์แวร์ต้อง "ป้อน" (ล้าง) เป็นระยะ ถ้าไม่ป้อนจนถึงค่าที่ตั้ง มันรีเซ็ตทั้งชิป

| ขั้น | ฟังก์ชัน |
|---|---|
| ปลดล็อกและปิดก่อนแก้ | `Cy_WDT_Unlock()` แล้ว `Cy_WDT_Disable()` |
| เลือกสัญญาณนาฬิกา (PILO หรือ clk_bak) | `Cy_WDT_SetClkSource()` |
| ตั้งเวลา | `Cy_WDT_SetMatch()` / `Cy_WDT_SetIgnoreBits()` |
| เปิด แล้วล็อกกันแก้โดยไม่ตั้งใจ | `Cy_WDT_Enable()` แล้ว `Cy_WDT_Lock()` |
| ป้อน | `Cy_WDT_ClearWatchdog()` |

> ข้อเตือนจาก PDL: เวลาของ watchdog ต้องยาวกว่าเวลาบูตของชิป และ oscillator ความแม่นยำต่ำต้องเผื่อ margin มาก (คลาดได้ถึง ±30%) — การหยุด CPU ที่ breakpoint อาจทำให้ watchdog รีเซ็ตกลางทาง

**สถานะในแม่แบบของ SDK:** ค้นซอร์สแล้วไม่พบการเปิด hardware watchdog จริง มีเพียง `Cy_WDT_Unlock()` ในโค้ดตั้งสัญญาณนาฬิกา — SDK ใช้ watchdog แบบซอฟต์แวร์ของ task แทน

---

## แนวคิด (2) — ป้อนที่ไหน: ที่ที่พิสูจน์ว่าระบบคืบหน้า

watchdog ตรวจได้เฉพาะสิ่งที่ "คนป้อน" รู้ — ถ้าป้อนจาก ISR ของ timer มันพิสูจน์ได้แค่ว่า interrupt ของ timer ยังทำงาน ซึ่งมักจริงแม้ task ทุกตัวตาย

รูปแบบที่ใช้ได้คือ **check-in กับผู้ดูแลหนึ่งคน**

1. task ที่สำคัญแต่ละตัวตั้งบิตของตัวเองเมื่อ **ทำงานคืบหน้าจริง** ไม่ใช่แค่ตื่นขึ้นมา
2. ผู้ดูแลเป็น task ที่ความสำคัญต่ำ ป้อนเฉพาะเมื่อบิตครบ แล้วล้างบิตทั้งหมด
3. เวลาของ watchdog ยาวกว่ารอบที่ช้าที่สุดของ task ทุกตัว บวก margin

> ผู้ดูแลความสำคัญต่ำยังจับได้ฟรี: task ความสำคัญสูงที่วนไม่ปล่อย CPU ผู้ดูแลจะไม่ได้รัน watchdog จึงรีเซ็ต

---

## แนวคิด (2) ต่อ — watchdog แบบซอฟต์แวร์จริงใน SDK

`deepcraft_task_watchdog()` ของ SDK ต้องถูกเรียกราว 1 Hz **"from a context that never blocks"** — task ของ model link เคย **"asleep inside its own queue receive with a command outstanding"** หลังสลับโมเดลไปเป็นร้อยครั้ง มันตรวจพบงานค้างแล้วปลุก task ให้ทำต่อ

> คอมเมนต์ยอมรับตรง ๆ ว่า **"The watchdog does not fix the underlying fault"** — watchdog คือการฟื้นตัว ไม่ใช่การแก้บั๊ก ต้องบันทึกทุกครั้งที่มันทำงาน

---

## แนวคิด (3) — บันทึกสาเหตุการรีเซ็ต

watchdog ที่รีเซ็ตเงียบ ๆ ทำให้ระบบดูเหมือน "บางทีก็บูตใหม่เอง"

- **อ่านสาเหตุ** `Cy_SysLib_GetResetReason()` คืนชุดบิต เช่น `CY_SYSLIB_RESET_HWWDT` (0x0001) `CY_SYSLIB_RESET_SOFT` (0x0010) ทดสอบด้วย `&` เพราะอาจมีหลายบิตพร้อมกัน — 0 หมายถึง "POR, XRES, or BOD" หลังบันทึกแล้วเรียก `Cy_SysLib_ClearResetReason()`
- **เก็บร่องรอยไว้ใน RAM ที่ไม่ถูกล้างตอนบูต** — linker script มี section `.noinit` ที่ startup ไม่แตะ ผู้ดูแลเขียน "task ไหนยังไม่ check in" ลงไปทุกรอบ ต้องมี magic number แยกขยะครั้งแรกออก — CM55 ใช้หลักเดียวกัน เขียน fault marker ไว้ที่ที่อยู่คงที่ใน SRAM ที่ **"survives until power cycle"**
- **ส่งออก** พิมพ์ตอนบูต นับจำนวน และส่งขึ้นระบบเก็บ log ถ้ามีการเชื่อมต่อ

---

## ตัวอย่างสมบูรณ์ — สามท่าใน 09_watchdog_sim.c

**ท่าที่ 1** แต่ละ task ทำงานหนึ่งรอบแล้ว check in ด้วยการตั้งบิต (task `sensor` ค้างตั้งแต่ tick 40)
**ท่าที่ 2** กลยุทธ์ A ป้อนทุก tick ไม่ดูอะไร กลยุทธ์ B ป้อนเมื่อบิตครบแล้วล้างบิต
**ท่าที่ 3** watchdog จำลองนับต่อ ถ้าเกินเวลาพิมพ์ว่ารีเซ็ต พร้อมชื่อ task ที่ขาด check in

```c
// กลยุทธ์ B: ป้อนเฉพาะเมื่อทุก task check in ครบ
if ((checkin_mask & ALL_TASKS_MASK) == ALL_TASKS_MASK) {
    wdt_ticks_since_feed = 0u;      // ป้อนจริง
    checkin_mask = 0u;              // ล้างบิตสำหรับรอบถัดไป
}
```

ลองแก้แล้วทายก่อนรัน: ในกลยุทธ์ B ลบบรรทัด `checkin = 0u;` ออก watchdog ยังจับการค้างได้ไหม เพราะอะไร

---

## ฝึกเติม

เปิด [practice/09_watchdog.c](practice/09_watchdog.c) — มีช่องให้เติม 5 จุด ผู้ดูแลแบบ check-in และบันทึกการบูตที่รอดข้ามการรีเซ็ต

1. `wd_checkin()` ตั้งบิตของ task
2. `supervisor_poll()` ไม่ป้อนถ้ายังขาด task
3. `supervisor_poll()` ล้างบิตหลังป้อน
4. `boot_record_update()` แยกขยะใน RAM ออกด้วย magic
5. `boot_record_update()` นับการรีเซ็ตจาก watchdog และเก็บชื่อ task ที่ขาด

```sh
gcc -std=c11 -Wall -Wextra -o watchdog practice/09_watchdog.c && ./watchdog
```

ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/09_watchdog.c](solution/09_watchdog.c) — เฉลยทดสอบสาเหตุการรีเซ็ตด้วย `&` ไม่ใช่ `==` และเตือนว่า `|=` ใน `wd_checkin()` ที่หลาย task เรียกพร้อมกันบนบอร์ดจริง ต้องมี critical section หรือใช้ event group

---

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) ครอบคลุมเป้าหมายทั้งสามข้อ (ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน)

1. ถ้าเฟิร์มแวร์ไม่ป้อน hardware watchdog ภายในเวลาที่ตั้ง จะเกิดอะไร
2. ข้อใดเป็นข้อควรระวังเมื่อเลือกเวลาของ watchdog ตามเอกสารของ PDL (เลือกได้หลายข้อ)
3. ทำไมการป้อน watchdog ใน ISR ของ timer จึงเป็นกับดัก
4. เรียงขั้นของรูปแบบ check-in กับผู้ดูแลหนึ่งคนในหนึ่งรอบ
5. ออกแบบให้รู้ว่า watchdog รีเซ็ตเมื่อไรและเพราะ task ไหน ข้อใดควรทำ (เลือกได้หลายข้อ)

---

## แล็บ

**งาน:** อ่านสาเหตุการรีเซ็ตของบอร์ดจริงในสถานการณ์ต่าง ๆ แล้วออกแบบการป้อน watchdog ให้แม่แบบ

1. เพิ่มสามบรรทัดนี้ใน `proj_cm33_ns/main.c` ทันทีหลัง `init_retarget_io();`
   ```c
   uint32_t reset_reason = Cy_SysLib_GetResetReason();
   printf("[RST] reason=0x%08lx%s\r\n", (unsigned long)reset_reason,
          (reset_reason & CY_SYSLIB_RESET_HWWDT) ? " HWWDT" : "");
   ```
   build แล้ว flash
2. บันทึกค่าในสี่สถานการณ์: ถอดสายเสียบใหม่, กดปุ่มรีเซ็ต, หลัง `make program`, และถอดเสียบอีกครั้ง — ค่าไหนเป็น 0 บิตไหนค้างข้ามการรีเซ็ต
3. เทียบค่าที่ได้กับตารางใน `cy_syslib.h` แยกสิ่งที่เห็นจริงออกจากสิ่งที่อนุมาน
4. ออกแบบ (บนกระดาษ) การเปิด hardware watchdog: task ที่ต้อง check in อย่างน้อยสามตัว รอบที่ช้าที่สุด เวลาของ watchdog พร้อม margin

**หลักฐานที่เก็บไว้ใน portfolio:** diff ของ main.c ตารางค่าสาเหตุการรีเซ็ตทั้งสี่สถานการณ์ และแบบร่างการออกแบบ watchdog ข้อ 4

---

## ไปต่อ

- อ่านหัวข้อ Functional Description, Clearing WDT ในหัวไฟล์ของ [`cy_wdt.h`](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_wdt.h) แล้วคำนวณว่าถ้าใช้ match value แบบในเอกสาร ต้องป้อนบ่อยแค่ไหน
- เปรียบเทียบ watchdog แบบ window กับแบบธรรมดาใน [Watchdog timer (Wikipedia)](https://en.wikipedia.org/wiki/Watchdog_timer) แบบ window จับบั๊กอะไรได้เพิ่ม

บทถัดไป: [บทเรียน 4.4 — DMA](../l04-dma/README.md)

---

## แหล่งที่มาและเครดิต

"พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

โค้ดของหลักสูตรนี้ (`examples/`, `practice/`, `solution/`) Apache-2.0 · โค้ดของ SDK ไม่ได้คัดลอกเป็นไฟล์
บทเรียนยกมาเป็นช่วงสั้น ๆ พร้อมลิงก์ไปยังไฟล์ที่ commit `ef72c1b` (Apache-2.0, tesaiot-pse84-devkit-sdk)
