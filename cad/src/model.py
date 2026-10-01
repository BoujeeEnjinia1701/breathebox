"""BreatheBox parametric model (build123d), TRL 3, constructable design (BBX-DDR-003).

Run from the repo root:
    python cad/src/model.py            export STEP and STL into cad/step and cad/stl, print the
                                       main envelopes and run the constructability checks
    python cad/src/model.py --check    run the constructability checks only

Every component is modelled as it is made: the housing is six 6 mm PVC foam boards glued and
screwed into 10 mm corner battens, lined with 10 mm closed-cell foam, with two core frames, three
dividers and a fan bulkhead that separate the four air paths; filters sit in strip seats; the
window insert is a panel with a flanged collar and a hood bolted through it on each side; the sill
bracket is two aluminium rails bolted under the housing, with two flattened-end tube struts bolted
(two bolts at each end, so the bracket is rigid) to angle cleats on the rails and on a padded wall foot. build_components() returns them all;
build_parts() groups them by BOM line for the concept media and the drawing.

Axes: X is depth through the wall (outdoors negative, room positive; the inner wall face is X = 0),
Y runs along the window width (supply side +Y, exhaust side -Y), Z is up with the room floor at
Z = 0. Units mm. The unit sits on the sill of a vertical sliding sash window; the lower sash is
raised and closed down onto the insert panel.
"""
import math
import sys
from collections import namedtuple
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Window and wall (context; design case in BBX-REQ-001)
    "wall_t": 250.0, "sill_z": 900.0,
    "open_w": 900.0,            # clear width between the jambs (R8 range 700 to 1000)
    "open_h": 1200.0,
    # Window insert panel (item 9)
    "panel_x0": -150.0, "panel_t": 20.0, "panel_h": 260.0, "seal": 3.0,
    # Housing (item 1): 6 mm PVC foam board shell, 10 mm foam lining, 10 x 10 mm corner battens
    "hx0": -110.0, "hx1": 400.0, "hw": 560.0, "hh": 250.0,
    "shell_t": 6.0, "lining_t": 10.0, "batten": 10.0,
    "board_t": 3.0,             # core frames and dividers: 3 mm PVC foam board
    "bulk_t": 6.0,              # fan bulkhead: 6 mm PVC foam board, as the shell
    # Counterflow core (item 2) and its seat
    "core_x0": -40.0, "core_l": 300.0, "core_w": 180.0, "core_h": 180.0, "core_z0": 930.0,
    "plate_pitch": 2.5, "plate_t": 0.15,
    "u_lip": 6.0,               # the core frames overlap the core's end faces by this much
    # Outdoor-end ports (collar bore), filters and seats
    "port_yc": 185.0, "port_w": 150.0, "port_h": 170.0, "port_z0": 935.0,
    "sfilter_t": 25.0,          # supply filter (item 5)
    "sf_lip": 5.0,              # lining lip inside the supply filter's frame
    "efilter_w": 220.0, "efilter_h": 190.0, "efilter_t": 12.0,   # exhaust filter (item 6)
    "ef_lip": 10.0,             # lining lip behind the exhaust filter pad
    "strip": 10.0,              # 10 x 10 mm strip for the filter seats
    # Collars (item 10): rectangular PVC tube with a flange on the panel's room face
    "collar_t": 3.0, "collar_flange": 20.0, "port_gap": 2.0,
    # Outdoor hoods (item 10): body from the back plate outward, mouth at the bottom
    "hood_d": 180.0, "hood_y_out": 340.0, "mouth_w": 130.0, "hood_z0": 925.0, "hood_z1": 1115.0,
    "hood_t": 3.0,
    # Fans (items 3 and 4): 120 x 120 x 32 mm class centrifugal blowers on the fan bulkhead
    "fan_x0": 280.0,            # kept for the appearance model (product_model.py)
    "bulk_x0": 300.0,           # core-side face of the fan bulkhead
    "fan_t": 32.0, "fan_s": 120.0, "fan_yc": 150.0, "fan_z0": 950.0, "fan_ring": (40.0, 34.0, 8.0),
    # Room-side grilles
    "sgrille": (310.0, 380.0, 40.0, 260.0),      # top supply outlet: x0, x1, y0, y1
    "egrille": (-250.0, -30.0, 930.0, 1120.0),   # front exhaust intake: y0, y1, z0, z1
    # Condensate drain (item 8)
    "drain_y": -40.0, "drain_z": 922.0, "tube_od": 12.0, "tube_id": 8.0,
    # Sill bracket (item 11)
    "bracket_t": 4.0, "bracket_w": 400.0, "bracket_x1": 390.0, "foot_z": 500.0,
    "rail_y": (150.0, 200.0),   # two 50 x 4 mm aluminium rails under the housing, each side
    "strut_r": 10.0, "strut_wall": 1.5, "strut_y": 158.0,
    "tab": 40.0, "tab_r": 13.0, "hole_pitch": 20.0,   # flattened end: length, end radius, two holes
    "angle": (40.0, 3.0), "cleat_len": 50.0,          # equal angle leg and thickness for the cleats
    "foot_bar": (60.0, 6.0), "pad_t": 2.0,
    "plate_bolts": ((30.0, 175.0), (330.0, 175.0)),
}

Comp = namedtuple("Comp", "name shape bom material group")

COLOURS = {1: "#E7F0EE", 2: "#D4A017", 3: "#0F766E", 4: "#C2410C", 5: "#2563EB", 6: "#94A3B8",
           7: "#7C3AED", 8: "#0EA5E9", 9: "#A7C4BC", 10: "#475569", 11: "#6B7280", 12: "#111827"}
NAMES = {1: "Insulated housing", 2: "Counterflow core", 3: "Supply fan, EC", 4: "Exhaust fan, EC",
         5: "Supply filter, ePM1", 6: "Exhaust filter, coarse", 7: "Controller, CO2 and RH",
         8: "Condensate tray and drain", 9: "Window insert panel", 10: "Outdoor hoods and collars",
         11: "Sill bracket", 12: "24 V power supply"}
EXPLODE = {1: (250, 0, 720), 2: (0, 0, 300), 3: (180, 300, 330), 4: (180, -300, 330), 5: (-60, -200, 520),
           6: (320, -140, 140), 7: (200, 0, 480), 8: (0, 0, -240), 9: (-300, 0, -60), 10: (-560, 0, -520),
           11: (200, 0, -320), 12: (250, 250, -150)}


# ------------------------------------------------------------------ primitives
def _box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); z0, z1 = sorted((z0, z1))
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _tube(a, b, r, r_in=0.0):
    from build123d import Plane, Solid, Vector
    a = Vector(*a); b = Vector(*b); d = b - a
    pl = Plane(origin=a, z_dir=d.normalized())
    s = Solid.make_cylinder(r, d.length, pl)
    if r_in > 0:
        s = s - Solid.make_cylinder(r_in, d.length, pl)
    return s


def _xcyl(x0, x1, y, z, r):
    return _tube((x0, y, z), (x1, y, z), r)


def _ycyl(y0, y1, x, z, r):
    return _tube((x, y0, z), (x, y1, z), r)


def _zcyl(z0, z1, x, y, r):
    return _tube((x, y, z0), (x, y, z1), r)


def _fuse(shapes):
    out = None
    for s in shapes:
        if s is None:
            continue
        out = s if out is None else out + s
    return out


def _mirror_y(shape):
    from build123d import Plane, mirror
    return mirror(shape, Plane.XZ)


def _bolt(axis, a, b, c1, c2, d=5.0, head=8.0, nut=8.0):
    """Bolt along an axis: head against face a (on the side away from b), shank from a to b, nut
    against face b. c1, c2 are the other two coordinates (y, z for X; x, z for Y; x, y for Z)."""
    sgn = 1 if b > a else -1
    hh, nh = 0.7 * d, 0.8 * d
    cyl = {"x": lambda s, e, r: _xcyl(s, e, c1, c2, r), "y": lambda s, e, r: _ycyl(s, e, c1, c2, r),
           "z": lambda s, e, r: _zcyl(s, e, c1, c2, r)}[axis]
    return cyl(a - sgn * hh, a, head / 2 + 0.5) + cyl(a, b, d / 2) + cyl(b, b + sgn * nh, nut / 2 + 0.6)


# ------------------------------------------------------------------ derived dimensions
def derived(p=PARAMS):
    """Dimensions derived from the parameters, shared with the calculation note and the pictures."""
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
    d["top"] = p["sill_z"] + p["hh"]
    d["wall_top"] = d["top"] - p["shell_t"]
    ct = p["collar_t"]
    py0, py1 = d["port_y"]
    pz0, pz1 = p["port_z0"], p["port_z0"] + p["port_h"]
    d["collar_out"] = (py0 - ct, py1 + ct, pz0 - ct, pz1 + ct)
    d["hood_back"] = p["panel_x0"] - 3.0          # outer face of the hood back plate
    f = p["collar_flange"]
    co = d["collar_out"]
    d["collar_fl"] = (co[0] - f, co[1] + f, co[2] - f, co[3] + f)
    e = 7.0                                        # bolt centre from the flange's outer edge
    fl = d["collar_fl"]
    d["hood_bolts"] = [(y, z) for y in (fl[0] + e - 1, fl[1] - e + 1) for z in (fl[2] + e, fl[3] - e)]
    # strut geometry (side +Y; the -Y side is its mirror). Each end has two holes on the strut axis
    # (end hole and inner hole, hole_pitch apart), so the strut joints are rigid.
    ang, at = p["angle"]
    sy = p["strut_y"]
    d["tab_face"] = sy + 1.5                       # tab is 3 mm thick, centred on the strut axis
    d["strut_top"] = (365.0, p["sill_z"] - p["bracket_t"] - at - 13.0)
    d["strut_foot"] = (p["pad_t"] + p["foot_bar"][1] + at + 13.0, p["foot_z"] - 8.0)
    (xa, za), (xb, zb) = d["strut_foot"], d["strut_top"]
    d["strut_len"] = math.hypot(xb - xa, zb - za)
    d["strut_angle"] = math.degrees(math.atan2(zb - za, xb - xa))
    u = ((xb - xa) / d["strut_len"], (zb - za) / d["strut_len"])
    hp = p["hole_pitch"]
    d["strut_u"] = u
    d["foot_holes"] = [(xa, za), (xa + hp * u[0], za + hp * u[1])]
    d["top_holes"] = [(xb, zb), (xb - hp * u[0], zb - hp * u[1])]
    d["strut_bar"] = d["strut_len"] + 2 * p["tab_r"]   # tube cut length before flattening (approximate)
    return d


# ------------------------------------------------------------------ components
def build_components(p=PARAMS):
    """Every component as a Comp(name, shape, bom, material, group), keyed by a short name.
    material keys are densities in docs/04-calcs/sizing.py; group is the build-plan group."""
    D = derived(p)
    S = p["sill_z"]
    st, lt, bt, bd = p["shell_t"], p["lining_t"], p["batten"], p["board_t"]
    x0, x1, hy = p["hx0"], p["hx1"], p["hw"] / 2
    top, wtop = D["top"], D["wall_top"]
    ix0, ix1, iy0, iy1, iz0, iz1 = D["inner"]
    py0, py1 = D["port_y"]
    pz0, pz1 = p["port_z0"], p["port_z0"] + p["port_h"]
    cx0, cx1 = p["core_x0"], D["core_x1"]
    cz0, cz1 = p["core_z0"], p["core_z0"] + p["core_h"]
    cw = p["core_w"] / 2
    bx0 = p["bulk_x0"]; bx1 = bx0 + p["bulk_t"]
    hb = bd / 2
    C = {}

    def add(key, name, shape, bom, material, group):
        C[key] = Comp(name, shape, bom, material, group)

    dy, dz = p["drain_y"], p["drain_z"]
    ro, ri = p["tube_od"] / 2, p["tube_id"] / 2

    # ---- 1 housing shell: base under everything, sides on the base, ends between the sides
    base = _box(x0, x1, -hy, hy, S, S + st)
    for (bxp, byp) in p["plate_bolts"]:
        for s in (1, -1):
            base -= _zcyl(S - 1, S + st + 1, bxp, s * byp, 2.75)
    sides = _box(x0, x1, hy - st, hy, S + st, wtop) + _box(x0, x1, -hy, -hy + st, S + st, wtop)
    sides -= _ycyl(hy - st - 1, hy + 1, 350.0, 1100.0, 6.0)                 # power cable gland
    end_out = _box(x0, x0 + st, -hy + st, hy - st, S + st, wtop)
    g = p["port_gap"]
    co = D["collar_out"]
    for s in (1, -1):
        end_out -= _box(x0 - 1, x0 + st + 1, s * (co[0] - g), s * (co[1] + g), co[2] - g, co[3] + g)
    end_out -= _xcyl(x0 - 1, x0 + st + 1, dy, dz, ro + 1)
    ey0, ey1, ez0, ez1 = p["egrille"]
    end_room = _box(x1 - st, x1, -hy + st, hy - st, S + st, wtop)
    end_room -= _box(x1 - st - 1, x1 + 1, ey0, ey1, ez0, ez1)
    for yy, rr in ((150.0, 3.0), (170.0, 6.0)):                               # status light, button
        end_room -= _xcyl(x1 - st - lt - 1, x1 + 1, yy, 1105.0, rr)
    add("base", "Housing base", base, 1, "pvc_board", "shell")
    add("sides", "Housing sides (2)", sides, 1, "pvc_board", "shell")
    add("end_out", "Outdoor end wall", end_out, 1, "pvc_board", "shell")
    add("end_room", "Room end wall", end_room, 1, "pvc_board", "shell")

    # ---- 1 corner battens 10 x 10 mm: four upright, four along the bottom edges
    bat = []
    for sx, xa in ((1, x0 + st), (-1, x1 - st)):
        for sy in (1, -1):
            bat.append(_box(xa, xa + sx * bt, sy * (hy - st), sy * (hy - st - bt), S + st, wtop))
        bat.append(_box(xa, xa + sx * bt, -(hy - st - bt), hy - st - bt, S + st, S + st + bt))
    for sy in (1, -1):
        bat.append(_box(x0 + st + bt, x1 - st - bt, sy * (hy - st), sy * (hy - st - bt), S + st, S + st + bt))
    add("battens", "Corner battens (8)", _fuse(bat), 1, "strip", "shell")

    # ---- 1 lining, 10 mm closed-cell foam
    floor = _box(ix0, ix1, iy0, iy1, S + st, iz0)
    for (bxp, byp) in p["plate_bolts"]:
        for s in (1, -1):
            floor -= _zcyl(S + st - 1, iz0 + 1, bxp, s * byp, 6.0)            # relief over the nuts
    lin_side = _box(ix0, ix1, iy1, iy1 + lt, iz0, wtop) + _box(ix0, ix1, iy0, iy0 - lt, iz0, wtop)
    lin_side -= _ycyl(iy1 - 1, hy - st + 1, 350.0, 1100.0, 6.0)
    lin_out = _box(x0 + st, ix0, iy0, iy1, iz0, wtop)
    sl = p["sf_lip"]
    lin_out -= _box(x0 + st - 1, ix0 + 1, py0 + sl, py1 - sl, pz0 + sl, pz1 - sl)    # supply: lip
    lin_out -= _box(x0 + st - 1, ix0 + 1, -py0, -py1, pz0, pz1)                     # exhaust: bore
    lin_out -= _xcyl(x0 + st - 1, ix0 + 1, dy, dz, ro + 1)
    el = p["ef_lip"]
    lin_room = _box(ix1, ix1 + lt, iy0, iy1, iz0, wtop)
    lin_room -= _box(ix1 - 1, ix1 + lt + 1, ey0 + el, ey1 - el, ez0 + el, ez1 - el)
    for yy, rr in ((150.0, 3.0), (170.0, 6.0)):
        lin_room -= _xcyl(ix1 - 1, ix1 + lt + 1, yy, 1105.0, rr)
    add("lining", "Foam lining", _fuse([floor, lin_side, lin_out, lin_room]), 1, "foam", "lining")

    # ---- 1 core frames (U cut over the core end), dividers, fan bulkhead: 6 mm board
    ul = p["u_lip"]
    frames = []
    for xa in (cx0 - bd, cx1):
        f = _box(xa, xa + bd, iy0, iy1, iz0, iz1) - _box(xa - 1, xa + bd + 1, -(cw - ul), cw - ul, cz0 + ul, iz1 + 1)
        if xa < 0:
            f -= _xcyl(xa - 1, xa + bd + 1, dy, dz, ro + 0.5)
        frames.append(f)
    add("frames", "Core frames (2)", _fuse(frames), 1, "pvc_board", "partitions")
    div_out = _box(ix0, cx0 - bd, -hb, hb, iz0, iz1) + _box(cx0 - bd, cx0, -hb, hb, cz0 + ul, cz1)
    div_core = _box(cx1 + bd, bx0, -hb, hb, iz0, iz1) + _box(cx1, cx1 + bd, -hb, hb, cz0 + ul, cz1)
    div_room = _box(bx1, ix1, -hb, hb, iz0, iz1)
    add("div_out", "Outdoor-end divider", div_out, 1, "pvc_board", "partitions")
    add("div_core", "Core-side divider", div_core, 1, "pvc_board", "partitions")
    add("div_room", "Room-side divider", div_room, 1, "pvc_board", "partitions")
    rr_, rin, rl = p["fan_ring"]
    fzc = p["fan_z0"] + p["fan_s"] / 2
    bulk = _box(bx0, bx1, iy0, iy1, iz0, iz1)
    for s in (1, -1):
        bulk -= _xcyl(bx0 - 1, bx1 + 1, s * p["fan_yc"], fzc, rr_ + 0.5)
    add("bulkhead", "Fan bulkhead", bulk, 1, "pvc_board", "partitions")

    # ---- 1 filter seats: 10 x 10 mm strips and bottom stops
    sk = p["strip"]
    sft = p["sfilter_t"]
    sfz0 = pz0 + 1.0                                   # filter 936 to 1106, on a 20 mm stop
    seats = [
        _box(ix0, ix0 + sk, py0 - sk, py0, iz0, iz1),                         # side strip
        _box(ix0 + sft, ix0 + sft + sk, py0 - 4, py0 + 6, iz0, iz1),          # lip strip, 6 mm over the edge
        _box(ix0 + sft, ix0 + sft + sk, py1 - 6, iy1, iz0, iz1),              # lip strip at the side lining
        _box(ix0, ix0 + sft, py0, py1, iz0, sfz0),                            # bottom stop
    ]
    eft = p["efilter_t"]
    efx0 = ix1 - eft
    efz0 = iz0 + sk
    seats += [
        _box(ix1 - sk, ix1, ey0 - sk, ey0, iz0, iz1),
        _box(ix1 - sk, ix1, ey1, ey1 + sk, iz0, iz1),
        _box(efx0 - sk, efx0, ey0, ey0 + sk, iz0, iz1),
        _box(efx0 - sk, efx0, ey1 - sk, ey1, iz0, iz1),
        _box(efx0, ix1, ey0, ey1, iz0, efz0),
    ]
    add("seats", "Filter seat strips and stops", _fuse(seats), 1, "strip", "seats")

    # ---- 1 lid: board, lining plug, core hold-down and filter top blocks, supply grille opening
    gx0, gx1, gy0, gy1 = p["sgrille"]
    lid = _box(x0, x1, -hy, hy, wtop, top)
    plug = _box(ix0 + 1, ix1 - 1, iy0 + 1, iy1 - 1, iz1, wtop)
    blocks = [_box(cx0 - bd, cx1 + bd, -(cw - ul), cw - ul, cz1, iz1),            # core hold-down
              _box(ix0 + 1, ix0 + sft + sk, py0 + 6, py1 - 6, sfz0 + p["port_h"], iz1),  # over the supply filter
              _box(efx0 - sk, ix1 - 1, ey0 + sk, ey1 - sk, efz0 + p["efilter_h"], iz1)]
    lid_board = lid - _box(gx0, gx1, gy0, gy1, wtop - 1, top + 1)
    plug = plug - _box(gx0, gx1, gy0, gy1, iz1 - 1, wtop + 1)
    add("lid", "Lid", lid_board, 1, "pvc_board", "lid")
    add("lid_lining", "Lid lining and foam blocks", _fuse([plug] + blocks), 1, "foam", "lid")

    # ---- 1 grilles: perforated aluminium, slots 4 mm wide
    eg = _box(x1, x1 + 2, ey0 - 10, ey1 + 10, ez0 - 10, ez1 + 10)
    for k in range(int((ey1 - ey0 - 10) // 10)):
        y = ey0 + 7 + 10 * k
        eg -= _box(x1 - 1, x1 + 3, y, y + 4, ez0 + 10, ez1 - 10)
    sg = _box(gx0 - 10, gx1 + 10, gy0 - 10, gy1 + 10, top, top + 2)
    for k in range(int((gx1 - gx0 - 6) // 10)):
        x = gx0 + 5 + 10 * k
        sg -= _box(x, x + 4, gy0 + 10, gy1 - 10, top - 1, top + 3)
    add("grilles", "Grilles (2)", eg + sg, 1, "aluminium", "grilles")

    # ---- 1 lid latches (2), one on each side wall, keeper on the lid
    lat = []
    for s in (1, -1):
        lat.append(_box(110, 150, s * hy, s * (hy + 10), wtop - 32, wtop - 4))
        lat.append(_box(118, 142, s * (hy - 18), s * (hy + 3), top, top + 2) + _box(118, 142, s * hy, s * (hy + 3), wtop - 4, top))
    add("latches", "Lid latches (2)", _fuse(lat), 1, "latch", "lid")

    # ---- 2 core, on four pads in the tray, ends against the core frames
    add("core", "Counterflow core", _box(cx0, cx1, -cw, cw, cz0, cz1), 2, "core", "core")

    # ---- 3, 4 fans on the bulkhead: supply on the room side, exhaust on the core side
    def blower(xb, yc, inlet_dir):
        body = _box(xb, xb + p["fan_t"], yc - p["fan_s"] / 2, yc + p["fan_s"] / 2, p["fan_z0"], p["fan_z0"] + p["fan_s"])
        xr = xb if inlet_dir < 0 else xb + p["fan_t"]
        ring = _tube((xr, yc, fzc), (xr + inlet_dir * rl, yc, fzc), rr_, rin)
        return body + ring
    add("fan_s", "Supply fan", blower(bx1, p["fan_yc"], -1), 3, "fan", "fans")
    add("fan_e", "Exhaust fan", blower(bx0 - p["fan_t"], -p["fan_yc"], +1), 4, "fan", "fans")

    # ---- 5, 6 filters in their seats
    add("sfilter", "Supply filter", _box(ix0, ix0 + sft, py0, py1, sfz0, sfz0 + p["port_h"]), 5, "filter", "filters")
    add("efilter", "Exhaust filter", _box(efx0, ix1, ey0, ey1, efz0, efz0 + p["efilter_h"]), 6, "filter", "filters")

    # ---- 7 controller on the room-side divider in the intake air; status board behind the room face
    ctrl = _box(bx1 + 10, bx1 + 50, -hb, -hb - 18, 1060, 1120)
    status = _box(ix1 - 6, ix1, 140, 180, 1095, 1115)
    add("ctrl", "Controller with CO2 sensor", ctrl, 7, "electronics", "controls")
    add("status", "Status light and button board", status, 7, "electronics", "controls")

    # ---- 8 tray between the core frames, four pads, drain tube through the outdoor end
    tray = _box(cx0, cx1, -100, 100, iz0, cz0) - _box(cx0 + 2, cx1 - 2, -98, 98, iz0 + 2, cz0 + 1)
    tray -= _xcyl(cx0 - 1, cx0 + 3, dy, dz, ro)
    pads = [_box(xa, xa + 20, ya, ya + 20, iz0 + 2, cz0) for xa in (cx0 + 10, cx1 - 30) for ya in (60, -80)]
    add("tray", "Condensate tray with core pads", _fuse([tray] + pads), 8, "petg", "tray")
    xd = -300.0
    drain = (_tube((cx0 + 2, dy, dz), (xd, dy, dz), ro, ri) + _tube((xd, dy, dz), (xd, dy, 700.0), ro, ri))
    add("drain", "Drain tube", drain, 8, "silicone", "tray")

    # ---- 9 window insert panel with collar cut-outs, drain hole and bolt holes; EPDM end seals
    ph = D["panel_half"]
    px0, px1 = p["panel_x0"], p["panel_x0"] + p["panel_t"]
    panel = _box(px0, px1, -ph, ph, S, S + p["panel_h"])
    for s in (1, -1):
        panel -= _box(px0 - 1, px1 + 1, s * (co[0] - 1), s * (co[1] + 1), co[2] - 1, co[3] + 1)
        for (yb, zb) in D["hood_bolts"]:
            panel -= _xcyl(px0 - 1, px1 + 1, s * yb, zb, 2.75)
    panel -= _xcyl(px0 - 1, px1 + 1, dy, dz, ro + 1)
    seals = _box(px0 + 2, px1 - 2, ph, ph + p["seal"], S + 4, S + p["panel_h"] - 4) + \
        _box(px0 + 2, px1 - 2, -ph, -ph - p["seal"], S + 4, S + p["panel_h"] - 4)
    add("panel", "Window insert panel", panel, 9, "panel", "insert")
    add("seals", "EPDM end seals", seals, 9, "epdm", "insert")

    # ---- 10 collars: tube through the panel into the housing port, flange on the panel's room face
    ct = p["collar_t"]
    hbk = D["hood_back"]
    fl = D["collar_fl"]
    collars, hoods, hplates, hbolts = [], [], [], []
    t = p["hood_t"]
    hx_out = px0 - 3 - p["hood_d"]
    for s in (1, -1):
        tube_ = _box(hbk, ix0 - lt, s * co[0], s * co[1], co[2], co[3]) - _box(hbk - 1, ix0 - lt + 1, s * py0, s * py1, pz0, pz1)
        flange = _box(px1, px1 + 3, s * fl[0], s * fl[1], fl[2], fl[3]) - _box(px1 - 1, px1 + 4, s * co[0], s * co[1], co[2], co[3])
        for (yb, zb) in D["hood_bolts"]:
            flange -= _xcyl(px1 - 1, px1 + 4, s * yb, zb, 2.75)
        collars.append(tube_ + flange)
        # hood: box glued to a back plate; the collar fits the plate's opening
        ya, yb_ = sorted((s * co[0], s * p["hood_y_out"]))
        h = _box(hx_out, hbk, ya, yb_, p["hood_z0"], p["hood_z1"])
        h -= _box(hx_out + t, hbk + 1, ya + t, yb_ - t, p["hood_z0"] + t, p["hood_z1"] - t)
        my0, my1 = sorted((s * D["mouth_y"][0], s * D["mouth_y"][1]))
        h -= _box(hx_out + t, hbk + 1, my0 + t, my1 - t, p["hood_z0"] - 1, p["hood_z0"] + t + 1)
        hoods.append(h)
        pa, pb = sorted((s * (fl[0] - 2), s * p["hood_y_out"]))
        hp = _box(hbk, px0, pa, pb, fl[2] - 7, fl[3] + 7) - _box(hbk - 1, px0 + 1, s * co[0], s * co[1], co[2], co[3])
        for (yb, zb) in D["hood_bolts"]:
            hp -= _xcyl(hbk - 1, px0 + 1, s * yb, zb, 2.75)
            hbolts.append(_bolt("x", px1 + 3, hbk, s * yb, zb, d=5.0))
        hplates.append(hp)
    add("collars", "Collars (2)", _fuse(collars), 10, "pvc_sheet", "collars")
    add("hoods", "Hoods (2)", _fuse(hoods), 10, "pvc_sheet", "hoods")
    add("hood_plates", "Hood back plates (2)", _fuse(hplates), 10, "pvc_sheet", "hoods")
    add("hood_bolts", "M5 bolts through collar, panel and hood (8)", _fuse(hbolts), 13, "steel", None)

    # ---- 11 sill bracket: plate, cleats, struts with flattened ends, wall foot with rubber pad
    bw = p["bracket_w"] / 2
    btk = p["bracket_t"]
    ang, at = p["angle"]
    cll = p["cleat_len"]
    ry0, ry1 = p["rail_y"]
    plate = _box(0, p["bracket_x1"], ry0, ry1, S - btk, S) + _box(0, p["bracket_x1"], -ry0, -ry1, S - btk, S)
    xs, zs = D["strut_top"]
    xf, zf = D["strut_foot"]
    tf = D["tab_face"]
    ux, uz = D["strut_u"]
    fh, ft = p["foot_bar"]
    pt_ = p["pad_t"]
    zfoot = p["foot_z"]
    pb, cb, sb = [], [], []
    for (bxp, byp) in p["plate_bolts"]:
        for s in (1, -1):
            plate -= _zcyl(S - btk - 1, S + 1, bxp, s * byp, 2.75)
            pb.append(_bolt("z", S - btk, S + st, bxp, s * byp, d=5.0))
    # top cleat: horizontal leg under the plate, upright leg carries the strut head
    ctx0 = xs - 27.0
    cleat_t = (_box(ctx0, ctx0 + cll, tf, tf + ang, S - btk - at, S - btk)
               + _box(ctx0, ctx0 + cll, tf, tf + at, S - btk - ang, S - btk))
    ycs = tf + ang / 2 + at / 2
    bar = _box(pt_, pt_ + ft, -bw, bw, zfoot - fh / 2, zfoot + fh / 2)
    cleat_f = (_box(pt_ + ft, pt_ + ft + at, tf, tf + ang, zfoot - cll / 2, zfoot + cll / 2)
               + _box(pt_ + ft, pt_ + ft + ang, tf, tf + at, zfoot - cll / 2, zfoot + cll / 2))
    for (hx, hz) in D["top_holes"]:
        cleat_t -= _ycyl(tf - 1, tf + at + 1, hx, hz, 3.3)
        sb.append(_bolt("y", p["strut_y"] - 1.5, tf + at, hx, hz, d=6.0, head=10.0, nut=10.0))
    for (hx, hz) in D["foot_holes"]:
        cleat_f -= _ycyl(tf - 1, tf + at + 1, hx, hz, 3.3)
        sb.append(_bolt("y", p["strut_y"] - 1.5, tf + at, hx, hz, d=6.0, head=10.0, nut=10.0))
    # countersunk M5 screws: the head sits in a 9 mm countersink, flush with the face
    for xx in (ctx0 + 10, ctx0 + cll - 10):
        cleat_t -= _zcyl(S - btk - at - 1, S - btk + 1, xx, ycs, 2.75)
        cb.append(_zcyl(S - 3, S, xx, ycs, 4.5) + _zcyl(S - btk - at, S - 3, xx, ycs, 2.5)
                  + _zcyl(S - btk - at - 4, S - btk - at, xx, ycs, 4.6))
        for s in (1, -1):
            plate -= _zcyl(S - btk - 1, S + 1, xx, s * ycs, 2.75)
            plate -= _zcyl(S - 3, S + 1, xx, s * ycs, 4.5)
    for zz in (zfoot - 15, zfoot + 15):
        cleat_f -= _xcyl(pt_ + ft - 1, pt_ + ft + at + 1, ycs, zz, 2.75)
        cb.append(_xcyl(pt_, pt_ + 3, ycs, zz, 4.5) + _xcyl(pt_ + 3, pt_ + ft + at, ycs, zz, 2.5)
                  + _xcyl(pt_ + ft + at, pt_ + ft + at + 4, ycs, zz, 4.6))
        for s in (1, -1):
            bar -= _xcyl(pt_ - 1, pt_ + ft + 1, s * ycs, zz, 2.75)
            bar -= _xcyl(pt_ - 1, pt_ + 3, s * ycs, zz, 4.5)
    pad = _box(0, pt_, -bw, bw, zfoot - fh / 2, zfoot + fh / 2)
    # strut: round tube between flattened ends; each flat is 3 mm thick on the strut's axis plane,
    # rounded to tab_r at the end hole, with two holes hole_pitch apart
    sy = p["strut_y"]
    tl, trr = p["tab"], p["tab_r"]
    r, rw = p["strut_r"], p["strut_wall"]

    def tab(xc, zc, sgn):
        from build123d import Plane, Box, Pos
        pl = Plane(origin=(xc, sy, zc), x_dir=(sgn * ux, 0, sgn * uz), z_dir=(0, 1, 0))
        b_ = pl * (Pos(tl / 2, 0, 0) * Box(tl, 2 * trr, 3)) + _ycyl(sy - 1.5, sy + 1.5, xc, zc, trr)
        for k in (0, 1):
            hx, hz = xc + sgn * k * p["hole_pitch"] * ux, zc + sgn * k * p["hole_pitch"] * uz
            b_ -= _ycyl(sy - 2, sy + 2, hx, hz, 3.3)
        return b_
    strut = (tab(xf, zf, 1) + tab(xs, zs, -1)
             + _tube((xf + tl * ux, sy, zf + tl * uz), (xs - tl * ux, sy, zs - tl * uz), r, r - rw))
    both = lambda sh: sh + _mirror_y(sh)  # noqa: E731
    add("bplate", "Bracket rails (2)", plate, 11, "aluminium", "bracket")
    add("cleats", "Angle cleats (4)", both(cleat_t) + both(cleat_f), 11, "aluminium", "bracket")
    add("struts", "Struts (2)", both(strut), 11, "aluminium", "bracket")
    add("foot", "Wall foot bar", bar, 11, "aluminium", "foot")
    add("pad", "Rubber wall pad", pad, 11, "rubber", "foot")
    add("plate_bolts", "M5 bolts, bracket rails to housing (4)", _fuse(pb), 13, "steel", None)
    add("cleat_bolts", "M5 and M6 bolts, cleats and struts", both(_fuse(cb)) + both(_fuse(sb)), 13, "steel", None)

    # ---- 12 adapter at a wall socket, low-voltage cable to the gland in the side wall
    psu = _box(0, 45, 520, 590, 300, 380)
    cable = (_tube((45, 555, 340), (60, 555, 340), 3) + _tube((60, 555, 340), (350, 300, 1100), 3)
             + _tube((350, 300, 1100), (350, hy + 8, 1100), 3))
    add("psu", "24 V adapter and cable", psu + cable, 12, "psu", "power")
    gland = _ycyl(hy, hy + 8, 350.0, 1100.0, 8.0) + _ycyl(hy - st - lt, hy, 350.0, 1100.0, 5.5)
    add("gland", "Cable gland, power entry", gland, 13, "nylon", None)
    return C


def build_parts(p=PARAMS):
    """Return [(name, shape, colour, bom_no, explode_offset)] for the unit (items 1 to 12), each BOM
    line fused from its components. Fixings (line 13) are left out."""
    C = build_components(p)
    by = {}
    for c in C.values():
        if c.bom == 13:
            continue
        by.setdefault(c.bom, []).append(c.shape)
    return [(NAMES[b], _fuse(by[b]), COLOURS[b], b, EXPLODE[b]) for b in sorted(by)]


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


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(p=PARAMS):
    """Pairs that must touch and pairs that must keep a clearance (mm). Returns a list of
    (description, overlap volume mm3, gap mm, expectation, ok). Also checks every pair of
    components for overlap."""
    C = build_components(p)
    ctx = context_parts(p)
    S_ = lambda k: C[k].shape  # noqa: E731
    rows = []

    def chk(desc, a, b_, expect):
        v = _vol(a, b_)
        gp = a.distance_to(b_)
        ok = v < 1e-2 and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    T = "touch"
    shell = S_("base") + S_("sides") + S_("end_out") + S_("end_room")
    # housing construction
    chk("Sides stand on the base", S_("sides"), S_("base"), T)
    chk("End walls stand on the base", S_("end_out") + S_("end_room"), S_("base"), T)
    chk("End walls fit between the sides", S_("end_out") + S_("end_room"), S_("sides"), T)
    chk("Battens in the corners, against the boards", S_("battens"), shell, T)
    chk("Lining on the boards", S_("lining"), shell, T)
    chk("Lining against the battens", S_("lining"), S_("battens"), T)
    chk("Lid on the wall tops", S_("lid"), shell, T)
    chk("Lid lining plug inside the walls (clearance)", S_("lid_lining"), S_("lining"), 0.5)
    chk("Lid lining on the lid board", S_("lid_lining"), S_("lid"), T)
    chk("Latches on the side walls", S_("latches"), S_("sides"), T)
    chk("Latch keepers on the lid", S_("latches"), S_("lid"), T)
    chk("Grilles on the room end and the lid", S_("grilles"), S_("end_room") + S_("lid"), T)
    # partitions
    for k in ("frames", "div_out", "div_core", "div_room", "bulkhead"):
        chk(f"{C[k].name} stand on the floor lining", S_(k), S_("lining"), T)
        chk(f"{C[k].name} under the lid lining", S_(k), S_("lid_lining"), T)
    chk("Outdoor-end divider meets the core face", S_("div_out"), S_("core"), T)
    chk("Core-side divider meets the core face", S_("div_core"), S_("core"), T)
    chk("Core-side divider meets the bulkhead", S_("div_core"), S_("bulkhead"), T)
    chk("Room-side divider meets the bulkhead", S_("div_room"), S_("bulkhead"), T)
    chk("Room-side divider meets the room end lining", S_("div_room"), S_("lining"), T)
    # core seat
    chk("Core ends against both core frames", S_("core"), S_("frames"), T)
    chk("Core on the tray pads", S_("core"), S_("tray"), T)
    chk("Core under the lid hold-down", S_("core"), S_("lid_lining"), T)
    chk("Tray on the floor lining", S_("tray"), S_("lining"), T)
    chk("Tray between the core frames", S_("tray"), S_("frames"), T)
    chk("Drain tube through the tray end wall", S_("drain"), S_("tray"), T)
    chk("Drain tube clear of the core frame hole", S_("drain"), S_("frames"), 0.4)
    chk("Drain tube clear of the outdoor end wall hole", S_("drain"), S_("end_out"), 0.9)
    chk("Drain tube clear of the panel hole", S_("drain"), S_("panel"), 0.9)
    chk("Drain tube clear of the hoods", S_("drain"), S_("hoods") + S_("hood_plates"), 20.0)
    # fans
    chk("Supply fan on the bulkhead (room side)", S_("fan_s"), S_("bulkhead"), T)
    chk("Exhaust fan on the bulkhead (core side)", S_("fan_e"), S_("bulkhead"), T)
    chk("Exhaust fan clear of the core frame", S_("fan_e"), S_("frames"), 1.5)
    chk("Supply fan clear of the room-side divider", S_("fan_s"), S_("div_room"), 50.0)
    chk("Exhaust fan clear of the core-side divider", S_("fan_e"), S_("div_core"), 50.0)
    chk("Supply fan clear of the lid", S_("fan_s"), S_("lid_lining"), 30.0)
    # filters
    chk("Supply filter against the end lining lip", S_("sfilter"), S_("lining"), T)
    chk("Supply filter in its seat", S_("sfilter"), S_("seats"), T)
    chk("Supply filter under its top block", S_("sfilter"), S_("lid_lining"), T)
    chk("Exhaust filter against the room end lining lip", S_("efilter"), S_("lining"), T)
    chk("Exhaust filter in its seat", S_("efilter"), S_("seats"), T)
    chk("Exhaust filter under its top block", S_("efilter"), S_("lid_lining"), T)
    chk("Filter seats on the lining", S_("seats"), S_("lining"), T)
    # controls
    chk("Controller on the room-side divider", S_("ctrl"), S_("div_room"), T)
    chk("Controller clear of the exhaust filter seat", S_("ctrl"), S_("seats"), 3.0)
    chk("Status board behind the room end lining", S_("status"), S_("lining"), T)
    chk("Power gland in the side wall", S_("gland"), S_("sides"), T)
    # window insert
    chk("Panel on the sill", S_("panel"), ctx["wall"], T)
    chk("Panel seals against the jambs", S_("seals"), ctx["frame"], T)
    chk("Panel under the raised lower sash", S_("panel"), ctx["lower_sash"], T)
    chk("Collar flanges on the panel's room face", S_("collars"), S_("panel"), T)
    chk("Hood back plates on the panel's outdoor face", S_("hood_plates"), S_("panel"), T)
    chk("Hoods on their back plates", S_("hoods"), S_("hood_plates"), T)
    chk("Collars in the hood back plates", S_("collars"), S_("hood_plates"), T)
    chk("Bolts through collar flange, panel and hood plate", S_("hood_bolts"), S_("collars") + S_("hood_plates"), T)
    chk("Hood bolts clear of the hoods", S_("hood_bolts"), S_("hoods"), 0.5)
    chk("Collars stop against the end lining", S_("collars"), S_("lining"), T)
    chk("Collars clear of the housing port (2 mm gasket)", S_("collars"), S_("end_out"), 1.9)
    chk("Collar flanges clear of the housing back (stop bead space)", S_("collars"), S_("base") + S_("sides"), 10.0)
    chk("Hoods clear of the outer sill", S_("hoods") + S_("hood_plates"), ctx["wall"], 4.0)
    chk("Hoods clear of the window frame", S_("hoods") + S_("hood_plates"), ctx["frame"], 50.0)
    chk("Housing clear of the lower sash", shell + S_("lid"), ctx["lower_sash"], 5.0)
    chk("Housing base on the sill", S_("base"), ctx["wall"], T)
    # bracket
    chk("Bracket rails under the housing base", S_("bplate"), S_("base"), T)
    chk("Bracket rails at the wall face", S_("bplate"), ctx["wall"], T)
    chk("Rail bolts through rails and base", S_("plate_bolts"), S_("bplate") + S_("base"), T)
    chk("Rail bolt nuts clear of the floor lining", S_("plate_bolts"), S_("lining"), 0.5)
    chk("Cleats under the rails and on the foot bar", S_("cleats"), S_("bplate") + S_("foot"), T)
    chk("Struts' flattened ends on the cleats", S_("struts"), S_("cleats"), T)
    chk("Struts clear of the rails", S_("struts"), S_("bplate"), 2.0)
    chk("Struts clear of the foot bar", S_("struts"), S_("foot"), 2.0)
    chk("Struts clear of the cleat bolts' heads and nuts", S_("struts"), S_("plate_bolts"), 5.0)
    chk("Foot bar on its pad", S_("foot"), S_("pad"), T)
    chk("Pad against the wall", S_("pad"), ctx["wall"], T)
    chk("Struts clear of the wall", S_("struts"), ctx["wall"], 5.0)
    chk("Adapter cable clear of the bracket", S_("psu"), S_("bplate") + S_("struts"), 10.0)
    # every pair of components: no overlap
    keys = list(C)
    bbs = {k: C[k].shape.bounding_box() for k in keys}

    def bb_hit(a, b_):
        A, B = bbs[a], bbs[b_]
        return not (A.max.X < B.min.X or B.max.X < A.min.X or A.max.Y < B.min.Y or B.max.Y < A.min.Y
                    or A.max.Z < B.min.Z or B.max.Z < A.min.Z)
    worst = []
    for i, a in enumerate(keys):
        for b_ in keys[i + 1:]:
            if bb_hit(a, b_):
                v = _vol(C[a].shape, C[b_].shape)
                if v > 1e-2:
                    worst.append((a, b_, v))
    for k in keys:
        for cname in ("wall", "frame", "lower_sash"):
            v = _vol(C[k].shape, ctx[cname])
            if v > 1e-2:
                worst.append((k, cname, v))
    rows.append((f"No two components overlap ({len(keys)} components and the window)", sum(w[2] for w in worst), 0.0, "none", not worst))
    for a, b_, v in worst:
        rows.append((f"  overlap {a} / {b_}", v, 0.0, "none", False))
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else ("no overlap" if exp == "none" else f">= {exp:g} mm")
        print(f"  {'ok ' if ok else 'BAD'}  {desc:62s} overlap {v:9.3f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    from build123d import export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    for name, shape in assemblies(parts).items():
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"), tolerance=0.2, angular_tolerance=0.3)
        bb = shape.bounding_box()
        print(f"{name:26s} {bb.size.X:6.1f} x {bb.size.Y:6.1f} x {bb.size.Z:6.1f} mm")
    d = derived()
    print(f"hood mouth clear distance {d['mouth_clear']:.0f} mm; hood outer edge +/-{PARAMS['hood_y_out']:.0f} mm; "
          f"panel half-length {d['panel_half']:.0f} mm")
    print(f"strut {d['strut_len']:.1f} mm between end holes at {d['strut_angle']:.1f} deg; top holes {d['top_holes']}; foot holes {d['foot_holes']}")
    print_checks()
