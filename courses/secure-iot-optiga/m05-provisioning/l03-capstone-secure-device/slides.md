---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 5.3 — งานปลายทาง: อุปกรณ์ที่ปลอดภัยหนึ่งชิ้น"
footer: "TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY 4.0"
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

# บทเรียน 5.3 — งานปลายทาง: อุปกรณ์ที่ปลอดภัยหนึ่งชิ้น

## รวม threat model การลงทะเบียน mTLS และการอัปเดตแบบป้องกัน เป็นอุปกรณ์หนึ่งชิ้นพร้อมหลักฐาน

**โมดูล 5 — การลงทะเบียนอุปกรณ์อย่างปลอดภัย**

---

## เป้าหมาย

งานชิ้นสุดท้ายไม่ได้วัดว่าอุปกรณ์ "ดูเหมือนทำงาน" แต่วัดว่าคุณ **พิสูจน์** ได้ไหมว่ามันทำงานตามที่อ้าง

เมื่อจบบทเรียนนี้ คุณจะ

1. ส่งอุปกรณ์ที่ลงทะเบียนแล้ว เชื่อมต่อด้วย mTLS และส่งข้อมูลขึ้นแพลตฟอร์มได้ พร้อม log เป็นหลักฐาน
2. ปรับ threat model จากโมดูลแรกให้สะท้อนมาตรการที่ทำจริง และระบุความเสี่ยงที่ยังเหลือ

---

## ก่อนเริ่ม

- เรียนมาก่อน: ทุกบทเรียนในหลักสูตรนี้ โดยเฉพาะแล็บของ 3.1, 3.2 และ 5.1
- ไฟล์ที่ต้องมี: threat model จาก [บทเรียน 1.1](../../m01-threats-and-crypto/l01-threat-modelling/README.md) และ `resources/evidence-checklist.md`
- **การอนุมัติ** การลงทะเบียนจริงสร้างกุญแจใหม่ในชิป และ Protected Update ทำให้ตัวนับ version ขึ้นถาวร — ทั้งสองต้องได้รับอนุญาตจากผู้สอนก่อน งานนี้ **ไม่มีขั้นใดเขียน metadata tag `C0`**

---

## ดูของจริงก่อน

ตลอดหลักสูตรเราเจอกรณีเดียวกันซ้ำหลายครั้ง — **บรรทัดที่ดูเหมือนสำเร็จ ไม่ได้แปลว่าสำเร็จ**

- `[PSA-Sign] Using Key OID ...` พิมพ์ **ก่อน** การลงนาม (3.1)
- `tesaiot_mqtt_publish()` คืน `true` แปลว่า **เข้าคิว** ไม่ใช่ถึง broker (3.2)
- `tesaiot_publish_protected_update()` คืน `0` แปลว่า **ขอแล้ว** ไม่ใช่เสร็จแล้ว (4.2)
- `ota_verify_firmware()` คืน `OTA_OK` โดยไม่ได้ตรวจอะไรเลย (4.2)

**ถามตัวเองก่อนเริ่ม** สำหรับแต่ละข้อข้างบน หลักฐานที่ **ถูก** คืออะไร และได้มาจากฝั่งไหน

---

## แนวคิด (1) — หลักฐานสี่ชนิด เรียงจากอ่อนไปแข็ง

```text
1. ข้อความที่อุปกรณ์พิมพ์    ใช้ได้เมื่อรู้ว่าพิมพ์ตอนไหน และไม่มีบรรทัด error ประกอบ
2. สถานะที่อ่านกลับจากชิป    เช่น metadata ก่อน/หลัง ชิปตอบตามจริงเสมอ
3. หลักฐานจากฝั่งผู้รับ      เช่นข้อมูลที่ subscriber ได้รับ
4. การทดสอบด้านลบ           กรณีที่ควรล้ม และล้มจริง
```

**มาตรการที่ไม่เคยถูกทดสอบให้ล้ม ยังไม่ได้พิสูจน์อะไร**

หลักฐานต้อง **ไม่รั่ว** — ห้ามแนบรหัสผ่าน MQTT, รหัส WiFi, หรือไฟล์ใน bundle ลงรายงาน ถ้าจะเผยแพร่ ให้แทน `device_id`/UID ด้วยค่าที่ปิดบางส่วน

---

## แนวคิด (2) — ความเสี่ยงที่ยังเหลือของแม่แบบ (commit ef72c1b)

| ความเสี่ยงที่ยังเหลือ | จากบทเรียน |
|---|---|
| ชิปกันขโมยกุญแจ แต่กันเฟิร์มแวร์ที่ถูกยึดสั่งลงนามไม่ได้ | 1.2 |
| ไม่ตรวจวันหมดอายุ/การเพิกถอนของใบรับรอง | 1.2 |
| สาย I2C ระหว่าง MCU กับชิปไม่ได้เข้ารหัสในค่าตั้งเริ่มต้น | 1.2 |
| TLS 1.2 ส่งใบรับรองอุปกรณ์แบบไม่เข้ารหัสใน handshake | 3.1 |
| ห่วงโซ่ secure boot ครอบแค่ CM33_S และเปิดเมื่อ provision แล้วเท่านั้น | 4.1 |
| OTA client ตัวอย่างยังไม่ตรวจ hash และลายเซ็นของเฟิร์มแวร์ | 4.2 |

threat model ที่อัปเดตแล้วต้องบอกตรง ๆ ว่าอะไรยังไม่ได้ป้องกัน

---

## ตัวอย่างสมบูรณ์ — หนึ่งแถวของตารางหลักฐาน

| ข้ออ้าง | หลักฐานบวก | หลักฐานลบ | ชนิด |
|---|---|---|---|
| อุปกรณ์เชื่อม broker ด้วย mTLS ด้วยกุญแจของ TESAIoT | `[mTLS] device pair verified — using TESAIoT identity`, `[PSA-Sign] Using Key OID 0xE0F1 ...`, `[MQTT] Connected to broker` ในการเชื่อมต่อเดียวกัน | ไม่มีบรรทัด ERROR ของ `trustm_ecdsa_sign` · `openssl s_client` ที่พอร์ต 8883 ไม่มีใบ client ถูกปฏิเสธ | 1 และ 4 |

หลักฐานบวกมีสามบรรทัด เพราะบรรทัดเดียวไม่พอ (3.1) หลักฐานลบพิสูจน์ว่าพอร์ตนั้นต้องการใบรับรองจริง ไม่ใช่ปล่อยทุกคนเข้า

---

## ฝึกเติม / แล็บ

**ฝึกเติม** จัดชนิดหลักฐาน: `mosquitto_sub` ได้รับ payload → **3 (ผู้รับ)** · `read_metadata` ก่อน/หลัง PU → **2 (ชิป)** · `tesaiot_mqtt_publish()` คืน `true` → **ไม่ใช่หลักฐาน** · พอร์ต 8884 ไม่ใส่ CA ได้ `Verify return code: 20` → **4 (ด้านลบ)**

**แล็บ** (~55 นาที) สถานะเริ่มต้น (อ่าน `C0`/`D0`) → ลงทะเบียน (ผู้สอนอนุญาต) → เปลี่ยนเป็น mTLS เก็บ log เต็ม → publish+พิสูจน์ว่าถึง → การทดสอบด้านลบ ≥2 ข้อ → Protected Update (ถ้าอนุญาต) → สถานะสุดท้าย (`C0` ต้องเท่าข้อ 1) → อัปเดต threat model → ตรวจการรั่วก่อนส่ง

---

## เช็กความเข้าใจ

1. หลักฐานชุดใดพอจะอ้างว่า "ชิปลงนาม CertificateVerify สำเร็จด้วยกุญแจที่ลงทะเบียนแล้ว"
   - ก) บรรทัด `Using Key OID 0xE0F1` อย่างเดียว · ข) บรรทัด device pair verified, Using Key OID 0xE0F1, ไม่มีบรรทัด ERROR ของ trustm_ecdsa_sign และ Connected to broker ในการเชื่อมต่อเดียวกัน · ค) หน้าจอขึ้นว่าเชื่อมต่อแล้ว · ง) `tesaiot_mqtt_connect()` คืน true

2. ข้อใดควรอยู่ในช่อง "ความเสี่ยงที่ยังเหลือ" ของ threat model หลังทำงานนี้เสร็จ
   - ก) ไม่มี เพราะใช้ mTLS แล้ว · ข) ห่วงโซ่ secure boot ครอบแค่ CM33_S และอุปกรณ์ไม่ตรวจวันหมดอายุของใบรับรอง · ค) กุญแจลับอยู่ใน flash · ง) รหัสผ่าน MQTT ถูกพิมพ์บน console

3. ทำไมต้องมีการทดสอบด้านลบในรายงาน
   - ก) เพื่อให้รายงานยาวขึ้น · ข) เพราะมาตรการที่ไม่เคยถูกทดสอบให้ล้ม อาจผ่านทุกครั้งไม่ว่ามันจะทำงานหรือไม่ · ค) เพราะแพลตฟอร์มบังคับ · ง) เพราะการทดสอบด้านบวกผิดเสมอ

---

## ไปต่อ

คุณผ่านหลักสูตร Secure IoT กับ OPTIGA™ Trust M แล้ว ทางที่ไปต่อได้

- ปิดช่องว่างของแม่แบบในงานของคุณเอง เช่นเติมการตรวจใน OTA client หรือออกแบบให้ CM33_S ตรวจ image ถัดไป
- อ่าน AN237849 ก่อนวางแผน provision secure boot ให้ผลิตภัณฑ์จริง
- ทบทวน TESAIoT Firmware Stack โมดูล 5 และลองตัวอย่างบน TESAIoT Developer Hub

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มาและเครดิต

"Secure IoT กับ OPTIGA™ Trust M" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program
สัญญาอนุญาต CC BY 4.0

TESA Open Knowledge · © 2026 สมาคมสมองกลฝังตัวไทย (TESA) · CC BY 4.0
