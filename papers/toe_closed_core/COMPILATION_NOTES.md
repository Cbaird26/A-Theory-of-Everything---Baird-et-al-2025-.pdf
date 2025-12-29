# Compilation Notes

## Prerequisites

To compile this paper, you need a LaTeX distribution with `latexmk`:

```bash
# macOS
brew install latexmk

# Or install full TeX Live distribution
# macOS: brew install --cask mactex
# Linux: sudo apt-get install texlive-full
```

## Compilation

Once `latexmk` is installed:

```bash
cd papers/toe_closed_core
make clean
make
```

This will produce `main.pdf`.

## Alternative (without latexmk)

If you have `pdflatex` but not `latexmk`, you can compile manually:

```bash
cd papers/toe_closed_core
pdflatex main.tex
pdflatex main.tex  # Run twice for references
```

## Verification Checklist

After compilation, verify the PDF contains:

- [ ] Kernel derivation section (mediator → Yukawa kernel)
- [ ] GKLS theorem + proof environment renders correctly
- [ ] Constraints table renders (booktabs lines look clean)
- [ ] Predictions page is present
- [ ] No "??" references (if present, run compilation again)

## Troubleshooting

If you see LaTeX errors, check:
1. All required packages are installed (amsmath, amssymb, amsthm, booktabs, hyperref)
2. No missing figure files (currently none required)
3. Bibliography compiles (currently using manual thebibliography, not BibTeX)

