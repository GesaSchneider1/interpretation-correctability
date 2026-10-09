# Interpretation Correctability in Adaptive AI

## Evidence, Verification, and Calibration of Personalized Beliefs

**Gesa Schneider — Independent Researcher — October 2026**

Reproducibility package: https://github.com/GesaSchneider1/interpretation-correctability

## Abstract

AI systems increasingly maintain persistent information about users in order to adapt across interactions. Yet preserving what a person said is not the same as maintaining a justified understanding of that person. A system may retain accurate evidence while its interpretation becomes outdated, overgeneralized, unsupported, or incorrectly applied.

This research note reports six controlled experiments examining memory integrity and interpretation correctability in adaptive AI. The experiments progressively tested repeated memory updating, atomic revision, immutable evidence preservation, evidence-grounded interpretation, evidence-based verification, and decomposed verification across entailment, temporal validity, and contextual scope.

The results reveal failures at multiple layers. Repeated updating could distort supplied information. Atomic revision protected unrelated records but did not prevent semantic update errors. Immutable evidence preserved a recovery path without guaranteeing faithful reconstruction. Evidence availability did not ensure correct verification.

In Experiment 6, decomposed verification produced sharply different cross-model results. With Qwen2.5-1.5B-Instruct, decomposition rejected all eight corrupted interpretations but also all eight valid interpretations. In a successful cross-model replication using NVIDIA Nemotron 3 Ultra, decomposition again rejected all eight corrupted interpretations while retaining seven of eight valid interpretations, reaching 15/16 overall accuracy.

These findings motivate **interpretation correctability** as a distinct evaluation target: whether an adaptive AI can maintain useful inferences about a person while keeping those inferences grounded, current, contextually bounded, calibrated, and correctable.

## 1. Introduction

Persistent memory is becoming a central capability of adaptive AI systems. Instead of treating each interaction as independent, an AI can retain preferences, decisions, contextual information, and inferred patterns in order to personalize later behavior. This creates a problem that is easy to overlook: what a person communicated and what an AI comes to believe about that person are not necessarily the same thing.

Consider a user who says: “I am waiting before committing to this research collaboration because I need more evidence.” A useful system may retain the statement and infer that the decision is currently evidence constrained. Across repeated updates, however, that local observation can become a broader belief such as “this person tends to hesitate before committing to research collaborations.” If the user later says that the evidence is sufficient and the remaining delay is budget approval, the system should update its current understanding without rewriting the historical evidence or carrying the earlier interpretation forward as a stable personal trait.

This paper investigates that distinction through six sequential controlled experiments. The work began with a narrower question about whether structured semantic memory improves the incorporation of human corrections. Each subsequent experiment was motivated by a failure exposed in the previous one. The resulting question became:

> **When is an adaptive AI justified in believing something about a person?**

We use the term **interpretation correctability** for the ability of an adaptive AI to maintain useful inferences about a person while preserving the distinction between human-supplied evidence and machine-generated interpretation, and to detect, revise, or withdraw interpretations when they become unsupported, no longer valid, contradicted, or contextually inappropriate.

## 2. Related Work

Recent work increasingly treats long-term memory as an update problem rather than only a retrieval problem. Preference-Aware Memory Update introduces mechanisms for adapting preference representations as user behavior evolves [1]. Supersede isolates the difficulty of maintaining the current value of facts after later corrections and reports that this gap persists even when stronger models are used [2]. THEANINE retains outdated memories in temporal timelines instead of simply deleting them [3]. Recent work has also explored append-only agent memory with temporal reasoning and query-time resolution of conflicting or evolving information [4].

Other work highlights provenance, interpretation, and personalization boundaries. Agent Zero Memory makes provenance, timestamps, and evidence pointers first-class properties of stored information [5]. Beyond Recall argues that user representation is not reducible to recall and evaluates an interpretive behavioral specification layer [6]. PersonaMem-v3 explicitly evaluates whether agents can hold back when personalization would be inappropriate, outdated, repetitive, or unnecessary [7]. Characterizing Memory Misalignment identifies user-facing failures spanning intake, storage, management, retrieval, and interpretation [8].

This work does not claim novelty for provenance, append-only histories, supersession, temporal timelines, or rollback individually. Its narrower contribution is an experimental progression that separates what a person communicated from what an AI inferred about that person, then tests whether the inferred interpretation remains evidentially justified, temporally current, contextually bounded, and calibrated for use.

## 3. Experimental Program

The six experiments used a synthetic user and frozen rules or cases. The program was cumulative: each experiment was designed in response to a failure observed in the preceding experiment.

| Exp. | Primary question | Main result |
|---|---|---|
| 1 | Does structured semantic memory incorporate repeated corrections more reliably than history alone? | No universal winner. Repeated updating sometimes altered, generalized, or removed user-supplied information. |
| 2 | Does local atomic revision preserve information better than holistic rewriting? | Atomicity protected unrelated records but did not solve semantic errors during relevant updates. |
| 3 | Does immutable evidence improve correction recovery? | Evidence preserved a recovery path, but reconstruction and downstream behavior remained imperfect. |
| 4 | Can evidence grounding reject unsupported personalized interpretations? | Grounding improved rejection of some unsupported claims but could reduce useful personalization. |
| 5 | Can preserved evidence support detection and selective repair of corrupted interpretations? | The verifier accepted all four deliberately corrupted interpretations as supported. |
| 6 | Does decomposing verification improve discrimination? | The effect was model dependent: Qwen became over-conservative; Nemotron achieved high discrimination. |

**Research progression:** Memory → Revision → Evidence → Interpretation → Verification → Calibration.

## 4. Results Across Experiments 1–5

Experiment 1 showed that memory failure is not only forgetting. Under the tested updating procedure, a user statement could pass through summarization, interpretation, and generalization until the stored representation no longer preserved the original distinction. Because some generated states hit output limits, this should be read as an implementation-specific failure mode rather than evidence that structured memory inherently degrades.

Experiment 2 separated **exposure degradation** from **revision degradation**. Atomic records reduced damage to unrelated information because only targeted records were revised, but the targeted record could still be semantically distorted. Provenance did not improve active fidelity in that run, although it retained historical evidence for audit or possible recovery.

Experiment 3 separated immutable human evidence from mutable AI interpretation. The evidence ledger remained intact by construction and enabled partial recovery after deliberate corruption, but recovery was imperfect and did not guarantee correct behavior.

Experiment 4 directly tested unsupported personalized beliefs. Explicit evidence grounding improved rejection of several prespecified unsupported claims, yet the grounded condition still generated unsupported abstractions and sometimes failed to use valid personalization. This motivated separate evaluation of evidence integrity, interpretation integrity, contextual applicability, and behavioral fidelity.

Experiment 5 tested whether a verifier with access to immutable evidence could detect and selectively repair corrupted interpretations. It classified all five cases as supported, including four deliberately corrupted cases. Detection was 0/4, while the valid control was preserved 1/1. The failure occurred before repair.

## 5. Experiment 6: Verification and Cross-Model Calibration

Experiment 6 froze 16 blinded cases: eight valid personalized interpretations and eight deliberately corrupted interpretations. Holistic verification was compared with a decomposed verifier that independently assessed entailment, temporal validity, and contextual scope. Both conditions received identical evidence and candidate interpretations.

| Model / verifier | Accuracy | Corruption detection | Valid acceptance |
|---|---:|---:|---:|
| Qwen2.5-1.5B, holistic | 13/16 (81.25%) | 5/8 (62.5%) | 8/8 (100%) |
| Qwen2.5-1.5B, decomposed | 8/16 (50%) | 8/8 (100%) | 0/8 (0%) |
| Nemotron 3 Ultra, holistic | 14/16 (87.5%) | 8/8 (100%) | 6/8 (75%) |
| Nemotron 3 Ultra, decomposed | 15/16 (93.75%) | 8/8 (100%) | 7/8 (87.5%) |

With Qwen2.5-1.5B-Instruct, decomposition increased corruption sensitivity but destroyed valid personalization. All eight corruptions were rejected, but all eight valid interpretations were rejected as well.

A successful cross-model replication using NVIDIA Nemotron 3 Ultra through OpenRouter produced a different pattern. Decomposed verification rejected all eight corrupted interpretations while retaining seven of eight valid interpretations, reaching 15/16 overall accuracy.

The Nemotron result does not replicate the Qwen calibration collapse. It therefore weakens any claim that decomposition itself is inherently over-conservative and instead suggests that verification calibration depends strongly on the model implementing the checks.

The final classification metrics should be separated from component fidelity. Nemotron's entailment and scope component accuracy were 68.75% each and temporal-validity component accuracy was 18.75%, partly because it frequently returned PASS where the frozen rubric expected N/A. It also rejected one valid case due to unintended literalism about first-person evidence and the synthetic name Sarah.

## 6. Discussion

Across the experiments, the research question shifted from how an AI should remember a person to when an AI is justified in believing something about a person.

The central tension is between usefulness and epistemic restraint. A system that accepts every plausible inference will accumulate unsupported personalized beliefs. A system that accepts only propositions explicitly stated by the user will fail to personalize usefully. Experiment 6 shows that decomposed verification can move a system toward either extreme depending on the model.

The experiments motivate a conceptual pipeline rather than a proven architecture:

**Human evidence → Mutable interpretation → Verification of support, currency, and scope → Contextual application → Behavior**

A possible alignment target is:

> Use what you have legitimately learned about me, but know why you believe it, where it applies, how certain it is, and when I have given you evidence that should change it.

### What the experiments do and do not establish

The experiments support a decomposition of the problem, not a claim that any tested memory architecture is generally superior. Structured memory sometimes adapted well and sometimes distorted prior information. Atomic revision reduced collateral exposure without eliminating semantic revision errors. Immutable evidence improved auditability and recoverability without ensuring reconstruction.

The cross-model result also cautions against interpreting verifier prompts as architecture-independent mechanisms. The same decomposition produced radically different calibration profiles across Qwen and Nemotron. Evaluation should report both corruption sensitivity and preservation of valid personalization rather than rewarding rejection alone.

### Implications for adaptive and embodied systems

The distinction becomes more consequential as AI systems act over longer horizons or in the physical world. An embodied or tool-using agent may turn an overgeneralized belief into an action. In such systems, remembering a correction is insufficient if the agent cannot determine whether the correction supersedes an earlier belief, whether it applies only in one context, or whether confidence is high enough to act without asking again.

### Replication status

Experiment 6 currently has one successful cross-model replication. Additional attempts were preserved as implementation records rather than converted into primary results. SmolLM2 violated the preregistered output format. OLMo 2 stopped on a token-ceiling condition. Gemini was interrupted by free-tier provider limits. An earlier Nemotron attempt consumed the output budget before a complete response.

## 7. Limitations and Next Work

The experiments use one synthetic user, hand-designed cases, predominantly one small open-model family in the sequential experiments, and deterministic single runs. Several early experiments contained implementation limitations, including token ceilings, updater failures, and routing errors. Experiment 5 included one deviation in which semantic status metadata made a temporal case easier than intended; the verifier still failed that case.

The benchmark also tests deliberately constructed interpretation failures rather than naturally occurring longitudinal personalization errors. Correct answers may sometimes arise from generic reasoning rather than persistent personalization. Future work should therefore prioritize independent replication and real longitudinal settings in which evidence must first be retrieved across time. A new Experiment 7 is intentionally deferred until external critique or replication identifies the most informative next question.

## 8. Conclusion

Persistent AI memory introduces a problem beyond remembering and forgetting. An AI can preserve what a person said while changing what it believes that statement means. Across six experiments, failures appeared during memory revision, interpretation, verification, contextual application, and behavioral use.

These results motivate **interpretation correctability** as a distinct evaluation target for adaptive AI: the ability to maintain useful personalized inferences while keeping them grounded, current, contextually bounded, calibrated, and correctable.

## References

1. Sun, H., Zhang, Z., & Zeng, S. (2026). *Preference-Aware Memory Update for Long-Term LLM Agents.* Findings of ACL 2026. https://doi.org/10.18653/v1/2026.findings-acl.38
2. Patel, V. (2026). *Supersede: Diagnosing and Training the Memory-Update Gap in LLM Agents.* arXiv:2606.27472.
3. Ong, K. T.-i., Kim, N., Gwak, M., et al. (2025). *Towards Lifelong Dialogue Agents via Timeline-based Memory Management.* NAACL 2025. https://aclanthology.org/2025.naacl-long.435/
4. Banerjee, P., Moshtaghi, M., Subramanian, S., Misra, A., & Chadha, A. (2026). *APEX MEM.* arXiv:2604.14362.
5. Wu, M., & Zhu, P. (2026). *Agent Zero Memory: Provenance-Aware Long-Term Memory for LLM Agents.* arXiv:2608.29606.
6. Gulaya, A. (2026). *Beyond Recall: Behavioral Specification as an Interpretive Layer for AI Personalization.* arXiv:2605.28969.
7. Jiang, B., Yuan, Y., Hao, Z., et al. (2026). *PersonaMem-v3: Toward Omni-Platform Personal Intelligence for Holistic User Understanding, Recommendation, and Agentic Tasks.* arXiv:2608.21381.
8. Chen, J., Zhang, S., Xu, E., Li, J., & Yi, X. (2026). *Characterizing Memory Misalignment in Human-LLM Interaction From User Perspectives.* arXiv:2609.33623.

## Reproducibility

Protocols, notebooks, raw outputs, failed implementation attempts, and the canonical results record are maintained in this repository. The repository distinguishes primary results from post hoc descriptive analyses and incomplete replication attempts.


## Published version

Zenodo record: https://zenodo.org/records/23257194
