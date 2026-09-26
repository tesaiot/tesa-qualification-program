---
id: twin.m02.l02
lang: en
title:
  th: 'แล็บ: ติดตั้ง Twin บน VS Code และเซสชันแรก'
  en: 'Lab: Install VS Code Twin and First Session'
summary:
  th: ติดตั้ง Bitstream Studio ผูก workspace เปิดเซสชันแรก (Simulator หรือ Bitstream) แล้วสังเกตและสลับเส้นทาง
  en: Install Bitstream Studio, bind the workspace, open a first session (Simulator or Bitstream), then observe and switch paths.
level: L3
time_min:
  lab: 180
hardware:
  emulator: true
  boards:
  - devkit
prerequisites:
- twin.m02.l01
objectives:
- th: ติดตั้ง Bitstream Studio และผูก workspace กับโปรเจกต์เฟิร์มแวร์หรือแพ็กแล็บ
  en: Install Bitstream Studio and bind a workspace to a firmware project or lab pack.
- th: เปิดเซสชันแรกสำเร็จอย่างน้อยหนึ่งเส้นทาง (Simulator หรือ Bitstream) พร้อมสกรีนช็อตหลักฐาน
  en: Open a first session on at least one path (Simulator or Bitstream) with screenshot evidence.
develops:
- skill: sys.simulation
  to: 2
- skill: iot.digital-twin
  to: 2
assesses:
- skill: sys.simulation
  level: 2
  evidence: README.md#deliverables-checklist
context:
  platform: psoc-edge-e84
  host: bitstream-studio
  ide: vscode
  simulator: Bitstream Simulator (not the BENTO Emulator)
status: alpha
translation: done
source_sha256: c4e3da1cb9d39a9c654cc85e6965eeb31bb5725c7e61ef1dbb96714340ae040c
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C2/M02/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M02 — Install VS Code Twin and First Session

**Course 2 · Module 2**
**Type:** Hands-on (install + bind + first live session)
**Suggested time:** 2–3 hours (including installation)

Read first: [Lesson](../l01-vscode-for-twin/README.md) · [Cheatsheet](../l01-vscode-for-twin/resources/vscode-twin-setup.md) · [← Table of Contents](../../README.md) · [← M01](../../m01-twin-architecture/l01-twin-architecture/README.md) · [M03 →](../../m03-virtual-device/l01-virtual-device-modeling/README.md)

### Useful references during the lab

| Document | Use when |
|---|---|
| [Hackathon README](https://github.com/drsanti/TESAIoT_Hackathon) | Installing the VSIX / flashing the HEX |
| [Bitstream Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) | Install Path A |
| [Course 1 M02](../../../firmware-sdk-edge-ai/m02-toolchain/l01-modustoolbox-and-vscode/README.md) | If you need to build/flash yourself |

---

## Lab Goals

- The **Bitstream Studio** extension is ready to use
- A workspace exists that can point at the firmware project or the lab pack
- A first session succeeds on at least one path: **Simulator** or **Bitstream**
- Visualization / moving values are visible, with evidence recorded
- [vscode-twin-setup.md](../l01-vscode-for-twin/resources/vscode-twin-setup.md) filled in

---

## Lab A — Install (required)

1. Install [VS Code](https://code.visualstudio.com/) (or Cursor)
2. Install Bitstream Studio:
   - **Path A:** the Marketplace, or
   - **Path B:** a VSIX from [Hackathon `vsix/`](https://github.com/drsanti/TESAIoT_Hackathon)
3. Reload → Command Palette → **Open Bitstream Studio**
4. (If using the board-free mode) install **Bitstream Simulator** per your kit's guide
5. Do the CA/credentials step **only if** your round's guide specifies it
6. (Recommended) run **Download Free Assets from GitHub** once, if you'll use 3D models from [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)

**Pass when:** Bitstream Studio opens, and you see the data-source toolbar / Link

---

## Lab B — Workspace bind (required)

1. Create or open a workspace folder per the lesson's layout
2. Place or link the `firmware/` folder (or clone Hackathon as a version reference)
3. Open Bitstream Studio from the same workspace window
4. Note the project path + the VSIX/HEX version in the setup sheet

**Pass when:** you can explain "which folder the firmware is in" and "which window the Twin host is opened from"

---

## Lab C — First live session (required)

Complete at least **one** path — starting with Simulator is recommended if the board isn't ready yet.

### C1 — Simulator path

1. Toolbar → **Simulator**
2. Start Simulator / Streaming
3. **Link / Connect**
4. Open Sensor Telemetry (or the designated panel)
5. Take a screenshot: values moving + the Link status

### C2 — Bitstream path (board)

1. Flash a HEX matched to the VSIX (`hex/` + the Flasher)
2. Toolbar → **Bitstream** · choose the COM
3. **Link / Connect** until the handshake succeeds
4. Confirm the graph/values from the board
5. Take a screenshot

**Pass when:** there is live evidence for at least one path (a screenshot or a short clip)

---

## Lab D — Observe & switch (recommended)

1. If you can do both Simulator and Bitstream — switch mode once, and confirm the old data is cleared / not mixed in
2. Briefly open the Output / logs when there is an error, and note the message
3. (Optional) open the `web-app/` page from Hackathon per its guide — point out that it is an outer Visualization layer

**Pass when (recommended):** there is a 3–5 line note on how you split the problem into layers

---

## Deliverables checklist

- [ ] Labs A–C passed
- [ ] [vscode-twin-setup.md](../l01-vscode-for-twin/resources/vscode-twin-setup.md) filled in completely
- [ ] First-session evidence (a screenshot)
- [ ] (Recommended) Lab D

---

## Troubleshooting

| Symptom | Approach |
|---|---|
| The Open Bitstream Studio command doesn't appear | The wrong VSIX was installed / you haven't Reloaded yet / a different app is open |
| The session / Link doesn't come up | Shutdown Backend Services and reopen · check port 9998 |
| The Simulator shows no value | The Simulator isn't Streaming yet · the mode is still set to Bitstream |
| Bitstream is empty | The wrong COM · the HEX doesn't match the version · the baud / USB cable |
| A port is already in use | Close the other editor that owns it · Shutdown the backends |
| The UI loads but the graph is still | The wrong workspace/panel is open · not Linked yet |

[Lesson](../l01-vscode-for-twin/README.md) · [Cheatsheet](../l01-vscode-for-twin/resources/vscode-twin-setup.md) · [Table of Contents](../../README.md) · [M03 →](../../m03-virtual-device/l01-virtual-device-modeling/README.md)
