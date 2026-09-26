---
id: elec.m06.l03
lang: th
title: {th: อ่านแผนผังวงจร, en: Reading schematics}
summary: {th: อ่านสัญลักษณ์ ชื่อสัญญาณ และบล็อกของแผนผังวงจร แล้วตามสัญญาณจากขาชิปไปถึงชิ้นส่วน, en: 'Read symbols, net names and blocks, and trace a signal from a chip pin to a component.'}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m06.l02]
objectives:
- {th: ระบุสัญลักษณ์ของชิ้นส่วนพื้นฐานและชื่อสัญญาณบนแผนผังวงจรได้, en: Identify basic component symbols and net names on a schematic.}
- {th: ตามสัญญาณหนึ่งเส้นจากขาของไมโครคอนโทรลเลอร์ไปถึงหลอด LED หรือปุ่มบนแผนผังของบอร์ดได้, en: Trace one signal from a microcontroller pin to an LED or button on a board schematic.}
develops:
- {skill: hwdev.design-basics, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: alpha
translation: pending
---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ระบุสัญลักษณ์ของชิ้นส่วนพื้นฐานและชื่อสัญญาณบนแผนผังวงจรได้
2. ตามสัญญาณหนึ่งเส้นจากขาของไมโครคอนโทรลเลอร์ไปถึงหลอด LED หรือปุ่มบนแผนผังของบอร์ดได้

## ก่อนเริ่ม

- แผนผังวงจร (schematic) ของบอร์ดที่คุณใช้ ชุดพัฒนาของผู้ผลิตชิปมักมีแผนผังให้ดาวน์โหลดในหน้าผลิตภัณฑ์ของชุดนั้น ถ้าหาไม่เจอให้ถามผู้สอนหรือผู้ดูแลบอร์ด
  ถ้าไม่มีแผนผังจริงเลย แนวคิดและฝึกเติมทั้งหมดทำได้ด้วยแผนผังตัวอย่างในหน้านี้ ส่วนแล็บทำได้บางส่วน
- TESAIoT Dev Kit ที่ flash ตัวอย่าง [QWA309 Potentiometer Monitor](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_pot_monitor&q=prac_qwa309_pot_monitor) และ [QWA309 Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) ได้
- มัลติมิเตอร์ และ logic analyzer

## ดูของจริงก่อน

เอกสารสาธารณะสองชิ้นเกี่ยวกับ TESAIoT Dev Kit พูดถึงลูกบิดตัวเดียวกันไม่ตรงกัน

- README ของตัวอย่าง Potentiometer Monitor และโค้ดของมัน ติดป้าย **VR1 = P15.5** และ **VR2 = P15.4**
- README ของ overlay บอร์ด QWA309 ใน SDK เขียนไว้ในหัวข้อข้อสังเกตของบอร์ดว่า "PCBA silkscreen swaps VR1↔VR2; schematic is authoritative (VR1=P15.4)"
  และอีกข้อหนึ่งว่า ขา CS ของ SPI คือ P9.0 ส่วนป้าย "9.2" บนแผ่นวงจรผิด เพราะ P9.2 คือ MOSI

ใครถูก คำถามนี้ไม่ได้ตอบด้วยการเลือกเชื่อเอกสารที่ดูน่าเชื่อกว่า แต่ตอบด้วยการอ่านแผนผังและวัด
ข้อสังเกตที่สำคัญคือ ทั้งสองเอกสาร **ตรงกันเรื่องชื่อขาของชิป** (P15.4 ถึง P15.7) และไม่ตรงกันเฉพาะ **ชื่อที่คนตั้ง** (VR1, VR2)
เมื่อจบบทนี้ คุณจะตัดสินเรื่องแบบนี้ได้เองบนบอร์ดของคุณ

## แนวคิด

### 1. สัญลักษณ์ รหัสชิ้นส่วน และค่า

<figure>
<svg viewBox="0 0 400 160" width="400" role="img" aria-label="สัญลักษณ์พื้นฐานในแผนผังวงจร" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<polyline points="10,30 20,30 22.5,24 27.5,36 32.5,24 37.5,36 42.5,24 47.5,36 50,30 60,30"/>
<text x="35" y="60" text-anchor="middle" fill="currentColor" stroke="none">R (US)</text>
<path d="M80 30H90"/><rect x="90" y="24" width="30" height="12" rx="3"/><path d="M120 30H130"/>
<text x="105" y="60" text-anchor="middle" fill="currentColor" stroke="none">R (IEC)</text>
<path d="M150 30H166M166 20V40M172 20V40M172 30H188"/>
<text x="169" y="60" text-anchor="middle" fill="currentColor" stroke="none">C</text>
<path d="M205 30H221M221 20V40M227 20V40M227 30H243"/><text x="214" y="18" font-size="11" fill="currentColor" stroke="none">+</text>
<text x="224" y="60" text-anchor="middle" fill="currentColor" stroke="none">C polar</text>
<path d="M262 30H274M274 22V38L286 30Z M286 22V38M286 30H298"/>
<text x="280" y="60" text-anchor="middle" fill="currentColor" stroke="none">diode</text>
<path d="M318 30H330M330 22V38L342 30Z M342 22V38M342 30H354M334 18l6 -8m-4 0h4v4M341 18l6 -8m-4 0h4v4"/>
<text x="336" y="60" text-anchor="middle" fill="currentColor" stroke="none">LED</text>
<path d="M20 110H34M34 98V122M34 105L50 94M34 115L50 126M44 124l6 2l-2 -6"/>
<text x="36" y="144" text-anchor="middle" fill="currentColor" stroke="none">NPN</text>
<path d="M85 110H97M97 98V122M103 98V106M103 107V113M103 114V122M103 102H115V92M103 118H115V128M103 110H115V118M106 110l4 -3m-4 3l4 3"/>
<text x="102" y="144" text-anchor="middle" fill="currentColor" stroke="none">N-MOSFET</text>
<path d="M160 106V114M150 114H170M154 118H166M158 122H162"/>
<text x="160" y="144" text-anchor="middle" fill="currentColor" stroke="none">GND</text>
<path d="M205 106H225M215 106V114"/><text x="215" y="101" text-anchor="middle" fill="currentColor" stroke="none">3V3</text>
<path d="M215 114V122"/>
<text x="215" y="144" text-anchor="middle" fill="currentColor" stroke="none">power net</text>
<path d="M255 110H268"/><circle cx="270" cy="110" r="2.5"/><circle cx="296" cy="110" r="2.5"/><path d="M298 110H311M272 108L295 98"/>
<text x="283" y="144" text-anchor="middle" fill="currentColor" stroke="none">SW</text>
<path d="M330 110H345"/><path d="M345 102H385L392 110L385 118H345Z"/>
<text x="366" y="114" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">SCL</text>
<text x="362" y="144" text-anchor="middle" fill="currentColor" stroke="none">net label</text>
</svg>
<figcaption>สัญลักษณ์ที่เจอบ่อย: ตัวต้านทาน (แบบอเมริกันเป็นฟันเลื่อย แบบ IEC เป็นกล่อง) ตัวเก็บประจุ ตัวเก็บประจุมีขั้ว ไดโอด LED ทรานซิสเตอร์ NPN MOSFET ชนิด N กราวด์ ชื่อไฟเลี้ยง สวิตช์ และป้ายชื่อสัญญาณ</figcaption>
</figure>

ตัวต้านทานมีสองแบบที่เจอบ่อย แบบฟันเลื่อย (นิยมในอเมริกาและญี่ปุ่น) กับแบบกล่อง (มาตรฐาน IEC นิยมในยุโรป) ความหมายเหมือนกัน

**รหัสอ้างอิง (reference designator)** ตัวอักษรบอกชนิด ตัวเลขบอกลำดับ ใช้ตรงกันทั้งในแผนผัง บนแผ่นวงจร และในรายการชิ้นส่วน (BOM)

| ตัวอักษร | ชนิด | ตัวอักษร | ชนิด |
|---|---|---|---|
| R | ตัวต้านทาน | U | ชิป (IC) |
| C | ตัวเก็บประจุ | J, P, CN | ขั้วต่อ |
| L | ตัวเหนี่ยวนำ | SW | สวิตช์ ปุ่ม |
| D | ไดโอด LED | TP | จุดทดสอบ |
| Q | ทรานซิสเตอร์ MOSFET | Y, X | คริสตัล |
| FB | ferrite bead | F | ฟิวส์ |

**การเขียนค่าแบบไม่มีจุดทศนิยม** แผนผังมักใช้ตัวอักษรแทนจุด เพราะจุดเล็ก ๆ หายง่ายเวลาพิมพ์หรือถ่ายสำเนา

```text
4k7 = 4.7 kΩ    2R2 = 2.2 Ω    1M0 = 1.0 MΩ    100n = 100 nF    4p7 = 4.7 pF    1u0 = 1.0 µF
```

รหัสที่พิมพ์บนตัวต้านทานชิป: สองหลักแรกคือตัวเลข หลักสุดท้ายคือจำนวนศูนย์ต่อท้าย "103" = 10 × 10³ = 10 kΩ, "472" = 4.7 kΩ
แบบสี่หลักใช้สามหลักแรกเป็นตัวเลข "4701" = 470 × 10¹ = 4.7 kΩ ตัวเก็บประจุเซรามิกแบบขาเสียบใช้หลักเดียวกันในหน่วย pF "104" = 10 × 10⁴ pF = 100 nF

### 2. สายสัญญาณ ชื่อสัญญาณ และหลายหน้า

**net** คือกลุ่มของจุดที่ต่อถึงกันทางไฟฟ้า แผนผังบอกว่าอะไรอยู่ใน net เดียวกันได้หลายวิธี

- **เส้นที่ลากต่อกัน** เส้นที่ต่อกันเป็นรูปตัว T มี **จุดดำ (junction dot)** เส้นสองเส้นที่ตัดกันเป็นกากบาท **โดยไม่มีจุด** แปลว่าไม่ต่อกัน
- **ป้ายชื่อ (net label)** จุดสองจุดที่มีป้ายชื่อเดียวกันคือ net เดียวกัน แม้ไม่มีเส้นลากถึงกันเลย ใช้ลดเส้นที่ลากข้ามหน้ากระดาษ
- **สัญลักษณ์ไฟเลี้ยงและกราวด์** ทุกสัญลักษณ์ "3V3" ทั่วทั้งแผนผังคือ net เดียวกัน ทุกสัญลักษณ์กราวด์ก็เช่นกัน
- **หลายหน้า (multi-sheet)** แผนผังของบอร์ดจริงมักมีหลายหน้า หน้าแรกเป็นแผนภาพบล็อก ป้ายชื่อหรือตัวเชื่อมข้ามหน้า (off-sheet connector) พาสัญญาณไปหน้าอื่น
  แผนผังแบบลำดับชั้น (hierarchical) ใช้บล็อกย่อยที่มีขาเข้าออกของตัวเอง

**ชื่อสัญญาณที่บอกความหมาย** ชื่อที่ดีบอกได้ทันทีว่าสัญญาณคืออะไร อยู่โดเมนแรงดันไหน และทำงานที่ระดับไหน
โปรแกรมทดสอบ header ของ TESAIoT Dev Kit พิมพ์ชื่อสัญญาณแบบนี้ออกจอ เช่น

```text
P13.3_GPIO_PWM5+_3V3     ขา P13.3 ของชิป | ใช้เป็น GPIO หรือ PWM5 ขั้วบวก | โดเมน 3.3 V
P15.2_ADC_2_PWM3+_3V3    ขา P15.2 | ใช้เป็น ADC ช่อง 2 หรือ PWM3 ขั้วบวก | โดเมน 3.3 V
```

**สัญญาณ active-low** มักมีเครื่องหมายกำกับอย่างใดอย่างหนึ่ง เช่น ขีดทับชื่อ (overbar) ขึ้นต้นด้วย n หรือ / หรือลงท้ายด้วย _N หรือ #
เช่น RESET_N, /CS, nWP, BTN_N ทั้งหมดแปลว่า "ทำงานเมื่อเป็น 0"

### 3. ตามสัญญาณจากขาชิปถึงชิ้นส่วน และเมื่อเอกสารไม่ตรงกับบอร์ด

<figure>
<svg viewBox="0 0 400 275" width="400" role="img" aria-label="แผนผังตัวอย่างที่ใช้ป้ายชื่อสัญญาณเชื่อมสองหน้า" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<rect x="20" y="30" width="90" height="130" rx="3"/>
<text x="65" y="50" text-anchor="middle" font-weight="bold" fill="currentColor" stroke="none">MCU</text>
<text x="106" y="84" text-anchor="end" font-size="11" fill="currentColor" stroke="none">IO1</text>
<text x="106" y="134" text-anchor="end" font-size="11" fill="currentColor" stroke="none">IO2</text>
<path d="M110 80H140"/>
<polyline points="140,80 150,80 152.5,74 157.5,86 162.5,74 167.5,86 172.5,74 177.5,86 180,80 190,80"/>
<text x="165" y="68" text-anchor="middle" fill="currentColor" stroke="none">R12 1k</text>
<path d="M190 80H220"/>
<path d="M220 72H250L262 80L250 88H220Z"/>
<text x="240" y="84" text-anchor="middle" font-size="10" fill="currentColor" stroke="none">LED1</text>
<text x="310" y="84" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">→ sheet 2</text>
<path d="M110 130H220"/>
<path d="M220 122H270L278 130L270 138H220Z"/>
<text x="247" y="134" text-anchor="middle" font-size="10" fill="currentColor" stroke="none">BTN_N</text>
<text x="320" y="134" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">→ sheet 2</text>
<path d="M20 190H380" stroke-dasharray="4 3"/>
<text x="20" y="208" font-size="11" fill="currentColor" stroke="none">sheet 2</text>
<path d="M30 230H60L68 238L60 246H30Z"/>
<text x="48" y="242" text-anchor="middle" font-size="10" fill="currentColor" stroke="none">LED1</text>
<path d="M68 238H100M100 230V246L112 238Z M112 230V246M112 238H140"/>
<path d="M100 226l6 -8m-4 0h4v4M107 226l6 -8m-4 0h4v4"/>
<text x="106" y="262" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">D5</text>
<path d="M140 238V246M130 246H150M134 250H146M138 254H142"/>
<path d="M180 230H230L238 238L230 246H180Z"/>
<text x="208" y="242" text-anchor="middle" font-size="10" fill="currentColor" stroke="none">BTN_N</text>
<path d="M238 238H280"/>
<circle cx="280" cy="238" r="2.5" fill="currentColor"/>
<path d="M280 238V226"/>
<polyline points="280,196 280,196 286,198.5 274,203.5 286,208.5 274,213.5 286,218.5 274,223.5 280,226 280,226"/>
<path d="M270 190H290M280 190V198"/><text x="280" y="185" text-anchor="middle" fill="currentColor" stroke="none">3V3</text>
<text x="292" y="214" font-size="11" fill="currentColor" stroke="none">R40 10k</text>
<path d="M280 238H310"/><circle cx="312" cy="238" r="2.5"/><circle cx="338" cy="238" r="2.5"/><path d="M314 236L336 226M340 238H360V246"/>
<path d="M360 246V254M350 254H370M354 258H366M358 262H362"/>
<text x="325" y="262" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">SW3</text>
</svg>
<figcaption>แผนผังตัวอย่าง (วาดขึ้นเพื่อฝึก ไม่ใช่แผนผังของบอร์ดจริง): หน้า 1 ขา IO1 และ IO2 ของ MCU ออกไปที่ป้ายชื่อ LED1 และ BTN_N หน้า 2 มีป้ายชื่อเดียวกัน จุดที่ชื่อเหมือนกันคือสายเส้นเดียวกันแม้ไม่มีเส้นลากถึงกัน</figcaption>
</figure>

**ขั้นตอนตามสัญญาณ**

1. หาสัญลักษณ์ของไมโครคอนโทรลเลอร์ (มักแบ่งเป็นหลายส่วนตามพอร์ต) แล้วหาขาที่สนใจ
2. ตามเส้นจากขาไปจนเจอชิ้นส่วนหรือป้ายชื่อ ถ้าเจอป้ายชื่อ ค้นหาชื่อเดียวกันในทุกหน้า (โปรแกรมอ่าน PDF ค้นข้อความได้)
3. ทุกชิ้นส่วนที่ผ่าน จดรหัสอ้างอิง ค่า และทิศทาง (เช่น LED หันแอโนดไปทางไหน)
4. ตามจนถึงปลายทาง มักเป็นไฟเลี้ยงหรือกราวด์ แล้วสรุปเป็นประโยค เช่น "ขา IO1 ขับ LED1 แบบ active-high ผ่าน 1 kΩ"
5. เปิดเอกสารข้อมูลของชิ้นส่วนที่ไม่รู้จักประกอบ ขาของชิ้นส่วนบนแผนผังเรียงตามสะดวกของคนวาด ไม่ได้เรียงตามตำแหน่งจริงบนตัวถัง

**เมื่อป้ายบนแผ่นวงจร (silkscreen) ไม่ตรงกับแผนผัง** แผนผังคือเอกสารที่ใช้สร้างแผ่นวงจร จึงมักเชื่อถือได้มากกว่าป้ายที่พิมพ์บนแผ่น
แต่แผนผังก็เป็นเอกสารที่คนเขียน มีรุ่นและอาจผิดได้ ข้อสรุปสุดท้ายต้องมาจากการวัด
ถอดไฟแล้วใช้โหมดความต่อเนื่องจากขาของ header ถึงชิ้นส่วน หรือเปิดไฟแล้วใช้โปรแกรมที่รู้ว่าขับขาไหน แล้วดูด้วย logic analyzer ว่าสัญญาณไปโผล่ที่ไหน

SDK ของ TESAIoT Dev Kit ก็เตือนเรื่องชื่อซ้อนชื่อไว้อีกกรณีหนึ่ง ในตัวอย่าง `cm33/io/04_gpio_led_button.c`
ชื่อ `CYBSP_USER_BTN1` ในโค้ดชี้ไปที่ `CYBSP_SW1` แต่ป้ายบนบอร์ดเขียน SW2 ทั้งสองอย่างไม่ได้ผิด เป็นชื่อในระบบต่างกัน สิ่งที่ผูกทุกชื่อเข้าด้วยกันคือ **ขาของชิป**

## ตัวอย่างสมบูรณ์

**โจทย์** ใช้แผนผังตัวอย่างในหัวข้อ 3 ตอบว่า LED1 และปุ่ม SW3 ทำงานแบบไหน และโปรแกรมต้องตั้งขาอย่างไร

**LED1**

1. หน้า 1: ขา IO1 → R12 (1 kΩ) → ป้าย LED1
2. หน้า 2: ป้าย LED1 → D5 (LED แอโนดทางป้าย แคโทดทางกราวด์) → GND
3. สรุป: IO1 เป็น 1 → กระแสไหลจาก IO1 ผ่าน R12 และ D5 ลงกราวด์ LED ติด เป็น **active-high**
4. กระแส: ถ้า V_f = 2.0 V ได้ (3.3 − 2.0) V / 1 kΩ = 1.3 mA
5. โปรแกรม: ตั้ง IO1 เป็นขาออกแบบ push-pull (บน PSoC คือ `CY_GPIO_DM_STRONG`) เริ่มต้นเป็น 0 เพื่อไม่ให้ไฟวาบตอนเปิดเครื่อง

**SW3**

1. หน้า 1: ขา IO2 → ป้าย BTN_N ตรง ๆ ไม่มีตัวต้านทานคั่น
2. หน้า 2: ป้าย BTN_N → จุดที่มี R40 (10 kΩ) ขึ้นไป 3V3 และ SW3 ลงกราวด์
3. สรุป: ปล่อยปุ่ม R40 ดึงขึ้นเป็น 1 กดปุ่ม SW3 ต่อลงกราวด์เป็น 0 เป็น **active-low** ตรงกับชื่อที่ลงท้าย _N
4. กระแสตอนกด 3.3 V / 10 kΩ = 0.33 mA
5. โปรแกรม: มี pull-up ภายนอกแล้ว ตั้ง IO2 เป็นขาเข้าแบบไม่มี pull ก็พอ (เปิด pull-up ภายในซ้อนก็ไม่ผิด แต่ไม่จำเป็น) และเขียน `pressed = !read(IO2)`

## ฝึกเติม

1. แปลค่าเหล่านี้ 4k7, 2R2, 100n, 1u0, และรหัสบนตัวต้านทานชิป "103" และ "4701" และบนตัวเก็บประจุเซรามิก "104"
2. บอกชนิดของชิ้นส่วนจากรหัสอ้างอิง U3, Q2, TP5, FB1, J4, Y1
3. แยกส่วนของชื่อสัญญาณ `P15.2_ADC_2_PWM3+_3V3` แล้วบอกว่าต่อสัญญาณ 5 V เข้าขานี้ได้ไหม
4. บนแผนผัง เส้นแนวนอนกับเส้นแนวตั้งตัดกันเป็นกากบาท ไม่มีจุดดำ สองเส้นนี้ต่อกันไหม ถ้าเป็นรูปตัว T มีจุดดำล่ะ
5. ชื่อสัญญาณใดเป็น active-low: RESET_N, /CS, nWP, EN, SCL
6. ป้ายบนแผ่นวงจรเขียนขา CS ของ SPI ไว้ที่ตำแหน่ง "9.2" แต่ SDK บอกว่า CS คือ P9.0 และ P9.2 คือ MOSI ออกแบบการทดลองที่ยืนยันได้ว่าขาไหนคือ CS โดยไม่ต้องเปิดแผนผัง

## เฉลย

1. 4.7 kΩ, 2.2 Ω, 100 nF, 1.0 µF, 10 kΩ, 4.7 kΩ และ 100 nF
2. U3 ชิป, Q2 ทรานซิสเตอร์หรือ MOSFET, TP5 จุดทดสอบ, FB1 ferrite bead, J4 ขั้วต่อ, Y1 คริสตัล
3. ขา P15.2 ของชิป | ใช้เป็น ADC ช่อง 2 หรือ PWM3 ขั้วบวก | โดเมน 3.3 V ต่อ 5 V ไม่ได้ เพราะเกินโดเมนแรงดันของขา (ดูบทเรียน [ระดับลอจิก](../../m02-digital-logic/l01-logic-levels-and-gates/README.md))
4. กากบาทไม่มีจุด ไม่ต่อกัน รูปตัว T มีจุด ต่อกัน (นักเขียนแผนผังที่ดีจะหลีกเลี่ยงจุดต่อรูปกากบาทที่มีจุด เพราะจุดเล็ก ๆ อาจหายตอนพิมพ์)
5. RESET_N, /CS และ nWP
6. ตัวอย่างหนึ่ง: ต่อ logic analyzer สองช่องเข้าขา header ตำแหน่ง "9.2" และขาข้างเคียงที่สงสัย รันโปรแกรมทดสอบ header แล้วกดปุ่ม SPI ESP32
   ตามโค้ดของตัวอย่าง ขา CS (P9.0) เริ่มเป็น 1 และลงเป็น 0 ตลอดช่วงส่งข้อมูล ส่วน MOSI (P9.2) เปลี่ยนตามบิตข้อมูลทุกจังหวะนาฬิกา ขาที่มีรูปคลื่นแบบ CS คือ CS จริง

## เช็กความเข้าใจ

ตอบคำถามใน [quiz.yaml](quiz.yaml) ให้ถูกอย่างน้อย 4 ใน 5 ข้อ

## แล็บ

**ส่วน A: ตามสัญญาณบนแผนผังจริง** (ถ้ามีแผนผังของบอร์ด)

1. หาแผนภาพบล็อกหน้าแรก จดว่าแผนผังมีกี่หน้า และแต่ละหน้าเป็นเรื่องอะไร
2. ตามสัญญาณของ LED ผู้ใช้หนึ่งดวงจากขาชิปถึงกราวด์หรือไฟเลี้ยง จดรหัสอ้างอิงและค่าของทุกชิ้นส่วนที่ผ่าน สรุปว่า active-high หรือ active-low
   แล้วเทียบกับ SDK ซึ่งระบุว่า LED ของบอร์ดติดเมื่อขาเป็น 1 (`CYBSP_LED_STATE_ON = 1`)
3. ตามสัญญาณของปุ่มผู้ใช้หนึ่งปุ่ม มีตัวต้านทาน pull-up ภายนอกหรือไม่ ถ้าไม่มี โปรแกรมต้องเปิด pull-up ภายในชิป ซึ่งตรงกับที่ SDK ตั้งปุ่มเป็น `CY_GPIO_DM_PULLUP`
4. หาตัวเก็บประจุ decoupling ของไมโครคอนโทรลเลอร์ นับว่ามีกี่ตัวและค่าอะไรบ้าง เตรียมไว้ใช้ในบทเรียนถัดไป

**ส่วน B: VR1 คือขาไหนบนบอร์ดของคุณ** (TESAIoT Dev Kit)

1. รันตัวอย่าง Potentiometer Monitor หมุนลูกบิดที่ป้ายบนแผ่นวงจรเขียนว่า VR1 ไปสุดทางหนึ่ง แล้วดูว่าการ์ดที่ขยับแสดงขาอะไร
2. ทำซ้ำกับลูกบิดทุกตัว เติมตาราง แล้วสรุปว่าบนบอร์ดของคุณ ป้ายบนแผ่นวงจร โค้ดของตัวอย่าง และคำอธิบายใน SDK สอดคล้องกันแบบไหน
3. เขียนข้อเสนอสั้น ๆ หนึ่งย่อหน้าว่า ถ้าคุณเป็นผู้ดูแลเอกสาร จะแก้ความสับสนนี้อย่างไร (ใบ้: เรียกด้วยชื่อขาของชิปเป็นหลัก)

| ป้ายบนแผ่นวงจร | ขาที่การ์ดบนจอแสดง | ชื่อที่โค้ดตัวอย่างใช้ | ตามแผนผัง (ถ้ามี) |
|---|---|---|---|
| VR1 | | | |
| VR2 | | | |
| VR3 | | | |
| VR4 | | | |

**ส่วน C: อ่านชื่อสัญญาณบน header** รันโปรแกรมทดสอบ header กดปุ่ม ADC In หรือ PWM Out แล้วจดชื่อสัญญาณเต็มที่จอพิมพ์ แยกส่วนความหมายแบบฝึกเติมข้อ 3

## ไปต่อ

บทเรียนสุดท้ายของหลักสูตร [พื้นฐาน PCB และ EMC](../l04-pcb-and-emc-basics/README.md) จะพาจากแผนผังไปสู่แผ่นวงจรจริง
ว่าตำแหน่งของตัวเก็บประจุและรูปร่างของลายวงจรมีผลกับสัญญาณรบกวนอย่างไร

## สะท้อนคิด

ในส่วน B คุณเชื่อเอกสารไหนก่อนวัด และหลังวัดแล้วความเชื่อนั้นเปลี่ยนไหม นิสัยนี้ใช้กับเอกสารอื่นที่คุณอ่านทุกวันได้อย่างไร

## แหล่งอ้างอิง

- [Circuit diagram (Wikipedia)](https://en.wikipedia.org/wiki/Circuit_diagram)
- [Lessons In Electric Circuits โดย Tony R. Kuphaldt (หนังสือเปิด)](https://www.ibiblio.org/kuphaldt/electricCircuits/)
- [SDK: README ของ overlay บอร์ดฐาน QWA309 (ขาและข้อสังเกตของบอร์ด)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-mpy/bento_libs/claw/kit-tesaiot-pse84-ai/README.md)
- [README ของ QWA309 Potentiometer Monitor (Developer Hub, commit 372d0d8)](https://github.com/tesaiot/developer-hub/blob/372d0d849578a6a49b634d3ecaab8b5958166921/prac_qwa309_pot_monitor/README.md)
- [SDK: cm33/io/04_gpio_led_button.c (ชื่อ define กับป้ายบนบอร์ด)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/io/04_gpio_led_button.c)
