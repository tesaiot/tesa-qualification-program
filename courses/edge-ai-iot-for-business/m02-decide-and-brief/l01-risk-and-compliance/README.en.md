---
id: biz.m02.l01
lang: en
title:
  th: ความเสี่ยงและการปฏิบัติตามกฎ
  en: Risk and compliance
summary:
  th: รู้จักความเสี่ยงสี่กลุ่มของผลิตภัณฑ์ IoT คือความปลอดภัยไซเบอร์ ข้อมูลส่วนบุคคลตาม PDPA มาตรฐานและการรับรอง และห่วงโซ่อุปทาน พร้อมหน่วยงานที่ต้องตรวจกับเขา
  en: Meet the four risk groups of an IoT product (cyber security, personal data under the PDPA, standards and certification, supply chain) and the agencies to check with.
level: L1
time_min: {concept: 15, practise: 10, check: 5}
hardware: {emulator: false, boards: [none]}
prerequisites: [biz.m01.l03]
objectives:
  - th: ระบุหลักความปลอดภัยพื้นฐานของอุปกรณ์ IoT ได้อย่างน้อย 3 ข้อ และบอกแหล่งอ้างอิงมาตรฐานได้อย่างน้อย 1 แหล่ง
    en: Name at least three basic IoT device security practices and at least one reference standard.
  - th: ตัดสินได้ว่าผลิตภัณฑ์ของตัวเองเก็บข้อมูลส่วนบุคคลหรือข้อมูลอ่อนไหวตาม พ.ร.บ.คุ้มครองข้อมูลส่วนบุคคล พ.ศ. 2562 หรือไม่ และบอกหน่วยงานกำกับได้
    en: Decide whether your product collects personal or sensitive data under Thailand's Personal Data Protection Act B.E. 2562 (2019), and name the regulator.
  - th: จับคู่ลักษณะของผลิตภัณฑ์กับหน่วยงานที่ต้องตรวจเรื่องมาตรฐานหรือการรับรองได้ถูก อย่างน้อย 2 ใน 3 กรณี
    en: Match product characteristics to the agency to check with on standards or certification, with at least 2 of 3 correct.
  - th: ระบุความเสี่ยงด้านห่วงโซ่อุปทานได้อย่างน้อย 2 ข้อ พร้อมวิธีลดความเสี่ยงข้อละหนึ่งวิธี
    en: Name at least two supply-chain risks with one mitigation each.
develops:
  - {skill: biz.risk-compliance, to: 2}
  - {skill: sec.fundamentals, to: 1}
  - {skill: test.standards, to: 1}
context: {audience: entrepreneur, lang: none, code: none, jurisdiction: Thailand}
status: alpha
translation: done
slides: slides.md
source_sha256: aae5951e50d212135eef8516fff003e90444c5c10b2371a69016fa1cea258bd0
---

## Objectives

1. Name the basic security practices for an IoT device and a reference standard
2. Decide whether a product collects personal or sensitive data, and know who regulates it
3. Know which kind of product must be checked with which agency for standards
4. Name supply-chain risks and how to reduce them

> **Please note** This lesson gives an overview to help you ask the right questions; it is not legal advice. Before selling a real product, check directly with the relevant
> agencies and consult a lawyer or an accredited test laboratory. Rules and notices change, so always look at the latest version from the official source.

## Before you start

- From the previous lesson, which cost bucket does certification testing sit in?
- Does your device send or receive radio signals (WiFi, Bluetooth, LoRa, cellular)?

## See it work first

Read these two short stories, then ask yourself which one is more expensive.

**Story one** A company sells home cameras that all share the same default password, with no way to update the firmware. One day, someone finds a way to access every camera from the internet.
**Story two** A company finishes designing a device and orders the first production batch, only to discover that a key part has a single vendor, and that vendor has just announced it is discontinuing it.

Both stories are hypothetical but genuinely possible, and both can be prevented at the design stage at far lower cost than fixing them later.

## Concepts

### 1. Cyber security of the device itself

Several basic principles agree across international IoT standards, for example

- **No identical default password on every unit**
- **Software can be updated safely**, for the whole life of the product, with customers told how long it will be supported
- **Keys and secrets are stored safely**, for example in a secure element, rather than in general-purpose memory
- **Communication is encrypted**, for example with TLS, with both the device and the server authenticated
- **There is a channel to report vulnerabilities**, with someone responsible for responding

References you can use as a framework

- ETSI EN 303 645 V3.1.3 (2024-09) *Cyber Security for Consumer Internet of Things: Baseline Requirements*
  https://www.etsi.org/deliver/etsi_en/303600_303699/303645/03.01.03_60/en_303645v030103p.pdf
- NIST IR 8259 *Foundational Cybersecurity Activities for IoT Device Manufacturers* https://csrc.nist.gov/pubs/ir/8259/final
- OWASP Internet of Things Project https://owasp.org/www-project-internet-of-things/

These standards are European and American, not Thai law, but they make a good checklist, and they are necessary if you plan to export.
If you would like to know how engineers handle these things on a real board, the course [Secure IoT with OPTIGA™ Trust M](../../../secure-iot-optiga/README.md) covers it in detail.

### 2. Personal data under the PDPA

The **Personal Data Protection Act B.E. 2562 (2019)** was published in the Royal Gazette, Volume 136, Part 69 A, on 27 May 2019
([the text from the Royal Gazette](https://www.ratchakitcha.soc.go.th/DATA/PDF/2562/A/069/T_0052.PDF)).
The regulator is the **Office of the Personal Data Protection Committee (PDPC)**, https://www.pdpc.or.th/

Questions you must be able to answer from the design stage

- **Can the data the device collects identify a person?** A face image, a recorded voice, one person's location, or a value tied to a username are usually personal data.
- **Is it sensitive data?** Section 26 names certain categories that need stricter care, such as health data and biometric data. Health devices need particular care here.
- **Are you collecting only what you need?** If the problem only needs to know "is someone in the room", using a sensor that captures no image (such as radar), or processing on the device and sending only the result, reduces how much personal data you need to look after (this is one reason edge, from an earlier lesson, matters).
- **Who is the data controller, and who is the data processor?** If you use another provider's cloud, you need a clear agreement.
- **How long is data kept, how is it deleted, and how are data subjects notified?**

### 3. Standards and certification before you sell

| If your product... | Agency to check with | Official website |
|---|---|---|
| Sends or receives radio signals (WiFi, Bluetooth, LoRa, cellular) | The Office of the National Broadcasting and Telecommunications Commission (NBTC), which checks what certification or filing a device needs before import or sale | https://www.nbtc.go.th/ |
| Is an electrical or electronic appliance that may fall under a Thai Industrial Standard (TIS/มอก.), some of which are mandatory | The Thai Industrial Standards Institute (TISI), Ministry of Industry | https://www.tisi.go.th/ |
| Claims a medical benefit, such as diagnosing or monitoring a disease, including software and AI that may qualify as a medical device | The Medical Device Control Division, Thai Food and Drug Administration (Thai FDA) | https://medical.fda.moph.go.th/samd-head |

Practical advice: ask a test laboratory from the prototype stage what your product needs to be tested for, how long it takes, and whether choosing an already-certified radio module can narrow the scope of testing.
If you plan to export, each country has its own requirements and must be checked separately.

### 4. Supply chain

- **A part has only one vendor** Line up a second source at the design stage.
- **A part is nearing end of life** Ask about the lifecycle status of key parts, and choose versions the manufacturer still supports for the long term.
- **Long lead times** Plan stock for critical parts.
- **Counterfeit parts** Buy from authorised distributors.
- **Provisioning keys and firmware at the factory** If a contract manufacturer is the one loading encryption keys onto the device, agree who holds the keys and how leaks are prevented.

## Practice

Build a **risk register** for your project with at least four rows, one per risk group.

| Group | Risk | Likelihood (low/medium/high) | Impact (low/medium/high) | Mitigation | Owner |
|---|---|---|---|---|---|
| Cyber security | | | | | |
| Personal data | | | | | |
| Standards and certification | | | | | |
| Supply chain | | | | | |

## Check your understanding

Answer the questions in [quiz.yaml](quiz.yaml). A score of 80% or more passes.

## Going further

The risk register from this lesson will be carried into the decision canvas in the final lesson. The next lesson covers build, buy or partner,
which changes who carries each of these risks.

## Reflect

Which risk in your register, if it happened, could never be fixed afterward? That one should be funded first.
