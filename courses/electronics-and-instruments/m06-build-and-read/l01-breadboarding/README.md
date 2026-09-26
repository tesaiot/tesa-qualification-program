---
id: elec.m06.l01
lang: th
title: {th: ต่อวงจรบนเบรดบอร์ด, en: Breadboarding}
summary: {th: รู้ว่ารูบนเบรดบอร์ดเชื่อมกันอย่างไร และต่อวงจรตามแผนผังให้ตรวจง่าย, en: Know how breadboard holes connect and build circuits from a schematic that are easy to check.}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m05.l02]
objectives:
- {th: ระบุแถวและรางไฟที่เชื่อมกันบนเบรดบอร์ดได้ถูกต้อง, en: Identify which rows and rails are connected on a breadboard.}
- {th: ต่อวงจรตามแผนผังโดยใช้สีสายตามแบบแผน และตรวจด้วยมัลติมิเตอร์ก่อนจ่ายไฟ, en: Build from a schematic with conventional wire colours and check with a multimeter before powering.}
develops:
- {skill: hwdev.breadboard, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: alpha
translation: pending
---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ระบุแถวและรางไฟที่เชื่อมกันบนเบรดบอร์ดได้ถูกต้อง
2. ต่อวงจรตามแผนผังโดยใช้สีสายตามแบบแผน และตรวจด้วยมัลติมิเตอร์ก่อนจ่ายไฟ

## ก่อนเริ่ม

- ใช้โหมดความต่อเนื่องและโหมดไดโอดของมัลติมิเตอร์ได้ (บทเรียน [วัดแรงดันและความต่อเนื่อง](../../m03-multimeter/l01-voltage-and-continuity/README.md))
- สำหรับแล็บ: เบรดบอร์ด สายจัมเปอร์หลายสี (แดง ดำ และสีอื่นอย่างน้อยสองสี) LED สีแดงสามดวง ตัวต้านทาน 1 kΩ สี่ตัว 10 kΩ หนึ่งตัว ปุ่มกดหนึ่งตัว
  และ TESAIoT Dev Kit ที่ flash ตัวอย่าง [QWA309 Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) ไว้
- ถ้าใช้ Eva Kit ต่อวงจรเดียวกันเข้าขาว่างของบอร์ด แล้วเขียนโปรแกรมสั้น ๆ กะพริบ LED และอ่านปุ่มเอง

## ดูของจริงก่อน

พลิกเบรดบอร์ดดูด้านหลัง ถ้าลอกแผ่นกาวได้โดยไม่เสียหาย (หรือดูภาพจากผู้ผลิต) จะเห็นแถบโลหะเรียงอยู่ใต้รู
แถบสั้นจำนวนมากอยู่ตรงกลาง และแถบยาวสองสามเส้นอยู่ริมบนและริมล่าง

ก่อนอ่านต่อ ลองทายว่ารูคู่ไหนต่อถึงกัน แล้วพิสูจน์ด้วยโหมดความต่อเนื่องของมัลติมิเตอร์ (เสียบสายจัมเปอร์สั้น ๆ สองเส้นลงในรูที่อยากทดสอบ แล้วแตะสายวัดที่ปลายสายจัมเปอร์)
ถ้าคุณทายผิดสักคู่ ดีมาก เพราะนั่นคือความผิดพลาดที่คุณจะไม่ทำตอนต่อวงจรจริง

## แนวคิด

### 1. ข้างในเบรดบอร์ด

<figure>
<svg viewBox="0 0 420 250" width="420" role="img" aria-label="ผังการเชื่อมต่อภายในเบรดบอร์ด รางไฟตามยาวและแถวละห้ารู" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<text x="20" y="22" font-weight="bold" fill="currentColor" stroke="none">+</text>
<text x="20" y="38" font-weight="bold" fill="currentColor" stroke="none">−</text>
<path d="M60 18H252" stroke-width="3"/>
<path d="M60 34H252" stroke-width="3" stroke-dasharray="4 3"/>
<text x="40" y="60" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">a</text>
<circle cx="68" cy="56" r="2"/>
<circle cx="84" cy="56" r="2"/>
<circle cx="100" cy="56" r="2"/>
<circle cx="116" cy="56" r="2"/>
<circle cx="132" cy="56" r="2"/>
<circle cx="148" cy="56" r="2"/>
<circle cx="164" cy="56" r="2"/>
<circle cx="180" cy="56" r="2"/>
<circle cx="196" cy="56" r="2"/>
<circle cx="212" cy="56" r="2"/>
<circle cx="228" cy="56" r="2"/>
<circle cx="244" cy="56" r="2"/>
<text x="40" y="76" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">b</text>
<circle cx="68" cy="72" r="2"/>
<circle cx="84" cy="72" r="2"/>
<circle cx="100" cy="72" r="2"/>
<circle cx="116" cy="72" r="2"/>
<circle cx="132" cy="72" r="2"/>
<circle cx="148" cy="72" r="2"/>
<circle cx="164" cy="72" r="2"/>
<circle cx="180" cy="72" r="2"/>
<circle cx="196" cy="72" r="2"/>
<circle cx="212" cy="72" r="2"/>
<circle cx="228" cy="72" r="2"/>
<circle cx="244" cy="72" r="2"/>
<text x="40" y="92" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">c</text>
<circle cx="68" cy="88" r="2"/>
<circle cx="84" cy="88" r="2"/>
<circle cx="100" cy="88" r="2"/>
<circle cx="116" cy="88" r="2"/>
<circle cx="132" cy="88" r="2"/>
<circle cx="148" cy="88" r="2"/>
<circle cx="164" cy="88" r="2"/>
<circle cx="180" cy="88" r="2"/>
<circle cx="196" cy="88" r="2"/>
<circle cx="212" cy="88" r="2"/>
<circle cx="228" cy="88" r="2"/>
<circle cx="244" cy="88" r="2"/>
<text x="40" y="108" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">d</text>
<circle cx="68" cy="104" r="2"/>
<circle cx="84" cy="104" r="2"/>
<circle cx="100" cy="104" r="2"/>
<circle cx="116" cy="104" r="2"/>
<circle cx="132" cy="104" r="2"/>
<circle cx="148" cy="104" r="2"/>
<circle cx="164" cy="104" r="2"/>
<circle cx="180" cy="104" r="2"/>
<circle cx="196" cy="104" r="2"/>
<circle cx="212" cy="104" r="2"/>
<circle cx="228" cy="104" r="2"/>
<circle cx="244" cy="104" r="2"/>
<text x="40" y="124" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">e</text>
<circle cx="68" cy="120" r="2"/>
<circle cx="84" cy="120" r="2"/>
<circle cx="100" cy="120" r="2"/>
<circle cx="116" cy="120" r="2"/>
<circle cx="132" cy="120" r="2"/>
<circle cx="148" cy="120" r="2"/>
<circle cx="164" cy="120" r="2"/>
<circle cx="180" cy="120" r="2"/>
<circle cx="196" cy="120" r="2"/>
<circle cx="212" cy="120" r="2"/>
<circle cx="228" cy="120" r="2"/>
<circle cx="244" cy="120" r="2"/>
<path d="M68 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M84 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M100 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M116 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M132 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M148 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M164 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M180 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M196 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M212 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M228 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M244 56V120" stroke-width="2.5" stroke-opacity="0.45"/>
<text x="40" y="164" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">f</text>
<circle cx="68" cy="160" r="2"/>
<circle cx="84" cy="160" r="2"/>
<circle cx="100" cy="160" r="2"/>
<circle cx="116" cy="160" r="2"/>
<circle cx="132" cy="160" r="2"/>
<circle cx="148" cy="160" r="2"/>
<circle cx="164" cy="160" r="2"/>
<circle cx="180" cy="160" r="2"/>
<circle cx="196" cy="160" r="2"/>
<circle cx="212" cy="160" r="2"/>
<circle cx="228" cy="160" r="2"/>
<circle cx="244" cy="160" r="2"/>
<text x="40" y="180" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">g</text>
<circle cx="68" cy="176" r="2"/>
<circle cx="84" cy="176" r="2"/>
<circle cx="100" cy="176" r="2"/>
<circle cx="116" cy="176" r="2"/>
<circle cx="132" cy="176" r="2"/>
<circle cx="148" cy="176" r="2"/>
<circle cx="164" cy="176" r="2"/>
<circle cx="180" cy="176" r="2"/>
<circle cx="196" cy="176" r="2"/>
<circle cx="212" cy="176" r="2"/>
<circle cx="228" cy="176" r="2"/>
<circle cx="244" cy="176" r="2"/>
<text x="40" y="196" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">h</text>
<circle cx="68" cy="192" r="2"/>
<circle cx="84" cy="192" r="2"/>
<circle cx="100" cy="192" r="2"/>
<circle cx="116" cy="192" r="2"/>
<circle cx="132" cy="192" r="2"/>
<circle cx="148" cy="192" r="2"/>
<circle cx="164" cy="192" r="2"/>
<circle cx="180" cy="192" r="2"/>
<circle cx="196" cy="192" r="2"/>
<circle cx="212" cy="192" r="2"/>
<circle cx="228" cy="192" r="2"/>
<circle cx="244" cy="192" r="2"/>
<text x="40" y="212" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">i</text>
<circle cx="68" cy="208" r="2"/>
<circle cx="84" cy="208" r="2"/>
<circle cx="100" cy="208" r="2"/>
<circle cx="116" cy="208" r="2"/>
<circle cx="132" cy="208" r="2"/>
<circle cx="148" cy="208" r="2"/>
<circle cx="164" cy="208" r="2"/>
<circle cx="180" cy="208" r="2"/>
<circle cx="196" cy="208" r="2"/>
<circle cx="212" cy="208" r="2"/>
<circle cx="228" cy="208" r="2"/>
<circle cx="244" cy="208" r="2"/>
<text x="40" y="228" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">j</text>
<circle cx="68" cy="224" r="2"/>
<circle cx="84" cy="224" r="2"/>
<circle cx="100" cy="224" r="2"/>
<circle cx="116" cy="224" r="2"/>
<circle cx="132" cy="224" r="2"/>
<circle cx="148" cy="224" r="2"/>
<circle cx="164" cy="224" r="2"/>
<circle cx="180" cy="224" r="2"/>
<circle cx="196" cy="224" r="2"/>
<circle cx="212" cy="224" r="2"/>
<circle cx="228" cy="224" r="2"/>
<circle cx="244" cy="224" r="2"/>
<path d="M68 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M84 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M100 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M116 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M132 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M148 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M164 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M180 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M196 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M212 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M228 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M244 160V224" stroke-width="2.5" stroke-opacity="0.45"/>
<path d="M60 140H252" stroke-dasharray="4 3"/>
<text x="260" y="144" fill="currentColor" stroke="none">centre channel</text>
<text x="68" y="48" text-anchor="middle" font-size="10" fill="currentColor" stroke="none">1</text>
<text x="116" y="48" text-anchor="middle" font-size="10" fill="currentColor" stroke="none">4</text>
<text x="164" y="48" text-anchor="middle" font-size="10" fill="currentColor" stroke="none">7</text>
<text x="212" y="48" text-anchor="middle" font-size="10" fill="currentColor" stroke="none">10</text>
<text x="260" y="26" fill="currentColor" stroke="none">power rails (long)</text>
<text x="260" y="84" fill="currentColor" stroke="none">5 holes in a column</text>
<text x="260" y="100" fill="currentColor" stroke="none">= one node</text>
</svg>
<figcaption>เส้นหนาจาง ๆ คือแผ่นโลหะใต้รู: ห้ารู a ถึง e ของคอลัมน์เดียวกันต่อกันเป็นจุดเดียว f ถึง j อีกจุดหนึ่ง ร่องกลางแยกสองฝั่งออกจากกัน รางไฟด้านบนต่อกันตามยาว (บางรุ่นขาดครึ่งกลาง)</figcaption>
</figure>

- **กลุ่มห้ารู** ตรงกลางเบรดบอร์ด รูห้ารูที่อยู่แนวเดียวกัน (a ถึง e) ต่อกันเป็นจุดเดียว (node เดียว) f ถึง j เป็นอีกจุดหนึ่ง
  ป้ายชื่อบนเบรดบอร์ดแต่ละยี่ห้อเรียก "แถว" หรือ "คอลัมน์" ต่างกัน ให้จำจากหลัก "ห้ารูในแนวเดียวกันที่ไม่ข้ามร่องกลาง" แทนชื่อ
- **ร่องกลาง (centre channel)** แยกสองฝั่งออกจากกัน ความกว้างพอดีกับชิปแบบสองแถวขา (DIP) ให้ขาแต่ละขาอยู่คนละจุด
- **รางไฟ (power rails)** แถบยาวริมขอบ มักมีเส้นสีแดง (+) และน้ำเงิน (−) กำกับ ใช้กระจายไฟเลี้ยงและกราวด์
  **เบรดบอร์ดยาวบางรุ่นรางไฟขาดครึ่งกลาง** ต้องตรวจด้วยโหมดความต่อเนื่องก่อนใช้ทุกแผ่น
- ระยะห่างระหว่างรู 2.54 mm (0.1 นิ้ว) เท่ากับขาของ header ทั่วไป

**ความผิดพลาดคลาสสิก** เสียบตัวต้านทานโดยขาทั้งสองอยู่ในกลุ่มห้ารูเดียวกัน ตัวต้านทานถูกลัดทิ้ง วงจรทำงานเหมือนไม่มีมัน
LED ที่เสียบแบบนี้ก็จะไม่ติดเลย เพราะไม่มีแรงดันคร่อม

### 2. สีสายและการจัดวาง

สีสายไม่มีผลทางไฟฟ้า แต่มีผลมากกับการตรวจ แบบแผนที่ใช้กันทั่วไป

| สี | ใช้กับ |
|---|---|
| แดง | ไฟเลี้ยงบวก (ถ้ามีหลายแรงดัน ให้แยกสี เช่น แดง = 5 V ส้ม = 3.3 V และเขียนป้ายกำกับไว้) |
| ดำ (หรือน้ำเงิน) | กราวด์ |
| สีอื่น | สัญญาณ แยกสีตามหน้าที่ เช่น เหลือง = ขาออกไป LED เขียว = ขาเข้าจากปุ่ม |

**หลักการจัดวางที่ทำให้ตรวจง่าย**

- ต่อตามแผนผังทีละส่วน (ทีละ net) ต่อเสร็จหนึ่ง net ขีดเส้นทับบนแผนผังที่พิมพ์ไว้หนึ่งเส้น
- สายสั้น แนบกับเบรดบอร์ด ไม่โค้งข้ามชิ้นส่วน ขาชิ้นส่วนตัดให้สั้นพอดี
- วางชิ้นส่วนตามทิศทางของแผนผัง (ไฟเข้าด้านบน กราวด์ด้านล่าง สัญญาณไหลจากซ้ายไปขวา) คนตรวจจะเทียบภาพได้เร็ว
- ถ้ามีชิป ใส่ตัวเก็บประจุ 100 nF คร่อมรางไฟชิดขาไฟของชิปแต่ละตัว (เหตุผลอยู่ในบทเรียน [ชิ้นส่วนพื้นฐาน](../../m01-circuits/l03-components/README.md))

**ข้อจำกัดของเบรดบอร์ด** แถบโลหะที่วางขนานกันมีความจุระหว่างกันราวไม่กี่ pF และหน้าสัมผัสมีความต้านทานกับความเหนี่ยวนำ
ผลคือเบรดบอร์ดไม่เหมาะกับสัญญาณเร็วระดับหลาย MHz จุดที่มีความต้านทานสูง และกระแสสูง

```text
ความจุแฝง 5 pF กับแหล่งสัญญาณความต้านทาน 100 kΩ
f_c = 1 / (2π × R × C) = 1 / (2π × 100 kΩ × 5 pF) ≈ 318 kHz
```

สัญญาณที่เร็วกว่าราวนี้จะถูกกรองจนขอบมน ถ้าความต้านทานเป็น 1 MΩ ความถี่นี้ลดลงเหลือราว 32 kHz
หน้าสัมผัสที่ใช้มานานจะหลวม เป็นต้นเหตุของวงจร "ทำงานบ้างไม่ทำงานบ้าง" ที่หาสาเหตุยาก

### 3. ตรวจก่อนจ่ายไฟ

ตรวจตามลำดับนี้ทุกครั้ง **ขณะที่เบรดบอร์ดยังไม่ต่อกับบอร์ดหรือแหล่งจ่าย**

1. **ตรวจด้วยตา** ไล่ทีละ net เทียบกับแผนผัง ขั้วของ LED และตัวเก็บประจุมีขั้ว ไม่มีขาชิ้นส่วนสองขาอยู่ในกลุ่มเดียวกันโดยไม่ตั้งใจ
2. **รางไฟกับกราวด์ต้องไม่ต่อกัน** โหมดความต่อเนื่องระหว่างราง + กับราง − ต้อง **ไม่ดัง**
3. **ความต้านทานระหว่างรางต้องสมเหตุสมผล** คำนวณไว้ก่อนว่าวงจรควรมีความต้านทานเท่าไรระหว่างราง แล้ววัดเทียบ
4. **ทดสอบ LED ด้วยโหมดไดโอด** แตะสายแดงที่ขาแอโนดและสายดำที่แคโทด ควรอ่านได้ราวแรงดัน V_f และบางดวงจะติดสลัว ๆ
5. **ต่อไฟตามลำดับ** GND ก่อน แล้วไฟเลี้ยง แล้วสายสัญญาณ ถ้ามีแหล่งจ่ายที่จำกัดกระแสได้ ตั้งขีดจำกัดต่ำไว้ก่อน (เช่น 50 mA) ถ้าผิดจะได้ไม่มีอะไรไหม้

## ตัวอย่างสมบูรณ์

**โจทย์** ต่อ LED สามดวงเข้าขา P13.3, P13.4, P13.5 และปุ่มแบบ active-low เข้าขา P13.0 ของ TESAIoT Dev Kit
แล้วใช้ปุ่ม GPIO Out และ GPIO In ของโปรแกรมทดสอบ header ทดสอบ

**แผนผัง (เขียนเป็นรายการ net)**

| net | ต่อกับ |
|---|---|
| GND | ขา GND ของ header, ราง − , แคโทดของ LED1 ถึง LED3, ขาหนึ่งของปุ่ม |
| 3V3 | ขา 3V3 ของ header, ราง + , ปลายหนึ่งของ R_pu 10 kΩ |
| LED1 | P13.3 → 1 kΩ → แอโนดของ LED1 (เช่นเดียวกัน LED2 ที่ P13.4 และ LED3 ที่ P13.5) |
| BTN_N | ปลายอีกข้างของ R_pu, ขาอีกข้างของปุ่ม, และ 1 kΩ ไปยัง P13.0 |

**รายการสาย**

| จาก | ไป | สี |
|---|---|---|
| GND ของ header | ราง − | ดำ |
| 3V3 ของ header | ราง + | แดง |
| P13.3, P13.4, P13.5 | ตัวต้านทาน 1 kΩ ของแต่ละดวง | เหลือง |
| P13.0 | ตัวต้านทาน 1 kΩ ที่ต่อกับ BTN_N | เขียว |

**คำนวณก่อนต่อ**

```text
กระแส LED แต่ละดวงเมื่อขาเป็น 1 (V_f ≈ 1.8 ถึง 2.0 V): (3.3 − 2.0) / 1 kΩ ≈ 1.3 mA ถึง (3.3 − 1.8) / 1 kΩ = 1.5 mA
ความต้านทานระหว่างราง + กับราง − ตอนไม่ต่อกับบอร์ด:
  ปล่อยปุ่ม → ไม่มีทางเดินกระแส อ่านได้ OL (เปิดวงจร)
  กดปุ่ม    → ผ่าน R_pu ลงกราวด์ อ่านได้ 10 kΩ
```

**ตรวจ** ราง + กับ − ไม่ดัง อ่านได้ OL และได้ 10 kΩ เมื่อกดปุ่ม LED ทุกดวงผ่านโหมดไดโอด แล้วจึงต่อเข้ากับบอร์ดตามลำดับ GND, 3V3, สายสัญญาณ

**ทดสอบ** กด GPIO Out ไฟสามดวงควรติดไล่กันตามลำดับขาทุกราว 0.7 s กด GPIO In แล้วกดปุ่ม บิต 0 ของ mask ต้องเปลี่ยนตามปุ่ม
ตัวต้านทาน 1 kΩ ระหว่าง BTN_N กับ P13.0 ป้องกันขาไว้ ระหว่างที่ GPIO Out ขับ P13.0 เป็นขาออก ถ้ามีคนกดปุ่ม กระแสจะไม่เกิน 3.3 mA

## ฝึกเติม

1. บนเบรดบอร์ดในภาพ รู a12 กับ e12 ต่อกันไหม e12 กับ f12 ล่ะ a12 กับ a13 ล่ะ
2. เสียบตัวต้านทานขาหนึ่งที่ b15 อีกขาที่ d15 จะเกิดอะไรขึ้น
3. ความจุแฝง 5 pF กับแหล่งสัญญาณ 10 kΩ ความถี่ที่เริ่มถูกกรองคือเท่าไร
4. บนเบรดบอร์ดมีทั้งไฟ 5 V และ 3.3 V ควรจัดสีสายและป้ายอย่างไร
5. ก่อนเสียบไฟ วัดความต้านทานระหว่างราง + กับราง − ได้ 0.4 Ω ควรทำอะไรต่อ
6. ในตัวอย่างสมบูรณ์ ถ้าลืมใส่ R_pu 10 kΩ ความต้านทานระหว่างรางเมื่อกดปุ่มจะอ่านได้เท่าไร และปุ่มจะทำงานในโหมด GPIO In ได้ไหม

## เฉลย

1. a12 กับ e12 ต่อกัน (กลุ่มห้ารูเดียวกัน) e12 กับ f12 ไม่ต่อ (ร่องกลางคั่น) a12 กับ a13 ไม่ต่อ (คนละกลุ่ม)
2. ขาทั้งสองอยู่ในกลุ่มเดียวกัน ตัวต้านทานถูกลัดทิ้ง ไม่มีผลกับวงจร
3. f_c = 1 / (2π × 10 kΩ × 5 pF) ≈ 3.18 MHz
4. ใช้สีต่างกันสำหรับแต่ละแรงดัน เช่น แดง = 5 V ส้ม = 3.3 V แยกรางคนละฝั่ง และเขียนป้ายกำกับที่รางด้วย อย่าให้คนอื่นต้องเดา
5. ห้ามเสียบไฟ ค่าใกล้ 0 Ω คือการลัดวงจร หาสายหรือขาชิ้นส่วนที่ต่อราง + กับ − ถึงกัน โดยถอดชิ้นส่วนทีละชิ้นแล้ววัดซ้ำ
6. อ่านได้ OL ทั้งตอนกดและปล่อย เพราะไม่มีทางจากราง + ลงกราวด์ ปุ่มยังดึงขาลงเป็น 0 ได้ตอนกด แต่ตอนปล่อยขาจะลอย (GPIO In ตั้งขาแบบไม่มี pull) ค่าจึงเชื่อถือไม่ได้

## เช็กความเข้าใจ

ตอบคำถามใน [quiz.yaml](quiz.yaml) ให้ถูกอย่างน้อย 4 ใน 5 ข้อ

## แล็บ

1. **สำรวจเบรดบอร์ดของคุณ** ใช้โหมดความต่อเนื่องตรวจว่ารางไฟต่อตลอดแนวหรือขาดครึ่งกลาง และสุ่มตรวจกลุ่มห้ารูสองสามกลุ่ม จดผล
2. **วาดแผนผัง** ของตัวอย่างสมบูรณ์ลงกระดาษด้วยสัญลักษณ์ (ดูสัญลักษณ์ในบทเรียน [อ่านแผนผังวงจร](../l03-reading-schematics/README.md) ถ้ายังไม่คุ้น) พิมพ์หรือถ่ายรูปเก็บไว้ข้างตัว
3. **ต่อทีละ net** ตามรายการสาย ขีดทับ net บนแผนผังทุกครั้งที่ต่อเสร็จ
4. **ตรวจก่อนจ่ายไฟ** ทำครบห้าข้อในหัวข้อ 3 จดค่าความต้านทานระหว่างรางตอนปล่อยและตอนกดปุ่ม
5. **จ่ายไฟ** ต่อ GND แล้ว 3V3 แล้วสายสัญญาณ วัดแรงดันราง + เทียบราง − ด้วยมัลติมิเตอร์
6. **ทดสอบการทำงาน** GPIO Out ไฟไล่ถูกลำดับไหม GPIO In บิต 0 ตามปุ่มไหม
7. **ให้เพื่อนตรวจ** ส่งเบรดบอร์ดกับแผนผังให้เพื่อนตรวจโดยคุณไม่อธิบาย จับเวลาว่าเพื่อนใช้กี่นาทีจึงยืนยันได้ว่าต่อถูกทุก net
   เวลานี้คือคะแนนความเรียบร้อยของงานคุณ

| รายการตรวจ | ผล |
|---|---|
| รางไฟขาดครึ่งกลางหรือไม่ | |
| ราง + กับ − (ปล่อยปุ่ม) | ควรเป็น OL |
| ราง + กับ − (กดปุ่ม) | ควรราว 10 kΩ |
| LED ทุกดวงผ่านโหมดไดโอด | |
| แรงดันราง + หลังจ่ายไฟ | |
| GPIO Out ไฟไล่ถูกลำดับ | |
| GPIO In บิต 0 ตามปุ่ม | |
| เวลาที่เพื่อนใช้ตรวจ | |

## ไปต่อ

เบรดบอร์ดเหมาะกับการทดลอง แต่วงจรที่ต้องทนการใช้งานจริงต้องบัดกรี บทเรียนถัดไป [บัดกรีอย่างปลอดภัย](../l02-soldering-safely/README.md)
จะฝึกบัดกรีหัวต่อหนึ่งแถวให้ผ่านการตรวจด้วยตาและมัลติมิเตอร์

## สะท้อนคิด

ครั้งล่าสุดที่วงจรบนเบรดบอร์ดของคุณไม่ทำงาน สาเหตุคืออะไร ถ้าใช้ขั้นตอนตรวจก่อนจ่ายไฟในบทนี้ คุณจะเจอมันเร็วขึ้นแค่ไหน

## แหล่งอ้างอิง

- [Breadboard (Wikipedia)](https://en.wikipedia.org/wiki/Breadboard)
