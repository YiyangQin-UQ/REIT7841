from portable_metadata import dumps as portable_json
from pathlib import Path
import json,hashlib,sys,os
os.environ.setdefault('MPLCONFIGDIR', str(Path(__import__('tempfile').gettempdir())/'reit-figure-mpl-cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
PROJECT=Path(__file__).resolve().parent.parent
ROOT=PROJECT/'inputs'
OUT=PROJECT/'generated/figures'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'pdf.fonttype':42,'svg.fonttype':'none'})
frames=[('G01_R02_0280.0_crop.png','a  P01 builds','Frame 04:40','Small triangle + parallelogram:\nthe head–neck combination.'),('G01_R02_0363.0_crop.png','b  P02 tidies','Frame 06:03','P02 tidies the existing\nhead–neck combination.'),('G01_R02_0388.0_crop.png','c  P01 revises','Frame 06:28','P01 rotates the parallelogram\nto join a large triangle.')]
fig=plt.figure(figsize=(180/25.4,126/25.4),facecolor='white')
fig.text(.035,.96,'A participant revises their own local solution',fontsize=12,weight='bold',va='top')
fig.text(.035,.905,'G01 · Physical overhead view · Goose task',fontsize=9.5,color='#444444',va='top')
for i,(fn,title,stamp,desc) in enumerate(frames):
 x=.035+i*.322
 ax=fig.add_axes([x,.245,.286,.586]);ax.imshow(Image.open(ROOT/'self_revision_frames'/fn),interpolation='none');ax.set_xticks([]);ax.set_yticks([]);ax.set_axis_off()
 fig.text(x,.839,title,fontsize=10.5,weight='bold',va='bottom')
 fig.text(x,.226,stamp,fontsize=9,weight='bold',va='top')
 fig.text(x,.179,desc,fontsize=8.6,va='top',linespacing=1.4)
fig.text(.035,.087,'Researcher-reported action anchors: approximately 04:38, 06:01 and 06:26.',fontsize=8.2,va='top')
fig.text(.035,.049,'The initial head–neck combination was judged correct; P01’s later revision was judged incorrect.',fontsize=8.2,va='top')
for ext in ['png','pdf','svg']:
 fig.savefig(OUT/f'F4_self_revision.{ext}',dpi=300,facecolor='white')

meta=json.loads((ROOT/'F4_self_revision_manifest.json').read_text())
meta['caption']=meta['caption'].replace('(a) A joins','(a) P01 joins').replace('(b) B tidies','(b) P02 tidies').replace('(c) A rotates','(c) P01 rotates').replace('that B only aligned','that P02 only aligned')
meta['participant_mapping']={'physical_original_A':'P01','physical_original_B':'P02'}
meta['outputs']=[{'path':str(OUT/f'F4_self_revision.{ext}'),'sha256':hashlib.sha256((OUT/f'F4_self_revision.{ext}').read_bytes()).hexdigest()} for ext in ['png','pdf','svg']]
meta['script']=str(Path(__file__));meta['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
meta['unchanged_crops']=[{'path':str(ROOT/'self_revision_frames'/f[0]),'sha256':hashlib.sha256((ROOT/'self_revision_frames'/f[0]).read_bytes()).hexdigest()} for f in frames]
meta['visual_qa']={'pixel_review_done':False}
(PROJECT/'generated/audit/figure_self_revision_build.json').write_text(portable_json(meta,ensure_ascii=False,indent=2))
print('G01 self-revision: exported PNG/PDF/SVG')
