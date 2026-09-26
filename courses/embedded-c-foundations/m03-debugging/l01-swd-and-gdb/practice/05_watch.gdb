# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
#
# practice/05_watch.gdb — ฝึกเติม: สคริปต์ GDB ที่ตามหาว่าใครเขียนทับ rec.count
# ใช้กับ examples/05_find_the_overrun.c ที่คอมไพล์แล้วด้วย -g -O0 แล้วรัน:
#     gdb -q -batch -x 05_watch.gdb ./overrun
#
# มีช่องให้เติม 3 จุด แทน ____ ด้วยคำสั่งหรือชื่อที่ถูก (บรรทัดที่ยังมี ____ จะทำให้ GDB แจ้ง error)
# ผลที่ต้องได้: GDB หยุดที่บรรทัดในลูปของ fill_samples พร้อมบอกค่าเก่าและค่าใหม่ของ count และ i มีค่า 8
# ลองเองก่อนอย่างน้อย 15 นาที แล้วค่อยเปิด solution/05_watch.gdb

set pagination off

# TODO 1: ตั้ง breakpoint ที่ต้นฟังก์ชันที่เติมค่าลงบัฟเฟอร์
break ____
run

# หยุดที่ต้นฟังก์ชันแล้ว ดูว่าได้อาร์กิวเมนต์อะไรมา และ struct ตอนนี้เป็นอย่างไร
info args
print *r

# TODO 2: เฝ้าดูการเขียนลงช่อง count ของ struct ที่ r ชี้อยู่
#         ใช้ watch -l เพื่อเฝ้า "ที่อยู่" นั้นต่อไปแม้จะออกจากฟังก์ชันนี้แล้ว
watch -l ____
continue

# GDB หยุดตรงคำสั่งที่เขียน count แล้ว
# TODO 3: พิมพ์ call stack ว่ามาถึงบรรทัดนี้ได้อย่างไร
____
print i
print r->samples
quit
