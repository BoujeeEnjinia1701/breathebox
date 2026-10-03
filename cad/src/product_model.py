"""BreatheBox product appearance model (build123d), TRL 3, constructable design.

Finished-product look for photoreal renders, built on the components of cad/src/model.py as they
are made (BBX-DDR-003), so every main dimension and position comes from the model: the PVC foam
board housing with softened outer edges, the top-board lid with two toggle latches (decided
2026-10-02), the slotted aluminium exhaust grille on the room face and supply grille in the lid,
the status light and button on the room face (decided 2026-10-02), the foam lining, core frames,
dividers and fan bulkhead, the plate core on its tray, two black blowers on the bulkhead (supply
on its room side, exhaust on its core side), the filters in their seats, the controller on the
room-side divider, the window insert panel with EPDM end seals, flanged collars, hoods on their
back plates with stainless mesh and M5 bolts, the sill bracket (rails, angle cleats, flattened-end
struts, padded wall foot 400 mm above the floor), the cable gland, the 24 V plug-in adapter and the
bought sash jammer. Context is a compact section of wall with the window frame and the raised
lower sash, cropped around the unit.

Render-only departures from model.py (REVIEW.md, Proposed, awaiting Amish): a clear inspection
window in the lid and a matching opening in the lid's foam lining, so the core, exhaust fan and
controller show (decided 2026-10-02: clear lid in the renders only; the prototype lid is opaque);
4 mm rounds on the housing's vertical edges and 2 mm on the lid; a name plate and rating label.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Axes as model.py: X is depth through the wall (outdoors negative, room positive, inner wall face
at X = 0), Y along the window width (supply side +Y, exhaust side -Y), Z up with the room floor
at Z = 0. Units mm.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import Axis, Box, Compound, Cylinder, Plane, Pos, Rot, Solid, Sphere, Vector, fillet
from model import PARAMS, derived, context_parts, build_components

TITLE = "BreatheBox: window-mounted heat recovery ventilator for one room"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": 40,
     "note": "Product render from the room side, front right and above (about 30 deg elevation); unit on "
             "the sill of a sash window, counterflow core and exhaust fan seen through a clear lid window "
             "(renders only; the prototype lid is opaque)"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": 35,
     "note": "Exploded view from the room side, front right and above (about 28 deg elevation): top-board "
             "lid with toggle latches, counterflow core, two fans, filters, controller, tray, housing, insert "
             "panel, collars and outdoor hoods, sill bracket, 24 V adapter and sash jammer"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 48, "az": 25,
     "note": "Detail view from the room side and above (about 48 deg elevation), without the wall: "
             "counterflow core, exhaust fan and controller through the clear lid window (renders only)"},
]

# Colours (restrained product palette; kit accent for the button and name plate)
C_SHELL = "#ECECE8"
C_LID = "#F3F3F0"
C_GRILLE = "#3A3F45"
C_DARK = "#24282D"
C_ACCENT = "#0F766E"
C_LINING = "#80868C"
C_CORE = "#D9E1DE"
C_RAIL = "#2F3439"
C_FAN = "#1F2328"
C_IMPELLER = "#40464D"
C_METAL = "#B8BEC6"
C_ALU = "#C9CED3"
C_MESH = "#8E949B"
C_PCB = "#166534"
C_CHIP = "#111827"
C_LABEL = "#F4F4F2"
C_FILTER = "#F2F3F0"
C_FRAME = "#D8CFBF"
C_PAD = "#9AA0A6"
C_TRAY = "#BFD6D8"
C_TUBE = "#E3E6E4"
C_PANEL = "#DCDFDB"
C_HOOD = "#4B535C"
C_RUBBER = "#1C1F23"
C_LED = "#34D399"
C_WALL = "#E6E3DD"
C_FRAMEW = "#F1F1EE"
C_GLASS = "#DCEBF5"

C_BOARD = "#D9D6CF"
WINDOW = (10.0, 380.0, -220.0, 25.0)   # clear lid window (renders only): x0, x1, y0, y1, over core, exhaust fan, controller
CROP = (-260.0, 12.0, -560.0, 560.0, 300.0, 1420.0)   # context section kept around the unit


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _b(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _pipe(points, r):
    """Round tube through `points` with spherical joints."""
    out = None
    for a, c in zip(points, points[1:]):
        a, c = Vector(*a), Vector(*c)
        d = c - a
        seg = Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _par(s, axis):
    return s.edges().filter_by(axis)


def _top(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _xmax(s):
    return s.faces().sort_by(Axis.X)[-1].edges()


def _xmin(s):
    return s.faces().sort_by(Axis.X)[0].edges()


def _screw_x(x, y, z, r=3.2, sgn=1):
    """Pan-head screw on a face normal to X (head toward sgn * X) with a slot."""
    h = 1.6
    s = _xcyl(x + sgn * h / 2, y, z, r, h)
    s = _fillet_try(s, _xmax(s) if sgn > 0 else _xmin(s), [0.6, 0.3])
    s -= _b(x + sgn * (h - 0.5) - 0.6, x + sgn * (h - 0.5) + 0.6, y - r * 0.8, y + r * 0.8, z - 0.4, z + 0.4)
    return s


def product_parts(P=PARAMS):
    D = derived(P)
    C = build_components(P)
    M = lambda k: C[k].shape  # noqa: E731
    S = P["sill_z"]
    x0, x1, hy = P["hx0"], P["hx1"], P["hw"] / 2
    top, wtop = D["top"], D["wall_top"]
    st, lt = P["shell_t"], P["lining_t"]
    ix0, ix1, iy0, iy1, iz0, iz1 = D["inner"]
    py0, py1 = D["port_y"]
    pz0, pz1 = P["port_z0"], P["port_z0"] + P["port_h"]
    cx0, cx1 = P["core_x0"], D["core_x1"]
    cz0, cz1 = P["core_z0"], P["core_z0"] + P["core_h"]
    cw = P["core_w"] / 2
    ey0, ey1, ez0, ez1 = P["egrille"]
    gx0, gx1, gy0, gy1 = P["sgrille"]
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    E_LID = (0, 0, 440)
    E_CORE = (0, 0, 220)
    E_FAN = (0, 0, 330)
    E_FRONT = (240, 0, 0)

    # ------------------------------------------------------------ housing (BOM 1)
    env = _b(x0, x1, -hy, hy, S, wtop)
    env = _fillet_try(env, _par(env, Axis.Z), [4.0, 3.0, 2.0])
    env = _fillet_try(env, _bottom(env), [1.5, 1.0])
    shell = (M("base") + M("sides") + M("end_out") + M("end_room")) & env
    add("Housing boards", shell, C_SHELL, "plastic", 1, "shell", (0, 0, 0))
    add("Corner battens", M("battens"), C_FRAME, "plastic", 1, "internal", (0, 0, 0))
    add("Foam lining", M("lining"), C_LINING, "plastic", 1, "internal", (0, 0, 0))
    add("Core frames, dividers and fan bulkhead", M("frames") + M("div_out") + M("div_core") + M("div_room") + M("bulkhead"),
        C_BOARD, "plastic", 1, "internal", (0, 0, 0))
    add("Filter seat strips", M("seats"), C_FRAME, "plastic", 1, "internal", (0, 0, 0))

    # top-board lid (decided 2026-10-02) with the render-only clear window
    lenv = _b(x0, x1, -hy, hy, wtop, top)
    lenv = _fillet_try(lenv, _par(lenv, Axis.Z), [4.0, 3.0, 2.0])
    lenv = _fillet_try(lenv, _top(lenv), [2.0, 1.5, 1.0])
    wx0, wx1, wy0, wy1 = WINDOW
    win = _b(wx0, wx1, wy0, wy1, iz1 - 30, top + 1)
    win = _fillet_try(win, _par(win, Axis.Z), [12.0, 8.0])
    lid = (M("lid") & lenv) - win
    add("Lid (top board)", lid, C_LID, "plastic", 1, "shell", E_LID)
    add("Lid foam lining and blocks", M("lid_lining") - win, C_LINING, "plastic", 1, "internal", E_LID)
    pane = _b(wx0 + 0.5, wx1 - 0.5, wy0 + 0.5, wy1 - 0.5, top - 4, top - 1)
    pane = _fillet_try(pane, _par(pane, Axis.Z), [11.5, 8.0])
    add("Clear lid window (renders only)", pane, C_GLASS, "clear", 1, "shell", E_LID)
    gas = _b(wx0 - 6, wx1 + 6, wy0 - 6, wy1 + 6, top, top + 1.2)
    gas = _fillet_try(gas, _par(gas, Axis.Z), [16.0, 12.0])
    gcut = _b(wx0, wx1, wy0, wy1, top - 10, top + 5)
    gas -= _fillet_try(gcut, _par(gcut, Axis.Z), [12.0, 8.0])
    add("Window gasket", gas, C_RUBBER, "rubber", 1, "shell", E_LID)

    # grilles: slotted aluminium, exhaust on the room face, supply in the lid
    gr = M("grilles")
    add("Exhaust intake grille", gr & _b(x1 - 1, x1 + 5, -hy, hy, S, top), C_GRILLE, "metal", 1, "shell", E_FRONT)
    add("Supply outlet grille", gr & _b(x0, x1, -hy, hy, top - 1, top + 5), C_GRILLE, "metal", 1, "shell", E_LID)

    # two toggle latches on the side walls, keepers on the lid (model.py positions)
    lat = M("latches")
    add("Toggle latches", lat & _b(x0, x1, -hy - 20, hy + 20, S, wtop), C_METAL, "metal", 1, "shell", (0, 0, 0))
    add("Latch keepers", lat & _b(x0, x1, -hy - 20, hy + 20, wtop, top + 5), C_METAL, "metal", 1, "shell", E_LID)

    # room face: status light and button through the end wall (decided 2026-10-02), name plate, label
    pod = _b(x1, x1 + 1.2, 136, 184, 1093, 1117)
    pod = _fillet_try(pod, _par(pod, Axis.X), [6.0, 4.0])
    pod -= _xcyl(x1, 150, 1105, 3.2, 4) + _xcyl(x1, 170, 1105, 6.2, 4)
    add("Control bezel", pod, C_DARK, "plastic", 7, "shell", (0, 0, 0))
    btn = _xcyl(x1 + 1.0, 170, 1105, 5.5, 4.0)
    btn = _fillet_try(btn, _xmax(btn), [1.2, 0.8])
    add("Mode button", btn, C_ACCENT, "plastic", 7, "shell", (0, 0, 0))
    led = _xcyl(x1 + 0.2, 150, 1105, 2.8, 3.0)
    led = _fillet_try(led, _xmax(led), [1.2, 0.8])
    add("Status light (lit)", led, C_LED, "emissive", 7, "shell", (0, 0, 0))
    add("Name plate", _b(x1, x1 + 0.6, 20, 130, 1062, 1074), C_ACCENT, "painted", 1, "shell", (0, 0, 0))
    add("Rating label", _b(x1, x1 + 0.4, 140, 230, 945, 965), C_LABEL, "paper", 13, "shell", (0, 0, 0))
    add("Cable gland", M("gland"), C_DARK, "plastic", 13, "shell", (0, 0, 0))

    # ------------------------------------------------------------ counterflow core (BOM 2)
    core = _b(cx0, cx1, -cw, cw, cz0, cz1)
    grooves = []
    for k in range(1, 36):
        y = -cw + k * 5.0
        grooves.append(_b(cx0 + 12, cx1 - 12, y - 0.4, y + 0.4, cz1 - 1.0, cz1 + 1))
        for xe in (cx0, cx1):
            grooves.append(_b(xe - 1, xe + 1, y - 0.4, y + 0.4, cz0 + 12, cz1 - 12))
    core -= Compound(grooves)
    add("Counterflow plate core", core, C_CORE, "plastic", 2, "internal", E_CORE)
    rails = []
    for sy in (-1, 1):
        for zz in (cz0, cz1):
            r = _b(cx0 + 1, cx1 - 1, sy * cw - 6, sy * cw + 1, zz - 6, zz + 1) if zz == cz1 else \
                _b(cx0 + 1, cx1 - 1, sy * cw - 6, sy * cw + 1, zz, zz + 6)
            if sy < 0:
                r = _b(cx0 + 1, cx1 - 1, -cw - 1, -cw + 6, *((zz - 6, zz + 1) if zz == cz1 else (zz, zz + 6)))
            rails.append(_fillet_try(r, _par(r, Axis.X), [1.5, 1.0]))
    add("Core corner rails", _union(rails), C_RAIL, "plastic", 2, "internal", E_CORE)

    # ------------------------------------------------------------ fans on the bulkhead (BOM 3, 4)
    ft, fs, fz0 = P["fan_t"], P["fan_s"], P["fan_z0"]
    fzc = fz0 + fs / 2
    rr, rin, rl = P["fan_ring"]
    bx0 = P["bulk_x0"]; bx1 = bx0 + P["bulk_t"]

    def blower(xb, yc, d):
        """Blower body from xb to xb + ft; inlet ring toward d (-1: -X, +1: +X), as model.py."""
        body = _b(xb, xb + ft, yc - fs / 2, yc + fs / 2, fz0, fz0 + fs)
        body = _fillet_try(body, _par(body, Axis.X), [10.0, 6.0])
        xr = xb if d < 0 else xb + ft
        ring = Solid.make_cylinder(rr, rl, Plane(origin=(xr, yc, fzc), z_dir=(d, 0, 0)))
        ring -= Solid.make_cylinder(rin, rl, Plane(origin=(xr, yc, fzc), z_dir=(d, 0, 0)))
        body += ring
        body -= Solid.make_cylinder(rin, 6, Plane(origin=(xr, yc, fzc), z_dir=(-d, 0, 0)))
        for sy in (-1, 1):
            for sz in (-1, 1):
                body -= _xcyl(xb + ft / 2, yc + sy * (fs / 2 - 9), fzc + sz * (fs / 2 - 9), 2.2, ft + 2)
        imp = Solid.make_cylinder(12, 6, Plane(origin=(xr, yc, fzc), z_dir=(-d, 0, 0)))
        for k in range(9):
            b = _b(xr - 6 if d < 0 else xr, xr if d < 0 else xr + 6, -1.0, 1.0, 13, 33)
            imp += Pos(0, yc, fzc) * Rot(360.0 / 9 * k + 18, 0, 0) * b
        return body, imp

    for xb, yc, d, nm, bom, stripe in ((bx1, P["fan_yc"], -1, "Supply fan", 3, C_ACCENT),
                                       (bx0 - ft, -P["fan_yc"], 1, "Exhaust fan", 4, "#B45309")):
        body, imp = blower(xb, yc, d)
        e = (E_FAN[0], E_FAN[1] + (60 if yc > 0 else -60), E_FAN[2])
        add(f"{nm} body", body, C_FAN, "plastic", bom, "internal", e)
        add(f"{nm} impeller", imp, C_IMPELLER, "plastic", bom, "internal", e)
        add(f"{nm} label", _b(xb + 5, xb + ft - 5, yc - 40, yc + 40, fz0 + fs, fz0 + fs + 0.5), C_LABEL, "paper", bom, "internal", e)
        add(f"{nm} label stripe", _b(xb + 5, xb + ft - 5, yc - 40, yc - 28, fz0 + fs + 0.5, fz0 + fs + 0.8), stripe, "paper", bom, "internal", e)

    # ------------------------------------------------------------ filters in their seats (BOM 5, 6)
    sb = M("sfilter").bounding_box()
    fx0, fx1, fy0, fy1, fz0_, fz1_ = sb.min.X, sb.max.X, sb.min.Y, sb.max.Y, sb.min.Z, sb.max.Z
    frame = _b(fx0, fx1, fy0, fy1, fz0_, fz1_) - _b(fx0 - 1, fx1 + 1, fy0 + 6, fy1 - 6, fz0_ + 6, fz1_ - 6)
    add("Supply filter frame, ePM1", frame, C_FRAME, "paper", 5, "internal", (0, 0, 260))
    pleats = []
    y = fy0 + 6
    while y < fy1 - 6:
        pleats.append(_b(fx0 + 3, fx1 - 3, y, min(y + 3.0, fy1 - 6), fz0_ + 6, fz1_ - 6))
        y += 6.0
    pleats.append(_b(fx0 + 10, fx0 + 15, fy0 + 6, fy1 - 6, fz0_ + 6, fz1_ - 6))
    add("Supply filter pleats, ePM1", _union(pleats), C_FILTER, "fabric", 5, "internal", (0, 0, 260))
    add("Exhaust filter pad", M("efilter"), C_PAD, "fabric", 6, "internal", (0, 0, 260))

    # ------------------------------------------------------------ controller on the room-side divider (BOM 7)
    cb = M("ctrl").bounding_box()
    pcb = _b(cb.min.X, cb.max.X, cb.max.Y - 1.6, cb.max.Y, cb.min.Z, cb.max.Z)
    add("Controller board", pcb, C_PCB, "plastic", 7, "internal", (0, 0, 0))
    yb = cb.max.Y - 1.6
    add("ESP32-C3 module", _b(cb.min.X + 4, cb.min.X + 22, yb - 2.5, yb, cb.min.Z + 30, cb.min.Z + 54), C_CHIP, "plastic", 7, "internal", (0, 0, 0))
    add("CO2 and RH sensor", _b(cb.min.X + 24, cb.max.X - 3, yb - 7, yb, cb.min.Z + 6, cb.min.Z + 22), C_DARK, "plastic", 7, "internal", (0, 0, 0))

    # ------------------------------------------------------------ tray and drain (BOM 8)
    add("Condensate tray with core pads", M("tray"), C_TRAY, "plastic", 8, "internal", (0, 0, -130))
    add("Drain tube", M("drain"), C_TUBE, "rubber", 8, "internal", (0, 0, -130))

    # ------------------------------------------------------------ window insert (BOM 9, 10)
    E_I = (-260, 0, 0)
    E_H = (-440, 0, 0)
    add("Window insert panel", M("panel"), C_PANEL, "plastic", 9, "shell", E_I)
    add("EPDM end seals", M("seals"), C_RUBBER, "rubber", 9, "shell", E_I)
    add("Flanged collars", M("collars"), C_HOOD, "plastic", 10, "shell", E_I)
    add("Outdoor hoods", M("hoods"), C_HOOD, "plastic", 10, "shell", E_H)
    add("Hood back plates", M("hood_plates"), C_HOOD, "plastic", 10, "shell", E_H)
    add("Hood bolts, M5", M("hood_bolts"), C_METAL, "metal", 13, "shell", E_H)
    t = P["hood_t"]
    hbk = D["hood_back"]
    hx_out = P["panel_x0"] - 3 - P["hood_d"]
    mesh = []
    for s in (1, -1):
        my0, my1 = sorted((s * D["mouth_y"][0], s * D["mouth_y"][1]))
        m = _b(hx_out + t + 1, hbk - 1, my0 + t + 1, my1 - t - 1, P["hood_z0"] + 0.5, P["hood_z0"] + 1.5)
        k = hx_out + t + 8
        slots = []
        while k < hbk - 8:
            slots.append(_b(k, k + 3, my0 + t + 6, my1 - t - 6, P["hood_z0"], P["hood_z0"] + 2))
            k += 6
        m -= Compound(slots)
        mesh.append(m)
    add("Stainless insect mesh", _union(mesh), C_MESH, "metal", 10, "shell", E_H)

    # ------------------------------------------------------------ sill bracket (BOM 11), foot 400 mm up
    E_B = (0, 0, -280)
    add("Bracket rails", M("bplate"), C_ALU, "metal", 11, "shell", E_B)
    add("Angle cleats", M("cleats"), C_ALU, "metal", 11, "shell", E_B)
    add("Struts, flattened ends", M("struts"), C_ALU, "metal", 11, "shell", E_B)
    add("Wall foot bar", M("foot"), C_ALU, "metal", 11, "shell", E_B)
    add("Rubber wall pad", M("pad"), C_RUBBER, "rubber", 11, "shell", E_B)
    add("Bracket bolts", M("plate_bolts") + M("cleat_bolts"), C_METAL, "metal", 13, "shell", E_B)

    # ------------------------------------------------------------ 24 V adapter and cable (BOM 12)
    add("24 V adapter and low-voltage cable", M("psu"), C_DARK, "plastic", 12, "accessory", (0, 0, 0))

    # ------------------------------------------------------------ sash jammer (BOM 14), bought
    add("Sash jammer", M("jammer"), "#7F1D1D", "plastic", 14, "accessory", (-200, -520, -1150))

    # ------------------------------------------------------------ context (not in the BOM)
    ctx = context_parts(P)
    crop = _b(*CROP)
    add("Wall section (painted plaster)", ctx["wall"] & crop, C_WALL, "paper", None, "context", (0, 0, 0))
    add("Window frame", (ctx["frame"] & crop), C_FRAMEW, "painted", None, "context", (0, 0, 0))
    add("Lower sash (raised)", ctx["lower_sash"] & crop, C_FRAMEW, "painted", None, "context", (0, 0, 0))
    add("Window glass", ctx["lower_glass"] & crop, C_GLASS, "clear", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:36s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
