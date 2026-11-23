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

- **Five stage benchmarks** (ADMET, docking/ligand ranking, PK, dose selection, target structure) plus a **100-item Protocol-QC** track, a **264-ligand** Merck/Schindler free-energy dataset, and a **30-item decision suite** across nine project archetypes (22/8 train/eval split).

Everything is scored by **one deterministic scorer — no LLM judge** — now including `pbpk`, `boin`, and `protocol` entry points. The fully-specified policies (the dose-selection rule, the generated-tier exposure formulas) are implemented in the open `score.py`, so any team's predictions re-score identically.

## The finding that matters most: construction dominates the result

Here's the result we most want people to sit with. On dose selection, we ran two tiers of 20 scenarios — hand-authored and generated. Claude Opus 5 scored **0.25–0.30 exact agreement on the hand-authored tier** and **0.95–1.00 on the generated tier.** Same model, same metric; the task changed, and the score swung across almost the whole range.

That is not a story about one model being good or bad. It's a warning: **a benchmark's construction can dominate its conclusions.** The generated tier derives its toxicity curves and labels from the same explicit equations — so an "oracle" with access to those equations matches them by *construction*, not by discovering anything. Report only the generated tier and you'd declare the task solved; report only the hand-authored tier and you'd declare it unsolved. Both would be misleading. We report both, side by side, and refuse to pool them.

## Where frontier models fail hardest: the clinical-pharmacology bench

This release folds in three clinical and quality-control tasks — **PBPK** (drug-exposure prediction), **BOIN** (Phase I dose-finding), and **Protocol-QC** (sequencing-QC gating) — with their full cross-system, same-item leaderboard. The pattern is stark and it matters: **frontier LLMs used directly fail worst exactly where an error is most costly.** On PBPK, the mean within-twofold agreement is **0.075**, and **no system clears a 0.200 ceiling** — GPT-5.6, GPT-5.6-luna, and a curated-retrieval system all tie there, and nothing beats it. On BOIN dose-finding the mean is **0.271**. These aren't knowledge questions a model can talk its way through; they're *execution* — predict the exposure, pick the dose — and that's where fluency runs out. Protocol-QC gating lands higher, 0.330 to 0.630 (Gemini 3.1 Pro leads), but still nowhere near dependable. We use the canonical **0.200** PBPK ceiling here and explicitly drop an earlier 1.00 result that came from a different, non-comparable task — the kind of number that looks like a headline and isn't one. (Pin the endpoint — name "peak concentration in micromolar" — and the best score rises to 0.467; we keep that as a *separate* protocol and never pool it with the 0.200 ceiling.)

## We flag our own limitations in the open

An oracle with the hidden toxicity curve matched **17 of 20** hand-authored dose labels — and the three misses exposed places where the *reference labels* and the *implemented policy* disagree, not where a solver erred. We found a scorer edge case too, and rather than silently rescoring, we **preserved the recorded numbers and marked them provisional.** The execution track stays just as honest: across 68 workflow topologies, confident matching agreed with fine-grained gold tool identities only **4%** of the time — picking the wrong *level of abstraction*, not a success rate for a completed programme.

## Try it, and tell us where we're wrong

DrugDev-Bench is **CC-BY-4.0**: datasets, scorers, adapters, documentation, and the paper. Run your own system against the fixed items and the open scorer, and your number is directly comparable — on the same items, under the same written policy. And because every reference policy and known limitation is in the open, the most useful contribution you can make is to find the one we missed.

**Code & paper:** github.com/bioMate-AI/drugdev-benchmark · **Sibling benchmark:** RealBio.

*Nonclinical methodological benchmark. Modeled dose/exposure references are not dosing recommendations. The authors also develop BioMate, an evaluated system — declared competing interest.*
