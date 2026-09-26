---
id: edgeai-dev.m06.l06
lang: th
title: {th: 'ลงมือทำ: ส่งเหตุการณ์ที่ fuse แล้วขึ้น MQTT', en: 'Hands-on: send the fused event over MQTT'}
summary: {th: 'เติมห้าจุดใน s17_fusion_iot.py ให้เลือกโมเดล อ่าน verdict อ่าน gyro ดิบ รวมสองสัญญาณด้วย AND แล้ว publish เหตุการณ์ที่ผ่านการยืนยันเป็น JSON ขึ้น MQTT broker ผ่าน WiFi ครั้งเดียวต่อเหตุการณ์ พร้อมเขียนโค้ดชุดเดียวที่ถอยเป็นโหมด [SIM] เองเมื่อไม่มีเน็ต', en: 'Fill five points in s17_fusion_iot.py to select the model, read the verdict, read the raw gyro, AND the two signals and publish each confirmed event once as JSON to an MQTT broker over WiFi, with one codebase that falls back to a [SIM] mode by itself when there is no network.'}
level: L3
time_min: {concept: 15, practise: 30, lab: 25, check: 5}
hardware: {emulator: true, boards: [devkit]}
prerequisites: [edgeai-dev.m06.l05]
objectives:
  - {th: เติมห้าจุดใน practice/s17_fusion_iot.py จนเหตุการณ์ fused ถูก publish ขึ้น topic ครั้งเดียวต่อการเขย่าหนึ่งครั้ง และตรวจเห็นข้อความได้จากฝั่งผู้รับ (เช่น mosquitto_sub หรือเว็บ MQTT client), en: 'Fill the five points in practice/s17_fusion_iot.py until each shake publishes one fused event to the topic, and confirm the message on the receiving side (for example mosquitto_sub or a web MQTT client).'}
  - {th: หาท่าที่โมเดลตอบคลาสเป้าหมายแต่ประตูดิบไม่ผ่าน (หรือกลับกัน) แล้วยืนยันว่าไม่มีเหตุการณ์ถูกส่ง, en: Find a motion where the model reports the target class but the raw gate fails (or the reverse) and confirm no event is sent.}
  - {th: อธิบายการ degrade อย่างสง่างามด้วย try/except ImportError และ is_connected() และบอกได้ว่าทำไมควรส่งเฉพาะเหตุการณ์ที่สรุปแล้วพร้อมหลักฐานดิบใน payload, en: 'Explain graceful degradation with try/except ImportError and is_connected(), and why only the summarised event with its raw evidence should go in the payload.'}
develops: [{skill: proto.mqtt, to: 2}, {skill: proto.wifi, to: 2}, {skill: ai.edge, to: 3}]
assesses: [{skill: proto.mqtt, level: 2, evidence: practice/s17_fusion_iot.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {note: Adapted from the author's Edge AI Developer course (2026-09)}
---

# บทเรียน 6.6 — ลงมือทำ: ส่งเหตุการณ์ที่ fuse แล้วขึ้น MQTT

> โมดูล 6 — แอป Edge AI · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เติมห้าจุดใน s17_fusion_iot.py ให้เลือกโมเดล อ่าน verdict อ่าน gyro ดิบ รวมสองสัญญาณด้วย AND แล้ว publish เหตุการณ์ที่ผ่านการยืนยันเป็น JSON ขึ้น MQTT broker ผ่าน WiFi ครั้งเดียวต่อเหตุการณ์ พร้อมเขียนโค้ดชุดเดียวที่ถอยเป็นโหมด [SIM] เองเมื่อไม่มีเน็ต

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เติมห้าจุดใน practice/s17_fusion_iot.py จนเหตุการณ์ fused ถูก publish ขึ้น topic ครั้งเดียวต่อการเขย่าหนึ่งครั้ง และตรวจเห็นข้อความได้จากฝั่งผู้รับ (เช่น mosquitto_sub หรือเว็บ MQTT client)
2. หาท่าที่โมเดลตอบคลาสเป้าหมายแต่ประตูดิบไม่ผ่าน (หรือกลับกัน) แล้วยืนยันว่าไม่มีเหตุการณ์ถูกส่ง
3. อธิบายการ degrade อย่างสง่างามด้วย try/except ImportError และ is_connected() และบอกได้ว่าทำไมควรส่งเฉพาะเหตุการณ์ที่สรุปแล้วพร้อมหลักฐานดิบใน payload

## ก่อนเริ่ม

ผ่านบทเรียน 6.5 มาแล้ว เข้าใจเงื่อนไข fused และ edge-trigger
เตรียมโปรแกรมรับข้อความ MQTT เช่น `mosquitto_sub -h test.mosquitto.org -t "tesaiot/edge-ai/s17/#" -v` หรือเว็บ MQTT client ที่ต่อ broker เดียวกันได้

- **อุปกรณ์:** บอร์ด TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) — Emulator จำลอง WiFi ให้ต่อติด และส่ง MQTT ถึง broker สาธารณะจริงผ่าน WebSocket (ต่อไม่ได้จะใช้ broker จำลอง) แต่ gyro บน Emulator ค้างใกล้ศูนย์ ซ้อมบน Emulator จึงต้องเปลี่ยนประตูเป็น accel ชั่วคราว บนบอร์ดต้องใส่ชื่อและรหัส WiFi ของคุณเอง
- **เรียนมาก่อน:** [บทเรียน 6.5 — sensor fusion: verdict ของโมเดลกับเซนเซอร์ดิบ](../l05-sensor-fusion/README.md)

## แนวคิด

ทั้งไฟล์อ่านเป็นประโยคเดียว: ต่อเน็ต → หาโมเดลและสั่งรัน → วนอ่าน verdict กับ gyro ดิบ → พอสองสัญญาณเห็นตรงกันก็ publish → หยุดตอนออก
ส่วนต่อเน็ตให้ไว้แล้ว: `import wifi, mqtt` อยู่ใน `try/except ImportError` (ไม่มีโมดูลก็ตั้ง `HAVE_NET = False`), `wifi.connect(WIFI_SSID, WIFI_PASS)` คืน True/False
และบล็อกจนต่อได้หรือหมดเวลา, `wifi.ip()` บอก IP, `mqtt.connect(BROKER, PORT, client_id=CLIENT_ID)` แล้วเช็ก `mqtt.is_connected()` ถ้าไม่ติดจะเข้าโหมด `[SIM]`
ที่พิมพ์ payload ลง console แทน ห้าจุดที่เติมคือ (1) `edge_ai.select(model['index'])` (2) `r = edge_ai.result()`
(3) `ax, ay, az, gx, gy, gz = sensors.bmi270.motion()` (4) `fused = model_hit and raw_ok` และ (5) `mqtt.publish(TOPIC, payload)` ใน `publish_event()`
ที่ห่อ `try/except OSError` ไว้ เพราะ publish โยน `OSError` เมื่อการเชื่อมต่อหลุด

MQTT เป็น publish/subscribe ผ่าน broker ผู้ส่งไม่ต้องรู้ว่าใครฟัง payload ของเราคือ JSON สั้น ๆ
`{"event": ..., "conf": ..., "gyro": ..., "ts": ...}` ใส่ทั้ง verdict และหลักฐานดิบให้ปลายทางตรวจการตัดสินใจย้อนหลังได้ และส่งเฉพาะเหตุการณ์ที่สรุปแล้ว
ไม่ส่งสตรีมดิบ ประหยัด bandwidth และรักษาความเป็นส่วนตัว ธง `fired` ทำให้หนึ่งเหตุการณ์คือหนึ่งข้อความ ไม่ spam broker สาธารณะ
broker สาธารณะมีคนใช้ร่วมกันมาก ให้เปลี่ยน `CLIENT_ID` และ `TOPIC` ให้มีชื่อของคุณต่อท้าย ถ้า client_id ซ้ำกัน broker จะเตะการเชื่อมต่อเก่าออก
และอย่าส่งข้อมูลส่วนตัวขึ้น broker สาธารณะ บน Emulator ให้เปลี่ยนประตูชั่วคราวเป็น `gmag = abs(ax) + abs(ay) + abs(az - 9.81)` กับ `MOTION_FLOOR = 5.0`
เพราะแผง HW ขยับเฉพาะ accel แล้วกดปุ่ม Shake บนบอร์ดจริงใช้ประตู gyro ตามเดิม

## ตัวอย่างสมบูรณ์

`s17_fusion_iot_full.py` ให้เลือกประตูได้สองแบบด้วย `GATE_MODE`: `"imu"` (gyro ดิบ แบบ corroboration) หรือ `"radar"` (มีคนอยู่ไหม แบบ multi-modal
คนละเซนเซอร์กับโมเดล บน Emulator ปุ่ม Shake ทำให้ presence เป็นจริง) นับจำนวนเหตุการณ์ ต่อ broker ใหม่อัตโนมัติเมื่อหลุด และแสดง RSSI จาก `wifi.status()["rssi"]`

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/s17_fusion_iot_full.py](examples/s17_fusion_iot_full.py) | fusion + IoT ฉบับขัดเรียบร้อย |

## ฝึกเติม

คอมเมนต์ `# เติม:` อยู่ที่บรรทัด 127 (`select`), 142 (`result`), 151 (อ่าน `motion()`), 162 (`fused`) และ 115 (`mqtt.publish` ใน `publish_event`)
ถ้า gyro ค้าง 0 ตลอดบนบอร์ด จุดที่ 151 ยังว่าง ถ้าเห็นบรรทัด `MQTT TX` แต่ฝั่งผู้รับไม่เห็นอะไร ตรวจจุดที่ 115 และชื่อ topic ทั้งสองฝั่ง

| ไฟล์ฝึก | เรื่อง |
|---|---|
| [practice/s17_fusion_iot.py](practice/s17_fusion_iot.py) | รวม verdict ของโมเดลกับเซนเซอร์ดิบ แล้วสตรีมขึ้นคลาวด์ (ฉบับฝึกเติมโค้ด) |

## เฉลย

เปิดเฉลยหลังจากลองเองแล้วอย่างน้อยหนึ่งรอบ และอ่าน [วิธีใช้เฉลย](../../README.md#วิธีใช้เฉลย) ก่อน

| เฉลย | คู่กับ |
|---|---|
| [solution/s17_fusion_iot.py](solution/s17_fusion_iot.py) | [practice/s17_fusion_iot.py](practice/s17_fusion_iot.py) |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. เขย่าแรงหนึ่งครั้งแต่ฝั่งผู้รับเห็นข้อความสิบกว่าข้อความ ส่วนใดของโค้ดหายไป *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) try/except OSError
   - ข) ธง fired ที่ยิงเฉพาะขอบขาขึ้นของ fused
   - ค) wifi.ip()
   - ง) ประตู gyro

   <details><summary>เฉลย</summary>

   **ข** — fused เป็นจริงหลายเฟรมติดกันระหว่างเขย่า ถ้าไม่มี fired ทุกเฟรมจะถูก publish

   </details>

2. บนบอร์ด gyro บนจอค้าง 0 ตลอดและไม่มีเหตุการณ์ถูกส่งเลย จุดใดยังว่าง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) จุดที่ 3 อ่าน sensors.bmi270.motion()
   - ข) จุดที่ 5 mqtt.publish
   - ค) จุดที่ 1 select
   - ง) ไม่มีจุดใดผิด

   <details><summary>เฉลย</summary>

   **ก** — ค่าเริ่มต้น gx = gy = gz = 0.0 ทำให้ gmag เป็น 0 ประตูดิบจึงไม่เคยเปิด fused ก็ไม่เคยจริง

   </details>

3. ยกบอร์ดเร็ว ๆ โมเดลตอบ shaking 0.7 แต่ gmag = 25 ที่ MOTION_FLOOR = 40 เกิดอะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) ส่งเหตุการณ์ เพราะโมเดลมั่นใจ
   - ข) ไม่ส่ง เพราะประตูดิบไม่ผ่าน fusion กรอง false positive นี้ไว้
   - ค) แอปพัง
   - ง) ส่งแบบ [SIM]

   <details><summary>เฉลย</summary>

   **ข** — AND ต้องผ่านทั้งสองด่าน นี่คือตัวอย่างของ false positive ที่ fusion มีไว้กรอง

   </details>

4. ทำไมจึงห่อ import wifi, mqtt ด้วย try/except ImportError *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) ให้ import เร็วขึ้น
   - ข) ให้โค้ดชุดเดียวรันได้แม้เฟิร์มแวร์ไม่มีโมดูลเน็ต โดยถอยเป็นโหมด offline แทนการพังตั้งแต่บรรทัด import
   - ค) เพื่อซ่อนรหัส WiFi
   - ง) ไม่จำเป็น

   <details><summary>เฉลย</summary>

   **ข** — degrade อย่างสง่างามคือเช็กก่อนใช้ส่วนที่ต้องมีเน็ต ส่วนที่เหลือของแอปยังทำงานและแสดงกลไก fusion ได้

   </details>

5. payload แบบใดเหมาะที่สุดกับหลัก edge-to-cloud ของบทเรียนนี้ *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) สตรีม IMU ดิบ 50 ครั้งต่อวินาที
   - ข) {"event":"shaking","conf":0.92,"gyro":180,"ts":123456} ครั้งเดียวต่อเหตุการณ์
   - ค) ไฟล์เสียงดิบทุกวินาที
   - ง) ภาพหน้าจอทุกเฟรม

   <details><summary>เฉลย</summary>

   **ข** — คิดที่ขอบแล้วส่งเฉพาะข้อสรุปพร้อมหลักฐานดิบที่จำเป็น ประหยัด bandwidth และรักษาความเป็นส่วนตัว

   </details>

## แล็บ

**MVP ของชุดบทเรียน 6.5–6.6:** การตัดสินใจแบบ fused (verdict AND ประตูดิบ) ถูก publish ขึ้น MQTT ได้จริง ครั้งเดียวต่อเหตุการณ์ ส่วนการขยับเบา ๆ ไม่ถูกส่ง

- [ ] ตั้ง `CLIENT_ID` กับ `TOPIC` ให้มีชื่อของคุณ เติมไฟล์ฝึกครบห้าจุด แล้วรันบนบอร์ดหรือ Emulator (เปลี่ยนเป็นประตู accel เมื่ออยู่บน Emulator)
- [ ] เปิดโปรแกรมรับข้อความ subscribe topic ของคุณ แล้วเขย่าจนเห็นข้อความฝั่งผู้รับ จดตัวอย่าง payload ลงบันทึกการเรียน
- [ ] หาท่าที่ด่านใดด่านหนึ่งไม่ผ่าน แล้วยืนยันว่าไม่มีข้อความถูกส่ง
- [ ] ถอดเน็ต (หรือใส่ชื่อ WiFi ผิด) แล้วยืนยันว่าแอปถอยเป็นโหมด `[SIM]` โดยไม่พัง

## ไปต่อ

โมดูลถัดไป (ใต้ฝากระโปรง) เราจะมุดลงไปดูสแตก Edge AI จริง ทั้ง tri-core, `ai_engine`, IPC model link และ TFLite-Micro บน NPU ว่า verdict ที่ใช้มาทั้งคอร์สเกิดขึ้นอย่างไร

บทเรียนถัดไป: [บทเรียน 7.1 — สแตก Edge AI: tri-core, ai_engine, IPC model link และ TFLite-Micro](../../m07-under-the-hood/l01-edge-ai-stack/README.md)

## สะท้อนคิด

- ถ้าบอร์ดร้อยตัวส่งเหตุการณ์ขึ้น topic เดียวกัน คุณจะออกแบบชื่อ topic และ payload อย่างไรให้ปลายทางแยกได้
- ข้อมูลใดไม่ควรขึ้น broker สาธารณะเด็ดขาด และคุณจะส่งมันไปที่ไหนแทน
