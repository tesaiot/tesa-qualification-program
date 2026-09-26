# s09_fft_spectrum.py - จากโดเมนเวลา สู่โดเมนความถี่ (ฉบับฝึกเติมโค้ด)
# วิธีรัน: 1) เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator ที่ ide.tesaiot.dev
#          2) เติมช่องว่างทั้ง 4 จุดตามคำใบ้ในคอมเมนต์ `# เติม:` ให้ครบ
#          3) กด "Program to Device" แล้วเขย่าบอร์ด (แกน Z) เร็ว-ช้าสลับกัน
#          4) ดูแท่งสเปกตรัมขยับ + ความถี่เด่น (peak) เปลี่ยนตามจังหวะที่เขย่า
#
# โมเดลเสียงบนบอร์ดไม่ได้ "ฟัง" คลื่นดิบทีละจุด มันดู "สเปกตรัม" ว่าความถี่ไหนแรง
# ชุดบทเรียนนี้เราจะเห็นด้วยตาว่า FFT (Fast Fourier Transform) ทำอะไร: เก็บสัญญาณ IMU N จุด
# ในโดเมนเวลา แล้วแปลงเป็นขนาดของแต่ละความถี่ในโดเมนความถี่ เขย่าเร็ว = พลังงาน
# ย้ายไปความถี่สูง เขย่าช้า = พลังงานอยู่ความถี่ต่ำ งานของเราคือเติม 4 ขั้นของ pipeline

import ui
ui.screen()
import lcd
import sensors
import time
import math

N = 32                 # จำนวนจุดต่อหน้าต่าง ต้องเป็นเลขยกกำลัง 2 (radix-2)
FS = 50.0              # อัตราสุ่ม ~50 Hz -> เห็นความถี่ได้ถึง 25 Hz (Nyquist = FS/2)
HALF = N // 2          # จำนวน bin ความถี่บวก (สเปกตรัมครึ่งแรก)

GREEN = 0x50D890       # bin ที่พลังงานสูงสุด (peak)
DIM   = 0x2A4A44       # bin อื่น ๆ
CYAN  = 0x71C7EC       # หัวข้อ / ป้าย Hz


def fft(re, im):
    """in-place iterative radix-2 FFT (Cooley-Tukey) — ให้มาแล้วครบ ไม่ต้องแก้.
    re/im คือ list ยาว N (im เริ่มเป็น 0 ทั้งหมด) หลังเรียกจะได้ผลอยู่ใน re/im เดิม.
    FFT ไม่ใช่กล่องดำ — มันคือการรวมไซน์/โคไซน์ที่ความถี่ต่าง ๆ อย่างมีระเบียบ"""
    n = len(re)
    # bit-reversal permutation
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
    # butterflies
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


lcd.clear()
lcd.console('<h2> FFT Spectrum - โดเมนความถี่</h2>')
lcd.console(' N=%d จุด, FS=%.0f Hz -> bin width = %.2f Hz, Nyquist = %.0f Hz'
            % (N, FS, FS / N, FS / 2))

# ---- สร้าง widget ครั้งเดียวก่อนเข้าลูป (สร้างซ้ำในลูปจะกินหน่วยความจำและจอกระพริบ) ----
ui.Label("FFT Spectrum - โดเมนความถี่", x=20, y=8, color=CYAN)
info = ui.Label("เขย่าบอร์ดแกน Z เร็ว-ช้า ดูพลังงานย้ายความถี่", x=20, y=32)

# หนึ่งแท่ง (Bar) ต่อหนึ่ง bin ความถี่ — สร้างไว้ก่อน แล้วในลูปแค่เปลี่ยนค่า/สี
hz_lbls = []
bars = []
for k in range(HALF):
    y = 62 + k * 19
    hz_lbls.append(ui.Label("%4.1f Hz" % (k * FS / N), x=20, y=y, color=DIM))
    bars.append(ui.Bar(x=100, y=y + 2, w=640, h=12, min=0, max=100, value=0, color=DIM))

peak_lbl = ui.Label("peak: -- Hz", x=20, y=62 + HALF * 19 + 4, color=GREEN)
back = ui.Button("< ออก", x=640, y=356, w=120, h=36)
back_id = back.id()

try:
    while True:
        # 1) เก็บ N จุดจาก IMU (แกน Z ของ accel ตอบสนองการเขย่าดี) — ให้มาแล้ว
        buf = []
        for _ in range(N):
            _, _, az, _, _, _ = sensors.bmi270.motion()
            buf.append(az)
            time.sleep_ms(int(1000 / FS))

        # 2) เติม: ตัด DC/แรงโน้มถ่วงออกก่อน ด้วยการลบค่าเฉลี่ยของหน้าต่าง
        #    ถ้าไม่ตัด bin 0 จะโตพุ่ง (แรงโน้มถ่วง ~1g อยู่ในนั้น) กลบสเปกตรัมจริง
        #    -> mean = sum(buf) / N
        mean = 0.0

        # 3) เติม: คูณ Hann window ลด spectral leakage (สัญญาณรั่วไป bin ข้างเคียง)
        #    หน้าต่างค่อย ๆ ไล่จาก 0 ที่ขอบ -> 1 ตรงกลาง -> 0 ที่ขอบ
        #    w[i] = 0.5 - 0.5*math.cos(2*math.pi*i/(N-1))
        #    -> re = [(buf[i] - mean) * (0.5 - 0.5*math.cos(2*math.pi*i/(N-1))) for i in range(N)]
        re = [(buf[i] - mean) for i in range(N)]
        im = [0.0] * N

        # FFT ในที่ (โดเมนเวลา -> โดเมนความถี่) — ให้มาแล้ว
        fft(re, im)

        # 4) เติม: ขนาด (magnitude) ของแต่ละความถี่ = ระยะจากจุดกำเนิดของเลขเชิงซ้อน
        #    mag[k] = sqrt(re[k]^2 + im[k]^2) เอาเฉพาะครึ่งแรก (ความถี่บวก HALF bin)
        #    -> mag = [math.sqrt(re[k]*re[k] + im[k]*im[k]) for k in range(HALF)]
        mag = [0.0 for k in range(HALF)]

        # 5) เติม: หา bin ที่พลังงานสูงสุด (ข้าม bin 0 = DC ที่เหลือ) = ความถี่เด่น
        #    -> kmax = max(range(1, HALF), key=lambda k: mag[k])
        kmax = 1

        # แสดงผล: ปรับสเกลให้เต็มจอ แล้วระบายแท่ง (bin เด่น = เขียว, อื่น ๆ = จาง)
        top = max(mag[1:]) if HALF > 1 else 1.0
        if top < 1e-6:
            top = 1e-6
        for k in range(HALF):
            bars[k].value(min(100, int(mag[k] / top * 100)))
            bars[k].color(GREEN if k == kmax else DIM)
        peak_lbl.text("peak: %.1f Hz  (bin %d)" % (kmax * FS / N, kmax))
        lcd.console("peak bin %d = %.1f Hz" % (kmax, kmax * FS / N))

        for ev in ui.poll():
            if ev.get("handle") == back_id:
                raise KeyboardInterrupt
except KeyboardInterrupt:
    pass
finally:
    info.text("จบ - สเปกตรัมนี้แหละคือ feature ที่โมเดลเสียงใช้")
    lcd.console('<span class=ok> จบการทำงาน</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
