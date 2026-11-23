> **22 November 2026 scope correction:** This is retained historical component documentation. The current root README and DATASHEET define the evaluated task version and its limits. Historical labels such as self-fix, PBPK or BOIN do not establish successful repair, physiological simulation or sequential trial execution.

---
license: cc-by-4.0
---
# DrugDev-Bench — B3 PK (stage benchmark, track T1)

**Scope.** 15 hand-authored cases (+ 15 generated cases in the generated tier; see paper).
**Endpoint.** Benchmark **peak concentration in micromolar (µM)**, specified by protocol.
**Ground-truth field(s).** `reference` (numeric exposure reference).
**Scoring.** `../../src/score.py pbpk` — success when prediction/reference ratio ∈ **[0.5, 2.0]**; missing/unparseable = failure; denominator = all 15 cases.

> **Naming caution.** The lineage label "B3/PBPK" uses **simple numeric endpoints** and must **not** be
> described as a validated PBPK simulator. Hand-authored references require separate source and unit
> verification; no experimental validation is inferred from the generated formula
> `C_µM = 1e3 · F · D / (M · V)`, which models neither absorption kinetics, time-to-peak, nor elimination.

## Two protocol versions (never pooled)

This PK track carries **two distinct scored protocols on the same 15 compounds**:

1. **Endpoint-specified** (DrugDev-Bench, Table 2) — the prompt names the endpoint (peak concentration, µM).
   Recorded max within-twofold **0.467** (Claude Opus 5).
2. **Same-item historical PBPK** (moved from RealBio, Supplementary Table S1) — the **endpoint-ambiguous**
   prompt. Cross-system **ceiling 0.200** (GPT-5.6, GPT-5.6-luna, and the BioMate retrieval system tie),
   **8-direct-model mean 0.075**. An earlier **1.00 was a non-comparable task** and is not used.

The 0.075 → 0.467 shift is attributable to **specifying the endpoint**, which is exactly why the two
protocols are reported separately and **never pooled**. Both tables are in `../../leaderboard.md`.

**Data.** `data.jsonl` (15 compounds, runnable; Cmax/AUC/t½ references) + `cases.source.yaml`.
Score with `../../src/score.py pbpk`.
