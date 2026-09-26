# Secure IoT กับ OPTIGA™ Trust M

ระดับ **L3** · สถานะ **alpha** · 5 โมดูล 11 บทเรียน · ประมาณ 20 ชั่วโมง

ความปลอดภัยเป็นจุดที่ TESA และ Infineon สอนได้ลึกกว่าที่อื่น เพราะบอร์ด TESAIoT Dev Kit มีชิปความปลอดภัย OPTIGA™ Trust M
และ SDK สาธารณะมีทั้งตัวอย่างและเอกสารเรื่อง mTLS, Protected Update และการลงทะเบียนอุปกรณ์ด้วย CSR อยู่แล้ว
หลักสูตรนี้เรียบเรียงวัสดุเหล่านั้นเป็นบทเรียน เริ่มจากคิดแบบผู้โจมตี แล้วค่อยลงมือกับชิปจริง
ลิงก์ไปยัง SDK ทุกลิงก์ตรึงไว้ที่ commit `ef72c1b`

ตลอดหลักสูตรเราใช้อุปกรณ์ตัวอย่างชิ้นเดียว คือโหนดเซนเซอร์บน TESAIoT Dev Kit ที่ส่งข้อมูลขึ้น TESAIoT Platform ผ่าน MQTTS
เริ่มจากทำ threat model ของมัน แล้วค่อย ๆ เติมมาตรการทีละบท จนบทสุดท้ายส่งอุปกรณ์ชิ้นนั้นพร้อมหลักฐานว่ามาตรการทำงานจริง
ทุกข้อเท็จจริงในบทเรียนอ้างถึงไฟล์ใน SDK เอกสารของ SDK ตัวอย่างบน TESAIoT Developer Hub หรือเอกสารสาธารณะของ Infineon
และทุกบทบอกตรง ๆ ว่า TLS, mTLS, ชิปความปลอดภัย, secure boot และ Protected Update **ไม่ได้** ป้องกันอะไร

## เหมาะกับใคร

- นักพัฒนาเฟิร์มแวร์ที่ผ่านหลักสูตรพื้นฐานเฟิร์มแวร์ภาษา C หรือเทียบเท่า
- ผู้ที่ต้องเชื่อมอุปกรณ์เข้าแพลตฟอร์ม IoT อย่างปลอดภัย
- ต้องมีบอร์ด TESAIoT Dev Kit และบัญชีหรือแพลตฟอร์ม TESAIoT สำหรับบทเรียนเรื่อง mTLS

**สิ่งที่ต้องเตรียม** TESAIoT PSE84 Dev Kit SDK ที่ commit `ef72c1b` กับ ModusToolbox 3.6 (README ของ SDK ระบุรุ่นนี้)
คอมพิวเตอร์ที่มี `openssl` และ `mosquitto-clients` และอุปกรณ์ที่ลงทะเบียนบน TESAIoT Platform สำหรับโมดูล 3 ถึง 5

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

หลักสูตรนี้อยู่ในสถานะ **alpha** ทุกบทเรียนมีเนื้อหา ตัวอย่างที่ยกจากซอร์สจริง แบบฝึกพร้อมเฉลย เช็กความเข้าใจใน `quiz.yaml` และแล็บ
ยังรอการทดลองสอนกับผู้เรียนจริงและคำติชม หน้าภาษาอังกฤษของแต่ละบทเรียนยังไม่ได้แปล (`translation: pending`)

**คำเตือนด้านความปลอดภัยของชิป** สถานะวงจรชีวิตของ OPTIGA (LcsO) เปลี่ยนได้ทางเดียวและย้อนกลับไม่ได้ ตาม README ของตัวอย่างใน SDK
ไม่มีตัวอย่างใดใน SDK ที่เขียน metadata tag C0 หรือเลื่อนสถานะนี้ และไม่มีบทเรียนใดในหลักสูตรนี้สั่งให้ทำ
แล็บที่เปลี่ยนสถานะของชิปแบบอื่น (การลงทะเบียนที่สร้างกุญแจใหม่ และ Protected Update ที่ทำให้ตัวนับ version ขึ้นถาวร) ถูกแยกเป็นแล็บเสริมที่ต้องได้รับอนุญาตจากผู้สอนก่อน
และการ provision secure boot ของอุปกรณ์อยู่นอกขอบเขตของแล็บ

## แหล่งอ้างอิงหลัก

- [TESAIoT PSE84 Dev Kit SDK (Apache-2.0) README](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/README.md)
- [Security / HSM (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__feat__security.html)
- [C4 — mTLS: the OPTIGA-backed TLS identity (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c4__mtls__optiga.html)
- [D2 — Enrolment and Protected Update end to end (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d2__enrolment__protected__update.html)
- [Infineon optiga-trust-m (host library, MIT) @ release-v5.8.3](https://github.com/Infineon/optiga-trust-m/tree/release-v5.8.3)
- [Infineon optiga-trust-m @ release-v5.3.0](https://github.com/Infineon/optiga-trust-m/tree/release-v5.3.0) รุ่นที่ SDK ใช้ตามไฟล์ `proj_cm55/deps/optiga-trust-m.mtb`
- ตัวอย่างบน TESAIoT Developer Hub: [device-servertls](https://dev.tesaiot.dev/?example=developer-hub--device-servertls&q=device-servertls) · [device-mtls](https://dev.tesaiot.dev/?example=developer-hub--device-mtls&q=device-mtls) · [c_ota_client](https://dev.tesaiot.dev/?example=developer-hub--c_ota_client&q=c_ota_client) · [pse84_tesaiot_client](https://dev.tesaiot.dev/?example=developer-hub--pse84_tesaiot_client&q=pse84_tesaiot_client) (Cypress EULA ลิงก์เท่านั้น)
- หลักสูตรคู่กัน: [TESAIoT Firmware Stack โมดูล 5 · เชื่อมต่อ TESAIoT Platform อย่างปลอดภัย](../tesaiot-firmware-stack/m05-connect-to-platform/README.md)
- [ETSI EN 303 645 V3.1.3 (2024-09) Cyber Security for Consumer Internet of Things: Baseline Requirements](https://www.etsi.org/deliver/etsi_en/303600_303699/303645/03.01.03_60/en_303645v030103p.pdf)

## สัญญาอนุญาต

- เนื้อหา CC BY-NC 4.0
- หลักสูตรนี้ไม่มีไฟล์โค้ดแยก โค้ดสั้น ๆ ที่เขียนขึ้นใหม่ในหน้าบทเรียนเป็น Apache-2.0
- โค้ดที่ยกมาสั้น ๆ พร้อมลิงก์ไปยังไฟล์และ commit มาจาก TESAIoT PSE84 Dev Kit SDK และ TESAIoT Developer Hub (Apache-2.0) และจากตัวอย่างของ Infineon optiga-trust-m (MIT) แต่ละชิ้นระบุที่มาและสัญญาอนุญาตไว้ตรงที่ยก
- โค้ดของตัวอย่าง `pse84_tesaiot_client` อยู่ภายใต้ Cypress (Infineon) EULA หลักสูตรนี้อ้างอิงด้วยลิงก์เท่านั้น ไม่คัดลอก และไฟล์ในโมดูล `tesaiot_mqtt` ของ SDK ที่พัฒนาต่อจากโปรเจกต์นั้นก็อ้างอิงด้วยลิงก์และสรุปความเท่านั้น

## อ้างอิง TESA

เมื่อนำหลักสูตรนี้ไปใช้ แบ่งปัน หรือดัดแปลง ต้องอ้างอิงดังนี้

> "Secure IoT กับ OPTIGA™ Trust M" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0

ถ้าแก้ไขเนื้อหา ให้เติม **(ดัดแปลง)** ต่อท้ายข้อความอ้างอิง พร้อมบอกสั้น ๆ ว่าเปลี่ยนอะไร
การอ้างอิงไม่ได้แปลว่า TESA รับรองงานของคุณ รายละเอียดและตัวอย่างอยู่ใน [ATTRIBUTION.md](../../ATTRIBUTION.md)
