# โมดูล 1 — สถาปัตยกรรม Digital Twin

*Digital Twin Architecture* · หลักสูตร [พัฒนาเฟิร์มแวร์ร่วมกับ TESA Digital Twin บน VS Code](../README.md)

## เป้าหมาย

วางแผนที่ความคิดของ Course 2: แยก Virtual Device, Digital Twin Platform, firmware logic และโฮสต์ออกจากกัน และรู้ว่าการทดสอบแบบไหนใช้ Twin ได้ แบบไหนต้องใช้บอร์ดจริง

## บทเรียน

| # | บทเรียน | เนื้อหา |
|---|---|---|
| 1 | [Virtual Device, Digital Twin และโลกของเฟิร์มแวร์จริง](l01-twin-architecture/README.md) | ความหมายของ Virtual Device และ Digital Twin สถาปัตยกรรมเป็นชั้น เส้นทาง live สองเส้น (Bitstream กับ Simulator) และเกณฑ์ตัดสินใจว่าเมื่อไรต้องใช้บอร์ดจริง |
| 2 | [แล็บ: แผนที่สถาปัตยกรรม Twin](l02-lab/README.md) | นิยามคำด้วยภาษาตัวเอง วาด data flow และกรอกตารางตัดสินใจว่าเทสไหนใช้ Twin ได้ เทสไหนต้องบอร์ด |

เวลาโดยประมาณตามต้นฉบับ: ประมาณ 2 ชั่วโมง (บทเรียน) + แล็บ 30–45 นาที

ชีตและแม่แบบประกอบ (อยู่ในโฟลเดอร์ `resources/` ของบทเรียนที่ 1):

- [twin-architecture-map.md](l01-twin-architecture/resources/twin-architecture-map.md)

## จุดตรวจ

ก่อนไปโมดูลถัดไป ตรวจว่าคุณทำสิ่งเหล่านี้ได้แล้ว:

- [ ] นิยามสามคำในส่วน A ด้วยคำพูดของตัวเอง
- [ ] แผนภาพ data flow ของระบบตัวอย่างหนึ่งชุด
- [ ] ตารางตัดสินใจอย่างน้อย 4 แถว มีทั้งแถว “Twin พอ” และ “ต้องบอร์ด”

[หน้าหลักสูตร](../README.md) · [โมดูล 2 →](../m02-vscode-twin/README.md)
