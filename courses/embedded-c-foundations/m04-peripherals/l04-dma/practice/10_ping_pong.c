// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// practice/10_ping_pong.c — ฝึกเติม: บัฟเฟอร์สองก้อนสลับกัน (ping-pong) ระหว่าง DMA กับ CPU
//
// แบบเดียวกับไดรเวอร์กล้องใน SDK ที่ให้ DMA เขียน line_buffer[row_buffer_flag] แล้วสลับ flag ทุกบรรทัด
// ขณะ DMA เติมก้อนหนึ่ง CPU ประมวลผลอีกก้อน กติกาของแบบฝึก
//   - DMA เขียนได้เฉพาะก้อนที่ไม่มีข้อมูลรอ (ready) และไม่ได้อยู่ในมือ CPU (in_use)
//   - เมื่อ DMA เสร็จหนึ่งก้อน ถ้าอีกก้อนว่าง ประกาศก้อนนี้ว่าพร้อมแล้วสลับไปเขียนอีกก้อน
//     ถ้าอีกก้อนไม่ว่าง (CPU ช้า) นับ overrun และเขียนทับก้อนเดิม ห้ามแตะก้อนของ CPU
//   - CPU ต้อง invalidate cache ของก้อนที่ได้มาก่อนอ่านเสมอ (ในแบบจำลองนี้คือ cache_invalidate)
// มีช่องให้เติม 6 จุด (มองหา TODO) ซึ่งมากที่สุดในโมดูลนี้
//     gcc -std=c11 -Wall -Wextra -o ping_pong 10_ping_pong.c && ./ping_pong
// ก่อนเติม test จะล้ม ลองเองก่อนอย่างน้อย 15 นาที แล้วค่อยเปิด solution/10_ping_pong.c
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define LEN (4u)

// ---- แบบจำลองหน่วยความจำกับ cache (ให้มาแล้ว เหมือน examples/10_dma_cache_sim.c) ----
typedef struct {
    uint8_t mem[LEN];
    uint8_t cache[LEN];
    bool    cached;
} buffer_t;

static uint8_t cpu_read(buffer_t *b, unsigned i)
{
    if (!b->cached) {
        memcpy(b->cache, b->mem, LEN);
        b->cached = true;
    }
    return b->cache[i];
}

static void cache_invalidate(buffer_t *b)
{
    b->cached = false;
}

// ---- ping-pong ----
typedef struct {
    buffer_t buf[2];
    bool     ready[2];    // มีข้อมูลที่ DMA เขียนเสร็จ รอ CPU
    bool     in_use[2];   // CPU กำลังอ่านอยู่
    unsigned dma_idx;     // ก้อนที่ DMA กำลังเขียน
    unsigned overruns;    // จำนวนครั้งที่ CPU ช้าจน DMA ต้องเขียนทับก้อนเดิม
} pingpong_t;

// เรียกจาก ISR "DMA done" หลัง DMA เขียนก้อน dma_idx เสร็จ
static void pp_dma_complete(pingpong_t *p)
{
    const unsigned cur = p->dma_idx;
    const unsigned other = 1u - cur;
    (void)cur;
    (void)other;

    /* TODO 1: ตรวจว่าก้อน other ว่างไหม (ไม่ ready และไม่ in_use) */

    /* TODO 2: ถ้าว่าง ประกาศว่าก้อน cur พร้อมแล้ว และเปลี่ยน dma_idx ไปที่ other */

    /* TODO 3: ถ้าไม่ว่าง เพิ่ม overruns แล้วให้ DMA เขียนก้อน cur ต่อ (ข้อมูลรอบนี้หาย) */
}

// CPU ขอก้อนที่พร้อม คืนหมายเลขก้อน หรือ -1 ถ้าไม่มี
static int pp_cpu_acquire(pingpong_t *p)
{
    (void)p;
    (void)cache_invalidate;   // บรรทัดนี้แค่กันคำเตือนของคอมไพเลอร์ จนกว่าคุณจะเรียกมันใน TODO 5
    /* TODO 4: หาก้อนที่ ready และยังไม่ in_use ถ้าเจอ ให้ตั้ง in_use แล้วคืนหมายเลขก้อน */

    /* TODO 5: ก่อนคืนก้อนให้ CPU อ่าน ต้อง invalidate cache ของก้อนนั้น ไม่อย่างนั้นอาจได้สำเนาเก่า */
    return -1;
}

// CPU อ่านเสร็จ คืนก้อนให้ DMA ใช้ได้อีก
static void pp_cpu_release(pingpong_t *p, int idx)
{
    (void)p;
    (void)idx;
    /* TODO 6: ล้าง ready และ in_use ของก้อนนั้น */
}

// ---- ให้มาแล้ว: จำลอง DMA เขียนก้อนปัจจุบันด้วยค่าเดียวทั้งก้อน ----
static void dma_fill(pingpong_t *p, uint8_t value)
{
    memset(p->buf[p->dma_idx].mem, value, LEN);
}

static int failures = 0;
#define CHECK_EQ(expected, actual)                                                          \
    do {                                                                                    \
        long e_ = (long)(expected), a_ = (long)(actual);                                    \
        if (e_ != a_) {                                                                     \
            printf("FAIL line %d: %s expected %ld got %ld\n", __LINE__, #actual, e_, a_);   \
            failures++;                                                                     \
        }                                                                                   \
    } while (0)

int main(void)
{
    static pingpong_t p;

    // CPU อ่านก้อน 0 หนึ่งครั้งก่อนเริ่ม ทำให้ cache มีสำเนาเก่าของก้อน 0 อยู่ (สถานการณ์จริงที่เจอบ่อย)
    (void)cpu_read(&p.buf[0], 0u);

    CHECK_EQ(-1, pp_cpu_acquire(&p));          // ยังไม่มีอะไรพร้อม

    dma_fill(&p, 0x11u);                        // DMA เติมก้อน 0
    pp_dma_complete(&p);
    CHECK_EQ(1, p.dma_idx);                     // สลับไปเขียนก้อน 1

    int idx = pp_cpu_acquire(&p);
    CHECK_EQ(0, idx);
    if (idx >= 0) {
        CHECK_EQ(0x11, cpu_read(&p.buf[idx], 0u));   // ต้องเห็นข้อมูลใหม่ ไม่ใช่สำเนาเก่าใน cache
    }

    dma_fill(&p, 0x22u);                        // ระหว่างที่ CPU ถือก้อน 0 DMA เติมก้อน 1
    pp_dma_complete(&p);                        // ก้อน 0 อยู่ในมือ CPU: DMA ต้องไม่สลับไปทับ
    CHECK_EQ(1, p.dma_idx);
    CHECK_EQ(1u, p.overruns);

    if (idx >= 0) {
        pp_cpu_release(&p, idx);                // CPU คืนก้อน 0
    }
    dma_fill(&p, 0x33u);                        // DMA เขียนก้อน 1 ใหม่ (ข้อมูล 0x22 หายไปแล้ว นั่นคือ overrun)
    pp_dma_complete(&p);
    CHECK_EQ(0, p.dma_idx);

    idx = pp_cpu_acquire(&p);
    CHECK_EQ(1, idx);
    if (idx >= 0) {
        CHECK_EQ(0x33, cpu_read(&p.buf[idx], 3u));
        pp_cpu_release(&p, idx);
    }
    CHECK_EQ(-1, pp_cpu_acquire(&p));          // คืนแล้ว ไม่มีอะไรค้าง

    printf("%s: %d failure(s)\n", failures ? "FAIL" : "PASS", failures);
    return failures ? 1 : 0;
}
