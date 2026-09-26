# บันทึกการเปลี่ยนแปลง (Changelog)

รุ่นของคลังความรู้ใช้ CalVer `YYYY.MM` ส่วนแผนที่ทักษะ `skills/skills.yaml` ใช้ SemVer แยกต่างหาก
(ดู [GOVERNANCE.md](GOVERNANCE.md)) รูปแบบบันทึกอิงตาม [Keep a Changelog](https://keepachangelog.com/)

Releases use CalVer `YYYY.MM`; the skill map `skills/skills.yaml` has its own SemVer (see [GOVERNANCE.md](GOVERNANCE.md)).
The format follows [Keep a Changelog](https://keepachangelog.com/).

## Unreleased

## 2026.09 — 2026-09-25

รุ่นแรกของ TESA Open Knowledge / First release.

### เพิ่ม (Added)

- โครงสร้าง repository และแคตาล็อกหลักสูตร `catalog/courses.yaml` (หลักสูตรในคลัง 11 หลักสูตร และหลักสูตรภายนอก 1 หลักสูตร)
  สถานะของแต่ละหลักสูตรตามวงจรชีวิต pre-alpha / alpha / beta / stable ระบุไว้ในแคตาล็อก
  / Repository layout and course catalogue (11 in-tree courses, 1 external), each with its life-cycle status.
- แผนที่ทักษะ `skills/skills.yaml` เวอร์ชัน 0.1.0: 127 ทักษะ ใน 24 กลุ่ม 6 ด้าน ดัดแปลงจาก Embedded Systems Engineering Roadmap
  ของ Meysam Parvizi (CC BY-SA 4.0) พร้อมโปรไฟล์บทบาท 6 แบบใน `skills/roles/`
  / Skill map 0.1.0 (127 skills, 24 groups, 6 areas) adapted from Meysam Parvizi's roadmap, plus six role profiles.
- ระดับ L1–L5 ที่ตัวเลขตรงกับคุณวุฒิวิชาชีพของ TPQI (`tqp/levels.md`) และการออกแบบใบรับรอง TQP ฉบับ v0.1
  (`tqp/certification.md`) ซึ่ง **ยังไม่เปิดรับผู้สมัครสอบ**
  / Levels L1–L5 aligned with TPQI numbering, and the TQP credential design v0.1 — **not yet open for candidates**.
- เอกสารธรรมาภิบาลและสัญญาอนุญาต: LICENSE, LICENSES/, NOTICE, NOTICE.md, ATTRIBUTION.md, TRADEMARKS.md, GOVERNANCE.md,
  SECURITY.md, CONTRIBUTING, CODE_OF_CONDUCT (Contributor Covenant 3.0 พร้อมฉบับแปลไทย), CITATION.cff
  / Governance and licensing documents, including a Thai translation of Contributor Covenant 3.0.
- อภิธานศัพท์ไทย–อังกฤษ `glossary/terms.yaml`, แม่แบบหลักสูตร โมดูล และบทเรียนใน `templates/` และคู่มือผู้เขียน
  `templates/AUTHORING.md` / Thai–English glossary, course/module/lesson templates and the authoring guide.
- แม่แบบ issue และ pull request ใน `.github/` / Issue forms and the pull-request template.
