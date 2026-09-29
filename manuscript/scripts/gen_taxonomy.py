#!/usr/bin/env python3
"""Generate the taxonomy figure (Fig. 4) from the coded dataset, as a single-SVG HTML.

Reads ../taxonomy/codebook.csv (66 mechanisms in 18 themes). Themes are grouped and colored by the six
mechanism families of Section 3. Each mechanism row shows:
  - a circle for LLM-agent evidence: filled = tested in >=1 study, ring with dot = proposed only, open = none
  - squares for breadth of use: one per discipline outside AI/ML where the mechanism appears (max 6)
The previous seed-based dendrogram is archived in figs/archive/.
Run from manuscript/:  python3 scripts/gen_taxonomy.py
"""
import csv, html, os

HERE = os.path.dirname(os.path.abspath(__file__))
CODEBOOK = os.path.join(HERE, '..', '..', 'taxonomy', 'codebook.csv')
OUT = os.path.join(HERE, '..', 'figs', 'figure5_cooperation-taxonomy.html')

# family: (label, dark, mid, themes)
FAMILIES = {
    'normative':   ('Normative',   '#8A5A0B', '#C79A3A', ['T15', 'T10', 'T12']),
    'social':      ('Social',      '#8F3F1E', '#C2662A', ['T03', 'T09', 'T16', 'T17']),
    'epistemic':   ('Epistemic',   '#2F3D6B', '#3A6EA5', ['T01', 'T02', 'T11']),
    'incentive':   ('Incentive',   '#2F6B4A', '#4F9070', ['T04', 'T05', 'T06', 'T18']),
    'constraint':  ('Constraint',  '#463BA0', '#6C5CD0', ['T08', 'T07']),
    'restorative': ('Restorative', '#04342C', '#0F766E', ['T13', 'T14']),
}
COLUMNS = [['normative', 'social', 'epistemic'], ['incentive', 'constraint', 'restorative']]

# display names for long mechanism labels (full names stay in the dataset)
SHORT = {
    'Ex ante action restriction & scoped permissions': 'Action restriction & scoped permissions',
    'Externality pricing & central incentive adjustment': 'Externality pricing & planner incentives',
    'Communication & internal-state oversight': 'Message & internal-state oversight',
    'Instilled prosocial dispositions & reasoning': 'Instilled prosocial dispositions',
    'Failure attribution & incident analysis': 'Failure attribution',
    'Centralized (pool) sanctioning & fines': 'Centralized (pool) sanctions & fines',
    'Access & terms conditioned on record': 'Access conditioned on record',
    'Outcome & resource-state feedback': 'Outcome & resource feedback',
    'Social learning & strategy selection': 'Social learning & selection',
    'Mutual aid, pooling & mutual credit': 'Mutual aid & pooling',
}
THEME_SHORT = {'Visibility, information & attribution': 'Visibility & attribution'}

INK, MUTED, HAIR = '#2C2C2A', '#6B7787', '#B3BEC9'
TEXTWIDTH_PT = 347.0          # LNCS \textwidth (122 mm)
ROW, THEME_ROW, FAM_ROW = 17.0, 19.0, 24.0
GAP_THEME, GAP_FAM = 5.0, 14.0
COL_W, COL_GAP, PAD = 336.0, 22.0, 14.0
TOP = 58.0
SQ, SQ_GAP, MAX_SQ = 6.0, 2.2, 6
FS = {'leaf': 13.0, 'theme': 13.0, 'fam': 15.5, 'title': 17.0, 'legend': 12.6}

def esc(s): return html.escape(s, quote=False)

def load():
    rows = list(csv.DictReader(open(CODEBOOK)))
    themes = {}
    for r in rows:
        themes.setdefault(r['theme_id'], (r['theme'], []))[1].append(r)
    return rows, themes

def breadth(r):
    # disciplines_all includes the seed spreadsheet's human examples (coarse discipline labels)
    ds = [x.split(':')[0] for x in (r.get('disciplines_all') or r['disciplines']).split(';') if x]
    return min(MAX_SQ, len([d for d in ds if d not in ('ai_ml',)]))

def column_height(col, themes):
    h = 0
    for f in col:
        h += FAM_ROW + GAP_FAM
        for t in FAMILIES[f][3]:
            h += THEME_ROW + len(themes[t][1]) * ROW + GAP_THEME
    return h

def build():
    rows, themes = load()
    used = {t for f in FAMILIES.values() for t in f[3]}
    assert used == set(themes), f'themes not placed: {set(themes) - used}'
    W = PAD * 2 + COL_W * 2 + COL_GAP
    body = max(column_height(c, themes) for c in COLUMNS)
    LEG = 46.0
    H = TOP + body + LEG
    scale = TEXTWIDTH_PT / W
    assert min(FS.values()) * scale >= 6.0, f'min font {min(FS.values()) * scale:.2f}pt < 6pt'

    o = ['<?xml version="1.0" encoding="UTF-8"?>',
         f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" font-family="\'Helvetica Neue\', Arial, sans-serif">',
         '<title>Taxonomy of cooperation-shaping mechanisms</title>',
         f'<desc>{len(rows)} mechanisms in {len(themes)} themes, grouped by six mechanism families, with markers for '
         'LLM-agent evidence and breadth of use across disciplines.</desc>',
         f'<style>.leaf{{font-size:{FS["leaf"]}px;fill:{INK}}}.theme{{font-size:{FS["theme"]}px;font-weight:700}}'
         f'.fam{{font-size:{FS["fam"]}px;font-weight:700;letter-spacing:0.4px}}'
         f'.title{{font-size:{FS["title"]}px;font-weight:700;fill:{INK};text-anchor:middle}}'
         f'.leg{{font-size:{FS["legend"]}px;fill:{MUTED}}}</style>',
         f'<text class="title" x="{W / 2:.1f}" y="30">Cooperation-shaping mechanisms for agent groups</text>']

    def llm_marker(x, y, r, dark):
        t, p = int(r['llm_tested_studies'] or 0), int(r['llm_proposed_studies'] or 0)
        if t:
            return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="{dark}"/>'
        s = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="#FFFFFF" stroke="{dark}" stroke-width="1.2"/>'
        if p: s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.3" fill="{dark}"/>'
        return s

    def squares(xr, y, n, mid):
        s = []
        for i in range(MAX_SQ):
            x = xr - (MAX_SQ - i) * (SQ + SQ_GAP)
            fill = mid if i < n else '#FFFFFF'
            stroke = mid if i < n else HAIR
            s.append(f'<rect x="{x:.1f}" y="{y - SQ / 2:.1f}" width="{SQ}" height="{SQ}" rx="1" fill="{fill}" stroke="{stroke}" stroke-width="0.8"/>')
        return ''.join(s)

    for ci, col in enumerate(COLUMNS):
        x0 = PAD + ci * (COL_W + COL_GAP); xr = x0 + COL_W
        y = TOP
        for f in col:
            label, dark, mid, tids = FAMILIES[f]
            o.append(f'<text class="fam" x="{x0:.1f}" y="{y + 9:.1f}" fill="{dark}">{esc(label.upper())}</text>')
            o.append(f'<line x1="{x0:.1f}" y1="{y + 15:.1f}" x2="{xr:.1f}" y2="{y + 15:.1f}" stroke="{mid}" stroke-width="1.6"/>')
            y += FAM_ROW
            for t in tids:
                tname, mechs = themes[t]
                ty = y + 9
                o.append(f'<text class="theme" x="{x0 + 6:.1f}" y="{ty:.1f}" fill="{dark}">{esc(THEME_SHORT.get(tname, tname))}</text>')
                y += THEME_ROW
                spine_top = y - 3
                for r in mechs:
                    ly = y + ROW / 2 - 2
                    o.append(f'<line x1="{x0 + 10:.1f}" y1="{ly:.1f}" x2="{x0 + 18:.1f}" y2="{ly:.1f}" stroke="{mid}" stroke-width="1.1" opacity="0.7"/>')
                    o.append(llm_marker(x0 + 24, ly, r, dark))
                    o.append(f'<text class="leaf" x="{x0 + 33:.1f}" y="{ly:.1f}" dominant-baseline="central">{esc(SHORT.get(r["mechanism"], r["mechanism"]))}</text>')
                    o.append(squares(xr, ly, breadth(r), mid))
                    y += ROW
                o.append(f'<line x1="{x0 + 10:.1f}" y1="{spine_top:.1f}" x2="{x0 + 10:.1f}" y2="{y - ROW / 2 - 2:.1f}" stroke="{mid}" stroke-width="1.6"/>')
                y += GAP_THEME
            y += GAP_FAM

    # legend
    ly = TOP + body + 18
    lx = PAD
    o.append(f'<line x1="{PAD:.1f}" y1="{ly - 12:.1f}" x2="{W - PAD:.1f}" y2="{ly - 12:.1f}" stroke="{HAIR}" stroke-width="0.8"/>')
    o.append(f'<text class="leg" x="{lx:.1f}" y="{ly + 4:.1f}">LLM-agent evidence:</text>')
    lx += 140
    for kind, txt in (('t', 'tested'), ('p', 'proposed only'), ('n', 'none')):
        dummy = {'llm_tested_studies': '1' if kind == 't' else '0', 'llm_proposed_studies': '1' if kind == 'p' else '0'}
        o.append(llm_marker(lx, ly, dummy, INK))
        o.append(f'<text class="leg" x="{lx + 8:.1f}" y="{ly + 4:.1f}">{txt}</text>')
        lx += 8 + len(txt) * 6.6 + 16
    lx += 6
    o.append(f'<text class="leg" x="{lx:.1f}" y="{ly + 4:.1f}">Disciplines outside AI:</text>')
    lx += 140
    for i in range(3):
        o.append(f'<rect x="{lx + i * (SQ + SQ_GAP):.1f}" y="{ly - SQ / 2:.1f}" width="{SQ}" height="{SQ}" rx="1" fill="{MUTED}" stroke="{MUTED}" stroke-width="0.8"/>')
    o.append(f'<text class="leg" x="{lx + 3 * (SQ + SQ_GAP) + 4:.1f}" y="{ly + 4:.1f}">= 3 (max 6)</text>')
    o.append('</svg>')
    return '\n'.join(o), len(rows), len(themes), min(FS.values()) * scale, W, H

if __name__ == '__main__':
    svg, n, nt, minpt, W, H = build()
    open(OUT, 'w').write(svg)
    print(f'wrote {os.path.relpath(OUT)}: {n} mechanisms, {nt} themes, viewBox {W:.0f}x{H:.0f}, min font {minpt:.2f}pt')
