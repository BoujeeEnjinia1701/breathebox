"""BreatheBox parametric model (build123d), TRL 3.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl, prints the main envelopes and runs a
clash check between the unit parts.

Massing-plus detail: correct interfaces (window insert panel, sash seat, outdoor hoods
with their 420 mm mouth separation, housing ports, core faces, filters, fans, tray and
drain, sill bracket) and main dimensions; not fabrication detail.

Axes: X is depth through the wall (outdoors negative, room positive; the inner wall face
is X = 0), Y runs along the window width (supply side +Y, exhaust side -Y), Z is up with
the room floor at Z = 0. Units mm. The unit sits on the sill of a vertical sliding sash
window; the lower sash is raised and closed down onto the insert panel.
"""
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Window and wall (context; design case in BBX-REQ-001)
    "wall_t": 250.0, "sill_z": 900.0,
    "open_w": 900.0,            # clear width between the jambs (R8 range 700 to 1000)
    "open_h": 1200.0,
    # Window insert panel (item 9)
    "panel_x0": -150.0, "panel_t": 20.0, "panel_h": 260.0, "seal": 3.0,
    # Housing (item 1): shell plus lining
    "hx0": -110.0, "hx1": 400.0, "hw": 560.0, "hh": 250.0,
    "shell_t": 6.0, "lining_t": 10.0,
    # Counterflow core (item 2)
    "core_x0": -40.0, "core_l": 300.0, "core_w": 180.0, "core_h": 180.0, "core_z0": 930.0,
    "plate_pitch": 2.5, "plate_t": 0.15,
    # Outdoor-end ports, filters and collars
    "port_yc": 185.0, "port_w": 150.0, "port_h": 170.0, "port_z0": 935.0,
    "sfilter_t": 25.0,          # supply filter (item 5), same face as the port
    "efilter_w": 220.0, "efilter_h": 190.0, "efilter_t": 12.0,   # exhaust filter (item 6)
    # Outdoor hoods (item 10): body from the port outward, mouth at the outer end
    "hood_d": 180.0, "hood_y_out": 340.0, "mouth_w": 130.0, "hood_z0": 925.0, "hood_z1": 1115.0,
    "hood_t": 3.0,
    # Fans (items 3 and 4): 120 x 120 x 32 mm class centrifugal blowers
    "fan_x0": 280.0, "fan_t": 32.0, "fan_s": 120.0, "fan_yc": 150.0, "fan_z0": 950.0,
    # Room-side grilles
    "sgrille": (290.0, 380.0, 60.0, 250.0),      # top supply outlet: x0, x1, y0, y1
    "egrille": (-250.0, -30.0, 930.0, 1120.0),   # front exhaust intake: y0, y1, z0, z1
    # Sill bracket (item 11)
    "bracket_t": 4.0, "bracket_w": 400.0, "bracket_x1": 390.0, "foot_z": 650.0,
    "strut_r": 10.0, "strut_wall": 1.5,
}


def _box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _tube(a, b, r, r_in=0.0):
    from build123d import Plane, Solid, Vector
    a = Vector(*a); b = Vector(*b); d = b - a
    pl = Plane(origin=a, z_dir=d.normalized())
    s = Solid.make_cylinder(r, d.length, pl)
    if r_in > 0:
        s = s - Solid.make_cylinder(r_in, d.length, pl)
    return s


def derived(p=PARAMS):
    """Dimensions derived from the parameters, shared with the calculation note."""
    w = p["shell_t"] + p["lining_t"]
    d = {
        "housing_wall": w,
        "inner": (p["hx0"] + w, p["hx1"] - w, -p["hw"] / 2 + w, p["hw"] / 2 - w,
                  p["sill_z"] + w, p["sill_z"] + p["hh"] - w),
        "port_y": (p["port_yc"] - p["port_w"] / 2, p["port_yc"] + p["port_w"] / 2),
        "mouth_y": (p["hood_y_out"] - p["mouth_w"], p["hood_y_out"]),
        "panel_half": p["open_w"] / 2 - p["seal"],
    }
    d["mouth_clear"] = 2 * d["mouth_y"][0]
    d["core_x1"] = p["core_x0"] + p["core_l"]
    return d


def build_parts(p=PARAMS):
    """Return [(name, shape, colour, bom_no, explode_offset)] for the unit (items 1 to 12)."""
    d = derived(p)
    S = p["sill_z"]
    x0, x1, hy, z1 = p["hx0"], p["hx1"], p["hw"] / 2, S + p["hh"]
    ix0, ix1, iy0, iy1, iz0, iz1 = d["inner"]
    py0, py1 = d["port_y"]
    pz0, pz1 = p["port_z0"], p["port_z0"] + p["port_h"]
    cx0, cx1 = p["core_x0"], d["core_x1"]
    cz0, cz1 = p["core_z0"], p["core_z0"] + p["core_h"]

    # 1 Housing: shell with lining (one solid), dividers and openings
    housing = _box(x0, x1, -hy, hy, S, z1) - _box(ix0, ix1, iy0, iy1, iz0, iz1)
    housing = housing + _box(ix0, cx0, -4, 4, cz0, iz1)                      # outdoor plenum divider
    housing = housing + _box(cx1, ix1 - p["efilter_t"] - 6, -4, 4, cz0, 1100)  # room plenum divider
    for s in (1, -1):                                                        # outdoor-end ports
        ya, yb = sorted((s * py0, s * py1))
        housing = housing - _box(x0 - 1, ix0 + 1, ya, yb, pz0, pz1)
    ey0, ey1, ez0, ez1 = p["egrille"]
    housing = housing - _box(ix1 - 1, x1 + 1, ey0, ey1, ez0, ez1)            # exhaust intake grille
    gx0, gx1, gy0, gy1 = p["sgrille"]
    housing = housing - _box(gx0, gx1, gy0, gy1, iz1 - 1, z1 + 1)            # supply outlet grille
    housing = housing - _tube((x0 - 1, 0, 923), (ix0 + 1, 0, 923), 7)       # drain pass-through

    # 2 Counterflow core
    core = _box(cx0, cx1, -p["core_w"] / 2, p["core_w"] / 2, cz0, cz1)

    # 3 Supply fan (+Y) and 4 exhaust fan (-Y): blower bodies with inlet rings
    def blower(yc):
        body = _box(p["fan_x0"], p["fan_x0"] + p["fan_t"], yc - p["fan_s"] / 2, yc + p["fan_s"] / 2,
                    p["fan_z0"], p["fan_z0"] + p["fan_s"])
        ring = _tube((p["fan_x0"] - 8, yc, p["fan_z0"] + 60), (p["fan_x0"], yc, p["fan_z0"] + 60), 40, 34)
        return body + ring
    supply_fan = blower(p["fan_yc"])
    exhaust_fan = blower(-p["fan_yc"])

    # 5 Supply filter behind the supply port; 6 exhaust filter behind the front grille
    supply_filter = _box(ix0 + 6, ix0 + 6 + p["sfilter_t"], py0, py1, pz0, pz1)
    ef_x1 = ix1 - 2
    exhaust_filter = _box(ef_x1 - p["efilter_t"], ef_x1, ey0, ey1, ez0 - 5, ez1 + 5)

    # 7 Controller with CO2 sensor, above the room plenum divider
    controller = _box(300, 372, -30, 30, 1108, 1126) + _box(368, 382, -12, 12, 1090, 1108)

    # 8 Condensate tray with drain tube out through the housing, panel and down the wall
    tray = _box(cx0 - 10, cx1 + 10, -100, 100, iz0, cz0) - _box(cx0 - 8, cx1 + 8, -98, 98, iz0 + 2, cz0 + 1)
    drain = (_tube((cx0 - 10, 0, 923), (-300, 0, 923), 6, 4)
             + _tube((-300, 0, 923), (-300, 0, 700), 6, 4))

    # 9 Window insert panel with port and drain cut-outs
    ph = d["panel_half"]
    px0, px1 = p["panel_x0"], p["panel_x0"] + p["panel_t"]
    panel = _box(px0, px1, -ph, ph, S, S + p["panel_h"])
    for s in (1, -1):
        ya, yb = sorted((s * (py0 - 3), s * (py1 + 3)))
        panel = panel - _box(px0 - 1, px1 + 1, ya, yb, pz0 - 3, pz1 + 3)
    panel = panel - _tube((px0 - 1, 0, 923), (px1 + 1, 0, 923), 7)

    # 10 Outdoor hoods (mouth faces down at the outer end) and collars through the panel
    t = p["hood_t"]
    hx_out = px0 - p["hood_d"]
    hoods = None
    for s in (1, -1):
        ya, yb = sorted((s * (py0 - 3), s * p["hood_y_out"]))
        h = _box(hx_out, px0, ya, yb, p["hood_z0"], p["hood_z1"])
        h = h - _box(hx_out + t, px0 + 1, ya + t, yb - t, p["hood_z0"] + t, p["hood_z1"] - t)
        my0, my1 = sorted((s * d["mouth_y"][0], s * d["mouth_y"][1]))
        h = h - _box(hx_out + t, px0 - t, my0 + t, my1 - t, p["hood_z0"] - 1, p["hood_z0"] + t + 1)
        pa, pb = sorted((s * py0, s * py1))
        collar = _box(px0 - 1, x0, pa - t, pb + t, pz0 - t, pz1 + t) - _box(px0 - 2, x0 + 1, pa, pb, pz0, pz1)
        h = h + collar
        hoods = h if hoods is None else hoods + h

    # 11 Sill bracket: plate under the room-side overhang, two tubular struts, padded wall foot
    bw = p["bracket_w"] / 2
    bracket = (_box(0, p["bracket_x1"], -bw, bw, S - p["bracket_t"], S)
               + _tube((8, -170, p["foot_z"]), (p["bracket_x1"] - 20, -170, S - p["bracket_t"] - 10), p["strut_r"], p["strut_r"] - p["strut_wall"])
               + _tube((8, 170, p["foot_z"]), (p["bracket_x1"] - 20, 170, S - p["bracket_t"] - 10), p["strut_r"], p["strut_r"] - p["strut_wall"])
               + _box(0, 8, -bw, bw, p["foot_z"] - 30, p["foot_z"] + 30))

    # 12 24 V plug-in adapter at a wall socket, low-voltage cable to the unit
    psu = _box(0, 45, 520, 590, 300, 380)
    cable = (_tube((45, 555, 340), (60, 555, 340), 3) + _tube((60, 555, 340), (60, 300, 880), 3)
             + _tube((60, 300, 880), (60, 286, 1000), 3))

    return [
        ("Insulated housing", housing, "#E7F0EE", 1, (250, 0, 720)),
        ("Counterflow core", core, "#D4A017", 2, (0, 0, 300)),
        ("Supply fan, EC", supply_fan, "#0F766E", 3, (180, 300, 330)),
        ("Exhaust fan, EC", exhaust_fan, "#C2410C", 4, (180, -300, 330)),
        ("Supply filter, ePM1", supply_filter, "#2563EB", 5, (-60, -200, 520)),
        ("Exhaust filter, coarse", exhaust_filter, "#94A3B8", 6, (320, -140, 140)),
        ("Controller, CO2 and RH", controller, "#7C3AED", 7, (200, 0, 480)),
        ("Condensate tray and drain", tray + drain, "#0EA5E9", 8, (0, 0, -240)),
        ("Window insert panel", panel, "#A7C4BC", 9, (-300, 0, -60)),
        ("Outdoor hoods and collars", hoods, "#475569", 10, (-560, 0, -520)),
        ("Sill bracket", bracket, "#6B7280", 11, (200, 0, -320)),
        ("24 V power supply", psu + cable, "#111827", 12, (250, 250, -150)),
    ]


def context_parts(p=PARAMS):
    """Grey context with no BOM number: wall with window opening, frame, sashes and floor."""
    S, W, H, T = p["sill_z"], p["open_w"], p["open_h"], p["wall_t"]
    jw = 40.0
    wall = _box(-T, 0, -900, 900, 0, 2500) - _box(-T - 1, 1, -W / 2 - jw, W / 2 + jw, S, S + H)
    frame = (_box(-190, -110, -W / 2 - jw, W / 2 + jw, S + H - 40, S + H)
             + _box(-190, -110, -W / 2 - jw, -W / 2, S, S + H)
             + _box(-190, -110, W / 2, W / 2 + jw, S, S + H))
    lo = S + p["panel_h"]
    lower_sash = _box(-150, -115, -W / 2, W / 2, lo, lo + 560) - _box(-151, -114, -W / 2 + 40, W / 2 - 40, lo + 40, lo + 520)
    lower_glass = _box(-136, -129, -W / 2 + 40, W / 2 - 40, lo + 40, lo + 520)
    upper_sash = _box(-185, -150, -W / 2, W / 2, S + 620, S + 1160) - _box(-186, -149, -W / 2 + 40, W / 2 - 40, S + 660, S + 1120)
    upper_glass = _box(-171, -164, -W / 2 + 40, W / 2 - 40, S + 660, S + 1120)
    floor = _box(-T, 1700, -900, 900, -40, 0)
    return {"wall": wall, "frame": frame, "lower_sash": lower_sash, "lower_glass": lower_glass,
            "upper_sash": upper_sash, "upper_glass": upper_glass, "floor": floor}


def assemblies(parts=None):
    from build123d import Compound
    parts = parts or build_parts()
    by = {bom: s for _, s, _, bom, _ in parts}
    unit = [s for _, s, _, bom, _ in parts if bom != 12]
    return {
        "breathebox-assembly": Compound(unit),
        "breathebox-housing": by[1],
        "breathebox-core": by[2],
        "breathebox-insert-panel": by[9],
        "breathebox-hoods": by[10],
        "breathebox-sill-bracket": by[11],
    }


if __name__ == "__main__":
    from build123d import export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    for name, shape in assemblies(parts).items():
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"))
        bb = shape.bounding_box()
        print(f"{name:26s} {bb.size.X:6.1f} x {bb.size.Y:6.1f} x {bb.size.Z:6.1f} mm")
    worst = 0.0
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            v = (parts[i][1] & parts[j][1]).volume
            if v > 1.0:
                print(f"clash {parts[i][0]} / {parts[j][0]}: {v:.0f} mm3")
                worst = max(worst, v)
    print("clash check: none" if worst == 0 else "clash check: see above")
    d = derived()
    print(f"hood mouth clear distance {d['mouth_clear']:.0f} mm; hood outer edge +/-{PARAMS['hood_y_out']:.0f} mm; "
          f"panel half-length {d['panel_half']:.0f} mm")
