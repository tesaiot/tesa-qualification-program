# โมดูล 4 — Co-simulation ระหว่างเฟิร์มแวร์กับ Twin

*Firmware–Twin Co-simulation* · หลักสูตร [พัฒนาเฟิร์มแวร์ร่วมกับ TESA Digital Twin บน VS Code](../README.md)

## เป้าหมาย

เอาเฟิร์มแวร์จริงมาวิ่งคู่กับ Twin แล้วพิสูจน์เส้นทางอินพุต–เอาต์พุตแบบมีหลักฐาน วัด latency และแยกปัญหาฝั่งเฟิร์มแวร์กับฝั่งโฮสต์

## บทเรียน

| # | บทเรียน | เนื้อหา |
|---|---|---|
| 1 | [Co-simulation: พิสูจน์ I/O วัด latency และแยกปัญหา](l01-firmware-twin-cosim/README.md) | bring-up ให้เสถียรก่อน พิสูจน์เส้นทาง input/output ใช้ web-app ภายนอกเป็นหลักฐานชั้นที่สอง วัด latency และไล่ปัญหาทีละชั้น |
| 2 | [แล็บ: I/O ครบวงจรแบบ co-simulation](l02-lab/README.md) | bring-up co-sim พิสูจน์เส้นทาง input และ output จด latency และ (แนะนำ) ใช้ web-app ex05 เป็นกระจกชั้นที่สอง |

เวลาโดยประมาณตามต้นฉบับ: ประมาณ 3 ชั่วโมง (บทเรียน) + แล็บ 2.5–3 ชั่วโมง

ชีตและแม่แบบประกอบ (อยู่ในโฟลเดอร์ `resources/` ของบทเรียนที่ 1):

- [cosim-checklist.md](l01-firmware-twin-cosim/resources/cosim-checklist.md)

## จุดตรวจ

ก่อนไปโมดูลถัดไป ตรวจว่าคุณทำสิ่งเหล่านี้ได้แล้ว:

- [ ] heartbeat ทั้งฝั่งโฮสต์และฝั่งเฟิร์มแวร์ (sim หรือบอร์ด)
- [ ] หลักฐานเส้นทาง input และ output
- [ ] latency คร่าว ๆ อย่างน้อยหนึ่งจุด
- [ ] กรอก cosim-checklist.md ครบ

[← โมดูล 3](../m03-virtual-device/README.md) · [หน้าหลักสูตร](../README.md) · [โมดูล 5 →](../m05-telemetry-cloud/README.md)
