# NOTICE — แผนที่ทักษะ (skills/)

## Attribution

"TESA Embedded Systems Skill Map" (แผนที่ทักษะวิศวกรรมระบบสมองกลฝังตัว TESA) is adapted from
"Embedded Systems Engineering Roadmap" (diagram v1.2.3, 2023-12-23; README @a9f4eac5) by Meysam Parvizi,
https://github.com/m3y54m/Embedded-Engineering-Roadmap, licensed under CC BY-SA 4.0
(https://creativecommons.org/licenses/by-sa/4.0/).

The adaptation is © 2026 สมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) and is licensed under
CC BY-SA 4.0 (full text: [../LICENSES/CC-BY-SA-4.0.txt](../LICENSES/CC-BY-SA-4.0.txt)).

**It is not endorsed by, or affiliated with, the original author.**

Pinned sources:

| Artefact | Reference |
|---|---|
| Diagram (PNG/PDF/VSDX) | release [v1.2.3](https://github.com/m3y54m/Embedded-Engineering-Roadmap/releases/tag/v1.2.3), tag commit `57f2758660f17bd835ca969d35e0b8d95e53a84e`, dated 2023-12-23 |
| README (topic list) | commit [`a9f4eac5c9f42031bebd87e25cdbfeb05b6f0c1b`](https://github.com/m3y54m/Embedded-Engineering-Roadmap/tree/a9f4eac5c9f42031bebd87e25cdbfeb05b6f0c1b), 2026-07-23 |

## Changes made by TESA

1. **Stable skill IDs.** Every node became a permanent, lowercase ID of the form `group.topic`
   (for example `mcu.gpio`, `proto.mqtt`). IDs are never renamed or reused; a retired skill is marked
   `deprecated: true` with `replaced_by:`.
2. **Structure.** Nodes were arranged into 6 areas and 24 groups for navigation. The original node path is kept in
   `eer_node` for every skill that comes from the diagram.
3. **Thai and English names.** Every area, group and skill has a Thai name next to the English one.
4. **Proficiency levels.** Five levels, L1–L5, were added. Their numbers match the Thai professional-qualification levels
   of TPQI (see [../tqp/levels.md](../tqp/levels.md)). The roadmap itself has no levels.
5. **Origin field.** `origin: eer` marks a node from the diagram v1.2.3, `origin: eer-readme` a topic found only in the newer
   README, and `origin: tesa` a skill TESA added.
6. **Importance.** The diagram's three importance categories (Required, Recommended, Possibilities) are kept as
   `importance: R | Rec | P` for diagram nodes. Skills not coloured on the diagram have `importance: null`.
7. **Topics taken from the newer README** (`origin: eer-readme`): `sec.crypto`, `sec.secure-boot`, `iot.ota`,
   `ai.model-training`, `proto.rs485`.
8. **Skills added by TESA** (`origin: tesa`): `lang.micropython`, `rtos.multicore-ipc`, `build.vendor-sdk`, `sec.tls`,
   `sec.secure-element`, `gui.hmi`, `iot.cloud-platform`, `iot.digital-twin`, `ai.data-collection`, `ai.model-deploy`,
   `hwdev.enclosure`, `hwdev.3d-modeling`, `biz.product-decision`, `biz.cost-bom`, `biz.risk-compliance`,
   `edu.lesson-design`, `edu.assessment`, `edu.facilitation`.
9. **Role profiles.** [roles/](roles/) re-weights importance per job role: a profile may require a skill the roadmap marks
   Recommended or Possibilities, and records that in `promoted_from`.
10. **Machine-readable form.** The map is YAML ([skills.yaml](skills.yaml)); tools export it as JSON and a CASE-shaped package,
    and each skill gets a stable UUID and page URL.
11. **What was not copied.** The roadmap's descriptions and learning-resource lists were not copied. Lessons link to the
    roadmap instead.

## Scope of the ShareAlike licence

Only the adapted skill map in `skills/` is CC BY-SA 4.0. Lessons and courses that merely refer to skill IDs are separate works
in a collection, remain CC BY 4.0, and are not adaptations of the roadmap. If you adapt this skill map, your version must be
licensed CC BY-SA 4.0 (or a licence CC lists as compatible) and must credit both TESA and Meysam Parvizi.

---

## ภาษาไทยโดยย่อ

แผนที่ทักษะในโฟลเดอร์นี้ดัดแปลงจาก "Embedded Systems Engineering Roadmap" ของ Meysam Parvizi (แผนภาพ v1.2.3 ลงวันที่ 2023-12-23
และ README ที่ commit a9f4eac5) สัญญาอนุญาต CC BY-SA 4.0 งานดัดแปลงนี้ © 2026 สมาคมสมองกลฝังตัวไทย (TESA) เผยแพร่ภายใต้
CC BY-SA 4.0 เช่นกัน และผู้เขียนต้นฉบับไม่ได้รับรองหรือเกี่ยวข้องกับงานดัดแปลงนี้

สิ่งที่ TESA เปลี่ยน: ตั้ง ID ถาวรให้ทุกทักษะ จัดกลุ่มเป็น 6 ด้าน 24 กลุ่ม เพิ่มชื่อภาษาไทย เพิ่มระดับ L1–L5 ที่ตัวเลขตรงกับ TPQI
เพิ่มฟิลด์ `origin` คงความสำคัญ R / Rec / P ตามแผนภาพ เพิ่มหัวข้อจาก README ฉบับใหม่ 5 ทักษะ เพิ่มทักษะของ TESA เอง 18 ทักษะ
ทำโปรไฟล์บทบาทที่ยกระดับความสำคัญตามสายงาน และทำเป็นข้อมูล YAML ที่เครื่องอ่านได้ ไม่ได้คัดลอกคำอธิบายหรือรายการแหล่งเรียนรู้ของต้นฉบับ

เฉพาะ `skills/` เท่านั้นที่เป็น CC BY-SA 4.0 บทเรียนที่เพียงอ้าง skill ID ยังเป็น CC BY 4.0
