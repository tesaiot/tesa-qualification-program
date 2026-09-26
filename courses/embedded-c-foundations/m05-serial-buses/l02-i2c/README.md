---
id: c-found.m05.l02
lang: th
title: {th: I2C, en: I2C}
summary: {th: สแกนบัส อ่านเขียนรีจิสเตอร์ของอุปกรณ์ และใช้ lock ของบัสร่วมกับงานอื่นอย่างถูกต้อง, en: 'Scan the bus, read and write device registers, and share the bus lock correctly with other tasks.'}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m05.l01]
objectives:
- {th: สแกนบัส I2C และระบุอุปกรณ์ที่พบจาก address ได้, en: Scan the I2C bus and identify devices by address.}
- {th: อ่านและเขียนรีจิสเตอร์ของอุปกรณ์ โดยถือ lock ของบัสตลอดหนึ่งธุรกรรมและคืนทุกครั้ง, en: Read and write device registers while holding the bus lock for one whole transaction and always releasing it.}
- {th: 'ถอดรหัสภาพสัญญาณ I2C ได้ครบ start, address, read/write, ACK/NACK และ stop', en: 'Decode an I2C trace: start, address, read/write, ACK/NACK and stop.'}
develops:
- {skill: proto.i2c, to: 3}
- {skill: meas.logic-analyzer, to: 3}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: pending
---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. สแกนบัส I2C และระบุอุปกรณ์ที่พบจาก address ได้
2. อ่านและเขียนรีจิสเตอร์ของอุปกรณ์ โดยถือ lock ของบัสตลอดหนึ่งธุรกรรมและคืนทุกครั้ง
3. ถอดรหัสภาพสัญญาณ I2C ได้ครบ start, address, read/write, ACK/NACK และ stop

ใช้เวลาประมาณ 70 นาที (แนวคิด 15 · ฝึก 25 · แล็บ 25 · เช็ก 5) แล็บใช้ logic analyzer สองช่องที่รับ 3.3 V ได้

## ก่อนเริ่ม

ทวนจากบทก่อนหน้าสองข้อ

1. UART ไม่มีสายสัญญาณนาฬิกา ผู้รับรู้จังหวะของบิตได้อย่างไร แล้วบัสที่มีสาย clock แยก (อย่าง I2C) ต่างกันอย่างไร
2. ตัวอย่าง `06_raw_register_access.c` ที่อ่านในบทเรียน 1.1 ทำ read-modify-write ของ `PWR_CTRL` ภายในอะไร และทำไมต้องครอบทั้งขั้น

## ดูของจริงก่อน

เปิด [examples/12_i2c_transaction.c](examples/12_i2c_transaction.c) โปรแกรมนี้จำลองบัสเซนเซอร์ของบอร์ดแล้วพิมพ์ธุรกรรมแบบที่ decoder ของ logic analyzer แสดง
**ทายก่อนรัน** ว่าไบต์แรกบนสายเมื่อจะอ่านจาก BMI270 (address `0x68`) คืออะไร

```sh
gcc -std=c11 -Wall -Wextra -o i2c_transaction examples/12_i2c_transaction.c
./i2c_transaction
```

คำตอบคือ `D0` ไม่ใช่ `68` เพราะ address 7 บิตถูกเลื่อนซ้ายหนึ่งบิตแล้วต่อด้วยบิต R/W บรรทัด `probe` แสดงสิ่งที่การสแกนทำ ส่ง address แล้วดูว่ามีใครตอบ ACK
ส่วนบรรทัด `read` แสดงว่าการอ่านรีจิสเตอร์หนึ่งครั้งประกอบด้วยการเขียนหมายเลขรีจิสเตอร์ repeated START แล้วจึงอ่าน ทั้งหมดในธุรกรรมเดียว

## แนวคิด

### 1. หนึ่งธุรกรรมบนบัส I2C

I2C ใช้สองสาย SCL (clock ที่ master เป็นคนขับ) และ SDA (ข้อมูล) ทั้งสองเป็นแบบ open-drain มีตัวต้านทานดึงขึ้น อุปกรณ์หลายตัวต่อร่วมสายเดียวกันและแยกกันด้วย address

| เหตุการณ์ | บนสาย | ความหมาย |
|---|---|---|
| START | SDA ลงขณะ SCL สูง | เริ่มธุรกรรม |
| address + R/W | 8 บิต MSB ก่อน: address 7 บิตแล้วบิต R/W (0 เขียน 1 อ่าน) | เรียกอุปกรณ์หนึ่งตัว |
| ACK / NACK | บิตที่เก้า ผู้รับดึง SDA ลง = ACK ปล่อยไว้สูง = NACK | "ได้รับแล้ว" หรือ "ไม่มีใครอยู่" / "พอแล้ว" |
| ข้อมูล | 8 บิต MSB ก่อน ตามด้วย ACK/NACK ทุกไบต์ | ทีละไบต์ |
| repeated START | START ใหม่โดยไม่ STOP ก่อน | เปลี่ยนจากเขียนเป็นอ่านโดยไม่ปล่อยบัส |
| STOP | SDA ขึ้นขณะ SCL สูง | จบธุรกรรม |

อุปกรณ์ส่วนใหญ่บนบัสเป็น "แฟ้มรีจิสเตอร์" ตัวอย่าง [06_raw_register_access.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/06_raw_register_access.c#L15-L32)
ของ SDK อธิบายว่า `sensor_i2c_read_reg()` เขียนหมายเลขรีจิสเตอร์ "with NO stop" แล้วตามด้วย repeated START กับการอ่าน
ซึ่ง "is what the parts expect and what you would get wrong writing it yourself" และบางอุปกรณ์ เช่น SHT40 ไม่มีรีจิสเตอร์เลย ใช้การส่งคำสั่งแล้วอ่านคำตอบ
ไฟล์เดียวกันจึงมี `sensor_i2c_write_raw()` กับ `sensor_i2c_read_raw()` ไว้สำหรับกรณีนั้น

### 2. สแกนแล้วพิสูจน์สายก่อนเชื่อไดรเวอร์

การสแกนคือการ probe ทุก address ในช่วง 0x08 ถึง 0x77 แล้วจดตัวที่ตอบ ACK บัสเซนเซอร์ของบอร์ดคือ SCB0 ที่ P8.0 (SCL) และ P8.1 (SDA)
ทำงานที่ 1.8 V และ 400 kHz และ address ที่คาดว่าจะพบบนบอร์ดนี้อยู่ในตาราง `bus_device_name()` ของ
[01_i2c_bus_scan.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/01_i2c_bus_scan.c#L98-L110)

| address | อุปกรณ์ |
|---|---|
| 0x08 | CapSense PSoC 4000T (บอร์ดฐาน) |
| 0x18 | TLV320DAC3100 audio codec |
| 0x44 | SHT40 ความชื้นและอุณหภูมิ |
| 0x68 | BMI270 IMU |
| 0x77 | DPS368 ความดันและอุณหภูมิ |

สองเรื่องที่ตัวอย่างเตือนไว้: BMM350 (0x15) อยู่บน I3C ซึ่งเป็นอุปกรณ์คนละตัว "and never appears here" และ address ที่ไม่อยู่ในตาราง "is not an error — it is a board you have added something to"
การพบ address ยังไม่ใช่การพิสูจน์ว่าเป็นชิปที่คิด [02_read_imu.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/02_read_imu.c#L32-L38)
สอนว่า "PROVE THE WIRE FIRST" อ่านรีจิสเตอร์ 0x00 ก่อน ได้ `0x24` คือ BMI270 จริง ได้ `0xFF` หรืออ่านไม่ได้คือบัสหรือชิปมีปัญหา ได้ค่าอื่นคือชิปคนละตัวที่ address เดียวกัน

### 3. lock ของบัส: หนึ่งธุรกรรมหนึ่ง lock และคืนทุกทาง

SCB0 มีหลายเจ้าของ บท J1 ของเอกสาร SDK ระบุว่า PAL ของ OPTIGA Trust M ก็เป็น master บน SCB0 ด้วย และ task เบื้องหลังอ่านเซนเซอร์ทุก 100 ms
ฟังก์ชันอ่านเขียนของ SDK **ไม่ถือ lock ให้** ผู้เรียกต้องครอบเองด้วย `sensor_i2c_lock()` กับ `sensor_i2c_unlock()` คอมเมนต์ใน 01_i2c_bus_scan.c
อธิบายว่าถ้าไม่ถือ "It works, it keeps working, and then one day a repeated START from this task lands between the address phase and the data phase
of the auto task's read and both come back wrong."

```c
/* Step 2 — take the bus. Never scan without this. */
if (!sensor_i2c_lock(SCAN_LOCK_TIMEOUT_MS)) {
    /* Someone still holds it after a full second. The likeliest cause is
     * the hazard in the header block: the auto task was suspended between
     * its own lock and unlock. Resuming it lets it finish and release. */
    printf("  sensor_i2c_lock(%u ms) TIMED OUT — someone holds the bus\r\n",
           (unsigned)SCAN_LOCK_TIMEOUT_MS);
    if (auto_was_running) {
        printf("  resuming the auto task so it can release the mutex\r\n");
        sensor_auto_start();
    }
    return SDK_EX_BUSY;
}
```

ที่มา: [01_i2c_bus_scan.c บรรทัด 143-155](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/01_i2c_bus_scan.c#L143-L155)
(Apache-2.0, tesaiot-pse84-devkit-sdk)

กติกาที่ได้จากตัวอย่างเหล่านี้

- **lock มี timeout เสมอ** และเมื่อหมดเวลาให้คืนผลว่า busy ไม่ใช่สรุปว่าบัสเสีย
- **หนึ่ง lock ต่อหนึ่งชุดข้อมูล ไม่ใช่ต่อหนึ่งรีจิสเตอร์** 02_read_imu อ่านความเร่ง gyro และอุณหภูมิภายใน lock เดียว เพื่อให้ทั้งสามมาจากจังหวะเดียวกัน
  และอุปกรณ์แบบสั่งแล้วรอคำตอบต้องถือ lock ข้าม "the command, the wait AND the response" (06_raw_register_access)
- **คืน lock ทุกทางออก** ในตัวอย่างสแกนมีบรรทัด "There is no path out of here that skips this." และบท J1 ชี้ว่าแม้การแจ้ง error ก็ต้องทำหลัง unlock
- **ไม่ถือ lock ข้ามการหน่วงเวลายาว ๆ** มันขวางทุกงานที่รอบัสอยู่

## ตัวอย่างสมบูรณ์

[examples/12_i2c_transaction.c](examples/12_i2c_transaction.c) ทำงานเป็นสามท่า

- **ท่าที่ 1** `address_byte()` เลื่อน address 7 บิตแล้วใส่บิต R/W
- **ท่าที่ 2** `probe()` จำลองการสแกนสี่ address รอบ 0x68 ตัวที่มีอุปกรณ์ตอบ ACK ที่เหลือ NACK
- **ท่าที่ 3** `read_register()` พิมพ์การอ่าน chip id หนึ่งไบต์ และการอ่านความเร่งหกไบต์ในธุรกรรมเดียว (burst read)

ลองแก้แล้วทายก่อนรัน

1. เปลี่ยนไปอ่าน DPS368 (0x77) ไบต์ address ตอนเขียนและตอนอ่านเป็นอะไร
2. ถ้าแยกการอ่านหกไบต์เป็นหกธุรกรรม ธุรกรรมละหนึ่งไบต์ จำนวนไบต์บนสายเพิ่มเป็นเท่าไร และทำไมตัวอย่างของ SDK บอกว่าแบบ burst "both faster and ATOMIC"
3. ใส่ `0x10` (DFR0522 RGB matrix ที่ต่อกับบัส 3.3 V ของ header) ลงในรายการอุปกรณ์ แล้ว probe ดู

## ฝึกเติม

เปิด [practice/12_i2c_trace.c](practice/12_i2c_trace.c) มีช่องให้เติม 4 จุด

1. `addr_byte()` ประกอบไบต์ address
2. `parse_addr_byte()` แยกกลับ และปฏิเสธ address ที่อยู่นอกช่วง 0x08 ถึง 0x77
3. `encode_read_reg()` สร้างลำดับเหตุการณ์ของการอ่านรีจิสเตอร์ รวม NACK ที่ไบต์สุดท้าย
4. `scan()` สแกนแบบเดียวกับ `sensor_i2c_scan()` และตัดผลเมื่อที่เก็บเต็ม

```sh
gcc -std=c11 -Wall -Wextra -o i2c_trace practice/12_i2c_trace.c && ./i2c_trace
```

## เฉลย

ลองเองก่อนอย่างน้อย 15 นาที แล้วเปิด [solution/12_i2c_trace.c](solution/12_i2c_trace.c)
คอมเมนต์ในเฉลยอธิบายสองจุดที่มักถูกข้าม ทำไมไม่มี STOP ระหว่างเลือกรีจิสเตอร์กับการอ่าน และทำไม master ต้องตอบ NACK ที่ไบต์สุดท้าย

## เช็กความเข้าใจ

ตอบคำถาม 5 ข้อใน [quiz.yaml](quiz.yaml) (บนเว็บไซต์อยู่ท้ายหน้านี้) ครอบคลุมเป้าหมายทั้งสามข้อ ตอบถูกตั้งแต่ 4 ข้อขึ้นไปถือว่าจบบทเรียน

## แล็บ

**งาน:** สแกนบัสเซนเซอร์ของบอร์ดด้วยตัวอย่างของ SDK แล้วจับธุรกรรม I2C จริงบนบัส 3.3 V ของ header ด้วย logic analyzer

**ส่วนที่ 1 สแกนด้วย SDK**

1. build ด้วย `make build -j ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/sensors/01_i2c_bus_scan` แล้ว flash ถอดสายเสียบใหม่
2. จาก serial console จด address ทุกตัวที่ตอบ และชื่อที่ตัวอย่างพิมพ์ เทียบกับตารางในแนวคิดข้อ 2 ตัวไหนไม่พบ ตัวไหนเกินมา
3. build อีกครั้งด้วย `SDK_EXAMPLE_CM33=cm33/sensors/02_read_imu` จดบรรทัด chip id และตอบว่านี่คือหลักฐานแบบไหนที่การสแกนให้ไม่ได้

**ส่วนที่ 2 จับสัญญาณ** (บัสเซนเซอร์ทำงานที่ 1.8 V และขาไม่ได้ออกมาที่ header ส่วนนี้จึงใช้บัส I2C 3.3 V ของ header แทน)

4. flash ตัวอย่าง [QWA309 — Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) จาก Developer Hub
   ต่อ logic analyzer ช่องหนึ่งที่ SCL อีกช่องที่ SDA ของ I2C บน Arduino header และต่อกราวด์ ตั้ง decoder เป็น I2C
5. จับขณะกดปุ่ม **Scan** บนจอ ตัวอย่างสแกน 0x08 ถึง 0x77 บนบัสเดียวกับจอสัมผัส หาใน decoder หนึ่ง address ที่ได้ NACK และหนึ่ง address ที่ได้ ACK
   แล้วถอดรหัสด้วยตาทีละบิต: START, 7 บิตของ address, บิต R/W, บิตที่เก้า, STOP
6. ถ้ามี DFR0522 RGB matrix ให้ต่อแล้วสแกนซ้ำ ควรเห็น 0x10 ตอบ ACK (ตัวอย่าง [DFR0522 RGB Dot Matrix](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_rgb_matrix&q=prac_qwa309_rgb_matrix) ใช้ address นี้)
7. วัดความถี่ของ SCL จากรูปคลื่น

**หลักฐานที่เก็บไว้ใน portfolio:** log ของการสแกนและ chip id จาก serial console ภาพรูปคลื่นของธุรกรรม ACK หนึ่งภาพและ NACK หนึ่งภาพที่ขีดป้ายด้วยมือ
และความถี่ SCL ที่วัดได้ (ให้บอกว่าวัดจากส่วนไหนของรูปคลื่น เพราะ I2C ความเร็วต่างกันได้ตามการตั้งค่าของแต่ละบัส)

## ไปต่อ

- อ่านบท [J1 — The sensor bus and its lock](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__j1__sensor__bus.html) ของเอกสาร SDK
  หัวข้อที่อธิบายว่าทำไม `sensor_i2c_init()` เรียกการกู้บัส (ปลดอุปกรณ์ที่ค้าง SDA ไว้) ก่อนตั้งขา
- อ่าน [Understanding the I2C Bus (Texas Instruments SLVA704)](https://www.ti.com/lit/an/slva704/slva704.pdf) เรื่อง pull-up และ clock stretching
  แล้วโยงกับ Appendix X #13 ของเอกสาร SDK ที่เล่าว่าอุปกรณ์ที่ยืด clock ค้างบนบัสของจอทำให้ task อื่นของ CM55 อดอาหาร

บทถัดไป: [บทเรียน 5.3 SPI](../l03-spi/README.md)

## สะท้อนคิด

- ถ้าคุณจะเพิ่มเซนเซอร์ตัวใหม่บนบัส SCB0 คุณต้องตรวจอะไรบ้างก่อน เพื่อไม่ให้เซนเซอร์สี่ตัวที่มีอยู่แล้วพัง
- เคยเจอโค้ดที่ "ส่วนใหญ่ทำงาน แต่บางทีค่าเพี้ยน" ไหม ลองคิดว่าเป็นอาการของการแย่งบัสได้หรือไม่

## แหล่งอ้างอิง

- [SDK: cm33/sensors/01_i2c_bus_scan.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/01_i2c_bus_scan.c)
- [SDK: cm33/sensors/06_raw_register_access.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/06_raw_register_access.c)
- [SDK: cm33/sensors/02_read_imu.c (พิสูจน์สายก่อนเชื่อ driver)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/02_read_imu.c)
- [J1 — The sensor bus and its lock (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__j1__sensor__bus.html)
- [Texas Instruments: Understanding the I2C Bus (SLVA704)](https://www.ti.com/lit/an/slva704/slva704.pdf)

## ตัวอย่างบน TESAIoT Developer Hub

ลองของจริงบน TESAIoT Dev Kit: เปิดตัวอย่างบน Developer Hub เพื่ออ่านโค้ด ดาวน์โหลด หรือ flash เฟิร์มแวร์สำเร็จรูป

- [QWA309 — DFR0522 RGB Dot Matrix](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_rgb_matrix&q=prac_qwa309_rgb_matrix) — ควบคุม DFRobot DFR0522 RGB matrix 8x16 (I2C 0x10) บน bus 3.3V ร่วมกับ display แสดง clear/fill/pixel/pattern ผ่าน LVGL UI
- [EP01 — DPS368 Monitor](https://dev.tesaiot.dev/?example=developer-hub--int_ep01_dps368_monitor&q=int_ep01_dps368_monitor) — อ่านค่าความดันบรรยากาศและอุณหภูมิจากเซนเซอร์ Infineon DPS368 ผ่าน I2C แล้วแสดงผลบนจอ LVGL
- [QWA309 — Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) — diagnostic: สแกนบัส I2C 3.3 V ของ header และทดสอบ UART, SPI, GPIO, PWM พร้อม console UI
