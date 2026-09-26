---
id: fw-sdk.m02.l01
lang: th
title:
  th: 'ModusToolbox™ และ VS Code: สร้าง build flash debug'
  en: 'ModusToolbox™ and VS Code: Create, Build, Flash, Debug'
summary:
  th: แยกบทบาทของ ModusToolbox™, VS Code, KitProg3 และ SDK ตั้ง environment ให้ครบ เลือก BSP ให้ตรงคิต และรู้วิธีไล่อาการเสียที่พบบ่อย
  en: Separate the roles of ModusToolbox™, VS Code, KitProg3 and the SDK, set up a complete environment, pick the right BSP and troubleshoot common failures.
level: L3
time_min:
  concept: 40
  practise: 25
  check: 10
hardware:
  emulator: false
  boards:
  - devkit
  - eva-kit
prerequisites:
- fw-sdk.m01.l02
objectives:
- th: ระบุว่างานที่กำหนดให้ (สร้างโปรเจกต์, แก้โค้ด, flash/debug, เรียก API) เป็นหน้าที่ของ ModusToolbox™, VS Code, KitProg3/OpenOCD หรือ SDK
  en: Assign a given task (create a project, edit code, flash/debug, call an API) to ModusToolbox™, VS Code, KitProg3/OpenOCD or the SDK.
- th: ระบุองค์ประกอบ environment ที่ต้องมีก่อน build (tools, Arm GCC, VS Code, สิทธิ์ USB ของ KitProg) และเลือก BSP ให้ตรงกับคิตในมือ
  en: List the environment needed before a build (tools, Arm GCC, VS Code, USB access to KitProg) and choose the BSP that matches the kit in hand.
- th: ใช้ตาราง troubleshooting เชื่อมอาการเสียกับสาเหตุที่น่าจะเป็นได้ถูกต้อง
  en: Use the troubleshooting table to link a symptom to its likely cause.
develops:
- skill: build.vendor-sdk
  to: 2
- skill: build.compilers
  to: 2
- skill: debug.jtag-swd
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
  path: C1/M02/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M02 — ModusToolbox and VS Code for Firmware Development

**Course 1 · Module 2**  
**Suggested time:** ประมาณ 2.5–3 ชั่วโมง (ติดตั้งเครื่องมือ + สร้างโปรเจกต์ + build / flash / debug)  
**Format:** บทเรียนเชิงปฏิบัติ — ใช้เครื่องพัฒนาและบอร์ดจริง  

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/toolchain-cheatsheet.md) · [← Table of Contents](../../README.md) · [← M01](../../m01-mcu-architecture/l01-architecture-and-sdk-layers/README.md) · [M03 →](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md)

> **ถ้าจะ build จากซอร์สเปิด** (ตรวจสอบเมื่อ 26 ก.ย. 2026): [README ของ tesaiot-pse84-devkit-sdk](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/README.md) (commit `ef72c1b`) ตรึง ModusToolbox™ ไว้ที่ **3.6 เท่านั้น** พร้อม Arm GCC 14.2.1 ที่มากับ ModusToolbox build ด้วย `make build` และ flash ด้วย `make program` ส่วนเฟิร์มแวร์ที่ใช้ในโมดูล 3–8 ของหลักสูตรนี้แจกเป็น HEX สำเร็จรูปและยังไม่เปิดซอร์ส ดูหมายเหตุในบทเรียนโมดูล 3 และที่[หน้าหลักสูตร](../../README.md)

---

## เป้าหมาย (Learning Outcomes)

เมื่อเรียนจบ คุณควรทำได้ดังนี้:

1. อธิบายบทบาทของ **[ModusToolbox™](https://www.infineon.com/modustoolbox)** ในการสร้างและจัดการโปรเจกต์เฟิร์มแวร์บน PSOC™ Edge  
2. ตั้งค่า **Environment / Toolchain** ที่จำเป็นให้ build ได้บนเครื่องของคุณ  
3. ใช้ **[Visual Studio Code](https://code.visualstudio.com/)** ร่วมกับระบบนิเวศ ModusToolbox™ เพื่อแก้ไขโค้ด **Build** และ **Debug**  
4. จัดการ **Project Configuration**, **Device / BSP Selection** และ **Library Management** ในระดับใช้งานจริง  
5. เชื่อมเครื่องมือเข้ากับฮาร์ดแวร์จริงเพื่อ **Flash** และ **Debug** จนรันโปรแกรมตัวอย่างได้  

โมดูลนี้พาคุณจากแผนที่สถาปัตยกรรมใน [M01](../../m01-mcu-architecture/l01-architecture-and-sdk-layers/README.md) ไปสู่เวิร์กโฟลว์จริง: สร้างโปรเจกต์บน BSP ของคิต เรียกใช้ชั้น SDK และเห็นโค้ดรันบนบอร์ด

> **หมายเหตุเวอร์ชัน**  
> คู่มือ Infineon สำหรับ PSOC™ Edge (เช่น [PSOC™ Edge quick start guide](https://documentation.infineon.com/modustoolbox/docs/psoc-edge-quick-start-guide)) มักแนะนำ **ModusToolbox™ tools 3.6 หรือใหม่กว่า**  
> ให้ยึดเวอร์ชันที่ชุดแล็บของคุณกำหนดเป็นหลัก หากต่างจากตัวเลขในบทนี้ ให้ยึดตามชุดแล็บ

### Read alongside this chapter

| เอกสาร | ใช้เมื่อ |
|---|---|
| [ModusToolbox™ software installation guide](https://www.infineon.com/modustoolboxsetupguide) | ติดตั้งครั้งแรกบน Windows / Linux / macOS |
| [PSOC™ Edge quick start guide](https://documentation.infineon.com/modustoolbox/docs/psoc-edge-quick-start-guide) | ตรวจรายการแพ็กที่ควรติดสำหรับ Edge |
| [AN235935 — Getting started with PSOC™ Edge on ModusToolbox™](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf) | ภาพรวมสถาปัตยกรรมเครื่องมือ + เส้นทาง Hello World |
| [Visual Studio Code for ModusToolbox™ user guide](https://documentation.infineon.com/modustoolbox/docs/visual-studio-code-for-modustoolbox-user-guide) ([PDF](https://www.infineon.com/assets/row/public/documents/30/44/infineon-visual-studio-code-user-guide-usermanual-en.pdf)) | เปิดโปรเจกต์ใน VS Code, build / program / debug |
| [ModusToolbox™ tools package user guide](https://www.infineon.com/assets/row/public/documents/30/68/infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf) | Project Creator, Library Manager, configurators, flow รวม |
| [mtb-example-psoc-edge-hello-world](https://github.com/Infineon/mtb-example-psoc-edge-hello-world) | ตัวอย่าง Hello World ของ Infineon (tools 3.6+) — อ้างอิงเสริม |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | **คลังตัวอย่างหลักของหลักสูตร** — Example Explorer, Code Editor, flowchart, API Reference |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | **Host / Digital Twin ใน VS Code** — Sensor Telemetry, Sensor Studio, เชื่อมต่อบอร์ดหรือ Simulator |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | **แพ็กแล็บ** — HEX firmware, VSIX, TESAIoT Flasher, web-app / BLE demos สำหรับ flash และฝึกปฏิบัติ |

---

## 1. Why Two Tools: ModusToolbox™ and VS Code

จาก M01 เรารู้แล้วว่า **TESA Firmware SDK** คือชุดไลบรารี/API ที่แอปเรียกใช้ ส่วนเครื่องมือพัฒนาเป็นอีกชั้นหนึ่ง

| เครื่องมือ | บทบาทหลักในหลักสูตรนี้ | อ่านเพิ่ม |
|---|---|---|
| **[ModusToolbox™](https://www.infineon.com/modustoolbox)** | ติดตั้ง toolchain, สร้างโปรเจกต์จาก BSP/template, จัดการ library, เปิด configurator | [Tools package user guide](https://www.infineon.com/assets/row/public/documents/30/68/infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf) |
| **[Visual Studio Code](https://code.visualstudio.com/)** | เขียนโค้ด, IntelliSense, build/debug ผ่านเวิร์กโฟลว์ที่ ModusToolbox™ รองรับ | [VS Code for ModusToolbox™](https://documentation.infineon.com/modustoolbox/docs/visual-studio-code-for-modustoolbox-user-guide) |
| **KitProg3 / OpenOCD** (บนคิต) | Flash และ debug บนฮาร์ดแวร์จริง | ส่วน Programming ใน [AN235935](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf) |

> **Key phrase**  
> **ModusToolbox™ ใช้สร้างโปรเจกต์และจัดการ toolchain/library — VS Code ใช้เขียนโค้ดและ debug — SDK คือ API ที่แอปเรียกใช้**

Infineon รองรับหลาย IDE ได้แก่ Eclipse, VS Code, IAR Embedded Workbench และ Arm® MDK (µVision) รวมถึงการทำงานแบบ CLI  
ดูภาพรวมได้ใน [AN235935](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf) และ [tools package user guide](https://www.infineon.com/assets/row/public/documents/30/68/infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf)

ในหลักสูตรนี้เราโฟกัสคู่ **ModusToolbox™ + VS Code** เพราะเป็นแนวทางที่พบได้บ่อยในการเรียนและทีมพัฒนาสมัยใหม่ และมีคู่มือเฉพาะทางชัดเจน

---

## 2. ModusToolbox™ for Creating Firmware Projects

### 2.1 What ModusToolbox™ Is

**ModusToolbox™** ไม่ใช่แค่ตัวติดตั้ง IDE แต่เป็น **ชุดเครื่องมือ + ไลบรารี + ระบบ build** สำหรับพัฒนาแอปบน Infineon MCU รวมถึงตระกูล [PSOC™ Edge](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm)

องค์ประกอบที่คุณจะใช้บ่อยในหลักสูตร:

| ส่วนประกอบ | ใช้ทำอะไร | อ่านเพิ่ม |
|---|---|---|
| **Setup / tools package** | ติดตั้ง base tools, GCC, programming tools | [Installation guide](https://www.infineon.com/modustoolboxsetupguide) |
| **Dashboard** | จุดเริ่มเปิดเครื่องมือและสร้างโปรเจกต์ | ลิงก์จาก Setup / docs ของเวอร์ชันที่ติดตั้ง |
| **Project Creator** | สร้างแอปจาก BSP + code example / template | [Tools package user guide — Project Creator](https://www.infineon.com/assets/row/public/documents/30/68/infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf) |
| **Library Manager** | เพิ่ม ลบ อัปเดตไลบรารีของโปรเจกต์ | ส่วน Library management ใน [AN235935](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf) |
| **Device Configurator** | ตั้งค่าขา, clock, peripheral แล้วสร้างโค้ดคอนฟิก | คู่มือ Device Configurator ใน tools package + `make device-configurator` |
| **Build system (`make`)** | compile / program / เปิดเครื่องมือผ่าน recipe มาตรฐาน | [Tools package user guide](https://www.infineon.com/assets/row/public/documents/30/68/infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf) |

หน้าผลิตภัณฑ์และจุดดาวน์โหลดรวม: [ModusToolbox™](https://www.infineon.com/modustoolbox)  
โปรแกรม Setup มักดาวน์โหลดผ่าน Infineon Development Center / Software Tools (ลิงก์ใน [VS Code user guide PDF](https://www.infineon.com/assets/row/public/documents/30/44/infineon-visual-studio-code-user-guide-usermanual-en.pdf) ชี้ไปที่ `softwaretools.infineon.com`)

### 2.2 Recommended Install Set for PSOC™ Edge

จาก [PSOC™ Edge quick start guide](https://documentation.infineon.com/modustoolbox/docs/psoc-edge-quick-start-guide) โดยสรุปควรติดตั้งอย่างน้อย:

1. **ModusToolbox™ Setup** ตาม [installation guide](https://www.infineon.com/modustoolboxsetupguide) สำหรับ OS ของคุณ  
2. **Arm® GNU Toolchain (GCC)**  
3. **Base tools package** เวอร์ชันที่รองรับ Edge (**3.6+** ตาม quick start)  
4. **IDE ตัวเลือก** — ในหลักสูตรนี้เลือก **VS Code** ([ดาวน์โหลด VS Code](https://code.visualstudio.com/Download) หากยังไม่มี)  
5. **Programming tools package** ตามที่ Setup เสนอ  
6. (ถ้าต้องใช้) **Edge Protect Security Suite** หรือแพ็ก ML เช่น [DEEPCRAFT™](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84) / Machine Learning Pack — ไม่บังคับสำหรับ Hello World แรก  

> **LLVM (optional)**  
> Quick start ระบุว่าบางงานอาจต้องการ [LLVM Embedded Toolchain for Arm](https://github.com/ARM-software/LLVM-embedded-toolchain-for-Arm/) ซึ่ง**ไม่รวม**ใน Setup มาตรฐาน — ติดตั้งเพิ่มเมื่อคู่มือของชุดที่ใช้ระบุ

#### Practical install tips (from Infineon installation guidance)

- ใช้ **Setup program** เป็นวิธีหลักตั้งแต่รุ่น 3.2 เป็นต้นไป เพราะช่วยเลือก tools, IDE และ toolchain เป็นชุด  
- หากสร้างแอปหรือเพิ่ม library แล้วระบบแจ้งว่าขาดแพ็ก ให้กลับไปเปิด Setup / ติดตั้งแพ็กที่ขาด (Project Creator และ Library Manager มักเตือนเมื่อขาด asset)  
- เครือข่ายที่บล็อก GitHub อาจกระทบการดึง BSP/library — ดูหัวข้อ proxy / manifest ใน [installation guide](https://www.infineon.com/modustoolboxsetupguide) และ Project Creator guide ของเวอร์ชันที่ติดตั้ง  

### 2.3 Creating a Project with Project Creator

Project Creator มีทั้ง GUI และ CLI ติดตั้งภายใต้โฟลเดอร์ tools ของ ModusToolbox™ (เช่น `.../ModusToolbox/tools_<version>/project-creator`)  
รายละเอียดขั้นตอนอยู่ใน [tools package user guide](https://www.infineon.com/assets/row/public/documents/30/68/infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf) และ [VS Code for ModusToolbox™ guide](https://documentation.infineon.com/modustoolbox/docs/visual-studio-code-for-modustoolbox-user-guide)

ลำดับมาตรฐาน:

1. เปิด **ModusToolbox™ Dashboard** หรือเปิด **Project Creator** โดยตรง  
2. เลือก **Kit / BSP** ที่ตรงกับบอร์ดในมือ เช่นตระกูล [KIT_PSE84_EVAL](https://www.infineon.com/evaluation-board/KIT-pse84-eval) ที่คุณมี  
3. เลือก **code example** หรือ template เริ่มต้น  
   - **แนะนำหลักสูตร:** เปิดตัวอย่างจาก **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** (กรอง Board / Domain ตามคิตในมือ) แล้วดาวน์โหลดหรือเปิดตามคู่มือของชุดที่ใช้  
   - **ทางเลือกผู้ผลิต:** [Hello World สำหรับ PSOC™ Edge](https://github.com/Infineon/mtb-example-psoc-edge-hello-world) เมื่อต้องการเทียบกับตัวอย่างดิบของ Infineon  
4. ใน Target IDE เลือก **Visual Studio Code / Microsoft Visual Studio Code** เพื่อให้สร้างไฟล์เวิร์กสเปซและคอนฟิกที่เกี่ยวข้อง  
5. ระบุโฟลเดอร์ปลายทาง แล้วให้เครื่องมือ **clone BSP/template และดึงไลบรารีที่จำเป็นจาก manifest**

ผลลัพธ์ที่คาดหวัง:

- โครงสร้างโปรเจกต์พร้อมระบบ `make`  
- ไลบรารี/BSP ที่ถูกดึงมาแล้ว  
- ไฟล์ `*.code-workspace` สำหรับ VS Code  

คลังตัวอย่างของหลักสูตร: **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**  
คลังตัวอย่างรวมของ Infineon (เสริม): [Code Examples for ModusToolbox™ Software](https://github.com/Infineon/Code-Examples-for-ModusToolbox-Software)

### 2.4 Typical Application Structure (Mental Model)

โครงสร้างจริงขึ้นกับ template แต่แนวคิดมักคล้ายกัน:

```text
my-app/
  ├── *.code-workspace          # เปิดด้วย VS Code
  ├── Makefile / makefiles      # ระบบ build ของ ModusToolbox™
  ├── main.c / source/           # โค้ดแอปของคุณ
  ├── deps / libs / bsps ...    # ไลบรารีและ BSP ที่ดึงมา (ชื่อโฟลเดอร์ตามเวอร์ชัน)
  ├── configs / design.modus    # คอนฟิกจาก Device Configurator (ถ้ามี)
  └── build/                    # ผล build (สร้างตอน compile)
```

**แนวปฏิบัติมืออาชีพ**

- แก้โค้ดผลิตภัณฑ์ในชั้นแอป ไม่แก้ในโฟลเดอร์ library จนเป็นนิสัย  
- เพิ่ม/อัปเดต dependency ผ่าน **Library Manager**  
- commit เฉพาะสิ่งที่ทีมกำหนด (บางทีมไม่ commit โฟลเดอร์ libs ทั้งก้อน — ตามนโยบายของทีม)

---

## 3. Environment and Toolchain

### 3.1 What “Environment” Means Here

ก่อน build ได้ เครื่องต้องมีอย่างน้อย:

| ส่วนประกอบ | ใช้ทำอะไร | อ้างอิง |
|---|---|---|
| ModusToolbox™ tools | Project Creator, Library Manager, make recipes, OpenOCD ฯลฯ | [Installation guide](https://www.infineon.com/modustoolboxsetupguide) |
| Arm GNU Toolchain (GCC) | แปลโค้ด C เป็นไบนารีสำหรับ Cortex-M | [Edge quick start](https://documentation.infineon.com/modustoolbox/docs/psoc-edge-quick-start-guide) |
| VS Code + extensions | แก้ไขและ debug | [VS Code guide](https://documentation.infineon.com/modustoolbox/docs/visual-studio-code-for-modustoolbox-user-guide) |
| USB access สำหรับ KitProg | ให้โฮสต์เห็น debugger บนบอร์ด | [AN235935 — Programming and Debugging](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf) |
| Terminal emulator | ดู UART log จากตัวอย่าง | README ของ [Hello World example](https://github.com/Infineon/mtb-example-psoc-edge-hello-world) มักแนะนำเช่น Tera Term |
| **Bitstream Studio** (แนะนำติดตั้ง) | Host app ใน VS Code — Sensor Telemetry / Sensor Studio / digital twin เชื่อมบอร์ดหลัง flash | [Marketplace — TERNIONDEV.bitstream-studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) |
| **TESAIoT_Hackathon pack** | HEX สำเร็จรูป, TESAIoT Flasher, VSIX สำรอง, web-app demos | [github.com/drsanti/TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) |

### 3.2 Path and Tool Discovery

ระบบ build ของ ModusToolbox™ คาดว่าจะหา tools package ได้ตาม path การติดตั้งมาตรฐาน  
หากติดตั้งผิดที่หรือมีหลายเวอร์ชันซ้อนกัน มักเจออาการ:

- `make` หา compiler ไม่เจอ  
- เปิด configurator ไม่ได้  
- program/debug ล้มเหลวทั้งที่บอร์ดเสียบอยู่  

แนวทางแก้เบื้องต้น:

1. ติดตั้งใหม่หรือซ่อมผ่าน [Setup / installation guide](https://www.infineon.com/modustoolboxsetupguide)  
2. เปิดเทอร์มินัลจากเวิร์กโฟลว์ที่เอกสาร VS Code / tools package แนะนำ  
3. ในโฟลเดอร์โปรเจกต์ ทดลองเป้าหมายมาตรฐาน เช่น `make help` หรือ `make build` (ชื่อเป้าหมายอาจต่างตาม template — ดู Makefile ของโปรเจกต์)

### 3.3 Optional: J-Link Instead of On-board KitProg

[Edge quick start](https://documentation.infineon.com/modustoolbox/docs/psoc-edge-quick-start-guide) ระบุทางเลือก **SEGGER J-Link**:

1. ติดตั้ง [J-Link software](https://www.segger.com/downloads/jlink/) แล้วจด path  
2. แก้ไฟล์ BSP (เช่น `bsp.mk`) เพิ่ม `BSP_PROGRAM_INTERFACE=JLink`  
3. ถ้าติดตั้งนอก path มาตรฐาน เพิ่ม `MTB_JLINK_DIR=...` เช่น  
   - Windows: `C:/Program Files/SEGGER/JLink_V852`  
   - macOS: `/Applications/SEGGER/JLink_V852`  
   - Linux: `/opt/SEGGER/JLink_V852`  

ส่วนใหญ่ใช้ **KitProg บนบอร์ด** ก่อน — สลับไป J-Link เมื่อจำเป็น

---

## 4. Using VS Code with the SDK (Edit, Build, Debug)

เอกสารหลักของส่วนนี้:  
[Visual Studio Code for ModusToolbox™ user guide](https://documentation.infineon.com/modustoolbox/docs/visual-studio-code-for-modustoolbox-user-guide) · [PDF](https://www.infineon.com/assets/row/public/documents/30/44/infineon-visual-studio-code-user-guide-usermanual-en.pdf)

### 4.1 Opening the Project

ลำดับมาตรฐาน:

1. สร้างโปรเจกต์ด้วย Project Creator โดยเลือก target เป็น VS Code หรือสร้างแล้วได้ไฟล์เวิร์กสเปซ  
2. เปิด **VS Code ด้วยมือ**  
3. เปิดไฟล์ **`{project-name}.code-workspace`** ในโฟลเดอร์โปรเจกต์  

อย่าเปิดแค่โฟลเดอร์ย่อยแบบสุ่มจน task / launch configuration หาย — ให้เปิดไฟล์ workspace ที่เครื่องมือสร้างให้  
รายละเอียดเพิ่มในส่วน “Using the code example” ของหลาย repo เช่น [Hello World docs flow](https://github.com/Infineon/mtb-example-psoc-edge-hello-world)

### 4.2 Extensions and Assistant

คู่มือ VS Code ของ Infineon อ้างถึง:

- ส่วนขยาย/เวิร์กโฟลว์ **ModusToolbox™ Assistant** (ตามเวอร์ชัน) สำหรับช่วยสร้างแอปและเปิดเครื่องมือ  
- **[Cortex-Debug](https://github.com/Marus/cortex-debug)** สำหรับเพิ่มความสามารถ debug ของ Cortex-M ใน VS Code  

ถ้าชุดแล็บของคุณระบุชุด extension ที่ล็อกไว้ — ติดตั้งตามรายการนั้นเพื่อให้:

- สร้าง/เปิดแอปได้จาก VS Code  
- รัน build / program / debug configurations  
- เปิด Device Configurator และเครื่องมืออื่นจากแผงช่วยเหลือ  

### 4.3 Build

ไม่ว่าจะกดปุ่มใน VS Code หรือใช้เทอร์มินัล หลักการเดียวกันคือเรียก **ระบบ make ของโปรเจกต์** ที่ ModusToolbox™ สร้างไว้  
ดูภาพรวม build/program/debug ใน [tools package user guide](https://www.infineon.com/assets/row/public/documents/30/68/infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf)

สิ่งที่ควรตรวจเมื่อ build สำเร็จ:

- ไม่มี error จาก compiler / linker  
- ได้ไฟล์เอาต์พุตในโฟลเดอร์ `build` ตามที่ template กำหนด  
- หลังเปลี่ยน BSP/library แล้วยัง build ใหม่ได้  

### 4.4 Program vs Debug

| การกระทำ | ความหมาย |
|---|---|
| **Program / Flash** | เขียนเฟิร์มแวร์ลงหน่วยความจำของอุปกรณ์ |
| **Debug** | มักรวมการ program แล้วหยุดที่ breakpoint / step โค้ดผ่าน GDB + OpenOCD หรือ probe อื่น |

[AN235935](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf) ระบุว่า ModusToolbox™ รองรับ **OpenOCD + GDB server** และ probe เช่น **KitProg3** หรือ **J-Link**  
สำหรับ PSOC™ Programmer แบบแยก (program/erase/verify/read) ดูเอกสาร Programming tools ของ Infineon ที่มากับ Setup

---

## 5. Project Configuration, Device Selection, and Library Management

### 5.1 Device / BSP Selection

**BSP (Board Support Package)** บอกโปรเจกต์ว่า:

- ใช้ชิป/บอร์ดใด  
- ขาและอุปกรณ์บนบอร์ดแมปอย่างไร  
- ต้องดึงไลบรารีใดเป็นอย่างน้อย  

การเลือก BSP ผิดตอนสร้างโปรเจกต์ = โค้ดอาจ build ได้แต่ **ขา LED/UART ไม่ตรงของจริง**

กฎง่าย ๆ: **เลือก BSP ให้ตรงกับคิตที่เสียบอยู่**  
ตัวอย่างคิตอ้างอิง: [KIT_PSE84_EVAL](https://www.infineon.com/evaluation-board/KIT-pse84-eval) · หน้า [PSOC™ Edge E84](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84)

Device Support Library ตัวอย่างบน GitHub: [mtb-dsl-pse8xxgp](https://github.com/Infineon/mtb-dsl-pse8xxgp)

### 5.2 Device Configurator

เปิดได้จากเวิร์กโฟลว์ IDE หรือจากโฟลเดอร์โปรเจกต์:

```bash
make device-configurator
```

ตาม [VS Code for ModusToolbox™ guide](https://www.infineon.com/assets/row/public/documents/30/44/infineon-visual-studio-code-user-guide-usermanual-en.pdf) ใช้เพื่อ:

- ดู/เปิดใช้งาน peripheral  
- ตั้งค่า pins, clocks, DMA ฯลฯ  
- สร้างโค้ดคอนฟิกที่ลิงก์เข้า build  
- เปิด configurator อื่นที่เกี่ยวข้อง (เช่น CAPSENSE™, QSPI) ตามที่ BSP รองรับ  

แต่ละ resource ที่เปิดมักมีลิงก์ไป API documentation ที่เกี่ยวข้อง

> สำหรับ PSOC™ Edge: การตั้งค่าและ init เพริเฟอรัลจำนวนมากถูกออกแบบให้ทำผ่าน **configurator + PDL** (ทบทวน [M01 §7–8](../../m01-mcu-architecture/l01-architecture-and-sdk-layers/README.md))  
> ใน M02 ให้ฝึก “เปิดดูและบันทึกคอนฟิก” ก่อนเขียน Driver ลึกใน M03

### 5.3 Library Manager

**Library Manager** ช่วย:

- เพิ่ม middleware / ไลบรารี  
- ลบของที่ไม่ใช้  
- อัปเดตเวอร์ชันตาม manifest บน GitHub ของ Infineon  

ใช้เมื่อต้องการฟีเจอร์เพิ่ม เช่น `retarget-io` (UART printf), `abstraction-rtos`, connectivity — ไม่คัดลอกไลบรารีจากโปรเจกต์อื่นแบบสุ่ม  
ดูคำอธิบาย library management ใน [AN235935](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf)

### 5.4 Project Configuration Checklist

ก่อนสรุปว่าโปรเจกต์พร้อมพัฒนาต่อ:

- [ ] BSP ตรงคิต  
- [ ] เปิดใน VS Code ผ่าน `.code-workspace`  
- [ ] build ผ่าน  
- [ ] รู้วิธีเปิด Device Configurator และ Library Manager  
- [ ] รู้ว่าโค้ดแอปอยู่ไฟล์/โฟลเดอร์ไหน  

---

## 6. Flash and Debug on Real Hardware

### 6.1 Hardware Prerequisites

- คิต PSOC™ Edge ที่ใช้ (เช่น [KIT_PSE84_EVAL](https://www.infineon.com/evaluation-board/KIT-pse84-eval))  
- สาย USB ที่จ่ายไฟและคุยกับ **KitProg** ได้  
- (ถ้ามี) พอร์ต UART ตามคู่มือคิต — บางคิตใช้ USB-UART ผ่าน KitProg  

### 6.2 KitProg3 and fw-loader

คิต Infineon มักมีโปรแกรมเมอร์บนบอร์ดชื่อ **KitProg**  
ModusToolbox™ คาด **KitProg3** (CMSIS-DAP) ซึ่งเร็วกว่าโหมด HID ในหลายกรณี ตามที่อธิบายในคู่มือ VS Code / tools

หากคิตเก่าหรือเฟิร์มแวร์ไม่ตรง:

- ใช้ **fw-loader** ที่มากับ ModusToolbox™ เพื่ออัปเดต KitProg  
- บน Linux อาจต้องติดตั้ง udev rules ก่อนใช้ fw-loader ครั้งแรก  

อ่านรายละเอียดในส่วน KitProg ของ [VS Code user guide PDF](https://www.infineon.com/assets/row/public/documents/30/44/infineon-visual-studio-code-user-guide-usermanual-en.pdf) และ [AN235935](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf)

### 6.3 Prebuilt HEX, Flasher, and Lab Pack

เมื่อเลือกใช้เฟิร์มแวร์สำเร็จรูป (ไม่ build จากซอร์สในตอนนั้น) หรือต้องการตัวติดตั้ง flasher / VSIX คู่กัน ให้ใช้แพ็กจาก:

**[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)**

| โฟลเดอร์ใน repo | ใช้ทำอะไร |
|---|---|
| [`hex/`](https://github.com/drsanti/TESAIoT_Hackathon/tree/main/hex) | ไฟล์ `.hex` ของ DevKit — flash ก่อนแล็บฮาร์ดแวร์ |
| [`flasher/`](https://github.com/drsanti/TESAIoT_Hackathon/tree/main/flasher) | ตัวติดตั้ง **TESAIoT Flasher** (Windows / macOS / Linux) |
| [`vsix/`](https://github.com/drsanti/TESAIoT_Hackathon/tree/main/vsix) | Bitstream Studio `.vsix` (ทางเลือกติดตั้งนอก Marketplace) |
| [`web-app/`](https://github.com/drsanti/TESAIoT_Hackathon/tree/main/web-app) | ตัวอย่าง HTML telemetry สำหรับฝึกหลังเชื่อมต่อโฮสต์ |

> จับคู่เวอร์ชัน **VSIX กับ HEX** ตามที่ README ของ repo แนะนำ (ดูรายการ `latest` ใน firmware manifest เมื่อมี)

ทางเลือก flash อื่นในหลักสูตร: **ModusToolbox™ Program** จากโปรเจกต์ที่คุณ build เอง (หมวดก่อนหน้า) หรือ TESAIoT Flasher + HEX จาก repo นี้

### 6.4 First Success Criteria (Hello World Path)

เป้าหมายขั้นต่ำของ M02:

1. Build โปรเจกต์ตัวอย่างผ่าน **หรือ** flash HEX จากแพ็กแล็บสำเร็จ  
2. Program ลงบอร์ดสำเร็จ  
3. เห็นพฤติกรรมที่ยืนยันได้ เช่น LED กระพริบ และ/หรือข้อความบน serial terminal / telemetry ใน Bitstream Studio  
4. เปิด debug session ได้ อย่างน้อย halt ที่ `main` หรือ breakpoint ง่าย ๆ (เมื่อใช้เส้นทาง build จากซอร์ส)

เส้นทางอ้างอิงหลักสูตร (ตัวอย่างโค้ด): **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**  
เส้นทางอ้างอิงแพ็กแล็บ (HEX / Flasher / demos): **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)**  
เส้นทางอ้างอิงผู้ผลิต (เสริม): [mtb-example-psoc-edge-hello-world](https://github.com/Infineon/mtb-example-psoc-edge-hello-world) + ขั้นตอนใน [AN235935](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf)

ถ้าทำครบเกณฑ์นี้ คุณพร้อมเข้า M03 เพื่อเรียก Driver API อย่างมีระบบ

### 6.5 Troubleshooting Quick Table

| อาการ | แนวทางตรวจ | อ่านเพิ่ม |
|---|---|---|
| บอร์ดไม่ปรากฏ / ไม่ program ได้ | สาย USB, พอร์ต, KitProg3, ไดรเวอร์, ลองพอร์ตอื่น | KitProg / fw-loader ในคู่มือ VS Code · [Hackathon troubleshooting](https://github.com/drsanti/TESAIoT_Hackathon) |
| Build หา toolchain ไม่เจอ | ติดตั้ง GCC/tools ตาม Setup, เปิดเทอร์มินัลที่ถูกต้อง | [Installation guide](https://www.infineon.com/modustoolboxsetupguide) |
| Build ผ่านแต่ไม่มีอาการบนบอร์ด | BSP ผิดคิต, ยังไม่ได้ program, ดูคนละ LED/UART | ตรวจ BSP กับหน้าคิต |
| Debug ต่อไม่ได้ | OpenOCD/KitProg, ปิดโปรแกรมที่ครองพอร์ต, ตรวจ launch config | [Cortex-Debug](https://github.com/Marus/cortex-debug) + VS Code guide |
| Serial ไม่มีข้อความ | baud rate, พอร์ต COM, ยังไม่มี retarget-io/UART ในตัวอย่าง | README ของ code example |
| Flash HEX แล้วไม่มี telemetry | VSIX กับ HEX คนละเวอร์ชัน, baud ไม่ใช่ 921600, ยังไม่ Link ใน Bitstream Studio | [TESAIoT_Hackathon README](https://github.com/drsanti/TESAIoT_Hackathon) |

---

## 7. How This Connects to TESA Firmware SDK

เมื่อโปรเจกต์พร้อมแล้ว คุณยืนบนสแต็กเดียวกับที่เรียนใน M01:

```text
VS Code (edit / build / debug)
        │
ModusToolbox™ tools (create, libraries, configurators, OpenOCD)
        │
Application  →  Utility / Driver API (TESA Firmware SDK ในหลักสูตร)
        │
BSP / PDL / HAL (Device Support)
        │
PSOC™ Edge hardware
```

- M02 ทำให้คุณ **พร้อมสร้างและรันโปรเจกต์บนเครื่องมือจริง**  
- M03 จะให้คุณ **เรียก Driver API** บนโปรเจกต์นั้นอย่างตั้งใจ  

ทบทวนชั้นซอฟต์แวร์: [M01 — Software Ecosystem](../../m01-mcu-architecture/l01-architecture-and-sdk-layers/README.md) · [Device Support Library (pse8xxgp)](https://github.com/Infineon/mtb-dsl-pse8xxgp)

---

## 8. Module Summary

1. **ModusToolbox™** สร้างโปรเจกต์จาก BSP/template และจัดการ toolchain / libraries / configurators  
2. **Environment** ที่ถูกต้อง = tools + GCC + VS Code + สิทธิ์เข้าถึง KitProg  
3. เปิดโปรเจกต์ผ่าน **`.code-workspace`** แล้ว build/debug ตามเวิร์กโฟลว์ Infineon  
4. **BSP ต้องตรงคิต**; ใช้ Device Configurator และ Library Manager เป็นทางหลัก  
5. **Flash + Debug บนบอร์ดจริง** คือเกณฑ์ผ่านของโมดูลนี้  

### Next Steps

1. ทำแบบฝึกปฏิบัติ: [Lab](../l02-lab/README.md)  
2. เก็บแผ่นสรุป: [Cheatsheet](resources/toolchain-cheatsheet.md)  
3. เมื่อพร้อม ไปต่อ **M03 — GPIO and Basic Peripherals** ([บทเรียน M03](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md))

---

## References and Further Reading

### Official Infineon documentation

1. [ModusToolbox™ product page](https://www.infineon.com/modustoolbox)  
2. [ModusToolbox™ software installation guide](https://www.infineon.com/modustoolboxsetupguide)  
3. [ModusToolbox™ tools package user guide (PDF)](https://www.infineon.com/assets/row/public/documents/30/68/infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf)  
4. [PSOC™ Edge quick start guide](https://documentation.infineon.com/modustoolbox/docs/psoc-edge-quick-start-guide)  
5. [AN235935 — Getting started with PSOC™ Edge E8 MCU on ModusToolbox™ (PDF)](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf)  
6. [Visual Studio Code for ModusToolbox™ user guide](https://documentation.infineon.com/modustoolbox/docs/visual-studio-code-for-modustoolbox-user-guide) · [PDF](https://www.infineon.com/assets/row/public/documents/30/44/infineon-visual-studio-code-user-guide-usermanual-en.pdf)  
7. [PSOC™ Edge E84 product page](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84)  
8. [KIT_PSE84_EVAL evaluation kit](https://www.infineon.com/evaluation-board/KIT-pse84-eval)  

### Code examples and libraries

9. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** — Example Explorer, flowchart, API Reference (แหล่งตัวอย่างหลักของหลักสูตร)  
10. [mtb-example-psoc-edge-hello-world](https://github.com/Infineon/mtb-example-psoc-edge-hello-world) — ตัวอย่าง Infineon เสริม  
11. [Code Examples for ModusToolbox™ Software](https://github.com/Infineon/Code-Examples-for-ModusToolbox-Software)  
12. [mtb-dsl-pse8xxgp (Device Support Library)](https://github.com/Infineon/mtb-dsl-pse8xxgp)  

### Related tools

13. [Visual Studio Code](https://code.visualstudio.com/) · [Download](https://code.visualstudio.com/Download) · [Docs](https://code.visualstudio.com/docs)  
14. [Cortex-Debug extension (GitHub)](https://github.com/Marus/cortex-debug)  
15. [SEGGER J-Link](https://www.segger.com/downloads/jlink/) (optional probe)  
16. [LLVM Embedded Toolchain for Arm](https://github.com/ARM-software/LLVM-embedded-toolchain-for-Arm/) (optional)  
17. [OpenOCD](https://openocd.org/) / KitProg3 ตามคู่มือคิต  

### Host application / Digital Twin

18. **[Bitstream Studio — Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** (`TERNIONDEV.bitstream-studio`) — VS Code extension สำหรับ Sensor Telemetry, Sensor Studio, digital twin 3D และโฮสต์ที่เชื่อมต่อเฟิร์มแวร์บน TESAIoT / PSoC Edge (USB / Wi‑Fi / MQTT หรือ Simulator)

### Lab pack / flash / demos

19. **[TESAIoT_Hackathon (GitHub)](https://github.com/drsanti/TESAIoT_Hackathon)** — HEX firmware (`hex/`), TESAIoT Flasher (`flasher/`), VSIX (`vsix/`), web-app telemetry demos (`web-app/`) สำหรับฝึกปฏิบัติ  

---

## เช็กความเข้าใจ

คำถามสั้นสามข้อใน [quiz.yaml](quiz.yaml) ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อน แล้วค่อยเทียบกับเฉลยและคำอธิบายในไฟล์

## แล็บ

ลงมือต่อที่ [แล็บ: สร้าง build flash และ debug โปรเจกต์เฟิร์มแวร์](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/toolchain-cheatsheet.md) · [← Table of Contents](../../README.md) · [← M01](../../m01-mcu-architecture/l01-architecture-and-sdk-layers/README.md) · [M03 →](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md)

## ตัวอย่างบน TESAIoT Developer Hub

ลองของจริงบน TESAIoT Dev Kit: เปิดตัวอย่างบน Developer Hub เพื่ออ่านโค้ด ดาวน์โหลด หรือ flash เฟิร์มแวร์สำเร็จรูป

- บทเรียนที่เกี่ยวข้อง: [TESAIoT Firmware Stack 1.1 · เครื่องมือ บอร์ด และ master template](../../../tesaiot-firmware-stack/m01-getting-started/l01-toolchain-and-master-template/README.md)
