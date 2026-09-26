# Blender for Twin visualization — Course 2 M03

**Course 2 · Module 3** (companion to Virtual Device Modeling)

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [TOC](../../../README.md)

Use with free assets: [ternion-3d-assets-free](https://github.com/drsanti/ternion-3d-assets-free)

---

## Install & UI

| Resource | URL |
|---|---|
| Download Blender | https://www.blender.org/download/ |
| Manual home (latest) | https://docs.blender.org/manual/en/latest/ |
| Manual 4.5 LTS | https://docs.blender.org/manual/en/4.5/ |
| Interface intro | https://docs.blender.org/manual/en/4.5/interface/index.html |
| Fundamentals (Studio, EN) | https://studio.blender.org/training/blender-fundamentals-45-lts/ |
| **Tutorial ภาษาไทย (YouTube)** | https://www.youtube.com/playlist?list=PLBPFpqyTjzeVCRoOEIDrqF07M8cXTfIXY |

Modes you will use most: **Object** · **Edit** · **Shading** · **Animation** editors (Dope Sheet / Timeline)

---

## Modeling

| Topic | Start here |
|---|---|
| Mesh intro | https://docs.blender.org/manual/en/4.5/modeling/meshes/introduction.html |
| Edit Mode tools | https://docs.blender.org/manual/en/4.5/modeling/meshes/editing/index.html |
| Extrude | https://docs.blender.org/manual/en/4.5/modeling/meshes/editing/mesh/extrude.html |
| Loop Cut | https://docs.blender.org/manual/en/4.5/modeling/meshes/tools/loop.html |
| Bevel | https://docs.blender.org/manual/en/4.5/modeling/meshes/editing/edge/bevel.html |
| Modifiers | https://docs.blender.org/manual/en/4.5/modeling/modifiers/introduction.html |
| Fundamentals — Modeling chapter | https://studio.blender.org/training/blender-fundamentals-45-lts/chapter/blender_4_5_lts_modeling/ |

Twin tips: real-world scale (meters) · Apply Scale · origin at meaningful pivot · keep polycount reasonable for webview

---

## Texturing / materials

| Topic | Start here |
|---|---|
| Materials intro | https://docs.blender.org/manual/en/4.5/render/materials/introduction.html |
| Principled BSDF | https://docs.blender.org/manual/en/4.5/render/shader_nodes/shader/principled.html |
| UV editing | https://docs.blender.org/manual/en/4.5/editors/uv/index.html |
| UV unwrap | https://docs.blender.org/manual/en/4.5/modeling/meshes/uv/unwrapping/index.html |
| Texture paint | https://docs.blender.org/manual/en/4.5/sculpt_paint/texture_paint/index.html |
| Image textures | https://docs.blender.org/manual/en/4.5/render/shader_nodes/textures/image.html |

For glTF/Twin: prefer **Principled BSDF** metal/rough maps; connect **UV Map** → Image Texture. See glTF materials section below.

Cubemaps / sample textures for Studio: [ternion-3d-assets-free `textures/`](https://github.com/drsanti/ternion-3d-assets-free/tree/main/assets/textures)

---

## Animation

| Topic | Start here |
|---|---|
| Animation intro | https://docs.blender.org/manual/en/4.5/animation/introduction.html |
| Keyframes | https://docs.blender.org/manual/en/4.5/animation/keyframes/index.html |
| Actions | https://docs.blender.org/manual/en/4.5/animation/actions.html |
| Armatures | https://docs.blender.org/manual/en/4.5/animation/armatures/index.html |
| Shape keys | https://docs.blender.org/manual/en/4.5/animation/shape_keys/index.html |
| Constraints | https://docs.blender.org/manual/en/4.5/animation/constraints/introduction.html |

What typically exports to glTF: object/bone **location · rotation · scale**, shape keys, skinning — not arbitrary material/light keyframes. Details: glTF animation docs below.

---

## Export for Twin (glTF / GLB)

| Topic | Start here |
|---|---|
| glTF 2.0 add-on (4.5) | https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html |
| glTF 2.0 add-on source and docs (Khronos) | https://github.com/KhronosGroup/glTF-Blender-IO |
| Khronos glTF overview | https://www.khronos.org/gltf/ |

Checklist:

1. Apply transforms where needed  
2. UV + Principled materials ready  
3. Animation = active Action / NLA as required by exporter  
4. Export **glTF Binary (.glb)** for Bitstream / Twin webview  
5. Compare naming with [ternion-3d-assets-free models](https://github.com/drsanti/ternion-3d-assets-free/tree/main/assets/models)

---

## Course 2 vs Course 3

| Here (C2 M03) | Later (Course 3) |
|---|---|
| Enough Blender to feed Twin visualization | Industrial design depth, casing, validation, prototype |

[Lesson](../README.md) · [Lab](../../l02-lab/README.md)
