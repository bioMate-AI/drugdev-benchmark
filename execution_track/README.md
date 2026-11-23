> **22 November 2026 scope correction:** This is retained historical component documentation. The current root README and DATASHEET define the evaluated task version and its limits. Historical labels such as self-fix, PBPK or BOIN do not establish successful repair, physiological simulation or sequential trial execution.

---
license: cc-by-4.0
---
# DrugDev-Bench — Execution track (T4) and composer diagnostics

**Specification.** Execution-grounded tasks require a **terminal run state** and output artifacts that can
be checked against the scientific task. Cross-stage tasks additionally require valid dependencies: the
output of one step must have the appropriate **identity, units, representation, and provenance** for the next.

**Present evidence = offline composer diagnostics over 68 workflow topologies.**
- Under a perfect-decomposition assumption, every subtask clears the resolver's confidence threshold, yet
  agreement with **fine-grained gold tool identities is only 4%** (granularity mismatch: workflow-level
  units vs. individual Galaxy tools).
- **66%** of catalogued workflows use free-text parameter descriptions where structured input-type tokens
  are expected, blocking them as handoff destinations.
- Replacing exact-string with the specified **semantic matcher raises the handoff fire rate 4.4% → 38.2%**.
  Residual failures include resolver errors and cross-ecosystem representation differences
  (e.g., a count matrix vs. an `ExpressionSet`).

> **These are resolver/handoff diagnostics, NOT success rates for complete development programmes.** A
> completed execution study must verify actual files, terminal state, transformations, and scientific
> endpoints with stage-specific provenance. Neither a plan that names the right stages nor a high handoff
> rate is sufficient. **No completed roster-wide execution result is reported in this release.**
