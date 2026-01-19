#!/usr/bin/env python3
"""Generate publication-ready frequency-domain plots for QRNG analysis."""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import Dict, Optional

from .frequency_analysis import analyze_frequency_domain, analyze_multi_source_coherence


# Frequency landmarks for annotation
FREQ_LANDMARKS = {
    "Schumann (7.83 Hz)": 7.83,
    "Line noise (50 Hz)": 50.0,
    "Line noise (60 Hz)": 60.0,
    "Audio max (20 kHz)": 2e4,
}


def plot_psd(
    frequencies: np.ndarray,
    psd: np.ndarray,
    output_path: Path,
    title: str = "Power Spectral Density",
    line_noise: Optional[Dict] = None,
    sampling_rate: Optional[float] = None,
):
    """Plot power spectral density with annotations.
    
    Args:
        frequencies: Frequency array (Hz)
        psd: Power spectral density
        output_path: Path to save figure
        title: Plot title
        line_noise: Detected line noise peaks (from detect_line_noise)
        sampling_rate: Sampling rate for annotation
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot PSD (log-log)
    ax.loglog(frequencies, psd, 'b-', linewidth=1.5, label='PSD')
    
    # Annotate line noise
    if line_noise:
        for freq_name, peaks in line_noise.items():
            for peak_freq in peaks:
                # Find corresponding PSD value
                idx = np.argmin(np.abs(frequencies - peak_freq))
                peak_psd = psd[idx]
                ax.plot(peak_freq, peak_psd, 'ro', markersize=8, label=f'Line noise: {freq_name}')
                ax.annotate(
                    f'{freq_name}\n{peak_freq:.1f} Hz',
                    xy=(peak_freq, peak_psd),
                    xytext=(10, 10),
                    textcoords='offset points',
                    fontsize=9,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                )
    
    # Annotate frequency landmarks if in range
    for landmark_name, landmark_freq in FREQ_LANDMARKS.items():
        if frequencies[0] <= landmark_freq <= frequencies[-1]:
            idx = np.argmin(np.abs(frequencies - landmark_freq))
            landmark_psd = psd[idx]
            ax.axvline(landmark_freq, color='gray', linestyle='--', alpha=0.5, linewidth=1)
            ax.text(
                landmark_freq,
                psd.max() * 0.1,
                landmark_name,
                rotation=90,
                verticalalignment='bottom',
                fontsize=8,
                alpha=0.7,
            )
    
    ax.set_xlabel('Frequency (Hz)', fontsize=12)
    ax.set_ylabel('Power Spectral Density (power/Hz)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved PSD plot: {output_path}")


def plot_coherence(
    frequencies: np.ndarray,
    coherence: np.ndarray,
    output_path: Path,
    source1: str,
    source2: str,
    title: Optional[str] = None,
):
    """Plot coherence between two sources.
    
    Args:
        frequencies: Frequency array (Hz)
        coherence: Coherence array (0-1)
        output_path: Path to save figure
        source1: Name of first source
        source2: Name of second source
        title: Plot title (default: auto-generated)
    """
    if title is None:
        title = f"Coherence: {source1} vs {source2}"
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.semilogx(frequencies, coherence, 'b-', linewidth=1.5, label='Coherence')
    ax.axhline(0.5, color='r', linestyle='--', alpha=0.5, label='Threshold (0.5)')
    
    ax.set_xlabel('Frequency (Hz)', fontsize=12)
    ax.set_ylabel('Coherence', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_ylim([0, 1.1])
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved coherence plot: {output_path}")


def generate_frequency_analysis_report(
    bits: np.ndarray,
    output_dir: Path,
    source_id: str = "qrng",
    sampling_rate: float = 1.0,
):
    """Generate complete frequency-domain analysis report.
    
    Args:
        bits: Bitstream array
        output_dir: Directory to save plots and report
        source_id: Identifier for this source
        sampling_rate: Sampling rate in Hz
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Run analysis
    results = analyze_frequency_domain(bits, sampling_rate=sampling_rate)
    
    # Generate PSD plot
    psd_path = output_dir / f"{source_id}_psd.png"
    plot_psd(
        results["frequencies"],
        results["psd"],
        psd_path,
        title=f"Power Spectral Density: {source_id}",
        line_noise=results["line_noise"],
        sampling_rate=sampling_rate,
    )
    
    # Generate summary report
    report_path = output_dir / f"{source_id}_frequency_report.md"
    with report_path.open("w") as f:
        f.write(f"# Frequency-Domain Analysis: {source_id}\n\n")
        f.write("## Summary Statistics\n\n")
        stats = results["summary_stats"]
        for key, value in stats.items():
            f.write(f"- **{key}**: {value}\n")
        
        f.write("\n## Line Noise Detection\n\n")
        if results["line_noise"]:
            for freq_name, peaks in results["line_noise"].items():
                f.write(f"- **{freq_name}**: Detected at {peaks} Hz\n")
        else:
            f.write("- No significant line noise detected.\n")
        
        f.write("\n## Periodicity\n\n")
        if results["periodicity"]:
            f.write(f"- **Detected period**: {results['periodicity']:.3f} seconds\n")
            f.write(f"- **Frequency**: {1.0/results['periodicity']:.3f} Hz\n")
        else:
            f.write("- No significant periodicity detected.\n")
    
    print(f"Generated frequency analysis report: {report_path}")
    
    return results

