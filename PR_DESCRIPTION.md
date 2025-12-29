# PR Description

**Title:**
ToE closeout v1: kernel derivation + GKLS no-signalling + QRNG constraints + multi-channel bounds

**Description:**

This merge locks a reproducible closeout artifact: formal consistency + preregistered QRNG bounds + digitized fifth-force constraint and a non-empty overlap region under explicitly stated assumptions; Higgs-portal bounds remain placeholders pending replacement with published ATLAS/CMS limits.

**Original Description:**

* Adds a reviewer-proof close-out package for the ToE core:

  * Derives the nonlocal kernel (K) from a local mediator (Green's function → Yukawa limit).
  * Formalizes modified measurement dynamics as local GKLS/Lindblad with an operational no-signalling theorem.
  * Declares minimal EFT parameterization + constraint channel mapping + operational measurement model.
* Adds a calibrated QRNG experimental pipeline:

  * Control tests (fair + known biased) validate detection + credible intervals.
  * Real hardware QRNG baseline (LfD / ID Quantique) yields strong evidence favoring the fair-coin null and bounds (|\epsilon|).
  * Preregistered within-run modulation test (alternating protocol) yields null modulation; block-size stability shows sign flips consistent with noise.
* Integrates constraints into the paper and recompiles PDF.
* Everything is committed on `toe-closeout-v1` and ready to merge to `main`.

**Notes:**

* PDFs are only whitelisted in `papers/` and `docs/` by pre-commit hook.

