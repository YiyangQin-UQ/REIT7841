# Derived analysis data and reproducible figures

This directory stores existing study-analysis inputs, calculations, source mappings and 11 reproducible graphical results. It contains no thesis document or LaTeX project.

## Data

- `inputs/geometry/`: source-row-preserving G03/G04/G06 pose traces, the saved Unity scene and extracted piece vertices/scales, target silhouette and selected G06 VR frame.
- `inputs/log_traces/`: three additional formal-round traces used in the paired-action analysis.
- `inputs/division_action_intervals.csv`: 293 accepted-grab/release pairs across six selected rounds, including all 79 pairs for G06 R03. Software endpoint IDs remain unchanged.
- `inputs/questionnaire/`: 48 participant-coded forms, all 12 items and their original wording. Values are 1–5 or literal `NA`; the two NA entries are retained.
- `inputs/self_revision_frames/`, `inputs/goose/`, `inputs/identity_frames/`: authentic crops/frames and relevant extraction or process provenance.
- `specs/`: explicit trace row selections, diagram specifications, source-code mappings and reference pixel hashes.
- `provenance/`: original/current hashes, locator adaptations, researcher corrections and selected-source audits. `source-archive/...` values identify historical originals; they are not runtime paths.
- `generated/`: recomputed numerical records, validation results and 11 retained PNG outputs.

See `SCHEMA.json` for keys, units and missing-value conventions. Original CSV line numbers include the header: data index = `source_line - 2`. Video clocks, UTC timestamps and active-task seconds are separate. Dataset/source IDs and former figure numbers are retained only as analysis metadata in JSON.

## Dependencies

Tested with Python 3.12.0, matplotlib 3.11.2, numpy 2.5.4 and Pillow 13.0.0. Install `requirements.txt` in a Python environment. No Unity execution, Codex installation or local skill is required.

## Run

From the repository root, or using the full path from another working directory:

```sh
python evidence/analysis/figures/reproduce.py
```

This re-extracts all seven meshes from the supplied saved scene, checks them against the archived geometry, runs the current analysis/drawing scripts and validates the resulting data and pixels. It writes only under this directory. PDFs/SVGs can be generated locally; they are ignored in the repository to avoid duplicate outputs. The retained graphical results are PNGs.

To check the six selected traces field-by-field against the four original ResearchV2 CSV files:

```sh
python evidence/analysis/figures/validate.py --raw-dir evidence/raw/vr/REIT_Tangram/ResearchV2
```

That raw directory is detected automatically in the full archive. A standalone copy explicitly reports original-log validation as not run if the raw files are absent; the supplied traces, 293 pairs, geometry, questionnaire and pixels are still checked.

`generated/audit/validation.json` records the executed checks. Current raw data and pixel results passed. The source backup establishes the stored geometry, not binary identity with the recording APK. Researcher judgments and intentions remain in the process records rather than being inferred from action counts.
