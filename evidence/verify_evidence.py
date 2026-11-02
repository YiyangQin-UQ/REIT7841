"""Verify the published evidence without editing any data. Python standard library only."""
from pathlib import Path
import csv, hashlib, json

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/'evidence'
def rows(path, delimiter=','):
    with path.open(encoding='utf-8-sig',newline='') as h:
        return list(csv.DictReader(h,delimiter=delimiter))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

manifest=json.loads((EVIDENCE/'raw/vr/manifest.json').read_text())
assert len(manifest['files'])==32
by_id={}
for item in manifest['files']:
    p=ROOT/item['path']
    assert p.stat().st_size==item['bytes'],item['path']
    assert sha(p)==item['sha256'],item['path']
    data=rows(p)
    assert len(data)==item['rows'],item['path']
    if item['log_id']:by_id[item['log_id']]=data
matched=json.loads((EVIDENCE/'analysis/log_alignment/nine_matched_rounds.json').read_text())
checked=0
for segment in matched:
    extract=rows(EVIDENCE/'analysis/log_traces'/(segment['slot']+'.csv'))
    assert len(extract)==segment['end_line']-segment['start_line']+1
    for expected_line,row in enumerate(extract,segment['start_line']):
        assert int(row['source_line'])==expected_line
        original=by_id[segment['log']][expected_line-2]
        assert {k:v for k,v in row.items() if k!='source_line'}==original
        checked+=1
survey=rows(EVIDENCE/'questionnaire/survey_confirmed.tsv','\t')
assert len(rows(EVIDENCE/'questionnaire/survey_raw.csv'))==45
assert len(survey)==48
assert len({r['participant_id'] for r in survey})==12
assert len({r['record_id'] for r in survey})==48
assert sum(r['Q01']=='NA' for r in survey)==2
assert len({(r['participant_id'],r['round_id']) for r in survey})==48
checks=EVIDENCE/'manifests/publication_files.json'
file_count=0
if checks.exists():
    for item in json.loads(checks.read_text())['files']:
        p=ROOT/item['path'];assert p.stat().st_size==item['bytes'];assert sha(p)==item['sha256'],item['path']
        file_count+=1
print(json.dumps({'status':'PASS','raw_vr_files':32,'matched_segments':len(matched),
                  'source_rows_verified':checked,'confirmed_questionnaires':48,
                  'publication_files_verified':file_count},indent=2))
