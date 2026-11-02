# Study-round to source-log alignment

The CSV extracts in [log_traces](../log_traces/) retain every original field and add `source_line`. The raw files remain complete, including rows outside these extracts. `source_line` uses the original CSV line numbering with the header at line 1.

| Study slot | Original log | Software round | Original lines | Extract |
|---|---|---|---:|---|
| G01_R03 | [L03](../../raw/vr/REIT_Tangram/ResearchV2/TECHNICAL_TEST_20261007T073616_da594fa6_events_v2.csv) | `TECHNICAL_TEST-R02` | 1000–4959 | [G01_R03.csv](../log_traces/G01_R03.csv) |
| G03_R03 | [L07](../../raw/vr/REIT_Tangram/ResearchV2/TECHNICAL_TEST_20261009T035445_fede18ca_events_v2.csv) | `TECHNICAL_TEST-R02` | 4094–5990 | [G03_R03.csv](../log_traces/G03_R03.csv) |
| G03_R04 | [L07](../../raw/vr/REIT_Tangram/ResearchV2/TECHNICAL_TEST_20261009T035445_fede18ca_events_v2.csv) | `TECHNICAL_TEST-R06` | 7393–12620 | [G03_R04.csv](../log_traces/G03_R04.csv) |
| G04_R03 | [L08](../../raw/vr/REIT_Tangram/ResearchV2/TECHNICAL_TEST_20261009T070503_5a0ebbc4_events_v2.csv) | `TECHNICAL_TEST-R01` | 403–2179 | [G04_R03.csv](../log_traces/G04_R03.csv) |
| G04_R04 | [L08](../../raw/vr/REIT_Tangram/ResearchV2/TECHNICAL_TEST_20261009T070503_5a0ebbc4_events_v2.csv) | `TECHNICAL_TEST-R04` | 4192–7078 | [G04_R04.csv](../log_traces/G04_R04.csv) |
| G05_R03 | [L09](../../raw/vr/REIT_Tangram/ResearchV2/TECHNICAL_TEST_20261009T084000_593a8c65_events_v2.csv) | `TECHNICAL_TEST-R02` | 1182–9959 | [G05_R03.csv](../log_traces/G05_R03.csv) |
| G05_R04 | [L09](../../raw/vr/REIT_Tangram/ResearchV2/TECHNICAL_TEST_20261009T084000_593a8c65_events_v2.csv) | `TECHNICAL_TEST-R03` | 10027–11263 | [G05_R04.csv](../log_traces/G05_R04.csv) |
| G06_R03 | [L12](../../raw/vr/REIT_Tangram/ResearchV2/TECHNICAL_TEST_20261010T084712_3a9476c5_events_v2.csv) | `TECHNICAL_TEST-R01` | 4112–7133 | [G06_R03.csv](../log_traces/G06_R03.csv) |
| G06_R04 | [L12](../../raw/vr/REIT_Tangram/ResearchV2/TECHNICAL_TEST_20261010T084712_3a9476c5_events_v2.csv) | `TECHNICAL_TEST-R03` | 7422–9380 | [G06_R04.csv](../log_traces/G06_R04.csv) |

G01 R03 in this alignment is one chair attempt within a longer session, not the entire experience. G01 R04 and the later G02 recordings do not have a validated exact log match in this alignment. G02 remains included in the study; its later recordings used new targets. See [current author corrections](../../protocol/author_corrections_20261102.json).
