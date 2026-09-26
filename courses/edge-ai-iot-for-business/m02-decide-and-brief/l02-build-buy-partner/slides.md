---
marp: true
theme: default
paginate: true
lang: th
title: "บทเรียน 2.2 — ทำเอง ซื้อ หรือหาพันธมิตร"
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

# บทเรียน 2.2 — ทำเอง ซื้อ หรือหาพันธมิตร

## ชั่งน้ำหนักระหว่างทำเอง ซื้อของสำเร็จ หรือหาพันธมิตร ด้วยปัจจัยหกข้อ และรู้คำถามที่ต้องตกลงให้ชัดก่อนเซ็นสัญญา

**โมดูล 2 — ตัดสินใจและส่งโจทย์**

หลักสูตร **Edge AI และ IoT สำหรับการตัดสินใจเชิงผลิตภัณฑ์** · ไม่ต้องเขียนโค้ด ไม่ต้องมีบอร์ด

---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. อธิบายข้อดีและข้อเสียของการทำเอง ซื้อ และหาพันธมิตร
2. ให้คะแนนทางเลือกด้วยตารางถ่วงน้ำหนักหกปัจจัย แล้วเลือกทางเลือกพร้อมเหตุผล
3. ระบุเรื่องที่ต้องตกลงกับพันธมิตรหรือผู้รับจ้างก่อนเซ็นสัญญา

---

## ก่อนเริ่ม

จากบทที่แล้ว ความเสี่ยงข้อไหนในโครงการของคุณที่แก้ทีหลังไม่ได้ และทีมของคุณตอนนี้มีคนทำฮาร์ดแวร์ เฟิร์มแวร์ หรือ AI อยู่แล้วหรือยัง

---

## ดูของจริงก่อน

ร้านกาแฟสามร้านอยากรู้เมื่อเครื่องชงกาแฟเริ่มมีอาการผิดปกติ

- **ร้านแรก ซื้อ** อุปกรณ์เฝ้าเครื่องจักรสำเร็จรูปพร้อมบริการรายเดือน เริ่มใช้ได้เร็ว แต่ปรับอะไรไม่ได้ และข้อมูลอยู่ในระบบของผู้ขาย
- **ร้านที่สอง ทำเอง** จ้างวิศวกรมาพัฒนาทั้งระบบ ได้ตรงใจทุกอย่าง แต่ใช้เวลานาน และต้องมีคนดูแลต่อเองตลอด
- **ร้านที่สาม หาพันธมิตร** ใช้โมดูลวิทยุและแพลตฟอร์ม IoT ที่มีอยู่แล้ว แล้วจ้างบริษัทออกแบบทำส่วนที่เป็นความรู้เฉพาะของร้าน

ไม่มีร้านไหนผิด แต่ละร้านเลือกตามสิ่งที่ตัวเองให้ความสำคัญ

---

## แนวคิด (1) — สามทางเลือก และแบบผสม

| ทางเลือก | ข้อดี | ข้อเสีย |
|---|---|---|
| **ซื้อ** ของสำเร็จรูปหรือบริการ | เร็ว ความเสี่ยงทางเทคนิคต่ำ | ปรับแต่งได้น้อย ขึ้นกับผู้ขาย |
| **ทำเอง** | ตรงความต้องการ เป็นเจ้าของ IP และข้อมูลเต็มที่ | ช้าและแพงช่วงต้น ต้องมีทีมดูแลระยะยาว |
| **หาพันธมิตร** บริษัทออกแบบ/ผู้ผลิตรับจ้าง/สถาบันการศึกษา | ได้ความเชี่ยวชาญโดยไม่ต้องสร้างทีมเต็ม | ต้องจัดการสัญญา ความเป็นเจ้าของ และการส่งมอบให้ดี |

โครงการจริงจำนวนมากเป็น **แบบผสม** เช่น ซื้อโมดูลวิทยุที่รับรองแล้ว ใช้แพลตฟอร์ม IoT ที่มีอยู่ และทำเองเฉพาะส่วนที่เป็นจุดต่างของธุรกิจ

---

## แนวคิด (2) — หกปัจจัยที่ใช้ชั่งน้ำหนัก

1. **เป็นจุดต่างทางธุรกิจไหม** ถ้าใช่ ควรเป็นเจ้าของเอง ถ้าไม่ใช่ ซื้อได้
2. **ต้องเสร็จเร็วแค่ไหน**
3. **ทีมมีความสามารถอยู่แล้วหรือยัง**
4. **จำนวนที่จะผลิตและใช้งาน** ยิ่งมาก การลงทุนทำเองยิ่งคุ้ม (เฉลี่ย NRE ได้มากขึ้น)
5. **ใครเป็นเจ้าของทรัพย์สินทางปัญญาและข้อมูล**
6. **ใครดูแลระยะยาว** รวมถึงอัปเดตความปลอดภัยตลอดอายุผลิตภัณฑ์

---

## แนวคิด (3) — เรื่องที่ต้องตกลงก่อนเซ็นสัญญา

- **ความเป็นเจ้าของ** ใครเป็นเจ้าของแบบวงจร ซอร์สโค้ด โมเดล และข้อมูลที่เก็บมา
- **การส่งมอบ** ได้ซอร์สโค้ด ไฟล์ออกแบบ และเอกสารครบพอให้ทีมอื่นดูแลต่อได้หรือไม่
- **กุญแจและการลงนาม** ใครถือกุญแจที่ใช้ลงนามเฟิร์มแวร์และกุญแจเข้ารหัสของอุปกรณ์
- **การอัปเดตและความปลอดภัย** ใครออกอัปเดต นานกี่ปี ค่าใช้จ่ายเท่าไร
- **การรับรองมาตรฐาน** ใครรับผิดชอบยื่นทดสอบและแก้ไขถ้าไม่ผ่าน
- **การรับประกันและการสิ้นสุดสัญญา** ถ้าพันธมิตรเลิกกิจการ ผลิตภัณฑ์ของคุณยังเดินต่อได้ไหม

TESA มีเครือข่ายบริษัทสมาชิก สถาบันการศึกษา และหลักสูตรอบรมที่ช่วยให้ทีมของคุณเติบโตได้ ถ้าเลือกทำเองหรือทำร่วม ทีมพัฒนาเรียนต่อได้จากหลักสูตรในเส้นทางนักพัฒนาของ TESA Open Knowledge

---

## ฝึกเติม

ให้คะแนนสามทางเลือกสำหรับโครงการของคุณ ใส่น้ำหนักตามความสำคัญ (รวม 100) และให้คะแนนแต่ละช่อง 1–5 คะแนนรวม = น้ำหนัก × คะแนน

| ปัจจัย | น้ำหนัก | ซื้อ | ทำเอง | พันธมิตร |
|---|---|---|---|---|
| เป็นจุดต่างทางธุรกิจ | | | | |
| ความเร็ว | | | | |
| ความสามารถของทีม | | | | |
| จำนวนผลิต | | | | |
| ความเป็นเจ้าของ | | | | |
| การดูแลระยะยาว | | | | |
| **รวม** | 100 | | | |

ถ้าผลที่ได้ขัดกับความรู้สึก ให้กลับไปดูว่าน้ำหนักตรงกับที่คิดจริงไหม

---

## เช็กความเข้าใจ / ไปต่อ / สะท้อนคิด

ตอบคำถามใน [quiz.yaml](quiz.yaml) ถูกตั้งแต่ 80% ขึ้นไปถือว่าผ่าน

**ไปต่อ** บทสุดท้ายรวมทุกอย่างที่ทำมา ทั้งโจทย์ สถาปัตยกรรม ต้นทุน ความเสี่ยง และทางเลือกนี้ เป็น decision canvas หนึ่งหน้า

**สะท้อนคิด** ถ้าพันธมิตรที่คุณเลือกหายไปพรุ่งนี้ อะไรในผลิตภัณฑ์ของคุณที่ยังอยู่ในมือคุณ

---

<!-- _class: cover -->
<!-- _backgroundColor: #0d1117 -->

## แหล่งที่มา

"Edge AI และ IoT สำหรับการตัดสินใจเชิงผลิตภัณฑ์" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย
(Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY-NC 4.0
