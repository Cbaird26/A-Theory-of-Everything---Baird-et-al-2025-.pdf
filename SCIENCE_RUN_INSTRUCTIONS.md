# Science Run: Prove/Kill the Scalar

**Purpose:** Run the "verdict" analysis to determine if the scalar is ruled out, alive-but-undetectable, or in a hunt band

---

## Quick Science Run

### Step 1: Place Canonical Curve

```bash
# Use monotone conservative version (most conservative bounds)
cp /path/to/eotwash_prl2016_digitized_contract_monotone_conservative_2026-01-21_155709_UTC.csv \
   data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv
```

**Or if already placed:**
```bash
# Verify canonical file exists
ls -lh data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv
```

### Step 2: Ingest and Create Provenance

```bash
make fifth-ingest INPUT=data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv
```

**What this does:**
- Validates CSV format
- Creates provenance JSON
- Registers curve in the system

### Step 3: Run Verdict Analysis (Big-N Real-Only Scan)

```bash
make fifth-detectability SEED=42 NPTS=10000 REAL_ONLY=1 ALPHA_MODE=A TARGET_FRAC=0.7
```

**Parameters:**
- `SEED=42` - Fixed seed for reproducibility
- `NPTS=10000` - Large sample size for robust statistics
- `REAL_ONLY=1` - Exclude synthetic curves, use only real experimental data
- `ALPHA_MODE=A` - Use placeholder mapping (α_pred = α_eff²)
- `TARGET_FRAC=0.7` - Focus 70% of samples in real curve lambda range

**What this does:**
- Samples model points from parameter space
- Computes detectability ratio: `r = alpha_pred / alpha_max`
- Categorizes points:
  - `r > 1`: Excluded (ruled out)
  - `r ≈ 0.1-1`: Hunt band (near detection)
  - `r << 1`: Far from detection (alive but undetectable)

### Step 4: Check Results

```bash
# View summary
cat results/fifth_force/detectability_summary.md

# Or open in editor
open results/fifth_force/detectability_summary.md
```

**What to look for:**
- **Excluded fraction:** Percentage of parameter space ruled out
- **Hunt band fraction:** Percentage near detection threshold
- **Coverage report:** Fraction of sampled space covered by real experimental data
- **Representative points:** Example points in each category

---

## Expected Results (Based on Previous Runs)

With the digitized Eöt-Wash curve and current placeholder mapping:

- **Not detected** (no confirmed signal)
- **Not broadly ruled out** (most of parameter space survives)
- **Small excluded fraction** (~1.3% of sampled points)
- **Small hunt band** (~1.8% near detection threshold)
- **Most parameter space** far below detectability

**Interpretation:**
- This is **not** "scalar proven"
- This is "scalar not killed yet under these assumptions"
- Provides a **target band** for future experiments/constraints

---

## Understanding the Output

### Detectability Summary Structure

The `detectability_summary.md` includes:

1. **Run Metadata:**
   - Seed, number of points, real-only mode status
   - Alpha mapping mode and parameters
   - Git commit hash

2. **Statistics:**
   - Total points sampled
   - Excluded count and percentage
   - Near-detectable (hunt band) count and percentage
   - Far-from-detection count and percentage

3. **Coverage Report (if REAL_ONLY=1):**
   - Fraction of sampled points within real experimental lambda ranges
   - Lambda range coverage from real curves

4. **Representative Points:**
   - Example points in each category
   - Shows where in parameter space each outcome occurs

5. **Notes:**
   - Which curves were used (real vs synthetic)
   - Mapping assumptions
   - Limitations and caveats

---

## Alternative Runs

### Quick Test Run (Faster)

```bash
make fifth-detectability SEED=42 NPTS=1000 REAL_ONLY=1 ALPHA_MODE=A
```

### Mapping Sensitivity Sweep

Test different alpha mapping modes:

```bash
# Mode A (placeholder)
make fifth-detectability SEED=42 NPTS=5000 REAL_ONLY=1 ALPHA_MODE=A

# Mode B (portal-derived proxy)
make fifth-detectability SEED=42 NPTS=5000 REAL_ONLY=1 ALPHA_MODE=B KAPPA=1.0

# Mode C (agnostic scaling)
make fifth-detectability SEED=42 NPTS=5000 REAL_ONLY=1 ALPHA_MODE=C S_FF=1.0 S_LAMBDA=1.0
```

Compare results to see if conclusions are mapping-sensitive.

### Uniform Sampling (No Targeting)

```bash
make fifth-detectability SEED=42 NPTS=10000 REAL_ONLY=1 ALPHA_MODE=A TARGET_FRAC=0.0
```

---

## After the Run

### 1. Interpret Results

**If excluded fraction is large (>10%):**
- Scalar is significantly constrained
- Many parameter combinations are ruled out
- Consider tightening mapping or checking assumptions

**If hunt band is significant (>5%):**
- Scalar is near detection threshold
- Good target for future experiments
- Consider refining constraints in this region

**If most space is far from detection:**
- Scalar survives current constraints
- Not ruled out, but also not detectable
- May need more sensitive experiments or different channels

### 2. Document Findings

Update or create:
- `results/fifth_force/detectability_analysis_v1.4.0.md` - Analysis summary
- Note mapping assumptions used
- Document any mapping sensitivity

### 3. Prepare for Release

If results are ready to publish:

```bash
# Prepare release with results
make prepare-release VERSION=v1.4.0

# Create GitHub Release
# Follow: docs/publishing/GITHUB_RELEASE_INSTRUCTIONS_v1.4.0.md
```

---

## Troubleshooting

**"File not found" errors:**
- Verify canonical CSV is in place: `ls data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv`
- Run ingestion first: `make fifth-ingest`

**"No curves found" errors:**
- Check that ingestion created provenance: `ls results/fifth_force/*.json`
- Verify curve is registered: `make fifth-data-ledger`

**Slow performance:**
- Reduce NPTS for testing (e.g., NPTS=1000)
- Use TARGET_FRAC=0.0 for uniform sampling (faster)

**Results seem wrong:**
- Check that REAL_ONLY=1 if you want only real curves
- Verify alpha mapping mode matches your intent
- Review detectability_summary.md for metadata

---

## Related Documentation

- Fifth-force start guide: `docs/fifth_force_start_here.md`
- Mapping sensitivity: `docs/MAPPING_SENSITIVITY.md`
- Real vs synthetic: `docs/REAL_VS_SYNTHETIC_GUARDRAILS.md`
- Claims and limits: `docs/CLAIMS_LIMITS_AND_FALSIFIERS.md`

---

**Ready to run the science! Place files, then execute the verdict run.**
