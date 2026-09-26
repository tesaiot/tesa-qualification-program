---
id: edgeai-dev.m04.l02
lang: th
title: {th: 'ลงมือทำ: ฟิลเตอร์ทำสัญญาณให้สะอาดสด ๆ', en: 'Hands-on: cleaning a live signal with a filter'}
summary: {th: เติมห้าจุดใน s08_filters.py ให้สร้างฟิลเตอร์จากชื่อด้วย keyword argument อ่านขนาดความเร่ง ป้อนเข้า filt.update และวาดกราฟดิบเทียบกรอง แล้ววัดผลด้วย noise down % และเทียบสามฟิลเตอร์กับสัญญาณเดียวกัน, en: 'Fill five points in s08_filters.py to build a filter by name with keyword arguments, read the acceleration magnitude, feed filt.update and plot raw against filtered, then measure the result as noise down % and compare three filters on the same signal.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m04.l01]
objectives:
  - {th: 'เติมห้าจุดใน practice/s08_filters.py จนสองกราฟต่างกันชัด (เส้นล่างเรียบกว่าเส้นบน) และเลือก EMA, Median, Kalman1D ใน dropdown ได้ครบโดยไม่เกิด error', en: 'Fill the five points in practice/s08_filters.py until the two charts clearly differ (the lower line is smoother) and EMA, Median and Kalman1D can all be selected without an error.'}
  - {th: จดค่า noise down % ของสามฟิลเตอร์กับสัญญาณเดียวกัน และสร้างสถานการณ์ที่ Median ชนะ EMA ชัดเจนพร้อมอธิบายเหตุผล, en: 'Record noise down % for the three filters on the same signal, and create a situation where Median clearly beats EMA, explaining why.'}
  - {th: อธิบายได้ว่าทำไมบรรทัด y = filt.update(x) บรรทัดเดียวใช้ได้กับทุกฟิลเตอร์ และทำไม noise down % วัดจากการกระตุกระหว่างเฟรม, en: 'Explain why the single line y = filt.update(x) works for every filter, and why noise down % is measured from frame-to-frame jitter.'}
develops: [{skill: sys.dsp, to: 2}, {skill: lang.micropython, to: 2}, {skill: sys.sensors-actuators, to: 2}]
assesses: [{skill: sys.dsp, level: 2, evidence: practice/s08_filters.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 4.2 — ลงมือทำ: ฟิลเตอร์ทำสัญญาณให้สะอาดสด ๆ

> โมดูล 4 — วิเคราะห์สัญญาณ · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เติมห้าจุดใน s08_filters.py ให้สร้างฟิลเตอร์จากชื่อด้วย keyword argument อ่านขนาดความเร่ง ป้อนเข้า filt.update และวาดกราฟดิบเทียบกรอง แล้ววัดผลด้วย noise down % และเทียบสามฟิลเตอร์กับสัญญาณเดียวกัน

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เติมห้าจุดใน practice/s08_filters.py จนสองกราฟต่างกันชัด (เส้นล่างเรียบกว่าเส้นบน) และเลือก EMA, Median, Kalman1D ใน dropdown ได้ครบโดยไม่เกิด error
2. จดค่า noise down % ของสามฟิลเตอร์กับสัญญาณเดียวกัน และสร้างสถานการณ์ที่ Median ชนะ EMA ชัดเจนพร้อมอธิบายเหตุผล
3. อธิบายได้ว่าทำไมบรรทัด y = filt.update(x) บรรทัดเดียวใช้ได้กับทุกฟิลเตอร์ และทำไม noise down % วัดจากการกระตุกระหว่างเฟรม

## ก่อนเริ่ม

ผ่านบทเรียน 4.1 มาแล้ว รู้จักนิสัยของ EMA, Median และ Kalman1D
เตรียมบันทึกการเรียนไว้จดค่า noise down % ของแต่ละฟิลเตอร์

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — โหมด IMU ครบบน Emulator ส่วนโหมด Radar range บน Emulator เป็นระยะจำลองจากลูกบิด ไม่มี multipath จริง
- **เรียนมาก่อน:** [บทเรียน 4.1 — ฟิลเตอร์ DSP: EMA, Median, Kalman และ radar range profile](../l01-dsp-filters/README.md)

## แนวคิด

ทั้งไฟล์อ่านเป็นประโยคเดียว: อ่านค่าดิบ → ป้อนเข้าฟิลเตอร์ → วาดดิบเทียบกรอง → วัดว่าลด noise ได้กี่เปอร์เซ็นต์ วนทุก 60 ms
ฟิลเตอร์ถูกสร้างใน "ขั้นสร้างครั้งเดียว" ผ่าน `make_filter(name)` ที่แปลงชื่อเป็นอ็อบเจกต์: EMA ให้ไว้แล้วเป็นตัวอย่าง เราเติม
`return dsp.Median(window=MED_WINDOW)` และ `return dsp.Kalman1D(q=KAL_Q, r=KAL_R)` ต้องเป็น keyword เสมอ
ถ้าลืมเติมสองจุดนี้ แอปยังรันได้ด้วย EMA แต่พอเลือก Median หรือ Kalman ฟังก์ชันจะคืน `None` แล้วพังตอนเรียก `update`

`read_raw()` อ่าน `sensors.bmi270.acceleration()` แล้วยุบเป็นขนาด `mag = (ax*ax + ay*ay + az*az) ** 0.5` (นิ่งราว 9.8)
คูณ 10 ให้เห็นชัดบนกราฟ 0..250 เพราะฟิลเตอร์ของบทเรียนนี้เป็นหนึ่งมิติ จึงต้องแปลงเวกเตอร์เป็นสเกลาร์ก่อน โหมด Radar range
อ่าน `sensors.radar_range()` เป็นเซนติเมตรโดยห่อ `try/except OSError` ไว้ หัวใจของบทเรียนคือบรรทัดเดียว `y = filt.update(x)`
ที่ไม่ต้องรู้ว่า `filt` เป็นฟิลเตอร์ชนิดไหน เพราะทุกตัวใช้ API เดียวกัน ถ้าลืมเติม (`y = x`) สองกราฟจะเหมือนกันเป๊ะ
ซึ่งเป็นการทดสอบง่าย ๆ ว่าเติมถูกหรือยัง

เราวัดความเรียบจาก **การกระตุกระหว่างเฟรม** ผลรวมของ |x − x_prev| ของเส้นดิบเทียบเส้นกรอง แล้ว
`red = (1 − filt_jit / raw_jit) × 100` เพราะกับเซนเซอร์จริงเราไม่มีเฉลยว่าค่าจริงคือเท่าไร การกระตุกที่ลดลงจึงเป็นตัวชี้ที่ตรงไปตรงมา
ความสำเร็จไม่ใช่ "เส้นดูสวย" แต่ต้องบอกได้ว่าทำไม Median ชนะ EMA ตอนเจอ spike และทำไม α เล็กลงจึงเรียบขึ้นแต่ตามช้าลง

## ตัวอย่างสมบูรณ์

`s08_filters_full.py` เพิ่ม slider จูนพารามิเตอร์สดตามชนิดฟิลเตอร์ (α ของ EMA, window ของ Median, r ของ Kalman) แถบ noise down
ที่เปลี่ยนสีตามเกณฑ์ และปุ่ม Freeze หยุดภาพไว้เทียบหนามกับเส้นเรียบ

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/s08_filters_full.py](examples/s08_filters_full.py) | ทำสัญญาณให้สะอาดด้วยฟิลเตอร์ DSP (ฉบับเต็ม) |

## ฝึกเติม

คอมเมนต์ `# เติม:` ห้าจุดอยู่ที่บรรทัด 46 (Median), 49 (Kalman1D), 99 (ขนาดความเร่ง), 144 (`filt.update`) และ 148 (วาดสองกราฟ)
เติมทีละจุด แล้วขยับบอร์ด สลับฟิลเตอร์ครบสามตัว ถ้าสองกราฟไม่ต่างกัน ให้ตรวจจุดที่ 144 ก่อน

| ไฟล์ฝึก | เรื่อง |
|---|---|
| [practice/s08_filters.py](practice/s08_filters.py) | ทำสัญญาณให้สะอาดด้วยฟิลเตอร์ DSP (ฉบับฝึกเติมโค้ด) |

## เฉลย

เปิดเฉลยหลังจากลองเองแล้วอย่างน้อยหนึ่งรอบ และอ่าน [วิธีใช้เฉลย](../../README.md#วิธีใช้เฉลย) ก่อน

| เฉลย | คู่กับ |
|---|---|
| [solution/s08_filters.py](solution/s08_filters.py) | [practice/s08_filters.py](practice/s08_filters.py) |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. เติมไฟล์แล้วแต่เส้น Filtered เหมือนเส้น Raw ทุกจุดไม่ว่าจะเลือกฟิลเตอร์ใด จุดใดยังว่าง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) return dsp.Median(window=MED_WINDOW)
   - ข) mag = (ax*ax + ay*ay + az*az) ** 0.5
   - ค) y = filt.update(x)
   - ง) raw_chart.value(clamp(x))

   <details><summary>เฉลย</summary>

   **ค** — placeholder y = x ทำให้ค่าที่วาดบนเส้นล่างคือค่าดิบ สองกราฟต่างกันก็ต่อเมื่อค่าผ่าน filt.update จริง

   </details>

2. เขียน return dsp.Median(5) ในจุดที่ 1 แล้วเลือก Median จะเกิดอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) ได้หน้าต่าง 5 ค่าตามต้องการ
   - ข) โยน TypeError เพราะ window เป็นพารามิเตอร์แบบ keyword เท่านั้น
   - ค) ได้หน้าต่าง 6 ค่า
   - ง) ฟิลเตอร์กลายเป็น EMA

   <details><summary>เฉลย</summary>

   **ข** — พารามิเตอร์ของฟิลเตอร์ใน dsp เป็น keyword-only ต้องเขียน dsp.Median(window=5) การส่งแบบ positional จะถูกปฏิเสธทันที

   </details>

3. เคาะบอร์ดแรงครั้งเดียวให้เกิด spike ผลที่คาดว่าจะเห็นบนเส้น Filtered ของ EMA เทียบกับ Median คืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) ทั้งสองตัดทิ้งได้เท่ากัน
   - ข) EMA เกลี่ยเป็นโหนกนุ่มที่ยังเห็น ส่วน Median โหวต spike ตกไปจนแทบไม่เห็น
   - ค) EMA ตัดทิ้งหมด ส่วน Median เกลี่ยเป็นโหนก
   - ง) ทั้งสองทำให้เส้นกลายเป็นศูนย์

   <details><summary>เฉลย</summary>

   **ข** — EMA ถ่วงค่าโดดเข้าไปในผลลัพธ์บางส่วน Median เลือกค่ากลางจึงไม่สนค่าโดดเดี่ยว นี่คือความต่างของ "เกลี่ย" กับ "โหวตตัด"

   </details>

4. raw_jit = 400 และ filt_jit = 100 ค่า noise down % เป็นเท่าไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) 25%
   - ข) 75%
   - ค) 100%
   - ง) 400%

   <details><summary>เฉลย</summary>

   **ข** — red = (1 − 100/400) × 100 = 75% การกระตุกของเส้นกรองเหลือหนึ่งในสี่ของเส้นดิบ

   </details>

## แล็บ

**MVP ของชุดบทเรียน 4.1–4.2:** ฟิลเตอร์ปรับสัญญาณเซนเซอร์ที่มี noise ให้ดีขึ้นอย่างเห็นได้ เส้น Filtered เรียบกว่า Raw ชัดเจน พร้อมตัวเลข noise down % ยืนยัน

- [ ] เติมไฟล์ฝึกครบห้าจุด รันได้บน Emulator หรือบอร์ด
- [ ] สลับครบสามฟิลเตอร์กับสัญญาณเดียวกัน แล้วจด noise down % ของแต่ละตัวลงบันทึกการเรียน
- [ ] สร้าง spike (เคาะบอร์ดแรงครั้งเดียว หรือใช้ radar บนบอร์ด) แล้วอธิบายว่าทำไม Median ชนะ EMA
- [ ] อธิบายได้ว่าเลือกฟิลเตอร์ตัวไหน เพราะอะไร และข้อแลกเปลี่ยนเรียบกับตอบสนองคืออะไร

## ไปต่อ

ชุดบทเรียนถัดไป (บทเรียน 4.3–4.4) เราจะมองสัญญาณเดียวกันในโดเมนความถี่ด้วย FFT

บทเรียนถัดไป: [บทเรียน 4.3 — FFT และโดเมนความถี่: bin, Nyquist, DC, leakage และ Hann window](../l03-fft-frequency-domain/README.md)

## สะท้อนคิด

- ถ้าต่อ Median แล้วตามด้วย EMA คุณคาดว่าจะได้ผลแบบไหน และต้องแลกกับอะไร
- noise down % สูงที่สุดเสมอเป็นสิ่งที่ดีที่สุดหรือไม่ ลองนึกถึงงานที่ต้องตอบสนองเร็ว
