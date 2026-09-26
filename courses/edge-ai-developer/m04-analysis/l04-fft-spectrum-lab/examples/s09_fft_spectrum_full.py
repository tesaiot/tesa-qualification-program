# s09_fft_spectrum_full.py - สเปกตรัม FFT สด ๆ จาก IMU (ฉบับเต็ม)
# วิธีรัน: เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator (ide.tesaiot.dev)
#          กด "Program to Device" แล้วเขย่าบอร์ดแกน Z เร็ว-ช้าสลับกัน
#
# ฉบับนี้คือเวอร์ชันที่ขัดจนเรียบร้อยของ s09_fft_spectrum.py — pipeline สี่ขั้นเดียวกับ
# ที่คุณเติมในไฟล์ฝึก (ตัด DC -> Hann window -> magnitude -> peak) แต่เพิ่มรายละเอียด
# ที่ทำให้ "อ่านสเปกตรัมได้นิ่งขึ้น": เฉลี่ยสเปกตรัมแบบ EMA ให้แท่งไม่กระตุก, โชว์
# ความถี่เด่นเป็นตัวเลขใหญ่ (Seg7), ค้างยอดสูงสุด (peak-hold) และวัดพลังงานรวม (RMS)

import ui
ui.screen()
import lcd
import sensors
import time
import math

N = 32                 # จุดต่อหน้าต่าง ต้องเป็นเลขยกกำลัง 2 (radix-2)
FS = 50.0              # อัตราสุ่ม ~50 Hz -> Nyquist = 25 Hz, bin width = FS/N
HALF = N // 2          # bin ความถี่บวก
SMOOTH = 0.5           # ค่าถ่วง EMA ของสเปกตรัม (0 = ไม่เฉลี่ย, ใกล้ 1 = นิ่งแต่หน่วง)

GREEN = 0x50D890       # bin เด่น + ความถี่เด่น
AMBER = 0xE0A03A       # peak-hold (ยอดสูงสุดที่เคยเห็น)
DIM   = 0x2A4A44       # bin อื่น ๆ
CYAN  = 0x71C7EC       # หัวข้อ / ป้าย Hz
SEC   = 0xCFC6BF       # ข้อความรอง


def fft(re, im):
    """in-place iterative radix-2 FFT (Cooley-Tukey). re/im = list ยาว N (im เริ่ม 0).
    หัวใจ: ถามสัญญาณว่ามีคลื่นไซน์ความถี่ไหนซ่อนอยู่ แต่ละอันแรงแค่ไหน แล้วตอบเป็น
    เลขเชิงซ้อนต่อ bin โดยใช้เวลาแค่ N log N (เร็วกว่า DFT ตรง ๆ ที่ใช้ N^2)"""
    n = len(re)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            re[i], re[j] = re[j], re[i]
            im[i], im[j] = im[j], im[i]
    length = 2
    while length <= n:
        ang = -2.0 * math.pi / length
        wr, wi = math.cos(ang), math.sin(ang)
        for start in range(0, n, length):
            cr, ci = 1.0, 0.0
            for k in range(length >> 1):
                a = start + k
                b = a + (length >> 1)
                tr = cr * re[b] - ci * im[b]
                ti = cr * im[b] + ci * re[b]
                re[b] = re[a] - tr
                im[b] = im[a] - ti
                re[a] += tr
                im[a] += ti
                cr, ci = cr * wr - ci * wi, cr * wi + ci * wr
        length <<= 1
    return re, im


# เตรียม Hann window ครั้งเดียว (คงที่ต่อ N) — ไม่ต้องคำนวณ cos ใหม่ทุกเฟรม
HANN = [0.5 - 0.5 * math.cos(2 * math.pi * i / (N - 1)) for i in range(N)]

lcd.clear()
lcd.console('<h2> FFT Spectrum - โดเมนความถี่ (ฉบับเต็ม)</h2>')
lcd.console(' N=%d, FS=%.0f Hz -> bin width = %.2f Hz, Nyquist = %.0f Hz'
            % (N, FS, FS / N, FS / 2))

# ---- สร้าง widget ครั้งเดียวก่อนลูป ----
ui.Label("FFT Spectrum", x=20, y=8, color=CYAN)
seg = ui.Seg7("--", x=210, y=6, color=GREEN)          # ความถี่เด่นตัวใหญ่ (Hz)
ui.Label("Hz", x=330, y=24, color=SEC)
rms_lbl = ui.Label("energy: -- ", x=380, y=14, color=CYAN)
info = ui.Label("เขย่าแกน Z เร็ว-ช้า พลังงานจะย้ายความถี่", x=20, y=36, color=SEC)

# หนึ่งแท่งต่อหนึ่ง bin + เส้น peak-hold
hz_lbls = []
bars = []
for k in range(HALF):
    y = 60 + k * 18
    hz_lbls.append(ui.Label("%4.1f" % (k * FS / N), x=20, y=y, color=DIM))
    bars.append(ui.Bar(x=86, y=y + 2, w=560, h=11, min=0, max=100, value=0, color=DIM))

hold_lbl = ui.Label("hold: -- Hz", x=660, y=62, color=AMBER)
peak_lbl = ui.Label("peak: -- Hz", x=660, y=86, color=GREEN)
back = ui.Button("< ออก", x=580, y=356, w=110, h=36)
back_id = back.id()

avg = [0.0] * HALF     # สเปกตรัมเฉลี่ยแบบ EMA
hold_bin = 0           # bin ที่เคยแรงสุด (peak-hold)
hold_mag = 0.0

try:
    while True:
        # 1) เก็บ N จุด (แกน Z) ด้วยอัตราสุ่มสม่ำเสมอ
        buf = []
        for _ in range(N):
            _, _, az, _, _, _ = sensors.bmi270.motion()
            buf.append(az)
            time.sleep_ms(int(1000 / FS))

        # 2) ตัด DC (ลบค่าเฉลี่ย) + 3) คูณ Hann window ที่เตรียมไว้
        mean = sum(buf) / N
        re = [(buf[i] - mean) * HANN[i] for i in range(N)]
        im = [0.0] * N

        # แปลงเข้าโดเมนความถี่
        fft(re, im)

        # 4) magnitude ครึ่งแรก แล้วเฉลี่ยแบบ EMA ให้แท่งนิ่งขึ้น
        for k in range(HALF):
            m = math.sqrt(re[k] * re[k] + im[k] * im[k])
            avg[k] = SMOOTH * avg[k] + (1.0 - SMOOTH) * m

        # 5) ความถี่เด่นของเฟรมนี้ (ข้าม bin 0 = DC ที่หลงเหลือ)
        kmax = max(range(1, HALF), key=lambda k: avg[k])

        # peak-hold: จำ bin ที่เคยแรงสุดไว้ (ค่อย ๆ ลืมทีละนิดถ้าไม่มีอะไรแรงกว่า)
        if avg[kmax] > hold_mag:
            hold_mag, hold_bin = avg[kmax], kmax
        else:
            hold_mag *= 0.97

        # พลังงานรวม (RMS ของสัญญาณหลังตัด DC) — บอกว่า "เขย่าแรงแค่ไหน"
        rms = math.sqrt(sum((buf[i] - mean) ** 2 for i in range(N)) / N)

        # ---- แสดงผล ----
        top = max(avg[1:]) if HALF > 1 else 1.0
        if top < 1e-6:
            top = 1e-6
        for k in range(HALF):
            bars[k].value(min(100, int(avg[k] / top * 100)))
            if k == kmax:
                bars[k].color(GREEN)
            elif k == hold_bin:
                bars[k].color(AMBER)
            else:
                bars[k].color(DIM)
        seg.text("%.0f" % (kmax * FS / N))
        rms_lbl.text("energy: %.3f" % rms)
        peak_lbl.text("peak: %.1f Hz" % (kmax * FS / N))
        hold_lbl.text("hold: %.1f Hz" % (hold_bin * FS / N))
        lcd.console("peak %.1f Hz  hold %.1f Hz  rms %.3f"
                    % (kmax * FS / N, hold_bin * FS / N, rms))

        for ev in ui.poll():
            if ev.get("handle") == back_id:
                raise KeyboardInterrupt
except KeyboardInterrupt:
    pass
finally:
    info.text("จบ - สเปกตรัมนี้คือ feature ที่โมเดลเสียงใช้")
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
