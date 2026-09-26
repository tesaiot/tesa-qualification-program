# อิเล็กทรอนิกส์และเครื่องมือวัดสำหรับนักพัฒนาระบบฝังตัว

ระดับ **L2** · สถานะ **pre-alpha (โครงร่าง อยู่ระหว่างเขียน)** · 6 โมดูล 15 บทเรียน · ประมาณ 20 ชั่วโมง

หลักสูตรนี้ปิดช่องว่างเรื่องอิเล็กทรอนิกส์และเครื่องมือวัด ซึ่ง Embedded Systems Engineering Roadmap จัดเป็นทักษะจำเป็น
และคุณวุฒิวิชาชีพนักพัฒนาระบบสมองกลฝังตัว ระดับ 4 ของ TPQI ก็มีหน่วยสมรรถนะด้านการพัฒนาฮาร์ดแวร์ (ICT-CSOS-107B)
ทุกบทผูกกับสิ่งที่วัดได้บนบอร์ด Eva Kit หรือ TESAIoT Dev Kit เช่น ลูกบิดที่เป็นวงจรแบ่งแรงดัน ปุ่มแบบ active-low หลอด LED ที่หรี่ด้วย PWM และบัส I2C ของเซนเซอร์
อีมูเลเตอร์ช่วยเรื่องนี้ไม่ได้ หลักสูตรนี้ต้องใช้บอร์ดและเครื่องมือวัดจริง

## เหมาะกับใคร

- นักศึกษาและนักพัฒนาที่เขียนโปรแกรมได้แล้ว แต่ยังไม่เคยใช้เครื่องมือวัด
- ผู้ที่ผ่าน Explorer หรือ AIoT in Action และอยากเข้าใจว่าบนบอร์ดเกิดอะไรขึ้นจริง
- ต้องมีบอร์ด มัลติมิเตอร์ logic analyzer ราคาประหยัดที่ใช้กับ sigrok ได้ และถ้าเป็นไปได้ ออสซิลโลสโคปของห้องแล็บ

## เมื่อจบหลักสูตร คุณจะทำได้

1. คำนวณแรงดัน กระแส ความต้านทาน และกำลังในวงจรพื้นฐาน และออกแบบวงจรแบ่งแรงดันกับตัวต้านทานจำกัดกระแสได้
2. อธิบายระดับลอจิก pull-up และ pull-down และต่อปุ่มแบบ active-low ได้ถูกต้อง
3. วัดแรงดัน ความต่อเนื่อง และกระแสด้วยมัลติมิเตอร์อย่างปลอดภัย
4. จับและถอดรหัสสัญญาณดิจิทัลด้วย logic analyzer และวัดสัญญาณด้วยออสซิลโลสโคปได้
5. ต่อวงจรบนเบรดบอร์ด บัดกรีอย่างปลอดภัย อ่านแผนผังวงจร และอธิบายหลัก PCB และ EMC เบื้องต้นได้

## โมดูลและบทเรียน

### [โมดูล 1 · วงจรและอิเล็กทรอนิกส์พื้นฐาน](m01-circuits/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| elec.m01.l01 | [แรงดัน กระแส และความต้านทาน](m01-circuits/l01-voltage-current-resistance/README.md) | 65 นาที |
| elec.m01.l02 | [วงจรแบ่งแรงดันและเซนเซอร์แบบอนาล็อก](m01-circuits/l02-dividers-and-sensors/README.md) | 65 นาที |
| elec.m01.l03 | [ชิ้นส่วนพื้นฐาน: ตัวต้านทาน ตัวเก็บประจุ ไดโอด และทรานซิสเตอร์](m01-circuits/l03-components/README.md) | 65 นาที |

### [โมดูล 2 · วงจรดิจิทัล](m02-digital-logic/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| elec.m02.l01 | [ระดับลอจิกและเกตพื้นฐาน](m02-digital-logic/l01-logic-levels-and-gates/README.md) | 65 นาที |
| elec.m02.l02 | [Pull-up, pull-down และปุ่มกด](m02-digital-logic/l02-pullups-and-buttons/README.md) | 65 นาที |

### [โมดูล 3 · มัลติมิเตอร์](m03-multimeter/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| elec.m03.l01 | [วัดแรงดันและความต่อเนื่อง](m03-multimeter/l01-voltage-and-continuity/README.md) | 65 นาที |
| elec.m03.l02 | [วัดกระแสอย่างปลอดภัย](m03-multimeter/l02-current-safely/README.md) | 65 นาที |

### [โมดูล 4 · Logic analyzer และ protocol analyzer](m04-logic-analyzer/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| elec.m04.l01 | [จับสัญญาณดิจิทัลครั้งแรก](m04-logic-analyzer/l01-capture-a-signal/README.md) | 65 นาที |
| elec.m04.l02 | [ถอดรหัส I2C และ UART](m04-logic-analyzer/l02-decode-i2c-and-uart/README.md) | 65 นาที |

### [โมดูล 5 · ออสซิลโลสโคป](m05-oscilloscope/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| elec.m05.l01 | [ออสซิลโลสโคปเบื้องต้น](m05-oscilloscope/l01-scope-basics/README.md) | 65 นาที |
| elec.m05.l02 | [วัด PWM](m05-oscilloscope/l02-measuring-pwm/README.md) | 65 นาที |

### [โมดูล 6 · ต่อวงจร บัดกรี อ่านแผนผัง และพื้นฐาน PCB กับ EMC](m06-build-and-read/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| elec.m06.l01 | [ต่อวงจรบนเบรดบอร์ด](m06-build-and-read/l01-breadboarding/README.md) | 65 นาที |
| elec.m06.l02 | [บัดกรีอย่างปลอดภัย](m06-build-and-read/l02-soldering-safely/README.md) | 65 นาที |
| elec.m06.l03 | [อ่านแผนผังวงจร](m06-build-and-read/l03-reading-schematics/README.md) | 65 นาที |
| elec.m06.l04 | [พื้นฐาน PCB และ EMC](m06-build-and-read/l04-pcb-and-emc-basics/README.md) | 65 นาที |

## สถานะของหลักสูตร

หลักสูตรนี้เป็นโครงร่าง (pre-alpha) ทุกบทเรียนมีเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว แต่ยังไม่มีเนื้อหา แล็บ และเช็กความเข้าใจ
**ความปลอดภัย** ทุกแล็บในหลักสูตรนี้ใช้ไฟแรงดันต่ำจากบอร์ดหรือแหล่งจ่ายห้องแล็บเท่านั้น ห้ามวัดไฟบ้าน

## แหล่งอ้างอิงหลัก

- [Lessons In Electric Circuits โดย Tony R. Kuphaldt (หนังสือเปิด)](https://www.ibiblio.org/kuphaldt/electricCircuits/)
- [OpenStax University Physics Volume 2 (บทวงจรไฟฟ้ากระแสตรง)](https://openstax.org/details/books/university-physics-volume-2)
- [sigrok PulseView](https://sigrok.org/wiki/PulseView)
- [sigrok protocol decoders](https://sigrok.org/wiki/Protocol_decoders)
- [AIoT in Action: examples/s05/05_adc_counts_to_volts.py (MIT)](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s05/05_adc_counts_to_volts.py)

## สัญญาอนุญาต

- เนื้อหา CC BY 4.0
- โค้ดใหม่ที่จะเพิ่มในหลักสูตรนี้ Apache-2.0
- ตัวอย่าง MicroPython ที่อ้างถึงเป็นของหลักสูตร AIoT in Action (MIT) ลิงก์ไปยัง commit ที่ตรึงไว้

## อ้างอิง TESA

เมื่อนำหลักสูตรนี้ไปใช้ แบ่งปัน หรือดัดแปลง ต้องอ้างอิงดังนี้

> "อิเล็กทรอนิกส์และเครื่องมือวัดสำหรับนักพัฒนาระบบฝังตัว" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0

ถ้าแก้ไขเนื้อหา ให้เติม **(ดัดแปลง)** ต่อท้ายข้อความอ้างอิง พร้อมบอกสั้น ๆ ว่าเปลี่ยนอะไร
การอ้างอิงไม่ได้แปลว่า TESA รับรองงานของคุณ รายละเอียดและตัวอย่างอยู่ใน [ATTRIBUTION.md](../../ATTRIBUTION.md)
