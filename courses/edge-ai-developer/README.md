# Edge AI Developer: จากเซนเซอร์สู่โมเดลบนอุปกรณ์

> ดัดแปลงจาก Edge AI Developer, © 2026 รศ.วิรุฬห์ ศรีบริรักษ์ วิศวกรรมระบบสมองกลฝังตัว ภาควิชาวิศวกรรมไฟฟ้า คณะวิศวกรรมศาสตร์ มหาวิทยาลัยบูรพา (BUU) · BENTO & TESAIoT (CC BY 4.0 / MIT)

เรียน **Edge AI** แบบครบวงจรจากของจริงบนบอร์ด PSoC Edge (**TESAIoT Dev Kit**: Cortex-M33 + Cortex-M55 + Ethos-U55 NPU) ด้วย **MicroPython** เริ่มจากรันโมเดลที่มากับบอร์ดให้เห็นปลายทางก่อน แล้วเดินตามวงจรชีวิตของข้อมูลห้าเสา:

**เก็บข้อมูล (DAQ) → ประมวลผล → วิเคราะห์สัญญาณ → ฝึกโมเดล → แอป Edge AI**

ระหว่างทางคุณจะฝึกโมเดลของตัวเองบน PC แล้วพาไฟล์เดียวกันไปรันบน MCU เบราว์เซอร์ และ Cortex-A แกะสแตกใต้ฝากระโปรงจาก MicroPython ถึง NPU และปิดท้ายด้วย capstone ที่ส่งมอบได้จริง ทุกบทเรียนเดินตามแนว PRIMM คือเห็นของที่ทำงานได้ก่อน แล้วค่อยแกะ ดัดแปลง และสร้างเอง

## สำหรับใคร

- นักพัฒนาและผู้เรียนที่เขียน MicroPython และ Python ได้แล้ว (เช่นผ่านหลักสูตร AIoT in Action) และอยากทำ Edge AI บนอุปกรณ์จริง
- วิศวกรที่ต้องการเข้าใจทั้งเส้นทางตั้งแต่ข้อมูลดิบจนถึงโมเดลบน NPU ไม่ใช่แค่เรียก API
- ผู้สอนที่ต้องการชุดบทเรียนพร้อมสไลด์ โค้ด ไฟล์ฝึก และเฉลย

ไม่ต้องมีพื้นฐาน machine learning มาก่อน คณิตศาสตร์ที่ใช้ (ตรีโกณมิติ สถิติพื้นฐาน FFT softmax) อธิบายไว้ในสไลด์ทีละขั้น

## จบหลักสูตรแล้วทำอะไรได้

1. อธิบายวงจรชีวิตของข้อมูลห้าขั้นใน Edge AI และใช้โมดูล edge_ai เลือกโมเดลจากทะเบียน อ่าน verdict และต่อเข้ากับ action บนบอร์ดได้
2. เก็บข้อมูลเซนเซอร์ที่ติดป้ายลง CSV ที่อัตราสุ่มคงที่ และเตรียม dataset ที่สมดุล แบ่ง train/val/test แบบ stratified โดยไม่มีข้อมูลรั่ว
3. แปลงสัญญาณดิบเป็นปริมาณทางฟิสิกส์และ feature ด้วยฟิลเตอร์ FFT และหน้าต่างเลื่อน และวัดผลของแต่ละขั้นด้วยตัวเลข
4. ฝึกโมเดล Conv1D ใน Docker บีบเป็น int8 แล้ววัด accuracy และ latency บน PC เว็บ และ MCU ผ่าน Vela พร้อมพิสูจน์ parity ภายในเกณฑ์ TOL
5. สร้างแอป Edge AI ที่กัน false positive ด้วย CONF_FLOOR, debounce และ cooldown รวม verdict กับเซนเซอร์ดิบ และส่งเหตุการณ์ขึ้น MQTT
6. อธิบายสแตกจาก MicroPython ถึง NPU เพิ่มโมเดลเข้าเฟิร์มแวร์ และส่งมอบ capstone ที่ข้ามอย่างน้อยสามเสาพร้อมเหตุผลการออกแบบที่ยืนบนการวัด

## ต้องมีอะไรบ้าง

- **บอร์ด** TESAIoT Dev Kit (PSoC Edge E84) ที่ลงเฟิร์มแวร์ MicroPython ของ BENTO แล้ว — **หรือเริ่มได้โดยไม่มีบอร์ด** ด้วย BENTO Emulator (Emulator จำลองเซนเซอร์และผลโมเดล บางบทเรียนต้องใช้บอร์ดจริง ดูบรรทัด "อุปกรณ์" ในแต่ละบทเรียน)
- **BENTO IDE** — <https://ide.tesaiot.dev/> เขียนโค้ดแล้วกด **Program to Device** จากเบราว์เซอร์ และมี BENTO Emulator ในตัว
- **PC** ที่มี Python 3 กับ numpy (โมดูล 5) และ Docker สำหรับฝึกโมเดล หรือใช้ Google Colab แทน Docker ได้
- **WiFi** สำหรับบทเรียน 6.6 (ส่ง MQTT ไป broker สาธารณะ)
- **ModusToolbox** กับ [TESAIoT PSE84 DevKit SDK](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) ถ้าจะทำส่วนเพิ่มโมเดลเข้าเฟิร์มแวร์ในโมดูล 7
- สมุดหรือไฟล์สำหรับ **บันทึกการเรียน** ของตัวเอง สไลด์และแล็บบอกเป็นระยะว่าควรจดอะไร

## โครงหลักสูตร

แปดโมดูล 42 บทเรียน ราว 60 ชั่วโมงตามหลักสูตรต้นฉบับ (20 ชุด ชุดละราวสามชั่วโมง) ผลรวมเวลาโดยประมาณของทุกบทเรียนในคลังนี้คือราว 50 ชั่วโมง ส่วนที่เหลือคือเวลาเก็บข้อมูล ฝึกโมเดล และทำ capstone ซึ่งยืดหยุ่นตามผู้เรียน บทเรียนมาเป็นชุด บทเรียนแนวคิดตามด้วยบทเรียน **ลงมือทำ**

| โมดูล | บทเรียน | ชั่วโมง (ประมาณ) | เรื่อง |
|---|---|---|---|
| [โมดูล 1 — เริ่มต้น: รันของจริงแล้วแกะดูข้างใน](m01-onboarding/README.md) | 7 | 7.8 | รันโมเดล Edge AI ของจริงก่อน แล้วแกะแอปเซนเซอร์กับแอป Edge AI จนเห็นโครงร่วมสี่จังหวะ ทะเบียนโมเดล และเส้นทางจาก verdict สู่ action |
| [โมดูล 2 — เก็บข้อมูลจากเซนเซอร์ (DAQ)](m02-daq/README.md) | 4 | 4.5 | เก็บข้อมูลจากเซนเซอร์ให้ตรงกับที่โมเดลต้องการ อัตราสุ่ม Nyquist หน้าต่าง schema ของ CSV และการเก็บ IMU กับเสียงบนเส้นเวลาเดียว |
| [โมดูล 3 — ประมวลผลด้วยคณิตศาสตร์และฟิสิกส์](m03-processing/README.md) | 4 | 4.6 | แปลงตัวเลขดิบเป็นปริมาณทางฟิสิกส์ (มุมเอียง พลังงาน ความสูง dBFS) ค่าอนุพัทธ์อย่าง dew point กับ heat index และจำแนกด้วยกฎก่อนใช้ ML |
| [โมดูล 4 — วิเคราะห์สัญญาณ](m04-analysis/README.md) | 6 | 7.0 | ทำสัญญาณให้สะอาดด้วยฟิลเตอร์ DSP มองในโดเมนความถี่ด้วย FFT แล้วบีบหน้าต่างเลื่อนเป็น feature vector ที่โมเดลเห็นจริง |
| [โมดูล 5 — ฝึกโมเดลและนำไปใช้หลายเป้าหมาย](m05-training/README.md) | 9 | 10.7 | เตรียม dataset ที่สมดุล ฝึกโมเดลของเราเองใน Docker บีบเป็น int8 แล้วพาไฟล์เดียวไปรันบนเว็บ Cortex-A และ MCU ผ่าน Vela พร้อมวัด parity |
| [โมดูล 6 — แอป Edge AI](m06-apps/README.md) | 6 | 7.2 | สร้างแอปที่โฟกัสโมเดลเดียว ต่อ verdict เข้ากับ action ผ่านท่อที่กัน false positive รวมกับเซนเซอร์ดิบ และส่งเหตุการณ์ขึ้น MQTT |
| [โมดูล 7 — ใต้ฝากระโปรงและการต่อเติม](m07-under-the-hood/README.md) | 4 | 4.8 | แกะสแตกจาก MicroPython ข้าม IPC ไปถึง ai_engine และ NPU แล้วใช้แผนที่นั้นเพิ่มโมเดลของเราเองให้โผล่ใน edge_ai.models() |
| [โมดูล 8 — Capstone: แอป Edge AI ของเราเอง](m08-capstone/README.md) | 2 | 3.8 | ออกแบบ สร้าง และส่งมอบ Guardian แอป Edge AI ที่ร้อยสามเสาไว้ในลูปเดียว พร้อมเหตุผลการออกแบบที่ยืนบนการวัด |

<details><summary>รายชื่อบทเรียนทั้งหมด</summary>

**โมดูล 1 — เริ่มต้น: รันของจริงแล้วแกะดูข้างใน**

- [บทเรียน 1.1 — Edge AI คืออะไร: วงจรชีวิตของข้อมูลห้าขั้นและเป้าหมายที่โมเดลไปรันได้](m01-onboarding/l01-edge-ai-lifecycle/README.md)
- [บทเรียน 1.2 — โมดูล edge_ai: ถามทะเบียนโมเดล เลือก แล้วอ่านคำตอบ](m01-onboarding/l02-edge-ai-module/README.md)
- [บทเรียน 1.3 — ลงมือทำ: เมนูโมเดลตัวแรกของเรา](m01-onboarding/l03-first-inference-lab/README.md)
- [บทเรียน 1.4 — แกะแอปเซนเซอร์: โครงร่วมสี่จังหวะของทุกโปรแกรม](m01-onboarding/l04-sensor-app-anatomy/README.md)
- [บทเรียน 1.5 — ลงมือทำ: remix เป็น Tilt Monitor ของเรา](m01-onboarding/l05-sensor-remix-lab/README.md)
- [บทเรียน 1.6 — แกะแอป Edge AI: ทะเบียนโมเดล verdict และ action](m01-onboarding/l06-edge-ai-app-anatomy/README.md)
- [บทเรียน 1.7 — ลงมือทำ: จาก verdict สู่ action บนบอร์ด](m01-onboarding/l07-verdict-action-lab/README.md)

**โมดูล 2 — เก็บข้อมูลจากเซนเซอร์ (DAQ)**

- [บทเรียน 2.1 — สุ่มสัญญาณให้ตรงกับโมเดล: อัตราสุ่ม Nyquist หน้าต่าง และ schema ของ CSV](m02-daq/l01-sampling-and-schema/README.md)
- [บทเรียน 2.2 — ลงมือทำ: DAQ logger เก็บ dataset ลง CSV](m02-daq/l02-daq-logger-lab/README.md)
- [บทเรียน 2.3 — เสียงและหลายเซนเซอร์บนเส้นเวลาเดียว: PDM 16 kHz ประทับเวลา และ jitter](m02-daq/l03-audio-and-timeline/README.md)
- [บทเรียน 2.4 — ลงมือทำ: เก็บ IMU กับเสียงลงไฟล์เดียว](m02-daq/l04-multicapture-lab/README.md)

**โมดูล 3 — ประมวลผลด้วยคณิตศาสตร์และฟิสิกส์**

- [บทเรียน 3.1 — จากตัวเลขดิบสู่ปริมาณทางฟิสิกส์: มุมเอียง พลังงาน ความสูง และ dBFS](m03-processing/l01-physics-quantities/README.md)
- [บทเรียน 3.2 — ลงมือทำ: เกจฟิสิกส์สี่ตัวบนจอ](m03-processing/l02-physics-gauges-lab/README.md)
- [บทเรียน 3.3 — ค่าอนุพัทธ์และการจำแนกด้วยกฎ: dew point, heat index และบันไดกฎ](m03-processing/l03-rules-before-ml/README.md)
- [บทเรียน 3.4 — ลงมือทำ: ตัวจำแนกความสบายด้วยกฎ](m03-processing/l04-rule-classifier-lab/README.md)

**โมดูล 4 — วิเคราะห์สัญญาณ**

- [บทเรียน 4.1 — ฟิลเตอร์ DSP: EMA, Median, Kalman และ radar range profile](m04-analysis/l01-dsp-filters/README.md)
- [บทเรียน 4.2 — ลงมือทำ: ฟิลเตอร์ทำสัญญาณให้สะอาดสด ๆ](m04-analysis/l02-filters-lab/README.md)
- [บทเรียน 4.3 — FFT และโดเมนความถี่: bin, Nyquist, DC, leakage และ Hann window](m04-analysis/l03-fft-frequency-domain/README.md)
- [บทเรียน 4.4 — ลงมือทำ: สเปกตรัมสดจาก IMU](m04-analysis/l04-fft-spectrum-lab/README.md)
- [บทเรียน 4.5 — feature และหน้าต่าง: สิ่งที่โมเดลเห็นจริง](m04-analysis/l05-features-and-windowing/README.md)
- [บทเรียน 4.6 — ลงมือทำ: feature vector จากหน้าต่างเลื่อน](m04-analysis/l06-windowing-lab/README.md)

**โมดูล 5 — ฝึกโมเดลและนำไปใช้หลายเป้าหมาย**

- [บทเรียน 5.1 — วิศวกรรมชุดข้อมูล: สมดุลคลาส หน้าต่าง และการแบ่ง train/val/test](m05-training/l01-dataset-engineering/README.md)
- [บทเรียน 5.2 — ลงมือทำ: เก็บ dataset ที่สมดุลบนบอร์ดแล้วแบ่งบน PC](m05-training/l02-dataset-lab/README.md)
- [บทเรียน 5.3 — ฝึกโมเดลใน Docker: หนึ่งชิ้นงาน สี่เป้าหมาย](m05-training/l03-training-pipeline/README.md)
- [บทเรียน 5.4 — ข้างในการฝึก: Keras, Conv1D, gradient descent, int8 และ confusion matrix](m05-training/l04-inside-training/README.md)
- [บทเรียน 5.5 — ลงมือทำ: เติมสคริปต์ฝึกแล้วรันใน Docker](m05-training/l05-train-lab/README.md)
- [บทเรียน 5.6 — รันโมเดลบนเว็บ: LiteRT.js, int8 I/O และ parity](m05-training/l06-web-runtime/README.md)
- [บทเรียน 5.7 — ลงมือทำ: verdict บนเว็บให้ตรงกับ PC และเรื่องราว Cortex-A](m05-training/l07-web-parity-lab/README.md)
- [บทเรียน 5.8 — quantize และ Vela: เอาโมเดลของเราขึ้น Ethos-U55](m05-training/l08-quantize-and-vela/README.md)
- [บทเรียน 5.9 — ลงมือทำ: เทียบสามเป้าหมาย MCU, Web และ PC](m05-training/l09-three-targets-lab/README.md)

**โมดูล 6 — แอป Edge AI**

- [บทเรียน 6.1 — หกโมเดลกับ edge_ai API: แอปที่โฟกัสโมเดลเดียว](m06-apps/l01-focused-apps/README.md)
- [บทเรียน 6.2 — ลงมือทำ: แอปโฟกัสของเราเอง](m06-apps/l02-focused-app-lab/README.md)
- [บทเรียน 6.3 — ท่อสั่งการ: CONF_FLOOR, debounce, cooldown และ on_result](m06-apps/l03-action-pipeline/README.md)
- [บทเรียน 6.4 — ลงมือทำ: action pipeline ที่กัน false positive](m06-apps/l04-action-pipeline-lab/README.md)
- [บทเรียน 6.5 — sensor fusion: verdict ของโมเดลกับเซนเซอร์ดิบ](m06-apps/l05-sensor-fusion/README.md)
- [บทเรียน 6.6 — ลงมือทำ: ส่งเหตุการณ์ที่ fuse แล้วขึ้น MQTT](m06-apps/l06-fusion-iot-lab/README.md)

**โมดูล 7 — ใต้ฝากระโปรงและการต่อเติม**

- [บทเรียน 7.1 — สแตก Edge AI: tri-core, ai_engine, IPC model link และ TFLite-Micro](m07-under-the-hood/l01-edge-ai-stack/README.md)
- [บทเรียน 7.2 — ลงมือทำ: ส่องสแตกจาก MicroPython](m07-under-the-hood/l02-trace-the-stack-lab/README.md)
- [บทเรียน 7.3 — เพิ่มโมเดลของเราเอง: สามการแก้ สัญญาสี่ฟังก์ชัน และ Vela](m07-under-the-hood/l03-add-your-own-model/README.md)
- [บทเรียน 7.4 — ลงมือทำ: ให้โมเดลใหม่โผล่ใน edge_ai.models()](m07-under-the-hood/l04-extend-model-lab/README.md)

**โมดูล 8 — Capstone: แอป Edge AI ของเราเอง**

- [บทเรียน 8.1 — ออกแบบ capstone: Guardian สามเสาในไฟล์เดียว](m08-capstone/l01-capstone-design/README.md)
- [บทเรียน 8.2 — ลงมือทำ: สร้างและส่งมอบแอป Edge AI](m08-capstone/l02-capstone-build-lab/README.md)

</details>

## ในแต่ละบทเรียนมีอะไร

| ไฟล์ | คืออะไร |
|---|---|
| `README.md` | เป้าหมาย สิ่งที่ต้องเตรียม แนวคิดโดยย่อ รายชื่อไฟล์โค้ด แล็บ และเช็กความเข้าใจ |
| `slides.md` | สไลด์ของบทเรียน (Marp) |
| `examples/` | ตัวอย่างและฉบับเต็มที่รันได้ทันที |
| `practice/` | ไฟล์ฝึก มีช่องว่าง `# เติม` ให้เติมเอง (บทเรียนลงมือทำ) |
| `solution/` | เฉลย ชื่อไฟล์ตรงกับไฟล์ฝึก |
| `quiz.yaml` | คำถามเช็กความเข้าใจ ผูกกับเป้าหมายแต่ละข้อ |

วิธีรันโค้ด MicroPython: เปิดไฟล์ใน BENTO IDE แล้วกด **Program to Device** (บอร์ด) หรือ **Run** (BENTO Emulator) · ไฟล์โค้ดขึ้นต้นด้วยเลขชุดเดิม เช่น `s11_dataset.py` ตามลำดับสไลด์ของต้นฉบับ

เครื่องมือฝั่ง PC ของโมดูล 5 อยู่ใน [`shared/training/`](shared/training/README.md) (`dataset_tools.py`, `train.py`, `eval_pc.py`, `convert_web.py`, `quantize_vela.sh`, `Dockerfile` และ notebook สำหรับ Colab) · หน้าเล่นคณิตแบบโต้ตอบ [`shared/interactive/math_lab.html`](shared/interactive/math_lab.html) ต้องดาวน์โหลดมาเปิดในเบราว์เซอร์ (ต้องต่อเน็ตเพื่อโหลด GeoGebra)

## ข้อจำกัดที่ควรรู้

- **BENTO Emulator** จำลองเซนเซอร์และผลของโมเดล (ยกเว้นโมเดล Motion ที่เปิดสวิตช์ REAL แล้วรันผ่าน ONNX Runtime Web) ไม่มีโมเดล Push แผง HW ขยับเฉพาะ accel และโมเดลเสียงไม่ชนะคลาส unlabelled ตัวเลข latency และเสียงจริงต้องดูบนบอร์ด
- โมเดล Cough, Alarm และ Siren เป็น DEEPCRAFT Ready-Model ของ Imagimob AB บริษัทในเครือ Infineon ใช้ได้เพื่อประเมินผลเท่านั้น และจำกัดจำนวนครั้งอนุมาน โมเดล Motion, Baby Cry และ Push เป็น export จาก DEEPCRAFT Studio ของ Imagimob เช่นกัน ไม่มีไฟล์โมเดลเหล่านี้อยู่ในคลังนี้
- บน TESAIoT Dev Kit การเปิดไมโครโฟน PDM จาก MicroPython ยังชนกับ clock ของระบบเสียง ตัวอย่างที่อ่านเสียงดิบเอง (บทเรียน 2.3–2.4 และตัวอย่าง 10) ผู้เขียนทดสอบบน PSoC Edge AI Kit ส่วนโมเดลเสียงผ่าน `edge_ai` ใช้ได้
- ซอร์สเฟิร์มแวร์ BENTO และเอกสารสถาปัตยกรรมภายในที่โมดูล 7 อ้างถึงยังไม่เปิดเผย ส่วนที่ตรวจได้คือ header และเอกสารใน [SDK สาธารณะ](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk) ซึ่งมีทางเพิ่มโมเดลด้วย `ai_engine_register()` แทนการแก้ `ai_engine.c`

## ต่างจากต้นฉบับ

หลักสูตรนี้ดัดแปลงจากสไลด์ 20 ชุดของ Edge AI Developer ข้อเท็จจริงที่ไม่ตรงกับ SDK สาธารณะ กับ BENTO Emulator
หรือกับผลการรันเครื่องมือซ้ำ ได้แก้ในบทเรียนแล้ว ข้อหลัก ๆ คือ

- `motion()` คืนค่าเป็น m/s² สูตรพลังงานจึงหารด้วย 9.81 และ pitch ใช้ `atan2(−ax, …)`
- `dataset_tools.py` ให้ 143 หน้าต่าง แบ่งเป็น 101/21/21 (ต้นฉบับเขียน 142 และ 100/22/22) และสูตรแบ่งชุดข้อมูลตรงกับ `split()`
- ถ้าลืม `representative_dataset` ตอนแปลงเป็น int8 จะเกิด ValueError ไม่ได้แค่ความแม่นยำลดลงเงียบ ๆ
- Emulator มีโมเดล 5 ตัว (ไม่มี Push) ผลของโมเดลเป็นการจำลอง ยกเว้นโมเดล Motion ที่รันจริงผ่าน ONNX Runtime Web และโหลดโมเดลของผู้เรียนไม่ได้
  แล็บเทียบผลบนเว็บจึงรันในหน้าเว็บของผู้เรียนเอง
- เฟิร์มแวร์ `wifi` ไม่มี `rssi()` ตัวอย่างจึงอ่าน `status()["rssi"]` และอาร์กิวเมนต์ของ `ui.tone` คือ (note, wave, velocity, ms)
- การอ้างถึงเอกสารภายในที่ยังไม่เปิดเผย เปลี่ยนเป็น header และเอกสารใน SDK สาธารณะ
- `train.py` เพิ่มตัวเลือก `--save-keras` ที่ `convert_web.py` ต้องใช้

ตัวเลขความแม่นยำและ latency ในบทเรียนเป็นของผู้เขียน ยังไม่ได้วัดซ้ำบนบอร์ด

## วิธีใช้เฉลย

เฉลยเปิดให้ดูได้โดยตั้งใจ แต่มีไว้ให้ **เทียบหลังจากพยายามเองแล้ว** ไม่ได้มีไว้คัดลอกวาง

1. **ลองเองก่อนอย่างน้อย 15 นาที** อ่านคำใบ้ `# เติม` ในไฟล์ฝึก เติมแล้วรันดูผลจริง ถ้า error ให้อ่านข้อความ error ให้จบก่อน
2. **เปิดเฉลยอ่าน แล้วปิด** อ่านให้เข้าใจว่าทำไมเขียนแบบนั้น แล้วปิดไฟล์เฉลยก่อนกลับไปแก้ไฟล์ของตัวเอง
3. **พิมพ์เอง ไม่วาง** นิ้วที่พิมพ์เองกับตาที่คัดลอกจำคนละแบบกัน
4. **เปลี่ยนตัวเลขแล้วดูผล** เช่นเกณฑ์ความมั่นใจ ขนาดหน้าต่าง หรือจำนวน epoch การรู้ว่า "ถ้าแก้ตรงนี้จะเกิดอะไร" คือความเข้าใจจริง

## สัญญาอนุญาต

- **เนื้อหา** (สไลด์ README ภาพที่วาดเองและภาพหน้าจอ) — CC BY 4.0
- **โค้ด** (`examples/`, `practice/`, `solution/`, `shared/`) และไฟล์โมเดลอ้างอิง `shared/training/model_int8.tflite` — MIT, Copyright (c) 2026 Wiroon Sriborrirux (ข้อความสัญญาอนุญาตเต็มอยู่ที่ `LICENSES/MIT.txt` ของรีโพ)
- **ภาพจากบุคคลที่สาม** — ใช้ตามสัญญาอนุญาตของแต่ละภาพ รายชื่อผู้สร้าง แหล่งที่มา และสัญญาอนุญาตอยู่ใน [credits.yaml](credits.yaml)
- **โมเดล DEEPCRAFT** ที่บอร์ดใช้เป็นของ Imagimob AB (บริษัทในเครือ Infineon Technologies) สัญญาอนุญาตของคลังนี้ไม่ครอบคลุมโมเดลเหล่านั้น

## ที่มา

หลักสูตรนี้ดัดแปลงจากหลักสูตร **Edge AI Developer** ของ รศ.วิรุฬห์ ศรีบริรักษ์ วิศวกรรมระบบสมองกลฝังตัว ภาควิชาวิศวกรรมไฟฟ้า คณะวิศวกรรมศาสตร์ มหาวิทยาลัยบูรพา (BUU) (ฉบับ 2026-09) โดยแบ่งสไลด์ 20 ชุดเป็น 42 บทเรียน จัดเป็นแปดโมดูล ตรวจข้อเท็จจริงกับเฟิร์มแวร์ BENTO, BENTO Emulator และ SDK สาธารณะ และปรับถ้อยคำให้เหมาะกับผู้เรียนทั่วไป · BENTO & TESAIoT

## อ้างอิง TESA

เมื่อนำหลักสูตรนี้หรือบางส่วนไปใช้ ดัดแปลง หรือเผยแพร่ต่อ กรุณาอ้างอิงตามนี้ (ถ้าดัดแปลง ให้เติม «(ดัดแปลง)» ต่อท้ายชื่อ และคงเครดิตผู้เขียนต้นฉบับไว้ด้วย):

> "Edge AI Developer: จากเซนเซอร์สู่โมเดลบนอุปกรณ์" จาก TESA Open Knowledge โดยสมาคมสมองกลฝังตัวไทย (Thai Embedded Systems Association: TESA) https://github.com/tesaiot/tesa-qualification-program สัญญาอนุญาต CC BY 4.0 · ดัดแปลงจาก Edge AI Developer, © 2026 รศ.วิรุฬห์ ศรีบริรักษ์ วิศวกรรมระบบสมองกลฝังตัว ภาควิชาวิศวกรรมไฟฟ้า คณะวิศวกรรมศาสตร์ มหาวิทยาลัยบูรพา (BUU) · BENTO & TESAIoT (CC BY 4.0 / MIT)

การอ้างอิงไม่ได้แปลว่า TESA หรือ Infineon รับรองหลักสูตรหรือผลงานที่นำไปใช้ต่อ ชื่อ TESA, TQP และ "Certified by TESA and Infineon" เป็นเครื่องหมายของโครงการ
