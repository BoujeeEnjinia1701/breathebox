# BOM notes

- Prices are indicative USD for single prototype quantities in September 2026. Every line is priced, with a supplier or supplier type; no price has been confirmed with a named supplier. They are estimates for TRL 3 review.
- Rows 1 to 12 match the numbered callouts in `media/exploded.png` and the parts in `cad/src/model.py`. Row 13 (seals, fasteners, wiring and the input fuse) is not drawn.
- Total parts cost is **$255.00** (BBX-CAL-001 section 9, computed by `docs/04-calcs/sizing.py`). That is $35 over the $220 budget in `project.yaml` and $5 over the $250 recommended at TRL 2, which is awaiting Amish (BBX-DDR-001 item A1). R15 is not met.
- Changes from TRL 2 ($243): larger blowers in rows 3 and 4 (+$8, because the TRL 2 fans could not reach 70 m³/h), collars through the panel in row 10 (+$2), and a 2 A fuse and holder in row 13 (+$2).
- The counterflow core (row 2) is the largest single cost and sets the heat recovery figure. A home-made crossflow core from corrugated plastic sheet would cost about $10 but recover only about 50 to 65 % (estimate).
- The unit runs from a certified 24 V plug-in adapter. There is no mains wiring inside the unit.
