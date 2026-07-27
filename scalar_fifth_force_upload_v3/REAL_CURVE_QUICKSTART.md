# Real Curve Quick Start 🎯

**Everything you need to complete Steps 2-5 once digitization is done.**

---

## One Command to Rule Them All

**Expected CSV location:** `data_raw/eotwash_prl2016_digitized_contract.csv` (in package folder)

**OR** if running from repo root: `data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv`

Once you have the digitized CSV in the correct location:

```bash
# From repo root:
./scripts/process_real_eotwash_curve.sh

# OR manually:
make fifth-ingest INPUT=data/raw/fifth_force/eotwash_prl2016_digitized_contract.csv
make fifth-detectability SEED=42 NPTS=2000
```

That's it! The script will:
1. ✅ Ingest the digitized curve
2. ✅ Rerun detectability analysis  
3. ✅ Show you the key statistics
4. ✅ Tell you what to update next

---

## What Happens Next

After the script runs, you'll need to:

1. **Review results:** `cat results/fifth_force/detectability_summary.md`
2. **Update canonical statement:** Use `docs/dev/canonical_statement_template.md`
3. **Update related docs:** Follow `docs/dev/real_curve_workflow.md` Step 8

---

## Full Workflow

See `docs/dev/real_curve_workflow.md` for complete step-by-step guide.

---

## Files Created

- ✅ `scripts/process_real_eotwash_curve.sh` - Automation script
- ✅ `docs/dev/canonical_statement_template.md` - Update template
- ✅ `docs/dev/real_curve_workflow.md` - Complete checklist

---

## Status

**Step 1 (Digitization):** Manual - use `docs/dev/eotwash_digitization_guide.md`  
**Steps 2-5 (Processing):** Automated - ready to run!  
**Step 6+ (Documentation):** Templates ready - follow workflow

---

**Ready when you are!** 🚀

