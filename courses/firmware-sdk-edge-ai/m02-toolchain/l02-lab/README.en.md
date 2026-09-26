---
id: fw-sdk.m02.l02
lang: en
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
translation: done
source_sha256: 60905822e294cc67d4e313feda8c9a898030f8e7725b5e758138b742a7ea6304
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

Once complete, you will:

- Have the ModusToolbox™ + VS Code environment installed/checked and ready
- Create a project from the BSP of the kit in hand
- Build successfully in VS Code or a terminal
- Flash and confirm the result on the real board
- Open a debug session at least once

---

## Prerequisites

- [ ] Have finished reading the [lesson](../l01-modustoolbox-and-vscode/README.md)
- [ ] The machine is installed per the lesson's list (or per your lab pack's guide)
- [ ] A PSOC™ Edge board + a USB cable
- [ ] Know the code/name of the kit used to pick the BSP

> **After a successful flash — watch telemetry on the host**
> Install **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** from the Marketplace (or from `vsix/` in the lab pack), then use the Command Palette → **Bitstream Studio: Open Bitstream Studio** / **Start Serial Bridge**
>
> **The HEX / Flasher / demos pack:** **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** — clone or download the ZIP, then use `hex/` + `flasher/` per the repo's README (match versions with the VSIX)

---

## Part 1 — Environment Check

Record the result in your notes:

| Item | Present? | Notes |
|---|---|---|
| ModusToolbox™ tools (state the version) | | |
| Arm GNU Toolchain (GCC) | | |
| VS Code | | |
| The extensions your lab pack requires | | |
| A terminal emulator (if you need to watch UART) | | |

**Pass when:** you have checked all the above and the machine is ready, or you can create a new project in Part 2

---

## Part 2 — Create a Project

1. Open the **ModusToolbox™ Dashboard** or **Project Creator**
2. Choose the **BSP/Kit** that matches the board in hand
3. Choose a starting example
   - Recommended: open one from the **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** (Example Explorer → filter by Board to match your kit)
   - Or Infineon's Hello World, if you choose that path
4. Choose **VS Code** as the target
5. Create the project into a neatly named folder (avoid a path with unusual spaces, if possible)

Record:

- Project name: _______________
- BSP chosen: _______________
- Folder path: _______________

**Pass when:** a `.code-workspace` file exists in the project

---

## Part 3 — Open in VS Code and Build

1. Open the **`*.code-workspace`** file with VS Code
2. Run a **build** per your chosen workflow (a button in the IDE, or `make` in the project terminal)
3. Fix any basic errors if there are any (toolchain / path / library)

| Build result | Notes |
|---|---|
| Time for the first success | |
| Errors found (if any) and how you fixed them | |

**Pass when:** the build succeeds with no errors

---

## Part 4 — Flash to the Board

1. Plug in USB so KitProg is ready
2. Program/Flash per the launch config or the command the documentation specifies
3. Observe the result on the board (LED / behaviour per the example)
4. If the example has UART: open a terminal at the baud rate per the guide, and record the message you get

**Pass when:** you see behaviour confirming the new firmware is running on the board

---

## Part 5 — Debug Once

1. Set a breakpoint in `main`, or a function that's obvious in the example
2. Start a debug session
3. Confirm it halts at the breakpoint, then resume/step at least once

Record:

- The configuration name used: _______________
- Halted at line/function: _______________

**Pass when:** debugging works for at least one round

---

## Part 6 — Configuration Awareness (Light)

You don't need to redesign the whole board — just open and look:

1. Open the **Device Configurator** (`make device-configurator`, or from the IDE)
2. Find the peripheral the example uses (such as GPIO for the LED, or UART)
3. Open the **Library Manager** and look at the list of libraries the project has

Answer briefly:

1. What is your BSP's name?
2. Name one library you see in the Library Manager
3. If you chose the wrong BSP for the kit, what kind of problem would you risk?

### Self-Check Guidance (Part 6)

1. It must match the real kit
2. Examples such as retarget-io, or HAL/PDL/BSP packages the project pulled in
3. Pins/devices won't match the real thing — the LED/UART doesn't work, or you program the wrong target

---

## Common Misconceptions

| Misconception | How to fix it |
|---|---|
| Installing VS Code alone is enough | You also need ModusToolbox™ tools + the toolchain |
| Opening a random subfolder is the same as opening the workspace | Open the `.code-workspace` file the system created for you |
| A successful build = the firmware is already on the board | You still need a separate program/flash step |
| Editing files in `libs` is always a good shortcut | Use the Library Manager / app code as the main path |

---

## Submission Checklist

- [ ] Part 1's machine check done
- [ ] A project created with the BSP matching the kit
- [ ] The build succeeded
- [ ] Flashed and saw the result on the board
- [ ] Debugging halted at least once
- [ ] Part 6's questions all answered

---

[Lesson](../l01-modustoolbox-and-vscode/README.md) · [Cheatsheet](../l01-modustoolbox-and-vscode/resources/toolchain-cheatsheet.md) · [Table of Contents](../../README.md) · [M03 →](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md)
