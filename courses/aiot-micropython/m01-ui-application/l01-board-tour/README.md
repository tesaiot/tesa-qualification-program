---
id: aiot-mpy.m01.l01
lang: th
title: {th: 'ทัวร์บอร์ด: เล่นของจริงก่อน', en: 'Board tour: play with the real thing first'}
summary: {th: เล่นเมนูที่มากับบอร์ดให้ครบก่อนเขียนโค้ดบรรทัดแรก แล้วจับคู่ให้ได้ว่าแต่ละเมนูอ่านเซนเซอร์ตัวไหน และหน้าไหนคือที่ที่โค้ดของเราจะไปปรากฏ, en: 'Play with the menus that ship on the board before writing any code, match each menu to the sensors it reads, and find the page where your own code will appear.'}
level: L2
time_min: {concept: 15, lab: 30, check: 5}
hardware: {emulator: true, boards: [eva-kit, devkit]}
prerequisites: []
objectives:
  - {th: 'ระบุเซนเซอร์ที่เมนู Home (แผง Sensor Live), Sensor Dashboard และ Smart Watch ใช้ ได้ถูกต้องอย่างน้อยสามเมนู จากการเอียง หมุน แตะ และหมุนลูกบิดบนบอร์ดจริงหรือ Emulator', en: 'Identify the sensors behind the Home (Sensor Live panel), Sensor Dashboard and Smart Watch menus for at least three menus, by tilting, turning, touching and turning the knob on the board or the Emulator.'}
  - {th: 'บอกได้ว่าเมนู Controls, Audio Player และ TESAIoT Connectivity มีเฉพาะบน Eva Kit และเลือกทางแทนบน Dev Kit ได้', en: 'State that Controls, Audio Player and TESAIoT Connectivity exist only on the Eva Kit, and choose the Dev Kit alternative.'}
  - {th: อธิบายว่าทำไมต้องเปิดหน้า BENTO Playground ค้างไว้ก่อนส่งโค้ดจาก BENTO IDE, en: Explain why the BENTO Playground page must be open before you send code from BENTO IDE.}
develops: [{skill: sys.sensors-actuators, to: 1}, {skill: iot.fundamentals, to: 1}, {skill: gui.embedded, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {repo: 'https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer', path: session-01.html (slides 1–7), ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079}
---

# บทเรียน 1.1 — ทัวร์บอร์ด: เล่นของจริงก่อน

> โมดูล 1 — แอปพลิเคชันบนจอที่มีอยู่แล้ว · สไลด์: [slides.md](slides.md) · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

เล่นเมนูที่มากับบอร์ดให้ครบก่อนเขียนโค้ดบรรทัดแรก แล้วจับคู่ให้ได้ว่าแต่ละเมนูอ่านเซนเซอร์ตัวไหน และหน้าไหนคือที่ที่โค้ดของเราจะไปปรากฏ

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. ระบุเซนเซอร์ที่เมนู Home (แผง Sensor Live), Sensor Dashboard และ Smart Watch ใช้ ได้ถูกต้องอย่างน้อยสามเมนู จากการเอียง หมุน แตะ และหมุนลูกบิดบนบอร์ดจริงหรือ Emulator
2. บอกได้ว่าเมนู Controls, Audio Player และ TESAIoT Connectivity มีเฉพาะบน Eva Kit และเลือกทางแทนบน Dev Kit ได้
3. อธิบายว่าทำไมต้องเปิดหน้า BENTO Playground ค้างไว้ก่อนส่งโค้ดจาก BENTO IDE

## ก่อนเริ่ม

ไม่ต้องเขียนโค้ดในบทเรียนนี้ เตรียมสมุดหรือไฟล์ไว้เป็น **บันทึกการเรียน** ของตัวเอง
(สไลด์จะบอกเป็นระยะว่าควรจดอะไร) ถ้าไม่มีบอร์ด เปิด BENTO Emulator ใน BENTO IDE แล้วเล่นตามได้เกือบทุกข้อ

- **อุปกรณ์:** บอร์ด Eva Kit หรือ TESAIoT Dev Kit ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว หรือ BENTO Emulator ใน [BENTO IDE](https://ide.tesaiot.dev/)

## ดูของจริงก่อน

เปิดบอร์ดแล้วอยู่ที่หน้า Home ก่อน อย่าเพิ่งกดเข้าเมนูไหน เอียงบอร์ด หมุนบอร์ด แตะแผ่นสัมผัส
และหมุนลูกบิด แล้วดูแผง Sensor Live มุมขวาบนของจอ ค่าพวกนี้วิ่งอยู่แล้วทั้งที่ยังไม่มีโค้ดของเราสักบรรทัด
เพราะเฟิร์มแวร์อ่านเซนเซอร์ให้ตลอดเวลา

## แนวคิด

บอร์ดในหลักสูตรนี้มีของครบทุกชิ้นที่ระบบ AIoT จริงต้องมี: เซนเซอร์วัดการเคลื่อนไหว (IMU) เข็มทิศ
ปุ่มสัมผัส (CapSense) ลูกบิด จอสัมผัส ไมโครโฟน และวิทยุ WiFi เมนูที่มากับเครื่องคือ "ปลายทาง"
ที่เราจะค่อย ๆ สร้างเองตลอดหลักสูตร การเล่นก่อนจึงไม่ใช่การเสียเวลา มันคือการเห็นเป้าก่อนออกเดิน

ทัวร์แบ่งเป็นสามรอบ รอบแรกคือหน้า Home กับแผง Sensor Live รอบที่สองคือสามเมนูที่ต้องเล่นให้ครบ
(Controls, Sensor Dashboard, Smart Watch) รอบที่สามคือเมนูที่ต้องรู้ว่ามีอยู่ (Audio Player,
Wi-Fi Setting, BENTO Playground, TESAIoT Connectivity) ระหว่างเล่นให้ถามตัวเองทุกครั้งว่า
ค่าบนจอมาจากเซนเซอร์ตัวไหน

สองบอร์ดใช้โค้ดชุดเดียวกัน แต่หน้า Home ไม่เหมือนกัน: Dev Kit ไม่มีการ์ด Controls, Audio Player
และ TESAIoT Connectivity ทีมที่ถือ Dev Kit จะเห็นไฟจริงติดจากโค้ดของตัวเองในบทเรียน 1.3 แทน

หน้าที่สำคัญที่สุดสำหรับเราคือ **BENTO Playground** ผลของโค้ดที่ส่งจาก BENTO IDE จะไปโผล่ที่หน้านี้
ถ้าไม่ได้เปิดค้างไว้ก่อนส่งโค้ด จะดูเหมือนว่าส่งแล้วไม่มีอะไรเกิดขึ้น

## ตัวอย่างสมบูรณ์

สไลด์ของบทเรียนนี้อ้างถึงไฟล์ที่อยู่ในบทเรียนอื่นด้วย:

- [m01-ui-application/l03-inside-the-box/examples/11_lights_and_a_button.py](../l03-inside-the-box/examples/11_lights_and_a_button.py) — หลอดไฟกับปุ่มจริง สั่งได้จาก Python บรรทัดเดียว
- [m01-ui-application/l03-inside-the-box/examples/15_one_number_many_faces.py](../l03-inside-the-box/examples/15_one_number_many_faces.py) — ตัวเลขตัวเดียว กับสิบวิธีที่จอเล่ามันออกมา

## เช็กความเข้าใจ

คำถามชุดเดียวกันอยู่ใน [quiz.yaml](quiz.yaml) สำหรับระบบที่ตรวจอัตโนมัติ

1. บนหน้า Home คุณหมุนบอร์ดรอบตัวเองโดยไม่เอียง แถวไหนของแผง Sensor Live ที่ค่าควรเปลี่ยนชัดที่สุด *(เลือกหนึ่งข้อ · เป้าหมายข้อ 1)*
   - ก) Comp (เข็มทิศ)
   - ข) Touch
   - ค) Pot
   - ง) ไม่มีแถวไหนเปลี่ยน เพราะยังไม่ได้เขียนโค้ด

   <details><summary>เฉลย</summary>

   **ก** — การหมุนรอบตัวเองเปลี่ยนทิศที่บอร์ดหัน เข็มทิศ (Comp) จึงเปลี่ยน ส่วนค่าพวกนี้วิ่งอยู่แล้วโดยไม่ต้องมีโค้ดของเรา เพราะเฟิร์มแวร์อ่านเซนเซอร์ให้ตลอดเวลา

   </details>

2. เมนูใดใช้ข้อมูลจากเซนเซอร์วัดการเคลื่อนไหว (IMU) เลือกทุกข้อที่ถูก *(เลือกได้หลายข้อ · เป้าหมายข้อ 1)*
   - ก) Sensor Dashboard (กราฟที่กระเพื่อมเมื่อเขย่าบอร์ด)
   - ข) Smart Watch (ตัวนับก้าว)
   - ค) แผง Sensor Live แถว IMU บนหน้า Home
   - ง) Wi-Fi Setting

   <details><summary>เฉลย</summary>

   **ก, ข, ค** — กราฟของ Sensor Dashboard, ตัวนับก้าวของ Smart Watch และแถว IMU ของ Sensor Live มาจากเซนเซอร์ความเร่งตัวเดียวกัน ส่วน Wi-Fi Setting ใช้วิทยุ ไม่ใช่เซนเซอร์

   </details>

3. ทีมของคุณถือ TESAIoT Dev Kit และหาการ์ด Controls บนหน้า Home ไม่เจอ ข้อใดถูกต้อง *(เลือกหนึ่งข้อ · เป้าหมายข้อ 2)*
   - ก) บอร์ดเสีย ต้องลงเฟิร์มแวร์ใหม่
   - ข) Dev Kit ไม่มีการ์ดนี้ ให้ดูไฟจริงติดจากโค้ดตัวอย่างในบทเรียน 1.3 แทน
   - ค) ต้องต่อ WiFi ก่อน การ์ดจึงจะขึ้น
   - ง) ต้องเสียบ SD card ก่อน

   <details><summary>เฉลย</summary>

   **ข** — Controls, Audio Player และ TESAIoT Connectivity มีเฉพาะบน Eva Kit สองบอร์ดใช้โค้ดชุดเดียวกัน ทีม Dev Kit จึงเห็นไฟจริงติดจากโค้ดของตัวเองแทน

   </details>

4. คุณกด Program to Device ใน BENTO IDE แล้วจอบอร์ดไม่แสดงอะไรเลย สิ่งแรกที่ควรตรวจคืออะไร *(เลือกหนึ่งข้อ · เป้าหมายข้อ 3)*
   - ก) เปิดหน้า BENTO Playground ค้างไว้บนบอร์ดแล้วหรือยัง
   - ข) เปลี่ยนไปใช้ภาษา C
   - ค) รีเซ็ตบอร์ดกลับค่าโรงงาน
   - ง) ต่อ WiFi ให้บอร์ด

   <details><summary>เฉลย</summary>

   **ก** — ผลของโค้ดที่ส่งจาก IDE ไปโผล่ที่หน้า BENTO Playground ถ้าบอร์ดค้างอยู่หน้าอื่น จะดูเหมือนส่งแล้วไม่มีอะไรเกิดขึ้น

   </details>

## แล็บ

**ทัวร์สามรอบ** (ราว 30 นาที) ทำบนบอร์ดจริงหรือ Emulator แล้วจดลงบันทึกการเรียน

- [ ] รอบที่ 1: หน้า Home เอียง หมุน แตะ ลากนิ้วบนแถบเลื่อน และหมุนลูกบิด แล้วจดว่าแถวไหนของ Sensor Live เปลี่ยน
- [ ] รอบที่ 2: Controls (Eva Kit) แตะวงกลมแล้วดูหลอด LED จริง · Sensor Dashboard เขย่าแล้วดูกราฟ · Smart Watch ปัดเปลี่ยนหน้า
- [ ] รอบที่ 3: เข้า Audio Player, Wi-Fi Setting, BENTO Playground และ TESAIoT Connectivity (ถ้ามี) เพื่อรู้ว่าอยู่ตรงไหน
- [ ] ทำตารางสามคอลัมน์ในบันทึกการเรียน: เมนู · เซนเซอร์ที่ใช้ · สิ่งที่เห็นบนจอ ให้ครบอย่างน้อยห้าแถว

## ไปต่อ

บทเรียนถัดไป: [บทเรียน 1.2 — ข้อความแรกขึ้นจอ: โมดูล lcd กับ ui](../l02-first-lines-on-screen/README.md)

## สะท้อนคิด

- เมนูไหนที่คุณคิดว่าเอาไปใช้ในงานของตัวเองได้ทันที และจะต้องเพิ่มอะไรอีก
- แผงหน้าปัดรถยนต์รุ่นเก่ามีลูกบิดจริงทุกชิ้น พอย้ายทุกอย่างขึ้นจอเดียว อะไรหายไปบ้าง
