# AIoT in Action: จากหน้าจอสัมผัสสู่แพลตฟอร์ม IoT (MicroPython)

> ดัดแปลงจาก AIoT in Action — Embedded Systems for AIoT Developer, © 2026 รศ.วิรุฬห์ ศรีบริรักษ์, Advance Innovation Centre (AIC) มหาวิทยาลัยบูรพา · BENTO & TESAIoT (CC BY 4.0 / MIT)

เรียน **AIoT** จากของจริงบนบอร์ด PSoC Edge — **Eva Kit** หรือ **TESAIoT Dev Kit** — ด้วยภาษา **MicroPython** เริ่มจากเล่นแอปที่มากับเครื่องให้เห็นปลายทางก่อน แล้วค่อย ๆ แกะลงไปทีละชั้นจนสร้างเองได้ทั้งวงจร:

**จอสัมผัส → ฮาร์ดแวร์ → เซนเซอร์ → เครือข่าย → MQTT → แพลตฟอร์ม IoT → ผลิตภัณฑ์ของเราเอง**

ตัวอย่างชุดเดียวกันรันได้ทั้งสองบอร์ด เพราะโค้ดถามบอร์ดเองว่ามีไฟกี่ดวง ปุ่มชื่ออะไร และมีเซนเซอร์อะไรบ้าง ไม่ต้องคอมไพล์ ไม่ต้องติดตั้ง toolchain ของภาษา C

## สำหรับใคร

- คนทั่วไปและผู้ประกอบการที่อยากเข้าใจว่าระบบ AIoT ทำงานอย่างไรจากของจริง ไม่ใช่จากภาพสไลด์
- นักพัฒนาซอฟต์แวร์ที่เขียน Python เป็นแล้ว และอยากลงมือกับฮาร์ดแวร์ เซนเซอร์ และ IoT
- ผู้เรียนสายวิศวกรรมหรือวิทยาศาสตร์ที่ต้องการพื้นฐานระบบสมองกลฝังตัวแบบลงมือทำ
- ผู้สอนที่ต้องการชุดบทเรียนพร้อมสไลด์ โค้ด ไฟล์ฝึก และเฉลย ไปใช้ในห้องเรียนของตัวเอง

พื้นฐานที่ควรมี: เขียน Python ระดับเบื้องต้นได้ (ตัวแปร if ลูป ฟังก์ชัน) ไม่ต้องมีพื้นฐานอิเล็กทรอนิกส์มาก่อน เรียนคนเดียวได้ และเรียนเป็นทีมสองถึงสี่คนต่อบอร์ดก็สนุก

## จบหลักสูตรแล้วทำอะไรได้

1. อธิบายสถาปัตยกรรมระบบ AIoT ว่าเซนเซอร์ การตัดสินใจบนอุปกรณ์ หน้าจอ และแพลตฟอร์มปลายทางแบ่งงานกันอย่างไร ตัดสินได้ว่างานใดควรจบบนบอร์ดและงานใดควรส่งออก และยกตัวอย่างการใช้งานในอุตสาหกรรมได้อย่างน้อยหนึ่งกรณี
2. เขียนโปรแกรม MicroPython ควบคุมฮาร์ดแวร์บนบอร์ด (LED ปุ่ม ปุ่มสัมผัส และค่าอนาล็อก) และสร้าง UI บนจอสัมผัสที่สถานะบนจอตรงกับสถานะของฮาร์ดแวร์จริงทุกครั้งที่ทดสอบ
3. อ่านข้อมูลเซนเซอร์ (IMU เข็มทิศ CapSense ลูกบิด) เลือกและใช้ตัวกรองสัญญาณที่เหมาะกับงาน แล้วออกแบบ HMI dashboard ที่แสดงผลแบบ real-time ภายในงบ widget และอัตราอัปเดตที่ตั้งไว้ และรันต่อเนื่องได้ 10 นาที
4. เชื่อมบอร์ดเข้า WiFi ส่งและรับข้อมูลผ่าน MQTT ทั้งสองทิศทาง และเปรียบเทียบช่องทางพอร์ต 1883 กับช่องทาง MQTTs ที่เข้ารหัส TLS (serverTLS) ได้ว่าอะไรปลอดภัยขึ้นและอะไรยังไม่ได้รับการปกป้อง
5. ประกอบทั้งหมดเป็น AIoT mini-product ที่แก้โจทย์จริงหนึ่งเรื่อง ทำงานต่อได้เมื่อเน็ตหลุด ส่งข้อมูลตาม schema ที่ออกแบบเอง และนำเสนอได้ภายใน 10 นาที

## ต้องมีอะไรบ้าง

- **บอร์ด** BENTO PSoC Edge **Eva Kit** (KIT_PSE84_EVAL_EPC2) หรือ **TESAIoT Dev Kit** (SoM KIT_PSE84_AI บนฐาน QWA309) ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว — **หรือไม่มีบอร์ดก็เริ่มได้** ด้วย BENTO Emulator ใน BENTO IDE (บางบทเรียนต้องใช้บอร์ดจริง ดูบรรทัด "อุปกรณ์" ในแต่ละบทเรียน)
- **BENTO IDE** — <https://ide.tesaiot.dev/> เขียนโค้ดแล้วกด **Program to Device** ได้จากเบราว์เซอร์ และมี BENTO Emulator ในตัว
- **WiFi** ตั้งแต่บทเรียน 1.4 (ต่อเน็ตครั้งแรก) และใช้จริงจังในโมดูล 4 · เครือข่ายที่ต้อง login ผ่านหน้าเว็บ บอร์ดใช้ไม่ได้ ให้ใช้ Hotspot จากมือถือแทน
- **TESAIoT Community Edition** สำหรับบทเรียน 4.4–4.9 และ capstone — แพลตฟอร์ม IoT ที่ติดตั้งเองได้ (<https://github.com/tesaiot/tesaiot-community-edition>)
- สมุดหรือไฟล์สำหรับ **บันทึกการเรียน** ของตัวเอง สไลด์จะบอกเป็นระยะว่าควรจดอะไร

สองบอร์ดต่างกันที่จำนวนไฟ (3 กับ 5 ดวง) เซนเซอร์เพิ่มบน Dev Kit (SHT40, DPS368, เรดาร์) และการ์ดบนหน้า Home (Dev Kit ไม่มี Controls, TESAIoT Connectivity และ Audio Player) สไลด์บอกไว้ทุกจุดที่สองบอร์ดต่างกัน

## โครงหลักสูตร

ห้าโมดูล 36 บทเรียน ราว 36 ชั่วโมงตามหลักสูตรต้นฉบับ (สิบสองชุด ชุดละสามชั่วโมง) ผลรวมเวลาโดยประมาณของทุกบทเรียนคือราว 38 ชั่วโมง แต่ละบทเรียนราว 45–75 นาที บทเรียนมาเป็นชุด ชุดละสามบทเรียน: **แนวคิด → แกะโค้ด → ลงมือทำ**

| โมดูล | บทเรียน | ชั่วโมง (ประมาณ) | เรื่อง |
|---|---|---|---|
| [โมดูล 1 — แอปพลิเคชันบนจอที่มีอยู่แล้ว](m01-ui-application/README.md) | 6 | 6.8 | รู้จักบอร์ดจากแอปที่มากับเครื่อง ส่งข้อความแรกขึ้นจอด้วย lcd และ ui แล้วพาค่าจากบอร์ดออกไปบนเครือข่ายและรับคำสั่งกลับมา |
| [โมดูล 2 — จากจอสู่ฮาร์ดแวร์](m02-ui-to-hardware/README.md) | 9 | 9.4 | สั่ง LED และอ่านปุ่มด้วย gpio สร้างแผงควบคุมบนจอสัมผัสที่คุมไฟจริง แล้วอ่านลูกบิดและ CapSense พร้อมกรองสัญญาณ |
| [โมดูล 3 — แสดงผลเซนเซอร์บน HMI](m03-sensor-hmi/README.md) | 9 | 8.9 | แปลงความเร่งเป็นมุมเอียง สุ่มสัญญาณให้ถูกแล้ววาดกราฟ real-time และประกอบ Mini-HMI Dashboard สี่การ์ดที่รันต่อเนื่องได้ |
| [โมดูล 4 — เชื่อมต่อแพลตฟอร์ม IoT](m04-iot-connectivity/README.md) | 9 | 9.4 | ต่อ WiFi อ่านค่าเครือข่ายให้เป็น ส่ง telemetry และรับ command ผ่าน MQTT ขึ้นแพลตฟอร์มที่ติดตั้งเอง แล้วย้ายขึ้น MQTTs ผ่าน TLS |
| [โมดูล 5 — Capstone: AIoT Mini-Product](m05-capstone/README.md) | 3 | 3.3 | เริ่มจากโจทย์จริง ออกแบบด้วย canvas และ schema แล้วประกอบ Sense → Decide → Show → Send เป็น mini-product ที่อยู่รอดเมื่อเน็ตหลุด และนำเสนอ 10 นาที |

<details><summary>รายชื่อบทเรียนทั้งหมด</summary>

**โมดูล 1 — แอปพลิเคชันบนจอที่มีอยู่แล้ว**

- [บทเรียน 1.1 — ทัวร์บอร์ด: เล่นของจริงก่อน](m01-ui-application/l01-board-tour/README.md)
- [บทเรียน 1.2 — ข้อความแรกขึ้นจอ: โมดูล lcd กับ ui](m01-ui-application/l02-first-lines-on-screen/README.md)
- [บทเรียน 1.3 — เปิดกล่อง: สองคอร์ งาน AIoT และป้ายของทีม](m01-ui-application/l03-inside-the-box/README.md)
- [บทเรียน 1.4 — บอร์ดออกจากโต๊ะ: ต่อ WiFi ครั้งแรก](m01-ui-application/l04-wifi-first-connect/README.md)
- [บทเรียน 1.5 — ค่าออกไป คำสั่งกลับมา: MQTT บน broker สาธารณะ](m01-ui-application/l05-values-out-commands-back/README.md)
- [บทเรียน 1.6 — ลงมือทำ: พาค่าจริงออกจากบอร์ด และสรุปโมดูล 1](m01-ui-application/l06-link-lab/README.md)

**โมดูล 2 — จากจอสู่ฮาร์ดแวร์**

- [บทเรียน 2.1 — โมดูล gpio: LED ปุ่ม และบอร์ดที่บอกได้ว่ามีอะไร](m02-ui-to-hardware/l01-gpio-leds-buttons/README.md)
- [บทเรียน 2.2 — หลังไฟและปุ่ม: active-low กันเด้ง และลูปที่ไม่หยุด](m02-ui-to-hardware/l02-active-low-debounce/README.md)
- [บทเรียน 2.3 — ลงมือทำ: ไฟวิ่งกับปุ่ม แล้วส่งขึ้น broker](m02-ui-to-hardware/l03-led-button-lab/README.md)
- [บทเรียน 2.4 — จอสัมผัสและ widget ตัวแรก](m02-ui-to-hardware/l04-touch-widgets/README.md)
- [บทเรียน 2.5 — event loop: แตะจอแล้วไฟจริงติด](m02-ui-to-hardware/l05-event-loop/README.md)
- [บทเรียน 2.6 — ลงมือทำ: แผงควบคุมสัมผัสของเรา และ widget ขั้นต่อไป](m02-ui-to-hardware/l06-touch-panel-lab/README.md)
- [บทเรียน 2.7 — อนาล็อกและสัมผัส: ADC ลูกบิด และ CapSense](m02-ui-to-hardware/l07-adc-capsense/README.md)
- [บทเรียน 2.8 — กรองสัญญาณ: EMA กับ Median แล้วแกะโค้ดเกจ](m02-ui-to-hardware/l08-filters/README.md)
- [บทเรียน 2.9 — ลงมือทำ: เกจลูกบิดกับแถบสัมผัส](m02-ui-to-hardware/l09-pot-capsense-lab/README.md)

**โมดูล 3 — แสดงผลเซนเซอร์บน HMI**

- [บทเรียน 3.1 — accelerometer กับมุมเอียง: roll และ pitch](m03-sensor-hmi/l01-accelerometer-tilt/README.md)
- [บทเรียน 3.2 — gyro ฟิลเตอร์ complementary และโค้ดเครื่องวัดระดับ](m03-sensor-hmi/l02-gyro-fusion/README.md)
- [บทเรียน 3.3 — ลงมือทำ: เครื่องวัดระดับดิจิทัล](m03-sensor-hmi/l03-digital-level-lab/README.md)
- [บทเรียน 3.4 — สุ่มสัญญาณให้ถูก: Nyquist aliasing และ ring buffer](m03-sensor-hmi/l04-sampling/README.md)
- [บทเรียน 3.5 — ui.Chart: กราฟหลาย series และคาบเวลาของลูปจริง](m03-sensor-hmi/l05-realtime-chart/README.md)
- [บทเรียน 3.6 — ลงมือทำ: กราฟความเร่งสามแกน](m03-sensor-hmi/l06-accel-chart-lab/README.md)
- [บทเรียน 3.7 — ออกแบบ HMI: การ์ด ลำดับสายตา สี และงบ widget](m03-sensor-hmi/l07-hmi-design/README.md)
- [บทเรียน 3.8 — ประกอบแดชบอร์ด: สี่การ์ดในลูปเดียว](m03-sensor-hmi/l08-dashboard-build/README.md)
- [บทเรียน 3.9 — ลงมือทำ: Mini-HMI Dashboard และการทดสอบ 10 นาที](m03-sensor-hmi/l09-dashboard-lab/README.md)

**โมดูล 4 — เชื่อมต่อแพลตฟอร์ม IoT**

- [บทเรียน 4.1 — WiFi และเครือข่าย: dBm DHCP IP และ DNS](m04-iot-connectivity/l01-wifi-networking/README.md)
- [บทเรียน 4.2 — จอสถานะเครือข่าย: แกะโค้ดโมดูล wifi](m04-iot-connectivity/l02-network-status-code/README.md)
- [บทเรียน 4.3 — ลงมือทำ: หน้าสถานะเครือข่ายของทีม](m04-iot-connectivity/l03-network-status-lab/README.md)
- [บทเรียน 4.4 — MQTT: pub/sub topic QoS และงบข้อมูล](m04-iot-connectivity/l04-mqtt-concepts/README.md)
- [บทเรียน 4.5 — MQTT กับแพลตฟอร์มที่ติดตั้งเอง: telemetry และ command](m04-iot-connectivity/l05-mqtt-platform/README.md)
- [บทเรียน 4.6 — ลงมือทำ: telemetry สองทาง](m04-iot-connectivity/l06-mqtt-telemetry-lab/README.md)
- [บทเรียน 4.7 — TLS: ใบรับรอง ห่วงโซ่ความเชื่อถือ และการจับมือ](m04-iot-connectivity/l07-tls-concepts/README.md)
- [บทเรียน 4.8 — โมดูล tesaiot: MQTTs สู่แพลตฟอร์ม](m04-iot-connectivity/l08-tesaiot-module/README.md)
- [บทเรียน 4.9 — ลงมือทำ: ส่งค่าจริงผ่านช่องทางเข้ารหัส](m04-iot-connectivity/l09-secure-telemetry-lab/README.md)

**โมดูล 5 — Capstone: AIoT Mini-Product**

- [บทเรียน 5.1 — จากโจทย์จริงสู่แบบ: canvas schema และการออกแบบตอนพัง](m05-capstone/l01-problem-to-design/README.md)
- [บทเรียน 5.2 — โครงตั้งต้น: Sense Decide Show Send](m05-capstone/l02-capstone-starter/README.md)
- [บทเรียน 5.3 — สร้างและนำเสนอ AIoT mini-product](m05-capstone/l03-build-and-present/README.md)

</details>

## ในแต่ละบทเรียนมีอะไร

| ไฟล์ | คืออะไร |
|---|---|
| `README.md` | เป้าหมาย สิ่งที่ต้องเตรียม แนวคิดโดยย่อ รายชื่อไฟล์โค้ด และเช็กความเข้าใจ |
| `slides.md` | สไลด์ของบทเรียน (Marp) พร้อมโน้ตผู้สอน |
| `examples/` | ตัวอย่างที่รันได้ทันที หัวไฟล์บอกว่า **ไฟล์นี้สอน** อะไร **ดูที่จอ** ตรงไหน และ **กับดัก** อยู่ตรงไหน |
| `practice/` | ไฟล์ฝึก มีช่องว่าง `# เติม:` ให้เติมเอง (บทเรียนลงมือทำ) |
| `solution/` | เฉลย ชื่อไฟล์ตรงกับไฟล์ฝึก |
| `quiz.yaml` | คำถามเช็กความเข้าใจ ผูกกับเป้าหมายแต่ละข้อ |

วิธีรันโค้ด: เปิดไฟล์ใน BENTO IDE → บนจอบอร์ดแตะการ์ด **BENTO Playground** ค้างไว้ → กด **Program to Device** แล้วอ่านผลบนจอบอร์ด (หรือกด Run บน BENTO Emulator) · ไฟล์โค้ดขึ้นต้นด้วยเลขชุดเดิม เช่น `s03_led_button.py` และข้อความบนจอบางไฟล์ยังขึ้นว่า "ชุด 9" ซึ่งหมายถึงชุดตัวอย่าง s09

โค้ดที่ใช้ร่วมกันหลายบทเรียนอยู่ใน [`shared/`](shared/): [`shared/lvgl_ports/`](shared/lvgl_ports/README.md) ตัวอย่าง LVGL ที่ถอดเป็น MicroPython · [`shared/widgets/`](shared/widgets/README.md) widget ทีละตัว · [`shared/usecase/`](shared/usecase/README.md) ตัวอย่างประยุกต์ · [`shared/web/`](shared/web/README.md) หน้าเว็บอ่านค่าและส่งคำสั่งผ่าน MQTT

## วิธีใช้เฉลย

เฉลยเปิดให้ดูได้โดยตั้งใจ แต่มีไว้ให้ **เทียบหลังจากพยายามเองแล้ว** ไม่ได้มีไว้คัดลอกวาง

1. **ลองเองก่อนอย่างน้อย 15 นาที** อ่านคำใบ้ `# เติม:` ในไฟล์ฝึก เติมแล้วส่งขึ้นบอร์ดดูผลจริง ถ้า error ให้อ่านข้อความ error ให้จบก่อน มันมักบอกบรรทัดที่ผิดตรง ๆ
2. **เปิดเฉลยอ่าน แล้วปิด** อ่านให้เข้าใจว่าทำไมเขียนแบบนั้น แล้วปิดไฟล์เฉลยก่อนกลับไปแก้ไฟล์ของตัวเอง
3. **พิมพ์เอง ไม่วาง** นิ้วที่พิมพ์เองกับตาที่คัดลอกจำคนละแบบกัน
4. **รันแล้วลองแก้ตัวเลข** เปลี่ยนค่าหน่วงเวลา สี หรือช่วงของกราฟ แล้วดูว่าอะไรเปลี่ยนบนจอ การรู้ว่า "ถ้าแก้ตรงนี้จะเกิดอะไร" คือความเข้าใจจริง

## สัญญาอนุญาต

- **เนื้อหา** (สไลด์ README ภาพที่วาดเองและภาพหน้าจอ) — CC BY 4.0
- **โค้ด** (`examples/`, `practice/`, `solution/`, `shared/`) — MIT, Copyright (c) 2026 Wiroon Sriborrirux, Advance Innovation Centre (AIC), Burapha University (ข้อความสัญญาอนุญาตเต็มอยู่ที่ `LICENSES/MIT.txt` ของรีโพ)
- **ภาพจากบุคคลที่สาม** — ใช้ตามสัญญาอนุญาตของแต่ละภาพ รายชื่อผู้สร้าง แหล่งที่มา และสัญญาอนุญาตอยู่ใน [credits.yaml](credits.yaml) · รูปจากคู่มือบอร์ดของ Infineon ใช้เพื่อการเรียนการสอน สิทธิ์เป็นของ Infineon Technologies AG

## ที่มา

หลักสูตรนี้ดัดแปลงจาก **AIoT in Action — Embedded Systems for AIoT Developer** ของ รศ.วิรุฬห์ ศรีบริรักษ์ Advance Innovation Centre (AIC) มหาวิทยาลัยบูรพา ([รีโพ](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer) @ `a80bbe88` · [เว็บสไลด์](https://advance-innovation-centre-aic.github.io/embedded-systems-for-aiot-developer/)) โดยแบ่งสไลด์สิบสองชุดเป็นบทเรียน จัดเป็นห้าโมดูล และปรับถ้อยคำให้เหมาะกับผู้เรียนทั่วไป · BENTO & TESAIoT

## อ้างอิง TESA

เมื่อนำหลักสูตรนี้หรือบางส่วนไปใช้ ดัดแปลง หรือเผยแพร่ต่อ กรุณาอ้างอิงตามนี้ (ถ้าดัดแปลง ให้เติม «(ดัดแปลง)» ต่อท้ายชื่อ และคงเครดิตต้นฉบับของ AIC ไว้ด้วย):

> "AIoT in Action: จากหน้าจอสัมผัสสู่แพลตฟอร์ม IoT (MicroPython)" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0 · ดัดแปลงจาก AIoT in Action — Embedded Systems for AIoT Developer, © 2026 รศ.วิรุฬห์ ศรีบริรักษ์, Advance Innovation Centre (AIC) มหาวิทยาลัยบูรพา · BENTO & TESAIoT (CC BY 4.0 / MIT)

การอ้างอิงไม่ได้แปลว่า TESA หรือ Infineon รับรองหลักสูตรหรือผลงานที่นำไปใช้ต่อ ชื่อ TESA, TQP และ "Certified by TESA and Infineon" เป็นเครื่องหมายของโครงการ
