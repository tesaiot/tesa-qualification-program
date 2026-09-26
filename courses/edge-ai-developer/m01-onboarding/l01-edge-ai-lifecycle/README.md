---
id: edgeai-dev.m01.l01
lang: th
title: {th: 'Edge AI คืออะไร: วงจรชีวิตของข้อมูลห้าขั้นและเป้าหมายที่โมเดลไปรันได้', en: 'What edge AI is: the five-stage data lifecycle and where a model can run'}
summary: {th: รู้ว่า Edge AI ต่างจาก AI บนคลาวด์ตรงไหน เห็นวงจรชีวิตของข้อมูลห้าขั้นที่เป็นโครงของทั้งหลักสูตร และรู้ว่าโมเดลตัวเดียวไปรันได้ที่ไหนบ้าง บนบอร์ดที่มีคอร์ควบคุมกับคอร์ AI แยกกัน, en: 'Learn how edge AI differs from cloud AI, see the five-stage data lifecycle that structures the whole course, and where one model can run, on a board with separate control and AI cores.'}
level: L3
time_min: {concept: 45, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: []
objectives:
  - {th: 'อธิบายความต่างระหว่าง Cloud AI กับ Edge AI จากจุดที่การอนุมานเกิดขึ้น และยกเหตุผลที่ควรรันบนอุปกรณ์ได้อย่างน้อยสามข้อจากสี่ข้อ (latency, privacy, cost, offline)', en: 'Explain how cloud AI and edge AI differ by where inference happens, and give at least three of the four reasons to run on the device (latency, privacy, cost, offline).'}
  - {th: เรียงห้าขั้นของวงจรชีวิตข้อมูล DAQ → Processing → Analysis → Training → Apps ได้ถูกลำดับ และบอกได้ว่าแต่ละขั้นตรงกับโมดูลใดของหลักสูตร, en: Put the five lifecycle stages DAQ → Processing → Analysis → Training → Apps in order and name the module of this course that covers each.}
  - {th: 'จับคู่เป้าหมาย MCU, Web, Cortex-A และ PC กับสิ่งที่ต้องทำกับไฟล์ .tflite แบบ int8 และ runtime ที่ใช้ แล้วอธิบายว่าทำไมมีแค่ MCU ที่ต้องผ่าน Vela', en: 'Match the MCU, web, Cortex-A and PC targets to what each does with the int8 .tflite file and the runtime it uses, and explain why only the MCU needs Vela.'}
  - {th: บอกได้ว่าโค้ด MicroPython รันบน Cortex-M33 ส่วนโมเดลรันบน Cortex-M55 กับ Ethos-U55 และเลือกโมเดลจากตารางหกโมเดลให้ตรงกับเซนเซอร์ที่ต้องใช้, en: 'State that MicroPython runs on the Cortex-M33 while models run on the Cortex-M55 with the Ethos-U55, and pick the model from the six-model table that matches a given sensor.'}
develops: [{skill: ai.edge, to: 1}, {skill: ai.model-deploy, to: 1}, {skill: hw.architecture, to: 1}, {skill: biz.product-decision, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 1.1 — Edge AI คืออะไร: วงจรชีวิตของข้อมูลห้าขั้นและเป้าหมายที่โมเดลไปรันได้

> โมดูล 1 — เริ่มต้น: รันของจริงแล้วแกะดูข้างใน · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

รู้ว่า Edge AI ต่างจาก AI บนคลาวด์ตรงไหน เห็นวงจรชีวิตของข้อมูลห้าขั้นที่เป็นโครงของทั้งหลักสูตร และรู้ว่าโมเดลตัวเดียวไปรันได้ที่ไหนบ้าง บนบอร์ดที่มีคอร์ควบคุมกับคอร์ AI แยกกัน

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. อธิบายความต่างระหว่าง Cloud AI กับ Edge AI จากจุดที่การอนุมานเกิดขึ้น และยกเหตุผลที่ควรรันบนอุปกรณ์ได้อย่างน้อยสามข้อจากสี่ข้อ (latency, privacy, cost, offline)
2. เรียงห้าขั้นของวงจรชีวิตข้อมูล DAQ → Processing → Analysis → Training → Apps ได้ถูกลำดับ และบอกได้ว่าแต่ละขั้นตรงกับโมดูลใดของหลักสูตร
3. จับคู่เป้าหมาย MCU, Web, Cortex-A และ PC กับสิ่งที่ต้องทำกับไฟล์ .tflite แบบ int8 และ runtime ที่ใช้ แล้วอธิบายว่าทำไมมีแค่ MCU ที่ต้องผ่าน Vela
4. บอกได้ว่าโค้ด MicroPython รันบน Cortex-M33 ส่วนโมเดลรันบน Cortex-M55 กับ Ethos-U55 และเลือกโมเดลจากตารางหกโมเดลให้ตรงกับเซนเซอร์ที่ต้องใช้

## ก่อนเริ่ม

ไม่ต้องเตรียมอะไรมากสำหรับบทเรียนแรก บทเรียนนี้เป็นแนวคิดล้วน ส่วนการลงมือรันโมเดลอยู่ในบทเรียน 1.2 และ 1.3
ถ้ามีเวลา เปิด [BENTO IDE](https://ide.tesaiot.dev/) ค้างไว้ในอีกแท็บ จะได้เห็นหน้าตาเครื่องมือที่ใช้ตลอดหลักสูตร

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/)

## ดูของจริงก่อน

หลักสูตรนี้สอนแบบ **กลับด้าน** เริ่มจากของที่ทำงานได้จริงก่อน แล้วค่อยแกะว่าข้างในเป็นอย่างไร (แนวทาง PRIMM:
Predict → Run → Investigate → Modify → Make) ชุดบทเรียน 1.1–1.3 จึงพาไปจบที่การรันเมนูหกโมเดลบนบอร์ด
ซึ่งเป็นขั้นที่ 5 ของวงจร ก่อนจะถอยกลับไปสร้างเองตั้งแต่ขั้นที่ 1 ในโมดูลถัด ๆ ไป

## แนวคิด

**Edge AI** คือการรันโมเดล (การอนุมาน หรือ inference) บนอุปกรณ์ตรงที่ข้อมูลเกิด ไม่ต้องส่งข้อมูลดิบไปให้เซิร์ฟเวอร์คิดแทน
ทั้ง Cloud AI และ Edge AI ใช้โมเดลแบบเดียวกันได้ ต่างกันที่การอนุมานเกิดที่ไหน และเหตุผลที่คุ้มจะย้ายมาไว้บนอุปกรณ์มีสี่ข้อ:
หน่วงเวลาต่ำ (latency) ข้อมูลไม่ออกจากเครื่อง (privacy) ไม่มีค่าเซิร์ฟเวอร์ต่อครั้ง (cost) และทำงานได้แม้เน็ตหลุด (offline)
ราคาที่ต้องจ่ายคือโมเดลต้องเล็กและเร็วพอจะอยู่บนชิปเล็ก ๆ ซึ่งเป็นเรื่องที่หลักสูตรนี้สอนตรง ๆ

หลักสูตรเดินตาม **วงจรชีวิตของข้อมูลห้าขั้น** ที่วิศวกรทำจริง: DAQ (เก็บข้อมูลดิบ, โมดูล 2) → Processing
(คณิตและฟิสิกส์, โมดูล 3) → Analysis (DSP, FFT, feature, โมดูล 4) → Training (ฝึกโมเดลใน Docker, โมดูล 5) → Apps
(อนุมานและสั่งการ, โมดูล 6) คอร์ส Edge AI ส่วนใหญ่สอนแค่ขั้นสุดท้าย แต่เราจะเข้าใจด้วยว่าโมเดล "เห็น" อะไร และทำไมต้องบีบให้เล็ก

โมเดลที่ฝึกครั้งเดียวไปรันได้ทั้งสเปกตรัม: **MCU + NPU** (บอร์ด BENTO, ต้องคอมไพล์เพิ่มด้วย Vela เพื่อให้ Ethos-U55 อ่านออก)
**Web** (LiteRT.js ในเบราว์เซอร์) **Cortex-A** (Raspberry Pi, Jetson, mini PC ด้วย ai-edge-litert) และ **PC** ใน Docker
ไฟล์ `.tflite` แบบ int8 คือแหล่งความจริงเดียว เพราะ int8 เป็นตัวหารร่วม: MCU บังคับใช้ ที่เหลือรับได้หมด
เรียนได้จากสามพื้นผิวด้วยโค้ด MicroPython ชุดเดียว คือ BENTO Emulator ในเบราว์เซอร์ บอร์ดจริง และ Python กับ Docker สำหรับฝึกโมเดล

บอร์ดมี "สองสมอง": **Cortex-M55 (400 MHz) กับ Ethos-U55 NPU** เป็นที่รันโมเดล ส่วน **Cortex-M33 (200 MHz)** เป็นคอร์ควบคุม
และเป็นที่รันโค้ด MicroPython ของเรา เวลาเรียก `edge_ai.result()` โค้ดบน M33 จะดึงผลจาก M55 มาผ่านช่องสื่อสารในชิป (IPC)
เฟิร์มแวร์บน TESAIoT Dev Kit มีโมเดล DEEPCRAFT หกตัวพร้อมใช้ (Motion, Baby Cry, Push, Cough, Alarm, Siren) แต่ละตัวผูกกับเซนเซอร์หนึ่งตัว
คือ IMU, ไมโครโฟน หรือเรดาร์ โมเดลเหล่านี้เป็นผลงานของ Imagimob AB บริษัทในเครือ Infineon ที่สร้างด้วย DEEPCRAFT Studio
ส่วน BENTO Emulator มีห้าตัว (ไม่มี Push Detection) ลำดับจึงไม่ตรงกับบอร์ด ให้หาโมเดลจากชื่อเสมอ

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. ข้อใดเป็นเหตุผลที่ควรรันโมเดลบนอุปกรณ์แทนการส่งขึ้นคลาวด์ (เลือกทุกข้อที่ถูก) *(เลือกได้หลายข้อ · เป้าหมายข้อ 1)*
   - ก) ตัดสินใจได้ในเสี้ยววินาทีโดยไม่ต้องรอ round-trip ไปเซิร์ฟเวอร์
   - ข) เสียงและท่าทางดิบไม่ต้องออกจากอุปกรณ์
   - ค) โมเดลบนอุปกรณ์ใหญ่และแม่นกว่าโมเดลบนคลาวด์เสมอ
   - ง) อุปกรณ์ยังตัดสินใจได้แม้เน็ตหลุด

   <details><summary>เฉลย</summary>

   **ก, ข, ง** — สี่เหตุผลในสไลด์คือ latency, privacy, cost และ offline ส่วนขนาดกลับเป็นข้อแลกเปลี่ยนของ Edge คือโมเดลต้องเล็กพอจะรันบนชิปเล็ก ๆ ไม่ได้ใหญ่กว่าคลาวด์

   </details>

2. เรียงขั้นของวงจรชีวิตข้อมูลตามลำดับที่หลักสูตรนี้เดิน *(เรียงลำดับ · เป้าหมายข้อ 2)*
   - ก) Training: ฝึกโมเดลแล้วส่งออกเป็น .tflite
   - ข) DAQ: เก็บข้อมูลดิบจากเซนเซอร์
   - ค) Apps: อนุมานแล้วสั่งการ
   - ง) Analysis: DSP, FFT และ feature
   - จ) Processing: คณิตและฟิสิกส์

   <details><summary>เฉลย</summary>

   **ข → จ → ง → ก → ค** — DAQ → Processing → Analysis → Training → Apps ตรงกับโมดูล 2 ถึง 6 ชุดบทเรียนแรกเริ่มที่ Apps ก่อนโดยตั้งใจ แต่วงจรจริงเริ่มจากข้อมูล

   </details>

3. ไฟล์ model_int8.tflite ไฟล์เดียวจะไปรันหลายเป้าหมาย เป้าหมายใดต้องผ่านขั้นคอมไพล์เพิ่ม *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) เบราว์เซอร์ที่ใช้ LiteRT.js
   - ข) บอร์ด MCU ที่มี Ethos-U55 ต้องผ่าน Vela ก่อน
   - ค) Raspberry Pi ที่ใช้ ai-edge-litert
   - ง) PC ใน Docker

   <details><summary>เฉลย</summary>

   **ข** — Vela แปลงส่วนของกราฟให้ NPU Ethos-U55 อ่านออก เป้าหมายอื่นใช้ไฟล์ int8 เดิมได้เลย int8 จึงเป็นตัวหารร่วมของทุกเป้าหมาย

   </details>

4. เมื่อโค้ด MicroPython เรียก edge_ai.result() สิ่งใดเกิดขึ้น *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) Cortex-M33 รันโมเดลเองแล้วคืนคำตอบ
   - ข) โค้ดบน Cortex-M33 ดึงผลอนุมานล่าสุดที่ Cortex-M55 กับ Ethos-U55 คำนวณไว้ผ่าน IPC
   - ค) บอร์ดส่งข้อมูลขึ้นคลาวด์แล้วรอคำตอบ
   - ง) Ethos-U55 รันโค้ด Python แทน M33

   <details><summary>เฉลย</summary>

   **ข** — โมเดลอนุมานบน M55 และ NPU ส่วน MicroPython อยู่บน M33 การเรียก result() คือการดึง (pull) ผลข้ามคอร์ผ่านช่องสื่อสารในชิป

   </details>

5. อยากตรวจว่ามีคนยื่นมือเข้าหาบอร์ดโดยไม่ใช้กล้องและไม่ใช้เสียง ควรเลือกโมเดลใดบน TESAIoT Dev Kit *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) Motion Detection (IMU)
   - ข) Cough Detection (MIC)
   - ค) Push Detection (RADAR)
   - ง) Siren Detection (MIC)

   <details><summary>เฉลย</summary>

   **ค** — Push Detection ใช้เรดาร์ 60 GHz จึงตรวจการยื่นมือได้โดยไม่ใช้กล้อง โมเดลนี้มีเฉพาะบนบอร์ดที่มีเรดาร์ บน BENTO Emulator จะไม่เห็นในรายชื่อ

   </details>

## ไปต่อ

บทเรียนถัดไปเราจะรู้จักโมดูล `edge_ai` สี่คำสั่งที่พาเราจากทะเบียนโมเดลไปถึงคำตอบบนจอ

บทเรียนถัดไป: [บทเรียน 1.2 — โมดูล edge_ai: ถามทะเบียนโมเดล เลือก แล้วอ่านคำตอบ](../l02-edge-ai-module/README.md)

## สะท้อนคิด

- งานในบ้านหรือที่ทำงานของคุณงานไหนบ้างที่ "ต้องตอบทันที" หรือ "ข้อมูลไม่ควรออกจากเครื่อง" จนควรเป็น Edge AI
- ถ้าโมเดลตัวหนึ่งรันได้ทั้งบนชิปราคาถูกและบน Jetson คุณจะใช้เกณฑ์อะไรเลือกว่ามันควรอยู่ที่ไหน
