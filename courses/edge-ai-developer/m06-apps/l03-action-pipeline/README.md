---
id: edgeai-dev.m06.l03
lang: th
title: {th: 'ท่อสั่งการ: CONF_FLOOR, debounce, cooldown และ on_result', en: 'The action pipeline: CONF_FLOOR, debounce, cooldown and on_result'}
summary: {th: 'เปลี่ยนการนับเป็นการสั่งการจริงอย่างมีวินัยด้วยท่อสี่ด่าน คือกรองด้วย CONF_FLOOR, debounce ที่ต้องจับต่อเนื่อง, cooldown ที่เว้นช่วงกันยิงรัว และ action ผ่านไฟ RGB เสียงและ log เสริมด้วย EMA smoothing คณิตของการยิงตอนขอบขึ้น และการเลือกระหว่าง poll กับ on_result', en: 'Turn counting into disciplined action with a four-stage pipeline - a CONF_FLOOR filter, a debounce that needs a streak, a cooldown against rapid re-firing, and the action itself through an RGB light, sound and a log - plus EMA smoothing, the maths of firing on the rising edge, and choosing between polling and on_result.'}
level: L3
time_min: {concept: 50, practise: 10, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m06.l02]
objectives:
  - {th: อธิบายท่อสี่ด่าน (กรอง → debounce → cooldown → action) และบอกได้ว่าแต่ละด่านกัน false positive แบบใด, en: Describe the four-stage pipeline (filter → debounce → cooldown → action) and say which kind of false positive each stage stops.}
  - {th: 'คำนวณ EMA หนึ่งก้าวด้วยมือจาก y_t = αx_t + (1 − α)y_{t−1} และอธิบายว่าทำไมมันกดยอดแหลมเดี่ยวได้โดยเก็บสถานะแค่ค่าเดียว', en: 'Compute one EMA step by hand from y_t = αx_t + (1 − α)y_{t−1}, and explain why it flattens single spikes while keeping only one state value.'}
  - {th: 'ใช้เงื่อนไขยิง fire = [c_t ≥ H] ∧ [c_{t−1} < H] ∧ [t − t_last ≥ T_cool] กับลำดับเฟรมที่กำหนด และอธิบายว่าทำไมต้องวัดเวลาด้วย ticks_diff', en: 'Apply the firing rule fire = [c_t ≥ H] ∧ [c_{t−1} < H] ∧ [t − t_last ≥ T_cool] to a given frame sequence, and explain why time must be measured with ticks_diff.'}
  - {th: เลือกระหว่าง poll ด้วย result() กับ callback ด้วย on_result() ให้งานที่กำหนด โดยรู้ว่า callback มาเมื่อคลาสเปลี่ยนและทวนคลาสเดิมราววินาทีละครั้ง, en: 'Choose between polling result() and an on_result() callback for a given task, knowing the callback arrives on a class change and repeats the same class about once a second.'}
develops: [{skill: ai.edge, to: 3}, {skill: sys.dsp, to: 2}, {skill: prog.state-machines, to: 2}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 6.3 — ท่อสั่งการ: CONF_FLOOR, debounce, cooldown และ on_result

> โมดูล 6 — แอป Edge AI · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เปลี่ยนการนับเป็นการสั่งการจริงอย่างมีวินัยด้วยท่อสี่ด่าน คือกรองด้วย CONF_FLOOR, debounce ที่ต้องจับต่อเนื่อง, cooldown ที่เว้นช่วงกันยิงรัว และ action ผ่านไฟ RGB เสียงและ log เสริมด้วย EMA smoothing คณิตของการยิงตอนขอบขึ้น และการเลือกระหว่าง poll กับ on_result

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. อธิบายท่อสี่ด่าน (กรอง → debounce → cooldown → action) และบอกได้ว่าแต่ละด่านกัน false positive แบบใด
2. คำนวณ EMA หนึ่งก้าวด้วยมือจาก y_t = αx_t + (1 − α)y_{t−1} และอธิบายว่าทำไมมันกดยอดแหลมเดี่ยวได้โดยเก็บสถานะแค่ค่าเดียว
3. ใช้เงื่อนไขยิง fire = [c_t ≥ H] ∧ [c_{t−1} < H] ∧ [t − t_last ≥ T_cool] กับลำดับเฟรมที่กำหนด และอธิบายว่าทำไมต้องวัดเวลาด้วย ticks_diff
4. เลือกระหว่าง poll ด้วย result() กับ callback ด้วย on_result() ให้งานที่กำหนด โดยรู้ว่า callback มาเมื่อคลาสเปลี่ยนและทวนคลาสเดิมราววินาทีละครั้ง

## ก่อนเริ่ม

ผ่านชุดบทเรียน 6.1–6.2 มาแล้ว มีแอปนับที่ใช้ CONF_FLOOR และขอบขาขึ้น และจำ `dsp.EMA` จากบทเรียน 4.1 ได้
เปิดตัวอย่าง `20_confirmed_alert.py` ไว้ใน BENTO IDE

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — บน Emulator ใช้โมเดล Motion กับปุ่ม Shake ซ้อมท่อได้ครบ (โมเดลเสียงบน Emulator เป็นค่าจำลองที่คลาสเหตุการณ์ไม่ชนะ) และ callback ของ on_result จะมาเมื่อโปรแกรมเรียก result() หรือ active()
- **เรียนมาก่อน:** [บทเรียน 6.2 — ลงมือทำ: แอปโฟกัสของเราเอง](../l02-focused-app-lab/README.md)

## ดูของจริงก่อน

รัน `s16_action_pipeline_full.py` (อยู่ในบทเรียน 6.4) เลือกโมเดล Cough แล้วลองไอ ไฟบนจอไล่จากฟ้า (เฝ้าดู) เป็นเหลือง (เจอแต่ยังไม่ชัวร์) แล้วค่อยเป็นแดง (ยิง)
สังเกตว่าไอแวบเดียวสั้น ๆ ไม่ยิงทันที แล้วถามว่ามันรู้ได้อย่างไรว่าอันไหนของจริง

## แนวคิด

verdict ดิบเชื่อทั้งดุ้นไม่ได้ โมเดลกระพริบเกินเส้นชั่ววูบได้เสมอ ถ้ายิงทุกเฟรมที่ `label == "cough"` จะเตือนผิดบ่อยจนคนเลิกสนใจ
ปัญหาเดียวกับ switch bounce ของปุ่มกด เราจึงวาง **ท่อสี่ด่าน**: (1) **กรอง** `hit = r['label'] == TARGET_CLASS and r['conf'] >= edge_ai.CONF_FLOOR`
ตัดคำตอบที่ไม่มั่นใจ (2) **debounce** `streak += 1` เมื่อ hit และ `streak = 0` ทันทีที่หลุด ต้องครบ `NEED_HITS` จึงพร้อม ยอดแหลมเดี่ยวผ่านไม่ได้เพราะไม่ค้าง
(3) **cooldown** `time.ticks_diff(now, last_fire) >= COOLDOWN_MS` กันยิงรัวตอนเหตุการณ์ค้างยาว ใช้ `ticks_diff` เสมอเพราะตัวนับ ms วนกลับได้
(4) **action** ใน `fire_action()` ที่แยกไว้ต่างหาก: การ์ดสีบนจอแทนไฟ RGB (ฟ้า เหลือง แดง), `ui.tone(note, wave, velocity, dur_ms)` หรือ `ui.sfx(...)`
ห่อด้วย `hasattr` และ log ผ่าน `lcd.console` พร้อมเวลาและความมั่นใจ

เกราะเสริมคือ **EMA** $y_t = \alpha x_t + (1-\alpha) y_{t-1}$ ที่ $\alpha = 0.35$ ถ้า $y_{t-1} = 0.20$ แล้วยอดแหลม $x_t = 0.90$ โผล่มา ได้ $y_t = 0.445$ ยังไม่ถึง 0.50
ต้องสูงจริงหลายเฟรมจึงไต่ข้ามเส้น และเก็บสถานะแค่ค่าเดียว debounce นับจำนวนเฟรม ส่วน smoothing กดขนาดของค่า ใช้คู่กันยิ่งแน่น
เขียนเป็นคณิตได้ว่า $c_t = c_{t-1} + 1$ เมื่อ hit และ $c_t = 0$ เมื่อพลาด แล้วยิงเมื่อ $[c_t \ge H] \wedge [c_{t-1} < H] \wedge [t - t_{last} \ge T_{cool}]$
คือยิงตอนความพร้อมเพิ่งครบ ครั้งเดียวต่อหนึ่งเหตุการณ์ แบบเดียวกับ edge-triggered interrupt

การรับผลมีสองแบบ **poll** คือเรียก `result()` เองทุกรอบ ได้ทุกเฟรมจึงนับ streak ได้ ส่วน **`edge_ai.on_result(cb)`** ให้เฟิร์มแวร์เรียกเราทันทีที่คลาสที่ชนะเปลี่ยน
และทวนคลาสเดิมราววินาทีละครั้ง จึงเหมาะกับการ log การเปลี่ยนคลาส (จำคลาสล่าสุดไว้แล้วข้ามรอบที่ทวน) แต่ไม่เหมาะกับ debounce
งานที่ต้องนับเฟรมหรือเวลาใช้ poll งานที่แค่ตอบสนองต่อเหตุการณ์ใช้ callback และถอนด้วย `edge_ai.on_result(None)` ตอนจบเสมอ

## ตัวอย่างสมบูรณ์

`19_motion_verdict_action.py` ใช้ป้าย ความมั่นใจ และเวลาอนุมานพร้อมกันก่อนสั่งเสียง (เกณฑ์ `CONF = 0.70`) และ `20_confirmed_alert.py`
ยืนยัน `CONFIRM_N = 4` รอบติดกันก่อนเชื่อ แล้วเว้น `ALERT_GAP_MS = 8000` ก่อนเตือนซ้ำ ซึ่งคือท่อแบบเดียวกันด้วยตัวเลขอีกชุด (ทั้งสองไฟล์ย้ายมาจากคอร์ส AIoT ของผู้เขียน)

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/19_motion_verdict_action.py](examples/19_motion_verdict_action.py) | ท่าทางสั่งงาน และราคาของแต่ละคำตัดสิน |
| [examples/20_confirmed_alert.py](examples/20_confirmed_alert.py) | ให้โมเดลเป็นแหล่งค่า แล้วยืนยันก่อนเตือน |

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นหรือใน `shared/` ด้วย:

- [m06-apps/l04-action-pipeline-lab/examples/s16_action_pipeline_full.py](../l04-action-pipeline-lab/examples/s16_action_pipeline_full.py) — action pipeline ครบวง: กรอง + smooth + debounce + action (ฉบับเต็ม)
- [m06-apps/l04-action-pipeline-lab/practice/s16_action_pipeline.py](../l04-action-pipeline-lab/practice/s16_action_pipeline.py) — จาก verdict สู่ action จริง: RGB + เสียง + log (ฉบับฝึกเติมโค้ด)

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. คลาส cough กระโดดขึ้นเหนือ CONF_FLOOR เพียงเฟรมเดียวแล้วตกลง ด่านใดกันไม่ให้ยิง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) ด่านกรอง
   - ข) ด่าน debounce เพราะ streak ไม่ถึง NEED_HITS แล้วรีเซ็ตเป็น 0
   - ค) ด่าน cooldown
   - ง) ด่าน action

   <details><summary>เฉลย</summary>

   **ข** — ยอดแหลมที่สูงพอผ่านด่านกรองได้ แต่ไม่ค้างต่อเนื่อง streak จึงไม่ครบ ส่วน cooldown มีไว้กันการยิงรัวตอนเหตุการณ์จริงค้างยาว

   </details>

2. EMA ที่ α = 0.35 ค่าเดิม y = 0.20 เจอค่าใหม่ x = 0.90 ได้ y ใหม่เท่าไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) 0.90
   - ข) 0.55
   - ค) 0.445
   - ง) 0.315

   <details><summary>เฉลย</summary>

   **ค** — 0.35 × 0.90 + 0.65 × 0.20 = 0.315 + 0.130 = 0.445 ยอดแหลมถูกกดจนยังไม่ข้ามเกณฑ์ 0.50

   </details>

3. NEED_HITS = 3 และพ้น cooldown แล้ว ลำดับเฟรม hit, hit, hit, hit, hit จะยิงกี่ครั้ง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) 0
   - ข) 1 ครั้ง ที่เฟรมที่สาม
   - ค) 3 ครั้ง
   - ง) 5 ครั้ง

   <details><summary>เฉลย</summary>

   **ข** — ยิงเมื่อ c_t ถึง 3 เป็นครั้งแรก (c_{t−1} = 2 < 3) เฟรมถัดไป c_{t−1} ครบแล้วจึงไม่ยิงซ้ำ และ cooldown เริ่มนับใหม่ด้วย

   </details>

4. ทำไมต้องใช้ time.ticks_diff(now, last_fire) แทน now − last_fire *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) เร็วกว่า
   - ข) ตัวนับ ticks_ms วนกลับได้ ticks_diff จัดการการวนกลับให้ผลต่างยังถูก
   - ค) ได้หน่วยวินาที
   - ง) ไม่มีความต่าง

   <details><summary>เฉลย</summary>

   **ข** — เมื่อตัวนับเต็มแล้ววนกลับ การลบตรง ๆ จะได้ค่าติดลบหรือผิด ticks_diff ออกแบบมาเพื่อกรณีนี้

   </details>

5. งานใดเหมาะกับ edge_ai.on_result(cb) มากที่สุด *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) นับ streak ต่อเฟรมเพื่อ debounce
   - ข) log เมื่อคลาสที่ชนะเปลี่ยน โดยจำคลาสล่าสุดไว้เพื่อข้ามรอบที่เฟิร์มแวร์ทวนคลาสเดิม
   - ค) วัด latency ทุกเฟรม
   - ง) smoothing ด้วย EMA ทุกเฟรม

   <details><summary>เฉลย</summary>

   **ข** — callback มาตอนคลาสเปลี่ยนและทวนราววินาทีละครั้ง ไม่ได้มาทุกเฟรม งานที่ต้องนับเฟรมจึงควรใช้ poll

   </details>

## แล็บ

- [ ] รัน `20_confirmed_alert.py` บน Emulator ด้วยโมเดล Motion กดปุ่ม Shake สั้น ๆ กับค้างยาว แล้วจดว่าป้ายสถานะที่ยืนยันแล้วเปลี่ยนเมื่อไร
- [ ] คำนวณ EMA ต่อจากตัวอย่างอีกสามเฟรมเมื่อ x = 0.90 ค้างไว้ แล้วดูว่าเฟรมใดข้าม 0.50
- [ ] เขียนลำดับ hit/miss สิบเฟรมที่มีทั้งยอดแหลมเดี่ยวและเหตุการณ์จริง แล้วทำเครื่องหมายเฟรมที่ยิงเมื่อ NEED_HITS = 3

## ไปต่อ

บทเรียน 6.4 เราจะเติมสี่ด่านของท่อใน `s16_action_pipeline.py` แล้วจูน `NEED_HITS` กับ `COOLDOWN_MS` จนกัน false positive ได้จริง

บทเรียนถัดไป: [บทเรียน 6.4 — ลงมือทำ: action pipeline ที่กัน false positive](../l04-action-pipeline-lab/README.md)

## สะท้อนคิด

- งานไหนที่การพลาดของจริง (false negative) แพงกว่าการเตือนผิด และคุณจะจูนท่อไปทางไหน
- ถ้าใช้ on_result ทำ debounce แทน poll จะเกิดปัญหาอะไร
