# Recording catalogue and segment navigation

[The recording catalogue](video_manifest.json) contains 26 stable V identifiers. [The segment index](video_segments.json) and its [tab-separated copy](video_segments.tsv) provide navigation to the retained source intervals and physical recordings.

Six physical-overhead viewing copies (V01–V06) have been prepared locally with interface identifiers cropped or masked; their viewing links have not yet been configured. The other 20 recordings remain local pending further privacy review. No recording is presented as uploaded merely because it appears in this catalogue. [Processing details](viewing_copy_processing.json) record the six copies and the preserved file clocks.

Viewing-copy paths use physical_direct/G01–G06/, physical_overhead/G01–G06/, and VR_recordings/G01–G06/. The endpoint field distinguishes primary and partner VR recordings. A VR group folder can include both first-person and shared-overhead segments. Stable V identifiers are retained across the original files and viewing copies.

The segment index has 59 navigation records: 47 retained VR source intervals and 12 physical recording spans. Multiple records can refer to the same task or the same event recorded at two endpoints. These records are not independent experiments. Physical start/end values cover the available file and do not assert exact task boundaries. Existing VR boundaries and tolerances have been preserved; no new continuous audiovisual review was performed for this catalogue.

Current interpretation follows the [author corrections](../protocol/author_corrections_20261102.json). G02's later recordings used new targets and remain in the six-group evidence; its questionnaires describe the original session. The confirmed questionnaire table has 48 records (45 original responses and 3 participant-confirmed researcher entries), so historical notes about three missing questionnaires are superseded. G05's later woman task is R04. G06's interrupted start and included restart are distinct records, not two independent condition observations.

Actual recording limits remain: G06 has no partner recording; V17 does not contain G04's formal swimmer task, which is covered by V23; the G03 partner files have a gap; and the G05 preliminary candle is outside both recordings. Empty segment bounds identify unavailable coverage, not an upload that should be invented. The six physical overhead recordings have no recoverable speech, and V14 is near-silent. The local automatic video transcripts have not been added as verified speech.

For existing thesis source identifiers, consult [the D-source map](../manifests/source_references.json). D entries identify records and analyses and are not a one-to-one video list. The six prepared viewing copies retain the original file clock, with no cuts or speed changes. V06 is black from 103.000 seconds to the end to cover a phone-interface transition. Any future edit that changes timing needs an explicit time mapping before these segment bounds can be used.

## Per-recording status

| Recording | Group | Folder | D sources | Access |
|---|---|---|---|---|
| V01 | G01 | physical_overhead | D03 | Local viewing copy ready; upload pending |
| V02 | G02 | physical_overhead | D53 | Local viewing copy ready; upload pending |
| V03 | G03 | physical_overhead | D57 | Local viewing copy ready; upload pending |
| V04 | G04 | physical_overhead | D60 | Local viewing copy ready; upload pending |
| V05 | G05 | physical_overhead | D62 | Local viewing copy ready; upload pending |
| V06 | G06 | physical_overhead | D12 | Local viewing copy ready; upload pending |
| V07 | G01 | physical_direct | D01 | Local only; privacy review pending |
| V08 | G02 | physical_direct | D52 | Local only; privacy review pending |
| V09 | G03 | physical_direct | D05 | Local only; privacy review pending |
| V10 | G04 | physical_direct | D07 | Local only; privacy review pending |
| V11 | G05 | physical_direct | D09 | Local only; privacy review pending |
| V12 | G06 | physical_direct | D63 | Local only; privacy review pending |
| V13 | G01 | VR_recordings | D51 | Local only; privacy review pending |
| V14 | G01 | VR_recordings | D04 | Local only; privacy review pending |
| V15 | G02 | VR_recordings | D55, D56 | Local only; privacy review pending |
| V16 | G03 | VR_recordings | D06, D58 | Local only; privacy review pending |
| V17 | G04 | VR_recordings | D08, D66 | Local only; privacy review pending |
| V18 | G05 | VR_recordings | D10, D11 | Local only; privacy review pending |
| V19 | G06 | VR_recordings | D14, D15 | Local only; privacy review pending |
| V20 | G01 | VR_recordings | D04 | Local only; privacy review pending |
| V21 | G03 | VR_recordings | D06 | Local only; privacy review pending |
| V22 | G03 | VR_recordings | D58 | Local only; privacy review pending |
| V23 | G04 | VR_recordings | D08, D61, D67 | Local only; privacy review pending |
| V24 | G05 | VR_recordings | D10, D11 | Local only; privacy review pending |
| V25 | G02 | VR_recordings | D55, D56 | Local only; privacy review pending |
| V26 | G01 | VR_recordings | D51 | Local only; privacy review pending |
