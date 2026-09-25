# BreatheBox

**Area:** Sustainable Housing · **Status:** Concept · **Prototype budget:** about $220 USD · **Difficulty:** 3 of 5

A window-mounted heat recovery ventilator for single rooms: two small fans and a counterflow core bring in fresh air while recovering most of the heat or cool from the outgoing air.

## Concept rationale

Room-by-room heat recovery gives renters and older homes clean air without large energy penalties or construction work.

## Burning platform

Indoor air quality and energy costs are both rising concerns, and most homes have no mechanical ventilation.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. It extends the lab's housing and clean tech work.

## Problem

Sealed, efficient homes need ventilation, but opening windows wastes energy and whole-house heat recovery systems are expensive to retrofit.

## Concept

A window-mounted heat recovery ventilator for single rooms: two small fans and a counterflow core bring in fresh air while recovering most of the heat or cool from the outgoing air.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Counterflow heat exchanger core
- Two EC fans
- Window insert panel
- Filters for supply air
- CO2 and humidity sensor with controller
- Condensate drain

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Mains wiring must be done or checked by a qualified electrician and follow local electrical code.

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

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Extending strong areas set.
