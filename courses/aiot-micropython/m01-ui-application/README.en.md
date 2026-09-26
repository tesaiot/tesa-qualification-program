# Module 1 — Existing UI-based Application

> Existing UI-based Application · [Course page](../README.md)

Meet the board through the apps it ships with, put your first lines on screen with lcd and ui, then send a value from the board out over the network and take a command back.

## Module objectives

See where the whole course ends up from the menus that ship on the board, know what the board's two brains do, put your own text on the screen, and take the board online for the first time: join WiFi, send a real value to a public broker, then take a command back to switch a light on the board.

## Lessons

| Lesson | Topic | Time (min) | Slides |
|---|---|---|---|
| [1.1](l01-board-tour/README.md) | Board tour: play with the real thing first | 50 | [slides.md](l01-board-tour/slides.md) |
| [1.2](l02-first-lines-on-screen/README.md) | First lines on screen: the lcd and ui modules | 75 | [slides.md](l02-first-lines-on-screen/slides.md) |
| [1.3](l03-inside-the-box/README.md) | Inside the box: two cores, AIoT and your team's screen | 75 | [slides.md](l03-inside-the-box/slides.md) |
| [1.4](l04-wifi-first-connect/README.md) | Leaving the desk: the first WiFi connection | 65 | [slides.md](l04-wifi-first-connect/slides.md) |
| [1.5](l05-values-out-commands-back/README.md) | Values out, commands back: MQTT on a public broker | 70 | [slides.md](l05-values-out-commands-back/slides.md) |
| [1.6](l06-link-lab/README.md) | Hands-on: a real value leaves the board, module 1 wrap-up | 70 | [slides.md](l06-link-lab/slides.md) |

The lessons in this module come in sets of three: concept → code walk-through → hands-on (the third lesson of each set has practice files and solutions).

## Module checkpoint

You pass this module when you can do every item below (the details are in the **Lab** section of the hands-on lessons):

- [ ] Play all five main menus and say which menu uses which sensor
- [ ] The board's screen shows the title, the team name, the members' names and a closing green line from the practice file `s01_hello_lcd.py`
- [ ] The file `09_your_level_rule.py` passes all six rows
- [ ] The board gets an IP address that is not `0.0.0.0`, and you can explain why a wrong password waits longer than a correct one
- [ ] Values from the board appear on your team's reader web page, or you can read from the screen at which step the link broke, and a command from the web page comes back and switches a light on the board
