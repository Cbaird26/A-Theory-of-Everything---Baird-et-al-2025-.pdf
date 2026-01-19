#!/usr/bin/env python3
"""Frequency Atlas: Conversion functions for physical scales to frequencies.

Converts timescales, energies, masses, and lengths to equivalent frequencies
using standard physics conversions. Includes landmark frequency ladder and
MQGT-SCF constraint channel mapping.

Key conversions:
- Timescale T → f = 1/T
- Energy E → f = E/h (Planck-Einstein)
- Mass m → f = mc²/h (Compton frequency)
- Length λ → f_eq ≈ c/(2πλ) (Yukawa range equivalent)

See docs/frequency_atlas.md for full documentation.
"""

import math

# Constants from CODATA 2018 (NIST)
H_PLANCK = 6.62607015e-34  # Planck constant (J·s), exact in SI
C_LIGHT = 299792458.0  # Speed of light (m/s), exact in SI
E_CHARGE = 1.602176634e-19  # Elementary charge (C), exact in SI
HBAR = H_PLANCK / (2 * math.pi)  # Reduced Planck constant

# Particle masses (CODATA 2018)
M_ELECTRON = 9.1093837015e-31  # Electron mass (kg)
M_PROTON = 1.67262192369e-27  # Proton mass (kg)

# Planck scale (via G_N = 6.67430e-11 m³/(kg·s²))
G_NEWTON = 6.67430e-11  # Newtonian constant of gravitation (m³/(kg·s²))
PLANCK_TIME = math.sqrt(HBAR * G_NEWTON / C_LIGHT**5)
PLANCK_FREQUENCY = 1.0 / PLANCK_TIME

# Higgs mass (125 GeV)
M_HIGGS_GEV = 125.0
M_HIGGS_J = M_HIGGS_GEV * 1e9 * E_CHARGE  # Convert GeV to joules via eV


def timescale_to_freq(T_seconds):
    """Convert timescale to frequency: f = 1/T.
    
    Args:
        T_seconds: Timescale in seconds
        
    Returns:
        Frequency in Hz
    """
    if T_seconds <= 0:
        raise ValueError("Timescale must be positive")
    return 1.0 / T_seconds


def energy_to_freq(E_joules):
    """Convert energy to frequency: f = E/h (Planck-Einstein).
    
    Args:
        E_joules: Energy in joules
        
    Returns:
        Frequency in Hz
    """
    return E_joules / H_PLANCK


def mass_to_freq(m_kg):
    """Convert mass to Compton frequency: f = mc²/h.
    
    Args:
        m_kg: Mass in kilograms
        
    Returns:
        Equivalent frequency in Hz (Compton frequency)
    """
    return (m_kg * C_LIGHT**2) / H_PLANCK


def length_to_freq_wave(lam_meters):
    """Convert wavelength to frequency: f = c/λ.
    
    Args:
        lam_meters: Wavelength in meters
        
    Returns:
        Frequency in Hz
    """
    if lam_meters <= 0:
        raise ValueError("Wavelength must be positive")
    return C_LIGHT / lam_meters


def length_to_freq_yukawa(lam_meters):
    """Convert Yukawa range to equivalent frequency: f_eq ≈ c/(2πλ).
    
    For short-range forces (Yukawa-type), this maps range to equivalent
    mediator energy scale, then to frequency via E = hf.
    
    Args:
        lam_meters: Interaction range in meters
        
    Returns:
        Equivalent frequency in Hz
        
    Note:
        This is a conceptual mapping, not a literal oscillation.
        The lab apparatus may be mechanically low-Hz, but it probes
        short ranges that correspond to high-energy mediator scales.
    """
    if lam_meters <= 0:
        raise ValueError("Range must be positive")
    return C_LIGHT / (2 * math.pi * lam_meters)


def eV_to_freq(E_eV):
    """Convert energy in eV to frequency: f = (E × e)/h.
    
    Args:
        E_eV: Energy in electron-volts
        
    Returns:
        Frequency in Hz
    """
    return energy_to_freq(E_eV * E_CHARGE)


def GeV_to_freq(E_GeV):
    """Convert energy in GeV to frequency: f = (E × 10⁹ × e)/h.
    
    Args:
        E_GeV: Energy in giga-electron-volts
        
    Returns:
        Frequency in Hz
    """
    return eV_to_freq(E_GeV * 1e9)


def build_frequency_ladder():
    """Build landmark frequency ladder from cosmic to Planck scales.
    
    Returns:
        List of dicts with keys: freq, label, category, description
    """
    landmarks = []
    
    # 0 Hz (DC/static)
    landmarks.append({
        'freq': 0.0,
        'label': '0 Hz (DC/static)',
        'category': 'static',
        'description': 'Steady fields and equilibria'
    })
    
    # Cosmic expansion (Hubble rate)
    HUBBLE_RATE_HZ = 2.18e-18  # Approximate, via H₀ ≈ 67.4 km/s/Mpc
    landmarks.append({
        'freq': HUBBLE_RATE_HZ,
        'label': '~2×10⁻¹⁸ Hz (Hubble rate)',
        'category': 'cosmology',
        'description': 'Cosmic expansion timescale'
    })
    
    # Nanohertz gravitational waves
    landmarks.append({
        'freq': 1e-9,
        'label': '~10⁻⁹ Hz (nanohertz GW)',
        'category': 'gravity',
        'description': 'Pulsar Timing Array band'
    })
    
    # 1/year
    ONE_YEAR_HZ = timescale_to_freq(365.25 * 24 * 3600)
    landmarks.append({
        'freq': ONE_YEAR_HZ,
        'label': f'{ONE_YEAR_HZ:.2e} Hz (1/year)',
        'category': 'geophysics',
        'description': 'Annual cycles'
    })
    
    # 1/day
    ONE_DAY_HZ = timescale_to_freq(24 * 3600)
    landmarks.append({
        'freq': ONE_DAY_HZ,
        'label': f'{ONE_DAY_HZ:.2e} Hz (1/day)',
        'category': 'geophysics',
        'description': 'Daily cycles'
    })
    
    # Schumann resonance
    landmarks.append({
        'freq': 7.83,
        'label': '7.83 Hz (Schumann)',
        'category': 'geophysics',
        'description': 'Earth-ionosphere cavity resonance'
    })
    
    # Human hearing
    landmarks.append({
        'freq': 20,
        'label': '20 Hz - 20 kHz (hearing)',
        'category': 'sensory',
        'description': 'Human audible range'
    })
    
    # Hydrogen 21-cm line
    F_21CM = length_to_freq_wave(0.21)
    landmarks.append({
        'freq': F_21CM,
        'label': f'{F_21CM:.6e} Hz (H 21-cm)',
        'category': 'astronomy',
        'description': 'Neutral hydrogen hyperfine transition'
    })
    
    # Cesium transition (SI second)
    F_CESIUM = 9192631770
    landmarks.append({
        'freq': F_CESIUM,
        'label': f'{F_CESIUM:.0f} Hz (Cs-133)',
        'category': 'metrology',
        'description': 'SI second definition'
    })
    
    # CMB peak
    CMB_PEAK_HZ = 160.2e9
    landmarks.append({
        'freq': CMB_PEAK_HZ,
        'label': f'{CMB_PEAK_HZ:.1e} Hz (CMB peak)',
        'category': 'cosmology',
        'description': 'Cosmic microwave background peak'
    })
    
    # Fifth-force equivalent (from Eöt-Wash range)
    # λ ~ 30 μm to 0.93 mm → f_eq ~ 5×10¹⁰ to 1.6×10¹² Hz
    FIFTH_FORCE_MIN = length_to_freq_yukawa(9.29e-4)  # 0.93 mm
    FIFTH_FORCE_MAX = length_to_freq_yukawa(3.00e-5)  # 30 μm
    landmarks.append({
        'freq': (FIFTH_FORCE_MIN + FIFTH_FORCE_MAX) / 2,
        'label': f'{FIFTH_FORCE_MIN:.1e} - {FIFTH_FORCE_MAX:.1e} Hz (fifth-force equiv)',
        'category': 'fifth_force',
        'description': 'Eöt-Wash hunt band equivalent frequency (sub-mm lab)'
    })
    
    # Bennu/OSIRIS-REx solar-system constraints
    # m ~ 10^-18 to 10^-17 eV → λ ~ 0.13 to 1.3 AU → f_eq ~ 2.4×10^-4 to 2.4×10^-3 Hz
    AU_METERS = 1.496e11  # 1 AU in meters
    BENNU_LAM_MIN = 0.13 * AU_METERS  # ~0.13 AU
    BENNU_LAM_MAX = 1.3 * AU_METERS   # ~1.3 AU
    BENNU_FEQ_MIN = length_to_freq_yukawa(BENNU_LAM_MAX)
    BENNU_FEQ_MAX = length_to_freq_yukawa(BENNU_LAM_MIN)
    landmarks.append({
        'freq': (BENNU_FEQ_MIN + BENNU_FEQ_MAX) / 2,
        'label': f'{BENNU_FEQ_MIN:.2e} - {BENNU_FEQ_MAX:.2e} Hz (Bennu equiv)',
        'category': 'fifth_force',
        'description': 'Bennu/OSIRIS-REx solar-system constraints (ultra-long range)'
    })
    
    # Visible light
    F_VISIBLE_MIN = 4.3e14
    F_VISIBLE_MAX = 7.5e14
    landmarks.append({
        'freq': (F_VISIBLE_MIN + F_VISIBLE_MAX) / 2,
        'label': f'{F_VISIBLE_MIN:.1e} - {F_VISIBLE_MAX:.1e} Hz (visible)',
        'category': 'electromagnetic',
        'description': 'Human vision range'
    })
    
    # Electron Compton frequency
    F_ELECTRON = mass_to_freq(M_ELECTRON)
    landmarks.append({
        'freq': F_ELECTRON,
        'label': f'{F_ELECTRON:.3e} Hz (electron Compton)',
        'category': 'quantum',
        'description': 'Electron rest energy'
    })
    
    # Proton Compton frequency
    F_PROTON = mass_to_freq(M_PROTON)
    landmarks.append({
        'freq': F_PROTON,
        'label': f'{F_PROTON:.3e} Hz (proton Compton)',
        'category': 'quantum',
        'description': 'Proton rest energy'
    })
    
    # Higgs frequency
    F_HIGGS = GeV_to_freq(M_HIGGS_GEV)
    landmarks.append({
        'freq': F_HIGGS,
        'label': f'{F_HIGGS:.2e} Hz (Higgs)',
        'category': 'particle_physics',
        'description': 'Higgs mass scale (~125 GeV)'
    })
    
    # Planck frequency
    landmarks.append({
        'freq': PLANCK_FREQUENCY,
        'label': f'{PLANCK_FREQUENCY:.2e} Hz (Planck)',
        'category': 'quantum_gravity',
        'description': 'Planck time inverse'
    })
    
    return landmarks


def print_frequency_table():
    """Print formatted frequency ladder table."""
    landmarks = build_frequency_ladder()
    
    print("\n" + "="*80)
    print("MQGT-SCF FREQUENCY LADDER")
    print("="*80)
    print(f"{'Frequency (Hz)':<20} {'Category':<20} {'Description'}")
    print("-"*80)
    
    for lm in landmarks:
        if lm['freq'] == 0:
            freq_str = "0 (DC)"
        else:
            freq_str = f"{lm['freq']:.3e}"
        print(f"{freq_str:<20} {lm['category']:<20} {lm['description']}")
    
    print("\n" + "="*80)
    print("MQGT-SCF CONSTRAINT CHANNELS")
    print("="*80)
    print(f"{'Channel':<25} {'Frequency Range':<30} {'Description'}")
    print("-"*80)
    print(f"{'Cosmology':<25} {'~10⁻¹⁸ Hz':<30} {'Hubble rate scale'}")
    print(f"{'Fifth-Force':<25} {'~5×10¹⁰–1.6×10¹² Hz':<30} {'Eöt-Wash hunt band (equiv)'}")
    print(f"{'QRNG':<25} {'Hz→GHz':<30} {'Device bandwidths'}")
    print(f"{'Higgs':<25} {'~3×10²⁵ Hz':<30} {'Higgs mass scale (~125 GeV)'}")
    print(f"{'Gravitational Waves':<25} {'10⁻⁴–1 Hz (LISA)':<30} {'Space-based GW band'}")
    print(f"{'Gravitational Waves':<25} {'20 Hz–5 kHz (LIGO)':<30} {'Ground-based GW band'}")
    
    print("\n" + "="*80)
    print(f"SPAN: ~43 orders of magnitude")
    print(f"From: {2.18e-18:.1e} Hz (cosmic expansion) → {PLANCK_FREQUENCY:.1e} Hz (Planck)")
    print("="*80 + "\n")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'table':
            print_frequency_table()
        elif command == 'convert':
            if len(sys.argv) < 4:
                print("Usage: frequency_atlas.py convert <type> <value> [unit]")
                print("  Types: timescale, energy, mass, wavelength, range, eV, GeV")
                sys.exit(1)
            
            conv_type = sys.argv[2]
            value = float(sys.argv[3])
            unit = sys.argv[4] if len(sys.argv) > 4 else None
            
            if conv_type == 'timescale':
                result = timescale_to_freq(value)
                print(f"{value} s → {result:.6e} Hz")
            elif conv_type == 'energy':
                result = energy_to_freq(value)
                print(f"{value} J → {result:.6e} Hz")
            elif conv_type == 'mass':
                result = mass_to_freq(value)
                print(f"{value} kg → {result:.6e} Hz")
            elif conv_type == 'wavelength':
                result = length_to_freq_wave(value)
                print(f"{value} m → {result:.6e} Hz")
            elif conv_type == 'range':
                result = length_to_freq_yukawa(value)
                print(f"{value} m → {result:.6e} Hz (Yukawa equiv)")
            elif conv_type == 'eV':
                result = eV_to_freq(value)
                print(f"{value} eV → {result:.6e} Hz")
            elif conv_type == 'GeV':
                result = GeV_to_freq(value)
                print(f"{value} GeV → {result:.6e} Hz")
            else:
                print(f"Unknown conversion type: {conv_type}")
                sys.exit(1)
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)
    else:
        print_frequency_table()
        
        print("\nExample conversions:")
        print(f"  1 year → {timescale_to_freq(365.25*24*3600):.3e} Hz")
        print(f"  1 eV → {eV_to_freq(1.0):.3e} Hz")
        print(f"  Electron mass → {mass_to_freq(M_ELECTRON):.3e} Hz")
        print(f"  1 meter wavelength → {length_to_freq_wave(1.0):.3e} Hz")
        print(f"  Eöt-Wash range (0.93 mm) → {length_to_freq_yukawa(9.29e-4):.3e} Hz (equiv)")

