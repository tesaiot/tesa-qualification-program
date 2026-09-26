# โมดูล 3 · mTLS สู่ TESAIoT Platform

**เป้าหมายของโมดูล** เชื่อมอุปกรณ์กับแพลตฟอร์มด้วย mTLS ที่ใช้ตัวตนจากชิปความปลอดภัย

สถานะ **alpha** (เนื้อหาครบ รอการทดลองสอนและคำติชม) · เวลาโดยประมาณ 140 นาที

**ข้อตกลงของโมดูล** แล็บหลักทำบนคอมพิวเตอร์ด้วย `openssl` และ `mosquitto-clients` แล็บบนบอร์ดต้องมีอุปกรณ์ที่ลงทะเบียนกับ TESAIoT Platform และห้ามนำข้อมูลรับรองจาก bundle ขึ้น repository ใด ๆ

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| [sec-iot.m03.l01](l01-tls-and-mtls/README.md) | TLS และ mTLS | 70 นาที |
| [sec-iot.m03.l02](l02-mqtts-to-tesaiot/README.md) | MQTTs ขึ้น TESAIoT Platform | 70 นาที |

## Checkpoint ท้ายโมดูล

- [ ] แผนภาพ handshake ของ mTLS ที่ระบุว่าขั้นไหนใช้กุญแจในชิป
- [ ] อุปกรณ์ส่งข้อมูลผ่าน MQTTs ขึ้น TESAIoT Platform และอธิบาย log ของการเชื่อมต่อได้
