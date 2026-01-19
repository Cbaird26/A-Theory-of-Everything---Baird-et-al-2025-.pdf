#!/usr/bin/env python3
"""
Generate publishable frequency ladder figure for MQGT-SCF.

Creates a log-scale frequency axis with constraint channels highlighted,
showing the span from cosmology (~10^-18 Hz) to Planck scale (~10^43 Hz).
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Physical constants
C_LIGHT = 299792458.0  # m/s
H_PLANCK = 6.62607015e-34  # J·s
EV_TO_JOULE = 1.602176634e-19  # J/eV

# Frequency landmarks (Hz)
FREQ_LANDMARKS = {
    "Cosmic expansion (H₀)": 2.18e-18,
    "Nanohertz GW (PTA)": 1e-9,
    "1/year": 3.17e-8,
    "1/day": 1.16e-5,
    "Schumann resonance": 7.83,
    "Human hearing (max)": 2e4,
    "Hydrogen 21cm": 1.420405751e9,
    "Cesium-133 (SI second)": 9192631770.0,
    "CMB peak": 1.602e11,
    "Visible light": 6e14,
    "Higgs mass (equiv)": 3.02e25,
    "Planck frequency": 1.85e43,
}

# Constraint channels (frequency ranges in Hz)
CONSTRAINT_CHANNELS = {
    "Cosmology": {
        "freq_range": [2e-18, 2.2e-18],
        "color": "blue",
        "label": "Cosmology (Hubble-scale clock)",
    },
    "Fifth-force (Eöt-Wash)": {
        "freq_range": [5.14e10, 1.59e12],
        "color": "orange",
        "label": "Fifth-force (Eöt-Wash λ → f_eq)",
    },
    "Fifth-force (Bennu)": {
        "freq_range": [2.4e-4, 2.4e-3],
        "color": "orange",
        "label": "Fifth-force (Bennu/OSIRIS-REx)",
        "alpha": 0.5,
    },
    "QRNG": {
        "freq_range": [1e3, 1e7],
        "color": "green",
        "label": "QRNG (device/DAQ bandwidth)",
    },
    "Atomic Spectroscopy": {
        "freq_range": [2.4e15, 2.4e21],  # ~10 eV to 10^7 eV via E = hf
        "color": "cyan",
        "label": "Atomic Spectroscopy (ETH Zurich, ~100 mHz precision)",
    },
    "Higgs": {
        "freq_range": [3e25, 3e25],
        "color": "red",
        "label": "Higgs / collider (energy↔frequency)",
    },
}

# Hunt band from detectability analysis
HUNT_BAND = {
    "freq_range": [8.4e9, 9.0e11],
    "color": "purple",
    "label": "Hunt band (0.1 < r ≤ 1.0)",
    "alpha": 0.3,
}


def lambda_to_freq_eq(lambda_m: float) -> float:
    """Convert Yukawa range to equivalent frequency."""
    if lambda_m <= 0:
        return np.nan
    return C_LIGHT / (2.0 * np.pi * lambda_m)


def create_frequency_ladder_figure(
    output_png: Path = None,
    output_pdf: Path = None,
    figsize=(12, 8),
):
    """Create the frequency ladder figure."""
    if output_png is None:
        output_png = Path("results/frequency_ladder.png")
    if output_pdf is None:
        output_pdf = Path("results/frequency_ladder.pdf")
    
    # Ensure output directories exist
    output_png.parent.mkdir(parents=True, exist_ok=True)
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Set up log scale
    freq_min = 1e-20
    freq_max = 1e44
    ax.set_xscale('log')
    ax.set_xlim(freq_min, freq_max)
    ax.set_xlabel('Frequency (Hz) on a log scale', fontsize=12)
    ax.set_ylabel('', fontsize=12)
    ax.set_title(
        'MQGT-SCF: Constraint Channels on a Frequency Axis\n'
        '(translation layer, not evidence)',
        fontsize=14,
        fontweight='bold'
    )
    
    # Draw constraint channels as horizontal bars
    y_positions = {}
    y_pos = 0.5
    
    # Cosmology
    y_positions["Cosmology"] = y_pos
    chan = CONSTRAINT_CHANNELS["Cosmology"]
    ax.barh(
        y_pos, 
        chan["freq_range"][1] - chan["freq_range"][0],
        left=chan["freq_range"][0],
        height=0.3,
        color=chan["color"],
        alpha=0.7,
        label=chan["label"]
    )
    y_pos += 1
    
    # Fifth-force (Bennu)
    y_positions["Fifth-force (Bennu)"] = y_pos
    chan = CONSTRAINT_CHANNELS["Fifth-force (Bennu)"]
    ax.barh(
        y_pos,
        chan["freq_range"][1] - chan["freq_range"][0],
        left=chan["freq_range"][0],
        height=0.3,
        color=chan["color"],
        alpha=chan.get("alpha", 0.7),
        label=chan["label"]
    )
    y_pos += 1
    
    # QRNG
    y_positions["QRNG"] = y_pos
    chan = CONSTRAINT_CHANNELS["QRNG"]
    ax.barh(
        y_pos,
        chan["freq_range"][1] - chan["freq_range"][0],
        left=chan["freq_range"][0],
        height=0.3,
        color=chan["color"],
        alpha=0.7,
        label=chan["label"]
    )
    y_pos += 1
    
    # Fifth-force (Eöt-Wash)
    y_positions["Fifth-force (Eöt-Wash)"] = y_pos
    chan = CONSTRAINT_CHANNELS["Fifth-force (Eöt-Wash)"]
    ax.barh(
        y_pos,
        chan["freq_range"][1] - chan["freq_range"][0],
        left=chan["freq_range"][0],
        height=0.3,
        color=chan["color"],
        alpha=0.7,
        label=chan["label"]
    )
    
    # Add hunt band overlay
    ax.barh(
        y_pos,
        HUNT_BAND["freq_range"][1] - HUNT_BAND["freq_range"][0],
        left=HUNT_BAND["freq_range"][0],
        height=0.15,
        color=HUNT_BAND["color"],
        alpha=HUNT_BAND["alpha"],
        label=HUNT_BAND["label"]
    )
    y_pos += 1
    
    # Atomic Spectroscopy
    y_positions["Atomic Spectroscopy"] = y_pos
    chan = CONSTRAINT_CHANNELS["Atomic Spectroscopy"]
    ax.barh(
        y_pos,
        chan["freq_range"][1] - chan["freq_range"][0],
        left=chan["freq_range"][0],
        height=0.3,
        color=chan["color"],
        alpha=0.7,
        label=chan["label"]
    )
    y_pos += 1
    
    # Higgs
    y_positions["Higgs"] = y_pos
    chan = CONSTRAINT_CHANNELS["Higgs"]
    # Single point, draw as small bar
    ax.barh(
        y_pos,
        freq_max * 0.01,  # Small width for visibility
        left=chan["freq_range"][0],
        height=0.3,
        color=chan["color"],
        alpha=0.7,
        label=chan["label"]
    )
    
    # Add vertical reference lines for key frequencies
    ref_freqs = {
        "1/day": 1.16e-5,
        "Schumann ~7.8 Hz": 7.83,
        "Cs-133 (1 s)": 9192631770.0,
        "Hearing ~20 kHz": 2e4,
        "Visible (f_opt)": 6e14,
        "Planck ~1/t_P": 1.85e43,
    }
    
    for label, freq in ref_freqs.items():
        if freq_min <= freq <= freq_max:
            ax.axvline(freq, color='lightblue', linestyle='--', alpha=0.5, linewidth=0.8)
            ax.text(freq, y_pos + 0.5, label, rotation=90, 
                  ha='right', va='bottom', fontsize=8, alpha=0.7)
    
    # Add annotation for Eöt-Wash range
    eotwash_chan = CONSTRAINT_CHANNELS["Fifth-force (Eöt-Wash)"]
    mid_freq = np.sqrt(eotwash_chan["freq_range"][0] * eotwash_chan["freq_range"][1])
    ax.annotate(
        f"Eöt-Wash digitized window (your CSV)\n"
        f"λ ≈ 29.9-0.93 (µm-mm)\n"
        f"f_eq ≈ {eotwash_chan['freq_range'][0]:.3e}-{eotwash_chan['freq_range'][1]:.3e} Hz\n"
        f"E_eq ≈ {HUNT_BAND['freq_range'][0]*H_PLANCK/EV_TO_JOULE:.3e}-{HUNT_BAND['freq_range'][1]*H_PLANCK/EV_TO_JOULE:.3e} eV\n"
        f"(f_eq = c/(2πλ); E = h f)",
        xy=(mid_freq, y_positions["Fifth-force (Eöt-Wash)"]),
        xytext=(mid_freq, y_positions["Fifth-force (Eöt-Wash)"] + 0.5),
        fontsize=9,
        ha='center',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
    )
    
    # Set y-axis labels
    ax.set_yticks(list(y_positions.values()))
    ax.set_yticklabels(list(y_positions.keys()))
    ax.set_ylim(-0.5, y_pos + 0.5)
    
    # Add grid
    ax.grid(True, alpha=0.3, linestyle=':')
    
    # Add legend
    ax.legend(loc='upper left', fontsize=9, framealpha=0.9)
    
    # Tight layout
    plt.tight_layout()
    
    # Save figures
    fig.savefig(output_png, dpi=300, bbox_inches='tight')
    fig.savefig(output_pdf, bbox_inches='tight')
    
    print(f"Frequency ladder figure saved:")
    print(f"  PNG: {output_png}")
    print(f"  PDF: {output_pdf}")
    
    plt.close()


def main():
    """Main entry point."""
    import argparse
    
    ap = argparse.ArgumentParser(
        description="Generate MQGT-SCF frequency ladder figure"
    )
    ap.add_argument(
        "--png",
        type=Path,
        default=Path("results/frequency_ladder.png"),
        help="Output PNG path"
    )
    ap.add_argument(
        "--pdf",
        type=Path,
        default=Path("results/frequency_ladder.pdf"),
        help="Output PDF path"
    )
    
    args = ap.parse_args()
    
    create_frequency_ladder_figure(
        output_png=args.png,
        output_pdf=args.pdf
    )


if __name__ == "__main__":
    main()

