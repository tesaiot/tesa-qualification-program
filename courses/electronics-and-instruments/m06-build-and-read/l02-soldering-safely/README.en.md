---
id: elec.m06.l02
lang: en
title: {th: บัดกรีอย่างปลอดภัย, en: Soldering safely}
summary: {th: บัดกรีจุดต่อที่ดี ตรวจงานด้วยตาและมัลติมิเตอร์ และทำงานอย่างปลอดภัยต่อตัวเองและบอร์ด, en: 'Make good joints, inspect by eye and multimeter, and work safely for yourself and the board.'}
level: L2
time_min: {concept: 15, practise: 20, lab: 25, check: 5}
hardware:
  emulator: false
  boards: [eva-kit, devkit]
prerequisites: [elec.m06.l01]
objectives:
- {th: บัดกรีหัวต่อหนึ่งแถวที่ไม่มีจุดเย็นหรือสะพานตะกั่ว และตรวจด้วยมัลติมิเตอร์, en: Solder a header row with no cold joints or bridges and verify with a multimeter.}
- {th: ระบุข้อปฏิบัติด้านความปลอดภัยของงานบัดกรีได้อย่างน้อยสี่ข้อ เช่น การระบายควันและการป้องกันไฟฟ้าสถิต, en: 'Name at least four soldering safety practices, such as fume extraction and ESD protection.'}
develops:
- {skill: hwdev.soldering, to: 2}
context:
  platform: psoc-edge-e84
  instruments: [multimeter, logic-analyzer, oscilloscope]
status: alpha
translation: done
source_sha256: 6487d04d998c2bfd4281e52291311f8bdca00249290c87b1e2f1e0871e161179
---

## Objectives

By the end of this lesson you will:

1. Solder one row of a header with no cold joints or solder bridges, and verify it with a multimeter
2. Name at least four soldering safety practices, with reasons

## Before you start

- A temperature-adjustable soldering iron with a stand, a damp sponge or brass wool for cleaning the tip, flux-cored solder, extra flux (if available), and desoldering braid
- A practice board (perfboard) or a cheap sensor board with unsoldered pins, and a 1 × 8 male header
- Safety glasses, an ESD wrist strap, an anti-static mat if available, and a fume extractor or an exhaust fan
- **Never practise soldering on the TESAIoT Dev Kit or the Eva Kit.** Heat applied at the wrong moment can lift a copper pad or damage a chip. Practise on a spare board until confident first.

> **Safety.** A soldering iron's tip runs at several hundred degrees Celsius — even a fraction of a second's contact will burn. Always set the iron down on its stand whenever you are not using it.
> If the iron falls, **never grab it.** Let it fall, then pick it up by the handle once you have steadied yourself. If you are burned, run cool tap water over the area for several minutes.

## See it work first

Look closely at the pins of a header on a finished, factory-made board with a magnifying glass, and compare it against the solder joints on a board a friend has just learned to solder (or a picture online).
Factory joints all share the same shape — a smooth cone tapering from the pin down to the copper pad.
A bad joint looks like a dull, round ball, with a rough surface, a gap between the solder and the pad, or solder bridging two pins together.

This observation is your first inspection tool — a trained eye catches a bad joint before a multimeter does.

## Concepts

### 1. Solder, temperature, and flux

- Leaded solder, Sn63/Pb37, melts at 183 °C. A popular lead-free alloy, SAC305, melts around 217 to 220 °C.
- A commonly used iron temperature is about 320 to 350 °C for leaded solder, and about 350 to 380 °C for lead-free — check the solder manufacturer's recommendation.
  Too hot burns off the flux before it can work, and can lift a copper pad. Too cool forces you to hold the iron there so long that heat spreads everywhere.
- **Flux** removes the oxide layer on metal, letting solder wet and flow onto the surface. Solder with no flux just rolls around as a ball on the surface without bonding.

**Steps for one joint**

1. Wipe the iron clean, and coat its tip with a thin layer of solder (tinning) — a shiny tip conducts heat well
2. Touch the iron's tip to **both the pin and the pad at the same time**, and wait about a second for both to heat up
3. Feed solder **at the joint**, on the side opposite the iron, not onto the iron's tip — the solder must melt from the joint's own heat
4. Once solder has flowed around the pin as a cone, pull the solder away first, then pull the iron away — the whole thing should take about two to three seconds
5. Do not move the workpiece until the solder has solidified

### 2. Good joints, bad joints, and how to fix them

<figure>
<svg viewBox="0 0 420 175" width="420" role="img" aria-label="Cross sections of a good solder joint, a cold joint, and a solder bridge" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" font-size="13">
<path d="M20 110H120"/><path d="M50 110H90" stroke-width="4"/>
<path d="M70 40V120"/>
<path d="M32 110C50 108 64 96 66 70M108 110C90 108 76 96 74 70"/>
<text x="70" y="150" text-anchor="middle" fill="currentColor" stroke="none">good: shiny, concave</text>
<text x="70" y="166" text-anchor="middle" fill="currentColor" stroke="none">wets pin and pad</text>
<path d="M150 110H250"/><path d="M180 110H220" stroke-width="4"/>
<path d="M200 40V120"/>
<path d="M178 108C170 90 185 72 200 72C215 72 230 90 222 108"/>
<text x="200" y="150" text-anchor="middle" fill="currentColor" stroke="none">cold / not wetted:</text>
<text x="200" y="166" text-anchor="middle" fill="currentColor" stroke="none">dull ball, gap at pad</text>
<path d="M280 110H400"/>
<path d="M292 110H318M362 110H388" stroke-width="4"/>
<path d="M305 40V120M375 40V120"/>
<path d="M296 110C300 86 320 84 340 88C360 84 380 86 384 110"/>
<text x="340" y="150" text-anchor="middle" fill="currentColor" stroke="none">bridge: solder joins</text>
<text x="340" y="166" text-anchor="middle" fill="currentColor" stroke="none">two pins</text>
</svg>
<figcaption>Left: a good joint is a smooth, concave cone, bonded to both the pin and the pad. Middle: a cold joint is a round ball, not bonded to the pad. Right: a solder bridge joins two pins that should not be connected.</figcaption>
</figure>

| Appearance | Name | Common cause | Fix |
|---|---|---|---|
| A smooth, concave cone, bonded to both pin and pad (leaded solder looks shiny; lead-free is normally a bit duller) | Good joint | | |
| A dull, round, rough ball with a gap between solder and pad | Cold joint | Not enough heat reached the pad, or the workpiece moved before the solder set | Add flux, then reheat until both the pin and the pad are reached |
| Solder joins two pins | Solder bridge | Too much solder, or dragging the iron across the pins | Add flux, then remove the excess with desoldering braid |
| Too little solder, with the hole visible around the pin | Insufficient solder | Fed too little solder, or pulled away too soon | Add a bit more solder |
| A lifted copper pad, or a broken trace | Overheating | The iron held too long, or too hot | Repair with a thin wire; practise using less time |

**Align the header first.** Solder one end pin first, check that the header sits square and flush against the board. If it leans, reheat that joint and push it straight.
Then solder the other end pin, and finally the rest in between. Plugging the header into a breadboard as a jig helps keep it straight, but watch out for heat warping the breadboard's plastic.

**Check with a multimeter (always with power removed)**

- **Continuity from the pin to its trace.** Touch one lead to the pin, and the other to the far end of the trace it connects to — it must beep. If not, that is a cold joint or a broken trace.
- **Adjacent pins must not connect.** Touch each pair of neighbouring pins in turn — none should beep (except a pair the circuit intentionally connects — check against the schematic). An 8-pin single-row header has 7 such pairs to check.

### 3. Safety for you and for the board

| Practice | Reason |
|---|---|
| Set the iron on its stand every time; switch it off when leaving the desk | The tip runs at several hundred degrees — it can burn skin, wires and the desk in a fraction of a second |
| Extract fumes from the work area; never lean over them | The UK's HSE documentation states that fumes from rosin (colophony)-based flux are a common cause of occupational asthma, and its residue can cause skin irritation |
| Wear safety glasses | Solder and flux can spatter, and cut-off lead ends can fly into an eye |
| Wash your hands afterwards; never eat or drink at the soldering bench | Leaded solder is toxic if ingested |
| Use an ESD wrist strap, and handle boards by the edge | A chip can be damaged by static electricity a person cannot even feel |
| Remove power and any battery before soldering any board; never solder directly on a lithium cell | Heat can damage a cell, causing it to swell or catch fire — use a battery holder, or a cell with factory-welded tabs |
| Keep the desk clean, with no paper or flammable items near the work area | Prevents fire from the iron or hot solder debris |

**Static electricity: a small number, a large effect.** The human body model used to test chips is a 100 pF capacitor discharging through 1.5 kΩ.

```text
At 2,000 V: energy = ½ × C × V² = ½ × 100 pF × (2000 V)² = 0.2 mJ
            peak current ≈ 2000 V / 1.5 kΩ = 1.33 A
```

The energy is so small a person usually cannot feel it at all, but an ampere-scale current running through a chip's microscopic structures for just a fraction of a microsecond is enough to degrade or destroy it.
Sometimes the damage does not kill the chip outright, but causes it to misbehave later — which is the hardest kind of fault to trace back to its cause.

**Why a wrist strap has a 1 MΩ resistor.** It lets charge drain to ground slowly and safely, and if a hand touches a live point, the resistor limits the current through the body.
For example, touching a 230 V point would give a current no higher than 230 V / 1 MΩ = 0.23 mA. Never connect a wrist strap straight to ground without this resistor.

## Worked example

**Problem:** solder a 1 × 8 male header onto a sensor board, then check it is ready to use.

1. **Prepare the area.** Turn on the fume extractor, put on glasses and the wrist strap, set the iron to 330 °C (leaded) or 360 °C (lead-free), wait for it to reach temperature, then wipe and tin the tip.
2. **Align.** Plug the header into the board with the long side of the pins facing down, and hold it in place with tape or a jig.
3. **The first pin.** Solder pin 1, check alignment. If it leans, reheat and push it straight. Then solder pin 8.
4. **The rest.** Work through pins 2 to 7, about two to three seconds each, wiping the iron every few joints.
5. **Inspect by eye.** Look at every joint with a magnifying glass or a phone camera, and mark any that look suspicious.
6. **Check with a multimeter.** Every pin must connect to its destination trace (8 checks); every adjacent pair must not connect (7 checks), except a pair the board's schematic states should connect, such as two GND pins.
7. **Fix** any that fail: add flux, reheat, or remove solder, then re-check just that joint and its neighbours.
8. **Close out.** Turn off the iron, let it cool on its stand, clean off flux residue if the manufacturer recommends it, and wash your hands.

## Practice

1. Match each appearance to its name: (a) a dull, round ball with a gap around the pad (b) solder joining pin 3 to pin 4 (c) a copper pad lifted off the board (d) a smooth, concave cone bonded to both pin and pad
2. Why must solder be fed at the joint, not at the iron's tip?
3. A 1 × 10 header has how many adjacent pairs that need checking for no connection?
4. Compute the energy and peak current from the human body model (100 pF, 1.5 kΩ) at 3,000 V.
5. A wrist strap has a 1 MΩ resistor. If a hand touches a live 50 V point, what is the maximum current through the body?
6. Name four safety practices with their reasons, without looking at the table in section 3.

## Solution

1. (a) cold joint  (b) solder bridge  (c) overheating, lifting the pad  (d) good joint
2. The solder must melt from the pin and pad's own heat, which means the joint is hot enough for the solder to wet the surface and bond. Fed at the iron's tip instead, the solder would melt and drip onto a still-cool surface, becoming a cold joint, and the flux would burn off before ever reaching the joint.
3. 9 pairs.
4. Energy = ½ × 100 pF × (3000 V)² = 0.45 mJ. Peak current = 3000 V / 1.5 kΩ = 2 A.
5. 50 V / 1 MΩ = 50 µA.
6. For example: set the iron on its stand, because its tip runs at several hundred degrees; extract fumes, because flux fumes irritate the airway; wear glasses, because solder and clipped leads can fly;
   use an ESD wrist strap, because a chip can be damaged by static a person cannot feel; wash your hands, because solder is toxic (any four from the table, each with its reason, is acceptable).

## Check your understanding

Answer at least 4 of the 5 questions in [quiz.yaml](quiz.yaml) correctly.

## Lab

**Before turning on the iron, check every item on this list**

- [ ] The fume extractor or exhaust fan is running, aimed away from your face
- [ ] Safety glasses on, and the wrist strap connected to the desk's ground point
- [ ] The iron stand is stable, and the damp sponge or brass wool is ready
- [ ] No flammable items, food, or drinks on the desk
- [ ] The workpiece is a practice board or a sensor board, not a main development board

**Steps**

1. Practise on a spare board first. Solder a resistor lead or a short wire onto at least 10 pads, until the last one looks like the good-joint picture.
2. Solder the 1 × 8 header, following the worked example.
3. Photograph every joint close up, score yourself against the table, then check with a multimeter.
4. **Practise fixing a fault.** On the practice board, deliberately create a solder bridge between two adjacent pads. Measure to confirm they are connected, then fix it with flux and desoldering braid, and measure again to confirm they are separated.

| Pin | By eye (good / cold / bridge / insufficient) | Pin to trace (beeps / silent) | To the next pin (must not beep) |
|---|---|---|---|
| 1 | | | 1–2: |
| 2 | | | 2–3: |
| … | | | … |
| 8 | | | none |

## Going further

Now that you can solder, next you need to know what to connect to what. The next lesson, [Reading a schematic](../l03-reading-schematics/README.md),
practises following a signal from a microcontroller pin to a component on a real board's schematic.

## Reflect

Which of your own solder joints did your eye say was good, but a multimeter said had failed (or the reverse)? What did that mismatch teach you?

## References

- [Soldering (Wikipedia)](https://en.wikipedia.org/wiki/Soldering)
- [HSE: Controlling health risks from rosin (colophony)-based solder flux fume](https://www.hse.gov.uk/pubns/indg249.htm)
- [Electrostatic discharge (Wikipedia)](https://en.wikipedia.org/wiki/Electrostatic_discharge)
