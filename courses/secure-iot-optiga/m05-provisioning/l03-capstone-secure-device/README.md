---
id: sec-iot.m05.l03
lang: th
title: {th: 'งานปลายทาง: อุปกรณ์ที่ปลอดภัยหนึ่งชิ้น', en: 'Capstone: one secure device'}
summary: {th: รวม threat model การลงทะเบียน mTLS และการอัปเดตแบบป้องกัน เป็นอุปกรณ์หนึ่งชิ้นพร้อมหลักฐาน, en: 'Combine the threat model, enrolment, mTLS and protected update into one device with evidence.'}
level: L3
time_min: {concept: 5, practise: 10, lab: 55, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m05.l02]
objectives:
- {th: ส่งอุปกรณ์ที่ลงทะเบียนแล้ว เชื่อมต่อด้วย mTLS และส่งข้อมูลขึ้นแพลตฟอร์มได้ พร้อม log เป็นหลักฐาน, en: 'Deliver an enrolled device that connects over mTLS and publishes to the platform, with logs as evidence.'}
- {th: ปรับ threat model จากโมดูลแรกให้สะท้อนมาตรการที่ทำจริง และระบุความเสี่ยงที่ยังเหลือ, en: Update the module-one threat model to reflect implemented mitigations and remaining risks.}
develops:
- {skill: sec.fundamentals, to: 3}
- {skill: iot.cloud-platform, to: 3}
- {skill: soft.communication, to: 2}
assesses:
- {skill: sec.fundamentals, level: 3, evidence: resources/evidence-checklist.md}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
source:
- {repo: 'https://github.com/tesaiot/tesaiot-pse84-devkit-sdk', path: bento-firmware-template-mtb-only, ref: ef72c1b658178eee8c38b1e47d28b006f80a59b5, license: Apache-2.0}
---

# บทเรียน 5.3: งานปลายทาง อุปกรณ์ที่ปลอดภัยหนึ่งชิ้น

> โมดูล 5 · การลงทะเบียนอุปกรณ์อย่างปลอดภัย · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

งานชิ้นสุดท้ายไม่ได้วัดว่าอุปกรณ์ "ดูเหมือนทำงาน" แต่วัดว่าคุณ **พิสูจน์** ได้ไหมว่ามันทำงานตามที่อ้าง
คุณจะส่งอุปกรณ์หนึ่งเครื่องที่ลงทะเบียนแล้ว เชื่อม mTLS ด้วยกุญแจในชิป ส่งข้อมูลขึ้นแพลตฟอร์ม และ threat model ที่อัปเดตตามความจริง

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. ส่งอุปกรณ์ที่ลงทะเบียนแล้ว เชื่อมต่อด้วย mTLS และส่งข้อมูลขึ้นแพลตฟอร์มได้ พร้อม log เป็นหลักฐาน
2. ปรับ threat model จากโมดูลแรกให้สะท้อนมาตรการที่ทำจริง และระบุความเสี่ยงที่ยังเหลือ

## ก่อนเริ่ม

- **เรียนมาก่อน:** ทุกบทเรียนในหลักสูตรนี้ โดยเฉพาะแล็บของ [3.1](../../m03-mtls-to-platform/l01-tls-and-mtls/README.md), [3.2](../../m03-mtls-to-platform/l02-mqtts-to-tesaiot/README.md) และ [5.1](../l01-csr-enrolment/README.md)
- **ไฟล์ที่ต้องมี:** threat model ของคุณจาก [บทเรียน 1.1](../../m01-threats-and-crypto/l01-threat-modelling/README.md) และแม่แบบรายงาน [resources/evidence-checklist.md](resources/evidence-checklist.md)
- **อุปกรณ์:** TESAIoT Dev Kit ที่ลงทะเบียนบน TESAIoT Platform แล้ว มีไฟล์ตั้งค่าที่เชื่อมต่อได้ และแม่แบบของ SDK ที่ apply patch ครบ (บทเรียน 3.1)
- **การอนุมัติ:** การลงทะเบียนจริงสร้างกุญแจใหม่ในชิป และ Protected Update ทำให้ตัวนับ version ขึ้นถาวร ทั้งสองอย่างต้องได้รับอนุญาตจากผู้สอนก่อน
  งานนี้ **ไม่มีขั้นใดเขียน metadata tag `C0`** ถ้าค่า `C0` ของช่องใดเปลี่ยนไประหว่างงาน ให้หยุดและรายงานทันที

## ดูของจริงก่อน

ตลอดหลักสูตรเราเจอกรณีเดียวกันซ้ำหลายครั้ง บรรทัดที่ดูเหมือนสำเร็จ ไม่ได้แปลว่าสำเร็จ

- `[PSA-Sign] Using Key OID ...` พิมพ์ **ก่อน** การลงนาม (บทเรียน 3.1)
- `tesaiot_mqtt_publish()` คืน `true` แปลว่า **เข้าคิว** ไม่ใช่ถึง broker (บทเรียน 3.2)
- `tesaiot_publish_protected_update()` คืน `0` แปลว่า **ขอแล้ว** ไม่ใช่เสร็จแล้ว (บทเรียน 4.2)
- ฟังก์ชัน `ota_verify_firmware()` คืน `OTA_OK` โดยไม่ได้ตรวจอะไรเลย (บทเรียน 4.2)

**ถามตัวเองก่อนเริ่ม:** สำหรับแต่ละข้อข้างบน หลักฐานที่ **ถูก** คืออะไร และได้มาจากฝั่งไหน

## แนวคิด

หลักฐานในงานนี้มีสี่ชนิด เรียงจากอ่อนไปแข็ง

1. **ข้อความที่อุปกรณ์พิมพ์** ใช้ได้เมื่อรู้ว่าบรรทัดนั้นพิมพ์ตอนไหน และมีบรรทัด error ที่ต้อง **ไม่** ปรากฏประกอบ
2. **สถานะที่อ่านกลับจากชิป** เช่น metadata ของ `0xE0E1` ก่อนและหลัง ชิปตอบตามความจริงไม่ว่า host จะพิมพ์อะไร
3. **หลักฐานจากฝั่งผู้รับ** เช่นข้อมูลที่ไปถึงผู้ subscribe หรือสิ่งที่แพลตฟอร์มบันทึก
4. **การทดสอบด้านลบ** กรณีที่ **ควรล้ม** และล้มจริง เช่นพอร์ต mTLS ปฏิเสธ client ที่ไม่มีใบรับรอง มาตรการที่ไม่เคยถูกทดสอบให้ล้ม ยังไม่ได้พิสูจน์อะไร

และหลักฐานต้อง **ไม่รั่ว** ห้ามแนบรหัสผ่าน MQTT รหัส WiFi หรือไฟล์ใน bundle ลงรายงาน log ของเฟิร์มแวร์ถูกออกแบบให้พิมพ์แค่ความยาวของรหัสอยู่แล้ว (`PassLen`, `passphrase=N byte(s)`)
ถ้ารายงานจะเผยแพร่ ให้แทน `device_id` และ UID ของชิปด้วยค่าที่ปิดบางส่วน

threat model ที่อัปเดตแล้วต้องบอกตรง ๆ ว่าอะไรยังไม่ได้ป้องกัน หลักสูตรนี้เจอความเสี่ยงที่ยังเหลือของแม่แบบที่ commit `ef72c1b` อย่างน้อยเท่านี้

| ความเสี่ยงที่ยังเหลือ | มาจากบทเรียน |
|---|---|
| ชิปกันการขโมยกุญแจ แต่กันเฟิร์มแวร์ที่ถูกยึดไม่ให้สั่งลงนามไม่ได้ | 1.2 |
| อุปกรณ์ไม่ตรวจวันหมดอายุและการเพิกถอนของใบรับรอง (`MBEDTLS_HAVE_TIME_DATE` และ CRL ปิดอยู่) | 1.2 |
| สาย I2C ระหว่าง MCU กับชิปไม่ได้เข้ารหัสในค่าตั้งเริ่มต้น | 1.2 |
| TLS 1.2 ส่งใบรับรองของอุปกรณ์แบบไม่เข้ารหัสใน handshake | 3.1 |
| ถ้าใช้ใบจากโรงงาน ตัวตนผูกกับอุปกรณ์ได้ด้วย ACL ฝั่ง broker เท่านั้น | 3.1 |
| ไฟล์ตั้งค่าบน LittleFS ที่มีรหัส WiFi ไม่ได้ระบุว่าเข้ารหัส | 3.2 |
| ห่วงโซ่ secure boot ในแม่แบบครอบแค่ CM33_S และเปิดเฉพาะเมื่อ provision แล้ว | 4.1 |
| OTA client ตัวอย่างยังไม่ตรวจ hash และลายเซ็นของเฟิร์มแวร์ | 4.2 |

## ตัวอย่างสมบูรณ์

นี่คือตัวอย่างการกรอกตารางหลักฐานหนึ่งแถว สำหรับข้อ "เชื่อม mTLS ด้วยตัวตนที่ลงทะเบียนแล้ว" ค่าในวงเล็บแหลมคือของจริงจากบอร์ดคุณ

| ข้ออ้าง | หลักฐานบวก | หลักฐานลบ | ชนิด |
|---|---|---|---|
| อุปกรณ์เชื่อม broker ด้วย mTLS และชิปเป็นผู้ลงนามด้วยกุญแจของ TESAIoT | UART: `[mTLS] device pair verified — using TESAIoT identity`, `[PSA-Sign] Using Key OID 0xE0F1 ...`, `[MQTT] Connected to broker` ภายในการเชื่อมต่อเดียวกัน | ไม่มีบรรทัด `[PSA-Sign] ERROR: trustm_ecdsa_sign status=...` · จากคอมพิวเตอร์ `openssl s_client` ที่พอร์ต 8883 โดยไม่มีใบของ client ถูกปฏิเสธด้วย alert | 1 และ 4 |

สังเกตว่าหลักฐานบวกมีสามบรรทัด เพราะบรรทัดเดียวไม่พอ (บทเรียน 3.1) และหลักฐานลบพิสูจน์ว่าพอร์ตนั้นต้องการใบรับรองจริง ไม่ใช่ปล่อยทุกคนเข้า
แถวอื่นในแม่แบบ [resources/evidence-checklist.md](resources/evidence-checklist.md) ใช้รูปแบบเดียวกัน

## ฝึกเติม

จัดแต่ละข้อว่าเป็นหลักฐานชนิดไหน (1 ข้อความจากอุปกรณ์ · 2 สถานะจากชิป · 3 ฝั่งผู้รับ · 4 การทดสอบด้านลบ) หรือ **ไม่ใช่หลักฐาน**

1. `mosquitto_sub` ที่ subscribe ไว้ก่อน ได้รับ payload ที่อุปกรณ์ publish ____
2. `optiga.read_metadata(0xE0E1)` ก่อนและหลัง Protected Update ได้ `D0` เปลี่ยนเป็นค่าที่ระบุ anchor และ `C0` เท่าเดิม ____
3. `tesaiot_mqtt_publish()` คืน `true` ____
4. การต่อพอร์ต 8884 โดยไม่ใส่ CA ได้ `Verify return code: 20` ____
5. ภาพถ่ายหน้าจอที่ขึ้น "The device can prove it holds the key this certificate names" ____

<details><summary>เฉลย</summary>

1. **3** ฝั่งผู้รับ
2. **2** สถานะจากชิป ชิปตอบตามจริงเสมอ
3. **ไม่ใช่หลักฐาน** ว่าข้อมูลถึง แปลแค่ว่าเข้าคิว
4. **4** การทดสอบด้านลบ พิสูจน์ว่าการตรวจใบของเซิร์ฟเวอร์ต้องมี anchor ที่ถูก
5. **1** ข้อความจากอุปกรณ์ ประโยคนี้มาจาก `prov_say()` หลังการตรวจคู่ใบกับกุญแจ มีน้ำหนักเมื่อแนบ log บน UART ของรอบเดียวกันด้วย

</details>

## เช็กความเข้าใจ

คำถามข้างล่างเป็นส่วนหนึ่งของชุดเต็มใน [quiz.yaml](quiz.yaml) ซึ่งระบบตรวจอัตโนมัติใช้

1. หลักฐานชุดใดพอจะอ้างว่า "ชิปลงนาม CertificateVerify สำเร็จด้วยกุญแจที่ลงทะเบียนแล้ว" *(เป้าหมายข้อ 1)*
   - ก) บรรทัด `[PSA-Sign] Using Key OID 0xE0F1` อย่างเดียว
   - ข) บรรทัด device pair verified, บรรทัด Using Key OID 0xE0F1, ไม่มีบรรทัด ERROR ของ `trustm_ecdsa_sign` และ `[MQTT] Connected to broker` ในการเชื่อมต่อเดียวกัน
   - ค) หน้าจอขึ้นว่าเชื่อมต่อแล้ว
   - ง) `tesaiot_mqtt_connect()` คืน `true`

   <details><summary>เฉลย</summary>

   **ข** ตามเกณฑ์ของบท C4 ที่เราใช้ในบทเรียน 3.1

   </details>

2. ข้อใดควรอยู่ในช่อง "ความเสี่ยงที่ยังเหลือ" ของ threat model หลังทำงานนี้เสร็จ *(เป้าหมายข้อ 2)*
   - ก) ไม่มี เพราะใช้ mTLS แล้ว
   - ข) ห่วงโซ่ secure boot ครอบแค่ CM33_S และอุปกรณ์ไม่ตรวจวันหมดอายุของใบรับรอง
   - ค) กุญแจลับอยู่ใน flash
   - ง) รหัสผ่าน MQTT ถูกพิมพ์บน console

   <details><summary>เฉลย</summary>

   **ข** ข้อ ค และ ง ไม่จริงในอุปกรณ์ที่ทำตามหลักสูตร ข้อ ก คือการทำ threat model แบบปิดตา mTLS ไม่ได้แก้ทุกข้อ

   </details>

3. ทำไมต้องมีการทดสอบด้านลบในรายงาน *(เป้าหมายข้อ 2)*
   - ก) เพื่อให้รายงานยาวขึ้น
   - ข) เพราะมาตรการที่ไม่เคยถูกทดสอบให้ล้ม อาจผ่านทุกครั้งไม่ว่ามันจะทำงานหรือไม่
   - ค) เพราะแพลตฟอร์มบังคับ
   - ง) เพราะการทดสอบด้านบวกผิดเสมอ

   <details><summary>เฉลย</summary>

   **ข** นี่คือหลักเดียวกับ "มาตรการที่ตรวจได้" ในบทเรียน 1.1 การทดสอบต้องทำให้ผลเป็นแดงได้

   </details>

## แล็บ

**ส่งอุปกรณ์หนึ่งชิ้นพร้อมรายงานหลักฐาน** ใช้เวลาราว 55 นาที กรอก [resources/evidence-checklist.md](resources/evidence-checklist.md) ไปพร้อมกัน

- [ ] **1. สถานะเริ่มต้น** (mtb-mpy) อ่าน metadata ของ `0xE0E1` จดค่า tag `C0` และ `D0` ถ้า `C0` ไม่ใช่ `01` หยุดและแจ้งผู้สอน บน mtb-only ให้บันทึกว่าข้ามขั้นนี้และเหตุผล
- [ ] **2. ลงทะเบียน** (ผู้สอนอนุญาตแล้ว) HSM Security → Enrol Certificate ในโหมดที่เชื่อมต่อได้อยู่ เก็บประโยคบนจอและบรรทัด UART ตามแล็บเสริมของบทเรียน 5.1 ผลตัดสินต้องเป็น "The device can prove it holds the key this certificate names"
- [ ] **3. เปลี่ยนเป็น mTLS** ตั้ง `tls_mode=mtls` แล้วเชื่อมต่อใหม่ เก็บ log ตั้งแต่ `[MQTT] Waiting for WiFi...` จนถึง `[MQTT] Connected to broker` แล้วตัดสินด้วยเกณฑ์สามข้อของบทเรียน 3.1
- [ ] **4. ส่งข้อมูลและพิสูจน์ว่าถึง** publish telemetry แล้วเก็บหลักฐานฝั่งผู้รับตามแล็บ 3.2 ข้อ 4 ระบุให้ชัดว่าหลักฐานมาจากไหน
- [ ] **5. การทดสอบด้านลบอย่างน้อยสองข้อ** เช่น พอร์ต 8883 ปฏิเสธ client ที่ไม่มีใบ (แล็บ 3.1 ข้อ 3) การตรวจเซิร์ฟเวอร์ล้มเมื่อไม่มี anchor (แล็บ 3.1 ข้อ 4) หรือ `SECURE_BOOT=yes` ถูกระบบ build ปฏิเสธ (แล็บ 4.1 ข้อ 2)
- [ ] **6. Protected Update (ถ้าผู้สอนอนุญาต)** ทำตามแล็บเสริมของบทเรียน 4.2 เก็บ metadata ก่อนและหลัง และผลของการเชื่อมต่อใหม่ที่ต้องเห็นบรรทัด `Ignoring a Protected Update bundle nobody asked for` ถ้ามี bundle ถูกส่งมา
- [ ] **7. สถานะสุดท้าย** อ่าน metadata ของ `0xE0E1` อีกครั้ง `C0` ต้องเท่ากับข้อ 1
- [ ] **8. อัปเดต threat model** ของบทเรียน 1.1 ทุกแถว STRIDE ต้องมีสถานะ (ยังไม่ทำ / ทำแล้ว / ทดสอบผ่าน) ตาราง ETSI ต้องมีหลักฐานหรือเหตุผล และช่องความเสี่ยงที่เหลือต้องมีอย่างน้อยสามข้อจากตารางในหัวข้อแนวคิด พร้อมแผนหนึ่งบรรทัดต่อข้อ
- [ ] **9. ตรวจการรั่ว** ค้นรายงานและไฟล์แนบทั้งหมดว่าไม่มีรหัสผ่าน ไม่มีไฟล์จาก bundle และไม่มีกุญแจลับ ก่อนส่ง

**เกณฑ์ผ่าน** ทุกข้ออ้างในรายงานมีหลักฐานอย่างน้อยหนึ่งชนิดจากสี่ชนิด ข้อ 3 และ 4 มีหลักฐานครบ มีการทดสอบด้านลบอย่างน้อยสองข้อ และ threat model มีความเสี่ยงที่เหลือพร้อมแผน

## ไปต่อ

คุณผ่านหลักสูตร Secure IoT กับ OPTIGA™ Trust M แล้ว ทางที่ไปต่อได้

- ปิดช่องว่างของแม่แบบในงานของคุณเอง เช่นเติมการตรวจใน OTA client (บทเรียน 4.2) หรือออกแบบให้ CM33_S ตรวจ image ถัดไป (บทเรียน 4.1)
- อ่าน [AN237849 Getting started with PSOC™ Edge security](https://www.infineon.com/AN237849) ก่อนวางแผน provision secure boot ให้ผลิตภัณฑ์จริง
- ทบทวนเส้นทางเชื่อมต่อทั้งโมดูลใน [TESAIoT Firmware Stack โมดูล 5](../../../tesaiot-firmware-stack/m05-connect-to-platform/README.md) และลองตัวอย่างบน [TESAIoT Developer Hub](https://dev.tesaiot.dev/)

กลับไปที่ [หน้าหลักสูตร](../../README.md)

## สะท้อนคิด

- ข้ออ้างไหนในรายงานของคุณที่หาหลักฐานยากที่สุด และเพราะอะไร
- ความเสี่ยงที่เหลือข้อไหนที่คุณจะรับไว้ได้ในผลิตภัณฑ์จริง และข้อไหนรับไม่ได้
- ถ้าต้องอธิบายงานนี้ให้ผู้บริหารที่ไม่ใช่วิศวกรฟังในสองนาที คุณจะพูดว่าอะไร

## แหล่งอ้างอิง

- [ETSI EN 303 645 V3.1.3 (2024-09) Cyber Security for Consumer Internet of Things: Baseline Requirements](https://www.etsi.org/deliver/etsi_en/303600_303699/303645/03.01.03_60/en_303645v030103p.pdf)
- [D2 — Enrolment and Protected Update end to end (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d2__enrolment__protected__update.html)
- [C4 — mTLS: the OPTIGA-backed TLS identity (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c4__mtls__optiga.html)
- [C3 — TESAIoT cloud: config file → MQTT task → broker (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c3__cloud__mqtt.html)
- ตัวอย่างบน Developer Hub: [device-mtls](https://dev.tesaiot.dev/?example=developer-hub--device-mtls&q=device-mtls) · [c_ota_client](https://dev.tesaiot.dev/?example=developer-hub--c_ota_client&q=c_ota_client) · [pse84_tesaiot_client](https://dev.tesaiot.dev/?example=developer-hub--pse84_tesaiot_client&q=pse84_tesaiot_client) (Cypress EULA ลิงก์เท่านั้น)
