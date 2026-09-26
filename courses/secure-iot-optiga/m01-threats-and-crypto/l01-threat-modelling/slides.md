---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.1 — Threat model ของอุปกรณ์ IoT"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0"
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

# บทเรียน 1.1 — Threat model ของอุปกรณ์ IoT

## ระบุทรัพย์สิน ผู้โจมตี และช่องทางโจมตีของอุปกรณ์หนึ่งชิ้น แล้วเลือกมาตรการที่ตรวจได้

**โมดูล 1 — Threat model และพื้นฐานวิทยาการเข้ารหัส**

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ระบุทรัพย์สินที่ต้องปกป้องของอุปกรณ์ IoT หนึ่งชิ้นได้อย่างน้อยสี่รายการ
2. จัดภัยคุกคามตามหมวด STRIDE และจับคู่แต่ละภัยกับมาตรการป้องกันที่ตรวจได้
3. เทียบ threat model ของตัวเองกับข้อกำหนดพื้นฐานของ ETSI EN 303 645 และระบุข้อที่ยังขาด

---

## ก่อนเริ่ม

- รู้: ภาษา C ระดับอ่านโค้ดคนอื่นออก และหลักการ publish/subscribe ของ MQTT
- อุปกรณ์: บทนี้เป็นงานคิดบนกระดาษเป็นหลัก บอร์ดยังไม่ต้องเสียบ
- แม่แบบ: `resources/threat-model-template.md` — งานชิ้นนี้จะกลับมาอีกครั้งในบทเรียน 5.3

**อุปกรณ์ตัวอย่างของหลักสูตร** คือเฟิร์มแวร์แม่แบบ `bento-firmware-template-mtb-only` บน TESAIoT Dev Kit ที่เชื่อม MQTTS ไปยัง `mqtt.tesaiot.dev` — server-TLS (พอร์ต 8884) หรือ mTLS (พอร์ต 8883)

---

## ดูของจริงก่อน

```text
[MQTT] Waiting for WiFi...
[MQTT-Config] Mode=%d, Broker=%s:%u, Client=%s, User=%s, PassLen=%u
[MQTT] Connecting to '%s:%u' as '%s'...
[MQTT] Connected to broker
```

สังเกตบรรทัด `[MQTT-Config]` — มันพิมพ์ชื่อผู้ใช้ แต่พิมพ์รหัสผ่านเป็นแค่ **ความยาว** (`PassLen`) เพราะ console ไม่ใช่วิทยุ และมักเป็นจอที่คนอื่นมองเห็นด้วย

แปลว่าคนเขียนเฟิร์มแวร์ได้ทำ threat model ไปแล้วอย่างน้อยหนึ่งข้อ — นับสาย UART เป็นช่องทางรั่วไหล **ก่อนอ่านต่อ** เขียนห้าอย่างที่ผู้โจมตีอยากได้จากบอร์ดนี้

---

## แนวคิด (1) — ทรัพย์สินและผู้โจมตี

| ทรัพย์สิน | สมบัติที่ต้องรักษา |
|---|---|
| กุญแจลับของตัวตนอุปกรณ์ (ใน OPTIGA™ Trust M) | ความลับ |
| ใบรับรองและ `device_id` | ความถูกต้อง |
| trust anchor ที่ใช้ตรวจเซิร์ฟเวอร์ | ความถูกต้อง |
| รหัส WiFi / รหัสผ่าน MQTT | ความลับ |
| สถานะวงจรชีวิตของชิป (LcsO) | ถูกต้อง เปลี่ยนได้ทางเดียว |

**ผู้โจมตีสี่แบบ** ผู้โจมตีทางเครือข่าย · คนที่ถือบอร์ดได้ (USB/I2C) · อุปกรณ์อื่นที่ถูกเจาะแล้ว · คนในที่เข้าถึง broker

---

## แนวคิด (2) — ขอบเขตความเชื่อใจ

```text
            [เซนเซอร์บนบอร์ด]
                   │ I2C
 [CM55: จอและสัมผัส] ──IPC── [CM33_NS: WiFi, MQTT] ──I2C── [OPTIGA Trust M]
                                    │
 ═══════ ขอบเขต: อากาศ ═════════════╪═══════════════════════════════
                                    │ WiFi
                             [access point] ── internet ── [broker] ── [Platform]
 ═══════ ขอบเขต: คนที่ถือบอร์ด ═══════════════════════════════════
   พอร์ต USB/KitProg (debug, flash) · สาย I2C ที่วัดได้บนบอร์ด
```

ทุกจุดที่ข้ามเส้นคือจุดที่ต้องถามว่า "อีกฝั่งเป็นใคร และเรารู้ได้อย่างไร"

---

## แนวคิด (3) — STRIDE: หกคำถามที่ถามทุกขอบเขต

| หมวด | ผู้โจมตีทำอะไร | สมบัติที่ต้องมี |
|---|---|---|
| **S**poofing | ปลอมตัวเป็นคนอื่น | การยืนยันตัวตน |
| **T**ampering | แก้ข้อมูล | ความถูกต้อง |
| **R**epudiation | ทำแล้วปฏิเสธ | ตามรอยได้ |
| **I**nfo disclosure | อ่านข้อมูลไม่มีสิทธิ์ | ความลับ |
| **D**enial of service | ทำให้ใช้ไม่ได้ | ความพร้อมใช้งาน |
| **E**levation of privilege | ได้สิทธิ์เกิน | การอนุญาต |

หมวดหนึ่งอาจว่างได้ แต่ต้องว่างเพราะคิดแล้ว ไม่ใช่เพราะลืมถาม

---

## แนวคิด (4) — มาตรการที่ตรวจได้ และเส้นฐาน ETSI

"เราใช้ TLS" **ไม่ใช่**มาตรการที่ตรวจได้ — มันเป็นแค่ชื่อเทคโนโลยี มาตรการที่ตรวจได้ต้องบอก **การทดสอบที่ทำให้ผลออกมาเป็นแดงได้** เช่น "ชี้ broker ไปเซิร์ฟเวอร์ที่ใช้ใบ self-signed แล้วอุปกรณ์ต้องตัดการเชื่อมต่อก่อนส่ง MQTT CONNECT"

เทียบกับ [ETSI EN 303 645](https://www.etsi.org/deliver/etsi_en/303600_303699/303645/03.01.03_60/en_303645v030103p.pdf) — ตัวอย่างข้อที่เกี่ยวกับโหนดเซนเซอร์โดยตรง

| ข้อ | สถานะ | ใจความ |
|---|---|---|
| 5.1-2A | R | ไม่ควรใช้รหัสผ่านยืนยันตัวตนระหว่างเครื่อง |
| 5.4-1, 5.4-3 | M | เก็บค่าความปลอดภัยอย่างปลอดภัย ห้ามฝังในซอร์ส |
| 5.6-4A | M | พอร์ต debug ต้องปิดหรือยืนยันตัวตน |

---

## ตัวอย่างสมบูรณ์ — threat model หนึ่งหน้า (บางส่วน)

**ขอบเขต** TESAIoT Dev Kit หนึ่งเครื่อง เฟิร์มแวร์แม่แบบ `mtb-only` ที่ `ef72c1b`

| หมวด | ภัย | มาตรการ | ตรวจอย่างไร |
|---|---|---|---|
| S | AP ปลอมทำตัวเป็น broker | ตรวจใบเซิร์ฟเวอร์กับ CA ที่ปักไว้ | ใบ self-signed ต้องล้มก่อน MQTT CONNECT |
| T | เฟิร์มแวร์ถูกเปลี่ยนเป็นตัวไม่ได้ลงนาม | secure boot ตรวจลายเซ็น CM33_S | build กุญแจอื่น flash บอร์ด provision แล้ว ต้องไม่บูต |
| I | กุญแจลับถูกอ่านออกจาก flash | กุญแจอยู่ใน OPTIGA™ Trust M | ค้นใน image ที่ build ไม่เจอกุญแจลับ |

**ช่องว่างเมื่อเทียบ ETSI** เช่น 5.1-2A (server-TLS ใช้รหัสผ่าน), 5.3-10 (`c_ota_client` มีฟิลด์ตรวจแต่ฟังก์ชันยังเป็น TODO ที่คืนผ่านเสมอ)

---

## ฝึกเติม / แล็บ

**ฝึกเติม** จัดภัยห้าข้อเข้าหมวด STRIDE พร้อมการทดสอบที่ตรวจได้ เช่น "มีคนส่งข้อความ `commands/...` ปลอมมาสั่งอุปกรณ์" (S/T), "publish ถี่จนคิวเต็ม ข้อมูลหาย" (D)

**แล็บ** threat model หนึ่งหน้าของอุปกรณ์ของคุณ

1. เลือกอุปกรณ์หนึ่งชิ้น เขียนขอบเขตในหนึ่งย่อหน้า
2. วาดแผนภาพขอบเขตความเชื่อใจ (อย่างน้อยเส้นอากาศและเส้นคนถือบอร์ด)
3. ระบุทรัพย์สินอย่างน้อยสี่รายการ พร้อมสมบัติที่ต้องรักษา (C, I, A)
4. เดิน STRIDE ครบหกหมวด ได้ภัยอย่างน้อยหกข้อ ทุกข้อมีการทดสอบที่ผลเป็นแดงได้
5. เทียบกับ ETSI เขียนช่องว่างอย่างน้อยสองข้อ

---

## เช็กความเข้าใจ

1. ข้อใดเป็น **ทรัพย์สิน** ที่ต้องรักษาความถูกต้องเป็นหลัก ไม่ใช่ความลับ
   - ก) รหัส WiFi ในที่เก็บข้อมูลรับรอง · ข) trust anchor ใน `tesaiot_root_ca.h` · ค) กุญแจลับในช่อง `0xE0F1` · ง) รหัสผ่าน MQTT ในโหมด server-TLS

2. "อุปกรณ์ใช้ TLS 1.2" เป็นมาตรการที่ตรวจได้หรือไม่
   - ก) ได้ เพราะ TLS 1.2 เป็นมาตรฐาน · ข) ไม่ได้ ต้องเขียนเป็นการทดสอบที่ผลเป็นแดงได้ · ค) ได้ ถ้า log ขึ้น `Connected to broker` · ง) ไม่ได้ เพราะ TLS ไม่เกี่ยวกับ STRIDE

3. คุณพบภัย "ผู้โจมตีส่งคำสั่งปลอมเข้าหัวข้อ commands" ควรจัดเป็นหมวดใดเป็นหลัก
   - ก) Denial of service · ข) Spoofing · ค) Information disclosure · ง) Repudiation

---

## ไปต่อ

ในตารางตัวอย่าง มาตรการเกือบทุกข้อพึ่ง hash ลายเซ็น การเข้ารหัส หรือใบรับรอง บทต่อไป [บทเรียน 1.2: พื้นฐานวิทยาการเข้ารหัสสำหรับระบบฝังตัว](../l02-crypto-basics/README.md) จะแยกเครื่องมือเหล่านี้ให้ชัด

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"Secure IoT กับ OPTIGA™ Trust M" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY-NC 4.0

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY-NC 4.0
