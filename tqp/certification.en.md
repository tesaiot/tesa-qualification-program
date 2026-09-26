# TQP credentials (TESA Qualification Program)

> **Status: design v0.1 — not yet open for candidates.**
> None of the credentials on this page can be applied for or examined today. Names, criteria, validity and procedures may all
> change before launch. Each tier will be announced here and in [CHANGELOG.md](../CHANGELOG.md) when it opens.

*Thai (source): [certification.md](certification.md)*

The TESA Qualification Program (TQP) is a **joint programme of the Thai Embedded Systems Association (TESA) and Infineon**.
TESA Open Knowledge is open content anyone can learn from for free. TQP credentials are an assessment kept separate from that
content, run by a certification unit that is separate from the content team and from course sales. Levels are defined in
[levels.en.md](levels.en.md).

## Tiers

| Tier | Name (draft) | What it says | Assessment | Identity check | Open Badges 3.0 type | Validity | Issuer |
|---|---|---|---|---|---|---|---|
| **T0** | Open Knowledge Completion | The holder completed lessons or a course. **Not a certification of competence.** | End-of-lesson checks and auto-graded labs; only `stable` lessons count | None | `CertificateOfCompletion` | No expiry; states the curriculum version | TESA |
| **T1** | TQP Skill Certificate, per skill cluster (e.g. C, peripherals, communication, MQTT, OPTIGA™ security, Edge AI) | The holder passed an assessment of one cluster on the exam date | Online knowledge exam plus a randomised practical task on a real board | Online proctoring with ID check | `Certificate` or `MicroCredential` | Not renewed; states the versions examined | TESA × Infineon |
| **T2** | TQP Certified Embedded Developer | Competence at L4 ≈ TPQI Embedded Systems Developer level 4 | Knowledge exam plus a proctored practical on PSOC™ Edge E84 at a test centre or remote lab | ID check on site or remotely | `Certification` with `validUntil` | 3 years; renew with continuing-education credits or re-examination | TESA × Infineon |
| **T3** | TQP Professional / Specialist (Secure IoT, Edge AI) | Competence at L5 ≈ TPQI level 5 in a specialism | Capstone project plus a panel interview with external examiners | ID check on site | `Certification` | 3 years | TESA × Infineon |
| **Trainer** | TQP Certified Trainer | May teach TQP-aligned courses | Holds an L4 credential in what they teach, completes a pedagogy course, and gives an observed teaching demonstration | ID check | `Certification` | 2 years | TESA × Infineon |

**Use the right words.** T0 is a record of completion; T1 is an assessment-based certificate that is not renewed; T2, T3 and
Trainer are certifications, with validity and renewal. Never call T0 or T1 a "certification".
**T0** carries the statement: "This records completion of learning. It is not a certification of competence by TESA or Infineon."

## Joint TESA × Infineon issuance

- T1, T2, T3 and Trainer credentials are issued jointly under **"Certified by TESA and Infineon"**.
- TESA is the issuer; Infineon endorses the definition of each credential, so anyone can verify that both parties stand behind it.
- Infineon co-designs the content and the exam blueprints and supports test centres with hardware.
- Each candidate's result is decided by the criteria and process agreed in the scheme, the same for everyone, with no decisions
  outside that process.
- Holders' use of "Certified by TESA and Infineon" is governed by [TRADEMARKS.md](../TRADEMARKS.md).

## Open and closed

| Public | Closed (in a separate private repository) |
|---|---|
| The skill map [skills/](../skills/) and role profiles | The exam item bank |
| Exam blueprints with section weights | The parameters that generate each candidate's task |
| Exam objectives | Hidden test vectors |
| Sample items | Grader internals |
| Practice labs and practical-task templates | |
| Scoring rubrics | |

Quizzes, practice files and solutions in TESA Open Knowledge are learning material and are never used as live exam items.

## Practical exams

- **Randomised per candidate:** pins, I²C addresses, sample rates, MQTT topics and injected faults to find.
- **Graded automatically on real hardware.** Proctors supervise but do not score.
- **Exam development:** a job task survey with companies, objectives published for community comment, item-writing workshops, a
  beta exam, a modified-Angoff study to set the cut score, and item analysis after use.
- **An idea not yet validated:** the OPTIGA™ Trust M on a registered exam board signs the result, proving it came from real hardware.

## Digital credential format

- **Open Badges 3.0**, built on **W3C Verifiable Credentials 2.0**.
- Issued from a `did:web` identifier on a domain TESA controls. TESA holds its own signing keys, so it can change issuing platform
  and existing credentials still verify.
- Revocation through a Bitstring Status List.
- Infineon issues an EndorsementCredential bound to each credential definition.
- A PDF with a QR code for human readers.
- Each credential aligns to skills at their permanent pages `/skills/<id>/` and levels, and to TPQI units where applicable.
- Both versions assessed are stated, e.g. "curriculum 2026.10 + skills 1.0.0".
- T1 carries every element of a micro-credential listed in the 2022 EU Recommendation.
- A CLR 2.0 transcript lets universities use the record as evidence under Thailand's credit-bank rules.

## Validity and renewal

- T0 and T1 do not expire, but always state the curriculum and skill-map versions assessed.
- T2 and T3 are valid for 3 years and are renewed with continuing-education credits or re-examination; the credit rules will be set
  in the scheme.
- Trainer is valid for 2 years.
- Once a credential expires or is revoked, the holder stops using its name and "Certified by TESA and Infineon".

## Impartiality

Offering training and certification in the same organisation is a threat to impartiality (the ISO/IEC 17024 principle). TQP is
designed around that from the start:

- **The TESA Certification Board** has its own charter and is separated, in writing and in process and information, from the
  TESA Open Knowledge editorial board and from TESA's course sales.
- **The scheme committee** includes employers, academics, Infineon, other vendors or users and a public member, with no party in
  the majority.
- **No TESA course is required**, and equivalent routes are accepted, such as Infineon Academy courses, university courses or work
  experience. Taking any course does not make the exam easier or cheaper.
- **Eligibility does not depend on TESA membership.**
- **Trainers do not examine people they trained** within 2 years, and all board and committee members declare conflicts of interest.
- ISO/IEC 17024 practice is followed from the start, with accreditation through Thailand's TISI to be sought later.

## Appeals and complaints

- A candidate may appeal a result in writing within 30 days of being notified.
- Appeals are heard by people who had no part in the original decision.
- The time limit for the reply, and the channel for other complaints, will be fixed in the scheme before the first exam.

## Personal data

- Handled under Thailand's Personal Data Protection Act (PDPA); exam records are kept for at least 6 years.
- Credential data belongs to the holder, who chooses whom to share it with.
- Results are shared with Infineon or employers only with the candidate's explicit consent each time.

## Route to TPQI

TPQI's Embedded Systems Developer qualifications at levels 4 and 5 have no certifying body yet. TESA plans to apply to become the
certifying body for level 4 once it has T1 and T2 exam data. Until TPQI recognises TESA, a TQP credential is not a TPQI
professional-qualification certificate.

## Planned phases (subject to change)

| Phase | Planned period | What happens |
|---|---|---|
| 0 Foundations | Oct–Nov 2026 | Charter and impartiality statement, working details agreed with Infineon, skill map v0.1 |
| 1 Pilot | Dec 2026–Mar 2027 | Pilot courses, first T0 |
| 2 Close the gaps | Apr–Sep 2027 | T1 pilot in 3–4 skill clusters, job task survey with member companies, educator programme |
| 3 National | Oct 2027 onward | T2 opens, application to TPQI, accreditation, T3 |

Until a tier is announced as open on this page, it is not open for candidates.
