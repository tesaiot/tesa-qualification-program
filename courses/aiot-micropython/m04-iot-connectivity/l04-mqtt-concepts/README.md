---
id: aiot-mpy.m04.l04
lang: th
title: {th: 'MQTT: pub/sub topic QoS และงบข้อมูล', en: 'MQTT: pub/sub, topics, QoS and the data budget'}
summary: {th: 'เข้าใจว่าทำไม IoT เลือก publish/subscribe ผ่าน broker แล้วออกแบบ topic, payload, QoS และงบข้อมูลต่อรอบของทีม โดยรู้เพดานเงียบสี่ข้อของโมดูล mqtt บนบอร์ดก่อนเขียนโค้ดบรรทัดแรก', en: 'Understand why IoT chooses publish/subscribe through a broker, then design the team''s topics, payload, QoS and per-cycle data budget, knowing the four silent limits of the board''s mqtt module before writing the first line.'}
level: L2
time_min: {concept: 35, lab: 15, check: 5}
hardware: {emulator: true, boards: [eva-kit, devkit]}
prerequisites: [aiot-mpy.m04.l03]
objectives:
  - {th: อธิบายความต่างของ client–server กับ publish/subscribe ได้ และบอกผลที่ตามมาสามข้อที่ทำให้ IoT เลือกแบบหลัง (บอร์ดไม่ต้องมี IP ที่คนอื่นเข้าถึงได้ · เพิ่มผู้รับได้โดยไม่แตะโค้ดบนบอร์ด · ผู้รับล่มไม่ทำให้ผู้ส่งล่ม), en: 'Explain how client–server differs from publish/subscribe and give the three consequences that make IoT choose the latter (the board needs no reachable IP, receivers can be added without touching board code, a receiver crash does not bring down the sender).'}
  - {th: ออกแบบ topic ของทีมได้ทั้งสองแบบ (`bento/<รหัสของคุณ>/telemetry` บน broker สาธารณะ และ `device/<device_id>/telemetry` บน TESAIoT CE ที่ช่องที่สองต้องเท่ากับ device_id) ตามกติกาตั้งชื่อสี่ข้อ และบอกได้ว่า subscription ที่มี `+` หรือ `#` รับ topic ใดบ้าง, en: 'Design the team''s topics in both patterns (`bento/<team>/telemetry` on a public broker and `device/<device_id>/telemetry` on TESAIoT CE, where the second level must equal the device_id) following the four naming rules, and state which topics a subscription with `+` or `#` receives.'}
  - {th: เลือก QoS ของแต่ละ topic ด้วยคำถาม "ถ้าข้อความนี้หายไปหนึ่งใบ ใครเดือดร้อน" และคำนวณงบข้อมูลต่อรอบได้ เช่น payload 80 ไบต์ทุก 5 วินาทีคือ 16 B/s พร้อมเขียน JSON ที่ทุกค่าที่ต้องขึ้นกราฟเป็นตัวเลข, en: 'Choose each topic''s QoS with the question "if one of these messages is lost, who suffers?", compute the data budget per cycle, e.g. an 80-byte payload every 5 seconds is 16 B/s, and write JSON in which every value meant for a graph is a number.'}
  - {th: บอกเพดานเงียบสี่ข้อของโมดูล mqtt บนบอร์ดได้ครบ (ช่องรับ 1 ข้อความ · payload ขาเข้า 255 ไบต์ · topic 127 ไบต์ · client_id / username / password 31 ตัวอักษร) พร้อมอาการเมื่อเกิน และอธิบายว่าทำไมลูปต้องฟังคำสั่งทุก 100 ms ไม่ใช่ทุก 5 วินาที, en: 'State all four silent limits of the board''s mqtt module (a 1-message receive slot, 255-byte incoming payload, 127-byte topic, 31-character client_id / username / password) with the symptom when each is exceeded, and explain why the loop must listen for commands every 100 ms, not every 5 seconds.'}
develops: [{skill: proto.mqtt, to: 2}, {skill: iot.fundamentals, to: 2}, {skill: iot.cloud-platform, to: 1}, {skill: hw.architecture, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {repo: 'https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer', path: session-10.html (slides 1–15), ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079}
---

# บทเรียน 4.4 — MQTT: pub/sub topic QoS และงบข้อมูล

> โมดูล 4 — เชื่อมต่อแพลตฟอร์ม IoT · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เข้าใจว่าทำไม IoT เลือก publish/subscribe ผ่าน broker แล้วออกแบบ topic, payload, QoS และงบข้อมูลต่อรอบของทีม โดยรู้เพดานเงียบสี่ข้อของโมดูล mqtt บนบอร์ดก่อนเขียนโค้ดบรรทัดแรก

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. อธิบายความต่างของ client–server กับ publish/subscribe ได้ และบอกผลที่ตามมาสามข้อที่ทำให้ IoT เลือกแบบหลัง (บอร์ดไม่ต้องมี IP ที่คนอื่นเข้าถึงได้ · เพิ่มผู้รับได้โดยไม่แตะโค้ดบนบอร์ด · ผู้รับล่มไม่ทำให้ผู้ส่งล่ม)
2. ออกแบบ topic ของทีมได้ทั้งสองแบบ (`bento/<รหัสของคุณ>/telemetry` บน broker สาธารณะ และ `device/<device_id>/telemetry` บน TESAIoT CE ที่ช่องที่สองต้องเท่ากับ device_id) ตามกติกาตั้งชื่อสี่ข้อ และบอกได้ว่า subscription ที่มี `+` หรือ `#` รับ topic ใดบ้าง
3. เลือก QoS ของแต่ละ topic ด้วยคำถาม "ถ้าข้อความนี้หายไปหนึ่งใบ ใครเดือดร้อน" และคำนวณงบข้อมูลต่อรอบได้ เช่น payload 80 ไบต์ทุก 5 วินาทีคือ 16 B/s พร้อมเขียน JSON ที่ทุกค่าที่ต้องขึ้นกราฟเป็นตัวเลข
4. บอกเพดานเงียบสี่ข้อของโมดูล mqtt บนบอร์ดได้ครบ (ช่องรับ 1 ข้อความ · payload ขาเข้า 255 ไบต์ · topic 127 ไบต์ · client_id / username / password 31 ตัวอักษร) พร้อมอาการเมื่อเกิน และอธิบายว่าทำไมลูปต้องฟังคำสั่งทุก 100 ms ไม่ใช่ทุก 5 วินาที

## ก่อนเริ่ม

ทบทวนสองเรื่องจากบทเรียน 4.1–4.3: `wifi.connect()` บล็อกได้ราว 85 วินาทีถ้ารหัสผิด จึงต้องต่อ WiFi ให้ได้ก่อนเริ่มเรื่อง MQTT
และ `wifi.ping()` รับเฉพาะเลข IP ซึ่งเราจะใช้ตรวจว่าเครื่องที่รัน broker คุยได้จริง ถ้า `wifi.is_connected()` เป็น False
อย่าเพิ่งไปหาสาเหตุที่ MQTT บทเรียนนี้ยังไม่ต้องเขียนโค้ด เตรียมบันทึกการเรียนไว้ออกแบบ topic และ payload ของทีม

- **อุปกรณ์:** บอร์ด Eva Kit หรือ TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) (บทเรียนนี้ยังไม่มีโค้ดให้รัน ภาพหน้าจอในสไลด์มาจากการรันไฟล์ `03_connect_and_publish.py` ของบทเรียน 4.5 บน Emulator ซึ่งบอกได้แค่ว่าบอร์ด "สั่งส่ง" แล้ว ผลจริงต้องดูที่เครื่องฝั่งรับ)
- **เรียนมาก่อน:** [บทเรียน 4.3 — ลงมือทำ: หน้าสถานะเครือข่ายของทีม](../l03-network-status-lab/README.md)

## ดูของจริงก่อน

ดูภาพแรกของสไลด์: บอร์ดอ่านเซนเซอร์แล้ว publish ค่า JSON ทุก 5 วินาทีเข้า broker ที่พอร์ต 1883 ซึ่งเป็นตัวกลางเพียงตัวเดียว
ไม่เก็บ ไม่ตัดสิน แค่ส่งต่อ ส่วน MQTT Explorer บนคอมเห็นทุกข้อความและพิมพ์คำสั่ง toggle LED เดินสวนกลับมาที่บอร์ดได้
โดยที่สองเครื่องไม่เคยรู้ที่อยู่ของกันเลย ภาพหน้าจอจาก Emulator ถัดมาแสดงบันไดสามขั้นก่อนส่งได้ (WiFi ได้ IP ·
broker ต่อแล้ว · publish กำลังส่ง) ถ้าจอบอกว่าส่งแล้วแต่ฝั่งรับไม่เห็นอะไร แปลว่ายังไม่จบ ชุดบทเรียนนี้ต้องดูสองจอพร้อมกัน

## แนวคิด

**ping พิสูจน์ได้แค่ว่าสายดี ยังไม่มีใครที่ปลายทาง** และของที่ส่งออกได้อย่างเดียวยังไม่เรียกว่าระบบ ต้องรับคำสั่งกลับมาได้ด้วย
แบบ client–server ที่เราคุ้น ผู้ถามต้องรู้ชื่อผู้ตอบและถามก่อนถึงได้คำตอบ ทั้งสองฝั่งผูกกันตรง ๆ ส่วน publish/subscribe
ผู้ส่งโยนข้อมูลใส่ topic ผู้รับขอรับตาม topic ทั้งสองฝั่งรู้จักแค่ topic เดียวกัน pub/sub จึงแยกผู้ส่งออกจากผู้รับทั้งเชิงพื้นที่
และเชิงเวลา ผลคือบอร์ดวิ่งออกไปหา broker เองจึงอยู่หลัง NAT ได้ เพิ่มผู้รับได้โดยไม่แตะโค้ดบนบอร์ด และผู้รับล่มไม่ทำให้ผู้ส่งล่ม
broker ไม่ใช่ฐานข้อมูล มันคือที่ทำการไปรษณีย์ที่รับแล้วส่งต่อทันที คำสั่งที่เราใช้มีแค่ `CONNECT` `SUBSCRIBE` `PUBLISH` `DISCONNECT`

**topic เป็นต้นไม้ ไม่ใช่ชื่อแบน ๆ** `+` แทนหนึ่งชั้นพอดี ส่วน `#` แทนทุกอย่างที่อยู่ใต้ลงไปกี่ชั้นก็ได้และต้องเป็นตัวสุดท้าย
ในภาพของสไลด์ แล็ปท็อปที่ subscribe `/plug1/#` ได้ทุกค่าของปลั๊กตัวที่หนึ่ง มือถือที่ subscribe `/+/current` ได้กระแสของทุกปลั๊ก
topic ไม่ต้องประกาศล่วงหน้า publish ไปชื่อไหนชื่อนั้นก็เกิด จึงต้องมีวินัยเอง: เรียงจากกว้างไปแคบ ห้ามขึ้นต้นด้วย `/`
ห้ามใส่ช่องว่างหรือภาษาไทย และอย่าใส่ค่าที่เปลี่ยนบ่อยลงในชื่อ topic บน broker สาธารณะเรากันชนด้วยรหัสที่ไม่ซ้ำใคร เช่น
`bento/team03/telemetry` กับ `bento/team03/cmd/led` (ของจริงให้ใช้รหัสของตัวเองแทน `team03`
เช่นชื่อเล่นภาษาอังกฤษตัวเล็กต่อด้วยเลขสุ่ม 4 หลักอย่าง `nok4821` เพราะผู้เรียนคนอื่นก็ใช้ broker เดียวกัน) ส่วนบน TESAIoT CE แพลตฟอร์มล็อกรูปแบบเป็น `device/team03/telemetry`
กับ `device/team03/commands` ช่องที่สองต้องเท่ากับ device_id เป๊ะ ไม่งั้น ACL ปฏิเสธ payload ส่งแค่ก้อนข้อมูล เพราะบริดจ์เติม
device_id และ timestamp ให้เอง ค่าซ้อน `{"accel":{"x":1}}` ถูกแบนเป็น `accel_x` และเฉพาะค่าตัวเลขเท่านั้นที่กลายเป็นเส้นกราฟ
`{"status":"ok"}` เก็บได้แต่ไม่ขึ้นกราฟ ต้องแปลงเป็น `{"ok": 1}` ชื่อ topic กับรูปร่าง payload คือสัญญากับทุกคนที่ใช้ข้อมูลนี้ต่อ

**บนบอร์ด WiFi และ MQTT อยู่บน CM33_NS คอร์เดียวกับโค้ด Python** ส่วน CM55 ที่วาดจอและอ่านเซนเซอร์ไม่แตะเครือข่ายเลย
ภาพนี้จริงทั้ง Eva Kit และ Dev Kit โมดูล `mqtt` ส่งข้อมูลรับรอง TLS เป็นค่าว่างเสมอ จึงต่อได้เฉพาะพอร์ตข้อความเปล่า 1883
ส่วน TLS อยู่ในบทเรียน 4.7–4.9 ข้อที่ต้องจำให้แม่นคืองานเครือข่ายวางข้อความขาเข้าลงช่องรับ "เมื่อไรก็ได้" ไม่รอให้เราเรียก
`get_message()` และช่องรับมีช่องเดียว สองข้อความที่มาติดกันก่อนเราเรียก ข้อความหลังทับข้อความแรกเงียบ ๆ ไม่มี error ไม่มีธงบอก
เพดานเงียบอีกสามข้อ: payload ขาเข้าเกิน 255 ไบต์ถูกตัดจน JSON parse ไม่ผ่าน · topic ขาเข้าเกิน 127 ไบต์ถูกตัด ·
`client_id` `username` `password` เกิน 31 ตัวอักษรถูกตัด แพลตฟอร์มหาอุปกรณ์ไม่เจอแล้วปฏิเสธการเชื่อมต่อ ทางแก้ที่ใช้ได้จริงคือ
poll ให้ถี่กว่าคนพิมพ์คำสั่ง `sleep_ms(100)` ในลูป ไม่ใช่ `sleep(5)` ซึ่งเหมาะกับคำสั่งจังหวะคนกด ไม่เหมาะกับสตรีมที่ไหลตลอด

**QoS คือราคาของคำว่าแน่ใจ** QoS 0 ส่งครั้งเดียว เน็ตหลุดก็หาย ถูกที่สุด · QoS 1 ส่งอย่างน้อยหนึ่งครั้งด้วย PUBACK ถ้า ack หาย
จะส่งซ้ำ ผู้รับจึงอาจได้ซ้ำ · QoS 2 ครั้งเดียวเป๊ะด้วยสี่ขั้นไป-กลับ ช้าและกินหน่วยความจำที่สุด `mqtt.publish(topic, payload, qos)`
และ `mqtt.subscribe(topic, qos)` รับ qos เป็นอาร์กิวเมนต์ตำแหน่ง telemetry ทุก 5 วินาทีใช้ QoS 0 เพราะค่าถัดไปมาอยู่แล้ว
ส่วนคำสั่งควรใช้ QoS 1 เพราะคำสั่งที่หายคือคำสั่งที่ผู้ใช้กดแล้วไม่เกิดอะไรขึ้น

**งบข้อมูลต่อรอบ** $\frac{80\ \text{B}}{5\ \text{s}} = 16\ \text{B/s}$ payload ขาออกราว 80 ไบต์ยังห่างเพดานที่ปลอดภัย 1000 ไบต์มาก
ส่วนคำสั่งขาเข้าราว 26 ไบต์ต้องไม่เกินเพดานแข็ง 255 ไบต์ ส่วนหัวคงที่ของ MQTT มีแค่ 2 ไบต์ ขณะที่ HTTP มีหัวเป็นข้อความหลายร้อยไบต์
ต่อคำขอ ซึ่งคือค่าไฟกับค่าเน็ตของอุปกรณ์ที่ส่งทุกห้าวินาทีเป็นปี (MQTT 3.1.1 เป็นมาตรฐาน OASIS เมื่อ 2014-10-29 และ 5.0
เมื่อ 2019-03-07 อุปกรณ์ฝังตัวส่วนใหญ่ยังใช้ 3.1.1) รอบการส่งเลือกจากว่าค่าที่วัดเปลี่ยนเร็วแค่ไหน อุณหภูมิห้องส่งทุก 5 วินาทีก็เกินพอ
ส่วนความสั่นของมอเตอร์ควรให้บอร์ดสรุปก่อน (ค่าสูงสุด RMS หรือจำนวนครั้งที่เกินเกณฑ์) "ส่งให้ถี่ที่สุด" เป็นการออกแบบที่แย่เสมอ

## ตัวอย่างสมบูรณ์

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นด้วย:

- [m04-iot-connectivity/l05-mqtt-platform/examples/03_connect_and_publish.py](../l05-mqtt-platform/examples/03_connect_and_publish.py) — ต่อ broker แล้วส่งค่าขึ้นไปหนึ่งชุด

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. ข้อใดเป็นเหตุผลที่ IoT เลือก publish/subscribe แทน client–server เลือกทุกข้อที่ถูก *(เลือกได้หลายข้อ · เป้าหมายข้อ 1)*
   - ก) บอร์ดไม่ต้องมี IP ที่คนอื่นเข้าถึงได้ เพราะบอร์ดวิ่งออกไปหา broker เอง จึงอยู่หลัง NAT ได้
   - ข) เพิ่มผู้รับรายใหม่ได้ด้วยการ subscribe เพิ่ม โดยไม่แตะโค้ดบนบอร์ด
   - ค) broker เก็บทุกข้อความไว้เป็นฐานข้อมูลให้ค้นย้อนหลังได้เสมอ
   - ง) ผู้รับล่มไม่ทำให้ผู้ส่งล่ม เพราะไม่มีใครค้างรอใคร

   <details><summary>เฉลย</summary>

   **ก, ข, ง** — pub/sub แยกผู้ส่งออกจากผู้รับทั้งเชิงพื้นที่และเชิงเวลา ส่วน broker ไม่ใช่ฐานข้อมูล มันคือที่ทำการไปรษณีย์ ที่รับแล้วส่งต่อทันที ไม่เก็บไว้ให้เว้นแต่สั่งให้เก็บ

   </details>

2. ทีมหนึ่ง publish ไปที่ bento/team03/telemetry และ bento/team03/cmd/led subscription ใดรับได้ทั้งสอง topic *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) bento/+/telemetry
   - ข) bento/team03/#
   - ค) bento/team03/+
   - ง) #/team03

   <details><summary>เฉลย</summary>

   **ข** — # แทนทุกชั้นที่อยู่ใต้ลงไปกี่ชั้นก็ได้ จึงครอบทั้ง telemetry และ cmd/led ส่วน + แทนหนึ่งชั้นพอดี bento/team03/+ จึงไม่ถึง cmd/led ที่ลึกสองชั้น และ # ต้องเป็นตัวสุดท้ายเสมอ

   </details>

3. อุปกรณ์ขึ้นทะเบียนบน TESAIoT CE ด้วย device_id ว่า team03 topic ใดที่แพลตฟอร์มยอมให้ publish telemetry *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) /device/team03/telemetry
   - ข) telemetry/team03/device
   - ค) device/team03/telemetry
   - ง) device/ทีม03/telemetry

   <details><summary>เฉลย</summary>

   **ค** — CE ล็อกรูปแบบเป็น device/<device_id>/telemetry และช่องที่สองต้องเท่ากับ device_id เป๊ะ ไม่งั้น ACL ปฏิเสธ ส่วนการขึ้นต้นด้วย / หรือใส่ภาษาไทยผิดกติกาตั้งชื่อ

   </details>

4. ทีมส่ง telemetry ทุก 5 วินาที และรับคำสั่งเปิดปิด LED จากผู้ใช้ ควรเลือก QoS อย่างไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) QoS 2 ทั้งคู่ เพราะแน่ใจที่สุด
   - ข) telemetry QoS 0 และคำสั่ง QoS 1
   - ค) telemetry QoS 1 และคำสั่ง QoS 0
   - ง) QoS 0 ทั้งคู่ เพราะถูกที่สุด

   <details><summary>เฉลย</summary>

   **ข** — telemetry หายหนึ่งใบไม่เสียหายเพราะค่าถัดไปมาใน 5 วินาทีอยู่แล้ว แต่คำสั่งที่หายคือคำสั่งที่ผู้ใช้กดแล้วไม่เกิดอะไรขึ้น QoS 2 ช้าและกินหน่วยความจำที่สุด จึงไม่ใช่ค่าตั้งต้นที่ดี

   </details>

5. ผู้ใช้กด on แล้ว off ติดกันเร็ว ๆ ขณะที่โค้ดบนบอร์ด sleep(5) อยู่ก่อนเรียก get_message() จะเกิดอะไรขึ้น *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) บอร์ดได้ทั้งสองคำสั่งตามลำดับ เพราะ broker ต่อคิวไว้ให้
   - ข) บอร์ดได้แค่ off ส่วน on หายไปเงียบ ๆ เพราะช่องรับมีช่องเดียวและข้อความใหม่เขียนทับ
   - ค) get_message() โยน error ว่าช่องรับเต็ม
   - ง) บอร์ดได้แค่ on เพราะข้อความแรกจองช่องไว้แล้ว

   <details><summary>เฉลย</summary>

   **ข** — งานเครือข่ายวางข้อความลงช่องรับเมื่อไรก็ได้ และช่องรับมีหนึ่งช่องที่เขียนทับเสมอ ไม่มี error ไม่มีธงบอก ทางแก้คือ poll ให้ถี่กว่าคนพิมพ์คำสั่ง เช่น sleep_ms(100) ในลูป

   </details>

## แล็บ

**ออกแบบสัญญาข้อมูลของทีม** (ราว 15 นาที) บนกระดาษหรือในบันทึกการเรียน ยังไม่ต้องเขียนโค้ด

- [ ] วาดภาพบอร์ด · broker · MQTT Explorer พร้อมลูกศรทิศของ telemetry ขาออกและคำสั่งขากลับ
- [ ] เขียน topic ของทีมทั้งสองแบบ (broker สาธารณะที่กันชนด้วยรหัสที่ไม่ซ้ำใคร และ TESAIoT CE ที่ช่องที่สองคือ device_id) แล้วตรวจกับกติกาตั้งชื่อสี่ข้อ
- [ ] เขียน subscription หนึ่งบรรทัดที่รับทุก topic ของทีม และอีกบรรทัดที่รับ telemetry ของทุกทีม ด้วย `#` หรือ `+`
- [ ] เขียน JSON payload ที่มีค่าเซนเซอร์เป็นตัวเลขอย่างน้อยสามฟิลด์ นับไบต์ แล้วคำนวณ B/s ที่รอบละ 5 วินาที เทียบกับถ้าส่งทุก 100 ms
- [ ] เขียน payload ของคำสั่งที่ไม่เกิน 255 ไบต์ และตั้ง client_id ที่ไม่เกิน 31 ตัวอักษร
- [ ] เลือก QoS ของแต่ละ topic พร้อมคำตอบของคำถาม "ถ้าหายไปหนึ่งใบ ใครเดือดร้อน"

## ไปต่อ

บทเรียน 4.5 แกะโมดูล `mqtt` ทั้งหกชื่อ ติดตั้ง TESAIoT Community Edition ด้วย Docker และส่ง telemetry กับรับคำสั่งจริงจากบอร์ด

บทเรียนถัดไป: [บทเรียน 4.5 — MQTT กับแพลตฟอร์มที่ติดตั้งเอง: telemetry และ command](../l05-mqtt-platform/README.md)

## สะท้อนคิด

- ถ้าพรุ่งนี้มีแดชบอร์ดตัวที่สองอยากดูข้อมูลของทีม ต้องแก้อะไรบนบอร์ดบ้าง และคำตอบนี้บอกอะไรเรื่อง pub/sub
- ค่าที่ทีมจะส่งเปลี่ยนเร็วแค่ไหน รอบการส่งที่เลือกมาจากคำถามนั้นหรือจากความรู้สึก
- ความล้มเหลวแบบเงียบข้อไหนในสี่ข้อที่คุณคิดว่าจะเจอก่อน และจะรู้ตัวได้อย่างไร
