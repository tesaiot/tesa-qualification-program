// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// examples/11_uart_frame.c — หนึ่งไบต์บนสาย UART หน้าตาเป็นอย่างไร
//
// เข้ารหัสไบต์เป็นลำดับบิตบนสาย (start, data แบบ LSB ก่อน, parity, stop) แล้ววาดเป็นรูปคลื่นแบบข้อความ
// พร้อมเวลาของแต่ละบิตที่ 115200 baud ซึ่งเป็นค่าของ debug UART และ UART บน header ของบอร์ดนี้
//
//     gcc -std=c11 -Wall -Wextra -o uart_frame 11_uart_frame.c
//     ./uart_frame
//
// ทายก่อนรัน: ไบต์ 0xA5 บิตแรกหลัง start bit เป็น 1 หรือ 0
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

typedef enum { PARITY_NONE, PARITY_EVEN, PARITY_ODD } parity_t;

// ท่าที่ 1: สร้างลำดับระดับสัญญาณของหนึ่งเฟรม คืนจำนวนบิต
// สายว่างอยู่ที่ 1 (idle high) start bit คือ 0 stop bit คือ 1
static unsigned uart_encode(uint8_t byte, parity_t parity, unsigned stop_bits, uint8_t *levels)
{
    unsigned n = 0u;
    unsigned ones = 0u;
    levels[n++] = 0u;                           // start
    for (unsigned i = 0u; i < 8u; i++) {        // data: LSB ก่อน (enableMsbFirst = false ในค่าตั้งของ BSP)
        const uint8_t bit = (uint8_t)((byte >> i) & 1u);
        ones += bit;
        levels[n++] = bit;
    }
    if (parity == PARITY_EVEN) {
        levels[n++] = (uint8_t)(ones & 1u);     // ทำให้จำนวน 1 รวม parity เป็นเลขคู่
    } else if (parity == PARITY_ODD) {
        levels[n++] = (uint8_t)((ones & 1u) ^ 1u);
    }
    for (unsigned i = 0u; i < stop_bits; i++) {
        levels[n++] = 1u;                       // stop
    }
    return n;
}

// ท่าที่ 2: วาดรูปคลื่นแบบข้อความ และบอกความหมายของแต่ละบิต
static void draw(const char *title, uint8_t byte, parity_t parity, unsigned stop_bits, double baud)
{
    uint8_t lv[12];
    const unsigned n = uart_encode(byte, parity, stop_bits, lv);
    printf("%s  0x%02X at %.0f baud, bit time %.2f us, frame %.1f us\n",
           title, (unsigned)byte, baud, 1e6 / baud, n * 1e6 / baud);
    printf("  idle ");
    for (unsigned i = 0u; i < n; i++) {
        printf("%s", lv[i] ? "‾‾‾" : "___");
    }
    printf(" idle\n        ");
    for (unsigned i = 0u; i < n; i++) {
        if (i == 0u) {
            printf(" S ");
        } else if (i <= 8u) {
            printf("D%u ", i - 1u);
        } else if (parity != PARITY_NONE && i == 9u) {
            printf(" P ");
        } else {
            printf(" T ");
        }
    }
    printf("\n");
}

int main(void)
{
    const double baud = 115200.0;
    // ท่าที่ 3: ไบต์เดียวกันในสองรูปแบบ และไบต์แรกที่ตัวอย่าง Header I/O Test ส่งออกทาง UART ของ header
    draw("8N1:", 0xA5u, PARITY_NONE, 1u, baud);
    draw("8E1:", 0xA5u, PARITY_EVEN, 1u, baud);
    draw("8N1:", 0x11u, PARITY_NONE, 1u, baud);
    printf("8N1 throughput at %.0f baud: %.0f bytes/s (10 bit times per byte)\n", baud, baud / 10.0);
    return 0;
}
