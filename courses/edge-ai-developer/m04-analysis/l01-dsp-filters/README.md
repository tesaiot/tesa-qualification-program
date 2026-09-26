---
id: edgeai-dev.m04.l01
lang: th
title: {th: 'ฟิลเตอร์ DSP: EMA, Median, Kalman และ radar range profile', en: 'DSP filters: EMA, Median, Kalman and the radar range profile'}
summary: {th: 'เปิดเสาที่ 3 (Analysis) ด้วยฟิลเตอร์ตามเวลา รู้ว่าสัญญาณรบกวนมีหลายหน้า เลือก EMA, Median หรือ Kalman1D ให้ตรงกับหน้าของ noise ใช้ API ร่วม update/value/reset และเห็น radar range profile ที่ฝั่ง C ทำให้แล้ว', en: 'Open pillar 3 (Analysis) with temporal filters - recognise the kinds of noise, choose EMA, Median or Kalman1D to match, use the shared update/value/reset API, and see the radar range profile the C side already computes.'}
level: L3
time_min: {concept: 45, practise: 10, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m03.l04]
objectives:
  - {th: 'แยกชนิดของสัญญาณรบกวน (white noise, spike, drift) และเลือกฟิลเตอร์ที่เหมาะกับแต่ละชนิดได้ พร้อมเหตุผล', en: 'Tell apart kinds of noise (white noise, spikes, drift) and choose the filter that suits each, with a reason.'}
  - {th: คำนวณ EMA หนึ่งก้าวด้วย y = αx + (1−α)y_prev และค่ากลางของหน้าต่าง Median ด้วยมือ แล้วอธิบายข้อแลกเปลี่ยนระหว่างความเรียบกับการตอบสนองเมื่อปรับ α, en: 'Compute one EMA step with y = αx + (1−α)y_prev and the median of a window by hand, and explain the smoothness-versus-response trade-off when α changes.'}
  - {th: อธิบาย Kalman gain K = P/(P+R) ว่าคือน้ำหนักที่ให้กับการวัด และบอกผลของการเพิ่ม r หรือ q, en: 'Explain the Kalman gain K = P/(P+R) as the weight given to the measurement, and state the effect of raising r or q.'}
  - {th: สร้างฟิลเตอร์ของ dsp ด้วย keyword argument ครั้งเดียวนอกลูป แล้วป้อนทีละค่าด้วย update() และอธิบายได้ว่าทำไมสร้างในลูปแล้วไม่เรียบ, en: 'Create a dsp filter with keyword arguments once outside the loop, feed it one sample at a time with update(), and explain why creating it inside the loop never smooths.'}
develops: [{skill: sys.dsp, to: 2}, {skill: hw.math, to: 2}, {skill: sys.sensors-actuators, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 4.1 — ฟิลเตอร์ DSP: EMA, Median, Kalman และ radar range profile

> โมดูล 4 — วิเคราะห์สัญญาณ · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เปิดเสาที่ 3 (Analysis) ด้วยฟิลเตอร์ตามเวลา รู้ว่าสัญญาณรบกวนมีหลายหน้า เลือก EMA, Median หรือ Kalman1D ให้ตรงกับหน้าของ noise ใช้ API ร่วม update/value/reset และเห็น radar range profile ที่ฝั่ง C ทำให้แล้ว

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. แยกชนิดของสัญญาณรบกวน (white noise, spike, drift) และเลือกฟิลเตอร์ที่เหมาะกับแต่ละชนิดได้ พร้อมเหตุผล
2. คำนวณ EMA หนึ่งก้าวด้วย y = αx + (1−α)y_prev และค่ากลางของหน้าต่าง Median ด้วยมือ แล้วอธิบายข้อแลกเปลี่ยนระหว่างความเรียบกับการตอบสนองเมื่อปรับ α
3. อธิบาย Kalman gain K = P/(P+R) ว่าคือน้ำหนักที่ให้กับการวัด และบอกผลของการเพิ่ม r หรือ q
4. สร้างฟิลเตอร์ของ dsp ด้วย keyword argument ครั้งเดียวนอกลูป แล้วป้อนทีละค่าด้วย update() และอธิบายได้ว่าทำไมสร้างในลูปแล้วไม่เรียบ

## ก่อนเริ่ม

ผ่านโมดูล 3 มาแล้ว เคยเห็นเกจสั่นทั้งที่วางบอร์ดนิ่งในบทเรียน 3.2 บทเรียนนี้คือคำตอบของอาการนั้น
เปิด `s08_filters_full.py` (อยู่ในบทเรียน 4.2) ไว้ลองเล่นก่อนแกะ

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — เรดาร์จริงมีบน TESAIoT Dev Kit ส่วนบน Emulator ระยะเรดาร์จำลองด้วยลูกบิด
- **เรียนมาก่อน:** [บทเรียน 3.4 — ลงมือทำ: ตัวจำแนกความสบายด้วยกฎ](../../m03-processing/l04-rule-classifier-lab/README.md)

## ดูของจริงก่อน

รัน `s08_filters_full.py` ก่อนอ่านโค้ด กราฟบนคือสัญญาณดิบ (ขนาดความเร่งสามแกน) กราฟล่างคือค่าเดียวกันหลังกรอง
เขย่าบอร์ดเบา ๆ แล้วสลับฟิลเตอร์ใน dropdown ดูว่าเส้นล่างเปลี่ยนนิสัยอย่างไร และแถบ noise down % บอกว่าลดการกระตุกได้กี่เปอร์เซ็นต์

## แนวคิด

ไม่มีเซนเซอร์ตัวไหนให้ค่าเรียบ สัญญาณรบกวนมีหลายหน้า: **white noise** หนามเล็กกระจายจากความร้อนหรือ ADC (เหมาะกับ EMA/SMA),
**spike/outlier** ค่าโดดเป็นครั้งคราวจาก multipath หรือการชนสัญญาณ (เหมาะกับ Median), **drift** ค่าเลื่อนช้า ๆ (เหมาะกับ HPF)
และแบบผสม (เหมาะกับ Kalman) ไม่มีฟิลเตอร์ตัวเทพ ต้องมองศัตรูก่อนหยิบเครื่องมือ Analysis มาก่อน Training เสมอ เพราะถ้าป้อนสัญญาณสกปรก
โมเดลจะเรียน "หนาม" ไปด้วย

ฟิลเตอร์ตามเวลาคือ **ความจำ** มันถ่วงค่าใหม่กับอดีต ฟิลเตอร์ใน `dsp` ทำงานแบบ streaming บน CM33 ทุกตัวใช้ API เดียวกัน:
สร้างครั้งเดียวนอกลูป → `y = f.update(x)` ทุกรอบ → `f.value()` อ่านค่าล่าสุด → `f.reset()` ล้าง state พารามิเตอร์ทุกตัวเป็น
**keyword argument** (`alpha=`, `window=`, `q=`, `r=`) ส่งแบบ positional เช่น `dsp.EMA(0.15)` จะโยน `TypeError`
ถ้าเผลอสร้างฟิลเตอร์ในลูป ความจำจะถูกลบทุกรอบ เส้นจะไม่มีวันเรียบ

**EMA:** $y[n] = \alpha x[n] + (1-\alpha) y[n-1]$ α เล็กเรียบแต่ตามช้า α ใหญ่ไวแต่หนามยังโผล่ ค่า `EMA_ALPHA = 0.15` คือเชื่อของใหม่ 15%
**Median** เรียงค่าล่าสุด N ตัวแล้วเอาค่ากลาง ค่าโดดจึงไม่มีสิทธิ์ชนะ (เช่น 98, 101, 240, 99, 100 ได้ 100 แต่ค่าเฉลี่ยได้ 127.6) เฟิร์มแวร์บังคับ
window เป็นเลขคี่ไม่เกิน 15 **Kalman1D** เก็บทั้งค่าประมาณและความไม่มั่นใจ P ทุกก้าวคำนวณ $K = P/(P+R)$ แล้ว $x \leftarrow x + K(z - x)$
`r` สูง (ไม่เชื่อเซนเซอร์) ทำให้ K เล็กจึงเรียบ `q` สูงยอมให้ค่าจริงขยับเร็ว มองได้ว่า Kalman คือ EMA ที่ปรับ α ของตัวเองได้

ตัวอย่างของจริงคือ **radar range profile**: `sensors.radar_range()` คืน `distance_m`, `peak_db`, `resolution_m`, `target`, `seq`
ฝั่ง C ทำ HPF → FFT → dB → หา peak ให้หมด ความละเอียดราว 0.33 เมตรต่อ bin และระยะชอบกระโดดเพราะ multipath ซึ่งคือ spike แท้ ๆ
ฟิลเตอร์ที่เหมาะจึงเป็น Median และในงานจริงเรามักต่อฟิลเตอร์กัน เช่น Median กัน spike ก่อนแล้ว EMA เกลี่ยต่อ

## ตัวอย่างสมบูรณ์

`05_radar_distance.py` คือไม้วัดระยะด้วยเรดาร์ที่ใช้ Median กันระยะกระโดด ลองทาย (Predict) ก่อนรันว่าถ้าเดินเข้าออกหน้าบอร์ด
ตัวเลขจะนิ่งหรือกระโดด แล้วรันเทียบบนบอร์ด

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/05_radar_distance.py](examples/05_radar_distance.py) | Radar Range: ไม้วัดระยะบนจอ (Bar + Seg7 + กราฟ) |

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นหรือใน `shared/` ด้วย:

- [m04-analysis/l02-filters-lab/examples/s08_filters_full.py](../l02-filters-lab/examples/s08_filters_full.py) — ทำสัญญาณให้สะอาดด้วยฟิลเตอร์ DSP (ฉบับเต็ม)
- [m04-analysis/l02-filters-lab/practice/s08_filters.py](../l02-filters-lab/practice/s08_filters.py) — ทำสัญญาณให้สะอาดด้วยฟิลเตอร์ DSP (ฉบับฝึกเติมโค้ด)

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. ระยะจากเรดาร์กระโดดเป็นครั้งคราวเพราะการสะท้อนหลายทาง ควรเลือกฟิลเตอร์ใดเป็นลำดับแรก *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) EMA
   - ข) Median
   - ค) HPF
   - ง) ไม่ต้องกรอง

   <details><summary>เฉลย</summary>

   **ข** — การกระโดดเป็น spike แท้ ๆ Median โหวตค่ากลางจึงตัด spike ทิ้งได้ ส่วน EMA จะเกลี่ยให้เป็นโหนกที่ยังเห็นอยู่

   </details>

2. y_prev = 10, x = 20 และ α = 0.25 ค่า EMA รอบนี้เป็นเท่าไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) 12.5
   - ข) 15
   - ค) 17.5
   - ง) 20

   <details><summary>เฉลย</summary>

   **ก** — y = 0.25 × 20 + 0.75 × 10 = 5 + 7.5 = 12.5 ค่าใหม่ได้น้ำหนักแค่หนึ่งในสี่ เส้นจึงตามช้าแต่เรียบ

   </details>

3. หน้าต่าง Median ห้าค่าคือ 98 101 240 99 100 ผลลัพธ์คืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) 127.6
   - ข) 100
   - ค) 240
   - ง) 98

   <details><summary>เฉลย</summary>

   **ข** — เรียงได้ 98 99 100 101 240 ค่ากลางคือ 100 spike 240 ถูกดันไปขอบ ขณะที่ค่าเฉลี่ย 127.6 ถูก spike ลาก

   </details>

4. ใน Kalman1D ถ้าเพิ่ม r (ไม่เชื่อเซนเซอร์มากขึ้น) โดย q คงเดิม ผลคืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) K โตขึ้น ค่ากระโดดตามการวัด
   - ข) K เล็กลง ค่าขยับทีละน้อย เรียบขึ้นแต่ตามช้าลง
   - ค) ไม่มีผลเพราะ K คงที่
   - ง) ฟิลเตอร์หยุดทำงาน

   <details><summary>เฉลย</summary>

   **ข** — K = P/(P+R) เมื่อ R โต K เล็กลง x += K(z − x) จึงขยับน้อย ได้ความเรียบแลกกับการตอบสนองแบบเดียวกับ α เล็กของ EMA

   </details>

5. โค้ดนี้สร้าง f = dsp.EMA(alpha=0.15) ไว้ในลูปทุกรอบแล้วเรียก f.update(x) ผลบนกราฟคืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) เส้นเรียบมากเพราะ α เล็ก
   - ข) เส้นกรองเหมือนเส้นดิบ เพราะฟิลเตอร์ที่เพิ่งสร้างคืนค่าแรกที่ป้อนตรง ๆ และความจำถูกลบทุกรอบ
   - ค) โปรแกรมโยน TypeError
   - ง) เส้นเป็นศูนย์ตลอด

   <details><summary>เฉลย</summary>

   **ข** — state อยู่ในอ็อบเจกต์ การสร้างใหม่ทุกรอบคือการเริ่มต้นใหม่ทุกครั้ง ฟิลเตอร์จึงไม่มีอดีตให้ถ่วง ต้องสร้างครั้งเดียวนอกลูป

   </details>

## แล็บ

- [ ] คำนวณ EMA ด้วยมือสามก้าวจาก x = 10, 10, 20 เริ่ม y = 10 ที่ α = 0.5 และ α = 0.1 แล้วเทียบว่าตัวไหนตามทันกว่า
- [ ] หาค่ากลางของหน้าต่าง [5, 7, 90, 6, 5] เทียบกับค่าเฉลี่ย แล้วจดลงบันทึกการเรียนว่าทำไมต่างกัน
- [ ] ใน REPL ลองเรียก `dsp.EMA(0.15)` ดูข้อความ error แล้วแก้เป็น `dsp.EMA(alpha=0.15)`

## ไปต่อ

บทเรียน 4.2 เราจะเติมไฟล์ `s08_filters.py` ให้สร้างฟิลเตอร์จากชื่อ กรองสัญญาณจริง และวัดผลเป็น noise down %

บทเรียนถัดไป: [บทเรียน 4.2 — ลงมือทำ: ฟิลเตอร์ทำสัญญาณให้สะอาดสด ๆ](../l02-filters-lab/README.md)

## สะท้อนคิด

- งานที่คุณสนใจเจอสัญญาณรบกวนหน้าไหนมากที่สุด และคุณยอมช้าได้แค่ไหนเพื่อแลกความเรียบ
- ทำไมการวัดความเรียบด้วยการกระตุกระหว่างเฟรมจึงใช้กับเซนเซอร์จริงได้ แม้ไม่มี "เฉลย" ว่าค่าจริงคือเท่าไร
