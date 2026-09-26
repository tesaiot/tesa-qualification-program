# TQP levels L1–L5

> **Status: design v0.1 — not yet open for candidates.**
> These levels already describe lessons, courses and skills today. The credentials tied to them (see
> [certification.en.md](certification.en.md)) cannot be obtained by anyone yet.

*Thai (source): [levels.md](levels.md)*

TESA Open Knowledge and the TESA Qualification Program (TQP) use one scale everywhere: for lessons, courses, the skills in
[skills/skills.yaml](../skills/skills.yaml) and credentials. **The level numbers match the professional-qualification levels of
Thailand's Professional Qualification Institute (TPQI)**, so an employer who sees "TQP L4" can relate it to TPQI level 4 at once.

## The levels

| Level | What the person can do | Revised Bloom | TPQI / NQF anchor | How it is evidenced |
|---|---|---|---|---|
| **L1 Aware** (รู้จัก) | Explain the concept in their own words and run the examples provided | Remember / Understand | — | End-of-lesson check at 80% or more, and the examples run |
| **L2 Guided** (ทำตามแนวทาง) | Modify or complete code on a given scaffold until it works | Apply (with scaffolding) | PQ 2–3 | Working practice (fill-in) files and the lesson checks |
| **L3 Independent** (ทำได้เอง) | Build something to a clear specification on their own, without a scaffold | Apply / Analyse | PQ 3 | Labs and a capstone with evidence (logs, photos, video) in a portfolio; the T1 exam |
| **L4 Professional** (มืออาชีพ) | Develop, test and fix a real system end to end, including with real test instruments | Analyse / Evaluate | TPQI Embedded Systems Developer level 4 (PQ 4) | T2 knowledge exam and practical exam on a real board |
| **L5 Design & Lead** (ออกแบบและนำทีม) | Design hardware and software architecture, make engineering trade-offs and coach others | Evaluate / Create | TPQI Embedded Systems Developer level 5 (PQ 5) | Capstone project and a panel interview with external examiners (T3) |

The anchors are best-fit, not formal equivalence. Per the Thailand AQRF Referencing Report (2020), professional-qualification
(PQ) levels are comparable with the national qualifications framework (NQF) on a level-to-level basis.

## The TPQI qualifications used as anchors

From the TPQI qualification database (checked September 2026):

| Qualification | Units of competence | Certifying bodies |
|---|---|---|
| [Digital industry, hardware branch, Embedded Systems Developer (นักพัฒนาระบบสมองกลฝังตัว) level 4](https://tpqi-net.tpqi.go.th/qualifications/2865) | ICT-CSOS-107B develop embedded hardware · ICT-FYNH-108B develop embedded software | None |
| [Digital industry, hardware branch, Embedded Systems Developer level 5](https://tpqi-net.tpqi.go.th/qualifications/2866) | ICT-SYMB-109B design the architecture · ICT-QOVE-110B design the hardware · ICT-KOTT-111B design the software, of embedded systems | None |
| [Software and applications branch, IoT Software Developer (นักพัฒนาซอฟต์แวร์เพื่ออินเตอร์เน็ตของสรรพสิ่ง) level 4](https://tpqi-net.tpqi.go.th/qualifications/2850) | 4 units (ICT-OYJA-038B, ICT-ZVDR-048B, ICT-RVUJ-052B, ICT-RZPO-054B) | Yes (anchor for the IoT device developer profile) |

**A TQP credential is not a TPQI professional-qualification certificate.** TQP reuses the level numbers only to make comparison
easy. TPQI certificates are issued by bodies TPQI recognises, and none exists yet for the Embedded Systems Developer occupation.
TESA plans to apply to become one once it has T1 and T2 exam data (see [certification.en.md](certification.en.md)).

## Using the levels

- **A lesson's or course's level** (`level: L2`) is the level it teaches at. **`develops: [{skill, to}]`** says how far a lesson
  takes a skill, and **`assesses: [{skill, level, evidence}]`** says at what level it assesses a skill and with which evidence.
- **L1–L3 can be developed entirely in TESA Open Knowledge** through lessons, practice, labs and capstones.
- **L4–L5 need evidence from controlled assessment** (T2, T3). Finishing lessons alone never yields L4 or L5.
- **An L4 role does not need every skill at L4.** The role profiles in [skills/roles/](../skills/roles/) set a minimum level per
  skill (mostly L3); the role's L4 is shown by integrating those skills into a working system in the practical exam.
- **Only `stable` lessons count toward TQP** (see [GOVERNANCE.md](../GOVERNANCE.md)).

## Other frameworks, used internally

SFIA 9 and the e-CF (EN 16234-1) measure the level of responsibility someone holds at work, not topic knowledge. We use them as
internal reference points only and do not publish a SFIA mapping as part of any credential, because that requires a licence from
the SFIA Foundation.
