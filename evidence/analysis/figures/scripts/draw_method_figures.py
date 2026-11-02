from portable_metadata import dumps as portable_json
from pathlib import Path
import json,hashlib,os
os.environ.setdefault('MPLCONFIGDIR', str(Path(__import__('tempfile').gettempdir())/'reit-figure-mpl-cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,Polygon,Rectangle,Ellipse
B=Path(__file__).resolve().parents[1];O=B/'generated/figures'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'pdf.fonttype':42,'svg.fonttype':'none','axes.linewidth':.7})
blue='#0072B2';green='#008568';orange='#9F6800';gray='#475569';dark='#152536'
manifest=[]
def line(ax,a,b,style='-',c=gray,arrow=False):
 if arrow:ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'-|>','color':c,'lw':1.1,'linestyle':style,'shrinkA':1,'shrinkB':1})
 else:ax.plot([a[0],b[0]],[a[1],b[1]],style,color=c,lw=1.1)
def text(ax,x,y,s,size=8.5,weight='normal',c=dark,ha='center',va='center'):
 return ax.text(x,y,s,fontsize=size,weight=weight,color=c,ha=ha,va=va,linespacing=1.18,zorder=5,bbox={'facecolor':'white','edgecolor':'none','pad':0.5} if s in ['Direct sight\nand physical contact','Camera phone','Sight barriers','Physical pieces','Viewing\nphone','Two local eye views','Shared virtual pieces'] else None)
def box(ax,x,y,w,h,label,fc='#F5F8FA',ec=gray,fs=8.5):
 ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle='round,pad=0.008,rounding_size=0.018',facecolor=fc,edgecolor=ec,lw=.8));text(ax,x,y,label,fs)
def pieces(ax,x=.5,y=.49,virtual=False):
 c=green if virtual else blue
 ax.add_patch(Rectangle((x-.155,y-.08),.31,.16,facecolor='#F6F8FA',edgecolor=c,lw=1))
 polys=[[(x-.12,y-.045),(x-.045,y+.047),(x-.045,y-.045)],[(x-.02,y-.045),(x+.06,y-.045),(x+.06,y+.035)],[(x+.085,y-.045),(x+.135,y-.045),(x+.135,y+.005),(x+.085,y+.005)]]
 for p in polys:ax.add_patch(Polygon(p,facecolor=c,alpha=.65,edgecolor=c,lw=.5))
def phone(ax,x,y,large=False):
 w=.12 if large else .10;h=.19 if large else .15
 ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle='round,pad=0.002,rounding_size=0.012',facecolor='white',edgecolor=dark,lw=.9));ax.add_patch(Rectangle((x-w*.38,y-h*.34),w*.76,h*.68,facecolor='#FFF1D4',edgecolor=orange,lw=.5))
def headset(ax,x,y,screen=False):
 ax.add_patch(FancyBboxPatch((x-.10,y-.045),.20,.09,boxstyle='round,pad=.003,rounding_size=.025',facecolor='#ECF6F1',edgecolor=dark,lw=1))
 if screen:ax.add_patch(Rectangle((x-.069,y-.023),.138,.046,facecolor='#FFE5AF',edgecolor=orange,lw=.7))
def export(fig,name,spec):
 for ext in ['pdf','png','svg']:fig.savefig(O/(name+'.'+ext),dpi=240,facecolor='white')
 manifest.append({'id':spec['figure_id'],'claim':spec['claim'],'type':'schematic','source_spec':str((B/'specs'/spec['_file']).relative_to(B)),'spec_sha256':hashlib.sha256((B/'specs'/spec['_file']).read_bytes()).hexdigest(),'caption':spec['caption'],'outputs':[{'path':str((O/(name+'.'+ext)).relative_to(B)),'sha256':hashlib.sha256((O/(name+'.'+ext)).read_bytes()).hexdigest()} for ext in ['pdf','png','svg']],'engine':'matplotlib','visual_review':'pending','data_generated':False})
 plt.close(fig)
fig,axs=plt.subplots(2,2,figsize=(160/25.4,157/25.4));fig.subplots_adjust(.015,.095,.985,.99,wspace=.055,hspace=.07)
for ax in axs.flat:
 ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off');ax.add_patch(FancyBboxPatch((.005,.005),.99,.99,boxstyle='round,pad=0,rounding_size=.02',fill=False,ec='#CBD5E1',lw=.7))
a=axs[0,0];text(a,.5,.92,'(a) R01 · Physical direct',9,'bold');pieces(a,.5,.56);text(a,.5,.70,'Shared physical pieces');
for x in [.18,.82]:
 a.add_patch(Ellipse((x,.24),.12,.12,facecolor='#E8F2F9',edgecolor=blue,lw=.8));text(a,x,.10,'Participant',8.5);line(a,(x,.31),(.4 if x<.5 else .6,.49),'--',blue);line(a,(x+.06 if x<.5 else x-.06,.29),(.45 if x<.5 else .55,.47),'-',dark,True)
text(a,.5,.35,'Direct sight\nand physical contact',8.5)
a=axs[0,1];text(a,.5,.92,'(b) R02 · Physical overhead',9,'bold');phone(a,.5,.74);text(a,.5,.59,'Camera phone',8.5);pieces(a,.5,.37);text(a,.5,.25,'Physical pieces',8.5)
for x in [.13,.87]:
 phone(a,x,.39);text(a,x,.22,'Viewing\nphone',8.5);line(a,(.5,.81),(x,.81),':',orange);line(a,(x,.81),(x,.48),':',orange,True);line(a,(x,.31),(x,.12),'-',dark);line(a,(x,.12),(.36 if x<.5 else .64,.12),'-',dark);line(a,(.36 if x<.5 else .64,.12),(.39 if x<.5 else .61,.29),'-',dark,True)
line(a,(.5,.45),(.5,.64),'--',blue);text(a,.5,.08,'Reach to move pieces',8.5);text(a,.23,.69,'Discord\nvideo',8.5,c=orange)
for x in [.29,.71]:a.plot([x,x],[.29,.48],color=gray,lw=3)
text(a,.5,.50,'Sight barriers',8.5)
a=axs[1,0];text(a,.5,.92,'(c) R03 · VR first person',9,'bold');pieces(a,.5,.60,True);text(a,.5,.74,'Shared virtual pieces');
for x in [.20,.80]:
 headset(a,x,.29);text(a,x,.18,'Quest 3',8.5);line(a,(x,.34),(.39 if x<.5 else .61,.54),'--',green)
text(a,.5,.43,'Two local eye views',8.5);box(a,.5,.07,.87,.10,'Tracked controllers: near / ray grab',fc='#F1F6F4',ec=green,fs=8.5);line(a,(.07,.12),(.07,.61),'-',dark);line(a,(.07,.61),(.34,.61),'-',dark,True)
a=axs[1,1];text(a,.5,.92,'(d) R04 · VR shared overhead',9,'bold');box(a,.5,.78,.84,.14,'Fixed orthographic camera',fc='#FFF5DF',ec=orange,fs=8.5);pieces(a,.5,.48,True);text(a,.5,.61,'Shared virtual pieces',8.5);line(a,(.5,.56),(.5,.70),'--',green)
for x in [.20,.80]:
 headset(a,x,.24,True);line(a,(.08 if x<.5 else .92,.77),(.08 if x<.5 else .92,.24),':',orange,True)
text(a,.5,.13,'Two head-following screens\ninside Quest 3 headsets',8.5)
line(a,(.13,.36),(.34,.46),'-',dark,True);line(a,(.87,.36),(.66,.46),'-',dark,True);text(a,.5,.34,'Tracked controllers',8.5)
# Legend placed in physical figure coordinates.
lax=fig.add_axes([.07,.015,.86,.055]);lax.axis('off');lax.set(xlim=(0,1),ylim=(0,1))
for x,sty,label,c in [(.02,'-','Action',dark),(.34,'--','View',blue),(.63,':','Video / display',orange)]:line(lax,(x,.65),(x+.075,.65),sty,c,sty=='-');text(lax,x+.09,.65,label,8.5,ha='left')
spec=json.loads((B/'specs/apparatus_figure_spec.json').read_text());spec['_file']='apparatus_figure_spec.json';export(fig,'Figure3_2_apparatus',spec)

fig=plt.figure(figsize=(160/25.4,151/25.4));ax=fig.add_axes([.015,.01,.97,.98]);ax.axis('off');ax.set(xlim=(0,1),ylim=(0,1))
def node(x,y,w,h,title,detail,fc='#F5F8FA',fs=8.5):
 ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle='round,pad=.006,rounding_size=.012',facecolor=fc,edgecolor='#66798A',lw=.85));text(ax,x,y+h*.20,title,9,'bold');text(ax,x,y-h*.17,detail,fs)
node(.38,.925,.70,.11,'Source records','Researcher reports · video · VR logs')
node(.38,.775,.70,.12,'Identify the task record','Dyad + condition + software attempt\nPractice, replay and restart kept distinct')
node(.38,.62,.70,.12,'Build a connected episode','Proposal / builder / modifier\nBefore → after → local outcome')
node(.25,.435,.46,.16,'Check action and meaning','Video anchors and researcher account\nKeep each source clock visible',fc='#EDF5FA',fs=8.3)
node(.75,.435,.46,.16,'Check actions and states','Accepted grab–release pairs\nLatest piece poses · selected geometry',fc='#EDF7F1',fs=8.3)
node(.50,.245,.74,.12,'Compare connected cases','Within a dyad, then across dyads\nRetain contrary cases and task differences')
node(.50,.075,.86,.12,'Write findings and interpretation','Distinguish observation, checked state and explanation\nRetain source codes')
node(.875,.735,.20,.23,'Context','48 survey\nrecords\n\nInterview\ncomments',fc='#FFF5DF',fs=8.3)
for a,b in [((.38,.865),(.38,.84)),((.38,.71),(.38,.685)),((.30,.555),(.25,.52)),((.52,.555),(.75,.52)),((.25,.35),(.35,.31)),((.75,.35),(.65,.31)),((.50,.18),(.50,.14))]:line(ax,a,b,'-',gray,True)
line(ax,(.98,.735),(.995,.735),'--',orange);line(ax,(.995,.735),(.995,.245),'--',orange);line(ax,(.995,.245),(.88,.245),'--',orange,True)
spec=json.loads((B/'specs/analysis_flow_figure_spec.json').read_text());spec['_file']='analysis_flow_figure_spec.json';export(fig,'Figure4_1_analysis_flow',spec)
(B/'generated/audit/method_figure_build.json').write_text(portable_json({'schema':'local.figure_build.v1','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'figures':manifest},indent=2))
print('Created 2 vector diagrams and PNG/SVG previews.')
