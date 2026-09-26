# อิเล็กทรอนิกส์และเครื่องมือวัดสำหรับนักพัฒนาระบบฝังตัว

ระดับ **L2** · สถานะ **alpha (ทดลองใช้)** · 6 โมดูล 15 บทเรียน · ประมาณ 20 ชั่วโมง

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

## ตัวอย่างบนบอร์ดที่ใช้ในแล็บ

แล็บส่วนใหญ่ใช้ตัวอย่างชุด QWA309 ของ Developer Hub เป็นแหล่งสัญญาณให้วัด ตัวอย่างชุดนี้รันบน TESAIoT Dev Kit เท่านั้น
ทุกแล็บบอกวิธีทำแทนสำหรับ Eva Kit ไว้ด้วย (ส่วนใหญ่คือเขียนโปรแกรมสั้น ๆ สร้างสัญญาณเดียวกันบนขาว่าง)

| ตัวอย่าง | ใช้ในบทเรียน |
|---|---|
| [QWA309 Potentiometer Monitor](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_pot_monitor&q=prac_qwa309_pot_monitor) | วงจรแบ่งแรงดันและ ADC, อ่านแผนผังวงจร |
| [QWA309 4-Channel ADC Scope](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_adc_scope&q=prac_qwa309_adc_scope) | วงจรแบ่งแรงดันและ ADC |
| [QWA309 Push Button Monitor](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_button_monitor&q=prac_qwa309_button_monitor) | Pull-up, pull-down และปุ่มกด |
| [QWA309 Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) | ระดับลอจิก ปุ่มกด logic analyzer ถอดรหัส I2C และ UART ออสซิลโลสโคป วัด PWM เบรดบอร์ด |

## สิ่งที่ต้องเตรียม

- บอร์ด TESAIoT Dev Kit (หรือ Eva Kit) พร้อมสาย USB
- มัลติมิเตอร์แบบดิจิทัลที่มีช่อง mA และคู่มือของเครื่อง
- logic analyzer ราคาประหยัดที่ใช้กับ PulseView ได้
- ออสซิลโลสโคปพร้อมโพรบ 10× (ของห้องแล็บ หรือแบบต่อ USB)
- เบรดบอร์ด สายจัมเปอร์ ตัวต้านทานชุดพื้นฐาน LED ปุ่มกด ตัวเก็บประจุ 100 µF
- หัวแร้งแบบปรับอุณหภูมิ แผ่นฝึกบัดกรี แว่นตานิรภัย สายรัดข้อมือกันไฟฟ้าสถิต และเครื่องดูดควัน (โมดูล 6)

## สถานะของหลักสูตร

หลักสูตรนี้อยู่ในสถานะ alpha (ทดลองใช้) ทุกบทเรียนมีแนวคิดพร้อมตัวอย่างคำนวณ ตัวอย่างสมบูรณ์ แบบฝึกพร้อมเฉลย แล็บ และคำถามเช็กความเข้าใจ
หน้าบทเรียนเป็นภาษาไทย หน้าภาษาอังกฤษของแต่ละบทยังรอแปล แผนภาพทั้งหมดเป็นงานวาดของหลักสูตรนี้เอง (CC BY-NC 4.0) ถ้าพบตัวเลขหรือขั้นตอนที่ผิด แจ้งได้ตาม [CONTRIBUTING.md](../../CONTRIBUTING.md)

**ความปลอดภัย** ทุกแล็บในหลักสูตรนี้ใช้ไฟแรงดันต่ำจากบอร์ดหรือแหล่งจ่ายห้องแล็บเท่านั้น ห้ามวัดไฟบ้าน
แต่ละบทเรียนมีข้อควรระวังของตัวเอง เช่น การวัดกระแส สายกราวด์ของโพรบ หัวแร้ง ควันฟลักซ์ และไฟฟ้าสถิต อ่านก่อนเริ่มแล็บทุกครั้ง

## แหล่งอ้างอิงหลัก

- [Lessons In Electric Circuits โดย Tony R. Kuphaldt (หนังสือเปิด)](https://www.ibiblio.org/kuphaldt/electricCircuits/)
- [OpenStax University Physics Volume 2 (บทวงจรไฟฟ้ากระแสตรง)](https://openstax.org/details/books/university-physics-volume-2)
- [sigrok PulseView](https://sigrok.org/wiki/PulseView)
- [sigrok protocol decoders](https://sigrok.org/wiki/Protocol_decoders)
- [AIoT in Action: examples/s05/05_adc_counts_to_volts.py (MIT)](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s05/05_adc_counts_to_volts.py)
- [TESAIoT Dev Kit SDK: แผนผังความสามารถของบอร์ดฐาน QWA309 (Apache-2.0)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-mpy/bento_libs/claw/kit-tesaiot-pse84-ai/README.md)
- [Developer Hub: แบบฝึกของ TESAIoT Dev Kit (commit 372d0d8)](https://github.com/tesaiot/developer-hub/tree/372d0d849578a6a49b634d3ecaab8b5958166921)

## สัญญาอนุญาต

- เนื้อหาและแผนภาพ CC BY-NC 4.0
- หลักสูตรนี้ยังไม่มีไฟล์โค้ดของตัวเอง ถ้าเพิ่มในอนาคตจะใช้ Apache-2.0
- ตัวอย่าง MicroPython ที่อ้างถึงเป็นของหลักสูตร AIoT in Action (MIT) ตัวอย่าง C เป็นของ Developer Hub และ SDK ของ TESAIoT Dev Kit ทั้งหมดอ้างอิงด้วยลิงก์ ไม่ได้คัดลอกเข้าคลังนี้

## อ้างอิง TESA

เมื่อนำหลักสูตรนี้ไปใช้ แบ่งปัน หรือดัดแปลง ต้องอ้างอิงดังนี้

> "อิเล็กทรอนิกส์และเครื่องมือวัดสำหรับนักพัฒนาระบบฝังตัว" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0

ถ้าแก้ไขเนื้อหา ให้เติม **(ดัดแปลง)** ต่อท้ายข้อความอ้างอิง พร้อมบอกสั้น ๆ ว่าเปลี่ยนอะไร
การอ้างอิงไม่ได้แปลว่า TESA รับรองงานของคุณ รายละเอียดและตัวอย่างอยู่ใน [ATTRIBUTION.md](../../ATTRIBUTION.md)
