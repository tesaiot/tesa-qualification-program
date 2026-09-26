---
id: fw-sdk.m02.l02
lang: th
title:
  th: 'แล็บ: สร้าง build flash และ debug โปรเจกต์เฟิร์มแวร์'
  en: 'Lab: Create, Build, Flash, and Debug a Firmware Project'
summary:
  th: ตรวจเครื่อง สร้างโปรเจกต์จาก BSP build ใน VS Code flash ลงบอร์ด และ debug อย่างน้อยหนึ่งครั้ง
  en: Check the machine, create a project from a BSP, build in VS Code, flash the board and debug at least once.
level: L3
time_min:
  lab: 120
hardware:
  emulator: false
  boards:
  - devkit
  - eva-kit
prerequisites:
- fw-sdk.m02.l01
objectives:
- th: สร้างโปรเจกต์จาก BSP ที่ตรงคิต แล้ว build สำเร็จใน VS Code หรือเทอร์มินัล
  en: Create a project from the matching BSP and build it in VS Code or a terminal.
- th: flash ลงบอร์ดและยืนยันผลที่สังเกตได้ (LED หรือข้อความ serial)
  en: Flash the board and confirm an observable result (LED or serial output).
- th: เปิด debug session และ halt ที่ main หรือ breakpoint ได้อย่างน้อยหนึ่งครั้ง
  en: Start a debug session and halt at main or a breakpoint at least once.
develops:
- skill: build.vendor-sdk
  to: 2
- skill: debug.jtag-swd
  to: 2
- skill: debug.gdb
  to: 1
assesses:
- skill: build.vendor-sdk
  level: 2
  evidence: README.md#submission-checklist
- skill: debug.jtag-swd
  level: 2
  evidence: README.md#part-5--debug-once
context:
  platform: psoc-edge-e84
  lang: c
  ide: modustoolbox-vscode
  firmware: tesaiot-bitstream (HEX; source not public yet)
status: alpha
translation: pending
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M02/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M02 — Create, Build, Flash, and Debug a Firmware Project

**Course 1 · Module 2**  
**Type:** Hands-on lab (requires PC tools + board)  
**Suggested time:** 90–120 minutes  

Read first: [Lesson](../l01-modustoolbox-and-vscode/README.md) · [Cheatsheet](../l01-modustoolbox-and-vscode/resources/toolchain-cheatsheet.md) · [← Table of Contents](../../README.md) · [← M01](../../m01-mcu-architecture/l01-architecture-and-sdk-layers/README.md) · [M03 →](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md)

---

## Lab Goals

เมื่อทำครบ คุณจะ:

- ติดตั้ง/ตรวจสภาพแวดล้อม ModusToolbox™ + VS Code ให้พร้อม  
- สร้างโปรเจกต์จาก BSP ของคิตในมือ  
- Build สำเร็จใน VS Code หรือเทอร์มินัล  
- Flash และยืนยันผลบนบอร์ดจริง  
- เปิด debug session อย่างน้อยหนึ่งครั้ง  

---

## Prerequisites

- [ ] อ่านจบ [บทเรียน](../l01-modustoolbox-and-vscode/README.md)  
- [ ] เครื่องติดตั้งตามรายการในบทเรียน (หรือตามคู่มือของชุดที่ใช้)  
- [ ] บอร์ด PSOC™ Edge + สาย USB  
- [ ] รู้รหัส/ชื่อคิตที่ใช้เลือก BSP  

> **หลัง flash สำเร็จ — ดู telemetry บนโฮสต์**  
> ติดตั้ง **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** จาก Marketplace (หรือจาก `vsix/` ในแพ็กแล็บ) แล้วใช้ Command Palette → **Bitstream Studio: Open Bitstream Studio** / **Start Serial Bridge**  
>  
> **แพ็ก HEX / Flasher / demos:** **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** — clone หรือดาวน์โหลด ZIP แล้วใช้ `hex/` + `flasher/` ตาม README ของ repo (จับคู่เวอร์ชันกับ VSIX)

---

## Part 1 — Environment Check

บันทึกผลลงโน้ต:

| รายการ | มีแล้ว? | หมายเหตุ |
|---|---|---|
| ModusToolbox™ tools (ระบุเวอร์ชัน) | | |
| Arm GNU Toolchain (GCC) | | |
| VS Code | | |
| ส่วนขยายที่ชุดแล็บกำหนด | | |
| Terminal emulator (ถ้าต้องดู UART) | | |

**ผ่านเมื่อ:** ตรวจรายการข้างบนครบว่าเครื่องพร้อม หรือคุณสร้างโปรเจกต์ใหม่ได้ใน Part 2

---

## Part 2 — Create a Project

1. เปิด **ModusToolbox™ Dashboard** หรือ **Project Creator**  
2. เลือก **BSP/Kit** ให้ตรงบอร์ดในมือ  
3. เลือกตัวอย่างเริ่มต้น  
   - แนะนำ: เปิดจาก **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** (Example Explorer → กรอง Board ตามคิต)  
   - หรือ Hello World ของ Infineon หากเลือกเส้นทางนั้น  
4. เลือกเป้าหมาย **VS Code**  
5. สร้างโปรเจกต์ลงโฟลเดอร์ที่ตั้งชื่อเป็นระเบียบ (หลีกเลี่ยง path มีช่องว่างแปลก ๆ ถ้าทำได้)  

บันทึก:

- ชื่อโปรเจกต์: _______________  
- BSP ที่เลือก: _______________  
- path โฟลเดอร์: _______________  

**ผ่านเมื่อ:** มีไฟล์ `.code-workspace` ในโปรเจกต์

---

## Part 3 — Open in VS Code and Build

1. เปิดไฟล์ **`*.code-workspace`** ด้วย VS Code  
2. รัน **build** ตามเวิร์กโฟลว์ที่เลือกใช้ (ปุ่มใน IDE หรือ `make` ในเทอร์มินัลโปรเจกต์)  
3. แก้ error เบื้องต้นถ้ามี (toolchain / path / library)  

| ผล build | บันทึก |
|---|---|
| สำเร็จครั้งแรกใช้เวลาประมาณ | |
| Error ที่เจอ (ถ้ามี) และวิธีแก้ | |

**ผ่านเมื่อ:** build สำเร็จโดยไม่มี error

---

## Part 4 — Flash to the Board

1. เสียบ USB ให้ KitProg พร้อม  
2. Program/Flash ตาม launch config หรือคำสั่งที่เอกสารกำหนด  
3. สังเกตผลบนบอร์ด (LED / พฤติกรรมตามตัวอย่าง)  
4. ถ้าตัวอย่างมี UART: เปิด terminal ที่ baud ตามคู่มือ แล้วบันทึกข้อความที่ได้  

**ผ่านเมื่อ:** เห็นพฤติกรรมที่ยืนยันว่าเฟิร์มแวร์ใหม่รันบนบอร์ด

---

## Part 5 — Debug Once

1. ตั้ง breakpoint ใน `main` หรือฟังก์ชันที่เห็นชัดในตัวอย่าง  
2. เริ่ม debug session  
3. ยืนยันว่า halt ที่ breakpoint ได้ แล้ว resume/step อย่างน้อยหนึ่งครั้ง  

บันทึก:

- ชื่อ configuration ที่ใช้: _______________  
- halt ที่บรรทัด/ฟังก์ชัน: _______________  

**ผ่านเมื่อ:** debug ทำงานได้อย่างน้อยหนึ่งรอบ

---

## Part 6 — Configuration Awareness (Light)

ไม่ต้อง redesign ทั้งบอร์ด — แค่เปิดดู:

1. เปิด **Device Configurator** (`make device-configurator` หรือจาก IDE)  
2. หา peripheral ที่ตัวอย่างใช้ (เช่น GPIO สำหรับ LED หรือ UART)  
3. เปิด **Library Manager** แล้วดูรายการไลบรารีที่มีในโปรเจกต์  

ตอบสั้น ๆ:

1. BSP ของคุณชื่ออะไร  
2. ไลบรารีหนึ่งตัวที่เห็นใน Library Manager คืออะไร  
3. ถ้าเลือก BSP ผิดคิต จะเสี่ยงปัญหาแบบใด  

### Self-Check Guidance (Part 6)

1. ต้องตรงกับคิตจริง  
2. ตัวอย่างเช่น retarget-io, HAL/PDL/BSP packages ตามที่โปรเจกต์ดึงมา  
3. ขา/อุปกรณ์ไม่ตรงของจริง — LED/UART ไม่ออก หรือ program คนละเป้าหมาย

---

## Common Misconceptions

| ความเข้าใจผิด | แก้ไขอย่างไร |
|---|---|
| ติดตั้ง VS Code อย่างเดียวพอ | ต้องมี ModusToolbox™ tools + toolchain |
| เปิดโฟลเดอร์ย่อยสุ่มก็เหมือนเปิด workspace | เปิด `.code-workspace` ที่ระบบสร้างให้ |
| Build ผ่าน = เฟิร์มแวร์อยู่บนบอร์ดแล้ว | ต้อง program/flash แยก |
| แก้ไฟล์ใน `libs` เป็นทางลัดดีเสมอ | ใช้ Library Manager / โค้ดแอปเป็นหลัก |

---

## Submission Checklist

- [ ] Part 1 ตรวจเครื่องแล้ว  
- [ ] สร้างโปรเจกต์ BSP ตรงคิต  
- [ ] Build สำเร็จ  
- [ ] Flash แล้วเห็นผลบนบอร์ด  
- [ ] Debug halt ได้อย่างน้อยหนึ่งครั้ง  
- [ ] ตอบคำถาม Part 6 ครบ  

---

[Lesson](../l01-modustoolbox-and-vscode/README.md) · [Cheatsheet](../l01-modustoolbox-and-vscode/resources/toolchain-cheatsheet.md) · [Table of Contents](../../README.md) · [M03 →](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md)
