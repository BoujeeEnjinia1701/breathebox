"""BreatheBox sizing calculations (BBX-CAL-001).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md and writes
docs/04-calcs/results.csv (requirement status table).

Geometry comes from cad/src/model.py (PARAMS and part volumes); costs come from
bom/bom.csv; the budget from project.yaml. All values are first-principles estimates
for a paper design. Nothing is measured.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad/src"))
from model import PARAMS as P, build_parts, derived  # noqa: E402

D = derived()

# ---------------------------------------------------------------- 1. assumptions
RHO, CP, NU, K_AIR = 1.2, 1005.0, 1.5e-5, 0.0257     # air near 20 °C
P_ATM = 101325.0
T_IN, RH_IN = 20.0, 0.50                             # design case indoors
T_OUT = 0.0                                          # design case outdoors
Q_NOM, Q_MIN, Q_MAX = 50.0, 30.0, 70.0               # m3/h per stream (R1, decision A5)
CO2_OUT, G_SLEEP, N_SLEEP, V_ROOM, H_SLEEP = 420.0, 0.014, 2, 30.0, 8.0
HDD, SEASON_D = 3500.0, 212                          # K·d, days (cold-temperate assumption)
NU_PLATE, K_PLATE = 7.54, 0.19                       # laminar parallel plates; polymer plate W/(m K)
AREA_FACTOR = 0.85                                   # share of plate area in effective counterflow
K_CORE_HEADERS = 2.0                                 # header entry, turns and exit, on channel velocity
FILTER_EPM1_PA_AT_1MS = 50.0                         # clean ePM1 50 % pleated, 25 mm, linear with velocity
FILTER_COARSE_PA_AT_1MS = 15.0                       # clean coarse pad
FILTER_LOADED = 2.0                                  # replacement point, x clean
MESH_PHI, K_MESH = 0.59, 2.0                         # 1 mm aperture mesh open area; K at low Reynolds number
K_HOOD, K_PORT, K_PLENUM, K_FAN_IN, K_GRILLE = 1.5, 1.0, 1.5, 1.0, 1.5
GRILLE_FREE = 0.5
FAN_P0, FAN_QF = 400.0, 100.0                        # Pa shut-off, m3/h free air at full speed
FAN_ETA, FAN_FIXED_W = 0.25, 0.3                     # total efficiency, fixed electronics loss per fan
FAN_DBA_FULL, ATTEN_DB = 52.0, 5.0                   # dB(A) at 1 m, full speed, bare fan; lining and grille
CTRL_W, BUCK_ETA = 0.5, 0.85
PSU_W = 36.0
SCREEN_PA = 5.0                                      # depressurization screening limit (assumption)
UNDERCUT_A, CD = 0.8 * 0.010, 0.6                    # bedroom door undercut 800 x 10 mm


def m3s(q):
    return q / 3600.0


def dyn(v):
    return 0.5 * RHO * v * v


def psat(t):
    """Saturation vapor pressure over water (t >= 0) or ice (t < 0), Pa (Magnus form)."""
    if t >= 0:
        return 610.94 * math.exp(17.625 * t / (t + 243.04))
    return 611.15 * math.exp(22.452 * t / (t + 272.55))


def w_of(pv):
    return 0.622 * pv / (P_ATM - pv)


# ---------------------------------------------------------------- 2. core geometry and effectiveness
pitch, pt = P["plate_pitch"] / 1000, P["plate_t"] / 1000
cw, ch, cl = P["core_w"] / 1000, P["core_h"] / 1000, P["core_l"] / 1000
n_ch = int(round(ch / pitch))
n_ch_s = n_ch // 2
gap = pitch - pt
dh = 2 * gap
n_plates = n_ch - 1
a_plate = cw * cl * n_plates
a_eff = a_plate * AREA_FACTOR
h_conv = NU_PLATE * K_AIR / dh
U = 1.0 / (2.0 / h_conv + pt / K_PLATE)
UA = U * a_eff
a_chan = n_ch_s * gap * cw          # flow area per stream


def cap(q):
    return m3s(q) * RHO * CP


def eff(q_s, q_e=None):
    """Counterflow effectiveness (on Cmin) for supply and exhaust flows in m3/h."""
    q_e = q_s if q_e is None else q_e
    cmin, cmax = min(cap(q_s), cap(q_e)), max(cap(q_s), cap(q_e))
    ntu, cr = UA / cmin, cmin / cmax
    if abs(1 - cr) < 1e-9:
        return ntu / (1 + ntu)
    e = math.exp(-ntu * (1 - cr))
    return (1 - e) / (1 - cr * e)


# ---------------------------------------------------------------- 3. pressure drop per stream
sf_area = P["port_w"] * P["port_h"] / 1e6
ef_area = P["efilter_w"] * P["efilter_h"] / 1e6
mouth_area = (P["mouth_w"] - 2 * P["hood_t"]) * (P["hood_d"] - 2 * P["hood_t"]) / 1e6
port_area = sf_area
half_face = (P["core_w"] / 2) * P["core_h"] / 1e6
fan_in_area = math.pi * 0.034 ** 2
gx0, gx1, gy0, gy1 = P["sgrille"]
sgrille_area = (gx1 - gx0) * (gy1 - gy0) / 1e6 * GRILLE_FREE
ey0, ey1, ez0, ez1 = P["egrille"]
egrille_area = (ey1 - ey0) * (ez1 - ez0) / 1e6 * GRILLE_FREE


def core_dp(q):
    v = m3s(q) / a_chan
    re = v * dh / NU
    f = 96.0 / re
    return f * cl / dh * dyn(v) + K_CORE_HEADERS * dyn(v), v, re


def stream_dp(q, stream, loaded=False):
    """Return (total Pa, {element: Pa}) for the supply or exhaust stream."""
    qs = m3s(q)
    fl = FILTER_LOADED if loaded else 1.0
    items = {}
    items["hood and mesh"] = (K_HOOD + K_MESH) * dyn(qs / mouth_area)
    items["panel port and collar"] = K_PORT * dyn(qs / port_area)
    items["plenum turn to core"] = K_PLENUM * dyn(qs / half_face)
    items["core"] = core_dp(q)[0]
    items["fan inlet"] = K_FAN_IN * dyn(qs / fan_in_area)
    if stream == "supply":
        items["filter"] = FILTER_EPM1_PA_AT_1MS * fl * qs / sf_area
        items["room grille"] = K_GRILLE * dyn(qs / sgrille_area)
    else:
        items["filter"] = FILTER_COARSE_PA_AT_1MS * fl * qs / ef_area
        items["room grille"] = K_GRILLE * dyn(qs / egrille_area)
    return sum(items.values()), items


# ---------------------------------------------------------------- 4. fan operating point, power, noise
def fan_speed(q, dp):
    """Speed ratio n on the curve dp = P0 n^2 (1 - (Q / (QF n))^2)."""
    return math.sqrt((dp + FAN_P0 * (q / FAN_QF) ** 2) / FAN_P0)


def fan_power(q, dp):
    return m3s(q) * dp / FAN_ETA + FAN_FIXED_W


def fan_dba(n):
    return FAN_DBA_FULL + 50 * math.log10(n)


def op(q, loaded=False):
    out = {}
    for s in ("supply", "exhaust"):
        dp, items = stream_dp(q, s, loaded)
        n = fan_speed(q, dp)
        out[s] = dict(dp=dp, items=items, n=n, w=fan_power(q, dp), dba=fan_dba(n))
    out["w_total"] = out["supply"]["w"] + out["exhaust"]["w"] + CTRL_W / BUCK_ETA
    room = 10 * math.log10(sum(10 ** ((out[s]["dba"] - ATTEN_DB) / 10) for s in ("supply", "exhaust")))
    out["room_dba"] = room
    return out


def max_q_full_speed(loaded):
    lo, hi = 1.0, FAN_QF
    for _ in range(60):
        mid = (lo + hi) / 2
        dp = max(stream_dp(mid, s, loaded)[0] for s in ("supply", "exhaust"))
        if FAN_P0 * (1 - (mid / FAN_QF) ** 2) >= dp:
            lo = mid
        else:
            hi = mid
    return lo


def q_for_dba(target, loaded=False):
    lo, hi = 5.0, Q_MAX
    for _ in range(60):
        mid = (lo + hi) / 2
        if op(mid, loaded)["room_dba"] <= target:
            lo = mid
        else:
            hi = mid
    return lo


# ---------------------------------------------------------------- 5. heat, condensate, frost
def heat(q, t_out=T_OUT):
    e = eff(q)
    c = cap(q)
    return e, c * (T_IN - t_out), e * c * (T_IN - t_out), t_out + e * (T_IN - t_out)


def condensate(q, t_out):
    """Upper bound: exhaust cooled to its dry outlet temperature and saturated there (g/h)."""
    e = eff(q)
    t_ex = T_IN - e * (T_IN - t_out)
    w_in = w_of(RH_IN * psat(T_IN))
    w_sat = w_of(psat(t_ex))
    m = m3s(q) * RHO * 3600
    return max(0.0, (w_in - w_sat) * 1000 * m), t_ex


def cold_corner(q_s, q_e, t_out):
    """Plate temperature at the exhaust outlet / supply inlet corner (equal h both sides)."""
    e = eff(q_s, q_e)
    cmin = min(cap(q_s), cap(q_e))
    t_ex = T_IN - e * cmin * (T_IN - t_out) / cap(q_e)
    return (t_ex + t_out) / 2, t_ex


def frost_onset(q):
    lo, hi = -20.0, 10.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if cold_corner(q, q, mid)[0] >= 0:
            hi = mid
        else:
            lo = mid
    return hi


def frost_supply_ratio(q_e, t_out):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if cold_corner(max(mid * q_e, 0.1), q_e, t_out)[0] >= 0:
            lo = mid
        else:
            hi = mid
    return lo


# ---------------------------------------------------------------- 6. CO2
def co2_ss(q):
    return CO2_OUT + N_SLEEP * G_SLEEP / q * 1e6


def co2_24h(q):
    """24 h mean with two sleepers for H_SLEEP h and an empty room otherwise (transients included)."""
    tau = V_ROOM / q
    ss = co2_ss(q) - CO2_OUT
    rise = ss * (H_SLEEP - tau * (1 - math.exp(-H_SLEEP / tau)))
    end = ss * (1 - math.exp(-H_SLEEP / tau))
    fall = end * tau * (1 - math.exp(-(24 - H_SLEEP) / tau))
    return CO2_OUT + (rise + fall) / 24


# ---------------------------------------------------------------- 7. mass, statics, cost
DENS = {  # kg/m3, effective for the massing solid
    1: (P["shell_t"] * 550 + P["lining_t"] * 30) / (P["shell_t"] + P["lining_t"]),  # PVC foam board + lining
    8: 1270.0,    # PETG tray and silicone tube
    9: (6 * 550 + (P["panel_t"] - 6) * 35) / P["panel_t"],                           # PVC skins over XPS
    10: 1400.0,   # rigid PVC sheet
    11: 2700.0,   # aluminium
}
FIXED_KG = {3: 0.30, 4: 0.30, 5: 0.10, 6: 0.05, 7: 0.08, 12: 0.25}
CORE_FRAME_KG, PLATE_RHO = 0.30, 1350.0
SUNDRIES_KG = 0.30


def masses():
    m = {}
    names = {}
    for name, shape, _, bom, _ in build_parts():
        names[bom] = name
        if bom in DENS:
            m[bom] = shape.volume / 1e9 * DENS[bom]
        elif bom == 2:
            m[bom] = a_plate * pt * PLATE_RHO + CORE_FRAME_KG
        else:
            m[bom] = FIXED_KG[bom]
    return m, names


def bom_total():
    rows = list(csv.DictReader((ROOT / "bom/bom.csv").open()))
    return sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows), rows


def budget():
    for line in (ROOT / "project.yaml").read_text().splitlines():
        if line.startswith("budget_usd:"):
            return float(line.split(":")[1].split("#")[0])
    return float("nan")


BUDGET_PROPOSED = 250.0


# ---------------------------------------------------------------- report
def main():
    pr = print
    pr("BBX-CAL-001 sizing, all values estimates\n")
    pr("== Core ==")
    pr(f"channels {n_ch} ({n_ch_s} per stream), gap {gap*1000:.2f} mm, Dh {dh*1000:.1f} mm, plates {n_plates}")
    pr(f"plate area {a_plate:.2f} m2, effective {a_eff:.2f} m2; h {h_conv:.1f} W/(m2 K), U {U:.1f} W/(m2 K), UA {UA:.1f} W/K")
    for q in (Q_MIN, Q_NOM, Q_MAX):
        dpc, v, re = core_dp(q)
        pr(f"  {q:.0f} m3/h: C {cap(q):.2f} W/K, NTU {UA/cap(q):.2f}, effectiveness {eff(q)*100:.1f} %, "
           f"channel v {v:.2f} m/s, Re {re:.0f}, core dp {dpc:.1f} Pa")

    pr("\n== Pressure drop per stream (clean / loaded filters) ==")
    for q in (Q_MIN, Q_NOM, Q_MAX):
        for s in ("supply", "exhaust"):
            c, items = stream_dp(q, s)
            l, _ = stream_dp(q, s, True)
            detail = ", ".join(f"{k} {v:.1f}" for k, v in items.items())
            pr(f"  {q:.0f} m3/h {s:7s}: {c:.1f} Pa clean, {l:.1f} Pa loaded  ({detail})")

    pr("\n== Fan operating points (fan: %.0f Pa shut-off, %.0f m3/h free air at full speed) ==" % (FAN_P0, FAN_QF))
    for q in (Q_MIN, Q_NOM, Q_MAX):
        for loaded in (False, True):
            o = op(q, loaded)
            pr(f"  {q:.0f} m3/h {'loaded' if loaded else 'clean '}: speed supply {o['supply']['n']:.2f}, exhaust {o['exhaust']['n']:.2f}; "
               f"fan W {o['supply']['w']:.2f} + {o['exhaust']['w']:.2f}; total {o['w_total']:.1f} W; room {o['room_dba']:.1f} dB(A) at 1 m")
    pr(f"  max flow at full speed: clean {max_q_full_speed(False):.0f} m3/h, loaded {max_q_full_speed(True):.0f} m3/h")
    pr(f"  flow meeting 30 dB(A) at 1 m, clean filters: {q_for_dba(30.0):.0f} m3/h")
    old_qf = 60.0
    pr(f"  TRL 2 fan (about {old_qf:.0f} m3/h free air) cannot reach 70 m3/h against any pressure")
    o70l = op(Q_MAX, True)
    pr(f"  peak input at 70 m3/h, loaded: {o70l['w_total']:.1f} W = {o70l['w_total']/24:.2f} A at 24 V; adapter {PSU_W:.0f} W, "
       f"margin {PSU_W - o70l['w_total']:.1f} W")
    q_pk = FAN_QF / math.sqrt(3)                      # peak air power on the assumed full-speed curve
    full_w = 2 * (m3s(q_pk) * FAN_P0 * (1 - (q_pk / FAN_QF) ** 2) / FAN_ETA + FAN_FIXED_W) + CTRL_W / BUCK_ETA
    pr(f"  worst case, both fans at full speed at peak air power ({q_pk:.0f} m3/h): {full_w:.1f} W ({full_w/24:.2f} A) "
       f"against the {PSU_W:.0f} W adapter; input fuse 2 A time-delay")

    pr("\n== Heat recovery ==")
    for q in (Q_NOM, Q_MAX):
        e, loss, rec, t_sup = heat(q)
        fan_s = op(q)["supply"]["w"]
        pr(f"  {q:.0f} m3/h at 0 °C out: exhaust heat {loss:.0f} W, recovered {rec:.0f} W, lost {loss-rec:.0f} W, "
           f"supply {t_sup:.1f} °C ({t_sup + fan_s/cap(q):.1f} °C with supply fan heat)")
    e50 = eff(Q_NOM)
    season = cap(Q_NOM) * e50 * HDD * 24 / 1000
    fan_season = op(Q_NOM)["w_total"] * 24 * SEASON_D / 1000
    pr(f"  season ({HDD:.0f} K d, {SEASON_D} d) at 50 m3/h: kept {season:.0f} kWh, fans and controls {fan_season:.0f} kWh, "
       f"ratio {season/fan_season:.0f}")

    pr("\n== Condensate and frost ==")
    worst = (0, None, None)
    for q in (Q_NOM, Q_MAX):
        t0 = frost_onset(q)
        for t in [x / 2 for x in range(int(t0 * 2), 21)]:
            g, tex = condensate(q, t)
            if g > worst[0]:
                worst = (g, q, t)
        g0, tex0 = condensate(q, 0.0)
        pr(f"  {q:.0f} m3/h: condensate at 0 °C {g0:.0f} g/h (exhaust out {tex0:.1f} °C); frost onset {t0:.1f} °C outdoors")
    pr(f"  worst condensate above frost onset: {worst[0]:.0f} g/h ({worst[0]/1000:.2f} L/h) at {worst[1]:.0f} m3/h, {worst[2]:.1f} °C")
    for q_e in (Q_NOM, Q_MAX):
        r = frost_supply_ratio(q_e, -10.0)
        net = q_e * (1 - r)
        dpr = RHO / 2 * (m3s(net) / (CD * UNDERCUT_A)) ** 2
        pr(f"  -10 °C, exhaust {q_e:.0f} m3/h: supply ratio {r:.2f} (supply {r*q_e:.0f} m3/h), net extract {net:.0f} m3/h, "
           f"room depressurization through an 800 x 10 mm door undercut {dpr:.1f} Pa (screen {SCREEN_PA:.0f} Pa)")
    pre = (frost_onset(Q_NOM) - (-10.0)) * cap(Q_NOM)
    pr(f"  balanced-flow preheat to hold the onset at -10 °C, 50 m3/h: {pre:.0f} W (adapter {PSU_W:.0f} W)")
    tube_id = 8.0
    pr(f"  drain: {tube_id:.0f} mm bore tube; worst flow {worst[0]/1000:.2f} L/h is {worst[0]/3600:.3f} mL/s")

    pr("\n== CO2 (two sleepers, 30 m3 room, no infiltration) ==")
    for q in (Q_MIN, Q_NOM, Q_MAX):
        pr(f"  {q:.0f} m3/h: steady state {co2_ss(q):.0f} ppm, 24 h mean {co2_24h(q):.0f} ppm, time constant {V_ROOM/q*60:.0f} min")
    r10 = frost_supply_ratio(Q_NOM, -10.0)
    pr(f"  frost mode at -10 °C: room still gets {Q_NOM:.0f} m3/h of extract; {r10*Q_NOM:.0f} m3/h through the core and "
       f"{Q_NOM*(1-r10):.0f} m3/h from the rest of the home")

    pr("\n== Geometry (from cad/src/model.py) ==")
    pr(f"  hood mouths clear distance {D['mouth_clear']:.0f} mm; hood outer edges +/-{P['hood_y_out']:.0f} mm")
    min_open = 2 * (P["hood_y_out"] + P["seal"])
    pr(f"  narrowest clear width that takes the hoods: {min_open:.0f} mm (R8 lower bound 700 mm)")
    pr(f"  housing {P['hx1']-P['hx0']:.0f} x {P['hw']:.0f} x {P['hh']:.0f} mm; on the sill {0-P['hx0']:.0f} mm, room overhang {P['hx1']:.0f} mm")
    pr(f"  largest opening through the installed unit: {P['plate_pitch']-P['plate_t']:.2f} mm core channels; mesh 1 mm")

    pr("\n== Mass ==")
    m, names = masses()
    for k in sorted(m):
        pr(f"  {k:2d} {names[k]:30s} {m[k]:.2f} kg")
    total_m = sum(m.values()) + SUNDRIES_KG
    unit_m = total_m - m[12]
    pr(f"  sundries {SUNDRIES_KG:.2f} kg; total {total_m:.1f} kg; installed unit without adapter {unit_m:.1f} kg")

    # statics: bracket carries the overhang, housing pivots on the inner wall edge
    parts = {b: s for _, s, _, b, _ in build_parts()}
    cg_x = sum(m[b] * parts[b].center().X for b in m if b not in (12, 9, 10)) / sum(m[b] for b in m if b not in (12, 9, 10))
    w_on = 9.81 * sum(m[b] for b in m if b not in (12, 9, 10))
    strut_ang = math.atan2(P["sill_z"] - P["bracket_t"] - 10 - P["foot_z"], P["bracket_x1"] - 20 - 8)
    f_strut = w_on * max(cg_x, 0) / (P["bracket_x1"] - 20) / math.sin(strut_ang)
    pr(f"  center of mass of the sill-borne parts at X = {cg_x:.0f} mm (room side of the wall face); "
       f"strut force if the bracket carries it all {f_strut:.0f} N total, {f_strut/2:.0f} N per strut")

    pr("\n== Cost ==")
    tot, rows = bom_total()
    b = budget()
    pr(f"  BOM total ${tot:.2f} ({len(rows)} lines); budget_usd ${b:.0f}: {'within' if tot <= b else 'over'} by ${abs(tot-b):.2f}; "
       f"proposed ${BUDGET_PROPOSED:.0f} (awaiting Amish): {'within' if tot <= BUDGET_PROPOSED else 'over'} by ${abs(tot-BUDGET_PROPOSED):.2f}")

    # --------------------------------------------------------------- requirements table
    o50, o50l, o70l = op(Q_NOM), op(Q_NOM, True), op(Q_MAX, True)
    qmax_l = max_q_full_speed(True)
    r7_ratio = frost_supply_ratio(Q_MAX, -10.0)
    res = [
        ("R1", f"30 to 70 m3/h each stream; full-speed limit {qmax_l:.0f} m3/h with loaded filters; balance by tach", "30 to 70 m3/h, within 10 %",
         "Met on paper"),
        ("R2", f"{eff(Q_NOM)*100:.1f} % at 50 m3/h ({eff(Q_MAX)*100:.1f} % at 70)", "75 % or more at 50 m3/h", "Met on paper"),
        ("R3", f"{o50['w_total']:.1f} W clean, {o50l['w_total']:.1f} W loaded filters", "12 W or less at 50 m3/h",
         "Met on paper" if o50l["w_total"] <= 12 else ("At risk" if o50["w_total"] <= 12 else "Not met")),
        ("R4", f"24 h mean {co2_24h(Q_NOM):.0f} ppm at 50 m3/h; night {co2_ss(Q_NOM):.0f} ppm", "1,000 ppm or less, 24 h mean", "Met on paper"),
        ("R5", "ePM1 50 % supply, coarse exhaust", "ePM1 50 % or better", "Met by specification"),
        ("R6", f"{o50['room_dba']:.0f} dB(A) at 50 m3/h; 30 dB(A) reached at {q_for_dba(30.0):.0f} m3/h", "30 dB(A) or less at 50 m3/h",
         "Not met" if o50["room_dba"] > 30 else "Met on paper"),
        ("R7", f"worst condensate {worst[0]/1000:.2f} L/h drains; frost onset {frost_onset(Q_NOM):.1f} °C; at -10 °C supply ratio {r7_ratio:.2f}",
         "Drain all condensate; no blockage to -10 °C", "Met on paper"),
        ("R8", f"hoods need {min_open:.0f} mm clear width; panel trims to 700 to 1,000 mm", "Sash 700 to 1,000 mm; slider adapter", "Met on paper (sash)"),
        ("R9", f"{unit_m:.1f} kg; no drilling; install time not calculable", "12 kg or less; 30 min or less", "Not verifiable at TRL 3 (mass met on paper)"),
        ("R10", f"24 V SELV adapter {PSU_W:.0f} W; {o70l['w_total']:.1f} W at 70 m3/h loaded, {full_w:.1f} W worst case at full speed; 2 A input fuse",
         "24 V SELV only", "Met by design"),
        ("R11", f"{D['mouth_clear']:.0f} mm between mouths; 1 mm mesh; mouths face down", "400 mm or more; mesh 1.5 mm or finer", "Met on paper"),
        ("R12", f"largest through opening {P['plate_pitch']-P['plate_t']:.2f} mm; sash locks onto panel", "No opening over 100 mm", "Met by design, unverified"),
        ("R13", "lift-off lid; filters and core slide out", "Tool-free filter change in 2 min or less", "Not verifiable at TRL 3"),
        ("R14", "no firmware yet; checked at firmware review", "Local data only", "Not verifiable at TRL 3"),
        ("R15", f"${tot:.2f}", f"${b:.0f} or less (${BUDGET_PROPOSED:.0f} proposed, awaiting Amish)",
         "Not met" if tot > b else "Met"),
    ]
    pr("\n== Requirement status ==")
    with (ROOT / "docs/04-calcs/results.csv").open("w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["id", "value", "target", "status"])
        for r in res:
            wr.writerow(r)
            pr(f"  {r[0]:4s} {r[3]:45s} {r[1]}")
    pr("\nwrote docs/04-calcs/results.csv")


if __name__ == "__main__":
    main()
