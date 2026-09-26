---
id: edgeai-dev.m04.l03
lang: th
title: {th: 'FFT และโดเมนความถี่: bin, Nyquist, DC, leakage และ Hann window', en: 'The FFT and the frequency domain: bins, Nyquist, DC, leakage and the Hann window'}
summary: {th: มองสัญญาณในโดเมนความถี่ เข้าใจว่า FFT แยกสัญญาณเป็นไซน์หลายความถี่อย่างไร แปลง bin เป็น Hz ด้วย f = k·FS/N รู้จัก bin width และ Nyquist เลือก N อย่างมีเหตุผล และจัดการศัตรูของสเปกตรัมด้วยการตัด DC Hann window และ magnitude, en: 'See signals in the frequency domain - how the FFT splits a signal into sines, converting a bin to Hz with f = k·FS/N, bin width and Nyquist, choosing N sensibly, and handling the spectrum''s enemies with DC removal, a Hann window and the magnitude.'}
level: L3
time_min: {concept: 45, practise: 10, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m04.l02]
objectives:
  - {th: อธิบายความต่างของโดเมนเวลากับโดเมนความถี่ และเหตุผลที่โมเดลเสียงดูสเปกตรัมแทนคลื่นดิบได้อย่างน้อยสองข้อ, en: Explain the difference between the time and frequency domains and give at least two reasons audio models look at the spectrum rather than the raw wave.}
  - {th: คำนวณความถี่ของ bin ด้วย f = k·FS/N bin width = FS/N และ Nyquist = FS/2 ได้ และเลือก N ให้เหมาะกับงานโดยบอกข้อแลกเปลี่ยนระหว่างความละเอียดกับความไว, en: 'Compute a bin''s frequency with f = k·FS/N, the bin width FS/N and Nyquist FS/2, and choose N for a task by stating the resolution-versus-responsiveness trade-off.'}
  - {th: อธิบายว่าทำไมต้องลบค่าเฉลี่ย (ตัด DC) คูณ Hann window และหา magnitude √(re² + im²) เฉพาะครึ่งแรกของ bin ก่อนอ่านสเปกตรัม, en: 'Explain why you subtract the mean (remove DC), multiply by a Hann window and take the magnitude √(re² + im²) over the first half of the bins before reading the spectrum.'}
  - {th: ตรวจความถูกต้องของ FFT ด้วยไซน์ที่รู้ความถี่ล่วงหน้า และทำนายได้ว่า peak ควรอยู่ที่ bin ใด, en: Check an FFT with a sine of known frequency and predict which bin the peak should land in.}
develops: [{skill: sys.dsp, to: 3}, {skill: hw.math, to: 2}, {skill: test.unit-tdd, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 4.3 — FFT และโดเมนความถี่: bin, Nyquist, DC, leakage และ Hann window

> โมดูล 4 — วิเคราะห์สัญญาณ · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

มองสัญญาณในโดเมนความถี่ เข้าใจว่า FFT แยกสัญญาณเป็นไซน์หลายความถี่อย่างไร แปลง bin เป็น Hz ด้วย f = k·FS/N รู้จัก bin width และ Nyquist เลือก N อย่างมีเหตุผล และจัดการศัตรูของสเปกตรัมด้วยการตัด DC Hann window และ magnitude

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. อธิบายความต่างของโดเมนเวลากับโดเมนความถี่ และเหตุผลที่โมเดลเสียงดูสเปกตรัมแทนคลื่นดิบได้อย่างน้อยสองข้อ
2. คำนวณความถี่ของ bin ด้วย f = k·FS/N bin width = FS/N และ Nyquist = FS/2 ได้ และเลือก N ให้เหมาะกับงานโดยบอกข้อแลกเปลี่ยนระหว่างความละเอียดกับความไว
3. อธิบายว่าทำไมต้องลบค่าเฉลี่ย (ตัด DC) คูณ Hann window และหา magnitude √(re² + im²) เฉพาะครึ่งแรกของ bin ก่อนอ่านสเปกตรัม
4. ตรวจความถูกต้องของ FFT ด้วยไซน์ที่รู้ความถี่ล่วงหน้า และทำนายได้ว่า peak ควรอยู่ที่ bin ใด

## ก่อนเริ่ม

ผ่านชุดบทเรียน 4.1–4.2 มาแล้ว เข้าใจฟิลเตอร์ในโดเมนเวลา และจำกฎ Nyquist จากบทเรียน 2.1 ได้
ถ้ามีเวลา ดาวน์โหลด [`math_lab.html`](../../shared/interactive/math_lab.html) มาเปิดในเบราว์เซอร์ (ต้องต่อเน็ตเพื่อโหลด GeoGebra) เพื่อลองเลื่อนความถี่ของคลื่นผสม

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/)
- **เรียนมาก่อน:** [บทเรียน 4.2 — ลงมือทำ: ฟิลเตอร์ทำสัญญาณให้สะอาดสด ๆ](../l02-filters-lab/README.md)

## ดูของจริงก่อน

รัน `s09_fft_spectrum_full.py` (อยู่ในบทเรียน 4.4) แล้วเขย่าบอร์ดขึ้นลงช้า ๆ สลับเร็ว ๆ แท่งสเปกตรัมจะขยับและความถี่เด่นเลื่อนตามจังหวะ
เห็น "พลังงานย้ายความถี่" ก่อน แล้วค่อยถามว่ามันรู้ได้อย่างไร

## แนวคิด

สัญญาณเดียวกันมองได้สองแบบ **โดเมนเวลา** บอกว่าตอนไหนสูงตอนไหนต่ำ **โดเมนความถี่** บอกว่าความถี่ไหนแรง โมเดลเสียงเลือกแบบหลัง
เพราะเสียงเดียวกันสองครั้งไม่เหมือนกันในโดเมนเวลาแต่การกระจายพลังงานตามความถี่คล้ายกัน สเปกตรัมบีบข้อมูลจาก 16,000 จุดต่อวินาทีเหลือไม่กี่สิบค่า
และความถี่มีความหมายทางกายภาพ หัวใจของ Fourier คือสัญญาณใด ๆ เขียนเป็นผลบวกของไซน์หลายความถี่ได้ FFT ถามกลับว่า "มีไซน์ความถี่ไหนบ้าง แรงแค่ไหน"

**FFT** คือวิธีคำนวณเร็วของ DFT $X[k] = \sum_{n=0}^{N-1} x[n] e^{-j 2\pi k n / N}$ รับ N จุด (เลขยกกำลังสอง) คืน N ค่าเชิงซ้อน
ด้วยเวลา $N\log N$ แทน $N^2$ bin ที่ k มีความถี่ $f_k = k F_S / N$ bin width $F_S/N$ คือความละเอียด และ Nyquist $F_S/2$ คือเพดาน
ที่ $F_S = 50$ Hz และ $N = 32$ หนึ่ง bin กว้าง 1.5625 Hz bin 4 คือ 6.25 Hz และอ่านได้ถึง 25 Hz การเลือก N คือการแลก:
N มากแยกความถี่ใกล้กันได้แต่ต้องเก็บนาน (N = 64 ใช้ราว 1.28 วินาที) N น้อยอัปเดตไวแต่ความถี่ใกล้กันรวมอยู่ bin เดียว

สเปกตรัมมีศัตรูที่ต้องจัดการก่อนอ่าน: (1) **DC** accel ที่วางนิ่งมีแรงโน้มถ่วงคงที่ซึ่งไปกองที่ bin 0 จนกลบทุกอย่าง แก้ด้วยการลบค่าเฉลี่ยของหน้าต่าง
(2) **spectral leakage** ขอบของท่อนสัญญาณไม่พอดีคาบเวลาของสัญญาณ พลังงานจึงรั่วไป bin ข้างเคียง แก้ด้วย Hann window
$w[i] = 0.5 - 0.5\cos(2\pi i/(N-1))$ ที่กดขอบให้เป็นศูนย์ แลกกับยอดที่อ้วนขึ้นเล็กน้อย (3) ผลเป็นเลขเชิงซ้อน เราสนแค่ขนาด
$|X[k]| = \sqrt{re^2 + im^2}$ และใช้แค่ครึ่งแรก (`HALF = N//2`) เพราะครึ่งหลังเป็นภาพสะท้อน จากนั้นหา bin เด่นโดยข้าม bin 0
แล้วแปลงเป็น Hz ก่อนเชื่อ FFT กับข้อมูลจริง ให้ตรวจด้วยไซน์ที่รู้คำตอบก่อนเสมอ เช่นไซน์ 6.25 Hz ต้องได้ peak ที่ bin 4

## ตัวอย่างสมบูรณ์

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นหรือใน `shared/` ด้วย:

- [shared/interactive/math_lab.html](../../shared/interactive/math_lab.html)

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. ข้อใดเป็นเหตุผลที่โมเดลเสียงดูสเปกตรัมแทนคลื่นดิบ (เลือกทุกข้อที่ถูก) *(เลือกได้หลายข้อ · เป้าหมายข้อ 1)*
   - ก) เสียงเดียวกันสองครั้งมีรูปคลื่นต่างกัน แต่การกระจายพลังงานตามความถี่คล้ายกัน
   - ข) สเปกตรัมบีบข้อมูลให้สั้นลง โมเดลจึงเล็กและเร็วขึ้น
   - ค) ความถี่มีความหมายทางกายภาพที่อ่านออก
   - ง) FFT ทำให้เสียงดังขึ้น

   <details><summary>เฉลย</summary>

   **ก, ข, ค** — สามข้อแรกคือเหตุผลในสไลด์ FFT ไม่ได้เปลี่ยนความดัง มันแค่เปลี่ยนมุมมองจากเวลาเป็นความถี่

   </details>

2. FS = 50 Hz และ N = 32 bin ที่ 3 คือความถี่เท่าไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) 3 Hz
   - ข) 4.69 Hz
   - ค) 6.25 Hz
   - ง) 25 Hz

   <details><summary>เฉลย</summary>

   **ข** — f = k·FS/N = 3 × 50 / 32 ≈ 4.69 Hz หนึ่ง bin กว้าง 1.5625 Hz

   </details>

3. ถ้าเพิ่ม N จาก 32 เป็น 128 ที่ FS = 50 Hz ผลคืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) bin กว้างขึ้น อัปเดตเร็วขึ้น
   - ข) bin แคบลงเหลือราว 0.39 Hz แยกความถี่ใกล้กันได้ แต่ต้องเก็บจุดนานราว 2.56 วินาที สเปกตรัมจึงอัปเดตช้า
   - ค) Nyquist สูงขึ้นเป็น 100 Hz
   - ง) ไม่มีผลเพราะ FFT ใช้ N เท่าไรก็ได้

   <details><summary>เฉลย</summary>

   **ข** — bin width = FS/N ส่วน Nyquist ขึ้นกับ FS เท่านั้น ความละเอียดความถี่กับความไวในเวลาแลกกันเสมอ

   </details>

4. วางบอร์ดนิ่งแล้วเห็นแท่ง bin 0 สูงเด่นกลบทุกแท่ง ขั้นใดถูกข้ามไป *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) การตัด DC ด้วยการลบค่าเฉลี่ยของหน้าต่าง
   - ข) การคูณ Hann window
   - ค) การหา magnitude
   - ง) การหา peak

   <details><summary>เฉลย</summary>

   **ก** — แรงโน้มถ่วงเป็นค่าคงที่ ในโดเมนความถี่คือ 0 Hz จึงไปกองที่ bin 0 ต้องลบค่าเฉลี่ยก่อน FFT

   </details>

5. สร้างไซน์ 12.5 Hz ที่ FS = 50 Hz, N = 32 ป้อน FFT peak ควรอยู่ที่ bin ใด *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) bin 4
   - ข) bin 8
   - ค) bin 12
   - ง) bin 16

   <details><summary>เฉลย</summary>

   **ข** — k = f·N/FS = 12.5 × 32 / 50 = 8 ลงตัวพอดี ถ้า FFT ถูก peak ต้องอยู่ที่ bin 8

   </details>

## แล็บ

- [ ] คำนวณความถี่ของ bin 1, 3 และ 8 ที่ FS = 50 Hz, N = 32 แล้วจดลงบันทึกการเรียน
- [ ] ใน REPL ทำ sanity check ด้วยไซน์ 6.25 Hz ตามสไลด์ แล้วลองเปลี่ยนเป็น 5 Hz ดูว่า peak เกลี่ยระหว่าง bin ใด
- [ ] เลือก N สำหรับงานที่ต้องแยกการสั่น 3.0 Hz กับ 3.5 Hz ออกจากกันที่ FS = 50 Hz พร้อมเหตุผล

## ไปต่อ

บทเรียน 4.4 เราจะเติม pipeline สี่ขั้นใน `s09_fft_spectrum.py` แล้วอ่านสเปกตรัมสดจาก IMU ด้วยตาตัวเอง

บทเรียนถัดไป: [บทเรียน 4.4 — ลงมือทำ: สเปกตรัมสดจาก IMU](../l04-fft-spectrum-lab/README.md)

## สะท้อนคิด

- งานรอบตัวคุณงานไหนที่ "ความถี่" บอกได้มากกว่า "ค่าตามเวลา" เช่นมอเตอร์ที่เริ่มเสีย
- ถ้าต้องการสเปกตรัมที่อัปเดตไวและละเอียดไปพร้อมกัน คุณจะแก้ปัญหานี้อย่างไร
