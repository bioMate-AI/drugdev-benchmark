> **22 November 2026 scope correction:** This is retained historical component documentation. The current root README and DATASHEET define the evaluated task version and its limits. Historical labels such as self-fix, PBPK or BOIN do not establish successful repair, physiological simulation or sequential trial execution.

---
license: cc-by-4.0
---
# DrugDev-Bench — B2 Docking & ligand assessment (stage benchmark, track T1)

**Scope.** 15 shared items. Structural / affinity references.
**Reported model endpoint.** **Ligand ranking** (the richer relative free-energy data live in `N1_free_energy/`).
**Scoring.** rank-correlation (Spearman) via `../../src/score.py`.

> **Coarse-metric caution.** With only three ligands per ranking item, the possible correlations are coarse.
> The historical export reports **mean Spearman 0.696 across eight direct-model systems**; a domain-agent
> value of 1.0 covers only **four completed cases** and is **not** a full-set result. This is evidence about
> a small ranking task — not docking-pose accuracy, prospective affinity prediction, or a completed
> discovery programme.

**Data.** `data.jsonl` ships with the suite package.
