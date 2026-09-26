---
id: sec-iot.m03.l02
lang: en
title: {th: MQTTs ขึ้น TESAIoT Platform, en: MQTTs to the TESAIoT Platform}
summary: {th: ตามเส้นทางตั้งแต่ไฟล์ตั้งค่า งาน MQTT จนถึง broker และส่งข้อมูลขึ้นแพลตฟอร์มผ่านการเชื่อมต่อที่เข้ารหัส, en: 'Follow the path from config file to MQTT task to broker, and publish to the platform over an encrypted link.'}
level: L3
time_min: {concept: 20, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [devkit]
prerequisites: [sec-iot.m03.l01]
objectives:
- {th: อธิบายเส้นทางข้อมูลจากไฟล์ตั้งค่า งาน MQTT จนถึง broker ของ TESAIoT ได้ครบทุกขั้น, en: Explain the data path from config file through the MQTT task to the TESAIoT broker.}
- {th: เชื่อมต่อ WiFi โดยเอาข้อมูลรับรองจากที่เก็บ แทนการฝังในโค้ด, en: Join WiFi with credentials from a store rather than hard-coded in source.}
- {th: เปรียบเทียบ MQTTs กับ HTTPS สำหรับอุปกรณ์หนึ่งชิ้น และเลือกให้เหมาะกับงาน, en: Compare MQTTs and HTTPS for a device and choose for the job.}
develops:
- {skill: sec.tls, to: 3}
- {skill: iot.cloud-platform, to: 3}
- {skill: proto.mqtt, to: 3}
context: {platform: psoc-edge-e84, lang: c, secure_element: optiga-trust-m, sdk: tesaiot-pse84-devkit-sdk}
status: alpha
translation: done
slides: slides.md
source:
- {repo: 'https://github.com/tesaiot/tesaiot-pse84-devkit-sdk', path: bento-firmware-template-mtb-only, ref: ef72c1b658178eee8c38b1e47d28b006f80a59b5, license: Apache-2.0}
- {repo: 'https://github.com/tesaiot/developer-hub', path: examples/embedded-devices/entry/device-servertls, ref: d2ed42c4a31232f553b6b8cef9ee7373db348c21, license: Apache-2.0}
source_sha256: 10bd1f063b42e158f7e01c51cfac95a8a612abfa0f1a6065dc8b22082deb3001
---

# Lesson 3.2: MQTTs to the TESAIoT Platform

> Module 3 · mTLS to the TESAIoT Platform · [Module overview](../README.md) · [Course home](../../README.md)

The last lesson looked at the secure channel. This one looks at everything that travels inside it, from the config file on the board, through the MQTT task, to the broker,
joining WiFi with not a single password in the source code, and deciding when to use HTTPS instead of MQTTs.

## Objectives

By the end of this lesson you will:

1. Explain the full data path from the config file, through the MQTT task, to the TESAIoT broker
2. Join WiFi using credentials from storage, rather than hard-coded in source
3. Compare MQTTs and HTTPS for one device and choose the one that fits the job

## Before you start

- **Already covered:** [Lesson 3.1: TLS and mTLS](../l01-tls-and-mtls/README.md)
- **On the platform:** one device already registered on the TESAIoT Platform, and that device's **Server-TLS bundle for MQTT.**
  The [device-servertls](https://github.com/tesaiot/developer-hub/blob/d2ed42c4a31232f553b6b8cef9ee7373db348c21/examples/embedded-devices/entry/device-servertls/README.md) example's README says the bundle contains `ca-chain.pem`, `endpoints.json` and MQTT credential files.
  You must select `include_password` at download time to get the password. **Never push these files to any repository.**
- **On your computer:** `mosquitto_sub` and `mosquitto_pub` (the mosquitto-clients package)
- **Read alongside:** [Lesson 5.1 of TESAIoT Firmware Stack: Telemetry to the TESAIoT Platform with Server-TLS](../../../tesaiot-firmware-stack/m05-connect-to-platform/l01-server-tls/README.md)

## See it work first

Here is what the `/.tesaiot_config` file looks like when the board reads it at boot. Its format is `key=value`, one per line, and the key names match the parser in
[tesaiot_config_store.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_config/tesaiot_config_store.c). Values in angle brackets are fields you fill in yourself.

```ini
tls_mode=server_tls
broker=mqtt.tesaiot.dev
port=1883
device_id=<device_id from the platform>
mqtt_pass=<MQTT password from the bundle>
keepalive=60
wifi_ssid=<WiFi name>
wifi_pass=<WiFi password>
wifi_security=WPA2
```

**Guess first:** which port will the board actually use to connect to the broker — 1883, per the `port=` line, or a different one? And where do the two passwords in this file end up appearing during the connection?

## Concepts

### 1. The path from config file to broker

Chapter [C3 of the SDK docs](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c3__cloud__mqtt.html) walks this whole path. The diagram below summarises it as steps.

```text
/.tesaiot_config  (LittleFS, key=value)
   │  tesaiot_config_init() at boot  (mtb-only: called from main())
   ▼
tesaiot_mqtt_connect()   ← the Connect button on the TESAIoT screen (IPC_CMD_TESAIOT_CONNECT)
   │                       ← tesaiot.connect() on the mtb-mpy variant
   │                       ← the HSM's enrolment work happens before touching the chip (lesson 5.1)
   ▼
mqtt_request_start()     creates the "MQTT" task the first time it is asked for, not at boot
   ▼
mqtt_client_task         waits for WiFi with app_wifi_is_ready(), up to 60 seconds, then waits for a start signal
   ▼
mqtt_client_config_init() picks the host, the port from tls_mode, SNI, client id, username/password, root CA
   │                       (for mTLS, followed by mqtt_mtls_setup_optiga() from lesson 3.1)
   ▼
cy_mqtt_connect()        retries up to max_retries ── TLS 1.2 ──▶ mqtt.tesaiot.dev
   ├─ publisher_task  ◀── queue ◀── tesaiot_mqtt_publish()   defaults to device/<device_id>/telemetry
   └─ subscriber      device/<device_id>/commands/#  picks a handler from the end of the topic name, on the MQTT event thread
```

`tls_mode` decides several things at once, per [mqtt_client_config.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_mqtt/mqtt_client_config.c).

| `tls_mode` | Port | Client id | Username | Password |
|---|---|---|---|---|
| `mtls` (0), `mtls_sw` (1) | 8883 | `factory_uid` (falls back to `device_id` if empty) | `mtls_device_id` | Empty — authenticates with the certificate |
| `server_tls` (2, the default) | 8884 | `device_id` | `device_id` | `mqtt_pass` |

So the answer to the first guess is **8884.** The `port=` line is stored but never used by MQTT at all — chapter C3 flags this as pitfall 1.
If your broker listens on a different port, you must change the switch in the code; there is no way to fix it from the config file.
As for the MQTT password, it appears inside MQTT CONNECT, which by then runs **inside** TLS, and the console prints only its `PassLen`.

Other pitfalls that C3 and the SDK's CSR contract record, which you will use in the lab:

- **The publisher's queue does not wait.** `tesaiot_mqtt_publish()` queues with a zero-second wait; when the queue is full the message is silently dropped, so publishing rapidly loses data.
- **The subscriber's handler runs on MQTT's event thread.** Anything that would block, or that touches the chip, must be handed off to a queue for your own task.
- **Someone must tend the session.** The broker drops a session after 1.5 times the keepalive (90 seconds when keepalive is 60) if no PINGREQ arrives.
  The CSR contract section 5.3 recounts one case where the cause was the Subscriber task's stack overflowing right after CONNACK — look at the device's own log first; the broker can only tell you that nothing arrived.
- **The topic always uses `device_id`.** In mTLS mode the client id is the Trust M's UID, but the topic must still be `device/<device_id>/...`. If you use the UID in the topic instead, the ACL will refuse it while the connection itself still looks fine, so the message just seems to vanish.

### 2. WiFi from storage, not from a `#define`

ETSI EN 303 645 provision 5.4-3 forbids hard-coding critical security parameters in source code.
The [10_wifi_join.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/10_wifi_join.c) example follows this strictly.
It looks for credentials in order: the credential store on LittleFS (mtb-mpy variant only), then `wifi_ssid`, `wifi_pass`, `wifi_security` in `tesaiot_config_store` (both variants).
If it finds neither, it **refuses to proceed**, and tells you how to save credentials instead. The comment in the file states that a credential compiled into an example is a credential that has leaked into a public code repository.

Details worth copying into your own work:

- Never print the passphrase at all — print only its length, because the console is often a screen other people can see
- Wipe the password buffer through a `volatile` pointer, so the compiler cannot optimise the write away just because it thinks no one reads it afterwards
- Always ask `app_wifi_is_ready()` first — calling `cy_wcm_is_connected_to_ap()` before WCM has started causes a hard fault on the board
- This example is **disabled by default**, because it turns on the radio and joins someone's real network — you must build it yourself with `EXAMPLE_WIFI_JOIN=1`

And to be complete: the config file lives on LittleFS, in the board's own memory — better than living in source, since it does not leak with the repository or a distributed image file.
But the SDK never claims this file is encrypted; assume that anyone who can read the board's flash can read it too. This is one reason mTLS, whose key lives inside the chip, beats an MQTT password sitting in a file.

### 3. MQTTs or HTTPS

Both run over TLS. They differ in conversation shape. The ports and authentication in the table come from the device-servertls and device-mtls READMEs on the Developer Hub.

| | MQTTs | HTTPS |
|---|---|---|
| Shape | A session stays open; publish and subscribe | Request and response, one at a time |
| Commands from the platform | Arrive on their own, via the `commands/#` subscription | The device must poll periodically, e.g. the OTA job endpoint in `c_ota_client` |
| Port and authentication | 8884 username/password · 8883 mTLS | 443, header `X-API-KEY` · 9444 mTLS |
| Cost on the board | A task alive for the whole keepalive period, and about 16 KB of stack for the handshake, per the `tesaiot_mqtt` README | Opens and closes per call; the HTTPS module in `03_https_session.c` holds one connection at a time |
| Fits | Continuous telemetry, and needing to receive commands | Occasional sends, large file downloads, calling a REST API |

A caution from [03_https_session.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/03_https_session.c):
its comment says the HTTPS path sets `root_ca_verify_mode = CY_AWS_ROOTCA_VERIFY_NONE` — encrypted, but it **does not verify the server's certificate.**
There is a separate plaintext entry point, a different function (`claw_http_connect_insecure`), meant only for public endpoints that carry no keys.
The author deliberately chose the plaintext mode by function name, not by port number, so the other side cannot just answer on port 80 and get an API key sent unencrypted.
If you want to send device data over HTTPS, pin the root CA first.

## Worked example

Taken from [10_wifi_join.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/10_wifi_join.c), lines 176–190 and 237–242
(TESAIoT PSE84 Dev Kit SDK, © Thai Embedded Systems Association, Apache-2.0)

```c
    {
        /* ~660 bytes. Static for the same reason as the buffers above. */
        static tesaiot_config_t cfg;
        tesaiot_config_get(&cfg);
        if (cfg.wifi_ssid[0] != '\0') {
            (void)snprintf(s_ssid, sizeof(s_ssid), "%s", cfg.wifi_ssid);
            (void)snprintf(s_pass, sizeof(s_pass), "%s", cfg.wifi_pass);
            (void)snprintf(s_sec,  sizeof(s_sec),  "%s", cfg.wifi_security);
            wipe(cfg.wifi_pass, sizeof(cfg.wifi_pass));
            return "tesaiot_config_store";
        }
        wipe(cfg.wifi_pass, sizeof(cfg.wifi_pass));
    }

    return NULL;
```

```c
        /* SSID and security only. The passphrase is never printed: the console
         * is not the radio, and this console is often a shared screen. */
        printf("  credentials from %s\r\n", from);
        printf("    ssid=\"%s\" security=\"%s\" passphrase=%u byte(s), not shown\r\n",
               s_ssid, s_sec[0] ? s_sec : "(default: WPA2)",
               (unsigned)strlen(s_pass));
```

Notice three things: the copy of the password in `cfg` is wiped immediately after copying, on **both** exit paths; the function returns the name of the store it used, not the password's value;
and the printed message gives everything you need to debug (SSID, security type, password length) without ever including the password itself.

Examples on the Developer Hub that do the same path on a computer:

- [TESA IoT Device → Platform (Server-TLS) — HTTPS or MQTTS via Mongoose](https://dev.tesaiot.dev/?example=developer-hub--device-servertls&q=device-servertls)
- [TESA IoT Device → Platform (mTLS) — HTTPS or MQTTS via Mongoose](https://dev.tesaiot.dev/?example=developer-hub--device-mtls&q=device-mtls)
- [PSoC Edge E84 + OPTIGA Trust M: TESAIoT MQTT Client](https://dev.tesaiot.dev/?example=developer-hub--pse84_tesaiot_client&q=pse84_tesaiot_client), the on-board reference project (Cypress EULA, link only) — the SDK's own `tesaiot_mqtt.h` file states the SDK's module was developed onward from this project

## Practice

Write a one-line call that publishes the JSON `{"t":25.0}` to the device's default telemetry topic, from your own task on CM33_NS.
Per chapter C3, the function's signature is `bool tesaiot_mqtt_publish(const char *topic, const char *payload, size_t payload_len);`.

```c
static const char payload[] = "{\"t\":25.0}";

if (!tesaiot_mqtt_publish(____, payload, ____)) {
    /* what can you conclude at this point? */
}
```

<details><summary>Solution</summary>

```c
if (!tesaiot_mqtt_publish(NULL, payload, sizeof(payload) - 1)) {
```

`NULL` (or an empty string) has the function build the topic `device/<device_id>/telemetry` itself. The length excludes the string's terminator.
A `false` result can mean: not connected yet, the publisher's queue is not ready, there is no `device_id`, memory could not be allocated, or the queue is full.
A `true` result means only that the message **has been queued** — not that it has reached the broker yet. Proof that it really arrived must come from the receiving side.

</details>

## Check your understanding

The questions below are part of the full set in [quiz.yaml](quiz.yaml), which the automated grader uses.

1. The config file has `tls_mode=server_tls` and `port=1883`. Which port will the board connect to the broker on? *(objective 1)*
   - a) 1883
   - b) 8883
   - c) 8884
   - d) 443

   <details><summary>Solution</summary>

   **c.** MQTT's port comes from `tls_mode` in `mqtt_client_config.c`; the `port=` line is never used.

   </details>

2. Why does the `10_wifi_join.c` example refuse to proceed when it finds no credentials in storage, instead of falling back to an SSID hard-coded in the source? *(objective 2)*
   - a) Because a fallback SSID uses too much memory
   - b) Because a credential compiled into the code is a credential that leaks with the public code repository, which conflicts with ETSI provision 5.4-3
   - c) Because WiFi does not support a fallback SSID
   - d) Because the compiler would not allow it

   <details><summary>Solution</summary>

   **b.** The example tells you how to save credentials instead, and there is no fourth option.

   </details>

3. A device measures temperature every 10 seconds, and must receive a fan on/off command from the platform within a few seconds. What should it use? *(objective 3)*
   - a) HTTPS, polling the platform every hour
   - b) MQTTs, publishing telemetry and subscribing to `commands/#`
   - c) Unencrypted HTTP, because it is faster
   - d) No connection needed

   <details><summary>Solution</summary>

   **b.** An open session lets commands arrive on their own, without polling. HTTPS suits occasional sends or large file downloads better.

   </details>

4. `tesaiot_mqtt_publish()` returns `true`. Which conclusion is correct? *(objective 1)*
   - a) The message has definitely reached the broker
   - b) The message has been queued by the publisher; proving it arrived requires looking at the receiving side
   - c) The platform has already stored the data
   - d) The broker's certificate has already been verified

   <details><summary>Solution</summary>

   **b.** Chapter C3 also warns that the `[Publisher] Published to ...` log line is disabled by default — never wait on that line as proof.

   </details>

## Lab

**Make a real connection, then prove it with evidence from the receiving side.** Write down every result in your learning log, and never write a real password into it.

- [ ] **1. WiFi from storage.** Put `wifi_ssid`, `wifi_pass` and `wifi_security` into the board's config file. On mtb-only, chapter C3 has you write them from the TESAIoT settings screen, or ship the file with the image's filesystem.
  On mtb-mpy you can write them from the REPL. Then build the example:
  ```bash
  make build ENABLE_PAGE_EXAMPLES=1 SDK_EXAMPLE_CM33=cm33/connectivity/10_wifi_join DEFINES+=EXAMPLE_WIFI_JOIN=1
  make program BENTO_WORKSPACE="$(cd .. && pwd)"
  ```
  Record the `credentials from ...` and `passphrase=N byte(s), not shown` lines. Then search your whole project folder with `grep -r "<your WiFi name>" .` — it must find nothing.
- [ ] **2. Configure MQTT.** Fill in `tls_mode=server_tls`, `broker=mqtt.tesaiot.dev`, `device_id` and `mqtt_pass` from the bundle. Leave `port=1883` in place too, to test your guess.
- [ ] **3. Connect.** Tap Connect on the TESAIoT screen, then record the UART lines in order, comparing them against the list in chapter C3, Step 3.
  In the `[MQTT-Config] Mode=..., Broker=...:<port>` line, what is the port? Does it match your guess?
- [ ] **4. Prove the data arrived.** Subscribe from your computer **first**, then have the board publish (use your Practice answer in your own task, or `tesaiot.publish()` on mtb-mpy).
  ```bash
  mosquitto_sub -h mqtt.tesaiot.dev -p 8884 --cafile ca-chain.pem \
    -u '<device_id>' -P '<MQTT password>' -t 'device/<device_id>/telemetry' -v
  ```
  If the broker will not let this account subscribe, that is the ACL doing its job — the SDK's CSR contract section 5.1 states that a device's own account may only subscribe to `commands`, `config` and `firmware`.
  Use a test account, or whatever check your platform administrator provides, and note where your evidence came from.
- [ ] **5. Someone must tend the session.** Leave the board idle for over 90 seconds, then publish again. Does it succeed? If not, look at the device's own log first (has a task died, or the stack overflowed?) before suspecting the broker.
- [ ] **6. Choose a channel.** Write a three-row table for your own project (for example: sending a reading every minute · downloading a 2 MB firmware image · receiving an emergency command). For each row, pick MQTTs or HTTPS, with one line of reasoning.
- [ ] **7. Update the threat model** from lesson 1.1, in the rows about WiFi, the MQTT password and the session, with what you saw in this lab.

## Going further

Our device now connects securely. The next question is whether the firmware actually running is the one we meant to ship.
Module 4 looks at the chain of trust from boot onward, and at updates that resist rollback.

Next lesson: [Lesson 4.1: Secure boot and the chain of trust](../../m04-secure-boot-and-update/l01-secure-boot/README.md)

## Reflect

- In your own work, is there a setting that is stored but never used, the way `port=` is here — and who would that mislead?
- If a message is lost in transit, how would your system know, and from which side?
- A password kept in a config file on the board is how much safer than one in source code, and who is it still at risk from?

## References

- [C3 — TESAIoT cloud: config file → MQTT task → broker (SDK docs built from commit ef72c1b)](https://tesaiot.github.io/tesaiot-pse84-devkit-sdk/sdk/mtb-only/group__c3__cloud__mqtt.html)
- [SDK: the tesaiot_mqtt module](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_mqtt/README.md)
- [SDK: tesaiot_mqtt/mqtt_client_config.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_mqtt/mqtt_client_config.c) (linked, not copied)
- [SDK: tesaiot_config/tesaiot_config_store.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/common/modules/tesaiot_config/tesaiot_config_store.c)
- [SDK: cm33/connectivity/10_wifi_join.c (credentials from storage, not a #define)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/10_wifi_join.c)
- [SDK: cm33/connectivity/03_https_session.c](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/proj_cm33_ns/examples/connectivity/03_https_session.c)
- [SDK: CSR_SUBMISSION_CONTRACT.md (ACL, keepalive, topics)](https://github.com/tesaiot/tesaiot-pse84-devkit-sdk/blob/ef72c1b658178eee8c38b1e47d28b006f80a59b5/bento-firmware-template-mtb-only/bento_libs/claw/kit-pse84-ai/modules/tesaiot/docs/CSR_SUBMISSION_CONTRACT.md)
- [TESAIoT Community Edition](https://github.com/tesaiot/tesaiot-community-edition)
- Examples on the Developer Hub: [device-servertls](https://dev.tesaiot.dev/?example=developer-hub--device-servertls&q=device-servertls) · [device-mtls](https://dev.tesaiot.dev/?example=developer-hub--device-mtls&q=device-mtls) · [pse84_tesaiot_client](https://dev.tesaiot.dev/?example=developer-hub--pse84_tesaiot_client&q=pse84_tesaiot_client) (Cypress EULA, link only)
