---
doc_id: BBX-DDR-001
title: BreatheBox TRL 2 review decisions
project: BreatheBox
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-09-26'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 recommendations adopted for TRL 3 under Amish's 2026-09-25 instruction, open for his review, and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-09-26'
  author: Amish Chadha
  change: "O3 decided by Amish, 2026-09-26: budget $255 (BBX-DDR-002)"
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** items A1 to A6 and O2 decided by Amish, 2026-09-25: go with recommendation (see BBX-DDR-002); item O1 remains proposed, awaiting Amish; O3 was decided by Amish on 2026-09-26 (budget $255, BBX-DDR-002).

## Context

The TRL 2 review note (`docs/REVIEW.md`, session of 2026-09-25) listed seven items as "Proposed, awaiting Amish", six of them with a recommendation. On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He did not review this repo's items one by one. The recommendations are therefore adopted as the basis for the TRL 3 calculations, model and drawing, and stay open for his review. Nothing in version 0.1 of this record was decided by Amish. On 2026-09-25 he accepted all recommendations ("i accept all your recommendations, go with them across all repos"); the status column now shows this, and BBX-DDR-002 lists the changes.

## Options considered

The options for each item are in `docs/REVIEW.md` (TRL 2 session) and BBX-PRC-001. They are not repeated here.

## Decision

*Table 1. Items adopted for TRL 3, since decided by Amish (BBX-DDR-002).*

| # | Item | Status | Where it now lives |
| --- | --- | --- | --- |
| A1 | Budget: recommendation (a), raise `budget_usd` from $220 to $250 and keep the bought counterflow core and the CO2 sensor | Decided by Amish, 2026-09-25: go with recommendation. `budget_usd` is now $250 (BBX-DDR-002); the priced BOM is $255, $5 over | BBX-CAL-001 section 9, BBX-REQ-001 R15, `bom/bom.csv` |
| A2 | Window type for the first version: vertical sliding sash | Decided by Amish, 2026-09-25: go with recommendation. Casement and tilt-and-turn inserts are a later variant | BBX-PRC-001 v0.3, BBX-REQ-001 R8, `cad/src/model.py` |
| A3 | Core type: bought polymer counterflow plate core (sensible only) | Decided by Amish, 2026-09-25: go with recommendation | BBX-PRC-001 v0.3, BBX-CAL-001 section 2, `bom/bom.csv` line 2 |
| A4 | Frost strategy: slow the supply fan, with the combustion-appliance warning | Decided by Amish, 2026-09-25: go with recommendation | BBX-PRC-001 v0.3 (Safety), BBX-CAL-001 section 6 |
| A5 | Nominal airflow: 50 m³/h with CO2-driven boost to 70 m³/h | Decided by Amish, 2026-09-25: go with recommendation | BBX-REQ-001 R1, BBX-CAL-001 sections 3 and 4 |
| A6 | Controller: single ESP32-C3 class module with an SCD41 class sensor, with sensor checks on CalRig | Decided by Amish, 2026-09-25: go with recommendation | BBX-PRC-001 v0.3, `bom/bom.csv` line 7 |

The TRL 2 review made no recommendation to change the pitch or problem wording, so `project.yaml` and `README.md` keep them.

### Items that remain open

*Table 2. Open items.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First co-design partner and region (for example a tenants' group or social landlord in the UK or Canada) | Proposed, awaiting Amish. No recommendation was made at TRL 2 |
| O2 | R6 noise shortfall found at TRL 3 (about 39 dB(A) at 50 m³/h against 30 dB(A)) | Decided by Amish, 2026-09-25: go with recommendation (quiet night mode, plus larger fans or a silencer checked against a real fan datasheet before any change to R6). See BBX-DDR-002 |
| O3 | Budget figure: $255 priced against $250 in `project.yaml` (was $220) | Decided by Amish, 2026-09-26: budget set to $255 to cover the priced BOM (BBX-DDR-002) |

## Consequences

- The TRL 3 work is costed and sized for a sash-window unit with a bought counterflow core, two 24 V blowers, a CO2 sensor and a slowed-fan frost mode.
- BBX-CAL-001 shows R6 and R15 not met; neither is resolved by these adoptions.
- The CO2 sensor check depends on CalRig. CalRig's R9 (CO2 span 400 to 2,000 ppm against a reference of ±(30 ppm + 3 %)) covers the 1,000 ppm range BreatheBox needs, and an SCD41 class breakout fits CalRig's 90 x 70 x 50 mm bay (R10). This is consistent with `calrig/docs/REVIEW.md`.
- Amish may reverse any item; the calculations would then be rerun.
