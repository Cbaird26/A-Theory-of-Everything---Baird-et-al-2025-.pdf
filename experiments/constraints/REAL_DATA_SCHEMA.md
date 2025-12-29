# Real Data Schema for Constraint Modules

This document defines the exact format required to replace placeholder data with real published bounds.

---

## Fifth-Force (Yukawa) Exclusion Data

**File:** `data/fifth_force_exclusion.csv`

**Format:**
```csv
lambda,alpha,excluded
1e-06,1e-12,0
2e-06,1.5e-12,0
5e-06,2e-12,1
...
```

**Columns:**
- `lambda`: Range parameter λ (meters). Log-spaced recommended: 1e-6 to 1e0 m
- `alpha`: Yukawa strength α (dimensionless). Typically 1e-12 to 1e-3
- `excluded`: Boolean (0 = allowed, 1 = excluded)

**Canonical Sources to Digitize:**
1. **Eötvös/EP tests:** Adelberger et al. (2009) "Tests of the gravitational inverse-square law below the dark-energy length scale" - short-range (< 1 mm)
2. **Torsion balance:** Kapner et al. (2007) "Tests of the gravitational inverse-square law" - intermediate range
3. **Lunar laser ranging:** Williams et al. (2004) "Lunar laser ranging tests of the equivalence principle" - long-range

**Recommended:** Start with Adelberger (2009) for short-range, then add Kapner (2007) for intermediate.

**Citation format for `refs.bib` or manual entry:**
```
\bibitem{Adelberger2009} E.~G.~Adelberger \textit{et al.}, ``Tests of the gravitational inverse-square law below the dark-energy length scale,'' \textit{Phys.\ Rev.\ Lett.} \textbf{98}, 131104 (2007).
\bibitem{Kapner2007} D.~J.~Kapner \textit{et al.}, ``Tests of the gravitational inverse-square law below the dark-energy length scale,'' \textit{Phys.\ Rev.\ Lett.} \textbf{98}, 021101 (2007).
```

---

## Higgs Portal Limits

**File:** `data/higgs_limits.json`

**Format:**
```json
{
  "invisible_width_limit_mev": 0.1,
  "signal_strength_deviation": 0.05,
  "mass_range_gev": [1.0, 1000.0],
  "coupling_range": [1e-6, 0.01],
  "source": "ATLAS+CMS combined (2023)",
  "note": "Replace with real combined limits from ATLAS/CMS invisible width + signal strength analyses"
}
```

**Fields:**
- `invisible_width_limit_mev`: Upper bound on invisible Higgs width (MeV)
- `signal_strength_deviation`: Maximum allowed fractional deviation from SM
- `mass_range_gev`: Scalar mass range [min, max] in GeV
- `coupling_range`: Higgs-portal coupling range [min, max]
- `source`: Citation string
- `note`: Notes about data provenance

**Canonical Sources:**
1. **ATLAS:** "Search for invisible Higgs boson decays" (Run 2 + Run 3 combined)
2. **CMS:** "Search for invisible decays of the Higgs boson" (Run 2 + Run 3)
3. **Combined:** ATLAS+CMS combination papers (most authoritative)

**Recommended:** Use ATLAS-CMS combined Run 2 limits (2020-2022) as baseline, then update with Run 3 if available.

**Citation format:**
```
\bibitem{ATLASinvisible} ATLAS Collaboration, ``Search for invisible Higgs boson decays in vector boson fusion at $\sqrt{s}=13$ TeV with the ATLAS detector,'' \textit{Phys.\ Rev.\ D} \textbf{101}, 012002 (2020).
\bibitem{CMSinvisible} CMS Collaboration, ``Search for invisible decays of the Higgs boson produced via vector boson fusion in proton-proton collisions at $\sqrt{s}=13$ TeV,'' \textit{Phys.\ Rev.\ D} \textbf{104}, 032003 (2021).
```

---

## Digitization Workflow

1. **Find the exclusion plot** in the paper (usually Figure 1 or 2)
2. **Use WebPlotDigitizer** (https://apps.automeris.io/wpd/) or similar tool
3. **Extract (λ, α) points** along the exclusion boundary
4. **Mark excluded region:** Points above/beyond the curve are `excluded=1`
5. **Save as CSV** with exact column names: `lambda,alpha,excluded`

For Higgs portal:
1. **Find the limit table or plot** (usually in supplementary material)
2. **Extract numerical limits** for invisible width and signal strength
3. **Note the mass/coupling ranges** where limits apply
4. **Update JSON** with real values and citation

---

## Quick Test After Replacement

```bash
# Regenerate figures
python scripts/fifth_force_yukawa.py --in data/fifth_force_exclusion.csv --out results/fifth_force_bounds.png
python scripts/higgs_portal_bounds.py --config data/higgs_limits.json --out results/higgs_portal_bounds.png
python scripts/make_global_constraints.py

# Verify figures look reasonable (exclusion regions should match published plots)
```

---

## Minimum Viable Real Data

**For immediate credibility, you need:**

1. **Fifth-force:** At least one real exclusion curve (Adelberger 2009 is easiest to digitize)
2. **Higgs portal:** At least one real limit number (ATLAS invisible width from Run 2)

**You do NOT need:**
- Full parameter scans
- Multiple experiments (one authoritative source per channel is enough)
- Real-time updates (static digitized bounds are fine)

**The goal:** Replace "placeholder" with "digitized from [Author et al. Year]" so reviewers see real bounds, not synthetic data.

