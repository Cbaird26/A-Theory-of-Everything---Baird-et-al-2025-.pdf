#!/usr/bin/env python3
from __future__ import annotations
import argparse
import re
from pathlib import Path

import pandas as pd

DOMAIN_RULES = [
    ("QRNG / Randomness", ["qrng", "bit", "bern", "dieharder", "nist", "run-length", "autocorrelation", "entropy", "bayes", "bf10"]),
    ("Quantum foundations (GKLS/Collapse)", ["gkls", "lindblad", "collapse", "born", "no-signalling", "nosignalling", "microcausality", "cptp"]),
    ("Mediator / Kernel / Fifth-force", ["yukawa", "kernel", "mediator", "fifth-force", "torsion", "casimir", "equivalence principle", "atom interferometry", "lunar laser"]),
    ("Collider / Higgs portal", ["higgs", "collider", "invisible width", "signal strength", "missing energy", "hl-lhc", "atlas", "cms"]),
    ("Cosmology / Gravity", ["cmb", "bao", "bbn", "inflation", "dark energy", "quintessence", "neff", "isw", "structure growth", "supernova", "h0", "gravitational wave"]),
    ("Neuro / Human coherence", ["eeg", "meg", "hrv", "breath", "meditation", "autonomic", "jhana", "placebo", "prosody", "mind-wandering"]),
    ("AI / Agents / Alignment", ["ai", "agent", "zora", "alignment", "reward", "verification", "proof-carrying", "self-model", "sentience"]),
    ("Research ops / Reproducibility", ["prereg", "preregister", "repo", "ci", "hash", "version", "reproduce", "audit", "digitiz", "webplotdigitizer", "citation"]),
    ("Core field theory / Unification", ["lorentz", "scalar", "lagrangian", "gauge", "anomaly", "rg flow", "horndeski", "ghost", "cutoff", "symmetry"]),
]

CUES_HIGH = ["bounded", "constrain", "experiment", "test", "predict", "likelihood", "bayes", "credible", "posterior", "bf10", "replication", "prereg"]
CUES_MED  = ["map", "derive", "model", "parameter", "channel", "observable", "figure", "table", "protocol", "curve", "plot"]

def classify_domain(text: str) -> str:
    t = text.lower()
    for dom, kws in DOMAIN_RULES:
        if any(k in t for k in kws):
            return dom
    return "Other / conceptual"

def score_testability(text: str, domain: str) -> int:
    t = text.lower()
    score = 0
    if any(c in t for c in CUES_HIGH):
        score += 2
    if any(c in t for c in CUES_MED):
        score += 1
    # physics channels get a small uplift (public bounds exist)
    if domain in {"QRNG / Randomness","Mediator / Kernel / Fifth-force","Collider / Higgs portal","Cosmology / Gravity"}:
        score += 1
    return min(score, 3)

def infer_status(text: str, domain: str) -> str:
    t = text.lower()
    # Items we actually closed in the repo work:
    if "kernel" in t and "mediator" in t:
        return "Closed (formalized in paper)"
    if "gkls" in t or "no-signalling" in t or "nosignalling" in t:
        return "Closed (formalized in paper)"
    if "qrng" in t and ("bounded" in t or "null" in t or "modulation" in t or "block-size" in t or "block size" in t):
        return "Closed (tested/bounded)"
    if "renormalize" in t or "η→0" in t or "eta→0" in t or "flows to baseline" in t:
        return "Closed (bounded; baseline limit)"

    # scaffolded channels you built (need real curves)
    if domain in {"Mediator / Kernel / Fifth-force","Collider / Higgs portal"} and ("bound" in t or "constraint" in t or "limits" in t or "excluded" in t):
        return "Scaffolded (needs digitized real bounds)"

    return "Open"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("infile", type=str, help="Path to docs/hypotheses_500.md")
    ap.add_argument("--outdir", type=str, default="experiments/hypotheses_triage/results")
    args = ap.parse_args()

    inpath = Path(args.infile)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    rows = []
    for line in inpath.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        m = re.match(r"^(\d+)\)\s*(.+)$", line)
        if not m:
            continue
        hid = int(m.group(1))
        txt = m.group(2).strip()
        dom = classify_domain(txt)
        testability = score_testability(txt, dom)
        status = infer_status(txt, dom)
        rows.append((hid, txt, dom, testability, status))

    df = pd.DataFrame(rows, columns=["id","hypothesis","domain","testability","status"]).sort_values("id")

    # Priority: high testability + not closed
    domain_weight = {
        "Mediator / Kernel / Fifth-force": 1.2,
        "Collider / Higgs portal": 1.2,
        "Cosmology / Gravity": 1.15,
        "QRNG / Randomness": 1.0,
        "Quantum foundations (GKLS/Collapse)": 0.9,
        "Core field theory / Unification": 0.85,
        "Neuro / Human coherence": 0.8,
        "AI / Agents / Alignment": 0.75,
        "Research ops / Reproducibility": 0.7,
        "Other / conceptual": 0.5,
    }
    def priority(row):
        base = row["testability"]
        if row["status"].startswith("Closed"):
            base -= 2
        elif row["status"].startswith("Scaffolded"):
            base += 0.5
        return max(0.0, base) * domain_weight.get(row["domain"], 0.6)

    df["priority_score"] = df.apply(priority, axis=1)

    domain_summary = df.groupby(["domain","status"]).size().unstack(fill_value=0).reset_index()
    status_summary = df["status"].value_counts().reset_index().rename(columns={"index":"status", "status":"count"})
    top_next = df.sort_values(["priority_score","testability"], ascending=False).head(30)

    # Write outputs
    df.to_csv(outdir / "hypotheses_matrix.csv", index=False)
    domain_summary.to_csv(outdir / "domain_summary.csv", index=False)
    status_summary.to_csv(outdir / "status_summary.csv", index=False)
    top_next.to_csv(outdir / "top_next_30.csv", index=False)

    report = []
    report.append("# 500 Hypotheses — Triage Report\n")
    report.append("This is a fast triage pass (classification + prioritization). It does not assert physical truth.\n")
    report.append("## Status summary\n")
    report.append(status_summary.to_markdown(index=False))
    report.append("\n\n## Domain × status\n")
    report.append(domain_summary.to_markdown(index=False))
    report.append("\n\n## Top 30 next actions (by priority_score)\n")
    report.append(top_next[["id","domain","testability","status","priority_score","hypothesis"]].to_markdown(index=False))
    (outdir / "report.md").write_text("\n".join(report), encoding="utf-8")

    print(f"Wrote outputs to: {outdir}")

if __name__ == "__main__":
    main()

