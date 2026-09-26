---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.1 — สถาปัตยกรรม MCU หลายโดเมนและชั้นของ Firmware SDK"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · ดัดแปลงจากงานของ ผศ.ดร.สันติ นุราช (KMUTT) · CC BY 4.0"
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

# บทเรียน 1.1 — สถาปัตยกรรม MCU หลายโดเมนและชั้นของ Firmware SDK

## อ่านแผนที่ PSOC™ Edge E84 แบบหลายโดเมน และชั้นซอฟต์แวร์ HAL/BSP · Driver API · Utility · Application ก่อนเขียนโค้ดจริง

**หลักสูตร TESA Firmware SDK สำหรับ Edge AI — โมดูล 1 · บทเรียน 1**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. จับคู่งานผลิตภัณฑ์ 4 แบบ (UI, always-on sensing, inference หนัก, publish MQTT) กับโดเมน Cortex-M55 / Cortex-M33 + NNLite / Ethos-U55 ได้ถูกต้อง พร้อมเหตุผลข้อละหนึ่งประโยค
2. จำแนกทุกขั้นตอนของโจทย์ตัวอย่างว่าอยู่ชั้น HAL/BSP, Driver API, Utility หรือ Application
3. อธิบายความต่างระหว่าง SDK กับ IDE (ModusToolbox™ / VS Code) โดยยกตัวอย่างสิ่งที่อยู่ในแต่ละฝั่งได้อย่างน้อยฝั่งละหนึ่งอย่าง

---

## ก่อนเริ่ม

- บทเรียนแรกของหลักสูตร — **ไม่มีบทเรียนก่อนหน้าที่ต้องผ่าน**
- **ไม่ต้องใช้บอร์ด** — โมดูล 1 เป็นบทเรียนเชิงแนวคิดล้วน ยังไม่ flash เฟิร์มแวร์ (การ flash Hello World อยู่ใน โมดูล 2)
- สิ่งที่ควรมีติดตัว: เขียนภาษา C ระดับพื้นฐานได้ (ฟังก์ชัน pointer struct callback) และใช้คอมพิวเตอร์/เทอร์มินัลเบื้องต้นได้
- เปิดแผ่นสรุปไว้ข้าง ๆ: [sdk-layer-cheatsheet.md](resources/sdk-layer-cheatsheet.md)

---

## ดูของจริงก่อน — ทำไม MCU ยุคนี้ถึงไม่เหมือนเดิม

MCU แบบดั้งเดิมอ่านสวิตช์/เซ็นเซอร์ ขับ LED/มอเตอร์ คุย UART/I²C/SPI บนคอร์เดียวได้ดีอยู่แล้ว — แต่ผลิตภัณฑ์อัจฉริยะสมัยใหม่ต้องการมากกว่านั้น

| ความต้องการ | ตัวอย่างในผลิตภัณฑ์ |
|---|---|
| ประมวลผลใกล้แหล่งข้อมูล | รู้ว่ามีคำสั่งเสียง/ท่าทาง โดยไม่ส่งเสียงดิบตลอดเวลา |
| ตอบสนองเร็ว (latency ต่ำ) | UI หรือ safety interlock ที่ต้องตอบในหน่วยมิลลิวินาที |
| ใช้พลังงานอย่างมีวินัย | รอฟังตลอดคืนบนแบตเตอรี่ |
| ความเป็นส่วนตัว | ข้อมูลดิบบางส่วนไม่ต้องออกนอกอุปกรณ์ |
| ทนเมื่อเน็ตหลุด | ฟังก์ชันหลักยังทำงานได้แม้คลาวด์ชั่วคราวใช้ไม่ได้ |

> แนวคิดนี้เรียกว่า **Edge AI** — นำ AI/ML ไปทำงานใกล้แหล่งข้อมูล ไม่ใช่ส่งข้อมูลดิบขึ้นคลาวด์ตลอดเวลา

---

## แนวคิด (1) — ทำไมคอร์เดียวมักไม่พอ

ถ้าบังคับงานทุกอย่างไว้บน CPU เดียว จะเจอข้อขัดแย้งบ่อย ๆ:

- ต้องการ inference หนัก → ต้อง clock สูง → กินพลังงานมาก
- ต้องการ always-on sensing → ต้องตื่นบ่อย → ชนกับงบพลังงาน
- ต้องการ UI/กราฟิก + เซ็นเซอร์ + เครือข่ายพร้อมกัน → แย่งเวลา CPU กัน

ดังนั้น MCU ยุค Edge AI จึงออกแบบเป็น **หลายโดเมน (multi-domain)** — แยกงานสมรรถนะสูงออกจากงานพลังงานต่ำ และแยกตัวเร่ง Neural Network ออกจากคอร์ทั่วไป

---

## แนวคิด (2) — PSOC™ Edge E84: สองโดเมนหลัก

| | High-Performance Domain | Low-Power Domain |
|---|---|---|
| คอร์ | Arm® Cortex®-M55 (สูงสุดราว 400 MHz, มี Helium™ DSP + FPU) | Arm® Cortex®-M33 (สูงสุดราว 200 MHz) |
| ตัวเร่ง ML | Arm® Ethos™-U55 NPU (สูงสุดราว 400 MHz, ราว 128 MAC/cycle) | Infineon NNLite |
| เหมาะกับ | ตรรกะผลิตภัณฑ์หลัก, DSP, inference สมรรถนะสูง, กราฟิก/connectivity โหมดแอ็กทีฟ | always-on sensing, wake-word, งานต่อเนื่องแบบประหยัดพลังงาน |

> **จำประโยคนี้ไว้**: อย่าท่องแค่ชื่อคอร์ — ให้ตอบได้ว่า *งานนี้ควรอยู่โดเมนไหน และทำไม*

---

## แนวคิด (3) — จับคู่งานกับโดเมน (design time)

| ประเภทงาน | โดเมนที่มักเหมาะสม | เหตุผลสั้น ๆ |
|---|---|---|
| UI / เมนู / ควบคุม LED จากสถานะแอป | High-Performance (M55) | เป็นตรรกะผลิตภัณฑ์หลัก |
| รอฟังเสียงเบา ๆ ทั้งคืน | Low-Power (M33 ± NNLite) | งบพลังงานสำคัญกว่า throughput |
| โมเดล gesture/vision ขั้นสูงบนอุปกรณ์ | Ethos-U55 (+ แอปบน M55 ประสาน) | ต้องการเร่ง ML |
| จัด JSON แล้ว publish MQTT | แอปบนคอร์หลัก (มัก M55) | เป็นโปรโตคอล/นโยบาย ไม่ใช่หน้าที่ NPU |
| กรองสัญญาณเบา ๆ ก่อนส่งเข้าโมเดล | M55 (DSP/Helium) หรือ utility บนแอป | preprocessing ไม่เท่ากับ inference |

---

## แนวคิด (4) — ความเข้าใจผิดที่พบบ่อย

| ความเข้าใจผิด | ความจริง |
|---|---|
| มี NPU แล้วไม่ต้องเขียนเฟิร์มแวร์ควบคุม I/O | NPU เร่ง inference — อ่านเซ็นเซอร์/สั่ง actuator ยังเป็นงานของแอป + driver |
| ทุกอย่างควรรันบน Cortex-M55 | งาน always-on ควรพิจารณาโดเมนพลังงานต่ำ |
| Edge AI = ส่งข้อมูลดิบขึ้นคลาวด์ตลอด | ตรงข้าม — มุ่งประมวลผลที่ขอบก่อน |
| NNLite กับ Ethos-U55 ใช้แทนกันได้ทุกงาน | คนละจุดประสงค์: always-on ประหยัดพลังงาน vs ML สมรรถนะสูง |
| ต้องเลือกโดเมนให้ถูกตั้งแต่บรรทัดแรกของ Hello World | บทเรียนนี้สอนแผนที่ — มอบหมาย task จริงจะชัดขึ้นใน โมดูล 4–5 |

---

## แนวคิด (5) — หน่วยความจำ SoC สำคัญกับ Edge AI อย่างไร

เอกสารผลิตภัณฑ์ของตระกูลระบุแนวประมาณ (ขึ้นกับรุ่นย่อย):

- **System SRAM** รวมสูงสุดราวหลาย MB (เอกสาร E84 มักพูดถึงราว **6 MB** รวมโดเมน)
- **SRAM ในโดเมน Low-Power** ราว 1 MB ในบางสรุปสถาปัตยกรรม
- **RRAM** หน่วยไม่ลบเลือนใช้พลังงานต่ำ ราว 512 KB ในหลายรุ่น

ทำไมสำคัญ: โมเดล ML และบัฟเฟอร์เซ็นเซอร์แย่ง SRAM กัน · กราฟิก HMI กินหน่วยความจำ/แบนด์วิดท์บัส · การเลือกเก็บน้ำหนักโมเดลใน RRAM/flash ภายนอกมีผลต่อเวลาบูตและพลังงาน

---

## แนวคิด (6) — จากสแต็กจริงของ Infineon สู่ภาษาของหลักสูตร

| ศัพท์ในหลักสูตร | สิ่งที่มักสัมพันธ์ในสแต็กจริง | ผู้เรียนทำอะไร |
|---|---|---|
| **HAL / BSP** | BSP + การ bring-up / นามธรรมบอร์ด | เลือกบอร์ด เรียก init ตามคู่มือโปรเจกต์ |
| **Driver API** | ทางเข้าควบคุมเพริเฟอรัลที่หลักสูตรให้ใช้เป็นมาตรฐาน (บน PDL/HAL/ไดรเวอร์ของ SDK) | อ่าน/เขียน GPIO, UART, I2C, SPI, PWM, ADC |
| **Utility Modules** | โมดูลช่วยที่ใช้ซ้ำในโปรเจกต์ตัวอย่าง/ผลิตภัณฑ์ | buffer, filter เบา ๆ, logging helper |
| **Application** | นโยบายผลิตภัณฑ์ (ชั้นที่คุณเขียนเองเสมอ) | task, การตัดสินใจ, เรียกใช้ชั้นด้านล่าง |

กฎง่าย ๆ: **Utility จัดของ — Driver คุยกับฮาร์ดแวร์ — Application ตัดสินใจ**

---

## แนวคิด (7) — SDK ไม่ใช่ IDE

| คำ | คืออะไร |
|---|---|
| **ModusToolbox™ / VS Code** | เครื่องมือพัฒนา (สร้างโปรเจกต์, จัดการไลบรารี, เขียนโค้ด, build, debug) |
| **TESA Firmware SDK** | ชุดซอฟต์แวร์/API และแนวทางที่โค้ดของคุณเรียกใช้ในหลักสูตร |
| **Device Support Library** | แพ็กเกจรองรับชิปจาก Infineon (PDL/HAL/utilities) |

> จำให้ขึ้นใจ: **ติดตั้ง IDE ได้ ≠ เข้าใจ SDK แล้ว**

---

## ตัวอย่างสมบูรณ์ — ไล่ชั้นด้วยโจทย์จริง (Scenario A)

โจทย์: อ่านอุณหภูมิผ่าน I²C ทุก 1 วินาที ถ้าเกินเกณฑ์ให้เปิด LED และพิมพ์ข้อความทาง UART

| ขั้นตอน | ชั้น |
|---|---|
| เริ่มต้นบอร์ดและขา I²C / LED / UART | HAL / BSP |
| อ่าน I²C, เขียน GPIO, ส่ง UART | Driver API |
| เก็บตัวอย่างล่าสุด N ค่า / ค่าเฉลี่ยเคลื่อนที่ | Utility |
| เปรียบเทียบเกณฑ์ เปลี่ยนสถานะผลิตภัณฑ์ | Application |

ดูฉบับเต็ม (รวม Scenario B — always-on แล้วปลุกไปรันโมเดล) ใน [README.md](README.md) หัวข้อ 8.7

---

## ฝึกเติม/แล็บ

[แล็บ: จับคู่โดเมน MCU กับชั้นของ SDK](../l02-lab/README.md) — แล็บเชิงแนวคิด ไม่ต้อง flash บอร์ด (~30–45 นาที)

1. จับคู่โดเมนกับงาน 4 ข้อ พร้อมเหตุผล
2. ติดป้ายชั้นซอฟต์แวร์ให้โครงสร้างโฟลเดอร์ตัวอย่าง
3. ตอบโจทย์รวมสองสถานการณ์ (on-device gesture, always-on then wake)
4. ทำ checklist ถูก/ผิด 10 ข้อ ให้ได้อย่างน้อย 8/10 ก่อนไป โมดูล 2

---

## เช็กความเข้าใจ

1. งาน "ฟังคำปลุก (wake-word) แบบใช้พลังงานต่ำตลอดคืน" ควรอยู่โดเมนใดตามแนวทางของบทเรียน
2. ใน Scenario A (อ่านอุณหภูมิทุก 1 วินาที) ขั้นตอน "เก็บตัวอย่างล่าสุด N ค่า / ค่าเฉลี่ยเคลื่อนที่" อยู่ชั้นใด
3. ข้อใดตรงกับประโยค "ติดตั้ง IDE ได้ ≠ เข้าใจ SDK แล้ว" มากที่สุด

---

## ไปต่อ

- **SDK ≠ IDE** — เครื่องมืออยู่คนละชั้นกับไลบรารีที่โค้ดเรียกใช้
- บทเรียนนี้ไม่ flash บอร์ด — พร้อมแล้วสำหรับติดตั้งเครื่องมือใน **โมดูล 2 — ModusToolbox™ และ VS Code สำหรับพัฒนาเฟิร์มแวร์**
- หลังโมดูล 2 ไปต่อ **โมดูล 3 — GPIO และอุปกรณ์ต่อพ่วงพื้นฐาน**

[บทเรียนโมดูล 2 →](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md)

---

## แหล่งที่มา

"บทเรียน 1.1 — สถาปัตยกรรม MCU หลายโดเมนและชั้นของ Firmware SDK" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C1 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
