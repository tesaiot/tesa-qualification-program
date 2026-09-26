---
id: biz.m02.l02
lang: en
title:
  th: ทำเอง ซื้อ หรือหาพันธมิตร
  en: Build, buy or partner
summary:
  th: ชั่งน้ำหนักระหว่างทำเอง ซื้อของสำเร็จ หรือหาพันธมิตร ด้วยปัจจัยหกข้อ และรู้คำถามที่ต้องตกลงให้ชัดก่อนเซ็นสัญญากับผู้รับจ้าง
  en: Weigh building in-house, buying off the shelf or partnering against six factors, and know what to settle before signing with a contractor.
level: L1
time_min: {concept: 15, practise: 10, check: 5}
hardware: {emulator: false, boards: [none]}
prerequisites: [biz.m02.l01]
objectives:
  - th: อธิบายข้อดีและข้อเสียของการทำเอง ซื้อ และหาพันธมิตร ได้อย่างน้อยทางละ 1 ข้อ
    en: Explain at least one advantage and one drawback each of building, buying and partnering.
  - th: ให้คะแนนทางเลือกด้วยตารางถ่วงน้ำหนักหกปัจจัย แล้วเลือกทางเลือกพร้อมเหตุผล
    en: Score the options with a six-factor weighted table and choose one with a reason.
  - th: ระบุเรื่องที่ต้องตกลงกับพันธมิตรหรือผู้รับจ้างก่อนเซ็นสัญญา อย่างน้อย 4 เรื่อง
    en: List at least four things to settle with a partner or contractor before signing.
develops:
  - {skill: biz.product-decision, to: 2}
  - {skill: biz.cost-bom, to: 2}
context: {audience: entrepreneur, lang: none, code: none}
status: alpha
translation: done
source_sha256: 67f5a4f733bc01b99388540316484ff61ee86a4d5439b38852ee8c8bcdb9e084
---

## Objectives

1. Explain the advantages and drawbacks of the three options
2. Score the options with a weighted table and choose one, with a reason
3. Know what to settle with a partner before signing

## Before you start

- From the previous lesson, which risk in your project can never be fixed later?
- Does your team already have someone who does hardware, firmware or AI?

## See it work first

Three coffee shops want to know when their espresso machine starts acting up.

- **The first shop buys** an off-the-shelf machine-monitoring device with a monthly service; it starts fast, but nothing can be customised, and the data sits in the vendor's system.
- **The second shop builds it themselves**, hiring engineers to develop the whole system; it fits exactly what they want, but takes a long time, and they must maintain it themselves forever.
- **The third shop finds a partner**, using an existing radio module and IoT platform, and hiring a design company to build only the part that is the shop's own know-how.

No shop is wrong. Each chose based on what matters most to them. This lesson helps you choose with reasons you can explain to others.

## Concepts

### 1. Three options, and a mix

| Option | Advantage | Drawback |
|---|---|---|
| **Buy** an off-the-shelf product or service | Fast, low technical risk | Little room to customise, dependent on the vendor, data may not be in your hands |
| **Build it yourself** | Exactly matches your needs, full ownership of the intellectual property and the data | Slow and expensive at first, needs a team and long-term maintenance of your own |
| **Partner** with a design house, contract manufacturer, or academic institution | Get expertise without building a full team | Must manage the contract, ownership, and handover carefully |

Many real projects are a **mix**: buy an already-certified radio module, use an existing IoT platform, and build only the part that is your business's own point of difference.

### 2. Six factors to weigh

1. **Is this a point of business difference?** If this part is the reason customers choose you, you should own it. If not, you can buy it.
2. **How fast must it be done?**
3. **Does the team already have the ability?**
4. **The volume to be made and used** The more units, the more worthwhile building it yourself becomes (recall averaging NRE from the cost lesson).
5. **Who owns the intellectual property and the data?**
6. **Who maintains it long-term**, including security updates for the whole life of the product?

### 3. Things to settle before signing with a partner

- **Ownership** Who owns the circuit design, the source code, the model, and the data collected.
- **Handover** Will you receive the source code, design files, and enough documentation for another team to maintain it?
- **Keys and signing** Who holds the keys used to sign firmware and the device's encryption keys.
- **Updates and security** Who issues updates, for how many years, and at what cost.
- **Standards certification** Who is responsible for submitting tests and fixing issues if it fails.
- **Warranty and contract termination** If the partner goes out of business, can your product still keep running?

TESA has a network of member companies, academic institutions, and training courses that can help your team grow.
If you choose to build it yourself or build it together, your development team can continue learning from courses on the developer pathway of TESA Open Knowledge.

## Practice

Score the three options for your project. Give each factor a weight based on importance (totalling 100), and score each cell 1–5.
Total score = the sum of weight x score.

| Factor | Weight | Buy | Build | Partner |
|---|---|---|---|---|
| Point of business difference | | | | |
| Speed | | | | |
| Team capability | | | | |
| Production volume | | | | |
| Ownership | | | | |
| Long-term maintenance | | | | |
| **Total** | 100 | | | |

The numbers in this table are not the answer. They help show what you value. If the result feels wrong, go back and check whether the weights really match what you think.

## Check your understanding

Answer the questions in [quiz.yaml](quiz.yaml). A score of 80% or more passes.

## Going further

The final lesson brings everything you have done together — the problem, the architecture, the cost, the risks, and this choice — into a one-page decision canvas.

## Reflect

If the partner you chose disappeared tomorrow, what part of your product would still be in your own hands?
