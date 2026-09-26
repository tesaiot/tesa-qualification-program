---
id: edgeai-dev.m05.l01
lang: th
title: {th: 'วิศวกรรมชุดข้อมูล: สมดุลคลาส หน้าต่าง และการแบ่ง train/val/test', en: 'Dataset engineering: class balance, windows and the train/val/test split'}
summary: {th: 'เริ่มสร้างโมเดลของเราเองจากสิ่งที่มาก่อนการฝึกเสมอ คือ dataset รู้จักท่อเตรียมข้อมูลสี่ขั้น capture, label, window, split เหตุผลของ class balance การแบ่ง train/val/test แบบ stratified และกฎเหล็กห้ามข้อมูลรั่ว (no leakage) โดยรันท่อทั้งเส้นด้วยข้อมูลสังเคราะห์ก่อน', en: 'Start building your own model from what always comes before training - the dataset. Learn the four-step preparation pipeline (capture, label, window, split), why class balance matters, the stratified train/val/test split and the no-leakage rule, running the whole pipeline on synthetic data first.'}
level: L3
time_min: {concept: 45, practise: 10, check: 10}
hardware: {emulator: false, boards: [none]}
prerequisites: [edgeai-dev.m04.l06]
objectives:
  - {th: เรียงท่อเตรียมข้อมูลสี่ขั้น capture → label → window → split ได้ และบอกได้ว่าขั้นใดทำบนบอร์ด ขั้นใดทำบน PC, en: Order the four-step preparation pipeline (capture → label → window → split) and say which steps run on the board and which on the PC.}
  - {th: คำนวณสัดส่วนคลาส p_c = n_c / N และอธิบายด้วยตัวอย่างได้ว่าทำไม dataset ที่ไม่สมดุลให้ความแม่นบนกระดาษที่หลอกตา, en: Compute the class share p_c = n_c / N and use an example to explain why an unbalanced dataset gives a misleading accuracy on paper.}
  - {th: 'คำนวณจำนวนหน้าต่างของแต่ละคลาสในกอง train, val และ test แบบ stratified ด้วย ⌊0.15·n_c⌋ และบอกหน้าที่ของแต่ละกอง', en: 'Compute the per-class window counts of a stratified train, val and test split with ⌊0.15·n_c⌋, and state the job of each set.'}
  - {th: ระบุได้ว่า normalize แบบใดทำให้ข้อมูลรั่ว และแก้ด้วยกฎ fit บน train แล้ว apply ทุกกอง, en: 'Identify which normalisation leaks data and fix it with the rule "fit on train, apply to every set".'}
develops: [{skill: ai.data-collection, to: 3}, {skill: ai.model-training, to: 1}, {skill: hw.math, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 5.1 — วิศวกรรมชุดข้อมูล: สมดุลคลาส หน้าต่าง และการแบ่ง train/val/test

> โมดูล 5 — ฝึกโมเดลและนำไปใช้หลายเป้าหมาย · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เริ่มสร้างโมเดลของเราเองจากสิ่งที่มาก่อนการฝึกเสมอ คือ dataset รู้จักท่อเตรียมข้อมูลสี่ขั้น capture, label, window, split เหตุผลของ class balance การแบ่ง train/val/test แบบ stratified และกฎเหล็กห้ามข้อมูลรั่ว (no leakage) โดยรันท่อทั้งเส้นด้วยข้อมูลสังเคราะห์ก่อน

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เรียงท่อเตรียมข้อมูลสี่ขั้น capture → label → window → split ได้ และบอกได้ว่าขั้นใดทำบนบอร์ด ขั้นใดทำบน PC
2. คำนวณสัดส่วนคลาส p_c = n_c / N และอธิบายด้วยตัวอย่างได้ว่าทำไม dataset ที่ไม่สมดุลให้ความแม่นบนกระดาษที่หลอกตา
3. คำนวณจำนวนหน้าต่างของแต่ละคลาสในกอง train, val และ test แบบ stratified ด้วย ⌊0.15·n_c⌋ และบอกหน้าที่ของแต่ละกอง
4. ระบุได้ว่า normalize แบบใดทำให้ข้อมูลรั่ว และแก้ด้วยกฎ fit บน train แล้ว apply ทุกกอง

## ก่อนเริ่ม

ผ่านโมดูล 4 มาแล้ว เข้าใจหน้าต่างเลื่อน WIN กับ HOP จากบทเรียน 4.5 และเคยเก็บ CSV ด้วย DAQ logger ในบทเรียน 2.2
เตรียม PC ที่มี Python 3 กับ numpy แล้วดาวน์โหลด [`dataset_tools.py`](../../shared/training/dataset_tools.py) ไว้

- **อุปกรณ์:** คอมพิวเตอร์ของคุณ ไม่ต้องใช้บอร์ด — ใช้ PC ที่มี Python 3 และ numpy บอร์ดหรือ Emulator ใช้ในบทเรียน 5.2
- **เรียนมาก่อน:** [บทเรียน 4.6 — ลงมือทำ: feature vector จากหน้าต่างเลื่อน](../../m04-analysis/l06-windowing-lab/README.md)

## ดูของจริงก่อน

รันท่อทั้งเส้นก่อนเข้าใจ: `python dataset_tools.py --synthesize --out data/gestures.csv` แล้ว `python dataset_tools.py --out data/gestures.csv`
จะได้ `samples (3600, 6) windows (143, 50, 6) class counts [48 48 47]` ถามตัวเองว่าตัวเลขสามตัวสุดท้ายบอกอะไร

## แนวคิด

**dataset** ของเราคือ CSV ธรรมดา หนึ่งบรรทัดต่อหนึ่ง sample ขึ้นต้นด้วย **label** ตามด้วยหกค่า `ax,ay,az,gx,gy,gz` จาก `sensors.bmi270.motion()`
label คือเฉลยที่มนุษย์ติดให้ เราใช้สามคลาสเดียวกับโมเดล Motion บนบอร์ด (`idle`, `circle`, `shaking`) เพื่อเทียบโมเดลของเรากับของสำเร็จได้ภายหลัง
CSV ดิบยังฝึกไม่ได้ ต้องผ่านสี่ขั้น: **capture** และ **label** บนบอร์ดด้วย MicroPython แล้ว **window** และ **split** บน PC ด้วย `dataset_tools.py`
ซึ่งมีห้าฟังก์ชัน `load_csv`, `make_windows`, `normalize`, `split` และ `synthesize` ข้อมูลสังเคราะห์ให้ท่อรันได้ก่อนมีข้อมูลจริง

**class balance:** ถ้า 95% ของข้อมูลเป็น `idle` โมเดลที่ตอบ `idle` ตลอดจะแม่น 95% บนกระดาษแต่ใช้งานไม่ได้ เราวัดด้วย $p_c = n_c/N$
และสมดุลเมื่อ $p_c \approx 1/K$ (สามคลาสคือราว 0.33) ทางแก้ที่ตรงที่สุดคือเก็บให้สมดุลตั้งแต่ตอนเก็บ **windowing** ใช้ `WIN = 50` (หนึ่งวินาทีที่ 50 Hz)
และ `HOP = 25` ป้ายของหน้าต่างคือป้ายส่วนใหญ่ในนั้น และต้องตัดแบบเดียวกับที่บอร์ดป้อนโมเดลตอนใช้งาน

**train / val / test:** train ให้โมเดลเรียน val ใช้เช็กระหว่างฝึกและจูน test สอบครั้งเดียวตอนจบ `split()` แบ่งแบบ **stratified**
คือแยกทีละคลาส สลับลำดับด้วย `rng.permutation` แล้วหั่น $n_{c,test} = \lfloor 0.15\,n_c \rfloor$, $n_{c,val} = \lfloor 0.15\,n_c \rfloor$ ที่เหลือเป็น train
ทุกกองจึงมีครบทุกคลาสในสัดส่วนเดิม ข้อมูลสังเคราะห์ 143 หน้าต่างแบ่งได้ train `[34 34 33]` val `[7 7 7]` test `[7 7 7]`
สุดท้ายคือ **no leakage:** `normalize()` คิด mean/std จาก train เท่านั้นแล้วใช้กับทุกกอง ถ้าคิดจากข้อมูลทั้งหมด test จะรั่วเข้า train
ตัวเลขความแม่นจะสวยเกินจริงโดยไม่มี error ใด ๆ เตือน

## ตัวอย่างสมบูรณ์

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นหรือใน `shared/` ด้วย:

- [m02-daq/l02-daq-logger-lab/examples/s04_daq_logger.py](../../m02-daq/l02-daq-logger-lab/examples/s04_daq_logger.py) — เก็บข้อมูล sensor ลงไฟล์ CSV (Data Acquisition)
- [m02-daq/l02-daq-logger-lab/practice/s04_daq_logger.py](../../m02-daq/l02-daq-logger-lab/practice/s04_daq_logger.py) — เก็บข้อมูล sensor ลงไฟล์ CSV (Data Acquisition) (ฉบับฝึกเติมโค้ด)
- [m05-training/l02-dataset-lab/practice/s11_dataset.py](../l02-dataset-lab/practice/s11_dataset.py) — เก็บ dataset IMU ที่ "สมดุลและพร้อม train" ลง CSV (ฉบับฝึกเติมโค้ด)
- [shared/training/dataset_tools.py](../../shared/training/dataset_tools.py) — Dataset tools for the IMU gesture classifier (Pillar 4 / Training).

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. เรียงท่อเตรียมข้อมูลจากเซนเซอร์จนพร้อมฝึก *(เรียงลำดับ · เป้าหมายข้อ 1)*
   - ก) window: ตัดเป็นหน้าต่าง 50 sample (บน PC)
   - ข) capture: อ่าน IMU ที่ 50 Hz (บนบอร์ด)
   - ค) split: แบ่ง train/val/test (บน PC)
   - ง) label: ติดป้ายท่าที่ทำ (บนบอร์ด)

   <details><summary>เฉลย</summary>

   **ข → ง → ก → ค** — capture กับ label เกิดบนบอร์ดขณะเก็บ ส่วน window กับ split ทำบน PC ด้วย dataset_tools.py แล้วจึงส่งต่อให้การฝึก

   </details>

2. dataset มี idle 950 หน้าต่าง circle 30 และ shaking 20 โมเดลที่ตอบ idle ทุกครั้งได้ความแม่นเท่าไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) 33%
   - ข) 50%
   - ค) 95% ทั้งที่ไม่ได้เรียนอะไรเลย
   - ง) 100%

   <details><summary>เฉลย</summary>

   **ค** — p_idle = 950/1000 = 0.95 ความแม่นบนกระดาษจึงสูงแต่หลอกตา สมดุลควรให้ทุกคลาสได้ราว 1/3

   </details>

3. คลาส shaking มี 40 หน้าต่าง split แบบ stratified (val = test = 0.15) ได้ train, val, test กี่หน้าต่าง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) 28, 6, 6
   - ข) 30, 5, 5
   - ค) 26, 7, 7
   - ง) 40, 0, 0

   <details><summary>เฉลย</summary>

   **ก** — ⌊0.15 × 40⌋ = 6 ไป test และ 6 ไป val ที่เหลือ 40 − 12 = 28 เป็น train train จึงรับเศษที่เหลือเสมอ

   </details>

4. ทำไมต้องมี val แยกจาก test *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) เพื่อให้ train มีข้อมูลน้อยลง
   - ข) เราดู val ซ้ำ ๆ ตอนจูน val จึงปนการตัดสินใจของเราไปแล้ว test ที่ไม่เคยแตะเท่านั้นที่บอกความแม่นจริง
   - ค) val กับ test ต่างกันแค่ชื่อ
   - ง) เพราะ test ต้องใหญ่กว่า train

   <details><summary>เฉลย</summary>

   **ข** — val ใช้ระหว่างฝึกจึงเริ่มเอนตามการจูน test เก็บไว้สอบครั้งเดียวตอนจบ ถ้าแอบดู test ระหว่างจูน ตัวเลขจะโกหก

   </details>

5. โค้ดแบบใดทำให้ข้อมูลรั่ว *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) split ก่อน แล้ว normalize(Xtr, Xva, Xte) ที่คิด mean/std จาก Xtr
   - ข) normalize X ทั้งก้อนด้วย mean/std ของข้อมูลทั้งหมด แล้วค่อย split
   - ค) ใช้ rng.permutation ก่อนหั่นแต่ละคลาส
   - ง) ตั้ง seed ของ split ให้คงที่

   <details><summary>เฉลย</summary>

   **ข** — mean/std ที่คิดรวม test ทำให้สถิติของ test เข้าไปอยู่ในข้อมูลที่ใช้ฝึก ต้อง fit บน train แล้ว apply ทุกกอง

   </details>

## แล็บ

- [ ] รัน `dataset_tools.py` แบบ `--synthesize` แล้วแบบอ่านไฟล์ จดจำนวน samples, windows และ class counts ลงบันทึกการเรียน
- [ ] ใน Python เรียก `split()` กับหน้าต่างที่ได้ แล้วพิมพ์ `np.bincount` ของทั้งสามกอง ตรวจว่าตรงกับการคำนวณด้วยมือ
- [ ] เขียนสองบรรทัดว่าถ้าเรียก `normalize()` ก่อน `split()` จะรั่วตรงไหน

## ไปต่อ

บทเรียน 5.2 เราจะเติม `s11_dataset.py` เก็บ dataset จริงบนบอร์ดโดยเฝ้าแถบสมดุล แล้วแบ่งบน PC

บทเรียนถัดไป: [บทเรียน 5.2 — ลงมือทำ: เก็บ dataset ที่สมดุลบนบอร์ดแล้วแบ่งบน PC](../l02-dataset-lab/README.md)

## สะท้อนคิด

- ถ้าเก็บท่าเดินจากหลายคน ทำไมควรแบ่ง train/test ตาม "คน" แทนตาม sample
- คลาสที่หายากในงานจริง เช่นเสียงเครื่องจักรเสีย คุณจะเก็บให้สมดุลได้อย่างไร
