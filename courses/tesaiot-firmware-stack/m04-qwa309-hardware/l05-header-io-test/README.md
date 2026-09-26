---
id: fw-stack.m04.l05
lang: th
title:
  th: "ทดสอบ I/O บน header: I2C UART SPI GPIO PWM ADC"
  en: "Header I/O test: I2C, UART, SPI, GPIO, PWM, ADC"
summary:
  th: "ทดสอบ I/O บน header: I2C UART SPI GPIO PWM ADC"
  en: "Header I/O test: I2C, UART, SPI, GPIO, PWM, ADC"
level: L3
time_min: {concept: 10, practise: 25, lab: 30, check: 5}
hardware: {emulator: false, boards: [devkit]}
prerequisites: [fw-stack.m01.l01]
objectives:
  - th: "ทดสอบขา I/O บน header ครบทุกชนิดด้วยโปรแกรม diagnostic และอ่านผลจากคอนโซลบนจอ"
    en: "Exercise every I/O type on the header with the diagnostic program and read the on-screen console"
  - th: "ยืนยันสัญญาณอย่างน้อยหนึ่งชนิดด้วย logic analyzer หรือออสซิลโลสโคป"
    en: "Confirm at least one signal with a logic analyzer or oscilloscope"
develops:
  - {skill: proto.uart, to: 2}
  - {skill: proto.spi, to: 1}
  - {skill: proto.i2c, to: 2}
  - {skill: mcu.pwm, to: 1}
  - {skill: meas.logic-analyzer, to: 1}
context: {platform: psoc-edge-e84, lang: c, ide: modustoolbox}
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/tesaiot/developer-hub
  path: "prac_qwa309_header_hw_test"
  ref: e5c772252e7d20f715463e0d27df9ece4e569c38
---

# ทดสอบ I/O บน header: I2C UART SPI GPIO PWM ADC

## เป้าหมาย

1. ทดสอบขา I/O บน header ครบทุกชนิดด้วยโปรแกรม diagnostic และอ่านผลจากคอนโซลบนจอ
2. ยืนยันสัญญาณอย่างน้อยหนึ่งชนิดด้วย logic analyzer หรือออสซิลโลสโคป

## แนวคิด

### บอร์ดฐาน QWA309 มีอะไรให้ฝึก

บอร์ดฐาน QWA309 ของ TESAIoT Dev Kit มีอุปกรณ์จริงให้ฝึก ได้แก่ ปุ่มกด potentiometer 4 ตัว CAN transceiver และ header สำหรับต่ออุปกรณ์ภายนอก บทเรียนนี้ใช้แบบฝึกของ Developer Hub ที่เขียนไว้สำหรับบอร์ดนี้โดยตรง บทเรียนนี้ใช้ header ของ QWA309 เป็นเครื่องมือ diagnostic ตรวจสอบเส้นทาง I/O ทุกแบบที่ header รองรับในโปรแกรมเดียว ทั้ง I2C, UART, SPI, GPIO, PWM และ ADC/PWM3 โดยการทดสอบส่วนใหญ่ต้องต่อสายไปยังบอร์ด ESP32-S3 companion ที่รันเฟิร์มแวร์ simulator เป็นคู่ทดสอบ

### เครื่องมือ diagnostic ทดสอบอะไรบ้าง และผ่านขาไหน

หน้าจอมีปุ่มทดสอบแยกแต่ละบัส: **Scan** สแกนหาอุปกรณ์บน I2C บัสของจอ/ทัช (`DISPLAY_I2C_CONTROLLER_HW`), **I2C ESP32** คุยกับ ESP32 simulator ที่ address `0x30`, **UART Echo** ผ่าน SCB9 (`P15.1` = TX, `P15.0` = RX ที่ 115200 8N1), **SPI ESP32** ผ่าน SPI แบบ bit-bang บน `P9.0`–`P9.3` (CS/MISO/MOSI/SCK), **GPIO In/Out** ผ่าน 6 ขา (`P13.0`, `P13.3`–`P13.7`), **PWM Out** ผ่านคู่สัญญาณกลับเฟส PWM5 (`P13.3`/`P13.4`) และ **ADC In**/**PWM3 Out** ผ่านคู่ขาเน็ต ADC/PWM3 (`P15.2`/`P15.3`) แต่ละปุ่มรันการทดสอบแบบ non-blocking ผ่าน `lv_timer_create()` แล้วพิมพ์ผลลงกล่อง console บนจอที่สร้างด้วย `lv_textarea_create()` พร้อม timestamp กดปุ่มใดจะ disable ปุ่มอื่นชั่วคราวจนกว่าการทดสอบนั้นจะจบ

### ยืนยันคำตอบด้วยโปรโตคอลเล็ก ๆ: magic byte + counter + checksum

การทดสอบที่ต้องคุยกับ ESP32 (I2C, UART, SPI) ใช้โครงสร้างแพ็กเก็ตเดียวกัน: byte แรกเป็น magic คงที่ (คำขอ `ESP32_SIM_REQ_MAGIC = 0xA5`, คำตอบ `ESP32_SIM_RSP_MAGIC = 0x5A`) ตามด้วย command byte, counter ที่เพิ่มทุกครั้งที่ส่ง และปิดท้ายด้วย checksum จาก `xor_checksum()` ที่ XOR ทุกไบต์ก่อนหน้าเข้าด้วยกัน ฝั่งรับตรวจ magic, counter และ checksum ครบทั้งสามอย่างก่อนถึงจะสรุปว่า PASS ถ้าไม่ผ่านจะ retry ตามจำนวนที่กำหนด (เช่น `UART_TEST_RETRIES`) การตรวจสามชั้นนี้ยืนยันได้ว่า ESP32 คู่ทดสอบได้รับคำขอ "ครั้งนี้" จริง (ไม่ใช่คำตอบเก่าที่ค้างอยู่) และข้อมูลไม่เพี้ยนระหว่างทาง — แต่ยืนยันได้เฉพาะเส้นทางที่ทดสอบเส้นนั้นเท่านั้น ไม่ได้แปลว่าขาอื่นบน header ใช้งานได้ด้วย

### สแกน I2C เฉพาะช่วง address ที่มาตรฐานสงวนไว้ให้ใช้งานทั่วไป

`run_i2c_scan()` ไล่ address ตั้งแต่ `I2C_SCAN_MIN_ADDR = 0x08` ถึง `I2C_SCAN_MAX_ADDR = 0x77` ไม่ใช่เต็มช่วง 7 บิต 0x00–0x7F เพราะ 0x00–0x07 และ 0x78–0x7F ถูกสงวนไว้ในมาตรฐาน I2C สำหรับการใช้งานพิเศษ เช่น general call address ที่อุปกรณ์หลายตัวอาจตอบพร้อมกัน และรูปแบบ 10-bit addressing การ probe address ที่สงวนไว้อาจไปกระตุ้นพฤติกรรมที่ไม่ตั้งใจ อุปกรณ์ I2C ทั่วไปจึงไม่ใช้ address ในช่วงนี้ ฟังก์ชันพิมพ์ผลเป็นตารางฐาน 16 แถวละ 16 address ตรงกับรูปแบบมาตรฐานของเครื่องมือสแกน I2C ทั่วไป

### SPI แบบ bit-bang: CPU สลับขาเองทีละบิต แทนฮาร์ดแวร์ SCB

`spi_transfer_frame()` ไม่ใช้ SPI peripheral ของชิปเลย แต่ควบคุมขา `P9.3` (SCK), `P9.2` (MOSI), `P9.1` (MISO), `P9.0` (CS) ด้วย `Cy_GPIO_Write()`/`Cy_GPIO_Read()` ธรรมดา สลับ CS ลง แล้ววนทีละบิตจาก MSB: เขียน MOSI, หน่วง `Cy_SysLib_DelayUs(5U)`, ยก SCK ขึ้น, หน่วงอีก 5 µs, อ่าน MISO เก็บบิต, ลด SCK ลง เป็น mode 0 (clock ว่างที่ LOW สุ่มตัวอย่างตอนขอบขาขึ้น) ข้อดีของวิธีนี้คือเลือกใช้ขาใดก็ได้และเหมาะกับงานทดสอบ แต่ข้อเสียคือความเร็วช้ากว่าฮาร์ดแวร์มาก (CPU ไม่ว่างตลอดการส่ง) และจังหวะ clock แกว่งได้เมื่อมี interrupt แทรก ต่างจาก SPI ฮาร์ดแวร์ (SCB) ที่เลื่อนบิตด้วยวงจรเฉพาะและได้ clock ที่สม่ำเสมอกว่า ความต่างนี้เห็นได้ชัดเมื่อวัดด้วย logic analyzer

### PWM ที่บอร์ดส่งได้แต่ตรวจเองไม่ได้: รายงาน "SENT" ไม่ใช่ "PASS"

`run_pwm_output_test()` สร้างสัญญาณ PWM5 คู่กลับเฟส (`P13.3` = PWM5+, `P13.4` = PWM5−) ด้วยการสลับ `Cy_GPIO_Write()` ตรง ๆ ในลูป ไม่ได้ใช้ PWM peripheral ของชิป ที่ `PWM_TEST_HALF_PERIOD_MS = 20` ms ต่อครึ่งคาบ (คาบเต็ม 40 ms ≈ 25 Hz) วนซ้ำ `PWM_TEST_CYCLES = 50` รอบ เพราะบอร์ดสั่งขาออกได้แต่ไม่มีทางตรวจเองว่าสัญญาณไปถึงปลายทางจริงหรือไม่ ผลลัพธ์จึงรายงานเป็น "SENT" (ส่งแล้ว) ไม่ใช่ "PASS" (ยืนยันผ่านแล้ว) ต้องตรวจยืนยันจากฝั่ง ESP32 หรือเครื่องมือวัดภายนอกแยกต่างหาก จุดที่ต้องดูเป็นพิเศษคือ both-high fault (สองขาขึ้น HIGH พร้อมกัน) ซึ่งเป็นอันตรายกับวงจรที่ขับด้วยสัญญาณคู่กลับเฟส

### เชื่อเครื่องมือวัดก่อนเชื่อผลของซอฟต์แวร์ เมื่อสองอย่างขัดกัน

ถ้าโปรแกรมรายงาน PASS (ผ่านการตรวจ magic/counter/checksum ครบ) แต่ logic analyzer ที่ต่อไว้ไม่เห็นสัญญาณเลย ให้ตรวจการวัดก่อนสรุปว่าผลซอฟต์แวร์ผิด: ขาและกราวด์ที่ต่อ ระดับ threshold ของเครื่องมือ sample rate และ trigger ให้ถูกต้อง แล้ววัดซ้ำกับสัญญาณที่รู้ผลแน่นอนก่อน (เช่นขาที่กำลังทดสอบอยู่) เมื่อเห็นสัญญาณแล้วจึงค่อยเทียบกับผลของโปรแกรม ถ้ายังไม่ตรงกันจึงค่อยสงสัยโค้ดหรือฮาร์ดแวร์จริง ๆ — หลักการนี้คือตรวจเครื่องมือวัดเองก่อนเชื่อตัวเลขที่มันบอก

## ตัวอย่างสมบูรณ์

แบบฝึกชุด QWA309 ของ Developer Hub (อ้างอิงที่ commit `e5c7722`) รันบน TESAIoT Dev Kit เท่านั้น เพราะใช้อุปกรณ์บนบอร์ดฐาน

- **QWA309 — Header I/O Test** — diagnostic: ทดสอบ Arduino header I/O ครบ (I2C 3V3, UART SCB9, SPI bit-bang, GPIO P13, PWM, ADC net, 4000T EZI2C) พร้อม console UI
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_header_hw_test/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_header_hw_test) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test)

โค้ดตัวอย่างด้านล่างคัดลอกจากไฟล์จริงที่ commit เดียวกัน (Apache-2.0, tesaiot/developer-hub)

[`header_tester_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_header_hw_test/header_tester_ui.c) — checksum ที่ยืนยันว่าข้อมูลไม่เพี้ยนระหว่างทาง:

```c
static uint8_t xor_checksum(const uint8_t *data, uint32_t size)
{
    uint8_t checksum = 0U;

    for (uint32_t i = 0U; i < size; i++)
    {
        checksum ^= data[i];
    }

    return checksum;
}
```

[`header_tester_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_header_hw_test/header_tester_ui.c) — สแกน I2C เฉพาะช่วง address ที่มาตรฐานสงวนไว้ให้ใช้งานทั่วไป:

```c
for (uint8_t row = 0U; row < 8U; row++)
{
    for (uint8_t col = 0U; col < 16U; col++)
    {
        uint8_t address = (uint8_t)(row * 16U + col);

        if ((address < I2C_SCAN_MIN_ADDR) || (address > I2C_SCAN_MAX_ADDR))
        {
            continue;   /* reserved range, not a normal device address */
        }

        bool device_found = probe_i2c_address(address, NULL);
        /* ... record into found_addresses[], print into row_text ... */
    }
}
```

[`header_tester_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_header_hw_test/header_tester_ui.c) — SPI แบบ bit-bang: CPU สลับขาเองทีละบิต mode 0:

```c
for (int8_t bit = 7; bit >= 0; bit--)
{
    uint32_t tx_bit = ((tx[byte_index] >> (uint8_t)bit) & 0x01U);

    Cy_GPIO_Write(HEADER_SPI_MOSI_PORT, HEADER_SPI_MOSI_PIN, tx_bit);
    Cy_SysLib_DelayUs(5U);
    Cy_GPIO_Write(HEADER_SPI_CLK_PORT, HEADER_SPI_CLK_PIN, 1U);
    Cy_SysLib_DelayUs(5U);

    if (Cy_GPIO_Read(HEADER_SPI_MISO_PORT, HEADER_SPI_MISO_PIN) != 0U)
    {
        rx_byte |= (uint8_t)(1U << (uint8_t)bit);
    }

    Cy_GPIO_Write(HEADER_SPI_CLK_PORT, HEADER_SPI_CLK_PIN, 0U);
    Cy_SysLib_DelayUs(5U);
}
```

[`header_tester_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_header_hw_test/header_tester_ui.c) — PWM5 คู่กลับเฟสด้วย GPIO ตรง ๆ ผลลัพธ์รายงาน "SENT" ไม่ใช่ "PASS":

```c
for (uint32_t cycle = 0U; cycle < PWM_TEST_CYCLES; cycle++)
{
    Cy_GPIO_Write(P13_3_PORT, P13_3_PIN, 1U);
    Cy_GPIO_Write(P13_4_PORT, P13_4_PIN, 0U);
    Cy_SysLib_Delay(PWM_TEST_HALF_PERIOD_MS);

    Cy_GPIO_Write(P13_3_PORT, P13_3_PIN, 0U);
    Cy_GPIO_Write(P13_4_PORT, P13_4_PIN, 1U);
    Cy_SysLib_Delay(PWM_TEST_HALF_PERIOD_MS);
}
/* Result: SENT - not PASS; the board cannot verify the far end. */
```

## จุดที่มักพลาด

- **เชื่อว่า PASS ของการทดสอบหนึ่งเส้นทางแปลว่าขาอื่นบน header ใช้งานได้ด้วย** — โปรโตคอล magic/counter/checksum ยืนยันเฉพาะเส้นทางที่ถูกทดสอบจริงเท่านั้น ขาอื่นต้องทดสอบแยกของมันเอง
- **สแกน I2C เต็มช่วง 0x00–0x7F** — ช่วง 0x00–0x07 และ 0x78–0x7F ถูกสงวนไว้ตามมาตรฐาน probe เข้าไปอาจกระตุ้นพฤติกรรมพิเศษ เช่น general call ที่อุปกรณ์หลายตัวตอบพร้อมกัน
- **คิดว่า SPI bit-bang กับ SPI ฮาร์ดแวร์ให้ผลเหมือนกันทุกด้าน** — bit-bang ยืดหยุ่นเรื่องขาแต่ช้ากว่าและ clock แกว่งได้เมื่อมี interrupt แทรก ต่างจาก SCB ที่ clock สม่ำเสมอกว่า
- **เห็นผล "SENT" ของ PWM Out แล้วสรุปว่าผ่านแล้ว** — บอร์ดสั่งขาออกได้แต่ตรวจเองไม่ได้ว่าสัญญาณไปถึงปลายทาง ต้องยืนยันด้วยเครื่องมือวัดหรือฝั่ง ESP32 แยกต่างหาก
- **เจอผลซอฟต์แวร์กับเครื่องมือวัดขัดกันแล้วเชื่อเครื่องมือวัดทันที** — ต้องตรวจการตั้งค่าเครื่องมือวัดเอง (สาย กราวด์ threshold sample rate trigger) ก่อน ด้วยการวัดสัญญาณที่รู้ผลแน่นอนก่อนเปรียบเทียบ

### build และ flash

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

## ลองแก้

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

## เช็กความเข้าใจ

- SPI แบบ bit-bang ต่างจาก SPI ด้วยฮาร์ดแวร์อย่างไร
- ถ้าโปรแกรมรายงานว่า UART ผ่าน แต่ logic analyzer ไม่เห็นสัญญาณ เชื่ออะไร

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

## แหล่งอ้างอิง

- [แบบฝึกทั้งหมดของ TESAIoT Dev Kit](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38) · commit `e5c7722`
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้
