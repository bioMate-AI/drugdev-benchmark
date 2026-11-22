# Known data errata

These issues affect the **hand-authored, unpaired** tiers listed in the resource catalog. They do not affect the paired procedure-adherence results: the 15 generated exposure items use synthetic compounds with no SMILES, and all 20 generated dose references are non-null. Stored labels are left unchanged for provenance; corrections below are recommendations for the next versioned task release.

## B3_pk (hand-authored PK, 15 items)

**PK-003 ibuprofen: unit error in the reference.** The stored `Cmax_uM: 37.4` matches the published 400 mg fasted value of 37.4 µg/mL ([PMC4269818](https://pmc.ncbi.nlm.nih.gov/articles/PMC4269818/)), not 37.4 µM. With the item's own MW (206.29 g/mol), 37.4 µg/mL ≈ 181.3 µM. The AUC field for this item should be checked for the same unit error. Treat PK-003 as unreliable until it is re-sourced.

**Four SMILES strings do not encode the named drug.** The stored MW values are correct; the SMILES are not. MW recomputed from the stored SMILES with RDKit:

| ID | Name | Stored MW | MW of stored SMILES | PubChem CID | PubChem SMILES |
|---|---|---|---|---|---|
| PK-005 | Warfarin | 308.33 | 256.26 | 54678486 | `CC(=O)CC(C1=CC=CC=C1)C2=C(C3=CC=CC=C3OC2=O)O` |
| PK-006 | Midazolam | 325.77 | 300.75 | 4192 | `CC1=NC=C2N1C3=C(C=C(C=C3)Cl)C(=NC2)C4=CC=CC=C4F` |
| PK-008 | Atorvastatin | 558.64 | 576.64 | 60823 | `CC(C)C1=C(C(=C(N1CC[C@H](C[C@H](CC(=O)O)O)O)C2=CC=C(C=C2)F)C3=CC=CC=C3)C(=O)NC4=CC=CC=C4` |
| PK-009 | Sildenafil | 474.58 | 478.62 | 135398744 | `CCCC1=NN(C2=C1N=C(NC2=O)C3=C(C=CC(=C3)S(=O)(=O)N4CCN(CC4)C)OCC)C` |

The other 11 items' SMILES agree with their stored MW to within 0.02 g/mol. Any model that derives properties from the SMILES receives a different molecule from the one named for these four items.

The remaining PK references (12 of 15) have no recovered original source. Analyte, formulation and population must be matched before these values are used as observed clinical exposures.

## B4_dose_selection (hand-authored dose, 20 items)

**Two null-MTD labels are not reproduced by the declared rule.** The rule is: retain doses at or below target + 0.10, select the dose closest to target, break ties toward the higher dose. With target 0.25:

| ID | DLT rates per level | Stored label | Declared rule gives |
|---|---|---|---|
| CT-005 | 0.02, 0.04, 0.07, 0.12 | null (`MTD_NOT_REACHED`) | level 4 (highest dose; all levels admissible) |
| CT-017 | 0.30, 0.50, 0.72, 0.90 | null (`HIGH_DLT_AT_STARTING_DOSE`, `TRIAL_SHOULD_STOP`) | level 1 (0.30 ≤ 0.35 admissible) |

The two nulls also mean different things: "MTD not reached, highest tested dose is tolerable" versus "no safe dose, stop". A single null cannot express both. The next task release needs an explicit response contract that separates them.

**CT-009 floating-point tie.** Levels are exactly 0.03 from target in exact arithmetic, but 0.03 and 0.030000000000000027 in binary floating point. A raw-minimum implementation picks the lower dose; a tolerance-based tie rule picks the higher dose, as the declared rule requires. The historical result is 17/20; tolerance-based reconstruction agrees with 18/20 stored labels, and CT-005 and CT-017 account for the remaining two.
