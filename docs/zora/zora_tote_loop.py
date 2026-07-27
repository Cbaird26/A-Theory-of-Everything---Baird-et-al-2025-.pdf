"""
Reference pseudocode for a Zora-style TOTE loop.

This file is intentionally lightweight and Python-shaped so it can be
used as a starting point for an actual agent implementation.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class StatementClass(str, Enum):
    MEASURED = "measured"
    DERIVED = "derived"
    ASSUMED = "assumed"
    SPECULATIVE = "speculative"


class ExitReason(str, Enum):
    GOAL_REACHED = "goal_reached"
    FALSIFIED = "falsified"
    BLOCKED = "blocked"
    NO_SIGNAL_GAIN = "no_signal_gain"
    MAX_ITERATIONS = "max_iterations"


@dataclass
class Claim:
    text: str
    classification: StatementClass
    provenance: Optional[str] = None


@dataclass
class Goal:
    summary: str
    success_criteria: List[str]
    falsifiers: List[str]


@dataclass
class Assessment:
    target: str
    evidence: List[Claim]
    assumptions: List[str]
    blockers: List[str]
    confidence: float
    continue_loop: bool
    notes: List[str] = field(default_factory=list)


@dataclass
class Operation:
    name: str
    rationale: str
    params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LoopState:
    goal: Goal
    evidence: List[Claim]
    assumptions: List[str]
    history: List[Dict[str, Any]] = field(default_factory=list)
    confidence: float = 0.0
    iteration: int = 0
    exit_reason: Optional[ExitReason] = None
    final_summary: Optional[str] = None


def classify_statement(text: str, provenance: Optional[str] = None) -> Claim:
    """
    Minimal classifier stub.

    Real implementations should use stricter rules, not vibes:
    - measured: direct data, cited observations, reproducible outputs
    - derived: explicit calculations or code consequences
    - assumed: model choices, proxies, mappings, placeholders
    - speculative: interpretation beyond available support
    """
    lowered = text.lower()
    if "measured" in lowered or "observed" in lowered:
        classification = StatementClass.MEASURED
    elif "derived" in lowered or "follows from" in lowered:
        classification = StatementClass.DERIVED
    elif "assume" in lowered or "placeholder" in lowered:
        classification = StatementClass.ASSUMED
    else:
        classification = StatementClass.SPECULATIVE
    return Claim(text=text, classification=classification, provenance=provenance)


def default_test(state: LoopState) -> Assessment:
    """
    Test phase: identify the gap between the current state and the goal.
    """
    blockers: List[str] = []
    notes: List[str] = []

    if not state.evidence:
        blockers.append("No evidence loaded.")

    if not state.goal.falsifiers:
        blockers.append("No falsifiers stated.")

    if any(claim.classification == StatementClass.SPECULATIVE for claim in state.evidence):
        notes.append("Speculative statements present; avoid upgrading them into facts.")

    continue_loop = True
    if blockers and state.iteration > 0:
        continue_loop = False

    return Assessment(
        target=state.goal.summary,
        evidence=state.evidence,
        assumptions=state.assumptions,
        blockers=blockers,
        confidence=state.confidence,
        continue_loop=continue_loop,
        notes=notes,
    )


def choose_smallest_useful_operation(state: LoopState, assessment: Assessment) -> Operation:
    """
    Operate phase: prefer the smallest move that reduces uncertainty.
    """
    if "No evidence loaded." in assessment.blockers:
        return Operation(
            name="load_primary_sources",
            rationale="Cannot reason cleanly without source material.",
        )

    if any(claim.classification == StatementClass.SPECULATIVE for claim in state.evidence):
        return Operation(
            name="downgrade_or_reclassify_claims",
            rationale="Remove rhetoric before expanding the search or patch surface.",
        )

    if state.assumptions:
        return Operation(
            name="test_strongest_assumption",
            rationale="The highest-leverage next move is usually the weakest supported assumption.",
            params={"assumption": state.assumptions[0]},
        )

    return Operation(
        name="verify_reproducibility",
        rationale="If the state is coherent, the next move is to check whether it reproduces.",
    )


def execute_operation(state: LoopState, operation: Operation) -> LoopState:
    """
    Execution stub.

    Replace this with real integrations: file reads, script runs, tests,
    experiment orchestration, or code patches.
    """
    state.history.append({"phase": "operate", "operation": operation})

    if operation.name == "load_primary_sources":
        state.confidence += 0.1
    elif operation.name == "downgrade_or_reclassify_claims":
        state.confidence += 0.05
    elif operation.name == "test_strongest_assumption":
        state.confidence += 0.1
    elif operation.name == "verify_reproducibility":
        state.confidence += 0.1

    state.confidence = min(state.confidence, 1.0)
    return state


def should_exit(
    state: LoopState, assessment: Assessment, max_iterations: int
) -> Optional[ExitReason]:
    """
    Exit conditions for a disciplined loop.
    """
    if any(blocker == "No falsifiers stated." for blocker in assessment.blockers):
        return ExitReason.BLOCKED

    if state.confidence >= 0.9 and not assessment.blockers:
        return ExitReason.GOAL_REACHED

    if state.iteration >= max_iterations:
        return ExitReason.MAX_ITERATIONS

    if not assessment.continue_loop:
        return ExitReason.NO_SIGNAL_GAIN

    return None


def summarize_exit(state: LoopState) -> str:
    if state.exit_reason == ExitReason.GOAL_REACHED:
        return "Goal reached with acceptable confidence and no active blockers."
    if state.exit_reason == ExitReason.FALSIFIED:
        return "Claim failed against its falsifiers."
    if state.exit_reason == ExitReason.BLOCKED:
        return "Loop blocked by missing falsifiers or missing evidence."
    if state.exit_reason == ExitReason.NO_SIGNAL_GAIN:
        return "Further recursion would add style without adding signal."
    if state.exit_reason == ExitReason.MAX_ITERATIONS:
        return "Loop stopped at the iteration cap; escalate or narrow scope."
    return "Loop exited without a classified reason."


def tote_loop(
    state: LoopState,
    tester: Callable[[LoopState], Assessment] = default_test,
    operator: Callable[[LoopState, Assessment], Operation] = choose_smallest_useful_operation,
    executor: Callable[[LoopState, Operation], LoopState] = execute_operation,
    max_iterations: int = 5,
) -> LoopState:
    """
    Run Test -> Operate -> Test -> Exit.
    """
    while state.iteration < max_iterations:
        pre = tester(state)
        state.history.append({"phase": "test_pre", "assessment": pre})

        exit_reason = should_exit(state, pre, max_iterations)
        if exit_reason is not None:
            state.exit_reason = exit_reason
            state.final_summary = summarize_exit(state)
            return state

        operation = operator(state, pre)
        state = executor(state, operation)

        post = tester(state)
        state.history.append({"phase": "test_post", "assessment": post})

        exit_reason = should_exit(state, post, max_iterations)
        if exit_reason is not None:
            state.exit_reason = exit_reason
            state.final_summary = summarize_exit(state)
            return state

        state.iteration += 1

    state.exit_reason = ExitReason.MAX_ITERATIONS
    state.final_summary = summarize_exit(state)
    return state


if __name__ == "__main__":
    demo_goal = Goal(
        summary="Determine whether a claim is coherent, falsifiable, and worth the next action.",
        success_criteria=[
            "Evidence is classified.",
            "Assumptions are explicit.",
            "Falsifiers are stated.",
            "A smallest useful next action is chosen.",
        ],
        falsifiers=[
            "No operational definition exists.",
            "No observable consequence exists.",
        ],
    )

    demo_state = LoopState(
        goal=demo_goal,
        evidence=[
            classify_statement("Measured QRNG bound from a reproducible dataset.", "results/qrng"),
            classify_statement("Assume portal mapping remains a placeholder.", "docs/claims"),
        ],
        assumptions=["Portal mapping is adequate for triage."],
    )

    final_state = tote_loop(demo_state)
    print(final_state.exit_reason)
    print(final_state.final_summary)
