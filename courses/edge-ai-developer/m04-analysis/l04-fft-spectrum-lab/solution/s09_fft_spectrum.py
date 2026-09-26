# s09_fft_spectrum.py - จากโดเมนเวลา สู่โดเมนความถี่ (FFT)
# วิธีรัน: เปิดใน BENTO IDE (บอร์ดจริง) หรือ BENTO Emulator (ide.tesaiot.dev)
#          กด "Program to Device" แล้วเขย่าบอร์ดแกน Z เร็ว-ช้าสลับกัน ดูสเปกตรัมขยับ
#
# เฉลยนี้ไม่ได้มีไว้ลอกวาง — สิ่งที่นับคือการอธิบายด้วยคำพูดของคุณเอง
# อ่านให้เข้าใจ ปิดไฟล์ แล้วพิมพ์ใหม่ด้วยมือ เพราะตอนพิมพ์เองนั่นแหละ pipeline สี่ขั้น
# (ตัด DC -> window -> magnitude -> peak) จะเข้าหัว หัวใจของชุดบทเรียนนี้คือเข้าใจว่า "ความถี่"
# เป็นอีกวิธีมองสัญญาณเดียวกัน และเป็นวิธีที่โมเดลเสียงมองจริง ๆ

import ui
ui.screen()
import lcd
import sensors
import time
import math

N = 32                 # จำนวนจุดต่อหน้าต่าง ต้องเป็นเลขยกกำลัง 2 (radix-2)
FS = 50.0              # อัตราสุ่ม ~50 Hz -> เห็นความถี่ได้ถึง 25 Hz (Nyquist = FS/2)
HALF = N // 2          # bin ความถี่บวก: k=0..HALF-1 คือ 0 Hz ถึงเกือบ Nyquist

GREEN = 0x50D890       # bin ที่พลังงานสูงสุด (ความถี่เด่น)
DIM   = 0x2A4A44       # bin อื่น ๆ
CYAN  = 0x71C7EC       # หัวข้อ / ป้าย Hz


def fft(re, im):
    """in-place iterative radix-2 FFT (Cooley-Tukey).
    re/im = list ยาว N (im เริ่มเป็น 0). FFT ไม่ใช่เวทมนตร์ — มันคือการถามสัญญาณว่า
    "ในตัวเธอมีคลื่นไซน์ความถี่ไหนซ่อนอยู่บ้าง แต่ละอันแรงแค่ไหน" แล้วตอบกลับเป็น
    เลขเชิงซ้อนต่อ bin (re = ส่วนโคไซน์, im = ส่วนไซน์)"""
    n = len(re)
    # bit-reversal permutation — จัดลำดับ input ให้ butterfly ทำงานในที่ได้
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
    # butterflies — รวมผลทีละคู่ ไล่ขนาด 2,4,8,...,N (นี่คือที่มาของคำว่า "Fast")
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
# bin width = FS/N คือ "ความละเอียดความถี่" — N มากขึ้น bin แคบลง แยกความถี่ได้ดีขึ้น
lcd.console(' N=%d จุด, FS=%.0f Hz -> bin width = %.2f Hz, Nyquist = %.0f Hz'
            % (N, FS, FS / N, FS / 2))

# ---- สร้าง widget ครั้งเดียวก่อนเข้าลูป — สร้างซ้ำทุกวนรอบจะกินหน่วยความจำและจอกระพริบ ----
ui.Label("FFT Spectrum - โดเมนความถี่", x=20, y=8, color=CYAN)
info = ui.Label("เขย่าบอร์ดแกน Z เร็ว-ช้า ดูพลังงานย้ายความถี่", x=20, y=32)

# หนึ่งแท่ง (Bar) ต่อหนึ่ง bin ความถี่ ป้าย Hz อยู่ซ้าย แท่งอยู่ขวา
# เราสร้างครบ HALF แท่งไว้ก่อน ในลูปแค่เปลี่ยน value + สี — ถูกกว่าการสร้าง widget ใหม่
hz_lbls = []
bars = []
for k in range(HALF):
    y = 62 + k * 19
    hz_lbls.append(ui.Label("%4.1f Hz" % (k * FS / N), x=20, y=y, color=DIM))
    bars.append(ui.Bar(x=100, y=y + 2, w=640, h=12, min=0, max=100, value=0, color=DIM))

peak_lbl = ui.Label("peak: -- Hz", x=20, y=62 + HALF * 19 + 4, color=GREEN)
back = ui.Button("< ออก", x=570, y=356, w=120, h=36)
back_id = back.id()

try:
    while True:
        # 1) เก็บ N จุดจาก IMU — แกน Z ของ accel ตอบสนองการเขย่าขึ้น-ลงได้ดี
        #    หน่วงทีละ 1/FS วินาที ให้ได้อัตราสุ่มตามที่ตั้งไว้ (สำคัญ! FFT อ่านความถี่
        #    ถูกต้องต่อเมื่อระยะห่างระหว่างจุดสม่ำเสมอ)
        buf = []
        for _ in range(N):
            _, _, az, _, _, _ = sensors.bmi270.motion()
            buf.append(az)
            time.sleep_ms(int(1000 / FS))

        # 2) ตัด DC ก่อน: ลบค่าเฉลี่ยของหน้าต่างออก แรงโน้มถ่วง ~1g เป็นค่าคงที่ (0 Hz)
        #    ถ้าไม่ลบ มันจะโผล่เป็นยอดใหญ่ที่ bin 0 กลบสเปกตรัมของการเขย่าจริง
        mean = sum(buf) / N

        # 3) คูณ Hann window: หน้าต่างค่อย ๆ ไล่ 0 -> 1 -> 0 กดขอบให้นุ่ม ลด spectral
        #    leakage (การที่พลังงานของหนึ่งความถี่รั่วไปเปื้อน bin ข้างเคียง เพราะเรา
        #    ตัดสัญญาณเป็นท่อน ๆ ที่ขอบไม่พอดีคาบ)
        re = [(buf[i] - mean) * (0.5 - 0.5 * math.cos(2 * math.pi * i / (N - 1)))
              for i in range(N)]
        im = [0.0] * N

        # แปลงเข้าโดเมนความถี่ (ในที่ ผลกลับมาอยู่ใน re/im)
        fft(re, im)

        # 4) magnitude = ขนาดของเลขเชิงซ้อนต่อ bin = sqrt(re^2 + im^2) = "ความถี่นี้แรงแค่ไหน"
        #    เอาเฉพาะครึ่งแรก (ความถี่บวก) อีกครึ่งเป็นภาพสะท้อนของสัญญาณจริง
        mag = [math.sqrt(re[k] * re[k] + im[k] * im[k]) for k in range(HALF)]

        # 5) ความถี่เด่น = bin ที่ magnitude สูงสุด (ข้าม bin 0 = DC ที่ยังหลงเหลือ)
        #    แปลง bin -> Hz ด้วย f = k * FS / N
        kmax = max(range(1, HALF), key=lambda k: mag[k])

        # แสดง: normalize ให้ยอดสูงสุดเต็มจอ แล้วระบายแท่ง (bin เด่น = เขียว, อื่น ๆ = จาง)
        top = max(mag[1:]) if HALF > 1 else 1.0
        if top < 1e-6:                       # กันหารศูนย์ตอนบอร์ดวางนิ่งสนิท
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
