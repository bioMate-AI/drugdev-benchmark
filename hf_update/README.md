---
license: cc-by-4.0
pretty_name: DrugDev-Bench
task_categories:
  - other
language:
  - en
tags:
  - drug-discovery
  - drug-development
  - pharmacokinetics
  - dose-finding
  - free-energy
  - admet
  - benchmark
  - llm-evaluation
  - agents
size_categories:
  - n<1K
configs:
  - config_name: default
    data_files:
      - split: info
        path: README.md
---

# DrugDev-Bench — an inspectable benchmark for drug-development *decisions*

Drug development is a chain of **decisions under constraints** — which target to study, which analogue to advance, whether exposure is sufficient, which dose to give next. DrugDev-Bench evaluates those decisions against **explicit reference policies**, keeping *a plausible answer* strictly separate from *a correctly executed one*, and keeping different kinds of ground truth (experimental, formula-derived, curated-policy, provisional) **labeled and non-interchangeable**.

> **This card documents a benchmark-DESIGN release** with instantiated task sets, offline validation, and *selected* model experiments. It is **not** a full model-vs-model leaderboard across all four tracks. The dose and PK numbers below are **provisional, run-level observations** pending scorer/reference-policy reconciliation (see the paper). They are **not** confidence intervals and do **not** establish clinical accuracy.

- **Code / scorer / full docs:** https://github.com/bioMate-AI/drugdev-benchmark
- **Paper (source of truth):** `paper/drugdev.pdf` in the GitHub repo
- **Sibling benchmark:** [RealBio](https://github.com/bioMate-AI/realbio-benchmark)
- **License:** CC-BY-4.0 (Merck/Schindler free-energy data retain their own attribution)

## Four tracks
- **T1 Molecular-tool workflows** — ADMET (B1, 20), docking/ligand ranking (B2, 15), PK (B3, 15 hand-authored), dose selection (B4, 20 hand-authored), target structure (B5, 10), relative binding free energy (N1, 8 series / 264 ligands).
- **T2 Targets & perturbations** — design-level in this release.
- **T3 Search & knowledge** — design-level in this release.
- **T4 Cross-stage execution** — specified; exercised via offline composer diagnostics (68 topologies).

Plus a **30-item decision suite** across nine archetypes (22/8 train/eval split) and two-item seeds for QSAR, retrosynthesis, and target identification.

## Scoring
One deterministic scorer, **no LLM judge**, six entry points (decision, categorical, set, numeric, dose, chain). The dose policy and generated-tier exposure formulas are fully specified and implemented in `src/score.py`.

## Selected results (provisional — see paper)
**Dose (two tiers of 20):** Oracle with hidden curve 0.85 (17/20); Claude Opus 5 0.25–0.30 hand vs 0.95–1.00 generated — **task construction dominates the result.**
**PK within-twofold (15 hand-authored):** Claude Opus 5 0.467 (max), Gemini 3.1 Pro 0.400, GPT-5.6-luna 0.333, GLM-5.2 0.267, GPT-5.6 0.200, others ≤0.067. Agreement with benchmark references, **not** clinical accuracy.
**Ligand ranking (15 items):** mean Spearman 0.696 across eight direct-model systems.
**Offline validation:** scorer/adapter/export implementation contracts pass (6/6, 15/15, 5/5, 14/14, 30/30, 22/22; free-energy oracle RMSE 0, composite ≈0.98).

## Citation
```bibtex
@misc{drugdevbench2026,
  title  = {DrugDev-Bench: an inspectable benchmark for drug-development decisions
            from molecular discovery to dose selection},
  author = {Zhang, Yaoyun and Dike, Andrew},
  year   = {2026},
  note   = {BioMate AI · BizBildr},
  url    = {https://github.com/bioMate-AI/drugdev-benchmark}
}
```

## Ethics & competing interests
A nonclinical methodological benchmark; modeled dose/exposure references are **not** dosing recommendations. The authors also develop BioMate, an evaluated system (declared competing interest).
