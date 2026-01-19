#!/usr/bin/env python3
"""Frequency-domain analysis for QRNG bitstreams.

Computes power spectral density, coherence, line noise detection,
and periodicity analysis for MQGT-SCF QRNG constraint channel.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from scipy import signal
from scipy.fft import fft, fftfreq


def compute_psd(
    bits: np.ndarray,
    sampling_rate: float = 1.0,
    nperseg: Optional[int] = None,
    **kwargs
) -> Tuple[np.ndarray, np.ndarray]:
    """Compute power spectral density using Welch's method.
    
    Args:
        bits: Bitstream array (0/1 values)
        sampling_rate: Sampling rate in Hz (default: 1.0)
        nperseg: Segment length for Welch's method (default: min(256, len(bits)//4))
        **kwargs: Additional arguments to scipy.signal.welch
    
    Returns:
        (frequencies, psd) where frequencies are in Hz and psd is in power/Hz
    """
    if len(bits) < 4:
        raise ValueError("Need at least 4 samples for PSD")
    
    # Convert bits to float for signal processing
    signal_data = bits.astype(float)
    
    # Default segment length
    if nperseg is None:
        nperseg = min(256, len(bits) // 4)
        nperseg = max(4, nperseg)  # At least 4 samples
    
    # Compute PSD using Welch's method
    frequencies, psd = signal.welch(
        signal_data,
        fs=sampling_rate,
        nperseg=nperseg,
        **kwargs
    )
    
    return frequencies, psd


def detect_line_noise(
    frequencies: np.ndarray,
    psd: np.ndarray,
    line_freqs: List[float] = [50.0, 60.0],
    harmonics: int = 5,
    threshold_db: float = 10.0,
) -> Dict[str, List[float]]:
    """Detect line noise peaks (50/60 Hz and harmonics).
    
    Args:
        frequencies: Frequency array from PSD
        psd: Power spectral density
        line_freqs: Base line frequencies to check (default: [50, 60] Hz)
        harmonics: Number of harmonics to check (default: 5)
        threshold_db: Threshold above background in dB (default: 10.0)
    
    Returns:
        Dictionary mapping frequency name to list of detected peak frequencies
    """
    # Convert PSD to dB
    psd_db = 10 * np.log10(psd + 1e-20)  # Add small offset to avoid log(0)
    
    # Estimate background (median)
    background_db = np.median(psd_db)
    
    detected = {}
    
    for base_freq in line_freqs:
        peaks = []
        for h in range(1, harmonics + 1):
            target_freq = base_freq * h
            
            # Find closest frequency bin
            idx = np.argmin(np.abs(frequencies - target_freq))
            actual_freq = frequencies[idx]
            
            # Check if peak is above threshold
            peak_power_db = psd_db[idx]
            if peak_power_db > background_db + threshold_db:
                peaks.append(actual_freq)
        
        if peaks:
            detected[f"{base_freq}_Hz"] = peaks
    
    return detected


def compute_coherence(
    bits1: np.ndarray,
    bits2: np.ndarray,
    sampling_rate: float = 1.0,
    nperseg: Optional[int] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """Compute coherence between two bitstreams.
    
    Args:
        bits1: First bitstream
        bits2: Second bitstream
        sampling_rate: Sampling rate in Hz
        nperseg: Segment length (default: auto)
    
    Returns:
        (frequencies, coherence) where coherence is 0-1
    """
    if len(bits1) != len(bits2):
        raise ValueError("Bitstreams must have same length")
    
    if len(bits1) < 4:
        raise ValueError("Need at least 4 samples")
    
    signal1 = bits1.astype(float)
    signal2 = bits2.astype(float)
    
    if nperseg is None:
        nperseg = min(256, len(bits1) // 4)
        nperseg = max(4, nperseg)
    
    frequencies, coherence = signal.coherence(
        signal1,
        signal2,
        fs=sampling_rate,
        nperseg=nperseg,
    )
    
    return frequencies, coherence


def detect_periodicity(
    bits: np.ndarray,
    sampling_rate: float = 1.0,
    min_period: float = 2.0,
    max_period: Optional[float] = None,
) -> Optional[float]:
    """Detect periodicities using autocorrelation.
    
    Args:
        bits: Bitstream array
        sampling_rate: Sampling rate in Hz
        min_period: Minimum period to detect (seconds)
        max_period: Maximum period to detect (seconds, default: len(bits)/sampling_rate/2)
    
    Returns:
        Dominant period in seconds, or None if none detected
    """
    if len(bits) < 4:
        return None
    
    signal_data = bits.astype(float)
    
    # Compute autocorrelation
    autocorr = np.correlate(signal_data, signal_data, mode='full')
    autocorr = autocorr[len(autocorr)//2:]
    
    # Normalize
    autocorr = autocorr / autocorr[0]
    
    # Find peaks (excluding zero lag)
    if max_period is None:
        max_period = len(bits) / sampling_rate / 2
    
    min_lag = int(min_period * sampling_rate)
    max_lag = int(max_period * sampling_rate)
    max_lag = min(max_lag, len(autocorr) - 1)
    
    if max_lag <= min_lag:
        return None
    
    # Find peak in range
    search_range = autocorr[min_lag:max_lag+1]
    peak_idx = np.argmax(search_range) + min_lag
    
    # Check if peak is significant (above threshold)
    threshold = 0.3  # Minimum correlation
    if autocorr[peak_idx] > threshold:
        period = peak_idx / sampling_rate
        return period
    
    return None


def analyze_frequency_domain(
    bits: np.ndarray,
    sampling_rate: float = 1.0,
    line_freqs: List[float] = [50.0, 60.0],
) -> Dict:
    """Complete frequency-domain analysis of QRNG bitstream.
    
    Args:
        bits: Bitstream array (0/1)
        sampling_rate: Sampling rate in Hz
        line_freqs: Line frequencies to check
    
    Returns:
        Dictionary with analysis results:
            - frequencies: PSD frequency array
            - psd: Power spectral density
            - line_noise: Detected line noise peaks
            - periodicity: Detected period (if any)
            - summary_stats: Summary statistics
    """
    results = {}
    
    # PSD
    frequencies, psd = compute_psd(bits, sampling_rate=sampling_rate)
    results["frequencies"] = frequencies
    results["psd"] = psd
    
    # Line noise detection
    line_noise = detect_line_noise(frequencies, psd, line_freqs=line_freqs)
    results["line_noise"] = line_noise
    
    # Periodicity
    periodicity = detect_periodicity(bits, sampling_rate=sampling_rate)
    results["periodicity"] = periodicity
    
    # Summary statistics
    results["summary_stats"] = {
        "total_samples": len(bits),
        "sampling_rate_hz": sampling_rate,
        "nyquist_freq_hz": sampling_rate / 2,
        "psd_peak_freq_hz": frequencies[np.argmax(psd)],
        "psd_peak_power": np.max(psd),
        "psd_mean_power": np.mean(psd),
        "line_noise_detected": len(line_noise) > 0,
        "periodicity_detected": periodicity is not None,
    }
    
    return results


def analyze_multi_source_coherence(
    bitstreams: Dict[str, np.ndarray],
    sampling_rate: float = 1.0,
) -> Dict[str, np.ndarray]:
    """Compute pairwise coherence between multiple QRNG sources.
    
    Args:
        bitstreams: Dictionary mapping source_id to bitstream array
        sampling_rate: Sampling rate in Hz
    
    Returns:
        Dictionary mapping (source1, source2) pairs to coherence arrays
    """
    coherence_results = {}
    source_ids = list(bitstreams.keys())
    
    for i, source1 in enumerate(source_ids):
        for source2 in source_ids[i+1:]:
            bits1 = bitstreams[source1]
            bits2 = bitstreams[source2]
            
            # Truncate to same length
            min_len = min(len(bits1), len(bits2))
            bits1_trunc = bits1[:min_len]
            bits2_trunc = bits2[:min_len]
            
            try:
                frequencies, coherence = compute_coherence(
                    bits1_trunc,
                    bits2_trunc,
                    sampling_rate=sampling_rate,
                )
                coherence_results[(source1, source2)] = {
                    "frequencies": frequencies,
                    "coherence": coherence,
                }
            except Exception as e:
                print(f"Warning: Failed to compute coherence for ({source1}, {source2}): {e}")
    
    return coherence_results

