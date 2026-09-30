#!/usr/bin/env python3
"""Draft figure: an ecological-systems view of an AI agent in human-AI infrastructure (sketch, not yet in the paper).

After Bronfenbrenner's (1979) nested systems: the model sits inside its microsystem (what it acts in directly),
mesosystem (links between those settings), exosystem (settings it is not part of that still shape it), and
macrosystem (law, markets, norms), with the chronosystem (change over time) around them. Brackets show how the rings
group into the three levels of Fig. 2A. Colors follow figs/PALETTE.md.
Run from manuscript/:  python3 scripts/gen_nested_rings.py
"""
import math, os
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'figs', 'drafts', 'figure_nested-rings.html')

INK, MUTED, HAIR = '#3F4D5A', '#6B7787', '#B3BEC9'
W, H = 960, 660
CX, CY = 300, 316
# (name, radius, (mid, dark, bg), examples)
RINGS = [
    ('Macrosystem', 272, ('#C79A3A', '#8A5A0B', '#FBEEDA'), ['law and regulation, market structure,', 'professional norms, cultural values']),
    ('Exosystem', 218, ('#4F9070', '#2F6B4A', '#E5F0E1'), ["platform policy, API limits, other firms'", 'agents, the monitoring stack']),
    ('Mesosystem', 164, ('#0F766E', '#04342C', '#E3F1EC'), ['handoffs, orchestrators, memory', 'shared across tasks']),
    ('Microsystem', 110, ('#3A6EA5', '#2F3D6B', '#DCE8F5'), ['its user, tools, memory, task,', 'and the agents it talks to']),
    ('Model', 54, ('#6C5CD0', '#463BA0', '#ECE9FB'), ['weights, training,', 'system prompt']),
]

def t(x, y, s, cls, anchor='middle', extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}"{extra}>{escape(s)}</text>'

def build():
    s = []
    for name, r, (mid, dark, bg), _ in RINGS:
        s.append(f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="{bg}" stroke="{mid}" stroke-width="1.6"/>')
    # ring labels at the top of each band
    radii = [r for _, r, _, _ in RINGS] + [0]
    for i, (name, r, (mid, dark, bg), _) in enumerate(RINGS):
        inner = radii[i + 1]
        y = CY - (r + inner) / 2 + 5 if name != 'Model' else CY + 5
        s.append(t(CX, y, name.upper() if name != 'Model' else 'MODEL', 'ring', extra=f' fill="{dark}"'))
    # chronosystem: an arc around the bottom, with an arrowhead
    R = 292
    a0, a1 = math.radians(160), math.radians(20)
    x0, y0 = CX + R * math.cos(a0), CY + R * math.sin(a0)
    x1, y1 = CX + R * math.cos(a1), CY + R * math.sin(a1)
    s.append(f'<path d="M{x0:.1f} {y0:.1f} A{R} {R} 0 0 0 {x1:.1f} {y1:.1f}" fill="none" stroke="{MUTED}" stroke-width="2.2" marker-end="url(#ah)"/>')
    s.append(t(CX, CY + R + 26, 'CHRONOSYSTEM (TIME)', 'chrono'))
    # legend with examples
    lx, ly = 632, 58
    s.append(t(lx, ly - 22, 'What each ring holds for an AI agent', 'lhead', 'start'))
    rows = list(reversed(RINGS))
    for i, (name, r, (mid, dark, bg), ex) in enumerate(rows):
        y = ly + i * 86
        s.append(f'<rect x="{lx}" y="{y}" width="16" height="16" rx="4" fill="{bg}" stroke="{mid}" stroke-width="1.5"/>')
        s.append(t(lx + 26, y + 13, name, 'lname', 'start', f' fill="{dark}"'))
        for j, line in enumerate(ex):
            s.append(t(lx + 26, y + 34 + j * 18, line, 'lex', 'start'))
    # brackets: how the rings map onto Fig. 2A's three levels
    groups = [(0, 0, 'individual model'), (1, 2, 'agent-group interactions'), (3, 4, 'governing institutions')]
    bx = lx - 16
    for a, b, label in groups:
        ya, yb = ly + a * 86 + 2, ly + b * 86 + 48
        s.append(f'<path d="M{bx + 6} {ya} L{bx} {ya} L{bx} {yb} L{bx + 6} {yb}" fill="none" stroke="{HAIR}" stroke-width="1.6"/>')
        ym = (ya + yb) / 2
        s.append(t(bx - 8, ym, label, 'bracket', extra=f' transform="rotate(-90 {bx - 8} {ym})"'))
    y = ly + 5 * 86
    s.append(f'<path d="M{lx} {y + 8} L{lx + 16} {y + 8}" stroke="{MUTED}" stroke-width="2.2" marker-end="url(#ah)"/>')
    s.append(t(lx + 26, y + 13, 'Chronosystem', 'lname', 'start', f' fill="{INK}"'))
    s.append(t(lx + 26, y + 34, 'model updates, drift, deprecations,', 'lex', 'start'))
    s.append(t(lx + 26, y + 52, 'incidents that change the rules', 'lex', 'start'))
    s.append(t(lx, y + 86, 'After Bronfenbrenner (1979). Brackets show the', 'note', 'start'))
    s.append(t(lx, y + 104, 'three levels of Fig. 2A.', 'note', 'start'))
    return s

def main():
    body = '\n'.join(build())
    css = f'''
  text{{font-family:"Helvetica Neue",Arial,sans-serif;}}
  .ring{{font-size:14px;font-weight:900;letter-spacing:1.2px;}}
  .chrono{{font-size:14px;font-weight:800;letter-spacing:.6px;fill:{MUTED};}}
  .lhead{{font-size:16px;font-weight:800;fill:{INK};}}
  .lname{{font-size:16px;font-weight:800;}}
  .lex{{font-size:14.5px;fill:{INK};}}
  .bracket{{font-size:13px;font-style:italic;fill:{MUTED};}}
  .note{{font-size:13.5px;font-style:italic;fill:{MUTED};}}'''
    html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>Draft: nested systems around an AI agent</title>
<!-- Draft generated by scripts/gen_nested_rings.py; not yet in the paper. -->
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
