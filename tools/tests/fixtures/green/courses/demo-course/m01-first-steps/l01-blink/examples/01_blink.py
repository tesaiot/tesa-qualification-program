# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
from machine import Pin
import time

WIFI_SSID = "<ชื่อเครือข่ายของคุณ>"
WIFI_PASS = "<รหัสผ่านของคุณ>"
led = Pin("LED", Pin.OUT)
while True:
    led.toggle()
    time.sleep(0.5)
