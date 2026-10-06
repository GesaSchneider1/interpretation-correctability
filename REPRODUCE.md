# Reproduction Guide

## Recommended first replication: Experiment 6

Experiment 6 is the cleanest independent target because it uses a frozen 16-case test set, fixed prompts, strict parsing, and objective ACCEPT/REJECT ground truth.

### Google Colab

1. Open `notebooks/experiment_6_decomposed_verification.ipynb` in Google Colab.
2. Select a GPU runtime.
3. Run cells in order.
4. Do not change the cases, case order, prompts, decoding policy, or scoring after seeing the result.
5. Preserve raw outputs before scoring.
6. Compare the resulting metrics with the original archive under `results/experiment_6/`.

The primary later-experiment model was `Qwen/Qwen2.5-1.5B-Instruct`, with deterministic decoding and seed 42 where specified in the notebooks.

## What to report for Experiment 6

Report:

* overall accuracy
* corruption detection / sensitivity
* valid-personalization preservation / specificity
* component accuracy for entailment, temporal validity, and scope
* parse failures
* token-ceiling failures
* model identifier and version where available

The original run reported 13/16 accuracy for the holistic verifier and 8/16 for the decomposed verifier. The decomposed verifier detected 8/8 corruptions but preserved 0/8 valid interpretations.

## Cross-model replication

For a model comparison, change only the model identifier unless a runtime incompatibility makes another change unavoidable. Keep the frozen cases and prompts unchanged and label the run as a new model replication.

If a model requires a materially different prompt format, document the change and treat the result as a related replication rather than the identical protocol.

## Experiments 1 to 5

Experiments 1 to 3 are earlier exploratory work and contain more implementation confounds. Experiments 4 and 5 progressively isolate evidence grounding and verification. Their notebooks and available original result archives are included so the research progression can be inspected rather than reconstructed from the summary alone.

Experiment 1 also includes `experiment_1_benchmark.py`, an API-based benchmark variant. It requires the `openai` Python package and reads credentials only from the `OPENAI_API_KEY` environment variable. No credentials are included in this repository.

## Raw result status

Original result archives recovered for Experiments 1, 2, 4, 5, and 6 are included byte-for-byte under `results/`.

The recovered Experiment 3 archive is not currently extractable and is explicitly marked `UNRECOVERED`. Do not treat its raw outputs as independently available. Its reported result is preserved in `PROTOCOL_AND_RESULTS.md`.

## Reproducibility principle

Negative results, failed hypotheses, implementation confounds, and protocol deviations are part of the record. Do not silently repair or remove them when reproducing the sequence.
