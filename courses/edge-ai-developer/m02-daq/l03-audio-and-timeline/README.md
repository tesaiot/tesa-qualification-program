---
id: edgeai-dev.m02.l03
lang: th
title: {th: 'เสียงและหลายเซนเซอร์บนเส้นเวลาเดียว: PDM 16 kHz ประทับเวลา และ jitter', en: 'Audio and several sensors on one timeline: 16 kHz PDM, timestamps and jitter'}
summary: {th: เพิ่มเซนเซอร์ตัวที่สองให้ dataset เข้าใจว่าไมโครโฟน PDM ส่งเสียงเป็น PCM 16 kHz อย่างไร ย่อเฟรมเสียงเป็นค่า dBFS ค่าเดียว แล้วมัดเสียงกับ IMU ไว้บนเส้นเวลาเดียวด้วย ticks_ms และตรวจ jitter ได้, en: 'Add a second sensor to the dataset - learn how the PDM microphone delivers 16 kHz PCM, reduce an audio frame to one dBFS value, and tie sound and IMU to one timeline with ticks_ms while checking for jitter.'}
level: L3
time_min: {concept: 40, practise: 10, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m02.l02]
objectives:
  - {th: อธิบายเส้นทาง PDM → PCM 16-bit → RMS → dBFS และคำนวณ dBFS ของเฟรมจาก RMS ได้ (เช่น RMS = 3277 ได้ราว −20 dBFS), en: Explain the path PDM → 16-bit PCM → RMS → dBFS and compute a frame's dBFS from its RMS (for example RMS = 3277 gives about −20 dBFS).}
  - {th: คำนวณระยะห่างระหว่างตัวอย่างเสียง Ts = 1/fs และความยาวของหนึ่งเฟรม t = N/fs ได้ และบอกว่าเฟรมที่ยาวเกินจังหวะแถวส่งผลกับ jitter อย่างไร, en: 'Compute the sample spacing Ts = 1/fs and one frame''s length t = N/fs, and say how a frame longer than the row period affects jitter.'}
  - {th: 'อธิบายได้ว่าทำไมต้อง "อ่านพร้อมกัน เขียนแถวเดียว ประทับเวลาร่วม" และใช้ time.ticks_diff(time.ticks_ms(), t0) แทนการลบตรง ๆ', en: 'Explain why you "read together, write one row, share one timestamp", and use time.ticks_diff(time.ticks_ms(), t0) instead of plain subtraction.'}
develops: [{skill: ai.data-collection, to: 2}, {skill: sys.dsp, to: 2}, {skill: sys.sensors-actuators, to: 2}, {skill: mcu.timers, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 2.3 — เสียงและหลายเซนเซอร์บนเส้นเวลาเดียว: PDM 16 kHz ประทับเวลา และ jitter

> โมดูล 2 — เก็บข้อมูลจากเซนเซอร์ (DAQ) · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เพิ่มเซนเซอร์ตัวที่สองให้ dataset เข้าใจว่าไมโครโฟน PDM ส่งเสียงเป็น PCM 16 kHz อย่างไร ย่อเฟรมเสียงเป็นค่า dBFS ค่าเดียว แล้วมัดเสียงกับ IMU ไว้บนเส้นเวลาเดียวด้วย ticks_ms และตรวจ jitter ได้

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. อธิบายเส้นทาง PDM → PCM 16-bit → RMS → dBFS และคำนวณ dBFS ของเฟรมจาก RMS ได้ (เช่น RMS = 3277 ได้ราว −20 dBFS)
2. คำนวณระยะห่างระหว่างตัวอย่างเสียง Ts = 1/fs และความยาวของหนึ่งเฟรม t = N/fs ได้ และบอกว่าเฟรมที่ยาวเกินจังหวะแถวส่งผลกับ jitter อย่างไร
3. อธิบายได้ว่าทำไมต้อง "อ่านพร้อมกัน เขียนแถวเดียว ประทับเวลาร่วม" และใช้ time.ticks_diff(time.ticks_ms(), t0) แทนการลบตรง ๆ

## ก่อนเริ่ม

ผ่านชุดบทเรียน 2.1–2.2 มาแล้ว มีไฟล์ `/gestures.csv` ของตัวเองและเข้าใจสี่จังหวะ DAQ
ถ้าจะใช้เสียงจริง เตรียมบอร์ดที่ไมโครโฟน PDM ใช้ได้ (ดูบรรทัดอุปกรณ์ด้านล่าง)

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — เสียงจริงต้องมาจากไมโครโฟน PDM บนบอร์ด ตัวอย่างเสียง 06/07 ระบุว่าใช้ได้บน PSoC Edge AI Kit ส่วนบน TESAIoT Dev Kit (มี audio codec) การเปิด PDM ยังชน clock ของระบบเสียง Emulator มี PDM_PCM ที่ส่งเสียงสังเคราะห์ให้ลองโครงโปรแกรมได้เท่านั้น
- **เรียนมาก่อน:** [บทเรียน 2.2 — ลงมือทำ: DAQ logger เก็บ dataset ลง CSV](../l02-daq-logger-lab/README.md)

## ดูของจริงก่อน

รัน `06_mic_level_meter.py` แล้วพูดหรือปรบมือใส่ไมค์ แถบ VU กับตัวเลข dBFS จะวิ่งตาม เห็นเสียงกลายเป็นตัวเลขจริง ๆ
จากนั้นดู `07_mic_record_wav.py` ที่อัดเสียงดิบทั้งก้อนลงไฟล์ `.wav` สองตัวนี้คือวัตถุดิบที่เราจะเอามามัดกับ IMU

## แนวคิด

ไมโครโฟนบนบอร์ดเป็นแบบ **PDM** ที่ส่งบิต 0/1 ความเร็วสูง ฮาร์ดแวร์ `machine.PDM_PCM` แปลงเป็นตัวอย่างเสียง **PCM** 16-bit
ที่ `sample_rate=16000` ให้เราอ่านเข้า `array.array("h", ...)` ด้วย `pdm.readinto(buf)` ระยะห่างระหว่างตัวอย่างคือ
$T_s = 1/f_s = 62.5\ \mu s$ และ 16 kHz พอสำหรับเสียงพูดและเสียงสิ่งแวดล้อมที่พลังงานส่วนใหญ่อยู่ต่ำกว่า 8 kHz ตามกฎ Nyquist
เราอ่านทีละก้อน `CHUNK = 512` ตัวอย่าง หนึ่งเฟรมจึงยาว $t = N/f_s = 512/16000 = 32$ ms

เก็บทุกตัวอย่างลง CSV ไม่ไหว (16,000 ค่าต่อวินาที) จึงย่อเฟรมเป็น **ค่าเดียว**: หา RMS (ขนาดเฉลี่ยของคลื่น) แล้วเทียบกับค่าสูงสุดของ 16-bit
เป็นเดซิเบล $\text{dBFS} = 20\log_{10}(\text{RMS}/32768)$ 0 คือดังสุด ยิ่งลบยิ่งเบา เสียงดิบทั้งก้อนเก็บแยกเป็น WAV ได้ถ้าต้องการ

ปัญหาของสองเซนเซอร์คือ **การ sync**: ถ้าเก็บคนละไฟล์คนละจังหวะ จะจับคู่ไม่ได้ว่าเสียงไหนคู่กับท่าไหน ทางออกคือ
**อ่านพร้อมกัน เขียนแถวเดียว ประทับเวลาร่วม**: ในหนึ่งรอบลูป อ่าน IMU และ MIC ติดกัน แล้วเขียนหนึ่งแถวที่ทั้งคู่ใช้ `t_ms` เดียวกัน
`t_ms = time.ticks_diff(time.ticks_ms(), t0)` ใช้ `ticks_diff` เพราะตัวนับมิลลิวินาทีวนกลับศูนย์ได้ (wrap-around)
ช่วงจริงระหว่างแถวจะเพี้ยนจาก 20 ms บ้างเพราะงานอ่านเสียงและเขียนไฟล์กินเวลา เรียกว่า **jitter** เพราะเราเก็บ `t_ms` จริงไว้ทุกแถว
จึงตรวจย้อนหลังได้ และลด jitter ได้ด้วยการลด `CHUNK` ลดงานในลูป และไม่พิมพ์ console ถี่ schema ของไฟล์คือ
`t_ms,label,ax,ay,az,gx,gy,gz,db` โดย label อยู่ทุกแถว dataset จึงพร้อม train ตั้งแต่ออกจากบอร์ด

## ตัวอย่างสมบูรณ์

ทาย (Predict) ก่อนรัน `06_mic_level_meter.py` ว่าเงียบกับปรบมือได้ dBFS ต่างกันราวเท่าไร แล้วรันเทียบ
ส่วน `07_mic_record_wav.py` ใช้ดึงไฟล์ `/rec.wav` ออกด้วย BENTO IDE (file transfer) หรือ `mpremote` แล้วเปิดฟังบน PC

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/06_mic_level_meter.py](examples/06_mic_level_meter.py) | VU Meter: ไมค์ PDM -> RMS -> dBFS -> แถบระดับเสียง + peak hold |
| [examples/07_mic_record_wav.py](examples/07_mic_record_wav.py) | อัดเสียงเป็นไฟล์ .wav พร้อมหน้าจอนับถอยหลัง |

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นหรือใน `shared/` ด้วย:

- [m02-daq/l02-daq-logger-lab/practice/s04_daq_logger.py](../l02-daq-logger-lab/practice/s04_daq_logger.py) — เก็บข้อมูล sensor ลงไฟล์ CSV (Data Acquisition) (ฉบับฝึกเติมโค้ด)
- [m02-daq/l04-multicapture-lab/practice/s05_multicapture.py](../l04-multicapture-lab/practice/s05_multicapture.py) — เก็บ 2 เซนเซอร์พร้อมกันบนเส้นเวลาเดียว (ฉบับฝึกเติมโค้ด)

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. เฟรมเสียงมี RMS = 32768 ซึ่งเท่ากับค่าสูงสุดของ 16-bit ค่า dBFS เป็นเท่าไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) 0 dBFS
   - ข) −96 dBFS
   - ค) +20 dBFS
   - ง) 32768 dBFS

   <details><summary>เฉลย</summary>

   **ก** — 20·log10(32768/32768) = 20·log10(1) = 0 dBFS คือดังสุด เสียงที่เบากว่านี้จะได้ค่าติดลบ ส่วน −96 คือค่าที่โค้ดใช้แทนความเงียบสนิท

   </details>

2. เรียงเส้นทางของเสียงจากไมโครโฟนจนเป็นคอลัมน์ db ใน CSV *(เรียงลำดับ · เป้าหมายข้อ 1)*
   - ก) หา RMS ของเฟรม
   - ข) บิต PDM 0/1 ความเร็วสูง
   - ค) แปลงเป็น dBFS แล้วเขียนลงแถว
   - ง) ตัวอย่าง PCM 16-bit ใน buf จาก pdm.readinto()

   <details><summary>เฉลย</summary>

   **ข → ง → ก → ค** — PDM → PCM ใน buffer → RMS → dBFS เป็นค่าเดียวต่อเฟรม ซึ่งเป็นก้าวแรกก่อนทำ spectrogram ในโมดูล 4

   </details>

3. ที่ fs = 16 kHz เฟรมขนาด N = 512 ตัวอย่างยาวเท่าไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) 3.2 ms
   - ข) 32 ms
   - ค) 62.5 µs
   - ง) 512 ms

   <details><summary>เฉลย</summary>

   **ข** — t = N / fs = 512 / 16000 = 0.032 วินาที = 32 ms ยาวกว่าจังหวะแถว 20 ms การอ่านเสียงจึงเป็นตัวการหลักของ jitter

   </details>

4. วิธีใดทำให้ค่าเสียงกับค่า IMU ใน dataset จับคู่ตามเวลาได้แน่นอน *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) เก็บเสียงกับ IMU คนละไฟล์แล้วจับคู่ตามลำดับบรรทัดทีหลัง
   - ข) อ่านทั้งสองเซนเซอร์ในรอบเดียวของลูป แล้วเขียนแถวเดียวที่มี t_ms ร่วมกัน
   - ค) ใช้ time.time() บันทึกเวลาแยกให้แต่ละไฟล์
   - ง) ตั้ง RATE_MS ให้เท่ากับ 0

   <details><summary>เฉลย</summary>

   **ข** — หนึ่งรอบ = หนึ่งแถว = หนึ่ง t_ms ทุกคอลัมน์ของแถวจึงหมายถึงช่วงเวลาเดียวกัน การจับคู่ตามลำดับพลาดง่ายเมื่ออัตราต่างกัน

   </details>

5. ทำไมใช้ time.ticks_diff(time.ticks_ms(), t0) แทน time.ticks_ms() - t0 *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) เพราะ ticks_diff เร็วกว่า
   - ข) เพราะตัวนับมิลลิวินาทีวนกลับศูนย์ได้ (wrap-around) ticks_diff คิดช่วงเวลาให้ถูกแม้ตัวนับวนรอบ
   - ค) เพราะ ticks_ms คืนค่าเป็นวินาที
   - ง) เพราะการลบใน MicroPython ทำไม่ได้

   <details><summary>เฉลย</summary>

   **ข** — ticks_ms กับ ticks_diff คือคู่มาตรฐานของ MicroPython สำหรับวัดช่วงเวลาสั้น ๆ อย่างปลอดภัยจาก wrap-around

   </details>

## แล็บ

- [ ] รัน VU meter แล้วจดค่า dBFS ตอนเงียบ ตอนพูด และตอนปรบมือลงบันทึกการเรียน
- [ ] คำนวณ t = N/fs ของ CHUNK = 256 และ 1024 แล้วบอกว่าตัวไหนเสี่ยงทำให้แถวห่างเกิน 20 ms
- [ ] เขียน schema ของไฟล์ multi-sensor ด้วยมือ แล้วบอกว่าแต่ละคอลัมน์มาจากคำสั่งอะไร

## ไปต่อ

บทเรียน 2.4 เราจะเติมไฟล์ `s05_multicapture.py` ให้เก็บ IMU กับเสียงบนเส้นเวลาเดียวลง `/multicapture.csv`

บทเรียนถัดไป: [บทเรียน 2.4 — ลงมือทำ: เก็บ IMU กับเสียงลงไฟล์เดียว](../l04-multicapture-lab/README.md)

## สะท้อนคิด

- งานไหนในชีวิตจริงที่ต้องดูเสียงกับการเคลื่อนไหวพร้อมกันถึงจะตัดสินถูก
- ถ้าเก็บเสียงกับ IMU มาคนละไฟล์แล้ว คุณยังพอกู้ให้ตรงเวลาได้ไหม ต้องมีข้อมูลอะไรเพิ่ม
