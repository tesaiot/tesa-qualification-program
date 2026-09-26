---
id: aiot-mpy.m04.l05
lang: th
title: {th: 'MQTT กับแพลตฟอร์มที่ติดตั้งเอง: telemetry และ command', en: 'MQTT with a self-hosted platform: telemetry and commands'}
summary: {th: ใช้โมดูล mqtt หกชื่อส่ง JSON จากบอร์ดขึ้น TESAIoT CE ที่ทีมติดตั้งเองและรับคำสั่งกลับมา โดยรู้ทันกับดักพอร์ต 1883 การขึ้นทะเบียนอุปกรณ์ และเพดานเงียบของแต่ละฟังก์ชัน, en: 'Use the six names of the mqtt module to send JSON from the board to the team''s own TESAIoT CE and take commands back, knowing the port-1883 trap, device registration and each function''s silent limits.'}
level: L2
time_min: {concept: 15, practise: 35, lab: 20, check: 5}
hardware: {emulator: true, boards: [eva-kit, devkit]}
prerequisites: [aiot-mpy.m04.l04]
objectives:
  - {th: ส่ง JSON ใบแรกขึ้น broker ด้วย `03_connect_and_publish.py` โดยตรวจค่าที่ `mqtt.connect()` คืนก่อนทำงานต่อ และบอกได้ว่าทางออกทั้งสามของ `mqtt.publish()` (True · False · OSError) แต่ละทางแปลว่าอะไร, en: 'Send the first JSON message to the broker with 03_connect_and_publish.py, checking what mqtt.connect() returns before going on, and state what each of the three outcomes of mqtt.publish() (True, False, OSError) means.'}
  - {th: 'เตรียม TESAIoT CE ให้บอร์ดใน LAN เข้าถึงได้ โดยแก้การเผยแพร่พอร์ตเป็น `0.0.0.0:1883:1883` ขึ้นทะเบียนอุปกรณ์ด้วย `device_id` สั้นไม่เกิน 31 ตัวอักษร และตั้ง `client_id == username == device_id` จน MQTT Explorer ที่ subscribe `device/#` เห็นข้อความของทีม', en: 'Make TESAIoT CE reachable from the board on the LAN by changing the port mapping to 0.0.0.0:1883:1883, registering the device with a short device_id of at most 31 characters and setting client_id == username == device_id, until MQTT Explorer subscribed to device/# sees the team''s messages.'}
  - {th: รับคำสั่งจาก MQTT Explorer ด้วยการ subscribe ครั้งเดียวแล้วถาม `get_message()` ทุกรอบลูป 100 ms ตรวจ `is not None` แปลง bytes ด้วย `.decode()` และครอบ `json.loads()` ด้วย `try/except ValueError` จนข้อความที่ไม่ใช่ JSON ไม่ทำให้โปรแกรมหยุด, en: 'Take commands from MQTT Explorer by subscribing once and asking get_message() on every 100 ms loop pass, checking is not None, decoding the bytes with .decode() and wrapping json.loads() in try/except ValueError, so a non-JSON message does not stop the program.'}
  - {th: อธิบายได้ว่าทำไมพอร์ต 1883 เป็นแค่สนามซ้อมที่ปิดล้อม และทำไมการเรียก `mqtt.disconnect()` ตอนเลิกใช้ตามตั้งใจ ทำให้ต่อใหม่ด้วย `client_id` เดิมได้ทันที, en: 'Explain why port 1883 is only a closed practice ground, and why calling mqtt.disconnect() when you stop on purpose lets you reconnect with the same client_id at once.'}
develops: [{skill: proto.mqtt, to: 2}, {skill: iot.cloud-platform, to: 2}, {skill: sec.fundamentals, to: 1}, {skill: soft.problem-solving, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: pending
slides: slides.md
source: {repo: 'https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer', path: session-10.html (slides 16–27), ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079}
---

# บทเรียน 4.5 — MQTT กับแพลตฟอร์มที่ติดตั้งเอง: telemetry และ command

> โมดูล 4 — เชื่อมต่อแพลตฟอร์ม IoT · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

ใช้โมดูล mqtt หกชื่อส่ง JSON จากบอร์ดขึ้น TESAIoT CE ที่ทีมติดตั้งเองและรับคำสั่งกลับมา โดยรู้ทันกับดักพอร์ต 1883 การขึ้นทะเบียนอุปกรณ์ และเพดานเงียบของแต่ละฟังก์ชัน

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. ส่ง JSON ใบแรกขึ้น broker ด้วย `03_connect_and_publish.py` โดยตรวจค่าที่ `mqtt.connect()` คืนก่อนทำงานต่อ และบอกได้ว่าทางออกทั้งสามของ `mqtt.publish()` (True · False · OSError) แต่ละทางแปลว่าอะไร
2. เตรียม TESAIoT CE ให้บอร์ดใน LAN เข้าถึงได้ โดยแก้การเผยแพร่พอร์ตเป็น `0.0.0.0:1883:1883` ขึ้นทะเบียนอุปกรณ์ด้วย `device_id` สั้นไม่เกิน 31 ตัวอักษร และตั้ง `client_id == username == device_id` จน MQTT Explorer ที่ subscribe `device/#` เห็นข้อความของทีม
3. รับคำสั่งจาก MQTT Explorer ด้วยการ subscribe ครั้งเดียวแล้วถาม `get_message()` ทุกรอบลูป 100 ms ตรวจ `is not None` แปลง bytes ด้วย `.decode()` และครอบ `json.loads()` ด้วย `try/except ValueError` จนข้อความที่ไม่ใช่ JSON ไม่ทำให้โปรแกรมหยุด
4. อธิบายได้ว่าทำไมพอร์ต 1883 เป็นแค่สนามซ้อมที่ปิดล้อม และทำไมการเรียก `mqtt.disconnect()` ตอนเลิกใช้ตามตั้งใจ ทำให้ต่อใหม่ด้วย `client_id` เดิมได้ทันที

## ก่อนเริ่ม

ทวนบทเรียน 4.4: topic สองรูป (`bento/<ทีม>/telemetry` บน broker สาธารณะ และ `device/<device_id>/telemetry` บน TESAIoT CE)
เพดาน 31 ตัวอักษรของ `client_id` / `username` / `password` และช่องรับข้อความที่มีช่องเดียว
เตรียมคอมที่มี Docker และ RAM อย่างน้อย 8 GB สำหรับติดตั้ง TESAIoT Community Edition ติดตั้ง MQTT Explorer ไว้
และให้บอร์ดกับคอมอยู่บน WiFi วงเดียวกัน

- **อุปกรณ์:** บอร์ด Eva Kit หรือ TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/) (ซ้อมโค้ดและหน้าจอบน Emulator ได้ ไฟล์ 05 ไม่ต่อเครือข่ายเลย แต่ข้อความไม่ออกไปถึง TESAIoT CE ในแลนของทีม และเมื่อยังไม่ได้ต่อ `publish()` บน Emulator คืน False แทนการโยน OSError การดูผลที่ MQTT Explorer จึงต้องใช้บอร์ดจริง)
- **เรียนมาก่อน:** [บทเรียน 4.4 — MQTT: pub/sub topic QoS และงบข้อมูล](../l04-mqtt-concepts/README.md)

## แนวคิด

โค้ดของชุดบทเรียนนี้สั้นกว่าบทเรียน 3.7–3.9 มาก แต่การตัดสินใจหนักกว่า สิ่งที่ทำให้แล้วคือ TCP/IP การเข้ารหัสแพ็กเก็ต MQTT
การส่ง keepalive และฝั่งแพลตฟอร์มทั้งหมด (broker EMQX บริดจ์ที่ subscribe `device/+/telemetry` รออยู่ ฐานข้อมูลอนุกรมเวลา
และกราฟที่สร้างจากชื่อคีย์ JSON) งานของเราคือสี่คำถาม: **ส่งอะไร ตั้งชื่อว่าอะไร ถี่แค่ไหน และทำอะไรกับคำสั่งที่รับกลับมา**

โมดูล `mqtt` มีหกชื่อเท่านั้น และแต่ละตัวล้มแบบเงียบได้ `connect()` คืน True/False ไม่โยน exception ถ้าไม่ตรวจ
โปรแกรมจะวิ่งต่อแล้ว publish ทุกใบหายเงียบ ชื่อคีย์เวิร์ดคือ `keepalive` ไม่ใช่ `keep_alive` และ `username=` ไม่ใช่ `user=`
(พิมพ์ผิดได้ `TypeError` ทันที) `publish()` มีสามทางออก: ยังไม่ได้ต่อได้ **OSError** · ต่ออยู่แต่ส่งไม่ผ่านได้ False · ส่งต่อให้ชั้นเครือข่ายแล้วได้ True
ซึ่งที่ QoS 0 ไม่ได้แปลว่า broker ได้รับ `publish()` รับแค่สามอาร์กิวเมนต์ ใส่ `retain=True` ได้ `TypeError`
`subscribe()` ที่ broker ปฏิเสธก็คืน False เฉย ๆ `get_message()` ไม่เคยบล็อก คืน `None` หรือ tuple `(topic, payload)`
โดย payload เป็น **bytes** ไม่เกิน 255 ไบต์ ส่วน `disconnect()` คืน `None` จึงห้ามใส่ใน `if` คีย์ `port` ตั้งได้
แต่โมดูลนี้ส่งข้อมูลรับรอง TLS เป็นค่าว่างเสมอ จึงต่อได้เฉพาะพอร์ตข้อความเปล่า

ครึ่งหลังของบทเรียนคือแพลตฟอร์มที่ทีมเป็นเจ้าของเอง ติดตั้ง TESAIoT CE ด้วย `make install` (ธง `PREBUILT=1`) ราว 15–30 นาที
`make up` ต้องมาก่อน `make init-pki` เอกสารทุกฉบับเขียนว่าพอร์ต 1883 แต่ `docker-compose.yml` เผยแพร่จริงเป็น
`127.0.0.1:11883:1883` บอร์ดใน LAN จึงเข้าไม่ถึงเลย ต้องแก้เป็น `0.0.0.0:1883:1883` แล้วใช้ `docker compose up -d emqx`
(`restart` ไม่อ่านพอร์ตใหม่) **ไฟล์ตั้งค่าคือความจริง** เพราะมันคือสิ่งที่เครื่องอ่าน แพลตฟอร์มนี้ไม่มีการลงทะเบียนอัตโนมัติ
ต้องเพิ่มอุปกรณ์ที่ Devices → Add device และตั้ง `device_id` เองให้สั้น เช่น `team03` ถ้าปล่อยให้สุ่มจะได้ UUID ยาว 36 ตัว
ถูกตัดเงียบที่ 31 แล้วต่อไม่ติดโดยไม่บอกสาเหตุ ขอรหัสด้วย `POST /api/v1/devices/<id>/reset-mqtt-password`
(ไม่ใช่ `/reset-password`) ตรวจว่าอุปกรณ์เป็น active และโหมด `server_tls` แล้วกรอกให้ `client_id == username == device_id` ตรงกันเป๊ะ

โค้ดหลักมีสามท่า ท่าที่ 1 ต่อ WiFi แล้ว `mqtt.connect(..., keepalive=60)` ซึ่งแปลว่าเงียบเกิน 60 วินาทีจะโดนตัด ส่งทุก 5 วินาทีจึงปลอดภัย
ท่าที่ 2 อ่าน `sensors.bmi270.motion()` ครั้งเดียวได้หกค่าจากช่วงเวลาเดียวกัน ใน `try` ใช้ `round()` เพราะ `0.12` กิน 4 ไบต์
แทน 12 แล้ว `json.dumps()` แบบแบน บริดจ์ห่อและเติม `device_id` กับ `timestamp` ให้เอง ห่อซ้ำจะได้ชื่อวัดขึ้นต้น `data_`
ท่าที่ 3 subscribe ครั้งเดียว แล้วถาม `get_message()` ทุกรอบ 100 ms คำสั่งจากภายนอกคือข้อมูลที่เราไม่ได้เขียนเอง
จึง `.decode()` แล้วครอบ `json.loads()` ด้วย `try` และจำสถานะ LED ในตัวแปรเอง ส่วนดวงไฟเลือก **ตามชื่อ** ด้วย
`led_named("RGB_GREEN", "LED2")` เพราะเลขดัชนีต่างกันตามบอร์ด ท่าที่ 4 ที่ไม่มีในโครงคือ `mqtt.disconnect()`
ถ้ากด Ctrl-C หรือรันใหม่โดยไม่เรียก broker ยังนับว่าเราอยู่จนครบ `keepalive` และ `client_id` เดิมยังถูกจอง

พอร์ต 1883 **ไม่มีการเข้ารหัส** `username`, `password` และ payload ทุกไบต์เดินบน WiFi เป็นข้อความอ่านออก ใครดักได้ก็ปลอมเป็นอุปกรณ์เรา
ส่งข้อมูลปลอมเข้าแพลตฟอร์มได้ทันที CE เองระบุว่า 1883 มีไว้สำหรับ local/dev เท่านั้น วันนี้จึงเป็นการฝึกในสนามซ้อมที่ปิดล้อม
**"ต่อได้" กับ "ต่อได้อย่างปลอดภัย" เป็นคนละคำถาม** เวลาข้อมูลไม่ขึ้นกราฟ ให้หาว่ากล่องสุดท้ายที่ยังเห็นข้อมูลคือกล่องไหน
ถ้า MQTT Explorer เห็นข้อความ ปัญหาอยู่ที่ topic ผิดรูปหรือ JSON ไม่ถูกต้อง ถ้าไม่เห็น ปัญหายังอยู่ฝั่งบอร์ด

## ตัวอย่างสมบูรณ์

สามไฟล์แรกต้องทำในบทเรียน เปิดตามลำดับนี้ทั้งชุดราว 35 นาที ทุกไฟล์ให้ทายก่อนรันว่าจอจะเป็นอย่างไร

1. `01_topic_design.py` (8 นาที) ดูการ์ดเขียวที่ publish ได้กับการ์ดส้มที่เป็น wildcard แล้วตอบว่าทำไม `+` กับ `#` ใส่ใน publish ไม่ได้
2. `03_connect_and_publish.py` (15 นาที) แก้ค่าบนหัวไฟล์ให้เป็นของทีม ดูป้ายสามขั้น (WiFi · broker · publish) เปลี่ยนเป็นเขียวตามลำดับ
   แล้วนับใน MQTT Explorer ว่าครบสิบข้อความไหม จากนั้นลองใส่ IP ของ broker ผิดหนึ่งครั้ง เพื่อจำว่าขั้นไหนล้มและล้มหน้าตาอย่างไร
3. `04_subscribe_command.py` (12 นาที) ส่ง `{"cmd":"beep"}` หรือ `{"cmd":"count"}` จาก MQTT Explorer แล้วลองส่งข้อความที่ไม่ใช่ JSON
   ดูว่าโปรแกรมไม่หยุด ส่วนการสลับ LED ด้วย `{"cmd":"toggle"}` ทำจริงในไฟล์ฝึกของบทเรียน 4.6

ติดตรงไหนเปิดไฟล์ที่ตอบอาการนั้น: ส่งได้แต่สั่งกลับไม่ตอบ เปิด `05_send_every_5s_still_listen.py` (ไม่ต้องต่อเครือข่าย ลองแก้ `LOOP_MS`
กับ `SEND_EVERY_MS` แล้วรันซ้ำ) · ไม่แน่ใจว่าจะใส่ฟิลด์อะไร เปิด `02_payload_shape.py` · โค้ดบอกว่าส่งแล้วแต่ MQTT Explorer ไม่เห็น
เปิด `06_sent_is_not_delivered.py` ซึ่งนับที่ปลายทาง ไม่ใช่นับที่ต้นทาง · อยากเห็นว่า `disconnect()` คืนชื่อให้ว่างจริง เปิด `07_disconnect_frees_id.py`

ไฟล์ตัวอย่างตั้ง topic เป็นรูป `bento/team03/...` และไฟล์ 04, 06, 07 เรียก `mqtt.connect()` โดยไม่ใส่ `username=` กับ `password=`
ถ้าจะรันกับ CE ของทีม ต้องเติมสองค่านี้ (CE ปฏิเสธอุปกรณ์ที่ไม่รู้จักตั้งแต่ตอน CONNECT) และใช้ topic รูป `device/<device_id>/...`

| ไฟล์ | ไฟล์นี้สอน |
|---|---|
| [examples/01_topic_design.py](examples/01_topic_design.py) | ออกแบบชื่อ topic ก่อนเขียนโค้ดส่ง |
| [examples/02_payload_shape.py](examples/02_payload_shape.py) | รูปร่างของ payload ตัดสินว่าฝั่งรับทำงานง่ายหรือยาก |
| [examples/03_connect_and_publish.py](examples/03_connect_and_publish.py) | ต่อ broker แล้วส่งค่าขึ้นไปหนึ่งชุด |
| [examples/04_subscribe_command.py](examples/04_subscribe_command.py) | รับคำสั่งจากข้างนอก แล้วทำตาม |
| [examples/05_send_every_5s_still_listen.py](examples/05_send_every_5s_still_listen.py) | ส่งทุก 5 วินาที แต่ยังรับคำสั่งได้ทุก 100 ms |
| [examples/06_sent_is_not_delivered.py](examples/06_sent_is_not_delivered.py) | publish คืน True แปลว่าอะไร และไม่แปลว่าอะไร |
| [examples/07_disconnect_frees_id.py](examples/07_disconnect_frees_id.py) | บอกลา broker ให้ถูกวิธี แล้วต่อใหม่ด้วยชื่อเดิมได้ทันที |

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นด้วย:

- [m04-iot-connectivity/l06-mqtt-telemetry-lab/practice/s10_mqtt_telemetry.py](../l06-mqtt-telemetry-lab/practice/s10_mqtt_telemetry.py) — ส่ง telemetry ขึ้น broker และรับคำสั่งกลับ (ฉบับฝึกเติมโค้ด)
- [m04-iot-connectivity/l08-tesaiot-module/examples/06_secure_publish_loop.py](../l08-tesaiot-module/examples/06_secure_publish_loop.py) — ส่งขึ้นแพลตฟอร์มผ่าน TLS แล้วโชว์หลักฐานบนจอ

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. ข้อใดถูกเกี่ยวกับค่าที่ `mqtt.publish(topic, payload)` คืน เลือกทุกข้อที่ถูก *(เลือกได้หลายข้อ · เป้าหมายข้อ 1)*
   - ก) เรียกตอนยังไม่ได้ต่อ broker จะได้ OSError ไม่ใช่ False
   - ข) ต่ออยู่แต่ส่งไม่ผ่านจะได้ False
   - ค) ได้ True แปลว่า broker ได้รับข้อความแล้วแน่นอน
   - ง) ใส่ `retain=True` เพิ่มได้ถ้าอยากให้ broker จำข้อความล่าสุด

   <details><summary>เฉลย</summary>

   **ก, ข** — publish() มีสามทางออก OSError เมื่อยังไม่ได้ต่อ False เมื่อต่ออยู่แต่ส่งไม่ผ่าน และ True ที่แปลแค่ว่าส่งต่อให้ชั้นเครือข่ายแล้ว ที่ QoS 0 ไม่มีการยืนยันจาก broker ส่วน retain ไม่ใช่พารามิเตอร์ ใส่ไปได้ TypeError

   </details>

2. ทีมติดตั้ง TESAIoT CE เสร็จ เอกสารบอกพอร์ต 1883 แต่บอร์ดที่อยู่ใน LAN เดียวกันต่อ broker ไม่ได้เลย ควรแก้อย่างไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) แก้ `docker-compose.yml` จาก `127.0.0.1:11883:1883` เป็น `0.0.0.0:1883:1883` แล้วสั่ง `docker compose up -d emqx`
   - ข) แก้ไฟล์เดียวกันแล้วสั่ง `docker compose restart` ก็พอ
   - ค) ใส่ `BROKER = "localhost"` ในโค้ดบนบอร์ด
   - ง) เปลี่ยนไปต่อพอร์ต 8884 ด้วยโมดูล `mqtt`

   <details><summary>เฉลย</summary>

   **ก** — ไฟล์ตั้งค่าเผยแพร่จริงเป็น 11883 และผูกกับ loopback บอร์ดจึงเข้าไม่ถึง ต้องแก้เป็น 0.0.0.0:1883 และใช้ up -d เพราะ restart ไม่อ่านพอร์ตใหม่ localhost ชี้ไปที่ตัวบอร์ดเอง และโมดูล mqtt ต่อพอร์ต TLS ไม่ได้

   </details>

3. เรียงขั้นของการรับคำสั่ง toggle จาก broker มาสลับ LED ให้ถูกลำดับ *(เรียงลำดับ · เป้าหมายข้อ 3)*
   - ก) แปลง `msg[1].decode()` แล้ว `json.loads()` ภายใน `try/except ValueError`
   - ข) เรียก `mqtt.subscribe(TOPIC_CMD)` ครั้งเดียวก่อนเข้าลูป
   - ค) ถ้า `cmd.get("cmd") == "toggle"` สลับตัวแปร `led_on` ที่จำไว้เอง แล้วสั่ง `lamp.value(...)`
   - ง) เรียก `mqtt.get_message()` ทุกรอบลูป 100 ms
   - จ) ตรวจว่า `msg is not None`

   <details><summary>เฉลย</summary>

   **ข → ง → จ → ก → ค** — subscribe ครั้งเดียวแล้วถาม get_message() ทุกรอบ ซึ่งคืน None เมื่อไม่มีข้อความจึงต้องตรวจก่อน payload เป็น bytes ต้อง decode ก่อน json.loads และครอบ try เพราะคนส่งมั่วได้เสมอ สถานะ LED ต้องจำเอง เพราะค่าของขาบอกแค่ระดับ ณ วินาทีที่ถาม

   </details>

4. ทีมกด Ctrl-C แล้วรันไฟล์เดิมใหม่ทันที บอร์ดต่อติดแล้วหลุดสลับกันทั้งที่โค้ดไม่ผิด สาเหตุและทางแก้ที่ตรงที่สุดคืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 4)*
   - ก) broker ยังนับว่าตัวเก่าอยู่จนครบ keepalive และ client_id เดิมยังถูกจอง ให้เรียก `mqtt.disconnect()` ใน `except KeyboardInterrupt:`
   - ข) keepalive สั้นเกินไป ให้ตั้ง `keep_alive=600`
   - ค) ต้องเรียก `if mqtt.disconnect():` ก่อน connect ทุกครั้ง
   - ง) บอร์ดเสีย ต้องลงเฟิร์มแวร์ใหม่

   <details><summary>เฉลย</summary>

   **ก** — ถ้าไม่บอกลา broker รอจนครบ keepalive กว่าจะยอมรับว่าเราไปแล้ว disconnect() คืนชื่อให้ว่างทันที แต่คืน None จึงใส่ใน if ไม่ได้ และคีย์เวิร์ดที่ถูกคือ keepalive ไม่ใช่ keep_alive

   </details>

5. คนที่ดักจับสัญญาณ WiFi ห้องเรียนได้ ทำอะไรได้บ้างเมื่อบอร์ดของทีมส่งผ่านพอร์ต 1883 เลือกทุกข้อที่ถูก *(เลือกได้หลายข้อ · เป้าหมายข้อ 4)*
   - ก) อ่าน username และ password ของทีมได้
   - ข) อ่านค่าเซนเซอร์ใน payload ได้
   - ค) ปลอมเป็นอุปกรณ์ของทีมส่งข้อมูลปลอมเข้าแพลตฟอร์มได้
   - ง) ไม่ได้อะไรเลย เพราะ broker ขอรหัสผ่านก่อนต่อ

   <details><summary>เฉลย</summary>

   **ก, ข, ค** — พอร์ต 1883 ไม่มีการเข้ารหัส ทุกไบต์รวมถึงรหัสผ่านเดินเป็นข้อความอ่านออก การขอรหัสผ่านไม่ช่วยเมื่อรหัสเองถูกอ่านได้ จึงใช้ 1883 ได้แค่ในสนามซ้อม ต่อได้กับต่อได้อย่างปลอดภัยเป็นคนละคำถาม

   </details>

## แล็บ

**เตรียมแพลตฟอร์มของทีม** ทำบนคอมของทีมกับบอร์ดจริง แล้วจดผลลงบันทึกการเรียน

- [ ] ติดตั้ง TESAIoT CE ด้วย `make install` โดยเรียก `make up` ก่อน `make init-pki`
- [ ] แก้ `docker-compose.yml` จาก `127.0.0.1:11883:1883` เป็น `0.0.0.0:1883:1883` สั่ง `docker compose up -d emqx` แล้วดู `docker compose ps` ว่าพอร์ตขึ้นเป็น `0.0.0.0:1883` จริง
- [ ] Devices → Add device ด้วย `device_id` สั้นที่ตั้งเอง ขอรหัสด้วย `reset-mqtt-password` และตรวจว่าเป็น active กับ `server_tls`
- [ ] หา IP ของคอมใน LAN (ไม่ใช่ localhost) แล้ว `wifi.ping()` จากบอร์ดให้ผ่านก่อนแตะ MQTT
- [ ] ต่อ MQTT Explorer ไปที่ IP เดียวกัน พอร์ต 1883 ด้วยชื่อและรหัสของทีม แล้ว subscribe `device/#` ไว้
- [ ] รัน `03_connect_and_publish.py` ด้วย `client_id == username == device_id` และ topic `device/<device_id>/telemetry` จนเห็นข้อความใน MQTT Explorer
- [ ] เขียนหนึ่งประโยคในบันทึกการเรียนว่าคนดักฟังบน WiFi ห้องเรียนเห็นอะไรบ้างเมื่อเราใช้พอร์ต 1883

## ไปต่อ

บทเรียน 4.6 ประกอบทุกท่าเป็นโปรแกรมเดียวใน `s10_mqtt_telemetry.py` ส่งค่าจริงทุก 5 วินาทีและรับ `{"cmd":"toggle"}` กลับมาสลับ LED
อ่านเสริมนอกเวลาได้ที่ `06_secure_publish_loop.py` ของบทเรียน 4.8 ซึ่งเป็นลูปเดียวกันบนช่องที่เข้ารหัส เปิดอ่านเทียบโครงได้ แต่อย่าเพิ่งรัน

บทเรียนถัดไป: [บทเรียน 4.6 — ลงมือทำ: telemetry สองทาง](../l06-mqtt-telemetry-lab/README.md)

## สะท้อนคิด

- เอกสารของ CE กับ `docker-compose.yml` ขัดกันเรื่องพอร์ต คุณจะเช็กอะไรก่อนเมื่อเจอระบบใหม่ครั้งหน้า
- ถ้ามีคนในห้องดักรหัส MQTT ของทีมไปได้ เขาทำอะไรกับแพลตฟอร์มของเราได้บ้าง
- ตัวนับ True จาก `publish()` เป็นหลักฐานว่าส่งถึงได้หรือไม่ ถ้าไม่ได้ หลักฐานที่เชื่อได้คืออะไร
