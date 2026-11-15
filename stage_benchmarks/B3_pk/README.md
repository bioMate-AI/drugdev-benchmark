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

**Recorded result (provisional).** Max within-twofold agreement **0.467** (Claude Opus 5) on the 15
hand-authored compounds; full table in `../../leaderboard.md`.

**Data.** `data.jsonl` ships with the suite package.
