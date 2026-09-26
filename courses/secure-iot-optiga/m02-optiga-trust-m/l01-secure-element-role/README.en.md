---
id: sec-iot.m02.l01
lang: en
title: {th: ชิปความปลอดภัยทำอะไรให้เรา, en: What a secure element does for us}
summary: {th: รู้ว่า OPTIGA™ Trust M เก็บและทำอะไร และอ่านสถานะของ HSM จาก SDK โดยไม่เริ่มธุรกรรม, en: 'Learn what OPTIGA™ Trust M stores and does, and read HSM state from the SDK without starting a transaction.'}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m01.l02]
objectives:
- {th: ระบุหน้าที่ของชิปความปลอดภัยได้อย่างน้อยสามข้อ เช่น เก็บกุญแจ ลงลายเซ็น และสุ่มเลข, en: 'Name at least three secure-element functions, such as key storage, signing and random numbers.'}
- {th: อ่านสถานะของ HSM ด้วยคำสั่งที่ไม่ต้องทำธุรกรรมกับชิป ตามตัวอย่างอ้างอิงของ SDK, en: 'Read HSM state with calls that need no chip transaction, following the SDK reference example.'}
- {th: อธิบายว่าคำสั่งใดของชิปย้อนกลับไม่ได้ และทำไมบทเรียนจะไม่แตะคำสั่งเหล่านั้น, en: Explain which chip operations are irreversible and why the lessons will not touch them.}
develops:
- {skill: sec.secure-element, to: 3}
- {skill: sec.crypto, to: 2}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
source:
- {repo: 'https://github.com/tesaiot/tesaiot-pse84-devkit-sdk', path: bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/ref_hsm.c, ref: ef72c1b658178eee8c38b1e47d28b006f80a59b5, license: Apache-2.0}
- {repo: 'https://github.com/Infineon/optiga-trust-m-overview', path: data/object_dumps/trust_m3_json.txt, ref: a45b86bda014efeebfb85f084f779cedb07b32dc, license: MIT}
source_sha256: 60921ea78ab05d39a2d80f2d0127985481c58a3c5de33abad6395b13fc8ce3ca
---

# Lesson 2.1: What a secure element does for us

> Module 2 · The OPTIGA™ Trust M secure element · [Module overview](../README.md) · [Course home](../../README.md)

The TESAIoT Dev Kit board has one OPTIGA™ Trust M chip, on the same I2C bus as the touch controller, commanded from the CM33_NS core.
This lesson opens it up: what is inside, what it can do, which reads are "free," and which commands, once run, can never be undone.

## Objectives

By the end of this lesson you will:

1. Name at least three secure-element functions, such as key storage, signing and random numbers
2. Read HSM state with calls that need no chip transaction, following the SDK's reference example
3. Explain which chip operations are irreversible, and why the lessons will not touch them

## Before you start

- **Already covered:** [Lesson 1.2: Crypto basics for embedded systems](../../m01-threats-and-crypto/l02-crypto-basics/README.md)
- **Board:** a TESAIoT Dev Kit with a USB cable plugged into the KitProg port, and a serial terminal program to read CM33_NS's console
- **Software:** the TESAIoT PSE84 Dev Kit SDK at commit `ef72c1b`, and ModusToolbox 3.6 (the SDK's README says this exact version is required)

```bash
git clone https://github.com/tesaiot/tesaiot-pse84-devkit-sdk.git
cd tesaiot-pse84-devkit-sdk
git checkout ef72c1b658178eee8c38b1e47d28b006f80a59b5
cd bento-firmware-template-mtb-only
./setup.sh --build
```

`setup.sh` prints every command it runs before running it. The first build takes about ten minutes.
After every flash, **unplug the USB cable all the way, count to ten, then plug it back in.** The SDK's README explains that the display needs a cold power edge; resetting through the debugger alone leaves the screen black.

## See it work first

Here is the header of the [ref_hsm.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/ref_hsm.c) example we will run today.
The SDK's author opens the file with the sentence "THIS IS A REFERENCE LIST, NOT A JOB," followed by:

> It enrols nothing, publishes nothing, and writes nothing — to the chip or anywhere else.

There is also a SAFETY paragraph stating that this file neither reads nor writes metadata tag `C0`, the chip's lifecycle state, which "moves one way only and which no reflash undoes."

**Guess first:** why is the very first example the SDK has us run against the secure element one that deliberately **does nothing to the chip at all**?
Write down a one-sentence answer, and come back to compare it at the end of Concepts section 3.

## Concepts

### 1. What this chip can do

Infineon describes the OPTIGA™ Trust M as a security controller on hardware certified to Common Criteria EAL6+ (high)
([optiga-trust-m-overview](https://github.com/Infineon/optiga-trust-m-overview)). We use six groups of functions on this board, each with real functions in Infineon's host library (`optiga_crypt.h` and `optiga_util.h`).

| Function | Host library call | What the board's SDK uses it for |
|---|---|---|
| Generate and store a private key | `optiga_crypt_ecc_generate_keypair` | Creates a new key pair during CSR enrolment (lesson 5.1) |
| Sign and verify a signature | `optiga_crypt_ecdsa_sign`, `optiga_crypt_ecdsa_verify` | Signs CertificateVerify in mTLS (lesson 3.1), and checks that a certificate matches a key |
| Generate random numbers with the TRNG | `optiga_crypt_random` | A helper in `tesaiot_crypto.c` calls it with `OPTIGA_RNG_TYPE_TRNG` (chapter D1 notes this file is shipped as a reference but not compiled into the template) |
| Key agreement and key derivation | `optiga_crypt_ecdh`, `optiga_crypt_hkdf`, `optiga_crypt_hmac` | Available, but not yet on the template's main path |
| Read/write data and metadata | `optiga_util_read_data`, `optiga_util_read_metadata`, `optiga_util_write_metadata` | Reads a certificate out for use in TLS |
| Protected update | `optiga_util_protected_update_start` / `_continue` / `_final` | Accepts a new certificate signed by the platform (lesson 4.2) |

The SDK does not have us call all of these functions directly. The parts dealing with owning the chip, enrolment and Protected Update are wrapped inside `libbento_hsm.a`,
which, per the [tesaiot_hsm docs](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/docs/sdk/tesaiot_hsm/README.md), exports 18 functions.

### 2. Objects, metadata and the lifecycle state

The inside of the chip is divided into slots (objects), each with a two-byte address called an OID. This table combines Infineon's example dump
([trust_m3_json.txt](https://github.com/Infineon/optiga-trust-m-overview/blob/a45b86bda014efeebfb85f084f779cedb07b32dc/data/object_dumps/trust_m3_json.txt), MIT)
with the usage the SDK records in `tesaiot_config.h` and in [chapter C4](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c4__mtls__optiga.html).

| OID | Factory value (Infineon's example dump) | What TESAIoT uses it for |
|---|---|---|
| `0xE0C2` | The chip's 27-byte UID, always readable, cannot be changed | The source of the `factory_uid` value used as the MQTT client id in mTLS mode |
| `0xE0E0` | Certificate from Infineon, Change = never | The factory identity |
| `0xE0F0` | An ECC P-256 key, paired with `0xE0E0`, Change = never, Execute = always | Signs TLS before enrolment |
| `0xE0E1` | A certificate slot, Change = LcsO < op | TESAIoT's device certificate |
| `0xE0F1` | A key slot, Change = LcsO < op | The key paired with `0xE0E1`, created during enrolment |
| `0xE0E8` | A trust-anchor slot, Change = LcsO < op | The anchor used to verify a Protected Update manifest |

Each slot's **metadata** is a TLV starting with tag `20`. There are only a handful of tags you need to be able to read in this course (see the dump, and Infineon's [example_optiga_util_protected_update.c](https://github.com/Infineon/optiga-trust-m/blob/release-v5.3.0/examples/optiga/example_optiga_util_protected_update.c)).

| Tag | Meaning | Common values |
|---|---|---|
| `C0` | LcsO, the object's lifecycle state | `01` creation, `03` initialization, `07` operational, `0F` termination |
| `C1` | The object's version, used to prevent rollback in Protected Update | Only ever goes up |
| `D0` | Change access condition — who can write | `FF` never, `E1 FC 07` = LcsO < op, `21 E0 E8` = requires a manifest verified with `0xE0E8` |
| `D1` / `D3` | Read / Execute access condition | `00` always |
| `E8` | The object's type | `11` trust anchor, `12` device certificate |

Look closely at `E1 FC 07`: it means "writable as long as LcsO is still below operational." Most of the slots we use are writable precisely because the chip is still at creation (`01`).
Chapter D2 of the SDK docs says every board on the lab bench should read `C0` as `01`.

### 3. What cannot be undone, and free state reads

The **irreversible** operations, as [06_protected_update.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/06_protected_update.c) states plainly, are:

1. **LcsO (tag `C0`)** travels one way only: `cr (0x01) -> in (0x03) -> op (0x07) -> te (0x0F)`. No reflash, no erase, no power cut brings it back.
   What moves it is writing metadata that contains tag `C0`. Once it reaches `op`, writing metadata can stop being possible forever, and
   any slot whose Change condition is `LcsO < op` can no longer be written normally either.
2. **The version counter (tag `C1`)** of an object that has been through a Protected Update only ever goes up; the next manifest must carry a larger number than the last.
3. **Change = never** on `0xE0E0` and `0xE0F0`: the factory identity can never be changed at all. This is not something we do, but you must know there is no way around it.

The **Protected Update lock** (tag `D0` = `21 E0 E8`), on the other hand, can be reversed **as long as LcsO is still below `op`.** Example 06 stresses that you must always say which kind of board you mean:
"permanent lock" is true for a device that has shipped, and not true for a development board.

No example in the SDK writes tag `C0`, and example 06 states that none of the 18 functions in `libbento_hsm.a` writes it either.
This course **never has you write `C0` or advance LcsO, under any circumstance**, because the result is a board that can no longer be used for learning, with no way to recover it.
Example 06 sets the principle that advancing the lifecycle should live in a separate, clearly named tool, run only by someone who has already decided to ship that board.

**Free state reads:** `ref_hsm.c` splits the questions into two kinds.

- Three functions read a plain variable, touching the chip not at all — call them from any task, as often as you like, even while enrolment is in flight:
  `trustm_requested_target_oid()`, `trustm_requested_anchor_oid()` and `trustm_current_correlation_id()`.
- `optiga_manager_lock()` is **not free.** It acquires the chip's access gate. If it returns `true`, you must return it with `optiga_manager_unlock()` every time,
  and if it returns `false`, that may just mean you have waited out the full ten-second timeout — so never call it from a UI tick.

## Worked example

Taken from [ref_hsm.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/ref_hsm.c), lines 65–89
(TESAIoT PSE84 Dev Kit SDK, © Thai Embedded Systems Association, Apache-2.0)

```c
    /* NULL when nothing is in flight; otherwise the id the platform's reply is
     * matched against. This is the "is an enrolment outstanding?" test, and it
     * is the value trustm_reset_state() destroys — so check it before you
     * reset anything. Print it guarded: %s given NULL faults on this
     * platform's newlib. */
    const char *cid = trustm_current_correlation_id();
    printf("  trustm_current_correlation_id()= %s\r\n",
           (cid != NULL) ? cid : "(none — nothing in flight)");

    /* ── Chip readiness — a balanced probe, not a free read ──────────────── */

    if (optiga_manager_lock()) {
        /* True means both "the manager is up" and "the gate is now ours". The
         * unlock is not optional and there is no path out of here without it. */
        printf("  optiga_manager_lock()          = true  (manager up, chip free)\r\n");
        optiga_manager_unlock();
        printf("  optiga_manager_unlock()        — gate returned\r\n");
    } else {
        /* Either optiga_manager_init() has never run, or another task has held
         * the chip for the full 10-second timeout. Those are different problems
         * and the return value does not separate them; if you need to know,
         * track whether your own code has called init(). */
        printf("  optiga_manager_lock()          = false (manager not "
               "initialised, or another task holds the chip)\r\n");
    }
```

Three things worth noticing in this code:

1. **Printing NULL needs a guard.** `printf("%s", NULL)` faults newlib on this platform, per the comment, so the example substitutes a message.
2. **Acquire it, and you must return it.** In the `true` branch, there is no path out of the function that skips `optiga_manager_unlock()`.
3. **A `false` value does not say why.** It can mean either "no one has initialised the manager yet" or "another task has held the chip for the full ten seconds." If you need to tell these two cases apart, your own code has to remember whether it has already called `optiga_manager_init()`.

## Practice

Sort each action into **free** (does not touch the chip), **holds the gate** (must be returned), **a chip transaction** (the chip does real work), or **irreversible**.

1. `trustm_requested_anchor_oid()` ____
2. `optiga_manager_lock()` ____
3. `optiga_crypt_ecdsa_sign(me, digest, 32, OPTIGA_KEY_ID_E0F0, sig, &len)` ____
4. Writing metadata containing tag `C0` with value `07` to a slot ____
5. A Protected Update that applies successfully — the part that is that slot's version counter ____
6. `trustm_current_correlation_id()` ____

<details><summary>Solution</summary>

1. **Free.** Reads a variable; the default value after reset is `0xE0E8`.
2. **Holds the gate.** Getting `true` means you must call `optiga_manager_unlock()`.
3. **A chip transaction**, and it must happen while you hold the gate (lesson 2.2).
4. **Irreversible.** That slot's LcsO advances to operational; never do this in this course.
5. **Irreversible.** The counter only goes up; the slot's lock, however, can still be reversed if LcsO is below `op`.
6. **Free.** NULL means no request is outstanding.

</details>

## Check your understanding

The questions below are part of the full set in [quiz.yaml](quiz.yaml), which the automated grader uses.

1. Which of these is **not** a function the OPTIGA™ Trust M provides to the board's SDK? *(objective 1)*
   - a) Generating random numbers with the TRNG
   - b) Making an ECDSA signature with a key inside the chip
   - c) Encrypting the image on the LCD screen
   - d) Storing a private key generated inside the chip

   <details><summary>Solution</summary>

   **c.** Drawing to the screen is CM55's job; the secure element has nothing to do with it.

   </details>

2. Which function does `ref_hsm.c` say is **not** a free read? *(objective 2)*
   - a) `trustm_requested_target_oid()`
   - b) `trustm_current_correlation_id()`
   - c) `optiga_manager_lock()`
   - d) `trustm_requested_anchor_oid()`

   <details><summary>Solution</summary>

   **c.** It holds the chip's access gate — `true` must be returned, and a `false` result may just mean you have already waited ten seconds.

   </details>

3. A development board has tag `C0` of slot `0xE0E1` reading `01`, and `D0` reading `21 E0 E8`. Which statement is correct? *(objective 3)*
   - a) This slot is permanently locked; there is no way to write it normally ever again
   - b) This slot accepts only a manifest verified with `0xE0E8`, but the lock can still be cleared because LcsO is still below op
   - c) The chip is broken
   - d) This slot can be written normally, as usual

   <details><summary>Solution</summary>

   **b.** The Protected Update lock is a condition in metadata, not a fuse. As long as LcsO is still at creation, writing metadata is still possible.

   </details>

4. Why does this course never have you write tag `C0`? *(objective 3)*
   - a) Because the chip does not support it
   - b) Because LcsO travels one way only, no reflash can bring it back, and once it reaches op, writing metadata can stop permanently
   - c) Because it requires a password from Infineon
   - d) Because it would break WiFi

   <details><summary>Solution</summary>

   **b.** The result is a board that can no longer be used for learning, with no way to recover it. The SDK's example 06 sets the principle that this job should live in a separate, clearly named tool.

   </details>

## Lab

**Read HSM state without starting anything at all.** Write down every line you get in your learning log.

- [ ] Build the template with the examples enabled, and select `ref_hsm` to run on CM33_NS (the example's id is in the `sdk_examples_cm33_table.c` table).
  ```bash
  make build ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/security/ref_hsm
  make program BENTO_WORKSPACE="$(cd .. && pwd)"
  ```
  Then unplug the USB cable, count to ten, plug it back in, and open a serial terminal on the KitProg port.
- [ ] **Guess before you look at the result:** what values will `trustm_requested_target_oid()` and `trustm_requested_anchor_oid()` return (read the comments in the file), and will `optiga_manager_lock()` return `true` or `false`?
- [ ] The example runner waits three seconds after boot, prints the full list of examples, then runs the one you selected. The source says the output looks like this:
  ```text
  --- tesaiot_hsm/ref_tesaiot_hsm (reference list) ---
    trustm_requested_target_oid()  = 0x....
    trustm_requested_anchor_oid()  = 0x....
    trustm_current_correlation_id()= ...
    optiga_manager_lock()          = ...
  ```
  Compare it against your guess. If `optiga_manager_lock()` returns `false`, explain which of the two cases it is, and how you know.
- [ ] Rebuild with `SDK_EXAMPLE_CM33=cm33/security/03_chip_ownership`. This example calls `optiga_manager_init()` first, then holds the gate. See how the `optiga_manager_lock()` line changes, and explain it using reason 3 from the worked example.
- [ ] Write a two-column table, "what this example can tell us" and "what it cannot tell us," with at least two items on each side.

**Forbidden in this lab:** do not enable `EXAMPLE_HSM_REQUEST_PU` and `EXAMPLE_HSM_ISOLATED_TEST` in example 06, and do not write any metadata at all.

If you want to see a different reference project, look at [PSoC Edge E84 + OPTIGA Trust M: TESAIoT MQTT Client](https://dev.tesaiot.dev/?example=developer-hub--pse84_tesaiot_client&q=pse84_tesaiot_client) on the Developer Hub.
It is menu-driven firmware with a menu to read the UID and the factory certificate, and a menu to read metadata. This project ships with the PSOC™ Edge E84 Evaluation Kit's BSP (`APP_KIT_PSE84_EVAL_EPC2`)
and is under the Cypress (Infineon) EULA, so this course references it by link only and does not copy its code.

## Going further

We have already seen that just asking "is the chip free?" means acquiring the gate and returning it. The next lesson goes deeper on that gate: why it has three names, why touch must be kept off the bus,
and what kind of work must never happen inside the task that draws the screen.

Next lesson: [Lesson 2.2: Rules for accessing the chip](../l02-chip-access-discipline/README.md)

## Reflect

- In your own project, which commands are irreversible once run, and are any of them hidden inside an example that anyone could just click to run?
- If you had to write an HSM status screen, which values from this example would you use, and which calls would you avoid making from the screen-draw loop?
- Has a `false` value with two possible meanings ever led you to fix the wrong thing in another piece of work?

## References

- [Infineon optiga-trust-m (host library, MIT) @ release-v5.8.3](https://github.com/Infineon/optiga-trust-m/tree/release-v5.8.3), and the version the SDK uses [@ release-v5.3.0](https://github.com/Infineon/optiga-trust-m/tree/release-v5.3.0)
- [Infineon optiga-trust-m-overview (MIT)](https://github.com/Infineon/optiga-trust-m-overview/tree/a45b86bda014efeebfb85f084f779cedb07b32dc)
- [SDK: tesaiot_hsm docs](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/docs/sdk/tesaiot_hsm/README.md)
- [SDK: cm33/security/ref_hsm.c (reading state without starting a transaction)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/ref_hsm.c)
- [SDK: cm33/security/06_protected_update.c (what cannot be undone)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/06_protected_update.c)
- [SDK: CM33-side examples (what you need to know about LcsO state)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/README.md)
- [SDK: tesaiot_config.h (TESAIoT's OID map)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/tesaiot/include/tesaiot_config.h)
- [D2 — Enrolment and Protected Update end to end (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d2__enrolment__protected__update.html)
- Example on the Developer Hub: [PSoC Edge E84 + OPTIGA Trust M: TESAIoT MQTT Client](https://dev.tesaiot.dev/?example=developer-hub--pse84_tesaiot_client&q=pse84_tesaiot_client) (Cypress EULA, link only)
