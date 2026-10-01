---
doc_id: BBX-DDR-003
title: BreatheBox design for construction
project: BreatheBox
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
---

# 0003: Design for construction

- **Date:** 2026-09-30
- **Status:** Draft. The changes in Table 1 were made under Amish's 2026-09-30 instruction to make the design physically buildable; they are open for his review. The items in Table 3 change the safety case or note value engineering and are **Proposed, awaiting Amish**; they are listed in the design decisions register (BBX-DEC-001).

## Context

On 2026-09-30 Amish asked for every repo to get an illustrated prototype build plan that shows how each component is made and how it fits the next, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The concept model of BBX-DDR-002 showed what BreatheBox does: a window insert with two hoods, a lined housing on the sill with a counterflow core, two fans, two filters, a condensate tray and a sill bracket. Checked with build123d, it could not be built as drawn. The housing was one solid with no joints and no lid; the air paths leaked into each other; the core, both filters, both fans and the controller floated with nothing holding them; the collars, hoods and bracket had no fixings; and the bracket could not hold the unit on the sill.

The changes below keep what the unit does: the same window insert, hood mouths and their 420 mm spacing, the same housing envelope (510 x 560 x 250 mm, 110 mm on the sill), the same core, fans, filters, airflows and controls, and both fans still in the room-end plenum. Nothing here changes the pitch. Every change is in `cad/src/model.py`, which now models each component as it is made (40 components) and runs 84 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, parts that must keep a gap keep it, and no two components overlap. All 84 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The housing was one solid shell: no boards, no joints, and no separate lid, although the concept has a lift-off lid for filter changes. | Six pieces of 6 mm PVC foam board (base, two sides, two ends, lid), glued with PVC cement and screwed into eight 10 x 10 mm corner battens; 10 mm closed-cell foam lining glued inside between the battens. The lid is a board with a foam plug that drops inside the wall lining, held by two small toggle latches, one each side. | Butt joints in 6 mm foam board need something behind them to screw into; the battens sit inside the lining's own thickness, so the inside dimensions are unchanged. The plug locates the lid without a frame. |
| P2 | The four air paths leaked into each other: air could pass round the sides of the core from one end of the box to the other, and both dividers stopped short of the floor and the lid. | Two core frames (3 mm PVC foam board) at the ends of the core, each with a U cut 168 wide that the core's end bears on through foam gasket; three full-height dividers (3 mm board) on the centre line, two with a thin tongue that reaches through the frame's U to the core face; a foam block under the lid closes the U above the core and holds it down. | This makes four sealed chambers (supply in, supply out, exhaust in, exhaust out) with the core as the only path between them, as the concept intends. |
| P3 | Each fan sat in one open chamber with its inlet and its outlet both in it, so it would mostly stir its own air. | A 6 mm fan bulkhead across the box 94 mm in from the room face. The supply fan sits on its room side, inlet through the bulkhead, blowing up to the top grille. The exhaust fan sits on its core side, inlet through the bulkhead from the room-air chamber, blowing into the core. Both stay in the room-end plenum. | Each fan now draws from one chamber and blows into another. The exhaust side of the core still runs at the higher pressure, so the open fan-position question (O4) is unchanged. |
| P4 | The core floated 8 mm above the tray, touching only the edges of the dividers; the tray's walls were outside the core's footprint. | The tray is shortened to the core's length (300 x 200 x 14 mm) and sits between the core frames; four 20 x 20 x 12 mm pads in the tray carry the core at its corners; the lid's foam block holds it down. | Water runs freely under the core to the drain; the core lifts straight out when the lid is off (R13). |
| P5 | Both filters floated in their chambers with no seat (the supply filter 4 mm and the exhaust pad 2 mm from the lining), and the exhaust pad was exactly the size of its opening, so air could pass round both. | Filter seats from 10 x 10 mm strip: side strips, lip strips that lap 6 mm (supply) and 10 mm (pad) over the filter edges on the downstream side, and a bottom stop; foam blocks under the lid press on the top edges. The lining forms a 5 mm lip behind the supply filter's frame and a 10 mm lip behind the pad. | The airflow pushes each filter onto its lips, so the seal improves as the filter loads. Filters still slide out by hand once the lid is off (R13). The pad now works through a 200 x 170 mm window: about 1 Pa more on the exhaust side at 50 m³/h (BBX-CAL-001 v0.4). |
| P6 | The controller floated in the air above the room-end divider, with its CO2 sensor straddling the supply outlet and the room-air intake. | The controller is mounted on standoffs on the room-side divider, inside the room-air intake chamber, so its sensor reads room air as the concept says. The status light and button are on a small board behind two holes in the room face. | The sensor sees only incoming room air. The light and button position matches the appearance-model proposal of 2026-09-26, which is still open (BBX-DEC-001). |
| P7 | The room openings had no grilles or finger guards in the BOM, although the safety notes require them, and the top supply opening sat partly over the core-side chamber once the bulkhead was in. | Two perforated or slotted aluminium grilles with openings no wider than 5 mm, bolted over the openings. The supply opening is moved to 310 to 380 mm from the inside wall face and widened to 220 mm (70 x 220 mm, was 90 x 190 mm), so it is wholly over the supply fan's outlet chamber. | Fingers cannot reach a fan. The smaller supply opening adds about 0.5 Pa at 50 m³/h. |
| P8 | The collars butted the housing back and passed through the panel with no fixing, and the hoods had nothing holding them to the panel. | Each collar is a 3 mm PVC tube with a 20 mm flange on the panel's room face. Each hood is glued to a 3 mm back plate on the panel's outdoor face; four M5 bolts per side clamp flange, panel and back plate. The collar's outdoor end fits the back plate's opening; its room end slides 6 mm into the housing opening on 2 mm foam gasket and stops on the end lining. Panel cut-outs are 158 x 178 mm. | Panel, collars and hoods become one window insert, built on the bench and set in the sash track from inside. The hoods cannot fall outward. The slip joint takes up small differences between windows; the collar is cut to length at the first fit. |
| P9 | The sill bracket plate was not fixed to the housing; the tube struts ended against the plate and the foot with no joint; and the unit relied on 0.65 friction at the sill to stop it sliding into the room. | Two 50 x 4 mm aluminium rails (replacing the 390 x 400 x 4 mm plate) bolted under the housing base with two M5 bolts each. Each strut's ends are flattened and bolted with two M6 bolts to 40 x 40 x 3 mm angle cleats under the rail and on a 60 x 6 mm foot bar with a 2 mm rubber pad. The foot is lowered from 650 to 500 mm above the floor. Anti-slip rubber tape under the housing base on the sill. | Two bolts at each strut end make the bracket a rigid frame; with single bolts it would fold. The lower foot halves the sill friction needed to 0.40, a margin of about 1.5 on anti-slip tape. The rails save 1.3 kg, which keeps the unit under the 12 kg mass limit (R9). |
| P10 | The drain tube ran along the centre line through the outdoor divider, and its bore started 1 mm above the tray floor, outside the tray. | The drain leaves the tray's outdoor end wall with its bore flush with the tray floor, 40 mm to the exhaust side of the centre line, and passes through the core frame, the end wall and the panel in the exhaust-outlet chamber. | No divider is pierced and no water is left standing in the tray. The tube still falls outdoors. |
| P11 | The power cable entered the housing beside the core, in the closed space between the core frames. | An M12 cable gland in the right side wall, into the supply fan's outlet chamber, with the inline 2 A fuse there. | The cable reaches the controller and both fans through grommets in the partitions without crossing the core seal. |
| P12 | (Found in checking.) With the added partitions in 6 mm board the installed mass rose to 13.0 kg, over R9's 12 kg. | Core frames and dividers in 3 mm PVC foam board; only the bulkhead, which carries the fans, stays 6 mm. Together with P9's rails, the installed mass is 11.4 kg. | Keeps R9 met on paper without changing any part that carries load. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | Installed unit 11.4 kg (was 10.5 kg), 0.6 kg under R9's 12 kg; 11.7 kg with the adapter. | Partitions, seats, grilles, latches, back plates, flanges, cleats and bolts; offset in part by the rails (P9) and 3 mm partitions (P12). |
| Stability | The parts carried by the sill and bracket weigh 8.6 kg with their centre of mass 162 mm into the room. The foot pushes on the wall with about 34 N; the sill needs 0.40 friction (0.65 with the concept's foot at 650 mm). Each strut's top joint carries about 6.5 N·m: 17 MPa in the tube and about 324 N on each M6 bolt. | P9. |
| Pressure and power | Exhaust stream +1.1 Pa and supply stream +0.5 Pa at 50 m³/h. Fans and controls 5.7 W clean, 7.5 W with loaded filters at 50 m³/h (was 5.6 and 7.4 W); 14.8 W at 70 m³/h loaded (was 14.5 W). Night mode 30.2 dB(A) clean (was 30.1). R1, R3, R6 and R10 status unchanged. | P5, P7. |
| Cost | BOM lines 1, 8, 9, 10, 11 and 13 respecified; lines 1, 10, 11 and 13 repriced. Parts $283.00 against the $255 value-engineering target (`budget_usd`): **R15 is over the target by $28**. See Table 3, A1. | Parts the concept needed but did not list. |
| Drawing | BBX-DWG-001 Rev P3; making sketches BBX-DWG-101 to 114 added. | Follows the model. |
| Documents | BBX-CAL-001 v0.4, BBX-REQ-001 v0.6, BBX-PRC-001 v0.6: mass, stability, pressure, power and cost figures; R15 status within the value-engineering target to over it by $28. | Follows the model. |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | Value engineering (a note, not a decision). The constructable design costs $283.00 against the $255 value-engineering target, $28 over. | (a) look for $28 of savings (for example 3D-printed grilles and a cheaper core), which may cost performance; (b) accept the estimate as the cost of building and guarding the unit. | (b), with (a) pursued where performance allows; the added parts are all needed. |
| A2 | Only friction at the sill stops the unit sliding into the room (margin about 1.5 on anti-slip tape). If it slid, it would tip off the sill into the room. | (a) accept, with a 50 N push test at the trial window (TRL 4); (b) lower the foot to 400 mm (margin about 1.9, longer struts); (c) add a positive restraint, such as a strap or a clamp to the window board, which may need drilling and conflict with R9. | (a), moving to (b) if the push test fails. |
| A3 | Sash lock (R12). The concept says the raised sash locks onto the insert panel, but no part does this: the window's own catch no longer meets once the lower sash is raised. | (a) a bought no-drill sash jammer or adjustable bar wedged in the inner track above the raised sash (about $10, which adds to the estimate in A1); (b) screw-fixed sash stops, which need drilling (R9). | (a). |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan BBX-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`); the design decisions register BBX-DEC-001 lists everything still open.
- Requirement status (BBX-CAL-001 v0.4): met 10, not met 1 (R6 noise at 50 m³/h, unchanged), over the value-engineering target 1 (R15 cost, new), not verifiable at TRL 3 3 (R9 install time, R13, R14). R9's mass part is met on paper at 11.4 kg.
- The appearance model `cad/src/product_model.py` and the photoreal renders (`media/render-*.png`), `media/card.png` and `media/social-preview.png` still show the concept: no bulkhead, the old fan positions and grille, the sill plate and the old bracket foot. They need regenerating on Amish's Mac, where Blender is.
- The core's port arrangement, the blowers' inlet and mounting, and the trial window's sill, stop bead and wall below are to be confirmed when parts are bought (BBX-DEC-001).
