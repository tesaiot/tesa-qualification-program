---
id: pdesign.m03.l02
lang: en
title:
  th: 'แล็บ: แอนิเมชันฝาและลำดับการเคลื่อนไหวสั้น'
  en: 'Lab: Lid Animation and Short Sequences'
summary:
  th: ตั้งบานพับ keyframe คลิป `lid_open` สร้างคลิปปิด ตรวจการชน และบันทึกรายการคลิป
  en: Set the hinge, keyframe a `lid_open` clip, add a close clip, check interference and log the clip list.
level: L2
time_min:
  lab: 180
hardware:
  emulator: false
  boards:
  - none
prerequisites:
- pdesign.m03.l01
objectives:
- th: สร้างคลิปเปิด/ปิดที่ตั้งชื่อแล้ว และบันทึกใน animation-clip-list.md
  en: Create named open/close clips and record them in animation-clip-list.md.
- th: บันทึกผลตรวจการชนพร้อมหลักฐานภาพหรือคลิปสั้น
  en: Record the interference check with an image or short clip as evidence.
develops:
- skill: hwdev.3d-modeling
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
source_sha256: e7eb716fbccfcdd1cfbdd2b5eca4f0025b3701e85232e59b59332d3a6469e660
source:
  repo: https://github.com/drsanti/TESAIoT-Courses
  path: C3/M03/lab.md
  ref: 287c21814ba8c75f693136616dcd270349a15966
---

# Lab M03 — Lid Animation and Short Sequences

**Course 3 · Module 3**
**Type:** Hands-on (pivot · keyframes · named clips · collision check)
**Suggested time:** ~2.5–3 hours

Read first: [Lesson](../l01-motion-and-interaction/README.md) · [Clip list](../l01-motion-and-interaction/resources/animation-clip-list.md) · [← TOC](../../README.md) · [← M02](../../m02-modeling-render/l01-modeling-materials-render/README.md) · [M04 →](../../m04-blender-to-twin/l01-blender-to-twin/README.md)

### Keep these tabs open

| Document | Why |
|---|---|
| [Editing Keyframes](https://docs.blender.org/manual/en/4.5/animation/keyframes/editing.html) | `I` to insert keys |
| [Timeline](https://docs.blender.org/manual/en/4.5/editors/timeline.html) | playhead / Auto Key |
| [Actions](https://docs.blender.org/manual/en/4.5/animation/actions.html) | name clips |
| [Set Origin](https://docs.blender.org/manual/en/4.5/scene_layout/object/origin.html) | hinge pivot |
| [glTF Animations](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html#animations) | naming for M04 |

---

## Lab Goals

- Set the lid's Origin at the hinge
- Build at least 1 open/close animation set
- Check that parts do not severely intersect during playback
- Name the Action/clip with a short English name, such as `lid_open`
- Fill in [animation-clip-list.md](../l01-motion-and-interaction/resources/animation-clip-list.md)

---

## Prerequisites

- [ ] Have the M02 file with `Enclosure_lid` / `Enclosure_base` already split
- [ ] Copy it to `m03_enclosure_motion.blend` before editing

If the lid–base is not split yet, go back and do Lab C in the [M02 lab](../../m02-modeling-render/l02-lab/README.md) first.

---

## Lab A — Hinge origin (required)

1. Select `Enclosure_lid`
2. Place the 3D Cursor at the hinge edge (Edit Mode → `Shift+S` → Cursor to Selected)
3. Object Mode → Origin to 3D Cursor
4. `Ctrl+A` → Rotation & Scale
5. Test-rotate with `R` on the correct axis — it must open like a hinge

**Pass when:** a teammate rotates the lid and understands where the hinge is without a long explanation

---

## Lab B — Keyframe `lid_open` (required)

1. Set the team's fps (24 recommended) and a frame range of about 1–3 seconds
2. Start frame: lid closed → `I` → Rotation
3. End frame: rotated open → `I` → Rotation
4. Play in the Timeline and check the motion
5. Name the Action `lid_open` (or an equivalent meaningful name)

**Pass when:** pressing Play clearly shows the lid opening from closed to open

---

## Lab C — Close clip or return motion (required)

Choose one:

- **C1:** A separately named Action, `lid_close`
- **C2:** A frame range continuing from open, returning to the closed pose, in the same clip (note this clearly in the clip list)

**Pass when:** both an open and a closed state exist and can be played back repeatedly

---

## Lab D — Interference check (required)

1. Play the animation slowly (scrub the playhead, or slow down playback)
2. Switch to Wireframe and check the hinge point and the tall components
3. Note in the clip list: pass / minor collision / shape needs fixing
4. If there is a severe collision: fix the Origin, the opening angle, or go back to M02

**Pass when:** there is no severe intersection, or the issue is recorded with a plan to fix it

---

## Lab E — Evidence + clip list (required)

1. Fill in [animation-clip-list.md](../l01-motion-and-interaction/resources/animation-clip-list.md) for every clip
2. Record evidence: screenshots of the closed+open frames, or a short viewport playblast
3. Save the `.blend`

---

## Lab F — Optional extras

- A `battery_reveal` clip (moving the object standing in for the battery)
- Use the Graph Editor to smooth the easing
- Parent a small part to the lid ([Parenting](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/parent.html))

---

## Deliverables checklist

- [ ] `m03_enclosure_motion.blend`
- [ ] Named open/close motion
- [ ] Interference check recorded
- [ ] [animation-clip-list.md](../l01-motion-and-interaction/resources/animation-clip-list.md) filled in completely
- [ ] Image or short clip evidence

---

## Troubleshooting

| Symptom | What to try |
|---|---|
| The lid rotates and floats as a whole block | The Origin is not yet at the hinge — redo Lab A |
| It rotates on the wrong axis | Use `R` then `X` / `Y` / `Z` · or rotate one axis at a time in the Transform panel |
| Pressing `I` shows no key | Check the Timeline · turn off Only Show Selected if needed · confirm the right object is selected |
| Auto Key creates messy keys | Turn off the record button in the Timeline, then delete extra keys in the Dope Sheet |
| The Action's name disappears after saving | Check the Action panel · don't delete the Action by accident |
| Collision at the hinge | Nudge the Origin slightly · or add spacing between lid and base in the model |

[Lesson](../l01-motion-and-interaction/README.md) · [Clip list](../l01-motion-and-interaction/resources/animation-clip-list.md) · [TOC](../../README.md) · [M04 →](../../m04-blender-to-twin/l01-blender-to-twin/README.md)
