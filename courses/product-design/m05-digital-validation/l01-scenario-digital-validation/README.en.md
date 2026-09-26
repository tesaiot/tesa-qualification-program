---
id: pdesign.m05.l01
lang: en
title:
  th: Digital validation ก่อนสร้างต้นแบบ
  en: Digital Validation before Prototyping
summary:
  th: ออกแบบสถานการณ์ทดสอบก่อนคลิก สังเกตและปรับดีไซน์ ผูกโมเดลกับข้อมูลเฟิร์มแวร์/Edge AI ด้วยหลักฐาน และสรุป checklist ก่อนพิมพ์
  en: Design test scenarios before clicking, observe and improve the design, bind the model to firmware/Edge AI data with evidence, and finish a pre-print checklist.
level: L2
time_min:
  concept: 35
  practise: 25
  check: 10
hardware:
  emulator: false
  boards:
  - none
prerequisites:
- pdesign.m04.l02
objectives:
- th: เขียน usage scenario อย่างน้อยสองรายการ พร้อมสิ่งที่ต้องดูบน Twin และสัญญาณผ่าน ก่อนลงมือทดสอบ
  en: Write at least two usage scenarios, each with what to watch on the Twin and its pass signal, before testing.
- th: ผูกสถานะเฟิร์มแวร์หรือ Edge AI หนึ่งอย่างเข้ากับการตอบสนองของโมเดล (สี คลิป หรือไฮไลต์) พร้อมหลักฐาน หรืออธิบายว่าทำไมยังผูกไม่ได้
  en: Bind one firmware or Edge AI state to a model response (colour, clip or highlight) with evidence, or explain why it cannot be bound yet.
- th: สรุปผลเป็น pre-prototype checklist ที่มี Top 3 fixes เรียงตามความสำคัญ
  en: Summarise the results as a pre-prototype checklist with the top three fixes in priority order.
develops:
- skill: iot.digital-twin
  to: 2
- skill: hwdev.enclosure
  to: 2
- skill: biz.product-decision
  to: 1
context:
  tool: blender-4.5
  twin-host: bitstream-studio
  output: glb, stl
status: alpha
translation: done
slides: slides.md
source_sha256: d713fce36cb75d636f4ee907510cf0dbef49e67141f37e56dc02073e59ddd338
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C3/M05/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M05 — Scenario and Digital Validation

**Course 3 · Module 5**
**Suggested time:** about 3 hours — run usage scenarios on the Twin, pair firmware/edge AI data, then fill in a fix list before printing a prototype
**Format:** a hands-on lesson — read it and test the scenarios directly; STL printing and the report are in [M06](../../m06-prototyping/l01-prototyping-final-project/README.md)

[Lab](../l02-lab/README.md) · [Pre-prototype checklist](resources/pre-prototype-checklist.md) · [← Table of Contents](../../README.md) · [← M04](../../m04-blender-to-twin/l01-blender-to-twin/README.md) · [M06 →](../../m06-prototyping/l01-prototyping-final-project/README.md)

---

## Objectives (Learning Outcomes)

By the end of this lesson you should be able to:

1. Set up a **usage scenario** (grip, place, open the lid, etc.) that the Twin can support
2. Assess the product's response and use the result to improve the design
3. Pair the model with **Edge AI / firmware** data (a state → colour / clip)
4. Do **Digital Validation** and produce an improvement list before building a prototype

> **Key phrase**
> Digital validation = *finding design bugs on screen before wasting plastic* — if you find a problem in M05 and don't write it down, you are not ready to print in M06.

### Read alongside this chapter

| Document | Use when |
|---|---|
| [M04 — Blender to Twin](../../m04-blender-to-twin/l01-blender-to-twin/README.md) | The GLB is already ready in Bitstream Studio |
| [M03 — Motion](../../m03-motion/l01-motion-and-interaction/README.md) | The `lid_open` clip for the lid-opening scenario |
| [Course 2 M04 / M05](../../../digital-twin/m04-cosimulation/l01-firmware-twin-cosim/README.md) | co-sim · telemetry · web-app consumers |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | Running the scenario on the Twin host |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | `web-app/ex06` (dashboard) · ex05 (orientation) |
| **[Electronic enclosure design guide (3DDFM)](https://www.3ddfm.com/design-guides/electronic-enclosure-design-guide/)** | An enclosure checklist / clearance / assembly |
| **[Protolabs — Enclosure for 3D printing](https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/)** | Walls · clearance before printing |
| **[All About Circuits — 3D-printed enclosure steps](https://www.allaboutcircuits.com/industry-articles/six-steps-for-designing-a-custom-3d-printed-electronics-enclosure/)** | The PCB-first validation mindset |
| **[DFM checklist thinking (Root3 Labs)](https://www.root3labs.com/dfm-checklist-prototype-to-production/)** | Questions before tooling / real production |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | Firmware reference when pairing a state |
| [Pre-prototype checklist](resources/pre-prototype-checklist.md) | This lesson's main deliverable form |

---

## 1. What Digital Validation Means in This Course

**Digital validation** in M05 is proving on the Twin that the enclosure + clips + sensor points **work together with real or simulated data**, before ordering a print in M06.

It is not:

- A substitute for full industry-standard testing
- A substitute for full impact simulation via FEA (unless you have that tool)

But it is:

```text
[Usage scenarios on Twin]
        │
        ▼
[Observe problems]  →  thin walls · blocked sensors · lid clash · bad port
        │
        ▼
[Bind firmware / Edge AI signals]  →  color / clip / highlight
        │
        ▼
[Pre-prototype checklist]  →  Top 3 fixes before print
```

Enclosure/DFM concepts used alongside this check: [3DDFM enclosure guide](https://www.3ddfm.com/design-guides/electronic-enclosure-design-guide/), [Protolabs enclosure guide](https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/)

---

## 2. Usage Scenarios — Design the Test First

Before playing a clip, write the scenario as a short sentence: **who, does what, expects to see what**.

### 2.1 Scenario catalog (pick at least two)

| Scenario ID | User action | What you watch on Twin | Pass signal |
|---|---|---|---|
| **S1 — Desk place** | Place the device on a desk in its normal orientation | The base sits still · the origin looks correct | It doesn't tip over in the view / the ports are readable once placed |
| **S2 — Handheld** | Hold the device (simulate a camera angle close to a hand) | Buttons/LEDs are within finger reach | No sharp edge blocks an important button |
| **S3 — Lid service** | Open the lid 3 times using the clip | Collision · the opening angle · seeing the PCB | No intersection · opening it reveals the service compartment |
| **S4 — Sensor access** | Trigger a sensor (scene/motion/tilting the board) | The `sensor_…` point + the value on a dashboard | The sensor opening is not blocked · there is a data stream |
| **S5 — Port plug** | Simulate plugging in a cable (look at the port opening) | The USB/port opening | The opening is big enough and faces the right way |
| **S6 — Alert state** | Trigger an over-threshold event (from Course 2) | A colour/highlight on the model, or a short clip | The firmware team and the design team can point to the same spot |

The lab requires at least **S3** plus one more from S1/S2/S4/S5 (adding S4 or S6 is recommended if you have a data stream).

### 2.2 How to run a scenario (lab loop)

1. Open the model in [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)
2. Read the scenario sentence out loud (or write it on the checklist)
3. Perform the action (play a clip / change the angle / trigger a sensor)
4. Note **what you expected** vs **what you saw**
5. If it breaks: log it as a fix item (don't fix it quietly without recording it)

### 2.3 Optional impact / drop (concept only)

If the Twin or the tools you have have **no** impact physics:

- Use a conceptual scenario: "if it fell off the desk, which corner of the box would take the force first?"
- Note your assumption + where the walls are thin — **do not claim you have actually simulated a real impact force**

---

## 3. Observe and Improve the Design

During/after a scenario, watch for these symptoms (summarised from general enclosure guidance):

| Risk | What it looks like | Typical fix before print |
|---|---|---|
| Walls too thin | The edges look sharp/thin in the Twin, or Thickness < ~2 mm | Increase thickness · add a rib in M02/M06 |
| A sensor opening is blocked | The opening is not above the chip · something else covers it | Move the opening · cut a new one |
| A port is hard to plug into | The opening is small/at the wrong angle | Enlarge the opening · add clearance |
| The lid hits a tall part | Opening the clip clips through USB/the display | Reduce the opening angle · move the hinge · adjust box height |
| Hard to assemble | No place for a screw / lid separation is unclear | Plan bosses in M06 · split parts for printing |
| Scale is off | It doesn't look right compared with the real board | Go back to M01/M04, fix it, and export again |

Log at least **3 issues** in the lab — even if some are "passes, but watch this."

If there is time: go back to Blender and fix **at least 1 spot**, then export a new GLB round (review [M04](../../m04-blender-to-twin/l01-blender-to-twin/README.md)).

---

## 4. Bind the Model to Edge AI / Firmware Data

Goal: make the Twin a **common language** between the design team and the firmware team.

### 4.1 Binding patterns (pick one or more)

| Firmware / Twin signal | Visual response on model |
|---|---|
| High temperature / a threshold event | Highlight the sensor opening area, or change the body's colour |
| BMI270 orientation | Rotate the preview to match the pose (if the host supports it), or compare two screens side by side |
| Mode / an LED on the device | Emission or a colour change at `led_status_window` |
| A lid-open command from the UI | Play the `lid_open` clip |

Review the data pipeline: [Course 2 M05](../../../digital-twin/m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md) · the points named in [M04](../../m04-blender-to-twin/l01-blender-to-twin/README.md)

### 4.2 Second screen — Hackathon dashboard

Recommended while running S4/S6:

1. Serve `web-app/` from [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)
2. Open **ex06** (multi-sensor dashboard) or **ex05** (orientation)
3. Capture both: the Twin scenario + the live sensor values

If there is no data stream in this round, use a **simulated state script** in the Studio (if available), or record binding the data as a plan for M06 / Course 2 — don't leave the gap without writing a reason.

### 4.3 Evidence rule

| Binding claim | Evidence required |
|---|---|
| "The model responds to the sensor" | A screenshot/clip showing both the model and the value change |
| "The sensor opening is at the right position" | A Twin image pointing at the spot + the `sensor_…` name + (if any) the real board |
| "Cannot be bound in this round yet" | A short reason + what will be done in M06 |

---

## 5. Digital Validation Checklist (Before Prototype)

Fill in the full version in [pre-prototype-checklist.md](resources/pre-prototype-checklist.md)

### 5.1 Minimum validation columns

| Area | Key question |
|---|---|
| **Scale** | Does the size still match the board/the M01 formula? |
| **Internal fit** | Do the PCB + battery + cables all fit together? |
| **Sensor openings** | Are the openings at the real sensor positions? |
| **Ports** | Can you plug in a cable/see the LED? |
| **Walls** | Thick enough to print (~2 mm as a starting point) |
| **Motion** | Does the lid/button collide with another part? |
| **Twin stability** | Does the GLB import reliably, and can clips play? |
| **Data link** | Is at least one state binding present, or is there a reason it isn't yet? |

Further enclosure/DFM questions for reference: [3DDFM checklist section](https://www.3ddfm.com/design-guides/electronic-enclosure-design-guide/), [Root3 DFM questions](https://www.root3labs.com/dfm-checklist-prototype-to-production/)

### 5.2 Top 3 fixes before print

The end of the checklist must have **3 fixes in priority order**, for example:

1. Enlarge the USB opening by +0.5 mm per side
2. Reduce the lid's opening angle from 110° to 95°
3. Increase the lid's wall thickness to 2.0 mm

If everything passes: write "Ready to print" and state what still needs watching during real assembly.

---

## 6. Quality Gate Before M06

| Check | Pass means |
|---|---|
| ≥ 2 scenarios run | Expected vs actual is recorded |
| ≥ 3 design issues or watch-outs logged | None left blank |
| Pre-prototype checklist filled | Including the top 3 fixes |
| Optional: 1 model fix re-exported | A new GLB exists if a fix was made |
| Optional: telemetry/web-app pair shot | Evidence of the data binding |

---

## Next Steps

1. Do the lab: [Lab](../l02-lab/README.md)
2. Fill in [pre-prototype-checklist.md](resources/pre-prototype-checklist.md)
3. When ready, continue to [M06 — Prototyping and Final Project](../../m06-prototyping/l01-prototyping-final-project/README.md)

---

## References and Further Reading

1. [M04 Blender to Twin](../../m04-blender-to-twin/l01-blender-to-twin/README.md) · [M03 Motion](../../m03-motion/l01-motion-and-interaction/README.md) · [Course 3 TOC](../../README.md)
2. [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)
3. [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) — `ex05`, `ex06`
4. [TESAIoT Developer Hub](https://dev.tesaiot.dev/)
5. [Electronic Enclosure Design Guide (3DDFM)](https://www.3ddfm.com/design-guides/electronic-enclosure-design-guide/)
6. [Enclosure design for 3D printing (Protolabs Network)](https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/)
7. [Six steps for 3D-printed electronics enclosures (All About Circuits)](https://www.allaboutcircuits.com/industry-articles/six-steps-for-designing-a-custom-3d-printed-electronics-enclosure/)
8. [DFM checklist questions (Root3 Labs)](https://www.root3labs.com/dfm-checklist-prototype-to-production/)
9. [Course 2 M04](../../../digital-twin/m04-cosimulation/l01-firmware-twin-cosim/README.md) · [Course 2 M05](../../../digital-twin/m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md)

---

## Check your understanding

Three short questions in [quiz.yaml](quiz.yaml), one per objective of this lesson. Try answering them yourself first, then compare with the answer key and explanations in the file.

## Lab

Continue hands-on at [Lab: usage scenarios and a pre-prototype checklist](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Pre-prototype checklist](resources/pre-prototype-checklist.md) · [← TOC](../../README.md) · [← M04](../../m04-blender-to-twin/l01-blender-to-twin/README.md) · [M06 →](../../m06-prototyping/l01-prototyping-final-project/README.md)
