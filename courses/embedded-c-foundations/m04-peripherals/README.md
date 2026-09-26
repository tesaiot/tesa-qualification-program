# โมดูล 4 · Timer, Interrupt, Watchdog, DMA และสัญญาณนาฬิกา

**เป้าหมายของโมดูล** ใช้อุปกรณ์ต่อพ่วงหลักของไมโครคอนโทรลเลอร์ตามกติกาของบริบท ISR และ RTOS

สถานะ **pre-alpha** (อยู่ระหว่างเขียน) · เวลาโดยประมาณ 280 นาที

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| [c-found.m04.l01](l01-gpio-and-interrupts/README.md) | GPIO และ interrupt | 70 นาที |
| [c-found.m04.l02](l02-timers-and-clocks/README.md) | Timer และสัญญาณนาฬิกา | 70 นาที |
| [c-found.m04.l03](l03-watchdog/README.md) | Watchdog | 70 นาที |
| [c-found.m04.l04](l04-dma/README.md) | DMA | 70 นาที |

## Checkpoint ท้ายโมดูล

- [ ] อ่านปุ่มด้วย interrupt และกันเด้งโดยไม่บล็อก
- [ ] ตั้งงานเป็นจังหวะด้วย timer และอธิบายผลของสัญญาณนาฬิกาต่อความแม่นยำ
- [ ] อธิบายตำแหน่งที่ถูกต้องของการป้อน watchdog ในโปรแกรมตัวอย่าง
