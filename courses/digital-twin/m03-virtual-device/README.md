# โมดูล 3 — การสร้างแบบจำลองอุปกรณ์เสมือน (+ Blender สำหรับ Twin 3D)

*Virtual Device Modeling (+ Blender for Twin 3D)* · หลักสูตร [พัฒนาเฟิร์มแวร์ร่วมกับ TESA Digital Twin บน VS Code](../README.md)

## เป้าหมาย

ออกแบบสิ่งที่ Twin จำลอง: โมเดลอุปกรณ์ที่มีเซ็นเซอร์ พฤติกรรม และสคริปต์เหตุการณ์ที่รันซ้ำได้ พร้อมพื้นฐาน Blender สำหรับโมเดล 3D ที่ Twin แสดง

## บทเรียน

| # | บทเรียน | เนื้อหา |
|---|---|---|
| 1 | [Virtual Device, behavior, event script และโมเดล 3D สำหรับ Twin](l01-virtual-device-modeling/README.md) | กำหนดโมเดลอุปกรณ์ เซ็นเซอร์ พฤติกรรม และสคริปต์เหตุการณ์ตามเวลา แล้วเตรียมโมเดล 3D ใน Blender ให้ส่งออกเป็น GLB สำหรับ Twin |
| 2 | [แล็บ: สร้าง Virtual Device และ event script](l02-lab/README.md) | สร้างโมเดลอุปกรณ์ กำหนด behavior เขียนสคริปต์เหตุการณ์ที่รันซ้ำได้ และ (แนะนำ) ฝึก Blender สั้น ๆ แล้วส่งออก GLB |

เวลาโดยประมาณตามต้นฉบับ: ประมาณ 4–5 ชั่วโมง (บทเรียน) + แล็บ 3–3.5 ชั่วโมง (+ 1–1.5 ชั่วโมงถ้าทำ Lab E Blender)

ชีตและแม่แบบประกอบ (อยู่ในโฟลเดอร์ `resources/` ของบทเรียนที่ 1):

- [blender-twin-cheatsheet.md](l01-virtual-device-modeling/resources/blender-twin-cheatsheet.md)
- [device-model-checklist.md](l01-virtual-device-modeling/resources/device-model-checklist.md)
- [sample-virtual-device.template.json](l01-virtual-device-modeling/resources/sample-virtual-device.template.json)

## จุดตรวจ

ก่อนไปโมดูลถัดไป ตรวจว่าคุณทำสิ่งเหล่านี้ได้แล้ว:

- [ ] device-model.json (หรือเทียบเท่า) ที่มีเซ็นเซอร์ ≥ 2 ชนิด
- [ ] behavior อย่างน้อยหนึ่งเส้นทางที่สังเกตผลได้
- [ ] event script ที่รันซ้ำได้ และหลักฐานผลบน visualization
- [ ] (แนะนำ) ไฟล์ .glb จาก Blender

[← โมดูล 2](../m02-vscode-twin/README.md) · [หน้าหลักสูตร](../README.md) · [โมดูล 4 →](../m04-cosimulation/README.md)
