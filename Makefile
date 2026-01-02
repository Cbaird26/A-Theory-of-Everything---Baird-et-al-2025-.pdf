# MQGT-SCF Makefile
# One-command workflows for common tasks

.PHONY: help qrng-validate qrng-ingest qrng-calibrate qrng-mixed

help:
	@echo "MQGT-SCF Makefile Targets:"
	@echo ""
	@echo "QRNG Pipeline:"
	@echo "  make qrng-validate              - Run QRNG regression tests"
	@echo "  make qrng-ingest INPUT=...      - Validate and ingest QRNG CSV"
	@echo "  make qrng-calibrate FAIR=... BIASED=... - Run calibration on controls"
	@echo "  make qrng-mixed MIXED=...       - Run mixed dataset analysis"
	@echo ""
	@echo "Example:"
	@echo "  make qrng-ingest INPUT=data/raw/my_qrng.csv"

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

