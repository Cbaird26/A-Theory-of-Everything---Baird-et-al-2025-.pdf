# Quick Start: A-B-A Pilot Test (15 minutes)

**Goal:** Clean 15-minute pilot with baseline → coherence → baseline.

---

## Setup (5 minutes)

1. **Phone in Airplane Mode** (Wi-Fi/Bluetooth OFF)
2. **Screen OFF**
3. Place on **stable surface** (wood/book, NOT metal table)
4. **Away from:** speakers, power strips, chargers, other phones
5. **Don't touch it** — movement is the #1 fake-signal generator

---

## Recording Protocol (15 minutes total)

### Phase A: Baseline (5 minutes)
- Start recording
- Do nothing special, just sit calmly
- Label: **BASELINE**

### Phase B: Coherence (5 minutes)
- Same setup, same stillness
- Do your coherence practice
- Label: **COHERENCE**

### Phase A: Post (5 minutes)
- Same setup, same stillness
- Return to baseline state
- Label: **POST**

**Total:** 15 minutes (A-B-A design)

---

## Export CSV

Make sure export includes:
- `mx, my, mz` (or `magx, magy, magz` or `x, y, z`) — magnetic field components
- `t` or `time` or `timestamp` (optional, can use `--sample-hz` instead)

**Recommended apps:**
- **iOS:** SensorLog, Physics Toolbox Suite
- **Android:** Sensor Logger, Physics Toolbox Suite

---

## Run Pipeline

```bash
# 1. Convert raw CSV → analysis format
# (block-sec 300 = 5 minutes per block)
python prep_magnetometer_csv.py --in /path/to/raw.csv --out data/raw/em_modulated.csv --block-sec 300 --start 0

# 2. Analyze
python analyze_em.py --data data/raw/em_modulated.csv --out-dir results/em_pilot

# 3. Generate LaTeX snippet
python generate_em_snippet.py --json results/em_pilot/em_modulation_summary.json
```

**What this does:**
- Block 0 (0-300s): `s=0` (baseline)
- Block 1 (300-600s): `s=1` (coherence)
- Block 2 (600-900s): `s=0` (post)

---

## What We're Looking For

A **real effect** should:
- Show the same direction in **BOTH baseline blocks** (A and A)
- Be stable if you change binning (1s vs 2s vs 5s)
- Survive permutation test

**Red flags (likely artifacts):**
- Disappears when you don't touch the phone → motion artifact
- Flips sign between baseline blocks → environmental drift
- Only shows up once → likely noise

---

## Troubleshooting

**If CSV has no timestamps:**
```bash
python prep_magnetometer_csv.py --in raw.csv --out data/raw/em_modulated.csv --sample-hz 10 --block-sec 300 --start 0
```
(Replace `10` with your actual sample rate in Hz)

**If column names don't match:**
The script looks for: `mx/my/mz`, `magx/magy/magz`, `x/y/z`, or `bx/by/bz`
If your CSV uses different names, rename columns to match.

**Check the output:**
```bash
head data/raw/em_modulated.csv
```
Should show: `t,power,s` columns

---

## Next Steps

After you run the pilot:
1. Check `results/em_pilot/em_modulation_summary.json` for β estimate
2. Look at `results/em_pilot/em_modulation_plot.png` for visualization
3. If interesting: replicate with a second run
4. If null: you've established a bound on EM coupling parameters (still valuable!)

---

## Notes

- **Movement is the enemy:** Keep phone still, don't touch it
- **Environmental confounds:** Wi-Fi, Bluetooth, power-line harmonics, temperature drift
- **Even null results are valuable:** They constrain the parameter space
- **Replication is key:** Any interesting finding needs a second independent run

