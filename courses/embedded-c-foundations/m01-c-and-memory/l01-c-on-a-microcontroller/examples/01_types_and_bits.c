// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// examples/01_types_and_bits.c — ชนิดข้อมูลขนาดแน่นอน overflow และการจัดการบิต
// รันบนคอมพิวเตอร์ของคุณได้เลย ไม่ต้องมีบอร์ด:
//
//     gcc -std=c11 -Wall -Wextra -o types_and_bits 01_types_and_bits.c
//     ./types_and_bits
//
// ทายก่อนรันว่าบรรทัด "count after +10" จะพิมพ์เลขอะไร
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

// "รีจิสเตอร์" จำลองหนึ่งตัว บนชิปจริงนี่คือที่อยู่ในหน่วยความจำที่ฮาร์ดแวร์เปลี่ยนค่าได้เอง
// จึงต้องเป็น volatile: บอกคอมไพเลอร์ว่าทุกการอ่านและเขียนต้องเกิดขึ้นจริงทุกครั้ง
static volatile uint32_t fake_ctrl = 0x00000005u;

#define CTRL_ENABLE_POS   (0u)
#define CTRL_ENABLE_MSK   (1u << CTRL_ENABLE_POS)       // bit 0
#define CTRL_MODE_POS     (4u)
#define CTRL_MODE_MSK     (0x7u << CTRL_MODE_POS)       // bits 4..6 (ฟิลด์ 3 บิต)

int main(void)
{
    // ท่าที่ 1: ขนาดของชนิดข้อมูลคือสัญญา ไม่ใช่ความบังเอิญของเครื่อง
    printf("sizeof: uint8_t=%zu uint16_t=%zu uint32_t=%zu uint64_t=%zu int=%zu\n",
           sizeof(uint8_t), sizeof(uint16_t), sizeof(uint32_t), sizeof(uint64_t), sizeof(int));

    uint8_t count = 250u;
    count = (uint8_t)(count + 10u);                    // 260 ไม่พอดี 8 บิต จึงวนกลับ (modulo 256)
    printf("count after +10 = %u\n", (unsigned)count);

    // ประกอบ int16 จากสองไบต์ little-endian แบบเดียวกับที่ SDK อ่านค่า accelerometer
    const uint8_t lsb = 0x30u, msb = 0xF8u;            // 0xF830 = -2000 ในแบบ two's complement
    const int16_t raw = (int16_t)((uint16_t)lsb | ((uint16_t)msb << 8));
    printf("raw int16 from bytes = %d\n", (int)raw);

    // คูณเลขใหญ่: 175000 * 65535 = 11,468,625,000 ใหญ่กว่า UINT32_MAX (4,294,967,295)
    const uint32_t t_raw = 65535u;
    const uint32_t wrong = 175000u * t_raw;            // คูณใน 32 บิต ผลวนกลับ
    const uint64_t right = (uint64_t)175000u * t_raw;  // ขยายเป็น 64 บิตก่อนคูณ
    printf("32-bit product = %" PRIu32 ", 64-bit product = %" PRIu64 "\n", wrong, right);

    // ท่าที่ 2: read-modify-write อ่านค่าเดิม แก้เฉพาะบิตของเรา แล้วเขียนกลับ
    printf("ctrl start      = 0x%08" PRIX32 "\n", fake_ctrl);
    fake_ctrl |= CTRL_ENABLE_MSK;                      // set: OR กับ mask
    fake_ctrl &= ~(uint32_t)0x4u;                      // clear bit 2: AND กับ ~mask
    fake_ctrl ^= (1u << 8);                            // toggle bit 8: XOR กับ mask
    printf("ctrl after RMW  = 0x%08" PRIX32 "\n", fake_ctrl);

    // ท่าที่ 3: เขียนฟิลด์หลายบิต ต้องล้างฟิลด์ก่อนแล้วค่อยใส่ค่าใหม่ ไม่งั้นบิตเก่าค้าง
    const uint32_t mode = 5u;                          // ค่าที่อยากใส่ในฟิลด์ MODE
    uint32_t v = fake_ctrl;                            // read (อ่านครั้งเดียว)
    v &= ~CTRL_MODE_MSK;                               // modify: ล้างฟิลด์
    v |= (mode << CTRL_MODE_POS) & CTRL_MODE_MSK;      // modify: ใส่ค่าใหม่ ตัดส่วนเกินด้วย mask
    fake_ctrl = v;                                     // write (เขียนครั้งเดียว)
    printf("ctrl MODE=5     = 0x%08" PRIX32 ", MODE reads back %" PRIu32 "\n",
           fake_ctrl, (fake_ctrl & CTRL_MODE_MSK) >> CTRL_MODE_POS);
    return 0;
}
