---
id: biz.m01.l03
lang: en
title:
  th: ต้นทุน BOM เวลา และทีม
  en: Cost, BOM, time and team
summary:
  th: แยกต้นทุนของผลิตภัณฑ์ IoT เป็นสามก้อน ประมาณต้นทุนต่อชิ้นจากตัวอย่างสมมติ และรู้ว่าต้องมีใครในทีมและต้องถามอะไรก่อนตั้งงบ
  en: Split an IoT product's cost into three parts, estimate cost per unit from a hypothetical example, and know which roles and questions matter before budgeting.
level: L1
time_min: {concept: 15, practise: 10, check: 5}
hardware: {emulator: false, boards: [none]}
prerequisites: [biz.m01.l02]
objectives:
  - th: จำแนกรายการค่าใช้จ่ายเป็นต้นทุนครั้งเดียว (NRE) ต้นทุนต่อชิ้น (BOM และประกอบ) และต้นทุนต่อเนื่อง ได้ถูกอย่างน้อย 5 ใน 6 รายการ
    en: Classify cost items as one-time (NRE), per-unit (BOM and assembly) or recurring, with at least 5 of 6 correct.
  - th: คำนวณต้นทุนต่อชิ้นตลอดอายุการใช้งานจากตัวเลขสมมติที่กำหนด และอธิบายว่าจำนวนผลิตเปลี่ยนผลลัพธ์อย่างไร
    en: Compute lifetime cost per unit from given hypothetical figures and explain how volume changes the result.
  - th: ระบุบทบาทในทีมที่โครงการ Edge AI และ IoT ต้องมี อย่างน้อย 4 บทบาท
    en: Name at least four team roles an edge AI and IoT project needs.
develops:
  - {skill: biz.cost-bom, to: 2}
  - {skill: biz.product-decision, to: 1}
context: {audience: entrepreneur, lang: none, code: none}
status: alpha
translation: done
slides: slides.md
source_sha256: 2871af5cbf2ee0f4a0a1c74939595f4ee18bdb228a396ebf9b1acee66b1ef6d7
---

## Objectives

1. Split cost into three parts: one-time, per-unit and recurring
2. Compute lifetime cost per unit from a hypothetical example
3. Name the team roles needed

> **A note on this lesson** We do not include any market prices or market statistics, because prices change quickly and vary a lot by volume and vendor.
> Every number in the example below is a **hypothetical number**, set to make the arithmetic easy; do not use it as a real price.
> Real prices must be obtained as quotations from vendors and contract manufacturers.

## Before you start

- From the previous lesson, how does the cost of edge differ from cloud?
- If someone asked "how much would this device cost to make?", what do you think you would need to ask back before you could answer?

## See it work first

Many business owners ask the price of the parts on the board and multiply by the quantity to be made, getting a number that looks pleasing.
But that number is usually only one part of the real cost. Development cost, certification testing, cloud cost, SIM card cost, and after-sales support are not in that number at all.
This lesson helps you see all three parts before you set a budget.

## Concepts

### 1. Three cost buckets

| Bucket | English term | Example items |
|---|---|---|
| **One-time** | NRE (non-recurring engineering) | Circuit and PCB design, firmware, an app or dashboard, data collection and model training, an enclosure mould, certification testing |
| **Per-unit** | BOM (bill of materials) + assembly | Chip or module, sensors, PCB, enclosure, power supply or battery, assembly, production-line testing, packaging |
| **Recurring** | recurring | Cloud cost, connectivity (e.g. a SIM card), security updates, customer support, warranty and unit replacement |

AI adds the most cost to the one-time bucket (collecting data, labelling it, training, testing), and also adds to the recurring bucket (maintaining the model as conditions on site change).

### 2. A hypothetical example: a fridge-monitoring sensor

> Every number in this example is hypothetical, not a market price.

Suppose

- One-time cost (NRE) totals **THB 600,000**
- Per-unit cost (BOM + assembly + testing) **THB 900**
- Recurring cost **THB 120 per device per year**
- A **3-year** lifetime per device

**If 1,000 units are made**, lifetime cost per unit = 600,000 / 1,000 + 900 + (120 x 3) = 600 + 900 + 360 = **THB 1,860**

**If 5,000 units are made** = 600,000 / 5,000 + 900 + 360 = 120 + 900 + 360 = **THB 1,380**

Two things to notice. First, as volume increases, the one-time cost is averaged down to a small amount, so the per-unit and recurring costs become the larger parts.
Second, the three-year recurring cost in this example is almost half of the per-unit cost. If you set your selling price while forgetting this bucket, the more you sell, the more you lose.

### 3. Time: four stages you should not skip

1. **Proof of concept** Use a development board to answer one question: "can it really measure and decide?"
2. **Prototype** Closer to the real thing; start thinking about the enclosure, power and safety.
3. **Pilot** Install a small number on the actual site, collect data, and learn what breaks.
4. **Production** Certification testing, and setting up the production line and after-sales support.

The two stages people most often underestimate the time for are collecting real-site data for AI, and certification testing.
Always ask people who have actually done these two stages how long they took.

### 4. The team you need (one person may cover several roles)

- **Product owner** Decides scope and priorities (often you)
- **Hardware** Designs the circuit, the PCB, and chooses parts
- **Firmware** Writes the program on the device
- **Cloud and app** Receives data, stores it, displays it, and sends alerts
- **Data and AI** Collects data, trains and tests the model (only for problems that need AI)
- **Test and compliance** Tests quality and coordinates certification
- **Contract manufacturer (EMS)** Assembles and tests on the production line, once production begins

## Practice

Using the same hypothetical numbers, but changing the lifetime to **5 years** and the volume to **2,000 units**,
compute the lifetime cost per unit and say which bucket is the largest (hint: 600,000 / 2,000 + 900 + 120 x 5).

Then write a list of at least three questions you would ask a vendor or contractor to turn these hypothetical numbers into real ones, for example
"how much does the per-unit price differ at 1,000 versus 5,000 units?", "which parts have only one vendor?", "is certification testing included in the price?"

## Check your understanding

Answer the questions in [quiz.yaml](quiz.yaml). A score of 80% or more passes.

## Going further

The next lesson covers risk and compliance, much of which is cost hidden in the one-time and recurring buckets,
such as radio certification testing cost and the cost of security updates for the whole life of the product.

## Reflect

In your project, which bucket do you know the least about, and who is the first person you should ask?
