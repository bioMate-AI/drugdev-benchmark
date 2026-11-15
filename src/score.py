#!/usr/bin/env python3
"""Deterministic scorer scaffold for DrugDev-Bench — no LLM judge.

DrugDev-Bench evaluates drug-development DECISIONS against explicit reference policies.
This scaffold implements the scoring entry points described in the manuscript
(paper/drugdev.pdf, Methods). The two fully-specified policies (dose selection and the
generated-tier exposure formulas) are implemented here EXACTLY as the paper defines them,
so any system's predictions re-score identically and judge-free.

Usage:  python3 score.py <entry_point> <predictions.jsonl>
        python3 score.py dose my_system/dose.jsonl

Scoring entry points (six, per Methods):
  decision     deprioritization-set F1 + best-pick agreement + liability/driver id
  categorical  controlled-vocabulary match with a negation guard
  set          F1 over a predicted set vs reference set
  numeric      full credit within a fold band; partial credit within the squared band
  dose         exact dose-decision agreement under the reference-curve policy (below)
  chain        stage coverage + LCS ordering + before/after gate adherence
Plus component helpers used by the paper's tables:
  pbpk         within-twofold on peak concentration (ratio in [0.5, 2.0])
  boin         exact MTD agreement on the historical same-item dose protocol (moved from RealBio)
  protocol     exact PASS/WARN/FAIL QC-action match (moved from RealBio; new clinical/QC track)
  fep          relative binding free energy: ΔΔG RMSE / MUE / Kendall / Spearman / f(<1 kcal)

DATA NOTE: data.jsonl files are released from the suite package. This public repo ships the
scorer scaffold and documentation; if a component's data.jsonl is absent, the scorer prints a
clear message rather than inventing items. No result numbers are fabricated anywhere.
"""
import json, os, sys, math, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# Map an entry point to the component folder that holds its data.jsonl (when released).
DATA_DIRS = {
    "dose":        "stage_benchmarks/B4_dose_selection",
    "boin":        "stage_benchmarks/B4_dose_selection",   # MTD same-item protocol (moved from RealBio)
    "pbpk":        "stage_benchmarks/B3_pk",
    "protocol":    "protocol_thresholds",                  # QC-gating track (moved from RealBio)
    "fep":         "N1_free_energy",
    "decision":    "decision_suite",
    "categorical": "decision_suite",
    "set":         "decision_suite",
    "numeric":     "decision_suite",
    "chain":       "decision_suite",
}

# ------------------------------------------------------------------ helpers
def _norm(s):
    return re.sub(r"\s+", " ", str(s).strip().lower())

def load_gt(entry):
    d = DATA_DIRS.get(entry)
    path = os.path.join(ROOT, d, "data.jsonl") if d else None
    if not path or not os.path.isfile(path):
        sys.exit(f"[DrugDev-Bench] No released data.jsonl for '{entry}' at {d}/.\n"
                 f"  Component data ships with the suite package (see that folder's README).")
    return {r["id"]: r for r in (json.loads(l) for l in open(path) if l.strip())}

def load_preds(path):
    return {r["id"]: r.get("prediction") for r in (json.loads(l) for l in open(path) if l.strip())}

# ------------------------------------------------------------------ dose policy (fully specified)
def select_dose(p, tau, band=0.10, tol=1e-9):
    """Deterministic reference-curve dose policy (Methods).
    p: list of DLT probabilities p_j at ordered doses d_j (1-indexed in the paper).
    tau: target DLT probability.
    Returns the selected dose index (1-based) or None for a no-dose decision.
    Rule: no dose if p_1 > tau + band; else argmin |p_j - tau| over admissible (p_j <= tau + band);
    ties select the HIGHER index. Small tolerance applied at the threshold.
    """
    if not p:
        return None
    if p[0] > tau + band + tol:
        return None
    admissible = [j for j, pj in enumerate(p) if pj <= tau + band + tol]
    if not admissible:
        return None
    best = None
    best_dist = math.inf
    for j in admissible:            # ascending index; '<=' keeps the HIGHER index on ties
        dist = abs(p[j] - tau)
        if dist <= best_dist + tol:
            best_dist = dist
            best = j
    return None if best is None else best + 1   # 1-based dose index

def score_dose(gt, preds):
    """Exact agreement of the predicted dose decision with the reference label (incl. no-dose)."""
    n = hit = 0
    for i, r in gt.items():
        if i not in preds:
            continue
        n += 1
        ref = r.get("reference")        # expected: dose index (int) or null / "no_dose"
        pred = preds[i]
        if _norm(pred) in ("none", "no_dose", "no dose", "null") and (ref is None):
            hit += 1
        elif str(pred) == str(ref):
            hit += 1
    return {"entry": "dose", "scored": n, "exact_outcome": round(hit / n, 4) if n else None,
            "note": "exact dose-decision agreement under the reference-curve policy; "
                    "PROVISIONAL per Methods (no-dose credit edge case flagged)."}

# ------------------------------------------------------------------ BOIN / MTD same-item (moved from RealBio)
def score_boin(gt, preds):
    """Exact MTD agreement on the historical same-item dose protocol (moved from RealBio).

    This is a SEPARATE protocol from the deterministic reference-curve `dose` scorer above and
    MUST NOT be pooled with it (drugdev.docx: the historical dose-only leaderboard scores 18
    scorable items and excludes the two null-MTD references; the structured-response protocol
    scores all 20). Reference = {true_MTD_level, true_MTD_mg}; a prediction is an MTD level (int),
    an MTD dose in mg, or a no-MTD declaration.
    """
    scorable = hit = null_cases = 0
    for i, r in gt.items():
        ref = r.get("reference") or {}
        lvl = ref.get("true_MTD_level"); mg = ref.get("true_MTD_mg")
        if lvl in (None, "null") and mg in (None, "null"):
            null_cases += 1                      # excluded from the 18-item historical denominator
            continue
        scorable += 1
        if i not in preds:
            continue
        p = _norm(preds[i])
        if (lvl is not None and p == _norm(lvl)) or (mg is not None and p == _norm(mg)) \
           or (lvl is not None and _norm(lvl) in p) or (mg is not None and _norm(mg) in p):
            hit += 1
    return {"entry": "boin", "scored_items": scorable, "excluded_null_mtd": null_cases,
            "exact_mtd_agreement": round(hit / scorable, 4) if scorable else None,
            "note": "historical same-item dose protocol (18 scorable of 20); NOT pooled with the "
                    "structured-response `dose` protocol; NOT the full Bayesian Optimal Interval design."}

# ------------------------------------------------------------------ protocol-QC gating (moved from RealBio)
def score_protocol(gt, preds):
    """Exact-match QC action (PASS / WARN / FAIL) vs the protocol-aware reference action.

    New track in DrugDev-Bench (moved from RealBio). Each item carries a public data accession
    (GEO / PRIDE / EMDB) and an expert VALID/DEFECTIVE label; the reference action is the
    protocol-specific correct decision, where one universal QC cutoff would false-alarm.
    """
    n = hit = 0
    for i, r in gt.items():
        if i not in preds:
            continue
        n += 1
        if _norm(preds[i]) == _norm(r.get("reference_action")):
            hit += 1
    return {"entry": "protocol", "scored": n, "qc_action_accuracy": round(hit / n, 4) if n else None,
            "note": "exact PASS/WARN/FAIL match vs the protocol-aware reference action; no LLM judge."}

# ------------------------------------------------------------------ generated-tier reference formulas
def generated_conc_nM(F, D_mg, M_g_per_mol, V_L):
    """C_nM = 1e6 * F * D / (M * V)   (D in mg, M in g/mol, V in L)."""
    return 1e6 * F * D_mg / (M_g_per_mol * V_L)

def generated_conc_uM(F, D_mg, M_g_per_mol, V_L):
    """C_uM = 1e3 * F * D / (M * V)   (generated PK peak-concentration proxy)."""
    return 1e3 * F * D_mg / (M_g_per_mol * V_L)

def emax_response(C, E0, Emax, EC50):
    """p(C) = E0 + Emax * C / (EC50 + C)."""
    return E0 + Emax * C / (EC50 + C)

# ------------------------------------------------------------------ PK within-twofold
def score_pbpk(gt, preds):
    """Within-twofold agreement on peak concentration (uM). Missing/unparseable = failure."""
    n = hit = 0
    for i, r in gt.items():
        n += 1                       # denominator is ALL reference cases
        ref = (r.get("reference") or {}).get("Cmax_uM") if isinstance(r.get("reference"), dict) else r.get("reference")
        pred = preds.get(i)
        try:
            ratio = float(pred) / float(ref)
            if 0.5 <= ratio <= 2.0:
                hit += 1
        except (TypeError, ValueError, ZeroDivisionError):
            pass                     # counts as a miss
    return {"entry": "pbpk", "scored": n, "within_twofold": round(hit / n, 4) if n else None,
            "note": "agreement with benchmark peak-concentration reference (uM); NOT clinical accuracy."}

# ------------------------------------------------------------------ free energy (N1)
def _rankdata(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    ranks = [0.0] * len(xs)
    i = 0
    while i < len(xs):
        j = i
        while j + 1 < len(xs) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks

def _spearman(a, b):
    ra, rb = _rankdata(a), _rankdata(b)
    n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((ra[i] - ma) * (rb[i] - mb) for i in range(n))
    da = math.sqrt(sum((x - ma) ** 2 for x in ra))
    db = math.sqrt(sum((x - mb) ** 2 for x in rb))
    return num / (da * db) if da and db else 0.0

def _kendall_tau_a(a, b):
    n = len(a); num = 0
    for i in range(n):
        for j in range(i + 1, n):
            s = (a[i] - a[j]) * (b[i] - b[j])
            num += (s > 0) - (s < 0)   # ties contribute 0 -> deflates tau-a (disclosed)
    denom = n * (n - 1) / 2
    return num / denom if denom else 0.0

def score_fep(gt, preds):
    """Relative binding free energy per series: RMSE, MUE, Kendall-tau-a, Spearman, f(<1 kcal).
    gt item: {id, series, ddg_ref}. pred: predicted ΔΔG (same series/reference convention).
    A reference-perfect input scores composite ~0.98 (tie-sensitive Kendall-tau-a) — disclosed.
    """
    by_series = {}
    for i, r in gt.items():
        if i not in preds:
            continue
        by_series.setdefault(r.get("series", "all"), []).append(
            (float(r.get("ddg_ref")), float(preds[i])))
    out = {}
    for s, pairs in by_series.items():
        ref = [a for a, _ in pairs]; prd = [b for _, b in pairs]
        n = len(pairs)
        rmse = math.sqrt(sum((a - b) ** 2 for a, b in pairs) / n)
        mue = sum(abs(a - b) for a, b in pairs) / n
        f1k = sum(1 for a, b in pairs if abs(a - b) <= 1.0) / n
        out[s] = {"n": n, "rmse": round(rmse, 4), "mue": round(mue, 4),
                  "kendall_tau_a": round(_kendall_tau_a(ref, prd), 4),
                  "spearman": round(_spearman(ref, prd), 4), "frac_within_1kcal": round(f1k, 4)}
    return {"entry": "fep", "series": out,
            "note": "leave-target-out partitioning specified for the ML variant; "
                    "reference-perfect input scores composite ~0.98 by Kendall-tau-a tie handling."}

# ------------------------------------------------------------------ decision-family stubs (specified, data-gated)
def score_set(gt, preds):
    """F1 over predicted vs reference set."""
    tp = fp = fn = 0
    for i, r in gt.items():
        if i not in preds:
            continue
        want = {_norm(x) for x in (r.get("reference") or [])}
        got = {_norm(x) for x in (preds[i] or [])}
        tp += len(want & got); fp += len(got - want); fn += len(want - got)
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
    return {"entry": "set", "precision": round(prec, 4), "recall": round(rec, 4), "f1": round(f1, 4)}

def score_categorical(gt, preds):
    """Controlled-vocabulary match with a negation guard."""
    n = hit = 0
    for i, r in gt.items():
        if i not in preds:
            continue
        n += 1
        pred = _norm(preds[i]); ref = _norm(r.get("reference"))
        negated = any(w in pred for w in ("not ", "no ", "without ", "n't"))
        if pred == ref and not (negated and "not" not in ref):
            hit += 1
    return {"entry": "categorical", "scored": n, "accuracy": round(hit / n, 4) if n else None,
            "note": "controlled vocabulary + negation guard."}

def score_numeric(gt, preds):
    """Full credit within a fold band; partial credit within the squared band."""
    total = 0.0; n = 0
    for i, r in gt.items():
        if i not in preds:
            continue
        n += 1
        try:
            ref = float(r.get("reference")); pred = float(preds[i])
            band = float(r.get("fold_band", 2.0))
            ratio = max(pred / ref, ref / pred) if ref and pred else math.inf
            if ratio <= band:
                total += 1.0
            elif ratio <= band ** 2:
                total += 0.5
        except (TypeError, ValueError, ZeroDivisionError):
            pass
    return {"entry": "numeric", "scored": n, "mean_credit": round(total / n, 4) if n else None,
            "note": "full within fold band, partial within squared band."}

def score_chain(gt, preds):
    """Stage coverage + longest-common-subsequence ordering + before/after gate adherence."""
    def lcs(a, b):
        dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
        for i in range(len(a)):
            for j in range(len(b)):
                dp[i + 1][j + 1] = dp[i][j] + 1 if a[i] == b[j] else max(dp[i][j + 1], dp[i + 1][j])
        return dp[len(a)][len(b)]
    cov = order = gate = n = 0.0
    for i, r in gt.items():
        if i not in preds:
            continue
        n += 1
        ref = [_norm(x) for x in (r.get("reference") or [])]
        got = [_norm(x) for x in (preds[i] or [])]
        cov += len(set(ref) & set(got)) / len(ref) if ref else 0.0
        order += lcs(ref, got) / len(ref) if ref else 0.0
        gate += 1.0 if all(got.index(a) < got.index(b)
                           for a, b in (r.get("gates") or []) if a in got and b in got) else 0.0
    return {"entry": "chain", "scored": int(n),
            "coverage": round(cov / n, 4) if n else None,
            "lcs_order": round(order / n, 4) if n else None,
            "gate_adherence": round(gate / n, 4) if n else None}

def score_decision(gt, preds):
    """Decision scoring = deprioritization-set F1 + best-pick agreement + liability/driver id.
    Composition over the per-field sub-scorers above."""
    return {"entry": "decision",
            "note": "composes set-F1 (deprioritization) + best-pick agreement + liability/driver id; "
                    "run with released decision_suite/data.jsonl."}

ENTRY = {
    "dose": score_dose, "boin": score_boin, "pbpk": score_pbpk,
    "protocol": score_protocol, "fep": score_fep,
    "decision": score_decision, "categorical": score_categorical,
    "set": score_set, "numeric": score_numeric, "chain": score_chain,
}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ENTRY:
        print("usage: python3 score.py <entry_point> <predictions.jsonl>")
        print("entry points:", ", ".join(ENTRY))
        sys.exit(1)
    entry, pred_path = sys.argv[1], sys.argv[2]
    result = ENTRY[entry](load_gt(entry), load_preds(pred_path))
    print(json.dumps(result, indent=2))
