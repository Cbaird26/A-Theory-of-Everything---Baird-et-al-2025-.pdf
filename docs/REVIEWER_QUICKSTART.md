# Reviewer Quickstart Guide

**Date:** 2026-01-19  
**Repository:** MQGT-SCF  
**Time to Complete:** ~10 minutes  
**Goal:** Reproduce key results from a fresh clone

---

## Purpose

This guide enables reviewers and outsiders to run the MQGT-SCF constraint lab and reproduce key results in approximately 10 minutes. It assumes a fresh clone and standard Python environment.

---

## Prerequisites

- Python 3.8 or higher
- Git
- Make (for Unix-like systems) or equivalent

---

## Step 1: Clone and Install (2 minutes)

```bash
# Clone the repository
git clone https://github.com/Cbaird26/MQGT-SCF.git
cd MQGT-SCF

# Install dependencies
make install

# Or manually:
# pip install -r requirements.txt
```

**Expected output:** Dependencies installed without errors.

**Verify installation:**
```bash
python --version  # Should be 3.8+
python -c "import numpy, pandas, matplotlib; print('Dependencies OK')"
```

---

## Step 2: Run Validation Tests (2 minutes)

```bash
# Run all regression tests
make test

# Or run individually:
make qrng-validate      # QRNG regression tests
make fifth-validate     # Fifth-force regression tests
```

**Expected output:** All tests pass (exit code 0).

**If tests fail:**
- Check Python version (requires 3.8+)
- Verify dependencies installed correctly
- See troubleshooting section below

---

## Step 3: Reproduce Key Results (5 minutes)

### Option A: Full Reproduction (Recommended for First Run)

```bash
# Reproduce all results (may take several minutes)
make reproduce
```

**Expected outputs:**
- `results/fifth_force/detectability_summary.md` - Fifth-force detectability analysis
- `results/qrng/multisource_epsilon_summary.md` - QRNG multisource calibration
- `results/DATA_LEDGER.csv` - Dataset ledger
- `results/DATA_LEDGER_SHA256.txt` - SHA256 hashes

### Option B: Quick Fifth-Force Reproduce (Faster)

```bash
# Run fifth-force detectability scan
make fifth-detectability SEED=42 NPTS=2000

# Generate canonical figures
make fifth-figures

# Generate data ledgers
make fifth-data-ledger
make fifth-sha256-ledger
```

**Expected outputs:**
- `results/fifth_force/detectability_summary.md` - Summary with detectability ratios
- `results/fifth_force/detectability_points.csv` - Sampled points with r values
- `fig_alpha_vs_lambda.png`, `fig_r_distribution.png`, `fig_hunt_band_locator.png` - Canonical figures
- `results/DATA_LEDGER.csv` - Dataset ledger
- `results/DATA_LEDGER_SHA256.txt` - SHA256 hashes

### Option C: Quick QRNG Reproduce

```bash
# Run QRNG multisource calibration
make qrng-multisource-report

# Expected output:
# results/qrng/multisource_epsilon_summary.md
# results/qrng/multisource_epsilon_max.json
```

---

## Step 4: Verify Reproducibility (1 minute)

### Check Output Files

```bash
# Verify outputs exist
ls -lh results/fifth_force/detectability_summary.md
ls -lh results/DATA_LEDGER.csv
ls -lh results/DATA_LEDGER_SHA256.txt

# Check summary content
head -20 results/fifth_force/detectability_summary.md
```

**Expected:** Summary file contains:
- Total points computed
- Statistics table (r thresholds, counts, fractions)
- Top points by detectability ratio
- Hunt band identification

### Verify Determinism

With the same seed, outputs should be identical:

```bash
# Run twice with same seed
make fifth-detectability SEED=42 NPTS=100
# ... wait for completion ...
make fifth-detectability SEED=42 NPTS=100

# Check outputs are identical
diff results/fifth_force/detectability_points.csv results/fifth_force/detectability_points.csv
# Should produce no output (files identical)
```

---

## Expected Results Summary

After completing the quickstart, you should see:

### Fifth-Force Results

**Detectability Summary** (`results/fifth_force/detectability_summary.md`):
- Total points: ~856 (with NPTS=2000 default, or as specified)
- Exclusions: ~1.3% of points (r > 1.0)
- Near-detectable: ~1.8% of points (0.1 < r ≤ 1.0)
- Hunt band: λ ~ 0.3-1.3 mm, f_eq ~ 5×10¹⁰–1.6×10¹² Hz

**Key Statistics:**
- Hunt band location: λ ≈ 0.3-1.3 mm (millimeter scales)
- Exclusions: ~1.3% at longer ranges (λ ~ 5-9 mm)
- Safe regions: ~94% far from detection (r < 0.001)

### QRNG Results

**Multisource Summary** (`results/qrng/multisource_epsilon_summary.md`):
- Pooled ε_max: 0.010887 (conservative mode)
- Per-source: NIST Beacon v2 (N=54,434 bits)
- Mode A (Conservative): worst-case bound
- Mode B (Weighted): inverse-variance weighting

### Data Ledgers

**Dataset Ledger** (`results/DATA_LEDGER.csv`):
- Lists all canonical datasets
- Sources, descriptions, versions
- SHA256 hashes for verification

**SHA256 Ledger** (`results/DATA_LEDGER_SHA256.txt`):
- Hash values for all data files
- Enables verification of data integrity

---

## Quick Validation Checklist

After running the quickstart, verify:

- [ ] All tests pass (`make test`)
- [ ] Detectability summary generated
- [ ] Hunt band identified (λ ~ 0.3-1.3 mm)
- [ ] Data ledgers generated
- [ ] SHA256 hashes computed
- [ ] Outputs are deterministic (same seed = same output)

---

## Troubleshooting

### Issue: "make: command not found"

**Solution (Unix-like):** Install Make:
```bash
# macOS
brew install make

# Linux
sudo apt-get install build-essential
```

**Alternative:** Run Python scripts directly:
```bash
python -m code.inference.fifth_force.detectability --seed 42 --n-points 2000
```

### Issue: Import errors

**Solution:** Verify dependencies installed:
```bash
pip install -r requirements.txt
# Or check what's missing:
python -c "import numpy, pandas, matplotlib, scipy"
```

### Issue: Test failures

**Solution:** Check Python version and dependencies:
```bash
python --version  # Should be 3.8+
pip install --upgrade pytest numpy pandas matplotlib scipy
```

### Issue: Missing data files

**Solution:** Verify data directory structure:
```bash
ls data/raw/fifth_force/*.csv
ls data/raw/qrng_sources/*.csv
```

If files are missing, check the repository includes data files or run data ingestion first.

### Issue: Permission errors

**Solution:** Ensure scripts are executable:
```bash
chmod +x scripts/*.sh
```

---

## Next Steps

After successfully running the quickstart:

1. **Read the scientific contract:** [`docs/CLAIMS_LIMITS_AND_FALSIFIERS.md`](CLAIMS_LIMITS_AND_FALSIFIERS.md)
   - Understand what's claimed vs. assumed
   - See falsifiers and limitations

2. **Explore constraint analysis:** [`docs/constraint_lab_snapshot.md`](constraint_lab_snapshot.md)
   - Multi-channel constraint overview
   - Dominance analysis

3. **Review fifth-force results:** [`docs/fifth_force_summary.md`](fifth_force_summary.md)
   - Detailed detectability analysis
   - Hunt band interpretation

4. **Check data ground truth:** [`docs/DATA_GROUND_TRUTH.md`](DATA_GROUND_TRUTH.md) (if exists)
   - Canonical dataset paths
   - Provenance tracking

---

## Advanced Usage

### Real-Only Mode

To exclude synthetic curves and use only real experimental data:

```bash
make fifth-detectability SEED=42 NPTS=2000 REAL_ONLY=1
```

**Note:** Real-only mode requires at least one real curve to be ingested. See [`docs/DATA_GROUND_TRUTH.md`](DATA_GROUND_TRUTH.md) for canonical dataset paths.

### Mapping Sensitivity Modes

To test different α_pred mapping assumptions:

```bash
# Mode A (legacy placeholder)
make fifth-detectability SEED=42 NPTS=2000 ALPHA_MODE=A

# Mode B (portal-derived proxy)
make fifth-detectability SEED=42 NPTS=2000 ALPHA_MODE=B KAPPA=1.0

# Mode C (agnostic scaling)
make fifth-detectability SEED=42 NPTS=2000 ALPHA_MODE=C S_FF=0.1 S_LAMBDA=1.0

# Mode D (ToE-native bridge: κ_cH, v_c → θ → α)
make fifth-detectability SEED=42 NPTS=2000 ALPHA_MODE=D
```

See [`docs/MAPPING_SENSITIVITY.md`](MAPPING_SENSITIVITY.md) for details on mapping modes.

**Mode D (ToE-Native):** Uses explicit ToE equations (Eq. 13) to map portal parameters (κ_cH, v_c) to mixing angle θ_hc, then to Yukawa strength α. This enables exact falsification tests and conversion of experimental bounds to ToE parameter constraints. See `code/inference/fifth_force/toe_bounds.py` for inverse mapping utilities.

### Enhanced Mixture Sampling

When using `--real-only` mode (default), the detectability pipeline automatically uses **50/50 mixture sampling**:
- **50% targeted sampling:** Points sampled within real curve λ coverage ranges
- **50% uniform sampling:** Points sampled uniformly across the full prior range

This provides better coverage of both the experimentally-constrained region and the broader parameter space.

**Default behavior (real-only mode):**
```bash
make fifth-detectability SEED=42 NPTS=2000 REAL_ONLY=1
# Automatically uses 50/50 mixture sampling
```

**Custom target fraction:**
```bash
make fifth-detectability SEED=42 NPTS=2000 REAL_ONLY=1 TARGET_FRAC=0.7
# Uses 70% targeted, 30% uniform sampling
```

**Uniform sampling only (disable mixture):**
```bash
make fifth-detectability SEED=42 NPTS=2000 REAL_ONLY=1 TARGET_FRAC=0.0
# Pure uniform sampling (no targeting)
```

The coverage report in the detectability summary shows per-curve coverage statistics and intersection coverage.

### Converting Experimental Bounds to ToE Parameters

Mode D enables conversion of experimental constraints (e.g., Eöt-Wash) to ToE parameter bounds:

```bash
# Convert Eöt-Wash α_max(λ) curve to ToE parameter bounds
python -m code.inference.fifth_force.toe_bounds \
    data/raw/eotwash_prl2016_digitized_contract.csv \
    --output-csv results/toe_parameter_bounds.csv \
    --f-n 0.30
```

This produces a CSV with columns:
- `lambda_m`: Yukawa range in meters
- `alpha_max`: Original experimental bound
- `theta_max`: Maximum allowed mixing angle (radians)
- `mphi_eV`, `mphi_GeV`: Scalar mediator mass
- `kappa_vc_max_GeV`: Maximum allowed |κ_cH v_c| in GeV

**Interpretation:**
- If your ToE model predicts |κ_cH v_c| > `kappa_vc_max_GeV` at any λ in the experimental window, that parameter choice is excluded.
- The parameter fork: if v_c=0, then Eq. (13) gives no tree-level mixing, and Eöt-Wash may not constrain this channel.

**Python API:**
```python
from code.inference.fifth_force.toe_bounds import compute_full_toe_bounds
import pandas as pd

# Load experimental curve
curve = pd.read_csv('data/raw/eotwash_prl2016_digitized_contract.csv')

# Convert to ToE bounds
toe_bounds = compute_full_toe_bounds(curve, f_n=0.30)

# Access bounds
print(f"|κ_cH v_c| must be < {toe_bounds['kappa_vc_max_GeV'].min():.3e} GeV")
```

---

## Verification Commands

Quick commands to verify everything works:

```bash
# Test suite
make test

# QRNG validation
make qrng-validate

# Fifth-force validation
make fifth-validate

# Quick detectability run
make fifth-detectability SEED=42 NPTS=100

# Check outputs exist
ls -lh results/fifth_force/detectability_summary.md
cat results/fifth_force/detectability_summary.md | head -30
```

---

## Expected Timeline

- **Step 1 (Clone & Install):** ~2 minutes
- **Step 2 (Validation):** ~2 minutes
- **Step 3 (Reproduce):** ~5 minutes (full) or ~2 minutes (quick)
- **Step 4 (Verify):** ~1 minute

**Total:** ~10 minutes for full reproduction

---

## Questions or Issues?

If you encounter problems not covered here:

1. Check the main README: [`README.md`](../README.md)
2. Review detailed guides:
   - [`docs/fifth_force_start_here.md`](fifth_force_start_here.md)
   - [`docs/qrng_multisource_start_here.md`](qrng_multisource_start_here.md)
3. Open an issue on GitHub: https://github.com/Cbaird26/MQGT-SCF/issues

---

**This quickstart is designed to enable rapid verification of reproducibility. If you can complete these steps, the lab is working correctly.**
