---
id: sec-iot.m01.l01
lang: en
title: {th: Threat model ของอุปกรณ์ IoT, en: Threat modelling an IoT device}
summary: {th: ระบุทรัพย์สิน ผู้โจมตี และช่องทางโจมตีของอุปกรณ์หนึ่งชิ้น แล้วเลือกมาตรการที่ตรวจได้, en: 'Name the assets, attackers and attack paths of one device and pick verifiable mitigations.'}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: []
objectives:
- {th: ระบุทรัพย์สินที่ต้องปกป้องของอุปกรณ์ IoT หนึ่งชิ้นได้อย่างน้อยสี่รายการ, en: Name at least four assets to protect on one IoT device.}
- {th: จัดภัยคุกคามตามหมวด STRIDE และจับคู่แต่ละภัยกับมาตรการป้องกันที่ตรวจได้, en: Classify threats with STRIDE and pair each with a verifiable mitigation.}
- {th: เทียบ threat model ของตัวเองกับข้อกำหนดพื้นฐานของ ETSI EN 303 645 และระบุข้อที่ยังขาด, en: Compare your threat model with the ETSI EN 303 645 baseline and list what is missing.}
develops:
- {skill: sec.fundamentals, to: 3}
- {skill: soft.problem-solving, to: 2}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
source:
- {repo: 'https://github.com/tesaiot/tesaiot-pse84-devkit-sdk', path: bento-firmware-template-mtb-only, ref: ef72c1b658178eee8c38b1e47d28b006f80a59b5, license: Apache-2.0, note: 'SDK files are linked and quoted in short excerpts, not copied.'}
- {repo: 'https://www.etsi.org/deliver/etsi_en/303600_303699/303645/03.01.03_60/', path: en_303645v030103p.pdf, note: 'Provision numbers cited; wording paraphrased.'}
source_sha256: ff485e9ddd4a402a30f74800eaa566304eb8d0a991a7487fea7ba9eb1876e05e
---

# Lesson 1.1: Threat modelling an IoT device

> Module 1 · Threat modelling and crypto fundamentals · [Module overview](../README.md) · [Course home](../../README.md)

Before touching a single secure-element command, we will sit down and think like an attacker about one device, start to finish.
This lesson uses a sensor node on the TESAIoT Dev Kit that sends data to the TESAIoT Platform over MQTTS as the running example for the whole course.

## Objectives

By the end of this lesson you will:

1. Name at least four assets that need protecting on one IoT device
2. Classify threats using the STRIDE categories and pair each one with a verifiable mitigation
3. Compare your own threat model against the ETSI EN 303 645 baseline and list what is still missing

## Before you start

- **Prior knowledge:** C at a level where you can read someone else's code, and the MQTT publish/subscribe principle.
  If you have never sent data to the platform before, you can read [lesson 5.1 of the TESAIoT Firmware Stack course](../../../tesaiot-firmware-stack/m05-connect-to-platform/l01-server-tls/README.md) first.
- **Hardware:** this lesson is mostly paper-based thinking; you do not need to plug in the board yet. But if you have a TESAIoT Dev Kit in hand, picking it up to look at its ports and cables will help you picture what an attacker can reach.
- **Template:** download [resources/threat-model-template.md](resources/threat-model-template.md) to fill in during the lab. This piece of work comes back again in the capstone lesson 5.3.

**The course's example device** is the `bento-firmware-template-mtb-only` firmware template in the TESAIoT PSE84 Dev Kit SDK (commit `ef72c1b`) running on the TESAIoT Dev Kit.
It reads the board's on-board sensor, joins WiFi using credentials from storage on the board, then connects over MQTTS to `mqtt.tesaiot.dev`.
It publishes to the `device/<device_id>/telemetry` topic and subscribes to commands at `device/<device_id>/commands/#`.
The connection has two main modes: server-TLS (the device authenticates with a username and password, on port 8884) and mTLS (the device authenticates with a key inside the OPTIGA™ Trust M, on port 8883).
These facts come from chapter [C3 of the SDK docs](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c3__cloud__mqtt.html).

## See it work first

Here are the lines the firmware prints over UART while connecting to the platform (text as in the C3 chapter's source; real values replace `%s` and `%u`)

```text
[MQTT] Waiting for WiFi...
[MQTT] WiFi connected
[MQTT] Start request received
[MQTT-Config] Mode=%d, Broker=%s:%u, Client=%s, User=%s, PassLen=%u
[MQTT] Instance created
[MQTT] Connecting to '%s:%u' as '%s'...
[MQTT] Connected to broker
```

Look closely at the `[MQTT-Config]` line. It prints the username, but prints the password only as its **length** (`PassLen`).
The [10_wifi_join.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/10_wifi_join.c) example does the same thing with the WiFi password,
and its comment gives the reason: the console is not radio, and a console screen is often visible to other people too.

That means the firmware's author has already done at least one piece of threat modelling: treating the UART line as a leak channel.
**Before reading on**, write down five things on this board that an attacker would want, then compare your list against the table in the next section.

## Concepts

### 1. Assets, attackers and trust boundaries

Threat modelling, following [OWASP](https://owasp.org/www-community/Threat_Modeling), starts from four questions:
what are we working on, what can go wrong, what are we going to do about it, and did we do a good enough job.
The first question forces us to draw the system's boundary before anything else; the last one forces every mitigation to be verifiable.

An **asset** is anything that hurts someone if it loses confidentiality, loses integrity, or becomes unavailable.
Our sensor node has at least this many:

| Asset | Where it lives on this node | Property to protect |
|---|---|---|
| The device identity's private key | Inside the OPTIGA™ Trust M, slots `0xE0F0` (factory key) and `0xE0F1` (TESAIoT's key) | Confidentiality, and no one else must be able to impersonate us with it |
| The certificate and `device_id` | Slot `0xE0E1` in the chip and the config file `/.tesaiot_config` | Integrity |
| The trust anchor used to verify the server | `tesaiot_root_ca.h`, compiled into the firmware | Integrity — if it is swapped, the device will trust a fake server |
| The WiFi password and the MQTT password (server-TLS mode) | The credential store on LittleFS and `tesaiot_config_store` | Confidentiality |
| The firmware of all three cores | Flash memory | Integrity |
| Telemetry | In transit to the broker | Integrity, and confidentiality if the job needs it |
| Commands from the platform | Topic `device/<device_id>/commands/#` | Integrity, and knowing who they came from |
| Continuous operation | The whole system | Availability |
| The chip's lifecycle state (LcsO) | Metadata tag `C0` of the object in the chip | Integrity — a one-way change, cannot be rolled back |

We think about four kinds of **attacker**, each reaching a different boundary:

- A network attacker, on the same WiFi or somewhere on the internet path — can stand up a fake access point, intercept and modify packets
- Someone holding the board — can plug into the debug USB port, read flash, or tap the I2C wires on the board
- Another device on the same platform that has already been compromised, trying to pose as ours
- An insider with access to the broker or the platform

A **trust boundary** is the line where data crosses from a side we control to a side we do not. Every point that crosses this line is a point where you must ask "who is on the other side, and how do we know?"

```text
            [on-board sensor]
                   │ I2C
 [CM55: display and touch] ──IPC── [CM33_NS: WiFi, MQTT] ──I2C (shared bus with touch)── [OPTIGA Trust M]
                                    │
 ═══════════════ boundary: the air ═╪══════════════════════════════════════════════
                                    │ WiFi
                             [access point] ── internet ── [broker mqtt.tesaiot.dev] ── [TESAIoT Platform]
 ═══════════════ boundary: whoever holds the board ═══════════════════════════════
   USB/KitProg port (debug, flash) · I2C wires measurable on the board
```

### 2. STRIDE: six questions to ask at every boundary

STRIDE is a mnemonic for six categories of threat, each paired with the property it violates, following the table in the [OWASP Threat Modeling Process](https://owasp.org/www-community/Threat_Modeling_Process).

| Category | What the attacker does | Property needed |
|---|---|---|
| **S**poofing | Pretends to be someone or something else | Authentication |
| **T**ampering | Modifies data at rest or in transit | Integrity |
| **R**epudiation | Does something and denies doing it, because the system cannot trace it | Non-repudiation |
| **I**nformation disclosure | Reads data it has no right to read | Confidentiality |
| **D**enial of service | Makes the system unusable | Availability |
| **E**levation of privilege | Gains more privilege than it should have | Authorization |

The way to use it is to walk each boundary in the diagram, one at a time, and ask these six questions at that boundary. Once you have a threat, then pick a mitigation.
A category can come up empty, but it must be empty because you thought it through, not because you forgot to ask.

### 3. Verifiable mitigations, and the ETSI EN 303 645 baseline

"We use TLS" is not a verifiable mitigation — it is just the name of a technology.
A verifiable mitigation must state a **test** that would go red if the mitigation were not working, for example:
"Point the broker at a test server using a self-signed certificate; the device must disconnect before sending MQTT CONNECT."
A test that passes every time, whether the mitigation is on or off, proves nothing at all.

Once you have a threat model, compare it against the industry baseline [ETSI EN 303 645 V3.1.3 (2024-09)](https://www.etsi.org/deliver/etsi_en/303600_303699/303645/03.01.03_60/en_303645v030103p.pdf).
Clause 5 of the standard has thirteen sections, from 5.1 (no universal default passwords) through to 5.13 (validate input data).
Each sub-provision has status M (mandatory) or R (recommended) per table B.1 of the standard. The ones that apply directly to our sensor node are:

| Provision | Status | Meaning (paraphrased) |
|---|---|---|
| 5.1-2A | R | Machine-to-machine authentication should not use passwords |
| 5.3-10 | M | If updates are received over the network, the update's authenticity and integrity must always be verified |
| 5.4-1 | M | Persistently stored security parameters must be stored securely (the standard cites a secure element as an example) |
| 5.4-3 | M | Critical security parameters must not be hard-coded in source code |
| 5.5-1 | M | Communicate using best-practice cryptography |
| 5.6-4A | M | Debug ports must be disabled, or protected with authentication |
| 5.7-1 | R | Software should be verified using a secure boot mechanism |
| 5.13-1B | M | Data arriving over the network must be validated before use |

Any provision your threat model has no mitigation for is a **gap** — write it down plainly, with a reason or a plan.

## Worked example

Here is a one-page threat model for the sensor node in its state **today** — server-TLS mode, a normal build of the template.
Each row says how it is verified, and which lesson in the course goes deeper into that topic.

**Scope:** one TESAIoT Dev Kit, the `mtb-only` firmware template at `ef72c1b`, connecting to `mqtt.tesaiot.dev` — not including the platform's back end.

| Category | Threat on this node | Mitigation | How to verify (expected result) | Goes deeper in |
|---|---|---|---|---|
| S | An attacker stands up a fake access point and poses as the broker | Verify the server certificate against the CA pinned in `tesaiot_root_ca.h` | Point `broker=` at a test server with a self-signed certificate; it must fail before MQTT CONNECT | Lesson 3.1 |
| S | Another device that obtained our MQTT password poses as us | Switch to mTLS with the key inside the chip, and have the broker's ACL bind the topic `device/{id}/#` to the certificate | Remove the chip from the bus and reconnect; there must be no backup key in flash to fall back on (chapter C4, Step 3) | Lessons 3.1, 3.2 |
| T | The firmware is swapped for an unsigned one | Extended Boot's secure boot verifies CM33_S's signature | Build with a different key and flash a board provisioned with `secure_boot=true`; it must not boot | Lesson 4.1 |
| T | The certificate in slot `0xE0E1` is overwritten | Protected Update locks the slot to accept only a manifest signed by the anchor | Read metadata tag `D0`; it must read `21 E0 E8`, and a plain write must be rejected | Lesson 4.2 |
| R | Someone denies asking for a certificate or an update | Every request carries a correlation id findable in both the device's log and the platform's log | Pick one request at random; it must be traceable on both sides | Lesson 5.1 |
| I | The WiFi password leaks from the repo or from the console screen | Keep it in the credential store, not a `#define`, and never print the passphrase | Search the whole repo — no SSID or password found — and the log shows `passphrase=N byte(s), not shown` | Lesson 3.2 |
| I | The private key is read out of flash | The key lives inside the OPTIGA™ Trust M, whose metadata denies read access | Search the built image — no private key found | Lesson 2.1 |
| D | Touch and the chip share I2C at the same time, stalling a transaction | A touch-hold wraps the whole transaction | Reconnect 20 times in a row; no `0x0102` must appear in the log | Lesson 2.2 |
| D | The broker drops the session after 90 seconds with no PINGREQ | The task running the MQTT loop must stay alive (enough stack) | Leave the device idle for over 90 seconds; publish must still succeed | Lesson 3.2 |
| E | A request from the network calls a high-risk command | The SDK's trust policy allows HTTPS only risk levels 0 and 1 | Call a risk-level-2 command over HTTPS; it must return `refused` ([07_trust_policy.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/07_trust_policy.c)) | — |

**Gaps against ETSI EN 303 645** as things stand today

1. **5.1-2A (R)** Server-TLS mode authenticates the device with a password; the fix is mTLS in Module 3
2. **5.3-10 (M)** The `c_ota_client` example on the Developer Hub has `file_hash` and `signature` fields in the job document, but the verification function is still a TODO that always returns pass (lesson 4.2)
3. **5.7-1 (R)** The normal build uses `SECURE_BOOT=0`, so the CM33_S image is unsigned (lesson 4.1)
4. **5.6-4A (M)** The template does not handle disabling the debug port; a real product must plan for this itself
5. **5.2-1 (M)** There must be a publicly disclosed vulnerability-reporting policy; this is an organisational task, not something the firmware can help with

Notice that item 5 has nothing to do with code at all. A good threat model must be willing to state which parts are outside the firmware's scope.

## Practice

The table below has five more threats on the same node. Fill in the STRIDE category and write a test that would go red. The first row is done for you.

| Threat | Category | Verifiable test |
|---|---|---|
| An attacker on the same WiFi reads the telemetry payload | I | Capture packets with Wireshark during a publish; you must see only TLS records, never the JSON message |
| Someone sends a forged `commands/...` message to control the device | ____ | ____ |
| Someone publishes so fast the publisher's queue fills up and our data is lost | ____ | ____ |
| A user with read-only rights on the platform can issue a firmware-write command | ____ | ____ |
| The device sends bad data and then denies having sent it | ____ | ____ |

<details><summary>Solution</summary>

- Forged command: **S** (and T). Test using another device's account to publish into `device/<our device_id>/commands/...`; the broker must refuse it. If it goes through, the ACL is not binding the topic to an identity.
- Full queue: **D**. Chapter C3 says `tesaiot_mqtt_publish()` queues with a zero-second wait; when the queue is full, the message is silently dropped. Test by publishing rapidly and counting whether everything arrives at the far end. If not everything arrives, there must be a counter or a return value that says so.
- Read rights that can still write: **E**. Test with a read-only account; calling a write command must be refused.
- Sent then denied: **R**. Test whether a single message can be traced back to a verified identity for the sender. If several devices share one password, this fails immediately.

</details>

## Check your understanding

The questions below are part of the full set in [quiz.yaml](quiz.yaml), which the automated grader uses.

1. Which of these is an **asset** whose main requirement is integrity, not confidentiality? *(objective 1)*
   - a) The WiFi password in the credential store
   - b) The trust anchor in `tesaiot_root_ca.h`
   - c) The private key in slot `0xE0F1`
   - d) The MQTT password in server-TLS mode

   <details><summary>Solution</summary>

   **b.** The CA certificate is public data — anyone can read it — but if someone can change it, the device will instantly trust a fake server. The other three all need confidentiality.

   </details>

2. Is "the device uses TLS 1.2" a verifiable mitigation? *(objective 2)*
   - a) Yes, because TLS 1.2 is a standard
   - b) No — it must be written as a test whose result can go red, e.g. a forged certificate must break the connection
   - c) Yes, if the log shows `Connected to broker`
   - d) No, because TLS has nothing to do with STRIDE

   <details><summary>Solution</summary>

   **b.** `Connected to broker` can appear even with certificate verification switched off. A meaningful test must try a case that should fail, and actually see it fail.

   </details>

3. Server-TLS mode authenticates the device with a username and password. Which ETSI EN 303 645 provision does this conflict with? *(objective 3)*
   - a) 5.1-2A, no passwords for machine-to-machine authentication
   - b) 5.7-1, secure boot
   - c) 5.13-1B, validating input data
   - d) None of these

   <details><summary>Solution</summary>

   **a.** This provision has status R (recommended), so it is a gap that needs a written reason or a plan. This course's plan is to switch to mTLS.

   </details>

4. You find the threat "an attacker sends a forged command to the commands topic." Which category does it belong to primarily? *(objective 2)*
   - a) Denial of service
   - b) Spoofing
   - c) Information disclosure
   - d) Repudiation

   <details><summary>Solution</summary>

   **b.** The attacker is impersonating the platform or an authorised sender. The mitigation is authentication plus an ACL that binds the topic to an identity.

   </details>

## Lab

**A one-page threat model for your device.** Use the template at [resources/threat-model-template.md](resources/threat-model-template.md).

- [ ] Pick one device — the course's sensor node, or your own project on the TESAIoT Dev Kit. Write its scope in one paragraph.
- [ ] Draw the trust-boundary diagram; it must have at least the air (WiFi) line and the whoever-holds-the-board line.
- [ ] Name at least four assets: where they live, and which property (C, I or A) they need.
- [ ] Walk all six STRIDE categories, producing at least six threats. Every one needs a mitigation and a test that can go red.
- [ ] Compare against the ETSI table in Concepts section 3. Write down at least two gaps, each with its M or R status.
- [ ] Trade with a classmate. Have them find one threat you missed, and add it to the table.

Keep this file — lesson 5.3 will have you come back and update which mitigations are actually in place, and which risks remain.

## Going further

In the example table, almost every mitigation leans on a hash, a signature, encryption, or a certificate. The next lesson pulls these tools apart clearly: which property each one gives you, and which it cannot.

Next lesson: [Lesson 1.2: Crypto fundamentals for embedded systems](../l02-crypto-basics/README.md)

## Reflect

- In a device you have built before, which asset did you not count as an asset at the time?
- Which mitigation in your own work was "put in" but has never had a test that actually proves it works?
- If you had to cut one mitigation for budget or time reasons, which would you cut, and how would you write down the risk that remains?

## References

- [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling)
- [OWASP Threat Modeling Process (the STRIDE table)](https://owasp.org/www-community/Threat_Modeling_Process)
- [OWASP Internet of Things Project](https://owasp.org/www-project-internet-of-things/)
- [ETSI EN 303 645 V3.1.3 (2024-09) Cyber Security for Consumer Internet of Things: Baseline Requirements](https://www.etsi.org/deliver/etsi_en/303600_303699/303645/03.01.03_60/en_303645v030103p.pdf)
- [NIST IR 8259 Foundational Cybersecurity Activities for IoT Device Manufacturers](https://csrc.nist.gov/pubs/ir/8259/final)
- [C3 — TESAIoT cloud: config file → MQTT task → broker (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c3__cloud__mqtt.html)
- [C4 — mTLS: the OPTIGA-backed TLS identity (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c4__mtls__optiga.html)
- [SDK: cm33/connectivity/10_wifi_join.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/10_wifi_join.c) (Apache-2.0)
- [SDK: cm33/connectivity/07_trust_policy.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/07_trust_policy.c) (Apache-2.0)
