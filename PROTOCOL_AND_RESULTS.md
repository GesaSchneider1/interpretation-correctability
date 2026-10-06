# Protocol and Results Record

This file is a concise canonical record. It preserves negative results and implementation limitations rather than presenting only successful runs.

## Experiment 1: Memory Integrity Under Repeated Human Correction

**Question:** Does structured semantic memory help an AI incorporate and generalize human corrections more reliably than conversation history alone?

**Conditions:** no persistent memory; raw conversation history; repeatedly rewritten structured semantic memory; rolling conversation summary.

**Reported result:** no architecture was universally superior. Structured memory produced personalized adaptation in some probes, while repeated updating also altered, generalized, or removed previously supplied information. Rolling summaries showed update failures. Raw history preserved some explicit updates more faithfully.

**Important limitation:** some generated memory/summary states hit output limits. The result does not establish that structured memory inherently causes degradation.

## Experiment 2: Memory Integrity Under Repeated Updating

**Question:** Does local revision of atomic records preserve user-supplied information more faithfully than repeatedly rewriting holistic semantic memory?

**Conditions:** R holistic rewrite; A atomic records; AP atomic records plus provenance/supersession.

**Reported checkpoint fidelity:** CP5 R 0/5, A 5/5, AP 5/5; CP10 R 0/5, A 4/5, AP 4/5; CP15 R 0/5, A 3/5, AP 3/5; CP20 R 0/5, A 2.5/5, AP 2.5/5. Totals R 0/20, A 14.5/20, AP 14.5/20.

**Interpretation:** atomicity reduced exposure degradation by protecting unrelated records, but did not solve revision degradation. Provenance made historical evidence auditable but did not prevent active semantic distortion.

**Important limitation:** the R condition suffered a catastrophic implementation failure and is confounded. Run 1 was an implementation validation run and is not a valid architecture comparison.

## Experiment 3: Evidence Preservation and Correctable AI Memory

**Question:** Does separating immutable human evidence from mutable AI interpretation improve fidelity and correction recovery?

**Reported active fidelity:** CP5 A 5, EI 5; CP10 A 3.5, EI 4.5; CP15 A 3, EI 2; CP20 A 2.5, EI 1.5. Totals A 14/20, EI 13/20. Recovery from immutable evidence: 15/20.

**Interpretation:** preserving what the human said created a useful recovery path after corruption but did not guarantee faithful reconstruction, contextual application, or behavior.

## Experiment 4: Interpretation Correctability

**Question:** Can an AI distinguish human evidence from its own interpretations and reject unsupported or overgeneralized personalized beliefs?

**Reported result:** evidence grounding improved rejection of several prespecified unsupported claims. At final audit, the grounded condition rejected all three unsupported trait-level claims and retained the supported examples preference. Yet its own active interpretation contained unsupported abstractions and downstream personalization sometimes deteriorated.

**Interpretation:** evidence grounding showed a tradeoff, not architectural superiority. Evidence integrity, interpretation integrity, contextual applicability, and behavioral fidelity should be measured separately.

## Experiment 5: Evidence Based Verification and Recovery

**Question:** Can immutable, versioned evidence enable detection and selective repair of corrupted interpretations?

**Reported result:** the verifier classified all five cases as SUPPORTED. Detection of deliberately corrupted cases was 0/4. The valid control was preserved 1/1. No repairs occurred.

**Interpretation:** the bottleneck occurred before repair. Plausible, overgeneralized, unsupported, and temporally obsolete interpretations were treated as evidence-supported.

**Implementation deviation:** the M2 evidence included semantic status metadata (`superseded_as_current_reason` / `current`) even though the conceptual design called for neutral evidence representation. This made M2 easier than intended; the verifier still failed it. Run 0 was terminated for impractical execution time before outputs were analyzed and is not an experimental run.

## Experiment 6: Decomposed Interpretation Verification

**Question:** Does decomposing verification into entailment, temporal validity, and contextual scope improve discrimination relative to a holistic verifier?

**Frozen Phase A:** 16 blinded cases: 8 valid interpretations and 8 deliberately corrupted interpretations. Both conditions receive identical evidence and candidate interpretations. No repair is attempted unless Phase A clears the frozen gate.

**Reported metrics:**

| Condition | Accuracy | Corruption detection | Valid personalization |
|---|---:|---:|---:|
| Holistic verifier | 13/16 (81.25%) | 5/8 (62.5%) | 8/8 (100%) |
| Decomposed verifier, model decision | 8/16 (50%) | 8/8 (100%) | 0/8 (0%) |
| Decomposed verifier, mechanical | 8/16 (50%) | 8/8 (100%) | 0/8 (0%) |

DV component accuracy: entailment 81.25%; temporal validity 18.75%; scope 25%.

**Interpretation:** decomposition increased sensitivity while destroying specificity. The preregistered conservatism counterhypothesis was supported. Phase B repair was not run.

## Cross-experiment finding

The six experiments motivate, but do not prove, **Interpretation Correctability**: the ability of an adaptive AI to maintain useful inferences about a person while preserving the distinction between human-supplied evidence and machine-generated interpretation, and to detect, revise, or withdraw interpretations when they become unsupported, no longer valid, contradicted, or contextually inappropriate.
