# Module 2 — From Screen to Hardware

> UI-to-Hardware Interfacing · [Course page](../README.md)

Drive LEDs and read a button with gpio, build a touch-screen control panel that drives real lights, then read a knob and CapSense with filtering.

## Module objectives

Write MicroPython that controls real hardware and can explain what happens at the electrical pin: a chasing light pattern, a debounced button, a touch control panel whose on-screen state matches the real lights, and a knob gauge and touch strip that show a raw value against a filtered one.

## Lessons

| Lesson | Topic | Time (min) | Slides |
|---|---|---|---|
| [2.1](l01-gpio-leds-buttons/README.md) | The gpio module: LEDs, a button and a board that describes itself | 50 | [slides.md](l01-gpio-leds-buttons/slides.md) |
| [2.2](l02-active-low-debounce/README.md) | Behind the LED and the button: active-low, debouncing, and a loop that never stops | 55 | [slides.md](l02-active-low-debounce/slides.md) |
| [2.3](l03-led-button-lab/README.md) | Hands-on: a chasing light and a button, then publish to the broker | 75 | [slides.md](l03-led-button-lab/slides.md) |
| [2.4](l04-touch-widgets/README.md) | The touch screen and your first widget | 50 | [slides.md](l04-touch-widgets/slides.md) |
| [2.5](l05-event-loop/README.md) | The event loop: touch the screen and a real light turns on | 70 | [slides.md](l05-event-loop/slides.md) |
| [2.6](l06-touch-panel-lab/README.md) | Hands-on: our own touch control panel, and the next widget | 65 | [slides.md](l06-touch-panel-lab/slides.md) |
| [2.7](l07-adc-capsense/README.md) | Analogue and touch: the ADC knob and CapSense | 65 | [slides.md](l07-adc-capsense/slides.md) |
| [2.8](l08-filters/README.md) | Filtering a signal: EMA and Median, then walking through a gauge | 65 | [slides.md](l08-filters/slides.md) |
| [2.9](l09-pot-capsense-lab/README.md) | Hands-on: a knob gauge and a touch strip | 70 | [slides.md](l09-pot-capsense-lab/slides.md) |

The lessons in this module come in sets of three: concept → code walk-through → hands-on (the third lesson of each set has practice files and solutions).

## Module checkpoint

You pass this module when you can do every item below (the details are in the **Lab** section of the hands-on lessons):

- [ ] A chasing light pattern runs across every LED that `gpio.num_leds()` reports, its speed can be adjusted, and pressing the button ten times makes the counter show exactly ten
- [ ] You can explain what happens, and why, if the debounce code is removed
- [ ] A three-colour control panel: touching it on and off follows the real light, and the on-screen state matches the real light in every case tested
- [ ] Turning the knob moves the bar across its whole range, threshold lights turn on one at a time, and the filtered value visibly sits steadier than the raw value on screen
- [ ] You can answer how a low `alpha` and a high `alpha` for the EMA give different results
