#!/usr/bin/env python3
"""Create monotone envelope version of fifth-force constraint curve.

Applies running minimum to ensure alpha_max is non-increasing as lambda_m increases.
This is conservative and protects against digitization errors.
"""

import csv
import sys

def create_monotone_envelope(input_file, output_file):
    """Read CSV, apply monotone envelope, write cleaned version."""
    
    # Read data
    rows = []
    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                'lambda_m': float(row['lambda_m']),
                'alpha_max': float(row['alpha_max']),
                'source_id': row['source_id'],
                'ref': row['ref']
            })
    
    # Sort by lambda_m
    rows.sort(key=lambda x: x['lambda_m'])
    
    # Apply running minimum (from right to left, then reverse)
    # This ensures alpha_max is non-increasing as lambda increases
    current_min = float('inf')
    for i in range(len(rows) - 1, -1, -1):
        if rows[i]['alpha_max'] < current_min:
            current_min = rows[i]['alpha_max']
        else:
            rows[i]['alpha_max'] = current_min
    
    # Write output
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['lambda_m', 'alpha_max', 'source_id', 'ref'])
        writer.writeheader()
        for row in rows:
            writer.writerow({
                'lambda_m': f"{row['lambda_m']:.15e}",
                'alpha_max': f"{row['alpha_max']:.15e}",
                'source_id': row['source_id'],
                'ref': row['ref']
            })
    
    # Report changes
    print(f"✅ Created monotone envelope version: {output_file}")
    print(f"   Total points: {len(rows)}")
    print(f"   Lambda range: {rows[0]['lambda_m']:.6e} to {rows[-1]['lambda_m']:.6e} m")
    print(f"   Alpha_max range: {min(r['alpha_max'] for r in rows):.6e} to {max(r['alpha_max'] for r in rows):.6e}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: create_monotone_envelope.py <input.csv> <output.csv>")
        sys.exit(1)
    
    create_monotone_envelope(sys.argv[1], sys.argv[2])

