---
doc_id: BBX-DDR-002
title: BreatheBox recommendations accepted
project: BreatheBox
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-26'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the recommendations accepted by Amish on 2026-09-25, what changed in the repo and the items still open
- version: "0.2"
  date: '2026-09-26'
  author: Amish Chadha
  change: "Budget set to $255 to cover the priced BOM: decided by Amish, 2026-09-26 (O3 closed)"
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Amish accepted every recommendation in `docs/REVIEW.md` and BBX-DDR-001. Items without a recommendation stay proposed, awaiting Amish, except the budget gap (O3), decided by Amish on 2026-09-26.

## Context

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item in `docs/REVIEW.md` and BBX-DDR-001 that was awaiting Amish or adopted for TRL 3 pending his review, and that carried a recommendation, is now decided: go with recommendation. Where a recommendation offered several options, the recommended option is the decision. Items with no recommendation are not decided here. TRL 4 remains on hold by Amish's instruction, so decided items that need building, testing or purchasing are recorded as decided but on hold.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item (source) | Decision | What changed in the repo |
| --- | --- | --- | --- |
| 1 | Budget (TRL 2 item 1; DDR-001 A1) | Raise `budget_usd` from $220 to $250; keep the bought core and the CO2 sensor | `project.yaml` `budget_usd` 220 to 250; README budget line; BBX-REQ-001 R15 target $250; BBX-CAL-001 section 9 and `results.csv`; BBX-PRB-001 constraints; `bom/bom-notes.md`; blueprint key figures. R15 is still not met ($255, $5 over) |
| 2 | Window type (TRL 2 item 2; A2) | Vertical sliding sash first; casement and tilt-and-turn later | Wording only (BBX-PRB-001, BBX-REQ-001 R8, BBX-PRC-001); design already sash-first |
| 3 | Core type (TRL 2 item 3; A3) | Bought polymer counterflow plate core | Wording only (BBX-PRC-001); already in BOM line 2 |
| 4 | Frost strategy (TRL 2 item 4; A4) | Slow the supply fan, with the combustion-appliance warning | Wording only; already in BBX-CAL-001 section 6 and the safety notes |
| 5 | Nominal airflow (TRL 2 item 5; A5) | 50 m³/h with CO2-driven boost to 70 m³/h | Wording only; already the design case |
| 6 | Controller (TRL 2 item 6; A6) | ESP32-C3 class module with an SCD41 class sensor, checked on CalRig | Wording only. The CalRig sensor check is TRL 4 work: decided, on hold |
| 7 | Noise, R6 (TRL 3 item 2; DDR-001 O2) | Option (a) quiet night mode near 30 to 32 m³/h, plus option (b) larger, slower fans or a lined silencer checked against a real fan datasheet before any change to R6 | Firmware rule added: night mode holds both streams at 32 m³/h and suppresses the CO2 boost. BBX-CAL-001 v0.2 (`sizing.py`): 30.1 dB(A) clean, 32.0 dB(A) loaded; CO2 1,295 ppm overnight, 712 ppm 24 h mean. BBX-PRC-001, BBX-REQ-001 R4 and R6 status, BBX-DWG-001 note (Rev P1 to P2), blueprint key figures, README. R6 target unchanged and still not met at 50 m³/h. Option (b) needs a chosen fan and its datasheet: decided, on hold with TRL 4 |
| 8 | Larger blowers, about 100 m³/h free air and 400 Pa (TRL 3 item 4) | Keep | Already in BOM lines 3 and 4 and BBX-CAL-001; wording updated in BBX-PRC-001 |
| 9 | 2 A time-delay input fuse (TRL 3 item 4) | Keep | Already in BOM line 13; wording updated in BBX-PRC-001 |
| 10 | Firmware fan speed cap at the 80 m³/h need (TRL 3 item 4) | Adopt as a firmware rule | BBX-PRC-001 (How it works, step 6) and BBX-CAL-001 section 4 now state it as a rule. No firmware is written (TRL 4, on hold) |
| 11 | Install restriction for rooms whose door seals airtight (TRL 3 item 4) | Keep | Already in the safety notes of BBX-PRC-001 and BBX-CAL-001 |

No recommendation changed the pitch or problem wording, so `project.yaml` and `README.md` keep them.

### Items still open

*Table 2. Items still proposed, awaiting Amish (no recommendation was made).*

| # | Item | Status |
| --- | --- | --- |
| O1 | First co-design partner and region (for example a tenants' group or social landlord in the UK or Canada) | Proposed, awaiting Amish |
| O3 | Budget gap: priced BOM $255 against the new $250 (accept about $255, drop to smaller blowers and lose the 70 m³/h boost, or find $5 elsewhere) | Decided by Amish, 2026-09-26: budget set to $255 (see below) |
| O4 | Fan position: both fans in the room-end plenum (exhaust side of the core at higher pressure, so any core leakage reaches the supply) versus the exhaust fan at the outdoor end | Proposed, awaiting Amish. No change made |

### Budget approved, 2026-09-26

On 2026-09-26 Amish wrote: "i approve all the budget items."

- Budget set to $255 to cover the priced BOM: decided by Amish, 2026-09-26. This closes O3. `project.yaml` `budget_usd` 250 to 255; BBX-REQ-001 R15 target $255, status Not met to Met; BBX-CAL-001 v0.3 (`sizing.py` and `results.csv` rerun); BBX-PRB-001, BBX-PRC-001, README, `bom/bom-notes.md` and the blueprint key figures updated. The BOM and geometry are unchanged.

## Consequences

- Requirement status (BBX-CAL-001 v0.3): met 11, not met 1 (R6 at 50 m³/h), not verifiable at TRL 3 3 (R9, R13, R14). The night mode narrows the R6 gap in use but not as R6 is written. R15 is met since the 2026-09-26 budget approval.
- The geometry and BOM are unchanged. The GA drawing moves to Rev P2 for the night mode note only; STEP and STL were re-exported from the unchanged model.
- Cross-repo: the SCD41 class sensor check on CalRig is decided and on hold with TRL 4. No other repo is affected, and none was edited.
- `trl: 3` and `trl_target: 3` are unchanged.
