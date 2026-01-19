# Interpretation Templates for Hunt Band Results

**Purpose:** Templates for updating canonical statements based on detectability results with real Eöt-Wash curve.

---

## Template A: Hunt Band Persists

**Use this if:** After ingesting real Eöt-Wash curve, hunt band still shows r ≈ 0.1–1 in sub-mm to mm regime.

### Canonical Statement Update

```markdown
## Canonical Statement

**Scalar fifth force not detected; not ruled out; maximally testable at λ ≈ [X.X] mm (sub-mm to mm: 10⁻⁴ to 10⁻³ m) under real Eöt-Wash experimental constraints.**

Under real digitized Eöt-Wash mm-cm constraints, the MQGT-SCF scalar fifth force:
- **Not detected:** No points exceed experimental bounds by significant margins
- **Not ruled out:** [X]% of parameter space remains viable
- **Maximally testable:** Hunt band at λ ≈ [X.X] mm where r ≈ [X.X]–[X.X] (almost detectable)

**Next experimental target:** Precision measurements at λ ≈ [X.X] mm (sub-mm to mm scales) with torsion balance tests, molecule spectroscopy, or Casimir tests would decisively test or falsify this scalar class.
```

### Interpretation Section Update

```markdown
## Interpretation

Under real digitized Eöt-Wash constraints, the scalar fifth force is:

1. **Not detected:** No points exceed experimental bounds by significant margins in the viable parameter space.
2. **Maximally constrained** in a narrow band around λ ≈ [X.X] mm (sub-mm to mm: 10⁻⁴ to 10⁻³ m), where `r ≈ [X.X]–[X.X]` (almost detectable).
3. **Excluded** at longer ranges (λ ~ [X]–[X] mm) for a small fraction ([X]%) of sampled points.
4. **Far from detection** (r ≪ 1) at shorter scales and most of the parameter space.

The structured clustering of high-r points in the sub-mm to mm regime (rather than random distribution) suggests this is a model feature, not sampling noise. **The hunt band persists under real experimental constraints, confirming this as a credible target regime for experimental probes.**
```

### Statistics to Fill In

- Total points: [N]
- r > 1.0: [X] points ([X.X]%)
- r > 0.1: [X] points ([X.X]%)
- r > 0.01: [X] points ([X.X]%)
- Highest r (non-excluded): [X.XXX] at λ = [X.XXX] mm
- Hunt band range: λ ≈ [X.X]–[X.X] mm

---

## Template B: Hunt Band Collapses

**Use this if:** After ingesting real Eöt-Wash curve, most points have r ≪ 1, hunt band disappears.

### Canonical Statement Update

```markdown
## Canonical Statement

**Scalar fifth force ruled out at sub-mm to mm scales under real Eöt-Wash experimental constraints.**

Under real digitized Eöt-Wash mm-cm constraints, the MQGT-SCF scalar fifth force is effectively excluded in the sub-mm to mm regime. The previously identified hunt band collapses, with [X]% of points having r < 0.001, indicating the scalar is far below experimental sensitivity at these scales.

**Conclusion:** This scalar class is not viable at sub-mm to mm scales under existing constraints. Future work should focus on other length regimes or alternative detection channels.
```

### Interpretation Section Update

```markdown
## Interpretation

Under real digitized Eöt-Wash constraints, the scalar fifth force is:

1. **Ruled out** at sub-mm to mm scales: [X]% of points have r < 0.001, indicating the scalar is far below experimental sensitivity.
2. **Hunt band collapsed:** The previously identified hunt band at λ ≈ 0.5 mm disappears under real constraints.
3. **Excluded** at longer ranges (λ ~ [X]–[X] mm) for [X]% of sampled points.
4. **Not detectable** in the mm-cm regime under current experimental bounds.

**Conclusion:** This class of scalar is effectively ruled out at sub-mm to mm scales. This is a valuable null result that constrains the parameter space and guides future model development.
```

### Statistics to Fill In

- Total points: [N]
- r > 1.0: [X] points ([X.X]%)
- r > 0.1: [X] points ([X.X]%) - should be very low
- r > 0.01: [X] points ([X.X]%)
- r < 0.001: [X] points ([X.X]%) - should be high
- Highest r (non-excluded): [X.XXX] at λ = [X.XXX] mm

---

## Template C: Partial Persistence

**Use this if:** Hunt band weakens but doesn't fully collapse (r ≈ 0.01–0.1 instead of 0.1–1).

### Canonical Statement Update

```markdown
## Canonical Statement

**Scalar fifth force not detected; weakly constrained at λ ≈ [X.X] mm under real Eöt-Wash experimental constraints.**

Under real digitized Eöt-Wash mm-cm constraints, the MQGT-SCF scalar fifth force:
- **Not detected:** No points exceed experimental bounds
- **Weakly constrained:** Small fraction ([X]%) of points show r ≈ 0.01–0.1 at λ ≈ [X.X] mm
- **Mostly safe:** [X]% of points have r < 0.001, far below detection

**Conclusion:** The scalar is not viable at sub-mm to mm scales under current constraints, though a small region remains marginally constrained. Future experiments could tighten bounds further or rule out this regime completely.
```

---

## How to Use These Templates

1. **Run detectability** with real curve:
   ```bash
   make fifth-detectability SEED=42 NPTS=5000
   ```

2. **Extract statistics** from `results/fifth_force/detectability_summary.md`:
   - Counts and fractions for r > thresholds
   - Top points by detectability ratio
   - Lambda range of hunt band

3. **Choose template** (A, B, or C) based on results

4. **Fill in values** from statistics

5. **Update** `docs/fifth_force_detectability_summary.md`:
   - Replace "Canonical Statement" section
   - Update "Interpretation" section
   - Update statistics table
   - Update "Limitations" (mark real curve as included)

6. **Update** `docs/notes/2026-01-08_scalar_detectability_hunt_band.md`:
   - Update hunt band analysis
   - Update synthesis and conclusion

---

## Key Phrases to Use

**If band persists:**
- "Hunt band persists under real experimental constraints"
- "Credible target regime for experimental probes"
- "Maximally testable at λ ≈ [X.X] mm"

**If band collapses:**
- "Hunt band collapses under real constraints"
- "Scalar ruled out at sub-mm to mm scales"
- "Valuable null result"

**Always:**
- "Not detected" (never claim detection)
- "Not ruled out" or "Ruled out" (be precise)
- "Under real experimental constraints" (anchor to data)

---

**These templates ensure consistent, defensible interpretation regardless of outcome.**

