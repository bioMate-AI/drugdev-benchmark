> **22 November 2026 scope correction:** This is retained historical component documentation. The current root README and DATASHEET define the evaluated task version and its limits. Historical labels such as self-fix, PBPK or BOIN do not establish successful repair, physiological simulation or sequential trial execution.

---
license: cc-by-4.0
---
# DrugDev-Bench — B5 Target structure (stage benchmark, track T1)

**Scope.** 10 targets.
**Ground-truth field(s).** sequence/structure inputs and **pocket-residue** references.
**Scoring.** `../../src/score.py set` (pocket-residue set F1) / `categorical`.

> Structure-based tracks require **task-specific similarity and temporal controls**; a good structural
> score cannot establish geometric validity, synthetic feasibility, or a suitable development profile.

**Data.** `data.jsonl` ships with the suite package.
