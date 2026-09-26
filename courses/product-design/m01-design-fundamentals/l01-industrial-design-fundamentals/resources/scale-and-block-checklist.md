# Scale and block checklist — Course 3 M01

**Course 3 · Module 1**

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [TOC](../../../README.md)

---

## Setup

| Item | Your value |
|---|---|
| Blender version | |
| Unit System | Metric |
| Length display | Millimeters |
| Unit Scale | 0.001 (team default) / other: |
| Track | A — measured board / B — placeholder 80×55×1.6 |

---

## Concept notes (short)

| Question | Answer |
|---|---|
| How is the device held / placed? | |
| Which ports must be visible? | |
| Which sensors need openings? | |
| Lid opens which way? | |

---

## Size source

| Item | Value |
|---|---|
| PCB source (calipers / datasheet / kit doc URL) | |
| PCB X × Y × thickness (mm) | |
| Tallest component height above PCB (mm) | |
| Clearance each side (mm) | |
| Planned wall thickness (mm) | |
| Top air gap (mm) | |
| Bottom air / base (mm) | |

Kit / docs used (if any):  
- [KIT_PSE84_EVAL guide](https://documentation.infineon.com/psocedge/docs/lne1762692969598)  
- Other:  

---

## Calculated enclosure outer (before modeling)

| Axis | Formula notes | Result (mm) |
|---|---|---|
| Outer X | | |
| Outer Y | | |
| Outer Z | | |

---

## Blender objects

| Object name | Dimensions X×Y×Z (mm) | Scale applied 1,1,1? | Origin set? |
|---|---|---|---|
| `PCB_placeholder` | | Yes / No | Yes / No |
| `Enclosure_block` | | Yes / No | Yes / No |
| (optional) | | | |

---

## Fit check

| Check | OK? | Notes |
|---|---|---|
| Wireframe: PCB inside enclosure | | |
| No accidental poke-through | | |
| Clearance roughly matches plan | | |

---

## Files

| File | Name |
|---|---|
| `.blend` | |
| Screenshot | |

---

## Quick recall

```text
Units (Metric + mm + Scale 0.001)
  → measure / placeholder PCB
  → calculate outer with clearance + wall
  → Enclosure_block
  → Apply Scale + name objects
  → screenshot + this checklist
```

### Online refs (click when stuck)

- [Blender Scene Units](https://docs.blender.org/manual/en/4.5/scene_layout/scene/properties.html#units)  
- [Apply Scale](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/apply.html)  
- [Set Origin](https://docs.blender.org/manual/en/4.5/scene_layout/object/origin.html)  
- [Enclosure clearance guide](https://www.hubs.com/knowledge-base/enclosure-design-3d-printing-step-step-guide/)  
- [Electronics enclosure steps](https://www.allaboutcircuits.com/industry-articles/six-steps-for-designing-a-custom-3d-printed-electronics-enclosure/)  

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [M02](../../../m02-modeling-render/l01-modeling-materials-render/README.md)
