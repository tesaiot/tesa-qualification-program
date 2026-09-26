# โมดูล 4 — เชื่อมต่อแพลตฟอร์ม IoT

> IoT Platform Connectivity · [หน้าหลักสูตร](../README.md)

ต่อ WiFi อ่านค่าเครือข่ายให้เป็น ส่ง telemetry และรับ command ผ่าน MQTT ขึ้นแพลตฟอร์มที่ติดตั้งเอง แล้วย้ายขึ้น MQTTs ผ่าน TLS

## เป้าหมายของโมดูล

พาบอร์ดขึ้นเครือข่ายแบบวินิจฉัยได้เมื่อมันพัง (dBm, DHCP, gateway, DNS) ส่งข้อมูลจริงสองทางผ่าน MQTT ขึ้น TESAIoT Community Edition ที่ติดตั้งเอง และส่งค่าเดิมผ่านช่องทางที่เข้ารหัส TLS พร้อมตอบได้ว่ามันปกป้องอะไร

## เครือข่ายและแพลตฟอร์มที่ใช้เมื่อเรียนเอง

- **WiFi:** WiFi บ้านหรือ Hotspot มือถือของคุณ ตั้งตามตารางในบทเรียน 1.4 (ชื่อภาษาอังกฤษไม่มีช่องว่าง รหัสอย่างน้อย 8 ตัว ย่าน 2.4 GHz) WiFi ที่ต้อง login ผ่านหน้าเว็บ บอร์ดใช้ไม่ได้
- **MQTT ธรรมดา (พอร์ต 1883):** broker ฝึกสาธารณะ `broker.hivemq.com` (สำรอง `test.mosquitto.org`) ใช้รหัสที่ไม่ซ้ำใครใน `client_id` และ topic เช่นชื่อเล่นต่อด้วยเลขสุ่ม 4 หลัก (`nok4821`) หรือ [TESAIoT Community Edition](https://github.com/tesaiot/tesaiot-community-edition) ที่ติดตั้งบนคอมของคุณเอง (บทเรียน 4.5–4.6)
- **MQTTs (บทเรียน 4.7–4.9):** บัญชี TESAIoT Platform ของคุณ ค่าประจำตัวของอุปกรณ์ได้จากหน้าจัดการอุปกรณ์ของแพลตฟอร์ม (CE ที่ติดตั้งเองใช้กับ MQTTs จากบอร์ดไม่ได้ เพราะ root CA ไม่ตรงกับที่ฝังในเฟิร์มแวร์ ดูบทเรียน 4.7)
- ถ้าเรียนเป็นกลุ่ม ผู้จัดอาจเตรียม broker และตัวตนของอุปกรณ์ไว้ให้

## บทเรียน

| บทเรียน | เรื่อง | เวลา (นาที) | สไลด์ |
|---|---|---|---|
| [4.1](l01-wifi-networking/README.md) | WiFi และเครือข่าย: dBm DHCP IP และ DNS | 50 | [slides.md](l01-wifi-networking/slides.md) |
| [4.2](l02-network-status-code/README.md) | จอสถานะเครือข่าย: แกะโค้ดโมดูล wifi | 55 | [slides.md](l02-network-status-code/slides.md) |
| [4.3](l03-network-status-lab/README.md) | ลงมือทำ: หน้าสถานะเครือข่ายของทีม | 65 | [slides.md](l03-network-status-lab/slides.md) |
| [4.4](l04-mqtt-concepts/README.md) | MQTT: pub/sub topic QoS และงบข้อมูล | 55 | [slides.md](l04-mqtt-concepts/slides.md) |
| [4.5](l05-mqtt-platform/README.md) | MQTT กับแพลตฟอร์มที่ติดตั้งเอง: telemetry และ command | 75 | [slides.md](l05-mqtt-platform/slides.md) |
| [4.6](l06-mqtt-telemetry-lab/README.md) | ลงมือทำ: telemetry สองทาง | 65 | [slides.md](l06-mqtt-telemetry-lab/slides.md) |
| [4.7](l07-tls-concepts/README.md) | TLS: ใบรับรอง ห่วงโซ่ความเชื่อถือ และการจับมือ | 55 | [slides.md](l07-tls-concepts/slides.md) |
| [4.8](l08-tesaiot-module/README.md) | โมดูล tesaiot: MQTTs สู่แพลตฟอร์ม | 75 | [slides.md](l08-tesaiot-module/slides.md) |
| [4.9](l09-secure-telemetry-lab/README.md) | ลงมือทำ: ส่งค่าจริงผ่านช่องทางเข้ารหัส | 70 | [slides.md](l09-secure-telemetry-lab/slides.md) |

บทเรียนในโมดูลนี้มาเป็นชุด ชุดละสามบทเรียน: แนวคิด → แกะโค้ด → ลงมือทำ (บทเรียนที่สามของแต่ละชุดมีไฟล์ฝึกและเฉลย)

## เช็กพอยต์ของโมดูล

ผ่านโมดูลนี้เมื่อทำได้ครบทุกข้อ (รายละเอียดอยู่ในหัวข้อ **แล็บ** ของบทเรียนลงมือทำ):

- [ ] หน้าสถานะเครือข่ายแสดงตารางวงเรียงตามความแรง เลข IP จาก DHCP และเวลา ping ที่อัปเดตทุก 3 วินาที
- [ ] อธิบายได้ว่าถ้า gateway ผ่านแต่อินเทอร์เน็ตเงียบ ปัญหาอยู่ที่ไหน
- [ ] publish JSON จากเซนเซอร์จริงทุก 5 วินาที และคำสั่ง `{"cmd":"toggle"}` สลับไฟบนบอร์ดได้
- [ ] telemetry ของทีมขึ้น dashboard ของแพลตฟอร์มผ่าน TLS และตอบได้ว่า serverTLS ปกป้องอะไรและไม่ปกป้องอะไร
