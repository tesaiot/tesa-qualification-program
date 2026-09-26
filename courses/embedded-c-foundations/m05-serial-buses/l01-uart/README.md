---
id: c-found.m05.l01
lang: th
title: {th: UART, en: UART}
summary: {th: เข้าใจเฟรมของ UART และกติกาเจ้าของพอร์ตเดียว แล้วยืนยันด้วย logic analyzer, en: 'Understand UART framing and the single-owner rule, and verify it with a logic analyzer.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m04.l04]
objectives:
- {th: 'ถอดรหัสเฟรม UART หนึ่งเฟรมจากภาพสัญญาณได้ครบ start bit, data, parity และ stop bit', en: 'Decode one UART frame from a trace: start bit, data, parity and stop bit.'}
- {th: อธิบายว่าทำไม UART หนึ่งพอร์ตควรมีเจ้าของเพียงงานเดียว และส่งต่อข้อมูลผ่านบัฟเฟอร์, en: Explain why one UART port should have a single owner task that hands data on through a buffer.}
- {th: ตั้งค่า logic analyzer ให้ถอดรหัส UART ที่ baud rate ที่กำหนดได้, en: Set up a logic analyzer to decode UART at a given baud rate.}
develops:
- {skill: proto.uart, to: 3}
- {skill: meas.logic-analyzer, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
slides: slides.md
---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ถอดรหัสเฟรม UART หนึ่งเฟรมจากภาพสัญญาณได้ครบ start bit, data, parity และ stop bit
2. อธิบายว่าทำไม UART หนึ่งพอร์ตควรมีเจ้าของเพียงงานเดียว และส่งต่อข้อมูลผ่านบัฟเฟอร์
3. ตั้งค่า logic analyzer ให้ถอดรหัส UART ที่ baud rate ที่กำหนดได้

ใช้เวลาประมาณ 70 นาที (แนวคิด 15 · ฝึก 25 · แล็บ 25 · เช็ก 5) แล็บต้องมี logic analyzer ที่รับสัญญาณ 3.3 V ได้
และโปรแกรม [PulseView](https://sigrok.org/wiki/PulseView) หรือโปรแกรมของผู้ผลิตเครื่องที่ถอดรหัส UART ได้

## ก่อนเริ่ม

ทวนจากบทก่อนหน้าสองข้อ

1. debug UART ของบอร์ดนี้ใช้สัญญาณนาฬิกา 100 MHz ตัวหาร 86 และ oversample 10 ได้ baud จริงเท่าไร และคลาดจาก 115200 กี่เปอร์เซ็นต์ (บทเรียน 4.2)
2. ring buffer ในบทเรียน 1.3 ให้ผู้เขียนแก้อะไร และผู้อ่านแก้อะไร

## ดูของจริงก่อน

เปิด [examples/11_uart_frame.c](examples/11_uart_frame.c) โปรแกรมนี้วาดรูปคลื่นของหนึ่งไบต์บนสาย UART **ทายก่อนรัน** ว่าไบต์ `0xA5`
บิตแรกหลัง start bit เป็น 1 หรือ 0

```sh
gcc -std=c11 -Wall -Wextra -o uart_frame examples/11_uart_frame.c
./uart_frame
```

บิตแรกเป็น 1 เพราะ UART ส่ง **บิตต่ำสุด (LSB) ก่อน** `0xA5` คือ `1010 0101` บนสายจึงเรียงเป็น 1 0 1 0 0 1 0 1 อ่านจากซ้ายไปขวา
ที่ 115200 baud หนึ่งบิตยาว 8.68 ไมโครวินาที และหนึ่งเฟรมแบบ 8N1 ยาวสิบบิต ไบต์เดียวกันนี้คือไบต์แรกที่คุณจะจับได้จากขาของบอร์ดในแล็บ

## แนวคิด

### 1. หนึ่งเฟรมของ UART

UART ไม่มีสายสัญญาณนาฬิกา ทั้งสองฝั่งตกลงความเร็ว (baud rate) กันไว้ก่อน แล้วใช้ขอบของ start bit เป็นจุดตั้งเวลา

```
 idle  start  D0  D1  D2  D3  D4  D5  D6  D7  [parity]  stop  idle
 ‾‾‾‾‾\_____/‾‾‾ ... ข้อมูล 8 บิต LSB ก่อน ...  [P]      ‾‾‾‾  ‾‾‾‾
```

| ส่วน | ระดับ | หน้าที่ |
|---|---|---|
| idle | 1 | สายว่างถูกดึงไว้ที่ระดับสูง |
| start | 0 | ขอบขาลงบอกผู้รับว่าเฟรมเริ่ม ผู้รับนับเวลาจากขอบนี้ |
| data | ตามข้อมูล | 5 ถึง 9 บิต ส่วนใหญ่ 8 บิต LSB ก่อน |
| parity (ถ้ามี) | ตามกติกา | even หรือ odd ให้จำนวน 1 รวมเป็นคู่หรือคี่ จับบิตผิดได้เป็นจำนวนคี่เท่านั้น |
| stop | 1 | 1 หรือ 2 บิต ถ้าผู้รับเห็น 0 ตรงนี้คือ framing error ซึ่งมักแปลว่า baud ไม่ตรงกัน |

ค่าตั้งของ debug UART ใน BSP ของ SDK ตรงกับ 8N1 ทุกข้อ `dataWidth = 8UL`, `parity = CY_SCB_UART_PARITY_NONE`,
`stopBits = CY_SCB_UART_STOP_BITS_1`, `enableMsbFirst = false` และ `oversample = 10`
([cycfg_peripherals.c บรรทัด 584-608](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_peripherals.c#L584-L608))
oversample คือจำนวนจังหวะนาฬิกาต่อหนึ่งบิต ผู้รับใช้มันหากลางบิต จุดที่ไกลจากขอบที่สุด จึงทนความคลาดของ baud ได้ระดับหนึ่ง
แม่แบบเปิดพอร์ตนี้ใน `init_retarget_io()` ด้วย `Cy_SCB_UART_Init()` และ `Cy_SCB_UART_Enable()` แล้วผูกกับ `printf` ผ่าน retarget-io
([retarget_io_init.c บรรทัด 59-93](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/driver/retarget_io_init.c#L59-L93))

### 2. หนึ่งพอร์ต หนึ่งเจ้าของ

UART คือสายไบต์เส้นเดียว ถ้าสอง task อ่านพอร์ตเดียวกัน ไบต์จะถูกแบ่งไปคนละครึ่งโดยไม่มีใครได้ข้อความครบ
ตัวอย่าง [08_tacp_host_protocol.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/08_tacp_host_protocol.c#L17-L30)
ของ SDK (variant mtb-mpy) มีหัวข้อว่า "ONE OWNER. EXACTLY ONE." และอธิบายว่า "a split stream is not a protocol — a magic byte lands in one task
and the command byte in the other, and both see garbage" งานอื่นที่อยากได้ข้อมูลจึงรับต่อจากเจ้าของผ่านบัฟเฟอร์ ในไฟล์นั้นคือ ring ที่อ่านด้วย
`tacp_ring_buf_read()` ซึ่งคืน -1 เมื่อว่าง (บทเรียน 1.3)

ขาส่งก็มีเจ้าของเหมือนกัน `printf` ของ retarget-io ถือ mutex ระหว่างพิมพ์ ตัวรันตัวอย่างของ SDK จึงตั้ง task ของมันไว้ที่ priority 1
พร้อมเหตุผลว่า mutex นี้ "with no priority inheritance" task ที่ความสำคัญต่ำที่สุดจึง "can only ever be the waiter, never the holder that blocks somebody more important"
([sdk_examples_cm33.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sdk_examples_cm33.c))
และห้าม `printf` จาก ISR เด็ดขาด ในแม่แบบนี้คอร์ CM33_NS เป็นเจ้าของ console ตัวเดียวของบอร์ด ส่วน CM55 ไม่มี console เลย (บทเรียน 2.1)

### 3. อ่านสาย UART ด้วย logic analyzer

logic analyzer สุ่มระดับของสายเป็น 0 หรือ 1 หลายครั้งต่อบิต แล้วโปรแกรมถอดรหัสทำสิ่งเดียวกับผู้รับ UART หาขอบ start แล้วอ่านกลางบิต ตั้งค่าให้ตรงกับผู้ส่งทุกข้อ

| ตั้งค่า | สำหรับ UART บน header ของบอร์ดนี้ |
|---|---|
| ขาที่วัด | TX ของ header คือ P15.1 (SCB9) และต่อกราวด์ของ analyzer กับกราวด์ของบอร์ดเสมอ |
| ระดับแรงดัน | 3.3 V ตรวจว่า analyzer ของคุณรับได้ |
| อัตราสุ่ม | หลายเท่าของ baud เช่น 1 MHz ขึ้นไปสำหรับ 115200 ยิ่งสูงยิ่งเห็นขอบชัด |
| decoder | UART, baud 115200, data 8 บิต, parity none, stop 1, bit order LSB first, สัญญาณไม่กลับขั้ว |
| trigger | ขอบขาลงบนสาย TX เพื่อจับเฟรมแรก |

ขาและรูปแบบนี้มาจากตาราง "Peripherals at a glance" ของเอกสาร SDK ("QWA309 header UART | P15.0 RX / P15.1 TX | SCB9, 115200 8N1")
ถ้า decoder ขึ้น framing error ทุกเฟรม ให้สงสัย baud ก่อนสิ่งอื่น ถ้าขึ้นไบต์ที่ดูเหมือนกลับบิต ให้สงสัยลำดับบิตหรือขั้วของสัญญาณ

## ตัวอย่างสมบูรณ์

[examples/11_uart_frame.c](examples/11_uart_frame.c) ทำงานเป็นสามท่า

- **ท่าที่ 1** `uart_encode()` สร้างระดับของ start, data แบบ LSB ก่อน, parity และ stop
- **ท่าที่ 2** `draw()` วาดรูปคลื่นแบบข้อความพร้อมป้าย S, D0 ถึง D7, P, T และเวลาของบิตกับเฟรม
- **ท่าที่ 3** วาด `0xA5` แบบ 8N1 และ 8E1 และ `0x11` ซึ่งเป็นไบต์ที่สองที่ตัวอย่าง Header I/O Test ส่ง แล้วคำนวณ throughput

ลองแก้แล้วทายก่อนรัน

1. เปลี่ยน baud เป็น 9600 ความยาวของเฟรมเป็นเท่าไร และถ้าต้องส่ง log 200 ไบต์ต่อวินาที 9600 พอไหม
2. เพิ่ม `PARITY_ODD` ให้ `0xA5` บิต parity เป็นอะไร
3. วาด `0xB4` แล้วเทียบกับรูปคลื่นที่คุณจะจับได้ในแล็บ

## ฝึกเติม

เปิด [practice/11_uart_decode.c](practice/11_uart_decode.c) ตัวถอดรหัสที่ทำงานแบบเดียวกับ logic analyzer มีช่องให้เติม 3 จุด เป็นบทแรกของโมดูล 5 จึงเว้นว่างน้อย

1. อ่านบิตข้อมูลที่กลางบิต LSB ก่อน
2. ตรวจ parity แบบ even และ odd
3. ตรวจ stop bit แล้วคืน framing error เมื่อผิด

```sh
gcc -std=c11 -Wall -Wextra -o uart_decode practice/11_uart_decode.c && ./uart_decode
```

test มีกรณี `0xFF` ซึ่งเป็นข้อมูลจริงไม่ใช่ "ไม่มีข้อมูล" และกรณี stop bit เป็น 0 ที่จำลองอาการ baud ไม่ตรงกัน

## เฉลย

ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/11_uart_decode.c](solution/11_uart_decode.c)
คอมเมนต์ในเฉลยชี้ข้อจำกัดของ parity ที่คนมักลืม มันจับได้เฉพาะเมื่อบิตผิดเป็นจำนวนคี่ ถ้าผิดสองบิตพร้อมกัน parity ยังถูก
ข้อมูลที่สำคัญจึงต้องมี checksum หรือ CRC ในระดับข้อความด้วย ตัวอย่าง Header I/O Test ปิดท้ายทุกแพ็กเก็ตด้วย XOR checksum และ TACP ของ SDK ใช้ CRC-16

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) (บนเว็บไซต์อยู่ท้ายหน้านี้) ครอบคลุมเป้าหมายทั้งสามข้อ ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน

## แล็บ

**งาน:** จับเฟรม UART จริงจากขาของบอร์ดด้วย logic analyzer ถอดรหัสด้วยตาก่อน แล้วยืนยันด้วย decoder

1. เปิดตัวอย่าง [QWA309 — Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) บน Developer Hub
   แล้ว flash เฟิร์มแวร์สำเร็จรูปของตัวอย่างลงบอร์ด (ตัวอย่างนี้ใช้ master template ของ Developer Hub ไม่ใช่แม่แบบของ SDK ภาพรวมอยู่ใน
   [TESAIoT Firmware Stack บทเรียน 1.1](../../../tesaiot-firmware-stack/m01-getting-started/l01-toolchain-and-master-template/README.md))
2. ต่อ logic analyzer: ช่องหนึ่งที่ P15.1 (TX ของ UART บน header) และกราวด์ ดูตำแหน่งขาจากแผ่นวงจรหรือเอกสารของบอร์ด ตั้งค่าตามตารางในแนวคิดข้อ 3
3. เริ่มจับ แล้วกดปุ่ม **UART Echo** บนจอ จอจะพิมพ์บรรทัด `TX: A5 11 00 B4` (เลขตัวที่สามเพิ่มทุกครั้งที่กด)
   เมื่อไม่มีบอร์ดคู่ทดสอบต่ออยู่ ผลบนจอจะเป็น FAIL เพราะไม่มีใครตอบ แต่แพ็กเก็ตยังถูกส่งออกจากขา TX ทุกครั้งที่ลองใหม่
   (ตัวอย่างส่ง `Cy_SCB_UART_PutArrayBlocking()` ก่อนรอคำตอบ และลองซ้ำได้ถึงสี่ครั้ง)
4. **ถอดรหัสด้วยตาก่อน** ขยายรูปคลื่นของไบต์แรก ระบุ start bit บิตข้อมูลทั้งแปด และ stop bit แล้วแปลงเป็นเลขฐานสิบหก ต้องได้ `A5`
   วัดความกว้างของหนึ่งบิตด้วยเคอร์เซอร์ของโปรแกรม เทียบกับ 8.68 ไมโครวินาที
5. เปิด decoder แล้วเทียบกับที่ถอดด้วยตา และกับบรรทัด `TX:` บนจอ
6. ทดลองตั้ง decoder ผิดทีละข้อ: baud 57600, parity even, bit order MSB first จดว่า decoder แสดงอะไรในแต่ละกรณี

**หลักฐานที่เก็บไว้ใน portfolio:** ภาพรูปคลื่นที่ขีดป้ายบิตด้วยมือ ภาพผลของ decoder ที่ตรงกับบรรทัด `TX:` บนจอ ค่าความกว้างของบิตที่วัดได้
และตารางอาการเมื่อตั้งค่าผิดทั้งสามแบบ

## ไปต่อ

- ตัวอย่าง `08_tacp_host_protocol.c` ของ SDK อธิบายว่า `tacp_init()` ล้าง RX FIFO ของฮาร์ดแวร์ ซึ่งถูกต้องตอนเริ่มระบบแต่ผิดถ้าเรียกทีหลัง
  อ่านหัวข้อ "WHAT tacp_init() COSTS" แล้วอธิบายว่าทำไม
- เอกสาร [Universal asynchronous receiver-transmitter (Wikipedia)](https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter) หัวข้อ framing และ break condition
- โจทย์ท้าทาย: ขยายตัวถอดรหัสในแบบฝึกให้อ่านหลายเฟรมต่อกันจากสัญญาณยาวหนึ่งเส้น แล้วถอดแพ็กเก็ต `A5 11 00 B4` ทั้งแพ็กเก็ตพร้อมตรวจ XOR checksum

บทถัดไป: [บทเรียน 5.2 I2C](../l02-i2c/README.md)

## สะท้อนคิด

- ถ้าคุณเห็นแต่ framing error บนสาย คุณจะตรวจอะไรเป็นสามอย่างแรก และเรียงลำดับอย่างไร
- งานไหนในระบบของคุณที่อยาก "แอบอ่าน" UART ของคนอื่น และคุณจะออกแบบให้มันรับข้อมูลจากเจ้าของแทนได้อย่างไร

## แหล่งอ้างอิง

- [SDK: cm33/connectivity/08_tacp_host_protocol.c (UART มีเจ้าของเดียว)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/08_tacp_host_protocol.c)
- [SDK: cycfg_peripherals.c ของ BSP (ค่าตั้งของ debug UART)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_peripherals.c)
- [Peripherals at a glance (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__peripherals__quickref.html)
- [sigrok PulseView](https://sigrok.org/wiki/PulseView)
- [Universal asynchronous receiver-transmitter (Wikipedia)](https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter)

## ตัวอย่างบน TESAIoT Developer Hub

ลองของจริงบน TESAIoT Dev Kit: เปิดตัวอย่างบน Developer Hub เพื่ออ่านโค้ด ดาวน์โหลด หรือ flash เฟิร์มแวร์สำเร็จรูป

- [QWA309 — Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) — diagnostic: ทดสอบ Arduino header I/O ครบ (I2C 3V3, UART SCB9, SPI bit-bang, GPIO P13, PWM, ADC net, 4000T EZI2C) พร้อม console UI
