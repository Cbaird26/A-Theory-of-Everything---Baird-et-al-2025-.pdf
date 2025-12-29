# Triage Results Integration Guide

## Status Snapshot (from 500-hypothesis triage)

- **Open:** 475
- **Scaffolded (needs digitized bounds):** 15
- **Closed (formalized math):** 5
- **Closed (tested/bounded):** 5

## Top 4 Next Moves (Highest Leverage)

1. **Replace fifth-force placeholder curves** with one real published exclusion curve
   - Digitize → drop into CSV schema → regenerate plots
   - Target: Adelberger 2009 or Kapner 2007

2. **Replace Higgs portal placeholder limits** with one conservative ATLAS/CMS bound
   - Update JSON → regenerate
   - Target: ATLAS-CMS combined Run 2 limits

3. **Run global overlap region check**
   - QRNG + fifth-force + Higgs
   - See if viable parameter space exists

4. **Add cosmology likelihoods** (one dataset at a time, minimal)
   - Only after steps 1-3 are complete

## Immediate Action: Scaffolded Items

Filter the triage results for `status = Scaffolded` - these are the "we already built the module, we just need real bounds curves" items.

**These are your immediate marching orders.**

## Domain Distribution

- Other / conceptual: 213
- Mediator / Kernel / Fifth-force: 81
- AI / Agents / Alignment: 65
- Research ops / Reproducibility: 43
- QRNG / Randomness: 25
- Core field theory / Unification: 21
- Neuro / Human coherence: 16
- Cosmology / Gravity: 15
- Quantum foundations (GKLS/Collapse): 13
- Collider / Higgs portal: 4

## What "No Tilt" Implies

- Deformation (η / tilt / modulation) is **consistent with 0 at current sensitivity**
- Model **flows to baseline fixed point** in lab
- Next move: **push constraints into channels where new fields would show up even if QRNG stays null**
  - Fifth-force, Higgs portal, cosmology, precision clocks, etc.

This is EFT discipline: keep the framework, but couplings are bounded → hunt elsewhere.

## File Locations (when integrated)

- Full matrix: `experiments/hypotheses_triage/results/hypotheses_matrix.csv`
- Top 30: `experiments/hypotheses_triage/results/top_next_30.csv`
- Report: `experiments/hypotheses_triage/results/report.md`
- Clusters: `experiments/hypotheses_triage/results/clusters.csv`

