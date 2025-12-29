# Merge Runbook — Step-by-Step

## ✅ Pre-Flight Check (DONE)

- [x] Branch: `toe-closeout-v1`
- [x] Latest commit: `09b9554` (Add post-merge verification checklist and citation section)
- [x] Remote tracking: `origin/toe-closeout-v1`
- [x] PR description ready: `PR_DESCRIPTION.md`
- [x] Post-merge checklist ready: `POST_MERGE_CHECKLIST.md`

**Note:** Uncommitted files (if any) won't be included in the PR unless explicitly `git add`ed. You can ignore them or stash with `git stash -u` if they're cluttering your view.

---

## Step 1: Open PR in Browser (MANUAL)

1. Go to: https://github.com/Cbaird26/A-Theory-of-Everything---Baird-et-al-2025-.pdf.git
2. Click **Pull requests** → **New pull request**
3. Set (double-check these):
   - **Base:** `main` ← **Compare:** `toe-closeout-v1`
4. **Title:** `ToE closeout v1: kernel derivation + GKLS no-signalling + QRNG constraints`
5. **Description:** Copy from `PR_DESCRIPTION.md` (see below)
6. Click **Create pull request**
7. Review the diff
8. Click **Merge pull request** → **Confirm merge**

---

## Step 2: Post-Merge Sync (Run these commands)

```bash
cd ~/mqgt-scf-paper
git checkout main
git pull origin main
git log -5 --oneline  # Verify merge commit is present
```

---

## Step 3: Smoke Test Paper

```bash
cd papers/toe_closed_core
pdflatex main.tex
pdflatex main.tex
ls -lah main.pdf  # Should show ~264K
```

---

## Step 4: Smoke Test QRNG Pipeline

```bash
cd ../../experiments/grok_qrng
source .venv/bin/activate
python analyze_qrng.py --data-dir data/raw --out-dir results --prior 1.0
# Should run without crashing (even if no data files exist)
```

---

## Step 5: Verify Citation Section

```bash
cd ../../
grep -A 5 "## Citation" README.md
ls -lah POST_MERGE_CHECKLIST.md
```

---

## Step 6: Optional — Tag Release

```bash
git tag -a toe-closeout-v1.0 -m "ToE closeout v1.0: kernel + GKLS + QRNG constraints"
git push origin toe-closeout-v1.0
```

Then on GitHub: **Releases** → **Draft a new release** → Select tag `toe-closeout-v1.0`

---

## PR Description (Copy-Paste)

**Title:**
```
ToE closeout v1: kernel derivation + GKLS no-signalling + QRNG constraints
```

**Description:**
```
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
```

---

## Status: Ready to Merge ✅

All core work is committed and pushed. The uncommitted files (docs, scripts) don't affect the PR.

**Next action:** Open the PR in your browser and merge it.

