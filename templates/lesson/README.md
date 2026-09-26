---
id: "<short>.m01.l01"                 # <short>.mNN.lNN — ถาวร ห้ามเปลี่ยนหลัง merge
lang: th
title:
  th: "<ชื่อบทเรียน>"
  en: "<Lesson title>"
summary:                              # หนึ่งประโยค
  th: "<บทเรียนนี้พาผู้เรียนไปทำอะไรได้>"
  en: "<What this lesson lets the learner do>"
level: L2                             # L1..L5 ดู tqp/levels.md
time_min: {concept: 10, practise: 20, lab: 20, check: 5}   # จำนวนเต็ม รวม 20–75 นาที
hardware: {emulator: true, boards: [eva-kit, devkit]}      # boards: eva-kit | devkit | none
prerequisites: []                     # lesson id ของบทก่อนหน้า เช่น ["<short>.m01.l00"]
objectives:                           # 2–4 ข้อ กริยาที่วัดผลได้ + เงื่อนไข (+ เกณฑ์) ทุกข้อต้องมีข้อเช็กใน quiz.yaml
  - th: "<เขียนโปรแกรมนับถอยหลังจาก N ถึง 1 ใน BENTO Emulator ได้ถูกต้อง>"
    en: "<Write a program that counts down from N to 1 in the BENTO Emulator>"
  - th: "<อธิบายได้ว่าทำไม range(3, 0, -1) หยุดที่ 1 โดยอ้างค่า stop>"
    en: "<Explain why range(3, 0, -1) stops at 1, referring to the stop value>"
develops:                             # อย่างน้อย 1 รายการ skill id ต้องมีใน skills/skills.yaml
  - {skill: lang.micropython, to: 2}
assesses:                             # ใส่หรือไม่ก็ได้ evidence ชี้ไฟล์ในบทเรียนนี้
  - {skill: lang.micropython, level: 2, evidence: practice/01_countdown.py}
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: pre-alpha                     # pre-alpha | alpha | beta | stable ดู GOVERNANCE.md
translation: pending                  # done เมื่อ README.en.md ตรงกับฉบับไทยล่าสุด
slides: slides.md                     # ลบบรรทัดนี้ถ้าบทเรียนไม่มีสไลด์
# source: {repo: https://github.com/<owner>/<repo>, path: <path>, ref: <commit>}   # ถ้านำเนื้อหามาจากที่อื่น
---

<!--
แม่แบบบทเรียน (ภาษาไทย) คัดลอกทั้งโฟลเดอร์ templates/lesson/ ไปที่ courses/«course-id»/mNN-«slug»/lNN-«slug»/
แทน «...» และค่าใน front matter ทุกจุด ลบหัวข้อที่ไม่เกี่ยวข้องได้ แต่ห้ามสลับลำดับ
ดูคู่มือเต็มที่ templates/AUTHORING.md
-->

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. «เป้าหมายข้อ 1 ตรงกับ objectives ข้อ 1 ใน front matter»
2. «เป้าหมายข้อ 2»

ใช้เวลาประมาณ 55 นาที «รวม time_min»

## ก่อนเริ่ม

ทวนของเดิมสองข้อ ลองตอบในใจก่อนอ่านต่อ

1. «คำถามทวนจากบทก่อนหน้า ข้อ 1»
2. «คำถามทวนจากบทก่อนหน้า ข้อ 2»

## ดูของจริงก่อน

เปิด [examples/01_countdown.py](examples/01_countdown.py) ใน BENTO IDE (https://ide.tesaiot.dev/) **ทายก่อนรัน** ว่าจอจะแสดงอะไร แล้วค่อยกดรัน
«ให้ผู้เรียนเห็นผลที่ทำงานได้จริงภายใน 15 นาทีแรก»

## แนวคิด

«ไม่เกินสามช่วง ช่วงละไม่เกิน 6 นาทีหรือหนึ่งหน้าจอ เขียนภาษาไทยคู่ศัพท์อังกฤษ เช่น อินเทอร์รัปต์ (interrupt) ครั้งแรกที่ใช้คำ»

## ตัวอย่างสมบูรณ์

[examples/01_countdown.py](examples/01_countdown.py) ทำงานเป็นสามท่า

- **ท่าที่ 1** กำหนดค่าที่เราจะลองเปลี่ยน
- **ท่าที่ 2** วนนับถอยหลังทีละหนึ่ง
- **ท่าที่ 3** พักระหว่างรอบ แล้วบอกว่าจบ

ลองแก้ `COUNT_FROM` เป็น 5 ทายก่อนว่าจะเห็นอะไร แล้วรันดู

## ฝึกเติม

เปิด [practice/01_countdown.py](practice/01_countdown.py) แล้วเติมส่วนที่เว้นไว้ให้โปรแกรมทำงานเหมือนตัวอย่าง
«ถ้ามีโจทย์เรียงโค้ด (Parsons) ให้ใส่ไว้ใน quiz.yaml ชนิด order»

## เฉลย

ลองเองก่อนอย่างน้อย 15 นาที แล้วค่อยเปิด [solution/01_countdown.py](solution/01_countdown.py) คอมเมนต์ในเฉลยอธิบายว่าทำไมแต่ละบรรทัดเป็นแบบนั้น

## เช็กความเข้าใจ

ตอบคำถามใน [quiz.yaml](quiz.yaml) ตอบถูกตั้งแต่ 80% ขึ้นไปถือว่าจบบทเรียนนี้

## แล็บ

«งานลงมือบนบอร์ดหรือ emulator ลำดับ Modify → Make บอกให้ชัดว่าต้องเก็บหลักฐานอะไร (รูป log วิดีโอ) ไว้ใน portfolio
ถ้าแล็บยาว ให้แยกเป็นไฟล์ lab.md ในโฟลเดอร์นี้แล้วลิงก์มาจากตรงนี้»

## ไปต่อ

«โจทย์ท้าทาย datasheet หรือ application note ที่ควรอ่าน หรือกรณีใช้งานจริงในอุตสาหกรรม»

## สะท้อนคิด

- อะไรในบทนี้ที่ทำให้คุณแปลกใจ
- ถ้าเอาไปใช้ในผลิตภัณฑ์จริง โค้ดนี้จะพังได้ตรงไหน
