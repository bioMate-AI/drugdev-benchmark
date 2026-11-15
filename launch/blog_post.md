# DrugDev-Bench: can an AI make a *drug-development decision* — not just predict a number?

*BioMate AI · with BizBildr · preprint 7 November 2026*

A model can predict a binding affinity, flag a toxicity, estimate a concentration — and still be unable to answer the question a drug-development team actually asks: *given all of that, what do we do next?* Advance this analogue or kill it? Is exposure high enough? Which dose do the next patients get? Those are **decisions under constraints**, and a correct property prediction is only an input to them, never a substitute.

Today we're releasing **DrugDev-Bench**, an open benchmark built around that gap — and built, deliberately, to be *inspected* rather than to crown a winner.

## Three things made explicit for every task

Most drug-discovery benchmarks score one property endpoint in isolation. DrugDev-Bench instead makes three things explicit for every item:

1. **The information the solver is given** — and, crucially, what is *hidden* from it.
2. **The policy that defines a correct decision** — written down, deterministic, checkable.
3. **The evidence required to confirm the decision was executed** — not merely described fluently.

A fourth commitment runs underneath all of it: **different kinds of ground truth are not interchangeable.** Experimental affinity data, closed-form reference formulas, model-derived toxicity curves, curated policy labels, and provisional class-level values each support different claims. DrugDev-Bench keeps them labeled as such instead of blending them into a single headline score.

## What's in it

DrugDev-Bench is organized into four tracks — molecular-tool workflows, targets and perturbations, search and knowledge, and cross-stage execution. The instantiated, documented components in this release are:

- **Five stage benchmarks:** ADMET (20 compounds), docking/ligand ranking (15 items), PK (15 hand-authored cases), dose selection (20 hand-authored scenarios), and target structure (10 targets).
- **A relative binding free-energy dataset** reusing the Merck/Schindler collection — **8 congeneric series, 264 ligands** with experimental affinity-derived ΔΔG.
- **A 30-item decision suite** across nine recurring project archetypes (lead-optimization triage, FEP selection, dose escalation, dose projection, tissue exposure, dose schedule, special populations, process knowledge, workflow chains), with a 22/8 train/eval split.

Everything is scored by **one deterministic scorer — no LLM judge** — with six entry points (decision, categorical, set, numeric, dose, chain). The two fully-specified policies, the dose-selection rule and the generated-tier exposure formulas, are implemented in the open `score.py`, so any team's predictions re-score identically.

## The finding that matters most: construction dominates the result

Here's the result we most want people to sit with. On dose selection, we ran two tiers of 20 scenarios — hand-authored and generated. Claude Opus 5 scored **0.25–0.30 exact agreement on the hand-authored tier** and **0.95–1.00 on the generated tier.** Same model, same metric; the task changed, and the score swung across almost the whole range.

That is not a story about one model being good or bad. It's a warning: **a benchmark's construction can dominate its conclusions.** The generated tier derives its toxicity curves and labels from the same explicit equations — so an "oracle" with access to those equations matches them by *construction*, not by discovering anything. Report only the generated tier and you'd declare the task solved; report only the hand-authored tier and you'd declare it unsolved. Both would be misleading. We report both, side by side, and refuse to pool them.

The pharmacokinetics track tells a companion story. After we pinned the endpoint to peak concentration in micromolar, the best within-twofold agreement across a dozen systems was **0.467** (Claude Opus 5). That's agreement with a benchmark reference — explicitly *not* clinical accuracy, and the underlying formula models neither absorption nor elimination. Calling it a "validated PBPK simulator" would be wrong, so we don't.

## We flag our own limitations in the open

An oracle with the hidden toxicity curve matched **17 of 20** hand-authored dose labels — and the three disagreements turned out to expose places where the *reference labels* and the *implemented policy* disagree, not where a solver erred. We also found a scorer edge case: in a no-dose scenario, an absent dose field could receive credit without an explicit no-dose declaration. Rather than silently rescoring, we **preserved the recorded numbers and marked them provisional.** The offline validation we do report — 6/6, 15/15, 5/5, 14/14, 30/30, 22/22 — checks *implementation contracts*, and we say plainly that it does **not** establish reference-label validity or model generalization.

The execution track makes the open frontier concrete. Across 68 workflow topologies, confident matching cleared the resolver's threshold yet agreed with fine-grained gold tool identities only **4%** of the time — it was picking the wrong *level of abstraction*. A compatible type label can still hide an incompatible scientific representation (a count matrix vs. an `ExpressionSet`). Raising a handoff "fire rate" from 4.4% to 38.2% with a smarter matcher is progress, but it is **not** a success rate for a completed programme.

## Try it, and tell us where we're wrong

DrugDev-Bench is **CC-BY-4.0**: datasets, scorers, adapters, documentation, and the paper. Run your own system against the fixed items and the open scorer, and your number is directly comparable — on the same items, under the same written policy. And because every reference policy and known limitation is in the open, the most useful contribution you can make is to find the one we missed.

**Code & paper:** github.com/bioMate-AI/drugdev-benchmark · **Sibling benchmark:** RealBio.

*Nonclinical methodological benchmark. Modeled dose/exposure references are not dosing recommendations. The authors also develop BioMate, an evaluated system — declared competing interest.*
