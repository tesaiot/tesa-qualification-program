---
id: edgeai-dev.m05.l02
lang: th
title: {th: 'ลงมือทำ: เก็บ dataset ที่สมดุลบนบอร์ดแล้วแบ่งบน PC', en: 'Hands-on: capture a balanced dataset on the board, split it on the PC'}
summary: {th: เติมสี่จุดใน s11_dataset.py ให้อ่าน IMU เขียน CSV นับจำนวนต่อคลาส และนำทางให้เก็บคลาสที่ยังน้อย จนได้ /gestures.csv สามคลาสที่สมดุลจากบอร์ด แล้วคัดลอกมาแบ่ง train/val/test บน PC พร้อมพิสูจน์ด้วย np.bincount ว่าทุกกองครบทุกคลาส, en: 'Fill four points in s11_dataset.py to read the IMU, write the CSV, count per class and steer you to the class that is short, until the board gives a balanced three-class /gestures.csv; then copy it to the PC, split it into train/val/test and prove with np.bincount that every set holds every class.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m05.l01]
objectives:
  - {th: เติมสี่จุดใน practice/s11_dataset.py จนกดปุ่ม label แล้ว /gestures.csv ได้ 200 บรรทัดใหม่ที่ค่าไม่เป็นศูนย์ แถบสมดุลขยับ และคำใบ้ชี้คลาสที่มีน้อยที่สุด, en: 'Fill the four points in practice/s11_dataset.py so each label press adds 200 non-zero lines to /gestures.csv, the balance bars move and the hint names the class with the fewest samples.'}
  - {th: เก็บ dataset จากบอร์ดให้ครบสามคลาสถึงเป้า แล้วบน PC รัน load_csv → make_windows → split → normalize ตามลำดับ และแสดง np.bincount ของทั้งสามกองที่มีครบทุกคลาส, en: 'Capture a dataset on the board with all three classes at target, then on the PC run load_csv → make_windows → split → normalize in that order and show an np.bincount for all three sets with every class present.'}
  - {th: ทดลองเก็บให้ไม่สมดุลโดยตั้งใจ แล้วอธิบายจากตัวเลขได้ว่าทำไม split แบบ stratified พาความไม่สมดุลไปทุกกอง และต้องแก้ตอนเก็บ, en: Capture an unbalanced dataset on purpose and use the numbers to explain why a stratified split carries the imbalance into every set and must be fixed at capture time.}
develops: [{skill: ai.data-collection, to: 3}, {skill: lang.micropython, to: 2}, {skill: lang.python, to: 2}]
assesses: [{skill: ai.data-collection, level: 2, evidence: practice/s11_dataset.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 5.2 — ลงมือทำ: เก็บ dataset ที่สมดุลบนบอร์ดแล้วแบ่งบน PC

> โมดูล 5 — ฝึกโมเดลและนำไปใช้หลายเป้าหมาย · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เติมสี่จุดใน s11_dataset.py ให้อ่าน IMU เขียน CSV นับจำนวนต่อคลาส และนำทางให้เก็บคลาสที่ยังน้อย จนได้ /gestures.csv สามคลาสที่สมดุลจากบอร์ด แล้วคัดลอกมาแบ่ง train/val/test บน PC พร้อมพิสูจน์ด้วย np.bincount ว่าทุกกองครบทุกคลาส

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เติมสี่จุดใน practice/s11_dataset.py จนกดปุ่ม label แล้ว /gestures.csv ได้ 200 บรรทัดใหม่ที่ค่าไม่เป็นศูนย์ แถบสมดุลขยับ และคำใบ้ชี้คลาสที่มีน้อยที่สุด
2. เก็บ dataset จากบอร์ดให้ครบสามคลาสถึงเป้า แล้วบน PC รัน load_csv → make_windows → split → normalize ตามลำดับ และแสดง np.bincount ของทั้งสามกองที่มีครบทุกคลาส
3. ทดลองเก็บให้ไม่สมดุลโดยตั้งใจ แล้วอธิบายจากตัวเลขได้ว่าทำไม split แบบ stratified พาความไม่สมดุลไปทุกกอง และต้องแก้ตอนเก็บ

## ก่อนเริ่ม

ผ่านบทเรียน 5.1 มาแล้ว เข้าใจ class balance, stratified split และกฎ no leakage
เตรียม PC ที่มี Python 3 กับ numpy และ [`dataset_tools.py`](../../shared/training/dataset_tools.py) และถ้าจะเก็บข้อมูลจริงต้องมีบอร์ด

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — Emulator จำลอง IMU ให้ซ้อมเติมโค้ดและกดปุ่ม label ได้ แต่ dataset ที่จะเอาไปฝึกโมเดลจริงต้องเก็บจาก IMU ของบอร์ด
- **เรียนมาก่อน:** [บทเรียน 5.1 — วิศวกรรมชุดข้อมูล: สมดุลคลาส หน้าต่าง และการแบ่ง train/val/test](../l01-dataset-engineering/README.md)

## แนวคิด

ทั้งไฟล์อ่านเป็นประโยคเดียว: เลือกป้าย → อ่าน IMU เป็นชุด → เขียนลง CSV → นับต่อคลาส → บอกว่าคลาสไหนยังน้อย → ครบเป้าทุกคลาสคือ dataset พร้อม
โครงยังเป็นสี่จังหวะเดิม (import → สร้างครั้งเดียว → ลูป → `ui.poll`) สิ่งใหม่อยู่ใน `record()` สองจุดแรกยกมาจาก DAQ logger:
(1) `ax, ay, az, gx, gy, gz = sensors.bmi270.motion()` ได้ accel หน่วย m/s² (`az` ราว 9.81 ตอนวางนิ่ง) กับ gyro หน่วย deg/s
(2) `f.write("%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n" % (label, ax, ay, az, gx, gy, gz))` ลำดับคอลัมน์ต้องตรง `CHANNELS` และป้ายต้องสะกดตรง `CLASSES`
เพราะ `load_csv()` ใช้ `CLASSES.index(label)` สะกด `Idle` ตัวใหญ่ก็ error แล้ว

สองจุดหลังคือสมองของ dataset engineering: (3) `counts[label] += BURST` หลังเขียนครบชุด แถบสมดุลจึงขยับ และ
(4) `fewest = min(counts, key=counts.get)` ที่วนคีย์ทั้งหมดแล้วคืน **ชื่อคลาส** ที่ค่าน้อยสุด โปรแกรมจึงบอกได้ว่าควรเก็บอะไรต่อ
เก็บที่ 20 ms ต่อครั้ง (50 Hz) ให้ตรงกับโมเดล Motion ถ้าอัตราต่าง ท่าเดียวกันจะยืดหรือหดในหน้าต่าง

เก็บครบแล้วคัดลอก `/gestures.csv` ออกจากบอร์ด (BENTO IDE file transfer หรือ `mpremote`) ไปไว้ที่ `data/gestures.csv` บน PC
แล้วเรียก `load_csv` → `make_windows` → `split` → `normalize(Xtr, Xva, Xte)` **split ก่อน normalize เสมอ** ปิดด้วยรายงาน `np.bincount`
ของทั้งสามกอง ถ้ากองใดขาดคลาส เช่น test เป็น `[20 20 0]` แปลว่าเก็บ `shaking` น้อยเกินไป ต้องกลับไปเก็บเพิ่มบนบอร์ด

## ตัวอย่างสมบูรณ์

`s11_dataset_full.py` เพิ่มการเตือนสีแดงเมื่อคลาสน้อยสุดต่ำกว่า 70% ของคลาสมากสุด (`BALANCE_TOL = 0.30`) แสดงอัตราสมดุล min/max
ประเมินจำนวนหน้าต่างด้วยสูตรเดียวกับ `make_windows()` และมีปุ่มล้างไฟล์ ข้อควรรู้: ตัวนับเริ่มที่ศูนย์ทุกครั้งที่รัน แม้ไฟล์เดิมจะมีข้อมูลอยู่แล้ว

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/s11_dataset_full.py](examples/s11_dataset_full.py) | เก็บ dataset IMU ที่สมดุลและพร้อม train ลง CSV (ฉบับเต็ม) |

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นหรือใน `shared/` ด้วย:

- [shared/training/dataset_tools.py](../../shared/training/dataset_tools.py) — Dataset tools for the IMU gesture classifier (Pillar 4 / Training).
- [shared/training/train.py](../../shared/training/train.py) — Train a tiny IMU gesture classifier and export it as int8 TFLite.

## ฝึกเติม

คอมเมนต์ `# เติม:` อยู่ที่บรรทัด 67 (หา `fewest`), 84 (อ่าน `motion()`), 88 (`f.write`) และ 93 (`counts[label] += BURST`)
ถ้า CSV เป็น 0.0 หมด จุดที่ 84 ยังว่าง ถ้าแถบไม่ขยับ จุดที่ 93 ยังว่าง ถ้าคำใบ้ชี้ `idle` ตลอด จุดที่ 67 ยังว่าง

| ไฟล์ฝึก | เรื่อง |
|---|---|
| [practice/s11_dataset.py](practice/s11_dataset.py) | เก็บ dataset IMU ที่ "สมดุลและพร้อม train" ลง CSV (ฉบับฝึกเติมโค้ด) |

## เฉลย

เปิดเฉลยหลังจากลองเองแล้วอย่างน้อยหนึ่งรอบ และอ่าน [วิธีใช้เฉลย](../../README.md#วิธีใช้เฉลย) ก่อน

| เฉลย | คู่กับ |
|---|---|
| [solution/s11_dataset.py](solution/s11_dataset.py) | [practice/s11_dataset.py](practice/s11_dataset.py) |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. กดปุ่ม label แล้วแถบสมดุลไม่ขยับเลย แต่ไฟล์มีบรรทัดเพิ่ม จุดใดยังว่าง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
   - ข) f.write(...)
   - ค) counts[label] += BURST
   - ง) fewest = min(counts, key=counts.get)

   <details><summary>เฉลย</summary>

   **ค** — แถบอ่านค่าจาก counts ถ้าไม่บวก BURST เข้าตัวนับ ไฟล์จะโตแต่โปรแกรมไม่รู้ว่าเก็บไปเท่าไร เป็นการเก็บแบบตาบอด

   </details>

2. counts = {'idle': 600, 'circle': 200, 'shaking': 400} ค่า min(counts, key=counts.get) คืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) 200
   - ข) 'circle'
   - ค) 'idle'
   - ง) ('circle', 200)

   <details><summary>เฉลย</summary>

   **ข** — min วนคีย์ของ dict แต่เทียบด้วย counts.get จึงคืนชื่อคลาสที่ค่าน้อยสุด ไม่ใช่ตัวเลข คำใบ้จึงบอกให้เก็บ circle เพิ่ม

   </details>

3. เรียงขั้นบน PC ให้ไม่มีข้อมูลรั่ว *(เรียงลำดับ · เป้าหมายข้อ 2)*
   - ก) split(X, y)
   - ข) load_csv("data/gestures.csv")
   - ค) normalize(Xtr, Xva, Xte)
   - ง) make_windows(s, l)

   <details><summary>เฉลย</summary>

   **ข → ง → ก → ค** — อ่านไฟล์ → ตัดหน้าต่าง → แบ่งกอง → normalize ด้วยสถิติของ train ถ้า normalize ก่อน split สถิติของ test จะรั่วเข้าไป

   </details>

4. เก็บ idle มากกว่าคลาสอื่นสามเท่าแล้ว split แบบ stratified ผลคืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) split ปรับให้ทุกกองสมดุลเอง
   - ข) ทุกกองได้ idle มากกว่าคลาสอื่นราวสามเท่าเหมือนกัน ความไม่สมดุลติดไปทุกกอง
   - ค) test ไม่มี idle เลย
   - ง) โปรแกรม error

   <details><summary>เฉลย</summary>

   **ข** — stratified รักษาสัดส่วนเดิมของแต่ละคลาสในทุกกอง จึงไม่แก้ความไม่สมดุล ต้องแก้ที่ตอนเก็บ

   </details>

## แล็บ

**MVP ของชุดบทเรียน 5.1–5.2:** dataset จากบอร์ดที่สะอาด สมดุล และแบ่งแล้ว ทุกกอง (train/val/test) มีครบสามคลาสในสัดส่วนใกล้เคียงกัน

- [ ] เติมไฟล์ฝึกครบสี่จุด ลองบน Emulator ก่อน แล้วเก็บของจริงบนบอร์ดจนทั้งสามคลาสถึง `TARGET`
- [ ] คัดลอก `gestures.csv` มา PC แล้วรัน split พิมพ์ `np.bincount` ของทั้งสามกองลงบันทึกการเรียน
- [ ] เก็บอีกไฟล์ที่ `idle` มากกว่าคลาสอื่นสามเท่าโดยตั้งใจ แล้วเทียบสัดส่วนในสามกอง อธิบายว่าทำไมความไม่สมดุลไม่หายไปเอง
- [ ] อธิบายได้ว่าทำไมต้อง balance ทำไมต้องสามกอง และทำไม normalize ต้อง fit บน train เท่านั้น

## ไปต่อ

ชุดบทเรียนถัดไป (บทเรียน 5.3–5.5) เราจะเอา dataset นี้ไปฝึกเป็นโมเดลจริงด้วย TensorFlow ใน Docker แล้วส่งออกเป็น `.tflite` แบบ int8

บทเรียนถัดไป: [บทเรียน 5.3 — ฝึกโมเดลใน Docker: หนึ่งชิ้นงาน สี่เป้าหมาย](../l03-training-pipeline/README.md)

## สะท้อนคิด

- dataset ของคุณมีหน้าต่างรวมกี่หน้าต่าง คุณคิดว่าพอสำหรับโมเดลเล็ก ๆ หรือไม่ และจะรู้ได้อย่างไร
- ถ้าต้องเพิ่มคลาสที่สี่ เช่น `tap` คุณต้องแก้ไฟล์ใดบ้างทั้งฝั่งบอร์ดและฝั่ง PC
