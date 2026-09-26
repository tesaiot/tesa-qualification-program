---
id: c-found.m03.l01
lang: th
title: {th: SWD และ GDB เบื้องต้น, en: SWD and GDB basics}
summary: {th: ต่อ debugger ผ่าน SWD ตั้ง breakpoint ดูค่า และเดินโปรแกรมทีละบรรทัด, en: 'Attach a debugger over SWD, set breakpoints, inspect values and step through code.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m02.l03]
objectives:
- {th: เริ่มการดีบักบนบอร์ดผ่าน SWD แล้วหยุดที่ breakpoint ในฟังก์ชันที่กำหนดได้, en: Start a debug session over SWD and stop at a breakpoint in a given function.}
- {th: ใช้คำสั่ง GDB ดูค่าตัวแปร ดู backtrace และเดินโปรแกรมทีละบรรทัดได้, en: 'Use GDB to print variables, show a backtrace and step line by line.'}
- {th: อธิบายว่าทำไมการหยุดที่ breakpoint อาจเปลี่ยนพฤติกรรมของระบบที่มีจังหวะเวลาหรือหลายคอร์, en: Explain why halting at a breakpoint can change the behaviour of a timing-sensitive or multi-core system.}
develops:
- {skill: debug.jtag-swd, to: 3}
- {skill: debug.gdb, to: 3}
- {skill: debug.openocd, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
slides: slides.md
---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. เริ่มการดีบักบนบอร์ดผ่าน SWD แล้วหยุดที่ breakpoint ในฟังก์ชันที่กำหนดได้
2. ใช้คำสั่ง GDB ดูค่าตัวแปร ดู backtrace และเดินโปรแกรมทีละบรรทัดได้
3. อธิบายว่าทำไมการหยุดที่ breakpoint อาจเปลี่ยนพฤติกรรมของระบบที่มีจังหวะเวลาหรือหลายคอร์

ใช้เวลาประมาณ 70 นาที (แนวคิด 15 · ฝึก 25 · แล็บ 25 · เช็ก 5) ฝึก GDB บนคอมพิวเตอร์ก่อน แล้วค่อยใช้กับบอร์ด

## ก่อนเริ่ม

ทวนจากโมดูล 1 และ 2 สองข้อ

1. แม่แบบของ SDK ตั้ง `CONFIG=Release` ไว้ใน `common.mk` ด้วยเครื่องหมาย `=` ถ้าคุณ build ด้วย `make build CONFIG=Debug` ค่าไหนชนะ (บทเรียน 2.2)
2. ถ้าลูป `for (i = 0; i <= 8; i++)` เขียนลงอาร์เรย์ขนาด 8 ไบต์ที่อยู่ใน struct ไบต์ที่เก้าจะไปตกที่ไหน (บทเรียน 1.3 เรื่อง struct และ padding)

สิ่งที่ต้องมีเพิ่ม: GDB บนคอมพิวเตอร์ (ติดตั้งแยก เช่น แพ็กเกจ `gdb` บน Linux หรือใช้ `lldb` บน macOS ซึ่งคำสั่งต่างกันเล็กน้อย)
และสำหรับบอร์ด Eclipse IDE for ModusToolbox™ ที่มากับ ModusToolbox 3.6

## ดูของจริงก่อน

เปิด [examples/05_find_the_overrun.c](examples/05_find_the_overrun.c) **ทายก่อนรัน** ว่าบรรทัด `round 0` จะพิมพ์ count เท่าไร

```sh
gcc -std=c11 -Wall -Wextra -g -O0 -o overrun examples/05_find_the_overrun.c
./overrun
```

ผลคือ `round 0: count = 16 (expected 8)` โปรแกรมบวก count ทีละ 8 แต่มีใครบางคนเขียนทับ count ก่อน
การอ่านโค้ดทีละบรรทัดหาคำตอบได้ แต่ debugger ตอบได้เร็วกว่าและพิสูจน์ได้ ด้วยคำสั่งเดียว: "หยุดทันทีที่มีใครเขียนตรงนี้"

## แนวคิด

### 1. สายโซ่จาก GDB ถึงชิป

```
GDB  <--TCP-->  OpenOCD (GDB server)  <--USB-->  KitProg3 บนบอร์ด  <--SWD-->  CPU ใน PSOC™ Edge
```

- **SWD (Serial Wire Debug)** คือพอร์ตดีบักของ Arm ใช้สายสัญญาณสองเส้น SWDIO กับ SWCLK (บวกกราวด์) ผ่านสายนี้ debugger
  หยุด CPU อ่านเขียนหน่วยความจำและรีจิสเตอร์ และตั้ง breakpoint กับ watchpoint ที่เป็นฮาร์ดแวร์ของคอร์ได้
- **KitProg3** คือ debugger ที่อยู่บนบอร์ดเอง ต่อผ่าน USB ตัวเดียวกับที่ใช้ flash และเป็นทาง UART console ด้วย
- **OpenOCD** เป็นโปรแกรมตัวกลางที่คุยกับ KitProg3 แล้วเปิดพอร์ตให้ GDB ต่อ ModusToolbox เป็นคนเรียกให้เมื่อคุณเริ่มการดีบักจาก IDE
- **GDB** คือตัวที่คุณพิมพ์คำสั่ง หรือที่ IDE ใช้อยู่เบื้องหลัง

README ของ SDK เตือนเรื่องหนึ่งไว้ชัดเจน: **อย่าเรียก openocd ตรง ๆ ด้วย `-f target/cat1d.cfg`** ทีม SDK ลองแล้วได้ `wrote 0 bytes`
ตามด้วย checksum ไม่ตรง เพราะ image อยู่ใน QSPI flash ภายนอกที่ต้องให้ ModusToolbox ตั้งค่าก่อน และเฟิร์มแวร์ที่กำลังรันเสียไปด้วย
ให้ flash ด้วย `make program` และเริ่มการดีบักผ่าน launch configuration ของ ModusToolbox

### 2. คำสั่ง GDB ที่ใช้ทุกวัน

| คำสั่ง | ทำอะไร |
|---|---|
| `break fill_samples` หรือ `break file.c:42` | หยุดเมื่อถึงฟังก์ชันหรือบรรทัดนั้น |
| `run` / `continue` (`c`) | เริ่ม / ทำงานต่อจนเจอ breakpoint ถัดไป |
| `next` (`n`) / `step` (`s`) / `finish` | ไปบรรทัดถัดไปโดยข้ามฟังก์ชัน / เข้าไปในฟังก์ชัน / ทำจนจบฟังก์ชันนี้ |
| `print x` (`p`) `print *ptr` `print arr` | ดูค่า ตามด้วย pointer ดู struct หรืออาร์เรย์ทั้งก้อน |
| `info locals` / `info args` | ดูตัวแปร local และอาร์กิวเมนต์ทั้งหมดของ frame ปัจจุบัน |
| `bt` (backtrace) | ดูว่ามาถึงตรงนี้ผ่านฟังก์ชันไหนบ้าง |
| `watch -l expr` | หยุดเมื่อมีการเขียนลงที่อยู่ของ `expr` (ใช้ hardware watchpoint ของคอร์) |
| `x/4xw addr` | ดูหน่วยความจำ 4 word เป็นเลขฐานสิบหก |

watchpoint คือเครื่องมือที่ทรงพลังที่สุดของตาราง เมื่อค่าเพี้ยนและไม่รู้ว่าใครเขียน อย่าไล่อ่านโค้ด ให้ฮาร์ดแวร์บอก
ข้อควรรู้เมื่อใช้กับบอร์ด: แม่แบบของ SDK build แบบ **Release** เป็นค่าเริ่มต้น (`common.mk` บรรทัด 20) คอมไพเลอร์จะเก็บตัวแปรไว้ในรีจิสเตอร์
ตัดตัวแปรทิ้ง หรือสลับลำดับบรรทัด GDB จึงอาจแสดง `<optimized out>` หรือกระโดดข้ามบรรทัดตอน `next` นั่นไม่ใช่ debugger เสีย
ถ้าต้องการเห็นทุกตัวแปร ให้ลอง build ด้วย `CONFIG=Debug` บน command line ซึ่งชนะ `=` ใน `common.mk` แล้วจดลงบันทึกการ build
(หลักสูตรนี้ยังไม่ได้ยืนยันบนบอร์ดว่า Debug ของแม่แบบนี้ build และบูตได้ครบ ถ้าไม่ได้ ให้ดีบักบน Release ต่อ)

### 3. การหยุด CPU ไม่ได้หยุดโลก

breakpoint หยุดแค่คอร์ที่ถูกดีบัก ทุกอย่างรอบตัวเดินต่อ ปุ่มที่กำลังถูกกด ข้อมูลที่ไหลเข้า UART เซนเซอร์ และอีกคอร์หนึ่ง
ระบบที่พึ่งจังหวะเวลาจึงทำตัวต่างไปเมื่อถูกหยุด เช่น การกดปุ่มที่เกิดขณะหยุดอาจหายไปทั้งครั้ง ไบต์ที่มาถึงระหว่างนั้นล้นบัฟเฟอร์
และถ้าเปิด watchdog ไว้ การหยุดนาน ๆ อาจทำให้บอร์ดรีเซ็ตกลางการดีบัก (บทเรียน 4.3)

บน PSOC™ Edge E84 เรื่องนี้ยิ่งชัดเพราะมีสองคอร์ทำงาน เอกสาร SDK บท G2 บันทึกว่าเมื่อ CM33 ถูกหยุด บรรทัด `[HB]` หยุดทันที
แต่ "the screen stays as it was (CM55 keeps running its last frame)" คอร์ที่ไม่ได้ถูกหยุดยังรอคำตอบทาง IPC จากคอร์ที่ถูกหยุดอยู่
และคอมเมนต์ใน [diag_blackbox.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/shared/include/diag_blackbox.h#L1-L22)
ของ SDK ระบุว่า config ของ openocd ที่ใช้ "exposes no CM55 debug target" คือในชุดเครื่องมือของแม่แบบนี้ เราดีบัก CM33 ได้ แต่หลักฐานจาก CM55
ต้องมาจากตัวนับและบันทึกที่มันเขียนไว้เอง ซึ่งเป็นเรื่องของบทเรียน 3.2

กับดักที่สำคัญที่สุดของแม่แบบ mtb-only คือ Appendix X #16 ของเอกสาร SDK: **การ attach debugger เข้ากับบอร์ดที่กำลังทำงาน
ทำให้ CM33 ไปค้างในลูปของ boot ROM** จนกว่าจะตัดไฟ คอมเมนต์ใน
[proj_cm33_ns/main.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/main.c#L292-L309)
เล่าว่ากว่าจะรู้เรื่องนี้ต้องเสียเวลาหลายชั่วโมงไปกับการโทษเฟิร์มแวร์ และบท G2 แนะนำว่าถ้าต้องใช้ debugger กับ variant นี้
ให้ "flash and halt-on-reset from a fresh programming session rather than attaching to a live board"

## ตัวอย่างสมบูรณ์

ฝึกบนคอมพิวเตอร์กับ [examples/05_find_the_overrun.c](examples/05_find_the_overrun.c) ซึ่งเขียนเป็นสามท่า

- **ท่าที่ 1** `fill_samples()` เติมค่าลงอาร์เรย์ 8 ช่อง ด้วยลูปที่มีบั๊กหนึ่งจุด
- **ท่าที่ 2** `main()` เรียกสามรอบ และบวก count ทีละ 8
- **ท่าที่ 3** พิมพ์ค่าที่ได้เทียบกับค่าที่ควรเป็น

session แบบโต้ตอบบนคอมพิวเตอร์ (พิมพ์ทีละบรรทัดหลัง `(gdb)`)

```text
$ gdb -q ./overrun
(gdb) break fill_samples
(gdb) run
(gdb) info args
(gdb) print *r
(gdb) next
(gdb) print i
(gdb) watch -l r->count
(gdb) continue
(gdb) bt
(gdb) print i
(gdb) quit
```

หลัง `continue` GDB จะหยุดที่บรรทัดในลูปของ `fill_samples` พร้อมแสดงค่าเก่าและค่าใหม่ของ `r->count`
`print i` ได้ 8 ซึ่งบอกว่าคำสั่งที่เขียนทับ count คือ `r->samples[8]` ช่องที่อยู่นอกอาร์เรย์ และ `bt` แสดงว่ามาจาก `main`
ลองแก้ `<=` เป็น `<` คอมไพล์ใหม่ แล้วรันทั้งโปรแกรมและ session นี้อีกครั้ง watchpoint ยังหยุดอยู่ไหม และหยุดที่ไหน

## ฝึกเติม

เปิด [practice/05_watch.gdb](practice/05_watch.gdb) เป็นสคริปต์ GDB ที่ทำ session ข้างบนแบบอัตโนมัติ มีช่องให้เติม 3 จุด (`____`)
ชื่อฟังก์ชันที่จะหยุด ตัวแปรที่จะเฝ้า และคำสั่งดู call stack รันด้วย

```sh
gdb -q -batch -x practice/05_watch.gdb ./overrun
```

ผลที่ต้องได้คือการหยุดด้วย watchpoint ในลูปของ `fill_samples` และ `print i` ได้ 8

## เฉลย

ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/05_watch.gdb](solution/05_watch.gdb)
จุดที่มักพลาดคือเขียน `watch r->count` โดยไม่มี `-l` ซึ่ง GDB จะเฝ้าแบบผูกกับ frame ของ `fill_samples` และลบ watchpoint ทิ้งเมื่อฟังก์ชันจบ
ส่วน `-l` คำนวณที่อยู่ครั้งเดียวแล้วเฝ้าที่อยู่นั้น ซึ่งคือสิ่งที่ต้องการเมื่อสงสัยว่า "ใครเขียนลงหน่วยความจำตรงนี้"

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) (บนเว็บไซต์อยู่ท้ายหน้านี้) ครอบคลุมเป้าหมายทั้งสามข้อ ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน

## แล็บ

**งาน:** หยุด CM33 ในตัวอย่าง GPIO ของ SDK ด้วย breakpoint แล้วดูตัวแปรของตัวกันเด้งขณะคุณกดปุ่ม

1. build แม่แบบโดยเลือกตัวอย่าง GPIO ถ้าจะลอง Debug ให้เพิ่ม `CONFIG=Debug` และจดลงบันทึกการ build
   ```sh
   make build -j ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/io/04_gpio_led_button
   ```
2. เปิดแม่แบบใน Eclipse IDE for ModusToolbox แล้วเริ่มการดีบักด้วย launch configuration แบบ **Debug (KitProg3_MiniProg4)**
   ของโปรเจกต์ CM33 non-secure จาก Quick Panel (ชื่อเต็มขึ้นกับชื่อโปรเจกต์ของคุณ) ซึ่ง program แล้วเริ่มจาก reset
   **ห้ามใช้แบบ attach กับบอร์ดที่กำลังทำงาน** (Appendix X #16)
3. ตั้ง breakpoint ที่ `example_io_gpio_led_button` แล้ว resume เมื่อหยุด พิมพ์ `bt` ใน Debugger Console หรือดูหน้าต่าง Call Stack
   จดชื่อฟังก์ชันที่เรียกเข้ามา (ควรเห็นตัวรันตัวอย่างของ SDK)
4. ใช้ `next` ข้าม `leds_init()` และ `button_init()` ทีละบรรทัด แล้วตั้ง breakpoint อีกตัวที่บรรทัด `presses++;`
   กดปุ่ม SW2 หนึ่งครั้ง เมื่อหยุด ดูค่า `stable` `cand` `agree` และ `presses`
5. ระหว่างที่ CM33 หยุดอยู่ สังเกต serial console และหน้าจอ บรรทัดไหนหยุด อะไรยังขยับ จดลงบันทึก แล้วอธิบายด้วยแนวคิดข้อ 3
6. ลบ breakpoint ทั้งหมด resume แล้วกดปุ่มอีกห้าครั้ง จำนวน `presses` ที่พิมพ์ตอนจบตรงกับที่กดไหม เทียบกับตอนที่ยังมี breakpoint อยู่

**หลักฐานที่เก็บไว้ใน portfolio:** ภาพหน้าจอ call stack ตอนหยุดในข้อ 3 ภาพหน้าต่างตัวแปรในข้อ 4 บันทึกสิ่งที่หยุดและสิ่งที่ยังขยับในข้อ 5
และผลการนับในข้อ 6 ถ้า GDB แสดง `<optimized out>` ให้จดไว้ด้วยว่าเป็นตัวแปรไหน และ build แบบไหน

## ไปต่อ

- คู่มือ [GDB](https://sourceware.org/gdb/current/onlinedocs/gdb.html/) หัวข้อ "Setting Watchpoints" อธิบายว่าเมื่อไรเป็น hardware watchpoint
  และมีได้กี่ตัวพร้อมกันขึ้นกับคอร์ ลองตั้งหลายตัวบนบอร์ดแล้วดูว่า GDB บอกอะไรเมื่อเกินจำนวน
- คู่มือ [OpenOCD](https://openocd.org/doc/html/index.html) หัวข้อ GDB and OpenOCD อธิบายว่า GDB ต่อกับ OpenOCD อย่างไร
  ใช้ประกอบความเข้าใจ แต่สำหรับบอร์ดนี้ให้เริ่มผ่าน ModusToolbox ตามคำเตือนของ SDK
- อ่านบท [G2 — The heartbeat: living without a REPL](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__g2__heartbeat.html)
  ของเอกสาร SDK ทั้งบท เรื่องจริงของเครื่องมือวัดที่ "is also the murder weapon"

บทถัดไป: [บทเรียน 3.2 วินิจฉัยความผิดพลาดจากหลักฐาน](../l02-diagnosing-faults/README.md)

## สะท้อนคิด

- บั๊กแบบไหนที่คุณคิดว่า debugger ช่วยได้น้อย และต้องใช้ตัวนับหรือ log แทน
- ถ้า breakpoint ทำให้บั๊กหายไป (มักเรียกว่า heisenbug) นั่นบอกอะไรคุณเกี่ยวกับสาเหตุของมัน

## แหล่งอ้างอิง

- [GDB documentation](https://sourceware.org/gdb/current/onlinedocs/gdb.html/)
- [OpenOCD User's Guide](https://openocd.org/doc/html/index.html)
- [SDK: แม่แบบ mtb-only README (แฟลชผ่าน KitProg)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/README.en.md)
- [SDK: README หลักของ repository (คำเตือนเรื่อง openocd)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/README.md)
- [G2 — The heartbeat: living without a REPL (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__g2__heartbeat.html)
- [Appendix X — Traps and anti-patterns (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__tut__x__traps__antipatterns.html)
- [Infineon mtb-example-psoc-edge-hello-world @ release-v2.1.0: using the code example (หัวข้อ Debugging)](https://github.com/Infineon/mtb-example-psoc-edge-hello-world/blob/release-v2.1.0/docs/using_the_code_example.md)
