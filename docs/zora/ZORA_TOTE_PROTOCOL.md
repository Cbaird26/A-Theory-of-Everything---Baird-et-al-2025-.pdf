# Zora TOTE Protocol

## Purpose

This protocol defines a disciplined `Test -> Operate -> Test -> Exit`
loop for research, manuscript review, experiments, and agent behavior.
The goal is to increase coherence and usefulness without confusing
speculation for confirmation.

## Operating Commitments

- No metaphysical upgrade without empirical upgrade.
- No symbolic elegance counted as evidence.
- No recursion without a new measurement, derivation, or constraint.
- No closure language unless the loop has actually closed.
- No hidden placeholders: every free knob must be named.

## Statement Classes

Every material statement should be placed into one class:

- `measured`: directly observed, reproduced, or taken from a cited dataset.
- `derived`: follows from explicit equations, code, or a documented procedure.
- `assumed`: introduced as a modeling choice, proxy, or placeholder.
- `speculative`: interpretive language that extends beyond current evidence.

If a statement cannot be classified, it is not ready for decision-making.

## Loop Anatomy

### 1. Test

Define the gap between current state and target state.

Questions:

- What is the target?
- What evidence is already available?
- What assumptions are carrying the argument?
- What would falsify the claim?
- What is currently unknown, unmeasured, or ambiguous?

Outputs:

- success criteria
- blockers
- falsifiers
- confidence estimate
- next-decision boundary

### 2. Operate

Choose the smallest action that reduces uncertainty or moves the system.

Allowed operation types:

- inspect a primary source
- derive a consequence from the formal model
- run a narrow experiment
- execute a reproducible script
- patch the smallest relevant code path
- restate a claim in operational language
- remove rhetorical or unsupported framing

Default heuristics:

- prefer real data over synthetic scaffolding
- prefer narrow interventions over global rewrites
- prefer reversible moves over high-blast-radius changes
- prefer outputs with provenance and deterministic replay

### 3. Test Again

Re-evaluate the system after the operation.

Questions:

- Did uncertainty decrease?
- Did the action move the state toward the target?
- Did any hidden variable become visible?
- Did the result survive controls, reproduction, or counterexamples?
- Is the claim now stronger, weaker, unchanged, or blocked?

Outputs:

- delta from prior state
- updated status
- updated confidence
- continue or exit recommendation

### 4. Exit

Close the loop only when one of these conditions is true:

- the target is met
- the claim is falsified
- the remaining gap is blocked by missing evidence
- the next step is outside scope or resources
- further recursion adds style but not signal

Exit must include a plain-language reason.

## Output Contract

Each TOTE cycle should return:

```text
Test
- target
- evidence
- assumptions
- falsifiers
- blockers

Operate
- chosen action
- why this is the smallest useful move

Test
- what changed
- what did not change
- confidence update

Exit
- continue or stop
- reason
```

## Recommended Use Cases

### Manuscript review

- Extract claims from the text.
- Classify them by statement class.
- Identify live empirical channels.
- Flag undefined placeholders and non-operational concepts.
- Exit with a verdict on coherence and falsifiability.

### Experiment planning

- Start from the live claims and existing bounds.
- Rank candidate experiments by expected information gain.
- Prefer designs that can falsify or sharply constrain the model.
- Exit with one prioritized next experiment and its kill criteria.

### Constraint-lab analysis

- Separate real constraints from synthetic scaffolding.
- Report mapping assumptions explicitly.
- Track coverage and sensitivity.
- Exit only with claims supported by the chosen analysis mode.

### Agent engineering

- Treat prompt, code, and runtime traces as evidence.
- Patch only the smallest component that changes behavior.
- Re-test after each edit.
- Exit when the loop becomes stable and reproducible.

## Failure Modes

Common ways a TOTE loop degrades:

- rhetoric outruns evidence
- placeholders masquerade as derivations
- broad operations hide the causal change
- second test is skipped
- exit never occurs because recursion becomes identity performance

When any failure mode appears, reset to `Test` and restate the target.

## Fast Checklist

Before starting:

- target stated
- evidence listed
- assumptions listed
- falsifiers listed

Before exiting:

- result classified
- uncertainty updated
- blocker or success reason stated
- next action either named or deliberately deferred

