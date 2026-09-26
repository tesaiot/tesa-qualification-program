# 07 - อัดเสียงเป็นไฟล์ .wav พร้อมหน้าจอนับถอยหลัง
# *** ข้อจำกัดปัจจุบัน: ตัวอย่างนี้ใช้ได้บน PSoC Edge AI Kit ***
# บน TESAIoT Dev Kit (มี audio codec) การเปิด PDM จะชนกับ clock ของ
# ระบบเสียง CM55 - แก้ใน firmware phase ถัดไป (PDM clock guard)
# Spinner + Seg7 ระหว่างอัด แล้วแจ้งผลพร้อมเสียงยืนยัน
# ดึงไฟล์ออกจากบอร์ด: ใช้ BENTO IDE (file transfer) หรือ mpremote
import ui
ui.screen()
import lcd
from machine import PDM_PCM
import array, struct, time

RATE = 16000
SECS = 5
CHUNK = 1024

lcd.clear()
lcd.console('<h2> WAV Recorder</h2>')

ui.Label("Recording...", x=320, y=30, color=0xFF4444)
spin = ui.Spinner(x=180, y=90)
seg = ui.Seg7("%d" % SECS, x=380, y=110, color=0xFFAA44)
ui.Label("วินาทีที่เหลือ", x=370, y=180, color=0x888888)

def wav_header(n_samples, rate):
    data_len = n_samples * 2                        # 16-bit mono
    return (b"RIFF" + struct.pack("<I", 36 + data_len) + b"WAVEfmt " +
            struct.pack("<IHHIIHH", 16, 1, 1, rate, rate * 2, 2, 16) +
            b"data" + struct.pack("<I", data_len))

pdm = PDM_PCM(0, sck="P8_5", data="P8_6", sample_rate=RATE)
buf = array.array("h", (0 for _ in range(CHUNK)))
total = RATE * SECS

lcd.console(' เริ่มอัด %d วินาที - พูดได้เลย!' % SECS)
try:
    with open("/rec.wav", "wb") as f:
        f.write(wav_header(total, RATE))
        written = 0
        last_left = SECS
        while written < total:
            pdm.readinto(buf)
            f.write(buf)
            written += CHUNK
            left = SECS - (written // RATE)
            if left != last_left:                   # อัปเดตเฉพาะวินาทีเปลี่ยน
                seg.text("%d" % left)
                last_left = left
finally:
    pdm.deinit()

spin.hide()
seg.text("OK")
ui.Label("บันทึกแล้ว: /rec.wav  (%d KB)" % ((44 + total * 2) // 1024),
         x=250, y=250, color=0x00FF88)
if hasattr(ui, "sfx"):
    ui.sfx(ui.SFX_UI_SELECT)
lcd.console('<span class=ok> เสร็จ! ไฟล์ /rec.wav</span>')

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
