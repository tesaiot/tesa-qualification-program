---
id: biz.m01.l02
lang: en
title:
  th: Edge, Cloud หรือ Hybrid
  en: Edge, cloud or hybrid
summary:
  th: เปรียบเทียบการประมวลผลบนอุปกรณ์ บนคลาวด์ และแบบผสม ในสี่มิติ คือความหน่วง ความเป็นส่วนตัว ต้นทุน และการเชื่อมต่อ แล้วเลือกให้เหมาะกับโจทย์
  en: Compare on-device, cloud and hybrid processing on latency, privacy, cost and connectivity, and choose what fits the problem.
level: L1
time_min: {concept: 15, practise: 10, check: 5}
hardware: {emulator: false, boards: [none]}
prerequisites: [biz.m01.l01]
objectives:
  - th: เปรียบเทียบ edge, cloud และ hybrid ได้ครบสี่มิติ คือความหน่วง ความเป็นส่วนตัว ต้นทุน และการเชื่อมต่อ
    en: Compare edge, cloud and hybrid on all four dimensions of latency, privacy, cost and connectivity.
  - th: เลือกสถาปัตยกรรมให้กรณีตัวอย่างพร้อมเหตุผลที่อ้างถึงอย่างน้อย 2 มิติ
    en: Choose an architecture for a case and justify it with at least two dimensions.
  - th: ระบุคำถามที่ต้องถามทีมเทคนิคก่อนเลือกสถาปัตยกรรมได้อย่างน้อย 3 ข้อ
    en: List at least three questions to ask the technical team before choosing an architecture.
develops:
  - {skill: biz.product-decision, to: 2}
  - {skill: ai.edge, to: 1}
  - {skill: iot.fundamentals, to: 2}
context: {audience: entrepreneur, lang: none, code: none}
status: alpha
translation: done
slides: slides.md
source_sha256: 698325c80ddec07f45441115e2787401473a602630a92700a88b03fec4d01cba
---

## Objectives

1. Compare edge, cloud and hybrid on all four dimensions
2. Choose an architecture for a case, with a reason
3. List the questions to ask the technical team before choosing

## Before you start

- From the previous lesson, what were the three steps before you talk about AI?
- How fast does your problem need to respond: within a fraction of a second, within a minute, or is tomorrow morning still fine?

## See it work first

Think of two kinds of doorbell camera. The first sends video all day up to the cloud, for a server elsewhere to check whether anyone walked past.
The second checks it itself, inside the camera, and only sends up a short message: "someone at the door at 14:05", along with a picture from just that moment.

Both give the user a similar-looking result, but they differ a lot in how much data must be sent, how much personal data leaves the house, and what happens when the internet drops.
The first is **cloud**, the second is **edge**, and if it also sends a summary up to the cloud to build a combined report, that is **hybrid**.

## Concepts

### 1. Three choices

- **Edge** The device measures and decides for itself, sending out only the result or the event.
- **Cloud** The device measures and sends the raw data up, letting a server think on its behalf.
- **Hybrid** The device decides urgent matters itself, then sends a summary up to the cloud for an overview, a history, and improving the next round of the model. Most real projects end up here.

### 2. Four dimensions to compare on

| Dimension | Edge | Cloud | A question that helps decide |
|---|---|---|---|
| **Latency** | Responds immediately, without waiting on the network | Must wait for a round trip; faster or slower depending on the network that day | Would it hurt if it were two seconds slower? |
| **Privacy** | Raw data, such as audio or video, never has to leave the device | Raw data is sent and stored elsewhere, and must be handled under the law | Can this data identify a person? |
| **Cost** | Each device is more expensive and harder to develop, but the monthly cost of transmission and processing is low | Devices are cheaper, but there is a continuous cloud and data-transfer cost that scales with volume | How many devices, and for how many years? |
| **Connectivity** | Keeps working even if the internet drops | Losing the internet means the thinking stops | Is the signal on site stable? |

Two more things are often forgotten. **Updates** (a cloud model can be changed in one place; a model on the device needs a safe remote-update system),
and **power** (a battery-powered device must choose between spending its power on thinking or on transmitting).

### 3. Reading the table well

No choice wins on every dimension. Your job is to say which dimension matters most for this problem, and accept paying more on the dimensions that matter less.
For example, a fall-detection system for the elderly cares most about privacy and latency, so it leans towards edge.
A monthly building energy-usage summary report barely cares about latency, so cloud is simpler and better value.

## Practice

Choose an option for these three cases, and write a reason that refers to at least two dimensions.

| Case | Edge / Cloud / Hybrid | Reason (at least 2 dimensions) |
|---|---|---|
| A durian orchard on a hillside, with intermittent mobile signal, that must trigger a water pump based on soil moisture | | |
| A retail chain with 200 branches that wants to compare weekly footfall | | |
| A fruit-sorting conveyor that must flick out bad pieces within a fraction of a second, and also wants daily reject statistics | | |

## Check your understanding

Answer the questions in [quiz.yaml](quiz.yaml). A score of 80% or more passes.

## Going further

Questions you should ask the technical team or a contractor before agreeing on an architecture.

1. If the internet drops for a day, what can the system still do, and is data from that period lost?
2. What raw data leaves the device, where does it go, and for how long is it kept?
3. Roughly what is the monthly cost per device, and what does it depend on?
4. If the model or firmware needs a fix, how will devices out in the field be updated, and how safe is that process?

## Reflect

Should your problem from the previous lesson be edge, cloud, or hybrid? Which dimension is what led you to that decision?
