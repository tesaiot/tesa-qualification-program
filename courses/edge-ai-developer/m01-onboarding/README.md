# โมดูล 1 — เริ่มต้น: รันของจริงแล้วแกะดูข้างใน

> Getting started: run the real thing, then take it apart · [หน้าหลักสูตร](../README.md)

รันโมเดล Edge AI ของจริงก่อน แล้วแกะแอปเซนเซอร์กับแอป Edge AI จนเห็นโครงร่วมสี่จังหวะ ทะเบียนโมเดล และเส้นทางจาก verdict สู่ action

## เป้าหมายของโมดูล

เห็นปลายทางของทั้งคอร์สตั้งแต่วันแรก: ถามทะเบียนโมเดล เลือก อ่านคำตอบ แล้วต่อเข้ากับการกระทำบนบอร์ด พร้อมรู้จักโครงร่วมที่ทุกโปรแกรมในคอร์สใช้

## บทเรียน

| บทเรียน | เรื่อง | เวลา (นาที) | สไลด์ |
|---|---|---|---|
| [1.1](l01-edge-ai-lifecycle/README.md) | Edge AI คืออะไร: วงจรชีวิตของข้อมูลห้าขั้นและเป้าหมายที่โมเดลไปรันได้ | 55 | [slides.md](l01-edge-ai-lifecycle/slides.md) |
| [1.2](l02-edge-ai-module/README.md) | โมดูล edge_ai: ถามทะเบียนโมเดล เลือก แล้วอ่านคำตอบ | 60 | [slides.md](l02-edge-ai-module/slides.md) |
| [1.3](l03-first-inference-lab/README.md) | ลงมือทำ: เมนูโมเดลตัวแรกของเรา | 70 | [slides.md](l03-first-inference-lab/slides.md) |
| [1.4](l04-sensor-app-anatomy/README.md) | แกะแอปเซนเซอร์: โครงร่วมสี่จังหวะของทุกโปรแกรม | 65 | [slides.md](l04-sensor-app-anatomy/slides.md) |
| [1.5](l05-sensor-remix-lab/README.md) | ลงมือทำ: remix เป็น Tilt Monitor ของเรา | 75 | [slides.md](l05-sensor-remix-lab/slides.md) |
| [1.6](l06-edge-ai-app-anatomy/README.md) | แกะแอป Edge AI: ทะเบียนโมเดล verdict และ action | 65 | [slides.md](l06-edge-ai-app-anatomy/slides.md) |
| [1.7](l07-verdict-action-lab/README.md) | ลงมือทำ: จาก verdict สู่ action บนบอร์ด | 75 | [slides.md](l07-verdict-action-lab/slides.md) |

บทเรียนมาเป็นชุด บทเรียนแนวคิดตามด้วยบทเรียน **ลงมือทำ** ที่มีไฟล์ฝึก เฉลย และแล็บ

## เช็กพอยต์ของโมดูล

ผ่านโมดูลนี้เมื่อทำได้ครบทุกข้อ (รายละเอียดอยู่ในหัวข้อ **แล็บ** ของบทเรียนลงมือทำ):

- [ ] รันเมนู `edge_ai` แล้วอ่านผลสดออก ทั้งคลาสที่ชนะ (`label`) และความมั่นใจ (`conf`) เปลี่ยนตามท่าทางหรือเสียงจริง (บทเรียน 1.3)
- [ ] remix ที่ต่างจากต้นฉบับจริง และอธิบายแต่ละส่วนได้ว่าอยู่จังหวะไหน (บทเรียน 1.5)
- [ ] remix `s03_anatomy_edgeai.py` ได้จริง คือสลับโมเดล (เปลี่ยน `MODEL_KEYWORD` และ `TARGET_CLASS`) และสั่งการเมื่อเจอคำตัดสินที่เข้าเงื่อนไข (บทเรียน 1.7)
