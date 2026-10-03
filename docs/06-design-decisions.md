---
doc_id: BBX-DEC-001
title: BreatheBox design decisions register
project: BreatheBox
doc_type: Design decisions register
version: "0.5"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-09-30'
    author: Amish Chadha
    change: Register opened with the open decisions from REVIEW.md, BBX-DDR-002 and BBX-DDR-003
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Budget treated as a value-engineering target
  - version: "0.3"
    date: '2026-10-01'
    author: Amish Chadha
    change: Dr. Geeti Chadha added as a contributor and the project moved to the BioMedical (healthcare) area (decided by Amish)
  - version: "0.4"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Amish approved the recommendations for all eight open decisions (BBX-DDR-003 accepted); moved to decisions made; To confirm items 4 and 5 and the value engineering note updated for the 400 mm foot and the sash jammer"
  - version: "0.5"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Approved follow-ups carried out: value engineering estimate USD 294 with the sash jammer (BOM line 14) and longer struts; To confirm item 5 restated with the 400 mm foot figures"
---

# BreatheBox design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in `docs/REVIEW.md`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

*Table 1. Items to confirm when parts are bought or the trial window is chosen.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The counterflow core's ends are each split into two halves along a centre line, one per air stream, and it is 180 x 180 x 300 mm | The core frames' U and the dividers' tongues are made for that port layout; a hexagonal core with side ports needs different frames | BBX-DDR-003, P2 |
| 2 | The blowers' inlet ring is 80 mm across or less, their mounting holes, and that the supply fan's outlet can face up toward the lid grille | Sets the bulkhead holes and fan mounting; the calculations use class values for the fan curve and noise | BBX-DDR-003, P3; BBX-CAL-001 section 11 |
| 3 | The supply filter is 150 x 170 x 25 mm with a frame at least 5 mm wide; the exhaust pad is 220 x 190 x 12 mm | The lining lips seal on the filter frame and the pad edge | BBX-DDR-003, P5 |
| 4 | The trial window's sill is at least 110 mm deep, its stop bead fits the 17 mm gap between the housing and the collar flange, and the wall below is clear for the foot about 370 to 430 mm above the floor (no radiator or skirting); the foot goes back to 500 mm only where the lower foot is blocked and the push test passes on that sill | Sets the collar length and whether the bracket fits; the first prototype has its foot at 400 mm (decided 2026-10-02) | BBX-DDR-003, P8, P9 and A2 |
| 5 | The anti-slip tape grips the trial sill's finish with friction of about 0.6 or more | The unit needs 0.32 with the foot at 400 mm (margin about 1.9 on anti-slip tape) and 0.40 if the foot goes back to 500 mm (margin about 1.5); the 50 N push test at the trial window decides | BBX-DDR-003, A2 |
| 6 | The toggle latches fit 6 mm board, and the latch screws can be backed by nuts inside | Lid fixing | BBX-DDR-003, P1 |

## Value engineering

Value-engineering target: USD 255 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 294 (USD 39 over the target). Main cost drivers and savings worth trying:

- The largest lines are the counterflow core (USD 48), the insulated housing (USD 42), the controller with CO2 and humidity sensing (USD 42), the outdoor hoods and collars (USD 26), the window insert panel (USD 20) and the two fans (USD 19 each).
- The concept's bill of materials was USD 255. The rise came from parts the concept needed but did not list (BBX-DDR-003): partitions, filter seats, grilles and latches (USD 18), hood back plates and collar flanges (USD 2), the bracket's rails, cleats and foot (USD 4), and bolts, gland and anti-slip tape (USD 4).
- The 2026-10-02 decisions added USD 11: the bought sash jammer (line 14, USD 10) and longer struts for the 400 mm foot (line 11, USD 1).
- Savings worth trying: printed grilles and a cheaper core, at some cost in performance.

## Decisions made

*Table 2. Decisions made by Amish.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 items A1 to A6: budget raised, sash windows first, bought polymer counterflow core, frost by slowing the supply fan, 50 m³/h nominal with boost to 70 m³/h, ESP32-C3 class controller with an SCD41 class sensor | Amish: "i accept all your recommendations, go with them across all repos." | BBX-DDR-001, BBX-DDR-002 |
| 2026-09-25 | Noise (R6): quiet night mode at 32 m³/h, plus larger slower fans or a lined silencer checked against a real datasheet before any change to R6 (on hold with TRL 4) | Amish, same instruction | BBX-DDR-002, item 7 |
| 2026-09-25 | Larger blowers (about 100 m³/h free air, 400 Pa); 2 A time-delay input fuse; firmware fan speed cap; no use in a room whose door seals airtight | Amish, same instruction | BBX-DDR-002, items 8 to 11 |
| 2026-09-25 | Check the CO2 sensor on the lab's CalRig before use (on hold with TRL 4) | Amish, same instruction | BBX-DDR-002, item 6 |
| 2026-09-26 | Budget set to $255 to cover the concept's priced BOM | Amish: "i approve all the budget items." | BBX-DDR-002 v0.2 |
| 2026-09-30 | Build plans in the approved format, with outstanding decisions kept in this separate register, not in the build plan | Amish: "this is the correct build plan ... Extend this across all the other repos"; "don't log outstanding decisions in this build plan" | BBX-BLD-001; this register |
| 2026-09-30 | Where the concept cannot be built, fix the design assumptions so it is physically feasible (instruction; the resulting changes were accepted on 2026-10-02, below) | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | BBX-DDR-003 |
| 2026-10-01 | Dr. Geeti Chadha added as a contributor (CONTRIBUTORS.md, README Credits) and the project moved to the BioMedical (healthcare) area, with soft, non-clinical wording: a research and educational prototype, not a medical device | Amish: "yes add Dr. Geeti Chadha to breathebox and dustbadge and make those both healthcare projects" | `project.yaml`, `CONTRIBUTORS.md`, `README.md`, BBX-PRB-001 v0.7, BBX-PRC-001 v0.8 |
| 2026-10-02 | Design for construction accepted: the changes P1 to P12 as made, with the cost rise they bring (open item 1) | Amish: "i approve your recommendations for all 555 open decisions." | BBX-DDR-003, P1 to P12 |
| 2026-10-02 | Sliding restraint: the first prototype is built with the wall foot at 400 mm (option b, margin about 1.9) and the 50 N push test is run at the trial window; the foot goes back to 500 mm only where a radiator or skirting blocks the lower foot and the push test passes on that sill (open item 2) | Amish: "i approve your recommendations for all 555 open decisions." | BBX-DDR-003, A2 |
| 2026-10-02 | Sash lock (R12): a bought no-drill sash jammer or adjustable security bar in the inner track above the raised sash is added to the bill of materials (option a, about USD 10) (open item 3) | Amish: "i approve your recommendations for all 555 open decisions." | BBX-DDR-003, A3 |
| 2026-10-02 | Fan position: both fans stay at the room end for the prototype; a cross-leakage check (CO2 tracer in the exhaust stream, measured in the supply) is added at TRL 4, and the exhaust fan moves to the outdoor end only if transfer exceeds about 3 % (open item 4) | Amish: "i approve your recommendations for all 555 open decisions." | BBX-DDR-002, O4 |
| 2026-10-02 | First region Canada, with a tenant organization in a city with older double-hung rental stock and cold winters; first candidate to approach ACORN Canada in Toronto, with ACORN in the United Kingdom as the alternative (open item 5) | Amish: "i approve your recommendations for all 555 open decisions." | BBX-DDR-001 and BBX-DDR-002, O1 |
| 2026-10-02 | Status light and button on the room face, as the build plan already has them (open item 6) | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW.md, 2026-09-26, item 2 |
| 2026-10-02 | Clear lid window in the renders only; the prototype has an opaque lid, and a clear lid is decided at TRL 4 once its cost and flame rating are priced (open item 7) | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW.md, 2026-09-26, item 1 |
| 2026-10-02 | Lid: the top board with two toggle latches, as built; the appearance model is updated to match (open item 8) | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW.md, 2026-09-26, item 3; BBX-DDR-003, P1 |
