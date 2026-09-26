---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 5.1 — UART"
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

# บทเรียน 5.1 — UART

## เข้าใจเฟรมของ UART และกติกาเจ้าของพอร์ตเดียว แล้วยืนยันด้วย logic analyzer

**โมดูล 5 — UART, I2C และ SPI กับ logic analyzer**

หลักสูตร **พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ถอดรหัสเฟรม UART หนึ่งเฟรมจากภาพสัญญาณได้ครบ start bit, data, parity และ stop bit
2. อธิบายว่าทำไม UART หนึ่งพอร์ตควรมีเจ้าของเพียงงานเดียว และส่งต่อข้อมูลผ่านบัฟเฟอร์
3. ตั้งค่า logic analyzer ให้ถอดรหัส UART ที่ baud rate ที่กำหนดได้

ใช้เวลาประมาณ 70 นาที — แล็บต้องมี logic analyzer ที่รับสัญญาณ 3.3 V และโปรแกรม [PulseView](https://sigrok.org/wiki/PulseView) หรือเทียบเท่า

---

## ก่อนเริ่ม

ทวนจากบทก่อนหน้าสองข้อ

1. debug UART ของบอร์ดนี้ใช้สัญญาณนาฬิกา 100 MHz ตัวหาร 86 และ oversample 10 ได้ baud จริงเท่าไร และคลาดจาก 115200 กี่เปอร์เซ็นต์
2. ring buffer ในบทเรียน 1.3 ให้ผู้เขียนแก้อะไร และผู้อ่านแก้อะไร

---

## ดูของจริงก่อน

เปิด [examples/11_uart_frame.c](examples/11_uart_frame.c) — วาดรูปคลื่นของหนึ่งไบต์บนสาย UART **ทายก่อนรัน**: ไบต์ `0xA5` บิตแรกหลัง start bit เป็น 1 หรือ 0

```sh
gcc -std=c11 -Wall -Wextra -o uart_frame examples/11_uart_frame.c
./uart_frame
```

บิตแรกเป็น 1 เพราะ UART ส่ง **บิตต่ำสุด (LSB) ก่อน** `0xA5` คือ `1010 0101` บนสายจึงเรียงเป็น 1 0 1 0 0 1 0 1 — ที่ 115200 baud หนึ่งบิตยาว 8.68 ไมโครวินาที และหนึ่งเฟรมแบบ 8N1 ยาวสิบบิต ไบต์เดียวกันนี้คือไบต์แรกที่คุณจะจับได้จากขาของบอร์ดในแล็บ

---

## แนวคิด (1) — หนึ่งเฟรมของ UART

UART ไม่มีสายสัญญาณนาฬิกา ทั้งสองฝั่งตกลง baud rate กันไว้ก่อน แล้วใช้ขอบของ start bit เป็นจุดตั้งเวลา

```text
 idle  start  D0..D7 (LSB ก่อน)  [parity]  stop  idle
 ‾‾‾‾‾\_____/‾‾‾ ... ข้อมูล 8 บิต ...        [P]   ‾‾‾‾  ‾‾‾‾
```

| ส่วน | ระดับ | หน้าที่ |
|---|---|---|
| idle | 1 | สายว่างถูกดึงไว้ที่ระดับสูง |
| start | 0 | ขอบขาลงบอกผู้รับว่าเฟรมเริ่ม |
| data | ตามข้อมูล | 5-9 บิต ส่วนใหญ่ 8 บิต LSB ก่อน |
| parity (ถ้ามี) | ตามกติกา | จับบิตผิดได้เป็นจำนวนคี่เท่านั้น |
| stop | 1 | ถ้าเห็น 0 ตรงนี้คือ framing error มักแปลว่า baud ไม่ตรงกัน |

ค่าตั้งของ debug UART ใน BSP ตรงกับ 8N1 ทุกข้อ: `dataWidth=8`, `parity=NONE`, `stopBits=1`, `enableMsbFirst=false`, `oversample=10`

---

## แนวคิด (2) — หนึ่งพอร์ต หนึ่งเจ้าของ

UART คือสายไบต์เส้นเดียว ถ้าสอง task อ่านพอร์ตเดียวกัน ไบต์จะถูกแบ่งไปคนละครึ่งโดยไม่มีใครได้ข้อความครบ — SDK ตั้งหัวข้อว่า **"ONE OWNER. EXACTLY ONE."** และอธิบายว่า **"a split stream is not a protocol — a magic byte lands in one task and the command byte in the other, and both see garbage"**

งานอื่นที่อยากได้ข้อมูลจึงรับต่อจากเจ้าของผ่านบัฟเฟอร์ (ring ที่คืน -1 เมื่อว่าง)

ขาส่งก็มีเจ้าของเหมือนกัน `printf` ของ retarget-io ถือ mutex ระหว่างพิมพ์ — ตัวรันตัวอย่างของ SDK ตั้งไว้ที่ priority 1 เพราะ mutex นี้ **"with no priority inheritance"** ทำให้ task ที่ความสำคัญต่ำสุด **"can only ever be the waiter, never the holder that blocks somebody more important"** — ห้าม `printf` จาก ISR เด็ดขาด

---

## แนวคิด (3) — อ่านสาย UART ด้วย logic analyzer

logic analyzer สุ่มระดับของสายเป็น 0 หรือ 1 หลายครั้งต่อบิต แล้วโปรแกรมถอดรหัสหาขอบ start แล้วอ่านกลางบิต ตั้งค่าให้ตรงกับผู้ส่งทุกข้อ

| ตั้งค่า | สำหรับ UART บน header ของบอร์ดนี้ |
|---|---|
| ขาที่วัด | TX คือ P15.1 (SCB9) ต่อกราวด์ของ analyzer กับกราวด์ของบอร์ดเสมอ |
| ระดับแรงดัน | 3.3 V |
| อัตราสุ่ม | หลายเท่าของ baud เช่น 1 MHz ขึ้นไปสำหรับ 115200 |
| decoder | UART, baud 115200, data 8 บิต, parity none, stop 1, LSB first |
| trigger | ขอบขาลงบนสาย TX เพื่อจับเฟรมแรก |

> ถ้า decoder ขึ้น framing error ทุกเฟรม ให้สงสัย baud ก่อนสิ่งอื่น ถ้าขึ้นไบต์ที่ดูเหมือนกลับบิต ให้สงสัยลำดับบิตหรือขั้วสัญญาณ

---

## ตัวอย่างสมบูรณ์ — สามท่าใน 11_uart_frame.c

**ท่าที่ 1** `uart_encode()` สร้างระดับของ start, data แบบ LSB ก่อน, parity และ stop
**ท่าที่ 2** `draw()` วาดรูปคลื่นแบบข้อความพร้อมป้าย S, D0-D7, P, T และเวลาของบิตกับเฟรม
**ท่าที่ 3** วาด `0xA5` แบบ 8N1 และ 8E1 และ `0x11` (ไบต์ที่สองที่ตัวอย่าง Header I/O Test ส่ง) แล้วคำนวณ throughput

```c
static const int idle = 1, start = 0, stop = 1;
// 0xA5 = 1010 0101 -> ส่งบิต LSB ก่อน: 1 0 1 0 0 1 0 1
for (int i = 0; i < 8; i++) {
    bit[i] = (byte >> i) & 1u;   /* LSB (bit0) ส่งก่อน */
}
```

ลองแก้แล้วทายก่อนรัน: เปลี่ยน baud เป็น 9600 ความยาวเฟรมเป็นเท่าไร ถ้าต้องส่ง log 200 ไบต์/วินาที 9600 พอไหม

---

## ฝึกเติม

เปิด [practice/11_uart_decode.c](practice/11_uart_decode.c) — ตัวถอดรหัสที่ทำงานแบบเดียวกับ logic analyzer มีช่องให้เติม 3 จุด (บทแรกของโมดูล 5 จึงเว้นว่างน้อย)

1. อ่านบิตข้อมูลที่กลางบิต LSB ก่อน
2. ตรวจ parity แบบ even และ odd
3. ตรวจ stop bit แล้วคืน framing error เมื่อผิด

```sh
gcc -std=c11 -Wall -Wextra -o uart_decode practice/11_uart_decode.c && ./uart_decode
```

test มีกรณี `0xFF` ซึ่งเป็นข้อมูลจริงไม่ใช่ "ไม่มีข้อมูล" และกรณี stop bit เป็น 0 ที่จำลองอาการ baud ไม่ตรงกัน ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/11_uart_decode.c](solution/11_uart_decode.c)

---

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) ครอบคลุมเป้าหมายทั้งสามข้อ (ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน)

1. เฟรม 8N1 หนึ่งเฟรมมีระดับตามลำดับเวลาเป็น 0 1 1 0 0 0 0 0 0 1 ไบต์ข้อมูลคืออะไร
2. decoder ขึ้น framing error เกือบทุกเฟรม สาเหตุที่น่าสงสัยก่อนสิ่งอื่นคืออะไร
3. task A กับ task B ต่างเรียกฟังก์ชันอ่าน UART พอร์ตเดียวกันวนไปเรื่อย ๆ จะเกิดอะไร
4. ทำไมตัวรันตัวอย่างของ SDK ที่ใช้ printf จึงตั้งไว้ที่ priority ต่ำที่สุดเหนือ idle
5. ต้องถอดรหัส UART บนขา P15.1 ของ header ด้วย logic analyzer ค่าตั้งใดถูกต้อง (เลือกได้หลายข้อ)

---

## แล็บ

**งาน:** จับเฟรม UART จริงจากขาของบอร์ดด้วย logic analyzer ถอดรหัสด้วยตาก่อน แล้วยืนยันด้วย decoder

1. เปิดตัวอย่าง [QWA309 — Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) แล้ว flash ลงบอร์ด
2. ต่อ logic analyzer ที่ P15.1 (TX) และกราวด์ ตั้งค่าตามตารางในแนวคิดข้อ 3
3. เริ่มจับ แล้วกดปุ่ม **UART Echo** บนจอ — จอจะพิมพ์ `TX: A5 11 00 B4`
4. **ถอดรหัสด้วยตาก่อน** ขยายรูปคลื่นไบต์แรก ระบุ start bit บิตข้อมูลทั้งแปด และ stop bit แปลงเป็นฐานสิบหก ต้องได้ `A5` วัดความกว้างหนึ่งบิตเทียบกับ 8.68 µs
5. เปิด decoder แล้วเทียบกับที่ถอดด้วยตา และกับบรรทัด `TX:` บนจอ
6. ทดลองตั้ง decoder ผิดทีละข้อ: baud 57600, parity even, bit order MSB first จดว่า decoder แสดงอะไร

**หลักฐานที่เก็บไว้ใน portfolio:** ภาพรูปคลื่นที่ขีดป้ายบิตด้วยมือ ภาพผลของ decoder ค่าความกว้างของบิตที่วัดได้ และตารางอาการเมื่อตั้งค่าผิด

---

## ไปต่อ

- `08_tacp_host_protocol.c` อธิบายว่า `tacp_init()` ล้าง RX FIFO ของฮาร์ดแวร์ ถูกต้องตอนเริ่มระบบแต่ผิดถ้าเรียกทีหลัง — อ่านหัวข้อ "WHAT tacp_init() COSTS" แล้วอธิบายว่าทำไม
- เอกสาร [UART (Wikipedia)](https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter) หัวข้อ framing และ break condition
- โจทย์ท้าทาย: ขยายตัวถอดรหัสให้อ่านหลายเฟรมต่อกัน แล้วถอดแพ็กเก็ต `A5 11 00 B4` ทั้งแพ็กเก็ตพร้อมตรวจ XOR checksum

บทถัดไป: [บทเรียน 5.2 — I2C](../l02-i2c/README.md)

---

## แหล่งที่มาและเครดิต

"พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

โค้ดของหลักสูตรนี้ (`examples/`, `practice/`, `solution/`) Apache-2.0 · โค้ดของ SDK ไม่ได้คัดลอกเป็นไฟล์
บทเรียนยกมาเป็นช่วงสั้น ๆ พร้อมลิงก์ไปยังไฟล์ที่ commit `ef72c1b` (Apache-2.0, tesaiot-pse84-devkit-sdk)
