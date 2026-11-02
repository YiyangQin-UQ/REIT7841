from portable_metadata import dumps as portable_json
"""Print clarification copied from the original exact-interval plot.
Only two auxiliary text blocks change; all data and plotting coordinates are preserved.
Exact accepted-grab to release intervals; categorical rows, no statistical test.

Run with Python and requirements.txt from this package.
The archived paired intervals are independently re-derived by validate.py after
field-by-field verification against the original ResearchV2 CSV files.
"""
from pathlib import Path
import csv
import hashlib
import json
import os
import sys

os.environ.setdefault('MPLCONFIGDIR', str(Path(__import__('tempfile').gettempdir())/'reit-figure-mpl-cache'))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
LEGACY_DIR = PROJECT/'inputs'
DATA = LEGACY_DIR/'division_action_intervals.csv'
SOURCE = LEGACY_DIR/'division_evidence.json' 
with DATA.open(newline='', encoding='utf-8') as f:
    rows = [r for r in csv.DictReader(f) if r['slot'] == 'G06_R03']
assert len(rows) == 79
for r in rows:
    r['start'] = float(r['grab_active_s'])
    r['end'] = float(r['release_active_s'])
    assert r['end'] >= r['start']

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8,
                     'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none',
                     'axes.labelsize': 8, 'xtick.labelsize': 7.5, 'ytick.labelsize': 8})
fig = plt.figure(figsize=(180/25.4, 148/25.4), facecolor='white')
ax = fig.add_axes([.205, .27, .765, .52])
order = ['S7', 'S4', 'S6', 'S5', 'S2', 'S1', 'S3']
names = ['S7  Square', 'S4  Parallelogram', 'S6  Large triangle 2',
         'S5  Large triangle 1', 'S2  Medium triangle',
         'S1  Small triangle 1', 'S3  Small triangle 2']
ypos = {p: 6-i for i, p in enumerate(order)}
colors = {'P1': '#0072B2', 'P2': '#D55E00'}
markers = {'P1': 'o', 'P2': 's'}
lane_offsets = {'P1': .13, 'P2': -.13}

for i, p in enumerate(order):
    y = ypos[p]
    if i % 2 == 0:
        ax.axhspan(y-.45, y+.45, color='#F5F6F7', zorder=0)
    for endpoint in ['P1', 'P2']:
        ax.hlines(y+lane_offsets[endpoint], 0, 225.278664, colors='#DDE0E3', lw=.4, zorder=1)

snapshots = [45, 64, 83, 145, 184, 214]
for i, t in enumerate(snapshots, 1):
    ax.axvline(t, ymin=.02, ymax=.94, color='#8B929A', linestyle=(0, (2, 3)), linewidth=.55, zorder=1)
    ax.text(t, 6.64, str(i), ha='center', va='center', fontsize=7.5,
            bbox={'boxstyle': 'circle,pad=.15', 'fc': 'white', 'ec': '#757D86', 'lw': .6})

for r in rows:
    endpoint = r['endpoint']
    y = ypos[r['piece_id']] + lane_offsets[endpoint]
    ax.plot([r['start'], r['end']], [y, y], color=colors[endpoint], linewidth=2.9,
            solid_capstyle='butt', zorder=3)
    ax.plot(r['start'], y, markers[endpoint], color=colors[endpoint],
            markerfacecolor='white' if endpoint == 'P2' else colors[endpoint],
            markersize=2.7, markeredgewidth=.6, zorder=4)

ax.set_xlim(0, 225.278664)
# y is a categorical list of pieces with two distinct actor lanes, not a magnitude axis.
ax.set_yticks(list(range(6, -1, -1)), names)
ax.set_xticks(list(range(0, 211, 30)))
ax.set_xlabel('Active time since the formal round started (s)', labelpad=6)
ax.tick_params(axis='y', length=0, pad=8)
ax.tick_params(axis='x', length=3, color='#68717A')
ax.spines[['left', 'right', 'top']].set_visible(False)
ax.spines['bottom'].set_color('#98A0A8')
ax.margins(y=.03)

fig.text(.055, .955, 'G06: local work becomes shared rebuilding', fontsize=12, weight='bold', va='top')
fig.text(.055, .911, 'First-person VR · candle task · one dyad · all 79 accepted grab–release intervals',
         fontsize=8.3, color='#424A54', va='top')
legend = [Line2D([0], [0], color=colors[p], marker=markers[p], linewidth=2.9,
                 markerfacecolor='white' if p == 'P2' else colors[p], markersize=4,
                 label=label) for p, label in [('P1', 'P11: upper lane'), ('P2', 'P12: lower lane')]]
fig.legend(handles=legend, loc='upper left', bbox_to_anchor=(.052, .878), ncol=2,
           frameon=False, handlelength=2, columnspacing=2.8, fontsize=8.2)
fig.text(.205, .815, 'Dashed lines: reconstructed states at 45, 64, 83, 145, 184 and 214 s.',
         fontsize=9.0, color='#606974')

notes = [
    (.055, 'Early local work', 'P11 manipulates the large triangles;\nP12 places the square\nand parallelogram.'),
    (.375, '116.7–136.1 s', 'P12 also manipulates both large\ntriangles as the body is reconfigured.'),
    (.695, '204.0–207.5 s', 'P11 manipulates the parallelogram\npreviously handled by P12.'),
]
for x, title, body in notes:
    fig.text(x, .184, title, fontsize=8.3, weight='bold', va='top')
    fig.text(x, .150, body, fontsize=7.6, va='top', linespacing=1.5)
fig.text(.055, .025, 'Bars: grab-to-release intervals; blank spans: no piece held.',
         fontsize=9.0, color='#606974', va='bottom', linespacing=1.35)



# Independent source pairing and integrity checks are in validate.py.
outputs=[]
for ext in ['png','pdf','svg']:
    p=PROJECT/'generated/figures'/f'F3_G06_action_timeline.{ext}'
    fig.savefig(p,dpi=300,facecolor='white')
    outputs.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(PROJECT/'generated/audit/figure_timeline_build.json').write_text(portable_json({'outputs':outputs,'interval_count':79,'all_79_rows_loaded':True,'plotting_instructions':'unchanged from current v1.1 script','software_to_research_participant':{'P1':'P11','P2':'P12'},'data_sha256':hashlib.sha256(DATA.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'pixel_review_done':False},indent=2))
print(portable_json({'timeline_outputs':outputs,'intervals':len(rows)}))
