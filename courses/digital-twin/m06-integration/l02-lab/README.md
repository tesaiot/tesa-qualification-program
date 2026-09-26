---
id: twin.m06.l02
lang: th
title:
  th: 'แล็บ Capstone: มินิโปรเจกต์ E2E บน Digital Twin'
  en: 'Lab: E2E Mini-Project on Digital Twin'
summary:
  th: ล็อกสถาปัตยกรรม ประกอบเดโมที่รันได้ รันเทส E2E สามเคส ฝึกไล่ log และจัดแพ็กส่งต่อ
  en: Lock the architecture, assemble a running demo, run three E2E test cases, practise log triage and package the handoff.
level: L3
time_min:
  lab: 120
hardware:
  emulator: true
  boards:
  - devkit
prerequisites:
- twin.m06.l01
objectives:
- th: ประกอบเดโม stimulus → firmware → Studio → dashboard/MQTT ที่รันซ้ำได้
  en: Assemble a repeatable stimulus → firmware → Studio → dashboard/MQTT demo.
- th: รันเทส E2E อย่างน้อยสามเคส (Normal, Stimulus, Command/fault) และบันทึกผ่าน/ไม่ผ่านพร้อมเหตุผล
  en: Run at least three E2E tests (Normal, Stimulus, Command/fault) and record pass/fail with reasons.
- th: จัดแพ็ก README และหลักฐานให้ผู้อื่นรันซ้ำได้
  en: Package the README and evidence so others can rerun the demo.
develops:
- skill: iot.digital-twin
  to: 3
- skill: test.sil-hil
  to: 2
- skill: soft.communication
  to: 2
assesses:
- skill: iot.digital-twin
  level: 3
  evidence: README.md#deliverables-checklist
- skill: test.sil-hil
  level: 2
  evidence: README.md#lab-c--three-e2e-test-cases-required
context:
  platform: psoc-edge-e84
  host: bitstream-studio
  ide: vscode
  simulator: Bitstream Simulator (not the BENTO Emulator)
status: alpha
translation: done
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C2/M06/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M06 — E2E Mini-Project on Digital Twin

**Course 2 · Module 6**  
**Type:** Capstone / End-to-End  
**Suggested time:** ~2 ชั่วโมง (+ เวลาเพิ่มสำหรับ README และหลักฐาน)

Read first: [Lesson](../l01-system-integration-testing/README.md) · [Case brief](../l01-system-integration-testing/resources/e2e-case-brief.md) · [Course package](../l01-system-integration-testing/resources/course-package.md) · [← TOC](../../README.md) · [← M05](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md)

### Useful references during the lab

| เอกสาร | ใช้เมื่อ |
|---|---|
| [M03](../../m03-virtual-device/l02-lab/README.md) · [M04](../../m04-cosimulation/l02-lab/README.md) · [M05](../../m05-telemetry-cloud/l02-lab/README.md) | device · co-sim · MQTT |
| [Hackathon `web-app/`](https://github.com/drsanti/TESAIoT_Hackathon) | **ex06** · **ex15** (หรือ ex09) |
| [Developer Hub](https://dev.tesaiot.dev/) | ตัวอย่างเฟิร์มแวร์ |
| [Course 1 M08](../../../firmware-sdk-edge-ai/m08-capstone/l02-lab/README.md) | รูปแบบ Capstone ฝั่งบอร์ด |

---

## Lab Goals

ส่งมอบเดโมสั้นบน Twin ที่ครบ:

**stimulus → firmware → Studio visualization → external dashboard/MQTT**  
พร้อมตารางเทส ≥ 3 เคส และ README รันซ้ำได้

---

## Prerequisites

- [ ] M02 Link เสถียร  
- [ ] M03 มี virtual device + event script (หรือเทียบเท่า)  
- [ ] M04 co-sim ผ่านอย่างน้อย Path เดียว  
- [ ] M05 เคย Start broker + subscriber ได้  
- [ ] โฟลเดอร์ผลงาน + `lab-notes/`  

---

## Recommended brief — pick a domain story

เริ่มจาก **Smart Environmental Monitor** (IoT / สภาพแวดล้อม) หรือแมปเป็นโดเมนอื่นตาม [README §4](../l01-system-integration-testing/README.md):

| Domain | เน้นเล่า | เซ็นเซอร์หลัก | Evidence เสริม |
|---|---|---|---|
| IoT | โหนด ↔ คลาวด์ | SHT40 + state | ex06 + ex15 |
| Home | ห้องสบาย / ปลอดภัย | SHT40 + switch | ex06 + MQTT cmd |
| Industrial | alarm บนไลน์ | temp/IMU | ex06 + ex08 + ex15 |
| Health-sim | ลิงก์เฝ้าระวัง (จำลอง) | BMI270 + SHT40 | ex05 + ex08 + ex09 |

| ส่วน | เลือกตัวอย่าง (ปรับตามโดเมน) |
|---|---|
| Sensors | SHT40 temp/humidity (± sensor อื่น) |
| Behavior | เกินเกณฑ์ → state/event + สัญญาณบนโฮสต์ |
| Script | Quiet → Warm/Alert |
| MQTT | publish telemetry; optional subscribe command |
| Evidence | Studio + **ex06** + (**ex15** หรือ **ex09**) |

กรอกรายละเอียดใน [e2e-case-brief.md](../l01-system-integration-testing/resources/e2e-case-brief.md)

---

## Lab A — Lock architecture (required)

1. เลือก **โดเมน** จาก [README §4](../l01-system-integration-testing/README.md) (IoT / Home / Industrial / Health-sim)  
2. วาด/เขียนแผนภาพ 4 ขั้นจากบทเรียน §2 แล้วใส่ชื่อเหตุการณ์ตามโดเมน  
3. ระบุ Path: Simulator / Board / Both  
4. ระบุ topic MQTT และ consumer หน้าเว็บที่จะใช้เป็นหลักฐาน  
5. คัดลอกโครง README จากบทเรียน §6.2 ลงโปรเจกต์ (ใส่บรรทัด Domain)  

**Pass when:** เพื่อนในทีมอ่านแล้วรู้โดเมน + เครื่องมือที่จะเปิดก่อน โดยไม่ถามเพิ่ม

---

## Lab B — Assemble the running demo (required)

1. Bring-up Studio (backend เดียว) + co-sim  
2. รัน event script / scene ของคุณ  
3. ยืนยันค่าบน Studio  
4. Serve `web-app/` → เปิด **ex06** ให้เห็นเซ็นเซอร์ที่เกี่ยวข้อง  
5. Start broker → publish (และ/หรือ subscribe) → ยืนยันบน **ex15** หรือ **ex09**  

**Pass when:** เดโม Normal รันได้ต่อเนื่อง ≥ 1 นาทีโดยไม่หลุด Link เอง

---

## Lab C — Three E2E test cases (required)

รันและกรอกตารางใน case brief:

| เคส | อย่างน้อยต้องพิสูจน์ |
|---|---|
| **Normal** | telemetry อัปเดตบน Studio + consumer |
| **Stimulus** | threshold / switch / script เปลี่ยน state หรือ event ชัด |
| **Command / fault** | คำสั่ง MQTT **หรือ** ตัด broker/สตรีมสั้น ๆ แล้วกู้คืน |

**Pass when:** อย่างน้อย 3 แถวมีผลจริง + ผ่าน? = ใช่ (หรือ Fail พร้อมเหตุผลและworkaround ที่ยอมรับได้)

---

## Lab D — Log triage drill (recommended)

จงใจทำให้พังหนึ่งอย่าง (ปิด broker / หยุด script / เปิดผิด panel) แล้ว:

1. ไล่ชั้น §3 ในบทเรียน  
2. จดชั้นที่พบปัญหา  
3. แก้กลับมาเดโมเขียว  

**Pass when:** มีบรรทัดใน case brief ส่วนปัญหา/การแก้

---

## Lab E — Package for handoff (required)

- [ ] README รันซ้ำได้  
- [ ] case brief กรอกครบ  
- [ ] หลักฐานสกรีนช็อต/คลิป (Studio + ex06 และ MQTT consumer)  
- [ ] ไม่มี password ในไฟล์ส่ง  
- [ ] รายการตรวจจาก [course-package.md](../l01-system-integration-testing/resources/course-package.md)  

---

## Deliverables checklist

- [ ] Lab A–C, E ผ่าน  
- [ ] (แนะนำ) Lab D  
- [ ] ลิงก์/โฟลเดอร์โปรเจกต์ที่พร้อมส่งต่อ  

---

## Troubleshooting

| อาการ | แนวทาง |
|---|---|
| เดโมยาวแล้วหลุด | กลับ M02/M04 bring-up · อย่าผสม backend |
| ex06 ว่างแต่ Studio มีค่า | Serve โฟลเดอร์ · connection badge · mask/fields |
| MQTT ว่าง | Start broker · topic ตรง · คนละท่อกับ Live Data |
| Stimulus ไม่เห็นบน consumer | ตรวจ script รันจริง · stale · อัตรา publish |
| ผลงานมี secret | ลบแล้วใส่ placeholder ใน README |

[Lesson](../l01-system-integration-testing/README.md) · [Case brief](../l01-system-integration-testing/resources/e2e-case-brief.md) · [Course package](../l01-system-integration-testing/resources/course-package.md) · [TOC](../../README.md)
