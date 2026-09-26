---
id: edgeai-dev.m06.l05
lang: th
title: {th: 'sensor fusion: verdict ของโมเดลกับเซนเซอร์ดิบ', en: 'Sensor fusion: the model''s verdict with the raw sensor'}
summary: {th: ทำให้การตัดสินใจเชื่อถือได้ขึ้นด้วย sensor fusion เอา verdict ของโมเดล (บอกว่าเป็นอะไร) มายืนยันกับเซนเซอร์ดิบ (บอกว่าแรงแค่ไหน) เข้าใจ corroboration แบบ AND กับ majority vote แบบ k จาก n ผ่านสูตรถ่วงน้ำหนักเดียวกัน และเห็นตัวอย่างระบบกันขโมยสามเซนเซอร์, en: 'Make decisions more trustworthy with sensor fusion - confirm the model''s verdict (what it is) with a raw sensor (how strong it is). Understand AND-style corroboration and k-of-n majority voting as one weighted formula, and study a three-sensor intruder alarm.'}
level: L3
time_min: {concept: 45, practise: 15, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m06.l04]
objectives:
  - {th: อธิบายได้ว่าทำไม verdict ของโมเดลเดี่ยวยังไม่พอ และโมเดลกับเซนเซอร์ดิบตอบคนละคำถามอย่างไร, en: 'Explain why a single model''s verdict is not enough, and how the model and a raw sensor answer different questions.'}
  - {th: คำนวณการตัดสินแบบโหวต k จาก n และแบบถ่วงน้ำหนัก S = Σ wᵢsᵢ ≥ θ ได้ และแสดงว่า AND คือกรณี k = n, en: 'Compute a k-of-n vote and a weighted decision S = Σ wᵢsᵢ ≥ θ, and show that AND is the case k = n.'}
  - {th: เขียนประตูยืนยันจากเซนเซอร์ดิบ gmag = |gx| + |gy| + |gz| > MOTION_FLOOR และเงื่อนไข fused = model_hit and raw_ok พร้อม edge-trigger, en: Write a raw-sensor gate gmag = |gx| + |gy| + |gz| > MOTION_FLOOR and the condition fused = model_hit and raw_ok with an edge trigger.}
develops: [{skill: ai.edge, to: 3}, {skill: sys.sensors-actuators, to: 3}, {skill: hw.math, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 6.5 — sensor fusion: verdict ของโมเดลกับเซนเซอร์ดิบ

> โมดูล 6 — แอป Edge AI · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

ทำให้การตัดสินใจเชื่อถือได้ขึ้นด้วย sensor fusion เอา verdict ของโมเดล (บอกว่าเป็นอะไร) มายืนยันกับเซนเซอร์ดิบ (บอกว่าแรงแค่ไหน) เข้าใจ corroboration แบบ AND กับ majority vote แบบ k จาก n ผ่านสูตรถ่วงน้ำหนักเดียวกัน และเห็นตัวอย่างระบบกันขโมยสามเซนเซอร์

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. อธิบายได้ว่าทำไม verdict ของโมเดลเดี่ยวยังไม่พอ และโมเดลกับเซนเซอร์ดิบตอบคนละคำถามอย่างไร
2. คำนวณการตัดสินแบบโหวต k จาก n และแบบถ่วงน้ำหนัก S = Σ wᵢsᵢ ≥ θ ได้ และแสดงว่า AND คือกรณี k = n
3. เขียนประตูยืนยันจากเซนเซอร์ดิบ gmag = |gx| + |gy| + |gz| > MOTION_FLOOR และเงื่อนไข fused = model_hit and raw_ok พร้อม edge-trigger

## ก่อนเริ่ม

ผ่านชุดบทเรียน 6.3–6.4 มาแล้ว มีท่อสั่งการที่กัน false positive และจำ rule classifier จากบทเรียน 3.3 ได้
เปิดตัวอย่าง `10_motion_alarm.py` ไว้ใน BENTO IDE

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — บน Emulator แผง HW ขยับเฉพาะ accel (ลากเอียงและปุ่ม Shake) gyro ค้างใกล้ศูนย์ และตัวอย่าง 10 ที่เปิดไมโครโฟน PDM รันบน TESAIoT Dev Kit ยังไม่ได้ (ใช้ได้บน Emulator กับ PSoC Edge AI Kit)
- **เรียนมาก่อน:** [บทเรียน 6.4 — ลงมือทำ: action pipeline ที่กัน false positive](../l04-action-pipeline-lab/README.md)

## ดูของจริงก่อน

รัน `10_motion_alarm.py` กดสวิตช์ Arm แล้วลองให้เซนเซอร์ไหวทีละตัว กับหลายตัวพร้อมกัน สังเกตว่ามันไม่ปลุกทุกครั้งที่เซนเซอร์ตัวเดียวไหว
ต้องโหวตสองในสามก่อนจึงขึ้น `!! INTRUDER !!` (บน Emulator ปุ่ม Shake ทำให้เรดาร์โหวตได้ แต่ IMU ของตัวอย่างนี้ดู gyro ซึ่ง Emulator ค้างใกล้ศูนย์)

## แนวคิด

โมเดลเดาผิดได้ด้วยความมั่นใจพอสมควร เช่นตอบ `shaking` 62% ตอนแค่วางบอร์ดแรงไปหน่อย **sensor fusion** รวมหลายแหล่งเป็นการตัดสินใจเดียวที่ดีกว่า
โมเดล (`edge_ai`, รันบน CM55 กับ NPU) ตอบว่า **"นี่คืออะไร"** เป็นความน่าจะเป็น ส่วนเซนเซอร์ดิบ (`sensors`, อ่านจาก Python บน CM33) ตอบว่า
**"แรงแค่ไหน"** เป็นหน่วยฟิสิกส์ แต่ละตัวพลาดคนละแบบ เอามาค้ำกันจึงทน false positive มากขึ้น แบบเดียวกับรถยนต์ที่ใช้กล้อง เรดาร์ และ lidar ก่อนเบรก

fusion ที่ใช้บ่อยมีสองรส **corroboration (AND)** สัญญาณหลักหนึ่งตัวกับประตูยืนยันหนึ่งตัว ยิงเมื่อผ่านทั้งคู่ เหมาะกับ "อย่าปลุกถ้าไม่ชัวร์"
และ **majority vote** $\text{fire} = [\sum_{i=1}^{n} s_i \ge k]$ อย่าง `10_motion_alarm.py` ที่โหวตสองในสามจากเรดาร์ IMU และไมค์ ยอมให้เซนเซอร์ตัวหนึ่งพลาดได้
ทั้งสองคือสูตรเดียวกัน $S = \sum w_i s_i$ และ $\text{fire} = [S \ge \theta]$ เมื่อ $w_i = 1$ และ $\theta = n$ ก็คือ AND ลด $\theta$ ลงก็ผ่อนเป็นโหวต
เพิ่ม $w_i$ ของตัวที่ไว้ใจก็ให้มันมีเสียงดังขึ้น

ประตูยืนยันของเราคือ rule classifier จากบทเรียน 3.3: `ax, ay, az, gx, gy, gz = sensors.bmi270.motion()` (accel หน่วย m/s² และ gyro หน่วย deg/s)
แล้ว `gmag = abs(gx) + abs(gy) + abs(gz)` กับ `raw_ok = gmag > MOTION_FLOOR` (ค่าตั้งต้น 40) รวมเป็น
`fused = model_hit and raw_ok` โดย `model_hit = r['label'] == TARGET_CLASS and r['conf'] >= edge_ai.CONF_FLOOR` แล้วยิงเหตุการณ์ตอนขอบขาขึ้นด้วยธง `fired`
เพื่อไม่ส่งซ้ำทุกเฟรม เขย่าแรงแต่โมเดลตอบ `idle` ก็ไม่ยิง โมเดลตอบ `shaking` แต่ gyro เบาก็ไม่ยิง

## ตัวอย่างสมบูรณ์

`10_motion_alarm.py` ระบบกันขโมยสามเซนเซอร์ (เรดาร์ `sensors.radar()["presence"]`, IMU และระดับเสียงจาก PDM) กับสวิตช์ Arm บนจอ
เป็น state machine DISARMED → ARMED → TRIGGERED ที่โหวตสองในสาม และอัปเดตจอเฉพาะตอนสถานะเปลี่ยน หัวไฟล์บอกไว้ว่าบน TESAIoT Dev Kit
การเปิด PDM ยังชนกับ clock ของระบบเสียง จึงใช้ได้บน PSoC Edge AI Kit และ Emulator

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/10_motion_alarm.py](examples/10_motion_alarm.py) | ระบบกันขโมย 3 เซนเซอร์ + สวิตช์ arm/disarm บนจอ |

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นหรือใน `shared/` ด้วย:

- [m01-onboarding/l07-verdict-action-lab/solution/s03_anatomy_edgeai.py](../../m01-onboarding/l07-verdict-action-lab/solution/s03_anatomy_edgeai.py) — แกะแอป Edge AI แล้ว remix: สลับโมเดล + สั่งการเมื่อเจอคลาส
- [m06-apps/l06-fusion-iot-lab/practice/s17_fusion_iot.py](../l06-fusion-iot-lab/practice/s17_fusion_iot.py) — รวม verdict ของโมเดลกับเซนเซอร์ดิบ แล้วสตรีมขึ้นคลาวด์ (ฉบับฝึกเติมโค้ด)

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. ข้อใดบรรยายหน้าที่ของโมเดลกับเซนเซอร์ดิบใน fusion ได้ถูกต้อง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) โมเดลบอกว่านี่คืออะไร (ความน่าจะเป็น) เซนเซอร์ดิบบอกว่าแรงแค่ไหน (หน่วยฟิสิกส์)
   - ข) ทั้งคู่บอกสิ่งเดียวกัน จึงใช้แทนกันได้
   - ค) เซนเซอร์ดิบแม่นกว่าโมเดลเสมอ
   - ง) โมเดลอ่านค่าฟิสิกส์ได้ดีกว่าเซนเซอร์ดิบ

   <details><summary>เฉลย</summary>

   **ก** — สองแหล่งตอบคนละคำถามและพลาดคนละแบบ เอามายืนยันกันจึงกัน false positive ได้

   </details>

2. ระบบโหวตสองในสาม เรดาร์เห็น IMU เงียบ ไมค์เห็น ผลคืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) ไม่ปลุก เพราะ IMU เงียบ
   - ข) ปลุก เพราะผลรวม 2 ≥ k = 2
   - ค) ไม่แน่นอน
   - ง) ปลุกก็ต่อเมื่อทั้งสามเห็น

   <details><summary>เฉลย</summary>

   **ข** — Σsᵢ = 1 + 0 + 1 = 2 ผ่านเกณฑ์ k = 2 การโหวตยอมให้เซนเซอร์ตัวหนึ่งพลาดได้ ถ้าต้องครบทั้งสามคือ k = n = AND

   </details>

3. สองสัญญาณ น้ำหนักเท่ากัน wᵢ = 1 ตั้ง θ เท่าไรจึงเท่ากับ AND *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) θ = 0
   - ข) θ = 1
   - ค) θ = 2
   - ง) θ = 0.5

   <details><summary>เฉลย</summary>

   **ค** — θ เท่าผลรวมน้ำหนักคือต้องผ่านทุกตัว ถ้า θ = 1 จะกลายเป็น OR ผ่านตัวเดียวก็ยิง

   </details>

4. โมเดลตอบ shaking ที่ conf 0.8 แต่ gx, gy, gz = 5, 10, 8 และ MOTION_FLOOR = 40 ค่า fused เป็นอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) True เพราะโมเดลมั่นใจ
   - ข) False เพราะ gmag = 23 ไม่เกิน 40 ประตูดิบไม่ผ่าน
   - ค) True เพราะ gmag > 0
   - ง) error

   <details><summary>เฉลย</summary>

   **ข** — fusion ใช้ AND ด่านเดียวไม่ผ่านก็ไม่ยิง นี่คือ false positive ของโมเดลที่ fusion กรองออก

   </details>

## แล็บ

- [ ] รัน `10_motion_alarm.py` (บน PSoC Edge AI Kit หรือ Emulator) แล้วจดว่าการกระทำแบบใดทำให้เซนเซอร์ใดโหวต และแบบใดไม่ปลุก
- [ ] คำนวณ S และผลการยิงของสามกรณีในบันทึกการเรียน โดยให้น้ำหนักเรดาร์ 2 IMU 1 ไมค์ 1 และ θ = 3
- [ ] เขียนเงื่อนไข fused ด้วยมือ แล้วระบุหนึ่งท่าที่โมเดลน่าจะตอบ shaking แต่ประตู gyro ไม่ผ่าน

## ไปต่อ

บทเรียน 6.6 เราจะเติม `s17_fusion_iot.py` ให้ fuse verdict กับ gyro ดิบ แล้วส่งเหตุการณ์ขึ้น MQTT broker ผ่าน WiFi

บทเรียนถัดไป: [บทเรียน 6.6 — ลงมือทำ: ส่งเหตุการณ์ที่ fuse แล้วขึ้น MQTT](../l06-fusion-iot-lab/README.md)

## สะท้อนคิด

- ระบบรอบตัวคุณระบบไหนควรใช้ AND และระบบไหนควรใช้โหวต เพราะพลาดแบบไหนแพงกว่า
- ถ้าเซนเซอร์ตัวหนึ่งในระบบโหวตเสียถาวร ระบบจะเปลี่ยนพฤติกรรมอย่างไร
