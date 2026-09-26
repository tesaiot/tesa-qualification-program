# โมดูล 4 — จาก Blender สู่ Digital Twin

*Blender to Twin Integration* · หลักสูตร [การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)](../README.md)

## เป้าหมาย

ส่งออกโมเดลเป็น GLB ที่ขนาดถูก แกนถูก ชื่อคลิปชัด แล้วนำเข้า Twin host กำหนดจุดเซ็นเซอร์และจุดโต้ตอบ และทดสอบกับคลิปหรือ telemetry

## บทเรียน

| # | บทเรียน | เนื้อหา |
|---|---|---|
| 1 | [ส่งออก GLB และนำเข้า Twin host](l01-blender-to-twin/README.md) | ความหมายของ Twin-ready การเตรียมไฟล์ก่อน export ขั้นตอน glTF Binary การตรวจหลังนำเข้า จุดเซ็นเซอร์และจุดโต้ตอบ และเมทริกซ์ทดสอบขั้นต่ำ |
| 2 | [แล็บ: ส่งออก GLB และนำเข้า Twin](l02-lab/README.md) | เตรียมไฟล์ ส่งออก .glb นำเข้า Twin host ทำเครื่องหมายจุดเซ็นเซอร์/โต้ตอบ แล้วทดสอบด้วยคลิปหรือข้อมูล |

เวลาโดยประมาณตามต้นฉบับ: ประมาณ 3 ชั่วโมง (บทเรียน) + แล็บ 2.5–3 ชั่วโมง

ชีตและแม่แบบประกอบ (อยู่ในโฟลเดอร์ `resources/` ของบทเรียนที่ 1):

- [export-twin-checklist.md](l01-blender-to-twin/resources/export-twin-checklist.md)

## จุดตรวจ

ก่อนไปโมดูลถัดไป ตรวจว่าคุณทำสิ่งเหล่านี้ได้แล้ว:

- [ ] ไฟล์ enclosure_twin.glb พร้อม .blend ต้นทาง
- [ ] สกรีนช็อตโมเดลใน Bitstream Studio ที่ขนาดและแกนใช้งานได้
- [ ] จุด sensor/interaction ≥ 1 จุดพร้อมชื่อ
- [ ] ผลทดสอบคลิปหรือ telemetry และ export-twin-checklist.md ครบ

[← โมดูล 3](../m03-motion/README.md) · [หน้าหลักสูตร](../README.md) · [โมดูล 5 →](../m05-digital-validation/README.md)
