---
license: cc-by-4.0
---
# DrugDev-Bench — Decision suite (30 tasks, 9 archetypes)

**Scope.** 30 decision tasks across nine archetypes (counts sum to 30). Each item presents a project
context, inputs, constraints, and a required decision; **the reference conclusion is hidden from the prompt.**
**Split.** 22 train / 8 evaluation, template-separated, with a fail-closed overlap guard.
**Scoring.** six entry points in `../src/score.py` — `decision`, `categorical`, `set`, `numeric`, `chain`
(decision = deprioritization-set F1 + best-pick agreement + liability/driver identification).

| Archetype | Tasks | Decision | Reference basis |
|---|---:|---|---|
| C Lead-optimization triage | 3 | Advance/deprioritize analogues; identify liability | ADMET inputs + project policy |
| E FEP selection | 2 | Rank binders, select candidates | Experimental relative free energy |
| H Dose escalation | 3 | Select MTD and safety flags | Benchmark dose-selection policy |
| F1/G Dose projection | 3 | Starting-dose / human-clearance estimate | MRSD formula + allometric assumptions |
| F2 Tissue/organ exposure | 3 | Assess target-site exposure | Unbound-partition / class-level *(provisional)* |
| F3 Dose schedule | 3 | Choose regimen from PK/PD driver | Curated PK/PD class |
| F4 Special populations | 4 | Adjust for organ impairment/interactions | Label-derived / provisional class values |
| P Process knowledge | 6 | Identify gates and prerequisites | Curated development-process references |
| W Workflow chain | 3 | Order stages, enforce gates | Reference directed acyclic graph |

> **Caution.** Reference bases are **mixed and kept labeled**; F2/F4 include provisional values requiring
> source verification. The 22/8 split reduces template leakage but does not establish independence across
> compounds, targets, formulas, or authoring conventions. The 264 free-energy ligands are **separate** and
> are **not** added to this 30-item denominator.

**Data.** `data.jsonl` ships with the suite package.
