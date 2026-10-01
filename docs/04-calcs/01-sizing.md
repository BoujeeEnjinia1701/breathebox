---
doc_id: BBX-CAL-001
title: BreatheBox sizing calculations
project: BreatheBox
doc_type: Calculation note
version: "0.5"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (core, pressure drop, fans, power, noise, heat recovery, condensate, frost, CO2, geometry, mass, cost) against BBX-REQ-001 v0.3
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); budget $250, quiet night mode at 32 m³/h and firmware rules added
- version: "0.3"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish; budget $255 covers the priced BOM, so R15 is met (BBX-DDR-002 v0.2)
- version: "0.4"
  date: '2026-09-30'
  author: Amish Chadha
  change: Constructable design (BBX-DDR-003); mass from the components as made, sill stability and bracket joints, filter seat and grille losses, cost $283 so R15 is not met
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
---

# BreatheBox sizing calculations

On paper, BreatheBox meets ten of its fifteen requirements. **One is not met and one is over its value-engineering target.** R6 (noise): the estimate is about 39 dB(A) at 1 m at 50 m³/h against 30 dB(A), and 30 dB(A) is reached only at about 32 m³/h. A quiet night mode at 32 m³/h (BBX-DDR-002) brings the estimate to about 30 dB(A) with clean filters and 32 dB(A) with loaded filters, but R6 is written for 50 m³/h. R15 (cost): the priced BOM of the constructable design (BBX-DDR-003) is $283, $28 over the $255 value-engineering target set on 2026-09-26; the savings worth trying are in the design decisions register (BBX-DEC-001). Three requirements (R9 install time, R13 filter change time and R14 firmware behavior) cannot be verified at TRL 3.

The calculations changed four TRL 2 figures. The TRL 2 fans (about 60 m³/h free air) could not reach 70 m³/h against any pressure, so the fan specification rises to about 100 m³/h free air and 400 Pa shut-off. Frost starts at about -2 °C outdoors, not -5 °C, because the plate at the cold corner is colder than the leaving exhaust air. The worst condensate flow is about 0.21 L/h, not 0.14 L/h. Fan and control power at 50 m³/h is about 5.6 W, not 9.5 W, because the system pressure is lower than the 80 Pa assumed.

Every number here is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads the geometry and part volumes from `cad/src/model.py`, the costs from `bom/bom.csv` and the budget from `project.yaml`. All values are first-principles estimates; nothing is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design.*

| Input | Value | Basis |
| --- | --- | --- |
| Design case | 30 m³ bedroom, two sleeping adults, 20 °C and 50 % RH indoors, 0 °C outdoors | BBX-REQ-001 |
| Air | 1.2 kg/m³, 1,005 J/(kg·K), 1.5 x 10⁻⁵ m²/s, 0.0257 W/(m·K) | Near 20 °C |
| Airflow per stream | 30 to 70 m³/h, 50 m³/h nominal; 32 m³/h in night mode | BBX-REQ-001 R1; BBX-DDR-001 item A5; BBX-DDR-002 |
| Core | 180 x 180 x 300 mm, 2.5 mm plate pitch, 0.15 mm polymer plates (0.19 W/(m·K)); 85 % of the plate area acts in counterflow | Typical small polymer plate core; no datasheet yet |
| Core heat transfer | Fully developed laminar flow between plates, Nu = 7.54; headers add 2.0 dynamic heads | Textbook laminar values |
| Supply filter | ISO 16890 ePM1 50 %, 25 mm pleated, 150 x 170 mm face; 50 Pa at 1.0 m/s clean, linear with velocity; replaced at twice the clean pressure drop ("loaded") | Typical for this filter class; to be replaced by the chosen filter's data |
| Exhaust filter | Coarse pad, 220 x 190 mm; 15 Pa at 1.0 m/s clean; loaded at twice | Typical |
| Hood and mesh | Hood turn K = 1.5, 1 mm mesh (open area about 59 %) K = 2.0 at low Reynolds number, on the 124 x 174 mm mouth | Conservative loss coefficients |
| Other losses | Port and collar K = 1.0; plenum turn K = 1.5 on the half core face; fan inlet K = 1.0 on a 68 mm inlet; grilles K = 1.5 on 50 % free area | Conservative loss coefficients |
| Fans | Full-speed curve Δp = 400 Pa x (1 - (Q/100 m³/h)²); speed scales by the fan laws; total efficiency 25 %, plus 0.3 W electronics per fan | Class values for 120 x 120 x 32 mm, 24 V centrifugal blowers; no datasheet yet |
| Fan noise | 52 dB(A) at 1 m for a bare fan at full speed; 50 log₁₀ of the speed ratio; 5 dB taken off for the lined plenum and grilles | Class value and fan law; the largest uncertainty in this note |
| Controls | 0.5 W at 3.3 V through an 85 % buck | ESP32-C3 class module with an SCD41 class sensor |
| CO2 | 0.014 m³/h per sleeping adult, 420 ppm outdoors, no infiltration, 8 h of sleep | Common planning values |
| Season | 3,500 K·d over 212 days | Cold-temperate climate |
| Depressurization | 5 Pa screening limit; 800 x 10 mm door undercut, discharge coefficient 0.6 | Screening assumption; to be checked against local code |
| Densities | PVC foam board 550 kg/m³; closed-cell foam 30 kg/m³; 10 x 10 mm strip 550 kg/m³; panel 190 kg/m³ effective; rigid PVC sheet 1,400 kg/m³; PETG 1,270 kg/m³; aluminium 2,700 kg/m³; modelled bolts 7,900 kg/m³; applied to each component's modelled volume | Typical materials |
| Sill friction | About 0.6 for anti-slip rubber tape on a painted or varnished sill | Assumption; to be checked with a push test |

## 2. Core effectiveness (R2)

The core has 72 channels (36 per stream) with a 2.35 mm gap and a 4.7 mm hydraulic diameter, and 71 plates with 3.83 m² of area, 3.26 m² of it effective. The laminar film coefficient is 41.2 W/(m²·K) on each side, so U is 20.3 W/(m²·K) and UA is 66.1 W/K. Because the flow in the channels stays laminar (Reynolds number 171 to 400), UA does not change with airflow.

*Table 2. Core performance, balanced flow.*

| Airflow | Heat capacity rate | NTU | Effectiveness | Channel velocity | Core pressure drop |
| --- | --- | --- | --- | --- | --- |
| 30 m³/h | 10.05 W/K | 6.58 | 86.8 % | 0.55 m/s | 6.8 Pa |
| 50 m³/h | 16.75 W/K | 3.95 | 79.8 % | 0.91 m/s | 11.7 Pa |
| 70 m³/h | 23.45 W/K | 2.82 | 73.8 % | 1.28 m/s | 16.9 Pa |

**R2 is met on paper:** 79.8 % at 50 m³/h against 75 %. At the 70 m³/h boost the effectiveness falls to 73.8 %, which is outside R2's 50 m³/h case.

## 3. System pressure drop (R1)

The supply stream loses more than the exhaust stream because it carries the ePM1 filter. The filter and the fan inlet dominate; the hoods, mesh and ports add less than 3 Pa together.

*Table 3. Pressure drop per stream, clean and loaded filters.*

| Airflow | Supply, clean | Supply, loaded | Exhaust, clean | Exhaust, loaded |
| --- | --- | --- | --- | --- |
| 30 m³/h | 27.9 Pa | 44.3 Pa | 14.4 Pa | 18.1 Pa |
| 50 m³/h | 52.3 Pa | 79.6 Pa | 28.7 Pa | 34.8 Pa |
| 70 m³/h | 81.4 Pa | 119.5 Pa | 46.8 Pa | 55.4 Pa |

At 50 m³/h the clean supply stream splits into filter 27.2 Pa, core 11.7 Pa, fan inlet 8.8 Pa, room grille 2.9 Pa, hood and mesh 0.9 Pa, plenum turn 0.7 Pa and port 0.2 Pa. The TRL 2 estimate of 80 Pa matches only the loaded supply filter case. The constructable design (BBX-DDR-003) adds about 0.5 Pa on the supply side, because the top grille opening is now 70 x 220 mm over the supply fan's outlet chamber, and about 1.1 Pa on the exhaust side, because the exhaust pad works through a 200 x 170 mm lining lip. The supply filter's lip lies on its frame, not its media, so its drop is unchanged.

## 4. Fans, power and noise (R1, R3, R6, R10)

**Operating points.** With the assumed full-speed curve, the fans reach 86 m³/h per stream with clean filters and **80 m³/h with loaded filters**, so the 30 to 70 m³/h range of R1 is covered with a margin. The TRL 2 fan (about 60 m³/h free air) could not reach 70 m³/h even with no system resistance, which is why BOM items 3 and 4 now call for about 100 m³/h free air and 400 Pa shut-off. The supply and exhaust fans run at different speeds for the same flow (0.62 and 0.57 of full speed at 50 m³/h), so balance within 10 % needs the tach feedback and a one-time calibration against the system curves. **R1 is met on paper.**

*Table 4. Operating points. Power is fans plus controls.*

| Case | Supply speed | Exhaust speed | Power | Room noise at 1 m |
| --- | --- | --- | --- | --- |
| 30 m³/h, clean | 0.40 | 0.35 | 2.6 W | 29.0 dB(A) |
| 30 m³/h, loaded | 0.45 | 0.37 | 3.3 W | 30.9 dB(A) |
| 50 m³/h, clean | 0.62 | 0.57 | 5.7 W | 38.7 dB(A) |
| 50 m³/h, loaded | 0.67 | 0.58 | 7.5 W | 40.0 dB(A) |
| 70 m³/h, clean | 0.83 | 0.78 | 11.2 W | 45.4 dB(A) |
| 70 m³/h, loaded | 0.89 | 0.79 | 14.8 W | 46.4 dB(A) |

**Power (R3).** 5.7 W at 50 m³/h with clean filters and 7.5 W with loaded filters, against 12 W. **R3 is met on paper.** Over the heating season the fans and controls use about 29 kWh.

**Noise (R6).** At 50 m³/h the estimate is about **39 dB(A) at 1 m, so R6 is not met.** With clean filters the unit reaches 30 dB(A) only at about 32 m³/h. The noise figure rests on an assumed catalog value and a fan law, so it may be several decibels out in either direction, but even a 5 dB error leaves R6 unmet at 50 m³/h.

**Night mode (BBX-DDR-002).** Amish accepted the recommendation of a quiet night mode, with larger, slower fans or a lined silencer to be checked against a real fan datasheet before any change to R6. The firmware rule is: in night mode both streams run at 32 m³/h (balanced by tach), the CO2 boost is suppressed, and frost mode and the speed cap still apply. At 32 m³/h the estimate is **30.2 dB(A) with clean filters and 32.0 dB(A) with loaded filters**, for 2.8 W and 3.6 W. With loaded filters, 30 dB(A) would need about 28 m³/h, below the 30 m³/h floor of R1, so the night mode stays at 32 m³/h and relies on filter changes. The datasheet check is on hold with TRL 4.

**Adapter and fuse (R10).** The 70 m³/h loaded case needs 14.8 W (0.62 A at 24 V). The worst case, both fans at full speed at their peak air power (58 m³/h each on the assumed curve), is about 35.4 W (1.48 A), just under the 36 W adapter rating. The firmware caps fan speed at what 80 m³/h needs (a firmware rule accepted in BBX-DDR-002), and the 24 V input carries a 2 A time-delay fuse. **R10 is met by design** (24 V SELV only).

## 5. Heat recovery

*Table 5. Heat at 0 °C outdoors and 20 °C indoors.*

| Airflow | Heat carried by exhaust | Recovered | Lost | Supply air |
| --- | --- | --- | --- | --- |
| 50 m³/h | 335 W | 267 W | 68 W | 16.0 °C (16.1 °C with fan heat) |
| 70 m³/h | 469 W | 346 W | 123 W | 14.8 °C (15.0 °C with fan heat) |

Over a season of 3,500 K·d at 50 m³/h the core keeps about 1,123 kWh of heat in the room for about 29 kWh of fan and control energy, a ratio of about 39 to 1. The 335 W is also the heat an open window would lose at the same airflow.

## 6. Condensate and frost (R7)

**Condensate.** Room air at 20 °C and 50 % RH holds 7.3 g/kg. The upper bound assumes the exhaust cools to its dry outlet temperature and leaves saturated. At 0 °C outdoors this gives 132 g/h at 50 m³/h (exhaust leaves at 4.0 °C) and 148 g/h at 70 m³/h. The worst case above frost onset is **214 g/h (0.21 L/h) at 70 m³/h and -3.0 °C**, above the 0.14 L/h estimated at TRL 2. That is 0.06 mL/s, which an 8 mm bore tube falling outward drains easily; the risk is the tube freezing outdoors, not its size.

**Frost onset.** Frost forms where the plate is coldest: the corner where cold supply air enters and exhaust air leaves. With equal film coefficients on both sides, that plate sits midway between the two air temperatures. Frost starts at about **-2.2 °C outdoors at 50 m³/h** and -3.0 °C at 70 m³/h. The TRL 2 figure of -5 °C used the exhaust air temperature alone and was too optimistic.

**Frost mode.** Slowing the supply fan (BBX-DDR-001 item A4) keeps the cold corner at 0 °C at -10 °C outdoors when the supply flow is 33 % of the exhaust flow: 17 m³/h against 50 m³/h. The room still receives 50 m³/h of fresh air, 17 m³/h through the core and 33 m³/h drawn from the rest of the home. Through an 800 x 10 mm door undercut that imbalance depressurizes the room by about 2.2 Pa (4.4 Pa at 70 m³/h), under the 5 Pa screening limit. With the door sealed, the depressurization could be much larger. **R7 is met on paper**, with the combustion-appliance restriction in BBX-PRC-001.

A preheater that kept the flows balanced at -10 °C would need about 130 W, more than three times the 36 W adapter. This supports the slowed-fan strategy for a 24 V unit.

> **Safety:** Frost mode extracts more air than it supplies. Do not use BreatheBox in a room with an open-flued or unflued fuel-burning appliance, and do not install it in a room whose door seals airtight.

## 7. CO2 (R4)

*Table 6. CO2 with two sleepers in a 30 m³ room, no infiltration.*

| Airflow | Night steady state | 24 h mean (8 h occupied) | Time constant |
| --- | --- | --- | --- |
| 30 m³/h | 1,353 ppm | 731 ppm | 60 min |
| 50 m³/h | 980 ppm | 607 ppm | 36 min |
| 70 m³/h | 820 ppm | 553 ppm | 26 min |
| 32 m³/h, night mode all day (bounding case) | 1,295 ppm | 712 ppm | 56 min |

**R4 is met on paper**: the 24 h mean is 607 ppm at 50 m³/h against 1,000 ppm, and even the night steady state (980 ppm) stays under 1,000 ppm. At 30 m³/h the 24 h mean still meets R4, although the night level reaches about 1,350 ppm. This matters for R6: the night mode at 32 m³/h (BBX-DDR-002) meets R4 as written, with a 24 h mean of 712 ppm even if it ran all day, while the room air rises toward about 1,300 ppm for part of the night.

## 8. Geometry, structure and mass (R8, R9, R11, R12)

- **R11, met on paper.** The hood mouths are 130 mm wide with outer edges at ±340 mm, leaving 420 mm between the supply intake and the exhaust outlet. Both face down, with 1 mm mesh.
- **R8, met on paper for sash windows.** The hoods need at least 686 mm of clear width, just inside the 700 mm lower bound; the panel trims to 700 to 1,000 mm. Casement and tilt-and-turn windows remain outside this version (BBX-DDR-001 item A2).
- **R12, met by design.** The largest opening through the installed unit is a 2.35 mm core channel; the mesh is 1 mm. The sash locks onto the panel.
- **Housing.** 510 x 560 x 250 mm, with 110 mm on the sill and 400 mm projecting into the room. The model now holds every component as it is made (BBX-DDR-003); its 84 constructability checks pass and no two of its 40 components overlap.
- **Stability on the sill (BBX-DDR-003).** The housing, its two rails, the struts and the wall foot are one rigid body, because each strut end has two bolts. The parts it carries weigh 8.6 kg with their centre of mass 162 mm on the room side of the wall face. The body rests on the inner edge of the sill and pushes on the wall at the foot, 400 mm lower, with about 34 N; the collars only slide into the housing, so friction at the sill is all that stops it sliding into the room. The friction needed is 0.40, against about 0.6 for anti-slip tape: a margin of about 1.5. With the concept's foot at 650 mm it would have been 0.65. A positive restraint is an open decision (BBX-DEC-001).
- **Bracket joints.** Each strut's top joint carries about 6.5 N·m: 17 MPa of bending in the 20 x 1.5 mm tube (6063 yields at about 110 MPa) and about 324 N of shear on each of its two M6 bolts. Both are small.

*Table 7. Mass from the modelled components (BBX-DDR-003).*

| Item | Mass |
| --- | --- |
| 1 Housing: boards, battens, lining, core frames, dividers, bulkhead, filter seats, lid, grilles, latches | 4.79 kg |
| 2 Core (plates 0.78 kg, frame 0.30 kg) | 1.08 kg |
| 3, 4 Fans | 0.60 kg |
| 5, 6 Filters | 0.15 kg |
| 7 Controller and status board | 0.08 kg |
| 8 Tray, pads and drain | 0.24 kg |
| 9 Insert panel and seals | 0.70 kg |
| 10 Collars, hoods and back plates | 2.08 kg |
| 11 Sill bracket: rails, cleats, struts, foot and pad | 1.23 kg |
| 12 Adapter | 0.25 kg |
| 13 Modelled bolts and cable gland | 0.19 kg |
| Sundries (wiring, gasket, glue, small screws) | 0.30 kg |
| **Total** | **11.7 kg (11.4 kg installed, without the adapter)** |

The mass part of R9 is met on paper (11.4 kg against 12 kg; it was 10.5 kg before the design was made constructable). The 30 min install time cannot be verified until someone fits the unit, so **R9 is not verifiable at TRL 3**.

## 9. Cost (R15)

The priced BOM totals **$283.00** over 13 lines, against the $255 value-engineering target (`budget_usd`, set on 2026-09-26, BBX-DDR-002; it was $250, and $220 before 2026-09-25). **R15 is over the target by $28.** The concept's BOM was $255; the rise comes from parts the concept needed but did not list, added when the design was made constructable (BBX-DDR-003): partitions, filter seats, grilles and latches (+$18), hood back plates and collar flanges (+$2), the bracket's rails, cleats and foot (+$4), and bolts, gland and anti-slip tape (+$4). The savings worth trying are in the design decisions register (BBX-DEC-001). Earlier, the increase from $243 to $255 came from the larger fans (+$8), the collars through the panel (+$2) and the input fuse and holder (+$2).

## 10. Results

*Table 8. Requirement status (from `docs/04-calcs/results.csv`).*

| ID | Value | Target | Status |
| --- | --- | --- | --- |
| R1 | 30 to 70 m³/h per stream; full-speed limit 80 m³/h with loaded filters; balanced by tach | 30 to 70 m³/h, within 10 % | Met on paper |
| R2 | 79.8 % at 50 m³/h (73.8 % at 70 m³/h) | 75 % or more at 50 m³/h | Met on paper |
| R3 | 5.7 W clean, 7.5 W loaded | 12 W or less at 50 m³/h | Met on paper |
| R4 | 24 h mean 607 ppm (712 ppm in night mode); night 980 ppm (1,295 ppm in night mode) | 1,000 ppm or less, 24 h mean | Met on paper |
| R5 | ePM1 50 % supply, coarse exhaust | ePM1 50 % or better | Met by specification |
| R6 | 39 dB(A) at 50 m³/h; night mode at 32 m³/h 30 dB(A) clean, 32 dB(A) loaded | 30 dB(A) or less at 50 m³/h | **Not met** |
| R7 | Worst condensate 0.21 L/h drains; frost onset -2.2 °C; supply at 33 % of exhaust at -10 °C | Drain all condensate; no blockage to -10 °C | Met on paper |
| R8 | Hoods need 686 mm clear width; panel 700 to 1,000 mm | Sash 700 to 1,000 mm; slider adapter | Met on paper (sash) |
| R9 | 11.4 kg; no drilling; install time not calculable | 12 kg or less; 30 min or less | Not verifiable at TRL 3 (mass met on paper) |
| R10 | 36 W SELV adapter; 14.8 W at 70 m³/h loaded; 35.4 W worst case; 2 A fuse | 24 V SELV only | Met by design |
| R11 | 420 mm between mouths; 1 mm mesh; mouths face down | 400 mm or more; mesh 1.5 mm or finer | Met on paper |
| R12 | Largest opening 2.35 mm; sash locks onto panel | No opening over 100 mm | Met by design, unverified |
| R13 | Lift-off lid; filters and core slide out | Tool-free filter change in 2 min or less | Not verifiable at TRL 3 |
| R14 | No firmware yet; checked at firmware review | Local data only | Not verifiable at TRL 3 |
| R15 | $283.00 | $255 value-engineering target | **Over the target by $28** |

Summary: met 10, not met 1 (R6), over the value-engineering target 1 (R15), not verifiable at TRL 3 3 (R9, R13, R14).

## 11. Limits of this note

- The fan curve, fan noise and filter resistance are class values, not datasheet values. R1, R3, R6 and R10 should be rechecked when parts are chosen; the night mode noise figure carries the same uncertainty.
- Laminar, fully developed flow and equal film coefficients are idealizations; real cores with headers usually recover a few points less than this model predicts.
- Leakage between streams in the core, air leakage around the insert panel and the latent heat released by condensation are not modeled. The last makes the frost onset slightly conservative.
- In the chosen layout both fans sit in the room-end plenum, so the exhaust side of the core runs at a higher pressure than the supply side. Any core leakage would carry stale air into the supply. This is noted for review and remains open (BBX-DDR-002); it is not changed here.
