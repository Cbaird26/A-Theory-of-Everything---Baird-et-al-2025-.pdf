"""Unit tests for frequency conversion functions in detectability module."""

import pytest
import numpy as np
import math

from code.inference.fifth_force.detectability import (
    lambda_to_freq_eq,
    freq_to_energy_eV,
    C_LIGHT,
    H_PLANCK,
    E_CHARGE,
)


def test_lambda_to_freq_eq_basic():
    """Test basic lambda to frequency conversion."""
    # Test case: λ = 1e-3 m (1 mm)
    lambda_m = 1e-3
    f_eq = lambda_to_freq_eq(lambda_m)
    
    # Expected: f_eq = c/(2πλ) = 299792458 / (2π × 1e-3) ≈ 4.77×10^10 Hz
    expected = C_LIGHT / (2 * math.pi * lambda_m)
    assert abs(f_eq - expected) < 1e-3
    
    # Should be approximately 4.77×10^10 Hz
    assert 4.76e10 < f_eq < 4.78e10


def test_lambda_to_freq_eq_eotwash_ranges():
    """Test Eöt-Wash specific ranges."""
    # Eöt-Wash: 30 μm to 0.93 mm
    # At λ = 9.29×10^-4 m (0.93 mm): f_eq ≈ 5.14×10^10 Hz
    lambda_m = 9.29e-4
    f_eq = lambda_to_freq_eq(lambda_m)
    expected = C_LIGHT / (2 * math.pi * lambda_m)
    assert abs(f_eq - expected) < 1e6  # Allow for numerical precision
    assert 5.13e10 < f_eq < 5.15e10
    
    # At λ = 3.00×10^-5 m (30 μm): f_eq ≈ 1.59×10^12 Hz
    lambda_m = 3.00e-5
    f_eq = lambda_to_freq_eq(lambda_m)
    expected = C_LIGHT / (2 * math.pi * lambda_m)
    assert abs(f_eq - expected) < 1e8  # Allow for numerical precision
    assert 1.58e12 < f_eq < 1.60e12


def test_lambda_to_freq_eq_edge_cases():
    """Test edge cases for lambda_to_freq_eq."""
    # Zero or negative lambda should return NaN
    assert np.isnan(lambda_to_freq_eq(0.0))
    assert np.isnan(lambda_to_freq_eq(-1.0))
    
    # Very large lambda should return very small frequency
    large_lambda = 1e10  # 10 million km
    f_eq = lambda_to_freq_eq(large_lambda)
    assert f_eq > 0
    assert f_eq < 1.0  # Should be very small
    
    # Very small lambda should return very large frequency
    small_lambda = 1e-10  # 0.1 nm
    f_eq = lambda_to_freq_eq(small_lambda)
    assert f_eq > 1e17  # Should be very large


def test_freq_to_energy_eV_basic():
    """Test basic frequency to energy conversion."""
    # Test case: f = 1×10^10 Hz
    freq_hz = 1e10
    E_eV = freq_to_energy_eV(freq_hz)
    
    # Expected: E = hf/e = (6.62607015e-34 × 1e10) / 1.602176634e-19
    expected = (H_PLANCK * freq_hz) / E_CHARGE
    assert abs(E_eV - expected) < 1e-15
    
    # Should be approximately 4.14×10^-5 eV
    assert 4.13e-5 < E_eV < 4.15e-5


def test_freq_to_energy_eV_eotwash_ranges():
    """Test Eöt-Wash frequency range energy conversions."""
    # At f_eq = 5.14×10^10 Hz: E ≈ 2.12×10^-4 eV
    freq_hz = 5.14e10
    E_eV = freq_to_energy_eV(freq_hz)
    # Should be approximately 2.12×10^-4 eV
    assert 2.11e-4 < E_eV < 2.13e-4
    
    # At f_eq = 1.59×10^12 Hz: E ≈ 6.59×10^-3 eV
    freq_hz = 1.59e12
    E_eV = freq_to_energy_eV(freq_hz)
    # Should be approximately 6.59×10^-3 eV
    assert 6.58e-3 < E_eV < 6.60e-3


def test_freq_to_energy_eV_edge_cases():
    """Test edge cases for freq_to_energy_eV."""
    # Zero frequency should return zero energy
    assert freq_to_energy_eV(0.0) == 0.0
    
    # Very large frequency should return large energy
    large_freq = 1e20
    E_eV = freq_to_energy_eV(large_freq)
    assert E_eV > 1000  # Should be many eV


def test_conversion_roundtrip():
    """Test that conversions are mathematically consistent."""
    # Test roundtrip: lambda → freq → energy, verify consistency
    
    # Start with a lambda value
    lambda_m = 1e-4  # 0.1 mm
    
    # Convert to frequency
    f_eq = lambda_to_freq_eq(lambda_m)
    
    # Convert frequency to energy
    E_eV = freq_to_energy_eV(f_eq)
    
    # Verify: E should equal hc/(2πλe)
    expected_E = (H_PLANCK * C_LIGHT) / (2 * math.pi * lambda_m * E_CHARGE)
    assert abs(E_eV - expected_E) < 1e-15


def test_conversion_constants():
    """Test that constants are correct (CODATA 2018 values)."""
    # Speed of light
    assert abs(C_LIGHT - 299792458.0) < 1e-9
    
    # Planck constant
    assert abs(H_PLANCK - 6.62607015e-34) < 1e-43
    
    # Elementary charge
    assert abs(E_CHARGE - 1.602176634e-19) < 1e-28

