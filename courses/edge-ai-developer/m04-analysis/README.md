# โมดูล 4 — วิเคราะห์สัญญาณ

> Signal analysis · [หน้าหลักสูตร](../README.md)

ทำสัญญาณให้สะอาดด้วยฟิลเตอร์ DSP มองในโดเมนความถี่ด้วย FFT แล้วบีบหน้าต่างเลื่อนเป็น feature vector ที่โมเดลเห็นจริง

## เป้าหมายของโมดูล

เข้าใจว่าโมเดลไม่เคยเห็นสัญญาณดิบ มันเห็น feature ที่ front-end เตรียมให้ และ front-end นั้นต้องตรงกันทุกที่

## บทเรียน

| บทเรียน | เรื่อง | เวลา (นาที) | สไลด์ |
|---|---|---|---|
| [4.1](l01-dsp-filters/README.md) | ฟิลเตอร์ DSP: EMA, Median, Kalman และ radar range profile | 65 | [slides.md](l01-dsp-filters/slides.md) |
| [4.2](l02-filters-lab/README.md) | ลงมือทำ: ฟิลเตอร์ทำสัญญาณให้สะอาดสด ๆ | 75 | [slides.md](l02-filters-lab/slides.md) |
| [4.3](l03-fft-frequency-domain/README.md) | FFT และโดเมนความถี่: bin, Nyquist, DC, leakage และ Hann window | 65 | [slides.md](l03-fft-frequency-domain/slides.md) |
| [4.4](l04-fft-spectrum-lab/README.md) | ลงมือทำ: สเปกตรัมสดจาก IMU | 75 | [slides.md](l04-fft-spectrum-lab/slides.md) |
| [4.5](l05-features-and-windowing/README.md) | feature และหน้าต่าง: สิ่งที่โมเดลเห็นจริง | 65 | [slides.md](l05-features-and-windowing/slides.md) |
| [4.6](l06-windowing-lab/README.md) | ลงมือทำ: feature vector จากหน้าต่างเลื่อน | 75 | [slides.md](l06-windowing-lab/slides.md) |

บทเรียนมาเป็นชุด บทเรียนแนวคิดตามด้วยบทเรียน **ลงมือทำ** ที่มีไฟล์ฝึก เฉลย และแล็บ

## เช็กพอยต์ของโมดูล

ผ่านโมดูลนี้เมื่อทำได้ครบทุกข้อ (รายละเอียดอยู่ในหัวข้อ **แล็บ** ของบทเรียนลงมือทำ):

- [ ] ฟิลเตอร์ปรับสัญญาณเซนเซอร์ที่มี noise ให้ดีขึ้นอย่างเห็นได้ เส้น Filtered เรียบกว่า Raw ชัดเจน พร้อมตัวเลข noise down % ยืนยัน (บทเรียน 4.2)
- [ ] รัน `s09_fft_spectrum.py` แล้วอ่านสเปกตรัมสดออก แท่งความถี่และ peak (Hz) เปลี่ยนตามการเขย่าเร็วหรือช้าจริง (บทเรียน 4.4)
- [ ] สร้าง feature vector จากสัญญาณดิบด้วยมือเอง ตัดหน้าต่าง (window + hop) แล้วบีบเป็น mean, std และ band ที่เปลี่ยนตามการเคลื่อนไหว (บทเรียน 4.6)
