# BLE connectivity cheatsheet — Course 1 M07

**Course 1 · Module 7**

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [TOC](../../../README.md)

---

## BLE vs MQTT (pick for Capstone)

| Need | Prefer |
|---|---|
| Phone / desktop nearby, no Wi‑Fi | **BLE** |
| Cloud / LAN broker / multi-subscriber | **MQTT** |
| Both local demo + cloud | Both (M08 bonus) |

---

## CM55 API (TESA)

| API | Role |
|---|---|
| `cm55_trigger_ble_periph_status_get` | Request status (async) |
| `cm55_ble_periph_status_get_sync` | Request + wait → `ipc_ble_periph_status_t` |
| `cm55_get_ble_periph_status` | Read last cached status |
| `cm55_trigger_ble_periph_adv_ctrl` | ADV action async |
| `cm55_ble_periph_adv_ctrl_sync` | ADV action + wait result |
| `cm55_ble_request_scan_all` / `_name` / `_addr` | Start scan (observer) |
| `cm55_ble_ipc_set_event_handler` | Receive `IPC_EVT_BLE_*` |

Headers (names only): `cm55_ipc_app.h`, `ipc_ble_periph_types.h`

---

## ADV actions

| `action` | Meaning |
|---|---|
| `0` | Stop advertising |
| `1` | Start advertising |
| `2` | Restart advertising |

```c
uint8_t result = 0xFF;
(void)cm55_ble_periph_adv_ctrl_sync(1U, &result, 5000U);
```

---

## Status fields (quick)

| Field | Watch for |
|---|---|
| `profile_ble_active` | BLE profile on |
| `stack_ready` | Stack up |
| `connection_id` | Non-zero ⇒ linked |
| `tx_notify_enabled` | Host enabled notify |
| `last_error` | Non-zero ⇒ inspect |

```c
ipc_ble_periph_status_t st;
(void)cm55_ble_periph_status_get_sync(&st, 5000U);
```

---

## Host checklist

1. Firmware BLE profile ON + reboot  
2. One Central only (`ble-flet` **or** nRF Connect)  
3. Hunt name prefix `TESAIoT-`  
4. If invisible after ~60 s idle ADV: reboot board / check ADV policy  

Pack: [TESAIoT_Hackathon](https://github.com/drsanti/TESAIoT_Hackathon) → `ble-flet/`

---

## Architecture reminder

```text
CM55 app  --IPC-->  CM33 BLE stack (AIROC)  --GATT-->  Phone/PC
```

---

## Further reading

- [Bluetooth LE overview](https://www.bluetooth.com/learn-about-bluetooth/tech-overview/)  
- [Infineon Find Me CE](https://github.com/Infineon/mtb-example-psoc-edge-btstack-findme)  
- [Developer Hub](https://dev.tesaiot.dev/)  

[Lesson](../README.md) · [Lab](../../l02-lab/README.md) · [M08 Capstone](../../../m08-capstone/l01-capstone-and-resources/README.md)
