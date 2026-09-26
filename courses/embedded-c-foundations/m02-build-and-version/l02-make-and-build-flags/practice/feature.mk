# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
#
# practice/feature.mk — ฝึกเติม: ตัวแปรเปิดปิดส่วนหนึ่งของเฟิร์มแวร์ แบบเดียวกับ ENABLE_PAGE_EXAMPLES ของ SDK
#
# โจทย์: ให้ feature/feature.c ถูกคอมไพล์เฉพาะเมื่อ ENABLE_FEATURE เป็น 1
#   - ค่าเริ่มต้นเป็น 0 (ปิด)
#   - เปิดได้ทั้งจาก command line (make ... ENABLE_FEATURE=1) และจาก environment (ENABLE_FEATURE=1 make ...)
#   - ค่าที่มีช่องว่างต่อท้ายโดยไม่ตั้งใจ เช่น 'ENABLE_FEATURE=1 ' ต้องยังนับว่าเปิด
#
# มีช่องให้เติม 2 จุด (มองหา TODO) ตรวจงานด้วย:
#     make -f feature.mk check
# ก่อนแก้จะเห็น FAIL บางบรรทัด แก้จนขึ้น PASS ครบสี่บรรทัด
# ลองเองก่อนอย่างน้อย 15 นาที แล้วค่อยเปิด solution/feature.mk

# TODO 1: บรรทัดนี้ให้ค่าเริ่มต้นเป็น 0 ก็จริง แต่ตัวดำเนินการ := เขียนทับค่าที่มาจาก environment
#         เปลี่ยนตัวดำเนินการให้ make ใช้ 0 เฉพาะเมื่อยังไม่มีใครให้ค่า
ENABLE_FEATURE := 0

# TODO 2: ตอนนี้ feature/feature.c ถูกคอมไพล์เสมอ ทำให้มันอยู่ในรายการเฉพาะเมื่อ ENABLE_FEATURE เป็น 1
#         ใช้ ifeq แบบเดียวกับ examples/flags.mk และอย่าลืมกับดักช่องว่างต่อท้าย
SOURCES := main.c util.c feature/feature.c

# ----- ส่วนตรวจงาน ไม่ต้องแก้ -----
# print พิมพ์ "ค่าของธง|รายการซอร์ส" แล้ว check เทียบกับคำตอบที่ถูกของแต่ละกรณี
THIS := $(firstword $(MAKEFILE_LIST))
SUB := $(MAKE) --no-print-directory -s -f $(THIS) print
OFF := 0|main.c util.c
ON := 1|main.c util.c feature/feature.c

.PHONY: print check
print:
	@echo "$(strip $(ENABLE_FEATURE))|$(SOURCES)"

check:
	@fails=0; \
	 r="$$($(SUB))"; \
	 if [ "$$r" = "$(OFF)" ]; then echo "PASS default is off"; else echo "FAIL default is off: got '$$r'"; fails=$$((fails + 1)); fi; \
	 r="$$($(SUB) ENABLE_FEATURE=1)"; \
	 if [ "$$r" = "$(ON)" ]; then echo "PASS command line turns it on"; else echo "FAIL command line turns it on: got '$$r'"; fails=$$((fails + 1)); fi; \
	 r="$$(ENABLE_FEATURE=1 $(SUB))"; \
	 if [ "$$r" = "$(ON)" ]; then echo "PASS environment turns it on"; else echo "FAIL environment turns it on: got '$$r'"; fails=$$((fails + 1)); fi; \
	 r="$$($(SUB) 'ENABLE_FEATURE=1 ')"; \
	 if [ "$$r" = "$(ON)" ]; then echo "PASS trailing space still counts as on"; else echo "FAIL trailing space still counts as on: got '$$r'"; fails=$$((fails + 1)); fi; \
	 [ $$fails -eq 0 ] || { echo "$$fails check(s) failed"; exit 1; }
