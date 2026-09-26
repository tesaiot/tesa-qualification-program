# โมดูล 5 — Telemetry และการจำลองคลาวด์

*Telemetry and Cloud Simulation* · หลักสูตร [พัฒนาเฟิร์มแวร์ร่วมกับ TESA Digital Twin บน VS Code](../README.md)

## เป้าหมาย

ขยายท่อข้อมูลออกนอก Studio: จำแนก telemetry/state/event ตรวจคุณภาพสตรีม ตั้ง broker ใน Twin host ทำ pub/sub และทดลองเครือข่ายไม่เสถียรแบบควบคุมได้

## บทเรียน

| # | บทเรียน | เนื้อหา |
|---|---|---|
| 1 | [ท่อ telemetry, MQTT บน Twin และ fault injection](l01-telemetry-cloud-simulation/README.md) | แยก Telemetry/State/Event แยกท่อ Live Data กับ MQTT ใช้ web-app ex08/ex09 ตรวจสตรีม และออกแบบการทดลองเครือข่ายเสีย |
| 2 | [แล็บ: ท่อ telemetry และ MQTT บน Twin](l02-lab/README.md) | ออกแบบ topic ตรวจคุณภาพ Live Data ด้วย ex08 ตั้ง broker แล้ว subscribe ด้วย ex09 และทดลอง lossy/reconnect |

เวลาโดยประมาณตามต้นฉบับ: ประมาณ 4 ชั่วโมง (บทเรียน) + แล็บ 3.5–4 ชั่วโมง

ชีตและแม่แบบประกอบ (อยู่ในโฟลเดอร์ `resources/` ของบทเรียนที่ 1):

- [telemetry-mqtt-lab-notes.md](l01-telemetry-cloud-simulation/resources/telemetry-mqtt-lab-notes.md)

## จุดตรวจ

ก่อนไปโมดูลถัดไป ตรวจว่าคุณทำสิ่งเหล่านี้ได้แล้ว:

- [ ] ตาราง topic ที่แยก Telemetry / State / Event
- [ ] pub/sub อย่างน้อยหนึ่งคู่ผ่าน broker ใน Studio
- [ ] fault injection อย่างน้อยหนึ่งเคสที่บันทึกผล
- [ ] กรอก telemetry-mqtt-lab-notes.md ครบ

[← โมดูล 4](../m04-cosimulation/README.md) · [หน้าหลักสูตร](../README.md) · [โมดูล 6 →](../m06-integration/README.md)
