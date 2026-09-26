---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 5.3 — SPI"
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

# บทเรียน 5.3 — SPI

## เข้าใจโหมดของ SPI และสาย chip select แล้วยืนยันสัญญาณด้วย logic analyzer

**โมดูล 5 — UART, I2C และ SPI กับ logic analyzer**

หลักสูตร **พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge** · ต่อจากบทเรียน 5.2

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. อธิบายโหมด SPI ทั้งสี่จาก CPOL และ CPHA และเลือกโหมดให้ตรงกับ datasheet ของอุปกรณ์ได้
2. ถอดรหัสภาพสัญญาณ SPI ได้ครบ SCLK, MOSI, MISO และ CS
3. เปรียบเทียบ SPI กับ I2C ในด้านจำนวนสาย ความเร็ว และการต่ออุปกรณ์หลายตัว

ใช้เวลาประมาณ 70 นาที — แล็บใช้ logic analyzer สี่ช่องที่รับ 3.3 V ได้

---

## ก่อนเริ่ม

ทวนจากสองบทก่อนสองข้อ

1. UART ส่งบิตไหนก่อน และ I2C ส่งบิตไหนก่อน
2. ใน I2C master เลือกอุปกรณ์ที่จะคุยด้วยอย่างไร ถ้าไม่มี address จะเลือกด้วยอะไรได้อีก

---

## ดูของจริงก่อน

เปิด [examples/13_spi_modes.c](examples/13_spi_modes.c) — วาดไบต์ `0xA5` ในโหมด SPI ทั้งสี่ ทำเครื่องหมาย `^` ใต้ขอบที่ผู้รับอ่านค่า **ทายก่อนรัน**: ในโหมด 3 ผู้รับอ่านที่ขอบขาขึ้นหรือขาลงของ SCLK

```sh
gcc -std=c11 -Wall -Wextra -o spi_modes examples/13_spi_modes.c
./spi_modes
```

โหมด 3 อ่านที่ขอบขาขึ้น เหมือนโหมด 0 ทั้งที่ SCLK ว่างอยู่คนละระดับ ส่วนโหมด 1 และ 2 อ่านที่ขอบขาลง — บรรทัดสุดท้ายเทียบ SPI สองตัวบนบอร์ดเดียวกัน: SPI ของเรดาร์ที่ 25 MHz กับ SPI แบบ bit-bang บน header ที่ราว 67 kHz ช้ากว่ากันหลายร้อยเท่า

---

## แนวคิด (1) — สี่สาย และโหมดสี่แบบ

SPI มีสัญญาณสี่เส้น: SCLK (clock จาก master), MOSI (master ส่งออก), MISO (slave ส่งกลับ) และ CS (เลือก slave) ทุกจังหวะของ SCLK master ส่งหนึ่งบิตและรับหนึ่งบิตพร้อมกัน

| โหมด | CPOL | CPHA | ผู้รับอ่านที่ |
|---|---|---|---|
| 0 | 0 (ต่ำ) | 0 | ขอบแรก = ขาขึ้น |
| 1 | 0 (ต่ำ) | 1 | ขอบที่สอง = ขาลง |
| 2 | 1 (สูง) | 0 | ขอบแรก = ขาลง |
| 3 | 1 (สูง) | 1 | ขอบที่สอง = ขาขึ้น |

การเลือกโหมดไม่ใช่การเดา — datasheet บอกด้วยชื่อโหมด ค่า CPOL/CPHA หรือแผนภาพเวลา ถ้าให้แค่แผนภาพ ดูสองอย่าง: SCLK ว่างที่ระดับไหน (CPOL) และข้อมูลนิ่งตรงขอบแรกหรือขอบสอง (CPHA)

SPI เรดาร์ใน BSP: `sclkMode = CY_SCB_SPI_CPHA0_CPOL0` (โหมด 0), `enableMsbFirst = true`, ข้อมูล 8 บิต, CS active low

---

## แนวคิด (2) — SPI ของจริงบนบอร์ด: ฮาร์ดแวร์กับ bit-bang

**SPI ของเรดาร์ BGT60TR13C** ใช้ SCB3 ที่ 25 Mbps ผูก ISR ด้วย `Cy_SysInt_Init()` การรับส่งใช้ `Cy_SCB_SPI_Transfer()` แบบ interrupt

ไดรเวอร์เรดาร์เคยรอให้การส่งเสร็จด้วยลูป `while` ที่ไม่มีขอบเขต — ถ้า interrupt ของ SPI หายไปหนึ่งครั้ง ลูปวนตลอดไป ทีม SDK วัดบนบอร์ดจริงพบว่าค่าบนหน้า Radar ค้างทุกครั้งหลังทำงานราวแปดวินาที จึงเปลี่ยนเป็นการรอแบบมีขอบเขตที่ยกเลิกการส่งแล้วคืน error

> **"A bounded spin turns an unrecoverable wedge into an error return."**

**SPI บน header** ในตัวอย่าง Header I/O Test เป็น bit-bang โหมด 0 ที่ CPU ตั้งขาเองทีละบิตด้วย `Cy_GPIO_Write()` ช้ากว่าฮาร์ดแวร์มาก แต่ดูง่ายด้วย logic analyzer และพอสำหรับงานทดสอบ 8 ไบต์

---

## แนวคิด (3) — SPI กับ I2C

| ด้าน | SPI | I2C |
|---|---|---|
| จำนวนสาย | 3 สายร่วม + CS หนึ่งเส้นต่อ slave | 2 สายร่วมทุกอุปกรณ์ |
| เลือกอุปกรณ์ | ด้วยสาย CS | ด้วย address 7 บิตในข้อมูล |
| ความเร็วบนบอร์ดนี้ | SPI เรดาร์ 25 MHz | บัสเซนเซอร์ 400 kHz |
| ทิศทาง | full-duplex | half-duplex |
| ผู้รับยืนยัน | ไม่มี (ไม่มี ACK) | มี ACK/NACK ทุกไบต์ |
| ลักษณะสาย | push-pull ขอบคม ขับได้เร็ว | open-drain + pull-up จำกัดด้วยความจุสาย |

> SPI เหมาะกับข้อมูลปริมาณมากจากอุปกรณ์ไม่กี่ตัว (เรดาร์ จอภาพ แฟลช) ส่วน I2C เหมาะกับเซนเซอร์หลายตัวที่ส่งข้อมูลน้อย ประหยัดขาของชิป — เพราะ SPI ไม่มี ACK การพิสูจน์ว่าสายดีต้องอ่านค่าที่รู้คำตอบ เช่นรีจิสเตอร์ ID

---

## ตัวอย่างสมบูรณ์ — สามท่าใน 13_spi_modes.c

**ท่าที่ 1** สร้างรูปคลื่นหนึ่งไบต์ MSB ก่อน ตาม CPOL และ CPHA ของแต่ละโหมด
**ท่าที่ 2** วาด SCLK และ MOSI เป็นเส้น พร้อมระดับว่างก่อนและหลังเฟรม และ `^` ใต้ขอบที่อ่าน
**ท่าที่ 3** เทียบความเร็วของ SPI ฮาร์ดแวร์ของเรดาร์กับ bit-bang ของ header

```c
// โหมด 0: CPOL=0 (ว่างต่ำ), CPHA=0 (อ่านที่ขอบแรก = ขาขึ้น)
for (int i = 7; i >= 0; i--) {       // MSB ก่อน
    int bit = (byte >> i) & 1u;
    /* วาง MOSI ให้นิ่งก่อนขอบขาขึ้น แล้วอ่านที่ขอบนั้น */
}
```

ลองแก้แล้วทายก่อนรัน: ถ้า master ใช้โหมด 0 แต่ slave ใช้โหมด 1 slave จะอ่านบิตที่ขอบไหน และข้อมูลที่ได้น่าจะเพี้ยนอย่างไร

---

## ฝึกเติม

เปิด [practice/13_spi_decode.c](practice/13_spi_decode.c) — ตัวถอดรหัส SPI สี่สาย บทสุดท้ายของโมดูล 5 จึงเว้นว่างมากที่สุด 6 จุด

1. แยก CPOL กับ CPHA จากเลขโหมด
2. ล้างสถานะเมื่อ CS ไม่ทำงาน
3. แยกขอบ leading กับ trailing
4. เลือกขอบที่ต้องอ่านตาม CPHA
5. เลื่อนบิตเข้าไบต์ MSB ก่อน จากค่าที่นิ่งอยู่ก่อนขอบ
6. เก็บไบต์เมื่อครบ 8 บิตโดยไม่เขียนเลยที่เก็บ

```sh
gcc -std=c11 -Wall -Wextra -o spi_decode practice/13_spi_decode.c && ./spi_decode
```

test ใช้เฟรมจริงที่ Header I/O Test ส่ง `A5 31 00 5A 01 02 03` ตามด้วย XOR checksum `CE` และมีกรณีตั้งโหมดผิด ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/13_spi_decode.c](solution/13_spi_decode.c)

---

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) ครอบคลุมเป้าหมายทั้งสามข้อ (ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน)

1. datasheet บอกว่า SCLK ว่างที่ระดับสูง และอ่านข้อมูลที่ขอบขาขึ้น (ขอบที่สองหลังออกจากระดับว่าง) ต้องตั้งโหมดใด
2. SPI เรดาร์ในค่าตั้งของ BSP ใช้ `sclkMode = CY_SCB_SPI_CPHA0_CPOL0` และ `enableMsbFirst = true` ข้อใดถูก
3. จับสัญญาณ SPI โหมด 0 ได้ CS ต่ำ แล้ว MOSI ที่ขอบขาขึ้นแปดครั้งติดกันเป็น `0 0 1 1 0 0 0 1` ไบต์ที่ master ส่งคืออะไร
4. decoder SPI ให้ไบต์ที่ดูเลื่อนไปหนึ่งบิตทุกไบต์ สาเหตุใดเป็นไปได้ (เลือกได้หลายข้อ)
5. ข้อใดเปรียบเทียบ SPI กับ I2C ได้ถูกต้อง (เลือกได้หลายข้อ)

---

## แล็บ

**งาน:** จับธุรกรรม SPI จริงบน header ถอดรหัสด้วยตาและด้วย decoder แล้วพิสูจน์ผลของการตั้งโหมดผิด

1. flash [Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) จาก Developer Hub
2. ต่อ logic analyzer สี่ช่องที่ P9.3 (SCK), P9.2 (MOSI), P9.1 (MISO), P9.0 (CS) และกราวด์
3. ตั้ง trigger ที่ขอบขาลงของ CS แล้วกด **SPI ESP32** จอจะพิมพ์ `TX req:` แปดไบต์
4. ถอดรหัสไบต์แรกด้วยตา: SCLK ว่างที่ระดับไหน MOSI นิ่งตอนขอบไหน อ่าน 8 บิต MSB ก่อน ต้องได้ `A5`
5. ตั้ง decoder SPI เป็นโหมด 0, MSB first, CS active low เทียบกับ `TX req:` แล้วเปลี่ยน decoder เป็นโหมด 1 ดูว่าไบต์เปลี่ยนเป็นอะไร
6. วัดความยาวของหนึ่งบิตและความยาวที่ CS อยู่ระดับต่ำ เทียบกับการประมาณราว 15 µs/บิต

**หลักฐานที่เก็บไว้ใน portfolio:** ภาพรูปคลื่นสี่ช่องที่ขีดป้ายไบต์แรกด้วยมือ ภาพผลของ decoder โหมด 0 และโหมด 1 และตัวเลขเวลาที่วัดได้

---

## ไปต่อ

- อ่านหัวไฟล์ของ [`cy_scb_spi.h` @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_scb_spi.h) หัวข้อ Configure Data Rate แล้วคำนวณตัวหารและ oversample สำหรับ SPI 10 MHz จาก 100 MHz
- เปิด [sigrok protocol decoders](https://sigrok.org/wiki/Protocol_decoders) ดูว่า decoder ของ SPI ต่อเป็นชั้นกับ decoder ของอุปกรณ์ได้อย่างไร

บทถัดไปเข้าสู่โมดูล 6: [บทเรียน 6.1 — Unit test บนเครื่องโฮสต์](../../m06-test-and-ci/l01-unit-tests-on-host/README.md)

---

## แหล่งที่มาและเครดิต

"พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

โค้ดของหลักสูตรนี้ (`examples/`, `practice/`, `solution/`) Apache-2.0 · โค้ดของ SDK ไม่ได้คัดลอกเป็นไฟล์
บทเรียนยกมาเป็นช่วงสั้น ๆ พร้อมลิงก์ไปยังไฟล์ที่ commit `ef72c1b` (Apache-2.0, tesaiot-pse84-devkit-sdk)
