# Original VR exports

All 32 CSV files from the available `REIT_Tangram` export folder are included, byte for byte: 13 ResearchV2 event logs and 19 legacy logs. File names, row order, timestamps, identifiers and numeric precision are unchanged. SHA-256 hashes are listed in [manifest.json](manifest.json).

ResearchV2 stores events, piece poses and participant head/controller poses in the same 34-column CSV. There are no separate pose/session JSON originals in the available export. The legacy format has 9 columns. See [schema.json](schema.json) for the actual headers.

`TECHNICAL_TEST` is a recorded software label, not a reliable exclusion rule. Several files with that label contain matched study activity. Practice, resets, interrupted attempts and unassigned logs are preserved. The nine matched segments below are log navigation units; they do not define the six-dyad study sample.

| Log | Original file | Rows | Matched study segments |
|---|---|---:|---|
| L01 | [G01_20261008T050538_fe2222fe_events_v2.csv](REIT_Tangram/ResearchV2/G01_20261008T050538_fe2222fe_events_v2.csv) | 96 | No validated segment in the retained nine-segment alignment |
| L02 | [TECHNICAL_TEST_20261007T073110_b3992186_events_v2.csv](REIT_Tangram/ResearchV2/TECHNICAL_TEST_20261007T073110_b3992186_events_v2.csv) | 567 | No validated segment in the retained nine-segment alignment |
| L03 | [TECHNICAL_TEST_20261007T073616_da594fa6_events_v2.csv](REIT_Tangram/ResearchV2/TECHNICAL_TEST_20261007T073616_da594fa6_events_v2.csv) | 18,571 | G01_R03 |
| L04 | [TECHNICAL_TEST_20261007T093401_a9cf223e_events_v2.csv](REIT_Tangram/ResearchV2/TECHNICAL_TEST_20261007T093401_a9cf223e_events_v2.csv) | 1,050 | No validated segment in the retained nine-segment alignment |
| L05 | [TECHNICAL_TEST_20261007T102325_390346f9_events_v2.csv](REIT_Tangram/ResearchV2/TECHNICAL_TEST_20261007T102325_390346f9_events_v2.csv) | 5,715 | No validated segment in the retained nine-segment alignment |
| L06 | [TECHNICAL_TEST_20261008T050322_1acce4df_events_v2.csv](REIT_Tangram/ResearchV2/TECHNICAL_TEST_20261008T050322_1acce4df_events_v2.csv) | 332 | No validated segment in the retained nine-segment alignment |
| L07 | [TECHNICAL_TEST_20261009T035445_fede18ca_events_v2.csv](REIT_Tangram/ResearchV2/TECHNICAL_TEST_20261009T035445_fede18ca_events_v2.csv) | 12,742 | G03_R03, G03_R04 |
| L08 | [TECHNICAL_TEST_20261009T070503_5a0ebbc4_events_v2.csv](REIT_Tangram/ResearchV2/TECHNICAL_TEST_20261009T070503_5a0ebbc4_events_v2.csv) | 7,164 | G04_R03, G04_R04 |
| L09 | [TECHNICAL_TEST_20261009T084000_593a8c65_events_v2.csv](REIT_Tangram/ResearchV2/TECHNICAL_TEST_20261009T084000_593a8c65_events_v2.csv) | 11,279 | G05_R03, G05_R04 |
| L10 | [TECHNICAL_TEST_20261010T024954_0023fdf8_events_v2.csv](REIT_Tangram/ResearchV2/TECHNICAL_TEST_20261010T024954_0023fdf8_events_v2.csv) | 34 | No validated segment in the retained nine-segment alignment |
| L11 | [TECHNICAL_TEST_20261010T062552_3260dfc6_events_v2.csv](REIT_Tangram/ResearchV2/TECHNICAL_TEST_20261010T062552_3260dfc6_events_v2.csv) | 11 | No validated segment in the retained nine-segment alignment |
| L12 | [TECHNICAL_TEST_20261010T084712_3a9476c5_events_v2.csv](REIT_Tangram/ResearchV2/TECHNICAL_TEST_20261010T084712_3a9476c5_events_v2.csv) | 9,495 | G06_R03, G06_R04 |
| L13 | [TECHNICAL_TEST_20261010T111851_95ec3dd3_events_v2.csv](REIT_Tangram/ResearchV2/TECHNICAL_TEST_20261010T111851_95ec3dd3_events_v2.csv) | 31 | No validated segment in the retained nine-segment alignment |

## Legacy exports

These are the original compact logs, including early technical sessions and companions to later ResearchV2 sessions. They are preserved for provenance, not counted as extra participants.

- [TECHNICAL_TEST_20260920_114200.csv](REIT_Tangram/TECHNICAL_TEST_20260920_114200.csv) — 32 rows
- [TECHNICAL_TEST_20260922_124918.csv](REIT_Tangram/TECHNICAL_TEST_20260922_124918.csv) — 43 rows
- [TECHNICAL_TEST_20260922_135543.csv](REIT_Tangram/TECHNICAL_TEST_20260922_135543.csv) — 2 rows
- [TECHNICAL_TEST_20260922_140106.csv](REIT_Tangram/TECHNICAL_TEST_20260922_140106.csv) — 2 rows
- [TECHNICAL_TEST_20260922_153610.csv](REIT_Tangram/TECHNICAL_TEST_20260922_153610.csv) — 16 rows
- [TECHNICAL_TEST_20260922_153727.csv](REIT_Tangram/TECHNICAL_TEST_20260922_153727.csv) — 19 rows
- [TECHNICAL_TEST_20260922_154329.csv](REIT_Tangram/TECHNICAL_TEST_20260922_154329.csv) — 2 rows
- [TECHNICAL_TEST_20261007_073110.csv](REIT_Tangram/TECHNICAL_TEST_20261007_073110.csv) — 85 rows
- [TECHNICAL_TEST_20261007_073616.csv](REIT_Tangram/TECHNICAL_TEST_20261007_073616.csv) — 1100 rows
- [TECHNICAL_TEST_20261007_093401.csv](REIT_Tangram/TECHNICAL_TEST_20261007_093401.csv) — 115 rows
- [TECHNICAL_TEST_20261007_102325.csv](REIT_Tangram/TECHNICAL_TEST_20261007_102325.csv) — 453 rows
- [TECHNICAL_TEST_20261008_050322.csv](REIT_Tangram/TECHNICAL_TEST_20261008_050322.csv) — 72 rows
- [TECHNICAL_TEST_20261009_035445.csv](REIT_Tangram/TECHNICAL_TEST_20261009_035445.csv) — 732 rows
- [TECHNICAL_TEST_20261009_070503.csv](REIT_Tangram/TECHNICAL_TEST_20261009_070503.csv) — 339 rows
- [TECHNICAL_TEST_20261009_084000.csv](REIT_Tangram/TECHNICAL_TEST_20261009_084000.csv) — 807 rows
- [TECHNICAL_TEST_20261010_024954.csv](REIT_Tangram/TECHNICAL_TEST_20261010_024954.csv) — 7 rows
- [TECHNICAL_TEST_20261010_062552.csv](REIT_Tangram/TECHNICAL_TEST_20261010_062552.csv) — 3 rows
- [TECHNICAL_TEST_20261010_084712.csv](REIT_Tangram/TECHNICAL_TEST_20261010_084712.csv) — 641 rows
- [TECHNICAL_TEST_20261010_111851.csv](REIT_Tangram/TECHNICAL_TEST_20261010_111851.csv) — 8 rows

## Identifiers and time

`P1`/`P2` and `client_id` are software endpoints, not globally stable thesis participant identities. The filenames contain software session IDs, not hardware serial numbers. UTC, server time, wall elapsed time and active task time are distinct clocks. Original values are retained. See the [current study guide](../../protocol/README.md) and [source-line alignment](../../analysis/log_alignment/README.md).

For `participant_pose`, the position and quaternion columns record the head pose; the JSON in `extra` contains `left`, `right`, `leftRotation` and `rightRotation` for the two controllers. The event reason explicitly identifies these as head/controller poses, not eye gaze. Piece events use the same pose columns for the relevant piece. `manipulation_id` links accepted grabs to their releases.
