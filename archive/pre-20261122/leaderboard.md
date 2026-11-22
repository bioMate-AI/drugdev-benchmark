# DrugDev-Bench — selected experiments (PROVISIONAL)

> These are **run-level observations on specific tiers**, not a suite-wide model ranking.
> Ranges are across **retained runs, not confidence intervals.** Scores are **provisional**
> pending the scorer and reference-policy reconciliation in the paper (Methods). Values are
> transcribed from the manuscripts (`paper/drugdev.pdf`, Tables 1–2; and the RealBio paper's
> same-item Supplementary Table S1 for the moved clinical tracks). No value is fabricated;
> anything not reported is marked `n/r`, and computed means are labeled as such.

## ⭐ Clinical-pharmacology & QC cross-system leaderboard (moved from RealBio)

These three tasks — **PBPK** (drug-exposure prediction), **BOIN** (trial dose-finding), and
**Protocol-QC** (sequencing-QC gating) — were moved **into DrugDev-Bench** from RealBio, together
with their cross-system results. Values are the **same-item historical comparison** (RealBio paper,
Supplementary Table S1), scored by the deterministic scorers now in `src/score.py` (no LLM judge).

| System | Protocol-QC (n=100) | PBPK within-2× (n=15) | BOIN exact-dose (n=18) |
|---|---:|---:|---:|
| Claude Opus 5 | 0.330 | 0.133 | 0.444 |
| Gemini 3.1 Pro | **0.630** | 0.000 | 0.278 |
| GPT-5.6 | 0.460 | **0.200** | **0.500** |
| GPT-5.6-luna | 0.340 | **0.200** | 0.389 |
| Qwen3.8-Max | 0.460 | 0.000 | 0.111 |
| GLM-5.2 | 0.440 | 0.000 | 0.111 |
| Kimi K3 | 0.360 | 0.000 | 0.167 |
| DeepSeek V4-pro | 0.420 | 0.067 | 0.167 |
| Biomni (Stanford A1) | 0.500 | 0.000 | **0.500** |
| BioMate (engine-free curated retrieval) | n/r | **0.200** | n/r |
| **8-direct-model mean** | 0.430 *(computed)* | **0.075** | **0.271** |

**The finding (now housed here).** Frontier LLMs used directly **fail worst on the clinical-pharmacology
computations.** On **PBPK**, the mean within-twofold agreement is **0.075**, and **no system exceeds 0.200**
— GPT-5.6, GPT-5.6-luna and the BioMate retrieval system all **tie at the 0.200 ceiling**. On **BOIN**
dose-finding the mean is **0.271**. These are *execution* tasks, exactly where errors are most costly.

> **Canonical PBPK = 0.200 ceiling.** An earlier PBPK result of **1.00 was a non-comparable task**
> (a different disease-state ratio problem) and is **not** used here. The same-item historical PK ceiling
> is **0.200** (BioMate 3/15; reported Wilson interval 0.071–0.452), tied by two direct models.
>
> **Protocol-QC range 0.330–0.630**, Gemini 3.1 Pro highest. A PASS/WARN/FAIL answer is a decision under
> the benchmark's reference policy, not a complete QC assessment. The `0.925` figure from an earlier public
> draft is **not** in the manuscript Table 1 and is **not** used.
>
> **Two protocol versions per track are never pooled.** PBPK/BOIN here are the *endpoint-ambiguous,
> same-item historical* protocol; DrugDev-Bench's *endpoint-specified* PK (best 0.467, below) and
> *structured-response* dose (below) are distinct protocols with different denominators.

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
