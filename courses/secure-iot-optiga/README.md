# Secure IoT กับ OPTIGA™ Trust M

ระดับ **L3** · สถานะ **pre-alpha (โครงร่าง อยู่ระหว่างเขียน)** · 5 โมดูล 11 บทเรียน · ประมาณ 20 ชั่วโมง

ความปลอดภัยเป็นจุดที่ TESA และ Infineon สอนได้ลึกกว่าที่อื่น เพราะบอร์ด TESAIoT Dev Kit มีชิปความปลอดภัย OPTIGA™ Trust M
และ SDK สาธารณะมีทั้งตัวอย่างและเอกสารเรื่อง mTLS, Protected Update และการลงทะเบียนอุปกรณ์ด้วย CSR อยู่แล้ว
หลักสูตรนี้เรียบเรียงวัสดุเหล่านั้นเป็นบทเรียน เริ่มจากคิดแบบผู้โจมตี แล้วค่อยลงมือกับชิปจริง
ลิงก์ไปยัง SDK ทุกลิงก์ตรึงไว้ที่ commit `ef72c1b`

## เหมาะกับใคร

- นักพัฒนาเฟิร์มแวร์ที่ผ่านหลักสูตรพื้นฐานเฟิร์มแวร์ภาษา C หรือเทียบเท่า
- ผู้ที่ต้องเชื่อมอุปกรณ์เข้าแพลตฟอร์ม IoT อย่างปลอดภัย
- ต้องมีบอร์ด TESAIoT Dev Kit และบัญชีหรือแพลตฟอร์ม TESAIoT สำหรับบทเรียนเรื่อง mTLS

## เมื่อจบหลักสูตร คุณจะทำได้

1. ทำ threat model ของอุปกรณ์ IoT หนึ่งชิ้น ระบุทรัพย์สิน ผู้โจมตี และมาตรการป้องกันที่ตรวจได้
2. อธิบายและเลือกใช้ hash ลายเซ็นดิจิทัล การเข้ารหัสแบบสมมาตรและอสมมาตร และใบรับรองได้เหมาะกับงาน
3. ใช้ OPTIGA™ Trust M ผ่าน SDK ตามกติกาการเข้าถึงชิป โดยกุญแจลับไม่ออกจากชิป
4. เชื่อมต่ออุปกรณ์กับ TESAIoT Platform ด้วย mTLS และอธิบายทุกขั้นของ handshake ได้
5. อธิบาย secure boot, Protected Update และการลงทะเบียนด้วย CSR และระบุการเปลี่ยนแปลงที่ย้อนกลับไม่ได้บนชิป

## โมดูลและบทเรียน

### [โมดูล 1 · Threat model และพื้นฐานวิทยาการเข้ารหัส](m01-threats-and-crypto/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| sec-iot.m01.l01 | [Threat model ของอุปกรณ์ IoT](m01-threats-and-crypto/l01-threat-modelling/README.md) | 70 นาที |
| sec-iot.m01.l02 | [พื้นฐานวิทยาการเข้ารหัสสำหรับระบบฝังตัว](m01-threats-and-crypto/l02-crypto-basics/README.md) | 70 นาที |

### [โมดูล 2 · ชิปความปลอดภัย OPTIGA™ Trust M](m02-optiga-trust-m/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| sec-iot.m02.l01 | [ชิปความปลอดภัยทำอะไรให้เรา](m02-optiga-trust-m/l01-secure-element-role/README.md) | 70 นาที |
| sec-iot.m02.l02 | [กติกาการเข้าถึงชิป](m02-optiga-trust-m/l02-chip-access-discipline/README.md) | 70 นาที |

### [โมดูล 3 · mTLS สู่ TESAIoT Platform](m03-mtls-to-platform/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| sec-iot.m03.l01 | [TLS และ mTLS](m03-mtls-to-platform/l01-tls-and-mtls/README.md) | 70 นาที |
| sec-iot.m03.l02 | [MQTTs ขึ้น TESAIoT Platform](m03-mtls-to-platform/l02-mqtts-to-tesaiot/README.md) | 70 นาที |

### [โมดูล 4 · Secure boot และ Protected Update](m04-secure-boot-and-update/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| sec-iot.m04.l01 | [Secure boot และ chain of trust](m04-secure-boot-and-update/l01-secure-boot/README.md) | 70 นาที |
| sec-iot.m04.l02 | [Protected Update](m04-secure-boot-and-update/l02-protected-update/README.md) | 70 นาที |

### [โมดูล 5 · การลงทะเบียนอุปกรณ์อย่างปลอดภัย](m05-provisioning/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| sec-iot.m05.l01 | [ลงทะเบียนด้วย CSR](m05-provisioning/l01-csr-enrolment/README.md) | 70 นาที |
| sec-iot.m05.l02 | [หน้าจอลงทะเบียนบนอุปกรณ์](m05-provisioning/l02-provisioning-screens/README.md) | 70 นาที |
| sec-iot.m05.l03 | [งานปลายทาง: อุปกรณ์ที่ปลอดภัยหนึ่งชิ้น](m05-provisioning/l03-capstone-secure-device/README.md) | 75 นาที |

## สถานะของหลักสูตร

หลักสูตรนี้เป็นโครงร่าง (pre-alpha) ทุกบทเรียนมีเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว แต่ยังไม่มีเนื้อหาและแบบฝึก
**คำเตือนด้านความปลอดภัยของชิป** สถานะวงจรชีวิตของ OPTIGA (LcsO) เปลี่ยนได้ทางเดียวและย้อนกลับไม่ได้ ตาม README ของตัวอย่างใน SDK
ไม่มีตัวอย่างใดใน SDK ที่เขียน metadata tag C0 หรือเลื่อนสถานะนี้ บทเรียนในหลักสูตรนี้จะไม่สั่งให้ทำเช่นกัน
โค้ด host library ของ Infineon ใช้วิธีลิงก์ไปยัง repository และ tag ไม่คัดลอกมา

## แหล่งอ้างอิงหลัก

- [TESAIoT PSE84 Dev Kit SDK (Apache-2.0) README](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/README.md)
- [Security / HSM (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__feat__security.html)
- [C4 — mTLS: the OPTIGA-backed TLS identity (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c4__mtls__optiga.html)
- [D2 — Enrolment and Protected Update end to end (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d2__enrolment__protected__update.html)
- [Infineon optiga-trust-m (host library, MIT) @ release-v5.8.3](https://github.com/Infineon/optiga-trust-m/tree/release-v5.8.3)
- [ETSI EN 303 645 V3.1.3 (2024-09) Cyber Security for Consumer Internet of Things: Baseline Requirements](https://www.etsi.org/deliver/etsi_en/303600_303699/303645/03.01.03_60/en_303645v030103p.pdf)

## สัญญาอนุญาต

- เนื้อหา CC BY 4.0
- โค้ดใหม่ที่จะเพิ่มในหลักสูตรนี้ Apache-2.0
- โค้ดของ SDK และของ Infineon ไม่ได้คัดลอกมา ใช้สัญญาอนุญาตของต้นทางตามลิงก์

## อ้างอิง TESA

เมื่อนำหลักสูตรนี้ไปใช้ แบ่งปัน หรือดัดแปลง ต้องอ้างอิงดังนี้

> "Secure IoT กับ OPTIGA™ Trust M" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0

ถ้าแก้ไขเนื้อหา ให้เติม **(ดัดแปลง)** ต่อท้ายข้อความอ้างอิง พร้อมบอกสั้น ๆ ว่าเปลี่ยนอะไร
การอ้างอิงไม่ได้แปลว่า TESA รับรองงานของคุณ รายละเอียดและตัวอย่างอยู่ใน [ATTRIBUTION.md](../../ATTRIBUTION.md)
