# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
#
# solution/feature.mk — เฉลยของ practice/feature.mk
#
# โจทย์: ให้ feature/feature.c ถูกคอมไพล์เฉพาะเมื่อ ENABLE_FEATURE เป็น 1
#   - ค่าเริ่มต้นเป็น 0 (ปิด)
#   - เปิดได้ทั้งจาก command line (make ... ENABLE_FEATURE=1) และจาก environment (ENABLE_FEATURE=1 make ...)
#   - ค่าที่มีช่องว่างต่อท้ายโดยไม่ตั้งใจ เช่น 'ENABLE_FEATURE=1 ' ต้องยังนับว่าเปิด
#
#     make -f feature.mk check    -> PASS ครบสี่บรรทัด

# ?= ให้ค่าเฉพาะเมื่อตัวแปรยังไม่ถูกนิยาม ค่าจาก environment จึงอยู่รอด
# (ค่าจาก command line ชนะทั้ง := และ ?= อยู่แล้ว test ที่สองจึงผ่านตั้งแต่ก่อนแก้)
ENABLE_FEATURE ?= 0

# ifeq เทียบข้อความตรงตัว $(strip) ตัดช่องว่างหน้าและหลังออกก่อนเทียบ
# ไฟล์ที่ไม่อยู่ใน SOURCES ไม่ถูกคอมไพล์ จึงไม่มีโค้ดของมันสักไบต์ใน image
SOURCES := main.c util.c
ifeq ($(strip $(ENABLE_FEATURE)),1)
SOURCES += feature/feature.c
endif

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
