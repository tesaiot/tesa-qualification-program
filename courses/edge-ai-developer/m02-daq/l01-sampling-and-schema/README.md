---
id: edgeai-dev.m02.l01
lang: th
title: {th: 'สุ่มสัญญาณให้ตรงกับโมเดล: อัตราสุ่ม Nyquist หน้าต่าง และ schema ของ CSV', en: 'Sampling to match the model: rate, Nyquist, windows and the CSV schema'}
summary: {th: เริ่มวงจรจากต้นน้ำ เข้าใจว่า DAQ คืออะไร ทำไมอัตราสุ่มต้องคงที่และต้องตรงกับที่โมเดลกิน (50 Hz) ใช้กฎ Nyquist กับสูตรความยาวหน้าต่าง T = N/fs และออกแบบ schema ของไฟล์ CSV ที่เขียนลง flash บนบอร์ด, en: 'Start the cycle upstream - learn what DAQ is, why the sampling rate must be steady and match what the model was trained on (50 Hz), use the Nyquist rule and the window length T = N/fs, and design the CSV schema written to the board''s flash.'}
level: L3
time_min: {concept: 40, practise: 10, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m01.l07]
objectives:
  - {th: 'อธิบายได้ว่าทำไม DAQ เป็นขั้นที่ 1 ของวงจรข้อมูล และยกปัจจัยที่ทำให้ dataset เสีย (garbage in, garbage out) ได้อย่างน้อยสามข้อ', en: 'Explain why DAQ is stage 1 of the data cycle and name at least three things that spoil a dataset (garbage in, garbage out).'}
  - {th: ใช้กฎ Nyquist fs ≥ 2·fmax ตัดสินว่าอัตราสุ่มที่กำหนดพอสำหรับสัญญาณหนึ่งหรือไม่ และคำนวณความยาวของหนึ่ง burst ด้วย T = N/fs, en: 'Use the Nyquist rule fs ≥ 2·fmax to judge whether a sampling rate is enough for a signal, and compute the length of one burst with T = N/fs.'}
  - {th: อธิบายได้ว่าทำไม logger ต้องสุ่มที่ 50 Hz ให้ตรงกับโมเดล Motion บนบอร์ด และจะเกิดอะไรกับรูปคลื่นถ้าเก็บที่อัตราอื่น, en: 'Explain why the logger samples at 50 Hz to match the Motion model on the board, and what happens to the waveform if you record at another rate.'}
  - {th: 'เขียน schema label,ax,ay,az,gx,gy,gz และบรรทัด CSV หนึ่ง sample ได้ถูก และเลือกโหมดเปิดไฟล์ "a" หรือ "w" ได้เหมาะกับสถานการณ์', en: 'Write the schema label,ax,ay,az,gx,gy,gz and a one-sample CSV line correctly, and choose the "a" or "w" file mode for the situation.'}
develops: [{skill: ai.data-collection, to: 2}, {skill: sys.dsp, to: 1}, {skill: sys.memory-fs, to: 1}, {skill: sys.sensors-actuators, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 2.1 — สุ่มสัญญาณให้ตรงกับโมเดล: อัตราสุ่ม Nyquist หน้าต่าง และ schema ของ CSV

> โมดูล 2 — เก็บข้อมูลจากเซนเซอร์ (DAQ) · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เริ่มวงจรจากต้นน้ำ เข้าใจว่า DAQ คืออะไร ทำไมอัตราสุ่มต้องคงที่และต้องตรงกับที่โมเดลกิน (50 Hz) ใช้กฎ Nyquist กับสูตรความยาวหน้าต่าง T = N/fs และออกแบบ schema ของไฟล์ CSV ที่เขียนลง flash บนบอร์ด

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. อธิบายได้ว่าทำไม DAQ เป็นขั้นที่ 1 ของวงจรข้อมูล และยกปัจจัยที่ทำให้ dataset เสีย (garbage in, garbage out) ได้อย่างน้อยสามข้อ
2. ใช้กฎ Nyquist fs ≥ 2·fmax ตัดสินว่าอัตราสุ่มที่กำหนดพอสำหรับสัญญาณหนึ่งหรือไม่ และคำนวณความยาวของหนึ่ง burst ด้วย T = N/fs
3. อธิบายได้ว่าทำไม logger ต้องสุ่มที่ 50 Hz ให้ตรงกับโมเดล Motion บนบอร์ด และจะเกิดอะไรกับรูปคลื่นถ้าเก็บที่อัตราอื่น
4. เขียน schema label,ax,ay,az,gx,gy,gz และบรรทัด CSV หนึ่ง sample ได้ถูก และเลือกโหมดเปิดไฟล์ "a" หรือ "w" ได้เหมาะกับสถานการณ์

## ก่อนเริ่ม

ผ่านโมดูล 1 มาแล้ว รู้จักโครงสี่จังหวะและ `sensors.bmi270.motion()`
เปิด REPL ของ BENTO IDE ไว้ลองเรียก `sensors.bmi270.motion()` ตอนวางนิ่งเทียบกับตอนเขย่า

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/)
- **เรียนมาก่อน:** [บทเรียน 1.7 — ลงมือทำ: จาก verdict สู่ action บนบอร์ด](../../m01-onboarding/l07-verdict-action-lab/README.md)

## แนวคิด

**DAQ (Data Acquisition)** คือการเก็บข้อมูลดิบจากเซนเซอร์ให้เป็นชุดที่เก็บ ค้น และใช้ต่อได้ เป็นวัตถุดิบตั้งต้นของทุกโมเดล
โมเดล Motion ที่เราเล่นในโมดูล 1 ก็เกิดจากคนที่เขย่าเซนเซอร์แล้วเก็บตัวเลขเป็นพัน ๆ sample ก่อน คุณภาพของ dataset
ขึ้นกับการติด label ถูก อัตราสุ่มคงที่ ความสมดุลของคลาส และความหลากหลายของสภาพจริง ข้อมูลเข้าเป็นขยะ ผลออกก็เป็นขยะ

**อัตราสุ่ม** คือจำนวนครั้งที่อ่านเซนเซอร์ต่อวินาที 50 Hz คืออ่านทุก 20 ms ในไฟล์จึงตั้ง `RATE_MS = 20` ไม่ใช่เลขสุ่ม
แต่ตรงกับอัตราที่โมเดล Motion บนบอร์ดถูกฝึกมา ถ้าเก็บที่อัตราอื่น รูปคลื่นจะยืดหรือหด ไม่เหมือนที่โมเดลเคยเห็น กฎ **Nyquist**
บอกว่าต้องสุ่มอย่างน้อยสองเท่าของความถี่สูงสุดที่อยากจับ $f_s \ge 2 f_{max}$ ไม่งั้นสัญญาณเร็วจะแปลงร่างเป็นคลื่นช้าปลอม (aliasing)
ความยาวหนึ่ง burst คือ $T = N / f_s$ เช่น `BURST = 200` ที่ 50 Hz ได้ 4 วินาที ยาวพอให้ทำท่าเต็มรอบ เพราะท่าทางเป็นรูปแบบตามเวลา
โมเดลต้องเห็นหลาย sample เรียงกันจึงแยก circle ออกจาก shaking ได้

**schema** ของ CSV คือบรรทัดแรก `label,ax,ay,az,gx,gy,gz` เป็นสัญญาระหว่างคนเก็บกับคนเทรน แต่ละบรรทัดถัดไปคือหนึ่ง snapshot
ของ IMU หกแกนพร้อมชื่อท่า ไฟล์เขียนลง flash บนบอร์ด (LittleFS) ด้วย `open()`/`write()` แบบเดียวกับ Python บนคอม
โหมด `"a"` เขียนต่อท้าย ส่วน `"w"` ทับไฟล์ ใช้ `"w"` ได้เฉพาะตอนรู้แน่ว่ายังไม่มีไฟล์ ก่อนเขียนโค้ดควรถามเซนเซอร์ใน REPL ก่อน
ว่าค่านิ่งกับค่าเขย่าหน้าตาเป็นอย่างไร จะได้รู้ว่าข้อมูลที่ลงไฟล์ "สมเหตุผล" หรือไม่

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. ข้อใดทำให้ dataset เสียทั้งที่โปรแกรมไม่ขึ้น error (เลือกทุกข้อที่ถูก) *(เลือกได้หลายข้อ · เป้าหมายข้อ 1)*
   - ก) กดปุ่ม shaking แต่วางบอร์ดนิ่ง
   - ข) เก็บ idle 1000 sample แต่ shaking แค่ 50 sample
   - ค) อัตราสุ่มแกว่งไปมาเดี๋ยวเร็วเดี๋ยวช้า
   - ง) เก็บหลายคนหลายท่าทางให้หลากหลาย

   <details><summary>เฉลย</summary>

   **ก, ข, ค** — label ผิด คลาสไม่สมดุล และอัตราไม่คงที่ ล้วนสอนโมเดลผิดแบบเงียบ ๆ ส่วนความหลากหลายของสภาพจริงทำให้โมเดลทนขึ้น

   </details>

2. การเขย่ามือเร็วสุดราว 10 Hz อัตราสุ่มต่ำสุดตามกฎ Nyquist คือเท่าไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) 5 Hz
   - ข) 10 Hz
   - ค) 20 Hz
   - ง) 100 Hz

   <details><summary>เฉลย</summary>

   **ค** — fs ≥ 2·fmax = 2 × 10 = 20 Hz ถ้าต่ำกว่านี้จะเกิด aliasing การเก็บที่ 50 Hz จึงเผื่อไว้พอ

   </details>

3. เก็บ N = 150 sample ที่ fs = 50 Hz หนึ่ง burst ยาวกี่วินาที *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) 0.33 วินาที
   - ข) 3 วินาที
   - ค) 7.5 วินาที
   - ง) 200 วินาที

   <details><summary>เฉลย</summary>

   **ข** — T = N / fs = 150 / 50 = 3 วินาที

   </details>

4. ถ้าเก็บ dataset ที่ 25 Hz ไปฝึกหรือเทียบกับโมเดลที่ฝึกมาที่ 50 Hz ปัญหาคืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) ไม่มีปัญหา เพราะค่าแต่ละ sample เหมือนเดิม
   - ข) รูปคลื่นตามเวลาจะห่างและยืดต่างจากที่โมเดลเคยเห็น โมเดลจึงอาจทายผิด
   - ค) ไฟล์จะใหญ่ขึ้นสองเท่า
   - ง) บอร์ดจะเขียนไฟล์ไม่ได้

   <details><summary>เฉลย</summary>

   **ข** — อัตราสุ่มตอนเก็บข้อมูลต้องเท่ากับตอนใช้งานจริง นี่คือหลักสำคัญของ Edge AI dataset สวยแค่ไหนก็ใช้ไม่ได้ถ้าอัตราไม่ตรง

   </details>

5. logger กดเก็บสาม burst แต่ไฟล์เหลือแค่ burst สุดท้าย สาเหตุน่าจะเป็นอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) เปิดไฟล์ในลูปบันทึกด้วยโหมด "w" ซึ่งทับไฟล์ทุกครั้ง แทนที่จะใช้ "a"
   - ข) ลืมเขียน \n ท้ายบรรทัด
   - ค) เรียก motion() แทน acceleration()
   - ง) flash เต็ม

   <details><summary>เฉลย</summary>

   **ก** — โหมด "a" เขียนต่อท้ายโดยไม่ลบของเก่า ใช้ "w" ได้เฉพาะตอนสร้างไฟล์ใหม่พร้อมหัวตาราง

   </details>

## แล็บ

- [ ] ใน REPL เรียก `sensors.bmi270.motion()` ตอนวางนิ่งและตอนเขย่า จดค่าลงบันทึกการเรียน
- [ ] คำนวณ T = N/fs ของ BURST = 200 ที่ 50 Hz และที่ 25 Hz
- [ ] เขียน schema และบรรทัดตัวอย่างหนึ่งบรรทัดของ sample ที่คุณอ่านได้จริงด้วยมือ

## ไปต่อ

บทเรียน 2.2 เราจะเขียน logger จริงตามสี่จังหวะ schema → sample → record → rate แล้วเก็บ dataset ไฟล์แรกของเรา

บทเรียนถัดไป: [บทเรียน 2.2 — ลงมือทำ: DAQ logger เก็บ dataset ลง CSV](../l02-daq-logger-lab/README.md)

## สะท้อนคิด

- ถ้าเซนเซอร์ของคุณจับสัญญาณที่แกว่งเร็วสุด 12 Hz คุณจะตั้งอัตราสุ่มเท่าไร และทำไมไม่ตั้งสูงเกินจำเป็น
- label ที่ผิดหนึ่ง burst ใน dataset หลายพันบรรทัด ส่งผลกับโมเดลอย่างไร
