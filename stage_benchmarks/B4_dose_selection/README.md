---
license: cc-by-4.0
---
# DrugDev-Bench — B4 Dose selection (stage benchmark, track T1)

**Scope.** 20 hand-authored scenarios (+ 20 generated in the generated tier).
**Ground-truth field(s).** policy-based `reference` dose index or no-dose label.
**Scoring.** `../../src/score.py dose` — exact dose-decision agreement under the deterministic
reference-curve policy.

**The reference-curve policy (implemented exactly in `score.py`).**
Let `p_j` be the DLT probability at ordered dose `d_j` and `τ` the target probability. Declare
**no dose** if `p_1 > τ + 0.10`; otherwise select the admissible dose (`p_j ≤ τ + 0.10`) minimizing
`|p_j − τ|`; **ties select the higher-indexed dose**; a small numerical tolerance is used at the threshold.

> **This is NOT BOIN.** It does not simulate sequential patient allocation, estimate toxicity from
> accumulating outcomes, or run BOIN's posterior elimination and final selection. The 0.10 band is a
> benchmark choice, not a universal BOIN safety criterion.
>
> **Two protocols are not pooled.** A historical dose-only leaderboard scores 18 non-null labels; the
> structured-response study includes all 20 outcomes (treating no-safe-dose as an outcome). They use
> different denominators and are reported separately.
>
> **Scorer limitation (flagged).** In a no-dose reference case, an absent dose field can currently receive
> credit without an explicit valid no-dose declaration. Scores are **provisional** and preserved as recorded.

## Two protocol versions (never pooled)

This dose track carries **two distinct scored protocols on the same scenarios**:

1. **Structured-response** (DrugDev-Bench, Table 1) — all **20** scenarios, treating no-safe-dose as an
   outcome. Oracle (hidden curve) **0.85** (17/20); Claude Opus 5 **0.25–0.30** (hand) vs **0.95–1.00** (generated).
2. **Same-item historical BOIN / dose-only** (moved from RealBio, Supplementary Table S1) — exact MTD
   agreement on the **18 scorable** scenarios (the two null-MTD references are excluded). Cross-system
   **8-direct-model mean 0.271** (GPT-5.6 and Biomni highest at 0.500). Score with `../../src/score.py boin`.

The drugdev manuscript explicitly forbids pooling these — different denominators (20 vs. 18) and different
reference semantics. Both tables are in `../../leaderboard.md`.

**Data.** `data.jsonl` (20 scenarios, runnable; `reference.true_MTD_level`/`true_MTD_mg`) + `cases.source.yaml`.
The deterministic reference-curve `dose` scorer and the `boin` MTD scorer are both in `../../src/score.py`.
