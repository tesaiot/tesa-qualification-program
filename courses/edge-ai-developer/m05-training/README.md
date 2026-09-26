# โมดูล 5 — ฝึกโมเดลและนำไปใช้หลายเป้าหมาย

> Training and deploying to several targets · [หน้าหลักสูตร](../README.md)

เตรียม dataset ที่สมดุล ฝึกโมเดลของเราเองใน Docker บีบเป็น int8 แล้วพาไฟล์เดียวไปรันบนเว็บ Cortex-A และ MCU ผ่าน Vela พร้อมวัด parity

## เป้าหมายของโมดูล

สร้างโมเดลของตัวเองตั้งแต่ข้อมูลจนถึงชิป และวัดให้ได้ว่าแต่ละเป้าหมายแลกอะไรกับอะไร

## บทเรียน

| บทเรียน | เรื่อง | เวลา (นาที) | สไลด์ |
|---|---|---|---|
| [5.1](l01-dataset-engineering/README.md) | วิศวกรรมชุดข้อมูล: สมดุลคลาส หน้าต่าง และการแบ่ง train/val/test | 65 | [slides.md](l01-dataset-engineering/slides.md) |
| [5.2](l02-dataset-lab/README.md) | ลงมือทำ: เก็บ dataset ที่สมดุลบนบอร์ดแล้วแบ่งบน PC | 75 | [slides.md](l02-dataset-lab/slides.md) |
| [5.3](l03-training-pipeline/README.md) | ฝึกโมเดลใน Docker: หนึ่งชิ้นงาน สี่เป้าหมาย | 65 | [slides.md](l03-training-pipeline/slides.md) |
| [5.4](l04-inside-training/README.md) | ข้างในการฝึก: Keras, Conv1D, gradient descent, int8 และ confusion matrix | 70 | [slides.md](l04-inside-training/slides.md) |
| [5.5](l05-train-lab/README.md) | ลงมือทำ: เติมสคริปต์ฝึกแล้วรันใน Docker | 75 | [slides.md](l05-train-lab/slides.md) |
| [5.6](l06-web-runtime/README.md) | รันโมเดลบนเว็บ: LiteRT.js, int8 I/O และ parity | 70 | [slides.md](l06-web-runtime/slides.md) |
| [5.7](l07-web-parity-lab/README.md) | ลงมือทำ: verdict บนเว็บให้ตรงกับ PC และเรื่องราว Cortex-A | 75 | [slides.md](l07-web-parity-lab/slides.md) |
| [5.8](l08-quantize-and-vela/README.md) | quantize และ Vela: เอาโมเดลของเราขึ้น Ethos-U55 | 70 | [slides.md](l08-quantize-and-vela/slides.md) |
| [5.9](l09-three-targets-lab/README.md) | ลงมือทำ: เทียบสามเป้าหมาย MCU, Web และ PC | 75 | [slides.md](l09-three-targets-lab/slides.md) |

บทเรียนมาเป็นชุด บทเรียนแนวคิดตามด้วยบทเรียน **ลงมือทำ** ที่มีไฟล์ฝึก เฉลย และแล็บ

## เช็กพอยต์ของโมดูล

ผ่านโมดูลนี้เมื่อทำได้ครบทุกข้อ (รายละเอียดอยู่ในหัวข้อ **แล็บ** ของบทเรียนลงมือทำ):

- [ ] dataset จากบอร์ดที่สะอาด สมดุล และแบ่งแล้ว ทุกกอง (train/val/test) มีครบสามคลาสในสัดส่วนใกล้เคียงกัน (บทเรียน 5.2)
- [ ] ฝึกโมเดล Keras ใน Docker สำเร็จ ได้รายงาน float32 accuracy, int8 accuracy และ confusion matrix บนชุดทดสอบที่โมเดลไม่เคยเห็น พร้อมไฟล์ `model_int8.tflite` และ `.norm.npz` (บทเรียน 5.5)
- [ ] verdict ของไฟล์ web ตรงกับฝั่ง PC ภายในเกณฑ์ (max|score_pc − score_web| ≤ TOL และคลาสที่ชนะตรงกัน) พร้อมอธิบายได้ว่าทำไมไม่จำเป็นต้องเท่ากันทุกบิต (บทเรียน 5.7)
- [ ] ตารางเทียบสามเป้าหมาย (MCU, Web, PC) ด้วยตัวเลขจริง อธิบายได้ว่าทำไม accuracy ตรงกันแต่ latency ต่างกัน และทำไม MCU ต้องผ่าน Vela (บทเรียน 5.9)
