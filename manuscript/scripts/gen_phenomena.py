#!/usr/bin/env python3
"""Fig.: group-level phenomena observed in multi-agent systems, by substrate.

A companion to the mechanisms taxonomy (Fig. 5): mechanisms are what we design; phenomena are what happens without
them. Rows are phenomenon types, columns are the three substrates (humans, MARL agents, LLM agents); each cell is a
dot sized by how many coded instances report that phenomenon in that substrate, colored by whether the pattern helps
(green), harms (terracotta), or is neutral/surprising (blue) for cooperation. Harmful rows are tied to documented
real-world incidents on the right.
Data: taxonomy/coding/phenomena_tags.csv, taxonomy/instances.csv, taxonomy/incidents.csv. Colors: figs/PALETTE.md.
Run from manuscript/:  python3 scripts/gen_phenomena.py
"""
import csv, math, os, subprocess, sys
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
TAX = os.path.join(HERE, '..', '..', 'taxonomy')
OUT_HTML = os.path.join(HERE, '..', 'figs', 'figure_phenomena.html')
OUT_SVG = os.path.join(HERE, '..', 'figures', 'figure_phenomena.svg')
OUT_PDF = os.path.join(HERE, '..', 'figures', 'figure_phenomena.pdf')

FONT = "'Helvetica Neue', Arial, sans-serif"
INK, MUT, HAIR, PAGE = '#3F4D5A', '#6B7787', '#B3BEC9', '#FBFAF7'
# valence -> (mid, dark, tint)
VAL = {'beneficial': ('#4F9070', '#2F6B4A', '#E5F0E1'),
       'neutral':    ('#3A6EA5', '#2F3D6B', '#DCE8F5'),
       'harmful':    ('#C2662A', '#8F3F1E', '#FBEDE6')}
SUBS = [('human', 'Humans'), ('marl', 'MARL agents'), ('llm', 'LLM agents')]

# row order: neutral/beneficial "what agents build" band, then the harmful "failure" band
ROWS = [
    ('comm_language', 'Emergent communication & language', 'neutral'),
    ('convention_coord', 'Conventions & coordination', 'neutral'),
    ('social_structure', 'Social structure: networks, hierarchy, roles', 'neutral'),
    ('culture', 'Culture, norms & individuality', 'neutral'),
    ('collective_intel', 'Collective intelligence & performance', 'neutral'),
    ('economy', 'Emergent economy & resource use', 'neutral'),
    ('cooperation', 'Spontaneous cooperation', 'beneficial'),
    ('conformity_bias', 'Conformity & collective bias', 'harmful'),
    ('collusion_deception', 'Collusion, deception & manipulation', 'harmful'),
    ('harm', 'Emergent harm: toxicity, fragility, breakout', 'harmful'),
]
# documented real-world incidents tied to the failure rows (from taxonomy/incidents.csv)
WILD = [
    ('collusion_deception', 'Agents collude to bypass guardrails', '2026'),
    ('collusion_deception', 'Agents ran a hidden message board to cheat an eval', '2026'),
    ('harm', "OpenAI agents' undisclosed web breakout", '2026'),
    ('harm', 'First AI-orchestrated espionage campaign', '2025'),
]


def load():
    tags = {r['instance_id']: r for r in csv.DictReader(open(os.path.join(TAX, 'coding', 'phenomena_tags.csv')))}
    inst = {r['instance_id']: r for r in csv.DictReader(open(os.path.join(TAX, 'instances.csv')))}
    grid = {}
    for iid, t in tags.items():
        sub = inst[iid]['agent_type']
        grid[(t['phenomenon_type'], sub)] = grid.get((t['phenomenon_type'], sub), 0) + 1
    return grid


# layout
LX, W = 470, 1310                 # left label width, total width
COLX = [LX + 70, LX + 190, LX + 310]   # substrate column centers
WILDX = LX + 410
ROWH, TOP, GAP = 52, 150, 34      # GAP: vertical break between the two bands


def dot(cx, cy, n, val):
    mid, dark, tint = VAL[val]
    r = 6 + 3.4 * math.sqrt(n) if n else 0
    o = []
    if n:
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="{tint}" stroke="{mid}" stroke-width="1.6"/>')
        o.append(f'<text x="{cx}" y="{cy + 4.5:.0f}" text-anchor="middle" font-size="14" font-weight="700" fill="{dark}">{n}</text>')
    else:
        o.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="#fff" stroke="{HAIR}" stroke-width="1.2"/>')
    return ''.join(o)


def row_y(i, band_split):
    """Row center; rows in the harmful band are pushed down by GAP."""
    return TOP + ROWH * i + ROWH / 2 + (GAP if i >= band_split else 0)


def build():
    grid = load()
    band_split = next(i for i, r in enumerate(ROWS) if r[2] == 'harmful')
    H = TOP + ROWH * len(ROWS) + GAP + 96
    o = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" xmlns="http://www.w3.org/2000/svg" font-family="{FONT}">',
         '<title>Group-level phenomena in multi-agent systems</title>',
         f'<rect width="{W}" height="{H}" fill="#fff"/>']
    # column headers
    for (key, lab), cx in zip(SUBS, COLX):
        o.append(f'<text x="{cx}" y="{TOP - 74}" text-anchor="middle" font-size="16" font-weight="800" fill="{INK}">{lab}</text>')
    o.append(f'<text x="{WILDX}" y="{TOP - 74}" font-size="16" font-weight="800" fill="{INK}">Documented in the wild</text>')
    o.append(f'<line x1="{LX}" y1="{TOP - 58}" x2="{W - 30}" y2="{TOP - 58}" stroke="{HAIR}" stroke-width="1.3"/>')
    # band labels
    o.append(f'<text x="34" y="{TOP - 20}" font-size="13.5" font-weight="800" fill="{MUT}" letter-spacing="0.5">WHAT AGENT GROUPS BUILD</text>')
    ysplit = TOP + ROWH * band_split + GAP / 2 + 4       # centered in the band gap
    o.append(f'<line x1="30" y1="{ysplit - 12:.0f}" x2="{W - 30}" y2="{ysplit - 12:.0f}" stroke="{VAL["harmful"][0]}" stroke-width="1" stroke-dasharray="3 4" opacity="0.7"/>')
    o.append(f'<text x="34" y="{ysplit + 4:.0f}" font-size="13.5" font-weight="800" fill="{VAL["harmful"][1]}" letter-spacing="0.5">WHERE IT GOES WRONG</text>')
    # rows
    wild_y = {}
    for i, (key, lab, val) in enumerate(ROWS):
        cy = row_y(i, band_split)
        mid, dark, tint = VAL[val]
        o.append(f'<text x="34" y="{cy + 5:.0f}" font-size="15.5" fill="{INK}">{escape(lab)}</text>')
        o.append(f'<rect x="26" y="{cy - 11:.0f}" width="4" height="22" rx="2" fill="{mid}"/>')
        for (skey, _), cx in zip(SUBS, COLX):
            o.append(dot(cx, cy, grid.get((key, skey), 0), val))
        wild_y[key] = cy
    # "in the wild" incident callouts, tied to their row (stacked around the row center)
    from collections import defaultdict
    groups = defaultdict(list)
    for key, head, yr in WILD:
        groups[key].append((head, yr))
    for key, items in groups.items():
        base = wild_y[key]
        n = len(items)
        for j, (head, yr) in enumerate(items):
            wy = base + (j - (n - 1) / 2) * 20
            o.append(f'<circle cx="{WILDX + 4}" cy="{wy:.0f}" r="3.2" fill="{VAL["harmful"][0]}"/>')
            o.append(f'<text x="{WILDX + 16}" y="{wy + 4:.0f}" font-size="13" fill="{INK}">{escape(head)} <tspan fill="{MUT}">({yr})</tspan></text>')
    # legend
    ly = H - 46
    o.append(f'<text x="34" y="{ly}" font-size="13.5" font-weight="700" fill="{INK}">Effect on cooperation:</text>')
    lx = 210
    for val, name in [('beneficial', 'beneficial'), ('neutral', 'neutral / surprising'), ('harmful', 'harmful')]:
        mid, dark, tint = VAL[val]
        o.append(f'<circle cx="{lx}" cy="{ly - 4:.0f}" r="7" fill="{tint}" stroke="{mid}" stroke-width="1.6"/>')
        o.append(f'<text x="{lx + 13}" y="{ly:.0f}" font-size="13.5" fill="{INK}">{name}</text>')
        lx += 40 + 8 * len(name)
    o.append(f'<text x="34" y="{ly + 22}" font-size="12.5" font-style="italic" fill="{MUT}">Dot area ∝ number of coded instances. A first-pass reading of a fast-moving literature; see the interactive taxonomy.</text>')
    o.append('</svg>')
    return '\n'.join(o)


def main():
    svg = build()
    html = (f'<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8"><title>Phenomena</title>\n'
            f'<!-- Generated by scripts/gen_phenomena.py. -->\n'
            f'<style>html,body{{margin:0;background:#fff;}} .fig{{width:{W}px;margin:0 auto;padding:12px;}}</style></head>'
            f'<body><div class="fig">\n{svg}\n</div></body></html>')
    open(OUT_HTML, 'w', encoding='utf-8').write(html)
    open(OUT_SVG, 'w', encoding='utf-8').write(svg)
    subprocess.run(['rsvg-convert', '--format', 'pdf1.5', '-o', OUT_PDF, OUT_SVG], check=True)
    print('wrote', os.path.relpath(OUT_HTML), 'and', os.path.relpath(OUT_PDF))


if __name__ == '__main__':
    main()
