---
id: fw-sdk.m02.l01
lang: en
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
slides: slides.md
source_sha256: d7622e2f785140adf4387bba2de84597f97c4dd3dccd9804cc5bf925fa1a45a2
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C1/M02/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M02 — ModusToolbox and VS Code for Firmware Development

**Course 1 · Module 2**
**Suggested time:** about 2.5–3 hours (installing tools + creating a project + build / flash / debug)
**Format:** a hands-on lesson — uses a real development machine and board

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/toolchain-cheatsheet.md) · [← Table of Contents](../../README.md) · [← M01](../../m01-mcu-architecture/l01-architecture-and-sdk-layers/README.md) · [M03 →](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md)

> **If you plan to build from open source** (checked on 2026-09-26): the [tesaiot-pse84-devkit-sdk README](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/README.md) (commit `ef72c1b`) pins ModusToolbox™ to **3.6 only**, with the Arm GCC 14.2.1 that ships with ModusToolbox, building with `make build` and flashing with `make program`. The firmware used in modules 3–8 of this course is distributed as ready-made HEX and is not yet open source. See the note in the Module 3 lesson and on the [course page](../../README.md)

---

## Objectives (Learning Outcomes)

By the end of this lesson you should be able to:

1. Explain the role of **[ModusToolbox™](https://www.infineon.com/modustoolbox)** in creating and managing firmware projects on PSOC™ Edge
2. Set up the **Environment / Toolchain** needed to build on your machine
3. Use **[Visual Studio Code](https://code.visualstudio.com/)** together with the ModusToolbox™ ecosystem to edit code, **Build**, and **Debug**
4. Manage **Project Configuration**, **Device / BSP Selection** and **Library Management** at a practical level
5. Connect the tools to real hardware to **Flash** and **Debug** until an example program runs

This module takes you from the architecture map in [M01](../../m01-mcu-architecture/l01-architecture-and-sdk-layers/README.md) to a real workflow: creating a project on the kit's BSP, calling the SDK layers, and seeing code run on the board.

> **A note on versions**
> Infineon's manuals for PSOC™ Edge (such as the [PSOC™ Edge quick start guide](https://documentation.infineon.com/modustoolbox/docs/psoc-edge-quick-start-guide)) usually recommend **ModusToolbox™ tools 3.6 or newer**.
> Treat the version your own lab pack specifies as authoritative; if it differs from the numbers in this lesson, follow the lab pack.

### Read alongside this chapter

| Document | Use when |
|---|---|
| [ModusToolbox™ software installation guide](https://www.infineon.com/modustoolboxsetupguide) | Installing for the first time on Windows / Linux / macOS |
| [PSOC™ Edge quick start guide](https://documentation.infineon.com/modustoolbox/docs/psoc-edge-quick-start-guide) | Checking the packages you should install for Edge |
| [AN235935 — Getting started with PSOC™ Edge on ModusToolbox™](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf) | An overview of the tool architecture + the Hello World path |
| [Visual Studio Code for ModusToolbox™ user guide](https://documentation.infineon.com/modustoolbox/docs/visual-studio-code-for-modustoolbox-user-guide) ([PDF](https://www.infineon.com/assets/row/public/documents/30/44/infineon-visual-studio-code-user-guide-usermanual-en.pdf)) | Opening a project in VS Code, build / program / debug |
| [ModusToolbox™ tools package user guide](https://www.infineon.com/assets/row/public/documents/30/68/infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf) | Project Creator, Library Manager, configurators, the overall flow |
| [mtb-example-psoc-edge-hello-world](https://github.com/Infineon/mtb-example-psoc-edge-hello-world) | Infineon's own Hello World example (tools 3.6+) — extra reference |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | **The course's main example library** — Example Explorer, Code Editor, flowcharts, API Reference |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | **A host / Digital Twin inside VS Code** — Sensor Telemetry, Sensor Studio, connecting to a board or Simulator |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | **The lab pack** — HEX firmware, VSIX, the TESAIoT Flasher, web-app / BLE demos for flashing and practice |

---

## 1. Why Two Tools: ModusToolbox™ and VS Code

From M01 we already know that the **TESA Firmware SDK** is the set of libraries/APIs an app calls, while the development tools are a separate layer.

| Tool | Main role in this course | Read more |
|---|---|---|
| **[ModusToolbox™](https://www.infineon.com/modustoolbox)** | Installs the toolchain, creates projects from a BSP/template, manages libraries, opens configurators | [Tools package user guide](https://www.infineon.com/assets/row/public/documents/30/68/infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf) |
| **[Visual Studio Code](https://code.visualstudio.com/)** | Writing code, IntelliSense, build/debug through the workflow ModusToolbox™ supports | [VS Code for ModusToolbox™](https://documentation.infineon.com/modustoolbox/docs/visual-studio-code-for-modustoolbox-user-guide) |
| **KitProg3 / OpenOCD** (on the kit) | Flashing and debugging on real hardware | The Programming section of [AN235935](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf) |

> **Key phrase**
> **ModusToolbox™ creates projects and manages the toolchain/libraries — VS Code writes code and debugs — the SDK is the API the app calls.**

Infineon supports several IDEs, including Eclipse, VS Code, IAR Embedded Workbench and Arm® MDK (µVision), plus CLI-based work.
See the overview in [AN235935](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf) and the [tools package user guide](https://www.infineon.com/assets/row/public/documents/30/68/infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf)

This course focuses on the pairing of **ModusToolbox™ + VS Code**, because it is a common approach in modern learning and development teams, and has clear dedicated documentation.

---

## 2. ModusToolbox™ for Creating Firmware Projects

### 2.1 What ModusToolbox™ Is

**ModusToolbox™** is not just an IDE installer, but a **set of tools + libraries + a build system** for developing apps on Infineon MCUs, including the [PSOC™ Edge](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm) family.

Components you will use often in this course:

| Component | What it's for | Read more |
|---|---|---|
| **Setup / tools package** | Installing base tools, GCC, programming tools | [Installation guide](https://www.infineon.com/modustoolboxsetupguide) |
| **Dashboard** | A starting point for opening tools and creating projects | Linked from the Setup / docs of the installed version |
| **Project Creator** | Creating an app from a BSP + code example / template | [Tools package user guide — Project Creator](https://www.infineon.com/assets/row/public/documents/30/68/infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf) |
| **Library Manager** | Adding, removing, updating a project's libraries | The Library management section of [AN235935](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf) |
| **Device Configurator** | Setting up pins, clocks, peripherals, then generating config code | The Device Configurator guide in the tools package + `make device-configurator` |
| **Build system (`make`)** | Compiling / programming / opening tools through standard recipes | [Tools package user guide](https://www.infineon.com/assets/row/public/documents/30/68/infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf) |

The product page and the main download point: [ModusToolbox™](https://www.infineon.com/modustoolbox)
The Setup program is usually downloaded through the Infineon Development Center / Software Tools (the link in the [VS Code user guide PDF](https://www.infineon.com/assets/row/public/documents/30/44/infineon-visual-studio-code-user-guide-usermanual-en.pdf) points to `softwaretools.infineon.com`)

### 2.2 Recommended Install Set for PSOC™ Edge

Per the [PSOC™ Edge quick start guide](https://documentation.infineon.com/modustoolbox/docs/psoc-edge-quick-start-guide), in summary you should install at least:

1. **ModusToolbox™ Setup** per the [installation guide](https://www.infineon.com/modustoolboxsetupguide) for your OS
2. **Arm® GNU Toolchain (GCC)**
3. **The base tools package** version that supports Edge (**3.6+** per the quick start)
4. **An IDE of your choice** — this course chooses **VS Code** ([download VS Code](https://code.visualstudio.com/Download) if you don't have it)
5. **The programming tools package**, as offered by Setup
6. (If needed) the **Edge Protect Security Suite**, or an ML pack such as [DEEPCRAFT™](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84) / the Machine Learning Pack — not required for the first Hello World

> **LLVM (optional)**
> The quick start states that some work may need the [LLVM Embedded Toolchain for Arm](https://github.com/ARM-software/LLVM-embedded-toolchain-for-Arm/), which is **not included** in the standard Setup — install it additionally when your lab pack's guide says to

#### Practical install tips (from Infineon installation guidance)

- Use the **Setup program** as the main method from version 3.2 onward, since it helps choose tools, IDE and toolchain as a set
- If creating an app or adding a library reports a missing package, go back and open Setup / install the missing package (Project Creator and Library Manager usually warn when an asset is missing)
- A network that blocks GitHub may affect pulling BSPs/libraries — see the proxy / manifest section of the [installation guide](https://www.infineon.com/modustoolboxsetupguide) and the Project Creator guide of the version installed

### 2.3 Creating a Project with Project Creator

Project Creator has both a GUI and a CLI, installed under ModusToolbox™'s tools folder (such as `.../ModusToolbox/tools_<version>/project-creator`).
Step-by-step detail is in the [tools package user guide](https://www.infineon.com/assets/row/public/documents/30/68/infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf) and the [VS Code for ModusToolbox™ guide](https://documentation.infineon.com/modustoolbox/docs/visual-studio-code-for-modustoolbox-user-guide)

The standard sequence:

1. Open the **ModusToolbox™ Dashboard**, or open **Project Creator** directly
2. Choose the **Kit / BSP** that matches the board in hand, such as the [KIT_PSE84_EVAL](https://www.infineon.com/evaluation-board/KIT-pse84-eval) family you have
3. Choose a starting **code example** or template
   - **Course recommendation:** open an example from the **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** (filter by Board / Domain to match your kit), then download or open it per your lab pack's guide
   - **A vendor alternative:** [Hello World for PSOC™ Edge](https://github.com/Infineon/mtb-example-psoc-edge-hello-world), when you want to compare against Infineon's raw example
4. In the Target IDE, choose **Visual Studio Code / Microsoft Visual Studio Code** so the workspace file and related config are generated
5. Give a destination folder, then let the tool **clone the BSP/template and pull the needed libraries from the manifest**

Expected result:

- A project structure ready for the `make` system
- The libraries/BSP already pulled in
- A `*.code-workspace` file for VS Code

The course's example library: **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**
Infineon's own combined example library (extra): [Code Examples for ModusToolbox™ Software](https://github.com/Infineon/Code-Examples-for-ModusToolbox-Software)

### 2.4 Typical Application Structure (Mental Model)

The real structure depends on the template, but the concept is usually similar:

```text
my-app/
  ├── *.code-workspace          # opened with VS Code
  ├── Makefile / makefiles      # ModusToolbox™'s build system
  ├── main.c / source/           # your app code
  ├── deps / libs / bsps ...    # pulled-in libraries and BSP (folder names vary by version)
  ├── configs / design.modus    # config from the Device Configurator (if any)
  └── build/                    # build output (created when compiling)
```

**Professional practice**

- Edit product code at the app layer; make a habit of not editing inside library folders
- Add/update dependencies through the **Library Manager**
- Commit only what the team agrees on (some teams don't commit the whole `libs` folder — per team policy)

---

## 3. Environment and Toolchain

### 3.1 What "Environment" Means Here

Before you can build, the machine needs at least:

| Component | What it's for | Reference |
|---|---|---|
| ModusToolbox™ tools | Project Creator, Library Manager, make recipes, OpenOCD, etc. | [Installation guide](https://www.infineon.com/modustoolboxsetupguide) |
| Arm GNU Toolchain (GCC) | Compiling C code into a binary for Cortex-M | [Edge quick start](https://documentation.infineon.com/modustoolbox/docs/psoc-edge-quick-start-guide) |
| VS Code + extensions | Editing and debugging | [VS Code guide](https://documentation.infineon.com/modustoolbox/docs/visual-studio-code-for-modustoolbox-user-guide) |
| USB access for KitProg | Letting the host see the debugger on the board | [AN235935 — Programming and Debugging](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf) |
| A terminal emulator | Viewing UART logs from an example | The [Hello World example](https://github.com/Infineon/mtb-example-psoc-edge-hello-world)'s README often recommends one, such as Tera Term |
| **Bitstream Studio** (recommended install) | A host app in VS Code — Sensor Telemetry / Sensor Studio / a digital twin connected to the board after flashing | [Marketplace — TERNIONDEV.bitstream-studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) |
| **The TESAIoT_Hackathon pack** | Ready-made HEX, the TESAIoT Flasher, a backup VSIX, web-app demos | [github.com/drsanti/TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) |

### 3.2 Path and Tool Discovery

ModusToolbox™'s build system expects to find the tools package at the standard install path.
If it is installed in the wrong place, or several versions overlap, you often see:

- `make` cannot find the compiler
- The configurator won't open
- Program/debug fails even though the board is plugged in

Basic troubleshooting steps:

1. Reinstall or repair through the [Setup / installation guide](https://www.infineon.com/modustoolboxsetupguide)
2. Open a terminal from the workflow the VS Code / tools package documentation recommends
3. In the project folder, try a standard target, such as `make help` or `make build` (target names may differ by template — check the project's Makefile)

### 3.3 Optional: J-Link Instead of On-board KitProg

The [Edge quick start](https://documentation.infineon.com/modustoolbox/docs/psoc-edge-quick-start-guide) states the **SEGGER J-Link** alternative:

1. Install the [J-Link software](https://www.segger.com/downloads/jlink/) and note the path
2. Edit the BSP file (such as `bsp.mk`) and add `BSP_PROGRAM_INTERFACE=JLink`
3. If installed outside the standard path, add `MTB_JLINK_DIR=...`, for example
   - Windows: `C:/Program Files/SEGGER/JLink_V852`
   - macOS: `/Applications/SEGGER/JLink_V852`
   - Linux: `/opt/SEGGER/JLink_V852`

Most people use the **on-board KitProg** first — switch to J-Link only when needed.

---

## 4. Using VS Code with the SDK (Edit, Build, Debug)

The main documentation for this section:
[Visual Studio Code for ModusToolbox™ user guide](https://documentation.infineon.com/modustoolbox/docs/visual-studio-code-for-modustoolbox-user-guide) · [PDF](https://www.infineon.com/assets/row/public/documents/30/44/infineon-visual-studio-code-user-guide-usermanual-en.pdf)

### 4.1 Opening the Project

The standard sequence:

1. Create a project with Project Creator, choosing VS Code as the target, or create one and obtain the workspace file
2. Open **VS Code by hand**
3. Open the **`{project-name}.code-workspace`** file in the project folder

Don't just open a random subfolder and lose the task / launch configuration — open the workspace file the tool created for you.
More detail is in the "Using the code example" section of several repos, such as the [Hello World docs flow](https://github.com/Infineon/mtb-example-psoc-edge-hello-world)

### 4.2 Extensions and Assistant

Infineon's VS Code guide references:

- The **ModusToolbox™ Assistant** extension/workflow (depending on the version) to help create apps and open tools
- **[Cortex-Debug](https://github.com/Marus/cortex-debug)** for extra Cortex-M debugging capability in VS Code

If your lab pack states a locked set of extensions — install per that list so you can:

- Create/open apps from VS Code
- Run build / program / debug configurations
- Open the Device Configurator and other tools from the helper panel

### 4.3 Build

Whether you press a button in VS Code or use a terminal, the same principle applies: it calls the **project's make system** that ModusToolbox™ set up.
See the build/program/debug overview in the [tools package user guide](https://www.infineon.com/assets/row/public/documents/30/68/infineon-modustoolbox-tools-package-user-guide-gettingstarted-en.pdf)

What to check when a build succeeds:

- No errors from the compiler / linker
- An output file exists in the `build` folder as the template defines it
- After changing the BSP/a library, it still builds again

### 4.4 Program vs Debug

| Action | Meaning |
|---|---|
| **Program / Flash** | Writing firmware into the device's memory |
| **Debug** | Usually includes programming, then halting at a breakpoint / stepping through code via GDB + OpenOCD or another probe |

[AN235935](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf) states that ModusToolbox™ supports an **OpenOCD + GDB server**, and probes such as **KitProg3** or **J-Link**.
For a standalone PSOC™ Programmer (program/erase/verify/read), see Infineon's Programming tools documentation that comes with Setup.

---

## 5. Project Configuration, Device Selection, and Library Management

### 5.1 Device / BSP Selection

The **BSP (Board Support Package)** tells the project:

- Which chip/board is being used
- How pins and on-board devices are mapped
- Which libraries must be pulled in at a minimum

Choosing the wrong BSP when creating a project = the code may still build, but **the LED/UART pins won't match the real thing**.

A simple rule: **choose the BSP that matches the kit plugged in**.
Reference kit examples: [KIT_PSE84_EVAL](https://www.infineon.com/evaluation-board/KIT-pse84-eval) · the [PSOC™ Edge E84](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm/psoc-edge-e84) page

An example Device Support Library on GitHub: [mtb-dsl-pse8xxgp](https://github.com/Infineon/mtb-dsl-pse8xxgp)

### 5.2 Device Configurator

Open it from the IDE workflow, or from the project folder:

```bash
make device-configurator
```

Per the [VS Code for ModusToolbox™ guide](https://www.infineon.com/assets/row/public/documents/30/44/infineon-visual-studio-code-user-guide-usermanual-en.pdf), it is used to:

- View/enable peripherals
- Set up pins, clocks, DMA, etc.
- Generate config code that links into the build
- Open other related configurators (such as CAPSENSE™, QSPI) that the BSP supports

Each resource you open usually has a link to related API documentation.

> For PSOC™ Edge: setting up and initialising most peripherals is designed to be done through the **configurator + PDL** (review [M01 §7–8](../../m01-mcu-architecture/l01-architecture-and-sdk-layers/README.md)).
> In M02, practise "opening and recording the config" before writing deeper Drivers in M03.

### 5.3 Library Manager

The **Library Manager** helps you:

- Add middleware / libraries
- Remove unused ones
- Update versions per Infineon's manifest on GitHub

Use it when you need an extra feature, such as `retarget-io` (UART printf), `abstraction-rtos`, connectivity — don't copy libraries randomly from another project.
See the library management explanation in [AN235935](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf)

### 5.4 Project Configuration Checklist

Before deciding the project is ready to keep developing:

- [ ] The BSP matches the kit
- [ ] It opens in VS Code through `.code-workspace`
- [ ] The build succeeds
- [ ] You know how to open the Device Configurator and the Library Manager
- [ ] You know which file/folder the app code is in

---

## 6. Flash and Debug on Real Hardware

### 6.1 Hardware Prerequisites

- The PSOC™ Edge kit you're using (such as [KIT_PSE84_EVAL](https://www.infineon.com/evaluation-board/KIT-pse84-eval))
- A USB cable that can power and talk to **KitProg**
- (If any) a UART port per the kit's guide — some kits use USB-UART through KitProg

### 6.2 KitProg3 and fw-loader

Infineon kits usually have an on-board programmer called **KitProg**.
ModusToolbox™ expects **KitProg3** (CMSIS-DAP), which is faster than HID mode in many cases, as explained in the VS Code / tools guides.

If the kit is old, or the firmware doesn't match:

- Use **fw-loader**, which ships with ModusToolbox™, to update KitProg
- On Linux, you may need to install udev rules before first using fw-loader

Read the KitProg section of the [VS Code user guide PDF](https://www.infineon.com/assets/row/public/documents/30/44/infineon-visual-studio-code-user-guide-usermanual-en.pdf) and [AN235935](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf) for details

### 6.3 Prebuilt HEX, Flasher, and Lab Pack

When choosing to use ready-made firmware (not building from source at that point), or when you need the matching flasher / VSIX installer, use the pack from:

**[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)**

| Folder in the repo | What it's for |
|---|---|
| [`hex/`](https://github.com/drsanti/TESAIoT_Hackathon/tree/main/hex) | The DevKit's `.hex` files — flash before the hardware lab |
| [`flasher/`](https://github.com/drsanti/TESAIoT_Hackathon/tree/main/flasher) | The **TESAIoT Flasher** installer (Windows / macOS / Linux) |
| [`vsix/`](https://github.com/drsanti/TESAIoT_Hackathon/tree/main/vsix) | Bitstream Studio's `.vsix` (an install alternative outside the Marketplace) |
| [`web-app/`](https://github.com/drsanti/TESAIoT_Hackathon/tree/main/web-app) | HTML telemetry examples for practice after connecting to the host |

> Match the **VSIX with the HEX** version per the repo's README recommendation (see the `latest` entry in the firmware manifest, when present)

Other flashing options in this course: **ModusToolbox™ Program** from a project you build yourself (the previous section), or the TESAIoT Flasher + HEX from this repo.

### 6.4 First Success Criteria (Hello World Path)

The minimum goal of M02:

1. Build the example project successfully **or** successfully flash a HEX from the lab pack
2. Successfully program the board
3. See confirmable behaviour, such as a blinking LED, and/or a message on the serial terminal / telemetry in Bitstream Studio
4. Open a debug session, at least halting at `main` or a simple breakpoint (when using the build-from-source path)

The course's reference path (code examples): **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**
The lab-pack reference path (HEX / Flasher / demos): **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)**
The vendor's reference path (extra): [mtb-example-psoc-edge-hello-world](https://github.com/Infineon/mtb-example-psoc-edge-hello-world) + the steps in [AN235935](https://www.infineon.com/row/public/documents/30/42/infineon-an235935-getting-started-with-psoc-edge-e8-modustoolbox-applicationnotes-en.pdf)

Once you meet this bar, you are ready for M03 to call the Driver API systematically.

### 6.5 Troubleshooting Quick Table

| Symptom | What to check | Read more |
|---|---|---|
| The board doesn't appear / won't program | The USB cable, port, KitProg3, drivers, try another port | KitProg / fw-loader in the VS Code guide · [Hackathon troubleshooting](https://github.com/drsanti/TESAIoT_Hackathon) |
| The build can't find the toolchain | Install GCC/tools per Setup, open the correct terminal | [Installation guide](https://www.infineon.com/modustoolboxsetupguide) |
| The build succeeds but nothing happens on the board | The BSP doesn't match the kit, it hasn't been programmed yet, you're watching the wrong LED/UART | Check the BSP against the kit's page |
| Debug won't connect | OpenOCD/KitProg, close programs holding the port, check the launch config | [Cortex-Debug](https://github.com/Marus/cortex-debug) + the VS Code guide |
| No message over Serial | The baud rate, the COM port, the example has no retarget-io/UART yet | The code example's README |
| Flashing the HEX gives no telemetry | The VSIX and HEX are mismatched versions, the baud isn't 921600, you haven't Linked in Bitstream Studio yet | The [TESAIoT_Hackathon README](https://github.com/drsanti/TESAIoT_Hackathon) |

---

## 7. How This Connects to TESA Firmware SDK

Once the project is ready, you are standing on the same stack you learned in M01:

```text
VS Code (edit / build / debug)
        │
ModusToolbox™ tools (create, libraries, configurators, OpenOCD)
        │
Application  →  Utility / Driver API (the TESA Firmware SDK in this course)
        │
BSP / PDL / HAL (Device Support)
        │
PSOC™ Edge hardware
```

- M02 makes you **ready to create and run a project on real tools**
- M03 will have you **call the Driver API** on that project, deliberately

Review the software layers: [M01 — Software Ecosystem](../../m01-mcu-architecture/l01-architecture-and-sdk-layers/README.md) · [Device Support Library (pse8xxgp)](https://github.com/Infineon/mtb-dsl-pse8xxgp)

---

## 8. Module Summary

1. **ModusToolbox™** creates projects from a BSP/template and manages the toolchain / libraries / configurators
2. **The right environment** = tools + GCC + VS Code + KitProg access
3. Open the project through the **`.code-workspace`**, then build/debug per the Infineon workflow
4. **The BSP must match the kit**; use the Device Configurator and Library Manager as the main path
5. **Flashing + debugging on real hardware** is this module's pass criterion

### Next Steps

1. Do the hands-on exercise: [Lab](../l02-lab/README.md)
2. Keep the summary sheet: [Cheatsheet](resources/toolchain-cheatsheet.md)
3. When ready, continue to **M03 — GPIO and Basic Peripherals** ([M03 lesson](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md))

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

9. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** — Example Explorer, flowcharts, API Reference (the course's main example source)
10. [mtb-example-psoc-edge-hello-world](https://github.com/Infineon/mtb-example-psoc-edge-hello-world) — an extra Infineon example
11. [Code Examples for ModusToolbox™ Software](https://github.com/Infineon/Code-Examples-for-ModusToolbox-Software)
12. [mtb-dsl-pse8xxgp (Device Support Library)](https://github.com/Infineon/mtb-dsl-pse8xxgp)

### Related tools

13. [Visual Studio Code](https://code.visualstudio.com/) · [Download](https://code.visualstudio.com/Download) · [Docs](https://code.visualstudio.com/docs)
14. [Cortex-Debug extension (GitHub)](https://github.com/Marus/cortex-debug)
15. [SEGGER J-Link](https://www.segger.com/downloads/jlink/) (optional probe)
16. [LLVM Embedded Toolchain for Arm](https://github.com/ARM-software/LLVM-embedded-toolchain-for-Arm/) (optional)
17. [OpenOCD](https://openocd.org/) / KitProg3, per your kit's guide

### Host application / Digital Twin

18. **[Bitstream Studio — Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** (`TERNIONDEV.bitstream-studio`) — a VS Code extension for Sensor Telemetry, Sensor Studio, a 3D digital twin, and a host connecting to firmware on TESAIoT / PSoC Edge (USB / Wi‑Fi / MQTT, or a Simulator)

### Lab pack / flash / demos

19. **[TESAIoT_Hackathon (GitHub)](https://github.com/drsanti/TESAIoT_Hackathon)** — HEX firmware (`hex/`), the TESAIoT Flasher (`flasher/`), VSIX (`vsix/`), web-app telemetry demos (`web-app/`) for hands-on practice

---

## Check your understanding

Three short questions in [quiz.yaml](quiz.yaml), one per objective of this lesson. Try answering them yourself first, then compare with the answer key and explanations in the file.

## Lab

Continue hands-on at [Lab: create, build, flash and debug a firmware project](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/toolchain-cheatsheet.md) · [← Table of Contents](../../README.md) · [← M01](../../m01-mcu-architecture/l01-architecture-and-sdk-layers/README.md) · [M03 →](../../m03-gpio-peripherals/l01-gpio-and-peripherals/README.md)

## Examples on the TESAIoT Developer Hub

Try the real thing on the TESAIoT Dev Kit: open examples on the Developer Hub to read the code, download it, or flash ready-made firmware.

- Related lesson: [TESAIoT Firmware Stack 1.1 · Tools, boards, and the master template](../../../tesaiot-firmware-stack/m01-getting-started/l01-toolchain-and-master-template/README.md)
