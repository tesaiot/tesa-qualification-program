# โมดูล 2 — ModusToolbox™ และ VS Code สำหรับพัฒนาเฟิร์มแวร์

*ModusToolbox™ and VS Code for Firmware Development* · หลักสูตร [TESA Firmware SDK สำหรับ Edge AI](../README.md)

## เป้าหมาย

ทำให้เครื่องพัฒนาพร้อมจริง: ติดตั้ง ModusToolbox™ + VS Code สร้างโปรเจกต์จาก BSP ที่ตรงคิต แล้ว build · flash · debug บนบอร์ดได้

## บทเรียน

| # | บทเรียน | เนื้อหา |
|---|---|---|
| 1 | [ModusToolbox™ และ VS Code: สร้าง build flash debug](l01-modustoolbox-and-vscode/README.md) | แยกบทบาทของ ModusToolbox™, VS Code, KitProg3 และ SDK ตั้ง environment ให้ครบ เลือก BSP ให้ตรงคิต และรู้วิธีไล่อาการเสียที่พบบ่อย |
| 2 | [แล็บ: สร้าง build flash และ debug โปรเจกต์เฟิร์มแวร์](l02-lab/README.md) | ตรวจเครื่อง สร้างโปรเจกต์จาก BSP build ใน VS Code flash ลงบอร์ด และ debug อย่างน้อยหนึ่งครั้ง |

เวลาโดยประมาณตามต้นฉบับ: ประมาณ 2.5–3 ชั่วโมง (บทเรียน) + แล็บ 90–120 นาที

ชีตและแม่แบบประกอบ (อยู่ในโฟลเดอร์ `resources/` ของบทเรียนที่ 1):

- [toolchain-cheatsheet.md](l01-modustoolbox-and-vscode/resources/toolchain-cheatsheet.md)

## จุดตรวจ

ก่อนไปโมดูลถัดไป ตรวจว่าคุณทำสิ่งเหล่านี้ได้แล้ว:

- [ ] build โปรเจกต์ตัวอย่างผ่าน หรือ flash HEX จากแพ็กแล็บสำเร็จ
- [ ] program ลงบอร์ดแล้วเห็นพฤติกรรมที่ยืนยันได้ (LED หรือข้อความ serial)
- [ ] เปิด debug session แล้ว halt ที่ main หรือ breakpoint ได้อย่างน้อยหนึ่งครั้ง

[← โมดูล 1](../m01-mcu-architecture/README.md) · [หน้าหลักสูตร](../README.md) · [โมดูล 3 →](../m03-gpio-peripherals/README.md)
