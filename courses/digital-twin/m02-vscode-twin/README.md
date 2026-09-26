# โมดูล 2 — VS Code สำหรับพัฒนาร่วมกับ Twin

*VS Code for Twin Development* · หลักสูตร [พัฒนาเฟิร์มแวร์ร่วมกับ TESA Digital Twin บน VS Code](../README.md)

## เป้าหมาย

ติดตั้ง Bitstream Studio ผูก workspace กับเฟิร์มแวร์หรือแพ็กแล็บ แล้วเปิดเซสชันแรกที่ทำซ้ำได้ ทั้งแบบ Simulator และ/หรือ Bitstream (UART)

## บทเรียน

| # | บทเรียน | เนื้อหา |
|---|---|---|
| 1 | [ตั้งโฮสต์ Twin ใน VS Code ด้วย Bitstream Studio](l01-vscode-for-twin/README.md) | ติดตั้ง Bitstream Studio (Marketplace หรือ VSIX) จัด workspace ผูกเฟิร์มแวร์ รู้จัก backend services และไล่ปัญหาเมื่อ UI ว่าง |
| 2 | [แล็บ: ติดตั้ง Twin บน VS Code และเซสชันแรก](l02-lab/README.md) | ติดตั้ง Bitstream Studio ผูก workspace เปิดเซสชันแรก (Simulator หรือ Bitstream) แล้วสังเกตและสลับเส้นทาง |

เวลาโดยประมาณตามต้นฉบับ: ประมาณ 3 ชั่วโมง (บทเรียน) + แล็บ 2–3 ชั่วโมง (รวมติดตั้ง)

ชีตและแม่แบบประกอบ (อยู่ในโฟลเดอร์ `resources/` ของบทเรียนที่ 1):

- [vscode-twin-setup.md](l01-vscode-for-twin/resources/vscode-twin-setup.md)

## จุดตรวจ

ก่อนไปโมดูลถัดไป ตรวจว่าคุณทำสิ่งเหล่านี้ได้แล้ว:

- [ ] Bitstream Studio พร้อมใช้ และ backend ขึ้น
- [ ] workspace ชี้โปรเจกต์เฟิร์มแวร์หรือแพ็กแล็บได้
- [ ] เซสชันแรกสำเร็จอย่างน้อยหนึ่งเส้นทาง พร้อมสกรีนช็อต
- [ ] กรอก vscode-twin-setup.md ครบ

[← โมดูล 1](../m01-twin-architecture/README.md) · [หน้าหลักสูตร](../README.md) · [โมดูล 3 →](../m03-virtual-device/README.md)
