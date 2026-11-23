# DrugDev-Bench — social collateral (DRAFT — not posted)

---

## LinkedIn post

**A model can predict a binding affinity, flag a toxicity, estimate a concentration — and still not be able to answer the question a drug-development team actually asks: given all of that, what do we do next?**

Today we're releasing **DrugDev-Bench**, an open benchmark for drug-development *decisions* — advance or kill an analogue, is exposure enough, which dose do the next patients get — not isolated property predictions.

Three things we make explicit for every task:
→ the information the solver is given (and what's hidden from it)
→ the policy that defines a correct decision (written down, deterministic)
→ the evidence that the decision was *executed*, not just described fluently

The headline finding: **frontier LLMs used directly fail worst on clinical-pharmacology execution — exactly where errors are most costly.** On PBPK drug-exposure prediction, the cross-system mean is **0.075** within-twofold and **no model clears a 0.200 ceiling**; on BOIN Phase I dose-finding the mean is **0.271**. Predicting an exposure or picking a trial dose is *execution*, and that's where fluency runs out.

A second finding worth sitting with: on dose selection, the *same* model (Claude Opus 5) scored **0.25–0.30 on hand-authored scenarios and 0.95–1.00 on generated ones.** Same metric. The task construction changed — and it swung the conclusion across almost the entire range.

That's the whole point. A benchmark's construction can dominate its result, so we report both tiers side by side, keep different kinds of ground truth (experimental vs. formula vs. curated policy) labeled and separate, score everything with **one deterministic scorer — no LLM judge**, and flag our own scorer limitations in the open rather than quietly rescoring.

Four tracks. Five stage benchmarks + a 100-item Protocol-QC track. 264-ligand free-energy set. A 30-task decision suite across nine archetypes. Deterministic `pbpk` / `boin` / `protocol` scorers ship with runnable data. CC-BY-4.0 — datasets, scorer, and paper.

It's built to be *inspected*, not to crown a winner. Run your system, and tell us where we're wrong.

🔗 github.com/bioMate-AI/drugdev-benchmark

*Nonclinical methodological benchmark — modeled dose/exposure values are not dosing recommendations. We also build BioMate, an evaluated system (declared competing interest).*

#DrugDiscovery #AIinPharma #Benchmarks #Pharmacokinetics #MachineLearning #ClinicalPharmacology

---

## X / Twitter thread

**1/**
A model can predict an affinity, a toxicity, a concentration — and still not answer the real question: given all that, what do we do next?

Introducing **DrugDev-Bench**: an open benchmark for drug-development *decisions*, not isolated property predictions. 🧵

**2/**
For every task we make 3 things explicit:
• the info the solver gets (and what's hidden)
• the policy that defines a correct decision
• the evidence it was *executed*, not just described fluently

One deterministic scorer. No LLM judge.

**3/**
The headline finding 👇

Frontier LLMs used directly fail worst on clinical-pharmacology *execution*:
• PBPK drug-exposure: mean **0.075** within-2×, nothing clears a **0.200** ceiling
• BOIN dose-finding: mean **0.271**

Exactly where a wrong answer mis-doses a trial.

**3b/**
(Canonical PBPK ceiling = 0.200. An earlier 1.00 came from a different, non-comparable task — we drop it. Pin the endpoint and the best rises to 0.467, kept as a *separate* protocol, never pooled.)

**4a/**
Second finding to sit with — same model (Claude Opus 5), same metric, dose selection:
• hand-authored → **0.25–0.30**
• generated → **0.95–1.00**

Task construction swung the conclusion across almost the whole range.

**4/**
So we refuse to pick the flattering tier. We report both, side by side, and never pool them.

An "oracle" with the generating equations matches generated labels *by construction* — that's not discovery, and we say so.

**5/**
PK track: after pinning the endpoint to peak concentration (µM), best within-twofold agreement across 12 systems was **0.467**.

That's agreement with a reference — NOT clinical accuracy, and NOT a validated PBPK simulator. We don't call it one.

**6/**
We flag our own limits in the open:
• an oracle hit 17/20 — and the 3 misses exposed reference-label vs. policy disagreements
• a no-dose scorer edge case → scores kept + marked PROVISIONAL, not silently rescored

**7/**
Whole thing is CC-BY-4.0: 4 tracks, 5 stage benchmarks, a 264-ligand free-energy set, a 30-task decision suite across 9 archetypes, the deterministic scorer, and the paper.

Built to be inspected, not to crown a winner.

**8/**
Run your system on the fixed items + open scorer → directly comparable numbers, same policy.

The best contribution you can make is finding the limitation we missed.

🔗 github.com/bioMate-AI/drugdev-benchmark
