---
id: aiot-mpy.m04.l06
lang: th
title: {th: 'ลงมือทำ: telemetry สองทาง', en: 'Hands-on: two-way telemetry'}
summary: {th: ประกอบโปรแกรม MQTT สองทางที่ส่ง JSON จากเซนเซอร์จริงขึ้น TESAIoT CE ของทีมทุก 5 วินาที และรับคำสั่ง toggle กลับมาสลับ LED บนบอร์ด ในลูปเดียวที่ไม่ทำคำสั่งหล่นหาย, en: 'Assemble a two-way MQTT program that publishes real sensor JSON to the team''s TESAIoT CE every 5 seconds and takes a toggle command back to switch an LED on the board, in one loop that does not drop commands.'}
level: L2
time_min: {concept: 10, practise: 35, lab: 15, check: 5}
hardware: {emulator: true, boards: [eva-kit, devkit]}
prerequisites: [aiot-mpy.m04.l05]
objectives:
  - {th: เติมช่องว่างหกจุดใน s10_mqtt_telemetry.py ทีละท่า จนบอร์ด publish JSON ที่มีค่าเซนเซอร์จริงเป็นตัวเลขอย่างน้อย 3 ฟิลด์ไปที่ device/<device_id>/telemetry ทุก 5 วินาที และ MQTT Explorer เห็นต่อเนื่องอย่างน้อย 1 นาที, en: 'Fill the six blanks in s10_mqtt_telemetry.py one move at a time until the board publishes JSON with at least 3 numeric real-sensor fields to device/<device_id>/telemetry every 5 seconds, seen continuously in MQTT Explorer for at least 1 minute.'}
  - {th: 'ทำให้คำสั่ง {"cmd":"toggle"} จาก MQTT Explorer สลับ LED บนบอร์ดได้ทั้งติดและดับ โดยเรียก get_message() ทุกรอบลูป 100 ms แทนการ sleep 5 วินาทีคร่อมทั้งลูป', en: 'Make a {"cmd":"toggle"} command from MQTT Explorer switch the board''s LED both on and off, calling get_message() on every 100 ms loop pass instead of sleeping 5 seconds across the loop.'}
  - {th: 'อธิบายว่า client_id, username, device_id และช่องที่สองของ topic ต้องสัมพันธ์กันอย่างไร และใช้ตารางกับดักหาสาเหตุของอาการที่ไม่มี error ชี้สาเหตุได้อย่างน้อยสามอาการ', en: 'Explain how client_id, username, device_id and the second topic level must relate, and use the pitfalls table to find the cause of at least three symptoms whose error does not point at the cause.'}
  - {th: แยกรอบวัดออกจากรอบส่งในไฟล์ 08 (200 ms กับ 2000 ms) และอธิบายด้วยตัวเลขว่าทำไมสองค่านี้ไม่ควรเท่ากัน, en: Separate the read period from the send period in file 08 (200 ms versus 2000 ms) and explain with numbers why the two should not be equal.}
develops: [{skill: proto.mqtt, to: 2}, {skill: iot.cloud-platform, to: 2}, {skill: iot.fundamentals, to: 2}, {skill: soft.problem-solving, to: 2}]
assesses: [{skill: proto.mqtt, level: 2, evidence: practice/s10_mqtt_telemetry.py}, {skill: iot.cloud-platform, level: 2, evidence: practice/s10_mqtt_telemetry.py}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {repo: 'https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer', path: session-10.html (slides 28–44), ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079}
---

# บทเรียน 4.6 — ลงมือทำ: telemetry สองทาง

> โมดูล 4 — เชื่อมต่อแพลตฟอร์ม IoT · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

ประกอบโปรแกรม MQTT สองทางที่ส่ง JSON จากเซนเซอร์จริงขึ้น TESAIoT CE ของทีมทุก 5 วินาที และรับคำสั่ง toggle กลับมาสลับ LED บนบอร์ด ในลูปเดียวที่ไม่ทำคำสั่งหล่นหาย

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. เติมช่องว่างหกจุดใน s10_mqtt_telemetry.py ทีละท่า จนบอร์ด publish JSON ที่มีค่าเซนเซอร์จริงเป็นตัวเลขอย่างน้อย 3 ฟิลด์ไปที่ device/<device_id>/telemetry ทุก 5 วินาที และ MQTT Explorer เห็นต่อเนื่องอย่างน้อย 1 นาที
2. ทำให้คำสั่ง {"cmd":"toggle"} จาก MQTT Explorer สลับ LED บนบอร์ดได้ทั้งติดและดับ โดยเรียก get_message() ทุกรอบลูป 100 ms แทนการ sleep 5 วินาทีคร่อมทั้งลูป
3. อธิบายว่า client_id, username, device_id และช่องที่สองของ topic ต้องสัมพันธ์กันอย่างไร และใช้ตารางกับดักหาสาเหตุของอาการที่ไม่มี error ชี้สาเหตุได้อย่างน้อยสามอาการ
4. แยกรอบวัดออกจากรอบส่งในไฟล์ 08 (200 ms กับ 2000 ms) และอธิบายด้วยตัวเลขว่าทำไมสองค่านี้ไม่ควรเท่ากัน

## ก่อนเริ่ม

บทเรียนนี้คือแล็บที่ต่อจากบทเรียน 4.4–4.5 ก่อนแตะโค้ดให้มีของครบ: TESAIoT CE ที่ทีมติดตั้งเองและเปิดพอร์ต 1883 ให้บอร์ดในแลนเข้าถึงได้
(ไม่ใช่ `127.0.0.1:11883`) อุปกรณ์ที่ขึ้นทะเบียนแล้วด้วย `device_id` สั้น ๆ ไม่เกิน 31 ตัวอักษร รหัสผ่าน MQTT ของทีม
IP ของเครื่องที่รัน CE และ MQTT Explorer ที่ต่อ broker เดียวกันแล้ว subscribe `device/#` รอไว้
ทวนสองเรื่องจากบทเรียน 4.4–4.5: `get_message()` มีช่องรับช่องเดียว และ `mqtt.publish(topic, payload)` รับตามตำแหน่งเท่านั้น

- **อุปกรณ์:** บอร์ด Eva Kit หรือ TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) (ซ้อมโค้ดและหน้าจอบน Emulator ได้ แต่ข้อความไม่ออกไปถึง TESAIoT CE ในแลนของทีม การผ่าน MVP จึงต้องใช้บอร์ดจริง)
- **เรียนมาก่อน:** [บทเรียน 4.5 — MQTT กับแพลตฟอร์มที่ติดตั้งเอง: telemetry และ command](../l05-mqtt-platform/README.md)

## แนวคิด

แล็บนี้เอาทุกชิ้นของบทเรียน 4.4–4.5 มาประกอบเป็นโปรแกรมเดียว ข้อมูลเดินสองทาง: ขาออกคือ JSON จากเซนเซอร์จริงทุก 5 วินาที
ขาเข้าคือคำสั่งที่คนอื่นพิมพ์มาสั่งไฟบนบอร์ดเรา ข้อที่ LED สลับได้คือหัวใจของ MVP ถ้าขาดข้อนี้ เราได้แค่ **เครื่องส่งข้อมูล**
ยังไม่ใช่ **อุปกรณ์ที่สั่งได้**

ตัวตนของทีมต้องตรงกันทุกจุด: `client_id`, `username` และ `device_id` คือค่าเดียวกัน และช่องที่สองของ topic ต้องเป็น
`device_id` ตรงตัวอักษร (`device/<device_id>/telemetry` กับ `device/<device_id>/commands`) ถ้าไม่ตรง ACL ของ CE
ปฏิเสธโดยที่ `publish()` ไม่ error สักคำ ส่วน payload ต้องส่งแบนและเป็นตัวเลข ค่าที่เป็นสตริงขึ้นบนแพลตฟอร์มได้แต่วาดเส้นกราฟไม่ได้

ลูปหลักมีนาฬิกา **สามเรือน** ไม่ใช่เรือนเดียว: เรือนของการส่ง (5 วินาที นับด้วย `time.ticks_diff()`) เรือนของนิ้ว
(`ui.poll()` ทุก 200 ms) และ `get_message()` ที่ถามทุกรอบลูป 100 ms เพราะช่องรับมีช่องเดียว ข้อความใหม่ทับของเก่าเงียบ ๆ
ทีมที่เขียน `time.sleep(5)` คร่อมทั้งลูปจะพบว่าบอร์ดไม่ตอบคำสั่ง ส่วนไฟ "ค่าค้าง" บนจอถูกเขียนเฉพาะตอนสถานะเปลี่ยน
เพราะคิวคำสั่งของจอมีก้นถัง พอเต็มแล้วเฟิร์มแวร์ทิ้งคำสั่งเปลี่ยนข้อความก่อน ตัวเลขจึงค้างโดยไม่มี error

สิบเอ็ดจากสิบสองแถวในตารางกับดักของสไลด์ **ไม่ส่ง error ที่ตรงกับสาเหตุ** จึงต้องอ่านก่อนเจอปัญหา ตัวอย่างที่เจอบ่อย:
`keep_alive` ที่ถูกคือ `keepalive` · `publish()` ไม่มี `retain` · payload ขาเข้าถูกตัดที่ 255 ไบต์
และ topic ขาเข้าที่ 127 ไบต์ · `client_id` ซ้ำกันทำให้สองทีมหลุดสลับกัน · `publish()` ตอนลิงก์หลุดโยน `OSError`
ไม่ได้คืน False จึงต้องเช็ก `is_connected()` และครอบด้วย `try/except OSError`

ไฟล์ 08 ปิดวงจรด้วยค่าจริง: อุณหภูมิจาก SHT40 บน Dev Kit ส่วน Eva Kit ไม่มีเซนเซอร์อุณหภูมิ ลูกบิดจึงเล่นบทแทน
(0–100 % = 15–45 °C) และ console บอกตั้งแต่รอบแรกว่าค่ามาจากไหน ไฟล์นี้วัดทุก 200 ms แต่ส่งทุก 2000 ms บนจอเส้นเขียว
(ค่าที่ส่งจริง) จึงเป็นขั้นบันไดใต้เส้นฟ้า (ค่าที่วัด) นั่นคือภาพของประโยค **จอเห็นบ่อยกว่าที่คลาวด์เห็น**

## ตัวอย่างสมบูรณ์

เปิด `08_real_sensor_leaves_the_board.py` หลังจากไฟล์ฝึกส่งได้แล้ว ก่อนรันให้ทายว่าเส้นเขียวบนกราฟจะหน้าตาอย่างไร
แล้วรันดู จากนั้นนับจาก console ว่าวัดกี่รอบและส่งกี่ครั้ง ข้อ "ตาคุณ" ท้ายไฟล์ให้เพิ่มเงื่อนไขส่งเฉพาะเมื่อค่าเปลี่ยนเกิน 0.3 องศา
แล้วดูว่าจำนวนครั้งที่ส่งลดลงเท่าไรโดยที่ปลายทางยังเห็นภาพเดิม ไฟล์นี้ตั้ง `TOPIC` ไว้เป็น `bento/team03/telemetry`
ถ้าจะให้ค่าขึ้นกราฟบน CE ของทีม ต้องใช้รูป `device/<device_id>/telemetry` ตามตารางกับดัก

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/08_real_sensor_leaves_the_board.py](examples/08_real_sensor_leaves_the_board.py) | ค่าที่วัดได้จริงบนโต๊ะนี้ ออกไปหาคนอื่น |

## ฝึกเติม

เปิด `practice/s10_mqtt_telemetry.py` หน้าจอเขียนมาให้ครบแล้ว ช่องว่างหกจุดอยู่ที่ตรรกะทั้งหมด ทำตามลำดับนี้ และรันทุกครั้งที่เติมเสร็จหนึ่งจุด

1. แก้ค่าเจ็ดบรรทัดบนหัวไฟล์ให้เป็นของทีม: `WIFI_SSID` `WIFI_PASSWORD` `BROKER` (IP ของเครื่องที่รัน CE ไม่ใช่ localhost) `DEVICE_ID` `MQTT_PASS` `TOPIC_PUB` `TOPIC_CMD`
2. ท่าที่ 1 เติมบรรทัด `mqtt.connect(...)` ด้วย `username=` และ `keepalive=` แล้วรันจนไฟ MQTT บนจอติดและ console ขึ้นว่าต่อแล้ว ห้ามข้ามไปท่าอื่นก่อน
3. ท่าที่ 2 เติม dict ของค่าเซนเซอร์ (ใช้ `round()` และเก็บเป็นตัวเลข) กับบรรทัด `mqtt.publish(TOPIC_PUB, json.dumps(data))` แล้วดูใน MQTT Explorer ว่าข้อความเข้ามาห่างกัน 5 วินาที
4. ท่าที่ 3 เติม `mqtt.subscribe(TOPIC_CMD)` ก่อนเข้าลูป `msg = mqtt.get_message()` ในลูป และ `lamp.value(...)` แล้วพิมพ์ `{"cmd":"toggle"}` จาก MQTT Explorer

รู้ว่าเสร็จเมื่อไฟ WiFi กับ MQTT ติด รายการ "สามใบล่าสุด" เดินขึ้นทุก 5 วินาที และไฟ "ไฟสั่งไกล" บนจอสลับพร้อม LED จริง
ถ้าท่าที่ 1 ยังไม่ครบ ไฟ MQTT จะไม่ติด จอจึงบอกได้เองว่ายังค้างอยู่ขั้นไหน

| ไฟล์ฝึก | เรื่อง |
|---|---|
| [practice/s10_mqtt_telemetry.py](practice/s10_mqtt_telemetry.py) | ส่ง telemetry ขึ้น broker และรับคำสั่งกลับ (ฉบับฝึกเติมโค้ด) |

## เฉลย

เปิดเฉลยหลังจากลองเองแล้วอย่างน้อยหนึ่งรอบ แล้วอ่าน [วิธีใช้เฉลย](../../README.md#วิธีใช้เฉลย) ก่อน

| เฉลย | คู่กับ |
|---|---|
| [solution/s10_mqtt_telemetry.py](solution/s10_mqtt_telemetry.py) | [practice/s10_mqtt_telemetry.py](practice/s10_mqtt_telemetry.py) |

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. บอร์ด publish ได้โดยไม่มี error แต่ TESAIoT CE ไม่มีข้อมูลของทีมเลย และ MQTT Explorer ที่ subscribe `device/#` ก็ไม่เห็นข้อความ สาเหตุที่ตารางกับดักชี้คืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) ช่องที่สองของ topic ไม่ตรงกับ `device_id` ACL ของ CE จึงปฏิเสธ ทั้งที่ฝั่งบอร์ดไม่มี error
   - ข) ตั้ง `keepalive=60` ยาวเกินไป
   - ค) payload เล็กเกินไป broker จึงทิ้ง
   - ง) ต้องใส่ `retain=True` ให้ `publish()` ข้อความจึงจะค้างอยู่บน broker

   <details><summary>เฉลย</summary>

   **ก** — ACL ของ CE ปฏิเสธข้อความที่ช่องที่สองของ topic ไม่ตรงกับ `device_id` โดยที่ `publish()` ไม่ error จึงต้องใช้ `device/<device_id>/telemetry` ตรงตัวอักษร ส่วน `retain` ไม่มีในโมดูลจริง ใส่เข้าไปจะได้ TypeError

   </details>

2. ทีมหนึ่งเขียนลูปเป็น publish แล้ว `time.sleep(5)` แล้วค่อย `get_message()` หนึ่งครั้ง ระหว่างนั้นเพื่อนส่ง `{"cmd":"toggle"}` มาสามครั้งรวดเดียว จะเกิดอะไรขึ้น *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) LED สลับสามครั้งตามลำดับ เพราะ broker เก็บคิวไว้ให้
   - ข) บอร์ดเห็นแค่ข้อความล่าสุด อีกสองข้อความถูกทับหายเงียบ ๆ เพราะช่องรับมีช่องเดียว
   - ค) บอร์ดโยน OSError เพราะข้อความล้น
   - ง) broker ตัดการเชื่อมต่อทันทีเพราะบอร์ดไม่ตอบ

   <details><summary>เฉลย</summary>

   **ข** — `get_message()` มีช่องรับช่องเดียว ข้อความใหม่ทับของเก่าโดยไม่เตือน วิธีเดียวคือถามให้ถี่พอ ลูปจึงเดินทุก 100 ms และนับ "ทุกห้าวินาที" ด้วย `ticks_diff` แทนการหยุดรอ

   </details>

3. สำหรับอุปกรณ์ของทีมบน TESAIoT CE ค่าใดต้องเท่ากับ `device_id` ที่ขึ้นทะเบียนไว้ เลือกทุกข้อที่ถูก *(เลือกได้หลายข้อ · เป้าหมายข้อ 3)*
   - ก) `client_id` ที่ส่งให้ `mqtt.connect()`
   - ข) `username` ที่ส่งให้ `mqtt.connect()`
   - ค) ช่องที่สองของ topic เช่น `device/team03/telemetry`
   - ง) `WIFI_SSID` ของห้อง

   <details><summary>เฉลย</summary>

   **ก, ข, ค** — CE ตรวจตัวตนด้วย `username == client_id == device_id` และ ACL ดูช่องที่สองของ topic ค่าทั้งสามจึงต้องเป็นคำเดียวกัน ส่วนชื่อวง WiFi ไม่เกี่ยว

   </details>

4. บรรทัด `mqtt.connect(BROKER, port=1883, client_id=DEVICE_ID, username=DEVICE_ID, password=MQTT_PASS, keep_alive=60)` ให้ `TypeError` ทันที ควรแก้อย่างไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) เปลี่ยน `keep_alive` เป็น `keepalive`
   - ข) เปลี่ยน `username=` เป็น `user=`
   - ค) ตัด `port=1883` ออก
   - ง) ส่งอาร์กิวเมนต์ทั้งหมดตามตำแหน่งแทน keyword

   <details><summary>เฉลย</summary>

   **ก** — คีย์เวิร์ดที่ถูกคือ `keepalive` ตามตารางกับดัก `keep_alive` มาจากเอกสารที่เขียนผิด และชื่ออาร์กิวเมนต์ผิดตัวเดียวก็ TypeError ทันที ส่วน `user=` ก็ผิดเช่นกัน ที่ถูกคือ `username=`

   </details>

5. ไฟล์ 08 วัดทุก 200 ms แต่ส่งทุก 2000 ms ถ้าเปลี่ยนให้ส่งทุก 200 ms เท่ากับรอบวัด ในห้องที่มีสิบห้าโต๊ะจะเกิดอะไรกับ broker ตัวเดียว *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) ไม่ต่างกัน เพราะข้อความเล็กมาก
   - ข) ราว 75 ข้อความต่อวินาที (5 ต่อวินาทีต่อบอร์ด) ห้องล่มได้โดยไม่มีใครเขียนโค้ดผิด
   - ค) ราว 15 ข้อความต่อวินาที เพราะหนึ่งโต๊ะหนึ่งข้อความ
   - ง) broker จะรวมข้อความให้เองจนเหลือทุก 2 วินาที

   <details><summary>เฉลย</summary>

   **ข** — ส่งทุก 200 ms คือ 5 ข้อความต่อวินาทีต่อบอร์ด สิบห้าโต๊ะเป็น 75 ข้อความต่อวินาทีเข้า broker ตัวเดียว การวัดไม่กวนใคร แต่การส่งกวน broker และเพื่อนร่วมห้อง สองตัวเลขนี้จึงไม่ควรเท่ากัน

   </details>

## แล็บ

**MVP: สองทาง** ทำบนบอร์ดจริงกับ CE ของทีม แล้วเก็บหลักฐานลงบันทึกการเรียน

- [ ] MQTT Explorer เห็นข้อความเข้าที่ topic ของทีมห่างกัน 5 วินาที ต่อเนื่องอย่างน้อย 1 นาที
- [ ] payload เป็น JSON ที่ถูกต้อง มีค่าจากเซนเซอร์จริงอย่างน้อย 3 ฟิลด์ และค่าเปลี่ยนเมื่อขยับบอร์ด
- [ ] พิมพ์ `{"cmd":"toggle"}` จาก MQTT Explorer แล้ว LED บนบอร์ดสลับได้ทั้งติดและดับ
- [ ] ข้อมูลขึ้นกราฟใน Device Details → Telemetry ของ TESAIoT CE ที่ทีมติดตั้งเอง
- [ ] เขียนอธิบายว่า `client_id`, `username`, `device_id` และช่องที่สองของ topic ต้องสัมพันธ์กันอย่างไร
- [ ] บันทึกภาพหน้าจอทั้งฝั่งบอร์ดและฝั่งคอมลงบันทึกการเรียน

## ไปต่อ

บทเรียน 4.7 ย้ายจากพอร์ต 1883 ไปพอร์ต 8884 ที่มี TLS วันนี้บอร์ดพูดได้และฟังเป็นแล้ว ต่อไปคือทำให้คนอื่นแอบฟังไม่ได้
ถ้ามีเวลา เลือกทำหนึ่งข้อจากสไลด์ต่อยอด: ฟังทั้งห้องด้วย `device/+/telemetry` แล้วเสนอ schema กลาง · ขยายคำสั่งให้คุม LED
แต่ละดวงด้วยชื่อจาก `gpio.board_info()["led_names"]` และ publish สถานะกลับ · วัดเพดาน 255 ไบต์ด้วยมือตัวเอง · หรือส่งเมื่อค่าเปลี่ยนแทนการส่งตามเวลา

บทเรียนถัดไป: [บทเรียน 4.7 — TLS: ใบรับรอง ห่วงโซ่ความเชื่อถือ และการจับมือ](../l07-tls-concepts/README.md)

## สะท้อนคิด

- ถ้าเน็ตของห้องหลุดไปสองนาที ข้อมูลช่วงนั้นควรหายไปเลย หรือบอร์ดควรเก็บไว้ส่งทีหลัง
- ใครควรตัดสินว่าค่าไหนผิดปกติ ระหว่างบอร์ดกับแพลตฟอร์ม
- ถ้ามีอุปกรณ์ 500 ตัวส่งทุก 5 วินาที broker ตัวเดียวรับไหวไหม และเราจะรู้ได้อย่างไรก่อนจะสาย
