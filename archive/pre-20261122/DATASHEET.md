# DrugDev-Bench — Dataset datasheet

Documentation for DrugDev-Bench (following the *Datasheets for Datasets* spirit). The source of truth is the manuscript at [`paper/drugdev.pdf`](paper/drugdev.pdf); where this datasheet and the paper differ, the paper governs.

## Motivation

Accurate predictions of individual molecular properties are useful inputs, but they do not establish that an agent can integrate those predictions into a defensible **project decision**. DrugDev-Bench was built to make three things explicit for every task: (1) the **information available to the solver**, (2) the **policy defining a correct decision**, and (3) the **evidence required to confirm execution** rather than mere description. A second motivation is to keep **different kinds of ground truth labeled and non-interchangeable**: experimental affinity data, reference formulas, model-derived curves, curated policy labels, and provisional class-level values are not the same form of evidence.

DrugDev-Bench builds on an extensive external ecosystem (Therapeutics Data Commons, TrialBench, molecular-property / docking / free-energy / retrieval resources). Its contribution is the **organization of development decisions and execution checks**, not a claim that drug-development or dose-finding benchmarks were previously absent.

## Composition

The suite is organized into **four tracks** (T1 molecular workflows; T2 targets & perturbations; T3 search & knowledge; T4 cross-stage execution). **Track membership is a design classification — not a statement that every task has a completed model sweep.** The instantiated, documented components are:

| Component | Scope | Ground-truth basis | Evidence type |
|---|---|---|---|
| **B1 ADMET** | 20 compounds | Curated property/toxicity labels: hERG, DILI, Ames-related, rule-of-five descriptors | Mixed; **provenance differs by endpoint** — a rule-of-five calculation is *not* a measured assay |
| **B2 Docking & ligand assessment** | 15 shared items | Structural/affinity references; reported endpoint = ligand ranking | Structural/affinity-derived |
| **B3 PK** | 15 hand-authored cases | Numeric peak-concentration reference (µM), units specified by protocol | Numeric reference; hand-authored provenance needs separate source/unit verification |
| **B4 Dose selection** | 20 hand-authored scenarios | Policy-based dose / no-dose labels (deterministic reference-curve rule) | Curated policy label |
| **B5 Target structure** | 10 targets | Sequence/structure inputs + pocket-residue references | Structural reference |
| **Protocol-QC** *(new; moved from RealBio)* | 100 items | Public accessions (GEO/PRIDE/EMDB) + expert VALID/DEFECTIVE labels; exact PASS/WARN/FAIL action | Expert-labeled against public data |
| **N1 Relative binding free energy** | 8 congeneric series · 264 ligands | Experimental affinity-derived ΔΔG | **Experimental** (Merck/Schindler) |
| **Decision suite** | 30 tasks · 9 archetypes | Mixed: measured inputs, formulas, curated policies, provisional class values | Mixed (kept labeled) |
| **Generated dose tier** | 20 scenarios | Closed-form `C_nM` + Emax `p(C)`, then dose rule | Derived formula |
| **Generated PK tier** | 15 cases | Closed-form `C_µM` proxy | Derived formula |
| **Seeds (S2)** | 2 items each: QSAR, retrosynthesis, target-ID | Instantiated task seeds | Seed-only; **no inferential ranking** |

**Totals.** Dose: 20 hand-authored + 20 generated = 40. PK: 15 hand-authored + 15 generated = 30. **Protocol-QC: 100 items (new; moved from RealBio).** **Counts describe available datasets; they do not imply every model was evaluated on every tier.** The decision suite's 22/8 train/eval split applies to its 30 items only; the 264 free-energy ligands are a separate component and are not added to the 30-item denominator.

**Clinical-pharmacology tracks moved from RealBio (PBPK, BOIN, Protocol-QC).** Three tasks were moved into
DrugDev-Bench together with their cross-system results (RealBio paper, same-item Supplementary Table S1), and
removed from the RealBio public repo in the same transfer. **PBPK and BOIN are not new item sets** — they are
the **same-item historical (endpoint-ambiguous / dose-only) protocol versions** of the existing B3 PK and B4
dose tracks, and the manuscripts forbid pooling them with the endpoint-specified / structured-response
protocols (different denominators: PBPK 15, BOIN 18-scorable-of-20). **Protocol-QC (100 items) is genuinely
new.** These three ship **runnable `data.jsonl`** plus their source `*.source.yaml`. Canonical cross-system
figures: **PBPK ceiling 0.200** (8-model mean 0.075; the earlier 1.00 was a non-comparable task and is
dropped), **BOIN mean 0.271**, **Protocol-QC 0.330–0.630** (Gemini highest; the earlier `0.925` figure is not
in the manuscript and is not used).

## Collection & labeling

- **N1 free energy** reuses the **Merck/Schindler FEP benchmark** (8 series, 264 ligands); `ΔΔG = ΔG_ligand − ΔG_reference` within a series.
- **B1–B5** are authored from public property, structural, and pharmacology sources, with provenance retained at the component level (ADMET endpoints in particular mix measured assays with computed descriptors).
- **Decision suite** items present a project context, inputs, constraints, and a required decision; the reference conclusion is hidden from the prompt. Labels combine measured inputs, formulas, and curated policy; **F2 tissue/organ and F4 special-population references include provisional class-level values requiring source verification before definitive benchmarking.**
- **Generated tiers** are produced by closed-form equations and the dose-selection rule; because the oracle uses the same formula/policy that created the labels, **its agreement there is a construction property, not independent validation.**

## Scoring

One deterministic scorer (`src/score.py`), **no LLM judge**, with **six entry points**: decision, categorical, set, numeric, dose, chain.
- **Dose:** declare no-dose if `p_1 > τ + 0.10`; else pick admissible (`p_j ≤ τ + 0.10`) dose minimizing `|p_j − τ|`; ties pick the higher index.
- **Numeric/PK:** full credit within a specified fold band (PK uses within-twofold, ratio ∈ [0.5, 2.0]); partial credit within the squared band; missing/unparseable = failure.
- **Free energy:** RMSE, MUE, Kendall-τ, Spearman, fraction within 1 kcal·mol⁻¹, and a composite; a reference-perfect input scores ≈0.98 (tie-sensitive Kendall-τ-a), which is disclosed, not treated as error.
- **Chain:** stage coverage + longest-common-subsequence ordering + before/after gate adherence.
- **Decision:** deprioritization-set F1 + best-pick agreement + liability/driver identification.

## Known limitations (flagged, not hidden)

- **Dose scorer gap:** in a no-dose reference case, an absent dose field can currently receive credit without an explicit valid no-dose declaration; probability bounds and contradictory fields are not comprehensively validated. **Recorded scores are preserved, not silently recalculated — hence "provisional."**
- **Two dose protocols are not pooled:** a historical dose-only leaderboard scores 18 non-null labels; the structured-response study includes all 20 outcomes. They use different denominators and are retained separately.
- **Simplified exposure math:** generated `C_nM`/`C_µM` are instantaneous amount-over-volume quantities — no absorption kinetics, clearance, or accumulation. They are **not** steady-state or validated oral-peak predictions, despite any "peak concentration" labeling.
- **Dose policy ≠ BOIN:** the deterministic reference-curve rule does not simulate sequential allocation or BOIN's elimination/final-selection; the 0.10 band is a benchmark choice.
- **PBPK lineage label (B3):** simple numeric endpoints; **not** a validated PBPK simulator.
- **Small denominators:** dose (20/tier), PK (15), ligand ranking (15, 3 ligands/item), decision suite (30). These do not support fine-grained model rankings or causal claims about scale/reasoning.
- **Provisional class-level references** (F2/F4, tissue exposure, special populations) require source verification before definitive benchmarking.
- **Serving-condition ambiguity:** source drafts report a 20,000-token budget for later structured-response runs vs. a superseded 12,000-token scorecard; per-run manifests are needed to attribute budgets. Local models use reasoning-disabled serving.

## Scope of evidence in this release

- **Offline validation** (Table 3) establishes scorer/adapter/export **implementation contracts** — not reference-label validity or model generalization.
- **Selected model experiments** (dose, PK, ligand ranking) are **run-level observations on specific tiers**, provisional pending scorer/reference-policy reconciliation.
- **Execution track (T4)** is specified and exercised via **offline composer diagnostics** (68 topologies); there is **no completed roster-wide execution result.**
- **Tracks T2/T3 and several S2 extensions** are design-level in this release, with external comparison families identified but **not** run on DrugDev-Bench.

## Uses & distribution

Intended for **inspectable, policy-explicit evaluation of drug-development decision-making** by AI systems. This is a **nonclinical methodological benchmark**; modeled dose/exposure references are not dosing recommendations. Released **CC-BY-4.0**; the Merck/Schindler free-energy data retain their original attribution/license. A verified archival identifier (e.g., Zenodo DOI) is **not yet** asserted in the preprint and will be added when available.
