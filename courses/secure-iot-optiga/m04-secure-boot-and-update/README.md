# โมดูล 4 · Secure boot และ Protected Update

**เป้าหมายของโมดูล** เข้าใจห่วงโซ่ความเชื่อใจตั้งแต่บูต และการอัปเดตที่ป้องกันการย้อนรุ่น

สถานะ **alpha** (เนื้อหาครบ รอการทดลองสอนและคำติชม) · เวลาโดยประมาณ 140 นาที

**ข้อตกลงของโมดูล** ไม่มีแล็บใด provision secure boot ของอุปกรณ์ หรือเขียน metadata tag C0 (LcsO) แล็บเสริมที่ส่ง Protected Update จริงทำให้ตัวนับ version ของช่องเป้าหมายขึ้นถาวร จึงต้องได้รับอนุญาตจากผู้สอนก่อน

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| [sec-iot.m04.l01](l01-secure-boot/README.md) | Secure boot และ chain of trust | 70 นาที |
| [sec-iot.m04.l02](l02-protected-update/README.md) | Protected Update | 70 นาที |

## Checkpoint ท้ายโมดูล

- [ ] แผนภาพ chain of trust ของบอร์ดตั้งแต่บูตจนถึงแอป
- [ ] อธิบายตัวนับกันย้อนรุ่นและผลของ manifest lock ได้
