# โมดูล 4 — การเขียนเฟิร์มแวร์แบบ RTOS

*RTOS Firmware Programming* · หลักสูตร [TESA Firmware SDK สำหรับ Edge AI](../README.md)

## เป้าหมาย

แยกงานตามความรับผิดชอบและจังหวะเวลาด้วย FreeRTOS: task, priority, queue, mutex, semaphore และ event group พร้อมกฎของ ISR

## บทเรียน

| # | บทเรียน | เนื้อหา |
|---|---|---|
| 1 | [เฟิร์มแวร์หลาย task ด้วย FreeRTOS](l01-freertos-programming/README.md) | สร้าง task ที่มีคาบเวลา เลือก priority ส่งข้อมูลด้วย queue ป้องกันบัสด้วย mutex ส่งสัญญาณด้วย semaphore/event group และเคารพกฎของ ISR |
| 2 | [แล็บ: เฟิร์มแวร์หลาย task ด้วย FreeRTOS](l02-lab/README.md) | สร้างสอง task คาบต่างกัน ส่งเหตุการณ์ปุ่มผ่าน queue ป้องกันบัสร่วมด้วย mutex แล้วเขียนโน้ตเรื่อง timing |

เวลาโดยประมาณตามต้นฉบับ: ประมาณ 3.5–4 ชั่วโมง (บทเรียน) + แล็บ 2.5–3.5 ชั่วโมง

ชีตและแม่แบบประกอบ (อยู่ในโฟลเดอร์ `resources/` ของบทเรียนที่ 1):

- [rtos-patterns.md](l01-freertos-programming/resources/rtos-patterns.md)

> โค้ด C ในโมดูลนี้ใช้ API ของเฟิร์มแวร์ TESAIoT Bitstream ซึ่งยังไม่เปิดซอร์ส อ่านหมายเหตุต้น[บทเรียน](l01-freertos-programming/README.md) ก่อนลงมือ

## จุดตรวจ

ก่อนไปโมดูลถัดไป ตรวจว่าคุณทำสิ่งเหล่านี้ได้แล้ว:

- [ ] สอง task กระพริบ LED ด้วยคาบเวลาต่างกันโดยไม่ busy-wait
- [ ] เหตุการณ์ปุ่มเดินทางผ่าน queue ไปยัง task ที่พิมพ์ UART
- [ ] ทรัพยากรที่ใช้ร่วมถูกป้องกันด้วย mutex หรือ API ล็อกบัส
- [ ] ตอบคำถาม timing ใน Lab E ครบ

[← โมดูล 3](../m03-gpio-peripherals/README.md) · [หน้าหลักสูตร](../README.md) · [โมดูล 5 →](../m05-sensor-data/README.md)
