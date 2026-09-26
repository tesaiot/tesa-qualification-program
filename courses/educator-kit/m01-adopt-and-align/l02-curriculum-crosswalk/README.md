---
id: edu.m01.l02
lang: th
title:
  th: ตารางเทียบผลลัพธ์การเรียนรู้ (Curriculum Crosswalk)
  en: The curriculum crosswalk
summary:
  th: เทียบบทเรียนแต่ละบทกับผลลัพธ์การเรียนรู้ของรายวิชา ด้าน K/S/E/C ตามมาตรฐานคุณวุฒิ 2565 การประเมิน ชั่วโมง หน่วยสมรรถนะ TPQI และคุณลักษณะบัณฑิต Washington Accord สำหรับ TABEE
  en: Map each lesson to a course learning outcome, the 2565 (2022) Thai qualification-standard domains K/S/E/C, assessment, hours, TPQI units and Washington Accord attributes for TABEE.
level: L3
time_min: {concept: 20, practise: 30, check: 5}
hardware: {emulator: false, boards: [none]}
prerequisites: [edu.m01.l01]
objectives:
  - th: เขียนผลลัพธ์การเรียนรู้ระดับรายวิชา (CLO) ในรูปกริยาวัดผลได้ + เงื่อนไข + เกณฑ์ ได้อย่างน้อย 3 ข้อ และระบุระดับ Bloom ของแต่ละข้อ
    en: Write at least three course learning outcomes as measurable verb + condition + criterion, naming each one's Bloom level.
  - th: จัดผลลัพธ์แต่ละข้อลงด้าน ความรู้ ทักษะ จริยธรรม หรือลักษณะบุคคล ตามประกาศมาตรฐานคุณวุฒิระดับอุดมศึกษา พ.ศ. 2565 ได้ถูกต้อง
    en: Assign each outcome to the Knowledge, Skills, Ethics or Character domain of the 2022 higher-education qualification standard.
  - th: เติมตารางเทียบรายบทเรียนอย่างน้อย 3 แถว ให้ครบทุกคอลัมน์ รวมหน่วย TPQI และ WA ในแถวที่เกี่ยวข้อง
    en: Complete at least three crosswalk rows in every column, including TPQI units and WA attributes where they apply.
develops:
  - {skill: edu.lesson-design, to: 3}
  - {skill: edu.assessment, to: 2}
assesses:
  - {skill: edu.lesson-design, level: 3, evidence: resources/crosswalk-template.md}
context: {audience: educator, frameworks: [TQF-2565, TPQI, IEA-GAPC-2021]}
status: alpha
translation: done
---

## เป้าหมาย

1. เขียน CLO ที่วัดผลได้ พร้อมระดับ Bloom
2. จัด CLO ลงด้าน K/S/E/C ตามมาตรฐานคุณวุฒิ 2565
3. เติมตารางเทียบรายบทเรียนให้ครบทุกคอลัมน์

## ก่อนเริ่ม

- จากบทที่แล้ว คุณเลือกรูปแบบการนำไปใช้แบบไหน และใช้บทเรียนใดบ้าง
- ผลลัพธ์การเรียนรู้ของรายวิชาคุณตอนนี้เขียนด้วยกริยาอะไร "เข้าใจ" "รู้" หรือกริยาที่วัดได้

## ดูของจริงก่อน

เปิดหน้าบทเรียน [โปรแกรมแรก: เขียนบนจอและเปิดไฟ](../../../explorer/m01-meet-embedded/l03-first-program/README.md) ดูส่วนหัว (front matter) ของไฟล์
คุณจะเห็น `objectives` ที่เขียนเป็นกริยาวัดผลได้ `develops` ที่บอก skill id และระดับ `time_min` ที่บอกเวลา และ `quiz.yaml` ที่มีข้อสอบผูกกับเป้าหมายทุกข้อ
ข้อมูลเหล่านี้ย้ายลงตารางเทียบของคุณได้เกือบทั้งหมด งานของคุณคือเชื่อมมันกับเอกสารของรายวิชาและกรอบมาตรฐาน

## แนวคิด

### 1. เขียนผลลัพธ์ก่อน แล้วค่อยออกแบบการประเมินและกิจกรรม

หลัก **constructive alignment** ให้ผลลัพธ์ การประเมิน และกิจกรรมการเรียนรู้ ชี้ไปทางเดียวกัน
([Biggs 1996](https://doi.org/10.1007/BF00138871)) และใช้ **Bloom ฉบับปรับปรุง** เลือกกริยาที่วัดได้
([Krathwohl 2002](https://doi.org/10.1207/s15430421tip4104_2))

| แบบที่วัดไม่ได้ | แบบที่วัดได้ (กริยา + เงื่อนไข + เกณฑ์) | Bloom |
|---|---|---|
| เข้าใจ GPIO | สั่งหลอด LED กะพริบตามจำนวนรอบที่กำหนดด้วย `gpio.led().on()/off()` บนบอร์ดหรืออีมูเลเตอร์ โดยจบที่สถานะดับทุกครั้ง | ประยุกต์ (apply) |
| รู้จัก MQTT | อธิบายบทบาทของ broker, topic, publish และ subscribe ด้วยแผนภาพ ถูกครบทั้งสี่คำ | เข้าใจ (understand) |
| รู้เรื่องความปลอดภัย | เปรียบเทียบความเสี่ยงของ broker สาธารณะพอร์ต 1883 กับ MQTTs และเลือกทางที่เหมาะกับข้อมูลที่กำหนดพร้อมเหตุผล | วิเคราะห์/ประเมิน |

### 2. ผลลัพธ์สี่ด้านตามมาตรฐานคุณวุฒิ 2565

ประกาศคณะกรรมการมาตรฐานการอุดมศึกษา เรื่อง รายละเอียดผลลัพธ์การเรียนรู้ตามมาตรฐานคุณวุฒิระดับอุดมศึกษา พ.ศ. 2565
(ราชกิจจานุเบกษา เล่ม 139 ตอนพิเศษ 212 ง ลงวันที่ 9 กันยายน 2565 ใช้บังคับตั้งแต่ 27 กันยายน 2565)
กำหนดให้ผลลัพธ์การเรียนรู้ประกอบด้วยอย่างน้อยสี่ด้าน คือ **ความรู้ (Knowledge) ทักษะ (Skills) จริยธรรม (Ethics) และลักษณะบุคคล (Character)**
([หน้าประกาศ สำนักงานปลัดกระทรวง อว.](https://www.ops.go.th/en/role/edu-standard/item/6940-2022-07-22-02-54-49))

บทเรียนด้านระบบฝังตัวส่วนใหญ่เสริมด้าน K และ S เป็นหลัก ส่วนด้าน E และ C มาจากกิจกรรมอย่าง
การอ้างอิงแหล่งที่มาให้ถูก (ดูบทถัดไป) การไม่ใส่รหัสผ่านในงานที่เผยแพร่ การทำงานเป็นทีมในแล็บ และ portfolio ที่ซื่อตรงต่อสิ่งที่ทำจริง

### 3. สองกรอบภายนอกที่มักถูกถาม

- **TPQI** คุณวุฒิวิชาชีพ "นักพัฒนาระบบสมองกลฝังตัว ระดับ 4" มีสองหน่วยสมรรถนะ คือ ICT-CSOS-107B (พัฒนาฮาร์ดแวร์ระบบสมองกลฝังตัว)
  และ ICT-FYNH-108B (พัฒนาซอฟต์แวร์ระบบสมองกลฝังตัว) ([TPQI-Net](https://tpqi-net.tpqi.go.th/qualifications/standard/book?id=81&cer_level_id=2865))
  ใส่หน่วยเหล่านี้เฉพาะบทเรียนที่เกี่ยวข้องจริง บทเรียนระดับ L1–L2 มักยังไม่ถึงเกณฑ์ของหน่วยสมรรถนะ แต่เป็นฐานของมัน
- **TABEE** การรับรองหลักสูตรวิศวกรรมของสภาวิศวกรใช้เกณฑ์คุณลักษณะบัณฑิตตาม Washington Accord
  (สภาวิศวกรอยู่ในรายชื่อ provisional signatory ของ Washington Accord ตาม[รายชื่อของ IEA](https://www.internationalengineeringalliance.org/accords/washington-accord#list-of-signatories)) ซึ่งกำหนดไว้ใน IEA Graduate Attributes and Professional Competencies ฉบับ 2021
  ([IEA GAPC 2021](https://www.internationalengineeringalliance.org/assets/Uploads/IEA-Graduate-Attributes-and-Professional-Competencies-2021.1-Sept-2021.pdf))
  มี 11 ข้อ WA1–WA11 รายชื่ออยู่ท้ายแม่แบบ

แผนที่ทักษะของ TESA ใช้ระดับ L1–L5 ที่ตัวเลขตรงกับระดับคุณวุฒิวิชาชีพ ดูรายละเอียดที่ [tqp/levels.md](../../../../tqp/levels.md)

## ตัวอย่างสมบูรณ์

สามแถวตัวอย่าง (ใช้บทเรียนที่มีอยู่จริงในคลัง)

| บทเรียน | CLO + กริยา Bloom | K/S/E/C | การประเมิน | ชั่วโมง | หน่วย TPQI | WA | skill id |
|---|---|---|---|---|---|---|---|
| `explore.m01.l03` | CLO1 สั่งหลอด LED กะพริบตามจำนวนรอบที่กำหนด และจบที่สถานะดับ (ประยุกต์) | S | `quiz.yaml` + ไฟล์ฝึก `practice/blink_count.py` | 0.15 / 0.25 / 0.1 | ฐานของ ICT-FYNH-108B | WA5 | `mcu.gpio` |
| `explore.m02.l02` | CLO2 อธิบายบทบาทของ broker, topic, publish, subscribe ด้วยแผนภาพ (เข้าใจ) | K | แผนภาพใน portfolio + `quiz.yaml` | 0.2 / 0.2 / 0.1 | | WA1 | `proto.mqtt`, `iot.fundamentals` |
| `explore.m02.l03` | CLO3 อ้างอิงแหล่งที่มาของสื่อที่นำมาดัดแปลงได้ถูกต้องตามสัญญาอนุญาต (ประยุกต์) | E | ข้อความอ้างอิงในงานที่ส่ง | 0.15 / 0.15 / 0.1 | | WA7 | `soft.communication` |

- **ท่าที่ 1** คัดลอก `objectives` และ `develops` จากหน้าบทเรียน
- **ท่าที่ 2** เขียน CLO ของรายวิชาที่บทเรียนนั้นรับใช้ อาจรวมหลายบทเรียนต่อหนึ่ง CLO
- **ท่าที่ 3** เลือกด้าน K/S/E/C ที่เด่นที่สุด ไม่ต้องใส่ทุกด้านทุกแถว
- **ท่าที่ 4** ใส่หน่วย TPQI และ WA เฉพาะที่อธิบายได้ว่าเกี่ยวจริง ถ้าต้องอธิบายยาว แปลว่าอาจไม่เกี่ยว

## ฝึกเติม

คัดลอก [resources/crosswalk-template.md](resources/crosswalk-template.md) แล้วเติมอย่างน้อยสามแถวสำหรับรายวิชาของคุณ
ใช้บทเรียนที่เลือกไว้ในบทที่แล้ว

## เช็กความเข้าใจ

ตอบคำถามใน [quiz.yaml](quiz.yaml) ถูกตั้งแต่ 80% ขึ้นไปถือว่าผ่าน

## ไปต่อ

ถ้าสถาบันของคุณกำลังเตรียมรับการประเมินจาก TABEE ตารางนี้ใช้เป็นหลักฐานประกอบได้ แต่คำตัดสินว่าหลักฐานเพียงพอหรือไม่เป็นของผู้ประเมิน
และรูปแบบเอกสารรายละเอียดรายวิชาที่แต่ละสถาบันใช้อาจต่างกัน ให้ตรวจกับหน่วยงานวิชาการของสถาบัน

## สะท้อนคิด

CLO ข้อไหนของรายวิชาคุณที่ยังไม่มีบทเรียนหรือการประเมินรองรับเลย ช่องว่างนั้นควรเติมด้วยอะไร
