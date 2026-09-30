#!/usr/bin/env python3
"""Draft figure: nested systems around interacting agents, with the taxonomy as a thick ring (exploration).

After Bronfenbrenner's (1979) ecological framework, with the examples, arrows, and labels drawn inside each ring:
interacting agents (robot icons) at the center; the microsystem (settings each agent acts in directly); the
mesosystem (links between those settings, drawn as two-way arrows); a thick ring holding the 66 coded mechanisms as
a curved tree (family node -> theme node -> one dot per mechanism: filled = tested with LLM agents, dotted = proposed
only, open = none); the exosystem and macrosystem; and the chronosystem (time) around them.
Data from docs/assets/taxonomy.json; colors follow figs/PALETTE.md.
Run from manuscript/:  python3 scripts/gen_rings_taxonomy.py
"""
import json, math, os
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', '..', 'docs', 'assets', 'taxonomy.json')
OUT = os.path.join(HERE, '..', 'figs', 'drafts', 'figure_rings-taxonomy.html')

INK, MUTED, HAIR, PAGE = '#3F4D5A', '#6B7787', '#B3BEC9', '#FBFAF7'
W, H = 1080, 1110
CX, CY = 540, 548
AGENT = ('#6C5CD0', '#463BA0', '#ECE9FB')
MICRO = ('#3A6EA5', '#2F3D6B', '#DCE8F5')
MESO = ('#0F766E', '#04342C', '#E3F1EC')
MECH = ('#B3BEC9', '#3F4D5A', '#FFFFFF')
EXO = ('#4F9070', '#2F6B4A', '#E5F0E1')
MACRO = ('#C79A3A', '#8A5A0B', '#FBEEDA')
# (outer radius, colors, label); the agents' circle is the innermost
R_AGENT, R_MICRO, R_MESO, R_MECH, R_EXO, R_MACRO = 80, 152, 204, 352, 420, 486
BANDS = [(R_MACRO, MACRO, 'MACROSYSTEM'), (R_EXO, EXO, 'EXOSYSTEM'), (R_MECH, MECH, None),
         (R_MESO, MESO, 'MESOSYSTEM'), (R_MICRO, MICRO, 'MICROSYSTEM'), (R_AGENT, AGENT, None)]
# example settings inside each ring: (label, angle in degrees, 0 = right, 90 = down)
MICRO_ITEMS = [('user', 180), ('tools', 0), ('memory', 128), ('task', 52)]
MESO_ITEMS = [('handoffs', 206), ('orchestrator', 334), ('shared memory', 90)]
EXO_ITEMS = [('platform policy', 238), ('API limits', 302), ("other firms' agents", 127), ('monitoring stack', 53), ('compute providers', 90)]
MACRO_ITEMS = [('law & regulation', 252), ('markets', 288), ('professional norms', 122), ('cultural values', 58)]
R_FAM, R_THEME, R_LEAF, R_ARC = R_MESO + 16, R_MESO + 70, R_MECH - 30, R_MECH - 14
TOP_GAP = 11                      # empty slots at the top of the mechanism ring, for its label

def t(x, y, s, cls, anchor='middle', extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}"{extra}>{escape(s)}</text>'

def P(a, r):
    return CX + r * math.cos(math.radians(a)), CY + r * math.sin(math.radians(a))

def arc_path(r, a0, a1):
    x0, y0 = P(a0, r); x1, y1 = P(a1, r)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f'M{x0:.1f} {y0:.1f} A{r} {r} 0 {large} 1 {x1:.1f} {y1:.1f}'

def pill(a, r, label, col):
    mid, dark, bg = col
    x, y = P(a, r)
    w = 18 + 7.4 * len(label)
    return (f'<rect x="{x - w / 2:.1f}" y="{y - 12:.1f}" width="{w:.1f}" height="24" rx="12" fill="#fff" stroke="{mid}" stroke-width="1.3"/>'
            + t(x, y + 4.8, label, 'pill', extra=f' fill="{dark}"'))

def robot(x, y, s, col):
    mid, dark, bg = col
    return (f'<line x1="{x}" y1="{y - 13 * s}" x2="{x}" y2="{y - 18 * s}" stroke="{dark}" stroke-width="{1.4 * s}"/>'
            f'<circle cx="{x}" cy="{y - 19.5 * s}" r="{2 * s}" fill="{mid}"/>'
            f'<rect x="{x - 9 * s}" y="{y - 13 * s}" width="{18 * s}" height="{13 * s}" rx="{3.5 * s}" fill="#fff" stroke="{dark}" stroke-width="{1.5 * s}"/>'
            f'<circle cx="{x - 4 * s}" cy="{y - 6.5 * s}" r="{1.8 * s}" fill="{dark}"/><circle cx="{x + 4 * s}" cy="{y - 6.5 * s}" r="{1.8 * s}" fill="{dark}"/>'
            f'<rect x="{x - 7 * s}" y="{y + 1.5 * s}" width="{14 * s}" height="{10 * s}" rx="{2.5 * s}" fill="{mid}" stroke="{dark}" stroke-width="{1.3 * s}"/>')

def mechanisms(fams):
    s = []
    mechs = [m for f in fams for th in f['themes'] for m in th['mechanisms']]
    gap = 1.8
    step = 360 / (len(mechs) + gap * (len(fams) - 1) + TOP_GAP)
    a = -90 + (TOP_GAP / 2) * step
    ang = {}
    for f in fams:
        for th in f['themes']:
            for m in th['mechanisms']:
                ang[m['id']] = a; a += step
        a += gap * step
    links, nodes, labels = [], [], []
    for f in fams:
        mid, dark = f['mid'], f['dark']
        tas = []
        for th in f['themes']:
            tas.append(sum(ang[m['id']] for m in th['mechanisms']) / len(th['mechanisms']))
        fa = sum(tas) / len(tas)
        fx, fy = P(fa, R_FAM)
        first = ang[f['themes'][0]['mechanisms'][0]['id']]
        last = ang[f['themes'][-1]['mechanisms'][-1]['id']]
        s.append(f'<path d="{arc_path(R_ARC, first - step * 0.4, last + step * 0.4)}" fill="none" stroke="{mid}" stroke-width="5" stroke-linecap="round"/>')
        for th, ta in zip(f['themes'], tas):
            tx, ty = P(ta, R_THEME)
            c1, c2 = P(fa, (R_FAM + R_THEME) / 2), P(ta, (R_FAM + R_THEME) / 2)
            links.append(f'<path d="M{fx:.1f} {fy:.1f} C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {tx:.1f} {ty:.1f}" stroke="{mid}" class="lk"/>')
            nodes.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="3" fill="#fff" stroke="{mid}" stroke-width="1.5"/>')
            for m in th['mechanisms']:
                ma = ang[m['id']]
                lx, ly = P(ma, R_LEAF)
                d1, d2 = P(ta, (R_THEME + R_LEAF) / 2), P(ma, (R_THEME + R_LEAF) / 2)
                links.append(f'<path d="M{tx:.1f} {ty:.1f} C{d1[0]:.1f} {d1[1]:.1f} {d2[0]:.1f} {d2[1]:.1f} {lx:.1f} {ly:.1f}" stroke="{mid}" class="lk"/>')
                fill = dark if m['llm'] == 'tested' else '#fff'
                nodes.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="4.3" fill="{fill}" stroke="{dark}" stroke-width="1.4"/>')
                if m['llm'] == 'proposed':
                    nodes.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="1.5" fill="{dark}"/>')
        nodes.append(f'<circle cx="{fx:.1f}" cy="{fy:.1f}" r="5.5" fill="{mid}"/>')
        # family label just outward of its node, kept horizontal with a white halo
        lxx, lyy = P(fa, R_FAM + 30)
        labels.append(t(lxx, lyy + 5, f['label'].upper(), 'fam', extra=f' fill="{dark}"'))
    s += links + nodes + labels
    lx, ly = P(-90, (R_MESO + R_MECH) / 2)
    s.append(t(lx, ly - 4, f'{len(mechs)} MECHANISMS', 'mechlabel'))
    s.append(t(lx, ly + 15, 'that institutions use', 'mechsub'))
    return s

def build():
    fams = json.load(open(DATA))['families']
    s = []
    for r, (mid, dark, bg), _ in BANDS:
        s.append(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="{bg}" stroke="{mid}" stroke-width="1.7"/>')
    radii = [b[0] for b in BANDS]
    for i, (r, (mid, dark, bg), name) in enumerate(BANDS[:-1]):
        if name:
            s.append(t(CX, CY - (r + radii[i + 1]) / 2 + 5, name, 'ring', extra=f' fill="{dark}"'))
    # mesosystem: two-way arrows linking the microsystem settings
    for a0, a1 in ((136, 172), (8, 44), (188, 232), (-52, -8)):
        s.append(f'<path d="{arc_path(R_MICRO + 12, a0, a1)}" fill="none" stroke="{MESO[0]}" stroke-width="2" marker-start="url(#ahm)" marker-end="url(#ahm)"/>')
    for items, r, col in ((MICRO_ITEMS, (R_AGENT + R_MICRO) / 2, MICRO), (MESO_ITEMS, R_MESO - 22, MESO),
                          (EXO_ITEMS, (R_MECH + R_EXO) / 2, EXO), (MACRO_ITEMS, (R_EXO + R_MACRO) / 2, MACRO)):
        for label, a in items:
            s.append(pill(a, r, label, col))
    s += mechanisms(fams)
    # interacting agents at the center
    pos = [(CX - 30, CY - 4), (CX + 30, CY - 4), (CX, CY + 36)]
    for i in range(3):
        for j in range(i + 1, 3):
            (x0, y0), (x1, y1) = pos[i], pos[j]
            s.append(f'<line x1="{x0}" y1="{y0 - 6}" x2="{x1}" y2="{y1 - 6}" stroke="{AGENT[0]}" stroke-width="1.8" stroke-dasharray="4 3"/>')
    for x, y in pos:
        s.append(robot(x, y, 1.45, AGENT))
    s.append(t(CX, CY - 44, 'AGENTS', 'ring', extra=f' fill="{AGENT[1]}"'))
    # chronosystem: a time arrow around the bottom
    R = R_MACRO + 20
    (x0, y0), (x1, y1) = P(150, R), P(30, R)
    s.append(f'<path d="M{x0:.1f} {y0:.1f} A{R} {R} 0 0 0 {x1:.1f} {y1:.1f}" fill="none" stroke="{MUTED}" stroke-width="2.4" marker-end="url(#ah)"/>')
    s.append(t(CX, CY + R + 26, 'CHRONOSYSTEM: model updates, drift, deprecations, incidents over time', 'chrono'))
    # corner notes: evidence key and attribution
    kx, ky = W - 190, 40
    s.append(t(kx, ky, 'LLM-agent evidence', 'khead', 'start'))
    for k, (kind, label) in enumerate((('tested', 'tested'), ('proposed', 'proposed only'), ('none', 'none yet'))):
        x, y = kx + 8, ky + 24 + k * 21
        s.append(f'<circle cx="{x}" cy="{y - 5}" r="4.3" fill="{INK if kind == "tested" else "#fff"}" stroke="{INK}" stroke-width="1.4"/>')
        if kind == 'proposed':
            s.append(f'<circle cx="{x}" cy="{y - 5}" r="1.5" fill="{INK}"/>')
        s.append(t(x + 14, y, label, 'kitem', 'start'))
    s.append(t(20, 40, 'After Bronfenbrenner (1979)', 'note', 'start'))
    return s

def main():
    body = '\n'.join(build())
    css = f'''
  text{{font-family:"Helvetica Neue",Arial,sans-serif;}}
  .ring{{font-size:15px;font-weight:900;letter-spacing:1.4px;}}
  .pill{{font-size:13.5px;font-weight:700;}}
  .lk{{fill:none;stroke-width:1.2;opacity:.65;}}
  .fam{{font-size:13px;font-weight:900;letter-spacing:.6px;paint-order:stroke;stroke:#fff;stroke-width:4px;}}
  .mechlabel{{font-size:15px;font-weight:900;letter-spacing:1.4px;fill:{INK};}}
  .mechsub{{font-size:13px;font-style:italic;fill:{MUTED};}}
  .chrono{{font-size:14px;font-weight:800;letter-spacing:.5px;fill:{MUTED};}}
  .khead{{font-size:14.5px;font-weight:800;fill:{INK};}}
  .kitem{{font-size:14px;fill:{INK};}}
  .note{{font-size:14px;font-style:italic;fill:{MUTED};}}'''
    marker = lambda k, c: f'<marker id="{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
    html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>Draft: nested systems with the taxonomy as a ring</title>
<!-- Draft generated by scripts/gen_rings_taxonomy.py; not yet in the paper. -->
<style>{css}
  html,body{{margin:0;background:#fff;}} .fig{{width:{W}px;margin:0 auto;padding:12px;}}
</style></head><body><div class="fig">
<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg">
<defs>{marker('ah', MUTED)}{marker('ahm', MESO[0])}</defs>
{body}
</svg></div></body></html>'''
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(html)
    print('wrote', os.path.relpath(OUT))

if __name__ == '__main__':
    main()
