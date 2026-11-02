# REIT7841 research data and analysis

Research data archive for the six-dyad collaborative Tangram study.

| Directory | Contents |
|---|---|
| `evidence/raw/vr/` | All 32 original VR CSV exports, file hashes and field schema |
| `evidence/questionnaire/` | 45 original responses, normalized data, 48 confirmed responses and item dictionary |
| `evidence/observations/` | Researcher process records, coded episodes and group interview transcripts |
| `evidence/analysis/` | Source-line extracts, event coding, case analyses, figure inputs, scripts and calculated outputs |
| `evidence/protocol/` | Identifier mapping, current corrections and logging implementation snapshots |
| `evidence/manifests/` | File provenance, SHA-256 checksums and source-reference mapping |

Original VR CSVs are unmodified. Historical analysis notes retain their version context; current identifier mappings and corrections are in `evidence/protocol/`. Original video/audio and signed consent/identity records are retained separately.

Verify files and data linkage: `python3 evidence/verify_evidence.py`.
Figure reproduction instructions and dependencies are in `evidence/analysis/figures/README.md`.
