# ANU QRNG API Notes

## Current Status

The ANU QRNG API (https://qrng.anu.edu.au/API/jsonI.php) may have intermittent issues:
- SSL certificate expiration warnings (handled with `verify=False`)
- 500 Server Errors (may require retries)
- Rate limiting (use `--sleep` parameter to be polite)

## Alternative QRNG Sources

If ANU API is unavailable, consider:

1. **NIST Randomness Beacon** (public, verifiable)
   - API: https://beacon.nist.gov/rest/record/last
   - Provides cryptographically verifiable random data
   - More reliable but different format

2. **Hardware QRNG devices**
   - ID Quantique, Quantis, etc.
   - Requires physical hardware

3. **Other public QRNG APIs**
   - Various research institutions provide similar services
   - Check current availability

## Workaround: Use Smaller Batches

If ANU API is having issues, try:
- Smaller `--n-bits` values (e.g., 10,000 instead of 200,000)
- Longer `--sleep` delays (e.g., 1.0 second)
- Run during off-peak hours

## For Testing: Pseudorandom is Fine

For pipeline validation, pseudorandom data (like `local_random_200k.txt`) is perfectly acceptable. The pipeline correctly identifies it as null, which validates the instrument.

Real QRNG data is needed for actual experimental constraints, but pseudorandom is sufficient for:
- Validating the analysis pipeline
- Testing Bayes factor calculations
- Generating LaTeX snippets
- Confirming the instrument works correctly

