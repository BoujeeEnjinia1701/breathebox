"""BreatheBox product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: a filleted warm-white housing split into a body and a
lift-off lid at a parting line, a clear inspection window in the lid over the counterflow core, the
exhaust fan and the controller, a louvred front exhaust grille and top supply grille, a control
pod with a lit status light and a teal button, a name plate, side latches, the plate core with its
plate texture and corner rails, two black blowers with impellers, pleated and pad filters, the
controller board, the condensate tray and drain, the grey foam lining with its plenum dividers,
the insert panel with EPDM end seals, two filleted outdoor hoods with stainless insect mesh and
flange screws, the anodized sill bracket with a rubber wall pad, and the 24 V plug-in adapter.
Context is a compact section of wall with the window frame and the raised lower sash, cropped
around the unit (the upper sash lies above the crop).
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS, derived() and context_parts() in model.py.
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
from model import PARAMS, derived, context_parts

TITLE = "BreatheBox: window-mounted heat recovery ventilator for one room"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": 40,
     "note": "Product render from the room side, front right and above (about 30 deg elevation); unit on "
             "the sill of a sash window, counterflow core and exhaust fan seen through the clear lid window"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": 35,
     "note": "Exploded view from the room side, front right and above (about 28 deg elevation): lid with "
             "window, counterflow core, two fans, filters, controller, tray, housing, insert panel, "
             "outdoor hoods, sill bracket and 24 V adapter"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 48, "az": 25,
     "note": "Detail view from the room side and above (about 48 deg elevation), without the wall: "
             "counterflow core, exhaust fan and controller through the clear lid window"},
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

PARTING_Z = 1110.0          # lid parting line (lid above, body below)
WINDOW = (10.0, 380.0, -220.0, 45.0)   # clear lid window: x0, x1, y0, y1 (over core, exhaust fan, controller)
CROP = (-260.0, 12.0, -560.0, 560.0, 600.0, 1420.0)   # context section kept around the unit


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
    S = P["sill_z"]
    x0, x1, hy, z1 = P["hx0"], P["hx1"], P["hw"] / 2, S + P["hh"]
    st = P["shell_t"]
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
    E_CORE = (0, 0, 200)
    E_FAN = (110, 0, 200)
    E_FRONT = (240, 0, 0)

    # ------------------------------------------------------------ housing (BOM 1)
    outer = _b(x0, x1, -hy, hy, S, z1)
    outer = _fillet_try(outer, _par(outer, Axis.Z), [14.0, 10.0, 6.0])
    outer = _fillet_try(outer, _top(outer), [10.0, 8.0, 5.0])
    outer = _fillet_try(outer, _bottom(outer), [3.0, 2.0])
    cav = _b(x0 + st, x1 - st, -hy + st, hy - st, S + st, z1 - st)
    cav = _fillet_try(cav, _par(cav, Axis.Z), [8.0, 5.0])
    inner = _b(ix0, ix1, iy0, iy1, iz0, iz1)
    shell = outer - cav
    lining = cav - inner
    lining += _b(ix0, cx0, -4, 4, cz0, iz1)                               # outdoor plenum divider
    lining += _b(cx1, ix1 - P["efilter_t"] - 6, -4, 4, cz0, 1100)         # room plenum divider
    cuts = []
    for s in (1, -1):                                                     # outdoor-end ports
        ya, yb = sorted((s * py0, s * py1))
        cuts.append(_b(x0 - 1, ix0 + 1, ya, yb, pz0, pz1))
    cuts.append(_b(ix1 - 1, x1 + 1, ey0, ey1, ez0, ez1))                  # exhaust intake grille
    cuts.append(_b(gx0, gx1, gy0, gy1, iz1 - 1, z1 + 1))                  # supply outlet grille
    wx0, wx1, wy0, wy1 = WINDOW
    win = _b(wx0, wx1, wy0, wy1, PARTING_Z + 5, z1 + 1)
    win = _fillet_try(win, _par(win, Axis.Z), [12.0, 8.0])
    cuts.append(win)
    cuts.append(Solid.make_cylinder(7, ix0 + 1 - (x0 - 1), Plane(origin=(x0 - 1, 0, 923), z_dir=(1, 0, 0))))
    cut = _union(cuts)
    shell -= cut
    lining -= cut
    lo = _b(x0 - 5, x1 + 5, -hy - 5, hy + 5, S - 5, PARTING_Z)
    hi = _b(x0 - 5, x1 + 5, -hy - 5, hy + 5, PARTING_Z + 1.0, z1 + 5)
    add("Housing body", shell & lo, C_SHELL, "plastic", 1, "shell", (0, 0, 0))
    add("Housing lid", shell & hi, C_LID, "plastic", 1, "shell", E_LID)
    add("Foam lining and plenum dividers", lining & lo, C_LINING, "plastic", 1, "internal", (0, 0, 0))
    add("Lid foam lining", lining & hi, C_LINING, "plastic", 1, "internal", E_LID)

    # clear inspection window and its gasket
    pane = _b(wx0 + 0.5, wx1 - 0.5, wy0 + 0.5, wy1 - 0.5, z1 - 5, z1 - 2)
    pane = _fillet_try(pane, _par(pane, Axis.Z), [11.5, 8.0])
    add("Clear lid window", pane, C_GLASS, "clear", 1, "shell", E_LID)
    gas = _b(wx0 - 6, wx1 + 6, wy0 - 6, wy1 + 6, z1, z1 + 1.2)
    gas = _fillet_try(gas, _par(gas, Axis.Z), [16.0, 12.0])
    gcut = _b(wx0, wx1, wy0, wy1, z1 - 10, z1 + 5)
    gas -= _fillet_try(gcut, _par(gcut, Axis.Z), [12.0, 8.0])
    add("Window gasket", gas, C_RUBBER, "rubber", 1, "shell", E_LID)

    # top supply grille insert: slots along Y, throwing air up and away
    sg = _b(gx0 - 6, gx1 + 6, gy0 - 6, gy1 + 6, z1 - 3, z1 + 1.5)
    sg = _fillet_try(sg, _par(sg, Axis.Z), [6.0, 4.0])
    for k in range(8):
        xs = gx0 + 6 + k * 10.5
        sg -= _b(xs, xs + 5.5, gy0 + 6, gy1 - 6, z1 - 5, z1 + 3)
    add("Supply outlet grille", sg, C_GRILLE, "plastic", 1, "shell", E_LID)

    # front exhaust grille insert: horizontal louvres
    fg = _b(x1 - 1.5, x1 + 2.5, ey0 - 8, ey1 + 8, ez0 - 8, ez1 + 8)
    fg = _fillet_try(fg, _par(fg, Axis.X), [6.0, 4.0])
    fg = _fillet_try(fg, _xmax(fg), [1.0, 0.6])
    z = ez0 + 8
    while z + 6 <= ez1 - 6:
        fg -= _b(x1 - 3, x1 + 4, ey0 + 8, ey1 - 8, z, z + 6)
        z += 12
    add("Exhaust intake grille", fg, C_GRILLE, "plastic", 1, "shell", E_FRONT)

    # side latches across the parting line, name plate, control pod
    lat = []
    for s in (1, -1):
        l = _b(230, 262, s * hy - 1 if s > 0 else -hy - 3, s * hy + 3 if s > 0 else -hy + 1,
               PARTING_Z - 22, PARTING_Z + 18)
        lat.append(_fillet_try(l, l.edges(), [1.5, 1.0]))
    add("Lid latches", _union(lat), C_ACCENT, "plastic", 1, "shell", (0, 0, 0))
    plate = _b(x1 - 0.2, x1 + 0.6, 20, 150, 1082, 1092)
    add("Name plate", plate, C_ACCENT, "painted", 1, "shell", (0, 0, 0))
    lab = _b(x1 - 0.2, x1 + 0.5, 40, 130, 942, 962)
    add("Rating label", lab, C_LABEL, "paper", 13, "shell", (0, 0, 0))
    pod = _b(x1 - 0.5, x1 + 2.5, 170, 250, 1066, 1098)
    pod = _fillet_try(pod, _par(pod, Axis.X), [12.0, 8.0])
    add("Control pod", pod, C_DARK, "plastic", 7, "shell", (0, 0, 0))
    btn = _xcyl(x1 + 4.5, 227, 1082, 8.5, 4.0)
    btn = _fillet_try(btn, _xmax(btn), [1.5, 1.0])
    add("Mode button", btn, C_ACCENT, "plastic", 7, "shell", (0, 0, 0))
    led = _xcyl(x1 + 4.0, 190, 1082, 4.0, 3.0)
    led = _fillet_try(led, _xmax(led), [1.8, 1.2, 0.8])
    ring = _xcyl(x1 + 3.0, 190, 1082, 6.0, 1.0) - _xcyl(x1 + 3.0, 190, 1082, 4.0, 2.0)
    add("Status light bezel", ring, C_METAL, "metal", 7, "shell", (0, 0, 0))
    add("Status light (lit)", led, C_LED, "emissive", 7, "shell", (0, 0, 0))

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
            r = _b(cx0 - 1, cx1 + 1, sy * cw - 7, sy * cw + 7, zz - 7, zz + 7)
            rails.append(_fillet_try(r, _par(r, Axis.X), [2.0, 1.0]))
    for xm in ((cx0 + cx1) / 2,):
        band = _b(xm - 8, xm + 8, -cw - 1.2, cw + 1.2, cz0 - 1.2, cz1 + 1.2) - _b(xm - 9, xm + 9, -cw, cw, cz0, cz1)
        rails.append(band)
    add("Core corner rails and strap", _union(rails), C_RAIL, "plastic", 2, "internal", E_CORE)

    # ------------------------------------------------------------ fans (BOM 3, 4)
    fx0, ft, fs, fz0 = P["fan_x0"], P["fan_t"], P["fan_s"], P["fan_z0"]
    fzc = fz0 + fs / 2

    def blower(yc):
        body = _b(fx0, fx0 + ft, yc - fs / 2, yc + fs / 2, fz0, fz0 + fs)
        body = _fillet_try(body, _par(body, Axis.X), [10.0, 6.0])
        body = _fillet_try(body, _xmax(body), [2.0, 1.0])
        body += _xcyl(fx0 + ft + 1.0, yc, fzc, 44.0, 2.0)                        # motor boss
        ring = _xcyl(fx0 - 4, yc, fzc, 40, 8) - _xcyl(fx0 - 4, yc, fzc, 34, 10)  # inlet ring (model.py)
        body += ring
        body -= _xcyl(fx0 + 1, yc, fzc, 34, 6)                                   # inlet eye
        for sy in (-1, 1):
            for sz in (-1, 1):
                body -= _xcyl(fx0 + ft / 2, yc + sy * (fs / 2 - 9), fzc + sz * (fs / 2 - 9), 2.2, ft + 2)
        imp = _xcyl(fx0 + 3, yc, fzc, 12, 6)
        for k in range(9):
            b = _b(fx0 - 1, fx0 + 5, -1.0, 1.0, 13, 33)
            imp += Pos(0, yc, fzc) * Rot(360.0 / 9 * k + 18, 0, 0) * b
        return body, imp

    for yc, nm, bom, stripe in ((P["fan_yc"], "Supply fan", 3, C_ACCENT), (-P["fan_yc"], "Exhaust fan", 4, "#B45309")):
        body, imp = blower(yc)
        e = (E_FAN[0], E_FAN[1] + (60 if yc > 0 else -60), E_FAN[2])
        add(f"{nm} body", body, C_FAN, "plastic", bom, "internal", e)
        add(f"{nm} impeller", imp, C_IMPELLER, "plastic", bom, "internal", e)
        lab = _b(fx0 + 5, fx0 + ft - 5, yc - 40, yc + 40, fz0 + fs, fz0 + fs + 0.5)
        add(f"{nm} label", lab, C_LABEL, "paper", bom, "internal", e)
        strip = _b(fx0 + 5, fx0 + ft - 5, yc - 40, yc - 28, fz0 + fs + 0.5, fz0 + fs + 0.8)
        add(f"{nm} label stripe", strip, stripe, "paper", bom, "internal", e)

    # ------------------------------------------------------------ filters (BOM 5, 6)
    sx0 = ix0 + 6
    frame = _b(sx0, sx0 + P["sfilter_t"], py0, py1, pz0, pz1) - _b(sx0 - 1, sx0 + P["sfilter_t"] + 1, py0 + 8, py1 - 8, pz0 + 8, pz1 - 8)
    add("Supply filter frame, ePM1", frame, C_FRAME, "paper", 5, "internal", (-40, 0, 200))
    pleats = []
    y = py0 + 8
    while y < py1 - 8:
        pleats.append(_b(sx0 + 3, sx0 + P["sfilter_t"] - 3, y, min(y + 3.0, py1 - 8), pz0 + 8, pz1 - 8))
        y += 6.0
    pleats.append(_b(sx0 + 10, sx0 + 15, py0 + 8, py1 - 8, pz0 + 8, pz1 - 8))
    add("Supply filter pleats, ePM1", _union(pleats), C_FILTER, "fabric", 5, "internal", (-40, 0, 200))
    ef_x1 = ix1 - 2
    epad = _b(ef_x1 - P["efilter_t"], ef_x1, ey0, ey1, ez0 - 5, ez1 + 5)
    epad = _fillet_try(epad, _par(epad, Axis.X), [4.0, 2.0])
    add("Exhaust filter pad", epad, C_PAD, "fabric", 6, "internal", (150, 0, 0))

    # ------------------------------------------------------------ controller (BOM 7)
    E_CTL = (110, 0, 280)
    pcb = _b(300, 372, -30, 30, 1108, 1110)
    pcb = _fillet_try(pcb, _par(pcb, Axis.Z), [2.0, 1.0])
    add("Controller board", pcb, C_PCB, "plastic", 7, "internal", E_CTL)
    mod = _b(306, 330, -22, -4, 1110, 1112.5)
    add("ESP32-C3 module", mod, C_CHIP, "plastic", 7, "internal", E_CTL)
    can = _b(308, 328, -20, -6, 1112.5, 1114.5)
    add("Module shield can", can, C_METAL, "metal", 7, "internal", E_CTL)
    comps = (_b(340, 350, 8, 18, 1110, 1114) + _b(336, 344, -20, -12, 1110, 1112) + _zcyl(356, -14, 1115, 4, 10)
             + _b(310, 322, 14, 24, 1110, 1116))
    add("Controller components", comps, C_CHIP, "plastic", 7, "internal", E_CTL)
    sens = _b(368, 382, -12, 12, 1090, 1108)
    sens = _fillet_try(sens, sens.edges(), [1.0, 0.5])
    add("CO2 and RH sensor", sens, C_DARK, "plastic", 7, "internal", E_CTL)
    sens_top = _b(371, 379, -8, 8, 1107.9, 1108.4)
    add("Sensor membrane", sens_top, C_LABEL, "paper", 7, "internal", E_CTL)

    # ------------------------------------------------------------ condensate tray and drain (BOM 8)
    tray = _b(cx0 - 10, cx1 + 10, -100, 100, iz0, cz0) - _b(cx0 - 8, cx1 + 8, -98, 98, iz0 + 2, cz0 + 1)
    tray = _fillet_try(tray, _par(tray, Axis.Z), [3.0, 1.5])
    add("Condensate tray", tray, C_TRAY, "plastic", 8, "internal", (0, 0, -130))
    drain = _pipe([(cx0 - 10, 0, 923), (-300, 0, 923), (-300, 0, 700)], 6.0)
    drain -= _pipe([(cx0 - 9, 0, 923), (-300, 0, 923), (-300, 0, 699)], 4.0)
    add("Drain tube", drain, C_TUBE, "rubber", 8, "internal", (0, 0, -130))

    # ------------------------------------------------------------ window insert panel (BOM 9)
    ph = D["panel_half"]
    px0, px1 = P["panel_x0"], P["panel_x0"] + P["panel_t"]
    panel = _b(px0, px1, -ph, ph, S, S + P["panel_h"])
    panel = _fillet_try(panel, _par(panel, Axis.X), [4.0, 2.0])
    for s in (1, -1):
        ya, yb = sorted((s * (py0 - 3), s * (py1 + 3)))
        panel -= _b(px0 - 1, px1 + 1, ya, yb, pz0 - 3, pz1 + 3)
    panel -= _xcyl((px0 + px1) / 2, 0, 923, 7, P["panel_t"] + 2)
    add("Window insert panel", panel, C_PANEL, "plastic", 9, "shell", (-220, 0, 0))
    seals = _union([_b(px0 + 2, px1 - 2, s * ph - (0 if s > 0 else P["seal"]), s * ph + (P["seal"] if s > 0 else 0),
                       S + 4, S + P["panel_h"] - 4) for s in (1, -1)])
    add("EPDM edge seals", seals, C_RUBBER, "rubber", 9, "shell", (-220, 0, 0))

    # ------------------------------------------------------------ outdoor hoods (BOM 10)
    t = P["hood_t"]
    hx_out = px0 - P["hood_d"]
    hoods, mesh, flange, fscr = [], [], [], []
    for s in (1, -1):
        ya, yb = sorted((s * (py0 - 3), s * P["hood_y_out"]))
        h = _b(hx_out, px0, ya, yb, P["hood_z0"], P["hood_z1"])
        h = _fillet_try(h, _par(h, Axis.X), [8.0, 5.0])
        h = _fillet_try(h, _xmin(h), [4.0, 2.0])
        h -= _b(hx_out + t, px0 + 1, ya + t, yb - t, P["hood_z0"] + t, P["hood_z1"] - t)
        my0, my1 = sorted((s * D["mouth_y"][0], s * D["mouth_y"][1]))
        h -= _b(hx_out + t, px0 - t, my0 + t, my1 - t, P["hood_z0"] - 1, P["hood_z0"] + t + 1)
        pa, pb = sorted((s * py0, s * py1))
        collar = _b(px0 - 1, x0, pa - t, pb + t, pz0 - t, pz1 + t) - _b(px0 - 2, x0 + 1, pa, pb, pz0, pz1)
        hoods += [h, collar]
        m = _b(hx_out + t + 2, px0 - t - 2, my0 + t + 2, my1 - t - 2, P["hood_z0"] + 0.5, P["hood_z0"] + 1.5)
        k = hx_out + t + 8
        slots = []
        while k < px0 - t - 8:
            slots.append(_b(k, k + 3, my0 + t + 6, my1 - t - 6, P["hood_z0"], P["hood_z0"] + 2))
            k += 6
        m -= Compound(slots)
        mesh.append(m)
        fl = _b(px0 - 3, px0, ya - 8, yb + 8, P["hood_z0"] - 8, P["hood_z1"] + 8)
        fl = _fillet_try(fl, _par(fl, Axis.X), [6.0, 4.0])
        fl -= _b(px0 - 4, px0 + 1, ya + t, yb - t, P["hood_z0"] + t, P["hood_z1"] - t)
        flange.append(fl)
        for yy in (ya - 1, yb + 1):
            for zz in (P["hood_z0"] - 2, P["hood_z1"] + 2):
                fscr.append(_screw_x(px0 - 3, yy, zz, 2.6, -1))
    E_H = (-440, 0, 0)
    add("Outdoor hoods and collars", _union(hoods), C_HOOD, "plastic", 10, "shell", E_H)
    add("Hood flanges", _union(flange), C_HOOD, "plastic", 10, "shell", E_H)
    add("Stainless insect mesh", _union(mesh), C_MESH, "metal", 10, "shell", E_H)
    add("Hood flange screws", _union(fscr), C_METAL, "metal", 13, "shell", E_H)

    # ------------------------------------------------------------ sill bracket (BOM 11)
    bw = P["bracket_w"] / 2
    bt = P["bracket_t"]
    bplate = _b(0, P["bracket_x1"], -bw, bw, S - bt, S)
    bplate = _fillet_try(bplate, _par(bplate, Axis.Z), [12.0, 6.0])
    r, rw = P["strut_r"], P["strut_wall"]
    struts = []
    for sy in (-170, 170):
        a, b = (8, sy, P["foot_z"]), (P["bracket_x1"] - 20, sy, S - bt - 10)
        tube = _pipe([a, b], r) - _pipe([a, b], r - rw)
        struts.append(tube)
        struts.append(_b(P["bracket_x1"] - 40, P["bracket_x1"] - 5, sy - 12, sy + 12, S - bt - 16, S - bt))
        struts.append(_b(8, 22, sy - 12, sy + 12, P["foot_z"] - 14, P["foot_z"] + 14))
    add("Sill bracket plate", bplate, C_ALU, "metal", 11, "shell", (0, 0, -280))
    add("Bracket struts", _union(struts), C_ALU, "metal", 11, "shell", (0, 0, -280))
    foot = _b(3, 8, -bw, bw, P["foot_z"] - 30, P["foot_z"] + 30)
    foot = _fillet_try(foot, _par(foot, Axis.X), [8.0, 4.0])
    add("Bracket wall foot", foot, C_ALU, "metal", 11, "shell", (0, 0, -280))
    pad = _b(0, 3, -bw + 4, bw - 4, P["foot_z"] - 26, P["foot_z"] + 26)
    pad = _fillet_try(pad, _par(pad, Axis.X), [6.0, 3.0])
    add("Rubber wall pad", pad, C_RUBBER, "rubber", 11, "shell", (0, 0, -280))

    # ------------------------------------------------------------ 24 V adapter and cable (BOM 12)
    psu = _b(0, 45, 520, 590, 300, 380)
    psu = _fillet_try(psu, psu.edges(), [6.0, 3.0])
    add("24 V plug-in adapter", psu, C_DARK, "plastic", 12, "accessory", (0, 0, 0))
    cable = _pipe([(45, 555, 340), (60, 555, 340), (60, 300, 880), (60, 286, 1000)], 3.0)
    add("Low-voltage cable", cable, C_RUBBER, "rubber", 12, "accessory", (0, 0, 0))

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
