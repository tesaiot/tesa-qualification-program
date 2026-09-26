---
id: sec-iot.m04.l01
lang: th
title: {th: Secure boot และ chain of trust, en: Secure boot and the chain of trust}
summary: {th: ตามลำดับการบูตของบอร์ดและดูว่าแต่ละขั้นตรวจขั้นถัดไปอย่างไร, en: Follow the board's boot order and how each stage checks the next.}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m03.l02]
objectives:
- {th: อธิบายบทบาทของคอร์ CM33_S ในการบูตแบบปลอดภัยของแม่แบบเฟิร์มแวร์, en: Explain the role of the CM33_S core in the template's secure boot.}
- {th: วาดห่วงโซ่ความเชื่อใจตั้งแต่ ROM จนถึงแอปพลิเคชัน และระบุว่าลายเซ็นถูกตรวจที่ขั้นใด, en: Draw the chain of trust from ROM to application and mark where signatures are checked.}
- {th: อธิบายความต่างระหว่าง secure boot กับการเข้ารหัสเฟิร์มแวร์, en: Explain the difference between secure boot and firmware encryption.}
develops:
- {skill: sec.secure-boot, to: 3}
- {skill: mcu.bootloader, to: 2}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
slides: slides.md
source:
- {repo: 'https://github.com/tesaiot/tesaiot-pse84-devkit-sdk', path: bento-firmware-template-mtb-only/configs, ref: ef72c1b658178eee8c38b1e47d28b006f80a59b5, license: Apache-2.0}
- {repo: 'https://github.com/Infineon/mtb-example-psoc-edge-basic-secure-app', path: README.md, ref: 96783c046340f79940f7d50b1c5c25fef4a0797f, note: 'Boot flow facts paraphrased; linked, not copied.'}
---

# บทเรียน 4.1: Secure boot และ chain of trust

> โมดูล 4 · Secure boot และ Protected Update · [ภาพรวมโมดูล](../README.md) · [หน้าหลักสูตร](../../README.md)

mTLS พิสูจน์ได้ว่ากุญแจอยู่ในชิป แต่ถ้าเฟิร์มแวร์ที่สั่งชิปถูกเปลี่ยน ผู้โจมตีก็สั่งชิปลงนามแทนเราได้ (บทเรียน 1.2)
คำถามของบทนี้จึงเป็น "เฟิร์มแวร์ที่รันอยู่ คือตัวที่เราตั้งใจให้รันจริงไหม" และบนบอร์ดนี้ใครเป็นคนตรวจ ตรวจถึงขั้นไหน

## เป้าหมาย

เมื่อจบบทเรียนนี้ คุณจะ:

1. อธิบายบทบาทของคอร์ CM33_S ในการบูตแบบปลอดภัยของแม่แบบเฟิร์มแวร์
2. วาดห่วงโซ่ความเชื่อใจตั้งแต่ ROM จนถึงแอปพลิเคชัน และระบุว่าลายเซ็นถูกตรวจที่ขั้นใด
3. อธิบายความต่างระหว่าง secure boot กับการเข้ารหัสเฟิร์มแวร์

## ก่อนเริ่ม

- **เรียนมาก่อน:** [บทเรียน 3.2: MQTTs ขึ้น TESAIoT Platform](../../m03-mtls-to-platform/l02-mqtts-to-tesaiot/README.md) และทบทวนเรื่องลายเซ็นใน [บทเรียน 1.2](../../m01-threats-and-crypto/l02-crypto-basics/README.md)
- **ซอฟต์แวร์:** แม่แบบ `bento-firmware-template-mtb-only` ของ SDK ที่ `ef72c1b` ที่ build ได้แล้ว
- **สิ่งที่บทนี้จะไม่ให้ทำ:** การ provision อุปกรณ์ให้เปิด secure boot (`secure_boot=true` ใน OEM policy) และการโอนความเป็นเจ้าของอุปกรณ์ด้วยกุญแจ OEM
  README ของ [ตัวอย่าง basic secure app ของ Infineon](https://github.com/Infineon/mtb-example-psoc-edge-basic-secure-app) บอกว่าหลัง provision แล้ว Extended Boot จะเปิด image แรกก็ต่อเมื่อลายเซ็นตรวจผ่านเท่านั้น
  งานนี้เปลี่ยนการทำงานของอุปกรณ์ระดับชิป ต้องทำตาม [AN237849 Getting started with PSOC™ Edge security](https://www.infineon.com/AN237849) โดยคนที่ตัดสินใจแล้วและดูแลกุญแจ OEM ได้

## ดูของจริงก่อน

ตาราง "คอร์ไหนทำอะไร" ใน [README ของแม่แบบ](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/README.en.md) มีแถวแรกแบบนี้

| Core | Runs | Typical work |
|---|---|---|
| **CM33_S** | secure boot | you will not touch this |

ส่วน [proj_cm33_s/main.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_s/main.c) ทั้งไฟล์ยาวไม่ถึงห้าสิบบรรทัด
คำอธิบายหัวไฟล์คือ "CM33 Secure boot - TrustZone setup and jump to CM33_NS" ใน `main()` มีแค่ `cybsp_init()` เปิด interrupt
อ่านค่า stack pointer กับ reset handler จากตาราง vector ของ CM33_NS แล้วกระโดดไปที่นั่น

**ทายก่อน:** ก่อนกระโดด CM33_S ตรวจลายเซ็นของเฟิร์มแวร์ CM33_NS หรือไม่ แล้วถ้าไม่ตรวจ ใครตรวจอะไร

## แนวคิด

### 1. บทบาทของ CM33_S

PSoC™ Edge E84 มีสามคอร์ และ Cortex-M33 ตัวหลักแบ่งเป็นฝั่ง secure กับ non-secure ด้วย TrustZone แม่แบบจึงมีสามโปรเจกต์ `proj_cm33_s`, `proj_cm33_ns`, `proj_cm55`
README ของตัวอย่าง Infineon อธิบายลำดับไว้ว่า Extended Boot เปิดโปรเจกต์ CM33 secure จากตำแหน่งคงที่ในหน่วยความจำ
CM33 secure ตั้งค่าการป้องกันแล้วเปิดแอป CM33 non-secure จากนั้น CM33 non-secure เปิดคอร์ CM55
ในแม่แบบของเรา ขั้นสุดท้ายนี้อยู่ใน `init_cm55_boot()` ที่เรียก `Cy_SysEnableCM55()` ตามบท [B1 ของเอกสาร SDK](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__b1__cm33__boot.html)

CM33_S จึงเป็น **image แรกของผู้ใช้** ที่ Extended Boot เห็น และเป็นข้อต่อเดียวที่ Extended Boot ตรวจลายเซ็นได้
ไฟล์ [common.mk](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/common.mk) ของแม่แบบมีสวิตช์ `SECURE_BOOT` สองค่า

- `SECURE_BOOT=0` (ค่าเริ่มต้น) ใช้ `configs/boot_with_extended_boot.json` image ของ CM33_S ได้แค่ส่วนหัว MCUboot และ **ไม่ได้ลงนาม**
- `SECURE_BOOT=1` ใช้ `configs/secure_boot_with_extended_boot.json` image ของ CM33_S ถูกลงนามด้วยกุญแจ OEM root of trust ตามที่อุปกรณ์ซึ่ง provision `secure_boot=true` แล้วต้องการ
  build log จะพิมพ์ยืนยันว่า CM33_S จะถูกลงนามด้วยกุญแจไฟล์ไหน

ค่าอื่นนอกจาก `0` กับ `1` เช่น `true` หรือ `yes` ทำให้ build **หยุดด้วย error** ทันที คอมเมนต์ในไฟล์ให้เหตุผลว่าค่าที่พิมพ์ผิดต้องไม่กลายเป็น build ที่ไม่ได้ลงนามแบบเงียบ ๆ

### 2. ห่วงโซ่ความเชื่อใจของบอร์ดนี้ และจุดที่มีการตรวจลายเซ็น

**root of trust** คือส่วนที่เราเชื่อโดยไม่มีใครตรวจมันอีกที ETSI EN 303 645 ข้อ 5.7-1 อธิบายว่า hardware root of trust เป็นวิธีหนึ่งที่ทำให้ secure boot มีความหมาย
บนบอร์ดนี้จุดเริ่มคือโค้ดของ Infineon ในชิป แล้วแต่ละขั้นเปิดขั้นถัดไป คำถามคือ **ก่อนเปิด มีการตรวจไหม**

```text
 Boot ROM (โค้ดของ Infineon ในชิป)
    │
    ▼
 Extended Boot (ของ Infineon)
    │   ตรวจลายเซ็นของ image CM33_S ด้วยกุญแจ OEM
    │   ✔ เมื่ออุปกรณ์ provision secure_boot=true และ build ด้วย SECURE_BOOT=1
    │   ✘ ในสภาพเริ่มต้นของแม่แบบ (SECURE_BOOT=0)
    ▼
 CM33_S  (proj_cm33_s)   cybsp_init() แล้วกระโดดไป reset handler ของ CM33_NS
    │   ✘ ไม่ตรวจลายเซ็นของ CM33_NS (main.c ของแม่แบบ)
    ▼
 CM33_NS (proj_cm33_ns)  FreeRTOS, PSA + driver ของ OPTIGA, WiFi, MQTT แล้ว Cy_SysEnableCM55()
    │   ✘ ไม่ตรวจลายเซ็นของ CM55
    ▼
 CM55    (proj_cm55)     จอ, Edge AI
        ◦ โมเดล AI ที่ส่งเข้ามาตอนรัน ผ่าน hook optiga_verify_staged_model() (บทเรียน 1.2)
```

หลักฐานว่าลายเซ็นครอบแค่ CM33_S อยู่ใน `secure_boot_with_extended_boot.json` ขั้น `sign` มีอินพุตไฟล์เดียวคือ `proj_cm33_s.hex`
ส่วน `proj_cm33_ns.hex` ผ่านแค่ขั้น `hex-relocate` และ `proj_cm55.hex` เข้าขั้น `merge` ตรง ๆ ทั้งสามรวมเป็น `app_combined.hex` ไฟล์เดียว

**ข้อสรุปที่ต้องเขียนลง threat model** ต่อให้เปิด secure boot ครบแล้ว ห่วงโซ่ในแม่แบบนี้ก็ขาดหลัง CM33_S ผู้ที่เขียน flash ส่วนของ CM33_NS หรือ CM55 ได้ จะรันโค้ดของตัวเองได้โดยไม่มีใครตรวจ
ถ้างานของคุณต้องการห่วงโซ่ครบ ต้องให้ CM33_S (หรือ bootloader ที่อยู่ตรงนั้น) ตรวจ image ถัดไปก่อนกระโดด Infineon มี EdgeProtect Bootloader ที่ README ของตัวอย่างอ้างถึง แต่แม่แบบนี้ไม่ได้ใช้

อีกสองที่ในหลักสูตรนี้ที่มีการตรวจลายเซ็น แต่ **ไม่ใช่** ขั้นของการบูต

- manifest ของ Protected Update ถูกตรวจ **ในชิป** OPTIGA™ Trust M ก่อนเขียน object (บทเรียน 4.2)
- hook ตรวจโมเดล AI ที่ส่งเข้ามาตอนรัน ใน SDK ค่าเริ่มต้นเป็นฟังก์ชัน weak ที่ตอบว่า "เครื่องนี้ตรวจลายเซ็นไม่ได้" (`-10`) ตามตัวอย่าง `02_model_signature_hook.c`

### 3. secure boot ไม่ใช่การเข้ารหัสเฟิร์มแวร์

สองอย่างนี้ตอบคนละคำถาม

| | secure boot | การเข้ารหัสเฟิร์มแวร์ |
|---|---|---|
| ตอบคำถาม | โค้ดนี้มาจากเจ้าของกุญแจและไม่ถูกแก้ใช่ไหม | คนอื่นอ่านโค้ดนี้ได้ไหม |
| สมบัติ | ความถูกต้องและความแท้ (integrity, authenticity) | ความลับ (confidentiality) |
| เครื่องมือ | ลายเซ็นดิจิทัล ตรวจด้วยกุญแจสาธารณะที่อุปกรณ์เชื่อ | การเข้ารหัสแบบสมมาตร ต้องมีกุญแจลับบนอุปกรณ์ไว้ถอด |
| ไม่ได้ป้องกัน | คนอ่านโค้ดใน flash, บั๊กในโค้ดที่ลงนามแล้ว, การโจมตีตอนรัน | การรันโค้ดอื่นแทน ถ้าไม่มีการตรวจลายเซ็นร่วมด้วย |

ในแม่แบบนี้ไม่มีขั้นเข้ารหัส image ในไฟล์ config ทั้งสอง ดังนั้นแม้เปิด secure boot ใครอ่าน flash ได้ก็ยังอ่านโค้ดได้
ความลับที่ฝังอยู่ใน image (เช่นรหัสผ่านที่คอมไพล์ติด) ไม่ได้ถูก secure boot ปกป้องเลย นี่คืออีกเหตุผลของ ETSI ข้อ 5.4-3 ในบทเรียน 3.2

ข้อสังเกตเล็ก ๆ อีกข้อ config แบบลงนามใส่ `security-counter` เป็น `1` ซึ่งในรูปแบบของ MCUboot คือเลขที่ใช้กันการย้อนรุ่นของ image
เอกสารที่หลักสูตรนี้ตรวจไม่ได้ยืนยันว่า Extended Boot บังคับใช้เลขนี้อย่างไร จึงยังไม่นับเป็นมาตรการกันย้อนรุ่นของเฟิร์มแวร์ บทเรียน 4.2 จะดูการกันย้อนรุ่นที่ยืนยันได้ในชิป OPTIGA™

## ตัวอย่างสมบูรณ์

คอมเมนต์หัวไฟล์ของ [secure_boot_with_extended_boot.json](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/configs/secure_boot_with_extended_boot.json) บรรทัด 1–15
(TESAIoT PSE84 Dev Kit SDK, © Thai Embedded Systems Association, Apache-2.0)

```text
// Signed variant of boot_with_extended_boot.json — selected by SECURE_BOOT=1 in common.mk.
//
// Identical to boot_with_extended_boot.json except the CM33_S sign stage additionally
// carries "signing-key" + "security-counter", which turn the MCUboot metadata into a real
// OEM signature that Extended Boot verifies once the device is provisioned secure_boot=true.
//
// Geometry (header-size / fill-value / slot-size / hex-address) is intentionally IDENTICAL to
// the unsigned config — it is this project's real flashmap. Do NOT replace it with the values
// from mtb-example-psoc-edge-basic-secure-app (slot-size 0x80000, hardcoded 0x70100000).
//
// {{OEM_SIGNING_KEY}} is supplied by common.mk via:
//     MTB_COMBINE_SIGN_ARGS += -s OEM_SIGNING_KEY "$(SECURE_BOOT_KEY)"
// Override the key with:  make SECURE_BOOT=1 SECURE_BOOT_KEY=/abs/path/to/key.pem
// If you invoke run-config by hand you MUST pass -s OEM_SIGNING_KEY <path>; an unset
// variable is a hard error ("Unknown variable: OEM_SIGNING_KEY"), never a silent unsigned build.
```

อ่านแล้วตอบได้สามข้อ

1. **ต่างจากแบบไม่ลงนามแค่สองฟิลด์** คือ `"signing-key"` กับ `"security-counter"` ในขั้น sign ของ CM33_S ส่วนหัว MCUboot มีอยู่แล้วในทั้งสองแบบ
2. **ลายเซ็นมีความหมายเมื่ออุปกรณ์ provision แล้วเท่านั้น** บอร์ดที่ยังไม่ provision `secure_boot=true` ไม่ได้ตรวจลายเซ็นนี้
3. **ผู้เขียนออกแบบให้ "ล้มแบบมีเสียง"** ถ้าไม่ได้ส่งกุญแจ build ต้อง error ไม่ใช่ได้ image ที่ไม่ลงนามแบบเงียบ ๆ เป็นหลักเดียวกับที่ `common.mk` ไม่ยอมรับค่า `SECURE_BOOT` นอกจาก `0` กับ `1`

## ฝึกเติม

แต่ละข้อความต่อไปนี้ เป็นจริงกับ **secure boot** กับ **การเข้ารหัสเฟิร์มแวร์** กับ **ทั้งสอง** หรือ **ไม่ใช่ทั้งสอง**

1. ทำให้คู่แข่งที่ซื้อบอร์ดไปอ่าน flash แล้วไม่เข้าใจโค้ด ____
2. ทำให้บอร์ดที่ provision แล้วไม่บูต image ที่ลงนามด้วยกุญแจอื่น ____
3. กันบั๊ก buffer overflow ในโค้ดที่ลงนามถูกต้อง ____
4. ต้องมีกุญแจลับอยู่บนอุปกรณ์เพื่อใช้งาน ____
5. กันการเปลี่ยนเฟิร์มแวร์ CM55 ในแม่แบบนี้ แม้เปิด `SECURE_BOOT=1` และ provision แล้ว ____

<details><summary>เฉลย</summary>

1. **การเข้ารหัสเฟิร์มแวร์**
2. **secure boot**
3. **ไม่ใช่ทั้งสอง** โค้ดที่ลงนามแล้วยังมีบั๊กได้ ลายเซ็นบอกแค่ว่ามาจากใคร
4. **การเข้ารหัสเฟิร์มแวร์** ต้องมีกุญแจถอดรหัสบนอุปกรณ์ ส่วน secure boot ใช้แค่กุญแจสาธารณะในการตรวจ
5. **ไม่ใช่ทั้งสอง** ในแม่แบบนี้ลายเซ็นครอบแค่ image ของ CM33_S

</details>

## เช็กความเข้าใจ

คำถามข้างล่างเป็นส่วนหนึ่งของชุดเต็มใน [quiz.yaml](quiz.yaml) ซึ่งระบบตรวจอัตโนมัติใช้

1. ใน `proj_cm33_s/main.c` ของแม่แบบ CM33_S ทำอะไรก่อนเปิด CM33_NS *(เป้าหมายข้อ 1)*
   - ก) ตรวจลายเซ็นของ CM33_NS ด้วย OPTIGA™ Trust M
   - ข) `cybsp_init()` แล้วอ่าน stack pointer และ reset handler จากตาราง vector ของ CM33_NS แล้วกระโดดไป
   - ค) ถอดรหัส image ของ CM33_NS
   - ง) เชื่อมต่อ WiFi

   <details><summary>เฉลย</summary>

   **ข** ไม่มีการตรวจลายเซ็นในขั้นนี้ ห่วงโซ่ในแม่แบบจึงขาดหลัง CM33_S

   </details>

2. build ด้วย `SECURE_BOOT=1` แล้ว flash ลงบอร์ดที่ **ยังไม่** provision `secure_boot=true` ผลคืออะไร *(เป้าหมายข้อ 2)*
   - ก) บอร์ดไม่บูต
   - ข) Extended Boot ยังไม่ได้บังคับตรวจลายเซ็น การมีลายเซ็นจึงยังไม่ได้เพิ่มการป้องกัน
   - ค) ชิป OPTIGA ถูกล็อก
   - ง) LcsO เปลี่ยนเป็น operational

   <details><summary>เฉลย</summary>

   **ข** คอมเมนต์ใน config บอกว่า Extended Boot ตรวจลายเซ็นนี้ "once the device is provisioned secure_boot=true"

   </details>

3. ข้อใดอธิบายความต่างของ secure boot กับการเข้ารหัสเฟิร์มแวร์ได้ถูก *(เป้าหมายข้อ 3)*
   - ก) secure boot ซ่อนโค้ด การเข้ารหัสยืนยันว่าใครเขียน
   - ข) secure boot ยืนยันว่าโค้ดมาจากเจ้าของกุญแจและไม่ถูกแก้ การเข้ารหัสทำให้คนอื่นอ่านโค้ดไม่ได้
   - ค) ทั้งสองอย่างเหมือนกัน
   - ง) secure boot ต้องใช้กุญแจลับบนอุปกรณ์

   <details><summary>เฉลย</summary>

   **ข** ต้องใช้คู่กันถ้าต้องการทั้งความถูกต้องและความลับ แม่แบบนี้ไม่มีขั้นเข้ารหัส image

   </details>

## แล็บ

**อ่านห่วงโซ่ของบอร์ดตัวเองจากหลักฐาน** บทนี้ไม่ provision และไม่ flash image ที่ลงนาม

- [ ] **1. เทียบสอง config** จากโฟลเดอร์แม่แบบ
  ```bash
  diff configs/boot_with_extended_boot.json configs/secure_boot_with_extended_boot.json
  ```
  จดทุกบรรทัดที่ต่าง นอกจากคอมเมนต์แล้วเหลือกี่ฟิลด์ ตรงกับข้อ 1 ในตัวอย่างสมบูรณ์ไหม
- [ ] **2. พิสูจน์ว่าระบบ build ล้มแบบมีเสียง** สั่ง build ด้วยค่าที่ไม่ถูกต้อง แล้วจดข้อความ error
  ```bash
  make build SECURE_BOOT=yes
  ```
  เขียนหนึ่งประโยคว่าทำไมการที่คำสั่งนี้ **ล้ม** จึงเป็นเรื่องดี
- [ ] **3. นับว่าอะไรถูกลงนาม** เปิด `configs/secure_boot_with_extended_boot.json` หาทุก `"command"` แล้วเขียนตารางว่าไฟล์ hex ของแต่ละคอร์ผ่านขั้นไหนบ้าง (sign, hex-relocate, merge)
- [ ] **4. วาดห่วงโซ่ของคุณ** สองแบบ แบบบอร์ดที่คุณถืออยู่ตอนนี้ และแบบผลิตภัณฑ์ที่เปิด secure boot ครบ ทำเครื่องหมาย ✔ ✘ ทุกข้อต่อพร้อมหลักฐานหนึ่งบรรทัด (ไฟล์และบรรทัด)
- [ ] **5. อัปเดต threat model** ของบทเรียน 1.1 แถว T ที่เกี่ยวกับเฟิร์มแวร์ และแถว ETSI 5.7-1 ให้สะท้อนสิ่งที่พบ รวมถึงข้อที่ห่วงโซ่ขาดหลัง CM33_S
- [ ] **6. อ่านต่อ (ไม่ต้องทำ)** จาก README ของ [ตัวอย่าง basic secure app ของ Infineon](https://github.com/Infineon/mtb-example-psoc-edge-basic-secure-app) เขียนรายการขั้นตอนที่ต้องเกิดบนอุปกรณ์ก่อน Extended Boot จะเริ่มตรวจลายเซ็น และระบุว่าขั้นไหนที่คุณคิดว่าต้องมีคนอนุมัติก่อนทำ

## ไปต่อ

secure boot ตอบเรื่องเฟิร์มแวร์ตอนเปิดเครื่อง แต่ข้อมูลบางอย่างในชิป เช่นใบรับรองของอุปกรณ์ ต้องเปลี่ยนได้ตลอดอายุการใช้งาน
บทต่อไปดูว่า OPTIGA™ Trust M รับการเปลี่ยนแปลงนั้นอย่างไรโดยไม่เชื่อ host และกันการย้อนรุ่นอย่างไร

บทเรียนถัดไป: [บทเรียน 4.2: Protected Update](../l02-protected-update/README.md)

## สะท้อนคิด

- ในผลิตภัณฑ์ของคุณ ห่วงโซ่ความเชื่อใจขาดที่ข้อต่อไหน และใครบ้างที่เขียนข้อมูลลงส่วนที่ไม่ถูกตรวจได้
- ถ้ากุญแจ OEM ที่ใช้ลงนามหลุด คุณจะรู้ได้อย่างไร และจะทำอะไรต่อ
- ลูกค้าของคุณต้องการความลับของโค้ด หรือความถูกต้องของโค้ด หรือทั้งสองอย่าง

## แหล่งอ้างอิง

- [SDK: แม่แบบ mtb-only README (CM33_S secure boot)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/README.en.md)
- [B1 — CM33_NS boot walk-through (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__b1__cm33__boot.html)
- [SDK: common.mk (สวิตช์ SECURE_BOOT)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/common.mk)
- [SDK: configs/secure_boot_with_extended_boot.json](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/configs/secure_boot_with_extended_boot.json) และ [boot_with_extended_boot.json](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/configs/boot_with_extended_boot.json)
- [SDK: proj_cm33_s/main.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_s/main.c)
- [Infineon: PSOC™ Edge MCU basic secure application](https://github.com/Infineon/mtb-example-psoc-edge-basic-secure-app) (ลิงก์ ไม่ได้คัดลอก)
- [Infineon AN237849: Getting started with PSOC™ Edge security](https://www.infineon.com/AN237849)
- [PSA Certified](https://www.psacertified.org/)
- [ETSI EN 303 645 V3.1.3 (2024-09)](https://www.etsi.org/deliver/etsi_en/303600_303699/303645/03.01.03_60/en_303645v030103p.pdf) ข้อ 5.7
