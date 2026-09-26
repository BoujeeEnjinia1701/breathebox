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

### Proposed, awaiting Amish

1. **Budget.** Options: (a) raise `budget_usd` from $220 to $250; (b) keep $220 by using a home-made crossflow core (about $10, but only about 50 to 65 % recovery, which fails R2); (c) keep $220 by dropping the CO2 sensor for humidity-only control (about $20 saved, weakens R4). Recommendation: (a). `project.yaml` is unchanged.
2. **Window type for the first version:** vertical sliding sash (recommended) versus a tilt-and-turn insert for continental Europe.
3. **Core type:** bought polymer counterflow plate core (recommended) versus alternating regenerative units or an enthalpy core for humid climates.
4. **Frost strategy:** slow the supply fan (recommended, with the combustion-appliance warning) versus a low-power preheater.
5. **Nominal airflow:** 50 m³/h with CO2-driven boost to 70 m³/h (recommended) versus 70 m³/h fixed.
6. **Controller:** single ESP32-C3 class module with an SCD41 class sensor (recommended), with sensor checks on CalRig.
7. **First co-design partner and region** (for example a tenants' group or social landlord in the UK or Canada).

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
