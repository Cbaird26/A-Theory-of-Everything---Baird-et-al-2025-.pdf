#!/usr/bin/env python3
"""
Generate interactive HTML frequency ladder visualization for MQGT-SCF.

Uses Plotly to create an interactive figure with zoom/pan, tooltips,
and toggleable constraint channels.
"""

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
except ImportError:
    print("Error: plotly is required for interactive visualization.")
    print("Install with: pip install plotly")
    import sys
    sys.exit(1)

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

# Constraint channels
CONSTRAINT_CHANNELS = {
    "Cosmology": {
        "freq_range": [2e-18, 2.2e-18],
        "color": "blue",
        "label": "Cosmology (Hubble-scale clock)",
        "lambda_range": "~Mpc scales",
        "description": "Cosmological expansion constraints",
    },
    "Fifth-force (Bennu)": {
        "freq_range": [2.4e-4, 2.4e-3],
        "color": "orange",
        "label": "Fifth-force (Bennu/OSIRIS-REx)",
        "lambda_range": "~0.13 to 1.3 AU",
        "description": "Asteroid tracking constraints on ultralight mediators",
    },
    "QRNG": {
        "freq_range": [1e3, 1e7],
        "color": "green",
        "label": "QRNG (device/DAQ bandwidth)",
        "lambda_range": "Device-dependent",
        "description": "Quantum random number generator constraints",
    },
    "Fifth-force (Eöt-Wash)": {
        "freq_range": [5.14e10, 1.59e12],
        "color": "orange",
        "label": "Fifth-force (Eöt-Wash λ → f_eq)",
        "lambda_range": "~30 μm to 0.93 mm",
        "description": "Torsion balance constraints on sub-mm fifth forces",
    },
    "Atomic Spectroscopy": {
        "freq_range": [2.4e15, 2.4e21],
        "color": "cyan",
        "label": "Atomic Spectroscopy (ETH Zurich)",
        "lambda_range": "Atomic scales (~10 eV to 10^7 eV)",
        "description": "Precision isotope shift measurements (~100 mHz precision)",
    },
    "Higgs": {
        "freq_range": [3e25, 3e25],
        "color": "red",
        "label": "Higgs / collider (energy↔frequency)",
        "lambda_range": "~125 GeV equivalent",
        "description": "Collider constraints on Higgs portal interactions",
    },
}

# Hunt band
HUNT_BAND = {
    "freq_range": [8.4e9, 9.0e11],
    "color": "purple",
    "label": "Hunt band (0.1 < r ≤ 1.0)",
    "description": "Near-detectable parameter space from detectability analysis",
}


def create_interactive_figure(output_path: Path = None):
    """Create interactive frequency ladder figure."""
    if output_path is None:
        output_path = Path("results/frequency_ladder_interactive.html")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    fig = go.Figure()
    
    # Add constraint channels as horizontal bars
    y_pos = 0
    y_positions = {}
    
    for channel_name, channel_info in CONSTRAINT_CHANNELS.items():
        y_positions[channel_name] = y_pos
        
        freq_min, freq_max = channel_info["freq_range"]
        freq_width = freq_max - freq_min
        
        # Create hover text
        hover_text = (
            f"<b>{channel_info['label']}</b><br>"
            f"Frequency range: {freq_min:.3e} to {freq_max:.3e} Hz<br>"
            f"λ range: {channel_info.get('lambda_range', 'N/A')}<br>"
            f"{channel_info.get('description', '')}"
        )
        
        fig.add_trace(go.Bar(
            x=[freq_width],
            y=[channel_name],
            base=[freq_min],
            orientation='h',
            marker=dict(color=channel_info["color"], opacity=0.7),
            name=channel_info["label"],
            hovertemplate=hover_text + "<extra></extra>",
            showlegend=True,
        ))
        
        y_pos += 1
    
    # Add hunt band overlay
    hunt_freq_min, hunt_freq_max = HUNT_BAND["freq_range"]
    hunt_width = hunt_freq_max - hunt_freq_min
    
    fig.add_trace(go.Bar(
        x=[hunt_width],
        y=["Fifth-force (Eöt-Wash)"],
        base=[hunt_freq_min],
        orientation='h',
        marker=dict(color=HUNT_BAND["color"], opacity=HUNT_BAND.get("alpha", 0.3)),
        name=HUNT_BAND["label"],
        hovertemplate=(
            f"<b>{HUNT_BAND['label']}</b><br>"
            f"Frequency range: {hunt_freq_min:.3e} to {hunt_freq_max:.3e} Hz<br>"
            f"{HUNT_BAND.get('description', '')}<extra></extra>"
        ),
        showlegend=True,
    ))
    
    # Add frequency landmarks as vertical lines
    for landmark_name, landmark_freq in FREQ_LANDMARKS.items():
        if 1e-20 <= landmark_freq <= 1e44:
            fig.add_vline(
                x=landmark_freq,
                line_dash="dash",
                line_color="lightblue",
                opacity=0.5,
                annotation_text=landmark_name,
                annotation_position="top",
            )
    
    # Update layout
    fig.update_layout(
        title=dict(
            text="MQGT-SCF: Constraint Channels on a Frequency Axis<br>"
                 "<sub>(translation layer, not evidence)</sub>",
            x=0.5,
            font=dict(size=16),
        ),
        xaxis=dict(
            type="log",
            range=[np.log10(1e-20), np.log10(1e44)],
            title="Frequency (Hz) on a log scale",
            showgrid=True,
            gridcolor="lightgray",
            gridwidth=1,
        ),
        yaxis=dict(
            title="",
            showgrid=False,
        ),
        height=600,
        hovermode='closest',
        legend=dict(
            x=1.02,
            y=1,
            xanchor="left",
            yanchor="top",
        ),
        margin=dict(r=200),
    )
    
    # Save as HTML
    fig.write_html(str(output_path))
    
    print(f"Interactive frequency ladder saved: {output_path}")
    print(f"  Open in browser to view with zoom/pan and tooltips")
    
    return fig


def main():
    """Main entry point."""
    import argparse
    
    ap = argparse.ArgumentParser(
        description="Generate interactive MQGT-SCF frequency ladder figure"
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=Path("results/frequency_ladder_interactive.html"),
        help="Output HTML path"
    )
    
    args = ap.parse_args()
    
    create_interactive_figure(output_path=args.output)


if __name__ == "__main__":
    main()

