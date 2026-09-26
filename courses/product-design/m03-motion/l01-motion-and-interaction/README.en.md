---
id: pdesign.m03.l01
lang: en
title:
  th: แอนิเมชันเปิด–ปิดและการตรวจการชน
  en: Open/Close Animation and Interference Checks
summary:
  th: เตรียม pivot ของฝา keyframe เปิด–ปิด ตั้งชื่อ Action ตรวจการชนขณะเล่น และเตรียมคลิปสำหรับ Twin
  en: Prepare the lid pivot, keyframe open and close, name the Action, check interference during playback and prepare clips for the Twin.
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
- pdesign.m02.l02
objectives:
- th: ตั้ง origin ของฝาที่บานพับ และ Apply Rotation/Scale ก่อนใส่ keyframe
  en: Place the lid origin at the hinge and apply rotation/scale before keyframing.
- th: สร้างคลิปเปิด–ปิด และตั้งชื่อ Action เป็นภาษาอังกฤษสั้นที่อ้างถึงได้ เช่น `lid_open`
  en: Create open/close clips and give each Action a short English name such as `lid_open`.
- th: ตรวจการชนขณะเล่นแอนิเมชัน และเลือกวิธีแก้ (เลื่อนบานพับ ลดมุมเปิด หรือแก้รูปทรง)
  en: Check for interference during playback and choose a fix (move the hinge, reduce the angle or change the shape).
develops:
- skill: hwdev.3d-modeling
  to: 2
- skill: hwdev.enclosure
  to: 2
context:
  tool: blender-4.5
  twin-host: bitstream-studio
  output: glb, stl
status: alpha
translation: done
slides: slides.md
source_sha256: 1b4f5c8b9116c9783a025492cdc05755c9b126710347e4f1830c35be3c22ac74
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C3/M03/README.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# M03 — Motion and Interaction

**Course 3 · Module 3**
**Suggested time:** about 3 hours — build open–close animation for the parts, check for collisions, and name clips ready for the Twin
**Format:** a hands-on lesson — read it and follow along directly in Blender; exporting GLB to the Twin is in [M04](../../m04-blender-to-twin/l01-blender-to-twin/README.md)

[Lab](../l02-lab/README.md) · [Clip list](resources/animation-clip-list.md) · [← Table of Contents](../../README.md) · [← M02](../../m02-modeling-render/l01-modeling-materials-render/README.md) · [M04 →](../../m04-blender-to-twin/l01-blender-to-twin/README.md)

---

## Objectives (Learning Outcomes)

By the end of this lesson you should be able to:

1. Build animation to open–close a part, or to reveal the internal structure
2. Simulate motion to assess usability (no parts pass through each other)
3. Build a set of motion sequences (**named clips / actions**) for the Twin or teaching material

> **Key phrase**
> Animation in M03 is a **mechanism-checking tool**, not just something to make it look nice — if the lid opens and clips through the base, the design is not yet ready to print.

### How this differs from Course 2 M03

| Course | M03 focus |
|---|---|
| [Course 2 M03](../../../digital-twin/m03-virtual-device/l01-virtual-device-modeling/README.md) | Virtual Device · sensor script · event simulation |
| **Course 3 M03 (this module)** | **Animating the product in Blender** (opening the lid / rotating a part / short clips) |

### Read alongside this chapter

| Document | Use when |
|---|---|
| [M02 — Modeling, Materials, Render](../../m02-modeling-render/l01-modeling-materials-render/README.md) | You need `Enclosure_lid` / `Enclosure_base` already split |
| **[Insert / edit keyframes](https://docs.blender.org/manual/en/4.5/animation/keyframes/editing.html)** | Press `I` to insert a keyframe |
| **[Timeline](https://docs.blender.org/manual/en/4.5/editors/timeline.html)** | Play / scrub frames / Auto Key |
| **[Actions](https://docs.blender.org/manual/en/4.5/animation/actions.html)** | Storing animation as a named Action |
| **[Dope Sheet](https://docs.blender.org/manual/en/4.5/editors/dope_sheet/index.html)** | Organising keyframes for the whole clip |
| **[Graph Editor](https://docs.blender.org/manual/en/4.5/editors/graph_editor/index.html)** | Smoothing the motion (optional) |
| **[Set Origin](https://docs.blender.org/manual/en/4.5/scene_layout/object/origin.html)** | The lid's pivot point (the hinge) |
| **[Parenting](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/parent.html)** | (Optional) attaching a part to the lid |
| **[glTF Animations](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#animations)** | Preparing clip names for export in M04 |
| **[Blender Fundamentals — Animation](https://studio.blender.org/training/blender-fundamentals-45-lts/)** | Official video (choose the Animation chapter) |
| **[INC111-2021 (Thai)](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY)** | Thai-language tutorial |
| [Clip list worksheet](resources/animation-clip-list.md) | Recording clip names, length, and rotation axis |

---

## 1. Why Animate the Product?

Animation in enclosure work answers questions a still image cannot fully answer:

| Question | What motion shows |
|---|---|
| Does opening the lid collide with a hand or a cable? | The lid's rotation path |
| Does the internal space fit the PCB / battery? | Opening the lid reveals the empty space |
| How does the user understand the way to open it? | A short clip for teaching material |
| What states can the Twin play? | The clip's name, such as `lid_open` |

At this early stage of the course, **mainly use Location / Rotation keyframes**.
Save an Armature (bones) for when the mechanism is genuinely complex — for most cases, a lid box rotating around its back edge is enough.

---

## 2. Prepare the Lid Pivot (Do This Before Keyframes)

From M02, you should already have separate objects, such as `Enclosure_lid` and `Enclosure_base`.

### 2.1 Place the origin at the hinge

The lid's Origin point = the pivot point ([Set Origin](https://docs.blender.org/manual/en/4.5/scene_layout/object/origin.html))

Recommended steps:

1. Select `Enclosure_lid`
2. Enter Edit Mode · select the edge or point you want as the hinge (usually the inner back edge)
3. `Shift+S` → Cursor to Selected
4. Object Mode → `Object → Set Origin → Origin to 3D Cursor`
5. Move the Cursor back to the World Origin if you want (`Shift+S` → Cursor to World Origin)

Test it: press `R` and rotate around the correct axis (usually **X** or **Y**, depending on how the model is oriented) — the lid should open like a hinge, not float away as a whole block.

### 2.2 Apply Rotation and Scale

Before inserting keyframes:

- `Ctrl+A` → **Rotation & Scale** on the lid (and the base if needed)
- Read [Apply](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/apply.html)

If Rotation in the Item panel is not zero even though the lid looks straight, it can be confusing when setting keys — Apply makes the starting values easy to read.

---

## 3. Keyframe Workflow — Lid Open / Close

Reference the official examples in [Editing Keyframes](https://docs.blender.org/manual/en/4.5/animation/keyframes/editing.html) and control timing with the [Timeline](https://docs.blender.org/manual/en/4.5/editors/timeline.html)

### 3.1 Set frame rate and range

| Setting | Lab default | Where |
|---|---|---|
| Frame rate | **24 fps** or 30 fps (same across the team) | Output Properties |
| Clip length | **1–3 seconds** per clip | e.g. 24–72 frames at 24 fps |
| Scene End | Long enough to play the clip | Timeline Start/End |

Example: a `lid_open` clip at 24 fps, 1.5 seconds long ≈ frame 1 → 36

### 3.2 Insert keys (closed → open)

1. Go to frame **1** (lid closed)
2. Select `Enclosure_lid`
3. Press `I` → choose **Rotation** (or LocRot if it needs to move too)
4. Go to the clip's end frame (e.g. **36**)
5. Rotate the lid open to the real working angle (e.g. 90° or 110°)
6. Press `I` → **Rotation** again
7. Press **Space** (or the Play button in the Timeline) to play it back

If you want Blender to insert keys automatically while you rotate: turn on **Auto Key** in the Timeline ([Timeline](https://docs.blender.org/manual/en/4.5/editors/timeline.html)) — remember that once it is on, every movement gets a key.

### 3.3 Optional second clip — close

Build a separate close clip, or continue into the next frame range:

- Frame 36 = open
- Frame 72 = closed (copy the rotation value from frame 1)

For the Twin, it is usually clearer to name these separately: `lid_open` and `lid_close`.

### 3.4 Name the Action

Animation in Blender is stored in an **Action** ([Actions](https://docs.blender.org/manual/en/4.5/animation/actions.html))

1. Open the Dope Sheet → **Action** mode (or the Action panel in the Animation workspace)
2. Give the Action a short English name, such as `lid_open`
3. Avoid empty names / duplicate names / Thai names in clip files that will be sent to the Twin

Good names:

| Good name | Avoid |
|---|---|
| `lid_open` | `Anim1`, `asdf`, `open_lid_th` |
| `lid_close` | `final_final2` |
| `battery_reveal` | Long names full of spaces |

Record every clip in [animation-clip-list.md](resources/animation-clip-list.md)

---

## 4. Collision / Interference Check While Playing

Play the animation slowly and check:

| Check | Pass means |
|---|---|
| Lid vs base | No severe intersection right at the hinge |
| Lid vs tall components | No collision with the USB head / sensors / display |
| Cable / finger space (concept) | There is room to imagine a hand opening it |
| Extreme angle | The open angle does not exceed what the real mechanism can do |

If there is a collision:

1. Move the hinge (the Origin)
2. Reduce the opening angle
3. Or go back and fix the shape in M02 (wall clearance / component height)

> **Key phrase**
> Motion that collides = a **design bug**, caught more cheaply here than after it's printed.

You do not need to turn on Physics simulation in M03 — visual inspection + Wireframe is enough for the lab.

---

## 5. Useful Product Motions (Pick What Fits)

| Motion idea | Typical keys | Twin / teaching use |
|---|---|---|
| Lid open–close | Rotation on the hinge | The core of this lab |
| Revealing the PCB inside | Lid open + a held camera | Teaching material on the structure |
| Removing the battery (concept) | Location of `Battery_block` | Showing a service compartment |
| LED state / a rotating part | A slight Rotation, or Emission (from M02) | Demonstrating an operating state |

Choose at least **one open/close set** to meet the criteria — the rest is extra work.

---

## 6. Sequences for Twin and Teaching Media

### 6.1 Keep clips short and purposeful

| Guideline | Why |
|---|---|
| 1–3 seconds per clip | Easy to manage · light to export · viewers understand one point |
| One clip = one intention | `lid_open` does not mix in a long camera rotation |
| Consistent names across the team | M04 / Bitstream Studio references the same names |

### 6.2 Prepare for glTF export (preview of M04)

Per [glTF Animations](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#animations):

- What exports well is **keyframed transforms** (and, in some cases, shape keys)
- If there are several Actions to export, they usually need to be **Stashed** into the NLA, depending on the export mode
- Track / action names affect the clip names inside the GLB file

In M03, just make sure playback in Blender is correct and every clip is fully named — the export button details are in M04.

### 6.3 Optional playblast for evidence

Record a short piece of evidence without a full render:

- Viewport → View → Viewport Render Animation (menu name varies by version)
- Or screen-record while pressing Play

Attach the file or a sequence of screenshots together with the clip list.

---

## 7. Quality Gate Before M04

| Check | Pass means |
|---|---|
| Lid origin at hinge | Rotating it behaves like a hinge |
| At least one open/close motion | Plays back in the Timeline |
| No severe mesh intersection | Checked during playback |
| Named action/clip | e.g. `lid_open` |
| Clip list filled | [animation-clip-list.md](resources/animation-clip-list.md) |
| Scale from M01–M02 unchanged | The PCB still fits |

---

## Next Steps

1. Do the lab: [Lab](../l02-lab/README.md)
2. Fill in [animation-clip-list.md](resources/animation-clip-list.md)
3. When ready, continue to [M04 — Blender to Twin Integration](../../m04-blender-to-twin/l01-blender-to-twin/README.md)

---

## References and Further Reading

### Blender animation (official)

1. [Editing Keyframes (4.5 LTS)](https://docs.blender.org/manual/en/4.5/animation/keyframes/editing.html)
2. [Timeline](https://docs.blender.org/manual/en/4.5/editors/timeline.html)
3. [Actions](https://docs.blender.org/manual/en/4.5/animation/actions.html)
4. [Dope Sheet](https://docs.blender.org/manual/en/4.5/editors/dope_sheet/index.html)
5. [Graph Editor](https://docs.blender.org/manual/en/4.5/editors/graph_editor/index.html)
6. [Set Origin](https://docs.blender.org/manual/en/4.5/scene_layout/object/origin.html)
7. [Parenting](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/parent.html)
8. [glTF 2.0 — Animations](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#animations)
9. [Blender Fundamentals 4.5 LTS](https://studio.blender.org/training/blender-fundamentals-45-lts/)
10. [INC111-2021 Blender (Thai)](https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY)

### Course links

11. [M02](../../m02-modeling-render/l01-modeling-materials-render/README.md) · [M04](../../m04-blender-to-twin/l01-blender-to-twin/README.md) · [Course 3 TOC](../../README.md)
12. [Course 2 M03](../../../digital-twin/m03-virtual-device/l01-virtual-device-modeling/README.md) (Virtual Device — a different focus)

---

## Check your understanding

Three short questions in [quiz.yaml](quiz.yaml), one per objective of this lesson. Try answering them yourself first, then compare with the answer key and explanations in the file.

## Lab

Continue hands-on at [Lab: lid animation and a short motion sequence](../l02-lab/README.md)

[Lab](../l02-lab/README.md) · [Clip list](resources/animation-clip-list.md) · [← TOC](../../README.md) · [← M02](../../m02-modeling-render/l01-modeling-materials-render/README.md) · [M04 →](../../m04-blender-to-twin/l01-blender-to-twin/README.md)
