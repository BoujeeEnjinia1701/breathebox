"""BreatheBox concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. X is depth through the wall (outdoors negative, room positive),
Y runs along the window width, Z is up with the room floor at Z = 0. The wall,
window and floor are grey context with no BOM number; kit parts are colored.
The unit sits on the sill of a vertical sliding (sash or single-hung) window whose
lower sash is raised and closed down onto the window insert panel.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all

WALL_T = 250.0            # wall thickness, outer face at X = -250, inner face at X = 0
SILL_Z = 900.0            # window sill height above the floor
OPEN_W = 1000.0           # clear window opening width
OPEN_H = 1200.0           # clear window opening height
PANEL_H = 260.0           # insert panel height (lower sash rests on top)

GREY = "#B8BEC6"
GLASS = "#BFD7E6"


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max coordinates."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def tube3(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


# ---------------- context: wall with window, floor (grey, no BOM number) ----------------
wall = box(-WALL_T, 0, -900, 900, 0, 2500) - box(-WALL_T - 1, 1, -OPEN_W / 2, OPEN_W / 2, SILL_Z, SILL_Z + OPEN_H)
floor = box(-WALL_T, 1700, -900, 900, -40, 0)
frame = (box(-190, -110, -OPEN_W / 2, OPEN_W / 2, SILL_Z + OPEN_H - 40, SILL_Z + OPEN_H)
         + box(-190, -110, -OPEN_W / 2, -OPEN_W / 2 + 40, SILL_Z, SILL_Z + OPEN_H)
         + box(-190, -110, OPEN_W / 2 - 40, OPEN_W / 2, SILL_Z, SILL_Z + OPEN_H))
# lower sash raised to sit on the insert panel; upper sash fixed
lo_z0 = SILL_Z + PANEL_H
lower_sash = (box(-150, -115, -460, 460, lo_z0, lo_z0 + 560) - box(-151, -114, -420, 420, lo_z0 + 40, lo_z0 + 520))
lower_glass = box(-136, -129, -420, 420, lo_z0 + 40, lo_z0 + 520)
upper_sash = (box(-185, -150, -460, 460, SILL_Z + 620, SILL_Z + 1160) - box(-186, -149, -420, 420, SILL_Z + 660, SILL_Z + 1120))
upper_glass = box(-171, -164, -420, 420, SILL_Z + 660, SILL_Z + 1120)

# ---------------- kit parts ----------------
# 1 Housing: insulated shell sitting on the sill, projecting 360 mm into the room
HX0, HX1, HY, HZ0, HZ1 = -110.0, 360.0, 280.0, SILL_Z, SILL_Z + 250.0
housing = box(HX0, HX1, -HY, HY, HZ0, HZ1) - box(HX0 + 8, HX1 - 8, -HY + 8, HY - 8, HZ0 + 8, HZ1 - 8)
housing = housing - box(HX1 - 9, HX1 + 1, -260, -20, 925, 1135)          # exhaust intake opening (front)
housing = housing - box(240, 330, 40, 180, HZ1 - 9, HZ1 + 1)             # supply outlet grille (top)
for y0 in (-260, 40):                                                    # outdoor-end ports to the hoods
    housing = housing - box(HX0 - 1, HX0 + 9, y0, y0 + 220, 935, 1105)

# 2 Counterflow core, 300 mm long along X, 180 x 180 mm section
core = box(-90, 210, -90, 90, 930, 1110)

# 3 Supply fan and 4 exhaust fan: EC centrifugal blowers in the room-end plenum
supply_fan = Pos(280, 110, 1040) * Cylinder(55, 70)
exhaust_fan = Pos(280, -110, 1040) * Cylinder(55, 70)

# 5 Supply filter (ePM1 class) on the outdoor end of the supply half of the core
supply_filter = box(-100, -92, 5, 88, 932, 1108)

# 6 Exhaust filter (coarse) behind the front intake opening
exhaust_filter = box(338, 350, -255, -25, 930, 1130)

# 7 Controller with CO2, humidity and temperature sensing, near the room intake
controller = box(225, 345, -15, 35, 1118, 1138) + box(300, 330, -10, 20, 1100, 1118)

# 8 Condensate tray under the core with a drain tube out through the panel and down the wall
tray = box(-100, 220, -100, 100, 910, 926) - box(-92, 212, -92, 92, 915, 927)
drain = (tube3((-100, 0, 914), (-300, 0, 914), 6) + tube3((-300, 0, 914), (-300, 0, 600), 6))

# 9 Window insert panel with edge seals, filling the gap under the raised lower sash
panel = box(-150, -120, -OPEN_W / 2 + 40, OPEN_W / 2 - 40, SILL_Z, SILL_Z + PANEL_H)
for yc in (-150, 150):
    panel = panel - box(-151, -119, yc - 110, yc + 110, 935, 1105)

# 10 Outdoor hoods with insect mesh, supply intake and exhaust outlet kept apart, plus short ducts
hoods = None
for yc in (-300, 300):
    h = box(-330, -150, yc - 90, yc + 90, 925, 1115) - box(-322, -149, yc - 82, yc + 82, 925 - 1, 1107)
    hoods = h if hoods is None else hoods + h
ducts = None
for y_hood, y_port in ((-300, -150), (300, 150)):
    d = box(-150, HX0, min(y_hood, y_port) - 60, max(y_hood, y_port) + 60, 945, 1095) \
        - box(-151, HX0 + 1, min(y_hood, y_port) - 52, max(y_hood, y_port) + 52, 953, 1087)
    ducts = d if ducts is None else ducts + d

# 11 Sill support bracket: plate under the overhang and a strut to the wall
bracket = (box(0, 340, -200, 200, SILL_Z - 10, SILL_Z)
           + tube3((5, -170, 640), (320, -170, SILL_Z - 10), 10)
           + tube3((5, 170, 640), (320, 170, SILL_Z - 10), 10)
           + box(0, 8, -200, 200, 610, 680))

# 12 24 V plug-in power supply at a wall socket, low-voltage cable to the unit
psu = box(0, 45, 520, 590, 300, 380)
cable = (tube3((45, 555, 340), (60, 555, 340), 3) + tube3((60, 555, 340), (60, 300, 880), 3)
         + tube3((60, 300, 880), (60, 283, 1000), 3))

parts = [
    Part("Wall with window opening", wall, "#D6D3CE", None),
    Part("Window frame", frame, GREY, None),
    Part("Lower sash (raised)", lower_sash, "#E5E7EB", None),
    Part("Lower sash glass", lower_glass, GLASS, None),
    Part("Upper sash", upper_sash, "#E5E7EB", None),
    Part("Upper sash glass", upper_glass, GLASS, None),
    Part("Insulated housing", housing, "#E7F0EE", 1, (250, 0, 720)),
    Part("Counterflow core", core, "#D4A017", 2, (0, 0, 260)),
    Part("Supply fan, EC", supply_fan, "#0F766E", 3, (160, 260, 300)),
    Part("Exhaust fan, EC", exhaust_fan, "#C2410C", 4, (160, -260, 300)),
    Part("Supply filter, ePM1", supply_filter, "#2563EB", 5, (-60, -420, 380)),
    Part("Exhaust filter, coarse", exhaust_filter, "#94A3B8", 6, (300, -140, 120)),
    Part("Controller, CO2 and RH", controller, "#7C3AED", 7, (200, 0, 470)),
    Part("Condensate tray and drain", tray + drain, "#0EA5E9", 8, (0, 0, -220)),
    Part("Window insert panel", panel, "#A7C4BC", 9, (-280, 0, -60)),
    Part("Outdoor hoods and ducts", hoods + ducts, "#475569", 10, (-520, -150, -560)),
    Part("Sill bracket", bracket, "#6B7280", 11, (200, 0, -300)),
    Part("24 V power supply", psu + cable, "#111827", 12, (250, 250, -150)),
]

FLOOR = Part("Room floor", floor, "#CFC8BD", None)

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
        key_figures=["Balanced 30 to 70 m3/h, 50 m3/h nominal (proposed)",
                     "Counterflow core, about 80 % sensible recovery at 50 m3/h (estimate)",
                     "About 270 W recovered at 0 °C out, 20 °C in (estimate)",
                     "About 9.5 W fans and controls, 24 V SELV (estimate)",
                     "Parts about $243 against $220 budget (indicative)"],
        cut_exclude=CONTEXT + ["Sill bracket", "24 V power supply"],
        context=[FLOOR],
        flow={"title": "heat flow at 0 °C outdoor, 20 °C indoor, 50 m³/h (estimates)", "unit": "W",
              "stages": [("Stale room air out", 335), ("Recovered in core", 268),
                         ("Fresh air in, about 16 °C", 268)],
              "losses": [(0, "Leaves with exhaust air", 67)]},
    )
