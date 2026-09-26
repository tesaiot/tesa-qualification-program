# โมดูล 7 — การเชื่อมต่อ Bluetooth Low Energy (BLE)

*Bluetooth Low Energy (BLE) Connectivity* · หลักสูตร [TESA Firmware SDK สำหรับ Edge AI](../README.md)

## เป้าหมาย

เชื่อมบอร์ดกับโทรศัพท์หรือพีซีที่อยู่ใกล้ผ่าน BLE: อ่านสถานะ peripheral สั่ง advertising และยืนยันการเชื่อมต่อด้วยโฮสต์ พร้อมเข้าใจว่า BLE ต่างจาก MQTT อย่างไร

## บทเรียน

| # | บทเรียน | เนื้อหา |
|---|---|---|
| 1 | [BLE สำหรับผลิตภัณฑ์ Edge](l01-ble-connectivity/README.md) | บทบาทของ BLE เทียบกับ MQTT คำศัพท์ GAP/GATT การแบ่งงาน CM33/CM55 การอ่านสถานะ สั่ง advertising และเส้นทาง scan |
| 2 | [แล็บ: การเชื่อมต่อ BLE](l02-lab/README.md) | อ่านสถานะ peripheral สั่ง advertising ให้โฮสต์ค้นพบและเชื่อมต่อ ทดสอบลิงก์สั้น ๆ และ (ทางเลือก) ลอง scan |

เวลาโดยประมาณตามต้นฉบับ: ประมาณ 3–3.5 ชั่วโมง (บทเรียน) + แล็บ ~2–2.5 ชั่วโมง

ชีตและแม่แบบประกอบ (อยู่ในโฟลเดอร์ `resources/` ของบทเรียนที่ 1):

- [ble-connectivity.md](l01-ble-connectivity/resources/ble-connectivity.md)

> โค้ด C ในโมดูลนี้ใช้ API ของเฟิร์มแวร์ TESAIoT Bitstream ซึ่งยังไม่เปิดซอร์ส อ่านหมายเหตุต้น[บทเรียน](l01-ble-connectivity/README.md) ก่อนลงมือ

## จุดตรวจ

ก่อนไปโมดูลถัดไป ตรวจว่าคุณทำสิ่งเหล่านี้ได้แล้ว:

- [ ] ตารางสถานะ peripheral ก่อนและหลังโฮสต์เชื่อมต่อ
- [ ] สกรีนช็อตโฮสต์ที่เห็นและเชื่อมต่ออุปกรณ์ได้
- [ ] โน้ตสั้นว่า BLE ต่างจาก MQTT อย่างไรในโปรเจกต์ของคุณ

[← โมดูล 6](../m06-mqtt/README.md) · [หน้าหลักสูตร](../README.md) · [โมดูล 8 →](../m08-capstone/README.md)
