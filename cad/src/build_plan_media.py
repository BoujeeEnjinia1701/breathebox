"""BreatheBox prototype build plan pictures (BBX-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|wiring ...]
With no argument it draws everything. A sheet or step number after the group draws only that one
(for example `sheets 103` or `steps 7`), which keeps memory low. Every picture is drawn from
cad/src/model.py (build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/BBX-DWG-101 to 114        making sketches for the made and drilled components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.

Views: the room face of the unit is +X. "Left" and "right" in the notes are as seen standing in
the room looking at the unit; right is +Y, the supply side.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, context_parts, _box  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-09-30"
P2 = dict(rev="P2", date="2026-10-02", revisions=[("P1", "Making sketch for the prototype build plan", "2026-09-30", "AC"),
                                              ("P2", "Wall foot at 400 mm, longer struts (BBX-DEC-001)", "2026-10-02", "AC")])
D = derived(P)
C = build_components(P)
CTX = context_parts(P)


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


S = lambda *ks: _fuse([C[k].shape for k in ks])  # noqa: E731

COL = {"shell": "#D6D3D1", "battens": "#A16207", "lining": "#64748B", "frames": "#16A34A", "dividers": "#22D3EE",
       "bulkhead": "#155E75", "seats": "#B45309", "fan_s": "#0F766E", "fan_e": "#C2410C", "ctrl": "#7C3AED",
       "tray": "#0EA5E9", "core": "#D4A017", "sfilter": "#2563EB", "efilter": "#94A3B8", "grilles": "#9CA3AF",
       "lid": "#E7F0EE", "lidlin": "#94A3B8", "latches": "#111827", "rails": "#6B7280", "struts": "#4B5563",
       "foot": "#374151", "pad": "#111827", "panel": "#A7C4BC", "collars": "#C2410C", "hoods": "#334155",
       "psu": "#111827", "bolt": "#111827", "wall": "#E5E7EB"}


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def made():
    """Named components in build order."""
    return {
        "shell": part("Housing boards and corner battens", S("base", "sides", "end_out", "end_room", "battens"), COL["shell"]),
        "rails": part("Bracket rails with top cleats", S("bplate") + _top_cleats(), COL["rails"]),
        "lining": part("Foam lining", S("lining"), COL["lining"]),
        "frames": part("Core frames (2)", S("frames"), COL["frames"]),
        "dividers": part("Dividers (3)", S("div_out", "div_core", "div_room"), COL["dividers"]),
        "bulkhead": part("Fan bulkhead", S("bulkhead"), COL["bulkhead"]),
        "seats": part("Filter seat strips and stops", S("seats"), COL["seats"]),
        "fans": part("Supply and exhaust fans", S("fan_s", "fan_e"), COL["fan_s"]),
        "controls": part("Controller and status board", S("ctrl", "status"), COL["ctrl"]),
        "tray": part("Condensate tray and drain tube", S("tray", "drain"), COL["tray"]),
        "core": part("Counterflow core", S("core"), COL["core"]),
        "filters": part("Supply and exhaust filters", S("sfilter", "efilter"), COL["sfilter"]),
        "grilles": part("Grilles (2)", S("grilles"), COL["grilles"]),
        "lid": part("Lid with lining, foam blocks and latches", S("lid", "lid_lining", "latches"), COL["lid"]),
        "struts": part("Struts (2)", S("struts"), COL["struts"]),
        "foot": part("Wall foot, pad and foot cleats", S("foot", "pad") + _foot_cleats(), COL["foot"]),
        "panel": part("Window insert panel", S("panel", "seals"), COL["panel"]),
        "collars": part("Collars (2)", S("collars"), COL["collars"]),
        "hoods": part("Hoods with back plates (2)", S("hoods", "hood_plates"), COL["hoods"]),
        "psu": part("24 V adapter and cable", S("psu"), COL["psu"]),
        "jammer": part("Sash jammer (bought)", S("jammer"), "#B91C1C"),
    }


def _split_cleats():
    """The cleats component holds the top and foot cleats of both sides; split them by height."""
    from build123d import Compound
    sol = C["cleats"].shape.solids()
    top = [s for s in sol if s.center().Z > 700]
    foot = [s for s in sol if s.center().Z <= 700]
    return Compound(children=top), Compound(children=foot)


def _top_cleats():
    return _split_cleats()[0]


def _foot_cleats():
    return _split_cleats()[1]


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    off = {"shell": (0, 0, 0), "rails": (0, 0, -200), "lining": (0, 0, 400), "frames": (0, 820, -150),
           "dividers": (0, 820, -430), "bulkhead": (0, 820, 380), "seats": (0, -820, -150), "fans": (0, 820, 640),
           "controls": (0, -820, 80), "tray": (0, -820, 300), "core": (0, -820, 520), "filters": (0, -820, 800),
           "grilles": (0, 0, 1020), "lid": (0, 0, 740), "struts": (0, 0, -330), "foot": (0, 0, -380),
           "panel": (0, 0, -1400), "collars": (300, 0, -1400), "hoods": (-330, 0, -1400), "psu": (250, 500, -350),
           "jammer": (0, -450, -1500)}
    parts = []
    for k, p in M.items():
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "BreatheBox prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the room side, right and above; right (supply side) is toward you",
                       elev=20, azim=28, size=(12, 10), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def _rot(shape, rx=0, ry=0, rz=0):
    from build123d import Rot
    return Rot(rx, ry, rz) * shape


def _centre(shape):
    from build123d import Pos
    c = shape.bounding_box().center()
    return Pos(-c.X, -c.Y, -c.Z) * shape


SHEETS = {}


def sheet(n):
    def deco(f):
        SHEETS[n] = f
        return f
    return deco


BASE = dict(project="BreatheBox", date=DATE)


def _sheet(key, shape, neighbours, n, title, material, notes, view_shape=None, inset=(24, 35), rev=None):
    kw = dict(BASE)
    if rev:
        kw.update(rev)
    return bv.component_sheet(Part(key, shape, "#0F766E"), neighbours, dwg_no=f"BBX-DWG-{n}", title=f"BreatheBox {title}: making sketch",
                              material=material, notes=notes, view_shape=view_shape, inset_view=inset, out_dir=str(DWG), **kw)


def _grey(*keys):
    return [Part(k, S(k), "#D1D5DB") for k in keys]


@sheet(101)
def s101():
    shell = S("base", "sides", "end_out", "end_room", "battens")
    return _sheet("Housing boards", shell, _grey("bplate", "panel"), 101, "housing boards and battens",
                  "6 mm PVC foam board; 10 x 10 mm PVC or pine strip",
                  ["Cut from 6 mm PVC foam board: base 510 x 560; two sides 510 x 238;",
                   "  two ends 548 x 238. Ends fit between the sides; all stand on the base.",
                   "Outdoor end: two 160 x 180 openings centred 185 left and right,",
                   "  from 24 to 204 up from its bottom edge; a 14 hole 40 left, 16 up.",
                   "Room end: a 220 x 190 opening from 30 to 250 left, 24 to 214 up;",
                   "  holes 6 and 12 at 150 and 170 right, 199 up (light and button).",
                   "Right side: a 12 hole 50 from the room end, 194 up (power gland).",
                   "Base: four 5.5 holes, 140 and 440 from the outdoor edge, 175 each side.",
                   "Battens 10 x 10: four uprights 238; two 478 under the sides; two 528",
                   "  under the ends. Glue every joint with PVC cement and screw each",
                   "  board into the batten behind it, 3.5 x 16 screws at 80 centres.",
                   "Check: square within 1 mm on the diagonals; openings line up with",
                   "  the collar and grille positions on the other sketches."],
                  view_shape=shell, inset=(24, 35))


@sheet(102)
def s102():
    lid = S("lid", "lid_lining", "latches")
    return _sheet("Lid", lid, _grey("base", "sides", "end_out", "end_room"), 102, "lid", "6 mm PVC foam board; 10 mm closed-cell foam",
                  ["Board 510 x 560 x 6 mm. Opening 70 x 220 for the supply grille,",
                   "  420 to 490 from the outdoor edge, 40 to 260 right of centre.",
                   "Lining plug: 10 mm foam, 476 x 526, glued centred under the board so",
                   "  it drops inside the wall lining with 1 mm all round; cut the same",
                   "  70 x 220 opening through it.",
                   "Foam blocks glued under the plug (they hold the core and filters):",
                   "  core hold-down 306 long x 168 wide x 24 deep, over the core;",
                   "  supply filter block 34 x 138 x 28 at the outdoor end, right;",
                   "  exhaust filter block 21 x 200 x 18 at the room end, left.",
                   "Latch keepers: one each side, 118 to 142 from the outdoor edge.",
                   "Check: the lid drops on with the plug inside the walls and the",
                   "  latches pull it down evenly onto the gasket tape."],
                  inset=(30, 35))


@sheet(103)
def s103():
    fr = S("frames")
    one = fr & _box(-60, -30, -300, 300, 900, 1200)
    return _sheet("Core frame", one, _grey("core", "tray", "div_out", "base", "sides"), 103, "core frame (make 2)",
                  "3 mm PVC foam board",
                  ["Make two from 3 mm PVC foam board, each 528 wide x 218 tall.",
                   "Cut a U 168 wide, centred, from 20 up off the bottom edge to the top.",
                   "  The core's 180 wide end then overlaps the U by 6 each side and 6",
                   "  at the bottom; stick 3 mm foam gasket tape round the U on the",
                   "  core side.",
                   "Outdoor frame only: a 13 hole 40 left of centre (as seen from the room;",
                   "  drawn here as seen from outdoors), 6 up, for the drain tube.",
                   "Fit: stands on the floor lining, glued to the side lining with",
                   "  contact adhesive, 300 apart (inside faces) so the core fits",
                   "  between them; the lid's foam block closes the U above the core.",
                   "Check: the core drops between the frames without force and both",
                   "  ends bear on the gasket all round the U."],
                  view_shape=_rot(_centre(one), 0, 0, 90), inset=(25, 40))


@sheet(104)
def s104():
    dv = S("div_out", "div_core", "div_room")
    from build123d import Pos
    lay = _fuse([Pos(0, 0, 0) * _centre(S("div_out")), Pos(0, 0, 0) * (Pos(70, 0, 0) * _centre(S("div_core"))),
                 Pos(170, 0, 0) * _centre(S("div_room"))])
    return _sheet("Dividers", dv, _grey("frames", "bulkhead", "core", "base"), 104, "dividers (3)", "3 mm PVC foam board",
                  ["Three pieces of 3 mm PVC foam board, all 218 tall, on the centre line.",
                   "Outdoor-end divider: 51 long, plus a tongue 3 long x 174 tall,",
                   "  20 up from the bottom, that reaches through the frame's U to the",
                   "  core face (drawn left).",
                   "Core-side divider: 37 long plus the same tongue (drawn middle).",
                   "Room-side divider: 78 long, plain (drawn right).",
                   "Fit: each stands on the floor lining, glued to the frame, bulkhead",
                   "  or end lining it meets; the tongue's end just touches the core.",
                   "The dividers split each end of the box into supply (right) and",
                   "  exhaust (left), so the two air streams never meet.",
                   "Check: no daylight past any divider edge with the core in."],
                  view_shape=lay, inset=(30, 45))


@sheet(105)
def s105():
    b = S("bulkhead")
    return _sheet("Fan bulkhead", b, _grey("fan_s", "fan_e", "div_core", "div_room", "base"), 105, "fan bulkhead",
                  "6 mm PVC foam board",
                  ["6 mm PVC foam board, 528 wide x 218 tall.",
                   "Two 81 holes for the fan inlets, centred 150 left and 150 right of",
                   "  centre, 94 up from the bottom edge.",
                   "Mark each fan's four mounting holes through the fan itself; drill 5",
                   "  and fit rubber grommets so the fans do not drum on the board.",
                   "Fit: stands on the floor lining, its room-side face 94 from the",
                   "  outside of the room end (78 from the end lining), glued to the",
                   "  side linings. Drawn as seen from outdoors.",
                   "The supply fan (right) goes on the room side, its inlet through the",
                   "  hole; the exhaust fan (left) goes on the core side, its inlet",
                   "  through the hole facing the room. M4 nylon screws.",
                   "Check: each fan ring sits in its hole with about 0.5 mm all round."],
                  view_shape=_rot(_centre(b), 0, 0, 90), inset=(30, 40))


@sheet(106)
def s106():
    sd = S("seats")
    sup = sd & _box(-120, 0, 0, 300, 900, 1200)
    return _sheet("Filter seats", sd, _grey("sfilter", "efilter"), 106, "filter seat strips and stops",
                  "10 x 10 mm PVC or pine strip",
                  ["All 10 x 10 strip, glued to the lining with contact adhesive.",
                   "Supply seat (outdoor end, right; drawn here): a side strip 218 long",
                   "  against the end lining beside the filter's left edge; two lip",
                   "  strips 218 long 25 out from the end lining, lapping 6 over each",
                   "  filter edge; a bottom stop 150 x 25 x 20 under the filter.",
                   "Exhaust seat (room end, left): side strips 218 long each side of",
                   "  the pad against the room end lining; lip strips 12 out from it,",
                   "  lapping 10 over each pad edge; a bottom stop 220 x 12 x 10.",
                   "The air pushes each filter onto its lips; the lid's foam blocks",
                   "  press on the top edges, so no air goes round a filter.",
                   "Check: each filter slides down into its seat by hand and sits",
                   "  square on its lips and stop."],
                  view_shape=_rot(_centre(sup), 0, 0, 90), inset=(30, 50))


@sheet(107)
def s107():
    t = S("tray")
    return _sheet("Condensate tray", t, _grey("frames", "drain", "base"), 107, "condensate tray", "PETG sheet 2 mm",
                  ["2 mm PETG sheet. Blank 328 x 228; fold up 14 mm on all four sides",
                   "  (heat gun and a wooden former), so the tray is 300 x 200 x 14.",
                   "Seal each corner inside with a fillet of clear silicone.",
                   "Drain hole 12 in the outdoor end wall, 40 left of centre, its",
                   "  centre 6 up from the underside so the bore is flush with the floor.",
                   "Four pads 20 x 20 x 12 cut from PETG offcuts stacked and glued, at",
                   "  the four corners, 10 in from each end and 60 out from the centre",
                   "  line; the core sits on them, so water runs freely underneath.",
                   "Fit: sits on the floor lining between the core frames.",
                   "Check: fill with 100 ml of water with the drain tube fitted; it all",
                   "  runs out with the box level, and no corner weeps."],
                  inset=(50, 35))


@sheet(108)
def s108():
    pnl = S("panel")
    return _sheet("Insert panel", pnl, _grey("collars", "hoods", "hood_plates") + [Part("wall", CTX["frame"], "#E5E7EB")], 108,
                  "window insert panel", "20 mm panel, PVC foam skins over XPS",
                  ["20 mm panel, 260 tall, cut to the window's clear width less 6",
                   "  (894 for a 900 window), so the EPDM seals take up 3 each end.",
                   "Two 158 x 178 cut-outs centred 185 left and right of centre, from",
                   "  31 to 209 up from the bottom edge.",
                   "Drain hole 14, 40 left of centre as seen from the room, 22 up",
                   "  (drawn as seen from outdoors, so it appears right of centre).",
                   "Bolt holes 5.5: at 93 and 277 out from centre on each side, 19 and",
                   "  221 up (eight in all). Drill them through the collar flange",
                   "  clamped in place, so they match.",
                   "Seal the cut edges of the XPS core with aluminium tape.",
                   "Fit: stands on the sill in the lower sash's track; the raised sash",
                   "  closes down on its top edge.",
                   "Check: slides into the track with the seals just touching the jambs."],
                  view_shape=_rot(_centre(pnl), 0, 0, 90), inset=(20, 150))


@sheet(109)
def s109():
    col = S("collars") & _box(-200, 0, 0, 400, 800, 1200)
    return _sheet("Collar", col, _grey("panel", "hood_plates", "end_out", "sfilter"), 109, "collar (make 2)", "3 mm rigid PVC sheet",
                  ["A rectangular tube, bore 150 x 170, from four strips of 3 mm PVC",
                   "  glued with PVC cement: two 49 x 156 and two 49 x 170.",
                   "  49 is the design-case length: cut it so the collar reaches from",
                   "  the hood plate's outside face to the housing's end lining.",
                   "Flange: a 3 mm PVC frame 196 x 216 with a 156 x 176 hole, glued",
                   "  round the tube 23 from its outdoor end.",
                   "Four 5.5 holes in the flange, 6 in from the long edges and 7 in",
                   "  from the short edges (at its corners).",
                   "Fit: the outdoor end goes through the panel cut-out into the hood",
                   "  back plate; the flange lies on the panel's room face; four M5",
                   "  bolts clamp flange, panel and hood plate. The room end slides",
                   "  6 into the housing opening on 2 mm foam gasket.",
                   "Check: bore square; flange flat on the panel."],
                  view_shape=_rot(_centre(col), 0, 0, 90), inset=(25, 150))


@sheet(110)
def s110():
    hd = (S("hoods") + S("hood_plates")) & _box(-400, 0, 0, 400, 800, 1200)
    return _sheet("Hood", hd, _grey("panel", "collars"), 110, "hood with back plate (make 2)", "3 mm rigid PVC sheet; 1 mm stainless mesh",
                  ["Back plate: 3 mm PVC, 255 wide x 230 tall, with a 156 x 176 hole",
                   "  for the collar and four 5.5 holes matching the collar flange.",
                   "Hood box from 3 mm PVC, glued to the plate's outer face: top",
                   "  180 x 233, two sides 180 x 187, outer end 233 x 187; open at the",
                   "  back (onto the plate) and at the bottom over the outer 124 mm of",
                   "  its width (the mouth); the inner 106 mm of the bottom is closed.",
                   "Mesh: 1 mm stainless mesh over the mouth, held by 10 mm PVC strips",
                   "  glued inside the mouth edges.",
                   "The two hoods are mirror images; mouths face down and point",
                   "  outward, 420 apart.",
                   "Fit: the collar glues into the plate's hole; the plate is bolted",
                   "  through the panel with the collar flange behind it.",
                   "Check: water poured on the top runs off, none enters the mouth."],
                  view_shape=_rot(_centre(hd), 0, 0, 90), inset=(15, 210))


def _top_hole_text():
    """Top cleat strut holes from the cleat's wall-side end and down from the rail's underside."""
    cx0 = D["strut_top"][0] - 27.0
    zr = P["sill_z"] - P["bracket_t"]
    (a, b), (c, d) = D["top_holes"]
    return (f"{a - cx0:.0f} and {c - cx0:.1f} from the cleat's",
            f"wall-side end, {zr - b:.0f} and {zr - d:.1f} down from the rail's underside")


def _foot_hole_text():
    """Foot cleat strut holes out from the bar's room face and up from the cleat's lower end."""
    xf = P["pad_t"] + P["foot_bar"][1]
    zl = P["foot_z"] - P["cleat_len"] / 2
    (a, b), (c, d) = D["foot_holes"]
    return (f"{a - xf:.0f} and {c - xf:.1f} out from the bar",
            f"face, {b - zl:.0f} and {d - zl:.1f} up from the cleat's lower end")


@sheet(111)
def s111():
    from build123d import Compound
    rail = C["bplate"].shape.solids()
    r1 = [s for s in rail if s.center().Y > 0][0]
    tc = [s for s in _top_cleats().solids() if s.center().Y > 0]
    one = r1 + Compound(children=tc)
    return _sheet("Bracket rail", one, _grey("base", "struts", "end_room"), 111, "bracket rail with its top cleat (make 2)",
                  "Aluminium flat bar 50 x 4; equal angle 40 x 40 x 3",
                  ["Rail: 50 x 4 aluminium flat bar, 390 long. Round the corners.",
                   "Two 5.5 holes for the housing bolts, 30 and 330 from the wall end,",
                   "  25 in from the rail's inner edge.",
                   "Two 5.5 holes countersunk from the top for the cleat, 348 and 378",
                   "  from the wall end, 31 in from the inner edge.",
                   "Cleat: 40 x 40 x 3 angle, 50 long. Flat leg under the rail, 338 to",
                   "  388 from the wall end, holes matching the rail. Upright leg on the",
                   "  rail's inner side: two 6.6 holes, " + _top_hole_text()[0],
                   "  " + _top_hole_text()[1] + ".",
                   "Drill the strut holes with the strut clamped in place (sketch 112).",
                   "Fit: the rail bolts under the housing base with two M5 bolts, nuts",
                   "  inside under the floor lining; its wall end is flush with the",
                   "  housing's line on the wall face."],
                  view_shape=one, inset=(-25, 40), rev=P2)


@sheet(112)
def s112():
    from build123d import Plane
    st = [s for s in C["struts"].shape.solids() if s.center().Y > 0]
    one = _fuse(st)
    ux, uz = D["strut_u"]
    xf, zf = D["strut_foot"]
    flat = Plane(origin=(xf, P["strut_y"], zf), x_dir=(ux, 0, uz), z_dir=(0, -1, 0)).to_local_coords(one)
    return _sheet("Strut", one, _grey("bplate", "foot", "base"), 112, "strut (make 2)", "Aluminium round tube 20 x 1.5 mm, 6063 class",
                  [f"Tube 20 x 1.5, cut {D['strut_len'] + 26:.0f} long.",
                   "Flatten 40 of each end in a vice between two flat bars, both flats",
                   "  in the same plane; anneal with a gas torch first if it cracks.",
                   "Trim each flat to 26 wide and round its end to a 13 radius about",
                   "  the end hole.",
                   f"End holes 6.6, {D['strut_len']:.1f} apart; a second 6.6 hole 20 in",
                   "  from each end hole, on the centre line. Two holes at each end",
                   "  make the joints rigid, so the bracket cannot fold.",
                   f"The strut rises at {D['strut_angle']:.0f} degrees from the wall foot to the rail.",
                   "Drill the second pair with the strut clamped to both cleats, so all",
                   "  four holes line up.",
                   "Fit: M6 bolts, heads on the strut side, nyloc nuts on the cleats.",
                   "Check: end holes within 0.5 of the length; flats not twisted."],
                  view_shape=flat, inset=(15, 60), rev=P2)


@sheet(113)
def s113():
    from build123d import Compound
    fc = [s for s in _foot_cleats().solids()]
    one = S("foot", "pad") + Compound(children=fc)
    return _sheet("Wall foot", one, _grey("struts", "bplate") + [Part("wall", CTX["wall"] & _box(-50, 0, -300, 300, 380, 950), "#E5E7EB")],
                  113, "wall foot with pad and foot cleats", "Aluminium flat bar 60 x 6; angle 40 x 40 x 3; rubber 2 mm",
                  ["Bar: 60 x 6 aluminium flat bar, 400 long. Four 5.5 holes, 181 each",
                   "  side of centre, 15 above and below its centre line, countersunk",
                   "  from the wall side so the screw heads sit flush.",
                   "Pad: 2 mm rubber sheet 400 x 60, glued to the wall side, with",
                   "  relief holes over the screw heads.",
                   "Cleats: 40 x 40 x 3 angle, 50 long. One leg on the bar's room face,",
                   "  holes matching the bar; the other leg points into the room, on",
                   "  the inner side, with two 6.6 holes " + _foot_hole_text()[0],
                   "  " + _foot_hole_text()[1] + ".",
                   f"Fit: the foot's centre line is {P['foot_z']:.0f} above the floor; the pad presses",
                   "  on the wall; nothing is fixed to the wall.",
                   "Check: the pad lies flat on the wall over its whole length."],
                  view_shape=_rot(_centre(one), 0, 0, 90), inset=(20, 60), rev=P2)


@sheet(114)
def s114():
    g = S("grilles")
    eg = g & _box(390, 410, -400, 400, 800, 1200)
    return _sheet("Grilles", g, _grey("end_room", "lid", "sides"), 114, "grilles (2)", "Aluminium sheet 1.5 to 2 mm",
                  ["Exhaust grille (room face, drawn): 240 wide x 210 tall, 21 slots",
                   "  4 wide x 170 long at 10 centres. Supply grille (lid): 90 x 240,",
                   "  6 slots 4 wide x 200 long at 10 centres.",
                   "Or buy perforated aluminium sheet with holes no larger than 5 mm",
                   "  and cut it to the same sizes.",
                   "Drill a 4.5 hole 6 in from each corner; deburr every edge.",
                   "Fit: each grille covers its opening with 10 to spare all round,",
                   "  held by four M4 bolts with nuts inside the box.",
                   "The grilles keep fingers off the fans: no opening wider than 5.",
                   "Check: a pencil cannot pass through any slot."],
                  view_shape=_rot(_centre(eg), 0, 0, 90), inset=(30, 30))


def sheets(which=None):
    out = []
    for n in sorted(SHEETS):
        if which and str(n) not in which:
            continue
        out.append(SHEETS[n]())
    return out


# ----------------------------------------------------------------- joints
def _win(sh, x0, x1, y0, y1, z0, z1):
    return sh & _box(x0, x1, y0, y1, z0, z1)


JOINTS = {}


def joint(n):
    def deco(f):
        JOINTS[n] = f
        return f
    return deco


def _j(n, items, title, sub, elev, azim, box_):
    parts = [part(nm, _win(sh, *box_), col) for nm, sh, col in items]
    return bv.joint(parts, OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", subtitle=sub, elev=elev, azim=azim, size=(8, 6))


@joint(1)
def j1():
    b = (-112, -40, 210, 282, 898, 960)
    return _j(1, [("Base board", S("base"), COL["shell"]), ("Side board", S("sides"), "#A8A29E"),
                  ("Outdoor end board", S("end_out"), "#E7E5E4"), ("Corner battens 10 x 10", S("battens"), COL["battens"]),
                  ("Foam lining", S("lining"), COL["lining"])],
              "housing corner (outdoor end, right, at the base)", "Seen from inside, above. Each board is glued and screwed into the batten behind it",
              40, -140, b)


@joint(2)
def j2():
    b = (-75, 15, -120, 5, 905, 1140)
    return _j(2, [("Core frame", S("frames"), COL["frames"]), ("Counterflow core", S("core"), COL["core"]),
                  ("Tray with pad", S("tray"), COL["tray"]), ("Outdoor-end divider with tongue", S("div_out"), COL["dividers"]),
                  ("Lid foam hold-down", S("lid_lining"), COL["lidlin"]), ("Floor lining", S("lining"), COL["lining"]),
                  ("Drain tube", S("drain"), "#0369A1")],
              "core seat at the outdoor end (cut on the centre line)", "Seen from the left, above. The core end bears on the frame round its U; the tongue meets the core face",
              18, -115, b)


@joint(3)
def j3():
    b = (255, 390, -270, 270, 916, 1010)
    return _j(3, [("Fan bulkhead", S("bulkhead"), COL["bulkhead"]), ("Supply fan (room side)", S("fan_s"), COL["fan_s"]),
                  ("Exhaust fan (core side)", S("fan_e"), COL["fan_e"]), ("Dividers", S("div_core", "div_room"), COL["dividers"]),
                  ("Room-end core frame", S("frames"), COL["frames"]), ("Exhaust filter", S("efilter"), COL["efilter"])],
              "fans on the bulkhead (cut through the fan centres)", "Seen from above. Each inlet ring passes through its hole; supply fan on the room side, exhaust fan on the core side",
              72, -25, b)


@joint(4)
def j4():
    b = (-125, -45, 85, 268, 1000, 1060)
    return _j(4, [("Outdoor end board", S("end_out"), "#A8A29E"), ("End lining with 5 mm lip", S("lining"), COL["lining"]),
                  ("Supply filter", S("sfilter"), COL["sfilter"]), ("Seat strips", S("seats"), COL["seats"]),
                  ("Collar (bore 150 wide)", S("collars"), COL["collars"]), ("Outdoor-end divider", S("div_out"), COL["dividers"])],
              "supply filter seat (cut at mid height)", "Seen from above, room toward the bottom. The air pushes the filter onto its lip strips",
              75, 0, b)


@joint(5)
def j5():
    b = (-200, -95, 259, 284, 900, 1140)
    return _j(5, [("Hood", S("hoods"), "#CBD5E1"), ("Hood back plate", S("hood_plates"), "#475569"),
                  ("Insert panel", S("panel"), COL["panel"]), ("Collar with its flange", S("collars"), "#B45309"),
                  ("M5 bolts, head on the flange, nut on the plate", S("hood_bolts"), COL["bolt"]),
                  ("Housing end board (2 mm gasket gap)", S("end_out"), "#E7E5E4"), ("End lining", S("lining"), COL["lining"])],
              "window insert, right side (cut through the outer bolts)", "Seen from the side, outdoors to the left. Collar flange, panel and hood plate are clamped by M5 bolts",
              8, -90, b)


@joint(6)
def j6():
    b = (-320, -20, -48, -32, 860, 950)
    return _j(6, [("Tray", S("tray"), COL["tray"]), ("Drain tube", S("drain"), "#0369A1"), ("Core frame", S("frames"), COL["frames"]),
                  ("End board, base, batten and lining", S("end_out", "base", "battens", "lining"), "#A8A29E"), ("Insert panel", S("panel"), COL["panel"]),
                  ("Sill", CTX["wall"], COL["wall"])],
              "drain path (cut along the tube)", "Seen from the left. The tube leaves the tray at floor level and falls outdoors",
              12, -90, b)


@joint(7)
def j7():
    b = (325, 395, 140, 205, 840, 912)
    return _j(7, [("Housing base", S("base"), COL["shell"]), ("Bracket rail", S("bplate"), COL["rails"]),
                  ("Top cleat", S("cleats"), "#1D4ED8"), ("Strut (flattened end)", S("struts"), COL["struts"]),
                  ("M5 and M6 bolts", S("cleat_bolts", "plate_bolts"), COL["bolt"])],
              "strut head on the top cleat (right side)", "Seen from below and inside. Two M6 bolts make the joint rigid; two countersunk M5 screws hold the cleat",
              -25, -140, b)


@joint(8)
def j8():
    zf = P["foot_z"]
    b = (0, 60, 135, 210, zf - 35, zf + 40)
    return _j(8, [("Wall face (behind the pad)", CTX["wall"] & _box(-6, 0, 120, 220, zf - 50, zf + 50), COL["wall"]),
                  ("Rubber pad", S("pad"), COL["pad"]), ("Foot bar", S("foot"), "#9CA3AF"),
                  ("Foot cleat", S("cleats"), "#1D4ED8"), ("Strut (flattened end)", S("struts"), COL["struts"]),
                  ("M5 and M6 bolts", S("cleat_bolts"), "#111827")],
              "strut foot on the wall foot (right side)", "Seen from the room, from the centre side and above. The pad only presses on the wall; nothing is fixed to it",
              22, -40, b)


@joint(9)
def j9():
    b = (95, 165, 240, 300, 1095, 1160)
    return _j(9, [("Side board", S("sides"), "#A8A29E"), ("Lid board", S("lid"), COL["lid"]), ("Lid lining plug", S("lid_lining"), COL["lidlin"]),
                  ("Side lining", S("lining"), COL["lining"]), ("Toggle latch and keeper", S("latches"), COL["latches"])],
              "lid and latch (right side)", "Seen from outside, right. The lining plug locates the lid; the latch pulls it onto the gasket",
              20, 60, b)


@joint(10)
def j10():
    b = (345, 405, -270, 0, 1040, 1080)
    return _j(10, [("Room end board", S("end_room"), "#A8A29E"), ("Room end lining with 10 mm lip", S("lining"), COL["lining"]),
                   ("Exhaust filter pad", S("efilter"), COL["efilter"]), ("Seat strips", S("seats"), COL["seats"]),
                   ("Exhaust grille", S("grilles"), "#4B5563"), ("Room-side divider", S("div_room"), COL["dividers"]),
                   ("Controller", S("ctrl"), COL["ctrl"])],
              "exhaust filter seat and grille (cut at mid height)", "Seen from above, room toward the bottom. Room air comes through the grille and pushes the pad onto its lip strips",
              75, 0, b)


def joints(which=None):
    out = []
    for n in sorted(JOINTS):
        if which and str(n) not in which:
            continue
        out.append(JOINTS[n]())
    return out


# ----------------------------------------------------------------- assembly steps
def _mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


STEPS = {}


def step_(n):
    def deco(f):
        STEPS[n] = f
        return f
    return deco


def _st(n, done, new, title, sub, **kw):
    kw.setdefault("elev", 24)
    kw.setdefault("azim", 35)
    return bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw)


def _M():
    return made()


@step_(1)
def st1():
    return _st(1, [part("Base board", S("base"), COL["shell"])],
               [_mv(part("Corner battens", S("battens"), COL["battens"]), (0, 0, 120)),
                _mv(part("Side boards", S("sides"), "#E7E5E4"), (0, 0, 260)),
                _mv(part("End boards", S("end_out", "end_room"), "#A8A29E"), (0, 0, 400))],
               "boards and corner battens", "Glue with PVC cement and screw each board into the batten behind it; check square on the diagonals",
               label_done=True)


@step_(2)
def st2():
    M = _M()
    return _st(2, [M["shell"]], [_mv(M["rails"], (0, 0, -160)), _mv(part("M5 bolts (nuts inside)", S("plate_bolts"), COL["bolt"]), (0, 0, -60))],
               "bracket rails under the base", "Rails with their top cleats; two M5 bolts each, nyloc nuts inside before the lining goes in",
               elev=-25, azim=35, label_done=False)


@step_(3)
def st3():
    M = _M()
    return _st(3, [M["shell"], M["rails"]], [_mv(M["lining"], (0, 0, 300))], "foam lining",
               "Floor first, then sides and ends; contact adhesive; cut round the openings and the bolt nuts", label_done=False)


@step_(4)
def st4():
    M = _M()
    return _st(4, [M["shell"], M["rails"], M["lining"]],
               [_mv(M["frames"], (0, 0, 300)), _mv(M["dividers"], (0, 0, 480)), _mv(M["bulkhead"], (0, 0, 380))],
               "core frames, dividers and fan bulkhead", "Each stands on the floor lining, glued to the side linings; frames 300 apart inside",
               elev=40, azim=35, label_done=False)


@step_(5)
def st5():
    M = _M()
    inside = [M["shell"], M["lining"], M["frames"], M["dividers"], M["bulkhead"]]
    return _st(5, inside, [_mv(M["seats"], (0, 0, 300))], "filter seat strips and stops",
               "Glued to the lining; try each filter in its seat before the glue sets", elev=62, azim=35, label_done=False)


@step_(6)
def st6():
    M = _M()
    inside = [M["shell"], M["lining"], M["frames"], M["dividers"], M["bulkhead"], M["seats"]]
    return _st(6, inside, [_mv(part("Supply fan (room side)", S("fan_s"), COL["fan_s"]), (0, 0, 260)),
                           _mv(part("Exhaust fan (core side)", S("fan_e"), COL["fan_e"]), (0, 0, 360))],
               "fans onto the bulkhead", "Four M4 nylon screws each through rubber grommets; inlet rings through the holes",
               elev=62, azim=35, label_done=False)


@step_(7)
def st7():
    M = _M()
    inside = [M["shell"], M["lining"], M["frames"], M["dividers"], M["bulkhead"], M["seats"], M["fans"]]
    return _st(7, inside, [_mv(part("Controller (intake side of the divider)", S("ctrl"), COL["ctrl"]), (0, -150, 250)),
                           _mv(part("Status board", S("status"), "#A855F7"), (0, 0, 250)),
                           _mv(part("Power cable gland", S("gland"), COL["bolt"]), (0, 120, 0))],
               "controls and power entry", "Controller on M3 standoffs on the divider; gland in the right side; wire as the wiring diagram",
               elev=62, azim=35, label_done=False)


@step_(8)
def st8():
    M = _M()
    inside = [M["shell"], M["lining"], M["frames"], M["dividers"], M["bulkhead"], M["seats"], M["fans"], M["controls"]]
    return _st(8, inside, [_mv(part("Tray with pads", S("tray"), COL["tray"]), (0, 0, 300)),
                           _mv(part("Drain tube", S("drain"), "#0369A1"), (-200, 0, 0))],
               "condensate tray and drain tube", "Tray between the frames; tube through the end wall into the tray, sealed with silicone at each wall",
               elev=62, azim=35, label_done=False)


@step_(9)
def st9():
    M = _M()
    inside = [M["shell"], M["lining"], M["frames"], M["dividers"], M["bulkhead"], M["seats"], M["fans"], M["controls"], M["tray"]]
    return _st(9, inside, [_mv(M["core"], (0, 0, 320))], "counterflow core",
               "Lower it between the frames onto the four pads; its supply channels open to the right at the outdoor end",
               elev=62, azim=35, label_done=False)


@step_(10)
def st10():
    M = _M()
    inside = [M["shell"], M["lining"], M["frames"], M["dividers"], M["bulkhead"], M["seats"], M["fans"], M["controls"], M["tray"], M["core"]]
    return _st(10, inside, [_mv(part("Supply filter", S("sfilter"), COL["sfilter"]), (0, 0, 300)),
                            _mv(part("Exhaust filter pad", S("efilter"), COL["efilter"]), (0, 0, 300))],
               "filters into their seats", "Slide each down behind its lip strips onto its stop; the supply filter's airflow arrow points into the box", elev=62, azim=35, label_done=False)


@step_(11)
def st11():
    M = _M()
    closed = [M["shell"], M["lining"], M["core"], M["fans"]]
    return _st(11, closed, [_mv(part("Exhaust grille", S("grilles") & _box(390, 410, -400, 400, 800, 1200), "#4B5563"), (150, 0, 0))],
               "exhaust grille on the room face", "Four M4 bolts with nuts inside; the supply grille goes on the lid the same way",
               label_done=False)


@step_(12)
def st12():
    M = _M()
    inside = [M["shell"], M["lining"], M["frames"], M["dividers"], M["bulkhead"], M["seats"], M["fans"], M["controls"],
              M["tray"], M["core"], M["filters"], part("Exhaust grille", S("grilles") & _box(390, 410, -400, 400, 800, 1200), COL["grilles"])]
    lid = part("Lid with supply grille, foam blocks and latch keepers", S("lid", "lid_lining") + (S("grilles") & _box(280, 400, -300, 300, 1149, 1160)), COL["lid"])
    lat = S("latches")
    lp = part("Toggle latch (right)", lat & _box(0, 300, 0, 400, 1000, 1200), COL["latches"])
    ln = part("Toggle latch (left)", lat & _box(0, 300, -400, 0, 1000, 1200), COL["latches"])
    return _st(12, inside, [_mv(lid, (0, 0, 280)), _mv(lp, (0, 110, 0)), _mv(ln, (0, -110, 0))],
               "lid on, latches closed", "Gasket tape on the wall tops; the lining plug drops inside; one latch each side",
               elev=30, azim=35, label_done=False)


def _boxed():
    M = _M()
    return [M["shell"], M["rails"], M["lid"], M["grilles"]]


@step_(13)
def st13():
    M = _M()
    return _st(13, _boxed(), [_mv(M["struts"], (120, 0, -120)), _mv(M["foot"], (220, 0, -200)),
                              _mv(part("M6 bolts, two at each strut end", S("cleat_bolts"), COL["bolt"]), (120, 0, -120))],
               "struts and wall foot", "Bolt each strut to its top cleat and to the foot cleat, two M6 bolts at each end; tighten all",
               elev=12, azim=60, label_done=False)


@step_(14)
def st14():
    M = _M()
    return _st(14, [M["panel"]], [_mv(M["collars"], (240, 0, 0)), _mv(M["hoods"], (-260, 0, 0)),
                                  _mv(part("M5 bolts (8)", S("hood_bolts"), COL["bolt"]), (160, 0, 0))],
               "window insert on the bench", "Collars through the panel from the room side, hoods on the outdoor side; four M5 bolts each",
               elev=25, azim=-35, label_done=True)


@step_(15)
def st15():
    M = _M()
    insert = part("Window insert (panel, collars, hoods)", S("panel", "seals", "collars", "hoods", "hood_plates", "hood_bolts"), COL["panel"])
    ctx = [part("Wall", CTX["wall"] & _box(-260, 10, -700, 700, 500, 2150), COL["wall"]),
           part("Frame and sashes", CTX["frame"] + CTX["lower_sash"] + CTX["upper_sash"], COL["wall"])]
    jam = part("Sash jammer (in the inner track)", S("jammer"), "#B91C1C")
    return _st(15, [], [_mv(insert, (0, 0, 220)), _mv(jam, (160, 0, 0))], "insert into the window, sash jammer fitted",
               "Raise the lower sash, set the insert in its track, hoods outside; close the sash onto it, then wedge the jammer above it",
               context=ctx, elev=18, azim=30, label_done=False)


@step_(16)
def st16():
    M = _M()
    insert = part("Window insert", S("panel", "seals", "collars", "hoods", "hood_plates"), COL["panel"])
    unit = part("BreatheBox unit with bracket", S("base", "sides", "end_out", "end_room", "lid", "grilles", "latches", "bplate",
                                                    "struts", "foot", "pad", "cleats"), "#5EAAA8")
    ctx = [part("Wall", CTX["wall"] & _box(-260, 10, -700, 700, 300, 2000), COL["wall"]),
           part("Frame and sashes", CTX["frame"] + CTX["lower_sash"] + CTX["upper_sash"], COL["wall"])]
    return _st(16, [insert], [_mv(unit, (220, 0, 0))], "unit onto the sill",
               "Anti-slip tape under the base; slide it back onto the collars until the foot pad meets the wall",
               context=ctx, elev=18, azim=30, label_done=False)


def steps(which=None):
    out = []
    for n in sorted(STEPS):
        if which and str(n) not in which:
            continue
        out.append(STEPS[n]())
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.2), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 72); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 70, "BreatheBox prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 66.6, "Bought modules wired at block level; no circuit board is laid out. Stranded copper; crimped connectors or ferrules on every terminal.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, "github.com/BoujeeEnjinia1701/breathebox", fontsize=7, color="#0F766E", ha="right", family="monospace")
    B = {}

    def blk(key, x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.4, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.3, sub, ha="center", va="top", fontsize=7.2, color=MUT, linespacing=1.3)
        B[key] = (x, y, w, h)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7.2, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY = "#B91C1C", "#1D4ED8", "#6B7280"
    blk("psu", 3, 44, 16, 13, "24 V adapter", "certified SELV,\n36 W, plugs into\na wall socket", "#111827")
    blk("gl", 24, 46, 11, 9, "Cable gland", "right side wall", "#6B7280")
    blk("fuse", 40, 46, 14, 9, "2 A fuse", "time-delay,\ninline holder", "#B45309")
    blk("buck", 59, 46, 15, 9, "24 to 3.3 V", "buck converter", "#16A34A")
    blk("ctrl", 79, 36, 20, 21, "Controller", "ESP32-C3 class module\nSCD41 class CO2, RH\nand temperature sensor\n(in the intake air)", "#7C3AED")
    blk("fs", 40, 22, 16, 11, "Supply fan", "24 V blower,\nPWM in, tach out", "#0F766E")
    blk("fe", 60, 22, 16, 11, "Exhaust fan", "24 V blower,\nPWM in, tach out", "#C2410C")
    blk("ntc", 82, 18, 16, 11, "Two NTC probes", "core exhaust outlet\nand supply air", "#6B7280")
    blk("st", 103, 38, 14, 13, "Status board", "LED and button\nbehind the\nroom face", "#A855F7")
    wire([(19, 50.5), (24, 50.5)], RED); lab(21.5, 53, "24 V lead", RED, "center")
    wire([(35, 50.5), (40, 50.5)], RED); lab(37.5, 53, "0.5 mm²", RED, "center")
    wire([(54, 50.5), (59, 50.5)], RED); lab(56.5, 53, "0.5 mm²", RED, "center")
    wire([(74, 50.5), (79, 50.5)], RED); lab(76.5, 53, "3.3 V", RED, "center")
    wire([(56.5, 46), (56.5, 38), (48, 38), (48, 33)], RED); wire([(56.5, 38), (68, 38), (68, 33)], RED)
    lab(57.5, 40.5, "24 V to both fans, 0.5 mm²", RED)
    wire([(84, 36), (84, 30), (52, 30), (52, 33)], BLU, 1.3); wire([(86, 36), (86, 31.5), (72, 31.5), (72, 33)], BLU, 1.3)
    lab(60, 28.4, "PWM and tach, 0.25 mm², one pair per fan", BLU)
    wire([(92, 36), (92, 29)], GRY, 1.3); lab(92.8, 33, "0.25 mm²,\ntwisted", GRY)
    wire([(99, 44.5), (103, 44.5)], GRY, 1.3); lab(101, 47, "0.25 mm²", GRY, "center")
    ax.text(2, 12.4, "Routing: the 24 V lead enters through the gland into the supply-outlet chamber. Wires pass between chambers only through grommets",
            fontsize=7.6, color=INK)
    ax.text(2, 9.6, "sealed with silicone: room-side divider (to the supply fan), bulkhead (to the exhaust fan), core frame (to the core exhaust NTC).",
            fontsize=7.6, color=INK)
    ax.text(2, 6.0, "Safety: 24 V SELV only. No mains wiring in the unit; never open the adapter. Unplug the adapter before opening the lid (fans can cut fingers).",
            fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(2, 3.6, "Red: 24 V and 3.3 V power. Blue: fan control. Grey: sensing and status.", fontsize=7.2, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview", "sheets", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "joints": joints, "steps": steps, "wiring": wiring}
    i = 0
    while i < len(args):
        w = args[i]
        nums = []
        while i + 1 < len(args) and args[i + 1].isdigit():
            nums.append(args[i + 1]); i += 1
        r = fns[w](nums) if w in ("sheets", "joints", "steps") else fns[w]()
        print(w, nums or "", "->", r)
        i += 1
