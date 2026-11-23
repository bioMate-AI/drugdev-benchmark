> **22 November 2026 scope correction:** This is retained historical component documentation. The current root README and DATASHEET define the evaluated task version and its limits. Historical labels such as self-fix, PBPK or BOIN do not establish successful repair, physiological simulation or sequential trial execution.

---
license: cc-by-4.0
---
# DrugDev-Bench — Protocol-QC gating (NEW track, moved from RealBio)

**Scope.** 100 items. Real public datasets on specialized library types where **one universal QC
threshold false-alarms** (low-input scRNA, CITE-seq, plate-based scRNA, spatial FFPE, small-RNA,
proteomics, cryo-EM, …). Each item carries a public data **accession (GEO / PRIDE / EMDB)** and an
expert **VALID / DEFECTIVE** label.
**Task.** Given the sequencing protocol and the QC situation, decide the correct action: **PASS / WARN / FAIL.**
**Ground-truth field(s).** `reference_action` (the protocol-aware correct action) + `ground_truth` (VALID/DEFECTIVE).
**Scoring.** `../src/score.py protocol` — exact-match QC-action accuracy, **no LLM judge**.

**Data.** `data.jsonl` (100 items, runnable) + `datasets.source.yaml` (full source with per-item
`universal_threshold_problem`, `biomate_profile`, naive vs. protocol-aware actions, and annotation notes).

## Cross-system result (same-item, RealBio Supplementary Table S1)

Protocol-QC accuracy ranges **0.330–0.630** across the reported systems; **Gemini 3.1 Pro is highest (0.630)**,
Claude Opus 5 lowest (0.330). Full table in `../leaderboard.md`.

> **Caution.** A PASS / WARN / FAIL response is a **decision under the benchmark's reference policy**, not a
> complete assessment of an analysis. The `0.925` figure that appeared in an earlier public draft is **not**
> in the manuscript Table 1 and is **not** used here.

**Provenance.** Moved into DrugDev-Bench from the RealBio evaluation suite (`protocol_thresholds`); the
RealBio public repo removes it in the same transfer. Cross-system values transcribed from the RealBio
manuscript (same-item Supplementary Table S1 / Table 1 QC-action column).
