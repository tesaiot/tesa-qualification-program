---
id: pdesign.m05.l02
lang: en
title:
  th: 'แล็บ: สถานการณ์ใช้งานและ checklist ก่อนทำต้นแบบ'
  en: 'Lab: Scenarios and Pre-Prototype Checklist'
summary:
  th: เขียนสถานการณ์ก่อนคลิก รันและจดปัญหา ผูกข้อมูลหรือบันทึกช่องว่าง แล้วกรอก checklist ก่อนทำต้นแบบ
  en: Write scenarios before clicking, run them and log issues, bind data or document the gap, then complete the pre-prototype checklist.
level: L2
time_min:
  lab: 180
hardware:
  emulator: false
  boards:
  - none
prerequisites:
- pdesign.m05.l01
objectives:
- th: รัน usage scenario ≥ 2 รายการบน Twin และจดปัญหาหรือจุดเฝ้าระวัง ≥ 3 ข้อ
  en: Run at least two usage scenarios on the Twin and log at least three issues or watch-outs.
- th: กรอก pre-prototype checklist พร้อม Top 3 fixes
  en: Complete the pre-prototype checklist with the top three fixes.
develops:
- skill: hwdev.enclosure
  to: 2
- skill: biz.product-decision
  to: 1
assesses:
- skill: hwdev.enclosure
  level: 2
  evidence: README.md#deliverables-checklist
context:
  tool: blender-4.5
  twin-host: bitstream-studio
  output: glb, stl
status: alpha
translation: done
source_sha256: e57c7d38d421a0a80c4c22fca141c6b33c0f6b9f82446abe41f48f8cd392096b
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C3/M05/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M05 — Scenarios and Pre-Prototype Checklist

**Course 3 · Module 5**
**Type:** Hands-on (scenarios · issues · optional fix · checklist)
**Suggested time:** ~2.5–3 hours

Read first: [Lesson](../l01-scenario-digital-validation/README.md) · [Pre-prototype checklist](../l01-scenario-digital-validation/resources/pre-prototype-checklist.md) · [← TOC](../../README.md) · [← M04](../../m04-blender-to-twin/l01-blender-to-twin/README.md) · [M06 →](../../m06-prototyping/l01-prototyping-final-project/README.md)

### Keep these tabs open

| Document | Why |
|---|---|
| [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) | run scenarios |
| [Hackathon web-app](https://github.com/drsanti/TESAIoT_Hackathon) | optional ex06 / ex05 |
| [Enclosure design guide](https://www.3ddfm.com/design-guides/electronic-enclosure-design-guide/) | what to inspect |
| [M04 export checklist](../../m04-blender-to-twin/l01-blender-to-twin/resources/export-twin-checklist.md) | sensor point names |

---

## Lab Goals

- Run at least **2** usage scenarios on the Twin
- Log at least **3** issues or watch-outs
- (Recommended) bind at least 1 firmware/telemetry state, or explain why it isn't bound yet
- Fill in [pre-prototype-checklist.md](../l01-scenario-digital-validation/resources/pre-prototype-checklist.md), including the **Top 3 fixes**
- (If time allows) fix 1 spot on the model and export a new GLB

---

## Prerequisites

- [ ] Have a `.glb` in Bitstream Studio from [M04](../../m04-blender-to-twin/l02-lab/README.md)
- [ ] Have a lid-opening clip, or note that a camera angle is used as a temporary substitute
- [ ] An evidence folder, `lab-notes/` or equivalent

---

## Lab A — Write scenarios before you click (required)

Choose at least 2 scenarios from Lesson §2.1 — **S3 (Lid service) is required**, plus one more.

| Scenario ID | Who / action | Expected result |
|---|---|---|
| S3 — Lid service | | |
| (second) | | |

**Pass when:** a teammate reads the table and can run it again without asking further questions

---

## Lab B — Run scenarios and log issues (required)

For each scenario:

1. Perform the action
2. Note expected vs actual
3. Take at least 1 screenshot per scenario
4. Accumulate the issue list (target ≥ 3 total, across all scenarios)

**Pass when:** both scenarios are fully logged, with ≥ 3 issues

---

## Lab C — Bind data or document the gap (required)

Choose one path:

| Option | What to do |
|---|---|
| **C1** | Link a Simulator/Board · open ex06 or ex05 · capture it alongside the Twin |
| **C2** | Bind a state in the Studio (colour/clip/highlight) to an event or mode |
| **C3** | Not bindable yet — write the reason + a plan for M06 into the checklist |

**Pass when:** there is image evidence **or** a clearly written reason in the checklist

---

## Lab D — Fill pre-prototype checklist (required)

1. Fill in every main row in [pre-prototype-checklist.md](../l01-scenario-digital-validation/resources/pre-prototype-checklist.md)
2. Write the **Top 3 design fixes before print**
3. Decide: Ready to print / Not ready (state the blockers)

**Pass when:** the Top 3 is not empty, and a Ready/Not ready decision is recorded

---

## Lab E — Optional quick fix loop

1. Pick 1 issue from the Top 3
2. Fix it in Blender
3. Export a GLB per [M04](../../m04-blender-to-twin/l01-blender-to-twin/README.md)
4. Import it again · quickly re-run S3
5. Note whether it improved

---

## Deliverables checklist

- [ ] 2 scenarios + screenshots
- [ ] ≥ 3 issues / watch-outs
- [ ] Pre-prototype checklist + Top 3 fixes
- [ ] Lab C evidence or a written gap
- [ ] (optional) a new GLB after a fix

---

## Troubleshooting

| Symptom | What to try |
|---|---|
| You don't know what problems to look for | Use the Risk table in Lesson §3 · turn on Wireframe while opening the lid |
| No sensor data stream | Use C3 · or run only S1–S3/S5, and plan the data binding for M06 |
| No lid-opening clip | Rotate the camera to simulate opening it · note that you need to go back to M03 |
| The checklist passes everything too quickly | Have a teammate review S3 again — it usually catches a missed hinge or port |
| The model's scale breaks after a fix | Apply Scale · check the Unit setting · export the whole file again |

[Lesson](../l01-scenario-digital-validation/README.md) · [Pre-prototype checklist](../l01-scenario-digital-validation/resources/pre-prototype-checklist.md) · [TOC](../../README.md) · [M06 →](../../m06-prototyping/l01-prototyping-final-project/README.md)
