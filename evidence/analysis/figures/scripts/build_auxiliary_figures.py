from portable_metadata import dumps as portable_json
"""Reproduce the two auxiliary thesis figures from read-only recorded sources."""
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
from matplotlib.patches import Rectangle

PROJECT=Path(__file__).resolve().parent.parent
HERE=PROJECT/'generated/figures'
RAW=PROJECT/'inputs/questionnaire/survey_confirmed.tsv'
DICT=PROJECT/'inputs/questionnaire/question_dictionary.tsv'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source(path, role):
    return {'path': str(path), 'sha256': sha(path), 'role': role}


def save(fig, name):
    outputs = []
    for suffix in ('png', 'pdf', 'svg'):
        target = HERE / f'{name}.{suffix}'
        fig.savefig(target, dpi=300, facecolor='white')
        outputs.append({'path': f'figures/{target.name}', 'sha256': sha(target)})
    plt.close(fig)
    return outputs


plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 8,
    'axes.edgecolor': '#B9C2C8', 'axes.labelcolor': '#23343D',
    'text.color': '#23343D', 'xtick.color': '#23343D',
    'ytick.color': '#23343D', 'pdf.fonttype': 42,
    'svg.fonttype': 'none', 'savefig.transparent': False,
})

raw_rows = list(csv.DictReader(RAW.open(encoding='utf-8-sig'), delimiter='\t'))
dictionary = list(csv.DictReader(DICT.open(encoding='utf-8-sig'), delimiter='\t'))
assert len(raw_rows) == 48
assert len({x['record_id'] for x in raw_rows}) == 48
rows = []
na = []
for raw in raw_rows:
    row = {k: v for k, v in raw.items() if not k.startswith('Q')}
    for q in (f'Q{i:02}' for i in range(1, 13)):
        if raw[q] == 'NA':
            row[q] = None
            na.append({'record_id': raw['record_id'], 'item': q, 'source_value': 'NA'})
        else:
            assert raw[q] in ['1', '2', '3', '4', '5']
            row[q] = int(raw[q])
    rows.append(row)
assert na == [
    {'record_id': 'G04_P08_R01', 'item': 'Q01', 'source_value': 'NA'},
    {'record_id': 'G04_P08_R02', 'item': 'Q01', 'source_value': 'NA'},
]
participants = sorted({r['participant_id'] for r in rows})
assert participants == [f'P{i:02}' for i in range(1, 13)]
lookup = {(r['participant_id'], r['round_id']): r for r in rows}
for pid in participants:
    assert sum(r['participant_id'] == pid for r in rows) == 4
items = ['Q04', 'Q06', 'Q09', 'Q10', 'Q12']
titles = ['Q04\nExplain intended\nplacement', 'Q06\nKnow puzzle\nprogress',
          'Q09\nMove pieces', 'Q10\nRotate pieces', 'Q12\nSolve puzzle\ntogether']
translations = [
    'I could identify which piece my partner was referring to.',
    'I could understand where my partner wanted to place a piece.',
    'I could judge whether my partner understood my suggestion.',
    'I could clearly explain where I wanted to place a piece.',
    'I could follow what my partner was doing.',
    'I knew the current progress of the puzzle.',
    'We could coordinate the timing of our actions.',
    'I could adjust my actions to avoid interfering with my partner.',
    'I could move a piece to the location I intended.',
    'I could rotate a piece to the orientation I intended.',
    'I knew which part of the task I was responsible for.',
    'I felt that we were solving the puzzle together.',
]
paired = []
counts = {}
for q in items:
    changes = []
    for pid in participants:
        a, b = lookup[pid, 'R03'], lookup[pid, 'R04']
        assert a[q] is not None and b[q] is not None
        paired.append({'participant_id': pid, 'group_id': a['group_id'], 'item': q,
                       'R03': a[q], 'R04': b[q]})
        changes.append(b[q] - a[q])
    counts[q] = {'R04_higher': sum(x > 0 for x in changes),
                 'same': sum(x == 0 for x in changes),
                 'R04_lower': sum(x < 0 for x in changes)}

# Raw paired ordinal values: no mean, error bars, total score, or hypothesis test.
# Horizontal axes show the entire valid 1–5 scale. Vertical positions are IDs.
fig, axes = plt.subplots(1, 5, figsize=(160 / 25.4, 126 / 25.4), sharey=True)
fig.subplots_adjust(left=.140, right=.985, top=.785, bottom=.170, wspace=.31)
blue, orange = '#0072B2', '#D55E00'
for panel, (ax, q, title) in enumerate(zip(axes, items, titles)):
    for group in range(6):
        if group % 2 == 0:
            ax.axhspan(group * 2 - .5, group * 2 + 1.5, color='#F0F3F5', zorder=0)
        if group:
            ax.axhline(group * 2 - .5, color='#D2D9DD', lw=.5, zorder=1)
    for i, pid in enumerate(participants):
        a = lookup[pid, 'R03'][q]
        b = lookup[pid, 'R04'][q]
        ax.plot([a, b], [i, i], color='#6B747B', lw=1.05, zorder=2)
        ax.scatter(a, i, s=30, marker='o', facecolor='white', edgecolor=blue,
                   linewidth=1.0, zorder=3)
        ax.scatter(b, i, s=10, marker='s', facecolor=orange, edgecolor=orange,
                   linewidth=.7, zorder=4)
    ax.set(xlim=(.6, 5.4), ylim=(11.7, -.7), xticks=[1, 2, 3, 4, 5])
    ax.set_yticks(range(12))
    ax.set_yticklabels([f'G{i//2+1:02}  {pid}' for i, pid in enumerate(participants)], fontsize=7.7)
    ax.set_title(title, fontsize=8.1, pad=11, fontweight='bold', linespacing=1.25)
    ax.grid(axis='x', color='#DDE3E7', lw=.5, zorder=0)
    ax.tick_params(axis='x', labelsize=7.7, length=2, pad=4)
    ax.tick_params(axis='y', length=0, pad=7)
    for side in ['top', 'right', 'left']:
        ax.spines[side].set_visible(False)
legend = [Line2D([], [], marker='o', markersize=5.8, markerfacecolor='white',
                 markeredgecolor=blue, color='none', label='R03: first-person VR'),
          Line2D([], [], marker='s', markersize=4.2, markerfacecolor=orange,
                 markeredgecolor=orange, color='none', label='R04: shared overhead VR')]
fig.legend(handles=legend, loc='upper center', bbox_to_anchor=(.57, .993),
           ncol=2, frameon=False, fontsize=8.1, handletextpad=.4, columnspacing=1.3)
fig.text(.57, .090, 'Item rating (1–5)', ha='center', fontsize=8.2)
fig.text(.025, .038, '12 participants; each row connects the same person’s two responses.', fontsize=7.7)
fig.text(.025, .010, 'A square inside a circle indicates equal ratings.', fontsize=7.7)
rating_outputs = save(fig, 'Figure5_8_VR_item_ratings')

paragraphs = [
    'The questionnaire adds a participant-level account of placement communication, progress awareness, piece control and joint solving (Figure 5.8). Ratings differed across these aspects. From first-person VR (R03) to shared overhead VR (R04), three participants rated explaining an intended placement more highly, eight gave the same rating and one gave a lower rating. Movement and rotation each received lower ratings from five participants, the same ratings from six and a higher rating from one. Communicating a placement and controlling a piece were therefore distinct aspects of the reported experience.',
    'The differences are visible within dyads. In G05, both participants rated explaining a placement more highly in R04, while their ratings of solving together fell from 5 to 4 and from 5 to 3. P09 also rated moving pieces from 5 to 1 and rotating them from 4 to 1. In G04, both participants rated solving together at 4 in both rounds, although P07 rated rotation at 1 and P08 at 4. The questionnaire therefore supplements the action evidence by showing that a sense of working together can coexist with very different experiences of control. The comparisons describe these sessions, whose fixed order, patterns and prototype versions also differed.',
]
rating_caption = (
    'Figure 5.8. Paired ratings for five questionnaire items in first-person VR (R03) and shared overhead VR (R04). '
    'Each row is one participant; circles and squares show the two raw ratings, connected within that participant. '
    'A square inside a circle indicates equal ratings. All 12 participants have both responses for these items '
    '(24 VR questionnaires from the confirmed 48-response dataset). Q04 concerns explaining an intended placement, '
    'Q06 knowing puzzle progress, Q09 moving a piece to an intended location, Q10 rotating it to an intended orientation, '
    'and Q12 feeling that the puzzle was solved together. Ratings use the full 1–5 scale; no combined score is calculated. '
    'The rounds occurred in a fixed order with different patterns and prototype versions. G02 ratings refer to the original '
    'session, not the later replay recording.'
)
coverage_rows = []
conditions = ['Physical direct', 'Physical overhead video', 'First-person VR', 'Shared overhead VR']
for i, condition in enumerate(conditions, 1):
    rid = f'R{i:02}'
    subset = [r for r in rows if r['round_id'] == rid]
    coverage_rows.append({
        'round': rid, 'condition': condition,
        'dyads_with_process_reports': 6,
        'confirmed_questionnaires': len(subset),
        'non_numeric_item_entries': sum(r[q] is None for r in subset for q in (f'Q{k:02}' for k in range(1, 13))),
        'process_note': 'G02 VR process material is a later replay.' if i >= 3 else '',
    })

# The historical source does not place the final four-round design in September.
nodes = [
    ('Original brief', 'External VR viewpoint; coordination, intent and workspace awareness.'),
    ('First-semester planning', 'Physical Tangram exploration informed the VR research and prototype.'),
    ('August plan and supervisor response', 'Keep the task family comparable; parts may be done separately or jointly.'),
    ('September decision', 'Use Tangram throughout.'),
    ('Implemented study', 'Four free-collaboration conditions; six familiar dyads; fixed order.\nActual patterns, practice and prototype versions retained.'),
]
fig = plt.figure(figsize=(160 / 25.4, 116 / 25.4))
ax = fig.add_axes([0, 0, 1, 1])
ax.set(xlim=(0, 1), ylim=(0, 1))
ax.axis('off')
for i, (heading, body) in enumerate(nodes):
    y = .817 - i * .195
    color = '#D9E7F0' if i == 0 else ('#D8EBE6' if i == 4 else '#F1F5F7')
    ax.add_patch(Rectangle((.025, y), .95, .15, facecolor=color, edgecolor='#ACBBC5', linewidth=.65))
    ax.text(.045, y + .113, heading, fontsize=9.1, fontweight='bold', va='center')
    ax.text(.045, y + .073, body, fontsize=8.0, va='top', linespacing=1.45)
    if i < 4:
        ax.annotate('', xy=(.5, y - .036), xytext=(.5, y - .004),
                    arrowprops={'arrowstyle': '-|>', 'color': '#345366', 'lw': .9, 'mutation_scale': 10})
history_outputs = save(fig, 'Figure3_1_research_development')
history_caption = (
    'Figure 3.1. Development of the research focus and study design. The August feedback called for a comparable task '
    'family while retaining the possibility of individual and joint work. The September discussion selected Tangram '
    'across the tasks. The final four-condition study is shown separately from those earlier plans. '
    'Sources: original project brief, early study plan, August thesis plan and supervisor response, '
    '1 September meeting transcript, and final study procedure.'
)

summary={'counts': {'responses':len(rows),'participants':len(participants),'NA':len(na)}, 'missing_values':na,'paired_values':paired,'descriptive_change_counts':counts,'history_nodes':nodes,'caption_questionnaire':rating_caption,'caption_history':history_caption,'outputs':rating_outputs+history_outputs}
(PROJECT/'generated/audit/auxiliary_build.json').write_text(portable_json(summary,ensure_ascii=False,indent=2))
print('Exported research-development and questionnaire figures')
