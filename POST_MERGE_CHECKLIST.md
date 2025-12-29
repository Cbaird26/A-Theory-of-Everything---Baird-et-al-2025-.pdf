# Post-Merge Checklist (Optional)

## Immediate Verification (after PR merge)

1. **Verify `main` has the merge commit**
   - Repo → `main` branch → confirm latest commit message references the closeout PR
   - Locally: `git checkout main && git pull`

2. **Smoke test: build + run in one go**
   
   From a fresh clone (or locally):
   
   ```bash
   # Build paper
   cd papers/toe_closed_core
   pdflatex main.tex
   pdflatex main.tex
   ```
   
   and
   
   ```bash
   # Run analysis pipeline
   cd ../../experiments/grok_qrng
   source .venv/bin/activate
   python analyze_qrng.py --data-dir data/raw --out-dir results --prior 1.0
   ```

3. **Pin the citation**
   - Add/confirm a short "How to cite this closeout" section in the repo README
   - Include: branch/tag name, commit hash, paper path (`papers/toe_closed_core/main.pdf`)

---

## Immediate (after PR merge)

- [x] PR merged to `main`
- [ ] Verify `main` branch is up to date locally: `git checkout main && git pull`

## Optional: Tag a Release (for citation)

```bash
git checkout main
git tag -a toe-closeout-v1.0 -m "ToE closeout v1: kernel derivation + GKLS no-signalling + QRNG constraints"
git push origin toe-closeout-v1.0
```

Then on GitHub: **Releases** → **Draft a new release** → Select tag `toe-closeout-v1.0`

## Optional: Zenodo DOI (for archival)

1. Go to https://zenodo.org
2. Connect GitHub account
3. Enable repository for Zenodo
4. Create a new GitHub release (triggers Zenodo archive)

## What's Already Complete

✅ Theory defined (MQGT-SCF Lagrangian + field equations)  
✅ Reviewer objections answered (kernel derivation, no-signalling, parameterization)  
✅ Experimental pipeline built and calibrated  
✅ Real QRNG data analyzed (baseline + modulation)  
✅ Null results reported with bounds  
✅ Paper updated and compiled  
✅ Everything committed and pushed  

**The project is complete. Everything else is polish.**

