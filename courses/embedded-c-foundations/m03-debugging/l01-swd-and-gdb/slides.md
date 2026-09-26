---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 3.1 — SWD และ GDB เบื้องต้น"
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

# บทเรียน 3.1 — SWD และ GDB เบื้องต้น

## ต่อ debugger ผ่าน SWD ตั้ง breakpoint ดูค่า และเดินโปรแกรมทีละบรรทัด

**โมดูล 3 — ดีบักด้วย SWD และ GDB**

หลักสูตร **พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. เริ่มการดีบักบนบอร์ดผ่าน SWD แล้วหยุดที่ breakpoint ในฟังก์ชันที่กำหนดได้
2. ใช้คำสั่ง GDB ดูค่าตัวแปร ดู backtrace และเดินโปรแกรมทีละบรรทัดได้
3. อธิบายว่าทำไมการหยุดที่ breakpoint อาจเปลี่ยนพฤติกรรมของระบบที่มีจังหวะเวลาหรือหลายคอร์

ใช้เวลาประมาณ 70 นาที — ฝึก GDB บนคอมพิวเตอร์ก่อน แล้วค่อยใช้กับบอร์ด

---

## ก่อนเริ่ม

ทวนจากโมดูล 1 และ 2 สองข้อ

1. แม่แบบของ SDK ตั้ง `CONFIG=Release` ไว้ใน `common.mk` ด้วยเครื่องหมาย `=` ถ้าคุณ build ด้วย `make build CONFIG=Debug` ค่าไหนชนะ
2. ถ้าลูป `for (i = 0; i <= 8; i++)` เขียนลงอาร์เรย์ขนาด 8 ไบต์ที่อยู่ใน struct ไบต์ที่เก้าจะไปตกที่ไหน

**สิ่งที่ต้องมีเพิ่ม:** GDB บนคอมพิวเตอร์ (หรือ `lldb` บน macOS) และสำหรับบอร์ด Eclipse IDE for ModusToolbox™

---

## ดูของจริงก่อน

เปิด [examples/05_find_the_overrun.c](examples/05_find_the_overrun.c) **ทายก่อนรัน**: บรรทัด `round 0` จะพิมพ์ count เท่าไร

```sh
gcc -std=c11 -Wall -Wextra -g -O0 -o overrun examples/05_find_the_overrun.c
./overrun
```

ผลคือ `round 0: count = 16 (expected 8)` — โปรแกรมบวก count ทีละ 8 แต่มีใครบางคนเขียนทับ count ก่อน

การอ่านโค้ดทีละบรรทัดหาคำตอบได้ แต่ debugger ตอบได้เร็วกว่าและพิสูจน์ได้ ด้วยคำสั่งเดียว: **"หยุดทันทีที่มีใครเขียนตรงนี้"**

---

## แนวคิด (1) — สายโซ่จาก GDB ถึงชิป

```text
GDB  <--TCP-->  OpenOCD (GDB server)  <--USB-->  KitProg3 บนบอร์ด  <--SWD-->  CPU ใน PSOC™ Edge
```

- **SWD** พอร์ตดีบักของ Arm ใช้สายสัญญาณสองเส้น SWDIO กับ SWCLK (บวกกราวด์) — หยุด CPU อ่านเขียนหน่วยความจำและตั้ง breakpoint/watchpoint ที่เป็นฮาร์ดแวร์ได้
- **KitProg3** debugger บนบอร์ดเอง ต่อผ่าน USB ตัวเดียวกับที่ใช้ flash และเป็นทาง UART console ด้วย
- **OpenOCD** ตัวกลางที่คุยกับ KitProg3 แล้วเปิดพอร์ตให้ GDB ต่อ
- **GDB** ตัวที่คุณพิมพ์คำสั่ง หรือที่ IDE ใช้อยู่เบื้องหลัง

> **อย่าเรียก openocd ตรง ๆ ด้วย `-f target/cat1d.cfg`** — ทีม SDK ลองแล้วได้ `wrote 0 bytes` และเฟิร์มแวร์ที่กำลังรันเสียไปด้วย ใช้ `make program` และเริ่มดีบักผ่าน launch configuration ของ ModusToolbox

---

## แนวคิด (2) — คำสั่ง GDB ที่ใช้ทุกวัน

| คำสั่ง | ทำอะไร |
|---|---|
| `break fill_samples` / `break file.c:42` | หยุดเมื่อถึงฟังก์ชันหรือบรรทัดนั้น |
| `run` / `continue` (`c`) | เริ่ม / ทำงานต่อจนเจอ breakpoint ถัดไป |
| `next` (`n`) / `step` (`s`) / `finish` | ข้ามฟังก์ชัน / เข้าไปในฟังก์ชัน / ทำจนจบฟังก์ชันนี้ |
| `print x` (`p`) / `print *ptr` | ดูค่า ตามด้วย pointer ดู struct/อาร์เรย์ |
| `info locals` / `info args` | ดูตัวแปร local และอาร์กิวเมนต์ของ frame ปัจจุบัน |
| `bt` (backtrace) | ดูว่ามาถึงตรงนี้ผ่านฟังก์ชันไหนบ้าง |
| `watch -l expr` | หยุดเมื่อมีการเขียนลงที่อยู่ของ `expr` |

**watchpoint คือเครื่องมือที่ทรงพลังที่สุด** — เมื่อค่าเพี้ยนและไม่รู้ว่าใครเขียน อย่าไล่อ่านโค้ด ให้ฮาร์ดแวร์บอก

---

## แนวคิด (2) ต่อ — Release ซ่อนตัวแปรจาก GDB

แม่แบบของ SDK build แบบ **Release** เป็นค่าเริ่มต้น คอมไพเลอร์จะเก็บตัวแปรไว้ในรีจิสเตอร์ ตัดตัวแปรทิ้ง หรือสลับลำดับบรรทัด GDB จึงอาจแสดง `<optimized out>` หรือกระโดดข้ามบรรทัดตอน `next` — **นั่นไม่ใช่ debugger เสีย**

ถ้าต้องการเห็นทุกตัวแปร ให้ลอง build ด้วย `CONFIG=Debug` บน command line ซึ่งชนะ `=` ใน `common.mk` แล้วจดลงบันทึกการ build

> หลักสูตรนี้ยังไม่ได้ยืนยันบนบอร์ดว่า Debug ของแม่แบบนี้ build และบูตได้ครบ ถ้าไม่ได้ ให้ดีบักบน Release ต่อ

---

## แนวคิด (3) — การหยุด CPU ไม่ได้หยุดโลก

breakpoint หยุดแค่คอร์ที่ถูกดีบัก ทุกอย่างรอบตัวเดินต่อ — ปุ่มที่กำลังถูกกดอาจหายไปทั้งครั้ง ไบต์ที่มาถึงระหว่างนั้นล้นบัฟเฟอร์ และถ้าเปิด watchdog ไว้ การหยุดนาน ๆ อาจทำให้บอร์ดรีเซ็ตกลางการดีบัก

บน PSOC™ Edge E84 มีสองคอร์: เมื่อ CM33 ถูกหยุด บรรทัด `[HB]` หยุดทันที แต่ **"the screen stays as it was (CM55 keeps running its last frame)"** — config ของ openocd ที่ใช้ **"exposes no CM55 debug target"**

> กับดักสำคัญที่สุด (Appendix X #16): **การ attach debugger เข้ากับบอร์ดที่กำลังทำงานทำให้ CM33 ไปค้างในลูปของ boot ROM** จนกว่าจะตัดไฟ — ให้ "flash and halt-on-reset from a fresh programming session" แทนการ attach

---

## ตัวอย่างสมบูรณ์ — session GDB บนคอมพิวเตอร์

[examples/05_find_the_overrun.c](examples/05_find_the_overrun.c): ท่าที่ 1 `fill_samples()` เติมอาร์เรย์ 8 ช่องด้วยลูปที่มีบั๊ก · ท่าที่ 2 `main()` เรียกสามรอบ · ท่าที่ 3 พิมพ์ค่าที่ได้เทียบกับที่ควรเป็น

```text
$ gdb -q ./overrun
(gdb) break fill_samples
(gdb) run
(gdb) print *r
(gdb) watch -l r->count
(gdb) continue
(gdb) bt
(gdb) print i
```

หลัง `continue` GDB หยุดที่บรรทัดในลูปที่เขียนทับ `r->count` — `print i` ได้ 8 บอกว่าคำสั่งที่เขียนทับคือ `r->samples[8]` ช่องที่อยู่นอกอาร์เรย์ และ `bt` แสดงว่ามาจาก `main`

---

## ฝึกเติม

เปิด [practice/05_watch.gdb](practice/05_watch.gdb) — สคริปต์ GDB ที่ทำ session ข้างบนแบบอัตโนมัติ มีช่องให้เติม 3 จุด (`____`): ชื่อฟังก์ชันที่จะหยุด ตัวแปรที่จะเฝ้า และคำสั่งดู call stack

```sh
gdb -q -batch -x practice/05_watch.gdb ./overrun
```

ผลที่ต้องได้คือการหยุดด้วย watchpoint ในลูปของ `fill_samples` และ `print i` ได้ 8

ลองเองก่อนอย่างน้อย 15 นาที แล้วค่อยเปิด [solution/05_watch.gdb](solution/05_watch.gdb) — จุดที่มักพลาด: เขียน `watch r->count` โดยไม่มี `-l` ซึ่ง GDB จะลบ watchpoint ทิ้งเมื่อฟังก์ชันจบ ส่วน `-l` เฝ้าที่อยู่นั้นตลอดไป

---

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) ครอบคลุมเป้าหมายทั้งสามข้อ (ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน)

1. บอร์ดรันเฟิร์มแวร์ mtb-only อยู่ และคุณต้องการหยุดที่ฟังก์ชันหนึ่ง วิธีใดตรงกับคำแนะนำของเอกสาร SDK
2. เรียงสายโซ่การดีบักจากเครื่องของคุณไปจนถึง CPU
3. ค่าของ `rec.count` เพี้ยนโดยไม่รู้ว่าใครเขียน คำสั่ง GDB ใดตอบคำถามนี้ได้ตรงที่สุด
4. หยุดอยู่ในฟังก์ชันหนึ่งบนบอร์ดที่ build แบบ Release แล้ว GDB แสดง `<optimized out>` ข้อใดถูก (เลือกได้หลายข้อ)
5. ขณะที่ CM33 หยุดที่ breakpoint อยู่ ข้อใดน่าจะเกิดขึ้น (เลือกได้หลายข้อ)

---

## แล็บ

**งาน:** หยุด CM33 ในตัวอย่าง GPIO ของ SDK ด้วย breakpoint แล้วดูตัวแปรของตัวกันเด้งขณะกดปุ่ม

1. build แม่แบบเลือกตัวอย่าง GPIO (`SDK_EXAMPLE_CM33=cm33/io/04_gpio_led_button`) ถ้าจะลอง Debug ให้เพิ่ม `CONFIG=Debug` และจดบันทึก
2. เปิดใน Eclipse IDE for ModusToolbox เริ่มดีบักด้วย **Debug (KitProg3_MiniProg4)** — **ห้ามใช้แบบ attach กับบอร์ดที่กำลังทำงาน**
3. ตั้ง breakpoint ที่ `example_io_gpio_led_button` resume แล้ว `bt` จดชื่อฟังก์ชันที่เรียกเข้ามา
4. `next` ข้าม `leds_init()`/`button_init()` แล้วตั้ง breakpoint ที่ `presses++;` กด SW2 หนึ่งครั้ง ดูค่า `stable` `cand` `agree` `presses`
5. ระหว่างที่ CM33 หยุดอยู่ สังเกต serial console และหน้าจอ บรรทัดไหนหยุด อะไรยังขยับ อธิบายด้วยแนวคิดข้อ 3
6. ลบ breakpoint ทั้งหมด resume แล้วกดอีกห้าครั้ง จำนวน `presses` ตรงกับที่กดไหม เทียบกับตอนมี breakpoint

**หลักฐานที่เก็บไว้ใน portfolio:** ภาพ call stack ข้อ 3, ภาพหน้าต่างตัวแปรข้อ 4, บันทึกข้อ 5, ผลการนับข้อ 6

---

## ไปต่อ

- คู่มือ [GDB](https://sourceware.org/gdb/current/onlinedocs/gdb.html/) หัวข้อ "Setting Watchpoints" — ลองตั้งหลายตัวบนบอร์ดแล้วดูว่า GDB บอกอะไรเมื่อเกินจำนวน hardware watchpoint
- อ่านบท [G2 — The heartbeat: living without a REPL](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__g2__heartbeat.html) ทั้งบท เรื่องจริงของเครื่องมือวัดที่ "is also the murder weapon"

บทถัดไป: [บทเรียน 3.2 — วินิจฉัยความผิดพลาดจากหลักฐาน](../l02-diagnosing-faults/README.md)

---

## แหล่งที่มาและเครดิต

"พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

โค้ดของหลักสูตรนี้ (`examples/`, `practice/`, `solution/`) Apache-2.0 · โค้ดของ SDK ไม่ได้คัดลอกเป็นไฟล์
บทเรียนยกมาเป็นช่วงสั้น ๆ พร้อมลิงก์ไปยังไฟล์ที่ commit `ef72c1b` (Apache-2.0, tesaiot-pse84-devkit-sdk)
