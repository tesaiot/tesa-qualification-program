# ธรรมาภิบาล (Governance)

เอกสารนี้บอกว่าใครดูแล TESA Open Knowledge ใครตัดสินใจเรื่องใด และบทเรียนหนึ่งบทเดินจากร่างแรกไปถึงสถานะที่นับใน
TESA Qualification Program (TQP) ได้อย่างไร เป็นฉบับ v0.1 (กันยายน 2569) และจะปรับเมื่อแต่งตั้งกองบรรณาธิการแล้ว

*English summary: [below](#english-summary)*

## 1. เจ้าของและผู้เผยแพร่

สมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) เป็นเจ้าของและผู้เผยแพร่ TESA Open Knowledge
TQP เป็นโครงการร่วมระหว่าง TESA และ Infineon คลังความรู้นี้เป็นแหล่งเรียนรู้แบบเปิดที่ป้อน Skillset Mapping ให้ TQP
แต่ **ไม่ใช่หน่วยรับรอง** การรับรองบุคคลเป็นหน้าที่ของหน่วยแยก (ดูข้อ 8)

## 2. บทบาท

| บทบาท | ใคร | หน้าที่ |
|---|---|---|
| **กองบรรณาธิการ (Editorial Board)** | 3–5 คน จาก TESA และนักวิชาการที่เป็นหัวหน้าหลักสูตร | กำหนดทิศทาง อนุมัติหลักสูตรใหม่ เลื่อนสถานะเป็น stable ดูแลสัญญาอนุญาต แผนที่ทักษะ และเอกสารนี้ |
| **Infineon** | ผู้แทนที่ Infineon แต่งตั้ง | พันธมิตรร่วมของ TQP และผู้ตรวจความถูกต้องทางเทคนิค ให้ความเห็นในการตรวจ แต่ไม่มีสิทธิ์วีโต้ในกองบรรณาธิการ |
| **หัวหน้าหลักสูตร (Course Lead)** | หนึ่งคนต่อหลักสูตร ระบุใน [`.github/CODEOWNERS`](.github/CODEOWNERS) | ดูแลเนื้อหา รับ PR ของหลักสูตร และเสนอเลื่อนสถานะบทเรียน |
| **ผู้ตรวจทางเทคนิค (Technical Reviewer)** | ผู้มีประสบการณ์ในเรื่องนั้น | รันโค้ดบนบอร์ดจริงหรือ emulator และบันทึกผล |
| **ผู้ตรวจด้านการสอน (Pedagogical Reviewer)** | ผู้สอนหรือนักออกแบบการเรียนรู้ | ตรวจเป้าหมาย เวลา prerequisite skill ID และภาษา |
| **ผู้แปล (Translator)** | ใครก็ได้ | แปลไทย ↔ อังกฤษ และดูแลสถานะ `translation` |
| **ผู้ร่วมพัฒนา (Contributor)** | ทุกคน | เสนอแก้ไขผ่าน issue และ pull request ตาม [CONTRIBUTING.md](CONTRIBUTING.md) |
| **ผู้ดูแลชุมชน (Community Moderators)** | อย่างน้อย 2 คนที่กองบรรณาธิการแต่งตั้ง | รับเรื่องและดำเนินการตาม [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) |

ระหว่างที่ยังไม่ได้แต่งตั้งกองบรรณาธิการ ผู้ดูแล repository ตามที่ระบุใน `.github/CODEOWNERS` ทำหน้าที่แทนชั่วคราว
และจะประกาศรายชื่อกองบรรณาธิการในเอกสารนี้เมื่อแต่งตั้งแล้ว

สมาชิกกองบรรณาธิการต้องแจ้งส่วนได้เสีย เช่น การขายคอร์สอบรม หรือการเป็นพนักงานของผู้ผลิตชิป และงดออกเสียงในเรื่องที่ตนมีส่วนได้เสียโดยตรง

## 3. การตรวจสองชั้น (two-key review)

บทเรียนใหม่หรือการแก้ไขที่เปลี่ยนเนื้อหาสาระ ต้องผ่านผู้ตรวจสองคนที่ไม่ใช่ผู้เขียน คนละด้าน

**ชั้นเทคนิค**
- รันทุกไฟล์ใน `examples/` และ `solution/` บนบอร์ดจริง หรือบน BENTO Emulator สำหรับบทเรียนที่ประกาศ `hardware.emulator: true`
- บันทึกใน PR ว่าทดสอบบนอะไร: ชื่อบอร์ด เวอร์ชันเฟิร์มแวร์ เวอร์ชัน toolchain (ModusToolbox, MicroPython) หรือเวอร์ชัน emulator
- การตรวจแบบ static (เช่น `mpy-cross` หรือ linter) ใช้แทนการรันบนบอร์ดไม่ได้ เพราะมีโค้ดที่ผ่าน `mpy-cross` แต่เฟิร์มแวร์บนบอร์ดไม่รับ

**ชั้นการสอน**
- เป้าหมาย 2–4 ข้อ เขียนด้วยกริยาที่วัดผลได้ พร้อมเงื่อนไข และทุกเป้าหมายมีข้อเช็กความเข้าใจคู่กัน
- เวลาใน `time_min` สมจริง และรวมอยู่ในช่วง 20–75 นาที
- prerequisite ครบ และ skill ID ใน `develops` / `assesses` มีอยู่จริงใน `skills/skills.yaml` ที่ระดับเหมาะสม
- ภาษาไทยชัดเจน ตามคู่มือผู้เขียน [templates/AUTHORING.md](templates/AUTHORING.md)

**ข้อยกเว้น** การแก้คำผิด ลิงก์เสีย หรือ erratum ที่ไม่เปลี่ยนสาระ ใช้การอนุมัติหนึ่งคนจากหัวหน้าหลักสูตรหรือผู้ดูแล

ทุก PR ต้องผ่าน `python3 tools/validate.py` และมี DCO sign-off ทุก commit

## 4. วงจรชีวิตของบทเรียนและหลักสูตร

สถานะอยู่ในฟิลด์ `status` ของ `course.yaml` และ front matter ของบทเรียน ใช้ค่าเดียวกันทั้งสองระดับ

| สถานะ | ความหมาย | เกณฑ์ที่ต้องผ่านเพื่อเข้าสถานะนี้ |
|---|---|---|
| `pre-alpha` | ร่างโครง | มีเป้าหมาย โครงบทเรียน และ skill ID ผ่าน validator แต่เนื้อหายังไม่ครบ |
| `alpha` | ฉบับร่างที่เรียนได้ | เนื้อหาครบทุกหัวข้อที่เกี่ยวข้อง ผู้เขียนรันโค้ดทุกไฟล์เองแล้ว |
| `beta` | ทดลองสอน | ผ่านการตรวจสองชั้น และ **มีผู้อื่นที่ไม่ใช่ผู้เขียนนำไปสอนนำร่องแล้ว** พร้อมบันทึกผลนำร่องใน issue หรือ PR |
| `stable` | พร้อมใช้ | ผ่าน beta แก้ข้อเสนอแนะจากการนำร่องแล้ว ไม่มี erratum ร้ายแรงค้างอยู่ และกองบรรณาธิการอนุมัติ |

- **เฉพาะบทเรียนสถานะ `stable` เท่านั้นที่นับใน TQP** เช่น ในใบ T0 และในการอ้างอิงแผนที่ทักษะของข้อสอบ
- สถานะของหลักสูตรไม่สูงกว่าสถานะของบทเรียนส่วนใหญ่ในหลักสูตรนั้น
- ID ของบทเรียน (`<short>.mNN.lNN`) ถาวร ไม่เปลี่ยนและไม่นำกลับมาใช้ซ้ำ แม้จะย้ายลำดับหรือเลิกใช้บทเรียนนั้นแล้ว
- ถ้าการเปลี่ยน toolchain หรือเฟิร์มแวร์ทำให้บทเรียนใช้ไม่ได้ ให้ลดสถานะลงจนกว่าจะแก้เสร็จ

## 5. รุ่นและเวอร์ชัน

- **คลังความรู้** ออกรุ่นแบบ CalVer `YYYY.MM` (เช่น `2026.09`) เป็น GitHub Release ทุกรุ่นมี DOI จาก Zenodo
  (DOI ประจำโครงการหนึ่งตัว และ DOI ประจำรุ่น) ข้อมูลอ้างอิงมาจาก [CITATION.cff](CITATION.cff)
- ทุกรุ่นระบุเวอร์ชันเฟิร์มแวร์ BENTO, ModusToolbox และ MicroPython ที่ใช้ทดสอบ ถ้าการเปลี่ยน toolchain บังคับให้ต้องแยก
  จะตัด branch `release/YYYY.MM` ส่วน `main` คือฉบับล่าสุดเสมอ
- **แผนที่ทักษะ** `skills/skills.yaml` ใช้ SemVer ในฟิลด์ `framework.version`
  - **MAJOR** เมื่อลบหรือเปลี่ยนชื่อ skill ID หรือเปลี่ยนความหมายของระดับ (ในทางปฏิบัติ ID ไม่เปลี่ยนชื่อ ให้เลิกใช้ด้วย
    `deprecated: true` และ `replaced_by:` แทน)
  - **MINOR** เมื่อเพิ่มทักษะ กลุ่ม หรือโปรไฟล์บทบาท หรือเลิกใช้ ID แบบมี `replaced_by`
  - **PATCH** เมื่อแก้ชื่อที่แสดงหรือคำอธิบายโดยไม่เปลี่ยนความหมาย
- ใบรับรองอ้างอิงทั้งสองเวอร์ชัน เช่น "curriculum 2026.10 + skills 1.0.0"

## 6. การตัดสินใจ

1. เรื่องทั่วไปใน PR ใช้ฉันทามติแบบเงียบ (lazy consensus): ถ้าผ่านการตรวจครบและไม่มีผู้คัดค้านพร้อมเหตุผลภายใน 7 วัน ให้ merge ได้
2. เมื่อมีข้อโต้แย้งที่หัวหน้าหลักสูตรตัดสินไม่ได้ ส่งให้กองบรรณาธิการ ซึ่งพยายามหาฉันทามติก่อน
   ถ้าไม่ได้ภายใน 14 วัน ใช้เสียงข้างมากของกองบรรณาธิการ
3. เรื่องต่อไปนี้ต้องได้เสียงเห็นชอบอย่างน้อย 2 ใน 3 ของกองบรรณาธิการ: เปลี่ยนสัญญาอนุญาต แก้เอกสารธรรมาภิบาลนี้
   ออกรุ่น MAJOR ของแผนที่ทักษะ และรับหรือถอดหลักสูตรออกจากแคตาล็อก
4. ความเห็นทางเทคนิคของ Infineon ต้องถูกบันทึกและตอบในการตรวจ แต่ไม่ใช่เสียงวีโต้
5. ทุกการตัดสินใจระดับกองบรรณาธิการบันทึกเป็น issue สาธารณะที่มีป้าย `decision` ยกเว้นเรื่องที่เกี่ยวกับข้อมูลส่วนบุคคลหรือจรรยาบรรณ

## 7. เนื้อหาจากภายนอก

- หลักสูตรที่ TESA เขียนเองอยู่ใน `courses/` หลักสูตรภายนอกลงทะเบียนใน `catalog/courses.yaml` โดย pin ที่ tag หรือ commit
  และบันทึกสัญญาอนุญาต
- ตัวอย่างโค้ดของ Infineon ใช้วิธีลิงก์ไปยัง repository และ tag เป็นค่าเริ่มต้น ถ้าคัดลอกมา ต้องคง header และไฟล์สัญญาอนุญาตเดิม
  และอ้างอิงแหล่งให้ครบ (ดู [NOTICE.md](NOTICE.md))
- เนื้อหาภายใต้ NDA ใด ๆ ห้ามนำเข้าคลังนี้

## 8. การแยกเนื้อหาเปิดออกจากการสอบ

- **คลังข้อสอบของ TQP อยู่ใน repository ส่วนตัวแยกต่างหาก** ไม่อยู่ในคลังนี้ ข้อเช็กความเข้าใจ แบบฝึก และเฉลยในคลังนี้เปิดสาธารณะ
  และไม่ถูกนำไปใช้เป็นข้อสอบจริง
- การรับรองบุคคลเป็นหน้าที่ของหน่วยรับรองของ TESA ที่แยกจากกองบรรณาธิการและจากฝ่ายขายคอร์สอบรม ตามที่อธิบายใน
  [tqp/certification.md](tqp/certification.md)
- ผู้ที่เขียนข้อสอบจริงไม่เปิดเผยข้อสอบหรือพารามิเตอร์ของโจทย์ในคลังนี้

## 9. การแก้ไขเอกสารนี้

เสนอแก้ด้วย pull request และต้องได้เสียงเห็นชอบตามข้อ 6.3

---

## English summary

**Owner.** TESA Open Knowledge is owned and published by the Thai Embedded Systems Association (TESA), สมาคมสมองกลฝังตัวไทย.
The TESA Qualification Program (TQP) is a joint TESA × Infineon programme. This repository feeds TQP's Skillset Mapping but is
not a certification body. This is governance v0.1 (September 2026).

**Roles.** An **editorial board** of 3–5 people (TESA plus academic course leads) sets direction, approves new courses and
promotions to stable, and owns licences, the skill map and this document. **Infineon** is the joint TQP partner and technical
reviewer: its comments must be recorded and answered, but it has no veto on the board. **Course leads** (one per course, in
[`.github/CODEOWNERS`](.github/CODEOWNERS)) look after their course. Technical and pedagogical **reviewers**, **translators**,
**contributors**, and at least two **community moderators** appointed by the board complete the list. Until the board is appointed,
the repository maintainers in CODEOWNERS act for it. Board members declare conflicts of interest and abstain where they have one.

**Two-key review.** A new lesson or a substantive change needs two reviewers other than the author.
*Technical:* every file in `examples/` and `solution/` is run on a real board, or on the BENTO Emulator for lessons that declare
`hardware.emulator: true`, and the PR records the board, firmware, toolchain (ModusToolbox, MicroPython) or emulator version.
A static check such as `mpy-cross` is not a board test. *Pedagogical:* 2–4 measurable objectives each with a matching check item,
realistic `time_min` (20–75 min in total), prerequisites, skill IDs that exist in `skills/skills.yaml`, clear Thai.
Errata that do not change substance need one approval. Every PR passes `python3 tools/validate.py` and has DCO sign-off.

**Life cycle.** `pre-alpha` (outline) → `alpha` (complete draft, author-tested) → `beta` (two-key reviewed **and piloted by someone
other than the author**) → `stable` (pilot feedback addressed, no serious open errata, board approval).
**Only stable lessons count toward TQP.** Lesson IDs are permanent and never reused.

**Releases.** The curriculum uses CalVer `YYYY.MM`, published as GitHub Releases with Zenodo DOIs (a concept DOI plus one per
version), each pinning the BENTO firmware, ModusToolbox and MicroPython versions tested. `skills/skills.yaml` uses SemVer:
removing or renaming a skill ID (or changing what a level means) is MAJOR; adding skills or roles, or deprecating with
`replaced_by`, is MINOR; wording fixes are PATCH. IDs are never renamed; they are deprecated. Credentials cite both versions,
e.g. "curriculum 2026.10 + skills 1.0.0".

**Decisions.** Lazy consensus on PRs (7 days without a reasoned objection). Disputes go to the board: consensus first, then a
simple majority after 14 days. Licence changes, changes to this document, MAJOR skill-map releases and adding or removing a
catalogue course need two thirds of the board. Board decisions are recorded as public issues labelled `decision`, except matters
of personal data or conduct.

**External material.** In-tree courses live in `courses/`; external courses are registered in `catalog/courses.yaml`, pinned to a
tag or commit with their licence. Infineon code is referenced by link by default; copied files keep their header and licence.
Nothing under NDA enters this repository.

**Open content vs exams.** The **TQP exam item bank lives in a separate private repository.** Quizzes, practice files and
solutions here are public and are never used as live exam items. Certification of persons belongs to a TESA certification unit
kept separate from the editorial board and from course sales (see [tqp/certification.md](tqp/certification.md)).
