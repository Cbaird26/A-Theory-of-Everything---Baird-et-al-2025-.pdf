#!/usr/bin/env python3
import argparse, json, re, math
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.special import betaln, expit, betaincinv


# -----------------------------
# Parsers (CSV / JSON / bitfile)
# -----------------------------

def _extract_bits_from_text(s: str) -> np.ndarray:
    # Keep only 0/1 characters; ignore spaces/commas/etc.
    bits = re.findall(r"[01]", s)
    if not bits:
        return np.array([], dtype=np.int8)
    return np.array([int(b) for b in bits], dtype=np.int8)

def load_bits_any(path: Path) -> pd.DataFrame:
    """
    Returns a DataFrame with at least:
      - bit (0/1)
    Optionally:
      - t (timestamp or trial index)
      - s (modulation signal in [-1,1] or {0,1})
    Accepted inputs:
      - CSV with columns like bit, b, outcome; optional t/time, optional s/mod/condition
      - JSON list of dicts with keys bit/b/outcome, optional t/time, optional s/mod/condition
      - Plain text containing 0/1 bitstring (any separators)
    """
    suffix = path.suffix.lower()

    if suffix in [".csv", ".tsv"]:
        df = pd.read_csv(path) if suffix == ".csv" else pd.read_csv(path, sep="\t")
        df = normalize_columns(df)
        return df

    if suffix in [".json", ".jsonl"]:
        if suffix == ".jsonl":
            rows = []
            with path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        rows.append(json.loads(line))
            df = pd.DataFrame(rows)
        else:
            obj = json.loads(path.read_text(encoding="utf-8"))
            df = pd.DataFrame(obj if isinstance(obj, list) else obj.get("data", []))
        df = normalize_columns(df)
        return df

    # Plain text fallback
    text = path.read_text(encoding="utf-8", errors="ignore")
    bits = _extract_bits_from_text(text)
    df = pd.DataFrame({"bit": bits, "t": np.arange(len(bits), dtype=np.int64)})
    return df

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Try to find bit column
    colmap = {c.lower(): c for c in df.columns}
    bit_candidates = ["bit", "b", "outcome", "x", "value"]
    bit_col = next((colmap[c] for c in bit_candidates if c in colmap), None)
    if bit_col is None:
        # Sometimes bits are in a column of strings like "010101"
        # Try first column as fallback
        first = df.columns[0]
        bits = _extract_bits_from_text("".join(df[first].astype(str).tolist()))
        return pd.DataFrame({"bit": bits, "t": np.arange(len(bits), dtype=np.int64)})

    out = pd.DataFrame()
    out["bit"] = pd.to_numeric(df[bit_col], errors="coerce").astype("Int64")
    out = out.dropna(subset=["bit"])
    out["bit"] = out["bit"].astype(int)
    out = out[(out["bit"] == 0) | (out["bit"] == 1)].copy()

    # optional time / trial index
    t_candidates = ["t", "time", "timestamp", "trial", "idx", "index"]
    t_col = next((colmap[c] for c in t_candidates if c in colmap), None)
    if t_col is not None:
        out["t"] = pd.to_numeric(df[t_col], errors="coerce")
    else:
        out["t"] = np.arange(len(out), dtype=np.int64)

    # optional modulation signal
    s_candidates = ["s", "mod", "signal", "condition", "valence", "eth", "e"]
    s_col = next((colmap[c] for c in s_candidates if c in colmap), None)
    if s_col is not None:
        s = pd.to_numeric(df[s_col], errors="coerce")
        out["s"] = s
    # else: no modulation column (fine)

    return out.reset_index(drop=True)


# -----------------------------------
# Statistics: bias + Bayes factor null
# -----------------------------------

def beta_binomial_log_marginal(k: int, n: int, a: float, b: float) -> float:
    # log ∫ Bin(k|n,p) Beta(p|a,b) dp = log Beta(k+a, n-k+b) - log Beta(a,b)
    return betaln(k + a, n - k + b) - betaln(a, b)

def bayes_factor_bias_vs_fair(bits: np.ndarray, prior_strength: float = 1.0) -> Tuple[float, Dict]:
    """
    H0: p = 0.5
    H1: p ~ Beta(a,b) centered at 0.5; use symmetric Beta(prior_strength, prior_strength)
    Returns BF10 (evidence for bias) and summary dict.
    """
    n = int(bits.size)
    k = int(bits.sum())
    a = prior_strength
    b = prior_strength

    # log p(D|H0)
    # Binomial likelihood at p=0.5: (0.5^n)
    log_p_D_H0 = -n * math.log(2.0)

    # log p(D|H1)
    log_p_D_H1 = beta_binomial_log_marginal(k, n, a, b)

    log_BF10 = log_p_D_H1 - log_p_D_H0
    BF10 = float(math.exp(log_BF10))

    phat = k / n if n else float("nan")
    eps = phat - 0.5

    # Posterior Beta parameters: Beta(k + a, n - k + b)
    post_a = k + a
    post_b = n - k + b
    
    # 95% credible interval for p
    p_lower = float(betaincinv(post_a, post_b, 0.025))
    p_upper = float(betaincinv(post_a, post_b, 0.975))
    
    # 95% credible interval for epsilon
    eps_lower = p_lower - 0.5
    eps_upper = p_upper - 0.5

    return BF10, {
        "n": n, "k": k, "p_hat": phat, "epsilon_hat": eps,
        "prior_a": a, "prior_b": b,
        "log_p_D_H0": float(log_p_D_H0),
        "log_p_D_H1": float(log_p_D_H1),
        "log_BF10": float(log_BF10),
        "BF10": BF10,
        "p_lower_95": p_lower,
        "p_upper_95": p_upper,
        "epsilon_lower_95": eps_lower,
        "epsilon_upper_95": eps_upper
    }


# ---------------------------------------------------
# Modulated model: logistic regression (optional signal)
# ---------------------------------------------------

def fit_logistic_modulation(bits: np.ndarray, s: np.ndarray, lr: float = 0.05, steps: int = 4000) -> Dict:
    """
    Model: p_t = sigmoid(alpha + beta*s_t)
    Returns MLE-ish gradient descent fit (simple, robust).
    """
    s = np.asarray(s, dtype=float)
    y = bits.astype(float)
    # standardize s to avoid scaling weirdness
    if np.nanstd(s) > 0:
        s0 = (s - np.nanmean(s)) / (np.nanstd(s) + 1e-12)
    else:
        s0 = s.copy()

    alpha = 0.0
    beta = 0.0

    for _ in range(steps):
        p = expit(alpha + beta * s0)
        # gradients of log-likelihood
        grad_a = np.sum(y - p)
        grad_b = np.sum((y - p) * s0)
        alpha += lr * grad_a / len(y)
        beta += lr * grad_b / len(y)

    p = expit(alpha + beta * s0)
    ll = float(np.sum(y * np.log(p + 1e-12) + (1 - y) * np.log(1 - p + 1e-12)))

    return {"alpha": float(alpha), "beta": float(beta), "loglik": ll}


# -------------
# Main pipeline
# -------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=str, default="data/raw", help="Directory with raw QRNG logs")
    ap.add_argument("--out-dir", type=str, default="results", help="Output directory")
    ap.add_argument("--prior", type=float, default=1.0, help="Symmetric Beta prior strength for bias test")
    args = ap.parse_args()

    data_dir = Path(args.data_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    all_rows = []
    for p in sorted(data_dir.glob("*")):
        if p.is_dir():
            continue
        df = load_bits_any(p)
        bits = df["bit"].to_numpy(dtype=np.int8)

        BF10, summ = bayes_factor_bias_vs_fair(bits, prior_strength=args.prior)
        row = {"file": p.name, **summ}

        if "s" in df.columns and df["s"].notna().any():
            s = df["s"].fillna(0.0).to_numpy(dtype=float)
            modfit = fit_logistic_modulation(bits, s)
            row.update({f"mod_{k}": v for k, v in modfit.items()})
        all_rows.append(row)

        # Quick plot per file: cumulative epsilon
        cum = np.cumsum(bits) / (np.arange(len(bits)) + 1) - 0.5
        plt.figure()
        plt.plot(cum)
        plt.xlabel("trial")
        plt.ylabel("cumulative epsilon (p_hat - 0.5)")
        plt.title(p.name)
        plt.tight_layout()
        plt.savefig(out_dir / f"{p.stem}_cumulative_epsilon.png", dpi=200)
        plt.close()

    res = pd.DataFrame(all_rows)
    res.to_csv(out_dir / "summary.csv", index=False)

    # Aggregate across all files
    if len(all_rows) > 0:
        # combine all bits across files for a global BF
        global_bits = []
        for p in sorted(data_dir.glob("*")):
            if p.is_dir():
                continue
            df = load_bits_any(p)
            global_bits.append(df["bit"].to_numpy(dtype=np.int8))
        global_bits = np.concatenate(global_bits) if global_bits else np.array([], dtype=np.int8)

        BF10, summ = bayes_factor_bias_vs_fair(global_bits, prior_strength=args.prior)
        (out_dir / "global_summary.json").write_text(json.dumps(summ, indent=2), encoding="utf-8")

        # Global cumulative epsilon plot
        cum = np.cumsum(global_bits) / (np.arange(len(global_bits)) + 1) - 0.5
        plt.figure()
        plt.plot(cum)
        plt.xlabel("trial")
        plt.ylabel("cumulative epsilon (p_hat - 0.5)")
        plt.title("GLOBAL")
        plt.tight_layout()
        plt.savefig(out_dir / "GLOBAL_cumulative_epsilon.png", dpi=220)
        plt.close()

    print(f"Wrote: {out_dir/'summary.csv'}")
    print(f"Wrote: {out_dir/'global_summary.json'} (if data present)")
    print("Done.")

if __name__ == "__main__":
    main()

