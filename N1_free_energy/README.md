> **22 November 2026 scope correction:** This is retained historical component documentation. The current root README and DATASHEET define the evaluated task version and its limits. Historical labels such as self-fix, PBPK or BOIN do not establish successful repair, physiological simulation or sequential trial execution.

---
license: cc-by-4.0
---
# DrugDev-Bench — N1 Relative binding free energy (track T1)

**Scope.** 8 congeneric series, **264 ligands**. Reuses the **Merck/Schindler FEP benchmark**
(Schindler et al., *J. Chem. Inf. Model.* 2020; data: https://github.com/MCompChem/fep-benchmark).
**Definition.** For a ligand and a designated reference in the same series,
`ΔΔG = ΔG_ligand − ΔG_reference`.
**Ground-truth field(s).** experimental affinity-derived relative free energies (`ddg_ref`, per series).
**Scoring.** `../src/score.py fep` — RMSE, mean unsigned error, **Kendall-τ-a**, Spearman, and the
fraction within **1 kcal·mol⁻¹**, plus a composite.

> **Disclosed scorer behaviour.** A **reference-perfect input scores ≈0.98** on the composite (not 1.0)
> because tied experimental values deflate Kendall-τ-a. This is a scorer-consistency property, **not**
> a molecular prediction result, and no comparison against a specialized FEP method is inferred from it.
>
> **ML variant.** Specifies **leave-target-out** partitioning — a design requirement distinct from a
> completed prospective or blinded FEP comparison.

**Attribution.** Experimental free-energy data © the Merck/Schindler collection; retain their license.
**Data.** ligand structures are referenced to the source collection; see the suite package.
