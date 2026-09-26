---
id: twin.m03.l02
lang: en
title:
  th: 'แล็บ: สร้าง Virtual Device และ event script'
  en: 'Lab: Build a Virtual Device and Event Script'
summary:
  th: สร้างโมเดลอุปกรณ์ กำหนด behavior เขียนสคริปต์เหตุการณ์ที่รันซ้ำได้ และ (แนะนำ) ฝึก Blender สั้น ๆ แล้วส่งออก GLB
  en: Create the device model, define a behaviour, write a repeatable event script and (recommended) a short Blender exercise exported to GLB.
level: L3
time_min:
  lab: 210
hardware:
  emulator: true
  boards:
  - none
prerequisites:
- twin.m03.l01
objectives:
- th: สร้างโมเดลอุปกรณ์ (device-model.json หรือเทียบเท่า) ที่มีเซ็นเซอร์ ≥ 2 ชนิดและ behavior ≥ 1 เส้นทาง
  en: Create a device model (device-model.json or equivalent) with at least two sensors and at least one behaviour.
- th: รัน event script ซ้ำและเก็บหลักฐานผลบน visualization
  en: Run the event script repeatedly and capture evidence on the visualisation.
develops:
- skill: sys.simulation
  to: 2
- skill: iot.digital-twin
  to: 2
- skill: hwdev.3d-modeling
  to: 1
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
source_sha256: 7e6d271532e1dc82d19ac4ff7b7f215bb4dcc72ce290d39f797b12895c0611ac
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C2/M03/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M03 — Build a Virtual Device and Event Script

**Course 2 · Module 3**
**Type:** Hands-on (Virtual Device + optional Blender → GLB)
**Suggested time:** ~3–3.5 hours for the Virtual Device (+ ~1–1.5 hours for Lab E)

Read first: [Lesson](../l01-virtual-device-modeling/README.md) · [Device checklist](../l01-virtual-device-modeling/resources/device-model-checklist.md) · [Blender cheatsheet](../l01-virtual-device-modeling/resources/blender-twin-cheatsheet.md) · [Template](../l01-virtual-device-modeling/resources/sample-virtual-device.template.json) · [← Table of Contents](../../README.md) · [← M02](../../m02-vscode-twin/l01-vscode-for-twin/README.md) · [M04 →](../../m04-cosimulation/l01-firmware-twin-cosim/README.md)

### Useful references during the lab

| Document | Use when |
|---|---|
| [M02 lab](../../m02-vscode-twin/l02-lab/README.md) | Getting a Studio / Simulator session ready |
| [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) | Scene presets / web-app evidence |
| [Course 1 M05](../../../firmware-sdk-edge-ai/m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) | What the sensor values mean |
| [Blender Manual 4.5](https://docs.blender.org/manual/en/4.5/) | Modeling / Texturing / Animation |
| [INC111-2021 playlist (Thai)](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY) | A Thai-language video tutorial |
| [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free) | Sample GLB / textures |

---

## Lab Goals

- Have a Virtual Device with at least **2 kinds** of sensor defined
- Have at least **1** behaviour path (an input → an observable state)
- Have a repeatable event script/timeline, with the result visible in the visualization
- Fill in [device-model-checklist.md](../l01-virtual-device-modeling/resources/device-model-checklist.md)
- (Recommended) a short Blender exercise: model, or texture, or animation → export **GLB**

**Suggested time:** ~3–3.5 hours (the Virtual Device) + ~1–1.5 hours (Lab E Blender, if done)

---

## Prerequisites

- [ ] Lab M02 passed (you can open Bitstream Studio)
- [ ] Choose a path: **Simulator** and/or a board that can stream
- [ ] Have a `lab-notes/` folder for model files + evidence
- [ ] (Lab E) install [Blender](https://www.blender.org/download/)

---

## Lab A — Create the model (required)

1. Copy [sample-virtual-device.template.json](../l01-virtual-device-modeling/resources/sample-virtual-device.template.json) to your own file, such as `lab-notes/device-model.json`
2. Set `deviceId` / `displayName` to something your team can recognise
3. Enable at least 2 sensor kinds from: switch, temperature/pressure, IMU
4. Set `default` and the `min`/`max` range (or equivalent) sensibly
5. Name at least 1 actuator (an LED / a flag / a log sink)

On the host: open the Simulator or a board, then choose a **scene** matching the model (such as Lab Quiet for a slow demo, Motion when there's an IMU)

**Pass when:** the model file reads sensibly, and the host shows at least one value related to the sensors you chose

---

## Lab B — Behavior (required)

Define and demonstrate at least one rule, such as:

- A command/button → an LED, or a UI status
- Temperature over a threshold → an event / a log message / a mode change

Write it as a `WHEN … THEN …` sentence in the checklist

**Pass when:** a teammate can trigger the input and point to the result on screen without guessing

---

## Lab C — Event script (required)

Write a timeline of at least 4 beats (see the example in the lesson), then actually run it:

1. Start from the default values / Lab Quiet
2. Trigger a scalar or a switch at a set time
3. Trigger the IMU, or switch to Motion (if the model has an IMU)
4. Record what you saw (before/after screenshots, or a short clip)

You may run it with **a stopwatch + by hand** if the tool has no automatic script file yet — but it must be repeatable on a second round.

**Pass when:** rerunning the script gives roughly the same sequence of results

---

## Lab D — Optional polish

- Add a second behaviour (a threshold + a command)
- Compare the Lab Quiet vs Motion scene on the same sensor set
- Open the Hackathon `web-app/` as an outer Visualization screen

---

## Lab E — Blender for Twin (recommended)

Use [blender-twin-cheatsheet.md](../l01-virtual-device-modeling/resources/blender-twin-cheatsheet.md) as your link map.
A Thai-language tutorial: the [INC111-2021 playlist](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY)

Choose at least **one** track to complete:

### E1 — Modeling

1. Install [Blender](https://www.blender.org/download/)
2. Build a simple part (a box case / a flat board) from a mesh primitive
3. Use Extrude / Bevel / Mirror per the [Modeling intro](https://docs.blender.org/manual/en/4.5/modeling/meshes/introduction.html)
4. Set the origin + Apply Scale

### E2 — Texturing

1. Unwrap the UV ([UV unwrapping](https://docs.blender.org/manual/en/4.5/modeling/meshes/uv/unwrapping/index.html))
2. Add [Principled BSDF](https://docs.blender.org/manual/en/4.5/render/shader_nodes/shader/principled.html) + a Base Color
3. (Optional) use a texture from [ternion-3d-assets-free textures](https://github.com/drsanti/ternion-3d-assets-free/tree/main/assets/textures)

### E3 — Animation

1. Keyframe a rotation or a lid opening for 2–3 seconds ([Keyframes](https://docs.blender.org/manual/en/4.5/animation/keyframes/index.html))
2. Play it in the Timeline to see it clearly

### E4 — Export & view

1. **Export → glTF 2.0 → `.glb`** per the [glTF exporter](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html)
2. Load it into Bitstream Studio (or compare it against a model in the free assets)
3. Record a screenshot + the `.glb` filename in the checklist

**Pass when (Lab E):** there is a `.glb` file and evidence it opens in the host, or at least opens again in Blender after re-importing

---

## Deliverables checklist

- [ ] `device-model.json` (or equivalent)
- [ ] Labs A–C passed
- [ ] [device-model-checklist.md](../l01-virtual-device-modeling/resources/device-model-checklist.md) filled in completely
- [ ] Evidence the script ran (an image/clip)
- [ ] (Recommended) Lab D
- [ ] (Recommended) Lab E + a `.glb`

---

## Troubleshooting

| Symptom | Approach |
|---|---|
| The model is written but the screen doesn't change | Not Linked yet / it's in a different mode, Simulator vs Bitstream |
| The IMU doesn't move | You're on the Environment or Lab Quiet scene — switch to Motion, or trigger per the script |
| A behaviour shows no result | You haven't clearly set an observation point (LED/UI/log) |
| The values look too "fake" | Normal for the Simulator — note in the model that it's synthetic |
| Can't reproduce a run | Write times in seconds, and always start from the same default |
| The GLB has no texture | You forgot the UV / didn't use Principled / turned off Materials on export — see [glTF materials](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html) |
| The GLB has no animation | The Action wasn't active / Animation wasn't turned on for export |
| The model is too big in Studio | Reduce subdivision · decimate · check the scale |

[Lesson](../l01-virtual-device-modeling/README.md) · [Device checklist](../l01-virtual-device-modeling/resources/device-model-checklist.md) · [Blender cheatsheet](../l01-virtual-device-modeling/resources/blender-twin-cheatsheet.md) · [Table of Contents](../../README.md) · [M04 →](../../m04-cosimulation/l01-firmware-twin-cosim/README.md)
