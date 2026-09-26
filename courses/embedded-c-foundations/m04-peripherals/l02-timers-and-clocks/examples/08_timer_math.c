// SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
// SPDX-License-Identifier: Apache-2.0
//
// examples/08_timer_math.c — คำนวณเวลาจากสัญญาณนาฬิกา ตัวหาร และค่า period ด้วยค่าจริงจาก BSP ของ SDK
//
// ค่าทุกตัวข้างล่างอ่านมาจากไฟล์ที่ Device Configurator สร้างไว้ในแม่แบบ mtb-only ของ SDK (commit ef72c1b):
//   CLK_HF10 = 100 MHz                          cycfg_clocks.c  (CY_CFG_SYSCLK_CLKHF10_FREQ_MHZ)
//   TCPWM0 SCB2 SCB3 อยู่ในกลุ่ม peri ที่ใช้ CLK_HF10   pse84_config.h
//   ตัวหารของแต่ละอุปกรณ์                          cycfg_peripheral_clocks.c (Cy_SysClk_PeriPclkSetDivider)
//   period, oversample, duty cycle ของ I2C          cycfg_peripherals.c
// PDL บอกว่าค่าตัวหาร N "causes integer division of (divider value + 1)"
//
//     gcc -std=c11 -Wall -Wextra -o timer_math 08_timer_math.c
//     ./timer_math
//
// ทายก่อนรัน: GENERAL_PURPOSE_TIMER ที่ BSP ตั้งไว้ จะ overflow ทุกกี่มิลลิวินาที
#include <stdint.h>
#include <stdio.h>

#define CLK_HF10_HZ (100000000.0)

// ท่าที่ 1: สัญญาณนาฬิกาหลังตัวหาร
static double divided_hz(double src_hz, uint32_t divider_value)
{
    return src_hz / ((double)divider_value + 1.0);
}

int main(void)
{
    // ท่าที่ 2: timer นับขึ้นจาก 0 ถึง period แล้วเกิด terminal count รวม period + 1 จังหวะต่อรอบ
    const double gp_hz = divided_hz(CLK_HF10_HZ, 9999u);          // GENERAL_PURPOSE_TIMER: 16-bit divider 9999
    const double gp_period_s = (9999.0 + 1.0) / gp_hz;            // period = 9999
    printf("GENERAL_PURPOSE_TIMER: counter clock %.0f Hz, overflow every %.1f ms\n",
           gp_hz, gp_period_s * 1000.0);

    const double pwm_hz = divided_hz(CLK_HF10_HZ, 49999u);        // PWM_LED_CTRL: 16-bit divider 49999
    const double pwm_period_s = (2000.0 + 1.0) / pwm_hz;          // period0 = 2000, compare0 = 1000 (สมมติว่านับ 0..period แบบ counter ตรวจกับ TRM ของชิป)
    printf("PWM_LED_CTRL: counter clock %.0f Hz, PWM period %.4f s, duty about %.1f%%\n",
           pwm_hz, pwm_period_s, 100.0 * 1000.0 / 2001.0);

    // ท่าที่ 3: สัญญาณนาฬิกาเดียวกันกำหนดความเร็วของบัสด้วย และความคลาดเคลื่อนมาจากการหารที่ไม่ลงตัว
    const double uart_baud = divided_hz(CLK_HF10_HZ, 86u) / 10.0; // DEBUG_UART: divider 86, oversample 10
    printf("DEBUG_UART: %.0f baud, %+.2f%% from 115200\n",
           uart_baud, 100.0 * (uart_baud - 115200.0) / 115200.0);

    const double i2c_hz = divided_hz(CLK_HF10_HZ, 9u) / (16.0 + 9.0); // I2C_CONTROLLER: divider 9, low 16 + high 9
    printf("I2C_CONTROLLER: %.0f Hz SCL\n", i2c_hz);

    const double spi_hz = divided_hz(CLK_HF10_HZ, 0u) / 4.0;      // SPI_CONTROLLER (radar): divider 0, oversample 4
    printf("SPI_CONTROLLER: %.0f Hz SCLK\n", spi_hz);
    return 0;
}
