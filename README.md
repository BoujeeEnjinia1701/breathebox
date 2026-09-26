# BreatheBox

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Sustainable Housing · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $220 USD · **Difficulty:** 3 of 5

A window-mounted heat recovery ventilator for single rooms: two small fans and a counterflow core bring in fresh air while recovering most of the heat or cool from the outgoing air.

![BreatheBox concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Concept rationale

Most homes will never get a ducted whole-house ventilation system, but almost every room has a window. BreatheBox puts heat recovery where the fresh air already comes in: a small counterflow core and two small 24 V fans in a box that sits on the sill, with an insulated panel under the raised sash. Room air and outdoor air pass each other on opposite sides of thin plates, so the room gets filtered fresh air at close to room temperature instead of a cold draft. A CO2 sensor runs the fans only as hard as the room needs.

It is open and garage-buildable because the people who most need it (renters, social housing tenants, owners of older homes) are the least served by installer-only products. Apart from the core and the fans, the parts are foam board, filter media and a small controller. The design files let a community repair group or a housing provider build, adapt and fix units locally, and the firmware keeps data on the device.

## Burning platform

People live indoors, and indoor air is often the worse air. The US EPA notes that Americans spend about 90 % of their time indoors and that indoor concentrations of some pollutants are often 2 to 5 times higher than typical outdoor levels ([US EPA](https://www.epa.gov/report-environment/indoor-air-quality)). Opening a window is the usual fix, and it throws heat away: in the European Union, buildings use about 40 % of energy, about 80 % of energy in homes goes to heating, cooling and hot water, and 85 % of buildings were built before 2000 ([European Commission](https://energy.ec.europa.eu/topics/energy-efficiency/energy-performance-buildings/energy-performance-buildings-directive_en)).

The cost of getting this wrong is not only energy. In England, 7 % of social rented homes had a damp problem in 2023, and the death of two-year-old Awaab Ishak from prolonged mould exposure led to a law with fixed deadlines for landlords to fix damp and mould ([UK Government](https://www.gov.uk/government/news/awaabs-law-to-force-landlords-to-fix-dangerous-homes)). Outdoor air needs filtering too: 99 % of the world's population lived where WHO air quality guideline levels were not met in 2019 ([WHO](https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health)).

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Social and rental housing | Fast, reversible fix for damp and stuffy bedrooms without building work |
| Home energy retrofit | Adds controlled ventilation after air sealing and insulation of older homes |
| Student and worker residences | One unit per small room, where windows are often kept shut for noise or security |
| Small offices and consulting rooms | Fresh, filtered air for one or two people in rooms with no mechanical ventilation |
| Assisted living and home care | Steady ventilation for people who cannot easily open and close windows |
| Maker education and repair cafes | Teaching build of airflow, heat transfer and sensing with a useful result |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| Canada | Long, cold heating seasons; Health Canada sets a 1,000 ppm long-term CO2 guideline for homes and names ventilation as the main way to remove CO2 ([Health Canada](https://www.canada.ca/en/health-canada/services/publications/healthy-living/residential-indoor-air-quality-guidelines-carbon-dioxide.html)) |
| United States | Window air conditioners have made sash-window units a familiar renter fix; Americans spend about 90 % of their time indoors ([US EPA](https://www.epa.gov/report-environment/indoor-air-quality)) |
| United Kingdom | Damp and mould in 7 % of social rented homes and new legal deadlines for landlords to fix them ([UK Government](https://www.gov.uk/government/news/awaabs-law-to-force-landlords-to-fix-dangerous-homes)) |
| Germany and the wider EU | 85 % of buildings built before 2000 and 75 % with poor energy performance ([European Commission](https://energy.ec.europa.eu/topics/energy-efficiency/energy-performance-buildings/energy-performance-buildings-directive_en)); tilt-and-turn windows need a different insert |
| India | Filtered supply air for bedrooms kept shut against outdoor pollution; the WHO South-East Asia Region has among the greatest numbers of deaths from ambient air pollution ([WHO](https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health)); an enthalpy core would suit humid heat |
| China | Cold northern winters and polluted outdoor air in one place; the WHO Western Pacific Region also carries among the greatest numbers of those deaths ([WHO](https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health)) |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. It extends the lab's housing and clean tech work. The real-world trigger is the push to fix damp and mould in rented homes, made urgent in England by Awaab's Law ([UK Government](https://www.gov.uk/government/news/awaabs-law-to-force-landlords-to-fix-dangerous-homes)), in homes where tenants cannot add ducts or cut holes in walls.

## Problem

Sealed, efficient homes need ventilation, but opening windows wastes energy and whole-house heat recovery systems are expensive to retrofit.

## Concept

A window-mounted heat recovery ventilator for single rooms: two small fans and a counterflow core bring in fresh air while recovering most of the heat or cool from the outgoing air.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

1. Insulated housing that sits on the window sill
2. Counterflow plate core, about 80 % sensible recovery (estimate)
3. Two 24 V brushless blowers, 30 to 70 m³/h balanced (proposed)
4. ePM1 supply filter and coarse exhaust filter
5. Controller with CO2, humidity and temperature sensing and a frost mode
6. Condensate tray draining outdoors
7. Insulated window insert panel with seals, under the raised and locked sash
8. Two outdoor hoods with insect mesh, a clamped sill bracket and a certified 24 V plug-in adapter

First-order estimates (to be checked at TRL 3): about 270 W of heat kept at 0 °C outdoors for about 9.5 W of fan power, about 10 kg, and about $243 in parts against a $220 budget. See the [design precis](docs/02-concept.md) and [requirements](docs/03-requirements.md), including the requirements not yet met.

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> The unit runs on 24 V from a certified plug-in adapter; do not open the adapter or add mains wiring. Do not use it in a room with an open-flued or unflued fuel-burning appliance, because frost mode extracts more air than it supplies. Lock the raised sash onto the insert panel and never install from outside above ground level. Fan impellers can cut fingers: unplug before opening the lid.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (BBX-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `BBX-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Extending strong areas set.
