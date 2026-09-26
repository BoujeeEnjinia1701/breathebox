---
doc_id: BBX-PRC-001
title: BreatheBox design precis
project: BreatheBox
doc_type: Design precis
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (architecture, first-order numbers, safety, media)
---

# BreatheBox design precis

## Summary

BreatheBox is a single-room heat recovery ventilator that sits on the sill of a sash window. Two small 24 V fans push stale room air out and draw fresh air in through a counterflow plate core, so the incoming air picks up about 80 % of the heat (or, in summer, the cool) of the outgoing air. First-order estimates for a bedroom at 50 m³/h and 0 °C outdoors: about 270 W of heat kept in the room for about 9.5 W of fan power, CO2 near 1,000 ppm with two sleepers, and about $243 in parts, which is over the $220 budget. All figures are estimates to be checked at TRL 3.

![Hero render](../media/hero.png)

Figure 1. Massing model on a sash window, with a 1.75 m person for scale.

## How it works

1. **Mount.** A 20 mm insulated panel fills the gap under the raised lower sash, which closes down onto it and is locked. The housing rests on the sill and on a clamped bracket; nothing is drilled.
2. **Exhaust path.** Room air enters a front grille, passes a coarse filter and one set of channels in the core, and leaves by the exhaust fan through a downward-facing outdoor hood.
3. **Supply path.** Outdoor air enters the second hood, about 420 mm from the exhaust outlet, passes an ePM1 filter and the other set of core channels, and the supply fan blows it into the room through a top grille that throws air up and away from the occupant.
4. **Recover.** The two streams flow in opposite directions on each side of thin polymer plates, so heat passes across without the air mixing.
5. **Drain.** In winter, moisture from the room air condenses in the core. A tray under the core falls to the outdoor side and a tube carries the water outside.
6. **Control.** A small controller reads CO2, humidity and temperature at the room intake and runs the fans between 30 and 70 m³/h. A temperature probe at the core's exhaust outlet triggers a frost mode that slows the supply fan when the outgoing air nears 0 °C. Readings show on a status LED and, optionally, on a local web page; nothing needs the cloud.

![Cutaway](../media/cutaway.png)

Figure 2. Cutaway through the supply side: hood and duct (outdoors, left), insert panel, filter, core over the condensate tray, supply fan and controller.

## Main components

Table 1. Main components. Numbers match `bom/bom.csv` and Figure 4.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Insulated housing | PVC foam board shell with 10 mm foam lining, about 470 x 560 x 250 mm | Lift-off lid for filters |
| 2 | Counterflow core | Polymer plate core about 180 x 180 x 300 mm | Spare-part HRV core; washable. Proposed, awaiting Amish |
| 3, 4 | Supply and exhaust fans | 24 V brushless centrifugal blowers, 120 mm class, PWM with tach | Tach allows flow balancing |
| 5 | Supply filter | ISO 16890 ePM1 50 % panel | Replace about every 6 months |
| 6 | Exhaust filter | Coarse washable pad | Keeps lint off the core |
| 7 | Controller | ESP32-C3 class module with a Sensirion SCD41 class CO2, humidity and temperature sensor and two NTC probes | Check the sensor on the lab's CalRig before use |
| 8 | Condensate tray and drain | PETG tray, 12 mm tube to outdoors | Falls outward |
| 9 | Window insert panel | 20 mm insulated panel with EPDM edge seals, trimmed to 700 to 1,000 mm | Sash locks onto it |
| 10 | Outdoor hoods and ducts | Two PVC hoods with 1 mm stainless mesh | Openings face down |
| 11 | Sill bracket | Aluminium plate and struts to a padded wall foot | Clamps; no drilling |
| 12 | Power supply | Certified 24 V, 1.5 A plug-in adapter | No mains wiring in the unit |

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3. Assumptions: air density 1.2 kg/m³, specific heat 1,005 J/(kg·K), design case as in BBX-REQ-001.

Table 2. First-order estimates.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Heat capacity rate of the airflow | about 16.8 W/K | 50 m³/h x 1.2 kg/m³ x 1,005 J/(kg·K) / 3,600 s/h | |
| Heat carried by exhaust air at 20 K difference | about 335 W | 16.8 W/K x 20 K; this is also the loss from an open window giving the same airflow | |
| Heat recovered | about 268 W; about 67 W still lost | 80 % sensible effectiveness | R2 met on paper |
| Supply air temperature at 0 °C outdoors | about 16 °C | 0 + 0.8 x 20 K | |
| Fan and control power | about 9.5 W | Two fans at about 4.5 W each (about 1.1 W air power at 80 Pa, about 25 % fan efficiency), controls about 0.5 W | R3 met on paper |
| Heating-season energy kept | about 1,100 kWh per season | 16.8 W/K x 24 h x 3,500 K·d (assumed cold-temperate climate) x 0.8 | |
| Fan energy over the same season | about 50 kWh | 9.5 W for 212 days | |
| CO2, two sleeping adults | about 980 ppm at 50 m³/h; about 820 ppm at 70 m³/h | Steady state, 0.014 m³/h per sleeper, 420 ppm outdoors | R4 marginal at 50, met at 70 |
| Condensate, upper bound | about 0.14 L/h | Room air 7.3 g/kg cooled to about 4 °C (saturation about 5.0 g/kg), 60 kg/h of air | R7 drain sized for 0.15 L/h |
| Frost onset | around -5 °C outdoors | Exhaust leaves the core at about 20 - 0.8 x (20 - T_out); at -5 °C this is about 0 °C | R7 at risk |
| Clear distance between hood openings | about 420 mm | Massing model | R11 met on paper |
| Unit mass | about 10 kg | Housing 3 kg, core 1.5 kg, fans 0.8 kg, panel 1.5 kg, hoods 1 kg, bracket 1.5 kg, others 0.7 kg | R9 met on paper |
| Parts cost | about $243 | Indicative prices, `bom/bom.csv` | **R15 not met** ($220 target) |

![Heat flow](../media/flow.png)

Figure 3. Heat flow in the design case (estimates).

## Key design choices

Each choice below is proposed, awaiting Amish.

- **Window insert rather than wall core.** Renters can install it, and it comes out without a trace. The cost is that it only suits windows with a vertical or horizontal sliding sash (R8).
- **Continuous counterflow core rather than a pair of alternating regenerative units.** A plate core runs one steady fan per stream, is simple to model and build, and keeps supply and exhaust separate. Alternating ceramic units avoid condensate drainage and frost more gracefully but need two wall openings and paired, reversing fans.
- **Buy the core, make the rest.** The core is the part a garage builder cannot make well. A home-made crossflow core from corrugated plastic would cost about $10 but recover only about 50 to 65 % (estimate).
- **Frost by slowing the supply fan.** The simplest frost strategy. It unbalances the flows for short periods and slightly depressurizes the room (see Safety). A small preheater would keep balance but adds mains-level power and cost.
- **24 V SELV only.** A certified plug-in adapter means no mains wiring for the builder (R10).
- **Sensible-only core.** A cheaper, washable polymer core. An enthalpy (moisture-transfer) core would suit hot, humid climates and dry winters better, at a higher price.

![Exploded view](../media/exploded.png)

Figure 4. Exploded view with BOM numbers.

## Safety

> **Safety:** Do not use BreatheBox in a room with an open-flued or unflued fuel-burning appliance (gas fire, oil or wood stove, water heater). In frost mode the unit extracts more air than it supplies and could draw combustion gases into the room.

> **Safety:** The raised sash must be locked onto the insert panel. An unlocked sash is a security risk, and a loose panel could fall outward from an upper floor. Check the bracket and panel before leaving the unit unattended, and never install from outside above ground level.

> **Safety:** Use only a certified 24 V SELV plug-in adapter, with a fuse on the low-voltage input. Do not open or modify the adapter. Keep the cable clear of the sash and of the condensate tube.

- Foam and plastics in the housing burn; choose fire-retardant grades and keep the unit away from heaters and curtains near heat sources.
- Fan impellers can cut fingers: guards or grilles on both room openings, and disconnect power before opening the lid.
- Clean the tray and replace filters on schedule; standing water and wet filters can grow mould.
- The CO2 reading is a ventilation indicator only and is not a health or medical measurement.

## Open questions for TRL 3

- Fan operating point: do 120 mm class blowers deliver 50 to 70 m³/h against the estimated 80 Pa, quietly enough for R6?
- Frost: how long does frost mode run at -10 °C, and what is the net depressurization?
- Core: which spare-part cores are available, at what size, effectiveness and pressure drop?
- Airtightness: how much air leaks around the insert panel and sash, and does it matter for balance?
- Window survey: what share of the first users' windows are sash, slider, casement or tilt-and-turn?
- Controller: reuse a common lab controller, or a single module as proposed?

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
