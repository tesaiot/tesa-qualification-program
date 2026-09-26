# s05_multicapture_full.py - Multi-Sensor Sync Capture (ฉบับเต็ม)
#
# ต่อยอดจากเฉลย s05_multicapture.py ให้กลายเป็น "โต๊ะเก็บ dataset" ที่ใช้ได้จริง เพิ่ม
# สามอย่างที่ dataset จริงต้องมี:
#   1) เก็บทั้งสองรูปแบบ: ไฟล์ CSV (IMU + ระดับเสียง ต่อแถว) และไฟล์ .wav เสียงดิบคู่กัน
#      ให้เลือกทีหลังได้ว่าจะ train จาก feature หรือจากคลื่นเสียงดิบ
#   2) ตรวจความสมบูรณ์ของเส้นเวลา: วัดช่วงเวลาจริงต่อแถว (ควรใกล้ 20 ms) และ jitter สูงสุด
#      ถ้า jitter สูง แปลว่าเก็บช้าเป็นบางจังหวะ — dataset จะเพี้ยน ต้องรู้ไว้
#   3) สรุปต่อ label: จำนวนแถว, peak dBFS, ช่วงเวลาเฉลี่ยจริง — เขียนลง manifest ด้วย
#
# ต้องรันบนบอร์ด BENTO AI Kit จริง (Emulator มีแค่เสียงสังเคราะห์ ไม่ใช่เสียงจริง) ดึงไฟล์ออกด้วย BENTO IDE
# หรือ mpremote: /multicapture.csv, /multicapture.wav, /multicapture_manifest.txt

import ui
ui.screen()
import lcd
from machine import PDM_PCM
import sensors
import array, math, struct, time

RATE_MS = 20                 # เป้าหมาย 50 Hz ต่อแถว
BURST = 200                  # ~4 วินาทีต่อการกดหนึ่งครั้ง
CHUNK = 512                  # sample เสียงต่อเฟรม
AUDIO_RATE = 16000
CSV_PATH = "/multicapture.csv"
WAV_PATH = "/multicapture.wav"
MANIFEST = "/multicapture_manifest.txt"
LABELS = ("idle", "circle", "shaking")

CYAN  = 0x71C7EC
GREEN = 0x50D890
AMBER = 0xFFAA44
CARD  = 0x2A1712
RED   = 0xE85B5B
SEC   = 0xCFC6BF

lcd.clear()
lcd.console('<h2> Multi-Sensor Capture (full) - IMU + MIC + WAV</h2>')

ui.Label("DAQ II - Sync Capture", x=20, y=10, color=CYAN)
status = ui.Label("เลือก label แล้วทำท่า + ส่งเสียงพร้อมกัน", x=20, y=44)
count_lbl = ui.Label("รวม: 0 แถว", x=20, y=76)

ui.Panel(x=20, y=104, w=470, h=118, color=CARD)
level = ui.Bar(x=36, y=124, w=430, h=14, min=0, max=60, value=0, color=GREEN)
seg = ui.Seg7("---", x=44, y=146, color=GREEN)
peak_lbl = ui.Label("peak: -- dBFS", x=220, y=150, color=AMBER)
timing_lbl = ui.Label("dt: -- ms   jitter: -- ms", x=220, y=190, color=SEC)

btns = []
for i, name in enumerate(LABELS):
    btns.append(ui.Button(name, x=20 + i * 130, y=250, w=120, h=54, color=GREEN))
back = ui.Button("< ออก", x=520, y=320, w=120, h=48, color=CARD)
back_id = back.id()

pdm = PDM_PCM(0, sck="P8_5", data="P8_6", sample_rate=AUDIO_RATE)
buf = array.array("h", (0 for _ in range(CHUNK)))


def wav_header(n_samples, rate):
    """หัวไฟล์ WAV 16-bit mono — เขียนก่อน แล้วค่อยเติมความยาวจริงตอนปิด"""
    data_len = n_samples * 2
    return (b"RIFF" + struct.pack("<I", 36 + data_len) + b"WAVEfmt " +
            struct.pack("<IHHIIHH", 16, 1, 1, rate, rate * 2, 2, 16) +
            b"data" + struct.pack("<I", data_len))


def ensure_csv():
    try:
        open(CSV_PATH, "r").close()
    except OSError:
        with open(CSV_PATH, "w") as f:
            f.write("t_ms,label,ax,ay,az,gx,gy,gz,db\n")


def dbfs(chunk):
    acc = 0
    for s in chunk:
        acc += s * s
    rms = math.sqrt(acc / len(chunk))
    return 20 * math.log10(rms / 32768) if rms > 0 else -96.0


ensure_csv()
total_rows = 0
wav_samples = 0


def record(label):
    """เก็บหนึ่งชุด: CSV (feature ต่อแถว) + WAV (เสียงดิบ) + วัดคุณภาพเส้นเวลา"""
    global total_rows, wav_samples
    status.text("กำลังบันทึก '%s' ..." % label)
    status.color(RED)
    peak = -96.0
    max_gap = 0
    t0 = time.ticks_ms()
    prev = t0
    fcsv = open(CSV_PATH, "a")
    fwav = open(WAV_PATH, "ab")
    try:
        for n in range(BURST):
            now = time.ticks_ms()
            t_ms = time.ticks_diff(now, t0)          # เส้นเวลาร่วมของทุกเซนเซอร์ในชุดนี้
            gap = time.ticks_diff(now, prev)         # ช่วงเวลาจริงระหว่างแถว (ไว้วัด jitter)
            if n > 0 and gap > max_gap:
                max_gap = gap
            prev = now

            ax, ay, az, gx, gy, gz = sensors.bmi270.motion()   # เซนเซอร์ 1: IMU
            pdm.readinto(buf)                                   # เซนเซอร์ 2: MIC (เสียงดิบ)
            db = dbfs(buf)
            if db > peak:
                peak = db

            # แถว feature ที่มัดสองเซนเซอร์ด้วย t_ms ร่วม
            fcsv.write("%d,%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.1f\n"
                       % (t_ms, label, ax, ay, az, gx, gy, gz, db))
            fwav.write(buf)                                     # เก็บคลื่นเสียงดิบไว้ด้วย
            wav_samples += CHUNK

            level.value(max(0, int(db + 60)))
            seg.text("%d" % (BURST - n))
            peak_lbl.text("peak: %.1f dBFS" % peak)
            time.sleep_ms(RATE_MS)
    finally:
        fcsv.close()
        fwav.close()

    elapsed = time.ticks_diff(time.ticks_ms(), t0)
    dt = elapsed / BURST                             # ช่วงเวลาเฉลี่ยจริง (ควรใกล้ RATE_MS)
    total_rows += BURST
    seg.text("OK")
    count_lbl.text("รวม: %d แถว" % total_rows)
    timing_lbl.text("dt: %.1f ms   jitter: %d ms" % (dt, max_gap))
    status.text("เสร็จ '%s' - เลือกท่าต่อไป" % label)
    status.color(GREEN)
    with open(MANIFEST, "a") as m:
        m.write("%s rows=%d dt=%.1fms jitter=%dms peak=%.1fdBFS\n"
                % (label, BURST, dt, max_gap, peak))
    lcd.console("<span class=ok> %s: %d แถว, dt %.1f ms, jitter %d ms, peak %.1f dBFS</span>"
                % (label, BURST, dt, max_gap, peak))


try:
    while True:
        for ev in ui.poll():
            h = ev.get("handle")
            if h == back_id:
                raise KeyboardInterrupt
            for i, b in enumerate(btns):
                if h == b.id():
                    record(LABELS[i])
        time.sleep_ms(30)
except KeyboardInterrupt:
    pass
finally:
    pdm.deinit()
    # ปิดท้าย WAV ให้ถูกต้อง: เขียนหัวใหม่ด้วยจำนวน sample จริงที่เก็บได้
    if wav_samples:
        try:
            payload = open(WAV_PATH, "rb").read()
            with open(WAV_PATH, "wb") as f:
                f.write(wav_header(wav_samples, AUDIO_RATE))
                f.write(payload)
        except OSError as e:
            lcd.console("<span class=error> ปิดไฟล์ WAV ไม่สำเร็จ: %s</span>" % e)
    lcd.console("<span class=ok> จบ: %d แถว, เสียง %d sample -> %s + %s</span>"
                % (total_rows, wav_samples, CSV_PATH, WAV_PATH))
    status.text("จบ - dataset: %s , %s" % (CSV_PATH, WAV_PATH))

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
