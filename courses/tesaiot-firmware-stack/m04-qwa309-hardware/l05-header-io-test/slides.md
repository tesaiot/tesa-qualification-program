---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 4.5 — ทดสอบ I/O บน header: I2C UART SPI GPIO PWM ADC"
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

# บทเรียน 4.5 — ทดสอบ I/O บน header: I2C UART SPI GPIO PWM ADC

## ทดสอบ I/O บน header: I2C UART SPI GPIO PWM ADC

**TESAIoT Dev Kit · PSoC Edge E84 · ภาษา C · ModusToolbox**

---

# เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ทดสอบขา I/O บน header ครบทุกชนิดด้วยโปรแกรม diagnostic และอ่านผลจากคอนโซลบนจอ
2. ยืนยันสัญญาณอย่างน้อยหนึ่งชนิดด้วย logic analyzer หรือออสซิลโลสโคป

---

# ก่อนเริ่ม

- ผ่านบทเรียนก่อนหน้ามาแล้ว: `fw-stack.m01.l01`
- บอร์ด: TESAIoT Dev Kit
- แพลตฟอร์ม: PSoC Edge E84 · ModusToolbox
- เวลาโดยประมาณ: เนื้อหา 10 + ฝึกตาม 25 + แล็บ 30 + เช็กความเข้าใจ 5 = 70 นาที

---

# ดูของจริงก่อน

แบบฝึกของ Developer Hub ที่เขียนไว้สำหรับบอร์ดฐาน QWA309 โดยตรง — เปิดบน Developer Hub แล้ว flash เฟิร์มแวร์สำเร็จรูปดูก่อนว่าหน้าจอเป็นอย่างไร

- **QWA309 — Header I/O Test** — diagnostic: ทดสอบ Arduino header I/O ครบ (I2C 3V3, UART SCB9, SPI bit-bang, GPIO P13, PWM, ADC net, 4000T EZI2C) พร้อม console UI
  [README](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_header_hw_test/README.md) · [โค้ด](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_header_hw_test) · [Developer Hub](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test)

---

# แนวคิด — บอร์ดฐาน QWA309 มีอะไรให้ฝึก

header ของ QWA309 เป็นเครื่องมือ diagnostic ตรวจ I/O ทุกแบบในโปรแกรมเดียว: I2C, UART, SPI, GPIO, PWM, ADC/PWM3

การทดสอบส่วนใหญ่ต้องต่อสายไปยังบอร์ด ESP32-S3 companion ที่รันเฟิร์มแวร์ simulator

---

# แนวคิด — ทดสอบอะไรบ้าง ผ่านขาไหน

Scan/I2C ESP32 (0x30) · UART Echo (SCB9, P15.0/1, 115200) · SPI ESP32 (bit-bang P9.0-3)

GPIO In/Out (P13.0,3-7) · PWM Out (P13.3/4) · ADC In/PWM3 Out (P15.2/3) — ปุ่มละหนึ่งบัส

---

# แนวคิด — ยืนยันคำตอบด้วย magic + counter + checksum

แพ็กเก็ต: magic คงที่ (0xA5 คำขอ / 0x5A คำตอบ) + command + counter + `xor_checksum()`

PASS ยืนยันเฉพาะเส้นทางที่ทดสอบ ไม่ได้แปลว่าขาอื่นใช้งานได้ด้วย

---

# แนวคิด — สแกน I2C เฉพาะช่วงที่มาตรฐานสงวนไว้

`I2C_SCAN_MIN_ADDR=0x08` ถึง `MAX_ADDR=0x77` ไม่ใช่เต็ม 0x00–0x7F

0x00–0x07 และ 0x78–0x7F สงวนไว้ (general call, 10-bit addressing) probe เข้าไปอาจกระตุ้นพฤติกรรมพิเศษ

---

# แนวคิด — SPI bit-bang: CPU สลับขาเองทีละบิต

`Cy_GPIO_Write/Read()` ธรรมดาบน P9.0-3 แทนฮาร์ดแวร์ SCB — mode 0, delay 5 µs ต่อขอบ

ยืดหยุ่นเรื่องขาแต่ช้ากว่า และ clock แกว่งได้เมื่อมี interrupt แทรก

---

# แนวคิด — PWM รายงาน "SENT" ไม่ใช่ "PASS"

`Cy_GPIO_Write()` สลับ P13.3/P13.4 ตรง ๆ (25 Hz, 50 รอบ) ไม่ใช้ PWM peripheral

บอร์ดสั่งออกได้แต่ตรวจเองไม่ได้ว่าถึงปลายทาง — ต้องยืนยันด้วยเครื่องมือวัดแยก

---

# แนวคิด — เครื่องมือวัดกับผลซอฟต์แวร์ขัดกัน เชื่ออะไรก่อน

ตรวจการตั้งค่าเครื่องมือวัดเอง (สาย กราวด์ threshold sample rate trigger) ก่อน

วัดสัญญาณที่รู้ผลแน่นอนก่อนเปรียบเทียบ — validate เครื่องมือก่อนเชื่อตัวเลข

---

# แนวคิด — ทักษะที่ฝึกในบทเรียนนี้

บทเรียนนี้พัฒนาทักษะต่อไปนี้ (ตามระดับ 1–5 ของหลักสูตร)

- `proto.uart` (ระดับ 2)
- `proto.spi` (ระดับ 1)
- `proto.i2c` (ระดับ 2)
- `mcu.pwm` (ระดับ 1)
- `meas.logic-analyzer` (ระดับ 1)

---

# ตัวอย่างสมบูรณ์ — สแกน I2C เฉพาะช่วงมาตรฐาน

[`header_tester_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_header_hw_test/header_tester_ui.c)

```c
for (uint8_t row = 0U; row < 8U; row++) {
    for (uint8_t col = 0U; col < 16U; col++) {
        uint8_t address = (uint8_t)(row * 16U + col);

        if ((address < I2C_SCAN_MIN_ADDR) ||
            (address > I2C_SCAN_MAX_ADDR)) {
            continue;   /* reserved range */
        }
        bool device_found = probe_i2c_address(address, NULL);
        /* ... record + print ... */
    }
}
```

---

# ตัวอย่างสมบูรณ์ — SPI bit-bang ทีละบิต

[`header_tester_ui.c`](https://github.com/tesaiot/developer-hub/blob/e5c772252e7d20f715463e0d27df9ece4e569c38/prac_qwa309_header_hw_test/header_tester_ui.c)

```c
for (int8_t bit = 7; bit >= 0; bit--)
{
    uint32_t tx_bit = ((tx[byte_index] >> (uint8_t)bit) & 0x01U);
    Cy_GPIO_Write(HEADER_SPI_MOSI_PORT, HEADER_SPI_MOSI_PIN, tx_bit);
    Cy_SysLib_DelayUs(5U);
    Cy_GPIO_Write(HEADER_SPI_CLK_PORT, HEADER_SPI_CLK_PIN, 1U);
    Cy_SysLib_DelayUs(5U);
    if (Cy_GPIO_Read(HEADER_SPI_MISO_PORT, HEADER_SPI_MISO_PIN) != 0U) {
        rx_byte |= (uint8_t)(1U << (uint8_t)bit);
    }
    Cy_GPIO_Write(HEADER_SPI_CLK_PORT, HEADER_SPI_CLK_PIN, 0U);
    Cy_SysLib_DelayUs(5U);
}
```

---

# จุดที่มักพลาด

- PASS ของเส้นทางหนึ่ง ≠ ขาอื่นบน header ใช้งานได้ด้วย — โปรโตคอลยืนยันแค่เส้นทางที่ทดสอบ
- สแกน I2C เต็ม 0x00–0x7F — ช่วงต้น/ท้ายสงวนไว้ อาจกระตุ้นพฤติกรรมพิเศษ
- คิดว่า SPI bit-bang เหมือน SPI ฮาร์ดแวร์ทุกด้าน — ช้ากว่าและ clock แกว่งได้
- เห็น "SENT" ของ PWM แล้วสรุปว่าผ่าน — บอร์ดตรวจเองไม่ได้ว่าถึงปลายทาง
- เครื่องมือวัดกับซอฟต์แวร์ขัดกันแล้วเชื่อเครื่องมือทันที — ตรวจการตั้งค่าเครื่องมือเองก่อน

---

# ตัวอย่างสมบูรณ์ — build และ flash

แบบฝึกชุด QWA309 ของ Developer Hub (อ้างอิงที่ commit `e5c7722`) รันบน TESAIoT Dev Kit เท่านั้น เพราะใช้อุปกรณ์บนบอร์ดฐาน

```sh
# ในโฟลเดอร์ master template (ดูบทเรียน 1.1)
# 1) ลบไฟล์ของ episode เก่าใน proj_cm55/apps/
# 2) คัดลอกไฟล์ทั้งหมดของ episode นี้ลงใน proj_cm55/apps/
make build
make program     # flash ผ่าน KitProg3
```

---

# ฝึกเติม / แล็บ

1. **ทาย** ก่อนแก้: เลือกค่าหนึ่งค่าที่ README ของตัวอย่างอธิบายไว้ในส่วน How แล้วเขียนว่าจะเห็นอะไรเปลี่ยนบนจอหรือใน log
2. **แก้และรัน** build + flash แล้วเทียบกับที่ทายไว้ ถ้าไม่ตรง ให้หาว่าเข้าใจส่วนไหนผิด
3. **ทำเพิ่ม** ต่อยอดหนึ่งอย่างที่ตัวอย่างยังไม่มี แล้วเก็บภาพหรือวิดีโอไว้ใน portfolio

---

# เช็กความเข้าใจ

- SPI แบบ bit-bang ต่างจาก SPI ด้วยฮาร์ดแวร์อย่างไร
- ถ้าโปรแกรมรายงานว่า UART ผ่าน แต่ logic analyzer ไม่เห็นสัญญาณ เชื่ออะไร

คำตอบอยู่ใน README ของตัวอย่างและในโค้ด ถ้าตอบข้อใดไม่ได้ ให้กลับไปอ่านส่วน Why / What / How อีกครั้ง

---

# ไปต่อ

- ทบทวนเป้าหมายทั้ง 2 ข้อของบทเรียนนี้ก่อนไปต่อ
- ถ้าตอบคำถามหน้าที่แล้วไม่ได้ครบ กลับไปอ่าน README ของตัวอย่างส่วน Why / What / How อีกครั้ง
- พร้อมแล้วไปเปิดบทเรียนถัดไปในโมดูลเดียวกัน

---

# แหล่งอ้างอิง

- [แบบฝึกทั้งหมดของ TESAIoT Dev Kit](https://github.com/tesaiot/developer-hub/tree/e5c772252e7d20f715463e0d27df9ece4e569c38) · commit `e5c7722`
- โค้ดเป็นของ Developer Hub และอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้

---

# เครดิต

> "TESAIoT Firmware Stack: เฟิร์มแวร์ภาษา C บน TESAIoT Dev Kit" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0

ตัวอย่างโค้ดเป็นผลงานของ TESAIoT Firmware Stack โดยสมาคมสมองกลฝังตัวไทย (TESA) ใน [tesaiot/developer-hub](https://github.com/tesaiot/developer-hub) รายละเอียดการให้เครดิตอยู่ที่ [ATTRIBUTION.md](../../../../ATTRIBUTION.md)
