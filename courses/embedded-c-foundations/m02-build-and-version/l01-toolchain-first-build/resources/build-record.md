# บันทึกการ build (build record)

คัดลอกไฟล์นี้ไปไว้ในโปรเจกต์ของคุณ (เช่น `docs/build-record.md`) แล้วเติมทุกช่องหลัง build ครั้งแรกสำเร็จ
และทุกครั้งที่เปลี่ยนเครื่องมือ บันทึกนี้คือสิ่งที่ทำให้คนอื่น หรือตัวคุณเองในอีกหกเดือน build เฟิร์มแวร์ตัวเดิมได้อีกครั้ง

คำสั่งในวงเล็บคือวิธีหาค่านั้น ให้คัดลอกผลลัพธ์จริงมาวาง อย่าพิมพ์จากความจำ

## เครื่องและเครื่องมือ

| รายการ | ค่า | ได้มาจาก |
|---|---|---|
| วันที่ build | | |
| ระบบปฏิบัติการของเครื่อง build | | `uname -a` หรือ About ของ Windows |
| ModusToolbox | | หน้า About ของ ModusToolbox หรือชื่อโฟลเดอร์ `tools_3.x` ที่ใช้ |
| Arm GCC | | `arm-none-eabi-gcc --version` (บรรทัดแรก) |
| GNU Make | | `make --version` (บรรทัดแรก) |
| Git | | `git --version` |
| bash | | `bash --version` (บรรทัดแรก ต้องเป็น 4 ขึ้นไป) |

## ซอร์สที่ build

| รายการ | ค่า | ได้มาจาก |
|---|---|---|
| repository | https://github.com/tesaiot/tesaiot-pse84-devkit-sdk | |
| แพ็กเกจที่แตกมา build | | ชื่อ release และ SHA-256 ของ zip จาก `SHA256SUMS.txt` เช่น `fw-c-only-v1.10.0` |
| commit ของซอร์สที่อ่านประกอบ | | `git rev-parse HEAD` ใน clone ที่ใช้อ่าน (หลักสูตรนี้ใช้ `ef72c1b`) |
| commit ของโปรเจกต์ของคุณเอง | | `git rev-parse HEAD` ในโปรเจกต์ของคุณ (บทเรียน 2.3) |
| มีไฟล์ที่แก้แต่ยังไม่ commit ไหม | | `git status --short` (ว่าง = ไม่มี) |
| variant | mtb-only | บรรทัด `variant:` ของ `./setup.sh --check` |
| ผลตรวจ patch ของ dependency | | บรรทัด `OK` ของ `shasum -a 256 -c .../PATCHED.sha256` |

## ผลลัพธ์

| รายการ | ค่า | ได้มาจาก |
|---|---|---|
| คำสั่ง build ที่ใช้ทั้งบรรทัด | | รวมตัวแปรทุกตัว เช่น `ENABLE_PAGE_EXAMPLES=1` |
| ขนาดของ `app_combined.hex` | | `wc -c build/app_combined.hex` |
| SHA-256 ของ `app_combined.hex` | | `shasum -a 256 build/app_combined.hex` หรือ `sha256sum` |
| บรรทัดยืนยันจากการ flash | | บรรทัดสุดท้ายของ `make program` |
| บรรทัด `[HB]` แรกบน serial console | | console 115200 8N1 หลังถอดสายเสียบใหม่ |
| ป้ายรุ่นบนหน้าจอ Home | | ควรลงท้ายด้วย `-mtb_only` |

## ปัญหาที่เจอและวิธีแก้

เขียนสั้น ๆ ทุกครั้งที่ติด อาการ สาเหตุที่พิสูจน์ได้ และสิ่งที่แก้ บันทึกนี้มีค่ากว่าที่คิดเมื่อเพื่อนร่วมทีมเจออาการเดียวกัน
