# TESA Open Knowledge

คลังความรู้เปิดด้านระบบสมองกลฝังตัว AIoT และ Edge AI ของ **สมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA)**
เรียนฟรีทีละบทเรียน มีสไลด์ ตัวอย่างโค้ดที่รันได้จริง แบบฝึก และเฉลย สำหรับนักพัฒนา บุคคลทั่วไป ผู้ประกอบการ ผู้สอน และนักศึกษา

**เว็บไซต์:** https://tesaiot.github.io/tesa-qualification-program/ · *English: [README.en.md](README.en.md)*

> **นำไปใช้ได้ทุกคน แต่ต้องให้เครดิต TESA ทุกครั้ง**
> อ่านข้อความเครดิตที่ต้องใช้และตัวอย่างสำหรับสไลด์ รายละเอียดรายวิชา เอกสารพิมพ์ และ repository โค้ด ที่ [ATTRIBUTION.md](ATTRIBUTION.md)

## TESA Open Knowledge คืออะไร

เราอยากให้ใครก็ตามที่สนใจระบบสมองกลฝังตัวได้เรียนจากของจริง ตั้งแต่ไฟดวงแรกบนบอร์ด ไปจนถึงอุปกรณ์ที่ส่งข้อมูลขึ้นแพลตฟอร์ม IoT
อย่างปลอดภัยและรันโมเดล AI บนตัวเอง เนื้อหาทุกบทเขียนเป็นภาษาไทยคู่ศัพท์อังกฤษ เปิดให้นำไปสอน ดัดแปลง และต่อยอดได้

บทเรียนทุกบทประกาศว่าพัฒนาทักษะใดถึงระดับใด โดยอ้าง [แผนที่ทักษะ](skills/README.md) ชุดเดียวกัน ข้อมูลนี้เป็นฐานของ
Skillset Mapping ใน **TESA Qualification Program (TQP) ซึ่งเป็นโครงการร่วมระหว่าง TESA และ Infineon**

การออกแบบ TQP ยังเป็นฉบับ v0.1 และ **ยังไม่เปิดรับผู้สมัครสอบ** วันนี้ยังไม่มีใบรับรองใดที่ขอรับได้
อ่านระดับ L1–L5 ที่ [tqp/levels.md](tqp/levels.md) และการออกแบบใบรับรองที่ [tqp/certification.md](tqp/certification.md)

## เส้นทางการเรียนรู้

| เส้นทาง | สำหรับใคร |
|---|---|
| **Explorer (บุคคลทั่วไป)** | ไม่เคยเขียนโปรแกรมก็เริ่มได้ เขียน MicroPython บรรทัดแรกใน BENTO Emulator ไม่ต้องมีบอร์ด |
| **ผู้ประกอบการ** | เข้าใจว่า Edge AI และ IoT ทำอะไรได้ ประเมินต้นทุนและความเสี่ยง แล้วเขียนโจทย์ให้นักพัฒนา ไม่ต้องเขียนโค้ด |
| **นักพัฒนา** | เริ่มจากระดับที่ตรงกับพื้นฐานของตัวเอง แล้วไปต่อที่เฟิร์มแวร์ภาษา C, Secure IoT และ Edge AI บนบอร์ดจริง |
| **นักศึกษา** | จาก AIoT in Action สู่เฟิร์มแวร์ภาษา C และ capstone ที่เก็บเป็น portfolio บน GitHub |
| **ผู้สอน** | ชุดสอน Educator Kit สำหรับนำหลักสูตรไปใช้ในรายวิชาของตัวเอง |

รายละเอียดของแต่ละเส้นทาง (ลำดับหลักสูตร ชั่วโมงเรียน และปลายทาง) อยู่ใน [catalog/tracks.yaml](catalog/tracks.yaml)

## หลักสูตร

| หลักสูตร | ระดับ | สถานะ |
|---|---|---|
| [Explorer: เปิดโลกระบบสมองกลฝังตัว](courses/explorer/README.md) | L1 รู้จัก | ฉบับร่าง (alpha) |
| [AIoT in Action: จากหน้าจอสัมผัสสู่แพลตฟอร์ม IoT (MicroPython)](courses/aiot-micropython/README.md) | L2 ทำตามแนวทาง | ฉบับร่าง (alpha) |
| [**TESAIoT Firmware Stack: เฟิร์มแวร์ภาษา C บน TESAIoT Dev Kit**](courses/tesaiot-firmware-stack/README.md) · หลักสูตรหลัก | L3 ทำได้เอง | ฉบับร่าง (alpha) |
| [Edge AI และ IoT สำหรับการตัดสินใจเชิงผลิตภัณฑ์](courses/edge-ai-iot-for-business/README.md) | L1 รู้จัก | ฉบับร่าง (alpha) |
| [การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)](courses/product-design/README.md) | L2 ทำตามแนวทาง | ฉบับร่าง (alpha) |
| [อิเล็กทรอนิกส์และเครื่องมือวัดสำหรับนักพัฒนาระบบฝังตัว](courses/electronics-and-instruments/README.md) | L2 ทำตามแนวทาง | ร่างโครง (pre-alpha) |
| [พื้นฐานเฟิร์มแวร์ภาษา C บน PSoC Edge](courses/embedded-c-foundations/README.md) | L3 ทำได้เอง | ร่างโครง (pre-alpha) |
| [TESA Firmware SDK สำหรับ Edge AI](courses/firmware-sdk-edge-ai/README.md) | L3 ทำได้เอง | ฉบับร่าง (alpha) |
| [พัฒนาเฟิร์มแวร์ร่วมกับ TESA Digital Twin บน VS Code](courses/digital-twin/README.md) | L3 ทำได้เอง | ฉบับร่าง (alpha) |
| [Secure IoT กับ OPTIGA™ Trust M](courses/secure-iot-optiga/README.md) | L3 ทำได้เอง | ร่างโครง (pre-alpha) |
| [Edge AI Developer: จากเซนเซอร์สู่โมเดลบนอุปกรณ์](courses/edge-ai-developer/README.md) | L3 ทำได้เอง | ร่างโครง (pre-alpha) |
| [ชุดสำหรับผู้สอน (Educator Kit)](courses/educator-kit/README.md) | L3 ทำได้เอง | ฉบับร่าง (alpha) |
| [Fundamental of Embedded Systems Developer I–II (เกมคอนโซล)](https://advance-innovation-centre-aic.github.io/embedded-systems-for-game_console_developer/) · หลักสูตรภายนอก | L2 ทำตามแนวทาง | พร้อมใช้ (stable) |

ความหมายของสถานะ: ร่างโครง (pre-alpha) มีโครงแต่เนื้อหายังไม่ครบ · ฉบับร่าง (alpha) เนื้อหาครบและผู้เขียนทดสอบแล้ว ·
ทดลองสอน (beta) ผ่านการตรวจสองชั้นและมีผู้อื่นนำไปสอนนำร่องแล้ว · พร้อมใช้ (stable) ใช้สอนได้เต็มที่ รายละเอียดใน [GOVERNANCE.md](GOVERNANCE.md)
หลักสูตรภายนอกดูแลโดยเจ้าของเอง และลงทะเบียนไว้ใน [catalog/courses.yaml](catalog/courses.yaml) โดยอ้างอิง commit ที่แน่นอน

## เรียนอย่างไร

**แกนของคลังนี้คือเฟิร์มแวร์ภาษา C บน TESAIoT Dev Kit** (PSoC Edge AI Kit SoM บนบอร์ดฐาน QWA309)
เครื่องมือหลักมีสามอย่าง

| ใช้อะไร | ทำอะไร |
|---|---|
| [ModusToolbox](https://www.infineon.com/cms/en/design-support/tools/sdk/modustoolbox-software/) + [master template ของ TESA](courses/tesaiot-firmware-stack/m01-getting-started/l01-toolchain-and-master-template/README.md) | build และ flash เฟิร์มแวร์ภาษา C ลงบอร์ด |
| [TESAIoT Developer Hub](https://dev.tesaiot.dev/) ([github.com/tesaiot/developer-hub](https://github.com/tesaiot/developer-hub)) | ตัวอย่างโค้ดจริงทีละตอน พร้อมคำอธิบาย Why / What / How และเฟิร์มแวร์สำเร็จรูปสำหรับ flash |
| [TESAIoT Dev Kit SDK](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) | SDK และเอกสารอ้างอิงของบอร์ด (Edge AI, security, BLE, IPC) |

เริ่มที่หลักสูตร [TESAIoT Firmware Stack](courses/tesaiot-firmware-stack/README.md) บทเรียนหนึ่งใช้เวลา 30–75 นาที และเดินตามลำดับนี้

1. **เป้าหมายและดูของจริงก่อน** รู้ว่าจบบทแล้วจะทำอะไรได้ แล้ว flash ตัวอย่างที่เสร็จแล้วลงบอร์ดเพื่อเห็นปลายทาง
2. **อ่านและไล่โค้ด** อ่าน Why / What / How ของตัวอย่าง แล้วไล่ไฟล์ตามลำดับที่บทเรียนแนะนำ
3. **build เองและลองแก้** วางไฟล์ลงใน master template ทายผลก่อนแก้ แล้วเทียบกับที่เห็นบนบอร์ด
4. **เช็กความเข้าใจและเก็บผลงาน** ตอบคำถามท้ายบท ต่อยอดหนึ่งอย่าง และเก็บภาพหรือวิดีโอไว้ใน portfolio

**ยังไม่เคยเขียนโปรแกรมบนบอร์ด หรือยังไม่มีบอร์ด** เริ่มที่ [Explorer](courses/explorer/README.md) หรือ
[AIoT in Action](courses/aiot-micropython/README.md) ซึ่งใช้ MicroPython ใน [BENTO IDE](https://ide.tesaiot.dev/)
และมี BENTO Emulator ให้ลองในเบราว์เซอร์โดยไม่ต้องมีบอร์ด แล้วค่อยต่อด้วยภาษา C

## ร่วมพัฒนา

แจ้งเนื้อหาผิด แปลบทเรียน หรือเขียนบทเรียนใหม่ได้ทุกคน เริ่มที่ [CONTRIBUTING.md](CONTRIBUTING.md) (ภาษาอังกฤษ: [CONTRIBUTING.en.md](CONTRIBUTING.en.md))
ผู้เขียนใช้ [แม่แบบ](templates/) และ [คู่มือผู้เขียน](templates/AUTHORING.md) ทุก commit ต้องมี DCO sign-off และทุก PR ต้องผ่าน
`python3 tools/validate.py` ชุมชนนี้ใช้ [จรรยาบรรณของชุมชน](CODE_OF_CONDUCT.md) ส่วนการตัดสินใจและการตรวจสองชั้นอธิบายไว้ใน [GOVERNANCE.md](GOVERNANCE.md)
พบช่องโหว่หรือข้อมูลลับหลุด ให้แจ้งแบบส่วนตัวตาม [SECURITY.md](SECURITY.md)

## สัญญาอนุญาต

| ส่วน | สัญญาอนุญาต |
|---|---|
| เนื้อหาบทเรียน สไลด์ และภาพที่ TESA ทำเอง | [CC BY 4.0](LICENSES/CC-BY-4.0.txt) |
| โค้ดใหม่ | [Apache-2.0](LICENSE) |
| โค้ดที่นำเข้าจากหลักสูตร AIoT in Action ของ AIC | [MIT](LICENSES/MIT.txt) |
| แผนที่ทักษะใน `skills/` | [CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt) |
| ภาพจากบุคคลที่สาม | ตามต้นทางของแต่ละภาพ ดู `credits.yaml` ของแต่ละหลักสูตร |

ชื่อและโลโก้ของ TESA, TQP, TESAIoT, BENTO และเครื่องหมายการค้าของ Infineon ไม่อยู่ใต้สัญญาอนุญาตเหล่านี้ ดู [TRADEMARKS.md](TRADEMARKS.md)

## ที่มาและเครดิต

- จัดทำและเผยแพร่โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA)
- หลักสูตร AIoT in Action ดัดแปลงจาก AIoT in Action — Embedded Systems for AIoT Developer, © 2026 รศ.วิรุฬห์ ศรีบริรักษ์,
  Advance Innovation Centre (AIC) มหาวิทยาลัยบูรพา · BENTO & TESAIoT (CC BY 4.0 / MIT)
- หลักสูตร TESA Firmware SDK, Digital Twin และการออกแบบผลิตภัณฑ์: เนื้อหาต้นฉบับโดย drsanti (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคม TESA
- แผนที่ทักษะดัดแปลงจาก Embedded Systems Engineering Roadmap โดย Meysam Parvizi (CC BY-SA 4.0)
- Infineon®, PSOC™, ModusToolbox™ และ OPTIGA™ เป็นเครื่องหมายการค้าของ Infineon Technologies AG ตัวอย่างโค้ดของ Infineon อ้างอิงด้วยลิงก์

รายละเอียดครบอยู่ใน [NOTICE.md](NOTICE.md) · อ้างอิงในงานวิชาการด้วย [CITATION.cff](CITATION.cff) · ประวัติรุ่นอยู่ใน [CHANGELOG.md](CHANGELOG.md)

## อ้างอิง TESA

> "TESA Open Knowledge" โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA)
> https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0

เมื่อใช้เพียงบางบทเรียนหรือบางหลักสูตร ให้ใช้ชื่อบทเรียนหรือหลักสูตรนั้นตามแบบใน [ATTRIBUTION.md](ATTRIBUTION.md)
