# Canonical Statement Template (For Real Curve)

**Purpose:** Template for updating `docs/fifth_force_detectability_summary.md` once real digitized Eöt-Wash curve is processed.

---

## Section to Update: Constraint Curves Used

**Replace the current "Constraint Curves Used" section with:**

```markdown
## Constraint Curves Used

The analysis uses an envelope across multiple constraint curves:

1. **eotwash_prl2016_digitized** (real data) ⭐ **NEW**
   - Source: Eöt-Wash Group / Tan et al. PRL 116, 131102 (2016)
   - Reference: [Full citation here]
   - Range: λ ~ 10⁻⁴ to 10⁻² m (mm-cm scale)
   - Status: **Real experimental constraint data** (digitized from published plot)
   - Provenance: See `results/fifth_force/eotwash_prl2016_digitized_contract_provenance.json`

2. **zenodo5080965_fig3** (real data)
   - Source: Heacock & Huber, DOI: 10.5281/zenodo.5080965
   - Range: λ ~ picometer-nanometer scale
   - Status: Real experimental constraint data

3. **placeholder_eotwash_style** (synthetic)
   - Purpose: Pipeline validation (superseded by real curve)
   - Range: λ ~ 10⁻⁶ to 10⁻³ m

4. **eotwash_style_synthetic_contract** (synthetic)
   - Purpose: Testing envelope logic (superseded by real curve)
   - Range: λ ~ 10⁻⁴ to 10⁻² m

5. **eotwash_tighter_synthetic_contract** (synthetic)
   - Purpose: Stress-testing (superseded by real curve)
   - Range: λ ~ 10⁻⁴ to 10⁻² m

**Status:** Analysis now includes real digitized mm-cm constraint curve. Synthetic curves remain in envelope for completeness but are superseded by real data in the mm-cm regime.
```

---

## Section to Update: Results Statistics

**Update the statistics table with new values from `results/fifth_force/detectability_summary.md`:**

```markdown
### Statistics

Total points computed: [NUMBER]

| Threshold | Count | Fraction | Change from Synthetic |
|-----------|-------|----------|----------------------|
| r > 1.0   |    [X] |  [X.X]%  | [±X.X%]              |
| r > 0.1   |    [X] |  [X.X]%  | [±X.X%]              |
| r > 0.01  |    [X] |  [X.X]%  | [±X.X%]              |
| r > 0.001 |    [X] |  [X.X]%  | [±X.X%]              |
```

**Fill in:**
- Extract values from `results/fifth_force/detectability_summary.md` statistics table
- Compare with previous synthetic results (shown in current document)
- Note whether exclusions increased/decreased

---

## Section to Update: Hunt Band

**Update with new hunt band analysis:**

```markdown
### Hunt Band (mm-cm Regime)

[CHOOSE ONE:]

**Option A - Hunt Band Persists:**
The highest detectability ratios cluster in a narrow band around **λ ≈ [X.X]–[X.X] mm** ([X]×10⁻⁴ to [X]×10⁻³ m), where `r ≈ 0.1–1`. This represents the regime where the scalar's predicted coupling strength approaches but does not exceed experimental upper limits from real Eöt-Wash constraints.

**Top non-excluded points:**
- Highest `r` (non-excluded): [X.XXX] at λ = [X.XXX] mm
- Points with `r > 0.5`: [X] points ([X.X]%)
- Points with `r > 0.1`: [X] points ([X.X]%)

**Conclusion:** The hunt band persists under real experimental constraints, confirming this as a credible target regime for experimental probes.

**Option B - Hunt Band Collapses:**
Under real Eöt-Wash constraints, the previously identified hunt band at λ ≈ 0.3–1.3 mm collapses. Most points now have `r ≪ 1`, indicating the scalar is far below experimental sensitivity in this regime.

**Statistics:**
- Points with `r > 0.1`: [X] points ([X.X]%) (down from 2.2% with synthetic)
- Highest `r` (non-excluded): [X.XXX] at λ = [X.XXX] mm

**Conclusion:** This class of scalar is effectively ruled out at mm-cm scales under existing Eöt-Wash constraints.
```

---

## Section to Add: Canonical Statement

**Add this new section after "Interpretation":**

```markdown
## Canonical Statement

**Scalar fifth force not detected; not ruled out; maximally testable at λ ≈ [X.X]–[X.X] mm under current experimental constraints.**

Under real Eöt-Wash mm-cm constraints, the MQGT-SCF scalar fifth force:
- **Not detected:** No points exceed experimental bounds by significant margins
- **Not ruled out:** [X]% of parameter space remains viable
- **Maximally testable:** Hunt band at λ ≈ [X.X]–[X.X] mm where r ≈ 0.1–1

**Next experimental target:** Precision measurements at λ ≈ [X.X]–[X.X] mm (torsion balance, molecule spectroscopy, or Casimir tests) would decisively test or falsify this scalar class.
```

**OR if hunt band collapses:**

```markdown
## Canonical Statement

**Scalar fifth force ruled out at mm-cm scales under existing experimental constraints.**

Under real Eöt-Wash mm-cm constraints, the MQGT-SCF scalar fifth force is effectively excluded in the mm-cm regime. The previously identified hunt band collapses, with [X]% of points having r < 0.001, indicating the scalar is far below experimental sensitivity at these scales.

**Conclusion:** This scalar class is not viable at mm-cm scales. Future work should focus on other length regimes or alternative detection channels.
```

---

## Section to Update: Limitations

**Update the limitations section:**

```markdown
## Limitations

1. **Real mm-cm curve included:** ✅ Analysis now uses real digitized Eöt-Wash constraint curve. Synthetic curves remain for regression testing but are superseded by real data.

2. **Mapping assumptions:** The mapping from model parameters to `alpha_pred` uses a temporary form (`alpha_pred = alpha_eff²`) with a TODO for physics refinement. Sensitivity to mapping uncertainty should be tested.

3. **Sampling:** Results are based on [NUMBER] points from a log-uniform independent sample. Broader sampling or targeted scans may reveal additional structure.

4. **Envelope logic:** The envelope takes the minimum `alpha_max` at each `lambda_m` across all curves. This is conservative and correctly prioritizes real experimental constraints over synthetic placeholders.
```

---

## Section to Update: Status Header

**Update the header:**

```markdown
**Date:** 2026-01-08  
**Repository:** MQGT-SCF  
**Status:** **Canonical (real experimental constraints)** ⭐
```

---

## Quick Update Checklist

Once `scripts/process_real_eotwash_curve.sh` completes:

- [ ] Extract statistics from `results/fifth_force/detectability_summary.md`
- [ ] Update "Constraint Curves Used" section (add real curve, mark as primary)
- [ ] Update statistics table with new values
- [ ] Update hunt band section (persist or collapse)
- [ ] Add canonical statement section
- [ ] Update limitations section (mark real curve as included)
- [ ] Update status header (change from "Preliminary" to "Canonical")
- [ ] Update related documents (fifth_force_summary.md, README.md)

---

## Example Values (Fill from Results)

After running detectability, extract from `results/fifth_force/detectability_summary.md`:

- Total points: [from statistics table]
- r > 1.0: [count] ([fraction]%)
- r > 0.1: [count] ([fraction]%)
- Top point: r = [value] at λ = [value] m
- Hunt band range: λ ≈ [min]–[max] m

Then fill in template above.

