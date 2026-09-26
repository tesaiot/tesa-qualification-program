---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.1 — ความเสี่ยงและการปฏิบัติตามกฎ"
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

# บทเรียน 2.1 — ความเสี่ยงและการปฏิบัติตามกฎ

## รู้จักความเสี่ยงสี่กลุ่มของผลิตภัณฑ์ IoT: ความปลอดภัยไซเบอร์ ข้อมูลส่วนบุคคลตาม PDPA มาตรฐานและการรับรอง และห่วงโซ่อุปทาน

**โมดูล 2 — ตัดสินใจและส่งโจทย์**

หลักสูตร **Edge AI และ IoT สำหรับการตัดสินใจเชิงผลิตภัณฑ์** · ไม่ต้องเขียนโค้ด ไม่ต้องมีบอร์ด

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ระบุหลักความปลอดภัยพื้นฐานของอุปกรณ์ IoT และแหล่งอ้างอิงมาตรฐาน
2. ตัดสินได้ว่าผลิตภัณฑ์เก็บข้อมูลส่วนบุคคลหรือข้อมูลอ่อนไหวหรือไม่ และรู้ว่าใครกำกับ
3. รู้ว่าผลิตภัณฑ์แบบไหนต้องตรวจเรื่องมาตรฐานกับหน่วยงานใด
4. ระบุความเสี่ยงด้านห่วงโซ่อุปทานและวิธีลดความเสี่ยง

> **ข้อควรทราบ** บทนี้ให้ภาพรวมเพื่อช่วยถามคำถามที่ถูก ไม่ใช่คำปรึกษาทางกฎหมาย ก่อนวางขายจริง ให้ตรวจกับหน่วยงานที่เกี่ยวข้องโดยตรงและปรึกษานักกฎหมายหรือห้องทดสอบที่ได้รับการรับรอง กฎและประกาศเปลี่ยนได้ ให้เปิดดูฉบับล่าสุดจากแหล่งทางการเสมอ

---

## ก่อนเริ่ม / ดูของจริงก่อน

**ก่อนเริ่ม** จากบทที่แล้ว ค่าทดสอบรับรองมาตรฐานอยู่ในต้นทุนก้อนไหน และอุปกรณ์ของคุณส่งข้อมูลด้วยคลื่นวิทยุ (WiFi, Bluetooth, LoRa, เครือข่ายมือถือ) หรือไม่

**ดูของจริงก่อน** สองเรื่องสมมติที่เกิดขึ้นได้จริง และป้องกันได้ตั้งแต่ขั้นออกแบบด้วยต้นทุนต่ำกว่าการแก้ทีหลังมาก

- บริษัทหนึ่งขายกล้องในบ้านที่ใช้รหัสผ่านเริ่มต้นเหมือนกันทุกเครื่อง และไม่มีวิธีอัปเดตเฟิร์มแวร์ — มีคนพบวิธีเข้าถึงกล้องทุกเครื่องจากอินเทอร์เน็ต
- บริษัทหนึ่งสั่งผลิตล็อตแรกแล้ว เพิ่งรู้ว่าชิ้นส่วนสำคัญตัวหนึ่งมีผู้ขายรายเดียว และผู้ขายประกาศหยุดผลิต

---

## แนวคิด (1) — ความปลอดภัยไซเบอร์ของตัวอุปกรณ์

หลักพื้นฐานที่มาตรฐานสากลด้าน IoT พูดตรงกันหลายข้อ

- ไม่มีรหัสผ่านเริ่มต้นที่เหมือนกันทุกเครื่อง
- อัปเดตซอฟต์แวร์ได้อย่างปลอดภัยตลอดอายุผลิตภัณฑ์ และบอกลูกค้าว่าจะดูแลนานเท่าไร
- เก็บกุญแจและข้อมูลลับอย่างปลอดภัย เช่นในชิปความปลอดภัย (secure element)
- สื่อสารแบบเข้ารหัส เช่น TLS และยืนยันตัวตนทั้งอุปกรณ์และเซิร์ฟเวอร์
- มีช่องทางรับแจ้งช่องโหว่และมีคนรับผิดชอบตอบ

แหล่งอ้างอิง: ETSI EN 303 645 · NIST IR 8259 · OWASP IoT Project — เป็นมาตรฐานยุโรป/สหรัฐฯ ไม่ใช่กฎหมายไทย แต่ใช้เป็นรายการตรวจที่ดีได้ และจำเป็นถ้าวางแผนส่งออก

---

## แนวคิด (2) — ข้อมูลส่วนบุคคลตาม PDPA

**พระราชบัญญัติคุ้มครองข้อมูลส่วนบุคคล พ.ศ. 2562** หน่วยงานกำกับคือ **สำนักงานคณะกรรมการคุ้มครองข้อมูลส่วนบุคคล (สคส.)**

คำถามที่ต้องตอบให้ได้ตั้งแต่ขั้นออกแบบ

- ข้อมูลที่อุปกรณ์เก็บ ระบุตัวบุคคลได้ไหม (ภาพใบหน้า เสียงพูด ตำแหน่งของคนคนหนึ่ง)
- เป็นข้อมูลอ่อนไหวไหม (มาตรา 26 เช่น ข้อมูลสุขภาพ ข้อมูลชีวภาพ)
- เก็บเท่าที่จำเป็นหรือเปล่า (เซนเซอร์ที่ไม่เก็บภาพ เช่นเรดาร์ หรือประมวลผลบนอุปกรณ์แล้วส่งเฉพาะผล ช่วยลดข้อมูลส่วนบุคคลที่ต้องดูแล — เหตุผลหนึ่งที่ edge สำคัญ)
- ใครเป็นผู้ควบคุมข้อมูล ใครเป็นผู้ประมวลผล
- เก็บนานเท่าไร ลบอย่างไร และแจ้งเจ้าของข้อมูลอย่างไร

---

## แนวคิด (3) — มาตรฐานและการรับรองก่อนวางขาย

| ถ้าผลิตภัณฑ์ของคุณ... | หน่วยงานที่ต้องตรวจ |
|---|---|
| ส่งหรือรับคลื่นวิทยุ (WiFi, Bluetooth, LoRa, มือถือ) | สำนักงาน กสทช. (nbtc.go.th) |
| เป็นเครื่องใช้ไฟฟ้า/อิเล็กทรอนิกส์ที่อยู่ในรายการ มอก. | สำนักงานมาตรฐานผลิตภัณฑ์อุตสาหกรรม (สมอ., tisi.go.th) |
| อ้างสรรพคุณทางการแพทย์ (วินิจฉัย/เฝ้าระวังโรค รวมซอฟต์แวร์/AI ที่เข้าข่ายเครื่องมือแพทย์) | กองควบคุมเครื่องมือแพทย์ อย. (medical.fda.moph.go.th) |

ถามห้องทดสอบตั้งแต่ขั้นต้นแบบว่าต้องทดสอบอะไรบ้าง ใช้เวลาเท่าไร และการเลือกใช้โมดูลวิทยุที่ผ่านการรับรองแล้วช่วยลดขอบเขตการทดสอบได้หรือไม่ ถ้าวางแผนส่งออก แต่ละประเทศมีข้อกำหนดของตัวเอง ต้องตรวจแยกกัน

---

## แนวคิด (4) — ห่วงโซ่อุปทาน

- **ชิ้นส่วนมีผู้ขายรายเดียว** หาชิ้นส่วนทดแทนไว้ตั้งแต่ออกแบบ (second source)
- **ชิ้นส่วนใกล้หยุดผลิต** ถามสถานะวงจรชีวิตของชิ้นส่วนหลัก เลือกรุ่นที่ผู้ผลิตยังสนับสนุนระยะยาว
- **ระยะเวลาสั่งซื้อนาน** วางแผนสต็อกชิ้นส่วนสำคัญ
- **ชิ้นส่วนปลอม** ซื้อจากผู้แทนจำหน่ายที่ได้รับแต่งตั้ง
- **การใส่กุญแจและเฟิร์มแวร์ในโรงงาน** ตกลงว่าใครถือกุญแจ และป้องกันการรั่วอย่างไร

---

## ฝึกเติม

ทำ **ทะเบียนความเสี่ยง** ของโครงการคุณอย่างน้อยสี่แถว แถวละหนึ่งกลุ่มความเสี่ยง

| กลุ่ม | ความเสี่ยง | โอกาส | ผลกระทบ | วิธีลดความเสี่ยง | ผู้รับผิดชอบ |
|---|---|---|---|---|---|
| ความปลอดภัยไซเบอร์ | | | | | |
| ข้อมูลส่วนบุคคล | | | | | |
| มาตรฐานและการรับรอง | | | | | |
| ห่วงโซ่อุปทาน | | | | | |

## เช็กความเข้าใจ

ตอบคำถามใน [quiz.yaml](quiz.yaml) ถูกตั้งแต่ 80% ขึ้นไปถือว่าผ่าน

---

## ไปต่อ / สะท้อนคิด

ทะเบียนความเสี่ยงที่ทำในบทนี้จะถูกนำไปใส่ใน decision canvas ในบทสุดท้าย บทถัดไปพูดเรื่องทำเอง ซื้อ หรือหาพันธมิตร ซึ่งเปลี่ยนว่าใครเป็นคนรับความเสี่ยงแต่ละข้อ

**สะท้อนคิด** ความเสี่ยงข้อไหนในทะเบียนของคุณที่ถ้าเกิดขึ้นแล้ว แก้ทีหลังไม่ได้เลย ข้อนั้นควรได้งบก่อน

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"Edge AI และ IoT สำหรับการตัดสินใจเชิงผลิตภัณฑ์" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0
