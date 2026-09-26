---
id: edgeai-dev.m02.l04
lang: th
title: {th: 'ลงมือทำ: เก็บ IMU กับเสียงลงไฟล์เดียว', en: 'Hands-on: IMU and sound in one file'}
summary: {th: เติมสี่ก้าวในลูปของ s05_multicapture.py คือประทับเวลา อ่าน IMU อ่านเสียง และเขียนแถว จนได้ /multicapture.csv ที่ทุกแถวมัด IMU กับระดับเสียงบน t_ms เดียวกัน แล้วตรวจไฟล์และ jitter ด้วยตัวเอง, en: 'Fill the four loop steps of s05_multicapture.py (timestamp, read IMU, read sound, write the row) until /multicapture.csv ties IMU and sound level to one t_ms on every row, then check the file and the jitter yourself.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m02.l03]
objectives:
  - {th: 'เติมสี่ช่องใน practice/s05_multicapture.py จนการกดปุ่ม label หนึ่งครั้งเพิ่ม 200 แถวลง /multicapture.csv ที่มีคอลัมน์ t_ms, label, ax..gz และ db ครบ', en: 'Fill the four blanks in practice/s05_multicapture.py so one label press adds 200 rows to /multicapture.csv with t_ms, label, ax..gz and db columns.'}
  - {th: ตรวจไฟล์ที่เก็บได้ว่า t_ms เพิ่มขึ้นต่อชุดและห่างกันราว 20 ms ค่า db เปลี่ยนตามเสียงจริง และวินิจฉัยได้ว่าช่องใดยังว่างจากอาการในไฟล์, en: Check the recorded file - t_ms rises within each burst about 20 ms apart and db follows real sound - and diagnose which blank is empty from the symptoms in the file.}
  - {th: อธิบายได้ว่าทำไมต้องเปิด PDM นอกลูปครั้งเดียว และคืนไมโครโฟนด้วย pdm.deinit() ในบล็อก finally, en: Explain why the PDM is opened once outside the loop and released with pdm.deinit() in the finally block.}
develops: [{skill: ai.data-collection, to: 2}, {skill: lang.micropython, to: 2}, {skill: sys.sensors-actuators, to: 2}]
assesses: [{skill: ai.data-collection, level: 2, evidence: practice/s05_multicapture.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 2.4 — ลงมือทำ: เก็บ IMU กับเสียงลงไฟล์เดียว

> โมดูล 2 — เก็บข้อมูลจากเซนเซอร์ (DAQ) · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เติมสี่ก้าวในลูปของ s05_multicapture.py คือประทับเวลา อ่าน IMU อ่านเสียง และเขียนแถว จนได้ /multicapture.csv ที่ทุกแถวมัด IMU กับระดับเสียงบน t_ms เดียวกัน แล้วตรวจไฟล์และ jitter ด้วยตัวเอง

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เติมสี่ช่องใน practice/s05_multicapture.py จนการกดปุ่ม label หนึ่งครั้งเพิ่ม 200 แถวลง /multicapture.csv ที่มีคอลัมน์ t_ms, label, ax..gz และ db ครบ
2. ตรวจไฟล์ที่เก็บได้ว่า t_ms เพิ่มขึ้นต่อชุดและห่างกันราว 20 ms ค่า db เปลี่ยนตามเสียงจริง และวินิจฉัยได้ว่าช่องใดยังว่างจากอาการในไฟล์
3. อธิบายได้ว่าทำไมต้องเปิด PDM นอกลูปครั้งเดียว และคืนไมโครโฟนด้วย pdm.deinit() ในบล็อก finally

## ก่อนเริ่ม

ผ่านบทเรียน 2.3 มาแล้ว เข้าใจ dBFS เส้นเวลาร่วม และ jitter
เตรียมบอร์ดที่เก็บเสียงได้ และเปิด REPL ไว้ตรวจไฟล์หลังเก็บเสร็จ

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — เก็บเสียงจริงต้องใช้บอร์ดที่ไมโครโฟน PDM ใช้ได้ (ผู้เขียนทดสอบบน PSoC Edge AI Kit บน TESAIoT Dev Kit การเปิด PDM ยังชน clock ของระบบเสียง) Emulator ให้เสียงสังเคราะห์ใช้ซ้อมโครงโปรแกรมได้ แต่รันผ่านบน Emulator ไม่ใช่หลักฐานว่าจะรันผ่านบนบอร์ด
- **เรียนมาก่อน:** [บทเรียน 2.3 — เสียงและหลายเซนเซอร์บนเส้นเวลาเดียว: PDM 16 kHz ประทับเวลา และ jitter](../l03-audio-and-timeline/README.md)

## แนวคิด

หัวใจทั้งไฟล์อยู่ใน `record()` แต่ละรอบของ `for _ in range(BURST)` เดินสี่ก้าวเป๊ะ: (1) ประทับเวลา
`t_ms = time.ticks_diff(time.ticks_ms(), t0)` (2) อ่าน IMU `ax, ay, az, gx, gy, gz = sensors.bmi270.motion()`
(3) อ่านเสียง `pdm.readinto(buf)` แล้ว `db = dbfs(buf)` ที่ให้ไว้แล้ว (4) เขียนแถว
`f.write("%d,%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.1f\n" % (t_ms, label, ax, ay, az, gx, gy, gz, db))`
ทั้งสี่ก้าวเกิดในรอบเดียวก่อน `time.sleep_ms(RATE_MS)` จึงถือว่าเป็นเวลาเดียวกัน ลำดับสำคัญ: อ่านทั้งคู่ก่อนเขียนแถวเสมอ
ไม่งั้นข้อมูลจะเหลื่อมกันหนึ่งรอบ

ส่วนบนของไฟล์ให้ไว้แล้ว: เปิด `PDM_PCM(0, sck="P8_5", data="P8_6", sample_rate=16000)` **ครั้งเดียวนอกลูป** เหมือนสร้าง widget ครั้งเดียว
เพราะเปิดปิดซ้ำทั้งกินเวลาและเสี่ยงชน เตรียม buffer และเขียนหัวตารางถ้าไฟล์ยังไม่มี `t0` ถูกตั้งใหม่ทุกครั้งที่กดปุ่ม label
แต่ละชุดจึงเริ่มนับเวลาจากศูนย์ของตัวเอง ตอนออก บล็อก `finally` เรียก `pdm.deinit()` คืนไมโครโฟนเสมอ ไม่งั้นโปรแกรมเสียงตัวถัดไป
อาจเปิด PDM ไม่ได้เพราะฮาร์ดแวร์ยังถูกจองอยู่

เก็บเสร็จแล้ว **ตรวจก่อนเชื่อ**: จำนวนแถวควรเท่ากับ `BURST × จำนวนครั้งที่กด`, `t_ms` เพิ่มขึ้นในแต่ละชุด และ `db` เปลี่ยนตามเสียงจริง
ถ้า `t_ms` เป็น 0 ทุกแถวแปลว่าก้าว 1 ยังว่าง ถ้า `db` นิ่งแปลว่าก้าว 3 ยังว่างหรือไมค์ไม่ได้เสียง ถ้าไฟล์ว่างแปลว่าก้าว 4 ยังว่าง

## ตัวอย่างสมบูรณ์

`s05_multicapture_full.py` เก็บทั้ง CSV และ WAV เสียงดิบคู่กัน วัดช่วงเวลาจริงต่อแถวและ jitter สูงสุด แล้วสรุปจำนวนแถว
peak dBFS และช่วงเวลาเฉลี่ยต่อ label ลงไฟล์ manifest เปิดอ่านหลังไฟล์ฝึกทำงานแล้ว เพื่อดูว่า dataset ระดับใช้งานจริงต้องเก็บอะไรเพิ่ม

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/s05_multicapture_full.py](examples/s05_multicapture_full.py) | Multi-Sensor Sync Capture (ฉบับเต็ม) |

## ฝึกเติม

ไฟล์มี `# เติม` สี่จุดที่บรรทัด 78, 83, 88 และ 92 เรียงตามสี่ก้าว แทน `pass` (และค่าสำรองที่เป็นศูนย์) ด้วยคำสั่งตามคำใบ้
แล้ว Program to Device เลือก label ทำท่าและส่งเสียงพร้อมกันราวสี่วินาที ดูจำนวนแถวขึ้นบนจอ แล้วเปิด CSV ตรวจ

| ไฟล์ฝึก | เรื่อง |
|---|---|
| [practice/s05_multicapture.py](practice/s05_multicapture.py) | เก็บ 2 เซนเซอร์พร้อมกันบนเส้นเวลาเดียว (ฉบับฝึกเติมโค้ด) |

## เฉลย

เปิดเฉลยหลังจากลองเองแล้วอย่างน้อยหนึ่งรอบ และอ่าน [วิธีใช้เฉลย](../../README.md#วิธีใช้เฉลย) ก่อน

| เฉลย | คู่กับ |
|---|---|
| [solution/s05_multicapture.py](solution/s05_multicapture.py) | [practice/s05_multicapture.py](practice/s05_multicapture.py) |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. เรียงสี่ก้าวในหนึ่งรอบของลูป record() *(เรียงลำดับ · เป้าหมายข้อ 1)*
   - ก) pdm.readinto(buf) แล้ว db = dbfs(buf)
   - ข) t_ms = time.ticks_diff(time.ticks_ms(), t0)
   - ค) f.write(...) หนึ่งแถว
   - ง) ax, ay, az, gx, gy, gz = sensors.bmi270.motion()

   <details><summary>เฉลย</summary>

   **ข → ง → ก → ค** — ประทับเวลา → อ่าน IMU → อ่านเสียง → เขียนแถว แล้วค่อย sleep_ms ไปรอบถัดไป ทุกค่าในแถวจึงเป็นเวลาเดียวกัน

   </details>

2. เปิด CSV แล้วพบว่า t_ms เป็น 0 ทุกแถว แต่ IMU และ db เปลี่ยนตามจริง ช่องใดยังว่าง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) ก้าว 1 ประทับเวลา
   - ข) ก้าว 2 อ่าน IMU
   - ค) ก้าว 3 อ่านเสียง
   - ง) ก้าว 4 เขียนแถว

   <details><summary>เฉลย</summary>

   **ก** — บรรทัดสำรอง t_ms = 0 ยังอยู่ เส้นเวลาจึงหาย จับคู่ตามเวลาไม่ได้ ต้องเติม ticks_diff

   </details>

3. คอลัมน์ db ของทุกแถวเป็น −96.0 ตลอดแม้ปรบมือใกล้บอร์ด สาเหตุที่น่าจะเป็นคืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) ยังไม่ได้เติม pdm.readinto(buf) buffer จึงเป็นศูนย์ หรือไมโครโฟนไม่ได้รับเสียง
   - ข) RATE_MS ตั้งสูงเกินไป
   - ค) ลืม \n ท้ายบรรทัด
   - ง) t0 ไม่ได้ตั้งใหม่

   <details><summary>เฉลย</summary>

   **ก** — dbfs() คืน −96.0 เมื่อ RMS เป็นศูนย์ ซึ่งเกิดเมื่อ buffer ไม่เคยถูกเติมด้วยเสียงจริง

   </details>

4. ข้อใดเป็นเหตุผลที่ต้องเรียก pdm.deinit() ใน finally (เลือกทุกข้อที่ถูก) *(เลือกได้หลายข้อ · เป้าหมายข้อ 3)*
   - ก) ไม่ว่าจะออกด้วยปุ่ม back หรือ error ไมโครโฟนจะถูกคืนเสมอ
   - ข) ถ้าไม่คืน โปรแกรมเสียงตัวถัดไปอาจเปิด PDM ไม่ได้เพราะฮาร์ดแวร์ยังถูกจอง
   - ค) deinit() ทำให้ไฟล์ CSV ถูกบันทึก
   - ง) เป็นนิสัยเดียวกับ edge_ai.stop() คือทิ้งเครื่องไว้ในสถานะที่รู้แน่

   <details><summary>เฉลย</summary>

   **ก, ข, ง** — ไฟล์ CSV ถูกปิดและ flush เองเมื่อออกจาก with ส่วน deinit() มีไว้คืนฮาร์ดแวร์ไมโครโฟน

   </details>

## แล็บ

**MVP ของชุดบทเรียน 2.3–2.4:** dataset ที่ log อย่างน้อยสองเซนเซอร์บนเส้นเวลาเดียว ไฟล์ `/multicapture.csv` มีคอลัมน์ `t_ms` + IMU + `db` และค่าจริงเปลี่ยนตามท่าและเสียง

- [ ] เติมไฟล์ฝึกครบสี่ช่อง รันบนบอร์ดจนได้ `/multicapture.csv`
- [ ] เก็บครบสาม label โดยแต่ละ label ทำท่าและส่งเสียงต่างกัน แล้วยืนยันใน CSV ว่า `db` และ IMU เปลี่ยนตามจริง
- [ ] ตรวจเส้นเวลา: `t_ms` ห่างกันใกล้ 20 ms ไหม จดลงบันทึกการเรียนว่าเจอ jitter ตรงไหน แล้วลองลด `CHUNK` เทียบ
- [ ] อธิบายได้ว่าโค้ดประทับ `t_ms` ตรงไหน อ่านสองเซนเซอร์ตรงไหน และทำไมต้องอยู่ในรอบเดียว

## ไปต่อ

โมดูลถัดไป (Processing) เราจะแปลงสัญญาณดิบที่เก็บมาเป็นปริมาณเชิงฟิสิกส์ เช่น มุมเอียง ความสูง และระดับเสียง แล้วโชว์เป็นเกจสด

บทเรียนถัดไป: [บทเรียน 3.1 — จากตัวเลขดิบสู่ปริมาณทางฟิสิกส์: มุมเอียง พลังงาน ความสูง และ dBFS](../../m03-processing/l01-physics-quantities/README.md)

## สะท้อนคิด

- jitter ที่คุณวัดได้มากที่สุดเกิดตอนไหน และคุณคิดว่ามาจากงานส่วนใดในลูป
- ถ้าต้องเพิ่มเซนเซอร์ตัวที่สาม (เช่นความดัน) ลงไฟล์เดียวกัน คุณต้องแก้ส่วนไหนบ้าง
