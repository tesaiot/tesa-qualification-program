# Cheatsheet — MQTT / MQTTs (M06)

**Course 1 · Module 6**

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [← Table of Contents](../../../README.md)

---

## Concepts

| Term | One-liner |
|---|---|
| Broker | ตัวกลาง pub/sub |
| Topic | ช่องชื่อแบบลำดับชั้น |
| QoS | ระดับรับประกันการส่ง (0/1/2 ในสเปก) |
| Retain | เก็บข้อความล่าสุดของ topic |
| MQTTs | MQTT + TLS (พอร์ตมัก 8883) |

---

## Ownership

| Core | Role |
|---|---|
| CM55 | `cm55_trigger_mqtt_*`, JSON encode |
| CM33 | Wi‑Fi + `cy_mqtt_*` session |

Wi‑Fi CONNECTED **before** MQTT.

---

## CM55 commands

```c
cm55_trigger_connect(ssid, pass, 0);
cm55_get_wifi_status(&st);

cm55_trigger_mqtt_policy_set(flags);
cm55_trigger_mqtt_connect();
cm55_get_mqtt_status(&mqtt);   /* state 2 = CONNECTED */
cm55_trigger_mqtt_disconnect();
```

Policy ideas: `AUTO_CONNECT` | `TELEMETRY_PUBLISH` | `MQTT_ENABLED` (factory often `0x07`)

---

## Config placeholders

```c
cfg.broker_host = "YOUR_BROKER_HOST";
cfg.port = 1883;   /* or 8883 */
cfg.tls  = 0;      /* 1 for MQTTs */
cfg.username / cfg.password = "YOUR_*";
cfg.root_ca_len = 0; /* may use embedded CA when tls=1 */
```

Topics: `bitstream/<MAC12>/sensors|actuators|status`  
Helper: `cm33_mqtt_format_mac_topic(...)`

---

## Payload

```c
bs_mqtt_telem_encode_json_readable(...);
/* primary path = JSON string; no CBOR path in current MQTT stack */
```

Telemetry publish behavior in current SDK: **QoS0**, **retain false** (teach spec vs implementation)

---

## Security checklist

- [ ] Prefer TLS for anything beyond a lab LAN  
- [ ] Do not commit Wi‑Fi / broker passwords  
- [ ] Know whether broker needs user/pass  
- [ ] Mutual TLS client cert: **not** in standard config v3  

---

## Host tools

| Tool | Link |
|---|---|
| Examples | [dev.tesaiot.dev](https://dev.tesaiot.dev/) |
| Hackathon MQTT | [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) `ex09`–`ex15` |
| Studio | [Bitstream Studio](https://marketplace.visualstudio.com/items?itemName=TERNIONDEV.bitstream-studio) |
| Concepts | [MQTT Essentials](https://www.hivemq.com/mqtt-essentials/) |

---

## Lab log

| Item | Your value |
|---|---|
| Wi‑Fi SSID | |
| Broker host:port | |
| tls (0/1) | |
| Client id / MAC topic | |
| Publish evidence | |
| Subscribe evidence | |

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [← Table of Contents](../../../README.md)
