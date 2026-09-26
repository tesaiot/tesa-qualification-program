// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// examples/05_find_the_overrun.c — โปรแกรมที่มีบั๊กหนึ่งจุด ไว้ฝึก GDB บนคอมพิวเตอร์ก่อนไปใช้กับบอร์ด
//
//     gcc -std=c11 -Wall -Wextra -g -O0 -o overrun 05_find_the_overrun.c
//     ./overrun
//
// ทายก่อนรัน: บรรทัด round 0 จะพิมพ์ count เท่าไร
// -g ใส่ข้อมูลสำหรับ debugger ส่วน -O0 ปิด optimisation ให้บรรทัดของโค้ดตรงกับคำสั่งเครื่อง
// (บนบอร์ด แม่แบบของ SDK build แบบ Release เป็นค่าเริ่มต้น ดูบทเรียน 3.1 ว่าต่างกันอย่างไร)
#include <stdint.h>
#include <stdio.h>

typedef struct {
    uint8_t  samples[8];   // ค่าจากเซนเซอร์ 8 ค่าล่าสุด
    uint32_t count;        // จำนวนค่าที่เก็บมาทั้งหมด อยู่ถัดจาก samples ในหน่วยความจำพอดี
} record_t;

static record_t rec;       // static: เริ่มเป็นศูนย์ทั้งก้อน

// ท่าที่ 1: เติมค่าลงบัฟเฟอร์ ฟังก์ชันนี้มีบั๊กหนึ่งจุด
static void fill_samples(record_t *r, uint8_t base)
{
    for (unsigned i = 0u; i <= 8u; i++) {
        r->samples[i] = (uint8_t)(base + i);
    }
}

int main(void)
{
    // ท่าที่ 2: เรียกสามรอบ และนับจำนวนค่าที่ควรจะมี
    for (unsigned round = 0u; round < 3u; round++) {
        fill_samples(&rec, (uint8_t)(round * 10u));
        rec.count += 8u;
        // ท่าที่ 3: เทียบกับค่าที่ควรเป็น ถ้าไม่ตรง แปลว่ามีใครเขียน count ที่เราไม่รู้
        printf("round %u: count = %u (expected %u)\n",
               round, (unsigned)rec.count, (round + 1u) * 8u);
    }
    return 0;
}
