#!/usr/bin/env python3
"""Verify portable inputs, all 293 intervals, 11 images, and optionally original VR rows.
Original CSV line numbers include the header; data index = source_line - 2.
Raw files are read only; no file outside this package is modified.
"""
from pathlib import Path
import argparse,csv,hashlib,json,sys
from collections import Counter
from PIL import Image
B=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--raw-dir',type=Path,default=None);a=ap.parse_args()
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
report={'package':'REIT7841 v1.1 figure reproduction','checks':{},'failures':[]}
def check(label,ok,details=None):
 report['checks'][label]={'pass':bool(ok),'details':details}
 if not ok:report['failures'].append(label)
manifest=json.loads((B/'provenance/file_manifest.json').read_text())
for item in manifest['files']:check('integrity:'+item['path'],sha(B/item['path'])==item['sha256'])
config=json.loads((B/'specs/trace_selection.json').read_text());expected=read(B/'inputs/division_action_intervals.csv')
rawdir=a.raw_dir
if rawdir is None:
 candidate=B.parents[1]/'raw/vr/REIT_Tangram/ResearchV2'
 if candidate.exists():rawdir=candidate
rawcache={};derived=[];tracechecks=[]
for c in config:
 trace=read(B/c['trace']);lines=[int(x['source_line']) for x in trace]
 check('trace-selection:'+c['slot'],len(trace)==c['row_count'] and lines==list(range(c['first_csv_line'],c['last_csv_line']+1)) and sha(B/c['trace'])==c['trace_sha256'])
 if rawdir is not None:
  rawpath=rawdir/c['raw_filename']
  if rawpath.exists():
   if rawpath not in rawcache:
    check('raw-sha:'+c['log_id'],sha(rawpath)==c['raw_sha256']);rawcache[rawpath]=read(rawpath)
   raw=rawcache[rawpath];same=all(all(raw[int(r['source_line'])-2].get(k)==v for k,v in r.items() if k!='source_line') for r in trace)
   check('raw-fields:'+c['slot'],same,{'rows':len(trace),'first_line':c['first_csv_line'],'last_line':c['last_csv_line']})
  else:check('raw-file:'+c['log_id'],False,{'expected':str(rawpath)})
 releases={r['manipulation_id']:r for r in trace if r['event']=='piece_release'}
 for r in trace:
  if r['event']!='grab_accepted':continue
  release=releases.get(r['manipulation_id'])
  check('paired:'+c['slot']+':'+r['manipulation_id'],release is not None and release['participant_id']==r['participant_id'])
  if release is None:continue
  derived.append({'slot':c['slot'],'condition':r['condition'],'log_id':c['log_id'],'round_id':r['round_id'],'endpoint':r['participant_id'],'client_id':r['client_id'],'piece_id':r['piece_id'],'grab_active_s':float(r['active_elapsed_s']),'release_active_s':float(release['active_elapsed_s']),'manipulation_id':r['manipulation_id'],'grab_source_line':int(r['source_line']),'release_source_line':int(release['source_line']),'release_x_m':float(release['position_x_m']),'release_y_m':float(release['position_y_m']),'release_z_m':float(release['position_z_m']),'source_file':'evidence/raw/vr/REIT_Tangram/ResearchV2/'+c['raw_filename']})
check('interval-count',len(derived)==len(expected)==293,dict(Counter(x['slot'] for x in derived)))
numeric={'grab_active_s','release_active_s','release_x_m','release_y_m','release_z_m'};integer={'grab_source_line','release_source_line'}
same=True
for new,old in zip(derived,expected):
 for k,v in new.items():
  if k=='source_file':continue
  if k in numeric:same=same and abs(v-float(old[k]))<1e-12
  elif k in integer:same=same and v==int(old[k])
  else:same=same and v==old[k]
check('all-293-pairs-match-archived',same,'All data fields compared. source_file is made repository-relative; human-readable piece_description is omitted from recomputed table.')
check('G06-R03-interval-count',sum(x['slot']=='G06_R03' for x in derived)==79)
(B/'generated/audit').mkdir(parents=True,exist_ok=True)
with (B/'generated/audit/recomputed_action_intervals.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(derived[0]));w.writeheader();w.writerows(derived)
# Numerical geometry and final research-participant labels are exported by the current plotting script.
geometry=B/'generated/audit/figure_geometry_measurements.json'
if geometry.exists():
 g=json.loads(geometry.read_text());ratios=[m['b_over_a'] for m in g['metrics']]
 check('geometry-raw-ratios',all(abs(x-y)<1e-12 for x,y in zip(ratios,[1.0001516758847848,.9991630040254492,1.3910371838889106])),ratios)
 check('geometry-display-ratios',g['display_ratios']==['1.00','1.00','1.39'])
 check('geometry-reconstruction',g['reconstruction_max_absolute_difference_m']<1e-10,g['reconstruction_max_absolute_difference_m'])
else:check('geometry-build-present',False)
ratings=list(csv.DictReader((B/'inputs/questionnaire/survey_confirmed.tsv').open(encoding='utf-8-sig'),delimiter='\t'))
na=[(x['record_id'],q) for x in ratings for q in [f'Q{i:02}' for i in range(1,13)] if x[q]=='NA']
check('questionnaire-48-and-2-NA',len(ratings)==48 and na==[('G04_P08_R01','Q01'),('G04_P08_R02','Q01')],na)
figures=[]
for f in json.loads((B/'specs/current_figure_pixels.json').read_text()):
 p=B/'generated/figures'/f"{f['name']}.png"
 if not p.exists():check('figure:'+f['figure_id'],False,'Not generated');continue
 im=Image.open(p).convert('RGBA');pixel=hashlib.sha256(im.tobytes()).hexdigest();same=list(im.size)==f['size'] and pixel==f['rgba_pixel_sha256']
 check('figure-pixels:'+f['figure_id'],same,{'name':f['name'],'pixels_equal_to_v1_1':same,'size':list(im.size),'png_sha256':sha(p),'rgba_pixel_sha256':pixel})
 figures.append({'figure':f['figure_id'],'name':f['name'],'pixels_equal':same})
report['figures']=figures
report['raw_validation']='All six selected traces checked field-by-field against four raw logs.' if rawdir is not None and not any(x.startswith('raw') for x in report['failures']) else ('NOT RUN: supply --raw-dir to verify the originals; slice and interval checks still run.' if rawdir is None else 'FAILED')
report['boundaries']=['Participant intentions and judgments of correctness are not inferred from grab counts.','Video and active-task clocks stay distinct.','Pixel matching establishes the figures reproduce this thesis version, not that every scientific interpretation is independently confirmed.','Numerical outputs and PNG pixels should match with the recorded environment. PDF/SVG byte hashes can differ because of timestamps and internal identifiers.']
report['status']='PASS' if not report['failures'] else 'FAIL'
(B/'generated/audit/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({'status':report['status'],'checks':len(report['checks']),'failures':report['failures'],'raw_validation':report['raw_validation'],'figures':figures},ensure_ascii=False))
sys.exit(bool(report['failures']))
