# แผนที่ทักษะ (Skill Map)

แผนที่ทักษะวิศวกรรมระบบสมองกลฝังตัว TESA (TESA Embedded Systems Skill Map) คือรายการทักษะที่ทุกบทเรียนใน TESA Open Knowledge
อ้างถึง และเป็นฐานของ Skillset Mapping ใน TESA Qualification Program (TQP) เราเก็บเป็นข้อมูล ไม่ใช่รูปภาพ
หน้า roadmap ตาราง coverage และการผูกใบรับรองกับทักษะจึงสร้างจากไฟล์ชุดนี้ได้อัตโนมัติ

| ไฟล์ | คืออะไร |
|---|---|
| [skills.yaml](skills.yaml) | แหล่งเดียวของ skill ID ทั้งหมด (127 ทักษะ ใน 24 กลุ่ม 6 ด้าน) เวอร์ชันอยู่ที่ `framework.version` |
| [roles/](roles/) | โปรไฟล์บทบาท 6 แบบ บอกว่าแต่ละสายงานต้องมีทักษะใดที่ระดับใด |
| [NOTICE.md](NOTICE.md) | ที่มา การให้เครดิต Meysam Parvizi และรายการสิ่งที่ TESA เปลี่ยน |

*English summary: [below](#english-summary)*

## skill ID

- รูปแบบ `กลุ่ม.หัวข้อ` ตัวพิมพ์เล็ก เช่น `mcu.gpio`, `proto.mqtt`, `sec.secure-element` ส่วนหน้าคือกลุ่ม (`mcu`, `proto`, `sec` …)
- **ID ถาวร** ไม่เปลี่ยนชื่อและไม่นำกลับมาใช้ซ้ำ เพราะใบรับรองที่ออกไปแล้วอ้าง ID เหล่านี้อยู่ ทักษะที่เลิกใช้จะมี
  `deprecated: true` และ `replaced_by:` แทนการลบ
- **ID ไม่ผูกกับผู้ผลิต** ชื่อ PSOC™ Edge, ModusToolbox™ หรือ BENTO อยู่ในฟิลด์ `context:` ของบทเรียน ไม่อยู่ใน ID
- ทุกทักษะมี UUID คงที่ คำนวณจาก
  `uuid5(NAMESPACE_URL, "https://tesaiot.github.io/tesa-qualification-program/skills/<id>/")` โดยเครื่องมือ ไม่ได้เก็บไว้ในไฟล์
  และมีหน้าเว็บถาวรที่ `/skills/<id>/` บนเว็บไซต์ของโครงการ
- ถ้าต้องการทักษะที่ยังไม่มี อย่าตั้ง ID เอง ให้เปิด issue เสนอ แล้วใช้ ID ที่ใกล้ที่สุดไปก่อน

## ระดับ L1–L5

ตัวเลขระดับตรงกับระดับคุณวุฒิวิชาชีพของสถาบันคุณวุฒิวิชาชีพ (TPQI) คนที่เห็น "L4" จะเทียบกับ TPQI ระดับ 4 ได้ทันที
รายละเอียดเต็มและวิธีเก็บหลักฐานอยู่ใน [tqp/levels.md](../tqp/levels.md)

| ระดับ | ชื่อ | ทำอะไรได้ | จุดเทียบ |
|---|---|---|---|
| L1 | รู้จัก (Aware) | อธิบายแนวคิด และรันตัวอย่างที่มีให้ได้ | — |
| L2 | ทำตามแนวทาง (Guided) | แก้หรือเติมโค้ดบนโครงที่มีให้ | — |
| L3 | ทำได้เอง (Independent) | สร้างงานตามข้อกำหนดที่ชัดเจนได้ด้วยตัวเอง | — |
| L4 | มืออาชีพ (Professional) | พัฒนา ทดสอบ และแก้ไขระบบจริงได้ครบวงจร | ≈ TPQI นักพัฒนาระบบสมองกลฝังตัว ระดับ 4 |
| L5 | ออกแบบและนำทีม (Design & Lead) | ออกแบบสถาปัตยกรรมฮาร์ดแวร์และซอฟต์แวร์ และชี้แนะผู้อื่นได้ | ≈ TPQI นักพัฒนาระบบสมองกลฝังตัว ระดับ 5 |

## ความสำคัญ (importance)

Roadmap ต้นฉบับแบ่งหัวข้อเป็นสามหมวดด้วยสีบนแผนภาพ เราเก็บหมวดนั้นไว้ในฟิลด์ `importance` และหน้า roadmap บนเว็บไซต์ระบายสีตามหมวดนี้

| ค่า | ความหมาย |
|---|---|
| `R` | จำเป็น (Required) |
| `Rec` | แนะนำ (Recommended) |
| `P` | ทางเลือก (Possibilities) |
| `null` | ไม่มีสีบนแผนภาพ ได้แก่ทักษะที่ TESA เพิ่ม และหัวข้อที่มีเฉพาะใน README ฉบับใหม่ของ Roadmap |

ต้นฉบับเองเขียนไว้ว่าความสำคัญเป็นค่าเฉลี่ย และต่างกันไปตามอุตสาหกรรมและบทบาทงาน เราจึงไม่ใช้สีเดียวกับทุกคน
แต่ให้โปรไฟล์บทบาท (หัวข้อด้านล่าง) ยกระดับความสำคัญตามสายงาน

## ที่มาของทักษะ (origin)

| ค่า | ความหมาย |
|---|---|
| `eer` | โหนดบนแผนภาพ Embedded Systems Engineering Roadmap v1.2.3 มีฟิลด์ `eer_node` เก็บตำแหน่งเดิม |
| `eer-readme` | หัวข้อที่มีเฉพาะใน README ฉบับใหม่ของ Roadmap (commit a9f4eac5) |
| `tesa` | ทักษะที่ TESA เพิ่ม เช่น `sec.secure-element`, `iot.digital-twin`, `biz.*`, `edu.*` |

## บทเรียนประกาศทักษะอย่างไร

front matter ของบทเรียนมีสองรายการ

- `develops` ทักษะที่บทเรียนนี้ **พัฒนา** และพาผู้เรียนไปถึงระดับใด (`to`) ต้องมีอย่างน้อยหนึ่งรายการ
- `assesses` ทักษะที่บทเรียนนี้ **ประเมิน** ที่ระดับใด (`level`) และหลักฐานคืออะไร (`evidence` ชี้ไปที่ไฟล์ในบทเรียน) ใส่หรือไม่ก็ได้

```yaml
develops: [{skill: mcu.gpio, to: 2}, {skill: mcu.timers, to: 2}]
assesses: [{skill: mcu.gpio, level: 2, evidence: practice/led_button.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
```

เฉพาะรายการใน `assesses` ของบทเรียนสถานะ `stable` เท่านั้นที่นำไปใช้เป็นหลักฐานของใบรับรองได้ ดู [templates/lesson/README.md](../templates/lesson/README.md)
และ [templates/AUTHORING.md](../templates/AUTHORING.md)

## โปรไฟล์บทบาท

ไฟล์ใน [roles/](roles/) มีรูปแบบนี้

```yaml
id: iot-device-developer
title: {th: ..., en: ...}
summary: {th: ..., en: ...}
target_level: L4                 # ระดับของบทบาทโดยรวม
requires:                        # ระดับขั้นต่ำรายทักษะ
  - {skill: proto.mqtt, level: 3, promoted_from: Rec}
anchors: {tpqi: "...", note: "..."}
```

- `target_level` คือระดับของบทบาทโดยรวม ส่วน `requires` คือระดับขั้นต่ำรายทักษะ บทบาทระดับ L4 ไม่จำเป็นต้องมีทุกทักษะที่ L4
  เพราะ L4 แสดงด้วยการรวมทักษะระดับ L3 เข้าเป็นระบบที่ใช้งานได้จริงภายใต้เงื่อนไขการสอบ
- `promoted_from` คือความสำคัญของทักษะนั้นบน Roadmap (ค่าเดียวกับ `importance` ใน skills.yaml): `R` แปลว่าจำเป็นอยู่แล้ว
  `Rec` หรือ `P` แปลว่าบทบาทนี้ยกขึ้นเป็นจำเป็น และ `null` แปลว่าไม่มีสีบน Roadmap
- โปรไฟล์ในสาย TESA × Infineon ยกหัวข้อ IoT, Edge AI, ความปลอดภัย และการประหยัดพลังงาน จาก `P` หรือ `Rec` ขึ้นเป็นจำเป็น
- ทักษะด้านบุคคล (`soft.*`) ทั้ง 6 ข้อเป็นทักษะจำเป็นในทุกโปรไฟล์ และประเมินจากหลักฐานในโปรเจกต์

| โปรไฟล์ | ระดับ | จุดเทียบ |
|---|---|---|
| [นักพัฒนาเฟิร์มแวร์](roles/firmware-developer.yaml) | L4 | TPQI นักพัฒนาระบบสมองกลฝังตัว ระดับ 4 |
| [นักพัฒนาอุปกรณ์ IoT](roles/iot-device-developer.yaml) | L4 | TPQI นักพัฒนาซอฟต์แวร์เพื่ออินเตอร์เน็ตของสรรพสิ่ง ระดับ 4 |
| [วิศวกร Edge AI](roles/edge-ai-engineer.yaml) | L4 | ยังไม่มีคุณวุฒิ TPQI โดยตรง |
| [วิศวกรความปลอดภัยระบบฝังตัว](roles/embedded-security-engineer.yaml) | L4 | ยังไม่มีคุณวุฒิ TPQI โดยตรง |
| [ผู้ประกอบการและเจ้าของผลิตภัณฑ์](roles/product-entrepreneur.yaml) | L3 | — |
| [ผู้สอน](roles/educator.yaml) | L4 | TQP Certified Trainer |

กรอบ SFIA ถูกใช้เป็นจุดเทียบภายในเท่านั้น และไม่ได้เผยแพร่เป็นส่วนหนึ่งของการเทียบระดับ เพราะการเผยแพร่ตารางเทียบกับ SFIA
ในฐานะส่วนหนึ่งของใบรับรองต้องมีสัญญาอนุญาตเฉพาะจาก SFIA Foundation

## ทำไม skills/ เป็น CC BY-SA แต่บทเรียนเป็น CC BY

แผนที่ทักษะดัดแปลงจาก Roadmap ของ Meysam Parvizi ซึ่งใช้ CC BY-SA 4.0 เงื่อนไข ShareAlike บังคับให้งานดัดแปลงใช้สัญญาอนุญาตเดียวกัน
โฟลเดอร์นี้จึงเป็น CC BY-SA 4.0 ส่วนบทเรียนที่เพียงอ้าง skill ID ถือเป็นงานแยกที่อยู่รวมกันในชุด (collection) ไม่ใช่งานดัดแปลงของ Roadmap
จึงยังเป็น CC BY 4.0 ได้ ข้อควรระวังคืออย่าคัดลอกข้อความหรือรายการแหล่งเรียนรู้ของ Roadmap ลงในบทเรียนหรือสไลด์ ให้ลิงก์ไปแทน
(คำอธิบายนี้เป็นการอ่านสัญญาอนุญาตในทางปฏิบัติ ไม่ใช่คำปรึกษาทางกฎหมาย)

## เวอร์ชัน

`skills.yaml` ใช้ SemVer ในฟิลด์ `framework.version`: ลบหรือเปลี่ยนชื่อ ID เป็นการเปลี่ยน MAJOR, เพิ่มทักษะ กลุ่ม หรือโปรไฟล์เป็น MINOR,
แก้ถ้อยคำเป็น PATCH รายละเอียดใน [GOVERNANCE.md](../GOVERNANCE.md)

---

## English summary

The **TESA Embedded Systems Skill Map** is the list of skills every lesson refers to, and the basis of the TQP Skillset Mapping.
It is data, not a picture: [skills.yaml](skills.yaml) holds 127 skills in 24 groups and 6 areas, [roles/](roles/) holds six role
profiles, and [NOTICE.md](NOTICE.md) gives the attribution to Meysam Parvizi and the list of TESA's changes.

- **IDs** look like `group.topic` (`mcu.gpio`, `proto.mqtt`), are lowercase, permanent and vendor-neutral (PSOC™ Edge,
  ModusToolbox™ and BENTO go in a lesson's `context:`). Retired skills get `deprecated: true` and `replaced_by:`. Each skill has a
  stable UUID, `uuid5(NAMESPACE_URL, "https://tesaiot.github.io/tesa-qualification-program/skills/<id>/")`, computed by tools, and
  a permanent page at `/skills/<id>/`. Never invent an ID in a lesson; propose it in an issue.
- **Levels L1–L5** (Aware, Guided, Independent, Professional, Design & Lead) use the same numbers as TPQI professional
  qualifications: L4 ≈ TPQI นักพัฒนาระบบสมองกลฝังตัว ระดับ 4 (Embedded Systems Developer level 4), L5 ≈ level 5.
  See [tqp/levels.en.md](../tqp/levels.en.md).
- **Importance** keeps the roadmap diagram's three colour categories: `R` Required, `Rec` Recommended, `P` Possibilities;
  `null` where the diagram has no colour. The site's roadmap page colours skills by this field.
- **Origin**: `eer` (a node on diagram v1.2.3, with its path in `eer_node`), `eer-readme` (only in the newer README),
  `tesa` (added by TESA).
- **Lessons** declare `develops: [{skill, to}]` (at least one) and optionally `assesses: [{skill, level, evidence}]`.
  Only `assesses` entries of `stable` lessons can serve as evidence for a credential.
- **Role profiles** have `target_level` (the level of the role as a whole) and `requires` (minimum level per skill).
  `promoted_from` repeats the skill's roadmap importance: `R` already required, `Rec`/`P` raised to required by this role,
  `null` no roadmap colour. TESA × Infineon profiles raise IoT, Edge AI, security and low-power skills; the six `soft.*` skills
  are required in every profile. SFIA is an internal reference only (publishing a SFIA mapping needs a SFIA licence).
- **Why CC BY-SA here and CC BY in lessons:** this map adapts a CC BY-SA 4.0 work, so ShareAlike applies to `skills/`.
  Lessons that only cite skill IDs are separate works in a collection and stay CC BY 4.0. Do not copy the roadmap's text or
  resource lists into lessons; link to them. (A practical reading, not legal advice.)
- **Versioning:** SemVer in `framework.version`; removing or renaming an ID is MAJOR (see [GOVERNANCE.md](../GOVERNANCE.md)).
