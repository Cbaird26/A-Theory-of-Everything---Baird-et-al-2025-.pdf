#!/usr/bin/env python3
"""
Format WebPlotDigitizer output CSV into fifth-force contract schema.

Takes a 2-column CSV (lambda_m, alpha_max) and adds:
- Header row
- source_id column
- ref column
"""

import csv
import sys
from pathlib import Path

def format_digitized_csv(input_path, output_path, source_id="eotwash_prl2016_digitized", ref="PRL 116, 131102 (2016) - Eöt-Wash Group"):
    """
    Format 2-column CSV to 4-column contract format.
    
    Args:
        input_path: Path to input CSV (2 columns, no headers)
        output_path: Path to output CSV (4 columns with headers)
        source_id: Value for source_id column
        ref: Value for ref column
    """
    rows_formatted = []
    
    # Add header row
    rows_formatted.append(["lambda_m", "alpha_max", "source_id", "ref"])
    
    # Read input CSV and format rows
    with open(input_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            # Skip blank lines
            if not row or all(not cell.strip() for cell in row):
                continue
            
            # Should have 2 columns (lambda_m, alpha_max)
            if len(row) == 2:
                lambda_m = row[0].strip()
                alpha_max = row[1].strip()
                
                # Add source_id and ref columns
                rows_formatted.append([lambda_m, alpha_max, source_id, ref])
            else:
                print(f"Warning: Skipping malformed row: {row}", file=sys.stderr)
    
    # Write formatted CSV
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows_formatted)
    
    print(f"✓ Formatted CSV: {len(rows_formatted)-1} data rows")
    print(f"  Input:  {input_path}")
    print(f"  Output: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: format_digitized_csv.py <input_csv> [output_csv]")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    
    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2])
    else:
        # Default: same location, same filename
        output_path = input_path
    
    format_digitized_csv(input_path, output_path)

