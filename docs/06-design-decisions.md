---
doc_id: BBX-DEC-001
title: BreatheBox design decisions register
project: BreatheBox
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-09-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-09-30'
    author: Amish Chadha
    change: Register opened with the open decisions from REVIEW.md, BBX-DDR-002 and BBX-DDR-003
---

# BreatheBox design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in `docs/REVIEW.md`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

*Table 1. Open decisions, all Proposed, awaiting Amish.*

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Design for construction: accept the changes that make the concept buildable (housing boards and battens, core frames, dividers and fan bulkhead, filter seats, grilles, bolted window insert, rigid rail-and-strut bracket with the foot at 500 mm, drain and power entry) | Accept as made; or ask for changes item by item | Accept | The whole build plan | BBX-DDR-003, P1 to P12 |
| 2 | Budget: parts now cost $283.00 against the $255 budget, so R15 is not met | (a) set the budget to $283; (b) find $28 of savings, such as printed grilles or a cheaper core, at some cost in performance; (c) keep $255 and record R15 as not met for the prototype | (a) | Bill of materials; R15 | BBX-DDR-003, A1 |
| 3 | Sliding restraint: only sill friction (needed 0.40, about 0.6 available on anti-slip tape) stops the unit sliding into the room and tipping off the sill | (a) accept, with a 50 N push test at TRL 4; (b) lower the foot to 400 mm (margin about 1.9, longer struts); (c) a positive restraint such as a strap or a clamp to the window board, which may need drilling | (a), moving to (b) if the push test fails | Wall foot height and strut length (sections 3.12 and 3.13); first checks | BBX-DDR-003, A2 |
| 4 | Sash lock (R12, safety case): no part locks the raised sash onto the insert panel, and the window's own catch no longer meets | (a) a bought no-drill sash jammer or adjustable bar in the inner track above the raised sash, about $10; (b) screw-fixed sash stops, which need drilling (R9) | (a) | Window fitting (step 15); bill of materials | BBX-DDR-003, A3 |
| 5 | Fan position: both fans at the room end put the exhaust side of the core at the higher pressure, so any core leakage reaches the supply | Keep both fans at the room end (warm, dry, easy to reach); or move the exhaust fan to the outdoor end (cold, wet air) | None made | Fan bulkhead and fan positions (section 3.6) | BBX-DDR-002, O4 |
| 6 | First co-design partner and region (for example a tenants' group or social landlord in the UK or Canada) | Open | None made | Trial window and its sill, stop bead and wall | BBX-DDR-001 and BBX-DDR-002, O1 |
| 7 | Status light and button on the room face, in a small pod (appearance model) | Adopt the room-face position; or keep them inside on the controller board | Adopt; the build plan already puts them behind two holes in the room face | Room end board holes and status board (sections 3.1 and 3.8) | REVIEW.md, 2026-09-26, item 2 |
| 8 | Clear inspection window in the lid (appearance model) | Keep for the renders and decide at TRL 4 on a clear lid's cost and fire rating; or an opaque lid | Keep for the renders, decide at TRL 4; the build plan uses an opaque lid | Lid (section 3.11) | REVIEW.md, 2026-09-26, item 1 |
| 9 | Lid joint: the appearance model splits the lid 40 mm below the top with side latches; the constructable design's lid is the top board alone, with two toggle latches | Top board lid as built; or the appearance model's deeper lid | Top board lid; update the appearance model to match | Lid and latches (section 3.11) | REVIEW.md, 2026-09-26, item 3; BBX-DDR-003, P1 |

## To confirm when parts are bought

*Table 2. Items to confirm when parts are bought or the trial window is chosen.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The counterflow core's ends are each split into two halves along a centre line, one per air stream, and it is 180 x 180 x 300 mm | The core frames' U and the dividers' tongues are made for that port layout; a hexagonal core with side ports needs different frames | BBX-DDR-003, P2 |
| 2 | The blowers' inlet ring is 80 mm across or less, their mounting holes, and that the supply fan's outlet can face up toward the lid grille | Sets the bulkhead holes and fan mounting; the calculations use class values for the fan curve and noise | BBX-DDR-003, P3; BBX-CAL-001 section 11 |
| 3 | The supply filter is 150 x 170 x 25 mm with a frame at least 5 mm wide; the exhaust pad is 220 x 190 x 12 mm | The lining lips seal on the filter frame and the pad edge | BBX-DDR-003, P5 |
| 4 | The trial window's sill is at least 110 mm deep, its stop bead fits the 17 mm gap between the housing and the collar flange, and the wall below is clear for the foot 470 to 530 mm above the floor (no radiator) | Sets the collar length and whether the bracket fits as drawn | BBX-DDR-003, P8 and P9 |
| 5 | The anti-slip tape grips the trial sill's finish with friction of about 0.6 or more | The unit needs 0.40 to stay put | BBX-DDR-003, A2 |
| 6 | The toggle latches fit 6 mm board, and the latch screws can be backed by nuts inside | Lid fixing | BBX-DDR-003, P1 |

## Decisions made

*Table 3. Decisions made by Amish.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 items A1 to A6: budget raised, sash windows first, bought polymer counterflow core, frost by slowing the supply fan, 50 m³/h nominal with boost to 70 m³/h, ESP32-C3 class controller with an SCD41 class sensor | Amish: "i accept all your recommendations, go with them across all repos." | BBX-DDR-001, BBX-DDR-002 |
| 2026-09-25 | Noise (R6): quiet night mode at 32 m³/h, plus larger slower fans or a lined silencer checked against a real datasheet before any change to R6 (on hold with TRL 4) | Amish, same instruction | BBX-DDR-002, item 7 |
| 2026-09-25 | Larger blowers (about 100 m³/h free air, 400 Pa); 2 A time-delay input fuse; firmware fan speed cap; no use in a room whose door seals airtight | Amish, same instruction | BBX-DDR-002, items 8 to 11 |
| 2026-09-25 | Check the CO2 sensor on the lab's CalRig before use (on hold with TRL 4) | Amish, same instruction | BBX-DDR-002, item 6 |
| 2026-09-26 | Budget set to $255 to cover the concept's priced BOM | Amish: "i approve all the budget items." | BBX-DDR-002 v0.2 |
| 2026-09-30 | Build plans in the approved format, with outstanding decisions kept in this separate register, not in the build plan | Amish: "this is the correct build plan ... Extend this across all the other repos"; "don't log outstanding decisions in this build plan" | BBX-BLD-001; this register |
| 2026-09-30 | Where the concept cannot be built, fix the design assumptions so it is physically feasible (instruction; the resulting changes are open item 1 above) | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | BBX-DDR-003 |
