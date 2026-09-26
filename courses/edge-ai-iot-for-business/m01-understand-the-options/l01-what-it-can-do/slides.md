---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 1.1 — Edge AI และ IoT ทำอะไรได้ และทำอะไรไม่ได้"
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

# บทเรียน 1.1 — Edge AI และ IoT ทำอะไรได้ และทำอะไรไม่ได้

## แยกโจทย์ธุรกิจที่ IoT และ Edge AI ช่วยได้จริง ออกจากโจทย์ที่ไม่ควรใช้ ผ่านกรณีตัวอย่างจากโรงงาน ฟาร์ม สุขภาพ และค้าปลีก

**โมดูล 1 — เข้าใจทางเลือก**

หลักสูตร **Edge AI และ IoT สำหรับการตัดสินใจเชิงผลิตภัณฑ์** · ไม่ต้องเขียนโค้ด ไม่ต้องมีบอร์ด

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. จำแนกได้ว่าโจทย์ไหนเหมาะกับ IoT อย่างเดียว IoT ร่วมกับ Edge AI หรือไม่ควรใช้ทั้งคู่
2. อธิบายข้อจำกัดหลักของ Edge AI ได้อย่างน้อย 3 ข้อ
3. เขียนโจทย์ธุรกิจของตัวเองเป็นประโยคเดียวที่ทีมเทคนิคเอาไปทำงานต่อได้

## ก่อนเริ่ม

ลองนึกถึงปัญหาหนึ่งเรื่องในกิจการของคุณที่ "อยากรู้ก่อนที่จะสายเกินไป" เช่น เครื่องจักรกำลังจะเสีย ของในตู้แช่กำลังจะเสีย หรือลูกค้ากำลังรอคิวนานเกินไป จดไว้หนึ่งบรรทัด เราจะกลับมาใช้ตอนท้ายบท

---

## ดูของจริงก่อน — สี่กรณีตัวอย่าง

อ่านตารางนี้แล้วลองเดาก่อนว่าแถวไหน "ต้องมี AI" จริง ๆ

| อุตสาหกรรม | สิ่งที่วัด | สิ่งที่ตัดสินใจ | ต้องมี AI ไหม |
|---|---|---|---|
| โรงงาน | การสั่นสะเทือนของมอเตอร์ | รูปแบบการสั่นผิดไปจากปกติ แจ้งช่างก่อนเสีย | มักต้อง — "ผิดปกติ" ไม่ใช่ตัวเลขตัวเดียว |
| ฟาร์ม | อุณหภูมิ ความชื้นอากาศ/ดิน | ความชื้นต่ำกว่าเกณฑ์ สั่งพ่นหมอกหรือรดน้ำ | มักไม่ต้อง — กฎเกณฑ์ธรรมดาก็พอ |
| สุขภาพ | การเคลื่อนไหวด้วยเรดาร์ (ไม่ใช้กล้อง) | เพิ่งมีการล้มและไม่ลุกขึ้น แจ้งญาติ | มักต้อง — การล้มกับการนั่งเร็วคล้ายกัน |
| ค้าปลีก | อุณหภูมิในตู้แช่ | อุ่นเกินเกณฑ์นานเกิน 15 นาที แจ้งผู้จัดการ | ไม่ต้อง — กฎเกณฑ์ธรรมดาก็พอ |

**สองในสี่แถวไม่ต้องใช้ AI เลย** — โจทย์ส่วนใหญ่ต้องการการวัดที่ดีกับกฎที่ชัด ก่อนจะต้องการ AI

---

## แนวคิด (1) — สองคำที่มักถูกใช้ปนกัน

- **IoT (Internet of Things)** คืออุปกรณ์ที่มีเซนเซอร์ วัดค่าได้เอง และส่งข้อมูลผ่านเครือข่าย ทำให้เรารู้สิ่งที่เกิดขึ้นโดยไม่ต้องมีคนไปยืนดู
- **Edge AI** คือการรันโมเดล AI ที่ฝึกมาแล้ว **บนตัวอุปกรณ์เอง** ใกล้เซนเซอร์ แทนที่จะส่งข้อมูลดิบทั้งหมดขึ้นคลาวด์ไปให้คอมพิวเตอร์ที่อื่นคิด

ชิปรุ่นใหม่สำหรับงานนี้เล็กลงและเก่งขึ้นมาก ตัวอย่างเช่นบอร์ด TESAIoT Dev Kit ที่ใช้ในหลักสูตรของ TESA ใช้ชิป Infineon PSoC™ Edge E84 ซึ่งมี Arm® Cortex®-M55 ร่วมกับหน่วยเร่ง AI (NPU) Ethos™-U55 และมีเซนเซอร์ความเคลื่อนไหว เรดาร์ 60 GHz ไมโครโฟน และเซนเซอร์สภาพแวดล้อมอยู่บนบอร์ด — ไม่ได้ยกตัวอย่างนี้เพื่อให้ซื้อบอร์ดรุ่นนี้ แต่เพื่อให้เห็นว่า "AI บนอุปกรณ์ตัวเล็ก" เป็นของที่มีอยู่จริงแล้ว

---

## แนวคิด (2) — บันไดสามขั้นก่อนพูดถึง AI

ถามตามลำดับนี้ ถ้าตอบได้ที่ขั้นไหน หยุดที่ขั้นนั้น

1. **วัดได้ไหม** ปัญหานี้มีสัญญาณอะไรที่เซนเซอร์จับได้ ถ้าไม่มีสัญญาณ ไม่มีเทคโนโลยีไหนช่วยได้
2. **กฎธรรมดาพอไหม** ถ้าตัดสินใจได้ด้วย "ค่าเกินเกณฑ์" หรือ "เกินเกณฑ์นานกว่า X นาที" ใช้ IoT กับกฎก็พอ ถูกกว่าและอธิบายง่ายกว่า
3. **ต้องจำรูปแบบไหม** ถ้า "ผิดปกติ" ไม่ใช่ตัวเลขตัวเดียว แต่เป็นรูปแบบของสัญญาณ เช่น เสียง การสั่น หรือท่าทาง นั่นคือที่ที่ Edge AI คุ้มค่า

---

## แนวคิด (3) — สิ่งที่ Edge AI ทำไม่ได้ หรือทำได้ไม่ดี

- **ไม่ถูกร้อยเปอร์เซ็นต์** โมเดลทุกตัวมีทั้งเตือนผิด (false alarm) และพลาดเหตุการณ์จริง ต้องออกแบบว่าผิดแล้วใครรับผิดชอบ และต้นทุนของการผิดแต่ละแบบเป็นเท่าไร
- **ไม่มีข้อมูล ไม่มีโมเดล** โมเดลเรียนจากตัวอย่าง ต้องมีข้อมูลจากหน้างานจริงทั้งตอนปกติและผิดปกติ การเก็บข้อมูลมักเป็นงานที่นานที่สุดของโครงการ
- **ไม่ใช่ติดตั้งแล้วจบ** สภาพหน้างานเปลี่ยน เครื่องจักรเปลี่ยน ฤดูเปลี่ยน โมเดลที่แม่นวันนี้อาจแม่นน้อยลงในปีหน้า ต้องมีแผนดูแลและอัปเดต
- **ไม่แทนการแก้กระบวนการ** ถ้าเตือนแล้วไม่มีใครรู้ว่าต้องทำอะไรต่อ ระบบที่แม่นแค่ไหนก็ไม่มีประโยชน์

---

## แนวคิด (4) — โจทย์ที่ดีมีสามส่วน

ประโยคโจทย์ที่ทีมเทคนิคเอาไปทำงานต่อได้ ต้องตอบครบสามส่วน **วัดอะไร** · **ตัดสินใจอะไร** · **ใครทำอะไรต่อ**

> วัดอุณหภูมิในตู้แช่ทุกตู้ ถ้าอุ่นเกินเกณฑ์นานกว่า 15 นาที ให้ส่งข้อความหาผู้จัดการกะ เพื่อไปตรวจประตูตู้ภายใน 30 นาที

ประโยคนี้ไม่มีคำว่า AI เลย และนั่นไม่ใช่ข้อเสีย

---

## ฝึกเติม

กลับไปที่ปัญหาที่คุณจดไว้ตอนต้นบท เขียนใหม่ให้ครบสามส่วน แล้วเดินบันไดสามขั้น บอกว่าโจทย์ของคุณหยุดที่ขั้นไหน

| ส่วน | โจทย์ของคุณ |
|---|---|
| วัดอะไร | |
| ตัดสินใจอะไร | |
| ใครทำอะไรต่อ | |
| หยุดที่ขั้น (1 วัดได้ไหม / 2 กฎพอไหม / 3 ต้องจำรูปแบบ) | |

## เช็กความเข้าใจ

ตอบคำถามใน [quiz.yaml](quiz.yaml) ถูกตั้งแต่ 80% ขึ้นไปถือว่าผ่าน

---

## ไปต่อ / สะท้อนคิด

ถ้าอยากเห็นกับตาว่าอุปกรณ์ตัวเล็ก "วัดแล้วตัดสินใจ" อย่างไร ลองหลักสูตร Explorer บทเรียนเรื่องอ่านเซนเซอร์ ใช้เวลาราวครึ่งชั่วโมงในเบราว์เซอร์ ไม่ต้องมีบอร์ด

**สะท้อนคิด** ถ้าระบบของคุณเตือนผิดสัปดาห์ละครั้ง พนักงานจะยังเชื่อมันไหม แล้วถ้าพลาดเหตุการณ์จริงเดือนละครั้ง ความเสียหายเป็นอย่างไร คำตอบของสองคำถามนี้บอกได้ว่าคุณต้องการความแม่นแค่ไหน

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"Edge AI และ IoT สำหรับการตัดสินใจเชิงผลิตภัณฑ์" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0
