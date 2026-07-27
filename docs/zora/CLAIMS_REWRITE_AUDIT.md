# Claims Rewrite Audit

## Purpose

This note records the first pass of grounded-claims cleanup for the
high-visibility MQGT-SCF documents.

## Rewritten

### `README.md`

Replaced direct overclaims that conflicted with the repository's own
scientific-contract documents, including:

- "We have completed the Theory of Everything"
- "fundamental breakthrough"
- "This is a historic moment in theoretical physics"

The README now aligns with the contract in
`docs/CLAIMS_LIMITS_AND_FALSIFIERS.md` by presenting MQGT-SCF as:

- a speculative EFT-style program
- a falsifiable constraint lab
- a public corpus for critique, reproduction, and experimental challenge

## Reviewed But Not Rewritten

### `docs/IMPLICATIONS_PUBLIC.md`

This file was already substantially aligned with the grounded posture:

- no discovery claim
- explicit "if validated" framing
- methodology-first tone
- safe public statement included

### `docs/publishing/public_statement.md`

This file was already conservative and release-safe. No change needed.

### `MAINLINE.md`

This file is more ambitious in tone than the public statement, but it does not
make the same direct completion/discovery claim as the README. Left unchanged
on this pass.

## Remaining Review Risk

These surfaces may still deserve a later pass if the goal is complete
message-discipline across the repo:

- release notes and release-ready summaries
- downstream AI/Zora framing outside the main scientific-contract documents
- any manuscript companions that imply proof, uniqueness, or validation
- any public summaries that drift from "constraint lab" into "closure achieved"

## Recommended Rule

When in doubt, default to this hierarchy:

1. `docs/CLAIMS_LIMITS_AND_FALSIFIERS.md`
2. `docs/REVIEWER_QUICKSTART.md`
3. `docs/IMPLICATIONS_PUBLIC.md`
4. everything else

If another document conflicts with those three, rewrite the other document.
