# TESAIoT Firmware Stack: เฟิร์มแวร์ภาษา C บน TESAIoT Dev Kit

หลักสูตรหลักของ TESA Qualification Program สำหรับนักพัฒนา เขียนเฟิร์มแวร์ภาษา C บน **TESAIoT Dev Kit**
(PSoC Edge AI Kit SoM บนบอร์ดฐาน QWA309) ด้วย ModusToolbox และ **master template** ของ TESA
ทุกบทเรียนผูกกับตัวอย่างจริงบน [TESAIoT Developer Hub](https://dev.tesaiot.dev/)
([github.com/tesaiot/developer-hub](https://github.com/tesaiot/developer-hub)) ที่อ้างอิงถึง commit ที่แน่นอน

| | |
|---|---|
| ระดับ | L3 ทำได้เอง |
| เวลา | ประมาณ 26 ชั่วโมง |
| บอร์ด | TESAIoT Dev Kit (โมดูล 5 บทเรียน 5.3 ใช้ Eva Kit ตาม BSP ของตัวอย่าง) |
| เครื่องมือ | ModusToolbox 3.6 ขึ้นไป, git, สาย USB-C สำหรับ KitProg3 |
| พื้นฐานที่ควรมี | ภาษา C ระดับ L2 (ตัวแปร ฟังก์ชัน pointer และ struct เบื้องต้น) |

## จะทำอะไรได้เมื่อจบหลักสูตร

1. build และ flash เฟิร์มแวร์ภาษา C ลง TESAIoT Dev Kit ด้วย ModusToolbox และ master template ได้ด้วยตัวเอง
2. สร้าง HMI บนจอสัมผัสด้วย LVGL ตั้งแต่ label จนถึง Wi-Fi Manager ที่มี state machine และเก็บโปรไฟล์ใน NVM
3. อ่านเซนเซอร์ทุกตัวบนบอร์ดและไมโครโฟน PDM แล้วรวมเป็นแดชบอร์ดที่ไม่กระตุก
4. ใช้ GPIO ADC I2C CAN UART SPI และ PWM บนบอร์ดฐาน QWA309 และยืนยันสัญญาณด้วยเครื่องมือวัด
5. ส่งข้อมูลขึ้น TESAIoT Platform ด้วย Server-TLS และ mTLS และอธิบายบทบาทของ OPTIGA™ Trust M และ OTA

## โมดูล

| โมดูล | บทเรียน | ที่มาของตัวอย่าง |
|---|---|---|
| [1 · เริ่มต้นกับ TESAIoT Dev Kit](m01-getting-started/README.md) | 1 | master template (`tesaiot_dev_kit_master`) |
| [2 · HMI Menu & Setting ด้วย LVGL](m02-hmi-menu-setting/README.md) | 7 | Episodes ชุดที่ 1 (`hmi_ep01`–`hmi_ep07`) |
| [3 · เซนเซอร์และเสียงบน TESAIoT Dev Kit](m03-interactive-sensors/README.md) | 7 | Episodes ชุดที่ 2 (`int_ep01`–`int_ep07`) |
| [4 · ฮาร์ดแวร์บนบอร์ดฐาน QWA309](m04-qwa309-hardware/README.md) | 5 | แบบฝึก `prac_qwa309_*` |
| [5 · เชื่อมต่อ TESAIoT Platform อย่างปลอดภัย](m05-connect-to-platform/README.md) | 4 | ตัวอย่าง `embedded-devices` และ `security` |

## เรียนอย่างไร

1. **ดูของจริงก่อน** เปิดตัวอย่างบน Developer Hub แล้ว flash เฟิร์มแวร์สำเร็จรูปลงบอร์ด (episode และแบบฝึก QWA309 มีให้ทุกตัว)
2. **อ่าน Why / What / How** ใน README ของตัวอย่าง แล้วไล่โค้ดตามลำดับไฟล์ที่บทเรียนแนะนำ
3. **build เอง** วางไฟล์ของตัวอย่างลงใน `proj_cm55/apps/` ของ master template แล้ว `make build` และ `make program`
4. **ลองแก้** ทายก่อนแก้ แล้วเทียบผลบนบอร์ด จากนั้นต่อยอดหนึ่งอย่างและเก็บไว้ใน portfolio
5. **เช็กความเข้าใจ** ตอบคำถามท้ายบทเรียนให้ได้ก่อนไปบทถัดไป

## โค้ดอยู่ที่ไหน

โค้ดทั้งหมดอยู่ใน Developer Hub และถูกอ้างอิงด้วยลิงก์ที่ pin ไว้ ไม่ได้คัดลอกเข้าคลังนี้ เพื่อให้มีต้นฉบับเดียว
episode แบบฝึก และตัวอย่างใน branch `main` เป็น Apache-2.0 ส่วน master template กับตัวอย่าง OPTIGA อยู่ภายใต้ EULA ของ
Infineon/Cypress

## ความสัมพันธ์กับหลักสูตรอื่น

- ถ้ายังไม่เคยเขียนโปรแกรมบนไมโครคอนโทรลเลอร์ เริ่มที่ [AIoT in Action (MicroPython)](../aiot-micropython/README.md) หรือ [Explorer](../explorer/README.md)
- พื้นฐานภาษา C สำหรับไมโครคอนโทรลเลอร์ การ debug และการทดสอบ อยู่ใน [พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge](../embedded-c-foundations/README.md) (อยู่ระหว่างเขียน)
- ต่อยอดด้านความปลอดภัยที่ [Secure IoT กับ OPTIGA™ Trust M](../secure-iot-optiga/README.md)

## อ้างอิง TESA

เมื่อนำหลักสูตรนี้หรือบางบทเรียนไปใช้ ให้ใส่ข้อความนี้ในจุดที่ผู้เรียนเห็น และเติม «(ดัดแปลง)» เมื่อมีการแก้ไข

> "TESAIoT Firmware Stack: เฟิร์มแวร์ภาษา C บน TESAIoT Dev Kit" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
> (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0

ตัวอย่างโค้ดเป็นผลงานของ TESAIoT Firmware Stack โดยสมาคมสมองกลฝังตัวไทย (TESA) ใน [tesaiot/developer-hub](https://github.com/tesaiot/developer-hub)
รายละเอียดการให้เครดิตอยู่ที่ [ATTRIBUTION.md](../../ATTRIBUTION.md)
