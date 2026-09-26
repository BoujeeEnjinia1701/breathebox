"""BreatheBox concept media (TRL 3), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. X is depth through the wall (outdoors negative, room positive),
Y runs along the window width, Z is up with the room floor at Z = 0. Geometry comes
from cad/src/model.py, so the media match the STEP files and drawing BBX-DWG-001.
The wall, window and floor are grey context with no BOM number. Figures are printed by
docs/04-calcs/sizing.py (BBX-CAL-001).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from concept import Part, render_all
from model import build_parts, context_parts

GREY = "#B8BEC6"
GLASS = "#BFD7E6"

ctx = context_parts()
parts = [
    Part("Wall with window opening", ctx["wall"], "#D6D3CE", None),
    Part("Window frame", ctx["frame"], GREY, None),
    Part("Lower sash (raised)", ctx["lower_sash"], "#E5E7EB", None),
    Part("Lower sash glass", ctx["lower_glass"], GLASS, None),
    Part("Upper sash", ctx["upper_sash"], "#E5E7EB", None),
    Part("Upper sash glass", ctx["upper_glass"], GLASS, None),
] + [Part(n, shape, colour, bom, ex) for n, shape, colour, bom, ex in build_parts()]

FLOOR = Part("Room floor", ctx["floor"], "#CFC8BD", None)

CONTEXT = ["Wall with window opening", "Window frame", "Lower sash (raised)", "Lower sash glass",
           "Upper sash", "Upper sash glass"]

if __name__ == "__main__":
    import concept
    # the exploded view shows kit parts only, so the wall does not hide them
    _orig = concept._render

    def _render(ps, out, *a, **k):
        if k.get("offsets"):
            ps = [p for p in ps if p.name not in CONTEXT]
        return _orig(ps, out, *a, **k)
    concept._render = _render

    render_all(
        parts, project="BreatheBox", title="Window heat recovery ventilator concept", dwg_no="BBX-DWG-010",
        date="2026-09-25",
        key_figures=["Balanced 30 to 70 m3/h, 50 m3/h nominal (BBX-CAL-001)",
                     "Counterflow core, about 80 % sensible recovery at 50 m3/h (est.)",
                     "About 267 W recovered at 0 °C out, 20 °C in (est.)",
                     "About 5.6 W fans and controls at 50 m3/h, 24 V SELV (est.)",
                     "About 39 dB(A) at 1 m at 50 m3/h, 30 in night mode: R6 not met (est.)",
                     "Parts $255 against $250 budget: R15 not met"],
        cut_exclude=CONTEXT + ["Sill bracket", "24 V power supply"],
        context=[FLOOR],
        flow={"title": "heat flow at 0 °C outdoor, 20 °C indoor, 50 m³/h (estimates, BBX-CAL-001)", "unit": "W",
              "stages": [("Stale room air out", 335), ("Recovered in core", 267),
                         ("Fresh air in, about 16 °C", 267)],
              "losses": [(0, "Leaves with exhaust air", 68)]},
    )
