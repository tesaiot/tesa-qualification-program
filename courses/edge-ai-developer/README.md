# Edge AI Developer: จากเซนเซอร์สู่โมเดลบนอุปกรณ์

ระดับ **L3** · สถานะ **pre-alpha (โครงร่าง อยู่ระหว่างเขียน)** · 7 โมดูล 20 บทเรียน · ประมาณ 40 ชั่วโมง

**หลักสูตรเต็มจะเผยแพร่เมื่อผู้เขียนเปิดให้** หลักสูตรต้นฉบับ Edge AI Developer มีครบทั้งสไลด์และโค้ดแล้ว และอยู่ระหว่างการตรวจทานของผู้เขียน
หน้านี้จึงเผยแพร่เฉพาะโครงร่าง คือชื่อโมดูลและบทเรียน เป้าหมายที่เขียนใหม่สำหรับคลังนี้ ทักษะที่พัฒนา และแหล่งอ้างอิงสาธารณะที่ตรวจแล้ว
ไม่มีสไลด์หรือโค้ดจากต้นฉบับอยู่ในโฟลเดอร์นี้

หลักสูตรเดินตามวงจรชีวิตของข้อมูลจริงห้าเสาหลัก **เก็บข้อมูล (DAQ) → ประมวลผล → วิเคราะห์สัญญาณ → ฝึกโมเดล → แอป Edge AI**
เรียนด้วย MicroPython บนบอร์ด TESAIoT Dev Kit เป็นหลัก ใช้ BENTO Emulator ในบทที่ไม่ต้องใช้ฮาร์ดแวร์จริง และฝึกโมเดลบนเครื่อง PC
เริ่มจากแกะแอปที่ทำงานได้แล้ว (แนวทางเดียวกับ PRIMM) ก่อนสร้างของตัวเอง

## เหมาะกับใคร

- นักพัฒนาและนักศึกษาที่ผ่านหลักสูตร AIoT in Action หรือเขียน MicroPython และ Python ได้แล้ว
- ไม่ต้องมีพื้นฐาน machine learning มาก่อน
- ต้องมีบอร์ด TESAIoT Dev Kit สำหรับบทที่ใช้ไมโครโฟน เรดาร์ และ NPU และเครื่อง PC สำหรับฝึกโมเดล

## เมื่อจบหลักสูตร คุณจะทำได้

1. อธิบายวงจรชีวิตของข้อมูลใน Edge AI ห้าขั้น และบอกได้ว่าโจทย์หนึ่งควรใช้โมเดลบนอุปกรณ์หรือกฎธรรมดา
2. เก็บข้อมูลจากเซนเซอร์หลายตัวบนเส้นเวลาเดียวกัน และเตรียมเป็นชุดข้อมูลที่ติดป้ายและแบ่งส่วนถูกต้อง
3. ประมวลผลและวิเคราะห์สัญญาณด้วยฟิลเตอร์ FFT และการแบ่งหน้าต่าง เพื่อสร้าง feature ที่โมเดลใช้
4. ฝึกโมเดลขนาดเล็ก แปลงให้ใช้ได้บนหลายเป้าหมาย และเทียบผลบนเครื่อง PC เว็บ และบอร์ด
5. สร้างแอป Edge AI ที่ลงมือทำตามผลของโมเดลอย่างเชื่อถือได้ และส่งเหตุการณ์ขึ้นแพลตฟอร์ม IoT

## โมดูลและบทเรียน

### [โมดูล 1 · เริ่มต้นและแกะแอปที่ทำงานได้](m01-onboarding/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| edgeai-dev.m01.l01 | [Edge AI และวงจรชีวิตของข้อมูล](m01-onboarding/l01-edge-ai-lifecycle/README.md) | 70 นาที |
| edgeai-dev.m01.l02 | [แกะแอปเซนเซอร์ทีละส่วน](m01-onboarding/l02-reverse-engineer-sensor-app/README.md) | 70 นาที |
| edgeai-dev.m01.l03 | [แกะแอป Edge AI](m01-onboarding/l03-reverse-engineer-edge-ai-app/README.md) | 70 นาที |

### [โมดูล 2 · เก็บข้อมูลจากเซนเซอร์ (DAQ)](m02-daq/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| edgeai-dev.m02.l01 | [อัตราสุ่มตัวอย่างและการบันทึกข้อมูล](m02-daq/l01-sampling-and-logging/README.md) | 70 นาที |
| edgeai-dev.m02.l02 | [เก็บเสียงและหลายเซนเซอร์บนเส้นเวลาเดียว](m02-daq/l02-audio-and-multisensor-capture/README.md) | 70 นาที |

### [โมดูล 3 · ประมวลผลด้วยคณิตศาสตร์และฟิสิกส์](m03-processing/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| edgeai-dev.m03.l01 | [คณิตศาสตร์ ฟิสิกส์ และการแสดงผล](m03-processing/l01-physics-and-visualisation/README.md) | 70 นาที |
| edgeai-dev.m03.l02 | [ตัวชี้วัดที่คำนวณได้และการจำแนกด้วยกฎ](m03-processing/l02-rule-based-classification/README.md) | 70 นาที |

### [โมดูล 4 · วิเคราะห์สัญญาณ](m04-analysis/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| edgeai-dev.m04.l01 | [ฟิลเตอร์ DSP](m04-analysis/l01-dsp-filtering/README.md) | 70 นาที |
| edgeai-dev.m04.l02 | [FFT และโดเมนความถี่](m04-analysis/l02-fft-frequency-domain/README.md) | 70 นาที |
| edgeai-dev.m04.l03 | [Feature และการแบ่งหน้าต่าง](m04-analysis/l03-features-and-windowing/README.md) | 70 นาที |

### [โมดูล 5 · ฝึกโมเดลและนำไปใช้หลายเป้าหมาย](m05-training/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| edgeai-dev.m05.l01 | [วิศวกรรมชุดข้อมูล](m05-training/l01-dataset-engineering/README.md) | 70 นาที |
| edgeai-dev.m05.l02 | [ฝึกโมเดลด้วย TensorFlow](m05-training/l02-train-in-tensorflow/README.md) | 70 นาที |
| edgeai-dev.m05.l03 | [นำโมเดลขึ้นเว็บ และเรื่องของคอมพิวเตอร์ Linux ขนาดเล็ก](m05-training/l03-deploy-to-web/README.md) | 70 นาที |
| edgeai-dev.m05.l04 | [Quantize และรันบน NPU](m05-training/l04-quantize-to-npu/README.md) | 70 นาที |

### [โมดูล 6 · แอป Edge AI](m06-apps/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| edgeai-dev.m06.l01 | [โมเดลที่มีอยู่และ API ของ edge_ai](m06-apps/l01-models-and-edge-ai-api/README.md) | 70 นาที |
| edgeai-dev.m06.l02 | [ท่อการกระทำ (action pipeline)](m06-apps/l02-action-pipelines/README.md) | 70 นาที |
| edgeai-dev.m06.l03 | [รวมหลายแหล่งข้อมูลและส่งขึ้น IoT](m06-apps/l03-sensor-fusion-iot/README.md) | 70 นาที |

### [โมดูล 7 · ใต้ฝากระโปรง ต่อเติม และงานปลายทาง](m07-under-the-hood/README.md)

| บทเรียน | เรื่อง | เวลา |
|---|---|---|
| edgeai-dev.m07.l01 | [สแตก Edge AI ใต้ฝากระโปรง](m07-under-the-hood/l01-edge-ai-stack/README.md) | 70 นาที |
| edgeai-dev.m07.l02 | [ต่อเติมด้วยโมเดลของตัวเอง](m07-under-the-hood/l02-extend-with-your-own-model/README.md) | 70 นาที |
| edgeai-dev.m07.l03 | [งานปลายทาง: แอป Edge AI ครบวงจร](m07-under-the-hood/l03-capstone/README.md) | 75 นาที |

## สถานะของหลักสูตร

สถานะ pre-alpha โครงร่างเท่านั้น ทุกบทเรียนมีเป้าหมาย ทักษะ และแหล่งอ้างอิงสาธารณะ ยังไม่มีเนื้อหา แบบฝึก และเช็กความเข้าใจ
เนื้อหาเต็ม สไลด์ และโค้ด จะเพิ่มเข้ามาเมื่อผู้เขียนเปิดเผยหลักสูตรต้นฉบับ
แหล่งอ้างอิงฝั่งภาษา C ลิงก์ไปยัง SDK ที่ commit `ef72c1b` และตัวอย่าง MicroPython ด้าน DSP ลิงก์ไปยังหลักสูตร AIoT in Action (MIT) ที่ commit ที่ตรึงไว้

## แหล่งอ้างอิงหลัก

- [SDK: แคตตาล็อกตัวอย่าง (หมวด edge_ai)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/README.en.md)
- [Edge AI: Engine lifecycle (เอกสาร SDK สร้างจาก commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__edge__ai__lifecycle.html)
- [TESAIoT PSE84 Dev Kit SDK README (ฮาร์ดแวร์โดยย่อ: Cortex-M55, Ethos-U55 NPU, เซนเซอร์)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/README.md)
- [TensorFlow](https://www.tensorflow.org/)
- [LiteRT (เดิมชื่อ TensorFlow Lite) documentation](https://ai.google.dev/edge/litert)
- [TensorFlow Lite for Microcontrollers (tflite-micro)](https://github.com/tensorflow/tflite-micro)
- [Arm Ethos-U Vela compiler (PyPI: ethos-u-vela)](https://pypi.org/project/ethos-u-vela/)

## สัญญาอนุญาต

- เนื้อหา (โครงร่างนี้) CC BY 4.0
- โค้ดใหม่ที่จะเพิ่มในหลักสูตรนี้ Apache-2.0
- ยังไม่มีโค้ดหรือสไลด์จากหลักสูตรต้นฉบับในโฟลเดอร์นี้

## อ้างอิง TESA

เมื่อนำหลักสูตรนี้ไปใช้ แบ่งปัน หรือดัดแปลง ต้องอ้างอิงดังนี้

> "Edge AI Developer: จากเซนเซอร์สู่โมเดลบนอุปกรณ์" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0

ถ้าแก้ไขเนื้อหา ให้เติม **(ดัดแปลง)** ต่อท้ายข้อความอ้างอิง พร้อมบอกสั้น ๆ ว่าเปลี่ยนอะไร
การอ้างอิงไม่ได้แปลว่า TESA รับรองงานของคุณ รายละเอียดและตัวอย่างอยู่ใน [ATTRIBUTION.md](../../ATTRIBUTION.md)
