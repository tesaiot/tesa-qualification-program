// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// examples/02_where_it_lives.c — ตัวแปรแต่ละตัวอยู่ที่ไหนในหน่วยความจำ
//
//     gcc -std=c11 -Wall -Wextra -o where_it_lives 02_where_it_lives.c
//     ./where_it_lives
//
// ทายก่อนรัน: ที่อยู่ของ local_buf กับ g_zeroed ตัวไหนมีค่ามากกว่า
// เลขที่อยู่บนคอมพิวเตอร์ของคุณจะไม่ตรงกับของเพื่อน (ระบบปฏิบัติการสุ่มตำแหน่งให้)
// แต่ "กลุ่ม" ของมันจะเหมือนกัน และบนไมโครคอนโทรลเลอร์ linker script เป็นคนกำหนดกลุ่มเหล่านี้
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int g_initialised = 42;                                   // static: .data (มีค่าเริ่มต้น ต้องคัดลอกจาก flash ตอนบูต)
int g_zeroed;                                             // static: .bss  (ศูนย์ตอนบูต ไม่กินที่ใน flash)
static const uint16_t k_table[4] = {10u, 20u, 40u, 80u};  // static: .rodata (อ่านอย่างเดียว อยู่ใน flash ได้)

static void show(const char *name, const void *addr, const char *region)
{
    printf("  %-22s %-16p %s\n", name, addr, region);
}

// ท่าที่ 3: แต่ละชั้นของการเรียกฟังก์ชันได้ stack frame ใหม่ของตัวเอง
static void depth(int level)
{
    uint32_t frame_marker = (uint32_t)level;  // local: อยู่ใน stack frame ของชั้นนี้
    printf("  depth %d: &frame_marker = %p\n", level, (void *)&frame_marker);
    if (level < 3) {
        depth(level + 1);
    }
}

int main(void)
{
    static uint32_t s_calls;      // static ในฟังก์ชัน: อายุยาวเท่าโปรแกรม อยู่ .bss ไม่ใช่ stack
    uint8_t local_buf[64] = {0};  // local: stack frame ของ main
    const char *msg = "hello";    // ตัวชี้อยู่ใน stack ส่วนข้อความอยู่ใน .rodata
    uint8_t *block = malloc(64);  // ตัวชี้อยู่ใน stack ส่วนก้อน 64 ไบต์อยู่ใน heap

    s_calls++;
    if (block == NULL) {          // malloc ล้มได้เสมอ ตรวจทุกครั้ง
        printf("malloc failed\n");
        return 1;
    }

    // ท่าที่ 1: พิมพ์ที่อยู่ แล้วจัดกลุ่มด้วยตาเอง
    printf("where each object lives:\n");
    show("k_table", (const void *)k_table, "static, read-only (.rodata)");
    show("\"hello\" literal", (const void *)msg, "static, read-only (.rodata)");
    show("g_initialised", (void *)&g_initialised, "static, initialised (.data)");
    show("g_zeroed", (void *)&g_zeroed, "static, zeroed (.bss)");
    show("s_calls", (void *)&s_calls, "static, zeroed (.bss)");
    show("block[0]", (void *)block, "heap");
    show("local_buf", (void *)local_buf, "stack");
    show("msg (the pointer)", (void *)&msg, "stack");

    // ท่าที่ 2: sizeof บอกว่าแต่ละอย่างกินกี่ไบต์ และกินจากส่วนไหน
    printf("sizes: local_buf=%zu bytes of stack, block=64 bytes of heap, k_table=%zu bytes of read-only data (flash on an MCU)\n",
           sizeof(local_buf), sizeof(k_table));

    // ท่าที่ 3: stack โตลงหรือโตขึ้น ดูจากที่อยู่ของแต่ละชั้น
    depth(1);

    free(block);                  // ทุก malloc ต้องมี free หนึ่งครั้ง และห้ามใช้ block หลังจากนี้
    block = NULL;
    return 0;
}
