# SPDX-FileCopyrightText: 2026 Wiroon Sriborrirux, Advance Innovation Centre (AIC), Burapha University
# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: MIT
#
# 01_send_to_dashboard.py - ค่าที่วัดได้บนบอร์ด ไปโผล่บนหน้าเว็บของเรา
#
# ย่อและดัดแปลงจาก examples/s02/05_value_leaves_the_board.py ของหลักสูตร AIoT in Action
# https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer
# (commit a80bbe88, MIT)
#
# ไฟล์นี้สอน: บันไดสามขั้นที่ห้ามสลับ WiFi ต้องได้ IP ก่อน แล้วจึงแนะนำตัวกับ broker
#             แล้วจึง publish ข้อความได้ ขั้นไหนไม่ผ่าน ต้องเห็นบนจอว่าติดที่ขั้นไหน
# ดูที่จอ   : ป้ายสามขั้นเปลี่ยนเป็นสีเขียวตามลำดับ แล้วเลขใบที่ส่งเดินขึ้น
# ดูอีกฝั่ง : เปิดหน้าเว็บอ่านค่าของหลักสูตร AIoT in Action ในเบราว์เซอร์ ต่อท้ายลิงก์ด้วยทีมของคุณ
#             https://advance-innovation-centre-aic.github.io/embedded-systems-for-aiot-developer/examples/web/my_first_reader.html?team=teamXX
# กับดัก    : ชื่ออาร์กิวเมนต์ของ mqtt.connect() คือ username= ไม่ใช่ user=
#             (ไฟล์นี้ไม่ได้ใช้ แต่จำไว้ก่อน) และ publish() ตอนสายหลุดไม่ได้คืน False
#             เฉย ๆ มันโยน OSError ออกมา จึงต้องดักทั้งสองทาง
#
# broker สาธารณะ broker.hivemq.com พอร์ต 1883 ไม่เข้ารหัส ใครก็ subscribe หัวข้อของเราได้
# และใครก็ publish เข้ามาได้ ห้ามส่งข้อมูลส่วนตัวหรือความลับผ่านไฟล์นี้เด็ดขาด

import json
import mqtt
import sensors
import time
import ui
import wifi

# ----- แก้สามบรรทัดนี้ -----
WIFI_SSID = "<ชื่อ WiFi ของคุณ>"       # บนบอร์ดจริงต้องแก้ ใน BENTO Emulator WiFi เป็นของจำลอง
WIFI_PASS = "<รหัส WiFi ของคุณ>"       # อย่าบันทึกรหัสจริงลงไฟล์ที่จะแชร์หรือ push ขึ้น GitHub
TEAM = "teamXX"                       # เลือกเลขสองหลักของคุณเอง เช่น team37 (ห้าม team00)

# สามบรรทัดนี้ไม่ต้องแก้ ต้องตรงกับที่หน้าเว็บอ่านค่าฟังอยู่
BROKER = "broker.hivemq.com"
ROOT = "bento-aiot"
TOPIC = ROOT + "/" + TEAM + "/telemetry"

N = 30            # ส่งกี่ใบ
GAP_MS = 2000     # เว้นระหว่างใบกี่ ms (broker ไม่เก็บใบล่าสุดไว้ หน้าเว็บจะเห็นแค่ใบถัดไป)

COL_TEXT, COL_DIM = 0xE8EAED, 0x9AA3AF
COL_OK, COL_WARN, COL_BAD = 0x30A46C, 0xF5A623, 0xE5484D

ui.screen()
time.sleep_ms(200)
ui.Label("ส่งค่าขึ้นแดชบอร์ด", x=24, y=8, color=COL_TEXT, value=28)
st1 = ui.Label("1) WiFi     ยังไม่ถึงคิว", x=24, y=64, color=COL_DIM, value=20)
st2 = ui.Label("2) broker   ยังไม่ถึงคิว", x=24, y=104, color=COL_DIM, value=20)
st3 = ui.Label("3) publish  ยังไม่ถึงคิว", x=24, y=144, color=COL_DIM, value=20)
seg = ui.Seg7(text="0", x=24, y=192, w=140, h=56, color=COL_OK)
note = ui.Label("พอร์ต 1883 ไม่เข้ารหัส ห้ามส่งของลับ", x=24, y=272,
                color=COL_WARN, value=16)
ui.poll()


def stop_here(label, msg):
    # โปรแกรมที่ล้มแล้วเงียบ คือโปรแกรมที่คนหน้างานต้องเดาเอง
    # ทุกทางออกจึงเขียนบนจอไว้ว่าติดที่ขั้นไหน แล้วจบ ไม่ค้างรอ
    label.color(COL_BAD)
    label.text(msg)
    ui.poll()
    print("หยุดที่:", msg)
    raise SystemExit


# client_id สร้างจาก TEAM ถ้าซ้ำกับคนอื่น broker จะเตะอีกฝั่งหลุด จึงไม่ยอมรันถ้ายังไม่แก้
if len(TEAM) != 6 or TEAM[:4] != "team" or not TEAM[4:].isdigit() or TEAM == "team00":
    stop_here(st1, "1) แก้ TEAM เป็นเลขของคุณก่อน เช่น team37")

# --- ขั้นที่ 1: WiFi ต้องได้ IP ก่อน ---
# ขึ้นป้าย "กำลังต่อ" ก่อนเรียก connect() เพราะระหว่างต่อ จอจะนิ่งไปพักหนึ่ง
st1.color(COL_WARN)
st1.text("1) WiFi     กำลังต่อ")
ui.poll()
if not wifi.connect(WIFI_SSID, WIFI_PASS):
    stop_here(st1, "1) WiFi     ต่อไม่ติด ตรวจชื่อและรหัส")

ip = wifi.ip()
if ip == "0.0.0.0":
    # "0.0.0.0" แปลว่ายังไม่ได้เลข IP ส่งอะไรออกไปไม่ได้
    stop_here(st1, "1) WiFi     ลิงก์ขึ้นแต่ยังไม่มี IP")
st1.color(COL_OK)
st1.text("1) WiFi     IP " + ip)
ui.poll()

# --- ขั้นที่ 2: แนะนำตัวกับ broker ---
st2.color(COL_WARN)
st2.text("2) broker   กำลังต่อ " + BROKER)
ui.poll()
try:
    linked = mqtt.connect(BROKER, port=1883, client_id="bento-aiot-" + TEAM,
                          keepalive=60)
except OSError:
    linked = False
if not linked:
    stop_here(st2, "2) broker   ต่อไม่ได้ เน็ตอาจกันพอร์ต 1883")
st2.color(COL_OK)
st2.text("2) broker   ต่อแล้ว")
ui.poll()

# --- ขั้นที่ 3: ส่งค่าจริงจากเซนเซอร์ ---
st3.color(COL_WARN)
st3.text("3) publish  " + TOPIC)
ui.poll()

sent = 0
for i in range(1, N + 1):
    knob = -1       # -1 แปลว่ารอบนี้อ่านลูกบิดไม่ได้
    az = -99.0      # -99 แปลว่ารอบนี้อ่านค่าเอียงไม่ได้
    try:
        s = sensors.snapshot()
        if "pot" in s:
            knob = int(s["pot"]["percent"])
        if "bmi270" in s:
            az = round(s["bmi270"]["az"], 2)
    except OSError:
        pass

    # คีย์สั้น ตัวเล็กทั้งหมด หน้าเว็บจะวาดกล่องหนึ่งกล่องต่อหนึ่งคีย์
    body = json.dumps({"id": TEAM, "n": i, "knob": knob, "az": az})

    try:
        ok = mqtt.publish(TOPIC, body)
    except OSError:
        stop_here(st3, "3) publish  สายหลุดที่ใบที่ " + str(i))
    if not ok:
        stop_here(st3, "3) publish  ถูกปฏิเสธที่ใบที่ " + str(i))

    sent = i
    seg.text(str(sent))
    ui.poll()
    print("ส่ง:", body)
    time.sleep_ms(GAP_MS)

st3.color(COL_OK)
st3.text("3) publish  ส่งครบ " + str(sent) + " ใบ")
note.color(COL_DIM)
note.text("is_connected() = " + str(mqtt.is_connected()))
ui.poll()

# ----- ตาคุณ -----
# ระหว่างที่ไฟล์นี้ส่ง หมุนลูกบิดหรือเอียงบอร์ด (ในอีมูเลเตอร์ใช้แผง HW)
# แล้วดูว่าเลข knob หรือ az บนหน้าเว็บขยับตามมือคุณไหม
# จดเลข n ของใบแรกที่หน้าเว็บเห็น แล้วอธิบายว่าทำไมมันไม่ใช่ใบที่ 1 เสมอไป
