# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
#
# solution/05_watch.gdb — เฉลยของ practice/05_watch.gdb
# ใช้กับ examples/05_find_the_overrun.c ที่คอมไพล์แล้วด้วย -g -O0 แล้วรัน:
#     gdb -q -batch -x 05_watch.gdb ./overrun
#
# ผลที่ต้องได้: GDB หยุดที่บรรทัดในลูปของ fill_samples พร้อมบอกค่าเก่าและค่าใหม่ของ count และ i มีค่า 8
# นั่นคือหลักฐานว่าคนที่เขียนทับ count คือ r->samples[8] ซึ่งอยู่นอกอาร์เรย์ (ลูปใช้ <= แทน <)

set pagination off

# breakpoint ที่ชื่อฟังก์ชัน: หยุดหลัง prologue ของฟังก์ชัน ก่อนบรรทัดแรกของตัวฟังก์ชัน
break fill_samples
run

# หยุดที่ต้นฟังก์ชันแล้ว ดูว่าได้อาร์กิวเมนต์อะไรมา และ struct ตอนนี้เป็นอย่างไร
info args
print *r

# watch -l (-location) คำนวณที่อยู่ของ r->count ครั้งเดียวแล้วเฝ้าที่อยู่นั้น
# ถ้าเขียน watch r->count เฉย ๆ GDB จะลบ watchpoint ทิ้งเมื่อออกจาก fill_samples เพราะ r เป็นตัวแปร local
watch -l r->count
continue

# GDB หยุดตรงคำสั่งที่เขียน count แล้ว
# backtrace (ย่อ bt) บอกว่าเรามาถึงบรรทัดนี้ผ่านฟังก์ชันไหนบ้าง
bt
print i
print r->samples
quit
