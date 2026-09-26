# s09_fft_spectrum.py - จากโดเมนเวลา สู่โดเมนความถี่ (FFT)
#
# โมเดลเสียงบนบอร์ดไม่ได้ "ฟัง" คลื่นดิบ มันดูสเปกตรัม (ความถี่ไหนแรง) โปรแกรมนี้
# แสดงให้เห็นด้วยตาว่า FFT ทำอะไร: เก็บสัญญาณ IMU N จุด แล้วแปลงเป็นสเปกตรัม
# ขนาดของแต่ละความถี่ — เขย่าเร็วจะเห็นพลังงานย้ายไปความถี่สูง
#
# เราเขียน FFT เอง (radix-2 Cooley-Tukey) เพื่อให้เห็นว่ามันไม่ใช่กล่องดำ —
# เป็นแค่การรวมไซน์/โคไซน์ที่ความถี่ต่าง ๆ

import ui, lcd, sensors, time, math

N = 64                 # ต้องเป็นเลขยกกำลัง 2 (radix-2)
FS = 50.0             # อัตราสุ่ม ~50 Hz -> เห็นความถี่ได้ถึง 25 Hz (Nyquist)


def fft(re, im):
    # in-place iterative radix-2 FFT. re/im = list ยาว N (im เริ่มเป็น 0)
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


# สร้าง widget ครั้งเดียว
ui.screen()
ui.Label("FFT Spectrum - โดเมนความถี่", x=20, y=10, color=0x71C7EC)
info = ui.Label("เขย่าบอร์ดดูพลังงานย้ายความถี่", x=20, y=44)
chart = ui.Chart(x=20, y=80, w=760, h=220)      # แสดงสเปกตรัม N/2 แท่ง
peak_lbl = ui.Label("peak: -- Hz", x=20, y=320, color=0x50D890)
back = ui.Button("< ออก", x=570, y=320, w=120, h=44, color=0x2A1712)

try:
    while True:
        # 1) เก็บ N จุด (แกน Z ของ accel — ตอบสนองการเขย่าดี)
        re = []
        for _ in range(N):
            _, _, az, _, _, _ = sensors.bmi270.motion()
            re.append(az)
            time.sleep_ms(int(1000 / FS))
        # 2) เอาค่าเฉลี่ยออก (ตัด DC / แรงโน้มถ่วง) แล้วทำ Hann window ลดขอบ
        mean = sum(re) / N
        re = [(re[i] - mean) * (0.5 - 0.5 * math.cos(2 * math.pi * i / (N - 1))) for i in range(N)]
        im = [0.0] * N
        # 3) FFT -> ขนาดครึ่งแรก (ความถี่บวก)
        fft(re, im)
        mag = [math.sqrt(re[k] * re[k] + im[k] * im[k]) for k in range(N // 2)]
        # 4) แสดง + หาความถี่เด่น
        chart.set_next(mag) if hasattr(chart, "set_next") else None
        for k, m in enumerate(mag):
            try:
                chart.add_series(k, int(m))
            except Exception:
                pass
        kmax = max(range(1, N // 2), key=lambda k: mag[k])
        peak_lbl.text("peak: %.1f Hz" % (kmax * FS / N))
        lcd.console("peak bin %d = %.1f Hz" % (kmax, kmax * FS / N))
        for ev in ui.poll():
            if ev.get("handle") == back.id():
                raise KeyboardInterrupt
except KeyboardInterrupt:
    pass
finally:
    info.text("จบ - FFT คือหัวใจของ feature ที่โมเดลเสียงใช้")

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
