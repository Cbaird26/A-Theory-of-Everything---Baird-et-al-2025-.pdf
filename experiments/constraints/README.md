# Constraint Modules — Multi-Channel EFT Bounds

This module implements constraint mapping for MQGT-SCF across multiple experimental channels:

1. **QRNG** (baseline + modulation) — already implemented in `../grok_qrng/`
2. **Fifth-force (Yukawa)** — mediator → Yukawa mapping
3. **Higgs portal** — collider/invisible-width bounds

## Quick Start

```bash
# Generate all constraint figures
python scripts/fifth_force_yukawa.py
python scripts/higgs_portal_bounds.py
python scripts/make_global_constraints.py

# Outputs are in results/
```

## Data Files

- `data/fifth_force_exclusion.csv` — Yukawa exclusion curve (λ, α, excluded)
- `data/higgs_limits.json` — Higgs portal limits (invisible width, signal strength)

**Note:** Currently contains placeholder data. See `REAL_DATA_SCHEMA.md` for instructions on replacing with real digitized bounds.

## Scripts

- `fifth_force_yukawa.py` — Maps mediator (m_M, g_M) → Yukawa (λ, α) and plots exclusion
- `higgs_portal_bounds.py` — Maps Higgs-portal couplings to collider bounds
- `make_global_constraints.py` — Combines all channels into one figure

## Integration

The global constraints figure is automatically copied to `papers/toe_closed_core/figures/` and included in the paper.

## Next Steps

1. Replace placeholder data with real digitized bounds (see `REAL_DATA_SCHEMA.md`)
2. Regenerate figures
3. Update citations in paper if needed

