---
id: c-found.m03.l02
lang: en
title: {th: วินิจฉัยความผิดพลาดจากหลักฐาน, en: Diagnosing faults from evidence}
summary: {th: แยกสาเหตุของความผิดพลาดด้วยตัวนับและผลลัพธ์ที่ตรงไปตรงมา แทนการเดาจาก log ที่ดูน่าเชื่อ, en: Separate fault causes with honest counters and result codes instead of guessing from reassuring logs.}
level: L3
time_min: {concept: 15, practise: 25, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [c-found.m03.l01]
objectives:
- {th: ตั้งสมมติฐานอย่างน้อยสามข้อสำหรับอาการ 'ไม่มีผลลัพธ์' และเลือกหลักฐานที่แยกแต่ละข้อออกจากกัน, en: Form at least three hypotheses for a 'no result' symptom and pick evidence that separates them.}
- {th: อ่านตัวนับวินิจฉัยของ SDK แล้วระบุได้ว่าความผิดพลาดอยู่ขั้นใด, en: Read the SDK's diagnostic counters and locate the failing stage.}
- {th: อธิบายว่าทำไมฟังก์ชันควรคืนผลลัพธ์ที่บอกความจริง เช่น ไม่พร้อม หรือไม่มีข้อมูล แทนการแกล้งว่าสำเร็จ, en: Explain why functions should return honest results such as unavailable or no data instead of pretending success.}
develops:
- {skill: debug.gdb, to: 3}
- {skill: soft.problem-solving, to: 3}
context: {platform: psoc-edge-e84, lang: c, toolchain: modustoolbox, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
slides: slides.md
source_sha256: 7f6559a70cf3fa9a073bfbaef0258e5f6b27be7ab881ded440bc3aec23e40b09
---

## Objectives

By the end of this lesson, you will be able to

1. Form at least three hypotheses for a "no result" symptom, and choose evidence that separates each one from the others.
2. Read the SDK's diagnostic counters and identify which stage is failing.
3. Explain why a function should return an honest result — such as unavailable or no data — instead of pretending success.

Takes about 70 minutes (concepts 15 · practice 25 · lab 25 · check 5).

## Before you start

Two review questions from lesson 3.1.

1. When CM33 is halted at a breakpoint, what keeps running, and why does halting change the system's behaviour?
2. In this template's toolset, can we attach a debugger to CM55? If not, where must CM55's evidence come from instead?

## See it work first

Open [examples/06_pipeline_counters.c](examples/06_pipeline_counters.c). This program simulates a three-stage pipeline like the SDK's Edge AI one, and produces three kinds of fault that look identical from the screen. **Predict before you run it:** in the `no verdict` case, which counter's difference will be zero, and what will the `result` column say?

```sh
gcc -std=c11 -Wall -Wextra -o pipeline examples/06_pipeline_counters.c
./pipeline
```

Every case shows `result=OK`, because the most recent result from when things were still fine is still sitting there, and the cumulative totals are all large too. Only the **difference** in counters over the measurement window tells you which stage the pipeline stopped at. The SDK writes about this exact issue in the 01_first_inference example: "A SNAPSHOT OUTLIVES ITS SESSION," and in 07_engine_health: "A big number is not health; a big number that is not growing is a stall."

## Concepts

### 1. One symptom, many causes: form hypotheses before touching the code

"The screen shows 0% and nothing happens." The header of [07_engine_health.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/07_engine_health.c#L8-L49) says this symptom "has four different causes and they need four different fixes." A fix that actually works starts by writing down every hypothesis, then choosing **evidence that gives a different answer for each one**. Evidence every hypothesis predicts the same way separates nothing at all.

| Hypothesis | If true, the one-second difference will be | Fix where |
|---|---|---|
| No data reaches the model (the sensor or CM33 isn't sending) | `feeds` +0 | The data source side |
| The processing task isn't running, or is stuck inside | `feeds` moves, `dq_calls` +0 | The task and model selection |
| Processing runs but produces no result (the data window isn't full yet, or the NPU is stuck) | `dq_calls` moves, `dq_ok` +0 | Wait for it to fill, or check the NPU |
| The model never loaded successfully in the first place | Use a different set of counters (next section) | Model loading |

The order you read in matters: start from the beginning of the pipeline, because if no data is going in, no processing cycles happening isn't news. And check first that the measurement itself is valid — if the active model changed between two readings, the counters were cleared, and the difference means nothing. The SDK's example reports "the active model changed under the measurement" instead of interpreting the numbers in that case.

A real story from the SDK showing why picking the right evidence matters: the header of [bento_bgt60trxx_platform.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/libraries/tesaiot-radar/bento_bgt60trxx_platform.c#L11-L36) recounts the radar getting stuck repeatedly, while the sensor's own stall watchdog reported zero stalls — because it "sits at the BOTTOM of the same loop that was stuck." A measuring tool sitting underneath the point that's stuck will never see the stall. Usable evidence has to sit **outside** whatever it's measuring.

### 2. Reading the SDK's counters: totals, differences, and ordering

The SDK provides two sets of counters that answer different questions.

- **"Is it running right now?"** `ai_engine_feeds()`, `ai_engine_dq_calls()`, `ai_engine_dq_ok()` in 07_engine_health are read as a **difference** between two readings a second apart, using a saturating `delta32()` ("Saturating, because a counter is cleared on a model switch").
- **"Did it ever load successfully?"** `ai_engine_init_calls()`, `ai_engine_init_returns()`, `ai_engine_inits()`, `ai_engine_last_init_rc()` in [10_model_load_diagnosis.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/10_model_load_diagnosis.c#L16-L27) are read **once**, because loading either happened or didn't, and a sentinel value `0x7FFFFFFF` separates "init was never called" from a 0 that means "init succeeded".

Another piece of evidence that's always usable on the mtb-only variant is the `[HB]` line every ten seconds (the SDK documentation's chapter G2). If it's still coming, CM33 is still scheduling tasks — the problem lies in one particular task, the screen, or CM55, not a dead core. And if CM55 crashes with a serious fault, [proj_cm55/main.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/main.c#L250-L299) blinks an LED code — 1 blink for a stack overflow, 2 for a failed malloc, 3 for a HardFault — and writes a value of `0xDEAD0001` through `0xDEAD0003` to a fixed address in SRAM. Even a core with no console can leave evidence behind, if you design for it in advance.

### 3. Results that tell the truth

A function that has no data and returns 0 while claiming success lets whoever's downstream make a confident, wrong decision. The SDK's example catalogue makes it a rule that "Every file returns an honest result code" — `SDK_EX_OK`, `SDK_EX_UNAVAILABLE`, `SDK_EX_BUSY`, `SDK_EX_REFUSED`, `SDK_EX_NO_DATA`, `SDK_EX_STARTED` — and "If the hardware is absent the example says so rather than pretending to succeed" ([the catalogue's README, section 5](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/README.en.md)).

Examples of how an ambiguous result does real harm, recorded by the SDK's own documentation:

- **Appendix X #25**: MQTT's `0x08060009` code gets overwritten once retries run out, "overwriting whatever result already held." A TLS failure and being denied authorization end up printing the same code — the documentation notes that three separate bugs across three layers all printed this same code, and it never changed while each was fixed in turn.
- **The sensor task's mask counter** in [05_auto_push_task.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/sensors/05_auto_push_task.c#L27-L34): a missing bit could mean "you disabled it" or "it isn't working," and "the API cannot tell you which."
- **`radar_dsp_snapshot()`** returns `false` when there is no first frame yet, which is different from `target == 0`, meaning no target. The SDK deliberately keeps these two apart.

The other side of honesty is that **a reassuring-looking log is not evidence.** Chapter A1 warns that on mtb-only, a successful boot prints almost nothing, and some lines exist in the source but are never actually printed — "If a document tells you to wait for one of them, the document is stale." Good evidence is what the system **actually emits**, not what's written somewhere in the code.

## Worked example

[examples/06_pipeline_counters.c](examples/06_pipeline_counters.c) runs in three parts.

- **Part 1**: `pipeline_tick()` simulates one beat of a pipeline; each kind of fault stops it at a different stage.
- **Part 2**: `get_confidence()` returns `RESULT_NO_DATA` if there has never been a result — but once there has been one, it returns the latest result, which might be stale.
- **Part 3**: `run_case()` reads the counters twice and prints both the cumulative value and the difference.

Try changing things and predicting the result before you run it.

1. Shrink the initial normally-running period from 50 rounds to 0. What does the `result` column of the failing case change to, and why is this more honest?
2. Add the time of the most recent successful result into `get_confidence()`, and have it return `RESULT_NO_DATA` if that result is older than some limit. Decide for yourself what "too old" means.
3. Write a hypothesis table like the one in concept 1 for the symptom "the screen never updates the humidity value," with at least three hypotheses and the evidence that separates each one.

## Practice

Open [practice/06_diagnose.c](practice/06_diagnose.c). There are 5 gaps to fill in, following the same logic as the SDK's 07_engine_health and 10_model_load_diagnosis.

1. A saturating `delta32()`.
2. `diagnose()` checks first whether the measurement itself is valid (the model didn't change).
3. `diagnose()` decides based on the differences, checking the earlier stage before the later one.
4. `load_diagnosis()` covers five causes, in order.
5. `read_latest()` returns an honest result, and does not touch the caller's value when there's no data.

```sh
gcc -std=c11 -Wall -Wextra -o diagnose practice/06_diagnose.c && ./diagnose
```

Notice that some tests pass even before you fill anything in — for example `delta32(10u, 15u) == 0u`, and the `STAGE_HEALTHY` case, because the starting code returns 0, and 0 already matches HEALTHY. A test that passes against code that does nothing at all proves nothing. This is the heart of lesson 6.1.

## Solution

Try it yourself for at least 15 minutes first, then open [solution/06_diagnose.c](solution/06_diagnose.c). The comments in the solution say which part of the system each result points to, because a good diagnosis doesn't end at naming a cause — it ends at "go look here next." Notice `LOAD_NO_RC`, the case where the counters' own bookkeeping doesn't add up: the solution reports it as its own state, rather than letting it fall through to `LOAD_OK`.

## Check your understanding

Answer the 5 questions in [quiz.yaml](quiz.yaml) (shown at the bottom of this page on the website), covering all three objectives. Getting 4 or more right counts as finishing the lesson.

## Lab

**Task:** diagnose the Edge AI pipeline on the board from its counters, then audit the SDK's own diagnostic example with evidence.

1. Build the template with `make build -j ENABLE_PAGE_EXAMPLES=1`, flash it, unplug and replug the cable, and open the serial console.
2. Run `cm55/edge_ai/07_engine_health` from **SDK Examples** with no model started yet. Record the message you get (it should say no model is running, and return NO_DATA).
3. Start a model from the firmware's Edge AI page, then run `07_engine_health` again. Record every difference value and the `VERDICT` line.
4. **Predict first**, then run `cm55/edge_ai/10_model_load_diagnosis`. Record what you see on screen from this example. Then open [its file](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/10_model_load_diagnosis.c) and compare it against three things: the rule in section 5 of the catalogue's README (on the CM55 side, "Never printf ... use sdk_example_logf()"), Appendix X #1 (printf on CM55 is a no-op once `libbento_edge_ai.a` is linked), and the line declaring this function in [sdk_examples_table.c line 41](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/sdk_examples_table.c#L41) versus the definition in the example file — do the return type and parameters match? Write down what you find, with the lines as evidence, and say which conclusions you **saw on the board with your own eyes** and which ones you **inferred from reading the code**.
5. On the serial console, check that `[HB]` keeps arriving every ten seconds throughout the experiment. If it stops for a while, record the time and what you were doing at that moment.

**Evidence to keep in your portfolio:** screenshots of 07's output both times, your table of differences and diagnosis, a short report for question 4 that separates "actually observed" from "inferred," and the `[HB]` log.

## Going further

- Read Appendix X items #25 and #27 in the SDK documentation. Both are examples of symptoms that point to the wrong place — write a hypothesis table for each.
- Challenge: design a "black box" struct for your own project. See a design example in [diag_blackbox.h](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/shared/include/diag_blackbox.h) (at this commit, in the mtb-only template, there's only the header — no `.c` file uses it yet, which is itself another example of code existing not being evidence that it works).

Next lesson, moving into module 4: [lesson 4.1, GPIO and interrupts](../../m04-peripherals/l01-gpio-and-interrupts/README.md)

## Reflect

- The last time you fixed a bug that came back — did you fix it based on the one hypothesis you happened to think of, or did you separate hypotheses with evidence first?
- Which function in your own code returns 0 or `true` when there's no data, and how could a caller be misled by that?

## References

- [SDK: cm55/edge_ai/10_model_load_diagnosis.c (four causes of a no-result symptom)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/10_model_load_diagnosis.c)
- [SDK: cm55/edge_ai/07_engine_health.c (reading counter differences)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/edge_ai/07_engine_health.c)
- [SDK: the example catalogue (Rules every example follows, result codes)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/README.en.md)
- [B1 — CM33_NS boot walk-through (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__b1__cm33__boot.html)
- [Appendix X — Traps and anti-patterns (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__tut__x__traps__antipatterns.html)
