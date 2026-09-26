from machine import Pin
import time

led = Pin("LED", Pin.OUT)
while True:
    ____          # สลับสถานะ LED
    time.sleep(0.5)
