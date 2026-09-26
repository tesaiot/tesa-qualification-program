---
id: edgeai-dev.m04.l06
lang: th
title: {th: 'ลงมือทำ: feature vector จากหน้าต่างเลื่อน', en: 'Hands-on: a feature vector from a sliding window'}
summary: {th: เติมห้าจุดใน s10_windowing.py ให้เก็บสัญญาณเข้า buffer คำนวณ mean std และพลังงานต่อย่าน แล้วเลื่อนหน้าต่างให้ซ้อน 50% จนได้ feature vector หกตัวที่ขยับตามการเคลื่อนไหวจริง พร้อมเห็นว่ามันคือหน่วยข้อมูลของ dataset ในโมดูลถัดไป, en: 'Fill five points in s10_windowing.py to buffer the signal, compute mean, std and band energy, and slide the window with 50% overlap, producing a six-value feature vector that follows real motion - the unit of the dataset in the next module.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m04.l05]
objectives:
  - {th: เติมห้าจุดใน practice/s10_windowing.py จนแท่ง feature ทั้งหกขยับ และตัวนับหน้าต่างเพิ่มขึ้นทุก HOP จุด, en: Fill the five points in practice/s10_windowing.py until all six feature bars move and the window counter rises every HOP samples.}
  - {th: วัดและจดค่า std ตอนวางนิ่งเทียบกับตอนเขย่า แล้วอธิบายได้ว่าต่างกันเพราะอะไร, en: 'Measure and record std at rest versus shaking, and explain why they differ.'}
  - {th: 'อธิบายได้ว่าลำดับ mean → std สำคัญอย่างไร และทำไมการลืม buf = buf[-WIN:] ทำให้หน่วยความจำรั่ว', en: 'Explain why the order mean → std matters and why forgetting buf = buf[-WIN:] leaks memory.'}
develops: [{skill: sys.dsp, to: 3}, {skill: lang.micropython, to: 2}, {skill: prog.memory, to: 1}]
assesses: [{skill: sys.dsp, level: 3, evidence: practice/s10_windowing.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 4.6 — ลงมือทำ: feature vector จากหน้าต่างเลื่อน

> โมดูล 4 — วิเคราะห์สัญญาณ · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เติมห้าจุดใน s10_windowing.py ให้เก็บสัญญาณเข้า buffer คำนวณ mean std และพลังงานต่อย่าน แล้วเลื่อนหน้าต่างให้ซ้อน 50% จนได้ feature vector หกตัวที่ขยับตามการเคลื่อนไหวจริง พร้อมเห็นว่ามันคือหน่วยข้อมูลของ dataset ในโมดูลถัดไป

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เติมห้าจุดใน practice/s10_windowing.py จนแท่ง feature ทั้งหกขยับ และตัวนับหน้าต่างเพิ่มขึ้นทุก HOP จุด
2. วัดและจดค่า std ตอนวางนิ่งเทียบกับตอนเขย่า แล้วอธิบายได้ว่าต่างกันเพราะอะไร
3. อธิบายได้ว่าลำดับ mean → std สำคัญอย่างไร และทำไมการลืม buf = buf[-WIN:] ทำให้หน่วยความจำรั่ว

## ก่อนเริ่ม

ผ่านบทเรียน 4.5 มาแล้ว รู้จัก WIN, HOP และ feature หกตัว
เตรียมบันทึกการเรียนไว้จดค่า std ตอนนิ่งกับตอนเขย่า

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/)
- **เรียนมาก่อน:** [บทเรียน 4.5 — feature และหน้าต่าง: สิ่งที่โมเดลเห็นจริง](../l05-features-and-windowing/README.md)

## แนวคิด

ทั้งไฟล์อ่านเป็นประโยคเดียว: เก็บสัญญาณเข้า buffer → พอครบหน้าต่างก็บีบเป็น feature → โชว์เป็นแท่ง → เลื่อนหน้าต่าง → วนต่อ
ห้าจุดที่เติมคือ (1) `buf.append(az)` ในลูปที่อ่าน `sensors.bmi270.motion()` ทีละ HOP จุดโดยหน่วง 20 ms (50 Hz)
(2) `mean = sum(win) / n` (3) `std = math.sqrt(sum((x - mean) ** 2 for x in win) / n)` ต้องมาหลัง mean เสมอเพราะใช้ค่า mean
(4) `band_e.append(sum((x - m) ** 2 for x in s) / len(s))` ในลูปสี่ย่าน และ (5) `buf = buf[-WIN:]` หลังบีบ feature
เพื่อเก็บแค่ WIN จุดท้าย หน้าต่างถัดไปจึงซ้อน 50% ถ้าลืมจุดสุดท้าย buffer จะโตไม่หยุดจนหน่วยความจำหมด

การแสดงผลให้ไว้แล้ว แท่งถูกสเกลแบบหยาบ (`mean` และ `std` คูณ 2 ส่วน band คูณ 0.02) เพียงเพื่อให้ตามองเห็น
`lcd.console` พิมพ์ค่าจริงของ feature vector ควบคู่ ตอนป้อนโมเดลจริงเราจะ normalize อย่างเป็นระบบในโมดูล 5 แต่หลักเดียวกัน
คือทำให้ทุก feature อยู่สเกลใกล้กัน ทุกอย่างเป็น Python ล้วนบน CM33 ไม่ต้องพึ่ง NPU

ความสำเร็จของชุดบทเรียนนี้คือบอกได้ว่าทำไมวางนิ่งแล้ว std ต่ำ และ feature vector นี้จะกลายเป็น dataset ได้อย่างไร
ในโมดูลถัดไปเราจะทำแบบเดียวกันแต่ติด label แล้วเก็บลง CSV เพื่อเอาไปฝึกโมเดลใน TensorFlow

## ตัวอย่างสมบูรณ์

`s10_windowing_full.py` เพิ่มการเน้นย่านที่แรงที่สุด ตัดสิน "นิ่ง" หรือ "ขยับ" จาก std ด้วยเส้นแบ่ง `STD_MOVE` (หน่วย m/s² ปรับได้ตามบอร์ด)
และวัดอัตราหน้าต่างต่อวินาที เป็นตัวอย่างของการจำแนกด้วยกฎบน feature ที่เราสร้างเอง

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/s10_windowing_full.py](examples/s10_windowing_full.py) | feature front-end แบบเห็นภาพ: windowing + feature vector (ฉบับเต็ม) |

## ฝึกเติม

คอมเมนต์ `# เติม:` อยู่ที่บรรทัด 37 (mean), 39 (std), 48 (band energy), 78 (`buf.append`) และ 91 (`buf = buf[-WIN:]`)
แทน `pass` หรือค่า `0.0` ด้วยคำสั่งตามคำใบ้ แล้ววางนิ่งสลับเขย่า ถ้าแท่งไม่ขยับ ตรวจการเยื้องบรรทัดและลำดับ mean → std

| ไฟล์ฝึก | เรื่อง |
|---|---|
| [practice/s10_windowing.py](practice/s10_windowing.py) | โมเดล "เห็น" อะไร: windowing + feature vector (ฉบับฝึกเติมโค้ด) |

## เฉลย

เปิดเฉลยหลังจากลองเองแล้วอย่างน้อยหนึ่งรอบ และอ่าน [วิธีใช้เฉลย](../../README.md#วิธีใช้เฉลย) ก่อน

| เฉลย | คู่กับ |
|---|---|
| [solution/s10_windowing.py](solution/s10_windowing.py) | [practice/s10_windowing.py](practice/s10_windowing.py) |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. รันแล้วแท่งทุกแท่งนิ่งและตัวนับหน้าต่างไม่ขึ้นเลย จุดใดยังว่างมากที่สุด *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) buf.append(az) ทำให้ buffer ไม่เคยครบหน้าต่าง
   - ข) band_e.append(...)
   - ค) buf = buf[-WIN:]
   - ง) std

   <details><summary>เฉลย</summary>

   **ก** — ถ้าไม่เก็บค่าเข้า buffer เงื่อนไข len(buf) >= WIN ไม่มีวันจริง จึงไม่มีการบีบ feature และไม่มีการนับหน้าต่าง

   </details>

2. วางบอร์ดนิ่งแล้ว std ต่ำ แต่เขย่าแล้ว std สูงมาก เพราะอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) เขย่าทำให้ค่าเฉลี่ยของ az สูงขึ้นเสมอ
   - ข) std วัดว่าค่ากระจายห่างจากค่าเฉลี่ยแค่ไหน เขย่าทำให้ az แกว่งไปมารอบค่าเฉลี่ยมาก
   - ค) เซนเซอร์เปลี่ยนหน่วยตอนเขย่า
   - ง) หน้าต่างสั้นลงตอนเขย่า

   <details><summary>เฉลย</summary>

   **ข** — ตอนนิ่งทุกจุดใกล้ค่าเฉลี่ย std จึงเล็ก ตอนเขย่าจุดกระจายห่างค่าเฉลี่ย std จึงใหญ่ เป็นเหตุผลที่ feature สถิติง่าย ๆ แยกท่าทางได้ดี

   </details>

3. ถ้าเขียนบรรทัด std ไว้ก่อนบรรทัด mean ภายใน features() จะเกิดอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) ได้ค่าเท่าเดิม
   - ข) std คำนวณจาก mean = 0.0 ค่าเริ่มต้น จึงผิด (ได้ค่าใกล้ระดับของสัญญาณแทนการแกว่ง)
   - ค) โปรแกรมโยน NameError ทุกครั้ง
   - ง) band energy ผิดแทน

   <details><summary>เฉลย</summary>

   **ข** — std ต้องใช้ mean ที่คำนวณแล้ว ถ้า mean ยังเป็น 0.0 ผลรวม (x − 0)² จะสะท้อนขนาดของสัญญาณ ไม่ใช่การกระจายรอบค่าเฉลี่ย

   </details>

4. ลืมเติม buf = buf[-WIN:] ผลระยะยาวคืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) หน้าต่างไม่ซ้อนกันแต่ทุกอย่างปกติ
   - ข) buffer โตขึ้นเรื่อย ๆ ไม่มีที่สิ้นสุดจนหน่วยความจำหมด
   - ค) feature ทุกตัวเป็นศูนย์
   - ง) อัตราสุ่มเร็วขึ้น

   <details><summary>เฉลย</summary>

   **ข** — features() ยังใช้ buf[-WIN:] จึงดูเหมือนทำงานปกติในช่วงแรก แต่ list ถูกต่อท้ายไม่หยุด เป็น memory leak ที่ทำให้บอร์ดค้างในที่สุด

   </details>

## แล็บ

**MVP ของชุดบทเรียน 4.5–4.6:** สร้าง feature vector จากสัญญาณดิบด้วยมือเอง ตัดหน้าต่าง (window + hop) แล้วบีบเป็น mean, std และ band ที่เปลี่ยนตามการเคลื่อนไหว

- [ ] เติมไฟล์ฝึกครบห้าจุด รันได้บน Emulator หรือบอร์ด
- [ ] วางนิ่งกับเขย่า จดค่า std ทั้งสองกรณีลงบันทึกการเรียน ต่างกันกี่เท่า และเพราะอะไร
- [ ] เปลี่ยน `HOP` เป็นค่าเดียวกับ `WIN` แล้วสังเกตว่าอัตราหน้าต่างเปลี่ยนอย่างไร เสี่ยงพลาดอะไร
- [ ] อธิบายได้ว่า window กับ hop คืออะไร ทำไมต้องซ้อน และ std บอกอะไร

## ไปต่อ

โมดูลถัดไป (Training) เราจะเก็บข้อมูลแบบนี้พร้อม label เป็น dataset จริง แบ่ง train, val, test แล้วฝึกโมเดลของเราเอง

บทเรียนถัดไป: [บทเรียน 5.1 — วิศวกรรมชุดข้อมูล: สมดุลคลาส หน้าต่าง และการแบ่ง train/val/test](../../m05-training/l01-dataset-engineering/README.md)

## สะท้อนคิด

- feature หกตัวนี้พอสำหรับแยก idle, circle และ shaking หรือไม่ ถ้าไม่พอ คุณจะเพิ่ม feature อะไร
- ถ้า band ของคุณแบ่งตามความถี่แทนเวลา ผลที่ได้จะใกล้เคียงอะไรที่โมเดลเสียงใช้
