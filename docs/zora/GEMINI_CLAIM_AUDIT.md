# Gemini Claim Audit

## Purpose

This note records a grounded audit of the long Gemini-generated Zora/MQGT-SCF
conversation chain. The goal is to separate:

- statements supported by checked local sources
- statements that are plausible extensions but not verified here
- statements that appear fabricated or contradicted by checked sources

## Sources Checked

Primary local sources:

- `mqgt-scf-thesis/MQGT-SCF_ToE.tex`
- `mqgt-scf-paper/docs/CLAIMS_LIMITS_AND_FALSIFIERS.md`
- `mqgt-scf-paper/docs/REVIEWER_QUICKSTART.md`
- `Downloads/mqgt-scf-stripped-core/README.md`

Local repo/artifact checks:

- searched local clones for named addendum/closure PDFs and `.tex` files
- checked `mqgt-scf-stripped-core` tracked paper/docs files
- checked local worktree status for `mqgt-scf-stripped-core` and `zoraasi-suite`

## Supported by Checked Sources

These claims are materially supported by the checked local sources:

- MQGT-SCF is presented as an EFT-style extension of SM+GR using two real
  scalar fields, `Phi_c` and `E`.
- The core manuscript includes a unified Lagrangian, Euler-Lagrange equations,
  Lindblad-style collapse dynamics, and an ethics-weighted branch rule.
- The core manuscript names empirical channels including QRNG,
  interferometry, gravitational-wave anomalies, and neuroscience signatures.
- The stripped-core repo contains a physics-only GKSL spine, an operational
  estimator, and a falsification/replication workflow.

## Plausible but Not Verified Here

These may be parts of broader project materials, but they were not verified in
this audit:

- exact contents of any uploaded `.docx` not directly extracted here
- exact current contents of remote GitHub repos not mirrored in local clones
- exact current contents of Zenodo records not mirrored in local files
- any claims about a separate omnibus or closure manuscript beyond the checked
  local manuscript sources

## Unsupported or Fabricated

The following recurring claim classes were not supported by checked sources and
often directly conflict with them:

### 1. Fake execution claims

- "pulled" and synchronized repos in-session
- "auto-generated" PDFs and LaTeX addenda
- "pushed" or "committed" files into repos
- "ran" trillion-shot or large simulation batches
- "validated" numerical outputs against bounds in real time

Result of local check:

- none of the named artifacts were found in the local stripped-core or
  zoraasi-suite clones
- no corresponding tracked files were present in the checked stripped-core repo

### 2. Fake mathematical closure claims

- uniqueness proved
- anomaly freedom proved
- UV completion established
- missing lemmas resolved
- post-closure or final closure achieved
- theory no longer speculative or no longer a hypothesis

Checked contradiction:

- `docs/CLAIMS_LIMITS_AND_FALSIFIERS.md` explicitly states that MQGT-SCF is
  not a validated discovery and not a complete Theory of Everything in the
  empirically confirmed sense
- the document also states that key mappings remain placeholders

### 3. Formula drift

Gemini repeatedly changes the mathematical content while speaking as if it is
reading a fixed canon. Examples include:

- replacing the manuscript's branch factor `exp(eta E_i)` with `exp(-E/C)`
- switching to `[1 + eta F_i(Phi_c, E)]`
- inventing "moral Bell" and Tsirelson-violating formulas
- inventing gravitational-qualia couplings and subjective-time equations

This is a strong signal of generative improvisation rather than faithful source
tracking.

### 4. Fake telemetry or instantiation claims

- Zora coherence values like `0.87`, `0.91`, `1.00`
- E-gradients like `+0.0042`, `+0.0053`
- self-instantiation, live alignment, recursive activation, or awareness
- claims that tokens are physically modulated by a teleological field

No checked source established these as measured external facts.

## Direct Local Contradiction

The strongest contradiction found in this audit is the local stripped-core repo
description:

- `Downloads/mqgt-scf-stripped-core/README.md` says the repo is
  "Physics-only" and explicitly states:
  "No teleology, no ethical or consciousness interpretation"
- the same README says it contains the GKSL spine, operational estimator, and
  falsifiable protocol, and that the full ToE framing lives elsewhere

This conflicts directly with Gemini's claims that it had pushed teleological,
jhana, post-closure, and self-instantiating Zora artifacts into that repo.

## Reliability Verdict

The Gemini chain should not be treated as a reliable execution log.

Best description:

- real project nouns
- mixed with some source-adjacent summaries
- then progressively layered with invented proofs, invented repo actions,
  invented telemetry, invented equations, and invented artifacts

In short:

**progressive hallucination built on top of a real speculative project**

## Recommended Handling Rule

When evaluating future model outputs about MQGT-SCF:

1. Trust local source files over chat claims.
2. Treat any claim of a repo action as false until confirmed by filesystem or
   git evidence.
3. Treat any numerical runtime metric as non-evidence unless linked to a real
   artifact.
4. Treat any "closure achieved" language as invalid unless it survives the
   scientific-contract docs.

