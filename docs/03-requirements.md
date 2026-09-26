---
doc_id: BBX-REQ-001
title: BreatheBox requirements
project: BreatheBox
doc_type: Requirements
version: "0.4"
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
  change: First measurable requirements for TRL 2, with status against the concept
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Status against BBX-CAL-001 at TRL 3; R7 condensate figure corrected to 0.21 L/h; R8 and R15 notes per BBX-DDR-001 (adopted for TRL 3, open for Amish's review)
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# BreatheBox requirements

These requirements are proposals for review, not yet validated with users, and will be revised after co-design (see BBX-PRB-001). Status is judged against the TRL 3 calculations in BBX-CAL-001 and the parametric model in `cad/src/model.py`; nothing has been built or measured. No target was relaxed at TRL 3. On 2026-09-25 Amish accepted the review recommendations (BBX-DDR-002): R15 now reads against a $250 budget (it was $220), and R4 and R6 show the quiet night mode; R6 itself is unchanged until a real fan datasheet has been checked. The R7 condensate figure was corrected from 0.15 to 0.21 L/h because the calculation showed a higher worst case.

The **design case** is a 30 m³ bedroom with two sleeping adults, 20 °C and 50 % relative humidity indoors, 0 °C outdoors, and a vertical sliding sash window with a 900 mm clear width.

Table 1. Requirements and status at TRL 3.

| ID | Requirement | Target | Status at TRL 3 (BBX-CAL-001) | Verification (TRL 4 or later) |
| --- | --- | --- | --- | --- |
| R1 | Balanced ventilation over a useful range | Supply and exhaust each adjustable from 30 to 70 m³/h (18 to 41 cfm); supply and exhaust within 10 % of each other outside frost mode | Met on paper: 80 m³/h per stream at full speed with loaded filters; balance by fan tach | Flow hood measurement |
| R2 | Recover heat from the exhaust air | Sensible effectiveness 75 % or more at 50 m³/h and balanced flow | Met on paper: 79.8 % | Temperatures on the four ports |
| R3 | Low running power | Fans and controls 12 W or less at 50 m³/h | Met on paper: 5.6 W clean, 7.4 W with loaded filters | Power meter |
| R4 | Keep bedroom air fresh | CO2 at or below 1,000 ppm (24-hour average) in the design case, following the Health Canada residential guideline | Met on paper: 607 ppm 24 h mean at 50 m³/h; 980 ppm overnight. In night mode (32 m³/h): 712 ppm 24 h mean, about 1,300 ppm overnight | CO2 logging |
| R5 | Filter the supply air | ISO 16890 ePM1 50 % or better on supply; coarse filter on exhaust to protect the core | Met by specification | Filter data sheet |
| R6 | Quiet at night | 30 dB(A) or less at 1 m from the room face at 50 m³/h | **Not met** at 50 m³/h: about 39 dB(A) (estimate). Night mode at 32 m³/h (BBX-DDR-002): about 30 dB(A) clean, 32 dB(A) with loaded filters | Sound meter |
| R7 | Handle condensate and frost | All condensate drains outdoors (up to about 0.21 L/h); runs without core blockage down to -10 °C outdoor, using a frost mode that may reduce supply flow | Met on paper: frost onset about -2.2 °C; at -10 °C the supply runs at 33 % of the exhaust | Cold-chamber or winter test |
| R8 | Fit common windows | Vertical sliding sash windows with 700 to 1,000 mm clear width and sill 150 mm or deeper; adapter panel for horizontal sliders | Met on paper for sash: the hoods need 686 mm. Casement and tilt-and-turn windows are a later variant (BBX-DDR-001 item A2, decided by Amish in BBX-DDR-002) | Fit check against a window survey |
| R9 | Renter-friendly installation | No drilling of frame or wall; one person installs or removes in 30 min or less; unit mass 12 kg or less | Not verifiable at TRL 3: mass 10.5 kg met on paper; install time needs a trial | Timed trials |
| R10 | Electrical safety | Only 24 V SELV inside the unit, from a certified plug-in adapter; fused low-voltage input; no user-accessible mains | Met by design: 36 W adapter, 2 A fuse; worst case 35.4 W | Design review |
| R11 | Weather and outdoor air | Rain-proof downward-facing hoods; insect mesh 1.5 mm or finer; 400 mm or more between supply intake and exhaust outlet | Met on paper: 420 mm; 1 mm mesh | Spray test |
| R12 | Security and child safety | Raised sash lockable onto the insert panel; no opening wider than 100 mm through the installed unit | Met by design, unverified: largest opening 2.35 mm | Design review with a locking bar |
| R13 | Serviceable | Filters changed without tools in 2 min or less; core removable for washing; all parts replaceable with a screwdriver | Not verifiable at TRL 3: lift-off lid and slide-out filters and core in the model | Timed trials |
| R14 | Local data only | CO2, humidity and temperature shown on the unit; works with no network or cloud account; optional local logging | Not verifiable at TRL 3: no firmware yet | Firmware review |
| R15 | Affordable | Prototype parts $250 or less (was $220; BBX-DDR-002) | **Not met:** $255 (priced BOM), $5 over | Priced BOM (`bom/bom.csv`) |

## Requirements not met

- **R6 (noise) not met:** about 39 dB(A) at 1 m at 50 m³/h against 30 dB(A). The accepted night mode (32 m³/h) gives about 30 dB(A) with clean filters and 32 dB(A) with loaded filters; larger, slower fans or a silencer are to be checked against a real fan datasheet (on hold with TRL 4) before any change to R6.
- **R15 (cost) not met:** $255 against the $250 budget in `project.yaml`. Whether to accept about $255 or find $5 is awaiting Amish.
- **Not verifiable at TRL 3:** R9 (install time), R13 (filter change time) and R14 (firmware).

## Assumptions

- Air density 1.2 kg/m³ and specific heat 1,005 J/(kg·K).
- CO2 generation about 0.014 m³/h per sleeping adult (estimate); outdoor CO2 about 420 ppm.
- Core, filter, fan and noise values are class values stated in BBX-CAL-001 section 1, not datasheet values.
