---
id: twin.m02.l01
lang: th
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
translation: pending
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C2/M02/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M02 — VS Code for Twin Development

**Course 2 · Module 2**  
**Suggested time:** ประมาณ 3 ชั่วโมง (ติดตั้ง + ผูก workspace + เซสชันแรก)  
**Format:** บทเรียนเชิงปฏิบัติ — ตั้งโฮสต์ Twin ใน VS Code แล้วเห็น telemetry แบบเรียลไทม์

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/vscode-twin-setup.md) · [← Table of Contents](../../README.md) · [← M01](../../m01-twin-architecture/l01-twin-architecture/README.md) · [M03 →](../../m03-virtual-device/l01-virtual-device-modeling/README.md)

---

## เป้าหมาย (Learning Outcomes)

เมื่อเรียนจบ คุณควรทำได้ดังนี้:

1. ติดตั้งและตั้งค่า **VS Code extension** สำหรับ TESAIoT / Digital Twin — **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)**  
2. จัด **workspace** และผูกโปรเจกต์เฟิร์มแวร์ (หรือ HEX แล็บ) เข้ากับ Twin host  
3. **Run / Link** เซสชันแรก: โหมด **Simulator** และ/หรือ **Bitstream (UART)** พร้อมดูผลแบบเรียลไทม์  
4. ใช้ **Console / Logs / Visualization** (Sensor Telemetry, Sensor Studio, สถานะ backend) เพื่อตรวจข้อมูล  

โมดูลนี้พาคุณจากแผนที่สถาปัตยกรรมใน [M01](../../m01-twin-architecture/l01-twin-architecture/README.md) ไปสู่ **เครื่องมือพร้อมใช้** — บทถัดไป ([M03](../../m03-virtual-device/l01-virtual-device-modeling/README.md)) จะสร้าง Virtual Device และสคริปต์เหตุการณ์เอง

> **โฮสต์หลักของ Course 2**  
> ในเอกสารหลักสูตรอาจเรียก *TESA Digital Twin / VS Code Extension* — ในแล็บ ติดตั้งและเปิด **Bitstream Studio** (Marketplace หรือ VSIX จาก Hackathon) เป็นจุดเข้าเดียวกัน

### Read alongside this chapter

| เอกสาร | ใช้เมื่อ |
|---|---|
| **[Bitstream Studio (Marketplace)](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | ติดตั้ง extension จาก Marketplace |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | แพ็กแล็บ: `vsix/`, `hex/`, `flasher/`, `web-app/` |
| **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** | GLB / texture / cubemap / รูป — Free Loader หรือ browse [`assets/`](https://github.com/drsanti/ternion-3d-assets-free/tree/main/assets) |
| [Visual Studio Code](https://code.visualstudio.com/) | ตัวแก้ไข / host ของ extension |
| [Course 1 M02 — ModusToolbox + VS Code](../../../firmware-sdk-edge-ai/m02-toolchain/l01-modustoolbox-and-vscode/README.md) | Build / flash เฟิร์มแวร์ (คู่กับโฮสต์ Twin) |
| [M01 — Twin Architecture](../../m01-twin-architecture/l01-twin-architecture/README.md) | ชั้น Communication / Visualization |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | ตัวอย่างเฟิร์มแวร์ที่จะ bind ใน workspace |

---

## 1. Why VS Code Is the Hub

ใน Course 2 **Visual Studio Code** ไม่ใช่แค่ตัวพิมพ์โค้ด — เป็นศูนย์กลางที่เชื่อม:

| ชิ้น | บทบาท |
|---|---|
| โปรเจกต์เฟิร์มแวร์ | จาก Course 1 / ModusToolbox / โฟลเดอร์แล็บ |
| **Bitstream Studio** | Twin host — telemetry, Sensor Studio, MQTT, 3D |
| **Bitstream Simulator** (เสริม) | Virtual MCU เมื่อไม่มีบอร์ด |
| Backend services | Serial bridge, MQTT broker บน localhost |
| Visualization | กราฟ / แผง / dashboard |

เป้าหมายของบทนี้: **ติดตั้ง → ผูกโปรเจกต์ → Link เซสชันแรก → เห็นค่าขยับ** ในสภาพแวดล้อมเดียว

```text
[VS Code]
   ├─ Firmware folder (edit / debug)
   ├─ Bitstream Studio webview  ← Twin UI
   ├─ Bridge :9998              ← Communication
   └─ (optional) Simulator VSIX ← Virtual device stream
```

> **Key phrase**  
> Course 1 M02 สอน *สร้างและ flash เฟิร์มแวร์* — Course 2 M02 สอน *เปิดโฮสต์ Twin ให้คุยกับเฟิร์มแวร์หรือ Simulator*

---

## 2. Install the Twin Extension

### 2.1 What to install

| ชิ้น | จำเป็นเมื่อ |
|---|---|
| [VS Code](https://code.visualstudio.com/) หรือ Cursor | เสมอ |
| **Bitstream Studio** (`TERNIONDEV.bitstream-studio`) | เสมอ — Twin host |
| **Bitstream Simulator** (companion VSIX) | เมื่อจะใช้โหมด **Simulator** ไม่มีบอร์ด |
| [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) pack | แนะนำ — VSIX/HEX/Flasher เวอร์ชันจับคู่ |

### 2.2 Path A — Visual Studio Marketplace

1. เปิด Extensions ใน VS Code  
2. ค้นหา **Bitstream Studio** หรือเปิด [หน้า Marketplace](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)  
3. **Install** → Reload เมื่อระบบขอ  
4. Command Palette → **Open Bitstream Studio**

### 2.3 Path B — Hackathon VSIX (lab pack)

เหมาะเมื่อต้องการล็อกเวอร์ชันให้ตรงกับ HEX:

1. Clone หรือดาวน์โหลด [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)  
2. เปิดโฟลเดอร์ `vsix/` เลือก `bitstream-studio-<version>.vsix` ตามเวอร์ชันที่ต้องการ  
3. Extensions → **…** → **Install from VSIX…**  
4. Reload → **Open Bitstream Studio**

ตัวอย่างจากเทอร์มินัล (เปลี่ยนชื่อไฟล์ตามเวอร์ชันที่ใช้):

```bash
code --install-extension vsix/bitstream-studio-0.1.8.vsix
code -r
```

(ใช้ `cursor` แทน `code` ถ้าใช้ Cursor)

> **Version matching**  
> VSIX กับ HEX ควรเป็นชุดเดียวกัน — ดู `latest` ใน firmware manifest ของ Hackathon เมื่อไม่แน่ใจ

### 2.4 Credentials / CA (when required)

บางชุดแล็บอาจมีขั้นตอนเชื่อถือใบรับรองหรือใส่ credentials สำหรับบริการเครือข่ายภายใน

- ถ้าคู่มือรอบนั้น**มี** — ทำก่อน Lab C และจดลง [setup sheet](resources/vscode-twin-setup.md)  
- ถ้าใช้เฉพาะ localhost bridge / Marketplace ทั่วไป — มัก**ไม่ต้อง** CA พิเศษ  

อย่า commit รหัสผ่านหรือ token ลงไฟล์ผลงาน

### 2.5 Verify the extension is alive

หลังติดตั้ง ตรวจอย่างน้อยหนึ่งอย่าง:

| ตรวจ | ผ่านเมื่อ |
|---|---|
| Command Palette มี **Open Bitstream Studio** | เห็นคำสั่ง |
| Status bar มีสถานะ Bitstream / backend | ไม่ error ค้าง |
| เปิด Studio แล้วมี toolbar (Bitstream / Simulator, Link) | UI โหลด |

จดเวอร์ชัน extension ลง cheatsheet

### 2.6 Free 3D assets (models / textures / images)

เมื่อ Twin หรือ Sensor Studio ต้องการโมเดล GLB, cubemap, หรือรูปภาพ ให้ใช้แหล่งทางการ:

**[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** — เนื้อหาอยู่ภายใต้ [`assets/`](https://github.com/drsanti/ternion-3d-assets-free/tree/main/assets) บน branch `main`

| วิธี | เมื่อใช้ |
|---|---|
| Command Palette → **Download Free Assets from GitHub** | ซิงก์เข้าเครื่องครั้งแรก / อัปเดตแพ็ก |
| Browse บน GitHub | หา `models/`, `textures/`, รูปภาพ |
| Online fallback ใน Studio | base `…/main/assets` (relative path เช่น `models/…/*.glb`) |

ไม่ต้องคัดลอก asset จาก workspace ส่วนตัวของผู้อื่นมาใส่รายงาน

---

## 3. Workspace Structure and Binding Firmware

### 3.1 Recommended layout

ไม่บังคับชื่อโฟลเดอร์เป๊ะ — สำคัญคือ**แยกชัด**และเปิดซ้ำได้:

```text
my-course2-workspace/
  firmware/          # โปรเจกต์ C จาก MTB / TESA (หรือลิงก์ไปโปรเจกต์ Course 1)
  lab-notes/         # โน้ต / สกรีนช็อต / setup sheet
  .vscode/           # tasks / settings ของทีม (ถ้ามี)
```

ทางเลือกที่เน้นโฮสต์ก่อน:

```text
my-course2-workspace/
  hackathon/         # clone TESAIoT_Hackathon (vsix + hex อ้างอิง)
  firmware/          # โปรเจกต์ที่แก้ไขจริง
  lab-notes/
```

### 3.2 What “binding” means in this course

ใน Bitstream Studio การผูกโปรเจกต์เข้ากับ Twin ไม่ได้แปลว่าต้องมีไฟล์ config ลับเฉพาะทุกครั้งเสมอ — ความหมายปฏิบัติคือ:

| ขั้น | ทำอะไร |
|---|---|
| 1 | เปิดโฟลเดอร์ workspace ที่มีเฟิร์มแวร์ (หรืออย่างน้อยรู้ path ที่จะ build/flash) |
| 2 | เปิด **Bitstream Studio** ในหน้าต่างเดียวกัน |
| 3 | เลือกแหล่งข้อมูล: **Simulator** หรือ **Bitstream** + COM ที่ถูกต้อง |
| 4 | (ถ้ามีบอร์ด) flash HEX ที่จับคู่ VSIX แล้วเปิดพอร์ต |
| 5 | กด **Link / Connect** จนเห็นสตรีม |

ถ้าใช้ ModusToolbox + VS Code สำหรับ debug บนคิต — เก็บ launch/tasks ตาม [Course 1 M02](../../../firmware-sdk-edge-ai/m02-toolchain/l01-modustoolbox-and-vscode/README.md) ไว้ใน `.vscode/` ของโปรเจกต์เฟิร์มแวร์ แล้วใช้ Studio คู่กันเป็นจอ Twin

### 3.3 Device / profile selection

| สถานการณ์ | เลือก |
|---|---|
| ไม่มีบอร์ดวันนี้ | **Simulator** + สตาร์ท Bitstream Simulator |
| มี DevKit + HEX ตรงเวอร์ชัน | **Bitstream** + เปิด COM (baud ตามเฟิร์มแวร์ — มัก 921600) |
| สลับโหมดกลางคัน | เปลี่ยน toolbar ทีละโหมด — **อย่าผสม** uart+sim ในหัว |

จำจาก M01: มีได้ทีละ backend เดียว

---

## 4. Backend Services (What Starts Automatically)

เมื่อเปิด Bitstream Studio (VSIX) ระบบมัก **auto-start** backend บนเครื่องคุณ เช่น:

| บริการ | พอร์ตที่พบบ่อย | บทบาท |
|---|---|---|
| Serial / WS bridge | **9998** | คุยระหว่าง webview ↔ UART / Simulator |
| MQTT broker (local) | **1883** / **8883** | ใช้ในแล็บ cloud ภายหลัง (M05) |

คำสั่งที่มีประโยชน์ (Command Palette — ชื่ออาจขึ้นต้นด้วย **Bitstream Studio:**):

| คำสั่งโดยประมาณ | เมื่อใช้ |
|---|---|
| Open Bitstream Studio | เปิด UI หลัก |
| Start / Stop Bitstream Simulator | โหมดไม่มีบอร์ด |
| Start All / Shutdown Backend Services | แก้พอร์ตชน หรือสลับไป terminal dev |
| **Download Free Assets from GitHub** | ซิงก์โมเดล/texture จาก [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free) |
| Open Connection Panel / Setup Checklist | กู้เซสชันแรก |

> **Multi-editor tip**  
> เปิด VS Code กับ Cursor พร้อมกันได้ แต่ bridge มี owner เดียว — ถ้าพอร์ตติด ให้ Shutdown จากหน้าต่างที่เป็นเจ้าของ แล้วค่อยเปิดใหม่

---

## 5. First Run / Debug Loop with Live Results

### 5.1 Path — Simulator (recommended first)

ลำดับที่ลดความเสี่ยงฮาร์ดแวร์:

1. ติดตั้ง Bitstream Studio (+ Simulator ถ้าต้องการโหมดไม่มีบอร์ด)  
2. **Open Bitstream Studio**  
3. Toolbar → แหล่งข้อมูล **Simulator**  
4. สตาร์ท Simulator / Streaming (หรือให้ Studio ช่วย Start เมื่อ Link)  
5. กด **Link / Connect**  
6. เปิด **Sensor Telemetry** (หรือแผงกราฟที่ต้องการ)  

**ผ่านเมื่อ:** เห็นค่าเซ็นเซอร์จำลองขยับภายในไม่กี่วินาที และสถานะลิงก์ปกติ

### 5.2 Path — Bitstream (real board)

1. Flash HEX จาก Hackathon (`hex/`) ด้วย Flasher หรือ ModusToolbox — เวอร์ชันจับคู่ VSIX  
2. เสียบ USB / เลือก COM  
3. Toolbar → **Bitstream**  
4. **Link / Connect** จน handshake สำเร็จ  
5. ดู Telemetry / Sensor Studio  

**ผ่านเมื่อ:** มีสตรีมจากบอร์ด (origin ฝั่ง uart) และ UI ไม่ว่าง

### 5.3 Firmware edit + observe (when building yourself)

วงจรที่ควรฝึกอย่างน้อยหนึ่งรอบ:

```text
Edit firmware (VS Code / MTB)
  → Build + Flash (Course 1 skills)
  → Link in Bitstream Studio
  → Watch telemetry / logs
  → Change one variable or rate
  → Re-flash / reconnect → confirm UI changes
```

ถ้าวันนี้ใช้แต่ HEX สำเร็จรูป — ยังถือว่า Lab ผ่านได้เมื่อ **host session** สำเร็จ; การแก้โค้ดจะเน้นใน M04

### 5.4 What to watch on day one

| ช่อง | ดูอะไร |
|---|---|
| **Toolbar** | Bitstream vs Simulator, Link state, MQTT chip (ถ้าเปิด) |
| **Sensor Telemetry** | กราฟ/ค่าล่าสุดขยับ |
| **Sensor Studio** | โหนด/พรีวิว (ถ้าเปิดใช้) |
| **Output / extension logs** | error ตอน start backend |
| **UART console** (ถ้ามี) | heartbeat จากเฟิร์มแวร์ |

แยกปัญหาเป็นชั้น (จากง่าย → ยาก):

1. Extension ยังไม่พร้อม / ไม่มีคำสั่ง  
2. Backend พอร์ตชน  
3. ยังไม่ Link หรือเลือกโหมดผิด  
4. เฟิร์มแวร์/ Simulator ยังไม่สตรีม  
5. Visualization คนละ workspace / ยังไม่เปิดแผง  

---

## 6. Console, Logs, and Visualization

| เครื่องมือ | ใช้เมื่อ |
|---|---|
| Bitstream Studio panels | หลัก — เห็น Twin / telemetry ทันที |
| VS Code Output / Developer Tools | ดีบัก extension / webview |
| Device UART terminal | ยืนยันว่าเฟิร์มแวร์พิมพ์ heartbeat |
| Hackathon `web-app/` | Dashboard ภายนอก (serve ตามคู่มือ) — เสริม visualization |

> **Key phrase**  
> ถ้า UI ว่าง ให้ถามตามลำดับ: *extension? backend? link? source streaming? correct panel?*

รายละเอียด co-sim ลึก (timing/latency) อยู่ใน [M04](../../m04-cosimulation/l01-firmware-twin-cosim/README.md) — M02 ขอแค่ **เซสชันแรกที่ทำซ้ำได้**

---

## Next Steps

1. ทำแล็บติดตั้งและเซสชันแรก: [แล็บ](../l02-lab/README.md)  
2. กรอกแผ่นตั้งค่า: [vscode-twin-setup.md](resources/vscode-twin-setup.md)  
3. เมื่อพร้อม ไปต่อ **M03 — Virtual Device Modeling**

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

## เช็กความเข้าใจ

คำถามสั้นสามข้อใน [quiz.yaml](quiz.yaml) ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อน แล้วค่อยเทียบกับเฉลยและคำอธิบายในไฟล์

## แล็บ

ลงมือต่อที่ [แล็บ: ติดตั้ง Twin บน VS Code และเซสชันแรก](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Cheatsheet](resources/vscode-twin-setup.md) · [← Table of Contents](../../README.md) · [← M01](../../m01-twin-architecture/l01-twin-architecture/README.md) · [M03 →](../../m03-virtual-device/l01-virtual-device-modeling/README.md)
