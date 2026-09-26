---
id: fw-sdk.m01.l02
lang: th
title:
  th: 'แล็บ: จับคู่โดเมน MCU กับชั้นของ SDK'
  en: 'Lab: Map MCU Domains to SDK Layers'
summary:
  th: 'แล็บเชิงแนวคิด (ไม่ต้อง flash บอร์ด): กรอกตารางจับคู่โดเมนกับงาน ติดป้ายชั้นซอฟต์แวร์ และตอบโจทย์รวมสองสถานการณ์'
  en: 'A conceptual lab (no flashing): fill in the domain-to-workload table, label the software layers and answer two integrated scenarios.'
level: L3
time_min:
  lab: 45
hardware:
  emulator: false
  boards:
  - none
prerequisites:
- fw-sdk.m01.l01
objectives:
- th: กรอกตารางจับคู่โดเมนกับงาน (ส่วนที่ 1) และตารางชั้นซอฟต์แวร์ (ส่วนที่ 2) ครบทุกแถวพร้อมเหตุผล
  en: Complete the domain-to-workload table (Part 1) and the software-layer table (Part 2) with a reason for every row.
- th: ทำ checklist จริง/เท็จ (ส่วนที่ 4) ถูกอย่างน้อย 8 จาก 10 ข้อ
  en: Score at least 8 of 10 on the true/false checklist (Part 4).
develops:
- skill: hw.architecture
  to: 2
- skill: build.vendor-sdk
  to: 1
assesses:
- skill: hw.architecture
  level: 2
  evidence: README.md#submission-checklist
context:
  platform: psoc-edge-e84
  lang: c
  ide: modustoolbox-vscode
  firmware: tesaiot-bitstream (HEX; source not public yet)
status: alpha
translation: done
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M01/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M01 — Map MCU Domains to TESA Firmware SDK Layers

**Course 1 · Module 1**  
**Type:** Conceptual lab (no board flash required)  
**Suggested time:** 30–45 minutes  

Read first: [Lesson](../l01-architecture-and-sdk-layers/README.md) · [Cheatsheet](../l01-architecture-and-sdk-layers/resources/sdk-layer-cheatsheet.md) · [← Table of Contents](../../README.md) · [M02 →](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md)

### Useful references while you map domains

| เอกสาร | ใช้เมื่อ |
|---|---|
| [E84 Product Brief (PDF)](https://www.infineon.com/assets/row/public/documents/30/45/infineon-psoc-edge-e84-productbrief-en.pdf) | ตรวจชื่อโดเมน / NPU / HMI |
| [AN241775 — HAL on PSOC™ Edge (PDF)](https://www.infineon.com/assets/row/public/documents/30/42/infineon-an241775-getting-started-with-hal-psoc-edge-applicationnotes-en.pdf) | จับคู่คำศัพท์ BSP / PDL / HAL |
| [Arm Cortex-M55](https://developer.arm.com/Processors/Cortex-M55) · [Ethos-U55](https://developer.arm.com/Processors/Ethos-U55) | อ่านลึกคอร์ / NPU |

---

## Lab Goals

เมื่อทำครบ คุณจะ:

- จับคู่โดเมนฮาร์ดแวร์ (Cortex-M55 / Cortex-M33 / Ethos-U55 NPU) กับประเภทงานได้อย่างสมเหตุสมผล
- ระบุได้ว่าโค้ดประเภทใดควรอยู่ชั้น HAL/BSP, Driver API, Utility หรือ Application
- ตรวจความเข้าใจด้วย checklist สั้น ๆ

---

## Prerequisites

- [ ] อ่านจบบทเรียน [บทเรียน](../l01-architecture-and-sdk-layers/README.md)
- [ ] เปิดแผ่นสรุป [sdk-layer-cheatsheet.md](../l01-architecture-and-sdk-layers/resources/sdk-layer-cheatsheet.md)
- [ ] กระดาษ โน้ต หรือไฟล์ว่างสำหรับกรอกคำตอบ

> **Flash / Hello World อยู่ที่ไหน?**  
> การติดตั้ง ModusToolbox สร้างโปรเจกต์ และ flash บอร์ดอยู่ใน **M02**  
> Lab นี้ตั้งใจเป็นแผนที่ความคิดก่อนลงมือกับเครื่องมือ

---

## Part 1 — Map Domains to Workloads

จากตารางด้านล่าง ให้เลือกโดเมนที่เหมาะสมที่สุดสำหรับแต่ละงาน  
ตอบได้มากกว่าหนึ่งโดเมนถ้าจำเป็น แต่ต้องเขียนเหตุผลสั้น ๆ

| # | งาน | ตัวเลือก | คำตอบของคุณ | เหตุผลสั้น ๆ |
|---|---|---|---|---|
| 1 | วนอ่านปุ่มและกระพริบ LED ตามสถานะ UI | M55 / M33 / NPU | | |
| 2 | ฟัง wake-word แบบใช้พลังงานต่ำตลอดเวลา | M55 / M33 / NPU | | |
| 3 | รันโมเดล gesture recognition บนอุปกรณ์ | M55 / M33 / NPU | | |
| 4 | จัดรูปแบบ JSON แล้ว publish MQTT | M55 / M33 / NPU | | |

### Self-Check Guidance (read after answering)

| # | แนวทาง |
|---|---|
| 1 | งาน UI/control หลักมักอยู่บน **Cortex-M55** |
| 2 | งาน always-on / low power มักโยง **Cortex-M33** |
| 3 | งาน inference หนัก ๆ มักพึ่ง **Ethos-U55 (NPU)** (แอปบน M55 ยังเป็นผู้ประสาน) |
| 4 | การจัด payload / MQTT เป็นงาน **Application บนคอร์หลัก** — ไม่ใช่หน้าที่ NPU โดยตรง |

ไม่จำเป็นต้องตรงคำต่อคำกับตารางนี้ ถ้าเหตุผลของคุณสอดคล้องกับหลัก multi-domain ก็ถือว่าผ่าน

---

## Part 2 — Label the SDK Layers

สมมติโครงสร้างโฟลเดอร์อย่างง่ายของโปรเจกต์เฟิร์มแวร์ (ชื่อสมมติเพื่อการเรียน — ไม่ใช่ path จริงของ SDK):

```text
app/
  main.c                 # product logic, สร้าง task
  gesture_policy.c       # ตัดสินใจเมื่อได้ผล inference
bsp/
  board_init.c           # clock, pin mux, bring-up
drivers/
  gpio_api.c
  i2c_api.c
  uart_api.c
utils/
  ring_buffer.c
  simple_filter.c
```

กรอกตาราง:

| กลุ่มไฟล์ | ชั้น (HAL/BSP, Driver, Utility, Application) | เหตุผลสั้น ๆ |
|---|---|---|
| `bsp/board_init.c` | | |
| `drivers/i2c_api.c` | | |
| `utils/ring_buffer.c` | | |
| `app/gesture_policy.c` | | |

### Self-Check Guidance

| กลุ่มไฟล์ | ชั้นที่คาดหวัง |
|---|---|
| `bsp/board_init.c` | HAL / BSP |
| `drivers/i2c_api.c` | Driver API |
| `utils/ring_buffer.c` | Utility |
| `app/gesture_policy.c` | Application |

---

## Part 3 — Integrated Scenarios

### 3A — On-Device Gesture

โจทย์:

> อ่านค่า IMU ผ่าน I²C เป็นคาบ → เก็บหน้าต่างตัวอย่างสั้น ๆ → ส่งเข้าโมเดลบน Ethos-U55 → ถ้าเป็นท่าทางที่สนใจให้เปิด LED และเตรียมข้อความไปคลาวด์

ตอบเป็นข้อ ๆ (ไม่ต้องเขียนโค้ด):

1. ชั้นใดรับผิดชอบการคุย I²C กับชิปเซ็นเซอร์  
2. ชั้นใดเหมาะกับบัฟเฟอร์หน้าต่างตัวอย่าง  
3. โดเมน/บล็อกฮาร์ดแวร์ใดเร่ง inference ขั้นสูง  
4. ชั้นใดตัดสินใจว่า “ท่านี้สำคัญพอจะเปิด LED”  
5. เหตุใดการ publish MQTT จึงยังไม่ใช่หน้าที่ของ NPU  

### Self-Check Guidance (3A)

1. Driver API  
2. Utility (หรือโครงสร้างใน Application ที่เรียก utility)  
3. Ethos-U55 NPU  
4. Application  
5. NPU เร่งคำนวณโมเดล — การจัดข้อความและโปรโตคอลเป็นงานแอป/สแต็กสื่อสารบนคอร์หลัก

### 3B — Always-On Then Wake

โจทย์:

> ระบบรอจับกิจกรรมเสียงบนโดเมนพลังงานต่ำตลอดคืน เมื่อมีเหตุการณ์จึงปลุกโดเมนสมรรถนะสูงเพื่อรันโมเดลหนักและอัปเดตจอ

ตอบ:

1. คอร์/ตัวเร่งใดเหมาะกับช่วง “รอฟังตลอดคืน”  
2. คอร์/ตัวเร่งใดเหมาะกับช่วง “inference หนักหลังถูกปลุก”  
3. เพราะเหตุใดจึงไม่ควรให้ Ethos-U55 ทำงานเต็มที่ตลอด 24 ชั่วโมงถ้าผลิตภัณฑ์ใช้แบตเตอรี่  

### Self-Check Guidance (3B)

1. Cortex-M33 และ/หรือ NNLite  
2. Cortex-M55 ประสานงาน + Ethos-U55  
3. โดเมนสมรรถนะสูงและ NPU กินพลังงานมากกว่า — always-on ควรอยู่โดเมนพลังงานต่ำแล้วค่อยปลุกเมื่อจำเป็น

---

## Part 4 — Understanding Checklist (True / False)

ตอบ **ถูก** หรือ **ผิด**

1. TESA Firmware SDK คือชื่อของโปรแกรม IDE แทน ModusToolbox  
2. HAL/BSP ช่วยให้นักพัฒนาไม่ต้องตั้งค่า register พื้นฐานของบอร์ดด้วยตัวเองทุกครั้ง  
3. Driver API เป็นชั้นหลักสำหรับควบคุม GPIO, UART, I2C, SPI, PWM, ADC ในแนวทางของหลักสูตร  
4. Utility modules ใช้แทน Driver เมื่อต้องการพูดกับฮาร์ดแวร์โดยตรง  
5. Cortex-M55 และ Ethos-U55 มีบทบาทเดียวกันในทุกงาน  
6. Edge AI หมายถึงการส่งข้อมูลดิบทั้งหมดขึ้นคลาวด์เสมอ  
7. การเลือกโดเมนประมวลผลมีผลต่อพลังงานและความหน่วง (latency)  
8. M01 ต้องการให้ผู้เรียน flash เฟิร์มแวร์ Hello World ให้สำเร็จ  
9. ความปลอดภัยระดับชิป (เช่น Secure Boot) เป็นส่วนหนึ่งของสถาปัตยกรรม ไม่ใช่หัวข้อแยกจาก MCU  
10. บทถัดไป (M02) จะลงมือติดตั้งเครื่องมือและสร้างโปรเจกต์จริง  

### Checklist Answers

1. ผิด — SDK ≠ IDE  
2. ถูก  
3. ถูก  
4. ผิด — Utility ไม่แทน Driver  
5. ผิด — บทบาทต่างกัน  
6. ผิด — Edge AI มุ่งประมวลผลที่ขอบ  
7. ถูก  
8. ผิด — เป็นของ M02  
9. ถูก  
10. ถูก  

เกณฑ์แนะนำ: ได้อย่างน้อย 8/10 ก่อนไป M02

---

## Common Misconceptions

| ความเข้าใจผิด | แก้ไขอย่างไร |
|---|---|
| มี NPU แล้วไม่ต้องเขียนเฟิร์มแวร์ควบคุม I/O | NPU เร่ง inference — การอ่านเซ็นเซอร์/สั่ง actuator ยังผ่าน Driver และแอป |
| Utility คือ driver แบบย่อ | Utility ช่วยงานซ้ำ — การคุยฮาร์ดแวร์ยังผ่าน HAL/Driver |
| ต้องจำ datasheet ทั้งเล่มก่อน lab แรก | M01 โฟกัสแผนที่สถาปัตยกรรมและชั้น SDK |

---

## Submission Checklist

- [ ] กรอกตารางส่วนที่ 1 ครบ พร้อมเหตุผล  
- [ ] กรอกตารางส่วนที่ 2 ครบ  
- [ ] ตอบส่วนที่ 3A และ 3B ครบ  
- [ ] ทำ checklist ส่วนที่ 4 ได้อย่างน้อย 8/10  
- [ ] พร้อมเข้า M02 โดยอธิบายได้แล้วว่า SDK ต่างจาก IDE อย่างไร และ multi-domain ต่างจากคอร์เดียวอย่างไร  

---

[Lesson](../l01-architecture-and-sdk-layers/README.md) · [Cheatsheet](../l01-architecture-and-sdk-layers/resources/sdk-layer-cheatsheet.md) · [Table of Contents](../../README.md)
