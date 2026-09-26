# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
#
# examples/flags.mk — ตัวแปรของ GNU Make ที่แม่แบบเฟิร์มแวร์ของ SDK ใช้ ในไฟล์เล็ก ๆ ที่รันบนคอมพิวเตอร์ได้
# ไฟล์นี้ไม่คอมไพล์อะไรเลย แค่พิมพ์ว่า make "เข้าใจ" ตัวแปรแต่ละตัวว่าอย่างไร
#
#     make -f flags.mk
#     make -f flags.mk ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/io/04_gpio_led_button
#     ENABLE_PAGE_EXAMPLES=1 make -f flags.mk
#
# ทายก่อนรันแต่ละแบบ ว่าบรรทัด SOURCES จะมีกี่ไฟล์
#
# หมายเหตุ: ห้ามเขียนคอมเมนต์ต่อท้ายบรรทัดกำหนดค่า ช่องว่างก่อน # จะกลายเป็นส่วนหนึ่งของค่า
# (ยกเว้นบรรทัด TRAILING ที่ตั้งใจทำให้ดู)

# ท่าที่ 1: ?= ให้ค่าเริ่มต้นเฉพาะเมื่อยังไม่มีใครให้ค่ามาก่อน (จาก command line หรือ environment)
# เป็นรูปแบบเดียวกับ proj_cm33_ns/Makefile ของ SDK
ENABLE_PAGE_EXAMPLES ?= 0
SDK_EXAMPLE_CM33 ?=

# ท่าที่ 2: = ขยายค่าทุกครั้งที่ถูกใช้ ส่วน := ขยายครั้งเดียวตอนอ่านบรรทัดนั้น
GREETING = hello $(WHO)
FROZEN := hello $(WHO)
WHO = world

# ท่าที่ 3: เลือกไฟล์ที่จะคอมไพล์ด้วยเงื่อนไข ไฟล์ที่ไม่อยู่ในรายการไม่ถูกคอมไพล์ ไม่มี object ไม่มีอะไรให้ลิงก์
# (ModusToolbox หาซอร์สเองจากการเดินทั้งโฟลเดอร์ แม่แบบจึงใช้ CY_IGNORE ตัดโฟลเดอร์ออก ผลลัพธ์เดียวกัน)
SOURCES := main.c sensor_auto_task.c
ifeq ($(strip $(ENABLE_PAGE_EXAMPLES)),1)
SOURCES += examples/sdk_examples_cm33.c examples/io/04_gpio_led_button.c
endif
DEFINES := ENABLE_PAGE_EXAMPLES=$(ENABLE_PAGE_EXAMPLES) SDK_EXAMPLE_CM33="$(SDK_EXAMPLE_CM33)"

# ท่าที่ 4: กับดักช่องว่างต่อท้าย ค่าของ TRAILING คือ "1 " (มีช่องว่าง) เพราะคอมเมนต์ต่อท้าย
# ifeq เทียบข้อความตรงตัว จึงไม่เท่ากับ 1 จนกว่าจะ strip (Appendix X #23 ของเอกสาร SDK คือกับดักนี้)
TRAILING := 1 # this comment leaves a trailing space in the value
ifeq ($(TRAILING),1)
TRAILING_RAW := yes
else
TRAILING_RAW := no
endif
ifeq ($(strip $(TRAILING)),1)
TRAILING_STRIPPED := yes
else
TRAILING_STRIPPED := no
endif

$(info ENABLE_PAGE_EXAMPLES = [$(ENABLE_PAGE_EXAMPLES)]  origin: $(origin ENABLE_PAGE_EXAMPLES))
$(info SDK_EXAMPLE_CM33     = [$(SDK_EXAMPLE_CM33)]  origin: $(origin SDK_EXAMPLE_CM33))
$(info GREETING (=)         = [$(GREETING)])
$(info FROZEN (:=)          = [$(FROZEN)])
$(info SOURCES              = $(SOURCES)  ($(words $(SOURCES)) files))
$(info DEFINES              = $(DEFINES))
$(info TRAILING             = [$(TRAILING)]  equals 1: $(TRAILING_RAW)  equals 1 after strip: $(TRAILING_STRIPPED))

.PHONY: all
all:
	@:
