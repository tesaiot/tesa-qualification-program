---
id: twin.m02.l02
lang: th
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
translation: pending
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C2/M02/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M02 — Install VS Code Twin and First Session

**Course 2 · Module 2**  
**Type:** Hands-on (install + bind + first live session)  
**Suggested time:** 2–3 ชั่วโมง (รวมติดตั้ง)  

Read first: [Lesson](../l01-vscode-for-twin/README.md) · [Cheatsheet](../l01-vscode-for-twin/resources/vscode-twin-setup.md) · [← Table of Contents](../../README.md) · [← M01](../../m01-twin-architecture/l01-twin-architecture/README.md) · [M03 →](../../m03-virtual-device/l01-virtual-device-modeling/README.md)

### Useful references during the lab

| เอกสาร | ใช้เมื่อ |
|---|---|
| [Hackathon README](https://github.com/drsanti/TESAIoT_Hackathon) | ติดตั้ง VSIX / flash HEX |
| [Bitstream Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) | Path A ติดตั้ง |
| [Course 1 M02](../../../firmware-sdk-edge-ai/m02-toolchain/l01-modustoolbox-and-vscode/README.md) | ถ้าต้อง build/flash เอง |

---

## Lab Goals

- Extension **Bitstream Studio** พร้อมใช้  
- มี workspace ที่ชี้โปรเจกต์เฟิร์มแวร์หรือแพ็กแล็บได้  
- เซสชันแรกสำเร็จอย่างน้อยหนึ่งเส้น: **Simulator** หรือ **Bitstream**  
- เห็น visualization / ค่าขยับ และบันทึกหลักฐาน  
- กรอก [vscode-twin-setup.md](../l01-vscode-for-twin/resources/vscode-twin-setup.md)  

---

## Lab A — Install (required)

1. ติดตั้ง [VS Code](https://code.visualstudio.com/) (หรือ Cursor)  
2. ติดตั้ง Bitstream Studio:  
   - **Path A:** Marketplace, หรือ  
   - **Path B:** VSIX จาก [Hackathon `vsix/`](https://github.com/drsanti/TESAIoT_Hackathon)  
3. Reload → Command Palette → **Open Bitstream Studio**  
4. (ถ้าจะใช้โหมดไม่มีบอร์ด) ติดตั้ง **Bitstream Simulator** ตามคู่มือของชุดที่ใช้  
5. ทำขั้นตอน CA/credentials **เฉพาะเมื่อ** คู่มือรอบนั้นระบุ  
6. (แนะนำ) รัน **Download Free Assets from GitHub** หนึ่งครั้งถ้าจะใช้โมเดล 3D จาก [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)  

**Pass when:** เปิด Bitstream Studio ได้ และเห็น toolbar แหล่งข้อมูล / Link

---

## Lab B — Workspace bind (required)

1. สร้างหรือเปิดโฟลเดอร์ workspace ตามโครงในบทเรียน  
2. วางหรือลิงก์โฟลเดอร์ `firmware/` (หรือ clone Hackathon เป็นอ้างอิงเวอร์ชัน)  
3. เปิด Bitstream Studio จากหน้าต่าง workspace เดียวกัน  
4. จด path โปรเจกต์ + เวอร์ชัน VSIX/HEX ลง setup sheet  

**Pass when:** คุณอธิบายได้ว่า “เฟิร์มแวร์อยู่โฟลเดอร์ไหน” และ “โฮสต์ Twin เปิดจากหน้าต่างไหน”

---

## Lab C — First live session (required)

ทำอย่างน้อย **หนึ่ง** เส้นทางให้จบ — แนะนำเริ่ม Simulator ถ้าบอร์ดยังไม่พร้อม

### C1 — Simulator path

1. Toolbar → **Simulator**  
2. Start Simulator / Streaming  
3. **Link / Connect**  
4. เปิด Sensor Telemetry (หรือแผงที่กำหนด)  
5. แคปหน้าจอ: ค่าขยับ + สถานะ Link  

### C2 — Bitstream path (board)

1. Flash HEX ที่จับคู่ VSIX (`hex/` + Flasher)  
2. Toolbar → **Bitstream** · เลือก COM  
3. **Link / Connect** จน handshake  
4. ยืนยันกราฟ/ค่าจากบอร์ด  
5. แคปหน้าจอ  

**Pass when:** มีหลักฐาน live อย่างน้อยหนึ่งเส้นทาง (สกรีนช็อตหรือคลิปสั้น)

---

## Lab D — Observe & switch (recommended)

1. ถ้าทำได้ทั้ง Simulator และ Bitstream — สลับโหมดหนึ่งครั้ง แล้วยืนยันว่าข้อมูลเก่าถูกล้าง/ไม่ปะปน  
2. เปิด Output / log สั้น ๆ เมื่อมี error แล้วจดข้อความ  
3. (ทางเลือก) เปิดหน้า `web-app/` จาก Hackathon ตามคู่มือ — ชี้ว่าเป็น Visualization ชั้นนอก  

**Pass when (recommended):** มีโน้ต 3–5 บรรทัดว่าแยกปัญหาเป็นชั้นอย่างไร

---

## Deliverables checklist

- [ ] Lab A–C ผ่าน  
- [ ] [vscode-twin-setup.md](../l01-vscode-for-twin/resources/vscode-twin-setup.md) กรอกครบ  
- [ ] หลักฐานเซสชันแรก (สกรีนช็อต)  
- [ ] (แนะนำ) Lab D  

---

## Troubleshooting

| อาการ | แนวทาง |
|---|---|
| ไม่เห็นคำสั่ง Open Bitstream Studio | ติดตั้งผิด VSIX / ยังไม่ Reload / เปิดคนละแอป |
| Session / Link ไม่ขึ้น | Shutdown Backend Services แล้วเปิดใหม่ · ตรวจพอร์ต 9998 |
| Simulator ไม่มีค่า | Simulator ยังไม่ Streaming · โหมดยังเป็น Bitstream |
| Bitstream ว่าง | COM ผิด · HEX ไม่จับคู่ · baud / สาย USB |
| พอร์ตถูก占用 | ปิด editor อื่นที่เป็น owner · Shutdown backends |
| UI โหลดแต่กราฟนิ่ง | เปิดผิด workspace/แผง · ยังไม่ Link |

[Lesson](../l01-vscode-for-twin/README.md) · [Cheatsheet](../l01-vscode-for-twin/resources/vscode-twin-setup.md) · [Table of Contents](../../README.md) · [M03 →](../../m03-virtual-device/l01-virtual-device-modeling/README.md)
