# พัฒนาเฟิร์มแวร์ร่วมกับ TESA Digital Twin บน VS Code

หลักสูตรเชิงปฏิบัติการพัฒนา ตรวจสอบ และทดสอบเฟิร์มแวร์ Edge AI ร่วมกับ Digital Twin บน VS Code (Bitstream Studio): จำลองอุปกรณ์ เซ็นเซอร์ พฤติกรรม ท่อข้อมูล และการเชื่อมต่อคลาวด์ เพื่อลดการพึ่งฮาร์ดแวร์จริงในช่วงพัฒนา

> เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA) · นำเข้าจาก [drsanti/TESAIoT-Courses — C2](https://github.com/drsanti/TESAIoT-Courses/tree/287c21814ba8c75f693136616dcd270349a15966/C2) (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

| | |
|---|---|
| ระดับ | L3 · ทำได้เอง |
| สถานะ | alpha (เนื้อหานำเข้าแล้ว กำลังทบทวน) |
| เวลาโดยประมาณ | ~18 ชั่วโมง (รวมเวลาของโมดูลตามต้นฉบับ) |
| ฮาร์ดแวร์ | ทำได้ด้วยโหมด Simulator ของ Bitstream Studio (ถ้ามี extension) หรือบอร์ด TESAIoT PSoC Edge DevKit |
| เหมาะกับ | นักพัฒนา · นักศึกษา · ผู้สอน |
| ภาษา | ไทย คำศัพท์เทคนิคเป็นภาษาอังกฤษ หัวข้อในบทเรียนเป็นภาษาอังกฤษตามต้นฉบับ · ฉบับภาษาอังกฤษของบทเรียนยังรอแปล |

## หลักสูตรนี้สำหรับใคร

นักพัฒนาเฟิร์มแวร์ที่ผ่านหลักสูตร 1 หรือมีพื้นฐาน C / MCU / MQTT เทียบเท่า และอยากทดสอบเฟิร์มแวร์กับอุปกรณ์จำลองก่อนหรือระหว่างใช้บอร์ดจริง

## ก่อนเรียน

- ผ่าน[หลักสูตร 1](../firmware-sdk-edge-ai/README.md) หรือมีพื้นฐาน C / MCU / MQTT เทียบเท่า (ต้นฉบับแนะนำ ไม่บังคับ)

## สิ่งที่ต้องมี

- **Visual Studio Code** 1.75 ขึ้นไป (Bitstream Studio ประกาศ engine `^1.75.0`; README ของแพ็กแล็บแนะนำ 1.85+) หรือ Cursor
- **Bitstream Studio** ([VS Marketplace](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) เวอร์ชัน 0.2.2 เมื่อ 26 ก.ย. 2026) หรือไฟล์ VSIX จาก `vsix/` ของ TESAIoT_Hackathon ที่คู่กับ HEX
- **Bitstream Simulator** สำหรับโหมดไม่มีบอร์ด: ต้นฉบับและ README ของแพ็กแล็บเรียกว่าเป็น extension แยก แต่เมื่อ 26 ก.ย. 2026 ยังไม่พบใน VS Marketplace และไม่พบใน `vsix/` ของ TESAIoT_Hackathon ถ้าหาไม่ได้ ให้ใช้เส้นทาง Bitstream (บอร์ดจริง) ในแล็บที่เปิดให้เลือก
- **บอร์ด** TESAIoT PSoC Edge DevKit + HEX `tesaiot-bitstream-<version>.hex` จาก [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon/tree/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/hex) สำหรับเส้นทาง Bitstream (UART 921600 baud)
- **web-app ตัวอย่าง** `ex01`–`ex17` ในโฟลเดอร์ [`web-app/`](https://github.com/drsanti/TESAIoT_Hackathon/tree/f5f09a6e89a42a800dd39bae362c1c3f2328cc72/web-app) ของ TESAIoT_Hackathon
- **Blender 4.5** (ลิงก์คู่มือในบทเรียนตรึงไว้ที่ 4.5) สำหรับส่วน Twin 3D ในโมดูล 3
- ไฟล์ `.vsix` และตัวติดตั้งใน TESAIoT_Hackathon เก็บด้วย Git LFS ถ้า `git clone` ให้ติดตั้ง `git-lfs` ก่อน หรือดาวน์โหลดทีละไฟล์จากหน้าเว็บ GitHub

รุ่นและเวอร์ชันทั้งหมดบันทึกไว้ในช่อง `toolchain` ของ [course.yaml](course.yaml)

## ผลลัพธ์การเรียนรู้

เมื่อจบหลักสูตร คุณจะ:

1. อธิบายสถาปัตยกรรม Digital Twin และตัดสินใจได้ว่าเมื่อไรใช้ Twin/Simulator และเมื่อไรต้องยืนยันบนบอร์ดจริง
2. ติดตั้งและใช้ Bitstream Studio บน VS Code เปิดเซสชัน Simulator หรือ Bitstream (UART) ได้ซ้ำ
3. สร้าง Virtual Device ที่มีเซ็นเซอร์ behavior และ event script ที่รันซ้ำได้
4. พิสูจน์ I/O ระหว่างเฟิร์มแวร์กับ Twin วัด latency และแยกปัญหาทีละชั้น
5. ออกแบบท่อ telemetry และ MQTT pub/sub แล้วทดลอง fault injection ภายใต้เงื่อนไขที่ควบคุมได้
6. ทดสอบระบบแบบ end-to-end ด้วยตารางเทสอย่างน้อย 3 เคส และส่งมอบ README ที่รันซ้ำได้

## โมดูล

| # | โมดูล | บทเรียน | แล็บ | เวลาตามต้นฉบับ |
|---|---|---|---|---|
| 1 | [สถาปัตยกรรม Digital Twin](m01-twin-architecture/README.md) | [Virtual Device, Digital Twin และโลกของเฟิร์มแวร์จริง](m01-twin-architecture/l01-twin-architecture/README.md) | [แล็บ](m01-twin-architecture/l02-lab/README.md) | ประมาณ 2 ชั่วโมง (บทเรียน) + แล็บ 30–45 นาที |
| 2 | [VS Code สำหรับพัฒนาร่วมกับ Twin](m02-vscode-twin/README.md) | [ตั้งโฮสต์ Twin ใน VS Code ด้วย Bitstream Studio](m02-vscode-twin/l01-vscode-for-twin/README.md) | [แล็บ](m02-vscode-twin/l02-lab/README.md) | ประมาณ 3 ชั่วโมง (บทเรียน) + แล็บ 2–3 ชั่วโมง (รวมติดตั้ง) |
| 3 | [การสร้างแบบจำลองอุปกรณ์เสมือน (+ Blender สำหรับ Twin 3D)](m03-virtual-device/README.md) | [Virtual Device, behavior, event script และโมเดล 3D สำหรับ Twin](m03-virtual-device/l01-virtual-device-modeling/README.md) | [แล็บ](m03-virtual-device/l02-lab/README.md) | ประมาณ 4–5 ชั่วโมง (บทเรียน) + แล็บ 3–3.5 ชั่วโมง (+ 1–1.5 ชั่วโมงถ้าทำ Lab E Blender) |
| 4 | [Co-simulation ระหว่างเฟิร์มแวร์กับ Twin](m04-cosimulation/README.md) | [Co-simulation: พิสูจน์ I/O วัด latency และแยกปัญหา](m04-cosimulation/l01-firmware-twin-cosim/README.md) | [แล็บ](m04-cosimulation/l02-lab/README.md) | ประมาณ 3 ชั่วโมง (บทเรียน) + แล็บ 2.5–3 ชั่วโมง |
| 5 | [Telemetry และการจำลองคลาวด์](m05-telemetry-cloud/README.md) | [ท่อ telemetry, MQTT บน Twin และ fault injection](m05-telemetry-cloud/l01-telemetry-cloud-simulation/README.md) | [แล็บ](m05-telemetry-cloud/l02-lab/README.md) | ประมาณ 4 ชั่วโมง (บทเรียน) + แล็บ 3.5–4 ชั่วโมง |
| 6 | [การรวมระบบและการทดสอบ](m06-integration/README.md) | [ทดสอบ end-to-end บน Digital Twin](m06-integration/l01-system-integration-testing/README.md) | [แล็บ](m06-integration/l02-lab/README.md) | ประมาณ 2 ชั่วโมง (บทเรียน) + แล็บ ~2 ชั่วโมง + เวลาเพิ่มสำหรับ README และหลักฐาน |

## วิธีเรียน

1. อ่านบทเรียนแล้วทำแล็บของแต่ละโมดูลตามลำดับ 1 → 6
2. ใช้ worksheet และ checklist ใน `resources/` ตอนตั้ง Twin และเก็บหลักฐาน
3. โฮสต์หลักคือ Bitstream Studio ติดตั้งจาก Marketplace หรือแพ็กแล็บ
4. หลักสูตรนี้โฟกัส Firmware ↔ Twin ↔ Cloud ไม่ทบทวน GPIO / RTOS ทั้งหมดซ้ำ แต่จะลิงก์กลับไปหลักสูตร 1 เมื่อจำเป็น

ต้นฉบับเขียนขึ้นเพื่อการอบรมแบบมีผู้สอน ถ้อยคำในบทเรียนปรับให้เรียนด้วยตัวเองได้แล้ว แต่ค่าที่ขึ้นกับเครื่องของคุณ (Wi-Fi, broker, พอร์ต COM, เวอร์ชัน HEX) ยังต้องตั้งเอง ให้เริ่มจากค่าที่บทเรียนให้ไว้ (เช่น baud 921600 หรือ broker ใน Bitstream Studio) แล้วดูเอกสารของเครื่องมือประกอบ ในเนื้อหาจะเห็นคำว่า **Course 1 / Course 2 / Course 3** และรหัส **M01–M08** ตามต้นฉบับ: Course 1 คือหลักสูตร TESA Firmware SDK สำหรับ Edge AI, Course 2 คือหลักสูตร Digital Twin และ Course 3 คือหลักสูตรการออกแบบผลิตภัณฑ์ ส่วน M0N คือโมดูลที่ N

## ลำดับที่แนะนำระหว่างสามหลักสูตร

ต้นฉบับแนะนำให้เรียนตามลำดับนี้:

```text
หลักสูตร 1  TESA Firmware SDK สำหรับ Edge AI        เฟิร์มแวร์บนบอร์ด
    │
    ▼
หลักสูตร 2  พัฒนาเฟิร์มแวร์ร่วมกับ Digital Twin        เฟิร์มแวร์ ↔ Digital Twin ↔ คลาวด์
    │
    ▼
หลักสูตร 3  การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม        ออกแบบผลิตภัณฑ์ → Twin → ต้นแบบจริง
```

ถ้าต้องการแค่งานออกแบบใน Blender เริ่มโมดูล 1–3 ของหลักสูตร 3 ก่อนได้ ส่วนแล็บที่ใช้ Twin จะง่ายขึ้นมากหลังเรียนหลักสูตร 2

- หลักสูตร 1: [TESA Firmware SDK สำหรับ Edge AI](../firmware-sdk-edge-ai/README.md)
- หลักสูตร 2: [พัฒนาเฟิร์มแวร์ร่วมกับ TESA Digital Twin บน VS Code](../digital-twin/README.md)
- หลักสูตร 3: [การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)](../product-design/README.md)

## ที่มาและสัญญาอนุญาต

เนื้อหาหลักสูตรนี้นำเข้าจาก [drsanti/TESAIoT-Courses](https://github.com/drsanti/TESAIoT-Courses) โฟลเดอร์ `C2/` ที่ commit [`287c218`](https://github.com/drsanti/TESAIoT-Courses/tree/287c21814ba8c75f693136616dcd270349a15966/C2) งานต้นฉบับได้รับทุนจากสมาคมสมองกลฝังตัวไทย (TESA) ซึ่งเป็นผู้ถือสิทธิ์ และเผยแพร่ที่นี่ภายใต้ [CC BY 4.0](../../LICENSES/CC-BY-4.0.txt) TESA Open Knowledge คงข้อความสอนของผู้เขียนไว้ตามเดิม สิ่งที่เพิ่มคือโครงสร้างโมดูล/บทเรียน front matter คำถามเช็กความเข้าใจ หมายเหตุเรื่องเฟิร์มแวร์และเครื่องมือ การแก้ลิงก์ให้ตรงโครงสร้างใหม่ และการปรับถ้อยคำที่ผูกกับการอบรมในห้องเรียน (เช่น รอบอบรม คะแนน) ให้เหมาะกับการเรียนแบบเปิด เครื่องมือและเอกสารของบุคคลที่สาม (Infineon, Blender, ระบบนิเวศ MQTT ฯลฯ) อยู่ภายใต้สัญญาอนุญาตของเจ้าของแต่ละราย

## อ้างอิง TESA

ถ้าคุณนำเนื้อหาหลักสูตรนี้ไปใช้ต่อ ไม่ว่าจะเป็นสไลด์ เอกสารประกอบการสอน มคอ.3 เอกสารแจก หรือ repo โค้ด โปรดอ้างอิงด้วยข้อความนี้:

> "พัฒนาเฟิร์มแวร์ร่วมกับ TESA Digital Twin บน VS Code" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0

ถ้าคุณดัดแปลงเนื้อหา ให้เติม «(ดัดแปลง)» ต่อท้ายข้อความข้างบน และคงเครดิตผู้เขียนต้นฉบับไว้ด้วย:

> เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์ มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
>
> เครื่องมือ Bitstream Studio (VS Code) และ Ternion ที่หลักสูตรนี้ใช้ เป็นผลงานของ ผศ.ดร.สันติ นุราช (KMUTT)

การอ้างอิงไม่ได้หมายความว่า TESA หรือ Infineon รับรองหลักสูตรหรืองานของคุณ ดูรูปแบบและตัวอย่างการอ้างอิงเพิ่มเติม (สไลด์ มคอ.3 เอกสารแจก repo โค้ด) ได้ที่ [ATTRIBUTION.md](../../ATTRIBUTION.md)
