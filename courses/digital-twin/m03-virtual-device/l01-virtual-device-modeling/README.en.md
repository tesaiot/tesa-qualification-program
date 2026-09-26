---
id: twin.m03.l01
lang: en
title:
  th: Virtual Device, behavior, event script และโมเดล 3D สำหรับ Twin
  en: Virtual Devices, Behaviours, Event Scripts and 3D Models for the Twin
summary:
  th: กำหนดโมเดลอุปกรณ์ เซ็นเซอร์ พฤติกรรม และสคริปต์เหตุการณ์ตามเวลา แล้วเตรียมโมเดล 3D ใน Blender ให้ส่งออกเป็น GLB สำหรับ Twin
  en: Define the device model, sensors, behaviours and timed event scripts, then prepare a Blender 3D model for export to GLB for the Twin.
level: L3
time_min:
  concept: 45
  practise: 20
  check: 10
hardware:
  emulator: true
  boards:
  - none
prerequisites:
- twin.m02.l02
objectives:
- th: กำหนด Virtual Device Model ที่มี identity เซ็นเซอร์อย่างน้อยสองชนิด (พร้อม unit, default, min/max) และเอาต์พุตที่สังเกตได้
  en: Define a Virtual Device Model with an identity, at least two sensors (unit, default, min/max) and an observable output.
- th: เขียน behavior แบบ WHEN/THEN ที่ทดสอบได้ทั้งขาเข้าและขาออก และไทม์ไลน์ event script ที่รันซ้ำได้
  en: Write a WHEN/THEN behaviour that is testable on input and output, and a repeatable event-script timeline.
- th: ระบุเงื่อนไขของโมเดล 3D ที่พร้อมใช้กับ Twin (สเกลจริง origin ชัด UV พร้อม) และขั้นตอนส่งออกเป็น glTF Binary (.glb)
  en: State what makes a 3D model Twin-ready (real scale, clear origin, UVs) and the steps to export glTF Binary (.glb).
develops:
- skill: iot.digital-twin
  to: 2
- skill: sys.simulation
  to: 2
- skill: test.sil-hil
  to: 1
- skill: hwdev.3d-modeling
  to: 1
context:
  platform: psoc-edge-e84
  host: bitstream-studio
  ide: vscode
  simulator: Bitstream Simulator (not the BENTO Emulator)
status: alpha
translation: done
source_sha256: 72371c12b154ca07b9bb576d160e425cc5124f912fbf88f443a943549f6249f4
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C2/M03/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M03 — Virtual Device Modeling

**Course 2 · Module 3**
**Suggested time:** about 4–5 hours (Virtual Device + behavior/script + a Blender for Twin 3D introduction)
**Format:** a hands-on lesson — designing a Virtual Device + Blender basics (Modeling / Texturing / Animation) for visualization on the Twin

[Lab](../l02-lab/README.md) · [Device checklist](resources/device-model-checklist.md) · [Blender cheatsheet](resources/blender-twin-cheatsheet.md) · [← Table of Contents](../../README.md) · [← M02](../../m02-vscode-twin/l01-vscode-for-twin/README.md) · [M04 →](../../m04-cosimulation/l01-firmware-twin-cosim/README.md)

> **Note:** the tables in this lesson reference scene buttons in TESAIoT_Hackathon's `ble-flet`, but [that repo's README](https://github.com/drsanti/TESAIoT_Hackathon/blob/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/README.md) (commit `f5f09a6`) states `ble-flet/` is not published. Use the panels in Bitstream Studio instead (checked on 2026-09-26)

---

## Objectives (Learning Outcomes)

By the end of this lesson you should be able to:

1. Build and configure a **Virtual Device Model** that reflects the course's target board
2. Simulate key sensors, such as **IMU, Temperature, Pressure, Switches**
3. Define **Behavior Simulation** so the input→state path is checkable
4. Write a repeatable **Event Simulation Script** for regression / demonstration
5. Explain **Blender**'s role in building a 3D model for the Twin: **Modeling, Texturing, Animation**, and the **export glTF/GLB** path
6. Use online documentation (the Blender Manual / Fundamentals / [the Thai-language tutorial](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY)) and [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free) to keep learning on your own

This module builds on [M02](../../m02-vscode-twin/l01-vscode-for-twin/README.md), where the host is already ready — now you will **design what the Twin simulates** (data + 3D shape), before bringing firmware into deeper co-sim in [M04](../../m04-cosimulation/l01-firmware-twin-cosim/README.md).

> **The approach: "model on paper + run on real tools + prepare 3D"**
> The Virtual Device Configuration describes *behaviour/sensors*.
> **Blender** prepares the *visual shell* the Twin / Sensor Studio displays — Course 3 goes deep into industrial design work; here we focus on enough skill for Course 2.

### Read alongside this chapter

| Document | Use when |
|---|---|
| [M01 — Twin Architecture](../../m01-twin-architecture/l01-twin-architecture/README.md) | Which layer of the platform the Virtual Device sits in |
| [M02 — VS Code Twin](../../m02-vscode-twin/l01-vscode-for-twin/README.md) | Opening the Simulator / Bitstream Studio before this lab |
| [Course 1 M05 — Sensor prep](../../../firmware-sdk-edge-ai/m05-sensor-data/l01-sensor-data-for-edge-ai/README.md) | Sensor types and what their values mean |
| **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)** | The host to see the result after setting up the model/scene |
| **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)** | `ble-flet` scene presets · `web-app/` |
| **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** | GLB models / textures / images for the Twin |
| **[Blender Manual 4.5 LTS](https://docs.blender.org/manual/en/4.5/)** | The official manual for Modeling / Materials / Animation |
| **[Blender Fundamentals 4.5 LTS](https://studio.blender.org/training/blender-fundamentals-45-lts/)** | An official video course from Blender Studio (English) |
| **[INC111-2021 Blender playlist (Thai)](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY)** | A Thai-language tutorial on YouTube — recommended for learners who want a Thai explanation |
| **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)** | Sensor examples on the firmware side |
| [A conceptual model example](resources/sample-virtual-device.template.json) | A JSON skeleton for your deliverable |
| [Blender cheatsheet](resources/blender-twin-cheatsheet.md) | Quick links for Modeling / Texturing / Animation / glTF |

---

## 1. What Is a Virtual Device Model

A **Virtual Device Model** is a software description of one device in the Twin world. At minimum, it should state:

| Part | Question it must answer |
|---|---|
| **Identity** | A fixed device name / id to reference in a report |
| **Sensors** | What exists · units · default value · the accepted range |
| **Actuators / outputs** | LEDs, flags, logs — things whose result can be observed |
| **Noise / dynamics (if any)** | Are values jumpy, or is simulated noise present? |
| **Behaviors** | When an input/command occurs, how does the state change? |
| **Events / scripts** | Timed scenarios that can be run again |

The model **does not need** to simulate every block in the silicon — it must **be enough to test the firmware's logic** per the lab's task.

| Too rough | More detail than needed |
|---|---|
| Tests don't reflect real behaviour | Wasted setup time that adds no learning |

> **Key phrase**
> A Virtual Device is an *agreement* between your test script and the Twin — not the whole datasheet.

### 1.1 Conceptual model document

Keep the model as a document the team can reread — an example skeleton in [sample-virtual-device.template.json](resources/sample-virtual-device.template.json):

```json
{
  "deviceId": "tesa-edge-demo-01",
  "displayName": "TESA Edge Demo Device",
  "sensors": [
    { "id": "temp", "type": "temperature", "unit": "C", "default": 25.0, "min": -10.0, "max": 85.0 },
    { "id": "btn_user", "type": "switch", "default": 0 },
    { "id": "imu", "type": "imu", "axes": ["ax", "ay", "az"], "default": [0, 0, 1] }
  ],
  "actuators": [
    { "id": "led_status", "type": "led", "default": 0 }
  ],
  "behaviors": [
    { "when": "command.led == on", "then": "actuators.led_status = 1" },
    { "when": "sensors.temp > 40", "then": "emit event threshold_exceeded" }
  ]
}
```

> This file is a **conceptual template for learning** — the real tool's fields may be named differently; map it to the Simulator / scene / SENSOR_CFG per the kit you use.

### 1.2 How the lab stack realizes the model

| Part of the model | What is usually used to run it for real, in this course |
|---|---|
| The sensor list + rates | **SENSOR_CFG** / **scene presets** (Motion, Lab Quiet, Environment, …) |
| Continuous IMU / env values | The **Bitstream Simulator** stream, or a real board |
| Identity | The device name / the MAC topic / `deviceId` in the report |
| Behavior (command → output) | A host command / an MQTT actuator / an LED on the board or UI |
| A timed event script | A timeline in the checklist + switching scenes / manually triggering / a script, depending on the tool you have |

---

## 2. Modeling Sensors

### 2.1 Sensor families in this course

| Type | Value usually simulated | Good for testing |
|---|---|---|
| **IMU** (such as BMI270) | accel / gyro (and fusion, depending on mode) | gesture, activity, orientation |
| **Temperature / Humidity** (such as SHT40) | A continuous scalar | threshold, a calibration path |
| **Pressure** (such as DPS368) | A continuous scalar | an environmental monitor |
| **Magnetometer** (such as BMM350) | Field axes | heading / fusion labs |
| **Switches / buttons** | 0/1 or an edge | UI logic, debounce |

Recommended learning order:

1. A switch + temperature (the result is easy to observe)
2. Add the IMU once the data pipe is ready
3. Combine env sensors into a monitor set

Review what the values mean: [Course 1 M05](../../../firmware-sdk-edge-ai/m05-sensor-data/l01-sensor-data-for-edge-ai/README.md)

### 2.2 Rates and scenes (practical knobs)

Instead of exposing every wire-level field right away, a lab host usually has **scene presets** at the use-case level:

| Scene (an example in the lab pack) | Approximate meaning |
|---|---|
| **Motion** | The IMU is denser · env is slower — suited to posture / motion |
| **Realtime** | A higher rate, for watching brief detail |
| **Lab Quiet** | ~1 Hz for everything — good for demos / saving resources |
| **Environment** | Emphasises SHT/DPS · the IMU is off or reduced |

In Bitstream / BLE labs, applying a scene usually means a **SENSOR_CFG** set (+ a BMI270 / fusion mode, depending on the tool) — learners should focus on *which profile the model needs*, not memorise every millisecond on day one.

### 2.3 Defaults, ranges, and honesty

When filling in a model, state:

| Field | Why it matters |
|---|---|
| `default` | The value when a script starts / before triggering |
| `min` / `max` | Prevents an unintentionally unrealistic test |
| The unit | Prevents confusing °C / Pa / g |
| "sim vs real" | A value from the Simulator is sine/synthetic — not real board noise |

---

## 3. Behavior Simulation

**Behavior** is the rule stating how the simulated device (or the firmware + host) responds once an input or command occurs.

### 3.1 Patterns worth practicing

| Pattern | Example | Observe the result at |
|---|---|---|
| **Command → actuator** | `led=on` → the status LED turns on | The UI / the board / a log |
| **Sensor → event** | `temp > 40` → `threshold_exceeded` | The event panel / MQTT / UART |
| **Switch → mode** | Press a button → the publish mode changes | The toolbar / the stream rate |
| **Host write → device** | A command from Studio/MQTT | The firmware responds |

Write a behaviour that is **testable on both input and output** — if there is only "the value moves" without an agreement on what should happen, you cannot measure whether the logic is correct.

### 3.2 Keep behaviors small

In M03, at least **1 path** written as a clear sentence is required, for example:

```text
WHEN user_button rising edge
THEN led_status = ON for 1 s AND log "btn"
```

Or:

```text
WHEN temperature > 40 °C for 2 s
THEN emit event "temp_high"
```

Expand the number of behaviors in M04/M06, once co-sim and E2E are ready.

---

## 4. Event Simulation Scripts

An **Event Simulation Script** builds a timed scenario, so regression and demonstration can be repeated.

### 4.1 Timeline example

```text
t = 0–2 s   : idle (defaults)
t = 2–5 s   : temperature ramp +0.5 °C / step
t = 5.0 s   : press virtual switch ~200 ms
t = 6.0 s   : short IMU shake pulse
t = 7–10 s  : observe outputs / events
t = 10 s    : stop or loop
```

### 4.2 How to "run" a script in the lab

Choose at least one method, per the tools you have:

| Method | Use when |
|---|---|
| **A manual timeline** | Follow the clock + notes — this passes M03's bar |
| **A scene switch** | Start Lab Quiet → switch to Motion at t=6 to trigger the IMU path |
| **Host / app controls** | A scene button in `ble-flet`, or a Studio panel |
| **A formal script file** | If that round's Twin tooling supports a script file — attach a relative path in the checklist |

What matters is **the sequence of events + the expected result + evidence**, not a specific scripting language.

### 4.3 Regression mindset

Keep the script/timeline in your lab folder:

```text
lab-notes/
  device-model.json      # from the template
  event-script-v1.md     # the timeline
  evidence/              # before/after screenshots
```

Once you edit the firmware in M04+, rerun the same script — if the result changes unintentionally, that's a regression signal.

---

## 5. Blender for Twin Visualization

The Virtual Device in the previous section describes **data and behaviour** — this section prepares a **3D visual stand-in** for the product/board, to display in the Digital Twin / Sensor Studio.

**[Blender](https://www.blender.org/)** is free, open-source 3D software that this course uses as the main path to **glTF / GLB** files, which the web host and Bitstream Studio support.

| Work layer in M03 | What you practise | The Twin destination |
|---|---|---|
| **Modeling** | Building the mesh shape of the case/board | A shape in the 3D scene |
| **Texturing** | UVs + a material / texture | A surface that looks realistic on the host |
| **Animation** | A brief keyframe / action | Showing an open-close mechanism, or a motion demo |
| **Export** | `.glb` | Loaded into Studio / compared against [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free) |

> **Course 2 vs Course 3**
> Here you get **enough foundation to use with the Twin**.
> The Product Industrial Design (Blender & Twin) course goes deep into casing, industrial workflow, validation and prototyping — don't wait for Course 3 if you just need a model to accompany telemetry in Course 2.

A quick-link sheet: [blender-twin-cheatsheet.md](resources/blender-twin-cheatsheet.md)

### 5.1 Getting Blender and the UI

1. Download from [blender.org/download](https://www.blender.org/download/)
2. Read the interface overview: [User Interface (Manual 4.5)](https://docs.blender.org/manual/en/4.5/interface/index.html)
3. The full manual: [Blender 4.5 LTS Manual](https://docs.blender.org/manual/en/4.5/), or [latest](https://docs.blender.org/manual/en/latest/)
4. An official video path (English): [Blender Fundamentals 4.5 LTS](https://studio.blender.org/training/blender-fundamentals-45-lts/)
5. A **Thai-language** video path: [INC111-2021 YouTube playlist](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY)

Modes you'll use often when building a device model:

| Mode | Use when | Read more |
|---|---|---|
| **Object Mode** | Moving/rotating/scaling a whole piece, combining objects | [Scenes & Objects](https://docs.blender.org/manual/en/4.5/scene_layout/object/index.html) |
| **Edit Mode** | Editing points, edges, faces (a mesh) | [Mesh introduction](https://docs.blender.org/manual/en/4.5/modeling/meshes/introduction.html) |
| **Shading workspace** | Arranging material / texture nodes | [Materials](https://docs.blender.org/manual/en/4.5/render/materials/introduction.html) |
| **Animation editors** | Timeline, Dope Sheet, Graph Editor | [Animation intro](https://docs.blender.org/manual/en/4.5/animation/introduction.html) |

### 5.2 Modeling (building the shape)

Modeling in Blender usually starts from a **mesh primitive** (cube, cylinder, plane…) and then enters **Edit Mode** to shape it — per [Mesh Modeling introduction](https://docs.blender.org/manual/en/4.5/modeling/meshes/introduction.html)

#### Main skills worth knowing in Course 2

| Skill | Why it matters for the Twin | Documentation |
|---|---|---|
| Select / Extrude | Building the case's walls, thick edges | [Extrude](https://docs.blender.org/manual/en/4.5/modeling/meshes/editing/mesh/extrude.html) |
| Loop Cut / Bevel | Rounded edges, splitting a face for UVs | [Loop Cut](https://docs.blender.org/manual/en/4.5/modeling/meshes/tools/loop.html) · [Bevel](https://docs.blender.org/manual/en/4.5/modeling/meshes/editing/edge/bevel.html) |
| Modifiers (Mirror, Solidify, Subdivision) | Building symmetry/thickness without redoing it by hand | [Modifiers](https://docs.blender.org/manual/en/4.5/modeling/modifiers/introduction.html) |
| Apply Scale / origin | Preventing the model from distorting when put into the Twin or animated | [Transforms](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/transform/index.html) |

A video workshop: [Fundamentals — Modeling chapter](https://studio.blender.org/training/blender-fundamentals-45-lts/chapter/blender_4_5_lts_modeling/)

#### An approach for an Edge / DevKit device model

1. Set the units to **metres** (or at least keep a consistent scale across the whole scene)
2. Place the **origin** at a meaningful point (a corner of the board, the lid's hinge axis, the point that sits on a desk)
3. Separate parts that may move (a lid, buttons, LEDs) into their own objects if you'll animate them
4. Control the polygon count — the Twin's webview doesn't need film-level density
5. Compare the style with the models in [ternion-3d-assets-free `/assets/models`](https://github.com/drsanti/ternion-3d-assets-free/tree/main/assets/models)

> **Key phrase**
> Good modeling for the Twin = *readable shape + real scale + a clear origin + UVs ready* — not detail for an advertising render.

Further study (Modeling):

- [Modeling section index (4.5)](https://docs.blender.org/manual/en/4.5/modeling/index.html)
- [Edit Mode mesh tools](https://docs.blender.org/manual/en/4.5/modeling/meshes/editing/index.html)
- [Geometry Nodes](https://docs.blender.org/manual/en/4.5/modeling/geometry_nodes/index.html) (advanced — not required for M03)

### 5.3 Texturing (materials and surfaces)

Texturing, in the Twin context, means giving the model's surface a colour / gloss / pattern that **can be exported to glTF**.

#### Main concepts

| Concept | Short meaning | Documentation |
|---|---|---|
| **Material** | A description of the surface on an object | [Materials introduction](https://docs.blender.org/manual/en/4.5/render/materials/introduction.html) |
| **Principled BSDF** | The standard PBR node that glTF understands well | [Principled BSDF](https://docs.blender.org/manual/en/4.5/render/shader_nodes/shader/principled.html) |
| **UV map** | 2D unwrap coordinates onto a texture | [UV editing](https://docs.blender.org/manual/en/4.5/editors/uv/index.html) · [Unwrapping](https://docs.blender.org/manual/en/4.5/modeling/meshes/uv/unwrapping/index.html) |
| **Image texture** | An image file (albedo / roughness / …) | [Image Texture node](https://docs.blender.org/manual/en/4.5/render/shader_nodes/textures/image.html) |
| **Texture Paint** | Painting a pattern directly on the model | [Texture Paint](https://docs.blender.org/manual/en/4.5/sculpt_paint/texture_paint/index.html) |

#### Recommended workflow for Course 2

```text
Mesh ready
  → Unwrap UV (Smart UV Project or by hand)
  → Principled BSDF
  → Base Color (± Roughness / Metallic maps)
  → Check in Material Preview / EEVEE
  → Export GLB (materials + UVs on)
```

Per the [glTF 2.0 exporter](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html):

- The material that exports best is **Metal/Rough PBR** from Principled BSDF
- Control the UV by connecting a **UV Map** (+ Mapping) into the Image Texture
- Unlit/shadeless has its own path in the exporter's manual, if you need a flat surface

Ready-to-use texture / cubemap sources in the Ternion system:

- Browse: [assets/textures](https://github.com/drsanti/ternion-3d-assets-free/tree/main/assets/textures)
- Sync in Studio: **Download Free Assets from GitHub** (see [M02 §2.6](../../m02-vscode-twin/l01-vscode-for-twin/README.md))

Further study (Texturing / shading):

- [Shader Nodes](https://docs.blender.org/manual/en/4.5/render/shader_nodes/index.html)
- [EEVEE](https://docs.blender.org/manual/en/4.5/render/eevee/index.html) / [Cycles](https://docs.blender.org/manual/en/4.5/render/cycles/index.html) (rendering in Blender — the Twin mainly uses the exported file)
- [glTF materials section](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#materials)

### 5.4 Animation (motion)

Animation helps demonstrate **product behaviour** on the Twin, such as opening a lid, pressing a button, rotating an arm — matching the behavior/event script on the data side.

#### Main concepts

| Concept | Short meaning | Documentation |
|---|---|---|
| **Keyframe** | A point in time where a transform/property value is recorded | [Keyframes](https://docs.blender.org/manual/en/4.5/animation/keyframes/index.html) |
| **Action** | A set of keyframes for an object | [Actions](https://docs.blender.org/manual/en/4.5/animation/actions.html) |
| **Armature / bones** | A skeleton for complex parts | [Armatures](https://docs.blender.org/manual/en/4.5/animation/armatures/index.html) |
| **Shape keys** | Morphing a shape (a soft lid, rubber) | [Shape Keys](https://docs.blender.org/manual/en/4.5/animation/shape_keys/index.html) |
| **Constraints** | Restricting motion by a rule | [Constraints](https://docs.blender.org/manual/en/4.5/animation/constraints/introduction.html) |

Overview: [Animation & Rigging introduction](https://docs.blender.org/manual/en/4.5/animation/introduction.html)

#### What usually makes it to the Twin (through glTF)

Per the [glTF 2.0](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html) manual:

| Generally supported | Often doesn't make it / gets overlooked |
|---|---|
| Keyframes of location / rotation / scale | Some light / material animation |
| Skinning (armature) | A complex driver that wasn't baked |
| Shape key animation | Blender-specific logic that isn't exported |

Tips for exporting animation:

1. Make the action **active**, or arrange the NLA per what the exporter requires
2. Test playing it back in Blender before exporting
3. Turn on the Animation option in the glTF export window
4. Check in Bitstream Studio / a viewer that the clip plays

> **Connecting to the Virtual Device**
> The timeline in §4 (the event script) = *a data event*
> The timeline in Blender = *a visual event*
> In the Capstone (M06), try to make these two tell the same story.

Further study (Animation):

- [Animation editors](https://docs.blender.org/manual/en/4.5/editors/dope_sheet/index.html)
- [NLA Editor](https://docs.blender.org/manual/en/4.5/editors/nla/index.html)
- [glTF Animations](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#animations)

### 5.5 Export to Twin — glTF / GLB

The recommended format for Bitstream Studio / the web Twin: **glTF Binary (`.glb`)**, a single file combining mesh + materials + (if any) animation

| Step | Action | Reference |
|---|---|---|
| 1 | Apply necessary transforms, check the origin | The transforms manual |
| 2 | UV + Principled ready | §5.3 |
| 3 | Animation ready (if any) | §5.4 |
| 4 | **File → Export → glTF 2.0** | [glTF 2.0 add-on (4.5)](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html) |
| 5 | Choose **glTF Binary (.glb)** · turn on Meshes / Materials / (Animations) | The export window |
| 6 | Load it into Bitstream Studio, or compare it against the [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free) pack | M02's Free Loader |

The industry standard: [Khronos glTF](https://www.khronos.org/gltf/)

Other formats (FBX/OBJ/STL) have their place for prototyping/3D printing — Course 3 goes deeper into that; in Course 2, focus on **GLB for the Twin**.

### 5.6 Suggested self-study path (Blender)

If you want to practise more on your own (~2–4 extra hours):

**A Thai-language option (recommended if you want a Thai narration):** watch the [INC111-2021 playlist](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY) together with the exercise in Lab E — use the English Manual when you need the latest tool detail.

**An official option (English):**

1. [Fundamentals 4.5 — start](https://studio.blender.org/training/blender-fundamentals-45-lts/)
2. Do the [Modeling](https://studio.blender.org/training/blender-fundamentals-45-lts/chapter/blender_4_5_lts_modeling/) chapter until you have a simple part
3. Read [Principled BSDF](https://docs.blender.org/manual/en/4.5/render/shader_nodes/shader/principled.html) + unwrap one piece
4. Add a keyframe rotating/opening a lid for 2–3 seconds
5. Export the `.glb` and try it in Studio
6. Compare the quality against the models in [assets/models](https://github.com/drsanti/ternion-3d-assets-free/tree/main/assets/models)

> Blender's UI changes by version — if a Thai clip uses an older version, treat the buttons/menus from the [Manual 4.5+](https://docs.blender.org/manual/en/4.5/) as authoritative, and use the clip as a workflow concept.

---

## 6. Design Checklist Before You Build

Before starting the lab, be able to answer:

1. Which **logic** of the firmware/product does this device test?
2. What are the minimum sensors needed (at least 2 types)?
3. Where do you observe the one behaviour path, on which screen?
4. How long does the event script take, and who on the team can rerun it?
5. (Recommended) will you use a 3D model from Blender, or from [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)?

A form to fill in: [device-model-checklist.md](resources/device-model-checklist.md) · [blender-twin-cheatsheet.md](resources/blender-twin-cheatsheet.md)

---

## Next Steps

1. Do the Virtual Device lab: [Lab](../l02-lab/README.md)
2. Fill in the checklist + attach the model/timeline
3. (Recommended) the Blender lab — export one GLB
4. When ready, continue to **M04 — Firmware–Twin Co-simulation**

---

## References and Further Reading

### Course / host

1. [M01 Twin Architecture](../../m01-twin-architecture/l01-twin-architecture/README.md) · [M02 VS Code Twin](../../m02-vscode-twin/l01-vscode-for-twin/README.md)
2. [Course 1 M05 Sensors](../../../firmware-sdk-edge-ai/m05-sensor-data/l01-sensor-data-for-edge-ai/README.md)
3. **[Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)**
4. **[TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)**
5. **[TESAIoT Developer Hub](https://dev.tesaiot.dev/)**
6. **[ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)** — [`assets/`](https://github.com/drsanti/ternion-3d-assets-free/tree/main/assets)
7. [sample-virtual-device.template.json](resources/sample-virtual-device.template.json)
8. [blender-twin-cheatsheet.md](resources/blender-twin-cheatsheet.md)

### Blender — official manuals & training

9. [Blender download](https://www.blender.org/download/)
10. [Blender Manual 4.5 LTS](https://docs.blender.org/manual/en/4.5/) · [Manual (latest)](https://docs.blender.org/manual/en/latest/)
11. [Modeling — meshes introduction](https://docs.blender.org/manual/en/4.5/modeling/meshes/introduction.html)
12. [Modeling section](https://docs.blender.org/manual/en/4.5/modeling/index.html)
13. [Materials introduction](https://docs.blender.org/manual/en/4.5/render/materials/introduction.html)
14. [Principled BSDF](https://docs.blender.org/manual/en/4.5/render/shader_nodes/shader/principled.html)
15. [UV editing](https://docs.blender.org/manual/en/4.5/editors/uv/index.html) · [UV unwrapping](https://docs.blender.org/manual/en/4.5/modeling/meshes/uv/unwrapping/index.html)
16. [Texture Paint](https://docs.blender.org/manual/en/4.5/sculpt_paint/texture_paint/index.html)
17. [Animation introduction](https://docs.blender.org/manual/en/4.5/animation/introduction.html)
18. [Keyframes](https://docs.blender.org/manual/en/4.5/animation/keyframes/index.html) · [Actions](https://docs.blender.org/manual/en/4.5/animation/actions.html)
19. [Armatures](https://docs.blender.org/manual/en/4.5/animation/armatures/index.html) · [Shape Keys](https://docs.blender.org/manual/en/4.5/animation/shape_keys/index.html)
20. [glTF 2.0 importer/exporter (4.5)](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html)
21. [Blender Fundamentals 4.5 LTS](https://studio.blender.org/training/blender-fundamentals-45-lts/)
22. [Fundamentals — Modeling chapter](https://studio.blender.org/training/blender-fundamentals-45-lts/chapter/blender_4_5_lts_modeling/)
23. **[INC111-2021 Blender tutorial playlist (Thai)](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY)**
24. [Khronos glTF](https://www.khronos.org/gltf/)

---

## Check your understanding

Three short questions in [quiz.yaml](quiz.yaml), one per objective of this lesson. Try answering them yourself first, then compare with the answer key and explanations in the file.

## Lab

Continue hands-on at [Lab: building a Virtual Device and an event script](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Device checklist](resources/device-model-checklist.md) · [Blender cheatsheet](resources/blender-twin-cheatsheet.md) · [← Table of Contents](../../README.md) · [← M02](../../m02-vscode-twin/l01-vscode-for-twin/README.md) · [M04 →](../../m04-cosimulation/l01-firmware-twin-cosim/README.md)
