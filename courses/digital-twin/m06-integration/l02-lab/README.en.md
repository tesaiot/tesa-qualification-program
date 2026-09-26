---
id: twin.m06.l02
lang: en
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
source_sha256: 1245eb3ea4185e2256e0238679df43c25c042b30115e4a80979539e32b21d251
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C2/M06/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M06 — E2E Mini-Project on Digital Twin

**Course 2 · Module 6**
**Type:** Capstone / End-to-End
**Suggested time:** ~2 hours (+ extra time for the README and evidence)

Read first: [Lesson](../l01-system-integration-testing/README.md) · [Case brief](../l01-system-integration-testing/resources/e2e-case-brief.md) · [Course package](../l01-system-integration-testing/resources/course-package.md) · [← TOC](../../README.md) · [← M05](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md)

### Useful references during the lab

| Document | Use when |
|---|---|
| [M03](../../m03-virtual-device/l02-lab/README.md) · [M04](../../m04-cosimulation/l02-lab/README.md) · [M05](../../m05-telemetry-cloud/l02-lab/README.md) | The device · co-sim · MQTT |
| [Hackathon `web-app/`](https://github.com/drsanti/TESAIoT_Hackathon) | **ex06** · **ex15** (or ex09) |
| [Developer Hub](https://dev.tesaiot.dev/) | Firmware examples |
| [Course 1 M08](../../../firmware-sdk-edge-ai/m08-capstone/l02-lab/README.md) | The Capstone format on the board side |

---

## Lab Goals

Deliver a short demo on the Twin, covering the full path:

**stimulus → firmware → Studio visualization → an external dashboard/MQTT**
with a test table of ≥ 3 cases, and a rerunnable README.

---

## Prerequisites

- [ ] M02's Link is stable
- [ ] M03 has a virtual device + an event script (or equivalent)
- [ ] M04's co-sim passed on at least one Path
- [ ] M05 already succeeded at Start broker + a subscriber
- [ ] A deliverables folder + `lab-notes/`

---

## Recommended brief — pick a domain story

Start from the **Smart Environmental Monitor** (IoT / environmental), or map it onto another domain per [README §4](../l01-system-integration-testing/README.md):

| Domain | Story emphasis | Main sensor | Extra evidence |
|---|---|---|---|
| IoT | A node ↔ the cloud | SHT40 + state | ex06 + ex15 |
| Home | A comfortable / safe room | SHT40 + a switch | ex06 + an MQTT cmd |
| Industrial | An alarm on the line | temp/IMU | ex06 + ex08 + ex15 |
| Health-sim | A watch link (simulated) | BMI270 + SHT40 | ex05 + ex08 + ex09 |

| Part | Example choice (adjust per domain) |
|---|---|
| Sensors | SHT40 temp/humidity (± another sensor) |
| Behavior | Over a threshold → a state/event + a signal on the host |
| Script | Quiet → Warm/Alert |
| MQTT | Publish telemetry; optionally subscribe to a command |
| Evidence | Studio + **ex06** + (**ex15** or **ex09**) |

Fill in the detail in [e2e-case-brief.md](../l01-system-integration-testing/resources/e2e-case-brief.md)

---

## Lab A — Lock architecture (required)

1. Choose a **domain** from [README §4](../l01-system-integration-testing/README.md) (IoT / Home / Industrial / Health-sim)
2. Draw/write the 4-step diagram from Lesson §2, and add event names matching the domain
3. State the Path: Simulator / Board / Both
4. State the MQTT topic and the web consumer page you'll use as evidence
5. Copy the README outline from Lesson §6.2 into your project (fill in the Domain line)

**Pass when:** a teammate reads it and knows the domain + which tool to open first, without asking anything further

---

## Lab B — Assemble the running demo (required)

1. Bring up Studio (a single backend) + co-sim
2. Run your event script / scene
3. Confirm the value on Studio
4. Serve `web-app/` → open **ex06** to see the relevant sensors
5. Start broker → publish (and/or subscribe) → confirm on **ex15** or **ex09**

**Pass when:** the Normal demo runs continuously for ≥ 1 minute without the Link dropping on its own

---

## Lab C — Three E2E test cases (required)

Run and fill in the table in the case brief:

| Case | Must prove at minimum |
|---|---|
| **Normal** | Telemetry updates on Studio + the consumer |
| **Stimulus** | A threshold / switch / script clearly changes a state or event |
| **Command / fault** | An MQTT command, **or** briefly cutting the broker/stream then recovering |

**Pass when:** at least 3 rows have a real result + Passed? = Yes (or Fail, with a reason and an acceptable workaround)

---

## Lab D — Log triage drill (recommended)

Deliberately break one thing (turn off the broker / stop the script / open the wrong panel), then:

1. Work through the layers in Lesson §3
2. Note the layer where the problem was found
3. Fix it back to a green demo

**Pass when:** there is a line in the case brief's issues/fixes section

---

## Lab E — Package for handoff (required)

- [ ] A rerunnable README
- [ ] The case brief filled in completely
- [ ] Screenshot/clip evidence (Studio + ex06 and the MQTT consumer)
- [ ] No password in the submitted files
- [ ] The checklist from [course-package.md](../l01-system-integration-testing/resources/course-package.md)

---

## Deliverables checklist

- [ ] Labs A–C, E passed
- [ ] (Recommended) Lab D
- [ ] A link/folder for the project, ready to hand off

---

## Troubleshooting

| Symptom | Approach |
|---|---|
| The demo runs a while, then drops | Go back to M02/M04's bring-up · don't mix backends |
| ex06 is empty but Studio has values | Serve the right folder · check the connection badge · the mask/fields |
| MQTT is empty | Start broker · check the topic matches · it's a different pipe from Live Data |
| A stimulus doesn't show on the consumer | Check the script actually ran · staleness · the publish rate |
| The deliverable has a secret in it | Remove it and put a placeholder in the README |

[Lesson](../l01-system-integration-testing/README.md) · [Case brief](../l01-system-integration-testing/resources/e2e-case-brief.md) · [Course package](../l01-system-integration-testing/resources/course-package.md) · [TOC](../../README.md)
