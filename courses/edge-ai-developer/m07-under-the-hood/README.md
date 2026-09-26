# โมดูล 7 — ใต้ฝากระโปรงและการต่อเติม

> Under the hood and extending the firmware · [หน้าหลักสูตร](../README.md)

แกะสแตกจาก MicroPython ข้าม IPC ไปถึง ai_engine และ NPU แล้วใช้แผนที่นั้นเพิ่มโมเดลของเราเองให้โผล่ใน edge_ai.models()

## เป้าหมายของโมดูล

เลิกเป็นแค่ผู้ใช้ API แล้วเริ่มเป็นคนที่อ่าน แก้ และต่อเติมสแตกได้

## บทเรียน

| บทเรียน | เรื่อง | เวลา (นาที) | สไลด์ |
|---|---|---|---|
| [7.1](l01-edge-ai-stack/README.md) | สแตก Edge AI: tri-core, ai_engine, IPC model link และ TFLite-Micro | 70 | [slides.md](l01-edge-ai-stack/slides.md) |
| [7.2](l02-trace-the-stack-lab/README.md) | ลงมือทำ: ส่องสแตกจาก MicroPython | 75 | [slides.md](l02-trace-the-stack-lab/slides.md) |
| [7.3](l03-add-your-own-model/README.md) | เพิ่มโมเดลของเราเอง: สามการแก้ สัญญาสี่ฟังก์ชัน และ Vela | 70 | [slides.md](l03-add-your-own-model/slides.md) |
| [7.4](l04-extend-model-lab/README.md) | ลงมือทำ: ให้โมเดลใหม่โผล่ใน edge_ai.models() | 75 | [slides.md](l04-extend-model-lab/slides.md) |

บทเรียนมาเป็นชุด บทเรียนแนวคิดตามด้วยบทเรียน **ลงมือทำ** ที่มีไฟล์ฝึก เฉลย และแล็บ

## เช็กพอยต์ของโมดูล

ผ่านโมดูลนี้เมื่อทำได้ครบทุกข้อ (รายละเอียดอยู่ในหัวข้อ **แล็บ** ของบทเรียนลงมือทำ):

- [ ] อธิบายสแตกได้ แล้วชี้ฟังก์ชันหรือฟิลด์ต้นทางของสามชั้น (transport, control, result) ได้อย่างน้อยชั้นละหนึ่งจุด (บทเรียน 7.2)
- [ ] โมเดลใหม่ที่เพิ่มเอง `edge_ai.count()` เพิ่มขึ้น ชื่อโผล่ใน `edge_ai.models()` และเลือกรันแล้วได้ verdict จริงบนบอร์ด (บทเรียน 7.4)
