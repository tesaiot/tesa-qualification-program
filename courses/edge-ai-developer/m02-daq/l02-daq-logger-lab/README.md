---
id: edgeai-dev.m02.l02
lang: th
title: {th: 'ลงมือทำ: DAQ logger เก็บ dataset ลง CSV', en: 'Hands-on: a DAQ logger that writes a CSV dataset'}
summary: {th: เขียน DAQ logger ตามสี่จังหวะ schema → sample → record → rate จนเก็บ dataset ที่ติด label ลง /gestures.csv บนบอร์ด แล้วตรวจไฟล์ วัดอัตราจริง และเข้าใจกับดักเงียบที่ทำให้ dataset เสีย, en: 'Write a DAQ logger in four beats (schema, sample, record, rate) until it stores a labelled dataset in /gestures.csv on the board, then check the file, measure the real rate and learn the silent traps that spoil a dataset.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m02.l01]
objectives:
  - {th: 'เติมสี่ช่องใน practice/s04_daq_logger.py จนกดปุ่ม label หนึ่งครั้งแล้วได้ 200 บรรทัดใหม่ในไฟล์ ที่ขึ้นต้นด้วยหัวตาราง label,ax,ay,az,gx,gy,gz และค่าไม่เป็นศูนย์หมด', en: 'Fill the four blanks in practice/s04_daq_logger.py so each label press adds 200 new lines to a file headed label,ax,ay,az,gx,gy,gz with values that are not all zero.'}
  - {th: เก็บครบสาม label อย่างน้อยคนละสอง burst แล้วเปิดไฟล์ใน REPL ยืนยันว่าจำนวนบรรทัดเท่ากับ 1 + (จำนวน burst × 200) และแต่ละ label สมดุล, en: 'Record all three labels at least twice each, then open the file in the REPL and confirm the line count equals 1 + (bursts × 200) and the labels are balanced.'}
  - {th: 'อธิบายได้ว่าทำไมอัตราจริงต่ำกว่า 50 Hz ที่ตั้งไว้ และระบุกับดักเงียบสี่ข้อ (โหมด "w", label ผิด, คอลัมน์สลับ, ลืม \n) ได้', en: 'Explain why the real rate is below the 50 Hz set, and name the four silent traps ("w" mode, wrong label, swapped columns, missing \n).'}
develops: [{skill: ai.data-collection, to: 2}, {skill: lang.micropython, to: 2}, {skill: sys.memory-fs, to: 2}]
assesses: [{skill: ai.data-collection, level: 2, evidence: practice/s04_daq_logger.py}, {skill: sys.memory-fs, level: 2, evidence: practice/s04_daq_logger.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 2.2 — ลงมือทำ: DAQ logger เก็บ dataset ลง CSV

> โมดูล 2 — เก็บข้อมูลจากเซนเซอร์ (DAQ) · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เขียน DAQ logger ตามสี่จังหวะ schema → sample → record → rate จนเก็บ dataset ที่ติด label ลง /gestures.csv บนบอร์ด แล้วตรวจไฟล์ วัดอัตราจริง และเข้าใจกับดักเงียบที่ทำให้ dataset เสีย

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เติมสี่ช่องใน practice/s04_daq_logger.py จนกดปุ่ม label หนึ่งครั้งแล้วได้ 200 บรรทัดใหม่ในไฟล์ ที่ขึ้นต้นด้วยหัวตาราง label,ax,ay,az,gx,gy,gz และค่าไม่เป็นศูนย์หมด
2. เก็บครบสาม label อย่างน้อยคนละสอง burst แล้วเปิดไฟล์ใน REPL ยืนยันว่าจำนวนบรรทัดเท่ากับ 1 + (จำนวน burst × 200) และแต่ละ label สมดุล
3. อธิบายได้ว่าทำไมอัตราจริงต่ำกว่า 50 Hz ที่ตั้งไว้ และระบุกับดักเงียบสี่ข้อ (โหมด "w", label ผิด, คอลัมน์สลับ, ลืม \n) ได้

## ก่อนเริ่ม

ผ่านบทเรียน 2.1 มาแล้ว จำ schema และเหตุผลของ 50 Hz ได้
เตรียมบันทึกการเรียนไว้จดจำนวน burst ต่อ label และจำนวนบรรทัดที่นับได้จริง

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — Emulator จำลอง IMU ให้ครบ ใช้ซ้อมเก็บ dataset ได้ แต่ข้อมูลที่จะเอาไปฝึกโมเดลจริงควรเก็บจากบอร์ด
- **เรียนมาก่อน:** [บทเรียน 2.1 — สุ่มสัญญาณให้ตรงกับโมเดล: อัตราสุ่ม Nyquist หน้าต่าง และ schema ของ CSV](../l01-sampling-and-schema/README.md)

## แนวคิด

logger ก็เดินโครงสี่จังหวะเดิม แต่ในลูปมี **สี่จังหวะของ DAQ**: **schema** (เขียนหัวตารางครั้งเดียวถ้าไฟล์ยังไม่มี โดยใช้ try/except
เปิดอ่านดูก่อน) → **sample** (`sensors.bmi270.motion()` หกแกนในครั้งเดียว) → **record** (`f.write` หนึ่งบรรทัดเรียงคอลัมน์ตรง schema
ปิดด้วย `\n`) → **rate** (`time.sleep_ms(RATE_MS)`) วน `BURST` รอบต่อการกดหนึ่งครั้ง ทุก DAQ ในโลกเดินสี่จังหวะนี้ ต่างแค่รายละเอียด
การเปิดด้วย `with open(PATH, "a")` ต่อหนึ่ง burst ทำให้ไฟล์ถูกปิดและ flush ทุกครั้ง ถอดสายกลางคันก็ยังไม่เสีย burst ที่เขียนจบแล้ว

`time.sleep_ms(20)` ไม่ได้ให้ 50 Hz เป๊ะ เพราะแต่ละรอบยังมีเวลาอ่านเซนเซอร์และเขียนไฟล์บวกเข้าไป อัตราจริงจึงต่ำกว่าเล็กน้อย
(ราว 40–45 Hz) ที่ยอมรับได้คือต่ำกว่าอย่างสม่ำเสมอ ที่แย่คืออัตราแกว่ง บทเรียนคือ **อย่าเชื่อค่าที่ตั้ง จงวัดค่าที่ได้จริง**
ซึ่งฉบับเต็มทำให้ดูด้วย `time.ticks_diff`

เก็บ label ให้ตรงกับคลาสของโมเดล Motion (`idle`, `circle`, `shaking`) และเก็บให้สมดุล แล้ว **ตรวจก่อนเชื่อ** ทุกครั้ง: นับบรรทัด ดูหัว
ดูค่า กับดักที่ไม่ขึ้น error มีสี่ข้อ คือเปิดด้วย `"w"` จนทับของเก่า กดปุ่มผิด label เขียนคอลัมน์สลับ และลืม `\n`
โครงนี้เป็นแม่แบบ เปลี่ยนแค่บรรทัด sample กับ schema ก็เก็บเซนเซอร์อื่นได้ เช่น `sensors.dps368.pressure_temperature()`
หรือ `sensors.sht40.temperature_humidity()` ที่อัตราช้ากว่านี้มาก ไฟล์ `/gestures.csv` นี้คือวัตถุดิบของโมดูล 5 (Training)

## ตัวอย่างสมบูรณ์

`s04_daq_logger.py` ในโฟลเดอร์ examples คือฉบับอ้างอิงที่บทเรียนนี้สร้างขึ้นรอบ ๆ ส่วน `s04_daq_logger_full.py` เพิ่มตัวนับแยก label
(ดู class balance สด ๆ) วัดอัตราจริงเป็น Hz และมีปุ่ม Clear ล้างไฟล์เริ่มใหม่ เปิดเทียบหลังเติมไฟล์ฝึกเสร็จ

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/s04_daq_logger.py](examples/s04_daq_logger.py) | เก็บข้อมูล sensor ลงไฟล์ CSV (Data Acquisition) |
| [examples/s04_daq_logger_full.py](examples/s04_daq_logger_full.py) | เก็บ dataset ลง CSV (ฉบับเต็ม) |

## ฝึกเติม

ไฟล์มี `pass` สี่จุด (บรรทัด 55, 69, 73 และ 76) ตรงสี่จังหวะ DAQ พอดี:
1) schema `f.write("label,ax,ay,az,gx,gy,gz\n")` 2) sample `ax, ay, az, gx, gy, gz = sensors.bmi270.motion()`
3) record `f.write("%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n" % (label, ax, ay, az, gx, gy, gz))` 4) rate `time.sleep_ms(RATE_MS)`
ถ้าทุกบรรทัดเป็น 0.0 แปลว่าช่อง 2 ยังว่าง ถ้าไฟล์ไม่เพิ่มเลยแปลว่าช่อง 3 ยังว่าง

| ไฟล์ฝึก | เรื่อง |
|---|---|
| [practice/s04_daq_logger.py](practice/s04_daq_logger.py) | เก็บข้อมูล sensor ลงไฟล์ CSV (Data Acquisition) (ฉบับฝึกเติมโค้ด) |

## เฉลย

เปิดเฉลยหลังจากลองเองแล้วอย่างน้อยหนึ่งรอบ และอ่าน [วิธีใช้เฉลย](../../README.md#วิธีใช้เฉลย) ก่อน

| เฉลย | คู่กับ |
|---|---|
| [solution/s04_daq_logger.py](solution/s04_daq_logger.py) | [practice/s04_daq_logger.py](practice/s04_daq_logger.py) |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. เรียงสี่จังหวะของ DAQ ในไฟล์ logger *(เรียงลำดับ · เป้าหมายข้อ 1)*
   - ก) record: เขียนหนึ่งบรรทัดลงไฟล์
   - ข) schema: เขียนหัวตารางครั้งเดียว
   - ค) rate: time.sleep_ms(RATE_MS)
   - ง) sample: sensors.bmi270.motion()

   <details><summary>เฉลย</summary>

   **ข → ง → ก → ค** — schema ทำครั้งเดียวตอนเริ่ม แล้ววน sample → record → rate ครบ BURST รอบต่อการกดหนึ่งครั้ง

   </details>

2. เปิดไฟล์ดูแล้วทุกบรรทัดเป็น 0.0000 หมดยกเว้นคอลัมน์ label ช่องใดยังว่าง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) ช่อง 1 schema
   - ข) ช่อง 2 sample ที่อ่าน motion()
   - ค) ช่อง 3 record
   - ง) ช่อง 4 rate

   <details><summary>เฉลย</summary>

   **ข** — บรรทัดสำรอง ax = ay = ... = 0.0 ทำให้โปรแกรมไม่ error แต่ถ้าไม่ได้อ่านเซนเซอร์จริง ทุกค่าจะเป็นศูนย์ dataset จึงไร้ประโยชน์

   </details>

3. เก็บ idle 2 burst, circle 2 burst และ shaking 3 burst ไฟล์ที่ถูกต้องควรมีกี่บรรทัด (รวมหัวตาราง) *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) 1400
   - ข) 1401
   - ค) 1407
   - ง) 601

   <details><summary>เฉลย</summary>

   **ข** — 7 burst × 200 = 1400 บรรทัดข้อมูล บวกหัวตาราง 1 บรรทัด เป็น 1401 และ shaking มีมากกว่าคลาสอื่นอยู่หนึ่ง burst ควรเก็บเพิ่มให้สมดุล

   </details>

4. ตั้ง RATE_MS = 20 แต่วัดได้จริงราว 43 Hz เพราะอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) เซนเซอร์เสีย
   - ข) แต่ละรอบมีเวลาอ่านเซนเซอร์และเขียนไฟล์บวกกับ sleep 20 ms หนึ่งรอบจริงจึงยาวกว่า 20 ms
   - ค) time.sleep_ms ปัดเป็นวินาที
   - ง) flash เขียนได้แค่ 43 ครั้งต่อวินาที

   <details><summary>เฉลย</summary>

   **ข** — นี่คือความจริงของงานฝังตัว ตราบใดที่ต่ำกว่าอย่างสม่ำเสมอก็ยังใช้ได้ สิ่งสำคัญคือวัดค่าจริงแทนการเชื่อค่าที่ตั้ง

   </details>

5. ข้อใดเป็นกับดักเงียบที่โปรแกรมรันผ่านแต่ dataset ผิด (เลือกทุกข้อที่ถูก) *(เลือกได้หลายข้อ · เป้าหมายข้อ 3)*
   - ก) เขียน gx ก่อน ax ไม่ตรง schema
   - ข) ลืม \n ท้ายบรรทัด ทุก sample ต่อกันเป็นบรรทัดเดียว
   - ค) สะกด sensors ผิดจนเกิด NameError
   - ง) เปิดไฟล์ด้วย "w" ในลูปบันทึก

   <details><summary>เฉลย</summary>

   **ก, ข, ง** — NameError ขึ้น error ให้เห็นทันทีจึงไม่ใช่กับดักเงียบ ส่วนอีกสามข้อรันผ่านแต่ข้อมูลผิด ต้องเปิดไฟล์ตรวจเสมอ

   </details>

## แล็บ

**MVP ของชุดบทเรียน 2.1–2.2:** logger ที่เก็บ N samples ที่ติด label ลง CSV ได้จริง เลือก label ได้ สุ่มที่อัตราคงที่ เขียนลงไฟล์บนบอร์ด และตรวจได้ว่าจำนวนบรรทัดถูกต้อง

- [ ] เติมไฟล์ฝึกครบสี่ช่อง เก็บ dataset ได้บน Emulator หรือบอร์ด
- [ ] เก็บครบสาม label อย่างน้อยคนละสอง burst แล้วนับบรรทัดใน REPL ให้ได้ 1 + (burst × 200)
- [ ] เปลี่ยน `RATE_MS` เป็น 40 (25 Hz) เก็บอีกชุด แล้วจดลงบันทึกการเรียนว่าเวลาต่อ burst และรูปคลื่นต่างไปอย่างไร
- [ ] อธิบายได้ว่าโค้ดทำสี่จังหวะ schema, sample, record, rate ตรงไหน และทำไม 50 Hz

## ไปต่อ

ชุดบทเรียนถัดไป (บทเรียน 2.3–2.4) เราจะเก็บเสียงกับ IMU พร้อมกันบนเส้นเวลาเดียว ให้ dataset รวยขึ้น

บทเรียนถัดไป: [บทเรียน 2.3 — เสียงและหลายเซนเซอร์บนเส้นเวลาเดียว: PDM 16 kHz ประทับเวลา และ jitter](../l03-audio-and-timeline/README.md)

## สะท้อนคิด

- dataset ของคุณสมดุลหรือยัง ถ้าไม่ คุณจะเก็บเพิ่มอย่างไรโดยไม่ทำให้ label ปนกัน
- ถ้าอยากเก็บความดันอากาศแทน IMU คุณต้องแก้กี่บรรทัด และควรตั้ง RATE_MS เท่าไร
