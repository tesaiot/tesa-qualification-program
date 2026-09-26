---
id: sec-iot.m04.l01
lang: en
title: {th: Secure boot และ chain of trust, en: Secure boot and the chain of trust}
summary: {th: ตามลำดับการบูตของบอร์ดและดูว่าแต่ละขั้นตรวจขั้นถัดไปอย่างไร, en: Follow the board's boot order and how each stage checks the next.}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m03.l02]
objectives:
- {th: อธิบายบทบาทของคอร์ CM33_S ในการบูตแบบปลอดภัยของแม่แบบเฟิร์มแวร์, en: Explain the role of the CM33_S core in the template's secure boot.}
- {th: วาดห่วงโซ่ความเชื่อใจตั้งแต่ ROM จนถึงแอปพลิเคชัน และระบุว่าลายเซ็นถูกตรวจที่ขั้นใด, en: Draw the chain of trust from ROM to application and mark where signatures are checked.}
- {th: อธิบายความต่างระหว่าง secure boot กับการเข้ารหัสเฟิร์มแวร์, en: Explain the difference between secure boot and firmware encryption.}
develops:
- {skill: sec.secure-boot, to: 3}
- {skill: mcu.bootloader, to: 2}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
slides: slides.md
source:
- {repo: 'https://github.com/tesaiot/tesaiot-pse84-devkit-sdk', path: bento-firmware-template-mtb-only/configs, ref: ef72c1b658178eee8c38b1e47d28b006f80a59b5, license: Apache-2.0}
- {repo: 'https://github.com/Infineon/mtb-example-psoc-edge-basic-secure-app', path: README.md, ref: 96783c046340f79940f7d50b1c5c25fef4a0797f, note: 'Boot flow facts paraphrased; linked, not copied.'}
source_sha256: ef4e0e0c8fc0337ab8cbf68ef77103f68f9dfd3d79b997b83979ba1d1053ce11
---

# Lesson 4.1: Secure boot and the chain of trust

> Module 4 · Secure boot and Protected Update · [Module overview](../README.md) · [Course home](../../README.md)

mTLS proves the key lives inside the chip, but if the firmware that commands the chip has been swapped, an attacker can have the chip sign on our behalf anyway (lesson 1.2).
So this lesson's question is: "is the firmware running right now the firmware we meant to run?" — and on this board, who checks that, and how far does the check go?

## Objectives

By the end of this lesson you will:

1. Explain the role of the CM33_S core in the firmware template's secure boot
2. Draw the chain of trust from ROM to application, and mark where signatures are checked
3. Explain the difference between secure boot and firmware encryption

## Before you start

- **Already covered:** [Lesson 3.2: MQTTs to the TESAIoT Platform](../../m03-mtls-to-platform/l02-mqtts-to-tesaiot/README.md), and review signatures from [lesson 1.2](../../m01-threats-and-crypto/l02-crypto-basics/README.md)
- **Software:** the SDK's `bento-firmware-template-mtb-only` template at `ef72c1b`, already building
- **What this lesson will not have you do:** provisioning a device to enable secure boot (`secure_boot=true` in the OEM policy), and transferring device ownership with an OEM key.
  The README of [Infineon's basic secure app example](https://github.com/Infineon/mtb-example-psoc-edge-basic-secure-app) says that once provisioned, Extended Boot opens the first image only if its signature verifies.
  This changes the device's behaviour at the chip level, and must follow [AN237849 Getting started with PSOC™ Edge security](https://www.infineon.com/AN237849), done by someone who has already decided to do it and who can manage the OEM key.

## See it work first

The "which core does what" table in the [template's README](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/README.en.md) has this as its first row.

| Core | Runs | Typical work |
|---|---|---|
| **CM33_S** | secure boot | you will not touch this |

Meanwhile [proj_cm33_s/main.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_s/main.c), the whole file, is under fifty lines.
Its header comment reads "CM33 Secure boot - TrustZone setup and jump to CM33_NS." Inside `main()` there is only `cybsp_init()`, enabling interrupts,
reading the stack pointer and reset handler from CM33_NS's vector table, and jumping there.

**Guess first:** before jumping, does CM33_S verify the signature of the CM33_NS firmware? And if not, who checks what?

## Concepts

### 1. The role of CM33_S

The PSoC™ Edge E84 has three cores, and its main Cortex-M33 is split into secure and non-secure sides with TrustZone. So the template has three projects: `proj_cm33_s`, `proj_cm33_ns`, `proj_cm55`.
Infineon's example README explains the order: Extended Boot opens the CM33 secure project from a fixed location in memory.
CM33 secure sets up protections, then opens the CM33 non-secure app; CM33 non-secure then starts the CM55 core.
In our template, this last step lives in `init_cm55_boot()`, which calls `Cy_SysEnableCM55()`, per [chapter B1 of the SDK docs](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__b1__cm33__boot.html).

So CM33_S is the **first user image** that Extended Boot sees, and the only joint where Extended Boot can verify a signature at all.
The template's [common.mk](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/common.mk) has a `SECURE_BOOT` switch with two values.

- `SECURE_BOOT=0` (the default) uses `configs/boot_with_extended_boot.json`. The CM33_S image gets only the MCUboot header and is **not signed.**
- `SECURE_BOOT=1` uses `configs/secure_boot_with_extended_boot.json`. The CM33_S image is signed with the OEM root-of-trust key that a device provisioned `secure_boot=true` requires.
  The build log prints confirmation of which key file CM33_S will be signed with.

Any value other than `0` or `1`, such as `true` or `yes`, makes the build **stop with an error** immediately. The comment in the file explains why: a mistyped value must never turn into a silently unsigned build.

### 2. This board's chain of trust, and where signatures are actually checked

The **root of trust** is the part we trust with no one else checking it. ETSI EN 303 645 provision 5.7-1 explains that a hardware root of trust is one way to make secure boot meaningful.
On this board, that starting point is Infineon's code inside the chip, and each stage opens the next. The question is: **before opening it, is there a check?**

```text
 Boot ROM (Infineon's code inside the chip)
    │
    ▼
 Extended Boot (Infineon's)
    │   verifies the CM33_S image's signature with the OEM key
    │   ✔ when the device is provisioned secure_boot=true and built with SECURE_BOOT=1
    │   ✘ in the template's default state (SECURE_BOOT=0)
    ▼
 CM33_S  (proj_cm33_s)   cybsp_init(), then jumps to CM33_NS's reset handler
    │   ✘ does not verify CM33_NS's signature (the template's main.c)
    ▼
 CM33_NS (proj_cm33_ns)  FreeRTOS, PSA + the OPTIGA driver, WiFi, MQTT, then Cy_SysEnableCM55()
    │   ✘ does not verify CM55's signature
    ▼
 CM55    (proj_cm55)     display, Edge AI
        ◦ an AI model uploaded at runtime goes through the optiga_verify_staged_model() hook (lesson 1.2)
```

The evidence that signing covers only CM33_S is in `secure_boot_with_extended_boot.json`: the `sign` stage takes exactly one input file, `proj_cm33_s.hex`.
`proj_cm33_ns.hex` only goes through the `hex-relocate` stage, and `proj_cm55.hex` goes straight into a `merge` stage; all three are combined into one `app_combined.hex` file.

**A conclusion that belongs in your threat model:** even with secure boot fully enabled, this template's chain breaks right after CM33_S. Whoever can write to the flash region of CM33_NS or CM55 can run their own code, unchecked.
If your work needs a complete chain, CM33_S (or a bootloader sitting there) must verify the next image before jumping to it. Infineon has an EdgeProtect Bootloader that the example README references, but this template does not use it.

There are two other places in this course where a signature is checked, but **neither is a boot stage:**

- A Protected Update manifest is verified **inside the chip**, by the OPTIGA™ Trust M, before it writes an object (lesson 4.2)
- The hook that verifies an AI model uploaded at runtime — in the SDK, this defaults to a weak function that answers "this device cannot verify signatures" (`-10`), per the `02_model_signature_hook.c` example

### 3. Secure boot is not firmware encryption

These two answer different questions.

| | Secure boot | Firmware encryption |
|---|---|---|
| Answers | Does this code come from the key's owner, unaltered? | Can someone else read this code? |
| Property | Integrity and authenticity | Confidentiality |
| Tool | A digital signature, verified with a public key the device trusts | Symmetric encryption, needing a private key on the device to decrypt |
| Does not protect against | Someone reading the code in flash, a bug in already-signed code, an attack at runtime | Running different code in its place, if no signature check accompanies it |

This template has no image-encryption stage in either config file, so even with secure boot enabled, anyone who can read flash can still read the code.
Secrets embedded in the image (such as a compiled-in password) get no protection from secure boot at all — this is another reason for ETSI provision 5.4-3 from lesson 3.2.

One more small thing worth noticing: the signed config sets `security-counter` to `1`, which, in MCUboot's format, is the number used to prevent image rollback.
The documentation this course could check does not confirm how Extended Boot enforces this number, so it does not yet count as a verified firmware anti-rollback mechanism. Lesson 4.2 looks at the anti-rollback mechanism that can actually be verified, inside the OPTIGA™ chip.

## Worked example

The header comment of [secure_boot_with_extended_boot.json](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/configs/secure_boot_with_extended_boot.json), lines 1–15
(TESAIoT PSE84 Dev Kit SDK, © Thai Embedded Systems Association, Apache-2.0)

```text
// Signed variant of boot_with_extended_boot.json — selected by SECURE_BOOT=1 in common.mk.
//
// Identical to boot_with_extended_boot.json except the CM33_S sign stage additionally
// carries "signing-key" + "security-counter", which turn the MCUboot metadata into a real
// OEM signature that Extended Boot verifies once the device is provisioned secure_boot=true.
//
// Geometry (header-size / fill-value / slot-size / hex-address) is intentionally IDENTICAL to
// the unsigned config — it is this project's real flashmap. Do NOT replace it with the values
// from mtb-example-psoc-edge-basic-secure-app (slot-size 0x80000, hardcoded 0x70100000).
//
// {{OEM_SIGNING_KEY}} is supplied by common.mk via:
//     MTB_COMBINE_SIGN_ARGS += -s OEM_SIGNING_KEY "$(SECURE_BOOT_KEY)"
// Override the key with:  make SECURE_BOOT=1 SECURE_BOOT_KEY=/abs/path/to/key.pem
// If you invoke run-config by hand you MUST pass -s OEM_SIGNING_KEY <path>; an unset
// variable is a hard error ("Unknown variable: OEM_SIGNING_KEY"), never a silent unsigned build.
```

Reading this gives you three things:

1. **Only two fields differ from the unsigned version** — `"signing-key"` and `"security-counter"` in CM33_S's sign stage. The MCUboot header is already present in both.
2. **The signature only means something once the device has been provisioned.** A board not yet provisioned `secure_boot=true` does not check this signature at all.
3. **The author designed it to "fail loudly."** If no key is supplied, the build must error out, not silently produce an unsigned image — the same principle as `common.mk` refusing any `SECURE_BOOT` value besides `0` and `1`.

## Practice

For each statement below, is it true of **secure boot**, **firmware encryption**, **both**, or **neither**?

1. Stops a competitor who buys the board from reading flash and understanding the code ____
2. Stops a provisioned board from booting an image signed with a different key ____
3. Prevents a buffer overflow bug in correctly signed code ____
4. Needs a private key present on the device to work ____
5. Prevents CM55's firmware from being swapped in this template, even with `SECURE_BOOT=1` and provisioning done ____

<details><summary>Solution</summary>

1. **Firmware encryption**
2. **Secure boot**
3. **Neither** — signed code can still have bugs; a signature only tells you who it came from
4. **Firmware encryption** — needs a decryption key on the device; secure boot only needs a public key to verify with
5. **Neither** — in this template, signing covers only the CM33_S image

</details>

## Check your understanding

The questions below are part of the full set in [quiz.yaml](quiz.yaml), which the automated grader uses.

1. In the template's `proj_cm33_s/main.c`, what does CM33_S do before starting CM33_NS? *(objective 1)*
   - a) Verifies CM33_NS's signature with the OPTIGA™ Trust M
   - b) `cybsp_init()`, then reads the stack pointer and reset handler from CM33_NS's vector table and jumps there
   - c) Decrypts the CM33_NS image
   - d) Connects to WiFi

   <details><summary>Solution</summary>

   **b.** There is no signature check at this stage, which is why the template's chain breaks right after CM33_S.

   </details>

2. You build with `SECURE_BOOT=1` and flash a board that is **not yet** provisioned `secure_boot=true`. What happens? *(objective 2)*
   - a) The board does not boot
   - b) Extended Boot has not yet been forced to check the signature, so having a signature adds no protection yet
   - c) The OPTIGA chip locks
   - d) LcsO changes to operational

   <details><summary>Solution</summary>

   **b.** The comment in the config says Extended Boot checks this signature "once the device is provisioned secure_boot=true."

   </details>

3. Which statement correctly describes the difference between secure boot and firmware encryption? *(objective 3)*
   - a) Secure boot hides the code; encryption confirms who wrote it
   - b) Secure boot confirms the code comes from the key's owner and is unaltered; encryption stops others from reading the code
   - c) They are the same thing
   - d) Secure boot needs a private key on the device

   <details><summary>Solution</summary>

   **b.** You need both together if you want integrity and confidentiality. This template has no image-encryption stage.

   </details>

## Lab

**Read your board's chain from the evidence.** This lesson does not provision anything, and does not flash a signed image.

- [ ] **1. Diff the two configs** from the template's folder.
  ```bash
  diff configs/boot_with_extended_boot.json configs/secure_boot_with_extended_boot.json
  ```
  Write down every line that differs. Besides comments, how many fields are left? Does it match item 1 in the worked example?
- [ ] **2. Prove the build system fails loudly.** Build with an invalid value and record the error message.
  ```bash
  make build SECURE_BOOT=yes
  ```
  Write one sentence on why this command **failing** is a good thing.
- [ ] **3. Count what actually gets signed.** Open `configs/secure_boot_with_extended_boot.json`, find every `"command"`, and write a table of which stages each core's hex file goes through (sign, hex-relocate, merge).
- [ ] **4. Draw your own chain**, in two versions: the board you are holding right now, and a shipped product with secure boot fully enabled. Mark ✔ or ✘ at every joint, each with one line of evidence (file and line).
- [ ] **5. Update the threat model** from lesson 1.1, in the T row about firmware and in the ETSI 5.7-1 row, to reflect what you found, including the fact that the chain breaks after CM33_S.
- [ ] **6. Read further (no need to do it)** in the README of [Infineon's basic secure app example](https://github.com/Infineon/mtb-example-psoc-edge-basic-secure-app). Write down the list of steps that must happen on a device before Extended Boot starts checking signatures, and mark which step you think needs someone's sign-off before it happens.

## Going further

Secure boot answers the question about firmware at power-on, but some data inside the chip — a device's certificate, for instance — must be changeable over the device's lifetime.
The next lesson looks at how the OPTIGA™ Trust M accepts that change without trusting the host, and how it prevents rollback.

Next lesson: [Lesson 4.2: Protected Update](../l02-protected-update/README.md)

## Reflect

- In your own product, where does the chain of trust break, and who can write to the part that goes unchecked?
- If the OEM key used for signing were to leak, how would you find out, and what would you do next?
- Does your customer need the confidentiality of the code, the integrity of the code, or both?

## References

- [SDK: the mtb-only template README (CM33_S secure boot)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/README.en.md)
- [B1 — CM33_NS boot walk-through (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__b1__cm33__boot.html)
- [SDK: common.mk (the SECURE_BOOT switch)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/common.mk)
- [SDK: configs/secure_boot_with_extended_boot.json](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/configs/secure_boot_with_extended_boot.json) and [boot_with_extended_boot.json](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/configs/boot_with_extended_boot.json)
- [SDK: proj_cm33_s/main.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_s/main.c)
- [Infineon: PSOC™ Edge MCU basic secure application](https://github.com/Infineon/mtb-example-psoc-edge-basic-secure-app) (linked, not copied)
- [Infineon AN237849: Getting started with PSOC™ Edge security](https://www.infineon.com/AN237849)
- [PSA Certified](https://www.psacertified.org/)
- [ETSI EN 303 645 V3.1.3 (2024-09)](https://www.etsi.org/deliver/etsi_en/303600_303699/303645/03.01.03_60/en_303645v030103p.pdf), provision 5.7
