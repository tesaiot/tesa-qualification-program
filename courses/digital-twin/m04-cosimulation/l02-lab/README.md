---
id: twin.m04.l02
lang: th
title:
  th: 'แล็บ: I/O ครบวงจรแบบ co-simulation'
  en: 'Lab: Co-simulation End-to-End I/O'
summary:
  th: bring-up co-sim พิสูจน์เส้นทาง input และ output จด latency และ (แนะนำ) ใช้ web-app ex05 เป็นกระจกชั้นที่สอง
  en: Bring up co-simulation, prove the input and output paths, note latency and (recommended) use web-app ex05 as a second mirror.
level: L3
time_min:
  lab: 180
hardware:
  emulator: true
  boards:
  - devkit
prerequisites:
- twin.m04.l01
objectives:
- th: รันเฟิร์มแวร์คู่ Twin/โฮสต์ให้มี heartbeat ทั้งสองฝั่ง
  en: Run firmware alongside the Twin/host with a heartbeat on both sides.
- th: เก็บหลักฐานทั้งเส้นทาง input และ output และจด latency อย่างน้อยหนึ่งจุด
  en: Capture evidence for both the input and output paths and record latency at one point or more.
develops:
- skill: test.sil-hil
  to: 2
- skill: soft.problem-solving
  to: 2
assesses:
- skill: test.sil-hil
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
  path: C2/M04/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M04 — Co-simulation End-to-End I/O

**Course 2 · Module 4**  
**Type:** Hands-on (bring-up + input path + output path + latency)  
**Suggested time:** ~2.5–3 ชั่วโมง  

Read first: [Lesson](../l01-firmware-twin-cosim/README.md) · [Checklist](../l01-firmware-twin-cosim/resources/cosim-checklist.md) · [← Table of Contents](../../README.md) · [← M03](../../m03-virtual-device/l01-virtual-device-modeling/README.md) · [M05 →](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md)

### Useful references during the lab

| เอกสาร | ใช้เมื่อ |
|---|---|
| [M02 lab](../../m02-vscode-twin/l02-lab/README.md) | Studio / Simulator / COM |
| [M03 lab](../../m03-virtual-device/l02-lab/README.md) | event script / Virtual Device |
| [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) | HEX · `web-app/` evidence |
| [Course 1 M04](../../../firmware-sdk-edge-ai/m04-rtos/l01-freertos-programming/README.md) | task timing |

---

## Lab Goals

- รันเฟิร์มแวร์คู่ Twin/โฮสต์ได้เสถียร  
- พิสูจน์ **input**: กระตุ้น → เฟิร์มแวร์รับรู้  
- พิสูจน์ **output**: เฟิร์มแวร์สั่ง → โฮสต์/ Twin สะท้อน  
- จด latency คร่าว ๆ อย่างน้อย 1 จุด  
- กรอก [cosim-checklist.md](../l01-firmware-twin-cosim/resources/cosim-checklist.md)  

---

## Prerequisites

- [ ] M02 เซสชันแรกผ่าน  
- [ ] M03 มี device model + event script (หรือ timeline)  
- [ ] เลือก path: **Simulator** และ/หรือ **Board + HEX**  
- [ ] โฟลเดอร์ `lab-notes/` สำหรับหลักฐาน  

---

## Lab A — Bring-up co-sim (required)

1. เปิด Bitstream Studio  
2. เลือก **Simulator** *หรือ* **Bitstream** (อย่างใดอย่างหนึ่ง)  
3. Link จนมีสตรีม/heartbeat  
4. รอ ≥ 30 วินาทีโดยไม่หลุด  
5. แคปหน้าจอสถานะ Link + กราฟ/ค่า  

**Pass when:** ทั้งโฮสต์และแหล่งเฟิร์มแวร์ (sim หรือบอร์ด) มีสัญญาณชีวิตชัด

---

## Lab B — Input path (required)

1. ใช้สคริปต์/ไทม์ไลน์จาก M03 หรือกระตุ้นด้วย scene/UI/ปุ่ม  
2. ให้เฟิร์มแวร์แสดงว่าอ่านค่าได้ (UART log, การเปลี่ยนโหมด, หรือค่าที่ echo บนโฮสต์อย่างชัดว่ามาจาก logic อ่าน)  
3. บันทึก: สิ่งที่กระตุ้น → สิ่งที่เฟิร์มแวร์รายงาน  

**Pass when:** คนในทีมอธิบายลูกศร Twin/stimulus → firmware ได้พร้อมหลักฐาน

---

## Lab C — Output path (required)

1. ให้เฟิร์มแวร์เปลี่ยนเอาต์พุตอย่างน้อยหนึ่งอย่าง (LED, flag, publish, log marker)  
2. ยืนยันว่า Bitstream Studio (หรือ `web-app/`) สะท้อนผล  
3. เทียบกับ behavior WHEN/THEN จาก M03  

**Pass when:** มีหลักฐานคู่ (firmware side + host side)

---

## Lab D — Latency note (recommended)

1. เลือกจุดวัดหนึ่งจุด (เช่น stimulus → first log line)  
2. ทำ 3 รอบ จดค่าโดยประมาณ  
3. เดาสาเหตุหน่วง 1 ข้อ (task period / scene rate / UI)  
4. กรอกใน checklist  

**Pass when:** มีตัวเลขช่วงและสมมติฐานแหล่งหน่วง — ไม่ต้องสวยที่สุด

---

## Lab E — Optional extras

- เปรียบเทียบ Path A (Simulator) กับ Path B (Board) บนสคริปต์เดียวกัน  
- ถ้ามี GLB จาก M03 — โหลดประกอบฉากแล้วจดว่าภาพช่วยสาธิตอะไร (ไม่แทน sensor truth)

### Lab E1 — Hackathon web-app `ex05` (recommended)

อ่าน walkthrough ใน [README §4](../l01-firmware-twin-cosim/README.md) ก่อน

1. Serve โฟลเดอร์ Hackathon **`web-app/`** แล้วเปิด **`ex05_bmi270_orientation.html`**  
2. ยืนยัน badge เป็น `connected` และมี `route:`  
3. ใน sensor settings เปิด BMI270 **Euler** และ/หรือ **Quaternion** ใน publish mask  
4. เอียงบอร์ด หรือสลับ scene Motion — horizon + ° ต้องขยับ  
5. แคปหน้าจอ **คู่กับ** แผง BMI270 ใน Studio; จด `source:` และ `mask 0x…`  

**Pass when:** อธิบายได้ว่า ex05 พิสูจน์ output path ชั้นนอก และถ้าค้างที่ *waiting for orientation* แปลว่า mask ไม่ครบ (ไม่ใช่แค่ “หน้าเว็บเสีย”)

---

## Deliverables checklist

- [ ] Lab A–C ผ่าน  
- [ ] [cosim-checklist.md](../l01-firmware-twin-cosim/resources/cosim-checklist.md) กรอกครบ  
- [ ] หลักฐาน input + output (สกรีนช็อต/คลิป/log)  
- [ ] (แนะนำ) Lab D latency  
- [ ] (แนะนำ) Lab E / E1 (`ex05`)  

---

## Troubleshooting

| อาการ | แนวทาง |
|---|---|
| Link ไม่ขึ้น | Shutdown backends · ตรวจพอร์ต · M02 |
| มีกราฟแต่กระตุ้นแล้วเงียบ | ตรวจ scene/cfg · สคริปต์ M03 · log เฟิร์มแวร์ |
| Log ถูกแต่ UI ไม่ขยับ | เปิดผิดแผง · consumer ไม่ได้ connect |
| ค่า latency สุ่มมาก | ใช้ timestamp ใน log · อย่าจับเวลาด้วยตาอย่างเดียว |
| สลับ Simulator/Bitstream แล้วงง | เคลียร์ข้อมูล · Link ใหม่ทีละโหมด |
| ex05 ค้าง *waiting for orientation* | เปิด Euler/Quaternion ใน BMI270 mask — ไม่ใช่แค่ accel/gyro |
| ex05 disconnected | Serve ถูกโฟลเดอร์ `web-app/` · Studio/bridge เปิดอยู่ |

[Lesson](../l01-firmware-twin-cosim/README.md) · [Checklist](../l01-firmware-twin-cosim/resources/cosim-checklist.md) · [Table of Contents](../../README.md) · [M05 →](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md)
