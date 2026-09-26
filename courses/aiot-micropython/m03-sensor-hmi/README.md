# โมดูล 3 — แสดงผลเซนเซอร์บน HMI

> Sensor Visualization on HMI · [หน้าหลักสูตร](../README.md)

แปลงความเร่งเป็นมุมเอียง สุ่มสัญญาณให้ถูกแล้ววาดกราฟ real-time และประกอบ Mini-HMI Dashboard สี่การ์ดที่รันต่อเนื่องได้

## เป้าหมายของโมดูล

อ่านเซนเซอร์จริง (IMU เข็มทิศ CapSense ลูกบิด) แล้วเล่าออกมาบนจอให้คนอ่านรู้เรื่อง: เครื่องวัดระดับสองแกน กราฟความเร่งสามแกนที่รู้คาบเวลาของลูปจริง และแดชบอร์ดสี่การ์ดที่อยู่ในงบ widget และรันได้สิบนาที

## บทเรียน

| บทเรียน | เรื่อง | เวลา (นาที) | สไลด์ |
|---|---|---|---|
| [3.1](l01-accelerometer-tilt/README.md) | accelerometer กับมุมเอียง: roll และ pitch | 45 | [slides.md](l01-accelerometer-tilt/slides.md) |
| [3.2](l02-gyro-fusion/README.md) | gyro ฟิลเตอร์ complementary และโค้ดเครื่องวัดระดับ | 55 | [slides.md](l02-gyro-fusion/slides.md) |
| [3.3](l03-digital-level-lab/README.md) | ลงมือทำ: เครื่องวัดระดับดิจิทัล | 70 | [slides.md](l03-digital-level-lab/slides.md) |
| [3.4](l04-sampling/README.md) | สุ่มสัญญาณให้ถูก: Nyquist aliasing และ ring buffer | 50 | [slides.md](l04-sampling/slides.md) |
| [3.5](l05-realtime-chart/README.md) | ui.Chart: กราฟหลาย series และคาบเวลาของลูปจริง | 55 | [slides.md](l05-realtime-chart/slides.md) |
| [3.6](l06-accel-chart-lab/README.md) | ลงมือทำ: กราฟความเร่งสามแกน | 70 | [slides.md](l06-accel-chart-lab/slides.md) |
| [3.7](l07-hmi-design/README.md) | ออกแบบ HMI: การ์ด ลำดับสายตา สี และงบ widget | 55 | [slides.md](l07-hmi-design/slides.md) |
| [3.8](l08-dashboard-build/README.md) | ประกอบแดชบอร์ด: สี่การ์ดในลูปเดียว | 60 | [slides.md](l08-dashboard-build/slides.md) |
| [3.9](l09-dashboard-lab/README.md) | ลงมือทำ: Mini-HMI Dashboard และการทดสอบ 10 นาที | 75 | [slides.md](l09-dashboard-lab/slides.md) |

บทเรียนในโมดูลนี้มาเป็นชุด ชุดละสามบทเรียน: แนวคิด → แกะโค้ด → ลงมือทำ (บทเรียนที่สามของแต่ละชุดมีไฟล์ฝึกและเฉลย)

## เช็กพอยต์ของโมดูล

ผ่านโมดูลนี้เมื่อทำได้ครบทุกข้อ (รายละเอียดอยู่ในหัวข้อ **แล็บ** ของบทเรียนลงมือทำ):

- [ ] วางราบแล้วอ่านได้ราว 0° เอียงแล้วแถบ roll/pitch วิ่งถูกทิศ และไฟเกินเกณฑ์ติดทีละดวง
- [ ] กราฟสามเส้นวิ่งสด ปุ่มหยุดหยุดข้อมูลจริง และจอบอกคาบลูปจริงเป็นมิลลิวินาที
- [ ] อธิบาย aliasing ได้จากตัวเลขคาบเวลาของลูปตัวเอง
- [ ] แดชบอร์ดสี่การ์ดไม่เกินงบ 32 widget และรันต่อเนื่อง 10 นาทีโดยไม่ค้างและไม่มี Traceback
