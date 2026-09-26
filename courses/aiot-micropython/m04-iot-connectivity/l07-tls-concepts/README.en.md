---
id: aiot-mpy.m04.l07
lang: en
title: {th: 'TLS: ใบรับรอง ห่วงโซ่ความเชื่อถือ และการจับมือ', en: 'TLS: certificates, the chain of trust and the handshake'}
summary: {th: เข้าใจว่า TLS ประกอบจากกุญแจคู่ ลายเซ็น และแฮช อ่านใบรับรอง ห่วงโซ่ความเชื่อถือ การจับมือ และ SNI ได้ แล้วบอกได้ว่า serverTLS บนพอร์ต 8884 ปกป้องอะไรและไม่ปกป้องอะไร, en: 'Understand how TLS is built from key pairs, signatures and hashes, read certificates, the chain of trust, the handshake and SNI, and state what serverTLS on port 8884 protects and what it does not.'}
level: L2
time_min: {concept: 35, lab: 15, check: 5}
hardware: {emulator: true, boards: [eva-kit, devkit]}
prerequisites: [aiot-mpy.m04.l06]
objectives:
  - {th: อธิบายหน้าที่ของการเข้ารหัสด้วยกุญแจคู่ ลายเซ็น และแฮชใน TLS และบอกได้ว่าใบรับรองรับรองอะไร (ชื่อคู่กับกุญแจสาธารณะ ที่ CA เซ็นไว้) และไม่ได้รับรองอะไร, en: 'Explain the roles of key-pair encryption, signatures and hashes in TLS, and state what a certificate vouches for (a name bound to a public key, signed by a CA) and what it does not.'}
  - {th: เรียงการจับมือ TLS 1.2 สี่จังหวะตั้งแต่ TCP จนถึง MQTT CONNECT ได้ถูกลำดับ ชี้ได้ว่า SNI เดินไปก่อนการเข้ารหัส และบอกอาการเมื่อ sni_hostname ไม่ตรงกับชื่อ broker, en: 'Order the four beats of a TLS 1.2 handshake from TCP to MQTT CONNECT, show that SNI travels before encryption starts, and name the symptom of an sni_hostname that does not match the broker.'}
  - {th: อธิบายว่าพอร์ต 8884 ถูกเลือกจาก tls_mode ไม่ใช่คีย์ port และทำไม MQTTs จากบอร์ดเข้า TESAIoT CE ที่ติดตั้งเองไม่ผ่าน, en: 'Explain that port 8884 is chosen by tls_mode rather than the port key, and why MQTTs from the board cannot reach a self-installed TESAIoT CE.'}
  - {th: กรอกตารางเทียบพอร์ต 1883 กับ 8884 ในบันทึกการเรียนจากสิ่งที่คนดักฟังเห็น และตอบได้โดยไม่เปิดสไลด์ว่า serverTLS พิสูจน์ช่องทางและเซิร์ฟเวอร์ แต่ไม่ได้พิสูจน์อุปกรณ์, en: 'Fill a 1883-versus-8884 comparison table in the learning log from what an eavesdropper sees, and state without the slides that serverTLS proves the channel and the server but not the device.'}
develops: [{skill: sec.tls, to: 2}, {skill: sec.fundamentals, to: 2}, {skill: sec.crypto, to: 1}, {skill: proto.tcp-ip, to: 1}]
context: {platform: psoc-edge-e84, lang: micropython, ide: bento-ide}
status: alpha
translation: done
slides: slides.md
source: {repo: 'https://github.com/Advance-Innovation-Centre-AIC/embedded-systems-for-aiot-developer', path: session-11.html (slides 1–18), ref: a80bbe88a34bcb9bb8d991f42f9252b77cdab079}
source_sha256: f7445494109bcfaf5ce8e88e54345003ef276e87148b402046bb194052eca9bb
---

# Lesson 4.7 — TLS: certificates, the chain of trust and the handshake

> Module 4 — IoT Platform Connectivity · Slides: [slides.md](slides.md) · [Module overview](../README.md) · [Course page](../../README.md)

Understand how TLS is built from key pairs, signatures and hashes, read certificates, the chain of trust, the handshake and SNI, and state what serverTLS on port 8884 protects and what it does not.

## Objectives

By the end of this lesson you will be able to:

1. Explain the roles of key-pair encryption, signatures and hashes in TLS, and state what a certificate vouches for (a name bound to a public key, signed by a CA) and what it does not
2. Order the four beats of a TLS 1.2 handshake from TCP to MQTT CONNECT, show that SNI travels before encryption starts, and name the symptom of an sni_hostname that does not match the broker
3. Explain that port 8884 is chosen by tls_mode rather than the port key, and why MQTTs from the board cannot reach a self-installed TESAIoT CE
4. Fill a 1883-versus-8884 comparison table in the learning log from what an eavesdropper sees, and state without the slides that serverTLS proves the channel and the server but not the device

## Before you start

Review lessons 4.4–4.6: data already flows both ways through `mqtt.*` on port 1883, but flows naked. Carry forward: JSON sent flat,
`device_id` no longer than 31 characters, and values must be numbers to chart.
Before finishing this lesson, you must have the device's four identity values: `device_id` · `api_key` · `mqtt_pass` · the broker's hostname.
Add a device to your TESAIoT Platform account, then read these four values from the platform's device management page
([TESAIoT Community Edition](https://github.com/tesaiot/tesaiot-community-edition), self-installed, works with port 1883 in lessons 4.4–4.6, but not with the MQTTs of lessons 4.7–4.9,
because of the root CA matter under Concepts). If learning in a group, your organiser may prepare the identity for you.
Record it in your learning log before touching code in lesson 4.8.

- **Equipment:** an Eva Kit or TESAIoT Dev Kit board with the BENTO MicroPython firmware installed, or the BENTO Emulator in [BENTO IDE](https://ide.tesaiot.dev/) (this lesson has no code to run; the real TLS connection starts in lesson 4.8 and needs a real board with an identity already from the platform)
- **Before this:** [Lesson 4.6 — Hands-on: two-way telemetry](../l06-mqtt-telemetry-lab/README.md)

## See it work first

Look at the slides' first picture, comparing what a sniffing tool sees on the same network. On port 1883, an eavesdropper reads every byte of MQTT CONNECT,
including `username: team03`, the device's password, and the sensor value's JSON. On port 8884, all that is seen is TLS Application Data — unreadable bytes,
the same length, the same timing, but the content is gone. The only thing still visible is the destination hostname. Same board, same network, almost the same code —
the only difference is which module we call.

## Concepts

Port 1883 is not "less secure" — it **has no security at all**, neither of content nor of identity. Unencrypted, everyone on the same network is us.
What 8884 adds is two things at once: encryption, and knowing who you are talking to. The module changes too,
from `mqtt`, which lets you pick the host and port yourself, to `tesaiot`, which is configured differently and cannot choose its own port.

TLS is built from three pieces: **encryption = locking against reading** (locked with a public key, only a private key can open it) · **signing = proving who wrote it**
(signed with a private key, anyone can verify with the public key) · **hashing = catching a change** (change one character and the whole value changes).
A server's certificate has fields Subject, Public Key, Validity, and Issuer + Signature. What gives it value is the CA's signature at the end.
A certificate means "someone you already trust confirms this key belongs to this name" — no more than that. It does not say the owner is good,
and it is public data that can be copied. The chain runs from a leaf, signed by an intermediate, up to a root, which signs itself. The root is where we
"chose to trust" in advance. If a box in the middle can install its own CA on your machine, it can issue a certificate for the same name — the list of trusted CAs matters just as much as encryption itself.

The handshake has four beats: **one**, TCP connects the circuit (not encrypted yet) · **two**, `ClientHello` says what it supports and attaches the destination hostname (SNI)
· **three**, the server presents a certificate, the board checks the signature up to a root it has, then exchanges this session's secret key · **four**, from `Finished` onward,
every byte is encrypted, and then MQTT CONNECT walks in inside. Our firmware negotiates TLS 1.2, which takes two round trips
(TLS 1.3 takes only one); on a board with a slow CPU, this takes several seconds. Lesson 4.8's code must therefore wait in a loop. SNI is the name that travels openly;
the server uses it to pick which certificate to present, so `sni_hostname` must exactly match the broker's name. Set it wrong and the symptom is **failing to connect with no message at all**.

On the board, TLS runs on CM33_NS, the same core running Python, while CM55, which draws the screen, never touches the network at all. The handshake consumes the largest single chunk of memory,
so `tesaiot.connect()` should be called at the start of the script, while memory is still free. The platform's root CA is compiled into the firmware,
with no API to change it at runtime. The port is a result of `tls_mode`, not a value you pass in: `server_tls` → 8884 (this set of lessons' path)
and `mutual_tls` → 8883 (needs the device's own certificate). Setting the `port` key does not error, but it only changes the label displayed.
MQTTs from the board therefore cannot reach a self-installed CE, because CE's install script randomises a new root CA every time — the board has no way of knowing it.
If you try it and it does not connect, do not debug the code — go back to using the TESAIoT platform's own host, which comes with the device's identity.

serverTLS can only prove one side: data stays encrypted the whole way, and we know the server is real because it presents a certificate signed by a CA with a name matching SNI —
but the server **does not know which device is speaking**. It only knows someone knows the correct `device_id` and `mqtt_pass`. This kind of secret can be copied.
Proving the device needs mTLS, with a private key that really lives inside the device. Before starting any code, every board still needs its own `device_id`,
because boards leave the factory with identical default values — if several boards reused the same one, the broker would keep kicking the old one off in a loop, even though every board's code is correct.

## Worked example

The slides for this lesson also refer to a file that lives in another lesson:

- [m04-iot-connectivity/l08-tesaiot-module/examples/06_secure_publish_loop.py](../l08-tesaiot-module/examples/06_secure_publish_loop.py) — send to the platform over TLS and show the evidence on screen

## Check your understanding

The same questions are in [quiz.yaml](quiz.yaml) for automatic marking.

1. What exactly does a broker's CA-signed X.509 certificate vouch for? *(choose one · objective 1)*
   - A) The public key in this certificate really belongs to this hostname, confirmed by a signature from a CA we already trust
   - B) The server's owner is a good person and keeps our data safely
   - C) The certificate is secret; if anyone copies it, they can instantly impersonate the server
   - D) Data passed through this server is always correct

   <details><summary>Solution</summary>

   **A** — A certificate only proves "a name bound to a key" and has value because of the CA's signature at the end. The certificate itself is public data that can be copied, and it says nothing about whether the owner is good or keeps data well.

   </details>

2. Order the TLS 1.2 handshake beats between the board and the broker, from the very start to when MQTT data begins to flow. *(order · objective 2)*
   - A) ClientHello says what it supports and attaches the destination hostname (SNI)
   - B) From Finished onward, every byte is encrypted, and MQTT CONNECT walks in inside
   - C) TCP connects the circuit, nothing encrypted yet
   - D) The server presents a certificate; the board checks the signature up to a root it has, then exchanges this session's secret key

   <details><summary>Solution</summary>

   **C → A → D → B** — TCP must come first, then ClientHello travels with SNI, still unencrypted. The server presents the certificate matching that name; the board checks up to a root, then exchanges the key. After Finished, every byte is encrypted. MQTT knows nothing about TLS — it is simply placed inside a pipe that has already been built.

   </details>

3. A team sets `sni_hostname` one character off from the broker's real name. What symptom would they see? *(choose one · objective 2)*
   - A) Fails to connect with no message at all
   - B) An error saying the hostname is wrong, along with the correct one
   - C) Connects, but data travels unencrypted
   - D) The board switches to port 8883 on its own

   <details><summary>Solution</summary>

   **A** — SNI is the name the server uses to pick which certificate to present. A wrong name gets the wrong certificate, fails verification, and fails silently — not an error that says the name is wrong.

   </details>

4. Which statements about the port and root CA of the `tesaiot` path are correct? Choose every correct one. *(choose all that apply · objective 3)*
   - A) The port actually connected to is chosen by `tls_mode`, with `server_tls` giving 8884
   - B) Setting the `port` key to 1883 makes the board connect on port 1883, unencrypted
   - C) MQTTs cannot reach a self-installed CE, because CE randomises a new root CA on every install, but the board only knows the root compiled into the firmware
   - D) The root CA on the board can be changed by calling an API at runtime

   <details><summary>Solution</summary>

   **A, C** — The port is a result of `tls_mode`; the `port` key only changes the displayed label. The root CA is compiled into the firmware, with no API to change it at runtime; using CE would require rebuilding the firmware with that CE's own CA baked in.

   </details>

5. What can the serverTLS used in this set of lessons actually do? Choose every correct one. *(choose all that apply · objective 4)*
   - A) Encrypt data the whole way, so no one in the middle can read it or alter it undetected
   - B) Prove the server is real, because it presents a certificate signed by a CA with a name matching SNI
   - C) Prove which device sent the data, even if someone has copied the `mqtt_pass`
   - D) Hide the destination hostname from an eavesdropper

   <details><summary>Solution</summary>

   **A, B** — serverTLS proves the channel and the server, not the device. Device identity comes from a password that can be copied, and SNI still travels openly, so an eavesdropper sees who we are talking to, just not what is said.

   </details>

## Lab

**A paper lab** (about 15 minutes). Record every item in your learning log.

- [ ] Record the device's four identity values from the platform's device management page (`device_id` · `api_key` · `mqtt_pass` · the broker's hostname), and count that `device_id` is no longer than 31 characters
- [ ] Open an HTTPS website's certificate in a browser; record the Subject, Issuer, Validity and the root → intermediate → leaf chain you see
- [ ] Draw the four handshake beats, marking which beat is still unencrypted, when SNI travels, and when MQTT CONNECT enters
- [ ] Fill a table comparing 1883 and 8884 (encryption · the broker's identity · the device's identity · destination · module) from the picture of what an eavesdropper sees — do not copy the slides' table
- [ ] Write one sentence in your own words: what does serverTLS prove, and what does it not prove

## Going further

Lesson 4.8 opens the `tesaiot` module function by function: set identity with `config_set()`, command `connect()`, then loop waiting for `is_connected()` before `publish()`.
If you want to understand this faster, watch the clips in the slides: PKI Bootcamp (the certificate chain, about 4 minutes) and SaKKo sama's Thai-language clip on SSL/TLS/HTTPS.

Next lesson: [Lesson 4.8 — The tesaiot module: MQTTs to the platform](../l08-tesaiot-module/README.md)

## Reflect

- If a box in the middle had its own CA installed on our machine, how would we know, and why does the list of trusted CAs matter just as much as encryption?
- If someone got hold of our device's `mqtt_pass`, what could serverTLS help with, and what could it not help with?
- A value you can set does not mean that value has an effect. Have you met another system with a key like this `port` one?
