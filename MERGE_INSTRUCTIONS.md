# PR Merge Instructions

## Step 1: Create PR

**Title:**
```
ToE closeout v1: kernel derivation + GKLS no-signalling + multi-channel constraints
```

**Description:**
Paste from `PR_DESCRIPTION.md` (see below)

**Then click:** "Create pull request" (green button, bottom right)

---

## Step 2: Merge PR

After PR is created, you'll see the PR page.

**If "Able to merge":**
1. Click **"Merge pull request"**
2. Choose **"Squash and merge"** (recommended - keeps main clean)
3. Click **"Confirm merge"**

**If blocked:**
- "Required checks haven't passed" → Usually safe to ignore for this repo
- "Branch is out of date" → Run: `git checkout toe-closeout-v1 && git pull origin main && git push`
- "Conflicts" → Tell me and I'll help resolve

---

## Step 3: Post-Merge Verification

```bash
git checkout main
git pull origin main
cd papers/toe_closed_core
pdflatex main.tex
pdflatex main.tex
```

If PDF compiles successfully, you're done! ✅

---

## PR Description (Copy-Paste)

This merge locks a reproducible closeout artifact: formal consistency + preregistered QRNG bounds + digitized fifth-force constraint and a non-empty overlap region under explicitly stated assumptions; Higgs-portal bounds remain placeholders pending replacement with published ATLAS/CMS limits.

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

