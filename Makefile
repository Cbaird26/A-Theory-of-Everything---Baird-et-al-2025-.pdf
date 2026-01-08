# MQGT-SCF Makefile
# One-command workflows for common tasks

.PHONY: help qrng-validate qrng-ingest qrng-calibrate qrng-mixed qrng-multisource-validate qrng-multisource-report qrng-dominance-with-multisource fifth-validate fifth-ingest fifth-report fifth-detectability fifth-fetch-zenodo5080965

help:
	@echo "MQGT-SCF Makefile Targets:"
	@echo ""
	@echo "QRNG Pipeline:"
	@echo "  make qrng-validate              - Run QRNG regression tests"
	@echo "  make qrng-ingest INPUT=...      - Validate and ingest QRNG CSV"
	@echo "  make qrng-calibrate FAIR=... BIASED=... - Run calibration on controls"
	@echo "  make qrng-mixed MIXED=...       - Run mixed dataset analysis"
	@echo "  make qrng-multisource-validate - Run multi-source QRNG tests"
	@echo "  make qrng-multisource-report   - Ingest sources + compute pooled epsilon_max"
	@echo "  make qrng-dominance-with-multisource - Re-run dominance using pooled epsilon_max"
	@echo "  make qrng-fetch-nist           - Fetch and cache NIST Beacon v2.0 data"
	@echo ""
	@echo "Fifth-Force Pipeline:"
	@echo "  make fifth-validate             - Run fifth-force regression tests"
	@echo "  make fifth-ingest INPUT=...     - Validate and ingest constraint CSV"
	@echo "  make fifth-report               - Run full fifth-force analysis pipeline"
	@echo "  make fifth-detectability        - Compute detectability map (r = alpha_pred/alpha_max)"
	@echo "  make fifth-fetch-zenodo5080965  - Fetch and ingest Zenodo 5080965 Fig3 curve"
	@echo ""
	@echo "Examples:"
	@echo "  make qrng-ingest INPUT=data/raw/my_qrng.csv"
	@echo "  make fifth-ingest INPUT=data/raw/fifth_force/my_constraint.csv"

# QRNG Pipeline Targets

qrng-validate:
	@echo "Running QRNG regression tests..."
	python -m pytest -q tests/test_qrng_controls_regression.py tests/test_qrng_ingest_contract.py

qrng-ingest:
	@if [ -z "$(INPUT)" ]; then \
		echo "Error: INPUT required. Usage: make qrng-ingest INPUT=data/raw/file.csv"; \
		exit 1; \
	fi
	@echo "Ingesting QRNG data: $(INPUT)"
	python -m code.inference.qrng_ingest $(INPUT)

qrng-calibrate:
	@if [ -z "$(FAIR)" ] || [ -z "$(BIASED)" ]; then \
		echo "Error: FAIR and BIASED required."; \
		echo "Usage: make qrng-calibrate FAIR=CONTROL_random_200k.csv BIASED=CONTROL_bias_p505_200k.csv"; \
		exit 1; \
	fi
	@echo "Running QRNG calibration..."
	cd experiments/constraints/scripts && python calibrate_qrng_physics.py --fair $(FAIR) --biased $(BIASED) --priors 0.5,1.0,2.0

qrng-mixed:
	@if [ -z "$(MIXED)" ]; then \
		echo "Error: MIXED required. Usage: make qrng-mixed MIXED=file1.csv,file2.csv"; \
		exit 1; \
	fi
	@echo "Running mixed dataset analysis..."
	cd experiments/constraints/scripts && python calibrate_qrng_physics.py --mixed $(MIXED)

# Multi-Source QRNG Pipeline Targets

qrng-multisource-validate:
	@echo "Running multi-source QRNG regression tests..."
	python -m pytest -q tests/test_qrng_multisource.py

qrng-multisource-report:
	@echo "Running multi-source QRNG calibration pipeline..."
	@echo "1. Ingesting sources from data/raw/qrng_sources/..."
	python -m code.inference.qrng_multisource_ingest \
		--raw-dir data/raw/qrng_sources \
		--processed-dir data/processed \
		--results-dir results/qrng
	@echo "2. Computing pooled epsilon_max (both modes)..."
	python -m code.inference.qrng_pooled_epsilon \
		--processed-dir data/processed \
		--results-dir results/qrng \
		--compute-both-modes
	@echo "3. Multi-source report complete."
	@echo "   Summary: results/qrng/multisource_epsilon_summary.md"
	@echo "   Pooled epsilon_max: results/qrng/multisource_epsilon_max.json"

qrng-dominance-with-multisource:
	@echo "Re-running dominance analysis with pooled epsilon_max..."
	@if [ ! -f "results/qrng/multisource_epsilon_max.json" ]; then \
		echo "Error: Pooled epsilon_max not found. Run 'make qrng-multisource-report' first."; \
		exit 1; \
	fi
	@echo "Using pooled epsilon_max from results/qrng/multisource_epsilon_max.json"
	@echo "Note: Update your dominance scan script to use --epsilon-max=None to auto-load pooled value"
	@echo "Or manually pass the value from the JSON file."

qrng-fetch-nist:
	@echo "Fetching NIST Beacon v2.0 data..."
	python scripts/fetch_nist_beacon_v2_cache.py --pulses 400 --out data/raw/qrng_sources/nist_beacon_v2_last400.csv

# Fifth-Force Pipeline Targets

fifth-validate:
	@echo "Running fifth-force regression tests..."
	python -m pytest -q tests/test_fifth_force_contract.py tests/test_fifth_force_constraints_regression.py tests/test_fifth_force_detectability.py

fifth-ingest:
	@if [ -z "$(INPUT)" ]; then \
		echo "Error: INPUT required. Usage: make fifth-ingest INPUT=data/raw/fifth_force/file.csv"; \
		exit 1; \
	fi
	@echo "Ingesting fifth-force constraint data: $(INPUT)"
	python -m code.inference.fifth_force.ingest $(INPUT)

fifth-report:
	@echo "Running full fifth-force analysis pipeline..."
	@echo "1. Validating tests..."
	@$(MAKE) fifth-validate
	@echo "2. Analysis complete. See results/fifth_force/ for outputs."
	@echo "   Summary: docs/fifth_force_summary.md"

fifth-detectability:
	@echo "Computing fifth-force detectability map..."
	@if [ -z "$(SEED)" ]; then SEED=42; fi
	@if [ -z "$(NPTS)" ]; then NPTS=1000; fi
	python -m code.inference.fifth_force.detectability --seed $(SEED) --n-points $(NPTS)
	@echo "Detectability summary: results/fifth_force/detectability_summary.md"
	@echo "  (seed=$(SEED), n_points=$(NPTS))"

fifth-fetch-zenodo5080965:
	@echo "Fetching Zenodo 5080965 Fig3 curve..."
	python -m code.inference.fifth_force.importers.zenodo5080965_fig3
	@echo "✅ Zenodo curve ingested. Validated CSV: data/processed/zenodo5080965_fig3_validated.csv"

