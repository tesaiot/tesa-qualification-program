// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// examples/10_dma_cache_sim.c — บั๊กสองแบบของบัฟเฟอร์ที่ DMA กับ CPU ใช้ร่วมกัน จำลองบนคอมพิวเตอร์
//
// แบบจำลองนี้มี "หน่วยความจำจริง" ที่ DMA เขียน และ "cache" ของ CPU ที่เก็บสำเนาไว้
// เหมือน Cortex-M55 ที่มี data cache (โค้ดของ SDK ตรวจด้วย __DCACHE_PRESENT)
//   บั๊ก 1: CPU อ่านบัฟเฟอร์ก่อน DMA เขียนเสร็จ ได้ข้อมูลครึ่งเก่าครึ่งใหม่
//   บั๊ก 2: DMA เขียนเสร็จแล้ว แต่ CPU อ่านสำเนาเก่าจาก cache
//
//     gcc -std=c11 -Wall -Wextra -o dma_cache_sim 10_dma_cache_sim.c
//     ./dma_cache_sim
//
// ทายก่อนรัน: บรรทัด "stale cache" จะพิมพ์ค่าอะไร
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define LEN (8u)

typedef struct {
    uint8_t mem[LEN];     // หน่วยความจำจริง (DMA อ่านเขียนตรงนี้)
    uint8_t cache[LEN];   // สำเนาที่ CPU เห็น
    bool    cached;       // cache มีสำเนาของบัฟเฟอร์นี้อยู่ไหม
} buffer_t;

// CPU อ่านผ่าน cache: ถ้ามีสำเนาอยู่ ได้สำเนา ไม่ไปดูหน่วยความจำจริง
static uint8_t cpu_read(buffer_t *b, unsigned i)
{
    if (!b->cached) {
        memcpy(b->cache, b->mem, LEN);    // cache miss: โหลดทั้ง line มาเก็บ
        b->cached = true;
    }
    return b->cache[i];
}

// "invalidate": ทิ้งสำเนา ครั้งหน้า CPU จะอ่านจากหน่วยความจำจริง
static void cache_invalidate(buffer_t *b)
{
    b->cached = false;
}

// DMA เขียนหน่วยความจำจริงทีละไบต์ ไม่ผ่าน cache และไม่บอก CPU
static void dma_write_bytes(buffer_t *b, unsigned from, unsigned to, uint8_t value)
{
    for (unsigned i = from; i < to && i < LEN; i++) {
        b->mem[i] = value;
    }
}

static void print_cpu_view(const char *label, buffer_t *b)
{
    printf("%-26s", label);
    for (unsigned i = 0u; i < LEN; i++) {
        printf(" %02X", (unsigned)cpu_read(b, i));
    }
    printf("\n");
}

int main(void)
{
    buffer_t b;
    memset(&b, 0, sizeof(b));

    // ท่าที่ 1: รอบแรก DMA เติม 0xAA ครบ CPU อ่าน (cache ว่าง จึงโหลดของจริง)
    dma_write_bytes(&b, 0u, LEN, 0xAAu);
    print_cpu_view("frame 1, read after done:", &b);

    // ท่าที่ 2: บั๊ก 2 — DMA เติม 0xBB ครบแล้ว แต่ CPU ไม่ invalidate จึงได้สำเนาเก่า
    dma_write_bytes(&b, 0u, LEN, 0xBBu);
    print_cpu_view("frame 2, stale cache:", &b);
    cache_invalidate(&b);
    print_cpu_view("frame 2, after invalidate:", &b);

    // ท่าที่ 3: บั๊ก 1 — CPU อ่านขณะ DMA เพิ่งเขียนไปครึ่งเดียว (invalidate ถูกแล้ว แต่ผิดเวลา)
    dma_write_bytes(&b, 0u, LEN / 2u, 0xCCu);
    cache_invalidate(&b);
    print_cpu_view("frame 3, read too early:", &b);
    dma_write_bytes(&b, LEN / 2u, LEN, 0xCCu);   // DMA เขียนส่วนที่เหลือเสร็จทีหลัง
    cache_invalidate(&b);
    print_cpu_view("frame 3, read after done:", &b);
    return 0;
}
