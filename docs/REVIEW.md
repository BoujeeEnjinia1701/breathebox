# Review note: BreatheBox

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (BBX-PRB-001 v0.2): problem, why it matters (cited), users, operating context, constraints, out of scope, prior work, open questions. There was no co-design checklist to keep.
- `docs/03-requirements.md` (BBX-REQ-001 v0.2): 15 measurable requirements (R1 to R15) with targets, a defined design case, a status column and assumptions.
- `docs/02-concept.md` (BBX-PRC-001 v0.2): how it works, numbered components, first-order numbers with assumptions, design choices, safety section, open questions.
- `cad/src/concept_media.py`: massing model of a sash window in a 250 mm wall with the unit on the sill (12 numbered parts); key figures and flow labels updated.
- `media/`: hero with a 1.75 m person, blueprint sheet (PNG, PDF, SVG), `model.glb` and `viewer.html`, exploded view with callouts 1 to 12, cutaway through the supply side, heat flow diagram (estimates). Temporary `media/_views*` folders removed.
- `bom/bom.csv` (13 rows, rows 1 to 12 match the exploded view) and `bom/bom-notes.md`.
- `README.md`: hero and links line; Concept rationale, Burning platform, Where it could be used, What sparked the idea expanded with cited figures; Key components and Safety updated (the old note about mains wiring no longer applied).
- `docs/pdf/`: branded PDFs rebuilt.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Airflow | 30 to 70 m³/h, 50 m³/h nominal (proposed) | R1 at risk (fan operating point) |
| Sensible recovery | about 80 % at 50 m³/h | R2 met on paper (75 %) |
| Heat kept at 0 °C out, 20 °C in | about 268 W of 335 W | |
| Supply air at 0 °C outdoors | about 16 °C | |
| Fans and controls | about 9.5 W | R3 met on paper (12 W) |
| Season energy kept (3,500 K·d assumed) | about 1,100 kWh, for about 50 kWh of fan energy | |
| CO2, two sleepers, 30 m³ room | about 980 ppm at 50 m³/h, about 820 ppm at 70 m³/h | R4 marginal at 50, met at 70 |
| Condensate, upper bound | about 0.14 L/h | R7 drain sized |
| Frost onset | around -5 °C outdoors | R7 at risk |
| Mass | about 10 kg | R9 met on paper |
| Parts cost | about $243 | **R15 not met** ($220) |

Requirements not met or at risk:

- **R15 (cost) not met:** about $243 against $220 (about 10 % over).
- **R8 (fit) not met** for casement and tilt-and-turn windows; the concept covers sash and slider windows only.
- **R1, R6, R7 at risk:** fan operating point, night noise (30 dB(A) at 1 m) and frost behavior are unverified.
- **R4 marginal:** two sleepers need the 70 m³/h boost to stay under 1,000 ppm, which makes R6 harder.

### Proposed, awaiting Amish (status updated 2026-09-25)

1. **Budget.** Options: (a) raise `budget_usd` from $220 to $250; (b) keep $220 by using a home-made crossflow core (about $10, but only about 50 to 65 % recovery, which fails R2); (c) keep $220 by dropping the CO2 sensor for humidity-only control (about $20 saved, weakens R4). Recommendation: (a). **Decided by Amish, 2026-09-25: go with recommendation** (BBX-DDR-002). `budget_usd` is now $250.
2. **Window type for the first version:** vertical sliding sash (recommended) versus a tilt-and-turn insert for continental Europe. **Decided by Amish, 2026-09-25: go with recommendation** (BBX-DDR-002).
3. **Core type:** bought polymer counterflow plate core (recommended) versus alternating regenerative units or an enthalpy core for humid climates. **Decided by Amish, 2026-09-25: go with recommendation** (BBX-DDR-002).
4. **Frost strategy:** slow the supply fan (recommended, with the combustion-appliance warning) versus a low-power preheater. **Decided by Amish, 2026-09-25: go with recommendation** (BBX-DDR-002).
5. **Nominal airflow:** 50 m³/h with CO2-driven boost to 70 m³/h (recommended) versus 70 m³/h fixed. **Decided by Amish, 2026-09-25: go with recommendation** (BBX-DDR-002).
6. **Controller:** single ESP32-C3 class module with an SCD41 class sensor (recommended), with sensor checks on CalRig. **Decided by Amish, 2026-09-25: go with recommendation** (BBX-DDR-002). The CalRig check is on hold with TRL 4.
7. **First co-design partner and region** (for example a tenants' group or social landlord in the UK or Canada). Still proposed, awaiting Amish (no recommendation).

No change to `project.yaml` pitch or problem: the numbers found support "recovering most of the heat".

### Safety concerns

- Depressurization in frost mode could draw combustion gases from open-flued or unflued appliances; the unit must not be used in such rooms.
- Window security and falling parts: the sash must be locked onto the panel; loose panels or hoods could fall from upper floors.
- Low-voltage only, from a certified adapter; fused input. Foam and plastic housing is combustible; fire-retardant grades proposed.
- Fan impellers (finger guards), and mould growth in a neglected tray or filter.

### Notes and gaps

- Several sources could not be fetched this session (US DOE, EU ecodesign regulation text, LUNOS product data), so no efficiency limits from regulations or competitor specifications are quoted. The claim that no open-source window HRV exists rests on a limited search.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).

### Recommended next step

Review this note and the media, then decide items 1 to 3. If approved, run `/advance-trl3` to check the fan operating point, pressure drop, noise, frost and condensate estimates by calculation and produce the parametric model and drawing sheet.

## Session 2026-09-25: TRL 3

Amish's instruction for this batch (2026-09-25): "you know the drill, nothing gets past TRL 3". He did not review this repo's TRL 2 items one by one, so the recommendations were adopted for TRL 3 work, open for his review. Nothing here is recorded as decided or approved by him.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (BBX-DDR-001 v0.1): items A1 to A6 adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review; O1 (co-design partner) stays "Proposed, awaiting Amish"; O2 (noise) and O3 (budget figure) added as open.
- `docs/04-calcs/01-sizing.md` (BBX-CAL-001 v0.1), `docs/04-calcs/sizing.py` and `docs/04-calcs/results.csv`: core effectiveness from plate geometry, pressure drop per stream, fan operating points, power, noise, heat recovery, condensate, frost onset and frost mode, room depressurization, CO2, geometry, bracket load, mass and cost, with a results table for R1 to R15. The script imports `cad/src/model.py` and reads `bom/bom.csv` and `project.yaml`.
- `cad/src/model.py`: parametric build123d model (massing plus: housing with dividers, ports and grilles; core; blowers; filters; controller; tray and drain; insert panel; hoods with offset mouths and collars; sill bracket; adapter). Exports `cad/step/` and `cad/stl/` for `breathebox-assembly`, `-housing`, `-core`, `-insert-panel`, `-hoods` and `-sill-bracket`. The built-in clash check finds no overlaps (the TRL 2 massing had ducts running through the panel).
- `cad/src/sheets.py` and `cad/drawings/BBX-DWG-001.svg`, `.pdf`, `.png`: general arrangement, Rev P1, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept blueprint keeps BBX-DWG-010. `cad/drawings/.gitkeep` removed.
- `bom/bom.csv` (13 lines, all priced with a supplier or supplier type; $255.00) and `bom/bom-notes.md`.
- `cad/src/concept_media.py` now builds from `model.py`; all media refreshed and checked by eye (`hero`, `cutaway`, `exploded`, `flow`, `concept-blueprint` PNG, PDF and SVG, `model.glb`, `viewer.html`). The exploded callout for the supply filter was moved so it is no longer hidden behind the housing. Temporary `media/_views*` folders deleted.
- BBX-PRB-001, BBX-PRC-001 and BBX-REQ-001 bumped to v0.3 (numbers from BBX-CAL-001; design choices shown as adopted for TRL 3, open for review; R7 condensate figure corrected to 0.21 L/h; no target relaxed). `README.md`: TRL badge and line, links to the drawing and calculations, key components and performance paragraph; the required sections are unchanged in wording and order, as none of their numbers changed. `project.yaml`: `trl: 3`, `trl_target: 3`, evidence listed; pitch, problem and `budget_usd` unchanged.

### Requirement status (BBX-CAL-001, Table 8)

Met 10, not met 2, at risk 0, not verifiable at TRL 3 3.

- **Not met: R6 (noise).** About 39 dB(A) at 1 m at 50 m³/h against 30 dB(A); 30 dB(A) is reached only near 32 m³/h. The figure rests on an assumed fan noise class value and is uncertain by several decibels, but not by 9.
- **Not met: R15 (cost).** $255 against $220 in `project.yaml`, and $5 over the $250 recommended at TRL 2.
- **Not verifiable at TRL 3:** R9 (install time; mass 10.5 kg met on paper), R13 (filter change time), R14 (firmware).
- **Met:** R1 (80 m³/h per stream at full speed with loaded filters), R2 (79.8 %), R3 (5.6 W clean, 7.4 W loaded), R4 (607 ppm 24 h mean, 980 ppm overnight), R5, R7 (frost mode holds to -10 °C with the supply at 33 % of exhaust), R8 (sash; hoods need 686 mm), R10, R11 (420 mm), R12.

TRL 2 numbers corrected by the calculations: fan specification raised from about 60 to about 100 m³/h free air (the TRL 2 fan could not reach 70 m³/h at all); frost onset about -2.2 °C, not -5 °C; worst condensate 0.21 L/h, not 0.14 L/h; power 5.6 W, not 9.5 W; season fan energy 28 kWh, not 50 kWh; mass 10.5 kg installed, not 10 kg; cost $255, not $243. Heat recovered (267 W) and CO2 (980 ppm, 820 ppm) confirm the TRL 2 estimates.

### Decisions recorded (BBX-DDR-001)

Each adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review, and since **decided by Amish, 2026-09-25: go with recommendation** (BBX-DDR-002): A1 budget rise to $250 (recorded only; `budget_usd` stays $220), A2 sash windows first, A3 bought polymer counterflow core, A4 frost by slowing the supply fan, A5 50 m³/h nominal with boost to 70 m³/h, A6 ESP32-C3 class controller with an SCD41 class sensor checked on CalRig.

### Still awaiting Amish (status updated 2026-09-25)

1. **Budget figure (O3).** $220 in `project.yaml`; $250 recommended; design now $255. Options: accept about $255; save about $8 with smaller blowers, which would drop the 70 m³/h boost (R1); or find $5 elsewhere. No recommendation beyond noting that the fan change is what made R1 feasible. Still proposed, awaiting Amish; `budget_usd` is now $250 under A1. **Decided by Amish, 2026-09-26: budget set to $255** (BBX-DDR-002).
2. **Noise, R6 (O2).** Options: (a) a quiet night mode near 30 to 32 m³/h, which still meets R4 as written (24 h mean about 730 ppm) but lets the room run near 1,350 ppm overnight; (b) larger, slower fans or a lined silencer section, at extra cost and size; (c) relax R6 to about 35 dB(A). Recommendation: (a) plus (b) checked against a real fan datasheet before any change to R6. **Decided by Amish, 2026-09-25: go with recommendation** (BBX-DDR-002). Night mode added; the datasheet check is on hold with TRL 4.
3. **First co-design partner and region (O1).** No recommendation. Still proposed, awaiting Amish.
4. **Engineering proposals made in this session**, awaiting confirmation: the larger blowers (about 100 m³/h free air, 400 Pa), the 2 A time-delay input fuse, a firmware fan speed cap at the 80 m³/h need (the worst case of 35.4 W sits just under the 36 W adapter), and the install restriction for rooms whose door seals airtight. **Decided by Amish, 2026-09-25: go with recommendation** (BBX-DDR-002).
5. **Fan position (review point).** Both fans sit in the room-end plenum, so the exhaust side of the core runs at higher pressure than the supply side and any core leakage would reach the supply. Options: keep it (warm, dry, serviceable fans) or move the exhaust fan to the outdoor end (cold, wet air). No change made. No recommendation, so still proposed, awaiting Amish (BBX-DDR-002 item O4).

### Cross-repo notes

- BreatheBox depends on CalRig for the CO2 sensor check. CalRig's R9 (CO2 span 400 to 2,000 ppm against a ±(30 ppm + 3 %) reference) covers the 1,000 ppm range needed, and an SCD41 class breakout fits CalRig's 90 x 70 x 50 mm bay (R10). No conflict found; CalRig was not edited.
- No other shared component (FieldNode, CellGuard, MotionCore, ThermaCart, TwinKit) is used.

### Safety concerns

- Frost mode depressurizes the room: about 2.2 Pa at 50 m³/h and 4.4 Pa at 70 m³/h through an 800 x 10 mm door undercut, under a 5 Pa screening limit (an assumption to check against local code), but much more in a room whose door seals. The combustion-appliance restriction stays and an airtight-room restriction is added.
- Window security and falling parts from upper floors, as at TRL 2.
- 24 V SELV only; the worst-case load is close to the 36 W adapter rating, so the speed cap and the 2 A fuse matter.
- The drain tube can freeze outdoors; combustible foam and plastics; fan impellers; mould in a neglected tray or filter.

### Gaps and notes

- Citations: the LUNOS page was fetched with WebFetch on 2026-09-25. It confirms the e² as one of the smallest decentralized fans but not its installation method, so BBX-PRB-001 now says so instead of claiming cored wall holes. The US DOE and EU ecodesign sources flagged at TRL 2 were not cited in the documents, so nothing further was checked. WebSearch was not available. The claim that no open-source window HRV exists still rests on a limited search.
- Fan curves, fan noise, filter resistance and core data are class values, not datasheet values; BBX-CAL-001 section 11 lists the limits.
- The kit's cutaway cuts at the mean Y of the parts and keeps the +Y (supply) half; this shows the hood, panel, supply filter, core, tray, supply fan and controller, so it was kept as is.
- No TRL 4 material exists in the repo (`firmware/` and `electronics/` are empty; `build-log/README.md` is the stock header only).

### Recommended next step

Review BBX-DDR-001 and the items above, especially the budget figure and the R6 noise options. TRL 4 is on hold by Amish's instruction; nothing further should be done until he lifts it. For the record, TRL 4 would need a built unit, chosen fan and core datasheets, a lab test report (TST, `environment: lab`) covering flow and balance, pressure drop, power, noise at 1 m, effectiveness, condensate and a cold-chamber frost run, and build log entries.

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is now **Decided by Amish, 2026-09-25: go with recommendation**. Items without one stay proposed, awaiting Amish.

### Decisions applied and what changed

Recorded in `docs/decisions/0002-recommendations-accepted.md` (BBX-DDR-002 v0.1); BBX-DDR-001 moves to v0.2 with its status column updated. Eleven items decided:

- **Budget (A1):** `budget_usd` $220 to **$250** in `project.yaml`; R15 target $220 to $250. BOM unchanged at $255, so R15 is still not met, now by $5 instead of $35.
- **Noise (O2), option (a) plus (b):** quiet night mode as a firmware rule, both streams held at **32 m³/h** with the CO2 boost suppressed. Noise at 1 m: 38.6 dB(A) at 50 m³/h (clean) becomes **30.1 dB(A)** clean and **32.0 dB(A)** loaded in night mode. CO2 overnight 980 ppm becomes about **1,295 ppm** in night mode; 24 h mean 607 ppm becomes 712 ppm (bounding case), still under R4's 1,000 ppm. Fan and control power 5.6 W becomes 2.8 W. R6 target unchanged; option (b) (fan datasheet, silencer) is on hold with TRL 4.
- **Engineering proposals from TRL 3:** larger blowers, 2 A time-delay fuse, firmware speed cap at the 80 m³/h need (now a stated firmware rule) and the airtight-room install restriction, all kept.
- **A2 to A6:** sash first, bought counterflow core, slowed-fan frost mode, 50 m³/h nominal with 70 m³/h boost, ESP32-C3 plus SCD41 class controller. Wording updated; the design already followed them.

Files changed: `project.yaml`, `README.md` (budget line, performance paragraph, key components, new "What sparked the idea", footer), BBX-PRB-001 v0.4, BBX-PRC-001 v0.4, BBX-REQ-001 v0.4, BBX-CAL-001 v0.2 (`sizing.py` and `results.csv` rerun), BBX-DDR-001 v0.2, BBX-DDR-002 v0.1, `bom/bom-notes.md`, `cad/src/sheets.py` (BBX-DWG-001 Rev P1 to **P2**, note "Flow 30 to 70 m3/h per stream, 50 nominal, 32 night mode"), `cad/src/concept_media.py` (key figures). Geometry and BOM are unchanged; STEP, STL, drawings, media and PDFs were regenerated, which also removes the old site address from every generated file. Temporary `media/_views*` folders deleted.

### Requirement status (BBX-CAL-001 v0.2)

Met 10, not met 2, not verifiable at TRL 3 3.

- **Not met: R6 (noise).** 39 dB(A) at 50 m³/h against 30 dB(A). Night mode reaches 30 dB(A) with clean filters and 32 dB(A) with loaded ones.
- **Not met: R15 (cost).** $255 against $250.
- **Not verifiable at TRL 3:** R9 (install time), R13 (filter change time), R14 (firmware).
- **Met:** R1, R2, R3, R4 (also in night mode), R5, R7, R8 (sash), R10, R11, R12.

### Still awaiting Amish

1. **First co-design partner and region (O1).** No recommendation.
2. **Budget gap (O3).** $255 against $250: accept, drop the boost with smaller blowers, or find $5. No recommendation. **Decided by Amish, 2026-09-26: budget set to $255** (BBX-DDR-002).
3. **Fan position (O4).** Both fans in the room-end plenum or exhaust fan at the outdoor end. No recommendation.

### Cross-repo actions

- **CalRig:** check the SCD41 class CO2 sensor on CalRig before use (decided under A6). This is TRL 4 work and on hold. CalRig was not edited.

### Write-up

"What sparked the idea" in `README.md` now traces the concept to the Saskatchewan Conservation House (Regina, 1977) and its pioneering air-to-air heat exchanger, cited to the Encyclopedia of Saskatchewan (University of Regina). The earlier text about a review of the lab's research areas and the footer line about the portfolio set were removed. `docs/01-problem.md` did not attribute the idea to a review.

### TRL

`trl: 3` and `trl_target: 3` are unchanged. TRL 4 remains on hold by Amish's instruction: no build, test, purchase, PCB or firmware was started. The decided items that need TRL 4 work (CalRig sensor check, fan datasheet and silencer check for R6) are on hold.

## Session 2026-09-26: budget approved

Amish wrote on 2026-09-26: "i approve all the budget items." Budget set to $255 to cover the priced BOM: decided by Amish, 2026-09-26. This closes O3.

- `project.yaml` `budget_usd` $250 to **$255**. The priced BOM is unchanged at $255.00 (13 lines).
- R15 (cost): target $250 to $255; status **Not met to Met**. Requirement status is now met 11, not met 1 (R6 noise), not verifiable at TRL 3 3 (R9, R13, R14).
- Files changed: `project.yaml`, `README.md`, BBX-PRB-001 v0.5, BBX-PRC-001 v0.5, BBX-REQ-001 v0.5, BBX-CAL-001 v0.3 (`sizing.py` and `results.csv` rerun), BBX-DDR-001 v0.3 (O3 row), BBX-DDR-002 v0.2, `bom/bom-notes.md`, `cad/src/concept_media.py` (blueprint key figure); media and PDFs regenerated, temporary `media/_views*` folders deleted.
- Still awaiting Amish: O1 (co-design partner) and O4 (fan position). `trl: 3` and `trl_target: 3` are unchanged; TRL 4 remains on hold.
