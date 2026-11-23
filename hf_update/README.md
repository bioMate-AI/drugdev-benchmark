---
pretty_name: RealDrug
license: cc-by-4.0
language:
  - en
task_categories:
  - other
tags:
  - benchmark
  - llm-evaluation
  - drug-development
  - deterministic-scoring
configs:
  - config_name: exposure_generated_v2
    data_files:
      - split: validation
        path: data/exposure_generated_v2.jsonl
  - config_name: dose_generated_v2
    data_files:
      - split: validation
        path: data/dose_generated_v2.jsonl
---

# RealDrug

**Evaluating language-model adherence to drug development procedures**

RealDrug compares fixed language-model endpoints with and without a method card on specified exposure-calculation and dose-selection procedures. It separates agreement with a supplied algorithm from independently validated pharmacological prediction. **The current paired study does not execute a scientific workflow, run a full physiological PK simulator or simulate a sequential clinical trial.**

RealDrug is the current benchmark name. DrugDev-Bench and RealPharma are former names; legacy file identifiers are retained for provenance. Protocol-QC and accession-routing studies belong to the companion RealBio benchmark, not to RealDrug's drug-task denominator.
**Code and analyses:** [GitHub](https://github.com/bioMate-AI/realdrug-benchmark) · **Dataset:** [Hugging Face](https://huggingface.co/datasets/YaoyunHug/realdrug_benchmark) · **[Datasheet](DATASHEET.md)** · **[Version changes](CHANGELOG.md)**

## Completed paired comparisons

| Task | Items | Models | Bare | Method card | Difference [95% interval] |
|---|---:|---:|---:|---:|---|
| Exposure calculation: within twofold | 15 | 4 | 0.867 | 1.000 | +0.133 [0.067, 0.217] |
| Emax-rule dose selection: exact agreement | 20 | 5 | 0.940 | 0.980 | +0.040 [−0.020, 0.100] |

These serving-matched comparisons use the same retained endpoint labels, items, 8,000-token output budget and retry handling within each task. Intervals are paired item-bootstrap intervals (10,000 resamples; seed 20261118), conditional on the retained snapshots. The dose interval includes no improvement. The exposure change is carried by Claude and GLM; GPT and Gemini already reach the score ceiling without the card. No overall score pools the two endpoints.

| Model | Exposure bare | Exposure card | Dose bare | Dose card |
|---|---:|---:|---:|---:|
| Claude Opus 5.5 | 0.733 | 1.000 | 1.00 | 1.00 |
| DeepSeek V4-pro | — | — | 0.95 | 0.95 |
| Gemini 3.8 Flash | 1.000 | 1.000 | 1.00 | 1.00 |
| GPT-6.1-sol-pro | 1.000 | 1.000 | 1.00 | 1.00 |
| GLM-5.3-prime | 0.733 | 1.000 | 0.75 | 0.95 |

A dash means the matched cell is unavailable, not a zero score. These endpoint labels identify archived runs; they are not a claim that every provider's latest release was evaluated.

![Agreement with generated procedure references](figures/RealDrug-procedures.png)

## What is being calculated

The exposure reference is `C_uM = 1000 × F × dose_mg / (MW × Vd_L)`. This simplified amount-to-volume proxy does not model absorption, clearance, tissue compartments or an observed clinical peak. The historical `pbpk_benchmark` path is an identifier, not evidence of physiological simulation.

The dose task uses generated Emax toxicity probabilities and a fixed closest-admissible-dose rule: retain doses at or below target + 0.10, select the closest to target, and break ties toward the higher dose. The legacy `boin_benchmark` identifier and BOIN/MTD prompt wording do not turn this into a sequential Bayesian optimal interval trial. **That wording mismatch can disadvantage the bare condition**, while the card provides the operational rule. The exposure card also clarifies the operational endpoint. These contrasts therefore do not isolate pharmacological knowledge alone.

Both reference generators reproduce every stored field of their 15/20-item sets. A procedure oracle scores 1.0 by construction; this establishes internal consistency, not independent biological validity. All 20 evaluated dose references are non-null, so no item is excluded for a null reference. Historical scorer behavior on other null-reference sets remains a limitation. Known errata in the hand-authored PK and dose tiers (a PK unit error, four SMILES that do not encode the named drug, and two null dose labels the declared rule does not reproduce) are listed in [ERRATA.md](https://github.com/bioMate-AI/realdrug-benchmark/blob/main/ERRATA.md); they do not affect the paired results.

An input-independent median exposure scores 0.333. The best single constant can cover at most 7/15 references (0.467), proved by exact overlap of the twofold acceptance intervals. This oracle-selected bound is not a trained deployable baseline. The lowest-dose rule scores 5/20 (0.25). Input-based arithmetic baselines remain relevant.
## Broader resource catalog

The wider drug development program remains important. Its components are retained with their evidence status; their sizes are not added to the paired study's denominator.

| Component | Scope | Evidence status |
|---|---|---|
| ADMET assessment | 20 compounds | Historical unpaired context; assay-source validity needs verification |
| Structured dose selection | 20 hand-authored and 20 generated items | Distinct unpaired tiers; reference-policy disagreements and scorer limits disclosed |
| Ligand ranking | 15 three-ligand items | Historical unpaired context; coarse ranks do not establish prospective affinity prediction |
| Relative binding free energy | 264 ligands in eight series | Scorer-consistency resource; no current paired model-performance claim |
| Decision suite | 30 tasks | Offline scoring/composer resources, not completed scientific trials |
| Cross-stage execution track | 68 topologies | Offline resolver/handoff diagnostics, not a workflow success rate |

See [CATALOG.md](CATALOG.md) and the retained component documentation. The shared reproduction snapshot covers the current paired comparisons; it is not a claim that all historical resource data and predictions have been independently validated or packaged. Experimental, generated and provisional labels must remain distinguishable.

## Interpretation and limitations

The sample sizes are small and template-dependent; the model panel is hand-selected. The study has no length/format-matched method-free control card, no independent observed-pharmacology reference test and no repeated-generation variance estimate. Serving settings match within the retained core, but provider revisions can change over time. Historical unmatched-versus-matched aggregate differences also change the model roster and cannot be assigned solely to serving.

Larger 60-item generated sets exist, but incomplete matched card cells prevent a complete-panel enlarged-set claim. No completed revised-card drug-task transfer result is asserted. Historical scorer null-reference and output-validation limitations remain disclosed. Modeled values are methodological references, not clinical recommendations.

See [RESULTS.md](RESULTS.md) for the per-model paired tables.

## Reproduce the reported analyses

The `reproduction/` directory is a shared, allowlisted snapshot for **both RealBio and RealDrug**. Historical directory names are preserved. It contains 110 primary prediction files and 22 supporting historical files, fixed references, original scoring rules, archived method-card/prompt code, generators and supplementary analyses. The counts describe prediction files, not independent tasks or cases.

```bash
cd reproduction
python3 -I reproduce.py
python3 -I bootstrap_primary.py > primary-bootstrap.json
python3 -I supplementary_analysis.py --output supplementary-recomputed.json
python3 -I verify_generated_references.py --output references-recomputed.json
```

These commands make **no model calls** and require only Python's standard library. The first verifies SHA-256 hashes and exact item-ID coverage before scoring. The historical credential-acquisition helper is replaced with an explicit failing stub in the archival harness; scientific prompts and cards are retained. The transformation is documented in `provenance-transformations.json`. Historical provider/database snapshots remain incomplete: offline reproduction of saved scores is not exact replay of original API calls.

The top-level `leaderboard.md` / `.csv` now show condition comparisons, not a product ranking. Previous public leaderboards and figures are preserved under `archive/pre-20261122/` for provenance and are **superseded**. Older papers in `paper/` are likewise historical; see `paper/README.md`. The revised preprint (v13, 22 November 2026) is [`paper/RealDrug-preprint-v13.pdf`](https://github.com/bioMate-AI/realdrug-benchmark/blob/v2026.11.22/paper/RealDrug-preprint-v13.pdf); this release is tagged `v2026.11.22`.

## Attribution and citation

Yaoyun Zhang and Andrew Dike. RealDrug. Benchmark data/code revision, 22 November 2026. BioMate AI; Andrew Dike is also affiliated with BizBildr. The authors develop BioMate and declare that affiliation. Cite release `v2026.11.22` (or the exact repository commit used) and the revised preprint in `paper/`.

```bibtex
@misc{realdrug2026,
  title = {RealDrug: Evaluating language-model adherence to drug development procedures},
  author = {Zhang, Yaoyun and Dike, Andrew},
  year = {2026},
  howpublished = {Benchmark data and code},
  url = {https://github.com/bioMate-AI/realdrug-benchmark},
  note = {Data/code revision 2026-11-22; cite the exact commit used}
}
```

Existing CC BY 4.0 project notices are preserved in [LICENSE](LICENSE) and the reproduction notices. Third-party materials retain their own terms and attribution. See the datasheet for source and validity limitations. [RealBio](https://github.com/bioMate-AI/realbio-benchmark) and [RealDrug](https://github.com/bioMate-AI/realdrug-benchmark) are companion studies, with no shared overall leaderboard score.
