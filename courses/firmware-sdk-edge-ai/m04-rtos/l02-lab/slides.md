---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 4.2 — แล็บ: เฟิร์มแวร์หลาย task ด้วย FreeRTOS"
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

# บทเรียน 4.2 — แล็บ: เฟิร์มแวร์หลาย task ด้วย FreeRTOS

## สร้างสอง task คาบต่างกัน ส่งเหตุการณ์ปุ่มผ่าน queue ป้องกันบัสร่วมด้วย mutex แล้วเขียนโน้ตเรื่อง timing

**หลักสูตร TESA Firmware SDK สำหรับ Edge AI — โมดูล 4 · แล็บ**

---

## เป้าหมาย

เมื่อทำครบ คุณจะ

1. รันสอง task ที่กระพริบ LED ด้วยคาบเวลา 500 ms และ 200 ms โดยไม่ busy-wait
2. ส่งเหตุการณ์ปุ่มผ่าน queue ไปยัง task ที่พิมพ์ UART
3. ป้องกันทรัพยากรที่ใช้ร่วมด้วย mutex หรือ API ล็อกบัสของโปรเจกต์

---

## ก่อนเริ่ม

- [ ] ผ่านแล็บโมดูล 3 (GPIO + UART อย่างน้อย)
- [ ] โปรเจกต์ตัวอย่างที่เรียก `cm55_initialize` / `cm55_start_scheduler` ได้
- [ ] รู้จุดที่โปรเจกต์อนุญาตให้ `xTaskCreate` (หลัง init / ใน callback)

> อย่าเรียก `vTaskStartScheduler()` ซ้ำเองถ้าโปรเจกต์ใช้ `cm55_start_scheduler()` แล้ว
> **หมายเหตุ:** snippet ในแล็บนี้ใช้ API ของเฟิร์มแวร์ TESAIoT Bitstream ซึ่งยังไม่เปิดซอร์ส — ดูรายละเอียดที่หมายเหตุต้นบทเรียน [บทเรียน 4.1](../l01-freertos-programming/README.md)

---

## ดูของจริงก่อน — เกณฑ์ผ่านของแต่ละบล็อก

| บล็อก | เกณฑ์ผ่าน |
|---|---|
| Lab A — สองจังหวะกระพริบ (required) | เห็นสองจังหวะบนบอร์ดโดยไม่ใช้ busy-delay ยาวใน task เดียว |
| Lab B — ปุ่ม → Queue → UART (required) | กดปุ่มแล้วเห็นข้อความบน serial โดย task กระพริบยังทำงานต่อ |
| Lab C — ล็อกทรัพยากรร่วม (required) | อธิบายได้ว่าทำไมต้องล็อก และสาธิตว่าไม่แย่งบัสแบบสุ่มพัง |
| Lab D — ธงพร้อม (แนะนำ) | task ผู้รอไม่เริ่มงานก่อนสัญญาณพร้อม |

---

## ฝึกเติม/แล็บ (1) — Lab A: Two blink rates

1. สร้าง task `LAB_BLINK_SLOW` กระพริบ LED ด้วยคาบ **500 ms**
2. สร้าง task `LAB_BLINK_FAST` กระพริบ LED อีกดวง (หรือสลับสี) ด้วยคาบ **200 ms**
3. ใช้ priority คนละค่าเล็กน้อย (เช่น idle+1 และ idle+2) แล้วสังเกตพฤติกรรม

```c
led_controller_toggle(LED_RED);
vTaskDelay(pdMS_TO_TICKS(500));
```

---

## ฝึกเติม/แล็บ (2) — Lab B: Button → Queue → UART task

1. สร้างคิวข้อความสั้น ๆ (`xQueueCreate`)
2. สร้าง task ดึงคิวแล้ว `printf` / `LOG_INFO`
3. ใน `cm55_button_on_pressed` (หรือจุด event ปุ่ม) ให้ `xQueueSend` ข้อความ เช่น `btn\r\n`

---

## ฝึกเติม/แล็บ (3) — Lab C: Shared resource lock

เลือกอย่างน้อยหนึ่งข้อ:

**C1 Mutex ของคุณเอง**
- สร้าง `xSemaphoreCreateMutex`
- task สองตัวแชร์การพิมพ์หรือแชร์ตัวแปรสถานะภายใต้ Take/Give

**C2 I²C lock ของ SDK**
- อ่านเซ็นเซอร์ใน task หนึ่ง
- ห่อด้วย `cm55_i2c_manager_i2c_lock` / `unlock` (หรือ API ล็อกที่โปรเจกต์ของคุณมี)

---

## ฝึกเติม/แล็บ (4) — Lab D: Ready flag (แนะนำ)

1. สร้าง `xEventGroupCreate`
2. task setup ตั้งบิต "READY" หลัง init เสร็จ
3. task อื่น `xEventGroupWaitBits` ก่อนเริ่มงาน

หรือใช้ binary semaphore เป็นสัญญาณ "พร้อมแล้ว" ก็ได้

---

## เช็กความเข้าใจ — Lab E: Timing notes

ตอบสั้น ๆ (5–8 บรรทัด):

1. ถ้าเอา `printf` ใส่ ISR จะเสี่ยงอะไร
2. ถ้า priority ของ task หนักสูงสุดตลอดเวลา ระบบจะเป็นอย่างไร
3. `depth × sizeof(item)` ของคิวกระทบ RAM อย่างไร

---

## ไปต่อ

ก่อนส่งงาน ตรวจกับตัวเองว่า:

- [ ] Lab A ผ่าน
- [ ] Lab B ผ่าน
- [ ] Lab C ผ่าน
- [ ] (แนะนำ) Lab D
- [ ] Lab E ตอบครบ
- [ ] กรอกตาราง API ใน [rtos-patterns.md](../l01-freertos-programming/resources/rtos-patterns.md)

พร้อมแล้ว ไปต่อ **โมดูล 5 — ข้อมูลเซ็นเซอร์และการเตรียมข้อมูลสำหรับ Edge AI**

[บทเรียนโมดูล 5 →](../../m05-sensor-data/l01-sensor-data-for-edge-ai/README.md)

---

## แหล่งที่มา

"บทเรียน 4.2 — แล็บ: เฟิร์มแวร์หลาย task ด้วย FreeRTOS" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

เนื้อหาต้นฉบับโดย ผศ.ดร.สันติ นุราช ภาควิชาวิศวกรรมระบบควบคุมและเครื่องมือวัด คณะวิศวกรรมศาสตร์
มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี (KMUTT) (https://github.com/drsanti) ภายใต้การสนับสนุนของสมาคมสมองกลฝังตัวไทย (TESA)
นำเข้าจาก drsanti/TESAIoT-Courses — C1 (commit `287c218`) ภายใต้สัญญาอนุญาต CC BY 4.0

ไม่มีภาพจากบุคคลที่สามในสไลด์ชุดนี้
