# SPDX-FileCopyrightText: 2026 Thai Embedded Systems Association (TESA)
# SPDX-License-Identifier: Apache-2.0
#
# Makefile — build และรัน unit test บนคอมพิวเตอร์ ไม่ต้องใช้ ModusToolbox
#
#   make test                                         รัน test_level_alarm_first.c
#   make test TEST=../practice/test_level_alarm.c     รันไฟล์ test อื่น
#   make test UNITY_DIR=/path/to/Unity/src            ถ้า Unity อยู่ที่อื่น
#   make clean
#
# CFLAGS ใช้ -Werror ให้คำเตือนกลายเป็นความล้มเหลว แบบเดียวกับ Makefile ของ host test ใน SDK (arduino_shield/test)

CC        ?= cc
UNITY_DIR ?= unity/src
TEST      ?= test_level_alarm_first.c
CFLAGS    := -std=c11 -Wall -Wextra -Werror -Wshadow -I. -I$(UNITY_DIR)
# ตั้งชื่อไฟล์ทดสอบจากพาธเต็ม ไม่ใช่ชื่อไฟล์อย่างเดียว: practice/ กับ solution/ มีไฟล์ชื่อเดียวกัน
# ถ้าใช้แค่ชื่อไฟล์ make จะเห็นไฟล์ของอีกฝั่งที่ใหม่กว่า แล้วรันของเก่าโดยไม่ build ใหม่
BIN       := build/$(subst /,_,$(subst ../,,$(basename $(TEST))))

.PHONY: test clean
test: $(BIN)
	./$(BIN)

$(BIN): $(TEST) level_alarm.c level_alarm.h $(UNITY_DIR)/unity.c
	@mkdir -p build
	$(CC) $(CFLAGS) -o $@ $(TEST) level_alarm.c $(UNITY_DIR)/unity.c

clean:
	rm -rf build
