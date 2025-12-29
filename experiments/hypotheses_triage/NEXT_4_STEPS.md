# Next 4 Steps — Highest Leverage Actions

Based on the 500-hypothesis triage, these are the immediate moves that convert "beautiful theory" into "physics object with a parameter map."

---

## Step 1: Replace Fifth-Force Placeholder with Real Curve

**Status:** Scaffolded (code exists, needs real data)

**Action:**
1. Pick one canonical source (Adelberger 2009 or Kapner 2007)
2. Digitize the exclusion curve using WebPlotDigitizer
3. Format as CSV: `lambda,alpha,excluded`
4. Replace: `experiments/constraints/data/fifth_force_exclusion.csv`
5. Regenerate: `python experiments/constraints/scripts/fifth_force_yukawa.py`
6. Verify citation matches the exact source

**Time:** ~30 minutes (digitization)

**Output:** Real exclusion bounds in the paper

---

## Step 2: Replace Higgs Portal Placeholder with Real Bounds

**Status:** Scaffolded (code exists, needs real data)

**Action:**
1. Find ATLAS-CMS combined Run 2 invisible width limit
2. Extract numerical bounds (invisible width, signal strength deviation)
3. Update: `experiments/constraints/data/higgs_limits.json`
4. Regenerate: `python experiments/constraints/scripts/higgs_portal_bounds.py`
5. Verify citation matches source

**Time:** ~20 minutes (data lookup + JSON update)

**Output:** Real collider bounds in the paper

---

## Step 3: Run Global Overlap Region Check

**Status:** Open (needs implementation)

**Action:**
1. Create script: `experiments/constraints/scripts/check_overlap_region.py`
2. Load QRNG bounds (epsilon < 0.003086)
3. Load fifth-force bounds (excluded region)
4. Load Higgs portal bounds (excluded region)
5. Compute intersection: viable parameter space
6. Plot: allowed region in (m_M, g_M) or (m_Phi, g_PhiH) space
7. Report: "Viable region exists" or "All parameter space excluded"

**Time:** ~1 hour (script + analysis)

**Output:** Parameter space map showing where the model can still live

---

## Step 4: Add Cosmology Likelihoods (Minimal)

**Status:** Open (needs implementation)

**Action:**
1. Pick one dataset (CMB, BAO, or supernova)
2. Create minimal likelihood module: `experiments/constraints/scripts/cosmology_likelihood.py`
3. Map scalar field parameters → cosmological observables
4. Compute likelihood for one dataset
5. Add to global constraints figure

**Time:** ~2-3 hours (depends on dataset complexity)

**Output:** One additional constraint channel

**Note:** Only do this after steps 1-3 are complete.

---

## Priority Order

1. **Step 1** (fifth-force) - Highest leverage, already scaffolded
2. **Step 2** (Higgs portal) - Second highest, already scaffolded
3. **Step 3** (overlap check) - Critical for showing viable space
4. **Step 4** (cosmology) - Expansion after core is solid

**Total time to complete steps 1-3:** ~2 hours

**Result:** Complete multi-channel constraint map with real bounds and viable parameter space analysis.

