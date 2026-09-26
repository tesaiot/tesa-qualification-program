---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.2 — แล็บ: จับคู่โดเมน MCU กับชั้นของ SDK"
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

# บทเรียน 1.2 — แล็บ: จับคู่โดเมน MCU กับชั้นของ SDK

## แล็บเชิงแนวคิด (ไม่ต้อง flash บอร์ด): กรอกตารางจับคู่โดเมนกับงาน ติดป้ายชั้นซอฟต์แวร์ และตอบโจทย์รวมสองสถานการณ์

**หลักสูตร TESA Firmware SDK สำหรับ Edge AI — โมดูล 1 · แล็บ**

---

## เป้าหมาย

เมื่อทำครบ คุณจะ

- จับคู่โดเมนฮาร์ดแวร์ (Cortex-M55 / Cortex-M33 / Ethos-U55 NPU) กับประเภทงานได้อย่างสมเหตุสมผล
- ระบุได้ว่าโค้ดประเภทใดควรอยู่ชั้น HAL/BSP, Driver API, Utility หรือ Application
- ตรวจความเข้าใจด้วย checklist สั้น ๆ

เกณฑ์ผ่าน: กรอกตารางส่วนที่ 1–2 ครบพร้อมเหตุผล และทำ checklist ถูก/ผิด (ส่วนที่ 4) ได้อย่างน้อย 8 จาก 10 ข้อ

---

## ก่อนเริ่ม

- [ ] อ่านจบ [บทเรียน 1.1 — สถาปัตยกรรม MCU หลายโดเมนและชั้นของ Firmware SDK](../l01-architecture-and-sdk-layers/README.md)
- [ ] เปิดแผ่นสรุป [sdk-layer-cheatsheet.md](../l01-architecture-and-sdk-layers/resources/sdk-layer-cheatsheet.md)
- [ ] กระดาษ โน้ต หรือไฟล์ว่างสำหรับกรอกคำตอบ

> **Flash / Hello World อยู่ที่ไหน?** การติดตั้ง ModusToolbox สร้างโปรเจกต์ และ flash บอร์ดอยู่ใน **โมดูล 2** — แล็บนี้ตั้งใจเป็นแผนที่ความคิดก่อนลงมือกับเครื่องมือ

---

## ดูของจริงก่อน — โครงสร้างโฟลเดอร์ตัวอย่าง

สมมติโครงสร้างโฟลเดอร์อย่างง่ายของโปรเจกต์เฟิร์มแวร์ (ชื่อสมมติเพื่อการเรียน — ไม่ใช่ path จริงของ SDK):

```text
app/
  main.c                 # product logic, สร้าง task
  gesture_policy.c       # ตัดสินใจเมื่อได้ผล inference
bsp/
  board_init.c           # clock, pin mux, bring-up
drivers/
  gpio_api.c
  i2c_api.c
  uart_api.c
utils/
  ring_buffer.c
  simple_filter.c
```

โครงสร้างนี้คือโจทย์ของส่วนที่ 2 ในแล็บ

---

## ฝึกเติม/แล็บ (1) — จับคู่โดเมนกับงาน (Part 1)

เลือกโดเมนที่เหมาะสมที่สุดสำหรับแต่ละงาน (ตอบได้มากกว่าหนึ่งโดเมนถ้าจำเป็น แต่ต้องเขียนเหตุผลสั้น ๆ)

| # | งาน | ตัวเลือก |
|---|---|---|
| 1 | วนอ่านปุ่มและกระพริบ LED ตามสถานะ UI | M55 / M33 / NPU |
| 2 | ฟัง wake-word แบบใช้พลังงานต่ำตลอดเวลา | M55 / M33 / NPU |
| 3 | รันโมเดล gesture recognition บนอุปกรณ์ | M55 / M33 / NPU |
| 4 | จัดรูปแบบ JSON แล้ว publish MQTT | M55 / M33 / NPU |

---

## ฝึกเติม/แล็บ (2) — ติดป้ายชั้น SDK (Part 2)

กรอกตาราง โดยใช้โครงสร้างโฟลเดอร์จากสไลด์ก่อนหน้า — ชั้นที่เลือกได้คือ HAL/BSP, Driver API, Utility หรือ Application

| กลุ่มไฟล์ | ชั้น | เหตุผลสั้น ๆ |
|---|---|---|
| `bsp/board_init.c` | | |
| `drivers/i2c_api.c` | | |
| `utils/ring_buffer.c` | | |
| `app/gesture_policy.c` | | |

---

## ฝึกเติม/แล็บ (3) — โจทย์รวม 3A: On-Device Gesture

> อ่านค่า IMU ผ่าน I²C เป็นช่วงเวลาคงที่ → เก็บหน้าต่างตัวอย่างสั้น ๆ → ส่งเข้าโมเดลบน Ethos-U55 → ถ้าเป็นท่าทางที่สนใจให้เปิด LED และเตรียมข้อความไปคลาวด์

ตอบเป็นข้อ ๆ (ไม่ต้องเขียนโค้ด):

1. ชั้นใดรับผิดชอบการคุย I²C กับชิปเซ็นเซอร์
2. ชั้นใดเหมาะกับบัฟเฟอร์หน้าต่างตัวอย่าง
3. โดเมน/บล็อกฮาร์ดแวร์ใดเร่ง inference ขั้นสูง
4. ชั้นใดตัดสินใจว่า "ท่านี้สำคัญพอจะเปิด LED"
5. เหตุใดการ publish MQTT จึงยังไม่ใช่หน้าที่ของ NPU

---

## ฝึกเติม/แล็บ (4) — โจทย์รวม 3B: Always-On Then Wake

> ระบบรอจับกิจกรรมเสียงบนโดเมนพลังงานต่ำตลอดคืน เมื่อมีเหตุการณ์จึงปลุกโดเมนสมรรถนะสูงเพื่อรันโมเดลหนักและอัปเดตจอ

ตอบ:

1. คอร์/ตัวเร่งใดเหมาะกับช่วง "รอฟังตลอดคืน"
2. คอร์/ตัวเร่งใดเหมาะกับช่วง "inference หนักหลังถูกปลุก"
3. เพราะเหตุใดจึงไม่ควรให้ Ethos-U55 ทำงานเต็มที่ตลอด 24 ชั่วโมงถ้าผลิตภัณฑ์ใช้แบตเตอรี่

---

## เช็กความเข้าใจ — checklist ถูก/ผิด (Part 4)

ตอบ **ถูก** หรือ **ผิด** (เกณฑ์แนะนำ: ได้อย่างน้อย 8/10 ก่อนไป โมดูล 2)

1. TESA Firmware SDK คือชื่อของโปรแกรม IDE แทน ModusToolbox
2. HAL/BSP ช่วยให้นักพัฒนาไม่ต้องตั้งค่า register พื้นฐานของบอร์ดด้วยตัวเองทุกครั้ง
3. Driver API เป็นชั้นหลักสำหรับควบคุม GPIO, UART, I2C, SPI, PWM, ADC ในแนวทางของหลักสูตร
4. Utility modules ใช้แทน Driver เมื่อต้องการพูดกับฮาร์ดแวร์โดยตรง
5. Cortex-M55 และ Ethos-U55 มีบทบาทเดียวกันในทุกงาน

---

## เช็กความเข้าใจ — checklist ถูก/ผิด (ต่อ)

6. Edge AI หมายถึงการส่งข้อมูลดิบทั้งหมดขึ้นคลาวด์เสมอ
7. การเลือกโดเมนประมวลผลมีผลต่อพลังงานและความหน่วง (latency)
8. โมดูล 1 ต้องการให้ผู้เรียน flash เฟิร์มแวร์ Hello World ให้สำเร็จ
9. ความปลอดภัยระดับชิป (เช่น Secure Boot) เป็นส่วนหนึ่งของสถาปัตยกรรม ไม่ใช่หัวข้อแยกจาก MCU
10. บทถัดไป (โมดูล 2) จะลงมือติดตั้งเครื่องมือและสร้างโปรเจกต์จริง

---

## ไปต่อ

ก่อนส่งงาน ตรวจกับตัวเองว่า:

- [ ] กรอกตารางส่วนที่ 1 ครบ พร้อมเหตุผล
- [ ] กรอกตารางส่วนที่ 2 ครบ
- [ ] ตอบส่วนที่ 3A และ 3B ครบ
- [ ] ทำ checklist ส่วนที่ 4 ได้อย่างน้อย 8/10
- [ ] อธิบายได้แล้วว่า SDK ต่างจาก IDE อย่างไร และ multi-domain ต่างจากคอร์เดียวอย่างไร

พร้อมแล้ว ไปต่อ **โมดูล 2 — ModusToolbox™ และ VS Code สำหรับพัฒนาเฟิร์มแวร์**

[บทเรียนโมดูล 2 →](../../m02-toolchain/l01-modustoolbox-and-vscode/README.md)

---

## แหล่งที่มา

"บทเรียน 1.2 — แล็บ: จับคู่โดเมน MCU กับชั้นของ SDK" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C1 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
