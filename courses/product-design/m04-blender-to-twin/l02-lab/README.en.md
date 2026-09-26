---
id: pdesign.m04.l02
lang: en
title:
  th: 'แล็บ: ส่งออก GLB และนำเข้า Twin'
  en: 'Lab: Export GLB and Import to Twin'
summary:
  th: เตรียมไฟล์ ส่งออก .glb นำเข้า Twin host ทำเครื่องหมายจุดเซ็นเซอร์/โต้ตอบ แล้วทดสอบด้วยคลิปหรือข้อมูล
  en: Prepare the file, export .glb, import it into the Twin host, mark sensor/interaction points, then test with a clip or data.
level: L2
time_min:
  lab: 180
hardware:
  emulator: false
  boards:
  - none
prerequisites:
- pdesign.m04.l01
objectives:
- th: ส่งออก enclosure_twin.glb และนำเข้า Bitstream Studio โดยขนาดและแกนใช้งานได้
  en: Export enclosure_twin.glb and import it into Bitstream Studio with usable scale and axis.
- th: กำหนดจุด sensor/interaction ≥ 1 จุดพร้อมชื่อ และทดสอบด้วยคลิปแอนิเมชันหรือ telemetry
  en: Mark at least one named sensor/interaction point and test with an animation clip or telemetry.
develops:
- skill: hwdev.3d-modeling
  to: 2
- skill: iot.digital-twin
  to: 2
assesses:
- skill: hwdev.3d-modeling
  level: 2
  evidence: README.md#deliverables-checklist
context:
  tool: blender-4.5
  twin-host: bitstream-studio
  output: glb, stl
status: alpha
translation: done
slides: slides.md
source_sha256: a9712a82750992502d07467f525459b1c96a6324ab9a3b7d0758d6a41eb63ef5
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C3/M04/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M04 — Export GLB and Import to Twin

**Course 3 · Module 4**
**Type:** Hands-on (prepare · export · import · mark points · test)
**Suggested time:** ~2.5–3 hours

Read first: [Lesson](../l01-blender-to-twin/README.md) · [Export checklist](../l01-blender-to-twin/resources/export-twin-checklist.md) · [← TOC](../../README.md) · [← M03](../../m03-motion/l01-motion-and-interaction/README.md) · [M05 →](../../m05-digital-validation/l01-scenario-digital-validation/README.md)

### Keep these tabs open

| Document | Why |
|---|---|
| [glTF 2.0 exporter](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html) | export options |
| [glTF Animations](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#animations) | stash / names |
| [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) | Twin host |
| [Hackathon web-app](https://github.com/drsanti/TESAIoT_Hackathon) | optional ex05 / ex06 |

---

## Lab Goals

- Produce a **`.glb`** file from the M02/M03 model
- Import it into [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) with a usable size/axis orientation
- Mark at least **1** named sensor or interaction point
- Test at minimum: placing the model + (an animation clip **or** telemetry)
- Fill in [export-twin-checklist.md](../l01-blender-to-twin/resources/export-twin-checklist.md)

---

## Prerequisites

- [ ] A file from M03 (or M02, if there is no clip yet — note this in the checklist)
- [ ] Bitstream Studio ready to use
- [ ] Copy the work to `m04_enclosure_twin.blend` before exporting

---

## Lab A — Prepare for export (required)

1. Apply Scale on the parts you will send
2. Check the object names and clip names (`lid_open`, etc.)
3. If there are several Actions: stash them into the NLA per the [glTF guide](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#animations)
4. Hide/delete cutters and anything you don't want to send
5. Save the `.blend`

**Pass when:** playback in Blender is still correct, and Scale reads 1,1,1

---

## Lab B — Export `.glb` (required)

1. `File → Export → glTF 2.0`
2. Choose **glTF Binary (.glb)**
3. Turn on Apply Modifiers · Materials · Animations (if any)
4. Export as `enclosure_twin.glb`
5. Record the export options used in the checklist

**Pass when:** a `.glb` file exists and is not 0 bytes

---

## Lab C — Import into Twin host (required)

1. Open Bitstream Studio
2. Import `enclosure_twin.glb` per that version's UI
3. Check: it is visible · the scale works · the orientation lets it sit on the floor
4. If there is a clip — play `lid_open` (or whatever name was exported)
5. Take a screenshot

**Pass when:** a screenshot shows the model in the host, and the checklist has Import OK ticked

---

## Lab D — Mark sensor / interaction point (required)

1. Choose at least 1 point (for example `sensor_bmi270_slot` or `interact_lid`)
2. Record: the name · where it is on the box · what it is tied to (a sensor / a clip / an LED)
3. Add a screenshot or sketch in the checklist

**Pass when:** someone else on the team reads the name and correctly points to the spot on the model

---

## Lab E — Data or motion test (recommended — part of the complete deliverable)

Choose at least one:

| Option | What to do |
|---|---|
| **E1 — Clip** | Play the animation in the Twin through a full open cycle (and close, if any) |
| **E2 — Telemetry** | Link a Simulator or a Board so there is a data stream while the model is on screen |
| **E3 — Web-app** | Open Hackathon **ex05** or **ex06** alongside the Twin and capture both |

**Pass when:** there is image/clip evidence in the deliverables folder

---

## Lab F — Optional

- Compare scale with a GLB from [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)
- Re-import the `.glb` back into Blender to confirm the clip is not lost
- Reduce poly count and export a second time, comparing file sizes

---

## Deliverables checklist

- [ ] `enclosure_twin.glb` (+ the source `.blend`)
- [ ] A screenshot from Bitstream Studio
- [ ] ≥ 1 sensor/interaction point
- [ ] The Lab E test result
- [ ] [export-twin-checklist.md](../l01-blender-to-twin/resources/export-twin-checklist.md) filled in completely

---

## Troubleshooting

| Symptom | What to try |
|---|---|
| The model is gigantic or tiny in the Twin | Check the team's Unit Scale · Apply Scale · export again — don't just zoom to compensate and call it done |
| No animation in the GLB | Stash the Action · turn on Animations during export · check the clip name |
| Materials look black/missing | Use Principled · check Materials is on during export · check the lighting in the Twin |
| A Boolean looks wrong after export | Turn on Apply Modifiers |
| Import fails to show anything | Check the `.glb` extension · try a sample model from the free assets to tell whether the file or the host is the problem |
| Telemetry seems unrelated to the model | They're different pipes — the model is the picture; use ex05/ex06 as the data evidence |

[Lesson](../l01-blender-to-twin/README.md) · [Export checklist](../l01-blender-to-twin/resources/export-twin-checklist.md) · [TOC](../../README.md) · [M05 →](../../m05-digital-validation/l01-scenario-digital-validation/README.md)
