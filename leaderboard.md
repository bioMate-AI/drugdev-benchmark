# DrugDev-Bench — selected experiments (PROVISIONAL)

> These are **run-level observations on specific tiers**, not a suite-wide model ranking.
> Ranges are across **retained runs, not confidence intervals.** Scores are **provisional**
> pending the scorer and reference-policy reconciliation in the paper (Methods). All values
> are transcribed from the manuscript (`paper/drugdev.pdf`, Tables 1–2 and the ligand-ranking
> export). No value is fabricated; anything not reported in the manuscript is marked `n/r`.

## Dose selection — structured responses (Table 1)
Two separate tiers, 20 scenarios each. The oracle receives the **hidden toxicity curve** (privileged
information) and is not a model given the same inputs. Local models use reasoning-disabled serving.

| Model / reference | Hand outcome | Hand fidelity | Hand empties | Generated outcome |
|---|---|---|---|---|
| Oracle (hidden curve) | 0.85 | 1.00 | — | 1.00 (by construction) |
| Claude Opus 5 | 0.25–0.30 | 0.60–0.68 | 0 | 0.95–1.00 |
| GPT-6.1-sol | 0.10 | ≈0.01 | 1–4 | 1.00 |
| Stock Qwen3.5-9B | 0.30 | 0.58 | 0 | 0.30 |
| BioMate 9B continued-pretrained | 0.50 | 0.74 | 0 | 0.05 |
| BioMate 9B fine-tuned | 0.30 | 0.31 | 0 | 0.10 |

Additional retained generated-tier runs reaching 1.00 outcome / 1.00 fidelity (no empties): one run each of
Claude Opus 5, GPT-6.1-sol, and Gemini 3.1 Pro; three further Opus runs scored 1.00, 1.00, 0.95.

## Pharmacokinetics — within-twofold, 15 hand-authored compounds (Table 2)
Endpoint = benchmark peak concentration (µM); success = ratio to reference in [0.5, 2.0]; missing = failure.

| Model | Within twofold |
|---|---|
| Claude Opus 5 | 0.467 |
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

## Ligand ranking (B2) — complementary but coarse
Historical shared export: **15 items**, **mean Spearman 0.696 across eight direct-model systems.**
A domain-agent value of 1.0 covers only **four completed cases** and is **not** a full-set result.
Per-system ligand-ranking values are **not reported** in the manuscript (`n/r`).

## Offline validation (Table 3) — implementation contracts only
| Component | Reported check |
|---|---|
| Relative free-energy scorer | 6/6 |
| Decision scorers | 15/15 |
| Chain scorer | 5/5 |
| Decision adapter | 14/14 (exemplar 7/7) |
| Synthesized gold completions | 30/30 at score 1.0 |
| Training reward checks | 22/22 training items |
| Free-energy oracle input | RMSE 0; composite ≈0.98 |

## Execution-track composer diagnostics (offline, 68 topologies)
- Perfect-decomposition passes resolver threshold, yet only **4%** agreement with fine-grained gold tool identities.
- **66%** of catalogued workflows use free-text parameter descriptions (block handoff destinations).
- Semantic matcher raises handoff fire rate **4.4% → 38.2%**.
These are resolver/handoff diagnostics, **not** success rates for complete programmes.
