# Device model checklist — Course 2 M03

**Course 2 · Module 3**

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [Template](sample-virtual-device.template.json) · [TOC](../../../README.md)

---

## Identity

| Item | Your value |
|---|---|
| Device id | |
| Display name | |
| Physical board target (kit name) | |
| Lab path | Simulator / Board / Both |

---

## Sensors enabled (≥ 2)

| Sensor id | Type | Unit | Default | Min | Max | Notes |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |
| | | | | | | |

Scene / profile used on host (e.g. Lab Quiet, Motion):  

---

## Actuators / observe points

| Id | Type | How you observe it |
|---|---|---|
| | | |

---

## Behaviors (≥ 1)

| # | WHEN | THEN | Evidence |
|---|---|---|---|
| 1 | | | |
| 2 (optional) | | | |

---

## Event script timeline

| t (s) | Action | Expected observation |
|---|---|---|
| 0 | | |
| | | |
| | | |
| | | |

Script filename / note location:  
Evidence filename(s):  
Second run OK? Yes / No  

---

## Blender / 3D (recommended)

| Item | Your value |
|---|---|
| Blender version | |
| Track done | Modeling / Texturing / Animation / Export |
| `.glb` filename | |
| Loaded in Bitstream Studio? | Yes / No |
| Compared to ternion-3d-assets-free? | Yes / No |
| Docs you used (URLs) | |

Cheatsheet: [blender-twin-cheatsheet.md](blender-twin-cheatsheet.md)

---

## Quick recall

```text
Model (sensors + actuators)
  → Behavior (WHEN/THEN)
  → Timed script (repeatable)
  → Evidence on Studio / dashboard
  → (optional) Blender GLB for Twin 3D
```

| Too coarse | Too fine |
|---|---|
| Tests don't match product logic | Config cost > learning value |

---

## Portals

- [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio)  
- [Hackathon](https://github.com/drsanti/TESAIoT_Hackathon)  
- [Developer Hub](https://dev.tesaiot.dev/)  
- [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)  

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [M04](../../../m04-cosimulation/l01-firmware-twin-cosim/README.md)
