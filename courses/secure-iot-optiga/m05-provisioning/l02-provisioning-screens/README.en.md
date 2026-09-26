---
id: sec-iot.m05.l02
lang: en
title: {th: หน้าจอลงทะเบียนบนอุปกรณ์, en: Provisioning screens on the device}
summary: {th: ส่งงานที่ใช้เวลาหลายวินาทีให้หน้าจอที่คอยถามสถานะ และปิดหน้าจอเก่าก่อนเปิดใหม่เสมอ, en: Hand seconds-long secure-element work to a polling screen and always tear the previous overlay down first.}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m05.l01]
objectives:
- {th: อธิบายว่าทำไมหน้าจอลงทะเบียนต้องถามสถานะเป็นระยะแทนการรอผลของชิป, en: Explain why the provisioning screen polls instead of waiting on the chip.}
- {th: เรียงลำดับการปิดหน้าจอเก่าและเปิดหน้าจอลงทะเบียนตามตัวอย่างของ SDK ได้ถูกต้อง, en: Order the overlay teardown and the enrol screen opening as the SDK example does.}
develops:
- {skill: sec.secure-element, to: 3}
- {skill: gui.embedded, to: 2}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
slides: slides.md
source:
- {repo: 'https://github.com/tesaiot/tesaiot-pse84-devkit-sdk', path: bento-firmware-template-mtb-only/proj_cm55/examples/security/01_hsm_screens.c, ref: ef72c1b658178eee8c38b1e47d28b006f80a59b5, license: Apache-2.0}
source_sha256: 01946a3c6a7a7331859e4fa6f1e85e8483c0af798baed17e63225027655ad415
---

# Lesson 5.2: Provisioning screens on the device

> Module 5 · Secure device provisioning · [Module overview](../README.md) · [Course home](../../README.md)

Enrolment in the last lesson took anywhere from several seconds to a full minute. During that time, whoever is holding the board needs to know something is happening, and the screen must not freeze.
This lesson looks at how the SDK's Enrol and Protect screens are designed: why they poll for status periodically, and why they must tear down the previous overlay before opening a new one, **every time.**

## Objectives

By the end of this lesson you will:

1. Explain why the provisioning screen polls for status periodically instead of waiting on the chip
2. Correctly order tearing down the old overlay and opening the enrolment screen, as the SDK's example does

## Before you start

- **Already covered:** [Lesson 5.1: Enrolment with a CSR](../l01-csr-enrolment/README.md), and Concepts section 3 of [lesson 2.2](../../m02-optiga-trust-m/l02-chip-access-discipline/README.md) (long work must leave the display task)
- **Review LVGL:** button events and screen state machines, from [TESAIoT Firmware Stack lesson 2.2](../../../tesaiot-firmware-stack/m02-hmi-menu-setting/l02-button-event/README.md) and [lesson 2.7](../../../tesaiot-firmware-stack/m02-hmi-menu-setting/l07-final-wifi-manager/README.md)
- **Board:** the SDK's template, built with `ENABLE_PAGE_EXAMPLES=1`. This lesson's lab **removes the platform credentials from the config file first**, so enrolment stops right at the connection step and no key ever gets generated.

## See it work first

The header comment of [01_hsm_screens.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/security/01_hsm_screens.c) states two things.
First, if you wait for the chip's result inline, the screen freezes, **and** `ui_busy_modal_service()` — the very thing meant to draw a window explaining why it is frozen — cannot draw either, so the screen goes "dead AND silent."
Second, if the previous round's window is still open, opening another gets silently refused, because `shell_open()` returns immediately when one already exists.

**Guess first:** for whoever is holding the board, is "the screen is frozen and silent" different from "I tapped it and nothing happened"? What would each symptom make them do next?

## Concepts

### 1. Why poll, instead of waiting

The work behind the Enrol screen takes a long time for three reasons we have already met. Asking for the chip's gate can wait up to ten seconds (lesson 2.2).
Generating a key pair and signing a CSR is a long transaction with the chip. And waiting for the platform's reply can take up to 60 seconds (chapter D2).
If the LVGL task waited on any of this itself, the whole screen would stop drawing.

[Chapter D2 of the SDK docs](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d2__enrolment__protected__update.html) shows that the SDK splits the work into three layers.

```text
 CM55 (display)                          CM33_NS
 Enrol button → hsm_enrol_open()
   opens a full-screen overlay
   sends IPC_CMD_HSM_PROVISION (op=CSR) ─▶ handle_hsm_provision()
   ◀─────────────── returns immediately ──   if work is already running, refuses with HSM_PROV_REJECTED_BUSY
                                              sets pending_op
   lv_timer polls with op=POLL ─────────▶  prov_task checks pending_op every 50 ms and calls prov_run(op)
   ◀── state, step, message ────────────   prov_say(state, step, "a human-readable sentence")
   draws the state, draws the message, loops
```

The values that travel over IPC, per chapter D2: op `POLL 0`, `CSR 1`, `PU 2`, `FETCH_CSR 3`, `UNLOCK 4`; state `IDLE/BUSY/DONE/FAILED`;
and step `KEYGEN 1`, `CSR 2`, `PUBLISH 3`, `WAIT 4`, `INSTALL 5`, `VERIFY 6`. The screen never needs to know what the chip is actually doing — it just asks "how far along are we now?" and draws.

While the chip is working, the firmware holds a touch-hold with a reason message, which appears on screen during the window when the screen refuses touches.
But during the 60-second wait for the platform, no hold is held at all, so the screen keeps responding (chapter D1's pitfall 5).
The seven on-screen sentences we saw in lesson 5.1 come from `prov_say()` on the CM33_NS side; chapter D2 confirms these are verified strings straight from the source.
As for the per-step labels living in `libbento_cm55.a`, chapter D2 warns that it cannot yet prove which label pairs with which step, because the display's files were not shipped as source — treat the seven sentences as your evidence instead.

### 2. Always tear down the old one first

`hsm_provision_ui_teardown()` closes whatever overlay is still open, and **cancels its status-polling timer.** It can be called repeatedly, and is safe even when nothing is open.
It guards against two problems.

- **Tap and silence.** Without tearing down the old one, opening a new overlay gets silently refused; whoever tapped assumes the device is not responding.
- **A stale timer writing into a freshly created screen.** The previous round's timer is still firing, and would write into LVGL objects that have already been deleted or recreated.

Chapter D2 therefore has the HSM page call `hsm_provision_ui_teardown()` as the **last command** in its destroy callback, after deleting the page's own timer.
Otherwise, the status-polling timer might fire after the objects have already been freed.

### 3. Screens that tell the truth

These two screens are designed to let whoever is holding the board make the right call.

- The **Protect** screen shows the full set of changes that are about to happen **before** doing them, and writes nothing until confirmed (comment in 01_hsm_screens.c)
- The **Enrol** screen, when it meets an already-locked slot, says "This slot takes signed manifests only ... Nothing was changed." before generating any key at all (lesson 4.2)
- The final verdict splits into three distinct cases, per chapter D2: "The device can prove it holds the key this certificate names," or "Installed, but the certificate does not belong to this chip's key," or "Installed; the pair check could not run."
  These three sentences differ because they call for different responses — the same principle as the result codes in `02_model_signature_hook.c`, which never collapse "no signature" and "could not verify" into one value.

## Worked example

Taken from [01_hsm_screens.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/security/01_hsm_screens.c), lines 55–74 and 78–80
(TESAIoT PSE84 Dev Kit SDK, © Thai Embedded Systems Association, Apache-2.0)

```c
    /* Idempotent, and first. If an earlier run's overlay is still up, opening
     * another would be refused silently -- shell_open() returns when one
     * already exists -- and the tap would look like it did nothing. */
    hsm_provision_ui_teardown();

    if (s_open_protect_next) {
        s_open_protect_next = false;
        hsm_protect_open();
        sdk_example_logf("opened Protected Update.");
        sdk_example_logf("it shows the pending change set BEFORE running it --"
                         " nothing is written until you confirm.");
        sdk_example_logf("tap this example again for the Enrol screen.");
    } else {
        s_open_protect_next = true;
        hsm_enrol_open();
        sdk_example_logf("opened Enrol Certificate.");
        sdk_example_logf("key pair -> CSR -> proof of possession -> certificate;"
                         " each step polls, none of it blocks this task.");
        sdk_example_logf("tap this example again for the Protected Update screen.");
    }
```

```c
    /* The screen is up and its own poll timer owns the work from here. That is
     * asynchronous progress, not a completed job. */
    return SDK_EX_STARTED;
```

The order to remember is **tear down the old one → open the new one → return "started"** — not "finished."
The value `SDK_EX_STARTED` tells the caller directly that the work is still running, and that from this point on the screen's own timer owns it, not this function.

## Practice

Your screen has an "Enrol" button, and its own timer named `s_clock_timer`. Fill in the blanks in the right order. (This code is written fresh for this lesson, using the SDK's API and LVGL 9.)

```c
static lv_timer_t *s_clock_timer;

static void enrol_btn_cb(lv_event_t *e)
{
    (void)e;
    ____(1)____();          /* always, before opening anything */
    ____(2)____();          /* opens the Enrol overlay; the real work runs on CM33_NS */
    /* this function never waits for a result */
}

void my_page_destroy(void)
{
    if (s_clock_timer != NULL) {
        ____(3)____(s_clock_timer);   /* delete this page's own timer */
        s_clock_timer = NULL;
    }
    ____(4)____();          /* tear down the provisioning overlay and its poll timer, as the last command */
}
```

<details><summary>Solution</summary>

1. `hsm_provision_ui_teardown` — safe to call repeatedly, and safe even when no overlay is open
2. `hsm_enrol_open`
3. `lv_timer_delete` (the LVGL 9 name that `page_hsm_destroy()` in chapter D2 uses)
4. `hsm_provision_ui_teardown`, last of all, following `page_hsm_destroy()`'s pattern, so no timer fires into objects that have already been deleted

</details>

## Check your understanding

The questions below are part of the full set in [quiz.yaml](quiz.yaml), which the automated grader uses.

1. If the Enrol screen waited for the chip's result inline inside the LVGL task, what would whoever is holding the board see? *(objective 1)*
   - a) The screen shows step-by-step progress normally
   - b) The whole screen freezes, and the window meant to explain why cannot draw either, so the screen goes both dead and silent
   - c) The chip works faster
   - d) Enrolment cancels itself automatically

   <details><summary>Solution</summary>

   **b.** This is why `IPC_CMD_HSM_PROVISION` returns immediately, and an `lv_timer` polls status periodically instead.

   </details>

2. Which order is correct when the user taps the button that opens the provisioning screen? *(objective 2)*
   - a) `hsm_enrol_open()`, then `hsm_provision_ui_teardown()`
   - b) `hsm_provision_ui_teardown()`, then `hsm_enrol_open()`, then return that it has started
   - c) `hsm_enrol_open()`, then wait until it finishes
   - d) No need to tear down the old one — LVGL handles that itself

   <details><summary>Solution</summary>

   **b.** If an old overlay is still open, opening a new one gets silently refused, per the example's comment.

   </details>

3. Why must `hsm_provision_ui_teardown()` be the last command in the page's destroy callback? *(objective 2)*
   - a) So the status-polling timer gets cancelled and never fires into LVGL objects that have already been freed
   - b) Because it is the slowest step
   - c) So enrolment restarts
   - d) Because it clears the correlation id

   <details><summary>Solution</summary>

   **a.** Chapter D2 gives the reason: a timer that fires after the object has been freed would be referencing memory that no longer exists.

   </details>

## Lab

**Watch the real polling screen, without really enrolling**

- [ ] **Make the board safe first.** Delete or blank out `device_id` and `mqtt_pass` in the `/.tesaiot_config` file (lesson 3.2). Keep the real values somewhere that is not a repository.
  Chapter D2 states that enrolment connects to the platform **before** generating any key. If it cannot connect, it stops right there, with no key ever created (the message D2 records for the no-reply case is "No answer from the platform after 30 seconds.")
- [ ] Build with `ENABLE_PAGE_EXAMPLES=1`, flash, then unplug the USB cable, count to ten, and plug it back in. Open the SDK Examples card on screen, select `cm55/security/01_hsm_screens`, and Run.
- [ ] The Enrol overlay opens. Record every message that appears, in order, with roughly how long each takes. While waiting, try tapping Back, and note during which windows the screen responds and during which it does not (look for the touch-hold's reason message).
- [ ] Press Back, then Run again — you get the Protect overlay this time. Record what this screen shows **before** asking you to confirm, then press Back **without confirming.**
- [ ] Read the example's log on the SDK Examples page after pressing Back. Does the message `each step polls, none of it blocks this task` match what you observed?
- [ ] Draw a state × step table for a provisioning screen in your own work (using chapter D2's six step values), and write the sentence the screen should show in each cell — especially in the FAILED cell, state clearly what was **not** changed.
- [ ] Restore `device_id` and `mqtt_pass` in the config file, then reconnect to the platform per lesson 3.2, to get ready for the capstone.

## Going further

We now have every piece: the threat model, the mTLS channel, the boot chain, Protected Update, enrolment, and screens that tell the truth.
The final lesson brings it all together into one device, with evidence that it actually works.

Next lesson: [Lesson 5.3: Capstone — one secure device](../l03-capstone-secure-device/README.md)

## Reflect

- In your own product, which task takes over a second, but is still being waited on inside the task that draws the screen?
- Does an error message on your screen say what was **not** changed?
- If a user taps a button twice in quick succession, what does your system do — and have you already tested that case?

## References

- [SDK: cm55/security/01_hsm_screens.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm55/examples/security/01_hsm_screens.c)
- [SDK: hsm_provision_ui.h docs](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/docs/sdk/cm55_core/hsm_provision_ui.md)
- [Security / HSM: Tutorials (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__feat__security__tut.html)
- [D1 — The chip-access discipline: gate, lock, touch-hold (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d1__chip__access__discipline.html)
- [D2 — Enrolment and Protected Update end to end (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__d2__enrolment__protected__update.html)
