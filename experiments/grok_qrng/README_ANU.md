# ANU QRNG Downloader

## Rate Limit Warning

**ANU API limit: 1 request per minute**

For 200,000 bits, you need ~25 requests = **~25 minutes minimum**.

The script defaults to 65 seconds between requests to be safe.

## Quick Start

```bash
# For 200k bits (takes ~25-30 minutes due to rate limit)
./fetch_anu_qrng_bits.py --n-bits 200000 --out data/raw/anu_run_01/anu_bits.txt

# For smaller test (10k bits, ~10 requests = ~10 minutes)
./fetch_anu_qrng_bits.py --n-bits 10000 --out data/raw/anu_test/anu_bits.txt --sleep 65
```

## Alternative: Use Pseudorandom for Testing

For pipeline validation, pseudorandom data is perfectly fine:

```bash
python - <<'PY'
import numpy as np
n=200000
bits = np.random.randint(0,2,size=n, dtype=np.int8)
with open("data/raw/test_run/local_random_200k.txt","w") as f:
    f.write("".join(map(str,bits.tolist())))
print("Wrote data/raw/test_run/local_random_200k.txt")
PY

./quick_run.sh test_run
```

The pipeline correctly identifies pseudorandom as null (BF10 << 1), which validates the instrument.

## Status

- ✅ Script created and handles SSL/retry issues
- ⚠️  ANU API has 1 req/min rate limit (slow but works)
- ✅ Pseudorandom validation already complete (grok_run_01)

