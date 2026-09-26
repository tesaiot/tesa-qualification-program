---
id: twin.m04.l02
lang: en
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
source_sha256: 6f8a33abb520682d143b1f2147047155810636d65e787c02823d8fca3153c2b6
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C2/M04/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M04 — Co-simulation End-to-End I/O

**Course 2 · Module 4**
**Type:** Hands-on (bring-up + input path + output path + latency)
**Suggested time:** ~2.5–3 hours

Read first: [Lesson](../l01-firmware-twin-cosim/README.md) · [Checklist](../l01-firmware-twin-cosim/resources/cosim-checklist.md) · [← Table of Contents](../../README.md) · [← M03](../../m03-virtual-device/l01-virtual-device-modeling/README.md) · [M05 →](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md)

### Useful references during the lab

| Document | Use when |
|---|---|
| [M02 lab](../../m02-vscode-twin/l02-lab/README.md) | Studio / Simulator / COM |
| [M03 lab](../../m03-virtual-device/l02-lab/README.md) | An event script / a Virtual Device |
| [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) | A HEX · `web-app/` evidence |
| [Course 1 M04](../../../firmware-sdk-edge-ai/m04-rtos/l01-freertos-programming/README.md) | Task timing |

---

## Lab Goals

- Run firmware alongside the Twin/host reliably
- Prove **input**: trigger it → the firmware perceives it
- Prove **output**: the firmware commands it → the host/Twin reflects it
- Note rough latency at at least 1 point
- Fill in [cosim-checklist.md](../l01-firmware-twin-cosim/resources/cosim-checklist.md)

---

## Prerequisites

- [ ] M02's first session passed
- [ ] M03 has a device model + an event script (or a timeline)
- [ ] Choose a path: **Simulator** and/or **Board + HEX**
- [ ] A `lab-notes/` folder for evidence

---

## Lab A — Bring-up co-sim (required)

1. Open Bitstream Studio
2. Choose **Simulator** *or* **Bitstream** (only one)
3. Link until there's a stream/heartbeat
4. Wait ≥ 30 seconds without it dropping
5. Take a screenshot of the Link status + the graph/values

**Pass when:** both the host and the firmware source (sim or board) show a clear sign of life

---

## Lab B — Input path (required)

1. Use the script/timeline from M03, or trigger it with a scene/UI/button
2. Have the firmware show it read the value (a UART log, a mode change, or a value echoed on the host that is clearly from the read logic)
3. Record: what was triggered → what the firmware reported

**Pass when:** someone on the team can explain the Twin/stimulus → firmware arrow, with evidence

---

## Lab C — Output path (required)

1. Have the firmware change at least one output (an LED, a flag, a publish, a log marker)
2. Confirm that Bitstream Studio (or the `web-app/`) reflects the result
3. Compare it against the WHEN/THEN behaviour from M03

**Pass when:** there is paired evidence (the firmware side + the host side)

---

## Lab D — Latency note (recommended)

1. Choose one measurement point (such as stimulus → the first log line)
2. Do 3 rounds and note the approximate value
3. Guess 1 likely cause of delay (the task period / the scene rate / the UI)
4. Fill it into the checklist

**Pass when:** there is a value range and a hypothesis for the delay source — it doesn't need to be the prettiest number

---

## Lab E — Optional extras

- Compare Path A (Simulator) with Path B (Board) on the same script
- If there is a GLB from M03 — load it into the scene and note what the image helps demonstrate (it does not replace sensor truth)

### Lab E1 — Hackathon web-app `ex05` (recommended)

Read the walkthrough in [README §4](../l01-firmware-twin-cosim/README.md) first

1. Serve the Hackathon **`web-app/`** folder and open **`ex05_bmi270_orientation.html`**
2. Confirm the badge is `connected`, with a `route:`
3. In the sensor settings, turn on BMI270 **Euler** and/or **Quaternion** in the publish mask
4. Tilt the board, or switch to the Motion scene — the horizon + ° must move
5. Take a screenshot **alongside** the BMI270 panel in Studio; note the `source:` and `mask 0x…`

**Pass when:** you can explain that ex05 proves the outer output path, and that if it stays stuck at *waiting for orientation*, the mask is incomplete (not just "the web page is broken")

---

## Deliverables checklist

- [ ] Labs A–C passed
- [ ] [cosim-checklist.md](../l01-firmware-twin-cosim/resources/cosim-checklist.md) filled in completely
- [ ] Input + output evidence (screenshot/clip/log)
- [ ] (Recommended) Lab D latency
- [ ] (Recommended) Lab E / E1 (`ex05`)

---

## Troubleshooting

| Symptom | Approach |
|---|---|
| The Link doesn't come up | Shutdown the backends · check the port · M02 |
| There's a graph, but it's silent after triggering | Check the scene/cfg · the M03 script · the firmware log |
| The log is correct, but the UI doesn't move | The wrong panel is open · the consumer didn't connect |
| Latency values are very scattered | Use a log timestamp · don't time it by eye alone |
| Switching Simulator/Bitstream causes confusion | Clear the data · Link fresh, one mode at a time |
| ex05 is stuck at *waiting for orientation* | Turn on Euler/Quaternion in the BMI270 mask — not just accel/gyro |
| ex05 is disconnected | Serve the correct `web-app/` folder · Studio/the bridge is open |

[Lesson](../l01-firmware-twin-cosim/README.md) · [Checklist](../l01-firmware-twin-cosim/resources/cosim-checklist.md) · [Table of Contents](../../README.md) · [M05 →](../../m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md)
