---
id: c-found.m05.l03
lang: th
title: {th: SPI, en: SPI}
summary: {th: เข้าใจโหมดของ SPI และสาย chip select แล้วยืนยันสัญญาณด้วย logic analyzer, en: 'Understand SPI modes and chip select, and verify signals with a logic analyzer.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m05.l02]
objectives:
- {th: อธิบายโหมด SPI ทั้งสี่จาก CPOL และ CPHA และเลือกโหมดให้ตรงกับ datasheet ของอุปกรณ์ได้, en: Explain the four SPI modes from CPOL and CPHA and match a device datasheet.}
- {th: 'ถอดรหัสภาพสัญญาณ SPI ได้ครบ SCLK, MOSI, MISO และ CS', en: 'Decode an SPI trace with SCLK, MOSI, MISO and CS.'}
- {th: เปรียบเทียบ SPI กับ I2C ในด้านจำนวนสาย ความเร็ว และการต่ออุปกรณ์หลายตัว, en: 'Compare SPI and I2C on wire count, speed and multi-device wiring.'}
develops:
- {skill: proto.spi, to: 3}
- {skill: meas.logic-analyzer, to: 2}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: pending
---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. อธิบายโหมด SPI ทั้งสี่จาก CPOL และ CPHA และเลือกโหมดให้ตรงกับ datasheet ของอุปกรณ์ได้
2. ถอดรหัสภาพสัญญาณ SPI ได้ครบ SCLK, MOSI, MISO และ CS
3. เปรียบเทียบ SPI กับ I2C ในด้านจำนวนสาย ความเร็ว และการต่ออุปกรณ์หลายตัว

ใช้เวลาประมาณ 70 นาที (แนวคิด 15 · ฝึก 25 · แล็บ 25 · เช็ก 5) แล็บใช้ logic analyzer สี่ช่องที่รับ 3.3 V ได้

## ก่อนเริ่ม

ทวนจากสองบทก่อนสองข้อ

1. UART ส่งบิตไหนก่อน และ I2C ส่งบิตไหนก่อน (บทเรียน 5.1 และ 5.2)
2. ใน I2C master เลือกอุปกรณ์ที่จะคุยด้วยอย่างไร ถ้าไม่มี address จะเลือกด้วยอะไรได้อีก

## ดูของจริงก่อน

เปิด [examples/13_spi_modes.c](examples/13_spi_modes.c) โปรแกรมนี้วาดไบต์ `0xA5` ในโหมด SPI ทั้งสี่ และทำเครื่องหมาย `^` ใต้ขอบที่ผู้รับอ่านค่า
**ทายก่อนรัน** ว่าในโหมด 3 ผู้รับอ่านที่ขอบขาขึ้นหรือขาลงของ SCLK

```sh
gcc -std=c11 -Wall -Wextra -o spi_modes examples/13_spi_modes.c
./spi_modes
```

โหมด 3 อ่านที่ขอบขาขึ้น เหมือนโหมด 0 ทั้งที่ SCLK ว่างอยู่คนละระดับ ส่วนโหมด 1 และ 2 อ่านที่ขอบขาลง
บรรทัดสุดท้ายเทียบ SPI สองตัวบนบอร์ดเดียวกัน SPI ของเรดาร์ที่ 25 MHz กับ SPI แบบ bit-bang บน header ที่ราว 67 kHz ช้ากว่ากันหลายร้อยเท่า

## แนวคิด

### 1. สี่สาย และโหมดสี่แบบ

SPI มีสัญญาณสี่เส้น SCLK (clock จาก master), MOSI (master ส่งออก), MISO (slave ส่งกลับ) และ CS หรือ SS (เลือก slave ส่วนใหญ่ทำงานที่ระดับต่ำ)
ข้อมูลวิ่งพร้อมกันสองทิศ ทุกจังหวะของ SCLK master ส่งหนึ่งบิตและรับหนึ่งบิต การ "อ่าน" จาก slave จึงคือการส่งอะไรสักอย่างออกไปพร้อมกันเสมอ

| โหมด | CPOL (ระดับว่างของ SCLK) | CPHA | ผู้รับอ่านที่ | ชื่อในค่าตั้งของ PDL |
|---|---|---|---|---|
| 0 | 0 (ต่ำ) | 0 | ขอบแรก = ขาขึ้น | `CY_SCB_SPI_CPHA0_CPOL0` |
| 1 | 0 (ต่ำ) | 1 | ขอบที่สอง = ขาลง | `CY_SCB_SPI_CPHA1_CPOL0` |
| 2 | 1 (สูง) | 0 | ขอบแรก = ขาลง | `CY_SCB_SPI_CPHA0_CPOL1` |
| 3 | 1 (สูง) | 1 | ขอบที่สอง = ขาขึ้น | `CY_SCB_SPI_CPHA1_CPOL1` |

การเลือกโหมดไม่ใช่การเดา datasheet ของอุปกรณ์ทุกตัวบอกไว้ ด้วยชื่อโหมด ด้วยค่า CPOL/CPHA หรือด้วยแผนภาพเวลาที่แสดงว่าข้อมูลถูกอ่านที่ขอบไหน
ถ้า datasheet ให้แค่แผนภาพ ให้ดูสองอย่าง SCLK ว่างที่ระดับไหน (CPOL) และข้อมูลต้องนิ่งตรงขอบแรกหรือขอบที่สอง (CPHA)
ค่าตั้งของ SPI ที่ต่อกับเรดาร์ใน BSP ของ SDK คือ `subMode = CY_SCB_SPI_MOTOROLA`, `sclkMode = CY_SCB_SPI_CPHA0_CPOL0` (โหมด 0),
`enableMsbFirst = true`, ข้อมูล 8 บิต และ CS ทุกขาทำงานที่ระดับต่ำ
([cycfg_peripherals.c บรรทัด 645-673](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bsps/TARGET_KIT_PSE84_AI/config/GeneratedSource/cycfg_peripherals.c#L645-L673))

### 2. SPI ของจริงบนบอร์ดนี้: ฮาร์ดแวร์กับ bit-bang

**SPI ของเรดาร์ BGT60TR13C** ใช้ SCB3 ขา MISO P21.4, MOSI P21.5, CLK P21.6, CS P21.7 และขา IRQ P20.3 ที่ 25 Mbps
([02_radar_presence.c บรรทัด 25-29](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/sensors/02_radar_presence.c#L25-L29))
ตัวเลขนี้ตรงกับการคำนวณ สัญญาณนาฬิกา 100 MHz ตัวหาร 0 และ `oversample = 4` ตามที่เอกสาร PDL บอกว่า master ต้องการ clk_scb เท่ากับ oversample คูณ data rate
task ของเรดาร์ตั้ง SPI ด้วย `Cy_SCB_SPI_Init()` ผูก ISR ด้วย `Cy_SysInt_Init()` เลือก slave ด้วย `Cy_SCB_SPI_SetActiveSlaveSelect()` แล้ว `Cy_SCB_SPI_Enable()`
([radar_task.c บรรทัด 152-173](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/radar_task.c#L152-L173))
และการรับส่งจริงใช้ `Cy_SCB_SPI_Transfer()` แบบ interrupt

ไฟล์ platform ของเรดาร์ใน SDK มีบทเรียนการดีบักที่ดีมาก ไดรเวอร์ต้นทางรอให้การส่งเสร็จด้วยลูป `while` ที่ไม่มีขอบเขต ถ้า interrupt ของ SPI หายไปหนึ่งครั้ง
ลูปนี้จะวนตลอดไป ทีม SDK วัดบนบอร์ดจริงแล้วพบว่าค่าบนหน้า Radar ค้างทุกครั้งหลังทำงานราวแปดวินาที จึงเปลี่ยนเป็นการรอแบบมีขอบเขตที่ยกเลิกการส่งแล้วคืน error
"A bounded spin turns an unrecoverable wedge into an error return."
([bento_bgt60trxx_platform.c บรรทัด 11-36 และ 85-102](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/bento_bgt60trxx_platform.c#L11-L102),
Apache-2.0 ต้นฉบับ Copyright 2022 Infineon Technologies AG ดัดแปลงใน tesaiot-pse84-devkit-sdk)

**SPI บน header** ในตัวอย่าง Header I/O Test ของ Developer Hub เป็น bit-bang โหมด 0 ที่ขา P9.3 (SCK), P9.2 (MOSI), P9.1 (MISO), P9.0 (CS)
CPU ตั้งค่าขาเองทีละบิตด้วย `Cy_GPIO_Write()` และหน่วง 5 ไมโครวินาทีระหว่างขั้น ช้ากว่าฮาร์ดแวร์มาก แต่ดูง่ายด้วย logic analyzer และพอสำหรับงานทดสอบ 8 ไบต์
(เอกสารตัวอย่างเรดาร์ของ SDK เตือนว่ามี "chip-select trap" ของ header ระหว่าง P9.0 กับ P9.2 ในแล็บให้ยึดขาตามที่ตัวอย่างที่คุณ flash พิมพ์บนจอ)

### 3. SPI กับ I2C

| ด้าน | SPI | I2C |
|---|---|---|
| จำนวนสาย | 3 สายร่วม (SCLK, MOSI, MISO) + CS หนึ่งเส้นต่อ slave | 2 สายร่วม (SCL, SDA) ทุกอุปกรณ์ |
| เลือกอุปกรณ์ | ด้วยสาย CS | ด้วย address 7 บิตในข้อมูล |
| ความเร็วบนบอร์ดนี้ | SPI ของเรดาร์ 25 MHz | บัสเซนเซอร์ 400 kHz |
| ทิศทาง | full-duplex ส่งและรับพร้อมกัน | half-duplex |
| ผู้รับยืนยันการรับ | ไม่มี (ไม่มี ACK) | มี ACK/NACK ทุกไบต์ |
| ลักษณะสาย | push-pull ขอบคม ขับได้เร็ว | open-drain กับ pull-up ความเร็วจำกัดด้วยความจุของสาย |

SPI เหมาะกับข้อมูลปริมาณมากจากอุปกรณ์ไม่กี่ตัว เช่นเรดาร์ จอภาพ หน่วยความจำแฟลช ส่วน I2C เหมาะกับเซนเซอร์หลายตัวที่ส่งข้อมูลน้อย ประหยัดขาของชิป
เพราะ SPI ไม่มี ACK การพิสูจน์ว่าสายดีจึงต้องอ่านค่าที่รู้คำตอบ เช่นรีจิสเตอร์ ID ของชิป แบบเดียวกับที่ทำกับ I2C ในบทเรียน 5.2

## ตัวอย่างสมบูรณ์

[examples/13_spi_modes.c](examples/13_spi_modes.c) ทำงานเป็นสามท่า

- **ท่าที่ 1** สร้างรูปคลื่นหนึ่งไบต์ MSB ก่อน ตาม CPOL และ CPHA ของแต่ละโหมด
- **ท่าที่ 2** วาด SCLK และ MOSI เป็นเส้น พร้อมระดับว่างก่อนและหลังเฟรม และ `^` ใต้ขอบที่อ่าน
- **ท่าที่ 3** เทียบความเร็วของ SPI ฮาร์ดแวร์ของเรดาร์กับ bit-bang ของ header

ลองแก้แล้วทายก่อนรัน

1. เปลี่ยนไบต์เป็น `0x31` ซึ่งเป็นไบต์ที่สองที่ตัวอย่าง Header I/O Test ส่ง แล้ววาดในโหมด 0
2. ถ้า master ใช้โหมด 0 แต่ slave ใช้โหมด 1 slave จะอ่านบิตที่ขอบไหน และข้อมูลที่ได้น่าจะเพี้ยนอย่างไร
3. ปรับให้พิมพ์ LSB ก่อน แล้วอธิบายว่าต้องตั้งค่าใดในทั้ง master และ decoder ให้ตรงกัน

## ฝึกเติม

เปิด [practice/13_spi_decode.c](practice/13_spi_decode.c) ตัวถอดรหัส SPI สี่สายแบบที่ logic analyzer ทำ นี่คือบทสุดท้ายของโมดูล 5 จึงเว้นว่างมากที่สุด 6 จุด

1. แยก CPOL กับ CPHA จากเลขโหมด
2. ล้างสถานะเมื่อ CS ไม่ทำงาน
3. แยกขอบ leading กับ trailing
4. เลือกขอบที่ต้องอ่านตาม CPHA
5. เลื่อนบิตเข้าไบต์ MSB ก่อน จากค่าที่นิ่งอยู่ก่อนขอบ
6. เก็บไบต์เมื่อครบ 8 บิตโดยไม่เขียนเลยที่เก็บ

```sh
gcc -std=c11 -Wall -Wextra -o spi_decode practice/13_spi_decode.c && ./spi_decode
```

test ใช้เฟรมจริงที่ตัวอย่าง Header I/O Test ส่งตอนกด SPI ครั้งแรก `A5 31 00 5A 01 02 03` ตามด้วย XOR checksum `CE`
และมีกรณีตั้งโหมดผิด ที่ decoder ต้องได้ไบต์ที่ไม่ตรงกับที่ส่ง

## เฉลย

ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/13_spi_decode.c](solution/13_spi_decode.c)
จุดสำคัญคือเฉลยอ่านค่าจาก `s[i - 1]` คือค่าที่นิ่งอยู่ก่อนขอบ แบบที่ flip-flop ของผู้รับจับจริง ถ้าอีกฝั่งเปลี่ยนข้อมูลตรงขอบนั้นพอดี (โหมดไม่ตรงกัน)
ผู้รับจะได้บิตของรอบก่อน test กรณีโหมดผิดมีไว้พิสูจน์ข้อนี้ และให้สังเกตว่า test นั้นผ่านได้ตั้งแต่ก่อนเติม เพราะโค้ดเปล่าก็ได้ไบต์ที่ไม่ตรงเหมือนกัน
test ที่ผ่านกับโค้ดเปล่ามีความหมายก็ต่อเมื่อ test คู่ของมัน (ถอดด้วยโหมดที่ถูกแล้วได้ `A5`) ผ่านด้วย

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) (บนเว็บไซต์อยู่ท้ายหน้านี้) ครอบคลุมเป้าหมายทั้งสามข้อ ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน

## แล็บ

**งาน:** จับธุรกรรม SPI จริงบน header ถอดรหัสด้วยตาและด้วย decoder แล้วพิสูจน์ผลของการตั้งโหมดผิด

1. flash ตัวอย่าง [QWA309 — Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) จาก Developer Hub (ถ้ายังไม่ได้ทำในบทเรียน 5.1)
2. ต่อ logic analyzer สี่ช่องที่ P9.3 (SCK), P9.2 (MOSI), P9.1 (MISO), P9.0 (CS) และกราวด์ ตรวจชื่อขากับบรรทัด `Port:` ที่ตัวอย่างพิมพ์บนจอตอนกดปุ่ม
3. ตั้ง trigger ที่ขอบขาลงของ CS แล้วกดปุ่ม **SPI ESP32** บนจอ จอจะพิมพ์บรรทัด `TX req:` ที่มีแปดไบต์
   (ถ้าไม่มีบอร์ดคู่ทดสอบ ผลบนจอจะเป็น FAIL แต่ master ยังส่งเฟรมออกมาทุกครั้ง)
4. ถอดรหัสไบต์แรกด้วยตา: SCLK ว่างที่ระดับไหน MOSI นิ่งตอนขอบไหน แล้วอ่าน 8 บิต MSB ก่อน ต้องได้ `A5`
5. ตั้ง decoder SPI เป็นโหมด 0, MSB first, CS active low เทียบกับบรรทัด `TX req:` แล้วเปลี่ยน decoder เป็นโหมด 1 ดูว่าไบต์เปลี่ยนเป็นอะไร
6. วัดความยาวของหนึ่งบิตและความยาวที่ CS อยู่ระดับต่ำ เทียบกับการประมาณราว 15 ไมโครวินาทีต่อบิตในตัวอย่างสมบูรณ์ ต่างกันเท่าไร เพราะอะไร

**หลักฐานที่เก็บไว้ใน portfolio:** ภาพรูปคลื่นสี่ช่องที่ขีดป้ายไบต์แรกด้วยมือ ภาพผลของ decoder ในโหมด 0 ที่ตรงกับ `TX req:` ภาพผลเมื่อตั้งเป็นโหมด 1
และตัวเลขเวลาที่วัดได้ในข้อ 6

## ไปต่อ

- อ่านหัวไฟล์ของ [`cy_scb_spi.h` @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/blob/release-v3.24.0/drivers/include/cy_scb_spi.h) หัวข้อ Configure Data Rate
  แล้วคำนวณว่าถ้าต้องการ SPI 10 MHz จากสัญญาณนาฬิกา 100 MHz ต้องตั้งตัวหารและ oversample อย่างไร
- เปิด [sigrok protocol decoders](https://sigrok.org/wiki/Protocol_decoders) ดูว่า decoder ของ SPI ต่อเป็นชั้นกับ decoder ของอุปกรณ์ (เช่นหน่วยความจำ SPI flash) ได้อย่างไร
- โจทย์ท้าทาย: ใช้ตัวถอดรหัสในแบบฝึกอ่านไฟล์ CSV ที่ export จาก PulseView ของคุณเอง

บทถัดไปเข้าสู่โมดูล 6: [บทเรียน 6.1 Unit test บนเครื่องโฮสต์](../../m06-test-and-ci/l01-unit-tests-on-host/README.md)

## สะท้อนคิด

- ถ้า datasheet ของอุปกรณ์ใหม่บอกแค่แผนภาพเวลา คุณจะอ่านอะไรจากภาพเพื่อเลือกโหมด และจะพิสูจน์อย่างไรว่าเลือกถูก
- ลูปรอที่ไม่มีขอบเขตในโค้ดของคุณมีกี่ที่ และถ้า interrupt ที่มันรอหายไปหนึ่งครั้ง อะไรจะเกิดขึ้น

## แหล่งอ้างอิง

- [Infineon mtb-pdl-cat1 (Peripheral Driver Library) @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/tree/release-v3.24.0)
- [SDK: cm55/sensors/02_radar_presence.c (ขาและความเร็วของ SPI เรดาร์)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/sensors/02_radar_presence.c)
- [SDK: tesaiot-radar/bento_bgt60trxx_platform.c (การรอ SPI แบบมีขอบเขต)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/bento_bgt60trxx_platform.c)
- [sigrok protocol decoders](https://sigrok.org/wiki/Protocol_decoders)
- [Serial Peripheral Interface (Wikipedia)](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface)

## ตัวอย่างบน TESAIoT Developer Hub

ลองของจริงบน TESAIoT Dev Kit: เปิดตัวอย่างบน Developer Hub เพื่ออ่านโค้ด ดาวน์โหลด หรือ flash เฟิร์มแวร์สำเร็จรูป

- [QWA309 — Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) — diagnostic: ทดสอบ Arduino header I/O ครบ (I2C 3V3, UART SCB9, SPI bit-bang, GPIO P13, PWM, ADC net, 4000T EZI2C) พร้อม console UI
