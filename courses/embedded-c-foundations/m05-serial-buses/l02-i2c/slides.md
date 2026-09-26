---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 5.2 — I2C"
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

# บทเรียน 5.2 — I2C

## สแกนบัส อ่านเขียนรีจิสเตอร์ของอุปกรณ์ และใช้ lock ของบัสร่วมกับงานอื่นอย่างถูกต้อง

**โมดูล 5 — UART, I2C และ SPI กับ logic analyzer**

หลักสูตร **พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge** · ต่อจากบทเรียน 5.1

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. สแกนบัส I2C และระบุอุปกรณ์ที่พบจาก address ได้
2. อ่านและเขียนรีจิสเตอร์ของอุปกรณ์ โดยถือ lock ของบัสตลอดหนึ่งธุรกรรมและคืนทุกครั้ง
3. ถอดรหัสภาพสัญญาณ I2C ได้ครบ start, address, read/write, ACK/NACK และ stop

ใช้เวลาประมาณ 70 นาที — แล็บใช้ logic analyzer สองช่องที่รับ 3.3 V ได้

---

## ก่อนเริ่ม

ทวนจากบทก่อนหน้าสองข้อ

1. UART ไม่มีสายสัญญาณนาฬิกา ผู้รับรู้จังหวะของบิตได้อย่างไร แล้วบัสที่มีสาย clock แยก (อย่าง I2C) ต่างกันอย่างไร
2. ตัวอย่าง `06_raw_register_access.c` ที่อ่านในบทเรียน 1.1 ทำ read-modify-write ของ `PWR_CTRL` ภายในอะไร และทำไมต้องครอบทั้งขั้น

---

## ดูของจริงก่อน

เปิด [examples/12_i2c_transaction.c](examples/12_i2c_transaction.c) — จำลองบัสเซนเซอร์ของบอร์ดแล้วพิมพ์ธุรกรรมแบบที่ decoder แสดง **ทายก่อนรัน**: ไบต์แรกบนสายเมื่อจะอ่านจาก BMI270 (address `0x68`) คืออะไร

```sh
gcc -std=c11 -Wall -Wextra -o i2c_transaction examples/12_i2c_transaction.c
./i2c_transaction
```

คำตอบคือ `D0` ไม่ใช่ `68` เพราะ address 7 บิตถูกเลื่อนซ้ายหนึ่งบิตแล้วต่อด้วยบิต R/W — บรรทัด `probe` แสดงสิ่งที่การสแกนทำ ส่ง address แล้วดูว่ามีใครตอบ ACK ส่วนบรรทัด `read` แสดงว่าการอ่านรีจิสเตอร์หนึ่งครั้งประกอบด้วยการเขียนหมายเลขรีจิสเตอร์ repeated START แล้วจึงอ่าน ทั้งหมดในธุรกรรมเดียว

---

## แนวคิด (1) — หนึ่งธุรกรรมบนบัส I2C

I2C ใช้สองสาย SCL (clock ที่ master ขับ) และ SDA (ข้อมูล) ทั้งสองเป็น open-drain มีตัวต้านทานดึงขึ้น อุปกรณ์หลายตัวต่อร่วมสายเดียวกันแยกกันด้วย address

| เหตุการณ์ | บนสาย | ความหมาย |
|---|---|---|
| START | SDA ลงขณะ SCL สูง | เริ่มธุรกรรม |
| address + R/W | 8 บิต MSB ก่อน | เรียกอุปกรณ์หนึ่งตัว (0 เขียน 1 อ่าน) |
| ACK / NACK | บิตที่เก้า | ดึงลง = ACK, ปล่อยสูง = NACK |
| ข้อมูล | 8 บิต MSB ก่อน + ACK/NACK ทุกไบต์ | ทีละไบต์ |
| repeated START | START ใหม่โดยไม่ STOP ก่อน | เปลี่ยนเขียนเป็นอ่านโดยไม่ปล่อยบัส |
| STOP | SDA ขึ้นขณะ SCL สูง | จบธุรกรรม |

> `sensor_i2c_read_reg()` เขียนหมายเลขรีจิสเตอร์ "with NO stop" แล้วตามด้วย repeated START กับการอ่าน — "is what the parts expect and what you would get wrong writing it yourself"

---

## แนวคิด (2) — สแกนแล้วพิสูจน์สายก่อนเชื่อไดรเวอร์

การสแกนคือ probe ทุก address ในช่วง 0x08-0x77 แล้วจดตัวที่ตอบ ACK บัสเซนเซอร์คือ SCB0 ที่ P8.0/P8.1 ทำงานที่ 1.8 V และ 400 kHz

| address | อุปกรณ์ |
|---|---|
| 0x08 | CapSense PSoC 4000T |
| 0x18 | TLV320DAC3100 audio codec |
| 0x44 | SHT40 ความชื้น/อุณหภูมิ |
| 0x68 | BMI270 IMU |
| 0x77 | DPS368 ความดัน/อุณหภูมิ |

BMM350 (0x15) อยู่บน I3C คนละตัว **"and never appears here"** และ address ที่ไม่อยู่ในตาราง **"is not an error — it is a board you have added something to"**

> **"PROVE THE WIRE FIRST"** — อ่านรีจิสเตอร์ 0x00 ก่อน ได้ `0x24` คือ BMI270 จริง ได้ `0xFF` หรืออ่านไม่ได้คือบัสหรือชิปมีปัญหา ได้ค่าอื่นคือชิปคนละตัวที่ address เดียวกัน

---

## แนวคิด (3) — lock ของบัส: หนึ่งธุรกรรมหนึ่ง lock

SCB0 มีหลายเจ้าของ — PAL ของ OPTIGA Trust M ก็เป็น master บน SCB0 ด้วย และ task เบื้องหลังอ่านเซนเซอร์ทุก 100 ms ฟังก์ชันของ SDK **ไม่ถือ lock ให้** ผู้เรียกต้องครอบเองด้วย `sensor_i2c_lock()`/`unlock()`

```c
/* Step 2 — take the bus. Never scan without this. */
if (!sensor_i2c_lock(SCAN_LOCK_TIMEOUT_MS)) {
    printf("  sensor_i2c_lock(%u ms) TIMED OUT — someone holds the bus\r\n",
           (unsigned)SCAN_LOCK_TIMEOUT_MS);
    return SDK_EX_BUSY;
}
```

- **lock มี timeout เสมอ** เมื่อหมดเวลาให้คืนผลว่า busy ไม่ใช่สรุปว่าบัสเสีย
- **หนึ่ง lock ต่อหนึ่งชุดข้อมูล ไม่ใช่ต่อหนึ่งรีจิสเตอร์** — อ่านความเร่ง gyro อุณหภูมิภายใน lock เดียว เพื่อให้มาจากจังหวะเดียวกัน
- **คืน lock ทุกทางออก** — "There is no path out of here that skips this."

---

## ตัวอย่างสมบูรณ์ — สามท่าใน 12_i2c_transaction.c

**ท่าที่ 1** `address_byte()` เลื่อน address 7 บิตแล้วใส่บิต R/W
**ท่าที่ 2** `probe()` จำลองการสแกนสี่ address รอบ 0x68 ตัวที่มีอุปกรณ์ตอบ ACK ที่เหลือ NACK
**ท่าที่ 3** `read_register()` พิมพ์การอ่าน chip id หนึ่งไบต์ และการอ่านความเร่งหกไบต์ในธุรกรรมเดียว (burst read)

```c
static uint8_t address_byte(uint8_t addr7, int read) {
    return (uint8_t)((addr7 << 1) | (read ? 1u : 0u));
}
// 0x68 << 1 | 1 (read) = 0xD1 ; 0x68 << 1 | 0 (write) = 0xD0
```

ลองแก้แล้วทายก่อนรัน: ถ้าแยกการอ่านหกไบต์เป็นหกธุรกรรม จำนวนไบต์บนสายเพิ่มเป็นเท่าไร และทำไมตัวอย่างบอกว่าแบบ burst "both faster and ATOMIC"

---

## ฝึกเติม

เปิด [practice/12_i2c_trace.c](practice/12_i2c_trace.c) — มีช่องให้เติม 4 จุด

1. `addr_byte()` ประกอบไบต์ address
2. `parse_addr_byte()` แยกกลับ และปฏิเสธ address ที่อยู่นอกช่วง 0x08-0x77
3. `encode_read_reg()` สร้างลำดับเหตุการณ์ของการอ่านรีจิสเตอร์ รวม NACK ที่ไบต์สุดท้าย
4. `scan()` สแกนแบบเดียวกับ `sensor_i2c_scan()` และตัดผลเมื่อที่เก็บเต็ม

```sh
gcc -std=c11 -Wall -Wextra -o i2c_trace practice/12_i2c_trace.c && ./i2c_trace
```

ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/12_i2c_trace.c](solution/12_i2c_trace.c) — เฉลยอธิบายสองจุดที่มักถูกข้าม: ทำไมไม่มี STOP ระหว่างเลือกรีจิสเตอร์กับการอ่าน และทำไม master ต้องตอบ NACK ที่ไบต์สุดท้าย

---

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) ครอบคลุมเป้าหมายทั้งสามข้อ (ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน)

1. สแกนบัสเซนเซอร์แล้วพบ 0x44, 0x68, 0x77 แต่ไม่พบ 0x15 ข้อใดสรุปได้ถูกต้อง
2. พบอุปกรณ์ตอบ ACK ที่ 0x68 ขั้นต่อไปที่ดีที่สุดก่อนเรียก `bmi270_init()` คืออะไร
3. ต้องอ่าน accelerometer, gyro และอุณหภูมิของ BMI270 เป็นชุดเดียวกัน วิธีถือ lock ใดถูกต้อง
4. เรียงขั้นของการสแกนบัสอย่างปลอดภัยตามตัวอย่าง `01_i2c_bus_scan`
5. decoder แสดงลำดับ S, D1, ACK, 24, NACK, P ข้อใดอธิบายถูก

---

## แล็บ

**งาน:** สแกนบัสเซนเซอร์ของบอร์ดด้วยตัวอย่างของ SDK แล้วจับธุรกรรม I2C จริงบนบัส 3.3 V ของ header ด้วย logic analyzer

**ส่วนที่ 1 สแกนด้วย SDK**

1. build ด้วย `SDK_EXAMPLE_CM33=cm33/sensors/01_i2c_bus_scan` flash ถอดสายเสียบใหม่
2. จด address ทุกตัวที่ตอบและชื่อที่พิมพ์ เทียบกับตารางในแนวคิดข้อ 2
3. build ด้วย `SDK_EXAMPLE_CM33=cm33/sensors/02_read_imu` จดบรรทัด chip id

**ส่วนที่ 2 จับสัญญาณ** (บัสเซนเซอร์ 1.8 V ไม่ออกมาที่ header จึงใช้บัส I2C 3.3 V ของ header แทน)

4. flash [Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) ต่อ logic analyzer ที่ SCL/SDA ตั้ง decoder เป็น I2C
5. จับขณะกด **Scan** หาหนึ่ง address ที่ได้ NACK และหนึ่งที่ได้ ACK ถอดรหัสด้วยตาทีละบิต
6. วัดความถี่ของ SCL จากรูปคลื่น

**หลักฐานที่เก็บไว้ใน portfolio:** log ของการสแกนและ chip id ภาพรูปคลื่น ACK/NACK ที่ขีดป้ายด้วยมือ และความถี่ SCL ที่วัดได้

---

## ไปต่อ

- อ่านบท [J1 — The sensor bus and its lock](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__j1__sensor__bus.html) — ทำไม `sensor_i2c_init()` เรียกการกู้บัสก่อนตั้งขา
- อ่าน [Understanding the I2C Bus (TI SLVA704)](https://www.ti.com/lit/an/slva704/slva704.pdf) เรื่อง pull-up และ clock stretching แล้วโยงกับ Appendix X #13 ที่เล่าว่าอุปกรณ์ที่ยืด clock ค้างทำให้ task อื่นอดอาหาร

บทถัดไป: [บทเรียน 5.3 — SPI](../l03-spi/README.md)

---

## แหล่งที่มาและเครดิต

"พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

โค้ดของหลักสูตรนี้ (`examples/`, `practice/`, `solution/`) Apache-2.0 · โค้ดของ SDK ไม่ได้คัดลอกเป็นไฟล์
บทเรียนยกมาเป็นช่วงสั้น ๆ พร้อมลิงก์ไปยังไฟล์ที่ commit `ef72c1b` (Apache-2.0, tesaiot-pse84-devkit-sdk)
