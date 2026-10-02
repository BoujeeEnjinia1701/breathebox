---
doc_id: BBX-PRB-001
title: BreatheBox problem statement
project: BreatheBox
doc_type: Problem statement
version: "0.8"
status: Draft
date: '2026-10-02'
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
  change: Populate to TRL 2 (users, context, constraints, prior work, open questions)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update; sash-first window type and budget position per BBX-DDR-001 (adopted for TRL 3, open for Amish's review); open questions updated
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish; constraint now $255
- version: "0.6"
  date: '2026-09-30'
  author: Amish Chadha
  change: Priced BOM of the constructable design ($283, BBX-DDR-003) noted against the $255 constraint
- version: "0.7"
  date: '2026-10-01'
  author: Amish Chadha
  change: BioMedical area (BBX-DEC-001 v0.3); out of scope states a research and educational prototype, not a medical device
- version: "0.8"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Sash lock and first co-design partner decided by Amish on 2026-10-02; ACORN Canada named as the first candidate to approach (BBX-DEC-001)"
---

# BreatheBox problem statement

Most homes have no mechanical ventilation, so the people in them choose between stale, damp air and an open window that throws away heat or cooling. Whole-house heat recovery ventilators solve this in new, airtight buildings, but they need ducts through ceilings and walls, which renters cannot install and owners of older homes rarely pay for. There is no open, low-cost, renter-installable way to ventilate one room with heat recovery.

## Why it matters

People spend most of their lives indoors. The US Environmental Protection Agency notes that Americans spend about 90 % of their time indoors and that indoor concentrations of some pollutants are often 2 to 5 times higher than typical outdoor levels ([US EPA, Report on the Environment: Indoor Air Quality](https://www.epa.gov/report-environment/indoor-air-quality)). Bedrooms are the worst case: two people sleep for eight hours behind a closed door and a closed window.

Energy is the other half of the problem. In the European Union, buildings use about 40 % of energy, about 80 % of the energy used in homes goes to heating, cooling and hot water, and 85 % of buildings were built before 2000 ([European Commission, Energy Performance of Buildings Directive](https://energy.ec.europa.eu/topics/energy-efficiency/energy-performance-buildings/energy-performance-buildings-directive_en)). As these homes are sealed and insulated, air leakage falls and moisture and CO2 build up unless ventilation is added. In England, 7 % of social rented homes had a damp problem in 2023, and the death of two-year-old Awaab Ishak in 2020 after prolonged exposure to mould led to a law that sets deadlines for landlords to fix damp and mould hazards ([UK Government, Awaab's Law](https://www.gov.uk/government/news/awaabs-law-to-force-landlords-to-fix-dangerous-homes)).

Outdoor air is not always clean either. The World Health Organization reports that 99 % of the world's population lived in places where its air quality guideline levels were not met in 2019 ([WHO, Ambient air quality and health](https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health)). An open window brings that air in unfiltered; a ventilator can filter it.

## Users and context

| User | Situation | What they need |
| --- | --- | --- |
| Renters in older flats and houses | Cannot drill, duct or change the building; often have one problem room (a bedroom or a small flat's main room) | A unit that goes into an existing window and comes out again without damage |
| Owners of older, poorly ventilated homes | Condensation and mould on cold walls; high heating bills; no budget for a whole-house system | Continuous fresh air to one or two rooms at low running cost |
| Households in polluted cities | Windows kept shut against traffic or smoke; stuffy bedrooms | Filtered supply air and a visible CO2 reading |
| Social housing providers and energy retrofit programs | Must fix damp and mould quickly across many homes | A low-cost, repeatable, documented measure that installs in minutes |
| Makers and community repair groups | Want to build, adapt and fix the unit locally | Open drawings, common parts and no special tools |

**Operating context.** One room of 20 to 40 m³ (for example, a 3 x 4 m bedroom with a 2.5 m ceiling holds 30 m³), one or two occupants, a window with a sill 800 to 1,000 mm above the floor, and a standard wall socket nearby. Outdoor air from about -10 °C to 35 °C. The first target window is the vertical sliding sash (single- or double-hung) common in North America and the United Kingdom, because the lower sash can close down onto an insert panel. This sash-first choice was decided by Amish on 2026-09-25 (BBX-DDR-001 item A2; BBX-DDR-002).

## Constraints

- Garage-buildable prototype, $255 USD in parts (`project.yaml`; raised from $220 to $250 by Amish on 2026-09-25 and to $255 on 2026-09-26, BBX-DDR-002). The priced BOM of the constructable design is $283 (BBX-CAL-001 v0.4, BBX-DDR-003); a $283 budget is proposed, awaiting Amish.
- No drilling of the window frame or wall; installs and removes without damage, so renters can use it.
- Low voltage only inside the unit (24 V SELV from a certified plug-in adapter); no mains wiring by the builder.
- Common, replaceable parts: standard fans, filter media cut to size, a spare-part HRV core.
- Quiet enough for a bedroom at night.
- Open licenses: CERN-OHL-S-2.0 for hardware, MIT for firmware and scripts.

## Out of scope

- Whole-house ventilation, ducted systems and replacement of building code ventilation.
- Heating or cooling the room (the unit recovers heat; it does not add it beyond fan heat).
- Kitchen and bathroom extraction, which need higher extract rates, and removal of combustion products from stoves or open-flued appliances.
- Medical or health claims. BreatheBox is a research and educational prototype, not a medical device. The CO2 display is an indicator of ventilation, not a health measurement.

## Prior work

- **Decentralized single-room ventilators.** Commercial through-wall units exist, for example the LUNOS e² family of small decentralized fans with heat recovery ([LUNOS, heat recovery products](https://www.lunos.de/en/heat-recovery)). The LUNOS page, checked on 2026-09-25, describes the e² as one of the smallest decentralized fans but does not state how it is installed. Through-wall units of this kind need an opening in the wall, which renters generally cannot make.
- **Plate heat exchangers.** Fixed-plate exchangers reach 70 to 90 % sensible efficiency at low pressure drop, but have a high chance of frosting in cold climates ([Wikipedia, Heat recovery ventilation](https://en.wikipedia.org/wiki/Heat_recovery_ventilation)). BreatheBox uses a plate counterflow core and needs a frost strategy.
- **Window air conditioners and window fans** show that a sash window with a filler panel is a familiar, renter-friendly mounting. They move air or heat but do not recover heat from exhaust air.
- **CO2 as a ventilation indicator.** Health Canada's residential guideline sets a long-term exposure limit of 1,000 ppm CO2 (24-hour average) and notes that ventilation is the primary means of removing CO2 indoors ([Health Canada, Residential indoor air quality guidelines: carbon dioxide](https://www.canada.ca/en/health-canada/services/publications/healthy-living/residential-indoor-air-quality-guidelines-carbon-dioxide.html)).

We have not found an open-source, window-mounted, counterflow heat recovery ventilator with published design files. This is a finding from a limited search and should be checked at TRL 3.

## Open questions

- [ ] Which windows dominate in the first user group? The first version targets sash windows (BBX-DDR-001 item A2); casement and tilt-and-turn windows (common in continental Europe) need a later insert.
- [x] Is a 260 mm raised sash acceptable for security, or is a locking bar needed as standard? Decided 2026-10-02: a bought no-drill sash jammer or adjustable security bar in the inner track is part of the kit (BBX-DEC-001).
- [ ] What noise level do users accept at night, and at what airflow? BBX-CAL-001 estimates about 39 dB(A) at 1 m at 50 m³/h and 30 dB(A) only near 32 m³/h, A quiet night mode at 32 m³/h (about 30 dB(A), BBX-DDR-002) is now part of the design, so the open part is whether users accept it and its overnight CO2 of about 1,300 ppm.
- [ ] How cold does it get where the first users live, and how often will the frost strategy run?
- [x] Who are the first co-design partners (a tenants' group, a social landlord or a retrofit program)? Decided 2026-10-02: Canada first, with a tenant organization in a city with older double-hung rental stock and cold winters. The first candidate to approach is ACORN Canada in Toronto, with ACORN in the United Kingdom as the alternative; nothing is agreed with either (BBX-DEC-001).
