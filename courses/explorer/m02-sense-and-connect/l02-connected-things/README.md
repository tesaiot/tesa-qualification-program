---
id: explore.m02.l02
lang: th
title:
  th: "ของที่คุยกันได้: MQTT และแดชบอร์ด"
  en: "Connected things: MQTT and a dashboard"
summary:
  th: เข้าใจว่า MQTT ส่งข้อความผ่าน broker อย่างไร แล้วส่งค่าเซนเซอร์ขึ้น broker สาธารณะให้ไปโผล่บนหน้าเว็บอ่านค่า
  en: Understand how MQTT moves messages through a broker, then publish sensor values to a public broker and watch them on a web page.
level: L1
time_min: {concept: 12, practise: 13, check: 5}
hardware: {emulator: true, boards: [none, eva-kit, devkit]}
prerequisites: [explore.m02.l01]
objectives:
  - th: อธิบายบทบาทของ broker, topic, publish และ subscribe ได้ด้วยแผนภาพหรือคำพูดของตัวเอง
    en: Explain the roles of broker, topic, publish and subscribe with a diagram or in your own words.
  - th: แก้ค่า TEAM ในตัวอย่าง รันให้ค่าเซนเซอร์ขึ้นหน้าเว็บอ่านค่า หรืออธิบายได้ว่าติดที่ขั้นไหนจากป้ายบนจอ
    en: Edit TEAM in the example and run it until sensor values reach the reader page, or explain from the on-screen steps where it stopped.
  - th: ระบุความเสี่ยงของการส่งข้อมูลผ่าน broker สาธารณะที่พอร์ต 1883 ได้อย่างน้อย 2 ข้อ
    en: Name at least two risks of sending data through a public broker on port 1883.
develops:
  - {skill: iot.fundamentals, to: 1}
  - {skill: proto.mqtt, to: 1}
  - {skill: sec.fundamentals, to: 1}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide, emulator: bento-emulator, broker: broker.hivemq.com}
status: alpha
translation: pending
source:
  repo: https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer
  path: examples/s02/05_value_leaves_the_board.py
  ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079
---

## เป้าหมาย

1. อธิบายบทบาทของ broker, topic, publish และ subscribe ได้
2. รันตัวอย่างให้ค่าเซนเซอร์ขึ้นหน้าเว็บอ่านค่า หรือบอกได้ว่าติดที่ขั้นไหน
3. ระบุความเสี่ยงของ broker สาธารณะที่ไม่เข้ารหัสได้อย่างน้อย 2 ข้อ

## ก่อนเริ่ม

- ในบทที่แล้ว คีย์ไหนของ `sensors.snapshot()` เก็บค่าลูกบิด
- ถ้าอยากให้เพื่อนอีกจังหวัดเห็นค่าลูกบิดบนบอร์ดของเรา ข้อมูลต้องเดินทางผ่านอะไรบ้าง

## ดูของจริงก่อน

บทนี้เป็นตัวอย่างนำทาง (guided example) ทำตามทีละขั้น

1. เปิด [examples/01_send_to_dashboard.py](examples/01_send_to_dashboard.py) ใน BENTO IDE
2. แก้บรรทัด `TEAM = "teamXX"` เป็นเลขสองหลักที่คุณเลือกเอง เช่น `"team37"` (ห้ามใช้ `team00`)
3. **ถ้าใช้บอร์ดจริง** แก้ `WIFI_SSID` กับ `WIFI_PASS` เป็นวง WiFi ที่บอร์ดต่อได้ (WiFi ที่ต้องล็อกอินผ่านหน้าเว็บมักใช้กับบอร์ดไม่ได้ ใช้ Hotspot มือถือแทน)
   **ถ้าใช้ BENTO Emulator** ไม่ต้องแก้สองบรรทัดนี้ WiFi ในอีมูเลเตอร์เป็นของจำลอง
4. เปิดแท็บใหม่ในเบราว์เซอร์ ไปที่หน้าอ่านค่าของหลักสูตร AIoT in Action แล้วต่อท้ายด้วยเลขทีมเดียวกัน เช่น
   `https://advance-innovation-centre-aic.github.io/embedded-systems-for-aiot-developer/examples/web/my_first_reader.html?team=team37`
5. กลับมารันโปรแกรม ดูป้ายสามขั้นบนจอเปลี่ยนเป็นสีเขียว แล้วดูหน้าเว็บ กล่องตัวเลข `knob` และ `az` ควรขึ้นมาและเปลี่ยนทุก 2 วินาที
6. หมุนลูกบิดหรือเอียงบอร์ด (ในอีมูเลเตอร์ใช้แผง **HW**) แล้วดูเลขบนหน้าเว็บขยับตาม

**เรื่องที่ต้องรู้ถ้าใช้อีมูเลเตอร์** อีมูเลเตอร์พยายามต่อ broker สาธารณะจริงผ่านเบราว์เซอร์ ถ้าต่อไม่ได้ภายในไม่กี่วินาที
มันจะแจ้งในลิ้นชัก Console แล้วถอยไปใช้ broker จำลองในเบราว์เซอร์แทน กรณีนั้นข้อความจะไม่ออกจากเครื่องของคุณ และหน้าเว็บจะไม่เห็นอะไร
ถ้าเจอแบบนี้ ไม่ใช่ความผิดของโค้ด ลองใหม่ภายหลัง หรือลองจากเครือข่ายอื่น

## แนวคิด

### 1. ไปรษณีย์กลางชื่อ broker

**MQTT** เป็นวิธีส่งข้อความสั้น ๆ ระหว่างอุปกรณ์ที่นิยมมากในงาน IoT หัวใจของมันคือ **broker** ซึ่งเปรียบได้กับไปรษณีย์กลาง

- อุปกรณ์ที่มีข้อมูลจะ **publish** (ส่ง) ข้อความไปที่ broker พร้อมระบุ **topic** (หัวข้อ) เช่น `bento-aiot/team37/telemetry`
- ใครก็ตามที่อยากรู้เรื่องนั้นจะ **subscribe** (บอกรับ) หัวข้อนั้นไว้กับ broker
- broker ส่งต่อข้อความให้ทุกคนที่บอกรับหัวข้อนั้น ผู้ส่งกับผู้รับไม่ต้องรู้จักกันเลย

```
  บอร์ด ──publish──►  broker  ──ส่งต่อ──►  หน้าเว็บที่ subscribe ไว้
          bento-aiot/team37/telemetry
```

ในตัวอย่างนี้ บอร์ด (หรืออีมูเลเตอร์) เป็นผู้ publish และหน้าเว็บอ่านค่าเป็นผู้ subscribe หัวข้อ `bento-aiot/team37/#`
เครื่องหมาย `#` แปลว่า "ทุกหัวข้อย่อยที่อยู่ใต้นี้"

### 2. บันไดสามขั้นที่ห้ามสลับ

ข้อมูลจะออกจากบอร์ดได้ต้องผ่านสามขั้นตามลำดับ **WiFi ต้องได้เลข IP ก่อน** จึง **แนะนำตัวกับ broker** ได้ แล้วจึง **publish** ได้
ตัวอย่างวาดป้ายสามขั้นบนจอ ขั้นที่ผ่านเป็นสีเขียว ขั้นที่ไม่ผ่านเป็นสีแดงพร้อมเหตุผล โปรแกรมที่ดีบอกได้เสมอว่าติดที่ขั้นไหน

### 3. ข้อความหน้าตาอย่างไร

ค่าที่ส่งถูกจัดเป็นข้อความรูปแบบ **JSON** ด้วย `json.dumps()` เช่น

```json
{"id": "team37", "n": 5, "knob": 42, "az": 9.79}
```

หน้าเว็บอ่านค่าวาดกล่องหนึ่งกล่องต่อหนึ่งคีย์ จึงไม่ต้องแก้หน้าเว็บเมื่อเราเพิ่มคีย์ใหม่

### 4. broker สาธารณะไม่ใช่ที่ส่งความลับ

`broker.hivemq.com` ที่พอร์ต 1883 เปิดให้ทุกคนใช้ฟรีและ **ไม่เข้ารหัส** ใครก็ subscribe หัวข้อของเราได้ และใครก็ publish ปลอมเข้ามาในหัวข้อเดียวกันได้
ถ้ามีคนเลือกเลขทีมเดียวกับคุณ คุณอาจเห็นค่าของเขาปนมา เหมาะกับการเรียนเท่านั้น
งานจริงใช้ **MQTTs** (MQTT ผ่าน TLS ที่เข้ารหัส) กับ broker ที่ต้องยืนยันตัวตน ซึ่งเป็นเรื่องในหลักสูตรระดับถัดไป

## ตัวอย่างสมบูรณ์

[examples/01_send_to_dashboard.py](examples/01_send_to_dashboard.py) ย่อมาจาก
[`examples/s02/05_value_leaves_the_board.py`](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/s02/05_value_leaves_the_board.py)
ของหลักสูตร AIoT in Action ส่วนหน้าเว็บอ่านค่าคือ
[`examples/web/my_first_reader.html`](https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer/blob/a80bbe88a34bcb9bb8d991f42f9252b77cdab079/examples/web/my_first_reader.html)
ของหลักสูตรเดียวกัน

- **ท่าที่ 1 ตรวจ TEAM** ถ้ายังเป็น `teamXX` โปรแกรมไม่ยอมรัน เพราะชื่อที่ซ้ำกับคนอื่นจะทำให้ broker เตะอีกฝั่งหลุด
- **ท่าที่ 2 WiFi** `wifi.connect(ssid, password)` คืน `True` หรือ `False` แล้วถาม `wifi.ip()` ว่าได้เลข IP จริงไหม (`"0.0.0.0"` แปลว่ายังไม่ได้)
- **ท่าที่ 3 broker** `mqtt.connect(BROKER, port=1883, client_id=..., keepalive=60)` คืน `True` เมื่อต่อสำเร็จ
- **ท่าที่ 4 publish** อ่านเซนเซอร์ ประกอบ JSON แล้ว `mqtt.publish(TOPIC, body)` ทุก 2 วินาที ดักทั้ง `False` และ `OSError`
- **ท่าที่ 5 สรุป** `mqtt.is_connected()` ตอบว่า "ตอนนี้" ยังต่ออยู่ไหม

## เช็กความเข้าใจ

ตอบคำถามใน [quiz.yaml](quiz.yaml) ถูกตั้งแต่ 80% ขึ้นไปถือว่าผ่าน

## แล็บ

วาดแผนภาพของคุณเองบนกระดาษ แสดงเส้นทางของข้อความหนึ่งใบจากลูกบิดไปจนถึงตัวเลขบนหน้าเว็บ ให้มีคำว่า broker, topic, publish และ subscribe ครบ
ถ่ายรูปแผนภาพคู่กับภาพหน้าจอหน้าเว็บที่เห็นค่าของคุณ (หรือภาพป้ายบนจอที่บอกว่าติดขั้นไหน) เก็บไว้ใน portfolio

## ไปต่อ

- หลักสูตร [AIoT in Action](../../../aiot-micropython/README.md) ต่อยอดเรื่องนี้ไปถึงการรับคำสั่งกลับจากหน้าเว็บ และการส่งข้อมูลแบบเข้ารหัสขึ้น TESAIoT Platform
- อ่านเพิ่มเรื่อง MQTT ได้ที่ https://mqtt.org/

## สะท้อนคิด

ถ้าจะใช้ระบบแบบนี้เฝ้าตู้แช่ของร้านค้า ข้อมูลอะไรที่คุณยอมให้คนอื่นเห็นได้ และข้อมูลอะไรที่ต้องไม่หลุดออกไปเด็ดขาด
