---
id: pdesign.m04.l01
lang: en
title:
  th: ส่งออก GLB และนำเข้า Twin host
  en: Exporting GLB and Importing into the Twin Host
summary:
  th: ความหมายของ Twin-ready การเตรียมไฟล์ก่อน export ขั้นตอน glTF Binary การตรวจหลังนำเข้า จุดเซ็นเซอร์และจุดโต้ตอบ และเมทริกซ์ทดสอบขั้นต่ำ
  en: What Twin-ready means, preparing the file, exporting glTF Binary, post-import checks, sensor and interaction points, and the minimum test matrix.
level: L2
time_min:
  concept: 40
  practise: 25
  check: 10
hardware:
  emulator: false
  boards:
  - none
prerequisites:
- pdesign.m03.l02
objectives:
- th: เตรียมไฟล์ก่อน export (หน่วย Apply Scale origin ลบ cutter/ไฟทดสอบ ชื่อ object) และส่งออกเป็น glTF Binary (.glb)
  en: Prepare the file before export (units, apply scale, origin, remove cutters/test lights, object names) and export glTF Binary (.glb).
- th: นำ .glb เข้า Bitstream Studio แล้วตรวจสเกล แกน ชื่อชิ้นส่วน และคลิปตามรายการตรวจ
  en: Import the .glb into Bitstream Studio and check scale, axis, part names and clips against the checklist.
- th: ตั้งชื่อจุดเซ็นเซอร์และจุดโต้ตอบตามรูปแบบ `sensor_…` / `interact_…` และทดสอบด้วยคลิปหรือ telemetry
  en: Name sensor and interaction points as `sensor_…` / `interact_…` and test them with a clip or telemetry.
develops:
- skill: hwdev.3d-modeling
  to: 2
- skill: iot.digital-twin
  to: 1
context:
  tool: blender-4.5
  twin-host: bitstream-studio
  output: glb, stl
status: alpha
translation: done
slides: slides.md
source_sha256: 3f99662a2af5e5e34e8db0e6cafce6c184e8955ec7167eb26aea10c01f1a3d78
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C3/M04/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M04 — Blender to Twin Integration

**Course 3 · Module 4**
**Suggested time:** about 3 hours — export GLB from Blender, import into a Twin host, define sensor/interaction points, then test against telemetry or an animation clip
**Format:** a hands-on lesson — read it and follow along directly; full usage-scenario simulation is in [M05](../../m05-digital-validation/l01-scenario-digital-validation/README.md)

[Lab](../l02-lab/README.md) · [Export checklist](resources/export-twin-checklist.md) · [← Table of Contents](../../README.md) · [← M03](../../m03-motion/l01-motion-and-interaction/README.md) · [M05 →](../../m05-digital-validation/l01-scenario-digital-validation/README.md)

---

## Objectives (Learning Outcomes)

By the end of this lesson you should be able to:

1. Export the model in **glTF/GLB** form (with FBX/OBJ as alternatives), ready to use with the Twin
2. Bring the model into **TESA Digital Twin** through the course's main host ([Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio))
3. Define **interaction points**, sensor points, and mounting positions
4. Test the model together with **telemetry / motion / sensor value** data

> **Key phrase**
> A good GLB = *correct size · correct axes · clear clip names · exportable materials* — import into the Twin, then dress the scene; don't fix the scale a hundred times over afterward.

### Read alongside this chapter

| Document | Use when |
|---|---|
| [M03 — Motion and Interaction](../../m03-motion/l01-motion-and-interaction/README.md) | The `lid_open` clip / the clip list |
| [Course 2 M03 — Blender for Twin](../../../digital-twin/m03-virtual-device/l01-virtual-device-modeling/README.md) | A short overview of exporting GLB |
| **[glTF 2.0 exporter (Blender 4.5)](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html)** | Mesh / Materials / Animations options |
| **[glTF Animations](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#animations)** | Stashing Actions · clip names |
| **[glTF Materials](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#materials)** | Principled BSDF that exports correctly |
| **[Apply Scale](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/apply.html)** | Before exporting |
| **[Khronos glTF](https://www.khronos.org/gltf/)** | The file standard the Twin / the web uses |
| **[Bitstream Studio (Marketplace)](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | Importing / displaying a 3D model + telemetry |
| **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** | Sample GLB files, for reference on scale and materials |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | `web-app/`, e.g. **ex05** for comparing sensor data |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | Board reference when pairing sensor points |
| [Export checklist](resources/export-twin-checklist.md) | The deliverables form |

---

## 1. What "Twin-ready" Means Here

In Course 3, the main Digital Twin host is **Bitstream Studio** (a VS Code extension) — it accepts **glTF Binary (`.glb`)** files for preview / Sensor Studio / Animation Lab, depending on the tools available.

```text
[Blender .blend]
   export glTF 2.0
        │
        ▼
   enclosure_twin.glb
        │
        ▼
[Bitstream Studio / Twin host]
   place model · mark sensor/interaction · play clip
        │
        ├── optional: live telemetry (Simulator or Board)
        └── optional: Hackathon web-app ex05 / ex06 as second screen
```

| Format | Use when |
|---|---|
| **`.glb`** | **The main target** — a single file combining mesh + materials + animations |
| `.gltf` + bins/textures | When you need to keep textures separate for external editing |
| FBX / OBJ | A backup route for other tools — not the web Twin's main path |
| STL | Kept for printing in M06 — does not replace GLB for the Twin |

Standard: [Khronos glTF](https://www.khronos.org/gltf/)

---

## 2. Prepare the Blend File Before Export

Follow this order every time, before pressing Export.

### 2.1 Scale, origin, and cleanup

| Step | Action | Why |
|---|---|---|
| 1 | Check the team's units still match M01 (Metric + mm + the agreed Unit Scale) | Prevents scale problems in the Twin |
| 2 | `Ctrl+A` → **Scale** (and Rotation if needed) on the parts you will send | [Apply](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/apply.html) |
| 3 | The lid's Origin is at the hinge (from M03) | The clip rotates around the right point |
| 4 | Delete/hide cutters, test lights, and cameras you don't want to send | A lighter, tidier file |
| 5 | Objects have short English names | So they can be referenced in the Twin / the checklist |

### 2.2 Materials that survive export

Use **Principled BSDF**, as practised in M02 — glTF supports its main parameters well ([glTF Materials](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#materials))

| Do | Avoid for Twin export |
|---|---|
| Clear Base Color / Roughness / Metallic | Complex shaders glTF does not understand |
| Enough UV for any important pattern (if using a texture) | Relying only on procedural nodes that cannot be baked |
| Test in Material Preview before exporting | Assuming EEVEE and the Twin look exactly the same |

### 2.3 Animations that will be included

Per [glTF Animations](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#animations):

- An Action is exported if it is the **active action**, or has been **stashed** into an NLA track
- If there are several clips (`lid_open`, `lid_close`), stash them all before exporting
- Track/action names affect the clip names in the GLB — use the same names as in the [clip list](../../m03-motion/l01-motion-and-interaction/resources/animation-clip-list.md)

### 2.4 Optional: reduce polycount

If the file is large or the Twin stutters:

- Reduce unnecessary subdivision
- Don't reduce it so much the port openings become unreadable
- Compare the file size with the examples in [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free) as a rough guide

---

## 3. Export glTF Binary (.glb) — Step by Step

Full reference: [glTF 2.0](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html)

1. Select only the parts to send (or send the whole scene, per the team's agreement)
2. `File → Export → glTF 2.0`
3. Format: **glTF Binary (.glb)**
4. Recommended options to turn on at minimum:

| Export option | Lab tip |
|---|---|
| **Selected Objects** (if you selected parts) | Prevents lights/test planes going along with it |
| **Data → Mesh → Apply Modifiers** | Sends the result of any Boolean/Solidify/Bevel not yet applied in the scene |
| **Materials** | Includes the Principled setup |
| **Animations** (if there is a M03 clip) | Turn it on and check the Mode below |

5. Animation Mode (when there are several clips):

| Mode | Use when |
|---|---|
| **Actions** (default) | There is an active action, or one already stashed in the NLA |
| **NLA Tracks** | Managing several tracks as clearly separate clips |

6. Name the file, for example `enclosure_twin.glb`, then Export
7. Check the file size and open it in your system's preview tool (or temporarily import it back into Blender) to confirm the clips still play

Record the options actually used in [export-twin-checklist.md](resources/export-twin-checklist.md)

---

## 4. Import into Bitstream Studio (Twin Host)

### 4.1 Bring-up

1. Install/open [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) from VS Code
2. Open your workspace (review the host approach from [Course 2](../../../digital-twin/README.md) if you have taken it)
3. Import the `.glb` file per that round's UI, for example
   - The **Assets / Model / Free Loader** panel
   - Or **Sensor Studio / 3D preview / Animation Lab**

Button details may differ by version — follow the manual for the version you're using, and note the panel name used in the checklist.

### 4.2 First checks after import

| Check | Pass means |
|---|---|
| Model visible | The box is visible in the viewport |
| Scale usable | Not abnormally tiny/gigantic compared with the real thing or the PCB you have in mind |
| Up-axis / orientation | It can sit on the "floor" without a long corrective rotation |
| Named parts readable | The lid/base can be told apart if the Twin shows a hierarchy |
| Animation (if exported) | `lid_open` plays, or a clip list is present |

If the scale is badly wrong: **go back and fix it in Blender, then export again** — don't just zoom to compensate in the Twin and call it done (that is acceptable only as a temporary workaround).

### 4.3 Compare with a known-good GLB (optional)

Load a model from [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free) alongside it, to confirm your machine's import pipeline works — then switch back to your own model.

---

## 5. Interaction Points and Sensor Nodes

The goal of this section: get the design team and the firmware team **speaking the same language**.

### 5.1 What to mark

| Point type | Example on your enclosure | Link to firmware / Twin |
|---|---|---|
| **Sensor node** | The opening above the IMU / temperature sensor | Sensor name, e.g. `bmi270`, `sht40` |
| **Interaction point** | The lid · a button · an LED window | The `lid_open` clip · an LED state |
| **Mount / placement** | The base that sits on a desk · screw holes | The origin used for placement in the scene |

In the lab, name at least **1 point** clearly enough to explain (its position on the model + a name tied to data).

### 5.2 Naming convention (lab)

```text
sensor_bmi270_slot
sensor_sht40_vent
interact_lid
interact_user_button
led_status_window
```

Record each name ↔ its meaning in the checklist — don't use a random name.

### 5.3 How you "define" them in the lab

Depending on the tools available, any one of these counts:

- An Empty / locator in Blender that gets exported along with the model
- A position note + a screenshot in the Twin
- Binding an animation clip or material to a state in the UI

What matters is **having evidence and a consistent name**, not just pointing at the air during a presentation.

---

## 6. Test with Telemetry or Motion Data

### 6.1 Minimum test matrix

| Test | How | Pass |
|---|---|---|
| **A — Static placement** | The model sits still in the Twin | Size/axes are usable |
| **B — Clip playback** | Play `lid_open` in the host | The lid opens as designed |
| **C — Live or sim data** (recommended) | Link a Simulator or Board + watch telemetry | Sensor values flow while the model is on screen |

### 6.2 Suggested second screen — Hackathon web-app

Once the model is in the Twin (this does not replace the export step):

1. Serve the `web-app/` folder from [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)
2. Open **ex05** (orientation) or **ex06** (dashboard), depending on the sensors you have
3. Capture both: the Twin with the model + the web-app with the values

Use this to teach that a 3D model is a **visual shell** — the sensor's truth lives in the data stream ([Course 2 M04](../../../digital-twin/m04-cosimulation/l01-firmware-twin-cosim/README.md) has an ex05 walkthrough).

### 6.3 Example bindings (pick one)

| If you have… | Binding idea |
|---|---|
| A BMI270 stream | Rotate/tilt the preview per orientation (if the host supports it), or compare against ex05 |
| A threshold / mode event | Change the colour of the `led_status_window` part, or play a short clip |
| Lid interaction in the UI | A button in the Twin that triggers `lid_open` |

You don't need to complete every item in 3 hours — choose at least one path with evidence.

---

## 7. Quality Gate Before M05

| Check | Pass means |
|---|---|
| A `.glb` file exists | Its name and location are recorded in the checklist |
| Import OK in Bitstream Studio | A screenshot |
| Scale / axis usable | No need to re-guess the scale |
| ≥ 1 sensor or interaction point documented | Name + position |
| Clip names match the M03 list (if any) | No renaming during export without recording it |
| Optional telemetry evidence | From the Studio and/or the web-app |

---

## Next Steps

1. Do the lab: [Lab](../l02-lab/README.md)
2. Fill in [export-twin-checklist.md](resources/export-twin-checklist.md)
3. When ready, continue to [M05 — Scenario and Digital Validation](../../m05-digital-validation/l01-scenario-digital-validation/README.md)

---

## References and Further Reading

### Blender / glTF

1. [glTF 2.0 importer/exporter (4.5 LTS)](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html)
2. [glTF Animations](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#animations)
3. [glTF Materials](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#materials)
4. [Apply Scale](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/apply.html)
5. [Khronos glTF](https://www.khronos.org/gltf/)
6. [Blender Fundamentals — Importing & Exporting](https://studio.blender.org/training/blender-fundamentals-45-lts/blender_4-5_lts_importing-exporting/)

### Twin host and evidence

7. [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)
8. [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)
9. [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) — `web-app/ex05`, `ex06`
10. [TESAIoT Developer Hub](https://dev.tesaiot.dev/)
11. [Course 2 M03](../../../digital-twin/m03-virtual-device/l01-virtual-device-modeling/README.md) · [Course 2 M04](../../../digital-twin/m04-cosimulation/l01-firmware-twin-cosim/README.md) · [Course 3 TOC](../../README.md)

---

## Check your understanding

Three short questions in [quiz.yaml](quiz.yaml), one per objective of this lesson. Try answering them yourself first, then compare with the answer key and explanations in the file.

## Lab

Continue hands-on at [Lab: export GLB and import into the Twin](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Export checklist](resources/export-twin-checklist.md) · [← TOC](../../README.md) · [← M03](../../m03-motion/l01-motion-and-interaction/README.md) · [M05 →](../../m05-digital-validation/l01-scenario-digital-validation/README.md)
