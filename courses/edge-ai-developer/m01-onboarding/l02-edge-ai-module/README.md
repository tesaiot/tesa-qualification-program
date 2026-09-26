---
id: edgeai-dev.m01.l02
lang: th
title: {th: 'โมดูล edge_ai: ถามทะเบียนโมเดล เลือก แล้วอ่านคำตอบ', en: 'The edge_ai module: list the models, select one, read its answer'}
summary: {th: 'ใช้สี่คำสั่งหลักของโมดูล edge_ai คือ models, select, result และ stop อ่านคำตอบของโมเดลเป็น dict แปลความ conf กับ CONF_FLOOR และ latency ให้ถูก แล้วรันเมนูหกโมเดลครั้งแรกบน Emulator หรือบอร์ด', en: 'Use the four core edge_ai calls (models, select, result, stop), read the model''s answer as a dict, interpret conf, CONF_FLOOR and latency correctly, and run the six-model menu for the first time on the emulator or the board.'}
level: L3
time_min: {concept: 30, practise: 20, check: 10}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m01.l01]
objectives:
  - {th: 'เรียก edge_ai.models() แล้วอ่านคีย์ index, name, sensor และ labels ของแต่ละโมเดลได้ถูก และอธิบายว่าทำไมควรถามทะเบียนจากเฟิร์มแวร์แทนการ hard-code ชื่อหรือเลขโมเดล', en: 'Call edge_ai.models() and read each model''s index, name, sensor and labels keys correctly, and explain why you ask the firmware''s registry instead of hard-coding names or numbers.'}
  - {th: อธิบายว่า edge_ai.select(n) ยืนยันการสลับโมเดลด้วยการสังเกต (confirm by observation) และห่อการเรียกด้วย try/except OSError ได้, en: 'Explain that edge_ai.select(n) confirms the switch by observation, and wrap the call in try/except OSError.'}
  - {th: 'อ่าน dict จาก edge_ai.result() แล้วบอกได้ว่า label, top, conf, scores, latency_ms และ seq หมายถึงอะไร ตัดสินได้ว่าผลใดเชื่อได้ตาม CONF_FLOOR (0.50) และแปลง latency เป็นจำนวนครั้งต่อวินาทีได้', en: 'Read the dict from edge_ai.result(), say what label, top, conf, scores, latency_ms and seq mean, decide which results to trust against CONF_FLOOR (0.50), and convert latency to runs per second.'}
  - {th: รันเมนู Edge AI บน BENTO Emulator หรือบอร์ด เลือกโมเดล กด Load แล้วเห็นคลาสที่ชนะเปลี่ยนตามท่าทางหรือเสียง, en: 'Run the edge AI menu on the BENTO Emulator or the board, choose a model, press Load and see the winning class change with motion or sound.'}
develops: [{skill: ai.edge, to: 2}, {skill: lang.micropython, to: 2}, {skill: rtos.multicore-ipc, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 1.2 — โมดูล edge_ai: ถามทะเบียนโมเดล เลือก แล้วอ่านคำตอบ

> โมดูล 1 — เริ่มต้น: รันของจริงแล้วแกะดูข้างใน · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

ใช้สี่คำสั่งหลักของโมดูล edge_ai คือ models, select, result และ stop อ่านคำตอบของโมเดลเป็น dict แปลความ conf กับ CONF_FLOOR และ latency ให้ถูก แล้วรันเมนูหกโมเดลครั้งแรกบน Emulator หรือบอร์ด

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เรียก edge_ai.models() แล้วอ่านคีย์ index, name, sensor และ labels ของแต่ละโมเดลได้ถูก และอธิบายว่าทำไมควรถามทะเบียนจากเฟิร์มแวร์แทนการ hard-code ชื่อหรือเลขโมเดล
2. อธิบายว่า edge_ai.select(n) ยืนยันการสลับโมเดลด้วยการสังเกต (confirm by observation) และห่อการเรียกด้วย try/except OSError ได้
3. อ่าน dict จาก edge_ai.result() แล้วบอกได้ว่า label, top, conf, scores, latency_ms และ seq หมายถึงอะไร ตัดสินได้ว่าผลใดเชื่อได้ตาม CONF_FLOOR (0.50) และแปลง latency เป็นจำนวนครั้งต่อวินาทีได้
4. รันเมนู Edge AI บน BENTO Emulator หรือบอร์ด เลือกโมเดล กด Load แล้วเห็นคลาสที่ชนะเปลี่ยนตามท่าทางหรือเสียง

## ก่อนเริ่ม

ทบทวนบทเรียน 1.1 ว่าโค้ด MicroPython อยู่บน Cortex-M33 ส่วนโมเดลอยู่บน Cortex-M55 กับ NPU
เปิด [BENTO IDE](https://ide.tesaiot.dev/) ไว้ ถ้ามีบอร์ดให้ต่อสาย USB ให้พร้อม ถ้ายังไม่มีก็ใช้ BENTO Emulator ได้ทั้งบทเรียน

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — บน Emulator คะแนนของโมเดลเป็นค่าจำลองจากเซนเซอร์จำลอง และมีห้าโมเดล (ไม่มี Push Detection)
- **เรียนมาก่อน:** [บทเรียน 1.1 — Edge AI คืออะไร: วงจรชีวิตของข้อมูลห้าขั้นและเป้าหมายที่โมเดลไปรันได้](../l01-edge-ai-lifecycle/README.md)

## แนวคิด

โมดูล `edge_ai` คือหน้าต่างเดียวที่เราคุยกับเครื่องยนต์อนุมานบน M55 บทเรียนนี้ใช้แค่สี่คำสั่ง **models → select → result → stop**
ซึ่งเป็นทั้งเรื่องราวของการรันโมเดล: อ่านทะเบียน เลือกโมเดล อ่านผล แล้วหยุด

`edge_ai.models()` คืน list ของ dict หนึ่งตัวต่อโมเดล มีคีย์ `index` (ใช้ตอน select) `name` (โชว์บนจอ) `sensor`
(0 = IMU, 1 = RADAR, 2 = MIC) และ `labels` (คลาสที่โมเดลตอบได้) นิสัยที่ดีคือ **ถามฮาร์ดแวร์ก่อน อย่าเดา**
ถ้าเฟิร์มแวร์เพิ่มหรือลดโมเดล โค้ดที่อ่านจาก `models()` จะปรับตามเอง ซึ่งสำคัญมากเพราะบอร์ดกับ Emulator มีจำนวนโมเดลไม่เท่ากัน

`edge_ai.select(n)` เป็นคำสั่งข้ามคอร์ มันส่งคำสั่งแล้วคอยเช็กว่าเครื่องยนต์สลับจริงหรือยัง (confirm by observation)
ถ้าไม่ยืนยันภายในเวลาที่กำหนดจะโยน `OSError` เราจึงห่อด้วย `try/except OSError` เสมอ และ `start(n)` ทำงานเหมือน `select(n)`

`edge_ai.result()` คืนผลล่าสุดเป็น dict หรือ `None` ถ้ายังไม่มีผล: `label` คลาสที่ชนะ `top` ลำดับของคลาสนั้น `conf` ความมั่นใจ 0..1
`scores` คะแนนทุกคลาสที่รวมกันได้ 1 `latency_ms` เวลาที่ NPU ใช้ และ `seq` ที่เพิ่มขึ้นทุกครั้งที่มีผลใหม่
ในภาษาคณิต คลาสที่ชนะคือ $\arg\max_k s_k$ และความมั่นใจคือ $\max_k s_k$ ค่า `CONF_FLOOR` = 0.50 คือเส้นที่เฟิร์มแวร์แนะนำ
ต่ำกว่านี้ถือว่าโมเดลยังไม่ชัวร์ เพราะโมเดลตอบเป็นความน่าจะเป็น ไม่ใช่ความจริงเด็ดขาด ส่วน latency แปลงเป็นจำนวนครั้งต่อวินาทีได้ด้วย
$\text{fps} = 1000 / t_{\text{ms}}$ เช่น 4.1 ms ≈ 244 ครั้งต่อวินาที

## ตัวอย่างสมบูรณ์

เปิด `12_edge_ai_menu.py` ดูก่อนว่าหน้า Edge AI จริงใช้สี่คำสั่งนี้อย่างไร ทาย (Predict) ก่อนรันว่าเลือก Motion แล้วเขย่าบอร์ดจะเกิดอะไร
แล้วค่อยรันเทียบ ไฟล์ที่เราจะเติมเองอยู่ในบทเรียน 1.3

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/12_edge_ai_menu.py](examples/12_edge_ai_menu.py) | Edge AI Menu: เลือกและรันโมเดล AI ได้ทุกตัวในเฟิร์มแวร์เดียว (ไม่ต้องต่อเน็ต) |

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นหรือใน `shared/` ด้วย:

- [m01-onboarding/l03-first-inference-lab/practice/s01_first_inference.py](../l03-first-inference-lab/practice/s01_first_inference.py) — รันโมเดล Edge AI ตัวแรกของเรา (ฉบับฝึกเติมโค้ด)

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. ทำไมโค้ดในหลักสูตรนี้ถึงอ่านชื่อโมเดลจาก edge_ai.models() แทนการเขียนชื่อหรือเลขโมเดลตายตัว *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) เพราะ models() เร็วกว่าการเขียน list เอง
   - ข) เพราะเฟิร์มแวร์แต่ละบอร์ดมีโมเดลไม่เท่ากัน ถ้าอ่านจากทะเบียน โค้ดจะปรับตามเองโดยไม่ต้องแก้
   - ค) เพราะ select() รับได้เฉพาะชื่อโมเดล
   - ง) เพราะ Emulator ไม่มีโมเดลเลย

   <details><summary>เฉลย</summary>

   **ข** — นิสัย "ถามฮาร์ดแวร์ก่อน อย่าเดา" ทำให้โค้ดชุดเดียวใช้ได้ทั้งบอร์ดหกโมเดลและ Emulator ห้าโมเดล ลำดับที่ต่างกันก็ไม่ทำให้พัง

   </details>

2. ถ้า edge_ai.select(n) ส่งคำสั่งไปแล้วแต่เครื่องยนต์ไม่สลับภายในเวลาที่กำหนด จะเกิดอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) select() คืน None เงียบ ๆ แล้วโปรแกรมทำต่อ
   - ข) select() โยน OSError เราจึงต้องห่อด้วย try/except OSError
   - ค) บอร์ดรีบูตเอง
   - ง) โมเดลตัวเดิมถูกลบออกจากทะเบียน

   <details><summary>เฉลย</summary>

   **ข** — select() ยืนยันด้วยการสังเกตว่าโมเดลที่ active เปลี่ยนจริง ถ้าไม่เห็นก็โยน OSError เพื่อไม่ให้โปรแกรมโกหกว่ากำลังรัน

   </details>

3. ผลคือ {'label': 'circle', 'conf': 0.41, ...} และ CONF_FLOOR = 0.50 ควรทำอย่างไรกับคำตอบนี้ *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) เชื่อเลยเพราะ circle ชนะ
   - ข) ถือว่ายังไม่ชัวร์ เพราะ conf ต่ำกว่า CONF_FLOOR ยังไม่ควรสั่งการตามคำตอบนี้
   - ค) เรียก select() ใหม่ทุกครั้งที่ conf ต่ำ
   - ง) คูณ conf ด้วย 2 ให้ผ่านเกณฑ์

   <details><summary>เฉลย</summary>

   **ข** — argmax เลือกผู้ชนะเสมอแม้คะแนนสูสี CONF_FLOOR คือเกณฑ์ตัดบนค่า conf เชื่อคำตอบก็ต่อเมื่อ conf ≥ 0.50

   </details>

4. latency_ms = 5 หมายความว่าโมเดลรันได้สูงสุดราวกี่ครั้งต่อวินาที *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) 5 ครั้ง
   - ข) 50 ครั้ง
   - ค) 200 ครั้ง
   - ง) 5000 ครั้ง

   <details><summary>เฉลย</summary>

   **ค** — fps = 1000 / t_ms = 1000 / 5 = 200 ครั้งต่อวินาที เหลือเฟือเมื่อเทียบกับลูปที่อ่านผลทุกราว 180 ms

   </details>

5. บน BENTO Emulator คุณเลือก Motion Detection กด Load แล้วลากแผ่นเอียงหรือกด Shake ควรเห็นอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) คลาสที่ชนะเปลี่ยนระหว่าง idle / circle / shaking พร้อมแถบความมั่นใจของทุกคลาส
   - ข) รายชื่อโมเดลหายไปจาก dropdown
   - ค) หน้าจอขึ้น Push ทุกครั้ง
   - ง) ไม่มีอะไรเปลี่ยนจนกว่าจะต่อ WiFi

   <details><summary>เฉลย</summary>

   **ก** — Motion มีสามคลาส idle circle shaking บน Emulator คะแนนเลียนแบบจากเซนเซอร์จำลอง จึงเปลี่ยนตามการเอียงหรือเขย่าที่เราจำลอง ไม่ต้องใช้เน็ตเลย

   </details>

## แล็บ

- [ ] ใน REPL หรือในไฟล์ พิมพ์ `edge_ai.models()` แล้วจดว่าบอร์ดหรือ Emulator ของคุณมีกี่โมเดล ชื่ออะไร ใช้เซนเซอร์อะไร
- [ ] รันเมนูบน Emulator (หรือบอร์ด) เลือก Motion Detection กด Load แล้วเห็นคลาสที่ชนะเปลี่ยนเป็น idle / circle / shaking
- [ ] ถ้ามีบอร์ด ลองสลับไปโมเดลไมโครโฟนอย่างน้อยหนึ่งตัว แล้วส่งเสียงให้คลาสเปลี่ยน

## ไปต่อ

บทเรียน 1.3 เราจะไล่โค้ดไฟล์ `s01_first_inference.py` แล้วเติมสี่ช่องเองจนเมนูทำงานครบวงจร

บทเรียนถัดไป: [บทเรียน 1.3 — ลงมือทำ: เมนูโมเดลตัวแรกของเรา](../l03-first-inference-lab/README.md)

## สะท้อนคิด

- ถ้าตั้ง CONF_FLOOR ต่ำเกินไปหรือสูงเกินไป แอปของคุณจะผิดพลาดแบบไหน
- ทำไม select() ถึงต้อง "รอดู" ว่าสลับจริง แทนที่จะเชื่อว่าสั่งแล้วสำเร็จ
