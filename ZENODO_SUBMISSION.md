# Zenodo Submission Draft

## Record type

**Publication → Preprint**

## Title

**Interpretation Correctability in Adaptive AI: Evidence, Verification, and Calibration of Personalized Beliefs**

## Creator

Gesa Schneider  
Independent Researcher

## Publication date

2026-10-09

## Description

AI systems increasingly maintain persistent information about users in order to adapt across interactions. Yet preserving what a person said is not the same as maintaining a justified understanding of that person. A system may retain accurate evidence while its interpretation becomes outdated, overgeneralized, unsupported, or incorrectly applied.

This research note reports six controlled experiments examining memory integrity and interpretation correctability in adaptive AI. The experiments progressively tested repeated memory updating, atomic revision, immutable evidence preservation, evidence-grounded interpretation, evidence-based verification, and decomposed verification across entailment, temporal validity, and contextual scope.

In Experiment 6, decomposed verification produced sharply different cross-model results. With Qwen2.5-1.5B-Instruct, it rejected all eight corrupted interpretations but also all eight valid interpretations. In a successful cross-model replication using NVIDIA Nemotron 3 Ultra, decomposed verification again rejected all eight corrupted interpretations while retaining seven of eight valid interpretations, reaching 15/16 overall accuracy.

The results motivate interpretation correctability as a distinct evaluation target: whether adaptive AI can maintain useful inferences about a person while keeping those inferences grounded, current, contextually bounded, calibrated, and correctable.

## Keywords

- interpretation correctability
- AI memory
- long-term agents
- personalization
- human-AI interaction
- memory integrity
- belief revision
- verification
- calibration
- provenance

## Related identifier

https://github.com/GesaSchneider1/interpretation-correctability

Use the closest available relation indicating that the repository supplements or contains the reproducibility materials for the preprint.

## Access and licensing

Open access.

Recommended paper license: **CC BY 4.0**, if desired. Repository code remains under the existing MIT license.

## Primary upload

- `Interpretation_Correctability_Research_Note_v1.pdf`

Optional source file:

- `Interpretation_Correctability_Research_Note_v1_final5.docx`

## Claims discipline

The repository preserves frozen protocols, notebooks, raw outputs, implementation-failure records, limitations, and the canonical results record. Primary results are separated from post hoc descriptive analyses and incomplete replication attempts.
