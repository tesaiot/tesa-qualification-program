---
id: fw-sdk.m01.l01
lang: th
title:
  th: สถาปัตยกรรม MCU หลายโดเมนและชั้นของ Firmware SDK
  en: Multi-domain MCU Architecture and Firmware SDK Layers
summary:
  th: อ่านแผนที่ PSOC™ Edge E84 แบบหลายโดเมน และชั้นซอฟต์แวร์ HAL/BSP · Driver API · Utility · Application ก่อนเขียนโค้ดจริง
  en: Read the multi-domain map of PSOC™ Edge E84 and the HAL/BSP, Driver API, Utility and Application layers before writing real code.
level: L3
time_min:
  concept: 50
  practise: 15
  check: 10
hardware:
  emulator: false
  boards:
  - none
prerequisites: []
objectives:
- th: จับคู่งานผลิตภัณฑ์ 4 แบบ (UI, always-on sensing, inference หนัก, publish MQTT) กับโดเมน Cortex-M55 / Cortex-M33 + NNLite / Ethos-U55 ได้ถูกต้อง พร้อมเหตุผลข้อละหนึ่งประโยค
  en: Match four product workloads (UI, always-on sensing, heavy inference, MQTT publish) to the Cortex-M55, Cortex-M33 + NNLite or Ethos-U55 domain, with a one-sentence reason each.
- th: จำแนกทุกขั้นตอนของโจทย์ตัวอย่างว่าอยู่ชั้น HAL/BSP, Driver API, Utility หรือ Application
  en: Classify every step of a worked scenario as HAL/BSP, Driver API, Utility or Application.
- th: อธิบายความต่างระหว่าง SDK กับ IDE (ModusToolbox™ / VS Code) โดยยกตัวอย่างสิ่งที่อยู่ในแต่ละฝั่งได้อย่างน้อยฝั่งละหนึ่งอย่าง
  en: Explain how the SDK differs from the IDE (ModusToolbox™ / VS Code), giving at least one example of what belongs to each.
develops:
- skill: hw.architecture
  to: 2
- skill: build.vendor-sdk
  to: 1
- skill: ai.edge
  to: 1
context:
  platform: psoc-edge-e84
  lang: c
  ide: modustoolbox-vscode
  firmware: tesaiot-bitstream (HEX; source not public yet)
status: alpha
translation: done
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M01/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M01 — MCU Architecture and Firmware SDK Structure

**Course 1 · Module 1**  
**Suggested time:** ประมาณ 2.5–3 ชั่วโมง (อ่านละเอียด + ทำแบบฝึก)  
**Format:** บทเรียนเชิงแนวคิด — ยังไม่ต้อง flash บอร์ด (เริ่มลงมือกับเครื่องมือใน [M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md))

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/sdk-layer-cheatsheet.md) · [← Table of Contents](../../README.md) · [M02 →](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md)

> **หมายเหตุ: โค้ดในบทนี้เขียนสำหรับเฟิร์มแวร์ชุดใด** (ตรวจสอบเมื่อ 26 ก.ย. 2026)
>
> โค้ด C ในบทนี้เรียก API ของเฟิร์มแวร์ **TESAIoT Bitstream** ที่ต้นฉบับเรียกว่า “TESA Firmware SDK” ซึ่งเผยแพร่เป็นไฟล์ HEX สำเร็จรูป (`tesaiot-bitstream-<version>.hex`) คู่กับ Bitstream Studio ในแพ็กแล็บ [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/tree/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/hex) **ซอร์สโค้ดของเฟิร์มแวร์ชุดนี้ยังไม่เปิดเผยต่อสาธารณะ** ฟังก์ชันอย่าง `led_controller_*`, `cm55_button_*`, `sensor_*`, `cm55_adc_*` จึงยังไม่มี header ให้เปิดดูหรือนำไป build เอง ให้อ่าน snippet เป็นแนวคิดและลำดับการเรียกใช้ ส่วนการเรียก FreeRTOS และ Infineon PDL (เช่น `xTaskCreate`, `vTaskDelay`, `Cy_GPIO_*`) เป็น API สาธารณะตามปกติ
>
> ถ้าต้องการโค้ดที่อ่านและ build ได้จากซอร์สเปิด ให้ดู [tesaiot-pse84-devkit-sdk](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) (Apache-2.0) ซึ่งเป็น**คนละโค้ดเบสและตั้งชื่อ API ต่างกัน** ตัวอย่างที่ตรวจแล้วว่าทำงานเรื่องเดียวกับบทนี้ (commit `ef72c1b`):
>
> - [README ของ SDK](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/README.md) และโฟลเดอร์ [`bento-firmware-template-mtb-only/`](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/tree/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/) — โครงสร้างเฟิร์มแวร์แบบเปิดทั้งชุด (`bsps/` · `bento_libs/` · `proj_cm33_ns/` · `proj_cm55/`) ใช้เทียบกับแผนที่ชั้น HAL/BSP · Driver · Utility · Application ในบทนี้

---

## เป้าหมาย (Learning Outcomes)

เมื่อเรียนจบ คุณควรทำได้ดังนี้:

1. อธิบายได้ว่าทำไมงาน **Edge AI** จึงต้องการไมโครคอนโทรลเลอร์แบบหลายโดเมน (multi-domain)
2. อธิบายโครงสร้างระบบของ **[PSOC™ Edge E84](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84)** ในระดับผู้พัฒนาเฟิร์มแวร์ ได้แก่โดเมนประสิทธิภาพสูง (Cortex-M55 + Ethos-U55) และโดเมนพลังงานต่ำ (Cortex-M33 + NNLite) รวมถึงภาพรวมหน่วยความจำ HMI และความปลอดภัย
3. อธิบายองค์ประกอบหลักของ **TESA Firmware SDK** ในมุมเรียน ได้แก่ **HAL / BSP**, **Driver API** และ **Utility Modules** และเชื่อมโยงได้กับสแต็กซอฟต์แวร์ของ **[ModusToolbox™](https://www.infineon.com/modustoolbox)** (PDL, HAL, BSP, middleware)
4. จับคู่ “งานที่ต้องการทำ” กับ “โดเมนฮาร์ดแวร์ / ชั้นซอฟต์แวร์ที่ควรเรียกใช้” ได้ก่อนลงมือเขียนโค้ดในบทถัดไป

โมดูลนี้คือ **แผนที่ความคิด** ของทั้งหลักสูตรที่ 1 หากเข้าใจสถาปัตยกรรมชิปและชั้นซอฟต์แวร์แล้ว การติดตั้งเครื่องมือ ([M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md)) และการเรียก Driver API ([M03](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md)) จะมีโครงที่ชัด

> **หมายเหตุเกี่ยวกับตัวเลขสเปก**  
> ตัวเลขความถี่ หน่วยความจำ และฟีเจอร์ด้านล่างอ้างจากคู่มือ Infineon สำหรับตระกูล PSOC™ Edge E8x / E84 เช่น [Product Brief (PDF)](https://www.infineon.com/assets/row/public/documents/30/45/infineon-psoc-edge-e84-productbrief-en.pdf) และ [หน้าผลิตภัณฑ์ E84](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84)  
> ชิปย่อย (SKU) บนบอร์ดที่คุณใช้อาจต่างกันเล็กน้อย — ให้ยึดเอกสารของบอร์ด/ชิปที่ได้รับจริงเป็นหลัก และใช้ตัวเลขในบทนี้เป็น **กรอบความเข้าใจ** ไม่ใช่แทน datasheet ทั้งเล่ม

### Read alongside this chapter

| เอกสาร | ใช้เมื่อ |
|---|---|
| [PSOC™ Edge E84 product page](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84) | ภาพรวมฟีเจอร์และโดเมนประมวลผล |
| [PSOC™ Edge E84 documentation hub](https://documentation.infineon.com/psocedge/docs/eyv1750399809563) | อ่านเอกสารตระกูล Edge เพิ่ม |
| [PSOC™ Edge E84 Product Brief (PDF)](https://www.infineon.com/assets/row/public/documents/30/45/infineon-psoc-edge-e84-productbrief-en.pdf) | สเปกสรุป: M55/M33, NPU, memory, HMI, security |
| [PSOC™ Edge family overview](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm) | เปรียบเทียบตระกูล Edge ทั้งสาย |
| [KIT_PSE84_EVAL](https://www.infineon.com/evaluation-board/KIT-pse84-eval) | ชุดประเมินผลที่ใช้เรียน/ต้นแบบ |
| [AN241775 — Getting started with HAL on PSOC™ Edge (PDF)](https://www.infineon.com/assets/row/public/documents/30/42/infineon-an241775-getting-started-with-hal-psoc-edge-applicationnotes-en.pdf) | สแต็ก PDL / HAL / BSP / middleware |
| [AN235935 — Getting started with PSOC™ Edge on ModusToolbox™ (PDF)](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf) | เชื่อมไปเครื่องมือใน M02 |
| [mtb-dsl-pse8xxgp (Device Support Library)](https://github.com/Infineon/mtb-dsl-pse8xxgp) | ซอร์ส PDL/HAL ของตระกูล PSE8xx |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | คลังตัวอย่างโค้ด / flowchart / API Reference ของหลักสูตร (อ้างอิงหลัก) |
| **[Bitstream Studio (Marketplace)](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | Host app ใน VS Code — telemetry, Sensor Studio, digital twin เชื่อมเฟิร์มแวร์ |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | แพ็กแล็บ: HEX, VSIX, Flasher, web-app demos สำหรับฝึกปฏิบัติ |

---

## 1. From Traditional MCUs to Edge AI

### 1.1 What Traditional MCUs Do Well

ไมโครคอนโทรลเลอร์ (MCU) ถูกใช้เป็นตัวควบคุมอุปกรณ์มานาน เช่น

- อ่านสวิตช์ / เซ็นเซอร์ง่าย ๆ
- ขับ LED, มอเตอร์, รีเลย์
- สื่อสารผ่าน UART / I²C / SPI
- รันลูปควบคุมที่คาดพฤติกรรมได้

งานเหล่านี้มักอยู่บนคอร์เดียว มีหน่วยความจำจำกัด และไม่ต้องการเร่งโมเดล Machine Learning บนชิป

### 1.2 What Changes with Edge AI

ผลิตภัณฑ์อัจฉริยะสมัยใหม่มักต้องการมากกว่า “อ่านค่าแล้วส่งขึ้นคลาวด์”:

| ความต้องการ | ตัวอย่างในผลิตภัณฑ์ |
|---|---|
| ประมวลผลใกล้แหล่งข้อมูล | รู้ว่ามีคำสั่งเสียง / ท่าทาง โดยไม่ส่งเสียงดิบตลอดเวลา |
| ตอบสนองเร็ว (latency ต่ำ) | UI หรือ safety interlock ที่ต้องตอบในหน่วยมิลลิวินาที |
| ใช้พลังงานอย่างมีวินัย | รอฟังตลอดคืนบนแบตเตอรี่ |
| ความเป็นส่วนตัว | ข้อมูลดิบบางส่วนไม่ต้องออกนอกอุปกรณ์ |
| ทนเมื่อเน็ตหลุด | ฟังก์ชันหลักยังทำงานได้แม้คลาวด์ชั่วคราวใช้ไม่ได้ |

แนวคิดนี้เรียกว่า **Edge AI** — การนำปัญญาประดิษฐ์หรือการเรียนรู้ของเครื่อง (Machine Learning) ไปทำงานใกล้แหล่งข้อมูล

### 1.3 Why a Single Core Is Often Not Enough

ถ้าบังคับงานทุกอย่างไว้บน CPU เดียว คุณจะเจอข้อขัดแย้งบ่อย ๆ เช่น

- ต้องการ inference หนัก → ต้อง clock สูง → กินพลังงานมาก
- ต้องการ always-on sensing → ต้องตื่นบ่อย → กับงบพลังงานชนกัน
- ต้องการ UI/กราฟิก + เซ็นเซอร์ + เครือข่ายพร้อมกัน → แย่งเวลา CPU กัน

ดังนั้น MCU ยุค Edge AI จึงออกแบบเป็น **หลายโดเมน** — แยกงานสมรรถนะสูง ออกจากงานพลังงานต่ำ และแยกตัวเร่ง Neural Network ออกจากคอร์ทั่วไป

หลักสูตรนี้ไม่ได้สอนแค่ “เขียน C ให้บอร์ดทำงาน” แต่สอนให้มอง **สถาปัตยกรรมชิป + ชั้นซอฟต์แวร์ SDK** เป็นระบบเดียวกัน

---

## 2. Course Platform: PSOC™ Edge E84

**TESA Firmware SDK** ในหลักสูตรนี้รองรับการพัฒนาบนตระกูล **[Infineon PSOC™ Edge](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm)** โดยใช้ **[PSOC™ Edge E84](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84)** เป็นกรณีศึกษาหลัก

อ่านสรุปสถาปัตยกรรมได้จาก [Product Brief (PDF)](https://www.infineon.com/assets/row/public/documents/30/45/infineon-psoc-edge-e84-productbrief-en.pdf) และ [เอกสารตระกูลบน Infineon documentation](https://documentation.infineon.com/psocedge/docs/eyv1750399809563)

### 2.1 Why This Family Fits Edge AI Learning

ตามเอกสารผลิตภัณฑ์ของ Infineon ตระกูล E84 ถูกวางเป็น MCU ที่รวม:

- สมรรถนะสูงสำหรับแอปและ ML ขั้นสูง — [Arm® Cortex®-M55](https://developer.arm.com/Processors/Cortex-M55) + [Ethos™-U55](https://developer.arm.com/Processors/Ethos-U55)
- โดเมนพลังงานต่ำสำหรับ always-on — [Arm® Cortex®-M33](https://developer.arm.com/Processors/Cortex-M33) + Infineon NNLite
- อินเทอร์เฟซ HMI (กราฟิก / เสียง) ในระดับชิป
- ความปลอดภัยระดับอุตสาหกรรม (เช่น Edge Protect / PSA ตามระดับที่ชิปรองรับ)
- ระบบนิเวศเครื่องมือ **[ModusToolbox™](https://www.infineon.com/modustoolbox)** และโซลูชัน ML อย่าง **[DEEPCRAFT™](https://www.infineon.com/design-resources/embedded-software/deepcraft-edge-ai-solutions)**

จุดนี้สำคัญต่อหลักสูตร: คุณจะได้ฝึกทั้งการควบคุม I/O แบบเฟิร์มแวร์คลาสสิก และการเตรียมทางไปยังงาน Edge AI / connectivity ในบทหลัง โดยไม่ต้องเปลี่ยนแพลตฟอร์มกลางคัน

ชุดประเมินผลอ้างอิง: **[KIT_PSE84_EVAL](https://www.infineon.com/evaluation-board/KIT-pse84-eval)** (ใช้ตามบอร์ดที่มี)

### 2.2 What to Focus on in M01 (and What to Skip for Now)

| โฟกัสใน M01 | ยังไม่จำเป็นใน M01 |
|---|---|
| มีโดเมนอะไรบ้าง และเหมาะกับงานแบบใด | จำ register map ทั้งชิป |
| ซอฟต์แวร์คุยกับฮาร์ดแวร์ผ่านชั้นไหน | ตั้งค่า Device Configurator ครบทุกหน้าจอ |
| ความสัมพันธ์ระหว่าง SDK กับ IDE | Flash Hello World (อยู่ใน M02) |
| ภาพรวมหน่วยความจำ / ความปลอดภัย / HMI | เขียนโมเดล ML เองทั้งหมด |

> **จำประโยคนี้ไว้**  
> ใน M01 คุณไม่ต้องท่อง datasheet ทั้งเล่ม  
> ให้ตอบได้ว่า “งานนี้ควรอยู่โดเมนไหน” และ “โค้ดนี้ควรอยู่ชั้นซอฟต์แวร์ไหน”

---

## 3. PSOC™ Edge Multi-Domain Architecture

Infineon อธิบาย PSOC™ Edge ว่าเป็นสถาปัตยกรรม **multi-domain** เพื่อสมดุลระหว่างสมรรถนะสูงกับการใช้พลังงานแบบละเอียด (fine-grained power optimization) — ดูสรุปได้จาก [E84 product page](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84) และ [Product Brief (PDF)](https://www.infineon.com/assets/row/public/documents/30/45/infineon-psoc-edge-e84-productbrief-en.pdf)

ในภาพรวมมีอย่างน้อยสองโดเมนหลักที่ผู้เรียนเฟิร์มแวร์ต้องรู้จัก:

### 3.1 High-Performance Domain

| องค์ประกอบ | บทบาทโดยสรุป | อ่านเพิ่ม |
|---|---|---|
| **Arm® Cortex®-M55** | คอร์แอปหลัก ความถี่สูงสุดราว **400 MHz** มี Helium™ DSP และ FPU | [Cortex-M55](https://developer.arm.com/Processors/Cortex-M55) · [Helium](https://developer.arm.com/Architectures/Helium) |
| **Arm® Ethos™-U55 NPU** | ตัวเร่ง Neural Network สำหรับงาน ML ขั้นสูง ความถี่สูงสุดราว **400 MHz** (เอกสารระบุราว 128 MAC/cycle) | [Ethos-U55](https://developer.arm.com/Processors/Ethos-U55) |

เหมาะกับงานเช่น:

- ตรรกะผลิตภัณฑ์หลัก / control loop
- preprocessing สัญญาณ (DSP)
- inference ที่ต้องการสมรรถนะสูง
- ประสานงานกับกราฟิก / connectivity ในโหมดแอ็กทีฟ

### 3.2 Low-Power Domain

| องค์ประกอบ | บทบาทโดยสรุป | อ่านเพิ่ม |
|---|---|---|
| **Arm® Cortex®-M33** | คอร์พลังงานต่ำ ความถี่สูงสุดราว **200 MHz** | [Cortex-M33](https://developer.arm.com/Processors/Cortex-M33) |
| **Infineon NNLite** | ตัวเร่ง Neural Network แบบใช้พลังงานต่ำสำหรับ Always-On AI/ML | [E84 product overview](https://documentation.infineon.com/psocedge/docs/eyv1750399809563) |

เหมาะกับงานเช่น:

- always-on sensing / wake word / acoustic activity detection
- งานที่ต้องทำงานต่อเนื่องโดยประหยัดพลังงาน
- เฝ้าระวังเงื่อนไขแล้วค่อย “ปลุก” โดเมนสมรรถนะสูงเมื่อจำเป็น

### 3.3 Simple Data-Flow View

```text
เซ็นเซอร์ / ไมโครโฟน / ปุ่ม
        │
        ├──────────────► Low-Power Domain
        │                Cortex-M33 + NNLite
        │                (always-on / wake / low-power ML)
        │                      │
        │                      │ ปลุก / ส่งเหตุการณ์
        │                      ▼
        └──────────────► High-Performance Domain
                         Cortex-M55 (+ Helium DSP)
                                │
                                ├──────────────► Ethos-U55 NPU (advanced inference)
                                │
                                ├──────────────► HMI (กราฟิก / เสียง) ตามงาน
                                │
                                └──────────────► Connectivity (เช่น Wi-Fi / MQTT ในบทหลัง)
```

> **Key phrase**  
> อย่าท่องแค่ชื่อคอร์ — ให้ตอบได้ว่า *งานนี้ควรอยู่โดเมนไหน และทำไม*

### 3.4 Task-to-Domain Mapping (Design Time)

| ประเภทงาน | โดเมนที่มักเหมาะสม | เหตุผลสั้น ๆ |
|---|---|---|
| UI / เมนู / ควบคุม LED จากสถานะแอป | High-Performance (M55) | เป็นตรรกะผลิตภัณฑ์หลัก |
| รอฟังเสียงเบา ๆ ทั้งคืน | Low-Power (M33 ± NNLite) | งบพลังงานสำคัญกว่า throughput |
| โมเดล gesture / vision ขั้นสูงบนอุปกรณ์ | Ethos-U55 (+ แอปบน M55 ประสาน) | ต้องการเร่ง ML |
| จัด JSON แล้ว publish MQTT | แอปบนคอร์หลัก (มัก M55) | เป็นโปรโตคอล/นโยบาย ไม่ใช่หน้าที่ NPU |
| กรองสัญญาณเบา ๆ ก่อนส่งเข้าโมเดล | M55 (DSP/Helium) หรือ utility บนแอป | preprocessing ไม่เท่ากับ inference |

### 3.5 Common Misconceptions

| ความเข้าใจผิด | ความจริง |
|---|---|
| มี NPU แล้วไม่ต้องเขียนเฟิร์มแวร์ควบคุม I/O | NPU เร่ง inference — การอ่านเซ็นเซอร์และสั่ง actuator ยังเป็นงานของแอป + driver |
| ทุกอย่างควรรันบน Cortex-M55 | งาน always-on ควรพิจารณาโดเมนพลังงานต่ำ |
| Edge AI = ส่งข้อมูลดิบขึ้นคลาวด์ตลอด | ตรงข้าม — มุ่งประมวลผลที่ขอบก่อน |
| NNLite กับ Ethos-U55 ใช้แทนกันได้ทุกงาน | คนละจุดประสงค์: always-on ประหยัดพลังงาน vs ML สมรรถนะสูง |
| ต้องเลือกโดเมนให้ถูกตั้งแต่บรรทัดแรกของ Hello World | M01 สอนแผนที่ — การมอบหมาย task จริงจะชัดขึ้นใน M04–M05 |

### 3.6 Think Before the Lab

เลือกโดเมนที่เหมาะสมที่สุดสำหรับแต่ละงาน:

1. กระพริบ LED ตามสถานะเมนูบนจอ  
2. ฟังคำปลุก (wake-word) แบบใช้พลังงานต่ำตลอดคืน  
3. รันโมเดลรู้จำท่าทางบนอุปกรณ์  
4. จัด JSON แล้ว publish ขึ้น broker  

แนวทาง: (1) M55 · (2) M33 / NNLite · (3) Ethos-U55 (+ M55 ประสาน) · (4) แอปบนคอร์หลัก  
รายละเอียดอยู่ใน [แล็บ](../l02-lab/README.md)

---

## 4. SoC Memory and On-Chip Connectivity (Developer Overview)

ผู้เรียนเฟิร์มแวร์ไม่จำเป็นต้องท่องทุกช่วงแอดเดรส แต่ควรรู้ว่า “ความจำมีหลายชั้น” และแต่ละชั้นมีผลต่อ latency / พลังงาน / ขนาดโมเดล

### 4.1 Memory Overview from E8x Family Documents

เอกสารผลิตภัณฑ์ของตระกูลระบุแนวประมาณดังนี้ (ขึ้นกับรุ่นย่อย — ตรวจใน [Product Brief](https://www.infineon.com/assets/row/public/documents/30/45/infineon-psoc-edge-e84-productbrief-en.pdf)):

| ทรัพยากร | บทบาทในมุมนักพัฒนา |
|---|---|
| **System SRAM** (รวมแล้วสูงสุดราวหลาย MB; เอกสาร E84 มักพูดถึงราว **6 MB** รวมโดเมน) | ที่เก็บโค้ด/ข้อมูล/บัฟเฟอร์กราฟิกหรือ ML ในโหมดแอ็กทีฟ |
| **SRAM ในโดเมน Low-Power** (เอกสารระบุราว 1 MB ในบางสรุปสถาปัตยกรรม) | รองรับงาน always-on โดยไม่ต้องเปิดทรัพยากรทั้งหมด |
| **TCM / cache ของ Cortex-M55** | ลด wait-state สำหรับโค้ดและข้อมูลวิกฤต |
| **RRAM** (เอกสารระบุราว 512 KB ในหลายรุ่น) | หน่วยไม่ลบเลือนใช้พลังงานต่ำ สำหรับเก็บข้อมูล/เฟิร์มแวร์บางส่วนตามการออกแบบระบบ |
| **Boot ROM** | โค้ดบูตของชิป |
| **หน่วยความจำภายนอกผ่าน SMIF / Octal / QSPI** (บนชุดประเมินผล) | ขยายโค้ด/โมเดล/แอสเซ็ตเมื่อ SRAM ในชิปไม่พอ |

### 4.2 Why Memory Matters for Edge AI

- โมเดล ML และบัฟเฟอร์เซ็นเซอร์แย่ง SRAM กัน  
- กราฟิก HMI กินหน่วยความจำและแบนด์วิดท์บัส  
- การเลือกเก็บน้ำหนักโมเดลใน RRAM / flash ภายนอกมีผลต่อเวลาบูตและพลังงาน  

ในหลักสูตรนี้ คุณจะสัมผัสผลจริงเมื่อจัด buffer ใน M05 และเมื่อเชื่อม UI/telemetry ในบทหลัง — M01 แค่ปูแผนที่

### 4.3 Peripherals and Interfaces Common in Edge / IoT Work

เอกสารตระกูลระบุชุดเพริเฟอรัลที่หลากหลาย ซึ่งในหลักสูตรจะค่อยฝึกทีละกลุ่ม:

| กลุ่ม | ตัวอย่าง | จะเน้นในบท |
|---|---|---|
| GPIO / Timer / PWM / ADC | ปุ่ม ไฟ มอเตอร์ อ่านอนาล็อก | [M03](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md) |
| UART / I²C / SPI / I3C | ดีบักคอนโซล เซ็นเซอร์ บัสความเร็วสูง | [M03](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md), M05 |
| USB / SD / Ethernet / CAN (ตามรุ่น) | เชื่อมต่อระบบ | เสริมตามความสนใจ |
| เสียง (PDM/I2S/TDM), กราฟิก (2.5D GPU, MIPI-DSI/DBI) | HMI | ภาพรวมใน M01; ลงมือตามชุดบอร์ด |
| วิทยุภายนอกบนคิต (เช่น Wi-Fi/Bluetooth บน Evaluation Kit) | Cloud / local radio | [M06 MQTT](../../m06-mqtt/l01-mqtt-and-mqtts/README.md) · [M07 BLE](../../m07-ble/l01-ble-connectivity/README.md) |

---

## 5. HMI, Audio, Graphics, and Security (Overview)

### 5.1 Human–Machine Interface (HMI)

PSOC™ Edge E84 ถูกวางให้รองรับ HMI ที่ซับซ้อนขึ้นกว่า MCU ทั่วไป เช่น (สรุปจาก [Product Brief](https://www.infineon.com/assets/row/public/documents/30/45/infineon-psoc-edge-e84-productbrief-en.pdf)):

- กราฟิกความละเอียดสูงในระดับที่เอกสารระบุ (เช่น เส้นทาง display ถึงราว 1024×768)
- 2.5D GPU และอินเทอร์เฟซจอ (MIPI-DSI / DBI ตามรุ่น)
- อินเทอร์เฟซไมโครโฟนหลายช่องและฟีเจอร์อย่าง Acoustic Activity Detection / wake-word ในบริบทพลังงานต่ำ

อ่านลึกเมื่อพร้อม (ไม่บังคับใน M01): รายการ application notes บน [PSOC™ Edge application notes](https://documentation.infineon.com/psocedge/docs/umo1761464512847) เช่น AN239191 (graphics) และ AN237939 (high-performance graphics / low power)

สำหรับหลักสูตรเฟิร์มแวร์: ให้เข้าใจว่า **HMI ไม่ได้อยู่นอกชิปเสมอไป** — บางส่วนเป็นบล็อกใน SoC ที่แอปต้องจัดทรัพยากรและพลังงานให้สอดคล้องกับโดเมนประมวลผล

### 5.2 Security at the Architecture Level

เอกสาร Infineon ระบุทิศทางความปลอดภัยระดับสูง เช่น

- Secure Enclave / lockstep ในโดเมนพลังงานต่ำ (ตามรุ่น)
- Secure Boot และที่เก็บคีย์
- แนวทาง Infineon Edge Protect / ระดับ PSA ตาม SKU
- ไลบรารีและบริการเข้ารหัสใน ecosystem (รวมแนวทาง Trusted Firmware-M ในบางเอกสาร)

จุดเริ่มค้นคว้า: [AN237849 — Getting started with PSOC™ Edge security](https://documentation.infineon.com/psocedge/docs/umo1761464512847) (ดูรายการ application notes) และสรุป security ใน Product Brief

ในหลักสูตรนี้:

| บท | สิ่งที่คาดหวัง |
|---|---|
| **M01** | รู้ว่าความปลอดภัยเป็นส่วนหนึ่งของสถาปัตยกรรมชิป ไม่ใช่ของแถม |
| **M06** | ลงรายละเอียด MQTT over TLS, ใบรับรอง และการยืนยันตัวตนในทางปฏิบัติ |

---

## 6. Evaluation Kits

Infineon มีคิตอย่างน้อยสองแนวทางที่พบบ่อยในการเริ่มต้นกับ E84:

| คิต | จุดประสงค์โดยสรุป | ลิงก์ |
|---|---|---|
| **KIT_PSE84_EVAL** (PSOC™ Edge E84 Evaluation Kit) | แพลตฟอร์มประเมินผลทั่วไป เข้าถึงอินเทอร์เฟซได้กว้าง เหมาะกับ rapid prototyping | [KIT_PSE84_EVAL](https://www.infineon.com/evaluation-board/KIT-pse84-eval) · [Kit guide](https://documentation.infineon.com/psocedge/docs/lne1762692969598) |
| **KIT_PSEA84** (PSOC™ Edge E84 AI Kit) | แนวทางต้นทุนต่ำกว่าสำหรับงาน Edge AI ตามที่ Infineon นำเสนอ | ดูบน [E84 product page](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84) |

### 6.1 Typical Evaluation Kit Features (Overview)

จากหน้าผลิตภัณฑ์คิต (รายละเอียดขึ้นกับรุ่นฮาร์ดแวร์ที่ถือ):

- ชิป PSOC™ Edge E84
- โปรแกรมเมอร์/ดีบักเกอร์บนบอร์ด (เช่น KitProg)
- หน่วยความจำภายนอก (QSPI / Octal flash / RAM ตามคิต)
- ไมโครโฟน / ลำโพง / จอ / กล้อง (บนคิตที่เน้น HMI)
- โมดูลไร้สาย เช่น AIROC™ Wi-Fi & Bluetooth® บนบางคิต
- หัวต่อขยาย (Arduino / mikroBUS / อื่น ๆ ตามคิต)

### 6.2 Product Directions That Match This Course

- บ้านอัจฉริยะ — เสียง / ท่าทาง / เทอร์โมสตัท
- สวมใส่ได้ — always-on sensing ใช้พลังงานต่ำ
- หุ่นยนต์ขนาดเล็ก — รับรู้บริบทในขอบเขตจำกัด
- ล็อก / ความปลอดภัย — ยืนยันตัวตนระดับอุปกรณ์
- Industrial HMI — จอและอินพุตท้องถิ่น

---

## 7. Software Ecosystem: From ModusToolbox™ to TESA Firmware SDK

ก่อนเข้าสู่ “HAL / Driver API / Utility” ในภาษาของหลักสูตร ควรเห็นภาพสแต็กจริงของ Infineon ที่ SDK และโปรเจกต์ตัวอย่างยืนอยู่บนนั้น  
อ่านคู่กับ [AN241775 (HAL on PSOC™ Edge)](https://www.infineon.com/assets/row/public/documents/30/42/infineon-an241775-getting-started-with-hal-psoc-edge-applicationnotes-en.pdf) และ [mtb-dsl-pse8xxgp](https://github.com/Infineon/mtb-dsl-pse8xxgp)

### 7.1 Software Layers in ModusToolbox™ (from Infineon Docs)

เอกสารอย่าง AN241775 และคู่มือ [ModusToolbox™](https://www.infineon.com/modustoolbox) วางภาพคร่าว ๆ ดังนี้:

```text
Applications / Code Examples / Reference Designs
        │
        ▼
Middleware libraries
(Graphics, ML, Wi-Fi/Bluetooth, CAPSENSE, Voice, Security, …)
        │
        ▼
Board Support Packages (BSP)
        │
        ▼
Device Support Library
  ├── Peripheral Driver Library (PDL)
  ├── Hardware Abstraction Layer (HAL)
  ├── Device Utilities
  └── Device Information
        │
        ▼
Hardware (PSOC™ Edge)
```

ความหมายสั้น ๆ:

| ชิ้นส่วน | ทำอะไร |
|---|---|
| **BSP** | โค้ดและคอนฟิกเฉพาะบอร์ด — init บอร์ด, แมปขา, ไลบรารีที่บอร์ดต้องการ |
| **PDL** | API ระดับต่ำของเพริเฟอรัล + header/startup ของชิป — ใกล้ฮาร์ดแวร์ |
| **HAL** | ชั้นพกพาที่ห่อ PDL; บน PSOC™ Edge รุ่นใหม่ Infineon เน้นให้ HAL รองรับ middleware และให้การตั้งค่าเพริเฟอรัลชัดขึ้นผ่าน **Device Configurator + PDL** |
| **Middleware** | สแต็กสำเร็จรูป (RTOS abstraction, connectivity, ML, กราฟิก ฯลฯ) |
| **Application** | โค้ดผลิตภัณฑ์ของคุณ |

> สำหรับ PSOC™ Edge: ลำดับที่เอกสารแนะนำบ่อยคือ  
> **ตั้งค่า/init เพริเฟอรัลด้วย PDL (และคอนฟิกิวเรเตอร์) → ผูกวัตถุ HAL เมื่อ middleware ต้องการ → middleware/แอปใช้งานต่อ**

### 7.2 Where TESA Firmware SDK Fits

**TESA Firmware SDK** ในหลักสูตรนี้คือชุดความรู้และ API ที่จัดให้ผู้เรียนพัฒนาผลิตภัณฑ์ TESAIoT / Edge AI บนแพลตฟอร์มข้างต้นอย่างเป็นระบบ

ในภาษาของบทเรียน เราจัดกลุ่มเป็นสามแกนที่ผู้เรียนต้องเข้าใจชัดก่อนลงมือเขียนโค้ด:

| ศัพท์ในหลักสูตร | สิ่งที่มักสัมพันธ์ในสแต็กจริง | ผู้เรียนทำอะไร |
|---|---|---|
| **HAL / BSP** | BSP + การ bring-up / นามธรรมบอร์ด (+ บริบท HAL ของแพลตฟอร์ม) | เลือกบอร์ด เรียก init ตามคู่มือโปรเจกต์ |
| **Driver API** | ทางเข้าควบคุมเพริเฟอรัลที่หลักสูตรให้ใช้เป็นมาตรฐาน (อยู่บน PDL/HAL/ไดรเวอร์ของ SDK ตามเวอร์ชันที่ใช้) | อ่าน/เขียน GPIO, UART, I2C, SPI, PWM, ADC |
| **Utility Modules** | โมดูลช่วยที่ใช้ซ้ำในโปรเจกต์ตัวอย่าง/ผลิตภัณฑ์ | buffer, filter เบา ๆ, logging helper |

และชั้นที่สี่ที่คุณเขียนเองเสมอ:

| ชั้น | ความหมาย |
|---|---|
| **Application** | นโยบายผลิตภัณฑ์, task, การตัดสินใจ, การเรียกใช้ชั้นด้านล่าง |

### 7.3 SDK Is Not the IDE

| คำ | คืออะไร | อ่านเพิ่ม |
|---|---|---|
| **ModusToolbox™ / VS Code** | เครื่องมือพัฒนา (สร้างโปรเจกต์, จัดการไลบรารี, เขียนโค้ด, build, debug) | [M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md) · [ModusToolbox™](https://www.infineon.com/modustoolbox) |
| **TESA Firmware SDK** | ชุดซอฟต์แวร์/API และแนวทางที่โค้ดของคุณเรียกใช้ในหลักสูตร | หมวด 8 ในบทนี้ |
| **Device Support Library** | แพ็กเกจรองรับชิปจาก Infineon (PDL/HAL/utilities) | [mtb-dsl-pse8xxgp](https://github.com/Infineon/mtb-dsl-pse8xxgp) |
| **DEEPCRAFT™** | เวิร์กโฟลว์โมเดล ML สำหรับ Edge (ภาพรวมใน M01; ลงรายละเอียดในบท Sensor/AI) | [DEEPCRAFT™](https://www.infineon.com/design-resources/embedded-software/deepcraft-edge-ai-solutions) |
| **Digital Twin** | มุมมองจำลอง / 3D บนโฮสต์ (หลักสูตร Digital Twin เต็มรูปแบบอยู่คนละคอร์ส) — เครื่องมือโฮสต์ที่ใช้ร่วมกับเฟิร์มแวร์คือ **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | [Marketplace](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) |

จำให้ขึ้นใจ: **ติดตั้ง IDE ได้ ≠ เข้าใจ SDK แล้ว**

---

## 8. Core SDK Building Blocks: HAL/BSP, Driver API, Utility

### 8.1 Bottom-Up Software Layers (Course Teaching Model)

```text
+--------------------------------------------------+
| Application / Product Logic                      |
| (นโยบายผลิตภัณฑ์, task, การตัดสินใจ)              |
+--------------------------------------------------+
| Utility Modules                                  |
| (buffer, helper, logging, งานช่วยที่ใช้ซ้ำ)         |
+--------------------------------------------------+
| Driver API                                       |
| (GPIO, UART, I2C, SPI, PWM, ADC, …)              |
+--------------------------------------------------+
| HAL / BSP                                        |
| (board bring-up, clocks, pin mux, นามธรรมบอร์ด)   |
+--------------------------------------------------+
| Hardware                                         |
| (PSOC™ Edge E84 + อุปกรณ์บนชุดประเมินผล)           |
+--------------------------------------------------+
```

### 8.2 BSP / HAL — Prepare the Stage

**Board Support Package (BSP)** ทำให้โปรเจกตรู้ว่ากำลังรันบนบอร์ดใด ขาใดต่ออะไร และต้องดึงไลบรารีใด

**Hardware Abstraction Layer (HAL)** ในระบบนิเวศ Infineon ช่วยให้ชั้นบนพูดภาษาที่พกพากว่าการแตะ register ตรง ๆ  
บน PSOC™ Edge รุ่นใหม่ เอกสารเน้นว่าการตั้งค่าและ init เพริเฟอรัลจำนวนมากทำผ่าน **configurator + PDL** ส่วน HAL ถูกใช้ร่วมกับ middleware อย่างมีเป้าหมาย

ในหลักสูตรนี้ คุณมักจะ:

1. สร้าง/เปิดโปรเจกต์จาก BSP ของคิต  
2. เรียก init ตามตัวอย่างของโปรเจกต์ หรือตัวอย่างบน **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**  
3. ไม่เริ่มจาก “เขียน register ทีละบิต” ในแบบฝึกมาตรฐาน

### 8.3 Driver API — Talk to Hardware

**Driver API** คือทางเข้าหลักสำหรับควบคุมอุปกรณ์ต่อพ่วงในแนวทางของหลักสูตร

ตัวอย่างงาน:

- GPIO — LED / ปุ่ม / สัญญาณควบคุม
- UART — log และโปรโตคอลข้อความ
- I²C / SPI — เซ็นเซอร์และหน่วยความจำภายนอก
- PWM / ADC — ขับสัญญาณและอ่านอนาล็อก
- Timer — จังหวะเวลา

กฎของหลักสูตร: **เรียก Driver API ของ SDK ตามเวอร์ชันที่ใช้** ไม่ข้ามไปเขียน register โดยตรง เว้นแต่บทนั้นระบุชัด

ชื่อฟังก์ชันจริงขึ้นกับเวอร์ชันที่ล็อกในโปรเจกต์ของคุณ — M01 โฟกัสบทบาทของชั้น ส่วนรายละเอียดเรียกใช้พร้อม snippet จริงจะฝึกใน **[M03](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md)** (เช่น `led_controller_*`, `cm55_button_*`, `sensor_*`, `cm55_adc_*`) และ RTOS ใน M04 (`xTaskCreate`, `vTaskDelay`, …)

### 8.4 Utility Modules — Helpers

**Utility Modules** ไม่แทน Driver แต่ช่วยงานซ้ำ ๆ เช่น

- ring buffer / queue เบา ๆ ในระดับแอป
- filter / smoothing เบื้องต้น
- logging helper
- ฟังก์ชันจัดรูปข้อมูลที่ใช้ร่วมหลายโมดูล

กฎง่าย ๆ: **Utility จัดของ — Driver คุยกับฮาร์ดแวร์ — Application ตัดสินใจ**

### 8.5 Application — Product Policy

ชั้นแอปคือที่ที่คุณเขียน เช่น

- เมื่อค่าเซ็นเซอร์เกินเกณฑ์ให้กระพริบไฟ
- เมื่อได้ผล inference แล้วเปลี่ยนโหมด
- เมื่อไรจะ publish ขึ้นคลาวด์ (รายละเอียดใน M06)
- จะปลุกโดเมนสมรรถนะสูงเมื่อใดหลังเหตุการณ์จากโดเมนพลังงานต่ำ

### 8.6 Quick Decision Table

| คำถามที่คุณถามตัวเอง | ชั้นที่น่าจะเกี่ยวข้อง |
|---|---|
| บอร์ดพร้อมรันหรือยัง นาฬิกาและขาตั้งแล้วหรือยัง | HAL / BSP |
| จะคุยกับ peripheral ชิ้นไหน | Driver API |
| มีงานช่วยที่ใช้ซ้ำหลายที่ไหม | Utility |
| นโยบายผลิตภัณฑ์คืออะไร ใครตัดสินใจ | Application |
| ต้องการสแต็กสำเร็จรูป (เช่น RTOS abstraction, Wi-Fi) | Middleware (ผ่านเครื่องมือ/ไลบรารีใน M02 เป็นต้นไป) |

แผ่นสรุปหนึ่งหน้า: [sdk-layer-cheatsheet.md](resources/sdk-layer-cheatsheet.md)

### 8.7 Worked Scenarios

#### Scenario A — Temperature Threshold

โจทย์: อ่านอุณหภูมิผ่าน I²C ทุก 1 วินาที ถ้าเกินเกณฑ์ให้เปิด LED และพิมพ์ข้อความทาง UART

| ขั้นตอน | ชั้น |
|---|---|
| เริ่มต้นบอร์ดและขา I²C / LED / UART | HAL / BSP |
| อ่าน I²C, เขียน GPIO, ส่ง UART | Driver API |
| เก็บตัวอย่างล่าสุด N ค่า / ค่าเฉลี่ยเคลื่อนที่ | Utility |
| เปรียบเทียบเกณฑ์ เปลี่ยนสถานะผลิตภัณฑ์ | Application |

#### Scenario B — Always-On Then Heavy Inference

โจทย์: รอจับ Acoustic Activity บนโดเมนพลังงานต่ำ เมื่อมีเหตุการณ์ค่อยปลุกโดเมนสมรรถนะสูงเพื่อรันโมเดลบน Ethos-U55 แล้วอัปเดต UI

| ขั้นตอน | โดเมน / ชั้น |
|---|---|
| รอฟัง / ตรวจกิจกรรมเสียง | Low-Power Domain (M33 ± NNLite) |
| ปลุกและส่งเหตุการณ์ | Application policy + inter-domain path ตามดีไซน์ระบบ |
| preprocessing / จัดหน้าต่างข้อมูล | Utility + แอปบน M55 |
| inference หนัก | Ethos-U55 |
| อัปเดตจอ / LED / ส่งสรุปขึ้นคลาวด์ | Application (+ connectivity ใน M06) |

---

## 9. Development Tools and ML Workflow (Preview)

### 9.1 Tools You Will Use in M02

| เครื่องมือ | บทบาท | อ่านเพิ่ม |
|---|---|---|
| **ModusToolbox™** | สร้างโปรเจกต์ จัดการ BSP/library, configurator | [ModusToolbox™](https://www.infineon.com/modustoolbox) · [M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md) |
| **Visual Studio Code** | เขียนโค้ด build และ debug (ร่วมกับส่วนขยาย/เวิร์กโฟลว์ที่เลือกใช้) | [VS Code](https://code.visualstudio.com/) · [VS Code for ModusToolbox™](https://documentation.infineon.com/modustoolbox/docs/visual-studio-code-for-modustoolbox-user-guide) |
| **KitProg / SWD debugger** | flash และไล่บั๊กบนฮาร์ดแวร์จริง | [AN235935 (PDF)](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf) |
| **Library Manager / Project Creator** | เลือกและอัปเดตไลบรารีในโปรเจกต์ | [Tools package user guide (PDF)](https://www.infineon.com/assets/row/public/documents/30/68/infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf) |

เอกสารเริ่มต้นที่เป็นประโยชน์จาก Infineon (อ่านเสริมได้):

- [AN235935 — Getting started with PSOC™ Edge on ModusToolbox™ (PDF)](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf)
- [AN241775 — Getting started with HAL on PSOC™ Edge (PDF)](https://www.infineon.com/assets/row/public/documents/30/42/infineon-an241775-getting-started-with-hal-psoc-edge-applicationnotes-en.pdf)
- [PSOC™ Edge quick start guide](https://documentation.infineon.com/modustoolbox/docs/psoc-edge-quick-start-guide)

### 9.2 DEEPCRAFT™ (Overview)

**[DEEPCRAFT™](https://www.infineon.com/design-resources/embedded-software/deepcraft-edge-ai-solutions)** เป็นโซลูชัน/สตูดิโอฝั่ง Infineon สำหรับเวิร์กโฟลว์โมเดล Edge AI ตั้งแต่การเตรียมข้อมูลไปจนถึงการนำโมเดลไปใช้บนอุปกรณ์

ในหลักสูตรนี้:

- M01: รู้ว่ามีเส้นทาง ML บนแพลตฟอร์ม และมันคนละชั้นกับ Driver GPIO
- M05: โฟกัสการเตรียมข้อมูลเซ็นเซอร์ / buffer / หน้าต่างข้อมูลให้พร้อมต่อ inference

> การ flash Hello World สำเร็จเป็นเป้าหมายของ **[M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md)** ไม่ใช่ M01

---

## 10. Module Summary

1. **Edge AI** ผลักให้ MCU ต้องรองรับทั้งสมรรถนะ พลังงาน HMI และความปลอดภัย — ไม่ใช่แค่ CPU เร็วขึ้น  
2. **[PSOC™ Edge E84](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84)** เป็นตัวอย่าง multi-domain: High-Performance (M55 + Ethos-U55) และ Low-Power (M33 + NNLite)  
3. หน่วยความจำ SoC มีหลายชั้น — มีผลต่อโมเดล กราฟิก และ always-on  
4. สแต็กจริงของ Infineon มี BSP / PDL / HAL / middleware — หลักสูตรอธิบายผ่าน **HAL/BSP + Driver API + Utility + Application**  
5. **SDK ≠ IDE** — เครื่องมืออยู่คนละชั้นกับไลบรารีที่โค้ดเรียกใช้  
6. M01 ไม่ flash บอร์ด — คุณพร้อมแล้วสำหรับติดตั้งเครื่องมือใน [M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md)

### Next Steps

1. ทำแบบฝึกปฏิบัติ: [Lab](../l02-lab/README.md)  
2. เก็บแผ่นสรุปไว้ข้างตัว: [Cheatsheet](resources/sdk-layer-cheatsheet.md)  
3. เมื่อพร้อม ไปต่อ **M02 — ModusToolbox and VS Code for Firmware Development** ([บทเรียน M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md))  
4. หลัง M02 แล้ว ไปต่อ **M03 — GPIO and Basic Peripherals** ([บทเรียน M03](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md))

---

## References and Further Reading

ใช้เป็นจุดเริ่มค้นคว้า — ตรวจเวอร์ชันล่าสุดบนเว็บ Infineon / Arm เสมอ

### Platform and architecture

1. [PSOC™ Edge E84 — Infineon product page](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84)  
2. [PSOC™ Edge E84 documentation hub](https://documentation.infineon.com/psocedge/docs/eyv1750399809563)  
3. [PSOC™ Edge E84 Microcontrollers Product Brief (PDF)](https://www.infineon.com/assets/row/public/documents/30/45/infineon-psoc-edge-e84-productbrief-en.pdf)  
4. [PSOC™ Edge family overview](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm)  
5. [KIT_PSE84_EVAL — Evaluation Kit](https://www.infineon.com/evaluation-board/KIT-pse84-eval)  

### CPU / NPU (Arm developer)

6. [Arm Cortex-M55](https://developer.arm.com/Processors/Cortex-M55)  
7. [Arm Helium technology](https://developer.arm.com/Architectures/Helium)  
8. [Arm Ethos-U55](https://developer.arm.com/Processors/Ethos-U55)  
9. [Arm Cortex-M33](https://developer.arm.com/Processors/Cortex-M33)  

### Software stack and tools

10. [ModusToolbox™ software](https://www.infineon.com/modustoolbox)  
11. [AN235935 — Getting started with PSOC™ Edge on ModusToolbox™ (PDF)](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf)  
12. [AN241775 — Getting started with HAL on PSOC™ Edge (PDF)](https://www.infineon.com/assets/row/public/documents/30/42/infineon-an241775-getting-started-with-hal-psoc-edge-applicationnotes-en.pdf)  
13. [Infineon mtb-dsl-pse8xxgp (Device Support Library)](https://github.com/Infineon/mtb-dsl-pse8xxgp)  
14. [PSOC™ Edge quick start guide](https://documentation.infineon.com/modustoolbox/docs/psoc-edge-quick-start-guide)  
15. [DEEPCRAFT™ AI Suite](https://www.infineon.com/design-resources/embedded-software/deepcraft-edge-ai-solutions)  
16. [Visual Studio Code](https://code.visualstudio.com/) — ใช้จริงใน [M02](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md)  
17. [PSOC™ Edge application notes index](https://documentation.infineon.com/psocedge/docs/umo1761464512847) — รายการ AN ด้านกราฟิก ความปลอดภัย พลังงาน connectivity  
18. [KIT_PSE84_EVAL kit guide](https://documentation.infineon.com/psocedge/docs/lne1762692969598)  
19. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** — คลังตัวอย่างโค้ด, flowchart, API Reference สำหรับ PSoC Edge E84 (แหล่งอ้างอิงหลักของหลักสูตร)  
20. **[Bitstream Studio — Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** — VS Code extension (Sensor Telemetry, Sensor Studio, digital twin) สำหรับโฮสต์ที่เชื่อมต่อกับเฟิร์มแวร์ TESAIoT / PSoC Edge  
21. **[TESAIoT_Hackathon (GitHub)](https://github.com/drsanti/TESAIoT_Hackathon)** — แพ็กฝึกปฏิบัติ: `hex/` (firmware), `vsix/` (Bitstream Studio), `flasher/` (TESAIoT Flasher), `web-app/` (telemetry demos)

---

## เช็กความเข้าใจ

คำถามสั้นสามข้อใน [quiz.yaml](quiz.yaml) ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อน แล้วค่อยเทียบกับเฉลยและคำอธิบายในไฟล์

## แล็บ

ลงมือต่อที่ [แล็บ: จับคู่โดเมน MCU กับชั้นของ SDK](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/sdk-layer-cheatsheet.md) · [← Table of Contents](../../README.md) · [M02 →](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md)

## ตัวอย่างบน TESAIoT Developer Hub

ลองของจริงบน TESAIoT Dev Kit: เปิดตัวอย่างบน Developer Hub เพื่ออ่านโค้ด ดาวน์โหลด หรือ flash เฟิร์มแวร์สำเร็จรูป

- บทเรียนที่เกี่ยวข้อง: [TESAIoT Firmware Stack 1.1 · เครื่องมือ บอร์ด และ master template](../../../tesaiot-firmware-stack/m01-getting-started/l01-toolchain-and-master-template/README.md)
