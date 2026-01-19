# QRNG Frequency-Domain Analysis

## Overview

Frequency-domain analysis provides a diagnostic lens for QRNG bitstreams, enabling detection of:
- Power spectral density (PSD) characteristics
- Line noise contamination (50/60 Hz, harmonics)
- Periodicities and correlations
- Multi-source coherence

This analysis is part of the MQGT-SCF QRNG constraint channel, where frequency becomes a **literal measurement** (not just a translation layer).

## Methodology

### Power Spectral Density (PSD)

Uses Welch's method to compute the power spectral density:

```python
from code.inference.qrng.frequency_analysis import compute_psd

frequencies, psd = compute_psd(bits, sampling_rate=1.0)
```

The PSD reveals:
- White noise characteristics (flat spectrum)
- Frequency-dependent biases
- Environmental contamination

### Line Noise Detection

Detects AC power line contamination (50/60 Hz and harmonics):

```python
from code.inference.qrng.frequency_analysis import detect_line_noise

line_noise = detect_line_noise(frequencies, psd, line_freqs=[50.0, 60.0])
```

This is critical for QRNG quality control, as line noise can introduce periodic biases that violate randomness assumptions.

### Periodicity Detection

Uses autocorrelation to detect periodic patterns:

```python
from code.inference.qrng.frequency_analysis import detect_periodicity

period = detect_periodicity(bits, sampling_rate=1.0)
```

### Multi-Source Coherence

Computes coherence between multiple QRNG sources:

```python
from code.inference.qrng.frequency_analysis import analyze_multi_source_coherence

coherence_results = analyze_multi_source_coherence(
    {"source1": bits1, "source2": bits2},
    sampling_rate=1.0
)
```

## Integration with MQGT-SCF

Frequency-domain analysis connects QRNG constraints to the broader MQGT-SCF framework:

- **QRNG bandwidth**: Typically Hz to GHz (device-dependent)
- **Line noise**: 50/60 Hz environmental contamination
- **MQGT-SCF prediction**: If scalar fields influence quantum measurements, frequency-domain structure may reveal subtle correlations

## Usage

### Command-Line

```bash
# Run QRNG analysis with frequency-domain diagnostics
python experiments/grok_qrng/analyze_qrng.py \
    --input data/raw/qrng/my_data.csv \
    --frequency-analysis
```

### Python API

```python
from code.inference.qrng.frequency_analysis import analyze_frequency_domain
from code.inference.qrng.visualize_frequency import generate_frequency_analysis_report

# Load bitstream
bits = load_bits("data/raw/qrng/my_data.csv")

# Run analysis
results = analyze_frequency_domain(bits, sampling_rate=1.0)

# Generate report and plots
generate_frequency_analysis_report(
    bits,
    output_dir=Path("results/qrng"),
    source_id="my_qrng",
    sampling_rate=1.0
)
```

## Output Files

- `{source_id}_psd.png`: Power spectral density plot (log-log scale)
- `{source_id}_frequency_report.md`: Summary report with statistics
- Coherence plots (for multi-source analysis)

## Interpretation

- **Flat PSD**: Indicates white noise (good for QRNG)
- **Line noise peaks**: Environmental contamination (requires mitigation)
- **Periodicities**: Systematic biases (violates randomness)
- **High coherence**: Correlated sources (may indicate shared environmental factors)

## References

- Welch's method: `scipy.signal.welch`
- Coherence: `scipy.signal.coherence`
- MQGT-SCF QRNG channel: See main ToE paper

