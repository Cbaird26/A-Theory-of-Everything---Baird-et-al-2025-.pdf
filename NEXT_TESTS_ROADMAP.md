# Next Tests Roadmap — High-Value Tightening Steps

This document outlines the clean, minimal, high-value ladder for further testing and constraint tightening. No new weirdness, just scientific tightening.

---

## Current Status

- ✅ QRNG bounds: Real hardware data (LfD/ID Quantique), two-sided 95% CI
- ✅ Fifth-force: Digitized Kapner 2007 exclusion curve
- ✅ Higgs portal: Real ATLAS Run-2 bounds (0.69 MeV invisible width, 0.13 signal deviation)
- ✅ Overlap: Non-empty viable region under stated assumptions

---

## Step 1: Replicate QRNG Bounds with Independent Source

**Goal:** Show the bound is robust across sources (not an API peculiarity).

**Protocol:**
- Run the same preregistered within-run protocol (alternating neutral/coherence)
- Use a different QRNG provider or (best) a local hardware QRNG
- Same analysis pipeline, same outputs, compare posteriors

**Outcome:**
- Likely still null → tighter bound on η / modulation parameters
- If anything deviates → immediate replication before interpretation

**Time:** ~2-3 hours (data collection + analysis)

---

## Step 2: Tighten Higgs Portal Constraints

**Current:** Conservative proxy using ATLAS H→inv bound + μ deviation

**Next step:**
- Plug in explicit published limits relevant to portal parameterization
- Invisible width is one piece; mixing constraints / global coupling fits are another
- Consider CMS H→inv bounds and combine with ATLAS

**Goal:**
- Rerun overlap region check with stronger Higgs constraints
- See if the "island" survives

**Time:** ~1-2 hours (data lookup + JSON update + rerun)

---

## Step 3: Add Second Fifth-Force Constraint Curve (Envelope)

**Current:** Single source (Kapner 2007)

**Next step:**
- Add at least one other authoritative curve (or envelope) spanning neighboring λ ranges
- Options: Adelberger 2009, Eötvös tests, atom interferometry
- Build an exclusion envelope

**Goal:**
- Remove "single-source digitization" fragility
- Rerun overlap with envelope

**Time:** ~1 hour (digitization + envelope script)

---

## Step 4: Global Posterior Overlap (Bayesian Parameter Inference)

**Current:** Deterministic intersection check

**Next upgrade:**
- Treat each channel as a likelihood
- Infer a joint posterior over parameters
- Report credible regions instead of hard cutoffs

**Goal:**
- Fully standard EFT constraint paper approach
- Bayesian credible regions for parameter space

**Time:** ~4-6 hours (likelihood implementation + MCMC or nested sampling)

---

## Step 5: Explore Other Observables (Only After Steps 1-4)

**If η is consistently null in QRNG, the responsible scientific pivot is:**

- Stop treating "bit frequency" as the sole observable
- Consider higher-order correlations or device-noise models **only if preregistered**
- Or shift to other channels where scalar portals typically show up:
  - Precision tests (atomic clocks, equivalence principle)
  - Cosmology (CMB, BAO, supernova)
  - Stellar cooling
  - Neutrino experiments

**Important:** Only after Steps 1-4 are complete and bounds are tightened.

---

## Single-Sentence Summary (for external communication)

> Next tests: replicate the QRNG bounds on an independent QRNG source; tighten Higgs portal constraints using published ATLAS/CMS limits beyond the proxy; add a second fifth-force curve/envelope; then replace hard intersections with a joint Bayesian posterior over parameters.

---

## Priority Order

1. **Step 1** (QRNG replication) - Highest value, validates robustness
2. **Step 2** (Higgs tightening) - Quick win, stronger constraints
3. **Step 3** (Fifth-force envelope) - Removes single-source fragility
4. **Step 4** (Bayesian inference) - Makes it fully standard EFT paper
5. **Step 5** (Other observables) - Only after 1-4 complete

**Total time to complete Steps 1-3:** ~4-6 hours  
**Result:** Tighter, more robust multi-channel constraints

---

## Notes

- All steps use existing pipeline (no new infrastructure needed)
- Each step is independently valuable
- Steps can be done in parallel or sequence
- The goal is tightening, not new physics claims

