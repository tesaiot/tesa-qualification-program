# โมดูล 8 — Capstone และแหล่งเรียนรู้ของหลักสูตร

*Capstone Project and Course Resources* · หลักสูตร [TESA Firmware SDK สำหรับ Edge AI](../README.md)

## เป้าหมาย

รวมทักษะจากโมดูล 1–7 เป็นมินิโปรเจกต์ที่สาธิตได้ และส่งมอบพร้อม README ที่ผู้อื่นทำซ้ำได้

## บทเรียน

| # | บทเรียน | เนื้อหา |
|---|---|---|
| 1 | [วางแผน Capstone และใช้แผนที่เอกสาร](l01-capstone-and-resources/README.md) | เกณฑ์ผ่านของ Capstone แผนที่ชีตและ API ของหลักสูตร สถาปัตยกรรมอ้างอิง และสถานการณ์สาธิตสามแบบ |
| 2 | [แล็บ Capstone: มินิโปรเจกต์](l02-lab/README.md) | สร้างมินิโปรเจกต์บนบอร์ดจริงที่รวม sensor, RTOS และ MQTT หรือ BLE สาธิตสามสถานการณ์ และส่งมอบ README ที่ทำซ้ำได้ |

เวลาโดยประมาณตามต้นฉบับ: ยืดหยุ่น — บทเรียน 2–4 ชั่วโมง + ทำ Capstone ต่อเองได้

ชีตและแม่แบบประกอบ (อยู่ในโฟลเดอร์ `resources/` ของบทเรียนที่ 1):

- [capstone-brief.md](l01-capstone-and-resources/resources/capstone-brief.md)
- [course-package.md](l01-capstone-and-resources/resources/course-package.md)

> โค้ด C ในโมดูลนี้ใช้ API ของเฟิร์มแวร์ TESAIoT Bitstream ซึ่งยังไม่เปิดซอร์ส อ่านหมายเหตุต้น[บทเรียน](l01-capstone-and-resources/README.md) ก่อนลงมือ

## จุดตรวจ

ก่อนไปโมดูลถัดไป ตรวจว่าคุณทำสิ่งเหล่านี้ได้แล้ว:

- [ ] build + flash ได้ตาม README ของคุณ
- [ ] มีอย่างน้อยสอง FreeRTOS task ทำงานจริง
- [ ] sensor path + สถานะบน LED/UART
- [ ] MQTT หรือ BLE ใช้งานได้พร้อมรับคำสั่งหรือยืนยันลิงก์
- [ ] สาธิตครบสามสถานการณ์ และไม่มี secret ในไฟล์สาธารณะ

[← โมดูล 7](../m07-ble/README.md) · [หน้าหลักสูตร](../README.md)
