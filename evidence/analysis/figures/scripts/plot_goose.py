from portable_metadata import dumps as portable_json
from pathlib import Path
import json,hashlib,os
os.environ.setdefault('MPLCONFIGDIR', str(Path(__import__('tempfile').gettempdir())/'reit-figure-mpl-cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
PROJECT=Path(__file__).resolve().parent.parent
ROOT=PROJECT/'inputs'
HERE=PROJECT/'generated/figures'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
package=json.loads((ROOT/'fig07_g06_goose_provenance.json').read_text())
panels=[
 {'crop_image':ROOT/'goose/panel_a.png','action':'P11 tries a large triangle for the body','event':'Event ~00:33','frame':'Frame 00:34'},
 {'crop_image':ROOT/'goose/panel_b.png','action':'P12 adds a small triangle to the neck','event':'Event ~00:53','frame':'Frame 00:54'},
 {'crop_image':ROOT/'goose/panel_c.png','action':'P11 adds the medium triangle','event':'Event ~01:02','frame':'Frame 01:04'},
 {'crop_image':ROOT/'goose/panel_d.png','action':'P11 and P12 complete the goose','event':'Completion ~01:20','frame':'Later check: frame 01:40'}]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'pdf.fonttype':42,'svg.fonttype':'none'})
fig=plt.figure(figsize=(180/25.4,158/25.4))
fig.text(.025,.973,'G06: extending an existing partial arrangement in turn',fontsize=11,weight='bold',va='top')
fig.text(.025,.934,'Physical overhead condition · goose task',fontsize=8.5,va='top')
positions=[(.025,.53,.455,.31),(.52,.53,.455,.31),(.025,.12,.455,.31),(.52,.12,.455,.31)]
for i,(p,pos) in enumerate(zip(panels,positions)):
    ax=fig.add_axes(pos);ax.imshow(Image.open(p['crop_image']));ax.axis('off')
    title=p['action']
    fig.text(pos[0],pos[1]+pos[3]+.057,f'{chr(97+i)}  {title}',fontsize=8.7,weight='bold',va='top')
    fig.text(pos[0],pos[1]+pos[3]+.006,f"{p['event']}  |  {p['frame']}",fontsize=7.3,va='bottom',color='#41464B')
fig.text(.025,.067,'Actions and event times follow the researcher’s account. Frame times identify the recorded states shown.',fontsize=7.3)
fig.text(.025,.032,'Panel d shows the completed arrangement beside the partitioned reference during the later check.',fontsize=7.3)
outputs=[]
for ext in ['png','pdf','svg']:
    p=HERE/f'fig07_g06_goose_continuation.{ext}';fig.savefig(p,dpi=300,facecolor='white')
    outputs.append({'path':p.name,'sha256':sha(p),'width_mm':180,'height_mm':158})

package['caption']=package['caption'].replace('(a) A trying','(a) P11 trying').replace('(b) B attaching','(b) P12 attaching').replace('(c) A placing','(c) P11 placing')
package['participant_mapping']={'physical_original_A':'P11','physical_original_B':'P12'}
package['outputs']=outputs
package['reproduction']={'script':str(Path(__file__)),'sha256':sha(__file__)}
package['unchanged_crops']=[{'path':str(p['crop_image']),'sha256':sha(p['crop_image'])} for p in panels]
for record,panel in zip(package['frames'],panels):record['action']=panel['action']
package['pixel_review_done']=False
(PROJECT/'generated/audit/figure_goose_build.json').write_text(portable_json(package,ensure_ascii=False,indent=2))
print('G06 goose: exported PNG/PDF/SVG')
