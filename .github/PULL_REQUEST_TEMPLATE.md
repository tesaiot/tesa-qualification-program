## สรุปการเปลี่ยนแปลง / Summary

<!-- บอกสั้น ๆ ว่าเปลี่ยนอะไรและทำไม ถ้าเกี่ยวกับ issue ให้เขียน "Closes #123" -->
<!-- What changed and why. Link the issue, e.g. "Closes #123". -->

## ทดสอบบน / Tested on

<!-- จำเป็นสำหรับบทเรียนหรือโค้ด / Required for lessons and code -->
- บอร์ด / Board: <!-- Eva Kit (KIT_PSE84_EVAL_EPC2) | TESAIoT Dev Kit | ไม่มี / none -->
- เฟิร์มแวร์ / Firmware: <!-- เช่น BENTO MicroPython firmware x.y.z -->
- Toolchain: <!-- เช่น ModusToolbox x.y, MicroPython x.y -->
- BENTO Emulator / IDE: <!-- เวอร์ชันหรือวันที่ทดสอบ / version or test date -->

## Checklist

- [ ] ทุก commit มี DCO sign-off (`git commit -s`) / Every commit is signed off (DCO)
- [ ] `python3 tools/validate.py` ผ่าน / The validator passes
- [ ] รันโค้ดทุกไฟล์ที่เพิ่มหรือแก้บนบอร์ดจริงหรือ emulator แล้ว และกรอก "ทดสอบบน" ด้านบน / I ran every added or changed code file on a board or the emulator and filled in "Tested on"
- [ ] สถานะภาษา: ฉบับไทยและอังกฤษตรงกัน หรือตั้ง `translation: pending` แล้ว / TH/EN status: both match, or `translation: pending` is set
- [ ] ภาพใหม่ทุกภาพมีรายการใน `credits.yaml` และมีข้อความ alt / Every new image is listed in `credits.yaml` and has alt text
- [ ] ไม่มีข้อมูลลับหรือข้อมูลภายใน: ไม่มีรหัส Wi-Fi, token, รหัสผ่าน broker, กุญแจ หรือ path ภายใน ใช้ค่าตัวแทนเท่านั้น / No secrets or internal details: placeholders only
- [ ] ใช้คำตามกติกา: บทเรียน / โมดูล / หลักสูตร และ "คาบเวลา" เฉพาะคาบของสัญญาณ / The words rule is followed
- [ ] skill ID ที่ใช้มีอยู่ใน `skills/skills.yaml` / Every skill ID exists in `skills/skills.yaml`
- [ ] ถ้านำเนื้อหาหรือโค้ดจากที่อื่นมา ระบุแหล่งและสัญญาอนุญาตแล้ว / Borrowed content or code is credited with its licence

ฉันยอมรับว่างานนี้เผยแพร่ใน TESA Open Knowledge พร้อมเครดิตของสมาคมสมองกลฝังตัวไทย (TESA) ตาม [ATTRIBUTION.md](https://github.com/tesaiot/tesa-qualification-program/blob/main/ATTRIBUTION.md)
By opening this pull request I agree that this work is published in TESA Open Knowledge with the credit of the Thai Embedded Systems Association (TESA), as set out in [ATTRIBUTION.md](https://github.com/tesaiot/tesa-qualification-program/blob/main/ATTRIBUTION.md).
