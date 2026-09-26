# โมดูล 6 — การรวมระบบและการทดสอบ

*System Integration and Testing* · หลักสูตร [พัฒนาเฟิร์มแวร์ร่วมกับ TESA Digital Twin บน VS Code](../README.md)

## เป้าหมาย

รวมโมดูล 1–5 เป็นระบบที่สาธิตซ้ำได้: stimulus → firmware → Studio → dashboard/MQTT พร้อมตารางเทส E2E อย่างน้อยสามเคส และ README ที่รันซ้ำได้

## บทเรียน

| # | บทเรียน | เนื้อหา |
|---|---|---|
| 1 | [ทดสอบ end-to-end บน Digital Twin](l01-system-integration-testing/README.md) | เกณฑ์ผ่านขั้นต่ำของ Capstone การวิเคราะห์ log ทีละชั้น โจทย์จากโดเมนจริง และกรณีศึกษา Smart Environmental Monitor |
| 2 | [แล็บ Capstone: มินิโปรเจกต์ E2E บน Digital Twin](l02-lab/README.md) | ล็อกสถาปัตยกรรม ประกอบเดโมที่รันได้ รันเทส E2E สามเคส ฝึกไล่ log และจัดแพ็กส่งต่อ |

เวลาโดยประมาณตามต้นฉบับ: ประมาณ 2 ชั่วโมง (บทเรียน) + แล็บ ~2 ชั่วโมง + เวลาเพิ่มสำหรับ README และหลักฐาน

ชีตและแม่แบบประกอบ (อยู่ในโฟลเดอร์ `resources/` ของบทเรียนที่ 1):

- [course-package.md](l01-system-integration-testing/resources/course-package.md)
- [e2e-case-brief.md](l01-system-integration-testing/resources/e2e-case-brief.md)

## จุดตรวจ

ก่อนไปโมดูลถัดไป ตรวจว่าคุณทำสิ่งเหล่านี้ได้แล้ว:

- [ ] เดโมที่รันซ้ำได้ครบเส้นทาง stimulus → firmware → Studio → consumer
- [ ] ตารางเทส E2E ≥ 3 เคสพร้อมผลจริง
- [ ] README วิธี bring-up → demo → teardown
- [ ] ไม่มี secret ในไฟล์ที่ส่งต่อ

[← โมดูล 5](../m05-telemetry-cloud/README.md) · [หน้าหลักสูตร](../README.md)
