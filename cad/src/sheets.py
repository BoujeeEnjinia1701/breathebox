"""BreatheBox general arrangement drawing BBX-DWG-001 (Rev P3).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/BBX-DWG-001.svg, .pdf and .png from the parametric model.
The concept blueprint sheet (media/concept-blueprint.*) keeps BBX-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawing import Sheet, project_views  # noqa: E402
from model import PARAMS as P, assemblies, build_parts, derived  # noqa: E402

D = derived()
asm = assemblies(build_parts())["breathebox-assembly"]
work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)

s = Sheet(project="BreatheBox", title="General arrangement, window HRV", dwg_no="BBX-DWG-001",
          rev="P3", author="Amish Chadha", date="2026-09-30", concept=True,
          material="Housing 6 mm PVC foam board, battens, foam lining; panel PVC/XPS; hoods PVC; bracket Al. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA for TRL 3 (BBX-CAL-001)", "2026-09-25", "AC"),
                     ("P2", "Night mode note (BBX-DDR-002)", "2026-09-25", "AC"),
                     ("P3", "Constructable design (BBX-DDR-003)", "2026-09-30", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 38, 140, 78, label="Isometric view", sublabel="Not to scale; adapter not shown")
s.add_notes("Key dimensions and interfaces (mm)", [
    f"Housing {P['hx1'] - P['hx0']:.0f} x {P['hw']:.0f} x {P['hh']:.0f}; {-P['hx0']:.0f} on sill, {P['hx1']:.0f} into room",
    f"Front view: outdoors at left; inner wall face at X = 0",
    f"Core {P['core_l']:.0f} x {P['core_w']:.0f} x {P['core_h']:.0f}, plate pitch {P['plate_pitch']}",
    f"Insert panel {P['panel_t']:.0f} thick x {P['panel_h']:.0f} high, trims to 700 to 1000",
    f"Ports {P['port_w']:.0f} x {P['port_h']:.0f} at Y = +/-{P['port_yc']:.0f}",
    f"Hood mouths {P['mouth_w']:.0f} wide, {D['mouth_clear']:.0f} clear; outer edge +/-{P['hood_y_out']:.0f}",
    "Supply filter ePM1 50 % 150 x 170 x 25; exhaust G3 pad",
    "Fans 120 x 120 x 32 blowers, 24 V PWM with tach",
    "Flow 30 to 70 m3/h per stream, 50 nominal, 32 night mode",
    "Core frames, dividers and fan bulkhead seal the four air paths",
    "Tray drain at floor level, 12 x 8 tube through panel",
    "Rails, struts and padded foot prop on the wall; no drilling",
    "Mass about 11.4 kg installed; build plan BBX-BLD-001",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=128, width=140)
s.save(ROOT / "cad/drawings/BBX-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/BBX-DWG-001.svg, .pdf, .png")
