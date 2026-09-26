# พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge

ระดับ **L3** · สถานะ **pre-alpha (โครงร่าง อยู่ระหว่างเขียน)** · 6 โมดูล 17 บทเรียน · ประมาณ 30 ชั่วโมง

หลักสูตรนี้ปิดช่องว่างที่ใหญ่ที่สุดของคลังความรู้ คือทักษะวิศวกรรมพื้นฐานที่ Embedded Systems Engineering Roadmap จัดเป็นระดับจำเป็น
ได้แก่ ภาษา C การจัดการหน่วยความจำ การ build การดีบัก อุปกรณ์ต่อพ่วง โปรโตคอลพื้นฐาน และการทดสอบ
ทุกบทผูกกับตัวอย่างภาษา C ที่มีอยู่จริงใน [TESAIoT PSE84 Dev Kit SDK](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) (Apache-2.0)
โดยลิงก์ไปยัง commit `ef72c1b` ที่ตรึงไว้ ตรงไหนที่ SDK ยังไม่มีตัวอย่าง บทเรียนจะบอกไว้ตรง ๆ และอ้างเอกสารของผู้ผลิตชิปแทน

## เหมาะกับใคร

- นักพัฒนาที่เขียน MicroPython หรือภาษาอื่นได้แล้ว และต้องการก้าวไปทำเฟิร์มแวร์ภาษา C
- นักศึกษาที่ผ่านหลักสูตร AIoT in Action หรือเทียบเท่า
- ต้องมีบอร์ด TESAIoT Dev Kit (แม่แบบเฟิร์มแวร์ของ SDK ที่ commit นี้รองรับบอร์ด KIT_PSE84_AI) เครื่องมือ ModusToolbox และสำหรับโมดูล 5 ต้องมี logic analyzer

## เมื่อจบหลักสูตร คุณจะทำได้

1. เขียนโค้ดภาษา C ที่จัดการบิต รีจิสเตอร์ และหน่วยความจำบนไมโครคอนโทรลเลอร์อย่างปลอดภัย โดยอธิบายได้ว่าข้อมูลแต่ละก้อนอยู่ที่ใดในหน่วยความจำ
2. build แฟลช และจัดการเวอร์ชันของเฟิร์มแวร์ด้วย ModusToolbox, Make และ Git ได้ซ้ำได้ทุกครั้ง
3. ดีบักเฟิร์มแวร์ด้วย SWD และ GDB และวินิจฉัยความผิดพลาดจากหลักฐาน ไม่ใช่การเดา
4. ใช้ GPIO, interrupt, timer, watchdog และ DMA ตามกติกาของบริบท ISR และ RTOS ได้ถูกต้อง
5. สื่อสารผ่าน UART, I2C และ SPI และยืนยันสัญญาณด้วย logic analyzer ได้
6. แยกตรรกะออกจากฮาร์ดแวร์เพื่อเขียน unit test บนเครื่องโฮสต์ และตั้ง CI ให้ตรวจทุกการเปลี่ยนแปลง

## โมดูลและบทเรียน

### [โมดูล 1 · ภาษา C สำหรับไมโครคอนโทรลเลอร์และหน่วยความจำ](m01-c-and-memory/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| c-found.m01.l01 | [ภาษา C บนไมโครคอนโทรลเลอร์](m01-c-and-memory/l01-c-on-a-microcontroller/README.md) | 70 นาที |
| c-found.m01.l02 | [แผนที่หน่วยความจำ stack และ heap](m01-c-and-memory/l02-memory-map-stack-heap/README.md) | 70 นาที |
| c-found.m01.l03 | [struct, pointer และบัฟเฟอร์วงแหวน](m01-c-and-memory/l03-structs-pointers-buffers/README.md) | 70 นาที |

### [โมดูล 2 · Build ด้วย ModusToolbox และ Make และ Git สำหรับเฟิร์มแวร์](m02-build-and-version/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| c-found.m02.l01 | [ชุดเครื่องมือและการ build ครั้งแรก](m02-build-and-version/l01-toolchain-first-build/README.md) | 70 นาที |
| c-found.m02.l02 | [Make และตัวแปรของการ build](m02-build-and-version/l02-make-and-build-flags/README.md) | 70 นาที |
| c-found.m02.l03 | [Git สำหรับงานเฟิร์มแวร์](m02-build-and-version/l03-git-for-firmware/README.md) | 70 นาที |

### [โมดูล 3 · ดีบักด้วย SWD และ GDB](m03-debugging/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| c-found.m03.l01 | [SWD และ GDB เบื้องต้น](m03-debugging/l01-swd-and-gdb/README.md) | 70 นาที |
| c-found.m03.l02 | [วินิจฉัยความผิดพลาดจากหลักฐาน](m03-debugging/l02-diagnosing-faults/README.md) | 70 นาที |

### [โมดูล 4 · Timer, Interrupt, Watchdog, DMA และสัญญาณนาฬิกา](m04-peripherals/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| c-found.m04.l01 | [GPIO และ interrupt](m04-peripherals/l01-gpio-and-interrupts/README.md) | 70 นาที |
| c-found.m04.l02 | [Timer และสัญญาณนาฬิกา](m04-peripherals/l02-timers-and-clocks/README.md) | 70 นาที |
| c-found.m04.l03 | [Watchdog](m04-peripherals/l03-watchdog/README.md) | 70 นาที |
| c-found.m04.l04 | [DMA](m04-peripherals/l04-dma/README.md) | 70 นาที |

### [โมดูล 5 · UART, I2C และ SPI กับ logic analyzer](m05-serial-buses/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| c-found.m05.l01 | [UART](m05-serial-buses/l01-uart/README.md) | 70 นาที |
| c-found.m05.l02 | [I2C](m05-serial-buses/l02-i2c/README.md) | 70 นาที |
| c-found.m05.l03 | [SPI](m05-serial-buses/l03-spi/README.md) | 70 นาที |

### [โมดูล 6 · Unit test และ CI](m06-test-and-ci/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| c-found.m06.l01 | [Unit test บนเครื่องโฮสต์](m06-test-and-ci/l01-unit-tests-on-host/README.md) | 70 นาที |
| c-found.m06.l02 | [CI สำหรับเฟิร์มแวร์](m06-test-and-ci/l02-ci-for-firmware/README.md) | 70 นาที |

## สถานะของหลักสูตร

หลักสูตรนี้เป็นโครงร่าง (pre-alpha) ทุกบทเรียนมีเป้าหมาย ทักษะที่พัฒนา และแหล่งอ้างอิงที่ตรวจแล้ว แต่ยังไม่มีเนื้อหา แบบฝึก และเช็กความเข้าใจ
ลิงก์ไปยัง SDK ทุกลิงก์ตรึงไว้ที่ commit เดียวกัน และตรวจแล้วว่าไฟล์มีอยู่จริง ณ commit นั้น
ตัวอย่างของ Infineon ใช้วิธีลิงก์ไปยัง repository และ tag ไม่คัดลอกมา

## แหล่งอ้างอิงหลัก

- [TESAIoT PSE84 Dev Kit SDK (Apache-2.0) README](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/README.md)
- [แม่แบบเฟิร์มแวร์ mtb-only: README](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/README.en.md)
- [แคตตาล็อกตัวอย่างภาษา C ของ SDK](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/README.en.md)
- [A1 — From the zip to your first program (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__a1__first__build.html)
- [Infineon mtb-pdl-cat1 (Peripheral Driver Library) @ release-v3.24.0](https://github.com/Infineon/mtb-pdl-cat1/tree/release-v3.24.0)

## สัญญาอนุญาต

- เนื้อหา CC BY 4.0
- โค้ดใหม่ที่จะเพิ่มในหลักสูตรนี้ Apache-2.0
- โค้ดของ SDK และของ Infineon ไม่ได้คัดลอกมา ใช้สัญญาอนุญาตของต้นทางตามลิงก์

## อ้างอิง TESA

เมื่อนำหลักสูตรนี้ไปใช้ แบ่งปัน หรือดัดแปลง ต้องอ้างอิงดังนี้

> "พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0

ถ้าแก้ไขเนื้อหา ให้เติม **(ดัดแปลง)** ต่อท้ายข้อความอ้างอิง พร้อมบอกสั้น ๆ ว่าเปลี่ยนอะไร
การอ้างอิงไม่ได้แปลว่า TESA รับรองงานของคุณ รายละเอียดและตัวอย่างอยู่ใน [ATTRIBUTION.md](../../ATTRIBUTION.md)
