---
id: edgeai-dev.m04.l04
lang: th
title: {th: 'ลงมือทำ: สเปกตรัมสดจาก IMU', en: 'Hands-on: a live spectrum from the IMU'}
summary: {th: เติม pipeline สี่ขั้นใน s09_fft_spectrum.py คือตัด DC คูณ Hann window หา magnitude และหา peak แล้วเขย่าบอร์ดดูแท่งสเปกตรัมกับความถี่เด่นเลื่อนตามจังหวะ พร้อมทดลองปิดทีละขั้นเพื่อเห็นว่าแต่ละขั้นแก้อะไร, en: 'Fill the four-step pipeline in s09_fft_spectrum.py (remove DC, apply a Hann window, compute the magnitude, find the peak), then shake the board to watch the bars and the dominant frequency follow your rhythm, and switch steps off one at a time to see what each fixes.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m04.l03]
objectives:
  - {th: เติมสี่ขั้นใน practice/s09_fft_spectrum.py จนแท่งสเปกตรัมขยับตามการเขย่า และความถี่เด่นที่แสดงอยู่ใกล้จำนวนครั้งที่เขย่าต่อวินาที (เช่นเขย่า 3 ครั้งต่อวินาทีได้ราว 3 Hz), en: Fill the four steps in practice/s09_fft_spectrum.py until the spectrum bars follow your shaking and the displayed peak is close to your shakes per second (about 3 Hz for three shakes a second).}
  - {th: ทดลองรันแบบไม่ตัด DC และแบบไม่คูณ window แล้วอธิบายได้ว่าสเปกตรัมเปลี่ยนไปอย่างไรและเพราะอะไร, en: 'Run once without removing DC and once without the window, and explain how the spectrum changes and why.'}
  - {th: อธิบายได้ว่าการเก็บ N จุดด้วยการหน่วง 1000/FS ms สม่ำเสมอ และการ normalize แท่งด้วยยอดสูงสุด ส่งผลต่อการอ่านสเปกตรัมอย่างไร, en: Explain how collecting N points with an even 1000/FS ms delay and normalising the bars by the highest peak affect reading the spectrum.}
develops: [{skill: sys.dsp, to: 3}, {skill: lang.micropython, to: 2}, {skill: gui.hmi, to: 1}]
assesses: [{skill: sys.dsp, level: 2, evidence: practice/s09_fft_spectrum.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 4.4 — ลงมือทำ: สเปกตรัมสดจาก IMU

> โมดูล 4 — วิเคราะห์สัญญาณ · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เติม pipeline สี่ขั้นใน s09_fft_spectrum.py คือตัด DC คูณ Hann window หา magnitude และหา peak แล้วเขย่าบอร์ดดูแท่งสเปกตรัมกับความถี่เด่นเลื่อนตามจังหวะ พร้อมทดลองปิดทีละขั้นเพื่อเห็นว่าแต่ละขั้นแก้อะไร

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เติมสี่ขั้นใน practice/s09_fft_spectrum.py จนแท่งสเปกตรัมขยับตามการเขย่า และความถี่เด่นที่แสดงอยู่ใกล้จำนวนครั้งที่เขย่าต่อวินาที (เช่นเขย่า 3 ครั้งต่อวินาทีได้ราว 3 Hz)
2. ทดลองรันแบบไม่ตัด DC และแบบไม่คูณ window แล้วอธิบายได้ว่าสเปกตรัมเปลี่ยนไปอย่างไรและเพราะอะไร
3. อธิบายได้ว่าการเก็บ N จุดด้วยการหน่วง 1000/FS ms สม่ำเสมอ และการ normalize แท่งด้วยยอดสูงสุด ส่งผลต่อการอ่านสเปกตรัมอย่างไร

## ก่อนเริ่ม

ผ่านบทเรียน 4.3 มาแล้ว รู้ว่า bin แปลงเป็น Hz อย่างไรและทำไมต้องตัด DC กับคูณ window
เตรียมจังหวะการเขย่าสามแบบ (ช้า กลาง เร็ว) และนับจำนวนครั้งต่อวินาทีของแต่ละแบบไว้เทียบ

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/)
- **เรียนมาก่อน:** [บทเรียน 4.3 — FFT และโดเมนความถี่: bin, Nyquist, DC, leakage และ Hann window](../l03-fft-frequency-domain/README.md)

## แนวคิด

ทั้งไฟล์อ่านเป็นประโยคเดียว: เก็บ N จุด → ตัด DC → คูณ window → FFT → หา magnitude → หา peak → วาดแท่ง
ส่วนที่ให้ไว้แล้วคือการเก็บ `az` จาก `sensors.bmi270.motion()` 32 จุดโดยหน่วง `1000/FS` ms สม่ำเสมอ (FFT อ่านความถี่ถูกต่อเมื่อระยะห่างเท่ากัน)
ฟังก์ชัน `fft()` แบบ radix-2 Cooley-Tukey ที่เขียนเป็น Python ให้อ่านได้ว่าเป็นแค่การบวกคูณเป็นระเบียบ และการวาดแท่งที่สร้างครั้งเดียวก่อนลูป

สี่ขั้นที่เราเติมคือ (1) `mean = sum(buf) / N` (2) `re = [(buf[i] - mean) * (0.5 - 0.5 * math.cos(2 * math.pi * i / (N - 1))) for i in range(N)]`
ซึ่งตัด DC แล้วคูณผ้าคลุมในบรรทัดเดียว (3) `mag = [math.sqrt(re[k] * re[k] + im[k] * im[k]) for k in range(HALF)]`
และ (4) `kmax = max(range(1, HALF), key=lambda k: mag[k])` เริ่มที่ 1 เพื่อข้าม bin 0 ที่ DC อาจหลงเหลือ
ความถี่เด่นแสดงเป็น `kmax * FS / N` แท่งถูก normalize ด้วยยอดสูงสุด จึงเต็มจอเสมอไม่ว่าเขย่าแรงหรือเบา

ถ้าลืมขั้นใด อาการจะบอกเอง: ไม่ตัด DC จะเห็น bin 0 พุ่ง ไม่คูณ window แท่งข้างเคียงของยอดจะรั่วสูงกว่าที่ควร ไม่หา magnitude แท่งแบนราบ
และไม่หา peak ความถี่เด่นจะค้างที่ bin 1 ความสำเร็จไม่ใช่แค่เห็นแท่งขยับ แต่ต้องบอกได้ว่า peak 3 Hz หมายถึงอะไร
และทำไมเขย่าเร็วขึ้นยอดจึงเลื่อนไปทางความถี่สูง

## ตัวอย่างสมบูรณ์

`s09_fft_spectrum.py` ในโฟลเดอร์ examples คือฉบับอ้างอิงที่ใช้ N = 64 ส่วน `s09_fft_spectrum_full.py` เพิ่มการเฉลี่ยสเปกตรัมแบบ EMA
ให้แท่งนิ่ง โชว์ความถี่เด่นตัวใหญ่ด้วย Seg7 ค้างยอดสูงสุด (peak-hold) และวัดพลังงานรวม (RMS)

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/s09_fft_spectrum.py](examples/s09_fft_spectrum.py) | จากโดเมนเวลา สู่โดเมนความถี่ (FFT) |
| [examples/s09_fft_spectrum_full.py](examples/s09_fft_spectrum_full.py) | สเปกตรัม FFT สด ๆ จาก IMU (ฉบับเต็ม) |

## ฝึกเติม

คอมเมนต์ `# เติม:` สี่ขั้นอยู่ที่บรรทัด 95 (ตัด DC), 100 (Hann window), 110 (magnitude) และ 115 (peak)
แทนค่าเริ่มต้นด้วยคำสั่งตามคำใบ้ แล้วเขย่าบอร์ดแกน Z เร็วช้าสลับกัน ถ้าแท่งไม่ขยับ ตรวจการเยื้องบรรทัดและชื่อตัวแปรก่อน

| ไฟล์ฝึก | เรื่อง |
|---|---|
| [practice/s09_fft_spectrum.py](practice/s09_fft_spectrum.py) | จากโดเมนเวลา สู่โดเมนความถี่ (ฉบับฝึกเติมโค้ด) |

## เฉลย

เปิดเฉลยหลังจากลองเองแล้วอย่างน้อยหนึ่งรอบ และอ่าน [วิธีใช้เฉลย](../../README.md#วิธีใช้เฉลย) ก่อน

| เฉลย | คู่กับ |
|---|---|
| [solution/s09_fft_spectrum.py](solution/s09_fft_spectrum.py) | [practice/s09_fft_spectrum.py](practice/s09_fft_spectrum.py) |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. เรียงขั้นของ pipeline ใน s09_fft_spectrum.py *(เรียงลำดับ · เป้าหมายข้อ 1)*
   - ก) fft(re, im)
   - ข) mean = sum(buf) / N (ตัด DC)
   - ค) kmax = max(range(1, HALF), key=...) (หา peak)
   - ง) คูณ Hann window
   - จ) mag = sqrt(re² + im²) ครึ่งแรก

   <details><summary>เฉลย</summary>

   **ข → ง → ก → จ → ค** — ตัด DC → window → FFT → magnitude → peak ขั้น FFT ให้ไว้แล้ว ส่วนอีกสี่ขั้นคือช่องที่เราเติม

   </details>

2. เติมครบแล้ว แท่งขยับตามการเขย่า แต่ป้าย peak ค้างที่ 1.6 Hz (bin 1) ตลอด ขั้นใดยังไม่ได้เติม *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) ตัด DC
   - ข) Hann window
   - ค) magnitude
   - ง) หา peak (kmax ยังเป็นค่าเริ่มต้น 1)

   <details><summary>เฉลย</summary>

   **ง** — placeholder kmax = 1 ทำให้ความถี่เด่นชี้ bin 1 เสมอ ต้องแทนด้วย max(range(1, HALF), key=lambda k: mag[k])

   </details>

3. ถ้าไม่คูณ Hann window สเปกตรัมจะเปลี่ยนอย่างไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) bin 0 พุ่งกลบทุกอย่าง
   - ข) ยอดยังอยู่ที่เดิม แต่แท่งข้างเคียงรั่วสูงกว่าที่ควร สเปกตรัมเลอะ
   - ค) แท่งแบนราบทั้งหมด
   - ง) ความถี่เด่นหายไป

   <details><summary>เฉลย</summary>

   **ข** — ขอบของหน้าต่างที่ไม่พอดีคาบเวลาของสัญญาณทำให้พลังงานรั่ว (spectral leakage) Hann กดขอบให้เป็นศูนย์จึงลดการรั่ว ส่วน bin 0 พุ่งเป็นอาการของการไม่ตัด DC

   </details>

4. ถ้าลบ time.sleep_ms(int(1000 / FS)) ออกจากลูปเก็บ N จุด ผลคืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) ไม่มีผลเพราะ FFT ไม่สนเวลา
   - ข) อัตราสุ่มจริงไม่ใช่ FS อีกต่อไป การแปลง kmax · FS / N เป็น Hz จึงผิด
   - ค) สเปกตรัมละเอียดขึ้นเสมอ
   - ง) บอร์ดรีสตาร์ต

   <details><summary>เฉลย</summary>

   **ข** — สูตร f = k·FS/N ถือว่าจุดห่างกัน 1/FS วินาทีเท่ากันทุกจุด ถ้าอัตราจริงต่างไป ค่า Hz ที่แสดงจะไม่ตรงกับความจริง

   </details>

## แล็บ

**MVP ของชุดบทเรียน 4.3–4.4:** รัน `s09_fft_spectrum.py` แล้วอ่านสเปกตรัมสดออก แท่งความถี่และ peak (Hz) เปลี่ยนตามการเขย่าเร็วหรือช้าจริง

- [ ] เติมไฟล์ฝึกครบสี่ขั้น รันได้บน Emulator หรือบอร์ด
- [ ] เขย่าสามจังหวะ (ช้า กลาง เร็ว) จด peak กี่ Hz ลงบันทึกการเรียนแล้วเทียบกับจำนวนครั้งต่อวินาทีที่นับได้
- [ ] รันแบบไม่ตัด DC (ปล่อย `mean = 0.0`) และแบบไม่คูณ window แล้วอธิบายว่าสเปกตรัมเปลี่ยนไปอย่างไร
- [ ] อธิบายได้ว่า pipeline ตัด DC, window, magnitude และ peak อยู่ตรงไหน ทำอะไร

## ไปต่อ

ชุดบทเรียนถัดไป (บทเรียน 4.5–4.6) เราจะต่อจากสเปกตรัมไปเป็นหน้าต่างเลื่อนและ feature vector ซึ่งคือสิ่งที่โมเดลเห็นจริง

บทเรียนถัดไป: [บทเรียน 4.5 — feature และหน้าต่าง: สิ่งที่โมเดลเห็นจริง](../l05-features-and-windowing/README.md)

## สะท้อนคิด

- peak ที่คุณวัดได้ตรงกับจังหวะที่นับเองแค่ไหน ถ้าคลาดเคลื่อน คิดว่ามาจากความละเอียดของ bin หรือจากมือคุณเอง
- ถ้าต้องตรวจมอเตอร์ที่หมุน 1,500 รอบต่อนาที คุณต้องตั้ง FS อย่างน้อยเท่าไร
