---
id: edgeai-dev.m03.l04
lang: th
title: {th: 'ลงมือทำ: ตัวจำแนกความสบายด้วยกฎ', en: 'Hands-on: a rule-based comfort classifier'}
summary: {th: เติม s07_rule_classifier.py ให้คำนวณ dew point กับ heat index เขียนบันไดกฎหกชั้นใน classify() และระบายสีคำตัดสินบนจอ แล้วเทียบกับ dsp.comfort_zone พร้อมเห็นจุดแข็งเรื่องอธิบายได้และข้อจำกัดที่ปูทางไปสู่ ML, en: 'Complete s07_rule_classifier.py so it computes dew point and heat index, write a six-step ladder in classify(), colour the verdict on screen, and compare it with dsp.comfort_zone while seeing the explainability strength and the limits that lead to ML.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m03.l03]
objectives:
  - {th: เติมสี่ช่องใน practice/s07_rule_classifier.py จนการ์ดคำตัดสินเปลี่ยนคำและสีตามอุณหภูมิกับความชื้นจริง และทำให้เกิดคลาสต่างกันอย่างน้อยสามคลาส, en: 'Fill the four blanks in practice/s07_rule_classifier.py until the verdict card changes word and colour with real temperature and humidity, producing at least three different classes.'}
  - {th: ปรับเส้นแบ่งหนึ่งเส้นแล้วอธิบายได้ว่าคำตัดสินที่ค่าใกล้เส้นเปลี่ยนไปอย่างไร และทำไมคำตัดสินของเราอาจไม่ตรงกับ dsp.comfort_zone โดยไม่แปลว่าผิด, en: 'Adjust one threshold and explain how verdicts near that line change, and why your verdict may disagree with dsp.comfort_zone without being wrong.'}
  - {th: อธิบายจุดแข็งด้านความอธิบายได้ของกฎ (rule trace) และข้อจำกัดสามข้อของกฎมือที่เป็นแรงจูงใจของ ML, en: Explain the explainability strength of rules (the rule trace) and three limits of hand-written rules that motivate ML.}
develops: [{skill: prog.algo-ds, to: 2}, {skill: lang.micropython, to: 2}, {skill: gui.hmi, to: 2}, {skill: ai.edge, to: 1}]
assesses: [{skill: prog.algo-ds, level: 2, evidence: practice/s07_rule_classifier.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 3.4 — ลงมือทำ: ตัวจำแนกความสบายด้วยกฎ

> โมดูล 3 — ประมวลผลด้วยคณิตศาสตร์และฟิสิกส์ · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เติม s07_rule_classifier.py ให้คำนวณ dew point กับ heat index เขียนบันไดกฎหกชั้นใน classify() และระบายสีคำตัดสินบนจอ แล้วเทียบกับ dsp.comfort_zone พร้อมเห็นจุดแข็งเรื่องอธิบายได้และข้อจำกัดที่ปูทางไปสู่ ML

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เติมสี่ช่องใน practice/s07_rule_classifier.py จนการ์ดคำตัดสินเปลี่ยนคำและสีตามอุณหภูมิกับความชื้นจริง และทำให้เกิดคลาสต่างกันอย่างน้อยสามคลาส
2. ปรับเส้นแบ่งหนึ่งเส้นแล้วอธิบายได้ว่าคำตัดสินที่ค่าใกล้เส้นเปลี่ยนไปอย่างไร และทำไมคำตัดสินของเราอาจไม่ตรงกับ dsp.comfort_zone โดยไม่แปลว่าผิด
3. อธิบายจุดแข็งด้านความอธิบายได้ของกฎ (rule trace) และข้อจำกัดสามข้อของกฎมือที่เป็นแรงจูงใจของ ML

## ก่อนเริ่ม

ผ่านบทเรียน 3.3 มาแล้ว รู้ว่าบันไดกฎต้องเรียงจากรุนแรงไปกว้าง
ถ้าใช้บอร์ด เตรียมวิธีเปลี่ยนอากาศรอบเซนเซอร์: หายใจรด กำบอร์ดไว้ในมือ หรือพาไปใกล้แอร์

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — ต้องมี SHT40 และ DPS368 (มีบน TESAIoT Dev Kit ไม่มีบน Eva Kit) ส่วน Emulator จำลองค่าให้และคำนวณ dsp ด้วยสูตรจริง
- **เรียนมาก่อน:** [บทเรียน 3.3 — ค่าอนุพัทธ์และการจำแนกด้วยกฎ: dew point, heat index และบันไดกฎ](../l03-rules-before-ml/README.md)

## แนวคิด

ในลูปมีสี่ก้าว: **อ่านค่าดิบ → แปลงเป็น derived → ตัดสินด้วยกฎ → วาดคลาส** ส่วนอ่านค่าดิบให้ไว้แล้ว
(`p, t = sensors.dps368.pressure_temperature()` และ `h = sensors.sht40.humidity()` ที่คืน %RH ค่าเดียว) ช่องเติมสี่จุดคือ
(1) `dp = dsp.dew_point(t, h)` (2) `hi = dsp.heat_index(t, h)` (3) บันไดกฎใน `classify()` ไล่ `danger` (hi ≥ 41) → `hot` (hi ≥ 32)
→ `humid` (h ≥ 70) → `cold` (t < 20) → `dry` (h < 30) → `comfortable` และ (4) `verdict.text(zone)` กับ
`verdict.color(COLORS.get(zone, WHITE))` ค่าตั้งต้น `dp = 0.0` และ `hi = t` กันโปรแกรมพังตอนยังเติมไม่ครบ
ถ้าลืมช่อง 3 `classify()` คืน `None` การ์ดจะว่างและเป็นสีขาว

ท่อนท้ายที่ให้ไว้แล้วแสดง `dsp.comfort_zone(t, h)` ไว้เทียบ คำตัดสินอาจไม่ตรงกันเพราะสองกฎนิยามความสบายต่างกัน (ของเราใช้ heat index
ของเฟิร์มแวร์ใช้อุณหภูมิดิบ และเลขเส้นต่างกัน) ไม่มีชุดไหน "ถูก" โดยสมบูรณ์ กฎขึ้นกับนิยามที่เลือก ซึ่งเป็นข้อจำกัดที่ ML จะเข้ามาช่วยด้วยข้อมูลจริง

จุดแข็งที่สุดของบันไดกฎคือทุกคำตัดสินสืบย้อนได้ว่าชั้นไหนยิง ฉบับเต็มให้ `classify()` คืนเหตุผลด้วย เช่น `why: feels-like 43 >= 41`
นี่คือ explainability ที่งานความปลอดภัยและการแพทย์ต้องการ แต่กฎมือชนกำแพงสามข้อ: กฎบานเมื่อ feature เยอะ, เส้นที่มนุษย์ตั้งอาจไม่ดีที่สุด,
และไม่ปรับตามข้อมูลใหม่ ความรู้สึกว่า "ถ้าเงื่อนไขเยอะกว่านี้ เขียน `if` ไม่ไหวแน่" คือแรงจูงใจที่แท้จริงของ ML ในโมดูล 5

## ตัวอย่างสมบูรณ์

`s07_rule_classifier_full.py` เพิ่ม rule trace (`why`) ไฟบอกว่าตรงหรือต่างจาก `dsp.comfort_zone` และฮิสเทอรีซิสกันคลาสกระพริบ
เมื่อค่าวัดสั่นคร่อมเส้นแบ่ง ลองเปิดอ่านหลังเติมไฟล์ฝึกเสร็จ

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/s07_rule_classifier_full.py](examples/s07_rule_classifier_full.py) | จำแนกสภาพอากาศด้วยกฎ (ฉบับเต็ม) |

## ฝึกเติม

คอมเมนต์ `# เติม:` อยู่ที่บรรทัด 43 (บันไดกฎใน `classify()`), 91 (dew point), 94 (heat index) และ 106–107 (ขึ้นจอพร้อมสี)
เติมทีละช่องแล้วรัน ถ้าคลาสไม่เปลี่ยน ให้ตรวจการเยื้องบรรทัดและลำดับชั้นของบันได

| ไฟล์ฝึก | เรื่อง |
|---|---|
| [practice/s07_rule_classifier.py](practice/s07_rule_classifier.py) | จำแนกสภาพอากาศด้วย "กฎ" ที่เราเขียนเอง (ฉบับฝึกเติมโค้ด) |

## เฉลย

เปิดเฉลยหลังจากลองเองแล้วอย่างน้อยหนึ่งรอบ และอ่าน [วิธีใช้เฉลย](../../README.md#วิธีใช้เฉลย) ก่อน

| เฉลย | คู่กับ |
|---|---|
| [solution/s07_rule_classifier.py](solution/s07_rule_classifier.py) | [practice/s07_rule_classifier.py](practice/s07_rule_classifier.py) |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. เรียงสี่ก้าวในลูปของ s07_rule_classifier.py *(เรียงลำดับ · เป้าหมายข้อ 1)*
   - ก) ตัดสินด้วยกฎ: zone = classify(t, h, hi)
   - ข) อ่านค่าดิบ: dps368 และ sht40
   - ค) วาดคลาส: verdict.text และ verdict.color
   - ง) แปลงเป็น derived: dew_point และ heat_index

   <details><summary>เฉลย</summary>

   **ข → ง → ก → ค** — อ่าน → แปลง → ตัดสิน → วาด เป็น pipeline ย่อของ classifier ทั้งตัว ช่องเติม 1–2 คือก้าวแปลง 3 คือก้าวตัดสิน 4 คือก้าววาด

   </details>

2. รันแล้วการ์ดคำตัดสินว่างเปล่าและเป็นสีขาวตลอด สาเหตุที่น่าจะเป็นที่สุดคืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) ยังไม่ได้เติมบันไดใน classify() ฟังก์ชันจึงคืน None และ COLORS.get(None, WHITE) ได้สีขาว
   - ข) SHT40 ไม่ได้ต่อ
   - ค) heat index สูงเกินไป
   - ง) Emulator ไม่รองรับ ui.Seg7

   <details><summary>เฉลย</summary>

   **ก** — คลาสที่ไม่อยู่ใน COLORS จะได้สีขาวเป็นค่าสำรอง อาการนี้บอกว่าบันไดยังไม่ทำงาน

   </details>

3. คำตัดสินของ classify() เป็น comfortable แต่ dsp.comfort_zone ตอบ acceptable ควรสรุปอย่างไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) classify() ผิดแน่นอน
   - ข) dsp.comfort_zone ผิดแน่นอน
   - ค) สองกฎนิยามความสบายต่างกัน (ใช้ค่าและเส้นแบ่งต่างกัน) ไม่ตรงกันไม่ได้แปลว่าผิด
   - ง) เซนเซอร์อ่านค่าไม่ตรงกัน

   <details><summary>เฉลย</summary>

   **ค** — ของเราตัดสินจาก heat index ส่วนของเฟิร์มแวร์ตัดสินจากอุณหภูมิดิบกับช่วงของตัวเอง กฎขึ้นกับนิยามที่เลือก

   </details>

4. ข้อใดเป็นข้อจำกัดของกฎมือที่ทำให้ต้องไปต่อที่ ML (เลือกทุกข้อที่ถูก) *(เลือกได้หลายข้อ · เป้าหมายข้อ 3)*
   - ก) กฎบานจนเขียนไม่ไหวเมื่อมี feature หลายสิบตัว
   - ข) เส้นแบ่งที่มนุษย์ตั้งอาจไม่ใช่เส้นที่ดีที่สุดสำหรับข้อมูลจริง
   - ค) กฎไม่ปรับตามข้อมูลใหม่เอง
   - ง) กฎอธิบายคำตัดสินไม่ได้

   <details><summary>เฉลย</summary>

   **ก, ข, ค** — ความอธิบายได้เป็นจุดแข็งของกฎ ไม่ใช่ข้อจำกัด rule trace บอกได้เสมอว่าชั้นไหนยิงคำตัดสิน

   </details>

## แล็บ

**MVP ของชุดบทเรียน 3.3–3.4:** เขียน `classify()` ด้วยบันไดกฎเอง แล้วบอร์ดหรือ Emulator โชว์คลาสที่เปลี่ยนตามจริงเมื่ออุณหภูมิหรือความชื้นเปลี่ยน
โดยใช้ค่าอนุพัทธ์อย่างน้อยหนึ่งตัวในการตัดสิน

- [ ] เติมไฟล์ฝึกครบสี่ช่อง รันได้บน Emulator หรือบอร์ด
- [ ] ทำให้เกิดอย่างน้อยสามคลาส (เช่น หายใจรด → `humid`, กำบอร์ด → `hot`, ปกติ → `comfortable`) แล้วจดวิธีลงบันทึกการเรียน
- [ ] ปรับเส้นแบ่งหนึ่งเส้น (เช่น `hi >= 32` เป็น `>= 30`) หาค่าที่คร่อมเส้นแล้วอธิบายว่าคำตัดสินเปลี่ยนอย่างไร
- [ ] ชี้ได้ว่าคลาส `hot` มาจากเงื่อนไขไหน และทำไมใช้ `hi` ไม่ใช่ `t`

## ไปต่อ

โมดูลถัดไป (Analysis) เริ่มจากฟิลเตอร์สัญญาณ EMA, Median และ Kalman ที่ทำให้สัญญาณสั่น ๆ เนียนขึ้นให้เห็นกับตา

บทเรียนถัดไป: [บทเรียน 4.1 — ฟิลเตอร์ DSP: EMA, Median, Kalman และ radar range profile](../../m04-analysis/l01-dsp-filters/README.md)

## สะท้อนคิด

- ถ้าคำตัดสินของคุณกับ `dsp.comfort_zone` ไม่ตรงกัน คุณจะตัดสินอย่างไรว่าจะเชื่อชุดไหน
- ฮิสเทอรีซิสแก้ปัญหาอะไร และทำไมมันจำเป็นกับเซนเซอร์จริงมากกว่าค่าจำลอง
