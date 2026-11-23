# DrugDev-Bench — launch video (60–90s)

**Format:** screen-recording + motion-graphics, voiceover. Target 80s.
**Tone:** calm, precise, credible — this benchmark's brand is *honesty*, not hype.

---

## Voiceover script (~195 words ≈ 80s)

**(0–10s)**
An AI can predict a binding affinity. Flag a toxicity. Estimate a concentration. But a drug-development team asks a harder question: given all of that — *what do we do next?*

**(10–22s)**
That's a decision under constraints. Advance this molecule or kill it. Is exposure enough? Which dose do the next patients get? A correct prediction is just an input. Meet DrugDev-Bench.

**(22–38s)**
For every task, we make three things explicit: the information the model is given — and what's hidden from it. The policy that defines a correct decision. And the evidence that the decision was actually *executed*, not just described. One deterministic scorer. No AI judge.

**(38–55s)**
Here's what you learn. The same model, scoring dose selection, went from zero-point-two-five on hand-written scenarios to nearly perfect on generated ones. Same metric. The way the task was built swung the result across almost the entire range.

**(55–70s)**
So we report both, side by side — and never pool them. We keep experimental data, formulas, and curated policy labeled and separate. And we flag our own scorer's limitations in the open.

**(70–80s)**
Four tracks. A 264-ligand free-energy set. Thirty decision tasks. All CC-BY. Built to be inspected — not to crown a winner. Run your system. Tell us where we're wrong.

---

## Shot list

| # | Time | Visual | On-screen text |
|---|---|---|---|
| 1 | 0–10s | Three quick cards flip past: an affinity value, a red "toxic" flag, a concentration curve | "predict a number…" |
| 2 | 10–22s | Cards dissolve into a branching decision tree (advance / kill / dose) | "…vs. make a decision" |
| 3 | 22–30s | Title card: **DrugDev-Bench** + one-line tagline | DrugDev-Bench |
| 4 | 30–38s | Three stacked rows animate in: "Information given / hidden", "Decision policy", "Execution evidence" | the 3 explicit things · "no LLM judge" |
| 5 | 38–55s | Bar/segment chart: one model, two tiers — **0.25–0.30** vs **0.95–1.00**, big swing animates | "same model · same metric" |
| 6 | 55–64s | Split screen, both tiers shown together with a "not pooled" stamp | "we report both" |
| 7 | 64–70s | Three labeled chips: "experimental / formula / curated policy" stay separate | "kept labeled" |
| 8 | 70–78s | Grid of components: 4 tracks · 5 stage benchmarks · 264 ligands · 30 decisions · CC-BY | repo URL fades in |
| 9 | 78–80s | End card: **github.com/bioMate-AI/drugdev-benchmark** + BioMate logo | "inspect it. break it." |

**Supers / legal (small, persistent on data shots):** "Provisional, run-level results. Agreement with benchmark references — not clinical accuracy. Nonclinical methodological benchmark."

**Audio:** restrained electronic bed, single soft marker hit on the 0.25→0.95 swing (shot 5).
