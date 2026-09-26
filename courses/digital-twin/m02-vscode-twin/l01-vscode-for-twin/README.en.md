---
id: twin.m02.l01
lang: en
title:
  th: ตั้งโฮสต์ Twin ใน VS Code ด้วย Bitstream Studio
  en: Setting up the Twin Host in VS Code with Bitstream Studio
summary:
  th: ติดตั้ง Bitstream Studio (Marketplace หรือ VSIX) จัด workspace ผูกเฟิร์มแวร์ รู้จัก backend services และไล่ปัญหาเมื่อ UI ว่าง
  en: Install Bitstream Studio (Marketplace or VSIX), organise the workspace, bind the firmware, know the backend services and debug an empty UI.
level: L3
time_min:
  concept: 40
  practise: 25
  check: 10
hardware:
  emulator: true
  boards:
  - devkit
prerequisites:
- twin.m01.l02
objectives:
- th: ติดตั้ง Bitstream Studio ด้วยเส้นทาง Marketplace หรือ VSIX และเลือกเวอร์ชัน VSIX ให้ตรงกับ HEX
  en: Install Bitstream Studio from the Marketplace or a VSIX and match the VSIX version to the HEX.
- th: เปิดเซสชันแรกแบบ Simulator หรือ Bitstream (UART) จนเห็นค่าเซ็นเซอร์ขยับบนแผง telemetry
  en: Open a first Simulator or Bitstream (UART) session until sensor values move on the telemetry panel.
- th: ไล่หาสาเหตุเมื่อ UI ว่างตามลำดับ extension → backend → link → source streaming → แผงที่ถูกต้อง
  en: 'Troubleshoot an empty UI in order: extension, backend, link, source streaming, correct panel.'
develops:
- skill: iot.digital-twin
  to: 2
- skill: sys.simulation
  to: 2
context:
  platform: psoc-edge-e84
  host: bitstream-studio
  ide: vscode
  simulator: Bitstream Simulator (not the BENTO Emulator)
status: alpha
translation: done
source_sha256: 01aff8ac879063e78467c5e5c1246768a2ad02b4a4e67377f54151801433a2ee
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C2/M02/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M02 — VS Code for Twin Development

**Course 2 · Module 2**
**Suggested time:** about 3 hours (installing + binding the workspace + a first session)
**Format:** a hands-on lesson — setting up the Twin host in VS Code and watching telemetry in real time

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/vscode-twin-setup.md) · [← Table of Contents](../../README.md) · [← M01](../../m01-twin-architecture/l01-twin-architecture/README.md) · [M03 →](../../m03-virtual-device/l01-virtual-device-modeling/README.md)

---

## Objectives (Learning Outcomes)

By the end of this lesson you should be able to:

1. Install and configure the **VS Code extension** for TESAIoT / Digital Twin — **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)**
2. Organise the **workspace** and bind the firmware project (or the lab's HEX) to the Twin host
3. **Run / Link** a first session: **Simulator** mode and/or **Bitstream (UART)** mode, watching the result in real time
4. Use the **Console / Logs / Visualization** (Sensor Telemetry, Sensor Studio, the backend's status) to check the data

This module takes you from the architecture map in [M01](../../m01-twin-architecture/l01-twin-architecture/README.md) to **a ready-to-use tool** — the next lesson ([M03](../../m03-virtual-device/l01-virtual-device-modeling/README.md)) will have you build a Virtual Device and event scripts yourself.

> **Course 2's main host**
> The course documentation may call it *TESA Digital Twin / VS Code Extension* — in the lab, install and open **Bitstream Studio** (from the Marketplace, or a VSIX from Hackathon) as the same single entry point.

### Read alongside this chapter

| Document | Use when |
|---|---|
| **[Bitstream Studio (Marketplace)](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | Installing the extension from the Marketplace |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | The lab pack: `vsix/`, `hex/`, `flasher/`, `web-app/` |
| **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** | GLB / textures / cubemaps / images — the Free Loader, or browse [`assets/`](https://github.com/drsanti/ternion-3d-assets-free/tree/main/assets) |
| [Visual Studio Code](https://code.visualstudio.com/) | The editor / the extension's host |
| [Course 1 M02 — ModusToolbox + VS Code](../../../firmware-sdk-edge-ai/m02-toolchain/l01-modustoolbox-and-vscode/README.md) | Building / flashing the firmware (alongside the Twin host) |
| [M01 — Twin Architecture](../../m01-twin-architecture/l01-twin-architecture/README.md) | The Communication / Visualization layers |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | Firmware examples to bind in the workspace |

---

## 1. Why VS Code Is the Hub

In Course 2, **Visual Studio Code** is not just a code editor — it is the central point connecting:

| Piece | Role |
|---|---|
| The firmware project | From Course 1 / ModusToolbox / a lab folder |
| **Bitstream Studio** | The Twin host — telemetry, Sensor Studio, MQTT, 3D |
| **Bitstream Simulator** (extra) | A virtual MCU when there is no board |
| Backend services | A serial bridge, an MQTT broker on localhost |
| Visualization | Graphs / panels / a dashboard |

This lesson's goal: **install → bind the project → Link a first session → see values move**, all in one environment.

```text
[VS Code]
   ├─ Firmware folder (edit / debug)
   ├─ Bitstream Studio webview  ← Twin UI
   ├─ Bridge :9998              ← Communication
   └─ (optional) Simulator VSIX ← Virtual device stream
```

> **Key phrase**
> Course 1 M02 teaches *building and flashing firmware* — Course 2 M02 teaches *opening a Twin host to talk to the firmware or the Simulator*.

---

## 2. Install the Twin Extension

### 2.1 What to install

| Piece | Required when |
|---|---|
| [VS Code](https://code.visualstudio.com/) or Cursor | Always |
| **Bitstream Studio** (`TERNIONDEV.bitstream-studio`) | Always — the Twin host |
| **Bitstream Simulator** (a companion VSIX) | When you'll use **Simulator** mode, with no board |
| The [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) pack | Recommended — matched VSIX/HEX/Flasher versions |

### 2.2 Path A — Visual Studio Marketplace

1. Open Extensions in VS Code
2. Search for **Bitstream Studio**, or open the [Marketplace page](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)
3. **Install** → Reload when prompted
4. Command Palette → **Open Bitstream Studio**

### 2.3 Path B — Hackathon VSIX (lab pack)

Suited to when you need to lock the version to match the HEX:

1. Clone or download [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)
2. Open the `vsix/` folder and choose `bitstream-studio-<version>.vsix` at the version you want
3. Extensions → **…** → **Install from VSIX…**
4. Reload → **Open Bitstream Studio**

An example from the terminal (change the filename to match the version used):

```bash
code --install-extension vsix/bitstream-studio-0.1.8.vsix
code -r
```

(use `cursor` instead of `code` if using Cursor)

> **Version matching**
> The VSIX and the HEX should be from the same set — check the `latest` entry in Hackathon's firmware manifest when unsure.

### 2.4 Credentials / CA (when required)

Some lab kits may have a step to trust a certificate or enter credentials for an internal network service.

- If your round's guide **has** this step — do it before Lab C, and note it in the [setup sheet](resources/vscode-twin-setup.md)
- If using only the localhost bridge / general Marketplace — a special CA is usually **not needed**

Never commit a password or a token into a deliverable file.

### 2.5 Verify the extension is alive

After installing, check at least one of these:

| Check | Passes when |
|---|---|
| The Command Palette has **Open Bitstream Studio** | The command appears |
| The status bar shows a Bitstream / backend status | No stuck error |
| Opening Studio shows a toolbar (Bitstream / Simulator, Link) | The UI loads |

Record the extension's version in the cheatsheet.

### 2.6 Free 3D assets (models / textures / images)

When the Twin or Sensor Studio needs a GLB model, a cubemap, or an image, use the official source:

**[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** — content lives under [`assets/`](https://github.com/drsanti/ternion-3d-assets-free/tree/main/assets) on the `main` branch

| Method | Use when |
|---|---|
| Command Palette → **Download Free Assets from GitHub** | Syncing to your machine for the first time / updating the pack |
| Browsing on GitHub | Finding `models/`, `textures/`, images |
| The online fallback in Studio | Base `…/main/assets` (a relative path such as `models/…/*.glb`) |

No need to copy assets from someone else's private workspace into your report.

---

## 3. Workspace Structure and Binding Firmware

### 3.1 Recommended layout

The folder names don't need to be exact — what matters is that it is **clearly separated** and can be reopened:

```text
my-course2-workspace/
  firmware/          # a C project from MTB / TESA (or a link to a Course 1 project)
  lab-notes/         # notes / screenshots / a setup sheet
  .vscode/           # team tasks / settings (if any)
```

A host-first alternative:

```text
my-course2-workspace/
  hackathon/         # a clone of TESAIoT_Hackathon (vsix + hex for reference)
  firmware/          # the project you actually edit
  lab-notes/
```

### 3.2 What "binding" means in this course

In Bitstream Studio, binding a project to the Twin doesn't always mean there has to be a special hidden config file — in practice, it means:

| Step | What to do |
|---|---|
| 1 | Open the workspace folder that has the firmware (or at least know the path to build/flash) |
| 2 | Open **Bitstream Studio** in the same window |
| 3 | Choose the data source: **Simulator** or **Bitstream** + the correct COM |
| 4 | (If you have a board) flash the HEX matched to the VSIX, then open the port |
| 5 | Press **Link / Connect** until you see a stream |

If using ModusToolbox + VS Code to debug on a kit — keep launch/tasks configs per [Course 1 M02](../../../firmware-sdk-edge-ai/m02-toolchain/l01-modustoolbox-and-vscode/README.md) in the firmware project's `.vscode/`, and use Studio alongside it as the Twin screen.

### 3.3 Device / profile selection

| Situation | Choose |
|---|---|
| No board today | **Simulator** + start the Bitstream Simulator |
| Have a DevKit + a matching-version HEX | **Bitstream** + open the COM (baud per the firmware — usually 921600) |
| Switching mode midway | Change the toolbar one mode at a time — **never mix** uart+sim in your head |

Remember from M01: only one backend can exist at a time.

---

## 4. Backend Services (What Starts Automatically)

Once you open Bitstream Studio (VSIX), the system usually **auto-starts** a backend on your machine, such as:

| Service | Common port | Role |
|---|---|---|
| Serial / WS bridge | **9998** | Talks between the webview ↔ UART / Simulator |
| An MQTT broker (local) | **1883** / **8883** | Used in a later cloud lab (M05) |

Useful commands (Command Palette — names may start with **Bitstream Studio:**):

| Approximate command | Use when |
|---|---|
| Open Bitstream Studio | Opening the main UI |
| Start / Stop Bitstream Simulator | The board-free mode |
| Start All / Shutdown Backend Services | Fixing a port conflict, or switching to a dev terminal |
| **Download Free Assets from GitHub** | Syncing models/textures from [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free) |
| Open Connection Panel / Setup Checklist | Recovering a first session |

> **Multi-editor tip**
> You can open VS Code and Cursor at the same time, but the bridge has only one owner — if a port is stuck, shut it down from the window that owns it, then reopen.

---

## 5. First Run / Debug Loop with Live Results

### 5.1 Path — Simulator (recommended first)

The sequence that reduces hardware risk:

1. Install Bitstream Studio (+ Simulator, if you want the board-free mode)
2. **Open Bitstream Studio**
3. Toolbar → data source **Simulator**
4. Start the Simulator / Streaming (or let Studio help Start it on Link)
5. Press **Link / Connect**
6. Open **Sensor Telemetry** (or whichever graph panel you want)

**Passes when:** you see simulated sensor values move within a few seconds, and the link status is normal

### 5.2 Path — Bitstream (real board)

1. Flash a HEX from Hackathon (`hex/`) with the Flasher or ModusToolbox — a version matching the VSIX
2. Plug in USB / choose the COM
3. Toolbar → **Bitstream**
4. **Link / Connect** until the handshake succeeds
5. Watch the Telemetry / Sensor Studio

**Passes when:** there is a stream from the board (origin on the uart side), and the UI is not empty

### 5.3 Firmware edit + observe (when building yourself)

A loop worth practising at least once:

```text
Edit firmware (VS Code / MTB)
  → Build + Flash (Course 1 skills)
  → Link in Bitstream Studio
  → Watch telemetry / logs
  → Change one variable or rate
  → Re-flash / reconnect → confirm UI changes
```

If today you only use a ready-made HEX — the lab still counts as passed once the **host session** succeeds; editing code is emphasised in M04.

### 5.4 What to watch on day one

| Area | What to look at |
|---|---|
| **Toolbar** | Bitstream vs Simulator, the Link state, the MQTT chip (if enabled) |
| **Sensor Telemetry** | The graph/latest value moving |
| **Sensor Studio** | Nodes/a preview (if enabled) |
| **Output / extension logs** | Errors when the backend starts |
| **The UART console** (if any) | A heartbeat from the firmware |

Split problems into layers (from easy → hard):

1. The extension isn't ready yet / has no commands
2. The backend has a port conflict
3. Not Linked yet, or the wrong mode was chosen
4. The firmware/Simulator isn't streaming yet
5. Visualization is a different workspace / the panel isn't open yet

---

## 6. Console, Logs, and Visualization

| Tool | Use when |
|---|---|
| Bitstream Studio panels | The main way — seeing the Twin / telemetry immediately |
| VS Code Output / Developer Tools | Debugging the extension / the webview |
| A device UART terminal | Confirming the firmware is printing a heartbeat |
| The Hackathon `web-app/` | An external dashboard (serve per its guide) — extra visualization |

> **Key phrase**
> If the UI is empty, ask in order: *the extension? the backend? the link? source streaming? the correct panel?*

Deeper co-sim detail (timing/latency) is in [M04](../../m04-cosimulation/l01-firmware-twin-cosim/README.md) — M02 only asks for **a first, reproducible session**.

---

## Next Steps

1. Do the install-and-first-session lab: [Lab](../l02-lab/README.md)
2. Fill in the setup sheet: [vscode-twin-setup.md](resources/vscode-twin-setup.md)
3. When ready, continue to **M03 — Virtual Device Modeling**

---

## References and Further Reading

1. **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)**
2. **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** — `vsix/`, `hex/`, `flasher/`
3. [Visual Studio Code](https://code.visualstudio.com/)
4. [Course 1 M02](../../../firmware-sdk-edge-ai/m02-toolchain/l01-modustoolbox-and-vscode/README.md) — ModusToolbox build/flash
5. [M01 Twin Architecture](../../m01-twin-architecture/l01-twin-architecture/README.md) · [Course 2 TOC](../../README.md)
6. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**
7. **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)**

---

## Check your understanding

Three short questions in [quiz.yaml](quiz.yaml), one per objective of this lesson. Try answering them yourself first, then compare with the answer key and explanations in the file.

## Lab

Continue hands-on at [Lab: installing the Twin in VS Code and a first session](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/vscode-twin-setup.md) · [← Table of Contents](../../README.md) · [← M01](../../m01-twin-architecture/l01-twin-architecture/README.md) · [M03 →](../../m03-virtual-device/l01-virtual-device-modeling/README.md)
