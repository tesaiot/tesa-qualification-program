# โมดูล 3 — GPIO และอุปกรณ์ต่อพ่วงพื้นฐาน

*GPIO and Basic Peripherals* · หลักสูตร [TESA Firmware SDK สำหรับ Edge AI](../README.md)

## เป้าหมาย

คุยกับฮาร์ดแวร์ผ่านชั้น Driver: LED ปุ่ม UART I²C PWM และ ADC บนโปรเจกต์ที่ build/flash ได้จากโมดูล 2 แล้วรวมเป็นวงจรเล็ก ๆ

## บทเรียน

| # | บทเรียน | เนื้อหา |
|---|---|---|
| 1 | [GPIO และอุปกรณ์ต่อพ่วงผ่าน Driver API](l01-gpio-and-peripherals/README.md) | ควบคุม LED ปุ่ม UART I²C PWM และ ADC ผ่านชั้น Driver และรู้ว่า SPI กับ timer อยู่ตรงไหนในสแต็ก |
| 2 | [แล็บ: GPIO และอุปกรณ์ต่อพ่วงบนฮาร์ดแวร์จริง](l02-lab/README.md) | ลงมือทีละบล็อก: LED + ปุ่ม, UART log, แล้วเลือก PWM / ADC / I²C อย่างน้อยหนึ่งอย่าง ก่อนรวมเป็นมินิวงจร |

เวลาโดยประมาณตามต้นฉบับ: ประมาณ 3 ชั่วโมง (บทเรียน) + แล็บ 2.5–3 ชั่วโมง

ชีตและแม่แบบประกอบ (อยู่ในโฟลเดอร์ `resources/` ของบทเรียนที่ 1):

- [peripheral-api-map.md](l01-gpio-and-peripherals/resources/peripheral-api-map.md)

> โค้ด C ในโมดูลนี้ใช้ API ของเฟิร์มแวร์ TESAIoT Bitstream ซึ่งยังไม่เปิดซอร์ส อ่านหมายเหตุต้น[บทเรียน](l01-gpio-and-peripherals/README.md) ก่อนลงมือ

## จุดตรวจ

ก่อนไปโมดูลถัดไป ตรวจว่าคุณทำสิ่งเหล่านี้ได้แล้ว:

- [ ] ปุ่มสลับ LED บนบอร์ดจริงได้
- [ ] มี log ทาง UART ที่อ่านได้บน terminal
- [ ] ทำ PWM, ADC หรือ I²C ได้อย่างน้อยหนึ่งอย่าง และจดชื่อฟังก์ชันจริงที่เรียกลงชีต

[← โมดูล 2](../m02-toolchain/README.md) · [หน้าหลักสูตร](../README.md) · [โมดูล 4 →](../m04-rtos/README.md)
