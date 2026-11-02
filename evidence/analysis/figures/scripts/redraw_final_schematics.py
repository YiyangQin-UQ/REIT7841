from portable_metadata import dumps as portable_json
"""Resize only the two explanatory schematics, preserving their source text and graph."""
from pathlib import Path
import ast
import hashlib
import json
import os
import re
import shutil
import sys
import subprocess

os.environ.setdefault('MPLCONFIGDIR', str(Path(__import__('tempfile').gettempdir())/'reit-figure-mpl-cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

BASE=Path(__file__).resolve().parent.parent
OUT=BASE/'generated/figures'
HISTORY_SOURCE=BASE/'scripts/build_auxiliary_figures.py'
FLOW_SOURCE=BASE/'scripts/draw_method_figures.py'
NAMES = ['Figure3_1_research_development', 'Figure4_1_analysis_flow']
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8.5,
                     'text.color': '#23343D', 'pdf.fonttype': 42,
                     'svg.fonttype': 'none', 'savefig.transparent': False})

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def words(value):
    return re.sub(r'\s+', ' ', value).strip()

history_ast = ast.parse(HISTORY_SOURCE.read_text())
history_nodes = next(ast.literal_eval(n.value) for n in history_ast.body
                     if isinstance(n, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id == 'nodes' for t in n.targets))
flow_ast = ast.parse(FLOW_SOURCE.read_text())
flow_nodes = []
for item in flow_ast.body:
    if isinstance(item, ast.Expr) and isinstance(item.value, ast.Call):
        call = item.value
        if isinstance(call.func, ast.Name) and call.func.id == 'node':
            flow_nodes.append([ast.literal_eval(v) for v in call.args])
assert len(history_nodes) == 5 and len(flow_nodes) == 8

manifest={'purpose':'Reproduce the final layout-adjusted explanatory schematics.','figures':[]}

def export(fig, name, size, original_nodes, text_artists, edges, source):
    expected = [part for node in original_nodes for part in node]
    drawn = [artist.get_text() for artist in text_artists]
    assert [words(x) for x in expected] == [words(x) for x in drawn]
    outputs=[]
    for ext in ('pdf','png','svg'):
        path=OUT/f'{name}.{ext}';fig.savefig(path,dpi=300,facecolor='white')
        outputs.append({'path':str(path.relative_to(BASE)),'sha256':sha(path)})
    plt.close(fig)
    manifest['figures'].append({'name':name,'physical_size_mm':size,'source_text_sequence':expected,'drawn_text_sequence':drawn,'text_word_order_unchanged':True,'semantic_edges':edges,'outputs':outputs})

# Figure 3.1 retains its five-node sequence, colours and downward arrows.
fig = plt.figure(figsize=(160/25.4, 95/25.4))
ax = fig.add_axes([0, 0, 1, 1]); ax.set(xlim=(0,1), ylim=(0,1)); ax.axis('off')
texts = []
for i, (title, body) in enumerate(history_nodes):
    y = .817 - i * .195
    fc = '#D9E7F0' if i == 0 else ('#D8EBE6' if i == 4 else '#F1F5F7')
    ax.add_patch(Rectangle((.025, y), .95, .15, facecolor=fc,
                           edgecolor='#ACBBC5', linewidth=.65))
    texts.append(ax.text(.045, y+.113, title, fontsize=9.1, weight='bold', va='center'))
    texts.append(ax.text(.045, y+.073, body, fontsize=8.5, va='top', linespacing=1.12))
    if i < 4:
        ax.annotate('', xy=(.5,y-.036), xytext=(.5,y-.004),
                    arrowprops={'arrowstyle':'-|>', 'color':'#345366', 'lw':.9,
                                'mutation_scale':10})
export(fig, NAMES[0], [160,95], history_nodes, texts,
       [[history_nodes[i][0],history_nodes[i+1][0]] for i in range(4)], HISTORY_SOURCE)

# Figure 4.1 retains all eight nodes and both branch/convergence paths.
fig = plt.figure(figsize=(160/25.4, 125/25.4))
ax = fig.add_axes([.015,.01,.97,.98]); ax.set(xlim=(0,1),ylim=(0,1)); ax.axis('off')
texts = []
for i, (x,y,w,h,title,detail) in enumerate(flow_nodes):
    fc = '#EDF5FA' if i == 3 else '#EDF7F1' if i == 4 else '#FFF5DF' if i == 7 else '#F5F8FA'
    ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,
                 boxstyle='round,pad=.006,rounding_size=.012',
                 facecolor=fc,edgecolor='#66798A',lw=.85))
    texts.append(ax.text(x,y+h*.20,title,fontsize=9,weight='bold',color='#152536',
                        ha='center',va='center',linespacing=1.12))
    texts.append(ax.text(x,y-h*.17,detail,fontsize=8.5,color='#152536',
                        ha='center',va='center',linespacing=1.12))
def arrow(a,b,style='-',color='#475569'):
    ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'-|>','color':color,
                   'lw':1.1,'linestyle':style,'shrinkA':1,'shrinkB':1})
for a,b in [((.38,.865),(.38,.84)),((.38,.71),(.38,.685)),
            ((.30,.555),(.25,.52)),((.52,.555),(.75,.52)),
            ((.25,.35),(.35,.31)),((.75,.35),(.65,.31)),
            ((.50,.18),(.50,.14))]: arrow(a,b)
ax.plot([.98,.995],[.735,.735],'--',color='#9F6800',lw=1.1)
ax.plot([.995,.995],[.735,.245],'--',color='#9F6800',lw=1.1)
arrow((.995,.245),(.88,.245),'--','#9F6800')
edges = [[0,1],[1,2],[2,3],[2,4],[3,5],[4,5],[5,6],[7,5]]
export(fig, NAMES[1], [160,125], [(n[4],n[5]) for n in flow_nodes],texts,
       [[flow_nodes[a][4],flow_nodes[b][4]] for a,b in edges],FLOW_SOURCE)
(BASE/'generated/audit/final_schematics_build.json').write_text(portable_json(manifest,ensure_ascii=False,indent=2))
print('Exported final layout-adjusted schematics')
