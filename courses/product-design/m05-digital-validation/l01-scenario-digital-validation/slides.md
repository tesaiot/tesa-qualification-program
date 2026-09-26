---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 5.1 — Digital validation ก่อนสร้างต้นแบบ"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT) · CC BY-NC 4.0"
---
<style>
section { font-size: 24px; padding: 40px 52px; justify-content: flex-start; }
section h1 { font-size: 1.45em; line-height: 1.12; margin: 0 0 .22em; }
section h2 { font-size: 1.12em; margin: .15em 0; }
section h3 { font-size: 1.0em; margin: .12em 0; }
section p, section li { margin: .16em 0; line-height: 1.32; }
section img { max-width: 100%; height: auto; }
section svg { max-height: 250px; }
section table { font-size: .78em; }
section pre { font-size: .70em; line-height: 1.32; background:#0d1117; color:#e6edf3; border:1px solid #30363d; border-radius:8px; padding:12px 16px; box-shadow:0 2px 8px rgba(0,0,0,.25); }
section pre code { white-space: pre-wrap; background:transparent; color:inherit; } section pre .hljs-comment{color:#8b949e;font-style:italic} section pre .hljs-keyword,section pre .hljs-built_in,section pre .hljs-literal{color:#ff7b72} section pre .hljs-string{color:#a5d6ff} section pre .hljs-number{color:#79c0ff} section pre .hljs-title,section pre .hljs-title.function_,section pre .hljs-section{color:#d2a8ff} section pre .hljs-meta{color:#ffa657} section pre .hljs-attr,section pre .hljs-attribute,section pre .hljs-name{color:#7ee787}
section blockquote { margin: .25em 0; font-size: .92em; }
/* two images on a line (parity / 2x2 grids) stay side-by-side and small */
section p > img + img { margin-left: 10px; }
/* scroll-within-slide: dense slides scroll instead of clipping */
section { overflow-y: auto; overflow-x: hidden; }
section::-webkit-scrollbar { width: 11px; }
section::-webkit-scrollbar-thumb { background:#4a90d9; border-radius:6px; }
section::-webkit-scrollbar-track { background:rgba(0,0,0,.06); }
/* image drop-shadow + cover-slide readability (auto) */
section img{filter:drop-shadow(0 3px 12px rgba(0,0,0,.5))}
section.cover *{color:#fff !important}
section.cover h1,section.cover h2,section.cover h3,section.cover p,section.cover li,section.cover strong,section.cover em,section.cover blockquote,section.cover div{text-shadow:0 2px 9px rgba(0,0,0,.92),0 0 3px rgba(0,0,0,.8)}
section.cover div[style*="background:#"],section.cover div[style*="background: #"]{background:rgba(10,14,20,.66) !important;border-color:rgba(120,200,255,.45) !important;max-width:62%}
section.cover blockquote{border-left:4px solid rgba(120,200,255,.6) !important;background:rgba(13,17,23,.55) !important;border-radius:6px;padding:.3em .6em}
section.cover h1,section.cover h2,section.cover h3,section.cover p,section.cover blockquote{max-width:60%}
section.cover div:not(:has(img)){max-width:62%}
section.cover img{filter:none}
</style>

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

# บทเรียน 5.1 — Digital validation ก่อนสร้างต้นแบบ

## ออกแบบสถานการณ์ทดสอบก่อนคลิก สังเกตและปรับดีไซน์ ผูกโมเดลกับข้อมูลเฟิร์มแวร์/Edge AI ด้วยหลักฐาน และสรุป checklist ก่อนพิมพ์

**โมดูล 5 — สถานการณ์ใช้งานและการตรวจสอบเชิงดิจิทัล**

หลักสูตร **การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)** · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT)

---

## เป้าหมาย

เมื่อเรียนจบบทเรียนนี้ คุณควรทำได้:

1. ตั้ง **usage scenario** (จับ วาง เปิดฝา ฯลฯ) ตามที่ Twin รองรับ
2. ประเมินการตอบสนองของผลิตภัณฑ์และนำผลไปปรับปรุงการออกแบบ
3. จับคู่โมเดลกับข้อมูล **Edge AI / เฟิร์มแวร์** (สถานะ → สี / คลิป)
4. ทำ **Digital Validation** และรายการปรับปรุงก่อนสร้างต้นแบบ

> **คาถาประจำบทเรียน**
> Digital validation = *หาบั๊กดีไซน์บนจอก่อนเสียพลาสติก* — ถ้าพบปัญหาในบทเรียนนี้แล้วยังไม่จด แสดงว่ายังไม่พร้อมพิมพ์ในโมดูลถัดไป

---

## Digital validation หมายถึงอะไรในหลักสูตรนี้

คือการพิสูจน์บน Twin ว่ากล่องหุ้ม + คลิป + จุดเซ็นเซอร์ **ใช้ร่วมกับข้อมูลจริง/จำลองได้** ก่อนสั่งพิมพ์ในโมดูล 6

**ไม่ใช่** การแทนการทดสอบมาตรฐานอุตสาหกรรมทั้งหมด หรือแทนการจำลองแรงกระแทกแบบ FEA เต็มรูป

```text
[Usage scenarios on Twin] → [Observe problems: thin walls · blocked sensors · lid clash · bad port]
    → [Bind firmware / Edge AI signals: color / clip / highlight]
        → [Pre-prototype checklist: Top 3 fixes before print]
```

---

## ออกแบบสถานการณ์ทดสอบก่อนคลิก

ก่อนเล่นคลิป ให้เขียนสถานการณ์เป็นประโยคสั้น ๆ: **ใคร ทำอะไร คาดหวังเห็นอะไร**

| สถานการณ์ | การกระทำ | สัญญาณผ่าน |
|---|---|---|
| **S1 วางโต๊ะ** | วางเครื่องบนโต๊ะในแนวใช้งานปกติ | ไม่ล้มในมุมมอง / อ่านพอร์ตได้ |
| **S2 ถือในมือ** | จำลองมุมกล้องใกล้มือ | ไม่มีขอบคมบังปุ่มสำคัญ |
| **S3 เปิดฝาบริการ** | เปิดฝาซ้ำ 3 รอบด้วยคลิป | ไม่ทะลุ · เปิดแล้วเห็นช่องบริการ |
| **S4 เข้าถึงเซ็นเซอร์** | กระตุ้นเซ็นเซอร์ (เอียงบอร์ด) | ช่องไม่ถูกบัง · มีสตรีม |
| **S5 เสียบพอร์ต** | จำลองเสียบสาย | ช่องใหญ่พอและหันทิศถูก |

ในแล็บบังคับอย่างน้อย **S3** และอีกหนึ่งข้อ ทำตาม action → จดสิ่งที่คาดกับสิ่งที่เห็น → ถ้าพังให้จดเป็นรายการแก้ ไม่แก้เงียบ ๆ

---

## สังเกตและปรับปรุงดีไซน์

| ความเสี่ยง | หน้าตาที่เห็น | วิธีแก้ทั่วไปก่อนพิมพ์ |
|---|---|---|
| ผนังบางเกินไป | ขอบดูคม/บางใน Twin หรือ Thickness < ~2 mm | เพิ่มความหนา · เติม rib |
| ช่องเซ็นเซอร์ถูกบัง | ช่องไม่อยู่เหนือชิป · มีชิ้นส่วนบัง | เลื่อนช่อง · ตัด opener ใหม่ |
| พอร์ตเสียบยาก | ช่องเล็ก/เอียงผิด | ขยายช่อง · เผื่อ clearance |
| ฝาชนชิ้นสูง | คลิปเปิดแล้วทะลุ USB/จอ | ลดมุมเปิด · เลื่อนบานพับ |
| สเกลเพี้ยน | เทียบบอร์ดจริงแล้วไม่คล้าย | กลับโมดูล 1/4 แก้แล้ว export ใหม่ |

ต้องจดปัญหาอย่างน้อย **3 ข้อ** ในแล็บ — แม้บางข้อจะเป็น "ผ่าน แต่ควรระวัง" ถ้าเวลาพอ กลับ Blender แก้อย่างน้อย 1 จุด แล้ว export GLB รอบใหม่

---

## ผูกโมเดลกับข้อมูล Edge AI / เฟิร์มแวร์

เป้าหมาย: Twin เป็นภาษาเดียวกันของทีมออกแบบกับทีมเฟิร์มแวร์

| สัญญาณเฟิร์มแวร์/Twin | การตอบสนองบนโมเดล |
|---|---|
| อุณหภูมิสูง / threshold event | เน้นบริเวณช่องเซ็นเซอร์ หรือเปลี่ยนสีตัวเครื่อง |
| BMI270 orientation | หมุน preview ตามท่า (ถ้า host รองรับ) |
| Mode / LED บนอุปกรณ์ | Emission หรือสีที่ `led_status_window` |
| คำสั่งเปิดฝาจาก UI | เล่นคลิป `lid_open` |

**กติกาหลักฐาน** อ้างว่า "โมเดลตอบตามเซ็นเซอร์" ต้องมีสกรีนช็อต/คลิปที่เห็นทั้งโมเดลและการเปลี่ยนค่า ถ้ายังผูกไม่ได้ในรอบนี้ ให้เขียนเหตุผลสั้น ๆ + สิ่งที่จะทำในโมดูล 6 — อย่าปล่อยช่องว่างโดยไม่เขียนเหตุผล

---

## Checklist ก่อนสร้างต้นแบบ

กรอกฉบับเต็มใน [pre-prototype-checklist.md](resources/pre-prototype-checklist.md) — คอลัมน์ตรวจขั้นต่ำ

| หัวข้อ | คำถามหลัก |
|---|---|
| Scale | ขนาดยังตรงบอร์ด/สูตรโมดูล 1 หรือไม่ |
| Internal fit | PCB + แบตเตอรี่ + สาย อยู่ร่วมกันได้หรือไม่ |
| Sensor openings | ช่องตรงตำแหน่งเซ็นเซอร์จริงหรือไม่ |
| Walls | หนาพอสำหรับพิมพ์ (~2 mm เป็นจุดเริ่ม) |
| Motion | ฝา/ปุ่มชนชิ้นอื่นหรือไม่ |
| Data link | มีการจับคู่สถานะอย่างน้อยหนึ่งอย่าง หรือมีเหตุผลที่ยังไม่ทำ |

ท้าย checklist ต้องมี **3 รายการแก้เรียงความสำคัญ** ก่อนพิมพ์ — ถ้าทุกอย่างผ่าน เขียนว่า "Ready to print" พร้อมสิ่งที่ยังต้องเฝ้าระวังตอนประกอบจริง

---

## เช็กความเข้าใจ / ไปต่อ

ตอบคำถามใน [quiz.yaml](quiz.yaml) — สามข้อ ผูกกับเป้าหมายของบทเรียนนี้ข้อละหนึ่งคำถาม ลองตอบเองก่อนแล้วค่อยเทียบกับเฉลยในไฟล์

---

## ฝึกเติม/แล็บ

ลงมือต่อที่ [แล็บ: สถานการณ์ใช้งานและ checklist ก่อนทำต้นแบบ](../l02-lab/README.md) (~2.5–3 ชั่วโมง)

- รัน usage scenario อย่างน้อย 2 รายการบน Twin (ต้องมี S3) แล้วจดปัญหาอย่างน้อย 3 ข้อ
- กรอก [pre-prototype-checklist.md](resources/pre-prototype-checklist.md) พร้อม Top 3 fixes

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"การออกแบบผลิตภัณฑ์เชิงอุตสาหกรรม (Blender และ Digital Twin)" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0 (ดัดแปลง)

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)

เครื่องมือ Bitstream Studio (VS Code) และ Ternion ที่หลักสูตรนี้ใช้ เป็นผลงานของ ผศ.ดร.สันติ นุราช (KMUTT)
