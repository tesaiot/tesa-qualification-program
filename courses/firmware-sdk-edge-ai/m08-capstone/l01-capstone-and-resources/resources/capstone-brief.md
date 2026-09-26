# Capstone brief — Course 1

**Course 1 · Module 8**

กรอกแล้วแนบกับงานส่ง — [Lab](../../l02-lab/README.md) · [Lesson](../README.md) · [TOC](../../../README.md)

---

## Project title

…

## Team / author

…

## Architecture — tasks

| Task name | Priority | Period / trigger | Responsibility | Queue / lock |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |

## Sensors and local I/O

| Item | Choice |
|---|---|
| Primary sensor API | e.g. `sensor_sht40_read` / `sensor_bmi270_read` |
| Filter / window | |
| LED / UART indication | |

## Connectivity choice

- [ ] MQTT (M06)  
- [ ] BLE (M07)  
- [ ] Both (bonus)

### MQTT (if used)

| Direction | Topic | Payload example |
|---|---|---|
| Publish telemetry | `bitstream/<MAC>/sensors` | |
| Publish event (optional) | | |
| Subscribe command | `bitstream/<MAC>/actuators` | |

Broker host:port (no password here):  
tls (0/1):  

### BLE (if used)

| Item | Value |
|---|---|
| Adv name / filter | e.g. `TESAIoT-*` |
| Host tool | ble-flet / nRF Connect / other |
| How you prove link | status / notify / command |

## Three demo scenarios

1. Normal:  
2. Stimulus:  
3. Host command:  

## Live host evidence (optional)

| Tool | What you showed |
|---|---|
| Bitstream Studio | |
| Hackathon web-app (ex…) | |
| Hackathon ble-flet | |
| MQTTX / nRF Connect / other | |

## Notes for Digital Twin (Course 2+)

What you would send next (`to_twin` / topics / fields):  

## Secrets check

- [ ] No Wi‑Fi password in submitted public files  
- [ ] No broker password in submitted public files  

[Lab](../../l02-lab/README.md) · [Course package](course-package.md)
