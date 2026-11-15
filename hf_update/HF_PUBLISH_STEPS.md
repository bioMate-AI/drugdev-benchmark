# HuggingFace publish steps — DrugDev-Bench (MANUAL; not run here)

The HuggingFace CLI is **not** logged in in this environment, so nothing was uploaded.
Run these steps once you are authenticated. The modern CLI is `hf` (the older `huggingface-cli`
aliases still work). Target: a **dataset** repo under the `bioMate-AI` org, parallel to RealBio.

## 0. One-time setup
```bash
pip install -U "huggingface_hub[cli]"
hf auth login                      # paste a WRITE token from https://huggingface.co/settings/tokens
hf auth whoami                     # confirm you are in the bioMate-AI org
```

## 1. Create the dataset repo
```bash
hf repo create bioMate-AI/drugdev-bench --repo-type dataset
# if the org namespace is unavailable, fall back to your user and transfer later:
#   hf repo create drugdev-bench --repo-type dataset
```

## 2. Push the dataset card + public artifacts
The card lives at `hf_update/README.md`. Upload it as the dataset `README.md`, and include the
paper, scorer, leaderboard, datasheet, and component docs so the HF page mirrors GitHub.

```bash
cd /Users/kky/drugdev-benchmark-public

# a) the dataset card (becomes the HF landing page)
hf upload bioMate-AI/drugdev-bench hf_update/README.md README.md --repo-type dataset

# b) supporting files (adjust/remove any you prefer to keep GitHub-only)
hf upload bioMate-AI/drugdev-bench DATASHEET.md       DATASHEET.md       --repo-type dataset
hf upload bioMate-AI/drugdev-bench leaderboard.md     leaderboard.md     --repo-type dataset
hf upload bioMate-AI/drugdev-bench leaderboard.csv    leaderboard.csv    --repo-type dataset
hf upload bioMate-AI/drugdev-bench models.yaml        models.yaml        --repo-type dataset
hf upload bioMate-AI/drugdev-bench paper/drugdev.pdf  paper/drugdev.pdf  --repo-type dataset
hf upload bioMate-AI/drugdev-bench src/score.py       src/score.py       --repo-type dataset

# c) component READMEs (whole folders in one call each)
hf upload bioMate-AI/drugdev-bench stage_benchmarks/ stage_benchmarks/ --repo-type dataset
hf upload bioMate-AI/drugdev-bench N1_free_energy/    N1_free_energy/    --repo-type dataset
hf upload bioMate-AI/drugdev-bench decision_suite/    decision_suite/    --repo-type dataset
hf upload bioMate-AI/drugdev-bench execution_track/   execution_track/   --repo-type dataset
```

## 3. (When released) upload the per-component data
The `data.jsonl` files ship with the suite package and are **not** in this public repo yet. Once
cleared for release, drop each into its component folder and upload, e.g.:
```bash
hf upload bioMate-AI/drugdev-bench stage_benchmarks/B4_dose_selection/data.jsonl \
    stage_benchmarks/B4_dose_selection/data.jsonl --repo-type dataset
```

## 4. Verify
```bash
# open https://huggingface.co/datasets/bioMate-AI/drugdev-bench and confirm the card renders,
# tags/pretty_name show, and the paper + scorer are downloadable.
```

## Notes
- Keep the HF card's YAML front matter in sync with GitHub's README front matter (`pretty_name`,
  `license: cc-by-4.0`, `tags`).
- Do **not** mark this as a leaderboard dataset; it is a design + selected-experiments release, and the
  card must preserve the "provisional" framing.
- If you created under your user namespace, transfer to the org via the dataset's
  **Settings → Rename or transfer this dataset**.
