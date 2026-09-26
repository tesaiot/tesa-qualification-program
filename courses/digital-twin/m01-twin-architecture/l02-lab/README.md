---
id: twin.m01.l02
lang: th
title:
  th: 'แล็บ: แผนที่สถาปัตยกรรม Twin'
  en: 'Lab: Twin Architecture Map'
summary:
  th: นิยามคำด้วยภาษาตัวเอง วาด data flow และกรอกตารางตัดสินใจว่าเทสไหนใช้ Twin ได้ เทสไหนต้องบอร์ด
  en: Define the terms in your own words, draw the data flow and fill in the table of which tests the Twin can cover and which need a board.
level: L3
time_min:
  lab: 45
hardware:
  emulator: false
  boards:
  - none
prerequisites:
- twin.m01.l01
objectives:
- th: วาดแผนภาพ data flow ของระบบตัวอย่างหนึ่งชุด ตั้งแต่เซ็นเซอร์ถึง dashboard
  en: Draw the data flow of one example system from sensor to dashboard.
- th: กรอกตารางตัดสินใจอย่างน้อย 4 แถว โดยมีทั้งแถวที่ “Twin พอ” และ “ต้องบอร์ด”
  en: Fill at least four rows of the decision table, including both a “Twin is enough” row and a “needs the board” row.
develops:
- skill: iot.digital-twin
  to: 2
- skill: test.sil-hil
  to: 1
assesses:
- skill: iot.digital-twin
  level: 2
  evidence: README.md#deliverables-checklist
context:
  platform: psoc-edge-e84
  host: bitstream-studio
  ide: vscode
  simulator: Bitstream Simulator (not the BENTO Emulator)
status: alpha
translation: done
slides: slides.md
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C2/M01/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M01 — Twin Architecture Map

**Course 2 · Module 1**  
**Type:** Conceptual + diagram (+ optional host peek)  
**Suggested time:** 30–45 นาที  

Read first: [Lesson](../l01-twin-architecture/README.md) · [Cheatsheet](../l01-twin-architecture/resources/twin-architecture-map.md) · [← Table of Contents](../../README.md) · [M02 →](../../m02-vscode-twin/l01-vscode-for-twin/README.md)

### Useful references during the lab

| เอกสาร | ใช้เมื่อ |
|---|---|
| [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) | ชี้ Visualization / Communication บนโฮสต์จริง |
| [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) | `web-app/` = dashboard นอกจอ Studio |
| [Course 1 M06](../../../firmware-sdk-edge-ai/m06-mqtt/l01-mqtt-and-mqtts/README.md) | ทบทวน MQTT ใน pipeline |

---

## Lab Goals

- แยก **Virtual Device / Twin Platform / Firmware Logic / Host** ได้ด้วยคำพูดตัวเอง  
- วาด **data flow** ของระบบตัวอย่างหนึ่งชุด  
- กรอกตารางตัดสินใจ: Twin พอไหม / ต้องบอร์ดจริงไหม  
- (แนะนำ) เปิดโฮสต์หรือ dashboard สั้น ๆ เพื่อเชื่อมแนวคิดกับของจริง  

---

## Part A — Definitions (your words)

เขียน 2–3 ประโยคต่อข้อ:

1. **Virtual Device** คืออะไร  
2. **Digital Twin** ในหลักสูตรนี้ครอบคลุมอะไรบ้าง *นอกจาก* ตัวอุปกรณ์  
3. ทำไมต้องแยก **Firmware Logic** จากรายละเอียดฮาร์ดแวร์  

**Pass when:** อ่านแล้วคนอื่นในทีมเข้าใจโดยไม่ต้องเปิดบทเรียน

---

## Part B — Architecture diagram

วาด (กระดาษ / Mermaid / กล่องข้อความ) แสดงอย่างน้อย:

- VS Code / Bitstream Studio  
- Firmware Logic  
- Communication path (UART และ/หรือ MQTT)  
- Twin Engine / Virtual Device (หรือ Simulator)  
- Visualization หรือ Dashboard  
- (ถ้ามี) Cloud / broker  

ตัวอย่างโครงเปล่า:

```text
[VS Code + Bitstream Studio]
        │
[Firmware Logic] ──comm──► [Twin / Simulator state]
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
              [Telemetry UI]          [web-app / MQTT]
```

**Pass when:** มีลูกศรทิศทางข้อมูลชัด และชี้ได้ว่า Virtual Device อยู่กล่องไหน

---

## Part C — Test decision table

กรอกอย่างน้อย 4 แถว (แนะนำครบทุกแถว):

| สถานการณ์ทดสอบ | Twin / Sim พอไหม | ต้องบอร์ดจริงไหม | เหตุผลสั้น ๆ |
|---|---|---|---|
| Logic สลับโหมดจากปุ่ม | | | |
| อ่าน IMU แล้วคำนวณบนโค้ด | | | |
| ตรวจรูปแบบ MQTT JSON / topic | | | |
| Wi‑Fi หรือ BLE ระยะในห้องจริง | | | |
| ตรวจ pin map / ขาผิด | | | |
| วัดพลังงาน / battery life | | | |

**Pass when:** มีอย่างน้อยหนึ่งแถวที่ตอบ “Twin พอ” และหนึ่งแถวที่ตอบ “ต้องบอร์ด”

---

## Part D — Optional host peek (recommended)

เลือกอย่างน้อยหนึ่งอย่าง:

1. เปิด **Bitstream Studio** แล้วชี้ให้เพื่อนเห็นว่าแผงไหนคือ Visualization / ตรงไหนเปลี่ยน Bitstream vs Simulator  
2. เปิดหน้า dashboard ใน [Hackathon `web-app/`](https://github.com/drsanti/TESAIoT_Hackathon) (ตามคู่มือของชุดที่ใช้) แล้วอธิบายว่ามันอยู่ชั้นไหนในแผนภาพ Part B  

**Pass when (optional):** มีโน้ต 3–5 บรรทัดว่า “สิ่งที่เห็นบนจอ = ชั้นไหนในสถาปัตยกรรม”

---

## Deliverables checklist

- [ ] ส่วน A ครบ 3 ข้อ  
- [ ] แผนภาพส่วน B  
- [ ] ตารางส่วน C ≥ 4 แถว  
- [ ] (แนะนำ) โน้ตส่วน D  

---

## Troubleshooting

| อาการ | แนวทาง |
|---|---|
| สับสน Virtual Device กับ Twin | Device = โมเดลเครื่องหนึ่ง; Twin = ระบบแวดล้อมทั้งก้อน |
| ไม่รู้จะวาด Simulator ไว้ไหน | วางคู่กับ Twin Engine / Virtual Device เป็น *แหล่งข้อมูลจำลอง* |
| คิดว่า Twin แทนบอร์ดได้ทุกอย่าง | ดูแถว RF / pin / พลังงานในตาราง C |

[Lesson](../l01-twin-architecture/README.md) · [Cheatsheet](../l01-twin-architecture/resources/twin-architecture-map.md) · [Table of Contents](../../README.md) · [M02 →](../../m02-vscode-twin/l01-vscode-for-twin/README.md)
