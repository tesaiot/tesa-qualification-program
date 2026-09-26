// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// examples/13_spi_modes.c — โหมด SPI ทั้งสี่ หน้าตาเป็นอย่างไรบนสาย SCLK และ MOSI
//
// วาดหนึ่งไบต์ (MSB ก่อน) ในแต่ละโหมด แล้วทำเครื่องหมาย ^ ใต้ขอบที่ผู้รับอ่านค่า (sample)
// โหมด = CPOL * 2 + CPHA
//   CPOL: ระดับของ SCLK ตอนว่าง (0 = ต่ำ, 1 = สูง)
//   CPHA: อ่านที่ขอบแรกหลังออกจากระดับว่าง (0) หรือขอบที่สอง (1)
//
//     gcc -std=c11 -Wall -Wextra -o spi_modes 13_spi_modes.c
//     ./spi_modes
//
// ทายก่อนรัน: ในโหมด 3 ผู้รับอ่านที่ขอบขาขึ้นหรือขาลงของ SCLK
#include <stdint.h>
#include <stdio.h>

// ท่าที่ 1: สร้างรูปคลื่นของหนึ่งไบต์ เป็นลำดับครึ่งคาบเวลา (half period) ของ SCLK
static void draw(unsigned mode, uint8_t byte)
{
    const unsigned cpol = (mode >> 1) & 1u;
    const unsigned cpha = mode & 1u;
    char sclk[64], mosi[64], mark[64];
    unsigned n = 0u;

    for (int bit = 7; bit >= 0; bit--) {             // MSB ก่อน (enableMsbFirst = true ในค่าตั้ง SPI ของ BSP)
        const char d = ((byte >> bit) & 1u) ? '1' : '0';
        // ครึ่งแรกของบิต: SCLK ยังอยู่ระดับว่าง (CPHA 0) หรือเพิ่งออกจากระดับว่าง (CPHA 1)
        sclk[n] = (char)('0' + (cpha ? !cpol : cpol));
        mosi[n] = d;
        mark[n] = ' ';
        n++;
        // ครึ่งหลังของบิต: ขอบที่ผู้รับอ่าน อยู่ที่จุดเปลี่ยนเข้าครึ่งนี้
        sclk[n] = (char)('0' + (cpha ? cpol : !cpol));
        mosi[n] = d;
        mark[n] = '^';
        n++;
    }
    sclk[n] = mosi[n] = mark[n] = '\0';

    // ท่าที่ 2: แปลงเลข 0/1 เป็นเส้นให้อ่านง่าย
    printf("mode %u (CPOL=%u CPHA=%u), byte 0x%02X, idle SCLK=%u\n", mode, cpol, cpha, (unsigned)byte, cpol);
    const char *idle = cpol ? "‾‾" : "__";            // ก่อนและหลังเฟรม SCLK อยู่ระดับว่าง
    printf("  SCLK  %s|", idle);
    for (unsigned i = 0u; i < n; i++) printf("%s", sclk[i] == '1' ? "‾‾" : "__");
    printf("|%s\n  MOSI  --|", idle);
    for (unsigned i = 0u; i < n; i++) printf("%s", mosi[i] == '1' ? "‾‾" : "__");
    printf("|--\n  read    |");
    for (unsigned i = 0u; i < n; i++) printf("%c ", mark[i]);
    printf("|\n");
}

int main(void)
{
    for (unsigned mode = 0u; mode < 4u; mode++) {
        draw(mode, 0xA5u);
    }
    // ท่าที่ 3: ความเร็วของ SPI สองแบบบนบอร์ดเดียวกัน
    // SPI ของเรดาร์: สัญญาณนาฬิกา 100 MHz, oversample 4 -> 25 MHz (ค่าตั้งใน BSP ของ SDK)
    // SPI แบบ bit-bang ของตัวอย่าง Header I/O Test: หน่วง 5 us สามครั้งต่อบิต -> ราว 15 us ต่อบิต
    printf("radar SPI: %.1f MHz SCLK; header bit-bang: about %.1f kHz (%.0f times slower)\n",
           100.0 / 4.0, 1000.0 / 15.0, 25e6 / (1e6 / 15.0));
    return 0;
}
