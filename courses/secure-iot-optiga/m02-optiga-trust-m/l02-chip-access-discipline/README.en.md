---
id: sec-iot.m02.l02
lang: en
title: {th: กติกาการเข้าถึงชิป, en: The chip-access discipline}
summary: {th: ใช้ประตูเข้าชิป lock และการกันหน้าจอสัมผัสออกจากบัสขณะชิปทำงาน ตามลำดับที่ SDK กำหนด, en: 'Use the chip gate, lock and touch-hold in the order the SDK requires.'}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m02.l01]
objectives:
- {th: 'เรียงลำดับ init, acquire, ใช้งาน และ release ของชิปได้ถูกต้อง และอธิบายผลเมื่อลืม release', en: 'Order init, acquire, use and release correctly, and explain what happens if release is forgotten.'}
- {th: อธิบายว่าทำไมการกันหน้าจอสัมผัสออกจากบัสต้องครอบทั้งธุรกรรม ไม่ใช่แค่ช่วงเตรียมการ, en: 'Explain why touch-hold must wrap the whole transaction, not just its setup.'}
- {th: ระบุงานที่ต้องย้ายออกจากงานวาดจอ เพราะธุรกรรมกับชิปใช้เวลาหลายวินาที, en: Identify work that must leave the display task because chip transactions take seconds.}
develops:
- {skill: sec.secure-element, to: 3}
- {skill: rtos.basics, to: 2}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
source:
- {repo: 'https://github.com/tesaiot/tesaiot-pse84-devkit-sdk', path: bento-firmware-template-mtb-only/proj_cm33_ns/examples/security, ref: ef72c1b658178eee8c38b1e47d28b006f80a59b5, license: Apache-2.0}
source_sha256: b05cd27af97d08cefdf4a3fea83335f6b9b5bc6c649bd2b93da7b3c05e9eb8d1
---

# Lesson 2.2: The chip-access discipline

> Module 2 · The OPTIGA™ Trust M secure element · [Module overview](../README.md) · [Course home](../../README.md)

There is one secure element on the board, on a single I2C bus, but at least four parts of the firmware want to use it.
The [03_chip_ownership.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/03_chip_ownership.c) example counts them for you:
the mTLS/MQTT path, the HSM's enrolment screen, MicroPython's `optiga` module, and the code you are about to write.
This lesson is the discipline that lets every one of them share the chip without colliding.

## Objectives

By the end of this lesson you will:

1. Order the chip's init, acquire, use and release correctly, and explain what happens if release is forgotten
2. Explain why touch-hold must wrap the whole transaction, not just its setup
3. Identify work that must leave the display task, because chip transactions take several seconds

## Before you start

- **Already covered:** [Lesson 2.1: What a secure element does for us](../l01-secure-element-role/README.md). You should already be able to build the SDK's template and run the `ref_hsm` example.
- **Review:** FreeRTOS tasks, priority, mutexes and `vTaskDelay()`. If you are not sure, review these from the C fundamentals course first.
- **Board:** a TESAIoT Dev Kit with USB plugged in and a serial terminal open, and a free hand for tapping the screen during the lab.

## See it work first

The comment at the top of [04_touch_hold.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/04_touch_hold.c) tells a real bug story:
on the TESAIoT Dev Kit, the secure element and the touch controller share the same I2C bus, and are commanded from different cores.
When CM55 reads the touchscreen while CM33 is talking to the chip, some transactions never finish, and the vendor's library has no timeout on that path, so the signature does not fail — it **hangs.**
The same build connects successfully on one boot cycle, then hangs forever on the next.

The mTLS path at the time stopped the touchscreen during "setup," then released it once setup was done.

**Guess first:** if the point where the touchscreen was stopped looks correct, why did the bug still happen? Think about **when** the TLS signature actually occurs. Write down your guess, and find the answer in Concepts section 2.

## Concepts

### 1. One gate, three names

Per [03_chip_ownership.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/03_chip_ownership.c)
and [chapter D1 of the SDK docs](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d1__chip__access__discipline.html), these three function pairs all hold and release **the same gate**.

| Pair | Answers the question | How it differs from the others |
|---|---|---|
| `optiga_chip_enter()` / `optiga_chip_exit()` | Is another task holding the chip? | Returns `false` for exactly one reason: someone else is holding it |
| `optiga_manager_lock()` / `optiga_manager_unlock()` | Is the manager ready, and can I use it? | Returns `false` if it has not been initialised yet |
| `optiga_manager_acquire()` / `optiga_manager_release()` | Gives you the `optiga_util_t *` used to command the chip, while holding the gate | Returns `NULL` if not initialised, or if the wait times out |

**The one non-negotiable order** is that `optiga_manager_init()` must come before everything else. It creates the mutex and the shared `optiga_util_t`; it can be called more than once, and must only be called from a task (chapter D1 warns it cannot be called before the scheduler starts).
Before init, `acquire()` returns `NULL` and `lock()` returns `false`, but `optiga_chip_enter()` **returns `true`** even though it has locked nothing at all — the author intended it that way,
so that `false` from `enter()` can mean only one thing: "someone else is holding the chip." That is why you **must never use `enter()` to ask whether the chip is ready** — that question belongs to `lock()`.

This gate **can be nested within the same task**, because helper functions in the firmware call each other — for example, generating a key calls a metadata read internally. An ordinary mutex would deadlock on the very first nested call.
But every acquisition still needs exactly one release; a depth counter ensures only the outermost release actually opens the gate.

**Another** task asking for it will wait at most ten seconds and then get `false`. So if you forget `release()` after `acquire()` on even one exit path,
the chip stays blocked for the rest of that boot. As example 03 puts it, every other part of the firmware that needs the chip — signing TLS, for instance — will wait ten seconds and then fail, every single time.
Conversely, if `acquire()` returns `NULL`, you must **not** call `release()`, because it has already returned the gate itself; releasing on top of that corrupts the depth counter of whichever task really holds it.

Last point: every `optiga_util_*` and `optiga_crypt_*` function is **asynchronous** — it returns immediately, and the real result arrives through a callback.
You must **hold the gate for the entire wait.** Releasing it while the command is still in flight hands the bus to another task in the middle of a transaction.

### 2. touch-hold must wrap every byte, not just the function that looks like the crypto work

The answer to the guess is in 04_touch_hold.c. The signature that matters is **CertificateVerify**, and it happens later, inside `cy_mqtt_connect()`, while the TLS handshake is running.
By then the touchscreen has already gone back to reading the bus. So the hold must wrap **the very last byte that talks to the chip**, wherever it happens to be.
This is why the current firmware has `trustm_ecdsa_sign()` hold both the gate and the touch-hold itself, for the whole signing operation (chapters C4 and D1).

The symptom you need to memorise is `OPTIGA_COMMS_ERROR (0x0102)`. Chapter D1 explains that it means a chip transaction was running while CM55 read the touchscreen on the same bus,
and it is usually followed by `OPTIGA_UTIL_ERROR_INSTANCE_IN_USE (0x0305)` on the next call. Chapter D1 also records a real incident where an 8-byte metadata write succeeded,
but the 580-byte certificate write that followed failed with `0x0102` after 57 seconds of retries — because the code was carried over from a reference project that has no touchscreen at all, and so no touch-hold whatsoever.
The SDK's fix is to hold the hold across the whole function, not command by command, because releasing it between steps just reopens the same window.

The hold rules, from example 04:

- **It counts.** Holds can nest; only the first one stops the touchscreen, and only the last one releases it. You must return exactly as many as you held, on every exit path, including the error ones.
- **The first hold delays about 50 ms**, deliberately, so any touch read already in flight finishes before the chip starts talking. A nested hold costs no extra time.
- **Use it only in a task.** It sleeps, so it is not safe from an ISR.
- **While held, the screen accepts no touches at all.** Use `optiga_manager_touch_hold_reason("...")`; this message is shown on screen, and the screen shows only the first hold's message.
- **A hold nobody returns leaves the screen permanently deaf** to whoever is holding the board. A screen that will not respond to touch looks no different from a hung device, and there is no "force release" command. Releasing extra does not fix it either — the counter simply floors at zero, but the pairing bug is still there, waiting to show up next cycle.
- **Never send the `IPC_CMD_TOUCH_RESUME` command directly.** Chapter D1 explains that CM55 treats this command as an unconditional, non-counted re-enable, and it will cancel a hold that some other task is still relying on.

**Nesting order:** the SDK uses both hold-wraps-lock (example 04) and lock-wraps-hold (`trustm_ecdsa_sign()` in chapter D1).
Two things must always hold true: the hold must wrap every byte that talks to the chip, and the pair must nest correctly — **whatever was acquired last must be released first.**
Chapter D1 flags this as pitfall 4: if you entered with lock then hold, on the way out you must release hold first, then unlock.

### 3. Work that takes several seconds must leave the task that draws the screen

Some chip transactions take whole seconds. Generating a key pair and signing a CSR, and receiving a Protected Update, are long conversations with the chip.
Asking for the gate can itself wait up to ten seconds. If any of this happens inside the LVGL task, the entire screen freezes.

[01_hsm_screens.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/security/01_hsm_screens.c) points out something worse than just a frozen screen.
If you wait for the result inline, the screen freezes, and **at the same time** `ui_busy_modal_service()` — the very thing meant to draw a window explaining why it is frozen — cannot draw either. So the screen goes both dead and silent.
The SDK's fix is that the `IPC_CMD_HSM_PROVISION` command returns immediately; the real work runs in a worker task on the CM33_NS side (chapter D2 says `prov_task` checks for work every 50 ms), and the screen polls status periodically with an `lv_timer`.

Work that **must never** live in a button's callback or in the display task:

- `optiga_manager_lock()` and `optiga_manager_acquire()` (can wait up to ten seconds)
- Any command that talks to the chip, and waiting for its callback
- Waiting for a network reply, such as waiting for the platform to send back a certificate (chapter D2 says this can wait up to 60 seconds)
- The same applies to a handler called from MQTT's event thread — chapter C3 says work that touches the chip must be queued off to your own task

And the flip side: chapter D1 warns **never hold touch-hold across a network wait.** During that 60-second wait, not a single byte talks to the chip — holding the touch-hold there just freezes the screen for minutes, for no reason at all.

## Worked example

The first part is taken from [03_chip_ownership.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/03_chip_ownership.c), lines 136–145,
and the second from [04_touch_hold.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/04_touch_hold.c), lines 94–104
(TESAIoT PSE84 Dev Kit SDK, © Thai Embedded Systems Association, Apache-2.0)

```c
    optiga_util_t *util = optiga_manager_acquire();
    if (util == NULL) {
        /* Either the gate timed out or the instance is missing. acquire()
         * releases the gate itself before returning NULL, so there is nothing
         * to give back here — do not call release() on a NULL. */
        printf("  optiga_manager_acquire() = NULL — busy, or the manager is "
               "not up\r\n");
        return SDK_EX_BUSY;
    }
    printf("  optiga_manager_acquire() = %p (gate held)\r\n", (void *)util);
```

```c
    /* The chip work belongs here, between the outermost hold and its release.
     * Note the ordering against example 01: take the chip gate and hold touch
     * for the same span. Two rules, one lifetime.
     *
     *     optiga_manager_touch_hold_reason("Signing");
     *     if (optiga_manager_lock()) {
     *         ... chip operations, including the wait for the callback ...
     *         optiga_manager_unlock();
     *     }
     *     optiga_manager_touch_release();
     */
```

Read these two together: two rules, the same lifetime. Both the gate and the hold must wrap the same span of time — from before the first byte to after the last byte of the transaction, **including the wait for the callback.**
(The comment's "example 01" refers to the chip-ownership example, which in the current template is file 03.)

## Practice

The function below reads data from one of the chip's slots under both rules. It is code written fresh for this lesson using the SDK's API.
Assume `optiga_manager_init()` has already been called, and the callback registered at init is what writes `s_status`. Fill in blanks (1) through (5).

```c
static volatile optiga_lib_status_t s_status;   /* written by the callback registered at init */

bool read_object_held(uint16_t oid, uint8_t *buf, uint16_t *len)
{
    bool ok = false;

    ____(1)____("Reading the secure element");       /* keep touch off the bus */

    optiga_util_t *util = ____(2)____();             /* hold the gate and get util */
    if (util == NULL) {
        ____(3)____();                               /* what must this exit path return? */
        return false;
    }

    s_status = OPTIGA_LIB_BUSY;
    if (optiga_util_read_data(util, oid, 0, buf, len) == OPTIGA_LIB_SUCCESS) {
        for (int i = 0; i < 200 && s_status == OPTIGA_LIB_BUSY; i++) {
            vTaskDelay(pdMS_TO_TICKS(10));           /* wait for the callback, up to ~2 s, still holding the gate */
        }
        ok = (s_status == OPTIGA_LIB_SUCCESS);
    }

    ____(4)____();                                   /* return the gate */
    ____(5)____();                                   /* release touch */
    return ok;
}
```

<details><summary>Solution</summary>

1. `optiga_manager_touch_hold_reason` — this message appears on screen while the screen refuses touches
2. `optiga_manager_acquire`
3. `optiga_manager_touch_release` — **not** `optiga_manager_release`, because an `acquire()` that returns `NULL` has already released the gate itself, but the hold we already took still needs returning
4. `optiga_manager_release`, only after the wait for the callback is done
5. `optiga_manager_touch_release` — the hold was taken first, so it is released last

Notice that the wait loop has a ceiling. Chapter C4 and a comment in `mqtt_mtls_setup.c` tell the story of a `while (status == BUSY);` loop with no timeout that once froze all of CM33_NS.

</details>

## Check your understanding

The questions below are part of the full set in [quiz.yaml](quiz.yaml), which the automated grader uses.

1. Why can `optiga_chip_enter()` not be used to ask "is the chip ready yet?" *(objective 1)*
   - a) Because it is slow
   - b) Because before init it returns `true` even though it has locked nothing; it returns `false` only when someone else is holding the chip
   - c) Because it can only be used from an ISR
   - d) Because it writes metadata

   <details><summary>Solution</summary>

   **b.** Asking whether the manager is ready is `optiga_manager_lock()`'s job.

   </details>

2. Some code calls `optiga_manager_acquire()`, gets a non-NULL value, then `return`s partway through when a read fails, without calling `release()`. What is the result? *(objective 1)*
   - a) No effect — the gate releases itself when the function ends
   - b) The chip stays blocked for the rest of that boot; any other task that asks, including a TLS signature, waits ten seconds and then fails
   - c) The chip resets itself
   - d) LcsO changes to operational

   <details><summary>Solution</summary>

   **b.** Example 03 calls this leaking the chip until the end of the boot. The fix is to write the function with a single exit path.

   </details>

3. The old mTLS path stopped the touchscreen only during setup. Why did it still hang? *(objective 2)*
   - a) Because setup took too long
   - b) Because the CertificateVerify signature happens later, inside `cy_mqtt_connect()`, by which point the touchscreen was already reading the bus again
   - c) Because the chip does not support TLS
   - d) Because it used the wrong port

   <details><summary>Solution</summary>

   **b.** The hold must wrap the very last byte that talks to the chip, not just the function that looks like the crypto work.

   </details>

4. In an "Enrol" button on an LVGL screen, what should be inside the button's callback? *(objective 3)*
   - a) `optiga_manager_lock()`, then generate the key pair
   - b) Wait for the certificate from the platform until it arrives
   - c) Close the old window, open a new one, hand the request to a worker task, and let an `lv_timer` poll its status
   - d) Hold touch-hold until enrolment finishes

   <details><summary>Solution</summary>

   **c.** The long work belongs in a worker; the screen only polls status. This is the shape of `hsm_enrol_open()`, which lesson 5.2 goes deeper into.

   </details>

## Lab

**Watch the discipline work in practice, then design one button correctly.**

- [ ] Build with `SDK_EXAMPLE_CM33=cm33/security/03_chip_ownership` and flash.
  ```bash
  make build ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/security/03_chip_ownership
  make program BENTO_WORKSPACE="$(cd .. && pwd)"
  ```
  Write down every line that appears after `--- tesaiot_hsm/01_chip_ownership ---` (the header line still carries the file's old number), and note the gate's depth counter alongside each line.
- [ ] Rebuild with `SDK_EXAMPLE_CM33=cm33/security/04_touch_hold`. The runner starts about three seconds after boot; during that window, tap the screen rapidly and note whether you see `Reading device certificate` on screen, and whether tapping during that window has any effect.
  Record the console lines that show the counter, `count 2 -> 1` and `count 1 -> 0`.
- [ ] Read the five `*_held()` functions in [chapter D1](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d1__chip__access__discipline.html), write down every reason message that appears on screen, and explain why none of them hold the hold across a wait for the platform.
- [ ] **Design** a "Read certificate" button on an LVGL screen. Draw a four-part sequence diagram: the button's callback (display task), a queue or IPC, a worker task that holds the gate and the hold, and an `lv_timer` that polls status.
  Label which core and which task each step runs on, and name three things that must never happen in the button's callback.
- [ ] Compare your Practice answer against this diagram: which box should `read_object_held()` be called from?

## Going further

Now we know how the chip signs, and how it must be accessed. The next module follows that signature into the TLS handshake:
when the chip is called, which certificate is sent, and how to read the symptoms when a connection fails.

Next lesson: [Lesson 3.1: TLS and mTLS](../../m03-mtls-to-platform/l01-tls-and-mtls/README.md)

## Reflect

- In firmware you have written before, which shared resource was protected only during "setup," without covering the actual span it was used?
- In a function with several exit paths in your own code, does every one of them return its resources? How do you know?
- How would your users tell "the screen is doing long work" apart from "the device has hung"?

## References

- [SDK: cm33/security/03_chip_ownership.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/03_chip_ownership.c)
- [SDK: cm33/security/04_touch_hold.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/security/04_touch_hold.c)
- [SDK: cm55/security/01_hsm_screens.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/security/01_hsm_screens.c)
- [D1 — The chip-access discipline: gate, lock, touch-hold (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d1__chip__access__discipline.html)
- [Chip gate & manager (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__tesaiot__hsm__chip__manager.html)
- [C3 — TESAIoT cloud: config file → MQTT task → broker (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c3__cloud__mqtt.html)
