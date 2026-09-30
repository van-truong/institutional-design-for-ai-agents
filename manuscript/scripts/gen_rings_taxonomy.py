#!/usr/bin/env python3
"""Draft figure: nested systems around interacting agents, with the taxonomy as one ring (exploration).

After Bronfenbrenner (1979). Interacting agents (robot icons) sit at the center, inside their microsystem and
mesosystem. The 66 coded mechanisms form a ring between the mesosystem and the exosystem, where institutions meet
agents' interactions: one dot per mechanism (filled = tested with LLM agents, dotted = proposed only, open = none),
grouped by family-colored arcs, with the count in a gap at the top. Exosystem, macrosystem, and the chronosystem
(time) surround them. Data from docs/assets/taxonomy.json; colors follow figs/PALETTE.md.
Run from manuscript/:  python3 scripts/gen_rings_taxonomy.py
"""
import json, math, os
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', '..', 'docs', 'assets', 'taxonomy.json')
OUT = os.path.join(HERE, '..', 'figs', 'drafts', 'figure_rings-taxonomy.html')

INK, MUTED, HAIR, PAGE = '#3F4D5A', '#6B7787', '#B3BEC9', '#FBFAF7'
W, H = 960, 700
CX, CY = 330, 346
AGENT = ('#6C5CD0', '#463BA0', '#ECE9FB')
RINGS = [  # outer to inner: (name, outer radius, colors)
    ('MACROSYSTEM', 300, ('#C79A3A', '#8A5A0B', '#FBEEDA')),
    ('EXOSYSTEM', 250, ('#4F9070', '#2F6B4A', '#E5F0E1')),
    ('MECHANISMS', 202, ('#B3BEC9', '#3F4D5A', '#FFFFFF')),
    ('MESOSYSTEM', 164, ('#0F766E', '#04342C', '#E3F1EC')),
    ('MICROSYSTEM', 118, ('#3A6EA5', '#2F3D6B', '#DCE8F5')),
    ('', 70, AGENT),
]
R_DOT, R_ARC = 181, 195          # mechanism dots and family arcs, inside the MECHANISMS band
TOP_GAP = 13                     # empty slots at the top of the band, for the "66 mechanisms" label

def t(x, y, s, cls, anchor='middle', extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}"{extra}>{escape(s)}</text>'

def P(a, r):
    return CX + r * math.cos(math.radians(a)), CY + r * math.sin(math.radians(a))

def arc(r, a0, a1, color, width):
    x0, y0 = P(a0, r); x1, y1 = P(a1, r)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return (f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 {large} 1 {x1:.1f} {y1:.1f}" fill="none" '
            f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>')

def robot(x, y, s, col):
    mid, dark, bg = col
    return (f'<line x1="{x}" y1="{y - 13 * s}" x2="{x}" y2="{y - 18 * s}" stroke="{dark}" stroke-width="{1.4 * s}"/>'
            f'<circle cx="{x}" cy="{y - 19.5 * s}" r="{2 * s}" fill="{mid}"/>'
            f'<rect x="{x - 9 * s}" y="{y - 13 * s}" width="{18 * s}" height="{13 * s}" rx="{3.5 * s}" fill="#fff" stroke="{dark}" stroke-width="{1.5 * s}"/>'
            f'<circle cx="{x - 4 * s}" cy="{y - 6.5 * s}" r="{1.8 * s}" fill="{dark}"/><circle cx="{x + 4 * s}" cy="{y - 6.5 * s}" r="{1.8 * s}" fill="{dark}"/>'
            f'<rect x="{x - 7 * s}" y="{y + 1.5 * s}" width="{14 * s}" height="{10 * s}" rx="{2.5 * s}" fill="{mid}" stroke="{dark}" stroke-width="{1.3 * s}"/>')

def build():
    data = json.load(open(DATA))
    fams = data['families']
    s = []
    for name, r, (mid, dark, bg) in RINGS:
        s.append(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="{bg}" stroke="{mid}" stroke-width="1.6"/>')
    # ring labels, centered at the top of each band (the mechanism label sits in the gap)
    radii = [r for _, r, _ in RINGS]
    for i, (name, r, (mid, dark, bg)) in enumerate(RINGS[:-1]):
        inner = radii[i + 1]
        if name == 'MECHANISMS':
            continue
        s.append(t(CX, CY - (r + inner) / 2 + 5, name, 'ring', extra=f' fill="{dark}"'))
    # mechanism ring: one dot per mechanism, grouped by family arcs, with a labeled gap at the top
    mechs = [(f, m) for f in fams for th in f['themes'] for m in th['mechanisms']]
    gap = 1.6
    slots = len(mechs) + gap * (len(fams) - 1) + TOP_GAP
    step = 360 / slots
    a = -90 + (TOP_GAP / 2) * step
    for fi, f in enumerate(fams):
        fm = [m for ff, m in mechs if ff is f]
        a_start = a
        for m in fm:
            x, y = P(a, R_DOT)
            fill = f['dark'] if m['llm'] == 'tested' else '#fff'
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.3" fill="{fill}" stroke="{f["dark"]}" stroke-width="1.4"/>')
            if m['llm'] == 'proposed':
                s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.5" fill="{f["dark"]}"/>')
            a += step
        s.append(arc(R_ARC, a_start - step * 0.4, a - step * 0.6, f['mid'], 4.5))
        a += gap * step
    s.append(t(CX, CY - R_DOT + 5, f'{len(mechs)} MECHANISMS', 'mechlabel'))
    # interacting agents at the center
    pos = [(CX - 30, CY - 6), (CX + 30, CY - 6), (CX, CY + 34)]
    for i in range(3):
        for j in range(i + 1, 3):
            (x0, y0), (x1, y1) = pos[i], pos[j]
            s.append(f'<line x1="{x0}" y1="{y0 - 6}" x2="{x1}" y2="{y1 - 6}" stroke="{AGENT[0]}" stroke-width="1.8" stroke-dasharray="4 3"/>')
    for x, y in pos:
        s.append(robot(x, y, 1.45, AGENT))
    # chronosystem arc
    R = 318
    x0, y0 = P(160, R); x1, y1 = P(20, R)
    s.append(f'<path d="M{x0:.1f} {y0:.1f} A{R} {R} 0 0 0 {x1:.1f} {y1:.1f}" fill="none" stroke="{MUTED}" stroke-width="2.2" marker-end="url(#ah)"/>')
    s.append(t(CX, CY + R + 26, 'CHRONOSYSTEM (TIME)', 'chrono'))
    # legend
    lx, ly = 690, 44
    s.append(t(lx, ly, 'What each ring holds', 'lhead', 'start'))
    rows = [('Agents', AGENT, 'models acting together'),
            ('Microsystem', RINGS[4][2], 'user, tools, memory, task'),
            ('Mesosystem', RINGS[3][2], 'handoffs and orchestrators'),
            ('Mechanisms', None, '66 levers institutions use'),
            ('Exosystem', RINGS[1][2], 'platform policy, API limits'),
            ('Macrosystem', RINGS[0][2], 'law, markets, norms, values')]
    y = ly + 28
    for name, col, ex in rows:
        if col:
            s.append(f'<rect x="{lx}" y="{y - 12}" width="15" height="15" rx="4" fill="{col[2]}" stroke="{col[0]}" stroke-width="1.5"/>')
        else:
            for k, f in enumerate(fams):
                s.append(f'<rect x="{lx + (k % 3) * 6}" y="{y - 12 + (k // 3) * 8}" width="5" height="6" rx="1" fill="{f["mid"]}"/>')
        s.append(t(lx + 24, y, name, 'lname', 'start', f' fill="{(col or (0, INK))[1]}"'))
        s.append(t(lx + 24, y + 18, ex, 'lex', 'start'))
        y += 50
    # family colors
    y += 4
    s.append(t(lx, y, 'Mechanism families', 'lhead2', 'start'))
    for k, f in enumerate(fams):
        fx, fy = lx + (k % 2) * 120, y + 22 + (k // 2) * 22
        s.append(f'<rect x="{fx}" y="{fy - 10}" width="14" height="5" rx="2.5" fill="{f["mid"]}"/>')
        s.append(t(fx + 20, fy, f['label'], 'lfam', 'start', f' fill="{f["dark"]}"'))
    # evidence key
    y += 22 + 3 * 22 + 12
    s.append(t(lx, y, 'LLM-agent evidence', 'lhead2', 'start'))
    for k, (kind, label) in enumerate((('tested', 'tested'), ('proposed', 'proposed only'), ('none', 'none yet'))):
        kx, ky = lx + 8, y + 22 + k * 20
        s.append(f'<circle cx="{kx}" cy="{ky - 5}" r="4.3" fill="{INK if kind == "tested" else "#fff"}" stroke="{INK}" stroke-width="1.4"/>')
        if kind == 'proposed':
            s.append(f'<circle cx="{kx}" cy="{ky - 5}" r="1.5" fill="{INK}"/>')
        s.append(t(kx + 14, ky, label, 'lex', 'start'))
    return s

def main():
    body = '\n'.join(build())
    css = f'''
  text{{font-family:"Helvetica Neue",Arial,sans-serif;}}
  .ring{{font-size:14px;font-weight:900;letter-spacing:1.2px;}}
  .mechlabel{{font-size:13.5px;font-weight:900;letter-spacing:1.2px;fill:{INK};}}
  .chrono{{font-size:14px;font-weight:800;letter-spacing:.6px;fill:{MUTED};}}
  .lhead{{font-size:16px;font-weight:800;fill:{INK};}}
  .lhead2{{font-size:14.5px;font-weight:800;fill:{INK};}}
  .lname{{font-size:15.5px;font-weight:800;}}
  .lex{{font-size:14px;fill:{INK};}}
  .lfam{{font-size:14px;font-weight:700;}}'''
    html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>Draft: nested systems with the taxonomy as a ring</title>
<!-- Draft generated by scripts/gen_rings_taxonomy.py; not yet in the paper. -->
<style>{css}
  html,body{{margin:0;background:#fff;}} .fig{{width:{W}px;margin:0 auto;padding:12px;}}
</style></head><body><div class="fig">
<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker></defs>
{body}
</svg></div></body></html>'''
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(html)
    print('wrote', os.path.relpath(OUT))

if __name__ == '__main__':
    main()
