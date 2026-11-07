# REIT7841 research data and analysis

Research data archive for the six-dyad collaborative Tangram study.

| Directory | Contents |
|---|---|
| `evidence/raw/vr/` | All 32 original VR CSV exports, file hashes and field schema |
| `evidence/questionnaire/` | 45 original responses, normalized data, 48 confirmed responses and item dictionary |
| `evidence/observations/` | Researcher process records, coded episodes and group interview transcripts |
| `evidence/analysis/` | Source-line extracts, event coding, case analyses, figure inputs, scripts and calculated outputs |
| `evidence/ethics/` | Original blank consent form and participant information sheet |
| `evidence/videos/` | 26-recording catalogue, viewing-copy access status and segment navigation |
| `evidence/protocol/` | Identifier mapping, current corrections and logging implementation snapshots |
| `evidence/manifests/` | File provenance, SHA-256 checksums and source-reference mapping |

Original VR CSVs are unmodified. Historical analysis notes retain their version context; current identifier mappings and corrections are in `evidence/protocol/`. The six [group interview transcripts](evidence/observations/interviews/README.md) match the retained source documents; this completeness check is not a new audio verification. [Blank study forms](evidence/ethics/README.md) preserve their original version. Signed consent forms, identity mappings, private correspondence and identifiable originals remain separately stored locally. [Recording access and segment navigation](evidence/videos/README.md) distinguish available UQ viewing copies from recordings retained locally.

Verify files and data linkage: `python3 evidence/verify_evidence.py`.
Figure reproduction instructions and dependencies are in `evidence/analysis/figures/README.md`.
