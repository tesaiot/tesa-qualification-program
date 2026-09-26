---
id: edgeai-dev.m04.l05
lang: th
title: {th: 'feature และหน้าต่าง: สิ่งที่โมเดลเห็นจริง', en: 'Features and windowing: what the model actually sees'}
summary: {th: เข้าใจสิ่งที่โมเดลเห็นจริง โมเดลไม่กิน sample ดิบทีละจุดแต่กินหน้าต่างที่ถูกบีบเป็น feature vector เรียนเรื่องหน้าต่างเลื่อนกับ hop ทำไมต้องซ้อน ฟีเจอร์เชิงสถิติ mean std และพลังงานต่อย่าน และโยงไปสู่ log-mel spectrogram ของโมเดลเสียง, en: 'Learn what the model actually sees - not raw samples one by one but windows squeezed into a feature vector; sliding windows and hop, why they overlap, statistical features (mean, std, band energy), and the link to the log-mel spectrogram used by audio models.'}
level: L3
time_min: {concept: 45, practise: 10, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m04.l04]
objectives:
  - {th: 'อธิบายได้ว่าทำไมโมเดลต้องดูหน้าต่างของสัญญาณแทน sample เดี่ยว และคำนวณจำนวนหน้าต่างต่อวินาทีจาก WIN, HOP และอัตราสุ่ม', en: 'Explain why a model must look at a window of signal rather than single samples, and compute windows per second from WIN, HOP and the sample rate.'}
  - {th: บอกข้อแลกเปลี่ยนของการซ้อนหน้าต่าง (hop เล็กกับใหญ่) และเหตุผลที่หน้าต่างซ้อนกันไม่พลาดเหตุการณ์สั้น, en: State the trade-off of window overlap (small versus large hop) and why overlapping windows do not miss short events.}
  - {th: คำนวณ mean และ std ของหน้าต่างเล็ก ๆ ด้วยมือ และอธิบายว่า std แยกนิ่งกับขยับได้อย่างไร ส่วน mean บอกท่าทางคงที่, en: 'Compute the mean and std of a small window by hand, and explain how std separates still from moving while mean tells the steady posture.'}
  - {th: อธิบายสายพาน log-mel = log(Mel(|FFT(x·w)|)) และเหตุผลที่ front-end ตอนฝึกกับตอนใช้งานต้องตรงกัน, en: Explain the log-mel pipeline log(Mel(|FFT(x·w)|)) and why the front-end must match between training and deployment.}
develops: [{skill: sys.dsp, to: 3}, {skill: ai.data-collection, to: 2}, {skill: hw.math, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 4.5 — feature และหน้าต่าง: สิ่งที่โมเดลเห็นจริง

> โมดูล 4 — วิเคราะห์สัญญาณ · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เข้าใจสิ่งที่โมเดลเห็นจริง โมเดลไม่กิน sample ดิบทีละจุดแต่กินหน้าต่างที่ถูกบีบเป็น feature vector เรียนเรื่องหน้าต่างเลื่อนกับ hop ทำไมต้องซ้อน ฟีเจอร์เชิงสถิติ mean std และพลังงานต่อย่าน และโยงไปสู่ log-mel spectrogram ของโมเดลเสียง

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. อธิบายได้ว่าทำไมโมเดลต้องดูหน้าต่างของสัญญาณแทน sample เดี่ยว และคำนวณจำนวนหน้าต่างต่อวินาทีจาก WIN, HOP และอัตราสุ่ม
2. บอกข้อแลกเปลี่ยนของการซ้อนหน้าต่าง (hop เล็กกับใหญ่) และเหตุผลที่หน้าต่างซ้อนกันไม่พลาดเหตุการณ์สั้น
3. คำนวณ mean และ std ของหน้าต่างเล็ก ๆ ด้วยมือ และอธิบายว่า std แยกนิ่งกับขยับได้อย่างไร ส่วน mean บอกท่าทางคงที่
4. อธิบายสายพาน log-mel = log(Mel(|FFT(x·w)|)) และเหตุผลที่ front-end ตอนฝึกกับตอนใช้งานต้องตรงกัน

## ก่อนเริ่ม

ผ่านชุดบทเรียน 4.3–4.4 มาแล้ว เข้าใจ FFT, Hann window และ magnitude
เปิดตัวอย่าง `s10_windowing.py` ไว้ใน BENTO IDE

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/)
- **เรียนมาก่อน:** [บทเรียน 4.4 — ลงมือทำ: สเปกตรัมสดจาก IMU](../l04-fft-spectrum-lab/README.md)

## ดูของจริงก่อน

รัน `s10_windowing.py` ก่อนเลย วางบอร์ดนิ่งสลับกับเขย่าเบา ๆ แล้วดูแท่ง mean, std และ band0..3 ขยับ
นั่นคือ feature vector ที่กำลังไหลเข้าโมเดล สัญญาณดิบก้อนหนึ่งกลายเป็นตัวเลขไม่กี่ตัว

## แนวคิด

เสียงไอหนึ่งครั้งหรือท่าเขย่าหนึ่งทีไม่ใช่ค่า ณ จุดเดียว แต่เป็น **รูปร่างของสัญญาณช่วงเวลาหนึ่ง** โมเดลจึงกิน **หน้าต่าง** (window)
เช่น `WIN = 50` จุดหรือหนึ่งวินาทีที่ 50 Hz หน้าต่างเลื่อนทีละ `HOP = 25` จุด จึงซ้อนกัน 50% และได้ feature ชุดใหม่ทุก 25 จุด
(สองครั้งต่อวินาที) การซ้อนทำให้ตอบไวขึ้นและไม่พลาดเหตุการณ์สั้นที่ตกร่องระหว่างหน้าต่าง แลกกับการคำนวณบ่อยขึ้น
ขนาดหน้าต่างไม่ได้ตั้งมั่ว โมเดลฝึกมาด้วยหน้าต่างขนาดไหน ตอนใช้งานก็ต้องป้อนขนาดเดียวกัน

หน้าต่าง 50 จุดถูกบีบเป็น **feature vector** หกตัว `[mean, std, band0, band1, band2, band3]` `mean` บอกระดับ DC หรือทิศของแรงโน้มถ่วงบนแกนนั้น
(ท่าทางคงที่) `std` = $\sqrt{\frac{1}{n}\sum (x_i - \bar{x})^2}$ บอกความแรงของการสั่น วางนิ่งต่ำ เขย่าสูง `band0..3` แบ่งหน้าต่างเป็นสี่ช่วง
**เวลา** แล้ววัด variance แต่ละช่วง จับได้ว่าการสั่นกระจุกอยู่ต้น กลาง หรือท้ายหน้าต่าง feature ดีแค่ไหน โมเดลก็เล็กและแม่นได้แค่นั้น

โมเดลเสียงบนบอร์ดใช้โครงเดียวกันแต่แบ่งย่านตาม **ความถี่**: ตัดหน้าต่าง → คูณ Hann → FFT → เอาขนาด → รวมเป็นย่าน mel ตามการได้ยินของหู
(ความถี่ต่ำละเอียด สูงหยาบ) → log บีบ dynamic range เขียนเป็นสูตรเดียวได้ว่า $\text{logmel} = \log(\mathrm{Mel}(|\mathrm{FFT}(x \cdot w)|))$
ข้อสรุปที่สำคัญที่สุดคือ **โมเดลไม่เคยเห็นสัญญาณดิบ** มันเห็นแต่ feature vector ที่ front-end บีบมาให้ ตอนฝึก dataset คือชุดของ feature vector
พร้อม label ตอนใช้งานบอร์ดบีบสัญญาณสดแบบเดียวกัน ถ้า front-end สองฝั่งไม่ตรงกัน โมเดลจะเพี้ยนทันที ซึ่งเป็นบั๊กคลาสสิกของ Edge AI

## ตัวอย่างสมบูรณ์

`s10_windowing.py` คือฉบับอ้างอิงที่ใช้ `WIN = 50` และ `HOP = 25` ลองทาย (Predict) ก่อนรันว่าแท่งใดจะสูงขึ้นมากที่สุดเมื่อเขย่า
แล้วลองหมุนบอร์ดช้า ๆ เทียบ จะเห็นว่า mean เปลี่ยนแต่ std ยังต่ำ

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/s10_windowing.py](examples/s10_windowing.py) | โมเดล "เห็น" อะไร: windowing + feature vector |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. WIN = 50, HOP = 25 ที่อัตราสุ่ม 50 Hz ได้ feature vector ใหม่กี่ชุดต่อวินาที *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) 1 ชุด
   - ข) 2 ชุด
   - ค) 25 ชุด
   - ง) 50 ชุด

   <details><summary>เฉลย</summary>

   **ข** — ได้ชุดใหม่ทุก HOP = 25 จุด ที่ 50 จุดต่อวินาทีจึงเป็น 2 ชุดต่อวินาที แต่ละชุดครอบคลุม 1 วินาทีและซ้อนกัน 50%

   </details>

2. ตั้ง HOP = WIN (ไม่ซ้อน) ความเสี่ยงหลักคืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) หน่วยความจำเต็ม
   - ข) เหตุการณ์สั้นที่คร่อมรอยต่อระหว่างสองหน้าต่างอาจถูกแบ่งครึ่งจนโมเดลพลาด และได้ผลช้าลง
   - ค) std กลายเป็นลบ
   - ง) อัตราสุ่มเปลี่ยน

   <details><summary>เฉลย</summary>

   **ข** — การซ้อนทำให้ทุกจุดถูกครอบด้วยหน้าต่างมากกว่าหนึ่งอัน และได้ผลบ่อยขึ้น ไม่ซ้อนประหยัดแรงแต่ตอบช้าและพลาดง่าย

   </details>

3. หน้าต่าง [7.8, 11.8, 7.8, 11.8] มี mean และ std เท่าไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) mean 9.8, std 0
   - ข) mean 9.8, std 2.0
   - ค) mean 4.0, std 9.8
   - ง) mean 11.8, std 4.0

   <details><summary>เฉลย</summary>

   **ข** — ค่าเฉลี่ย 9.8 ทุกจุดห่างจากค่าเฉลี่ย 2.0 std จึงเป็น 2.0 เทียบกับหน้าต่างนิ่ง [9.8, 9.8, 9.8, 9.8] ที่ std = 0 แม้ mean เท่ากัน

   </details>

4. หมุนบอร์ดช้า ๆ จากราบเป็นตั้ง feature ใดเปลี่ยนมากที่สุด *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) mean เพราะทิศของแรงโน้มถ่วงบนแกน Z เปลี่ยน ส่วน std ยังต่ำเพราะไม่มีการสั่น
   - ข) std เพราะบอร์ดเคลื่อนที่
   - ค) band3 เท่านั้น
   - ง) ไม่มี feature ใดเปลี่ยน

   <details><summary>เฉลย</summary>

   **ก** — mean บอกท่าทางคงที่ std บอกการสั่น การหมุนช้า ๆ เปลี่ยนระดับเฉลี่ยของ az แต่แทบไม่ทำให้ค่าแกว่ง

   </details>

5. เรียงสายพานสร้าง log-mel spectrogram จากสัญญาณเสียงหนึ่งหน้าต่าง *(เรียงลำดับ · เป้าหมายข้อ 4)*
   - ก) FFT
   - ข) คูณ Hann window (x · w)
   - ค) log
   - ง) เอาขนาด |·|
   - จ) รวมเป็นย่าน Mel

   <details><summary>เฉลย</summary>

   **ข → ก → ง → จ → ค** — x·w → FFT → |·| → Mel → log ถ้าตอนฝึกกับตอนใช้บนบอร์ดทำขั้นเหล่านี้ไม่ตรงกัน ผลของโมเดลจะเพี้ยน

   </details>

## แล็บ

- [ ] คำนวณจำนวนหน้าต่างต่อวินาทีเมื่อ WIN = 50, HOP = 25 ที่ 50 Hz และเมื่อ HOP = 50
- [ ] คำนวณ mean และ std ของหน้าต่าง [9.8, 9.8, 9.8, 9.8] กับ [7.8, 11.8, 7.8, 11.8] ด้วยมือ แล้วจดลงบันทึกการเรียน
- [ ] เขียนสายพาน log-mel ทีละขั้นด้วยคำของคุณเอง พร้อมบอกว่าขั้นไหนเคยทำมาแล้วในบทเรียน 4.4

## ไปต่อ

บทเรียน 4.6 เราจะเติมไฟล์ `s10_windowing.py` ให้เก็บ buffer บีบ feature และเลื่อนหน้าต่างเอง

บทเรียนถัดไป: [บทเรียน 4.6 — ลงมือทำ: feature vector จากหน้าต่างเลื่อน](../l06-windowing-lab/README.md)

## สะท้อนคิด

- ถ้าต้องจำแนก "เดิน" กับ "วิ่ง" คุณคิดว่า feature ตัวไหนในหกตัวนี้ช่วยมากที่สุด และยังขาดอะไร
- ทำไมการเปลี่ยนขนาดหน้าต่างหลังฝึกโมเดลแล้วจึงอันตราย
