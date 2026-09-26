# Cheatsheet — Architecture and SDK Layers (M01)

**Course 1 · Module 1**

ใช้ควบคู่บทเรียนและแบบฝึก M01 — แผ่นสรุปหนึ่งหน้า ไม่แทน datasheet

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [← Table of Contents](../../../README.md)

---

## Hardware Domains (PSOC™ Edge E84 Overview)

แหล่งอ้างอิงหลัก: [E84 product page](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84) · [Product Brief (PDF)](https://www.infineon.com/assets/row/public/documents/30/45/infineon-psoc-edge-e84-productbrief-en.pdf)

| โดเมน | องค์ประกอบหลัก | นึกถึงเมื่อ | อ่านเพิ่ม |
|---|---|---|---|
| High-Performance | Cortex-M55 (~400 MHz) + Helium DSP · Ethos-U55 NPU | แอปหลัก, DSP, inference สมรรถนะสูง, UI แอ็กทีฟ | [M55](https://developer.arm.com/Processors/Cortex-M55) · [Ethos-U55](https://developer.arm.com/Processors/Ethos-U55) |
| Low-Power | Cortex-M33 (~200 MHz) · NNLite | always-on, wake-word, งานประหยัดพลังงาน | [M33](https://developer.arm.com/Processors/Cortex-M33) |
| Memory (แนวเอกสารตระกูล) | System SRAM รวมสูงสุดราวหลาย MB · RRAM · หน่วยภายนอกบนคิต | บัฟเฟอร์เซ็นเซอร์/โมเดล/กราฟิก | Product Brief § Memory |
| Security / HMI | Secure Enclave · GPU/display · เสียง | ไม่ใช่ของแถม — ออกแบบคู่กับแอป | [E84 docs hub](https://documentation.infineon.com/psocedge/docs/eyv1750399809563) |

ตัวเลขขึ้นกับ SKU — ยึดเอกสารบอร์ดที่ใช้เป็นหลัก · คิตอ้างอิง: [KIT_PSE84_EVAL](https://www.infineon.com/evaluation-board/KIT-pse84-eval)

## Quick Task Mapping

| งาน | แนวทาง |
|---|---|
| LED / เมนู / control loop | M55 (แอป) |
| รอฟังตลอดคืน | M33 ± NNLite |
| โมเดล ML หนักบนอุปกรณ์ | Ethos-U55 (+ M55 ประสาน) |
| JSON / MQTT | แอปบนคอร์หลัก — ไม่ใช่ NPU |

---

## Software Layers (Course Teaching Model)

| ชั้น | คำถามช่วยเลือก | ตัวอย่าง |
|---|---|---|
| Hardware | ชิป/บอร์ดทำอะไรได้ | GPIO, I2C, NPU, วิทยุ |
| HAL / BSP | บอร์ดพร้อมรันหรือยัง | board init, clock, pin mux |
| Driver API | คุย peripheral ชิ้นไหน | GPIO, UART, I2C, SPI, PWM, ADC |
| Utility | มีงานช่วยซ้ำไหม | ring buffer, filter, log helper |
| Application | นโยบายคืออะไร | task, gesture policy, MQTT publish |

### Key Phrases

- **HAL/BSP เตรียมเวที**
- **Driver คุยกับฮาร์ดแวร์**
- **Utility ช่วยจัดของ**
- **Application ตัดสินใจและประสานระบบ**

---

## Relation to the ModusToolbox™ Stack (Summary)

อ่านคู่: [AN241775 (PDF)](https://www.infineon.com/assets/row/public/documents/30/42/infineon-an241775-getting-started-with-hal-psoc-edge-applicationnotes-en.pdf) · [mtb-dsl-pse8xxgp](https://github.com/Infineon/mtb-dsl-pse8xxgp)

```text
App → Middleware → BSP → Device Support (PDL / HAL / utilities) → Hardware
```

| ศัพท์ Infineon | ความหมายสั้น |
|---|---|
| BSP | แพ็กเกจเฉพาะบอร์ด |
| PDL | ไดรเวอร์ระดับต่ำของเพริเฟอรัล |
| HAL | ชั้นพกพา/ห่อสำหรับ middleware และพอร์ตข้ามแพลตฟอร์ม |
| Middleware | RTOS abstraction, connectivity, ML, กราฟิก ฯลฯ |

บน PSOC™ Edge รุ่นใหม่: ตั้งค่า/init เพริเฟอรัลมักผ่าน **Device Configurator + PDL** แล้วค่อยผูก HAL เมื่อ middleware ต้องการ

---

## Not the Same Layer

| คำ | ความหมาย | ลิงก์ |
|---|---|---|
| ModusToolbox™ / VS Code | เครื่องมือพัฒนา (IDE / toolchain) | [ModusToolbox™](https://www.infineon.com/modustoolbox) · [M02](../../../m02-toolchain/l01-modustoolbox-and-vscode/README.md) |
| TESA Firmware SDK | ชุดไลบรารี / API และแนวทางในหลักสูตร | [Lesson](../README.md) |
| DEEPCRAFT™ | เวิร์กโฟลว์โมเดล Edge AI | [DEEPCRAFT™ AI Suite](https://www.infineon.com/design-resources/embedded-software/deepcraft-edge-ai-solutions) |
| Digital Twin / host app | มุมมอง 3D / telemetry บนโฮสต์ที่คุยกับเฟิร์มแวร์ | [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) |

---

## Further Reading (one-click)

1. [PSOC™ Edge E84 product page](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84)  
2. [Product Brief (PDF)](https://www.infineon.com/assets/row/public/documents/30/45/infineon-psoc-edge-e84-productbrief-en.pdf)  
3. [AN241775 — HAL on PSOC™ Edge (PDF)](https://www.infineon.com/assets/row/public/documents/30/42/infineon-an241775-getting-started-with-hal-psoc-edge-applicationnotes-en.pdf)  
4. [AN235935 — Getting started on ModusToolbox™ (PDF)](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf)  
5. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** — คลังตัวอย่างโค้ดของหลักสูตร  
6. **[Bitstream Studio (Marketplace)](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** — VS Code host / digital twin เชื่อมเฟิร์มแวร์  
7. **[TESAIoT_Hackathon (GitHub)](https://github.com/drsanti/TESAIoT_Hackathon)** — HEX, Flasher, VSIX, web-app demos สำหรับแล็บ  

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [← Table of Contents](../../../README.md)
