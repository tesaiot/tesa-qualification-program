---
id: elec.m04.l02
lang: th
title: {th: ถอดรหัส I2C และ UART, en: Decoding I2C and UART}
summary: {th: ใช้ protocol decoder ของ sigrok อ่านธุรกรรม I2C และเฟรม UART จากบอร์ดจริง, en: Use sigrok protocol decoders to read I2C transactions and UART frames from a real board.}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m04.l01]
objectives:
- {th: 'ตั้ง decoder ของ I2C แล้วอ่าน address, read/write และ ACK จากการสแกนบัสได้', en: 'Set up the I2C decoder and read address, read/write and ACK from a bus scan.'}
- {th: ตั้ง decoder ของ UART ที่ baud rate ถูกต้อง และอธิบายอาการเมื่อตั้งผิด, en: Set up the UART decoder at the right baud rate and describe the symptoms of a wrong setting.}
develops:
- {skill: meas.logic-analyzer, to: 2}
- {skill: proto.i2c, to: 2}
- {skill: proto.uart, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: alpha
translation: done
---

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ

1. ตั้ง decoder ของ I2C แล้วอ่าน address, read/write และ ACK จากการสแกนบัสได้
2. ตั้ง decoder ของ UART ที่ baud rate ถูกต้อง และอธิบายอาการเมื่อตั้งผิด

## ก่อนเริ่ม

- ต่อ logic analyzer ตั้งอัตราสุ่ม และใช้ trigger ได้แล้ว (บทเรียน [จับสัญญาณดิจิทัลครั้งแรก](../l01-capture-a-signal/README.md))
- TESAIoT Dev Kit ที่ flash ตัวอย่าง [QWA309 Header I/O Test](https://dev.tesaiot.dev/?example=developer-hub--prac_qwa309_header_hw_test&q=prac_qwa309_header_hw_test) ไว้
  ตัวอย่างนี้มีปุ่ม **Scan** ที่สแกนบัส I2C และปุ่ม **UART Echo** ที่ส่งแพ็กเก็ตสั้น ๆ ออกขา UART ของ header
- แผนผังขาของบอร์ด เพื่อหาตำแหน่งขา SDA, SCL ของบัส I2C บน header และขา P15.1 (UART TX)
- ถ้าใช้ Eva Kit ให้สแกนบัส I2C และพิมพ์ข้อความออก UART ด้วยโปรแกรมของคุณเอง ขั้นตอนการถอดรหัสเหมือนกันทุกอย่าง

## ดูของจริงก่อน

กดปุ่ม **Scan** บนจอของโปรแกรมทดสอบ header โปรแกรมจะพิมพ์ตารางที่อยู่ 0x08 ถึง 0x77 ช่องที่มีอุปกรณ์ตอบจะขึ้นเป็นตัวเลข ช่องอื่นเป็น `--`
แล้วสรุปว่า "Found N device(s)" ตามด้วยรายการที่อยู่

โปรแกรมรู้ได้อย่างไรว่ามีอุปกรณ์อยู่ที่ที่อยู่ไหน มันถามทีละที่อยู่ 112 ครั้ง แล้วฟังว่ามีใครตอบ "มีครับ" หรือไม่
บทนี้เราจะดักฟังบทสนทนาทั้ง 112 ครั้งนั้นบนสายจริง และพิสูจน์ด้วยตาตัวเองว่าตารางบนจอพูดความจริง

## แนวคิด

### 1. I2C บนสาย: START, address, R/W, ACK, STOP

I2C ใช้สายสองเส้น **SCL** (สัญญาณนาฬิกา มาสเตอร์เป็นคนขับ) และ **SDA** (ข้อมูล) ทั้งสองเส้นเป็นแบบ open-drain อุปกรณ์ทำได้แค่ดึงสายลง
ตัวต้านทาน **pull-up** เป็นตัวดึงสายขึ้น หลักเดียวกับปุ่ม active-low ในบทเรียน [Pull-up, pull-down และปุ่มกด](../../m02-digital-logic/l02-pullups-and-buttons/README.md)

<figure>
<svg viewBox="0 0 390 170" width="390" role="img" aria-label="เฟรม I2C ส่ง address 0x30 แบบเขียนพร้อม ACK" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<text x="10" y="47" fill="currentColor" stroke="none">SCL</text>
<text x="10" y="107" fill="currentColor" stroke="none">SDA</text>
<polyline points="20,30 80,30 80,55 90,55 90,30 103,30 103,55 116,55 116,30 129,30 129,55 142,55 142,30 155,30 155,55 168,55 168,30 181,30 181,55 194,55 194,30 207,30 207,55 220,55 220,30 233,30 233,55 246,55 246,30 259,30 259,55 272,55 272,30 285,30 285,55 298,55 298,30 311,30 311,55 330,55 330,30 374,30"/>
<polyline points="20,90 70,90 70,115 84,115 84,115 110,115 110,90 136,90 136,90 162,90 162,115 188,115 188,115 214,115 214,115 240,115 240,115 266,115 266,115 292,115 292,115 336,115 336,115 346,115 346,90 374,90"/>
<text x="96.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<text x="122.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">1</text>
<text x="148.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">1</text>
<text x="174.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<text x="200.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<text x="226.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<text x="252.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<text x="278.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">W</text>
<text x="304.5" y="138" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">A</text>
<text x="70" y="158" text-anchor="middle" font-weight="bold" fill="currentColor" stroke="none">S</text>
<text x="168" y="158" text-anchor="middle" fill="currentColor" stroke="none">address 0x30</text>
<text x="278" y="158" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">R/W</text>
<text x="306" y="158" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">ACK</text>
<text x="346" y="158" text-anchor="middle" font-weight="bold" fill="currentColor" stroke="none">P</text>
</svg>
<figcaption>เฟรม I2C: START (S) คือ SDA ตกขณะ SCL สูง ตามด้วย address 7 บิต (0x30 = 0110000) บิต R/W (0 = เขียน) แล้วอุปกรณ์ปลายทางดึง SDA ลงเพื่อ ACK จบด้วย STOP (P) คือ SDA ขึ้นขณะ SCL สูง</figcaption>
</figure>

- **START (S)** SDA ตกลงขณะ SCL ยังสูง เป็นสัญญาณ "จะเริ่มพูดแล้ว"
- **address 7 บิต** ส่งจากบิตสูงสุดก่อน (MSB first) ข้อมูลบน SDA ต้องนิ่งขณะ SCL สูง และเปลี่ยนได้เฉพาะตอน SCL ต่ำ
- **R/W** บิตที่ 8 เป็น 0 = เขียน, 1 = อ่าน
- **ACK / NACK** ในจังหวะนาฬิกาที่ 9 มาสเตอร์ปล่อย SDA ถ้าอุปกรณ์ที่อยู่นั้นมีอยู่จริง มันจะดึง SDA ลง (ACK) ถ้าไม่มีใคร SDA ค้างสูงด้วย pull-up (NACK)
- **STOP (P)** SDA ขึ้นขณะ SCL สูง

**address 7 บิตกับไบต์บนสาย** ไบต์แรกบนสายคือ address เลื่อนซ้ายหนึ่งบิตแล้วต่อด้วยบิต R/W
address 0x30 แบบเขียนจึงเป็นไบต์ 0x60 แบบอ่านเป็น 0x61 เอกสารข้อมูลบางฉบับเขียนที่อยู่เป็นแบบ 8 บิต (0x60) ทำให้คนสับสนบ่อยมาก
decoder ของ sigrok แสดงเป็น 7 บิตโดยปริยาย (เช่น "Address write: 30")

**เครื่องสแกนบัสทำอะไร** โปรแกรมทดสอบ header ส่ง START + address + W แล้ว STOP ทีละที่อยู่ ไม่ส่งข้อมูลอื่นเลย
ที่อยู่ที่ได้ ACK คือที่อยู่ที่มีอุปกรณ์ ตามเอกสารของบอร์ดใน SDK บัส I2C บน header ของ TESAIoT Dev Kit มีชิป CapSense (PSoC 4000T) ตอบที่ 0x08
คุณจึงควรเห็น ACK ที่ 0x08 อย่างน้อยหนึ่งที่อยู่ ส่วนที่อยู่อื่นที่ตอบ ให้เทียบกับรายการที่จอพิมพ์

**ขนาด pull-up ของ I2C** (สูตรจาก TI SLVA689) ตัวต้านทานต้องไม่เล็กจนอุปกรณ์ดึงสายลงไม่ถึง V_OL และไม่ใหญ่จนขอบขาขึ้นช้าเกินข้อกำหนด

```text
R_p(min) = (V_CC − V_OL(max)) / I_OL = (3.3 − 0.4) V / 3 mA = 967 Ω
R_p(max) = t_r / (0.8473 × C_b)
  Fast-mode 400 kHz (t_r ≤ 300 ns) บัส 100 pF → 300 ns / (0.8473 × 100 pF) = 3.54 kΩ
  Standard-mode 100 kHz (t_r ≤ 1000 ns) บัส 100 pF → 11.8 kΩ
```

บัส 400 kHz ที่มีความจุ 100 pF จึงเลือกได้ระหว่าง 967 Ω ถึง 3.54 kΩ เช่น 2.2 kΩ
ค่าคงที่ 0.8473 มาจาก ln(0.7 / 0.3) คือเวลาที่ RC ใช้ขึ้นจาก 0.3 × V_CC ถึง 0.7 × V_CC ซึ่งเป็นเกณฑ์ V_IL และ V_IH ของ I2C

### 2. UART บนสาย: ไม่มีสัญญาณนาฬิกา ต้องตกลงความเร็วกันก่อน

UART ส่งข้อมูลบนสายเส้นเดียวต่อทิศทาง (TX ของฝั่งหนึ่งต่อกับ RX ของอีกฝั่ง) ไม่มีสายนาฬิกา สองฝั่งจึงต้องตั้ง **baud rate** เท่ากันไว้ล่วงหน้า
รูปแบบที่พบบ่อยที่สุดคือ **8N1** ข้อมูล 8 บิต ไม่มีบิตตรวจ (parity) บิตหยุด 1 บิต

<figure>
<svg viewBox="0 0 400 145" width="400" role="img" aria-label="เฟรม UART 8N1 ของไบต์ 0xA5" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<polyline points="10,40 50,40 50,40 50,80 80,80 80,40 110,40 110,80 140,80 140,40 170,40 170,80 200,80 200,80 230,80 230,40 260,40 260,80 290,80 290,40 320,40 320,40 350,40 380,40"/>
<path d="M50 90V96" stroke-dasharray="4 3"/>
<text x="65.0" y="110" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">start</text>
<text x="65.0" y="30" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<path d="M80 90V96" stroke-dasharray="4 3"/>
<text x="95.0" y="110" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">b0</text>
<text x="95.0" y="30" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">1</text>
<path d="M110 90V96" stroke-dasharray="4 3"/>
<text x="125.0" y="110" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">b1</text>
<text x="125.0" y="30" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<path d="M140 90V96" stroke-dasharray="4 3"/>
<text x="155.0" y="110" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">b2</text>
<text x="155.0" y="30" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">1</text>
<path d="M170 90V96" stroke-dasharray="4 3"/>
<text x="185.0" y="110" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">b3</text>
<text x="185.0" y="30" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<path d="M200 90V96" stroke-dasharray="4 3"/>
<text x="215.0" y="110" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">b4</text>
<text x="215.0" y="30" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<path d="M230 90V96" stroke-dasharray="4 3"/>
<text x="245.0" y="110" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">b5</text>
<text x="245.0" y="30" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">1</text>
<path d="M260 90V96" stroke-dasharray="4 3"/>
<text x="275.0" y="110" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">b6</text>
<text x="275.0" y="30" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0</text>
<path d="M290 90V96" stroke-dasharray="4 3"/>
<text x="305.0" y="110" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">b7</text>
<text x="305.0" y="30" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">1</text>
<path d="M320 90V96" stroke-dasharray="4 3"/>
<text x="335.0" y="110" text-anchor="middle" font-size="11" fill="currentColor" stroke="none">stop</text>
<text x="335.0" y="30" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">1</text>
<text x="10" y="30" font-size="11" fill="currentColor" stroke="none">idle</text>
<text x="200" y="135" text-anchor="middle" font-size="12" fill="currentColor" stroke="none">0xA5 = 1010 0101, sent LSB first · 115200 baud: 8.68 µs per bit</text>
</svg>
<figcaption>เฟรม UART แบบ 8N1 ของไบต์ 0xA5: สายว่างเป็น 1 บิตเริ่มเป็น 0 ตามด้วยข้อมูล 8 บิตเรียงจากบิตต่ำสุด (LSB) แล้วบิตหยุดเป็น 1</figcaption>
</figure>

- สายว่างเป็น 1
- **บิตเริ่ม (start)** เป็น 0 หนึ่งช่วงบิต ฝั่งรับใช้ขอบขาลงนี้ตั้งจังหวะ
- **ข้อมูล 8 บิต** ส่งจาก **บิตต่ำสุดก่อน (LSB first)** ตรงข้ามกับ I2C
- **บิตหยุด (stop)** เป็น 1 ถ้าฝั่งรับอ่านได้ 0 ตรงนี้ จะรายงาน framing error

**ตัวเลขที่ 115200 baud**

```text
1 บิต     = 1 / 115200 s = 8.68 µs
1 ไบต์    = 10 บิต (start + 8 + stop) = 86.8 µs
ส่งได้สูงสุด = 115200 / 10 = 11,520 ไบต์ต่อวินาที
```

**ตัวอย่าง** ไบต์ 0xA5 = 1010 0101 ส่ง LSB ก่อน บิตบนสายหลังบิตเริ่มจึงเป็น 1, 0, 1, 0, 0, 1, 0, 1 แล้วตามด้วยบิตหยุด 1

**UART Echo ของโปรแกรมทดสอบ header** ส่งแพ็กเก็ต 4 ไบต์ออกขา P15.1 ที่ 115200 8N1 คือ `A5 11 <ตัวนับ> <checksum>`
ตัวนับเริ่มที่ 0 และเพิ่มทีละหนึ่งทุกครั้งที่กดปุ่ม checksum คือ XOR ของสามไบต์แรก กดครั้งแรกจึงได้ `A5 11 00 B4` (0xA5 XOR 0x11 = 0xB4)
และโปรแกรมพิมพ์ไบต์ที่ส่งไว้บนจอในบรรทัด `TX:` ด้วย เราจึงมีเฉลยให้เทียบกับ decoder
ถ้าไม่มีบอร์ด ESP32-S3 ตอบกลับตามที่ตัวอย่างออกแบบไว้ ตามค่าคงที่ในโค้ด โปรแกรมจะรอคำตอบครั้งละ 250 ms พัก 10 ms แล้วส่งซ้ำ รวม 4 ครั้ง ระยะห่างจริงให้วัดเองจากภาพ

### 3. อ่านภาพสัญญาณให้เจอความผิดพลาด

**ตั้ง baud ผิด** decoder จะวัดบิตผิดจังหวะ อาการคือไบต์เพี้ยนและมี framing error

- ตั้ง 9600 กับสัญญาณ 115200 หนึ่งบิตที่ decoder คาดคือ 104 µs แพ็กเก็ต 4 ไบต์ทั้งก้อน (ราว 347 µs) ยาวเพียงราว 3.3 บิตของ 9600 decoder จึงเห็นไบต์เดียวที่เพี้ยนหรือ error
- ตั้ง 57600 (ครึ่งหนึ่ง) แต่ละบิตที่ decoder อ่านคร่อมสองบิตจริง ได้ไบต์ผิดค่าและมักมี framing error
- ตั้งเร็วเกินไป เช่น 230400 decoder เห็นหนึ่งบิตจริงเป็นสองบิต ไบต์ที่ได้ไม่มีความหมาย

**หา baud จากภาพ** ซูมหาพัลส์ที่แคบที่สุด (หนึ่งบิต) แล้วคำนวณ baud ≈ 1 / ความกว้าง พัลส์ 8.68 µs คือ 115200 พัลส์ 104 µs คือ 9600
แล้วเลือกค่ามาตรฐานที่ใกล้ที่สุด UART ทนความคลาดของ baud ได้เพียงเล็กน้อย (โดยทั่วไปความคลาดรวมของสองฝั่งควรไม่เกินราว 2 ถึง 3%)

**อาการอื่นที่ภาพบอกได้**

| สิ่งที่เห็น | สาเหตุที่เป็นไปได้ |
|---|---|
| I2C: address ได้ NACK ทุกที่อยู่ | ไม่มีอุปกรณ์ ไฟเลี้ยงอุปกรณ์ไม่มา สาย SDA กับ SCL สลับกัน หรือ address ผิด |
| I2C: SDA หรือ SCL ค้างต่ำตลอด | อุปกรณ์ค้างกลางธุรกรรม หรือสายลัดลงกราวด์ |
| I2C: ขอบขาขึ้นช้าเป็นเส้นโค้งยาว (ต้องดูด้วยออสซิลโลสโคป) | pull-up ใหญ่เกินไป หรือบัสยาวจนความจุสูง |
| UART: ไม่มีอะไรบนสาย RX ทั้งที่อีกฝั่งส่ง | ต่อ TX เข้า TX (ต้องไขว้ TX กับ RX) หรือลืมต่อ GND ร่วม |

## ตัวอย่างสมบูรณ์

**โจทย์** ถอดรหัสการสแกนบัส I2C ของโปรแกรมทดสอบ header แล้วยืนยันผลบนจอ

1. **ต่อสาย** GND ของเครื่องเข้า GND ช่อง 0 เข้า SCL ช่อง 1 เข้า SDA ของบัส I2C บน header (หาตำแหน่งจากแผนผังขาของบอร์ด)
2. **อัตราสุ่ม** ยังไม่รู้ความเร็วบัส ใช้ 8 MHz ไว้ก่อน ครอบคลุมถึง 400 kHz (ได้ 20 ตัวอย่างต่อคาบเวลาของ SCL)
   จับแล้ววัดคาบเวลาของ SCL ถ้าพบว่าเป็น 100 kHz ลดอัตราสุ่มลงได้เพื่อจับได้นานขึ้น
3. **trigger** ขอบขาลงของ SDA (ซึ่งเกิดตอน START) กด Run แล้วกด Scan บนจอ
4. **เพิ่ม decoder** ใน PulseView เพิ่ม decoder ชื่อ I2C กำหนด SCL = ช่อง 0 และ SDA = ช่อง 1
5. **อ่านผล** แถบ decoder จะแสดงลำดับ Start → Address write: 08 → ACK หรือ NACK → Stop ซ้ำไปเรื่อย ๆ ทีละที่อยู่
6. **ตรวจ** ที่อยู่ 0x08 ควรได้ ACK (ชิป CapSense) ส่วนที่อยู่ที่ไม่มีอุปกรณ์จะได้ NACK นับที่อยู่ที่ได้ ACK ทั้งหมดแล้วเทียบกับ "Found N device(s)" บนจอ ต้องตรงกันทุกที่อยู่
7. **ดูไบต์ดิบ** เปลี่ยนการแสดงผลของ decoder ให้แสดง address แบบ 8 บิต ที่อยู่ 0x08 แบบเขียนต้องเป็น 0x10

ถ้าจำนวนที่ได้ ACK บนสายไม่ตรงกับจอ อย่าเพิ่งโทษเครื่องมือ ตรวจก่อนว่าจับได้ครบทั้ง 112 ที่อยู่หรือไม่ (เวลาจับพอไหม) และอัตราสุ่มเร็วพอไหม

## ฝึกเติม

1. อุปกรณ์มี address 7 บิตเป็น 0x44 ไบต์แรกบนสายแบบเขียนและแบบอ่านเป็นเท่าไร
2. decoder แสดง "Address read: 68" ตามด้วย NACK หมายความว่าอะไร และจะตรวจอะไรต่อ
3. UART 9600 8N1 หนึ่งบิตยาวเท่าไร หนึ่งไบต์ยาวเท่าไร ส่งได้สูงสุดกี่ไบต์ต่อวินาที
4. ส่งไบต์ 0x55 ที่ UART 8N1 สายจะมีรูปร่างอย่างไร ทำไมไบต์นี้จึงมีประโยชน์เวลาหา baud
5. วัดพัลส์ที่แคบที่สุดบนสาย UART ได้ 26 µs baud น่าจะเป็นเท่าไร
6. บัส I2C 3.3 V ที่ 100 kHz มีความจุรวม 200 pF หา R_p(min) และ R_p(max) แล้วตอบว่า 4.7 kΩ ใช้ได้หรือไม่
7. กดปุ่ม UART Echo เป็นครั้งที่สาม (ตัวนับเป็น 0x02) แพ็กเก็ตทั้ง 4 ไบต์บนสายควรเป็นอะไร

## เฉลย

1. เขียน: 0x44 เลื่อนซ้ายหนึ่งบิต = 0x88 อ่าน: 0x89
2. มาสเตอร์ขออ่านจากที่อยู่ 0x68 แต่ไม่มีใครตอบ ตรวจว่าอุปกรณ์มีไฟเลี้ยง อยู่บนบัสเดียวกันจริง (บอร์ดอาจมีหลายบัส) และ address ถูกต้องตามเอกสาร รวมถึงขา address ของอุปกรณ์
3. 1 บิต = 1 / 9600 = 104.2 µs 1 ไบต์ = 10 บิต = 1.042 ms ส่งได้สูงสุด 960 ไบต์ต่อวินาที
4. 0x55 = 0101 0101 ส่ง LSB ก่อนได้ 1, 0, 1, 0, 1, 0, 1, 0 เมื่อรวมบิตเริ่ม (0) และบิตหยุด (1) สายจะสลับ 0 กับ 1 ทุกบิต เป็นคลื่นสี่เหลี่ยมที่ทุกพัลส์กว้างหนึ่งบิตพอดี วัดความกว้างแล้วได้ baud ทันที
5. 1 / 26 µs = 38,462 baud ค่ามาตรฐานที่ใกล้ที่สุดคือ 38400
6. R_p(min) = (3.3 − 0.4) / 3 mA = 967 Ω R_p(max) = 1000 ns / (0.8473 × 200 pF) = 5.90 kΩ ค่า 4.7 kΩ อยู่ในช่วง ใช้ได้
7. `A5 11 02 B6` เพราะ 0xA5 XOR 0x11 XOR 0x02 = 0xB6

## เช็กความเข้าใจ

ตอบคำถามใน [quiz.yaml](quiz.yaml) ให้ถูกอย่างน้อย 4 ใน 5 ข้อ

## แล็บ

**ส่วน A: การสแกนบัส I2C** ทำตามตัวอย่างสมบูรณ์ แล้วเติมตาราง

| สิ่งที่ตรวจ | บนจอของบอร์ด | จาก decoder |
|---|---|---|
| ความถี่ SCL | ไม่แสดง | |
| จำนวนที่อยู่ที่ถูกถาม | 112 (0x08 ถึง 0x77) | |
| ที่อยู่ที่ได้ ACK | | |
| ไบต์บนสายของที่อยู่แรกที่ได้ ACK (แบบ 8 บิต) | ไม่แสดง | |

**ส่วน B: UART Echo**

1. ต่อช่อง 0 เข้า P15.1 (TX) และถ้ามีช่องว่าง ต่อช่อง 1 เข้า P15.0 (RX) ตั้งอัตราสุ่ม 4 MHz เวลาจับ 2 s trigger ขอบขาลงของช่อง 0
2. เพิ่ม decoder ชื่อ UART ตั้ง baud 115200, 8 data bits, parity none, 1 stop bit กำหนด RX ของ decoder ให้อ่านช่อง 0
   (ชื่อ RX และ TX ในหน้าตั้งค่า decoder หมายถึงสายที่ decoder จะอ่าน ไม่ได้หมายถึงฝั่งของบอร์ด)
3. กด UART Echo บนจอ เทียบไบต์ที่ decoder อ่านได้กับบรรทัด `TX:` บนจอ ต้องตรงกันทุกไบต์ และนับว่าแพ็กเก็ตถูกส่งกี่ครั้ง ห่างกันเท่าไร
4. วัดความกว้างของบิตเริ่ม คำนวณ baud จริงจากภาพ แล้วเทียบกับ 115200
5. **ทำให้ผิดโดยตั้งใจ** เปลี่ยน baud ของ decoder เป็น 57600 และ 9600 จดสิ่งที่ decoder แสดง แล้วอธิบายด้วยหัวข้อ 3
6. ดูช่อง 1 (RX) ถ้าไม่มีอุปกรณ์ตอบกลับ สายจะว่างเป็น 1 ตลอด ถ้าคุณมีบอร์ด ESP32-S3 ตามที่ README ของตัวอย่างอธิบาย จะเห็นคำตอบ 5 ไบต์ขึ้นต้นด้วย 0x5A

| baud ของ decoder | สิ่งที่เห็น |
|---|---|
| 115200 | |
| 57600 | |
| 9600 | |

## ไปต่อ

logic analyzer บอกได้ว่าสัญญาณเป็น 0 หรือ 1 เมื่อไร แต่ไม่บอกว่าแรงดันจริงหน้าตาเป็นอย่างไร บทเรียนถัดไป [ออสซิลโลสโคปเบื้องต้น](../../m05-oscilloscope/l01-scope-basics/README.md)
จะให้เราเห็นขอบสัญญาณ แรงดันเกิน และสัญญาณรบกวนที่ logic analyzer มองไม่เห็น ถ้าอยากต่อยอดด้าน I2C บนบอร์ดนี้ ดูบทเรียน
[RGB matrix ผ่าน I2C ในหลักสูตร TESAIoT Firmware Stack](../../../tesaiot-firmware-stack/m04-qwa309-hardware/l03-rgb-matrix-i2c/README.md)

## สะท้อนคิด

ครั้งต่อไปที่โปรแกรมบอกว่า "ส่งแล้ว" หรือ "ไม่พบอุปกรณ์" คุณจะใช้เวลากี่นาทีพิสูจน์ด้วย logic analyzer ว่าบนสายเกิดอะไรขึ้นจริง และมันคุ้มกว่าการเดาไหม

## แหล่งอ้างอิง

- [sigrok protocol decoders](https://sigrok.org/wiki/Protocol_decoders)
- [Texas Instruments: Understanding the I2C Bus (SLVA704)](https://www.ti.com/lit/an/slva704/slva704.pdf)
- [SDK: cm33/sensors/01_i2c_bus_scan.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/01_i2c_bus_scan.c)
- [Texas Instruments: I2C Bus Pullup Resistor Calculation (SLVA689)](https://www.ti.com/lit/an/slva689/slva689.pdf)
- [SDK: แผนผังความสามารถของบอร์ดฐาน QWA309 (kit-tesaiot-pse84-ai/README.md)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-mpy/bento_libs/claw/kit-tesaiot-pse84-ai/README.md)
- [โค้ดของ QWA309 Header I/O Test (Developer Hub, commit 372d0d8)](https://github.com/tesaiot/developer-hub/blob/372d0d849578a6a49b634d3ecaab8b5958166921/prac_qwa309_header_hw_test/header_tester_ui.c)
