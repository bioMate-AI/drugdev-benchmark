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

## Existing component paths

- `stage_benchmarks/B1_admet/`: ADMET resource description.
- `stage_benchmarks/B2_docking_ligand/`: ligand-ranking context.
- `stage_benchmarks/B3_pk/`: historical PK task; current generated exposure core is `data/exposure_generated_v2.jsonl`.
- `stage_benchmarks/B4_dose_selection/`: historical structured dose tier; current core is `data/dose_generated_v2.jsonl`.
- `stage_benchmarks/B5_target_structure/`: target/structure task description, not a completed paired result.
- `N1_free_energy/`, `decision_suite/`, `execution_track/`: broader resources and offline checks.
- `protocol_thresholds/`: historical retained copy; scientific ownership moved to RealBio.

Any previous component claim of a full simulator, BOIN trial or expert-validated clinical endpoint must be read in light of the current datasheet and the exact task version. Historical files are kept for auditability, not as current validated performance claims.
