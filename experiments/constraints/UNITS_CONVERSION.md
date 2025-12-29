# Units Conversion Reference

**Critical: Kapner plot may show x-axis in mm, but CSV must be in meters.**

## Conversion Factors

| Plot Units | Multiply By | Result (meters) |
|------------|-------------|-----------------|
| mm (millimeters) | 1e-3 | m |
| cm (centimeters) | 1e-2 | m |
| μm (micrometers) | 1e-6 | m |
| nm (nanometers) | 1e-9 | m |

## Examples

- Plot shows: 1 mm → CSV: 0.001 m (1e-3 m)
- Plot shows: 10 μm → CSV: 0.00001 m (1e-5 m)
- Plot shows: 0.1 mm → CSV: 0.0001 m (1e-4 m)

## Quick Check

After digitization, verify:
- Lambda values should be **~1e-6 to ~1e0 meters** for EP tests
- If your values are 1000x smaller, you forgot to convert mm → m
- If your values are 1000x larger, you converted wrong direction

## In WebPlotDigitizer

**Option 1:** Calibrate using meters directly
- Set calibration points to meter values (e.g., 1e-3 m, 1e-2 m)

**Option 2:** Export in plot units, then convert
- Export with mm values
- Multiply entire lambda column by 1e-3 in Excel/Python
- Then set excluded=1

**Recommended:** Option 1 (calibrate in meters) to avoid conversion errors.

