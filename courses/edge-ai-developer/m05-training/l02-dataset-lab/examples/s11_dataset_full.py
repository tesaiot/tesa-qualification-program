# s11_dataset_full.py - เก็บ dataset IMU ที่สมดุลและพร้อม train ลง CSV (ฉบับเต็ม)
# วิธีรัน: เปิดใน BENTO IDE เสียบบอร์ดจริง กด "Program to Device"
#          แตะปุ่ม label ทำท่านั้นค้าง ~4 วินาที เก็บให้ทั้ง 3 คลาสสมดุล
#
# ฉบับนี้คือเวอร์ชันที่ขัดจนเรียบร้อยของ s11_dataset.py - โครงเดียวกับที่คุณเติมใน
# ไฟล์ฝึก แต่ยกระดับเรื่อง "dataset engineering" อีกสามชั้น:
#   1) เตือน "ไม่สมดุล" สดๆ - ถ้าคลาสมากสุดห่างคลาสน้อยสุดเกินเกณฑ์ ขึ้นเตือนสีแดง
#   2) โชว์อัตราสมดุล (min/max) + จำนวนหน้าต่างโดยประมาณที่ split จะได้ต่อกอง
#   3) ปุ่ม "ล้างไฟล์" เริ่มเก็บใหม่ + สรุปสัดส่วนตอนออก
# ทั้งหมดยังยืนบนคำสั่งเดิม: sensors.bmi270.motion() + f.write() + counts ต่อคลาส

import ui
ui.screen()
import lcd
import sensors
import time

# ---- ปรับตรงนี้: เป้าหมาย / อัตรา / เกณฑ์สมดุล ----
RATE_MS = 20            # 50 Hz - ตรงกับอัตราที่โมเดล Motion บนบอร์ดกิน
BURST = 200            # sample ต่อการกดหนึ่งครั้ง (~4 วินาที)
TARGET = 1000          # เป้าหมายต่อคลาส
WIN = 50               # ความยาวหน้าต่าง (ตรงกับ dataset_tools.py) - ใช้ประเมินจำนวนหน้าต่าง
HOP = 25               # ระยะเลื่อนหน้าต่าง (ตรงกับ dataset_tools.py)
BALANCE_TOL = 0.30     # ยอมให้คลาสน้อยสุดต่างจากมากสุดได้ไม่เกิน 30% ก่อนเตือน
PATH = "/gestures.csv"
CLASSES = ("idle", "circle", "shaking")

# ธีมสีเดียวกับหน้าอื่นในคอร์ส
CYAN   = 0x71C7EC
GREEN  = 0x50D890
AMBER  = 0xE0A03A
RED    = 0xE85B5B
DIM    = 0x6A3A31
CARD   = 0x2A1712

lcd.clear()
lcd.console('<h2> Dataset Engineering - เก็บให้สมดุล (ฉบับเต็ม)</h2>')
lcd.console(' เป้าหมาย %d sample/คลาส · เตือนเมื่อไม่สมดุลเกิน %d%%'
            % (TARGET, int(BALANCE_TOL * 100)))

# ---- สร้าง widget ครั้งเดียวก่อนลูป ----
ui.Label("Dataset - เก็บ IMU ให้สมดุล", x=20, y=10, color=CYAN)
status = ui.Label("แตะปุ่ม label แล้วทำท่านั้นค้างไว้", x=20, y=42, color=CYAN)

btns = {}
bars = {}
labs = {}
for i, name in enumerate(CLASSES):
    y = 82 + i * 52
    btns[name] = ui.Button(name, x=20, y=y, w=150, h=42, color=GREEN)
    labs[name] = ui.Label("%s: 0" % name, x=190, y=y + 2, color=CYAN)
    bars[name] = ui.Bar(x=190, y=y + 24, w=560, h=12, min=0, max=TARGET, value=0, color=DIM)

hint = ui.Label("เริ่มเก็บได้เลย", x=20, y=250, color=AMBER)
balance_lbl = ui.Label("สมดุล: -- ", x=20, y=280, color=CYAN)
windows_lbl = ui.Label("หน้าต่างโดยประมาณ: --", x=300, y=280, color=CYAN)
clear_btn = ui.Button("ล้างไฟล์", x=470, y=352, w=120, h=36, color=CARD)
back = ui.Button("< ออก", x=570, y=352, w=120, h=36, color=CARD)

counts = {c: 0 for c in CLASSES}


def write_header():
    """เขียนหัวตาราง (ใช้ตอนเริ่ม + ตอนล้างไฟล์)"""
    with open(PATH, "w") as f:
        f.write("label,ax,ay,az,gx,gy,gz\n")


def ensure_file():
    try:
        open(PATH, "r").close()
    except OSError:
        write_header()


def est_windows(n_samples):
    """ประเมินจำนวนหน้าต่างที่ make_windows() จะได้จาก n_samples (WIN/HOP เดียวกับ PC)"""
    if n_samples < WIN:
        return 0
    return (n_samples - WIN) // HOP + 1


def refresh_balance():
    """อัปเดตแถบ + เตือนความไม่สมดุล + ประเมินจำนวนหน้าต่างต่อกอง split"""
    for c in CLASSES:
        bars[c].value(min(counts[c], TARGET))
        labs[c].text("%s: %d" % (c, counts[c]))

    lo = min(counts.values())
    hi = max(counts.values())
    fewest = min(counts, key=counts.get)

    # อัตราสมดุล: คลาสน้อยสุดเป็นกี่เท่าของมากสุด (1.00 = สมดุลเป๊ะ)
    ratio = (lo / hi) if hi > 0 else 1.0
    balance_lbl.text("สมดุล: %.2f (น้อยสุด/มากสุด)" % ratio)

    # ประเมินจำนวนหน้าต่างรวม (ผลรวมของทุกคลาส) เพื่อให้เห็นว่า train จะมีข้อมูลพอไหม
    total_win = sum(est_windows(counts[c]) for c in CLASSES)
    windows_lbl.text("หน้าต่างโดยประมาณ: %d" % total_win)

    if hi > 0 and ratio < (1.0 - BALANCE_TOL):
        # ไม่สมดุลเกินเกณฑ์ - เตือนแดง แล้วชี้คลาสที่ต้องเก็บเพิ่ม
        hint.text("ไม่สมดุล! เก็บ '%s' เพิ่มด่วน (%d vs %d)" % (fewest, lo, hi))
        hint.color(RED)
    elif counts[fewest] < TARGET:
        hint.text("เก็บ '%s' เพิ่ม (น้อยสุดตอนนี้)" % fewest)
        hint.color(AMBER)
    else:
        hint.text("ครบทุกคลาสถึงเป้า + สมดุล - พร้อม split!")
        hint.color(GREEN)


def record(label):
    """เก็บ BURST samples ของ label ลงไฟล์ที่ 50 Hz แล้วนับเข้าตัวนับสมดุล"""
    status.text("กำลังเก็บ '%s' ..." % label)
    with open(PATH, "a") as f:
        for _ in range(BURST):
            ax, ay, az, gx, gy, gz = sensors.bmi270.motion()
            f.write("%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n" % (label, ax, ay, az, gx, gy, gz))
            time.sleep_ms(RATE_MS)
    counts[label] += BURST
    refresh_balance()
    status.text("เสร็จ '%s' - เลือกท่าต่อไปให้สมดุล" % label)
    lcd.console("<span class=ok> logged %d of '%s' -> %s</span>" % (BURST, label, PATH))


def clear_dataset():
    """ล้างไฟล์ + รีเซ็ตตัวนับ เริ่มเก็บใหม่ทั้งหมด"""
    write_header()
    for c in CLASSES:
        counts[c] = 0
    refresh_balance()
    status.text("ล้างไฟล์แล้ว - เริ่มเก็บใหม่")
    lcd.console(" cleared %s" % PATH)


ensure_file()
refresh_balance()

try:
    while True:
        for ev in ui.poll():
            h = ev.get("handle")
            if h == back.id():
                raise KeyboardInterrupt
            elif h == clear_btn.id():
                clear_dataset()
            else:
                for name in CLASSES:
                    if h == btns[name].id():
                        record(name)
        time.sleep_ms(30)
except KeyboardInterrupt:
    pass
finally:
    total = sum(counts.values())
    lo = min(counts.values())
    hi = max(counts.values())
    ratio = (lo / hi) if hi > 0 else 1.0
    lcd.console("<span class=ok> dataset done: %d samples, balance %.2f</span>" % (total, ratio))
    lcd.console(" per-class: %s" % ", ".join("%s=%d" % (c, counts[c]) for c in CLASSES))
    if ratio < (1.0 - BALANCE_TOL):
        lcd.console("<span class=error> ยังไม่สมดุล ควรเก็บเพิ่มก่อน train</span>")
    status.text("จบ - split ต่อบน PC ด้วย dataset_tools.py")

# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
