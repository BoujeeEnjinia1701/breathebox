---
doc_id: BBX-REQ-001
title: BreatheBox requirements
project: BreatheBox
doc_type: Requirements
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
  change: First measurable requirements for TRL 2, with status against the concept
---

# BreatheBox requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with users, and will be checked by calculation at TRL 3 and revised after co-design (see BBX-PRB-001). Status is judged against the first-order estimates in BBX-PRC-001; nothing has been built or measured.

The **design case** is a 30 m³ bedroom with two sleeping adults, 20 °C and 50 % relative humidity indoors, 0 °C outdoors, and a vertical sliding sash window with a 900 mm clear width.

Table 1. Requirements and status at TRL 2.

| ID | Requirement | Target | Status at TRL 2 | Verification (TRL 3 or later) |
| --- | --- | --- | --- | --- |
| R1 | Balanced ventilation over a useful range | Supply and exhaust each adjustable from 30 to 70 m³/h (18 to 41 cfm); supply and exhaust within 10 % of each other outside frost mode | At risk: fan operating point against about 80 Pa is unverified | Fan curve against a system pressure estimate; later flow hood measurement |
| R2 | Recover heat from the exhaust air | Sensible effectiveness 75 % or more at 50 m³/h and balanced flow | Met on paper: about 80 % (estimate from core class) | Core data sheet; later temperature measurements on four ports |
| R3 | Low running power | Fans and controls 12 W or less at 50 m³/h | Met on paper: about 9.5 W (estimate) | Fan data; later power meter |
| R4 | Keep bedroom air fresh | CO2 at or below 1,000 ppm (24-hour average) in the design case, following the Health Canada residential guideline | Met at 70 m³/h (about 820 ppm, estimate); marginal at 50 m³/h (about 980 ppm, estimate) | Mass balance calculation; later CO2 logging |
| R5 | Filter the supply air | ISO 16890 ePM1 50 % or better on supply; coarse filter on exhaust to protect the core | Met by specification | Filter data sheet |
| R6 | Quiet at night | 30 dB(A) or less at 1 m from the room face at 50 m³/h | Not verified, at risk | Fan noise data and duct attenuation estimate; later sound meter |
| R7 | Handle condensate and frost | All condensate drains outdoors (up to about 0.15 L/h); runs without core blockage down to -10 °C outdoor, using a frost mode that may reduce supply flow | At risk: frost behavior below about -5 °C is unverified | Psychrometric calculation; later cold-chamber or winter test |
| R8 | Fit common windows | Vertical sliding sash windows with 700 to 1,000 mm clear width and sill 150 mm or deeper; adapter panel for horizontal sliders | Partly met: sash and slider only; casement and tilt-and-turn windows **not met** | Model check against a window survey |
| R9 | Renter-friendly installation | No drilling of frame or wall; one person installs or removes in 30 min or less; unit mass 12 kg or less | Met on paper: about 10 kg (estimate) | Fitting sequence review; later timed trials |
| R10 | Electrical safety | Only 24 V SELV inside the unit, from a certified plug-in adapter; fused low-voltage input; no user-accessible mains | Met by design | Design review |
| R11 | Weather and outdoor air | Rain-proof downward-facing hoods; insect mesh 1.5 mm or finer; 400 mm or more between supply intake and exhaust outlet | Met on paper (about 420 mm) | Model check; later spray test |
| R12 | Security and child safety | Raised sash lockable onto the insert panel; no opening wider than 100 mm through the installed unit | Met by design, unverified | Design review |
| R13 | Serviceable | Filters changed without tools in 2 min or less; core removable for washing; all parts replaceable with a screwdriver | Met by design | Design review |
| R14 | Local data only | CO2, humidity and temperature shown on the unit; works with no network or cloud account; optional local logging | Met by design | Firmware sketch review at TRL 3 |
| R15 | Affordable | Prototype parts $220 or less | **Not met:** about $243 (indicative) | Priced BOM (`bom/bom.csv`) |

## Requirements not met or at risk

- **R15 (cost) not met:** about $243 against $220. A budget change is proposed in `docs/REVIEW.md`, awaiting Amish.
- **R8 (fit) not met for casement and tilt-and-turn windows.** A separate insert is needed for those markets.
- **R1, R6 and R7 at risk:** the fan operating point, night-time noise and cold-weather frost behavior are unverified and are the main TRL 3 checks.
- **R4 marginal at 50 m³/h:** the design case needs the 70 m³/h boost while two people sleep, which makes R6 harder.

## Assumptions

- Air density 1.2 kg/m³ and specific heat 1,005 J/(kg·K).
- CO2 generation about 0.014 m³/h per sleeping adult (estimate); outdoor CO2 about 420 ppm.
- The core behaves like a typical polymer plate counterflow core of this size; effectiveness falls as flow rises.
- System pressure at 50 m³/h about 80 Pa across filter, core, hoods and grilles (estimate).
