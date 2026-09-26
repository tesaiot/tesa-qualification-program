# Cheatsheet — ModusToolbox™ and VS Code Workflow (M02)

**Course 1 · Module 2**

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [← Table of Contents](../../../README.md)

---

## Roles

| Piece | Role |
|---|---|
| [ModusToolbox™](https://www.infineon.com/modustoolbox) | สร้างโปรเจกต์, libraries, configurators, OpenOCD recipes |
| [VS Code](https://code.visualstudio.com/) | แก้ไขโค้ด, build/debug UI |
| TESA Firmware SDK / libs | API ที่แอปเรียกใช้ |
| KitProg3 | Flash/debug บนคิต |

**Key phrase:** ModusToolbox™ สร้างโปรเจกต์และจัดการ toolchain — VS Code เขียนโค้ดและ debug — SDK คือ API

---

## First-Time Setup (Edge)

จาก [Edge quick start](https://documentation.infineon.com/modustoolbox/docs/psoc-edge-quick-start-guide) + [installation guide](https://www.infineon.com/modustoolboxsetupguide):

1. ModusToolbox™ Setup (tools **3.6+** หรือเวอร์ชันที่ชุดแล็บกำหนด)  
2. Arm GNU Toolchain (GCC)  
3. VS Code + extensions ที่กำหนด ([VS Code guide](https://documentation.infineon.com/modustoolbox/docs/visual-studio-code-for-modustoolbox-user-guide))  
4. Programming tools / KitProg access  
5. (Optional) [J-Link](https://www.segger.com/downloads/jlink/), DEEPCRAFT™ packs  

---

## Create → Open → Build → Program → Debug

```text
Dashboard / Project Creator
    → select BSP (must match kit)
    → select example (Hello World)
    → generate project
Open *.code-workspace in VS Code
    → build
    → program/flash via KitProg3 + OpenOCD
    → debug (breakpoint in main)
```

ตัวอย่างอ้างอิงหลักสูตร: **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**  
Host / Digital Twin ใน VS Code: **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)**  
แพ็กแล็บ (HEX / Flasher / VSIX / web-app): **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)**  
ตัวอย่าง Infineon เสริม: [mtb-example-psoc-edge-hello-world](https://github.com/Infineon/mtb-example-psoc-edge-hello-world)

---

## Everyday Tools

| Tool | Command / entry | Use |
|---|---|---|
| Device Configurator | `make device-configurator` | pins, clocks, peripherals |
| Library Manager | จาก Dashboard / IDE | add/remove/update libs |
| Build | IDE button หรือ `make` | compile/link |
| Program | launch config / make target **หรือ** TESAIoT Flasher + HEX | flash image |
| fw-loader | มากับ tools package | อัปเดต KitProg → KitProg3 |
| Lab pack | [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) | `hex/`, `flasher/`, `vsix/`, `web-app/` |

คู่มือรวม: [Tools package user guide (PDF)](https://www.infineon.com/assets/row/public/documents/30/68/infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf) · [AN235935 (PDF)](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf)

---

## Troubleshooting

| Symptom | Check |
|---|---|
| No kit / program fail | USB, KitProg3, driver, cable |
| Toolchain not found | tools install path, correct terminal |
| Runs wrong pins | wrong BSP ([KIT_PSE84_EVAL](https://www.infineon.com/evaluation-board/KIT-pse84-eval)) |
| No UART text | COM port, baud, retarget-io |
| Debug attach fail | OpenOCD busy port, [Cortex-Debug](https://github.com/Marus/cortex-debug) |

---

## Do / Don't

| Do | Don't |
|---|---|
| เลือก BSP ให้ตรงคิต | คัดลอก libs ข้ามโปรเจกต์มั่ว ๆ |
| เปิด `.code-workspace` | แก้ register ก่อนทำ Hello World สำเร็จ |
| ใช้ Library Manager | สันนิษฐานว่า build = ลงบอร์ดแล้ว |
