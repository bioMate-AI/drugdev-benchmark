---
license: cc-by-4.0
pretty_name: DrugDev-Bench
task_categories:
  - other
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
---

# DrugDev-Bench — an inspectable benchmark for drug-development *decisions*, from molecular discovery to dose selection

### The one-sentence version
Drug development is a chain of **decisions under constraints** — which target to study, which analogue to advance, whether exposure is sufficient, which dose to give next — and DrugDev-Bench asks whether an AI system can make those decisions against **explicit reference policies**, keeping *a plausible-sounding answer* strictly separate from *a correctly executed one*.

### Why this benchmark is built the way it is
A model can predict a single property — a binding affinity, a toxicity flag, a concentration — and still be unable to turn those predictions into a defensible project decision. Most drug-discovery benchmarks score one property endpoint in isolation; DrugDev-Bench instead makes three things explicit for every item: **the information the solver is given, the policy that defines the correct decision, and the evidence required to confirm the decision was actually executed** (not just described).

A second design commitment runs through the whole suite: **different kinds of ground truth are not interchangeable.** Experimental affinity data, closed-form reference formulas, model-derived toxicity curves, curated policy labels, and provisional class-level values are each valid for different claims — and DrugDev-Bench keeps them labeled as such rather than collapsing them into one headline number.

> ### Read this first — what this release *is* and *is not*
> This is a **benchmark-design release with instantiated task sets, offline validation evidence, and selected model experiments.** It is deliberately *not* a full model-vs-model leaderboard across all four tracks. The dose and pharmacokinetic (PK) numbers below are **provisional, run-level observations** pending the scorer and reference-policy reconciliation described in the paper (`paper/drugdev.pdf`, Methods) — they are **not** confidence intervals, and they do **not** establish clinical accuracy or general model capability. We report exactly what was measured, on exactly which items, and flag what has not yet been run suite-wide. This honesty is the point: the suite is designed to be *inspected*, not to crown a winner.

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)

**🌐 Project:** [biomate.ai](https://biomate.ai) · **📄 Paper:** [`paper/drugdev.pdf`](paper/drugdev.pdf) · **📊 Datasheet:** [`DATASHEET.md`](DATASHEET.md) · **🔗 Sibling benchmark:** [RealBio](https://github.com/bioMate-AI/realbio-benchmark)

---

## The four tracks

DrugDev-Bench organizes drug-development work into four tracks (Fig. 1 in the paper). **Track membership is a design classification — it does not assert that every task has a completed model sweep.**

| Track | Scope | What a correct answer requires |
|---|---|---|
| **T1 — Molecular-tool workflows** | ADMET, docking/ligand assessment, PK, dose selection, target structure, relative binding free energy | A specified calculation or property call, scored against its stated reference and units |
| **T2 — Targets & perturbations** | Target prioritization, perturbation-response tasks | A decision grounded in target/perturbation evidence (design-level in this release) |
| **T3 — Search & knowledge** | Evidence retrieval and knowledge-grounded decisions | A conclusion backed by retrieved evidence, not a plausible rationale alone |
| **T4 — Cross-stage execution** | End-to-end and cross-stage tasks with terminal-state + artifact checks | A real run whose outputs have the right identity, units, representation and provenance for the next stage |

**Instantiated components in this release:** five **stage benchmarks** (B1–B5), one **relative binding free-energy dataset** (N1: 8 series, 264 ligands), and a **30-item decision suite** across nine archetypes. The execution track (T4) is specified and exercised through **offline composer diagnostics** — not yet a completed roster-wide execution study.

---

## Repository layout

```
├── stage_benchmarks/
│   ├── B1_admet/            # 20 compounds — curated ADMET property/toxicity labels
│   ├── B2_docking_ligand/   # 15 shared items — ligand-ranking endpoint
│   ├── B3_pk/               # 15 hand-authored PK cases (peak concentration, µM)
│   ├── B4_dose_selection/   # 20 hand-authored dose scenarios (policy-based labels)
│   └── B5_target_structure/ # 10 targets — sequence/structure + pocket residues
├── N1_free_energy/          # 8 congeneric series, 264 ligands (Merck/Schindler FEP)
├── decision_suite/          # 30 decision tasks across 9 archetypes (22/8 train/eval split)
├── execution_track/         # cross-stage composer diagnostics (offline)
├── src/score.py             # deterministic scorer scaffold — six scoring entry points
├── leaderboard.md / .csv    # SELECTED, PROVISIONAL experiments (dose, PK, ligand ranking)
├── models.yaml              # model roster for the selected experiments
├── paper/drugdev.pdf        # the manuscript (source of truth)
└── DATASHEET.md             # dataset documentation (scope, provenance, limitations)
```

Each component carries its own `README.md` stating scope, ground-truth field(s), reference basis, and scoring entry point. **Data files (`data.jsonl`) are released from the suite package;** this public repo ships the documentation, scorer scaffold, and selected results. Where an item set is not yet publicly released, its README says so explicitly.

---

## The instantiated components (what actually exists today)

### Stage benchmarks (Table 4 in the paper)

| Component | Scope | Reference / evaluation | Track |
|---|---|---|---|
| **B1 ADMET** | 20 compounds | Curated property & toxicity labels (hERG, DILI, Ames-related, rule-of-five descriptors); provenance differs by endpoint | T1 |
| **B2 Docking & ligand assessment** | 15 shared items | Structural/affinity references; the reported model endpoint is **ligand ranking** | T1 |
| **B3 PK** | 15 hand-authored cases | Numeric exposure reference; endpoint = **peak concentration (µM)**, specified by protocol | T1 |
| **B4 Dose selection** | 20 hand-authored scenarios | Policy-based dose / no-dose references (deterministic reference-curve rule) | T1 |
| **B5 Target structure** | 10 targets | Sequence/structure inputs + pocket-residue references | T1 |
| **N1 Relative binding free energy** | 8 series · 264 ligands | Experimental affinity-derived ΔΔG (Merck/Schindler FEP benchmark) | T1 |

> **A naming caution carried from the paper:** the PK component (lineage label *B3*) uses **simple numeric endpoints**; it must **not** be described as a validated PBPK simulator just because of that label. Likewise the dose policy below is **not** the full Bayesian Optimal Interval (BOIN) trial design.

### The decision suite — 30 tasks, nine archetypes (Table 5)

Each item presents a project context, inputs, constraints, and a required decision; the reference conclusion is hidden from the prompt. Counts sum to 30. **Reference bases are mixed and are kept labeled.**

| Archetype | Tasks | Decision | Reference basis |
|---|---:|---|---|
| **C** Lead-optimization triage | 3 | Advance or deprioritize analogues; identify liability | ADMET reference inputs + project policy |
| **E** FEP selection | 2 | Rank binders and select candidates | Experimental relative free energy |
| **H** Dose escalation | 3 | Select MTD and safety flags | Benchmark dose-selection policy |
| **F1/G** Dose projection | 3 | Starting-dose / human-clearance estimate | MRSD formula + allometric assumptions |
| **F2** Tissue/organ exposure | 3 | Assess target-site exposure | Unbound-partition / class-level references *(provisional)* |
| **F3** Dose schedule | 3 | Choose regimen from the PK/PD driver | Curated PK/PD class |
| **F4** Special populations | 4 | Adjust for organ impairment or interactions | Label-derived / provisional class values *(provisional)* |
| **P** Process knowledge | 6 | Identify gates and prerequisites | Curated development-process references |
| **W** Workflow chain | 3 | Order stages and enforce gates | Reference directed acyclic graph |

A **22/8 train/evaluation split** applies to these 30 items, with template-separated sources and a fail-closed overlap guard. (The 264 free-energy ligands are a **separate** component and are **not** added to this 30-item denominator.)

### Seeds and designed extensions (Supplementary S2)

The export also contains **two-item seeds** for QSAR, retrosynthesis, and target identification — enough to instantiate the task family, **not** enough for inferential ranking. Molecular generation, stability/manufacturing, freedom-to-operate, regulatory narrative, and full cross-stage execution are part of the coverage plan **without assigned model results** in this release.

---

## Scoring — one deterministic scaffold, six entry points

`src/score.py` exposes **six scoring entry points** matching the output types in the suite: **decision, categorical, set, numeric, dose, chain** (no LLM judge). The two fully-specified policies are implemented here exactly as the paper defines them:

**Dose-selection policy (deterministic reference-curve rule).** Let `p_j` be the dose-limiting-toxicity (DLT) probability at ordered dose `d_j` and `τ` the target probability. The rule declares **no dose** if `p_1 > τ + 0.10`; otherwise it selects the admissible dose minimizing `|p_j − τ|`, where admissibility means `p_j ≤ τ + 0.10`; **ties select the higher-indexed dose**, with a small numerical tolerance at the threshold.

> **This is a benchmark reference policy, not BOIN.** It does not simulate sequential patient allocation, estimate toxicity from accumulating outcomes, or run BOIN's posterior elimination and final selection. The 0.10 band is a benchmark choice.

**Generated exposure/toxicity references.** Generated dose cases use bioavailability `F`, dose `D` (mg), molecular weight `M` (g/mol), distribution volume `V` (L):

```
C_nM = 1e6 · F · D / (M · V)                    # concentration (nM)
p(C) = E0 + Emax · C / (EC50 + C)               # Emax exposure–response
C_µM = 1e3 · F · D / (M · V)                    # generated PK peak-concentration proxy (µM)
```

Probabilities are rounded to three decimals before the dose rule is applied to produce the label — so **oracle agreement with generated labels is a construction property, not independent validation.** These equations are simplified instantaneous-distribution quantities (no absorption kinetics, clearance, or accumulation) and must not be called steady-state or validated oral-peak predictions.

**Free-energy scorer (N1).** For a ligand and designated reference in the same series, `ΔΔG = ΔG_ligand − ΔG_reference`. The scorer reports RMSE, mean unsigned error, Kendall-τ and Spearman rank measures, and the fraction within 1 kcal·mol⁻¹. A **reference-perfect input scores ≈0.98 on the composite** (not 1.0) because tied experimental values deflate Kendall-τ-a — a disclosed scorer property, not prediction error. The ML variant specifies **leave-target-out** partitioning.

**A known scorer limitation (flagged, not hidden).** In a no-dose reference case, an absent dose field can currently receive credit even without an explicit valid no-dose declaration; probability bounds and contradictory output fields are not comprehensively validated. Recorded scores are **preserved as-is**, not silently recalculated — hence "provisional."

---

## Selected experiments (provisional — read the caveats)

These are the measurements actually recorded. They are **run-level observations on specific tiers**, not a suite-wide model ranking. See `leaderboard.md` / `leaderboard.csv` and the paper's Methods for the exact protocol and its open issues.

### Dose selection — structured responses, two tiers of 20 scenarios each (Table 1)

| Model / reference | Hand outcome | Hand fidelity | Hand empties | Generated outcome |
|---|---|---|---|---|
| **Oracle** (hidden toxicity curve) | **0.85** | 1.00 | — | 1.00 *by construction* |
| Claude Opus 5 | 0.25–0.30 | 0.60–0.68 | 0 | 0.95–1.00 |
| GPT-6.1-sol | 0.10 | ≈0.01 | 1–4 | 1.00 |
| Stock Qwen3.5-9B | 0.30 | 0.58 | 0 | 0.30 |
| BioMate 9B continued-pretrained | 0.50 | 0.74 | 0 | 0.05 |
| BioMate 9B fine-tuned | 0.30 | 0.31 | 0 | 0.10 |

Ranges are across **retained runs, not confidence intervals.** Local models use reasoning-disabled serving. The oracle receives **privileged** curve information and is not a model given the same inputs; its 17/20 agreement **diagnoses disagreements between reference labels and the implemented policy** (two concern no-safe-dose labels not triggered by the elimination threshold; one concerns a closest-to-target vs. higher-dose choice) — it is **not** an upper bound or an end-to-end score. The hand/generated reversal of the continued-pretrained 9B model (0.50 → 0.05) argues **against** a simple capability ordering.

### Pharmacokinetics — within-twofold agreement, 15 hand-authored compounds (Table 2)

Endpoint = benchmark peak concentration (µM); a prediction succeeds when its ratio to the reference lies in **[0.5, 2.0]**. Missing/unparseable predictions count as failures.

| Model | Within twofold |
|---|---|
| Claude Opus 5 | **0.467** |
| Gemini 3.1 Pro | 0.400 |
| GPT-5.6-luna | 0.333 |
| GLM-5.2 | 0.267 |
| GPT-5.6 | 0.200 |
| DeepSeek V4-pro | 0.067 |
| BioMate 9B (base) | 0.067 |
| Qwen3.8-Max | 0.000 |
| Qwen3.8-27B | 0.000 |
| Kimi K3 | 0.000 |
| BioMate 9B (SFT) | 0.000 |
| Biomni (A1 scaffold) | 0.000 |

This is **agreement with benchmark references**, not clinical prediction accuracy. Generated PK cases and earlier endpoint-ambiguous runs are excluded.

### Ligand ranking (B2) — complementary but coarse

The historical shared export includes **15 ligand-ranking items** and reports **mean Spearman 0.696 across eight direct-model systems.** A domain-agent value of 1.0 covers only **four completed cases** and is **not** a full-set result. With only three ligands per ranking item, possible correlations are coarse; this is evidence about a small ranking task — not docking-pose accuracy or prospective affinity prediction.

### Offline validation (Table 3) — implementation contracts, not science

| Component | Reported check | Interpretation |
|---|---|---|
| Relative free-energy scorer | 6/6 | Numeric & ranking score behaviour |
| Decision scorers | 15/15 | Decision-format & matching behaviour |
| Chain scorer | 5/5 | Coverage, ordering, gate logic |
| Decision adapter | 14/14; exemplar 7/7 | Dispatch & prompt-construction checks |
| Synthesized gold completions | 30/30 at score 1.0 | Internal consistency with the scorer |
| Training reward checks | 22/22 training items | Gold-vs-trivial-wrong ordering |
| Free-energy oracle input | RMSE 0; composite ≈0.98 | Tie-sensitive composite behaviour |

These are **self-tests of implementation contracts** — they do **not** establish reference-label validity or model generalization.

### Execution-track composer diagnostics (offline)

Over **68 workflow topologies**: under a perfect-decomposition assumption, every subtask clears the resolver's confidence threshold, yet agreement with **fine-grained gold tool identities is only 4%** (a granularity mismatch — workflow-level units vs. individual Galaxy tools). Separately, **66% of catalogued workflows use free-text parameter descriptions** where structured input-type tokens are expected, blocking them as handoff destinations; replacing exact-string with the specified **semantic matcher raises the handoff fire rate from 4.4% to 38.2%.** These are **resolver/handoff diagnostics, not success rates** for complete programmes.

---

## Key takeaways (faithful to what was measured)

1. **Task construction dominates the result.** Exact dose agreement for Claude Opus 5 moves from **0.25–0.30** (hand-authored) to **0.95–1.00** (generated) — the generated task is *not* uniformly unsolved by LLMs; the contrast reflects sensitivity to specification, not a single causal factor.
2. **Specified calculations ≠ validated science.** High fidelity under a coarse metric, or RMSE 0 on a scorer's own oracle input, confirms *implementation consistency* — not mechanistic or clinical correctness.
3. **Evidence types must stay separate.** Experimental ΔΔG, reference formulas, model-derived curves, and provisional class-level values each need their own validation; internal scorer agreement cannot stand in for physiological accuracy.
4. **Execution is the open frontier.** Confident matching can pick the wrong level of abstraction, and a compatible type label can hide an incompatible representation (a count matrix vs. an `ExpressionSet`). A completed execution study must verify files, terminal state, transformations, and endpoints — neither a correct plan nor a high handoff rate suffices.
5. **The numbers are provisional by design.** They are preserved as recorded, with their scorer limitations disclosed, so the community can inspect and re-adjudicate rather than inherit a polished-but-unchecked ranking.

---

## Run your own system

```bash
# produce predictions.jsonl per component — {"id": ..., "prediction": <answer>} — then:
python3 src/score.py dose   my_system/dose.jsonl        # deterministic reference-curve policy
python3 src/score.py pbpk   my_system/pbpk.jsonl        # within-twofold on peak concentration (µM)
python3 src/score.py fep    my_system/fep.jsonl         # ΔΔG RMSE / MUE / Kendall / Spearman / f(<1 kcal)
# scoring entry points: decision · categorical · set · numeric · dose · chain
```

The scorer is deterministic and judge-free; any result you produce is directly comparable to the (provisional) numbers above **on the same items under the same policy**.

---

## Citation

```bibtex
@misc{drugdevbench2026,
  title  = {DrugDev-Bench: an inspectable benchmark for drug-development decisions
            from molecular discovery to dose selection},
  author = {Zhang, Yaoyun and Dike, Andrew},
  year   = {2026},
  note   = {BioMate AI · BizBildr. Preprint, 7 November 2026},
  url    = {https://github.com/bioMate-AI/drugdev-benchmark}
}
```

## Ground-truth sources (external references)
- **Relative free energy (N1)** — Schindler et al., *J. Chem. Inf. Model.* 60, 5457–5474 (2020); data: [MCompChem/fep-benchmark](https://github.com/MCompChem/fep-benchmark).
- **Dose / trials context** — Liu & Yuan, *JRSS-C* 64, 507–523 (2015); Yuan et al., *Clin. Cancer Res.* 22, 4291–4301 (2016). *(BOIN motivates the setting; the implemented rule is a simplified reference-curve policy, not BOIN.)*
- **Landscape** — Therapeutics Data Commons (Huang et al., NeurIPS D&B 2021); TrialBench (Chen et al., *Sci. Data* 2025); ScienceAgentBench (Chen et al., ICLR 2025).

## Ethics & competing interests
A **nonclinical methodological benchmark.** Modeled dose/exposure references are **not** dosing recommendations, and internal consistency is **not** clinical validation. The authors also develop **BioMate**, an evaluated system; Y.Z. and A.D. are affiliated with BioMate AI, and A.D. is additionally affiliated with BizBildr. Declared as competing financial interests.

## License
**CC-BY-4.0** — datasets, scorers, adapters, and documentation. See [`LICENSE`](LICENSE). Experimental free-energy data are attributed to the Merck/Schindler collection; other components retain their own reference and licensing records.

---
Built by **[BioMate AI](https://biomate.ai)** · sibling benchmark: **[RealBio](https://github.com/bioMate-AI/realbio-benchmark)**
