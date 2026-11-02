from portable_metadata import dumps as portable_json
"""Rebuild case figures from saved mesh and recorded world poses; no invented coordinates."""
from pathlib import Path
import csv, json, math, hashlib, itertools, sys, os
os.environ.setdefault('MPLCONFIGDIR', str(Path(__import__('tempfile').gettempdir())/'reit-figure-mpl-cache'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image

PROJECT=Path(__file__).resolve().parent.parent
ROOT=PROJECT/'generated/figures'
REV=PROJECT/'generated/audit'
INP=PROJECT/'inputs/geometry'
GEO=json.loads((INP/'geometry_from_backup.json').read_text())['geometry']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.titlesize':9,
    'svg.fonttype':'none','pdf.fonttype':42,'savefig.facecolor':'white'})
COLORS=dict(zip(['S1','S2','S3','S4','S5','S6','S7'],
    ['#CC79A7','#D9D9D9','#0072B2','#009E73','#56B4E9','#D55E00','#F0E442']))
OUTPUTS=[]
QA=[]

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def hull(pts):
    pts=sorted(set(tuple(p) for p in pts))
    def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[];up=[]
    for p in pts:
        while len(lo)>1 and cross(lo[-2],lo[-1],p)<=0:lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up)>1 and cross(up[-2],up[-1],p)<=0:up.pop()
        up.append(p)
    return lo[:-1]+up[:-1]
def rotate(v,q):
    x,y,z,w=np.array(q)/np.linalg.norm(q)
    tx=2*(y*v[2]-z*v[1]);ty=2*(z*v[0]-x*v[2]);tz=2*(x*v[1]-y*v[0])
    return [v[0]+w*tx+y*tz-z*ty,v[1]+w*ty+z*tx-x*tz,v[2]+w*tz+x*ty-y*tx]
def read(slot):return list(csv.DictReader((INP/f'{slot}.csv').open(encoding='utf-8-sig')))
def reconstruct(slot,t):
    latest={}
    for r in read(slot):
        if r['active_elapsed_s'] and float(r['active_elapsed_s'])<=t and r['piece_id'] in GEO and r['position_x_m'] and r['event'] in {'piece_initial','piece_pose','piece_release','piece_settle_pose','piece_settled'}:
            latest[r['piece_id']]=r
    out={}
    for k,r in latest.items():
        pos=[float(r[f'position_{x}_m']) for x in 'xyz'];q=[float(r[f'rotation_{x}']) for x in 'xyzw']
        world=[np.array(rotate([v*GEO[k]['scale'] for v in p],q))+pos for p in GEO[k]['points']]
        out[k]={'hull_xz':hull([(p[0],p[2]) for p in world]),'source_line':r['source_line'],
                'last_pose_age_s':t-float(r['active_elapsed_s']),'event':r['event'],'held_by':r['held_by']}
    return out
def draw(ax,state,transform=None,ids=True):
    for k,item in sorted(state.items()):
        p=np.asarray(item['hull_xz']);p=p if transform is None else transform(p)
        ax.add_patch(Polygon(p,facecolor=COLORS[k],edgecolor='#30343A',linewidth=.55))
        if ids:
            c=p.mean(0)
            ax.text(*c,k,ha='center',va='center',fontsize=7.2,color='#111111',
                    bbox={'facecolor':'white','edgecolor':'none','alpha':.7,'pad':.35})
    ax.set_aspect('equal');ax.axis('off')
def save(fig,name,width,height):
    fig.set_size_inches(width/25.4,height/25.4)
    fig.canvas.draw()
    # Export identical drawing instructions without the local skill QA import.
    for ext in ['png','pdf','svg']:
        p=ROOT/f'{name}.{ext}';fig.savefig(p,dpi=300)
        OUTPUTS.append({'path':p.name,'sha256':sha(p),'width_mm':width,'height_mm':height})
    plt.close(fig)

sequence=json.loads((INP/'G06_candle_sequence.json').read_text())
outcomes=json.loads((INP/'three_candle_outcomes.json').read_text())
maxdiff=0.
for st in sequence+outcomes:
    fresh=reconstruct(st['slot'],st['time'])
    for k,v in fresh.items():
        assert v['source_line']==st['state'][k]['source_line']
        maxdiff=max(maxdiff,float(np.max(np.abs(np.asarray(v['hull_xz'])-st['state'][k]['hull_xz']))))
    st['state']=fresh
assert maxdiff<1e-10

# Same coordinates, scale and orientation across the six snapshots.
points=np.concatenate([np.asarray(x['hull_xz']) for st in sequence for x in st['state'].values()])
xmin,zmin=points.min(0);xmax,zmax=points.max(0)
fig,axes=plt.subplots(2,3)
fig.subplots_adjust(left=.025,right=.975,bottom=.075,top=.89,wspace=.09,hspace=.26)
fig.text(.025,.965,'G06: rebuilding a near-complete candle',fontsize=11,weight='bold')
fig.text(.025,.929,'First-person VR round · analytical top projections from recorded poses',fontsize=8)
labels=['Six-piece candidate','Trying the remaining piece','Opening the body',
        'New upper-body anchor','Medium triangle incorporated','Seven-piece configuration']
for i,(ax,st,label) in enumerate(zip(axes.flat,sequence,labels)):
    draw(ax,st['state']);ax.set_xlim(xmin-.04,xmax+.04);ax.set_ylim(zmin-.04,zmax+.04)
    ax.set_title(f"{chr(97+i)}  {st['time']:.0f} s · {label}",loc='left',fontsize=7.8,pad=8)
axes[0,0].text(.5,-.03,'S2 remains outside the candidate',ha='center',transform=axes[0,0].transAxes,fontsize=7)
axes[1,2].text(.5,-.03,'Accepted in the session; geometry differs',ha='center',transform=axes[1,2].transAxes,fontsize=7)
fig.text(.025,.03,'Times are active task seconds. Common world scale and orientation; no snapping or rearrangement.',fontsize=7.4)
save(fig,'fig01_g06_reconstruction_sequence',180,151)

def dimensions(st,upper,lower):
    state=st['state'];a,b=max(itertools.combinations(state[upper]['hull_xz'],2),key=lambda p:math.dist(*p))
    a,b=np.array(a),np.array(b)
    if a[0]>b[0]:a,b=b,a
    length=np.linalg.norm(b-a);u=(b-a)/length;v=np.array([-u[1],u[0]])
    center=(a+b)/2
    trans=lambda p:np.column_stack(((p-center)@u,(p-center)@v))
    lowerpts=trans(np.concatenate([np.asarray(state[k]['hull_xz']) for k in lower]))
    lo,hi=lowerpts[:,0].min(),lowerpts[:,0].max()
    return {'slot':st['slot'],'active_elapsed_s':st['time'],'a_m':float(length),
            'b_m':float(hi-lo),'b_over_a':float((hi-lo)/length),'upper_piece':upper,
            'lower_pieces':lower,'source_lines':{k:state[k]['source_line'] for k in [upper]+lower},
            'lower_extent':[float(lo),float(hi)],'lower_min_y':float(lowerpts[:,1].min())},trans
measurements=[];transforms=[]
for st,up,low in zip(outcomes,['S6','S5','S6'],[['S5'],['S6'],['S1','S5','S3']]):
    m,t=dimensions(st,up,low);measurements.append(m);transforms.append(t)
previous=json.loads((INP/'01_上下外沿测量及来源.json').read_text())
for now,old in zip(measurements,previous['metrics']):
    assert abs(now['b_over_a']-old['lower_upper_ratio'])<1e-12
later=[r for r in read('G06_R03') if r['piece_id'] in {'S1','S3','S5','S6'}
       and r['active_elapsed_s'] and float(r['active_elapsed_s'])>214
       and r['event'] in {'grab_accepted','piece_pose','piece_release','piece_settle_pose','piece_settled'}]
assert not later
target=np.asarray(Image.open(INP/'00_vela-5_silhouette.png').convert('RGBA'))
mask=(target[:,:,3]>128)&(target[:,:,:3].max(2)<100)
assert all(mask[y].sum()==364 for y in [451,452,812,813])

def dimension_annotation(ax,m):
    a=m['a_m'];lo,hi=m['lower_extent'];yb=m['lower_min_y']-.055
    ax.annotate('',xy=(-a/2,.025),xytext=(a/2,.025),arrowprops={'arrowstyle':'|-|','color':'#20252B','linewidth':.8})
    ax.text(a/2+.025,.025,'a',fontsize=8,va='center')
    for x in [lo,hi]:ax.plot([x,x],[m['lower_min_y'],yb],color='#4B5563',lw=.5,ls=':')
    ax.annotate('',xy=(lo,yb),xytext=(hi,yb),arrowprops={'arrowstyle':'|-|','color':'#20252B','linewidth':.8})
    ax.text(hi+.025,yb,'b',fontsize=8,va='center')

fig,axes=plt.subplots(1,4)
fig.subplots_adjust(left=.025,right=.975,bottom=.25,top=.83,wspace=.12)
fig.text(.025,.954,'A geometric check of the accepted candle configurations',fontsize=10.5,weight='bold')
fig.text(.025,.908,'Target silhouette and three first-person VR cases · analytical top projections',fontsize=8)
# Original target silhouette: one uniform scale, fixed to 0.44 m body width only for display.
yy,xx=np.where(mask);crop=mask[yy.min():yy.max()+1,xx.min():xx.max()+1]
scale=.44/364
rgba=np.zeros((*crop.shape,4),dtype=np.uint8);rgba[:,:,:3]=55;rgba[:,:,3]=crop*255
axes[0].imshow(rgba,extent=[(xx.min()-424.5)*scale,(xx.max()+1-424.5)*scale,
                         (451-(yy.max()+1))*scale,(451-yy.min())*scale],interpolation='nearest')
axes[0].set_title('a  Target',loc='left');axes[0].text(.5,-.08,'b/a = 1.00',transform=axes[0].transAxes,ha='center',weight='bold')
for i,(ax,st,m,tr) in enumerate(zip(axes[1:],outcomes,measurements,transforms),1):
    draw(ax,st['state'],tr);dimension_annotation(ax,m)
    ax.set_title(f"{chr(97+i)}  {st['slot'][:3]} · {st['time']} s",loc='left')
    ax.text(.5,-.08,f"b/a = {m['b_over_a']:.2f}",transform=ax.transAxes,ha='center',weight='bold')
for ax in axes:
    ax.set_xlim(-.40,.40);ax.set_ylim(-.52,.55);ax.set_aspect('equal');ax.axis('off')
fig.text(.025,.157,'a: longest chord of the upper large triangle.  b: lower-piece extent projected along that chord.',fontsize=7.4)
fig.text(.025,.108,'Whole layouts are rigidly aligned to a; all three cases retain the same world scale.',fontsize=7.4)
fig.text(.025,.059,'Target scaled uniformly for comparison. This ratio measures one geometric relation, not total shape error.',fontsize=7.4)
save(fig,'fig02_candle_geometry_comparison',180,111)

fig=plt.figure()
fig.text(.025,.955,'G06 near completion: recorded view and geometric reconstruction',fontsize=10.5,weight='bold')
ax1=fig.add_axes([.025,.23,.60,.62]);ax2=fig.add_axes([.665,.23,.30,.62])
ax1.imshow(Image.open(INP/'G06_R03_00945.000.jpg'));ax1.axis('off')
ax1.set_title('a  Recorded first-person view · video 15:45',loc='left',fontsize=8.5)
draw(ax2,outcomes[-1]['state'],transforms[-1]);dimension_annotation(ax2,measurements[-1])
ax2.set_xlim(-.42,.42);ax2.set_ylim(-.52,.56)
ax2.set_title('b  Top projection · log 214 s',loc='left',fontsize=8.5)
fig.text(.68,.18,'a = 0.440 m     b = 0.612 m',fontsize=8)
fig.text(.025,.12,'The same near-end arrangement is shown in two records; the video and log use separate clocks.',fontsize=7.4)
fig.text(.025,.07,'Recorded frame is unchanged. Projection uses logged geometry; colours are relabelled by piece ID.',fontsize=7.4)
save(fig,'fig03_g06_recorded_view_and_geometry',180,109)

# Same-piece provenance: P2 revisits both small triangles, then P1 takes them up.
g03_states=[{'slot':'G03_R03','time':t,'state':reconstruct('G03_R03',t)} for t in [52,73,99]]
g03_events=[{k:r[k] for k in ['active_elapsed_s','event','participant_id','piece_id','source_line']}
            for r in read('G03_R03') if r['piece_id'] in ['S1','S3'] and r['active_elapsed_s']
            and float(r['active_elapsed_s'])<=99 and r['event'] in ['grab_accepted','piece_release','piece_settled']]
fig,axes=plt.subplots(1,3)
fig.subplots_adjust(left=.025,right=.975,bottom=.26,top=.81,wspace=.12)
fig.text(.025,.953,'G03: revisiting one’s own pieces, then taking up a partner’s work',fontsize=10.2,weight='bold')
fig.text(.025,.904,'First-person VR round · the same two small triangles (S1 and S3) across three states',fontsize=8)
allpoints=np.concatenate([np.asarray(v['hull_xz']) for st in g03_states for v in st['state'].values()])
lo=allpoints.min(0);hi=allpoints.max(0)
for i,(ax,st) in enumerate(zip(axes,g03_states)):
    for k,v in sorted(st['state'].items(),key=lambda x:x[0] in ['S1','S3']):
        pts=np.asarray(v['hull_xz']);focus=k in ['S1','S3']
        ax.add_patch(Polygon(pts,facecolor=COLORS[k] if focus else '#ECEFF1',
                            edgecolor='#20252B' if focus else '#ADB5BD',linewidth=1.0 if focus else .45))
        c=pts.mean(0);ax.text(*c,k,ha='center',va='center',fontsize=8 if focus else 6.8,
                            color='#101418' if focus else '#737B83',
                            bbox={'facecolor':'white','edgecolor':'none','alpha':.75,'pad':.35})
    ax.set_xlim(lo[0]-.05,hi[0]+.05);ax.set_ylim(lo[1]-.05,hi[1]+.05)
    ax.set_aspect('equal');ax.axis('off')
    titles=['P05 forms a two-piece shape','P05 separates the two pieces','P06 takes up both pieces']
    ax.set_title(f"{chr(97+i)}  {st['time']} s · {titles[i]}",loc='left',fontsize=8)
    grabs=['P05 grabs: 36.14 s / 48.07 s','P05 grabs: 67.38 s / 69.33 s','P06 grabs: 93.56 s / 96.29 s']
    ax.text(.5,-.10,grabs[i],ha='center',transform=ax.transAxes,fontsize=7.6)
fig.text(.025,.13,'Snapshots follow logged settling events. Common world scale and orientation; other pieces provide context.',fontsize=7.3)
fig.text(.025,.07,'Recorded actions and spatial changes show self-revision followed by partner continuation.',fontsize=7.3)
save(fig,'fig04_g03_self_revision_and_continuation',180,113)

for event in g03_events:
    event['research_participant_id']={'P1':'P06','P2':'P05'}.get(event['participant_id'])
(REV/'figure_g03_piece_continuation_evidence.json').write_text(portable_json({'states':g03_states,'events':g03_events,'software_to_research_participant':{'P1':'P06','P2':'P05'},'time_selection':'52/73/99 s follow settling events at 51.522347/72.517809/98.698791 s','clock_boundary':'Video and activity clocks remain distinct. Mapping does not make video B03:06 equal to log 67.38 s.'},ensure_ascii=False,indent=2))
(REV/'figure_geometry_measurements.json').write_text(portable_json({'metrics':measurements,'display_ratios':[format(m['b_over_a'],'.2f') for m in measurements],'reconstruction_max_absolute_difference_m':maxdiff,'target_pixel_spans':[364]*4},indent=2))
(REV/'figure_geometry_build.json').write_text(portable_json({'outputs':OUTPUTS,'automated_layout':QA,'script_sha256':sha(__file__),'inputs':[{'path':str(p),'sha256':sha(p)} for p in sorted(INP.iterdir())],'pixel_review_done':False},ensure_ascii=False,indent=2))
print(portable_json({'geometry_outputs':len(OUTPUTS),'raw_ratios':[m['b_over_a'] for m in measurements],'max_coordinate_difference':maxdiff}))
