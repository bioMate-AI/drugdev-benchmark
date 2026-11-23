> **22 November 2026 scope correction:** This is retained historical component documentation. The current root README and DATASHEET define the evaluated task version and its limits. Historical labels such as self-fix, PBPK or BOIN do not establish successful repair, physiological simulation or sequential trial execution.

---
license: cc-by-4.0
---
# DrugDev-Bench — B1 ADMET (stage benchmark, track T1)

**Scope.** 20 compounds. Curated ADMET property and toxicity labels.
**Ground-truth field(s).** per-endpoint curated labels — hERG, drug-induced liver injury (DILI), Ames-related, and rule-of-five descriptors.
**Scoring.** `../../src/score.py` entry points `categorical` / `numeric` / `set` (no LLM judge).

> **Evidence caution (from the paper).** Reference types are **mixed** and provenance differs by endpoint.
> A rule-of-five calculation is **not** a measured assay; mixed reference types must not be described
> collectively as experimental measurements. Data licensing and primary-source attribution are retained
> at the component level.

**Data.** `data.jsonl` ships with the suite package.
