# โมดูล 6 — MQTT และ MQTTs สำหรับสื่อสารกับคลาวด์

*MQTT and MQTTs for Cloud Communication* · หลักสูตร [TESA Firmware SDK สำหรับ Edge AI](../README.md)

## เป้าหมาย

เชื่อมอุปกรณ์กับ broker: Wi-Fi ก่อนเสมอ แล้ว connect MQTT, publish telemetry, subscribe รับคำสั่ง และเข้าใจความต่างของ MQTT กับ MQTTs

## บทเรียน

| # | บทเรียน | เนื้อหา |
|---|---|---|
| 1 | [MQTT และ MQTTs บนอุปกรณ์ Edge](l01-mqtt-and-mqtts/README.md) | หลักการ publish/subscribe เส้นทางเชื่อมต่อของเฟิร์มแวร์ (Wi-Fi → MQTT) การตั้งค่า broker topic payload JSON และความปลอดภัยด้วย TLS |
| 2 | [แล็บ: Wi-Fi, MQTT connect, publish และ subscribe](l02-lab/README.md) | join Wi-Fi เชื่อม MQTT publish ข้อความหรือ telemetry แล้ว subscribe รับคำสั่งกลับ พร้อมบันทึกคอนฟิกโดยไม่เปิดเผยความลับ |

เวลาโดยประมาณตามต้นฉบับ: ประมาณ 3.5–4 ชั่วโมง (บทเรียน) + แล็บ 2.5–3.5 ชั่วโมง

ชีตและแม่แบบประกอบ (อยู่ในโฟลเดอร์ `resources/` ของบทเรียนที่ 1):

- [mqtt-cloud.md](l01-mqtt-and-mqtts/resources/mqtt-cloud.md)

> โค้ด C ในโมดูลนี้ใช้ API ของเฟิร์มแวร์ TESAIoT Bitstream ซึ่งยังไม่เปิดซอร์ส อ่านหมายเหตุต้น[บทเรียน](l01-mqtt-and-mqtts/README.md) ก่อนลงมือ

## จุดตรวจ

ก่อนไปโมดูลถัดไป ตรวจว่าคุณทำสิ่งเหล่านี้ได้แล้ว:

- [ ] Wi-Fi ขึ้นสถานะ CONNECTED แล้ว MQTT เชื่อมกับ broker ที่เลือกได้
- [ ] publish แล้วเห็นข้อความบน subscriber ของโฮสต์
- [ ] คำสั่งจากโฮสต์กลับถึงอุปกรณ์
- [ ] รายงานสั้นไม่มีรหัสผ่านหรือใบรับรองจริง

[← โมดูล 5](../m05-sensor-data/README.md) · [หน้าหลักสูตร](../README.md) · [โมดูล 7 →](../m07-ble/README.md)
