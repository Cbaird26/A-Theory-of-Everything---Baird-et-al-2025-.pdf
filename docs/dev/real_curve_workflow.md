# Real Eöt-Wash Curve Workflow: Complete Checklist

**Purpose:** Step-by-step guide for completing the transition from synthetic to real experimental constraints.

---

## Overview

This workflow completes Steps 2-5 of the plan once Step 1 (manual digitization) is done.

**Timeline:** ~30 minutes after digitization complete

---

## Prerequisites

- ✅ Digitized CSV file saved as: `data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv`
- ✅ CSV follows contract format (see `data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv.template`)
- ✅ CSV validated (lambda_m strictly increasing, all values positive)

---

## Step 1: Manual Digitization (Already Done?)

**Status Check:**
```bash
ls -lh data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv
```

**If file doesn't exist:**
1. Follow `docs/dev/eotwash_digitization_guide.md`
2. Use WebPlotDigitizer to digitize Eöt-Wash PRL 2016 curve
3. Save as: `data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv`
4. Verify format matches template

**Expected time:** ~10 minutes

---

## Step 2-5: Automated Processing

**Run the automation script:**
```bash
./scripts/process_real_eotwash_curve.sh
```

**What it does:**
1. ✅ Validates CSV exists
2. ✅ Ingests curve (`make fifth-ingest`)
3. ✅ Reruns detectability (`make fifth-detectability`)
4. ✅ Extracts key statistics
5. ✅ Shows next steps

**Expected time:** ~2 minutes

---

## Step 6: Review Results

**Check the updated detectability summary:**
```bash
cat results/fifth_force/detectability_summary.md
```

**Key things to look for:**
- Statistics table (r > thresholds)
- Top 5-10 points by detectability ratio
- Whether hunt band persists or collapses
- Compare with previous synthetic results

**Expected time:** ~5 minutes

---

## Step 7: Update Canonical Statement

**File to update:** `docs/fifth_force_detectability_summary.md`

**Use template:** `docs/dev/canonical_statement_template.md`

**Key updates:**

1. **Status header:**
   ```markdown
   **Status:** Canonical (real experimental constraints) ⭐
   ```

2. **Constraint curves section:**
   - Add `eotwash_prl2016_digitized` as primary real curve
   - Mark synthetic curves as superseded
   - Include full paper citation

3. **Statistics table:**
   - Update with new values from results
   - Add comparison column (change from synthetic)

4. **Hunt band section:**
   - Update with new λ range (if changed)
   - Choose Option A (persists) or Option B (collapses)
   - Update top points

5. **Add canonical statement:**
   ```markdown
   ## Canonical Statement
   
   Scalar fifth force not detected; not ruled out; maximally testable at λ ≈ [X.X]–[X.X] mm under current experimental constraints.
   ```

6. **Update limitations:**
   - Mark real curve as included ✅
   - Note synthetic curves superseded

**Expected time:** ~15 minutes

---

## Step 8: Update Related Documents

### Update `docs/fifth_force_summary.md`

Add note in detectability section:
```markdown
**Update:** Analysis now includes real digitized Eöt-Wash mm-cm constraint curve.
See `docs/fifth_force_detectability_summary.md` for canonical results.
```

### Update `data/raw/fifth_force/README.md`

Mark digitized curve as complete:
```markdown
#### `eotwash_prl2016_digitized_contract.csv` ✅ **COMPLETE**
- **Source:** Eöt-Wash Group / Tan et al. PRL 116, 131102 (2016)
- **Status:** Digitized and ingested
- **Date:** [DATE]
- **Provenance:** `results/fifth_force/eotwash_prl2016_digitized_contract_provenance.json`
```

### Update `docs/constraint_lab_snapshot.md` (if exists)

Update status:
```markdown
**Fifth-Force Status:** ✅ Real mm-cm curve included
**Detectability Status:** ✅ Canonical results available
```

**Expected time:** ~5 minutes

---

## Step 9: Verify Everything

**Checklist:**

- [ ] Digitized CSV ingested successfully
- [ ] Provenance manifest created
- [ ] Detectability rerun complete
- [ ] Results file updated
- [ ] Canonical statement updated
- [ ] Related documents updated
- [ ] All cross-references working

**Quick verification:**
```bash
# Check ingestion
ls -lh data/processed/eotwash_prl2016_digitized_contract_validated.csv
ls -lh results/fifth_force/eotwash_prl2016_digitized_contract_provenance.json

# Check detectability
grep -A 5 "| Threshold" results/fifth_force/detectability_summary.md

# Check canonical doc
grep "Canonical" docs/fifth_force_detectability_summary.md
```

---

## Expected Outcomes

### Case A: Hunt Band Persists

**What you'll see:**
- Statistics show r > 0.1 points still present (maybe 1-3%)
- Top points cluster around λ ≈ 0.3–1.3 mm
- Hunt band survives real constraints

**Canonical statement:**
> "Scalar fifth force not detected; not ruled out; maximally testable at λ ≈ 0.3–1.3 mm under current experimental constraints."

**Next step:** Propose experimental test (torsion balance, molecule spectroscopy)

### Case B: Hunt Band Collapses

**What you'll see:**
- Statistics show r > 0.1 drops significantly (maybe <0.5%)
- Most points have r < 0.001
- Hunt band disappears

**Canonical statement:**
> "Scalar fifth force ruled out at mm-cm scales under existing experimental constraints."

**Next step:** Pivot to other channels or accept falsification

**Either outcome is valuable** - clean, empirical, world-facing physics.

---

## Troubleshooting

### "CSV not found"
- Check file path: `data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv`
- Verify filename matches exactly (case-sensitive)

### "Ingestion fails validation"
- Check CSV format matches template
- Verify `lambda_m` strictly increasing
- Verify all values positive
- Check for extra headers/formatting

### "Detectability shows no change"
- Check envelope includes new curve: `grep eotwash_prl2016 results/fifth_force/detectability_summary.md`
- Verify curve is in mm-cm range (overlaps with sampled points)
- Check if curve is tighter/looser than synthetic

### "Canonical statement unclear"
- Review template: `docs/dev/canonical_statement_template.md`
- Check if hunt band persists or collapses
- Use appropriate option (A or B) from template

---

## Quick Reference

**Files created/updated:**
- `scripts/process_real_eotwash_curve.sh` - Automation script
- `docs/dev/canonical_statement_template.md` - Update template
- `docs/dev/real_curve_workflow.md` - This checklist

**Key commands:**
```bash
# Run automation
./scripts/process_real_eotwash_curve.sh

# Manual steps (if needed)
make fifth-ingest INPUT=data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv
make fifth-detectability SEED=42 NPTS=2000

# View results
cat results/fifth_force/detectability_summary.md
```

**Key documents:**
- `docs/fifth_force_detectability_summary.md` - Update this
- `docs/dev/eotwash_digitization_guide.md` - Digitization instructions
- `docs/dev/canonical_statement_template.md` - Update template

---

## Success!

Once complete, you'll have:
- ✅ Real experimental constraint curve ingested
- ✅ Updated detectability analysis with real bounds
- ✅ Canonical "Scalar Hunt Result" statement
- ✅ All documents cross-referenced and updated

**This is the moment the hunt stops being hypothetical.**

---

**Created:** 2026-01-08  
**Purpose:** Complete workflow for transitioning to real experimental constraints

