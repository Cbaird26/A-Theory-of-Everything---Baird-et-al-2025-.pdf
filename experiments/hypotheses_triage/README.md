# Hypotheses Triage Engine

Fast classification and prioritization of 500 hypotheses into actionable categories.

## Quick Start

1. **Create the hypotheses file:**
   ```bash
   # Create docs/hypotheses_500.md with numbered list:
   # 1) First hypothesis...
   # 2) Second hypothesis...
   # ...
   # 500) Last hypothesis...
   ```

2. **Run the triage:**
   ```bash
   python experiments/hypotheses_triage/triage_500.py docs/hypotheses_500.md
   ```

3. **Check outputs:**
   - `results/hypotheses_matrix.csv` - Full matrix (all 500)
   - `results/domain_summary.csv` - Counts by domain × status
   - `results/status_summary.csv` - Counts by status
   - `results/top_next_30.csv` - Priority-ranked top 30
   - `results/report.md` - Human-readable summary

## What It Does

- **Classifies** each hypothesis into domains (QRNG, Quantum foundations, Mediator, Collider, Cosmology, Neuro, AI, Research ops, Core theory)
- **Scores testability** (0-3) based on keywords
- **Infers status:**
  - "Closed" - Already formalized/tested in repo
  - "Scaffolded" - Code exists, needs real data
  - "Open" - Not yet addressed
- **Prioritizes** by testability + domain weight + status

## Dependencies

```bash
pip install pandas
```

## Output Interpretation

- **Priority score:** Higher = more actionable next step
- **Testability:** 0-3 (higher = more testable)
- **Status:** Closed/Scaffolded/Open
- **Domain:** Which physics/experimental channel

The top 30 list gives you the immediate "what to do next" roadmap.

